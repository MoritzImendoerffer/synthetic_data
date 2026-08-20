---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-045
status: done
kind: mechanism
title: "Put the causal-clause rule into the author-facing guide"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-045 — Put the causal-clause rule into the author-facing guide

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

The owner's amendment of the frozen regime, 2026-08-20. Everything authored from here carries it.

## Acceptance criteria

- [x] rule 4 says the cause stands in the clause where the causal verb stands, names the six verbs, and covers the case where the cause is a convention or a procedure rather than a species
- [x] no sentence is copied from any pc_package document into the guide (the guide-from-the-corpus loop)
- [x] no counter, no threshold and no obligation list reaches the author; REVIEW_CHECKLIST.md, RUNNER.md, section_plan.yaml, check_style.py and the launch prompt untouched
- [x] check_style.py --selftest still passes on all four human sources

## What was built

Rule 4 of WRITING_GUIDE.md rewritten and the §8 self-read line with it. Before: 'Name the physical cause when you give one', which is conditional and says nothing about where the cause stands. After: the cause stands in the clause where the causal verb stands, the six verbs are named, the cause may not sit in the next sentence or after a colon, and where what does the causing is a convention, a procedure or a design choice rather than a species the sentence says what it holds constant or what follows from it, because a list of what was done is not a reason and Materials and methods needs the reason as much as Results does. The round-zero sentence that occasioned this was deliberately NOT quoted into the guide: a guide distilled from a shipped document is how the register loop started once already. §8 now asks of each sentence that gives a reason whether the reason stands in the clause with its verb. check_style.py --selftest: 4 of 4 human sources measured and passing. No counter added anywhere.

## Files it touched

- [[WRITING_GUIDE]] — `authoring/WRITING_GUIDE.md`
