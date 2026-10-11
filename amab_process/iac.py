"""Intermediate acceptance criteria (Rev 2.0), the Rev 1.0 criteria they replace, and the checks
that keep the new ones honest.

The rule (PCMP-001 Rev 2.0, config ``iac:``) is the specification-driven one. A drug-substance
criterion is carried BACKWARD through the train, one step at a time, using the WORST CASE each
downstream step has shown on the platform (the prior products X-Mab, Y-Mab and Z-Mab): its
lowest clearance fold and its largest increase. Going backward through step j,

    limit entering j  =  (limit leaving j  -  largest increase at j)  x  lowest clearance fold at j

and the criterion for a step's OUTPUT is the limit entering the next step. Attributes no
downstream step changes keep the drug-substance criterion. Viral clearance is held to the
platform claim of each step, and the claims sum to the cumulative requirement.

:func:`derive` takes the configuration and nothing else. That is the whole point: a criterion
that could read ``outputs/`` could be fitted to the data it judges, which is exactly what
INV-001 found in Rev 1.0 (``tests/test_iac.py`` holds it to this).
"""
from __future__ import annotations

from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from .config import Config

#: step response -> drug-substance attribute key
RESP_TO_CQA = {
    "pool_hcp_ng_mg": "hcp", "hcp_out_ng_mg": "hcp",
    "aggregate_out_pct": "aggregates_hmw", "aggregates_hmw": "aggregates_hmw",
    "leached_protein_a_ppm": "leached_protein_a",
    "lmw_cesds_pct": "fragments_lmw",
    "xmulv_lrf": "lrv_xmulv", "mvm_lrf": "lrv_mvm",
    "afucosylation": "afucosylation", "galactosylation": "galactosylation",
    "high_mannose": "high_mannose", "acidic_variants": "acidic_variants",
}


def _order(cfg: Config) -> List[str]:
    return list(cfg.train_order)


def _ds(cfg: Config, cqa: str):
    c = cfg.cqa(cqa)
    return float(c["acceptance"][0]), float(c["acceptance"][1])


def _platform(cfg: Config, step: str, cqa: str) -> dict:
    return ((cfg.raw()["iac"]["platform"].get(step) or {}).get(cqa) or {})


def limit_leaving(cfg: Config, step: str, cqa: str,
                  tighten: Optional[Dict] = None) -> Dict[str, float]:
    """The criterion on the OUTPUT of ``step`` for attribute ``cqa``, with its derivation.

    Returns ``{"low", "high", "fold", "added"}``: the bounds, and the product of the downstream
    worst-case folds and the sum of the downstream worst-case increases that produced them."""
    lo, hi = _ds(cfg, cqa)
    order = _order(cfg)
    fold, added = 1.0, 0.0
    for j in reversed(order[order.index(step) + 1:]):
        p = dict(_platform(cfg, j, cqa))
        p.update((tighten or {}).get((j, cqa), {}))
        a = float(p.get("add_max", 0.0))
        f = float(p.get("fold_min", 1.0))
        hi = (hi - a) * f
        fold *= f
        added += a
        # a floor is carried back by the SMALLEST increase, which on the platform is none
        lo = lo * f if lo > 0 else lo
    return {"low": lo, "high": hi, "fold": fold, "added": added}


def viral_claim(cfg: Config, step: str, resp: str) -> Optional[float]:
    return (cfg.raw()["iac"]["viral_claims"].get(step) or {}).get(resp)


