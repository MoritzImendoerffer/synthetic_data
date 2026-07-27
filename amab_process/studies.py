"""Characterization studies: DoE datasets, PPQ batches, Monte-Carlo capability.

These functions turn the process model into the datasets the report presents:

* :func:`step_feeds` — the representative scale-down feed to each unit operation
  (the nominal upstream output), so a step DoE varies only that step's parameters.
* :func:`screening_doe` / :func:`rsm_doe` — coded designs decoded to natural units,
  run through the single unit operation, returning runs x responses.
* :func:`fit_effects` — OLS main-effect / interaction (and quadratic) model with
  ANOVA, used for effect (Pareto) plots and design-space contours.
* :func:`ppq_batches` — a PPQ/validation campaign at NOR-distributed set-points.
* :func:`monte_carlo` / :func:`capability` — commercial-scale batch variation and
  per-CQA process-capability (Cpk) against the acceptance criteria.
"""

from __future__ import annotations

import itertools
from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

from .config import Config
from .core import Stream
from .doe import central_composite, decode, full_factorial, two_level_fractional
from .process import Process

# multivariate DoE factors per unit operation (natural parameter keys)
DOE_FACTORS: Dict[str, List[str]] = {
    "bioreactor": ["pH", "temperature", "co2", "osmolality", "duration"],
    "protein_a": ["load", "elution_ph", "flow", "end_collect"],
    "viral_inactivation": ["ph", "hold_time", "temperature"],
    "cex": ["load", "wash_cond", "elution_ph", "stop_collect"],
    "aex": ["load_ph", "wash1_cond", "load_cond", "load"],
    "virus_filtration": ["filtration_volume", "pressure"],
}

# factors carried into the response-surface (CCD) design per unit operation
# (a subset of the screening factors — the significant few). Default: first four.
RSM_TOP: Dict[str, List[str]] = {
    "bioreactor": ["pH", "temperature", "duration", "co2"],
    "aex": ["load_ph", "wash1_cond", "load_cond", "load"],
}

# responses of interest per unit operation (keys resolved from cqas then metrics)
DOE_RESPONSES: Dict[str, List[str]] = {
    "bioreactor": ["afucosylation", "galactosylation", "high_mannose",
                   "acidic_variants", "aggregates_hmw"],
    "protein_a": ["pool_hcp_ng_mg", "step_yield", "leached_protein_a_ppm"],
    "viral_inactivation": ["aggregate_out_pct", "xmulv_lrf", "acidic_variants"],
    "cex": ["aggregate_out_pct", "hcp_out_ng_mg", "step_yield"],
    "aex": ["hcp_out_ng_mg", "xmulv_lrf", "mvm_lrf", "step_yield"],
    "virus_filtration": ["mvm_lrf", "xmulv_lrf", "step_yield"],
}


def step_feeds(proc: Process) -> Dict[str, Optional[Stream]]:
    """Representative feed stream into each unit operation (nominal batch inputs)."""
    batch = proc.nominal_batch()
    feeds: Dict[str, Optional[Stream]] = {}
    for key, res in zip([k for k, _ in proc.units], batch.steps):
        feeds[key] = res.inp.copy() if res.inp is not None else None
    feeds["bioreactor"] = None
    return feeds


def _unit(proc: Process, key: str):
    return dict(proc.units)[key]


def _response_value(res, name: str) -> float:
    if name in res.out.cqas:
        return float(res.out.cqas[name])
    if name in res.metrics:
        return float(res.metrics[name])
    if name == "step_yield":
        return float(res.step_yield)
    return float("nan")


def _run_design(proc: Process, key: str, design: pd.DataFrame,
                responses: Sequence[str], feed: Optional[Stream],
                rng: np.random.Generator) -> pd.DataFrame:
    uo = _unit(proc, key)
    factors = [c for c in design.columns if c != "run_type"]
    ranges = {f: uo.uo.param(f).prange for f in factors}
    natural = decode(design, ranges)
    rows = []
    for i in range(len(design)):
        overrides = {f: float(natural.iloc[i][f]) for f in factors}
        res = uo.run(None if feed is None else feed.copy(), rng, setpoints=overrides)
        row = {"run": i + 1, "run_type": design.iloc[i]["run_type"]}
        row.update({f: float(natural.iloc[i][f]) for f in factors})
        row.update({f"coded_{f}": float(design.iloc[i][f]) for f in factors})
        for r in responses:
            row[r] = _response_value(res, r)
        rows.append(row)
    return pd.DataFrame(rows)


