---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-011
status: todo
kind: measurement
title: "Prove the corpus is unchanged: annexes, grounding, outputs, tests and style at the end of the unit"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-011 — Prove the corpus is unchanged: annexes, grounding, outputs, tests and style at the end of the unit

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

This is the rebuild-and-reground task the workflow requires, sized to what this unit touches: nothing upstream of a rendered document changes, so the expectation is 'identical', and the task exists to prove it rather than assume it. Runs whichever way D4 fell, after TASK-005 and after whichever of TASK-006..TASK-010 ran.

## Acceptance criteria

- [ ] `cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py` → 20/20 annexes valid; `GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py` → 2084/2084 quotes grounded, 0 weak anchors
- [ ] `git diff --stat outputs/ pc_package/ground_truth/ pc_package/*.qmd` is empty — no shipped document, annex or dataset changed anywhere in this unit
- [ ] `make test PY="uv run python"` passes (89, or the count TASK-006 recorded if it ran); `make style PY="uv run python"` → 24 OK / 0 FAIL
- [ ] the two untracked probe files and their renders are either deleted or listed in the outcome as deliberately left untracked; `git status --short` shows nothing tracked outside docs/, authoring/, tests/, .claude/work/ and CLAUDE.md

**Depends on:** [[TASK-005]]

## Files it touched

- not recorded
