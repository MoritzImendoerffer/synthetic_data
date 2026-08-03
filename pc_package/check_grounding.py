#!/usr/bin/env python3
"""Grounding check for the A-Mab ground-truth annexes.

For every ``ground_truth/<ID>.json`` this verifies that each
``SourceReference.quote`` appears **verbatim** in the matching rendered document
(the ``.docx`` named by the annex ``inventory.file_name``), under whitespace-
collapsed comparison — a quote that spans a line wrap in the rendered text still
matches. This is the machine-checkable form of golden rule 3 ("everything is
grounded"): prose may only state what the data supports, and every annex quote
must exist in the document it annotates.

One thing survives the collapse: a **table cell boundary reads as " | "**. Stripping
the docx XML to bare text used to run adjacent cells together behind a single space, so
the row quote ``"3 Production Bioreactor Forms the glycan ... CQAs"`` gave a consumer no
way to tell the step number from the step name, or either from the role. The cell
boundary is real structure in the document, and a quote that spans a row now carries it:
``"3 | Production Bioreactor | Forms the glycan ... CQAs"``. Prose quotes are unaffected —
they live inside one paragraph and never cross a cell boundary.

Run:   python check_grounding.py
Exit:  0 if every quote grounds, 1 otherwise (so it can gate ``make corpus``).
"""
from __future__ import annotations

import glob
import html
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
GT = os.path.join(HERE, "ground_truth")


#: What a table cell boundary reads as in the extracted text. ``build_ground_truth._md_rows``
#: joins a rendered row with the same string, so a full-row quote stays a verbatim substring.
CELL_SEP = " | "

#: Sub/superscript digits, folded to the plain digit on BOTH sides of the comparison.
#:
#: Not cosmetic: the rendered corpus is inconsistent about them. "XMuLV LRF (log₁₀)" comes
#: from one label in ``doe_report``, and PCR-008's PAR table keeps the subscript characters
#: while PCR-006's turns them into a subscript run carrying "10" — the same string, two
#: renderings, because the documents were rendered at different times. A quote cannot be
#: verbatim against both, and which one a given .docx has is not a fact about the content.
#: This is the same kind of normalisation as the whitespace collapse: fold a rendering
#: artifact, then demand an exact match on everything that is left.
SCRIPT_DIGITS = str.maketrans("₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹", "01234567890123456789")


def normalize(s: str) -> str:
    """Collapse whitespace and fold script digits — the comparison form for both sides."""
    return re.sub(r"\s+", " ", s).translate(SCRIPT_DIGITS).strip()


def docx_text(path: str) -> str:
    """Whitespace-collapsed plain text of a .docx (word/document.xml).

    ``</w:tc>`` (end of a table cell) becomes ``CELL_SEP`` before the tags are stripped, so
    the cells of a row stay separable in the extracted text. Every other tag becomes a
    space, and runs of whitespace collapse to one — that is what lets a quote span a line
    wrap. Note the separator also lands after the last cell of a row, so a table reads as
    one continuous ``a | b | c | d | e | f`` stream; a quote built from a whole row matches
    inside it without needing a row marker.
    """
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    xml = xml.replace("</w:tc>", CELL_SEP)
    xml = re.sub(r"<[^>]+>", " ", xml)
    return normalize(html.unescape(xml))


#: Fields that must exist verbatim in the document. ``table_header`` is the rendered header
#: row of the table a quote is anchored in (``schema_ext.SourceReference``) — a real span,
#: and one that pydantic will silently drop if the annex is dumped without
#: ``serialize_as_any``, so it needs a gate of its own.
GROUNDED_FIELDS = ("quote", "table_header")


def _quotes(obj, fields=("quote",)):
    """Yield every string in ``fields`` anywhere in the annex JSON.

    Defaults to ``quote`` alone: the reuse count in ``specificity_report`` is about spans
    offered as *evidence*, and a header is shared by every row of its table by design.
    """
    if isinstance(obj, dict):
        for f in fields:
            q = obj.get(f)
            if isinstance(q, str):
                yield q
        for v in obj.values():
            yield from _quotes(v, fields)
    elif isinstance(obj, list):
        for v in obj:
            yield from _quotes(v, fields)


