"""Standard complex tables of the Rev 2.0 corpus, each built from the generated CSVs.

Every builder returns a :class:`ctable.CTable`. A document prints it (``T.show()`` in a chunk with
``#| output: asis``) and ``build_ground_truth.py`` calls the SAME builder with the same arguments
to get the rendered rows (``T.rows()``), so an annex quote anchored on a merged row stays verbatim
when the seed changes.

The footnotes state where a value came from (which method, which study, which deviation), and
nothing else. Every number is read from ``outputs/data/``; no builder computes a criterion.
"""
from __future__ import annotations

import math
import os
import re
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from ctable import C, CTable

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "outputs", "data")


def _csv(name):
    return pd.read_csv(os.path.join(DATA, name))


def _cfg():
    from amab_process import load_config
    return load_config()


# --------------------------------------------------------------------------------------
# Number formatting: one rule for every table in the corpus
# --------------------------------------------------------------------------------------
def num(v, nd=None) -> str:
    """A value as a table shows it. NaN is "n.t." (not tested); inf is "–"."""
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "n.t."
    v = float(v)
    if math.isinf(v):
        return "–"
    if nd is not None:
        return f"{v:,.{nd}f}"
    a = abs(v)
    if a >= 1000:
        return f"{v:,.0f}"
    if a >= 100:
        return f"{v:.0f}"
    if a >= 10:
        return f"{v:.1f}"
    return f"{v:.2f}"


def pval(v) -> str:
    """A process-parameter value as the configuration states it (3.5, 90, 0.75)."""
    return f"{float(v):g}"


def crit(lo, hi, spec_type) -> str:
    """A criterion as text: "≤ 100", "≥ 6.6" or "18.0–40.0"."""
    if spec_type == "upper":
        return f"≤ {num(hi)}"
    if spec_type == "lower":
        return f"≥ {num(lo)}"
    return f"{num(lo)}–{num(hi)}"


STEP_NAME = {
    "bioreactor": "Production bioreactor", "harvest": "Harvest", "protein_a": "Protein A",
    "viral_inactivation": "Low-pH viral inactivation", "cex": "Cation exchange",
    "aex": "Anion exchange", "virus_filtration": "Virus filtration", "ufdf": "UF/DF",
}
ATTR_NAME = {
    "afucosylation": "Afucosylation (%)", "galactosylation": "Galactosylation (%)",
    "high_mannose": "High mannose (%)", "acidic_variants": "Acidic variants (%)",
    "aggregates_hmw": "Aggregates, HMW (%)", "hcp": "Host cell protein (ng/mg)",
    "leached_protein_a": "Leached Protein A (ppm)", "fragments_lmw": "Fragments, LMW (%)",
    "lrv_xmulv": "XMuLV clearance (log10)", "lrv_mvm": "MVM clearance (log10)",
}


