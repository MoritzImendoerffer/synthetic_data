# Status PCP-009 (Version 2.0 authoring)

Author: Opus 5.5 (claude-opus-5-5), started 2026-10-10.
Target: `pc_package/PCP-009_virus_filtration.DRAFT.qmd` (instantiated from template).

## Inputs read
- RUNNER.md, brief (authoring/out/PCP-009.brief.md), section_plan.yaml (plan), STORY_BIBLE.md (all),
  WRITING_GUIDE.md, REGISTER_EXEMPLAR.md (all), PLAN-LESSONS.md, data-state-2026-10-09b.md
- Rendered PCMP-001 (pdftotext, scratch pcmp001.txt) and frozen V1 PCP-009 (scratch pcp009_v1.txt)
- Helper outputs explored (scratch explore1-4.py): criteria 4.62/4.62 (platform claim), fragments <= 2.00 (DS),
  V1 4.97/5.47 (nominal less 0.35), SDM compares step_yield only (3 SD vs 5 mfg), iac_verification(UO) empty,
  no tightened/widened, studies S-VF-SDM/DOE/RSM 2026-04-15..2026-05-15 sequential, no equipment, V1 approved 2026-04-13,
  fragments nrCE-SDS on every run (method_plan), no SEC fragment result, no augmentation.

## Decisions
- Structure: section_plan plan order; appendices before References (template + RUNNER + V1; CLAUDE.md contradicts itself).
- Criteria table T.iac_derivation placed in sec 7 (criteria); T.criteria_change in 1.1; T.methods_by_study in 5.3.
- Keep V1 rules verbatim in substance: flux decay + integrity test compared in SDM qualification (record has step yield only ->
  report records departure); effects 'over half the range' (V1; conflicts with PCMP-001 6.2 wording + engine 2*coef: REPORT IT);
  V1 adequacy condition 'residual SE small against distance to criterion' kept; V1 success criterion kept; V1 approvals rule kept.
- V1 sampling oddity 'unspiked filtrate pool' resolved toward V1 5.2 'same run' (record: yield on every spiked design run).
- Builder note of T.criteria_change says no approved V1 plan contained the criteria; frozen V1 PCP-009 Table 7.1 does: REPORT IT.
- Adequacy: PCMP-001 7.2 + generic residual regressions (alpha) + Cook's distance > 4/n; remedy per PCMP-001; no CA3/INV-002 text.
- D-001 sentence in sec 8 item 1 (other parameter at its set-point, 201-point grid, fitted RSM model).
- One figure (planned design points + NOR + set-point), dataviz skill loaded (blue/orange slots, shape-coded).

## Progress
- [x] Inputs read (docs + helpers)
- [x] Draft written (one pass, section_plan.yaml -> plan), then two revision rounds in this context
- [x] check_render passes (pass 1: all hard gates OK; pass 2 after revisions: all hard gates OK; numeral lint advisory flags identifiers only: Version 1.0/2.0, §refs, finding numbers, coded levels, 4/n)
- [x] pdf + docx rendered (quarto, venv on PATH), every complex table inspected at 110 dpi (pp. 8, 10, 11, 13, 16, 17, 18, 20, 21, 24, 29, 30, 33, 34)
- [x] final check_render: all hard gates OK; PDF 35 pp; 362 sentences, 6919 words of prose (check_render count); no <<NEEDS:>>

## Log
- Pass 1 check_render: OK (35 pp). Revisions: Table 5.1 widths, Table 6.1 as CTable, windows table note (qualification
  runs vs decision at analysis), adequacy attribution (1-4 PCMP-001 + generic tests; 5-6 this plan), V1 floors in change 1,
  names with codes per section, removed edit narration outside 1.1, classification per PCMP-001 7.7.
- Pass 2 check_render: OK.
- Pass 3 check_render --render: OK (after narrowing appendix columns, softening one prior-knowledge sentence).
- Explicit quarto render pdf + docx, then final check_render (no --render): OK, PDF checks (glyphs, xrefs, 12 complex
  tables, no repeated index cell, no text < 7.9 pt) all OK.
- DONE. Annex (build_ground_truth) not started: separate step after review.

