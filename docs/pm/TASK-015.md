---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-015
status: todo
kind: document
title: "Author PCR-003 (Production Bioreactor (Step 3)) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-003", "PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-015 — Author PCR-003 (Production Bioreactor (Step 3)) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

118 annex quotes, 35 rhetorical spans to re-anchor later in this batch's annex task. PCR-003 is at an earlier round (round three / Track D / round two); re-done so the corpus has ONE register. BLOCKED: B2's release is undecided (the owner decided only the PCR-008 re-author on 2026-08-20). Unblock when the owner says so, or when TASK-043 settles and the owner is asked again. Released by the owner on 2026-08-20 (decisions.b2_released_2026_08_20), and authored under the amended rule 4 of WRITING_GUIDE.md.

## Acceptance criteria

- [ ] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PCR-003, <uokey>=bioreactor, <outline>=report_doe: brief rebuilt fresh (`## 2b` 1, `## 5d` 0, §5c names D-002); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [ ] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [ ] `check_render.py pc_package/PCR-003_bioreactor.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `report_doe` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [ ] the registered discrepancy D-002 is carried in substance by the draft (brief §5c assignment read against the text; ANNEX-A-BATCH §5), stated in the outcome
- [ ] the content review (§4): run 1 filed as content-review-PCR-003.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [ ] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

**Depends on:** [[TASK-045]]

## Documents it is about

- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- `pc_package/PCR-003_bioreactor.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCR-003.md`
