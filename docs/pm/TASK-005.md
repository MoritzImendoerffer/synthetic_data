---
type: pm-task
epic: 2026-08-19_01_fourth-round-one-document
sprint: 2026-08-19_01_fourth-round-one-document
task: TASK-005
status: todo
kind: measurement
title: "Count what the reading named, before/after against the same script, and write the results page"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-007"]
---

> [!warning] Generated from `.claude/work/2026-08-19_01_fourth-round-one-document/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-005 — Count what the reading named, before/after against the same script, and write the results page

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

Every number from measure_apparatus.py or check_style output saved in the unit — no session heredoc. Compare against PCR-007's own baseline (measure_baseline_PCR-007.txt) AND against the probe page, so the reader sees whether a whole document under the regime looks like the two subsections did.

## Acceptance criteria

- [ ] `uv run --extra discourse python ../2026-08-18_03_author-facing-apparatus/measure_apparatus.py pc_package/PCR-007_cex.qmd pc_package/PCR-007_cex.DRAFT.qmd > measure_after_PCR-007.txt` — shipped and new side by side, sources first, all blocks; `uv run python authoring/check_style.py --review` on both saved as check_style_after_PCR-007.txt
- [ ] the results page holds: the regime (inputs and word count, model, check_render passes, one content-review cycle with its per-question counts); the reading verbatim; the rule applied; a table shipped vs new vs the four sources for `, which`, all trailing relatives, `acts on / through`, `governs / sets`, `, so `, `, and `+clause (regex and parser), opens with a connective, passive, chaining, copula, `its`, mean_len, pct_under_15, pct_over_40, staccato — every number from the two saved files; the gate result on both (GATED and the advisory rows); pages and sentence counts; and the comparison with the probe's numbers (docs/results/2026-08-19-apparatus-probe.md §3) in one paragraph
- [ ] a 'what was found on the way' section: <<NEEDS>> the agent hit, helpers extended if any, what the content review flagged and what one cycle changed, anything the RUNNER as rebuilt got wrong
- [ ] a Verification section whose commands are exactly the ones run; the page is linked from docs/results/README.md at ship (TASK-008)
- [ ] written whichever way D6 fell; on FAIL it says 'the draft is kept in the unit and nothing shipped'

**Depends on:** [[TASK-004]]

## Documents it is about

- **PCR-007** — `pc_package/PCR-007_cex.qmd`

## Files it touched

- [[2026-08-<dd>-fourth-round-PCR-007]] — `docs/results/2026-08-<dd>-fourth-round-PCR-007.md`
- `.claude/work/2026-08-19_01_fourth-round-one-document/measure_after_PCR-007.txt`
- `.claude/work/2026-08-19_01_fourth-round-one-document/check_style_after_PCR-007.txt`
