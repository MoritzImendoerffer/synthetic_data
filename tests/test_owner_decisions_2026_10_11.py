"""The owner's decisions of 2026-10-11 on the production bioreactor, as the engine and the config carry them."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pc_package"))
sys.path.insert(0, os.path.join(HERE, ".."))

import doe_report as D  # noqa: E402
import _pcpkg as P  # noqa: E402


def test_bioreactor_classes_follow_the_rule():
    """Osmolality CPP (narrow PAR), dissolved oxygen GPP (no effect shown), basal medium KPP (expected growth
    effect): reclassified by the rule of PCMP-001 §7.7."""
    uo = P.CFG.unit_op("bioreactor")
    assert uo.param("osmolality").classification == "CPP"
    assert uo.param("do").classification == "GPP"
    assert uo.param("medium_conc").classification == "KPP"


def test_acidic_alarms_sit_inside_the_nor_on_the_side_that_lowers_acidic_variants():
    m = D.acidic_mitigation()
    for a in m["alarms"]:
        lo, hi = a["nor"]
        assert lo < a["alarm"] < hi, a
        assert (a["alarm"] > a["setpoint"]) == (a["side"] == "high"), a
    # the action limit at harvest guards the lower criterion by the precision of icIEF
    assert m["action_limit"] > m["lower_criterion"]
    assert abs(m["action_limit"] - (m["lower_criterion"] + m["guard"] * m["sd"])) < 1e-9


def test_review_findings_are_no_events():
    """A process characterization study raises no deviation: the events are Version 1.0's only."""
    d = P.csv("deviations.csv")
    assert not d["detected_during"].str.contains("Version 2.0").any()
    assert len(d) == 17
