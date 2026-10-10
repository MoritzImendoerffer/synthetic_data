# Content review of PCR-003 Version 2.0, draft run 2 (2026-10-10)

Judge: Claude Opus 5.5 (a09515a806ce2f416), read only `PCR-003_bioreactor.DRAFT.run2.txt` (3,333 lines); figures
judged on captions. Saved by the coordinator from the agent's hand-back. Statistical and procedural "because"
clauses not flagged under Q1.

Most serious (judge's summary): two statements contradict the document's tables (§1.1, §7.1); PD-003-03 and
PD-003-04 are deviations by the document's own definition [coordinator: superseded by the owner's decision of
2026-10-10, no deviations in a characterization report]; a risk argument in §7.1 has batches failing at a step with
no test; three classes go against the document's decision logic; pH controlled by CO2 while pCO2 is an independent
factor; the initial viable cell concentration effect is one significant result in 20 tests; the report's own
effect-size bands decide the classes; the mitigation has no limit values.

## Q1. Physical cause with a direction
1. "…so the culture sets the levels at which both enter purification." (§1.1)
2. "The culture also sets the amount of host cell protein and DNA that the purification steps have to clear." (§1.1;
   lysis only in §2.1)
3. "The glycan attributes are set by the enzymes of the Golgi." (§2.1; no direction)
4. "Culture pH, temperature, pCO2 and osmolality act on the same enzymes and donor pools through the growth rate and
   the intracellular pH, so their effects on the glycans are expected to interact." (§2.1; no direction)
5. "…while pCO2 and osmolality act on the intracellular pH and on sialylation." (§2.1)
6. "Dissolved carbon dioxide acidifies the cytosol, so a higher pCO2 is expected to act on the Golgi enzymes in the
   same direction as a lower culture pH." (§2.1; the effect of a lower pH is never stated)
7. "The initial viable cell concentration sets where on the growth curve the culture starts." (§2.1)
8. "Afucosylation and galactosylation are linked to efficacy, because A-Mab acts mainly through ADCC." (§2.2;
   galactosylation has no mechanism or direction anywhere)
9. "Each of them changes the pH of the Golgi or the size of the nucleotide sugar pools." (§2.3; wrong for culture
   duration, which §2.1 says acts by weighting the pool toward late antibody)
10. "…and there the large effects of pCO2 and culture pH set the edges of its PARs (Section 7.3)." (§5.3.3)
11. "Culture pH acts on the same enzyme through the pH of the Golgi, so an interaction was expected, but the study
    does not show which property of the cell sets its size." (§5.6)
12. "…because sialylation and glycation respond differently, and the study does not identify which route
    dominates." (§5.6)
13. "Routine operation is therefore limited by acidic variants, and the control strategy acts on that corner
    (Section 10)." (§5.6)
14. "…including osmolality, which acts on acidic variants in the integrated model." (§8)
15. minor: "Acidic variants decide its boundary." (§6, executive summary, Conclusion 2)

## Q2. Terms of art
1. "The NOR-propagated PAR is the one that supports a claim." (§3.5; also "NOR-propagated analysis")
2. "The set-point analysis holds the other factors at their set-points…" (§3.5)
3. "Every selected model meets the model F-test, the lack-of-fit test and the limit on overfitting of PCMP-001
   §7.2." (executive summary; "limit on overfitting")
