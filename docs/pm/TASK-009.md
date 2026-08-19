---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-009
status: doing
kind: document
title: "Author PCR-009 (Small-Virus Retentive Filtration (Step 9)) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/doing]
about: ["PCR-009"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-009 — Author PCR-009 (Small-Virus Retentive Filtration (Step 9)) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `doing` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

70 annex quotes, 37 rhetorical spans to re-anchor later in this batch's annex task.

## Acceptance criteria

- [ ] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PCR-009, <uokey>=virus_filtration, <outline>=report_doe: brief rebuilt fresh (`## 2b` 1, `## 5d` 0, §5c names D-001); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [ ] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [ ] `check_render.py pc_package/PCR-009_virus_filtration.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `report_doe` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [ ] the registered discrepancy D-001 is carried in substance by the draft (brief §5c assignment read against the text; ANNEX-A-BATCH §5), stated in the outcome
- [ ] the content review (§4): run 1 filed as content-review-PCR-009.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [ ] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

**Depends on:** [[TASK-003]], [[TASK-005]]

## What was built

IN PROGRESS 2026-08-19: brief rebuilt (2b 1, 5d 0), scaffold instantiated, ONE agent (`opus`, fresh context) launched with the AUTHOR-A-DOCUMENT §2 prompt verbatim; four B1 authors run concurrently. Audit, checks and the review cycle follow when it reports.

## Documents it is about

- **PCR-009** — `pc_package/PCR-009_virus_filtration.qmd`

## Files it touched

- `pc_package/PCR-009_virus_filtration.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCR-009.md`
