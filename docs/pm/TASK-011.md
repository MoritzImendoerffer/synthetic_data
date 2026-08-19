---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-011
status: done
kind: measurement
title: "Prove the corpus is unchanged: annexes, grounding, outputs, tests and style at the end of the unit"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-011 — Prove the corpus is unchanged: annexes, grounding, outputs, tests and style at the end of the unit

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

This is the rebuild-and-reground task the workflow requires, sized to what this unit touches: nothing upstream of a rendered document changes, so the expectation is 'identical', and the task exists to prove it rather than assume it. Runs whichever way D4 fell, after TASK-005 and after whichever of TASK-006..TASK-010 ran.

## Acceptance criteria

- [x] `cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py` → 20/20 annexes valid; `GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py` → 2084/2084 quotes grounded, 0 weak anchors
- [x] `git diff --stat outputs/ pc_package/ground_truth/ pc_package/*.qmd` is empty — no shipped document, annex or dataset changed anywhere in this unit
- [x] `make test PY="uv run python"` passes (89, or the count TASK-006 recorded if it ran); `make style PY="uv run python"` → 24 OK / 0 FAIL
- [x] the two untracked probe files and their renders are either deleted or listed in the outcome as deliberately left untracked; `git status --short` shows nothing tracked outside docs/, authoring/, tests/, .claude/work/ and CLAUDE.md

**Depends on:** [[TASK-005]]

## What was built

Run 2026-08-19 after TASK-005..TASK-010 (TASK-009 still halted for the owner's read; it changes nothing under pc_package/, so this proof stands and is re-run at ship). `cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py` -> 20/20 annexes valid. `GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py` -> 2084/2084 quotes grounded across 20 annexes, exit 0 with strict anchors (0 weak anchors — no 'weak' line printed). `git diff --stat outputs/ pc_package/ground_truth/ pc_package/*.qmd` -> empty: no shipped document, annex or dataset changed anywhere in this unit. `make test` -> 95 passed (89 + test_limits_split, test_evaluate_gates_only_the_tics, and the five mechanism tests, minus the retired test_limits_unchanged). `make style` -> 26 OK / 0 FAIL (24 shipped + the two untracked probe files the glob picks up). `git status --short` shows nothing tracked modified; the only untracked files are pc_package/PCR-005_protein_a.PROBE.{qmd,pdf} and .EXCERPT.{qmd,pdf}, deliberately left untracked as the probe's vehicle (their content is in A.pdf/B.pdf and reproducible from build_probe_scaffold.py + the agent's transcript) — TASK-012 decides whether to delete them.

## Files it touched

- not recorded
