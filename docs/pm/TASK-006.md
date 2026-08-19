---
type: pm-task
epic: 2026-08-19_01_fourth-round-one-document
sprint: 2026-08-19_01_fourth-round-one-document
task: TASK-006
status: todo
kind: annex
title: "Promote the new PCR-007: render, re-cut its 33 spans, re-anchor its annex, re-ground the corpus"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-007"]
---

> [!warning] Generated from `.claude/work/2026-08-19_01_fourth-round-one-document/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-006 — Promote the new PCR-007: render, re-cut its 33 spans, re-anchor its annex, re-ground the corpus

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

Serial, no overlap with anything else. The re-anchoring is the round's cost (Track D budget: 21–44 quotes; the whole rhetorical layer). Re-cut spans FIRST (ANNEX-A-BATCH §3), then rebuild and read the misses (§4). A mechanistic_warrant span is now held to content: it must name a cause, per RHETORICAL_ANNEX.md as rewritten on 2026-08-19.

## Acceptance criteria

- [ ] runs ONLY on D6 = PASS; follows ../2026-08-18_02_register-track-d/procedures/ANNEX-A-BATCH.md for the one document: `git mv -f` DRAFT -> PCR-007_cex.qmd, both formats rendered explicitly (`quarto render … --to docx && --to pdf` with the venv on PATH), check_render reports no missing glyph on the FRESH pdf, page count recorded
- [ ] authoring/rhetorical/PCR-007.spans.yaml re-curated wholesale against the new text: still 33 spans (or the count stated with the reason), every quote tested under BOTH extractors (check_grounding.docx_text -> 'R2', build_rhetorical_annex.doc_text -> 'R²') before the builder runs; every mechanistic_warrant span names a physical cause (RHETORICAL_ANNEX.md's criterion) — a category-label span is not labelled mechanistic_warrant
- [ ] the _cx_* region of build_ground_truth.py re-anchored: prose quotes moved to the sentence that names the same record; every table-row quote left to rebuild itself; every report-summary statement READ against the new text and rewritten where the report no longer says it (round three found two); registered discrepancies: none for PCR-007, stated
- [ ] `cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py` -> 20/20 annexes valid; `GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py` -> N/N quotes grounded across 20 annexes with N printed (2084 today; a re-anchor may add or merge, never drop a record silently — any change in N explained), 0 weak anchors
- [ ] `git status --short pc_package/` shows exactly PCR-007_cex.qmd, .docx, .pdf, ground_truth/PCR-007.json (and build_ground_truth.py, the spans yaml); no other rendered pair moved; `git diff --stat outputs/` empty
- [ ] make style 24 OK / 0 FAIL; make test unchanged

**Depends on:** [[TASK-004]]

## Documents it is about

- **PCR-007** — `pc_package/PCR-007_cex.qmd`

## Files it touched

- `pc_package/PCR-007_cex.qmd`
- `pc_package/PCR-007_cex.docx`
- `pc_package/PCR-007_cex.pdf`
- `authoring/rhetorical/PCR-007.spans.yaml`
- `pc_package/build_ground_truth.py`
- `pc_package/ground_truth/PCR-007.json`
