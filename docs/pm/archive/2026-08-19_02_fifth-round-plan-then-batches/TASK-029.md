---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-029
status: done
kind: document
title: "Author PCP-007 (Cation Exchange Chromatography (Step 7)) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCP-006", "PCP-007", "PCP-008", "PCP-009", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-029 — Author PCP-007 (Cation Exchange Chromatography (Step 7)) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

49 annex quotes, 0 rhetorical spans to re-anchor later in this batch's annex task. PCP-007 is at an earlier round (round three / Track D / round two); re-done so the corpus has ONE register. Blocked on 2026-08-21 by D8's FAIL rule and RELEASED the same day by the owner, together with B5.

## Acceptance criteria

- [x] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PCP-007, <uokey>=cex, <outline>=plan: brief rebuilt fresh (`## 2b` 1, `## 5d` 0, §5c None); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [x] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [x] `check_render.py pc_package/PCP-007_cex.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `plan` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [x] no registered discrepancy for this document, stated
- [x] the content review (§4): run 1 filed as content-review-PCP-007.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [x] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

**Depends on:** [[TASK-026]]

## What was built

PCP-007 / cex / plan (DoE). Brief fresh (2b 1, 5d 0, §5c None — no registered discrepancy, stated). TWO authoring runs. RUN 1 WAS SET ASIDE: the mechanical audit lists were both empty (suspect [], other-qmd [], 33 commands) and the draft still failed the acceptance clause 'Reads of only the allowed inputs and code', because the author ran `cat authoring/DISCREPANCIES.md`, which is not a .qmd and carries no measurement keyword but quotes VERBATIM PROSE FROM FOUR SIBLING DOCUMENTS (PCP-006, PCP-008, PCP-009 in D-001; PCR-003 in D-002). The leak reached the text: the draft's §8.2 fused PCP-008's clause with PCP-009's grid clause. The author was sent there by an allowed input — §5c's own line 'The registry is authoring/DISCREPANCIES.md'. Evidence filed as PCP-007.DRAFT.run1-siblingleak.{qmd,pdf,md}; prompt NOT amended (regime frozen); fresh agent re-launched with the same prompt. RUN 2 (the document that stands): ONE agent (`opus`, self-reported claude-opus-5), §2 prompt verbatim, audit clean over both its turns (40 then 50 commands, DISCREPANCIES.md not read). Hard gates passed on the FIRST invocation and again after the revision; no missing glyphs on a pdf newer than the qmd both times, 0 <<NEEDS>>, 0 typed measurements. 29 pages as authored, 30 after. 255 / 5,942 as authored, 257 / 6,135 after. Review: run 1 Q1 13 / Q2 4 / Q3 4 / Q4 8 (No-No-No-Yes); run 2 Q1 12 / Q2 0 / Q3 0 / Q4 3 (No-YES-YES-Yes). Q2 AND Q3 both converged, as for PCP-003. Run 2's Q1 row is 1 mechanistic sentence plus 11 administrative/statistical uses, and the judge scoped the question itself, unprompted, saying 'If only mechanism-bearing clauses are counted, the answer is yes with that single exception'. NOT promotable on all four; proceeds to TASK-030. VERIFIED RATHER THAN TAKEN ON REPORT: the safety-factor values are inline expressions ({python} agg_marg / hcp_marg), and the claim that the design centre is the set-point for every CEX factor is true against plan_params('cex') (25 of 10-40, 5 of 3-7, 6.0 of 5.8-6.2, 1.0 of 0.5-1.5), so §5c 'None' holds and no unregistered inconsistency was created. UNACTED FINDINGS: the author changed 'assurance factor' to 'safety factor', diverging from the term config/parameters.yaml uses in its ipc_limits.margin comment (a one-word revert; PCP-008 already split the corpus on the neighbouring 'assurance margin'); 'OD desc.' as the stop-collect unit is a loose label inherited from the parameter table; one mechanism sentence still defers its direction to the next sentence and three trailing glosses survive.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCP-006** — `pc_package/PCP-006_viral_inactivation.qmd`
- **PCP-007** — `pc_package/PCP-007_cex.qmd`
- **PCP-008** — `pc_package/PCP-008_aex.qmd`
- **PCP-009** — `pc_package/PCP-009_virus_filtration.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `pc_package/PCP-007_cex.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCP-007.md`