def screening_doe(proc: Process, key: str, feed: Optional[Stream],
                  rng: np.random.Generator, center_points: int = 3) -> pd.DataFrame:
    """Two-level screening design (full factorial, or res-V half-fraction for k=5)."""
    factors = DOE_FACTORS[key]
    if len(factors) == 5:
        design = two_level_fractional(
            factors, generators={factors[4]: factors[:4]},
            base_factors=factors[:4], center_points=center_points)
    else:
        design = full_factorial(factors, center_points=center_points)
    return _run_design(proc, key, design, DOE_RESPONSES[key], feed, rng)


def rsm_doe(proc: Process, key: str, feed: Optional[Stream],
            rng: np.random.Generator, top_factors: Optional[Sequence[str]] = None,
            center_points: int = 4) -> pd.DataFrame:
    """Face-centred central-composite response-surface design."""
    factors = list(top_factors) if top_factors else DOE_FACTORS[key][:4]
    design = central_composite(factors, center_points=center_points, face_centered=True)
    return _run_design(proc, key, design, DOE_RESPONSES[key], feed, rng)


def superseded_doe(proc: Process, key: str, feed: Optional[Stream],
                   rng: np.random.Generator, kind: str, deam: Dict[str, float],
                   top_factors: Optional[Sequence[str]] = None,
                   center_points: Optional[int] = None) -> pd.DataFrame:
    """Run the SAME screening/rsm design as the nominal study, but on a non-representative
    load (deamidation active) — the invalidated first execution that was re-run.

    A deviation that invalidates a study and forces a full re-execution means the study was
    *really performed twice*. This regenerates that first execution as a real dataset by
    setting the unit-op's ``load_deamidated`` context (see the step model) so the responses
    carry the anomaly, then clearing it. Deterministic given ``rng`` and ``deam``.
    """
    uo = _unit(proc, key)
    setattr(uo, "load_deamidated", dict(deam))
    try:
        if kind == "screening":
            return screening_doe(proc, key, feed, rng,
                                 center_points=3 if center_points is None else center_points)
        return rsm_doe(proc, key, feed, rng, top_factors=top_factors,
                       center_points=4 if center_points is None else center_points)
    finally:
        if hasattr(uo, "load_deamidated"):
            delattr(uo, "load_deamidated")


def fit_effects(df: pd.DataFrame, response: str, factors: Sequence[str],
                quadratic: bool = False) -> Dict[str, object]:
    """Fit an OLS main-effect + 2-way interaction (+ quadratic) model on coded factors."""
    import statsmodels.formula.api as smf

    coded = {f: df[f"coded_{f}"] for f in factors}
    data = pd.DataFrame(coded)
    data["_y"] = df[response].values
    terms = list(factors)
    terms += [f"{a}:{b}" for a, b in itertools.combinations(factors, 2)]
    if quadratic:
        terms += [f"I({f}**2)" for f in factors]
    formula = "_y ~ " + " + ".join(terms)
    model = smf.ols(formula, data=data).fit()
    eff = model.params.drop("Intercept", errors="ignore")
    effects = (2 * eff).rename("effect").to_frame()          # effect = 2 x coeff
    effects["coef"] = eff
    effects["p_value"] = model.pvalues.reindex(effects.index)
    effects["abs_effect"] = effects["effect"].abs()
    effects = effects.sort_values("abs_effect", ascending=False)
    return {"model": model, "effects": effects, "r2": model.rsquared,
            "r2_adj": model.rsquared_adj}