def derive(cfg: Config, tighten: Optional[Dict] = None) -> pd.DataFrame:
    """The full IAC table. Reads the configuration only, plus, through :func:`final`, the
    tightening that verification may impose (never a loosening)."""
    rows = []
    for step, resps in cfg.raw()["iac"]["responses"].items():
        uo = cfg.unit_op(step)
        for resp in resps:
            cqa = RESP_TO_CQA[resp]
            c = cfg.cqa(cqa)
            claim = viral_claim(cfg, step, resp)
            if claim is not None:
                rows.append({"step": uo.step, "step_key": step, "response": resp, "cqa": cqa,
                             "ds_low": c["acceptance"][0], "ds_high": c["acceptance"][1],
                             "spec_type": "lower", "downstream_fold": np.nan,
                             "downstream_added": np.nan, "iac_low": float(claim),
                             "iac_high": np.inf, "basis": "platform claim"})
                continue
            d = limit_leaving(cfg, step, cqa, tighten)
            changed = d["fold"] != 1.0 or d["added"] != 0.0
            two = cqa in ("afucosylation", "galactosylation", "high_mannose", "acidic_variants")
            rows.append({"step": uo.step, "step_key": step, "response": resp, "cqa": cqa,
                         "ds_low": c["acceptance"][0], "ds_high": c["acceptance"][1],
                         "spec_type": "two_sided" if two else "upper",
                         "downstream_fold": d["fold"], "downstream_added": d["added"],
                         "iac_low": d["low"] if two else 0.0, "iac_high": d["high"],
                         "basis": "back-calculated" if changed else "drug substance"})
    return pd.DataFrame(rows)


def cumulative_claims(cfg: Config) -> pd.DataFrame:
    """Sum of the per-step platform claims against the cumulative requirement."""
    rows = []
    for resp, cqa in (("xmulv_lrf", "lrv_xmulv"), ("mvm_lrf", "lrv_mvm")):
        claimed = sum(float(v[resp]) for v in cfg.raw()["iac"]["viral_claims"].values() if resp in v)
        rows.append({"cqa": cqa, "claimed_sum": claimed, "required": _ds(cfg, cqa)[0],
                     "met": claimed >= _ds(cfg, cqa)[0]})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------------------
# Verification: did this campaign's studies show the worst case the criteria assumed?
# --------------------------------------------------------------------------------------
#: the one-sided confidence of the bound that may replace a platform worst case (PCMP-001 §7.5): the
#: upper end of a two-sided interval at 2 x (1 - BOUND_CONFIDENCE)
BOUND_CONFIDENCE = 0.95


def sdm_offset(cfg: Config, sdm: Optional[pd.DataFrame], step: str, col: str, log: bool):
    """The scale-down offset of one output at its point estimate, as the verification applies it
    (PCMP-001 §7.1 rule 2; owner, 2026-10-11): ``("ratio", r)`` for an output modelled on the log
    scale, the ratio of the geometric means, or ``("difference", d)``, the difference of the means,
    scale-down minus manufacturing scale, from ``sdm_qualification.csv``. The same estimate as
    ``doe_report.sdm_offset`` at its point. None when the output has no qualification data (fragments,
    viral clearance) or the config switches offsets off (``analytics.sdm.apply_offset``)."""
    if sdm is None or not cfg.raw()["analytics"]["sdm"].get("apply_offset", False):
        return None
    d = sdm[sdm["step"] == step]
    if col not in d.columns:
        return None
    a = d.loc[d["scale"] == "scale-down", col].dropna().to_numpy(float)
    b = d.loc[d["scale"] == "manufacturing", col].dropna().to_numpy(float)
    if len(a) < 2 or len(b) < 2:
        return None
    if log:
        return "ratio", float(np.exp(np.log(a).mean() - np.log(b).mean()))
    return "difference", float(a.mean() - b.mean())


def to_mfg(off, y):
    """A scale-down value at manufacturing scale: divided by a ratio offset (on the log scale, the
    log ratio subtracted), minus a difference offset, unchanged with no offset. As
    ``doe_report.to_mfg``."""
    y = np.asarray(y, dtype=float)
    if off is None:
        return y
    kind, v = off
    return y / v if kind == "ratio" else y - v