# --------------------------------------------------------------------------------------
# 1. Analytical methods by step and study
# --------------------------------------------------------------------------------------
def methods_by_study(steps: Optional[List[str]] = None, label="tbl-methods-by-study") -> CTable:
    """Which method measured aggregate and fragments in which study, step by step."""
    cfg = _cfg()
    plan = _csv("method_plan.csv")
    st = {s["id"]: s for s in cfg.raw()["campaign"]["studies"]}
    steps = steps or ["bioreactor", "harvest", "protein_a", "viral_inactivation", "cex", "aex",
                      "virus_filtration", "ufdf"]
    amd = cfg.raw()["campaign"]["method_decision"]

    def frag(step, kind):
        sid = {"screening": {"virus_filtration": "S-VF-DOE"}.get(step), "rsm": None}.get(kind)
        row = plan[(plan["step"] == step) & (plan["kind"] == kind)]
        if row.empty:
            return None
        r = row.iloc[0]
        if not r["lmw_in_scope"]:
            return None
        m = []
        if r["lmw_sec"]:
            m.append("SEC^a)^" if step in ("protein_a", "viral_inactivation") else "SEC")
        if r["lmw_cesds"]:
            m.append("nrCE-SDS^b)^" if step in ("protein_a", "viral_inactivation")
                     else "nrCE-SDS^c)^" if step == "cex" else "nrCE-SDS")
        return ", ".join(m)

    body = []
    for step in steps:
        has_doe = not plan[(plan["step"] == step) & (plan["kind"].isin(["screening", "rsm"]))].empty
        if not has_doe:
            body.append([C(STEP_NAME[step], rs=2), "Aggregates, HMW", C("no DoE^e)^", cs=2)])
            body.append(["Fragments, LMW", C("no DoE^e)^", cs=2)])
            continue
        fs, fr = frag(step, "screening"), frag(step, "rsm")
        body.append([C(STEP_NAME[step], rs=2), "Aggregates, HMW", C("SEC", cs=2)])
        if fs is None and fr is None:
            body.append(["Fragments, LMW", C("not in scope^f)^", cs=2)])
        else:
            if step == "aex":
                fs, fr = fs + "^d)^", fr + "^d)^"
            body.append(["Fragments, LMW", fs or "n.t.", fr or "n.t."])
    ret = st["S-PA-RET"]
    notes = [
        ("a)", "In this matrix part of the host cell protein elutes in the SEC low molecular weight "
               f"window. Reported for information only ({amd['id']})."),
        ("b)", f"Retained response-surface samples, tested {ret['start']} to {ret['end']}."),
        ("c)", "Both methods on the same samples, the comparability study S-CEX-FRC."),
        ("d)", "Re-executed design (DEV-008-01). The invalidated first execution measured "
               "fragments by SEC."),
        ("e)", "Univariate characterization only."),
        ("f)", "Fragments were not an attribute of this study."),
    ]
    used = {m for row in body for c in row for m in re.findall(r"\^([a-f]\))\^", str(getattr(c, "text", c)))}
    notes = [n for n in notes if n[0] in used]
    return CTable(
        header=[[C("Step", rs=2), C("Attribute", rs=2), C("Method used in study", cs=2)],
                ["Screening", "Response surface"]],
        body=body, align="llll", notes=notes, notes_per_row=True,
        caption="Methods used for size variants, by step and study.", label=label)


# --------------------------------------------------------------------------------------
# 2. Intermediate acceptance criteria, with their derivation
# --------------------------------------------------------------------------------------
def iac_derivation(steps: Optional[List[str]] = None, label="tbl-iac") -> CTable:
    t = _csv("iac.csv")
    if steps:
        t = t[t["step_key"].isin(steps)]
    order = ["hcp", "aggregates_hmw", "fragments_lmw", "leached_protein_a", "acidic_variants",
             "afucosylation", "galactosylation", "high_mannose", "lrv_xmulv", "lrv_mvm"]
    body, marks = [], set()
    for cqa in [c for c in order if c in set(t["cqa"])]:
        g = t[t["cqa"] == cqa].sort_values("step")
        first = True
        for _, r in g.iterrows():
            if r["basis"] == "platform claim":
                deriv = [C("not applicable", cs=2)]
                basis = "Platform claim^c)^"
                marks.add("c)")
            else:
                deriv = [num(r["downstream_fold"]), num(r["downstream_added"])]
                if r["basis"] == "drug substance":
                    basis, m = "Drug substance^a)^", "a)"
                elif "tightened" in r["basis"]:
                    basis, m = "Back-calculated, tightened^b)^", "b)"
                else:
                    basis, m = "Back-calculated", None
                if m:
                    marks.add(m)
            row = []
            if first:
                row += [C(ATTR_NAME[cqa], rs=len(g)), C(crit(r["ds_low"], r["ds_high"], r["spec_type"])
                                                        if r["basis"] != "platform claim"
                                                        else f"≥ {num(r['ds_low'])}^d)^", rs=len(g))]
                if r["basis"] == "platform claim":
                    marks.add("d)")
                first = False
            row += [STEP_NAME[r["step_key"]], *deriv,
                    crit(r["iac_low"], r["iac_high"], r["spec_type"]), basis]
            body.append(row)
    notes = [
        ("a)", "No downstream step changes the attribute, so the drug-substance criterion applies."),
        ("b)", "The response-surface model of a downstream step predicted, within its NOR, a worse "
               "value than the platform worst case. The A-Mab value replaced it."),
        ("c)", "Log reduction claimed for this step in the modular viral clearance claim."),
        ("d)", "Cumulative requirement across the steps that clear the virus."),
    ]
    return CTable(
        header=[[C("Attribute", rs=2), C("Drug-substance criterion", rs=2), C("Step output", rs=2),
                 C("Downstream worst case", cs=2), C("Intermediate acceptance criterion", rs=2),
                 C("Basis", rs=2)],
                ["Clearance fold", "Increase"]],
        body=body, align=["P{2.6cm}", "l", "P{2.6cm}", "r", "r", "l", "P{3.2cm}"],
        notes=[n for n in notes if n[0] in marks], notes_per_row=True,
        caption="Intermediate acceptance criteria and their derivation from the drug-substance "
                "criteria.", label=label, resize=True)


