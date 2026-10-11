"""Rev 2.0 intermediate acceptance criteria: a priori, loosened by data only through the stated
widening rule, and the Rev 1.0 criteria they replace reproduced exactly.

INV-001's central finding is that the Rev 1.0 criteria were fitted to the data they judged. These
tests are the reason the same cannot be said of Rev 2.0.
"""
from __future__ import annotations

import builtins
import os

import numpy as np
import pandas as pd
import pytest

from amab_process import iac
from amab_process.config import load_config

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "outputs", "data")
CFG = load_config()


def test_derive_reads_no_file(monkeypatch):
    """derive() must not be able to see outputs/: any file open fails the test."""
    def refuse(*a, **k):
        raise AssertionError(f"derive() opened a file: {a[:1]}")
    monkeypatch.setattr(builtins, "open", refuse)
    monkeypatch.setattr(pd, "read_csv", refuse)
    t = iac.derive(CFG)
    assert len(t) > 0


def test_no_margin_anywhere_in_the_rule():
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                assert k != "margin", "a tuned margin is what INV-001 retired"
                walk(v)
    walk(CFG.raw()["iac"])


def test_viral_claims_meet_the_cumulative_requirement():
    c = iac.cumulative_claims(CFG)
    assert c["met"].all(), c.to_string()


def test_final_loosens_only_by_the_widening_rule():
    """A criterion may widen only where allow_widening is on and the 95 % confidence bound of the
    A-Mab worst case beats the platform value (owner's decision 2026-10-08). Any other loosening is
    a criterion fitted to its data, which is INV-001's finding."""
    t = pd.read_csv(os.path.join(DATA, "iac.csv"))
    v = pd.read_csv(os.path.join(DATA, "iac_verification.csv"))
    loose = (t["iac_high"] > t["iac_high_apriori"] + 1e-12) | (t["iac_low"] < t["iac_low_apriori"] - 1e-12)
    assert (~loose | t["widened"]).all()          # loosened only where a widening reached it
    if not CFG.raw()["iac"].get("allow_widening", False):
        assert not loose.any()
    else:
        assert v["widening_supported"].fillna(False).astype(bool).any() or not loose.any()


def test_widening_uses_the_bound_not_the_point_prediction():
    v = pd.read_csv(os.path.join(DATA, "iac_verification.csv"))
    f = iac.final(CFG, v)
    v2 = v.copy()
    v2["predicted_nor_bound95"] = v2["predicted_nor"]   # a point-prediction widening would move
    g = iac.final(CFG, v2)
    if f["widened"].any():
        assert not np.allclose(f["iac_high"], g["iac_high"])


def test_tightening_only_where_verification_failed():
    v = pd.read_csv(os.path.join(DATA, "iac_verification.csv"))
    t = pd.read_csv(os.path.join(DATA, "iac.csv"))
    failed = set(v.loc[v["met"] == False, "cqa"])  # noqa: E712
    assert set(t.loc[t["tightened"], "cqa"]) <= failed


def test_final_is_apriori_when_every_assumption_holds():
    v = pd.read_csv(os.path.join(DATA, "iac_verification.csv"))
    v["met"] = True
    v["widening_supported"] = False
    f = iac.final(CFG, v)
    assert not f["tightened"].any() and not f["widened"].any()
    assert np.allclose(f["iac_high"], f["iac_high_apriori"])


def test_rev1_criteria_reproduce_what_rev1_printed():
    """PCR-007 Rev 1.0 section 7.1 printed 193 ng/mg and 1 % HMW for the CEX pool."""
    r = pd.read_csv(os.path.join(DATA, "criteria_rev1.csv"))
    cex = r[r["step_key"] == "cex"].set_index("response")
    assert round(cex.loc["hcp_out_ng_mg", "high"]) == 193
    assert cex.loc["aggregate_out_pct", "high"] == pytest.approx(1.0)
    assert cex.loc["aggregate_out_pct", "margin"] == pytest.approx(5.0)


def test_widening_needs_an_adequate_model():
    """A widening rests on a model that passes the adequacy tests of PCMP-001 (PCR-005 review)."""
    v = pd.read_csv(os.path.join(DATA, "iac_verification.csv"))
    w = v[v["widening_supported"] == True]  # noqa: E712
    assert (w["model_adequate"] == True).all()  # noqa: E712


# --------------------------------------------------------------------------------------
# Owner's decisions of 2026-10-11: folds and increases at manufacturing scale, the UF/DF aggregate
# allowance, and NORs that offsets do not move
# --------------------------------------------------------------------------------------
def _rsm(key):
    return pd.read_csv(os.path.join(DATA, f"doe_{key}_rsm.csv"))


@pytest.mark.parametrize("step,col,mode", [("cex", "hcp_out_ng_mg", "fold"),
                                           ("cex", "aggregate_out_pct", "fold"),
                                           ("aex", "hcp_out_ng_mg", "fold"),
                                           ("viral_inactivation", "aggregate_out_pct", "add")])
