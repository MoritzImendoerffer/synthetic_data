"""Design-of-experiments analysis engine for the characterization reports.

Turns the seeded DoE datasets (``outputs/data/doe_<key>_{screening,rsm}.csv``)
into the full statistical content a Stage-1 characterization report needs:
factor legends, effect/coefficient tables with standard errors and significance,
model-adequacy summaries (R^2 / adjusted / predicted R^2, F), ANOVA with
lack-of-fit from the center-point replicates, design matrices for the appendices,
center-point reproducibility, and response-surface contour / diagnostic figures.

Everything is computed from the seeded data with statsmodels, so every table and
figure is reproducible and consistent with the model. Reusable for any unit
operation that has DoE data (factors/responses come from ``amab_process.studies``).
"""
from __future__ import annotations

import itertools

import numpy as np
import pandas as pd
import statsmodels.api as sm

from _pcpkg import CFG, cqa_reg, csv, st

RESP_LABEL = {
    "afucosylation": "Afucosylation", "galactosylation": "Galactosylation",
    "high_mannose": "High mannose", "acidic_variants": "Acidic variants",
    "aggregates_hmw": "Aggregates (HMW)",
    # downstream unit-operation responses (protein_a, viral_inactivation, cex, aex, vf)
    "pool_hcp_ng_mg": "Pool HCP (ng/mg)", "hcp_out_ng_mg": "Pool HCP (ng/mg)",
    "leached_protein_a_ppm": "Leached Protein A (ppm)", "step_yield": "Step yield",
    "aggregate_out_pct": "Aggregates (HMW, %)",
    "xmulv_lrf": "XMuLV LRF (log₁₀)", "mvm_lrf": "MVM LRF (log₁₀)",
}
_LETTERS = "ABCDEFGH"


def screening_factors(key):
    return st.DOE_FACTORS[key]


def rsm_factors(key):
    # Mirror studies.rsm_doe: use the explicit RSM_TOP subset if defined,
    # otherwise the first four screening factors (the CCD default).
    return st.RSM_TOP.get(key, screening_factors(key)[:4])


def responses(key):
    return st.DOE_RESPONSES[key]


def factor_letters(key):
    """Stable factor->letter map (screening order), reused for the RSM terms."""
    return {f: _LETTERS[i] for i, f in enumerate(screening_factors(key))}


def factor_legend_df(key):
    lmap = factor_letters(key)
    names = {p.key: p.name for p in CFG.unit_op(key).parameters}
    units = {p.key: p.unit for p in CFG.unit_op(key).parameters}
    rows = [[lmap[f], names.get(f, f), units.get(f, ""),
             "screening + RSM" if f in rsm_factors(key) else "screening"]
            for f in screening_factors(key)]
    return pd.DataFrame(rows, columns=["Code", "Factor", "Unit", "Studied in"])


def _term_label(name, lmap):
    if name == "const":
        return "Intercept"
    if name.endswith("^2"):
        return lmap[name[:-2]] + "²"
    if ":" in name:
        a, b = name.split(":")
        return lmap[a] + lmap[b]
    return lmap[name]


def _design(df, factors, quadratic):
    X = pd.DataFrame(index=df.index)
    names = list(factors)
    for f in factors:
        X[f] = df["coded_" + f]
    for a, b in itertools.combinations(factors, 2):
        X[f"{a}:{b}"] = df["coded_" + a] * df["coded_" + b]
        names.append(f"{a}:{b}")
    if quadratic:
        for f in factors:
            X[f"{f}^2"] = df["coded_" + f] ** 2
            names.append(f"{f}^2")
    return sm.add_constant(X), names


def has_superseded(key, kind="screening"):
    """True if a real superseded (re-executed) DoE dataset exists for this step/kind."""
    import os
    from _pcpkg import DATA
    return os.path.exists(os.path.join(DATA, f"doe_{key}_{kind}_superseded.csv"))


