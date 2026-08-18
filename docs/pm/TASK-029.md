---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-029
status: todo
kind: measurement
title: "Measure the whole corpus by one method, apply the stopping rule, record the reading"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-029 — Measure the whole corpus by one method, apply the stopping rule, record the reading

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-029.md. ONE METHOD FOR ALL 20 DOCUMENTS, from TASK-002's script and nothing else. NO CONTROL COLUMN EXCEPT PCR-003 AND THE FOUR SOURCES -- if all 19 move together, say so; a corpus that drifts together is not the same evidence as a document that moves against a control.

## Acceptance criteria

- [ ] measure_trackd.py run ONCE over all 20 committed .qmd, saved in the unit; every cell on the page traces to that file, verified by script over every table row
- [ ] the corpus stopping rule in decisions.corpus_stopping_rule is applied per document, all 19, with a holds? column and the verdict naming the line that decided it
- [ ] the page carries the before/after table per document with denominators, the four source columns, and PCR-003 as the untouched control
- [ ] the three regressions round three found unprinted -- ', which', the staccato and 'its' -- are measured across all 19 and reported whether or not they were targeted
- [ ] docs/results/README.md gains a row

**Depends on:** [[TASK-028]]

## Documents it is about

- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- [[2026-08-XX-register-track-d]] — `docs/results/2026-08-XX-register-track-d.md`
- [[README]] — `docs/results/README.md`
