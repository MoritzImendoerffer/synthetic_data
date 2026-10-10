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
