#!/usr/bin/env python3
"""Validate an insertions file before it is applied.

Runs ahead of splice.py so a malformed or ambiguous insertion never reaches the
document. Exits non-zero on any error; warnings do not fail the run.

    python validate_insertions.py --qmd pc_package/PCR-007_cex.qmd \
        --insertions build/insertions/PCR-007/deviations.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from _common import fenced_regions, in_regions, line_of, locate_anchor

ALLOWED_TOP = {"doc_id", "section_id", "insertions"}
ALLOWED_INS = {"anchor", "insert_after"}
MIN_ANCHOR_CHARS = 40


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--qmd", required=True, type=Path)
    ap.add_argument("--insertions", required=True, type=Path)
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    text = args.qmd.read_text(encoding="utf-8")
    fences = fenced_regions(text)

    try:
        data = yaml.safe_load(args.insertions.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"ERROR  unparseable YAML: {exc}")
        return 1

    if not isinstance(data, dict):
        print("ERROR  top level is not a mapping")
        return 1

    extra = set(data) - ALLOWED_TOP
    if extra:
        errors.append(f"unexpected top-level keys: {sorted(extra)}")
    for req in ("doc_id", "section_id", "insertions"):
        if req not in data:
            errors.append(f"missing top-level key: {req}")

    insertions = data.get("insertions") or []
    if not isinstance(insertions, list) or not insertions:
        errors.append("insertions must be a non-empty list")
        insertions = []

    for n, ins in enumerate(insertions, 1):
        tag = f"insertion {n}"
        if not isinstance(ins, dict):
            errors.append(f"{tag}: not a mapping")
            continue

        extra = set(ins) - ALLOWED_INS
        if extra:
            # this is the no-rewrite guarantee: replace/delete have no schema slot
            errors.append(f"{tag}: forbidden keys {sorted(extra)} — "
                          "only anchor and insert_after exist, by design")

        anchor = (ins.get("anchor") or "").strip()
        body = (ins.get("insert_after") or "").strip()

        if not anchor:
            errors.append(f"{tag}: empty anchor")
            continue
        if not body:
            errors.append(f"{tag}: empty insert_after")

        spans = locate_anchor(text, anchor)
        if not spans:
            errors.append(f"{tag}: anchor not found — "
                          f"{anchor[:60]!r}")
            continue
        if len(spans) > 1:
            lines = ", ".join(str(line_of(text, s)) for s, _ in spans)
            errors.append(f"{tag}: anchor is ambiguous, {len(spans)} matches "
                          f"at lines {lines} — choose a longer anchor")
            continue

        start, _ = spans[0]
        if in_regions(start, fences):
            errors.append(f"{tag}: anchor falls inside a fenced code block "
                          f"(line {line_of(text, start)})")

        if len(anchor) < MIN_ANCHOR_CHARS:
            warnings.append(f"{tag}: anchor is short ({len(anchor)} chars); "
                            "collision risk grows as the document fills")
        if "`{python}" in anchor:
            warnings.append(f"{tag}: anchor contains an inline expression; "
                            "prefer a sentence of plain prose")

    for w in warnings:
        print(f"WARN   {w}")
    for e in errors:
        print(f"ERROR  {e}")

    if errors or (args.strict and warnings):
        print(f"FAIL   {args.insertions}")
        return 1
    print(f"OK     {args.insertions} — {len(insertions)} insertion(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
