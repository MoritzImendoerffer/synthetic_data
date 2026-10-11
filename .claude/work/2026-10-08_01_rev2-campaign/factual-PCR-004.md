# Factual check of PCR-004 Version 2.0, draft run 1 (2026-10-11)

Checker: Claude Opus 5.5 (ac0b909cf1ef246bd). Line numbers refer to `PCR-004_harvest.DRAFT.txt`. Scratch scripts in
scratchpad/pcr004_check/. Saved by the coordinator from the agent's hand-back.

## Errors, most consequential first
- E1 §13 opening: "It records … every departure from PCP-004 as a discrepancy from the plan." The register holds 3
  entries; §3.2, §3.4, §3.5, §4.2, §7 and §11 describe 10 or more further departures. Register them (coordinator).
- E2 §3.5 and §8: "simulates 2,000 batches with every parameter drawn within its NOR". PCMP-001 §6.4/§6.5 draw each
  parameter from N(set-point, NOR width/6), clipped to the characterized range; in monte_carlo.csv 60 of 2,000 batches
  have one of the 5 recorded parameters outside its NOR (viral inactivation temperature below 20 °C in 41). Use
  PCMP-001's wording. (INV-001 §4.4 also says "draws every parameter inside its NOR": corpus-level conflict.)
- E3 §7 uses study event DEV-004-02 of S-HAR-UNI as evidence ("The failure is therefore taken as the capacity of the
  media.") while the executive summary, §11, conclusion 7 and §13.1.2 say the events bear on no conclusion. Rest §7 on
  the duplicate runs and the steep rise, or qualify the "no bearing" sentences.
- E4 "Changes in this revision" omits what moved: Version 1.0 gave the depth filter load PAR as 80–160 L/m2 with every
  NOR inside its PAR (Version 2.0: 80–140, upper NOR limit on the edge), and stated a qualified model, "a laboratory
  disk-stack centrifuge", with "no difference between scales" (Version 2.0: no qualification, no such centrifuge).
  State both, and that the three classes are unchanged.
- E5 Table 5.1 note b and Appendix C note b ("give no precision for SEC or nrCE-SDS"); Appendix C maps aggregate to
  AMV-3011. The record gives AMV-3221 for the univariate aggregate results (3.8 % RSD, LOQ 0.20 % HMW, dev_methods.csv)
  and nrCE-SDS a repeatability SD of 0.06 points (config analytics.methods.cesds), as the engine uses
  (doe_report._ofat_method_sd); aggregate and fragments then scatter at about method precision. AMV-3221 is in no
  SOP/AMV register while the plan names AMV-3011. [coordinator: corpus convention, as PTP-001 states it: the SEC
  aggregate method is validated under AMV-3011 (SOP-3011) and AMV-3221 is the record of its qualified performance;
  cite both that way.]
- E6 §11: "two NOR limits were not run as levels" → three (8,000 g, 10,000 g, 10 NTU; §4.2, Table 4.2).
- E7 §1.2: "Objectives 2 and 5 were met." Objective 2 concerns HCP and DNA "released by cell breakage", and the
  within-run comparison against the culture could not be made (§3.4; culture not recorded, §3.2). "Met in part".
- E8 §3.5: "No plan sets a criterion for a held pool." PCMP-001 Version 2.0 §5 and §7.3 judge a held pool against the
  criteria it must meet on entering the next step, the criterion the report then uses in item 1; only the fragments
  criterion (none at the Protein A load) and the rule for the expected level are the report's own. (REPORT-LESSONS §2
  rule 10 used the same wrong phrase.)
- E9 Table 5.4 vs Table A.1: the hold pool's day-0 aggregate is 1.12 and 1.14 %; all 30 runs of S-HAR-UNI2 lie at
  1.40–1.67 % (set-point mean 1.59 %); both are clarified harvest at set-point; the gap is about 8× the SEC
  repeatability. The hold verdict uses changes only. Source: config analytics.holds.harvest.hmw0 1.10 against about
  1.55 % in the step model. [coordinator: the record does not name the culture of the hold pool; state both levels and
  that, and that the verdict rests on changes.]
- E10 §3.5: "Fragments, which PCP-004 did not list". PCP-004 Table 4.1 lists fragments in scope (and §2.2 says four
  attributes were placed in scope); the plan says fragments are not a response of its study and are not named in its
  criteria.
- E11 §5.5 and §8: "1.11 % … out of harvest". 1.115 (1.10 + 0.015 for one day at 2–8 °C, analytics.nominal_train;
  report_values.json 1.115) rounds to 1.12; the value includes a one-day cold hold S-HAR-UNI2 does not have.
- E12 §2.2: "the attributes of high and very high criticality are called critical (CMC Biotech Working Group 2009)".
  PCMP-001 calls all 11 register attributes CQAs and §8 applies the CQA Cpk target to fragments; verify or cut.
