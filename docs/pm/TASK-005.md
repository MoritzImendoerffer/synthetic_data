---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-005
status: done
kind: measurement
title: "Count what the reading named, run the gate on the probe, and write the results page"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-006"]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-005 — Count what the reading named, run the gate on the probe, and write the results page

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Write the page whichever way D4 fell. A FAIL page is the record that the hypothesis was tested and how, and it is what stops a fifth round from re-running the same probe. Keep the reading verbatim in the page too, not only in the unit.

## Acceptance criteria

- [x] `uv run --extra discourse python $U/measure_apparatus.py pc_package/PCR-005_protein_a.EXCERPT.qmd pc_package/PCR-005_protein_a.PROBE.qmd > $U/measure_probe.txt` — all blocks including frames, sources first
- [x] `uv run python authoring/check_style.py pc_package/PCR-005_protein_a.PROBE.qmd` run as the gate stands (before TASK-006): the pass/fail and every failing row recorded verbatim; the same on the EXCERPT (expected: excerpt OK; the probe's mean_len / pct_under_15 result is the test of results §5.1 and is recorded whichever way it falls)
- [x] docs/results/2026-08-18-apparatus-probe.md exists with: the regime (inputs, word counts from TASK-002, model), the owner's reading verbatim, the decision-rule application, a table shipped-excerpt vs probe vs the four sources for `, which`, all trailing relatives, acts-through, follows-from, governs/sets, mean_len, pct_under_15, passive; the gate result on both; the mechanistic_warrant span audit line (26 / 6); a Verification section whose commands are exactly the ones above; and, if FAIL, the sentence 'the proposal is retired and results §8 stands'
- [x] every number on the page comes from measure_probe.txt or the check_style output saved in the unit — no session heredoc (results §9's defect is not repeated)
- [x] the roadmap row 0 and docs/next/README.md row 0 are updated to say what D4 settled and where the page is

**Depends on:** [[TASK-001]], [[TASK-004]]

## What was built

Page: docs/results/2026-08-19-apparatus-probe.md (dated by the reading, 2026-08-19, not the plan's 2026-08-18). Every number on it is from measure_probe.txt (measure_apparatus.py over EXCERPT + PROBE, all blocks, sources first), check_style_probe.txt, check_style_excerpt.txt, or the --spans run; no session heredoc.

What moved with the reading (per 100 sentences, shipped -> probe, sources): `, which` 25.4 -> 5.6 (0.6-2.4); all trailing relatives 28.8 -> 6.7 (1.2-3.0); follows from / behaves as / physical chemistry / confirms the expectation / aggressive each 1.7 -> 0; governs/sets 5.1 -> 1.1; acts on/through 1.7 -> 3.3 (the one frame that survived — three sentences, each followed by a concrete quantity, quoted on the page).

What moved the other way while the reader preferred it: `, so ` 0.0 -> 8.9 % (sources 0.1-0.4); `, and `+clause 0.0 -> 15.6 regex / 19.3 parser (1-3.4); opens with a connective 11.9 -> 0.0 (3.7-6.1); passive 38.6 -> 31.8 (57-64); `the <noun> is` 9.8 -> 15.9 per 1k (3.4-6.0); staccato 5.1 -> 7.8. Every measure rounds one to three gated or printed sits at or beyond round-zero in the probe. THE FINDING: those measures never tracked the reader's judgement.

The gate as it stands: PROBE FAILS — pct_over_40 1.1 (floor 3.0), rather_than 1.6 per 1k (3 in 1,829; ceiling 0.8); mean_len 20.3 / median 18.0 / pct_under_15 31.1 / paren 3.3 all within a tenth of their edges. EXCERPT passes every row. Results §5.1 predicted mean_len and pct_under_15; the fail landed on the neighbouring rows, same direction. The gate rejects the preferred text and passes the rejected one — TASK-006 stands.

Span audit line on the page: 26 / 7 (the six named + PCR-006-R14). ROADMAP row 0 and docs/next/README.md row 0 updated to D4 = PASS with the page linked.

## Documents it is about

- **PCR-006** — `pc_package/PCR-006_viral_inactivation.qmd`

## Files it touched

- [[2026-08-19-apparatus-probe]] — `docs/results/2026-08-19-apparatus-probe.md`
- `.claude/work/2026-08-18_03_author-facing-apparatus/measure_probe.txt`
- `.claude/work/2026-08-18_03_author-facing-apparatus/check_style_probe.txt`
- `.claude/work/2026-08-18_03_author-facing-apparatus/check_style_excerpt.txt`