4. "…do not meet the criterion on residuals and influential runs…" (throughout)
5. "The design space, judged on the same single-batch interval, covers 73.7 % of the region studied…"
6. "Its PAR for acidic variants ends 0.15 routine standard deviations above the NOR high." (§9; also "2.25 routine
   standard deviations")
7. "The lower limit is carried back unchanged, which assumes that no downstream step lowers acidic variants
   (PCP-003 §12)." (§7.1; "carried back" also Tables 1.2, 7.1; usual: back-calculated)
8. "Near-equivalent models" and "Within 2 AICc units of the selected models lie 15 other models…" (§5.3.5)
9. "The widening alone moves the criterion 0.14 points back toward the patient." (§7.1; consumer's / producer's risk)
10. Abbreviation list "Man5 high mannose, in the headers of the design tables" (Man5 is one glycoform; no table uses
    it) [coordinator: the design tables now say "High mannose"; drop the abbreviation]
11. "PCP-003 §7 requires the NOR to lie inside the declared operating region, and the NOR to be narrowed until it
    does." (§7.2; "declared operating region")
12. Table 13.1 (DEV-003-09) "judged through its offset under the offset rule of PCMP-001 Version 2.0" [coordinator:
    the entry is now PD-003-13]
13. Table 7.1 footnote b "a downstream step’s A-Mab worst case within its NOR"
14. minor: "High mannose species are cleared from the circulation faster than the processed glycoforms…" (§2.2;
    complex-type glycoforms)

## Q3. Filing sentences
1. "The selected model decides, and the others are a sensitivity analysis. A feature that only some of them carry is
   not reported as a finding." (§3.5)
2. "…so the other terms are not reported as findings." (§5.3.3)
3. "…and these bands are its own." (§5.3.3)
4. "This test is the report's own approach." (§3.5)
5. "The capability of Section 8 comes from the integrated model and does not depend on these runs." (§5.3.2)
6. "…so it is shown here for comparison only." (§6)
7. "The design space is not the product of the PARs of Section 7.3." (§6)
8. "This ground therefore does not support the decision on its own." (§7.2)
9. "…so its Cpk of 15.7 mainly reflects that distance." (§8)
10. "The expectation and the class conflict, and the data of this study cannot resolve it." (§9, twice)
11. "On all runs every PAR contains the NOR, a result that rests on the augmentation runs and the model selection."
    (Conclusion 3)
12. "…short of the NOR high, which is the result INV-001 gives." (§1.4)
13. "That use is the discrepancy PD-003-04." and "The duplicate runs that the test needs are the discrepancy
    PD-003-05." (§3.5)
14. "The screening model identifies effects." (§5.2)

## Q4. Criteria and results
1. "This report reads a change of a fifth of the width or more as large, of a tenth to a fifth as moderate and of
   less than a tenth as small, and these bands are its own." (§5.3.3; bands set at analysis decide the classes, §9)
2. "This test is the report's own approach." (§3.5; univariate rule chosen at analysis)
3. "…with the size of each residual trend compared with the criterion of its output." (§3.5; no threshold; §5.3.2
   "nearly the same" for 1.07 against 1.09)
4. Criterion (e) "The normal quantile plot of the residuals shows no departure from normality." reported as "…with no
   marked departure from normality, so the normality criterion is met." (§5.3.2; visual, weaker wording)
5. "The models of high mannose and aggregate predict them poorly, with a root mean square error of prediction 1.7 and
   1.8 times their residual standard deviation." (§5.3.4; no criterion or consequence; aggregate 11 of 16 inside the
   95 % interval, Table 5.9)
6. "A NOR is the range in which the process is routinely controlled, and narrowing it was judged impractical."
   (§7.2; no basis for setting aside the narrowing rule)
7. "Their values are not in the record of this step." (§10, alarm limits) and "…and the record of this step gives no
   action limit for it." (§10; the mitigation has no limits)
8. "The glycan results of the batch were confirmed by three determinations by the glycan map (SOP-3010, validated
   under AMV-3010)." (§13.2; no criterion for "confirmed")
9. minor: "…the smallest number for which the straight-line prediction at the NOR high has a standard error of at
   most 0.5 times the standard deviation between runs." (§4.5) and "…to give a probability of at least 0.90" (§4.3)

## Q5. Contradicted or wrong
Contradicted by the document:
1. "The production bioreactor is the only step of the A-Mab drug substance process at which product quality
   attributes are formed." (§1.1) vs Table 7.1 and §7.1 (low pH adds 1.00 point acidic variants, 0.56 aggregate) and
   §2.2 ("The CQA register assigns fragments to harvest") [coordinator: D-002, registered; keep the sentence exactly,
   fix only the elaboration after it]
