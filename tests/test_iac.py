"""Rev 2.0 intermediate acceptance criteria: a priori, never loosened by data, and the Rev 1.0
criteria they replace reproduced exactly.

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


def test_final_never_loosens():
    t = pd.read_csv(os.path.join(DATA, "iac.csv"))
    assert (t["iac_high"] <= t["iac_high_apriori"] + 1e-12).all()
    assert (t["iac_low"] >= t["iac_low_apriori"] - 1e-12).all()


def test_tightening_only_where_verification_failed():
    v = pd.read_csv(os.path.join(DATA, "iac_verification.csv"))
    t = pd.read_csv(os.path.join(DATA, "iac.csv"))
    failed = set(v.loc[v["met"] == False, "cqa"])  # noqa: E712
    assert set(t.loc[t["tightened"], "cqa"]) <= failed


def test_final_is_apriori_when_every_assumption_holds():
    v = pd.read_csv(os.path.join(DATA, "iac_verification.csv"))
    v["met"] = True
    f = iac.final(CFG, v)
    assert not f["tightened"].any()
    assert np.allclose(f["iac_high"], f["iac_high_apriori"])


def test_rev1_criteria_reproduce_what_rev1_printed():
    """PCR-007 Rev 1.0 section 7.1 printed 193 ng/mg and 1 % HMW for the CEX pool."""
    r = pd.read_csv(os.path.join(DATA, "criteria_rev1.csv"))
    cex = r[r["step_key"] == "cex"].set_index("response")
    assert round(cex.loc["hcp_out_ng_mg", "high"]) == 193
    assert cex.loc["aggregate_out_pct", "high"] == pytest.approx(1.0)
    assert cex.loc["aggregate_out_pct", "margin"] == pytest.approx(5.0)
