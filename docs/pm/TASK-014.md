---
type: pm-task
epic: 2026-10-08_01_rev2-campaign
sprint: 2026-10-08_01_rev2-campaign
task: TASK-014
status: done
kind: annex
title: "Annex the pilot: INV-001, PCMP-001, PCP-005, PCR-005"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCMP-001", "PCP-005", "PCR-005"]
---

> [!warning] Generated from `.claude/work/2026-10-08_01_rev2-campaign/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-014 — Annex the pilot: INV-001, PCMP-001, PCP-005, PCR-005

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Acceptance criteria

- [x] validate_annex all valid
- [x] GROUNDING_STRICT_ANCHORS=1 check_grounding passes on the three

**Depends on:** [[TASK-011]], [[TASK-012]], [[TASK-013]], [[TASK-016]]

## What was built

All four pilot documents annexed against their final text: 21/21 valid, 3086/3086 grounded with strict anchors (INV-001 302, PCMP-001 521, PCP-005 165, PCR-005 265), Rev 1.0 set still 2089/2089, 136 tests. PCR-005 rhetorical spans re-curated (40, roles unchanged) - owner to confirm.

## Documents it is about

- **PCMP-001** — `pc_package/PCMP-001_master_plan.qmd`
- **PCP-005** — `pc_package/PCP-005_protein_a.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`

## Files it touched

- `pc_package/build_ground_truth.py`
