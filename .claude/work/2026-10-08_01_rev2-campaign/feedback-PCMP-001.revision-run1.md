# PCMP-001 revision, review run 1: what to change (one cycle)

## A. Data and machinery changed after your revision. Re-render and re-check every computed sentence.
1. Tightening now uses the 95 % confidence bound of the A-Mab prediction, like widening (both
   directions conservative, `amab_process/iac.py: final`). The two aggregate criteria upstream of
   cation exchange are now stricter (bioreactor 6.57 %, low-pH inactivation pool 7.11 %).
2. The bioreactor aggregate criterion is now marked BOTH tightened (by the cation exchange model)
   and widened (by the bound of the low-pH inactivation aggregate increase, 0.54 against the
   platform 0.70). `iac.csv` basis "back-calculated, tightened and widened on verification", and
   `tightened` and `widened` are both True on that row. Any sentence that says the tightened
   criteria came from the cation exchange model alone, or counts tightened and widened criteria as
   disjoint sets, must be recomputed and reworded.
3. `T.methods_by_study()` no longer shows aggregate by SEC at a step where aggregate is not a
   response of the designs (Protein A, anion exchange, virus filtration: "not a response").
4. The rule text must now say that a worse step is replaced by its 95 % bound, not by its point
   prediction.

## B. Tables (owner's comment, 2026-10-08)
5. Index cells that repeat down the rows are merged. The render gate now fails a table that repeats
   its first cell. Your table of instrumented scale-down systems repeats "EQ-BRX-205": build it with
   `T.frame(df, caption, label, merge=[...])` (tables.py, section 13), or with
   `T.calibration_windows()` if it carries the same content. Check every other table of yours.
6. Long headers are broken over two lines (`header={"col": "Drug-substance\ncriterion"}` in
   `T.frame`) or abbreviated with the abbreviation defined in the table note and in the
   Abbreviations table.

## C. Flagged sentences, each with what it lacks
Q1, a cause without its physical content:
- "Intermediate pools are held between steps, and the hold can change the product." Lacks which
  species changes (aggregation, deamidation, proteolysis) and in which direction.
- "...pool host cell protein, the output that sets the ranges of the step." Lacks why host cell
  protein limits the step: which parameters move it toward its criterion.
- "Within its NOR, the cation exchange model predicts an aggregate clearance as low as …" and the
  sentence after it. In a plan, say only that this was what verification found and refer to the
  report. Do not explain a mechanism the plan cannot support.

Q2, terms that are not terms of art:
- "set-point analysis" and "NOR-propagated analysis". The reports' tables use these two names, so
  keep them, but introduce each with what it is in established words (a univariate proven
  acceptable range with the other parameters at set-point, and the same range with the other
  parameters varying within their NORs).
- "decision statistic": say what is compared with the criterion, in plain words.
- "analytical method decision AMD-001": name it as the decision to change the fragment method to
  nrCE-SDS, with the identifier after it.
- "fragment balance": say what is meant (fragment results compared across steps).

Q3, sentences that file their own finding or answer an objection nobody raised:
- "This criterion is wider than the Version 1.0 limit, and it is not a loosening of an approved
  criterion." Keep the fact once, but give its reason in the same sentence or the next (the
  Version 1.0 limit was never an approved criterion), so it reads as information, not a defence.
- "It is not a deviation, because no procedure and no GMP requirement was departed from." Keep the
  classification, stated as what the event is (work the plan did not foresee), not as a rebuttal.
- "A low criticality reduces the weight an attribute carries in RA-001. It does not remove the
  attribute from the acceptance framework." Remove, or attach it to the place where it matters.
- "This rule is set here, before any Version 2.0 report applied it. That is the difference from
  …". Keep one plain sentence on when the rule was set.

Q4, criteria without a basis:
- the 90 % confidence interval of the offset (give the basis: the two-sided 90 % interval is the
  one used for comparing two means at 5 % per side);
- α = 0.05 for model terms (the conventional level, stated once with its consequence);
- the NOR standard deviation of one sixth of the NOR width (state the assumption: the NOR spans
  ±3 standard deviations of routine variation);
