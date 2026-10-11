# Readability review of PCR-007 Version 2.0, after fix pass 1 (2026-10-11), medium effort

Saved by the coordinator from the agent's hand-back.

# Review of PCR-007 (cation exchange chromatography characterization report, Version 2.0, draft)

**Reviewer model:** Claude Opus 5.5 (claude-opus-5-5)

I read only `/home/moritz/github_repos/synthetic_data/.claude/work/2026-10-08_01_rev2-campaign/PCR-007_cex.DRAFT.txt` and changed nothing. I recomputed most of the numbers in the text from the tables: the multipliers from the Table 5.6 coefficients, the offsets, the drift arithmetic, the Cpk values, the clearance factors, the counts of near-equivalent models, and the 22 grid points. Nearly all of them agree. The flags below are the exceptions.

---

## Q1. Is a physical cause named where the causal verb stands?

- "...to have little effect on the aggregate separation, which happens during elution." (§2.1, item 2). **Fails.** It gives a phase of the cycle as the cause, not a physical one. It should say that ionic strength at load and wash does not change the relative charge of aggregate and monomer at the elution pH.
- "Within this range conductivity has no demonstrated effect on aggregate, as expected for a parameter that acts during the wash rather than during elution." (§5.6). **Fails** for the same reason. Load conductivity also acts on binding during loading.
- "Curvature was expected in the effects of elution stop collect and elution buffer pH, because both move the cut point against a peak that has a maximum" (§2.1). **Fails.** pH does not move a cut point. It changes the charge of the antibody and so the position and width of the peak.
- "Elution flow rate was assigned to a univariate assessment, because its expected effect on the separation is small." (§2.3, item 2). **Fails.** No mechanism is given, such as residence time or mass transfer. The mechanism only appears later, in §4.4.
- "Protein load, elution buffer pH and elution stop collect govern aggregate, and protein load and load/wash conductivity govern host cell protein..." (§11). **Fails.** "Govern" carries no physical cause or direction.
- "The main effects of load, pH and conductivity follow the physical chemistry of the step." (§11). **Fails.** It invokes physical chemistry without naming any.

## Q2. Is every technical term a term of art?

These terms are coined or local to the document and are not established terms of art:

- "NOR-propagated" (range or analysis)
- "set-point analysis"
- "single-run limit"
- "criterion in force" and "a priori criterion"
- "limit on overfitting" (used for the R² minus predicted R² gap)
- "near-equivalent models"
- "bound of a single batch"
- "analytical method decision"
- "study event"
- "Flag limit" and "F median" (Table 5.5, §13.2.2)
- "Region inside" and "Region outside" (Tables 5.8 and 5.9)
- "verification-qualified" (AMV-3221)
- "managed forward" (§11)

"No run of any model exceeds the F median of the Cook's distance" (§13.2.2) is also mis-phrased: the Cook's distance is compared with the median of F(p, n − p).

## Q3. Does any sentence tell the reader how to file its finding?

- "The excess can never exceed the host cell protein present." (§3.3). Answers an objection nobody raised.
- "These are sensitivities, and the selected model decides." (§5.3.4)
- "The model on all runs decides, so this is a sensitivity and changes no conclusion." (§5.3.5)
- "The contours of a model with no interaction between the two factors plotted are parallel on any scale, so their shape there is no separate evidence." (§5.3.7)
- "The classification of the stop collect rests on the measured effect, not on the mechanism (Section 9)." (§5.6)
- "...on a fragment model that does not meet PCMP-001 §7.2, and the confirmation carries that limitation." (Executive summary). Also "The confirmation has a limitation." (§7.4)
- "...so the platform value stands, and this result is for information (Section 7.4)." (§5.4)
- "...and a judgement of relevance is named as a judgement." (§9)
- "That is a judgement, and no plan sets a threshold for it." and "For yield the class is a judgement too." (§9, elution flow rate)
- "...so these departures from the expected mechanism do not weaken them, but they remain unexplained." (§11)

## Q4. Is every criterion stated with its basis, and every result reported as met or not met?

- "Aggregate in the pool of the run was verified by 3 determinations with the method AMV-3221... the mean of 3 determinations has a 95 % confidence interval of ± 9.44 % of its value." (§13.1.2). **Fails.** No result, no criterion and no met or not met is given. Only the method's confidence interval is stated.
- "...the column inlet temperature was above its set-point for 38 minutes and reached 26.4 °C." (§13.1.2). **Fails.** Neither the set-point nor the permitted range is stated.
- "Section 12 states the outcome against each objective." (§1.2). **Fails in part.** Conclusions 1, 2, 4, 5 and 6 report outcomes but never say "met". Only conclusion 3 says met or not met, and only for fragments.
- Conclusion 2 (objective 2). **Fails.** Objective 2 requires the fitted models to predict that fragments meet their criterion. Fragments have no model, yet objective 2 is not declared not met for fragments, while objective 3 is (see also Q5).
- Everything else passes. The criteria in Tables 7.1, 7.2 and 7.4 each carry a basis and a met or not met outcome, and so do the scale-down model qualification, the capability target, the flow-rate range and the adequacy criteria.

## Q5. Is anything scientifically wrong, or contradicted by a table in the same document?