# --------------------------------------------------------------------------------------
# 3. Rev 1.0 against Rev 2.0 criteria
# --------------------------------------------------------------------------------------
def criteria_change(steps: Optional[List[str]] = None, label="tbl-criteria-change") -> CTable:
    new = _csv("iac.csv")
    old = _csv("criteria_rev1.csv")
    if steps:
        new, old = new[new["step_key"].isin(steps)], old[old["step_key"].isin(steps)]
    keys = sorted(set(zip(new["step"], new["step_key"], new["response"])) |
                  set(zip(old["step"], old["step_key"], old["response"])))
    body, marks = [], set()
    by_step: Dict[str, list] = {}
    for step, sk, resp in keys:
        by_step.setdefault(sk, []).append(resp)
    for sk in sorted(by_step, key=lambda k: new.loc[new["step_key"] == k, "step"].min()
                     if k in set(new["step_key"]) else 99):
        resps = by_step[sk]
        for i, resp in enumerate(resps):
            o = old[(old["step_key"] == sk) & (old["response"] == resp)]
            n = new[(new["step_key"] == sk) & (new["response"] == resp)]
            cqa = (n.iloc[0]["cqa"] if not n.empty else o.iloc[0]["cqa"])
            st = "lower" if cqa.startswith("lrv") else ("two_sided" if (not o.empty and o.iloc[0]["low"] > 0 and not cqa.startswith("lrv")) else "upper")
            if o.empty and cqa == "fragments_lmw":
                ocells = [C("not assessed^c)^", cs=2)]
                marks.add("c)")
            elif o.empty:
                ocells = [C("none^a)^", cs=2)]
                marks.add("a)")
            else:
                orow = o.iloc[0]
                code = _rule_code(orow["rule"])
                marks.add(code)
                rule = f"^{code}^" + ("" if pd.isna(orow["margin"]) else f" margin {num(orow['margin'], 1)}")
                ocells = [crit(orow["low"], orow["high"], st), rule]
            if n.empty:
                ncells = [C("none", cs=2)]
            else:
                nrow = n.iloc[0]
                ncells = [crit(nrow["iac_low"], nrow["iac_high"], nrow["spec_type"]), nrow["basis"]]
            row = ([C(STEP_NAME[sk], rs=len(resps))] if i == 0 else []) + [ATTR_NAME[cqa], *ocells, *ncells]
            body.append(row)
    marks.add("b)")
    notes = [("a)", "Version 1.0 set no step criterion and judged the step against the "
                    "drug-substance criterion."),
             ("b)", "Applied in the Version 1.0 reports at analysis. No approved Version 1.0 plan "
                    "contained these criteria (INV-001 finding 1)."),
             ("c)", "Version 1.0 did not report fragments. The attribute was added at Version 2.0.")]
    old_rules = {_rule_code(r): r for r in old["rule"].unique()}
    notes += [(c, f"Version 1.0 rule: {old_rules[c]}.") for c in sorted(old_rules)]
    return CTable(
        header=[[C("Step", rs=2), C("Attribute", rs=2), C("Version 1.0^b)^", cs=2), C("Version 2.0", cs=2)],
                ["Criterion", "Rule", "Criterion", "Basis"]],
        body=body, align=["P{2.4cm}", "P{3.4cm}", "l", "l", "l", "P{3.6cm}"],
        notes=[x for x in notes if x[0] in marks], notes_per_row=True, size="footnotesize",
        caption="Acceptance criteria for the step outputs in Version 1.0 and Version 2.0.",
        label=label, resize=True)


