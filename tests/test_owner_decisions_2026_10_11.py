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


def test_combined_alert_covers_every_failing_nor_combination():
    """Option 1 (owner, 2026-10-11): conditional limits derived from the model; the alert fires when every alert
    parameter is beyond its limit, and it covers every combination inside the NOR box that fails the criterion."""
    m = D.acidic_mitigation()
    assert m["covers_nor"]
    for a in m["alert"]:
        if a["limit"] is not None:
            assert a["side"] in ("high", "low")
    # the action limit at harvest guards the lower criterion by the precision of icIEF
    assert m["action_limit"] > m["lower_criterion"]
    assert abs(m["action_limit"] - (m["lower_criterion"] + m["guard"] * m["sd"])) < 1e-9


def test_review_findings_are_no_events():
    """A process characterization study raises no deviation: the events are Version 1.0's only."""
    d = P.csv("deviations.csv")
    assert not d["detected_during"].str.contains("Version 2.0").any()
    assert len(d) == 17


def test_nor_flags_match_the_par_margins():
    """A NOR that does not hold is flagged for discussion with manufacturing, not narrowed (owner,
    2026-10-11). nor_flags lists exactly the factor and output pairs whose NOR in force reaches outside
    the NOR-propagated PAR (checked here on Protein A, the step whose load NOR was reversed)."""
    f = D.nor_flags("protein_a")
    assert list(f.columns)[:6] == ["step", "step_key", "factor", "factor_name", "unit", "response"]
    m = D.par_margins("protein_a")
    expect = {(r["factor"], r["response"]) for _, r in m.iterrows() if not r["contains_nor"]}
    got = {(r["factor"], r["response"]) for _, r in f.iterrows() if r["response"] in set(m["response"])}
    assert got == expect