- the 95 % predictive interval of a single batch (say which side is compared with a one-sided
  criterion);
- Cpk ≥ 1.33 ("common industry practice" is weak; say what 1.33 corresponds to).

Q5, contradictions and errors:
- Criticality levels against Tool #1 scores (Table 3.1): the viral clearance rows are VH with a
  score of 20, below several H rows. The text says the levels follow the scores. Say how viral
  safety was assigned (very high by rule, because of its impact, whatever the uncertainty term
  gives), or describe the relation between level and score correctly for every row.
- The bioreactor aggregate criterion (see A.2).
- "Screening designs executed before that date measured fragments by SEC (Table 7.3)." The
  response-surface designs of Protein A, low-pH inactivation and cation exchange also measured
  fragments by SEC (Table 7.3, and their dates in the chronology table). Correct the scope.
- The offset rule says every judgement subtracts the offset, while viral clearance and fragments
  "carry no offset". Fragments have criteria. State the rule with its condition: the offset is
  subtracted where the qualification compared that output at both scales; an output not compared
  (fragments, viral clearance) is judged as predicted, and its representativeness rests on what
  the step plan states (mechanism, spiking model).
- The predictive interval is described differently in two sections (residual and NOR variation in
  one, residual and coefficient uncertainty in the other). They are two different analyses (the
  NOR-propagated range by Monte Carlo, and the outputs over the NOR by the exact prediction
  interval). Name each for what it is.
- 2026-07-24 is called an approval date in one place and the compilation date in another. Use one
  meaning, consistent with the revision history.
- Fragments are assigned to harvest in Table 3.1 (where they form), but no criterion or study at
  harvest exists. Say that they form there and are judged downstream.
- Table 6.1 does not list aggregate as a response at Protein A or virus filtration, which is right.
  Check the text against the corrected methods table (A.3).
- "No step after cation exchange removes aggregate." This is the derivation's assumption, not a
  fact about anion exchange and UF/DF. State it as what the derivation credits.

Q6, sentences that say nothing a reader would miss (cut, or merge into the sentence they repeat):
- "This corrects the first three findings of INV-001. The Version 1.0 step criteria were …" (restates the paragraph above);
- "Their plans and reports are correspondingly shorter, and no designed experiment is planned for them.";
- "Two analyses are used, and each is referred to by the name given here.";
- "This plan sets the rule and reports no offset.";
- "Judging that pool against the drug substance limit of 100 ng/mg would fail every acceptable run." ("acceptable run" contradicts itself);
- "The tightened criteria came from … each is stricter … The widened criteria … each is wider …" (tautological);
- the "That is the …" sentence openings after "gives the argument for it" and after "carries the same structure";
- "Each viral step must meet its own claim." (third statement);
- "A PAR is never extended beyond the characterized range." (restates §2);
- "Fragments were not an attribute of the production bioreactor designs." (third statement);
- "The calibration of 3 scale-down systems bears directly on the results." (vague: name what each system controls);
- "It is a property of the step and its mechanism, and it does not depend on the other steps."

Q7, sentences that need the paragraph before them (name the thing):
- "This corrects the first three findings of INV-001." Name the three findings.
- "Verification widened both criteria, to 19,241 and 476 ng/mg, by the rule in Section 7.5." Name what replaced what.
- "A-Mab data enter a criterion only through verification, and only by the rule …". Say what the rule does.
- "The intermediate acceptance criteria rest on assumptions about the downstream steps." and "Each report checks the assumptions …". Name the assumptions (the platform worst-case clearance or increase of each downstream step).
- "Of the 9 assumptions, 7 can be checked …" and "For 1 further assumption … and 1 assumption was not confirmed." Name the attributes and steps.
- "The first execution of the anion exchange design (S-AEX-SUP) was invalidated under deviation DEV-008-01 …". Say why.
- "… as AMD-001 decided." Name the decision.
- "The calibration of 3 scale-down systems …". Name the measurements.