def _rule_code(rule: str) -> str:
    """A short footnote code for a Version 1.0 rule, so the table row stays one line."""
    # numbered in the order INV-001 lists the Version 1.0 rules: the back-calculation first
    r = str(rule)
    if r.startswith("nominal back"):
        return "R1"
    if r.startswith("mean"):
        return "R2"
    if r.startswith("requirement"):
        return "R3"
    return "R4"


# --------------------------------------------------------------------------------------
# 4. Hold-time stability
# --------------------------------------------------------------------------------------
HOLD_POOL = {"harvest": "clarified harvest", "protein_a": "Protein A eluate (held at elution pH)",
             "viral_inactivation": "neutralized viral inactivation pool"}


def hold_stability(pool: str, label: Optional[str] = None) -> CTable:
    h = _csv(f"hold_{pool}.csv")
    body = []
    for temp, g in h.groupby("temperature", sort=False):
        for i, (_, r) in enumerate(g.iterrows()):
            row = ([C(temp, rs=len(g))] if i == 0 else []) + [
                str(int(r["day"])), num(r["hmw_pct"]), num(r["lmw_sec_pct"]) + "^a)^",
                (num(r["lmw_cesds_pct"]) if not pd.isna(r["lmw_cesds_pct"]) else "n.t.^b)^"),
                num(r["acidic_pct"], 1)]
            body.append(row)
    return CTable(
        header=[[C("Storage", rs=2), C("Day", rs=2), C("Size variants (%)", cs=3), C("Acidic variants (%)", rs=2)],
                ["HMW (SEC)", "LMW (SEC)", "LMW (nrCE-SDS)"]],
        body=body, align="lrrrrr", style="grid",
        notes=[("a)", "Includes host cell protein eluting in the low molecular weight window "
                      "(AMD-001). Not used for evaluation."),
               ("b)", "Not tested. The first and last time points were retained and tested by "
                      "nrCE-SDS after AMD-001, with the retained response-surface samples.")],
        caption=f"Hold-time stability of the {HOLD_POOL[pool]}.", label=label or f"tbl-hold-{pool.replace('_', '-')}")


# --------------------------------------------------------------------------------------
# 5. SEC against nrCE-SDS (S-CEX-FRC)
# --------------------------------------------------------------------------------------
def method_comparability(label="tbl-sec-cesds") -> CTable:
    c = _csv("cex_fraction_comparability.csv")
    body = []
    for sample, g in c.groupby("sample", sort=False):
        for i, (_, r) in enumerate(g.iterrows()):
            row = ([C(sample, rs=len(g))] if i == 0 else []) + [
                str(int(r["replicate"])), num(r["lmw_sec_pct"]), num(r["lmw_cesds_pct"]),
                f"{r['difference']:+.2f}"]
            body.append(row)
    return CTable(
        header=[[C("Sample", rs=2), C("Replicate", rs=2), C("Fragments, LMW (%)", cs=2), C("SEC minus nrCE-SDS", rs=2)],
                ["SEC", "nrCE-SDS"]],
        body=body, align="lrrrr",
        notes=[("", "nrCE-SDS reports the sum of clipped species. The partial molecules seen under "
                    "SDS (HHL, HH, HL, free light chain), which come from antibody lacking one or more "
                    "interchain disulfide bonds, are excluded. This makes the two methods comparable.")],
        caption="Fragments by SEC and by non-reduced CE-SDS on the same samples (study S-CEX-FRC).",
        label=label)


