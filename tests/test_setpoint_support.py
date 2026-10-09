"""The Version 2.0 set-point decisions and the evidence behind them (owner, 2026-10-09): the PAR
margins, the worst corner of the NOR, the low-pH hold study at the re-centred pH (PD-006-01), the
cation exchange verification runs (PD-006-02), the model of an output the data give without error,
and the plan's parameter table."""
from __future__ import annotations

import os
import sys

import numpy as np
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pc_package"))

import doe_report as D  # noqa: E402
from _pcpkg import CFG, plan_params  # noqa: E402


def test_low_ph_margins_in_force_and_as_characterized():
    """In force, every NOR-propagated PAR of low-pH inactivation contains its NOR and the pH
    set-point has a margin to the XMuLV PAR edge; as characterized, XMuLV has no such PAR."""
    m = D.par_margins("viral_inactivation")
    assert bool(m["contains_nor"].all())
    x = m[(m["response"] == "xmulv_lrf") & (m["factor"] == "ph")].iloc[0]
    assert x["sp_hi"] > x["nor_hi"] > 0
    with D.characterized_nor():
        m0 = D.par_margins("viral_inactivation")
        assert not D.nor_met("viral_inactivation", "xmulv_lrf")
    assert not bool(m0[m0["response"] == "xmulv_lrf"]["contains_nor"].any())
    assert D.nor_met("viral_inactivation", "xmulv_lrf")


def test_worst_corner_agrees_with_the_nor_judgement():
    """The worst corner is judged as nor_met judges, at manufacturing scale against the
    manufacturing-scale criterion."""
    for key, resp in (("bioreactor", "acidic_variants"), ("protein_a", "pool_hcp_ng_mg"),
                      ("cex", "hcp_out_ng_mg")):
        w = D.nor_worst_corner(key, resp)
        assert w["met"] == D.nor_met(key, resp)
        assert w["criterion"] == D.effective_acceptance(key, resp)
        assert w["pi_low"] <= w["predicted"] <= w["pi_high"]


def test_bioreactor_acidic_variants_fail_on_the_interval_not_the_median():
    w = D.nor_worst_corner("bioreactor", "acidic_variants")
    assert w["side"] == "lower" and not w["met"] and w["median_met"]


def test_ofat_holm_adjustment_and_reading():
    a = D.ofat_analysis().set_index("response")
    p = a["p_ph"].sort_values()
    m = len(p)
    expect, run = {}, 0.0
    for i, (k, v) in enumerate(p.items()):
        run = max(run, min(1.0, (m - i) * v))
        expect[k] = run
    for k, v in expect.items():
        assert a.loc[k, "p_ph_holm"] == pytest.approx(v)
    alpha = float(CFG.raw()["campaign"]["thresholds"]["effect_alpha"])
    # aggregate and fragments rise with hold time and show no pH effect
    for r in ("aggregate_out_pct", "lmw_cesds_pct"):
        assert a.loc[r, "slope_60"] > 0 and a.loc[r, "p_slope"] < alpha
        assert not a.loc[r, "ph_significant"]
    # the low-pH model of acidic variants has no pH term, so an apparent pH difference must sit
    # before the hold and not grow over it
    assert "ph" not in D.fit("viral_inactivation", "rsm", "acidic_variants")["names"]
    if a.loc["acidic_variants", "ph_significant"]:
        assert a.loc["acidic_variants", "p_interaction"] >= alpha
        assert np.sign(a.loc["acidic_variants", "diff_t0"]) == np.sign(a.loc["acidic_variants", "ph_effect"])
    assert bool(a["met_nor"].all())


def test_cex_verification_decision():
    s = D.cex_verification_summary().set_index("cqa")
    assert int(s["n_runs"].iloc[0]) == int(s["n_required"].max())
    z = 1.6448536269514722
    for cqa, r in s.iterrows():
        lb = np.exp(np.mean(np.log(r["folds"])) - z * r["sigma_ln"] / np.sqrt(len(r["folds"])))
        assert r["fold_bound"] == pytest.approx(lb, rel=1e-9)
        assert r["passed"] == (r["fold_bound"] >= r["f_required"])
        assert r["alpha_at_n"] == pytest.approx(0.05, abs=0.01)   # the test holds its level
        assert r["power_at_n"] >= float(CFG.raw()["analytics"]["cex_verification"]["power"])


def test_exact_fit_takes_the_smallest_exact_model():
    """Low-pH acidic variants: every replicate identical to the precision reported, so the data
    are fitted exactly; the smallest exact model is hold time alone, and AICc is not defined."""
    f = D.fit("viral_inactivation", "rsm", "acidic_variants")
    assert f["exact"] and f["names"] == ["hold_time"] and np.isnan(f["aicc"])
    assert not D.fit("protein_a", "rsm", "pool_hcp_ng_mg")["exact"]


def test_plan_states_the_characterized_setpoint_and_nor():
    pp = plan_params("viral_inactivation").set_index("Parameter")
    for p in CFG.unit_op("viral_inactivation").parameters:
        assert float(pp.loc[p.name, "Set-point"]) == pytest.approx(p.setpoint_characterized)
        lo, hi = p.nor_characterized
        assert pp.loc[p.name, "NOR"].replace("–", "-").split("-")[0].strip() == f"{lo:g}"
