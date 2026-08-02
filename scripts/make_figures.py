#!/usr/bin/env python3
"""Render every figure in the process characterization report.

Reads the datasets in ``outputs/data/`` (produced by ``generate_data.py``) and
the process model, and writes PNGs to ``outputs/figures/`` plus a manifest.
Design-space and response-surface contours are built from the fitted response-
surface (CCD) models — the standard QbD presentation — while set-points, NORs
and acceptance limits come from the configuration.

Usage:  python scripts/make_figures.py
"""

from __future__ import annotations

import json
import os
import sys
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from amab_process import Process, load_config          # noqa: E402
from amab_process import studies as st                  # noqa: E402
from amab_process import viz                            # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "outputs", "data")
FIGS = os.path.join(ROOT, "outputs", "figures")
os.makedirs(FIGS, exist_ok=True)
viz.apply_style()

CFG = load_config()
PROC = Process(CFG)
MANIFEST: dict = {}


def load(name: str) -> pd.DataFrame:
    return pd.read_csv(os.path.join(DATA, name))


def out(fig, name: str, caption: str) -> None:
    path = os.path.join(FIGS, name)
    viz.savefig(fig, path)
    MANIFEST[name] = caption
    print(f"  {name:38s} {caption[:60]}")


def _ranges(key, factors):
    uo = CFG.unit_op(key)
    return {f: uo.param(f).prange for f in factors}


def _natural(coded, lo, hi):
    return 0.5 * (lo + hi) + coded * 0.5 * (hi - lo)


def rsm_model(ccd: pd.DataFrame, response: str, factors, quad=True):
    return st.fit_effects(ccd, response, factors, quadratic=quad)["model"]


def predict_grid(model, factors, xf, yf, XXc, YYc):
    d = {f: np.zeros(XXc.size) for f in factors}
    d[xf] = XXc.ravel()
    d[yf] = YYc.ravel()
    return np.asarray(model.predict(pd.DataFrame(d))).reshape(XXc.shape)


# ============================================================ 1. process flow
def fig_process_flow():
    steps = [(CFG.unit_op(k).step, CFG.unit_op(k).name) for k in CFG.train_order]
    labels = ["Production\nBioreactor", "Harvest /\nClarification", "Protein A\nCapture",
              "Low-pH Viral\nInactivation", "Cation\nExchange\n(CEX)", "Anion\nExchange\n(AEX)",
              "Virus\nFiltration", "UF/DF\n(Formulation)"]
    notes = ["Glycans, aggregate,\nHCP, DNA formed", "clarify", "HCP↓, DNA↓,\nleached Prot.A↑",
             "XMuLV ↓↓\naggregate ↑", "aggregate ↓↓\nHCP ↓", "HCP ↓, DNA ↓\nXMuLV/MVM ↓",
             "MVM/XMuLV ↓", "concentrate\nto 75 g/L"]
    fig, ax = plt.subplots(figsize=(12, 3.2))
    n = len(labels)
    w, h, gap = 1.0, 1.0, 0.75
    for i, (lab, note) in enumerate(zip(labels, notes)):
        x = i * (w + gap)
        color = viz.CATEGORICAL[0] if i in (0,) else (viz.STATUS["serious"] if i in (3, 6) else viz.CATEGORICAL[4])
        box = FancyBboxPatch((x, 0), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                             linewidth=1.2, edgecolor="#c3c2b7", facecolor="#eef4fb")
        ax.add_patch(box)
        ax.text(x + w / 2, h / 2 + 0.15, lab, ha="center", va="center", fontsize=7.8, weight="bold", color=viz.INK)
        ax.text(x + w / 2, h / 2 - 0.36, f"Step {steps[i][0]}", ha="center", va="center", fontsize=6.8, color=viz.MUTED)
        ax.text(x + w / 2, -0.42, note, ha="center", va="top", fontsize=6.6, color=viz.INK2)
        if i < n - 1:
            ax.add_patch(FancyArrowPatch((x + w, h / 2), (x + w + gap, h / 2),
                                         arrowstyle="-|>", mutation_scale=11, color=viz.MUTED, lw=1.2))
    ax.set_xlim(-0.3, n * (w + gap) - gap + 0.3)
    ax.set_ylim(-1.05, 1.2)
    ax.axis("off")
    ax.set_title("A-Mab drug-substance process train", loc="left")
    out(fig, "fig_process_flow.png", "A-Mab drug-substance process flow (Steps 3-10) with the principal quality impact of each unit operation.")


