"""Scale-down offsets (owner's decision 2026-10-08): the offset is applied to every Version 2.0
judgement, never to a Version 1.0 one, and the qualification is decision-based."""
from __future__ import annotations

import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pc_package"))

import doe_report as D  # noqa: E402
import tables as T  # noqa: E402


def test_offset_is_scale_down_minus_manufacturing():
    """On the scale the output is modelled on: a difference for leached Protein A, and a ratio of
    geometric means for pool host cell protein, which PCR-005 models on the log scale (PD-005-03)."""
    o = D.sdm_offset("protein_a", "leached_protein_a_ppm")
    assert o["scale"] == "difference"
    assert o["offset"] == pytest.approx(o["mean_sd"] - o["mean_m"])
    assert o["lo"] < o["offset"] < o["hi"]
    h = D.sdm_offset("protein_a", "pool_hcp_ng_mg")
    assert D.fit("protein_a", "rsm", "pool_hcp_ng_mg")["transform"] == "log"
    assert h["scale"] == "ratio"
    assert h["offset"] == pytest.approx(h["mean_sd"] / h["mean_m"])
    assert h["lo"] < h["offset"] < h["hi"]


def test_planned_runs_alone_are_three():
    o = D.sdm_offset("protein_a", "pool_hcp_ng_mg", studies=["S-PA-SDM"])
    assert o["n_sd"] == 3 and D.sdm_offset("protein_a", "pool_hcp_ng_mg")["n_sd"] > 3


def test_judging_moves_the_criterion_by_the_offset():
    acc = D.effective_acceptance("protein_a", "leached_protein_a_ppm")
    j = D._judging("protein_a", "leached_protein_a_ppm")
    d = D.sdm_offset("protein_a", "leached_protein_a_ppm")["offset"]
    assert j[1] == pytest.approx(acc[1] + d)
    # a ratio scales the criterion: y_sd / r <= criterion  <=>  y_sd <= criterion * r
    acc = D.effective_acceptance("protein_a", "pool_hcp_ng_mg")
    j = D._judging("protein_a", "pool_hcp_ng_mg")
    r = D.sdm_offset("protein_a", "pool_hcp_ng_mg")["offset"]
    assert j[1] == pytest.approx(acc[1] * r)


def test_back_transformed_limits_keep_their_coverage():
    """A log-scale model gives the interval on the log scale, back-transformed: the limits are the
    exponentials of the log-scale limits (exp is increasing), and the centre is the median."""
    import numpy as np
    r = D.fit("protein_a", "rsm", "pool_hcp_ng_mg")
    m, lo, hi = D.prediction_interval("protein_a", "pool_hcp_ng_mg", {"load": [36.0]})
    sf = r["model"].get_prediction(D._design_matrix(r, __import__("pandas").DataFrame(
        {f: [D._to_coded(36.0, "protein_a", f) if f == "load" else 0.0] for f in r["factors"]}))).summary_frame(alpha=0.05)
    assert np.allclose([m[0], lo[0], hi[0]], np.exp(sf[["mean", "obs_ci_lower", "obs_ci_upper"]].iloc[0].to_numpy()))
    assert hi[0] - m[0] > m[0] - lo[0]          # asymmetric in ng/mg, as a skewed quantity is


def test_version_1_judgement_has_no_offset():
    with D.rev1_criteria_in_force():
        assert D._offset_value("protein_a", "pool_hcp_ng_mg") == 0.0


def test_no_offset_without_sdm_data():
    assert D._offset_value("virus_filtration", "mvm_lrf") == 0.0


def test_qualified_means_same_conclusion_at_both_ends():
    t = T.sdm_offsets_data()
    j = t[t["judged"]]
    assert ((j["met_lo"] == j["met_point"]) & (j["met_point"] == j["met_hi"]) == j["qualified"]).all()


def test_pp_study_map_covers_every_parameter():
    from amab_process import load_config
    cfg = load_config()
    m = T.pp_study_map()
    n = sum(len(cfg.unit_op(s).parameters) for s in T.STEP_NAME)
    assert len(m) == n
    assert all(a <= s for a, s in zip(m["affected"], m["studied"]))
