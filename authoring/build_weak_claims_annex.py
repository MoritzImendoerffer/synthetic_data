#!/usr/bin/env python3
"""Emit the annex fragment for the labeled weak claims and verify grounding.

    Standalone strict check for the feature described in ``authoring/WEAK_CLAIMS.md``. The
    claims are ACTIVE on ``feature/weak-claims-via-brief`` and assigned in each document's
    brief BEFORE it is authored; this script runs afterwards and only ever READS the
    document. It is not the pipeline path — ``pc_package/build_ground_truth.py`` emits the
    annex records — but it is the sharpest single check of the layer.

    The registry is two-phase (``assignment:`` then ``captured:``). A claim that is assigned
    but not yet captured is reported as PENDING and is not a failure: that is the expected
    state between authoring a document and recording the author's wording. A captured quote
    that no longer appears IS a failure, and the fix is always to re-read the document and
    re-record the wording, never to edit the document to match.

Emit the ground-truth annex fragment for the labeled weak claims, and verify each is
grounded (its verbatim quote appears in the document it labels).

    uv run python authoring/build_weak_claims_annex.py --doc PCR-003 \
        --file pc_package/PCR-003_bioreactor.DRAFT.qmd

For each document in ``authoring/weak_claims.yaml`` this:
  1. checks that every planted claim's ``quote`` appears VERBATIM (whitespace-collapsed)
     in the target document — the same grounding rule as ``pc_package/check_grounding.py``;
  2. writes ``authoring/out/<DOC>.weak_claims.json`` — a labeled-assertion fragment
     (``support = "unsupported"`` + weakness_type + rationale) ready to merge into the
     document's ground-truth annex when ``pc_package/build_ground_truth.py`` runs.

The point of the benchmark feature: the quote GROUNDS (it exists in the document) yet is
LABELED weak. A grounding-only check would pass it; a model must use this label to learn
that a fluent, in-register sentence can still be unsupported.

Exit 0 iff every planted claim's quote is grounded.
"""
from __future__ import annotations

import argparse
import glob
import html
import json
import os
import re
import sys
import zipfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")
REGISTRY = os.path.join(HERE, "weak_claims.yaml")


def _collapse(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def doc_text(path: str) -> str:
    """Whitespace-collapsed plain text of a .qmd (comments stripped) or a rendered .docx."""
    if path.endswith(".docx"):
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8")
        xml = re.sub(r"<[^>]+>", " ", xml)
        return _collapse(html.unescape(xml))
    raw = open(path, encoding="utf-8").read()
    raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.DOTALL)  # comments do not render
    return _collapse(raw)


def resolve_file(doc_id: str, explicit: str | None) -> str | None:
    if explicit:
        return explicit if os.path.exists(explicit) else None
    # prefer a rendered docx, then a DRAFT qmd, then the committed qmd
    for pat in (f"pc_package/{doc_id}_*.docx", f"pc_package/{doc_id}_*.DRAFT.qmd",
                f"pc_package/{doc_id}_*.qmd"):
        hits = sorted(glob.glob(os.path.join(ROOT, pat)))
        if hits:
            return hits[0]
    return None


def captured(c: dict) -> dict:
    """The recorded half of a claim, under either registry shape.

    The registry became two-phase when the feature was rebuilt around the brief: an
    ``assignment`` written before the document and a ``captured`` block filled in after it
    renders. Older entries are flat. Reading both shapes keeps this script usable on any
    branch, which is the same reason ``build_rhetorical_annex.py`` does it.
    """
    return c.get("captured") or c


def annex_fragment(doc_id: str, claims: list[dict]) -> dict:
    """A self-contained fragment mirroring the ground-truth annex assertion shape."""
    return {
        "document_id": doc_id,
        "weak_claims": [
            {
                "id": c["id"],
                "section": c.get("section"),
                "support": "unsupported",             # the label: NOT grounded by evidence
                "weakness_type": c["weakness_type"],
                "source_reference": {"quote": _collapse(captured(c)["quote"])},
                "rationale": _collapse(captured(c).get("rationale", "")),
                "correct_version": _collapse(captured(c).get("correct_version", "")),
            }
            for c in claims
            if (captured(c) or {}).get("quote")
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", help="document id (default: every doc in weak_claims.yaml)")
    ap.add_argument("--file", help="document to check the quotes against (qmd or docx)")
    args = ap.parse_args()

    reg = yaml.safe_load(open(REGISTRY, encoding="utf-8"))
    all_claims = reg.get("claims", {}) or {}
    docs = [args.doc] if args.doc else list(all_claims)
    os.makedirs(OUT, exist_ok=True)

    rc = 0
    for doc_id in docs:
        claims = all_claims.get(doc_id, [])
        if not claims:
            print(f"WARN  no claims registered for {doc_id}")
            continue
        path = resolve_file(doc_id, args.file if args.doc else None)
        print(f"== {doc_id} ({len(claims)} planted claim(s)) ==")
        if not path:
            print(f"MISS  no document found to ground against (render or author it first)")
            rc = 1
            continue
        text = doc_text(path)
        grounded = 0
        pending = 0
        for c in claims:
            raw = (captured(c) or {}).get("quote")
            if not raw:
                # Assigned, not yet recorded. Expected between authoring and the capture
                # step; only a captured quote can be checked, and only against the document.
                pending += 1
                print(f"  PEND {c['id']} [{c['weakness_type']}] assigned, wording not recorded yet")
                continue
            q = _collapse(raw)
            ok = q in text
            grounded += ok
            print(f"  {'OK  ' if ok else 'FAIL'} {c['id']} [{c['weakness_type']}]"
                  + ("" if ok else f"\n       ungrounded quote: {q!r}"
                                   f"\n       re-read the document and re-record the wording;"
                                   f" never edit the document to match"))
            if not ok:
                rc = 1
        frag = annex_fragment(doc_id, claims)
        out = os.path.join(OUT, f"{doc_id}.weak_claims.json")
        json.dump(frag, open(out, "w", encoding="utf-8"), indent=2)
        print(f"  {grounded}/{len(claims) - pending} grounded"
              + (f" · {pending} pending capture" if pending else "")
              + f" · wrote {os.path.relpath(out, ROOT)} "
                f"(checked against {os.path.relpath(path, ROOT)})")
    return rc


if __name__ == "__main__":
    sys.exit(main())
