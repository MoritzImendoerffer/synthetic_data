---
type: pm-task
epic: 2026-08-19_01_fourth-round-one-document
sprint: 2026-08-19_01_fourth-round-one-document
task: TASK-006
status: done
kind: annex
title: "Promote the new PCR-007: render, re-cut its 33 spans, re-anchor its annex, re-ground the corpus"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-005", "PCR-007", "PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-19_01_fourth-round-one-document/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-006 — Promote the new PCR-007: render, re-cut its 33 spans, re-anchor its annex, re-ground the corpus

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Serial, no overlap with anything else. The re-anchoring is the round's cost (Track D budget: 21–44 quotes; the whole rhetorical layer). Re-cut spans FIRST (ANNEX-A-BATCH §3), then rebuild and read the misses (§4). A mechanistic_warrant span is now held to content: it must name a cause, per RHETORICAL_ANNEX.md as rewritten on 2026-08-19.

## Acceptance criteria

- [x] runs ONLY on D6 = PASS; follows ../2026-08-18_02_register-track-d/procedures/ANNEX-A-BATCH.md for the one document: `git mv -f` DRAFT -> PCR-007_cex.qmd, both formats rendered explicitly (`quarto render … --to docx && --to pdf` with the venv on PATH), check_render reports no missing glyph on the FRESH pdf, page count recorded
- [x] authoring/rhetorical/PCR-007.spans.yaml re-curated wholesale against the new text: still 33 spans (or the count stated with the reason), every quote tested under BOTH extractors (check_grounding.docx_text -> 'R2', build_rhetorical_annex.doc_text -> 'R²') before the builder runs; every mechanistic_warrant span names a physical cause (RHETORICAL_ANNEX.md's criterion) — a category-label span is not labelled mechanistic_warrant
- [x] the _cx_* region of build_ground_truth.py re-anchored: prose quotes moved to the sentence that names the same record; every table-row quote left to rebuild itself; every report-summary statement READ against the new text and rewritten where the report no longer says it (round three found two); registered discrepancies: none for PCR-007, stated
- [x] `cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py` -> 20/20 annexes valid; `GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py` -> N/N quotes grounded across 20 annexes with N printed (2084 today; a re-anchor may add or merge, never drop a record silently — any change in N explained), 0 weak anchors
- [x] `git status --short pc_package/` shows exactly PCR-007_cex.qmd, .docx, .pdf, ground_truth/PCR-007.json (and build_ground_truth.py, the spans yaml); no other rendered pair moved; `git diff --stat outputs/` empty
- [x] make style 24 OK / 0 FAIL; make test unchanged

**Depends on:** [[TASK-004]]

## What was built

Promoted 2026-08-19 per ANNEX-A-BATCH.md for one document. `git mv -f` DRAFT -> pc_package/PCR-007_cex.qmd; both formats rendered explicitly with the venv on PATH; check_render: 'no missing glyphs' on the fresh pdf; 50 pages (was 51).

Rhetorical layer (fresh agent, verified by me): authoring/rhetorical/PCR-007.spans.yaml re-curated wholesale — 33 spans kept, none dropped, no role changed, no edge dropped; all 33 quotes new (no old quote survived the re-author); 10 spans changed section (R00/R03/R04/R05/R17 because the argument moved — the 'nothing downstream removes it' stake to §2.2, the in-process-limit argument to §7.1, the PCR-005/PCR-008 credit to §10; R19–R21 because §7 is now subdivided; R29/R30 track the renamed deviation subsections). `build_rhetorical_annex.py --doc PCR-007` -> 'OK wrote authoring/out/PCR-007.rhetorical.json', 33 spans · 4 claim<-justification edges · 1 coreference edge; the two-extractor test prints only 'checked', plus a duplicate-quote assertion (none). The two mechanistic_warrant spans name a physical cause with a direction (R07 ionic-strength screening of the sulfonate-ligand/acidic-HCP attraction vs the more strongly held antibody; R08 the extra weakly bound HCP a heavy load carries into the wash, hence the negative interaction).

Annex (second fresh agent, verified by me): 31 PCR-007 prose quotes re-anchored in the _cx_* region of build_ground_truth.py — cx_equipment 1, CXMETHOD_QUOTE[True] 4, cx_studies 4, cx_design_spaces 1, cx_report_sections 10, cx_assertions 11; every table-row quote rebuilt itself (param_rows / cqa_rows / par_rows), no hand-typed row, no weak anchor. All ten report_sections statements READ against the new report and rewritten where it no longer says what they asserted (st2 no longer 'no other step changes the attribute' — the new §8 says aggregate is formed in the bioreactor and raised by the low-pH hold; st7 the old 'corner outside the operating region' claim is gone; st9 was duplicating st2 and now carries the capability result). Assertions rewritten to the new report's claims (protein load carries the largest effect on both cleared attributes; the flow-rate null anchored on §4.4; the aggregate acceptance criterion off a caption fragment onto §7.1 prose; the three cleared attributes off one shared clause). Two annex-data corrections in the same region: ds:cex gains attr:hcp (the new §6 says HCP rejects part of the region on its own) and its definition no longer says the worst corner is all four at their upper edges; and the PAR builder's pool-HCP rows carry the parameter unit like every other row (_par_interval()), with the stale out_of_schema_notes, docstring and two dead constants corrected/removed. Left alone, noted for the next re-author: CX_CQA_QUOTE[True] still holds old PCR-007 strings but is dead (cx_cqas anchors on cqa_rows).

Gates, run by me: `build_ground_truth.py && validate_annex.py` -> 20/20 annexes valid; `GROUNDING_STRICT_ANCHORS=1 check_grounding.py` -> OK PCR-007: 110 quotes, 0 ungrounded; 2084/2084 quotes grounded across 20 annexes, exit 0, no weak anchor; weak_claims 0 in all 20; `git status --short` -> exactly authoring/rhetorical/PCR-007.spans.yaml, pc_package/PCR-007_cex.{qmd,docx,pdf}, build_ground_truth.py, ground_truth/PCR-007.json; `git diff --stat outputs/` empty; make test 95 passed; make style 24 OK / 0 FAIL. PCR-007 carries no registered discrepancy (stated). N unchanged at 2084: no record added or merged.

## Documents it is about

- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`
- **PCR-007** — `pc_package/PCR-007_cex.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- `pc_package/PCR-007_cex.qmd`
- `pc_package/PCR-007_cex.docx`
- `pc_package/PCR-007_cex.pdf`
- `authoring/rhetorical/PCR-007.spans.yaml`
- `pc_package/build_ground_truth.py`
- `pc_package/ground_truth/PCR-007.json`
