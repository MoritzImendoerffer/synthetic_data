# Content review: PCP-003 Version 2.0, Production Bioreactor (run 2)

**Reviewer:** Claude Opus 5.5 (model ID `claude-opus-5-5`)
**Date:** 2026-10-09

**What I reviewed.** I read `PCP-003_bioreactor.DRAFT.run2.txt`, the text of the PDF. I checked the tables as images in `pc_package/PCP-003_bioreactor.DRAFT.pdf`, pages 9, 12, 15–16, 20–21, 23–24, 28, 34 and 37–38.

**Basis.** The review uses the document only, plus general knowledge of cell culture, analytics and statistics. I checked the arithmetic in Python using only values printed in the document: the planned design in Appendix B, the thresholds in Section 7, and the numbers in Sections 7, 8 and 11.

**Remit applied.** Version 2.0 may state what PCMP-001 Version 2.0 sets:

- the a priori criteria
- the fragment method
- the offset rule
- the adequacy tests
- the judgement statistics
- the verification rule
- the execution windows

It may also add generic tests. Beyond that it keeps Version 1.0.

I did not flag a missing rule where the plan says plainly that it sets none. The plan does this correctly in these places:

- Section 5.1: no qualification rule without an adequate model.
- Section 5.2: no rule for key process parameters.
- Section 6.3: no rule for the osmolality NOR, and none for changing the factors of the response-surface design.
- Section 7 item 4: no rule for a PAR narrower than the NOR.
- Section 7 item 5: no rule for the univariate study.
- Section 7 item 8: no capability criterion.

Things the plan adds after the data were known are flagged under Q4 and marked **[after data]**.

## Answers

| # | Question | Answer |
|---|---|---|
| 1 | Every cause is named as a physical cause with a direction | **No** |
| 2 | Every technical term is a term of art | **No** |
| 3 | Some sentence tells the reader how to file a finding | **Yes** (defect present) |
| 4 | Every criterion has its basis, and a second analyst can apply every stated rule | **No** |
| 5 | Some statement is wrong, inconsistent or contradicted by a table | **Yes** (defects present) |
| 6 | No sentence reads as machine-written ("yes" = none flagged) | **No** |
| 7 | Every sentence can be understood on its own ("yes" = none flagged) | **No** |

## The three most consequential problems

1. **The Cook's distance test fails almost every model by construction.**
   - Where: Section 7 item 2d and Section 1.1 item 7.
   - On the planned 28-run face-centred design with the 15-term model, at least one run exceeds 4/n = 0.143 in 99.5 % of correctly specified models (Q5-1).
   - Every prediction, every PAR, the design space and the scale-down qualification need an adequate model. So the rule hands all of them to an approach that the report chooses after the data are known.
   - The plan also does not say how the PAR intersection is formed when an attribute has no adequate model (Q4-4).
2. **pCO2 and osmolality are not separated as the plan claims, and the pCO2 PAR is not stated at manufacturing scale.**
   - Osmolality is not among the parameters controlled throughout a run (Section 5.2).
   - Section 4.1 says osmolality follows base additions and rises with pCO2. No procedure holds osmolality constant while pCO2 varies fourfold.
   - Section 6.2 says a pCO2 excursion at scale brings an osmolality rise with it. Yet Section 8 states the pCO2 PAR "at manufacturing scale" from a model in which osmolality is held constant. There is no rule for this, and no statement that none is set.
   - Section 4.1 expects osmolality to raise high mannose, the only attribute of very high criticality. Osmolality still gets no PAR. See Q4-2, Q5-2 and Q5-3.
3. **A second analyst cannot apply the classification rule.**
   - Where: Section 7 item 7.
   - The CPP decision rests on five terms that are not defined: "practically relevant", "appreciably", "high/low risk", "readily controlled" and "wide against its NOR". The plan does not say it leaves them to the report or to SOP-4001.
   - Significance alone cannot carry the decision. The screening tests 75 terms at α = 0.05, so about 3.75 are expected to be significant by chance (Q4-1).

**Next in line:** assumption 4 says the univariate parameters do not interact with the other parameters. The plan's own mechanisms in Section 4.1 contradict it (Q5-4).

## Checks that hold

- **Aggregate criterion.**
  - 5.00 × 1.4038 − 0.5586 = 6.4604, shown as 6.46.
  - 5.00 × 2.00 − 0.70 = 9.30.
  - The order of the calculation is right. Low-pH inactivation (step 6) comes before cation exchange (step 7), so the condition is x + 0.56 ≤ 5.00 × 1.4038.
  - From the rounded table values, 5.00 × 1.40 − 0.56 = 6.44. The note to Table 7.1 explains the difference, but that note has no marker (see Table observations).
