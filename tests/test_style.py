"""The register gate's sentence splitter and its advisory clause-packing counts."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "authoring"))
import check_style as cs

FIXTURE = (
    "The tests rest on four replicates, so a result bounds the evidence, and the case is open. "
    "Therefore, the model is provisional. "
    "The range was set wider than the control range, so that the study measures robustness. "
    "The step meets its criterion."
)


def test_sentences_splits_four():
    assert len(cs.sentences(FIXTURE)) == 4


def test_packing_counts():
    m, *_ = cs.measure(FIXTURE)
    assert m["_n_so_mid"] == 2          # sentences 1 and 3
    assert m["_n_initial_conn"] == 1    # "Therefore, …"
    assert m["_n_coord2"] == 1          # sentence 1: ", so" and ", and"
    assert m["_n_sent"] == 4


def test_limits_split():
    """Five gated tics, seven advisory signals, twelve rows in the union — and the union keeps
    the row order the committed baseline tables were printed in (2026-08-19, TASK-006 of
    2026-08-18_03_author-facing-apparatus)."""
    assert len(cs.GATED) == 5
    assert len(cs.ADVISORY) == 7
    assert len(cs.LIMITS) == 12
    assert set(cs.LIMITS) == set(cs.GATED) | set(cs.ADVISORY)
    assert not (set(cs.GATED) & set(cs.ADVISORY))
    assert list(cs.LIMITS) == ["mean_len", "median_len", "pct_over_40", "pct_over_55",
                               "pct_under_15", "em_dash", "semicolon", "colon", "paren",
                               "bold", "multi_hyphen", "rather_than"]
    assert not any(k.startswith("_pct_") for k in cs.LIMITS)


def test_evaluate_gates_only_the_tics():
    """A text that breaks every advisory band and no gated one passes evaluate(); the
    self-test's union view sees the same text fail."""
    m = {"_n_sent": cs.MIN_SENTENCES, "mean_len": 12.0, "median_len": 10.0, "pct_over_40": 0.0,
         "pct_over_55": 0.0, "pct_under_15": 80.0, "paren": 0.0, "rather_than": 5.0,
         "em_dash": 0.0, "semicolon": 0.0, "colon": 0.0, "bold": 0.0, "multi_hyphen": 0.0}
    assert cs.evaluate(m) == []
    assert {k for k, *_ in cs.evaluate(m, cs.LIMITS)} == {
        "mean_len", "median_len", "pct_over_40", "pct_under_15", "paren", "rather_than"}


FIXTURE_AND = (
    "The screening study covered five parameters, and the remaining four were assessed one at a time. "
    "The design space rests on the response surface model, not on the screening fit. "
    "Galactosylation, high mannose, and afucosylation were measured on one separation. "
    "The step meets its criterion in every run."
)


def test_and_clause_and_not_tail():
    m, *_ = cs.measure(FIXTURE_AND)
    assert m["_n_sent"] == 4
    assert m["_n_and_clause"] == 1     # sentence 1 only; the Oxford comma in sentence 3 must NOT count
    assert m["_n_not_tail"] == 1       # sentence 2
