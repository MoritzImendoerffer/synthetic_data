# Readability review of PCR-004 Version 2.0, after fix pass 1 and the data-state pass (2026-10-11), medium effort

Saved by the coordinator from the agent's hand-back.

# Review of PCR-004 (Harvest and Clarification, Version 2.0 draft)

**Reviewer model:** Claude Opus 5.5 (claude-opus-5-5). I read only `/home/moritz/github_repos/synthetic_data/.claude/work/2026-10-08_01_rev2-campaign/PCR-004_harvest.DRAFT.txt`. I changed nothing and wrote no file.

Most numbers in the text check out against the tables when I recomputed them: set-point means, resolutions, NOR changes, Cpk values, the 8.2 log10 DNA reduction, and the hold changes. The real problems are a few internal contradictions (Q5), heavy repetition (Q6) and labels used without saying what they mean (Q7).

---

## Q1. Is a physical cause named where a cause is given?

Almost every causal clause names a physical cause: proteases, settling velocity, charged media sites, void-space filling, deamidation rate. Four sentences use "sets" or "decides" with no mechanism in the clause:

- "The centrifugal field sets how much turbidity reaches the depth filter, and most of its effect lies below the set-point." (§11) "Sets" names no mechanism. It should say that settling velocity rises with the field.
- "For the operation of the step this means that the parameters of harvest decide the clarity of the feed to capture, while the time and the temperature of the hold decide how far fragments and acidic variants rise before capture." (§5.7) "Decide" twice, with no species or direction. The protease and deamidation causes are in the sentences before it, not in this one.
- "What it decides is the condition of the feed to Protein A capture." (§1.1) The verb is vague and no cause is given.
- "...because SEC reads fragments high wherever the sample still carries host cell protein." (§3.3) It names the species but not the interaction: host cell protein co-elutes in the LMW region.

## Q2. Is every technical term a term of art?

- "resolution of the turbidity method ... 6.30 NTU" (§5.2, and "resolution" throughout, defined in §3.5 as 2.77 × SD). In analytical chemistry "resolution" means peak separation or instrument resolution. The quantity defined is the repeatability limit or critical difference (ISO 5725, 2.8σ).
- "the reading of the change over it" (exec summary, §3.5, §11, PD-004-02). Not a term. It means the rule for computing the hold change: the largest change from day 0.
- "the level that enters the hold" / "the level expected to enter the hold". This is a coined label. It means the worst-case starting level of the hold.
- "the 4 runs at the full set-point" (§3.5, Table 5.3 note). "Full set-point" is coined. It means runs with every parameter at set-point.
- "set-point centrate" (heading of PD-004-06 and Table 13.2). A coined compound.
- "a priori value of ≤ 9.30 %" (§2.2). Not explained and not a standard term in this context.
- "Host-Cell-Protein Quantitation by ELISA", "Residual Host-Cell DNA" (Table 3.1 titles). Coined hyphenated compounds.
- "integrated model of the train" (§3.5, §8). Used as if standard and never defined. It should say what it is: a Monte Carlo propagation of the step models.

## Q3. Does any sentence tell the reader how to file what it has just said?

- "Within normal operation that exposure is brief, so an effect on aggregate is a mechanism to check, not an expected one." (§2.1) A trailing category label.
- "Version 1.0 gave no result for any parameter effect, so its conclusions can be compared with those of this revision only as conclusions, not result by result." (§1.4) A gloss on how to compare.
- "S-HAR-UNI2 is a univariate study, not a designed experiment, and no multivariate model is fitted to it." (§4.2) Re-files a study already described.
- "The claim of the study stops at that pool, those two temperatures and that time." (§4.3) Scope filing.
- "That part of the assumption remains an assumption, and the criteria ... rest on it." (§5.5) Renames the finding as a category.
- "The verdict at the lower limit does not depend on the hold, because the level that enters it already fails." (§5.6) Restates the sentence before it as a verdict category.
- "...so this is an expectation and not a result." (§5.7) Files the statement. It is acceptable as a caveat, but it is still a filing clause.
- "It lies outside the NOR, so the data do not contradict the NOR." (§7) Answers an objection nobody raised.
- "A turbidity at that limit is the cleanest clarified harvest of the range, and no criterion binds there." (§7) Answers an objection nobody raised.
- "Indices this far above the target confirm a large distance from each limit and decide nothing at this step." (§8) A gloss on how to read the Cpk table.
- "That monitoring is a control of the production bioreactor." (§10) Files the monitoring under another step.
- "Movement within a NOR is routine operation." (§6) Boilerplate filing.

