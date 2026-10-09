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

from amab_process.config import load_config

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "outputs", "data")
TAG = "corpus-rev1.0"

SHARED = ["doe_bioreactor_screening", "doe_bioreactor_rsm", "doe_protein_a_screening",
          "doe_protein_a_rsm", "doe_viral_inactivation_screening", "doe_viral_inactivation_rsm",
          "doe_cex_screening", "doe_cex_rsm", "doe_aex_screening", "doe_aex_rsm",
          "doe_aex_screening_superseded", "doe_aex_rsm_superseded",
          "doe_virus_filtration_screening", "doe_virus_filtration_rsm",
          "process_summary", "viral_clearance"]
# monte_carlo and ppq_batches left this list on 2026-10-08: they sample each parameter within the
# NOR in force, and Version 2.0 narrowed three NORs (config nor_v2, PCR-005 and PCR-006).


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
    rev2 = cfg["campaign"]["revisions"][-1]["effective"]
    # studies a report records as a discrepancy from its plan: after Version 1.0, before Version 2.0
    pd_studies = {x for ds in cfg["campaign"]["plan_discrepancies"].values() for d in ds
                  for x in d.get("studies", [])}
    for s in cfg["campaign"]["studies"]:
        if s["id"] in supplementary:
            # runs a deviation added during the investigation: after Version 1.0, before closure
            assert rev1 < s["start"] <= s["end"] < closed, s["id"]
            continue
        if s["id"] in pd_studies:
            assert rev1 < s["start"] <= s["end"] < rev2, s["id"]
            continue
        assert s["start"] <= s["end"] < rev1, s["id"]
        if s.get("equipment"):
            assert s["end"] < due[s["equipment"]], s["id"]


def test_each_plan_approved_before_its_first_study():
    """STORY_BIBLE: each plan was approved after the master plan and before its studies began
    (INV-001 finding 5). Re-dating S-BRX-SDM on 2026-10-09 once broke this for PCP-003."""
    cfg = load_config()
    raw = cfg.raw()["campaign"]
    appr = raw["plan_approval"]
    for k in cfg.train_order:
        doc = f"PCP-{cfg.unit_op(k).step:03d}"
        first = min(s["start"] for s in raw["studies"] if s["step"] == k)
        assert appr["PCMP-001"] < appr[doc] < first, (doc, appr[doc], first)


def test_method_decision_between_comparability_and_aex_repeat():
    import yaml
    cfg = yaml.safe_load(open(os.path.join(ROOT, "config", "parameters.yaml")))
    st = {s["id"]: s for s in cfg["campaign"]["studies"]}
    d = cfg["campaign"]["method_decision"]["date"]
    assert st["S-CEX-FRC"]["end"] < d < st["S-AEX-SCR"]["start"]


# --------------------------------------------------------------------------------------
# Harvest and UF/DF univariate studies (owner's option A, 2026-10-08)
# --------------------------------------------------------------------------------------
def _nodoe():
    u = pd.read_csv(os.path.join(DATA, "univariate_studies.csv"))
    return u[u["step"].isin(["harvest", "ufdf"])]


def test_nodoe_effects_vanish_at_set_point():
    """The new effects are zero at set-point and draw no random number, so the nominal batch is
    the one Version 1.0 described."""
    from amab_process.process import Process
    proc = Process(load_config())
    a, b = proc.nominal_batch(), proc.nominal_batch()
    ds = a.drug_substance.cqas
    assert ds == b.drug_substance.cqas
    ufdf = a.steps[-1]
    assert ufdf.out.cqas["aggregates_hmw"] == ufdf.inp.cqas["aggregates_hmw"]


