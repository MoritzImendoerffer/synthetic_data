"""Reproducibility and correctness tests for the A-Mab process model."""

import math
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from amab_process import Process, load_config
from amab_process import studies as st

CFG = load_config()


@pytest.fixture(scope="module")
def proc():
    return Process(CFG)


def test_config_integrity():
    """Every process parameter has a valid range, NOR within PAR, and a classification."""
    for key in CFG.train_order:
        uo = CFG.unit_op(key)
        for p in uo.parameters:
            lo, hi = p.prange
            assert lo <= hi, f"{key}.{p.key} bad range"
            assert p.nor[0] <= p.nor[1]
            assert lo - 1e-9 <= p.nor[0] and p.nor[1] <= hi + 1e-9, f"{key}.{p.key} NOR outside PAR"
            assert p.classification in {"CPP", "WC-CPP", "KPP", "GPP", "non-CPP"}


def test_reproducible(proc):
    """Same seed -> identical drug-substance CQAs."""
    a = proc.nominal_batch().drug_substance.cqas
    b = proc.nominal_batch().drug_substance.cqas
    assert a.keys() == b.keys()
    for k in a:
        assert math.isclose(a[k], b[k], rel_tol=1e-12), k


def test_mass_balance(proc):
    """Per-step yields are physical and overall yield is reasonable."""
    batch = proc.nominal_batch()
    for s in batch.steps:
        assert 0.5 <= s.step_yield <= 1.0, f"{s.step} yield {s.step_yield}"
    assert 0.6 <= batch.overall_yield <= 0.95


def test_cqas_in_spec_at_nominal(proc):
    """All CQAs meet acceptance at the nominal (set-point) operating condition."""
    ds = proc.nominal_batch().drug_substance.cqas
    for c in CFG.cqas:
        v = ds.get(c["key"])
        assert v is not None, c["key"]
        lo, hi = c["acceptance"]
        if c["key"].startswith("lrv"):
            assert v >= lo, f"{c['key']} {v} < {lo}"
        else:
            assert lo - 1e-9 <= v <= hi + 1e-9, f"{c['key']} {v} not in [{lo},{hi}]"


def test_viral_clearance_margin(proc):
    """Cumulative viral clearance exceeds the total requirements with margin."""
    ds = proc.nominal_batch().drug_substance.cqas
    assert ds["lrv_xmulv"] > 16.7
    assert ds["lrv_mvm"] > 8.6


def test_capability_all_pass(proc):
    """Monte-Carlo capability: every CQA has Cpk >= 1.0 (min target 1.33)."""
    mc = st.monte_carlo(proc, n=300)
    cap = st.capability(mc, CFG)
    assert (cap["Cpk"] >= 1.0).all(), cap[["cqa", "Cpk"]].to_string()


def test_bioreactor_effect_directions(proc):
    """Screening DoE reproduces known A-Mab effect directions (culture duration
    lowers afucosylation and galactosylation)."""
    scr = st.screening_doe(proc, "bioreactor", None, proc.rng(7))
    fx = st.fit_effects(scr, "galactosylation", st.DOE_FACTORS["bioreactor"])
    dur = fx["effects"].loc["duration", "effect"]
    assert dur < 0, "culture duration should lower galactosylation"
    assert fx["r2"] > 0.8


def test_protein_a_hcp_load_ph(proc):
    """Protein A pool HCP rises with higher load and lower elution pH."""
    unit = dict(proc.units)["protein_a"]
    feed = st.step_feeds(proc)["protein_a"]
    low = unit.run(feed.copy(), proc.rng(1), setpoints={"load": 15, "elution_ph": 3.9}).out.cqas["hcp"]
    high = unit.run(feed.copy(), proc.rng(1), setpoints={"load": 50, "elution_ph": 3.2}).out.cqas["hcp"]
    assert high > low
