# TASK-002 procedure — the measurement, as a file

**This task exists because the same failure has now happened twice.** Round two's owner-reading
counts lived in a heredoc in the session that produced them and were in no file; round three's
first task had to reconstruct them from a results page and prove they reproduced. The proposal's
Track C figure — 1.5 % `, so ` in `WRITING_GUIDE.md`, "measured 2026-08-17" — came from an unsaved
method and re-measured at **3.77 %** on 2026-08-18. The two are not comparable and the older one
cannot be checked.

So: **no number this round publishes may come from anywhere but `measure_trackd.py`.**

## What it must print

One row per document, one column per measure, every rate with its denominator, plus the four human
source columns from `refs/text/`:

- from `check_style.py`: `, so `, opens-with-a-connective, 2+ coordinators, `, and `+clause (regex,
  a **floor**), `, not `, and the five length numbers (mean, median, over-40, over-55, under-15);
- from `check_discourse.py` (needs `--extra discourse`): topic chaining, copula, adjunct front
  field, passive, `, and `+clause (parser). All but chaining divide by the sentences that have a
  root and a subject;
- the two measures round three had to compute by hand and must not have to again: `, which` per
  sentence, and the staccato — sentences inside a run of three or more consecutive sentences under
  fifteen words, which the sources run at 0.37–3.94 % and round three's `PCR-003` at 6.86 %;
- possessives per 1000 words (`its`, `their`, `it is/was`, `the <noun> is`).

**Wrap the two gates; do not re-implement them.** Import `prose_from_qmd`, `prose_from_extract`,
`sentences`, `HUMAN_SOURCES` from `check_style`, and shell out to or import `check_discourse`.
A second implementation of a measure is a second answer to the same question.

## Acceptance, literally

```bash
uv run python .claude/work/2026-08-18_02_register-track-d/measure_trackd.py $(ls pc_package/*.qmd) > /tmp/now.txt
```

must reproduce `measure_baseline_style.txt` and `measure_baseline_discourse.txt` to one decimal,
including these, which are the ones a mistake would move:

| document | measure | value |
|---|---|---|
| PCP-005 | passive | 66.7 % — above the source band |
| PCP-008 | passive | 67.7 % — the highest in the corpus |
| RA-001 | passive | 64.2 % — also above |
| RA-001 | `, so ` | 14.6 % — the worst in the corpus |
| PCR-004 | `, and `+clause | 29.3 % — the worst |
| PCR-003 | `, and `+clause | 0.5 % — the only document at target |

Those six are the fixture. If the script disagrees with the baseline on any of them, the script is
wrong, not the baseline.
