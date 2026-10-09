# Content review: PCP-003 Version 2.0, Production Bioreactor (Step 3)

- Source: `.claude/work/2026-10-08_01_rev2-campaign/PCP-003_bioreactor.DRAFT.txt` (the text of the PDF, 35 pages). No other file in the repository was read.
- Reviewer: Claude Opus 5.5 (`claude-opus-5-5`), 2026-10-09.
- Numbers were checked with Python, using only values printed in this document.
- Quotes are exact, except that words split across PDF lines have been joined again.
- How the questions were read:
  - Q1 covers sentences that claim a physical cause. A "because" that justifies a procedural or statistical decision is judged under Q3, Q5 or Q6 instead.
  - For Q3 and Q5, "yes" means the problem exists.
  - For Q6 and Q7, "yes" means no sentence was flagged, as instructed.

## Checks that passed

- **Table A.1** is a 2^(5−1) half fraction with E = ABCD (I = ABCDE). The design is therefore resolution V, and no main effect or two-factor interaction is aliased with another. The run order is a permutation of 1 to 19. The 16-term model on 19 runs leaves 3 residual degrees of freedom (2 for pure error, 1 for lack of fit), as Section 5.5 states.
- **Table B.1** holds the full 2^4 factorial, 8 axial runs and 4 centre runs. The run order is a permutation of 1 to 28. The 15-term quadratic leaves 13 residual degrees of freedom (3 for pure error, 10 for lack of fit), as stated.
- **Tables 6.1 and 6.2** agree. Every range studied extends beyond its NOR at both ends, and every NOR is symmetric about its set-point. The ratio of range width to NOR width runs from 1.5 (feed volume) to 2.5 (pH and initial viable cell concentration), which matches Section 4.3.
- **Run counts:** 3 + 19 + 16 + 28 = 66, 4 × 2 × 2 = 16, 3^4 = 81 and 5 × 4 = 20.
- **Table 1.1:** every Version 2.0 upper limit is above the Version 1.0 limit, and only acidic variants gains a lower limit.
- **Criterion arithmetic:**
  - Acidic variants: 40.0 − 0.40 = 39.6, and 40.0 − 1.00 = 39.0.
  - Aggregate: the a priori value 9.30 equals 5.00 × 2.00 − 0.70. That fixes the derivation as the drug substance limit × clearance fold − increase.
- **Dates:**
  - Version 1.0 was approved on 2025-08-25, before the first study started on 2025-08-27.
  - Every study window closed before the probe calibration fell due on 2026-06-14.
  - The screening study ended on 2025-10-03 and the response-surface study started on 2025-10-20, which fits Section 6.3.

## Q1. Is a physical cause named, with its direction, where a cause is given?

- "No downstream step changes the glycan profile, because neither Protein A nor the two ion exchange steps separate glycan variants under platform conditions (CMC Biotech Working Group 2009)."
  Q1: The cause restates the claim, since a purification step changes a glycan profile only by separating glycoforms. It names no property, such as the neutral glycoforms carrying no charge difference for the ion exchangers to resolve.
- "Afucosylation depends on the fucosyltransferase that adds core fucose in the Golgi, on the supply of its nucleotide sugar donor, and on how long the glycan stays in the Golgi before secretion."
  Q1: The species are named but not the direction. A larger donor supply or a longer residence in the Golgi lowers afucosylation.
- "Conditions that change the growth rate, the intracellular pH or the nucleotide sugar pool are therefore expected to move afucosylation."
  Q1: "Move" gives no direction, and the conditions are not named.
- "Afucosylation governs binding to the Fcγ receptor, so it is linked directly to the efficacy of the molecule."
  Q1: No direction is given (lack of core fucose raises binding), and no specific receptor is named. The effect is on FcγRIIIa, not on Fcγ receptors in general.
- "Culture temperature, culture pH, pCO2 and osmolality act on the same enzymes and the same donor pool, through the growth rate, the intracellular pH and the metabolic state of the cell."
  Q1: The sentence names four parameters and three routes, but no direction for any of them.
- "The effects of these parameters on galactosylation are therefore expected to interact."
  Q1: An interaction is inferred from a shared pathway, with no physical cause for a non-additive effect such as a limiting donor pool (see also Q5).
- "Culture pH and dissolved oxygen are expected to act on high mannose only weakly."
  Q1: No mechanism or direction is given. The paragraph also links no studied parameter to the mechanism it describes (fast Golgi transit or inhibited enzymes).
- "A longer culture and a higher culture pH are therefore expected to raise aggregate."
  Q1, for pH: the sentence before it names colloidal stability "at the culture pH". It never says that stability falls as the pH approaches the isoelectric point, so the direction for pH has no stated cause.
- "Culture temperature and culture pH set the rates of these reactions."
  Q1: No direction is given (higher temperature and higher pH speed up deamidation). Neither parameter alone sets the rate of glycation or of enzymatic sialylation.
- "pCO2 and osmolality act through the intracellular pH and the sialylation machinery, and the culture duration sets the time at temperature."
  Q1: No direction is given for pCO2 or for osmolality.
