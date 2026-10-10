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
def _minus(s: str) -> str:
    """A formatted number with a true minus sign, and no sign on a value that rounds to zero
    ("−0.00"). The tables printed negatives with a hyphen (PCR-006 author, 2026-10-10)."""
    if s.startswith("-"):
        return ("−" + s[1:]) if any(ch in "123456789" for ch in s) else s[1:]
    return s


def num(v, nd=None) -> str:
    """A value as a table shows it. NaN is "n.t." (not tested); inf is "–"."""
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "n.t."
    v = float(v)
    if math.isinf(v):
        return "–"
    if nd is not None:
        return _minus(f"{v:,.{nd}f}")
    a = abs(v)
    if a >= 1000:
        return _minus(f"{v:,.0f}")
    if a >= 100:
        return _minus(f"{v:.0f}")
    if a >= 10:
        return _minus(f"{v:.1f}")
    return _minus(f"{v:.2f}")


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
def step_mid(key: str) -> str:
    """A step's name inside a sentence: "low-pH viral inactivation", but "Protein A" and "UF/DF"."""
    n = STEP_NAME[key]
    return n if (n.startswith("Protein A") or n[:2].isupper()) else n[0].lower() + n[1:]


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
        ("a)", "In the Protein A and low-pH viral inactivation pools part of the host cell protein "
               f"elutes in the SEC low molecular weight window. Reported for information only ({amd['id']})."),
        # the hold studies were made after AMD-001 and measured fragments by nrCE-SDS directly
        # (owner, 2026-10-09), so the retests covered the response-surface samples only
        ("b)", f"Retained samples of the response-surface design, tested {ret['start']} to {ret['end']}."),
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
        align, cap = "lll", f"Methods used for size variants in the designed studies, {step_mid(steps[0])}."
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
                    basis, m = "DS criterion^a)^", "a)"
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
               "value than the platform worst case. The one-sided 95 % prediction bound of a single "
               "batch there replaced it."),
        ("c)", "Log reduction claimed for this step in the modular viral clearance claim."),
        ("d)", "Cumulative requirement across the steps that clear the virus."),
        ("e)", "The one-sided 95 % prediction bound of a single batch at a downstream step's A-Mab "
               "worst case within its NOR was better than the platform worst case. The bound replaced "
               "it."),
    ]
    step_h = [] if one_step else [C("Step output", rs=2)]
    step_a = [] if one_step else ["P{2.9cm}"]      # one line for most step names
    return CTable(
        header=[[C("Attribute", rs=2), C("DS criterion", rs=2), *step_h,
                 C("Downstream worst case\n(platform or verified)", cs=2), C("IAC", rs=2),
                 C("Basis", rs=2)],
                ["Clearance factor", "Increase"]],
        body=body, align=["P{2.4cm}", "l", *step_a, "r", "r", "l", "P{2.6cm}"], size="footnotesize",
        notes=[n for n in notes if n[0] in marks] + [("", "DS, drug substance. IAC, intermediate acceptance criterion. Increase, in the unit of the criterion.")] + [("", "Computed from unrounded values. A criterion recomputed from the rounded values shown can differ in its last digit.")], notes_per_row=True,
        caption=("Intermediate acceptance criteria" + (f" for the {step_mid(t['step_key'].iloc[0])} "
                 "output" if one_step else "") + " and their derivation from the drug-substance criteria."),
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
            # the state of the Version 1.0 criterion in its own column, a dash for the rule: centred
            # across both, "none" read as either (PCP-006 review run 2)
            if o.empty and cqa == "fragments_lmw":
                ocells = ["not assessed^c)^", "–"]
                marks.add("c)")
            elif o.empty:
                ocells = ["none^a)^", "–"]
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
                    # say what the criterion was tightened or widened FROM: beside a Version 1.0
                    # value three times smaller, "tightened" alone read as wrong (PCP-006 review)
                    t_, w_ = "tightened" in b_, "widened" in b_
                    short = ("Carried back, " + " and ".join(
                        [x for x, f in (("tightened^d)^", t_), ("widened^e)^", w_)) if f])
                        + " from " + crit(nrow["iac_low_apriori"], nrow["iac_high_apriori"], nrow["spec_type"]))
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
             # "an adequate model" read as all four criteria of PCMP-001 §7.2; the widening rule asks
             # the first three (PCMP-001 §7.5 rule 2; PCP-007 review run 2, 2026-10-10)
             ("e)", "Widened on verification: a downstream step did better than the platform worst "
                    "case at the one-sided 95 % prediction bound of a single batch, on a model that "
                    "meets the first three adequacy criteria of PCMP-001 §7.2.")]
    old_rules = {_rule_code(r): r for r in old["rule"].unique()}
    # a subtraction in a recorded rule is shown with a minus sign, not a hyphen
    notes += [(c, f"Version 1.0 rule: {old_rules[c].replace(' - ', ' − ')}.") for c in sorted(old_rules)]
    header = [[C("Step", rs=2), C("Attribute", rs=2), C("Version 1.0^b)^", cs=2), C("Version 2.0", cs=2)],
              ["Criterion", "Rule", "Criterion", "Basis"]]
    # wide enough that an attribute and a Version 1.0 rule take one line each: the table for the
    # whole train otherwise runs past the foot of its page (INV-001 Table 3.1)
    align = ["P{2.3cm}", "P{3.6cm}", "l", "P{2.3cm}", "l", "P{3.3cm}"]
    if len(by_step) == 1:
        header, body = _drop_step_column(header, body)
        align = align[1:]
    return CTable(
        header=header,
        body=body, align=align,
        notes=[x for x in notes if x[0] in marks], notes_per_row=True, size="footnotesize",
        caption="Acceptance criteria for the step outputs in Version 1.0 and Version 2.0"
                + (f", {step_mid(next(iter(by_step)))}." if len(by_step) == 1 else "."),
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
    """The hold study of one intermediate. The hold studies were made during the Version 2.0
    re-analysis, after AMD-001 (owner, 2026-10-09), so fragments are by nrCE-SDS on every sample and
    an SEC fragment column appears only where the method plan still lists SEC for the study."""
    h = _csv(f"hold_{pool}.csv")
    sec = "lmw_sec_pct" in h and h["lmw_sec_pct"].notna().any()
    body = []
    for temp, g in h.groupby("temperature", sort=False):
        for i, (_, r) in enumerate(g.iterrows()):
            row = ([C(temp, rs=len(g))] if i == 0 else []) + [
                str(int(r["day"])), num(r["hmw_pct"])] + ([num(r["lmw_sec_pct"])] if sec else []) + [
                (num(r["lmw_cesds_pct"]) if not pd.isna(r["lmw_cesds_pct"]) else "n.t."),
                num(r["acidic_pct"], 1)]
            body.append(row)
    sub = ["HMW (SEC)"] + (["LMW (SEC)^a)^"] if sec else []) + ["LMW (nrCE-SDS)"]
    notes = ([("a)", "Every SEC result for low molecular weight species includes host cell protein "
                     "eluting in that window (AMD-001). Not used for evaluation.")] if sec else [])
    return CTable(
        header=[[C("Storage", rs=2), C("Day", rs=2), C("Size variants (%)", cs=len(sub)),
                 C("Acidic variants (%)", rs=2)], sub],
        body=body, align="l" + "r" * (len(sub) + 2), style="grid", notes=notes,
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
            kind = ("Clearance factor, lowest" if r["assumption"] == "fold_min" else
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
            if pd.isna(r["predicted_nor"]):
                camp = [C("not a response^a)^", cs=4)]          # nothing to verify: one cell
            else:
                camp = [nt(r["observed_edge"]), nt(r["predicted_nor"]), nt(r["predicted_nor_bound95"]), out]
            row = ([C(STEP_NAME[sk], rs=len(g))] if i == 0 else []) + [
                ATTR_NAME[r["cqa"]].split(" (")[0], *kcell, num(r["assumed"]), *camp]
            body.append(row)
    notes = [("a)", "Not a response of the response-surface study at this step, so the platform "
                    "value stands unverified."),
             ("b)", "The criteria upstream of this step were recalculated with the one-sided 95 % "
                    "prediction bound of a single batch at the value predicted within the NOR."),
             ("c)", "The one-sided 95 % prediction bound of a single batch is better than the platform "
                    "worst case. The criteria upstream of this step were recalculated with the bound."),
             ("d)", "The one-sided 95 % prediction bound of a single batch is better than the platform "
                    "worst case, but the model is not adequate by the criteria of PCMP-001: it fails a "
                    "test, or it fits the results exactly and the tests cannot be applied. The platform "
                    "value stands.")]
    used = {m for row in body for c in row for m in re.findall(r"\^([a-d]\))\^", str(getattr(c, "text", c)))}
    rounding = [("", "Computed from unrounded values. A criterion recomputed from the rounded values shown can differ in its last digit.")]
    return CTable(
        # "Platform" spans two header rows, so it takes no align: an aligned cell becomes \multicolumn{1}{c},
        # inside which multirow's "=" width is the whole line width, and the table was shrunk to 4.5 pt to
        # fit (INV-001 final pass, 2026-10-09). It sits right-aligned over its right-aligned values.
        header=[[C("Step", rs=2), C("Attribute", rs=2), C("Worst case", rs=2), C("Platform", rs=2),
                 C("This campaign", cs=3, align="c"), C("Outcome", rs=2)],
                # centred in fixed-width columns: right-aligned two-line labels in narrow columns ran
                # into each other (INV-001 and PCR-005 reviews, 2026-10-08)
                [C("At the\nedges", align="c"), C("Within\nthe NOR", align="c"), C("95 %\nbound", align="c")]],
        body=body, align=["P{2.2cm}", "P{2.4cm}", "P{2.6cm}", "R{1.5cm}", "R{1.5cm}", "R{1.5cm}", "R{1.5cm}", "P{2.7cm}"],
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


# one-word response labels for the DoE tables, defined in a note of each table that uses them
RESP_SHORT = {"leached_protein_a_ppm": "LPA"}
RESP_SHORT_LEGEND = {"leached_protein_a_ppm": "leached Protein A"}


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
    # kind "aug": the INV-002 augmentation runs of the step (block 2)
    name = f"doe_{step}_{kind}{'_superseded' if superseded else ''}.csv"
    d = _csv(name)
    factors = [c[len("coded_"):] for c in d.columns if c.startswith("coded_")]
    resps = [r for r in st.DOE_RESPONSES[step] if r in d.columns]
    lmw = [c for c in ("lmw_sec_pct", "lmw_cesds_pct") if c in d.columns]
    # a column with no result in any run says nothing; a note names it instead
    untested = [c for c in resps + lmw if d[c].isna().all()]
    resps = [r for r in resps if r not in untested]
    lmw = [c for c in lmw if c not in untested]
    devs = {} if (superseded or kind == "aug") else _deviation_runs(step, kind)
    # factors as letter codes with their units; the note gives the names (owner, 2026-10-08). The codes are the
    # report's own (D.factor_letters, screening order), not the column positions: the bioreactor response-surface
    # file orders duration before pCO2, so positions gave C and D where the report says E and C (PCR-003 check)
    import doe_report as D
    letters = D.factor_letters(step)
    codes = [letters.get(f, chr(ord("A") + i)) for i, f in enumerate(factors)]
    fl, fu, fnote = [], [], []
    for k, f in zip(codes, factors):
        p = cfg.unit_op(step).param(f)
        unit = re.sub(r"\s*\(.*\)$", "", p.unit)       # "AU (OD280, descending)" -> "AU"
        fl.append(k)
        fu.append(unit)
        name = p.name[0].lower() + p.name[1:] if p.name[1:2].islower() else p.name
        fnote.append(f"{k}, {name}" + (f" ({p.unit.replace(' (', ', ').rstrip(')')})" if unit != p.unit else ""))
    factor_note = ". ".join(fnote) + "."
    # three header rows, one line each: the group, the factor code or response, and its unit
    # (PCR-005 review, 2026-10-08: units wrapped under the labels into four- and five-line headers)
    rl_, ru_ = [], []
    for r_ in resps:
        m_ = re.fullmatch(r"(.*?) \((.*)\)", RESP_LABEL.get(r_, r_))
        lab_, u_ = (m_.group(1), m_.group(2)) if m_ else (RESP_LABEL.get(r_, r_), "")
        rl_.append(RESP_SHORT.get(r_, lab_))
        ru_.append(u_ or ("log10" if r_.endswith("_lrf") else ""))
    head1 = [C("Run", rs=3), C("Type", rs=3), C("Factor settings", cs=len(factors)),
             C("Responses", cs=len(resps))]
    head2 = fl + rl_
    head3 = fu + ru_
    if lmw:
        head1.append(C("Fragments, LMW", cs=len(lmw)))
        head2 += ["SEC" if c == "lmw_sec_pct" else "nrCE-SDS" for c in lmw]
        head3 += ["%"] * len(lmw)
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
    # run types in blocks: one merged cell per run of consecutive identical types
    i = 0
    while i < len(body):
        j = i
        while j + 1 < len(body) and body[j + 1][1] == body[i][1]:
            j += 1
        if j > i:
            body[i][1] = C(body[i][1], rs=j - i + 1)
            for k_ in range(i + 1, j + 1):
                body[k_].pop(1)
        i = j + 1
    dev = _csv("deviations.csv").set_index("dev_id")
    import doe_report as D
    corr = {d_: (f_, v_) for _, f_, v_, d_ in D.setting_corrections(step, kind)} if not superseded else {}
    pname = {p.key: p.name for p in cfg.unit_op(step).parameters}
    notes = [(mk, f"{did}: {dev.loc[did, 'summary']}. Run retained"
                  + (f", and analysed at the recorded {pname[corr[did][0]][:1].lower() + pname[corr[did][0]][1:]} "
                     f"of {corr[did][1]:g} in Version 2.0" if did in corr else "") + ".")
             for did, mk in marks.items()]
    notes.append(("", f"Factors: {factor_note}"))
    short = [f"{RESP_SHORT[r_]}, {RESP_SHORT_LEGEND[r_]}" for r_ in resps if r_ in RESP_SHORT]
    if short:
        notes.append(("", ". ".join(short) + "."))
    if lmw and step in ("protein_a", "viral_inactivation") and "lmw_sec_pct" in lmw:
        notes.append(("", "LMW by SEC is biased in this matrix and is not used for evaluation (AMD-001)."))
    if any(d[c].isna().any() for c in resps + lmw):
        notes.append(("", "n.t. = not tested."))
    if untested:
        lab = lambda c: {"lmw_sec_pct": "LMW by SEC", "lmw_cesds_pct": "LMW by nrCE-SDS"}.get(c, RESP_LABEL.get(c, c))
        notes.append(("", f"Not tested in this design: {', '.join(lab(c) for c in untested)}."))
    title = {"screening": "screening", "rsm": "response-surface", "aug": "augmentation"}[kind]
    return CTable(
        header=[head1, head2, head3], body=body, align=["l", "l"] + ["R{1.35cm}"] * len(head2),
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
    """Each step output against its IAC, at manufacturing scale: the model's prediction at the
    set-point and its range over the NOR box of the response-surface factors, and whether the
    criterion is met across the NOR. An output with no adequate model (PCMP-001 §7.2) shows the
    range of its measured results instead and is judged on them; an output modelled on the log
    scale shows the median (its back-transformed mean)."""
    import itertools
    import doe_report as D
    cfg = _cfg()
    t = _csv("iac.csv")
    t = t[t["step_key"] == step]
    body, any_off, any_meas, any_log, any_ratio = [], False, False, False, False
    for _, r in t.iterrows():
        resp = r["response"]
        try:
            res = D.fit(step, "rsm", resp)
        except Exception:
            continue
        uo = cfg.unit_op(step)
        fac = res["factors"]
        kind, v = D._offset(step, resp)
        any_off = any_off or v != (1.0 if kind == "ratio" else 0.0)
        any_ratio = any_ratio or kind == "ratio"
        ok = bool(D.nor_met(step, resp))
        if res["status"] == "none":
            # no adequate model sets a range: the measured results, at manufacturing scale
            m = D.to_mfg(step, resp, D.measured_values(step, resp))
            any_meas = True
            body.append([ATTR_NAME[r["cqa"]], crit(r["iac_low"], r["iac_high"], r["spec_type"]),
                         "n.a.^c)^", f"{num(m.min())} to {num(m.max())}^c)^", "Yes" if ok else "No"])
            continue
        grid = list(itertools.product(*[[uo.param(f).nor[0], uo.param(f).setpoint, uo.param(f).nor[1]] for f in fac]))
        y = D.to_mfg(step, resp, D.predict(step, resp, natural={f: [g[i] for g in grid] for i, f in enumerate(fac)}))
        lo, hi = float(np.min(y)), float(np.max(y))
        sp = float(D.to_mfg(step, resp, D.predict(step, resp, natural={f: uo.param(f).setpoint for f in fac}))[0])
        lg = res.get("transform") == "log"
        any_log = any_log or lg
        mk = "^d)^" if lg else ""
        body.append([ATTR_NAME[r["cqa"]], crit(r["iac_low"], r["iac_high"], r["spec_type"]),
                     num(sp) + mk, f"{num(lo)} to {num(hi)}" + mk, "Yes" if ok else "No"])
    notes = [("a)", "Judged at every combination of NOR low, set-point and NOR high. Quality "
                    "attributes: the 95 % prediction interval of a single run (t quantile, coefficient "
                    "and residual uncertainty)."
                    + (" Viral clearance: the mean prediction." if any(str(x).startswith("lrv")
                                                                      for x in t["cqa"]) else ""))]
    if any_off:
        notes.append(("b)", "At manufacturing scale: the scale-down prediction minus the offset of the "
                            "scale-down model for this output"
                            + (", or divided by it where the offset is a ratio" if any_ratio else "") + "."))
    if any_meas:
        # "at manufacturing scale" alone was wrong for an output with no known offset, such as
        # fragments (PCR-006 author, 2026-10-10)
        notes.append(("c)", "No adequate model (PCMP-001 §7.2): the range of the measured results of the "
                            "designs, less the offset of the scale-down model where one is known, on which "
                            "the output is judged."))
    if any_log:
        notes.append(("d)", "Modelled on the log scale: the median, the back-transformed mean "
                            "prediction."))
    return CTable(
        header=[[C("Attribute", rs=2), C("Criterion", rs=2), C("Mean predicted by the response-surface model" + ("^b)^" if any_off else ""), cs=2), C("Met across\nthe NOR^a)^", rs=2)],
                ["At the set-point", "Range over the NOR"]],
        body=body, align="llrrl", notes=notes, notes_per_row=True,
        caption=f"{STEP_NAME[step]} outputs against their intermediate acceptance criteria.",
        label=label or f"tbl-criteria-{step.replace('_', '-')}")


# --------------------------------------------------------------------------------------
# 9. Process parameters, grouped by step
# --------------------------------------------------------------------------------------
def nor_change(par) -> Optional[str]:
    """How the NOR in force differs from the NOR as characterized: "narrowed" (inside it),
    "moved" (same width, shifted), "moved and narrowed", or None when unchanged. The pH NOR of
    low-pH inactivation moved at Version 2.0 and did not narrow (PCMP-001 author, 2026-10-09)."""
    (lo0, hi0), (lo1, hi1) = map(float, par.nor_characterized), map(float, par.nor)
    if (lo0, hi0) == (lo1, hi1):
        return None
    if lo1 >= lo0 and hi1 <= hi0:
        return "narrowed"
    if math.isclose(hi1 - lo1, hi0 - lo0, rel_tol=1e-9, abs_tol=1e-9):
        return "moved"
    if hi1 - lo1 < hi0 - lo0:
        return "moved and narrowed"
    raise ValueError(f"{par.name}: the NOR in force {lo1}–{hi1} is wider than the NOR as "
                     f"characterized {lo0}–{hi0}, which no Version 2.0 decision allows")


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
                # a Version 2.0 report narrowed or moved this NOR; the note gives the NOR the studies used
                m = f"c{len([u for u in used if u.startswith('c')]) + 1})"
                nor[-1] = f"{nor[-1]}^{m}^"
                used.add(m)
                wu = lambda v_: f"pH {v_}" if par.unit == "pH" else f"{v_} {par.unit}"
                narrowed.append((m, f"{nor_change(par).capitalize()} at Version 2.0 from "
                                    f"{wu(pval(par.nor_characterized[0]) + '–' + pval(par.nor_characterized[1]))}, "
                                    f"the NOR as characterized (PCR-{uo.step:03d})."))
            sp_txt = pval(r["setpoint"])
            if par.setpoint_characterized is not None and float(par.setpoint) != float(par.setpoint_characterized):
                # a Version 2.0 report moved this set-point; the studies ran around the former one
                m = f"c{len([u for u in used if u.startswith('c')]) + 1})"
                sp_txt = f"{pval(par.setpoint)}^{m}^"
                used.add(m)
                wu = lambda v_: f"pH {v_}" if par.unit == "pH" else f"{v_} {par.unit}"
                # the set-point of the plan, not "the set-point the studies were run around": the low-pH
                # designs were centred elsewhere (PTP-001 factual check, 2026-10-10)
                narrowed.append((m, f"Moved at Version 2.0 from {wu(pval(par.setpoint_characterized))}, "
                                    f"the set-point in the characterization plan (PCR-{uo.step:03d})."))
            # the study type as a mark on the parameter, not a column of its own: with that column
            # the table for the whole train ran 58 pt into the page foot of PCMP-001 (2026-10-10)
            pname = r["parameter"]
            if r["study"] != "multivariate":
                pname += "^b)^"
                used.add("b)")
            row = ([C(STEP_NAME[k], rs=len(g))] if i == 0 else []) + [
                pname, r["unit"], sp_txt, *nor,
                f"{pval(par.prange[0])}–{pval(par.prange[1])}", r["classification"]]
            body.append(row)
    notes = [("a)", "The normal operating range equals the characterized range."),
             ("b)", "Studied one factor at a time. Every other parameter was studied in the designed "
                    "experiments of its step.")] + narrowed
    return CTable(
        header=[["Step", "Parameter", "Unit", "Set-point", "NOR", "Characterized\nrange", "Class"]],
        body=body, align=["P{1.8cm}", "P{4.0cm}", "P{2.6cm}", "r", "P{2.2cm}", "l", "l"],
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
    # the studies Version 1.0 reported (finding F5), not those of the re-analysis
    chron = chron[chron["end"].astype(str) < rev1]
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
    # 2026-10-10 (owner's decisions Q5 and Q8): the further outputs the Version 1.0 plans compared
    "dna_pool_pg_mg": ("Residual DNA", "pg/mg", 1), "lpa_pool_ppm": ("Leached Protein A", "ppm", 2),
    "ds_concentration_g_per_l": ("Final concentration", "g/L", 1), "flux_lmh": ("Permeate flux", "LMH", 1),
}


def _DOE_STEPS():
    """The steps with a response-surface design."""
    from amab_process import studies as _st
    return set(_st.DOE_FACTORS)


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
            ratio = q.get("scale") == "ratio"           # an output modelled on the log scale
            ko = 1.0 if ratio else k
            rows.append({"step_key": step, "output": col, "n_sd": q["n_sd"], "n_m": q["n_m"],
                         "mean_sd": q["mean_sd"] * k, "mean_m": q["mean_m"] * k, "ratio": ratio,
                         "offset": q["offset"] * ko, "lo": q["lo"] * ko, "hi": q["hi"] * ko,
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
        # run counts are usually the same for every output of a step: one merged cell, not a
        # column repeating one number (PCR-005 review, 2026-10-08)
        same_n = g["n_sd"].nunique() == 1 and g["n_m"].nunique() == 1
        for i, (_, r) in enumerate(g.iterrows()):
            name, unit, nd = SDM_OUTPUT[r["output"]]
            f = lambda v: _minus(f"{v:,.{nd}f}")
            lead = [C(STEP_NAME[sk], rs=len(g))] if i == 0 else []
            if r["judged"]:
                concl = [f"{yn(r['met_lo'])} / {yn(r['met_point'])} / {yn(r['met_hi'])}"]
                q = yn(r["qualified"])
            elif sk not in _DOE_STEPS():
                # a step with no designed experiment (UF/DF): its outputs may carry a criterion, but
                # PCMP-001 §7.1 decides qualification on the response-surface model (PCP-010 author)
                concl = ["no model^c)^"]
                q = "n.a.^c)^"
            else:
                concl = ["no criterion^a)^"]
                q = "n.a.^a)^"
            if not same_n:
                runs = [str(r["n_sd"]), str(r["n_m"])]
            elif i == 0:
                runs = [C(str(r["n_sd"]), rs=len(g)), C(str(r["n_m"]), rs=len(g))]
            else:
                runs = []
            if r.get("ratio"):
                # modelled on the log scale: geometric means, and the offset as a ratio
                g3 = lambda v: f"{v:.3f}"
                cells = [f(r["mean_sd"]) + "^b)^", f(r["mean_m"]) + "^b)^", "×" + g3(r["offset"]) + "^b)^",
                         f"×{g3(r['lo'])} to ×{g3(r['hi'])}"]
            else:
                cells = [f(r["mean_sd"]), f(r["mean_m"]), f(r["offset"]), f"{f(r['lo'])} to {f(r['hi'])}"]
            body.append(lead + [name + (f" ({unit})" if unit else ""), *runs, *cells, *concl, q])
    notes = [("a)", "The output has no acceptance criterion at this step, so no conclusion depends "
                    "on its offset and qualification does not apply. The offset is recorded."),
             ("b)", "Modelled on the log scale: geometric means, and the offset as the ratio of the "
                    "scale-down to the manufacturing geometric mean. The manufacturing-scale value is "
                    "the scale-down value divided by the ratio."),
             ("c)", "The step has no response-surface model, and PCMP-001 §7.1 decides the qualification "
                    "on that model. The offset is recorded, and the report states how it is used.")]
    doe = _DOE_STEPS()
    used = any((not j) and k in doe for j, k in zip(t["judged"], t["step_key"]))
    used_nomodel = any((not j) and k not in doe for j, k in zip(t["judged"], t["step_key"]))
    used_ratio = bool(t.get("ratio", pd.Series(dtype=bool)).fillna(False).astype(bool).any())
    from amab_process.config import _NOR_MODE
    which = "the NOR as characterized" if _NOR_MODE["mode"] == "characterized" else "the NOR in force"
    legend = [("", "SDM, scale-down model. Mfg, manufacturing scale. Offset, scale-down mean minus "
                   "manufacturing mean. Met over NOR: the criterion is met at every combination of NOR "
                   f"low, set-point and NOR high ({which}), with the offset at the low end of its "
                   "interval, at its estimate (est.) and at the high end.")]
    header = [[C("Step", rs=2), C("Output", rs=2), C("Runs", cs=2),
                 C("Mean", cs=2), C("Offset", cs=2),
                 C("Met over NOR\n(low/est./high)", rs=2), C("Qualified", rs=2)],
                ["SDM", "Mfg", "SDM", "Mfg", "Estimate", f"{ci} % CI"]]
    align = ["P{2.0cm}", "P{2.6cm}", "c", "c", "r", "r", "r", "r", "P{2.4cm}", "c"]   # the CI on one line
    one = t["step_key"].nunique() == 1
    if one:
        header, body = _drop_step_column(header, body)
        align = align[1:]
    sub = (f", {step_mid(t['step_key'].iloc[0])}" if one else "") + (
        ", planned runs only" if studies else "")
    return CTable(
        header=header, body=body, align=align,
        size="footnotesize",
        notes=[n for n in notes if (n[0] == "a)" and used) or (n[0] == "b)" and used_ratio)
               or (n[0] == "c)" and used_nomodel)] + legend,
        notes_per_row=True,
        caption=caption or ("Offsets of the scale-down models (scale-down minus manufacturing scale) "
                            f"and the qualification of each model for each output{sub}."),
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
    # a performance output (turbidity, residual buffer, concentration) is not an attribute
    cqa = D.RESP_TO_CQA.get(resp, resp)
    return cqa if cqa in set(_csv("cqa_register.csv")["key"]) else None


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
            pv = fr["model"].pvalues.drop(["const", "block"], errors="ignore")   # a block is not an effect
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
    # one row per reference: a document may join a step list and the shared list, and a reference
    # in both must not print twice (keep the first)
    sops = [(i, t) for k, (i, t) in enumerate(sops) if i not in [x for x, _ in list(sops)[:k]]]
    amvs = [(i, t) for k, (i, t) in enumerate(amvs) if i not in [x for x, _ in list(amvs)[:k]]]
    d = pd.DataFrame([["Standard operating procedure", i, t] for i, t in sops]
                     + [["Analytical method validation", i, t] for i, t in amvs],
                     columns=["Type", "Reference", "Title"])
    return frame(d, "Procedures and method validations referenced in this document.", label,
                 merge=["Type"], align=["P{3.0cm}", "l", "P{9.5cm}"])


# --------------------------------------------------------------------------------------
# 14. Model adequacy and the INV-002 augmentations (PCMP-001 §7.2)
# --------------------------------------------------------------------------------------
REMEDY_TEXT = {"augment": "Augmentation", "refit": "Refit", "none": "–"}
REASON_TEXT = {
    "attribute of the drug substance specification with an effect":
        "Attribute of the drug substance specification, with an effect",
    "not a drug substance test": "Viral clearance, not a drug substance test",
    "no effect to resolve": "No effect to resolve",
    "assurance not reached within the size of the planned design":
        "Probability of success not reached within the size of the planned design",
}


def _attr_label(resp: str, step: str) -> str:
    cqa = _resp_cqa(resp, step)
    return ATTR_NAME.get(cqa, resp) if cqa else resp


def _term_name(term: str, step: str) -> str:
    """A model term in words: "pH", "pH × culture duration", "culture duration²"."""
    names = {p.key: p.name for p in _cfg().unit_op(step).parameters}
    nm = lambda k: (lambda n: n[0].lower() + n[1:] if n[1:2].islower() else n)(names.get(k, k))
    if ":" in term:
        a, b = term.split(":")
        return f"{nm(a)} × {nm(b)}"
    if term.endswith("^2"):
        return nm(term[:-2]) + "²"
    return nm(term)


def _terms_text(terms, step: str) -> str:
    """Model terms in words, joined, the first capitalised."""
    t = ", ".join(_term_name(x, step) for x in terms)
    return t[:1].upper() + t[1:]


def model_adequacy(steps: Optional[List[str]] = None, failing_only: bool = True,
                   label: str = "tbl-model-adequacy") -> CTable:
    """The full quadratic models of the planned response-surface runs against PCMP-001 §7.2, one
    block per step: runs, terms, R², predicted R², their difference, and the two p-values."""
    t = _csv("model_adequacy.csv")
    th = _cfg().raw()["campaign"]["thresholds"]
    if steps:
        t = t[t["step_key"].isin(steps)]
    if failing_only:
        t = t[~t["adequate"].astype(bool)]
    body = []
    for sk, g in t.groupby("step_key", sort=False):
        for i, (_, r) in enumerate(g.iterrows()):
            body.append(([C(STEP_NAME[sk], rs=len(g))] if i == 0 else []) + [
                _attr_label(r["response"], sk), str(int(r["n"])), str(int(r["k"])),
                f"{r['R2']:.2f}", f"{r['predR2']:.2f}", f"{r['gap']:.2f}",
                f"{r['p_lof']:.3f}", "<0.001" if r["p_model"] < 0.001 else f"{r['p_model']:.3f}"])
    return CTable(
        header=[[C("Step", rs=2), C("Attribute", rs=2), C("Runs", rs=2), C("Terms", rs=2),
                 C("R²", rs=2), C("Predicted\nR²", rs=2), C("R² minus\npredicted R²", rs=2),
                 C("p-value", cs=2)], ["Lack of fit", "Model"]],
        body=body, align=["P{2.4cm}", "P{4.4cm}", "r", "r", "r", "r", "r", "r", "r"],
        notes=[("", f"Full quadratic model on the planned runs. Terms include the intercept. PCMP-001 "
                    f"§7.2 requires a significant model F-test (α = {float(th['effect_alpha']):g}), no "
                    f"significant lack of fit (α = {float(th['lof_alpha']):g}) and R² minus predicted R² of "
                    f"at most {float(th['max_r2_minus_pred_r2']):.2f}. R² minus predicted R² is calculated "
                    "before rounding.")],
        notes_per_row=True, size="footnotesize",
        caption="Response-surface models that do not meet the model-adequacy criteria of PCMP-001."
                if failing_only else "Model adequacy of the response-surface models.",
        label=label, resize=True)


def adequacy_remedy(steps: Optional[List[str]] = None, label: str = "tbl-remedy") -> CTable:
    """For each failing model: the effects the refit on the planned runs keeps, the runs an
    augmentation would need for the assurance target, and the remedy the rule of INV-002 gives."""
    t = _csv("model_adequacy.csv")
    t = t[~t["adequate"].astype(bool)]
    ma = _cfg().raw()["campaign"]["model_adequacy"]
    if steps:
        t = t[t["step_key"].isin(steps)]
    body = []
    for sk, g in t.groupby("step_key", sort=False):
        for i, (_, r) in enumerate(g.iterrows()):
            # the whole refit, with a main effect it keeps only because a term containing it remains
            # (not itself significant) in parentheses: a list of the significant terms alone read
            # as a refit that broke hierarchy (INV-002 review, 2026-10-09)
            eff = set(str(r["effects"]).split()) if isinstance(r["effects"], str) else set()
            red = str(r["reduced_terms"]).split() if isinstance(r["reduced_terms"], str) else []
            eff_t = ", ".join(_term_name(x, sk) if x in eff else f"({_term_name(x, sk)})" for x in red)
            eff_t = (eff_t[:1].upper() + eff_t[1:] if not eff_t.startswith("(")
                     else "(" + eff_t[1:2].upper() + eff_t[2:]) if eff_t else "None, the mean only"
            m_req = "–" if pd.isna(r["m_required"]) else str(int(r["m_required"]))
            rem = REMEDY_TEXT[r["remedy"]]
            if r["remedy"] == "augment":
                rem = "Augmentation^a)^"
            body.append(([C(STEP_NAME[sk], rs=len(g))] if i == 0 else []) + [
                _attr_label(r["response"], sk), eff_t, m_req, rem,
                REASON_TEXT.get(r["reason"], r["reason"])])
    return CTable(
        header=[["Step", "Attribute", "Terms of the refit\n(planned runs)^b)^", "Runs\nneeded",
                 "Remedy", "Reason"]],
        # landscape text width on letter paper with 1 in margins is 22.9 cm: at 4.2 cm the effects
        # column wrapped to six lines and the table ran off its page, and a table taller than the
        # text height leaves an empty landscape page before it (tables are placed [H]; INV-002
        # authoring, 2026-10-08)
        body=body, align=["P{2.0cm}", "P{3.6cm}", "P{7.0cm}", "r", "P{2.5cm}", "P{4.8cm}"],
        notes=[("a)", "The step's augmentation has the largest number of runs that any of the models "
                      "the rule augments at that step needs."),
               ("b)", "Terms significant at α = "
                      f"{float(_cfg().raw()['campaign']['thresholds']['effect_alpha']):g}. A main effect in "
                      "parentheses is not significant and is kept because an interaction or a square of "
                      "it remains in the refit."),
               ("", f"Runs needed: the smallest augmentation with a probability of success of at least "
                    f"{float(ma['assurance']):.2f}, at the effects of the planned runs, that the planned model "
                    "meets the lack-of-fit test and the limit on overfitting. A dash means not reached within "
                    "the size of the planned design, or not computed when the refit keeps no effect. For a "
                    "refitted model the number is what an augmentation would have needed, and no runs were made.")],
        notes_per_row=True, size="footnotesize", landscape=True,
        caption="Remedy of each model that does not meet the model-adequacy criteria.", label=label)


_ORDINAL = {1: "", 2: "second", 3: "third", 4: "fourth"}


def sample_size(steps: Optional[List[str]] = None, label: str = "tbl-sample-size") -> CTable:
    """The assurance curve of each failing model with an effect: the assurance with the planned
    runs alone and with 4, 8, … further runs, the size reached, and the power at that size."""
    g = _csv("augmentation_sample_size.csv")
    ma = _cfg().raw()["campaign"]["model_adequacy"]
    target = float(ma["assurance"])
    if steps:
        g = g[g["step_key"].isin(steps)]
    show = [0, 4, 8, 12, 16, 20, 24, 28]
    body = []
    for sk, gg in g.groupby("step_key", sort=False):
        resps = list(dict.fromkeys(gg["response"]))
        for i, resp in enumerate(resps):
            x = gg[gg["response"] == resp].set_index("m")
            # three decimals: at two, 0.895 to 0.899 printed as the 0.90 target (INV-002 review run 2)
            cells = [f"{x.loc[m, 'assurance']:.3f}" if m in x.index else "–" for m in show]
            hit = x[(x.index > 0) & (x["assurance"] >= target)]
            m_req = int(hit.index[0]) if len(hit) else None
            pw = "–" if m_req is None else (f"{x.loc[m_req, 'min_power']:.2f}"
                                            if not pd.isna(x.loc[m_req, "min_power"]) else "–")
            body.append(([C(STEP_NAME[sk], rs=len(resps))] if i == 0 else []) + [
                _attr_label(resp, sk), *cells, "–" if m_req is None else str(m_req), pw])
    return CTable(
        header=[[C("Step", rs=2), C("Attribute", rs=2), C("Probability of success with further runs", cs=len(show)),
                 C("Runs\nneeded", rs=2), C("Lowest\npower", rs=2)],
                [str(m) for m in show]],
        body=body, align=["P{2.2cm}", "P{3.2cm}"] + ["r"] * (len(show) + 2),
        # the wording INV-002 settled on after review run 1 (2026-10-09): what the simulation
        # conditions on, its scale, and why no size takes the assurance much above 1 - lof_alpha
        notes=[("", f"Probability of success: the probability, at the effects estimated from the planned runs, that the "
                    "planned model meets the lack-of-fit test and the limit on overfitting of PCMP-001 "
                    f"§7.2, estimated from {int(ma['reps']):,} simulated data sets. It does not include the "
                    "uncertainty of those estimates. The planned model is the full quadratic, with a block "
                    "term where there are further runs. The data are simulated on the raw scale from the "
                    "refit of the planned runs and its residual standard deviation. Further runs: a "
                    f"D-optimal augmentation of that size. Sizes in steps of {int(ma['step'])} were computed, "
                    f"and the table shows every {_ORDINAL[(show[1] - show[0]) // int(ma['step'])]} size. A dash in a "
                    "probability column marks a size larger "
                    "than the planned design, which was not computed. Runs needed: the smallest size with "
                    f"a probability of success of at least {target:.2f}, and a dash where it is not reached within the "
                    "size of the planned design. Lowest power: the power, at that size and α = "
                    f"{float(_cfg().raw()['campaign']['thresholds']['effect_alpha']):g}, of the weakest "
                    "significant effect of the refit. The lack-of-fit test rejects a correct model in "
                    f"{100 * float(_cfg().raw()['campaign']['thresholds']['lof_alpha']):g} % of data sets, so "
                    f"no size takes the probability much above {1 - float(_cfg().raw()['campaign']['thresholds']['lof_alpha']):.2f}.")],
        notes_per_row=True, size="footnotesize", landscape=True,
        caption="Probability of success that the planned model meets the lack-of-fit test and the limit on "
                "overfitting, by the number of further runs.", label=label)


def _name_unit(name: str, unit: str) -> str:
    """A parameter with its unit for a column header: "Load pH", "Culture temperature\n(°C)",
    "Dissolved CO2\n(pCO2, mmHg)" (no unit that only repeats the name, no double parentheses)."""
    if unit in ("", "pH") or name.endswith(unit):
        return name
    if name.endswith(")"):
        i = name.rindex("(")
        return name[:i].rstrip() + "\n" + name[i:-1] + ", " + unit + ")"
    return f"{name}\n({unit})"


def augmentation_design(step: str, label: Optional[str] = None) -> CTable:
    """The D-optimal augmentation of one step as INV-002 approved it: the coded points and their
    settings, in the order of the design (the execution order was randomized)."""
    a = _csv(f"doe_{step}_aug.csv")
    cfg = _cfg()
    factors = [c[len("coded_"):] for c in a.columns if c.startswith("coded_")]
    codes = [chr(ord("A") + i) for i in range(len(factors))]
    # one number of decimals per factor (6.60, 6.85, 7.10, not 6.6, 6.85, 7.1), and each setting
    # column headed by the factor's name, so two columns in the same unit are told apart without
    # the note (INV-002 review run 1, 2026-10-09)
    def _dec(v):
        t = f"{float(v):g}"
        return len(t.split(".")[1]) if "." in t else 0
    dec = {f: max(_dec(v) for v in a[f]) for f in factors}
    body = []
    for _, r in a.iterrows():
        body.append([str(int(r["run"]))] + [f"{int(round(r['coded_' + f])):+d}".replace("+0", "0")
                                            for f in factors]
                    + [f"{float(r[f]):.{dec[f]}f}" for f in factors])
    units = [re.sub(r"\s*\(.*\)$", "", cfg.unit_op(step).param(f).unit) for f in factors]
    names = [cfg.unit_op(step).param(f).name for f in factors]
    note = ". ".join(f"{k}, {n}" for k, n in zip(codes, names)) + "."
    return CTable(
        header=[[C("Run", rs=2), C("Coded level", cs=len(factors)), C("Setting", cs=len(factors))],
                codes + [f"{k}, " + _name_unit(n, u) for k, n, u in zip(codes, names, units)]],
        body=body, align=["r"] + ["c"] * len(factors) + ["R{2.1cm}"] * len(factors),
        notes=[("", "Factors: " + note), ("", "Block 2. Runs are numbered on from the planned "
                                              "design.")],
        notes_per_row=True, size="footnotesize",
        caption=f"D-optimal augmentation of the {step_mid(step)} "
                "response-surface design.",
        label=label or f"tbl-aug-design-{step.replace('_', '-')}")


def model_reevaluation(step: str, label: Optional[str] = None) -> CTable:
    """Each output of a step with a criterion: its full quadratic model on the planned runs, the
    same model with a block term on all runs where the step was augmented, and the model the
    output ends up with (PCMP-001 §7.2)."""
    import doe_report as D
    th = _cfg().raw()["campaign"]["thresholds"]
    crit = _cfg().raw()["iac"]["responses"].get(step, [])
    aug = D.has_augmentation(step)
    body = []
    for resp in [r for r in crit if r in D.rsm_data(step, "planned").columns]:
        p = D.fit(step, "rsm", resp, runs="planned", form="full")
        row = [_attr_label(resp, step), str(p["n"]), f"{p['R2']:.2f}", f"{p['predR2']:.2f}",
               f"{p['gap']:.2f}"]
        if aug:
            a = D.fit(step, "rsm", resp, runs="all", form="full")
            if a["block"]:
                pb = float(a["model"].pvalues.get("block"))
                row += [str(a["n"]), f"{a['R2']:.2f}", f"{a['predR2']:.2f}", f"{a['gap']:.2f}",
                        f"{a['p_lof']:.3f}", f"{pb:.3f}"]
            else:
                row += [C("not measured in the augmentation^a)^", cs=6)]
        u = D.fit(step, "rsm", resp)
        nm_ = [_term_name(t, step) for t in u["names"]]
        sc = ", log scale" if u.get("transform") == "log" else ""
        if u["status"] == "none":
            used = "None^b)^"
        elif not nm_:
            used = f"No effect{sc}"
        elif len(nm_) <= 3:
            used = ", ".join(nm_)[:1].upper() + ", ".join(nm_)[1:] + sc
        else:
            used = f"{len(nm_)} terms{sc}"
        row.append(used)
        body.append(row)
    head1 = [C("Attribute", rs=2), C("Planned runs, full quadratic", cs=4)]
    head2 = ["Runs", "R²", "Pred. R²", "Gap"]
    if aug:
        head1.append(C("All runs, full quadratic with block", cs=6))
        head2 += ["Runs", "R²", "Pred. R²", "Gap", "Lack of\nfit p", "Block p"]
    head1.append(C("Model used\n(terms)", rs=2))
    # a lettered note only where a cell cites it: a step without augmentation and with an adequate
    # model for every output printed both notes with no marker in the table (PCR-005, 2026-10-09)
    cited = {m for row in body for c in row for m in re.findall(r"\^([a-z]\))\^", str(getattr(c, "text", c)))}
    return CTable(
        header=[head1, head2], body=body,
        align=["P{3.2cm}"] + ["r"] * (len(head2)) + ["P{2.4cm}"],
        notes=[n for n in [("a)", "Viral clearance was not measured in the augmentation runs (INV-002)."),
                           ("b)", "No adequate model. The output is judged on its measured results.")]
               if n[0] in cited] + [
               ("", f"Gap: R² minus predicted R², at most {float(th['max_r2_minus_pred_r2']):.2f} "
                    "under PCMP-001 §7.2. Model used: the scale chosen by the Box-Cox profile and the "
                    "model with the lowest AICc among the hierarchical submodels of the full quadratic, "
                    "a block term kept (INV-002).")],
        notes_per_row=True, size="footnotesize", landscape=aug,
        caption="Re-evaluation of the response-surface models"
                + (" with the augmentation runs" if aug else "") + ".",
        label=label or f"tbl-reeval-{step.replace('_', '-')}")


# --------------------------------------------------------------------------------------
# 17. Support for the re-centred low-pH set-points (PCR-006, PD-006-01 and PD-006-02)
# --------------------------------------------------------------------------------------
def _p3(p) -> str:
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def _sgn(v, nd=2) -> str:
    """A signed difference, with no negative zero."""
    return f"{0.0:.{nd}f}" if round(abs(v), nd) == 0 else f"{v:+.{nd}f}".replace("-", "−")


def vi_ofat(label="tbl-vi-ofat") -> CTable:
    """S-VI-OFAT: every result of the low-pH hold at the re-centred and the former pH set-point."""
    d = _csv("vi_ofat.csv")
    ph = sorted(d["ph"].unique())
    o = _cfg().raw()["analytics"]["vi_ofat"]
    attrs = [("aggregate_out_pct", "Aggregate,\n% HMW (SEC)"), ("lmw_cesds_pct", "Fragments,\n% LMW (nrCE-SDS)"),
             ("acidic_variants", "Acidic variants,\n% (icIEF)")]
    body = []
    for t, g in d.groupby("hold_min", sort=True):
        reps = sorted(g["replicate"].unique())
        for i, rep in enumerate(reps):
            row = ([C(str(int(t)), rs=len(reps))] if i == 0 else []) + [str(int(rep))]
            for resp, _ in attrs:
                for p in ph:
                    v = g[(g["ph"] == p) & (g["replicate"] == rep)][resp]
                    row.append(num(float(v.iloc[0]), 2))
            body.append(row)
    return CTable(
        header=[[C("Hold time\n(min)", rs=2), C("Repli-\ncate", rs=2)] + [C(h, cs=len(ph)) for _, h in attrs],
                [f"pH {p:.2f}" for _ in attrs for p in ph]],
        body=body, align="ll" + "r" * (len(attrs) * len(ph)),
        notes=[("", f"Temperature {o['temperature']:g} °C. Time 0 is the load after pH adjustment, before "
                    "the hold. Each hold time was run in duplicate at each pH.")],
        size="footnotesize",
        caption="Quality attributes over the low-pH hold at the re-centred and the former pH set-point "
                "(study S-VI-OFAT).", label=label)


def ofat_effects(label="tbl-vi-ofat-effects") -> CTable:
    """S-VI-OFAT: the analysis of covariance of each attribute on pH and hold time."""
    import doe_report as D
    a = D.ofat_analysis()
    o = _cfg().raw()["analytics"]["vi_ofat"]
    new, old = sorted(o["ph"])[0], sorted(o["ph"])[1]
    hold_nor = _cfg().unit_op("viral_inactivation").param("hold_time").nor
    body = []
    for r in a.itertuples():
        spec = ("two_sided" if not math.isnan(r.crit_lo) and not math.isnan(r.crit_hi)
                else "upper" if not math.isnan(r.crit_hi) else "lower")
        body.append([r.attribute, r.method, num(r.mean_new, 2), num(r.mean_old, 2),
                     f"{_sgn(r.ph_effect)} ({_sgn(r.ph_lo)} to {_sgn(r.ph_hi)})", _p3(r.p_ph_holm),
                     _p3(r.p_interaction), _sgn(r.slope_60), num(r.method_sd, 2),
                     f"{num(r.min_nor, 2)}–{num(r.max_nor, 2)}", crit(r.crit_lo, r.crit_hi, spec)])
    return CTable(
        header=[[C("Attribute", rs=2), C("Method", rs=2), C("Mean", cs=2),
                 C(f"Effect of pH {new:.2f} against pH {old:.2f}", cs=2),
                 C("pH × hold\ntime, p^c)^", rs=2), C("Change per\n60 min^d)^", rs=2),
                 C("Method\nrepeat-\nability, SD^e)^", rs=2), C(f"Results at\npH {new:.2f}^f)^", rs=2),
                 C("Criterion\nof the step", rs=2)],
                [f"pH {new:.2f}", f"pH {old:.2f}", "Difference\n(95 % CI)^a)^", "p^b)^"]],
        body=body, align=["l", "l", "r", "r", "P{3.6cm}", "r", "r", "r", "r", "r", "r"],
        notes=[("a)", "Difference of the means at any hold time, from a model of the result on pH (two "
                      "levels) and hold time, in the unit of the attribute (points for a percentage)."),
               ("b)", "Adjusted by Holm's method for the three attributes tested."),
               ("c)", "Interaction: whether the change with hold time differs between the two pH values."),
               ("d)", "Common to both pH values, in the unit of the attribute."),
               ("e)", "At the mean level of the attribute in the study."),
               ("f)", f"Lowest and highest single result at hold times up to {hold_nor[1]:g} min, the "
                      "upper end of the hold time NOR in force.")],
        notes_per_row=True, size="footnotesize", landscape=True,
        caption=f"Effect of the inactivation pH on the quality attributes over the low-pH hold "
                f"(study S-VI-OFAT).", label=label)


def _vi_cex_runs_table(runs_file, summary, load_note, caption, label) -> CTable:
    """Cation exchange runs on low-pH material, one row per run, and the decision on the clearance
    factor of aggregate and of fragments (S-CEX-VER, S-VI-WC)."""
    runs = _csv(runs_file)
    s = summary.set_index("cqa")
    body = []
    for r in runs.itertuples():
        body.append([str(int(r.run)), num(r.load_aggregate_pct, 2), num(r.aggregate_out_pct, 2),
                     num(r.aggregate_fold, 2), num(r.load_lmw_cesds_pct, 2), num(r.lmw_cesds_pct, 2),
                     num(r.fragment_fold, 2)])
    ag, fr = s.loc["aggregates_hmw"], s.loc["fragments_lmw"]
    for lab, a_, f_ in (("Geometric mean fold", num(ag["fold_gmean"], 2), num(fr["fold_gmean"], 2)),
                        ("Lower 95 % confidence\nbound^a)^", num(ag["fold_bound"], 2), num(fr["fold_bound"], 2)),
                        ("Fold the criteria\nrely on^b)^", num(ag["f_required"], 2), num(fr["f_required"], 2)),
                        ("Result", "Passed" if ag["passed"] else "Not passed",
                         "Passed" if fr["passed"] else "Not passed")):
        body.append([lab, "", "", a_, "", "", f_])
    return CTable(
        header=[[C("Run", rs=2), C("Aggregate, % HMW (SEC)", cs=3), C("Fragments, % LMW (nrCE-SDS)", cs=3)],
                ["Load", "Pool", "Fold", "Load", "Pool", "Fold"]],
        body=body, align=["P{3.4cm}"] + ["R{1.45cm}"] * 6,
        notes=[("", load_note + " Cation exchange at set-point. Fold: load divided by pool."),
               ("a)", "One-sided, of the mean log fold, with the run-to-run SD of the log fold from the "
                      "cation exchange data, as in the simulation that set the number of runs."),
               ("b)", "The clearance factor through cation exchange that the intermediate acceptance "
                      "criteria upstream of it assume (PCMP-001).")],
        notes_per_row=True, caption=caption, label=label)


def cex_verification_runs(label="tbl-cex-verification") -> CTable:
    """S-CEX-VER: each cation exchange run on the worst-case material of the re-centred step, and the
    decision on the clearance factor of each attribute."""
    import doe_report as D
    lf = _cfg().raw()["analytics"]["cex_verification"]["load_from"]
    note = (f"Load: material inactivated at pH {lf['ph']:.2f}, the re-centred set-point, for "
            f"{lf['hold_time']:g} min at {lf['temperature']:g} °C, the longest hold and the highest "
            "temperature of the NOR in force.")
    return _vi_cex_runs_table("cex_verification.csv", D.cex_verification_summary(), note,
                              "Cation exchange runs on material from the re-centred low-pH step "
                              "(study S-CEX-VER).", label)


def vi_worst_case_runs(label="tbl-vi-worst-case") -> CTable:
    """S-VI-WC (PD-006-03): each low-pH hold at the low end of the pH PAR with hold time and temperature at the
    upper ends of their NORs, followed by
    a cation exchange run, and the decision on the clearance factor of each attribute."""
    import doe_report as D
    from amab_process.analytics import _position
    w = _cfg().raw()["analytics"]["vi_worst_case"]
    lf = {k: _position(_cfg(), "viral_inactivation", k, pos) for k, pos in w["load_from"].items()}
    note = (f"Load: material held at pH {lf['ph']:.2f}, the lower end of the pH range studied and of "
            f"the pH PAR, for {lf['hold_time']:g} min at {lf['temperature']:g} °C, the upper ends of "
            "the hold-time and temperature NORs in force.")
    s, _ = D.vi_worst_case_summary()
    return _vi_cex_runs_table("vi_worst_case.csv", s, note,
                              "Low-pH holds at the low end of the pH PAR, with hold time and temperature at the upper ends of their NORs, each followed by "
                              "a cation exchange run (study S-VI-WC).", label)


def cex_verification_n(label="tbl-cex-verification-n") -> CTable:
    """S-CEX-VER: the simulation that set the number of runs."""
    import doe_report as D
    g = _csv("cex_verification_n.csv")
    s = D.cex_verification_summary().set_index("cqa")
    v = _cfg().raw()["analytics"]["cex_verification"]
    names = {"aggregates_hmw": "Aggregate", "fragments_lmw": "Fragments"}
    body = []
    for cqa, gg in g.groupby("cqa", sort=False):
        r = s.loc[cqa]
        for i, (_, x) in enumerate(gg.iterrows()):
            lead = ([C(names[cqa], rs=len(gg)), C(num(r["f_data"], 2), rs=len(gg)),
                     C(num(r["f_required"], 2), rs=len(gg)), C(f"{r['sigma_ln']:.3f}", rs=len(gg))]
                    if i == 0 else [])
            body.append(lead + [str(int(x["n"])), f"{x['p_pass_at_data']:.2f}", f"{x['p_pass_at_required']:.3f}"]
                        + ([C(str(int(r["n_required"])), rs=len(gg))] if i == 0 else []))
    return CTable(
        header=[[C("Attribute", rs=2), C("Fold in the\ncation exchange\ndata^a)^", rs=2),
                 C("Fold the\ncriteria\nrely on", rs=2), C("SD of the\nlog fold", rs=2), C("Runs", rs=2),
                 C("Probability of passing", cs=2), C("Runs\nneeded^b)^", rs=2)],
                ["Fold as in\nthe data", "Fold equal to\nthe required"]],
        body=body, align="lrrrrrrr",
        notes=[("", f"{int(v['reps']):,} simulated verifications per number of runs. A verification "
                    "passes when the one-sided 95 % lower confidence bound of the mean log fold is at "
                    "least the fold the criteria rely on."),
               ("a)", "At set-point, from the selected model of aggregate. Fragments, which have no "
                      "adequate model, from the centre points."),
               ("b)", f"The smallest number of runs, at most {int(v['n_max'])}, with a probability of "
                      f"passing of at least {float(v['power']):.2f} when cation exchange clears as its data show.")],
        notes_per_row=True, size="footnotesize",
        caption="Number of cation exchange verification runs, from a simulation of the verification.",
        label=label)