def _nor_worst(cfg: Config, step: str, df: pd.DataFrame, col: str, feed: float, mode: str,
               form: str = "selected", bound: str = "batch", sdm: Optional[pd.DataFrame] = None):
    """Worst predicted fold (mode 'fold') or increase (mode 'add') over the NOR box of the step's
    response-surface factors, from the model INV-002 corrective action CA3 selects for the output
    (``adequacy.select_model``: Box-Cox scale, AICc over the hierarchical submodels of the full
    quadratic), evaluated at every combination of NOR low, set-point and NOR high, and the same
    worst case at its one-sided 95 % confidence bound. ``form="full"`` uses the full quadratic on
    the raw scale instead, the model the plans prescribe: the verification as it would have been
    without CA3, which INV-002 compares with the one in force (CA3 was adopted before INV-001
    closed, so the criteria fixed at that closure rest on the selected models).

    The fold and the increase are computed at manufacturing scale (PCMP-001 §7.1 rule 2; owner,
    2026-10-11): the feed is a manufacturing-scale value of the process model, so the scale-down
    prediction of the pool, and its bound, are converted by the step's offset at its point estimate
    (:func:`sdm_offset`, on the scale of the model) before they are compared with it. So are the
    measured results behind ``edge``. Returns (edge, worst, bound, adequacy, offset)."""
    import itertools
    from . import adequacy as ad
    from .studies import RSM_TOP, DOE_FACTORS
    fac = [f for f in RSM_TOP.get(step, DOE_FACTORS[step][:4]) if f"coded_{f}" in df]
    th = {k: float(v) for k, v in cfg.raw()["campaign"]["thresholds"].items()}
    if form == "full":
        sel = {**ad.adequacy(df, col, fac, ad.full_terms(fac), th), "scale": "raw"}
    else:
        sel = ad.select_model(df, col, fac, th)
    off = sdm_offset(cfg, sdm, step, col, sel["scale"] == "log")
    meas = to_mfg(off, df[col].to_numpy(float))
    edge = float((feed / meas).min()) if mode == "fold" else float((meas - feed).max())
    uo = cfg.unit_op(step)
    pts = []
    # the NOR as characterized: the criteria were fixed at INV-001 closure, before any report
    # narrowed a NOR, so no later NOR decision moves them
    for combo in itertools.product(*[[uo.param(f).nor_characterized[0], uo.param(f).setpoint_characterized,
                                      uo.param(f).nor_characterized[1]] for f in fac]):
        pts.append({"coded_" + f: (v - sum(uo.param(f).prange) / 2) / ((uo.param(f).prange[1] - uo.param(f).prange[0]) / 2)
                    for f, v in zip(fac, combo)})
    # a design with an augmentation block is predicted at block 0, the average of the two blocks
    P = pd.DataFrame(pts)
    blk = bool(sel.get("block", False))
    X = ad.matrix(P.assign(**{ad.BLOCK: 1}) if blk else P, sel["terms"], blk)
    if blk:
        X[ad.BLOCK] = 0.0
    X = X.to_numpy()
    back = np.exp if sel["scale"] == "log" else (lambda v: v)
    # the upper confidence limit of the output where a high output is bad (a fold computed from it
    # is a lower bound on the clearance), or the upper limit of the increase; one-sided 95 %: the
    # upper limit of the two-sided 90 % interval, on the scale of the model, back-transformed
    # bound="batch": the one-sided prediction bound of a single batch, the rule in force (owner,
    # 2026-10-09; PCMP-001 §7.5); bound="mean": the confidence bound of the mean output, the rule as
    # first set on 2026-10-08, kept for comparison only
    ci = sel["model"].get_prediction(X).summary_frame(alpha=2 * (1 - BOUND_CONFIDENCE))
    y = to_mfg(off, back(ci["mean"].to_numpy()))
    up = to_mfg(off, back(ci["mean_ci_upper" if bound == "mean" else "obs_ci_upper"].to_numpy()))
    worst = float((feed / y).min()) if mode == "fold" else float((y - feed).max())
    bound = float((feed / up).min()) if mode == "fold" else float((up - feed).max())
    adq = {"r2_gap": sel["gap"], "p_lof": sel["p_lof"], "adequate": bool(sel["adequate"])}
    return edge, worst, bound, adq, off


