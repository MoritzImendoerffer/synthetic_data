---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-015
status: done
kind: document
title: "Author PCR-003 (Production Bioreactor (Step 3)) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-003", "PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-015 — Author PCR-003 (Production Bioreactor (Step 3)) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

118 annex quotes, 35 rhetorical spans to re-anchor later in this batch's annex task. PCR-003 is at an earlier round (round three / Track D / round two); re-done so the corpus has ONE register. BLOCKED: B2's release is undecided (the owner decided only the PCR-008 re-author on 2026-08-20). Unblock when the owner says so, or when TASK-043 settles and the owner is asked again. Released by the owner on 2026-08-20 (decisions.b2_released_2026_08_20), and authored under the amended rule 4 of WRITING_GUIDE.md.

## Acceptance criteria

- [x] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PCR-003, <uokey>=bioreactor, <outline>=report_doe: brief rebuilt fresh (`## 2b` 1, `## 5d` 0, §5c names D-002); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [x] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [x] `check_render.py pc_package/PCR-003_bioreactor.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `report_doe` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [x] the registered discrepancy D-002 is carried in substance by the draft (brief §5c assignment read against the text; ANNEX-A-BATCH §5), stated in the outcome
- [x] the content review (§4): run 1 filed as content-review-PCR-003.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [x] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

**Depends on:** [[TASK-045]]

## What was built

AUTHOR-A-DOCUMENT.md followed for PCR-003 / bioreactor / report_doe, under the amended rule 4. Brief rebuilt fresh (2b 1, 5d 0, §5c D-002). ONE agent (`opus`, fresh context; Opus 5 self-reported), §2 prompt verbatim. Audit over the full transcript, both turns (128 commands): suspect list EMPTY, other-qmd list EMPTY. check_render: hard gates passed on the first invocation and after the revision; docx OK, PDF no missing glyphs, no gated tic, no banned phrase, 0 <<NEEDS>>; numeral-lint FAIL is 20 advisory lines, all statistical conventions or identifiers. Size: 467 sentences / 10,269 words as authored, 453 / 10,005 after the cycle; 55 pages both times (band 41-56). D-002 CARRIED AND VERIFIED after the revision: the absolute claim stands verbatim and unqualified in §1.1, its authorized elaboration follows, nothing reconciles it later, and leached Protein A is never mentioned (grep 0). Neither judge flagged it. Content review (content-review-PCR-003.md), two fresh judges, ONE return: run 1 flagged Q1 20 / Q2 8 / Q3 11 / Q4 30 — the heaviest run-1 load of the campaign — verdicts No-No-No-Yes; run 2 flagged Q1 6 (+ a bookkeeping family) / Q2 0 / Q3 6 / Q4 7, verdicts No-YES-No-Yes. THE CYCLE CONVERGED, the third of three under the amended rule. A CONFLICT WAS RECORDED BEFORE THE RETURN WAS SENT: six of run 1's Q4 flags are content this project requires — WRITING_GUIDE rule 6 (say where a claim stops) and CLAUDE.md's framing rule (screening identifies, RSM predicts). The return was sent unfiltered because filtering it would be the session overruling the reviewer, and the author holds the guide. The author CONVERTED them to fact rather than deleting the content: the framing rule now reads as a statement of what each design produced, and scope limits survive as 'over the range studied' in six places. Verified in the rendered text. THE REVISION FOUND TWO SUBSTANTIVE ERRORS: the claim that pCO2 and culture pH sharing a sign is 'what a shared intracellular mechanism predicts' was FALSE (higher pCO2 lowers cytosolic pH while higher culture pH raises it, so a shared account predicts opposite signs); and 'Both are additive, which is what independent mechanisms give' was circular. The author also reports checking every new direction against the fitted coefficients and dropping one that would have had the wrong sign against the fitted -2.01, and revising eight unflagged sentences with the identical defect. Pre- and post-review drafts preserved. No style row, no frame count recorded.

## Documents it is about

- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- `pc_package/PCR-003_bioreactor.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCR-003.md`
