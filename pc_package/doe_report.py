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
from amab_process import adequacy as ad
from amab_process.config import characterized_nor  # noqa: F401  (D.characterized_nor())

RESP_LABEL = {
    "afucosylation": "Afucosylation", "galactosylation": "Galactosylation",
    "high_mannose": "High mannose", "acidic_variants": "Acidic variants",
    "aggregates_hmw": "Aggregates (HMW)",
    # downstream unit-operation responses (protein_a, viral_inactivation, cex, aex, vf)
    "pool_hcp_ng_mg": "Pool HCP (ng/mg)", "hcp_out_ng_mg": "Pool HCP (ng/mg)",
    "leached_protein_a_ppm": "Leached Protein A (ppm)", "step_yield": "Step yield",
    "aggregate_out_pct": "Aggregates (HMW, %)",
    "xmulv_lrf": "XMuLV LRF (log₁₀)", "mvm_lrf": "MVM LRF (log₁₀)",
    # Rev 2.0 analytical layer (amab_process/analytics.py)
    "lmw_cesds_pct": "Fragments (LMW, %, nrCE-SDS)", "lmw_sec_pct": "Fragments (LMW, %, SEC)",
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


def fragment_responses(key, kind="rsm", superseded=False):
    """The fragment columns measured on EVERY run of this study (Rev 2.0). A method the plan
    did not run for the study is NaN throughout and is not returned; neither is a column with a
    gap, because a model cannot be fitted to it."""
    try:
        d = csv(f"doe_{key}_{kind}{'_superseded' if superseded else ''}.csv")
    except FileNotFoundError:
        return []
    return [c for c in ("lmw_sec_pct", "lmw_cesds_pct") if c in d.columns and d[c].notna().all()]


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
    if name == ad.BLOCK:
        return "Block"
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


# Which runs and which model a response-surface fit uses (INV-002). By default every run of the
# step, planned and augmentation, with a block term, and the model PCMP-001 §7.2 allows: the full
# quadratic when it is adequate, else the hierarchical refit. ``planned_full_models`` restores the
# full quadratic on the planned runs, which is what Version 1.0 fitted and what INV-001 compared.
_MODELS = {"runs": "all", "form": "auto", "corrected": True}
_FIT_CACHE: dict = {}
TH = {k: float(v) for k, v in CFG.raw()["campaign"]["thresholds"].items()}


class planned_full_models:
    """Context manager: every response-surface fit inside it is the full quadratic model on the
    planned runs, with no augmentation and no refit."""
    def __enter__(self):
        self._old = dict(_MODELS)
        _MODELS.update(runs="planned", form="full", corrected=False)
        return self

    def __exit__(self, *a):
        _MODELS.clear()
        _MODELS.update(self._old)
        return False


def setting_corrections(key, kind="rsm"):
    """[(run, factor, recorded value, deviation)] for the runs of a design that Version 2.0 analyses
    at a recorded setting rather than the design setting (config ``campaign.setting_corrections``;
    the value is read from the deviation record)."""
    events = {e["id"]: e for evs in CFG.raw()["deviations"]["events"].values() for e in evs}
    return [(int(c["run"]), c["factor"], float(events[c["deviation"]]["values"][c["value_from"]]),
             c["deviation"])
            for c in CFG.raw()["campaign"].get("setting_corrections", [])
            if c["step"] == key and c["kind"] == kind]


def rsm_data(key, runs="all", corrected=True):
    """The response-surface runs of a step: the planned design (block 1) and, with ``runs="all"``,
    the INV-002 augmentation (block 2) where the step has one. With ``corrected`` a run recorded off
    its design setting carries the recorded setting (``setting_corrections``)."""
    import os
    from _pcpkg import DATA
    df = csv(f"doe_{key}_rsm.csv").copy()
    df[ad.BLOCK] = 1
    if corrected:
        for run, factor, value, _ in setting_corrections(key, "rsm"):
            i = df.index[df["run"] == run]
            df.loc[i, factor] = value
            df.loc[i, "coded_" + factor] = float(_to_coded(value, key, factor))
    path = os.path.join(DATA, f"doe_{key}_aug.csv")
    if runs == "all" and os.path.exists(path):
        aug = csv(f"doe_{key}_aug.csv").copy()
        df = pd.concat([df, aug[[c for c in aug.columns if c in df.columns]]], ignore_index=True)
    return df


def has_augmentation(key):
    import os
    from _pcpkg import DATA
    return os.path.exists(os.path.join(DATA, f"doe_{key}_aug.csv"))


def _rsm_fit(key, resp, runs, form, corrected=True):
    """The response-surface fit of an output. By default the model INV-002 corrective action CA3
    selects (``adequacy.select_model``: Box-Cox scale, AICc over the hierarchical submodels of the full
    quadratic, block kept), with ``status`` "selected" when it meets PCMP-001 §7.2 and "none" when it
    does not (the output is then judged on its measured results). ``form="full"`` gives the full
    quadratic on the raw scale with no gate (``status`` "full"): Version 1.0's analysis, and the
    planned model the reports compare against. ``full`` always carries the full model's statistics,
    and ``full_scale`` the full quadratic on the scale of the chosen model (on the log scale for a
    log-scale output, so that a term the selection dropped can be tested where it was dropped)."""
    factors = rsm_factors(key)
    df = rsm_data(key, runs, corrected)
    d = df[df[resp].notna()].reset_index(drop=True)
    full = ad.adequacy(d, resp, factors, ad.full_terms(factors), TH)
    if form == "full":
        chosen, frm, transform, ycol, boxcox, status = full, "full", None, resp, None, "full"
        full_scale = full
    else:
        sel = ad.select_model(d, resp, factors, TH)
        chosen, frm = sel, "selected"
        transform = "log" if sel["scale"] == "log" else None
        ycol, boxcox, d = sel["ycol"], sel["boxcox"], sel["data"]
        status = "selected" if sel["adequate"] else "none"
        full_scale = (ad.adequacy(d, ycol, factors, ad.full_terms(factors), TH)
                      if transform == "log" else full)
    m = chosen["model"]
    return dict(model=m, df=d, factors=factors, names=list(chosen["terms"]), quad=True,
                transform=transform, ycol=ycol, boxcox=boxcox, aicc=chosen.get("aicc"),
                aicc_full=chosen.get("aicc_full"),
                block=bool(chosen["block"]), n=chosen["n"], R2=chosen["R2"], adjR2=chosen["adjR2"],
                predR2=chosen["predR2"], gap=chosen["gap"], F=chosen["F"], p=chosen["p"],
                rmse=chosen["rmse"], ss_pe=chosen["ss_pe"], df_pe=chosen["df_pe"],
                ss_lof=chosen["ss_lof"], df_lof=chosen["df_lof"], F_lof=chosen["F_lof"],
                p_lof=chosen["p_lof"], sse=chosen["sse"], form=frm, status=status,
                adequate=bool(chosen["adequate"]), full=full, full_scale=full_scale, runs=runs,
                exact=bool(chosen.get("exact", False)))


def fit(key, kind, resp, superseded=False, runs=None, form=None):
    """Fit the coded model (2FI for screening; for RSM see below) + diagnostics.

    A response-surface fit (``kind="rsm"``) uses every run of the step, planned and INV-002
    augmentation (with a block term), and the model PCMP-001 §7.2 allows (``_rsm_fit``), unless
    ``runs="planned"`` or ``form="full"`` asks otherwise. Inside ``rev1_criteria_in_force`` or
    ``planned_full_models`` it is the full quadratic on the planned runs.

    ``superseded=True`` fits the invalidated first-execution dataset
    (``doe_<key>_<kind>_superseded.csv``) instead of the reported one — used to show that
    an anomalous interaction present in the superseded data is absent from the requalified
    data (Deviation root-cause confirmation)."""
    if kind == "rsm" and not superseded:
        runs = runs or _MODELS["runs"]
        form = form or _MODELS["form"]
        corrected = _MODELS["corrected"]
        if _CRITERIA["rev"] == "1.0":
            runs, form, corrected = "planned", "full", False
        ck = (key, resp, runs, form, corrected)
        if ck not in _FIT_CACHE:
            _FIT_CACHE[ck] = _rsm_fit(key, resp, runs, form, corrected)
        return _FIT_CACHE[ck]
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


def rsm_coeff_df(key, resp, runs=None, form=None):
    """Response-surface coefficient table in model order (Intercept, main, 2FI, quad, block):
    the model the response ends up with by default; ``form="full"`` / ``runs="planned"`` give
    the full quadratic model or the planned runs only."""
    r = fit(key, "rsm", resp, runs=runs, form=form)
    m, lmap = r["model"], factor_letters(key)
    order = ["const"] + r["names"] + ([ad.BLOCK] if r["block"] else [])
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
    Z = _predict_points(r, pd.DataFrame(data)).reshape(XX.shape)
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
        zc = float(np.nanmean(Z))
        if float(np.nanmax(Z) - np.nanmin(Z)) <= 1e-9 * max(1.0, abs(zc)):
            # flat over these two factors (a model with no term in them): one level at its value,
            # not twelve levels of rounding noise with an offset on the colour bar
            d = max(1e-6, 0.005 * abs(zc))
            cs = ax.contourf(xn, yn, np.full_like(Z, zc), levels=[zc - d, zc + d], cmap="viridis")
            cb = fig.colorbar(cs, ax=ax, shrink=0.85, ticks=[zc])
            cb.ax.set_yticklabels([f"{zc:.3g}"])
        else:
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
    actual = r["df"][r.get("ycol", resp)].values          # on the scale of the model
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
PAR_GRID = 81            # parameter grid points across the characterization range
PAR_GRID_SETPOINT = 201  # grid points of the set-point (design-centre) PAR analysis
#: the NOR spans this many standard deviations of a parameter's draw in the NOR-propagated
#: analysis: SD = NOR width / NOR_SD_DIVISOR (3 SD either side of the set-point), clipped to the range
NOR_SD_DIVISOR = 6.0
#: the coverage of the central interval of the NOR-propagated analysis, and of a prediction interval
PI_LEVEL = 0.95
#: the one-sided confidence level of the bound in the verification of platform worst cases (iac.py)
from amab_process.iac import BOUND_CONFIDENCE as VERIFICATION_BOUND  # noqa: E402

# response key -> CQA-register key (for responses not named as a CQA key directly)
RESP_TO_CQA = {
    "hcp_out_ng_mg": "hcp", "pool_hcp_ng_mg": "hcp", "xmulv_lrf": "lrv_xmulv",
    "mvm_lrf": "lrv_mvm", "leached_protein_a_ppm": "leached_protein_a",
    "aggregate_out_pct": "aggregates_hmw", "residual_dna": "residual_dna",
    "lmw_cesds_pct": "fragments_lmw",
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
# Intermediate acceptance criteria (Rev 2.0) — the limit a step's OWN output must meet.
#
# `acceptance_for` above returns the DRUG-SUBSTANCE criterion and keeps doing so. A step is
# judged against its intermediate acceptance criterion (IAC), derived a priori in
# amab_process/iac.py from the drug-substance criterion and the platform worst case of every
# downstream step, then tightened wherever this campaign's verification showed a downstream step doing worse
# within its NOR, and widened only where the one-sided 95 % prediction bound of a single batch at the
# A-Mab worst case beats the platform value on an adequate model (config `iac.allow_widening`, owner's
# decisions 2026-10-08 and 2026-10-09). The table is outputs/data/iac.csv; nothing here
# computes a limit, it only reads one. The Rev 1.0 criteria, fitted after the data were seen
# (INV-001), are outputs/data/criteria_rev1.csv and are read only to tabulate the change.
# --------------------------------------------------------------------------------------
def _iac_row(key, resp):
    t = csv(_CRITERIA.get("file", "iac.csv"))
    r = t[(t["step_key"] == key) & (t["response"] == resp)]
    return None if r.empty else r.iloc[0]


_CRITERIA = {"rev": "2.0"}


class criteria_from:
    """Context manager: inside it the Version 2.0 criteria are read from another criteria file of
    the same form as ``iac.csv`` (``iac_full.csv``, ``iac_batch.csv``). The models stay the selected
    ones. For showing what a conclusion would be under criteria derived another way."""
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self._old = _CRITERIA.get("file")
        _CRITERIA["file"] = self.name
        return self

    def __exit__(self, *a):
        if self._old is None:
            _CRITERIA.pop("file", None)
        else:
            _CRITERIA["file"] = self._old
        return False


class criteria_without_ca3:
    """Context manager: inside it the Version 2.0 criteria are the ones the verification on the full
    quadratic models gives (``iac_full.csv``), the criteria as they would have been without INV-002
    corrective action CA3. The models stay the selected ones. INV-002 uses it to show whether any
    conclusion of a report depends on the criteria that CA3 moved."""
    def __enter__(self):
        self._old = _CRITERIA.get("file")
        _CRITERIA["file"] = "iac_full.csv"
        return self

    def __exit__(self, *a):
        if self._old is None:
            _CRITERIA.pop("file", None)
        else:
            _CRITERIA["file"] = self._old
        return False


def ca3_criteria_sensitivity():
    """For every output with a criterion and a response-surface model: the judgement across the NOR
    in force with the criteria in force and with the criteria as they would have been without CA3,
    and whether the conclusion differs; every NOR-propagated PAR of the output; and, for an output
    with a scale-down offset, whether the scale-down model is qualified under each (the conclusion
    with the offset at either end of its interval), which can depend on the criterion even where the
    conclusion at the estimate does not."""
    rows = []
    m = csv("model_adequacy.csv")
    for _, r in m.iterrows():
        key, resp = r["step_key"], r["response"]
        acc_in = ipc_limit(key, resp)
        met_in = nor_met(key, resp)
        pars_in = {f: par_nor_propagated(key, resp, f)["par_nat"] for f in rsm_factors(key)} \
            if fit(key, "rsm", resp)["status"] != "none" and acc_in is not None else {}
        with criteria_without_ca3():
            acc_wo = ipc_limit(key, resp)
            met_wo = nor_met(key, resp)
            pars_wo = {f: par_nor_propagated(key, resp, f)["par_nat"] for f in rsm_factors(key)} \
                if fit(key, "rsm", resp)["status"] != "none" and acc_wo is not None else {}
        same_par = all((pars_in.get(f) is None and pars_wo.get(f) is None) or
                       (pars_in.get(f) is not None and pars_wo.get(f) is not None and
                        np.allclose(pars_in[f], pars_wo[f], rtol=1e-6, atol=1e-9)) for f in set(pars_in) | set(pars_wo))
        # the qualification of the scale-down model, which judges the conclusion with the offset at
        # either end of its interval (an output with an offset at its step only)
        q_in = offset_qualification(key, resp) if sdm_offset(key, resp) is not None else None
        with criteria_without_ca3():
            q_wo = offset_qualification(key, resp) if sdm_offset(key, resp) is not None else None
        rows.append({"step_key": key, "response": resp,
                     "qualified_in_force": None if not q_in or not q_in.get("judged") else bool(q_in["qualified"]),
                     "qualified_without_ca3": None if not q_wo or not q_wo.get("judged") else bool(q_wo["qualified"]),
                     "criterion_in_force": None if acc_in is None else acc_in[1] if acc_in[2] == "upper" else acc_in[0],
                     "criterion_without_ca3": None if acc_wo is None else acc_wo[1] if acc_wo[2] == "upper" else acc_wo[0],
                     "criterion_moved": (acc_in is None) != (acc_wo is None) or (acc_in is not None and not np.allclose(
                         [x if np.isfinite(x) else 0.0 for x in acc_in[:2]],
                         [x if np.isfinite(x) else 0.0 for x in acc_wo[:2]], rtol=1e-6, atol=1e-9)),
                     "met_in_force": met_in, "met_without_ca3": met_wo,
                     "conclusion_differs": met_in != met_wo, "pars_same": bool(same_par)})
    out = pd.DataFrame(rows)
    out["qualification_differs"] = [a is not None and b is not None and a != b
                                    for a, b in zip(out["qualified_in_force"], out["qualified_without_ca3"])]
    return out


def ipc_limit(key, resp):
    """(lo, hi, spec_type): the step's intermediate acceptance criterion, or None if the step has
    none for this response. Kept under its Rev 1.0 name so callers did not have to change.
    Inside :func:`rev1_criteria_in_force` it returns the Version 1.0 criterion instead."""
    if _CRITERIA["rev"] == "1.0":
        t = csv("criteria_rev1.csv")
        r = t[(t["step_key"] == key) & (t["response"] == resp)]
        if r.empty:
            return None
        r = r.iloc[0]
        return float(r["low"]), float(r["high"]), ("lower" if r["cqa"].startswith("lrv") else "upper")
    r = _iac_row(key, resp)
    if r is None:
        return None
    return float(r["iac_low"]), float(r["iac_high"]), str(r["spec_type"])


iac_limit = ipc_limit


def effective_acceptance(key, resp):
    """The criterion the PAR analysis judges a step against: its IAC where one is defined,
    otherwise the drug-substance criterion."""
    acc = ipc_limit(key, resp) or acceptance_for(key, resp)
    if acc and _CRITERIA["rev"] == "1.0" and resp == "acidic_variants":
        # Version 1.0 assessed acidic variants against the ceiling only (INV-001 finding 4)
        acc = (acc[0], acc[1], "upper")
    if _CRITERIA["rev"] == "1.0" and resp == "lmw_cesds_pct":
        return None                       # Version 1.0 did not assess fragments
    return acc


# --------------------------------------------------------------------------------------
# Scale-down offsets (owner's decision 2026-10-08). A scale-down model may differ in mean from
# manufacturing scale, provided the offset is known precisely enough. The offset of an output is
# the mean of the scale-down set-point runs minus the mean of the manufacturing-scale batches,
# with its two-sided 90 % confidence interval (pooled-variance Student t), from
# sdm_qualification.csv. Every Version 2.0 judgement against a criterion translates the
# scale-down prediction to manufacturing scale by subtracting the offset. The model is qualified
# for an output when the conclusion against its criterion over the NOR is the same with the
# offset at either end of its interval (:func:`offset_qualification`). Outputs with no SDM data
# (fragments, viral clearance) have no offset and are judged as predicted.
# --------------------------------------------------------------------------------------
_OFFSET = {"end": "point"}                 # "point", "lo", "hi" or "none"


def sdm_offset(key, resp, studies=None):
    """dict(n_sd, n_m, mean_sd, mean_m, offset, lo, hi, half, df) for one output of one step, or
    None when the qualification has no data for it. ``studies`` restricts the scale-down runs
    (e.g. ``["S-PA-SDM"]``, the planned runs alone); by default every scale-down study counts."""
    from scipy import stats as _st
    d = csv("sdm_qualification.csv")
    d = d[d["step"] == key]
    if resp not in d.columns:
        return None
    a = d[d["scale"] == "scale-down"]
    if studies is not None:
        a = a[a["study"].isin(studies)]
    a = a[resp].dropna().to_numpy(float)
    b = d.loc[d["scale"] == "manufacturing", resp].dropna().to_numpy(float)
    if len(a) < 2 or len(b) < 2:
        return None
    # on the scale the output is modelled on: for a log-scale model the difference of the mean logs,
    # reported as a ratio of geometric means (PCR-005 Version 2.0, discrepancy from the plan)
    try:
        log = fit(key, "rsm", resp).get("transform") == "log"
    except Exception:
        log = False
    if log:
        a, b = np.log(a), np.log(b)
    dfp = len(a) + len(b) - 2
    sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / dfp)
    ci = float(CFG.raw()["analytics"]["sdm"].get("offset_ci", 0.90))
    half = float(_st.t.ppf(0.5 + ci / 2, dfp) * sp * np.sqrt(1 / len(a) + 1 / len(b)))
    off = float(a.mean() - b.mean())
    if log:
        return dict(n_sd=len(a), n_m=len(b), mean_sd=float(np.exp(a.mean())), mean_m=float(np.exp(b.mean())),
                    offset=float(np.exp(off)), lo=float(np.exp(off - half)), hi=float(np.exp(off + half)),
                    half=half, df=dfp, ci=ci, scale="ratio", log_offset=off)
    return dict(n_sd=len(a), n_m=len(b), mean_sd=float(a.mean()), mean_m=float(b.mean()),
                offset=off, lo=off - half, hi=off + half, half=half, df=dfp, ci=ci, scale="difference")


def _offset(key, resp):
    """("difference", d) or ("ratio", r): the offset the current judgement applies, on the scale
    the output is modelled on. ("difference", 0) in Version 1.0 mode, when switched off in the
    config, or when the output has no SDM data."""
    if _CRITERIA["rev"] == "1.0" or _OFFSET["end"] == "none":
        return "difference", 0.0
    if not CFG.raw()["analytics"]["sdm"].get("apply_offset", False):
        return "difference", 0.0
    o = sdm_offset(key, resp, _OFFSET.get("studies"))
    if o is None:
        return "difference", 0.0
    return o["scale"], {"point": o["offset"], "lo": o["lo"], "hi": o["hi"]}[_OFFSET["end"]]


def _offset_value(key, resp):
    """The additive offset the current judgement applies (0 for none). For an output modelled on
    the log scale the offset is a ratio: use ``to_mfg``."""
    kind, v = _offset(key, resp)
    return v if kind == "difference" else 0.0


def to_mfg(key, resp, y):
    """A scale-down value at manufacturing scale: minus the offset, or divided by it when the output
    is modelled on the log scale and its offset is a ratio."""
    kind, v = _offset(key, resp)
    y = np.asarray(y, dtype=float)
    return y / v if kind == "ratio" else y - v


def _judging(key, resp):
    """(lo, hi, stype) as the scale-down prediction is judged: the criterion moved by the offset.
    A scale-down value y meets the criterion when its manufacturing-scale value does, that is when
    lo + d <= y <= hi + d (an offset d), or lo·r <= y <= hi·r (a ratio r)."""
    acc = effective_acceptance(key, resp)
    if acc is None:
        return None
    kind, v = _offset(key, resp)
    if kind == "ratio":
        return acc[0] * v, acc[1] * v, acc[2]
    return acc[0] + v, acc[1] + v, acc[2]


class offset_at:
    """Context manager: judge with the offset at one end of its interval ("lo", "hi"), at its
    point estimate ("point"), or without it ("none"); ``studies`` restricts the runs it is
    estimated from."""
    def __init__(self, end, studies=None):
        self.end, self.studies = end, studies

    def __enter__(self):
        self._old = dict(_OFFSET)
        _OFFSET["end"] = self.end
        _OFFSET["studies"] = self.studies
        return self

    def __exit__(self, *a):
        _OFFSET.clear()
        _OFFSET.update(self._old)
        return False


def measured_values(key, resp):
    """Every measured result of the response in the designs of the step (screening, response
    surface and any INV-002 augmentation), at the scale of the scale-down model."""
    vals = []
    frames = [csv(f"doe_{key}_{k}.csv") for k in ("screening", "rsm")]
    if has_augmentation(key):
        frames.append(csv(f"doe_{key}_aug.csv"))
    for df in frames:
        if resp in df.columns:
            vals.append(df[resp].dropna().to_numpy(float))
    return np.concatenate(vals) if vals else np.array([])


def measured_met(key, resp):
    """Does every measured result of the designs meet the criterion at manufacturing scale? The
    judgement of an output with no adequate model (PCMP-001 §7.2: such a model sets no range).
    The designs span the range studied, so this also covers the NOR. None when the output has no
    criterion or no result."""
    acc = _judging(key, resp)
    v = measured_values(key, resp)
    if acc is None or not len(v):
        return None
    lo, hi, stype = acc
    return bool(np.all(_in_spec(v, lo, hi, stype)))


def model_status(key, resp):
    """"selected" (the selected model meets PCMP-001 §7.2) or "none" (no adequate model) for a
    response-surface output; "full" inside ``planned_full_models`` and Version 1.0 mode."""
    try:
        return fit(key, "rsm", resp)["status"]
    except Exception:
        return None


def nor_met(key, resp):
    """Does the output meet its criterion across the NOR, at manufacturing scale? Judged at every
    combination of NOR low, set-point and NOR high of the response-surface factors: for a quality
    attribute the 95 % prediction interval of a single run, for viral clearance the mean. An
    output with no adequate model is judged on its measured results (``measured_met``).
    None when the output has no criterion or no response-surface model."""
    acc = _judging(key, resp)
    if acc is None:
        return None
    try:
        r = fit(key, "rsm", resp)
    except Exception:
        return None
    if r["status"] == "none":
        return measured_met(key, resp)
    uo = CFG.unit_op(key)
    grid = list(itertools.product(*[[uo.param(f).nor[0], uo.param(f).setpoint, uo.param(f).nor[1]]
                                    for f in r["factors"]]))
    nat = {f: [g[i] for g in grid] for i, f in enumerate(r["factors"])}
    lo, hi, stype = acc
    if decision_statistic(resp) == "batch":
        _, plo, phi = prediction_interval(key, resp, nat)
        return bool(np.all(_in_spec(plo, lo, hi, stype)) and np.all(_in_spec(phi, lo, hi, stype)))
    return bool(np.all(_in_spec(np.asarray(predict(key, resp, natural=nat)), lo, hi, stype)))


def nor_prediction_limit(key, resp, side="upper"):
    """The most extreme single-run value the response-surface model predicts within the NOR, at
    manufacturing scale: the upper (or lower) 95 % prediction limit at the worst combination of NOR
    low, set-point and NOR high of the factors, minus the scale-down offset. This is the highest
    (lowest) level a pool is expected to carry in routine manufacture, which a hold-time criterion
    adds the hold increase to (PCP-005 Version 2.0). None when the step has no model for it."""
    try:
        r = fit(key, "rsm", resp)
    except Exception:
        return None
    if r["status"] == "none":
        return None                     # no adequate model sets an expected level (INV-002)
    uo = CFG.unit_op(key)
    grid = list(itertools.product(*[[uo.param(f).nor[0], uo.param(f).setpoint, uo.param(f).nor[1]]
                                    for f in r["factors"]]))
    nat = {f: [g[i] for g in grid] for i, f in enumerate(r["factors"])}
    _, lo, hi = prediction_interval(key, resp, nat)
    return float(to_mfg(key, resp, np.max(hi))) if side == "upper" else float(to_mfg(key, resp, np.min(lo)))


def offset_qualification(key, resp, studies=None):
    """The qualification of the scale-down model for one output (owner's rule, 2026-10-08).

    Returns dict(offset..., met_point, met_lo, met_hi, qualified, judged). ``judged`` is False for
    an output with no criterion or no model at the step: its offset is recorded and nothing
    depends on it. ``qualified`` is True when the conclusion of :func:`nor_met` is the same with
    the offset at its point estimate and at either end of its confidence interval."""
    o = sdm_offset(key, resp, studies)
    if o is None:
        return None
    out = dict(o)
    with offset_at("point", studies):
        out["met_point"] = nor_met(key, resp)
    if out["met_point"] is None:
        out.update(met_lo=None, met_hi=None, judged=False, qualified=True)
        return out
    with offset_at("lo", studies):
        out["met_lo"] = nor_met(key, resp)
    with offset_at("hi", studies):
        out["met_hi"] = nor_met(key, resp)
    out["judged"] = True
    out["qualified"] = out["met_lo"] == out["met_point"] == out["met_hi"]
    return out


class rev1_criteria_in_force:
    """Context manager: inside it, every PAR and acceptance helper judges against the Version 1.0
    criteria (criteria_rev1.csv), at the NOR and set-points as characterized, as Version 1.0 did.
    Used to state, from the data, which Version 1.0 conclusions moved at Version 2.0. Never used to
    produce a Version 2.0 result."""
    def __enter__(self):
        _CRITERIA["rev"] = "1.0"
        self._cn = characterized_nor()
        self._cn.__enter__()
        return self

    def __exit__(self, *a):
        _CRITERIA["rev"] = "2.0"
        self._cn.__exit__(*a)
        return False


def par_table_rev1(key):
    """``par_table`` as Version 1.0 computed it: the same models, judged against the Version 1.0
    criteria. For the "Changes in this revision" comparison only."""
    with rev1_criteria_in_force():
        return par_table(key)


def acceptance_basis(key, resp):
    """How the criterion `effective_acceptance` returned was set, as iac.csv records it:
    'drug substance', 'back-calculated', 'back-calculated, tightened on verification' or
    'platform claim'. 'drug substance' also when no IAC row exists."""
    r = _iac_row(key, resp)
    return "drug substance" if r is None else str(r["basis"])


def iac_table(key=None):
    """The IAC table (all steps, or one), as amab_process.iac wrote it."""
    t = csv("iac.csv")
    return t if key is None else t[t["step_key"] == key].reset_index(drop=True)


def rev1_criteria(key=None):
    """The Rev 1.0 in-process criteria, with the rule and margin each used (data for INV-001)."""
    t = csv("criteria_rev1.csv")
    return t if key is None else t[t["step_key"] == key].reset_index(drop=True)


def iac_verification(key=None):
    """Platform worst case assumed vs observed at the edges and predicted within the NOR."""
    t = csv("iac_verification.csv")
    return t if key is None else t[t["step_key"] == key].reset_index(drop=True)


def p_oos():
    """Integrated-model probability of an out-of-specification drug substance, per attribute."""
    return csv("p_oos.csv")


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

    Uses `effective_acceptance(key, resp)`: the step's intermediate acceptance criterion where one is
    configured, otherwise the drug-substance criterion (and for viral-clearance responses
    the back-calculated STEP floor rather than the cumulative requirement). Returns None
    when the response maps to no acceptance criterion (e.g. step yield)."""
    acc = _judging(key, resp)
    if acc is None:
        return None
    lo, hi, stype = acc
    return _in_spec(np.asarray(values, dtype=float), lo, hi, stype)


def _to_coded(natural, key, f):
    p = CFG.unit_op(key).param(f)
    lo, hi = p.prange
    return (np.asarray(natural, dtype=float) - (lo + hi) / 2) / ((hi - lo) / 2)


def _back(r, v):
    """From the scale of the model to the scale of the response: exp for a log-scale model. A
    back-transformed mean is the median of the response (its mean is exp(σ²/2) higher); a
    back-transformed prediction limit keeps its coverage, since exp is increasing."""
    return np.exp(v) if r.get("transform") == "log" else v


def _predict_points(r, coded):
    """Predict the fitted model at coded factor settings (DataFrame of factor columns), on the
    scale of the response (a log-scale model gives the median). A block term is set to 0, the
    average of the two blocks."""
    return _back(r, _design_matrix(r, coded) @ np.asarray(r["model"].params))


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


def par_at_design_centre(key, resp, factor, n_grid=PAR_GRID_SETPOINT):
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

    The criterion is `effective_acceptance`: the step's intermediate acceptance criterion where one is
    configured, otherwise the drug-substance criterion.
    """
    acc = effective_acceptance(key, resp)
    if acc is None:
        return None
    lo, hi, stype = _judging(key, resp)
    r = fit(key, "rsm", resp)
    xs = np.linspace(-1, 1, n_grid)
    coded = pd.DataFrame({f: (xs if f == factor else np.zeros(n_grid)) for f in r["factors"]})
    yhat = _predict_points(r, coded)
    par_c = _contiguous_range(xs, _in_spec(yhat, lo, hi, stype))
    return {"factor": factor, "resp": resp, "acc": acc, "xs_nat": _natural(xs, key, factor),
            "y": yhat, "par_coded": par_c,
            "par_nat": None if par_c is None else (_natural(par_c[0], key, factor),
                                                   _natural(par_c[1], key, factor))}


def decision_statistic(resp):
    """What the NOR-propagated PAR judges, per attribute class (PCMP-001 Version 2.0).

    'batch'  the 95 % predictive interval of a single batch: NOR variation of the other
             factors plus the model residual. For quality attributes, where a single batch is
             what must meet the criterion.
    'worst_case'  (viral clearance, owner's decision 2026-10-08) the mean predicted LRF with the
             other factors at the least favourable combination of their NOR low, set-point and
             NOR high, as viral clearance is validated at worst-case conditions. Until
             2026-10-08 this was 'mean': the 2.5th percentile of the mean over NOR draws.
    (former 'mean' text follows for the record) the 2.5th percentile of the MEAN response over
             operating points drawn within the NOR, without the residual. For viral clearance, whose platform claim is stated as an
             average log reduction factor (A-Mab p.131) and whose residual is mostly the
             variability of the infectivity assay, not of the process. (ICH Q5A(R2) asks for
             duplicate spiking runs but does not prescribe how they are combined; do not cite it
             for the mean.)
             The per-batch result is still computed (``batch=True``) and reported for information.
    """
    return "worst_case" if resp in VIRAL_COL else "batch"


def _mc_predictive(r, key, factor, x_coded, others, rng, n_mc, residual=True):
    """Monte-Carlo draws of the response at target `factor`=x_coded with the `others` varied
    within their NOR (~N(set-point, NOR/6), clipped), plus the model residual unless
    ``residual`` is False (see :func:`decision_statistic`). Factored out so a Bayesian
    posterior-predictive backend can replace it later."""
    coded = pd.DataFrame({factor: np.full(n_mc, x_coded)})
    for g in others:
        p = CFG.unit_op(key).param(g)
        w = max((p.nor[1] - p.nor[0]) / NOR_SD_DIVISOR, 1e-9)
        nat = np.clip(rng.normal(p.setpoint, w, n_mc), p.prange[0], p.prange[1])
        coded[g] = _to_coded(nat, key, g)
    noise = rng.normal(0.0, r["rmse"], n_mc)      # drawn either way: the stream stays aligned
    if residual and _CRITERIA["rev"] != "1.0":
        # A single batch's 95 % predictive interval needs the uncertainty of the fitted
        # coefficients as well as the residual: each draw takes its own coefficient vector from
        # their estimated sampling distribution. Version 1.0 used the point coefficients plus the
        # residual only, which understates the interval (found in the PCR-005 Version 2.0 review);
        # rev1_criteria_in_force keeps that behaviour so Version 1.0 still reproduces.
        X = _design_matrix(r, coded[r["factors"]])
        m = r["model"]
        b = rng.multivariate_normal(np.asarray(m.params), np.asarray(m.cov_params()), n_mc)
        return _back(r, np.einsum("ij,ij->i", X, b) + noise)
    lin = _design_matrix(r, coded[r["factors"]]) @ np.asarray(r["model"].params)
    return _back(r, lin + (noise if residual else 0.0))


def _design_matrix(r, coded):
    """The model matrix of a fitted RSM at coded settings, columns in the model's own order; a
    block term at 0, the average of the two blocks."""
    X = pd.DataFrame({"const": np.ones(len(coded))}, index=coded.index)
    for f in r["factors"]:
        X[f] = np.asarray(coded[f], dtype=float)
    for a, b in itertools.combinations(r["factors"], 2):
        X[f"{a}:{b}"] = X[a].values * X[b].values
    if r["quad"]:
        for f in r["factors"]:
            X[f"{f}^2"] = X[f].values ** 2
    cols = ["const"] + r["names"]
    if r.get("block"):
        X[ad.BLOCK] = 0.0
        cols = cols + [ad.BLOCK]
    return X[cols].to_numpy()


def prediction_interval(key, resp, natural, alpha=0.05):
    """(mean, lower, upper) of the exact 95 % prediction interval for a single new run at the
    given settings, from the fitted response-surface model (t quantile, coefficient and residual
    uncertainty). ``natural`` maps factor -> sequence; factors omitted sit at the design centre."""
    r = fit(key, "rsm", resp)
    n = max(len(np.atleast_1d(v)) for v in natural.values())
    coded = pd.DataFrame({f: np.zeros(n) for f in r["factors"]})
    for f, v in natural.items():
        coded[f] = np.atleast_1d(_to_coded(np.atleast_1d(v), key, f)) * np.ones(n)
    X = _design_matrix(r, coded)
    sf = r["model"].get_prediction(X).summary_frame(alpha=alpha)
    # on a log-scale model the interval is computed on the log scale and back-transformed: its
    # coverage is exact, it is asymmetric in the units of the response, and the centre is the median
    return (_back(r, sf["mean"].to_numpy()), _back(r, sf["obs_ci_lower"].to_numpy()),
            _back(r, sf["obs_ci_upper"].to_numpy()))


def par_nor_propagated(key, resp, factor, n_grid=PAR_GRID, n_mc=PAR_MC_N, batch=None):
    """PAR of `factor` for `resp` with the other factors varying within their NOR.

    ``batch`` forces the per-batch statistic (True) or the mean statistic (False); by default
    it follows :func:`decision_statistic`. Version 1.0 used the per-batch statistic for every
    response, and :func:`rev1_criteria_in_force` restores that.

    The PAR is the range of `factor` over which the 95% predictive interval of the CQA
    (from the NOR Monte-Carlo of the fitted model) stays within acceptance — a robustness
    criterion, so it is narrower than the at-set-point PAR. The criterion is
    `effective_acceptance`: the step's intermediate acceptance criterion (Version 2.0) where one is defined."""
    acc = effective_acceptance(key, resp)
    if acc is None:
        return None
    lo, hi, stype = _judging(key, resp)
    r = fit(key, "rsm", resp)
    others = [g for g in r["factors"] if g != factor]
    rng = np.random.default_rng(PAR_SEED)
    xs = np.linspace(-1, 1, n_grid)
    med = np.empty(n_grid); p_lo = np.empty(n_grid); p_hi = np.empty(n_grid); p_in = np.empty(n_grid)
    if batch is None:
        batch = decision_statistic(resp) == "batch" or _CRITERIA["rev"] == "1.0"
    if not batch and decision_statistic(resp) == "worst_case":
        # worst case: at each scanned value, the other factors at the combination of their NOR
        # low / set-point / NOR high that is least favourable to the criterion
        grid = list(itertools.product(*[[_to_coded(CFG.unit_op(key).param(g).nor[0], key, g),
                                         _to_coded(CFG.unit_op(key).param(g).setpoint, key, g),
                                         _to_coded(CFG.unit_op(key).param(g).nor[1], key, g)]
                                        for g in others])) or [()]
        for i, x in enumerate(xs):
            pts = pd.DataFrame([{factor: x, **dict(zip(others, c))} for c in grid])
            y = _predict_points(r, pts[r["factors"]])
            worst = float(np.min(y)) if stype == "lower" else float(np.max(y))
            med[i] = float(np.median(y)); p_lo[i] = worst if stype == "lower" else float(np.min(y))
            p_hi[i] = worst if stype == "upper" else float(np.max(y))
            p_in[i] = float(_in_spec(y, lo, hi, stype).mean())
        mask = (p_lo >= lo) if stype == "lower" else (p_hi <= hi) if stype == "upper" else ((p_lo >= lo) & (p_hi <= hi))
        sp = float(_to_coded(CFG.unit_op(key).param(factor).setpoint, key, factor))
        par_c = _contiguous_range(xs, mask, center=sp)
        return {"factor": factor, "resp": resp, "acc": acc, "xs_nat": _natural(xs, key, factor),
                "med": med, "p_lo": p_lo, "p_hi": p_hi, "p_in": p_in, "par_coded": par_c,
                "par_nat": None if par_c is None else (_natural(par_c[0], key, factor),
                                                       _natural(par_c[1], key, factor))}
    for i, x in enumerate(xs):
        y = _mc_predictive(r, key, factor, x, others, rng, n_mc, residual=batch)
        med[i] = np.median(y); p_lo[i] = np.percentile(y, 2.5); p_hi[i] = np.percentile(y, 97.5)
        p_in[i] = _in_spec(y, lo, hi, stype).mean()
    if stype == "upper":
        mask = p_hi <= hi
    elif stype == "lower":
        mask = p_lo >= lo
    else:
        mask = (p_lo >= lo) & (p_hi <= hi)
    # Anchor the range at the SET-POINT of the scanned factor: the other factors are drawn around
    # their set-points, and "none (set-point breaches)" must mean exactly that. Until 2026-10-08
    # this anchored at coded 0, the design centre, which differs from the set-point for six
    # factors (DISCREPANCIES.md D-001's table). No Version 1.0 result was affected, because no
    # Version 1.0 criterion failed at a design centre while passing at the set-point; the first
    # Version 2.0 run would have reported low-pH inactivation pH as having no NOR-propagated range.
    # par_at_design_centre is deliberately NOT changed (D-001).
    sp = float(_to_coded(CFG.unit_op(key).param(factor).setpoint, key, factor))
    par_c = _contiguous_range(xs, mask, center=sp)
    return {"factor": factor, "resp": resp, "acc": acc, "xs_nat": _natural(xs, key, factor),
            "med": med, "p_lo": p_lo, "p_hi": p_hi, "p_in": p_in, "par_coded": par_c,
            "par_nat": None if par_c is None else (_natural(par_c[0], key, factor),
                                                   _natural(par_c[1], key, factor))}


def _pi_points(r, coded, alpha=None):
    """(centre, lower, upper) of the prediction interval of a single new run at coded factor
    settings (DataFrame of factor columns), on the scale of the response: a log-scale model gives
    the median and the back-transformed exact limits. The interval is two-sided at ``PI_LEVEL``."""
    alpha = (1.0 - PI_LEVEL) if alpha is None else alpha
    sf = r["model"].get_prediction(_design_matrix(r, coded)).summary_frame(alpha=alpha)
    return (_back(r, sf["mean"].to_numpy()), _back(r, sf["obs_ci_lower"].to_numpy()),
            _back(r, sf["obs_ci_upper"].to_numpy()))


def design_space_grid(key, n=11, basis="batch"):
    """How much of the characterized region actually meets every criterion this step governs.

    Once a step has intermediate acceptance criteria, the design space stops being "the whole characterized
    region" as a matter of course: a parameter whose PAR is narrower than its characterization
    range is, by definition, a parameter some of whose characterized settings are unacceptable.
    This evaluates the fitted response-surface models on an evenly spaced grid over the coded
    cube and reports what survives, so a report can state the size of its region from the data
    instead of asserting it.

    A grid point is inside when every output meets its criterion there on the statistic it is
    judged on everywhere else (owner's decision 2026-10-10: the design space on the single-batch
    limit): a quality attribute when both ends of the 95 % prediction interval of a single run lie
    within its criterion, viral clearance when its mean prediction does. The criterion is moved
    by the scale-down offset (``_judging``). ``basis="mean"`` gives the former convention, every
    output on its mean (median) prediction, for comparison only.

    Returns a dict with ``fraction`` (share of grid points inside every criterion),
    ``per_response`` (share each response alone rejects), ``binding`` (the response that
    rejects most) and ``basis``.
    """
    if basis not in ("batch", "mean"):
        raise ValueError(f"basis must be 'batch' or 'mean', not {basis!r}")
    fs = rsm_factors(key)
    grids = np.meshgrid(*[np.linspace(-1, 1, n)] * len(fs), indexing="ij")
    coded = pd.DataFrame({f: g.ravel() for f, g in zip(fs, grids)})
    ok = np.ones(len(coded), dtype=bool)
    per, measured = {}, {}
    # fragments by nrCE-SDS carry a criterion at every step from Protein A on but are not among
    # ``responses(key)``; without them the region was drawn without one quality attribute
    # (PCR-005 author, 2026-10-10)
    frag = [c for c in fragment_responses(key) if c == "lmw_cesds_pct" and c not in responses(key)]
    for resp in list(responses(key)) + frag:
        acc = _judging(key, resp)
        if acc is None:
            continue
        lo, hi, stype = acc
        r = fit(key, "rsm", resp)
        if r["status"] == "none":
            # no adequate model draws a boundary (PCMP-001 §7.2); the output constrains nothing
            # when every measured result meets its criterion, and is reported in ``measured``
            measured[resp] = measured_met(key, resp)
            continue
        if basis == "batch" and decision_statistic(resp) == "batch":
            _, plo, phi = _pi_points(r, coded)
            good = _in_spec(plo, lo, hi, stype) & _in_spec(phi, lo, hi, stype)
        else:
            good = _in_spec(_predict_points(r, coded), lo, hi, stype)
        per[resp] = float(1.0 - good.mean())
        ok &= good
    binding = max(per, key=per.get) if per else None
    return {"fraction": float(ok.mean()), "per_response": per, "binding": binding,
            "n_points": int(len(coded)), "measured": measured, "basis": basis}



def residual_influence(key, resp, runs=None, form=None):
    """Criterion 4 of PCMP-001 §7.2 for the selected model of one response-surface output: "the
    residuals show no pattern against predicted values or run order, and no single run dominates
    the fit", tested as the Version 2.0 plans state it (``campaign.thresholds``):

    * a regression of the absolute residuals on the predicted values (a spread that grows with the
      level), at ``residual_alpha``; not tested for a model with no term, which predicts one value;
    * a regression of the residuals on the order of execution (a drift), at ``residual_alpha``; the
      runs of a second block continue the order of the first;
    * Cook's distance against ``cook_factor``/n (a run that dominates the fit).

    One definition for every report (2026-10-10), so that two reports cannot test the criterion
    differently. Residuals are on the scale of the model. Returns a dict: ``p_spread``,
    ``spread_slope``, ``p_order``, ``order_slope`` (per run), ``order_range`` (runs), ``cook``
    (array, in the row order of ``runs``), ``runs``, ``cook_max``, ``cook_run``, ``cook_limit``,
    ``over`` (runs above the limit), ``n``, ``trends_met``, ``cook_met``, ``met``; ``testable`` is
    False for an exact fit (no residual), whose criterion cannot be applied."""
    import statsmodels.api as sm
    th = CFG.raw()["campaign"]["thresholds"]
    alpha = float(th.get("residual_alpha", th["effect_alpha"]))
    k4 = float(th.get("cook_factor", 4.0))
    r = fit(key, "rsm", resp, runs=runs, form=form)
    if r.get("exact"):
        return {"testable": False, "met": None, "trends_met": None, "cook_met": None, "n": int(r["n"])}
    m, d = r["model"], r["df"]
    n = len(d)
    cd = np.asarray(m.get_influence().cooks_distance[0], dtype=float)
    if r["names"]:
        g = sm.OLS(np.abs(np.asarray(m.resid, float)), sm.add_constant(np.asarray(m.fittedvalues, float))).fit()
        p_spread, spread = float(g.pvalues[1]), float(g.params[1])
    else:
        p_spread, spread = float("nan"), float("nan")
    order = d["run_order"].to_numpy(dtype=float).copy()
    if ad.BLOCK in d.columns and (d[ad.BLOCK] > 1).any():
        first = (d[ad.BLOCK] == 1).to_numpy()
        order[~first] += order[first].max()
    go = sm.OLS(np.asarray(m.resid, float), sm.add_constant(order)).fit()
    p_order, drift = float(go.pvalues[1]), float(go.params[1])
    lim = k4 / n
    run_ids = d["run"].to_numpy()
    over = [int(x) for x in run_ids[cd > lim]]
    trends_met = bool((np.isnan(p_spread) or p_spread >= alpha) and p_order >= alpha)
    cook_met = not over
    return {"testable": True, "p_spread": p_spread, "spread_slope": spread, "p_order": p_order,
            "order_slope": drift, "order_range": float(order.max() - order.min()), "cook": cd,
            "runs": [int(x) for x in run_ids], "cook_max": float(cd.max()),
            "cook_run": int(run_ids[int(cd.argmax())]), "cook_limit": lim, "over": over, "n": n,
            "alpha": alpha, "trends_met": trends_met, "cook_met": cook_met,
            "met": bool(trends_met and cook_met)}


def oot_check(key, resp, run, value, level=None):
    """The out-of-trend rule the analytical review applies (deviation record ``oot_rule``; owner's
    decision Q7, 2026-10-10): a result is out of trend when it lies outside the two-sided
    ``level`` prediction interval of a single result from the full quadratic model of the
    response-surface design, fitted to the other runs (the run under review left out), at the
    settings of the run under review. The review was made when the design was run, so the planned
    runs at their recorded settings and the model the plan specified are used: model selection was
    adopted only in September 2026 (INV-002 CA3; the rule named it until 2026-10-10). ``level``
    defaults to the record's ``oot_level`` (0.99). Returns a dict: ``lower``, ``upper``,
    ``centre``, ``value``, ``out``, ``terms``, ``scale`` ("raw"), ``level``, ``df``."""
    import statsmodels.api as _sm
    lvl = 0.99 if level is None else float(level)
    full = rsm_data(key, "planned")
    rest = full[full["run"] != run].reset_index(drop=True)
    row = full[full["run"] == run].reset_index(drop=True)
    if row.empty:
        raise ValueError(f"run {run} is not a response-surface run of {key}")
    terms = ad.full_terms(rsm_factors(key))
    m = _sm.OLS(rest[resp].astype(float), ad.matrix(rest, terms, False)).fit()
    sf = m.get_prediction(ad.matrix(row, terms, False)).summary_frame(alpha=1.0 - lvl)
    c, lo, hi = (float(sf[k].iloc[0]) for k in ("mean", "obs_ci_lower", "obs_ci_upper"))
    v = float(value)
    return {"lower": lo, "upper": hi, "centre": c, "value": v, "out": bool(v < lo or v > hi),
            "terms": list(terms), "scale": "raw", "level": lvl, "df": float(m.df_resid)}

def governing_factor(key, resp):
    """The RSM factor with the largest absolute main effect on `resp` — its governing
    parameter, used for the representative PAR plot."""
    lmap = factor_letters(key)
    letter_to_factor = {lmap[f]: f for f in rsm_factors(key)}
    for term in screening_effects_df(key, resp)["Term"]:
        if term in letter_to_factor:
            return letter_to_factor[term]
    return rsm_factors(key)[0]


def _fmt_crit(v):
    v = float(v)
    if abs(v) >= 1000:
        return f"{v:,.0f}"
    return f"{v:.3g}"


def _par_str(par_nat, unit=""):
    if par_nat is None:
        return "none (set-point breaches)"
    lo, hi = par_nat
    u = f" {unit}" if unit else ""
    return f"{_inward(lo, up=True):g}–{_inward(hi, up=False):g}{u}"


def _inward(x, up, sig=3):
    """Round a PAR edge to ``sig`` significant figures TOWARD the inside of the range: a lower
    edge up, an upper edge down. Rounding an edge outward prints a value the analysis rejected
    (3.235 printed as 3.23, where the predictive bound already exceeds the criterion; found by the
    PCR-005 Version 2.0 review). An edge that is already exact at ``sig`` figures is unchanged."""
    import math
    x = float(x)
    if x == 0 or not math.isfinite(x):
        return x
    step = 10 ** (math.floor(math.log10(abs(x))) - sig + 1)
    q = x / step
    if abs(q - round(q)) < 1e-9:
        return round(round(q) * step, 12)
    return round((math.ceil(q) if up else math.floor(q)) * step, 12)


def par_table(key):
    """PAR table: for each governed CQA x RSM factor, the characterization range and both
    PARs (at-set-point and NOR-propagated), in natural units."""
    names = {p.key: p.name for p in CFG.unit_op(key).parameters}
    units = {p.key: p.unit for p in CFG.unit_op(key).parameters}
    rows = []
    for resp in list(responses(key)) + fragment_responses(key, "rsm"):
        acc = effective_acceptance(key, resp)
        if acc is None:
            continue
        # the criterion the two PAR columns were measured against, so the table does not
        # leave the reader to guess whether it was the step's limit or the drug substance's
        lo, hi, stype = acc
        # formatted as tables.num does: no scientific notation for a plain magnitude (≤ 16,000,
        # not ≤ 1.6e+04, which the PCR-005 Version 2.0 pdf showed)
        crit = (f"≥ {_fmt_crit(lo)}" if stype == "lower" else f"≤ {_fmt_crit(hi)}" if stype == "upper"
                else f"{_fmt_crit(lo)}–{_fmt_crit(hi)}")
        status = fit(key, "rsm", resp)["status"]
        basis = {"full": "model", "selected": "selected model", "none": "measured results"}[status]
        for factor in rsm_factors(key):
            p = CFG.unit_op(key).param(factor)
            rng_ = f"{p.prange[0]:g}–{p.prange[1]:g}"
            if status == "none":
                # PCMP-001 §7.2: no adequate model sets a range. The designs span the range
                # studied, so the range holds on the measured results when every one meets the
                # criterion, and is not established otherwise.
                par_s = par_n = rng_ if measured_met(key, resp) else "not established"
            else:
                par_s = _par_str(par_at_design_centre(key, resp, factor)["par_nat"])
                par_n = _par_str(par_nor_propagated(key, resp, factor)["par_nat"])
            rows.append([RESP_LABEL.get(resp, resp), names.get(factor, factor), rng_,
                         units.get(factor, ""), crit, par_s, par_n, basis])
    return pd.DataFrame(rows, columns=["CQA", "Parameter", "Char. range", "Unit",
                                       "Criterion", "PAR (set-point)", "PAR (NOR)", "Basis"])


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

    # predictions drawn at manufacturing scale (scale-down prediction minus the offset), so the
    # criterion is drawn as it stands
    mfg = lambda v: to_mfg(key, resp, v)
    ax[0].plot(ps["xs_nat"], mfg(ps["y"]), color="#2a78d6", lw=1.6)
    _limits(ax[0]); _shade(ax[0], ps["par_nat"]); _marks(ax[0])
    ax[0].set_title("At set-point (others fixed)", fontsize=10)
    ax[0].set_xlabel(f"{pname} ({unit})"); ax[0].set_ylabel(label)

    ax[1].plot(pn["xs_nat"], mfg(pn["med"]), color="#2a78d6", lw=1.6, label="median")
    ax[1].fill_between(pn["xs_nat"], mfg(pn["p_lo"]), mfg(pn["p_hi"]), color="#2a78d6", alpha=0.18,
                       lw=0, label="95% predictive")
    _limits(ax[1]); _shade(ax[1], pn["par_nat"]); _marks(ax[1])
    ax[1].set_title("Others varying within NOR (Monte-Carlo)", fontsize=10)
    ax[1].set_xlabel(f"{pname} ({unit})")

    h, l = ax[1].get_legend_handles_labels()
    ax[1].legend(h, l, fontsize=7, loc="best")
    fig.suptitle(f"Proven acceptable range — {label} vs {pname}", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    return fig


def fig_assurance():
    """INV-002: the probability of success (config key `assurance`) that the planned model meets
    PCMP-001 §7.2, against the number of further runs, one line per failing model with an effect;
    the target as a dashed line."""
    import matplotlib.pyplot as plt
    g = csv("augmentation_sample_size.csv")
    target = float(CFG.raw()["campaign"]["model_adequacy"]["assurance"])
    names = {"bioreactor": "Bioreactor", "protein_a": "Protein A",
             "viral_inactivation": "Low-pH inactivation", "cex": "Cation exchange",
             "aex": "Anion exchange", "virus_filtration": "Virus filtration"}
    attr = {"high_mannose": "high mannose", "acidic_variants": "acidic variants",
            "hcp_out_ng_mg": "host cell protein", "pool_hcp_ng_mg": "host cell protein",
            "lmw_cesds_pct": "fragments", "xmulv_lrf": "XMuLV clearance", "mvm_lrf": "MVM clearance",
            "leached_protein_a_ppm": "leached Protein A", "afucosylation": "afucosylation",
            "galactosylation": "galactosylation", "aggregates_hmw": "aggregate",
            "aggregate_out_pct": "aggregate"}
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    for (step, resp), x in g.groupby(["step_key", "response"], sort=False):
        ls = ":" if resp in ad.VIRAL else "-"
        ax.plot(x["m"], x["assurance"], ls, marker="o", ms=3, lw=1.3,
                label=f"{names.get(step, step)}, {attr.get(resp, resp)}")
    ax.axhline(target, color="#c0392b", lw=1.0, ls="--", label=f"target {target:.2f}")
    ax.set_xlabel("Further runs (D-optimal augmentation)")
    ax.set_ylabel("Probability of success")
    ax.set_ylim(-0.02, 1.02)
    ax.legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=3, frameon=False)
    fig.tight_layout()
    return fig


# --------------------------------------------------------------------------------------
# Version 2.0 support for the re-centred low-pH set-points (PCR-006, PD-006-01 and PD-006-02)
# --------------------------------------------------------------------------------------
#: the attributes of the low-pH hold study, with the method that measured each
OFAT_ATTR = {"aggregate_out_pct": ("Aggregate", "% HMW", "SEC"),
             "lmw_cesds_pct": ("Fragments", "% LMW", "nrCE-SDS"),
             "acidic_variants": ("Acidic variants", "%", "icIEF")}


def _ofat_method_sd(resp, level):
    """The repeatability of the method behind an attribute of the low-pH hold study, as an SD in
    the attribute's own unit at ``level``: SEC and icIEF from their CV, nrCE-SDS absolute."""
    raw = CFG.raw()
    if resp == "lmw_cesds_pct":
        return float(raw["analytics"]["methods"]["cesds"]["sd_abs"])
    if resp == "aggregate_out_pct":
        meth = {m["id"]: m for m in raw["deviations"]["methods"]}
        return float(meth["AMV-3221"]["precision_pct"]) / 100 * level
    return float(raw["analytics"]["sdm"]["assay_cv"]["acidic_variants"]) * level


def ofat_analysis():
    """S-VI-OFAT (PD-006-01): the low-pH hold at the re-centred pH against the former set-point.

    Per attribute, an analysis of covariance: the result on pH (two levels, as a factor) and hold
    time. The pH effect (re-centred minus former set-point) is taken from the model with both main
    effects, at any hold time, with its 95 % confidence interval and p-value; the p-values of the
    three attributes are adjusted by Holm's method, because three attributes were tested. The
    interaction (whether the rate of change with hold time differs between the two pH values) is
    tested in the model with it. The slope is the change per 60 min, common to both pH values.
    ``method_sd`` is the repeatability of the method at the mean level, so the pH effect can be set
    against it. ``diff_t0`` is the difference between the two pH values at time 0, the pH-adjusted
    load before any hold, where a hold effect cannot yet have acted. ``max_nor`` is the highest single result at the re-centred pH within the hold time
    NOR in force, ``max_all`` the highest over the study, and ``criterion`` the step's
    intermediate acceptance criterion for the attribute (low, high)."""
    import statsmodels.formula.api as smf
    o = CFG.raw()["analytics"]["vi_ofat"]
    d = csv("vi_ofat.csv").copy()
    new, old = float(CFG.unit_op("viral_inactivation").param("ph").setpoint), \
        float(CFG.unit_op("viral_inactivation").param("ph").setpoint_characterized)
    assert sorted({new, old}) == sorted(float(p) for p in o["ph"])
    d["new"] = (d["ph"] == new).astype(int)
    hold_nor = CFG.unit_op("viral_inactivation").param("hold_time").nor
    rows = []
    for resp, (name, unit, method) in OFAT_ATTR.items():
        main = smf.ols(f"{resp} ~ new + hold_min", data=d).fit()
        inter = smf.ols(f"{resp} ~ new * hold_min", data=d).fit()
        ci = main.conf_int(alpha=0.05).loc["new"]
        sl = main.params["hold_min"] * 60
        sl_ci = main.conf_int(alpha=0.05).loc["hold_min"] * 60
        at_new = d[d["new"] == 1]
        lo, hi, typ = ipc_limit("viral_inactivation", resp)
        lo, hi = (lo if typ in ("lower", "two_sided") else np.nan), (hi if typ in ("upper", "two_sided") else np.nan)
        rows.append({"response": resp, "attribute": name, "unit": unit, "method": method,
                     "n_per_ph": int((d["new"] == 1).sum()),
                     "mean_new": float(at_new[resp].mean()), "mean_old": float(d[d["new"] == 0][resp].mean()),
                     "ph_effect": float(main.params["new"]), "ph_lo": float(ci[0]), "ph_hi": float(ci[1]),
                     "p_ph": float(main.pvalues["new"]), "p_interaction": float(inter.pvalues["new:hold_min"]),
                     "slope_60": float(sl), "slope_lo": float(sl_ci[0]), "slope_hi": float(sl_ci[1]),
                     "p_slope": float(main.pvalues["hold_min"]),
                     "method_sd": _ofat_method_sd(resp, float(d[resp].mean())),
                     "max_nor": float(at_new[at_new["hold_min"] <= hold_nor[1]][resp].max()),
                     "max_all": float(at_new[resp].max()), "crit_lo": lo, "crit_hi": hi})
    out = pd.DataFrame(rows)
    # Holm's step-down adjustment over the attributes
    order = np.argsort(out["p_ph"].to_numpy())
    m, adj, run = len(out), np.empty(len(out)), 0.0
    for i, j in enumerate(order):
        run = max(run, min(1.0, (m - i) * float(out["p_ph"].iloc[j])))
        adj[j] = run
    out["p_ph_holm"] = adj
    alpha = float(CFG.raw()["campaign"]["thresholds"]["effect_alpha"])
    out["ph_significant"] = out["p_ph_holm"] < alpha
    # where an apparent pH effect sits: already before the hold (time 0, the pH-adjusted load) or
    # growing over it (the interaction)
    t0 = d[d["hold_min"] == d["hold_min"].min()]
    out["diff_t0"] = [float(t0[t0["new"] == 1][r].mean() - t0[t0["new"] == 0][r].mean()) for r in out["response"]]
    # judged per result, against both ends where the criterion has two
    at_nor = d[(d["new"] == 1) & (d["hold_min"] <= hold_nor[1])]
    out["min_nor"] = [float(at_nor[r].min()) for r in out["response"]]
    out["met_nor"] = [(np.isnan(r.crit_lo) or r.min_nor >= r.crit_lo) and (np.isnan(r.crit_hi) or r.max_nor <= r.crit_hi)
                      for r in out.itertuples()]
    return out


def cex_verification_summary(runs_file="cex_verification.csv"):
    """S-CEX-VER (PD-006-02): cation exchange runs at set-point on the worst-case material of the
    re-centred low-pH step, per attribute.

    ``f_required`` is the clearance fold the Version 2.0 criteria rely on (the platform worst case,
    or the 95 % bound that replaced it), ``f_data`` the fold the cation exchange data show at
    set-point, ``sigma_ln`` the run-to-run SD of the log fold, and ``n_required`` the number of runs
    the simulation gives for a power of ``analytics.cex_verification.power`` (``power_at_n``), at
    most ``n_max``; ``alpha_at_n`` is the probability of passing when the true fold equals the
    required one. The runs: the folds, their geometric mean, the one-sided 95 % lower confidence
    bound of the mean log fold with sigma known, and whether it reaches the required fold
    (``passed``). ``pool_max`` and ``pool_crit`` set the highest pool result against the cation
    exchange criterion for the attribute."""
    from scipy import stats as _st
    v = CFG.raw()["analytics"]["cex_verification"]
    g = csv("cex_verification_n.csv")
    runs = csv(runs_file)
    alpha = float(CFG.raw()["campaign"]["thresholds"]["effect_alpha"])
    z = float(_st.norm.ppf(1 - alpha))
    cols = {"aggregates_hmw": ("aggregate_fold", "aggregate_out_pct", "load_aggregate_pct", "Aggregate"),
            "fragments_lmw": ("fragment_fold", "lmw_cesds_pct", "load_lmw_cesds_pct", "Fragments")}
    rows = []
    for cqa in v["attributes"]:
        fcol, pcol, lcol, name = cols[cqa]
        gg = g[g["cqa"] == cqa]
        n_req = int(gg["n_required"].iloc[0])
        at = gg[gg["n"] == n_req].iloc[0]
        f = runs[fcol].to_numpy(float)
        sigma = float(gg["sigma_ln"].iloc[0])
        lb = float(np.exp(np.log(f).mean() - z * sigma / np.sqrt(len(f))))
        f_req = float(gg["f_required"].iloc[0])
        rows.append({"cqa": cqa, "attribute": name, "f_data": float(gg["f_data"].iloc[0]),
                     "f_required": f_req, "sigma_ln": sigma, "n_required": n_req,
                     "power_at_n": float(at["p_pass_at_data"]), "alpha_at_n": float(at["p_pass_at_required"]),
                     "n_runs": len(f), "folds": [float(x) for x in f],
                     "fold_gmean": float(np.exp(np.log(f).mean())), "fold_bound": lb,
                     "passed": bool(lb >= f_req), "every_run_above": bool((f >= f_req).all()),
                     "load_max": float(runs[lcol].max()), "pool_max": float(runs[pcol].max()),
                     "pool_crit": ipc_limit("cex", pcol)[1] if ipc_limit("cex", pcol) else np.nan})
    out = pd.DataFrame(rows)
    assert int(out["n_runs"].iloc[0]) == int(out["n_required"].max())   # as many runs as the larger need
    return out


def vi_worst_case_summary():
    """S-VI-WC (PD-006-03): the cation exchange decision on the material of the harshest combination
    within the PAR, by the same rule as S-CEX-VER (``cex_verification_summary``), and the hold output
    of each run against the step's intermediate acceptance criteria."""
    s = cex_verification_summary("vi_worst_case.csv")
    w = csv("vi_worst_case.csv")
    hold = []
    for col, resp in (("load_aggregate_pct", "aggregate_out_pct"), ("load_lmw_cesds_pct", "lmw_cesds_pct"),
                      ("load_acidic_variants", "acidic_variants")):
        lo, hi, typ = ipc_limit("viral_inactivation", resp)
        v = w[col].to_numpy(float)
        ok = ((v >= lo) if typ in ("lower", "two_sided") else True) & ((v <= hi) if typ in ("upper", "two_sided") else True)
        hold.append({"response": resp, "min": float(v.min()), "max": float(v.max()), "crit_lo": lo, "crit_hi": hi,
                     "spec_type": typ, "met": bool(np.all(ok))})
    return s, pd.DataFrame(hold)


def osmolality_analysis():
    """S-BRX-OSM (PD-003-01): each bioreactor output regressed on osmolality (a straight line over
    its three levels, with the other parameters at their least favourable NOR combination for acidic
    variants). Per output: the slope across the NOR, its p-value, and at each level the predicted mean
    and the 95 % prediction interval of a single batch, at manufacturing scale (the scale-down offset
    of the output applied), judged against the criterion of the step."""
    import statsmodels.formula.api as smf
    d = csv("osmolality_study.csv")
    o = CFG.raw()["analytics"]["osmolality_study"]
    p = CFG.unit_op("bioreactor").param(o["factor"])
    half = (p.nor[1] - p.nor[0]) / 2
    d = d.assign(x=(d[o["factor"]] - p.setpoint) / half)
    rows = []
    for resp in st.DOE_RESPONSES["bioreactor"]:
        m = smf.ols(f"{resp} ~ x", data=d).fit()
        acc = effective_acceptance("bioreactor", resp)
        for lev in sorted(d[o["factor"]].unique()):
            x = (lev - p.setpoint) / half
            sf = m.get_prediction(pd.DataFrame({"x": [x]})).summary_frame(alpha=1 - PI_LEVEL)
            # the study ran in the scale-down model: its results are taken to manufacturing scale by the
            # output's scale-down offset before they are judged, as every result is
            mean, plo, phi = (float(to_mfg("bioreactor", resp, float(sf[c].iloc[0])))
                              for c in ("mean", "obs_ci_lower", "obs_ci_upper"))
            lo, hi, typ = acc if acc else (np.nan, np.nan, None)
            rows.append({"response": resp, "level": float(lev), "slope_nor": float(m.params["x"]),
                         "p_slope": float(m.pvalues["x"]), "mean": mean, "pi_low": plo, "pi_high": phi,
                         "sd": float(np.sqrt(m.mse_resid)), "crit_lo": lo, "crit_hi": hi, "spec_type": typ,
                         "mean_met": None if typ is None else bool((typ == "upper" or mean >= lo) and (typ == "lower" or mean <= hi)),
                         "pi_met": None if typ is None else bool((typ == "upper" or plo >= lo) and (typ == "lower" or phi <= hi))})
    return pd.DataFrame(rows)


def par_margins(key):
    """How far each set-point and each NOR edge sits from the edge of its NOR-propagated PAR.

    One row per output with a criterion and an adequate model, and per response-surface factor:
    the set-point, the NOR, the PAR and the range studied, and the margins in the unit of the
    parameter. ``sp_lo``/``sp_hi`` are set-point minus the lower PAR edge and upper PAR edge minus
    set-point, ``nor_lo``/``nor_hi`` the same from the NOR edges. A PAR edge that coincides with
    the end of the range studied is where the study stopped, not where the criterion fails, and
    its margins are None. ``contains_nor`` is False when the NOR reaches outside the PAR. Run it
    inside :func:`characterized_nor` for the set-points and NOR the studies were run around."""
    uo = CFG.unit_op(key)
    rows = []
    for resp in responses(key):
        if effective_acceptance(key, resp) is None or fit(key, "rsm", resp)["status"] == "none":
            continue
        for f in rsm_factors(key):
            p = uo.param(f)
            par = par_nor_propagated(key, resp, f)["par_nat"]
            tol = 1e-6 * (p.prange[1] - p.prange[0])
            if par is None:
                rows.append({"response": resp, "factor": f, "setpoint": p.setpoint, "nor_low": p.nor[0],
                             "nor_high": p.nor[1], "range_low": p.prange[0], "range_high": p.prange[1],
                             "par_low": None, "par_high": None, "sp_lo": None, "sp_hi": None,
                             "nor_lo": None, "nor_hi": None, "contains_nor": False})
                continue
            lo, hi = float(par[0]), float(par[1])
            lo_edge, hi_edge = lo > p.prange[0] + tol, hi < p.prange[1] - tol
            rows.append({"response": resp, "factor": f, "setpoint": p.setpoint, "nor_low": p.nor[0],
                         "nor_high": p.nor[1], "range_low": p.prange[0], "range_high": p.prange[1],
                         "par_low": lo, "par_high": hi,
                         "sp_lo": p.setpoint - lo if lo_edge else None, "sp_hi": hi - p.setpoint if hi_edge else None,
                         "nor_lo": p.nor[0] - lo if lo_edge else None, "nor_hi": hi - p.nor[1] if hi_edge else None,
                         "contains_nor": bool(lo <= p.nor[0] + tol and hi >= p.nor[1] - tol)})
    return pd.DataFrame(rows)


def nor_worst_corner(key, resp):
    """The least favourable combination of NOR low, set-point and NOR high for an output with a
    criterion, at manufacturing scale: the settings, the predicted value (the median on a log-scale
    model) and the 95 % prediction interval of a single run there, and whether that interval meets
    the criterion. For a two-sided criterion the corner is the one whose interval comes nearest to
    either limit, relative to the width of the criterion. None when the output has no criterion or
    no adequate model."""
    # the manufacturing-scale criterion, against predictions taken to manufacturing scale (the
    # same judgement as nor_met, which moves the criterion to the scale-down scale instead)
    acc = effective_acceptance(key, resp)
    if acc is None or _judging(key, resp) is None or fit(key, "rsm", resp)["status"] == "none":
        return None
    lo, hi, stype = acc
    r = fit(key, "rsm", resp)
    uo = CFG.unit_op(key)
    grid = list(itertools.product(*[[uo.param(f).nor[0], uo.param(f).setpoint, uo.param(f).nor[1]]
                                    for f in r["factors"]]))
    nat = {f: [g[i] for g in grid] for i, f in enumerate(r["factors"])}
    m, plo, phi = prediction_interval(key, resp, nat)
    m, plo, phi = (np.asarray(to_mfg(key, resp, v), float) for v in (m, plo, phi))
    if stype == "upper":
        score, side = phi - hi, "upper"
    elif stype == "lower":
        score, side = lo - plo, "lower"
    else:
        w = hi - lo
        s_lo, s_hi = (lo - plo) / w, (phi - hi) / w
        score = np.maximum(s_lo, s_hi)
        side = None
    i = int(np.argmax(score))
    if side is None:
        side = "lower" if (lo - plo[i]) >= (phi[i] - hi) else "upper"
    return {"settings": {f: float(nat[f][i]) for f in r["factors"]}, "predicted": float(m[i]),
            "pi_low": float(plo[i]), "pi_high": float(phi[i]), "side": side,
            "met": bool(_in_spec(np.array([plo[i]]), lo, hi, stype)[0] and _in_spec(np.array([phi[i]]), lo, hi, stype)[0]),
            "median_met": bool(_in_spec(np.array([m[i]]), lo, hi, stype)[0]), "criterion": (lo, hi, stype)}


def selection_comparison():
    """INV-002: for every response-surface output with a criterion (``model_adequacy.csv``), the
    model the exhaustive AICc search of CA3 selects against the models a stepwise search by AICc
    would have stopped at (backward from the full quadratic, forward from the mean), on the same
    scale and runs. An output the data give without error has no AICc (``exact``) and is left out
    of the comparison. ``backward_worse``/``forward_worse``: the stepwise search stopped at a model
    with a higher AICc than the best candidate."""
    rows = []
    m = csv("model_adequacy.csv")
    for _, r in m.iterrows():
        f = fit(r["step_key"], "rsm", r["response"])
        row = {"step_key": r["step_key"], "response": r["response"], "scale": f["transform"] or "raw",
               "exact": bool(f.get("exact", False)), "n_terms": len(f["names"]), "aicc": f["aicc"]}
        if not row["exact"]:
            for direction in ("backward", "forward"):
                sw = ad.stepwise_aicc(f["df"], f["ycol"], f["factors"], bool(f["block"]), direction)
                row[f"{direction}_terms"] = len(sw["terms"])
                row[f"{direction}_aicc"] = sw["aicc"]
                row[f"{direction}_worse"] = bool(sw["aicc"] > f["aicc"] + 1e-6)
        rows.append(row)
    return pd.DataFrame(rows)


def augmentation_prediction_check():
    """INV-002: an independent check of the models selected on the planned runs. For every output
    of a step with an INV-002 augmentation, the model selected on the planned runs alone predicts
    the augmentation runs, which it has not seen: how many of them fall inside its 95 % prediction
    interval, the root mean square error of those predictions against the model's own residual SD
    (on the scale of the model), and the block term of the model on all runs (a shift between the
    two blocks would explain misses that the model does not)."""
    rows = []
    for key in st.DOE_FACTORS:
        if not has_augmentation(key):
            continue
        aug = csv(f"doe_{key}_aug.csv")
        for resp in list(responses(key)) + fragment_responses(key, "rsm"):
            if resp not in aug.columns or aug[resp].isna().all():
                continue
            fp = fit(key, "rsm", resp, runs="planned")
            if fp["status"] == "none":
                continue
            a = aug[aug[resp].notna()].reset_index(drop=True)
            coded = pd.DataFrame({f: a["coded_" + f] for f in fp["factors"]})
            sf = fp["model"].get_prediction(_design_matrix(fp, coded)).summary_frame(alpha=0.05)
            y = a[resp].to_numpy(float)
            y = np.log(y) if fp["transform"] == "log" else y
            inside = (y >= sf["obs_ci_lower"].to_numpy()) & (y <= sf["obs_ci_upper"].to_numpy())
            fa = fit(key, "rsm", resp)
            m = fa["model"]
            rows.append({"step_key": key, "response": resp, "scale_planned": fp["transform"] or "raw",
                         "terms_planned": list(fp["names"]), "terms_all": list(fa["names"]),
                         "scale_all": fa["transform"] or "raw", "n_new": int(len(a)),
                         "inside_pi": int(inside.sum()),
                         "rmsep": float(np.sqrt(np.mean((y - sf["mean"].to_numpy()) ** 2))),
                         "rmse_model": float(np.sqrt(fp["model"].mse_resid)),
                         "block_coef": float(m.params.get(ad.BLOCK, np.nan)),
                         "block_p": float(m.pvalues.get(ad.BLOCK, np.nan))})
    return pd.DataFrame(rows)


def verification_all_runs():
    """INV-002: the verification of the platform worst cases (``iac.verification``), which uses the
    planned runs because the criteria were fixed before the augmentation runs existed, repeated on
    all runs for each step with an augmentation, so a report can say whether the extra runs would
    have moved a criterion. Rows as in ``iac_verification.csv`` for those steps."""
    from amab_process import iac as _iac, load_config
    cfg = load_config()
    rows = []
    v = csv("iac_verification.csv")
    ps = csv("process_summary.csv")
    for key in [k for k in st.DOE_FACTORS if has_augmentation(k)]:
        if key not in set(v["step_key"]):
            continue
        data = {key: rsm_data(key, runs="all", corrected=False)}
        # only this step's rows are kept; the low-pH acidic-variant feed is not needed for them
        out = _iac.verification(cfg, data, ps, _nominal_fragments(), vi_feed_acidic=float("nan"))
        rows.append(out[out["step_key"] == key])
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def _nominal_fragments():
    from amab_process import analytics as _an, load_config
    return _an.nominal_train(load_config())