- E13 §3.5 item 2: the fragments entering level is not "the highest level expected in routine manufacture" (set-point
  culture only; a longer culture within its NOR raises fragments, §2.1). Verdict holds (1.76 against 2 %); say it as a
  limit.
- E14 minor: Table B.1 note (intercept and residual SD in the unit of the response); §3.4 "two results for each
  response" (not for centrate turbidity in the turbidity series); §7 "met every criterion at every level" (slope
  criteria judged per series).

## Departures from PCP-004 Version 2.0
1. Unclarified culture not sampled: confirmed (plan §5.4, Appendix B, §5.3).
2. No HCP or DNA in the centrate, no filtrate sample: confirmed (Appendix B); one planned sample point missing either way.
3. Filter-train pressure not measured: confirmed (plan §1, objective 3, §5.1).
4. Protein A load challenge not run: confirmed (plan §1, §6.2).
5. Depth filter load series run once on set-point centrate: confirmed (plan §5.5, §6.2, §11, Appendix A; centrate
   turbidity 53.8–62.2 NTU matches 9,000 g, not 6,000 g (≈123) or 12,000 g (≈44)).
6. Levels differ from Appendix A, NOR limits not run: confirmed; mentioned only in the PD-004-01 paragraph, not in the
   register entry.
7. Viability, cell density and run order not recorded: confirmed (plan §12 item 2, §6.2); also the sequence of the
   series (§6.2, §11), the turbidity material made from the two earlier series, and the culture-as-block analysis (§12
   item 3).
8. Fragments measured although not a response: confirmed for S-HAR-UNI2 (plan §4.2; §3.5 applies a criterion);
   refuted for S-HAR-HLD (PD-004-02 covers it).
9. Rules the plan leaves to the report: confirmed (plan §8); a fifth, the qualification rule (§5.1), is moot under
   PD-004-03.
10. Slope tested against the regression residual, not the set-point replicates: confirmed (plan §5.5, §5.4); the plan's
    error should decide (REPORT-LESSONS §1 rule 9). Under it the widest interval ends in §5.5 become 35, 92, 12 and 22 %
    of the set-point mean (HCP, DNA, aggregate, fragments), not 34, 59, 11 and 16 %; the Table 5.3 CIs move.
11. No method for the antibody concentration: confirmed as a gap the plan leaves open (§5.3); the register carries
    AMV-3021 (Protein A affinity HPLC), the titre method for a harvest (REPORT-LESSONS §2 rule 8).
Further: practical significance not reported as planned (plan §5.5: each significant slope's change across the NOR
against method precision; the report gives changes over the range studied; across the NOR: centrate turbidity vs rcf
−24.6 NTU, post-clarification turbidity vs rcf −0.22 NTU (single-result precision about 0.16), vs depth filter load
+2.84 NTU); the impurity release and product quality criteria (§7 criteria 1 and 3) replaced by the report's slope
rule, not registered and not said whether chosen after the results; the aggregate method (E5); records not held
(temperature and end-of-culture-to-clarification time held constant, constant flux and matched Q/Σ (§5.2); one assay
campaign per series with the same reagent lots (§5.3); equipment calibration status per run (§9); the analysis agreed
with Statistics before the first run (§10)); lower weight: no quadratic fitted although two relationships are not
linear (§5.5); depth filter load effect sizes over 80–160 L/m2, not over the PAR (§8); "investigated before the range is
reported" (§7) has no record.

## Checked and correct
Table 5.3 and Table B.1 (slope, SE, intercept, residual SD, change, CI, p with both error terms, R²), "same slopes
significant", the 19-test count; all 210 cells of Table A.1 and Table 5.2; Table 5.1; prose numbers from the univariate
data (level means, ranges, 86 % share, 2.3-fold rise, challenge slope and R², §5.5 percentages, step yield 92.4–97.7 %,
95.7 %); hold Table 5.4, Table 5.5 (engine limits 2.346, 30.254, 16.247, the changes), §5.6 (2.648, 0.43); criteria
(6.46, 9.30, 1.40-fold, 0.56, 18.0–39.0, fragments) against iac.csv and PCMP-001 Table 7.1; Table 8.1 and the 0.15 %
bound; residual DNA (149,000 ng per dose, 8.2 log10, 2.5/1.5/5 log10, 700 mg); 18.72 %; 15,000 L; 5 PPQ batches;
dates against study_chronology.csv, INV-001 and the plan; both registers and the event facts; objectives and criteria
against the plan; parameter table; PCMP-001 and PCP-004 section citations; Figures 5.1–5.3.

## Not checked
A-Mab page citations (p.47, p.85) and the "called critical" rule; other reports' content; whether DEV-004-02 was
examined "before the range was reported"; the equipment of S-HAR-UNI2 and the culture of the hold pool (not in record).
