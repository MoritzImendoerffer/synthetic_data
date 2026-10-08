---
type: pm-task
epic: 2026-10-08_01_rev2-campaign
sprint: 2026-10-08_01_rev2-campaign
task: TASK-010
status: done
kind: measurement
title: "Rebuild data and figures; old documents still ground"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
---

> [!warning] Generated from `.claude/work/2026-10-08_01_rev2-campaign/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-010 — Rebuild data and figures; old documents still ground

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Acceptance criteria

- [x] make clean && make data figures succeeds
- [x] the 20 committed Rev 1.0 docx still ground against their annexes (they are not re-rendered)
- [x] pytest passes

**Depends on:** [[TASK-003]], [[TASK-004]], [[TASK-005]], [[TASK-006]]

## What was built

make data figures OK (only fig_capability.png changed); pytest 131 passed; Rev 1.0 docx untouched; grounding 2089/2089.

## Files it touched

- `outputs/`
