"""Model adequacy of the response-surface designs (PCMP-001 §7.2) and its two remedies (INV-002).

PCMP-001 Version 2.0 §7.2 judges a response-surface model adequate for prediction when its F-test is
significant, its lack of fit against pure error is not, and its predicted R² falls short of R² by no
more than ``campaign.thresholds.max_r2_minus_pred_r2``. A model that fails the lack-of-fit test or that
limit "is either refitted with a justified change of terms or transformation, or it is not used to set
a range". The Version 2.0 re-analysis found 14 full quadratic models with a criterion that fail the
limit (INV-002). Two remedies follow, chosen by a rule stated in INV-002 before any new run was made
(``campaign.model_adequacy``):

* **Augmentation.** For an attribute of the drug substance specification on which the planned design
  shows an effect, further runs are added to the design as a second block, in a D-optimal augmentation
  of the face-centred design, and the planned model (full quadratic plus a block term) is fitted to all
  runs. The number of runs is the smallest that gives an assurance of at least ``assurance`` that the
  model meets §7.2, simulated from what the planned runs show.
* **Refit.** Every other failing model is refitted by hierarchical backward elimination at
  ``effect_alpha``. A response with no adequate model, full or refitted, is judged on its measured
  results.

This module is the one implementation of the model matrix, the adequacy statistics, the refit, the
assurance and the augmentation. The data generator (which plans and runs the augmentation) and the
report engine (which judges with the model each response ends up with) both import it.
"""
from __future__ import annotations

import itertools
from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

BLOCK = "block"
VIRAL = ("xmulv_lrf", "mvm_lrf")


# --------------------------------------------------------------------------------------
# Model terms and matrix
# --------------------------------------------------------------------------------------
def full_terms(factors: Sequence[str], quad: bool = True) -> List[str]:
    """Main effects, two-factor interactions and (``quad``) squares, in model order."""
    t = list(factors) + [f"{a}:{b}" for a, b in itertools.combinations(factors, 2)]
    return t + [f"{f}^2" for f in factors] if quad else t


def parents(term: str) -> List[str]:
    if ":" in term:
        return term.split(":")
    if term.endswith("^2"):
        return [term[:-2]]
    return []


def block_code(block) -> np.ndarray:
    """Effect coding of a two-block design: planned runs -1, augmentation runs +1, so that a
    prediction at block 0 is the average of the two blocks."""
    b = np.asarray(block, dtype=float)
    return np.where(b <= 1, -1.0, 1.0)


def matrix(df: pd.DataFrame, terms: Sequence[str], block: bool = False) -> pd.DataFrame:
    """The model matrix: a constant, the terms from the ``coded_<factor>`` columns, and the block."""
    X = pd.DataFrame({"const": np.ones(len(df))}, index=df.index)
    for t in terms:
        if ":" in t:
            a, b = t.split(":")
            X[t] = df["coded_" + a].to_numpy(float) * df["coded_" + b].to_numpy(float)
        elif t.endswith("^2"):
            X[t] = df["coded_" + t[:-2]].to_numpy(float) ** 2
        else:
            X[t] = df["coded_" + t].to_numpy(float)
    if block:
        X[BLOCK] = block_code(df[BLOCK])
    return X


def has_blocks(df: pd.DataFrame) -> bool:
    return BLOCK in df.columns and df[BLOCK].nunique() > 1


# --------------------------------------------------------------------------------------
# Adequacy statistics (PCMP-001 §7.2, criteria 1-3)
# --------------------------------------------------------------------------------------
def _pure_error(df: pd.DataFrame, y: np.ndarray, factors: Sequence[str]):
    """Pure error from replicated settings within a block (the centre points of a planned design,
    and any point an augmentation repeats in its own block)."""
    cols = ["coded_" + f for f in factors] + ([BLOCK] if BLOCK in df.columns else [])
    keys = df[cols].round(6).astype(str).agg("|".join, axis=1).to_numpy()
    ss, dfree = 0.0, 0
    for k in np.unique(keys):
        g = y[keys == k]
        if len(g) > 1:
            ss += float(((g - g.mean()) ** 2).sum())
            dfree += len(g) - 1
    return ss, dfree


