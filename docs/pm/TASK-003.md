---
type: pm-task
epic: 2026-08-19_01_fourth-round-one-document
sprint: 2026-08-19_01_fourth-round-one-document
task: TASK-003
status: todo
kind: measurement
title: "Content review before the reading: the four questions on the draft, at most one return to the author"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-007"]
---

> [!warning] Generated from `.claude/work/2026-08-19_01_fourth-round-one-document/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-003 — Content review before the reading: the four questions on the draft, at most one return to the author

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

This is the pipeline's own review step, and it is what the reading judges. One cycle only: the calibration (predecessor, content-review-calibration.md) showed the judge is stricter than the owner and consistent, so a second cycle would be tuning the draft to the judge. The judge must not have read the guide, any counter, or the shipped PCR-007. Keep the run-1 draft (`cp` to $U/PCR-007_cex.DRAFT.run1.qmd) so the results page can say what one cycle changed.

## Acceptance criteria

- [ ] a fresh-context agent (model recorded), given exactly the prompt of ../2026-08-18_03_author-facing-apparatus/procedures/REVIEW-BEFORE-PROMOTION.md and the DRAFT's PDF and nothing else, reports the flagged sentences per question, verbatim, and the four yes/no answers; filed as content-review-PCR-007-draft.md (run 1)
- [ ] if any question reads 'no': the SAME authoring agent (the TASK-002 context) is re-invoked ONCE with the flagged sentences quoted as what the section lacks — never as a phrase to insert, never with a count — and re-runs check_render itself; then a second fresh judge repeats the review (run 2), filed below run 1; the DRAFT is re-rendered to pdf and glyph-checked
- [ ] if every question reads 'yes' at run 1, no return cycle: say so
- [ ] the outcome states run-1 and run-2 counts per question with the sentences (e.g. 'Q4: 9 -> 3'), and the disposition — 'promotable on content' when the four read yes or every no has been answered in one cycle; otherwise 'not promotable on content', which does not stop TASK-004 (the owner reads whatever the pipeline produced in one cycle) but is recorded
- [ ] `git status --short pc_package/` still shows only the DRAFT and its renders

**Depends on:** [[TASK-002]]

## Documents it is about

- **PCR-007** — `pc_package/PCR-007_cex.qmd`

## Files it touched

- `.claude/work/2026-08-19_01_fourth-round-one-document/content-review-PCR-007-draft.md`
- `pc_package/PCR-007_cex.DRAFT.qmd`