- **Acidic variants.** 40.0 − 1.00 = 39.0.
- **Table 1.1.** Every Version 2.0 upper limit is above the limit Version 1.0 applied. The Version 1.0 lower limits equal the drug substance lower limits.
- **Table 6.1.** Every range studied extends beyond the NOR at both ends. The ratio of range width to NOR width is between 1.5 and 2.5 for all nine parameters:

  | Parameter | Ratio |
  |---|---|
  | pH | 2.5 |
  | Temperature | 2.0 |
  | pCO2 | 2.0 |
  | Osmolality | 1.6 |
  | Duration | 2.0 |
  | Dissolved oxygen | 2.0 |
  | Initial viable cell concentration | 2.5 |
  | Basal medium | 2.0 |
  | Feed | 1.5 |

- **Run counts.**
  - 3 + 19 + 16 + 28 = 66.
  - 4 × 2 × 2 = 16 univariate runs.
  - 3⁴ = 81 NOR combinations.
  - 5 × 4 = 20 PARs.
- **Degrees of freedom.**
  - Screening: 19 − 16 = 3 (2 for pure error, 1 for lack of fit).
  - Response surface: 28 − 15 = 13 (3 for pure error, 10 for lack of fit).
- **Appendix A.**
  - E = ABCD in all 16 factorial runs, so I = ABCDE and the design is resolution V.
  - The start orders are permutations of 1–19 (A.1) and 1–28 (B.1).
- **Section 8.** With SD = NOR/6, P(|Z| < 3) = 0.9973.
- **Table 11.1** matches the stated sequence.
  - Screening ends 2025-10-03 and the univariate study starts 2025-10-06.
  - The univariate and response-surface studies overlap from 2025-10-20 to 2025-10-31.
  - Every window closes before 2026-06-14.

## Q1. Is each cause named as a physical cause with a direction?

I flagged a sentence when its causal verb has no physical cause with a direction in the same clause.

1. "Culture temperature and culture pH set the growth rate and the intracellular pH, pCO2 lowers the intracellular pH, and osmolality changes the supply of nucleotide sugars."
   - Fails Q1: "set" and "changes" give no direction. Only the pCO2 clause has one.
2. "Each of these parameters can therefore change afucosylation, in a direction that the models will show."
   - Fails Q1: no direction, and "therefore" rests on the directionless sentence before it. Also Q6.
3. "Culture temperature, culture pH and pCO2 act on the galactosyltransferase and on the supply of UDP-galactose through the growth rate and the intracellular pH, in directions that the models will show."
   - Fails Q1: "act on" with no direction. Also Q6.
4. "Culture pH, culture temperature and pCO2 act both on the processing enzymes and on the rate of secretion, and the models will show the direction of their effects."
   - Fails Q1: "act on" with no direction. Also Q6.
5. "Culture pH, pCO2 and osmolality also act on the intracellular pH and on sialylation, and the direction of that route is not known from the chemistry."
   - Fails Q1: no direction. Part of the route is known: the plan itself says pCO2 lowers intracellular pH. Only the step from intracellular pH to sialylation is unknown, and the sentence should say so.
6. "The production bioreactor sets this load, and the purification steps clear it."
   - Fails Q1: the cause given is a unit operation. The real cause is cell lysis late in the culture. Also Q6.
7. "The effects of temperature and pH on the glycans pass through the glycosyltransferases and the growth rate, and the effect of each may depend on the level of the other and on the culture duration."
   - Fails Q1: names a route with no direction.
8. "The initial viable cell concentration acts on aggregate through the antibody concentration."
   - Fails Q1: "acts on" with no direction in the clause. The direction appears only about 30 lines earlier. Also Q6.
9. "The multivariate parameters act on the galactosyltransferase and the fucosyltransferase, on the supply of UDP-galactose and GDP-fucose, and on the rates of deamidation and aggregation (Section 4.1)."
   - Fails Q1: "act on" with no direction.
   - The next sentence infers interactions from this. Sharing a target does not by itself give an interaction. The donor-limitation argument in Section 4.1 does.
10. "The basal medium concentration and the nutrient feed-1 volume set the supply of glucose, amino acids and the precursors of UDP-galactose." *(low)*
    - Fails Q1: "set" with no direction. The direction comes only in the next sentence.
11. "Protein A binds the Fc region at the interface of the CH2 and CH3 domains, so it captures every glycoform alike (PCMP-001 §3)." *(low)*
    - Fails Q1: names a location, not the property that matters. That property is that the binding site does not include the Asn297 glycan.

**Not flagged.** These sentences each name a species or a property and a direction:

- fucosylation (GDP-fucose supply)
- galactose donor depletion
- osmolality and specific productivity
- Golgi transit time and high mannose
- aggregation as pH approaches the isoelectric point
- deamidation
- cell lysis
- CO2 stripping
- bicarbonate and osmolality

