# INV-002, after review run 1: what to change (one cycle)

Two inputs: the owner's comments on your draft (section A), and the first content review,
`content-review-INV-002.md` in this folder (section B). Some review findings were checked against the
code and the data before this list was written; where the check settled a finding, the resolution is
given and you write to it. Every value stays computed; new helpers are named below.

## A. The owner's comments (2026-10-09). These come first.

The owner read §8.1 and wrote: "Do not expect that a reader will understand this reasoning." The
passage on the log scale and the passage on the exhaustive search must be rewritten so that a reader
in the field, who is not a statistician, can follow every step. STORY_BIBLE §9b now has a section
"Explaining the log scale and the search to a reader": follow it point by point, with numbers from
the data. In short, the owner asked:

1. "A process parameter changes the level of host cell protein by a factor … Why? Under which
   setting? Untransformed, in the model equation?" Give the model on both scales (ln y = b0 + b1·x1 +
   … + e; transformed back, y = e^b0 · e^(b1·x1) · … · e^e), say what a factor e^b per coded unit
   means, give the fold changes of the main effects of pool host cell protein across the range
   studied (from `D.fit("protein_a", "rsm", "pool_hcp_ng_mg")["model"].params`, e^(2b)), and give the
   physical reasons (a purification step removes a share of what is present; the ELISA precision is a
   percentage of the level, `deviations.methods` AMV-3012 precision_pct). Show the raw-scale
   interaction that disappears on the log scale (`["full"]` and `["full_scale"]` p-values of
   load × elution pH).
2. "The spread of what? The residuals? What does least squares assume, name it." Name it: residuals
   independent and normally distributed, with mean zero and the same variance over the whole range
   studied. Show the evidence: the residual SD of the raw full model in the lower and the upper half
   of its predictions, against the same on the log scale (compute both), and the Box-Cox λ with its
   95 % interval.
3. "So what are the implications? Limits for these factors are calculated as ratios? Intervals for
   these factors are not suitable?" Answer plainly: the criteria and the prediction limits stay in
   ng/mg; effects become fold changes and the scale-down offset becomes a ratio of geometric means;
   the intervals are suitable, because coverage is kept exactly under the back-transformation and
   the least-squares assumption holds on the log scale; they are asymmetric (give one example, for
   instance at the least favourable NOR combination of Protein A, `D.prediction_interval`); the
   predicted value is the median; near an upper criterion a raw-scale model understates the scatter.
4. On the paragraph "The search is exhaustive because a stepwise search changes one term at a
   time …": "I do not understand this logic." Rewrite in this order: the goal (the lowest AICc among
   all hierarchical submodels); what AICc is and why the small-sample correction (give the size of
   the correction for the full quadratic on 28 runs); exhaustive search; why not stepwise; and what a
   stepwise search would have done here, computed: `D.selection_comparison()` gives, for each output
   with a criterion, the AICc and number of terms of the exhaustive choice and of a backward and a
   forward stepwise search. Give the counts (outputs compared, backward worse, forward worse, either
   worse) and one example. Then how CA2 differed (stepwise, p-values, raw scale only).

## B. Review run 1, with what the check of the code and data showed

1. **Hierarchy of the refits (review A1, the review's first point).** The refits are hierarchical:
   `adequacy.reduce` never removes a main effect while a term containing it remains. Table 5.1 listed
   only the significant terms, so main effects kept for hierarchy were invisible. `T.adequacy_remedy`
   now prints the whole refit, with such a main effect in parentheses and a note. Make the text match:
   Table 5.1 gives the terms of each refit; the power table (Table 6.2) is of the significant effects
   (say so). The simulation's true model is the whole refit.
2. **The augmentations changed two models (review point 2).** Say so plainly. New computed facts,
   `D.augmentation_prediction_check()`: the model selected on the planned runs predicts the
   augmentation runs it has not seen. Give, for each output of the augmented steps, how many new runs
   fall inside its 95 % prediction interval, its prediction error against its own residual SD, and the
   block term on all runs (none is significant, so the misses come from the models, not from a shift
   between the blocks). High mannose and bioreactor aggregates predict the new runs poorly; on all
   runs high mannose loses the interactions the planned runs suggested and aggregates gains a pH
   curvature. So: passing §7.2 on the planned runs did not make those models reliable; the
   augmentation was not needed to pass the test, but it changed what two models say, and the reports
   use the models on all runs. This replaces "sharpened the estimates".
3. **The adequacy check after selection is optimistic, and CA3 widened criteria (review point 3).**
   State both plainly. The selection used the same runs that §7.2 then judges, so §7.2 is an
   optimistic check of a selected model (point 2 gives the independent check that exists). All four
   criteria that CA3 moved are wider. Then the sensitivity, computed with
   `D.ca3_criteria_sensitivity()` (and `D.criteria_without_ca3()`): judged against the criteria the
   full quadratic models would have given, does any output's conclusion across the NOR change, and
   which NOR-propagated PARs change? (Today: no conclusion changes, and one PAR moves: the elution
   buffer pH PAR for pool host cell protein at Protein A; give its two lower ends and the NOR.) Add,
   from `D.verification_all_runs()`, that the anion exchange bound behind the widenings is the same on
   all runs as on the planned runs. Do not argue that CA3 was adopted for a good reason only; give
   this evidence that no decision rests on the widening.
4. **The sample-size simulation and "assurance" (review point 4).** The simulation ran on the raw
   scale because the planned model was the raw full quadratic, the model the plan prescribed when the
   runs were sized; say so. What is computed is the probability, at the effects estimated from the
   planned runs, that the planned model meets §7.2: define "assurance" in exactly those words at first
   use, and say that it does not include the uncertainty of those estimates.
5. **The 0.95 ceiling of Table 6.1 (review point 5).** Explain it: the lack-of-fit test at α = 0.05
   rejects a correct model in 5 % of data sets, so no design can push the probability above about 0.95.
6. **The effectiveness check (review point 6).** The record is corrected
   (`campaign.investigation_2.effectiveness_check`, `EFFECTIVENESS2`): the old criterion, every planned
   model adequate, fails most of the time even when the check works. Use the new wording.
7. **Text against tables (review point 7):** fix all five (Table 6.1 "at or below 0.005"; Table 8.1
   anion exchange "lower"; Table 9.2 "Two changes"; Table 5.1 footnote a against the anion exchange
   rows; and the claim that INV-002 gives no results of the new runs, which Tables 8.1, 9.1 and §9.2
   contradict: say what INV-002 gives and what the reports give).
8. **Acidic variants at low-pH inactivation fits exactly.** Say so where its status is given: the
   replicates are identical at the precision reported, so there is no pure error to test lack of fit
   against, the model reproduces every run, and the smallest exact model is taken (STORY_BIBLE §9b,
   `D.fit(...)["exact"]`).
9. **Outputs judged on measured results** face a weaker standard than a prediction interval for a
   future batch: say so, and give for each the margin between its highest measured result and its
   criterion.
10. **A model with no terms** is not proof that the output does not depend on the parameters: it says
    no effect was detected at the power the design gives (§6.4). Reword everywhere.
11. **Document codes** (PCMP-001, PCMR-001, PCR-00N, SOP-1002, PD-xxx): name each at first use.
12. Every other flagged sentence and table observation of the review file.

Gate and render as before (`check_render --render` now renders the pdf as well and fails on an
unresolved cross-reference). Report what you changed under A and B, the gate result and page count.
