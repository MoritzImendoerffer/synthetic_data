---
type: pm-task
epic: 2026-10-08_01_rev2-campaign
sprint: 2026-10-08_01_rev2-campaign
task: TASK-005
status: done
kind: model
title: "Two-sided capability for acidic variants"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
---

> [!warning] Generated from `.claude/work/2026-10-08_01_rev2-campaign/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-005 — Two-sided capability for acidic variants

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Moves the headline min Cpk (1.51 -> ~1.03 per the old proposal). Report both numbers in the results page.

## Acceptance criteria

- [x] capability.csv acidic_variants spec_type two_sided; min Cpk before and after printed with its CQA

**Depends on:** [[TASK-003]]

## What was built

acidic_variants two-sided. min Cpk 1.51 (lrv_mvm) -> 1.03 (acidic_variants, Cpl against the 18 % floor). test_capability_all_pass restated around the finding.

## Files it touched

- `amab_process/studies.py`
- `tests/test_process.py`
