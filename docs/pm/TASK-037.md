---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-037
status: done
kind: annex
title: "Promote batch B5 (PTP-001, PCMP-001, RA-001, PCMR-001): render, re-cut spans, re-anchor, re-ground"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCMP-001", "PCMR-001", "PCP-005", "PCR-005", "PTP-001", "RA-001"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-037 — Promote batch B5 (PTP-001, PCMP-001, RA-001, PCMR-001): render, re-cut spans, re-anchor, re-ground

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

B5: 4 documents, 440 quotes, 49 spans. Serial: no overlap with authoring or another annex task.

## Acceptance criteria

- [x] ANNEX-A-BATCH.md (2026-08-18_02 unit) for the batch, SERIAL: promote each DRAFT, render both formats explicitly, no missing glyph on each FRESH pdf, page counts recorded; the OLD pdf of every document in the batch saved first as `$U/B5-old-<DOC>.pdf` (for the sampled reading)
- [x] rhetorical spans re-cut FIRST for every document with a layer (PCMR-001 49), tested under BOTH extractors, builder writes with the count (dropped none, or explained); every mechanistic_warrant span names a physical cause
- [x] annex quotes re-anchored in each document's region (440 quotes across the batch; table rows rebuild themselves); every report_sections statement READ against the new text and rewritten where false
- [x] no registered discrepancy in this batch, stated
- [x] 20/20 valid; strict grounding N/N with N printed and any change explained; 0 weak anchors; weak_claims 0 in all 20; `git status --short` only this batch's files; `git diff --stat outputs/` empty; make test; make style 24 OK

**Depends on:** [[TASK-033]], [[TASK-034]], [[TASK-035]], [[TASK-036]]

## What was built

Batch B5 promoted: PTP-001, PCMP-001, RA-001, PCMR-001, serial. Old pdfs saved first as B5-old-*.pdf (24, 25, 30, 34 pp). PROMOTED ONTO THE SHIPPED FILENAMES, not the plan's: the files list named <DOC>_None.qmd for all four, inherited from DOC_REGISTRY returning key=None for every corpus-level document, and promoting there would have created four NEW files for a corpus of 24 and left build_ground_truth.py pointing at the old .docx so grounding would have passed against stale text while the new documents shipped ungrounded. Corrected in state.json before promotion, with the reason. Rendered both formats explicitly: PTP-001 26 pp (was 24), PCMP-001 23 (was 25), RA-001 28 (was 30), PCMR-001 38 (was 34); no missing glyphs on any FRESH pdf; corpus still 20 .qmd, no _None leftovers. SUBTITLE REGRESSION STOPPED: the template builds 'A-Mab Drug Substance — __UO_TITLE__ — __DOC__' and UO_TITLE IS 'A-Mab Drug Substance' for these four, so it doubles. PCMR-001's author caught it; the other three had not. Shipped PTP-001, PCMP-001 and PCMR-001 already carried the correct single form, so promoting as drafted would have REGRESSED two shipped documents. De-duplicated all three before promotion, which also fixes shipped RA-001's long-standing duplicate. Root cause is the template, recorded not fixed. RHETORICAL SPANS: all 32 of PCMR-001's were ungrounded after the re-author (0/32) and every one was re-cut against the new text and tested under BOTH extractors before the builder ran; 32/32 written, none dropped, both mechanistic_warrant spans name a physical cause. The plan's note said 49 spans; the file has 32. ANNEX RE-ANCHORING, 342 quotes: PTP-001 27, PCMP-001 33, RA-001 168, PCMR-001 114. The bulk were table-row quotes that failed because each re-authored document builds its own derived tables: RA-001's per-step failure-mode table gained a 'Potential effect' column (one fix cleared 148), PCMP-001's register moved 'Set by' to the end as 'Formed or set at' (one fix cleared 20), PCMR-001's capability table kept the raw 'two_sided' spelling with Cpk to ONE decimal AND a thousands separator, its viral table dropped Mechanism and Report, its deviation table dropped Step and Root cause. STRUCTURAL CHANGES, not re-wording: PTP-001's gap register went from 6 gaps to 7 with different content and was rebuilt entirely (two gap_area values had to be mapped onto the schema's closed literal set). STATEMENTS READ, NOT JUST RE-ANCHORED: every report_sections statement of all four documents was read back against the new text and most were rewritten, because the re-authors dropped concepts the annex asserted — PCMP-001 lost the 'intermediate pool is not the drug substance' framing, the three-procedure taxonomy and the assurance-margin/break-even contrast; RA-001 folded its 'justified univariate' parameter into the univariate count (22+15, not 22+14+1) and dropped its own prospectivity claim; PTP-001 no longer says none of its gaps is closed by the plan. ONE ASSERTION REMOVED: PCMP-001 carried a Protein A in-process limit for host cell protein WITH ITS VALUE, and the re-authored plan states the rule and leaves every value to the step's own documents, so the assertion had nothing to attest; PCP-005 and PCR-005 carry the same limit in their own annexes. FINAL: 2089/2089 quotes grounded across 20 annexes under GROUNDING_STRICT_ANCHORS=1, exit 0, 0 weak anchors; 20/20 valid; weak_claims 0 in all 20; git diff --stat outputs/ empty; make test 95 passed; make style 24 OK; git status only this batch's files.

## Documents it is about

- **PCMP-001** — `pc_package/PCMP-001_master_plan.qmd`
- **PCMR-001** — `pc_package/PCMR-001_master_report.qmd`
- **PCP-005** — `pc_package/PCP-005_protein_a.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`
- **PTP-001** — `pc_package/PTP-001_transfer.qmd`
- **RA-001** — `pc_package/RA-001_risk_assessment.qmd`

## Files it touched

- `pc_package/PTP-001_transfer.qmd`
- `pc_package/PCMP-001_master_plan.qmd`
- `pc_package/RA-001_risk_assessment.qmd`
- `pc_package/PCMR-001_master_report.qmd`
- `pc_package/build_ground_truth.py`
- `authoring/rhetorical/PCMR-001.spans.yaml`
- `pc_package/ground_truth/PTP-001.json`
- `pc_package/ground_truth/PCMP-001.json`
- `pc_package/ground_truth/RA-001.json`
- `pc_package/ground_truth/PCMR-001.json`
