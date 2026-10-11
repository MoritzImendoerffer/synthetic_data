# Readability review of PCR-008 Version 2.0, after fix pass 1 (2026-10-11), medium effort

Saved by the coordinator from the agent's hand-back.

# Review of PCR-008 (anion exchange, Version 2.0 draft)

**Reviewer model:** Claude Opus 5.5 (claude-opus-5-5).

I read only the draft text file and changed nothing. I spot-checked the key numbers by hand. These all reproduce from the coefficients and appendix tables:
- the least favourable XMuLV and MVM means (5.86, 4.24)
- the host cell protein set-point and NOR range (15.3, 10.7 to 21.9)
- the design-space edges (6.85 and 6.72 mS/cm) and the 4.96 % MVM exclusion
- the flow-rate t-tests
- the centre-point statistics
- the 1,337 candidate count
- the widening arithmetic (16,719 and 418; 3.08-fold)
- the 0.15 % upper bound
- the z = −2.57 test

## Q1. Is a physical cause named where a cause is given?
- "Load pH and the conductivities act on the same binding equilibrium from opposite sides. For this reason PCP-008 §4.1 expected the effect of Equil/Wash-1 conductivity on host cell protein to depend on load pH." (§2.1). Two factors acting in opposite directions does not imply that they interact. No physical cause for the interaction is named.
- "Fragments are expected to leave the step at the level at which they enter it, because on the platform no step after cation exchange changes the fragment level" (§2.1). The cause given is platform history, not physics. It should say that fragments carry the antibody's positive charge and flow through.
- "Operating flow rate was assessed one factor at a time, because binding of the small, highly charged impurities is fast relative to the residence time..." (§2.3). Host cell proteins and DNA are not "small" as a class. The sentence also ignores virus, which §2.1 calls the species most likely to respond to flow rate.
- "The cause was a set-point in the method that was slightly permissive." (§13.1.2). This names no physical cause, and the direction is doubtful (see Q5).
- "Residence time is the route by which flow rate could act on viral clearance" (§9). The mechanism, slow diffusion of virus particles to the ligand, is not stated in this clause.

## Q2. Is every technical term a term of art?
These are coined or local terms, not terms of art:
- "NOR-propagated range"
- "PAR (set-point)"
- "platform worst case"
- "single-batch limit"
- "design-space fraction"
- "spread p" / "spread regression" (Table 5.4)
- "deciding statistic" (§6)
- "completion rule" (PD-008-08, §13.2)
- "study event"
- "clearance factor shown" (Table 5.11)
- "each governed quality attribute" / "each attribute it governs" (§1.2)
- "near-equivalent models" (the literature says "models with substantial support, ΔAICc < 2")

"Equil/Wash-1" is a local abbreviation, but it is defined.

## Q3. Does any sentence tell the reader how to file a finding?
- "Characterization of A-Mab therefore confirms and bounds known behaviour." (§2.1). Renames the section as a category.
- "This report cites that number and does not recalculate it." (§4.3). Answers an objection nobody raised.
- "None of them decides an acceptance." (§3.5.7, repeated in §13.2). Same.
- "so the choice of plotted parameter is not a ranking." (§7.3). Same.
- "The rule of PCMP-001 §7.5 does not ask for the offset interval, and the bound in force is the one the rule gives." (§7.5). A defensive gloss.
- "Protein load was classified as a WC-CPP on the selected model, which decides." (§9). Also "...it stays in the selected model, which decides the judgements of this report." (§5.3.2). The trailing "which decides" is a filing gloss.
- "Its data confirm the cause and serve no other purpose." (§11).
- "A range that reaches the end of the characterized range is reported as reaching it, and no claim is made beyond it." (§7.3).

## Q4. Is every criterion stated with its basis, and every result reported as met or not met?
The step criteria (Table 7.1), adequacy, scale-down qualification, capability and verification are all stated with a basis and reported as met. The gaps:
- "...and a statement against the completion rule of PCP-008 §7 item 8." (§13.2, PD-008-08). A criterion of the plan that is never stated and never reported as met or not met.
- "No numerical threshold exists either for how far inside its acceptable range a parameter must be held, so the margin between each NOR and its proven acceptable range is stated." (§9). "Well controlled" has no criterion. The margin is not actually stated for protein load or operating flow rate.
- "PCP-008 §7 sets no numerical limit for the release profile of the load. The record classes the first lot... as not representative" (§13.1.1). The judgement that the load is representative has no criterion.
- "This report judges it practically relevant for that reason." (§9). Practical relevance is judged with no threshold. This is disclosed.

