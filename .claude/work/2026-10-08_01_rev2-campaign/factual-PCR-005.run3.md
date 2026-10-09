# Factual check, run 3: PCR-005 Version 2.0 draft (Protein A chromatography)

Checked by Claude Opus 5.5 (model ID `claude-opus-5-5`) on 2026-10-09.

- **Document:** `PCR-005_protein_a.DRAFT.run3.txt`, the text of `pc_package/PCR-005_protein_a.DRAFT.pdf` (67 pages, rendered 2026-10-09 20:15).
- **Fact sheet:** `authoring/out/PCR-005.brief.md` (generated 19:45).
- **Content references:** the rendered revised plan `PCP-005_protein_a.pdf` (19:56) and master plan `PCMP-001_master_plan.pdf` (20:20), read in full in the sections the report cites (PCP-005 §1.1, §2, §4.1, §5.1, §5.3, §5.5, §6.2 to §6.4, §7, §8.1 to §8.3, §11, §12; PCMP-001 §5 to §7.9).
- **Context:** `data-state-2026-10-09b.md`, `factual-PCR-005.md`, `factual-PCR-005.run2.md`, `status-PCR-005.md`.
- **Method:**
  - I read the draft and the brief in full. Each number-bearing sentence, and each sentence whose deciding word depends on data, was checked against the table of the draft that holds its value and against the brief.
  - Where those were silent or disagreed I opened `outputs/data/` (`sdm_qualification`, `univariate_studies`, `hold_protein_a`, `hold_harvest`, `study_chronology`, `capability`, `model_adequacy`, the Protein A designs, `deviations`) and `config/parameters.yaml` (the assurance target, the DNA reductions of the process model, the NORs).
  - Model-derived claims were recomputed read-only with scratch scripts (`c1.py` to `c16.py` in the session scratchpad) through `doe_report`, `tables`, `_pcpkg` and `amab_process.adequacy` (via `D.ad`): the selected models, the offsets and qualification, the design-space grid, the 9 near-AICc models, the stepwise searches, the three analyses of run 23, the deletion analysis, the residual checks, a Cook's distance simulation (3,000 data sets per output), the CA3 sensitivity, the verification table, the bioreactor limits and the capability table.
  - For attributions to the A-Mab case study I searched `refs/text/amab.txt`. For the INV-001 finding numbers I read the finding list in `authoring/STORY_BIBLE.md` §9b.
  - I read no `pc_package/*.qmd` and nothing under `authoring/rhetorical/` or `authoring/history/`, and changed nothing in the repository except this report.

## Status of the open points of the earlier checks

All five errors of run 2 and its probable error are closed. Of its notes, most are closed by rewrites or by today's data change; three remain (see the end of this section).

