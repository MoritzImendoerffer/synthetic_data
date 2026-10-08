---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-013
status: done
kind: measurement
title: "Rebuild-and-reground proof after batch B1"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-006", "PCR-008", "PCR-009", "PCR-010"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-013 — Rebuild-and-reground proof after batch B1

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

No make data figures.

## Acceptance criteria

- [x] `check_render.py --render` clean on every promoted document of the batch (glyphs on fresh pdfs; docx restored by name afterwards); 20/20 valid; N/N grounded strict, exit 0; `git diff --stat outputs/` empty; make test; make style 24 OK; page counts against CLAUDE.md's bands, re-measured at ship if moved

**Depends on:** [[TASK-011]]

## What was built

check_render.py --render on each promoted B1 document: all chunks exec, no <<NEEDS>>, tic gate OK, docx renders, no missing glyph on the fresh pdf (PCR-006, PCR-008, PCR-009, PCR-010); each re-rendered docx restored by name afterwards; strict grounding 2088/2088 against the committed docx, exit 0; `git diff --stat outputs/` empty; make test 95; make style 24 OK; tree clean. Page counts 45 / 54 / 34 / 30 — reports with a DoE inside CLAUDE.md's 41–56 band except PCR-009 at 34 (the smallest DoE in the corpus: 2 factors, 19 runs — depth follows the design; the band sentence is re-measured at ship), the non-DoE PCR-010 at 30 against the 26–28 band (also re-measured at ship).

## Documents it is about

- **PCR-006** — `pc_package/PCR-006_viral_inactivation.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`
- **PCR-009** — `pc_package/PCR-009_virus_filtration.qmd`
- **PCR-010** — `pc_package/PCR-010_ufdf.qmd`

## Files it touched

- not recorded
