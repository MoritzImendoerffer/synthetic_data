---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-017
status: done
kind: annex
title: "Promote batch B2 (PCR-004, PCR-003, PCR-005): render, re-cut spans, re-anchor, re-ground"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCP-005", "PCP-008", "PCP-009", "PCR-003", "PCR-004", "PCR-005", "PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-017 — Promote batch B2 (PCR-004, PCR-003, PCR-005): render, re-cut spans, re-anchor, re-ground

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

B2: 3 documents, 291 quotes, 110 spans. Serial: no overlap with authoring or another annex task.

## Acceptance criteria

- [x] ANNEX-A-BATCH.md (2026-08-18_02 unit) for the batch, SERIAL: promote each DRAFT, render both formats explicitly, no missing glyph on each FRESH pdf, page counts recorded; the OLD pdf of every document in the batch saved first as `$U/B2-old-<DOC>.pdf` (for the sampled reading)
- [x] rhetorical spans re-cut FIRST for every document with a layer (PCR-004 36, PCR-003 35, PCR-005 39), tested under BOTH extractors, builder writes with the count (dropped none, or explained); every mechanistic_warrant span names a physical cause
- [x] annex quotes re-anchored in each document's region (291 quotes across the batch; table rows rebuild themselves); every report_sections statement READ against the new text and rewritten where false
- [x] registered discrepancies PCR-003 (D-002): registered_sentence present in the new docx per ANNEX-A-BATCH §5; `discrepancies.yaml` and `DISCREPANCIES.md` updated together if the wording moved, the claim unchanged
- [x] 20/20 valid; strict grounding N/N with N printed and any change explained; 0 weak anchors; weak_claims 0 in all 20; `git status --short` only this batch's files; `git diff --stat outputs/` empty; make test; make style 24 OK

**Depends on:** [[TASK-014]], [[TASK-015]], [[TASK-016]]

## What was built

Batch B2 promoted (PCR-004, PCR-003, PCR-005). ANNEX-A-BATCH.md followed, serial, for four documents at once (B2's three plus PCR-008 attempt 3), because the grounding check is corpus-wide and a single boundary keeps the corpus mid-change for the shortest time. Old pdfs saved first as $U/B2-old-<DOC>.pdf from 083bfb1. Promoted, then rendered BOTH formats explicitly: PCR-004 31 pp, PCR-003 55 pp, PCR-005 47 pp, PCR-008 53 pp, no missing glyphs on any FRESH pdf. RHETORICAL SPANS RE-CUT FIRST, all 135 (PCR-004 36, PCR-005 39, PCR-003 35, PCR-008 25): every previous quote failed against the re-authored text, so every one was re-cut, tested under BOTH extractors (0 failures) and the builder wrote each layer with its full count, dropping none. Nine section labels changed name and three PCR-004 spans moved section, each recorded in the file header with the reason. One error was caught by the both-extractor test: RS-P01 had been given a sentence from PCR-005, not PCR-003. ANNEXES: 113 quotes ungrounded after promotion, all in the four re-authored documents; table-row quotes survived untouched as the procedure predicts, and every failure was prose. All re-anchored in build_ground_truth.py, scoped to each document's region. PCR-004's h_proven_acceptable_ranges was rewritten: the re-authored report renders no @tbl-par at all, so the three PAR records now anchor on the §7 sentence that names each parameter. THREE report_sections STATEMENTS WERE FALSE against the new text and no gate catches that — PCR-005 claimed 'all 47 pools assayed met the 5 ppm criterion', which the re-authored report never says (it reports 2.87 ppm at the set-point against 5 ppm); PCR-004 claimed 'No designed experiment was executed at this step', which is no longer true of a report with a univariate characterization design; and one PCR-004 statement had been overwritten by a scoped replacement. All three rewritten to what the documents say. One collateral edit was caught and reverted: a PCP-005 statement in the shared 1508-2264 region. RESULT: 2085/2085 quotes grounded across 20 annexes under GROUNDING_STRICT_ANCHORS=1, 0 weak anchors; 20/20 valid; weak_claims 0 in all 20. D-002's registered_sentence verified present in the new PCR-003 docx; D-001 (PCR-008) carries no registered_sentence by design and was verified in substance. make test 95 passed; make style 24 OK; `git diff --stat outputs/` empty; only the four documents' qmd/docx/pdf, their four annexes, their four spans files and build_ground_truth.py changed. PRE-EXISTING AND NOT CAUSED HERE: PCP-003, PCP-008 and PCP-009 report a registered_sentence that is absent from their rendered docx. Those documents were not touched by this batch and their files are unchanged, so the mismatch predates it. Recorded for the results page.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCP-005** — `pc_package/PCP-005_protein_a.qmd`
- **PCP-008** — `pc_package/PCP-008_aex.qmd`
- **PCP-009** — `pc_package/PCP-009_virus_filtration.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-004** — `pc_package/PCR-004_harvest.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`

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
