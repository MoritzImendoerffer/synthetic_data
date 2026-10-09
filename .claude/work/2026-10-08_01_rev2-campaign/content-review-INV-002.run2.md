# Content review of INV-002 (run 2 draft)

**Reviewer:** Claude Opus 5.5 (model ID `claude-opus-5-5`), 2026-10-09.

**Document:** INV-002, "Response-surface models below the model-adequacy criteria". This is the Version 1.0 draft, reviewed from the text of the 47-page PDF (`INV-002_model_adequacy.DRAFT.run2.txt`). I read nothing else in the repository.

**Method:** I read every sentence of the body and every table against the seven questions. I recomputed the arithmetic and statistics in Python, using only values printed in the document and the design structure it states. That structure is face-centred designs with 4, 3 and 2 factors on 28, 18 and 12 runs; those run counts imply four centre points per design. Quotes are exact. I rejoined words split at a line end and dropped the page numbers.

---

## Answers

| Q | Question (short form) | Answer |
|---|---|---|
| 1 | Does each cause name a physical cause in the clause where the verb stands? | **No** |
| 2 | Is every technical term a term of art? | **No** |
| 3 | Does any sentence tell the reader how to file its own finding? | **Yes** (11 sentences) |
| 4 | Is every criterion given with its basis, every result reported as met or not met, and every rule applicable by a second analyst? | **No** |
| 5 | Is any statement wrong, or contradicted by a table? | **Yes** |
| 6 | Is no sentence machine-like? ("yes" = nothing flagged) | **No** (16 flagged) |
| 7 | Can every sentence be understood on its own? ("yes" = nothing flagged) | **No** (67 flagged, 34 of them for §7.2 used alone) |

## The three most consequential problems, in order

1. **The adequacy verdicts that close the investigation are asserted, not shown, and one of them is impossible.**
   - The three statistics of PCMP-001 §7.2 are printed for only 3 of the 19 selected models called adequate (Table 8.1), and for none of the 8 full quadratic models said to pass. Table 2.1 has no statistics.
   - The augmentations were sized so that the full quadratic model with a block term would meet the criteria on all runs, with an assurance of 0.90. Whether it did is never reported.
   - Acidic variants at low-pH viral inactivation is counted as meeting the criteria (Table 2.1, and the 19 of 22 in Section 8.5), but it fits exactly:
     - There is no pure error, so the lack-of-fit test cannot be run.
     - The residual mean square is zero, so the model F-test is undefined.
     - The Box-Cox interval that Section 8.1 reports for this output cannot exist. Hold time has three levels, so the full quadratic fits any function of hold time exactly, at every λ. Recomputed on an 18-run face-centred design: the residual sum of squares stays below 1e-26 for λ from −1 to 2.

2. **A criterion in force, and the risk case for the wider criteria, rest on steps the document does not show.**
   - The production bioreactor aggregate criterion (6.46 %) comes from the low-pH aggregate increase bound (0.559 %). That bound is taken over the NOR as characterized, which allows a hold of at most 120 min.
   - Section 9.2 says PCR-006 moves the low-pH NOR (pH, hold time and temperature) to recover the XMuLV claim. The text still asserts "The criterion that follows is still right, because routine manufacture never holds longer than the NOR", for a NOR that has since moved and is not given.
   - The risk conclusion relies on "a normal-tail probability of less than one per million". No failure in 2,000 simulated batches only bounds the rate below 0.15 % (one-sided 95 %).
   - A normal tail for host cell protein also contradicts the document's own case, in Section 8.2, that its error is multiplicative.

3. **The effectiveness check cannot detect the failure this investigation found.**
   - It counts planned models that fail the model-adequacy tests. Section 8.1 itself calls that check optimistic for a selected model.
   - Table 8.2 shows that selected models which pass can still miss new runs:
     - High mannose: 13 of 16 new runs inside the 95 % interval. The chance of so few under a correct model is 0.043.
     - Aggregates: 11 of 16 inside. The chance under a correct model is 0.0009.
   - The "upper 95 % limit" of the check is not defined.
   - Nothing checks CA1 to CA3 themselves, or PA2.

---

## Question 1. Causes

Most causal clauses in this report give a statistical or procedural reason, for example the block term, the hierarchy rule or the lack-of-fit false-rejection rate. Those are judged under questions 4 and 5. Four sentences give a physical cause, and none of them names it in the clause where the verb stands.

| Sentence | Fails | Why |
|---|---|---|
| "Two properties of the process and the method make host cell protein behave this way." | Q1 | The verb "make … behave" has no cause in its clause. The two properties only appear in the next two sentences. |
| "A purification step removes a share of what is present, so a parameter changes the share that is removed, not a fixed amount." | Q1 | Too generic. It names no species or interaction (for example host cell protein bound to the antibody or the resin and released by the elution buffer), and gives no direction. It explains why the effects multiply. It does not explain why protein load multiplies pool HCP by 2.43 while a higher elution buffer pH multiplies it by 0.30. |
| "Where the A-Mab increase replaces the platform value, the replacement reflects the shorter hold, not a more stable product." | Q1 | It names a duration, not the physical cause, which is that the antibody aggregates at low pH and the aggregate grows with time at that pH. It also rules out the other physical cause, a more stable molecule, with no A-Mab data at 180 min. |
| "This replacement reflects the shorter hold of the NOR as characterized, at most 120 min against the 180-min hold of the platform worst case, not a more stable product." | Q1 | Same as the row above. |

## Question 2. Terms of art

