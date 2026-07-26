#!/usr/bin/env python3
"""Generate every dataset consumed by the report and the FMEA.

Deterministic: all randomness derives from the master seed in
``config/parameters.yaml`` (with fixed per-study offsets), so re-running
reproduces byte-identical CSVs. Outputs land in ``outputs/data/`` plus a
``outputs/report_values.json`` of headline scalars used inline in the report.

Usage:  python scripts/generate_data.py
"""

from __future__ import annotations

import json
import os
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from amab_process import Process, load_config          # noqa: E402
from amab_process import studies as st                  # noqa: E402
from amab_process import deviations as dv               # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "outputs", "data")
os.makedirs(DATA, exist_ok=True)


def save(df: pd.DataFrame, name: str) -> str:
    path = os.path.join(DATA, name)
    df.to_csv(path, index=False)
    print(f"  wrote {name:34s} ({len(df):>4d} rows x {df.shape[1]} cols)")
    return path


def main() -> None:
    cfg = load_config()
    proc = Process(cfg)
    print(f"A-Mab data generation — seed={cfg.seed}")
    values: dict = {"seed": cfg.seed, "product": cfg.meta["product"],
                    "commercial_scale_l": cfg.meta["commercial_scale_l"]}

    # -- 1. nominal batch + bioreactor timecourse -----------------------------
    batch = proc.nominal_batch()
    tc = proc.units[0][1].timecourse(rng=proc.rng())
    save(tc, "nominal_timecourse.csv")
    values["nominal_titer_g_per_l"] = round(float(tc["titer"].iloc[-1]), 2)
    values["peak_vcd_e6"] = round(float(tc["vcd"].max()), 2)
    values["final_viability_pct"] = round(float(tc["viability"].iloc[-1]), 1)
    values["overall_yield"] = round(float(batch.overall_yield), 3)
    values["ds_mass_kg"] = round(batch.drug_substance.product_mass_g / 1000, 1)
    values["ds_conc_g_per_l"] = batch.drug_substance.meta.get("ds_concentration_g_per_l")

    # -- 2. process summary (per-step nominal metrics) ------------------------
    rows = []
    for (key, _), sres in zip(proc.units, batch.steps):
        uo = cfg.unit_op(key)
        rows.append({"step": uo.step, "unit_operation": uo.name,
                     "step_yield": round(sres.step_yield, 3),
                     "product_mass_g": round(sres.out.product_mass_g, 0),
                     **{k: round(v, 4) for k, v in sres.metrics.items()}})
    save(pd.DataFrame(rows).sort_values("step"), "process_summary.csv")

    # -- 3. yield waterfall ----------------------------------------------------
    wf = pd.DataFrame([{"step": cfg.unit_op(k).step, "unit_operation": cfg.unit_op(k).name,
                        "step_yield": round(s.step_yield, 4),
                        "cumulative_yield": round(np.prod([x.step_yield for x in batch.steps[:i + 1]]), 4)}
                       for i, ((k, _), s) in enumerate(zip(proc.units, batch.steps))])
    save(wf.sort_values("step"), "yield_waterfall.csv")

    # -- 4. per-step DoE studies + fitted effects -----------------------------
    feeds = st.step_feeds(proc)
    doe_r2: dict = {}
    for i, key in enumerate(st.DOE_FACTORS):
        rng = proc.rng(100 + 10 * i)
        factors = st.DOE_FACTORS[key]
        scr = st.screening_doe(proc, key, feeds[key], rng)
        save(scr, f"doe_{key}_screening.csv")
        top = st.RSM_TOP.get(key, factors[:4])
        rsm = st.rsm_doe(proc, key, feeds[key], rng, top_factors=top)
        save(rsm, f"doe_{key}_rsm.csv")
        # fit effects for every response (screening for main effects)
        eff_rows = []
        for resp in st.DOE_RESPONSES[key]:
            if scr[resp].std() < 1e-9:
                continue
            fx = st.fit_effects(scr, resp, factors)
            doe_r2[f"{key}:{resp}"] = round(fx["r2"], 3)
            e = fx["effects"].reset_index().rename(columns={"index": "term"})
            e.insert(0, "response", resp)
            eff_rows.append(e)
        if eff_rows:
            save(pd.concat(eff_rows, ignore_index=True), f"effects_{key}.csv")
    values["doe_r2"] = doe_r2

    # -- 5. PPQ campaign -------------------------------------------------------
    ppq = st.ppq_batches(proc)
    save(ppq.round(5), "ppq_batches.csv")
    values["n_ppq"] = len(ppq)

    # -- 6. Monte-Carlo commercial batches + capability -----------------------
    n_mc = int(cfg.meta["n_monte_carlo"])
    mc = st.monte_carlo(proc, n=n_mc)
    save(mc.round(6), "monte_carlo.csv")
    cap = st.capability(mc, cfg)
    save(cap.round(4), "capability.csv")
    values["n_monte_carlo"] = n_mc
    values["min_cpk"] = round(float(cap["Cpk"].min()), 2)
    values["all_cpk_ge_1_33"] = bool((cap["Cpk"] >= 1.33).all())

    # -- 7. viral clearance summary (nominal per-step) ------------------------
    def lrf(step_key, metric):
        return round(float(batch.step(step_key).metrics.get(metric, 0.0)), 2)
    vc = pd.DataFrame([
        {"step": "Low-pH Viral Inactivation", "XMuLV": lrf("viral_inactivation", "xmulv_lrf"), "MVM": 0.0},
        {"step": "Anion Exchange (AEX)", "XMuLV": lrf("aex", "xmulv_lrf"), "MVM": lrf("aex", "mvm_lrf")},
        {"step": "Virus Filtration", "XMuLV": lrf("virus_filtration", "xmulv_lrf"), "MVM": lrf("virus_filtration", "mvm_lrf")},
    ])
    vc.loc["Total"] = ["Cumulative", round(vc["XMuLV"].sum(), 2), round(vc["MVM"].sum(), 2)]
    save(vc.reset_index(drop=True), "viral_clearance.csv")
    values["total_lrv_xmulv"] = round(vc["XMuLV"][:3].sum(), 2)
    values["total_lrv_mvm"] = round(vc["MVM"][:3].sum(), 2)

    # -- 8. parameter classification register ---------------------------------
    prows = []
    for key in cfg.train_order:
        uo = cfg.unit_op(key)
        for p in uo.parameters:
            prows.append({"step": uo.step, "unit_operation": uo.name,
                          "parameter": p.name, "unit": p.unit, "setpoint": p.setpoint,
                          "nor_low": p.nor[0], "nor_high": p.nor[1],
                          "par_low": p.par[0], "par_high": p.par[1],
                          "classification": p.classification, "study": p.study})
    preg = pd.DataFrame(prows)
    save(preg, "parameter_classification.csv")
    cls_counts = preg["classification"].value_counts().to_dict()
    values["param_class_counts"] = {k: int(v) for k, v in cls_counts.items()}
    values["n_parameters"] = int(len(preg))
    values["n_cpp"] = int((preg["classification"].isin(["CPP", "WC-CPP"])).sum())

    # -- 9. CQA register (from config) ----------------------------------------
    crows = []
    for c in cfg.cqas:
        crows.append({"cqa": c["name"], "key": c["key"], "unit": c["unit"],
                      "category": c["category"], "acc_low": c["acceptance"][0],
                      "acc_high": c["acceptance"][1], "criticality": c["criticality_level"],
                      "tool1_score": c.get("tool1_score"), "tool2_severity": c.get("tool2_severity"),
                      "set_by": c.get("set_by"), "spec_type": st.spec_type(c["key"])})
    save(pd.DataFrame(crows), "cqa_register.csv")

    # -- 10. messy-campaign facts (deviations + supporting records) -----------
    devbuild = dv.build(cfg)
    for name, df in devbuild["tables"].items():
        save(df, name)
    values["dev_scalars"] = devbuild["scalars"]
    values["n_deviations"] = int(len(devbuild["tables"]["deviations.csv"]))

    # -- write headline values -------------------------------------------------
    with open(os.path.join(ROOT, "outputs", "report_values.json"), "w") as fh:
        json.dump(values, fh, indent=2)
    print(f"\nheadline values -> outputs/report_values.json")
    print(f"  overall yield {values['overall_yield']:.1%} | DS {values['ds_mass_kg']} kg | "
          f"titer {values['nominal_titer_g_per_l']} g/L | min Cpk {values['min_cpk']} | "
          f"CPPs {values['n_cpp']}/{values['n_parameters']}")
    print(f"  viral clearance: XMuLV {values['total_lrv_xmulv']} (>16.7), MVM {values['total_lrv_mvm']} (>8.6)")


if __name__ == "__main__":
    main()
