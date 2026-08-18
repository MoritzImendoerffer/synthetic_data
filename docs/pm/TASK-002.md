---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-002
status: todo
kind: mechanism
title: "Freeze the Track D measurement as a script that reproduces the baseline"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-002 — Freeze the Track D measurement as a script that reproduces the baseline

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-002.md. THIS IS THE MEMORY-MEMO TASK. Twice now a number quoted in a planning document came from an unsaved heredoc and could not be reproduced -- round two's owner-reading counts, and the proposal's 1.5 % guide figure that re-measured at 3.77 %. No number produced by this round may come from anywhere but this script. It wraps check_style.py and check_discourse.py rather than re-implementing them.

## Acceptance criteria

- [ ] measure_trackd.py takes a list of .qmd and prints one row per document for every measure the stopping rule names, each with its denominator, plus the four human-source columns
- [ ] run over all 20 committed .qmd it reproduces measure_baseline_style.txt and measure_baseline_discourse.txt EXACTLY -- same numbers to one decimal, including PCP-005 passive 66.7, PCP-008 67.7 and RA-001 64.2, the three already above the source band
- [ ] it also emits the staccato and ', which' measures round three added by hand, so they are on one denominator with the rest
- [ ] the script is committed inside the work unit and the results page cites it by path

## Files it touched

- `.claude/work/2026-08-18_02_register-track-d/measure_trackd.py`
- `.claude/work/2026-08-18_02_register-track-d/measure_baseline_style.txt`
- `.claude/work/2026-08-18_02_register-track-d/measure_baseline_discourse.txt`
