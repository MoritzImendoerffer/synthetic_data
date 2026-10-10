# PCR-005: follow-up pass after the record changed (2026-10-10, afternoon)

Fix these and nothing else. The document is promoted: `pc_package/PCR-005_protein_a.qmd`, edited in place.
Every value stays computed and every deciding word computed or asserted.

1. **DEV-005-02, the out-of-trend rule, changed** (your flag). The record now reads: "outside the two-sided
   99 % prediction interval of a single result from the full quadratic model of the response-surface design,
   fitted to the other runs of the design without the result under review, at the settings of the run".
   Model selection was adopted in September 2026, while the review was made when the design ran, so the
   review fitted the model the plan specified. The ratio of the first result to the re-assay is now 3.0
   (`dev_005_02_first_over_reported`). `D.oot_check` fits the full quadratic: the interval at run 11 is about
   −1.46 to 5.38 ppm on 12 residual degrees of freedom (`df` in its result), the first result (about 6.4 ppm)
   lies above it and above every other run, and the re-assay inside. State the interval as the rule gives it
   (its lower end lies below zero, so only a high result could be out of trend at that run). Your asserts on
   `oot_terms == ["D"]` and on the selection with the first result in place no longer hold: follow the data,
   and keep every claim computed.
2. **The widening rule, §7.1** (your flag): state it as PCMP-001 §7.5 rule 2 now does: the first three
   adequacy criteria (a significant model, no significant lack of fit, the limit on overfitting) and not an
   exact fit; the fourth criterion does not decide the change. Where PCR-005 relies on the widened host cell
   protein criterion, PCMP-001 §7.5 asks the report that relies on it for "the bound, the runs behind it,
   and the reason why the performance of the downstream step for A-Mab is known well enough": the anion
   exchange model meets the first three criteria and fails the fourth on Cook's distance; INV-002 §8.4 shows
   the bound still above the platform value with each flagged run deleted (cite it, values computed through
   the helpers). Never "passed the adequacy tests".
3. **New deviation DEV-005-03** (`deviations.csv`): the univariate study ran each end of each range in
   duplicate, without the runs at the centre that PCP-005 requires; the reference is the qualification runs
   at set-point. PCP-005 is being restored to its Version 1.0 §6.4 (low edge, centre, high edge, the same
   responses as the multivariate designs), so PCR-005 records this departure in its deviations section, and
   beside the univariate results. The fragment result by nrCE-SDS of S-PA-UNI is not measured (samples not
   retained), as you already state.
4. **Builders changed under you**: true minus signs in the tables (`T.num`); the note of
   `T.criteria_results` for an output with no adequate model now reads "the range of the measured results of
   the designs, less the offset of the scale-down model where one is known"; `D.design_space_grid` includes
   fragments (no grid point excluded). Re-render and check the font floor and the table fit.
5. Leave the annex: the coordinator re-anchors it after this pass.

Gate with `check_render.py --render` (with `.venv/bin/python`), render the pdf and the docx, read the page
image of every table you changed. Report each item with where it was resolved, the passes, the page count,
and any `<<NEEDS:>>` left (none).
