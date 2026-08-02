"""Consistency tests for config/parameters.yaml against the study definitions.

The config is the single source of truth (CLAUDE.md golden rule 1), but nothing previously
checked that its *descriptive* metadata agrees with the studies the model actually
generates. It did not: three bioreactor parameters were labelled ``study: "multivariate"``
while appearing in no multivariate design, so the rendered parameter tables claimed a study
that produced no data. These tests make that class of drift a build failure.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from amab_process import load_config
from amab_process import studies as st

CFG = load_config()

STUDY_VALUES = {"multivariate", "univariate"}


def _params(key):
    return CFG.unit_op(key).parameters


def test_study_values_are_known():
    """Only the two defined study types are used anywhere in the config."""
    bad = [(k, p.key, p.study) for k in CFG.train_order for p in _params(k)
           if p.study not in STUDY_VALUES]
    assert not bad, f"unknown study type(s): {bad}"


def test_multivariate_matches_doe_factors():
    """``study: "multivariate"`` means exactly "a factor of this step's seeded DoE".

    A parameter claiming a multivariate study while absent from the design has no data
    behind the claim, and a DoE factor labelled univariate understates what was done.
    Either direction is a documentation defect, because the parameter tables in every
    plan and report render this column verbatim.
    """
    problems = []
    for key in CFG.train_order:
        factors = set(st.DOE_FACTORS.get(key, []))
        for p in _params(key):
            in_doe = p.key in factors
            claims_mv = p.study == "multivariate"
            if in_doe and not claims_mv:
                problems.append(f"{key}.{p.key}: is a DoE factor but study={p.study!r}")
            if claims_mv and not in_doe:
                problems.append(
                    f"{key}.{p.key}: study='multivariate' but not a DoE factor "
                    f"(factors: {sorted(factors) or 'none — this step has no DoE'})")
    assert not problems, "study type disagrees with the seeded designs:\n  " + \
                         "\n  ".join(problems)


def test_non_doe_steps_have_no_multivariate_parameters():
    """Steps with no seeded DoE (harvest, ufdf) must not claim a multivariate study."""
    for key in CFG.train_order:
        if st.DOE_FACTORS.get(key):
            continue
        mv = [p.key for p in _params(key) if p.study == "multivariate"]
        assert not mv, f"{key} has no DoE but claims multivariate study for {mv}"


@pytest.mark.parametrize("key", ["bioreactor", "protein_a", "viral_inactivation",
                                 "cex", "aex", "virus_filtration"])
def test_every_doe_factor_is_a_config_parameter(key):
    """Every factor in a seeded design resolves to a real config parameter."""
    keys = {p.key for p in _params(key)}
    missing = [f for f in st.DOE_FACTORS.get(key, []) if f not in keys]
    assert not missing, f"{key}: DoE factor(s) with no config parameter: {missing}"


def test_generated_parameter_table_matches_config():
    """The generated CSV must agree with the config it was derived from.

    This is the test that was missing. ``study`` was corrected in the config, and
    ``test_multivariate_matches_doe_factors`` passed immediately — because it reads
    ``CFG`` directly. But ``plan_params()`` / ``report_params()`` render
    ``outputs/data/parameter_classification.csv``, which had not been regenerated, so
    every rendered parameter table still showed the old value while the config, the
    prose and the test all said otherwise. A config invariant that never looks at the
    generated artifact cannot catch that class of drift.
    """
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "outputs", "data", "parameter_classification.csv")
    if not os.path.exists(path):
        pytest.skip("outputs/ not generated; run scripts/generate_data.py")
    import csv as _csv
    with open(path) as fh:
        rows = list(_csv.DictReader(fh))

    want = {}
    for key in CFG.train_order:
        for p in _params(key):
            want[(CFG.unit_op(key).name, p.name)] = (p.study, p.classification)

    problems = []
    for r in rows:
        k = (r["unit_operation"], r["parameter"])
        if k not in want:
            problems.append(f"{k}: in the CSV but not in the config")
            continue
        study, classification = want[k]
        if r["study"] != study:
            problems.append(f"{k[1]} ({k[0]}): CSV study={r['study']!r} "
                            f"but config says {study!r}")
        if r["classification"] != classification:
            problems.append(f"{k[1]} ({k[0]}): CSV classification={r['classification']!r} "
                            f"but config says {classification!r}")
    assert not problems, (
        "outputs/data/parameter_classification.csv is stale relative to "
        "config/parameters.yaml — re-run scripts/generate_data.py and commit ONLY the "
        "intended CSV change:\n  " + "\n  ".join(problems))


def test_annex_study_designs_match_the_seeded_designs():
    """Annex StudyDesign run and centre-point counts must come from the designs.

    These live in schema fields rather than in quote strings, so ``check_grounding`` never
    looks at them: an annex can assert a run count the design contradicts and still report
    every quote grounded. The counts were literals until they were derived; this test is
    what stops them drifting back.
    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gt = os.path.join(root, "pc_package", "ground_truth")
    data = os.path.join(root, "outputs", "data")
    if not os.path.isdir(gt):
        pytest.skip("annexes not built; run pc_package/build_ground_truth.py")

    import csv as _csv
    import glob
    import json

    def design(key, kind):
        path = os.path.join(data, f"doe_{key}_{kind}.csv")
        if not os.path.exists(path):
            return None
        with open(path) as fh:
            rows = list(_csv.DictReader(fh))
        return len(rows), sum(1 for r in rows if r["run_type"] == "center")

    def univariate_counts(key):
        """Run counts a UNIVARIATE schedule can legitimately have at a non-DoE step.

        Harvest (Step 4) and UF/DF (Step 10) run no designed experiment, so their studies
        match no ``doe_*.csv`` and the seeded-design check above cannot see them. Their
        schedules are still derived from the parameter register, in one of two shapes, and
        each plan states which it uses:

          * edges plus the set-point as a reference, per parameter — PCP-010, "9 runs in
            total: 6 runs at an edge and 3 at the set-point";
          * every distinct level among the two characterization edges, the two normal-
            operating edges and the set-point — PCP-004, whose turbidity series is one run
            shorter because its NOR and characterization range share a lower edge.

        Both are computed here from ``CFG`` alone, so a count that is neither remains a
        failure. This is deliberately not a free pass: it is the same "derived, never typed"
        rule the DoE branch enforces, applied to the schedule these steps actually run.
        """
        uo = CFG.unit_op(key)
        ps = [p for p in uo.parameters if p.study == "univariate"]
        if not ps:
            return set()
        edges_plus_reference = 3 * len(ps)
        distinct_levels = sum(
            len({p.prange[0], p.nor[0], p.setpoint, p.nor[1], p.prange[1]}) for p in ps)
        return {edges_plus_reference, distinct_levels}

    keys = [k for k in CFG.train_order if st.DOE_FACTORS.get(k)]
    nondoe_runs = set()
    for k in CFG.train_order:
        if not st.DOE_FACTORS.get(k):
            nondoe_runs |= univariate_counts(k)

    problems = []
    for path in sorted(glob.glob(os.path.join(gt, "*.json"))):
        annex = json.load(open(path))
        doc = annex["document_id"]
        for sd in annex.get("studies") or []:
            n_runs, n_cp = sd.get("n_runs"), sd.get("n_center_points")
            if n_runs is None and n_cp is None:
                continue
            # match against any seeded design of any DoE step; the annex names its own
            # unit operation, so a mismatch everywhere means the numbers are invented.
            if any(design(k, kind) == (n_runs, n_cp)
                   for k in keys for kind in ("screening", "rsm")
                   if design(k, kind) is not None):
                continue
            # A univariate study has no centre points, so n_cp must be absent, and its run
            # count must be one the parameter register produces.
            if n_cp is None and n_runs in nondoe_runs:
                continue
            problems.append(f"{doc} {sd.get('study_id', '?')}: "
                            f"n_runs={n_runs}, n_center_points={n_cp} matches no seeded "
                            f"design and no univariate schedule the register supports")
    assert not problems, ("annex StudyDesign counts disagree with the seeded designs:\n  "
                          + "\n  ".join(problems))


def test_ranges_contain_nor_and_setpoint():
    """The NOR sits inside the characterization range, and the set-point inside the NOR."""
    problems = []
    for key in CFG.train_order:
        for p in _params(key):
            rlo, rhi = p.prange
            nlo, nhi = p.nor
            if not (rlo <= nlo <= nhi <= rhi):
                problems.append(f"{key}.{p.key}: NOR {p.nor} not inside range {p.prange}")
            if not (nlo <= p.setpoint <= nhi):
                problems.append(f"{key}.{p.key}: set-point {p.setpoint} outside NOR {p.nor}")
    assert not problems, "range/NOR/set-point nesting broken:\n  " + "\n  ".join(problems)
