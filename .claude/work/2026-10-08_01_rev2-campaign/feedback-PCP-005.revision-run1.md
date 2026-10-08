# PCP-005 revision, review run 1: what to change (one cycle)

## A. Machinery changed after your revision. Re-render and re-check every computed sentence.
1. Tightening now uses the 95 % confidence bound, like widening. The aggregate criterion your hold
   section quotes changed (6.57 %). The bioreactor aggregate criterion is now both tightened and
   widened (`iac.csv` basis).
2. `T.iac_derivation([UO])` drops the constant "Step output" column when it shows one step, and
   both derivation tables now say they are computed from unrounded values. The reviewer recomputed
   2.00 × 1.32 − 0.15 = 2.49 against your 2.50, and 100 × 192 = 19,200 against your 19,241. In the
   prose, do not invite the arithmetic with rounded factors: give the criterion and its inputs as
   the table does, or round consistently.
3. `T.worst_case_verification` no longer shows concentration units on fold rows, and merges the
   worst-case column. The related-documents and SOP tables now have fixed column widths.

## B. Tables (owner's comment, 2026-10-08)
4. Your planned design matrices (appendices) repeat "factorial", "axial" and "center" down the Type
   column: build them with `T.frame(..., merge=["Type"])` or order and merge them so each run type
   is one cell. Use one spelling ("centre" as in the text, or "center" throughout).
5. Table 6.2 repeats "screening + RSM" in every row: a constant column carries nothing. Drop it and
   say it once in the caption or the text, or merge it.
6. Table 7.1 repeats "Single batch, 95 % predictive interval": merge it, and keep "95 %" on one line.
7. Table 6.1: the NOR column wraps "150–/250". Widen that column.

## C. Flagged sentences, each with what it lacks
Q1:
- "As the load approaches the dynamic binding capacity, the mass transfer zone moves down the bed
  and carries impurity into the eluate that the wash would otherwise remove." Lacks the interaction
  by which host cell protein reaches the eluate (host cell protein associated with the bound
  antibody, or bound to the resin, is not displaced by the wash).
- "At high load more host cell protein is held weakly on the bed, so there is more for a low
  elution pH to release." The direction is questionable (at high load the antibody displaces weakly
  bound host cell protein). State the mechanism the prior knowledge supports, in its direction.
- "It also depends on how long the load is held before capture, because host cell proteases in the
  clarified harvest cleave exposed ligand." and its two repeats (§5.1, §12 item 2). Lacks the step
  that links the hold to the ligand: protease activity in the load rises during the hold, so the
  load that reaches the column cleaves more ligand.
- "Residual DNA is measured for information … because its clearance is expected to be large and
  insensitive to the parameters." Give the physical reason here (DNA is polyanionic and does not
  bind Protein A).
- "In manufacture bed height is held by the packing specification, so it is studied one factor at a
  time." Reconcile with the sentence before it, which gives a physical reason to study bed height
  with load.

Q2, terms that are not terms of art:
- "set-point analysis" and "NOR-propagated analysis": keep the names, which the reports' tables use,
  but introduce each in established words at first use.
- "predictive interval": the term is "prediction interval". Use it throughout.
- "statistic judged", "offset rule", "widened on verification", "method decision": say what is
  meant in plain words (the value compared with the criterion; the rule for qualifying a scale-down
  model by its offset; the decision to measure fragments by nrCE-SDS).
- "Version 1.0 analysis limit" and "approved plan criterion": say what each is once, plainly.
- "clearance fold" for fragments: say how the fold is defined for a percentage (ratio of fragment
  level in the feed to that in the pool).
- "step outputs": the step pool.

Q3:
- "This is not a loosening of an approved criterion." Keep the fact once with its reason (the
  Version 1.0 limit was never an approved criterion).
- "It does not by itself disqualify the model for leached Protein A, and PCR-005 states its size and
  its cause." A plan does not anticipate an objection. State the rule.
- "For that reason it may be applied to studies that were already executed." Borderline. Keep it
  only if the reason is in the same sentence.

