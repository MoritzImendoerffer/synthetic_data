# Content review of PCR-005 (Protein A chromatography), Version 2.0 draft, run 2

**Reviewer model:** Claude Opus 5.5 (`claude-opus-5-5`).

**Source read:** `.claude/work/2026-10-08_01_rev2-campaign/PCR-005_protein_a.DRAFT.txt`, all 2,549 lines. I read no other file in the repository.

**Method notes**
- Quotes are verbatim, with the PDF's line-break hyphens rejoined. Every quote was checked by script against a normalized copy of the text.
- Numbers were re-derived only from the document's own tables. I refitted the screening model from Appendix A (Table 13.4) and the response-surface models from Appendix B (Table 13.5). The refits reproduce Tables 5.3–5.8, 5.1/5.2, the 15,384 / 16,062 / 16,550 / 16,932 ng/mg prediction limits, the 15,022–15,417 influence range, the p = 0.020 reversal test and the DEV-005-01 predictions. Where a refit disagrees with the text, the item is listed under Q5.
- For Q1, I tested causal claims about the process, product or method. A "because" that only gives the reason for a procedural or statistical decision (for example "because the Version 1.0 limit was never approved") is not a physical-cause claim, so Q1 does not apply to it. Those sentences are covered under Q3 or Q6 where relevant.

---

## Q1. Causal claims without a physical cause and direction in the same clause

- "Both parameters act on the host cell protein that is eluted, so an interaction between them was possible, and the designs can estimate it." — **Q1.** "Act on" names no species, interaction or direction, and the paragraph has just said that no mechanism for the load effect was assumed. Two factors acting on one output does not by itself predict an interaction.
- "For this reason breakthrough rises as the load approaches the dynamic binding capacity and as the residence time falls." — **Q1.** The cause just given (pore diffusion) explains only the residence-time half. Breakthrough rising near the dynamic binding capacity follows from how that capacity is defined, not from pore diffusion.
- "Neither the life of the resin nor the protease activity of the load is a setting of the run, so within the ranges of one run leached Protein A was expected to be flat." — **Q1.** The cause is procedural ("not a setting"). It ignores the physical driver, which is how long the ligand is exposed to harvest proteases, and load volume and flow rate set that time (see Q5).
- "The expected cause is the longer hold of the clarified harvest before capture at manufacturing scale." — **Q1 (mild).** The clause names a process condition. The species (harvest proteases) and the interaction (cleavage of the ligand) appear only two sentences later.
- "For aggregate and acidic variants the highest expected level is the upper 95 % prediction limit of the production bioreactor model within its NOR (PCR-003), because capture does not change them." — **Q1.** The cause restates the conclusion. The physical reason (the ligand binds the Fc of monomer, aggregate and every charge variant alike) is not in the clause.
- "The two designs were run at different times (Table 4.3), and a difference between their feeds or in how the end of collection was set could act in this way." — **Q1.** It names no feed property (host cell protein level, titre, protease) and no direction that could reverse the sign of the end-of-collection effect.
- "Its NOR is also narrowed by this report, because the qualification of the scale-down model for pool host cell protein depends on it (Section 3.1)." — **Q1.** The cause is a property of the laboratory model's offset uncertainty, not of the process. It is offered as support for criticality (see Q5).
- "Leached Protein A depends on the life of the resin and on the protease activity of the load." — **Q1 (mild).** No direction is given. Leaching falls as the resin ages and rises with protease activity.
- "The mechanism of the load effect is not established, because pool host cell protein is reported per mg of antibody." — **Q1.** A reporting convention is not a cause, and the reasoning does not follow: the mechanism is unknown because no study was designed to find it.
- "The investigation found an error at the titration end point during buffer preparation." — **Q1 (mild).** "An error" names no physical cause or direction, for example acid over-added, or the same miscalibrated meter reading about 0.17 pH units high.
- "The investigation attributed the first result to suspected carryover in the ELISA." — **Q1 (mild).** Carryover is named, but the document never says whether the out-of-trend result was high or low.
- "They were made to narrow the confidence interval of the offset for pool host cell protein, which is the output that sets the ranges of the step." — **Q1 (mild).** "Sets" is used for a statistical relation. It means the output whose criterion limits the PARs. The same wording appears in the PD-005-01 row of the discrepancy table.

Mechanistic causes that pass include histidine protonation at the CH2–CH3 interface, pore diffusion with residence time, host cell protein co-eluting in the SEC low molecular weight window, ligand fragments that still bind Fc, the weakly held impurity eluting at the elution front, and residence time being set by bed height at constant linear velocity.

## Q2. Terms that are not terms of art

