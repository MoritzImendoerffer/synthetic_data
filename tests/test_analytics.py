"""Rev 2.0 analytical layer: same experiments as Rev 1.0, and a method story the data carries.

The first test is the one the whole campaign rests on. Rev 2.0 is a re-analysis of the
experiments Rev 1.0 reported, plus the measurements the method decision required. If adding the
analytical layer moved a single pre-existing value, the two revisions would describe different
experiments and the superseded set would stop being a fair comparison.

The comparison is against the CSVs committed at tag ``corpus-rev1.0``, at a relative tolerance
of 1e-12, because regenerating in a different BLAS build drifts the last digit (RUNNER.md,
"Output-drift caution") and that drift is not a change of experiment.
"""
from __future__ import annotations

import io
import os
import subprocess

import numpy as np
import pandas as pd
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "outputs", "data")
TAG = "corpus-rev1.0"

SHARED = ["doe_bioreactor_screening", "doe_bioreactor_rsm", "doe_protein_a_screening",
          "doe_protein_a_rsm", "doe_viral_inactivation_screening", "doe_viral_inactivation_rsm",
          "doe_cex_screening", "doe_cex_rsm", "doe_aex_screening", "doe_aex_rsm",
          "doe_aex_screening_superseded", "doe_aex_rsm_superseded",
          "doe_virus_filtration_screening", "doe_virus_filtration_rsm",
          "monte_carlo", "ppq_batches", "process_summary", "viral_clearance"]


def _at_tag(name):
    try:
        raw = subprocess.run(["git", "show", f"{TAG}:outputs/data/{name}.csv"], cwd=ROOT,
                             capture_output=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.skip(f"tag {TAG} not available")
    return pd.read_csv(io.BytesIO(raw))


@pytest.mark.parametrize("name", SHARED)
def test_rev1_experiments_unchanged(name):
    old = _at_tag(name)
    new = pd.read_csv(os.path.join(DATA, f"{name}.csv"))
    assert len(new) == len(old)
    for col in old.columns:
        assert col in new.columns, f"{name}: column {col} dropped"
        a, b = old[col], new[col]
        if pd.api.types.is_numeric_dtype(a):
            assert np.allclose(a, b, rtol=1e-12, atol=0, equal_nan=True), f"{name}.{col} moved"
        else:
            assert (a.astype(str) == b.astype(str)).all(), f"{name}.{col} moved"


def test_effects_rows_unchanged():
    for key in ["bioreactor", "protein_a", "viral_inactivation", "cex", "aex", "virus_filtration"]:
        old = _at_tag(f"effects_{key}")
        new = pd.read_csv(os.path.join(DATA, f"effects_{key}.csv"))
        new = new[new["response"].isin(set(old["response"]))].reset_index(drop=True)
        assert np.allclose(old["effect"], new["effect"], rtol=1e-9), key


def _cmp():
    return pd.read_csv(os.path.join(DATA, "cex_fraction_comparability.csv"))


def test_sec_biased_high_in_capture_matrices():
    """The finding behind AMD-001: SEC reads high where HCP and leached ligand co-elute."""
    c = _cmp()
    for sample in ("Protein A pool", "VI pool"):
        d = c[c["sample"] == sample]["difference"]
        assert d.mean() > 0.25, f"{sample}: bias {d.mean():.3f} too small to have been noticed"


def test_sec_bias_bounded_by_hcp_mass():
    """The bias can never exceed the host cell protein mass in the sample (1e4 ng/mg = 1 %)."""
    from amab_process import analytics as an
    from amab_process.config import load_config
    for hcp in (100.0, 9000.0, 25000.0):
        assert an.sec_bias(load_config(), hcp) <= hcp / 1e4


def test_sec_agrees_after_cex():
    """From the CEX pool onward SEC agrees with CE-SDS within the CE-SDS precision."""
    import yaml
    cfg = yaml.safe_load(open(os.path.join(ROOT, "config", "parameters.yaml")))
    sd = cfg["analytics"]["methods"]["cesds"]["sd_abs"]
    c = _cmp()
    for sample in ("CEX pool", "AEX pool"):
        assert abs(c[c["sample"] == sample]["difference"].mean()) < 2 * sd, sample


def test_method_plan_matches_the_columns():
    """A cell is NaN exactly where the plan says the method did not run."""
    plan = pd.read_csv(os.path.join(DATA, "method_plan.csv")).set_index("study")
    from amab_process.analytics import STUDY_ID
    for (step, kind), sid in STUDY_ID.items():
        if kind == "superseded" or sid not in plan.index or not plan.loc[sid, "lmw_in_scope"]:
            continue
        df = pd.read_csv(os.path.join(DATA, f"doe_{step}_{kind}.csv"))
        assert df["lmw_sec_pct"].notna().all() == bool(plan.loc[sid, "lmw_sec"]), sid
        assert df["lmw_cesds_pct"].notna().all() == bool(plan.loc[sid, "lmw_cesds"]), sid


def test_repeated_aex_doe_switched_method():
    """The owner's example: the repeated DoE has CE-SDS, the invalidated first one SEC."""
    first = pd.read_csv(os.path.join(DATA, "doe_aex_rsm_superseded.csv"))
    again = pd.read_csv(os.path.join(DATA, "doe_aex_rsm.csv"))
    assert first["lmw_sec_pct"].notna().all() and first["lmw_cesds_pct"].isna().all()
    assert again["lmw_cesds_pct"].notna().all() and again["lmw_sec_pct"].isna().all()


def test_chronology_resolves_calibration_tension():
    """Every study ran before the cal_due of the equipment it used and before Rev 1.0."""
    import yaml
    cfg = yaml.safe_load(open(os.path.join(ROOT, "config", "parameters.yaml")))
    due = {e["id"]: e["cal_due"] for e in cfg["deviations"]["equipment"]}
    rev1 = cfg["campaign"]["revisions"][0]["effective"]
    supplementary = {v["study"] for v in cfg["analytics"]["sdm"].get("supplementary", {}).values()}
    closed = cfg["campaign"]["investigation"]["closed"]
    for s in cfg["campaign"]["studies"]:
        if s["id"] in supplementary:
            # runs a deviation added during the investigation: after Version 1.0, before closure
            assert rev1 < s["start"] <= s["end"] < closed, s["id"]
            continue
        assert s["start"] <= s["end"] < rev1, s["id"]
        if s.get("equipment"):
            assert s["end"] < due[s["equipment"]], s["id"]


def test_method_decision_between_comparability_and_aex_repeat():
    import yaml
    cfg = yaml.safe_load(open(os.path.join(ROOT, "config", "parameters.yaml")))
    st = {s["id"]: s for s in cfg["campaign"]["studies"]}
    d = cfg["campaign"]["method_decision"]["date"]
    assert st["S-CEX-FRC"]["end"] < d < st["S-AEX-SCR"]["start"]