def adequacy(df: pd.DataFrame, resp: str, factors: Sequence[str], terms: Sequence[str],
             thresholds: Dict[str, float], block: Optional[bool] = None) -> Dict[str, object]:
    """Fit ``terms`` (plus a block term when the data hold two blocks) and judge them against
    §7.2. ``adequate`` is the range-setting test of §7.2: no significant lack of fit and the
    overfitting limit met. ``f_ok`` is criterion 1 (a significant model)."""
    d = df[df[resp].notna()]
    blk = has_blocks(d) if block is None else block
    X = matrix(d, terms, blk)
    y = d[resp].to_numpy(float)
    m = sm.OLS(y, X).fit()
    h = m.get_influence().hat_matrix_diag
    press = float(np.sum((m.resid / (1 - h)) ** 2))
    sst = float(np.sum((y - y.mean()) ** 2))
    pred = 1 - press / sst if sst > 0 else float("nan")
    ss_pe, df_pe = _pure_error(d, y, factors)
    sse = float((m.resid ** 2).sum())
    df_lof = int(m.df_resid) - df_pe
    ss_lof = max(sse - ss_pe, 0.0)
    f_lof = (ss_lof / df_lof) / (ss_pe / df_pe) if (df_pe > 0 and df_lof > 0 and ss_pe > 0) else float("nan")
    p_lof = float(stats.f.sf(f_lof, df_lof, df_pe)) if np.isfinite(f_lof) else float("nan")
    gap = float(m.rsquared - pred)
    lof_ok = not (p_lof < float(thresholds["lof_alpha"]))
    gap_ok = gap <= float(thresholds["max_r2_minus_pred_r2"])
    # an intercept-only model has no F-test; it describes "no effect", which is a finding, not a failure
    p_model = float(m.f_pvalue) if len(terms) else float("nan")
    return dict(model=m, terms=list(terms), block=blk, n=int(m.nobs), k=int(X.shape[1]),
                R2=float(m.rsquared), adjR2=float(m.rsquared_adj), predR2=pred, gap=gap,
                p=p_model, F=float(m.fvalue) if len(terms) else float("nan"),
                rmse=float(np.sqrt(m.mse_resid)), sse=sse, ss_pe=ss_pe, df_pe=df_pe,
                ss_lof=ss_lof, df_lof=df_lof, F_lof=f_lof, p_lof=p_lof,
                lof_ok=lof_ok, gap_ok=gap_ok, adequate=bool(lof_ok and gap_ok),
                f_ok=bool(len(terms) and p_model < float(thresholds["effect_alpha"])))


# --------------------------------------------------------------------------------------
# The refit: hierarchical backward elimination
# --------------------------------------------------------------------------------------
def reduce(df: pd.DataFrame, resp: str, factors: Sequence[str], terms: Sequence[str],
           alpha: float, block: Optional[bool] = None) -> List[str]:
    """Remove, one at a time, the least significant term that no remaining term contains (a main
    effect stays while an interaction or square of it remains), until every removable term is
    significant at ``alpha``. A block term is part of the design and is never removed."""
    d = df[df[resp].notna()]
    blk = has_blocks(d) if block is None else block
    terms = list(terms)
    y = d[resp].to_numpy(float)
    while terms:
        m = sm.OLS(y, matrix(d, terms, blk)).fit()
        needed = {p for t in terms for p in parents(t)}
        pv = {t: float(m.pvalues[t]) for t in terms if t not in needed}
        worst = max(pv, key=lambda t: (pv[t], -terms.index(t)))
        if pv[worst] < alpha:
            break
        terms.remove(worst)
    return terms


def significant(fit: Dict[str, object], alpha: float) -> List[str]:
    m = fit["model"]
    return [t for t in fit["terms"] if float(m.pvalues[t]) < alpha]


# --------------------------------------------------------------------------------------
# D-optimal augmentation of a face-centred design
# --------------------------------------------------------------------------------------
def _fmat(points: np.ndarray, quad: bool, block: np.ndarray) -> np.ndarray:
    n, k = points.shape
    cols = [np.ones(n)] + [points[:, i] for i in range(k)]
    cols += [points[:, i] * points[:, j] for i, j in itertools.combinations(range(k), 2)]
    if quad:
        cols += [points[:, i] ** 2 for i in range(k)]
    cols += [np.asarray(block, dtype=float)]
    return np.column_stack(cols)


