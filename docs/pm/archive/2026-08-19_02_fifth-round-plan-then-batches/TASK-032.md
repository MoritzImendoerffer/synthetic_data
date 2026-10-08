---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-032
status: done
kind: measurement
title: "Rebuild-and-reground proof after batch B4"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCP-007"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-032 — Rebuild-and-reground proof after batch B4

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

No make data figures.

## Acceptance criteria

- [x] `check_render.py --render` clean on every promoted document of the batch (glyphs on fresh pdfs; docx restored by name afterwards); 20/20 valid; N/N grounded strict, exit 0; `git diff --stat outputs/` empty; make test; make style 24 OK; page counts against CLAUDE.md's bands, re-measured at ship if moved

**Depends on:** [[TASK-030]]

## What was built

Rebuild-and-reground proof after B4, with no `make data figures`. `check_render.py --render` clean on both promoted documents: all chunks exec, all inline expressions eval, 0 <<NEEDS>>, all five gated tic rows 0.0, docx renders, and no missing glyphs on either FRESH pdf. 20/20 annexes valid. GROUNDING 2088/2088 quotes across 20 annexes under GROUNDING_STRICT_ANCHORS=1, exit code 0, 0 weak anchors — the same N as the pre-promotion baseline and as TASK-030. `git diff --stat outputs/` empty. make test 95 passed. make style 24 OK. Page counts 31 pp (PCP-003) and 30 pp (PCP-007), both inside CLAUDE.md's plans band of 23-31 pp, so the band does not move; PCP-003 sits at the top of it. The render rewrote both tracked .docx files, so they were RESTORED BY NAME (never `git checkout -- pc_package/`, which would take the untracked B5 drafts with it) and grounding re-run against the restored files, still 2088/2088. Tree clean apart from the B5 drafts being authored concurrently.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCP-007** — `pc_package/PCP-007_cex.qmd`

## Files it touched

- not recorded
