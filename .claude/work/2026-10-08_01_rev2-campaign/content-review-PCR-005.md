# Content review — PCR-005 Version 2.0 draft, run 1 (2026-10-08)

Judge: fresh-context agent, Claude Opus 5.5, with its own recomputation script. Reproduced:
equivalence verdicts and degrees of freedom, the centre-point SD and CV, adjusted R² and F, the
HCP ANOVA, the standard errors, the DEV-005-01 predictions, the NOR range, the 93.2 % design space,
the Cpks, 16,000 / 158 / 2.45, the median SEC bias, residence times.

Verdicts: Q1 No · Q2 No · Q3 sentences present · Q4 No · Q5 many · Q6 No.

## Fixed at the source (the orchestrator's)

- **PAR edges rounded outward.** 3.235 printed "3.23", where the analysis had already rejected
  3.23. `doe_report._par_str` now rounds inward (`_inward`). The judge's medium-confidence
  objection to 3.23 was correct.
- **`T.criteria_results`** judged "Met across the NOR" on the mean, against the plan's per-batch
  decision statistic. It now uses mean ± 1.96 residual SD for quality attributes, with a footnote.
- **DEV-005-01's detection** contradicted its use on run 23 (release testing "detected" it). Now:
  a post-run review of the preparation record; release had passed on a mis-standardised meter.
- **DEV-005-02's re-assay value** (1.6 ppm) contradicted the seeded data (minimum 1.70). It now names
  RSM run 11 and carries no value; the table is the re-assay.
- **The leached Protein A scale-effect mechanism** ("rises with cycle number") was backwards.
  Now: a longer load hold at scale, so host cell proteases cleave more ligand. Corrected in
  config, STORY_BIBLE and PCP-005 (one-sentence fix).
- **Disposition tokens** (`supplementary_runs_executed`) now print as words in `dev_register`.

## Returned to the author

End of pool collect and flow rate against Table 5.7 (and the screening-to-RSM sign reversal),
criterion numbering, Cook's distance not met, the hold-study reading, the LOQ for drug-substance
leached Protein A, the design-space definition, Figure 5.3, univariate individual results,
terms, eleven filing or padding items, four causes without direction.

# Run 2 (2026-10-08), fresh judge, Claude Opus 5.5

Almost all arithmetic reproduced: screening effects, equivalence half-widths, ANOVA, run-23
predictions, the univariate deltas, Cpk, the criteria, the hold differences. Verdicts: Q1 No ·
Q2 No · Q3 sentences present · Q4 No · Q5 12 items · Q6 No.

## Fixed at the source

- **The prediction interval.** The engine's per-batch statistic omitted coefficient uncertainty
  and used z. `_mc_predictive` now draws the coefficients from their covariance in every
  simulated batch (Version 2.0 only; Version 1.0 mode unchanged, so it reproduces).
  `tables.criteria_results` uses the exact 95 % prediction interval (`D.prediction_interval`).
  Effect: the Protein A elution pH PAR (NOR) went from 3.24 to 3.26 – 3.9. The bioreactor
  acidic-variant PARs narrowed (temperature 34.9–36). The conclusions otherwise hold.
- **`par_table` criteria** printed "≤ 1.6e+04". Now "≤ 16,000".
- **Complex tables** default to shrink-to-fit (horizontal overflow of Table 7.1 found by the
  author).
- **"Mis-standardised"** is replaced by "incorrectly calibrated" in config.
- **The mechanism file (protein_a) leached-Protein-A entry** is completed with the new-resin fact
  and the load-hold dependence, and marked pending the owner's review.

## Returned to the author (final factual pass, then promotion)

Statistical "governs", model rules broken by the text, the criticality convention, numbers, three
unsupported mechanisms, plan references, two terms, thirteen cuts.