## Q2. Is every technical term a term of art?

1. "For each output, the judgement over the NOR is whether the output meets its criterion at all 81 combinations of NOR low, set-point and NOR high of the 4 response-surface factors."
   - Fails Q2: "judgement over the NOR" is coined. The check tests whether the NOR conclusion is robust to the offset, and should be named that way.
2. "The first analysis gives the set-point PAR, the PAR with the other factors at their set-points." and "The second analysis gives the NOR-propagated PAR, the PAR with the other factors varied over their NORs."
   - Fails Q2: "set-point PAR" and "NOR-propagated PAR" are coined. The literature terms are univariate PAR and PAR with the other parameters varied across their NORs.
3. "A model that fails the lack of fit test or the limit on overfitting is either refitted with a justified change of terms or transformation, or it is not used to set a range (PCMP-001 §7.2)."
   - Fails Q2: "the limit on overfitting" is not a term of art. It means the requirement that predicted R² be within 0.20 of R². Also Q4 and Q7.
4. "It is the drug substance limit multiplied by the clearance fold, less the increase."
   - Fails Q2: "clearance fold" is not standard, and Table 7.1 calls the same quantity "Clearance factor".
5. "Version 2.0 records the execution window of each study and the calibration status of the instrumented system that the studies used (Section 11)." *(low)*
   - Fails Q2: "instrumented system" is not a term of art. It means the pCO2 probe EQ-BRX-205. "Execution window" is defined in Section 11 and is acceptable.
6. "Each drug substance criterion is carried backward through the worst case of every downstream step, with no margin (PCMP-001 §7.3)." The basis "Carried back" in Tables 1.1 and 7.1 has the same problem. *(low)*
   - Fails Q2: the term of art is back-calculation, which the plan itself uses in the R1 legend.
7. Table 4.1, "10–40 % (G1+G2 equiv.)".
   - Fails Q2: "G1+G2 equiv." is not a defined measure. Total galactosylation is either G1 + G2 or (G1 + 2·G2)/2, and the abbreviation entry for %Gal does not say which.

## Q3. Does any sentence tell the reader how to file a finding?

1. "The change moves risk between the producer and the patient." The sentence that follows does the same: "A stricter criterion lowers the risk to the patient and raises the risk to the producer, because more batches may fail it."
   - Fails Q3: these sentences file the verification result as a risk trade-off.
   - For the tightening the framing is wrong. With the A-Mab cation exchange bound, the a priori criterion would let drug substance reach (9.30 + 0.70)/1.4038 = **7.12 % HMW** against a limit of 5.00 %. The tightening restores the drug substance limit; it does not move risk.
2. "Manufacturing Science holds the manufacturing-scale batch data and carries the ranges to the receiving site, and it reviews the plan as a function separate from Process Development / MSAT."
   - Fails Q3: the trailing clause answers an objection about independence that nobody raised.
   - It is also inconsistent (Q5-12): MSAT is "Manufacturing Science and Technology".
3. "The widening does not reflect a more stable product." *(borderline)*
   - Fails Q3: it files the widening before giving its cause. The following sentences carry the substance and should lead, for example: "The widening comes from the shorter A-Mab hold: ...".

## Q4. Does every criterion have its basis, and can a second analyst apply every rule?

1. **Classification, Section 7 item 7.** These three sentences:
   - "A critical process parameter (CPP) has an effect on a CQA that is significant and practically relevant within the range studied, and a high risk of falling outside its acceptable range in operation."
   - "A well-controlled critical process parameter (WC-CPP) has the same kind of effect on a CQA but a low risk of falling outside its acceptable range, because it is readily controlled and its PAR is wide against its NOR."
   - "A significant effect that is too small to move the attribute appreciably within the PAR does not by itself make a parameter critical."

   Fails Q4: these terms are not defined:
   - "practically relevant"
   - "high/low risk"
   - "readily controlled"
   - "wide against its NOR"
   - "appreciably"

   The plan does not say it leaves them to the report or to SOP-4001. Significance alone cannot carry the decision. The screening tests 15 terms × 5 responses = 75 terms, so about 75 × 0.05 = **3.75** are expected to be significant by chance.
2. **pCO2 PAR at manufacturing scale.** Two sentences conflict:
   - Section 6.2: "The effect of a pCO2 excursion at manufacturing scale is then the effect of pCO2 in the models plus the effect of the rise in osmolality that comes with it."
   - Section 8: "Each PAR is computed from the response-surface model of the attribute, with the offset of the attribute subtracted so that the PAR is stated at manufacturing scale."

   Fails Q4:
   - The response-surface model holds osmolality at 400 mOsm/kg, so the pCO2 PAR is a PAR at constant osmolality.
   - An offset estimated at the set-points corrects a level, not a slope.
   - The plan neither adds the osmolality rise nor says plainly that it sets no rule for it. Assumption 5 says the two effects add, but gives no procedure.
