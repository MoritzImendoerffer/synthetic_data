---
type: pm-task
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
task: TASK-007
status: todo
kind: annex
title: "Promote both drafts, render both formats, re-anchor the annexes and re-ground the corpus"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-007 — Promote both drafts, render both formats, re-anchor the annexes and re-ground the corpus

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-007.md in this work unit — numbered steps, code, commands and the output each must print. Follow it top to bottom.  THIS IS THE BOUNDARY THAT MUST CLOSE. Between TASK-005/006 and the end of this task the corpus is mid-change; after it, everything is green again.  THE REBUILD-AND-REGROUND TASK the workflow requires: no config changed, so `make data figures` is not needed and `git diff outputs/` empty is the assertion; but the documents changed, so every annex quote over changed text is re-anchored here.  WHAT BREAKS. check_grounding.py names each missing quote. The bioreactor entities are built by the 'build_' builders in build_ground_truth.py (build_params ~226, param_row_quotes ~261, build_cqas ~282 as of round one — grep for them); re-anchor by rebuilding the row from the same DataFrame the document renders (row_quotes(), table_header=rows.header), never by joining cells with a space. Prose quotes are re-anchored to the sentence that names the record, never the reverse: nothing is added to a document after authoring.  THE SPANS TRAP from round one: build_rhetorical_spans raises SystemExit when a span is missing, so the first rebuild after a re-author writes NOTHING, including PCP-003.json — a grounding count taken then measures stale files. Re-curate the spans yaml first, then rebuild, then count.  THE PDF TRAP: check_render.py --render renders only the docx and glyph-checks the pdf already on disk. Render both pdfs explicitly.  BUDGET about 40 re-anchored spans per document (round one: 80 across two, 34 of them the curated layer).

## Acceptance criteria

- [ ] both DRAFTs replace their committed .qmd; `quarto render --to docx` and `--to pdf` run explicitly for both, and `check_render.py` reports 0 missing glyphs on the FRESH pdfs
- [ ] `cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py` reports 20/20 annexes valid
- [ ] `GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py` passes with 0 weak anchors, and the completion note reports the new total against 2084/2084 and how many spans were re-anchored per document (round one: 24 and 56)
- [ ] authoring/rhetorical/PCR-003.spans.yaml is re-curated against the new text and `uv run python authoring/build_rhetorical_annex.py --doc PCR-003` writes 35 spans (or the new count, stated) and drops none
- [ ] D-001 and D-002 stand: the registered_sentence fields in authoring/discrepancies.yaml are re-verified against the new text and DISCREPANCIES.md quotes the new wording
- [ ] the guide's ✗ examples that quote round-one PCP-003/PCR-003 text are labelled with the date they stood (already required by TASK-002), so no ✗ block claims to quote live text
- [ ] `git diff outputs/` is empty — no number moved, so no dataset may change
- [ ] `make test PY="uv run python"` passes; `make style PY="uv run python"` passes 20/20
- [ ] the two annexes' weak_claims lists are still empty

**Depends on:** [[TASK-005]], [[TASK-006]]

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `pc_package/PCP-003_bioreactor.qmd`
- `pc_package/PCR-003_bioreactor.qmd`
- `pc_package/build_ground_truth.py`
- `authoring/rhetorical/PCR-003.spans.yaml`
- `authoring/discrepancies.yaml`
- [[DISCREPANCIES]] — `authoring/DISCREPANCIES.md`
- [[WRITING_GUIDE]] — `authoring/WRITING_GUIDE.md`
