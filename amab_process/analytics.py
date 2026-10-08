"""Analytical layer (Rev 2.0): fragments, which method measured them, and how SEC reads them.

Everything here is computed AFTER the process model has run, from its own RNG streams, so no
pre-existing response, effect or Monte-Carlo column moves. Rev 1.0 and Rev 2.0 therefore analyse
the same experiments, and ``tests/test_analytics.py`` proves it against the tag ``corpus-rev1.0``.

Three things are modelled, all configured under ``analytics:`` in ``config/parameters.yaml``:

* the **true** fragment level (clipped species) through the train: formed in culture and during
  the harvest hold, partly lost at Protein A (Fab-type fragments carry no Fc), raised a little by
  the low-pH hold, partly cleared by cation exchange, unchanged after that;
* **nrCE-SDS**, which reads the true level with its own precision and a limit of quantitation;
* **SEC**, which reads the true level plus the part of the pool's host cell protein that elutes
  in the LMW window. The bias cannot exceed the HCP mass present; it is a few tenths of a percent
  at capture and viral inactivation and negligible from cation exchange onward.

Which method measured which study is the ``analytics.plan``; a study or method absent from it is
"not tested", and the column holds NaN.
"""
from __future__ import annotations

from typing import Dict, Optional

import numpy as np
import pandas as pd

from .config import Config

# DoE study ids per (step, kind), as recorded in campaign.studies
STUDY_ID = {
    ("protein_a", "screening"): "S-PA-SCR", ("protein_a", "rsm"): "S-PA-RSM",
    ("viral_inactivation", "screening"): "S-VI-SCR", ("viral_inactivation", "rsm"): "S-VI-RSM",
    ("cex", "screening"): "S-CEX-SCR", ("cex", "rsm"): "S-CEX-RSM",
    ("aex", "screening"): "S-AEX-SCR", ("aex", "rsm"): "S-AEX-RSM",
    ("aex", "superseded"): "S-AEX-SUP",
    ("virus_filtration", "screening"): "S-VF-DOE", ("virus_filtration", "rsm"): "S-VF-RSM",
    ("bioreactor", "screening"): "S-BRX-SCR", ("bioreactor", "rsm"): "S-BRX-RSM",
}

#: Operating parameters the fragment model reads, recorded per Monte-Carlo batch.
FRAG_OPS = [("bioreactor", "duration"), ("protein_a", "elution_ph"),
            ("viral_inactivation", "hold_time"), ("viral_inactivation", "temperature"),
            ("cex", "stop_collect")]

LMW_SEC, LMW_CE = "lmw_sec_pct", "lmw_cesds_pct"


def _a(cfg: Config) -> dict:
    return cfg.raw()["analytics"]


def _rng(cfg: Config, *key: int) -> np.random.Generator:
    """An independent stream: the master seed, the analytics offset and a study-specific key."""
    return np.random.default_rng([cfg.seed, int(_a(cfg)["rng_offset"]), *key])


def _coded(cfg: Config, step: str, param: str, value) -> np.ndarray:
    lo, hi = cfg.unit_op(step).param(param).prange
    return (np.asarray(value, dtype=float) - (lo + hi) / 2) / ((hi - lo) / 2)


def _sp(cfg: Config, step: str, param: str) -> float:
    return float(cfg.unit_op(step).param(param).setpoint)


# --------------------------------------------------------------------------------------
# True fragment level through the train
# --------------------------------------------------------------------------------------
def frag_harvest(cfg: Config, duration=None, hold_days: float = 0.0, cold: bool = True):
    f = _a(cfg)["fragments"]
    d = _sp(cfg, "bioreactor", "duration") if duration is None else duration
    rate = f["harvest_hold_rate_2_8"] if cold else f["harvest_hold_rate_rt"]
    return f["harvest_base"] * (1 + f["harvest_duration_coef"] * _coded(cfg, "bioreactor", "duration", d)) \
        + rate * np.asarray(hold_days, dtype=float)


def frag_protein_a(cfg: Config, feed, elution_ph=None):
    f = _a(cfg)["fragments"]
    ph = _sp(cfg, "protein_a", "elution_ph") if elution_ph is None else elution_ph
    return np.asarray(feed) * f["protein_a_passthrough"] \
        + f["protein_a_elution_ph_coef"] * _coded(cfg, "protein_a", "elution_ph", ph)


