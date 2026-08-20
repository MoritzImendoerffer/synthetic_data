---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-051
status: done
kind: annex
title: "Dispose of PCR-004 per the reading: promote attempt 2, or revert to the pre-campaign text by name; re-ground either way"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCP-004", "PCP-006", "PCP-008", "PCP-009", "PCP-010", "PCR-004", "PCR-010"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-051 — Dispose of PCR-004 per the reading: promote attempt 2, or revert to the pre-campaign text by name; re-ground either way

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

The revert target is 083bfb1, the commit the B2-old pdfs were taken from. build_ground_truth.py has moved a long way since, so the harvest region is restored by named hunks only.

## Acceptance criteria

- [x] On PASS: ANNEX-A-BATCH for one document — promote, render both formats, re-cut the 36 spans against the new text under BOTH extractors, re-anchor the harvest-region annex quotes, read every report_sections statement against the new text
- [x] On FAIL: restore pc_package/PCR-004_harvest.{qmd,docx,pdf} and authoring/rhetorical/PCR-004.spans.yaml from 083bfb1, plus the harvest-region hunks of build_ground_truth.py, by named hunks and never a whole-file checkout
- [x] either way: 20/20 valid; strict grounding N/N with N printed; 0 weak anchors; `git diff --stat outputs/` empty; make test; make style 24 OK

**Depends on:** [[TASK-050]]

## What was built

PCR-004 attempt 2 PROMOTED on the TASK-050 PASS, in the same serial pass as B3. The revert branch was not taken. ANNEX-A-BATCH.md followed, serial, for six documents in one pass (B3's five plans plus PCR-004 attempt 2), because the grounding check is corpus-wide and one boundary keeps the corpus mid-change for the shortest time. B3's pre-promotion pdfs saved as $U/B3-old-<DOC>.pdf from 083bfb1 for the sampled reading. Promoted, then rendered BOTH formats: PCR-004 33 pp, PCP-004 27, PCP-006 29, PCP-008 29, PCP-009 28, PCP-010 25; no missing glyphs on any FRESH pdf; all five plans inside the 23-31 plan band, PCR-004 above the 26-28 non-DoE report band as flagged. RHETORICAL SPANS: only PCR-004 carries a layer (the five plans carry none, which is what docs/next/rhetorical-layer-coverage.md is about). All 36 re-cut against attempt 2, tested under BOTH extractors (0 failures), builder wrote 36 spans dropping none. Four section labels changed name-only. ANNEXES: 151 quotes ungrounded after promotion, re-anchored per document with region-scoped edits. TWO BUILDER CHANGES rather than quote swaps: h_proven_acceptable_ranges restored to ROW anchors because attempt 2 renders @tbl-par again (attempt 1 had stated the ranges in prose and the builder had been changed to match); and h_param_rows dropped its '.0f' override because both documents of the pair now render the set-point with a thousands separator. TWO COLLATERAL EDITS CAUGHT AND REVERTED, both from region-scoped replacement hitting a sibling document that was not in this batch: PCR-010's AMV-3013 method quote and its scale-down equipment quote, which had acquired a doubled 'EQ-TFF-142, EQ-TFF-142'. Both restored; PCR-010 back to 77/77. REGISTERED DISCREPANCIES, per §5: D-001's registered_sentence for PCP-008 and PCP-009 no longer matched its document. Both mismatches were cosmetic and neither changed the claim — a hyphen and a curly apostrophe in PCP-008, and in PCP-009 a sentence that had been captured from the .qmd SOURCE and still contained the literal inline expression instead of the rendered 201. discrepancies.yaml and DISCREPANCIES.md updated together; all three D-001 sentences now verify present. PCP-003's mismatch is untouched and stays pre-existing, since that document is not in this batch. RESULT: 2088/2088 quotes grounded across 20 annexes under GROUNDING_STRICT_ANCHORS=1, exit 0, 0 weak anchors; 20/20 valid; weak_claims 0 in all 20; make test 95 passed; make style 24 OK; `git diff --stat outputs/` empty; only the six documents' qmd/docx/pdf, their six annexes, PCR-004's spans file, build_ground_truth.py and the two discrepancy files changed.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCP-004** — `pc_package/PCP-004_harvest.qmd`
- **PCP-006** — `pc_package/PCP-006_viral_inactivation.qmd`
- **PCP-008** — `pc_package/PCP-008_aex.qmd`
- **PCP-009** — `pc_package/PCP-009_virus_filtration.qmd`
- **PCP-010** — `pc_package/PCP-010_ufdf.qmd`
- **PCR-004** — `pc_package/PCR-004_harvest.qmd`
- **PCR-010** — `pc_package/PCR-010_ufdf.qmd`

## Files it touched

- `pc_package/PCR-004_harvest.qmd`
- `pc_package/PCR-004_harvest.docx`
- `pc_package/PCR-004_harvest.pdf`
- `authoring/rhetorical/PCR-004.spans.yaml`
- `pc_package/build_ground_truth.py`
- `pc_package/ground_truth/PCR-004.json`
