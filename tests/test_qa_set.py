"""The graded question-answer set (pc_package/build_qa.py) builds, grounds and meets its floors.

Builds the set in memory from the rendered Version 2.0 documents and checks, independently of the
builder's own filtering, that every evidence quote (and every key-point quote) is a verbatim
substring of its rendered document under check_grounding's extraction, that item ids are unique,
and that each level has at least its minimum count. A stale curated item does not fail the test by
itself; it fails only if its level drops below the floor.
"""
import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = os.path.join(ROOT, "pc_package")
sys.path.insert(0, PKG)


@pytest.fixture(scope="module")
def built():
    try:
        import build_qa as Q
    except Exception as exc:  # pragma: no cover - environment without the model deps
        pytest.skip(f"build_qa does not import: {exc}")
    try:
        corpus = Q.Corpus()
    except FileNotFoundError as exc:
        pytest.skip(f"rendered corpus not available: {exc}")
    items, report = Q.build(corpus)
    return Q, corpus, items, report


def _evidence(it):
    out = list(it.get("evidence") or [])
    for kp in it.get("key_points") or []:
        out += kp.get("evidence") or []
    return out


def test_every_quote_grounds(built):
    Q, corpus, items, _ = built
    import check_grounding as G
    bad = []
    for it in items:
        for e in _evidence(it):
            for field in ("quote", "table_header"):
                q = e.get(field)
                if q and G.normalize(q) not in corpus.text.get(e["doc_id"], ""):
                    bad.append((it["id"], e["doc_id"], q[:70]))
    assert not bad, f"{len(bad)} ungrounded quote(s): {bad[:5]}"


def test_evidence_only_from_version_2_documents(built):
    Q, corpus, items, _ = built
    scope = set(corpus.docs)
    for it in items:
        assert set(it["docs"]) <= scope, it["id"]
        assert it["docs"] == sorted({e["doc_id"] for e in _evidence(it)}), it["id"]


def test_ids_unique(built):
    _, _, items, _ = built
    ids = [it["id"] for it in items]
    assert len(ids) == len(set(ids))


def test_level_minimums(built):
    Q, _, items, report = built
    for lv, n in Q.MIN_COUNTS.items():
        got = sum(1 for it in items if it["level"] == lv)
        assert got >= n, f"{lv}: {got} items, minimum {n}; stale: {report['stale']}"


def test_item_shape(built):
    _, _, items, _ = built
    for it in items:
        assert it["question"] and it["answer"], it["id"]
        if it["level"] in ("L1", "L2", "L3", "L4"):
            assert _evidence(it), it["id"]
        if it["level"] in ("L2", "L3", "L4"):
            assert it.get("reasoning"), it["id"]
        if it["level"] == "SUM":
            assert 5 <= len(it["key_points"]) <= 12, it["id"]
        if it["level"] == "NONE":
            assert it["expected"] == "not in the documents" and it["absent_terms"], it["id"]
        json.dumps(it, ensure_ascii=False)