- "For pool host cell protein the NOR-propagated PAR of elution buffer pH is 3.25–3.9, narrower than its range studied of 3.2–3.9." — **Q2.** "NOR-propagated PAR / analysis / range" is coined. The literature says a PAR evaluated with the other parameters varied over their NORs, or a multivariate PAR. It appears throughout F7, §1.4, §7.3, §9 and §12.
- "Table 7.3 gives the PAR of each multivariate parameter for each output with a criterion, by the set-point analysis and by the NOR-propagated analysis of PCMP-001 §6.4." — **Q2.** "Set-point analysis" is coined; the literature calls it a univariate PAR with the other parameters at set-point. "Multivariate parameter" is also coined, because the study is multivariate, not the parameter.
- "The range of a univariate parameter is supported when every individual result at both ends meets its criterion at manufacturing scale, after the offset is subtracted (PCP-005 §6.4)." — **Q2.** "Univariate parameter" has the same problem.
- "Held at elution pH for 7 days at 2-8 °C or 21 °C, the Protein A eluate met the hold rule of PCP-005." — **Q2.** "Hold rule" is an internal label, not a term.
- "The model was qualified under SOP-1001 by the offset rule of PCMP-001 §7.1, as PCP-005 §5.1 applies it." — **Q2.** "Offset rule" is an internal label. "Offset" by itself is accepted in scale-down model qualification.
- "The criterion in force is ≤ 16,379 ng/mg, with the basis “back-calculated, widened on verification”." — **Q2.** "Widened on verification" is an internal status label.
- "Every output met its criterion across the NOR in force at manufacturing scale." — **Q2.** "NOR in force" and "NOR as characterized" are internal states, not terms.
- "The lowest level of acidic variants expected in the pool is below the floor of 18 % before any hold, a result of the production bioreactor (PCR-003)." — **Q2.** The term is "lower limit", not "floor". "Floor" recurs in §5.7.
- "At this step that one-factor test identifies elution buffer pH, whose PAR for pool host cell protein is narrower than its range studied." — **Q2.** "One-factor test" is coined.
- "At commercial scale the integrated model of the train gives a Cpk of 6.19 for host cell protein and 10.82 for fragments in the drug substance." — **Q2 (mild).** The term of art is "integrated process model".
- Abbreviation entry "AMD — analytical method decision" — **Q2 (mild).** This is an internal document type, not a term.

"End of pool collect" is industry shorthand (end-of-collection criterion) and acceptable. "Tool #1", WC-CPP, KPP and GPP are A-Mab case-study terms and acceptable.

## Q3. Sentences that tell the reader how to file a finding, or answer an objection nobody raised

- "This is not a loosening of an approved criterion, because the Version 1.0 limit was never approved." — **Q3.** It pre-empts an objection nobody raised.
- "It is replaced by a criterion derived without data from the Protein A studies it judges, and widened on the data of cation exchange by a rule that PCMP-001 stated before this report applied it (Section 7)." — **Q3.** This is a defensive gloss. The facts belong in §7 without the rebuttal framing.
- "The point prediction is never used." — **Q3.** It answers an objection nobody raised.
- "PCMP-001 stated this rule before any Version 2.0 report applied it." — **Q3.** A defensive gloss, the second time this is said.
- "A model that predicts left-out runs this much worse than it fits its own runs cannot carry a criterion upstream." — **Q3.** It justifies the rule against an imagined challenge, and restates it.
- "The rule and the criterion were not changed." — **Q3.** A defensive gloss in the Discussion.
- "The qualification rule of PCMP-001 §7.1, the criterion and the confidence level were not changed, and every run that was made is used." — **Q3.** A defensive gloss. It also leaves open the real issue, that runs were added after a failed result was seen (see Q5).
- "The lowest level of acidic variants expected in the pool is below the floor of 18 % before any hold, a result of the production bioreactor (PCR-003)." — **Q3.** The trailing appositive tells the reader where to file the finding.
- "This is a result of the production bioreactor, not of the hold, and it is assessed in PCR-003." — **Q3.** It files the finding elsewhere.
- "The lowest Cpk of the drug substance, 1.03 for Acidic charge variants (deamidation), belongs to an attribute this step does not change, and it is discussed in PCMR-001." — **Q3.** It files a below-target result away. The claim it rests on is also contradicted (Q5) and the result is not judged (Q4).
- "These figures describe the drug substance after cation exchange and anion exchange have removed most of what the Protein A pool carries." — **Q3 (borderline).** A gloss on how to read the high Cpk values.

## Q4. Criteria stated with their basis, and results reported as met or not met

Most criteria pass. Host cell protein ≤ 16,379 ng/mg, leached Protein A ≤ 158 ppm and fragments ≤ 2.45 % are each derived in §7.1. The adequacy criteria, the qualification rule and the univariate rule are stated, and each is reported as met or not met. The exceptions are these.

