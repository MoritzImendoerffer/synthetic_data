# Readability review of PCR-010 Version 2.0, after fix pass 1 (2026-10-11), medium effort

Saved by the coordinator from the agent's hand-back.

# PCR-010 review (UF/DF characterization report, Version 2.0)

**Model:** Claude Opus 5.5 (`claude-opus-5-5`).

**Document:** `/home/moritz/github_repos/synthetic_data/.claude/work/2026-10-08_01_rev2-campaign/PCR-010_ufdf.DRAFT.txt`. I read only this file, changed nothing and wrote no file.

**Arithmetic checks:** I recomputed the derived values against Tables A.1 and B.1. All of these agree within rounding:
- the Table 3.1 means and offsets, and the Table 5.1 set-point statistics;
- the extremes and margins (4.21, 4.22, 2.2, 1.9 and 18.3 pp), and the 24 runs inside the NOR;
- the corner sums (0.06 and 0.10 pp) and the "41 times" ratio;
- the leave-one-out offsets;
- the Cpk values, the 3/2000 bound and the DNA unit conversion;
- e^0.995 = 2.70 per diavolume, and 63 % removed per diavolume.

One small gap: Table 8.1 gives a normal tail of 821 per million for the acidic variants, but the rounded mean and SD give about 775. That is plausible from unrounded values.

---

## Flags by question

### Q1. Is a physical cause named, with its direction, in the clause?
- "TMP and the final DS concentration both act on the polarization layer at the membrane wall." The clause says neither how they act nor in which direction. The mechanism only comes in the next two sentences.
- "A change of aggregate is the same at both scales, because the aggregate offset is a constant difference." (Table 5.2 note.) The reason given is an assumption, not a physical cause. The offset was measured only at the set-point, so a constant offset across settings is asserted, not shown.
- "The investigation attributed the shortfall to the residual hold-up volume of the skid..." (13.1.2.) It does not say how hold-up lowers the final concentration, for example dilution by the recovery flush.
- "This report judges that effect not practically relevant, because it is too small to move aggregate appreciably within the PAR." (Section 9, for both TMP and final concentration.) The "because" clause just restates the rule. It gives no cause and no number.

### Q2. Is every technical term a term of art?
- "residual process buffer". This is not a standard term. The text admits that neither the species measured nor the method is named, so a reader cannot tell what it measures.
- "allowance" (e.g. "That allowance tightens the criterion..."). This is not a term of art in this sense. It means "the prediction bound of the aggregate rise added across the step".
- "Transmembrane-pressure excursion" (Table 13.1). This is a hyphenated coined compound.
- "topped up" / "top-up" (Table 13.1, 13.1.2). This is informal. The report itself notes that the correction was a further concentration.

### Q3. Does any sentence tell the reader how to file the finding?
- "That is a judgement and not the application of a rule, because no plan sets a threshold for it (PD-010-06). Section 9 uses it." (5.3)
- "That is a judgement, because no threshold was set before the data." (7.2)
- "That judgement was made with the data known." (7.3)
- "...so a class that rests on it is a judgement, and this report names it as one." (9)
- "The class of TMP rests on a judgement of practical relevance." (9)
- "Each rule was stated and applied with the data known, and each judgement that rests on one is named as a judgement where it is made." (13.2)
- "These three discrepancies limit what the record can show, and Section 11 states how they bear on its reading." (13.2)
- "An interval that includes zero does not show that the two scales agree." (3.1) This answers an objection nobody had raised yet.
- "The study record holds no release result for the formulation buffer, and this report claims none." (5.5) This also pre-empts an objection.
- "No result for a parameter effect existed when it was made, so none of its conclusions rests on runs added after a result was known." (4.2, repeated in 13.2) This is defensive filing, though INV-001 makes it partly relevant.

