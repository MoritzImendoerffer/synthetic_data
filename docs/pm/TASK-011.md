---
type: pm-task
epic: 2026-10-08_01_rev2-campaign
sprint: 2026-10-08_01_rev2-campaign
task: TASK-011
status: done
kind: document
title: "Author INV-001 (investigation report)"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-003", "PCR-006"]
---

> [!warning] Generated from `.claude/work/2026-10-08_01_rev2-campaign/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-011 — Author INV-001 (investigation report)

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Pilot.

## Acceptance criteria

- [x] check_render hard gates pass; docx + pdf render
- [x] merged tables visible in pdf

**Depends on:** [[TASK-009]], [[TASK-010]]

## What was built

INV-001 v1.0 authored (one Opus 5.5 agent, audit clean), run-1 review -> SEC model found physically impossible (fixed at source) + CA4/terms; author cycle; run-2: all arithmetic verified, 13 Q5 items (3 from tables.py, fixed) -> one factual pass (recorded departure). Shipped 30 pp, 238 sentences / 4,180 words, 5 complex tables fit, 0 NEEDS. Surfaces two NOR-corner shortfalls for PCR-003 (acidic 17.7 vs 18) and PCR-006 (XMuLV 6.43 vs 6.6).

## Documents it is about

- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-006** — `pc_package/PCR-006_viral_inactivation.qmd`

## Files it touched

- `pc_package/INV-001_investigation.qmd`
