# What the reviews of the first three plans found, as rules for the next plan

Written 2026-10-09 from the content reviews and factual passes of PCP-005, PCP-006 and PCP-003
(`content-review-*.md`, `feedback-*.md` in this work unit). Each rule below was broken at least once
by a careful author and caught by a fresh reader. The rules say what must be true in the plan, not how
to word it. Read the rendered PCMP-001 for the rules a plan applies; this file only says where plans
went wrong when applying them.

## 1. The rules the plan states

1. **Scale-down qualification order.** The qualification runs and the offset estimate are made before
   the first characterization run of the step. Whether the model is qualified for an output is
   decided at analysis, because the decision is the conclusion over the NOR with the offset at either
   end of its interval, and that needs the response-surface model. Say both, in that order, wherever
   the plan says the model is qualified (the study sequence table included). An output the
   qualification does not compare (fragments, at most steps) carries no offset: say so, and state the
   assumption the judgement then rests on.
2. **What is judged on what.** A quality attribute is judged on a single batch, through the 95 %
   prediction interval of a single batch, because the criterion applies to each batch. The model
   predicting a mean is the reason an interval is needed, not the reason for the single batch. Viral
   clearance is judged on the mean predicted log reduction at the least favourable combination of
   NOR low, set-point and NOR high of the other parameters. Scope every general sentence to the
   outputs it covers, so the two rules never contradict each other.
3. **The two PAR analyses.** Define both at first use. The first holds the other parameters at their
   set-points and judges the mean prediction (check brief §5c: some plans carry registered discrepancy
   D-001 here, and it stays as registered). The NOR-propagated analysis draws each other parameter
   from a normal distribution centred on its set-point with a standard deviation of the NOR width
   divided by `D.NOR_SD_DIVISOR`, clipped at the range studied, and judges the single-batch interval.
   That is not "varying within the NOR", so do not say so. The NOR-propagated PAR is the one that
   supports a claim.
4. **Model adequacy.** Name the conditions of PCMP-001 §7.2 as tests a result passes or fails: the
   model F-test, lack of fit against pure error, R² less predicted R² against its limit, and the tests
   on the residuals and on influence (state the statistic and the cut-off, and the basis of the
   cut-off). State the remedy for a failing model exactly as the rendered PCMP-001 states it, and what
   follows when the remedy fails (no range from that model; the output judged on its measured results,
   `D.nor_met`). Do not describe the model selection of INV-002 corrective action CA3 as the plan's
   method: PCMP-001 does not adopt it, and each report records it as a discrepancy from its plan.
5. **Classification.** PCMP-001 and SOP-4001 set no numerical threshold for "practically relevant" or
   "wide". Do not let an undefined magnitude word decide a class. Say that the report states the
   effect size across the PAR and the margin of the PAR to the NOR, and classifies on them.
6. **Criteria and their basis.** A criterion of this step is derived a priori: the drug substance
   criterion carried back through the platform worst case of each downstream step, with no margin.
   Verification at a downstream step may since have replaced a platform value with a single-batch
   bound, so say which downstream result entered which criterion. The true statement is that no
   result of this plan's own studies enters its criteria. An increase is in percentage points.
   Criteria are computed from unrounded values (the table note says so). A two-sided criterion
   (acidic variants) is judged at both ends. Fragments are judged on nrCE-SDS results only, on the
   samples and days that have one.
7. **The verification rule.** The bound that moves a criterion is the one-sided 95 % prediction bound
   of a single batch at the least favourable NOR combination (`D.VERIFICATION_BOUND`), never a
   confidence bound of the mean and never a point prediction. The platform increases of the low-pH hold
   are over a 180-min hold, and the A-Mab values are within a NOR that ends at 120 min, so a
   replacement there reflects the shorter hold, not a more stable product (STORY_BIBLE §9b).
8. **No defensive glosses.** State once, where the criteria are given, that the Version 1.0 limit was
   set at analysis and was in no approved plan. Do not add a sentence that the wider criterion "does
   not loosen" anything.

9. **What an amendment may add** (STORY_BIBLE §9b, after the PCP-006 factual check). A Version 2.0
   plan is issued after its studies ran. It may state, and list as changes, what PCMP-001 Version 2.0
   sets, plus generic tests applied the same way in every plan. Those tests are the residual regressions
   at α = 0.05 and Cook's distance above 4/n. It must not add a step-specific decision rule, such as a
   refit procedure, a NOR rule for one parameter or a test chosen for one study, and it never says a
   rule was "fixed before the data".
   - It keeps the design, sampling, spiking and every decision rule as Version 1.0 stated them, even
     where a study departed from them or the data broke a rule. The report records the departure.
     Deleting a Version 1.0 rule after the data hides the departure (PCP-003 factual check). A plan
     author may read the frozen Version 1.0 plan (`pc_package/superseded/rev1/`) for its rules, design,
     sampling and procedures, never for voice.
   - It describes no study made after Version 1.0: no hold study, augmentation, confirmation or support
     study. Each report records those as discrepancies from its plan.

## 2. Science

- A cause names the species, the property and the direction in the clause where the cause verb
  stands. Prior knowledge from the A-Mab case study is stated as an expectation, never as "known" or
  "confirmed".
- Check the normalisation before giving a mechanism: an output per mg of antibody does not rise
  because more antibody is loaded. Inactivation is first order, so the log reduction is proportional
  to the rate integrated over the hold, not equal to it.
- A step that does not separate a species (glycoforms, charge variants at capture) is said not to
  separate it for a physical reason, not by restating the claim.

## 3. The record

- The plan's approval date comes before the first study of its step (`rev1_date(DOC)` against
  `study_chronology.csv`; compute and assert it).
- Studies whose windows overlap ran in parallel, so say so, and define the start and end of a window.
- Studies that started after Version 1.0 (augmentation, confirmation, support and second univariate
  studies) are not studies of this plan. The report records each as a discrepancy from the plan.
- A deviation is a departure from an approved procedure or a GMP requirement, or an unplanned event
  in execution. A discrepancy from the plan is work the plan did not foresee. Keep the words apart.

## 4. Tables

- Never retype or override a builder's header or note in the document. If a builder is wrong, report
  it.
- In your own tables use at most two header lines, no constant column, units in the header, a legend
  for every code (H, VH, L, VL), and merged repeated cells (`T.frame(..., merge=[...])`).

## 5. Readability

- Give the name with a code at its first use in each section (SOP numbers, study codes, finding and
  action codes).
- State a gloss once, then use the short name.
- Cut sentences that only point at a table, restate the previous sentence or a caption, or comment on
  the document's own coverage ("not repeated here").