# --- PPQ & Monte-Carlo --------------------------------------------------------
def _sample_overrides(proc: Process, rng: np.random.Generator,
                      keys: Optional[Sequence[str]] = None) -> Dict[str, Dict[str, float]]:
    """Sample a batch operating point: each parameter ~ N(setpoint, (NOR width)/6)."""
    keys = keys or [k for k, _ in proc.units]
    overrides: Dict[str, Dict[str, float]] = {}
    for key in keys:
        uo = proc.cfg.unit_op(key)
        d = {}
        for p in uo.parameters:
            lo, hi = p.nor
            sigma = max((hi - lo) / 6.0, 1e-9)
            val = rng.normal(p.setpoint, sigma)
            val = float(np.clip(val, p.prange[0], p.prange[1]))
            d[p.key] = val
        overrides[key] = d
    return overrides


def ppq_batches(proc: Process, n: Optional[int] = None,
                rng: Optional[np.random.Generator] = None) -> pd.DataFrame:
    """Run a PPQ / validation campaign; one row per batch with DS CQAs and yield."""
    n = n or int(proc.cfg.meta["n_ppq_batches"])
    rng = rng or proc.rng(1000)
    rows = []
    for b in range(1, n + 1):
        batch = proc.run_batch(rng, overrides=_sample_overrides(proc, rng))
        row = {"batch": f"PPQ-{b:03d}", "overall_yield": batch.overall_yield}
        row.update(batch.drug_substance.cqas)
        rows.append(row)
    return pd.DataFrame(rows)


def monte_carlo(proc: Process, n: Optional[int] = None,
                rng: Optional[np.random.Generator] = None) -> pd.DataFrame:
    """Commercial-scale batch simulation; one row per batch with DS CQAs and yield."""
    n = n or int(proc.cfg.meta["n_monte_carlo"])
    rng = rng or proc.rng(5000)
    rows = []
    for b in range(n):
        batch = proc.run_batch(rng, overrides=_sample_overrides(proc, rng))
        row = {"batch": b, "overall_yield": batch.overall_yield}
        row.update(batch.drug_substance.cqas)
        rows.append(row)
    return pd.DataFrame(rows)


# capability spec type: 'upper' = smaller-is-better impurity (upper limit only);
# 'lower' = larger-is-better viral clearance (lower requirement only);
# otherwise a two-sided target range. Acidic charge variants (deamidation) are a
# very-low-criticality attribute whose risk is elevated levels, so capability is
# assessed one-sided against the upper design-space bound.
UPPER_ONLY = {"aggregates_hmw", "hcp", "residual_dna", "leached_protein_a", "acidic_variants"}
LOWER_ONLY = {"lrv_xmulv", "lrv_mvm"}


def spec_type(key: str) -> str:
    if key in UPPER_ONLY:
        return "upper"
    if key in LOWER_ONLY:
        return "lower"
    return "two_sided"


def capability(df: pd.DataFrame, cfg: Config) -> pd.DataFrame:
    """Per-CQA descriptive stats and process capability vs acceptance criteria.

    Capability is one-sided for impurities (Cpu) and for viral clearance (Cpl),
    and two-sided (Cpk = min) for target-range attributes — so an impurity with
    no meaningful lower limit is not penalised by proximity to zero.
    """
    rows = []
    for c in cfg.cqas:
        k = c["key"]
        if k not in df.columns:
            continue
        x = df[k].to_numpy(dtype=float)
        mu, sd = float(np.mean(x)), float(np.std(x, ddof=1))
        lo, hi = c["acceptance"]
        stype = spec_type(k)
        cpl = (mu - lo) / (3 * sd) if sd > 0 else np.inf
        cpu = (hi - mu) / (3 * sd) if sd > 0 else np.inf
        if stype == "lower":             # viral clearance: floor only
            cpk, cpu = cpl, np.nan
        elif stype == "upper":           # impurity: ceiling only
            cpk, cpl = cpu, np.nan
        else:                            # two-sided target range
            cpk = min(cpl, cpu)
        rows.append({
            "cqa": c["name"], "key": k, "unit": c["unit"], "spec_type": stype,
            "criticality": c["criticality_level"], "n": len(x),
            "mean": mu, "sd": sd, "min": float(x.min()), "max": float(x.max()),
            "acc_low": lo, "acc_high": hi, "Cpl": cpl, "Cpu": cpu, "Cpk": cpk,
        })
    return pd.DataFrame(rows)
