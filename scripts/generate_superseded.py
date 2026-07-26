#!/usr/bin/env python3
"""Generate the seeded *superseded* (re-executed) DoE datasets and refresh the
deterministic deviation tables — WITHOUT regenerating the nominal baselines.

Where a deviation invalidated a study and forced a full re-execution, the study was
really performed twice. This produces the invalidated first execution as a real dataset,
so the report can reference it and confirm root cause from the requalified data. Currently
that is anion exchange (Step 8), Deviation DEV-008-01 (non-representative, deamidated load).

Why a separate script (not `generate_data.py`): regenerating every output in a different
library environment silently drifts the DoE/effects CSVs in the deep decimals. This writes
only NEW files (`doe_<key>_<kind>_superseded.csv`) plus the deterministic, RNG-free
deviation tables (`deviations.csv`, `dev_*.csv`) and patches the `dev_scalars` /
`n_deviations` entries of `report_values.json` in place. `git diff outputs/` after running
must show only intended additions.

    uv run python scripts/generate_superseded.py
"""
from __future__ import annotations

import json
import os
import sys
import warnings

import numpy as np

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from amab_process import Process, load_config      # noqa: E402
from amab_process import studies as st              # noqa: E402
from amab_process import deviations as dv           # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "outputs", "data")
RV = os.path.join(ROOT, "outputs", "report_values.json")


def _superseded_events(cfg):
    """Yield (doc_id, event) for every deviation carrying a `superseded` block."""
    events = (cfg.raw().get("deviations", {}) or {}).get("events", {}) or {}
    for doc_id, evs in events.items():
        for ev in evs:
            if ev.get("superseded"):
                yield doc_id, ev


def main() -> None:
    cfg = load_config()
    proc = Process(cfg)
    feeds = st.step_feeds(proc)
    print(f"A-Mab superseded-study generation — seed={cfg.seed}")

    n_new = 0
    for doc_id, ev in _superseded_events(cfg):
        key = ev["step"]
        sup = ev["superseded"]
        deam = {"corner": float(sup["hcp_deam_corner_coef"])}
        top = st.RSM_TOP.get(key, st.DOE_FACTORS[key][:4])
        rng = proc.rng(int(sup.get("seed_offset", 800)))  # dedicated, reproducible stream
        for kind in sup.get("kinds", ["screening", "rsm"]):
            df = st.superseded_doe(proc, key, feeds[key], rng, kind, deam, top_factors=top)
            path = os.path.join(DATA, f"doe_{key}_{kind}_superseded.csv")
            df.to_csv(path, index=False)
            n_new += 1
            print(f"  wrote doe_{key}_{kind}_superseded.csv  ({len(df)} runs) — {ev['id']}")

    # deterministic deviation tables (RNG-free) — additive, safe to rewrite
    devbuild = dv.build(cfg)
    for name, tbl in devbuild["tables"].items():
        tbl.to_csv(os.path.join(DATA, name), index=False)
    print(f"  refreshed {len(devbuild['tables'])} deviation table(s) "
          f"({len(devbuild['tables']['deviations.csv'])} events)")

    # patch report_values.json in place: dev_scalars + n_deviations only
    with open(RV) as fh:
        values = json.load(fh)
    values["dev_scalars"] = devbuild["scalars"]
    values["n_deviations"] = int(len(devbuild["tables"]["deviations.csv"]))
    with open(RV, "w") as fh:
        json.dump(values, fh, indent=2)
    print(f"  patched report_values.json (dev_scalars, n_deviations)")

    # sanity: show the anomalous BD interaction the superseded data must carry
    import doe_report as D  # imported after outputs are written
    for doc_id, ev in _superseded_events(cfg):
        key = ev["step"]
        if key != "aex":
            continue
        sup_eff = D.screening_effects_df(key, "hcp_out_ng_mg", superseded=True)
        nom_eff = D.screening_effects_df(key, "hcp_out_ng_mg", superseded=False)
        def _bd_p(dfe):
            row = dfe[dfe.Term.isin(["BD", "DB"])]
            return float(row["p-value"].iloc[0]) if len(row) else float("nan")
        print(f"\n  {ev['id']} root-cause check (protein-load × wash-1-conductivity, BD):")
        print(f"    superseded (deamidated)  p(BD) = {_bd_p(sup_eff):.4g}  <- should be significant")
        print(f"    requalified (reported)   p(BD) = {_bd_p(nom_eff):.4g}  <- should be non-significant")

    print(f"\n{n_new} superseded dataset(s) written. `git diff outputs/` and commit only intended additions.")


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(ROOT, "pc_package"))  # for doe_report in the sanity check
    main()