3. "A model that fails the lack of fit test or the limit on overfitting is either refitted with a justified change of terms or transformation, or it is not used to set a range (PCMP-001 §7.2)."
   - Fails Q4: "justified" is not defined, and neither is the choice between refitting and dropping the model.
   - No remedy is given for a model that fails criterion a or d. Yet the absolute-residual test in criterion d detects non-constant variance, the textbook case for a transformation.
4. "A parameter has a PAR for each attribute, and the range carried into the control strategy is their intersection."
   - Fails Q4: the rule is open when an attribute has no adequate model, and so no PAR (Section 7 item 2). Is that attribute left out of the intersection, or is no range carried at all?
   - This is not a marginal case, because almost every model fails criterion d (Q5-1).
   - Criterion a also declares a flat, well-controlled response inadequate, although a flat response is the best case for a PAR.
5. "Each step output is judged against its intermediate acceptance criterion in Table 7.1, at manufacturing scale."
   - Fails Q4: does not say where the output is judged. It could be at the set-point, at the 81 NOR combinations, or over the Monte Carlo simulation of Section 8.
6. **The verification rule.** Two sentences:
   - "Where the A-Mab worst case predicted within the NOR of a downstream step is worse than the platform worst case, the one-sided 95 % prediction bound of a single batch there replaces the platform value, and every criterion upstream becomes stricter."
   - "Where that bound is better than the platform value, and the model behind it meets the adequacy criteria above, the bound replaces the platform value, and every criterion upstream becomes wider."

   Fails Q4:
   - The mean prediction triggers tightening, but the bound triggers widening. When the mean is better than the platform value and the single-batch bound is worse, neither branch applies. The platform value then stands, although A-Mab data show that a single batch can do worse.
   - The rule does not say how the worst case within the NOR is found: at the corners, on a grid, or at the 3^k combinations.
7. **The basis of the carried-back criteria.** Two sentences:
   - "The aggregate criterion is carried back through the aggregate clearance of cation exchange and the aggregate increase across low-pH viral inactivation."
   - "Its lower limit is the drug substance lower limit of 18.0 %, because the derivation credits low-pH viral inactivation with no increase on the side of the lower limit."

   Fails Q4:
   - The stated basis is "the worst case of every downstream step", but only two steps appear.
   - Table 7.1 merges all downstream steps into one factor and one increase. A reader cannot check that Protein A elution, anion exchange, virus filtration and UF/DF were taken as 1.00 and 0.00.
   - For the lower limit of acidic variants, the adverse direction is a decrease, and the ion exchange steps separate by charge (Q5-8).
8. **[after data]** The low-pH argument in Section 7, Version 2.0. Three sentences:
   - "At the edges of the range studied, the A-Mab aggregate increase was 0.84 percentage points, more than the platform worst case of 0.70."
   - "The NORs in force for hold time and temperature end at the same values as the NORs as characterized, and the low-pH aggregate model has no pH term."
   - "The bound therefore also covers the NORs in force, and routine manufacture does not hold longer than the NOR."

   Fails Q4:
   - This is reasoning about another step's results, written after the data were known.
   - The plan itself says the report PCR-003 gives this argument.
   - The amendment may state the verification rule and the criterion it yields. It should not argue a downstream result.
   - The science is also weak (Q5-5).
9. **[after data]** "For the widening it gives the bound, the runs behind it, and the reason why the performance of low-pH viral inactivation for A-Mab is known well enough to replace the platform value."
   - Fails Q4: "known well enough" adds an undefined standard on top of the stated rule (an adequate model plus the bound). It also presupposes the answer.
10. **[after data]** "The bioreactor report PCR-003 reports what the screening showed, and it records the later osmolality study S-BRX-OSM as discrepancy PD-003-01 from this plan."
    - Fails Q4: this is an execution detail known only after the screening data: a study added later and its discrepancy number. It does not belong in the design section of the plan.
11. "At each of 81 grid points across the range studied of the parameter of interest, 2,000 operating points are drawn for the other factors." *(low)*
    - Fails Q4: with 2,000 draws, the 97.5th percentile has a Monte Carlo standard error of about **0.06 SD**. No seed and no tolerance are set, so two analysts can get different PAR edges.
12. "This plan measures acidic variants by icIEF only (Section 5.3)." *(low)*
    - Fails Q4: the drug substance criterion in Table 4.1 is given for "CEX/icIEF". The plan states no bridging between the two methods and does not say the limit is independent of the method.

## Q5. Is any statement wrong, inconsistent or contradicted by a table?

**Q5-1. The Cook's distance rule** (Section 7 item 2d; Section 1.1 item 7).

The sentences:

- "No single run dominates when no run has a Cook’s distance above 4/n, where n is the number of runs of the design."
- "No run may have a Cook’s distance above 4/n, where n is the number of runs of the design."

The rule conflicts with the design in Table B.1 and the model in Section 5.5 (28 runs, p = 15 terms). Arithmetic:

1. The leverage h of each run type:

   | Run type | h |
   |---|---|
   | Factorial | 0.659 |
   | Axial | 0.498 |
   | Centre | 0.120 |

   The leverages sum to 15.0 = p.
2. Cook's D = (r²/p) × h/(1 − h), where r is the studentized residual.
   - For a factorial run, D = r² × 0.659/(15 × 0.341) = 0.129 r². This exceeds 4/28 = **0.143** when |r| > **1.05**.
   - An axial run exceeds it when |r| > 1.47.
3. I simulated 20,000 fits of a correctly specified model with normal errors. In **99.5 %** of them at least one run exceeds 4/n.
   - Criterion d as a whole fails in 99.6 %.
   - The two slope tests alone reject 6.6 % and 7.8 % of correct models.
4. Criterion c adds to this. On this design E[PRESS] − E[SSE] = 54.4 σ².
   - Predicted R² therefore stays within 0.20 of R² on average only when R² ≥ 1 − 13/(5 × 54.4) ≈ **0.95**.
   - In the simulation, fits with R² ≈ 0.87 failed criterion c 96 % of the time.

Conclusion: here p/n = 0.54. At that ratio, 4/n can serve to flag runs for a look, but not as a pass/fail test. This generic test was added in Version 2.0, and it cannot tell an adequate model from an inadequate one.

**Q5-2. Osmolality said to be held constant.**

The sentence: "Osmolality and pCO2 are separate factors of the screening design, and each run holds each of them at the level that the design gives (Section 5.2)."

The plan's own text does not support it:

- Section 5.2 says only "pH, temperature, dissolved oxygen and pCO2 are controlled at the levels of the run throughout the culture". Osmolality is not on that list.
- Section 4.1 says "In routine manufacture osmolality follows the base and feed additions and the accumulation of metabolites".
- Section 4.1 also says pCO2 "raises the osmolality of the medium as bicarbonate accumulates".

Physical chemistry adds a second problem:

- At fixed pH, bicarbonate is proportional to pCO2. The design levels of 40 and 160 mmHg (Table 6.2) need 160/40 = 4 times as much bicarbonate at the high level, plus the matching cation from the base.
- With textbook values for CO2 solubility and pK′ (these are not in the document), the difference is about 20 mmol/L at pH 6.85. That is about 40 mOsm/kg, and almost twice as much at pH 7.1.
- 40 mOsm/kg is the half-width of the osmolality range studied (360–440 mOsm/kg).

The plan does not say how osmolality is set or when it is measured: in the initial medium, by salt additions, by control, or at its peak. So the claim that the design separates the two effects is unsupported.

**Q5-3. The pCO2 PAR is not at manufacturing scale.** See Q4-2. The sentence in Section 6.2 contradicts the claim in Section 8 that every PAR is "stated at manufacturing scale".

**Q5-4. The univariate assumption contradicts Section 4.1.**

The sentence: "The univariate parameters do not interact with the other parameters within their ranges, and their effects do not reverse between the two ends of each range studied."

Section 4.1 predicts two interactions:

- **Galactosylation.** Section 4.1 says "When the supply of UDP-galactose limits the reaction, a parameter that speeds the enzyme can raise galactosylation only as far as the donor allows. The effect of one parameter can then depend on the level of another." It also says "The basal medium concentration and the nutrient feed-1 volume set the supply of … the precursors of UDP-galactose", and that the donor is depleted late in the culture. Together these predict that basal medium and feed volume interact with culture duration, temperature and pH.
- **Aggregate.** The rate of aggregate formation "rises with the antibody concentration and with the time at temperature". A higher initial viable cell concentration raises the antibody concentration. So the amount formed scales with concentration × time, which is an interaction between initial viable cell concentration and duration.

A study that varies one factor at a time cannot detect either interaction.

**Q5-5. The aggregate widening holds only while the low-pH hold stays inside its NOR.**

The sentence: "The bound therefore also covers the NORs in force, and routine manufacture does not hold longer than the NOR."

Arithmetic from the document's own values:

- Take a batch at the criterion, 6.46 % HMW, held to the 180 min edge of the range studied (increase 0.84).
- It gives (6.46 + 0.84)/1.4038 = **5.20 % HMW** in drug substance, above the 5.00 % limit.
- Keeping drug substance at 5.00 % with an increase of 0.84 would need a criterion of 5 × 1.4038 − 0.84 = 6.18 %.

So the widened criterion covers only holds of 120 min or less. A hold beyond the NOR but within the PAR is exactly the case a PAR is meant to allow.