- "Because each parameter acts on several reactions at once, the net direction of its effect on acidic variants cannot be predicted from mechanism."
  Q1: "Several reactions" are invoked without the direction of any of them. Q5 explains why the conclusion is wrong for culture duration.
- "Culture duration is therefore expected to act on the glycans that change with culture age, on aggregate and on the impurity load."
  Q1: The clause gives no direction. Galactosylation is expected to fall, and aggregate and the impurity load to rise.
- "Culture pH and culture temperature act on the glycosyltransferases and on the rates of deamidation and aggregation, and their effects on the glycans are coupled to each other and to the culture duration."
  Q1: No direction is given, and "coupled" names no physical interaction.
- "pCO2 acidifies the cytosol, so it acts on the cell in the same way as culture pH but from inside."
  Q1: The first clause passes. The second, "in the same way as culture pH", names no effect on any attribute.
- "High osmolality slows growth and shifts the balance of the nucleotide sugar pool."
  Q1: In the second clause, "shifts the balance" has no direction and names no glycan.
- "The 4 remaining parameters are expected to act on the culture mainly through growth and titer."
  Q1: No direction is given.
- "Dissolved oxygen acts only weakly on the glycans within its range, and it is controlled by sparging and agitation independently of the other parameters."
  Q1: No mechanism or direction is given for the weak effect.
- "The multivariate parameters act on the same Golgi enzymes, the same nucleotide sugar pool and the same reaction rates, and their effects are therefore expected to interact (Section 4.1)."
  Q1: No direction is given, and the expected interaction has no physical cause (see Q5).
- "pCO2 also depends on scale, because it is set by the balance between the carbon dioxide that the cells produce and the carbon dioxide that the gas flow strips."
  Q1: The balance is named, but not which way scale moves it. pCO2 is higher at large scale, where less CO2 is stripped per unit volume.

These causal sentences pass:
- "Late in a fed-batch culture the galactose donor and the manganese cofactor of the galactosyltransferase are depleted, and the harvested pool accumulates antibody made under those conditions."
- "The level of high mannose rises when transit through the Golgi is fast relative to the processing enzymes, or when those enzymes are inhibited."
- "Viability falls late in a fed-batch culture, so a longer culture carries a larger load of both into the harvest."
- "pCO2 also raises the osmolality of the medium as bicarbonate accumulates."
- "Fragments are formed in the culture and during the hold of the harvest, by proteases released from lysed cells that clip the antibody."

These causal sentences were not judged under Q1, because they justify procedural or statistical decisions:
- the AMD-001 "because" in Section 1.1;
- the axial-run "because" in Section 6.3;
- the "because" for the glycan criteria in Section 7, item 3;
- the WC-CPP "because" in Section 7, item 6;
- the NOR-propagated PAR "because" in Section 8 (judged under Q5);
- "which is why the attribute has very high criticality" in Section 4.1.

## Q2. Is every technical term a term of art?

- "The NOR-propagated PAR uses the 95 % predictive interval of a single batch (Section 8)."
  Q2: "NOR-propagated PAR" is a coinage from inside this document set. "Predictive interval" also sits next to "prediction interval" (Sections 5.1 and 5.5) for a closely related interval.
- "The set-point PAR is the contiguous range around the set-point over which the mean prediction meets the criterion."
  Q2: "Set-point PAR" is also a coinage, for a one-factor PAR on the mean prediction with the other factors at their set-points.
- "For this reason each quality attribute is judged on a single batch (PCMP-001 §6.2)."
  Q2: "Judged on a single batch" is not a term of art, and it reads as "judged on data from one batch". The intended meaning is a 95 % prediction interval for one future batch. The same phrase appears again in Section 7, item 3.
- "The report will show it on the principal planes of the models."
  Q2: "Principal planes" is not a DoE term. The usual form is an overlay contour plot for each pair of factors, with the others at their set-points.
- "The method decision AMD-001 of 2026-03-20 made non-reduced CE-SDS (nrCE-SDS) the method for fragments at every step."
  Q2: A "method decision" (AMD, "analytical method decision") is a company document type, not a term of art. This is a minor point.
- "A model that fails the lack of fit test or the limit on overfitting is not used to set a range."
  Q2: "The limit on overfitting" is a paraphrase of the predicted R² criterion in item 2c.
- "For aggregate, the Version 1.0 limit was the drug substance limit carried back through the nominal downstream clearance of this campaign and divided by a margin of 6.8 (INV-001 finding 2)."
  Q2: A value you divide by is a safety factor. A "margin" is normally an allowance that is added or subtracted. Table 1.1 repeats "margin 6.8".
- "Culture pH and culture temperature act on the glycosyltransferases and on the rates of deamidation and aggregation, and their effects on the glycans are coupled to each other and to the culture duration."
  Q2: "Coupled" stands in for the statistical term "interact".
- "pCO2 acidifies the cytosol, so it acts on the cell in the same way as culture pH but from inside."
  Q2: "From inside" is an informal way of saying "through the intracellular pH".
