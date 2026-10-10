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
    return float(cfg.unit_op(step).param(param).setpoint_characterized)


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
def augmentation_studies(cfg: Config, steps) -> list:
    """The augmentation studies of INV-002 that the model-adequacy rule gave a step, as campaign
    study records. Which steps are augmented is computed (``adequacy.plan``), so the studies are
    added here and not listed in ``campaign.studies``: another seed can augment other steps."""
    aug = cfg.raw()["campaign"]["model_adequacy"]["studies"]
    return [{"id": aug[k]["id"], "step": k, "kind": "augmentation", "start": aug[k]["start"],
             "end": aug[k]["end"]} for k in steps]


def chronology(cfg: Config, extra: Optional[list] = None) -> pd.DataFrame:
    return pd.DataFrame(list(cfg.raw()["campaign"]["studies"]) + list(extra or []))


def method_plan(cfg: Config, extra: Optional[list] = None) -> pd.DataFrame:
    """One row per study: which method measured fragments, and which measured HMW."""
    a = _a(cfg)
    rows = []
    for s in list(cfg.raw()["campaign"]["studies"]) + list(extra or []):
        p = a["plan"].get(s["id"])
        rows.append({"study": s["id"], "step": s["step"], "kind": s["kind"],
                     "start": s["start"], "end": s["end"],
                     "lmw_sec": bool(p and "sec" in p), "lmw_cesds": bool(p and "cesds" in p),
                     "lmw_in_scope": p is not None})
    return pd.DataFrame(rows)


def hold_study(cfg: Config, pool: str, ps: pd.DataFrame) -> pd.DataFrame:
    """Hold-time stability of one intermediate: HMW and acidic variants at every time point, LMW by
    CE-SDS at ``cesds_days`` and by SEC only where the method plan lists SEC for the study. The hold
    studies were made after AMD-001 (owner, 2026-10-09): nrCE-SDS on every sample, no SEC fragment
    result. NaN = not tested."""
    h = _a(cfg)["holds"][pool]
    sec = "sec" in (_a(cfg)["plan"].get(h["study"]) or [])
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
                LMW_SEC: (float(measure(cfg, "sec", [true_f], rng, hcp[0], lpa[0])[0]) if sec else np.nan),
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
    # appended last so no step index above moves (owner's decision Q8, 2026-10-10: S-UFDF-SDM, the comparison
    # Version 1.0 PCP-010 planned: step yield, permeate flux, final concentration and aggregate)
    "ufdf": ["step_yield", "aggregate_out_pct", "ds_concentration_g_per_l", "flux_lmh"],
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
    # repeatability of the results of one step only (assay_cv_step), from a stream of its own, so that no
    # draw of the shared loop above moves
    cvs = _a(cfg)["sdm"].get("assay_cv_step", {}).get(row.get("step"), {})
    if cvs:
        rng2 = _rng(cfg, 11, si, stream, i, 1)
        for r, c in cvs.items():
            if r in row and row[r] is not None:
                row[r] = float(row[r] * rng2.lognormal(0.0, float(c)))


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
                row = {"study": f"S-{ {'bioreactor': 'BRX', 'protein_a': 'PA', 'viral_inactivation': 'VI', 'cex': 'CEX', 'aex': 'AEX', 'virus_filtration': 'VF', 'ufdf': 'UFDF'}[step]}-SDM",
                       "step": step, "scale": scale, "run": i + 1}
                for r in resps:
                    v = _response_value(res, r)
                    if r == "aggregate_out_pct" and np.isnan(v):
                        # a step with no aggregate metric of its own (UF/DF): the aggregate of its pool
                        v = float(res.out.cqas.get("aggregates_hmw", np.nan))
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
                    # read from the run, no draw (studies.EXTRA_RESPONSES; owner's decision Q5)
                    for col, src in EXTRA_RESPONSES_UNI.get(step, ()):
                        row[col] = _response_value(res, src)
                    rows.append(row)
    out = pd.DataFrame(rows)
    # the repeatability of each method on those results, from a stream of its own (key 33)
    return _assay_cols(out, {"harvest_hcp_ng_mg": _assay_cv(cfg, "AMV-3012"),
                             "harvest_dna_pg_mg": _assay_cv(cfg, "AMV-3014")}, _rng(cfg, 33, 2))


