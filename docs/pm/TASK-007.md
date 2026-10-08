---
type: pm-task
epic: 2026-10-08_01_rev2-campaign
sprint: 2026-10-08_01_rev2-campaign
task: TASK-007
status: done
kind: mechanism
title: "ctable(): one spec -> HTML table (DOCX merged cells) + raw LaTeX twin (PDF), crossref, footnotes; grounding reads it"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
---

> [!warning] Generated from `.claude/work/2026-10-08_01_rev2-campaign/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-007 — ctable(): one spec -> HTML table (DOCX merged cells) + raw LaTeX twin (PDF), crossref, footnotes; grounding reads it

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Acceptance criteria

- [x] test doc renders to docx and pdf; docx has gridSpan and vMerge; pdf page image checked by eye (multirow, footnote row)
- [x] @tbl- crossref resolves in both formats
- [x] ctable_row_quotes() returns rows that check_grounding finds verbatim (test)
- [x] check_style ignores raw html/latex blocks (test)

## What was built

pc_package/ctable.py: CTable/C, HTML twin (DOCX gridSpan/vMerge) + raw LaTeX twin (booktabs/grid, multirow, cmidrule, footnote rows), inside a {#tbl-} crossref div; rows()/header_rows()/notes_text() reproduce docx_text. pc_package/_tables.tex for the PDF header. tests/test_ctable.py 4 pass incl. a real DOCX render of the owner's two messy tables, every row grounding. Raw blocks are emitted at render time from python chunks, so check_style never sees them.

## Files it touched

- `pc_package/_pcpkg.py`
- `pc_package/check_grounding.py`
- `pc_package/build_ground_truth.py`
- `authoring/check_style.py`
- `tests/test_ctable.py`