- "Capability at commercial scale is estimated from the integrated model of the whole train (PCMP-001 §6.5)."
  Q2: The term of art is "integrated process model". "The whole train" is shop-floor shorthand.
- The units in Tables 6.1 and 6.2 have the same problem (see the table observations): "mOsm" should be mOsm/kg, "e6 cells/mL" should be 10⁶ cells/mL, and "% sat" should be % air saturation.

## Q3. Does any sentence tell the reader how to file what it has just stated?

- "The wider criteria do not loosen an approved criterion."
  Q3: The sentence tells the reader how to file the change it has just stated (every upper limit is higher) before anyone has objected. The next sentence, that the Version 1.0 limits were in no approved plan, makes the point on its own.
- "In both directions the bound replaces the platform value, never the point prediction."
  Q3: "Never the point prediction" answers an objection nobody raised, and the two sentences before it already say that the bound replaces the platform value.
- "A discrepancy from the plan is not a deviation."
  Q3: The sentence files what was just defined by saying what it is not. It also needs a basis, because in common GMP usage an unplanned departure from an approved protocol is a protocol deviation.

## Q4. Is every criterion stated with its basis, and can every decision rule be applied unambiguously?

- "The residuals show no pattern against predicted values or run order, and no single run dominates the fit."
  Q4: There is no test or threshold, such as a Cook's distance or studentized residual limit. "Run order" is also undefined, because the windows in Table 11.1 imply that the runs were made in parallel.
- "A model that fails the lack of fit test or the limit on overfitting is not used to set a range."
  Q4: This conflicts with "adequate for prediction when all of the following hold". It leaves open whether a model that fails only the F-test (a) or only the residual check (d) may set a range.
- "Where no adequate model results, the response is reported against its criterion over the runs of the designs."
  Q4: No decision follows. The plan does not say whether a range can then be proven, which range is carried forward, or how the scale-down model is qualified for that output, since qualification needs the model's prediction interval.
- "Each combination is judged on the exact 95 % prediction interval of a single run from the response-surface model."
  Q4: This makes qualification depend on an adequate response-surface model, so it is undefined for an output that has none. It also covers only the NOR of the 4 response-surface factors, although the offset is applied to the univariate and osmolality results as well.
- "The offset is reported with its two-sided 90 % confidence interval."
  Q4, minor: the interval method for 3 runs against 5 batches (pooled or Welch) is not stated, yet rule 3 depends on the ends of the interval.
- "Where an attribute does not meet its criterion even at the set-point, the report states that no PAR exists for that attribute and states the consequence for the NOR (PCMP-001 §7.6)."
  Q4: A consequence is stated only when no PAR exists, not when the PAR is narrower than the NOR. Objective 4 ("to show where the NOR lies within it") assumes that case away. "At the set-point" also does not say which analysis is meant.
- "The design space of the step is the region of the 4 response-surface factors, within the range studied, in which every measured attribute meets its criterion on the mean predictions of the adequate models."
  Q4: The rule is undefined when an attribute has no adequate model (is that attribute dropped?). It also does not state the levels of osmolality and of the four univariate parameters at which the region holds.
- "A critical process parameter (CPP) has a significant and practically relevant effect on a CQA and a high risk of falling outside its acceptable range in operation."
  Q4: "Practically relevant" and "high risk" have no thresholds. The same applies to "readily controlled" and "wide against its NOR" in the definition of a WC-CPP.
- "A key process parameter (KPP) affects process performance and has no effect on a CQA within its range."
  Q4: "No effect", set against the CPP's "significant and practically relevant", leaves no class for a parameter that has a significant but small effect on a CQA and also affects performance.
- "A significant effect that is too small to move the attribute appreciably does not by itself make a parameter critical, and the report states the size of each effect beside its significance."
  Q4: "Appreciably" has no threshold, such as a fraction of the width of the criterion, so criticality cannot be judged from this plan.
- "A Cpk of at least 1.33 is expected of a CQA in routine manufacture, and a Cpk below 1 requires an action in the control strategy."
  Q4: "Expected" is not a decision, and the outcome for a Cpk from 1.00 to 1.33 is not stated.
- "The results of the univariate study are reported against the criteria of Table 7.1 and beside the set-point runs of the qualification study."
  Q4: No rule says what result supports a range. It could be each run inside the criterion after the offset is subtracted, the mean of the duplicates, or an interval. Nor does the plan say how large a difference between the two ends matters.
- "The range of a univariate parameter is supported by its own data (PCMP-001 §4)."
  Q4: The same gap applies. The sentence also does not say whether the supported range is a PAR in the sense of Section 7, item 4.
- "The effects of osmolality are reported from the screening model (Section 6.3)."
  Q4: Osmolality is a multivariate parameter with a NOR (Table 6.1), yet it gets no PAR. No rule says how its range is proven or which range goes into the control strategy.
- "The response-surface study starts after Process Development and Statistics have reviewed the results of the screening study."
  Q4: No rule says what the review can change. For example, a significant osmolality effect or curvature could add a factor to the response-surface design.
- "A run whose recorded setting departs from its design level is recorded as a deviation, and its impact is assessed in the report."
  Q4: No tolerance is given for "departs", although every controlled parameter has a control band.
