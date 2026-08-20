---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-016
status: done
kind: document
title: "Author PCR-005 (Protein A Chromatography (Step 5)) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCMR-001", "PCP-005", "PCR-004", "PCR-005", "PCR-007", "PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-016 — Author PCR-005 (Protein A Chromatography (Step 5)) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

97 annex quotes, 39 rhetorical spans to re-anchor later in this batch's annex task. PCR-005 is at an earlier round (round three / Track D / round two); re-done so the corpus has ONE register. BLOCKED: B2's release is undecided (the owner decided only the PCR-008 re-author on 2026-08-20). Unblock when the owner says so, or when TASK-043 settles and the owner is asked again. Released by the owner on 2026-08-20 (decisions.b2_released_2026_08_20), and authored under the amended rule 4 of WRITING_GUIDE.md.

## Acceptance criteria

- [x] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PCR-005, <uokey>=protein_a, <outline>=report_doe: brief rebuilt fresh (`## 2b` 1, `## 5d` 0, §5c None); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [x] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [x] `check_render.py pc_package/PCR-005_protein_a.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `report_doe` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [x] no registered discrepancy for this document, stated
- [x] the content review (§4): run 1 filed as content-review-PCR-005.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [x] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

**Depends on:** [[TASK-045]]

## What was built

AUTHOR-A-DOCUMENT.md followed for PCR-005 / protein_a / report_doe, under the amended rule 4. Brief rebuilt fresh (2b 1, 5d 0, §5c None). ONE agent (`opus`, fresh context; Opus 5 self-reported), §2 prompt verbatim. Audit over the full transcript, both turns (107 commands): suspect list EMPTY, other-qmd list EMPTY. check_render: hard gates passed on the first invocation and after the revision; docx OK, PDF no missing glyphs, no gated tic, no banned phrase, 0 <<NEEDS>>, numeral lint clean after revision. Size: 445 sentences / 9,922 words as authored, 453 / 10,022 after the cycle; 47 pages both times (band 41-56). D-001 does not apply: for protein_a the design centre coincides with the set-point for all four RSM factors and §3.5 says so. Content review (content-review-PCR-005.md), two fresh judges, ONE return: run 1 flagged Q1 21 (14 mechanism + 7 procedural) / Q2 4 / Q3 7 / Q4 19, verdicts No-No-No-Yes; run 2 flagged Q1 3 (+4 noted for completeness) / Q2 3 / Q3 2 / Q4 6, verdicts No-No-No-Yes. THE CYCLE CONVERGED, on every question, as PCR-004's did. THE REVISION ALSO FOUND TWO FACTUAL ERRORS no question asked about: §1.1 claimed the step removes more host cell protein and DNA than any other step of the train, which by fold contradicts PCR-007 (cation exchange 78-fold against roughly 55-fold here); and §13.2 called the leached Protein A ELISA the least precise method at this step, backwards against its own §3.3 (AMV-3016 6.5 % vs AMV-3012 9.5 %). Both corrected by the author in the same pass; both would have shipped. A substantive finding the document carries rather than smooths: the NOR corner at high protein load with low elution pH breaches the step's in-process host cell protein limit on the mean model (93.8 % of the NOR box meets it), so load and elution pH are treated as a jointly controlled pair in §6, §7, §9 and §10. Checked against PCP-005 and PCMR-001 for a conflicting 'NOR wholly inside the design space' claim; none found. Four `nan` cells remain in its ANOVA table, from doe_report.py's anova_lof_df, as in every DoE report in the corpus — recorded for a machinery proposal, not fixed. Pre- and post-review drafts preserved. No style row, no frame count recorded.

## Documents it is about

- **PCMR-001** — `pc_package/PCMR-001_master_report.qmd`
- **PCP-005** — `pc_package/PCP-005_protein_a.qmd`
- **PCR-004** — `pc_package/PCR-004_harvest.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`
- **PCR-007** — `pc_package/PCR-007_cex.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- `pc_package/PCR-005_protein_a.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCR-005.md`
