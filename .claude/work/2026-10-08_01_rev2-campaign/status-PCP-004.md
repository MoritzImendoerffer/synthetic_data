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