| Sentence | Fails | Why |
|---|---|---|
| "The assurance is the probability, at the effects estimated from the planned runs, that the planned model, the full quadratic with a block term, meets §7.2 on all runs (Section 6)." | Q2 | "Assurance" is a term of art (O'Hagan and Stevens): power averaged over the uncertainty of the effect. "The assurance does not include the uncertainty of those estimates" excludes exactly that. What is computed is power, or probability of success, at the estimated effects. |
| "The simulation estimates the assurance, the probability, at the effects estimated from the planned runs, that the planned model meets §7.2 once the design has been augmented by a given number of runs." | Q2 | Same misuse of "assurance". |
| "Of the 22 full quadratic models in scope, 14 did not meet the limit on overfitting, which allows predicted R² to fall short of R² by at most 0.20." | Q2 | The phrase "limit on overfitting" is the document's own name for a cap on R² minus predicted R². Section 4 shows that this statistic tracks 1 − R², so the name claims more than the test measures. |
| "A conclusion over the NOR is the judgement whether an output meets its criterion everywhere within the NOR, at every combination of NOR low, set-point and NOR high of the response-surface factors." | Q2 | Coined term. About 20 later sentences use it and cannot be read without Section 2. |
| "The NOR as characterized is the NOR against which the studies were planned and run." | Q2 | Coined label, with the same problem. |
| "The NOR in force is the NOR that a Version 2.0 report sets, where it moved one." | Q2 | Coined label, with the same problem. |
| "Both directions use the single-batch bound, never a confidence bound of the mean, because every output is judged per batch and the platform worst case that the bound replaces was a single run." | Q2 | The term "single-batch bound" is coined shorthand. The term of art is the one-sided 95 % prediction bound for one future batch. |
| "A bound from a tolerance interval would be statistically purer, but it is too conservative, and the single-batch prediction bound was chosen as the pragmatic rule." | Q2 | The phrases "statistically purer" and "pragmatic rule" are not statistical terms and say nothing measurable. |
| "The target of 0.90 is the probability of success customary for a confirmatory study, 0.80 to 0.90, taken at its upper end because a further failure would leave a criterion attribute without an adequate model." | Q2 | The term "criterion attribute" is coined. The customary 0.80 to 0.90 is the convention for power, which supports the point made on "assurance" above. |
| "Preventive action PA1, the design-size check, checks each new design by simulation before its plan is approved, at the expected effects and with the analysis the plan states." | Q2 | The term "design-size check" is coined. The term of art is a sample-size or power calculation. |
| "An output that the data give without error, with replicates that agree exactly at the precision the method reports, is fitted exactly by more than one candidate." | Q2 | The phrase "that the data give without error" is not a statistical expression, and it misdescribes the case (see Q5). |
| "The full quadratic model of host cell protein does not meet §7.2, so its bound of 4.28 cannot widen a criterion, and the platform worst-case clearance fold of 4 enters the derivation." | Q2 (minor) | The term "clearance fold" is unusual. The literature says clearance factor, fold clearance or log reduction value. |

## Question 3. Sentences that file their own finding

| Sentence | Fails | Why |
|---|---|---|
| "They describe the planned design under those effects, not what could have been known before any run." | Q3 | Answers a hindsight objection that nobody raised. |
| "The verification replaces a platform worst case by the one-sided 95 % prediction bound of a single batch, never by a confidence bound of the mean." | Q3 | "never by a confidence bound of the mean" rebuts an unraised alternative, in the Summary, before any reason is given. |
| "A bound from a tolerance interval would be statistically purer, but it is too conservative, and the single-batch prediction bound was chosen as the pragmatic rule." | Q3 | Answers an objection nobody raised, and files the choice as "pragmatic" instead of giving the numbers. |
| "A replacement does not always mean that the product did better." | Q3 | Pre-empts a misreading that nobody proposed. |
| "The criterion that follows is still right, because routine manufacture never holds longer than the NOR." | Q3 | Files the criterion as "still right" against an unraised objection. The claim is also unsupported (Q5). |
| "This replacement reflects the shorter hold of the NOR as characterized, at most 120 min against the 180-min hold of the platform worst case, not a more stable product." | Q3 | "not a more stable product" answers an objection nobody raised. |
| "The log scale changes the following, and nothing else:" | Q3 | "and nothing else" rebuts an unraised worry. |
| "It is therefore suitable, and the least-squares assumption behind it holds on the log scale, which on the raw scale it does not." | Q3 | A trailing gloss that files the interval as "suitable". |
| "Each is judged on its measured results, which is a weaker standard than the prediction interval of a single future batch that a modelled output meets (Section 5)." | Q3 | The trailing clause renames the approach as a category ("a weaker standard"), repeating Section 5. |
| "The refits remain the record of how the rule was applied, and the sample-size calculation rests on them." | Q3 | Files the refits as "the record". |
| "Model selection, corrective action CA3, replaced the refits by backward elimination of corrective action CA2 in the reports, so CA2 stands as the record of how the rule was applied." | Q3 | The trailing clause files CA2 as "the record". |

## Question 4. Criteria, results against criteria, and rules a second analyst can apply

| Sentence | Fails | Why |
|---|---|---|
| "PCMP-001 §7.2 limits R² minus predicted R² to at most 0.20." | Q4 | No basis is given for the limit. The common rule of thumb compares adjusted R², not R², with predicted R² (difference under about 0.2). Under that rule, high mannose passes (adjusted R² 0.813; gap 0.26 − 0.09 × 14/13 = 0.16), and host cell protein at anion exchange sits at the limit (0.27 − 0.07 × 14/13 = 0.19). The choice of rule therefore decides whether two of the three augmentations were triggered. It also decides whether the designs are "small": a 28-run face-centred design is the textbook design for a four-factor quadratic. |
| "Model selection gives an adequate model for 19 of the 22 outputs with a criterion." | Q4 | The verdicts are not shown against the criteria. Table 8.1 gives the statistics for 3 of the 19. The other 16, including the 11 that failed as full quadratics, are only asserted. |
| "Every full quadratic model that met the limit has an R² of at least 0.96, and every model that failed it has an R² of at most 0.95." | Q4 | The first half cannot be checked, because no table gives the 8 passing models. |
| "The 8 models that meet §7.2 on the planned runs need no remedy (Table 2.1)." | Q4 | Table 2.1 holds no statistics. A pass is claimed but not shown. |
| "Each augmentation is the smallest D-optimal set of runs that gives an assurance of at least 0.90." | Q4 | The outcome that the augmentations were sized for is never reported as met or not met for the three models: the full quadratic with a block term meeting the criteria on all runs. |
| "The smallest model that fits exactly is taken, with hold time as its only term." | Q4 | No rule says how an exact fit is judged against the three tests. There is no lack-of-fit test without pure error, and F is undefined with a zero residual mean square. Nor does any rule say how a conclusion over the NOR is reached with a prediction interval of zero width. |
| "High mannose and aggregates at the production bioreactor predict the new runs worst." | Q4 | No criterion set beforehand. Under a correct model with independent intervals, P(at most 13 of 16 inside) = 0.043 and P(at most 11 of 16 inside) = 0.0009. Afucosylation (14 of 16) gives 0.19. A stated rule would settle which models fail. |
| "They changed what two models of the production bioreactor say, those of high mannose and aggregates, whose models selected on the planned runs predict the new runs poorly." | Q4 | The word "poorly" is used without a stated criterion. |
| "In the Protein A pool, with the offset at the low end of its interval, a ratio of 0.89, the upper 95 % prediction limit over the NOR at manufacturing scale is 16,763 ng/mg." | Q4 | It does not say whether the limit is one-sided or two-sided. The arithmetic matches the upper end of the two-sided interval: 15,349 × 0.97 / 0.89 = 16,729, equal to 16,763 within the rounding of the printed ratios (a ratio of 1.092 is needed; rounding allows 1.078 to 1.102). The criteria are derived with a one-sided 95 % bound, which gives about 14,755 × 0.97 / 0.89 = 16,081 at this point. |
| "Every measured result of the designs is compared with the criterion at manufacturing scale." | Q4 | Two things are left open. First, which designs: Table 8.3 counts 19 results for a 12-run design. Second, the scale for the offset of an output with no adequate model: Section 8.1 step 4 takes the offset "on the scale of its model", and these outputs have no model. |
| "The criterion is the design-size check documented for every planned model of the next two characterization plans before approval, and at their first analysis no more planned models failing the model-adequacy criteria than the check predicts at its upper 95 % limit." | Q4 | Four gaps. The method for the upper 95 % limit is not stated (for example a Poisson-binomial distribution over the per-model probabilities, assuming independence). It counts a check that Section 8.1 calls optimistic for selected models. Nothing covers CA1 to CA3 or PA2. Nothing says what happens if no plan is written by 2027-06-30. |
| "The integrated process model gives no out-of-specification drug substance for either attribute in its 2,000 simulated batches, and a normal-tail probability of less than one per million." | Q4 | No acceptance criterion is given for the risk. Nothing describes the model, which criteria it simulated, or how the normal tail was fitted. |
| "The production bioreactor report (PCR-003) states how this result is handled." | Q4 | A criterion that is not met (lower prediction limit 16.2 % against 18 %) is left with no stated action in the impact assessment. |
| "The claims of the three viral clearance steps add up to 16.72 log10, against a cumulative requirement of 16.7 log10." | Q4 | No basis is given for the 16.7 log10 requirement. |
| "At closure the augmentation runs of corrective action CA1 were complete, and the refits of corrective action CA2 and the model selection of corrective action CA3 were complete." | Q4 | The second part of CA1 (re-evaluation on all runs, due 2026-09-30) is not reported. The investigation closed on 2026-09-28 with it open, and the closure section is silent about it. |
| "The output is modelled on the log scale (λ = 0) where the 95 % profile-likelihood interval of λ contains 0 and excludes 1." | Q4 (minor) | A second analyst can apply the rule, but its basis is not given: why 1 must be excluded, and why only λ = 0 or 1 is allowed. It also keeps the raw scale where the data reject it (Q5). |

## Question 5. Statements that are wrong or contradicted by a table

Most serious first. Each entry gives the conflicting table or section and the arithmetic.

1. **"Where the interval excludes both 0 and 1, as for afucosylation at the production bioreactor and acidic variants at low-pH viral inactivation, the raw scale is kept."**
   - **Wrong for acidic variants.** Section 8.5.3 and the note a) to Table 9.1 say that a model with hold time as its only term reproduces every run.
     - In a face-centred design hold time has three levels. The full quadratic, which contains hold time and hold time², therefore reproduces any function of hold time exactly, on any power scale.
     - So the residual sum of squares is zero for every λ. The profile log-likelihood −(n/2) ln(SSE/n) + (λ − 1) Σ ln y is then unbounded, and no interval exists.
     - Recomputed on an 18-run face-centred design with y linear in one factor: SSE stays between 1e-31 and 1e-26 for λ from −1 to 2, which is rounding noise.
   - **Also wrong for afucosylation, on the planned runs.** Table 8.2 shows its planned-run model on the log scale ("Log → raw"), so the sentence holds only for all runs.

