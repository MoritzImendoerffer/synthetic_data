---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-007
status: todo
kind: measurement
title: "Measure the pilot, take the owner's reading, and decide whether the remaining 16 run"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-007 — Measure the pilot, take the owner's reading, and decide whether the remaining 16 run

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-007.md. THIS IS THE DECISION POINT THE PILOT EXISTS FOR. The rule is fixed in decisions.pilot_stopping_rule below and no edge moves after the numbers are seen. If the pilot clears and the reading is acceptable, the remaining 16 run. If it does not, the round stops here and Track C -- rewriting the guide's own commentary -- becomes the candidate instead, having cost three documents rather than nineteen. PCR-003 IS THE CONTROL: it is already at the target register and this round does not touch it, so a measure that moves in the pilot and not in PCR-003 is the instruction rather than drift.

## Acceptance criteria

- [ ] measure_trackd.py run over the three pilot documents plus PCR-003 (the untouched control) and the four sources, one invocation, saved to measure_pilot.txt
- [ ] the pilot stopping rule below is applied line by line to each of the three, with a holds? column
- [ ] the project owner's reading of the three rendered pdfs is recorded VERBATIM and dated, and whatever it quotes is counted afterwards, in that order
- [ ] D3 is written as a decisions note with the numbers and both branches, and settled by the owner before any of TASK-008..TASK-028 starts

**Depends on:** [[TASK-006]]

## Documents it is about

- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `.claude/work/2026-08-18_02_register-track-d/measure_pilot.txt`
- [[D3-does-track-d-continue]] — `docs/pm/decisions/D3-does-track-d-continue.md`
