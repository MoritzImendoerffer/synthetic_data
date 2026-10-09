# Content review of INV-002 (response-surface models below the model-adequacy criteria)

Reviewer: Claude Opus 5.5 (`claude-opus-5-5`), 2026-10-09.
Source: `INV-002_model_adequacy.DRAFT.txt` (the text of the PDF dated 2026-09-28). I read no other
file in the repository. Every number below is either printed in the document or computed in Python
from printed numbers and from the design structure the document describes (face-centred designs of
28, 18 and 12 runs, which implies 4 centre points each). Quotes are verbatim, except that words
the PDF split with a hyphen at a line end have been joined again.

## Answers for the document as a whole

| # | Question | Answer |
|---|---|---|
| 1 | Does every causal clause name the actual cause in the clause where the verb stands? | No |
| 2 | Is every technical term a term of art? | No |
| 3 | Does any sentence tell the reader how to file the finding it has just stated? | Yes |
| 4 | Is every acceptance criterion stated with its basis, and every result reported against it as met or not met? | No |
| 5 | Is any statement scientifically or statistically wrong, or contradicted by a table in the document? | Yes |
| 6 | Is the text free of sentences that read as machine-written? ("yes" means none flagged) | No |
| 7 | Can every sentence be understood without the rest of the document? ("yes" means none flagged) | No |

The most important problems, in order of consequence:

1. The refits in Table 5.1 and Table 6.2 break the strong hierarchy that Section 5 says the
   elimination keeps (five refits). Either the tables leave out terms the refit kept, or the refits
   are not hierarchical. The simulation uses these refits as the true model.
2. The second block did not "sharpen" two of the three models. It changed them (Table 8.1): high
   mannose lost 4 of its 6 terms and moved to the log scale, and acidic variants gained 4 terms.
   This weakens "not needed for adequacy". It also bears on the verification behind the
   intermediate acceptance criteria, which uses models selected on the planned runs only.
3. The document never says that a §7.2 check on a model chosen by an exhaustive AICc search on the
   same runs is optimistic. Yet two host cell protein criteria widen by about 30 % because the anion
   exchange model passes only once selected. All four criteria in Table 9.2 come out wider under
   model selection, which was adopted after the failures were known. The document states neither
   the direction nor why it is acceptable.
4. The sample-size simulation draws constant-variance normal errors on the raw scale for the three
   outputs that Section 8.1 and Table 8.1 put on the log scale. Its "assurance" is computed at
   fixed point estimates.