def _univariate_increase(cfg: Config, step: str, uni: pd.DataFrame, study: str, col: str,
                         sdm: Optional[pd.DataFrame], bound: str = "batch"):
    """The largest increase of an output across the NOR of a step studied one factor at a time
    (UF/DF aggregate; owner, 2026-10-11). An ordinary least squares fit of the output, at
    manufacturing scale (difference offset at its point estimate), on the main effects of the factors
    of the univariate study ``study``, all runs pooled (each run carries the set-point of the factors
    it did not vary). The increase is the one-sided 95 % prediction bound of a single run at the least
    favourable combination of NOR low, set-point and NOR high of the factors, minus the fitted mean
    at the set-point; a factor with a one-sided NOR (``nor_one_sided: low``) takes its NOR high as the
    upper edge of the combination. ``edge`` is the largest measured result minus that fitted mean.
    Returns (edge, worst, bound, adequacy, offset) as :func:`_nor_worst`."""
    import itertools
    from . import adequacy as ad
    th = {k: float(v) for k, v in cfg.raw()["campaign"]["thresholds"].items()}
    uo = cfg.unit_op(step)
    d = uni[(uni["study"] == study) & uni[col].notna()].copy()
    fac = list(dict.fromkeys(d["parameter"]))
    off = sdm_offset(cfg, sdm, step, col, log=False)
    d[col] = to_mfg(off, d[col].to_numpy(float))

    def coded(f, v):
        lo, hi = uo.param(f).prange
        return (np.asarray(v, dtype=float) - (lo + hi) / 2) / ((hi - lo) / 2)
    for f in fac:
        nat = np.where(d["parameter"] == f, d["value"].to_numpy(float), uo.param(f).setpoint_characterized)
        d["coded_" + f] = coded(f, nat)
    a = ad.adequacy(d.reset_index(drop=True), col, fac, fac, th, block=False)
    # the NOR as characterized, as for the response-surface steps
    combos = list(itertools.product(*[[uo.param(f).nor_characterized[0], uo.param(f).setpoint_characterized,
                                       uo.param(f).nor_characterized[1]] for f in fac]))
    P = pd.DataFrame([{"coded_" + f: float(coded(f, v)) for f, v in zip(fac, c)} for c in combos])
    S = pd.DataFrame([{"coded_" + f: float(coded(f, uo.param(f).setpoint_characterized)) for f in fac}])
    m = a["model"]
    ci = m.get_prediction(ad.matrix(P, fac).to_numpy()).summary_frame(alpha=2 * (1 - BOUND_CONFIDENCE))
    ref = float(m.predict(ad.matrix(S, fac).to_numpy())[0])
    up = ci["mean_ci_upper" if bound == "mean" else "obs_ci_upper"].to_numpy()
    edge = float(d[col].max() - ref)
    worst = float(ci["mean"].max() - ref)
    bnd = float(up.max() - ref)
    adq = {"r2_gap": a["gap"], "p_lof": a["p_lof"], "adequate": bool(a["adequate"])}
    return edge, worst, bnd, adq, off


def _adequacy(cfg: Config, model, df: pd.DataFrame, col: str) -> Dict[str, float]:
    """The model-adequacy tests of PCMP-001 (campaign thresholds): R² minus predicted R² (PRESS)
    within ``max_r2_minus_pred_r2``, and no significant lack of fit against the centre-point pure
    error at ``lof_alpha``. A widening must rest on a model that passes both."""
    from scipy import stats as sst
    th = cfg.raw()["campaign"]["thresholds"]
    y = df[col].to_numpy(float)
    h = model.get_influence().hat_matrix_diag
    press = float(np.sum((model.resid.to_numpy() / (1 - h)) ** 2))
    sst_ = float(np.sum((y - y.mean()) ** 2))
    pred_r2 = 1 - press / sst_ if sst_ > 0 else float("nan")
    gap = float(model.rsquared - pred_r2)
    p_lof = float("nan")
    if "run_type" in df:
        cen = df.loc[df["run_type"] == "center", col].to_numpy(float)
        df_pe = len(cen) - 1
        ss_pe = float(((cen - cen.mean()) ** 2).sum()) if len(cen) else 0.0
        df_lof = int(model.df_resid) - df_pe
        ss_lof = max(float((model.resid ** 2).sum()) - ss_pe, 0.0)
        if df_pe > 0 and df_lof > 0 and ss_pe > 0:
            p_lof = float(sst.f.sf((ss_lof / df_lof) / (ss_pe / df_pe), df_lof, df_pe))
    ok = gap <= float(th["max_r2_minus_pred_r2"]) and not (p_lof < float(th["lof_alpha"]))
    return {"r2_gap": gap, "p_lof": p_lof, "adequate": bool(ok)}


