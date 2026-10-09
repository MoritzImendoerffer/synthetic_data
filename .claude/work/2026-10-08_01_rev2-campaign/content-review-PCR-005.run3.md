# Content review: PCR-005 Protein A chromatography (draft), run 3

- Reviewer: Claude Opus 5.5 (model ID `claude-opus-5-5`), 2026-10-09.
- Source read: `.claude/work/2026-10-08_01_rev2-campaign/PCR-005_protein_a.DRAFT.txt` only.
- Checks: refits in Python (numpy, scipy) from numbers printed in the document only: Appendix A, Appendix B, Tables 3.1, 5.1 to 5.16, 7.1, 8.1, 13.2 and 13.4. Run 23 is coded at pH 3.38 unless stated otherwise. AICc counts σ² as a parameter, as in Burnham and Anderson.

## Answers

| Question | Answer |
|---|---|
| 1. Each cause names a physical cause in its clause | **No** |
| 2. Every technical term is a term of art | **No** |
| 3. A sentence tells the reader how to file its finding | **Yes** |
| 4. Every criterion has its basis, and every result is met or not met | **No** |
| 5. A statement is wrong or contradicted by a table or figure | **Yes** |
| 6. No sentence reads as machine-written (yes = none flagged) | **No** |
| 7. Every sentence stands alone (yes = none flagged) | **No** |

## Numbers that reproduce

These checks passed. They are listed so that the author knows which numbers are solid.

- Screening: Table 5.3 (pool HCP, leached Protein A), Table 5.4 and Table C.1 reproduce from Appendix A to the printed digits.
- Pool HCP, log scale, run 23 at 3.38. Box-Cox λ = 0.06, with an interval of −0.33 to 0.42. The coefficients, standard errors and p-values of Table 5.8 reproduce, as does the ANOVA of Table 5.9 (lack of fit F 5.70, p 0.088). R² is 0.977, adjusted R² 0.971 and predicted R² 0.963. The raw-scale full quadratic gives lack of fit p = 0.024.
- Table 13.2 reproduces in full. That covers the selected terms, the p of AB (0.156, 0.069, 0.081), the upper prediction limits (15,697, 15,423 and 15,497 ng/mg) and the low-end limits.
- Influence deletions: 15,308 to 15,554 ng/mg. The coefficients of A and B change by at most 3.1 % and 2.2 %.
- Pool HCP medians at manufacturing scale: 4,259 to 12,474 ng/mg over the NOR, 7,150 at the set-point, 20,216 at the corner and 11,520 at the NOR corner. The design-space fractions reproduce (100 %, 99.9 to 100 %, 98.8 to 100 %, 99.9 %), and so does the excluded region (≥ 44 g/L resin, ≤ pH 3.27).
- Cook's distances in Table 5.12 reproduce (largest values, runs and counts), and so does the HCP trend on predicted (p = 0.463).
- Leached Protein A: mean 2.94 ppm, SD 0.67 ppm, predicted R² −0.075, lack of fit p = 0.906, upper prediction limit 5.52 ppm at manufacturing scale.
- Step yield and fragment models: every statistic lies within the rounding of the appendix values. I checked this by perturbing each value within its last printed digit.
- Screening against the response-surface model: the ratio rises by a factor of 1.22 across end of pool collect (p = 0.021). The model predicts −1,644 ng/mg for the screening effect of end of pool collect, against +708 ± 700.
- Also reproduced: the sums of Table 5.16; the criteria arithmetic (16,000, 9.30, 2.45, 158); the Δ values and confidence intervals of Table 5.13 (pooled SD, 3 df); the Cpk for HCP (6.14); the 0.15 % bound; and the 46 % reduction in the half-width of the offset interval.

## Question 1: physical cause in the clause

Most causal sentences pass. Examples that pass are pore diffusion and dynamic binding capacity, cleaved ligand that still binds Fc, protease clipping, residence time and breakthrough, and early desorption at the elution front. The six below do not.

1. "On the log scale this interaction is not significant, because the two effects multiply (Section 5.3.1)." (1.4)
   Q1: the "because" gives a mathematical form, not a physical cause. The physical reason (Section 5.8) is absent, and the claim is also circular (see Q5).
2. "Load flow rate acts on pool host cell protein only through a small curvature, with a rise at both ends of its range." (5.8)
   Q1: "acts on ... through a small curvature" names a model term, not a species, an interaction or a property of the resin.
