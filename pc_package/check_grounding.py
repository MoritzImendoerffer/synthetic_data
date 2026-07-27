#!/usr/bin/env python3
"""Grounding check for the A-Mab ground-truth annexes.

For every ``ground_truth/<ID>.json`` this verifies that each
``SourceReference.quote`` appears **verbatim** in the matching rendered document
(the ``.docx`` named by the annex ``inventory.file_name``), under whitespace-
collapsed comparison — a quote that spans a line wrap in the rendered text still
matches. This is the machine-checkable form of golden rule 3 ("everything is
grounded"): prose may only state what the data supports, and every annex quote
must exist in the document it annotates.

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


def docx_text(path: str) -> str:
    """Whitespace-collapsed plain text of a .docx (word/document.xml)."""
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    xml = re.sub(r"<[^>]+>", " ", xml)
    return re.sub(r"\s+", " ", html.unescape(xml)).strip()


def _quotes(obj):
    """Yield every ``quote`` string anywhere in the annex JSON."""
    if isinstance(obj, dict):
        q = obj.get("quote")
        if isinstance(q, str):
            yield q
        for v in obj.values():
            yield from _quotes(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _quotes(v)


# A quote that grounds is not automatically a quote that attests anything. Three shapes
# ground trivially while pointing at prose that contains neither end of the relation they
# claim: a span short enough to be ubiquitous ("acceptance criteria"), one sentence reused
# as the anchor for many records (RA-001 once used a single placeholder for 41 separate
# assertions), and a span that occurs several times in the document so the reference is
# ambiguous. The corpus convention is to anchor a per-record assertion on the RENDERED
# TABLE ROW carrying the relation, so the span contains both ends.
MAX_QUOTE_REUSE = 8       # one span anchoring more records than this attests little
MAX_DOC_OCCURRENCES = 3   # a span this common in the document is an ambiguous reference


def specificity_report(annex, text) -> list[str]:
    """Advisory warnings about quotes that ground but attest little.

    Deliberately NOT a word-count rule. The corpus convention is to anchor a per-record
    assertion on the rendered table row carrying the relation, and those rows are short —
    "Production Bioreactor Culture pH" is four words and names both ends of what it
    asserts, which makes it a better anchor than a twelve-word sentence that merely
    discusses the topic. What actually signals a weak anchor is *non-distinctiveness*:
    the same span standing in for many different records, or appearing so often in the
    document that the reference is ambiguous.
    """
    from collections import Counter
    counts = Counter(re.sub(r"\s+", " ", q).strip() for q in _quotes(annex))
    out = []
    for norm, n in counts.most_common():
        if n > MAX_QUOTE_REUSE:
            out.append(f"anchors {n} records: {norm[:70]!r}")
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
        quotes = list(_quotes(annex))
        miss = [q for q in quotes if re.sub(r"\s+", " ", q).strip() not in text]
        total_q += len(quotes)
        total_miss += len(miss)
        weak = specificity_report(annex, text)
        status = "OK  " if not miss else "FAIL"
        note = f", {len(weak)} weak anchor(s)" if weak else ""
        print(f"{status} {doc_id}: {len(quotes)} quotes, {len(miss)} ungrounded{note}")
        for q in miss:
            print(f"       ungrounded quote: {q!r}")
        if weak and os.environ.get("GROUNDING_VERBOSE"):
            for w in weak:
                print(f"       weak anchor: {w}")
    print(f"\n{total_q - total_miss}/{total_q} quotes grounded across {len(annexes)} annexes.")
    return 0 if total_miss == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
