# probe-setup.py -- the SETUP chunk of the probe file. Code only: the scalars, tables and
# figures the two subsections may quote as inline expressions. Extracted 2026-08-18 from the
# shipped PCR-005 setup chunk so that the probe and the shipped excerpt compute the same numbers.
import sys, os
sys.path.insert(0, os.path.abspath("."))
from _pcpkg import *  # noqa: F401,F403
import doe_report as D
import matplotlib.pyplot as plt
import scipy.stats as sstat
import itertools
import numpy as np
import pandas as pd

DOC = "PCR-005"
UO = "protein_a"
UO_TITLE = "Protein A Chromatography (Step 5)"

# --- doc-local derived scalars (pulled from the model; never typed) -----------------
alpha = 0.05
step_no = CFG.unit_op(UO).step
n_scr = doe_runs(UO, "screening")
n_rsm = doe_runs(UO, "rsm")
cp_scr = doe_centre_points(UO, "screening")
cp_rsm = doe_centre_points(UO, "rsm")
FS = D.rsm_factors(UO)
RESP = D.responses(UO)
PNAME = {p.key: p.name for p in CFG.unit_op(UO).parameters}
PUNIT = {p.key: p.unit for p in CFG.unit_op(UO).parameters}
NOR = {f: CFG.unit_op(UO).param(f).nor for f in FS}
PR = {f: CFG.unit_op(UO).param(f).prange for f in FS}
SP = {f: CFG.unit_op(UO).param(f).setpoint for f in FS}

scr_df = csv(f"doe_{UO}_screening.csv")
rsm_df = csv(f"doe_{UO}_rsm.csv")
pools = pd.concat([scr_df, rsm_df], ignore_index=True)
n_pools = len(pools)
n_fact_scr = int((scr_df.run_type == "factorial").sum())
n_fact_rsm = int((rsm_df.run_type == "factorial").sum())
n_axial_rsm = int((rsm_df.run_type == "axial").sum())
n_params = len(CFG.unit_op(UO).parameters)
n_multi = sum(1 for p in CFG.unit_op(UO).parameters if p.study == "multivariate")
n_uni = n_params - n_multi
cls_counts = report_params(UO)["Class"].value_counts().to_dict()
n_wccpp = cls_counts.get("WC-CPP", 0)
n_kpp = cls_counts.get("KPP", 0)
n_gpp = cls_counts.get("GPP", 0)
n_cpp = cls_counts.get("CPP", 0)

fits_scr = {r: D.fit(UO, "screening", r) for r in RESP}
fits_rsm = {r: D.fit(UO, "rsm", r) for r in RESP}
n_terms_scr = len(fits_scr[RESP[0]]["names"])
n_terms_rsm = len(fits_rsm[RESP[0]]["names"])
df_res_scr = int(fits_scr[RESP[0]]["model"].df_resid)
df_res_rsm = int(fits_rsm[RESP[0]]["model"].df_resid)


def eff(resp, term):
    d = D.screening_effects_df(UO, resp)
    return float(d.loc[d["Term"] == term, "Effect"].iloc[0])


def eff_p(resp, term):
    d = D.screening_effects_df(UO, resp)
    return float(d.loc[d["Term"] == term, "p-value"].iloc[0])


def rcoef(resp, term):
    d = D.rsm_coeff_df(UO, resp)
    return float(d.loc[d["Term"] == term, "Coef."].iloc[0])


def rcoef_p(resp, term):
    d = D.rsm_coeff_df(UO, resp)
    return float(d.loc[d["Term"] == term, "p-value"].iloc[0])


def n_sig_scr(resp, a=alpha):
    d = D.screening_effects_df(UO, resp)
    return int((d["p-value"] < a).sum())


def n_sig_rsm(resp, a=alpha):
    d = D.rsm_coeff_df(UO, resp)
    return int((d[d["Term"] != "Intercept"]["p-value"] < a).sum())


def cvr(resp, kind="rsm"):
    d = D.center_cv_df(UO, kind)
    return float(d.loc[d["Response"] == D.RESP_LABEL[resp], "%CV"].iloc[0])


