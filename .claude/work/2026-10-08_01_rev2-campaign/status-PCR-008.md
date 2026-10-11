# Status — PCR-008 (Anion Exchange, Step 8) Version 2.0 authoring

Author model: Claude Opus 5.5 (claude-opus-5-5). Started 2026-10-11.
Draft: `pc_package/PCR-008_aex.DRAFT.qmd` (instantiated from template before start).
Scratch: `/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/be14bf3c-e46a-46fd-b419-65482c2add0e/scratchpad/pcr008/` (explore*.py, PCP-008.txt, PCMP-001.txt)

## Inputs read (all done)
RUNNER, brief, section_plan (report_doe), STORY_BIBLE, WRITING_GUIDE, REGISTER_EXEMPLAR, REPORT-LESSONS,
data-state 09b + 10-10, rendered PCP-008 + PCMP-001 (pdftotext), helper signatures (_pcpkg, doe_report, tables, ctable).

## Data facts established (explore scripts)
- Selected models: HCP log (A,B)+block n=40 adequate; XMuLV raw (A,C,D,AD) n=28; MVM raw (A,C) n=28;
  yield no term +block (planned-only: none, gap 0.213); fragments no term +block.
- Coded 0 = range midpoint: protein load 175 g/L vs set-point 200 (D-001: say nothing about where PAR(set-point)
  holds others; describe centre points honestly; no reconciling sentence).
- Verification HCP bound 4.2673 (planned runs, no offset, one-sided 95 %); LOO min 4.21 (run 5); flagged runs
  on planned model 2, 9; none > F median. Offset sensitivity: at offset est 4.18, at unfavourable CI end 3.08 (<4).
  Without CA3: full quadratic inadequate (gap 0.275) -> platform 4 stands; PA/CEX qualifications then fail.
- Near-equivalent (ΔAICc<=2): HCP 5 (all A,B; AB in 2, A² in 2, C in 1); XMuLV 2 (AD only in selected);
  MVM 3; frag 3; yield 4.
- Cook flagged (all runs): HCP 9; XMuLV 6,16; yield 38,40; frag 23,35,36; none above F median.
- Design space 0.950 (batch = mean), binding MVM; NOR inside; load pH PAR(NOR) XMuLV 7.22, MVM 7.23 lower edge.
- DNA/LPA pools all < LOQ (RSM + SDM). DNA LOQ 1 pg/mg = 0.7 ng/dose >> 0.001 criterion; model dna_lrv 5.
- Superseded: BD effect 34.8 ng/mg p=0.002 (requalified 0.22, p=0.86).
- governing_factor(mvm) = load_ph from screening; RSM largest |main| = load_cond (equal within SE) -> hand-back.

## Hand-back candidates (departures in neither register, helper issues)
- bed pressure not measured in S-AEX-SDM (PCP-008 §5.1)
- spiked-load comparison / spiking model qualification: no record (PCP-008 §5.1, §7)
- cytotoxicity/interference controls, detection limits: no record (PCP-008 §5.4)
- load qualification: only icIEF acidic variants recorded (PCP-008 §7 item 2 lists HCP, conc., pH, cond.)
- DEV-008-03 record does not name the screening run (PCP-008 §9 run-level buffer lot identity)
- augmentation load lot not recorded; LOT-CEX-8851 expired 2026-04-12 before S-AEX-AUG (PCP-008 §6.3 second lot)
- equipment for AEX studies not named in record (PCP-008 §5.2/§11)
- flow rate WC-CPP vs plan rule (no demonstrated effect -> GPP)
- approaches stated for PCP-008 §7 no-threshold rules (flow-rate effect test, assay attribution, well-controlled)
- D.governing_factor uses screening effects (MVM)
- HCP bound computed without SDM offset; at unfavourable offset end below 4