3. "The two effects of protein load expected in Section 2 act in opposite directions." (5.8)
   Q1: the clause names no cause. The two effects are referred to by section number and named only in the next sentence.
4. "It is consistent with effects that multiply, because the load then sets how much host cell protein is held weakly on the column and the elution pH sets the fraction of it that is released." (5.8)
   Q1: "sets" appears twice with no direction. The sentence does not say that more load holds more host cell protein, or that lower pH releases a larger fraction.
5. "As the load approaches the dynamic binding capacity, the mass transfer zone is expected to extend further down the bed, and host cell protein that the wash would otherwise displace is then carried into the eluate." (5.8)
   Q1: no interaction is named that explains why a longer mass transfer zone keeps the wash from displacing host cell protein.
6. "The expected cause is protease activity in the load." (3.1)
   Q1, minor: the clause names the agent but not the direction or the interaction. The longer hold and the cleaved ligand come two sentences later.

## Question 2: terms of art

1. "The NOR-propagated PAR is the range over which a single batch meets the criterion while the other parameters vary within their NORs (PCMP-001 §6.4)." (Executive summary, F7)
   Q2: "NOR-propagated PAR" is the document's coinage. The literature speaks of a multivariate PAR, or a PAR with the other parameters varied over their NORs.
2. "The set-point PAR is a univariate PAR with the other parameters at their set-points, judged on the mean prediction." (3.5)
   Q2: "set-point PAR" is coined. "Univariate PAR", which the sentence itself uses, is the term.
3. "Its rule gave no augmentation for leached Protein A, which showed no effect to resolve, or for fragments, whose assurance target could not be reached within the size of the planned design." (5.3)
   Q2: "assurance target" is not a term of art and is defined nowhere in the report.
4. "Host cell protein that rides on the antibody leaves with it at every pH studied and does not explain the pH effect." (5.8)
   Q2: "rides on" is colloquial. The term is product-associated host cell protein.
5. "Pool host cell protein is judged with a ratio offset and leached Protein A with a difference." (Conclusions, item 2)
   Q2: "ratio offset" is not standard. Say a multiplicative offset (the ratio of geometric means).
6. "In the full quadratic model the predicted R² of leached Protein A and of fragments is below zero, and both fail the limit on predictive power by a wide margin." (5.3)
   Q2, minor: "the limit on predictive power" is a house label. Say what it is: predicted R² no more than 0.20 below R².

## Question 3: telling the reader how to file a finding

1. "The Version 1.0 limit was never an approved criterion (INV-001 finding 1), so the wider criterion does not loosen an approved one." (1.4)
   Q3: a defensive gloss that answers an objection nobody has raised. It also passes over the fact that the criterion in force is wider than the a priori Version 2.0 criterion of ≤ 16,000 ng/mg.
2. "PCMP-001 is not changed by it." (3.5; repeated in 13.3.4 as "PCMP-001 is not changed.")
   Q3: answers an objection nobody raised.
3. "Their offset is unknown, not zero." (3.1)
   Q3, borderline: the gloss repairs a misreading that the previous sentence invites ("carry no offset"). Say "have no measured offset" once.
4. "The claim stops at the precision of the runs." (5.3.3)
   Q3: tells the reader how to file the no-dependence finding. State the smallest effect the design would have resolved instead.
5. "The hold therefore leaves the risk at the lower limit where the production bioreactor puts it." (5.7)
   Q3: files the lower-limit failure for acidic variants under another step, instead of stating what it means for the hold.
6. "The upper tail of the residuals is therefore shorter than a normal distribution gives, and the upper prediction limits, which assume a normal residual, are if anything conservative." (5.3.1)
   Q3: the trailing clause files the finding as reassuring. Nobody suggested that the limits were not conservative.
7. "the deviation record shows the buffer below its target pH; analysing the run at the recorded setting is the conservative reading" (Table 13.3, PD-005-03, Reason)
   Q3: renames the choice as "the conservative reading". That is true only of the upper prediction limit (Table 13.2), not of the model terms the choice changes.

## Question 4: criteria with their basis, results as met or not met

1. "The NOR-propagated PAR is the range of a parameter over which a single batch meets the criterion while the other parameters vary within their NORs." (3.5)
   Q4: the share of the 2,000 simulated batches that must meet the criterion at a grid point is not stated, so the PAR has no stated acceptance limit.
2. "Neither p-value is below 0.0071, the level at which 7 tests together keep a 5 % risk of a false call." (5.5)
   Q4: two trend tests fail criterion 5 at the planned α = 0.05. They are never reported as "not met" but are re-judged against a level the plan does not contain (see Q5).
