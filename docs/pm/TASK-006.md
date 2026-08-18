---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-006
status: done
kind: annex
title: "Promote, render, re-anchor and re-ground the pilot batch (PCP-007, PCR-005, RA-001)"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCMR-001", "PCP-003", "PCP-006", "PCP-007", "PCP-008", "PCP-009", "PCR-003", "PCR-005"]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-006 — Promote, render, re-anchor and re-ground the pilot batch (PCP-007, PCR-005, RA-001)

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/ANNEX-A-BATCH.md. Batch exposure: about 507 quotes and 39 rhetorical spans. RE-CURATE THE SPANS FIRST or build_ground_truth writes nothing for that document. THE TWO-EXTRACTOR TRAP cost round two a cycle: check_grounding.docx_text yields 'R2', build_rhetorical_annex.doc_text yields 'R²'. Row quotes survive a re-author untouched; only prose moves. READ every annex report-summary statement -- round three found two that asserted something the re-authored report no longer said, and no gate catches that.

## Acceptance criteria

- [x] each DRAFT replaces its committed .qmd; docx and pdf rendered explicitly with the venv on PATH; check_render.py reports 0 missing glyphs on each FRESH pdf; page counts recorded
- [x] for every document in this batch that has a rhetorical layer, its authoring/rhetorical/<DOC>.spans.yaml is re-curated against the new text and EVERY span is tested under BOTH extractors before any builder runs; `build_rhetorical_annex.py --doc <DOC>` writes the same span count as before or states the new one and drops none
- [x] `cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py` -> 20/20 valid
- [x] `GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py` -> N/N with 0 weak anchors, N reported against 2084 and the number of quotes re-anchored stated per document
- [x] every registered discrepancy carried by a document in this batch is re-verified verbatim against the new text; discrepancies.yaml and DISCREPANCIES.md updated together if a wording moved
- [x] no document outside this batch has its .qmd, .docx, .pdf or annex modified (git status does not list them); `git diff --stat outputs/` empty; make test and make style pass; weak_claims empty in all 20 annexes

**Depends on:** [[TASK-003]], [[TASK-004]], [[TASK-005]]

## What was built

The pilot batch is promoted, rendered, re-anchored and re-grounded. The corpus is back at 2084/2084 quotes grounded across 20 annexes with GROUNDING_STRICT_ANCHORS=1 and 0 weak anchors, 20/20 annexes valid, exit 0.

RENDERS. All three promoted with `git mv -f`, then docx and pdf rendered explicitly with the venv on PATH, and each pdf glyph-checked FRESH: PCP-007 30 pp (was 33, and 28 before the re-author round), PCR-005 47 pp (was 43), RA-001 30 pp. No missing glyphs on any of the three. Plans band 23-31, DoE-report band 41-56; all three sit inside.

THE RHETORICAL LAYER FAILED WHOLESALE, WHICH IS THE NORMAL STATE. All 39 of PCR-005's spans went ungrounded on the re-authored text -- the layer is curated against one revision of the prose and a one-pass re-author invalidates every quote at once. Re-curated all 39 against the new text, holding every role and every section, and tested each under BOTH extractors before any builder ran: 39/39 present under check_grounding.docx_text and build_rhetorical_annex.doc_text. build_rhetorical_annex.py --doc PCR-005 then wrote 39 spans, dropping none, with the same role distribution as before (claim 10, justification 9, bounded_conclusion 5, mechanistic_warrant 4, deferral 3, cross_step_credit 2, deviation_disposition 2, hedge 2, problem_statement 1, restatement 1). This was also the end-to-end test of TASK-001's converted YAML, on the only pilot document with a layer, and the gate behaved as designed: doing it in the wrong order would have made build_ground_truth.py write nothing at all.

Three spans changed more than their wording, and the file's header says why. R17 (mechanistic_warrant, the resin-property account of ligand release) moved to Mechanistic interpretation and R27 (cross_step_credit for leached Protein A) moved to Response-surface models, because the argument moved there. R25 lost its supported_by edge: the re-authored Design space section makes a different claim, about load flow rate and end of pool collect, which the assayed-pool evidence in R23 does not support. Claim<-justification edges went 13 -> 12 for that reason.

QUOTES RE-ANCHORED, PER DOCUMENT. 68 of 2084 across the three, and 0 elsewhere: PCP-007 28 of 67, PCR-005 30 of 123, RA-001 10 of 317. RA-001 is the largest annex in the corpus and lost only 10, which confirms what the row builders are for -- every table-row quote survived the re-author untouched, because row_quotes() rebuilds the row from the DataFrame the document renders. All 68 misses were prose.