"The low-pH aggregate model has no pH term" treats a term dropped by model selection as evidence that pH has no effect. pH is a known driver of aggregation at low pH. A dropped term shows only that its effect was not resolved within the range studied.

**Q5-6. The revision history contradicts Section 1.1.**

The revision history says: "Reissued under INV-001 and INV-002: a priori intermediate acceptance criteria, re-analysis of the studies, execution dates recorded; changes listed in the document (see INV-001)".

Section 1.1 says:

- "INV-002 changes nothing in this plan".
- Seven changes are listed, and none of them is a re-analysis.
- What INV-002 changed in the analysis is recorded in PCR-003 as discrepancies from this plan.

So the revision history claims a change the plan does not contain.

**Q5-7. The offsets cannot plausibly have been estimated before the first characterization run.**

The sentence: "The offsets are estimated before the first characterization run, and the decision whether the model is qualified for an output is made at analysis."

The dates in Table 11.1:

- S-BRX-SDM ends **Friday 2025-09-05**.
- S-BRX-SCR starts **Monday 2025-09-08**, three calendar days later.

In those three days, all of this would have had to happen:

- the last scale-down culture tested by glycan mapping, icIEF and SEC
- the results reviewed and released by Analytical Development (Section 9)
- the offsets estimated

The rule first appears in Version 2.0, which took effect on 2026-09-30. It cannot have governed what was done in September 2025. The plan should say whether the requirement was met.

**Q5-8. The lower limit for acidic variants ignores the ion exchange steps.**

The sentence: "Its lower limit is the drug substance lower limit of 18.0 %, because the derivation credits low-pH viral inactivation with no increase on the side of the lower limit."

- For a lower limit the adverse direction is a decrease.
- Section 4.1 says "The two ion exchange steps separate by charge" and counts sialylated forms among the acidic variants. A decrease across cation or anion exchange is therefore possible, and none is shown.
- "No downstream step is credited with removing acidic variants" is conservative only for the upper limit.
- Table 7.1 also disagrees with a direct reading of it. Its increase of 1.00, applied to the lower limit, gives 18.0 − 1.00 = 17.0, not the 18.0 shown.

**Q5-9. The glycan profile is "decided in this step" only for neutral glycoforms.**

The sentence: "The glycan profile of the drug substance is therefore decided in this step."

- The premises include that sialic acid carries a charge and that ion exchange separates by charge.
- Sialylated glycans carry galactose. Any downstream removal of acidic species would therefore lower %Gal.
- The conclusion holds for the neutral glycoforms only.

This weakens the claim "Afucosylation, galactosylation and high mannose keep their drug substance criteria, because no downstream step changes them" for the lower limit of galactosylation. The effect is probably small, but the argument has a gap.

**Q5-10. SEC and host cell protein.**

The sentence: "It does not apply to aggregate, which SEC reads from the high molecular weight window (PCMP-001 §7.8)."

- Host cell proteins span sizes above the antibody and form complexes, so some elute in or before the HMW window.
- The samples here are culture fluid (Section 5.4), and no Protein A clean-up is described.
- The argument needs the sample preparation, or evidence that no host cell protein elutes in the HMW window.

**Q5-11. The calibration argument does not address drift** (Section 12, risk 2).

The sentence: "The calibration interval of the probe limits this risk, and every study window closed before the next calibration of the probe was due (Section 11)."

- Drift happens between calibrations, so a study that ended before the due date may still have used a drifted probe.
- Only the as-found result of the calibration due on 2026-06-14 shows whether the probe held. That result was available 108 days before this version took effect.
- The plan gives neither that result nor the date of the previous calibration.

**Q5-12. The names of the functions contradict each other.**

- Section 10 says Manufacturing Science reviews "as a function separate from Process Development / MSAT" (the Q3-2 sentence).
- The abbreviation list defines MSAT as "Manufacturing Science and Technology", which is the author's function and the document owner.
- The claim that the two are separate contradicts these names, unless the organization is explained.

**Q5-13. The capability simulation** (Section 5.5). *(low)*

The sentences:

- "The model simulates 2,000 batches, with every process parameter varying about its set-point as in the PAR analysis (Section 8), and it records the drug substance attributes of each batch."
- "The same simulation gives, for each attribute, the probability that the drug substance falls outside its criterion."

Two problems:

- **Not every parameter varies.** The PAR analysis varies only the 4 response-surface factors. Osmolality and the 4 univariate parameters have no terms in that model, so "every process parameter varying" cannot carry their variation through.
- **The count cannot resolve the thresholds.** A count over 2,000 batches resolves steps of 1/2000 = 0.05 %.

  | Cpk | One-sided fraction outside | Expected batches out of 2,000 |
  |---|---|---|
  | 1.33 | 0.0033 % | 0.066 (the count is zero in 94 % of simulations) |
  | 1.00 | 0.135 % | 2.7 |

  The estimate cannot resolve the region between the two thresholds that Section 7 item 8 uses.