## Q4. Does every criterion have its basis, and is every result reported as met or not met?

Mostly yes. Every result is reported against a criterion. The hold approach is openly declared as chosen after the data. Host cell protein and DNA are correctly reported as having no criterion. Two exceptions:

- "Post-clarification turbidity is compared with the upper limit of its NOR, 10 NTU." (§7 criterion 2, and the Table 5.2 note) The basis given is the NOR itself, which is circular. No link to Protein A fouling or capacity is given for the 10 NTU value.
- In Table 7.1, the "Result closest to the criterion" column reports p-values (HCP p = 0.122, aggregate p = 0.379, residual DNA p = 0.376). These are the residual-error sensitivity values from Appendix B. They are not the primary test of §3.5 and Table 5.3 (0.107, 0.466, 0.524). The table never says which error term it uses.

## Q5. Is any statement wrong or contradicted by a table in the document?

1. **Table 7.1 vs Table 5.3.** Table 7.1 gives "Host cell protein, p = 0.122", "Aggregate, p = 0.379" and "Residual DNA, p = 0.376". Table 5.3, the stated primary analysis, gives 0.107, 0.466 and 0.524. The values in Table 7.1 come from Appendix B (residual error), which §3.5 calls a sensitivity analysis only.
2. **Turbidity PAR of 1–20 NTU vs the 10 NTU clarification criterion.** "The proven acceptable range of post-clarification turbidity ... is 1–20 NTU" (exec summary, Table 7.1, §12). Yet "A setting that delivers clarified harvest above that value [10 NTU] has failed to clarify" (§7). The depth filter load PAR is cut at 140 L/m2 because 10.7–11.0 NTU fails. The same document then accepts up to 20 NTU as proven acceptable. §10 also monitors against 1–10 NTU. These cannot all hold.
3. **Table 13.2 (PD-004-01) vs §1.2, §3.4 and PD-004-04.** The table says S-HAR-UNI2 "measured fragments and residual DNA, which the plan did not name as responses". But PCP-004 objective 2 (§1.2) names "host cell protein and DNA", and PD-004-04 says the plan sampled "for host cell protein and DNA". The prose of PD-004-01 names fragments only.
4. **Fragments as clipping only (§2.1, §5.7).** "Fragments are clipped antibody, mostly cleaved in or near the hinge..." and "Clipping is set by the protease ... not by the field..." This leaves out disulfide reduction during harvest and hold. That is a well-known harvest-specific source of LMW species measured by nrCE-SDS: cell lysis releases thioredoxin and reductase, and it depends on shear and lysis, so on the field. It is relevant because the conclusion "not by the field" rests on mechanism.
5. **Model vs Table 5.4.** "The process model at set-point carries 1.10 % fragments at the end of culture and 1.12 % in the clarified harvest after a hold of one day at 2-8 °C..." (§5.5, §8). That is +0.02. Table 5.4 shows +0.23 in day 1 at 2-8 °C (1.00 to 1.23). The text says nothing about the gap.
6. **The 2-8 °C fragment rise is computed two ways.** "Over 7 days fragments rose 2.6 times as much at 21 °C as at 2-8 °C" (§5.6) uses the day 0 to day 7 change of 0.21. Table 5.5 uses the largest change, +0.24, which gives a ratio of 2.3.
7. **The hold claim in §10 vs §3.5.** "The hold study supports a hold of up to 7 days at 2-8 °C or at 21 °C for aggregate, fragments..." But §3.5 says the fragment level entering the hold "is therefore not the highest level expected in routine manufacture". Also, supporting a 7-day hold of clarified harvest at 21 °C with no bioburden or endotoxin data is scientifically unsound.
8. **"Far from binding" vs §8.** "...it describes the condition of the feed even where its own criterion is far from binding" (§2.2, residual DNA). §8 says the train must remove about 8.2 log10 of DNA against 9 log10 credited, a margin of about 0.8 log. The criterion "≤ 0.001 ng/dose" (Table 2.1, Table 8.1) is 1 pg/dose. That is about four orders of magnitude below the usual 10 ng/dose expectation and is probably a unit or value error.
9. **The GPP class.** "Post-clarification turbidity was classified as a GPP" (§9). §9 defines a GPP as a parameter that "affects neither" a CQA nor process performance. But §2.1 says turbidity fouls the Protein A bed, and the effect on capture "was not measured". Not measured is not the same as no effect, so the class contradicts its own definition.
10. **The level-mean fall (minor).** "centrate turbidity changed by −78.7 NTU" (§9) and "the fall of 78.7 NTU" (§5.2). The level means in Table 5.2 give 122.5 − 43.95 = 78.55. This is probably rounding, but it does not reproduce from the table.
11. **The control does not protect anything (minor).** "...and it protects the Protein A resin from fouling" (§10). A turbidity test detects high turbidity. It does not protect the resin unless an action is defined for a failed result.

