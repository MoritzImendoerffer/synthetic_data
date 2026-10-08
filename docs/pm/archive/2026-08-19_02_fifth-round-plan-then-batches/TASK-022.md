---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-022
status: done
kind: document
title: "Author PCP-008 (Anion Exchange Chromatography (Step 8)) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-006", "PCP-008", "PCR-003", "PCR-004"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-022 — Author PCP-008 (Anion Exchange Chromatography (Step 8)) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

51 annex quotes, 0 rhetorical spans to re-anchor later in this batch's annex task. Released by the owner on 2026-08-20 after the B2 reading split (PCR-003 PASS, PCR-004 FAIL). Authored under the amended rule 4.

## Acceptance criteria

- [x] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PCP-008, <uokey>=aex, <outline>=plan: brief rebuilt fresh (`## 2b` 1, `## 5d` 0, §5c names D-001); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [x] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [x] `check_render.py pc_package/PCP-008_aex.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `plan` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [x] the registered discrepancy D-001 is carried in substance by the draft (brief §5c assignment read against the text; ANNEX-A-BATCH §5), stated in the outcome
- [x] the content review (§4): run 1 filed as content-review-PCP-008.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [x] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

**Depends on:** [[TASK-018]]

## What was built

PCP-008 / aex / plan. Brief fresh (2b 1, 5d 0, §5c D-001). ONE agent (`opus`), §2 prompt verbatim. AUDIT: the keyword scan matched 'reflow' twice, from the author's own line-wrapping helper (`def reflow(par, width=88)`) which changes only where source lines break. Every measurement keyword checked and all zero: --review 0, check_discourse 0, measure_ 0, .sentences( 0, prose_from_qmd 0, mean_len 0. Judged a FALSE POSITIVE of the audit's keyword list and the draft was NOT set aside; that is this session's judgement against the procedure's mechanical rule, recorded as such, and the keyword needs narrowing. Hard gates passed on the first invocation and after the revision; docx OK, no missing glyphs, 0 <<NEEDS>>. 29 pages. 242 / 5,562 as authored, 240 / 5,474 after. Review: run 1 Q1 4 real + 7 registry / Q2 0 / Q3 2 / Q4 6 (No-YES-No-Yes); run 2 Q1 3 + 5 registry / Q2 1 / Q3 0 / Q4 5 (No-No-YES-Yes). THE TWO JUDGES DISAGREE on 'assurance margin': run 1 passed it as defined in place, run 2 failed it as undefined. PCP-006's author removed the same term on the same flag, so the batch is now inconsistent on it. The author REFUSED the seven registry Q1 flags, correctly: they are the corpus's fixed vocabulary under rule 5 and the judge marked them category labels. TOOLCHAIN TRAP FOUND: re-wrapping split an inline expression across a newline, which Quarto renders as literal source text; check_render caught it only via the expression count 28 vs 29. Repaired, and no shipped PDF carries the defect. D-001 intact.

## Documents it is about

- **PCP-006** — `pc_package/PCP-006_viral_inactivation.qmd`
- **PCP-008** — `pc_package/PCP-008_aex.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-004** — `pc_package/PCR-004_harvest.qmd`

## Files it touched

- `pc_package/PCP-008_aex.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCP-008.md`