def d_optimal_augment(planned: np.ndarray, m: int, quad: bool = True) -> np.ndarray:
    """``m`` runs on the face-centred levels (-1, 0, +1) that maximise det(X'X) of the full
    quadratic model with a block term, the planned runs held fixed (block -1, new runs +1).
    Greedy sequential selection, then Fedorov exchange to convergence. Deterministic: ties go to
    the first candidate in lexicographic order, so the design needs no random number."""
    k = planned.shape[1]
    cand = np.array(list(itertools.product([-1.0, 0.0, 1.0], repeat=k)))
    X0 = _fmat(planned, quad, -np.ones(len(planned)))
    Fc = _fmat(cand, quad, np.ones(len(cand)))
    M = X0.T @ X0 + 1e-6 * np.eye(X0.shape[1])
    chosen: List[int] = []
    for _ in range(m):
        v = np.einsum("ij,jk,ik->i", Fc, np.linalg.inv(M), Fc)
        j = int(np.argmax(np.round(v, 12)))
        chosen.append(j)
        M = M + np.outer(Fc[j], Fc[j])

    def logdet(idx):
        Xa = np.vstack([X0, Fc[idx]])
        s, ld = np.linalg.slogdet(Xa.T @ Xa)
        return ld if s > 0 else -np.inf

    best, improved = logdet(chosen), True
    while improved:
        improved = False
        for pos in range(m):
            for j in range(len(cand)):
                if j == chosen[pos]:
                    continue
                trial = chosen.copy()
                trial[pos] = j
                ld = logdet(trial)
                if ld > best + 1e-9:
                    best, chosen, improved = ld, trial, True
    return cand[sorted(chosen)]


# --------------------------------------------------------------------------------------
# Sample size: the assurance that the planned model meets §7.2 after an augmentation
# --------------------------------------------------------------------------------------
def assurance(df: pd.DataFrame, resp: str, factors: Sequence[str], truth_terms: Sequence[str],
              aug: np.ndarray, thresholds: Dict[str, float], reps: int,
              rng: np.random.Generator, quad: bool = True) -> Dict[str, object]:
    """Simulate the response from what the planned runs show (the refitted model and its residual
    standard deviation), on the planned runs plus the augmentation ``aug``; fit the planned model
    (full quadratic, with a block term when ``aug`` has runs) to each simulated data set; return
    the share that meets §7.2 (no significant lack of fit and the overfitting limit), the median
    gap, and the power for each significant term of the refitted model."""
    d = df[df[resp].notna()]
    planned = d[["coded_" + f for f in factors]].to_numpy(float)
    truth = sm.OLS(d[resp].to_numpy(float), matrix(d, truth_terms)).fit()
    sigma = float(np.sqrt(truth.mse_resid))
    pts = np.vstack([planned, aug]) if len(aug) else planned
    blk = np.r_[-np.ones(len(planned)), np.ones(len(aug))]
    cd = pd.DataFrame(pts, columns=["coded_" + f for f in factors])
    mu = matrix(cd, truth_terms).to_numpy() @ truth.params.to_numpy()
    X = _fmat(pts, quad, blk)
    if not len(aug):
        X = X[:, :-1]
    n, p = X.shape
    XtXi = np.linalg.pinv(X.T @ X)
    h = np.einsum("ij,jk,ik->i", X, XtXi, X)
    Y = mu[:, None] + rng.normal(0.0, sigma, (n, reps))
    B = XtXi @ X.T @ Y
    E = Y - X @ B
    sse = (E ** 2).sum(0)
    sst = ((Y - Y.mean(0)) ** 2).sum(0)
    gap = (1 - sse / sst) - (1 - ((E / (1 - h)[:, None]) ** 2).sum(0) / sst)
    keys = [tuple(np.round(r, 6)) + (b,) for r, b in zip(pts, blk)]
    groups: Dict[tuple, List[int]] = {}
    for i, kk in enumerate(keys):
        groups.setdefault(kk, []).append(i)
    reps_ = [g for g in groups.values() if len(g) > 1]
    ss_pe = sum(((Y[g] - Y[g].mean(0)) ** 2).sum(0) for g in reps_) if reps_ else np.zeros(reps)
    df_pe = sum(len(g) - 1 for g in reps_)
    df_lof = (n - p) - df_pe
    if df_lof > 0 and df_pe > 0:
        p_lof = stats.f.sf(((sse - ss_pe) / df_lof) / (ss_pe / df_pe), df_lof, df_pe)
    else:
        p_lof = np.ones(reps)
    ok = (gap <= float(thresholds["max_r2_minus_pred_r2"])) & (p_lof >= float(thresholds["lof_alpha"]))
    cols = ["const"] + full_terms(factors, quad) + ([BLOCK] if len(aug) else [])
    mse = sse / (n - p)
    tcrit = stats.t.ppf(1 - float(thresholds["effect_alpha"]) / 2, n - p)
    power = {}
    for t in truth_terms:
        if float(truth.pvalues[t]) < float(thresholds["effect_alpha"]):
            j = cols.index(t)
            power[t] = float((np.abs(B[j] / np.sqrt(mse * XtXi[j, j])) > tcrit).mean())
    return {"assurance": float(ok.mean()), "median_gap": float(np.median(gap)), "power": power,
            "sigma": sigma}