2. **"Model selection gives an adequate model for 19 of the 22 outputs with a criterion."**
   - This conflicts with Section 8.5.3: "There is therefore no pure error to test lack of fit against".
   - Table 2.1 also counts acidic variants at low-pH viral inactivation among the models that meet §7.2.
   - In fact one of the three tests cannot be run for this output, and the F-test has a zero residual mean square.

3. **"An output that the data give without error, with replicates that agree exactly at the precision the method reports, is fitted exactly by more than one candidate."**
   - Agreement at reporting precision is not absence of error. The error is smaller than the reporting step; rounding alone contributes an SD of the step divided by √12.
   - A model with zero residual SD gives a prediction interval of zero width, which cannot be a 95 % interval for a future batch.

4. **"The criterion that follows is still right, because routine manufacture never holds longer than the NOR."**
   - This is not shown, and it is undermined by Section 9.2. The 0.559 % aggregate increase, which sets the production bioreactor aggregate criterion at 7.02 − 0.559 = 6.46 %, is a bound over the NOR as characterized (at most 120 min).
   - Section 9.2 says "The low-pH viral inactivation report (PCR-006) moves the NOR of inactivation pH, hold time and temperature". The aim is to lift the lowest LRF of 6.16, which sits at pH 3.6, 60 min and 19 °C.
   - Lower pH, a longer hold or higher temperature all tend to raise aggregates. The document does not show that the bound still covers the NOR in force.
   - Table 9.3 judges conclusions "at the NOR in force", while the criteria derive from the NOR as characterized.

5. **"The integrated process model gives no out-of-specification drug substance for either attribute in its 2,000 simulated batches, and a normal-tail probability of less than one per million."**
   - Zero events in 2,000 bound the rate at 1 − 0.05^(1/2000) = 0.0015 (one-sided 95 %; rule of three: 3/2000).
   - The figure "less than one per million" is 1,500 times smaller. It needs a normal tail about 4.75 SD out, far beyond the data.
   - For host cell protein, Section 8.2 argues that the error is multiplicative, and under that a normal tail on ng/mg understates the upper tail.

6. **"The block term is not significant for any output on all runs (the smallest p-value is 0.091), so the misses come from the models, not from a shift between the blocks."**
   - This contradicts the document's own principle in Section 6.4: "It is not evidence that the effect is absent."
   - It also contradicts Section 6.1, which says a change in the effects between blocks is not taken up by the block term. The block term tests only a constant shift.
   - The augmentation began on 2026-09-03, at least 3.5 months after the last planned study ended on 2026-05-15 (Table 1.1). A change between campaigns is therefore a live alternative.
   - A p-value of 0.091, for fragments at anion exchange, is not far from 0.05.

