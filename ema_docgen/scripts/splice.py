#!/usr/bin/env python3
"""Apply an insertions file to a .qmd, additively.

The agent never edits the document; this does. Each anchor must resolve to
exactly one span. Insertions are placed as new paragraphs after the paragraph
containing their anchor, so existing paragraphs stay byte-identical — which is
what the ground-truth grounding test depends on.

All-or-nothing: if any insertion fails to resolve, nothing is written.

    python splice.py --qmd pc_package/PCR-007_cex.qmd \
        --insertions build/insertions/PCR-007/deviations.yaml [--dry-run]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from _common import fenced_regions, in_regions, line_of, locate_anchor, paragraph_end


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--qmd", required=True, type=Path)
    ap.add_argument("--insertions", required=True, type=Path)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    text = args.qmd.read_text(encoding="utf-8")
    original_len = len(text)
    fences = fenced_regions(text)

    data = yaml.safe_load(args.insertions.read_text(encoding="utf-8"))
    insertions = data.get("insertions") or []

    planned: list[tuple[int, str, str]] = []  # (offset, body, anchor_preview)
    failures: list[str] = []

    for n, ins in enumerate(insertions, 1):
        anchor = (ins.get("anchor") or "").strip()
        body = (ins.get("insert_after") or "").strip()
        spans = locate_anchor(text, anchor)

        if len(spans) != 1:
            failures.append(
                f"insertion {n}: {len(spans)} matches for anchor {anchor[:60]!r}"
            )
            continue
        start, end = spans[0]
        if in_regions(start, fences):
            failures.append(f"insertion {n}: anchor inside fenced code block")
            continue

        planned.append((paragraph_end(text, end), body, anchor[:60]))

    if failures:
        for f in failures:
            print(f"ERROR  {f}")
        print("ABORT  no changes written")
        return 1

    # Resolve report line numbers against the ORIGINAL text, before any
    # mutation — once text is spliced, the planned offsets no longer line up
    # with it and line_of() would report drifted (wrong) line numbers.
    report = [(line_of(text, offset), preview)
              for offset, _, preview in sorted(planned, key=lambda p: p[0])]

    # Apply in reverse offset order so earlier offsets remain valid.
    for offset, body, preview in sorted(planned, key=lambda p: -p[0]):
        addition = "\n\n" + body
        if offset >= len(text):
            addition = "\n\n" + body + "\n"
        text = text[:offset] + addition + text[offset:]

    added_words = sum(len(b.split()) for _, b, _ in planned)
    for orig_line, preview in report:
        print(f"       after line {orig_line}: {preview}...")

    if args.dry_run:
        print(f"DRY    {len(planned)} insertion(s), +{added_words} words "
              f"(nothing written)")
        return 0

    args.qmd.write_text(text, encoding="utf-8")
    print(f"OK     {args.qmd}: {len(planned)} insertion(s), "
          f"+{added_words} words, {original_len} -> {len(text)} chars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
