---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-006
status: done
kind: measurement
title: "Rebuild-and-reground proof after the pilot's promotion"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-005"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-006 — Rebuild-and-reground proof after the pilot's promotion

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Nothing upstream of a render changed but this document; no make data figures.

## Acceptance criteria

- [x] `check_render.py pc_package/PCP-005_protein_a.qmd --render` clean with glyphs; 20/20 valid; N/N grounded strict, exit 0; `git diff --stat outputs/` empty; make test passes; make style 24 OK; the re-rendered docx restored by name if --render rewrote it; page count inside CLAUDE.md's plan band 23–31 pp or the band re-measured at ship

**Depends on:** [[TASK-005]]

## What was built

check_render.py --render on the promoted PCP-005: all chunks exec, no <<NEEDS>>, tic gate OK, docx renders, no missing glyph; the re-rendered docx restored by name; strict grounding 2084/2084 against the committed docx, exit 0; `git diff --stat outputs/` empty; make test 95; make style 24 OK; 31 pages, inside the plan band 23–31. Clean boundary: the unit can be picked up cold from here.

## Documents it is about

- **PCP-005** — `pc_package/PCP-005_protein_a.qmd`

## Files it touched

- not recorded
