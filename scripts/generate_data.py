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
from amab_process import analytics as an                # noqa: E402
from amab_process import iac as ia                      # noqa: E402
from amab_process import adequacy as ad                 # noqa: E402

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
    ps = pd.DataFrame(rows).sort_values("step")
    save(ps, "process_summary.csv")

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
        top = st.RSM_TOP.get(key, factors[:4])
        rsm = st.rsm_doe(proc, key, feeds[key], rng, top_factors=top)
        # Rev 2.0 analytical layer: fragment columns per the method plan, drawn from their own
        # streams AFTER both designs ran, so the shared DoE stream above is untouched.
        scr = an.annotate_doe(cfg, key, "screening", scr, ps)
        rsm = an.annotate_doe(cfg, key, "rsm", rsm, ps)
        scr["run_order"] = an.run_order(cfg, scr, 2 * i)
        rsm["run_order"] = an.run_order(cfg, rsm, 2 * i + 1)
        if key == "protein_a":
            bio_hmw = float(feeds["protein_a"].cqas.get("aggregates_hmw", 1.5))
            scr = an.protein_a_extras(cfg, scr, "screening", bio_hmw)
            rsm = an.protein_a_extras(cfg, rsm, "rsm", bio_hmw)
        save(scr, f"doe_{key}_screening.csv")
        save(rsm, f"doe_{key}_rsm.csv")
        # fit effects for every response (screening for main effects)
        eff_rows = []
        extra = [c for c in (an.LMW_SEC, an.LMW_CE) if c in scr.columns and scr[c].notna().all()]
        for resp in list(st.DOE_RESPONSES[key]) + extra:
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
    ppq["fragments_lmw"] = an.frag_batches(cfg, ppq, stream=0)
    save(ppq.round(5), "ppq_batches.csv")
    values["n_ppq"] = len(ppq)

    # -- 6. Monte-Carlo commercial batches + capability -----------------------
    n_mc = int(cfg.meta["n_monte_carlo"])
    mc = st.monte_carlo(proc, n=n_mc)
    mc["fragments_lmw"] = an.frag_batches(cfg, mc, stream=1)
    save(mc.round(6), "monte_carlo.csv")
    cap = st.capability(mc, cfg)
    save(cap.round(4), "capability.csv")
    # Version 1.0's simulation: the same Monte Carlo at the NOR as characterized, which is the NOR
    # Version 1.0 sampled (same stream, so it reproduces Version 1.0). Its capability fixes the
    # Version 1.0 capability-based limits and INV-001's capability findings; no Version 2.0 NOR
    # decision may move them.
    from amab_process.config import characterized_nor
    with characterized_nor():
        mc1 = st.monte_carlo(proc, n=n_mc)
    mc1["fragments_lmw"] = an.frag_batches(cfg, mc1, stream=1)
    cap1 = st.capability(mc1, cfg)
    save(cap1.round(4), "capability_rev1.csv")
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
                          "classification": p.classification, "study": p.study,
                          # the NOR and set-point as characterized, where a Version 2.0 report moved them
                          "nor_char_low": p.nor_characterized[0], "nor_char_high": p.nor_characterized[1],
                          "setpoint_char": p.setpoint_characterized})
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

    # -- 11. Rev 2.0 analytical layer: chronology, method plan, holds, comparability ------
    # INV-002: PCMP-001 §7.2 applied to every response-surface model with a criterion, on the
    # planned runs; the remedy of each failing model; the sample sizes; and the augmentation runs
    # of the steps the rule names. The planned DoE files are not touched.
    rsm_planned = {k: pd.read_csv(os.path.join(DATA, f"doe_{k}_rsm.csv")) for k in st.DOE_FACTORS}
    adq = ad.plan(cfg, rsm_planned, lambda si, ri: an._rng(cfg, 14, si, ri))
    save(adq["models"], "model_adequacy.csv")
    save(adq["grid"], "augmentation_sample_size.csv")
    save(adq["steps"], "augmentation_plan.csv")
    aug_studies = an.augmentation_studies(cfg, list(adq["steps"]["step_key"]))
    aug_id = {s_["step"]: s_["id"] for s_ in aug_studies}
    for si, key in enumerate(st.DOE_FACTORS):
        path = os.path.join(DATA, f"doe_{key}_aug.csv")
        if key in adq["designs"]:
            save(an.augmentation_runs(cfg, proc, feeds, key, adq["designs"][key], aug_id[key],
                                      len(rsm_planned[key]), si), f"doe_{key}_aug.csv")
        elif os.path.exists(path):
            os.remove(path)            # another seed augmented this step; this one does not
    save(an.chronology(cfg, aug_studies), "study_chronology.csv")
    save(an.method_plan(cfg, aug_studies), "method_plan.csv")
    for pool in cfg.raw()["analytics"]["holds"]:
        save(an.hold_study(cfg, pool, ps).round(4), f"hold_{pool}.csv")
    save(an.comparability(cfg, ps).round(4), "cex_fraction_comparability.csv")
    save(an.sdm_qualification(cfg, proc, feeds), "sdm_qualification.csv")
    # S-VI-UNI2 (PD-006-06) appended last: XMuLV clearance at the ends of the A-Mab concentration range
    save(pd.concat([an.univariate_studies(cfg, proc, feeds), an.univariate_nodoe(cfg, proc, feeds),
                    an.vi_concentration_xmulv(cfg, proc, feeds)], ignore_index=True),
         "univariate_studies.csv")
    values["fragments_nominal"] = {k: round(v, 3) for k, v in an.nominal_train(cfg).items()}

    # -- 12. Rev 2.0 intermediate acceptance criteria (config only), Rev 1.0 criteria (data),
    #        verification of the platform worst cases, integrated-model P(OOS) --------------
    save(ia.derive(cfg), "iac_apriori.csv")
    save(ia.cumulative_claims(cfg), "iac_viral_cumulative.csv")
    save(ia.rev1_criteria(cfg, ps, cap1, vc.reset_index(drop=True)).round(4), "criteria_rev1.csv")
    rsm_data = {k: pd.read_csv(os.path.join(ROOT, "outputs", "data", f"doe_{k}_rsm.csv"))
                for k in st.DOE_FACTORS}
    # the rule in force (owner, 2026-10-09): a criterion is tightened or widened on the one-sided 95 %
    # prediction bound of a single batch (PCMP-001 §7.5)
    ver = ia.verification(cfg, rsm_data, ps, an.nominal_train(cfg),
                          vi_feed_acidic=feeds["viral_inactivation"].cqas["acidic_variants"], bound="batch")
    save(ver.round(4), "iac_verification.csv")
    save(ia.final(cfg, ver), "iac.csv")
    # the same verification on the full quadratic models the plans prescribe: the criteria as they
    # would have been without INV-002 corrective action CA3 (adopted before INV-001 closed, so the
    # criteria in force rest on the selected models); INV-002 compares the two
    ver_full = ia.verification(cfg, rsm_data, ps, an.nominal_train(cfg),
                               vi_feed_acidic=feeds["viral_inactivation"].cqas["acidic_variants"],
                               form="full", bound="batch")
    save(ver_full.round(4), "iac_verification_full.csv")
    save(ia.final(cfg, ver_full), "iac_full.csv")
    save(ia.p_oos(cfg, mc), "p_oos.csv")
    save(ia.p_oos(cfg, mc1), "p_oos_rev1.csv")        # the simulation at the NOR as characterized

    # -- 13. Version 2.0 support for the re-centred low-pH set-points (PCR-006, PD-006-01/02) ------
    save(an.vi_ofat(cfg, proc, feeds).round(4), "vi_ofat.csv")
    vcfg = cfg.raw()["analytics"]["cex_verification"]
    thr = {k: float(v) for k, v in cfg.raw()["campaign"]["thresholds"].items()}
    cex_rsm = rsm_planned["cex"]
    cfac = [c[len("coded_"):] for c in cex_rsm.columns if c.startswith("coded_")]
    vrow = ver.set_index(["step_key", "cqa"])
    allow_w = bool(cfg.raw()["iac"].get("allow_widening", False))

    def relied_on(cqa):
        r = vrow.loc[("cex", cqa)]
        moved = (r["met"] is False or r["met"] == False) or (allow_w and bool(r["widening_supported"]))  # noqa: E712
        return float(r["predicted_nor_bound95"]) if moved else float(r["assumed"])

    vgrid, ns = [], []
    nom_frag = an.nominal_train(cfg)
    for k_, cqa in enumerate(vcfg["attributes"]):
        if cqa == "aggregates_hmw":
            # the fold the CEX data show at set-point, and its run-to-run SD, from the selected model
            sel = ad.select_model(cex_rsm, "aggregate_out_pct", cfac, thr)
            sp = pd.DataFrame([{"coded_" + f_: float(np.ravel(an._coded(cfg, "cex", f_, cfg.unit_op("cex").param(f_).setpoint_characterized))[0]) for f_ in cfac}])
            lin = float((ad.matrix(sp, sel["terms"]).to_numpy() @ sel["model"].params.to_numpy())[0])
            feed = float(ps.set_index("step").loc[6, "aggregate_out_pct"])
            out = np.exp(lin) if sel["scale"] == "log" else lin
            sigma = float(np.sqrt(sel["model"].mse_resid)) if sel["scale"] == "log" else float(np.sqrt(sel["model"].mse_resid) / out)
            f_data = feed / out
        else:
            # fragments have no adequate CEX model: the fold and its SD from the centre points, with the
            # nrCE-SDS repeatability on the load
            cen = cex_rsm[cex_rsm["run_type"] == "center"]["lmw_cesds_pct"].to_numpy(float)
            feed = float(nom_frag["viral_inactivation"])
            lf = np.log(feed / cen)
            sigma = float(np.sqrt(lf.var(ddof=1) + (cfg.raw()["analytics"]["methods"]["cesds"]["sd_abs"] / feed) ** 2))
            f_data = float(np.exp(lf.mean()))
        f_req = relied_on(cqa)
        res = ad.verification_runs(f_data, f_req, sigma, int(vcfg["n_max"]), float(vcfg["power"]),
                                   int(vcfg["reps"]), an._rng(cfg, 17, k_))
        for g_ in res["grid"]:
            vgrid.append({"cqa": cqa, "f_data": f_data, "f_required": f_req, "sigma_ln": sigma, **g_,
                          "n_required": res["n"]})
        ns.append(res["n"] if res["n"] is not None else int(vcfg["n_max"]))
    save(pd.DataFrame(vgrid).round(5), "cex_verification_n.csv")
    save(an.cex_verification(cfg, proc, feeds, max(ns)).round(5), "cex_verification.csv")

    # -- 14. The owner's decisions of 2026-10-09: worst-case confirmation runs after the hold-time NOR
    #        was revised (PD-006-03), and the osmolality study (PD-003-01) --------------------------
    save(an.vi_worst_case(cfg, proc, feeds, max(ns)).round(5), "vi_worst_case.csv")
    save(an.osmolality_study(cfg, proc, feeds).round(5), "osmolality_study.csv")

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
