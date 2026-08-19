---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-011
status: done
kind: annex
title: "Promote batch B1 (PCR-006, PCR-008, PCR-009, PCR-010): render, re-cut spans, re-anchor, re-ground"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-006", "PCP-008", "PCP-009", "PCR-006", "PCR-008", "PCR-009", "PCR-010"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-011 — Promote batch B1 (PCR-006, PCR-008, PCR-009, PCR-010): render, re-cut spans, re-anchor, re-ground

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

B1: 4 documents, 303 quotes, 123 spans. Serial: no overlap with authoring or another annex task.

## Acceptance criteria

- [x] ANNEX-A-BATCH.md (2026-08-18_02 unit) for the batch, SERIAL: promote each DRAFT, render both formats explicitly, no missing glyph on each FRESH pdf, page counts recorded; the OLD pdf of every document in the batch saved first as `$U/B1-old-<DOC>.pdf` (for the sampled reading)
- [x] rhetorical spans re-cut FIRST for every document with a layer (PCR-006 31, PCR-008 25, PCR-009 37, PCR-010 30), tested under BOTH extractors, builder writes with the count (dropped none, or explained); every mechanistic_warrant span names a physical cause
- [x] annex quotes re-anchored in each document's region (303 quotes across the batch; table rows rebuild themselves); every report_sections statement READ against the new text and rewritten where false
- [x] registered discrepancies PCR-006 (D-001), PCR-008 (D-001), PCR-009 (D-001): registered_sentence present in the new docx per ANNEX-A-BATCH §5; `discrepancies.yaml` and `DISCREPANCIES.md` updated together if the wording moved, the claim unchanged
- [x] 20/20 valid; strict grounding N/N with N printed and any change explained; 0 weak anchors; weak_claims 0 in all 20; `git status --short` only this batch's files; `git diff --stat outputs/` empty; make test; make style 24 OK

**Depends on:** [[TASK-005]], [[TASK-007]], [[TASK-008]], [[TASK-009]], [[TASK-010]]

## What was built

Batch B1 promoted 2026-08-19 per ANNEX-A-BATCH, serial. Old pdfs saved first as B1-old-PCR-006/008/009/010.pdf (for the sampled reading). DRAFTs -> PCR-006_viral_inactivation.qmd, PCR-008_aex.qmd, PCR-009_virus_filtration.qmd, PCR-010_ufdf.qmd; both formats rendered explicitly; no missing glyph on any fresh pdf; pages 45 (46 as authored), 54, 34, 30.

Spans re-cut FIRST, four fresh agents in parallel (one YAML each, no builder run), every quote tested under both extractors, no duplicates: PCR-006 31/31 (no role or edge changed; 7 spans moved section); PCR-008 25/25 (4 section renames; the two hollow-warrant frames the Track D page named — 'behaves as a charge partitioning process', 'Its governing parameter is…' — are gone, replaced by causes); PCR-009 37/37 (13 section moves; one edge dropped, R19 supported_by [R15,R17] -> [R15], because the new pressure warrant no longer supports the load claim); PCR-010 30/30 (18 section moves as §5/§6 were subdivided; one edge dropped, R24 [R21,R23] -> [R23], the scale-down weak quantity changed). Every mechanistic_warrant quote names a physical cause with a direction (12 across the four, verified in the reports).

Annexes re-anchored by two agents in sequence, each on its two regions only, verified by me: PCR-006 30 quotes (vi_step 1, vi_equipment 1, VIMETHOD 3, VI_CQA 3, vi_studies 4, vi_design_spaces 1, vi_report_sections 10, vi_assertions 10) — the design-space definition INVERTED to the new report (aggregate binds, two corners fall out), S01/S03/S04/S05/S06/S09/S10 restated, S08 given two anchors (+1 quote via a new `also=` slot in st()), stale vi_params rationales corrected; PCR-008 26 (ax_step 1, ax_equipment 1, AXMETHOD 5, ax_studies 4, ax_design_spaces 1, ax_report_sections 7+1, ax_assertions 7) — design space inverted (pool HCP the only constraining response, load pH low / wash conductivity high the rejected corner), a new S08 for the NOR box not entirely inside the design space (+1), assertions re-based on §9's reasons; PCR-009 21 (vf_* 1+1+2+2+5+9+1) — S07 was false in the new text and rewritten, S01 two anchors, S10 added for the PAR-below-NOR finding (+2), pressure assertion rewritten, DesignSpace definition one-directional; PCR-010 25 (uf_* 1+2+3+2+3+5+9) — the two monitored-attribute assertions moved off a table caption onto §2.2 sentences (new UFATTR_REPORT_QUOTE), S09 ('formulation characterization deferred') dropped because the new report does not say it and replaced by the no-margin-below-NOR finding, PAR acceptance_basis rewritten, the plan annexes PCP-009/010 restored byte-identical after a shared-text leak was caught. Table rows rebuilt themselves throughout; no hand-typed row.

D-001: PCR-006, PCR-008, PCR-009 carry it as do_not_reconcile with no registered_sentence; each new text keeps D.par_table as it comes ('PAR (set-point)' unrenamed), never says where the other parameters were held ('at fixed settings' / 'holds the rest' / 'fixes the other parameter'), and adds no reconciling sentence — checked on the rendered text. Found on the way, not acted on: PCP-008's registered_sentence in discrepancies.yaml has an ASCII apostrophe where the rendered document has a typographic one, so ANNEX-A-BATCH §5's check prints False for a sentence that is verbatim in the document (pre-existing; PCP-008 is in B3 — fix the YAML or normalise the check then); and `table_title` fields are stale corpus-wide but ungated.

Gates, run by me: 20/20 annexes valid; `GROUNDING_STRICT_ANCHORS=1 check_grounding.py` -> OK PCR-006 103/0, PCR-008 115/0, PCR-009 82/0, PCR-010 77/0, PCP-006/008/009/010 unchanged and OK; 2088/2088 quotes grounded across 20 annexes, exit 0, no weak anchor — N rose from 2084 to 2088 by the four added records named above, none dropped; weak_claims 0 in all 20; `git status --short` exactly the four qmd/docx/pdf, build_ground_truth.py, the four spans yaml, the four ground_truth json, and the four old pdfs in the unit; `git diff --stat outputs/` empty; make test 95; make style 24 OK / 0 FAIL.

## Documents it is about

- **PCP-006** — `pc_package/PCP-006_viral_inactivation.qmd`
- **PCP-008** — `pc_package/PCP-008_aex.qmd`
- **PCP-009** — `pc_package/PCP-009_virus_filtration.qmd`
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
