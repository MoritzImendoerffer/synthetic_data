---
type: pm-task
epic: 2026-08-16_01_register-from-four-sources
sprint: 2026-08-16_01_register-from-four-sources
task: TASK-008
status: done
kind: annex
title: "Promote both pilot documents, re-anchor their annexes, and fix what the rewrite falsified"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCP-006", "PCP-008", "PCP-009", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-16_01_register-from-four-sources/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-008 — Promote both pilot documents, re-anchor their annexes, and fix what the rewrite falsified

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

THIS IS THE BOUNDARY THAT MUST CLOSE. Between TASK-007 and the end of this task the corpus is mid-change; after it, everything is green again. Two documents now, not one.

WHAT BREAKS IN THE ANNEXES. Re-authoring invalidates every annex quote taken over changed text, and PCR-003 is the largest annex in the corpus. check_grounding.py names each one. The bioreactor entities are built by the 'build_' prefixed builders in build_ground_truth.py - build_params at about line 226, param_row_quotes at 261, build_cqas at 282. Re-anchor by rebuilding the row from the same DataFrame the document renders, using row_quotes(df, keys), and pass table_header=rows.header alongside it. The caption stays in table_title and is never the anchor.

THE RULES THAT BITE HERE. Anchor every parameter and attribute record on its own rendered row, never on a caption or a bare label. Keep prose reuse at or below MAX_PROSE_REUSE = 3; MAX_ROW_REUSE = 8 applies to rows because a row carries both ends of its relation by construction. Fix a weak anchor by finding the span that names the record, NEVER by raising a threshold. Build row quotes with row_quotes() or _join_cells(), never by joining cells with a space - the cell boundary reads as ' | '. NEVER edit a document to suit a stale quote.

WHAT THE REWRITE FALSIFIES OUTSIDE THE ANNEXES, and this is easy to miss. Four of the seven worked corrections added in TASK-003 and TASK-005 quote text that these two documents will no longer contain:
  WRITING_GUIDE 2c shape 1 - PCR-003, the acidic-variants sentence
  WRITING_GUIDE 2d shape 2 - PCP-003, the re-issued-matrix sentence
  WRITING_GUIDE 2d shape 3 - PCR-003, the afucosylation null result
  WRITING_GUIDE 2d shape 4 - PCR-003, the First/Second/Third/Fourth run
They stay in the guide, because they are real machine-register prose and that is what makes them good teaching material. What changes is the label: 'from PCR-003, Quality attributes in scope' becomes 'from PCR-003 as it stood before 2026-08-17'. Leaving them in the present tense makes the guide assert something false about the corpus, which is the exact class of defect this epic keeps finding.

discrepancies.yaml's registered_sentence for PCP-003 and PCR-003 has the same problem and it is worse, because the brief prints it as 'the sentence this document currently carries'. Re-verify both against the new text and update them. The other three (PCP-006, PCP-008, PCP-009) are untouched by this pilot and must still verify.

The previous total was 2084/2084 quotes across 20 annexes. Report the new total; it will move, and that is expected.

FROM TASK-007. Both drafts exist and gate clean: pc_package/PCP-003_bioreactor.DRAFT.qmd and pc_package/PCR-003_bioreactor.DRAFT.qmd. Their .docx and .pdf are gitignored. The sentences you must re-verify into discrepancies.yaml are, verbatim from the new text:
  D-001, PCP-003 section 8: 'The first holds the other factors at their set-points and scans the parameter of interest across the full characterization range, evaluating the fitted response-surface model on a grid of `{python} par_grid` points.' Note the inline expression inside it, so the registered_sentence must be taken from the RENDERED text, not from the .qmd source.
  D-002, PCR-003 section 1.1: 'The production bioreactor is the only step of the drug substance process at which product quality attributes are formed.'

## Acceptance criteria

- [x] both DRAFTs replace their committed .qmd and render to .docx and .pdf with no errors
- [x] cd pc_package && build_ground_truth.py && validate_annex.py reports 20/20 annexes valid
- [x] GROUNDING_STRICT_ANCHORS=1 check_grounding.py passes with zero weak anchors, and the new total is reported against the previous 2084/2084
- [x] D-002 still stands: the ProcessStep.description for step:production_bioreactor still carries the absolute in BOTH PCR-003.json and PCP-003.json
- [x] the four worked corrections in WRITING_GUIDE that quote PCR-003 and PCP-003 are relabelled as superseded prose, since they no longer quote live text
- [x] the registered_sentence fields for PCP-003 and PCR-003 in discrepancies.yaml are re-verified against the new text and updated to the new wording
- [x] make test PY="uv run python" passes with 85 tests
- [x] git diff outputs/ is empty: no number moved, so no dataset may change
- [x] make style PY="uv run python" passes over all 20 documents

**Depends on:** [[TASK-007]]

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCP-006** — `pc_package/PCP-006_viral_inactivation.qmd`
- **PCP-008** — `pc_package/PCP-008_aex.qmd`
- **PCP-009** — `pc_package/PCP-009_virus_filtration.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `pc_package/PCP-003_bioreactor.qmd`
- `pc_package/PCR-003_bioreactor.qmd`
- `pc_package/build_ground_truth.py`
- [[WRITING_GUIDE]] — `authoring/WRITING_GUIDE.md`
- `authoring/discrepancies.yaml`
