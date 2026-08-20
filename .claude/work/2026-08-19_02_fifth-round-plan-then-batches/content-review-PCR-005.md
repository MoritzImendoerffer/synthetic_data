# Content review of the PCR-005 draft — before promotion

**2026-08-20, TASK-016 §4.** Batch B2, authored under the amended rule 4 of `WRITING_GUIDE.md`.
Protein A chromatography has a DoE, so the document is a `report_doe`. §5c of the brief assigns no
registered discrepancy; D-001 does not bite here because for `protein_a` the design centre
coincides with the set-point for all four RSM factors, and §3.5 says so.

Two fresh judges (`opus`, self-reported Claude Opus 5 both times), the four Content questions
verbatim, the rendered PDF and nothing else, with one return to the author in between.

## Run 1 — as authored (`PCR-005.DRAFT.pre-review.qmd`, 47 pp)

**Q1 No · Q2 No · Q3 No · Q4 Yes.** Flags: Q1 14 mechanism-bearing + 7 procedural, Q2 4, Q3 7, Q4 19.

### Q1, group A — mechanism-bearing uses that fail

- "Pool host cell protein is governed by protein load and by elution buffer pH." (Exec summary) — names two parameters, not a species, and the direction arrives only in the next sentence.
- "The step sets one critical quality attribute, leached Protein A, and it delivers the principal removal of host cell protein and of DNA in the train." (§1.1) — "sets" takes an administrative object.
- "The physical chemistry of the step sets the expectation against which the results were read." (§2.1) — "sets" takes an abstract object.
- "Load and elution pH therefore act on the same quantity, the impurity burden carried into the eluate…" (§2.1) — names a quantity rather than a species, and gives no direction.
- "Protein load and elution buffer pH were ranked highest because both act directly on the impurity burden of the eluate." (§2.3) — "directly" does the work a mechanism should.
- "Load flow rate and end of pool collect were included because both act on yield and both can interact with load through the mass transfer zone." (§2.3) — the mass transfer zone is invoked without saying what it does.
- "A full factorial was used rather than a fraction because four factors cost only 16 factorial runs, and because the interaction … was expected on mechanistic grounds…" (§4.2) — "on mechanistic grounds" defers the mechanism to a phrase.
- "…they were retained because both act on yield and because dropping a factor from the design would have held it at its set-point and hidden any curvature it carries." (§4.3) — third "act on yield".
- "Temperature acts on the diffusion coefficient of the antibody and on the strength of the hydrophobic contacts at the interface between the Fc region and the ligand…" (§4.4) — names species and interaction but never a direction. Same gap in "Bed height at a fixed linear velocity sets the residence time and the pressure drop across the column".
- "Step yield is governed by the end of pool collection." (§5.2, repeated in §5.3) — direction and size come only in the following sentence.
- "The end of pool collection acts on the impurity ratio through the denominator." (§5.4) — the judge's "strongest instance": points at a mathematical object.
- "The design space is therefore set by one response and by the two parameters that govern it." (§6)
- "Two parameters govern the impurity burden of the eluate, protein load and elution buffer pH, and they act together rather than separately." (§11)
- "The capture step governs three process impurity attributes of the drug substance." (§2.2, recurring in Exec summary, §8, §12) — a scoping statement.

### Q1, group B — the judge's own heading: "procedural because clauses (strictly failing the same test, though no physical cause is at issue)"

Seven, including "It is not applied in this report, because no viral clearance is claimed for this
step." (§1.3), the two acceptance-criterion clauses in §3.5, "That upper bound does not come from a
demonstrated effect of pH, because §5.3 found none." (§7), and the §10 pair-control sentence.

### Q2 — four

"binding response" / "the response that binds" (constrained-optimization sense, in a document where
binding means ligand binding); "mechanism of action" applied to temperature; "the impurity ratio …
through the denominator".

### Q3 — seven

"The surfaces follow from the physical chemistry of affinity capture." · "Yield behaves as the
transport argument predicts." · "Leached Protein A behaved as the leaching mechanism predicts." ·
"The curvature in elution pH has the same origin." · "Where there is little co-eluting impurity,
there is little to dilute." (near-tautology) · "That is the flattening the positive quadratic term
describes." · "The physical chemistry of the step sets the expectation against which the results
were read."

### Q4 — nineteen

Including "…which is what the leaching mechanism predicts within a single run.", "The margin is what
makes it a control rather than a break-even point…", "That diagonal is the interaction, and it is
the feature that constrains the design space in §6.", "…is a property of the mechanism and not of
the design.", "The absence of a detectable parameter effect is therefore the expected result and not
a failure of the design.", "The right panel of Figure 7.2 is the one that carries the finding of
this section…", "That index is the one to read for this step…", "The useful statement for leached
Protein A is the margin rather than the index.", "The absence of a critical process parameter
reflects the control capability of the step and not the absence of an effect.", "The result that
matters most for the control strategy is the one the two analyses of §7 disagree about.", "The
difference is not a discrepancy between two models."

