---
type: pm-task
epic: 2026-08-18_01_register-third-round
sprint: 2026-08-18_01_register-third-round
task: TASK-005
status: done
kind: annex
title: "Promote the draft, render both formats, re-anchor the PCR-003 annex and spans, and re-ground the corpus"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-18_01_register-third-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-005 — Promote the draft, render both formats, re-anchor the PCR-003 annex and spans, and re-ground the corpus

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-005.md — the previous unit's TASK-007 procedure for one document. THIS IS THE BOUNDARY THAT MUST CLOSE. RE-CURATE THE SPANS FIRST or build_ground_truth writes nothing. THE TWO-EXTRACTOR TRAP is recorded in HANDOFF and cost a cycle in round two: test every span under both before the builder; a span containing 'R²' passes one and fails the other. Row quotes survive a re-author untouched (round two: every table-row quote held); only prose quotes move. Re-anchor to the sentence in the NEW text that names the record; never edit the document to fit a quote. Only PCR-003's builder strings change; the plan's (', and PCP-003 …' branches, ' if report else') stay. If git status shows PCP-003.docx/.pdf or any other annex modified, a full make corpus ran — restore each by NAME.

## Acceptance criteria

- [x] the DRAFT replaces pc_package/PCR-003_bioreactor.qmd; docx and pdf rendered explicitly; check_render.py reports 0 missing glyphs on the FRESH pdf; page count recorded
- [x] authoring/rhetorical/PCR-003.spans.yaml re-curated against the new text; every span tested against BOTH extractors (build_rhetorical_annex.doc_text yields 'R²', check_grounding.docx_text yields 'R2') before the builder runs; `uv run python authoring/build_rhetorical_annex.py --doc PCR-003 --file pc_package/PCR-003_bioreactor.docx` writes 35 spans (or the new count, stated) and drops none
- [x] `cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py` → 20/20; `GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py` → N/N with 0 weak anchors, N reported against 2084 and the number of PCR-003 quotes re-anchored stated (round two: 23 quotes, 33 spans)
- [x] D-002's registered_sentence re-verified verbatim against the new .qmd; DISCREPANCIES.md quotes the new wording if it moved; 'leached Protein A' does not occur in the report
- [x] PCP-003's annex and rendered files are byte-identical to HEAD (git status does not list them); `git diff --stat outputs/` empty; `make test` and `make style` pass; both annexes' weak_claims still empty

**Depends on:** [[TASK-004]]

## What was built

PCR-003 promoted, rendered, re-anchored and re-grounded. The boundary is closed: 2084/2084 quotes grounded across 20 annexes, strict anchors, 0 weak anchors, exit 0. The same total as before and as round two, which is the point -- no quote was dropped to make the count come out.

PROMOTED AND RENDERED. The DRAFT replaced pc_package/PCR-003_bioreactor.qmd (git mv, so the file history follows), and the three *.DRAFT.* files are gone from the tree. Both formats rendered explicitly with the venv on PATH: docx OK, pdf OK, 56 pages against round two's 59. check_render.py on the FRESH pdf: 'OK    PCR-003_bioreactor.pdf: no missing glyphs', all chunks exec, all inline expressions eval, 0 <<NEEDS:>>, register OK, exit 0. 'DRAFT' does not appear anywhere in the promoted file.

SPANS RE-CURATED FIRST, before the builder ran. All 35 were ungrounded against the new text, so all 35 were re-cut -- round two re-cut 33 of 35. Every one was tested against BOTH extractors before build_rhetorical_annex.py was run, which is the trap that cost round two a cycle: check_grounding.docx_text yields 'R2' and build_rhetorical_annex.doc_text yields 'R²' on the same 93,085-character extraction. The scratch harness reported 35/35 grounded under both, and no re-run was needed. The builder then wrote 35 spans, dropped none, and kept the same role distribution (claim 8, justification 6, bounded_conclusion 4, problem_statement 3, cross_step_credit 3, deviation_disposition 3, mechanistic_warrant 2, hedge 2, deferral 2, restatement 2), 11 claim<-justification edges and 2 coreference edges.

Every new span quote is free of digits except four that carry a document ID or 'Stage 2' (RS-C01, RS-C02, RS-F01, RS-R01), and every one is free of R2/R², which is now stated as a rule in the file's header comment. Two section labels were updated to the new headings (RS-D02 to 'DEV-003-01 — dissolved CO2 probe drift').

22 OF 177 PCR-003 QUOTES RE-ANCHORED in build_ground_truth.py; round two needed 23 of the same 177. Every table-row quote survived untouched again, because the row builders rebuild the row from the DataFrame the document renders -- only prose quotes moved. The 22 were: the ProcessStep executive-summary quote, both Equipment quotes, all four StudyDesign quotes, the DesignSpace quote, all nine CLASS_QUOTE parameter-classification quotes, and five of the six report-summary statements. Each was re-anchored to the sentence in the NEW text that names the same record. No document text was edited to suit a stale quote, and no threshold was moved.

TWO REPORT-SUMMARY STATEMENTS WERE REWRITTEN, not just re-quoted, because the re-authored document no longer says what they asserted. st(4) claimed 'The response-surface models are adequate for all five responses and predictive for four of them'; the new report states adequacy and that every overall F test reaches significance, and never makes the four-of-five predictive claim, so the statement now says what the document says. st(6) kept its statement but moved section from 'Process capability and robustness' to 'Conclusions', which is where the new text carries the all-attributes-meet-acceptance sentence. An annex statement that outlives the sentence it summarizes is the failure mode the discrepancies file warns about, so both were changed rather than force-fitted.

D-002 SURVIVED THE THIRD RE-AUTHOR UNCHANGED. The registered_sentence is verbatim in the new .qmd under whitespace collapse and verbatim in the rendered docx, at §1.1 'Product and unit operation'. discrepancies.yaml and DISCREPANCIES.md therefore needed no edit -- the wording did not move. 'leached Protein A' still does not occur in the report (0), and the annex still carries the absolute in the ProcessStep description (1 hit on 'only step'). Both annexes' weak_claims are empty.

GATES: build_ground_truth.py + validate_annex.py -> 20/20 annexes valid. GROUNDING_STRICT_ANCHORS=1 check_grounding.py -> 2084/2084, 0 weak anchors, exit 0 (PCP-003 105/105, PCR-003 177/177). make test -> 89 passed. make style -> 24 OK / 0 FAIL. git diff --stat outputs/ -> empty.

NOTHING OUTSIDE THE ALLOWED SET MOVED. git status lists exactly: authoring/rhetorical/PCR-003.spans.yaml, the three deleted *.DRAFT.* files, PCR-003_bioreactor.qmd/.docx/.pdf, build_ground_truth.py, ground_truth/PCR-003.json. ground_truth/PCP-003.json rebuilt byte-identical to HEAD, and PCP-003's qmd/docx/pdf are byte-identical to HEAD -- verified with git diff --quiet, not by reading the status line. No other rendered document and no other annex moved, so no full make corpus ran. authoring/out/PCR-003.rhetorical.json is written and gitignored, as designed.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `pc_package/PCR-003_bioreactor.qmd`
- `pc_package/build_ground_truth.py`
- `authoring/rhetorical/PCR-003.spans.yaml`
- `authoring/discrepancies.yaml`
- [[DISCREPANCIES]] — `authoring/DISCREPANCIES.md`
