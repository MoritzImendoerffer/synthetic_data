---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-037
status: todo
kind: annex
title: "Promote batch B5 (PTP-001, PCMP-001, RA-001, PCMR-001): render, re-cut spans, re-anchor, re-ground"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCMP-001", "PCMR-001", "PTP-001", "RA-001"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-037 — Promote batch B5 (PTP-001, PCMP-001, RA-001, PCMR-001): render, re-cut spans, re-anchor, re-ground

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

B5: 4 documents, 440 quotes, 49 spans. Serial: no overlap with authoring or another annex task.

## Acceptance criteria

- [ ] ANNEX-A-BATCH.md (2026-08-18_02 unit) for the batch, SERIAL: promote each DRAFT, render both formats explicitly, no missing glyph on each FRESH pdf, page counts recorded; the OLD pdf of every document in the batch saved first as `$U/B5-old-<DOC>.pdf` (for the sampled reading)
- [ ] rhetorical spans re-cut FIRST for every document with a layer (PCMR-001 49), tested under BOTH extractors, builder writes with the count (dropped none, or explained); every mechanistic_warrant span names a physical cause
- [ ] annex quotes re-anchored in each document's region (440 quotes across the batch; table rows rebuild themselves); every report_sections statement READ against the new text and rewritten where false
- [ ] no registered discrepancy in this batch, stated
- [ ] 20/20 valid; strict grounding N/N with N printed and any change explained; 0 weak anchors; weak_claims 0 in all 20; `git status --short` only this batch's files; `git diff --stat outputs/` empty; make test; make style 24 OK

**Depends on:** [[TASK-033]], [[TASK-034]], [[TASK-035]], [[TASK-036]]

## Documents it is about

- **PCMP-001** — `pc_package/PCMP-001_master_plan.qmd`
- **PCMR-001** — `pc_package/PCMR-001_master_report.qmd`
- **PTP-001** — `pc_package/PTP-001_transfer.qmd`
- **RA-001** — `pc_package/RA-001_risk_assessment.qmd`

## Files it touched

- `pc_package/PTP-001_None.qmd`
- `pc_package/PCMP-001_None.qmd`
- `pc_package/RA-001_None.qmd`
- `pc_package/PCMR-001_None.qmd`
- `pc_package/build_ground_truth.py`
- `authoring/rhetorical/PCMR-001.spans.yaml`
- `pc_package/ground_truth/PTP-001.json`
- `pc_package/ground_truth/PCMP-001.json`
- `pc_package/ground_truth/RA-001.json`
- `pc_package/ground_truth/PCMR-001.json`
