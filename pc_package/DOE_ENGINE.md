# The DoE analysis engine (`doe_report.py`)

`doe_report.py` turns the seeded design-of-experiments (DoE) datasets into the
statistical tables and figures a Stage-1 process-characterization **report** needs:
effect estimates, response-surface models, ANOVA with lack-of-fit, design matrices
and diagnostic plots. Everything is computed with `statsmodels` from the CSVs the
process model already writes to `outputs/data/`, so every number is reproducible and
consistent with the rest of the document set — nothing is typed by hand.

This document explains, in plain language, what the engine computes and how to use
it. It assumes no statistics background beyond "we changed some settings and measured
some outcomes."

---

## 1. The idea in one paragraph

A characterization study runs the process many times at different parameter settings
(a *design*), measures the quality attributes each time (the *responses*), and then
fits a formula that predicts each response from the settings. From that formula we
learn which parameters matter, how they interact, and over what region of settings the
product still meets specification (the *design space*). `doe_report.py` does the
fitting and produces the tables/figures; the seeded process model
(`amab_process/`) produced the runs and measurements.

## 2. The two designs it analyzes

For each unit operation the studies engine (`amab_process/studies.py`) produced two
datasets, both stored as `outputs/data/doe_<unit>_<kind>.csv`:

- **Screening** (`kind="screening"`) — a *resolution-V fractional factorial*: a small
  set of runs that changes several parameters at once in a balanced pattern, so we can
  see which parameters and which two-parameter interactions have a real effect, cheaply.
  Think of it as "which knobs matter?"
- **Response surface** (`kind="rsm"`) — a *face-centred central-composite design*: more
  runs on the parameters that survived screening, including centre and mid-edge points,
  so we can also capture *curvature* and build an accurate predictive model. Think of it
  as "now map the important knobs precisely."

Each CSV has one row per run: a `run` index, a `run_type` (`factorial`, `axial` or
`center`), the parameter settings in natural units and in *coded* units (the `coded_*`
columns, where the set-point is 0 and the studied range edges are −1 and +1), and one
column per measured response.

## 3. The statistics, in plain language

- **Effect** (screening) — how much a response changes when a parameter goes from its
  low to its high setting. Reported as `effect = 2 × coefficient` on the coded factors;
  larger magnitude = more influential.
- **Coefficient / std. error / t / p-value** — the fitted weight of each term, its
  uncertainty, and whether it is statistically distinguishable from zero. A **p-value <
  0.05** (flagged `*`, `**`, `***`) means the term is significant.
- **R²** — the fraction of the response variation the model explains (1.0 = perfect).
  **Adjusted R²** penalises adding useless terms. **Predicted R²** (computed from the
  PRESS statistic by leaving each run out in turn) estimates how well the model predicts
  *new* runs; if it is close to the adjusted R², the model is not over-fitted.
- **ANOVA + lack-of-fit** — splits the leftover ("residual") variation into
  **lack of fit** (the model missing real structure) and **pure error** (irreducible
  run-to-run noise, measured from the replicated centre points). If the lack-of-fit
  F-test is **not significant (p > 0.05)**, the model is adequate.
- **Centre-point %CV** — the run-to-run reproducibility at the set-point; it is the
  pure-error estimate and a direct read-out of process + assay noise.

> **Practical caveat.** A full 15-term model fitted to the 19-run screening design is
> deliberately near-saturated — it is for *identifying* active effects, not for
> prediction (its predicted R² is meaningless). The **response-surface model is the
> credible predictive model** and is what defines the design space. The report text
> says this explicitly; keep that framing in any new report.

## 4. Where the numbers come from (grounding & reproducibility)

The engine reads only `outputs/data/doe_<unit>_<kind>.csv`, and takes the factor and
response lists from the registries in `amab_process.studies`
(`DOE_FACTORS`, `RSM_TOP`, `DOE_RESPONSES`). It therefore inherits the master seed and
the config: **re-run `make data` with a different `meta.seed` or different parameter
ranges in `config/parameters.yaml`, and every table and figure updates automatically
and consistently.** No value is hard-coded in the engine or the report.

## 5. API reference

All functions take a `key` — the unit-operation key from the config
(`"bioreactor"`, `"protein_a"`, `"viral_inactivation"`, `"cex"`, `"aex"`,
`"virus_filtration"`). `kind` is `"screening"` or `"rsm"`; `resp` is a response key
(e.g. `"afucosylation"`). Functions ending in `_df` return a pandas `DataFrame` ready
to print with `_pcpkg.show(...)`.