def frag_vi(cfg: Config, feed, hold_time=None, temperature=None):
    f = _a(cfg)["fragments"]
    t = _sp(cfg, "viral_inactivation", "hold_time") if hold_time is None else hold_time
    T = _sp(cfg, "viral_inactivation", "temperature") if temperature is None else temperature
    ct = _coded(cfg, "viral_inactivation", "temperature", T)
    return np.asarray(feed) + f["vi_delta_180"] * (np.asarray(t, dtype=float) / 180.0) * (1 + f["vi_temp_coef"] * ct)


def frag_cex(cfg: Config, feed, stop_collect=None):
    f = _a(cfg)["fragments"]
    sc = _sp(cfg, "cex", "stop_collect") if stop_collect is None else stop_collect
    fold = f["cex_clearance_fold"] * (1 + f["cex_stop_collect_coef"] * _coded(cfg, "cex", "stop_collect", sc))
    return np.asarray(feed) / fold


def nominal_train(cfg: Config) -> Dict[str, float]:
    """True fragment level leaving each step at set-point (harvest held one day at 2-8 C)."""
    h = float(frag_harvest(cfg, hold_days=1.0))
    pa = float(frag_protein_a(cfg, h))
    vi = float(frag_vi(cfg, pa))
    cx = float(frag_cex(cfg, vi))
    return {"bioreactor": float(frag_harvest(cfg)), "harvest": h, "protein_a": pa,
            "viral_inactivation": vi, "cex": cx, "aex": cx, "virus_filtration": cx, "ufdf": cx}


# --------------------------------------------------------------------------------------
# Measurement
# --------------------------------------------------------------------------------------
def sec_bias(cfg: Config, hcp_ng_mg, lpa_ppm=0.0):
    """Absolute % added to SEC LMW: the LMW-eluting fraction of the host cell protein mass
    (1e4 ng/mg = 1 %). ``lpa_ppm`` is accepted and ignored: a few ppm cannot register."""
    b = _a(cfg)["sec_bias"]
    return b["lmw_fraction"] * np.asarray(hcp_ng_mg, dtype=float) / 1e4


def measure(cfg: Config, method: str, true, rng: np.random.Generator, hcp=0.0, lpa=0.0):
    m = _a(cfg)["methods"][method]
    true = np.asarray(true, dtype=float)
    noise = rng.normal(0.0, m["sd_abs"], size=true.shape)
    if method == "sec":
        return np.maximum(true + sec_bias(cfg, hcp, lpa) + noise, 0.0)
    return np.maximum(true + noise, 0.0)


def _matrix(step: str, ps: pd.DataFrame, df: Optional[pd.DataFrame] = None):
    """(pool HCP ng/mg, leached Protein A ppm) the sample matrix carries, per run where the DoE
    measured them, else the nominal value of that step's pool."""
    ps = ps.set_index("step")
    nom = {
        "protein_a": (ps.loc[5, "pool_hcp_ng_mg"], ps.loc[5, "leached_protein_a_ppm"]),
        "viral_inactivation": (ps.loc[5, "pool_hcp_ng_mg"], ps.loc[5, "leached_protein_a_ppm"]),
        "cex": (ps.loc[7, "hcp_out_ng_mg"], ps.loc[5, "leached_protein_a_ppm"] / 10.0),
        "aex": (ps.loc[8, "hcp_out_ng_mg"], ps.loc[5, "leached_protein_a_ppm"] / 1000.0),
        "virus_filtration": (ps.loc[8, "hcp_out_ng_mg"], ps.loc[5, "leached_protein_a_ppm"] / 1000.0),
    }
    hcp, lpa = nom.get(step, (0.0, 0.0))
    n = 1 if df is None else len(df)
    hcp = np.full(n, float(hcp))
    lpa = np.full(n, float(lpa))
    if df is not None:
        for col in ("pool_hcp_ng_mg", "hcp_out_ng_mg"):
            if col in df.columns:
                hcp = df[col].to_numpy(dtype=float)
        if "leached_protein_a_ppm" in df.columns:
            lpa = df["leached_protein_a_ppm"].to_numpy(dtype=float)
    return hcp, lpa


def _doe_true(cfg: Config, step: str, df: pd.DataFrame) -> Optional[np.ndarray]:
    nom = nominal_train(cfg)
    n = len(df)
    if step == "protein_a":
        return frag_protein_a(cfg, np.full(n, nom["harvest"]), df["elution_ph"].to_numpy())
    if step == "viral_inactivation":
        return frag_vi(cfg, np.full(n, nom["protein_a"]), df["hold_time"].to_numpy(),
                       df["temperature"].to_numpy())
    if step == "cex":
        return frag_cex(cfg, np.full(n, nom["viral_inactivation"]), df["stop_collect"].to_numpy())
    if step in ("aex", "virus_filtration"):
        return np.full(n, nom["cex"])
    return None


