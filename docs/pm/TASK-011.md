---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-011
status: todo
kind: annex
title: "Promote batch B1 (PCR-006, PCR-008, PCR-009, PCR-010): render, re-cut spans, re-anchor, re-ground"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-006", "PCR-008", "PCR-009", "PCR-010"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-011 — Promote batch B1 (PCR-006, PCR-008, PCR-009, PCR-010): render, re-cut spans, re-anchor, re-ground

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

B1: 4 documents, 303 quotes, 123 spans. Serial: no overlap with authoring or another annex task.

## Acceptance criteria

- [ ] ANNEX-A-BATCH.md (2026-08-18_02 unit) for the batch, SERIAL: promote each DRAFT, render both formats explicitly, no missing glyph on each FRESH pdf, page counts recorded; the OLD pdf of every document in the batch saved first as `$U/B1-old-<DOC>.pdf` (for the sampled reading)
- [ ] rhetorical spans re-cut FIRST for every document with a layer (PCR-006 31, PCR-008 25, PCR-009 37, PCR-010 30), tested under BOTH extractors, builder writes with the count (dropped none, or explained); every mechanistic_warrant span names a physical cause
- [ ] annex quotes re-anchored in each document's region (303 quotes across the batch; table rows rebuild themselves); every report_sections statement READ against the new text and rewritten where false
- [ ] registered discrepancies PCR-006 (D-001), PCR-008 (D-001), PCR-009 (D-001): registered_sentence present in the new docx per ANNEX-A-BATCH §5; `discrepancies.yaml` and `DISCREPANCIES.md` updated together if the wording moved, the claim unchanged
- [ ] 20/20 valid; strict grounding N/N with N printed and any change explained; 0 weak anchors; weak_claims 0 in all 20; `git status --short` only this batch's files; `git diff --stat outputs/` empty; make test; make style 24 OK

**Depends on:** [[TASK-005]], [[TASK-007]], [[TASK-008]], [[TASK-009]], [[TASK-010]]

## Documents it is about

- **PCR-006** — `pc_package/PCR-006_viral_inactivation.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`
- **PCR-009** — `pc_package/PCR-009_virus_filtration.qmd`
- **PCR-010** — `pc_package/PCR-010_ufdf.qmd`

## Files it touched

- `pc_package/PCR-006_viral_inactivation.qmd`
- `pc_package/PCR-008_aex.qmd`
- `pc_package/PCR-009_virus_filtration.qmd`
- `pc_package/PCR-010_ufdf.qmd`
- `pc_package/build_ground_truth.py`
- `authoring/rhetorical/PCR-006.spans.yaml`
- `authoring/rhetorical/PCR-008.spans.yaml`
- `authoring/rhetorical/PCR-009.spans.yaml`
- `authoring/rhetorical/PCR-010.spans.yaml`
- `pc_package/ground_truth/PCR-006.json`
- `pc_package/ground_truth/PCR-008.json`
- `pc_package/ground_truth/PCR-009.json`
- `pc_package/ground_truth/PCR-010.json`
