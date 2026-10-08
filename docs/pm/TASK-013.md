---
type: pm-task
epic: 2026-10-08_01_rev2-campaign
sprint: 2026-10-08_01_rev2-campaign
task: TASK-013
status: done
kind: document
title: "Author PCR-005 Rev 2.0"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCMP-001", "PCP-005", "PCR-005"]
---

> [!warning] Generated from `.claude/work/2026-10-08_01_rev2-campaign/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-013 — Author PCR-005 Rev 2.0

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Pilot. May read PCP-005 and PCMP-001 for content.

## Acceptance criteria

- [x] check_render hard gates pass; review checklist run by a fresh reviewer

**Depends on:** [[TASK-012]]

## What was built

PCR-005 v2.0: one Opus 5.5 author, audit clean. First draft left 5 NEEDS for data the plan promised but the model lacked -> generated (univariate studies, column efficiency, run order, per-pool HMW, centre-point DNA) for all steps. Found the PCP-005 equivalence test could never pass with n=3 -> DEV-005-03, 6 supplementary runs (S-PA-SDM2), margin unchanged: HCP equivalent, yield misses by 1.4 % of margin. Run-1 review -> 6 source fixes (inward PAR rounding, decision statistic, DEV-005-01/-02 consistency, leaching mechanism, tokens); run-2 -> prediction interval now includes coefficient uncertainty (engine), par_table number format, shrink-to-fit tables; final factual pass. Shipped 55 pp, 625 sentences / 11,661 words, 0 NEEDS.

## Documents it is about

- **PCMP-001** — `pc_package/PCMP-001_master_plan.qmd`
- **PCP-005** — `pc_package/PCP-005_protein_a.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`

## Files it touched

- `pc_package/PCR-005_protein_a.qmd`
