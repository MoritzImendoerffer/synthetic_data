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

## Resolution (author pass, 2026-10-10, Claude Opus 5.5)

All eight items are done in `pc_package/PCR-005_protein_a.qmd`. The backup is
`PCR-005_protein_a.pre-datastate.qmd` in this folder. Section numbers are those of the rendered PDF
(69 pp). Details and values are in `status-PCR-005.md` §4.

1. Done. §6 is rewritten on the single-batch limit and names the statistic where the region is defined.
   The mean-based region (97.5 %) is given once, as a comparison. Every fraction, the binding output and
   the excluded region are recomputed on the grid of 41. The setup assert now checks the single-batch
   definition independently through `D.prediction_interval` for all three outputs with a criterion.
   Fragments are judged too, because the helper's response list leaves them out. The statistic is also
   named in F7, §3.5, §5.8, §7.3 and Conclusion 6. No figure or table draws the region.
2. Done. §13.2 gives the rule from the record with its 99 % level and the interval at the run's settings
   (`D.oot_check`, 1.38–5.12 ppm). The first result lies outside it and the re-assay inside. The first
   result now lies above the range of the other runs, and the asserts follow the data. The analysis with
   the first result in place was recomputed: an adequate, significant end-of-pool-collect model, with the
   judgement, the PARs and the class unchanged. §5.3.3 follows.
3. Done. §7.1, risk item 2 names the release test (ELISA, AMV-3012), its LOQ and its coverage (80 %, 2D
   western blot against the platform CHO antigen).
4. Done. §2.2 and §8 give DNA in pg/mg up to the drug substance and in ng/dose at it. The dose and the
   70 kg assumption are stated. The drug substance level, the Cpk and the count out of specification come
   from the data. The 5-log anion exchange reduction is stated as not measured (pools < LOQ).
5. Done. §3.3, §4.4, §5.6 (Table 5.15 gains HMW and LMW by SEC, and a new paragraph), §9 (the classes of
   temperature and bed height rest for fragments on the mechanism and the response-surface model), F10 and
   the Discussion. No sentence now says that the univariate study measured no size variant, and no nrCE-SDS
   fragment result is claimed from it.
6. Done. §3.1 item 4, §5.3.1, F1, the Discussion and Conclusion 2 say that the selected model decides, as
   the rule states, and that the others are a sensitivity.
7. Done. Every criterion-5 result now comes from `D.residual_influence`. Its exact agreement with the own
   computation was asserted and gated before the own computation was removed. The thresholds come from
   `THRESHOLDS`, and the deletion analysis is unchanged.
8. Done. §4.5 states that the held eluate is judged against the criteria in force, not the a priori values.

Gate: final `check_render.py` green (no `<<NEEDS:>>`). The pdf and docx render with exit 0. The page
images of the changed tables were read.

Raised for the coordinator (not changed, outside this list):
- PCR-005 §7.1 paraphrases the widening rule without the F-test and exact-fit conditions that PCMP-001 §7.5
  now states. This is wording only, because the anion exchange model has F-test p = 2.7e-13.
- `D.design_space_grid` ignores fragments.
- PCP-005 Version 2.0 §6.4 lists no SEC responses for S-PA-UNI.
- The DEV-005-02 `oot_rule` names "the selected model", which is anachronistic for a review made in
  January to February 2026.
- The annex needs re-anchoring.
