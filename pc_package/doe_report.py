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

from _pcpkg import CFG, csv, st

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
    """Panel of RSM response surfaces over two factors (others at set-point).

    The grid adapts to the number of responses (bioreactor: 5 -> 2x3;
    protein_a / most downstream steps: 3 -> 1x3; aex: 4 -> 2x2).
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