| Run 2 item | Status in this draft |
|:--|:--|
| 1. PD-005-02 narrowed to pool host cell protein | **Closed.** Section 13.3 now names PD-005-02 as the influence analysis "because no selected model meets criterion 5", and Table 13.4 covers every output with a criterion. |
| 2. Leached Protein A said to meet criterion 2 | **Closed.** Table 5.7 has a column per criterion with "n.a." for leached Protein A. Section 5.3 reads "each model with a term meets criterion 2". Section 11 reads "on lack of fit and predictive power". |
| 3. Section 7.3 design-space corner | **Closed.** With the new criterion (≤ 17,069 ng/mg) the median now does exceed it at the corner with the other two factors at set-point (20,217 ng/mg), and Section 7.3 says so. |
| 4. 15 and 14 terms | **Closed.** "an intercept and 14 terms" in Sections 3.5 and 4.3. |
| 5. Executive summary on qualification | **Closed.** F1 is rewritten and correct. |
| 6. (probable) anion exchange model on 28 runs | **Closed.** Section 7.1 states the bound is from the 28 planned runs, gives S-AEX-AUG (2026-09-10 to 09-24), and that the bound on all 40 runs is also 4.27 (4.2673 and 4.2691). |
| Note: run-23 basis of Table 5.6 | **Closed.** The table note now names run 23 at its recorded pH (PD-005-03). |
| Note: aggregate bound 0.54 vs 0.535 | **Moot.** New data. Section 4.5 now gives 1.404 and 0.559, and 5 × 1.404 − 0.559 = 6.461. |
| Note: F7 grid limits 44 g/L and pH 3.27 | **Closed.** Section 6 now gives the continuous boundary (42.4 g/L, pH 3.30). |
| Note: load flow rate curvature (Section 9) | **Closed.** Now limited to "Within the NOR". |
| Note: BD "smaller than the main effects" | **Closed.** "smaller than the significant main effects". |
| Note: PD-005-01 reason "the output that sets the ranges" | **Closed by the data.** Pool host cell protein now sets the pH PAR and the load NOR. |
| Note: "every output" in F8 and Conclusion 5 | **Closed.** "every output with a criterion". |
| Note: revision history omits INV-002 | **Partly closed.** It now reads "Reissued under INV-001 and INV-002". |
| Note: `D.governing_factor` for fragments | **Closed.** The brief no longer names one for fragments, and the report plots pH (largest effect, 0.054 against 0.028). |
| Could not check: "PCP-005 §8.1" | **Closed.** The revised plan has §8.1 "Intermediate acceptance criteria". |
| Could not check: S-PA-RET in PCP-005 Version 2.0 | **Closed.** PCP-005 §1.1 item 3 and Table 11.1 include it. |
| Could not check: screening pools "not retained" | **Closed.** PCP-005 §1.1 item 3 and PCMP-001 §7.8 say so. |
| Could not check: case-study attributions | **Closed.** All three are in `refs/text/amab.txt`: no claim for viral clearance at Protein A (p. 118); no significant effect on aggregate (p. 123); "roughly 50 %" at the edge of a mean-based region (p. 59). Robustness to feed inputs is also there (p. 125). |
| Could not check: INV-001 finding numbers | **Closed.** Findings 1, 2, 4, 5 and 6 are used with the meanings STORY_BIBLE §9b gives them. |
| Note: coefficients change "by at most 3 %" | **Open (rounding).** The largest change is still 3.12 %: protein load, with run 6 deleted. |
| Note: the brief's SOP/AMV subset | **Open (brief).** It still omits SOP-3015, SOP-3016, AMV-3013 and AMV-3019. All four are in the PCMP-001 register (Table 5.2) with the titles the report prints. |
| Could not check: "same laboratory columns", "same procedures" | **Open.** No source in the permitted files. |

## Errors

**1. Section 1.2 quotes the objectives "as PCP-005 §2 states them", but changes two of them**
- **Where:** Section 1.2, objectives 1 and 6.
- **What it says:**
  - Objective 1: "To estimate the offset between the scale-down model and manufacturing scale for each output that the qualification compares, and to qualify the model by that offset for each of these outputs with a criterion."
  - Objective 6: "...under SOP-4001, and to support the Stage 2 ranges and the control strategy."
- **What the plan says:** PCP-005 §2 (revised plan, p. 9):
  - Objective 1 is "To estimate, **before the first characterization run**, the offset ...". The report drops the timing. It is the very condition that the 6 runs of S-PA-SDM2 depart from (PD-005-01; PCMP-001 §7.1 has the same rule).
  - Objective 6 ends at "under the parameter classification procedure SOP-4001". The clause "and to support the Stage 2 ranges and the control strategy" is not in the plan.
  - Objective 4 also loses "from the response-surface models" and "at manufacturing scale where an offset applies". This is minor.
- **Fix:** Quote the six objectives as the plan words them, including "before the first characterization run" in objective 1. Delete the added clause of objective 6, or drop "as PCP-005 §2 states them".

**2. F9 and Conclusion 9 say the held eluate met the criteria for acidic variants, but Table 5.17 marks the acidic lower limit "No"**
- **Where:** Executive summary F9 and Section 12, Conclusion 9.
- **What they say:**
  - F9: "the eluate held ... met the criteria of the low-pH inactivation load for aggregate, acidic variants and fragments."
  - Conclusion 9: "an eluate made at set-point met the criteria of the low-pH inactivation load after 7 days".
- **What the document says:**
  - Table 5.17 has "Met: No" in both acidic-variant rows against the lower limit of ≥ 18 %, at 16.2 % and 16.1 %.
  - Section 5.7 states the same: "The lower limit of 18 % is not met before the hold".
  - What the hold rule supports is narrower. The change over the hold stays within each criterion, and the hold does not lower acidic variants.
- **Fix:** In F9 and Conclusion 9, write that what the hold adds keeps aggregate, fragments and acidic variants within their criteria. Then add that acidic variants can enter the hold below their lower limit, as F9 already says in its last sentence. Conclusion 9 needs that sentence too.

