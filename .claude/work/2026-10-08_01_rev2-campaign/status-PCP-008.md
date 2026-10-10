# Status — PCP-008 (Anion Exchange Chromatography) Version 2.0 draft

Author: Opus 5.5 (claude-opus-5-5), one pass, into `pc_package/PCP-008_aex.DRAFT.qmd`.
Run of 2026-10-10 (the 2026-10-09 run left the DRAFT as the bare template; started again).

## Inputs read (2026-10-10)
RUNNER, brief PCP-008, section_plan (plan), STORY_BIBLE (incl. §9b), WRITING_GUIDE, REGISTER_EXEMPLAR,
PLAN-LESSONS, data-state-2026-10-09b; rendered PCMP-001 V2 and frozen PCP-008 V1.0 (content only);
signatures/docstrings in _pcpkg.py, doe_report.py, tables.py, ctable.py. No other .qmd opened.

## Decisions
- Keep every V1.0 design/sampling/spiking/decision rule: 19-run full factorial (16 + 3 CP), 28-run FCCD
  (16 + 8 + 4 CP), randomized within one resin lot and one load lot (lot block rule), load qualification and
  invalidate/re-execute rule, spiked/unspiked matched load, spiking model qualified separately, DNA and
  leached Protein A monitored on every RSM pool (not fitted), flow-rate univariate low/centre/high + viral run
  at high, carry-into-multivariate rule, NOR narrowed rather than criterion relaxed, contiguity rule, green
  plot on governing factor, seed, V1.0 qualification output list, EQ-CHR-118 as planned equipment.
- Replaced only where PCMP-001 V2 sets the rule, each listed in "Changes in this revision": a priori IACs
  (T.criteria_change, T.iac_derivation), judgement statistics (batch PI / viral worst case in NOR), offset
  qualification (decision at analysis), fragments by nrCE-SDS (AMD-001), §7.2 adequacy + generic tests
  (|residual| on predicted and residual on run order at alpha; Cook's D > 4/n), verification rule, execution
  windows + approval date (F5), capability thresholds + P(OOS), coding description corrected (protein load
  centre 175 is not the set-point 200).
- D-001 written in §PAR as registered ("holds the other parameters at their set-points ...").
- S-AEX-SUP listed in the execution-window table with a footnote (PCR-008 records it); S-AEX-AUG excluded.
- INV-002 named once (revision history names it); not described.

## Flags for the coordinator (found while reading the record)
- Frozen V1.0 PCP-008 §7 states the V1.0 criteria (21.7 ng/mg, 3.78, 3.28) although canon (INV-001 F1,
  T.criteria_change note) says no approved V1.0 plan contained them.
- study_chronology has no equipment for any S-AEX study; V1.0 (kept) names EQ-CHR-118.
- sdm_qualification has no residual DNA / leached Protein A / bed pressure for AEX; V1.0 (kept) lists them.
- univariate_studies: flow rate at low/high in duplicate, no centre run, no XMuLV run; V1.0 (kept) plans
  low/centre/high and a viral run at high.
- DoE CSVs carry no residual DNA or leached Protein A; V1.0 (kept) monitors them on every RSM pool.
- A regression of OLS residuals on predicted values is zero by construction; the plan uses |residuals|.

## Progress
- [x] body written (all sections, section_plan `plan` order; 2026-10-10)
- [x] check_render --render: pass 1 failed only on the two matrix tables (legend note wrapped in a
      narrow table, so the checker could not find it); note moved into the caption; pass 2 all hard gates OK
- [x] citations fixed to [@key]; capability sentence trimmed to what PCMP-001 states; passives for decisions
- [x] names given with document codes at first use per section; two column widths adjusted
- [x] explicit pdf + docx render, check_render re-run (green), all 9 complex tables inspected as png
- DONE 2026-10-10. Final: check_render all hard gates OK; PDF 37 pp, no missing glyphs, all xrefs
  resolved, complex tables complete, no text < 7.9 pt; 397 sentences / 8,047 words of prose (as
  check_render prints); no <<NEEDS:>>. Numeral lint (advisory) flags only identifiers, section/item
  numbers, coded levels and the 4/n convention. Not done here (by design): annex, review.
