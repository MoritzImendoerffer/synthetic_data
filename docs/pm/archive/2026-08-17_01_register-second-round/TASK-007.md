---
type: pm-task
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
task: TASK-007
status: done
kind: annex
title: "Promote both drafts, render both formats, re-anchor the annexes and re-ground the corpus"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-007 — Promote both drafts, render both formats, re-anchor the annexes and re-ground the corpus

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-007.md in this work unit — numbered steps, code, commands and the output each must print. Follow it top to bottom.  THIS IS THE BOUNDARY THAT MUST CLOSE. Between TASK-005/006 and the end of this task the corpus is mid-change; after it, everything is green again.  THE REBUILD-AND-REGROUND TASK the workflow requires: no config changed, so `make data figures` is not needed and `git diff outputs/` empty is the assertion; but the documents changed, so every annex quote over changed text is re-anchored here.  WHAT BREAKS. check_grounding.py names each missing quote. The bioreactor entities are built by the 'build_' builders in build_ground_truth.py (build_params ~226, param_row_quotes ~261, build_cqas ~282 as of round one — grep for them); re-anchor by rebuilding the row from the same DataFrame the document renders (row_quotes(), table_header=rows.header), never by joining cells with a space. Prose quotes are re-anchored to the sentence that names the record, never the reverse: nothing is added to a document after authoring.  THE SPANS TRAP from round one: build_rhetorical_spans raises SystemExit when a span is missing, so the first rebuild after a re-author writes NOTHING, including PCP-003.json — a grounding count taken then measures stale files. Re-curate the spans yaml first, then rebuild, then count.  THE PDF TRAP: check_render.py --render renders only the docx and glyph-checks the pdf already on disk. Render both pdfs explicitly.  BUDGET about 40 re-anchored spans per document (round one: 80 across two, 34 of them the curated layer).

## Acceptance criteria

- [x] both DRAFTs replace their committed .qmd; `quarto render --to docx` and `--to pdf` run explicitly for both, and `check_render.py` reports 0 missing glyphs on the FRESH pdfs
- [x] `cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py` reports 20/20 annexes valid
- [x] `GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py` passes with 0 weak anchors, and the completion note reports the new total against 2084/2084 and how many spans were re-anchored per document (round one: 24 and 56)
- [x] authoring/rhetorical/PCR-003.spans.yaml is re-curated against the new text and `uv run python authoring/build_rhetorical_annex.py --doc PCR-003` writes 35 spans (or the new count, stated) and drops none
- [x] D-001 and D-002 stand: the registered_sentence fields in authoring/discrepancies.yaml are re-verified against the new text and DISCREPANCIES.md quotes the new wording
- [x] the guide's ✗ examples that quote round-one PCP-003/PCR-003 text are labelled with the date they stood (already required by TASK-002), so no ✗ block claims to quote live text
- [x] `git diff outputs/` is empty — no number moved, so no dataset may change
- [x] `make test PY="uv run python"` passes; `make style PY="uv run python"` passes 20/20
- [x] the two annexes' weak_claims lists are still empty

**Depends on:** [[TASK-005]], [[TASK-006]]

## What was built

The boundary is closed: both drafts promoted, both formats rendered, every annex re-anchored, the corpus green again.

GROUNDING: 2084/2084 quotes grounded across 20 annexes with GROUNDING_STRICT_ANCHORS=1 and zero weak anchors -- the same total as before the round, which is the point: no quote was dropped to make the count work. PCP-003 105 quotes and PCR-003 177, both 0 ungrounded. 44 quote instances were re-anchored (21 in PCP-003, 23 in PCR-003) from 37 edited strings in build_ground_truth.py; round one needed 80 across the pair. Every table-row quote still grounded untouched, because the row builders rebuild the row from the DataFrame the document renders -- only prose quotes moved. Nothing was edited in either document to suit a stale quote.

RHETORICAL LAYER: 35 spans, none dropped, none added. 33 of the 35 needed a new quote; RS-08 and RS-B03 still grounded on the re-authored text. RS-F02 moved from 'Screening: factor effects' to 'Response-surface models' because the screening deferral to Appendix C now carries an inline response count and the response-surface one does not -- same role, same target, a quote that a seed change cannot break. Two section titles were updated where the headings moved (DEV-003-01 and DEV-003-02 now say 'dissolved carbon dioxide' and 'nutrient feed-1'). All 11 claim<-justification edges and both coreference edges still resolve.

A TRAP WORTH RECORDING, and it cost a cycle: the two extractors disagree on superscripts. build_rhetorical_annex.doc_text reads word/document.xml directly and yields 'R2'; check_grounding.docx_text yields 'R2' without the superscript. A quote containing the character therefore grounds in one and fails in the other, which is exactly what happened to RS-J02 ('Predicted R2 is negative for every response') -- it passed my check_grounding test and failed the builder. RS-J02 and RS-H01 were re-cut onto symbol-free sentences and every span is now tested against BOTH extractors before the builder runs. Anyone curating spans should do the same; testing one extractor is not testing the gate.

D-001 AND D-002 BOTH SURVIVE. D-002's registered sentence is verbatim in the re-authored PCR-003, unqualified, in the introduction where the assignment places it, and 'leached Protein A' does not occur anywhere in the document, so nothing reconciles it. D-001's wording moved with the re-author, so discrepancies.yaml now carries the live sentence ('...holds the other factors at the set-points in @tbl-params...'), verified verbatim against the .qmd source, and DISCREPANCIES.md quotes the new wording and records the re-verification date. What each item claims is unchanged: the at-set-point commitment and the unqualified absolute.

RENDERS: both formats rendered explicitly with the venv on PATH. PCP-003 29 pages (round one 30), PCR-003 59 pages (round one 51). check_render reports 'no missing glyphs' on both FRESH pdfs and the style gate OK on both.

GATES: validate_annex 20/20 valid. weak_claims 0 in both annexes, so main is still fully grounded. `git diff outputs/` is empty -- no config changed and no dataset moved. `make test PY="uv run python"` 88 passed. `make style PY="uv run python"` 24 OK lines, 0 FAIL.

git status lists exactly the twelve files the procedure permits: the two .qmd, their .docx and .pdf, build_ground_truth.py, the two annex JSONs, PCR-003.spans.yaml, discrepancies.yaml and DISCREPANCIES.md. No other rendered document and no other annex was touched, so no restore by name was needed.

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