# --------------------------------------------------------------------------------------
# 6. Verification of the platform worst cases
# --------------------------------------------------------------------------------------
def worst_case_verification(steps: Optional[List[str]] = None, label="tbl-iac-verification") -> CTable:
    v = _csv("iac_verification.csv")
    if steps:
        v = v[v["step_key"].isin(steps)]
    body = []
    for sk, g in v.groupby("step_key", sort=False):
        for i, (_, r) in enumerate(g.iterrows()):
            kind = "Clearance fold, lowest" if r["assumption"] == "fold_min" else "Increase, largest"
            met = "n.t.^a)^" if pd.isna(r["met"]) else ("Yes" if bool(r["met"]) else "No^b)^")
            row = ([C(STEP_NAME[sk], rs=len(g))] if i == 0 else []) + [
                ATTR_NAME[r["cqa"]], kind, num(r["assumed"]),
                num(r["observed_edge"]) if not pd.isna(r["observed_edge"]) else "n.t.^a)^",
                num(r["predicted_nor"]) if not pd.isna(r["predicted_nor"]) else "n.t.^a)^", met]
            body.append(row)
    return CTable(
        header=[[C("Step", rs=2), C("Attribute", rs=2), C("Worst case", rs=2), C("Platform", rs=2),
                 C("This campaign", cs=2), C("Confirmed", rs=2)],
                ["At the edges", "Within the NOR"]],
        body=body, align="lllrrrl",
        notes=[("a)", "Not a response of the response-surface study at this step."),
               ("b)", "The criteria upstream of this step were recalculated with the value predicted "
                      "within the NOR.")],
        notes_per_row=True,
        caption="Platform worst cases assumed by the intermediate acceptance criteria, against this "
                "campaign's results.", label=label, resize=True)


# --------------------------------------------------------------------------------------
# 7. DoE results with method sub-columns and deviation footnotes
# --------------------------------------------------------------------------------------
RESP_LABEL = {
    "afucosylation": "Afuc. (%)", "galactosylation": "Gal. (%)", "high_mannose": "Man5 (%)",
    "acidic_variants": "Acidic (%)", "aggregates_hmw": "HMW (%)", "aggregate_out_pct": "HMW (%)",
    "pool_hcp_ng_mg": "HCP (ng/mg)", "hcp_out_ng_mg": "HCP (ng/mg)", "step_yield": "Yield (%)",
    "leached_protein_a_ppm": "Leached PrA (ppm)", "xmulv_lrf": "XMuLV LRF", "mvm_lrf": "MVM LRF",
}


def _deviation_runs(step: str, kind: str) -> Dict[int, str]:
    """{run number: deviation id} for runs a deviation names, from the summaries and lot use."""
    out = {}
    dev = _csv("deviations.csv")
    lots = _csv("dev_lots.csv") if os.path.exists(os.path.join(DATA, "dev_lots.csv")) else pd.DataFrame()
    word = "screening" if kind == "screening" else "RSM"
    for _, d in dev[dev["step"] == step].iterrows():
        texts = [str(d["summary"])]
        if isinstance(d.get("lot"), str) and not lots.empty:
            texts += list(lots.loc[lots.iloc[:, 0] == d["lot"]].astype(str).values.ravel())
        for t in texts:
            m = re.search(rf"{word} run (\d+)", t, re.I)
            if m:
                out[int(m.group(1))] = d["dev_id"]
    return out