def annotate_doe(cfg: Config, step: str, kind: str, df: pd.DataFrame,
                 ps: pd.DataFrame, sub: int = 0) -> pd.DataFrame:
    """Return ``df`` with the fragment columns the method plan says were measured.

    Columns are added only for steps where fragments are in scope at all; a method the plan
    does not list for this study is NaN in every row ("not tested"). Pre-existing columns are
    returned untouched."""
    sid = STUDY_ID.get((step, kind))
    true = _doe_true(cfg, step, df)
    if sid is None or true is None:
        return df
    plan = _a(cfg)["plan"].get(sid, [])
    out = df.copy()
    hcp, lpa = _matrix(step, ps, df)
    idx = list(_a(cfg)["plan"]).index(sid) if sid in _a(cfg)["plan"] else 99
    # ``sub`` separates two designs that share one study id (the superseded AEX execution ran
    # a screening and a response-surface design under S-AEX-SUP)
    out[LMW_SEC] = measure(cfg, "sec", true, _rng(cfg, 1, idx, sub), hcp, lpa) if "sec" in plan else np.nan
    out[LMW_CE] = measure(cfg, "cesds", true, _rng(cfg, 2, idx, sub)) if "cesds" in plan else np.nan
    return out


# --------------------------------------------------------------------------------------
# Monte Carlo / PPQ: fragments in the drug substance
# --------------------------------------------------------------------------------------
def frag_batches(cfg: Config, ops: pd.DataFrame, stream: int) -> np.ndarray:
    """True drug-substance fragment level per batch from the recorded operating point.

    The harvest hold is not a process parameter of the model, so it is drawn here, from its own
    stream: 0-2 days at 2-8 C, uniform."""
    rng = _rng(cfg, 3, stream)
    hold = rng.uniform(0.0, 2.0, size=len(ops))
    h = frag_harvest(cfg, ops["op_bioreactor_duration"].to_numpy(), hold)
    pa = frag_protein_a(cfg, h, ops["op_protein_a_elution_ph"].to_numpy())
    vi = frag_vi(cfg, pa, ops["op_viral_inactivation_hold_time"].to_numpy(),
                 ops["op_viral_inactivation_temperature"].to_numpy())
    cx = frag_cex(cfg, vi, ops["op_cex_stop_collect"].to_numpy())
    # batch-to-batch biological variation of clipping, multiplicative
    return cx * rng.lognormal(0.0, 0.06, size=len(ops))


# --------------------------------------------------------------------------------------
# Chronology, method plan, hold studies, comparability
# --------------------------------------------------------------------------------------
def chronology(cfg: Config) -> pd.DataFrame:
    return pd.DataFrame(cfg.raw()["campaign"]["studies"])


def method_plan(cfg: Config) -> pd.DataFrame:
    """One row per study: which method measured fragments, and which measured HMW."""
    a = _a(cfg)
    rows = []
    for s in cfg.raw()["campaign"]["studies"]:
        p = a["plan"].get(s["id"])
        rows.append({"study": s["id"], "step": s["step"], "kind": s["kind"],
                     "start": s["start"], "end": s["end"],
                     "lmw_sec": bool(p and "sec" in p), "lmw_cesds": bool(p and "cesds" in p),
                     "lmw_in_scope": p is not None})
    return pd.DataFrame(rows)


def hold_study(cfg: Config, pool: str, ps: pd.DataFrame) -> pd.DataFrame:
    """Hold-time stability of one intermediate: HMW and acidic variants at every time point,
    LMW by SEC at every time point and by CE-SDS only at ``cesds_days``. NaN = not tested."""
    h = _a(cfg)["holds"][pool]
    pools = list(_a(cfg)["holds"])
    rng = _rng(cfg, 4, pools.index(pool))
    nom = nominal_train(cfg)
    f0 = nom["harvest"] if pool == "harvest" else nom[pool]
    hcp, lpa = _matrix("protein_a" if pool == "harvest" else pool, ps)
    rows = []
    for ti, temp in enumerate(h["temps"]):
        cold = temp.startswith("2-8")
        # clipping is protease-driven; purified pools carry far less protease than harvest
        frag_rate = (_a(cfg)["fragments"]["harvest_hold_rate_2_8"] if cold
                     else _a(cfg)["fragments"]["harvest_hold_rate_rt"]) * (1.0 if pool == "harvest" else 0.4)
        for d in h["days"]:
            true_f = f0 + frag_rate * d
            rows.append({
                "pool": pool, "temperature": temp, "day": d,
                "hmw_pct": float(h["hmw0"] + h["hmw_rate"][ti] * d + rng.normal(0, 0.05)),
                "acidic_pct": float(h["acid0"] + h["acid_rate"][ti] * d + rng.normal(0, 0.25)),
                LMW_SEC: float(measure(cfg, "sec", [true_f], rng, hcp[0], lpa[0])[0]),
                LMW_CE: (float(measure(cfg, "cesds", [true_f], rng)[0]) if d in h["cesds_days"] else np.nan),
            })
    return pd.DataFrame(rows)