- "The held eluate therefore carries the criteria that PCMP-001 sets for the output of the production bioreactor, ≤ 6.64 % HMW and 18–39.6 % acidic variants." — **Q4.** The basis is a pointer only. The derivation is not stated. 6.64 % equals DS ≤ 5 % × the cation exchange bound of 1.44-fold − the viral inactivation increase of 0.54 points. No basis at all is given for 18–39.6 %.
- Table 5.13, acidic variants rows (criterion "≤ 39.6", Met "Yes") — **Q4.** The criterion is two-sided (18–39.6 %, §4.5) but the table judges only the upper side. The lower limit is not met by the expected level (14.7 %, §5.7), and the table does not show this.
- "The lowest Cpk of the drug substance, 1.03 for Acidic charge variants (deamidation), belongs to an attribute this step does not change, and it is discussed in PCMR-001." — **Q4.** 1.03 is below the 1.33 target of PCMP-001 §7.9, though above the 1.00 minimum. The report does not say "not met".
- "The Cpk of 2785.30 for leached Protein A is not meaningful." — **Q4.** No verdict is given against 1.33. If the value is not meaningful, the report should say how the attribute is judged instead, for example on the margin of the pool result against ≤ 158 ppm.
- "Residual DNA and aggregate were measured for information." — **Q4.** Residual DNA is a CQA in scope (Table 2.1), and the step is "the principal point of clearance" for it. No intermediate criterion is set, and no reason is given why none is needed.
- "The same simulation gives the probability that a drug substance batch falls outside its specification." — **Q4 (minor).** Promised in §3.5, but §8 gives only "No simulated batch fell outside these criteria." It reports no probability and no bound (0 of 2,000 batches bounds the rate at about 0.15 % at 95 % confidence).
- The decision statistic is called the "upper 95 % prediction limit" but its sidedness is never stated. The values reproduce only as the upper end of the two-sided 95 % interval, and the NOR narrowing depends on that choice (Q5, item A13).

## Q5. Statements that are scientifically wrong or contradicted by the document's own tables

### A. Contradicted by a table, a figure or another statement in the document (checked)