# --------------------------------------------------------------------------------------
# The plan of INV-002: a remedy for every failing model, and the augmentation of each step
# --------------------------------------------------------------------------------------
def plan(cfg, rsm: Dict[str, pd.DataFrame], rng_for) -> Dict[str, object]:
    """Apply §7.2 to every response-surface model that carries a criterion, on the planned runs,
    and decide each failing model's remedy by the rule of ``campaign.model_adequacy``.

    ``rng_for(step_index, response_index)`` returns the random stream of one assurance curve.
    Returns the per-model table (``models``), the sample-size grid (``grid``), the per-step plan
    (``steps``) and the coded augmentation design of each augmented step (``designs``)."""
    raw = cfg.raw()
    th = {k: float(v) for k, v in raw["campaign"]["thresholds"].items()}
    ma = raw["campaign"]["model_adequacy"]
    alpha, target, reps, stepsz = th["effect_alpha"], float(ma["assurance"]), int(ma["reps"]), int(ma["step"])
    not_spec = set(ma["not_specification"])
    crit = raw["iac"]["responses"]
    models, grid, steps, designs = [], [], [], {}
    for si, (step, df) in enumerate(rsm.items()):
        factors = [c[len("coded_"):] for c in df.columns if c.startswith("coded_")]
        resps = [r for r in crit.get(step, []) if r in df.columns and df[r].notna().all()]
        planned = df[["coded_" + f for f in factors]].to_numpy(float)
        sizes = list(range(stepsz, int(len(df) * float(ma["max_fraction_of_planned"])) + 1, stepsz))
        cache: Dict[int, np.ndarray] = {}
        need_m = []
        for ri, resp in enumerate(resps):
            full = adequacy(df, resp, factors, full_terms(factors), th)
            row = {"step_key": step, "response": resp, "n": full["n"], "k": full["k"],
                   "R2": full["R2"], "adjR2": full["adjR2"], "predR2": full["predR2"], "gap": full["gap"],
                   "p_model": full["p"], "p_lof": full["p_lof"], "adequate": full["adequate"],
                   "reduced_terms": "", "reduced_k": np.nan, "reduced_gap": np.nan,
                   "reduced_p_lof": np.nan, "reduced_adequate": np.nan, "effects": "",
                   "m_required": np.nan, "assurance_at_m": np.nan, "remedy": "none", "reason": ""}
            if not full["adequate"]:
                rt = reduce(df, resp, factors, full_terms(factors), alpha)
                red = adequacy(df, resp, factors, rt, th)
                sig = significant(red, alpha)
                row.update(reduced_terms=" ".join(rt), reduced_k=red["k"], reduced_gap=red["gap"],
                           reduced_p_lof=red["p_lof"], reduced_adequate=red["adequate"],
                           effects=" ".join(sig))
                m_req, a_req = None, None
                if sig:
                    rng = rng_for(si, ri)
                    for m in [0] + sizes:
                        if m and m not in cache:
                            cache[m] = d_optimal_augment(planned, m)
                        aug = cache[m] if m else np.zeros((0, len(factors)))
                        a = assurance(df, resp, factors, rt, aug, th, reps, rng)
                        grid.append({"step_key": step, "response": resp, "m": m,
                                     "n_total": len(df) + m, "assurance": a["assurance"],
                                     "median_gap": a["median_gap"],
                                     "min_power": min(a["power"].values()) if a["power"] else np.nan,
                                     "power": " ".join(f"{t}={v:.3f}" for t, v in a["power"].items())})
                        if m_req is None and m and a["assurance"] >= target:
                            m_req, a_req = m, a["assurance"]
                if resp in not_spec:
                    remedy, reason = "refit", "not a drug substance test"
                elif not sig:
                    remedy, reason = "refit", "no effect to resolve"
                elif m_req is None:
                    remedy, reason = "refit", "assurance not reached within the size of the planned design"
                else:
                    remedy, reason = "augment", "attribute of the drug substance specification with an effect"
                    need_m.append(m_req)
                row.update(m_required=m_req if m_req is not None else np.nan,
                           assurance_at_m=a_req if a_req is not None else np.nan,
                           remedy=remedy, reason=reason)
            models.append(row)
        if need_m:
            m_step = max(need_m)
            designs[step] = cache[m_step]
            steps.append({"step_key": step, "n_planned": len(df), "m": m_step,
                          "responses": " ".join(r["response"] for r in models
                                                if r["step_key"] == step and r["remedy"] == "augment")})
    return {"models": pd.DataFrame(models), "grid": pd.DataFrame(grid),
            "steps": pd.DataFrame(steps, columns=["step_key", "n_planned", "m", "responses"]),
            "designs": designs}


