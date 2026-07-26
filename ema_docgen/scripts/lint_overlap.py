#!/usr/bin/env python3
"""Report n-gram overlap between generated prose and source literature.

The A-Mab case study and the cited FDA/ICH guidance are near-certainly in the training data of
any model this corpus is used to evaluate. If the corpus carries their phrasing,
retrieval and QA scores measure memorisation rather than retrieval — a
contaminated benchmark, and one that is hard to detect after the fact.

This is a corpus property worth tracking, not a hard gate. Default is to warn.

    python lint_overlap.py --refs refs/text/amab.txt \
        --targets pc_package/PCR-007_cex.qmd --n 8 --max-hits 0
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from _common import prose_only

WORD = re.compile(r"[a-z0-9]+")


def tokens(text: str) -> list[str]:
    return WORD.findall(text.lower())


def ngrams(toks: list[str], n: int) -> list[tuple[str, ...]]:
    return [tuple(toks[i:i + n]) for i in range(len(toks) - n + 1)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refs", nargs="+", required=True, type=Path)
    ap.add_argument("--targets", nargs="+", required=True, type=Path)
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--max-hits", type=int, default=0,
                    help="fail above this many overlapping n-grams")
    ap.add_argument("--show", type=int, default=10)
    args = ap.parse_args()

    ref_grams: set[tuple[str, ...]] = set()
    for ref in args.refs:
        ref_grams |= set(ngrams(tokens(ref.read_text(encoding="utf-8",
                                                     errors="replace")), args.n))
    print(f"       reference {args.n}-grams: {len(ref_grams):,}")

    status = 0
    for target in args.targets:
        toks = tokens(prose_only(target.read_text(encoding="utf-8")))
        grams = ngrams(toks, args.n)
        hits = [g for g in grams if g in ref_grams]
        uniq = sorted(set(hits))

        if len(uniq) > args.max_hits:
            print(f"FAIL   {target}: {len(uniq)} overlapping {args.n}-gram(s) "
                  f"of {len(grams):,}")
            for g in uniq[:args.show]:
                print(f"       \"{' '.join(g)}\"")
            if len(uniq) > args.show:
                print(f"       ... and {len(uniq) - args.show} more")
            status = 1
        else:
            print(f"OK     {target}: {len(uniq)} overlapping {args.n}-gram(s)")
    return status


if __name__ == "__main__":
    sys.exit(main())
