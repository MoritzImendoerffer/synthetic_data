---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-019
status: done
kind: measurement
title: "Rebuild-and-reground proof after batch B2"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-003", "PCR-004", "PCR-005", "PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-019 — Rebuild-and-reground proof after batch B2

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

No make data figures.

## Acceptance criteria

- [x] `check_render.py --render` clean on every promoted document of the batch (glyphs on fresh pdfs; docx restored by name afterwards); 20/20 valid; N/N grounded strict, exit 0; `git diff --stat outputs/` empty; make test; make style 24 OK; page counts against CLAUDE.md's bands, re-measured at ship if moved

**Depends on:** [[TASK-017]]

## What was built

Rebuild-and-reground proof after B2, no `make data figures`. check_render --render clean on all four promoted documents; the only FAIL lines are the ADVISORY numeral lint (PCR-003 20 lines, PCR-008 15, all statistical conventions, guidance names and identifiers). No missing glyphs on any fresh pdf. The four docx/pdf pairs were then restored BY NAME so the committed baseline could not drift, and everything re-verified against the committed renders: 20/20 annexes valid; 2085/2085 quotes grounded under GROUNDING_STRICT_ANCHORS=1, exit 0, 0 weak anchors; `git diff --stat outputs/` empty; make test 95 passed; make style 24 OK; `git status --short` empty. PAGE COUNTS against CLAUDE.md's bands: PCR-003 55, PCR-005 47, PCR-008 53 — all inside the 41-56 band for a report with a DoE. PCR-004 is 31 pp against a measured non-DoE band of 26-28, so the band moves or the document is long; flagged at authoring, not padded down, and to be re-measured at ship.

## Documents it is about

- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-004** — `pc_package/PCR-004_harvest.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- not recorded
