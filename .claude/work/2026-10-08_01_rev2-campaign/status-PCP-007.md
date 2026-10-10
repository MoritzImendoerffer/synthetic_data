# Status — PCP-007 (Cation Exchange Chromatography, plan) Version 2.0

Author: Claude Opus 5.5 (claude-opus-5-5), one pass, per authoring/RUNNER.md.
Draft: pc_package/PCP-007_cex.DRAFT.qmd (+ .pdf 42 pp, .docx), DONE 2026-10-10.
The note of 2026-10-09 that this replaces described a run whose draft was never written.

## Inputs read (2026-10-10)
- RUNNER.md, PCP-007 brief, section_plan.yaml (plan), STORY_BIBLE (incl. §9b), WRITING_GUIDE,
  REGISTER_EXEMPLAR, PLAN-LESSONS, data-state-2026-10-09b.
- Rendered PCMP-001 (pdftotext) and frozen PCP-007 V1.0 (pdftotext), content only.
- Signatures/docstrings in _pcpkg.py, doe_report.py, tables.py, ctable.py, check_render.py.

## Decisions
- Kept every V1.0 design/sampling/decision rule (rule 9): 2^4 full factorial + 3 CP (19 runs);
  face-centred CCD 16+8+4 (28); randomised order, CPs spread; single feed lot or CPs balanced over
  lots; augmentation rule; flow-rate univariate at low end, set-point, high end + escalation rule;
  sampling (load, FT, wash, pool, strip retained); qualification compares yield, aggregate, HCP,
  DNA, leached PA (V1.0 list) + plate count/asymmetry (PCMP-001 §5); operating-region rule; PAR
  contiguity; fixed MC seed (D.PAR_SEED); no minimum Cpk for the step; change control.
- Changes listed (9 items in §1.1), each a PCMP-001 V2.0 rule naming the V1.0 rule it replaces:
  IACs; fragments by nrCE-SDS; offset rule; §7.2 tests + residual regressions (alpha) and Cook 4/n;
  single-batch judgement + NOR-propagated distribution; verification of this step's worst cases;
  classification on effect size across PAR + PAR-to-NOR margin; campaign Cpk thresholds (PCMR-001);
  execution record (windows, EQ-CHR-118 calibration, V1.0 approval date).