def test_nodoe_design_and_findings():
    u = _nodoe()
    cfg = load_config().raw()["analytics"]["univariate_nodoe"]
    n = len(cfg["levels"]) * int(cfg["replicates"])
    assert (u.groupby(["step", "parameter"]).size() == n).all()
    # post-clarification turbidity is studied as a challenge: the level set is the level measured
    t = u[u["parameter"] == "turbidity"]
    assert np.allclose(t["clarified_turbidity_ntu"], t["value"], rtol=0.15)
    assert t["centrate_turbidity_ntu"].isna().all()
    # residual buffer at the 8 DV set-point is the 0.034 % Version 1.0 printed
    sp = u[(u["parameter"] == "diavolumes") & (u["level"] == "set-point")]
    assert abs(sp["residual_buffer_pct"].mean() - 0.034) < 0.003
    # the clarified turbidity knee lies above the depth filter load NOR, not inside it
    d = u[u["parameter"] == "depth_filter_load"].groupby("value")["clarified_turbidity_ntu"].mean()
    assert d.iloc[-1] > 2 * d.iloc[0] and d.iloc[:-1].max() < 1.3 * d.iloc[0]


def test_harvest_keeps_the_no_quality_impact_assumption():
    """A-Mab p.85: harvest has no impact on product quality. No attribute slope is significant."""
    from scipy import stats
    u = _nodoe()
    for (step, par), g in u[u["step"] == "harvest"].groupby(["step", "parameter"]):
        for col in ("hcp_out_ng_mg", "aggregate_out_pct"):
            assert stats.linregress(g["value"], g[col]).pvalue > 0.05, (par, col)


def test_nodoe_responses_are_not_attributes():
    import sys
    sys.path.insert(0, os.path.join(ROOT, "pc_package"))
    import tables as T
    for r in ("centrate_turbidity_ntu", "clarified_turbidity_ntu", "residual_buffer_pct",
              "ds_concentration_g_per_l"):
        assert T._resp_cqa(r, "harvest") is None
    assert T._resp_cqa("aggregate_out_pct", "ufdf") == "aggregates_hmw"


def test_version1_capability_reproduced():
    """The Version 1.0 capability-based limits and INV-001's capability findings come from the
    simulation at the NOR as characterized, which reproduces Version 1.0 for every attribute those
    limits use: no Version 2.0 NOR decision may move a Version 1.0 number."""
    old = _at_tag("capability").set_index("key")
    new = pd.read_csv(os.path.join(DATA, "capability_rev1.csv")).set_index("key")
    for k in ("afucosylation", "galactosylation", "high_mannose", "acidic_variants"):
        assert np.allclose(old.loc[k, ["mean", "sd"]].to_numpy(float),
                           new.loc[k, ["mean", "sd"]].to_numpy(float), rtol=1e-9), k



def test_recentred_low_ph_support():
    """PCR-006 Version 2.0: the OFAT study at the re-centred pH shows no pH effect on aggregate or
    fragments beyond method precision, and the CEX verification has the number of runs its
    simulation gives and passes its rule."""
    from scipy import stats
    o = pd.read_csv(os.path.join(DATA, "vi_ofat.csv"))
    for col in ("aggregate_out_pct", "lmw_cesds_pct"):
        a = o[(o["ph"] == 3.4) & (o["hold_min"] > 0)][col].to_numpy()
        b = o[(o["ph"] == 3.5) & (o["hold_min"] > 0)][col].to_numpy()
        assert stats.ttest_rel(a, b).pvalue > 0.05, col
    n = pd.read_csv(os.path.join(DATA, "cex_verification_n.csv"))
    v = pd.read_csv(os.path.join(DATA, "cex_verification.csv"))
    assert len(v) == int(n["n_required"].max())
    z = stats.norm.ppf(0.95)
    for cqa, col in (("aggregates_hmw", "aggregate_fold"), ("fragments_lmw", "fragment_fold")):
        r = n[n["cqa"] == cqa].iloc[0]
        lb = np.log(v[col]).mean() - z * r["sigma_ln"] / np.sqrt(len(v))
        assert lb >= np.log(r["f_required"]), cqa


