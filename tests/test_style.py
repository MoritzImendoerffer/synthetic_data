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


def test_limits_unchanged():
    assert len(cs.LIMITS) == 12
    assert not any(k.startswith("_pct_") for k in cs.LIMITS)


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
