---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-046
status: done
kind: document
title: "Re-author PCR-008 (attempt 3) in one pass under the amended guide, with one content-review cycle"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-008", "PCR-004", "PCR-005", "PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-046 — Re-author PCR-008 (attempt 3) in one pass under the amended guide, with one content-review cycle

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Third attempt, and the first under the amended rule 4. The comparison text for the reading stays the ROUND-ZERO pdf ($U/B1-old-PCR-008.pdf). May run concurrently with B2's document tasks.

## Acceptance criteria

- [x] procedures/AUTHOR-A-DOCUMENT.md followed for PCR-008 / aex / report_doe exactly as TASK-042: brief rebuilt fresh (2b 1, 5d 0, §5c D-001), DRAFT instantiated, ONE fresh agent (`opus`) with the §2 prompt verbatim; a NEW blind key drawn to blind-key-B1d.md BEFORE the agent is launched
- [x] transcript audit clean; check_render --render clean with glyphs; 0 <<NEEDS>>; D-001 carried
- [x] content review: run 1 by a fresh judge, ONE return to the same author if any question reads no, run 2 by a second fresh judge; filed with run-1/run-2 counts
- [x] outcome records model, passes, sizes, audit, review counts, and specifically what the Materials and methods scale-down paragraph now says a convention buys

**Depends on:** [[TASK-045]]

## What was built

AUTHOR-A-DOCUMENT.md followed for PCR-008 / aex / report_doe, attempt 3, and the FIRST PCR-008 authored under the amended rule 4. Brief rebuilt fresh (2b 1, 5d 0, §5c D-001). NEW blind key drawn to blind-key-B1d.md BEFORE the agent was launched (md5 265df6a1d65d2d4ebe01461ae6547b4d, unopened). ONE agent (`opus`, fresh context; Opus 5 self-reported), §2 prompt verbatim. Audit over the full transcript, both turns (103 commands): suspect list EMPTY, other-qmd list EMPTY. check_render: hard gates passed on the FIRST invocation and after the revision; docx OK, PDF no missing glyphs, no gated tic, no banned phrase, 0 <<NEEDS>>; the numeral-lint FAIL is 15 advisory lines, all guidance names, abbreviation expansions, coded levels and alpha/CI conventions. D-001 carried and re-verified after the revision: par_table shown as it comes, 'PAR (set-point)' not renamed, the PAR prose says only that the other three parameters were 'held constant' without asserting where, and no reconciliation with PCP-008 anywhere in the section. Size: 485 sentences / 10,830 words at 56 pages as authored; 484 / 11,087 at 53 pages after the cycle. 'govern' is at ZERO in the rendered text and the 'X rather than Y' formula went from six to zero. THE REVISION FOUND A PHYSICS ERROR: the step-yield paragraph had put the recovery risk at a load pH low enough for the antibody to acquire a net negative charge, which is backwards; it now puts the risk edge at a high load pH approaching the isoelectric point. Content review (content-review-PCR-008-attempt3.md), two fresh judges, ONE return: run 1 flagged Q1 20 / Q2 8 / Q3 7 / Q4 17; run 2 flagged Q1 17 / Q2 4 / Q3 7 / Q4 12; verdicts No-No-No-Yes both times. It improved but converged far less than PCR-004 (26/5/7/15 -> 4/0/0/8) or PCR-005 (21/4/7/19 -> 3/3/2/6), which is now a property of this document across four independent authorings. Five of its nine residual procedural Q1 flags are the §9 classification rationales, and a well-controlled CPP is defined by control capability, so those cannot rest on physics without misstating the classification — the third document in the batch where the reviewer's questions flag mandated content. Pre- and post-review drafts preserved. No style row, no frame count recorded.

## Documents it is about

- **PCP-008** — `pc_package/PCP-008_aex.qmd`
- **PCR-004** — `pc_package/PCR-004_harvest.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- `pc_package/PCR-008_aex.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCR-008-attempt3.md`