3. "Each selected model meets the criteria." (5.3)
   Q4: the leached Protein A model has no F-test, so it cannot meet criterion 2 (a significant model F-test). Table 5.7 should show n.a. for that criterion, not "Yes".
4. "The hold criterion of PCP-005 is therefore met." (5.7)
   Q4: Table 5.16 reports "No" twice, and the verdict in the text does not carry it.
5. "At manufacturing scale every individual result met its criterion." (5.6)
   Q4: fragments have a criterion (≤ 2.45 %) but no result in S-PA-UNI. Report them as not tested, and limit the support to the attributes that were measured.
6. "The leached Protein A result of run 11 of the response-surface design was out of trend at analytical review." (13.2)
   Q4: neither the out-of-trend limit nor the original result is given.

## Question 5: wrong statements and contradictions

### Major

**The hold verdict against Table 5.16**

1. "Held at elution pH for 7 days at 2-8 °C or 21 °C, the Protein A eluate met the hold criterion of PCP-005 (criterion 7)." (Executive summary, F9)
   Q5: Table 5.16 is titled as the judgement against criterion 7 and shows "No" for acidic variants at the lower limit at both temperatures. Section 4.5 makes the lower limit part of the judgement.
2. "The hold criterion of PCP-005 is therefore met." (5.7)
   Q5: the same conflict with the two "No" rows of Table 5.16.
3. "The attribute closest to its criterion is acidic variants at 21 °C, at 31.2 % against ≤ 39.6 %." (5.7)
   Q5: Table 5.16 has acidic variants outside their criterion (16.1 % and 16.2 % against ≥ 18 %). The attribute nearest its limit is in fact the one that fails.
4. "A hold of 7 days at elution pH is supported at both 2-8 °C and 21 °C (finding F9)." (5.7)
   Q5: besides the conflict with Table 5.16, the claim generalises beyond what was tested. Only one eluate, made at set-point (pH 3.55), was held. Acid-driven aggregation and clipping are faster at the NOR-low pH of 3.4, and clipping by proteases may grow with pool host cell protein, so the measured increase does not bound a 7-day hold across the NOR.

**"No CPP"**

5. "No parameter of the step was classified as a CPP." (Executive summary)
   Q5: contradicted by the Abbreviations table, where a WC-CPP is a "well-controlled critical process parameter". Two parameters of the step are critical, and a reader will take "no CPP" to mean none is.
6. "In summary the step has 2 WC-CPPs, 2 KPPs and 2 GPPs, and no CPP." (9)
   Q5: same.
7. "The step has no CPP." (Conclusions, item 6)
   Q5: same.

**"The two effects multiply"**

8. "On the log scale this interaction is not significant, because the two effects multiply (Section 5.3.1)." (1.4)
   Q5: circular. The multiplication is inferred from the non-significance, and p = 0.156 is only absence of evidence. With run 23 at its design pH or excluded, p falls to 0.069 and 0.081 and AICc keeps the term (Table 13.2).
9. "On the raw scale the model of Version 1.0 described this as an interaction, and on the log scale none remains." (11)
   Q5: contradicted by Table 13.2, where the interaction is selected on the log scale in 2 of the 3 analyses of run 23. At the recorded pH, my refit puts models with AB within 1.1 and 1.4 AICc units of the selected model.
10. "The run is analysed at its recorded pH, and the conclusions are the same with the run at its design pH or excluded." (Executive summary)
   Q5: true only for the conclusion over the NOR. In Table 13.2 the selected model gains AB and A², so F3's "the selected model does not contain it" changes. In my refit at the design pH, A² has p = 0.018 in the selected model, so the load effect levels off.
11. "No single run therefore decides a conclusion of this report (finding F8)." (5.5)
   Q5: the same paragraph says that deleting run 23 adds AB and A² to the selected model. One run decides whether the model of pool host cell protein contains the interaction.
12. "Elution buffer pH and protein load have the largest effects on pool host cell protein, and the two effects multiply." (Conclusions, item 4)
   Q5: stated without the run 23 qualification that Section 5.3.1 gives.

Evidence (refit, run 23 at 3.38). The selected model is A, B, C, D, C². The nearest alternatives are:

- A, B, C, D, A², C²: ΔAICc 0.33.
- A, B, D, B²: ΔAICc 0.38.
- A, B, C, D, AB, C²: ΔAICc 1.06.
- A, B, C, D, AB, A², C²: ΔAICc 1.40.