7. **"A change in the effects between the blocks is not, and no augmentation repeats a point that could show it."**
   - Contradicted by Section 7.1 ("The corner runs repeat settings that the planned factorial runs also used") and by Tables 7.1 and 7.2.
   - Runs 29, 33, 35, 41 and 44 repeat planned corners, and every factor sits at both its levels among them. A change in an effect between blocks would show as unequal block-to-block differences across these five pairs.
   - Anion exchange runs 33 and 36 repeat planned corners in the same way.

8. **Table 8.3 conflicts with Tables 2.1 and 9.1.**
   - The row "Virus filtration XMuLV clearance ≥ 4.62 19 5.90 1.28" counts 19 measured results.
   - The virus filtration design has 12 runs (Tables 2.1 and 9.1), and it was not augmented.
   - The other two rows (18 and 28) equal the response-surface runs, so "the designs of the step" is counted in two different ways.

9. **Table 8.3 note, "Every measured result of the designs of the step, at manufacturing scale."**
   - The note covers an XMuLV LRF. Viral clearance is only measured at small scale, so there is no manufacturing-scale LRF and no offset can be estimated. The phrase "at manufacturing scale" cannot apply to this row.

10. **"Model selection later put 3 of the outputs simulated here on the log scale (high mannose and acidic variants at the production bioreactor, and host cell protein at anion exchange)." / "For them, the error of constant variance on the raw scale is an assumption that the log-scale analysis does not support (Section 8.2)."**
    - Contradicted by Table 8.1. On the 28 planned runs, which are the runs the simulation used, high mannose was selected on the **raw** scale. It moves to log only on all 44 runs.

11. **The same sentence as item 1, read for afucosylation.**
    - An interval that excludes λ = 1 rejects the raw scale. By Section 8.2's own reasoning, the least-squares assumption behind the prediction interval then fails.
    - Yet the afucosylation model used for ranges is "Raw, 9 terms, 44 runs" (Table 9.1), and nothing is said about it.

12. **"On the log scale the same model has 0.067 and 0.074, in natural-log units." against "The precision of the host cell protein ELISA (AMV-3012) is a percentage of the level, 9.5 %, so the scatter of the results grows with the level."**
    - 0.067 to 0.074 in natural-log units is a CV of about 7 %. That is below the 9.5 % of the assay alone. A run residual contains the assay error plus process variation, so its SD should not be smaller, unless each result is a mean of replicate assays. With 13 residual df an estimate this low is possible by chance, but the next two points suggest a simpler explanation.
    - The interval in Section 8.2 implies a larger value. Its half-width is ln(15,349 / 12,201) = 0.2296 = t(0.975, 22) × s × √(1 + h₀). With t = 2.074, s × √(1 + h₀) = 0.111, so s is about 0.094 to 0.106 for h₀ from 0.1 to 0.4.
    - The figures agree if the half-split values are plain SDs of the residuals. A full quadratic with 15 terms on 28 runs shrinks those by about √(1 − 15/28) = 0.68: 0.067 / 0.68 = 0.098 and 0.074 / 0.68 = 0.109.
    - Either the label "residual SD" or the numbers are wrong.

13. **"The assumption of equal variance holds on the log scale and does not hold on the raw scale."**
    - Overstated. On the raw scale the variance ratio is 1.48² = 2.2, on residuals that share 13 df. The one-sided 5 % point of F(6, 6) is 4.28, and of F(13, 13) it is 2.58. The split alone does not show unequal variance; the Box-Cox interval is the evidence.
    - A test can fail to reject an assumption. It cannot show that the assumption holds.
    - The evidence is for the full quadratic, not for the selected 5-term model that sets the limits.

14. **"It found 14 of the 22 full quadratic models below the limit on overfitting."**
    - Wrong direction. The limit is a maximum, and the 14 models lie above it: 0.26 to 2.14 against 0.20 (Table 3.1).

15. **"A model that fails the lack-of-fit test or the limit on overfitting is refitted with a justified change of terms or transformation, or it is not used to set a range."** (Section 3)
    - Section 3 and Section 5 describe §7.2 differently. Section 5 says: "PCMP-001 §7.2 allows two remedies for a model that fails the lack-of-fit test or the limit on overfitting." It adds that "the design may instead be augmented with further runs as a second block".
    - Section 3's account of §7.2 leaves augmentation out.

16. **"It decided by p-value, which tests each term against zero and does not compare models."**
    - Wrong. The t-test, or partial F-test, of a term is a comparison of two nested models: one with the term and one without it.
    - What it does not do is weigh fit against the number of terms on a common scale, or compare models that are not nested.

17. **Table 10.1 conflicts with the text in Section 10.**
    - Table 10.1 gives CA3 as "complete at closure" (2026-09-28).
    - The CA3 action includes "each report records it as a discrepancy from its plan".
    - The text says "Its second part, the re-evaluation of the augmented designs on all runs, is carried by the Version 2.0 reports of the two steps, due on 2026-09-30, together with the models chosen by model selection." The reports that carry CA3 are therefore due after closure.

18. **"Responses are simulated at the planned and the augmentation runs, as the true model plus an error drawn from a normal distribution with the residual standard deviation, the same at every level."**
    - The planned results were already in hand, and they had failed (for example, high mannose had a gap of 0.26). For an augmentation of those data, the relevant probability is conditional on the observed planned results. Re-drawing them answers a different question: that of a new design made of planned plus augmentation runs.
    - The "true model" is the refit, chosen by significance. Its kept coefficients are biased away from zero, which makes the assurance optimistic.
    - Neither limitation is stated.

19. **Table 6.1 is ambiguous at 0.90.**
    - MVM clearance at anion exchange prints 0.90 at 20 further runs, yet "Runs needed" is 22.
    - Acidic variants print 0.90 at 12 runs, and "Runs needed" is 12.
    - With 4,000 data sets, the first value must lie between 0.895 and 0.8999. On its face the table contradicts its own rule.

20. **"No effect of the parameters on them was detected within the ranges studied, at the power the designs give (Section 6.4)."** (and "It says that no effect of the parameters was detected within the range studied, at the power the design gives (Section 6.4).")
    - Section 6.4 gives power only for effects in the high mannose, acidic variant and anion exchange host cell protein models.
    - No power is given anywhere for leached Protein A, fragments at anion exchange or fragments at virus filtration, so the cited section does not support the statement.