def comparability(cfg: Config, ps: pd.DataFrame) -> pd.DataFrame:
    """S-CEX-FRC: the same samples by SEC and by nrCE-SDS, across the matrices of the train."""
    nom = nominal_train(cfg)
    rng = _rng(cfg, 5, 0)
    rows = []
    for spec in _a(cfg)["comparability"]:
        step = spec["step"]
        base = nom[step] * spec.get("frag_mult", 1.0)
        if spec["sample"] == "CEX load":
            base = nom["viral_inactivation"]
        mstep = "cex" if spec["sample"].startswith("CEX fraction") else step
        hcp, lpa = _matrix(mstep, ps)
        for i in range(int(spec["n"])):
            true_f = base * rng.lognormal(0.0, 0.05)
            sec = float(measure(cfg, "sec", [true_f], rng, hcp[0], lpa[0])[0])
            ce = float(measure(cfg, "cesds", [true_f], rng)[0])
            rows.append({"sample": spec["sample"], "step": step, "replicate": i + 1,
                         LMW_SEC: sec, LMW_CE: ce, "difference": sec - ce})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------------------
# Scale-down model qualification (S-xx-SDM)
# --------------------------------------------------------------------------------------
SDM_RESPONSES = {
    "bioreactor": ["afucosylation", "galactosylation", "high_mannose", "acidic_variants", "aggregates_hmw"],
    "protein_a": ["pool_hcp_ng_mg", "step_yield", "leached_protein_a_ppm"],
    "viral_inactivation": ["aggregate_out_pct", "acidic_variants"],
    "cex": ["aggregate_out_pct", "hcp_out_ng_mg", "step_yield"],
    "aex": ["hcp_out_ng_mg", "step_yield"],
    "virus_filtration": ["step_yield"],
}


def _assay_noise(cfg: Config, row: dict, si: int, stream: int, i: int) -> None:
    """Analytical repeatability on a qualification result, from its own stream. A step whose
    process model passes an attribute through unchanged (acidic variants across low-pH
    inactivation) would otherwise report the same value for every run at both scales."""
    cv = _a(cfg)["sdm"].get("assay_cv", {})
    rng = _rng(cfg, 11, si, stream, i)
    for r, c in cv.items():
        if r in row and row[r] is not None:
            row[r] = float(row[r] * rng.lognormal(0.0, float(c)))


def sdm_qualification(cfg: Config, proc, feeds) -> pd.DataFrame:
    """Set-point runs at small scale against manufacturing-scale batches, per step.

    Both scales run the same process model at the set-point, each from its own stream, so they
    differ by run-to-run variation only, except where ``analytics.sdm.scale_offset`` records a
    known scale effect (leached Protein A follows resin cycle history at manufacturing scale)."""
    from .studies import _response_value, _unit
    a = _a(cfg)["sdm"]
    rows = []
    for si, (step, resps) in enumerate(SDM_RESPONSES.items()):
        uo = _unit(proc, step)
        off = a.get("scale_offset", {}).get(step, {})
        for scale, n, stream in (("scale-down", a["n_scale_down"], 0), ("manufacturing", a["n_manufacturing"], 1)):
            rng = _rng(cfg, 6, si, stream)
            for i in range(int(n)):
                feed = feeds.get(step)
                res = uo.run(None if feed is None else feed.copy(), rng)
                row = {"study": f"S-{ {'bioreactor': 'BRX', 'protein_a': 'PA', 'viral_inactivation': 'VI', 'cex': 'CEX', 'aex': 'AEX', 'virus_filtration': 'VF'}[step]}-SDM",
                       "step": step, "scale": scale, "run": i + 1}
                for r in resps:
                    v = _response_value(res, r)
                    if scale == "manufacturing" and r in off:
                        v *= float(off[r])
                    row[r] = v
                _assay_noise(cfg, row, si, stream, i)
                if step in CHROM_STEPS:
                    ce = _rng(cfg, 7, si, stream, i)
                    row["plates_per_m"] = float(ce.normal(*a["column"]["plates_per_m"]))
                    row["asymmetry"] = float(ce.normal(*a["column"]["asymmetry"]))
                rows.append(row)
        # supplementary scale-down runs recorded by a deviation (DEV-005-03)
        sup = a.get("supplementary", {}).get(step)
        if sup:
            rng = _rng(cfg, 6, 99, 2)
            for i in range(int(sup["n"])):
                feed = feeds.get(step)
                res = uo.run(None if feed is None else feed.copy(), rng)
                row = {"study": sup["study"], "step": step, "scale": "scale-down", "run": i + 1}
                for r in resps:
                    row[r] = _response_value(res, r)
                _assay_noise(cfg, row, si, 9, i)
                ce = _rng(cfg, 7, si, 9, i)
                row["plates_per_m"] = float(ce.normal(*a["column"]["plates_per_m"]))
                row["asymmetry"] = float(ce.normal(*a["column"]["asymmetry"]))
                rows.append(row)
    return pd.DataFrame(rows)