- "Each simulated batch carries the model residual and the uncertainty of the fitted coefficients."
  Q4, minor: the distributions used are not stated, so the PAR result cannot be reproduced from the plan.
- "The upper limit for acidic variants is carried back through the increase across low-pH viral inactivation."
  Q4: Table 7.1 gives "Carried back, widened" as the basis for the whole range 18.0–39.6, but only the upper limit is carried back. No basis is given for the 18.0 % lower limit. Table 4.1 also gives the drug substance criterion for "CEX/icIEF", which are two methods that do not give the same acidic percentage, while the studies use icIEF only.

## Q5. Is any statement wrong, internally inconsistent, or contradicted by a table?

### Major

- "At the set-point the culture lasts 17 days."
  Q5, conflicts with Table 11.1: S-BRX-SDM ran from 2025-08-27 to 2025-09-05 (9 days) and S-BRX-UNI from 2025-10-06 to 2025-10-17 (11 days). Every run of both studies is held at the 17-day set-point duration (Table 6.1, Section 6.4), so neither window can contain one complete culture.
- "The qualification study comes first, so that the scale-down model is established before any characterization run."
  Q5, conflicts with Section 5.1, rule 3, and with Table 11.1: qualification is decided on prediction intervals from the response-surface model. That model exists only after S-BRX-RSM, the last study, which ended on 2025-12-12. Section 1 ("that is qualified against manufacturing scale") likewise presents qualification as already settled.
- "Within the ranges studied the culture is fed to excess, so neither is expected to move the glycans appreciably."
  Q5, internally inconsistent: Section 4.1 says the galactose donor and the manganese cofactor "are depleted" late in the culture. If they run out, then the basal medium concentration and the feed volume, which "set the supply of nutrients and glycosylation precursors", are expected to move galactosylation.
- "The univariate parameters act mainly through growth and titer, or are controlled independently of the other parameters."
  Q5, internally inconsistent: Section 4.1 names the growth rate as a route to afucosylation and the antibody concentration as a driver of aggregate. Acting through growth and titer is therefore a route to the CQAs and to interactions, not a reason to expect neither. Assumption 4 in Section 12 rests on this sentence.
- "Dissolved oxygen acts only weakly on the glycans within its range, and it is controlled by sparging and agitation independently of the other parameters."
  Q5, conflicts with Section 5.1, where agitation and gas flow are set to match CO2 stripping: the gas sparged to hold dissolved oxygen also strips CO2, so dissolved oxygen control is coupled to pCO2.
- "Osmolality is not a factor of the response-surface design, and it is held at its set-point in every run of that design."
  Q5: This cannot be done as described.
  - Section 4.1 says osmolality is set by base and feed additions and by metabolites, and that it rises with pCO2.
  - Section 5.2 controls only pH, temperature, dissolved oxygen and pCO2, and fixes the media composition.
  - The plan gives no means of holding 400 mOsm while pCO2 runs from 40 to 160 mmHg (Table 6.2).
  - Nor does it say how osmolality is set independently of pCO2 in Table A.1. Runs 3, 7, 11 and 15 combine 160 mmHg with 360 mOsm, and runs 2, 6, 10 and 14 combine 40 mmHg with 440 mOsm.
  - The pCO2 effect in the response-surface model then leaves out the rise in osmolality that comes with pCO2 at manufacturing scale.
- "The design space of the step is the region of the 4 response-surface factors, within the range studied, in which every measured attribute meets its criterion on the mean predictions of the adequate models."
  Q5, internally inconsistent: Section 7, item 3, and Section 5.5 say "A quality attribute is judged on a single batch." The plan itself says that a batch at the edge of a mean-prediction region passes only about half the time. Such a region does not give the assurance of quality that ICH Q8(R2) attaches to a design space.
- "These measures of process performance are not responses of the designs."
  Q5, conflicts with Section 7, item 6 (a KPP "affects process performance") and with Objective 6: without viable cell concentration, viability or titer as responses, no parameter can be shown to be a KPP.
- "Each criterion assumes that every downstream step performs at least as well as its platform worst case."
  Q5, contradicted by Table 7.1: the two widened criteria assume that low-pH viral inactivation does better than its platform worst case. They use an aggregate increase of 0.53 % instead of 0.70 %, and an acidic variant increase of 0.40 % instead of 1.00 %.
- "Each drug substance criterion is carried backward through the platform worst case of every downstream step, from X-Mab, Y-Mab and Z-Mab, with no margin (PCMP-001 §7.3)."
  Q5, contradicted by Table 7.1: the aggregate and acidic variant values in the table (1.52-fold, 0.53 and 0.40) are A-Mab confidence bounds, not the platform values (2.00-fold, 0.70 and 1.00).
- "The resulting aggregate criterion of ≤ 7.04 % HMW is stricter than the a priori criterion of ≤ 9.30 %."
  Q5, check against Table 7.1:
  - The derivation that gives 9.30 (5.00 × 2.00 − 0.70) gives 5.00 × 1.52 − 0.53 = 7.07 from the values printed in the table.
  - A value of 7.04 is possible only if the unrounded clearance is 1.515–1.516 and the increase 0.530–0.535. Both inputs would then sit at the edge of their rounding intervals, and the largest possible rounding error is 0.03.
  - Confirm the value, or print a third decimal.