1. "The PAR of every other parameter, and every PAR for leached Protein A and fragments, spans the range studied." (F7) — It contradicts §5.3.4 ("No PAR is claimed from the model (finding F6).") and §7.3 ("no PAR is claimed from them"). Table 7.3 prints these PARs anyway.
2. Table 7.2 — It marks leached Protein A and fragments "Met across the NOR: Yes" from predictions of models that Table 5.6 rejects. The text below the table says instead "For these two outputs the decision rests on the measured results, every one of which met its criterion."
3. "Cation exchange and anion exchange remove host cell protein, leached Protein A and fragments after this step, and judging the pool against the drug substance limit would fail every acceptable run." — Contradicted by Table 13.5 and Table 2.1. Every nrCE-SDS fragment result (0.77–1.09 %) meets the drug substance limit of ≤ 2 %. After the 1.18 ppm offset, only 3 of 47 leached Protein A results exceed ≤ 5 ppm (screening run 19, response-surface runs 7 and 27). The claim holds for host cell protein only.
4. "Acidic variants are not an output of this step, so the two-sided capability assessment of INV-001 finding 4 does not apply here." — Contradicted by §4.5, §5.7 and Table 5.13. The held eluate's acidic variants are judged against the two-sided range 18–39.6 %, and the lower limit is not met by the expected level of 14.7 %.
5. "The lowest Cpk of the drug substance, 1.03 for Acidic charge variants (deamidation), belongs to an attribute this step does not change, and it is discussed in PCMR-001." — Contradicted by Tables 5.12 and 5.13. Acidic variants rise 0.4 points (2–8 °C) and 0.9 points (21 °C) over the 7-day hold, which §10 item 4 permits.
6. "The other rows serve the criteria of other steps." and "No criterion of this step was tightened." (§7.1) — Contradicted by Table 7.1 together with §4.5. This report's hold study uses ≤ 6.64 % HMW and 18–39.6 % acidic variants, and these rest on the viral inactivation aggregate and acidic-variant rows and on the cation exchange aggregate row, which is "Not confirmed, tightened". 6.64 % reproduces as 5 % × 1.436 − 0.54. The platform values would give 5 % × 2.00 − 0.70 = 9.30 %, so the aggregate criterion applied at this step was tightened.
7. "Every other downstream value on which these criteria rely was confirmed or bettered by its A-Mab data." — It conflicts with the same section. The anion exchange host cell protein model and the cation exchange and viral inactivation fragment models fail the predictive-power test, and §7.1 says such a model "cannot carry a criterion upstream". A model that is too poor to widen a value cannot confirm it either.
8. Several sentences say the host cell protein model "shows no lack of fit" (F3; §11; Conclusion 3; §13.4). These are "The response-surface model for pool host cell protein is significant, shows no lack of fit and predicts left-out runs within the limit of PCP-005 §7 (criteria 2 to 4).", "The response-surface model for pool host cell protein is significant, shows no lack of fit and meets the limit on predictive power, with a lack of fit test close to its limit.", "Its model is significant, shows no lack of fit and meets the limit on predictive power." and "The model for pool host cell protein is significant, shows no lack of fit and meets the limit on predictive power." — Table 5.8 shows a lack-of-fit F of 7.88 (p = 0.058), and the residual SD (895) is 2.5 times the pure-error SD (357). The lack of fit is not significant, which is not the same as absent. The §11 sentence contradicts itself.
9. Table 5.9, step-yield row (max D 0.38, run 12, 6 runs above 4/n) — My refit of the Appendix B data reproduces this row from the discarded full quadratic model (0.39, run 12, 6 runs). The reduced model the report actually uses gives max D 0.21 at run 15, with 2 runs above 4/n. "Like every model of the study, it does not meet the limit on influential runs (Section 5.3)." is therefore true, but no table supports it. "A full quadratic model of 15 terms in 28 runs has a mean leverage of 0.54." does not explain the 5-term reduced model, whose mean leverage is 0.18.
10. "It does not meet the limit on influential runs, a Cook’s distance below 4/n (criterion 5, finding F8, Section 5.3)." and F4's "(Section 5.3)" — These are wrong cross-references. The influence analysis is in §5.5.
11. "The same verdicts follow when predicted R² is compared with adjusted R², as PCMP-001 §7.2 states the criterion." versus "The response-surface model of the downstream step must also pass the adequacy tests of PCMP-001 §7.2, on lack of fit and on how far predicted R² falls short of R²." — The two sentences state the PCMP-001 §7.2 criterion two different ways. The cation exchange and anion exchange gaps (0.14 and 0.27) are quoted against R².
12. "The scale-down model is qualified by its offset for both outputs with a criterion, but for pool host cell protein only after two changes." — §7.2 says there are 3 outputs with a criterion. Fragments has a criterion but was not part of the qualification.
13. "With the offset at the low end of its 90 % confidence interval, the upper 95 % prediction limit of a single run over the NOR reaches 16,550 ng/mg at manufacturing scale, above the criterion of ≤ 16,379 ng/mg." — 16,550, 16,062, 15,384 and 16,932 reproduce only as the upper end of a two-sided 95 % interval (t at 0.975, 13 df). Read as a one-sided upper 95 % limit, as the wording says, the limit at the NOR as characterized is 16,177 ng/mg. That is below the criterion, so the scale-down model would qualify and the NOR would not need narrowing. The NOR change rests on a sidedness the report never states.
14. "Fragments by nrCE-SDS fall slightly as elution buffer pH rises, and no adequate model results, so the decision rests on the measured results." and "Fragments by nrCE-SDS fall slightly as elution pH rises, which is the direction expected from acid-catalysed hinge hydrolysis during elution." — The fragment model is not significant (p = 0.280) and has a negative predicted R². §5.3.3 dismisses the single significant term of the equally inadequate leached Protein A model as "about what chance alone gives". The two cases rest on the same kind of evidence but are treated in opposite ways. One term at p = 0.008 among 14 is not significant after allowing for 14 tests.
15. "Fragments by nrCE-SDS were not part of the qualification, because the method decision AMD-001 was taken after study S-PA-SDM had closed." — Table 4.3 places S-PA-SDM2 (2026-09-07 to 2026-09-11) after S-PA-RET (April 2026), so after AMD-001. The 6 supplementary runs could have carried fragments, and the reason given covers only the 3 planned runs.
16. "This holds for protein load, elution buffer pH and their interaction on pool host cell protein, and for every main effect and the interaction of protein load with load flow rate on step yield." — §2.1 gave no expected direction for the protein load × pH interaction ("an interaction between them was possible"). Section 2 also gave no expectation for pH on yield. Agreement "in direction" cannot be claimed for either.
17. "A discrepancy from the plan is work that the plan did not foresee, done without any such departure." — It contradicts the definition just before it. Work outside an approved plan is a departure from an approved procedure. By the report's own definition, S-PA-RET (nrCE-SDS retest of retained samples, not in the Version 1.0 plan) is also a discrepancy, yet it is not recorded. That holds unless a later PCP-005 version added it, which the report does not say.
18. "The difference between these rises, 0.095 %, is smaller than the difference of 0.099 % between the day 0 aliquots." and "Aggregate rose by 0.46 % at 21 °C against 0.07 % at 2-8 °C." — Table 5.12 gives rises of 0.22 and 0.32 for fragments (not 0.31) and 0.45 for aggregate (not 0.46). With the printed values both differences are 0.10, so "smaller" does not hold. The argument depends on a 0.004-point gap in digits the table does not show.
19. "Pool host cell protein exceeds its criterion only in the corner of high protein load and low elution buffer pH, below the NOR of elution buffer pH (Section 6, Section 7)." and "Pool host cell protein exceeds its criterion only at high protein load with elution buffer pH below its NOR." — Both hold only with load flow rate and end of pool collect inside their NORs. With both at the low end of their ranges studied, the Table 5.7 coefficients exceed the criterion at 50 g/L for pH below 3.47, which is inside the pH NOR.
20. "It lies wholly below the elution buffer pH NOR of 3.4–3.7, at pH 3.32 and below, and it reaches down to a protein load of 37 g/L resin, inside the protein load NOR of 20–38 g/L resin." — From the Table 5.7 coefficients, the boundary at pH 3.2 is 36.1 g/L, not 37 g/L. This is minor; it is probably the first grid point.
21. "Over the whole range studied of all 4 factors, 93.5 % of the design region meets the criterion." — Minor. This is a count of grid points (11 per axis reproduces 93.5 %). The fraction of the region from the same coefficients is 95.7 %, and 96.7 % rather than 96.3 % for the two-factor region. The grid is not stated.
22. "This is the predictive model of the step, and every PAR and every prediction of a quality attribute in this report comes from it." followed by "Step yield is the exception, because its full quadratic model failed the limit on predictive power and was replaced by a reduced model (Section 5.3)." — Minor. Step yield is not a quality attribute and has no PAR, so it cannot be the exception.
23. "The run was analysed at its design setting." and "The 2 deviations of the study did not change its conclusions (Section 13)." — I refitted the Appendix B data with run 23 at its recorded pH of 3.38. The residual becomes −2,201 ng/mg, Cook's D becomes 0.38 and the residual SD becomes 1,218 ng/mg. The upper prediction limit over the narrowed NOR, with the offset at the low end, becomes 16,387 ng/mg, above ≤ 16,379. The scale-down model would then not qualify even at the narrowed NOR. The only justification given for using the design setting is that the result fits the design-setting prediction, which is circular, and no sensitivity analysis is reported. So the claim that the deviations did not change the conclusions depends on that analysis choice.