## Q5. Is any statement wrong, or contradicted by a table in the same document?
1. **Table 7.3 against §1.4, §7.3 and the executive summary.** The text gives the MVM NOR-propagated lower edge of load pH as 7.2225. Table 7.3 prints 7.23, but to two decimals 7.2225 is 7.22. §5.3.4 ("between 7.2 and 7.23 for MVM") repeats the 7.23.
2. **§13.1.2, DEV-008-02.** "the trailing-edge UV set-point that ends pool collection was 180 mAU, against the corrected set-point of 120 mAU... slightly permissive." On a falling trailing edge, a higher cut-off ends collection earlier and collects less, so 180 mAU is more restrictive, not more permissive. Check the direction.
3. **§13.1.2 and §11.** "It therefore acts on all those runs alike and does not enter the estimated effects..." and "...so it cannot have created or hidden an effect within them." This is scientifically overstated. A fixed UV cut cuts off a different share of the trailing tail, which holds weakly bound host cell protein, at different conductivity and pH. The cut can therefore interact with the factors.
4. **§5.4.** "The data therefore show no effect of flow rate within the range studied" rests, for viral clearance, on one spiked run at 450 cm/hr. The lower end was not spiked. §7.4 states the narrower claim correctly.
5. **§9, protein load, against §5.3.2 and §3.5.2.** §5.3.2 says the protein load interaction is "not established as an effect of protein load". §3.5.2 says a feature carried by only some near-equivalent models "is not treated as an established effect". §9 still classifies protein load as a WC-CPP, on a judgement that this same effect is practically relevant. The conservative class is defensible, but the reasoning is internally inconsistent.
6. **§7.5 against Table 7.2.** "Within the NOR the lowest predicted clearance factor is 5.40." From Table 7.2, 117.0 / 21.9 = 5.34. The text says the 28-run model is used, which explains the gap, but the reader is not told the two values differ. Similarly, the "lack of fit p-value of 0.824" in §7.5 sits beside 0.842 in Table 5.4. These are different models, but the swapped digits look like a transposition and should be checked.
7. **"Upper 95 % limit of a single run" (executive summary, §7.2, 29.4 ng/mg).** §3.5.5 says this is the upper end of a two-sided interval, so a one-sided 97.5 % limit. §7.5 uses a "one-sided 95 % prediction bound" (4.18-fold, about 28 ng/mg). Two different "95 %" upper limits appear unreconciled.
8. **Table 2.1.** The viral clearance attributes (VH) have Tool #1 scores of 20, below host cell protein (M-H) at 36. The footnote ("very high by rule") explains it, but the table reads as contradictory.
9. **Residual DNA criterion of ≤ 0.001 ng/dose (Table 2.1, §5.5).** This is about 10,000-fold below the usual 10 ng/dose limit (WHO/FDA). It is scientifically implausible as a drug substance criterion. This is a configuration issue, but the document states it as fact.
10. **§7.5, item 2.** The ELISA "detects 80 % of the host cell protein species". The argument that the risk falls on the producer does not address the 20 % of species that release testing cannot detect, which is a patient risk.
11. **Executive summary.** "The log reduction factors (LRFs) of both viruses depend on load pH and load conductivity." This omits the protein load term in the selected XMuLV model (Table 5.3).
12. **Table 3.1, minor.** The peak asymmetry offset is printed as 0.03, but the means printed are 1.22 − 1.20 = 0.02. Likely rounding.

## Q6. Which sentences read as machine-written?
- "These replicates are the pure error against which lack of fit is tested." (§5.1). Restates §3.1 almost word for word.
- "The standard deviations of the LRFs at the centre point... compare with a repeatability of the infectivity assays of 0.3 and 0.32 log10." Hedged: "compare with" never says whether they are larger.
- "The spiking runs were made in the same scale-down model as a small-scale spiking study" (§3.1). Garbled.
- "A WC-CPP is a critical process parameter, so the step has five critical process parameters, all well controlled." (§9). Restatement.
- "The range rests on the assumption that the effect of flow rate does not depend on the other parameters, which a univariate study cannot test." (§7.4). The same point appears three times (§4.4, §7.4, §11).
- "The results are analysed as recorded." / "The runs of the re-executed designs are analysed as recorded." Says nothing a reader would miss.
- The narrative paragraphs after Table 13.2 (PD-008-04 to PD-008-09) largely repeat the table and §3.1 to §3.5. Example: "The coding of protein load, PD-008-09 (Section 3.5), placed coded 0 at 175 g/L resin..."
- "The last records the approaches this report states where the plan sets no threshold, and the analyses it adds." (executive summary). Clumsy, and "the last" seems to point at "the coding of protein load".
- "...by 2D western blot against the platform CHO host cell protein antigen" after "species of the platform antigen" (§7.5). Redundant.

## Q7. Can each sentence be understood on its own?
- "This Version 2.0 is issued under the investigations INV-001 and INV-002." (executive summary). Should name what each found: criteria set after the data were reviewed, and response-surface models below the adequacy criteria.
- "...augmented by 12 runs, a number INV-002 calculated." Should name the model adequacy investigation.
- "They measured no viral clearance, because INV-002 spiked no virus in an augmentation." (§3.4). An investigation does not spike. Should say the augmentation design decided by the model adequacy investigation included no spiked runs.
- "The screening run of DEV-008-03 is not identified in the record." (§11). Should say "the screening run made with the equilibration buffer below its pH range".
- "...under the method decision AMD-001 of 2026-03-20" (§1.4) and "because it ran before AMD-001" (§13.1.1). Should name the decision: nrCE-SDS for fragments.
- "...a statement against the completion rule of PCP-008 §7 item 8." Should say what the rule requires.
- "These two models have no F-test, and on the reading of Section 3.5 the first criterion does not apply to them." (§5.3.1). Should name "the model F-test criterion".
- "What it changed was computed (Section 5.3.3)." (§13.2). Abstract subject. Should say that the effect of the augmentation on each selected model and judgement was computed.
- "...on the model selected on the 28 planned runs, the runs on which the criteria were fixed when INV-001 closed." (§7.5). Unclear. §7.1 says the criteria use no study data, so this should say what was fixed on those runs.
- "By the rule the bound replaced the platform value." (§7.5). Should name "the widening rule of the master plan".

## Answers for the document as a whole
1. No
2. No
3. Yes (sentences of this kind are present)
4. No
5. Yes (statements are wrong or contradicted by tables)
6. No (sentences flagged)
7. No (sentences flagged)

The most consequential items to fix:
- the direction of the DEV-008-02 UV set-point, and the claim that it "cannot have created or hidden an effect"
- the 7.2225 vs 7.23 mismatch in Table 7.3
- classifying protein load as a WC-CPP on an effect the report itself calls not established
- the completion rule, which is cited but never stated or reported against
