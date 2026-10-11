# Readability review of PCR-009 Version 2.0, after fix pass 1 and the data-state pass (2026-10-11), medium effort

Saved by the coordinator from the agent's hand-back.

## Review of PCR-009 (virus filtration characterization report, Version 2.0, draft)

**Model:** Claude Opus 5.5 (claude-opus-5-5). I read only `/home/moritz/github_repos/synthetic_data/.claude/work/2026-10-08_01_rev2-campaign/PCR-009_virus_filtration.DRAFT.txt`. I changed nothing and wrote no files.

**Numbers checked against the tables.** I recomputed the following from Appendix B and Tables 5.7, 5.8 and C.1, and all of them agree: the MVM model line (6.31 to 4.57), the 137.6 L/m2 crossing, 5.25 and 5.54 at the NOR, the 91 % grid, the leverage of run 5 (0.25), the residuals of runs 5 and 2, the sums of squares for pure error and lack of fit, the screening effect of A (−1.61), the fragment curvature (−0.08 and +0.05), the fragment upper limit of a single run (0.78), the gap formula for a model with no term, the count of 13 submodels, the claim sums (16.72 and 8.62), the three MVM results below the claim, and the Cpk values within rounding. The flags below are what remains.

### Q1. Causal verbs without a physical cause in the clause
- "The study shows that filtration volume is the parameter that governs the MVM clearance of the step." (§11). It uses "governs" without naming the cause. It should say that fouling shifts flux to the largest pores as volume rises.
- "the maximum load is the parameter that bounds the claim" (§2.1) and "For operation, the volume filtered per square metre of membrane is the parameter that bounds the MVM claim." (§5.4). Neither names a mechanism or a direction in the clause.
- "Filtration volume was ranked high because MVM retention falls as the volume filtered per unit area rises." (§2.3). The cause given is the effect itself. It does not name the fouling or the shift of flux.
- "Filtration pressure sets the flux." (§2.1). No direction is given.
- "Because the load sets how much of the membrane is still open and the pressure sets how fast the filtrate crosses it, PCP-009 §4.3 expected the fall ... to be steeper at high pressure" (§2.1). It uses "sets" twice without a direction. The two clauses also do not imply an interaction.
- "...does not depend on the antibody, so the platform experience sets the direction expected for each effect." (§2.1). "Sets" is used here for an inference, not for a cause.

### Q2. Terms that are not terms of art
These are coined or idiosyncratic:
- "NOR-propagated analysis/PAR"
- "least favourable NOR combination"
- "limit on overfitting" (the term of art is the predicted R² gap)
- "criterion on influential runs"
- "statistic of judgement"
- "model with no term" (the term of art is "intercept-only model")
- "near-equivalent models"
- "the Version 1.0 conditions"
- "single-run limit"
- "Spread" (as a residual test name)
- "the register" (meaning the CQA register)
- "the claim of this step" used as a criterion

"Knowledge space", "characterized region", WC-CPP, "flux decay" and "volumetric load" are acceptable.

### Q3. Sentences that tell the reader how to file a finding
- "The criterion, the statistic of judgement and the model changed together, and the move reflects the three changes at once." (§1.4)
- "Criterion 3 then judges the number of runs and not the model." (§5.3)
- "Because the selected model is not adequate, its fourth criterion decides nothing." (§5.3)
- "...was kept, so the PAR and the design space do not rest on the deletion." (§11). This answers an objection nobody raised.
- "On the mean prediction of every output the region is the same, because the output that bounds it is judged on its mean either way." (§6)
- "...so the classification of an affected parameter is a judgement on the values stated below." (§9). This renames the finding as a category.
- "Its leverage, 0.25, is below 2p/n = 0.33, and like every run it lies inside the range studied." (§5.3). The trailing gloss adds nothing.
- Borderline: "The lower edge of the PAR is the lower end of the range studied, where the study stopped and not where the claim fails." (§7)

### Q4. Criteria and their basis
Every step criterion and every result is stated with its basis and judged met or not met, in Tables 7.1, 7.2, 5.5 and 5.6, the objectives and the success criterion. The gaps are in the basis of the higher-level criteria:
- The cumulative requirements "≥ 8.6 log10" and "≥ 16.7 log10" (Table 2.1, §2.2) are given with no basis. Nothing says how they derive from the virus burden and the safety margin.
- "Their criterion was set by the sponsor when fragments joined the register" (§2.2). That names who set the 2.00 % fragment criterion, not why.