If AICc counts only the coefficients, A, B, C, D, A², C² ranks first by 0.05. The report does not say which convention it used. Burnham and Anderson, whom it cites, treat a ΔAICc below 2 as substantial support, so the single selected model does not carry the weight these sentences put on it.

**Figure 5.1**

13. "The pool host cell protein panel shows the median of the log-scale model, whose straight and parallel contours are the mark of two effects that multiply." (5.3.1)
   Q5: wrong. Any model without an A×B term gives straight parallel contours on any monotone scale, an additive raw-scale model included. Here the selected model has no AB term by construction. Effects that multiply show in the spacing of evenly spaced contour levels (closer at high values), not in their straightness.

**Cook's distance and leverage**

14. "The factorial and axial runs of a face-centred design carry high leverage by construction." (5.5)
   Q5: in the selected HCP model the axial runs have below-average leverage (0.11 to 0.17; factorial runs 0.27 to 0.28; mean 0.21). The leached Protein A model has no term, so every run has the same leverage, 1/28.
15. "Cook’s distances above 4/n are therefore expected in this design, and the limit does not separate an influential run from a run at a corner." (5.5)
   Q5: run 7 of leached Protein A exceeds 4/n on its residual alone (+1.67 ppm, 2.5 SD, leverage 0.036). Run 1 of fragments has leverage 0.14. With n = 28 and normal residuals, the 4/n cut flags about 1.3, 1.6 and 2.1 runs for models of 1, 3 and 6 coefficients, in any design.
16. "The limit of 4/n is better suited to a design with low leverage than to a face-centred design, whose factorial and axial runs carry high leverage." (11)
   Q5: same evidence as items 14 and 15.
17. "A limit based on the leverage of each run would serve the purpose of the criterion better." (11)
   Q5: Cook's distance already combines leverage and residual. A limit on leverage alone would not have caught run 7 of leached Protein A.

**Residual trends**

18. "Neither p-value is below 0.0071, the level at which 7 tests together keep a 5 % risk of a false call." (5.5)
   Q5: criterion 5, as quoted in Section 3.5, applies per test at α = 0.05. The Bonferroni level was chosen after the results were seen, the same practice that INV-001 was opened over, and it is not recorded among PD-005-01 to PD-005-04.
19. "The two residual trends found are small against the criteria, and neither is significant once the number of tests is allowed for." (11)
   Q5: same.

**Fragments "at manufacturing scale"**

20. "Every range and every conclusion against a criterion in this report is therefore at manufacturing scale." (3.1)
   Q5: contradicted three paragraphs later ("Fragments therefore carry no offset ... Their offset is unknown, not zero"). The fragment conclusions are at scale-down, with an unknown offset.
21. "Each of the 3 outputs with a criterion met it across the NOR at manufacturing scale." (Executive summary, F7)
   Q5: same. Table 7.2 footnote a) and the legend of Table 7.3 repeat the claim.
22. "The proven acceptable ranges and the design space rest on the selected models and on a scale-down model qualified for each output that it compares at both scales." (Executive summary)
   Q5: the fragment PARs (Table 7.3) rest on a scale-down model that was never compared for fragments, so this reassurance does not cover them.

**Antibody in the load**

23. "In clarified harvest the absorbance at 280 nm also counts host cell protein and other species that absorb at that wavelength, and no method of this study measures the antibody in the load alone." (3.3)
   Q5: contradicted by the load value "pg per mg antibody" in Section 5.4 and by a protein load "set by the load volume and the titre" in Section 9. If the scale-down load was set from A280, the protein-load axis (g/L resin) is not the antibody load of the commercial NOR, and every load effect and PAR shifts.
24. "The load carried 137,045 to 234,778 pg per mg antibody and the pool 498 to 1,372 pg/mg, a reduction of 2.2 to 2.5 log10 across the step." (5.4)
   Q5: a per-mg-antibody value in the load needs the antibody in the load, which Section 3.3 says was not measured.
25. "The load is set by the load volume and the titre, and it is readily controlled within its NOR of 20–40 g/L resin, inside a PAR that spans the range studied of 10–50 g/L resin." (9)
   Q5: the titre is the measurement that Section 3.3 says this study did not make.

**The widened HCP criterion**

26. "The performance of both steps for A-Mab is known well enough to replace the platform values." (7.1)
   Q5: the A-Mab bounds are 95 % confidence bounds on the mean clearance at the worst NOR combination. The platform worst case they replace is an observed value, and the criterion is applied to a single batch; this report judges its own outputs on the prediction interval of a single run. A single batch can clear less than 41.8-fold or 5.18-fold, as the runs at the edges did (30.3-fold and 3.63-fold).
