---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-038
status: todo
kind: measurement
title: "Sampled blind reading of one document from batch B5 \u2014 HALT for the owner (D8)"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-038 — Sampled blind reading of one document from batch B5 — HALT for the owner (D8)

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

HARD STOP. The reading is of the promoted document, so a FAIL means a shipped document the owner rejects is in the corpus: record it, do not revert silently — the owner decides whether to re-author it or to revert to the old text by name.

## Acceptance criteria

- [ ] the owner names one document of the batch; its OLD pdf (saved in the annex task) and the promoted pdf copied to A.pdf/B.pdf under a key drawn then (secrets.choice), no key/size/page count printed; READING.md's sampled-reading text delivered
- [ ] the answer recorded VERBATIM before the key is opened by checksum; decisions.pass_rule applied mechanically; D8's table gains the batch's row (document, verdict, date)
- [ ] PASS releases the next batch; FAIL stops the unit: the next batch's document tasks are set blocked with the reason, and the owner decides in D8

**Depends on:** [[TASK-037]]

## Files it touched

- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/owner-reading-B5-<date>.md`
- [[D8-do-the-batches-continue]] — `docs/pm/decisions/D8-do-the-batches-continue.md`