# --------------------------------------------------------------------------------------
# Transformation (the other remedy PCMP-001 §7.2 names): the log scale, where the data support it
# --------------------------------------------------------------------------------------
def boxcox_interval(df: pd.DataFrame, resp: str, factors: Sequence[str], terms: Sequence[str],
                    level: float = 0.95, grid=None) -> Dict[str, float]:
    """Profile likelihood of the Box-Cox exponent λ for the model ``terms``: the estimate and its
    ``level`` interval (likelihood within chi²₁(level)/2 of the maximum). The log scale is λ = 0, the
    raw scale λ = 1. The response must be positive."""
    d = df[df[resp].notna()]
    y = d[resp].to_numpy(float)
    X = matrix(d, terms, has_blocks(d)).to_numpy()
    n = len(y)
    gm = float(np.exp(np.log(y).mean()))
    lams = np.linspace(-2.0, 2.0, 401) if grid is None else np.asarray(grid)

    def llf(lam):
        z = np.log(y) * gm if abs(lam) < 1e-12 else (y ** lam - 1) / (lam * gm ** (lam - 1))
        r = sm.OLS(z, X).fit()
        return -n / 2 * np.log(r.ssr / n)

    ll = np.array([llf(l_) for l_ in lams])
    keep = lams[ll >= ll.max() - stats.chi2.ppf(level, 1) / 2]
    return {"lambda": float(lams[ll.argmax()]), "lo": float(keep.min()), "hi": float(keep.max()),
            "ll_log": float(llf(0.0) - ll.max()), "ll_raw": float(llf(1.0) - ll.max())}


def log_supported(df: pd.DataFrame, resp: str, factors: Sequence[str], terms: Sequence[str]) -> bool:
    """True when the response is positive and the Box-Cox interval contains 0 and excludes 1: the
    data support the log scale and reject the raw one."""
    d = df[df[resp].notna()]
    if not (d[resp] > 0).all():
        return False
    b = boxcox_interval(d, resp, factors, terms)
    return b["lo"] <= 0.0 <= b["hi"] and not (b["lo"] <= 1.0 <= b["hi"])