27. "Each bound is taken on its unfavourable side, at the least favourable combination of the NOR." (7.1)
   Q5: true of the mean, not of a batch, so it overstates the protection.
28. "For pool host cell protein the conclusion is the same at both ends of the offset interval, on the planned runs alone and on all runs." (11)
   Q5: this holds only under the widened criterion. Against the a priori ≤ 16,000 ng/mg, the upper prediction limit over the NOR is 15,697 ng/mg at the ratio estimate, but 17,143 at the low end and 19,212 on the planned runs (Table 13.2, Section 13.3.1). The scale-down model would then not be qualified for pool HCP. The report should say that the widening decides the qualification.
29. "PCMP-001 §7.3 derives them a priori from the drug substance criteria and the platform worst case of each downstream step, and PCMP-001 §7.5 lets the A-Mab results of a downstream step tighten or widen them (Section 7)." (1.4)
   Q5: "a priori" describes what the derivation uses, not when it was made. PCMP-001 Version 2.0 was issued under INV-001 after every run in this report had been made, so the widening rule was approved with the A-Mab results already known.

**Univariate ranges without fragments**

30. "No difference from the set-point runs was detected for operating temperature or bed height, and their ranges studied are supported with the other parameters at their set-points." (Conclusions, item 7)
   Q5: fragments have a criterion but were not measured in S-PA-UNI. The report's own mechanisms make both parameters relevant to fragments: hinge hydrolysis depends on temperature, and capture of Fc-bearing species depends on bed height and residence time (3 min at 10 cm).

**DEV-005-02**

31. "Both deviations were investigated and the affected data were retained." (Executive summary)
   Q5: the out-of-trend result of run 11 was set aside for the analysis on a cause that "was not confirmed" (13.2). Invalidating a result needs a confirmed assignable cause. Neither the original value nor an analysis that includes it is given, and the value bears on the run-order drift (p = 0.046) and on the no-term model.
32. "The leached Protein A result of run 11 that was out of trend was replaced by a re-assay on a suspected cause, and the re-assay result lies inside the range of the other runs (DEV-005-02)." (11)
   Q5: same.

### Minor

33. "The limit on how far predicted R² may fall short of R² guards against such overfitting (Montgomery 2017)." (3.5)
   Q5: the 0.2 rule is usually stated against adjusted R², as in the Design-Expert output that Montgomery reproduces. The cation exchange fragment model fails at 0.21 against R² (7.1), so which form applies decides whether its bound is credited.
34. "It has no effect on leached Protein A or fragments." (9, load flow rate)
   Q5: states the absence of a detected effect as the absence of an effect. Say "no effect detected within the range studied".
35. "SEC (AMV-3011) remains the method for aggregate, because no host cell protein elutes in its high molecular weight window." (3.3)
   Q5: an absolute claim with no data in the report. Host cell protein bound to the antibody, and host cell proteins larger than IgG, can elute in the HMW window.
36. "This agrees with the expectation that Protein A capture does not separate aggregate from monomer, and that the short time at elution pH in the column forms little." (5.4)
   Q5: aggregate was measured in the pools only, so the data cannot show that capture leaves aggregate unchanged.
37. "No criterion upstream of this step relies on a platform value of the Protein A step, so no Protein A value had to be checked against the A-Mab data." (7.1)
   Q5: the bioreactor-output criteria for aggregate and acidic variants rely on the assumption that capture leaves them unchanged (Section 4.5). This report does not check that assumption against the load.
38. "Both are in the scale-down model, so the offset cancels from the difference." (5.6)
   Q5: true for the additive offset of leached Protein A. The HCP offset is a ratio, which scales a difference rather than cancelling from it (negligible at 0.973, but inexact).
39. "With none of 2,000 outside, the probability of an out-of-specification batch is below 0.15 % at 95 % confidence." (8)
   Q5: this bounds the Monte Carlo error of the simulation, not the probability for real batches. The uncertainty of the integrated process model itself is not in the bound.
40. "It was made under the method decision AMD-001, which set nrCE-SDS as the method for fragments, and PCP-005 Version 2.0 includes it." (13.3)
   Q5: S-PA-RET ran in April 2026, under PCP-005 Version 1.0. A later plan version does not make it planned at the time, and S-PA-SDM2 is treated as a discrepancy on the same facts.