# --------------------------------------------------------------------------------------
# Results a Version 1.0 plan required and the seeded record lacked (owner's decision Q5, 2026-10-10:
# "Attributes in scope should be measured unless justified"). Each is a NEW column from a NEW stream
# (keys 30 to 36), drawn after the results it sits beside, so no existing value moves.
# --------------------------------------------------------------------------------------
EXTRA_RESPONSES_UNI = {"bioreactor": (("harvest_hcp_ng_mg", "hcp"), ("harvest_dna_pg_mg", "residual_dna"))}
# the univariate studies of the designed steps whose size variants a Version 1.0 plan required, measured
# by the methods analytics.plan lists for them (only S-PA-UNI has an entry: SEC, before the method decision
# AMD-001; its samples were not retained beyond 30 days, so the April 2026 retests could not cover them)
UNI_SIZE_STUDIES = {"S-PA-UNI": "protein_a", "S-VI-UNI": "viral_inactivation", "S-CEX-UNI": "cex",
                    "S-AEX-UNI": "aex"}


def _assay_cols(df: pd.DataFrame, cvs: Dict[str, float], rng: np.random.Generator) -> pd.DataFrame:
    """Each column of ``cvs`` (name -> CV) times its method's lognormal repeatability, in the order
    given, from ``rng``; a NaN stays NaN and still takes its draw, so the draws do not depend on
    which rows carry a result."""
    out = df.copy()
    for col, cv in cvs.items():
        if col in out.columns:
            v = out[col].to_numpy(dtype=float)
            out[col] = v * rng.lognormal(0.0, float(cv), size=len(v))
    return out


def bioreactor_impurities(cfg: Config, df: pd.DataFrame, sub: int) -> pd.DataFrame:
    """Host cell protein (ELISA, AMV-3012) and residual DNA (qPCR, AMV-3014) in the clarified broth
    of every bioreactor design run, which PCP-003 Version 1.0 required: the model's values (recorded
    by ``studies.EXTRA_RESPONSES``) with each method's repeatability, from stream 33."""
    return _assay_cols(df, {"harvest_hcp_ng_mg": _assay_cv(cfg, "AMV-3012"),
                            "harvest_dna_pg_mg": _assay_cv(cfg, "AMV-3014")}, _rng(cfg, 33, sub))


def univariate_size_variants(cfg: Config, uni: pd.DataFrame, ps: pd.DataFrame, feeds) -> pd.DataFrame:
    """Size variants of the univariate studies of the designed steps, which their Version 1.0 plans
    required ("the same responses measured as in the multivariate designs", PCP-005 §6.4): fragments
    by the methods ``analytics.plan`` lists for the study, and at Protein A aggregate by SEC, as the
    designs record it. The parameters these studies vary do not act on fragments in the model, so the
    true level is the step's set-point value; SEC carries the host cell protein of the run's pool in
    its LMW window (``sec_bias``). Stream 30."""
    plan = _a(cfg)["plan"]
    nom = nominal_train(cfg)
    out = uni.copy()
    for c in (LMW_SEC, LMW_CE, "hmw_sec_pct"):
        if c not in out.columns:
            out[c] = np.nan
    for si, (sid, step) in enumerate(UNI_SIZE_STUDIES.items()):
        sel = out["study"] == sid
        if "spiked" in out.columns:
            sel &= out["spiked"].fillna(False).astype(bool) == False    # a spiked run reports clearance only
        idx = out.index[sel]
        m = plan.get(sid, [])
        if not len(idx) or not m:
            continue
        rows = out.loc[idx]
        mcols = [c for c in ("pool_hcp_ng_mg", "hcp_out_ng_mg", "leached_protein_a_ppm")
                 if c in rows.columns and rows[c].notna().all()]
        hcp, lpa = _matrix(step, ps, rows[mcols])
        true = np.full(len(idx), float(nom[step]))
        if "sec" in m:
            out.loc[idx, LMW_SEC] = measure(cfg, "sec", true, _rng(cfg, 30, si, 0), hcp, lpa)
        if "cesds" in m:
            out.loc[idx, LMW_CE] = measure(cfg, "cesds", true, _rng(cfg, 30, si, 1))
        if step == "protein_a" and "sec" in m:
            bio_hmw = float(feeds["protein_a"].cqas.get("aggregates_hmw", 1.5))
            out.loc[idx, "hmw_sec_pct"] = bio_hmw + _rng(cfg, 30, si, 2).normal(0.0, 0.05, len(idx))
    return out