2. "In the low-pH response-surface design every run at the same hold time gave the same acidic-variant result, so the
   full quadratic model reproduces the results exactly, cannot be judged against PCMP-001 §7.2, and the platform value
   stands." vs "The aggregate criterion would then be 6.19 % and the upper limit of acidic variants 39.6 %." (§7.1);
   identical icIEF results implausible at 2 % relative precision (Table D.1)
3. "A discrepancy from the plan is work that the plan did not foresee, with no such departure." (§13) vs PD-003-03
   and PD-003-04 [coordinator: superseded, see the record rule]
4. "The net change is a tightening, so more batches would fail at this step and fewer would reach the patient with
   too much aggregate, and the risk moves toward the producer." vs "This report sets no in-process test of aggregate
   at harvest, so an excursion beyond the criterion would be detected at release…" (§7.1)
5. "Osmolality is a WC-CPP." (§9) vs the section's own rule ("It is a WC-CPP when that risk is low, because the
   parameter is readily controlled and its PAR is wide against its NOR"; "…so the wide PAR that PCMP-001 §7.7 names
   for a WC-CPP cannot be shown for it"); "Dissolved oxygen is a KPP." (no process-performance effect shown or
   expected); "Basal medium concentration is a GPP." (the plan expects an effect on growth and titre); Table 4.1
6. "…because the spread of their residuals grows with the predicted value…" (executive summary, Discussion item 2)
   vs §5.3.2 ("1.07 points in the lower half ... and 1.09 points in the upper half, nearly the same")
7. "The screening design included three centre points, run at positions 11, 15 and 19 of its 19 runs." and "The
   response-surface design included four, run at positions 3, 4, 8 and 25 of its 28 runs." (§3.4) vs Table A.1
   (centre points 17–19) and B.1 (25–28): run numbers in Table 5.5 cannot be placed in run order
8. "Judged on the 95 % prediction interval of a single batch at manufacturing scale" vs Table 7.2 footnote b
   ("interval of a single run (t quantile, coefficient and residual uncertainty)"; no batch-to-batch variance, no
   offset uncertainty)