## Q6. Which sentences read as machine-written?

I looked for padding, restatement and hedged emphasis.

1. "The characterization of A-Mab tests these expectations and bounds the effects for this cell line and this molecule."
   - Padding: it says what any characterization does.
2. "The expected effects are summarized below, and the sign and size of each effect will be read from the fitted models."
   - Padding.
3. "Each of these parameters can therefore change afucosylation, in a direction that the models will show."
   - Hedged filler. The phrase "the models will show" recurs in two more sentences (Q1-3, Q1-4).
4. "The production bioreactor sets this load, and the purification steps clear it."
   - Says nothing a reader would miss.
5. "A longer culture is therefore expected to lower galactosylation and to raise aggregate, host cell protein and residual DNA."
   - Restates the galactosylation, aggregate and cell lysis paragraphs above it.
6. "A higher culture temperature or a higher culture pH speeds deamidation and aggregation."
   - Restates earlier paragraphs. It also adds a temperature effect on aggregation that the aggregate paragraph did not claim.
7. "Dissolved carbon dioxide crosses the cell membrane and lowers the intracellular pH."
   - Restates "pCO2 lowers the intracellular pH" from earlier in the same section.
8. "The initial viable cell concentration acts on aggregate through the antibody concentration."
   - Restates the aggregate paragraph.
9. "The Version 1.0 limits were applied at analysis and appeared in no approved plan (INV-001 finding 1)."
   - The third statement of this fact. The other two are in Section 1.1 and in note a of Table 1.1.
10. "The precision of each method contributes to the spread of the replicated centre points."
    - Textbook filler.
11. "The replicated centre points of the screening and response-surface designs estimate the pure error of each design, and they show whether curvature is present."
    - Made three times, in Sections 5.4, 5.5 and 6.2.
12. "The judgement over the NOR is whether the output meets its criterion at all 81 combinations of NOR low, set-point and NOR high of the 4 response-surface factors."
    - A word-for-word repeat of Section 5.1 item 3.
13. "The design space of the step comes from the response-surface model, like every prediction and every PAR (PCMP-001 §6.2)." and "A quality attribute is judged on a single batch, not on the mean prediction (Section 5.5)."
    - Section 7 item 6 sets no criterion. It restates Section 5.5 and item 3.
14. "The draw assumes that each half of the NOR spans 3 standard deviations of routine variation."
    - Restates the sentence before it.
15. "A wider criterion does the opposite." and "The aggregate criterion in force is stricter than the a priori criterion, although the low-pH bound widened it."
    - Padding, and a restatement of the sentence that ends the previous paragraph.
16. "Osmolality and the 4 univariate parameters are not factors of the response-surface model, and no PAR is computed for them from it."
    - Restates Section 6.3 and Section 7 item 5.

## Q7. Which sentences need the rest of the document to be understood?

| # | Sentence | What it should name instead |
|---|---|---|
| 1 | "The judgement over the NOR in the qualification uses the exact 95 % prediction interval of a single run (Section 5.1)." | It uses a label only. Name the check: whether the output meets its criterion at all 81 NOR combinations. |
| 2 | "A model that fails the lack of fit test or the limit on overfitting …" | "The requirement that predicted R² be within 0.20 of R²". |
| 3 | "That rule changed the criterion of this step for aggregate." This sentence opens a paragraph in Section 7; the same sentence is in Section 1.1 item 2. | "The verification rule of PCMP-001 §7.5". |
| 4 | "The change moves risk between the producer and the patient." | The subject is abstract. Name "replacing a platform worst case with an A-Mab bound". |
| 5 | "Item 5 of Section 7 states what this plan sets for their ranges." | It uses a label only, and item 5 sets nothing. Say "This plan sets no decision rule for their ranges; PCR-003 states its approach." |
| 6 | "INV-002 changes nothing in this plan." | "The investigation of the response-surface models that failed the adequacy criteria". |
| 7 | "The interference that led to AMD-001 is host cell protein that elutes in the low molecular weight window of SEC." | "The decision to measure fragments by nrCE-SDS". |
| 8 | "QA opened INV-001 on 2026-08-03 after its review of the master report PCMR-001 Version 1.0 for BLA readiness." *(low)* | "The investigation INV-001". |
| 9 | "RA-001 gives the scores and the rationale for each assignment, and they are not repeated here." *(low)* | "The risk assessment RA-001". |
| 10 | "PCMP-001 sets no qualification rule for an output that has no adequate response-surface model, and this plan sets none." *(low)* | "The master plan PCMP-001". |
| 11 | "Criticality was assigned with Tool #1 of the A-Mab case study (CMC Biotech Working Group 2009)." | What Tool #1 is: a criticality score, the product of impact and uncertainty. |
| 12 | "The preventive action PA3 of the QA investigation INV-001 requires this of every study record." | Replace "this" with "a record of the execution window and the calibration status". |
| 13 | "The bioreactor report PCR-003 reports what the screening showed, and it records the later osmolality study S-BRX-OSM as discrepancy PD-003-01 from this plan." | What S-BRX-OSM did. |