### Q5. Statements that are wrong or that conflict with a table
1. "A membrane that passes the test has no defect large enough for the test to detect, and the retention of XMuLV depends on that integrity." (§10). The same claim appears in §11 and in the PD-009-04 paragraph. This is misleading. Post-use integrity tests of parvovirus filters are designed to detect loss of small-virus retention. MVM retention depends on membrane integrity at least as much as XMuLV retention does.
2. "A higher pressure compresses the fouling layer and raises the flux" (§2.1). This attributes the wrong cause. Compressing the fouling layer raises its resistance. Flux rises with pressure despite the compaction, not because of it.
3. "step yield is limited by product held up in the fouling layer and in the system. Yield is therefore expected to be high and to fall slowly as the load rises." (§2.1). The mechanism stated contradicts the expectation. A fixed system hold-up is a smaller fraction of a larger load, so yield should rise with load unless the loss in the fouling layer grows faster.
4. "The interaction model leaves one degree of freedom for lack of fit, which is the test for curvature, so its fit statistics overstate how well it fits" (§4.2). This is a non sequitur. The fit statistics are optimistic because 4 parameters are fitted to 5 distinct points, not because of the one degree of freedom for lack of fit.
5. Table 13.1 gives the outcome of DEV-009-02 as "run retained in the analysis" (singular). §13.1.2 conflicts with it: "the runs made on the lot were retained ... The lot may therefore have been used for several runs". The Executive summary also says "The runs concerned".
6. "A design of 12 runs with an SD of the centre points of 0.12 log10 detects a slope..." (§11). It uses the centre-point SD (0.12). The residual SD of the model is 0.23 (Table 5.5), and that is what sets the standard errors.
7. "The lower 95 % limit of a single run at the least favourable NOR combination is 4.71 log10" (§6). 4.71 matches the lower end of a two-sided 95 % interval. A one-sided 95 % limit computed from Tables 5.7 and 5.8 is about 4.81. The text should label the limit precisely.
8. Low severity. Table 5.1 gives the response-surface centre-point SD of XMuLV as 0.18, the screening yield SD as 0.77 and the response-surface yield SD as 0.84. Recomputed from Tables A.1 and B.1 they are 0.17, 0.75 and 0.83. This is probably rounding in the appendix values, but it should be checked.
9. Low severity. In Table 13.1 and §13.1.1, a design run is judged "above the NOR" at 22 psi, while the designs deliberately ran at up to 30 psi. The relevant reference is the run's own set pressure.

### Q6. Sentences that read as machine-written
- "Version 2.0 judges every output with a criterion against the criteria of the master plan PCMP-001 Version 2.0 ..." (Executive summary)
- "The conclusions on the PARs moved." / "...the move reflects the three changes at once." (§1.4)
- "Because the selected model is not adequate, its fourth criterion decides nothing." (§5.3)
- "Criterion 3 then judges the number of runs and not the model." (§5.3)
- "On the mean prediction of every output the region is the same, because the output that bounds it is judged on its mean either way." (§6)
- "...and it costs no product that the designs detect (PCP-009 §7)." (§6)
- "A design of 12 runs ... detects a slope as large as the effect of volume, but not effects of the size of the standard errors of these terms." (§11). This is tautological.
- "PCP-009 §7 asks how this report reads 'the scale-down model is qualified'." (Conclusion 1)
- "With the criteria as they would have been without corrective action CA3, the criteria of this step, the judgement of each output over the NOR and the PARs of MVM LRF are the same." (PD-009-01 paragraph). This is circular.
- Restatement as a pattern:
  - "Version 1.0 stated that every run passed its post-use test with no result recorded" appears four times (§3.1, §11, Table 13.2, PD-009-03).
  - The PD-009-01 to PD-009-07 paragraphs largely restate Table 13.2.
  - "Step yield has no criterion" recurs throughout.

### Q7. References by code alone, and abstract subjects
- "The selected model of MVM LRF meets the first three model-adequacy criteria of PCMP-001 §7.2. It does not meet the fourth..." (Executive summary). It should name the F-test, lack of fit, the predicted R² gap, and residuals and influence.
- "Table 5.5 judges each selected model against the first three criteria of PCMP-001 §7.2, and Table 5.6 against the fourth." (§5.3). It should name the criteria.
- "The model of MVM LRF does not meet the fourth criterion." (§5.3). It should name "the criterion on residuals and influential runs".
- "The model with no term ... meets the second and third criteria." (§5.3). It should name lack of fit and the overfitting gap.
- "...so both Version 1.0 conditions are met." (§5.3). It should name normality of the residuals and the residual SD against the distance to the criterion.
- "Criterion 3 then judges the number of runs and not the model." (§5.3). It should name the predicted R² gap.
- "Conclusion 3: '...meets the first three adequacy criteria of PCMP-001 §7.2 and fails the fourth on run 5.'" It should name the criteria and describe run 5.
- "Its upper boundary depends on run 5." (Conclusion 7). It should say "the axial run at 50 L/m2 and 19 psi with the highest LRF".
- "The last records the analyses that the plan does not contain (PD-009-07)." (Executive summary). It should name the analyses.
- "PCP-009 §7 asks how this report reads 'the scale-down model is qualified'." (Conclusion 1). It should state what the plan requires.
- "...without corrective action CA3..." (PD-009-01 paragraph). It should say "without the model selection".
- Abstract subjects:
  - "The conclusions on the PARs moved." (§1.4). It should name the PAR values.
  - "That bounds an event that affected one response-surface run." (§13.1) and "That does not bound an event that affected several runs" (§11). Both should name the deletion of each run in turn.
  - "The boundary rests on single runs." (§6) and "The upper PAR edge of filtration volume depends on single runs." (§11). Both should name runs 5 and 7 and what deleting them does.

### Answers for the document as a whole
1. No
2. No
3. Yes (several sentences do it)
4. No (the step criteria are fully based and judged; the basis of the cumulative viral requirements and of the fragment criterion is not given)
5. Yes (items 1–7; items 1–3 are the substantive ones)
6. No
7. No