### Q4. Is every criterion stated with its basis, and every result reported as met or not met?
- "The buffer-exchange criterion of PCP-010 ... could not be judged as planned." (Executive summary, 5.5, 12.) This result is reported as neither met nor not met.
- "The plan passes a parameter over its range when ... the change measured across the range is small against the criterion. It leaves the threshold for a small change to this report." (7.2) This acceptance condition has no criterion set in advance, so it is judged without one.
- "The model is qualified for aggregate when that conclusion is the same with the offset at its estimate and at either end of its interval." (3.1) The report set this qualification criterion itself, after the data. Its basis is "keeps the logic of PCMP-001 §7.1" and nothing more.
- "At every edge the highest aggregate result lay at least 4.22 percentage points below its criterion ... This report judges that no attribute approached its criterion." (7.3) The threshold for "approaches" is set after the data.
- "PCMP-001 §7.9 sets a target Cpk of 1.33 and a minimum of 1.00." The basis is cited only as a plan section. The acidic-variant Cpk is reported as "acceptable" even though the report itself shows it would be 0.63 at the level the study measured.

### Q5. Is any statement scientifically wrong, or contradicted in the document?
- "A further diavolume only lowers the residual process buffer." (1.4 item 9, 4.1, 5.5, 10 item 3, Table 13.2 PD-010-07.) Section 4.1 contradicts it in the very next sentence: "It also adds time on the skid and passes through the pump, which could raise aggregate and the acidic charge variants". Section 2.1 says the same.
- "Above it, a higher TMP compresses the polarization layer and raises the concentration at the wall further, with no gain in flux." (2.1) In the pressure-independent regime the wall concentration sits at its limiting (gel) value. A higher TMP thickens or compacts the layer but does not raise the wall concentration further. The expectation that aggregate rises with TMP above the limiting flux therefore rests on a doubtful premise.
- "TMP was classified as a KPP. Its only measured effect is on aggregate, a CQA." (9) This conflicts with the KPP definition the report quotes in the same section ("affects process performance ... and has no effect on a CQA within its range"). It also conflicts with Table 5.2: TMP had no significant slope on step yield, final concentration or residual buffer, so it has no measured effect on process performance. Table 9.1 admits that flux is "from the mechanism. Not measured across the range". The final DS concentration likewise has a significant effect on a CQA (Table 5.2, p < 0.001).
- "The model-adequacy criteria of PCMP-001 §7.2 apply to response-surface models and do not apply here." (3.5) Section 7.1 then judges the main-effects fit by a §7.2 limit: "R² exceeds predicted R² by 0.15, within the limit of 0.2 of PCMP-001 §7.2". The report applies the criteria after saying they do not apply.
- "Residual DNA ... ≤ 0.001 ng/dose" (Table 2.1, Table 8.1), with a simulated mean of "0.00024 pg per mg of antibody". The criterion is about 10,000-fold tighter than the usual 10 ng per dose. The simulated level is orders of magnitude below what any residual DNA assay can quantify. This looks scientifically implausible, even if it comes from the register.
- "...and that no step after low-pH viral inactivation changes the acidic charge variants (PCMP-001 §7.3)." (7.1) This assumption conflicts with the report's own statements, in 1.1 and 2.1, that deamidation continues on the UF/DF skid. The report says the study "neither confirms nor contradicts" it, but its own mechanism contradicts it.
- "...with a standard deviation of one sixth of the width of its NOR..." (3.5) The number-of-diavolumes NOR is one-sided (≥ 7 DV) and has no width (Table 4.1), so the way that parameter is drawn is undefined. Section 7.1 has the same gap: "every combination of NOR low, set-point and NOR high" has no defined NOR high for diavolumes.

