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
