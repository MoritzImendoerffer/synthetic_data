---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-048
status: todo
kind: annex
title: "Dispose of PCR-008 per the reading: promote attempt 3, or revert to round zero by name; re-ground either way"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-048 — Dispose of PCR-008 per the reading: promote attempt 3, or revert to round zero by name; re-ground either way

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

Carries TASK-044's revert recipe unchanged. build_ground_truth.py has moved since 8327605~1.

## Acceptance criteria

- [ ] On PASS: ANNEX-A-BATCH for one document — promote the attempt-3 DRAFT, render both formats, re-cut the 25 spans against the new text, re-anchor the ax_* report quotes, D-001 §5 check
- [ ] On FAIL: `git checkout 8327605~1 -- pc_package/PCR-008_aex.qmd pc_package/PCR-008_aex.docx pc_package/PCR-008_aex.pdf authoring/rhetorical/PCR-008.spans.yaml` plus restoring ONLY the ax_* REPORT branches of build_ground_truth.py to their 8327605~1 state, by named hunks, never a whole-file checkout
- [ ] either way: 20/20 valid; strict grounding N/N with N printed; 0 weak anchors; `git diff --stat outputs/` empty; make test; make style 24 OK

**Depends on:** [[TASK-047]]

## Documents it is about

- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- `pc_package/PCR-008_aex.qmd`
- `pc_package/PCR-008_aex.docx`
- `pc_package/PCR-008_aex.pdf`
- `authoring/rhetorical/PCR-008.spans.yaml`
- `pc_package/build_ground_truth.py`
- `pc_package/ground_truth/PCR-008.json`