def aex_univariate_viral(cfg: Config, proc, feeds) -> pd.DataFrame:
    """The spiked run of the anion exchange flow-rate study at the high end of the range, which PCP-008
    Version 1.0 planned: XMuLV and MVM log reduction, from its own stream (key 31). One row, appended
    to the univariate study (``spiked``); the unspiked responses are not reported for it."""
    from .studies import _response_value, _unit
    p = cfg.unit_op("aex").param("flow")
    res = _unit(proc, "aex").run(feeds["aex"].copy(), _rng(cfg, 31, 0), setpoints={"flow": float(p.prange[1])})
    return pd.DataFrame([{"study": "S-AEX-UNI", "step": "aex", "parameter": "flow", "level": "high",
                          "value": float(p.prange[1]), "replicate": 3, "spiked": True,
                          "xmulv_lrf": _response_value(res, "xmulv_lrf"),
                          "mvm_lrf": _response_value(res, "mvm_lrf")}])


def ion_exchange_impurities(cfg: Config, df: pd.DataFrame, step: str, feeds, stream: int) -> pd.DataFrame:
    """Residual DNA (qPCR, AMV-3014) and leached Protein A (ELISA, AMV-3016) in the load and the pool of
    each run, which PCP-007 and PCP-008 Version 1.0 required on every response-surface pool and in the
    qualification. The step clears both by its log reduction (``process.<step>.model`` dna_lrv,
    leached_pa_lrv), independent of the parameters of the design (A-Mab: DNA and Protein A largely
    insensitive), with a run-to-run SD of 0.15 log, and each result carries its method's repeatability.
    A result below the method's LOQ is reported as below it (NaN, and ``*_lt_loq`` True). Stream 32."""
    rng = _rng(cfg, 32, stream)
    n = len(df)
    m = cfg.process[step]["model"]
    meth = {x["id"]: x for x in cfg.raw()["deviations"]["methods"]}
    feed = feeds[step]
    out = df.copy()
    for name, unit, src, lrv, amv in (("dna", "pg_mg", "residual_dna", m["dna_lrv"], "AMV-3014"),
                                      ("lpa", "ppm", "leached_protein_a", m["leached_pa_lrv"], "AMV-3016")):
        cv, loq = float(meth[amv]["precision_pct"]) / 100.0, float(meth[amv]["loq"])
        true = float(feed.cqas.get(src, 0.0))
        load = true * rng.lognormal(0.0, cv, n)
        pool = true / 10 ** (float(lrv) + rng.normal(0.0, 0.15, n)) * rng.lognormal(0.0, cv, n)
        out[f"{name}_load_{unit}"] = np.where(load >= loq, load, np.nan)
        out[f"{name}_load_lt_loq"] = load < loq
        out[f"{name}_pool_{unit}"] = np.where(pool >= loq, pool, np.nan)
        out[f"{name}_pool_lt_loq"] = pool < loq
    return out