# --------------------------------------------------------------------------------------
# Model selection: the analysis INV-002 corrective action CA3 applies to every response-surface output
# --------------------------------------------------------------------------------------
def hierarchical_subsets(factors: Sequence[str], quad: bool = True) -> List[List[str]]:
    """Every submodel of the full quadratic that obeys strong hierarchy: an interaction only with
    both its main effects, a square only with its main effect. Simplest first, in a fixed order."""
    out = []
    for r in range(len(factors) + 1):
        for main in itertools.combinations(factors, r):
            extra = [f"{a}:{b}" for a, b in itertools.combinations(main, 2)]
            extra += [f"{f}^2" for f in main] if quad else []
            for k in range(len(extra) + 1):
                for e in itertools.combinations(extra, k):
                    out.append(list(main) + list(e))
    return out


def aicc(y: np.ndarray, X: np.ndarray) -> float:
    """Akaike's information criterion with the small-sample correction, for an OLS fit (the
    residual variance counted as a parameter)."""
    m = sm.OLS(y, X).fit()
    k, n = X.shape[1] + 1, len(y)
    return float(m.aic + 2 * k * (k + 1) / (n - k - 1)) if n - k - 1 > 0 else float("inf")


#: SSE / SST below which a fit is exact: the data carry no error at the precision reported
EXACT_TOL = 1e-12


def select_model(df: pd.DataFrame, resp: str, factors: Sequence[str], thresholds: Dict[str, float],
                 block: Optional[bool] = None, transform: bool = True) -> Dict[str, object]:
    """The model of one response-surface output, as INV-002 CA3 analyses it.

    1. The scale: the Box-Cox profile of the full quadratic. The log scale where its 95 % interval
       contains 0 and excludes 1 (the response must be positive), else the raw scale.
    2. The model: the hierarchical submodel of the full quadratic with the lowest AICc, by
       exhaustive search (stepwise search can stop at a worse model); a block term is kept.
    3. The check: the selected model against PCMP-001 §7.2. ``adequate`` also requires a
       significant model F-test when the model has terms; a model with no term says the output
       does not depend on the parameters within the range studied.
    An output whose results the full quadratic reproduces exactly (identical replicates, no residual)
    is fitted exactly by several models; the smallest of them is taken, ``exact`` is True and AICc is
    not defined (NaN). Such a model is never ``adequate``: with no residual there is no pure error for
    the lack-of-fit test and no residual mean square for the model F-test, so PCMP-001 §7.2 cannot be
    applied, and its prediction interval has zero width. The output is judged on its measured
    results, and it cannot widen a criterion (INV-002 review run 2; owner, 2026-10-09). No Box-Cox
    interval is computed for it: the profile likelihood is unbounded when every λ fits exactly.
    Returns the ``adequacy`` dict of the selected model with ``scale``, ``ycol``, ``boxcox``,
    ``aicc``, ``aicc_full``, ``exact`` and the data (``data``) it was fitted to."""
    d = df[df[resp].notna()].reset_index(drop=True)
    blk = has_blocks(d) if block is None else block
    scale, ycol, bc = "raw", resp, None
    y0 = d[resp].to_numpy(float)
    X0 = matrix(d, full_terms(factors), blk).to_numpy()
    sst0 = float(((y0 - y0.mean()) ** 2).sum())
    exact_raw = sst0 > 0 and float(((y0 - X0 @ np.linalg.lstsq(X0, y0, rcond=None)[0]) ** 2).sum()) / sst0 < EXACT_TOL
    if transform and not exact_raw and (d[resp] > 0).all():
        bc = boxcox_interval(d, resp, factors, full_terms(factors))
        if bc["lo"] <= 0.0 <= bc["hi"] and not (bc["lo"] <= 1.0 <= bc["hi"]):
            scale, ycol = "log", f"ln_{resp}"
            d = d.assign(**{ycol: np.log(d[resp].to_numpy(float))})
    y = d[ycol].to_numpy(float)
    X = matrix(d, full_terms(factors), blk)
    sst = float(((y - y.mean()) ** 2).sum())

    def rel_sse(cols):
        r = np.linalg.lstsq(X[cols].to_numpy(), y, rcond=None)[0]
        return float(((y - X[cols].to_numpy() @ r) ** 2).sum()) / sst if sst > 0 else 0.0

    # An output the data give without error (every replicate identical to the precision the method
    # reports) is fitted exactly by more than one model, and AICc, whose log SSE is then rounding
    # noise, cannot choose among them. The smallest model that fits exactly is taken instead.
    exact = sst > 0 and rel_sse(list(X.columns)) < EXACT_TOL
    best = None
    for terms in hierarchical_subsets(factors):
        cols = ["const"] + terms + ([BLOCK] if blk else [])
        if exact:
            if rel_sse(cols) < EXACT_TOL and (best is None or len(terms) < len(best[1])):
                best = (float("nan"), terms)
            continue
        a = aicc(y, X[cols].to_numpy())
        if best is None or a < best[0] - 1e-9:
            best = (a, terms)
    order = full_terms(factors)
    terms = [t for t in order if t in best[1]]
    fit = adequacy(d, ycol, factors, terms, thresholds, blk)
    if terms and not fit["f_ok"]:
        fit["adequate"] = False
    if exact:
        # §7.2 cannot be applied to a model with no residual (see the docstring)
        fit["adequate"] = False
    fit.update(scale=scale, ycol=ycol, boxcox=bc, aicc=best[0], exact=exact,
               aicc_full=float("nan") if exact else aicc(y, X.to_numpy()), data=d)
    return fit


