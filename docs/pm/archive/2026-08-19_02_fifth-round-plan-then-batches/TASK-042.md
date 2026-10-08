---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-042
status: done
kind: document
title: "Re-author PCR-008 (attempt 2) in one pass under the same regime, with one content-review cycle"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-008", "PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-042 — Re-author PCR-008 (attempt 2) in one pass under the same regime, with one content-review cycle

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Attempt 1 (the currently promoted PCR-008) lost its blind reading to the round-zero text on 2026-08-20 — the only FAIL in five readings since the rebuild. Its review cycle was the heaviest of the batch (~30 filing clauses cut; run 1 of its review listed ~30 Q4 flags). Same regime, no new rule: whether attempt 1 was a bad draw is exactly what this tests. The comparison text for the reading is the ROUND-ZERO pdf ($U/B1-old-PCR-008.pdf), not attempt 1.

## Acceptance criteria

- [x] procedures/AUTHOR-A-DOCUMENT.md followed for PCR-008 / aex / report_doe, exactly as TASK-008: brief rebuilt fresh (2b 1, 5d 0, §5c D-001), DRAFT instantiated, ONE fresh agent (`opus`) with the §2 prompt verbatim; a NEW blind key drawn to blind-key-B1c.md BEFORE the agent is launched
- [x] transcript audit clean (no --review, no check_discourse, no measure_, no sentence listing, no other .qmd); check_render --render clean with glyphs; 0 <<NEEDS>>; D-001 carried (PAR table as it comes, no statement of where the other parameters were held, no reconciliation with PCP-008)
- [x] content review: run 1 by a fresh judge on the draft PDF, ONE return to the same author if any question reads no, run 2 by a second fresh judge; filed as content-review-PCR-008-attempt2.md with run-1/run-2 counts
- [x] outcome records model, passes, sizes, audit, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT and its renders

## What was built

AUTHOR-A-DOCUMENT.md followed for PCR-008 / aex / report_doe, as TASK-008; attempt 2, fresh session, same frozen regime, nothing added to the prompt. Brief rebuilt fresh (2b 1, 5d 0; §5c D-001). New blind key drawn to blind-key-B1c.md BEFORE the agent existed (8 bytes, md5 7c40abbf77c8519448f89e0013a63a90, unopened; this session never opened the shipped PCR-008_aex.qmd). ONE agent (`opus`, fresh context; Opus 5 self-reported), §2 prompt verbatim. Audit over the FULL transcript, both turns (59 commands): reads were RUNNER, out/PCR-008.brief.md, section_plan.yaml, STORY_BIBLE, WRITING_GUIDE, REGISTER_EXEMPLAR, _pcpkg.py, doe_report.py and its own DRAFT; suspect list EMPTY, other-qmd list EMPTY. check_render: hard gates passed on the first invocation as authored and again after the review revision; docx render OK, PDF no missing glyphs, gated tics all 0.0/1k words, 0 <<NEEDS>>, typed-measurement grep 0 hits (the one advisory numeral line is `ICH Q5A(R2)`, a guidance identifier). Every section of `report_doe` present in order. Size: 437 sentences / 8,789 words as authored, 446 / 8,981 after the cycle; 48 pages either way (band 41-56). Registered discrepancy D-001 carried and re-verified after the revision: D.par_table(UO) shown as it comes, 'PAR (set-point)' not renamed, nothing said about where the other parameters were held, no reconciliation with PCP-008 in the PAR section. Content review (content-review-PCR-008-attempt2.md), two fresh judges, ONE return in between: run 1 flagged Q1 12 / Q2 8 / Q3 5 / Q4 12, verdicts No-No-No-Yes; run 2, after the cycle, flagged Q1 16 / Q2 9 / Q3 9 / Q4 14, verdicts No-No-No-Yes. The cycle did not converge and the second judge flagged MORE in every question, partly on a formula the revision itself introduced ('act on one equilibrium from opposite sides', repeated in three sections). Run 2 also states that Q1 has no exemption for procedural or statistical 'because' and flags eight correct sentences under it. Two substantive points recorded, not patched (nothing is added to a finished document; one cycle only): §1.1 'The step sets the cumulative clearance of minute virus of mice' against viral_clearance.csv, where AEX supplies 4.71 of the 10.03 log10 cumulative MVM (the same paragraph two sentences later says the step 'does not carry the whole claim for either model virus'); and the §5.4 'below its isoelectric point' phrasing, which was present in attempt 1 and which attempt 1's judge cited as PASSING Q1. Neither is in DISCREPANCIES.md. Pre-review draft preserved as PCR-008-attempt2.DRAFT.pre-review.{qmd,pdf}; attempt 1's artifacts untouched. `git status --short pc_package/` shows only the untracked DRAFT (its .docx/.pdf are ignored). No style row, no frame count recorded.

## Documents it is about

- **PCP-008** — `pc_package/PCP-008_aex.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- `pc_package/PCR-008_aex.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCR-008-attempt2.md`