21. **"The lack-of-fit test therefore gives no sign of systematic error in the full quadratic model."** (minor)
    - With four centre points, pure error has 3 df, against lack-of-fit df of 10, 5 and 3 for the 4-, 3- and 2-factor designs. The test therefore has little power.
    - For a model of the mean, where "the check reduces to the lack-of-fit test", a pass is nearly automatic.

22. **"A conclusion over the NOR is the judgement whether an output meets its criterion everywhere within the NOR, at every combination of NOR low, set-point and NOR high of the response-surface factors."** (minor)
    - The grid of combinations is not "everywhere". With a squared term (load flow rate² for pool host cell protein; culture pH² for acidic variants), the extreme of the prediction or of its bound can lie between grid points.

23. **"PRESS divides the residual of each run by one minus its leverage, and at the average leverage of these designs this enlarges a squared residual by a factor of 4.0 to 5.1."** and **"R² minus predicted R² therefore grows with the share of the variation that the model leaves unexplained, one minus R²."** (minor)
    - Both are correct at the average leverage: 4.64, 5.06 and 4.00.
    - But leverage in these designs runs from 0.12 to 0.66 (4 factors) and from 0.21 to 0.79 (2 factors). The expected enlargement, Σ(1 / (1 − hᵢ)) / (n − p), is therefore 5.2, 7.0 and 5.4.
    - In Table 3.1 the gap per unit of 1 − R² ranges from 2.75 (fragments at virus filtration) to 8.4 (MVM at virus filtration).
    - Acidic variants (1 − R² = 0.06) has a larger gap (0.34) than high mannose (1 − R² = 0.09; gap 0.26).

24. **"For a model of the mean alone, R² is zero and R² minus predicted R² depends on the number of runs only, 0.19 for 12 runs and 0.08 for 28, so for such a model the check reduces to the lack-of-fit test."** (minor)
    - Correct for a single block (0.190 and 0.075).
    - Fragments at anion exchange is a model of the mean with a block term on 40 runs (Table 9.1), and its R² is not zero.

25. **"Least squares, and the t-tests, F-tests and prediction intervals built on it, assume residuals that are independent and normally distributed, with mean zero and the same variance over the whole range studied."** (minor)
    - Least-squares estimates need no normality. Only the tests and intervals do.

26. **"The residual standard deviations of the refits behind these figures are 0.43 % for high mannose, 1.50 % for acidic variants and 2.37 ng/mg for host cell protein."** (minor)
    - The units are percentage points, not per cent.

27. **Query, not a finding.** "On the selected model of all runs, the lower prediction limit at culture pH 6.95, culture temperature 34.5 °C, culture duration 18 days and dissolved CO2 (pCO2) 130 mmHg is 16.2 % at manufacturing scale, so the criterion is not met."
    - If 6.95 and 18 days are the NOR highs (both lie above the coded centre), the low end of acidic variants sits at high pH and long culture. That runs against the usual direction: deamidation rises with pH and with time.
    - The document gives no coefficient signs or interaction that would let a reader see why.

## Question 6. Sentences that read as machine-written

| Sentence | Fails | Why |
|---|---|---|
| "The log scale changes the following, and nothing else:" | Q6 | Emphasis that adds nothing. |
| "It is therefore suitable, and the least-squares assumption behind it holds on the log scale, which on the raw scale it does not." | Q6 | Garbled ("which … it does not"). It restates the previous paragraph. |
| "The interval from the log scale is correctly wider there." | Q6 | The word "correctly" is hedged emphasis. The sentence restates the one before it. |
| "Passing §7.2 on the planned runs did not make every model reliable." | Q6 | A vague signpost ("reliable" is undefined). The next sentences carry the content. |
| "The augmentation was not needed to pass the test, but it changed what these two models say, and the reports use the models of all runs." | Q6 | Restates the opening of 8.5.1 and the Summary. |
| "Each change that model selection made is argued by its risk." | Q6 | Commentary on the text's own argument. |
| "A replacement does not always mean that the product did better." | Q6 | A hedge that the next sentence makes redundant. |
| "A bound from a tolerance interval would be statistically purer, but it is too conservative, and the single-batch prediction bound was chosen as the pragmatic rule." | Q6 | A hedged evaluation with no numbers. |
| "Under those effects a failure was at least as likely as success for each of the three models." | Q6 | Restates the three numbers just given (0.25, 0.44, 0.49). |
| "The decision was to calculate the further runs needed to resolve the effects where a model bears on the drug substance specification, and to reduce the model in every other case." | Q6 | Restates the numbered rule that follows it. |
| "Predicted R² falls well below R² even where the lack-of-fit test gives no sign of systematic error." | Q6 | Restates Section 3. The phrase "well below" is vague. |
| "In both cases the low end of the offset interval decides." | Q6 | Appears word for word in both 8.5.5 and 9.1. Section 8.5.5 as a whole duplicates 9.1. |
| "These two qualifications rest on the criteria that model selection widened." | Q6 | Appears word for word in the Summary and in 9.1, and again in 8.5.5 as "These two qualifications rest on the widening, which Section 9.1 sets out." |
| "An output that the data give without error, with replicates that agree exactly at the precision the method reports, is fitted exactly by more than one candidate." | Q6 | No statistician phrases it this way. |
| "The corrective action for it is model selection for every response-surface output, adopted on the same date as corrective action CA3 (Section 8)." | Q6 | The 2026-09-15 root-cause and CA3 date already appears in the Summary, Section 1, Table 1.1 and Section 8.1. |
| "Its runs are numbered on from the planned design." | Q6 (minor) | Unidiomatic. Better: the augmentation runs continue the run numbers of the planned design. |

## Question 7. Sentences that cannot be read on their own

**A. §7.2 used alone (criterion code).** The thing to name is "the model-adequacy criteria": a significant model F-test, no significant lack of fit, and R² minus predicted R² of at most 0.20. Each sentence below fails Q7 for this reason.