EIGHT ANNEX STATEMENTS ASSERTED SOMETHING THE RE-AUTHORED DOCUMENTS NO LONGER SAY. This is the failure round three found twice and no gate catches: the quote can be re-anchored while the statement stays false. Each was rewritten to what the document now says, with the reason in a comment beside it.

  RA-001 S12 claimed the assignment "predicts no classification and no design space". The phrase "design space" does not occur anywhere in the re-authored RA-001. Cut back to the half the document makes.
  RA-001 S13 claimed one attribute, leached Protein A, has no parameter ranked against it. The re-authored document never says this and mentions leached Protein A only as an attribute entering at the capture step. Replaced by a limitation the document does state, that the risk priority number is ordinal.
  PCP-007 S4 called the step "the principal aggregate reduction step"; the re-authored plan calls it the aggregate polishing step and carries the point through the fact that pool purity cannot be recovered downstream.
  PCP-007 S5 said pool aggregate is judged against the DRUG-SUBSTANCE limit at this step. It is not any more: the re-authored plan gives aggregate a POOL criterion too, carrying the drug-substance criterion through unchanged and leaving the assurance margin to cover the whole difference. Both governed attributes now have a pool criterion, derived two different ways.
  PCP-007 S6 said an above-limit pool "constrains anion exchange and is reconciled in PCMR-001". The word reconcile does not appear in the re-authored plan. Replaced by the reason the margin is there.
  PCP-007 S7 described a worst-case aggregate challenge run separately from the designed experiments. That section is gone -- the word "worst" does not occur in the document at all. Replaced by the decision rule for a model that fails.
  PCR-005 S3 said the attribute the step sets stays inside acceptance across the whole characterized region. The re-authored report qualifies that (NOR propagation excludes a sliver at the high pH edge), so the statement now carries what the Design space section does say, that the constraint is a joint one.
  PCR-005 S7 quoted "The limit is met after anion exchange and not before", a sentence the re-authored report no longer contains.

TWO ASSERTIONS ALSO CHANGED MEANING, not just anchor. PCP-007's aggregate acceptance assertion said the criterion is "applied directly to this pool", which the re-authored plan contradicts. And elution flow rate is now expected to act through residence time and PEAK SHARPNESS, where the assertion said residence time and pressure drop.

ONE OUT-OF-BATCH ANNEX MOVED AND WAS PUT BACK. The aggregate acceptance assertion text is shared by PCP-007 and PCR-007, so correcting it rewrote ground_truth/PCR-007.json -- a document this batch does not touch and did not re-author. The text is now conditional on `report`, PCR-007.json is byte-identical to HEAD again, and git status lists only this batch. Worth carrying into the remaining annex tasks: the cx_/pa_/vi_ builders are pair-shared, and an unconditional edit reaches the sibling.

REGISTERED DISCREPANCIES. None of the three batch documents carries one. All five registered sentences that use the `registered_sentence` key are still verbatim in their own .qmd (PCP-003, PCP-006, PCP-008, PCP-009 D-001; PCR-003 D-002); the three report-side D-001 records use a different shape and carry no such key. None of the eight discrepancy-carrying documents is modified by this batch, so none could have been created or erased. PCP-007's author reported avoiding D-001 rather than touching it, and that checks out: its §8 commits the first PAR analysis to holding the other parameters at their SET-POINTS and then states explicitly that the set-point coincides with the range midpoint at this step, which is the approved method D-001 registers a departure from elsewhere.

GATES. 20/20 annexes valid. 2084/2084 quotes grounded, strict anchors, 0 weak, exit 0. weak_claims 0 in all 20. make test 89 passed. make style 24 OK / 0 FAIL. `git diff outputs/` empty. check_render on each of the three: register gate OK, 0 missing glyphs; the numeral advisory reports 5 / 3 / 8 lines and every one is an exempt category -- α = 0.05, the coded levels −1 and +1, the 95 % predictive interval, and in RA-001 identifiers such as IgG1, pCO2, feed-1 and "Section 5". git status lists only this batch's .qmd/.docx/.pdf, build_ground_truth.py, its three annexes and the PCR-005 spans file.

## Documents it is about

- **PCMR-001** — `pc_package/PCMR-001_master_report.qmd`
- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCP-006** — `pc_package/PCP-006_viral_inactivation.qmd`
- **PCP-007** — `pc_package/PCP-007_cex.qmd`
- **PCP-008** — `pc_package/PCP-008_aex.qmd`
- **PCP-009** — `pc_package/PCP-009_virus_filtration.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`

## Files it touched

- `pc_package/build_ground_truth.py`
- `authoring/rhetorical/`
- `authoring/discrepancies.yaml`
- [[DISCREPANCIES]] — `authoring/DISCREPANCIES.md`
- `pc_package/PCP-007_cex.qmd`
- `pc_package/PCR-005_protein_a.qmd`
- `pc_package/RA-001_risk_assessment.qmd`