## Table observations

**Headers that run together or are ambiguous**

- **Table 4.1.** The first column is headed "CQA", but it lists acidic variants and residual DNA. The text calls both very low criticality and not critical.
- **Table 7.1.** The header "Downstream worst case (platform or verified)" does not say which cells are platform values and which are verified. Only notes a and b on the Basis column tell.
- **Table 1.1.** The table says "R1, margin 6.8" where the text says "a safety factor of 6.8". In the R1 legend, "nominal back-calculation / margin", the slash can be read as "or" or as "divided by".
- **Table B.1.** The columns run A, B, E, C. Table A.1 and Table 6.2 run A, B, C, D, E, so the C column is easily read as E.

**Constant columns**

- **Table 5.2.** Both design columns hold one merged value per row ("SEC", "not in scope"). The whole table restates one sentence.
- **Table 11.1.** "Equipment" (EQ-BRX-205) and "Next calibration due" (2026-06-14) are one merged value for all four studies. The information that would vary, the previous calibration date and the as-found result, is missing.
- **Table 7.1.** "Clearance factor" is 1.00 and "Increase" is 0.00 in all three glycan rows. That is acceptable as data, but the single combined pair hides which downstream steps contribute.

**Missing units or definitions**

- **Table 6.1.**
  - No time basis is given for osmolality: initial, held, or peak.
  - The unit "× standard" does not say which standard concentration.
- **Table 4.1.**
  - "G1+G2 equiv." is not defined.
  - "Tool #1" has no scale.
  - Residual DNA "≤ 0.001 ng/dose" is 1 pg per dose. That is 100 to 10,000 times below the usual limits of 100 pg to 10 ng per dose. Check the unit.

**Footnote markers with no note, or notes with no marker**

- **Table 7.1.** The note "Computed from unrounded values. A criterion recomputed from the rounded values shown can differ in its last digit." has no marker anywhere in the table. I checked the raw text and the image. The note applies to the aggregate criterion: 5.00 × 1.40 − 0.56 = 6.44 against the 6.46 shown.
- **Table 5.2.** Note a says "this study" (singular, past tense), but the table covers two planned designs.
- **All other markers match their notes:** a–c, R1 and R2 in Table 1.1, and a–c in Table 7.1.

**Codes with no legend**

- **Table B.1.** The codes A, B, C and E are not referred to Table 6.2. Only D is explained in the text. The text before Table A.1 does refer to Table 6.2.
- **Table 3.2.** SOP-3016 is paired with AMV-3021. Every other pair of procedure and validation shares its number (3010, 3011, 3013).

**Values in a table that disagree with the text**

- **Revision history.** It says "re-analysis of the studies" and "Reissued under … INV-002". Section 1.1 says "INV-002 changes nothing in this plan" (Q5-6).
- **Table 7.1, acidic variants.** An increase of 1.00 applied to both limits gives 17.0–39.0, not the 18.0–39.0 shown. The text explains the difference; the table does not (Q5-8).
- **Table 7.1, note b.** It leaves out the condition "on an adequate model", which both Table 1.1 note c and the text state.
- **Table 3.2.** "Titre" in the table, "titer" in Section 5.2.
- **Precision.** Table 4.1 gives "2–13 %" where Tables 1.1 and 7.1 give 2.00–13.0. This is cosmetic.

## Other observations (not counted against a question)

- **Equal variance across scales.** Section 5.1 pools the SD of the two scales. Section 8 uses the residual SD of the scale-down runs for a single batch at manufacturing scale. Both assume the run-to-run variance is the same at both scales, and Section 12 does not list this assumption.
- **The offset uncertainty is not carried into the PAR.** Section 8 subtracts the point estimate of the offset. The 90 % interval from Section 5.1 is used only for the NOR check, so a PAR edge can shift by the width of that interval with no test.
- **Host cell protein is excluded on a procedural ground:** "because neither has a criterion at this step". The plan says plainly that it does not assess the effect of culture duration on the host cell protein load, which the remit allows. As a result, the classification of culture duration ignores an effect that Section 4.1 predicts.
- **Osmolality is left out of the response-surface design without a reason.** Section 4.1 expects osmolality to raise high mannose, the only attribute of very high criticality. Yet osmolality is the one multivariate parameter left out of the response-surface design, and no reason is given beyond PCMP-001 §6.1.