- Revision history, Version 2.0 entry: "Re-analysis under INV-001: a-priori intermediate acceptance criteria, fragments by nrCE-SDS, two-sided capability for acidic variants, scale-down models qualified by their offsets, execution dates recorded (see INV-001)"
  Q5, conflicts with Section 1.1 ("The decision does not change the methods of this plan, because fragments are not an attribute of the bioreactor studies (Table 5.2).") and with Table 5.2: the entry lists a change that this plan does not make.
- "The attributes of high and very high criticality are called critical."
  Q5, conflicts with Table 4.1 and the sentence that introduces it. Both call all 7 attributes "critical quality attributes", including acidic variants and residual DNA (VL) and host cell protein (M-H).
- "Table 3.1 lists the documents of the A-Mab package to which this plan refers."
  Q5, contradicted by Table 3.1. The table omits:
  - PCP-004 (Section 1);
  - PCR-006 and PCR-007 (Section 7), whose results changed two of this plan's criteria;
  - AMD-001 (Sections 1.1 and 5.3).
- "PCR-003 relies on both changed criteria."
  Q5: A plan cannot know what its report relies on without knowing the results. The sentence tells a reviewer that the outcome depends on the widened limits, which undercuts "The criteria in force are derived without data from the bioreactor studies." For aggregate, the net change was a tightening, from ≤ 9.30 to ≤ 7.04.
- "High mannose glycans are species on which processing in the Golgi never proceeded."
  Q5, scientifically wrong: Man5, the main high mannose form on antibodies, is made in the Golgi when α-mannosidase I trims Man8. High mannose species are those whose processing stopped before GlcNAc transferase I.
- "Because each parameter acts on several reactions at once, the net direction of its effect on acidic variants cannot be predicted from mechanism."
  Q5: This is wrong for culture duration, on the plan's own account. Deamidation is named as the main source, and it accumulates with time at temperature, so a longer culture is expected to raise acidic variants.
- "The multivariate parameters act on the same Golgi enzymes, the same nucleotide sugar pool and the same reaction rates, and their effects are therefore expected to interact (Section 4.1)."
  Q5, a non sequitur (Section 4.1 has the same reasoning for galactosylation): effects on a shared target can be additive. A shared target is a reason to test for interactions, not to expect them.
- "In general the NOR-propagated PAR is narrower than the set-point PAR, because the range must hold while the rest of the operating point moves within its NOR."
  Q5, incomplete: the set-point PAR is judged on the mean prediction, but the NOR-propagated PAR is judged on the 95 % interval of a single batch, which includes residual and coefficient uncertainty. That alone narrows it, even with the other factors fixed.
- "The probe is under calibration and change control, and a recorded setting that departs from its design level is recorded and assessed (Section 9)."
  Q5: This control cannot detect the risk it is listed against. A drifting probe reports the design level, because the controller holds the probe's own reading there. Only an independent offline pCO2 measurement or a calibration check reveals drift.
- "Mixing, aeration, mass transfer and process control of pH, dissolved oxygen, temperature and nutrient addition are equivalent at both scales."
  Q5, an overclaim: mixing time and CO2 removal differ between a bench vessel and a 15,000 L vessel, and the plan itself says that agitation, gas flow and pCO2 depend on scale. Equivalence is what qualification tests, not a premise. The working volume of the scale-down model is stated nowhere.
- "Agitation and gas flow depend on scale, and they are set so that oxygen transfer and carbon dioxide stripping match those of the commercial vessel (PCMP-001 §5)."
  Q5, conflicts with "In the scale-down model pCO2 is a factor of the designs and is controlled at the level of each run." If stripping is fixed to match commercial scale, pCO2 cannot also be held at 40, 100 or 160 mmHg without changing the gas flow or adding CO2.
- "Each run of the scale-down model gives one sample for the responses, taken from the culture fluid at the end of the culture."
  Q5: The plan states no purification of the sample before testing.
  - Released N-glycan mapping of culture fluid would also release glycans from host cell glycoproteins.
  - SEC and icIEF of culture fluid would also measure host cell proteins of every size and charge.
  - The claim in Section 1.1 that host cell protein does not affect the aggregate result therefore holds only for a purified sample.
- "Host cell protein and residual DNA are formed in the culture as cells lyse, but they are not responses of the bioreactor studies."
  Q5, internally inconsistent: Section 4.1 expects culture duration to raise the impurity load, and Objective 6 promises evidence to classify every parameter. Host cell protein has criticality M-H (36) in Table 4.1, yet the effect of culture duration on it is neither measured nor argued out of scope. The same holds for fragments, which Section 4.2 says are formed in the culture.

### Minor

- "The mechanisms by which the culture conditions act on the quality attributes are therefore known from the platform."
  Q5, an overclaim: data from three earlier antibodies give the direction and size of effects, not their mechanisms. The plan itself later says the acidic variant direction "cannot be predicted from mechanism".
