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
    o = D.sdm_offset("protein_a", "pool_hcp_ng_mg")
    assert o["offset"] == pytest.approx(o["mean_sd"] - o["mean_m"])
    assert o["lo"] < o["offset"] < o["hi"]


def test_planned_runs_alone_are_three():
    o = D.sdm_offset("protein_a", "pool_hcp_ng_mg", studies=["S-PA-SDM"])
    assert o["n_sd"] == 3 and D.sdm_offset("protein_a", "pool_hcp_ng_mg")["n_sd"] > 3


def test_judging_moves_the_criterion_by_the_offset():
    acc = D.effective_acceptance("protein_a", "pool_hcp_ng_mg")
    j = D._judging("protein_a", "pool_hcp_ng_mg")
    d = D.sdm_offset("protein_a", "pool_hcp_ng_mg")["offset"]
    assert j[1] == pytest.approx(acc[1] + d)


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
