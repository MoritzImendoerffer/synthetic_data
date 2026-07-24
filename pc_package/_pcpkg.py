"""Shared helpers for the A-Mab process-characterization document package.

Every document in ``pc_package/`` imports this module from its Quarto setup
chunk (``from _pcpkg import *``). It reuses the seeded model outputs in
``outputs/`` — the same single source of truth as the consolidated report — so
no number in any document is typed by hand. Path handling is anchored on this
file, so it works regardless of the Quarto working directory.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np  # noqa: F401  (re-exported for document chunks)
import pandas as pd

# Repo root = parent of pc_package/ (independent of the render CWD).
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from amab_process import load_config  # noqa: E402
from amab_process import studies as st  # noqa: E402  (re-exported)

CFG = load_config()
DATA = os.path.join(ROOT, "outputs", "data")
FIG = "../outputs/figures"  # markdown image paths are relative to a doc in pc_package/
V = json.load(open(os.path.join(ROOT, "outputs", "report_values.json")))

# Package-wide document metadata (keep in sync across the set).
EFFECTIVE_DATE = "2026-07-24"
VERSION = "1.0"
COMPANY = "Novacyte Biologics"          # fictional sponsor
SENDING_SITE = "Novacyte Biologics — Cambridge, MA (Development)"
RECEIVING_SITE = "Novacyte Biologics — Grafton, WI (Commercial DS)"
PRODUCT = "A-Mab"

# --------------------------------------------------------------------------- #
# Document registry — the whole set, so cross-references are consistent.       #
# --------------------------------------------------------------------------- #
UNIT_OP_TITLES = {
    "bioreactor": "Production Bioreactor",
    "harvest": "Harvest and Clarification",
    "protein_a": "Protein A Chromatography",
    "viral_inactivation": "Low-pH Viral Inactivation",
    "cex": "Cation Exchange Chromatography",
    "aex": "Anion Exchange Chromatography",
    "virus_filtration": "Small-Virus Retentive Filtration",
    "ufdf": "Ultrafiltration / Diafiltration",
}


def _uo_docs():
    """Per-unit-operation PCP/PCR IDs, numbered by process step (Steps 3-10)."""
    out = {}
    for key in CFG.train_order:
        uo = CFG.unit_op(key)
        step = uo.step
        name = UNIT_OP_TITLES.get(key, uo.name)
        out[f"PCP-{step:03d}"] = ("Process Characterization Plan", f"{name} (Step {step})", key)
        out[f"PCR-{step:03d}"] = ("Process Characterization Report", f"{name} (Step {step})", key)
    return out


DOC_REGISTRY = {
    "PTP-001": ("Process Transfer Plan", "A-Mab Drug Substance", None),
    "RA-001": ("Pre-Characterization Process Risk Assessment", "A-Mab Drug Substance", None),
    "PCMP-001": ("Process Characterization Master Plan", "A-Mab Drug Substance", None),
    "PCMR-001": ("Process Characterization Master Report", "A-Mab Drug Substance", None),
    **_uo_docs(),
}

# Placeholder controlled-document numbers referenced across the set. Prefixes
# SOP / AMV / PPQ are recognized by the nlp_reports DOCUMENT_ID matcher.
SOP_REFS = [
    ("SOP-1001", "Qualification of Scale-Down Models"),
    ("SOP-1002", "Design, Execution and Statistical Analysis of DoE Studies"),
    ("SOP-2003", "Operation of the Production Bioreactor (Fed-Batch)"),
    ("SOP-2004", "Cell-Culture Media and Feed Preparation"),
    ("SOP-3010", "Released N-Glycan Mapping by 2-AB HILIC-UPLC"),
    ("SOP-3011", "Size-Variant Analysis by SEC-HPLC"),
    ("SOP-3012", "Host-Cell-Protein Quantitation by ELISA"),
    ("SOP-3013", "Charge-Variant Analysis by icIEF"),
    ("SOP-3014", "Residual Host-Cell DNA by qPCR"),
    ("SOP-4001", "Process-Parameter Classification and Control-Strategy Definition"),
]
AMV_REFS = [
    ("AMV-3010", "N-Glycan Map (2-AB HILIC-UPLC)"),
    ("AMV-3011", "Size-Variants (SEC-HPLC)"),
    ("AMV-3012", "Host-Cell Protein ELISA"),
    ("AMV-3013", "Charge Variants (icIEF)"),
    ("AMV-3014", "Residual DNA (qPCR)"),
]


# --------------------------------------------------------------------------- #
# Data helpers (mirror the consolidated report's setup chunk).                 #
# --------------------------------------------------------------------------- #
def csv(name):
    """Read a CSV from outputs/data/ by file name."""
    return pd.read_csv(os.path.join(DATA, name))


def pct(x):
    return f"{100 * x:.1f}%"


def show(df, floatfmt=None):
    """Emit a DataFrame as a GitHub-markdown table (Quarto renders it to docx/pdf)."""
    print(df.to_markdown(index=False, floatfmt=floatfmt or ".3g"))


param_reg = csv("parameter_classification.csv")
cqa_reg = csv("cqa_register.csv")
cap = csv("capability.csv")


def _rng_str(lo, hi):
    return f"{lo:g}–{hi:g}"


def plan_params(key):
    """Parameters to be studied (no post-hoc classification) — for a Plan."""
    uo = CFG.unit_op(key)
    d = param_reg[param_reg.unit_operation == uo.name].copy()
    d["Range studied"] = d.apply(lambda r: _rng_str(r.par_low, r.par_high), axis=1)
    d["NOR"] = d.apply(lambda r: _rng_str(r.nor_low, r.nor_high), axis=1)
    d = d.rename(columns={"parameter": "Parameter", "unit": "Unit", "setpoint": "Set-point",
                          "study": "Study type"})
    return d[["Parameter", "Unit", "Set-point", "Range studied", "NOR", "Study type"]]


def report_params(key):
    """Parameters with final classification — for a Report."""
    uo = CFG.unit_op(key)
    d = param_reg[param_reg.unit_operation == uo.name].copy()
    d["NOR"] = d.apply(lambda r: _rng_str(r.nor_low, r.nor_high), axis=1)
    d["PAR"] = d.apply(lambda r: _rng_str(r.par_low, r.par_high), axis=1)
    d = d.rename(columns={"parameter": "Parameter", "unit": "Unit", "setpoint": "Set-point",
                          "classification": "Class", "study": "Study"})
    return d[["Parameter", "Unit", "Set-point", "NOR", "PAR", "Class", "Study"]]


def cqas_for(key):
    """CQAs primarily set/controlled by a unit operation, with acceptance criteria."""
    d = cqa_reg[cqa_reg.set_by == key].copy()
    d["Acceptance"] = d.apply(lambda r: f"{r.acc_low:g}–{r.acc_high:g} {r.unit}", axis=1)
    d = d.rename(columns={"cqa": "CQA", "category": "Category", "criticality": "Criticality",
                          "tool1_score": "Tool #1"})
    return d[["CQA", "Category", "Acceptance", "Criticality", "Tool #1"]]


def cap_for(keys):
    """Commercial-scale capability rows for the given CQA keys."""
    d = cap[cap.key.isin(keys)].copy()
    d["Acceptance"] = d.apply(lambda r: f"{r.acc_low:g}–{r.acc_high:g}", axis=1)
    d["Mean ± SD"] = d.apply(lambda r: f"{r['mean']:.3g} ± {r['sd']:.2g}", axis=1)
    d = d.rename(columns={"cqa": "CQA", "criticality": "Crit.", "spec_type": "Spec"})
    return d[["CQA", "Crit.", "Spec", "Acceptance", "Mean ± SD", "Cpk"]]


def top_effects(key, response, n=6):
    e = csv(f"effects_{key}.csv")
    e = e[e.response == response].copy().head(n)
    e["term"] = e["term"].str.replace(":", " × ", regex=False)
    e["signif."] = np.where(e.p_value < 0.05, "yes", "")
    return e[["term", "effect", "p_value", "signif."]].rename(
        columns={"term": "Term", "effect": "Effect", "p_value": "p-value"})


def doe_runs(key, kind):
    """Row count of a DoE design CSV (design structure only, no responses)."""
    return len(csv(f"doe_{key}_{kind}.csv"))


# --------------------------------------------------------------------------- #
# Front-matter blocks (returned as markdown strings; print under output: asis) #
# --------------------------------------------------------------------------- #
SYN_BANNER = (
    "> **SYNTHETIC DOCUMENT — NOT A REAL RECORD.** Illustrative content generated "
    "from a seeded model of the *A-Mab* case study (CMC Biotech Working Group, 2009). "
    f"{COMPANY} and all sites, SOP/AMV numbers and signatories are fictional. "
    "For NLP corpus development only; not for any regulated use.\n"
)


def title_block(doc_id, unit_op=None):
    """Render the controlled-document title block for a document."""
    cls, subject, _ = DOC_REGISTRY[doc_id]
    rows = [
        ("Document ID", doc_id),
        ("Document class", cls),
        ("Title", f"{cls} — {subject}" if unit_op is None else f"{cls}: {unit_op}"),
        ("Product", PRODUCT),
        ("Version", VERSION),
        ("Effective date", EFFECTIVE_DATE),
        ("Status", "Approved (synthetic)"),
        ("Document owner", "Manufacturing Science & Technology (MSAT)"),
        ("Sponsor / sites", f"{COMPANY}; {SENDING_SITE} → {RECEIVING_SITE}"),
    ]
    df = pd.DataFrame(rows, columns=["Field", "Value"])
    return df.to_markdown(index=False)


def related_docs_md(doc_id):
    """A cross-reference table to the sibling documents in the package."""
    step = None
    if doc_id[:4] in ("PCP-", "PCR-"):
        step = int(doc_id.split("-")[1])
    order = ["PTP-001", "RA-001", "PCMP-001"]
    if step is not None:
        sib = ("PCR-%03d" % step) if doc_id.startswith("PCP") else ("PCP-%03d" % step)
        order.append(sib)
    order.append("PCMR-001")
    rows = []
    for rid in order:
        if rid == doc_id:
            continue
        cls, subject, _ = DOC_REGISTRY[rid]
        rel = {"PTP-001": "Parent — transfer scope",
               "RA-001": "Parent — risk basis for study scope",
               "PCMP-001": "Parent — master plan",
               "PCMR-001": "Rolls up into",
               }.get(rid, "Sibling — paired document")
        rows.append([rid, f"{cls} ({subject})", rel])
    df = pd.DataFrame(rows, columns=["Document ID", "Title", "Relationship"])
    return df.to_markdown(index=False)


def sop_table(sops=None, amvs=None):
    rows = [[sid, title, "SOP"] for sid, title in (sops or SOP_REFS)]
    rows += [[aid, title, "Method validation"] for aid, title in (amvs or AMV_REFS)]
    df = pd.DataFrame(rows, columns=["Reference", "Title", "Type"])
    return df.to_markdown(index=False)