- Not described: S-CEX-VER (PD-006-02), hold/augmentation/confirmation studies, CA3 model
  selection (PD-007-01 is the report's). S-CEX-FRC named only as the basis of AMD-001.
- Asserts in setup: NOR/set-point = as characterized; set-point = design centre; design counts;
  criteria bases; AEX bound and adequacy; LPA IAC only at Protein A; no DNA IAC; approval before
  first study; qualification before characterization; UNI parallel to RSM; AMD-001 inside RSM and
  after FRC; RSM end before EQ-CHR-118 calibration due; SEC/nrCE-SDS agreement from CEX pool on.

## Progress
- [x] setup chunk, front matter, all body sections in section_plan order
- [x] check_render: 9 runs; run 2 (first --render) FAILED the table-fit check (appendix matrix notes
      hyphenated in the PDF); legend moved to prose; every later run passed (exit 0)
- [x] assessor read-through of the rendered text; fixes (single-batch rationale per PLAN-LESSONS
      rule 2, NOR-propagated defined at first use, names with codes, table widths)
- [x] final quarto render pdf (42 pp) + docx; check_render on the fresh PDF: exit 0
- [x] every complex table inspected as png (Tables 1.1, 3.2, 4.1, 5.1, 6.1, 6.2, 7.1, 7.2, 10.1,
      11.1, A.1, B.1)
- [ ] annex (separate step; own tables use T.frame on setup variables cq_tab, pp_tab, leg_tab,
      wc_tab, roles_tab, win_tab, mx_scr, mx_rsm — mirror them in the builder)

## For the report author (PCR-007) — departures the kept V1.0 text implies
- Qualification compared yield, plate count, asymmetry, aggregate, HCP only (no DNA, no leached PA).
- S-CEX-UNI ran flow rate in duplicate at the two ends, no set-point runs; measured yield,
  aggregate, HCP only.
- No DNA/leached PA results on the load or pool of any design run.
None of these is in PLAN_DISCREPANCIES or deviations.csv for PCR-007 today (only PD-007-01).

## Revision after review run 1 + factual check (started 2026-10-10 afternoon)
Inputs read: feedback-plans-shared-2026-10-10.md, feedback-PCP-007.run1.md, factual-PCP-007.md,
content-review-PCP-007.md, data-state-2026-10-10.md, PLAN-LESSONS (rules 4, 8, 10), re-rendered
PCMP-001 (§1.1, §6.2 four analyses incl. design space, §7.1, §7.2, §7.5 rule 2, §7.7).
Plan of the rewrite (one pass, same draft):
- Restore V1.0 design/sampling/decision sentences word for word (V1.0 text from
  superseded/rev1/PCP-007_cex.pdf); numbers inline; sentence-initial digits as words (W()).
- D-001 directive: drop only the coded-0 / design-centre clauses of V1.0 §5.5 and §8 (not listed,
  listing would describe them); report to coordinator.
- Changes list: 11 items (IAC; fragments; offset; adequacy + remedy; NOR-propagated definition;
  operating region on single-batch limit; verification; classification rules; capability; execution
  record incl. compiled criteria; descriptive corrections).
- Fragment fold question: iac.verification divides the process-model nominal feed by the pool
  prediction for all three checked CEX worst cases, so no fold rests on a load result (report).

### Revision result (2026-10-10, 15:46) — DONE, not committed
- Draft rewritten in one pass to the fix list and the ten shared resolutions; V1.0 design, sampling
  and decision statements restored word for word (numbers inline, sentence-initial counts as words).
- Coordinator correction applied: V1.0 §5.5 coding sentence and §8 first-analysis sentence restored
  word for word (set-point = design centre asserted in setup); no new design-centre sentence.
- Changes in this revision: 11 items, each naming the PCMP-001 V2.0 rule and the V1.0 text replaced.
- check_render: run 1 dry OK, runs 2-4 --render OK (exit 0), final run on fresh PDF exit 0.
- PDF 40 pp; docx rendered; 444 sentences, 9,979 words of prose; no <<NEEDS:>>.
- Tables re-inspected as png: 4.1, 6.1, 6.2, 7.2, 10.1, 11.1 (Table 11.1 activity column widened).
- PCP-007_cex.DRAFT.txt refreshed (pdftotext -layout).
- Left for the coordinator: one-sided 95 % verification bound vs two-sided 95 % interval (PCMP-001's
  choice); V1.0 wording kept where reviewers flagged it (should-rules, "confirm the mechanism",
  flow rate x collection window, load interactions via peak broadening vs via the wash, capability
  simulation without a residual draw, "the control strategy will be built on the region").
- Fragment fold (Table 7.2): iac.verification divides the process-model nominal feed by the pool
  prediction for HCP, aggregate and fragments alike, so no fold rests on a load result.

## Final pass after review run 2 (started 2026-10-10 evening)
Inputs: feedback-PCP-007.final.md (A1-A12, B), content-review-PCP-007.run2.md, PCMP-001 re-render
(§6.3, §6.5, §7.8 "every study that measures fragments, at every step, measures them by nrCE-SDS").
Plan: Changes rewritten (V1.0 rules quoted in changes 3, 4, 6, 10; change 11 names what V1.0 said and
what is corrected; directions unchanged); §7.2 lead-in replaced (no "used for prediction only if");
§7.5 V2.0 rule only; §13 CA2 amendment sentence, no "acceptable"; §4.1 HCP/LPA binding corrected;
§7.6 clearance factor = nominal feed of process model / predicted pool; §8 flow rate + fragments;
§11 calibration "record names ... for the response-surface study only"; §5.3 PCMP-001 §7.8 wording,
T.methods_by_study dropped; B: Q1 interactions named, Q2 terms, Q3/Q6/Q7 cuts and names.

### Final pass result (2026-10-10, 17:18) — DONE, not committed
- All A1-A12 and B items of feedback-PCP-007.final.md applied (map in the coordinator report).
- check_render: dry run OK; --render exit 0; closing run on the fresh PDF exit 0 (3 runs, no failure).
- PDF 40 pp, docx rendered, 11 complex tables (T.methods_by_study dropped); 459 sentences,
  10,517 words of prose; no <<NEEDS:>>. Table 1.1 inspected (builder note b re-rendered); no table of
  this document changed.
- PCP-007_cex.DRAFT.txt refreshed.
- Left: "It answers what one parameter can do ..." (Version 1.0 §8, restored on the coordinator's
  instruction) kept although run 2 lists it under Q6; PCMP-001 §6.3 itself still says "A model is used
  for prediction only if it meets the adequacy criteria in Section 7.2" (the sentence deleted from the
  plan under A1).
