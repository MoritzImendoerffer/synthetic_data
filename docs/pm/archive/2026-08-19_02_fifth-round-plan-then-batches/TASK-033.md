---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-033
status: done
kind: document
title: "Author PTP-001 (A-Mab Drug Substance) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCMP-001", "PCMR-001", "PCP-010", "PTP-001"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-033 — Author PTP-001 (A-Mab Drug Substance) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

58 annex quotes, 0 rhetorical spans to re-anchor later in this batch's annex task. Corpus-level document: no §2b (no single step).

## Acceptance criteria

- [x] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PTP-001, <uokey>=None, <outline>=transfer_plan: brief rebuilt fresh (`## 2b` 0, `## 5d` 0, §5c None); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [x] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [x] `check_render.py pc_package/PTP-001_None.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `transfer_plan` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [x] no registered discrepancy for this document, stated
- [x] the content review (§4): run 1 filed as content-review-PTP-001.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [x] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

## What was built

PTP-001 / None / transfer_plan. Brief fresh (2b 0, 5d 0, §5c None — no registered discrepancy, stated). ONE agent (`opus`, self-reported claude-opus-5), §2 prompt verbatim. Audit clean on all three turns (38, 47, 52 commands; suspect [], other-qmd [], no sibling draft, DISCREPANCIES.md not read). Hard gates passed on the first invocation and after each pass; no missing glyphs on a pdf newer than the qmd every time, 0 <<NEEDS>>, 0 typed measurements, numeral lint fully OK (the first document of the batch to reach that). 26 pages throughout. 181 / 3,319 as authored, 187 / 3,526 after the cycle, 189 / 3,570 after the correctness pass. Review: run 1 Q1 5 / Q2 0 / Q3 2 / Q4 6 (No-YES-No-Yes); run 2 Q1 4 / Q2 0 / Q3 0 / Q4 0 (No-YES-YES-YES). QUESTION 4 PASSES — the first document in the entire campaign to do so; every earlier document in every batch answered yes. Three of four questions pass. Q2 passed on the FIRST run. `rather than` fell 15 -> 4, the construction the run-1 judge named as the carrier of five of its six Q4 hits. THE REVISION INTRODUCED TWO PHYSICS ERRORS, neither present in the pre-review draft (both checked): an oxygen/CO2 co-movement whose stated reason predicts the opposite sign, and a deamidation rate/extent conflation. Same failure mode as PCP-010's revision. THE OWNER AUTHORISED ONE MORE PASS for those two sentences only, overriding decisions.one_review_cycle for this document, on the PCP-010 precedent that a correctness matter is not a style preference. The author DECLINED TO ASSERT A DIRECTION IT COULD NOT ESTABLISH for oxygen and stated the opposite driving-force direction instead, and split rate from extent for deamidation. UNACTED FINDINGS: 'verification-qualified', the judge's only Q2 flag, is generated table content from outputs/data/dev_methods.csv (verified) rather than authored prose; four Q1 sentences survive, three of them called borderline by the judge. SEPARATE MECHANISM FINDING, verified and not fixed: all_sop_table() unions only globals ending in _SOP_REFS/_AMV_REFS, so it skips the base SOP_REFS and AMV_REFS and omits 10 SOPs (SOP-1001, SOP-1002, SOP-2003, SOP-2004, SOP-3010..3014, SOP-4001) and all 5 AMVs from the campaign-wide register its docstring calls 'every controlled document cited anywhere in the corpus'. Pre-existing; affects PTP-001, PCMP-001 and PCMR-001. A one-line fix, but a mechanism change and it moves three documents' rendered tables, so it is the owner's call.

## Documents it is about

- **PCMP-001** — `pc_package/PCMP-001_master_plan.qmd`
- **PCMR-001** — `pc_package/PCMR-001_master_report.qmd`
- **PCP-010** — `pc_package/PCP-010_ufdf.qmd`
- **PTP-001** — `pc_package/PTP-001_transfer.qmd`

## Files it touched

- `pc_package/PTP-001_None.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PTP-001.md`
