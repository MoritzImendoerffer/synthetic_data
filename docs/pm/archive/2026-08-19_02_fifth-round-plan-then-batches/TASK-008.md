---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-008
status: done
kind: document
title: "Author PCR-008 (Anion Exchange Chromatography (Step 8)) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-008", "PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-008 — Author PCR-008 (Anion Exchange Chromatography (Step 8)) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

83 annex quotes, 25 rhetorical spans to re-anchor later in this batch's annex task.

## Acceptance criteria

- [x] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PCR-008, <uokey>=aex, <outline>=report_doe: brief rebuilt fresh (`## 2b` 1, `## 5d` 0, §5c names D-001); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [x] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [x] `check_render.py pc_package/PCR-008_aex.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `report_doe` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [x] the registered discrepancy D-001 is carried in substance by the draft (brief §5c assignment read against the text; ANNEX-A-BATCH §5), stated in the outcome
- [x] the content review (§4): run 1 filed as content-review-PCR-008.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [x] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

**Depends on:** [[TASK-003]], [[TASK-005]]

## What was built

AUTHOR-A-DOCUMENT.md followed for PCR-008 / aex / report_doe; brief fresh (2b 1, 5d 0; §5c D-001 (first analysis never located; no reconciliation with PCP-008)). ONE agent (`opus`, fresh context; Opus 5 (self-reported)), prompt verbatim. Audit: Read RUNNER, section_plan, STORY_BIBLE, WRITING_GUIDE, REGISTER_EXEMPLAR, its own DRAFT; suspect list EMPTY; no other .qmd. check_render: 5 invocations, hard gates passed first; revision 3 pass(es) after the review return. Result: 54 pages (53 as authored), 449 sentences / 9,914 words, 35 chunks, 206 inline, 0 NEEDS, no missing glyph; every section of `report_doe` present in order; typed-measurement grep hits only statistical conventions / image widths. Registered discrepancy: D-001 (first analysis never located; no reconciliation with PCP-008). Content review (content-review-PCR-008.md): Q1 25 govern + most sets/acts -> 0 deferrals, ~10 relational + 3 empty connectives + 3 no-direction; Q2 10 -> 0; Q3 8 -> 0 (+1 borderline); Q4 ~30 -> 6 (+2). A substantive finding in the draft: the NOR box is not entirely inside the design space (99.6 %; the low-pH/high-conductivity corner predicts pool HCP 22.3 vs the in-process 21.7 ng/mg), reported adverse-first and carried into the control strategy. Not promotable on content by the checklist's letter after one cycle (Q4 residue and/or relational verbs); proceeds to the batch annex. Pre- and post-review drafts preserved in the unit. No style row, no frame count recorded.

## Documents it is about

- **PCP-008** — `pc_package/PCP-008_aex.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- `pc_package/PCR-008_aex.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCR-008.md`