def pred(resp, **nat):
    base = dict(SP)
    base.update(nat)
    return float(D.predict(UO, resp, natural=base)[0])


def corner(resp, box, worst="max"):
    rows = list(itertools.product(*[box[f] for f in FS]))
    vals = [float(D.predict(UO, resp, natural=dict(zip(FS, r)))[0]) for r in rows]
    i = int(np.argmax(vals)) if worst == "max" else int(np.argmin(vals))
    return dict(zip(FS, rows[i])), vals[i]


PAR = D.par_table(UO)


def par_cell(resp, factor, col):
    m = (PAR["CQA"] == D.RESP_LABEL[resp]) & (PAR["Parameter"] == PNAME[factor])
    return str(PAR.loc[m, col].iloc[0])


# acceptance criteria
hcp_ipc = D.ipc_limit(UO, "pool_hcp_ng_mg")[1]
hcp_margin = CFG.ipc_limits["steps"][UO]["pool_hcp_ng_mg"]["from_ds_backcalc"]["margin"]
hcp_ceiling = hcp_ipc * hcp_margin
hcp_ds_lim = D.acceptance_for(UO, "pool_hcp_ng_mg")[1]
lpa_lim = D.acceptance_for(UO, "leached_protein_a_ppm")[1]
hcp_basis = D.acceptance_basis(UO, "pool_hcp_ng_mg")
lpa_basis = D.acceptance_basis(UO, "leached_protein_a_ppm")

# the assayed pools, read without a model
lpa_max = float(pools["leached_protein_a_ppm"].max())
lpa_min = float(pools["leached_protein_a_ppm"].min())
lpa_mean = float(pools["leached_protein_a_ppm"].mean())
lpa_sd = float(pools["leached_protein_a_ppm"].std(ddof=1))
lpa_head = lpa_lim - lpa_max
lpa_over = int((pools["leached_protein_a_ppm"] > lpa_lim).sum())
hcp_pool_max = float(pools["pool_hcp_ng_mg"].max())
hcp_pool_min = float(pools["pool_hcp_ng_mg"].min())
n_pool_over = int((pools["pool_hcp_ng_mg"] > hcp_ipc).sum())
n_pool_over_lowph = int((pools.loc[pools["pool_hcp_ng_mg"] > hcp_ipc, "elution_ph"]
                         == PR["elution_ph"][0]).sum())
yld_min = float(pools["step_yield"].min())
yld_max = float(pools["step_yield"].max())

# the nominal train
ps = csv("process_summary.csv").set_index("step")
hcp_nom = float(ps.loc[step_no, "pool_hcp_ng_mg"])
lpa_nom = float(ps.loc[step_no, "leached_protein_a_ppm"])
cex_fold = float(ps.loc[7, "hcp_clearance_fold"])
aex_fold = float(ps.loc[8, "hcp_clearance_fold"])
down_fold = cex_fold * aex_fold
dna_lrv = float(CFG.unit_op(UO).model["dna_lrv"])

# predictions from the fitted response-surface models
hcp_sp = pred("pool_hcp_ng_mg")
lpa_sp = pred("leached_protein_a_ppm")
yld_sp = pred("step_yield")
hcp_sp_ratio = hcp_ipc / hcp_sp
nor_corner, hcp_nor_worst = corner("pool_hcp_ng_mg", NOR)
par_corner, hcp_par_worst = corner("pool_hcp_ng_mg", PR)
lpa_nor_corner, lpa_nor_worst = corner("leached_protein_a_ppm", NOR)
yld_corner, yld_worst = corner("step_yield", PR, worst="min")
hcp_nor_worst_ds = hcp_nor_worst / down_fold
hcp_sp_ds = hcp_sp / down_fold
def corner_txt(c):
    parts = []
    for f in FS:
        nm = PNAME[f]
        nm = nm[0].lower() + nm[1:]
        parts.append(f"{nm} {c[f]:g}" if PUNIT[f].lower() == "ph"
                     else f"{nm} {c[f]:g} {PUNIT[f]}")
    return ", ".join(parts[:-1]) + " and " + parts[-1]