- "The assurance is the probability, at the effects estimated from the planned runs, that the planned model, the full quadratic with a block term, meets §7.2 on all runs (Section 6)."
- "Each output is modelled on the log or the raw scale, as its Box-Cox profile decides, by the submodel of the full quadratic with the lowest AICc, and that model is judged against §7.2."
- "Once selected, the three models that the augmentations were made for meet §7.2 on the planned runs alone, so the augmentations were not needed to pass that test."
- "A §7.2 check of a selected model is optimistic, because the selection used the same runs."
- "As an immediate action, no proven acceptable range, design space or judgement across the normal operating range (NOR) was set from a model that did not meet §7.2 while the investigation was open."
- "Table 3.1 lists the 14 full quadratic models that do not meet PCMP-001 §7.2, out of the 22 models in scope."
- "The 8 models that meet §7.2 on the planned runs need no remedy (Table 2.1)."
- "With the planned runs alone, the probability that the full quadratic model meets §7.2 is 0.25 for high mannose, 0.44 for acidic variants and 0.49 for host cell protein at anion exchange."
- "§7.2 leaves it to the investigation of a failing model to state when a design is augmented and how the number of runs is calculated."
- "The number of runs is the smallest that gives an assurance of at least 0.90 that the planned model, the full quadratic with a block term, meets §7.2 on all runs (Section 6)."
- "The refitted model is then judged against §7.2 in the same way as the full model."
- "Where neither the full nor the refitted model meets §7.2, the response is judged on its measured results, as PCMP-001 §7.2 asks."
- "The refits of the fragments model of low-pH viral inactivation and the fragments model of cation exchange do not meet §7.2 either."
- "The simulation estimates the assurance, the probability, at the effects estimated from the planned runs, that the planned model meets §7.2 once the design has been augmented by a given number of runs."
- "Their effects are too small against the residual variation for the full quadratic model to meet §7.2 at any size computed."
- "The augmentations are sized for §7.2, not for the power of each effect."
- "The production bioreactor report (PCR-003) therefore re-evaluates every model of the step on all runs, including the 3 models that met §7.2 on the planned runs."
- "The selection used the same runs that §7.2 then judges."
- "A model chosen as the best of many candidates fits those runs better than a model fixed in advance, so §7.2 is an optimistic check of a selected model."
- "Where the bound itself is better than the platform worst case, on a selected model that meets §7.2, the bound replaces the platform value, and the criteria upstream widen."
- "Every output whose full quadratic model met §7.2 has an adequate selected model."
- "The three models that the augmentations were made for meet §7.2 on the planned runs alone once they are selected."
- "They were decided on 2026-09-02 under the model of the plan, the full quadratic, which failed §7.2 on the planned runs."
- "Table 8.1 gives the three selected models on the planned runs and on all runs, with all three statistics of §7.2."
- "Each meets §7.2 on both sets of runs."
- "Passing §7.2 on the planned runs did not make every model reliable."
- "The refit had reduced it to its mean, which meets §7.2."
- "The full quadratic model of host cell protein does not meet §7.2, so its bound of 4.28 cannot widen a criterion, and the platform worst-case clearance fold of 4 enters the derivation."
- "The selected model meets §7.2, and its bound of 4.27 replaces the platform fold."
- "Each widening rests on the one-sided 95 % prediction bound of a single batch at the least favourable combination of the NOR as characterized, from a selected model that meets §7.2."
- "A §7.2 check of a selected model is optimistic (Section 8.1), so Table 9.3 shows what depends on the widening."
- "Two of these conclusions are not met on either model, and both rested on full quadratic models that fail §7.2:"
- "PCMP-001 §7.2 leaves it to the investigation of a failing model to state when a design is augmented and how the number of runs is calculated."
- "Once selected, the models that the augmentations were made for meet §7.2 on the planned runs alone."

**B. INV-001 used alone (finding number).** The thing to name is "the investigation into acceptance criteria set after the data were seen". Each sentence below fails Q7 for this reason.

- "Model selection was adopted before INV-001 closed on 2026-09-18, so the intermediate acceptance criteria fixed at that closure rest on the selected models."
- "QA opened INV-002 on 2026-08-31, while INV-001 was still open."
- "The Version 1.0 documents, whose ranges came from the full quadratic models, were already on hold for BLA use under INV-001."
- "INV-001 set it, and this investigation does not change it." (This one also needs "it" named: the rule that derives the intermediate acceptance criteria.)
- "The last planned response-surface study ended on 2026-05-15, before INV-001 was opened."
- "Model selection was adopted as corrective action CA3 on 2026-09-15, before INV-001 closed on 2026-09-18."
- "Both augmentations ended after INV-001 closed, on 2026-09-24, and the verification uses only the planned runs of each step."
- "The intermediate acceptance criteria in force were fixed at the closure of INV-001 on the selected models."

**C. PCMP-001 used alone.** The thing to name is "the process characterization master plan". Each sentence below fails Q7 for this reason.

- "PCMP-001 Version 1.0 had left these thresholds to the individual study."
- "The threshold of PCMP-001 Version 2.0 came later." (This one also needs the threshold named: R² minus predicted R² of at most 0.20.)
- "PCMP-001 is not changed."
- "PCMP-001 and the plans are not amended."

**D. Rule codes and labels.**

| Sentence | Fails | Name instead |
|---|---|---|
| "The curves of the anion exchange models of XMuLV clearance and MVM clearance, and the virus filtration model of MVM clearance cross the target within the size of the planned design, and these models are refitted under rule 2." | Q7 | The code "rule 2" should be named: viral clearance models are refitted and no virus is spiked. |
| "The rule gives 3 models an augmentation, in 2 steps." | Q7 | Name it: the remedy rule approved on 2026-09-02. |
| "The rule did not foresee one case." | Q7 | Which rule, and which case: the XMuLV model at low-pH viral inactivation, which bears on a NOR decision. |
| "The rule refitted it as a model of viral clearance." | Q7 | Name the rule, and "it" (the XMuLV model at low-pH viral inactivation). |
| "In this campaign the rule applies to acidic variants at low-pH viral inactivation." | Q7 | Three rules are in play in Section 8.1 alone. This one is the exact-fit rule. |
| "Last planned response-surface study ended (S-VF-RSM)" (Table 1.1) | Q7 | A study code with the study unnamed: the virus filtration response-surface study. |

**E. Abstract stand-ins and referents not named in the sentence.**