def test_verification_applies_the_scale_down_offset(step, col, mode):
    """PCMP-001 §7.1 rule 2: the scale-down pool prediction is taken to manufacturing scale before it
    is compared with the manufacturing-scale feed. A ratio offset r multiplies a fold by r; a
    difference offset d lowers an increase by d."""
    sdm = pd.read_csv(os.path.join(DATA, "sdm_qualification.csv"))
    feed = 10.0
    e0, w0, b0, _, off0 = iac._nor_worst(CFG, step, _rsm(step), col, feed, mode, sdm=None)
    e1, w1, b1, _, off = iac._nor_worst(CFG, step, _rsm(step), col, feed, mode, sdm=sdm)
    assert off0 is None and off is not None
    kind, v = off
    if kind == "ratio":
        assert (w1, b1, e1) == pytest.approx((w0 * v, b0 * v, e0 * v))
    else:
        assert (w1, b1, e1) == pytest.approx((w0 - v, b0 - v, e0 - v))


def test_every_output_with_an_offset_is_verified_with_it():
    """Every verified output the qualification measured carries its offset; fragments and outputs
    with no qualification data carry none."""
    v = pd.read_csv(os.path.join(DATA, "iac_verification.csv"))
    done = v[v["predicted_nor"].notna()]
    for _, r in done.iterrows():
        if r["cqa"] == "fragments_lmw":
            assert pd.isna(r["offset"]), r.to_dict()
        else:
            assert r["offset_scale"] in ("ratio", "difference"), r.to_dict()


def test_ufdf_aggregate_allowance():
    """PCMP-001 assumes no step after cation exchange changes aggregate. UF/DF raises it within its
    NOR: the increase is the one-sided 95 % prediction bound of a single run at the least favourable
    NOR combination of an OLS on S-UFDF-UNI2, minus the fitted mean at the set-point, and it tightens
    the cation exchange pool criterion by exactly that amount. Recomputed here independently."""
    import itertools
    import statsmodels.api as sm
    p = CFG.raw()["iac"]["platform"]["ufdf"]["aggregates_hmw"]
    study, col = p["verify"]["study"], p["verify"]["response"]
    u = pd.read_csv(os.path.join(DATA, "univariate_studies.csv"))
    u = u[u["study"] == study].copy()
    uo = CFG.unit_op("ufdf")
    fac = list(dict.fromkeys(u["parameter"]))
    for f in fac:
        u[f] = np.where(u["parameter"] == f, u["value"], uo.param(f).setpoint_characterized)
    m = sm.OLS(u[col], sm.add_constant(u[fac])).fit()
    combos = pd.DataFrame(list(itertools.product(*[[uo.param(f).nor_characterized[0],
                                                     uo.param(f).setpoint_characterized,
                                                     uo.param(f).nor_characterized[1]] for f in fac])),
                          columns=fac)
    up = m.get_prediction(sm.add_constant(combos, has_constant="add")).summary_frame(
        alpha=2 * (1 - iac.BOUND_CONFIDENCE))["obs_ci_upper"].max()
    sp = pd.DataFrame([{"const": 1.0, **{f: uo.param(f).setpoint_characterized for f in fac}}])
    inc = float(up - m.predict(sp)[0])          # the offset is a constant shift and cancels here
    v = pd.read_csv(os.path.join(DATA, "iac_verification.csv")).set_index(["step_key", "cqa"])
    r = v.loc[("ufdf", "aggregates_hmw")]
    assert r["assumed"] == 0.0
    assert r["predicted_nor_bound95"] == pytest.approx(inc, abs=1e-4)
    t = pd.read_csv(os.path.join(DATA, "iac.csv")).set_index(["step_key", "response"])
    cex = t.loc[("cex", "aggregate_out_pct")]
    if inc > 0:
        assert bool(r["met"]) is False and bool(cex["tightened"])
        assert cex["iac_high"] == pytest.approx(cex["ds_high"] - r["predicted_nor_bound95"], abs=1e-4)


def test_ufdf_diavolumes_nor_is_one_sided():
    """Diavolumes are a minimum (owner, 2026-10-11); the UF/DF combination takes the NOR high as
    its upper edge, so the NOR high must still be defined."""
    p = CFG.unit_op("ufdf").param("diavolumes")
    assert p.nor_one_sided == "low"
    assert p.nor_characterized[1] > p.setpoint_characterized


def test_protein_a_load_nor_is_not_moved_by_an_offset():
    """NORs come from production (owner, 2026-10-11). The Protein A load NOR in force is the NOR as
    characterized; the narrowing made for the scale-down offset was reversed."""
    p = CFG.unit_op("protein_a").param("load")
    assert list(p.nor) == list(p.nor_characterized)
    reg = pd.read_csv(os.path.join(DATA, "parameter_classification.csv"))
    row = reg[(reg["step"] == 5) & (reg["parameter"] == p.name)].iloc[0]
    assert (row["nor_low"], row["nor_high"]) == (row["nor_char_low"], row["nor_char_high"])
