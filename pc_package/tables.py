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
from typing import Dict, List, Optional, Sequence

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
        # aggregate by SEC wherever the designs carry an aggregate result on their runs (a modelled
        # response, or SEC's own HMW result recorded beside the fragment window at Protein A)
        hmw = False
        for kind_ in ("screening", "rsm"):
            f_ = os.path.join(DATA, f"doe_{step}_{kind_}.csv")
            if os.path.exists(f_):
                cols_ = set(pd.read_csv(f_, nrows=0).columns)
                hmw = hmw or bool({"aggregates_hmw", "aggregate_out_pct", "hmw_sec_pct"} & cols_)
        body.append([C(STEP_NAME[step], rs=2), "Aggregates, HMW",
                     C("SEC" if hmw else "not measured^g)^", cs=2)])
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
        ("c)", "Both methods on the same samples of this design."),
        ("d)", "Re-executed design (DEV-008-01). The invalidated first execution measured "
               "fragments by SEC."),
        ("e)", "Univariate characterization only."),
        ("f)", "Fragments were not an attribute of this study."),
        ("g)", "Aggregate was not measured in the designs at this step."),
    ]
    used = {m for row in body for c in row for m in re.findall(r"\^([a-g]\))\^", str(getattr(c, "text", c)))}
    notes = [n for n in notes if n[0] in used]
    header = [[C("Step", rs=2), C("Attribute", rs=2), C("Method used in study", cs=2)],
              ["Screening", "Response surface"]]
    align, cap = "llll", "Methods used for size variants in the designed studies, by step."
    if len(steps) == 1:
        header, body = _drop_step_column(header, body)
        align, cap = "lll", f"Methods used for size variants in the designed studies, {STEP_NAME[steps[0]]}."
    return CTable(header=header, body=body, align=align, notes=notes, notes_per_row=True,
                  caption=cap, label=label)


