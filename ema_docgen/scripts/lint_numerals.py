#!/usr/bin/env python3
"""Fail on bare numerals in prose.

Every measurement in these documents must come from the seeded model via an
inline expression or helper call. A number typed directly into prose is either
invented or hand-copied, and both break the guarantee that the annexes and the
document cannot disagree.

Identifiers are exempt — document IDs, guidance names, citation keys and
cross-reference labels are names, not measurements.

    python lint_numerals.py pc_package/PCR-007_cex.qmd [...]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from _common import blank_out, line_of, prose_only

EXEMPT = [
    re.compile(r"`[^`]*`"),                        # inline code, incl. `{python} ...`
    re.compile(r"\[@[^\]]+\]"),                    # [@amab2009; @ichq8]
    re.compile(r"@(?:tbl|fig|sec|eq|lst)-[\w-]+"), # @tbl-cqa
    re.compile(r"\b[A-Z]{2,6}-\d{2,4}(?:-\d{2})?\b"),  # SOP-2007, DEV-007-02
    re.compile(r"\bICH\s+Q\d+[A-Z]?\b"),
    re.compile(r"\bPDA\s+TR\s+\d+\b"),
    re.compile(r"\bISO\s+\d+\b"),
    re.compile(r"\bUSP\s*<\d+>\b"),
    re.compile(r"§\s*\d+(?:\.\d+)*"),
    re.compile(r"\{[^}\n]*\}"),                    # {#tbl-cqa}, {width=100%}, attrs
    re.compile(r"https?://\S+"),
    re.compile(r"^\s*#{1,6}\s.*$", re.MULTILINE),  # headings
    # --- domain nomenclature: names, not measurements ---
    re.compile(r"\bStage\s+\d\b"),                 # Stage 1 / Stage 2
    re.compile(r"\bStep\s+\d+\b"),                 # Step 7
    re.compile(r"\bTool\s*#\s*\d\b"),              # A-Mab Tool #1
    re.compile(r"\bIgG\d\b"),
    re.compile(r"\bQ\d{1,2}[A-Z]?\b"),             # ICH Q8, Q9, Q11
    re.compile(r"\bTechnical\s+Report\s+\d+\b"),
    re.compile(r"\b(?:FDA|EMA|ICH|EU|WHO|CMC)\s+\d{4}\b"),
    re.compile(r"\bPhase\s+[I]+[a-z]?\b"),
]

DEFAULT_ALLOW_FILE = "ema_docgen/numerals.allow"

DIGIT = re.compile(r"\d")


def load_allow(path: Path | None) -> list[re.Pattern]:
    """Extra exemption regexes, one per line; # comments and blanks ignored.

    Compiled with ``re.MULTILINE`` so that a ``^``-anchored rule (e.g. the ordered-list
    marker rule ``^\\s*\\d+\\.\\s``) matches at the start of every line rather than only at
    the start of the whole document — which is what the author of that rule intended, and
    what the built-in EXEMPT heading pattern already does.
    """
    if path is None or not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(re.compile(line, re.MULTILINE))
    return out


def check(path: Path, show: int, extra: list[re.Pattern]) -> int:
    raw = path.read_text(encoding="utf-8")
    text = prose_only(raw)

    for pattern in EXEMPT + extra:
        spans = [(m.start(), m.end()) for m in pattern.finditer(text)]
        text = blank_out(text, spans)

    hits = list(DIGIT.finditer(text))
    if not hits:
        print(f"OK     {path}")
        return 0

    # collapse to one report per line
    lines: dict[int, str] = {}
    for m in hits:
        ln = line_of(raw, m.start())
        if ln not in lines:
            lines[ln] = raw.splitlines()[ln - 1].strip()

    print(f"FAIL   {path}: {len(lines)} line(s) with bare numerals in prose")
    for ln in sorted(lines)[:show]:
        print(f"       {ln}: {lines[ln][:100]}")
    if len(lines) > show:
        print(f"       ... and {len(lines) - show} more")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--show", type=int, default=15)
    ap.add_argument("--allow-file", type=Path, default=Path(DEFAULT_ALLOW_FILE),
                    help="extra exemption regexes, one per line")
    args = ap.parse_args()
    extra = load_allow(args.allow_file)
    if extra:
        print(f"       {len(extra)} extra exemption(s) from {args.allow_file}")
    return max(check(p, args.show, extra) for p in args.paths)


if __name__ == "__main__":
    sys.exit(main())
