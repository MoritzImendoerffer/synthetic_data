"""The rendered table row and the annex quote must agree on the cell boundary.

A row quote is built by ``build_ground_truth._join_cells`` and checked against the text
``check_grounding.docx_text`` extracts from the rendered .docx. The two sides encode the
same thing — where one cell ends and the next begins — in two different places, so they
can drift apart silently: the quote would simply stop grounding, 20 documents at a time.
These tests pin the encoding from both ends.

The cells used to be joined by a single space, which grounded fine and told a consumer
nothing: "3 Production Bioreactor Forms the glycan ... CQAs" gives no way to separate the
step number from the step name from the role.
"""

import os
import sys
import zipfile

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pc_package"))

import check_grounding as G  # stdlib only, so it always imports


@pytest.fixture
def docx(tmp_path):
    """Write a minimal .docx holding one table (only word/document.xml is ever read)."""
    def build(*rows):
        cells = "".join(
            "<w:tr>" + "".join(f"<w:tc><w:p><w:r><w:t>{c}</w:t></w:r></w:p></w:tc>" for c in row)
            + "</w:tr>" for row in rows)
        path = tmp_path / f"t{len(list(tmp_path.iterdir()))}.docx"
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("word/document.xml", f"<w:document><w:body><w:tbl>{cells}</w:tbl>"
                                            "</w:body></w:document>")
        return str(path)
    return build


def _join_cells():
    try:
        import build_ground_truth as B
    except Exception as exc:                     # needs outputs/data via _pcpkg
        pytest.skip(f"build_ground_truth not importable ({exc}); run make data")
    return B._join_cells


def test_cell_boundary_is_readable_in_the_extracted_text(docx):
    """Adjacent cells are separated, not run together behind one space."""
    text = G.docx_text(docx(["3", "Production Bioreactor", "Forms the glycan CQAs"]))
    assert "3 | Production Bioreactor | Forms the glycan CQAs" in text


def test_row_quote_grounds_in_the_rendered_row(docx):
    """What the annex writes as a quote is what the checker reads out of the document."""
    row = ["Culture pH", "pH", "6.85", "6.75–6.95"]
    quote = _join_cells()(row)
    assert quote in G.docx_text(docx(row)), f"{quote!r} does not ground"


def test_an_empty_cell_keeps_its_place_in_the_row(docx):
    """An empty cell renders as a bare separator on both sides, not as a dropped column.

    Dropping it would shift every following value one column left in the quote, which is
    exactly the kind of silent mis-attribution the separator exists to prevent."""
    row = ["Hold time", "", "60 min"]
    quote = _join_cells()(row)
    assert quote == "Hold time | | 60 min"
    assert quote in G.docx_text(docx(row))


def test_a_row_quote_does_not_leak_into_the_next_row(docx):
    """The separator after the last cell of a row does not make two rows one quote."""
    text = G.docx_text(docx(["Load pH", "7.4"], ["Load conductivity", "3.2"]))
    assert "Load pH | 7.4" in text
    assert "7.4 Load conductivity" not in text


# --------------------------------------------------------------------------- #
# The anchor rules: what a quote has to attest, not just that it exists.       #
# --------------------------------------------------------------------------- #
def _annex(doc_id):
    path = os.path.join(ROOT, "pc_package", "ground_truth", f"{doc_id}.json")
    if not os.path.exists(path):
        pytest.skip("annexes not built; run pc_package/build_ground_truth.py")
    import json
    return json.load(open(path))


def _quote_counts(annex):
    from collections import Counter
    c = Counter()

    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get("quote"), str):
                c[o["quote"]] += 1
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(annex)
    return c


ALL_DOCS = ["PCP-003", "PCR-003", "PCP-004", "PCR-004", "PCP-005", "PCR-005",
            "PCP-006", "PCR-006", "PCP-007", "PCR-007", "PCP-008", "PCR-008",
            "PCP-009", "PCR-009", "PCP-010", "PCR-010", "PTP-001", "RA-001",
            "PCMP-001", "PCMR-001"]


@pytest.mark.parametrize("doc_id", ALL_DOCS)
def test_no_span_is_reused_past_its_ceiling(doc_id):
    """The two-tier reuse rule, per annex.

    Fourteen annexes once anchored every parameter of a step on the caption of the table
    those parameters sit in — six records behind one span that named none of them. That
    reported clean while the reuse ceiling was a single number set at 8.
    """
    counts = _quote_counts(_annex(doc_id))
    bad = [(q, n) for q, n in counts.items()
           if n > (G.MAX_ROW_REUSE if G.CELL_SEP in q else G.MAX_PROSE_REUSE)]
    assert not bad, "spans reused past the ceiling for their shape: " + repr(bad[:3])


@pytest.mark.parametrize("doc_id", ALL_DOCS)
def test_parameter_and_attribute_records_anchor_on_a_row(doc_id):
    """Every parameter and attribute record cites the row that names it, not a caption."""
    annex = _annex(doc_id)
    loose = []
    for sec in annex.get("entities", []):
        for kind, name_field in (("parameters", "parameter_name"),
                                 ("quality_attributes", "attribute_name")):
            for e in sec.get(kind, []):
                quotes = [r.get("quote", "") for r in e.get("source_references", [])]
                if not any(G.CELL_SEP in q for q in quotes):
                    loose.append((e.get(name_field), quotes[:1]))
    assert not loose, f"{doc_id}: records not anchored on a rendered row: {loose[:3]}"


@pytest.mark.parametrize("doc_id", ALL_DOCS)
def test_the_column_header_survives_serialization(doc_id):
    """Wherever an entity record anchors on a row, its header reached the JSON.

    This is the canary for a silent serialization bug, not a style rule: ``table_header``
    lives on the ``schema_ext`` subclass while the vendored models annotate the contract
    class, so ``model_dump`` drops it from every such reference unless the annex is dumped
    with ``serialize_as_any=True`` — no warning, no validation error, just a thinner annex.
    """
    annex = _annex(doc_id)
    missing = []
    for sec in annex.get("entities", []):
        for kind in ("parameters", "quality_attributes"):
            for e in sec.get(kind, []):
                for r in e.get("source_references", []):
                    if G.CELL_SEP in (r.get("quote") or "") and not r.get("table_header"):
                        missing.append((e.get("parameter_name") or e.get("attribute_name"),
                                        r["quote"][:40]))
    assert not missing, f"{doc_id}: row anchors that lost their header: {missing[:3]}"


def test_the_header_names_the_columns_of_the_row_it_carries():
    """A header has to line up with its row, or it mislabels every cell.

    Same cell count, and the header is the one that reads as column names.
    """
    annex = _annex("PCR-003")
    checked = 0
    for sec in annex.get("entities", []):
        for e in sec.get("parameters", []):
            for r in e.get("source_references", []):
                h, q = r.get("table_header"), r.get("quote") or ""
                if not h or G.CELL_SEP not in q:
                    continue
                assert h.count(G.CELL_SEP) == q.count(G.CELL_SEP), (
                    f"{e.get('parameter_name')}: header has {h.count(G.CELL_SEP) + 1} columns, "
                    f"row has {q.count(G.CELL_SEP) + 1}")
                assert e.get("parameter_name") in q and e.get("parameter_name") not in h
                checked += 1
    assert checked, "no row-anchored parameter found to check"
