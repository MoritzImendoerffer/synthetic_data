"""INV-002: model adequacy (PCMP-001 §7.2), the refit, the sample size and the augmentation.

The generator plans and runs the augmentations; the report engine judges with the model each
response ends up with. Both import ``amab_process.adequacy``. These tests hold the properties a
reader of INV-002 relies on.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import pytest

from amab_process import adequacy as ad
from amab_process.config import load_config

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "outputs", "data")
CFG = load_config()
TH = {k: float(v) for k, v in CFG.raw()["campaign"]["thresholds"].items()}
MA = CFG.raw()["campaign"]["model_adequacy"]


def _csv(name):
    return pd.read_csv(os.path.join(DATA, name))


def test_refit_keeps_hierarchy_and_the_block():
    """No interaction or square without its main effects, and the block is never removed."""
    rsm = _csv("doe_bioreactor_rsm.csv").assign(block=1)
    aug = _csv("doe_bioreactor_aug.csv")
    d = pd.concat([rsm, aug[[c for c in aug.columns if c in rsm.columns]]], ignore_index=True)
    f = [c[6:] for c in rsm.columns if c.startswith("coded_")]
    for resp in ("high_mannose", "acidic_variants", "afucosylation"):
        terms = ad.reduce(d, resp, f, ad.full_terms(f), TH["effect_alpha"])
        for t in terms:
            assert set(ad.parents(t)) <= set(terms), (resp, t)
        fit = ad.adequacy(d, resp, f, terms, TH)
        assert fit["block"] and "block" in fit["model"].params.index


def test_d_optimal_augmentation_is_deterministic_and_on_the_design_levels():
    rsm = _csv("doe_aex_rsm.csv")
    pts = rsm[[c for c in rsm.columns if c.startswith("coded_")]].to_numpy(float)
    a, b = ad.d_optimal_augment(pts, 8), ad.d_optimal_augment(pts, 8)
    assert np.array_equal(a, b)
    assert set(np.unique(a)) <= {-1.0, 0.0, 1.0}


def test_plan_follows_the_rule():
    """Every failing model has a remedy by the rule; viral clearance is never augmented; an
    augmented step has the largest size any of its models needs, within the planned design."""
    m = _csv("model_adequacy.csv")
    bad = m[~m["adequate"].astype(bool)]
    assert set(bad["remedy"]) <= {"augment", "refit"}
    assert (m[m["adequate"].astype(bool)]["remedy"] == "none").all()
    assert not bad[bad["response"].isin(MA["not_specification"])]["remedy"].eq("augment").any()
    plan = _csv("augmentation_plan.csv")
    for _, r in plan.iterrows():
        need = bad[(bad["step_key"] == r["step_key"]) & (bad["remedy"] == "augment")]["m_required"]
        assert r["m"] == need.max() and r["m"] <= r["n_planned"]
        aug = _csv(f"doe_{r['step_key']}_aug.csv")
        assert len(aug) == r["m"] and (aug["block"] == 2).all()
        assert aug["run"].min() == r["n_planned"] + 1
        for v in MA["not_specification"]:
            if v in aug.columns:
                assert aug[v].isna().all()             # no virus spiked in an augmentation


def test_assurance_reached_at_the_chosen_size():
    m = _csv("model_adequacy.csv")
    for _, r in m[m["remedy"] == "augment"].iterrows():
        assert r["assurance_at_m"] >= float(MA["assurance"])


def test_augmentation_dates_inside_the_second_investigation():
    inv2 = CFG.raw()["campaign"]["investigation_2"]
    ch = _csv("study_chronology.csv")
    aug = ch[ch["kind"] == "augmentation"]
    assert len(aug) == len(_csv("augmentation_plan.csv"))
    assert (aug["start"] >= MA["decided"]).all() and (aug["end"] <= inv2["closed"]).all()


def test_engine_uses_the_adequate_model_and_reproduces_version_1():
    sys.path.insert(0, os.path.join(ROOT, "pc_package"))
    import doe_report as D
    for key in D.st.DOE_FACTORS:
        for resp in CFG.raw()["iac"]["responses"].get(key, []):
            r = D.fit(key, "rsm", resp)
            if r["status"] in ("full", "refit"):
                assert r["adequate"], (key, resp)
            with D.rev1_criteria_in_force():
                v1 = D.fit(key, "rsm", resp)
            assert v1["runs"] == "planned" and len(v1["names"]) == len(ad.full_terms(D.rsm_factors(key)))


def test_exhaustive_search_is_never_beaten_by_a_stepwise_search():
    """CA3 searches every hierarchical submodel because a stepwise search changes one term at a
    time and can stop where no single change lowers AICc although another combination of terms
    has a lower AICc. The exhaustive optimum is never worse, and on this campaign's data a
    stepwise search does stop at a worse model for some outputs (INV-002 gives the count)."""
    sys.path.insert(0, os.path.join(ROOT, "pc_package"))
    import doe_report as D
    c = D.selection_comparison()
    x = c[~c["exact"]]
    for d in ("backward", "forward"):
        assert (x[f"{d}_aicc"] >= x["aicc"] - 1e-6).all()
    assert bool((x["backward_worse"] | x["forward_worse"]).any())


def test_ca3_criteria_sensitivity_and_the_independent_checks():
    """INV-002: the criteria CA3 moved are those that differ between iac.csv and iac_full.csv; the
    sensitivity of every conclusion to them is computed, the planned-run models are checked on the
    augmentation runs they have not seen, and the verification is repeated on all runs."""
    sys.path.insert(0, os.path.join(ROOT, "pc_package"))
    import doe_report as D
    import pandas as pd
    s = D.ca3_criteria_sensitivity()
    a, f = D.csv("iac.csv"), D.csv("iac_full.csv")
    mm = a.merge(f, on=["step_key", "response"], suffixes=("", "_f"))
    moved = mm[(mm["iac_high"].round(6) != mm["iac_high_f"].round(6)) | (mm["iac_low"].round(6) != mm["iac_low_f"].round(6))]
    in_scope = set(zip(s["step_key"], s["response"]))
    assert set(zip(s[s["criterion_moved"]]["step_key"], s[s["criterion_moved"]]["response"])) == \
        {k for k in zip(moved["step_key"], moved["response"]) if k in in_scope}
    c = D.augmentation_prediction_check()
    assert set(c["step_key"]) == {k for k in D.st.DOE_FACTORS if D.has_augmentation(k)}
    assert bool((c["inside_pi"] <= c["n_new"]).all())
    v = D.verification_all_runs()
    assert set(v.dropna(subset=["predicted_nor"])["step_key"]) <= set(c["step_key"])
