#!/usr/bin/env python3
"""Build the graded question–answer set over the Version 2.0 corpus.

A test set for the owner's ``dw`` tool (doctool): a retrieval pipeline is scored on whether it
finds the right passage in the right document and gives the right answer, and a summarization run
on whether it covers the key points with correct citations. Spec:
``.claude/work/2026-10-08_01_rev2-campaign/spec-qa-set.md``; schema and scoring: ``qa/README.md``.

Most items are generated here from the annexes, the CSVs and the helpers; a small curated set
(``qa/curated.yaml``) covers the hard multi-document, summarization and unanswerable items. The
script checks both the same way.

Scope is ``build_ground_truth.REV2_READY``, read from the rendered ``.docx`` of each document. A
document that joins REV2_READY is picked up on the next run, with no change here.

Golden rules: no value is typed in this file. Generated answers come from the annexes (themselves
built from the CSVs), the CSVs and the table builders. Every evidence quote must be a verbatim
substring of the rendered document under ``check_grounding``'s own extraction and normalisation; a
generated item whose quote does not ground is dropped, a curated one is reported stale and left out.

Run:    python build_qa.py            (from pc_package/)
Writes: qa/qa_set.jsonl, qa/qa_set.md
Exit:   0, or 1 if a level falls below its minimum count.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import sys
from collections import defaultdict

import check_grounding as G

HERE = os.path.dirname(os.path.abspath(__file__))
GT = os.path.join(HERE, "ground_truth")
QA = os.path.join(HERE, "qa")
CURATED = os.path.join(QA, "curated.yaml")

LEVELS = ("L1", "L2", "L3", "L4", "SUM", "NONE")
#: The floor of each level. The targets of the spec are rough (L1 ~40, L2 ~40, L3 ~30, L4 ~25,
#: SUM ~8, NONE ~15); the floors leave room for stale curated items and for documents not yet
#: promoted to REV2_READY.
MIN_COUNTS = {"L1": 30, "L2": 25, "L3": 15, "L4": 15, "SUM": 6, "NONE": 12}

#: How many generated items of one level one document (L1, L2) or one group (L3, L4) may give.
#: Selection is stable: by a hash of the item key, round-robin over templates.
CAP_L1_PER_DOC = 3
CAP_L2_PER_DOC = 5
CAP_L3_PER_GROUP = 5
CAP_L4_TEMPLATE = 8

NOT_IN_DOCS = "not in the documents"


# --------------------------------------------------------------------------- #
# Scope and text                                                                #
# --------------------------------------------------------------------------- #
def rev2_ready() -> set:
    """REV2_READY as build_ground_truth defines it. Imported; parsed from the source if the module
    does not import (another agent may be editing a builder), so the QA build never depends on it."""
    try:
        import build_ground_truth as B
        return set(B.REV2_READY)
    except Exception:  # pragma: no cover - fallback path
        src = open(os.path.join(HERE, "build_ground_truth.py")).read()
        for node in ast.walk(ast.parse(src)):
            tgt = getattr(node, "target", None) or (node.targets[0] if isinstance(node, ast.Assign) else None)
            if isinstance(tgt, ast.Name) and tgt.id == "REV2_READY":
                return set(ast.literal_eval(node.value))
        raise SystemExit("REV2_READY not found in build_ground_truth.py")


class Corpus:
    """The Version 2.0 documents in scope: annex and rendered text of each."""

    def __init__(self):
        self.docs = sorted(rev2_ready())
        self.annex, self.text, self.file = {}, {}, {}
        for d in self.docs:
            a = json.load(open(os.path.join(GT, f"{d}.json")))
            fname = a["inventory"]["file_name"]
            path = os.path.join(HERE, fname)
            if not os.path.exists(path):
                raise FileNotFoundError(f"{d}: rendered document {fname} not found (render the corpus)")
            self.annex[d], self.file[d] = a, fname
            self.text[d] = G.docx_text(path)

    def grounds(self, doc, quote) -> bool:
        return doc in self.text and bool(quote) and G.normalize(quote) in self.text[doc]

    def entities(self, doc, kind):
        out = []
        for e in self.annex[doc].get("entities", []):
            out.extend(e.get(kind) or [])
        return out


# --------------------------------------------------------------------------- #
# Small helpers                                                                 #
# --------------------------------------------------------------------------- #
def slug(s) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")


def h(key) -> str:
    return hashlib.sha1(str(key).encode()).hexdigest()


def fmt(v) -> str:
    """A computed number as text, without spurious digits."""
    import tables as T
    return T.num(v)


def ev(doc, quote, header=None) -> dict:
    e = {"doc_id": doc, "quote": quote}
    if header:
        e["table_header"] = header
    return e


def ref_ev(doc, ref) -> dict:
    return ev(doc, ref["quote"], ref.get("table_header"))


def row_refs(refs):
    """Source references that are rendered rows (they name their record), rows first."""
    return sorted([r for r in refs or [] if r.get("quote")], key=lambda r: G.CELL_SEP not in r["quote"])


def step_of(label: str) -> str:
    """'Protein A Chromatography (Step 5)' -> 'Protein A Chromatography'."""
    return re.sub(r"\s*\(Step \d+\)\s*$", "", label or "").strip()


NUM = r"[-−]?\d[\d,]*(?:\.\d+)?"


def range_of(s):
    """(lo, hi) from '20–40 g/L resin' or 'pH 6.75–6.95'; None for a one-sided or other form."""
    m = re.search(rf"({NUM})\s*[–-]\s*({NUM})", s or "")
    if not m:
        return None
    f = lambda x: float(x.replace(",", "").replace("−", "-"))
    return f(m.group(1)), f(m.group(2))


def numbers_in(s):
    return re.findall(r"\d[\d,]*(?:\.\d+)?", s or "")


def doc_label(doc) -> str:
    import _pcpkg as P
    cls, subj, key = P.DOC_REGISTRY[doc]
    if doc.startswith("PCP-"):
        return f"the {P.UNIT_OP_TITLES[key]} characterization plan ({doc})"
    if doc.startswith("PCR-"):
        return f"the {P.UNIT_OP_TITLES[key]} characterization report ({doc})"
    return {"PCMP-001": "the process characterization master plan (PCMP-001)",
            "RA-001": "the pre-characterization risk assessment (RA-001)",
            "PTP-001": "the process transfer plan (PTP-001)",
            "PCMR-001": "the process characterization master report (PCMR-001)"}.get(
        doc, f"investigation {doc}")


def doc_step_key(doc):
    import _pcpkg as P
    return P.DOC_REGISTRY.get(doc, (None, None, None))[2]


def item(level, template, keys, question, answer, evidence, reasoning=None, value=None, unit=None):
    it = {"id": "-".join([level, template] + [slug(k) for k in keys]),
          "level": level, "template": template, "question": question, "answer": answer}
    if value is not None:
        it["answer_value"] = value
        it["unit"] = unit
    it["evidence"] = evidence
    it["docs"] = sorted({e["doc_id"] for e in evidence})
    if reasoning:
        it["reasoning"] = reasoning
    return it


def select(cands, cap, group_of=lambda it: it["docs"][0], per_template=None):
    """Stable selection: per group, round-robin over templates in hash order, at most ``cap``
    items, and at most ``per_template`` of one template."""
    groups = defaultdict(lambda: defaultdict(list))
    for it in cands:
        groups[group_of(it)][it["template"]].append(it)
    out = []
    for g in sorted(groups):
        by_t = {t: sorted(v, key=lambda it: h(it["id"]))[:per_template] for t, v in groups[g].items()}
        order = sorted(by_t, key=h)
        picked, i = [], 0
        while len(picked) < cap and any(by_t.values()):
            t = order[i % len(order)]
            if by_t[t]:
                picked.append(by_t[t].pop(0))
            i += 1
        out.extend(picked)
    return out


# --------------------------------------------------------------------------- #
# Shared lookups                                                                #
# --------------------------------------------------------------------------- #
def params_by_name(C, doc):
    return {p["parameter_name"]: p for p in C.entities(doc, "parameters")}


def param_csv_range(step_name, pname, which="nor"):
    import _pcpkg as P
    r = P.param_reg[(P.param_reg.unit_operation == step_name) & (P.param_reg.parameter == pname)]
    if r.empty:
        return None
    r = r.iloc[0]
    return float(r[f"{which}_low"]), float(r[f"{which}_high"])


def in_force(C, doc):
    return [c for c in C.annex[doc].get("acceptance_criteria", [])
            if c.get("status") == "in force" and c.get("source", {}).get("quote")]


def crit_text(c, spec=None):
    import tables as T
    lo, hi = c.get("low"), c.get("high")
    if lo is None:
        return T.crit(None, hi, "upper")
    if hi is None:
        return T.crit(lo, None, "lower")
    return T.crit(lo, hi, "two_sided")


def crit_value(c):
    lo, hi = c.get("low"), c.get("high")
    return [lo, hi]


def cqa_unit(cqa):
    """The unit of an attribute, from the CQA register."""
    import _pcpkg as P
    r = P.cqa_reg[P.cqa_reg.key == cqa]
    return None if r.empty else str(r.iloc[0]["unit"])


def attr_label(cqa):
    import tables as T
    return T.ATTR_NAME.get(cqa, cqa.replace("_", " "))


def attr_plain(cqa):
    """'Aggregates, HMW (%)' -> 'aggregates, HMW', for use in a sentence."""
    s = re.sub(r"\s*\([^)]*\)\s*$", "", attr_label(cqa))
    return s if s[:2].isupper() or s.startswith(("XMuLV", "MVM", "Leached Protein A")) else s[0].lower() + s[1:]


def step_plain(key):
    import tables as T
    return T.step_mid(key)


def first_label(quote):
    """The record a row quote names: its first cell that is not a step name."""
    import tables as T
    cells = [c.strip() for c in quote.split(G.CELL_SEP.strip())]
    steps = set(T.STEP_NAME.values())
    for c in cells:
        if c and c not in steps:
            return c
    return cells[0]


def g(v) -> str:
    """A parameter value as the configuration states it (3.5, 90, 0.75), without float noise."""
    return f"{round(float(v), 6):g}"


#: Annex values that disagree with the CSVs (a document rendered before the data changed). The
#: item is left out and the record listed in the build report.
INCONSISTENT: list = []


def nor_consistent(doc, step, pname, nor) -> bool:
    """The NOR a document states against parameter_classification.csv: the NOR in force, or the
    NOR the characterization studies used (a plan states the latter)."""
    import _pcpkg as P
    r = P.param_reg[(P.param_reg.unit_operation == step) & (P.param_reg.parameter == pname)]
    got = range_of(nor)
    if r.empty or not got:
        return True
    r = r.iloc[0]
    ok = any(abs(got[0] - float(r[a])) < 1e-9 and abs(got[1] - float(r[b])) < 1e-9
             for a, b in (("nor_low", "nor_high"), ("nor_char_low", "nor_char_high")))
    if not ok:
        INCONSISTENT.append(f"{doc}: NOR of {pname} ({step}) is {nor}; parameter_classification.csv gives "
                            f"{g(r['nor_low'])}–{g(r['nor_high'])}")
    return ok


def criterion_consistent(doc, c) -> bool:
    """An in-force criterion an annex records against iac.csv."""
    import _pcpkg as P
    import tables as T
    t = P.csv("iac.csv")
    r = t[(t.step_key == c["step"]) & (t.cqa == c["attribute"])]
    if r.empty:
        return True
    r = r.iloc[0]
    want = T.crit(r["iac_low"], r["iac_high"], r["spec_type"])
    ok = crit_text(c) == want
    if not ok:
        INCONSISTENT.append(f"{doc}: criterion for {c['attribute']} at {c['step']} is {crit_text(c)}; "
                            f"iac.csv gives {want}")
    return ok


def ra_rpn(p):
    m = re.search(r"initial RPN of (\d+) and priority (\w+)", p.get("rationale_for_criticality") or "")
    return (int(m.group(1)), m.group(2)) if m else None


# --------------------------------------------------------------------------- #
# L1: one fact, one document, one passage                                       #
# --------------------------------------------------------------------------- #
def gen_l1(C):
    import _pcpkg as P
    out = []
    chrono = P.csv("study_chronology.csv").set_index("id")
    for d in C.docs:
        # parameter NOR and class
        for p in C.entities(d, "parameters"):
            step = step_of(p.get("associated_step"))
            for r in row_refs(p.get("source_references")):
                nor = p.get("NOR") or ""
                if nor and all(n in r["quote"] for n in numbers_in(nor)) and p["parameter_name"] in r["quote"]:
                    if not nor_consistent(d, step, p["parameter_name"], nor):
                        break
                    rng = range_of(nor)
                    out.append(item("L1", "param-nor", [d, p["parameter_name"]],
                                    f"What is the normal operating range of {p['parameter_name']} at the {step} step in {doc_label(d)}?",
                                    nor, [ref_ev(d, r)], value=list(rng) if rng else None, unit=p.get("unit")))
                    break
            cls = p.get("parameter_type")
            if cls and cls != "unclassified":
                for r in row_refs(p.get("source_references")):
                    if re.search(rf"(^|\| ){re.escape(cls)}( |$)", r["quote"]) and p["parameter_name"] in r["quote"]:
                        out.append(item("L1", "param-class", [d, p["parameter_name"]],
                                        f"How is {p['parameter_name']} at the {step} step classified in {doc_label(d)}?",
                                        cls, [ref_ev(d, r)]))
                        break
        # PARs
        for par in C.annex[d].get("proven_acceptable_ranges", []):
            r = (row_refs(par.get("source_references")) or [None])[0]
            if r and r.get("table_header") and par.get("par_nor_propagated"):
                attr = re.sub(r"\s*\([^)]*\)\s*$", "", par["quality_attribute"])
                out.append(item("L1", "par", [d, par["parameter"], attr],
                                f"What is the NOR-propagated proven acceptable range of {par['parameter']} "
                                f"for {attr} in {doc_label(d)}?",
                                par["par_nor_propagated"], [ref_ev(d, r)],
                                value=list(range_of(par["par_nor_propagated"]) or []) or None,
                                unit=None))
        # intermediate acceptance criteria in force
        for c in in_force(C, d):
            ct = crit_text(c)
            q = c["source"]["quote"]
            if ct in G.normalize(q) and C.grounds(d, q) and criterion_consistent(d, c):
                out.append(item("L1", "criterion", [d, c["step"], c["attribute"]],
                                f"What acceptance criterion applies to {attr_plain(c['attribute'])} at the "
                                f"{step_plain(c['step'])} step output in {doc_label(d)}?",
                                f"{ct} ({c.get('basis')})", [ev(d, q, c["source"].get("table_header"))],
                                value=crit_value(c), unit=c.get("unit")))
        # study execution dates
        for s in C.annex[d].get("studies", []):
            sid = s["study_id"].split(":")[-1]
            if sid not in chrono.index:
                continue
            row = chrono.loc[sid]
            for r in row_refs(s.get("source_references")):
                if sid in r["quote"] and row["start"] in r["quote"] and row["end"] in r["quote"]:
                    out.append(item("L1", "study-dates", [d, sid],
                                    f"When was study {sid} carried out, according to {doc_label(d)}?",
                                    f"{row['start']} to {row['end']}", [ref_ev(d, r)],
                                    value=[row["start"], row["end"]], unit="date"))
                    break
        # analytical method references
        for m in C.entities(d, "analytical_methods"):
            for r in row_refs(m.get("source_references")):
                if m["method_id"] in r["quote"] and m["method_name"] in r["quote"]:
                    out.append(item("L1", "method", [d, m["method_id"]],
                                    f"Which analytical method validation covers the {m['method_name']} method "
                                    f"in {doc_label(d)}?", m["method_id"], [ref_ev(d, r)]))
                    break
        # study events
        for e in C.entities(d, "deviations"):
            for r in row_refs(e.get("source_references")):
                if e["deviation_id"] in r["quote"] and e.get("summary") and e["summary"] in r["quote"]:
                    out.append(item("L1", "event", [d, e["deviation_id"]],
                                    f"What happened in study event {e['deviation_id']}, and how was it handled?",
                                    f"{e['summary']}; {e.get('disposition')}", [ref_ev(d, r)]))
                    break
        # discrepancies from the plan
        for pd_ in P.PLAN_DISCREPANCIES.get(d, []):
            q = f"{pd_['id']} | {pd_['subject']}"
            if C.grounds(d, q):
                out.append(item("L1", "discrepancy", [d, pd_["id"]],
                                f"What is discrepancy {pd_['id']} from the plan about?",
                                pd_["subject"], [ev(d, q)]))
        # process capability
        for cp in C.entities(d, "capabilities"):
            r = (row_refs(cp.get("source_references")) or [None])[0]
            if (r and G.CELL_SEP in r["quote"] and not d.startswith("INV-") and cp.get("index_value") is not None
                    and f"{cp['index_value']:g}" in r["quote"]):
                lab = first_label(r["quote"])
                out.append(item("L1", "cpk", [d, cp["quality_attribute"]],
                                f"What Cpk does {doc_label(d)} give for {lab}?",
                                f"Cpk {cp['index_value']:g}", [ref_ev(d, r)],
                                value=cp["index_value"], unit=None))
        # transfer gaps
        for g in C.annex[d].get("transfer_gaps", []):
            r = (row_refs(g.get("source_references")) or [None])[0]
            if r and g["description"] in r["quote"]:
                out.append(item("L1", "transfer-gap", [d, g["gap_id"]],
                                f"What action does {doc_label(d)} set for the transfer gap \"{g['description']}\"?",
                                re.sub(r"\s*Owner:.*$", "", g["mitigation"]), [ref_ev(d, r)]))
        # initial risk priority
        if d == "RA-001":
            for p in C.entities(d, "parameters"):
                rp = ra_rpn(p)
                r = (row_refs(p.get("source_references")) or [None])[0]
                if rp and r and str(rp[0]) in r["quote"] and rp[1] in r["quote"]:
                    out.append(item("L1", "ra-priority", [d, step_of(p["associated_step"]), p["parameter_name"]],
                                    f"What initial risk priority and RPN does {doc_label(d)} give "
                                    f"{p['parameter_name']} at the {step_of(p['associated_step'])} step?",
                                    f"{rp[1]}, initial RPN {rp[0]}", [ref_ev(d, r)], value=rp[0], unit="RPN"))
    # dedupe on id (a parameter can appear under two section entities)
    uniq = {}
    for it in out:
        uniq.setdefault(it["id"], it)
    return select(list(uniq.values()), CAP_L1_PER_DOC)


# --------------------------------------------------------------------------- #
# L2: reasoning within one document                                             #
# --------------------------------------------------------------------------- #
def gen_l2(C):
    import _pcpkg as P
    import tables as T
    out = []
    alpha = T._alpha()
    for d in C.docs:
        pmap = params_by_name(C, d)
        # NOR inside the PAR, and by what margin
        for par in C.annex[d].get("proven_acceptable_ranges", []):
            p = pmap.get(par["parameter"])
            pr = range_of(par.get("par_nor_propagated"))
            if not p or not pr:
                continue
            step = step_of(p.get("associated_step"))
            nr = param_csv_range(step, p["parameter_name"]) or range_of(p.get("NOR"))
            pref = next((r for r in row_refs(p.get("source_references"))
                         if all(n in r["quote"] for n in numbers_in(p.get("NOR")))), None)
            parref = (row_refs(par.get("source_references")) or [None])[0]
            if not nr or not pref or not parref or not parref.get("table_header"):
                continue
            below, above = nr[0] - pr[0], pr[1] - nr[1]
            inside = below >= 0 and above >= 0
            attr = re.sub(r"\s*\([^)]*\)\s*$", "", par["quality_attribute"])
            unit = p.get("unit") or ""
            ans = (f"{'Yes' if inside else 'No'}: NOR {g(nr[0])}–{g(nr[1])} {unit}, PAR {par['par_nor_propagated']}; "
                   f"margin {g(below)} below and {g(above)} above").strip()
            out.append(item("L2", "nor-in-par", [d, p["parameter_name"], attr],
                            f"In {doc_label(d)}, does the NOR of {p['parameter_name']} lie inside its "
                            f"NOR-propagated proven acceptable range for {attr}, and by what margin at each end?",
                            ans, [ref_ev(d, pref), ref_ev(d, parref)],
                            reasoning=[f"NOR of {p['parameter_name']}: {p['NOR']} (parameter table).",
                                       f"NOR-propagated PAR for {attr}: {par['par_nor_propagated']} (PAR table).",
                                       "Margin = NOR low − PAR low, and PAR high − NOR high."],
                            value=[round(below, 6), round(above, 6)], unit=unit or None))
        # criterion met across the NOR, and by how much (reports with a response-surface design)
        key = doc_step_key(d)
        if d.startswith("PCR-") and key:
            out.extend(_l2_criteria(C, d, key))
        # model adequacy: lack of fit and the R² gap
        for mf in C.entities(d, "model_fits"):
            if mf.get("lack_of_fit_p") is None or mf.get("r_squared") is None or mf.get("predicted_r_squared") is None:
                continue
            if d == "INV-002" and not str(mf.get("model_form", "")).startswith("full quadratic"):
                continue
            r = (row_refs(mf.get("source_references")) or [None])[0]
            if not r:
                continue
            lab = first_label(r["quote"])
            gap = mf["r_squared"] - mf["predicted_r_squared"]
            lof = mf["lack_of_fit_p"]
            which = ("the full quadratic model fitted in Version 1.0" if d == "INV-002"
                     else "the selected response-surface model")
            step = mf.get("unit_operation", "")
            out.append(item("L2", "model-fit", [d, step, mf["response"]],
                            f"For {lab} at the {step} step, does {which} show significant lack of fit at "
                            f"α = {fmt(alpha)}, and how far apart are R² and predicted R²? Answer from {doc_label(d)}.",
                            f"{'Significant' if lof < alpha else 'No significant'} lack of fit (p = {fmt(lof)}); "
                            f"R² {fmt(mf['r_squared'])} − predicted R² {fmt(mf['predicted_r_squared'])} = {fmt(gap)}",
                            [ref_ev(d, r)],
                            reasoning=[f"Lack-of-fit p = {fmt(lof)}, compared with α = {fmt(alpha)}.",
                                       "Gap = R² − predicted R²."],
                            value=round(gap, 4), unit=None))
        # lowest capability
        caps = [(cp, (row_refs(cp.get("source_references")) or [None])[0]) for cp in C.entities(d, "capabilities")]
        caps = [(cp, r) for cp, r in caps if r and G.CELL_SEP in r["quote"] and cp.get("index_value") is not None]
        if len(caps) >= 2 and d.startswith("PCR-"):
            low = min(caps, key=lambda x: x[0]["index_value"])
            lab = first_label(low[1]["quote"])
            out.append(item("L2", "lowest-cpk", [d],
                            f"Which drug substance attribute has the lowest process capability in {doc_label(d)}, "
                            f"and what is its Cpk?",
                            f"{lab}, Cpk {low[0]['index_value']:g}", [ref_ev(d, r) for _, r in caps],
                            reasoning=[f"Read the Cpk of each of the {len(caps)} attributes.",
                                       f"The smallest is {lab}."],
                            value=low[0]["index_value"], unit=None))
        # number of discrepancies a report records
        pds = P.PLAN_DISCREPANCIES.get(d, [])
        quotes = [f"{x['id']} | {x['subject']}" for x in pds]
        if pds and all(C.grounds(d, q) for q in quotes):
            out.append(item("L2", "discrepancy-count", [d],
                            f"How many discrepancies from its plan does {doc_label(d)} record?",
                            f"{len(pds)} ({pds[0]['id']} to {pds[-1]['id']})", [ev(d, q) for q in quotes],
                            reasoning=["Count the entries of the discrepancy register."],
                            value=len(pds), unit="discrepancies"))
        # RA-001: the highest initial RPN of a step
        if d == "RA-001":
            by_step = defaultdict(list)
            for p in C.entities(d, "parameters"):
                rp, r = ra_rpn(p), (row_refs(p.get("source_references")) or [None])[0]
                if rp and r:
                    by_step[step_of(p["associated_step"])].append((p, rp, r))
            for step, ps in by_step.items():
                if len(ps) < 2:
                    continue
                top = max(x[1][0] for x in ps)
                names = [x[0]["parameter_name"] for x in ps if x[1][0] == top]
                out.append(item("L2", "ra-top-rpn", [d, step],
                                f"Which parameter of the {step} step carries the highest initial RPN in {doc_label(d)}?",
                                f"{', '.join(names)} (initial RPN {top})", [ref_ev(d, x[2]) for x in ps],
                                reasoning=[f"Read the initial RPN of the {len(ps)} parameters of the step.",
                                           "Take the largest."],
                                value=top, unit="RPN"))
        # PCMP-001 / PTP-001: the critical parameters of a step
        if d in ("PCMP-001", "PTP-001"):
            by_step = defaultdict(list)
            for p in C.entities(d, "parameters"):
                r = (row_refs(p.get("source_references")) or [None])[0]
                if r and p.get("parameter_type") not in (None, "unclassified"):
                    by_step[step_of(p["associated_step"])].append((p, r))
            for step, ps in by_step.items():
                crit = [x[0]["parameter_name"] for x in ps if x[0]["parameter_type"] in ("CPP", "WC-CPP")]
                if len(ps) < 2:
                    continue
                out.append(item("L2", "critical-count", [d, step],
                                f"How many of the parameters {doc_label(d)} lists for the {step} step are critical "
                                f"(CPP or WC-CPP), and which?",
                                f"{len(crit)} of {len(ps)}" + (f": {', '.join(crit)}" if crit else ""),
                                [ref_ev(d, r) for _, r in ps],
                                reasoning=[f"Read the class of each of the {len(ps)} parameters of the step.",
                                           "Count those classed CPP or WC-CPP."],
                                value=len(crit), unit="parameters"))
    uniq = {}
    for it in out:
        uniq.setdefault(it["id"], it)
    return select(list(uniq.values()), CAP_L2_PER_DOC, per_template=3)


def _criteria_rows(C, d, key):
    """{cqa -> rendered row of the report's criteria table} for the rows that ground."""
    import tables as T
    try:
        rows = T.criteria_results(key).rows()
    except Exception:
        return {}
    out = {}
    for cqa, name in T.ATTR_NAME.items():
        for r in rows:
            if r.startswith(name + " |") and C.grounds(d, r):
                out[cqa] = r
    return out


def _l2_criteria(C, d, key):
    import _pcpkg as P
    import doe_report as D
    import tables as T
    out = []
    rows = _criteria_rows(C, d, key)
    if not rows:
        return out
    header = " | ".join(T.criteria_results(key).header_rows())
    iac = P.csv("iac.csv")
    for _, r in iac[iac.step_key == key].iterrows():
        cqa, resp = r["cqa"], r["response"]
        if cqa not in rows:
            continue
        try:
            if D.fit(key, "rsm", resp)["status"] == "none" or D.decision_statistic(resp) != "batch":
                continue
            lo, hi = D.nor_prediction_limit(key, resp, "lower"), D.nor_prediction_limit(key, resp, "upper")
            ok = bool(D.nor_met(key, resp))
        except Exception:
            continue
        margins, steps = [], []
        if r["spec_type"] in ("upper", "two_sided"):
            margins.append(r["iac_high"] - hi)
            steps.append(f"Upper limit {fmt(hi)} against the upper end {fmt(r['iac_high'])}: margin {fmt(r['iac_high'] - hi)}.")
        if r["spec_type"] in ("lower", "two_sided"):
            margins.append(lo - r["iac_low"])
            steps.append(f"Lower limit {fmt(lo)} against the lower end {fmt(r['iac_low'])}: margin {fmt(lo - r['iac_low'])}.")
        m = min(margins)
        crit = T.crit(r["iac_low"], r["iac_high"], r["spec_type"])
        a = attr_plain(cqa)
        out.append(item("L2", "criterion-margin", [d, cqa],
                        f"In {doc_label(d)}, is the {a} criterion of the {step_plain(key)} output met across the "
                        f"NOR, judged on the 95 % limits of a single run, and by what margin?",
                        f"{'Yes' if ok else 'No'}: criterion {crit}, single-run limits {fmt(lo)} to {fmt(hi)} "
                        f"over the NOR; smallest margin {fmt(m)}" + ("" if ok else " (outside the criterion)"),
                        [ev(d, rows[cqa], header if C.grounds(d, header) else None)],
                        reasoning=[f"Criterion: {crit}."] + steps + ["A negative margin means the criterion is not met."],
                        value=round(float(m), 4), unit=cqa_unit(cqa)))
    return out


# --------------------------------------------------------------------------- #
# L3: the same fact in two documents                                            #
# --------------------------------------------------------------------------- #
def _pair_param(C, a, b, template, field, qtext, docs_needed=True):
    out = []
    pa, pb = params_by_name(C, a), params_by_name(C, b)
    for name in sorted(set(pa) & set(pb)):
        x, y = pa[name], pb[name]
        if step_of(x.get("associated_step")) != step_of(y.get("associated_step")):
            continue
        vx, vy = x.get(field), y.get(field)
        if not vx or not vy or "unclassified" in (vx, vy):
            continue
        def ref(p, v):
            return next((r for r in row_refs(p.get("source_references")) if name in r["quote"]
                         and (all(n in r["quote"] for n in numbers_in(v)) if field == "NOR" else v in r["quote"])), None)
        rx, ry = ref(x, vx), ref(y, vy)
        if not rx or not ry:
            continue
        same = (range_of(vx) == range_of(vy)) if field == "NOR" else vx == vy
        step = step_of(x.get("associated_step"))
        out.append(item("L3", template, [a, b, step, name],
                        qtext.format(p=name, s=step, a=doc_label(a), b=doc_label(b)),
                        (f"Yes, {vx} in both" if same else f"No: {vx} in {a}, {vy} in {b}"),
                        [ref_ev(a, rx), ref_ev(b, ry)],
                        reasoning=[f"{a}: {vx}.", f"{b}: {vy}.", "Compare."]))
    return out


def gen_l3(C):
    import _pcpkg as P
    out = []
    docs = set(C.docs)
    chrono = P.csv("study_chronology.csv").set_index("id")
    for d in C.docs:
        if not d.startswith("PCR-"):
            continue
        plan = "PCP-" + d[4:]
        if plan in docs:
            out += _pair_param(C, plan, d, "nor-plan-report", "NOR",
                               "Is the NOR of {p} at the {s} step the same in {a} and in {b}?")
            # a study planned in the plan and executed in the report
            sp = {s["study_id"]: s for s in C.annex[plan].get("studies", [])}
            for s in C.annex[d].get("studies", []):
                sid = s["study_id"].split(":")[-1]
                if s["study_id"] not in sp or sid not in chrono.index:
                    continue
                row = chrono.loc[sid]
                rp = next((r for r in row_refs(sp[s["study_id"]].get("source_references")) if sid in r["quote"]), None)
                rr = next((r for r in row_refs(s.get("source_references"))
                           if sid in r["quote"] and row["start"] in r["quote"]), None)
                if rp and rr:
                    out.append(item("L3", "study-plan-report", [plan, d, sid],
                                    f"Study {sid} is planned in {doc_label(plan)}. When was it carried out, "
                                    f"according to {doc_label(d)}?",
                                    f"{row['start']} to {row['end']}", [ref_ev(plan, rp), ref_ev(d, rr)],
                                    reasoning=[f"{plan} plans {sid}.", f"{d} gives its execution window."],
                                    value=[row["start"], row["end"]], unit="date"))
        for other in ("PCMP-001", "PTP-001"):
            if other in docs:
                out += _pair_param(C, d, other, "class-report-" + other.lower(), "parameter_type",
                                   "Does {b} carry the same class for {p} at the {s} step as {a} assigns?")
        if "RA-001" in docs:
            ra, rep = params_by_name(C, "RA-001"), params_by_name(C, d)
            for name in sorted(set(ra) & set(rep)):
                x, y = ra[name], rep[name]
                rp = ra_rpn(x)
                cls = y.get("parameter_type")
                if not rp or not cls or cls == "unclassified" or step_of(x["associated_step"]) != step_of(y["associated_step"]):
                    continue
                rx = (row_refs(x.get("source_references")) or [None])[0]
                ry = next((r for r in row_refs(y.get("source_references")) if name in r["quote"] and cls in r["quote"]), None)
                if not rx or not ry:
                    continue
                step = step_of(x["associated_step"])
                out.append(item("L3", "ra-priority-class", ["RA-001", d, step, name],
                                f"What initial priority did {doc_label('RA-001')} give {name} at the {step} step, "
                                f"and how does {doc_label(d)} classify it after characterization?",
                                f"{rp[1]} priority (initial RPN {rp[0]}); classified {cls}",
                                [ref_ev("RA-001", rx), ref_ev(d, ry)],
                                reasoning=[f"RA-001: priority {rp[1]}, initial RPN {rp[0]}.",
                                           f"{d}: class {cls}."]))
        if "PCMP-001" in docs:
            pc = {(c["step"], c["attribute"]): c for c in in_force(C, "PCMP-001")}
            for c in in_force(C, d):
                k = (c["step"], c["attribute"])
                if k not in pc:
                    continue
                x = pc[k]
                same = (x.get("low"), x.get("high")) == (c.get("low"), c.get("high"))
                ca, cb = crit_text(x), crit_text(c)
                if ca not in G.normalize(x["source"]["quote"]) or cb not in G.normalize(c["source"]["quote"]):
                    continue
                if not (criterion_consistent("PCMP-001", x) and criterion_consistent(d, c)):
                    continue
                out.append(item("L3", "criterion-pcmp-report", ["PCMP-001", d, c["attribute"]],
                                f"Is the {attr_plain(c['attribute'])} criterion of the {step_plain(c['step'])} output "
                                f"set in {doc_label('PCMP-001')} the one that {doc_label(d)} applies?",
                                f"Yes, {cb} in both" if same else f"No: {ca} in PCMP-001, {cb} in {d}",
                                [ev("PCMP-001", x["source"]["quote"], x["source"].get("table_header")),
                                 ev(d, c["source"]["quote"], c["source"].get("table_header"))],
                                reasoning=[f"PCMP-001: {ca}.", f"{d}: {cb}.", "Compare."],
                                value=crit_value(c), unit=c.get("unit")))
    uniq = {}
    for it in out:
        uniq.setdefault(it["id"], it)
    # one group per unit operation: the report (or plan) the comparison is about
    return select(list(uniq.values()), CAP_L3_PER_GROUP,
                  group_of=lambda it: next((d for d in it["docs"] if d.startswith("PCR-")), it["docs"][0]))


# --------------------------------------------------------------------------- #
# L4: reasoning across several documents (generated chains)                     #
# --------------------------------------------------------------------------- #
def gen_l4(C):
    out = _l4_criterion_chain(C) + _l4_parameter_trace(C)
    by_t = defaultdict(list)
    for it in out:
        by_t[it["template"]].append(it)
    return [it for t in sorted(by_t) for it in sorted(by_t[t], key=lambda it: h(it["id"]))[:CAP_L4_TEMPLATE]]


def _verification_rows():
    """[(step_key, cqa, csv row, rendered row)] in the order worst_case_verification renders them."""
    import _pcpkg as P
    import tables as T
    v = P.csv("iac_verification.csv")
    recs = [(sk, r) for sk, g in v.groupby("step_key", sort=False) for _, r in g.iterrows()]
    rows = T.worst_case_verification().rows()
    if len(rows) != len(recs):
        return []
    return [(sk, r["cqa"], r, row) for (sk, r), row in zip(recs, rows)]


def _l4_criterion_chain(C):
    """How a tightened or widened criterion is derived: the drug substance criterion and the
    downstream worst case (PCMP-001), the verification that changed it (INV-001), and whether the
    step meets it (the step report, when it is in scope)."""
    import _pcpkg as P
    import tables as T
    out = []
    if "PCMP-001" not in C.text:
        return out
    iac = P.csv("iac.csv")
    der = T.iac_derivation()
    der_rows = der.rows()
    der_hdr = " | ".join(der.header_rows())
    ver = _verification_rows()
    ver_doc = next((d for d in ("INV-001", "PCMP-001") if d in C.text and ver and C.grounds(d, ver[0][3])), None)
    order = list(P.CFG.train_order)
    for _, r in iac.iterrows():
        if not (bool(r["tightened"]) or bool(r["widened"])):
            continue
        key, cqa = r["step_key"], r["cqa"]
        crit = T.crit(r["iac_low"], r["iac_high"], r["spec_type"])
        dstr = f"{T.STEP_NAME[key]} | {T.num(r['downstream_fold'])} | {T.num(r['downstream_added'])} | {crit}"
        drow = next((x for x in der_rows if dstr in x and C.grounds("PCMP-001", x)), None)
        if not drow:
            continue
        ds = T.crit(r["ds_low"], r["ds_high"], r["spec_type"])
        evid = [ev("PCMP-001", drow, der_hdr if C.grounds("PCMP-001", der_hdr) else None)]
        steps = [f"PCMP-001: drug substance criterion {ds}; downstream clearance factor {T.num(r['downstream_fold'])} "
                 f"and increase {T.num(r['downstream_added'])}; criterion {crit} at the {step_plain(key)} output."]
        changes = []
        if ver_doc:
            for sk, vc, vr, vrow in ver:
                if vc != cqa or sk not in order or order.index(sk) <= order.index(key) or not C.grounds(ver_doc, vrow):
                    continue
                if pd_isna(vr["met"]):
                    continue
                if not bool(vr["met"]):
                    what = "tightened"
                elif bool(vr.get("widening_supported")):
                    what = "widened"
                else:
                    continue
                kind = "clearance factor" if vr["assumption"] == "fold_min" else "increase"
                changes.append(f"{step_plain(sk)} {kind}: platform {T.num(vr['assumed'])}, single-batch bound "
                               f"{T.num(vr['predicted_nor_bound95'])} ({what})")
                evid.append(ev(ver_doc, vrow))
                steps.append(f"{ver_doc}: at {step_plain(sk)} the platform {kind} {T.num(vr['assumed'])} is replaced "
                             f"by the single-batch bound {T.num(vr['predicted_nor_bound95'])}, so the criterion is {what}.")
        if not changes:
            continue
        rep = f"PCR-{P.CFG.unit_op(key).step:03d}"
        met = ""
        if rep in C.text:
            row = _criteria_rows(C, rep, key).get(cqa)
            if row:
                ok = row.rstrip().endswith("Yes")
                evid.append(ev(rep, row))
                met = f"; {rep} finds it {'met' if ok else 'not met'} across the NOR"
                steps.append(f"{rep}: the criterion is {'met' if ok else 'not met'} across the NOR.")
        out.append(item("L4", "criterion-chain", [key, cqa],
                        f"How is the {attr_plain(cqa)} criterion at the {step_plain(key)} output derived from the "
                        f"drug substance criterion, and which downstream verification changed it"
                        + (f"? Is it met in {doc_label(rep)}?" if met else "?"),
                        f"{ds} at drug substance, carried back to {crit}; changed by: " + "; ".join(changes) + met,
                        evid, reasoning=steps, value=crit_value({"low": None if r["spec_type"] == "upper" else r["iac_low"],
                                                                 "high": r["iac_high"]}),
                        unit=cqa_unit(cqa)))
    return out


def pd_isna(v):
    try:
        import pandas as pd
        return pd.isna(v)
    except Exception:
        return v is None


def _l4_parameter_trace(C):
    """One parameter from the initial risk assessment to the transfer plan: priority (RA-001), range
    studied (the plan), class (the report) and the class carried into transfer (PTP-001)."""
    out = []
    need = {"RA-001", "PTP-001"}
    if not need <= set(C.docs):
        return out
    ra, ptp = params_by_name(C, "RA-001"), params_by_name(C, "PTP-001")
    for d in C.docs:
        plan = "PCP-" + d[4:]
        if not d.startswith("PCR-") or plan not in C.text:
            continue
        rep, pl = params_by_name(C, d), params_by_name(C, plan)
        for name in sorted(set(rep) & set(pl) & set(ra) & set(ptp)):
            x, p, y, t = ra[name], pl[name], rep[name], ptp[name]
            if len({step_of(z["associated_step"]) for z in (x, p, y, t)}) != 1:
                continue
            rp, cls, tcls = ra_rpn(x), y.get("parameter_type"), t.get("parameter_type")
            studied = p.get("PAR")
            if not rp or not studied or cls in (None, "unclassified") or tcls in (None, "unclassified"):
                continue
            rx = (row_refs(x.get("source_references")) or [None])[0]
            rpl = next((r for r in row_refs(p.get("source_references")) if name in r["quote"]
                        and all(n in r["quote"] for n in numbers_in(studied))), None)
            ry = next((r for r in row_refs(y.get("source_references")) if name in r["quote"] and cls in r["quote"]), None)
            rt = next((r for r in row_refs(t.get("source_references")) if name in r["quote"] and tcls in r["quote"]), None)
            if not all((rx, rpl, ry, rt)):
                continue
            step = step_of(x["associated_step"])
            out.append(item("L4", "parameter-trace", [d, name],
                            f"Trace {name} at the {step} step from the initial risk assessment to the transfer plan: "
                            f"its initial priority, the range the plan studies, the class the report assigns, and "
                            f"whether the transfer plan carries that class.",
                            f"{rp[1]} priority (initial RPN {rp[0]}); range studied {studied}; classified {cls} in {d}; "
                            f"{'carried unchanged' if tcls == cls else f'carried as {tcls}'} in PTP-001",
                            [ref_ev("RA-001", rx), ref_ev(plan, rpl), ref_ev(d, ry), ref_ev("PTP-001", rt)],
                            reasoning=[f"RA-001: priority {rp[1]}, initial RPN {rp[0]}.",
                                       f"{plan}: range studied {studied}.", f"{d}: class {cls}.",
                                       f"PTP-001: class {tcls}."]))
    return out


# --------------------------------------------------------------------------- #
# Curated items                                                                 #
# --------------------------------------------------------------------------- #
def load_curated():
    import yaml
    if not os.path.exists(CURATED):
        return []
    return yaml.safe_load(open(CURATED)) or []


def check_curated(C, raw):
    """(kept, stale): a curated item is stale when a quote does not ground, an evidence document is
    out of scope, or an absent term turns up in a Version 2.0 document."""
    kept, stale = [], []
    corpus_lower = {d: t.lower() for d, t in C.text.items()}
    for it in raw:
        it = dict(it)
        it.setdefault("template", "curated")
        why = []
        evs = list(it.get("evidence") or [])
        for kp in it.get("key_points") or []:
            evs += kp.get("evidence") or []
        for e in evs:
            if e["doc_id"] not in C.text:
                why.append(f"{e['doc_id']} not in REV2_READY")
            elif not C.grounds(e["doc_id"], e["quote"]):
                why.append(f"quote not in {e['doc_id']}: {e['quote'][:60]!r}")
        if it["level"] == "NONE":
            it["expected"] = NOT_IN_DOCS
            for term in it.get("absent_terms") or []:
                # a whole-word match, so that "Tween" does not hit "between"
                pat = re.compile(r"(?<![\w])" + re.escape(G.normalize(term).lower()) + r"(?![\w])")
                hit = [d for d, t in corpus_lower.items() if pat.search(t)]
                if hit:
                    why.append(f"absent term {term!r} found in {', '.join(hit)}")
            if not it.get("absent_terms"):
                why.append("no absent_terms")
            it.setdefault("answer", NOT_IN_DOCS)
            it.setdefault("evidence", [])
        if it["level"] == "SUM":
            n = len(it.get("key_points") or [])
            if not 5 <= n <= 12:
                why.append(f"{n} key points (5-12 required)")
        it["docs"] = sorted({e["doc_id"] for e in evs})
        (stale if why else kept).append((it, why) if why else it)
    return kept, stale


# --------------------------------------------------------------------------- #
# Assembly                                                                      #
# --------------------------------------------------------------------------- #
FIELD_ORDER = ["id", "level", "template", "question", "answer", "answer_value", "unit", "evidence", "docs",
               "reasoning", "key_points", "expected", "absent_terms"]


def build(C=None):
    """Return (items, report). ``report`` counts generated, dropped, curated and stale items."""
    C = C or Corpus()
    INCONSISTENT.clear()
    gen = gen_l1(C) + gen_l2(C) + gen_l3(C) + gen_l4(C)
    kept_gen, dropped = [], []
    for it in gen:
        bad = [e for e in it["evidence"] if not C.grounds(e["doc_id"], e["quote"])
               or (e.get("table_header") and not C.grounds(e["doc_id"], e["table_header"]))]
        (dropped if bad else kept_gen).append(it)
    cur, stale = check_curated(C, load_curated())
    items = kept_gen + cur
    ids = [it["id"] for it in items]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        raise SystemExit(f"duplicate item ids: {dup}")
    items = [{k: it[k] for k in FIELD_ORDER if k in it} for it in items]
    items.sort(key=lambda it: (LEVELS.index(it["level"]), it["template"], it["id"]))
    report = {
        "docs": C.docs,
        "generated": {lv: sum(1 for it in kept_gen if it["level"] == lv) for lv in LEVELS},
        "curated": {lv: sum(1 for it in cur if it["level"] == lv) for lv in LEVELS},
        "total": {lv: sum(1 for it in items if it["level"] == lv) for lv in LEVELS},
        "dropped": [it["id"] for it in dropped],
        "stale": [(it.get("id"), why) for it, why in stale],
        "inconsistent": sorted(set(INCONSISTENT)),
    }
    return items, report


def write_md(items, report, path):
    names = {"L1": "L1: one fact, one document", "L2": "L2: reasoning within one document",
             "L3": "L3: the same fact in two documents", "L4": "L4: reasoning across several documents",
             "SUM": "SUM: summarization tasks", "NONE": "NONE: not answerable from the documents"}
    L = ["# Question–answer set (generated)", "",
         "Generated by `build_qa.py`; do not edit. Schema and scoring: `README.md`.", "",
         f"Documents in scope ({len(report['docs'])}): {', '.join(report['docs'])}.", "",
         "| Level | Generated | Curated | Total |", "|---|---|---|---|"]
    for lv in LEVELS:
        L.append(f"| {lv} | {report['generated'][lv]} | {report['curated'][lv]} | {report['total'][lv]} |")
    if report["stale"]:
        L += ["", "Stale curated items (left out):", ""] + [f"- `{i}`: {'; '.join(w)}" for i, w in report["stale"]]
    for lv in LEVELS:
        L += ["", f"## {names[lv]}", ""]
        for it in (x for x in items if x["level"] == lv):
            L += [f"### `{it['id']}`", "", f"**Q.** {it['question']}", "", f"**A.** {it['answer']}", ""]
            for st in it.get("reasoning") or []:
                L.append(f"- {st}")
            for kp in it.get("key_points") or []:
                L.append(f"- {kp['point']} ({', '.join(e['doc_id'] for e in kp['evidence'])})")
            if it.get("absent_terms"):
                L.append(f"- Absent terms checked: {', '.join(it['absent_terms'])}")
            for e in it.get("evidence") or []:
                L.append(f"> {e['doc_id']}: \"{e['quote']}\"")
            L.append("")
    open(path, "w").write("\n".join(L) + "\n")


def main(argv=None) -> int:
    items, report = build()
    os.makedirs(QA, exist_ok=True)
    with open(os.path.join(QA, "qa_set.jsonl"), "w") as fh:
        for it in items:
            fh.write(json.dumps(it, ensure_ascii=False) + "\n")
    write_md(items, report, os.path.join(QA, "qa_set.md"))
    print(f"documents in scope: {len(report['docs'])}")
    print(f"{'level':6} {'gen':>5} {'cur':>5} {'total':>6} {'min':>5}")
    low = []
    for lv in LEVELS:
        t = report["total"][lv]
        print(f"{lv:6} {report['generated'][lv]:5} {report['curated'][lv]:5} {t:6} {MIN_COUNTS[lv]:5}")
        if t < MIN_COUNTS[lv]:
            low.append(lv)
    if report["dropped"]:
        print(f"{len(report['dropped'])} generated item(s) dropped (a quote did not ground)")
    for i, why in report["stale"]:
        print(f"STALE {i}: {'; '.join(why)}")
    for x in report["inconsistent"]:
        print(f"NOTE  annex disagrees with the data, item left out: {x}")
    print(f"wrote qa/qa_set.jsonl ({len(items)} items) and qa/qa_set.md")
    if low:
        print(f"FAIL  below the minimum count: {', '.join(low)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
