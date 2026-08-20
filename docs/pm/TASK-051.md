---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-051
status: todo
kind: annex
title: "Dispose of PCR-004 per the reading: promote attempt 2, or revert to the pre-campaign text by name; re-ground either way"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-004"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-051 — Dispose of PCR-004 per the reading: promote attempt 2, or revert to the pre-campaign text by name; re-ground either way

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

The revert target is 083bfb1, the commit the B2-old pdfs were taken from. build_ground_truth.py has moved a long way since, so the harvest region is restored by named hunks only.

## Acceptance criteria

- [ ] On PASS: ANNEX-A-BATCH for one document — promote, render both formats, re-cut the 36 spans against the new text under BOTH extractors, re-anchor the harvest-region annex quotes, read every report_sections statement against the new text
- [ ] On FAIL: restore pc_package/PCR-004_harvest.{qmd,docx,pdf} and authoring/rhetorical/PCR-004.spans.yaml from 083bfb1, plus the harvest-region hunks of build_ground_truth.py, by named hunks and never a whole-file checkout
- [ ] either way: 20/20 valid; strict grounding N/N with N printed; 0 weak anchors; `git diff --stat outputs/` empty; make test; make style 24 OK

**Depends on:** [[TASK-050]]

## Documents it is about

- **PCR-004** — `pc_package/PCR-004_harvest.qmd`

## Files it touched

- `pc_package/PCR-004_harvest.qmd`
- `pc_package/PCR-004_harvest.docx`
- `pc_package/PCR-004_harvest.pdf`
- `authoring/rhetorical/PCR-004.spans.yaml`
- `pc_package/build_ground_truth.py`
- `pc_package/ground_truth/PCR-004.json`
