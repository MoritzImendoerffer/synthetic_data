---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-010
status: done
kind: document
title: "Author PCR-010 (Ultrafiltration / Diafiltration (Step 10)) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-010"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-010 — Author PCR-010 (Ultrafiltration / Diafiltration (Step 10)) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

68 annex quotes, 30 rhetorical spans to re-anchor later in this batch's annex task. Non-DoE report (report_nondoe): no screening/RSM, no mechanistic subsection; do not fabricate a DoE.

## Acceptance criteria

- [x] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PCR-010, <uokey>=ufdf, <outline>=report_nondoe: brief rebuilt fresh (`## 2b` 1, `## 5d` 0, §5c None); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [x] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [x] `check_render.py pc_package/PCR-010_ufdf.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `report_nondoe` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [x] no registered discrepancy for this document, stated
- [x] the content review (§4): run 1 filed as content-review-PCR-010.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [x] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

**Depends on:** [[TASK-003]], [[TASK-005]]

## What was built

AUTHOR-A-DOCUMENT.md followed for PCR-010 / ufdf / report_nondoe; brief fresh (2b 1, 5d 0; §5c none). ONE agent (`opus`, fresh context; Opus 5 (self-reported)), prompt verbatim. Audit: Read RUNNER, section_plan, two figure PNGs; scratchpad test qmd ×2 (lint/abbrev tests) — allowed; suspect list EMPTY. check_render: 3 invocations, hard gates passed first; revision 1 pass(es) after the review return. Result: 30 pages, 289 sentences / 6,005 words (304 / 6,116), 11 chunks, 85 inline, 0 NEEDS, no missing glyph; every section of `report_nondoe` present in order; typed-measurement grep hits only statistical conventions / image widths. Registered discrepancy: none. Content review (content-review-PCR-010.md): Q1 16 documentary + 7 no-direction -> 5 mechanism-context deferrals + 11 registry; Q2 clean -> clean; Q3 9 -> 7; Q4 19 -> 13. Non-DoE handled as non-DoE (no design space claimed; PARs = the ranges studied, bounded three ways). Author found and fixed a rendered em-dash leaking from a CQA name ('Viral clearance — MVM') that the source-level tic gate cannot see; judge noted a tension §1.1 'What the step can do to the product is mechanical' vs §2.2 deamidation. Not promotable on content by the checklist's letter after one cycle (Q4 residue and/or relational verbs); proceeds to the batch annex. Pre- and post-review drafts preserved in the unit. No style row, no frame count recorded.

## Documents it is about

- **PCR-010** — `pc_package/PCR-010_ufdf.qmd`

## Files it touched

- `pc_package/PCR-010_ufdf.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCR-010.md`