def sdm_impurities(cfg: Config, sdm: pd.DataFrame, feeds) -> pd.DataFrame:
    """Residual DNA and leached Protein A in the cation and anion exchange pools of the qualification
    runs at both scales (``ion_exchange_impurities``, streams 34 and 35): the outputs PCP-007 and PCP-008
    Version 1.0 compared beside the others. Pools below the LOQ carry no value."""
    out = sdm.copy()
    for k, step in enumerate(("cex", "aex")):
        idx = out.index[out["step"] == step]
        if not len(idx):
            continue
        sub = ion_exchange_impurities(cfg, out.loc[idx].reset_index(drop=True), step, feeds, 34 + k)
        for c in ("dna_pool_pg_mg", "dna_pool_lt_loq", "lpa_pool_ppm", "lpa_pool_lt_loq"):
            out.loc[idx, c] = sub[c].to_numpy()
    return out


def cex_univariate_impurities(cfg: Config, uni: pd.DataFrame, feeds) -> pd.DataFrame:
    """Residual DNA and leached Protein A in the load and the pool of each run of the cation exchange
    flow-rate study, which PCP-007 Version 1.0 required ("the responses of §5.3 will be measured on
    each"; §5.3 lists residual DNA and leached Protein A). As ``ion_exchange_impurities``, stream 37."""
    out = uni.copy()
    idx = out.index[out["study"] == "S-CEX-UNI"]
    if not len(idx):
        return out
    sub = ion_exchange_impurities(cfg, out.loc[idx].reset_index(drop=True), "cex", feeds, 37)
    for c in ("dna_load_pg_mg", "dna_load_lt_loq", "dna_pool_pg_mg", "dna_pool_lt_loq",
              "lpa_load_ppm", "lpa_load_lt_loq", "lpa_pool_ppm", "lpa_pool_lt_loq"):
        out.loc[idx, c] = sub[c].to_numpy()
    return out


def nodoe_extras(cfg: Config, uni: pd.DataFrame, feeds) -> pd.DataFrame:
    """Attributes in scope of the Version 2.0 univariate studies of harvest and UF/DF that their plans
    list and the record lacked: fragments by nrCE-SDS (AMV-3020) and residual DNA by qPCR (AMV-3014) in
    the clarified harvest, acidic variants by icIEF (AMV-3013) in the UF/DF retentate. The harvest
    parameters do not act on them (A-Mab's no-impact assumption) and the UF/DF model has no charge-variant
    effect, so each is the feed value with its method's repeatability. Fragments are those of the
    harvest at the end of culture, sampled at clarification. Stream 36."""
    out = uni.copy()
    for c in (LMW_CE, "dna_out_pg_mg"):
        if c not in out.columns:
            out[c] = np.nan
    studies = _a(cfg)["univariate_nodoe"]["studies"]
    h = out.index[out["study"] == studies.get("harvest")]
    if len(h):
        out.loc[h, LMW_CE] = measure(cfg, "cesds", np.full(len(h), float(frag_harvest(cfg))), _rng(cfg, 36, 0))
        dna = float(feeds["harvest"].cqas.get("residual_dna", 0.0))
        out.loc[h, "dna_out_pg_mg"] = dna * _rng(cfg, 36, 1).lognormal(0.0, _assay_cv(cfg, "AMV-3014"), len(h))
    u = out.index[out["study"] == studies.get("ufdf")]
    if len(u):
        av = float(feeds["ufdf"].cqas.get("acidic_variants", np.nan))
        out.loc[u, "acidic_variants"] = av * _rng(cfg, 36, 2).lognormal(0.0, _assay_cv(cfg, "AMV-3013"), len(u))
    return out


def _nodoe_levels(p) -> list:
    """Five levels: the range ends, set-point, and halfway between set-point and each end."""
    lo, hi, sp = float(p.prange[0]), float(p.prange[1]), float(p.setpoint_characterized)
    return [lo, (lo + sp) / 2, sp, (sp + hi) / 2, hi]


def _assay_cv(cfg: Config, spec) -> float:
    if isinstance(spec, str):
        meth = {m["id"]: m for m in cfg.raw()["deviations"]["methods"]}[spec]
        return float(meth["precision_pct"]) / 100
    return float(spec)