# --------------------------------------------------------------------------------------
# Owner's decisions of 2026-10-09 (second session): exact fits, hold studies, the
# concentration confirmation study, and the numbering of discrepancies from the plan
# --------------------------------------------------------------------------------------
def test_exact_fit_is_never_adequate():
    """A response the full quadratic reproduces exactly has no residual, so neither the lack-of-fit
    test nor the model F-test can be computed: PCMP-001 §7.2 cannot pass it, no Box-Cox interval is
    reported, and it cannot widen a criterion (INV-002 review run 2)."""
    from amab_process import adequacy as ad
    lv = [-1.0, 0.0, 1.0]
    df = pd.DataFrame([{"coded_a": a, "coded_b": b} for a in lv for b in lv] * 2)
    df["y"] = 20.0 + 0.2 * df["coded_b"]                     # depends on one factor, no error
    th = {k: float(v) for k, v in load_config().raw()["campaign"]["thresholds"].items()}
    fit = ad.select_model(df, "y", ["a", "b"], th)
    assert fit["exact"] and not fit["adequate"] and fit["boxcox"] is None
    v = pd.read_csv(os.path.join(DATA, "iac_verification.csv"))
    r = v[(v["step_key"] == "viral_inactivation") & (v["cqa"] == "acidic_variants")].iloc[0]
    assert not bool(r["model_adequate"]) and not bool(r["widening_supported"])


def test_hold_studies_are_version2_discrepancies_with_nrcesds_throughout():
    """No Version 1.0 document planned or reported a hold study, so they were made during the
    Version 2.0 re-analysis, after AMD-001: nrCE-SDS on every sample and no SEC fragment result.
    Each is a discrepancy from its plan."""
    cfg = load_config().raw()
    st = {s["id"]: s for s in cfg["campaign"]["studies"]}
    rev1 = cfg["campaign"]["revisions"][0]["effective"]
    amd = cfg["campaign"]["method_decision"]["date"]
    pd_studies = {x for ds in cfg["campaign"]["plan_discrepancies"].values() for d in ds
                  for x in d.get("studies", [])}
    for pool, h in cfg["analytics"]["holds"].items():
        assert st[h["study"]]["start"] > max(rev1, amd) and h["study"] in pd_studies, pool
        d = pd.read_csv(os.path.join(DATA, f"hold_{pool}.csv"))
        assert d["lmw_cesds_pct"].notna().all() and d["lmw_sec_pct"].isna().all(), pool


def test_concentration_confirmation_study_closes_the_deviation():
    """DEV-006-03: PCP-006 Version 1.0 required XMuLV clearance on every run of the A-Mab
    concentration study and S-VI-UNI measured none. S-VI-UNI2 (PD-006-06) measures it at both ends
    of the range in duplicate, and the inactivation does not depend on the concentration."""
    cfg = load_config()
    devs = {e["id"]: e for e in cfg.raw()["deviations"]["events"]["PCR-006"]}
    assert "DEV-006-03" in devs
    u = pd.read_csv(os.path.join(DATA, "univariate_studies.csv"))
    old = u[u["study"] == "S-VI-UNI"]
    assert old.get("xmulv_lrf", pd.Series(dtype=float)).isna().all()      # the deviation itself
    new = u[u["study"] == cfg.raw()["analytics"]["vi_concentration"]["study"]]
    p = cfg.unit_op("viral_inactivation").param("protein_conc")
    assert sorted(new["value"].unique()) == [float(p.prange[0]), float(p.prange[1])]
    assert new["xmulv_lrf"].notna().all() and (new.groupby("level").size() == 2).all()


def test_computed_discrepancies_keep_their_numbers():
    """A configured discrepancy given an explicit higher number does not renumber the computed ones
    a report already cites: model selection stays PD-005-04 beside the hold study PD-005-05."""
    import sys
    sys.path.insert(0, os.path.join(ROOT, "pc_package"))
    from _pcpkg import PLAN_DISCREPANCIES
    for doc, ds in PLAN_DISCREPANCIES.items():
        ids = [d["id"] for d in ds]
        assert ids == sorted(ids) and len(set(ids)) == len(ids), doc
    sel = {d["id"] for ds in PLAN_DISCREPANCIES.values() for d in ds
           if d["subject"].startswith("Model selection")}
    assert {"PD-005-04", "PD-006-04"} <= sel
