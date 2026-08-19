---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-007
status: done
kind: document
title: "Author PCR-006 (Low-pH Viral Inactivation (Step 6)) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-006", "PCR-006"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-007 — Author PCR-006 (Low-pH Viral Inactivation (Step 6)) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

82 annex quotes, 31 rhetorical spans to re-anchor later in this batch's annex task.

## Acceptance criteria

- [x] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PCR-006, <uokey>=viral_inactivation, <outline>=report_doe: brief rebuilt fresh (`## 2b` 1, `## 5d` 0, §5c names D-001); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [x] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [x] `check_render.py pc_package/PCR-006_viral_inactivation.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `report_doe` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [x] the registered discrepancy D-001 is carried in substance by the draft (brief §5c assignment read against the text; ANNEX-A-BATCH §5), stated in the outcome
- [x] the content review (§4): run 1 filed as content-review-PCR-006.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [x] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

**Depends on:** [[TASK-003]], [[TASK-005]]

## What was built

AUTHOR-A-DOCUMENT.md followed for PCR-006 / viral_inactivation / report_doe; brief fresh (2b 1, 5d 0; §5c D-001 ('at fixed settings'; no reconciliation with PCP-006)). ONE agent (`opus`, fresh context; Opus 5 (self-reported)), prompt verbatim. Audit: Read RUNNER.md, section_plan.yaml; cat of the brief/guide/bible/exemplar; read check_style.py source for BANNED; two scratchpad test qmd (caption test) — allowed; suspect list EMPTY. check_render: 6 invocations, 0 hard failures; revision 1 pass(es) after the review return. Result: 45 pages (46 as authored), 413 sentences / 8,617 words (408 / 8,667), 35 chunks, 161 inline, 0 NEEDS, no missing glyph; every section of `report_doe` present in order; typed-measurement grep hits only statistical conventions / image widths. Registered discrepancy: D-001 ('at fixed settings'; no reconciliation with PCP-006). Content review (content-review-PCR-006.md): Q1 ~15+10 -> 3 (mild: 'the level the production bioreactor sets'); Q2 5 -> 2 (identity-controlled/quality-controlled from section_plan.yaml's note; assurance margin from doe_report's docstring); Q3 6 -> 0; Q4 11+ -> 3–4. Judge also found a mechanism error in the executive summary (charge variants assigned to unfolding; §1.1/§5.4 say acid-catalysed reactions) — recorded, one cycle spent. Not promotable on content by the checklist's letter after one cycle (Q4 residue and/or relational verbs); proceeds to the batch annex. Pre- and post-review drafts preserved in the unit. No style row, no frame count recorded.

## Documents it is about

- **PCP-006** — `pc_package/PCP-006_viral_inactivation.qmd`
- **PCR-006** — `pc_package/PCR-006_viral_inactivation.qmd`

## Files it touched

- `pc_package/PCR-006_viral_inactivation.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCR-006.md`
