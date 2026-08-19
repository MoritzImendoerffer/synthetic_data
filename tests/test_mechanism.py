"""authoring/mechanism/<key>.yaml — one per unit operation, no number in the prose.

Added 2026-08-19 (TASK-009, work unit 2026-08-18_03_author-facing-apparatus). The files supply
the physical chemistry the reports explain (brief §2b). They are written from domain knowledge
and read once by the owner, and the one thing a test can hold them to is the golden rule: no
number lives in them, so a reseed cannot stale them and nothing in them can contradict a CSV.
"""
import glob
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pc_package"))
import _pcpkg as P  # noqa: E402

MECH = os.path.join(ROOT, "authoring", "mechanism")
UO_KEYS = ["bioreactor", "harvest", "protein_a", "viral_inactivation", "cex", "aex",
           "virus_filtration", "ufdf"]
DIGIT = re.compile(r"[0-9]")


def _load(key):
    with open(os.path.join(MECH, f"{key}.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_one_file_per_unit_operation():
    have = sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(MECH, "*.yaml")))
    assert have == sorted(UO_KEYS), have


def test_shape_and_provenance():
    for key in UO_KEYS:
        m = _load(key)
        assert m["key"] == key
        for field in ("step_title", "source", "reviewed_by_owner", "overview", "cqas",
                      "parameters"):
            assert field in m, (key, field)
        assert "domain knowledge" in m["source"]


def test_no_number_in_prose():
    """Every prose value is digit-free. `source` is provenance and may carry a date."""
    for key in UO_KEYS:
        m = _load(key)
        prose = [m["overview"]] + list(m["cqas"].values()) + list(m["parameters"].values())
        for text in prose:
            assert not DIGIT.search(text), (key, text[:80])


def test_every_config_parameter_has_a_mechanism():
    for key in UO_KEYS:
        want = {q.key for q in P.CFG.unit_op(key).parameters}
        have = set(_load(key)["parameters"])
        assert want <= have, (key, want - have)


def test_every_cqa_the_step_sets_has_a_mechanism():
    reg = P.cqa_reg
    for key in UO_KEYS:
        want = set(reg.loc[reg["set_by"] == key, "key"])
        have = set(_load(key)["cqas"])
        assert want <= have, (key, want - have)
