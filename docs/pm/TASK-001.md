---
type: pm-task
epic: 2026-10-08_01_rev2-campaign
sprint: 2026-10-08_01_rev2-campaign
task: TASK-001
status: done
kind: mechanism
title: "Freeze Rev 1.0: tag corpus-rev1.0, copy the 20 DOCX/PDF and annexes to pc_package/superseded/rev1/"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
---

> [!warning] Generated from `.claude/work/2026-10-08_01_rev2-campaign/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-001 — Freeze Rev 1.0: tag corpus-rev1.0, copy the 20 DOCX/PDF and annexes to pc_package/superseded/rev1/

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Rev 1.0 is a frozen record, not rebuildable from main. Regenerate it from the tag.

## Acceptance criteria

- [x] git tag corpus-rev1.0 points at b3b9952
- [x] pc_package/superseded/rev1/ holds 20 .docx, 20 .pdf, 20 ground_truth/*.json and a README with sha256 manifest
- [x] `check_grounding.py --dir superseded/rev1` reports every quote grounded (2089/2089 expected)

## What was built

Tag corpus-rev1.0 at b3b9952. pc_package/superseded/rev1/: 20 docx, 20 pdf, 20 annexes, README with sha256 manifest. check_grounding.py gained --dir; GROUNDING_STRICT_ANCHORS=1 --dir superseded/rev1 -> 2089/2089.

## Files it touched

- `pc_package/superseded/rev1/`
- `pc_package/check_grounding.py`
