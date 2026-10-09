# PCP-006, after review run 1: what to change (one cycle)

Read `content-review-PCP-006.md` in this folder for every flagged sentence and table observation.
The findings below needed a decision or a check of the code or record; each is resolved, so write to
the resolution. Everything else in the review: fix as the review says.

## Decision rules a reader cannot apply (Q4)

1. Residuals and influence: state the statistic and the cut-off, as a test a result can pass or fail:
   a regression of the absolute residuals on the predicted values, and of the residuals on run order,
   each with no slope significant at α = 0.05 (`THRESHOLDS`/config), and no run with a Cook's
   distance above 4/n.
2. The refit rule of PCMP-001 §7.2: state it as PCMP-001 states it (read the rendered PCMP-001), so
   that it covers every adequacy condition, and say what a justified change of terms or transformation
   is in this plan: removal of terms that are not significant, keeping hierarchy, or a transformation
   the residuals support; a model that still fails sets no range.
3. The NOR-propagated analysis: give the distribution of the other parameters as the engine draws it
   (read `doe_report._mc_predictive` and `par_nor_propagated` for the rule, and pull any number).
4. "Appreciably" and every other word that decides a classification: give the rule of PCMP-001 and
   SOP-4001 as PCMP-001 states it.
5. The A-Mab concentration study measures some attributes only: judge each range against the
   criteria of the attributes it measures, and say which.
6. The hold rule: fragments are judged on the days with an nrCE-SDS result (`hold_viral_inactivation.csv`).
7. Acidic variants have a two-sided criterion: judge both ends.
8. Fragments carry no scale-down offset (the qualification does not measure them): remove "at
   manufacturing scale" for them, and state the assumption they rest on.

## Statements that are wrong or inconsistent (Q5)

1. Qualification sequencing. The qualification runs and the offset estimate come before the first
   characterization run (study S-VI-SDM); the qualification decision needs the response-surface model
   (the conclusion over the NOR with the offset at either end of its interval), so it is made at
   analysis. Say both, in that order, everywhere the plan says the model is qualified before the
   studies (Table 11.1 included).
2. "Fragments are measured by nrCE-SDS in every study at every step": Table 5.3 shows otherwise. Say
   what the table says (the method decision AMD-001 of its date, SEC before it, the retests).
3. Concentration and composition: reconcile. Name the property of the pool that the representativeness
   of the scale-down model rests on, and give the prior knowledge on concentration without claiming
   more than it supports.
4. Table 4.1: viral safety is very high by rule, whatever its Tool #1 score (PCMP-001): say so in the
   table note and the text, so the scores and the bands do not read as an error.
5. The first PAR analysis judges the mean prediction; the NOR-propagated analysis judges a single
   batch on its prediction interval and is the one that supports a claim. State both, as PCMP-001
   does. Keep the statement that the first analysis holds the other parameters at their set-points
   as it is (registered discrepancy D-001, brief §5c).
6. Mechanisms: low pH inactivates an enveloped virus by denaturing its envelope glycoproteins (and
   disrupting the envelope); say it precisely. Succinimide is a basic species: do not present its
   formation as adding acidic variants. Give the rise of acidic variants over the hold as the prior
   knowledge the brief gives, and give a mechanism only if it is right.

## Tables

- Table 1.1 (`T.criteria_change`) now says what a criterion was tightened or widened from; re-render
  and check that the text around it matches.
- Table 4.1, Table 7.2 and Table 11.1 are your own tables: fix the header depth, the split category
  labels and the ambiguous score column (4.1), the column headed "Criterion that relies on it" whose
  cells name steps (7.2), and the merged phase label and the report listed as a study (11.1).

Gate and render (`check_render --render` now renders the pdf too, and fails on an unresolved
cross-reference). Report what you changed, the gate result and the page count.
