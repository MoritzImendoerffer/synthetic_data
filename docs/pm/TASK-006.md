---
type: pm-task
epic: 2026-10-08_01_rev2-campaign
sprint: 2026-10-08_01_rev2-campaign
task: TASK-006
status: done
kind: model
title: "Specification-driven IACs replace ipc_limits; Rev 1.0 criteria kept as data; integrated-model P(OOS)"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
---

> [!warning] Generated from `.claude/work/2026-10-08_01_rev2-campaign/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-006 — Specification-driven IACs replace ipc_limits; Rev 1.0 criteria kept as data; integrated-model P(OOS)

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Keep ipc_limit/effective_acceptance names as thin wrappers so Rev 1.0 helpers still import.

## Acceptance criteria

- [x] config `iac:` with platform worst-case clearance per step and attribute, each with a source comment; no `margin` key anywhere
- [x] outputs/data/iac.csv (step, attribute, DS criterion, worst-case downstream clearance, IAC, basis) and criteria_rev1.csv (the old computed limits)
- [x] test: perturbing every DoE response CSV leaves iac.csv unchanged
- [x] viral IACs equal the A-Mab platform claims and sum to >= the cumulative requirement
- [x] outputs/data/pos_integrated.csv: P(OOS) per DS attribute from the MC model
- [x] doe_report.clearance_verification(): observed min clearance over each step's PAR vs the worst case assumed

**Depends on:** [[TASK-003]], [[TASK-005]]

## What was built

config iac: (platform worst cases with sources, A-Mab viral claims 16.72/8.62 vs 16.7/8.6); ipc_limits renamed rev1_ipc_limits (data). amab_process/iac.py derive (config only), verification (edge-observed + NOR-predicted), final (tighten-only), rev1_criteria (reproduces CEX 193 ng/mg and 1 % HMW), p_oos. Verification: 8 met, CEX aggregate fold 1.505 < 2.0 -> VI pool aggregate IAC 10.0 -> 7.53, bioreactor 9.3 -> 6.83. doe_report reads iac.csv. tests/test_iac.py 7 pass; 127 total.

## Files it touched

- `config/parameters.yaml`
- `pc_package/doe_report.py`
- `scripts/generate_data.py`
- `tests/test_iac.py`
