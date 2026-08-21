---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-038
status: todo
kind: measurement
title: "Sampled blind reading of one document from batch B5 \u2014 measurement, not a gate (D8)"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-038 — Sampled blind reading of one document from batch B5 — measurement, not a gate (D8)

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

Not a hard stop. The reading still runs exactly as READING.md specifies — blind, key drawn and sealed before staging, the answer recorded verbatim and committed before the key is opened, the rule applied mechanically — because a reading that cannot fail measures nothing. What changed on 2026-08-21 is only the consequence: the owner is happy with the documents, keeps every promoted one, and released both remaining batches, so the verdict feeds the results page instead of the schedule. The reading is of the promoted document, so a FAIL still means a shipped document the owner reads as the weaker text: record it plainly, never revert silently.

## Acceptance criteria

- [ ] the owner names one document of the batch; its OLD pdf (saved in the annex task) and the promoted pdf copied to A.pdf/B.pdf under a key drawn then (secrets.choice), no key/size/page count printed; READING.md's sampled-reading text delivered
- [ ] the answer recorded VERBATIM before the key is opened by checksum; decisions.pass_rule applied mechanically; D8's table gains the batch's row (document, verdict, date)
- [ ] the verdict is RECORDED and carried to the results page; it releases nothing and blocks nothing. Owner's decision of 2026-08-21: B4 and B5 are both released in advance and every promoted document stays, so a FAIL is a finding about the pipeline and not a disposition of the corpus. If a FAIL names a defect in a specific document, put it to the owner as a question rather than acting on it.

**Depends on:** [[TASK-037]]

## Files it touched

- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/owner-reading-B5-<date>.md`
- [[D8-do-the-batches-continue]] — `docs/pm/decisions/D8-do-the-batches-continue.md`