def univariate_nodoe(cfg: Config, proc, feeds) -> pd.DataFrame:
    """S-HAR-UNI and S-UFDF-UNI: the two steps without a design (owner's option A, 2026-10-08).

    Each varied parameter at five levels in duplicate, the others at set-point, from its own
    stream (key 12). Each result carries the repeatability of its method
    (``analytics.univariate_nodoe.assay``). Harvest keeps A-Mab's no-quality-impact assumption:
    its attributes pass through and differ only by assay noise. Rows have the columns of
    ``univariate_studies`` and are appended to it."""
    from .studies import _response_value, _unit
    u = _a(cfg)["univariate_nodoe"]
    attr = {"hcp_out_ng_mg": "hcp", "aggregate_out_pct": "aggregates_hmw"}
    rows = []
    for si, (step, study) in enumerate(u["studies"].items()):
        uo = _unit(proc, step)
        challenge = u.get("challenge", {}).get(step, {})
        params = [q for q in cfg.unit_op(step).parameters if q.study == "univariate"]
        for pi, p in enumerate(params):
            for li, (level, val) in enumerate(zip(u["levels"], _nodoe_levels(p))):
                rng = _rng(cfg, 12, si, pi, li)
                for rep in range(1, int(u["replicates"]) + 1):
                    feed = feeds.get(step)
                    res = uo.run(None if feed is None else feed.copy(), rng, setpoints={p.key: float(val)})
                    row = {"study": study, "step": step, "parameter": p.key, "level": level,
                           "value": float(val), "replicate": rep}
                    for r in u["responses"][step]:
                        if p.key in challenge:
                            # the level set is the response; another performance output is not reported
                            if r == challenge[p.key]:
                                v = float(val)
                            elif r in attr or r == "step_yield":
                                v = float(res.out.cqas[attr[r]]) if r in attr else float(res.step_yield)
                            else:
                                row[r] = np.nan
                                continue
                        else:
                            v = float(res.out.cqas[attr[r]]) if r in attr else _response_value(res, r)
                        if r in u["assay"]:
                            v *= float(np.exp(rng.normal(0, _assay_cv(cfg, u["assay"][r]))))
                        row[r] = v
                    rows.append(row)
    return pd.DataFrame(rows)


def augmentation_runs(cfg: Config, proc, feeds, step: str, coded: np.ndarray, study: str,
                      n_planned: int, si: int) -> pd.DataFrame:
    """The runs of one INV-002 augmentation: the D-optimal points of ``coded`` run in the
    scale-down model as a second block (``block`` 2; the planned runs are block 1), numbered on
    from the planned design, in a randomized order. Every draw comes from this study's own stream
    (key 13), so no planned run moves. Viral clearance is not measured (``not_specification``: the
    augmentation sizes no viral model, and no virus is spiked). Fragments are measured by the
    methods the analytical plan lists for the study."""
    from .doe import decode
    from .studies import DOE_FACTORS, DOE_RESPONSES, RSM_TOP, _response_value, _unit
    factors = list(RSM_TOP.get(step, DOE_FACTORS[step][:4]))
    design = pd.DataFrame(np.asarray(coded, dtype=float), columns=factors)
    uo = _unit(proc, step)
    natural = decode(design, {f: uo.uo.param(f).prange for f in factors})
    skip = set(cfg.raw()["campaign"]["model_adequacy"]["not_specification"])
    rng = _rng(cfg, 13, si, 0)
    rows = []
    for i in range(len(design)):
        ov = {f: float(natural.iloc[i][f]) for f in factors}
        feed = feeds.get(step)
        res = uo.run(None if feed is None else feed.copy(), rng, setpoints=ov)
        row = {"run": n_planned + i + 1, "run_type": "augmentation", **ov,
               **{f"coded_{f}": float(design.iloc[i][f]) for f in factors}}
        for r in DOE_RESPONSES[step]:
            row[r] = np.nan if r in skip else _response_value(res, r)
        rows.append(row)
    out = pd.DataFrame(rows)
    true = _doe_true(cfg, step, out)
    if true is not None:
        plan = _a(cfg)["plan"].get(study, [])
        out[LMW_SEC] = np.nan
        out[LMW_CE] = measure(cfg, "cesds", true, _rng(cfg, 13, si, 1)) if "cesds" in plan else np.nan
    out["block"] = 2
    out["study"] = study
    out["run_order"] = _rng(cfg, 13, si, 2).permutation(len(out)) + 1
    return out