def doe_results(step: str, kind: str, label: Optional[str] = None, superseded: bool = False) -> CTable:
    from amab_process import studies as st
    cfg = _cfg()
    name = f"doe_{step}_{kind}{'_superseded' if superseded else ''}.csv"
    d = _csv(name)
    factors = [c[len("coded_"):] for c in d.columns if c.startswith("coded_")]
    resps = [r for r in st.DOE_RESPONSES[step] if r in d.columns]
    lmw = [c for c in ("lmw_sec_pct", "lmw_cesds_pct") if c in d.columns]
    devs = {} if superseded else _deviation_runs(step, kind)
    fl = []
    for f in factors:
        p = cfg.unit_op(step).param(f)
        fl.append(f"{p.name} ({p.unit})")
    head1 = [C("Run", rs=2), C("Type", rs=2), C("Factor settings", cs=len(factors)),
             C("Responses", cs=len(resps))]
    head2 = fl + [RESP_LABEL.get(r, r) for r in resps]
    if lmw:
        head1.append(C("Fragments, LMW (%)", cs=len(lmw)))
        head2 += ["SEC" if c == "lmw_sec_pct" else "nrCE-SDS" for c in lmw]
    body, marks = [], {}
    for _, r in d.iterrows():
        run = int(r["run"])
        rl = str(run)
        if run in devs:
            mk = f"{chr(ord('a') + len(marks))})"
            marks.setdefault(devs[run], mk)
            rl = f"{run}^{marks[devs[run]]}^"
        row = [rl, str(r["run_type"]).replace("_", " ")]
        row += [pval(r[f]) for f in factors]
        for resp in resps:
            v = r[resp]
            row.append(num(100 * v, 1) if resp == "step_yield" else num(v))
        row += [num(r[c]) for c in lmw]
        body.append(row)
    dev = _csv("deviations.csv").set_index("dev_id")
    notes = [(mk, f"{did}: {dev.loc[did, 'summary']}. Run retained.") for did, mk in marks.items()]
    if lmw and step in ("protein_a", "viral_inactivation") and "lmw_sec_pct" in lmw:
        notes.append(("", "LMW by SEC is biased in this matrix and is not used for evaluation (AMD-001). n.t. = not tested."))
    elif lmw:
        notes.append(("", "n.t. = not tested."))
    title = {"screening": "screening", "rsm": "response-surface"}[kind]
    return CTable(
        header=[head1, head2], body=body, align=["l", "l"] + ["R{1.35cm}"] * len(head2),
        notes=notes, notes_per_row=True, size="footnotesize", resize=True,
        caption=(f"{'Invalidated first execution: ' if superseded else ''}{STEP_NAME[step]} "
                 f"{title} design, settings and results."),
        label=label or f"tbl-doe-{step.replace('_', '-')}-{kind}{'-sup' if superseded else ''}")