def fit(key, kind, resp, superseded=False):
    """Fit the coded model (2FI for screening, full quadratic for RSM) + diagnostics.

    ``superseded=True`` fits the invalidated first-execution dataset
    (``doe_<key>_<kind>_superseded.csv``) instead of the reported one — used to show that
    an anomalous interaction present in the superseded data is absent from the requalified
    data (Deviation root-cause confirmation)."""
    suffix = "_superseded" if superseded else ""
    df = csv(f"doe_{key}_{kind}{suffix}.csv")
    factors = rsm_factors(key) if kind == "rsm" else screening_factors(key)
    quad = kind == "rsm"
    Xc, names = _design(df, factors, quad)
    m = sm.OLS(df[resp], Xc).fit()
    h = m.get_influence().hat_matrix_diag
    press = float(np.sum((m.resid.values / (1 - h)) ** 2))
    sst = float(np.sum((df[resp] - df[resp].mean()) ** 2))
    pred_r2 = 1 - press / sst if sst > 0 else np.nan
    cen = df[df.run_type == "center"][resp]
    df_pe = len(cen) - 1
    ss_pe = float(((cen - cen.mean()) ** 2).sum())
    sse = float((m.resid ** 2).sum())
    df_lof = int(m.df_resid) - df_pe
    ss_lof = max(sse - ss_pe, 0.0)
    f_lof = (ss_lof / df_lof) / (ss_pe / df_pe) if (df_pe > 0 and df_lof > 0 and ss_pe > 0) else np.nan
    from scipy import stats as _ss
    p_lof = float(_ss.f.sf(f_lof, df_lof, df_pe)) if np.isfinite(f_lof) else np.nan
    return dict(model=m, df=df, factors=factors, names=names, quad=quad,
                n=int(m.nobs), R2=m.rsquared, adjR2=m.rsquared_adj, predR2=pred_r2,
                F=m.fvalue, p=m.f_pvalue, rmse=float(np.sqrt(m.mse_resid)),
                ss_pe=ss_pe, df_pe=df_pe, ss_lof=ss_lof, df_lof=df_lof,
                F_lof=f_lof, p_lof=p_lof, sse=sse)


def _sig(p):
    return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""


def screening_effects_df(key, resp, top=None, superseded=False):
    """Effect estimates (effect = 2*coef on coded factors), sorted by |effect|.

    ``superseded=True`` reports the effects from the invalidated first execution — e.g. to
    show the anomalous protein-load × wash-1-conductivity interaction that appears there and
    is absent from the requalified data reported in the body."""
    r = fit(key, "screening", resp, superseded=superseded)
    m, lmap = r["model"], factor_letters(key)
    rows = []
    for name in r["names"]:
        c = m.params[name]
        rows.append([_term_label(name, lmap), 2 * c, c, m.bse[name], m.tvalues[name],
                     m.pvalues[name], _sig(m.pvalues[name])])
    d = pd.DataFrame(rows, columns=["Term", "Effect", "Coef.", "Std. err.", "t", "p-value", "Sig."])
    d = d.reindex(d["Effect"].abs().sort_values(ascending=False).index)
    return d.head(top) if top else d


def rsm_coeff_df(key, resp):
    """Full quadratic-model coefficient table in model order (Intercept, main, 2FI, quad)."""
    r = fit(key, "rsm", resp)
    m, lmap = r["model"], factor_letters(key)
    order = ["const"] + r["names"]
    rows = [[_term_label(n, lmap), m.params[n], m.bse[n], m.tvalues[n], m.pvalues[n], _sig(m.pvalues[n])]
            for n in order]
    return pd.DataFrame(rows, columns=["Term", "Coef.", "Std. err.", "t", "p-value", "Sig."])


def fit_summary_df(key, kind):
    rows = []
    for resp in responses(key):
        r = fit(key, kind, resp)
        rows.append([RESP_LABEL.get(resp, resp), r["n"], r["R2"], r["adjR2"], r["predR2"],
                     r["F"], r["p"], r["rmse"]])
    return pd.DataFrame(rows, columns=["Response", "N", "R²", "Adj. R²", "Pred. R²",
                                       "F", "p-value", "RMSE"])


def anova_lof_df(key, resp):
    """ANOVA-style model / residual / lack-of-fit / pure-error partition (RSM)."""
    r = fit(key, "rsm", resp)
    m = r["model"]
    ss_model = float(m.ess)
    df_model = int(m.df_model)
    ss_res = r["sse"]
    df_res = int(m.df_resid)
    rows = [
        ["Model", ss_model, df_model, ss_model / df_model, m.fvalue, m.f_pvalue],
        ["Residual", ss_res, df_res, ss_res / df_res if df_res else np.nan, np.nan, np.nan],
        ["  Lack of fit", r["ss_lof"], r["df_lof"],
         r["ss_lof"] / r["df_lof"] if r["df_lof"] else np.nan, r["F_lof"], r["p_lof"]],
        ["  Pure error", r["ss_pe"], r["df_pe"],
         r["ss_pe"] / r["df_pe"] if r["df_pe"] else np.nan, np.nan, np.nan],
    ]
    return pd.DataFrame(rows, columns=["Source", "Sum sq.", "df", "Mean sq.", "F", "p-value"])