41. "Against the drug substance criteria at manufacturing scale, pool host cell protein would fail in all 47 results of the designs, leached Protein A in 4 of 47, and fragments in none of 28." (2.2)
   Q5: adding 1.18 ppm to the printed results, 3 exceed 5 ppm (5.04, 5.24 and 5.79). Screening run 6 equals 5.00 ppm, which meets ≤ 5 ppm.
42. "PD-005-02 records it for pool host cell protein, whose upper prediction limit over the NOR lies closest to its criterion." (13.3.2)
   Q5: Table 13.3 records PD-005-02 for every output with a criterion.
43. "For fragments it is the upper prediction limit of the fragment model of this step over its NOR (Section 5.3.4)." (4.5)
   Q5: Section 5.3.4 gives no prediction limit; its 1.09 % is the highest measured pool. The limit is quoted as 1.09 % in Section 3.1 and Table 5.16, and refits to 1.096 %.
44. "Residual DNA, which has no intermediate acceptance criterion, reaches a Cpk of 10.81 in the drug substance." (8)
   Q5: the simulation needs a DNA clearance for each downstream step, which Section 2.2 says the platform history does not give. The values used are not stated.

## Question 6: sentences that read as machine-written

1. "Model selection changed what the models of this step can support." (11)
   Q6: an empty topic sentence. The content arrives only in the next two sentences.
2. "The claim stops at the precision of the runs." (5.3.3)
   Q6: an aphorism. The next sentence says the same thing plainly.
3. "Its standard deviation at the centre points, 0.97 ppm, is no smaller than its standard deviation across all 28 runs of the design, 0.67 ppm." (5.1)
   Q6: hedged understatement, since the centre-point SD is 45 % larger. The consequence that matters goes unsaid: such pure error leaves the lack of fit test with no power.
4. "The upper tail of the residuals is therefore shorter than a normal distribution gives, and the upper prediction limits, which assume a normal residual, are if anything conservative." (5.3.1)
   Q6: "if anything" is hedged emphasis.
5. "The hold therefore leaves the risk at the lower limit where the production bioreactor puts it." (5.7)
   Q6: a figurative restatement of the two sentences before it.
6. "Each bound rests on a designed experiment that spans the NOR of its step and extends beyond it." / "Each model predicts left-out runs nearly as well as it fits its own runs." / "Each bound is taken on its unfavourable side, at the least favourable combination of the NOR." (7.1)
   Q6: a parallel triplet that restates the numbers of the two paragraphs before it (gaps 0.03 and 0.02, lowest value over the NOR).
7. "A limit based on the leverage of each run would serve the purpose of the criterion better." (11)
   Q6: a vague recommendation with nothing behind it (and wrong, see Q5).

## Question 7: sentences that do not stand alone

1. "INV-002 did not augment the Protein A design." (5.3)
   Q7: name the investigation and its augmentation rule.
2. "Its rule gave no augmentation for leached Protein A, which showed no effect to resolve, or for fragments, whose assurance target could not be reached within the size of the planned design." (5.3)
   Q7: say what the rule is and what the assurance target is.
3. "Table 5.7 judges each selected model against criteria 2 to 4 of PCP-005 §7, a significant model, no significant lack of fit and a predicted R² within the limit of R²." (5.3)
   Q7: "within the limit of R²" is unclear. Say "no more than 0.20 below R²".
4. "PD-005-02 records it for pool host cell protein, whose upper prediction limit over the NOR lies closest to its criterion." (13.3.2)
   Q7: a discrepancy code is the subject and "it" the object. Name the influence analysis.
5. "At this step every NOR-propagated PAR spans its range studied (Section 7), so criterion 8 identifies no parameter on its own." (9)
   Q7: name the rule ("the practical-relevance rule").
6. "The conclusion over the NOR and the qualification of the scale-down model are therefore the same however run 23 is analysed." (13.1)
   Q7: state the conclusion: pool HCP meets ≤ 21,662 ng/mg at every NOR combination.
7. "For leached Protein A (run 7) and fragments (run 1) the deletion leaves the conclusion unchanged as well." (5.5)
   Q7: state which conclusion.
8. "Model selection changed what the models of this step can support." (11)
   Q7: name the change. The leached Protein A and fragment models now pass and support PARs.
9. "One result does not follow the expectations." (11)
   Q7: name it: end of pool collect has opposite signs in the two designs.
10. "The other limitations are those the plan named." (11)
   Q7: name them in the sentence, or drop it.