def vi_ofat(cfg: Config, proc, feeds) -> pd.DataFrame:
    """S-VI-OFAT: the low-pH hold at the re-centred pH against the former set-point, over the hold
    times of ``analytics.vi_ofat``, in duplicate, from its own stream (key 15). Aggregate and acidic
    variants as the step model gives them; fragments as the fragment model gives them, measured by
    nrCE-SDS. Time 0 is the pH-adjusted load before the hold."""
    from .studies import _response_value, _unit
    o = _a(cfg)["vi_ofat"]
    uo = _unit(proc, "viral_inactivation")
    feed = feeds["viral_inactivation"]
    nom = nominal_train(cfg)
    meth = {m["id"]: m for m in cfg.raw()["deviations"]["methods"]}
    sec_cv = float(meth["AMV-3221"]["precision_pct"]) / 100
    icief_cv = float(_a(cfg)["sdm"]["assay_cv"]["acidic_variants"])
    rows = []
    for ai, ph in enumerate(o["ph"]):
        for ti, t in enumerate(o["hold_min"]):
            rng = _rng(cfg, 15, ai, ti)
            for rep in range(1, int(o["replicates"]) + 1):
                if t == 0:
                    agg, acid = float(feed.cqas["aggregates_hmw"]), float(feed.cqas["acidic_variants"])
                    frag_true = float(nom["protein_a"])
                else:
                    res = uo.run(feed.copy(), rng, setpoints={"ph": float(ph), "hold_time": float(t),
                                                              "temperature": float(o["temperature"])})
                    agg = _response_value(res, "aggregate_out_pct")
                    acid = _response_value(res, "acidic_variants")
                    frag_true = float(frag_vi(cfg, nom["protein_a"], t, o["temperature"]))
                frag = float(measure(cfg, "cesds", np.array([frag_true]), rng)[0])
                # every result carries the repeatability of its method (SEC, icIEF): the step model
                # gives acidic variants without noise, which a laboratory result never is
                agg *= float(np.exp(rng.normal(0.0, sec_cv)))
                acid *= float(np.exp(rng.normal(0.0, icief_cv)))
                rows.append({"study": o["study"], "ph": float(ph), "hold_min": int(t),
                             "temperature": float(o["temperature"]), "replicate": rep,
                             "aggregate_out_pct": agg, "acidic_variants": acid, LMW_CE: frag})
    return pd.DataFrame(rows)