# A quote that grounds is not automatically a quote that attests anything. Three shapes
# ground trivially while pointing at prose that contains neither end of the relation they
# claim: a span short enough to be ubiquitous ("acceptance criteria"), one sentence reused
# as the anchor for many records (RA-001 once used a single placeholder for 41 separate
# assertions), and a span that occurs several times in the document so the reference is
# ambiguous. The corpus convention is to anchor a per-record assertion on the RENDERED
# TABLE ROW carrying the relation, so the span contains both ends.
#
# The reuse cap is therefore two-tier, by what the span IS rather than by how long it is:
#
#   prose  — a sentence reused past MAX_PROSE_REUSE is the caption failure. Fourteen annexes
#            once anchored every parameter of a step on the caption of the table those
#            parameters sit in; six records, one span, and the reference said "somewhere in
#            that table". Three is the ceiling because a sentence that genuinely states four
#            relations is rare, and every one in this corpus turned out to have a shorter
#            slice, or a per-record sentence elsewhere, that names its own record.
#   a row  — a rendered table row carries both ends of its relation by construction, so
#            reuse means the row states several relations at once, which it can. RA-001's
#            ranking rows name five attributes each and rightly anchor five assertions.
#            Kept at the old ceiling; past that, even a row is doing too much.
MAX_PROSE_REUSE = 3       # a sentence anchoring more records than this attests little
MAX_ROW_REUSE = 8         # a rendered row may carry several relations, but not many
MAX_DOC_OCCURRENCES = 3   # a span this common in the document is an ambiguous reference


def specificity_report(annex, text) -> list[str]:
    """Advisory warnings about quotes that ground but attest little.

    Deliberately NOT a word-count rule. The corpus convention is to anchor a per-record
    assertion on the rendered table row carrying the relation, and those rows are short —
    "Culture pH | pH | 6.85 | 6.75–6.95" names both ends of what it asserts, which makes it
    a better anchor than a twelve-word sentence that merely discusses the topic. What
    actually signals a weak anchor is *non-distinctiveness*: the same span standing in for
    many different records, or appearing so often in the document that the reference is
    ambiguous. The reuse ceiling depends on the shape of the span (see the constants).
    """
    from collections import Counter
    counts = Counter(normalize(q) for q in _quotes(annex))
    out = []
    for norm, n in counts.most_common():
        is_row = CELL_SEP in norm
        cap = MAX_ROW_REUSE if is_row else MAX_PROSE_REUSE
        if n > cap:
            shape = "row" if is_row else "prose"
            out.append(f"one {shape} span anchors {n} records (max {cap}): {norm[:70]!r}")
            continue
        occ = text.count(norm)
        if occ > MAX_DOC_OCCURRENCES:
            out.append(f"occurs {occ}x in the document (ambiguous): {norm[:70]!r}")
    return out


def main() -> int:
    annexes = sorted(glob.glob(os.path.join(GT, "*.json")))
    if not annexes:
        print("no annexes found in ground_truth/ — run build_ground_truth.py first")
        return 1
    total_q = 0
    total_miss = 0
    total_weak = 0
    # The corpus is at zero weak anchors. Set GROUNDING_STRICT_ANCHORS=1 to keep it there;
    # the check stays advisory by default so a work-in-progress annex is not blocked.
    strict = bool(os.environ.get("GROUNDING_STRICT_ANCHORS"))
    for path in annexes:
        annex = json.load(open(path))
        doc_id = annex["document_id"]
        fname = annex.get("inventory", {}).get("file_name")
        docx = os.path.join(HERE, fname) if fname else None
        if not docx or not os.path.exists(docx):
            print(f"MISS {doc_id}: rendered document '{fname}' not found (render the corpus first)")
            total_miss += 1
            continue
        text = docx_text(docx)
        quotes = list(_quotes(annex, GROUNDED_FIELDS))
        miss = [q for q in quotes if normalize(q) not in text]
        total_q += len(quotes)
        total_miss += len(miss)
        weak = specificity_report(annex, text)
        total_weak += len(weak)
        status = "OK  " if not miss else "FAIL"
        note = f", {len(weak)} weak anchor(s)" if weak else ""
        print(f"{status} {doc_id}: {len(quotes)} quotes, {len(miss)} ungrounded{note}")
        for q in miss:
            print(f"       ungrounded quote: {q!r}")
        if weak and (strict or os.environ.get("GROUNDING_VERBOSE")):
            for w in weak:
                print(f"       weak anchor: {w}")
    print(f"\n{total_q - total_miss}/{total_q} quotes grounded across {len(annexes)} annexes.")
    if total_weak:
        print(f"{total_weak} weak anchor(s); GROUNDING_VERBOSE=1 lists them.")
        if strict:
            print("FAIL  GROUNDING_STRICT_ANCHORS is set and the corpus is not at zero. "
                  "Anchor each record on its own table row (build_ground_truth.row_quotes).")
            return 1
    return 0 if total_miss == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