def verification(cfg: Config, data: Dict[str, pd.DataFrame], ps: pd.DataFrame,
                 frag_nominal: Dict[str, float], vi_feed_acidic: float,
                 form: str = "selected", bound: str = "batch", *, sdm: pd.DataFrame,
                 uni: pd.DataFrame) -> pd.DataFrame:
    """For every platform worst case the IACs rely on, what THIS campaign showed for that step.

    Two numbers. ``observed_edge`` is the worst value among the response-surface runs, which sit
    at the characterization edges and beyond the NOR. ``predicted_nor`` is the worst value the
    fitted response-surface model predicts anywhere in the NOR box, which is the region routine
    manufacture runs in and so the one the criteria have to hold for. ``met`` is judged on
    ``predicted_nor``. A platform worst case that is not met is replaced, in :func:`final`, by
    the A-Mab value, which can only tighten the criterion. ``form`` is passed to
    :func:`_nor_worst`: the selected models by default, ``"full"`` for the verification on the full
    quadratic models the plans prescribe, as it would have been without INV-002 corrective action
    CA3.

    Every fold and increase is computed at manufacturing scale, the scale-down results converted by
    the step's offset from ``sdm`` (``sdm_qualification.csv``; PCMP-001 §7.1 rule 2, owner,
    2026-10-11). ``offset`` and ``offset_scale`` record what was applied. A platform entry with a
    ``verify`` block names a univariate study in ``uni`` (``univariate_studies.csv``) instead of a
    response-surface design (UF/DF aggregate, :func:`_univariate_increase`)."""
    pss = ps.set_index("step")
    vi_in_agg = float(pss.loc[6, "aggregate_out_pct"] - pss.loc[6, "aggregate_delta_pct"])
    feeds = {
        ("cex", "hcp"): (float(pss.loc[5, "pool_hcp_ng_mg"]), "hcp_out_ng_mg", "fold"),
        ("cex", "aggregates_hmw"): (float(pss.loc[6, "aggregate_out_pct"]), "aggregate_out_pct", "fold"),
        ("cex", "fragments_lmw"): (frag_nominal["viral_inactivation"], "lmw_cesds_pct", "fold"),
        ("aex", "hcp"): (float(pss.loc[7, "hcp_out_ng_mg"]), "hcp_out_ng_mg", "fold"),
        ("viral_inactivation", "aggregates_hmw"): (vi_in_agg, "aggregate_out_pct", "add"),
        ("viral_inactivation", "fragments_lmw"): (frag_nominal["protein_a"], "lmw_cesds_pct", "add"),
        ("viral_inactivation", "acidic_variants"): (float(vi_feed_acidic), "acidic_variants", "add"),
    }
    rows = []
    for step, attrs in cfg.raw()["iac"]["platform"].items():
        for cqa, p in attrs.items():
            kind = "fold_min" if "fold_min" in p else "add_max"
            assumed = float(p[kind])
            edge = nor = nor_bound = off = None
            adq = {"r2_gap": None, "p_lof": None, "adequate": None}
            if "verify" in p:
                v = p["verify"]
                edge, nor, nor_bound, adq, off = _univariate_increase(cfg, step, uni, v["study"],
                                                                      v["response"], sdm, bound)
            elif (step, cqa) in feeds and step in data:
                feed, col, mode = feeds[(step, cqa)]
                df = data[step]
                if col in df and df[col].notna().all():
                    edge, nor, nor_bound, adq, off = _nor_worst(cfg, step, df, col, feed, mode, form,
                                                                bound, sdm)
            met = None if nor is None else (nor >= assumed if kind == "fold_min" else nor <= assumed)
            # widening (owner's decision 2026-10-08): allowed only where the A-Mab worst case beats
            # the platform value even at its 95 % confidence bound
            # ... and only on a model that passes the adequacy tests of PCMP-001: a widening needs
            # good arguments, and a model that fails them is not one (PCR-005 review, 2026-10-08).
            # Tightening needs no such test: a worse prediction is a warning even from a weak model.
            better = None if nor is None else (
                (nor_bound > assumed if kind == "fold_min" else nor_bound < assumed) and bool(adq["adequate"]))
            rows.append({"step": cfg.unit_op(step).step, "step_key": step, "cqa": cqa,
                         "assumption": kind, "assumed": assumed, "observed_edge": edge,
                         "predicted_nor": nor, "predicted_nor_bound95": nor_bound if nor is not None else None,
                         "met": met, "widening_supported": better, "model_adequate": adq["adequate"],
                         "r2_minus_pred_r2": adq["r2_gap"], "p_lack_of_fit": adq["p_lof"],
                         "offset_scale": off[0] if off else None, "offset": off[1] if off else None,
                         "source": p.get("source", "")})
    return pd.DataFrame(rows)