## Q6. Which sentences read as machine-written?

- PD-004-07: "None of them is in the record, because none was entered in the study record." A tautology. The same circular reason appears in Table 13.2 ("not entered in the study record", "not scheduled in the study record") and in PD-004-04 and PD-004-05.
- "Table 3.3 shows the methods of the designed studies of the campaign at this step, of which there are none." (§3.3) A sentence and a table that say nothing.
- "The level expected to enter the hold and the reading of the change over it are this report's approach, chosen after the results were known." This is repeated almost word for word in the exec summary, §3.5, §11, §12 conclusion 4, PD-004-02 and Table 13.2.
- "PCMP-001 Version 2.0 judges a held pool against the criteria it must meet on entering the next step." Repeated four times.
- "No result of that study enters this report, so neither bears on its conclusions." Repeated in the exec summary, §4.2, §11, §12, §13.1.1 and §13.1.2.
- "Every parameter effect, proven acceptable range and class ... rests on S-HAR-UNI2." Repeated in §1.4, PD-004-01 and §11.
- "The conclusions roll up into PCMR-001." It appears twice in the exec summary, then again in §10 and §12.
- "The record does not name the culture from which the pool was made." Repeated in §4.3 and §5.6.
- "This report presents the study that PCP-004 planned, the further work of the Version 2.0 re-analysis and their outcome. It is the paired report of PCP-004." (§1.1) Padding.
- "Judged that way, the level expected to enter the hold plus the largest change over it met the criteria..." (exec summary) Stacked abstractions.
- "Each narrows what the study supports, as Section 3.2, Section 3.4 and Section 4.2 state." (§11) Padding.

## Q7. Can each sentence be understood alone?

- "Version 1.0 recorded two study events in S-HAR-UNI, DEV-004-01 and DEV-004-02." (exec summary), "The 2 study events of S-HAR-UNI have no bearing..." (§11) and "The study events DEV-004-01 and DEV-004-02 have no bearing..." (§12 conclusion 7). These should name the events: a high depth filter flush turbidity and a post-clarification turbidity excursion.
- "Objective 4 was met in part." and "Objective 5 was met, within the limits stated in Section 7." (§1.2) These should name the objectives: the effect on size variants and turbidity, and the definition of the PARs and classes.
- "S-HAR-UNI2 supplies every parameter result. S-HAR-HLD supplies the hold judgement..." (§11) These should name the studies: the univariate study of 2026-09 and the 7-day hold study.
- "Three of the discrepancies from the plan change what the report rests on." (§11) An abstract subject. It should name them: the new univariate study, the hold study and the unqualified scale-down model.
- "The other discrepancies narrow what the study supports, and PD-004-08 records the rules..." (§11) The code is used alone. It should name the rules the plan left open: method resolution, fit statistics, the turbidity range decision and the combining of filter series.
- "The judgement of the held pool therefore rests on the changes over the hold, added to the levels expected to enter it..." (§5.6) An abstract stand-in. It should name the worst-case starting level from the bioreactor prediction interval.
- "...which the runs of S-HAR-UNI2 did not have." (§5.5) The referent is unclear. It should say whether the runs lacked the one-day cold hold or the level.
- "The aggregate criterion is stricter than its a priori value of ≤ 9.30 %." (§2.2) It should say where 9.30 % comes from: platform worst-case values.
- "The unqualified model places every result at the scale of the study." (§11) An abstract subject. It should say that the results have no known offset from manufacturing scale.
- "The capability of the drug substance comes from the integrated model of the train (PCMP-001 §6.5)." (§3.5, §8) It should name the method: a Monte Carlo simulation through the step models.

---

## Yes/no answers

1. Causes named physically: **No.** Mostly compliant, but four "sets/decides" sentences give no mechanism.
2. All terms are terms of art: **No.**
3. Filing or objection glosses present: **Yes.**
4. Every criterion has its basis and every result is met or not met: **No**, narrowly. The 10 NTU basis is circular, and the Table 7.1 p-values come from the wrong error term.
5. Any statement wrong or contradicted by a table: **Yes.** The main ones are Table 7.1 vs Table 5.3, the turbidity PAR vs the clarification limit, Table 13.2 on residual DNA, and the DNA criterion value.
6. No machine-like sentences: **No.**
7. All sentences understandable alone: **No.**