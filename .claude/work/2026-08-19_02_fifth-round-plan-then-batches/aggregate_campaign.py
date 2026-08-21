#!/usr/bin/env python3
"""Corpus-level before/after for the fifth-round campaign, from one file.

    uv run --extra discourse python .claude/work/2026-08-19_02_fifth-round-plan-then-batches/\
aggregate_campaign.py

It shells out to `measure_apparatus.py --check-baseline` over all 20 shipped .qmd, parses the
`baseline X, script Y` cells that command already prints, and reports the corpus median before and
after for each measure. It computes nothing of its own: every number here is a number that script
produced, aggregated. The baseline is the pre-campaign corpus recorded in work unit
2026-08-18_02_register-track-d; "after" is the corpus as promoted at the end of this unit.

Written for TASK-040 so the results page cites code rather than a session heredoc, which is the
failure recorded in docs/results/2026-08-18-track-d-stopped.md §9.
"""
import re, subprocess, statistics, collections, glob, sys, os

ROOT = "/home/moritz/github_repos/synthetic_data"
MEASURE = os.path.join(
    ROOT, ".claude/work/2026-08-18_03_author-facing-apparatus/measure_apparatus.py")

def main():
    docs = sorted(glob.glob(os.path.join(ROOT, "pc_package/*.qmd")))
    out = subprocess.run(
        ["uv", "run", "--extra", "discourse", "python", MEASURE, "--check-baseline", *docs],
        capture_output=True, text=True, cwd=ROOT).stdout
    cells = collections.defaultdict(list)
    pat = re.compile(r"^(?:FAIL|OK)\s+(\w+)\s+(.+?)\s+/\s+(\S+\.qmd):\s+baseline\s+([\d.]+),"
                     r"\s+script\s+([\d.]+)")
    for line in out.split("\n"):
        m = pat.match(line.strip())
        if m:
            block, measure, doc, before, after = m.groups()
            cells[(block, measure)].append((doc, float(before), float(after)))
    print(f"{len(docs)} documents; {sum(len(v) for v in cells.values())} cells\n")
    print(f"{'block':<10} {'measure':<52} {'n':>3} {'before':>8} {'after':>8} {'delta':>8}")
    for (block, measure), rows in sorted(cells.items()):
        b = statistics.median(r[1] for r in rows)
        a = statistics.median(r[2] for r in rows)
        print(f"{block:<10} {measure[:52]:<52} {len(rows):>3} {b:>8.1f} {a:>8.1f} {a-b:>+8.1f}")

if __name__ == "__main__":
    main()
