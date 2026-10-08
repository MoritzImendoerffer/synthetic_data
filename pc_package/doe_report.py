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
PAR_GRID = 81            # parameter grid points across the characterization range

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
# within its NOR, and widened only where the 95 % confidence bound of the A-Mab worst case beats
# the platform value (config `iac.allow_widening`, owner's decision 2026-10-08). The table is outputs/data/iac.csv; nothing here
# computes a limit, it only reads one. The Rev 1.0 criteria, fitted after the data were seen
# (INV-001), are outputs/data/criteria_rev1.csv and are read only to tabulate the change.
# --------------------------------------------------------------------------------------
def _iac_row(key, resp):
    t = csv("iac.csv")
    r = t[(t["step_key"] == key) & (t["response"] == resp)]
    return None if r.empty else r.iloc[0]


_CRITERIA = {"rev": "2.0"}


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
    dfp = len(a) + len(b) - 2
    sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / dfp)
    ci = float(CFG.raw()["analytics"]["sdm"].get("offset_ci", 0.90))
    half = float(_st.t.ppf(0.5 + ci / 2, dfp) * sp * np.sqrt(1 / len(a) + 1 / len(b)))
    off = float(a.mean() - b.mean())
    return dict(n_sd=len(a), n_m=len(b), mean_sd=float(a.mean()), mean_m=float(b.mean()),
                offset=off, lo=off - half, hi=off + half, half=half, df=dfp, ci=ci)


def _offset_value(key, resp):
    """The offset the current judgement applies (0 in Version 1.0 mode, when switched off in the
    config, or when the output has no SDM data)."""
    if _CRITERIA["rev"] == "1.0" or _OFFSET["end"] == "none":
        return 0.0
    if not CFG.raw()["analytics"]["sdm"].get("apply_offset", False):
        return 0.0
    o = sdm_offset(key, resp, _OFFSET.get("studies"))
    if o is None:
        return 0.0
    return {"point": o["offset"], "lo": o["lo"], "hi": o["hi"]}[_OFFSET["end"]]


def _judging(key, resp):
    """(lo, hi, stype) as the scale-down prediction is judged: the criterion moved by the offset.
    A scale-down value y meets the criterion when y - offset does, that is when
    lo + offset <= y <= hi + offset."""
    acc = effective_acceptance(key, resp)
    if acc is None:
        return None
    d = _offset_value(key, resp)
    return acc[0] + d, acc[1] + d, acc[2]


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


def nor_met(key, resp):
    """Does the output meet its criterion across the NOR, at manufacturing scale? Judged at every
    combination of NOR low, set-point and NOR high of the response-surface factors: for a quality
    attribute the 95 % prediction interval of a single run, for viral clearance the mean.
    None when the output has no criterion or no response-surface model."""
    acc = _judging(key, resp)
    if acc is None:
        return None
    try:
        r = fit(key, "rsm", resp)
    except Exception:
        return None
    uo = CFG.unit_op(key)
    grid = list(itertools.product(*[[uo.param(f).nor[0], uo.param(f).setpoint, uo.param(f).nor[1]]
                                    for f in r["factors"]]))
    nat = {f: [g[i] for g in grid] for i, f in enumerate(r["factors"])}
    lo, hi, stype = acc
    if decision_statistic(resp) == "batch":
        _, plo, phi = prediction_interval(key, resp, nat)
        return bool(np.all(_in_spec(plo, lo, hi, stype)) and np.all(_in_spec(phi, lo, hi, stype)))
    return bool(np.all(_in_spec(np.asarray(predict(key, resp, natural=nat)), lo, hi, stype)))


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
    criteria (criteria_rev1.csv). Used to state, from the data, which Version 1.0 conclusions
    moved at Version 2.0. Never used to produce a Version 2.0 result."""
    def __enter__(self):
        _CRITERIA["rev"] = "1.0"
        return self

    def __exit__(self, *a):
        _CRITERIA["rev"] = "2.0"
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


def par_at_design_centre(key, resp, factor, n_grid=201):
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
        w = max((p.nor[1] - p.nor[0]) / 6.0, 1e-9)
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
        return np.einsum("ij,ij->i", X, b) + noise
    return _predict_points(r, coded[r["factors"]]) + (noise if residual else 0.0)


def _design_matrix(r, coded):
    """The model matrix of a fitted RSM at coded settings, columns in the model's own order."""
    X = pd.DataFrame({"const": np.ones(len(coded))}, index=coded.index)
    for f in r["factors"]:
        X[f] = np.asarray(coded[f], dtype=float)
    for a, b in itertools.combinations(r["factors"], 2):
        X[f"{a}:{b}"] = X[a].values * X[b].values
    if r["quad"]:
        for f in r["factors"]:
            X[f"{f}^2"] = X[f].values ** 2
    return X[["const"] + r["names"]].to_numpy()


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
    return sf["mean"].to_numpy(), sf["obs_ci_lower"].to_numpy(), sf["obs_ci_upper"].to_numpy()


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