**3. The report measures the load mass for step yield by Protein A affinity HPLC, but PCP-005 plans A280, and no discrepancy is recorded**
- **Where:** Section 3.3 ("divided by the mass loaded, from the titre and the load volume"), Section 3.2, and Table D.1 ("Protein A affinity HPLC ... Protein load of each run, step yield").
- **What the plan says:** PCP-005 §5.3 says "Step yield is the mass of antibody in the pool divided by the mass loaded, **both from the protein concentration by absorbance at 280 nm** and the measured volumes." PCP-005 Table 5.1 lists step yield as A280 on the "Load and pool of every run".
- **The gap:**
  - Neither Section 13 nor Table 13.4 records the departure.
  - Under the canon in data-state §5, the plan keeps what Version 1.0 planned, and the report records the departure.
  - This is an unregistered plan/report inconsistency. CLAUDE.md treats one as a bug.
- **Fix:** Record the titre basis of the load mass as a discrepancy from PCP-005 §5.3. Alternatively, if Version 1.0 of the plan already named the titre method, correct the revised plan. The report's own text, which explains why A280 cannot measure antibody in a clarified harvest, is right.

**4. Section 2.2 counts 3 leached Protein A results above the drug substance limit, but there are 4**
- **Where:** Section 2.2: "leached Protein A in 3 of 47 with 1 more at 5.00 ppm".
- **What the data say:**
  - At manufacturing scale (scale-down result minus the 1.1802 ppm offset), 4 results exceed ≤ 5 ppm: screening 5.0024 and 5.0392, response surface 5.2445 and 5.7916.
  - The "5.00 ppm" result is screening run 6 (3.82 ppm in the scale-down model). It is 5.002 ppm, above the limit under the strict comparison that the engine uses (`_in_spec`).
  - The run-2 check verified "4 of 47".
- **Fix:** Write "leached Protein A in 4 of 47, one of them at 5.002 ppm". If the intent is a rounding convention, state the convention.

**5. Section 8 says the hold raises acidic variants, but Section 5.7 says it does not change them by more than the methods resolve**
- **Where:** Section 8, last paragraph: "The hold of the eluate raises acidic variants slightly (Section 5.7), which is away from the lower limit that sets the Cpk."
- **What the document says:** Section 5.7 says "Acidic variants changed by 0.3 points at both temperatures, less than the 0.6 points between the day 0 aliquots. The hold therefore did not change acidic variants by more than the methods and aliquots resolve."
- **Fix:** Write "The hold of the eluate does not lower acidic variants (Section 5.7), so it does not move them towards the lower limit that sets the Cpk."

**6. The fragment rise at 2-8 °C is said to be "no more than" the day-0 difference, but unrounded it is slightly more**
- **Where:** Section 5.7: "At 2-8 °C they changed by 0.08 points, no more than that difference."
- **What the data say:** In `hold_protein_a.csv` the rise at 2-8 °C is 0.0840 points (0.9070 to 0.9910). The day-0 aliquot difference is 0.0813 points (0.9070 against 0.8257). The two values are equal only after rounding.
- **Fix:** Write "about the same as that difference". The conclusion that the rise is not resolved still holds.

## Checked and correct

Apart from errors 1 to 6:

- **Scale-down qualification (Section 3.1, Tables 3.1 and 13.3, F1, Section 13.3.1).**
  - Values match `D.sdm_offset` and `D.offset_qualification`:
    - the ratio 0.973 (0.891 to 1.063), geometric means 7,701 and 7,911, 12 df;
    - leached Protein A 2.52 and 3.70, −1.18 (−1.97 to −0.39);
    - step yield, plates and asymmetry rows.
  - Upper prediction limits:
    - 15,697 and 17,143 ng/mg over the load NOR as characterized;
    - 15,349, 16,763 and 14,055 ng/mg over the NOR in force;
    - the load edge at which the low-end limit reaches the criterion is 39.81 g/L resin.
  - On the planned runs alone:
    - ratio 0.935 (0.795 to 1.100) and an upper limit of 18,786 ng/mg;
    - Table 13.3 "No / Yes / Yes";
    - leached Protein A −1.60 (−2.76 to −0.43);
    - the half-width 46 % narrower (45.7 %).
  - The four conditions of the qualification. The a priori criterion would fail at 16,763 ng/mg. Each scale-down leached Protein A run is below 3.70 ppm (highest 3.658).