nor_corner_txt = corner_txt(nor_corner)
par_corner_txt = corner_txt(par_corner)
yld_corner_txt = corner_txt(yld_corner)

# coverage of the normal operating range and of the characterized region
_g = np.meshgrid(*[np.linspace(NOR[f][0], NOR[f][1], 11) for f in FS], indexing="ij")
_natgrid = {f: x.ravel() for f, x in zip(FS, _g)}
nor_ok = float((D.predict(UO, "pool_hcp_ng_mg", natural=_natgrid) <= hcp_ipc).mean())
nor_lpa_max = float(D.predict(UO, "leached_protein_a_ppm", natural=_natgrid).max())
dsg = D.design_space_grid(UO)
ds_frac = dsg["fraction"]
ds_binding = D.RESP_LABEL[dsg["binding"]]
ds_n = dsg["n_points"]
ds_rej_lpa = dsg["per_response"]["leached_protein_a_ppm"]

# the elution pH that the top of the load NOR requires
_ph = np.linspace(PR["elution_ph"][0], PR["elution_ph"][1], 701)
_yy = D.predict(UO, "pool_hcp_ng_mg", natural={
    "load": np.full(_ph.size, NOR["load"][1]), "elution_ph": _ph,
    "flow": np.full(_ph.size, SP["flow"]), "end_collect": np.full(_ph.size, SP["end_collect"])})
ph_at_load_hi = float(_ph[_yy <= hcp_ipc].min())

# the deviation run, placed in the characterization range
dev_ph_coded = float(D.to_coded(UO, "elution_ph", dev_005_01_ph_measured))
range_ratio_min = min((PR[f][1] - PR[f][0]) / (NOR[f][1] - NOR[f][0]) for f in FS)
d_vs_b_hcp = abs(rcoef("pool_hcp_ng_mg", "B") / rcoef("pool_hcp_ng_mg", "D"))

# commercial-scale capability
cap_keys = ["hcp", "residual_dna", "leached_protein_a"]
_c = cap[cap.key.isin(cap_keys)].set_index("key")
cpk_hcp = float(_c.loc["hcp", "Cpk"])
cpk_dna = float(_c.loc["residual_dna", "Cpk"])
cpk_lpa = float(_c.loc["leached_protein_a", "Cpk"])
hcp_ds_mean = float(_c.loc["hcp", "mean"])
hcp_ds_sd = float(_c.loc["hcp", "sd"])
hcp_ds_max = float(_c.loc["hcp", "max"])
lpa_ds_mean = float(_c.loc["leached_protein_a", "mean"])
lpa_ds_ratio = float(_c.loc["leached_protein_a", "acc_high"]) / lpa_ds_mean
cpk_tight = float(_c["Cpk"].min())
cpk_tight_name = str(_c.loc[_c["Cpk"].idxmin(), "cqa"])
n_mc = V["n_monte_carlo"]
scale_l = V["commercial_scale_l"]

# analytical methods
methods = csv("dev_methods.csv").set_index("id")
amv_ids = [a for a, _ in PROTEIN_A_AMV_REFS]
methods_df = csv("dev_methods.csv")
methods_df = methods_df[methods_df["id"].isin(amv_ids)].rename(columns={
    "id": "Method", "name": "Analytical procedure", "precision_pct": "Precision (%RSD)",
    "loq": "LoQ", "loq_unit": "LoQ unit", "accuracy_pct": "Accuracy (%)",
    "variance_fraction": "Assay share of variance"})
lpa_prec = float(methods.loc["AMV-3016", "precision_pct"])
lpa_varfrac = float(methods.loc["AMV-3016", "variance_fraction"])
lpa_loq = float(methods.loc["AMV-3016", "loq"])
hcp_prec = float(methods.loc["AMV-3012", "precision_pct"])
hcp_varfrac = float(methods.loc["AMV-3012", "variance_fraction"])