def vi_concentration_xmulv(cfg: Config, proc, feeds) -> pd.DataFrame:
    """S-VI-UNI2 (PD-006-06, owner 2026-10-09): XMuLV-spiked low-pH holds at the low and the high end
    of the A-Mab concentration range studied, in duplicate, the other parameters at their set-points as
    characterized, from its own stream (key 20). It measures what PCP-006 Version 1.0 required of the
    concentration study and S-VI-UNI did not (DEV-006-03). The step model has no concentration term in
    the inactivation (acid denaturation of the viral envelope consumes no antibody), so the results
    differ by run-to-run variation only. Aggregate and acidic variants carry the repeatability of their
    methods, as in S-VI-OFAT. Rows have the columns of ``univariate_studies`` plus ``xmulv_lrf``."""
    from .studies import _response_value, _unit
    spec = _a(cfg)["vi_concentration"]
    uo = _unit(proc, "viral_inactivation")
    p = cfg.unit_op("viral_inactivation").param(spec["parameter"])
    meth = {m["id"]: m for m in cfg.raw()["deviations"]["methods"]}
    sec_cv = float(meth["AMV-3221"]["precision_pct"]) / 100
    icief_cv = float(_a(cfg)["sdm"]["assay_cv"]["acidic_variants"])
    rows = []
    for li, (level, val) in enumerate((("low", p.prange[0]), ("high", p.prange[1]))):
        rng = _rng(cfg, 20, li)
        for rep in range(1, int(spec["replicates"]) + 1):
            feed = feeds.get("viral_inactivation")
            res = uo.run(None if feed is None else feed.copy(), rng, setpoints={p.key: float(val)})
            agg = _response_value(res, "aggregate_out_pct") * float(np.exp(rng.normal(0.0, sec_cv)))
            acid = _response_value(res, "acidic_variants") * float(np.exp(rng.normal(0.0, icief_cv)))
            rows.append({"study": spec["study"], "step": "viral_inactivation", "parameter": p.key,
                         "level": level, "value": float(val), "replicate": rep,
                         "aggregate_out_pct": agg, "acidic_variants": acid,
                         "xmulv_lrf": float(res.metrics["xmulv_lrf"])})
    return pd.DataFrame(rows)


def _position(cfg: Config, step: str, param: str, pos: str) -> float:
    """A named position of a parameter, in force: ``range_low``/``range_high`` (the range studied),
    ``nor_low``/``nor_high`` (the NOR in force) or ``setpoint`` (the set-point in force)."""
    p = cfg.unit_op(step).param(param)
    return float({"range_low": p.prange[0], "range_high": p.prange[1], "nor_low": p.nor[0],
                  "nor_high": p.nor[1], "setpoint": p.setpoint}[pos])


def _vi_cex_runs(cfg: Config, proc, feeds, n: int, study: str, lf: Dict[str, float],
                 key: int) -> pd.DataFrame:
    """``n`` runs of the low-pH hold at the settings ``lf``, each followed by a cation exchange run at
    set-point on its own material, from the stream ``key``. The hold output (aggregate, fragments by
    nrCE-SDS, acidic variants) is the load of the cation exchange run."""
    from .studies import _response_value, _unit
    vi, cx = _unit(proc, "viral_inactivation"), _unit(proc, "cex")
    nom = nominal_train(cfg)
    icief_cv = float(_a(cfg)["sdm"]["assay_cv"]["acidic_variants"])
    rows = []
    for i in range(int(n)):
        rng = _rng(cfg, key, i)
        vres = vi.run(feeds["viral_inactivation"].copy(), rng, setpoints={k: float(x) for k, x in lf.items()})
        load = vres.out.copy()
        cres = cx.run(load.copy(), rng)
        frag_load = float(frag_vi(cfg, nom["protein_a"], lf["hold_time"], lf["temperature"]))
        frag_pool = float(frag_cex(cfg, frag_load))
        fl, fp = measure(cfg, "cesds", np.array([frag_load, frag_pool]), rng)
        # acidic variants of the hold output carry the icIEF repeatability, as in S-VI-OFAT (the step
        # model gives them without noise); drawn last, so no value above moves
        acid = float(load.cqas["acidic_variants"]) * float(np.exp(rng.normal(0.0, icief_cv)))
        rows.append({"study": study, "run": i + 1,
                     "load_aggregate_pct": float(load.cqas["aggregates_hmw"]),
                     "aggregate_out_pct": _response_value(cres, "aggregate_out_pct"),
                     "hcp_out_ng_mg": _response_value(cres, "hcp_out_ng_mg"),
                     "step_yield": float(cres.step_yield),
                     "load_lmw_cesds_pct": float(fl), LMW_CE: float(fp),
                     "load_acidic_variants": acid})
    out = pd.DataFrame(rows)
    out["aggregate_fold"] = out["load_aggregate_pct"] / out["aggregate_out_pct"]
    out["fragment_fold"] = out["load_lmw_cesds_pct"] / out[LMW_CE]
    return out


