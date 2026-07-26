"""Seeded 'messy-campaign' facts: deviations and their supporting records.

Real characterization campaigns are long partly because real campaigns are
messy — excursions, expired lots, drifted probes, re-assays. The clean simulated
process in :mod:`amab_process` emits none of that, so the narrated-deviation
sections of the reports (the ``ema_docgen`` density pass) had nothing true to
say. This module supplies those facts.

They are *recorded events*, not random draws, so they live as fixed constants in
``config/parameters.yaml`` under the top-level ``deviations`` key; this module
only reshapes them into tables plus a flat scalar map. It is therefore fully
deterministic (no RNG) and seed-independent: re-running reproduces byte-identical
output, and changing ``meta.seed`` leaves the deviations unchanged.

Scalar naming (single, uniform rule so the fact packs and the documents agree)::

    scalar = <id>.lower().replace('-', '_') + '_' + <field>

e.g. ``DEV-007-02`` + ``tmax`` -> ``dev_007_02_tmax``; ``LOT-BUF-2287`` +
``expiry`` -> ``lot_buf_2287_expiry``; ``AMV-3221`` + ``precision`` ->
``amv_3221_precision``. The scalars are written to
``outputs/report_values.json`` and exposed as inline-expression names by
``pc_package/_pcpkg.py``.
"""
from __future__ import annotations

import math
from typing import Any, Dict

import pandas as pd
from scipy import stats

# analytical-method config field -> scalar suffix
_METHOD_SUFFIX = {
    "precision_pct": "precision",
    "loq": "loq",
    "variance_fraction": "var_frac",
    "accuracy_pct": "accuracy",
}


def _base(rec_id: str) -> str:
    """Normalise a record ID to its scalar-name stem (``DEV-007-02`` -> ``dev_007_02``)."""
    return str(rec_id).lower().replace("-", "_")


def _t_975(df: int) -> float:
    """Two-sided 95% Student-t quantile for ``df`` degrees of freedom."""
    return float(stats.t.ppf(0.975, df))


def build(cfg) -> Dict[str, Any]:
    """Reshape the ``deviations`` config into tables + a flat scalar map.

    Returns ``{"tables": {filename: DataFrame}, "scalars": {name: value}}``.
    ``scalars`` values are floats or ISO date strings, keyed by the uniform
    naming rule above.
    """
    d = cfg.raw().get("deviations", {}) or {}
    methods = d.get("methods", []) or []
    equipment = d.get("equipment", []) or []
    lots = d.get("lots", []) or []
    prior_docs = d.get("prior_docs", []) or []
    events = d.get("events", {}) or {}

    scalars: Dict[str, Any] = {}

    # -- supporting records -------------------------------------------------- #
    for m in methods:
        b = _base(m["id"])
        for field, suffix in _METHOD_SUFFIX.items():
            if field in m:
                scalars[f"{b}_{suffix}"] = m[field]
    for e in equipment:
        if "cal_due" in e:
            scalars[f"{_base(e['id'])}_cal_due"] = e["cal_due"]
    for lot in lots:
        if "expiry" in lot:
            scalars[f"{_base(lot['id'])}_expiry"] = lot["expiry"]

    method_precision = {m["id"]: m.get("precision_pct") for m in methods}

    # -- deviation events ---------------------------------------------------- #
    dev_rows = []
    for doc_id, evs in events.items():
        for ev in evs:
            b = _base(ev["id"])
            vals = dict(ev.get("values", {}) or {})
            # Derived multi-hop fact: relative 95% CI half-width (%) of the
            # verification set, from the linked method precision and n.
            if "ver_n" in vals and ev.get("method") in method_precision:
                n = int(vals["ver_n"])
                prec = method_precision[ev["method"]]
                if n > 1 and prec:
                    vals["ci_hw"] = round(_t_975(n - 1) * prec / math.sqrt(n), 2)
            for k, v in vals.items():
                scalars[f"{b}_{k}"] = v
            dev_rows.append({
                "doc_id": doc_id,
                "dev_id": ev["id"],
                "step": ev.get("step", ""),
                "type": ev.get("type", "deviation"),
                "summary": ev.get("summary", ""),
                "detected_during": ev.get("detected_during", ""),
                "root_cause": ev.get("root_cause", ""),
                "disposition": ev.get("disposition", ""),
                "lot": ev.get("lot", ""),
                "equipment": ev.get("equipment", ""),
                "method": ev.get("method", ""),
                "prior_doc": ev.get("prior_doc", ""),
            })

    tables = {
        "deviations.csv": pd.DataFrame(dev_rows),
        "dev_methods.csv": pd.DataFrame(methods),
        "dev_equipment.csv": pd.DataFrame(equipment),
        "dev_lots.csv": pd.DataFrame(lots),
        "dev_prior_docs.csv": pd.DataFrame(prior_docs),
    }
    return {"tables": tables, "scalars": scalars}
