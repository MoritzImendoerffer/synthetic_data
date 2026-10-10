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


def test_each_registered_influence_analysis_is_backed_by_the_data():
    """Every 'influence analysis' discrepancy rests on at least one adequate selected model of an output
    with a criterion that fails criterion 4 of PCMP-001 §7.2 (residual patterns, influential runs)."""
    import doe_report as D
    import _pcpkg as P
    for doc, ds in P.PLAN_DISCREPANCIES.items():
        for d in ds:
            if "influence analysis" not in d["subject"]:
                continue
            key = d["step"]
            failing = []
            for resp in D.responses(key):
                if D._judging(key, resp) is None:
                    continue
                r = D.fit(key, "rsm", resp)
                if r["status"] == "none":
                    continue
                if D.residual_influence(key, resp)["met"] is False:
                    failing.append(resp)
            assert failing, f"{doc} {d['id']}: no selected model of {key} fails criterion 4"


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
