---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-025
status: todo
kind: annex
title: "Promote batch B3 (PCP-004, PCP-006, PCP-008, PCP-009, PCP-010): render, re-cut spans, re-anchor, re-ground"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCP-004", "PCP-006", "PCP-008", "PCP-009", "PCP-010"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-025 — Promote batch B3 (PCP-004, PCP-006, PCP-008, PCP-009, PCP-010): render, re-cut spans, re-anchor, re-ground

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

B3: 5 documents, 191 quotes, 0 spans. Serial: no overlap with authoring or another annex task.

## Acceptance criteria

- [ ] ANNEX-A-BATCH.md (2026-08-18_02 unit) for the batch, SERIAL: promote each DRAFT, render both formats explicitly, no missing glyph on each FRESH pdf, page counts recorded; the OLD pdf of every document in the batch saved first as `$U/B3-old-<DOC>.pdf` (for the sampled reading)
- [ ] rhetorical spans re-cut FIRST for every document with a layer (none in this batch), tested under BOTH extractors, builder writes with the count (dropped none, or explained); every mechanistic_warrant span names a physical cause
- [ ] annex quotes re-anchored in each document's region (191 quotes across the batch; table rows rebuild themselves); every report_sections statement READ against the new text and rewritten where false
- [ ] registered discrepancies PCP-006 (D-001), PCP-008 (D-001), PCP-009 (D-001): registered_sentence present in the new docx per ANNEX-A-BATCH §5; `discrepancies.yaml` and `DISCREPANCIES.md` updated together if the wording moved, the claim unchanged
- [ ] 20/20 valid; strict grounding N/N with N printed and any change explained; 0 weak anchors; weak_claims 0 in all 20; `git status --short` only this batch's files; `git diff --stat outputs/` empty; make test; make style 24 OK

**Depends on:** [[TASK-020]], [[TASK-021]], [[TASK-022]], [[TASK-023]], [[TASK-024]]

## Documents it is about

- **PCP-004** — `pc_package/PCP-004_harvest.qmd`
- **PCP-006** — `pc_package/PCP-006_viral_inactivation.qmd`
- **PCP-008** — `pc_package/PCP-008_aex.qmd`
- **PCP-009** — `pc_package/PCP-009_virus_filtration.qmd`
- **PCP-010** — `pc_package/PCP-010_ufdf.qmd`

## Files it touched

- `pc_package/PCP-004_harvest.qmd`
- `pc_package/PCP-006_viral_inactivation.qmd`
- `pc_package/PCP-008_aex.qmd`
- `pc_package/PCP-009_virus_filtration.qmd`
- `pc_package/PCP-010_ufdf.qmd`
- `pc_package/build_ground_truth.py`
- `pc_package/ground_truth/PCP-004.json`
- `pc_package/ground_truth/PCP-006.json`
- `pc_package/ground_truth/PCP-008.json`
- `pc_package/ground_truth/PCP-009.json`
- `pc_package/ground_truth/PCP-010.json`