- **Fragment bound from the harvest hold.** Fragments rose 0.55 points at 21 °C (1.1776 to 1.7295). Added to 1.0936 that gives 1.65 %.
- **Statistical methods (Section 3.5).**
  - Factors 2.43, 3.30 and 0.85.
  - Root mean square 679 and 957 ng/mg (41 %), and 0.067 and 0.074 on the log scale (10 %).
  - Box-Cox λ 0.06 (−0.32 to 0.42), and every other output's interval contains 1.
  - The set-point median 7,150 ng/mg (5,687 to 8,989).
  - The search:
    - 1,337 hierarchical models;
    - stepwise searches worse for 12 of 21 outputs (`D.selection_comparison`);
    - forward search stops at 4 terms for pool host cell protein;
    - backward search stops at 4 terms for leached Protein A and 5 for fragments.
  - 4/n = 0.14, and the Monte Carlo settings match PCMP-001 §6.4 and PCP-005 §8.2.
- **Results tables.**
  - Tables 5.1 to 5.5, 5.7 to 5.9, 5.11 to 5.13 and C.1 against the engine. Table 5.6 against the refits with run 23 at its recorded pH: 0.98, 0.89, 0.09; 0.57, −0.74, 1.30; 0.61, −1.28, 1.89. The step-yield gap is 0.31.
  - The BD p-value is 0.046, and 0.052 refitted from the yields rounded as printed.
  - 0.97 ppm is 44 % above 0.67 ppm.
  - The leached Protein A half-width is 0.67 ppm.
- **Table 5.10 and Section 5.3.1.**
  - All 9 models within 2 AICc units, with ΔAICc, upper limits at the estimate and at the low end, criteria 2 to 4 met, and the 2 "No".
  - AB p-values: at least 0.126 (0.144, 0.126, 0.164, 0.184); 0.156, 0.069 and 0.081 in the full log model; 0.064 and 0.071 in the selected models.
  - The pH effect is 14,081 and 5,804 ng/mg.
  - The flow curvature is 8 %, 14 % and at most 4 %.
  - 7 results above 17,069 ng/mg: 3 screening and 4 response-surface, at 17,150 to 25,800 ng/mg, all at 50 g/L resin and pH 3.2.
  - Pool host cell protein ranged from 2,149 to 25,114 ng/mg.
- **Section 5.3.2.** The step-yield claims: 5.0 and 2.3 points, −1.80 and 0.02. The six results at 99.0 % (5 design results and 1 univariate result), 5 of them at 3.2 CV.
- **Section 5.5 and Section 13.**
  - The residual trends, the 0.84 ppm drift (0.5 % of 158) and the fragment spread of 0.04 points.
  - The flagged runs are 6, 12 and 23 for pool host cell protein, run 7 for leached Protein A and run 1 for fragments.
  - Deleting a flagged run gives limits of 14,978 to 15,252 ng/mg, with at most 16,657 at the low end. Leached Protein A and fragments still meet their criteria.
  - The Cook's distance simulation gives 1.33 to 2.47 flagged runs and at least one flag in 87 % to 96 % of data sets.
  - Section 13.1: −0.21, 2.0 SD, 10,368, 8,390, 7,761 and Cook's distance 0.16. Table 13.2, and the load² term −0.11 with p = 0.018.
  - Section 13.2: 3.82, 5.00, 2.12, 3.30, ×1.8, p = 0.052 and p = 0.064.
- **Univariate study (Tables 5.14 and 5.15).** The differences, and the highest results at manufacturing scale, 10,488 ng/mg and 5.38 ppm.
- **Other measured results.**
  - Aggregate 1.40 to 1.73 %, DNA 137,045 to 234,778 and 498 to 1,372 pg/mg, a reduction of 2.2 to 2.5 log10.
  - Fragments 0.77 to 1.09 %, with an upper prediction limit of 1.09 % (1.0936).
- **Hold study (Section 5.7, Table 5.17).**
  - Aggregate 0.41 and 0.11. Day-0 differences 0.07, 0.6 and 0.08. Fragments +0.25.
  - The entering levels match `D.nor_prediction_limit` and `D.nor_worst_corner` on the bioreactor model: 2.35, 30.3 and 16.2. The corner is pH 6.95, 34.5 °C, 18 days and 130 mmHg, with a median of 18.4 %.
  - The low-pH hold NOR is 100 to 120 min against a range of 60 to 180 min.
- **Design space (Section 6, F7, Section 7.3, Conclusion 6).** On the 41-point grid:
  - 98.3 %, beyond 42.4 g/L resin at pH 3.2, and below pH 3.30 at 50 g/L resin;
  - medians 20,217 and 11,269 ng/mg and an upper limit of 25,690 ng/mg;
  - 96.6 to 98.8 % and 92.7 to 98.5 % at the corners;
  - 97.5 % in 4 dimensions, at 33 g/L resin or more with pH 3.41 or less;
  - no excluded point inside both NORs;
  - with the other two factors within their NORs, at 39 g/L resin or more with pH 3.34 or less;
  - NOR medians 4,259 to 12,201 ng/mg.