### B. Scientifically wrong or questionable (by mechanism or practice)

1. "A lower elution pH protonates more histidine and acidic residues, which disrupts more of both kinds of association and releases more host cell protein with the product." and "A lower pH protonates more histidine and acidic residues, which disrupts the electrostatic association of host cell protein with the antibody and with the resin, so more host cell protein is released with the product." — Questionable. Host cell protein that rides on the antibody leaves the column with it at every elution pH studied. Breaking that association during elution cannot raise pool host cell protein. The pH effect needs host cell protein held by the resin backbone or ligand that desorbs only at lower pH and otherwise leaves at the strip. §2.1 also says "electrostatic and hydrophobic" where §5.8 says only "electrostatic".
2. "A fragment is captured only if it still carries Fc." and "Fab fragments flow through with the load, and the pool carries less fragment than the feed." — Overstated. Native staphylococcal Protein A also binds the VH3 framework of Fab, and humanized IgG1 frameworks are often VH3. This holds only for a ligand engineered without VH3 binding, or for a non-VH3 antibody, and the report states neither.
3. "Step yield is the mass of antibody in the pool divided by the mass loaded, from the protein concentration by absorbance at 280 nm (AMV-3019) and the measured volumes." — Wrong for the load. A280 of clarified harvest measures all absorbing species, not antibody. Load titre is normally measured by analytical Protein A HPLC. Table 13.10 repeats this.
4. "The scale-down model is taken as representative for fragments on mechanism." and "The capture of Fc-bearing species and low-pH hinge hydrolysis do not depend on scale at equal bed height, residence time and elution pH." — Inconsistent with §3.1's own explanation of the leached Protein A offset. If the held manufacturing harvest carries more protease activity, the same proteases clip the antibody and give Fc-bearing fragments that Protein A captures. A scale offset for fragments is then expected, not excluded.
5. "Neither the life of the resin nor the protease activity of the load is a setting of the run, so within the ranges of one run leached Protein A was expected to be flat." and "Leached Protein A could not be modelled, and the mechanism gives no reason for it to follow the settings of a single run." — Questionable. Protein load and load flow rate set the loading time, so they set how long the ligand is exposed to harvest proteases. The mechanism does give a reason for dependence.
6. "Its NOR is also narrowed by this report, because the qualification of the scale-down model for pool host cell protein depends on it (Section 3.1)." — This uses the uncertainty of the laboratory model's offset as evidence of the parameter's criticality, which mixes model qualification with process impact.
7. "The decision to make them was taken after the result on the 3 planned runs was known." — The runs were added after a failed qualification and pooled with runs made 10 months earlier. This is optional stopping, which raises the false-pass rate, and the report does not address it. The 7 centre-point runs of the two designs are set-point runs of the scale-down model (§3.5) made at the same time as the designs, and the report does not say why they were not used.
8. "The out-of-trend leached Protein A result (DEV-005-02) was replaced by a valid re-assay." — The original result was replaced on a "suspected" cause (carryover), not a confirmed one. Its value and direction are not reported.

## Q6. Sentences that read as machine-written (padding, restatement, hedged emphasis, saying nothing)

The executive summary and conclusions restate findings by design, so they are not flagged for that alone.

