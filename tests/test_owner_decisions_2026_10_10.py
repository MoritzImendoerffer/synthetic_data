"""The owner's decisions of 2026-10-10 (Q2, Q3, Q4, Q7, Q8 and the influence analyses), held by the data.

Each test names the decision it holds. A seed or config change that breaks one of these properties
must be argued, not absorbed: the documents state these facts.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import pytest

from amab_process.config import load_config

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "outputs", "data")
sys.path.insert(0, os.path.join(ROOT, "pc_package"))
CFG = load_config()
DOE_STEPS = ["bioreactor", "protein_a", "viral_inactivation", "cex", "aex", "virus_filtration"]


def _csv(name):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        pytest.skip(f"{name} missing; run make data")
    return pd.read_csv(path)


def test_q4_dna_is_carried_in_pg_per_mg_and_judged_per_dose():
    """Q4: the dose converts pg/mg to ng/dose, and the drug substance meets A-Mab's < 1e-3 ng/dose."""
    import _pcpkg as P
    from amab_process.unit_ops.ufdf import dna_ng_per_dose
    d = CFG.meta["dose"]
    assert P.DOSE_MG == float(d["mg_per_kg"]) * float(d["body_weight_kg"])
    assert dna_ng_per_dose(CFG, 1.0) == pytest.approx(P.DOSE_MG / 1000.0)
    # the capture load of the design data is the harvest DNA of the model
    pa = _csv("doe_protein_a_rsm.csv")["dna_load_pg_mg"].dropna()
    harvest = float(CFG.process["bioreactor"]["rsm"]["harvest_centre"]["residual_dna_pg_mg"])
    assert 0.5 * harvest < pa.median() < 2.0 * harvest
    limit = [c for c in CFG.raw()["cqas"] if c["key"] == "residual_dna"][0]["acceptance"][1]
    mc = _csv("monte_carlo.csv")["residual_dna"]
    assert mc.max() < limit, "a simulated batch exceeds the drug substance DNA criterion"


def test_q3_hcp_elisa_coverage_in_the_record():
    m = _csv("dev_methods.csv").set_index("id")
    assert 0 < float(m.loc["AMV-3012", "coverage_pct"]) <= 100
    assert isinstance(m.loc["AMV-3012", "coverage_method"], str)


def test_q7_out_of_trend_rule_flags_the_first_result_and_not_the_reassay():
    """Q7: the record's trigger is checkable, and the data obey it."""
    import doe_report as D
    import _pcpkg as P
    ev = [e for e in CFG.raw()["deviations"]["events"]["PCR-005"] if e["id"] == "DEV-005-02"][0]
    run, ratio = int(ev["values"]["run"]), float(ev["values"]["first_over_reported"])
    lvl = float(ev["values"]["oot_level"])
    assert ev.get("oot_rule")
    reassay = float(D.rsm_data("protein_a", "planned").set_index("run").loc[run, "leached_protein_a_ppm"])
    assert D.oot_check("protein_a", "leached_protein_a_ppm", run, reassay * ratio, lvl)["out"]
    assert not D.oot_check("protein_a", "leached_protein_a_ppm", run, reassay, lvl)["out"]
    assert P.DEV_SCALARS["dev_005_02_first_over_reported"] == ratio


def test_q2_design_space_on_the_single_batch_limit_is_never_larger():
    """Q2: a single batch is a stricter statistic than the mean."""
    import doe_report as D
    for key in DOE_STEPS:
        b = D.design_space_grid(key, n=7)
        m = D.design_space_grid(key, n=7, basis="mean")
        assert b["basis"] == "batch"
        assert b["fraction"] <= m["fraction"] + 1e-12, key


def _failing_criterion_4(key):
    """Outputs with a criterion whose selected model fails criterion 4 of PCMP-001 §7.2 under the rule of
    the owner's decision of 2026-10-10: a residual trend at the level of the residual tests, or a run
    whose Cook's distance exceeds the median of F(p, n - p). A run above 4/n only flags it."""
    import doe_report as D
    resps = list(D.responses(key)) + [c for c in D.fragment_responses(key)
                                      if c == "lmw_cesds_pct" and c not in D.responses(key)]
    out = []
    for resp in resps:
        if D._judging(key, resp) is None or D.fit(key, "rsm", resp)["status"] == "none":
            continue
        if D.residual_influence(key, resp)["met"] is False:
            out.append(resp)
    return out