| Sentence | Fails | Name instead |
|---|---|---|
| "The finding concerns the full quadratic model of PCMP-001 §6.2, fitted to the runs of the planned face-centred design." | Q7 | What was found: 14 of 22 full quadratic models exceed the 0.20 limit on R² minus predicted R². |
| "The decision was to calculate the further runs needed to resolve the effects where a model bears on the drug substance specification, and to reduce the model in every other case." | Q7 | Who decided what: QA approved the remedy rule on 2026-09-02. |
| "A replacement does not always mean that the product did better." | Q7 | Replacing the platform worst-case aggregate increase by the A-Mab bound. |
| "The investigation changes the model of every output with a criterion in the report of its step." | Q7 | Model selection (CA3) replaces the full quadratic model in each report. |
| "Each change that model selection made is argued by its risk." | Q7 | The four wider intermediate criteria. |
| "These two qualifications rest on the widening, which Section 9.1 sets out." | Q7 | The scale-down qualifications for host cell protein, and the wider criteria from the selected models. |
| "The check has three outcomes." | Q7 | The check of a selected model against the model-adequacy criteria. |
| "The differences come from changes at 3 downstream steps:" | Q7 | The differences between the criteria from the two verifications. |
| "They changed what two models of the production bioreactor say, those of high mannose and aggregates, whose models selected on the planned runs predict the new runs poorly." | Q7 | "They" means the augmentation runs. The phrase "what … say" should become the terms gained and lost. |
| "The augmentation was not needed to pass the test, but it changed what these two models say, and the reports use the models of all runs." | Q7 | Which test (the model-adequacy criteria), and which change (terms dropped and added). |
| "The scale-down model, however, would not be qualified for host cell protein in the Protein A pool and at cation exchange." | Q7 | The condition: against the criteria that the full quadratic models would have given. |
| "Model selection made 4 of them wider." | Q7 | Which four intermediate acceptance criteria, and against what. |
| "The integrated process model gives no out-of-specification drug substance for either attribute in its 2,000 simulated batches, and a normal-tail probability of less than one per million." | Q7 | This model appears nowhere else in the document. Say what it is and what it simulates. |
| "Its augmentation runs were complete at closure." | Q7 | "Its" means corrective action CA1. |
| "The power is the share of simulated data sets in which the term is significant at α = 0.05 in the fitted planned model." | Q7 | "The planned model" means the full quadratic with a block term. |

---

## The owner's request: the log scale and the model search

**Verdict: partly met.**

**What Section 8.2 now does well.** It walks a reader who is not a statistician through most of the requested steps:
- The model on the log scale and transformed back, as two equations.
- What a coded unit is: −1 to +1 over the range studied.
- What a factor per coded unit means: e^b per coded unit and e^2b over the range, with four worked fold changes and "A factor below one is a decrease".
- What least squares assumes.
- Evidence: the residual SD by halves on both scales, and the Box-Cox interval.
- Seven consequences for limits and intervals, including a worked asymmetric interval.

**What Section 8.3 does well.** It explains the search step by step:
- Strong hierarchy.
- The number of candidates (13, 95 and 1,337, all correct).
- What AICc rewards and charges, with the 28-run arithmetic (32 and 49.5, both correct).
- Why a stepwise search can stop short, with an example.

**Where it does not do what was asked.** A reader who is not a statistician will stall at these sentences:

| Sentence | Gap |
|---|---|
| "The Box-Cox profile likelihood of the power λ is calculated for the full quadratic model of the output, with the block term where the runs form two blocks (Box and Cox 1964)." | The step that decides the scale is the one left unexplained. Nothing says that the output is raised to the power λ, that λ = 1 is the raw scale and λ = 0 is read as the natural log, or what a profile likelihood is. Nor does anything say why the scale is chosen on the full quadratic before the search. |
| "The Box-Cox profile puts λ at 0.06, with a 95 % interval from −0.32 to 0.42, which contains 0 and excludes 1." | The reader gets the numbers without knowing what the interval measures. |
| "Each parameter multiplies the output by a fixed factor, 𝑒𝑏 per coded unit and 𝑒2𝑏 from the low to the high end of its range." | No worked case. For protein load, e^2b = 2.43 gives b = 0.444 and e^b = 1.56, so pool HCP rises 56 % per coded unit, that is per half of the studied range. The size of that half-range in g/L resin is never given. The equation shows only linear terms, although the worked model has a squared term. |
| "Load flow rate also has a squared term, so its effect is not the same along its range." | Says what the effect is not, not what it is: where it turns, or the factor from low to centre and from centre to high. |
| "On the raw scale the full quadratic model of pool host cell protein has a residual SD of 638 ng/mg in the lower half of its predictions and 947 ng/mg in the upper half." | Neither how the halves are formed nor what "residual SD" means here is said. The log-scale figures are probably not ordinary residual SDs (Q5 item 12). Nothing tests whether a ratio of 1.48 is more than chance. |
| "The assumption of equal variance holds on the log scale and does not hold on the raw scale." | Overstated (Q5 item 13). Nothing covers the other two assumptions the paragraph lists, normality and independence: there is no normal plot and no run-order check. The evidence is for the full quadratic, not for the selected model that sets the limits. |
| "Least squares, and the t-tests, F-tests and prediction intervals built on it, assume residuals that are independent and normally distributed, with mean zero and the same variance over the whole range studied." | Teaches the wrong thing on one point: least-squares estimates need no normality. Only the tests and intervals do. |
| "At the least favourable combination of the NOR (protein load 39 g/L resin, elution buffer pH 3.4, load flow rate 150 cm/hr and end of pool collect 2.3 CV), the predicted pool host cell protein is 12,201 ng/mg, and the 95 % prediction interval of a single run runs from 9,698 to 15,349 ng/mg, 2,503 below and 3,148 above." | Skips the step that explains the asymmetry: ln 12,201 = 9.409, ± 0.230 on the log scale, then transformed back. It does not say whether the scale-down offset of 0.97 has been applied; it says "single run" here and "single batch" elsewhere. It does not say that the interval is two-sided while the criteria use a one-sided 95 % bound (about 14,755 ng/mg at this point). |
| "It is therefore suitable, and the least-squares assumption behind it holds on the log scale, which on the raw scale it does not." | Garbled. The reader loses the thread exactly where the assumption is tied to the interval. |
| "It rewards a close fit and charges a penalty for every estimated quantity, so that a term is kept only where it improves the fit by more than its penalty (Hurvich and Tsai 1989; Burnham and Anderson 2002)." | The fit term, n ln(SSE/n), is never shown. The reader sees the penalty (32 + 49.5) but not what it is weighed against. How large a difference in AICc matters appears only later, in Section 8.5.2. |

---

## Table observations

**Table 1.1**
- "S-VF-RSM" is not expanded, and RSM is not in the Abbreviations. The components of S-BRX-AUG and S-AEX-AUG (BRX, AEX, AUG) are not expanded either, although the row text names the studies.

