---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-043
status: done
kind: measurement
title: "Blind reading: round-zero PCR-008 vs attempt 2 \u2014 HALT for the owner (D8)"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-043 — Blind reading: round-zero PCR-008 vs attempt 2 — HALT for the owner (D8)

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

HARD STOP.

## Acceptance criteria

- [x] A.pdf/B.pdf = $U/B1-old-PCR-008.pdf and the attempt-2 DRAFT pdf under blind-key-B1c.md, copied printing no key/size/page count; READING.md's two questions; recorded VERBATIM before the key is opened by checksum; the rule applied mechanically (attempt 2 preferred and fewer than five sentences quoted from it -> PASS)
- [x] D8's table gains the row; on PASS TASK-044 promotes attempt 2; on FAIL TASK-044 reverts PCR-008 to round-zero by name; either way B2's release is re-put to the owner if still undecided

**Depends on:** [[TASK-042]]

## What was built

A.pdf/B.pdf staged from B1-old-PCR-008.pdf (round zero) and the attempt-2 DRAFT pdf by a script that read blind-key-B1c.md and printed no key, no size and no page count, so the session stayed blind; committed as 6a493b4. The two files' embedded creation dates differed by seventeen days and were normalized to one timestamp before staging, title/author/page size already matching; document content untouched. READING.md's two questions put verbatim, with the owner told in advance that the comparison text is the round-zero report they had already read and preferred, and asked to say if they recognized it (they did not say). Reading recorded VERBATIM and committed with the key still sealed (16b7643), then the key opened and verified by first-pages text hash (A=6b4f149537c6=round zero, B=4a34d7808bed=attempt 2; byte hashes do not apply after the date normalization). Key: new = B. RULE APPLIED MECHANICALLY: new judged better = NO (the owner preferred A, the round-zero text, 'I like A better. The reasoning is better to understand and follow'); sentences quoted from the new document = 5, as 'hard to read' with 'some phrases in it that sound AI generated' — not fewer than five. Both legs fail. TASK-043 = FAIL. This answers what TASK-042 was set to test: attempt 1 was not a bad draw, and two attempts under the frozen regime have now lost to the round-zero text. Unlike the first reading it is diagnostic: both quoted passages are the scale-down model qualification paragraph, where round zero explains what the scaling convention buys ('This convention holds residence time and mass transport constant across scales') and attempt 2 lists what the model keeps without saying why that makes it a model. Finding for TASK-040: in a Materials and methods paragraph whose 'cause' is a convention rather than a species, the review questions' pressure to name a physical cause and to delete filing clauses removed the explanatory sentence and left an inventory, which the owner read as machine prose. D8's table has the row; the disposition per plan is TASK-044 reverting PCR-008 to round zero by name; B2's release is re-put to the owner and TASK-014/015/016 stay blocked.

## Documents it is about

- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/owner-reading-B1c-<date>.md`
- [[D8-do-the-batches-continue]] — `docs/pm/decisions/D8-do-the-batches-continue.md`