11. "The broader mass transfer zone at a short residence time would explain a rise at high flow, and the mechanism of Section 2 predicts no rise at low flow." (5.8)
   Q7: name the mechanism (binding capacity limited by residence time).
12. "The two effects of protein load expected in Section 2 act in opposite directions." (5.8)
   Q7: name the two effects.
13. "PCR-003 accepts that corner on the PAR analysis of its plan, with alarm limits on culture pH and pCO2 inside the NOR on the side that lowers acidic variants, and with monitoring of acidic variants at harvest." (5.7)
   Q7: name the production bioreactor report, and say what "accepts that corner on the PAR analysis of its plan" means.
14. "No simulated batch of 2,000 fell outside the drug substance criterion of any of these attributes." (8)
   Q7: name the attributes (HCP, fragments, residual DNA). Acidic variants, also in Table 8.1, had one batch outside.
15. "Neither trend changes a conclusion." (5.5)
   Q7: state the conclusion (both outputs still meet their criteria over the NOR).
16. "Table 5.13 gives the results of study S-PA-UNI." (5.6)
   Q7: say "the univariate study".
17. "The NOR-propagated PAR is the one that supports a claim." (3.5)
   Q7: say which claim (a PAR carried into the control strategy).
18. "The register lists 2 deviations for the studies of the step." (Executive summary)
   Q7: say "the deviation register".
19. "The hold therefore leaves the risk at the lower limit where the production bioreactor puts it." (5.7)
   Q7: name the risk: acidic variants below 18 % at the least favourable bioreactor NOR corner.

## Table observations

- **Table 1.1:** no issues.
- **Table 1.2:**
  - In the extracted text the b) marker stands on its own line under "Rule"; check that it attaches to "none".
  - Footnote d) says "a downstream step" did better, but both cation exchange and anion exchange were credited (7.1).
  - "none" for leached Protein A sits badly with item 4 of 1.4, which says Version 1.0 judged it against ≤ 5 ppm. Show "≤ 5 (drug substance)".
  - "R1, margin 4.5" wraps, and needs a footnote before it can be read.
- **Table 2.1:**
  - Acidic variants are judged in this report (5.7, Table 5.16, Table 8.1) but are missing from the attributes in scope.
  - The "Tool #1" header should say what the number is (the Tool #1 score, impact × uncertainty).
  - "≤2%" lacks the spaces used elsewhere.
- **Tables 3.1 and 13.4:**
  - Title and legend say "scale-down minus manufacturing scale", but the HCP row is a ratio.
  - The "Met over NOR (low/est./high)" header runs to three lines.
  - The run counts (9 and 5; 3 and 5) are printed only in the leached Protein A row and read as if they belong to it.
  - ASCII hyphens serve as minus signs ("-1.18") where other tables use "−".
- **Table 3.2:**
  - SOP-3015 sits between the SOP and AMV groups, below SOP-4001, so its type is ambiguous.
  - The titles use "Host-Cell", "Size-Variants" and "Process-Parameter", against "host cell protein" in the text, and one method title contains "(ppm)".
- **Table 3.3:** no issues.
- **Tables 4.1, 4.2 and 4.3:** no issues.
- **Table 5.1:** fragments by nrCE-SDS, a response with a criterion, are missing. The four centre points in Appendix B give 0.89 % ± 0.077 (CV 8.6 %).
- **Table 5.2:** no issues.
- **Table 5.3:** no issues; it reproduces.
- **Table 5.4:** reproduces exactly.
- **Table 5.5:**
  - A refit from Appendix A gives BD p = 0.052, against 0.046 in the table, and effects that differ in the second decimal.
  - The difference lies within the rounding of yields printed to 0.1 %, but the significance call for BD cannot be reproduced from the appendix, and the text calls BD significant.
- **Table 5.6:**
  - "No effect" in the "Model used (terms)" column is a finding, not a model; write "intercept only".
  - The footnote "a block term kept (INV-002)" conflicts with 5.3, which says the design is one block.
  - The scale of the full quadratic (raw) is not stated.
  - For leached Protein A, R² 0.57 and Pred. R² −0.74 give a gap of 1.31, not the printed 1.30; a refit gives −0.73.
  - Step yield is omitted, though its full quadratic fails the 0.20 limit (refit: R² 0.92, predicted R² 0.61) and the KPP classes rest on the yield model.
- **Table 5.7:**
  - The three-line header splits its labels across lines (Adj./R², Pred./R², Model/p, LoF/p).
  - "Met: Yes" for leached Protein A, although criterion 2 is n.a. for a model with no term.
- **Table 5.8:** reproduces.
- **Table 5.9:** reproduces, but the precision is mixed (0.237, 0.2436, 0.006562).
- **Tables 5.10 and 5.11:** within the rounding of the appendix values.
- **Table 5.12:**
  - Run order is given nowhere (Appendix B lists run numbers only), so the run-order trends cannot be checked.
  - The fragment trend on predicted refits to p = 0.027 (0.021 in the table), within rounding.
- **Table 5.13:**
  - The values of the three reference runs are not shown.
  - The Δ values imply an arithmetic mean of about 7,414 ng/mg, while Table 13.4 gives 7,400 ng/mg for the same runs as a geometric mean. Say which mean each table uses.
- **Table 5.14:** no issues.
- **Table 5.15:** footnotes a) and b) run together on one line.
- **Table 5.16:**
  - The two "No" rows contradict the verdict in the text (Q5).
  - "Sum" is ambiguous; for the lower limit it is a difference. Call it "Level after the hold".
  - The title says criterion 7, while the text treats the lower-limit rows as outside criterion 7.