- "It was applied at analysis and appears in no approved plan." — **Q6.** It restates the sentence before it, the Table 1.2 footnote a) and INV-001 finding 1 from the same section.
- "The step is also the principal point of clearance for host cell protein and DNA, and it partly clears fragments." — **Q6.** A verbatim repeat of §1.1.
- "In this matrix part of the host cell protein elutes in the low molecular weight window of SEC and is counted as fragment." — **Q6.** The fourth statement of the SEC co-elution point (§2.1, §1.4 item 4, Table 3.3 footnote a), and a fifth follows in the Table 5.12 footnote.
- "The qualification of the scale-down model does not compare these attributes, so the hold results carry no offset." — **Q6.** It repeats the last sentence of §3.1.
- "Every range and every conclusion against a criterion is therefore stated at manufacturing scale." — **Q6.** It restates the sentence before it, and recurs in §1.4 item 6.
- "A prediction of pool host cell protein or leached Protein A is translated to manufacturing scale by subtracting the offset of that output before it is compared with a criterion (Section 3.1)." and "The prediction of pool host cell protein or leached Protein A is translated to manufacturing scale by subtracting its offset before it is compared with the criterion." — **Q6.** The third and fourth statements of the offset subtraction.
- "The Cpk for leached Protein A is 2785.30, and no simulated batch of 2,000 fell outside these criteria." — **Q6.** It reports a number to two decimals that the next sentence calls not meaningful.
- "Collecting further into the tail adds antibody and little host cell protein, so the ratio falls." — **Q6.** It restates §5.3.1.
- "A higher load flow rate shortens the residence time and lowers the dynamic binding capacity." — **Q6.** A verbatim repeat of §2.1.
- "Load flow rate has no significant effect on pool host cell protein." — **Q6.** The third statement (executive summary, §5.3.1, §5.8).
- "The two parameters interact, and the fall of pool host cell protein with rising pH is steeper at high load." — **Q6.** A restatement in the mechanistic section that adds no mechanism.
- "For operation, elution buffer pH and protein load have the largest effects on pool host cell protein, and the risk lies in the corner of low pH and high load." — **Q6.** A restatement.
- "End of pool collect is also associated with pool host cell protein." — **Q6.** A hedged restatement. A designed experiment has just shown that the parameter lowers pool host cell protein, so "associated with" understates it.
- "Load flow rate is associated with lower yield at high load." — **Q6.** The same hedge.
- "Load flow rate is associated with lower step yield." and "End of pool collect is associated with higher step yield and lower pool host cell protein." — **Q6.** The same hedge again, in the capability section, where these sentences add nothing.
- "The elution buffer prepared below its target pH (DEV-005-01) showed that this release test depends on a correctly calibrated pH meter." — **Q6.** It says nothing a reader would miss, since every pH test depends on a calibrated meter, and it is the third statement. It also names no corrective action.
- "The release test is the control on which the WC-CPP class of elution buffer pH relies, and here it did not detect the error because the meter was incorrectly calibrated." — **Q6.** The fourth statement.
- "The limits of the univariate study are stated in Section 4.4." — **Q6.** A pointer that says nothing.
- "Each output is judged at every combination of NOR low, set-point and NOR high, on the 95 % prediction interval of a single run, which includes the uncertainty of the model coefficients and of the residual (PCMP-001 §6.4)." — **Q6.** It restates the Table 7.2 footnote b) directly above it.
- "Within its NOR cation exchange clears host cell protein better than the platform worst case, at the one-sided 95 % confidence bound, and its model passes the adequacy tests.", "The criterion of this step therefore holds only while cation exchange runs within its NOR." and "Anion exchange is credited with its platform value only, because its model fails the predictive power test." — **Q6.** The Discussion repeats §7.1 almost word for word and adds no interpretation.
- "The offsets of the outputs without a criterion are -0.2 percentage points for step yield, -116 plates per metre for column efficiency and -0.02 for peak asymmetry." — **Q6.** It reads Table 3.1 back.
- "On the planned runs the offset for pool host cell protein is -550 ng/mg (-1,799 to 699 ng/mg), and for leached Protein A -1.60 ppm (-2.76 to -0.43 ppm)." — **Q6.** It reads Table 13.3 back.
- "Step yield has no acceptance criterion, and its model is used for the classification of parameters only." — **Q6.** It restates §2.2.
- "Each design used one feed, so the effect of feed quality on the step was not estimated." — **Q6.** It restates §3.2.
- "The plan did not foresee these runs." — **Q6.** The third statement (§3.1, §13 table, §13.3).
- "No adequate model results for leached Protein A, so its dependence on the parameters of the multivariate design is not resolved." — **Q6.** "No adequate model results for …" is an unidiomatic formula used about nine times (F5, F6, §1.4, §3.1, §4.5, §5.3, §7.3 twice). It reads as templated.

## Q7. Sentences that depend on a code or label, or on an abstract stand-in