## Progress
- [x] setup chunk (scratch/setup_body.py + display block at top of scratch/part3.qmd; assembled = part1 + setup_body + part3)
- [x] body sections, all of report_doe written (exec summary to Appendix D), assembled into the DRAFT 2026-10-11
- [x] local run: setup 85 s, 399 inline exprs ok, 50 chunks ok (scratch/run_chunk.py)
- [x] check_render pass 1: style OK, docx OK, pdf OK; FAIL table-fit check (shared `_rows` var) -> fixed with unique vars
- [x] check_render pass 2: all OK except text < 7.9 pt in 3 tables (p45 criteria_results, p46 PAR, p51 cap) -> fixed (narrower cols; tabcolsep group for builder table)
- [x] check_render pass 3: all OK except criteria_results note 7.8 pt (CTable sets its own tabcolsep) -> \let\small\footnotesize group
- [x] check_render pass 4: PASS (all hard checks; numeral lint advisory). 72 pp, 692 sentences, 13786 words
- [x] added 4 asserts (plates CI, CV, edge run, BD sign); explicit pdf render 10:21 OK (3 PD rows)
- [x] coordinator note (config briefly listed PD-009-03..07 under PCR-008): the explicit DOCX render in that window
      failed on `assert n_pd == 3` (as intended); config fixed; DOCX re-rendered 10:33 OK
- [x] prose SUP_MAX printed with T.num (table A.2 shows 150)
- [x] final explicit renders: pdf 10:35 OK, docx 10:36 OK
- [x] final check_render (reads the PDF): exit 0. 51 chunks, 397 inline exprs, no NEEDS; style gate OK;
      692 sentences, 13,786 words of prose; 32 complex tables complete; no text below 7.9 pt; PDF 72 pp
- [x] every complex table and figure looked at in the PDF (pdftoppm), final pages p11/19/27/44/45/50/65/67/71
DONE 2026-10-11. Hand-back below is the final list.

## Decisions taken in the text
- D-001: PAR table via T.frame(D.par_table(UO)) unchanged columns; first analysis defined without saying where
  others are held or where it is anchored; centre runs described as coded 0 = range middle (175 vs 200), no link to PAR.
- Flow rate WC-CPP: reason given (viral claim validated within range; one spiked run; no interaction resolvable),
  and said plainly that the rule alone would give GPP -> hand-back.
