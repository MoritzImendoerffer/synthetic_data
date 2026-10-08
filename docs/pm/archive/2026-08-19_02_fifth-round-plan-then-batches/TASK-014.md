---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-014
status: done
kind: document
title: "Author PCR-004 (Harvest and Clarification (Step 4)) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-004", "PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-014 — Author PCR-004 (Harvest and Clarification (Step 4)) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

76 annex quotes, 36 rhetorical spans to re-anchor later in this batch's annex task. Non-DoE report (report_nondoe): no screening/RSM, no mechanistic subsection; do not fabricate a DoE. BLOCKED: B2's release is undecided (the owner decided only the PCR-008 re-author on 2026-08-20). Unblock when the owner says so, or when TASK-043 settles and the owner is asked again. Released by the owner on 2026-08-20 (decisions.b2_released_2026_08_20), and authored under the amended rule 4 of WRITING_GUIDE.md.

## Acceptance criteria

- [x] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PCR-004, <uokey>=harvest, <outline>=report_nondoe: brief rebuilt fresh (`## 2b` 1, `## 5d` 0, §5c None); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [x] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [x] `check_render.py pc_package/PCR-004_harvest.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `report_nondoe` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [x] no registered discrepancy for this document, stated
- [x] the content review (§4): run 1 filed as content-review-PCR-004.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [x] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

**Depends on:** [[TASK-045]]

## What was built

AUTHOR-A-DOCUMENT.md followed for PCR-004 / harvest / report_nondoe. FIRST document authored under the amended rule 4 of WRITING_GUIDE.md. Brief rebuilt fresh (2b 1, 5d 0, §5c None). ONE agent (`opus`, fresh context; Opus 5 self-reported), §2 prompt verbatim. Audit over the full transcript, both turns (40 commands): reads were RUNNER, section_plan.yaml, three outputs/figures PNGs and its own DRAFT, with the brief, WRITING_GUIDE, STORY_BIBLE and REGISTER_EXEMPLAR read by `cat`; suspect list EMPTY, other-qmd list EMPTY. check_render: hard gates passed on the first invocation and after the revision; docx OK, PDF no missing glyphs, no gated tic, no banned phrase, 0 <<NEEDS>>, typed-measurement grep hits only image widths. Structure matches report_nondoe: design space replaced by an operating-range statement, appendices without design matrices, all 15 sections in order. NO DoE fabricated (harvest has none); the step's one quantitative argument is the DEV-004-02 turbidity excursion, which bounds the depth filter load PAR to the NOR. Size: 318 sentences / 7,140 words as authored, 323 / 7,062 after the cycle; 31 pages both times, against a measured non-DoE band of 26-28 — flagged, not padded down. Content review (content-review-PCR-004.md), two fresh judges, ONE return: run 1 flagged Q1 26 / Q2 5 / Q3 7 / Q4 15, verdicts No-No-No-Yes; run 2 flagged Q1 4 (+2 borderline) / Q2 0 / Q3 0 / Q4 8, verdicts No-YES-YES-Yes. THE CYCLE CONVERGED, which PCR-008 attempt 2's did not (12/8/5/12 -> 16/9/9/14 there). The author separated documentary from physical causes itself rather than complying uniformly, and every 'governs/sets/acts on' used for a step-to-attribute register relation is gone, grep-verified at zero. Run 1 also made the reviewer's Q1 scope problem visible: 16 of its 26 Q1 flags were sentences stating that the step governs no CQA, which is most of what a non-DoE report of this step has to say. Recorded in D8 as open, not acted on. Two smaller notes from run 2, not acted on (one cycle only): the document spells 'disk-stack' in three places and 'disc stack' in one, and the residual Q4 flags are all the 'which is the X in §Y' cross-reference clause. Pre- and post-review drafts preserved in the unit. No style row, no frame count recorded.

## Documents it is about

- **PCR-004** — `pc_package/PCR-004_harvest.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- `pc_package/PCR-004_harvest.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCR-004.md`