## Open points for the coordinator (in the report)
1. T.criteria_change note a) ('No approved Version 1.0 plan contained these criteria') vs frozen V1 PCP-009 Table 7.1 (4.97/5.47).
2. Effect convention: V1 'half the range' kept; PCMP-001 6.2 'over the coded range'; engine screening effect = 2*coef.
3. V1 SDM qualification compares flux decay + integrity test too; record has step yield only (kept V1; PCR-009 records departure).
4. V1 'unspiked filtrate pool' for protein resolved toward V1 5.2 'same run'.
5. No helper/engine implementation of residual regressions or Cook's distance (generic tests); 4/n typed as a convention.

## Revision run 2 (2026-10-10, after review run 1 + factual check)
- Inputs read: feedback-plans-shared-2026-10-10.md, feedback-PCP-009.run1.md, factual-PCP-009.md,
  content-review-PCP-009.md, data-state-2026-10-10.md, PLAN-LESSONS (rules 4, 8, 10), PCMP-001 re-render (7.2, 7.5, 6.2).
- Draft unchanged since run 1 (qmd 09:47); run-1 copy saved to scratch PCP-009.run1.qmd.
- Plan: rebuild body on V1 text verbatim for design/sampling/spiking/decision statements and expectations;
  changes list keeps old items 1-7 (7 = record, names findings 1 and 5) and adds 8 design space, 9 classification,
  10 corrections; D-001 sentence verbatim (§5c) in §8; drop Table 5.4 (V1 sampling prose verbatim) and
  T.methods_by_study (execution record); Table 5.1 regrouped, caption 'under PCMP-001 §7.1'; Tables 6.1/6.2 no
  constant column; appendix matrices two-level header; residual test via THRESHOLDS residual_alpha/cook_factor.
- DONE (revision run 2). check_render --render: 3 passes, all hard gates OK each time; explicit quarto pdf + docx;
  final check_render OK (glyphs, xrefs, 8 complex tables complete, no text into page foot, no repeated index cell,
  no text < 7.9 pt). PDF 34 pp. 328 sentences, 7133 words of prose (check_render count). No <<NEEDS:>>.
  D-001 sentence (§5c) verbatim in the rendered PDF text and the DOCX text. DRAFT.txt refreshed (pdftotext -layout).
  Tables changed and inspected at 110 dpi: 5.1 (regrouped, merged, note c for the run counts), 6.1 and 6.2 (constant
  columns dropped to captions), 10.1 (rows), 11.1 (unchanged design), A.1 and B.1 (two-level header, coded columns centred).
  Dropped: Table 5.4 (V1 sampling prose restored verbatim) and T.methods_by_study (execution record; builder untouched).
- Flags left: V1 word-for-word sentences the review called glosses or codes (phase criterion sentence; 'rather than
  assert' design-space sentence); gloss tails trimmed from three V1 non-design sentences; shared builders untouched
  (Table 3.2 type column, Table 7.1 spanner, Table 1.1 note); annex must not anchor on methods_by_study or on the
  dropped constant columns of Tables 6.1/6.2.

## Final pass (2026-10-10, after review run 2: feedback-PCP-009.final.md)
- A1: §11 "Each phase begins..." and §12 "If the qualification in §5.1 fails..." quoted in change 3 as Version 1.0
  gating rules replaced by PCMP-001 §7.1 and removed from the body; §12 keeps the V1 mitigation sentence; the
  "no output with a criterion is compared at both scales" sentence now stands once, in §5.1.
- A2: sentence after the V1 success criterion (§7). A3: integrity sentence corrected (§4.1), listed in change 10.
- A4: yield mechanism restated as hold-up in the fouling layer that grows with volume (§4.1), listed in change 10;
  V1 expectation unchanged. A5: output count replaced by naming the responses (§1). A6/A7: §11. A8: §7 "criteria in
  force equal their a priori values (Table 7.1)", asserted in setup. A9: unspiked filtrate pool untouched.
- B: Tables 3.1/3.2 restatements cut; Table 6.1/6.2 caption restatements cut; INV-002 CAs named; compared outputs
  named in change 3; classification rule named in change 9; platform worst case defined in change 6; Table 5.1 one
  criterion per row (only the comparison merged, counts in note b); log10 one way in my tables.
- Gate: check_render --render with .venv/bin/python, 1 pass, all hard gates OK; quarto pdf + docx; final check_render
  OK. PDF 34 pp; 331 sentences, 7285 words of prose. D-001 verbatim (PDF and DOCX). No <<NEEDS:>>. DRAFT.txt refreshed.
  Table pages read at 110 dpi: 5.1 (p16), 5.2 (p17), 6.1 (p19), 6.2 (p20).