def design_space_grid(key, n=11):
    """How much of the characterized region actually meets every criterion this step governs.

    Once a step has intermediate acceptance criteria, the design space stops being "the whole characterized
    region" as a matter of course: a parameter whose PAR is narrower than its characterization
    range is, by definition, a parameter some of whose characterized settings are unacceptable.
    This evaluates the fitted response-surface models on an evenly spaced grid over the coded
    cube and reports what survives, so a report can state the size of its region from the data
    instead of asserting it.

    Returns a dict with ``fraction`` (share of grid points inside every criterion),
    ``per_response`` (share each response alone rejects) and ``binding`` (the response that
    rejects most). Uses mean predictions, matching the design-space convention of the reports.
    """
    fs = rsm_factors(key)
    grids = np.meshgrid(*[np.linspace(-1, 1, n)] * len(fs), indexing="ij")
    coded = pd.DataFrame({f: g.ravel() for f, g in zip(fs, grids)})
    ok = np.ones(len(coded), dtype=bool)
    per = {}
    for resp in responses(key):
        acc = _judging(key, resp)
        if acc is None:
            continue
        lo, hi, stype = acc
        y = _predict_points(fit(key, "rsm", resp), coded)
        good = _in_spec(y, lo, hi, stype)
        per[resp] = float(1.0 - good.mean())
        ok &= good
    binding = max(per, key=per.get) if per else None
    return {"fraction": float(ok.mean()), "per_response": per, "binding": binding,
            "n_points": int(len(coded))}


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
        for factor in rsm_factors(key):
            p = CFG.unit_op(key).param(factor)
            ps = par_at_design_centre(key, resp, factor)
            pn = par_nor_propagated(key, resp, factor)
            rows.append([RESP_LABEL.get(resp, resp), names.get(factor, factor),
                         f"{p.prange[0]:g}–{p.prange[1]:g}", units.get(factor, ""),
                         crit, _par_str(ps["par_nat"]), _par_str(pn["par_nat"])])
    return pd.DataFrame(rows, columns=["CQA", "Parameter", "Char. range", "Unit",
                                       "Criterion", "PAR (set-point)", "PAR (NOR)"])


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
    d = _offset_value(key, resp)
    ax[0].plot(ps["xs_nat"], ps["y"] - d, color="#2a78d6", lw=1.6)
    _limits(ax[0]); _shade(ax[0], ps["par_nat"]); _marks(ax[0])
    ax[0].set_title("At set-point (others fixed)", fontsize=10)
    ax[0].set_xlabel(f"{pname} ({unit})"); ax[0].set_ylabel(label)

    ax[1].plot(pn["xs_nat"], pn["med"] - d, color="#2a78d6", lw=1.6, label="median")
    ax[1].fill_between(pn["xs_nat"], pn["p_lo"] - d, pn["p_hi"] - d, color="#2a78d6", alpha=0.18,
                       lw=0, label="95% predictive")
    _limits(ax[1]); _shade(ax[1], pn["par_nat"]); _marks(ax[1])
    ax[1].set_title("Others varying within NOR (Monte-Carlo)", fontsize=10)
    ax[1].set_xlabel(f"{pname} ({unit})")

    h, l = ax[1].get_legend_handles_labels()
    ax[1].legend(h, l, fontsize=7, loc="best")
    fig.suptitle(f"Proven acceptable range — {label} vs {pname}", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    return fig
