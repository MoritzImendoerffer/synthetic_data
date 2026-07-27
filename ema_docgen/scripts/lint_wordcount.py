#!/usr/bin/env python3
"""Compare per-section prose word counts against the docspec targets.

The target is a lint tolerance band, never an instruction to the agent — telling
a model to hit a word count produces padding. This exists so sections that came
out far off can be found, which usually means the fact pack was thin rather than
the prose being wrong.

    python lint_wordcount.py --docspec ema_docgen/docspec/PCR-007.yaml \
        --qmd pc_package/PCR-007_cex.qmd
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

from _common import prose_only

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*(?:\{[^}]*\})?\s*$", re.MULTILINE)


def norm_heading(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def sections_in(text: str) -> list[tuple[str, int, int]]:
    """(heading_text, body_start, body_end) for each heading, prose only."""
    prose = prose_only(text)
    marks = [(m.group(2), m.end()) for m in HEADING.finditer(prose)]
    out = []
    for i, (title, start) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(prose)
        # trim the next heading line itself
        if i + 1 < len(marks):
            end = prose.rfind("\n", 0, end)
            nl = prose.rfind("\n", 0, end)
            end = nl if nl != -1 else end
        out.append((title, start, end))
    return [(t, s, e) for t, s, e in out]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docspec", required=True, type=Path)
    ap.add_argument("--qmd", required=True, type=Path)
    args = ap.parse_args()

    spec = yaml.safe_load(args.docspec.read_text(encoding="utf-8"))
    text = args.qmd.read_text(encoding="utf-8")
    prose = prose_only(text)

    found = {norm_heading(t): (s, e) for t, s, e in sections_in(text)}

    status = 0
    missing = []
    pending = []
    rows = []
    for sec in spec.get("sections", []):
        heading = sec["heading"]
        # A docspec heading that still carries an unfilled placeholder — e.g.
        # "DEV-01 — <title from the fact pack>" on a new_section entry — cannot
        # match a rendered heading yet. Report it as PENDING rather than MISS,
        # and do not fail: the section has not been written. Finalize the
        # heading in the docspec once the section exists.
        if "<" in heading:
            pending.append(sec["id"])
            continue
        key = norm_heading(heading)
        target = sec["target_words"]
        tol = sec.get("tolerance", 0.25)
        if key not in found:
            missing.append(sec["id"])
            continue
        s, e = found[key]
        actual = len(prose[s:e].split())
        lo, hi = target * (1 - tol), target * (1 + tol)
        flag = "" if lo <= actual <= hi else ("LOW" if actual < lo else "HIGH")
        if flag:
            status = 1
        rows.append((sec["id"], actual, target, flag))

    width = max((len(r[0]) for r in rows), default=10)
    for sid, actual, target, flag in rows:
        print(f"       {sid:<{width}}  {actual:>5} / {target:<5} {flag}")

    if pending:
        # Non-fatal: these sections are not written yet.
        print(f"PEND   docspec heading not finalized (fill the <...> placeholder "
              f"once written): {', '.join(pending)}")
    if missing:
        status = 1
        print(f"MISS   headings not present in {args.qmd.name}: "
              f"{', '.join(missing)}")

    print(("FAIL   " if status else "OK     ") + str(args.qmd))
    return status


if __name__ == "__main__":
    sys.exit(main())