9. Table 13.1 DEV-003-04 disposition ("accepted on risk as the producer's risk with an osmolality alarm inside the
   NOR") vs §7.2 and §10 (alarms on pH, pCO2 and osmolality plus monitoring at harvest)
10. "Osmolality was held constant while pCO2 varied in these designs, so a rise of osmolality does not explain it."
    (§5.6) vs Table A.1 (osmolality is factor D at 360 and 440 mOsm/kg)
11. "Acidic variants were printed with a two-sided range and assessed against its upper end alone (finding 4)"
    (§1.4) vs Table 1.2 ("≤ 25.8", one-sided)
12. "…and across the ranges studied the feed replenishes those components faster than the cells use them." vs "The
    donor and the manganese cofactor of the enzyme are depleted late in a fed-batch culture, so galactosylation is
    expected to fall as the culture ages." (§2.1; §5.6 relies on the second; no metabolite data, DEV-003-05)
Scientifically wrong or unsupported:
13. "Culture pH was controlled by carbon dioxide and base addition, temperature by the vessel jacket and dissolved
    oxygen by sparging and agitation." with "…with pCO2 held at its level by the sparge." (§3.2): CO2 cannot be both
    the pH actuator and an independently held factor; how were pH 6.6 / 40 mmHg runs held (Table B.1 runs 1, 3, 5,
    7)? §9 repeats "readily controlled by carbon dioxide and base addition".
14. "The difference is significant at α = 0.05 for a single parameter and attribute." (§5.4) and "It raises acidic
    variants, an attribute of very low criticality, by 3.51 points across its range" (§9): one significant result in
    20 tests (28 with HCP and DNA, Table 5.11); p = 0.009 fails Bonferroni 0.0025; about one false positive expected;
    DEV-003-07 and the 17.69 % projection rest on it.
15. "At the least favourable NOR combination of the other parameters, osmolality at its NOR high therefore takes the
    mean of acidic variants below the lower limit." (§5.5; §8, §13.10): slope p = 0.191 (Table 5.12); "Mean" values
    19.1, 18.4, 17.7 are fitted line values.
16. "There the predicted median at manufacturing scale is 18.39 %, above the lower limit" (§7.2): the 0.39-point
    margin is smaller than the model bias at the set-point (22.23 % predicted vs centre-point mean 21.50 %, §5.3.1,
    Table 5.1; 22.8 % Table 7.2 vs 21.85 % manufacturing batches, Table 3.1); afucosylation 8.29 vs 7.61 (SE 0.18) not
    discussed.
17. "The residual of run 4 on the screening model is at most 0.16 times the residual standard deviation for any
    attribute." (§13.1): with 16 terms on 19 runs each factorial run has leverage about 0.99, so its residual is near
    zero whatever the run did.
18. minor: "The glycan distribution is completed in the Golgi before the antibody is secreted" (§1.1; glycosidases
    from lysed cells can trim glycans in the culture fluid)
19. minor: residual DNA "≤ 0.001 ng/dose" (Table 2.1) 10,000 times below the usual 10 ng/dose; check the unit
    [coordinator: A-Mab's claimed range < 10^-3 ng/dose, met through clearance; state the source and the dose]
20. minor: "For galactosylation, for example, a difference smaller than 3.1 points between the two ends of a range
    would not have been detected." (§5.4): detected about half the time at 3.1; about 4.3 at 80 % power.

## Q6. Machine-written
1. "The conclusions are stated for the commercial process and are bounded by the scale-down model on which they rest
   (Section 3.1)." (§1.3)
2. One point about eight times: "That containment rests on the 16 augmentation runs and on the model selection."
   (executive summary; §1.4, §5.3.4, §7.2, Discussion item 1, Conclusion 3, §13.8, §13.11)
3. "Read so, the effects of culture duration on afucosylation, culture duration on galactosylation, culture pH on high
   mannose, culture pH on acidic variants and pCO2 on acidic variants are large." (§5.3.3; restates Table 5.6)
4. "The deletions cover the conclusions over the NOR, the PARs and the design space." (§5.3.2)
5. "They changed what the models of this step predict, and with it the headline results." (§5.3.4)
6. "Standard deviations from four and three runs are imprecise." (§5.1)
7. "With the precision of the method, three determinations give a 95 % confidence interval of ± 6.21 % of the
   result." (§13.2)
8. "The expectation and the class conflict, and the data of this study cannot resolve it." (§9, twice)
9. "The study does not explain the direction." and "The mechanism does not explain the direction of the pCO2
   effects." (§5.6; five paragraphs end on "does not show/explain")
10. "INV-002 also refitted each failing planned model by hierarchical backward elimination, to simulate the
    augmentation." (§3.5)
11. "A NOR is the range in which the process is routinely controlled, and narrowing it was judged impractical."
    (§7.2)
12. "…so its Cpk of 15.7 mainly reflects that distance." (§8)
13. "The results roll up into PCMR-001." (Conclusion 8; executive summary; §1.1)
14. "Each figure also plots the standardized residuals against the predicted values and the predicted against the
    measured values, on the scale of the model." (§5.3.2)

## Q7. Cannot stand alone
1. "The response-surface model of each of the five modelled attributes was selected on all 44 runs by the procedure
   of INV-002 corrective action CA3." (name the procedure)
2. "Every selected model meets the model F-test, the lack-of-fit test and the limit on overfitting of PCMP-001
   §7.2." (state the limit)
3. "With each run flagged by its Cook's distance deleted in turn, no conclusion over the normal operating range (NOR)
   and no proven acceptable range (PAR) changed." ("conclusion over the NOR" stand-in; also §3.1, §5.3.2, §7.1, §11,
   §13.13)
4. "That containment rests on the 16 augmentation runs and on the model selection." ("That every PAR contains the
   NOR")
5. "The departures from PCP-003 found in the re-analysis are recorded as the deviations DEV-003-03 to DEV-003-09, and
   the further discrepancies from the plan as PD-003-05 and PD-003-06 (Section 13)." [coordinator: now PD-003-07 to
   PD-003-13]
6. "The analytical method decision AMD-001 of 2026-03-20 changes no method of this report (Table 3.3)."
7. "…were assigned to univariate study, for the reason given in Section 2.1." (§2.3)
8. "That use is the discrepancy PD-003-04."
9. "The rule that sent these models to augmentation was decided on 2026-09-02, after the results of the planned runs
   were known and before any augmentation run was made." (state the rule)
10. "Every model has at least one run above 4/n = 0.091, with 17 flags on 13 runs in all."
11. "The deletions cover the conclusions over the NOR, the PARs and the design space."
12. "They changed what the models of this step predict, and with it the headline results."
13. "The response-surface and osmolality studies ran at the set-point of this parameter, so the judgement of Section
    7.2 does not include the effect."
14. "PCP-003 §7 requires the NOR to lie inside the declared operating region, and the NOR to be narrowed until it
    does."
15. "PCMR-001 consolidates this capability with the risk decision of Section 7.2."
16. "The mechanism of Section 2.1 predicts the opposite direction."
17. "…which added an osmolality alarm to the mitigation of Section 7.2." (§13.10)
18. "…the judgement over the NOR is the same for both attributes (Section 5.3.2)." (§13.13)
19. "…the study is complete except for the operating region, which does not contain the NOR for acidic variants"
    (Conclusion 7; "the operating region" never defined)

## Hard-to-read tables and figures
Table 1.2 (rule codes R1, R2 only in footnotes; footnote marks break the aggregate cell; glycan ranges labelled R2
though their lower ends are drug substance limits); Table 3.1 (one Offset column mixes differences and ratios, caption
defines a difference; merged run counts; dense "Yes / Yes / Yes"); Table 3.3 (a table for one method; does not show
what AMD-001 changed); Table 5.2 (attribute labels centred in merged blocks of up to 12 rows; effects sorted by p; two
non-significant screening models unmarked); Table 5.3 (ten columns; wrapped λ intervals; garbled "Pred. R² minus R²"
header); Table 5.4 ("Model used" mixes term counts with a seven-line term list; half-width columns; page number
inside); Table 5.5 ("p" is a p-value in "Spread p" and the number of parameters in "F(p, n − p)"); Table 5.9 (mixes
planned-run measures with the block p of the all-runs model); Tables 5.10 and 5.11 (broken merged cells, no verdict
column; percentages mixed with six-digit HCP and DNA); Table 5.12 ("Mean" holds fitted values); Table 7.1 (does not
show that the acidic-variant increase applies to the upper limit only; 6.46 % not recomputable: 5.00 × 1.40 − 0.56 =
6.44); Table 7.2 (mean range 18.4–26.7 inside 18.0–39.0 but verdict "No"; the deciding limit 16.25 % not shown);
Table 7.3 (twenty rows, two informative cells; range studied not shown); Table 8.1 (DNA as 0.00017 and 0.000038; tail
0.00317 per million; footnote "the dose in the text"); Tables 13.1 and 13.2 (long sentences in narrow cells; PD-003-04
"Done" about 35 lines); Tables A.1, B.1, B.2 (Run is not run order; factor columns A, B, E, C; run 4 shows 160 mmHg,
the analysis uses 153.5); Tables 5.7 and C.1–C.13 (coded letters, four decimals; C.1–C.5 sorted by p); Figure 5.6
(scale-down values before the offset); Figure 6.1 (grid covers only the NOR of pH and pCO2).

## Answers
1 No; 2 No; 3 Yes; 4 No; 5 Yes; 6 No; 7 No.