### Q6. Which sentences read as machine-written?
- "Section 9 uses it." (5.3)
- "The study does not show any of these directions at its precision." (5.4) This restates "No slope was significant".
- "The residual process buffer was still falling at the top of the range studied, as the exponential fall predicts." (5.5) This restates the sentence before it.
- "Operation within the NORs is routine." (6) It says nothing a reader would miss.
- "They do not support the movement of two parameters away from their set-points at the same time." (6) This restates the sentence before and the definition of a design space.
- "A PAR cannot be wider than the range studied." (7.3 limitation 3) This restates "Each PAR is the range studied, and no claim is made beyond it".
- "That is a judgement, because no threshold was set before the data." (7.2)
- "Each rule was stated and applied with the data known, and each judgement..." (13.2)
- "These three discrepancies limit what the record can show, and Section 11 states how they bear on its reading." (13.2)
- "A further diavolume only lowers the residual process buffer." This is repeated five times across the document.
- "The use of those offsets is accepted on that argument (PD-010-01)." (Executive summary)

### Q7. Can each sentence be read on its own?
- "Under rule 1 of PCMP-001 §7.5 the bound replaces the assumption of no change..." (7.1) It should name the rule, that a prediction bound measured in the campaign replaces a platform assumption.
- "PCMP-001 §7.5 checks the assumption on S-UFDF-UNI2, although..." (7.1) A plan section is the subject. It should say that this report checks the assumption of no aggregate change after cation exchange, using the univariate study data.
- "PCP-010 §4.3 keeps the rule of Version 1.0." (2.3) It should name the rule, that runs with two parameters at their edges are needed when an attribute nears its criterion.
- "...so the rule of PCP-010 §5.3 attributes neither to the assay." (5.3) It should name the rule, that a change larger than the pure error is not assay noise.
- "The register accepts this because..." (11) and "...which the register accepts with argument (objective i)." (12) "The register" is an abstract stand-in. It should say "the discrepancy entry for using the first skid's offsets on the second skid".
- "PD-010-03 leaves the change across the step unknown..." (13.2) It should name "the absence of load, pre-diafiltration and permeate samples".
- "PD-010-04 means that the randomized order..." (13.2) It should name "the missing execution records".
- "The rise of aggregate across this step moves a criterion upstream." (Executive summary) It should say that the aggregate criterion of the cation exchange pool is tightened.
- "That allowance tightens the criterion of the cation exchange pool..." (Executive summary) and "The allowance of Section 7.1 carries it into the criterion of the cation exchange pool." (9) They should name the 0.104 pp prediction bound of the aggregate rise.
- "Its implication for product quality is still carried, because the allowance of Section 7.1 includes it..." (9) This is an abstract subject. It should say that the TMP effect on aggregate is included in the 0.104 pp bound.
- "The approach of this report keeps the logic of PCMP-001 §7.1." (3.1) It should name the logic, that qualification is judged at the offset estimate and at both ends of its interval.
- "The lower limit of 18 % limits it." (Executive summary) "It" stands for the Cpk. The sentence should say that the Cpk is set by the distance from the mean to the 18 % lower limit.
- "Objective (iii) is not met." (5.5) It should name the objective, to find the number of diavolumes at which the retentate reaches the formulation buffer.

---

## Whole-document answers

| # | Question | Answer |
|---|---|---|
| 1 | Is a physical cause with direction named in the clause? | **No.** Mostly it is, but four clauses fail. |
| 2 | Is every technical term a term of art? | **No.** Mostly minor: "residual process buffer", "allowance", "top-up", and one coined compound. |
| 3 | Does any sentence file its own finding? | **Yes.** There are repeated "that is a judgement" glosses and pre-emptive defences. |
| 4 | Is every criterion stated with its basis and every result reported as met or not met? | **No.** The buffer-exchange criterion is unjudged, and the "small change", "approaches" and qualification rules were set after the data. |
| 5 | Is any statement wrong or self-contradicted? | **Yes.** "A further diavolume only lowers..." conflicts with 4.1 and 2.1. The TMP wall-concentration premise is doubtful. TMP as a KPP conflicts with the quoted definition and Table 5.2. §7.2 is applied after being declared inapplicable. The DNA criterion and level are implausible. The NOR width for diavolumes is undefined. |
| 6 | No machine-like sentences? | **No.** Eleven flagged. |
| 7 | Every sentence understandable on its own? | **No.** Thirteen flagged. |