- Verification: bound in force 4.27 (rule as stated); sensitivity table tbl-bound (LOO, flagged, all runs,
  offset est/unfavourable end, plan's full quadratic); four-part risk argument.
- DEV-008-02: ci_hw and ver_robust_n not used (meaning not in the record I may read).
- DEV-008-03: run not named in record -> screening leave-one-out over 19 runs reported.


## Staged after pass 3 started (in scratch/part3.qmd, to go into pass 4)
- A-Mab typed at sentence start; duplicate NOR sentence in design space; conclusion 3 (flow rate);
  asserts RI_P met + governing factors; sorted SOP list; MARG_TXT; msd() from monte_carlo.csv in tbl-cap;
  contour figures 6.4x5.2 in; narrower cols tbl-par/tbl-cap; tabcolsep 4pt group around T.criteria_results;
  Appendix B intro fixed (superseded results confirm cause only); superseded screening table added (A.2);
  §5.1 spike-volume clause; objective 2 clause; CA2 sentence narrowed.

## Hand-back (draft)
Departures in neither register:
1. S-AEX-SDM did not measure bed pressure (PCP-008 §5.1 lists it).
2. No record of the spiking-model qualification (spiked vs unspiked load; spike volume) (PCP-008 §5.1).
3. No record of cytotoxicity/interference controls or detection limits (PCP-008 §5.4).
4. Load qualification: only icIEF acidic variants recorded; no HCP/protein conc./pH/conductivity of lots (PCP-008 §7 item 2).
5. DEV-008-03 record does not name the screening run (PCP-008 §9 run-level buffer-lot identity); report ran
   a leave-one-out over the 19 screening runs instead (analysis not in the plan).
6. Augmentation load lot not named; LOT-CEX-8851 expired 2026-04-12 before S-AEX-AUG; no second-lot
   comparison (PCP-008 §6.3).
7. Equipment of the AEX studies not named in the record (PCP-008 §5.2; §11 states it).
8. Operating flow rate WC-CPP while the plan's rule (no demonstrated effect) gives GPP; report gives the
   viral-claim reason and says so.
9. Approaches stated for PCP-008 §7 no-threshold rules (t-test at 0.05 for flow; assay repeatability for LRF
   effects; NOR-in-PAR margins for 'well controlled') - REPORT-LESSONS §3.2 wants them registered.
10. Analyses not in the plan: near-equivalent-model sensitivity, screening-vs-RSM z-test of the AB term,
    offset sensitivity of the verification bound, screening leave-one-out.
11. Coding: plan says set-point = coded 0; protein load set-point 200 is not the range middle (175); centre
    runs at 175. Described honestly, not linked to PAR (D-001).
NOR change: none argued by the data.
Helper issues:
- D.governing_factor uses screening effects; MVM -> load_ph, RSM largest |main| is load_cond (equal within SE).
- T.model_reevaluation prints negative pred R2 with a hyphen.
- capability.csv rounds residual DNA to 4 decimals (SD 0.0000; cap_for prints '0.0002 ± 0').
- dev_008_02_ci_hw / ver_robust_n: no definition in the brief; unused.
- Verification bound computed without SDM offset (iac.verification); at unfavourable CI end 3.08 < 4.
- T.criteria_results slightly wider than the text block at its default size (needed tabcolsep).

## Fix pass 1 (2026-10-11, same author)
Inputs: feedback-PCR-008.run1.md, factual-PCR-008.md, data-state-2026-10-11.md, REPORT-LESSONS §3.1, §6, §7;
brief regenerated (authoring/out/PCR-008.brief.md). Backup of the pre-pass draft:
scratchpad/pcr008/PCR-008_aex.DRAFT.pre-fix1.qmd. No config, helper or annex change.

Setup changes: register IDs by subject (PD_SDM, PD_VIR, PD_LOAD, PD_REC, PD_MEAS, PD_CODE, PD_APPR), n_pd == 10;
verification at manufacturing scale (offset asserted equal to iac's; edge and bound asserts divide by the offset;
LOO passes sdm=/uni= to iac.verification); B_EST dropped, B_LO = B95/offset*lo; QD_CEX and not QD_PA;
BD_R_P_RAW on all 40 runs (like the log value); SUP_Y / SUP_Y_PMIN (E14); SCR_EDGE_RUN/FOLD; EDGE_X/EDGE_M/
MARG_TXT/INTERSECT_PH unrounded; asserts for FP[YLD] F-test, LOT expiry before S-AEX-UNI, |mC| > |mA|,
protein load in the XMuLV worst case, CEX_AT_PLATFORM > 100, 11 register CQAs.

Resolved: A (PD-008-04..10 cited in §3.1, §3.2, §3.4, §3.5, §7.3, §13.1.1, §13.1.3 and described in §13.2;
§3.2 no longer asserts platform control), B (bound 4.18 at manufacturing scale, unfavourable offset end 3.08,
duplicate row dropped, criteria 418 / 16,719 computed, PA/CEX qualification sentence now CEX only), C (flow rate
WC-CPP argued as a judgement on the scope of the viral claim; §7.7 quoted), E1–E15.
Gate: check_render --render exit 0 (twice); explicit pdf + docx renders OK; final check_render exit 0.
78 pp, 51 chunks, 439 inline expressions, 32 complex tables, no NEEDS. Numeral lint advisory only.
Tables looked at: 3.2, 7.3, 7.4, 7.5, 13.2, D.1. DRAFT.txt refreshed.

Hand-back items (neither register / helpers):
- no date for the offset estimates (PCMP-001 §7.1 wants them before the first run) - not in PD-008-04/07;
- step yield by A280 (AMV-3019): PCP-008 Table 3.2 names no yield method; the report now names AMV-3019 from the
  method register (as PCR-007 does) - a method the plan does not name;
- T.criteria_results note a) attaches to column headers (builder); D.governing_factor uses screening effects;
  discrepancy_register renders over 4-5 pages in very narrow columns.