**Table 3.1**
- In the text extract the words of the headers "Predicted R²" and "R² minus predicted R²" are interleaved over three lines, so the column order is hard to read. Check the PDF.
- The step labels "Protein A" and "Cation exchange" sit between their rows.
- Values agree with the text. In three rows the printed R² and predicted R² give gaps of 0.30, 0.51 and 2.15, against the printed 0.29, 0.50 and 2.14. The note explains this: the gap is calculated before rounding.

**Table 5.1**
- The dash in "Runs needed" has two meanings. The note says: "A dash means not reached within the size of the planned design, or not computed when the refit keeps no effect." Only the Reason column tells a reader which one applies to a row.
- The footnote markers a) and b) both have notes.
- The page numbers of this rotated table ("18", "19") leak into the text extract.

**Table 6.1**
- At 0.90 the table cannot be read: MVM clearance at anion exchange shows 0.90 at 20 runs with 22 runs needed, while acidic variants shows 0.90 at 12 runs with 12 needed. Print three decimals or add a note.
- "the table shows every fourth" (note) and "with every fourth size" (text) are wrong. The columns 0, 4, 8, … 28 show every **second** computed size, since sizes were computed in steps of 2.
- "Lowest power" is ambiguous. It is the power of the weakest effect at the size needed, not the lowest power over all sizes. The note explains this.

**Table 6.2**
- The note refers to Table 6.1 by a description ("The lowest power column of the table of assurance by the number of further runs") instead of by its number.

**Tables 7.1 and 7.2**
- In the text extract, the Table 7.2 headers for factor B (Equil/Wash-1 conductivity, mS/cm) and factor C (Load conductivity, mS/cm) run together. The word "conductivity" from C sits on the same line as "Equil/Wash-1", and B's own "conductivity" and both units follow on the lines below, so it is unclear which unit belongs to which column. Check the PDF.
- All coded levels agree with the settings, in both tables.

**Table 8.1**
- "Model p" is a constant column: < 0.001 in all six rows.
- R² and predicted R² are not given separately.

**Table 8.2**
- "Aggregates, HMW (%)": HMW is not in the Abbreviations.
- "Block p" belongs to a different model (the one selected on all runs) from the other columns in the row (the model selected on the planned runs). The note explains this, but the row mixes two models.

**Table 8.3**
- "Measured results" holds a count, not results. Call it number of results, or n.
- The virus filtration count of 19 disagrees with the 12 runs in Tables 2.1 and 9.1.
- The phrase "at manufacturing scale" in the note cannot apply to an LRF.

**Table 9.1**
- The "No adequate model" rows give no scale, which the offset rule needs.
- The merged "Discrepancies from the plan" column floats between rows in the text extract.
- Footnotes a) and b) are complete.

**Table 9.2**
- "Full" and "Selected" each appear twice, with different meanings: once for the limit, once for the downstream value.
- "Value in the derivation" mixes units in one column (% increase and dimensionless fold). The row labels carry the units.
- Two "Selected" values follow only from unrounded folds:
  - 7.02: from 5 × 1.404. The printed 1.40 gives 7.00.
  - 17,069: from 4,000 × 4.267. The printed 4.27 gives 17,080.
  - Add "calculated before rounding", as in Table 3.1.
- Footnote a) is complete.

**Table 9.3**
- "Conclusion over the NOR" is a constant column ("met / met" in all four rows).
- "Without model selection" names the same values that Table 9.2 calls "Full".

**Table 10.1**
- CA3 "complete at closure" conflicts with reports due 2026-09-30, after closure on 2026-09-28.
- CA1 "runs complete at closure" leaves the status of its second part unstated.
- The Owner column uses "Quality Assurance" where the rest of the document uses QA.

**Abbreviations with no legend**
- HMW (Table 8.2).
- CV, column volumes (Section 8.2).
- AMV (AMV-3012).
- RSM (Table 1.1).
- The document-type codes PCR, PCMP, PCMR and INV. PCR also collides with polymerase chain reaction in a virology context.

**Footnote markers**
- Every marker has a note, and every note has a marker (Tables 5.1, 9.1 and 9.2). No problem found.

**Units**
- Section 6.4 gives SDs in "%" that are percentage points.
- Table 9.2 mixes units in one column (see above).

---

## Arithmetic that checks out

These values were recomputed from the document and agree with it:

- **Table 3.1 and Section 3:** R² minus predicted R² for all 14 rows, within rounding. The counts 14 of 22; 5 failing F-tests (p from 0.280 to 0.936); 10 + 4 groups; R² ranges of 0.60 to 0.95 and 0.27 to 0.57; minimum predicted R² −1.83; lowest lack-of-fit p 0.096.
- **Section 4:** terms 15, 10 and 6; average leverage 0.536, 0.556 and 0.500; enlargement at average leverage 4.64, 5.06 and 4.00.
- **Model of the mean:** gap 0.190 for 12 runs and 0.075 for 28 runs.
- **Section 8.3:** candidate counts 13, 95 and 1,337; AIC penalty 32; AICc correction 49.45.
- **Section 6.2:** 81 candidate points; largest correlation between squared terms 0.689 on the planned runs and 0.542 on all runs (production bioreactor).
- **Tables 7.1 and 7.2:** every coded level agrees with its setting; 11 edge midpoints and 5 corners, and 10 and 2; corner repeats at runs 29, 33, 35, 41, 44 and 33, 36.
- **Section 5 counts:** 11 refits split 5, 3 and 3; 18, 22 and 8 runs; Table 6.2 has 9 of 14 effects at power 0.90 or more.
- **Section 8.2 interval:** 2,503 below and 3,148 above; symmetric on the log scale (±0.2296). Ratios 947/638 = 1.48 and 0.074/0.067 = 1.10 from the rounded values; the printed 1.11 is possible from unrounded ones.
- **Offsets:** 16,763 agrees within rounding with 15,349 × 0.97 / 0.89.
- **Table 9.2:** the derivation and the widenings of 4.4, 4.0, 6.7 and 6.75 %.
- **Risk arithmetic:** 17,069 / 40 / 4.267 = 100.0 and (6.46 + 0.559) / 1.404 = 5.00.
- **Table 8.3:** all three margins.
- **XMuLV at virus filtration:** an AICc difference of 1.0 implies R² 0.32 and F(1, 10) = 4.75, so p = 0.054, against the printed 0.053.
- **Section 9.2:** the implied XMuLV claim at anion exchange is 16.72 − 6.6 − 4.62 = 5.50 log10.
- **Tables 8.2 and 9.1:** the term counts and scales agree with Table 8.1 and the text. Seven outputs are on the log scale.