def stepwise_aicc(df: pd.DataFrame, ycol: str, factors: Sequence[str], block: bool,
                  direction: str) -> Dict[str, object]:
    """A stepwise search by AICc under strong hierarchy, for comparison with the exhaustive search
    of :func:`select_model` (INV-002 explains why CA3 searches exhaustively). ``backward`` starts
    from the full quadratic and removes, at each step, the removable term (one no remaining term
    contains) whose removal lowers AICc most; ``forward`` starts from the mean and adds, at each step,
    the term whose parents are all present and whose addition lowers AICc most. Each stops when no
    single change lowers AICc. A block term is always kept. Returns {"aicc", "terms"}."""
    full = full_terms(factors)
    X = matrix(df, full, block)
    y = df[ycol].to_numpy(float)

    def score(terms):
        return aicc(y, X[["const"] + list(terms) + ([BLOCK] if block else [])].to_numpy())

    def hierarchical(terms):
        return all(set(parents(t)) <= set(terms) for t in terms)
    cur = list(full) if direction == "backward" else []
    best = score(cur)
    while True:
        if direction == "backward":
            cands = [[x for x in cur if x != t] for t in cur]
        else:
            cands = [cur + [t] for t in full if t not in cur]
        moves = [(score(c), c) for c in cands if hierarchical(c)]
        if not moves:
            break
        s, c = min(moves, key=lambda m: m[0])
        if s < best - 1e-9:
            best, cur = s, c
        else:
            break
    return {"aicc": float(best), "terms": [t for t in full if t in cur]}


# --------------------------------------------------------------------------------------
# Small-scale verification runs: how many (PCR-006, PD-006-02)
# --------------------------------------------------------------------------------------
def verification_runs(f_data: float, f_req: float, sigma: float, n_max: int, power: float,
                      reps: int, rng: np.random.Generator, alpha: float = 0.05) -> Dict[str, object]:
    """Simulation of a verification of a clearance fold. Each run gives a log fold
    ln f ~ N(ln f_true, sigma²). The verification passes when the one-sided (1 - alpha) lower
    confidence bound of the mean log fold, with sigma known from the earlier data, is at least
    ln f_req. By construction a true fold equal to f_req passes with probability alpha. Returns, for
    n = 1 … n_max + 2, the probability of passing when the true fold is the one the data show
    (``f_data``) and when it equals the required fold, and the smallest n <= n_max reaching
    ``power`` (None when none does)."""
    z = stats.norm.ppf(1 - alpha)
    rows, n_req = [], None
    for n in range(1, n_max + 3):
        out = {}
        for lab, ft in (("data", f_data), ("required", f_req)):
            y = rng.normal(np.log(ft), sigma, (reps, n)).mean(axis=1)
            out[lab] = float((y - z * sigma / np.sqrt(n) >= np.log(f_req)).mean())
        rows.append({"n": n, "p_pass_at_data": out["data"], "p_pass_at_required": out["required"]})
        if n_req is None and n <= n_max and out["data"] >= power:
            n_req = n
    return {"grid": rows, "n": n_req}