- "Leached Protein A is lower in the scale-down model, for an expected cause given in Section 3.1." — **Q7.** Name the cause: the longer harvest hold at manufacturing scale, with more protease cleaving more ligand during loading.
- "Leached Protein A is lower in the laboratory column, for the expected cause given in Section 3.1." — **Q7.** The same fix.
- "The model is qualified for leached Protein A over the NOR as characterized." — **Q7.** Name the NOR (protein load 20–40 g/L resin, before narrowing) and the rule (the conclusion is the same across the 90 % confidence interval of the offset).
- "Held at elution pH for 7 days at 2-8 °C or 21 °C, the Protein A eluate met the hold rule of PCP-005." — **Q7.** Name the rule (largest increase over the hold plus the highest level expected in the pool stays within the criterion).
- "Table 5.13 judges the hold against the hold rule of PCP-005 §7 (criterion 7)." — **Q7.** Same as above.
- "The model was qualified under SOP-1001 by the offset rule of PCMP-001 §7.1, as PCP-005 §5.1 applies it." — **Q7.** Three codes and a label; the rule needs to be named in this sentence.
- "SEC (AMV-3011) remains the method for aggregate, where no co-elution of this kind applies." — **Q7.** Name what does not co-elute: no host cell protein elutes in the high molecular weight window.
- "A model that fails criterion 3 or 4 was refitted with a justified change of terms, or it was not used to set a range." — **Q7.** Say "fails the lack-of-fit test or the predictive-power limit".
- "Table 5.6 judges each response-surface model against criteria 2 to 4 of PCP-005 §7." — **Q7 (mild).** Criterion codes only; the next sentence names them.
- "Each response-surface model is judged against the model adequacy criteria of PCP-005 §7, which Version 1.0 left to the analysis." — **Q7.** "Left to the analysis" is unclear. Say what Version 1.0 did, for example "did not apply".
- "Acidic variants are not an output of this step, so the two-sided capability assessment of INV-001 finding 4 does not apply here." — **Q7.** Say what finding 4 found, not only its code.
- "RA-001 assessed every parameter of the step before characterization began." and "RA-001 gives the scores and the rationale." — **Q7.** Name the document (the pre-characterization risk assessment) and give the scores, which the section depends on.
- "The screening design ran before the method decision AMD-001, and its pools were not retained." — **Q7.** Say what AMD-001 decided: nrCE-SDS replaced SEC for fragments. The same applies to the other bare uses of AMD-001 and S-PA-SDM.
- "At this step that one-factor test identifies elution buffer pH, whose PAR for pool host cell protein is narrower than its range studied." — **Q7.** "That one-factor test" stands in for "the rule that an effect matters when the PAR is narrower than the range studied".
- "No criterion upstream of this step relies on a worst case of the Protein A step, so this report carries no verification of its own." — **Q7.** "Verification" is abstract. Say "no Protein A platform value had to be checked against A-Mab data".
- "A model that predicts left-out runs this much worse than it fits its own runs cannot carry a criterion upstream." — **Q7.** "Carry a criterion upstream" is a metaphor. Say "cannot be used to recalculate the criteria of the steps before it".
- "The widened value rests on cation exchange alone." — **Q7.** Say "Only the cation exchange bound of 40.95-fold replaced a platform value".
- "It was widened by the rule of PCMP-001 §7.5." — **Q7 (mild).** A label; the rule is defined in the next sentences.
- "The criterion of this step therefore holds only while cation exchange runs within its NOR." — **Q7.** Name the criterion: pool host cell protein ≤ 16,379 ng/mg.
- "The scale-down model is qualified by its offset for both outputs with a criterion, but for pool host cell protein only after two changes." — **Q7.** Name the changes: the narrowed load NOR and the 6 added set-point runs.
- "The supplementary runs therefore changed the qualification for pool host cell protein." — **Q7.** Say what changed: not qualified became qualified at the narrowed NOR.
- "The limits of the univariate study are stated in Section 4.4." — **Q7.** Name them: no interactions, 2 runs per end, and a reference from another campaign.
- "Both are above the target of 1.33 that PCMP-001 sets." — **Q7 (mild).** A bare code. The same applies to "the criteria of PCMP-001 Version 2.0" in the executive summary; name it as the process characterization master plan.
- Table 4.1 note, "… as the scale-down model section explains." — **Q7.** A vague pointer; give "Section 3.1".

## Table observations

**Headers longer than two lines or with sub-headers running together**
- Table 1.2. The header takes three lines: the group row, "Criterion Rule / Criterion Basis" run together, and a lone "b)" line. Footnote b) sits on the Rule column header but describes only the leached Protein A "none" row, while the host cell protein row does have a Version 1.0 step limit. The code "R1" in a cell is explained only in a footnote.
- Table 3.1, and the same layout in Table 13.3. Three header lines, and "SDM Mfg SDM Mfg Estimate 90 % CI" runs together under two group headers. The CI cells wrap ("-929 to / 427"). The table does not say which NOR "Met over NOR" refers to (the narrowed 20–38 g/L).
- Table 5.6. Three header lines ("Adj./Pred./Model" over "R²/R²/p"). The model names wrap, and the step-yield label sits between its two rows, so the full-quadratic values print above the label.
- Table 5.9. "Max. D Run D > 4/n" runs together, and "Run" (the run with the largest D) is ambiguous.
- Table 5.13. "Highest expected / Largest increase" runs together.
- Table 7.1. "This campaign" over "At the edges / Within the NOR / 95 % bound" wraps into "At the Within 95 % / edges the NOR bound".
- Table 7.2. Three header lines.
- Table 8.1. "Crit. Spec" runs together.
- Tables 13.4 and 13.5 (Appendices A and B). Four to five header lines, with units split across lines ("(g/L / resin)", "Leached / PrA / (ppm)").

**Same value in every row of a column, or an index cell repeated instead of merged**
- Table 3.1: Runs SDM = 9 and Mfg = 5 in every row. Table 13.3: 3 and 5 in every row.
- Table 5.10: n = 2 in every row.
- Table 5.13: Met = "Yes" in every row. "Highest expected" repeats the same value in both temperature rows of each attribute instead of merging.
- Table 7.2: "Met across the NOR" = "Yes" in every row.
- Table 7.3. "Char. range" repeats the same four ranges in all three output blocks. "PAR (set-point)" equals "Char. range" in all 12 rows, and "PAR (NOR)" does in 11 of 12. One cell (3.25–3.9) carries information.
- Table 8.1: "Spec" = "upper" in every row.
- Deviation table (§13): Disposition = "retained" in every row.
- Tables 13.4 and 13.5: "Type" repeats "factorial" 16 times, "axial" 8 times and "center" 4 times instead of grouping the rows into blocks.

