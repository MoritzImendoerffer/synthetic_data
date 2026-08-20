---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-044
status: todo
kind: annex
title: "Dispose of PCR-008 per the reading: promote attempt 2, or revert to round-zero by name; re-ground either way"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-006", "PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-044 — Dispose of PCR-008 per the reading: promote attempt 2, or revert to round-zero by name; re-ground either way

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

The revert path is the delicate one: build_ground_truth.py has moved since 8327605~1 (PCR-006/009/010 re-anchoring). Restore only the ax_* report-branch hunks, verified by check_grounding on all 20 afterwards.

## Acceptance criteria

- [ ] On PASS: ANNEX-A-BATCH for one document — promote the attempt-2 DRAFT, render both formats, re-cut the 25 spans against the new text (both extractors), re-anchor the ax_* report quotes, D-001 §5 check; on FAIL: `git checkout 8327605~1 -- pc_package/PCR-008_aex.qmd pc_package/PCR-008_aex.docx pc_package/PCR-008_aex.pdf authoring/rhetorical/PCR-008.spans.yaml` plus restoring the ax_* REPORT branches of build_ground_truth.py to their 8327605~1 state (the plan branches and every other region keep their current state — surgical, by named hunks, never a whole-file checkout of build_ground_truth.py, which also carries the B1 re-anchoring of three other documents), and the FAIL recorded in HANDOFF at ship as the document where the old register won
- [ ] either way: 20/20 valid; strict grounding N/N with N printed and explained (2088 today); 0 weak anchors; `git diff --stat outputs/` empty; make test; make style 24 OK; git status clean of everything but this document's files

**Depends on:** [[TASK-043]]

## Documents it is about

- **PCR-006** — `pc_package/PCR-006_viral_inactivation.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- `pc_package/PCR-008_aex.qmd`
- `pc_package/PCR-008_aex.docx`
- `pc_package/PCR-008_aex.pdf`
- `authoring/rhetorical/PCR-008.spans.yaml`
- `pc_package/build_ground_truth.py`
- `pc_package/ground_truth/PCR-008.json`
