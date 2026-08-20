---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-049
status: done
kind: document
title: "Re-author PCR-004 (attempt 2) in one pass under the same regime, with one content-review cycle"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-004"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-049 — Re-author PCR-004 (attempt 2) in one pass under the same regime, with one content-review cycle

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

The owner preferred the pre-campaign text for this document (TASK-018 FAIL), and ranked it last of three on the same paragraph in the cross-document reading the same day. The comparison text for the reading stays the PRE-CAMPAIGN pdf ($U/B2-old-PCR-004.pdf). May run alongside B3. The regime is unchanged, so this tests the draw.

## Acceptance criteria

- [x] procedures/AUTHOR-A-DOCUMENT.md followed for PCR-004 / harvest / report_nondoe exactly as TASK-014: brief rebuilt fresh (2b 1, 5d 0, §5c None), DRAFT instantiated, ONE fresh agent (`opus`) with the §2 prompt verbatim; a NEW blind key drawn to blind-key-B2b-PCR-004.md BEFORE the agent is launched, with a random nonce so neither length nor checksum identifies the letter, and NO checksum printed
- [x] transcript audit clean; check_render --render clean with glyphs; 0 <<NEEDS>>; no DoE fabricated (the step has none) and every section of section_plan.yaml report_nondoe present in order
- [x] content review: run 1 by a fresh judge, ONE return to the same author if any question reads no, run 2 by a second fresh judge; filed with run-1/run-2 counts
- [x] outcome records model, passes, sizes, audit, review counts, and specifically what §6 now says about the absence of a design space — the paragraph the owner read

## What was built

PCR-004 attempt 2 / harvest / report_nondoe, regime UNCHANGED (attempt 1 was already written under the amended rule 4, so this tests the draw). Brief fresh (2b 1, 5d 0, §5c None). NEW key drawn to blind-key-B2b-PCR-004.md with a nonce BEFORE the agent was launched, no checksum printed. ONE agent (`opus`, Opus 5 self-reported). Audit clean over all three turns. All hard gates pass every turn; no missing glyphs, 0 <<NEEDS>>. 34 pages as authored, 33 after revision, against a non-DoE band of 26-28 (attempt 1 was 31). 355 sentences / 7,684 words as authored, 353 / 7,438 after. REVIEW: attempt 2 run 1 Q1 26 / Q2 5 / Q3 7 / Q4 25; run 2 Q1 5 (+7 methodological) / Q2 7 / Q3 6 / Q4 ~20. Against attempt 1: run 1 was 26/5/7/15 and run 2 was 4/0/0/8. THE TWO FIRST RUNS ARE IDENTICAL ON Q1, Q2 AND Q3 — two independent authors, same brief, same regime — so the first-draft profile is a property of the document, not a draw. THE TWO SECOND RUNS ARE NOT: attempt 1 converged to 4/0/0/8, attempt 2 did not converge and its Q2 went UP from 5 to 7. The revision is the high-variance step, not the authoring. CORRECTNESS RETURN (owner-authorised): typo, 'more'->'most', and a numerical error — a 25 % excursion against 4.0 % precision called 'an order of magnitude', now a grounded scalar rendering as 6. The author then found on its own that 'host cell protein carries the highest Tool #1 score' is false (aggregate 60, HCP 36, DNA 6) and said no gate would have caught it because the comparison was its own — the sentence that prompted docs/next/comparison-claims-unchecked.md. Spelling unified to 'disk'. TWO RENDERING DEFECTS found by looking at rendered pages, not extracted text: table column collision (en-dashes wider than pandoc assumes) and tabulate reparsing values into 6.56e+04. No shipped document carries the latter; the former cannot be grepped, so nothing gates layout.

## Documents it is about

- **PCR-004** — `pc_package/PCR-004_harvest.qmd`

## Files it touched

- `pc_package/PCR-004_harvest.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCR-004-attempt2.md`