| Function | Returns | Use in the report |
|---|---|---|
| `factor_legend_df(key)` | Code (A–…), Factor, Unit, "Studied in" | the factor-coding legend table |
| `factor_letters(key)` | dict `{factor: letter}` | the factor→letter map (used internally by the legend/terms) |
| `screening_effects_df(key, resp, top=None)` | Term, Effect, Coef., Std. err., t, p-value, Sig. — sorted by \|effect\| | screening effect tables (per response) |
| `fit_summary_df(key, kind)` | Response, N, R², Adj. R², Pred. R², F, p, RMSE (one row per response) | model-adequacy summary |
| `rsm_coeff_df(key, resp)` | Term, Coef., Std. err., t, p-value, Sig. (model order) | response-surface coefficient tables |
| `anova_lof_df(key, resp)` | Source, Sum sq., df, Mean sq., F, p (Model / Residual / Lack of fit / Pure error) | the ANOVA table |
| `center_cv_df(key, kind)` | Response, n, Mean, SD, %CV | centre-point reproducibility |
| `coded_matrix_df(key, kind)` | Run, Type, coded factor columns (A, B, …) + responses | appendix design matrices (compact) |
| `design_matrix_df(key, kind)` | Run, Type, natural factor columns + responses | design matrix in natural units |
| `fig_rsm_contours(key, xf="pH", yf="duration")` | matplotlib `Figure` (2×3 response-surface panel) | design-space / surface figure |
| `fig_diagnostics(key, resp)` | matplotlib `Figure` (residuals, Q–Q, actual-vs-predicted) | model-validation figure |
| `planned_matrix_df(key, kind, coded=True)` | the design matrix **without** responses | a plan's appendix: the design as proposed |
| `fit(key, kind, resp)` | dict of the raw model + all statistics | for custom needs |
| `responses(key)` / `screening_factors(key)` / `rsm_factors(key)` | lists | to loop over responses/factors |
| `has_superseded(key, kind)` | bool | whether a first, superseded execution exists (AEX) |

### Prediction, acceptance and proven acceptable ranges

| Function | Returns | Use in the report |
|---|---|---|
| `predict(key, resp, kind="rsm", coded=…, natural=…)` | predicted response at a point | "the model predicts X at the set-point" |
| `to_coded(key, f, natural)` / `to_natural(key, f, coded)` | scalar | convert between coded and natural units |
| `acceptance_for(key, resp)` | `(low, high)` or one-sided | the criterion the response is judged against |
| `meets_acceptance(key, resp, values)` | bool / array | whether a prediction clears its criterion |
| `par_at_design_centre(key, resp, factor)` | `(low, high)` | the PAR scan with other factors at coded 0 |
| `par_nor_propagated(key, resp, factor)` | `(low, high)` | the PAR with the other factors varied over their NORs |
| `governing_factor(key, resp)` | factor key | which factor binds the range for that response |
| `par_table(key)` | the PAR table as rendered | the report's PAR section |
| `fig_par(key, resp, factor)` | matplotlib `Figure` | the PAR scan figure |

**Read [`../authoring/DISCREPANCIES.md`](../authoring/DISCREPANCIES.md) before touching the PAR
helpers.** `par_at_design_centre` holds the other factors at the design centre, while the
plans commit to the set-point and the rendered column is headed "PAR (set-point)". That gap
is deliberate and registered as D-001. The function name says what it really does; the
document names are what the discrepancy consists of.

Module constant `RESP_LABEL` maps response keys to display names.

### Example (standalone)

```python
import doe_report as D
D.fit_summary_df("bioreactor", "rsm")        # R²/adj/pred per CQA
D.rsm_coeff_df("bioreactor", "afucosylation")# coefficient table
D.anova_lof_df("bioreactor", "afucosylation")# ANOVA with lack-of-fit
```

## 6. Figures

Both figure functions build the plot from the fitted model and return a matplotlib
`Figure`:

- `fig_rsm_contours(key, xf, yf)` — a grid of filled contour plots showing each response
  over two chosen factors, with the others held at the **design centre** (coded 0). Good for
  visualising the design space. The figure's own title says "set-point", which for six
  factors across three steps is not the same point — a deliberate, registered discrepancy
  (D-001 in [`../authoring/DISCREPANCIES.md`](../authoring/DISCREPANCIES.md)). Do not correct
  the title without removing that entry.
- `fig_diagnostics(key, resp)` — residuals-vs-predicted, a normal Q–Q plot and
  actual-vs-predicted, the standard checks that a model is trustworthy.

## 7. Using it inside a Quarto document

Tables (with `#| output: asis`):

````markdown
```{python}
#| output: asis
show(D.rsm_coeff_df(UO, "afucosylation"), floatfmt=".3g")
```

: Response-surface coefficients for afucosylation. {#tbl-coef-afuc}
````

Figures (Quarto captures the current matplotlib figure):

````markdown
```{python}
#| label: fig-contours
#| fig-cap: "Response surfaces for the CQAs over culture pH × culture duration."
D.fig_rsm_contours(UO)
plt.show()
```
````

## 8. Adding another unit operation

1. Confirm the unit has DoE data: `outputs/data/doe_<key>_screening.csv` and
   `..._rsm.csv` exist (they do for `bioreactor`, `protein_a`, `viral_inactivation`,
   `cex`, `aex`, `virus_filtration`).
2. Reuse every function above with the new `key` — nothing else to change; factors and
   responses come from the studies registries automatically.
3. Pick the two most influential factors for `fig_rsm_contours(key, xf=…, yf=…)`.

**Steps without DoE** — harvest (Step 4) and UF/DF (Step 10) were not characterized by
DoE; their reports present univariate/qualitative characterization and do **not** call
this engine. Do not fabricate a DoE for them.

## 9. Dependencies

`statsmodels`, `scipy`, `numpy`, `pandas`, `matplotlib` (all already in
`requirements.txt`). The engine imports shared paths/config from `_pcpkg.py`.
