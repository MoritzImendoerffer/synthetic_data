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
