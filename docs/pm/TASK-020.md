---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-020
status: done
kind: document
title: "Author PCP-004 (Harvest and Clarification (Step 4)) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-004", "PCP-006", "PCP-010", "PCR-003", "PCR-004"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-020 — Author PCP-004 (Harvest and Clarification (Step 4)) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

36 annex quotes, 0 rhetorical spans to re-anchor later in this batch's annex task. Released by the owner on 2026-08-20 after the B2 reading split (PCR-003 PASS, PCR-004 FAIL). Authored under the amended rule 4.

## Acceptance criteria

- [x] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PCP-004, <uokey>=harvest, <outline>=plan: brief rebuilt fresh (`## 2b` 1, `## 5d` 0, §5c None); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [x] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [x] `check_render.py pc_package/PCP-004_harvest.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `plan` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [x] no registered discrepancy for this document, stated
- [x] the content review (§4): run 1 filed as content-review-PCP-004.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [x] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

**Depends on:** [[TASK-018]]

## What was built

PCP-004 / harvest / plan (NON-DoE). Brief fresh (2b 1, 5d 0, §5c None). ONE agent (`opus`, Opus 5 self-reported), §2 prompt verbatim. Audit clean over both turns. check_render hard gates passed on the FIRST invocation and after the revision; docx OK, no missing glyphs, 0 <<NEEDS>>, coined-compound rate fell to 0.0. 27 pages (plan band 23-31). 239 sentences / 5,306 words as authored, 236 / 5,483 after the cycle. Review: run 1 Q1 7 / Q2 3 / Q3 6 / Q4 10 (No-No-No-Yes); run 2 Q1 2 / Q2 1 / Q3 0 / Q4 2 (No-No-YES-Yes). CONVERGED. Fixed beyond register: the unsupported superlative in §12 (said 'least precise method in the set' against a table quoting two of four; now 'the less precise of the two methods quoted'), and disk-stack spelling unified to the SOP registry form. TWO UNACTED FINDINGS: the Tool #1 gloss it added is false against cqa_register.csv (viral clearance VH at 20 vs galactosylation H at 48), the same false inference PCP-006 and PCP-010 wrote independently; and a document-internal conflict where §5.4 draws the reference sample from 'the harvest vessel' while §4.1 defines that vessel as receiving the sterile-filtered filtrate. No DoE fabricated; no in-process limit invented (harvest has no ipc_limits entry).

## Documents it is about

- **PCP-004** — `pc_package/PCP-004_harvest.qmd`
- **PCP-006** — `pc_package/PCP-006_viral_inactivation.qmd`
- **PCP-010** — `pc_package/PCP-010_ufdf.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-004** — `pc_package/PCR-004_harvest.qmd`

## Files it touched

- `pc_package/PCP-004_harvest.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCP-004.md`