def design_matrix_df(key, kind):
    """Natural-unit design matrix with responses, for an appendix."""
    df = csv(f"doe_{key}_{kind}.csv")
    factors = rsm_factors(key) if kind == "rsm" else screening_factors(key)
    names = {p.key: p.name for p in CFG.unit_op(key).parameters}
    cols = ["run", "run_type"] + factors + responses(key)
    d = df[cols].copy()
    d = d.rename(columns={"run": "Run", "run_type": "Type",
                          **{f: names.get(f, f) for f in factors},
                          **{r: RESP_LABEL.get(r, r) for r in responses(key)}})
    return d


def coded_matrix_df(key, kind):
    """Coded (±1/0) design matrix with letter-coded factors + responses (compact appendix)."""
    df = csv(f"doe_{key}_{kind}.csv")
    factors = rsm_factors(key) if kind == "rsm" else screening_factors(key)
    lmap = factor_letters(key)
    d = pd.DataFrame({"Run": df["run"].astype(int), "Type": df["run_type"]})
    for f in factors:
        d[lmap[f]] = df["coded_" + f].round().astype(int)
    for r in responses(key):
        d[RESP_LABEL.get(r, r)] = df[r]
    return d


def planned_matrix_df(key, kind, coded=True):
    """Design matrix with the RESPONSE COLUMNS REMOVED — the form a protocol may show.

    A `PCP-00N` protocol is prospective: it states the design that will be executed, and
    must not display measured results. `design_matrix_df` / `coded_matrix_df` both append
    the responses, so a plan needs this stripped variant. Both plan documents had
    re-implemented it locally; use this instead.

    coded=True gives the letter-coded ±1/0 matrix, coded=False the natural-unit one.
    """
    df = coded_matrix_df(key, kind) if coded else design_matrix_df(key, kind)
    labels = {RESP_LABEL.get(r, r) for r in responses(key)}
    return df[[c for c in df.columns if c not in labels]]


def center_cv_df(key, kind):
    """Center-point mean / SD / %CV per response (reproducibility / pure error)."""
    df = csv(f"doe_{key}_{kind}.csv")
    cen = df[df.run_type == "center"]
    rows = []
    for resp in responses(key):
        v = cen[resp]
        rows.append([RESP_LABEL.get(resp, resp), len(v), v.mean(), v.std(ddof=1),
                     100 * v.std(ddof=1) / v.mean() if v.mean() else np.nan])
    return pd.DataFrame(rows, columns=["Response", "n", "Mean", "SD", "%CV"])


# --------------------------------------------------------------------------- #
# Figures (built with matplotlib; Quarto captures the current figure).        #
# --------------------------------------------------------------------------- #
def _predict_grid(r, xf, yf, n=40):
    """Predict over xf x yf with every other factor at coded 0, the design centre."""
    m = r["model"]
    grid = np.linspace(-1, 1, n)
    XX, YY = np.meshgrid(grid, grid)
    data = {}
    for f in r["factors"]:
        data[f] = (XX if f == xf else YY if f == yf else np.zeros_like(XX)).ravel()
    X = pd.DataFrame({"const": np.ones(XX.size)})
    for f in r["factors"]:
        X[f] = data[f]
    for a, b in itertools.combinations(r["factors"], 2):
        X[f"{a}:{b}"] = data[a] * data[b]
    if r["quad"]:
        for f in r["factors"]:
            X[f"{f}^2"] = data[f] ** 2
    Z = m.predict(X[["const"] + r["names"]]).values.reshape(XX.shape)
    return XX, YY, Z


def _natural(coded, key, f):
    p = CFG.unit_op(key).param(f)
    lo, hi = p.prange
    mid = (lo + hi) / 2
    return mid + coded * (hi - lo) / 2


