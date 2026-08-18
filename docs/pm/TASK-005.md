---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-005
status: todo
kind: measurement
title: "Count what the reading named, run the gate on the probe, and write the results page"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-005 — Count what the reading named, run the gate on the probe, and write the results page

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

Write the page whichever way D4 fell. A FAIL page is the record that the hypothesis was tested and how, and it is what stops a fifth round from re-running the same probe. Keep the reading verbatim in the page too, not only in the unit.

## Acceptance criteria

- [ ] `uv run --extra discourse python $U/measure_apparatus.py pc_package/PCR-005_protein_a.EXCERPT.qmd pc_package/PCR-005_protein_a.PROBE.qmd > $U/measure_probe.txt` — all blocks including frames, sources first
- [ ] `uv run python authoring/check_style.py pc_package/PCR-005_protein_a.PROBE.qmd` run as the gate stands (before TASK-006): the pass/fail and every failing row recorded verbatim; the same on the EXCERPT (expected: excerpt OK; the probe's mean_len / pct_under_15 result is the test of results §5.1 and is recorded whichever way it falls)
- [ ] docs/results/2026-08-18-apparatus-probe.md exists with: the regime (inputs, word counts from TASK-002, model), the owner's reading verbatim, the decision-rule application, a table shipped-excerpt vs probe vs the four sources for `, which`, all trailing relatives, acts-through, follows-from, governs/sets, mean_len, pct_under_15, passive; the gate result on both; the mechanistic_warrant span audit line (26 / 6); a Verification section whose commands are exactly the ones above; and, if FAIL, the sentence 'the proposal is retired and results §8 stands'
- [ ] every number on the page comes from measure_probe.txt or the check_style output saved in the unit — no session heredoc (results §9's defect is not repeated)
- [ ] the roadmap row 0 and docs/next/README.md row 0 are updated to say what D4 settled and where the page is

**Depends on:** [[TASK-001]], [[TASK-004]]

## Files it touched

- [[2026-08-18-apparatus-probe]] — `docs/results/2026-08-18-apparatus-probe.md`
- `.claude/work/2026-08-18_03_author-facing-apparatus/measure_probe.txt`