5. Text and tables disagree in five places: Table 6.1 (0.01 against "at or below 0.005"), Table 8.1
   (0.02 against 0.02 described as "lower"), Table 9.2 (changes at three steps against "Two
   changes"), Table 5.1 (footnote a against the anion exchange rows), and Tables 8.1 and 9.1 plus
   Section 9.2 against "does not give the results of the new runs".
6. The effectiveness check fails more often than not even if the preventive action works. With
   0.90 per model, two plans with 8 models between them all pass with a chance of about 0.43.

---

## Question 1: is the actual cause named?

1. "The model fails because it fits the runs it was estimated from much better than it predicts a run left out of the fit." (Section 3)
   Q1: the "because" clause restates the failed test. The cause is the high leverage of a full quadratic on these designs (average 0.50 to 0.56) acting on residual variation that is large relative to the effects.

2. "Predicted R² therefore falls well below R², even where the lack-of-fit test shows no systematic error." (Section 4)
   Q1: leverage is the same for the 8 models that pass, so it cannot be the whole cause. The gap is about (1 − R²)·[1/(1 − h)² − 1], about 3.6 × (1 − R²) at h = 15/28, so a model fails unless R² is above about 0.95. This dependence on the unexplained share is not named.

3. "More runs narrow the gap only slowly, because the model has nothing to estimate but noise." (Section 4)
   Q1 (minor): names the condition, not the property. With no effect, R² minus predicted R² depends only on the number of terms relative to the number of runs, not on the noise level, so it shrinks only as runs outgrow terms.

4. "Viral clearance is not a drug substance test, so its models are refitted and no virus is spiked." (Summary), and "They are refitted because viral clearance is not a drug substance test." (Section 5)
   Q1: the cause is a category label. The real reason (clearance is claimed from worst-case spiking runs against a cumulative claim, ICH Q5A) appears only in rule 2. The label also does not explain why the XMuLV model at low-pH viral inactivation, which changes a NOR (Section 9.2), gets no runs.

5. "AICc is used because these designs are small." (Section 8.1)
   Q1: names the condition, not the property. When the parameter count approaches the run count, the AIC penalty is too small and favours overfitted models. AICc adds 2k(k + 1)/(n − k − 1) to correct this. The next sentences give only part of this.

6. "The second change is at cation exchange, where the bounds move with the model." (Section 9.1), and "The anion exchange host cell protein model meets §7.2 only once selected, and the bounds at cation exchange move with the model." (Summary)
   Q1: "move with the model" names no cause. The bounds differ because the selected models (log scale, 8 and 6 terms, Table 9.1) give a different worst-case prediction and a different standard error from the 15-term full quadratic.

7. "A step’s augmentation has the largest number of runs that any of its models needs, so a model of the same step that needs fewer runs has an assurance above the target at that size." (Section 6.1)
   Q1: the inference rests on assurance never falling as runs are added. That property is not stated, and it is not guaranteed (see Question 5, item A6).

8. "The designs span the characterized range, so a response whose measured results all meet the criterion meets it over the NOR." (Section 5)
   Q1: covering the range is not a sufficient cause. The conclusion also needs batch-to-batch and assay variation that is small against the margin to the criterion, and no extreme between design points (see Question 5, item B6).

These causes are named correctly and are not flagged: leverage as the weight of a run in its own fitted value; the refit used as the truth because the full model would carry its fitted noise; squared terms correlated because every corner run sets all of them to one; an exhaustive search because a stepwise search can stop at a local optimum; back-transformed intervals keeping their coverage because the transformation preserves order; the log scale for host cell protein because effects act by a factor and the spread grows with the level.

## Question 2: terms of art

1. "The assurance is the share of simulated data sets in which the planned model meets both criteria." (Section 6.1, and throughout)
   Q2: "assurance" is a term of art for the probability of success averaged over uncertainty in the effects (O'Hagan, Stevens and Campbell 2005). Here it is computed at fixed point estimates from one refit. That is the probability of success, or power, at the estimated effects.

2. "Each curve uses its own random stream of the seeded process model, so the calculation gives the same result each time it is run." (Section 6.1)
   Q2: "seeded process model" is not a term of art. In a real report it would also say that the data come from a simulator. Write "a fixed seed of the pseudo-random number generator, one stream per curve".

3. "The criterion is the next two characterization plans approved with the design-size check, and every planned model adequate at first analysis." (Section 11)
   Q2: "design-size check" is coined. Call it the simulation-based sample-size justification of preventive action PA1.

4. "For high mannose, 4 terms of the planned-run model did not survive the second block." (Section 8.3.1)
   Q2: "planned-run model" is a coined compound. Write "the model selected on the 28 planned runs".

5. "For every output with a criterion the two give the same conclusion, at the NOR as characterized and at the NOR in force." (Section 9.2)
   Q2: "conclusion over the NOR", "NOR as characterized" and "NOR in force" are coined labels. They are used from Section 1 onward and never defined.

6. "Its full quadratic model does not meet §7.2, so its bound of 4.84 cannot widen a criterion, and the platform fold of 4 enters the derivation." (Section 9.1)
   Q2 (minor): "platform fold" is shorthand. Write "the platform worst-case clearance fold of 4".

Not flagged: "limit on overfitting" is plain English for the predicted-R² criterion. It is defined in Section 3 and used consistently.

## Question 3: telling the reader how to file a finding

1. "The augmentations were therefore not needed for adequacy, and they sharpened the estimates." (Summary)
   Q3: the trailing clause files the finding (the runs were not needed) as a benefit, answering an objection nobody raised. Table 8.1 shows a change of model, not a sharpening (Question 5, item A7).

2. "The second block sharpened the estimates." (Section 8.3.1)
   Q3: the same gloss. It leaves unanswered the question a reviewer would ask: why were both augmentations completed after 2026-09-15, once model selection showed they were not needed?

3. "Once selected, the models that the augmentations were made for meet §7.2 on the planned runs alone, and the augmentations sharpened their estimates." (Section 12)
   Q3: the same gloss, a third time.

4. "The simulation is built from what the planned runs show, and from nothing else." (Section 6.1)
   Q3: "and from nothing else" heads off an objection nobody raised. It is also not quite true, because the normal, constant-variance error model is an assumption, not something the runs show.

## Question 4: criteria with their basis, results against criteria

1. "The number of runs is the smallest that gives an assurance of at least 0.90 that the planned model, the full quadratic with a block term, meets §7.2 on all runs (Section 6)." (Section 5, rule 1)
   Q4: no basis is given for 0.90. Nor is one given for the cap at the planned design size, beyond "keeps a remedy from becoming a new study". The document also does not say that 0.95 is the ceiling (Question 5, item B3).

2. "On it, the lowest mean LRF within the NOR as characterized is 6.16, at inactivation pH 3.6, hold time 60 min and temperature 19 °C, and the step claim of 6.6 is not met." (Section 9.2)
   Q4: the basis of the 6.6 log10 step claim is not stated.

3. "On the selected model of all runs, the lower prediction limit at culture pH 6.95, culture temperature 34.5 °C, culture duration 18 days and dissolved CO2 (pCO2) 130 mmHg is 16.2 % at manufacturing scale, below the lower limit of 18 %." (Section 9.2)
   Q4: the basis of the 18 % lower limit (intermediate criterion or specification) is not stated, and the result is not written as "not met".

4. "The full quadratic model of the planned runs does not meet the criterion either." (Section 9.2)
   Q4: no lower prediction limit is given for the full quadratic model, so "does not meet" cannot be checked.

5. "Once selected, the three models that the augmentations were made for meet §7.2 on the planned runs alone." (Summary), and "Model selection gives an adequate model for 19 of the 22 outputs with a criterion." (Section 8.3)
   Q4: §7.2 has three tests, but for the selected models only R² minus predicted R² is reported (Table 8.1). No lack-of-fit or model F-test result is given for any selected model.

6. "Each is judged on its measured results, and every measured result meets its criterion at manufacturing scale." (Section 8.3.2)
   Q4: neither the criteria nor the range of measured results is given for the three outputs, so "meets" cannot be checked, and the margin is unknown.

7. "PCMP-001 Version 2.0 derives the intermediate acceptance criteria a priori, from the platform worst case of each downstream step." (Section 8.2)
   Q4: the drug substance limits the derivation starts from are not stated, and neither is the chain of steps. They back out of Table 9.2 as 100 ng/mg host cell protein and 5.0 % aggregates at the cation exchange output. Without them the a priori values 9.30, 16,000, 10.0 and 400 cannot be checked.

8. "QA opened INV-002 on 2026-08-31 and classified it as minor." (Summary), and "The investigation confirmed the classification as minor." (Section 12)
   Q4: the classification criteria (minor against major) are not stated. The basis is only implied by "no product impact".

## Question 5: wrong, unsupported, or contradicted by a table

### A. Contradicted by a table in the same document

A1. "At each step, the least significant term that no remaining term contains is removed." and "A main effect therefore stays while an interaction or a square of it remains." (Section 5), against "Table 5.1 gives the effects that the refit keeps for each model." (Section 3)
   Q5, Tables 5.1 and 6.2: five refits keep an interaction or a square without its main effect. Both bioreactor models keep culture pH × culture duration without culture duration. The low-pH fragments refit keeps hold time × temperature and inactivation pH² without temperature or inactivation pH. The cation exchange fragments refit keeps elution buffer pH × elution stop collect without elution buffer pH. The anion exchange XMuLV refit keeps load pH × protein load without protein load. Either the tables leave out main effects the refit kept, in which case the simulation's true model has more terms than the 14 powered in Table 6.2, or the elimination was not hierarchical.

A2. "Their assurance stays at or below 0.005 at every size computed, up to the size of the planned design (Table 6.1)." (Section 4), and "The fragment models of Protein A and cation exchange stay at or below 0.005 at every size." (Section 6.3)
   Q5, Table 6.1: cation exchange fragments shows 0.01 at 28 further runs. Text and table agree only if the estimate is exactly 20 of 4,000 data sets. Print three decimals, or write "at most 0.01".

A3. "R² minus predicted R² is lower on all runs for each of the three." (Section 8.3.1)
   Q5, Table 8.1: anion exchange host cell protein shows 0.02 on both sets of runs. For high mannose, the planned-run value is on the raw scale and the all-runs value on the log scale, so the two cannot be compared.

A4. "This report does not give the results of the new runs." (Summary), with the scope exclusion "The results of the augmentation runs." (Section 2)
   Q5, Tables 8.1 and 9.1 and Section 9.2: the report gives the selected models and R² minus predicted R² on all 44 and all 40 runs. It gives the model of every output of both augmented steps on all runs. It also gives a lower prediction limit of 16.2 % "On the selected model of all runs".

A5. "Two changes in the verification account for the differences." (Section 9.1)
   Q5, Table 9.2: four downstream values differ, at three steps. At anion exchange the host cell protein fold is 4 against 5.18. At cation exchange the host cell protein fold is 40.9 against 41.8 and the aggregate fold 1.44 against 1.52. At low-pH viral inactivation the aggregate increase is 0.538 against 0.535. This last one is a third change, and the text attaches it to the second with "also".

A6. "The step’s augmentation has the largest number of runs any of its models needs." (Table 5.1, footnote a), and "A step’s augmentation has the largest number of runs that any of its models needs, so a model of the same step that needs fewer runs has an assurance above the target at that size." (Section 6.1)
   Q5, Tables 5.1 and 6.1: at anion exchange, XMuLV needs 18 runs and MVM needs 22, but the augmentation is 12. The footnote should say "of the models the rule augments". The "so" also assumes that assurance never falls as runs are added. D-optimal augmentations of different sizes do not guarantee that, and Table 6.1 shows a fall (anion exchange MVM, 0.19 at 0 runs and 0.18 at 4). It happens to hold for acidic variants at 16 runs (0.95).

A7. "The second block sharpened the estimates." and "The augmentations were therefore not needed for adequacy." (Section 8.3.1)
   Q5, Table 8.1: the second block changed two of the three models. High mannose lost 4 of its 6 terms, gained culture pH × culture temperature, and moved from the raw to the log scale. Acidic variants gained 4 terms. A model selected on 28 runs met §7.2 and was still wrong about its terms, so "not needed for adequacy" holds only for the §7.2 statistics. This matters because the verification behind the intermediate acceptance criteria uses models selected on the planned runs only (Section 8.2).

### B. Statistically wrong or unsupported

B1. "Once selected, the three models that the augmentations were made for meet §7.2 on the planned runs alone." (Summary), and "The anion exchange host cell protein model meets §7.2 only once selected, and the bounds at cation exchange move with the model." (Summary)
   Q5: the models were chosen by an exhaustive AICc search over up to 1,337 candidates, plus a Box-Cox choice of scale, on the same runs. Their predicted R² and model F-test are therefore optimistic: PRESS leaves a run out of the fit but not out of the selection. The document never says so, yet the widening of two host cell protein criteria depends on this check. A cross-validation that repeats the selection in each fold would give an honest predicted R².

B2. "Responses are simulated at the planned and the augmentation runs, as the true model plus normal error with the residual standard deviation." (Section 6.1, step 3)
   Q5, Section 8.1 and Table 8.1: the errors are drawn with constant variance on the raw scale, from raw-scale refits. Yet the document later models all three outputs on the log scale (high mannose on all runs, acidic variants and anion exchange host cell protein on both). Section 8.1 also says the spread of host cell protein grows with its level. The run numbers rest on an error model the document itself rejects. Host cell protein shows the cost: the interaction and curvature of the raw refit (power 0.77 and 0.55, Table 6.2) disappear on the log scale (Table 8.1, main effects only).

B3. "It is judged against the lack-of-fit test at α = 0.05 and the limit of 0.20 on R² minus predicted R²." (Section 6.1, step 4)
   Q5, Table 6.1: the true model in the simulation has no lack of fit, so the lack-of-fit test fails 5 % of data sets at any size. That is why every curve that rises stops at 0.95, and it is not explained. A target of 0.90 therefore asks for about 0.95 on the limit on overfitting. The simulation also applies two of the three tests of §7.2 (Section 3), so the note "meets PCMP-001 §7.2" overstates what was simulated.

B4. "Simulated from what the planned runs show, the planned design alone gives the full quadratic model an assurance of meeting §7.2 of 0.25 for high mannose, 0.44 for acidic variants and 0.49 for host cell protein at anion exchange." and "A failure was therefore the more likely outcome for each of these models before any run was made." (Section 4)
   Q5: the probabilities are computed at the fixed coefficients of a refit chosen by backward elimination, which biases the kept coefficients away from zero, from the same runs that failed. They do not describe what was knowable before any run. For host cell protein, 0.49 lies 1.3 Monte Carlo standard errors (0.008 at 4,000 data sets) below 0.5, so "more likely" is not resolved for that model.

B5. "It says that the output does not depend on the parameters within the range studied." (Section 8.1); "Within the ranges studied these outputs do not depend on the parameters, and the model is their mean, with the block term where the design has two blocks." (Section 8.3.3); "For an attribute with no effect, the refit to the mean describes the result fully, and further runs would not change it." (Section 5)
   Q5, Section 6.4: a model with no term shows that no effect was detected, not that none exists. Section 6.4 says so itself: "It is not evidence that the effect is absent". Further runs raise the power to find a small effect. Also, a mean-only model cannot fail the limit on overfitting on 12 or more runs: its R² minus predicted R² is (n/(n − 1))² − 1, which is 0.19 at 12 runs and 0.08 at 28. For these outputs the §7.2 check therefore reduces to the lack-of-fit test.

B6. "The designs span the characterized range, so a response whose measured results all meet the criterion meets it over the NOR." (Section 5)
   Q5, Section 9.2: 12 to 28 scale-down results inside a per-batch criterion do not show that every batch over the NOR will be inside it. Modelled outputs are judged on a 95 % prediction interval for a single batch (Section 9.2, item 2). The three outputs without an adequate model are therefore held to a weaker standard than the others.

B7. "AICc is not defined for an exact fit, so the smallest candidate that fits exactly is selected instead." and "In this campaign the rule applies to acidic variants at low-pH viral inactivation." (Section 8.1)
   Q5, Table 9.1: with zero residual, the model F-test and the lack-of-fit test of step 3 cannot be computed (zero denominators). Yet Table 9.1 lists the model as adequate (raw, 1 term, 18 runs) without saying how §7.2 was applied. A charge-variant assay has non-zero repeatability. Results that lie exactly on a one-term model with no spread between replicates mean the reporting precision is too coarse to resolve the variation. That is a finding about the measurement, not a model.

B8. "The worst prediction is taken at its one-sided 95 % confidence bound." (Section 8.2)
   Q5, Table 9.2: precision differs across the 3^k combinations, so the combination with the worst point prediction need not have the worst bound. A pointwise bound at the most extreme of up to 81 combinations is not a 95 % bound on the worst case. It is also a bound on a mean clearance, carried into a criterion that is judged per batch on a prediction interval (Section 9.2). Every A-Mab value in Table 9.2 comes from this step.

B9. "The same verification on the full quadratic models gives different values for 4 criteria (Section 9.1)." (Summary), with "INV-001 set it, and this investigation does not change it." (Section 2)
   Q5, Table 9.2: in all four criteria the selected models give the wider limit. Production bioreactor aggregates are 7.04 against 6.64, low-pH aggregates 7.58 against 7.18, cation exchange host cell protein 518 against 400, and Protein A host cell protein 21,662 against 16,379, which is +6 %, +6 %, +30 % and +32 %. The analysis was adopted on 2026-09-15, after the failures were known on 2026-08-31. A post-data choice of analysis that widens four criteria is the pattern INV-001 was opened for. The document neither states the direction nor argues why it is acceptable, and "does not change it" is true of the rule but not of the criteria in force.

B10. "The augmentation runs moved no criterion." (Summary, Sections 9.1 and 12)
   Q5 (misleading): this is true by construction, because the verification uses only the planned runs (Section 9.1). The 12 anion exchange runs did measure host cell protein. That fold now widens two criteria from the 28-run model, although a 40-run model exists (Table 8.1).

B11. "They are refitted because viral clearance is not a drug substance test." with "The rule spends runs where they can change a decision about the drug substance." (Section 5)
   Q5, Section 9.2: the XMuLV model at low-pH viral inactivation does change a decision. The step claim is not met on it, and PCR-006 moves three NORs. The stated principle does not cover this case.

B12. "The criterion is the next two characterization plans approved with the design-size check, and every planned model adequate at first analysis." (Section 11)
   Q5: if PA1 sizes each model for 0.90, the chance that every model of two plans passes is about 0.9^m. That is 0.43 for 8 models and 0.10 for this campaign's 22. Even a design of any size fails the lack-of-fit test for 5 % of correct models (item B3). The check will usually fail when the action works. Test the share of adequate models against the planned assurance instead.

B13. "Preventive action PA1 checks each new characterization plan before approval, by simulation at the effects the plan expects, for an assurance of at least 0.90 that its planned models meet the model-adequacy criteria." (Section 10)
   Q5: PA1 "uses the simulation of Section 6", which fits the full quadratic. After corrective action CA3 and PA2, plans are analysed by model selection, so PA1 would size the design for a model nobody fits. Sections 4 and 6.3 also show that a full quadratic of an output with no effect, or a small one, cannot reach 0.90 at any size computed. No plan with such an output could pass PA1.

### C. Minor

C1. "Further runs let the full model estimate every term." (Section 5)
   Q5: the planned designs already estimate every term (28 runs for 15 terms, 18 for 10, 12 for 6). Further runs make the estimates more precise.

C2. "It has no point at which exactly one factor sits at its centre level." (Section 6.2)
   Q5: true for the three- and four-factor designs. It is false for the two-factor virus filtration design, whose four axial points each have exactly one factor at its centre. Also, "These points separate the squared terms from each other." is strong: in the 44-run bioreactor design (Table 7.1 plus the planned runs) the largest correlation between squared terms is still 0.54, against 0.69 in the planned design. "Reduce the correlation between" is accurate.

C3. "Otherwise it is modelled on the raw scale (λ = 1)." (Section 8.1)
   Q5: if the interval excludes both 0 and 1, the rule chooses the raw scale that the profile rejects. So "the scale that its Box-Cox profile supports" (Summary) and "the scale chosen by the Box-Cox profile" (Table 8.1 note) describe a two-way rule too generously.

C4. "Model selection keeps a term in filtration pressure, because that model has the lower AICc (−7.8 against −6.8 for the mean alone)." (Section 8.3.2)
   Q5 (method): the numbers agree with each other. A difference of 1.0 on 12 runs implies R² of about 0.32 and an F-test p of about 0.054, against the printed 0.053. But by the cited Burnham and Anderson (2002), models within 2 AICc units have about equal support. The rule turns a 1-unit difference into "no adequate model" where the mean model meets §7.2, and that fragility should be stated.

C5. "PCMP-001 §7.2 judges a response-surface model by three tests (Montgomery 2017)." and "R² minus predicted R² may not exceed 0.20." (Section 3)
   Q5 (attribution): as usually cited (Design-Expert output reproduced in Montgomery), the 0.2 rule of thumb compares predicted R² with adjusted R², not with R². On that basis high mannose (0.16) and anion exchange host cell protein (0.195) would pass (Table 3.1). If the plan uses R² on purpose, say that it is stricter than the textbook rule.

C6. "A real difference between the blocks is taken up by the block term of the fitted model." (Section 6.1)
   Q5: only a constant shift is taken up. A change in factor effects between blocks run four months apart is not, and the second block has no replicated point to show it.

C7. "Each report records them as discrepancies from its plan, not as deviations, because no procedure and no GMP requirement was departed from." (Section 9)
   Q5 (GMP practice): the reports depart from the analysis the approved plans prescribe, which Section 4 names as the root cause. The claim that "no procedure and no GMP requirement was departed from" rests on an unstated distinction between an approved plan and a procedure. A departure from an approved protocol is normally recorded as a protocol deviation or covered by an amendment.

C8. "PCMP-001 Version 2.0 §7.2 refers to this investigation for when a design is augmented and how the number of runs is calculated." (Section 9.3), with "§7.2 leaves it to this investigation to state when a design is augmented and how the number of runs is calculated." (Section 5)
   Q5 (chronology): §7.2 was in force before INV-002 was opened, since applying it triggered INV-002 on 2026-08-31, and "PCMP-001 and the plans are not amended". So §7.2 can refer to INV-002 only in general terms. Say "to the investigation of the failure".

C9. "A model that fails the lack-of-fit test or the limit on overfitting is refitted with a justified change of terms or transformation, or it is not used to set a range." (Section 3)
   Q5: Section 5 lists the remedies §7.2 allows differently (a refit with a change of terms, or augmentation). Neither section says what happens to a model that fails the model F-test, and five models in Table 3.1 also fail it (p = 0.365, 0.280, 0.936, 0.398 and 0.811).

C10. "A failing model of an attribute of the drug substance specification, on which the refit of the planned runs keeps an effect, is resolved by further runs (corrective action CA1)." (Summary)
   Q5, Table 5.1: fragments at Protein A, at low-pH viral inactivation and at cation exchange fit this description. They were refitted, because the target was not reached within the planned size (rule 3). The Summary omits this exception.

C11. "Predicted R² therefore falls well below R², even where the lack-of-fit test shows no systematic error." (Section 4)
   Q5: with 3 pure-error degrees of freedom (4 centre points), a non-significant lack-of-fit test does not show the absence of systematic error. The wording of Section 3, "gives no sign of", is the accurate one.

Checked and consistent, not flagged: the totals of Table 2.1 (22 models, 14 failing); every R² minus predicted R² in Table 3.1 (within 0.01 rounding); the model F-test p-values of Table 3.1, recomputed from R², terms and runs; the term counts and the average leverage of 0.50 to 0.56; the candidate counts 13, 95 and 1,337 under strong hierarchy; the 3 + 5 + 3 split of the 11 refitted models; Table 6.2 (14 effects, 9 with a power of at least 0.90); the runs needed and assurances quoted in Section 6.3; every coded and actual setting in Tables 7.1 and 7.2, and the counts of edge and corner points (11 and 5, 10 and 2); the 7 log-scale outputs and the 3 outputs without a term (Table 9.1); and the arithmetic of Table 9.2 within rounding (for example 7.18 − 0.538 = 6.64, and 400 × 40.95 = 16,379).

## Question 6: sentences that read as machine-written

1. "The model fails because it fits the runs it was estimated from much better than it predicts a run left out of the fit." (Section 3)
   Q6: restates the test defined a few sentences earlier.

2. "The rule below puts this into effect." (Section 5)
   Q6: says nothing a reader would miss.

3. "The rule spends runs where they can change a decision about the drug substance." (Section 5)
   Q6: restates "The decision was to calculate the further runs needed to resolve the effects where a model bears on the drug substance specification", earlier in the same section.

4. "No model draws a boundary for such a response." (Section 5)
   Q6: restates rule 5 ("No model sets a range for it.") and the sentence before it.

5. "The rule refits these viral clearance models all the same." (Section 6.3)
   Q6: restates Section 5.

6. "A term with a power of 0.55 is not significant in about 45 % of simulated data sets." (Section 6.4)
   Q6: restates the definition of power for a reader who already knows it.

7. "The second block sharpened the estimates." (Section 8.3.1)
   Q6: vague emphasis that a reader would not miss (see also Question 3 and Question 5, item A7).

8. "The reports of the two steps give the results of the new runs and the models of their other outputs." (Section 8.3.1)
   Q6: the third statement of the same pointer (Summary, Section 2).

9. "Table 10.1 lists the corrective and preventive actions, which are managed in the quality system (International Council for Harmonisation 2008)." (Section 10)
   Q6: the relative clause and its citation add nothing.

10. "Corrective action CA1 is the augmentation of the designs that the rule names, with the number of runs this investigation calculated, and the re-evaluation of their models on all runs with a block term." (Section 10)
    Q6: restates the Action column of Table 10.1 nearly word for word, as do the CA2, CA3, PA1 and PA2 sentences of the same paragraph.

11. "The corrective actions are owned by MSAT and were due on 2026-09-30.", "Preventive action PA1 is owned by Statistics and preventive action PA2 by Quality Assurance." and "Both are due on 2026-12-31." (Section 10)
    Q6: restate the Owner and Due columns of Table 10.1.

## Question 7: sentences that cannot be read on their own

Criterion code without the criterion (the pattern runs through the whole document):

1. "Each output is modelled on the scale that its Box-Cox profile supports, by the submodel of the full quadratic with the lowest AICc, and that model is judged against §7.2." (Summary)
   Q7: "§7.2" alone. Name "the model-adequacy criteria of the master plan (PCMP-001 §7.2)". The same applies to most of the 60 or so uses of "§7.2".
2. "The 8 models that meet §7.2 on the planned runs need no remedy (Table 2.1)." (Section 3)
   Q7: as above.
3. "The augmentations are sized for §7.2, not for the power of each effect." (Section 6.4)
   Q7: as above.
4. "A plan approved without the design-size check, or a planned model that fails §7.2 at its first analysis, fails the check." (Section 11)
   Q7: as above. "the design-size check" should also be named (see item 22).

Document codes the document never names:

5. "PCMP-001 Version 2.0 also states campaign thresholds for model adequacy in §7.2." (Section 1)
   Q7: PCMP-001 is never named. Write "the process characterization master plan (PCMP-001)".
6. "INV-001 was opened on 2026-08-03, after the QA review of PCMR-001 Version 1.0 for BLA readiness found that the acceptance criteria of the proven acceptable range analysis had been set after the data were seen." (Section 1)
   Q7: PCMR-001 is never named. Write "the master characterization report (PCMR-001)".
7. "PCR-003 states how this result is handled." (Section 9.2)
   Q7: name "the production bioreactor characterization report (PCR-003)".
8. "PCR-006 moves the NOR of inactivation pH, hold time and temperature, and it states the conclusion over the NOR in force." (Section 9.2)
   Q7: name the report. "the NOR in force" also needs a definition.
9. "INV-001 is not reopened." (Section 9.3)
   Q7: name it as the investigation into acceptance criteria set after the data were seen.
10. "PCMR-001 consolidates the conclusions of the step reports after the remedies and the model selection." (Section 9.3)
    Q7: as item 6.
11. "Preventive action PA2 revises SOP-1002 so that a characterization plan states its model-selection procedure." (Section 10)
    Q7: say what SOP-1002 governs.
12. "PCR-003 records the production bioreactor augmentation as PD-003-01, and PCR-008 records the anion exchange augmentation as PD-008-01." (Section 9)
    Q7: "PD" is never expanded (plan discrepancy), and the reports are not named.

Corrective-action codes without the action:

13. "The Version 2.0 reports of the steps carry the re-evaluation of corrective action CA1 and the models of corrective action CA3." (Section 10)
    Q7: name "the re-evaluation of the augmented designs on all runs" and "the models chosen by model selection".
14. "At closure the augmentation runs of corrective action CA1 were complete, and corrective actions CA2 and CA3 were complete." (Section 12)
    Q7: name "the refits by backward elimination" and "the model selection".
15. "Model selection (corrective action CA3) later replaced this analysis for every output, the outputs that CA2 had refitted included (Section 8)." (Section 5)
    Q7: "this analysis" and "CA2" both stand for the refit by hierarchical backward elimination. Name it.
16. "Preventive action PA1 is owned by Statistics and preventive action PA2 by Quality Assurance." (Section 10)
    Q7: name the two actions.

Abstract stand-ins:

17. "The same verification on the full quadratic models gives different values for 4 criteria (Section 9.1)." (Summary)
    Q7: no verification has been named before this sentence. Name "the verification of the platform worst cases behind the intermediate acceptance criteria".
18. "Two changes in the verification account for the differences." (Section 9.1)
    Q7: name the changes in the sentence.
19. "The rule of Section 5 and the augmentations it gave had been decided before that date, under the model of the plan." (Section 4)
    Q7: name "the remedy rule" and "the full quadratic model".
20. "The simulation of Section 6 quantifies this for the models that the rule augments." (Section 4)
    Q7: "this" stands for the gap between R² and predicted R² at these leverages.
21. "The three models that the rule augments reach the target within the size of their planned design." (Section 6.3)
    Q7: name "an assurance of 0.90".
22. "The criterion is the next two characterization plans approved with the design-size check, and every planned model adequate at first analysis." (Section 11)
    Q7: name the check (the simulation of design size in preventive action PA1).
23. "Section 9.1 gives what this changed." (Section 8.2)
    Q7: "this" stands for the replacement of platform values by bounds from the selected models.
24. "The second block sharpened the estimates." (Section 8.3.1)
    Q7: say what changed (terms dropped and added, the scale, R² minus predicted R²).

---

## Table observations

**Title block.** The title, "Investigation Report: A-Mab Drug Substance", does not name the subject (response-surface models below the model-adequacy criteria). A reader cannot tell this investigation from INV-001 by its title.

**Abbreviations.** "SOP", "PD" (plan discrepancy), "CA" and "PA" are used but not listed. Neither are the study codes S-BRX-AUG and S-AEX-AUG.

**Table 1.1 (chronology).** The 2026-09-24 row holds two events, with the date centred between them. In the text, "Production bioreactor augmentation ended (S-BRX-AUG)" sits directly under the 2026-09-18 row, so a reader can date the end of the bioreactor runs to 2026-09-18. Use one row per event or align the date to the top. The table leaves out the date PCMP-001 Version 2.0 took effect, and the end of the last planned response-surface study (2026-05-15, Section 4). Both matter to the chronology of §7.2.

**Table 2.1.** The two narrow headers "Planned runs" and "Model terms" are stacked so that they read "Planned Model / runs terms". The "Attributes with a criterion" column does not mark which attributes are counted under "Below §7.2", so Table 3.1 is needed to tell.

**Table 3.1.** The header runs over four lines. "R²", "Predicted R²" and "R² minus predicted R²" interleave ("Predicted / R² / R² predicted R²"), which makes the three R² columns hard to tell apart. The step labels are centred inside wrapped attribute cells, so "Protein A" lands between "Leached Protein A" and "(ppm)", and "Anion exchange" splits around "Host cell protein (ng/mg)". The footnote states only two of the three §7.2 tests. It omits the model F-test, although the table prints the model p-value and five models fail it (0.365, 0.280, 0.936, 0.398, 0.811); mark those. Three printed differences are 0.01 below the difference of the printed columns (0.29, 0.50, 2.14 against 0.30, 0.51, 2.15). This is rounding, but a footnote "computed before rounding" would stop the question.

**Table 5.1.** The sub-header "(planned runs)" of "Effects in the refit" sits under "Runs needed", so the header reads "Runs needed (planned runs)". Footnote a) is contradicted by the anion exchange rows (18 and 22 runs needed, 12 run). "Effects in the refit" leaves out main effects that a hierarchical refit must keep, or the refits are not hierarchical (Question 5, item A1). The values 18, 22 and 8 in "Refit" rows can be read as runs that were made. "Filtration volume (load)" is not the usual term; volumetric throughput or loading (L/m²) is. In the extract, the page number "16" falls inside the table body; check the landscape page.

**Table 6.1.** The footnote defines "–" only for "Runs needed". In the assurance columns, "–" means a size beyond the planned design (low-pH viral inactivation beyond 18 runs, virus filtration beyond 12), and that is not stated. The text quotes values at 18 runs (0.75 and 0.74) that the table does not show, because it shows every fourth size. Cation exchange fragments shows 0.01 at 28, against "at or below 0.005" in the text. Low-pH fragments is flat at 0.45 at 12 and 16 runs and then, by the text, 0.74 at 18. A jump of 0.29 in two runs is worth checking against Figure 6.1. The note calls the model "full quadratic with a block term" for the 0 column too, where there is no second block. The ceiling of 0.95 (Question 5, item B3) deserves a line in the note. Units "(%)" and "(log10)" wrap onto their own lines, and "Anion exchange" splits around the host cell protein row.

**Table 6.2.** If the refits are hierarchical, the table leaves out culture duration, which the refit keeps in both bioreactor models (Question 5, item A1). The note refers to "the sample-size table" rather than Table 6.1.

**Table 7.1.** Every row matches its coded levels, and the counts are 11 edge and 5 corner points. The pH settings mix precision (6.6, 6.85, 7.1); use 6.60, 6.85, 7.10. "A (pH)" uses pH as if it were a unit.

**Table 7.2.** Every row matches its coded levels, and the counts are 10 edge and 2 corner points. B and C are both headed "(mS/cm)", so without the footnote the reader cannot tell equilibration and Wash-1 conductivity from load conductivity. Put the factor names in the header. The C settings mix precision (3, 5.5, 8).

**Table 8.1.** "Runs" values wrap ("Planned," on one line and "28" on the next, beside the terms). Long term lists break inside a term ("culture pH / × culture temperature"). Anion exchange host cell protein shows 0.02 on both sets of runs, against "R² minus predicted R² is lower on all runs for each of the three". The high mannose values compare a raw-scale and a log-scale statistic. The table reports only the overfitting statistic, although the text says these models "meet §7.2"; add the lack-of-fit and model F-test p-values. The note "the scale chosen by the Box-Cox profile" overstates a two-way rule.

**Table 9.1.** The merged "Discrepancies from the plan" cells wrap so that codes and descriptions split ("PD-003-01, / augmentation", "PD-003-02, model / selection"), and in the text flow they interleave with the attribute rows. The low-pH acidic variants row (raw, 1 term, 18 runs) is the exact-fit case of Section 8.1, and nothing marks it. Rows reading "No adequate model" give no run count. The other rows do.

**Table 9.2.** The header runs over five lines. Under "Upper limit" and "Value in the derivation", the sub-headers wrap ("Full / quadratic", "Selected / models"), and "A priori" and "Platform" sit on a line of their own between them, so the sub-headers run together. The criterion values sit between the two downstream rows they depend on. Platform and A-Mab values mix precision (0.7 against 0.538, 2 against 1.44, 4 against 5.18). The drug substance limits behind the "A priori" column are not given. The table shows changes at three steps where the text says "Two changes in the verification account for the differences". The note's phrase "where it replaces it" has two unclear pronouns. The values reproduce from the printed factors within rounding (518 × 41.8 = 21,652 against 21,662 printed).

**Table 10.1.** The CA1 status, "runs complete at closure", reports only part of the action. The re-evaluation of the models on all runs is given no status, although Section 8.3.1 and Table 8.1 show it was done. The value "complete at closure" repeats the column header "Status at closure".

**Figure 6.1.** Only the caption is in the text. It agrees with Table 6.1 (one line per failing model with an effect, 10 lines). It cannot confirm the jump of the low-pH fragments curve between 16 and 18 runs.
