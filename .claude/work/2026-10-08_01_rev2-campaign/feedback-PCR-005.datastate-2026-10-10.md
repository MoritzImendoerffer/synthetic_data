# PCR-005 Version 2.0, re-opened after the owner's decisions of 2026-10-10: what to change

The document is promoted (`pc_package/PCR-005_protein_a.qmd`, 67 pp). The owner's decisions of
2026-10-10 changed the data and the engine under it, and its setup chunk now stops on its design-space
assert, as it should. This is a fix pass on the promoted text: change what the list requires and leave
the rest alone, except where the readability rule (WRITING_GUIDE rule 11) makes you rewrite a sentence
you touch. Every value stays computed; every deciding word is computed or asserted.

Read first: `data-state-2026-10-10.md` (this folder; it supplements `data-state-2026-10-09b.md`), and
§6 of `procedures/REPORT-LESSONS.md` (the decisions as rules).

## Required changes

1. **The design space is drawn on the single-batch limit** (owner Q2). `D.design_space_grid(UO)` now
   puts a grid point inside when both ends of the 95 % prediction interval of a single run lie within
   the criterion for every quality attribute (offset applied), and viral clearance on the mean. Rewrite
   the design-space section on that statistic: every fraction, the binding output, the description of
   the excluded region, and any figure or table that draws the region. Name the statistic where the
   region is defined. The mean-based region (`basis="mean"`) may be given once as a comparison, named
   as such. Replace the setup assert at the design-space block, which recomputes the mean-based
   fraction, with one that checks the single-batch definition.
2. **DEV-005-02 and its out-of-trend rule** (owner Q7). The deviation record now holds the rule
   (`deviations.csv`, column `oot_rule`) and its level (`dev_005_02_oot_level`), and the first result is
   2.5 times the re-assay (`dev_005_02_first_over_reported`; the recorded 1.8 put the first result inside
   the rule's interval, so the record called a result out of trend that was not). State the rule and
   its numbers: `D.oot_check(UO, "leached_protein_a_ppm", run, value)` gives the interval at the run's
   settings for the first result (outside) and for the re-assay (inside). The first result is now above
   the range of the other runs, so every sentence and assert that says both results lie inside that
   range must follow the data. Recompute the analysis with the first result in place.
3. **Detection of host cell protein** (owner Q3). The risk argument for the pool host cell protein
   criterion names the release test, its LOQ and its coverage: `dev_methods.csv` AMV-3012
   `coverage_pct` and `coverage_method` (scalar `amv_3012_coverage`).
4. **Residual DNA in physical units with a dose** (owner Q4). Check every sentence about DNA: levels
   are pg per mg of antibody upstream of the drug substance and ng per dose at it
   (`_pcpkg.DOSE_MG`, `dna_ng_per_dose`; the 70 kg body weight is an assumption, say so if the dose
   enters an argument). The model's anion exchange DNA clearance is now 5 logs; the anion exchange
   pools are below the qPCR LOQ, so that clearance is not measured there. Any statement of the drug
   substance DNA level, its capability or its probability out of specification is computed again.
5. **The univariate study now has SEC size variants** (owner Q5). `univariate_studies.csv` S-PA-UNI:
   `lmw_sec_pct` and `hmw_sec_pct`. Report them as PCP-005 Version 1.0 required ("the same responses
   measured as in the multivariate designs"): aggregate by SEC, and SEC fragments for information only
   (biased in this matrix, AMD-001). State that fragments were not measured by nrCE-SDS in this study
   because its samples were not retained beyond 30 days, so the April 2026 retest covered only the
   retained response-surface samples; what the class of bed height and operating temperature for
   fragments then rests on (the mechanism and the response-surface model); and claim no nrCE-SDS fragment
   result from the univariate study (REPORT-LESSONS §6 rule 6). Remove any statement that the
   univariate study measured no size variant at all.
6. **Near-equivalent models** (owner Q6). Where the report gives the models within 2 AICc units of the
   selected one (two of them would not qualify the scale-down model), say that the selected model
   decides, as the rule stated it, and the others are a sensitivity.
7. **Criterion 4 by the shared helper.** `D.residual_influence(UO, resp)` now holds the corpus
   definition of the residual and influence criterion (the regressions of the absolute residuals on
   the predicted values and of the residuals on run order, at `THRESHOLDS["residual_alpha"]`, and
   Cook's distance against `THRESHOLDS["cook_factor"]`/n). Use it for the criterion's results in
   place of the document's own computation, and assert that the two agree before you remove yours.
   The deletion analysis (PD-005-02) stays as it is.
8. **Held pools** (owner Q1): the criteria in force, as the report already does. Check it is stated.

## Gate and report

Gate with `check_render.py --render`; render the pdf and the docx; read the page images of every table
and figure you changed. Keep `status-PCR-005.md` in this folder current (append a "Re-opened
2026-10-10" log). Report: which model you are, each item with where it was resolved, the check_render
passes, the page count, and any `<<NEEDS:>>` left (there should be none).
