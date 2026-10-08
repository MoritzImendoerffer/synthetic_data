---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-030
status: done
kind: annex
title: "Promote batch B4 (PCP-003, PCP-007): render, re-cut spans, re-anchor, re-ground"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCMR-001", "PCP-003", "PCP-006", "PCP-007", "PCP-008", "PCP-009"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-030 — Promote batch B4 (PCP-003, PCP-007): render, re-cut spans, re-anchor, re-ground

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

B4: 2 documents, 115 quotes, 0 spans. Serial: no overlap with authoring or another annex task.

## Acceptance criteria

- [x] ANNEX-A-BATCH.md (2026-08-18_02 unit) for the batch, SERIAL: promote each DRAFT, render both formats explicitly, no missing glyph on each FRESH pdf, page counts recorded; the OLD pdf of every document in the batch saved first as `$U/B4-old-<DOC>.pdf` (for the sampled reading)
- [x] rhetorical spans re-cut FIRST for every document with a layer (none in this batch), tested under BOTH extractors, builder writes with the count (dropped none, or explained); every mechanistic_warrant span names a physical cause
- [x] annex quotes re-anchored in each document's region (115 quotes across the batch; table rows rebuild themselves); every report_sections statement READ against the new text and rewritten where false
- [x] registered discrepancies PCP-003 (D-001): registered_sentence present in the new docx per ANNEX-A-BATCH §5; `discrepancies.yaml` and `DISCREPANCIES.md` updated together if the wording moved, the claim unchanged
- [x] 20/20 valid; strict grounding N/N with N printed and any change explained; 0 weak anchors; weak_claims 0 in all 20; `git status --short` only this batch's files; `git diff --stat outputs/` empty; make test; make style 24 OK

**Depends on:** [[TASK-028]], [[TASK-029]]

## What was built

Batch B4 promoted: PCP-003 and PCP-007, serial, no rhetorical layer in either (the nine spans files are the reports plus PCMR-001). Old pdfs saved first as B4-old-PCP-003.pdf (29 pp) and B4-old-PCP-007.pdf (30 pp) for TASK-031. `git mv` refused the drafts because they were untracked; plain `mv -f` over the tracked file is the correct promotion here and the procedure's `git mv -f` line assumes a tracked draft. Rendered both formats explicitly with the venv on PATH: PCP-003 31 pp (was 29), PCP-007 30 pp (was 30), no missing glyphs on either FRESH pdf, 0 <<NEEDS>>, 0 typed measurements, gated tics 0.0. RE-ANCHORED 52 quotes: 24 in PCP-003 (19 distinct) and 28 in PCP-007 (21 distinct); table rows rebuilt themselves as the procedure predicts and needed nothing. GROUNDING 2088/2088 quotes across 20 annexes, unchanged from the pre-promotion baseline of 2088/2088; 20/20 valid; 0 weak anchors under GROUNDING_STRICT_ANCHORS=1; weak_claims 0 in all 20. Per-document check_grounding counts are 105 (PCP-003) and 67 (PCP-007) because that denominator is quotes PLUS table_headers: 66+39 and 49+18, so the plan's notes of 66 and 49 were exact. FOUR report_sections STATEMENTS WERE FALSE against the re-authored text and were rewritten, not just re-anchored — the defect class the procedure warns about, which no gate catches. PCP-007 st6 still said 'assurance margin' and 'break-even point', both removed by the review cycle, and attributed the divisor to host cell protein alone when the plan divides BOTH criteria by a safety factor; PCP-007 st7 said a model fails 'any of the four acceptance conditions' when the plan states two, and claimed the governing parameters are held at their normal operating ranges, which the plan never says; PCP-003 st4 read the lack-of-fit test as sufficient when it is one of three adequacy conditions; PCP-003 st5 said 'every governed attribute' where the plan declares the region over every MODELLED attribute. SCALE_L was added to the builder (P.V['commercial_scale_l']) so the vessel quote is built from the value the document renders instead of a typed 15,000. D-001: the commitment survived the re-author VERBATIM in the .qmd, so §5 required no change to what it claims. REGISTRY DEFECT FOUND AND CORRECTED: PCP-003's registered_sentence is stored in .qmd form and its comment justified that by citing PCP-009 as precedent — false, PCP-009 stores the RENDERED sentence with '201 points' baked in, as do PCP-006 and PCP-008. ANNEX-A-BATCH §5's docx test therefore can never pass for PCP-003, and a session running it mechanically would read a surviving discrepancy as vanished. The comment in discrepancies.yaml and the prose in DISCREPANCIES.md now say so and point the check at the .qmd; the claim itself is untouched and the convention split is recorded rather than repaired. make test 95 passed; make style 24 OK; git diff --stat outputs/ empty; git status shows only this batch's files plus the two discrepancy files.

## Documents it is about

- **PCMR-001** — `pc_package/PCMR-001_master_report.qmd`
- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCP-006** — `pc_package/PCP-006_viral_inactivation.qmd`
- **PCP-007** — `pc_package/PCP-007_cex.qmd`
- **PCP-008** — `pc_package/PCP-008_aex.qmd`
- **PCP-009** — `pc_package/PCP-009_virus_filtration.qmd`

## Files it touched

- `pc_package/PCP-003_bioreactor.qmd`
- `pc_package/PCP-007_cex.qmd`
- `pc_package/build_ground_truth.py`
- `pc_package/ground_truth/PCP-003.json`
- `pc_package/ground_truth/PCP-007.json`
