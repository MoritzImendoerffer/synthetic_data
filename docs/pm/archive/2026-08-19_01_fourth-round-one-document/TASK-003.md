---
type: pm-task
epic: 2026-08-19_01_fourth-round-one-document
sprint: 2026-08-19_01_fourth-round-one-document
task: TASK-003
status: done
kind: measurement
title: "Content review before the reading: the four questions on the draft, at most one return to the author"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-007"]
---

> [!warning] Generated from `.claude/work/2026-08-19_01_fourth-round-one-document/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-003 — Content review before the reading: the four questions on the draft, at most one return to the author

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

This is the pipeline's own review step, and it is what the reading judges. One cycle only: the calibration (predecessor, content-review-calibration.md) showed the judge is stricter than the owner and consistent, so a second cycle would be tuning the draft to the judge. The judge must not have read the guide, any counter, or the shipped PCR-007. Keep the run-1 draft (`cp` to $U/PCR-007_cex.DRAFT.run1.qmd) so the results page can say what one cycle changed.

## Acceptance criteria

- [x] a fresh-context agent (model recorded), given exactly the prompt of ../2026-08-18_03_author-facing-apparatus/procedures/REVIEW-BEFORE-PROMOTION.md and the DRAFT's PDF and nothing else, reports the flagged sentences per question, verbatim, and the four yes/no answers; filed as content-review-PCR-007-draft.md (run 1)
- [x] if any question reads 'no': the SAME authoring agent (the TASK-002 context) is re-invoked ONCE with the flagged sentences quoted as what the section lacks — never as a phrase to insert, never with a count — and re-runs check_render itself; then a second fresh judge repeats the review (run 2), filed below run 1; the DRAFT is re-rendered to pdf and glyph-checked
- [x] if every question reads 'yes' at run 1, no return cycle: say so
- [x] the outcome states run-1 and run-2 counts per question with the sentences (e.g. 'Q4: 9 -> 3'), and the disposition — 'promotable on content' when the four read yes or every no has been answered in one cycle; otherwise 'not promotable on content', which does not stop TASK-004 (the owner reads whatever the pipeline produced in one cycle) but is recorded
- [x] `git status --short pc_package/` still shows only the DRAFT and its renders

**Depends on:** [[TASK-002]]

## What was built

Run 1 (fresh judge, self-reported Opus 5, given the four questions and the run-2 draft PDF, nothing else): Q1 No, Q2 No, Q3 No, Q4 Yes — ~15 mechanism-shaped Q1 flags plus 'governs' in four incompatible senses; 10 coinages (handle, binding attribute, buys back, break-even point, assurance factor, a plane with twist, the two mechanisms, impurity load, instrument, aggregate front, governed attribute); 14 Q3 back-references mostly in §5.4 and §11; ~24 Q4 filing clauses plus a four-times 'n bounds apply' frame. Filed in content-review-PCR-007-draft.md with every sentence.

ONE return to the SAME authoring agent (its own context), the flagged sentences quoted as what each lacks, no count, no phrase to insert. The author revised once: 3 check_render passes, 50 pages, 482 sentences / 10,702 words (from 493 / 10,730), every named sentence changed and two referential fixes the rewrites forced; §5.4 rewritten end to end; the coinages replaced by terms of art (assurance factor -> safety factor ×6, governed attribute -> attributes this step clears ×12, …); the four frames deleted; the legitimate §13.2 gloss kept. Pre- and post-review drafts preserved in the unit.

Run 2 (second fresh judge, self-reported Opus 5, quotes machine-verified against the PDF): Q1 No (7 mechanism-shaped flags remain — the executive summary's 'acted on … in opposite directions', two flow-rate sentences with a channel but no direction, three circular/evidentiary because-clauses, 'the assay sets the limit' — plus 17 documentary/statistical/control-system uses the judge listed on the literal test and called substantively sound); Q2 No (4 new coinages: identity-controlled/quality-controlled, verification-qualified, quality-linked parameters, instrumented decision; 2 weak) — none of run 1's remain; Q3 No narrowly (1 clear: 'That result holds only over the characterized ranges.', 2 borderline; 'all 22 other sentences of §5.4 make directional, species-named claims'); Q4 Yes (11, from ~24; the strongest §9's 'which is the criterion that separates a well-controlled critical process parameter from a critical one').

Disposition: NOT promotable on content by the checklist's letter after one cycle; the reading proceeds on the one-cycle output as the plan says. No second cycle (it would tune the draft to the judge). `git status --short pc_package/` -> only the untracked DRAFT.qmd.

## Documents it is about

- **PCR-007** — `pc_package/PCR-007_cex.qmd`

## Files it touched

- `.claude/work/2026-08-19_01_fourth-round-one-document/content-review-PCR-007-draft.md`
- `pc_package/PCR-007_cex.DRAFT.qmd`