# --------------------------------------------------------------------------------------
# 8. Criterion | Result | Met
# --------------------------------------------------------------------------------------
def criteria_results(step: str, label: Optional[str] = None) -> CTable:
    """Each step output against its IAC: the model-predicted range over the NOR box of the
    response-surface factors, and whether the whole range meets the criterion."""
    import itertools
    import doe_report as D
    cfg = _cfg()
    t = _csv("iac.csv")
    t = t[t["step_key"] == step]
    body = []
    for _, r in t.iterrows():
        resp = r["response"]
        try:
            res = D.fit(step, "rsm", resp)
        except Exception:
            continue
        uo = cfg.unit_op(step)
        fac = res["factors"]
        grid = list(itertools.product(*[[uo.param(f).nor[0], uo.param(f).setpoint, uo.param(f).nor[1]] for f in fac]))
        y = D.predict(step, resp, natural={f: [g[i] for g in grid] for i, f in enumerate(fac)})
        lo, hi = float(np.min(y)), float(np.max(y))
        # judged on the decision statistic of PCMP-001: a single batch (the mean prediction at
        # every NOR corner widened by the 95 % prediction half-width, 1.96 x residual SD) for a
        # quality attribute, the mean for viral clearance
        if D.decision_statistic(resp) == "batch":
            _, plo, phi = D.prediction_interval(step, resp, {f: [g[i] for g in grid] for i, f in enumerate(fac)})
            ok = bool(np.all(D.meets_acceptance(step, resp, plo)) and np.all(D.meets_acceptance(step, resp, phi)))
        else:
            ok = bool(np.all(D.meets_acceptance(step, resp, y)))
        sp = float(D.predict(step, resp, natural={f: uo.param(f).setpoint for f in fac})[0])
        body.append([ATTR_NAME[r["cqa"]], crit(r["iac_low"], r["iac_high"], r["spec_type"]),
                     num(sp), f"{num(lo)} to {num(hi)}", "Yes" if ok else "No"])
    return CTable(
        header=[[C("Attribute", rs=2), C("Criterion", rs=2), C("Mean predicted by the response-surface model", cs=2), C("Met across the NOR^a)^", rs=2)],
                ["At the set-point", "Range over the NOR"]],
        body=body, align="llrrl",
        notes=[("a)", "Judged at every combination of NOR low, set-point and NOR high. Quality "
                      "attributes: the 95 % prediction interval of a single run (t quantile, coefficient "
                      "and residual uncertainty). Viral clearance: the mean prediction.")],
        caption=f"{STEP_NAME[step]} outputs against their intermediate acceptance criteria.",
        label=label or f"tbl-criteria-{step.replace('_', '-')}")


# --------------------------------------------------------------------------------------
# 9. Process parameters, grouped by step
# --------------------------------------------------------------------------------------
def parameters_by_step(steps: Optional[List[str]] = None, label="tbl-parameters-by-step") -> CTable:
    p = _csv("parameter_classification.csv")
    cfg = _cfg()
    keys = steps or list(cfg.train_order)
    body, used = [], set()
    for k in keys:
        uo = cfg.unit_op(k)
        g = p[p["step"] == uo.step]
        for i, (_, r) in enumerate(g.iterrows()):
            par = cfg.unit_op(k).param(next(q.key for q in uo.parameters if q.name == r["parameter"]))
            same = (par.nor[0], par.nor[1]) == (par.prange[0], par.prange[1])
            nor = [C("as characterized^a)^", cs=2)] if same else [pval(r["nor_low"]), pval(r["nor_high"])]
            if same:
                used.add("a)")
            study = "multivariate" if r["study"] == "multivariate" else "univariate^b)^"
            if r["study"] != "multivariate":
                used.add("b)")
            row = ([C(STEP_NAME[k], rs=len(g))] if i == 0 else []) + [
                r["parameter"], r["unit"], pval(r["setpoint"]), *nor,
                pval(par.prange[0]), pval(par.prange[1]), study, r["classification"]]
            body.append(row)
    notes = [("a)", "The normal operating range equals the characterized range."),
             ("b)", "Studied one factor at a time.")]
    return CTable(
        header=[[C("Step", rs=2), C("Parameter", rs=2), C("Unit", rs=2), C("Set-point", rs=2),
                 C("NOR", cs=2), C("Characterized range", cs=2), C("Study", rs=2), C("Class", rs=2)],
                ["Low", "High", "Low", "High"]],
        body=body, align=["P{2.2cm}", "P{3.4cm}", "l", "r", "r", "r", "r", "r", "l", "l"],
        notes=[n for n in notes if n[0] in used], notes_per_row=True,
        size="footnotesize", resize=True,
        caption="Process parameters by step: set-point, ranges and classification.", label=label)