# ============================================================ 2. bioreactor kinetics
def fig_bioreactor_timecourse():
    tc = load("nominal_timecourse.csv")
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.2))
    axes[0].plot(tc.day, tc.vcd, color=viz.CATEGORICAL[0], lw=2, marker="o", ms=4, label="Total VCD")
    axes[0].plot(tc.day, tc.viable_cell_conc, color=viz.CATEGORICAL[4], lw=2, marker="s", ms=3, label="Viable cell conc.")
    axes[0].set_ylabel("cells (×10⁶/mL)"); axes[0].set_title("Cell growth"); axes[0].legend(fontsize=8)
    axes[1].plot(tc.day, tc.viability, color=viz.CATEGORICAL[5], lw=2, marker="o", ms=4)
    axes[1].set_ylabel("viability (%)"); axes[1].set_title("Culture viability"); axes[1].set_ylim(0, 100)
    axes[2].plot(tc.day, tc.titer, color=viz.CATEGORICAL[1], lw=2, marker="o", ms=4)
    axes[2].set_ylabel("titer (g/L)"); axes[2].set_title("Product titer")
    for a in axes:
        a.set_xlabel("culture day")
    fig.suptitle("Production bioreactor — nominal fed-batch profile (set-point operation)", x=0.02, ha="left", weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    out(fig, "fig_bioreactor_timecourse.png", "Nominal production-bioreactor time course: viable cell density, viability and titer over the fed-batch culture.")


# ============================================================ 3. bioreactor Pareto
def fig_bioreactor_pareto():
    eff = load("effects_bioreactor.csv")
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))
    for ax, resp, title in [(axes[0], "afucosylation", "Afucosylation"),
                            (axes[1], "galactosylation", "Galactosylation")]:
        d = eff[eff.response == resp].copy().head(8).iloc[::-1]
        colors = [viz.STATUS["critical"] if p < 0.05 else viz.MUTED for p in d.p_value]
        ax.barh(range(len(d)), d.effect.abs(), color=colors)
        ax.set_yticks(range(len(d)))
        ax.set_yticklabels([t.replace(":", "×") for t in d.term], fontsize=8)
        ax.set_xlabel("|effect| (% per coded unit)")
        ax.set_title(title)
    fig.suptitle("Bioreactor screening DoE — standardized effects (red = significant, p < 0.05)", x=0.02, ha="left", weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    out(fig, "fig_bioreactor_pareto.png", "Pareto of standardized main and interaction effects from the bioreactor screening DoE for afucosylation and galactosylation.")


# ============================================================ 4. bioreactor design space
def fig_bioreactor_designspace():
    ccd = load("doe_bioreactor_rsm.csv")
    factors = st.RSM_TOP["bioreactor"]
    xf, yf = "pH", "duration"
    rng = _ranges("bioreactor", factors)
    models = {r: rsm_model(ccd, r, factors) for r in ["afucosylation", "galactosylation", "high_mannose", "acidic_variants", "aggregates_hmw"]}
    gc = np.linspace(-1, 1, 80)
    XXc, YYc = np.meshgrid(gc, gc)
    Xn = _natural(XXc, *rng[xf]); Yn = _natural(YYc, *rng[yf])
    Z = {r: predict_grid(m, factors, xf, yf, XXc, YYc) for r, m in models.items()}
    acc = {c["key"]: c["acceptance"] for c in CFG.cqas}
    inspec = np.ones_like(XXc, dtype=bool)
    for r, z in Z.items():
        lo, hi = acc[r]
        # honour the CQA's spec type, as doe_report.meets_acceptance does: an upper-only
        # attribute is not out of spec below the range-of-experience floor.
        stype = st.spec_type(r)
        if stype != "lower":
            inspec &= (z <= hi)
        if stype != "upper":
            inspec &= (z >= lo)

    fig, ax = plt.subplots(figsize=(6.4, 5.0))
    ax.contourf(Xn, Yn, inspec.astype(float), levels=[0.5, 1.5], colors=[viz.STATUS["good"]], alpha=0.16)
    cs = ax.contour(Xn, Yn, Z["afucosylation"], levels=6, colors=viz.CATEGORICAL[0], linewidths=1.0)
    ax.clabel(cs, inline=True, fontsize=7, fmt="%.0f")
    for r, col in [("afucosylation", viz.CATEGORICAL[0]), ("galactosylation", viz.CATEGORICAL[1])]:
        for bound in acc[r]:
            ax.contour(Xn, Yn, Z[r], levels=[bound], colors=[viz.STATUS["critical"]], linewidths=1.8, linestyles="--")
    pH = CFG.unit_op("bioreactor").param("pH"); dur = CFG.unit_op("bioreactor").param("duration")
    ax.add_patch(plt.Rectangle((pH.nor[0], dur.nor[0]), pH.nor[1] - pH.nor[0], dur.nor[1] - dur.nor[0],
                               fill=False, edgecolor=viz.INK, lw=1.5, ls=":", label="NOR"))
    ax.plot(pH.setpoint, dur.setpoint, "o", color=viz.INK, ms=8, label="Set-point")
    ax.set_xlabel("culture pH"); ax.set_ylabel("culture duration (days)")
    ax.set_title("Bioreactor design space (pH × duration)\nblue = afucosylation contours; green shade = all CQAs in-spec")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(False)
    out(fig, "fig_bioreactor_designspace.png", "Production-bioreactor design space in the pH × culture-duration plane; the shaded region satisfies all cell-culture CQAs simultaneously (dashed red = acceptance boundaries).")


# ============================================================ 5. Protein A HCP RSM
def fig_protein_a_hcp():
    ccd = load("doe_protein_a_rsm.csv")
    factors = ["load", "elution_ph", "flow", "end_collect"]
    xf, yf = "load", "elution_ph"
    rng = _ranges("protein_a", factors)
    model = rsm_model(ccd, "pool_hcp_ng_mg", factors)
    gc = np.linspace(-1, 1, 80); XXc, YYc = np.meshgrid(gc, gc)
    Xn = _natural(XXc, *rng[xf]); Yn = _natural(YYc, *rng[yf])
    Z = predict_grid(model, factors, xf, yf, XXc, YYc)
    fig, ax = plt.subplots(figsize=(6.4, 5.0))
    cf = ax.contourf(Xn, Yn, Z, levels=12, cmap="Blues")
    cs = ax.contour(Xn, Yn, Z, levels=8, colors="white", linewidths=0.7)
    ax.clabel(cs, inline=True, fontsize=7, fmt="%.0f")
    fig.colorbar(cf, ax=ax, label="pool HCP (ng/mg)")
    p = CFG.unit_op("protein_a")
    ax.plot(p.param("load").setpoint, p.param("elution_ph").setpoint, "o", color=viz.INK, ms=8, label="Set-point")
    ax.set_xlabel("protein load (g/L resin)"); ax.set_ylabel("elution pH")
    ax.set_title("Protein A — pool HCP response surface\n(HCP rises at high load and low elution pH)")
    ax.legend(fontsize=8); ax.grid(False)
    out(fig, "fig_protein_a_hcp.png", "Protein A pool HCP response surface (load × elution pH); HCP increases with higher protein load and lower elution pH, reproducing A-Mab Figure 4.2.")


# ============================================================ 6. VI aggregate + design space
def fig_vi_aggregate():
    scr = load("doe_viral_inactivation_screening.csv")
    p = CFG.unit_op("viral_inactivation")
    # aggregate vs hold time at low/high temperature from the model
    feeds = st.step_feeds(PROC)
    times = np.linspace(0, 240, 40)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.0))
    ax = axes[0]
    for temp, col, lab in [(15, viz.CATEGORICAL[0], "15 °C"), (25, viz.CATEGORICAL[5], "25 °C")]:
        agg = []
        for t in times:
            res = dict(PROC.units)["viral_inactivation"].run(
                feeds["viral_inactivation"].copy(), PROC.rng(7),
                setpoints={"hold_time": t, "temperature": temp, "ph": p.param("ph").setpoint})
            agg.append(res.metrics["aggregate_out_pct"])
        ax.plot(times, agg, color=col, lw=2, label=lab)
    viz.nor_band(ax, *p.param("hold_time").nor, setpoint=p.param("hold_time").setpoint, vertical=True)
    ax.axvline(180, color=viz.MUTED, ls="-.", lw=1, label="max hold 180 min")
    ax.set_xlabel("hold time (min)"); ax.set_ylabel("aggregate, HMW (%)")
    ax.set_title("Aggregate vs hold time"); ax.legend(fontsize=8)

    # XMuLV LRF vs pH and time -> design space
    ax = axes[1]
    phs = np.linspace(3.2, 4.0, 60); ts = np.linspace(30, 180, 60)
    PH, T = np.meshgrid(phs, ts)
    lrf = np.zeros_like(PH)
    for i in range(PH.shape[0]):
        for j in range(PH.shape[1]):
            res = dict(PROC.units)["viral_inactivation"].run(
                feeds["viral_inactivation"].copy(), PROC.rng(7),
                setpoints={"ph": PH[i, j], "hold_time": T[i, j], "temperature": 21})
            lrf[i, j] = res.metrics["xmulv_lrf"]
    cf = ax.contourf(PH, T, lrf, levels=12, cmap="Blues")
    ax.contour(PH, T, lrf, levels=[6.0], colors=[viz.STATUS["critical"]], linewidths=2, linestyles="--")
    fig.colorbar(cf, ax=ax, label="XMuLV LRF (log₁₀)")
    ax.plot(p.param("ph").setpoint, p.param("hold_time").setpoint, "o", color=viz.INK, ms=8, label="Set-point")
    ax.set_xlabel("inactivation pH"); ax.set_ylabel("hold time (min)")
    ax.set_title("XMuLV inactivation (dashed = 6.0 log floor)"); ax.legend(fontsize=8); ax.grid(False)
    fig.suptitle("Low-pH viral inactivation — product quality and viral clearance", x=0.02, ha="left", weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    out(fig, "fig_vi_aggregate.png", "Low-pH viral inactivation: aggregate formation vs hold time at 15/25 °C (left) and the XMuLV log-reduction surface over pH × hold time (right).")


# ============================================================ 7. CEX contours
def fig_cex():
    ccd = load("doe_cex_rsm.csv")
    factors = ["load", "wash_cond", "elution_ph", "stop_collect"]
    rng = _ranges("cex", factors)
    gc = np.linspace(-1, 1, 70); XXc, YYc = np.meshgrid(gc, gc)
    xf, yf = "load", "wash_cond"
    Xn = _natural(XXc, *rng[xf]); Yn = _natural(YYc, *rng[yf])
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for ax, resp, lab, cmap in [(axes[0], "hcp_out_ng_mg", "pool HCP (ng/mg)", "Blues"),
                                (axes[1], "aggregate_out_pct", "aggregate, HMW (%)", "Greens")]:
        Z = predict_grid(rsm_model(ccd, resp, factors), factors, xf, yf, XXc, YYc)
        cf = ax.contourf(Xn, Yn, Z, levels=12, cmap=cmap)
        cs = ax.contour(Xn, Yn, Z, levels=8, colors="white", linewidths=0.6); ax.clabel(cs, inline=True, fontsize=7, fmt="%.1f")
        fig.colorbar(cf, ax=ax, label=lab)
        p = CFG.unit_op("cex")
        ax.plot(p.param("load").setpoint, p.param("wash_cond").setpoint, "o", color=viz.INK, ms=7)
        ax.set_xlabel("protein load (g/L resin)"); ax.set_ylabel("load/wash conductivity (mS/cm)"); ax.grid(False)
    axes[0].set_title("HCP clearance"); axes[1].set_title("Aggregate clearance")
    fig.suptitle("Cation exchange (CEX) — response surfaces (load × wash conductivity)", x=0.02, ha="left", weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    out(fig, "fig_cex.png", "CEX response surfaces for pool HCP and aggregate over protein load × load/wash conductivity.")


# ============================================================ 8. AEX HCP + viral
def fig_aex():
    ccd = load("doe_aex_rsm.csv")
    factors = st.RSM_TOP["aex"]
    rng = _ranges("aex", factors)
    gc = np.linspace(-1, 1, 70); XXc, YYc = np.meshgrid(gc, gc)
    p = CFG.unit_op("aex")
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    # HCP driven by load pH × Equil/Wash-1 conductivity; viral clearance by load pH × load conductivity.
    panels = [(axes[0], "hcp_out_ng_mg", "pool HCP (ng/mg)", "Blues", "wash1_cond", "Equil/Wash-1 conductivity (mS/cm)"),
              (axes[1], "xmulv_lrf", "XMuLV LRF (log₁₀)", "Purples", "load_cond", "load conductivity (mS/cm)")]
    for ax, resp, lab, cmap, yf, ylab in panels:
        Xn = _natural(XXc, *rng["load_ph"]); Yn = _natural(YYc, *rng[yf])
        Z = predict_grid(rsm_model(ccd, resp, factors), factors, "load_ph", yf, XXc, YYc)
        cf = ax.contourf(Xn, Yn, Z, levels=12, cmap=cmap)
        cs = ax.contour(Xn, Yn, Z, levels=7, colors="white", linewidths=0.6); ax.clabel(cs, inline=True, fontsize=7, fmt="%.1f")
        fig.colorbar(cf, ax=ax, label=lab)
        ax.plot(p.param("load_ph").setpoint, p.param(yf).setpoint, "o", color=viz.INK, ms=7)
        ax.set_xlabel("load pH"); ax.set_ylabel(ylab); ax.grid(False)
    axes[0].set_title("HCP clearance (load pH × Equil/Wash-1 cond.)")
    axes[1].set_title("XMuLV clearance (load pH × load cond.)")
    fig.suptitle("Anion exchange (AEX) — HCP and viral clearance", x=0.02, ha="left", weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    out(fig, "fig_aex.png", "AEX response surfaces: HCP clearance falls as load pH decreases and Equil/Wash-1 conductivity increases; XMuLV log-reduction falls as load pH decreases and load conductivity increases.")


# ============================================================ 9. VF MVM vs volume
def fig_vf():
    p = CFG.unit_op("virus_filtration")
    feeds = st.step_feeds(PROC)
    vols = np.linspace(50, 140, 60)
    mvm = []
    for v in vols:
        res = dict(PROC.units)["virus_filtration"].run(feeds["virus_filtration"].copy(), PROC.rng(9),
                                                       setpoints={"filtration_volume": v})
        mvm.append(res.metrics["mvm_lrf"])
    # NO ACCEPTANCE LINE IS DRAWN HERE, deliberately. This figure used to draw a spec line
    # at 4.62 labelled "4.62 log floor", with a caption asserting that the load limit
    # preserves LRF >= 4.62. Both numbers were typed, and the 4.62 is not this model's
    # acceptance floor at all: it is an observation from the A-Mab case study (LRV >= 4.62
    # for load <= 105 L/m2, p.152-166), recorded in the comment above this unit operation in
    # config/parameters.yaml. The step's actual requirement is back-calculated from the
    # cumulative viral-clearance requirement less the clearance credited to the other steps,
    # which gives 3.89 log10 for MVM — so the figure was presenting prior knowledge as a
    # specification and overstating the floor by 0.73 log10. The back-calculation lives in
    # doe_report.acceptance_for and belongs to the report, not to a figure script.
    nor_lo, nor_hi = p.param("filtration_volume").nor
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    ax.plot(vols, mvm, color=viz.CATEGORICAL[6], lw=2.2, label="MVM LRF")
    viz.nor_band(ax, nor_lo, nor_hi, setpoint=p.param("filtration_volume").setpoint, vertical=True)
    ax.axvline(nor_hi, color=viz.MUTED, ls="-.", lw=1, label=f"{nor_hi:g} L/m² limit")
    ax.set_xlabel("filtration volume / load (L/m²)"); ax.set_ylabel("MVM log-reduction (log₁₀)")
    ax.set_title("Virus filtration — MVM clearance vs volumetric load"); ax.legend(fontsize=8)
    out(fig, "fig_vf.png",
        f"Small-virus filtration: MVM log-reduction declines with volumetric load, and the "
        f"normal operating range is bounded at {nor_hi:g} L/m². The step acceptance floor is "
        f"back-calculated in PCR-009 from the cumulative requirement and the clearance "
        f"credited to the other steps; it is not drawn here.")


# ============================================================ 10. viral clearance bar
def fig_viral_clearance():
    vc = load("viral_clearance.csv")
    steps = vc[vc.step != "Cumulative"]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.0))
    for ax, virus, req, col in [(axes[0], "XMuLV", 16.7, viz.CATEGORICAL[0]),
                                (axes[1], "MVM", 8.6, viz.CATEGORICAL[6])]:
        bottoms = 0.0
        for _, r in steps.iterrows():
            ax.bar("cumulative", r[virus], bottom=bottoms, label=r.step, width=0.55)
            bottoms += r[virus]
        ax.axhline(req, color=viz.STATUS["critical"], ls="--", lw=1.6, label=f"requirement > {req}")
        ax.text(0, bottoms + 0.3, f"Σ = {bottoms:.1f}", ha="center", fontsize=9, weight="bold")
        ax.set_ylabel(f"{virus} log-reduction (log₁₀)"); ax.set_title(virus)
        ax.set_xticks([])
    axes[1].legend(fontsize=7, loc="upper right")
    fig.suptitle("Cumulative viral clearance vs regulatory requirement", x=0.02, ha="left", weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    out(fig, "fig_viral_clearance.png", "Modular viral clearance by step for XMuLV and MVM; cumulative clearance exceeds the total requirement with margin.")


# ============================================================ 11. capability panels
def fig_capability():
    mc = load("monte_carlo.csv"); cap = load("capability.csv")
    keys = ["afucosylation", "galactosylation", "high_mannose", "aggregates_hmw", "hcp", "acidic_variants"]
    fig, axes = plt.subplots(2, 3, figsize=(11, 6.0))
    for ax, key in zip(axes.ravel(), keys):
        c = CFG.cqa(key); row = cap[cap.key == key].iloc[0]
        ax.hist(mc[key], bins=40, color=viz.SEQUENTIAL[3], alpha=0.85)
        lo, hi = c["acceptance"]
        if st.spec_type(key) != "lower":
            if st.spec_type(key) == "two_sided":
                ax.axvline(lo, color=viz.STATUS["critical"], ls="--", lw=1.4)
            ax.axvline(hi, color=viz.STATUS["critical"], ls="--", lw=1.4)
        ax.axvline(mc[key].mean(), color=viz.INK, ls=":", lw=1.2)
        ax.set_title(f"{c['name'][:26]}  (Cpk {row.Cpk:.2f})", fontsize=9)
        ax.set_xlabel(c["unit"]); ax.grid(axis="y")
    fig.suptitle(f"Commercial-scale process capability (n = {len(mc)} simulated batches)", x=0.02, ha="left", weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    out(fig, "fig_capability.png", "Monte-Carlo drug-substance CQA distributions vs acceptance limits, annotated with process capability (Cpk).")


# ============================================================ 12. yield waterfall
def fig_yield_waterfall():
    wf = load("yield_waterfall.csv").sort_values("step")
    fig, ax = plt.subplots(figsize=(9.5, 4.0))
    ax.plot(range(len(wf)), wf.cumulative_yield * 100, color=viz.CATEGORICAL[0], lw=2, marker="o")
    for i, r in enumerate(wf.itertuples()):
        ax.annotate(f"{r.cumulative_yield*100:.0f}%", (i, r.cumulative_yield * 100),
                    textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8)
    ax.set_xticks(range(len(wf)))
    ax.set_xticklabels([n.split(" (")[0].replace(" Chromatography", "") for n in wf.unit_operation],
                       rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("cumulative step yield (%)"); ax.set_ylim(0, 105)
    ax.set_title("Cumulative product yield across the drug-substance train")
    out(fig, "fig_yield_waterfall.png", "Cumulative product step-yield across the eight modelled unit operations.")


# ============================================================ 13. parameter classification
def fig_param_classification():
    preg = load("parameter_classification.csv")
    order = ["CPP", "WC-CPP", "KPP", "GPP", "non-CPP"]
    ct = preg.groupby(["unit_operation", "classification"]).size().unstack(fill_value=0)
    ct = ct.reindex(columns=[c for c in order if c in ct.columns])
    steps = [CFG.unit_op(k).name for k in CFG.train_order if CFG.unit_op(k).name in ct.index]
    ct = ct.reindex(steps)
    colors = {"CPP": viz.STATUS["critical"], "WC-CPP": viz.STATUS["serious"],
              "KPP": viz.CATEGORICAL[3], "GPP": viz.CATEGORICAL[4], "non-CPP": viz.MUTED}
    fig, ax = plt.subplots(figsize=(10, 4.4))
    left = np.zeros(len(ct))
    for cls in ct.columns:
        ax.barh(range(len(ct)), ct[cls], left=left, color=colors.get(cls, viz.MUTED), label=cls)
        left += ct[cls].values
    ax.set_yticks(range(len(ct)))
    ax.set_yticklabels([s.split(" (")[0] for s in ct.index], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("number of process parameters"); ax.legend(fontsize=8, ncol=5, loc="lower right")
    ax.set_title("Process-parameter classification by unit operation"); ax.grid(axis="x")
    out(fig, "fig_param_classification.png", "Post-characterization classification of process parameters (CPP / WC-CPP / KPP / GPP) by unit operation.")


def main():
    print("Rendering figures ...")
    for f in [fig_process_flow, fig_bioreactor_timecourse, fig_bioreactor_pareto,
              fig_bioreactor_designspace, fig_protein_a_hcp, fig_vi_aggregate, fig_cex,
              fig_aex, fig_vf, fig_viral_clearance, fig_capability, fig_yield_waterfall,
              fig_param_classification]:
        f()
    with open(os.path.join(ROOT, "outputs", "figure_manifest.json"), "w") as fh:
        json.dump(MANIFEST, fh, indent=2)
    print(f"\n{len(MANIFEST)} figures -> outputs/figures/  (+ figure_manifest.json)")


if __name__ == "__main__":
    main()