def final(cfg: Config, ver: pd.DataFrame) -> pd.DataFrame:
    """The criteria in force: the a-priori table, tightened wherever verification showed a step
    doing worse within its NOR than the platform worst case assumed, and widened only where the 95 %
    confidence bound of the A-Mab worst case beats the platform value and ``allow_widening`` is on.

    Both directions use the 95 % confidence bound, never the point prediction: a step that does
    worse is replaced by the bound, which is worse still, and a step that does better is credited
    only with its bound. A criterion upstream of two changed steps can be both tightened by one and
    widened by the other; ``tightened`` and ``widened`` say which changes reached it, and the value
    is the net of both."""
    tight, wide = {}, {}
    for _, r in ver[ver["met"] == False].iterrows():  # noqa: E712  (None stays unverified)
        tight[(r["step_key"], r["cqa"])] = {r["assumption"]: float(r["predicted_nor_bound95"])}
    # Widening (owner's decision 2026-10-08: "if the data supports it, a criterion could be
    # widened, but it needs good arguments"). The report argues each one.
    if "widening_supported" in ver.columns and cfg.raw()["iac"].get("allow_widening", False):
        for _, r in ver[ver["widening_supported"] == True].iterrows():  # noqa: E712
            wide[(r["step_key"], r["cqa"])] = {r["assumption"]: float(r["predicted_nor_bound95"])}
    a = derive(cfg)
    f = derive(cfg, {**tight, **wide})
    ft, fw = derive(cfg, tight), derive(cfg, wide)
    a["iac_low_apriori"], a["iac_high_apriori"] = a["iac_low"], a["iac_high"]
    a["iac_low"], a["iac_high"] = f["iac_low"], f["iac_high"]
    a["tightened"] = (ft["iac_high"] < a["iac_high_apriori"]) | (ft["iac_low"] > a["iac_low_apriori"])
    a["widened"] = (fw["iac_high"] > a["iac_high_apriori"]) | (fw["iac_low"] < a["iac_low_apriori"])
    # the derivation columns of a changed row show the values that replaced the platform worst
    # cases, so the criterion can be recomputed from its own row
    ch = a["tightened"] | a["widened"]
    a.loc[ch, "downstream_fold"] = f.loc[ch, "downstream_fold"]
    a.loc[ch, "downstream_added"] = f.loc[ch, "downstream_added"]
    a.loc[a["tightened"] & ~a["widened"], "basis"] = "back-calculated, tightened on verification"
    a.loc[a["widened"] & ~a["tightened"], "basis"] = "back-calculated, widened on verification"
    a.loc[a["widened"] & a["tightened"], "basis"] = "back-calculated, tightened and widened on verification"
    return a


