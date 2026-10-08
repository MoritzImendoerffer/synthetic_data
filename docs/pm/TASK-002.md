---
type: pm-task
epic: 2026-10-08_01_rev2-campaign
sprint: 2026-10-08_01_rev2-campaign
task: TASK-002
status: done
kind: model
title: "Record execution chronology and resolve the calibration-date tension"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
---

> [!warning] Generated from `.claude/work/2026-10-08_01_rev2-campaign/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-002 — Record execution chronology and resolve the calibration-date tension

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Acceptance criteria

- [x] config `campaign.studies` gives an execution window per study (incl. the AEX first execution and the CEX fraction study)
- [x] test: every study window ends before the cal_due of the equipment it used and before the Rev 1.0 effective date
- [x] outputs/data/study_chronology.csv generated

## What was built

config campaign: (revisions, INV-001, AMD-001 2026-03-20, 21 study windows). outputs/data/study_chronology.csv. tests/test_analytics.py::test_chronology_resolves_calibration_tension and ::test_method_decision_between_comparability_and_aex_repeat pass.

## Files it touched

- `config/parameters.yaml`
- `amab_process/deviations.py`
- `tests/test_config.py`
