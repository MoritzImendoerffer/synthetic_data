---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-014
status: blocked
kind: document
title: "Author PCR-004 (Harvest and Clarification (Step 4)) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: another task
tags: [pm/task, pm/blocked]
about: ["PCR-004", "PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-014 — Author PCR-004 (Harvest and Clarification (Step 4)) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `blocked` · **Waiting on:** another task · **Board:** [[_Board]]

## Why it exists

76 annex quotes, 36 rhetorical spans to re-anchor later in this batch's annex task. Non-DoE report (report_nondoe): no screening/RSM, no mechanistic subsection; do not fabricate a DoE. BLOCKED by D8 B1 = FAIL (2026-08-20): the owner preferred the old PCR-008 in the sampled reading; the batches do not continue until D8 settles.

## Acceptance criteria

- [ ] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PCR-004, <uokey>=harvest, <outline>=report_nondoe: brief rebuilt fresh (`## 2b` 1, `## 5d` 0, §5c None); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [ ] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [ ] `check_render.py pc_package/PCR-004_harvest.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `report_nondoe` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [ ] no registered discrepancy for this document, stated
- [ ] the content review (§4): run 1 filed as content-review-PCR-004.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [ ] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

**Depends on:** [[TASK-012]]

## Documents it is about

- **PCR-004** — `pc_package/PCR-004_harvest.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- `pc_package/PCR-004_harvest.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCR-004.md`
