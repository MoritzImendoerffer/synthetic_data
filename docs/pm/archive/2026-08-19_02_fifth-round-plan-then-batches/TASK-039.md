---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-039
status: done
kind: measurement
title: "Rebuild-and-reground proof after batch B5"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCMP-001", "PCMR-001", "PTP-001", "RA-001"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-039 — Rebuild-and-reground proof after batch B5

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

No make data figures.

## Acceptance criteria

- [x] `check_render.py --render` clean on every promoted document of the batch (glyphs on fresh pdfs; docx restored by name afterwards); 20/20 valid; N/N grounded strict, exit 0; `git diff --stat outputs/` empty; make test; make style 24 OK; page counts against CLAUDE.md's bands, re-measured at ship if moved

**Depends on:** [[TASK-037]]

## What was built

Rebuild-and-reground proof after B5, no `make data figures`. check_render.py --render clean on all four promoted documents: all chunks exec, all inline expressions eval, 0 <<NEEDS>>, gated tic rows all OK, docx renders, no missing glyphs on any FRESH pdf. 20/20 annexes valid. GROUNDING 2089/2089 quotes across 20 annexes under GROUNDING_STRICT_ANCHORS=1, exit 0, 0 weak anchors — the same N as TASK-037. git diff --stat outputs/ empty. make test 95 passed. make style 24 OK. The render rewrote all four tracked .docx, so they were RESTORED BY NAME and grounding re-run against the restored files, still 2089/2089; the tree is clean afterwards. Page counts 26 / 23 / 28 / 38 pp (PTP-001, PCMP-001, RA-001, PCMR-001). NOTE FOR SHIP: CLAUDE.md's depth bands cover reports with a DoE (41-56 pp), reports without one (26-28 pp) and plans (23-31 pp), and say nothing about the four corpus-level documents. PCMR-001 at 38 pp sits outside every stated band because no band describes it. The bands need a fourth row rather than a correction.

## Documents it is about

- **PCMP-001** — `pc_package/PCMP-001_master_plan.qmd`
- **PCMR-001** — `pc_package/PCMR-001_master_report.qmd`
- **PTP-001** — `pc_package/PTP-001_transfer.qmd`
- **RA-001** — `pc_package/RA-001_risk_assessment.qmd`

## Files it touched

- not recorded