1. "...the retained sample was re-tested and gave pH 5.02..." for a "Tris load/wash buffer" (§13.1.1, Table 13.1). **Scientifically implausible.** Tris (pKa about 8.1) has no buffering capacity at pH 5.
2. "Most host cell proteins have an isoelectric point below the load pH and leave in the load flow-through" (§2.1). **Conflicts with the load pH of about 5.0** implied in §13.1.1. Most CHO host cell proteins have a pI above 5 and would bind a cation exchanger at that pH.
3. "Viral clearance and the final levels of host cell protein, residual DNA and leached Protein A are controlled by anion exchange and virus filtration, in PCR-008 and PCR-009" (§10). **Wrong on two counts.** Virus filtration does not clear these impurities. §1.1 also credits enveloped virus clearance to low-pH inactivation, which this sentence leaves out.
4. Conclusion 2 against conclusion 3 and objective 2 (§1.2). **Inconsistent.** Fragments are in objective 2, but only objective 3 is declared not met for fragments.
5. "With run 14 deleted the selection keeps a stop collect term of −0.76 percentage points per coded unit (p = 0.078)" (§5.3.6). **Likely a transcription error.** −0.76 and p = 0.078 are exactly the conductivity (B) term in Table C.2.
6. "Its cause was that the expiry date was not checked when the buffer was prepared." (§13.1.1). **Illogical.** The lot expired after it was prepared, so a check at preparation could not have caught it. The missing check is at the time of use.
7. "...each NOR edge lies inside its proven acceptable range by at least the distance to the end of the range studied" (§7.3). **Wrong wording.** The PAR equals the range studied (Table 7.3), so the margin is exactly that distance, not "at least" it.
8. Captions of Figures 5.4 and 5.5 give "step yield (fraction)". **Conflicts with Tables 5.3, 5.10 and B.1**, which give yield in %.
9. Residual DNA criterion "≤ 0.001 ng/dose" (Tables 2.1 and 8.1, §8). **Implausible.** It is four orders of magnitude tighter than the usual 10 ng/dose and looks like a unit error.
10. PD-007-02 Reason, "selected models of this step do not meet the criterion..." (Table 13.2). **Conflicts with Table 5.5.** Only the host cell protein model fails criterion 4, so the plural is wrong.
11. "The bound comes from the 28 planned runs of its response-surface design... On all its runs, with the 12 runs of the INV-002 augmentation, the bound is 4.18." (§7.1, item 3). **Ambiguous.** It does not say which run set gives the bound in force, or whether the 28-run value also equals 4.18.

## Q6. Which sentences read as machine-written?

- "The log scale has four consequences for the reader." (§3.5). A signpost.
- "All four screening factors were carried into it, so the plan's rule for a screening factor left out of the response-surface design did not apply." (§4.3). States the absence of a rule nobody invoked.
- "For operation, aggregate control rests on protein load, elution buffer pH and elution stop collect together..." (§5.6). Restates the section.
- "The step contributes to every attribute in Table 8.1." (§8). Says nothing.
- "The study shows how the four multivariate parameters act on the pool." (§11). An empty topic sentence.
- "Without the feed lots, no run can be traced to a lot." (§11). Also "...so runs cannot be compared by lot." (§3.2). Both are tautological.
- "Five limitations remain, and each is managed forward." (§11). Padding, and not true for item 4 (fragments), which names no forward action.
- "Residual DNA has no criterion at this step, so no conclusion of this report depends on its offset." (§3.1). Restated in §11 and §13.2.4.
- "The results roll up into the master report PCMR-001." (Executive summary). Repeated in conclusion 7 and §10.
- PD-007-03 Reason, "the set-point reference was taken from the qualification runs" (Table 13.2). Repeats the "Done" column instead of giving a reason.
- PD-007-02 Reason (Table 13.2). Restates the finding as its own reason.

## Q7. Can each sentence be understood without the rest of the document?

- "In the flow-rate study the comparison of item 5 is used." (§3.5.1, item 1). Also "...by the approach of Section 3.5.1 item 5." (§5.5) and "...the comparison of Section 3.5.1 item 5 has no screening effect..." (§5.5). Should name the comparison: the difference between the two ends with its 95 % CI, set against the smallest significant screening effect.
- "...confirmed by the rule of PCP-007 §7.6..." (Executive summary and conclusion 6). Should name the rule: the lowest predicted clearance factor within the NOR is not below the platform value.
- "With screening run 6 deleted... With response-surface run 14 deleted..." (§11). Should name the expired buffer lot run and the column temperature excursion run.
- Conclusion 7, "Without run 6... Without run 14..." Same fix as above.
- "With run 14 deleted the selection keeps a stop collect term..." (§5.3.6). Should name it as the run with the temperature excursion.
- "...and the trend is bounded over the NOR by its size against the criterion." (§11). An abstract stand-in. Should name the run-order drift of the host cell protein residuals (a factor of 1.13, giving 326 against 418 ng/mg).
- "The 2 study events recorded in Version 1.0 are reported under their DEV numbers..." (Executive summary). Should name the expired buffer lot and the temperature excursion.
- "...S-CEX-VER from 2026-09-24 to 2026-09-25 and S-VI-WC from 2026-09-26 to 2026-09-29." (Executive summary). Should say what the studies tested: aggregate and fragment clearance at the set-point on low-pH pool material.
- "...the plan's rule for a screening factor left out of the response-surface design did not apply." (§4.3). Should state the rule.

---

## Answers for the document as a whole

| # | Question | Answer |
|---|---|---|
| 1 | A physical cause is named wherever a cause is given | **No** (6 sentences fail) |
| 2 | Every technical term is a term of art | **No** |
| 3 | Some sentence tells the reader how to file its finding | **Yes** (10 or more) |
| 4 | Every criterion has its basis, and every result is reported met or not met | **No** (the run 14 aggregate verification, the temperature excursion, and objectives without a met or not met) |
| 5 | Some statement is wrong or contradicted by a table | **Yes** (the most serious: Tris at pH 5.02, host cell protein pI against the load pH, the virus filtration claim in §10, the objective 2 inconsistency, the −0.76 / p 0.078 duplicate) |
| 6 | No sentence reads as machine-written | **No** |
| 7 | Every sentence is understood alone | **No** |
