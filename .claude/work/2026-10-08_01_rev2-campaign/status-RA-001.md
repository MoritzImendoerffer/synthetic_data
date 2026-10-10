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

## Revision run 1 (2026-10-10, after factual-RA-001.md and feedback-RA-001.run1.md)
- [x] read feedback-RA-001.run1.md, factual-RA-001.md; shared fixes checked in code: RC.cqa_table
      (criteria by type, fragments Severity None), build_fmea.fill texts, related_docs_md relations,
      UNIT_OP_ROLE bioreactor; PCMP-001 pdf re-read for §2 (Q8(R2) continuum), §3 (fragments origin),
      §7.8 wording.
- [x] Table 3.2 (methods by study) and the S-CEX-FRC reason dropped; one pointer to PCMP-001 V2.0 §7.8
      and Table 7.3 (§3). "Every study at every step" deleted.
- [x] Table 3.1 built from RC.cqa_table(); fragments severity "—" with note (not scored); note on the
      origin (A-Mab except fragments, sponsor-set at V2.0); sev_reg_min/max over scored attributes.
- [x] V1.0 detection-6 wording restored (prose and Table 2.1); occurrence/detection prose in V1.0 words.
- [x] errors 4, 5, 7, 8, 9 worded as factual-RA-001.md gives them; error 10 by the builder.
- [x] science corrections and statements the tables contradicted: corrected, listed in new Table 1.3
      (tbl-corrections, 13 rows). Continuum citation kept at Q8(R2) as PCMP-001 §2, listed.
- [x] fragments-not-scored said once (§3, last two paragraphs); §1.1, §4.2 and §6 point to §3.
- [x] Table 5.2: cells superseded at V2.0 marked per report (PCR-005, PCR-006) with notes pointing to
      PCMP-001 Table 4.2; turbidity note (measured, not set).
- [x] "register" kept for the attribute register only; codes named at first use (finding 5, CA3, CA2,
      SOP-2008, PCP-008, the viral clearance claim); PCMR-001 gloss in §1 cut.
- [x] abbreviations: AEX, AMV, DO, TMP, WV dropped (unused); OD -> OD280.
- [x] check_render revision pass 1 and 2: all HARD gates OK (332 sentences, 5987 words); pdf + docx
      rendered; 35 pp. Page images read: Tables 1.2, 1.3, 2.1, 3.1, 4.2, 5.2 (Table 3.1 last column
      widened after the first look). .txt extract refreshed.

### Annex notes for this revision
- tbl-cqa: T.frame of reg31 (RC.cqa_table() grouped by category, Category first, merge=["Category"]);
  markers: acceptance of fragments ^o)^ (origin note), severity "—^n)^" (not scored), viral "Set by" ^v)^;
  CTable relabels them a), b), c) in order of use.
- tbl-corrections: new T.frame in its chunk (merge=["Section"], style="rows").
- tbl-params: markers ^t)^ on post-clarification turbidity, per-report markers on superseded set-point
  and NOR cells (relabelled), ^a)^ on the justified univariate study.
- tbl-methods-by-study no longer exists; the brief still lists T.methods_by_study() for RA-001.

### Flags left
- Acidic variants: the corrected expectation (rise with culture pH) is the opposite of the seeded
  model (effects_bioreactor.csv: pH effect on acidic_variants -4.17, p = 0.003; STORY_BIBLE PCR-003
  worst corner at high pH). PCR-003 must report the measured direction as contradicting RA-001.
- "≤ 2 %" in Table 3.1: the cell prints the helper string; pdftotext merges it to "≤2%" on that
  wrapped line only (word boxes identical to "≤ 5 %"); the DOCX text is the helper string.