## Disposition after run 1

Returned to the same authoring agent in one message: the four questions restated and the flagged
sentences with what each lacks, in the judge's words. Replacement terms the judge named were
stripped before sending. No count and no verdict was sent.

**The revision found two factual errors that no question asked about.** §1.1 had claimed the step
"removes more host cell protein and more DNA than any other step of the train"; by fold, cation
exchange clears more host cell protein (78-fold against roughly 55-fold), so the sentence would have
contradicted `PCR-007`. §13.2 had called the leached Protein A ELISA "the least precise of the
methods applied at this step"; AMV-3016 is 6.5 % against AMV-3012 at 9.5 %, so the claim was
backwards and contradicted the document's own §3.3. Both were corrected by the author in the same
pass. Forcing a clause to name a species and a direction is what exposes a sign error.

445 sentences / 9,922 words became 453 / 10,022; 47 pages both times.

## Run 2 — after the one revision cycle

**Q1 No · Q2 No · Q3 No · Q4 Yes.** Flags: Q1 3 (+3 documentary "govern" and 1 arithmetic noted for
completeness), Q2 3 (+1 borderline), Q3 2 (+1 noted), Q4 6 (+2 borderline).

The judge's preamble: "The document uses no causal 'since' and no 'acts through'. Most instances
pass cleanly and in the same clause (e.g. 'because binding at the ligand is limited by diffusion
into the pores of the bead'; 'because the polyanionic molecule does not bind the ligand and is
removed in the flow-through and the wash'; 'because a higher load leaves more host cell protein on
the bed at the end of the wash and a lower elution pH releases more of it with the product')."

### Q1 — three genuine

- "Because those quantities are held equal, the residence time and the number of transfer units of the small column match the commercial column, and the chemistry the antibody experiences is the same at both scales." (§3.1) — the because-clause contains only the anaphor "those quantities".
- "The two act on capacity in opposite directions and both are small across the range studied compared with the effects of load and pH." (§4.4) — "act on" carried by "the two" and an unsigned "in opposite directions".
- "The investigation did not resolve whether the error lay in the preparation of the buffer or in the release measurement of it, and it did not need to, because both readings lead to the same disposition for the reasons above." (§13.1) — defers to "the reasons above".
- Borderline: "The two act on the same weakly held protein, so the penalty for a high load is larger at a low elution pH than at a high one." (§11) — the species is in the clause but the direction is not. The judge notes the §12 twin passes.

The judge flagged three documentary "govern" sentences ("ICH Q5A governs the viral safety
evaluation…", "The controlled documents that govern execution and analysis are listed in Table
1.2.", "Preparation and release of the buffer are governed by SOP-2103.") explicitly "for
completeness, not as laundering", each having a concrete named agent.

### Q2 — three

"the undivided ceiling" (§3.5) · "assurance margin" (§3.5, "transparent and defined in place, but
it is not the term of art") · "carboxylate contacts" (§5.4). Borderline: "free ligand" (§2.1, §2.3),
ambiguous in a document where leached Protein A is discussed two paragraphs later.

### Q3 — two

"The capture step is now characterized to the depth the transfer requires." (§11) · "Within the
range studied bed height is a property of the packing rather than of the chemistry." (§4.4). Close:
"Both routes depend on how much antibody is bound and on how completely it is released." (§5.4).

### Q4 — six

"…which is a performance range and not a quality risk." (§8) · "Step yield is a process performance
attribute with no acceptance criterion, and it is reported without one." (§3.5) · "Pool host cell
protein is not robust in that sense, and it is the attribute the control strategy manages." (§8) ·
"Within the range studied bed height is a property of the packing rather than of the chemistry."
(§4.4) · "No numerical acceptance threshold for Cpk is set in this package, and none is asserted
here." (§8) · "The indices are reported with the mean and the criterion beside them, so the margin
can be read directly." (§8). Two borderline in §4.1 and §6.

## Counts per question

| run | Q1 | Q2 | Q3 | Q4 | verdicts |
|---|---|---|---|---|---|
| 1 (as authored) | 21 (14 + 7 procedural) | 4 | 7 | 19 | No · No · No · Yes |
| 2 (after one cycle) | 3 (+4 noted) | 3 (+1) | 2 (+1) | 6 (+2) | No · No · No · Yes |

## Disposition

One cycle only. The draft stands as revised and goes to the batch annex step with B2.

## Notes not acted on

The judge's run-2 Q1 list again includes sentences that fail only by the letter — the three
documentary "govern" clauses, which it says it flags "for completeness, not as laundering", and one
whose cause is arithmetic rather than physical. That is the same unscoped-question finding recorded
for `PCR-004` and in D8.

Four `nan` cells remain in the ANOVA table of this document, as in every DoE report in the corpus.
They come from `doe_report.py`'s `anova_lof_df`, which writes `np.nan` into the F and p columns of
the Residual and Pure error rows, where those statistics do not exist. Not authored text, not fixed
here, and recorded for a machinery proposal.