# --------------------------------------------------------------------------------------
# Rev 1.0 criteria, recomputed exactly as Rev 1.0 computed them, kept as data for INV-001
# --------------------------------------------------------------------------------------
def rev1_criteria(cfg: Config, ps: pd.DataFrame, cap: pd.DataFrame, vc: pd.DataFrame) -> pd.DataFrame:
    """The in-process limits Rev 1.0 applied (config ``rev1_ipc_limits``), with the rule and the
    margin each used. Reproduces doe_report.ipc_limit as it stood at tag corpus-rev1.0."""
    r1 = cfg.raw()["rev1_ipc_limits"]
    pss = ps.set_index("step")
    capk = cap.set_index("key")
    rows = []
    viral_row = {"viral_inactivation": "Low-pH Viral Inactivation", "aex": "Anion Exchange (AEX)",
                 "virus_filtration": "Virus Filtration"}
    vcol = {"xmulv_lrf": ("XMuLV", "lrv_xmulv"), "mvm_lrf": ("MVM", "lrv_mvm")}
    for step, ents in r1["steps"].items():
        uo = cfg.unit_op(step)
        for resp, ent in ents.items():
            cqa = RESP_TO_CQA[resp]
            lo_ds, hi_ds = _ds(cfg, cqa)
            if "from_capability" in ent:
                row = capk.loc[ent["from_capability"]]
                val = float(row["mean"]) + float(r1["capability_alert_sigma"]) * float(row["sd"])
                rule, margin = f"mean + {r1['capability_alert_sigma']} sd of capability", np.nan
                # Version 1.0 judged acidic variants against the ceiling only (INV-001 finding
                # 4); the glycans kept their drug-substance floor
                lo, hi = (0.0 if cqa == "acidic_variants" else lo_ds), val
            elif "from_ds_backcalc" in ent:
                spec = ent["from_ds_backcalc"]
                down = pss[pss.index > uo.step]
                fold = float(down[spec["clearance_column"]].dropna().prod()) if spec["clearance_column"] in down else 1.0
                ceiling = hi_ds * (fold if fold > 0 else 1.0)
                inc = spec.get("increase_column")
                if inc and inc in down.columns:
                    ceiling -= float(down[inc].dropna().sum())
                margin = float(spec.get("margin", 1.0))
                rule = "nominal back-calculation / margin"
                lo, hi = 0.0, ceiling / margin
            elif "from_modular_claim" in ent:
                col, _ = vcol[resp]
                claim = float(vc[vc["step"] == viral_row[step]].iloc[0][col])
                rule, margin = f"nominal claim less {r1['viral_assay_allowance']} log10 for assay variability", np.nan
                lo, hi = claim - float(r1["viral_assay_allowance"]), np.inf
            else:
                continue
            rows.append({"step": uo.step, "step_key": step, "response": resp, "cqa": cqa,
                         "rule": rule, "margin": margin, "low": lo, "high": hi})
    # viral criteria Rev 1.0 took from the modular back-calculation in acceptance_for
    for step, resps in (("viral_inactivation", ["xmulv_lrf"]), ("aex", ["xmulv_lrf", "mvm_lrf"])):
        for resp in resps:
            col, cqa = vcol[resp]
            cum = float(vc[vc["step"] == "Cumulative"].iloc[0][col])
            stepv = float(vc[vc["step"] == viral_row[step]].iloc[0][col])
            rows.append({"step": cfg.unit_op(step).step, "step_key": step, "response": resp,
                         "cqa": cqa, "rule": "requirement - nominal of other steps",
                         "margin": np.nan, "low": max(_ds(cfg, cqa)[0] - (cum - stepv), 0.0),
                         "high": np.inf})
    return pd.DataFrame(rows).sort_values(["step", "response"]).reset_index(drop=True)


# --------------------------------------------------------------------------------------
# Integrated process model: probability of an out-of-specification drug substance
# --------------------------------------------------------------------------------------
def p_oos(cfg: Config, mc: pd.DataFrame) -> pd.DataFrame:
    """P(OOS) per drug-substance attribute from the Monte-Carlo integrated model.

    Two numbers, because a few thousand simulated batches cannot resolve a rare event: the
    observed count outside the criterion, and the normal-tail probability from the simulated
    mean and standard deviation (one- or two-sided as the criterion is)."""
    from math import erf, sqrt
    from .studies import spec_type

    def tail(z):
        return 0.5 * (1 - erf(z / sqrt(2)))

    rows = []
    for c in cfg.cqas:
        k = c["key"]
        if k not in mc.columns:
            continue
        x = mc[k].to_numpy(dtype=float)
        lo, hi = c["acceptance"]
        mu, sd = float(x.mean()), float(x.std(ddof=1))
        st = spec_type(k)
        out = ((x < lo) if st == "lower" else (x > hi) if st == "upper" else ((x < lo) | (x > hi)))
        p_lo = tail((mu - lo) / sd) if st in ("lower", "two_sided") and sd > 0 else 0.0
        p_hi = tail((hi - mu) / sd) if st in ("upper", "two_sided") and sd > 0 else 0.0
        rows.append({"cqa": c["name"], "key": k, "spec_type": st, "n": len(x),
                     "n_oos": int(out.sum()), "p_oos_normal": p_lo + p_hi,
                     "ppm_normal": (p_lo + p_hi) * 1e6})
    return pd.DataFrame(rows)
