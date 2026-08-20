---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-042
status: todo
kind: document
title: "Re-author PCR-008 (attempt 2) in one pass under the same regime, with one content-review cycle"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-042 — Re-author PCR-008 (attempt 2) in one pass under the same regime, with one content-review cycle

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

Attempt 1 (the currently promoted PCR-008) lost its blind reading to the round-zero text on 2026-08-20 — the only FAIL in five readings since the rebuild. Its review cycle was the heaviest of the batch (~30 filing clauses cut; run 1 of its review listed ~30 Q4 flags). Same regime, no new rule: whether attempt 1 was a bad draw is exactly what this tests. The comparison text for the reading is the ROUND-ZERO pdf ($U/B1-old-PCR-008.pdf), not attempt 1.

## Acceptance criteria

- [ ] procedures/AUTHOR-A-DOCUMENT.md followed for PCR-008 / aex / report_doe, exactly as TASK-008: brief rebuilt fresh (2b 1, 5d 0, §5c D-001), DRAFT instantiated, ONE fresh agent (`opus`) with the §2 prompt verbatim; a NEW blind key drawn to blind-key-B1c.md BEFORE the agent is launched
- [ ] transcript audit clean (no --review, no check_discourse, no measure_, no sentence listing, no other .qmd); check_render --render clean with glyphs; 0 <<NEEDS>>; D-001 carried (PAR table as it comes, no statement of where the other parameters were held, no reconciliation with PCP-008)
- [ ] content review: run 1 by a fresh judge on the draft PDF, ONE return to the same author if any question reads no, run 2 by a second fresh judge; filed as content-review-PCR-008-attempt2.md with run-1/run-2 counts
- [ ] outcome records model, passes, sizes, audit, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT and its renders

## Documents it is about

- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- `pc_package/PCR-008_aex.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCR-008-attempt2.md`
