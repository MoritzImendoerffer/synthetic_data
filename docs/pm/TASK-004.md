---
type: pm-task
epic: 2026-10-08_01_rev2-campaign
sprint: 2026-10-08_01_rev2-campaign
task: TASK-004
status: done
kind: model
title: "Hold-time stability and CEX fraction comparability datasets"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
---

> [!warning] Generated from `.claude/work/2026-10-08_01_rev2-campaign/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-004 — Hold-time stability and CEX fraction comparability datasets

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Acceptance criteria

- [x] outputs/data/hold_<pool>.csv for harvest, protein_a, viral_inactivation with n.t. cells as NaN
- [x] outputs/data/cex_fraction_comparability.csv with SEC and CE-SDS LMW per sample and sample type

**Depends on:** [[TASK-003]]

## What was built

hold_harvest/protein_a/viral_inactivation.csv (CE-SDS only at cesds_days, NaN otherwise) and cex_fraction_comparability.csv (20 rows, 9 sample types).

## Files it touched

- `amab_process/analytics.py`
- `config/parameters.yaml`
- `scripts/generate_data.py`