**Inconsistent formatting of one kind of value**
- Criteria: "≤2%" (Table 2.1) against "≤ 5 ppm" and "≤ 100 ng/mg". Table 5.13 gives the acidic-variant criterion as "≤ 39.6" where §4.5 has 18–39.6 %.
- Ranges: an en dash ("20–38") in most tables, but "3,802 to 13,320" in Table 7.2 and "-929 to 427" in Tables 3.1 and 13.3. Temperature ranges use a hyphen ("2-8 °C").
- Minus sign: a true minus ("−1 to +1", §3.5) but hyphen-minus everywhere else ("-251", "-5,245").
- Decimals: the Effect and Coef. columns of Tables 5.4, 5.5 and 13.6 mix integers and decimals (7,269 / 167 / 6.08 / -70.6). Table 7.1 mixes 0.70, 40.0, 3.16 and 10.0, and shows 40.9 where the text says 40.95, which looks like a rounding error. Table 13.9 prints "-0.00" three times and shows −0.05 where the text quotes −0.053.
- Thousands separator: "2785.30" in Table 8.1, against "16,379" elsewhere. It also carries two decimals on a value the text calls not meaningful.
- Spurious precision: sums of squares to nine digits (Table 5.8, 907,763,711) and %CV to two decimals (Tables 5.1 and 5.2, 33.84).
- Attribute labels: leached Protein A appears as "LPA" (Tables 5.10 and 5.11), "Leached PrA" (Appendices A and B) and "Leached Protein A" elsewhere. Run type is spelled "center" in the appendix tables and "centre" in the text. Table 4.1 says "Char. range" where the text says "range studied".
- Hyphenated compounds in tables, where the prose has the plain form: "Elution-buffer pH" (deviation table and Table 13.5 footnote), "Host-Cell Protein ELISA", "Size-Variants", "Life-Cycle", "Process-Parameter … Control-Strategy" (SOP/AMV list).

**Other table issues**
- Uncaptioned tables: related documents (§1.3), the SOP/AMV list (§3.3), the deviation register and the discrepancy table (§13). The numbering shows gaps where they fall (no Table 1.1, 3.2, 13.1 or 13.2).
- Appendix tables are numbered 13.4–13.10, continuing Section 13, instead of A.1, B.1 and so on.
- Table 4.1: set-point and NOR run together in two rows ("30 20–38", "20 15–25").
- Table 4.2: the header row "Code Factor Unit" is repeated alone at the top of page 24 with no rows under it.
- Table 7.3 footnote typo: "buffer ph (pH)".
- Tables 7.2 and 7.3 print leached Protein A and fragment rows from models the report rejects (see Q5 A1 and A2).
- Table 5.9's step-yield row describes the discarded full quadratic model (see Q5 A9).

## Answers for the document as a whole

| # | Question | Answer |
|---|---|---|
| 1 | Does every causal claim name a physical cause and direction in its own clause? | **No.** 12 sentences flagged. The core mechanisms pass, but several causal clauses use "act on", "sets" or a procedural cause, or give no direction. |
| 2 | Is every technical term a term of art? | **No.** Coined terms include NOR-propagated PAR, set-point analysis, hold rule, offset rule, widened on verification, NOR in force / as characterized, floor, one-factor test, and univariate / multivariate parameter. |
| 3 | Does any sentence tell the reader how to file a finding, or answer an unraised objection? | **Yes (fails).** 11 sentences, mostly defensive glosses about the rule history and filings away of the acidic-variant results. |
| 4 | Is every criterion stated with its basis and every result reported as met or not met? | **No.** The held-eluate criteria have no stated basis. The acidic-variant lower limit is missing from the Table 5.13 verdict. The drug substance Cpk of 1.03 against the 1.33 target and the leached Protein A Cpk get no verdict. No residual DNA criterion is set or justified. |
| 5 | Is any statement scientifically wrong or contradicted by the document's own tables or figures? | **Yes (fails).** 23 checked contradictions and 8 mechanistic or practice issues. The most consequential: the F7 PAR claim against §5.3.4/§7.3; the acidic-variant statements against Tables 5.12/5.13; "No criterion of this step was tightened" against Table 7.1; the Table 5.9 step-yield row being the discarded model; the prediction-limit sidedness on which the NOR narrowing rests; and run 23, where analysing at the recorded pH 3.38 takes the scale-down model qualification limit to 16,387 ng/mg, above ≤ 16,379. |
| 6 | No machine-like sentences? (yes = none flagged) | **No.** 26 flagged items (30 sentences), mostly restatements and the hedged "is associated with" for designed-experiment effects. |
| 7 | Every sentence understandable alone? (yes = none flagged) | **No.** 24 flags, mostly bare codes and labels such as the hold rule, the offset rule, criterion numbers, RA-001 and AMD-001, and abstract stand-ins such as "carries no verification of its own" and "carry a criterion upstream". |
