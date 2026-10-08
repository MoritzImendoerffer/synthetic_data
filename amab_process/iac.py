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
def _nor_worst(cfg: Config, step: str, df: pd.DataFrame, col: str, feed: float, mode: str):
    """Worst predicted fold (mode 'fold') or increase (mode 'add') over the NOR box of the step's
    response-surface factors: the quadratic RSM model evaluated at every combination of NOR low,
    set-point and NOR high."""
    import itertools
    from .studies import RSM_TOP, DOE_FACTORS, fit_effects
    fac = [f for f in RSM_TOP.get(step, DOE_FACTORS[step][:4]) if f"coded_{f}" in df]
    model = fit_effects(df, col, fac, quadratic=True)["model"]
    uo = cfg.unit_op(step)
    pts = []
    for combo in itertools.product(*[[uo.param(f).nor[0], uo.param(f).setpoint, uo.param(f).nor[1]] for f in fac]):
        pts.append({f: (v - sum(uo.param(f).prange) / 2) / ((uo.param(f).prange[1] - uo.param(f).prange[0]) / 2)
                    for f, v in zip(fac, combo)})
    X = pd.DataFrame(pts)
    y = np.asarray(model.predict(X))
    worst = float((feed / y).min()) if mode == "fold" else float((y - feed).max())
    # the same worst case at 95 % confidence: the upper confidence limit of the output where a
    # high output is bad (a fold computed from it is a lower bound on the clearance), or the
    # upper limit of the increase
    ci = model.get_prediction(X).summary_frame(alpha=0.05)
    up = ci["mean_ci_upper"].to_numpy()
    bound = float((feed / up).min()) if mode == "fold" else float((up - feed).max())
    return worst, bound


def verification(cfg: Config, data: Dict[str, pd.DataFrame], ps: pd.DataFrame,
                 frag_nominal: Dict[str, float], vi_feed_acidic: float) -> pd.DataFrame:
    """For every platform worst case the IACs rely on, what THIS campaign showed for that step.

    Two numbers. ``observed_edge`` is the worst value among the response-surface runs, which sit
    at the characterization edges and beyond the NOR. ``predicted_nor`` is the worst value the
    fitted response-surface model predicts anywhere in the NOR box, which is the region routine
    manufacture runs in and so the one the criteria have to hold for. ``met`` is judged on
    ``predicted_nor``. A platform worst case that is not met is replaced, in :func:`final`, by
    the A-Mab value, which can only tighten the criterion."""
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
            edge = nor = nor_bound = None
            if (step, cqa) in feeds and step in data:
                feed, col, mode = feeds[(step, cqa)]
                df = data[step]
                if col in df and df[col].notna().all():
                    edge = float((feed / df[col]).min()) if mode == "fold" else float((df[col] - feed).max())
                    nor, nor_bound = _nor_worst(cfg, step, df, col, feed, mode)
            met = None if nor is None else (nor >= assumed if kind == "fold_min" else nor <= assumed)
            # widening (owner's decision 2026-10-08): allowed only where the A-Mab worst case beats
            # the platform value even at its 95 % confidence bound
            better = None if nor is None else (nor_bound > assumed if kind == "fold_min" else nor_bound < assumed)
            rows.append({"step": cfg.unit_op(step).step, "step_key": step, "cqa": cqa,
                         "assumption": kind, "assumed": assumed, "observed_edge": edge,
                         "predicted_nor": nor, "predicted_nor_bound95": nor_bound if nor is not None else None,
                         "met": met, "widening_supported": better, "source": p.get("source", "")})
    return pd.DataFrame(rows)


def final(cfg: Config, ver: pd.DataFrame) -> pd.DataFrame:
    """The criteria in force: the a-priori table, tightened wherever verification showed a step
    doing worse within its NOR than the platform worst case assumed. Never loosened."""
    tighten = {}
    for _, r in ver[ver["met"] == False].iterrows():  # noqa: E712  (None stays unverified)
        tighten[(r["step_key"], r["cqa"])] = {r["assumption"]: float(r["predicted_nor"])}
    # Widening uses the 95 % confidence bound, never the point prediction, and only where the
    # bound beats the platform worst case (owner's decision 2026-10-08: "if the data supports it,
    # a criterion could be widened, but it needs good arguments"). The report argues each one.
    if "widening_supported" in ver.columns and cfg.raw()["iac"].get("allow_widening", False):
        for _, r in ver[ver["widening_supported"] == True].iterrows():  # noqa: E712
            tighten[(r["step_key"], r["cqa"])] = {r["assumption"]: float(r["predicted_nor_bound95"])}
    a = derive(cfg)
    f = derive(cfg, tighten)
    a["iac_low_apriori"], a["iac_high_apriori"] = a["iac_low"], a["iac_high"]
    a["iac_low"], a["iac_high"] = f["iac_low"], f["iac_high"]
    a["tightened"] = (a["iac_high"] < a["iac_high_apriori"]) | (a["iac_low"] > a["iac_low_apriori"])
    a["widened"] = (f["iac_high"] > a["iac_high_apriori"]) | (f["iac_low"] < a["iac_low_apriori"])
    # the derivation columns of a tightened row show the value that replaced the platform worst
    # case, so the criterion can be recomputed from its own row
    ch = a["tightened"] | a["widened"]
    a.loc[ch, "downstream_fold"] = f.loc[ch, "downstream_fold"]
    a.loc[ch, "downstream_added"] = f.loc[ch, "downstream_added"]
    a.loc[a["tightened"], "basis"] = "back-calculated, tightened on verification"
    a.loc[a["widened"], "basis"] = "back-calculated, widened on verification"
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
                lo, hi = lo_ds, val
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
