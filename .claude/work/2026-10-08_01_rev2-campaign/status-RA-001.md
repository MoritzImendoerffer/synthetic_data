# Status: RA-001 Version 2.0 (Pre-Characterization Process Risk Assessment)

Author: Claude Opus 5.5 (claude-opus-5-5), one-pass author per authoring/RUNNER.md.
Draft: `pc_package/RA-001_risk_assessment.DRAFT.qmd` (instantiated from template before start).
Scratch: `/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/be14bf3c-e46a-46fd-b419-65482c2add0e/scratchpad/ra001/`

## Progress
- [x] 2026-10-10 started; RUNNER.md read; DRAFT inspected (template only, body empty).
- [x] inputs read: brief, section_plan (risk_assessment), STORY_BIBLE, WRITING_GUIDE,
      REGISTER_EXEMPLAR, PLAN-LESSONS (incl. the rule-8/10 update of 2026-10-10), data-state-2026-10-10
- [x] content-only reads: PCMP-001 rendered (V2.0), RA-001 V1.0 rendered (superseded/rev1)
- [x] body authored (one pass, all sections in section_plan order)
- [x] check_render pass 1: chunks/inline OK, style gate OK, docx+pdf rendered; HARD FAIL tbl-params
      cut off (taller than a page). Fixed: step names from T.STEP_NAME, plan_params study labels
      with a note for the one justified parameter, column widths. Table 3.1 Category widened.
- [x] check_render pass 2: all HARD gates OK. Assessor read of the pdf: wording fixes (no
      "nothing else changes"; singular verbs on compound parameter names; fragments statement
      folded into change 2 instead of repeated in §1.1 and §4).
- [x] explicit quarto render --to pdf / --to docx; check_render pass 3: all HARD gates OK
- [x] every complex table inspected at 110 dpi: Table 3.1 marker overflowed the right rule
      (last column widened); failure-mode tables 4.2-4.9 given style="rows" (multi-line rows ran
      together). Re-rendered pdf + docx; check_render pass 4 (final): all HARD gates OK.
- [x] PCMP-001 was re-rendered by another agent during the run (12:25): its section and table
      numbering and every cited statement re-checked in the new pdf, unchanged.
- DONE 2026-10-10. PDF 33 pp. Gate prose count: 335 sentences, 5941 words. No <<NEEDS:>>.
  Numeral lint (advisory) flags identifiers only (Version 1.0/2.0, PCMP-001 §/Table numbers,
  finding numbers, SOP/AMV IDs, pCO2, feed-1, Tool #1).

## Tables the annex builder must reproduce (same calls as the qmd)
- tbl-train: T.frame(process_steps_df(), caption, "tbl-train", align=[...])
- tbl-related: related_docs_md(DOC) + caption line ": Documents related to this assessment."
- tbl-scoring: T.frame of the scoring DataFrame built in its chunk, merge=["Score"]
- tbl-cqa: T.frame(reg31[...]) built in SETUP: all_cqas() (criteria by type) joined with
  RC.cqa_table() Severity and "Set by", rows grouped by category, markers a) on fragments and
  b) on the two viral "Set by" cells; header CQA->"Quality attribute", Tool #1->"Tool #1\nscore",
  Set by->"Formed or\nset at". NOT RC.cqa_table() as it stands (see record notes).
- tbl-methods-by-study: T.methods_by_study()
- tbl-ranking: T.frame(RC.ra_scope_df().drop(columns=["CQA(s) at risk"]), merge=["Step","Unit operation"])
- tbl-fm-<step>: fm_table(k, label) = T.frame of RC.ra_detail_df() rows of the step, Step dropped,
  style="rows" (labels tbl-fm-bioreactor, -harvest, -protein-a, -vi, -cex, -aex, -vf, -ufdf)
- tbl-scope: T.frame(scope) built in SETUP from RC.ra_rows() (asserted equal to char_scope_df counts)
- tbl-params: T.frame(params52) built in SETUP from plan_params(k) (NOR/set-point as characterized),
  step names T.STEP_NAME, merge=["Step"], marker a) on the AEX operating flow rate
- tbl-approvals: T.frame of the responsibilities DataFrame in its chunk

## Record notes (for the coordinator)
- RC.cqa_table() still prints every criterion as "lo–hi" (viral clearance "16.7–30 log10"), the
  Version 1.0 form that _pcpkg._acc_text and PCMP-001 Table 3.1 replaced; the document composes
  Table 3.1 from all_cqas() + RC severity instead. Fix RC.cqa_table() (use _acc_text) or anchor the
  annex on the composed rows.
- Fragments' severity 4 in RC.cqa_table() is the fallback default (fragments_lmw is not in
  build_fmea.CQA_SEVERITY), the same default as "performance". The document says it enters no score.
- PCMP-001 V2 §3 says all register criteria are "taken from the A-Mab case study"; the brief called
  the fragments criterion "sponsor-set". The document states neither origin.
- RC failure-mode text (build_fmea CONTENT) keeps Version 1.0 labels ("Dissolved CO2 ... mmHg",
  "Osmolality ... mOsm", "titer") and says UF/DF diavolumes are "not part of DS characterization",
  which contradicts the scope (PCP-010/PCR-010). Not editable here.
- Version 1.0 text errors not carried over: "a maximum volumetric load" shares a bound with its NOR
  (it is the LOW end of filtration volume that is shared); the two Protein A performance factors
  "cost no additional runs"; CEX protein load "carries the highest severity because both aggregate
  and HCP are at risk" (8 comes from aggregate, shared by elution pH and stop collect).
- Revision history says "approval and execution dates recorded": the only execution date this
  prospective document records is the start of the first study (S-BRX-SDM, 2025-08-11).