def cex_verification(cfg: Config, proc, feeds, n: int) -> pd.DataFrame:
    """S-CEX-VER: ``n`` cation exchange runs at set-point on the worst-case material of the
    re-centred low-pH step (``analytics.cex_verification.load_from``), from their own stream
    (key 16): each run inactivates its own load and purifies it. Aggregate as the step models give
    it; fragments from the fragment model, measured by nrCE-SDS on load and pool."""
    v = _a(cfg)["cex_verification"]
    return _vi_cex_runs(cfg, proc, feeds, n, v["study"], v["load_from"], 16)


def vi_worst_case(cfg: Config, proc, feeds, n: int) -> pd.DataFrame:
    """S-VI-WC (PD-006-03): the low-pH hold at the harshest combination within the PAR after the
    hold-time NOR was revised (``analytics.vi_worst_case.load_from``, named positions resolved in
    force), each run followed by a cation exchange run at set-point, from its own stream (key 18).
    As many runs as the cation exchange verification (``n``)."""
    w = _a(cfg)["vi_worst_case"]
    lf = {k: _position(cfg, "viral_inactivation", k, pos) for k, pos in w["load_from"].items()}
    return _vi_cex_runs(cfg, proc, feeds, n, w["study"], lf, 18)


def osmolality_runs(cfg: Config) -> int:
    """Runs per level of S-BRX-OSM: the smallest number for which the straight-line prediction at the
    highest of three equally spaced levels has a standard error of at most ``se_fraction`` of the
    run-to-run SD, that is n >= (1/3 + 1/2) / se_fraction**2 for levels coded -1, 0, +1."""
    o = _a(cfg)["osmolality_study"]
    k = len(o["levels"])
    codes = np.linspace(-1, 1, k)
    need = (1.0 / k + 1.0 / float((codes ** 2).sum())) / float(o["se_fraction"]) ** 2
    return int(np.ceil(need - 1e-9))


def osmolality_study(cfg: Config, proc, feeds) -> pd.DataFrame:
    """S-BRX-OSM (PD-003-01): osmolality at its NOR low, set-point and NOR high, with the four
    response-surface parameters at their least favourable NOR combination for acidic variants
    (``analytics.osmolality_study.at``, named positions in force), ``osmolality_runs`` cultures per
    level, from its own stream (key 19). Osmolality is set independently of pCO2 (``control``)."""
    from .studies import DOE_RESPONSES, _response_value, _unit
    o = _a(cfg)["osmolality_study"]
    uo = _unit(proc, "bioreactor")
    fac = o["factor"]
    at = {k: _position(cfg, "bioreactor", k, pos) for k, pos in o["at"].items()}
    levels = [_position(cfg, "bioreactor", fac, pos) for pos in o["levels"]]
    n = osmolality_runs(cfg)
    rows = []
    for li, lv in enumerate(levels):
        for rep in range(n):
            rng = _rng(cfg, 19, li, rep)
            res = uo.run(None, rng, setpoints={**at, fac: lv})
            row = {"study": o["study"], "level": o["levels"][li], fac: lv, "replicate": rep + 1, **at}
            for r in DOE_RESPONSES["bioreactor"]:
                row[r] = _response_value(res, r)
            rows.append(row)
    out = pd.DataFrame(rows)
    out.insert(1, "run", range(1, len(out) + 1))
    out["run_order"] = _rng(cfg, 19, 99).permutation(len(out)) + 1
    return out


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
    # the DNA of the clarified broth (process.bioreactor harvest_centre), the load of capture
    load = float(cfg.process["bioreactor"]["rsm"]["harvest_centre"]["residual_dna_pg_mg"]) * rng.lognormal(0, 0.15, len(out))
    pool = load / 10 ** (lrv + rng.normal(0, 0.15, len(out)))
    out["dna_load_pg_mg"] = np.where(centre, load, np.nan)
    out["dna_pool_pg_mg"] = np.where(centre, pool, np.nan)
    return out
