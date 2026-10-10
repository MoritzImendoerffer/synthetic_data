# Status: PCP-004 Version 2.0 (Harvest and Clarification plan)

Author: Claude Opus 5.5 (claude-opus-5-5), one-pass author per authoring/RUNNER.md.
Draft: `pc_package/PCP-004_harvest.DRAFT.qmd` (instantiated from template before start).
Scratch: `/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/be14bf3c-e46a-46fd-b419-65482c2add0e/scratchpad/pcp004/`
(pcmp001.txt and pcp004_rev1.txt there are the pdftotext extracts read for content).

## Progress
- [x] 2026-10-10 started; RUNNER.md read; DRAFT inspected (template only, body empty).
- [x] inputs read: brief, section_plan (plan + report_doe/nondoe), STORY_BIBLE, WRITING_GUIDE,
      REGISTER_EXEMPLAR, PLAN-LESSONS, data-state-2026-10-09b
- [x] content-only reads: PCMP-001 rendered (V2.0), PCP-004 V1.0 rendered (superseded/rev1)
- [x] body authored (one pass, all sections in section_plan order)
- [x] check_render pass 1: all HARD gates OK (33 pp pdf); numeral lint flags identifiers only
- [x] assessor read of pass-1 pdf: wording/name fixes, change 2 completed (V1.0 'accept before
      characterization' rule replaced, listed), CQA table merged by Category, param table md_table widths
- [x] check_render pass 2: all HARD gates OK
- [x] pdf inspected table by table (pdftoppm, 110 dpi): found inline '\u00a0' printed literally as
      '\xa0' (Quarto prints the repr of an inline string; the gate does not catch it). Fixed with
      pandoc '\ ' in the source. Widened Table B.1 methods column, Table 6.1 widths.
- [x] check_render pass 3, 4: all HARD gates OK
- [x] explicit `quarto render --to pdf` and `--to docx`; final check_render (pass 5): all HARD gates OK
- DONE 2026-10-10. PDF 34 pp. Gate prose count: 373 sentences, 6923 words. No <<NEEDS:>>.

## Tables the annex builder must reproduce (same calls)
- tbl-related: related_docs_md(DOC) + caption line
- tbl-sops: T.sop_references(sops=HARVEST_SOP_REFS, amvs=HARVEST_AMV_REFS)
- tbl-cqas: T.frame(cqas_by_keys(["hcp","residual_dna","aggregates_hmw","fragments_lmw"]) with columns
  reordered Category first, merge=["Category"], header Acceptance->"Drug substance\ncriterion")
- tbl-perf: T.frame from csv("dev_methods.csv") rows AMV-3015, AMV-3012
- tbl-methods-by-study: T.methods_by_study(["harvest"])
- tbl-params: md_table of plan_params(UO) cells, set-point formatted f0 (= show() cells)
- tbl-roles, tbl-phases, tbl-levels, tbl-sampling: T.frame built in the chunks of the qmd

## Facts checked through helpers (for the successor)
- No IAC for harvest (`D.iac_table("harvest")` empty); harvest has no platform worst case
  (`CFG.raw()["iac"]["platform"]` has no harvest key), so the derivation credits it with no change.
- No Version 1.0 analysis-time criterion at harvest (`D.rev1_criteria("harvest")` empty);
  `T.criteria_change(["harvest"])` is empty, so it is not printed.
- Studies: S-HAR-UNI 2025-11-03..2025-11-21 (this plan's); S-HAR-UNI2, S-HAR-HLD (Sept 2026, after
  INV-001 closed) are NOT this plan's (PD-004-01, PD-004-02 in `discrepancy_register("PCR-004")`).
- Version 1.0 approved 2025-10-20 (`rev1_date`), V1.0 title block carried 2026-07-24 (`REV1`).
- method_plan: S-HAR-UNI lmw_in_scope False (fragments not a response); ran before AMD-001.
- NO harvest scale-down qualification in the record: no S-HAR-SDM in study_chronology.csv, no harvest
  rows in sdm_qualification.csv; PCMP-001 §5 lists no harvest output as compared. Version 1.0 planned
  one. The plan keeps the V1.0 qualification design with the V2.0 offset rule (PLAN-LESSONS 9). To
  be reported to the coordinator: PCR-004 register has no entry for this.
- Method performance for AMV-3015/AMV-3012 from `csv("dev_methods.csv")`.
- Turbidity: lower edge of range studied == lower NOR limit (1 NTU); V1.0 §4.3 wrongly said every
  range is wider on both sides. Computed in setup, not repeated.

## Decisions
- Structure = section_plan `plan`; screening/RSM subsections omitted (non-DoE); appendices A (planned
  levels) and B (sampling schedule) kept from V1.0 with appendix_numbering.
- Keep every V1.0 design/sampling/decision rule; replace only what PCMP-001 V2.0 replaces (equivalence
  test of the SDM -> offset rule), and list each change in §1.1.
- Case-study assumption (no impact on product quality) stated as an assumption in §4.1 and §12.
- Hold study / S-HAR-UNI2 named once in §1.1 as not studies of this plan; never described.

## Revision run 1 (2026-10-10, same author), after feedback-PCP-004.run1.md
Inputs read: feedback-PCP-004.run1.md, factual-PCP-004.md, content-review-PCP-004.md,
data-state-2026-10-10.md, rebuilt brief; PCMP-001 re-rendered 11:39 (structure unchanged, section
refs still valid). Table 3.2 is already merged in PDF (multirow) and DOCX (vMerge).
Plan: restore V1.0 wording of objectives, qualification design, operation, sampling, statistics,
criteria, PAR, phases (marking V1.0 text); offset rule per fix list B/err 1 ("would only be recorded";
no rule for HCP/DNA/clarified turbidity, PCR-004 states approach; runs/data set not named by V1.0);
no execution claims (A1); drop INV-002 (A2); no "forms"; mechanism corrections (discs, laminar flow,
radius/sigma, L/m2 volume, centrate SV point, DNA LOQ claim); change list +6 (discrepancy) +7
(corrections/gaps); tables: 4.1 source+dose notes & wider criterion col, 5.1 RSD/LOQ/analytical
variance + AMV-3014 row, drop methods_by_study and Table 11.1, 6.1 one number format w/o constant
column, A.1 planned levels per series (long form, doubled filter series), B.1 method names + legend.
- [x] revision written (one pass, same author) - [x] gate: 4 runs, all HARD gates OK each time
- [x] pdf/docx rendered (venv on PATH); changed tables inspected as images: 4.1, 5.1, 6.1, 10.1, A.1, B.1
- DONE 2026-10-10 12:0x. PDF 35 pp. Gate prose count: 344 sentences, 7139 words. No <<NEEDS:>>.
- Removed: T.methods_by_study (only "no DoE"), Table 11.1 (phases; prose as V1.0), AMD and DoE abbrevs.
- Annex builder must now reproduce: tbl-cqas (Category first, merged, header "Quality attribute",
  3 unmarked notes, notes_per_row); tbl-perf (AMV-3015/3012/3014, RSD/LOQ/accuracy/analytical
  variance %); tbl-params (md_table, 5 columns, f0 numbers incl. ranges, no study-type column);
  tbl-levels (long form: Series, Material, Level, Setting; merged Series+Material); tbl-sampling
  (method names + AMV legend note); tbl-roles (cell text as V1.0).
- Left (reported): V1.0 design criticisms per coordinator C (shear device single rate, SEC on crude
  culture, clarified-vs-culture netting DNA adsorption, criterion 2 basis, blend bypassing the sterile
  filter, <LOQ exclusion, turbidity-series PAR, time-held rule vs retained centrate); helper-defined
  related_docs_md (no PCP-003/PCP-005/PCR-005) and revision-history cell; Table 3.2 already merged.
