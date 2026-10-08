---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-047
status: done
kind: measurement
title: "Blind reading: round-zero PCR-008 vs attempt 3 \u2014 HALT for the owner (D8)"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-047 — Blind reading: round-zero PCR-008 vs attempt 3 — HALT for the owner (D8)

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

HARD STOP. Third reading of this document; the owner has preferred round zero twice.

## Acceptance criteria

- [x] A.pdf/B.pdf = $U/B1-old-PCR-008.pdf and the attempt-3 DRAFT pdf under blind-key-B1d.md, copied printing no key/size/page count, embedded dates normalized as in TASK-043
- [x] READING.md's two questions; recorded VERBATIM and committed before the key is opened; the rule applied mechanically
- [x] D8's table gains the row

**Depends on:** [[TASK-046]]

## What was built

PASS, 2026-08-20, recorded in owner-reading-B1d-2026-08-20.md and acted on by TASK-048, which promoted attempt 3. The status field was never moved off `pending` at the time, so the reading was missing from the campaign tally until 2026-08-21. Fourth blind reading of PCR-008 and the first it passed: the owner read §2.1 by their own choice, split at first ('I like the shorter sentences from A better but the logical structure of the paragraphs to each other is better in B'), and the deciding question — which of the two reads as a paper — was put and answered BEFORE the key was opened. Answer A. Key: new = A, verified by first-pages text hash. Both legs of the rule hold: new judged better = yes, sentences quoted from the new text = 0. The variable between attempt 2 (FAIL) and attempt 3 (PASS) was the amended rule 4 and nothing else — same procedure, same prompt, same review cycle, same comparison text, a fresh author each time.

## Documents it is about

- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/owner-reading-B1d-<date>.md`
- [[D8-do-the-batches-continue]] — `docs/pm/decisions/D8-do-the-batches-continue.md`
