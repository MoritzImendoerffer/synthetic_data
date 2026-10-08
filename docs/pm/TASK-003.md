---
type: pm-task
epic: 2026-10-08_01_rev2-campaign
sprint: 2026-10-08_01_rev2-campaign
task: TASK-003
status: done
kind: model
title: "Analytical model: fragments (LMW), per-study method assignment, SEC matrix bias, all on independent RNG streams"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
---

> [!warning] Generated from `.claude/work/2026-10-08_01_rev2-campaign/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-003 — Analytical model: fragments (LMW), per-study method assignment, SEC matrix bias, all on independent RNG streams

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Acceptance criteria

- [x] `fragments_lmw` CQA in cqa_register.csv with DS criterion and source comment
- [x] DoE CSVs gain lmw_sec_pct / lmw_cesds_pct; a cell is NaN exactly where the method plan says not tested
- [x] test: every pre-existing DoE, PPQ and MC column is byte-identical to a same-environment run of the old generator (fixture captured before the change)
- [x] test: SEC minus CE-SDS LMW bias > 0 at protein_a and VI, |bias| below the CE-SDS precision at CEX and later

**Depends on:** [[TASK-002]]

## What was built

fragments_lmw CQA (DS <=2.0 %, nrCE-SDS clipped species). amab_process/analytics.py: true fragment model, SEC bias = 0.00011*HCP + 0.06*leached PA, method plan; all on independent RNG streams after the run. 18 parametrized byte-identity tests vs corpus-rev1.0 pass (rtol 1e-12). SEC-CE bias: Protein A pool +1.19, VI pool +1.29, CEX pool +0.03, AEX pool -0.06. AEX superseded = SEC only, re-execution = CE-SDS only. Mechanism entries for fragments added to harvest/protein_a/viral_inactivation/cex yaml with pending_owner_review.

## Files it touched

- `config/parameters.yaml`
- `amab_process/analytics.py`
- `amab_process/studies.py`
- `scripts/generate_data.py`
- `scripts/generate_superseded.py`
- `tests/test_process.py`