- **Table 7.1:**
  - The header runs to three lines, and the "Worst case" column holds the metric, not a worst case.
  - "At the edges" holds measured run values (7.1), while "Within the NOR" and "95 % bound" hold model values; the header does not say so.
  - "Confirmed, not widened" contradicts footnote b), which says the model fails an adequacy test. An inadequate model confirms nothing.
  - For acidic variants at low-pH viral inactivation, the 95 % bound equals the NOR value (0.40 and 0.40), which implies no estimation uncertainty.
  - The rounding footnote says a recomputed criterion "can differ in its last digit". But 100 × 41.8 × 5.18 = 21,652, against 21,662: the difference is in the tens digit.
- **Table 7.2:**
  - The header says "Mean", but the HCP entries are medians (footnote c).
  - The quantity judged, the upper prediction limit (15,697 ng/mg, 5.52 ppm, 1.09 %), is missing, so the margin to each criterion cannot be seen.
  - Footnote a) applies an offset to every row, but fragments carry none.
  - "4.12 to 4.12".
- **Table 7.3:**
  - The header runs to three lines.
  - Every cell repeats the range studied; one sentence would carry it.
  - The legend says "at manufacturing scale", which is not true for fragments.
- **Table 8.1:**
  - Residual DNA is missing, though the text gives its Cpk (10.81).
  - "CEX" in "CEX/icIEF" is not in the Abbreviations and reads as the process step.
  - Leached Protein A "0.003 ± 0.0006" is printed to four decimals for values the text says cannot be measured.
- **Table 13.1:** no issues.
- **Table 13.2:** reproduces.
- **Table 13.3:**
  - In PD-005-01 the "Done" text runs into the "Reason" column ("re-analysishost cell protein").
  - In PD-005-04, "95 %" is split across lines, and the "Done" cell runs to about 17 lines.
  - "selecting the model is standard practice" is asserted without a reference.
- **Tables A.1 and B.1:**
  - "center" against "centre" in the text.
  - The "nrCE-SDS" header is broken across lines.
  - Six step-yield results (Appendix A, Appendix B, Table 5.14) are exactly 99.0 % and none is higher. That suggests a reporting ceiling the report does not mention. A censored refit keeps the negative square of end of pool collect (−1.17, p = 0.049), but only at the edge of significance.
  - Aggregate (HMW) results are tabulated nowhere, though 5.4 reports their range over 47 pools.
  - Table B.1 shows run 23 at its design pH (3.55), not the analysed 3.38. The footnote says so, but the factor column is what a reader refits from.
- **Table C.1:** reproduces.
- **Table D.1:** "Reportable: step yield, %" for a protein concentration method. The reportable is a concentration; step yield is derived from it.
- **Figures:**
  - Figures 5.1 and 5.3 show step yield "as a fraction", while every table uses %.
  - Figure 5.1 has no fragment panel, though the fragment model has terms in exactly the two factors plotted.

## Yes/no answers

1. Physical cause named wherever a cause is given: **No**
2. Every technical term a term of art: **No**
3. Any sentence telling the reader how to file its finding: **Yes**
4. Every criterion with its basis, and every result reported as met or not met: **No**
5. Any statement wrong or contradicted by a table or figure: **Yes**
6. No machine-like sentence (yes = none flagged): **No**
7. Every sentence understandable on its own (yes = none flagged): **No**