- "The characterization of A-Mab confirms and bounds these effects for this cell line and this molecule."
  Q5: A protocol that says its study "confirms" the expected effects presupposes the result. Objective 3 ("to show that each model is adequate") does the same.
- "The 3 set-point runs of the qualification study are the set-point reference of the univariate study."
  Q5: The reference runs started 40 days before the univariate study (Table 11.1). Time and media lot are therefore confounded with the comparison (Section 12, risk 4), and no concurrent set-point run is planned.
- "For acidic variants, whose criterion is two-sided, both conditions apply."
  Q5, misleading against Table 7.1: afucosylation, galactosylation and high mannose also have two-sided criteria. The Cpk sentence in Section 5.5 implies the same.
- "The second analysis lets the other response-surface factors vary within their NORs."
  Q5, slightly inaccurate: the draws are normal, with a standard deviation of one sixth of the NOR width, and are clipped at the range studied, not at the NOR. About 0.27 % of draws per factor, or 0.8 % of operating points, therefore fall outside the NOR.
- "The fit statistics of the screening model therefore overstate how well it fits."
  Q5, imprecise: with 3 residual degrees of freedom, R² describes the fit to these runs correctly. What it overstates is how well the model would predict new runs.
- "Each study record states the execution window of the study and the calibration status of the instrumented system that it used, as the corrective action PA3 of INV-001 requires."
  Q5, inconsistent labels: Section 1.1 names the INV-001 corrective action CA2, and "PA" normally denotes a preventive action.
- "The initial viable cell concentration sets where on the growth curve the culture starts, and it changes the titer more than any quality attribute."
  Q5: The sentence compares changes in different units (g/L against %). The comparison means nothing without a common scale, such as a fraction of the width of each criterion.
- Osmolality is given in "mOsm" in Tables 6.1 and 6.2. Osmolality is expressed per kilogram of water, so the unit should be mOsm/kg.

## Q6. Which sentences read as machine-written?

- "The parameters act on these attributes in different ways."
  Q6: The sentence says nothing. The sentences after it carry the content.
- "The net direction of each effect will be read from the fitted models."
  Q6: It repeats "The sign and size of each effect will be read from the fitted models." from the same section.
- "Fragments are not an attribute of the bioreactor studies."
  Q6: This is the third time the fact is stated (Section 1, Section 1.1 and Section 4.2). It appears again in Section 5.3 and in the footnote to Table 5.2.
- "Fragments are not measured in the bioreactor studies, and aggregate is measured by SEC in both designs (Table 5.2)."
  Q6: It repeats Section 1.1 and Table 5.1.
- "The method decision AMD-001 does not change the methods of this plan (Section 1.1)."
  Q6: It repeats Section 1.1 almost word for word.
- "Before either judgement the offset of the output is subtracted, so that the result is stated at manufacturing scale."
  Q6: It repeats Section 5.1, rule 2.
- "A study of one factor at a time cannot show an interaction with other parameters (Section 6.4)."
  Q6: The same point is made again in Section 6.4 and in Section 12, assumption 4.
- "Both ends of the criterion are therefore assessed."
  Q6: It restates the clause immediately before it.
- "The screening design identifies effects."
  Q6: This is the fourth statement of the screening model's role (twice in Section 5.5, then in Section 6.3), and it adds nothing here.
- "The report will state the effects of osmolality from the screening model, which identifies effects but does not predict."
  Q6: A restatement, which is repeated once more in Section 8.
- "The effects of osmolality are reported from the screening model (Section 6.3)."
  Q6: A restatement.
- "The derivation uses no data from the studies it judges."
  Q6: It repeats "None of them uses data from the bioreactor studies." from the start of the same section, and Section 1.1.
- "Version 1.0 of this plan was approved on 2025-08-25, before the first study started on 2025-08-27."
  Q6: It repeats Section 1.1 almost word for word.
- "The set-point reference is the 3 set-point runs of the qualification study S-BRX-SDM, made in the same scale-down system."
  Q6: It repeats Section 5.4.

## Q7. Can each sentence be understood on its own?

- "PCMP-001 §7.3 derives these criteria a priori from the drug substance criteria and the platform worst case of every downstream step."
  Q7: A section code is the subject. Name "the master plan PCMP-001".
- "The rule changed 2 of the 5 criteria of this step (Section 7)."
  Q7: Name the verification rule and the two criteria (aggregate and acidic variants).
- "The verification rule changed 2 of the 5 criteria of this step."
  Q7: Name the two criteria.
- "PCR-003 relies on both changed criteria."
  Q7: Name the bioreactor report, and the aggregate and acidic variant criteria.
- "Version 2.0 applies the campaign thresholds that PCMP-001 Version 2.0 sets for the significance of model terms, for model adequacy and for capability (Section 5.5, Section 7)."
  Q7: Give the thresholds (α = 0.05, predicted R² within 0.20 of R², and Cpk 1.33 and 1).
- "Acidic variants and residual DNA have very low criticality, and they remain in scope with their criteria (PCMP-001 §3)."
  Q7: Say what they remain in scope of, since residual DNA is not a response of these studies.
