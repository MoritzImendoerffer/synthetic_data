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

    keys = [k for k in CFG.train_order if st.DOE_FACTORS.get(k)]
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
            if not any(design(k, kind) == (n_runs, n_cp)
                       for k in keys for kind in ("screening", "rsm")
                       if design(k, kind) is not None):
                problems.append(f"{doc} {sd.get('study_id', '?')}: "
                                f"n_runs={n_runs}, n_center_points={n_cp} matches no seeded design")
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
