# INV-002, revision: what to change

The draft (`pc_package/INV-002_model_adequacy.DRAFT.qmd`) was written before the owner's decision of
2026-10-09 that every DoE is analysed by model selection. The investigation adopted that analysis as
its corrective action CA3, and the draft does not yet describe it. This revision brings the draft into
line with the record. You are its author for this revision: change what the list requires, keep
what it does not touch, and apply WRITING_GUIDE rule 11 (each sentence understandable on its own;
name the thing, not its code) wherever you write.

Facts come only from the brief (`authoring/out/INV-002.brief.md`, regenerated today, "INV-002 facts"
and §4c), STORY_BIBLE §9b, and the helpers. Never type a number. Every deciding word (adequate, met,
changed, none, all, wider) is computed or asserted in the setup chunk.

## A. Describe every procedure the investigation applied (owner: "INV-002 should contain a description of the applied procedures")

In the order they happened, each with its date where the record gives one:
1. The adequacy test of PCMP-001 §7.2 applied to the planned full quadratic models (the plan's model):
   the model F-test, lack of fit against pure error, and R² minus predicted R² (PRESS). This is the
   finding; it stays as the draft has it.
2. The rule of `campaign.model_adequacy` (decided before any new run): augmentation or refit.
3. The refit by hierarchical backward elimination (corrective action CA2).
4. The sample-size calculation and the D-optimal augmentations (CA1). Keep the method and results as
   they are. State once that the assurance concerned the planned model (the full quadratic with a
   block term), because that was the model the plan prescribed when the runs were sized.
5. **Model selection (CA3, adopted on `selection_adopted`).** This is new and must be described in
   full, as a statistician would need to repeat it (`amab_process/adequacy.py: select_model`,
   `boxcox_interval`, `hierarchical_subsets`, `aicc`; STORY_BIBLE §9b items 1–4):
   - the scale: the Box-Cox profile likelihood of the full quadratic, with its 95 % interval; the log
     scale where the interval contains 0 and excludes 1, otherwise the raw scale. Say why a log scale
     matters for an output like host cell protein (effects that multiply, a spread that grows with the
     level) and what it means for limits: a prediction interval computed on the log scale and
     back-transformed keeps its coverage, is asymmetric in natural units, and a back-transformed mean
     is the median;
   - the search: every submodel of the full quadratic that respects strong hierarchy (an interaction or
     a square only with its main effects), the block term always kept, and the model with the lowest
     AICc chosen by exhaustive search. Give the number of candidate models for four, three and two
     factors from `len(list(ad.hierarchical_subsets(factors)))`. Say why exhaustive search rather than
     stepwise (stepwise search can stop at a worse model) and why AICc (it corrects AIC for small
     samples, and these designs are small);
   - the check: the selected model judged against PCMP-001 §7.2, with a significant model F-test when
     it has terms; a model with no term says the output does not depend on the parameters within the
     range studied; an output with no adequate model is judged on its measured results and sets no
     range;
   - the scale-down offset taken on the scale of the model: a ratio of geometric means for a log-scale
     output.
   CA3 replaced the refits of CA2 for every output, including those CA2 had refitted. PCMP-001 is not
   changed: each DoE report records the model selection as a discrepancy from its plan (the IDs are in
   `PLAN_DISCREPANCIES`, computed). Cite `@boxcox1964`, `@hurvich1989`, `@burnham2002`,
   `@montgomery2017` and `@fedorov1972` where each method is named (now in `references.bib`).
6. The verification of the platform worst cases behind the intermediate acceptance criteria uses the
   selected models (`iac.py`), on the planned runs.

## B. Root cause

The record (STORY_BIBLE §9b, section_plan `root_cause`): the plans prescribed the full quadratic as the
predictive model and no model selection. The full quadratic keeps every term whatever the data show,
and the planned designs are small for it; the leverage argument of the draft explains why such a model
fails the limit on overfitting, and it stays as the mechanism. The contributing cause stays (no
adequacy criterion in the Version 1.0 plans, so no check of design size against it). Rewrite the
Summary's "The cause is the size of the planned designs" to match.

## C. What CA3 changed: say it honestly

1. **The augmentations.** Once selected, the models the augmentations were made for are adequate on
   the planned runs alone (`D.fit(step, "rsm", resp, runs="planned")["status"]` against
   `model_adequacy.csv`; assert it). So the augmentations were not needed for adequacy. They were
   decided and made under the plan's model, and they sharpened the estimates: show how, from the data
   (for example the number of terms of each selected model on the planned runs and on all runs, and
   which terms of the planned-run model did not survive the second block). The step reports give the
   results of the new runs; INV-002 does not.
2. **The outputs with no adequate model** after selection (`status` "none"), by step, judged on their
   measured results.
3. **The criteria.** CA3 was adopted before INV-001 closed, so the criteria fixed at that closure rest
   on the selected models. The same verification on the full quadratic models
   (`csv("iac_full.csv")`, `csv("iac_verification_full.csv")`) gives different values for some
   criteria: the brief lists them, with the verification rows behind them (at anion exchange, the host
   cell protein model fails §7.2 as a full quadratic and passes once selected, so its bound supports a
   widening; the cation exchange bounds move). State which criteria differ and why, in a small table
   built with `T.frame(...)` from those CSVs (merged cells where a value repeats), and that the
   augmentation runs moved no criterion (they ended after INV-001 closed, and the verification uses
   the planned runs). The draft says four times that no criterion changes (Summary, the impact section
   twice, the conclusion), and near line 681 that the anion exchange host cell protein model does not
   meet §7.2 so the cation exchange criterion keeps the platform value. All of these are now wrong.
4. **Conclusions over the NOR** that rested on a failing model, from the data, per report: low-pH viral
   inactivation, XMuLV clearance (not met at the least favourable combination of the NOR as
   characterized, `D.nor_met` inside `D.characterized_nor()`; PCR-006 moves the NOR, one clause), and
   any other row of the brief's status table whose `nor_met` is False (production bioreactor acidic
   variants: say what the data show and that PCR-003 states how it is handled; do not decide it here).

## D. Impact, CAPA, closure

- The impact table by report (keep `@tbl-impact` if it still fits, otherwise rebuild it): the remedy,
  the selected model's status, the discrepancies from the plan (augmentation and model selection).
- The CAPA table is `CAPA2` (CA1, CA2, CA3, PA1, PA2) with the effectiveness check `EFFECTIVENESS2`.
  The text around it must match the table, action by action.
- The Conclusion: the classification confirmed, the CAPA status, the criteria statement of C3.
- The record names no equipment for the augmentation studies. Do not name any.

## E. Gate and render

`uv run python authoring/check_render.py pc_package/INV-002_model_adequacy.DRAFT.qmd --render` until it
passes, then render pdf and docx (`cd pc_package && PATH="$PWD/../.venv/bin:$PATH" quarto render
INV-002_model_adequacy.DRAFT.qmd --to pdf`, then `--to docx`) and look at every complex table once
(`pdftoppm` a page to png and read it). Report: which model you are, each item above and where you
changed it, the number of `check_render` passes, the page count, and anything you could not resolve.