CHROM_STEPS = ("protein_a", "cex", "aex")


def univariate_studies(cfg: Config, proc, feeds) -> pd.DataFrame:
    """S-xx-UNI: each univariate parameter of a DoE step run in duplicate at the low and the high
    end of its characterized range, the other parameters at set-point. The set-point reference is
    the scale-down qualification runs. A parameter the step model does not respond to shows no
    effect beyond run-to-run variation, which is the result a GPP classification rests on."""
    from .studies import _response_value, _unit
    rows = []
    sid = {"bioreactor": "S-BRX-UNI", "protein_a": "S-PA-UNI", "viral_inactivation": "S-VI-UNI",
           "cex": "S-CEX-UNI", "aex": "S-AEX-UNI"}
    for si, (step, study) in enumerate(sid.items()):
        uo = _unit(proc, step)
        resps = SDM_RESPONSES[step]
        for pi, p in enumerate([q for q in cfg.unit_op(step).parameters if q.study == "univariate"]):
            for li, (level, val) in enumerate((("low", p.prange[0]), ("high", p.prange[1]))):
                rng = _rng(cfg, 8, si, pi, li)
                for rep in (1, 2):
                    feed = feeds.get(step)
                    res = uo.run(None if feed is None else feed.copy(), rng, setpoints={p.key: float(val)})
                    row = {"study": study, "step": step, "parameter": p.key, "level": level,
                           "value": float(val), "replicate": rep}
                    for r in resps:
                        row[r] = _response_value(res, r)
                    rows.append(row)
    return pd.DataFrame(rows)


def run_order(cfg: Config, df: pd.DataFrame, study_index: int) -> np.ndarray:
    """A randomized execution order for a design, from its own stream. Recorded in the CSV beside
    the standard-order run number (the record had standard order only)."""
    rng = _rng(cfg, 9, study_index)
    return rng.permutation(len(df)) + 1


def protein_a_extras(cfg: Config, df: pd.DataFrame, kind: str, bio_hmw: float) -> pd.DataFrame:
    """Per-pool aggregate by SEC (information only) and residual DNA on centre-point runs.

    Aggregate passes the capture step with the feed level plus a small rise at low elution pH;
    residual DNA is measured on the load and the pool of the centre-point runs only (NaN = not
    tested) and cleared by ``process.protein_a.model.dna_lrv``."""
    out = df.copy()
    rng = _rng(cfg, 10, 0 if kind == "screening" else 1)
    cph = _coded(cfg, "protein_a", "elution_ph", out["elution_ph"].to_numpy())
    out["hmw_sec_pct"] = bio_hmw + 0.08 * (-cph) + rng.normal(0, 0.05, len(out))
    lrv = float(cfg.process["protein_a"]["model"]["dna_lrv"])
    centre = out["run_type"].astype(str).str.startswith("cent").to_numpy()
    load = 2.0e5 * rng.lognormal(0, 0.15, len(out))
    pool = load / 10 ** (lrv + rng.normal(0, 0.15, len(out)))
    out["dna_load_pg_mg"] = np.where(centre, load, np.nan)
    out["dna_pool_pg_mg"] = np.where(centre, pool, np.nan)
    return out