def fig_rsm_contours(key, xf="pH", yf="duration"):
    """Panel of RSM response surfaces over two factors, the others at the DESIGN CENTRE.

    The grid adapts to the number of responses (bioreactor: 5 -> 2x3;
    protein_a / most downstream steps: 3 -> 1x3; aex: 4 -> 2x2).

    Note the figure's own title says "set-point", and the design centre is not the set-point
    for six factors across three steps. That mismatch is deliberate and registered as D-001
    in ``authoring/DISCREPANCIES.md`` — the code is honest, the rendered documents carry the
    discrepancy. Do not "fix" the title without removing the D-001 entry.
    """
    import matplotlib.pyplot as plt
    resps = responses(key)
    names = {p.key: p.name for p in CFG.unit_op(key).parameters}
    n = len(resps)
    ncols = 3 if n >= 5 else (2 if n == 4 else n)
    nrows = -(-n // ncols)  # ceil
    fig, axes = plt.subplots(nrows, ncols, figsize=(min(11, 3.7 * ncols), 3.3 * nrows),
                             squeeze=False)
    axes = axes.ravel()
    for ax, resp in zip(axes, resps):
        r = fit(key, "rsm", resp)
        XX, YY, Z = _predict_grid(r, xf, yf)
        xn = _natural(XX, key, xf)
        yn = _natural(YY, key, yf)
        cs = ax.contourf(xn, yn, Z, levels=12, cmap="viridis")
        ax.contour(xn, yn, Z, levels=6, colors="white", linewidths=0.4, alpha=0.6)
        fig.colorbar(cs, ax=ax, shrink=0.85)
        ax.set_title(RESP_LABEL.get(resp, resp), fontsize=10)
        ax.set_xlabel(names.get(xf, xf), fontsize=8)
        ax.set_ylabel(names.get(yf, yf), fontsize=8)
        ax.tick_params(labelsize=7)
    for ax in axes[len(resps):]:
        ax.axis("off")
    fig.suptitle("Response-surface predictions (remaining factors held at set-point)", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    return fig


def fig_diagnostics(key, resp):
    """Residuals-vs-predicted, normal-QQ and actual-vs-predicted for one response (RSM)."""
    import matplotlib.pyplot as plt
    import scipy.stats as ss
    r = fit(key, "rsm", resp)
    m = r["model"]
    fitted = m.fittedvalues.values
    resid = m.resid.values
    std_resid = resid / (r["rmse"] if r["rmse"] else 1.0)
    actual = r["df"][resp].values
    fig, ax = plt.subplots(1, 3, figsize=(11, 3.4))
    ax[0].scatter(fitted, std_resid, s=18, color="#2a78d6")
    ax[0].axhline(0, color="grey", lw=0.8)
    ax[0].set_xlabel("Predicted"); ax[0].set_ylabel("Std. residual")
    ax[0].set_title("Residuals vs predicted", fontsize=10)
    ss.probplot(std_resid, plot=ax[1])
    ax[1].set_title("Normal Q–Q", fontsize=10)
    lim = [min(actual.min(), fitted.min()), max(actual.max(), fitted.max())]
    ax[2].scatter(actual, fitted, s=18, color="#2a78d6")
    ax[2].plot(lim, lim, color="grey", lw=0.8)
    ax[2].set_xlabel("Actual"); ax[2].set_ylabel("Predicted")
    ax[2].set_title("Actual vs predicted", fontsize=10)
    fig.suptitle(f"Model diagnostics — {RESP_LABEL.get(resp, resp)}", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    return fig


# --------------------------------------------------------------------------- #
# Proven acceptable ranges (PAR).                                             #
# --------------------------------------------------------------------------- #
# For each parameter x CQA the step governs, the PAR is the sub-range of the
# parameter's CHARACTERIZATION range over which the CQA stays within its (study-
# provided) acceptance criterion. Two analyses:
#   1. at-set-point  — the other factors held at set-point (coded 0);
#   2. NOR-propagated — the other factors varied within their NOR by Monte-Carlo
#      of the fitted response-surface model (+ residual noise), so the PAR holds
#      even when the rest of the operating point moves within its normal range.
# Acceptance criteria come from the A-Mab study (cqa_register.csv, DS-level), so no
# backward-clearance calculation is needed. Deterministic (fixed PAR_SEED); the MC
# is the reproducible default and is factored so a Bayesian (bambi/PyMC) posterior-
# predictive backend could replace `_mc_predictive` later without touching callers.
PAR_SEED = 20240724
PAR_MC_N = 2000          # Monte-Carlo draws per grid point
PAR_GRID = 81            # grid points across the characterization range, NOR-propagated scan
PAR_CENTRE_GRID = 201    # grid points across the characterization range, design-centre scan

# response key -> CQA-register key (for responses not named as a CQA key directly)
RESP_TO_CQA = {
    "hcp_out_ng_mg": "hcp", "pool_hcp_ng_mg": "hcp", "xmulv_lrf": "lrv_xmulv",
    "mvm_lrf": "lrv_mvm", "leached_protein_a_ppm": "leached_protein_a",
    "aggregate_out_pct": "aggregates_hmw", "residual_dna": "residual_dna",
}


# viral-clearance responses are STEP contributions to a CUMULATIVE requirement, so their
# step-level acceptance is back-calculated (not the DS spec). Maps a step key to its row in
# viral_clearance.csv.
VIRAL_STEP_ROW = {"viral_inactivation": "Low-pH Viral Inactivation",
                  "aex": "Anion Exchange (AEX)", "virus_filtration": "Virus Filtration"}
VIRAL_COL = {"mvm_lrf": ("MVM", "lrv_mvm"), "xmulv_lrf": ("XMuLV", "lrv_xmulv")}


def acceptance_for(key, resp):
    """(acc_low, acc_high, spec_type) for a step's response, or None if it maps to no CQA.

    spec_type is 'upper' (impurity ceiling), 'lower' (clearance floor) or 'two_sided'.
    For impurities and formed CQAs the acceptance is the study-provided DS-level criterion
    (cqa_register.csv). For a viral-clearance response the criterion is the STEP's required
    log-reduction, back-calculated from the cumulative requirement minus the other steps'
    nominal contribution (modular clearance) — the only case needing a backward calculation."""
    if resp in VIRAL_COL:
        col, cqa_key = VIRAL_COL[resp]
        floor = float(cqa_reg[cqa_reg["key"] == cqa_key].iloc[0]["acc_low"])
        step_row = VIRAL_STEP_ROW.get(key)
        vc = csv("viral_clearance.csv")
        if step_row is not None and step_row in set(vc["step"]):
            cum = float(vc[vc["step"] == "Cumulative"].iloc[0][col])
            stepv = float(vc[vc["step"] == step_row].iloc[0][col])
            return max(floor - (cum - stepv), 0.0), float("inf"), "lower"
        return floor, float("inf"), "lower"
    cqa_key = resp if resp in set(cqa_reg["key"]) else RESP_TO_CQA.get(resp)
    if cqa_key is None:
        return None
    row = cqa_reg[cqa_reg["key"] == cqa_key]
    if row.empty:
        return None
    row = row.iloc[0]
    return float(row["acc_low"]), float(row["acc_high"]), str(row["spec_type"])


# --------------------------------------------------------------------------------------
# Public prediction API.
#
# Documents need to evaluate a fitted response-surface model at settings of their own
# choosing — a worst-case corner, the edges of the NOR box, a 1-D scan for an edge of
# failure. Before these wrappers existed the only route was the private `_predict_points`
# / `_to_coded` / `_natural` / `_in_spec`, and every authored report reached for them. That
# is a missing public API, not an author error: use these instead.
# --------------------------------------------------------------------------------------
def to_coded(key, f, natural):
    """Natural units -> coded (-1..+1 over the characterization range) for one factor."""
    return _to_coded(natural, key, f)


def to_natural(key, f, coded):
    """Coded (-1..+1) -> natural units for one factor."""
    return _natural(np.asarray(coded, dtype=float), key, f)


def predict(key, resp, kind="rsm", coded=None, natural=None, superseded=False):
    """Predict `resp` at given factor settings. Returns a numpy array.

    Give exactly one of ``coded`` or ``natural``, each a mapping factor -> value (scalars or
    equal-length sequences). Factors you omit are held at the design centre (coded 0), which
    is the characterization-range midpoint and is NOT necessarily the set-point — check
    ``CFG.unit_op(key).param(f).setpoint`` if the distinction matters for your claim.

        D.predict("bioreactor", "galactosylation",
                  natural={"pH": 6.60, "temperature": 35.8, "duration": 15})

    The prediction is the fitted model's mean response. It carries no interval, so do not
    present it as an assurance statement without one (see `par_nor_propagated` for the
    NOR-propagated form used in the PAR analysis).
    """
    if (coded is None) == (natural is None):
        raise ValueError("give exactly one of coded= or natural=")
    r = fit(key, kind, resp, superseded=superseded)
    settings = {}
    if natural is not None:
        for f, v in natural.items():
            if f not in r["factors"]:
                raise KeyError(f"{f!r} is not a factor of the {key} {kind} model "
                               f"(factors: {r['factors']})")
            settings[f] = np.atleast_1d(_to_coded(v, key, f))
    else:
        for f, v in coded.items():
            if f not in r["factors"]:
                raise KeyError(f"{f!r} is not a factor of the {key} {kind} model "
                               f"(factors: {r['factors']})")
            settings[f] = np.atleast_1d(np.asarray(v, dtype=float))
    n = max((len(v) for v in settings.values()), default=1)
    grid = pd.DataFrame({f: np.full(n, 0.0) for f in r["factors"]})
    for f, v in settings.items():
        grid[f] = v if len(v) == n else np.full(n, v[0])
    return _predict_points(r, grid)


def meets_acceptance(key, resp, values):
    """Boolean array: does each predicted value meet this response's acceptance criterion?

    Uses `acceptance_for(key, resp)`, so viral-clearance responses are judged against the
    back-calculated STEP floor rather than the cumulative requirement. Returns None when the
    response maps to no acceptance criterion (e.g. step yield)."""
    acc = acceptance_for(key, resp)
    if acc is None:
        return None
    lo, hi, stype = acc
    return _in_spec(np.asarray(values, dtype=float), lo, hi, stype)


def _to_coded(natural, key, f):
    p = CFG.unit_op(key).param(f)
    lo, hi = p.prange
    return (np.asarray(natural, dtype=float) - (lo + hi) / 2) / ((hi - lo) / 2)


def _predict_points(r, coded):
    """Predict the fitted model at coded factor settings (DataFrame of factor columns)."""
    X = pd.DataFrame({"const": np.ones(len(coded))}, index=coded.index)
    for f in r["factors"]:
        X[f] = np.asarray(coded[f], dtype=float)
    for a, b in itertools.combinations(r["factors"], 2):
        X[f"{a}:{b}"] = X[a].values * X[b].values
    if r["quad"]:
        for f in r["factors"]:
            X[f"{f}^2"] = X[f].values ** 2
    return np.asarray(r["model"].predict(X[["const"] + r["names"]]))


def _in_spec(y, lo, hi, stype):
    if stype == "upper":
        return y <= hi
    if stype == "lower":
        return y >= lo
    return (y >= lo) & (y <= hi)


def _contiguous_range(xs, mask, center=0.0):
    """The contiguous True interval of `mask` containing the grid point nearest `center`;
    (xs_lo, xs_hi) or None if the centre itself is not acceptable."""
    ci = int(np.argmin(np.abs(xs - center)))
    if not bool(mask[ci]):
        return None
    lo = ci
    while lo > 0 and bool(mask[lo - 1]):
        lo -= 1
    hi = ci
    while hi < len(xs) - 1 and bool(mask[hi + 1]):
        hi += 1
    return float(xs[lo]), float(xs[hi])


def par_at_design_centre(key, resp, factor, n_grid=PAR_CENTRE_GRID):
    """PAR of `factor` for `resp` with all other factors at the DESIGN CENTRE (coded 0).

    The design centre is the midpoint of each factor's characterization range. It is **not**
    the set-point, and for six response-surface factors it differs:

        viral_inactivation  ph 3.5 vs 3.6 · hold_time 90 vs 120 · temperature 21 vs 20
        aex                 load 200 vs 175
        virus_filtration    filtration_volume 90 vs 95 · pressure 13 vs 19

    **This is a REGISTERED DISCREPANCY, deliberately preserved — do not "fix" it silently.**
    The approved protocols commit to the set-point (PCP-006: "The first holds the other
    parameters at their set-points"; PCP-008 and PCP-009 likewise), so the executed analysis
    departs from the method its own protocol specifies. The reports then present the result
    under a column headed "PAR (set-point)". A review should have caught this and did not.

    It is retained as a benchmark item for cross-document consistency checking, and is
    documented in ``authoring/DISCREPANCIES.md``. Changing the computation, or relabelling
    ``par_table``'s column, would erase it. Read that file before touching either.

    The function name says design centre because the *code* should be honest about what it
    computes; the *documents* carry the discrepancy.
    """
    acc = acceptance_for(key, resp)
    if acc is None:
        return None
    lo, hi, stype = acc
    r = fit(key, "rsm", resp)
    xs = np.linspace(-1, 1, n_grid)
    coded = pd.DataFrame({f: (xs if f == factor else np.zeros(n_grid)) for f in r["factors"]})
    yhat = _predict_points(r, coded)
    par_c = _contiguous_range(xs, _in_spec(yhat, lo, hi, stype))
    return {"factor": factor, "resp": resp, "acc": acc, "xs_nat": _natural(xs, key, factor),
            "y": yhat, "par_coded": par_c,
            "par_nat": None if par_c is None else (_natural(par_c[0], key, factor),
                                                   _natural(par_c[1], key, factor))}


def _mc_predictive(r, key, factor, x_coded, others, rng, n_mc):
    """Monte-Carlo predictive draws of the response at target `factor`=x_coded with the
    `others` varied within their NOR (~N(set-point, NOR/6), clipped) + model residual noise.
    Factored out so a Bayesian posterior-predictive backend can replace it later."""
    coded = pd.DataFrame({factor: np.full(n_mc, x_coded)})
    for g in others:
        p = CFG.unit_op(key).param(g)
        w = max((p.nor[1] - p.nor[0]) / 6.0, 1e-9)
        nat = np.clip(rng.normal(p.setpoint, w, n_mc), p.prange[0], p.prange[1])
        coded[g] = _to_coded(nat, key, g)
    return _predict_points(r, coded[r["factors"]]) + rng.normal(0.0, r["rmse"], n_mc)


def par_nor_propagated(key, resp, factor, n_grid=PAR_GRID, n_mc=PAR_MC_N):
    """PAR of `factor` for `resp` with the other factors varying within their NOR.

    The PAR is the range of `factor` over which the 95% predictive interval of the CQA
    (from the NOR Monte-Carlo of the fitted model) stays within acceptance — a robustness
    criterion, so it is narrower than the at-set-point PAR."""
    acc = acceptance_for(key, resp)
    if acc is None:
        return None
    lo, hi, stype = acc
    r = fit(key, "rsm", resp)
    others = [g for g in r["factors"] if g != factor]
    rng = np.random.default_rng(PAR_SEED)
    xs = np.linspace(-1, 1, n_grid)
    med = np.empty(n_grid); p_lo = np.empty(n_grid); p_hi = np.empty(n_grid); p_in = np.empty(n_grid)
    for i, x in enumerate(xs):
        y = _mc_predictive(r, key, factor, x, others, rng, n_mc)
        med[i] = np.median(y); p_lo[i] = np.percentile(y, 2.5); p_hi[i] = np.percentile(y, 97.5)
        p_in[i] = _in_spec(y, lo, hi, stype).mean()
    if stype == "upper":
        mask = p_hi <= hi
    elif stype == "lower":
        mask = p_lo >= lo
    else:
        mask = (p_lo >= lo) & (p_hi <= hi)
    par_c = _contiguous_range(xs, mask)
    return {"factor": factor, "resp": resp, "acc": acc, "xs_nat": _natural(xs, key, factor),
            "med": med, "p_lo": p_lo, "p_hi": p_hi, "p_in": p_in, "par_coded": par_c,
            "par_nat": None if par_c is None else (_natural(par_c[0], key, factor),
                                                   _natural(par_c[1], key, factor))}


def governing_factor(key, resp):
    """The RSM factor with the largest absolute main effect on `resp` — its governing
    parameter, used for the representative PAR plot."""
    lmap = factor_letters(key)
    letter_to_factor = {lmap[f]: f for f in rsm_factors(key)}
    for term in screening_effects_df(key, resp)["Term"]:
        if term in letter_to_factor:
            return letter_to_factor[term]
    return rsm_factors(key)[0]


def _par_str(par_nat, unit=""):
    if par_nat is None:
        return "none (set-point breaches)"
    lo, hi = par_nat
    u = f" {unit}" if unit else ""
    return f"{lo:.3g}–{hi:.3g}{u}"


def par_table(key):
    """PAR table: for each governed CQA x RSM factor, the characterization range and both
    PARs (at-set-point and NOR-propagated), in natural units."""
    names = {p.key: p.name for p in CFG.unit_op(key).parameters}
    units = {p.key: p.unit for p in CFG.unit_op(key).parameters}
    rows = []
    for resp in responses(key):
        if acceptance_for(key, resp) is None:
            continue
        for factor in rsm_factors(key):
            p = CFG.unit_op(key).param(factor)
            ps = par_at_design_centre(key, resp, factor)
            pn = par_nor_propagated(key, resp, factor)
            rows.append([RESP_LABEL.get(resp, resp), names.get(factor, factor),
                         f"{p.prange[0]:g}–{p.prange[1]:g}", units.get(factor, ""),
                         _par_str(ps["par_nat"]), _par_str(pn["par_nat"])])
    return pd.DataFrame(rows, columns=["CQA", "Parameter", "Char. range", "Unit",
                                       "PAR (set-point)", "PAR (NOR)"])


def acceptance_table(key):
    """Per-response acceptance criteria for a step, with the basis of each.

    The prospective counterpart of :func:`par_table`. A protocol has to state what each
    measured response must achieve *before* any data exist, and the two bases differ: an
    impurity or formed CQA is judged against the study-provided drug-substance criterion,
    while a viral-clearance response is judged against the STEP contribution
    back-calculated by :func:`acceptance_for` from the cumulative requirement. Responses
    that map to no CQA (e.g. step yield) are omitted, as they are in ``par_table``.
    """
    rows = []
    for resp in responses(key):
        acc = acceptance_for(key, resp)
        if acc is None:
            continue
        lo, hi, stype = acc
        if resp in VIRAL_COL:
            cqa_key = VIRAL_COL[resp][1]
            unit, crit = "log₁₀ (this step)", f"≥ {lo:.2f}"
            basis = "Cumulative requirement less the clearance credited to the other steps"
        else:
            cqa_key = resp if resp in set(cqa_reg["key"]) else RESP_TO_CQA.get(resp)
            unit = str(cqa_reg[cqa_reg["key"] == cqa_key].iloc[0]["unit"])
            crit = (f"≤ {hi:g}" if stype == "upper" else
                    f"≥ {lo:g}" if stype == "lower" else f"{lo:g}–{hi:g}")
            basis = "Drug-substance specification"
        cqa_name = str(cqa_reg[cqa_reg["key"] == cqa_key].iloc[0]["cqa"])
        rows.append([RESP_LABEL.get(resp, resp), cqa_name, crit, unit, basis])
    return pd.DataFrame(rows, columns=["Response", "Quality attribute",
                                       "Acceptance criterion", "Unit", "Basis"])


def fig_par(key, resp, factor):
    """Two-panel PAR figure for one (CQA, parameter): at-set-point (left) and
    NOR-propagated (right). Parameter on x, response on y, acceptance limits drawn, and the
    acceptable parameter region shaded green; set-point and NOR marked."""
    import matplotlib.pyplot as plt
    ps = par_at_design_centre(key, resp, factor)
    pn = par_nor_propagated(key, resp, factor)
    lo, hi, stype = ps["acc"]
    p = CFG.unit_op(key).param(factor)
    pname = {pp.key: pp.name for pp in CFG.unit_op(key).parameters}.get(factor, factor)
    unit = p.unit
    label = RESP_LABEL.get(resp, resp)
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)

    def _limits(a):
        if stype in ("upper", "two_sided") and np.isfinite(hi):
            a.axhline(hi, color="#c0392b", lw=1.0, ls="--", label="acceptance limit")
        if stype in ("lower", "two_sided") and lo > 0:
            a.axhline(lo, color="#c0392b", lw=1.0, ls="--",
                      label=None if stype == "two_sided" else "acceptance limit")

    def _marks(a):
        a.axvline(p.setpoint, color="grey", lw=0.9, ls=":")
        a.axvspan(p.nor[0], p.nor[1], color="grey", alpha=0.12, lw=0, label="NOR")

    def _shade(a, par_nat):
        if par_nat is not None:
            a.axvspan(par_nat[0], par_nat[1], color="#2ecc71", alpha=0.25, lw=0,
                      label="PAR (acceptable)")

    ax[0].plot(ps["xs_nat"], ps["y"], color="#2a78d6", lw=1.6)
    _limits(ax[0]); _shade(ax[0], ps["par_nat"]); _marks(ax[0])
    ax[0].set_title("At set-point (others fixed)", fontsize=10)
    ax[0].set_xlabel(f"{pname} ({unit})"); ax[0].set_ylabel(label)

    ax[1].plot(pn["xs_nat"], pn["med"], color="#2a78d6", lw=1.6, label="median")
    ax[1].fill_between(pn["xs_nat"], pn["p_lo"], pn["p_hi"], color="#2a78d6", alpha=0.18,
                       lw=0, label="95% predictive")
    _limits(ax[1]); _shade(ax[1], pn["par_nat"]); _marks(ax[1])
    ax[1].set_title("Others varying within NOR (Monte-Carlo)", fontsize=10)
    ax[1].set_xlabel(f"{pname} ({unit})")

    h, l = ax[1].get_legend_handles_labels()
    ax[1].legend(h, l, fontsize=7, loc="best")
    fig.suptitle(f"Proven acceptable range — {label} vs {pname}", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    return fig