def test_residual_criterion_discrepancies_match_the_data():
    """A report carries the discrepancy 'conclusions resting on models that do not meet the criterion on
    residuals and influential runs' exactly where a selected model fails criterion 4 (owner's decision
    2026-10-10, "4/n flags, F decides"): bioreactor, Protein A, cation exchange and virus filtration;
    not low-pH inactivation or anion exchange, where every model passes."""
    import doe_report as D
    import _pcpkg as P
    from amab_process import studies as st
    for key in st.DOE_FACTORS:
        doc = f"PCR-{CFG.unit_op(key).step:03d}"
        has = any("residuals and influential runs" in d["subject"] for d in P.PLAN_DISCREPANCIES.get(doc, []))
        fails = _failing_criterion_4(key)
        assert has == bool(fails), f"{doc}: discrepancy {'present' if has else 'absent'}, failing models {fails}"


def test_cook_rule_flags_at_4_over_n_and_fails_above_the_f_median():
    """The flag and the decision are two limits: every flagged run lies below the F median except where the
    model fails, and only virus filtration MVM has a run above it."""
    import doe_report as D
    over_f = {}
    for key in ("bioreactor", "protein_a", "viral_inactivation", "cex", "aex", "virus_filtration"):
        for resp in D.responses(key):
            if D._judging(key, resp) is None or D.fit(key, "rsm", resp)["status"] == "none":
                continue
            ri = D.residual_influence(key, resp)
            if not ri.get("testable"):
                continue
            assert ri["cook_limit"] < ri["f_limit"]
            assert set(ri["over_f"]) <= set(ri["over"])
            if ri["over_f"]:
                over_f[(key, resp)] = ri["over_f"]
    assert set(over_f) == {("virus_filtration", "mvm_lrf")}, over_f


def test_q8_ufdf_qualification_and_offsets():
    """Q8: S-UFDF-SDM compares the four outputs Version 1.0 PCP-010 planned, at both scales."""
    import doe_report as D
    q = _csv("sdm_qualification.csv")
    u = q[q["step"] == "ufdf"]
    a = CFG.raw()["analytics"]["sdm"]
    assert set(u["study"]) == {"S-UFDF-SDM"}
    assert (u["scale"] == "scale-down").sum() == int(a["n_scale_down"])
    assert (u["scale"] == "manufacturing").sum() == int(a["n_manufacturing"])
    for col in ("step_yield", "aggregate_out_pct", "ds_concentration_g_per_l", "flux_lmh"):
        assert u[col].notna().all(), col
    assert D.sdm_offset("ufdf", "aggregate_out_pct") is not None


def test_q5_univariate_studies_measure_what_their_plans_required():
    """Q5: size variants by the method of the time (analytics.plan) in the univariate studies of the
    designed steps; the spiked AEX run at the high flow rate; the harvest and UF/DF attributes in scope."""
    u = _csv("univariate_studies.csv")
    plan = CFG.raw()["analytics"]["plan"]
    col = {"sec": "lmw_sec_pct", "cesds": "lmw_cesds_pct"}
    for sid in ("S-PA-UNI", "S-VI-UNI", "S-CEX-UNI", "S-AEX-UNI"):
        plan.setdefault(sid, [])
        rows = u[(u["study"] == sid) & ~(u["spiked"].fillna(False).astype(bool))]
        for meth in ("sec", "cesds"):
            has = rows[col[meth]].notna()
            assert has.all() if meth in plan[sid] else not has.any(), (sid, meth)
    sp = u[u["spiked"].fillna(False).astype(bool)]
    assert len(sp) == 1 and sp["study"].iloc[0] == "S-AEX-UNI" and sp["level"].iloc[0] == "high"
    assert sp[["xmulv_lrf", "mvm_lrf"]].notna().all(axis=None)
    har = u[u["study"] == "S-HAR-UNI2"]
    assert har[["lmw_cesds_pct", "dna_out_pg_mg"]].notna().all(axis=None)
    assert u.loc[u["study"] == "S-UFDF-UNI2", "acidic_variants"].notna().all()
    assert u.loc[u["study"] == "S-BRX-UNI", ["harvest_hcp_ng_mg", "harvest_dna_pg_mg"]].notna().all(axis=None)
    cx = u[u["study"] == "S-CEX-UNI"]
    assert (cx["dna_pool_pg_mg"].isna() == cx["dna_pool_lt_loq"].astype(bool)).all()
    assert cx["dna_load_pg_mg"].notna().all()


def test_q5_ion_exchange_impurities_and_loq():
    """Q5: DNA and leached Protein A on every response-surface pool of CEX and AEX; a pool below the
    method's LOQ carries no value and is flagged."""
    for step in ("cex", "aex"):
        d = _csv(f"doe_{step}_rsm.csv")
        for name, unit in (("dna", "pg_mg"), ("lpa", "ppm")):
            v, flag = d[f"{name}_pool_{unit}"], d[f"{name}_pool_lt_loq"].astype(bool)
            assert (v.isna() == flag).all(), (step, name)
    aex = _csv("doe_aex_rsm.csv")
    assert aex["dna_pool_lt_loq"].astype(bool).all(), "5 logs of AEX DNA clearance leave the pools below the LOQ"
