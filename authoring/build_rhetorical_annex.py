#!/usr/bin/env python3
"""Ground the curated rhetorical-role spans for a document and emit the annex layer.

    uv run python authoring/build_rhetorical_annex.py --doc PCR-003 \
        --file pc_package/PCR-003_bioreactor.DRAFT.qmd

Reads ``authoring/rhetorical/<DOC>.spans.yaml`` (curated spans: id, section, role, quote,
and relation fields) and:
  1. checks every span's ``quote`` appears VERBATIM (whitespace-collapsed) in the document
     — the same grounding rule as ``pc_package/check_grounding.py``;
  2. merges the ``weak_claims.yaml`` claims that are present in the document as
     ``role: weak_claim`` (``support: unsupported``), and skips the ones that are not;
  3. validates that every relation target (``supported_by`` / ``restates`` / ``bounds``)
     resolves to an existing span id;
  4. writes ``authoring/out/<DOC>.rhetorical.json`` — the labeled spans plus the argument
     (claim<-justification) and coreference (restatement->claim) edge lists.

See RHETORICAL_ANNEX.md for the taxonomy. Exit 0 iff every span grounds and every relation
target resolves.
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
SPANS_DIR = os.path.join(HERE, "rhetorical")
WEAK = os.path.join(HERE, "weak_claims.yaml")

ROLES = {
    "problem_statement", "claim", "justification", "mechanistic_warrant", "hedge",
    "bounded_conclusion", "cross_step_credit", "deviation_disposition", "deferral",
    "restatement", "weak_claim",
}


def _collapse(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def doc_text(path: str) -> str:
    if path.endswith(".docx"):
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8")
        return _collapse(html.unescape(re.sub(r"<[^>]+>", " ", xml)))
    raw = open(path, encoding="utf-8").read()
    raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.DOTALL)
    return _collapse(raw)


def resolve_file(doc_id: str, explicit: str | None) -> str | None:
    if explicit:
        return explicit if os.path.exists(explicit) else None
    for pat in (f"pc_package/{doc_id}_*.docx", f"pc_package/{doc_id}_*.DRAFT.qmd",
                f"pc_package/{doc_id}_*.qmd"):
        hits = sorted(glob.glob(os.path.join(ROOT, pat)))
        if hits:
            return hits[0]
    return None


def _registered_quote(claim: dict) -> str | None:
    """The claim's wording, under either registry shape.

    A two-phase registry records it under ``captured.quote`` (filled in after the document is
    authored) and leaves it null while the claim is only assigned; a flat registry puts it
    directly under ``quote``.
    """
    captured = claim.get("captured")
    if isinstance(captured, dict):
        return captured.get("quote")
    return claim.get("quote")


def weak_claim_spans(doc_id: str, text: str) -> list[dict]:
    """Registered weak claims that are actually in the document, as spans.

    A registered claim whose wording is absent is **skipped with a note**, not emitted. That
    is the normal state whenever the feature is not applied to a document: the registry
    outlives the claims, so emitting them would put spans in the annex whose text exists
    nowhere in the document. ``pc_package/build_ground_truth.py`` skips them for the same
    reason — the two builders have to agree, or the annex disagrees with itself.
    """
    if not os.path.exists(WEAK):
        return []
    reg = yaml.safe_load(open(WEAK, encoding="utf-8")) or {}
    out, skipped = [], []
    for c in (reg.get("claims", {}) or {}).get(doc_id, []):
        raw = _registered_quote(c)
        quote = _collapse(raw) if raw else ""
        if not quote or quote not in text:
            skipped.append(c["id"])
            continue
        out.append({"id": c["id"], "section": c.get("section"), "role": "weak_claim",
                    "support": "unsupported", "weakness_type": c.get("weakness_type"),
                    "quote": quote})
    if skipped:
        print(f"  note  {len(skipped)} registered weak claim(s) not in this document, so not "
              f"in the layer ({', '.join(skipped)}). Expected unless the document was authored "
              f"with them.")
    return out


def build(doc_id: str, path: str) -> tuple[dict, int]:
    spans_file = os.path.join(SPANS_DIR, f"{doc_id}.spans.yaml")
    curated = []
    if os.path.exists(spans_file):
        curated = (yaml.safe_load(open(spans_file, encoding="utf-8")) or {}).get("spans", []) or []
    text = doc_text(path)
    merged = list(curated) + weak_claim_spans(doc_id, text)
    ids = {s["id"] for s in merged}

    errs = 0
    role_counts: dict[str, int] = {}
    for s in merged:
        role = s.get("role")
        if role not in ROLES:
            print(f"FAIL  {s.get('id')}: unknown role {role!r} (see RHETORICAL_ANNEX.md)")
            errs += 1
        role_counts[role] = role_counts.get(role, 0) + 1
        q = _collapse(s.get("quote", ""))
        s["quote"] = q
        if q not in text:
            print(f"FAIL  {s.get('id')} [{role}] ungrounded quote: {q!r}")
            errs += 1
        for field in ("supported_by", "restates", "bounds"):
            tgt = s.get(field)
            if tgt is None:
                continue
            for t in (tgt if isinstance(tgt, list) else [tgt]):
                if t not in ids:
                    print(f"FAIL  {s.get('id')}: {field} -> unknown span id {t!r}")
                    errs += 1

    argument_links = [{"claim": s["id"], "justification": j}
                      for s in merged for j in (s.get("supported_by") or [])]
    coref_links = [{"restatement": s["id"], "claim": s["restates"]}
                   for s in merged if s.get("restates")]

    layer = {
        "document_id": doc_id,
        "taxonomy": sorted(ROLES),
        "rhetorical_spans": merged,
        "argument_links": argument_links,
        "coreference_links": coref_links,
    }
    print(f"  roles: " + ", ".join(f"{r}={n}" for r, n in sorted(role_counts.items())))
    print(f"  {len(merged)} spans · {len(argument_links)} claim<-justification edges · "
          f"{len(coref_links)} coreference edges")
    return layer, errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", required=True)
    ap.add_argument("--file", help="document to ground against (qmd or docx)")
    args = ap.parse_args()

    path = resolve_file(args.doc, args.file)
    print(f"== {args.doc} ==")
    if not path:
        print("MISS  no document found to ground against")
        return 1
    layer, errs = build(args.doc, path)
    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, f"{args.doc}.rhetorical.json")
    if errs:
        # Never leave a failing layer on disk. It would carry spans that are not in the
        # document, and nothing downstream re-checks a file that already exists.
        if os.path.exists(out):
            os.remove(out)
            print(f"      removed the previous {os.path.relpath(out, ROOT)}")
        print(f"FAIL  not written; {errs} error(s) against "
              f"{os.path.relpath(path, ROOT)}. Fix the spans, then re-run.")
        return 1
    json.dump(layer, open(out, "w", encoding="utf-8"), indent=2)
    print(f"OK    wrote {os.path.relpath(out, ROOT)} "
          f"(grounded against {os.path.relpath(path, ROOT)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