- "Conditions that change the growth rate, the intracellular pH or the nucleotide sugar pool are therefore expected to move afucosylation."
  Q7: "Conditions" stands in for the studied parameters. Name them.
- "Culture temperature, culture pH, pCO2 and osmolality act on the same enzymes and the same donor pool, through the growth rate, the intracellular pH and the metabolic state of the cell."
  Q7: Name the galactosyltransferase and its galactose donor.
- "Culture duration is therefore expected to act on the glycans that change with culture age, on aggregate and on the impurity load."
  Q7: Name galactosylation, and name host cell protein and DNA.
- "The multivariate parameters act on the same Golgi enzymes, the same nucleotide sugar pool and the same reaction rates, and their effects are therefore expected to interact (Section 4.1)."
  Q7: "The same" needs the enzymes and the reactions named.
- "The model is qualified for an output when the conclusion against its criterion over the NOR is the same with the offset at either end of its confidence interval."
  Q7: "The conclusion" is defined only in the next sentence. Write "whether the output meets its criterion at all 81 NOR combinations of the 4 response-surface factors".
- "The scale-down model is qualified for an output when the conclusion against its criterion over the NOR is the same with the offset at either end of its 90 % confidence interval (Section 5.1)."
  Q7: The same stand-in, and Section 7 does not define it at all.
- "A model that fails the lack of fit test or the limit on overfitting is not used to set a range."
  Q7: Name the predicted R² criterion.
- "The NOR-propagated PAR uses the 95 % predictive interval of a single batch (Section 8)."
  Q7: The label is used before Section 8 defines it. Write "the PAR computed with the other factors varied over their NORs".
- "Classification is a result of the study, and it is reported in PCR-003 under SOP-4001."
  Q7: Name the bioreactor report and the classification procedure.
- "The criteria below apply PCMP-001 §7 to the production bioreactor."
  Q7: Name the acceptance criteria of the master plan.
- "Capability is judged in PCMR-001 against the values of PCMP-001 §7.9."
  Q7: Name the master report, and give the values in this sentence (they appear only in the next).
- "Each study record states the execution window of the study and the calibration status of the instrumented system that it used, as the corrective action PA3 of INV-001 requires."
  Q7: "PA3" is a bare code, and Section 1.1 calls the INV-001 action CA2.

## Table observations

**Approvals table and Table 10.1**
- Table 10.1 is titled "Responsibilities of the functions that approve this plan", and Section 10 says "The same functions approve the plan". The Approvals table, however, lists one approver (Quality Assurance); the other four functions are the author and three reviewers.
- "Manufacturing Science" (a reviewer) and "Process Development / MSAT" (the author) overlap, since MSAT is Manufacturing Science and Technology. It is unclear whether they are the same function.

**Revision history**
- The Version 2.0 entry lists "fragments by nrCE-SDS", which this plan does not adopt (Section 1.1, Section 5.3, Table 5.2).
- "Re-analysis" describes the work of the report, not of the plan.
- "a-priori" is hyphenated here but written "a priori" elsewhere.

**Abbreviations**
- These are used but not defined: CEX (Table 4.1), DoE (Table 3.2), sd (Table 1.1), VH, H, M-H and VL (Table 4.1), %Gal and G1+G2 (Table 4.1), and "e6" (Table 6.1).

**Table 1.1**
- The footnote letters differ from Table 7.1 for the same ideas. Here b) means widened and c) tightened. In Table 7.1, a) means tightened, b) widened and c) drug substance criterion. A reader comparing the two tables meets two meanings of "c)".
- Footnote b) includes "on an adequate model", but footnote b) of Table 7.1 leaves this condition out.
- R2 explains only the upper limits. The source of the Version 1.0 lower limits (2.00, 10.0 and 3.00, which equal the drug substance lower limits) is not stated.
- Several cells wrap badly:
  - "R1, margin 6.8" breaks across two lines.
  - "Carried back, tightenedc) and widenedb)" runs over three lines, with the footnote letters joined to the words.
- The Basis column says "Drug substance", where Table 7.1 says "DS criterion".
- The rows are in alphabetical order, but Table 7.1 lists aggregate first.

**Table 3.1**
- The table omits PCP-004, PCR-006, PCR-007 and AMD-001, all of which the text cites (see Q5).
- The relationship given for PCMR-001 is "Rolls up into". According to Section 1, it is the report PCR-003 that rolls up into PCMR-001, so the plan's own relationship to PCMR-001 is not stated.
- "(Production Bioreactor (Step 3))" nests one set of brackets inside another.

**Table 3.2**
- The merged type labels ("Standard operating procedure", "Analytical method validation") wrap over three lines and are centred vertically. As a result, SOP-1001, SOP-1002 and AMV-3010 have no label on their own line.
- The table spells "Titre", while the text spells "titer".
- SOP-3016 is paired with AMV-3021, whereas every other method shares its number between SOP and AMV.
- SOP-3016 and AMV-3021 are not cited anywhere in the text, although the sentence introducing the table says it lists what "this plan cites".

