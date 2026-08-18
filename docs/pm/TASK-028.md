---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-028
status: todo
kind: annex
title: "Promote, render, re-anchor and re-ground the master report (PCMR-001)"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCMR-001"]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-028 — Promote, render, re-anchor and re-ground the master report (PCMR-001)

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/ANNEX-A-BATCH.md. Batch exposure: about 273 quotes and 49 rhetorical spans. RE-CURATE THE SPANS FIRST or build_ground_truth writes nothing for that document. THE TWO-EXTRACTOR TRAP cost round two a cycle: check_grounding.docx_text yields 'R2', build_rhetorical_annex.doc_text yields 'R²'. Row quotes survive a re-author untouched; only prose moves. READ every annex report-summary statement -- round three found two that asserted something the re-authored report no longer said, and no gate catches that.

## Acceptance criteria

- [ ] each DRAFT replaces its committed .qmd; docx and pdf rendered explicitly with the venv on PATH; check_render.py reports 0 missing glyphs on each FRESH pdf; page counts recorded
- [ ] for every document in this batch that has a rhetorical layer, its authoring/rhetorical/<DOC>.spans.yaml is re-curated against the new text and EVERY span is tested under BOTH extractors before any builder runs; `build_rhetorical_annex.py --doc <DOC>` writes the same span count as before or states the new one and drops none
- [ ] `cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py` -> 20/20 valid
- [ ] `GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py` -> N/N with 0 weak anchors, N reported against 2084 and the number of quotes re-anchored stated per document
- [ ] every registered discrepancy carried by a document in this batch is re-verified verbatim against the new text; discrepancies.yaml and DISCREPANCIES.md updated together if a wording moved
- [ ] no document outside this batch has its .qmd, .docx, .pdf or annex modified (git status does not list them); `git diff --stat outputs/` empty; make test and make style pass; weak_claims empty in all 20 annexes

**Depends on:** [[TASK-027]]

## Documents it is about

- **PCMR-001** — `pc_package/PCMR-001_master_report.qmd`

## Files it touched

- `pc_package/build_ground_truth.py`
- `authoring/rhetorical/`
- `authoring/discrepancies.yaml`
- [[DISCREPANCIES]] — `authoring/DISCREPANCIES.md`
- `pc_package/PCMR-001_master_report.qmd`