Q4:
- The hold criteria (≤ 6.57 % aggregate, 18–39.6 % acidic variants) appear without their a priori
  values and without the reason they moved. Give both, from the data.
- The univariate rule judges individual results at both ends, while Table 7.1 says single batch,
  95 % prediction interval. Say why a univariate study is judged differently, or align them.
- Fragments are used without the scale-down qualification that criterion 1 requires. State the
  basis on which a fragment result from the scale-down model is accepted (mechanism, and what the
  plan does to confirm it).
- The lack-of-fit α and the 0.20 limit: give their basis once (PCMP-001 and why).

Q5:
- Temperature: "Temperature is not expected to interact with the other parameters." contradicts the
  paragraph's own mechanism (temperature raises dynamic binding capacity, so it interacts with load
  by the flow-rate argument of §4.1 item 2 and §4.3). Make the argument consistent, and give the
  reason temperature is studied one factor at a time.
- The offset: "every result that is judged against a criterion is first translated to manufacturing
  scale" and "Every judgement against a criterion subtracts that offset" are contradicted by
  fragments, which carry no offset, and by the hold results judged as measured. State the rule with
  its condition: the offset applies to outputs that the qualification compared at both scales.
- The hold criterion: judging the held eluate against the absolute criterion for the bioreactor
  output does not bound the increase during the hold (a pool at that criterion would exceed it after
  any increase). Say what the hold criterion limits (the increase over the hold, judged against the
  room between the step's expected output and the criterion, or whatever the data and the rule
  support), and make criterion 7 say it.
- Table 1.1 footnote a) says Version 1.0 judged leached Protein A against the drug-substance
  criterion, and the text says Version 1.0 applied one analysis limit, for pool host cell protein.
  Both are true. Make the text say both, so the reader does not see a conflict.
- Table 8.2 shows units in the attribute column of fold rows (fixed in the builder, A.3). Check your
  text does not repeat the error.
- Table 5.2's title now says "in the designed studies" (builder). Check your text describes it that
  way.
- No change for the residual DNA criterion (< 10^-3 ng/dose is the A-Mab case study's value) and
  none for predicted R² against R² (the campaign threshold is R² minus predicted R²).

Q6, cut or merge:
- "Three kinds of limit therefore need to be kept apart in this document.";
- "The manufacturing history of these antibodies establishes the mechanism of the step and the performance to expect from it." (overclaim);
- "The step is robust, and the direction of its main effects is known (CMC Biotech Working Group 2009).";
- "The ranges of protein load and end of pool collect are set symmetrically about their set-points." (all four are);
- "The difference between the mean at each end and the set-point mean is reported with its 95 % confidence interval, as the size of the effect." (restates);
- "Table 7.1 lists the outputs of the step, …" (restates the caption, after the table);
- "The NOR-propagated analysis therefore judges the predictive interval of a single batch." (restates §8.2);
- the fourth statement that leached Protein A clearance is not a response downstream;
- "The life of the resin is controlled by SOP-2008." (non sequitur where it stands);
- the third statement of the widen/tighten rule in §12 item 4.

Q7, name the thing:
- "A Version 2.0 criterion is a criterion of this revision, derived a priori by PCMP-001 §7.3 and verified by PCMP-001 §7.5." Name the derivation and the check.
- "… then widened by the rule of PCMP-001 §7.5, …". Name the rule.
- "… the model is qualified when the conclusion of criterion 6 over the NOR is the same …". Name what criterion 6 decides.
- "A model that fails criterion 3 or 4 …". Name the two tests.
- "The decision rule for the hold is criterion 7 of Section 7." State the rule.
- "Each parameter is classified under SOP-4001 by the decision logic of PCMP-001 §7.7." Name the logic in a clause.
- "… with the width that PCMP-001 §6.4 sets from its NOR …". Give the width.
- "… after study S-PA-SDM had closed on 2025-11-14." Name the study.
- "… before the method decision AMD-001." (three places). Name the decision.
- "PCR-005 relies on 2 widened criteria …". Name them.