**Table 4.1**
- The criticality codes (H, VH, VL and M-H) are not defined, and "M-H" is not a category the text names.
- The header "Tool #1" holds the score (impact × uncertainty) and should say so.
- "10–40 % (G1+G2 equiv.)" does not define total galactosylation clearly.
- "(CEX/icIEF)" gives two methods for one criterion, which may not give the same acidic percentage. "CEX" is undefined and collides with the name of the process step.
- "Acidic charge variants (deamidation)" equates acidic variants with deamidation, but Section 4.1 also names sialylated glycans and glycated lysines.
- The residual DNA criterion "≤ 0.001 ng/dose" (1 pg/dose) is unusually low. Check the unit.
- The title says "Critical quality attributes", but the text calls only the attributes of high and very high criticality critical.
- Capitalization is inconsistent: "High Mannose" and "Host Cell Protein" in the table, lower case in the text.

**Table 5.2**
- Footnote a), "Fragments were not an attribute of this study.", restates the cell it marks ("not in scope"). It is in the past tense and refers to one study, while the table covers two designs.
- The title limits the table to "the designed studies", but the qualification and univariate studies also measure aggregate by SEC.
- Section 1.1 cites this table as the reason fragments are out of scope, but the table only restates that they are.

**Table 5.3**
- The "Runs" column mixes runs and batches ("3 scale-down, 5 manufacturing scale").
- The S-BRX-SDM entry in the "Replication" column ("all scale-down runs at the set-points") is not a replication count.
- There is no total row (the text gives 66).

**Table 6.1**
- Three units are incomplete or non-standard: "mOsm" should be mOsm/kg, "e6 cells/mL" should be 10⁶ cells/mL, and "% sat" should be % air saturation.
- The decimals are inconsistent. The basal medium NOR "1–1.4" sits beside the set-point "1.2" and the range "0.8–1.6", so it should read 1.0–1.4. The initial viable cell concentration set-point "1" should read 1.0.
- "Nutrient feed-1 volume, % of working volume" does not say whether 12 % is the total or the per-feed volume, or whether it refers to the initial or the final working volume.
- The label "Dissolved CO2 (pCO2)" mixes a concentration with a partial pressure, while the unit (mmHg) is a partial pressure.

**Table 6.2**
- The table agrees with Table 6.1 (checked), but it repeats the "mOsm" unit.

**Table 7.1**
- The header "Downstream worst case" is wrong for two rows. For aggregate and acidic variants the values are A-Mab 95 % confidence bounds, not worst cases. The platform values (2.00, 0.70 and 1.00) and the a priori criteria (9.30 and 39.0) appear only in the text.
- The aggregate criterion of 7.04 cannot be reproduced from its own row: 5.00 × 1.52 − 0.53 = 7.07 (see Q5).
- "Clearance fold 1.00" for the glycans and for acidic variants means nothing, because these attributes are not cleared. A dash would be clearer.
- The acidic variant basis, "Carried back, widened", applies to the upper limit only.
- "Increase, in the unit of the criterion" means percentage points. The text, however, writes "0.70 %", "0.53 %" and "0.40 %", which can be read as relative increases.
- Two notes have no marker: the abbreviation line and the note on rounding.
- The Basis cells wrap over three lines, with the footnote letters joined to the words ("tighteneda) and widenedb)").
- "Drug-substance" is hyphenated in the caption and in footnote c), but not in the text.

**Table 11.1**
- The S-BRX-SDM window (9 days) and the S-BRX-UNI window (11 days) are each shorter than one 17-day culture at the set-point (Table 6.1).
- The S-BRX-SCR window (25 days) can hold its eight 19-day runs only if they all started within 6 days, that is, in parallel. The plan does not say the runs were parallel, which also leaves "run order" undefined.
- The table does not define "End".
- The calibration status that Section 1.1 (item 6) says is recorded is given only in prose.

**Table A.1 and Table B.1**
- The header "Run Run order" reads as one run-together label in both tables.
- In Table B.1, the axial rows 17 to 24 are misaligned when rendered. Their values shift left with uneven spacing (for example "−1 0  0 0"), so a ±1 cannot be assigned to a column by its position.
- The axial pairs in Table B.1 are listed in the order A, B, E, C, which does not follow the column order A, B, C, E.
- Both design matrices were checked and are correct (see "Checks that passed").

## Answers for the document as a whole

| Question | Answer | Note |
|---|---|---|
| 1. Physical cause named, with its direction, where a cause is given | No | 19 sentences flagged |
| 2. Every technical term a term of art | No | 10 sentences flagged, plus 3 units |
| 3. Any sentence that tells the reader how to file a finding | Yes | 3 sentences flagged |
| 4. Every criterion with its basis, and every rule unambiguous | No | 18 sentences flagged |
| 5. Any statement wrong, internally inconsistent or contradicted by a table | Yes | 24 major and 9 minor items |
| 6. No sentence reads as machine-written ("yes" = none flagged) | No | 14 sentences flagged |
| 7. Every sentence understandable on its own ("yes" = none flagged) | No | 18 sentences flagged |
