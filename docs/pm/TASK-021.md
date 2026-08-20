---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-021
status: done
kind: document
title: "Author PCP-006 (Low-pH Viral Inactivation (Step 6)) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-006", "PCR-003", "PCR-004"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-021 — Author PCP-006 (Low-pH Viral Inactivation (Step 6)) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

44 annex quotes, 0 rhetorical spans to re-anchor later in this batch's annex task. Released by the owner on 2026-08-20 after the B2 reading split (PCR-003 PASS, PCR-004 FAIL). Authored under the amended rule 4.

## Acceptance criteria

- [x] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PCP-006, <uokey>=viral_inactivation, <outline>=plan: brief rebuilt fresh (`## 2b` 1, `## 5d` 0, §5c names D-001); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [x] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [x] `check_render.py pc_package/PCP-006_viral_inactivation.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `plan` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [x] the registered discrepancy D-001 is carried in substance by the draft (brief §5c assignment read against the text; ANNEX-A-BATCH §5), stated in the outcome
- [x] the content review (§4): run 1 filed as content-review-PCP-006.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [x] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

**Depends on:** [[TASK-018]]

## What was built

PCP-006 / viral_inactivation / plan. Brief fresh (2b 1, 5d 0, §5c D-001). ONE agent (`opus`), §2 prompt verbatim. Audit clean both turns. Hard gates passed on the first invocation and after the revision; no missing glyphs, 0 <<NEEDS>>. 29 pages. 239 / 5,622 as authored, 241 / 5,694 after. Review: run 1 Q1 7 / Q2 2 / Q3 3 / Q4 7 (No-No-No-Yes); run 2 Q1 4 / Q2 0 / Q3 1 / Q4 2 (No-YES-No-Yes). CONVERGED. D-001 carried and re-verified after the revision, unreconciled. Run 1's judge scoped Q1 unprompted. UNACTED FINDING: the Tool #1 definition the author added says 'a higher score is a higher criticality', which the register contradicts.

## Documents it is about

- **PCP-006** — `pc_package/PCP-006_viral_inactivation.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-004** — `pc_package/PCR-004_harvest.qmd`

## Files it touched

- `pc_package/PCP-006_viral_inactivation.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCP-006.md`
