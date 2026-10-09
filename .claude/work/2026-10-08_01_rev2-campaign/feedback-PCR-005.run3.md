# PCR-005, after review run 3 and factual check 2: what to change (one cycle)

Three inputs: the owner's comments (A), the factual check `factual-PCR-005.run2.md` (B) and the
content review `content-review-PCR-005.run3.md` (C). Read both files for the exact sentences. Where a
finding needed a check of the code, the data or the record, it was made before this list was written,
and the resolution is given: write to it. Every value stays computed.

## A. The owner's comments (2026-10-09)

The owner read the log-scale passage of INV-002, which says what yours says, and wrote: "Do not expect
that a reader will understand this reasoning." Then: why does a parameter change host cell protein by
a factor, and in which equation; the spread of what, and what least squares assumes, named; what the
implications are (are limits ratios? are the intervals not suitable?); and that the logic of
"exhaustive rather than stepwise" could not be followed. STORY_BIBLE §9b now has "Explaining the log
scale and the search to a reader". Rewrite your statistical methods (and the first place the log scale
is used) to that standard, with your own data: the model on both scales, the fold changes of the main
effects, the physical reasons, the named assumption and the evidence for it (residual SD in the lower
and upper half of the predictions on the raw full model and on the log model; Box-Cox λ and interval),
the implications, and the search in order. `D.selection_comparison()` gives the stepwise comparison
(one row per output with a criterion); use the Protein A rows.

## B. Factual check 2 (5 errors, 1 probable)

1. §13.3.2 limits PD-005-02 to pool host cell protein. The record was widened again today (it now
   covers the influence analysis of every output and the residual trends, criterion 5 as a whole):
   make every mention match `discrepancy_register(DOC)`.
2. Leached Protein A has no term, so it has no F-test: criterion 2 does not apply to it. Fix Table 5.7,
   §5.3 and the Discussion.
3. §7.3 says the design space excludes the high-load, low-pH corner: say precisely what is excluded
   (the median meets the criterion there; the upper limit of a single batch does not) and by which
   statistic the design space is defined.
4. Count model terms one way throughout (state whether the intercept is counted).
5. The executive summary's "qualified for each output that it compares at both scales": only outputs
   with a criterion are judged; the others have their offset recorded.
6. Probable error 6, settled: the criteria rest on the planned runs, because they were fixed when
   INV-001 closed, before the augmentation runs existed. On all runs the anion exchange bound is the
   same to three significant figures (`D.verification_all_runs()` against `D.iac_verification("aex")`).
   Say both.
Plus the notes of the factual check (rounding of 0.53, and the rest).

## C. Review run 3, with resolutions

1. **The hold (C1–C4).** The lower limit of acidic variants is not met by the pool entering the hold at
   the least favourable corner of the bioreactor NOR; that is a property of the bioreactor, handled in
   PCR-003, and the hold raises acidic variants, it never lowers them. Criterion 7 judges what the hold
   adds. Say so, in the table and the text: the hold meets criterion 7 for every attribute it changes,
   and the lower-limit rows show the level entering the hold, with the reference to PCR-003. Remove
   "the attribute closest to its criterion is acidic variants at 31.2 %". The hold study held one
   eluate made at set-point: say so, and bound the claim to what that supports.
2. **"No CPP" (C5–C7).** Name the classes: no parameter is in the class CPP; two are well-controlled
   critical process parameters (WC-CPP), which are critical.
3. **The interaction (C8–C12).** Say what the data support and no more: on the log scale the main
   effects of load and elution pH are additive, which in ng/mg is a multiplicative effect, and that
   multiplicative structure is what the raw-scale interaction largely was; whether a further load ×
   elution pH interaction exists on the log scale the data do not decide. Its p-value is above 0.05
   in every analysis of run 23, AICc selects it in two of the three, and models with and without it
   lie within 2 AICc units of each other (compute, in the setup chunk, the models within 2 AICc units of
   the selected one with `adequacy.hierarchical_subsets` and `adequacy.aicc`, and name what they
   share and where they differ). State the AICc convention (the residual variance is counted as a
   parameter). Every conclusion over the NOR is the same whichever of these models is used: show that
   for the nearest ones. Fix every sentence the review lists.
4. **Figure 5.1 (C13).** Straight parallel contours come from the absence of an interaction term in the
   model, not from effects that multiply. Correct the sentence.
5. **Cook's distance and leverage (C14–C17).** Remove the claims about leverage; say instead that the
   4/n cut-off flags a run or two in most models of this size even when the model is correct, and keep
   the influence analysis as the test of whether a conclusion depends on a run.
6. **Residual trends (C18–C19).** Criterion 5 applies per test at α = 0.05, as the plan states. Judge it
   so: the two trends found (leached Protein A with run order, fragments' spread with level) do not
   meet it. Do not use a multiplicity correction as the decision; it was not in the plan. Give each
   trend's size against the criterion of its output, and that the conclusions rest on the analysis of
   PD-005-02 (whose record now covers criterion 5 as a whole).
7. **Fragments and scale (C20–C22).** Fragments carry no offset because the qualification never
   measured them, so their conclusions assume no difference between the scales, on the mechanism given
   and the bound from the harvest hold study. Remove "every conclusion is at manufacturing scale" and
   "qualified for each output it compares" where they include fragments.
8. **The load titre (C23–C25).** The registry now has the titre method: Protein A affinity HPLC,
   `SOP-3016` and `AMV-3021` (`SOP_REFS`, `AMV_REFS`, `PROTEIN_A_AMV_REFS`, and its performance in
   `deviations.methods`). The protein load of each run is set from the load volume and the titre by
   that method; A280 is used on the purified pool. Correct §3.3, §5.4 and §9, and the method table.
9. **The widened criterion (C26–C29).** Describe the rule exactly: the one-sided 95 % confidence bound
   of the mean clearance at the least favourable NOR combination replaced the platform value. Say that
   a single batch can clear less (the runs at the edges did: give their folds). Say that the
   qualification of the scale-down model for pool host cell protein depends on the widening: against
   the criterion without the widening it would not be qualified (`D.criteria_without_ca3()` with
   `D.offset_qualification`). "A priori" means derived from the drug substance criteria and the
   platform worst cases without this campaign's data; PCMP-001 Version 2.0, which states the rule, was
   issued after the studies: say that, not that the rule preceded the data. Whether the rule should
   use a bound for a single batch is a question put to the owner: write nothing that depends on the
   answer.
10. **Univariate ranges (C30).** S-PA-UNI did not measure fragments: limit the claim to the attributes
    measured.
11. **DEV-005-02 (C31–C32).** The record now holds the first result
    (`deviations` DEV-005-02 `values.first_over_reported`, a multiple of the reported re-assay of run
    11). The cause was suspected, not confirmed. Report both results, say that the re-assay is the one
    used and why, and give the analysis with the first result in place of the re-assay (model
    selection, the judgement of leached Protein A, the run-order trend). State whether any conclusion
    changes.
12. Every other flagged sentence (Q1–Q4, Q6, Q7) and table observation of the review.

Gate and render (`check_render --render` now renders the pdf too, and fails on an unresolved
cross-reference). Report what you changed under A, B and C, the gate result and the page count.
