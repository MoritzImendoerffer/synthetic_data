---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-002
status: done
kind: document
title: "Author PCP-005 (Protein A Chromatography (Step 5)) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-005"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-002 — Author PCP-005 (Protein A Chromatography (Step 5)) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

48 annex quotes, 0 rhetorical spans to re-anchor later in this batch's annex task. THE PILOT of the plan genre: no rhetorical layer, plan_params not report_params, prospective voice. The first plan under the rebuilt apparatus.

## Acceptance criteria

- [x] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PCP-005, <uokey>=protein_a, <outline>=plan: brief rebuilt fresh (`## 2b` 1, `## 5d` 0, §5c None); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [x] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [x] `check_render.py pc_package/PCP-005_protein_a.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `plan` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [x] no registered discrepancy for this document, stated
- [x] the content review (§4): run 1 filed as content-review-PCP-005.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [x] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

**Depends on:** [[TASK-001]]

## What was built

AUTHOR-A-DOCUMENT.md followed for PCP-005 / protein_a / plan. ONE agent (`opus`, fresh context; self-reported Claude Opus 5 [1m]), prompt verbatim. Audit: Read of RUNNER.md and section_plan.yaml, `cat` of the brief, WRITING_GUIDE.md, STORY_BIBLE.md, REGISTER_EXEMPLAR.md, code for signatures; suspect list EMPTY (no --review, no check_discourse, no measure_, no listing, no rewrite script, no check_style at all); no other .qmd. check_render: 1 pass to clean (2 in total after the revision) — 11 chunks, 44 (then 42) inline expressions, no <<NEEDS>>, tic gate OK, docx renders, no missing glyph; numeral lint 10 advisory hits, all permitted conventions (p thresholds, coded levels −1/0/+1, 95 % CI, IgG1); typed-measurement grep: no prose hit. Every `plan` section present in order (Purpose and scope … Risks and assumptions, Approvals, Appendices A–B as unnumbered). No registered discrepancy (§5c 'None'). 31 pages; 259 sentences / 5,750 words as authored, 262 / 5,785 after the review cycle.

Content review (content-review-PCP-005.md): run 1 Q1 8 / Q2 4 / Q3 3 / Q4 9; ONE return to the same author (1 check_render pass); run 2 Q1 0 / Q2 0 / Q3 0 / Q4 5 — three of four clean, Q4 'the fault present' (five sentences, one inside mechanism prose). Not promotable on content by the letter; proceeds to the reading. Pre-review draft kept as PCP-005.DRAFT.pre-review.qmd/.pdf. Finding: 'carboxylate contacts' came from authoring/mechanism/protein_a.yaml via brief §2b — to be corrected at ship (regime frozen). `git status --short pc_package/` -> only the untracked DRAFT.qmd.

## Documents it is about

- **PCP-005** — `pc_package/PCP-005_protein_a.qmd`

## Files it touched

- `pc_package/PCP-005_protein_a.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCP-005.md`