def _drop_step_column(header, body):
    """Remove a leading step column that spans the whole table (one step shown): the caption
    names the step instead. The step cell is the first cell of the first body row only."""
    header = [list(header[0][1:])] + [list(r) for r in header[1:]]
    body = [list(body[0][1:])] + [list(r) for r in body[1:]]
    return header, body


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
    one_step = t["step_key"].nunique() == 1        # a constant step column carries nothing
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
                elif "tightened and widened" in r["basis"]:
                    basis, m = "Carried back, tightened^b)^ and widened^e)^", None
                    marks.update({"b)", "e)"})
                elif "tightened" in r["basis"]:
                    basis, m = "Carried back, tightened^b)^", "b)"
                elif "widened" in r["basis"]:
                    basis, m = "Carried back, widened^e)^", "e)"
                else:
                    basis, m = "Carried back", None
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
            row += ([] if one_step else [STEP_NAME[r["step_key"]]]) + [*deriv,
                    crit(r["iac_low"], r["iac_high"], r["spec_type"]), basis]
            body.append(row)
    notes = [
        ("a)", "No downstream step changes the attribute, so the drug-substance criterion applies."),
        ("b)", "The response-surface model of a downstream step predicted, within its NOR, a worse "
               "value than the platform worst case. The 95 % confidence bound of that prediction "
               "replaced it."),
        ("c)", "Log reduction claimed for this step in the modular viral clearance claim."),
        ("d)", "Cumulative requirement across the steps that clear the virus."),
        ("e)", "The 95 % confidence bound of a downstream step's A-Mab worst case within its NOR "
               "was better than the platform worst case. The bound replaced it."),
    ]
    step_h = [] if one_step else [C("Step output", rs=2)]
    step_a = [] if one_step else ["P{2.2cm}"]
    return CTable(
        header=[[C("Attribute", rs=2), C("Drug-substance\ncriterion", rs=2), *step_h,
                 C("Downstream worst case", cs=2), C("Intermediate\nacceptance\ncriterion", rs=2),
                 C("Basis", rs=2)],
                ["Clearance fold", "Increase"]],
        body=body, align=["P{2.4cm}", "l", *step_a, "r", "r", "l", "P{2.6cm}"], size="footnotesize",
        notes=[n for n in notes if n[0] in marks] + [("", "Computed from unrounded values. A criterion recomputed from the rounded values shown can differ in its last digit.")], notes_per_row=True,
        caption="Intermediate acceptance criteria and their derivation from the drug-substance "
                "criteria" + (f", {STEP_NAME[t['step_key'].iloc[0]]} output" if one_step else "") + ".",
        label=label, resize=True)


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
                rule = code + ("" if pd.isna(orow["margin"]) else f", margin {num(orow['margin'], 1)}")
                ocells = [crit(orow["low"], orow["high"], st), rule]
            if n.empty:
                ncells = [C("none", cs=2)]
            else:
                nrow = n.iloc[0]
                b_ = str(nrow["basis"])
                short = {"drug substance": "Drug substance", "platform claim": "Platform claim",
                         "back-calculated": "Carried back"}.get(b_)
                if short is None:
                    t_, w_ = "tightened" in b_, "widened" in b_
                    short = "Carried back, " + " and ".join(
                        [x for x, f in (("tightened^d)^", t_), ("widened^e)^", w_)) if f])
                    marks.update({"d)"} if t_ else set()); marks.update({"e)"} if w_ else set())
                ncells = [crit(nrow["iac_low"], nrow["iac_high"], nrow["spec_type"]), short]
            row = ([C(STEP_NAME[sk], rs=len(resps))] if i == 0 else []) + [ATTR_NAME[cqa], *ocells, *ncells]
            body.append(row)
    marks.add("b)")
    notes = [("a)", "Version 1.0 set no step criterion and judged the step against the "
                    "drug-substance criterion."),
             ("b)", "Applied in the Version 1.0 reports at analysis. No approved Version 1.0 plan "
                    "contained these criteria (INV-001 finding 1)."),
             ("c)", "Version 1.0 did not report fragments. The attribute was added at Version 2.0."),
             ("d)", "Tightened on verification: a downstream step did worse within its NOR than the "
                    "platform worst case."),
             ("e)", "Widened on verification: a downstream step did better than the platform worst "
                    "case at its 95 % confidence bound, on an adequate model.")]
    old_rules = {_rule_code(r): r for r in old["rule"].unique()}
    notes += [(c, f"Version 1.0 rule: {old_rules[c]}.") for c in sorted(old_rules)]
    header = [[C("Step", rs=2), C("Attribute", rs=2), C("Version 1.0^b)^", cs=2), C("Version 2.0", cs=2)],
              ["Criterion", "Rule", "Criterion", "Basis"]]
    align = ["P{2.3cm}", "P{3.1cm}", "l", "P{1.9cm}", "l", "P{3.3cm}"]
    if len(by_step) == 1:
        header, body = _drop_step_column(header, body)
        align = align[1:]
    return CTable(
        header=header,
        body=body, align=align,
        notes=[x for x in notes if x[0] in marks], notes_per_row=True, size="footnotesize",
        caption="Acceptance criteria for the step outputs in Version 1.0 and Version 2.0"
                + (f", {STEP_NAME[next(iter(by_step))]}." if len(by_step) == 1 else "."),
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
        header=[[C("Sample", rs=2), C("Replicate", rs=2), C("Fragments, LMW (%)", cs=2), C("SEC minus\nnrCE-SDS", rs=2)],
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
    widen = bool(_cfg().raw()["iac"].get("allow_widening", False))
    if steps:
        v = v[v["step_key"].isin(steps)]
    body = []
    for sk, g in v.groupby("step_key", sort=False):
        for i, (_, r) in enumerate(g.iterrows()):
            kind = ("Clearance fold, lowest" if r["assumption"] == "fold_min" else
                    "Increase, largest" + (" (points)" if ATTR_NAME[r["cqa"]].endswith("(%)") else ""))
            if pd.isna(r["met"]):
                out = "n.t.^a)^"
            elif not bool(r["met"]):
                out = "Not confirmed, tightened^b)^"
            elif widen and bool(r.get("widening_supported")):
                out = "Better, widened^c)^"
            elif (r["predicted_nor_bound95"] > r["assumed"] if r["assumption"] == "fold_min"
                  else r["predicted_nor_bound95"] < r["assumed"]) and r.get("model_adequate") is False:
                out = "Confirmed, not widened^d)^"
            else:
                out = "Confirmed"
            nt = lambda x: num(x) if not pd.isna(x) else "n.t.^a)^"
            kinds = list(g["assumption"])
            kcell = []
            if i == 0 or kinds[i] != kinds[i - 1]:
                n = 1
                while i + n < len(kinds) and kinds[i + n] == kinds[i]:
                    n += 1
                kcell = [C(kind, rs=n) if n > 1 else kind]
            row = ([C(STEP_NAME[sk], rs=len(g))] if i == 0 else []) + [
                ATTR_NAME[r["cqa"]].split(" (")[0], *kcell, num(r["assumed"]), nt(r["observed_edge"]),
                nt(r["predicted_nor"]), nt(r["predicted_nor_bound95"]), out]
            body.append(row)
    notes = [("a)", "Not a response of the response-surface study at this step."),
             ("b)", "The criteria upstream of this step were recalculated with the 95 % confidence "
                    "bound of the value predicted within the NOR."),
             ("c)", "The 95 % confidence bound is better than the platform worst case. The criteria "
                    "upstream of this step were recalculated with the bound."),
             ("d)", "The 95 % confidence bound is better than the platform worst case, but the model "
                    "fails an adequacy test of PCMP-001, so the platform value stands.")]
    used = {m for row in body for c in row for m in re.findall(r"\^([a-d]\))\^", str(getattr(c, "text", c)))}
    rounding = [("", "Computed from unrounded values. A criterion recomputed from the rounded values shown can differ in its last digit.")]
    return CTable(
        header=[[C("Step", rs=2), C("Attribute", rs=2), C("Worst case", rs=2), C("Platform", rs=2),
                 C("This campaign", cs=3), C("Outcome", rs=2)],
                ["At the\nedges", "Within\nthe NOR", "95 %\nbound"]],
        body=body, align=["P{2.2cm}", "P{2.4cm}", "P{2.6cm}", "r", "r", "r", "r", "P{2.7cm}"],
        size="footnotesize",
        notes=[n for n in notes if n[0] in used] + rounding,
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
        # more columns than a portrait page holds at the font floor: a landscape page of its own
        landscape=len(head2) + 2 >= 12,
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
    body, any_off = [], False
    for _, r in t.iterrows():
        resp = r["response"]
        try:
            res = D.fit(step, "rsm", resp)
        except Exception:
            continue
        uo = cfg.unit_op(step)
        fac = res["factors"]
        grid = list(itertools.product(*[[uo.param(f).nor[0], uo.param(f).setpoint, uo.param(f).nor[1]] for f in fac]))
        # shown and judged at manufacturing scale: the scale-down prediction minus the offset
        d = D._offset_value(step, resp)
        any_off = any_off or d != 0
        y = D.predict(step, resp, natural={f: [g[i] for g in grid] for i, f in enumerate(fac)}) - d
        lo, hi = float(np.min(y)), float(np.max(y))
        ok = bool(D.nor_met(step, resp))
        sp = float(D.predict(step, resp, natural={f: uo.param(f).setpoint for f in fac})[0]) - d
        body.append([ATTR_NAME[r["cqa"]], crit(r["iac_low"], r["iac_high"], r["spec_type"]),
                     num(sp), f"{num(lo)} to {num(hi)}", "Yes" if ok else "No"])
    return CTable(
        header=[[C("Attribute", rs=2), C("Criterion", rs=2), C("Mean predicted by the response-surface model" + ("^b)^" if any_off else ""), cs=2), C("Met across\nthe NOR^a)^", rs=2)],
                ["At the set-point", "Range over the NOR"]],
        body=body, align="llrrl",
        notes=[("a)", "Judged at every combination of NOR low, set-point and NOR high. Quality "
                      "attributes: the 95 % prediction interval of a single run (t quantile, coefficient "
                      "and residual uncertainty). Viral clearance: the mean prediction."),
               ("b)", "At manufacturing scale: the scale-down prediction minus the offset of the "
                      "scale-down model for this output.")][:2 if any_off else 1],
        caption=f"{STEP_NAME[step]} outputs against their intermediate acceptance criteria.",
        label=label or f"tbl-criteria-{step.replace('_', '-')}")


# --------------------------------------------------------------------------------------
# 9. Process parameters, grouped by step
# --------------------------------------------------------------------------------------
def parameters_by_step(steps: Optional[List[str]] = None, label="tbl-parameters-by-step") -> CTable:
    p = _csv("parameter_classification.csv")
    cfg = _cfg()
    keys = steps or list(cfg.train_order)
    body, used, narrowed = [], set(), []
    for k in keys:
        uo = cfg.unit_op(k)
        g = p[p["step"] == uo.step]
        for i, (_, r) in enumerate(g.iterrows()):
            par = cfg.unit_op(k).param(next(q.key for q in uo.parameters if q.name == r["parameter"]))
            same = (par.nor[0], par.nor[1]) == (par.prange[0], par.prange[1])
            nor = ["as characterized^a)^"] if same else [f"{pval(r['nor_low'])}–{pval(r['nor_high'])}"]
            if same:
                used.add("a)")
            if list(par.nor) != list(par.nor_characterized):
                # a Version 2.0 report narrowed this NOR; the note gives the NOR the studies used
                m = f"c{len([u for u in used if u.startswith('c')]) + 1})"
                nor[-1] = f"{nor[-1]}^{m}^"
                used.add(m)
                narrowed.append((m, f"Narrowed at Version 2.0 from {pval(par.nor_characterized[0])}–"
                                    f"{pval(par.nor_characterized[1])} {par.unit}, the NOR as characterized "
                                    f"(PCR-{uo.step:03d})."))
            study = "multivariate" if r["study"] == "multivariate" else "univariate^b)^"
            if r["study"] != "multivariate":
                used.add("b)")
            row = ([C(STEP_NAME[k], rs=len(g))] if i == 0 else []) + [
                r["parameter"], r["unit"], pval(r["setpoint"]), *nor,
                f"{pval(par.prange[0])}–{pval(par.prange[1])}", study, r["classification"]]
            body.append(row)
    notes = [("a)", "The normal operating range equals the characterized range."),
             ("b)", "Studied one factor at a time.")] + narrowed
    return CTable(
        header=[["Step", "Parameter", "Unit", "Set-point", "NOR", "Characterized\nrange", "Study", "Class"]],
        body=body, align=["P{2.0cm}", "P{3.4cm}", "P{2.0cm}", "r", "P{1.9cm}", "l", "l", "l"],
        notes=[n for n in notes if n[0] in used], notes_per_row=True,
        size="footnotesize", resize=True,
        caption="Process parameters by step: set-point, ranges and classification.", label=label)


# --------------------------------------------------------------------------------------
# 10. Calibration of the instrumented systems against the study execution windows (INV-001 F5)
# --------------------------------------------------------------------------------------
def calibration_windows_data() -> pd.DataFrame:
    """One row per study that used an instrumented system, grouped by system, studies in the
    order they started. The annex keys its records on these rows."""
    eq = _csv("dev_equipment.csv")
    chron = _csv("study_chronology.csv")
    rev1 = str(_cfg().raw()["campaign"]["revisions"][0]["effective"])
    rows = []
    for _, e in eq.iterrows():
        for _, s in chron[chron["equipment"] == e["id"]].sort_values("start").iterrows():
            rows.append({"Equipment": e["id"], "Description": e["description"],
                         "Next calibration due": e["cal_due"], "Study": s["id"],
                         "Execution start": s["start"], "Execution end": s["end"],
                         "Date in Version 1.0 title block": rev1})
    return pd.DataFrame(rows)


def calibration_windows(label="tbl-calibration") -> CTable:
    d = calibration_windows_data()
    body = []
    for _, g in d.groupby("Equipment", sort=False):
        n = len(g)
        for i, (_, r) in enumerate(g.iterrows()):
            lead = [C(r["Equipment"], rs=n), C(r["Description"], rs=n),
                    C(r["Next calibration due"], rs=n)] if i == 0 else []
            body.append(lead + [r["Study"], r["Execution start"], r["Execution end"]]
                        + ([C(r["Date in Version 1.0 title block"], rs=n)] if i == 0 else []))
    return CTable(
        header=[[C("Equipment", rs=2), C("Description", rs=2), C("Next\ncalibration due", rs=2),
                 C("Study executed on the system", cs=3), C("Date in\nVersion 1.0\ntitle block", rs=2)],
                ["Study", "Start", "End"]],
        body=body, align=["l", "P{3.4cm}", "P{2.2cm}", "l", "l", "l", "P{2.2cm}"],
        caption="Execution windows of the studies that used instrumented systems, against the "
                "calibration due date and the date in the Version 1.0 title blocks.", label=label)


# --------------------------------------------------------------------------------------
# 11. Scale-down offsets and the qualification of each model for each output
# --------------------------------------------------------------------------------------
SDM_OUTPUT = {
    "afucosylation": ("Afucosylation", "%", 2), "galactosylation": ("Galactosylation", "%", 2),
    "high_mannose": ("High mannose", "%", 2), "acidic_variants": ("Acidic variants", "%", 2),
    "aggregates_hmw": ("Aggregates, HMW", "%", 2), "aggregate_out_pct": ("Aggregates, HMW", "%", 2),
    "pool_hcp_ng_mg": ("Host cell protein", "ng/mg", 0), "hcp_out_ng_mg": ("Host cell protein", "ng/mg", 1),
    "leached_protein_a_ppm": ("Leached Protein A", "ppm", 2), "step_yield": ("Step yield", "%", 1),
    "plates_per_m": ("Column efficiency", "plates/m", 0), "asymmetry": ("Peak asymmetry", "", 2),
}


def sdm_offsets_data(steps: Optional[List[str]] = None, studies: Optional[List[str]] = None) -> pd.DataFrame:
    """One row per step and output of the scale-down qualification: the offset (scale-down minus
    manufacturing), its interval, and the qualification of doe_report.offset_qualification.
    Step yield is printed in percent (the data hold a fraction)."""
    import doe_report as D
    d = _csv("sdm_qualification.csv")
    order = [s for s in STEP_NAME if s in set(d["step"])]
    rows = []
    for step in (steps or order):
        sub = d[d["step"] == step]
        for col in [c for c in SDM_OUTPUT if c in sub.columns and sub[c].notna().any()]:
            q = D.offset_qualification(step, col, studies)
            if q is None:
                continue
            k = 100.0 if col == "step_yield" else 1.0
            rows.append({"step_key": step, "output": col, "n_sd": q["n_sd"], "n_m": q["n_m"],
                         "mean_sd": q["mean_sd"] * k, "mean_m": q["mean_m"] * k,
                         "offset": q["offset"] * k, "lo": q["lo"] * k, "hi": q["hi"] * k,
                         "judged": q["judged"], "met_point": q["met_point"], "met_lo": q["met_lo"],
                         "met_hi": q["met_hi"], "qualified": q["qualified"]})
    return pd.DataFrame(rows)


def sdm_offsets(steps: Optional[List[str]] = None, studies: Optional[List[str]] = None,
                label="tbl-sdm-offsets", caption: Optional[str] = None) -> CTable:
    """The offsets of the scale-down models, one block per step (merged step cell), with the
    conclusion over the NOR at the offset and at both ends of its interval."""
    t = sdm_offsets_data(steps, studies)
    ci = int(round(100 * float(_cfg().raw()["analytics"]["sdm"].get("offset_ci", 0.90))))
    yn = lambda v: "Yes" if v else "No"
    body = []
    for sk, g in t.groupby("step_key", sort=False):
        for i, (_, r) in enumerate(g.iterrows()):
            name, unit, nd = SDM_OUTPUT[r["output"]]
            f = lambda v: f"{v:,.{nd}f}"
            lead = [C(STEP_NAME[sk], rs=len(g))] if i == 0 else []
            if r["judged"]:
                concl = [f"{yn(r['met_lo'])} / {yn(r['met_point'])} / {yn(r['met_hi'])}"]
                q = yn(r["qualified"])
            else:
                concl = ["no criterion^a)^"]
                q = "Yes^a)^"
            body.append(lead + [name + (f" ({unit})" if unit else ""), str(r["n_sd"]), str(r["n_m"]),
                                f(r["mean_sd"]), f(r["mean_m"]), f(r["offset"]),
                                f"{f(r['lo'])} to {f(r['hi'])}", *concl, q])
    notes = [("a)", "The output has no acceptance criterion at this step, so no conclusion depends "
                    "on its offset. The offset is recorded.")]
    used = any(not j for j in t["judged"])
    legend = [("", "SD, scale-down model. Mfg, manufacturing scale. Offset, scale-down mean minus "
                   "manufacturing mean. Met over NOR: the criterion is met at every combination of NOR "
                   "low, set-point and NOR high, with the offset at the low end of its interval, at its "
                   "estimate (est.) and at the high end.")]
    return CTable(
        header=[[C("Step", rs=2), C("Output", rs=2), C("Runs", cs=2),
                 C("Mean", cs=2), C("Offset", cs=2),
                 C("Met over NOR\n(low/est./high)", rs=2), C("Qualified", rs=2)],
                ["SD", "Mfg", "SD", "Mfg", "Estimate", f"{ci} % CI"]],
        body=body, align=["P{2.0cm}", "P{2.6cm}", "c", "c", "r", "r", "r", "P{1.6cm}", "P{2.4cm}", "c"],
        size="footnotesize",
        notes=(notes if used else []) + legend, notes_per_row=True,
        caption=caption or ("Offsets of the scale-down models (scale-down minus manufacturing scale) "
                            "and the qualification of each model for each output."),
        label=label, resize=True)


# --------------------------------------------------------------------------------------
# 12. Campaign overviews for PCMR-001: what was studied, and what each parameter affects
# --------------------------------------------------------------------------------------
# Short attribute names for the dense overview tables (legend in each table's notes).
ATTR_SHORT = {
    "afucosylation": "Afuc", "galactosylation": "Gal", "high_mannose": "Man5",
    "acidic_variants": "Acidic", "aggregates_hmw": "HMW", "hcp": "HCP",
    "leached_protein_a": "LPA", "fragments_lmw": "LMW", "lrv_xmulv": "XMuLV", "lrv_mvm": "MVM",
}
ATTR_ORDER = list(ATTR_SHORT)
ATTR_LEGEND = ("Afuc, afucosylation. Gal, galactosylation. Man5, high mannose. Acidic, acidic "
               "variants. HMW, aggregates. LMW, fragments. HCP, host cell protein. LPA, leached "
               "Protein A. XMuLV and MVM, clearance of the model viruses.")

# Parameter classes, the columns of the parameter-by-step matrices. A parameter not listed is
# "Other". Classes are a reading aid, not data: the parameters come from the config.
PARAM_CLASS = {
    "pH": "pH", "elution_ph": "pH", "ph": "pH", "load_ph": "pH",
    "temperature": "Temperature",
    "duration": "Time", "hold_time": "Time",
    "load": "Load", "filtration_volume": "Load", "depth_filter_load": "Load",
    "flow": "Flow rate",
    "wash_cond": "Conductivity", "wash1_cond": "Conductivity", "load_cond": "Conductivity",
    "pressure": "Pressure", "tmp": "Pressure",
    "ivcc": "Concentration", "medium_conc": "Concentration", "protein_conc": "Concentration",
    "final_conc": "Concentration",
    "end_collect": "Pool collection", "stop_collect": "Pool collection",
}
CLASS_ORDER = ["pH", "Temperature", "Time", "Load", "Flow rate", "Conductivity", "Pressure",
               "Concentration", "Pool collection", "Other"]
# fragments by SEC are unreliable in the capture matrices (AMD-001), so there they do not count
_SEC_FRAGMENTS_VALID = ("cex", "aex", "virus_filtration")


def _resp_cqa(resp: str, step: str) -> Optional[str]:
    import doe_report as D
    if resp == "lmw_cesds_pct":
        return "fragments_lmw"
    if resp == "lmw_sec_pct":
        return "fragments_lmw" if step in _SEC_FRAGMENTS_VALID else None
    if resp == "step_yield":
        return None
    return D.RESP_TO_CQA.get(resp, resp)


def _alpha() -> float:
    return float(_cfg().raw()["campaign"]["thresholds"]["effect_alpha"])


def pp_study_map() -> pd.DataFrame:
    """One row per process parameter of the train: the designs that varied it with their runs,
    the attributes measured in them (``studied``) and the attributes with a significant term
    involving the parameter (``affected``). A response-surface factor is judged on every term of
    its quadratic model, a factor of the screening design alone on its screening model, and a
    parameter of a univariate study on the slope of the attribute against its setting. Step
    yield is a performance output and is not listed."""
    import doe_report as D
    from scipy import stats as sst
    cfg, a = _cfg(), _alpha()
    uni = _csv("univariate_studies.csv")
    chron = _csv("study_chronology.csv")
    rows = []
    for step in STEP_NAME:
        uo = cfg.unit_op(step)
        doe = step in D.st.DOE_FACTORS
        scr = D.screening_factors(step) if doe else []
        rsm = D.rsm_factors(step) if doe else []
        sid = lambda kind: ", ".join(chron.loc[(chron["step"] == step) & (chron["kind"] == kind), "id"])
        for p in uo.parameters:
            r = {"step_key": step, "param": p.key, "name": p.name, "classification": p.classification,
                 "screening_runs": 0, "rsm_runs": 0, "uni_runs": 0, "studies": [],
                 "studied": set(), "affected": set()}
            for kind, facs in (("screening", scr), ("rsm", rsm)):
                if p.key not in facs:
                    continue
                n = len(_csv(f"doe_{step}_{kind}.csv"))
                r[f"{kind}_runs"] = n
                r["studies"].append(sid(kind))
                for resp in list(D.responses(step)) + D.fragment_responses(step, kind):
                    cqa = _resp_cqa(resp, step)
                    if cqa is None:
                        continue
                    r["studied"].add(cqa)
                    # the predictive model decides; the screening model only for a factor the
                    # response surface did not carry
                    if kind == "rsm" or p.key not in rsm:
                        m = D.fit(step, kind, resp)["model"]
                        terms = [t for t in m.pvalues.index if t != "const" and
                                 p.key in re.split(r"[:^]", t)]
                        if any(m.pvalues[t] < a for t in terms):
                            r["affected"].add(cqa)
            u = uni[(uni["step"] == step) & (uni["parameter"] == p.key)]
            if not u.empty:
                r["uni_runs"] = len(u)
                r["studies"].append(", ".join(sorted(u["study"].unique())))
                for col in u.columns[6:]:
                    if u[col].notna().all():
                        cqa = _resp_cqa(col, step)
                        if cqa is None:
                            continue
                        r["studied"].add(cqa)
                        if u["value"].nunique() > 1 and u[col].nunique() > 1:
                            if sst.linregress(u["value"], u[col]).pvalue < a:
                                r["affected"].add(cqa)
            r["studies"] = ", ".join(s for s in r["studies"] if s)
            rows.append(r)
    return pd.DataFrame(rows)


def _attrs(s) -> str:
    return ", ".join(ATTR_SHORT[c] for c in ATTR_ORDER if c in s)


def pp_cqa_matrix(kind: str = "studied", label: Optional[str] = None) -> CTable:
    """Process parameters (columns, by class) against unit operations (rows). Each cell names the
    parameter and the attributes it was studied for (``kind="studied"``) or significantly affects
    (``kind="affected"``), one line per parameter where a step has several of one class."""
    if kind not in ("studied", "affected"):
        raise ValueError(kind)
    m = pp_study_map()
    m["cls"] = m["param"].map(lambda k: PARAM_CLASS.get(k, "Other"))
    classes = [c for c in CLASS_ORDER if c in set(m["cls"])]
    body, none_used = [], False
    for step, g in m.groupby("step_key", sort=False):
        row = [STEP_NAME[step]]
        for c in classes:
            v = g[g["cls"] == c]
            lines = []
            for _, r in v.iterrows():
                att = _attrs(r[kind])
                if not att:
                    att, none_used = "none^a)^", True
                lines.append(f"{r['name']}: {att}")
            row.append("\n".join(lines) or "–")
        body.append(row)
    if kind == "studied":
        a = ("none^a)^", "The campaign data set holds no attribute result for a study of this "
                         "parameter.")
        cap = "Process parameters by unit operation, with the attributes each was studied for."
    else:
        a = ("none^a)^", f"No term involving the parameter is significant at p < {_alpha():g} for "
                         "any attribute measured.")
        cap = ("Process parameters by unit operation, with the attributes each significantly "
               "affects.")
    notes = ([("a)", a[1])] if none_used else []) + [("", ATTR_LEGEND)]
    if kind == "affected":
        notes.append(("", "A response-surface factor is judged on every term of its quadratic model "
                          "(main effect, interaction, quadratic), a factor of the screening design alone "
                          "on its screening model, and a parameter of a univariate study on the slope "
                          "of the attribute against its setting."))
    return CTable(
        header=[[C("Unit operation", rs=2), C("Process parameters", cs=len(classes))], classes],
        body=body, align=["P{1.9cm}"] + ["P{3.3cm}" if c == "Other" else "P{1.6cm}" for c in classes],
        notes=notes, notes_per_row=True, style="grid", size="scriptsize", landscape=True,
        caption=cap, label=label or f"tbl-pp-{kind}")


def studies_overview(label: str = "tbl-studies-overview") -> CTable:
    """Every process parameter of the train with the studies that varied it: screening and
    response-surface runs (multivariate), univariate runs, and the attributes measured. Runs of
    one design are merged over the parameters it varied."""
    m = pp_study_map()
    body = []
    for step, g in m.groupby("step_key", sort=False):
        g = g.reset_index(drop=True)
        cols = {}
        for col in ("screening_runs", "rsm_runs"):
            # merge identical consecutive run counts of one design down the step
            spans, i = [], 0
            while i < len(g):
                j = i
                while j + 1 < len(g) and g.loc[j + 1, col] == g.loc[i, col] and g.loc[i, col] > 0:
                    j += 1
                spans.append((i, j - i + 1))
                i = j + 1
            cols[col] = {s: n for s, n in spans}
        for i, r in g.iterrows():
            row = [C(STEP_NAME[step], rs=len(g))] if i == 0 else []
            row += [r["name"], r["classification"]]
            for col in ("screening_runs", "rsm_runs"):
                if i in cols[col]:
                    v = int(r[col])
                    row.append(C(str(v) if v else "–", rs=cols[col][i]))
            row += [str(int(r["uni_runs"])) if r["uni_runs"] else "–",
                    _attrs(r["studied"]) or "none^a)^", r["studies"] or "–"]
            body.append(row)
    return CTable(
        header=[[C("Unit operation", rs=2), C("Process parameter", rs=2), C("Class", rs=2),
                 C("Runs, multivariate", cs=2), C("Runs,\nunivariate", rs=2),
                 C("Attributes\nmeasured", rs=2), C("Studies", rs=2)],
                ["Screening", "Response surface"]],
        body=body, align=["P{2.2cm}", "P{3.4cm}", "l", "c", "c", "c", "P{3.2cm}", "P{3.0cm}"],
        notes=[("a)", "The campaign data set holds no attribute result for a study of this "
                      "parameter."), ("", ATTR_LEGEND)],
        notes_per_row=True, size="footnotesize", landscape=True,
        caption="Studies of the characterization campaign by unit operation and process parameter.",
        label=label)


def model_effects_overview(steps: Optional[List[str]] = None, label: str = "tbl-model-effects") -> CTable:
    """For each step with a response-surface design and each attribute it measured: the main
    effects, two-factor interactions and quadratic terms significant at the campaign's effect_alpha,
    by parameter name, with R² and predicted R²."""
    import doe_report as D
    cfg, a = _cfg(), _alpha()
    body = []
    for step in [s for s in STEP_NAME if s in D.st.DOE_FACTORS and (steps is None or s in steps)]:
        names = {p.key: p.name for p in cfg.unit_op(step).parameters}
        resps = [r for r in list(D.responses(step)) + D.fragment_responses(step, "rsm")
                 if _resp_cqa(r, step) is not None]
        block = []
        for resp in resps:
            fr = D.fit(step, "rsm", resp)
            pv = fr["model"].pvalues.drop("const")
            sig = [t for t in pv.index if pv[t] < a]
            main = [names[t] for t in sig if ":" not in t and "^" not in t]
            inter = [" × ".join(names[x] for x in t.split(":")) for t in sig if ":" in t]
            quad = [names[t.split("^")[0]] + "²" for t in sig if "^" in t]
            cqa = _resp_cqa(resp, step)
            lab = ATTR_NAME.get(cqa, cqa)
            if resp == "lmw_sec_pct":
                lab += ", SEC"
            elif resp == "lmw_cesds_pct":
                lab += ", nrCE-SDS"
            block.append([lab, ", ".join(main) or "none", ", ".join(inter) or "none",
                          ", ".join(quad) or "none", f"{fr['R2']:.2f}", f"{fr['predR2']:.2f}"])
        for i, b in enumerate(block):
            body.append(([C(STEP_NAME[step], rs=len(block))] if i == 0 else []) + b)
    return CTable(
        header=[[C("Unit operation", rs=2), C("Attribute", rs=2),
                 C(f"Significant terms of the response-surface model (p < {a:g})", cs=3),
                 C("R²", rs=2), C("Predicted R²", rs=2)],
                ["Main effects", "Interactions", "Quadratic"]],
        body=body, align=["P{2.4cm}", "P{3.4cm}", "P{5.4cm}", "P{6.4cm}", "P{2.6cm}", "r", "r"],
        size="footnotesize", landscape=True,
        caption="Significant effects of the response-surface models, by unit operation and attribute"
                + ("" if steps is None else " (" + ", ".join(STEP_NAME[s_].lower() if s_ != "protein_a" else "Protein A"
                                                          for s_ in steps) + ")") + ".",
        label=label)



# --------------------------------------------------------------------------------------
# 13. Any DataFrame as a complex table, with its index columns merged down the rows
# --------------------------------------------------------------------------------------
def frame(df: pd.DataFrame, caption: str, label: str, merge: Sequence[str] = (),
          header: Optional[Dict[str, str]] = None, align=None, notes=(), **kw) -> CTable:
    """A DataFrame as a :class:`CTable`, the way a report sets a table: each column in ``merge``
    (the index columns, left to right) has consecutive identical values merged into one cell
    down the rows, and a column is merged only within the merged cell of the column to its left.
    ``header`` renames columns; write "\\n" in a header to break a long one ("Drug-substance\\n
    criterion"). Use it instead of a pipe table whenever a first column repeats (owner,
    2026-10-08)."""
    dd = df.reset_index(drop=True)
    d = dd.astype(object).where(dd.notna(), "n.t.")
    cols = list(d.columns)
    merge = [c for c in cols if c in merge]
    spans: Dict[tuple, int] = {}
    covered = set()
    groups = [(0, len(d))]
    for c in merge:
        j = cols.index(c)
        new_groups = []
        for g0, g1 in groups:
            i = g0
            while i < g1:
                k = i
                while k + 1 < g1 and str(d.iloc[k + 1, j]) == str(d.iloc[i, j]):
                    k += 1
                spans[(i, j)] = k - i + 1
                covered.update((r, j) for r in range(i + 1, k + 1))
                new_groups.append((i, k + 1))
                i = k + 1
        groups = new_groups
    body = []
    for i in range(len(d)):
        row = []
        for j in range(len(cols)):
            if (i, j) in covered:
                continue
            v = str(d.iloc[i, j])
            row.append(C(v, rs=spans[(i, j)]) if spans.get((i, j), 1) > 1 else v)
        body.append(row)
    names = [(header or {}).get(c, str(c)) for c in cols]
    return CTable(header=[names], body=body, caption=caption, label=label, align=align,
                  notes=notes, **kw)



# --------------------------------------------------------------------------------------
# 14. Procedures and method validations a document cites, grouped by type
# --------------------------------------------------------------------------------------
def sop_references(sops=None, amvs=None, label: str = "tbl-sops") -> CTable:
    """The SOP and method-validation references (``_pcpkg.SOP_REFS`` / ``AMV_REFS`` by default),
    with the type as a merged first column, as a report groups them. The merged form of
    ``sop_table()``."""
    import _pcpkg as P
    sops = P.SOP_REFS if sops is None else sops
    amvs = P.AMV_REFS if amvs is None else amvs
    d = pd.DataFrame([["Standard operating procedure", i, t] for i, t in sops]
                     + [["Analytical method validation", i, t] for i, t in amvs],
                     columns=["Type", "Reference", "Title"])
    return frame(d, "Procedures and method validations referenced in this document.", label,
                 merge=["Type"], align=["P{3.0cm}", "l", "P{9.5cm}"])