- **Section 7 and Tables 7.1 to 7.3.**
  - Every Table 7.1 value against `D.iac_verification()`.
  - 171-fold, 427 and 109 ng/mg.
  - Table 7.2: fragments 0.92 and 0.89 to 0.96, leached Protein A 4.12, and the limits 15,349, 5.52 and 1.09.
  - The pH PAR 3.21 (3.209) and 3.25 without CA3 (3.244, rounded inward like every PAR). Without CA3 the NOR conclusion is unchanged and the scale-down model is not qualified.
  - The margins 0.009, 0.19 and 0.34.
  - The fragment-model gaps of 0.21 (cation exchange) and 0.33 (low pH).
  - The anion exchange full quadratic fails §7.2 (gap 0.27).
  - The aggregate derivation: 6.46 and 9.30, and 0.84 and 0.53.
- **Capability (Section 8, Table 8.1).** Cpk 6.17, 10.62, 10.81 and 1.05. 821 per million. Leached Protein A mean 0.003 ppm. 0.15 % at 95 %. DNA reductions in the config: 2.5, 1.5 and 4.0 log10.
- **Plan and master-plan citations.**
  - Every PCP-005 citation exists with the number and meaning used: §2 (but see error 1), §4.1, §5.1, §5.5 ("15 terms"), §6.2, §6.4, §7 criteria 1 to 7 (criterion 7, classification), §8.1 and §8.2 ("set-point analysis").
  - So does every PCMP-001 citation: §5, §6, §6.4, §7.1, §7.2, §7.3, §7.5 (the three reasons and the four parts of the risk argument), §7.6, §7.7, §7.8 and §7.9.
  - The plan's Table 7.1 note c gives the one-sided 97.5 % limit.
- **Dates.**
  - PCP-005 was approved on 2025-11-03, before the first study on 2025-11-05.
  - AMD-001 (2026-03-20) came after S-PA-SDM and before S-PA-RET.
  - S-PA-SDM2 ran while INV-001 was open. S-PA-HLD started after INV-001 closed (09-19 against 09-18).
  - CA3 was adopted on 2026-09-15. S-AEX-AUG ended 2026-09-24, after INV-001 closed.
  - Every study ended before 2026-09-30.

## Notes, not counted

- **Table 7.1 note b is stale in the render.** It says the low-pH acidic model "fails an adequacy test of PCMP-001". The prose of Section 7.1 says, correctly, that an exact fit "cannot be judged adequate". `tables.py` changed at 20:20, after the 20:15 render, and its note now covers the exact fit. A re-render fixes it.
- **Hold changes for acidic variants are taken from the rounded table values.** The Table 5.17 footnote declares this.
  - Unrounded, the rises are 0.28 points at 2-8 °C and 0.23 points at 21 °C, not "0.3 at both".
  - The largest fall is 0.16 points, not 0.1.
  - No conclusion changes, because each is below the 0.61-point day-0 difference.
- **"The coefficients ... change by at most 3 %".** The largest change is 3.12 % (see the status table).
- **Section 7.1 gives the anion exchange adequacy statistics on the 28 planned runs** (gap 0.024, lack of fit p 0.824). On all 40 runs they are 0.021 and 0.842. The sentence names its basis, so this is not an error.

## Could not check

- **PCR-003.** The statement that PCR-003 accepts the acidic-variant corner as the producer's risk, with alarm limits on culture pH, pCO2 and osmolality, and with monitoring at harvest.
- **Statements about how the studies were run, with no source in the permitted files:**
  - the offset "was measured on the same laboratory columns as the designs";
  - the S-PA-SDM2 runs used "the same procedures as the planned runs".

(Checked after the first write and found correct:
- the ELISA precision of 9.5 %, the HPLC precision of 2.0 % and the ELISA LOQ of 1.0 ng/mg, against `config` `analytics` (AMV-3012 and AMV-3021);
- "at most 2.5 %" host cell protein in the pool. The highest scale-down result, 25,114 ng/mg, is 2.51 %, and A280 is read on the scale-down pool.)
- **Whether PCP-005 Version 1.0 named the titre method for the load mass.** This decides how error 3 is fixed.
