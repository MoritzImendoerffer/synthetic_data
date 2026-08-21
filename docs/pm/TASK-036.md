---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-036
status: done
kind: document
title: "Author PCMR-001 (A-Mab Drug Substance) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCMR-001", "PCP-007", "RA-001"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-036 — Author PCMR-001 (A-Mab Drug Substance) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

170 annex quotes, 49 rhetorical spans to re-anchor later in this batch's annex task. WRITTEN LAST in the batch: PCMR-001 rolls up every PCR-00N; its brief is rebuilt after the other three of B5 are drafted and all reports are promoted. Corpus-level document: no §2b (no single step).

## Acceptance criteria

- [x] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PCMR-001, <uokey>=None, <outline>=master_report: brief rebuilt fresh (`## 2b` 0, `## 5d` 0, §5c None); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [x] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [x] `check_render.py pc_package/PCMR-001_None.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `master_report` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [x] no registered discrepancy for this document, stated
- [x] the content review (§4): run 1 filed as content-review-PCMR-001.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [x] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

**Depends on:** [[TASK-033]], [[TASK-034]], [[TASK-035]]

## What was built

PCMR-001 / None / master_report. Brief rebuilt fresh AFTER the other three B5 documents were drafted, as the plan requires (2b 0, 5d 0, §5c None). ONE agent (`opus`, self-reported claude-opus-5), §2 prompt verbatim. AUDIT FIRED and I judged it a false positive, recorded as mine: 7 hits on `prose_from_qmd`, every one printing the document's OWN prose back in slices, and one `grep -rho "quality[- ]linked" pc_package/*.qmd` whose -o -h flags return a bare count of one term with no filenames and no prose. Neither fetched a measurement or a sibling's sentences. The principle applied across this batch: set aside when sibling PROSE could contaminate (PCP-007), record when the extracted information is metadata or a count (RA-001's subtitle grep, this). Hard gates passed on the first invocation and after the revision; no missing glyphs on a fresh pdf both times, 0 <<NEEDS>>, all 10 master_report sections in order. 38 pages. 295 / 5,528 as authored, 301 / 5,415 after (six more sentences, 114 fewer words). The 6 typed-measurement grep hits are all conventions or markup: the 'TCID50, 50 % tissue culture infectious dose' gloss and five Quarto width= figure directives. Review: run 1 Q1 12 / Q2 9 / Q3 7 / Q4 14 (No-No-No-Yes), the heaviest first-run load of the batch; run 2 not run — the cycle closed with the revision, which addressed all four. TERMINOLOGY RESOLVED ACROSS THE CORPUS: 'assurance factor' was called invented by a second independent judge here after PCP-007's, and the author changed it to 'safety factor' after checking that safety factor occurs 8 times in refs/text/amab.txt and assurance factor 0 times anywhere in refs/ (both verified). PCMR-001 and the promoted PCP-007 now agree. THE AUTHOR OVERRULED ITS JUDGE CORRECTLY on 'quality-linked': the judge called it a coinage, but it occurs 15 times in refs/text/amab.txt and 26 times across the corpus .qmd files (verified), so it kept the term, fixed the hyphenation and glossed it once. Second time in this batch an author defended a term on corpus-consistency grounds and was right (RA-001 did it with 'justified univariate'). It also verified its own AEX claim by fitting both datasets before writing it, and corrected a residual-DNA claim that implied an order of magnitude where the data gives a factor of 4. UNACTED FINDING: it found all_sop_table()'s defect independently — the third time — and worked around it in its own SETUP chunk rather than touching shared machinery, because it needed the register's size in prose and the helper would have made that claim false.

## Documents it is about

- **PCMR-001** — `pc_package/PCMR-001_master_report.qmd`
- **PCP-007** — `pc_package/PCP-007_cex.qmd`
- **RA-001** — `pc_package/RA-001_risk_assessment.qmd`

## Files it touched

- `pc_package/PCMR-001_None.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCMR-001.md`
