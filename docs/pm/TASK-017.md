---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-017
status: todo
kind: annex
title: "Promote batch B2 (PCR-004, PCR-003, PCR-005): render, re-cut spans, re-anchor, re-ground"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-003", "PCR-004", "PCR-005"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-017 — Promote batch B2 (PCR-004, PCR-003, PCR-005): render, re-cut spans, re-anchor, re-ground

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

B2: 3 documents, 291 quotes, 110 spans. Serial: no overlap with authoring or another annex task.

## Acceptance criteria

- [ ] ANNEX-A-BATCH.md (2026-08-18_02 unit) for the batch, SERIAL: promote each DRAFT, render both formats explicitly, no missing glyph on each FRESH pdf, page counts recorded; the OLD pdf of every document in the batch saved first as `$U/B2-old-<DOC>.pdf` (for the sampled reading)
- [ ] rhetorical spans re-cut FIRST for every document with a layer (PCR-004 36, PCR-003 35, PCR-005 39), tested under BOTH extractors, builder writes with the count (dropped none, or explained); every mechanistic_warrant span names a physical cause
- [ ] annex quotes re-anchored in each document's region (291 quotes across the batch; table rows rebuild themselves); every report_sections statement READ against the new text and rewritten where false
- [ ] registered discrepancies PCR-003 (D-002): registered_sentence present in the new docx per ANNEX-A-BATCH §5; `discrepancies.yaml` and `DISCREPANCIES.md` updated together if the wording moved, the claim unchanged
- [ ] 20/20 valid; strict grounding N/N with N printed and any change explained; 0 weak anchors; weak_claims 0 in all 20; `git status --short` only this batch's files; `git diff --stat outputs/` empty; make test; make style 24 OK

**Depends on:** [[TASK-014]], [[TASK-015]], [[TASK-016]]

## Documents it is about

- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-004** — `pc_package/PCR-004_harvest.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`

## Files it touched

- `pc_package/PCR-004_harvest.qmd`
- `pc_package/PCR-003_bioreactor.qmd`
- `pc_package/PCR-005_protein_a.qmd`
- `pc_package/build_ground_truth.py`
- `authoring/rhetorical/PCR-004.spans.yaml`
- `authoring/rhetorical/PCR-003.spans.yaml`
- `authoring/rhetorical/PCR-005.spans.yaml`
- `pc_package/ground_truth/PCR-004.json`
- `pc_package/ground_truth/PCR-003.json`
- `pc_package/ground_truth/PCR-005.json`
