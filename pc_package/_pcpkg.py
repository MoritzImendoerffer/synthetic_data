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

# Harvest / clarification (Step 4) controlled-document subsets. Placeholders,
# defined here so the harvest documents pull their references from the shared
# registry rather than hard-coding numbers in the .qmd. Reuses the corpus-wide
# SOP/AMV numbers where they apply and adds the two clarification-specific SOPs.
HARVEST_SOP_REFS = [
    ("SOP-1001", "Qualification of Scale-Down Models"),
    ("SOP-2005", "Harvest by Continuous Disk-Stack Centrifugation"),
    ("SOP-2006", "Clarification by Depth and Sterile Filtration"),
    ("SOP-4001", "Process-Parameter Classification and Control-Strategy Definition"),
]
HARVEST_AMV_REFS = [
    ("AMV-3015", "Turbidity by Nephelometry (NTU)"),
    ("AMV-3012", "Host-Cell Protein ELISA"),
    ("AMV-3014", "Residual DNA (qPCR)"),
    ("AMV-3011", "Size-Variants (SEC-HPLC)"),
]

# Protein A capture (Step 5) controlled-document subsets. Placeholders defined
# here so the Protein A documents pull references from the shared registry rather
# than hard-coding numbers. Reuses the corpus-wide HCP/DNA/SEC methods and adds
# the capture-specific SOP and the leached-Protein-A assay (AMV-3016).
PROTEIN_A_SOP_REFS = [
    ("SOP-1001", "Qualification of Scale-Down Models"),
    ("SOP-1002", "Design, Execution and Statistical Analysis of DoE Studies"),
    ("SOP-2007", "Operation of the Protein A Capture Chromatography Step"),
    ("SOP-2008", "Chromatography Resin Life-Cycle, Packing and Sanitization"),
    ("SOP-4001", "Process-Parameter Classification and Control-Strategy Definition"),
]
PROTEIN_A_AMV_REFS = [
    ("AMV-3016", "Leached Protein A by ELISA (ppm)"),
    ("AMV-3012", "Host-Cell Protein ELISA"),
    ("AMV-3014", "Residual DNA (qPCR)"),
    ("AMV-3011", "Size-Variants (SEC-HPLC)"),
]

# Low-pH Viral Inactivation (Step 6) controlled-document subsets. Placeholders;
# adds the inactivation-step SOP and the XMuLV infectivity assay (AMV-3017), and
# reuses the shared SEC / charge-variant methods.
VIRAL_INACT_SOP_REFS = [
    ("SOP-1001", "Qualification of Scale-Down Models"),
    ("SOP-1002", "Design, Execution and Statistical Analysis of DoE Studies"),
    ("SOP-2009", "Operation of the Low-pH Viral Inactivation Step"),
    ("SOP-4001", "Process-Parameter Classification and Control-Strategy Definition"),
]
VIRAL_INACT_AMV_REFS = [
    ("AMV-3017", "XMuLV Infectivity Titre (TCID50)"),
    ("AMV-3011", "Size-Variants (SEC-HPLC)"),
    ("AMV-3013", "Charge Variants (icIEF)"),
]

# Cation Exchange polishing (Step 7) controlled-document subsets. Placeholders;
# adds the CEX-step SOP (SOP-2010) and reuses the shared resin life-cycle SOP and
# the SEC / HCP / DNA / leached-Protein-A methods. CEX is the principal aggregate
# polish (SEC-HPLC is the primary assay) and a major HCP/DNA/leached-PA clearance step.
CEX_SOP_REFS = [
    ("SOP-1001", "Qualification of Scale-Down Models"),
    ("SOP-1002", "Design, Execution and Statistical Analysis of DoE Studies"),
    ("SOP-2010", "Operation of the Cation-Exchange Polishing Chromatography Step"),
    ("SOP-2008", "Chromatography Resin Life-Cycle, Packing and Sanitization"),
    ("SOP-4001", "Process-Parameter Classification and Control-Strategy Definition"),
]
CEX_AMV_REFS = [
    ("AMV-3011", "Size-Variants (SEC-HPLC)"),
    ("AMV-3012", "Host-Cell Protein ELISA"),
    ("AMV-3014", "Residual DNA (qPCR)"),
    ("AMV-3016", "Leached Protein A by ELISA (ppm)"),
]

# Anion Exchange polishing (Step 8) controlled-document subsets. Placeholders;
# adds the AEX-step SOP (SOP-2011) and the MVM infectivity assay (AMV-3018), and
# reuses the shared resin life-cycle SOP and the HCP / DNA / leached-Protein-A /
# XMuLV-infectivity / charge-variant methods. AEX is a flow-through final polish:
# it SETS the MVM viral-clearance CQA and is a major clearance step for HCP,
# residual DNA, leached Protein A and enveloped virus (XMuLV). The charge-variant
# (icIEF) method supports the load-material acidic-variant (deamidation) assessment.
AEX_SOP_REFS = [
    ("SOP-1001", "Qualification of Scale-Down Models"),
    ("SOP-1002", "Design, Execution and Statistical Analysis of DoE Studies"),
    ("SOP-2011", "Operation of the Anion-Exchange Polishing Chromatography Step"),
    ("SOP-2008", "Chromatography Resin Life-Cycle, Packing and Sanitization"),
    ("SOP-4001", "Process-Parameter Classification and Control-Strategy Definition"),
]
AEX_AMV_REFS = [
    ("AMV-3012", "Host-Cell Protein ELISA"),
    ("AMV-3014", "Residual DNA (qPCR)"),
    ("AMV-3016", "Leached Protein A by ELISA (ppm)"),
    ("AMV-3017", "XMuLV Infectivity Titre (TCID50)"),
    ("AMV-3018", "MVM Infectivity Titre (TCID50/qPCR)"),
    ("AMV-3013", "Charge Variants (icIEF)"),
]

# Small-Virus Retentive Filtration (Step 9) controlled-document subsets. Placeholders;
# adds the virus-filtration-step SOP (SOP-2012, operation + post-use filter integrity test)
# and reuses the MVM / XMuLV infectivity assays. Virus filtration is the dedicated
# small-virus removal step: size-based (mechanistic) clearance that is orthogonal to the
# low-pH (Step 6) and anion-exchange (Step 8) mechanisms. It provides the largest single
# MVM (parvovirus) log-reduction and a major enveloped-virus (XMuLV) log-reduction.
VIRUS_FILT_SOP_REFS = [
    ("SOP-1001", "Qualification of Scale-Down Models"),
    ("SOP-1002", "Design, Execution and Statistical Analysis of DoE Studies"),
    ("SOP-2012", "Operation and Post-Use Integrity Testing of the Small-Virus Retentive Filtration Step"),
    ("SOP-4001", "Process-Parameter Classification and Control-Strategy Definition"),
]
VIRUS_FILT_AMV_REFS = [
    ("AMV-3018", "MVM Infectivity Titre (TCID50/qPCR)"),
    ("AMV-3017", "XMuLV Infectivity Titre (TCID50)"),
]

# Ultrafiltration / Diafiltration (Step 10) controlled-document subsets. Placeholders;
# adds the UF/DF-step SOP (SOP-2013) and reuses the SEC / charge-variant / protein-A
# concentration methods. UF/DF is a formulation (mass-balance) operation reported with the
# drug product: it concentrates and buffer-exchanges to the DS target and forms/clears no
# product-quality CQA, so its parameters are KPP (process performance) not CPP.
UFDF_SOP_REFS = [
    ("SOP-1001", "Qualification of Scale-Down Models"),
    ("SOP-2013", "Operation of the Ultrafiltration / Diafiltration (Formulation) Step"),
    ("SOP-4001", "Process-Parameter Classification and Control-Strategy Definition"),
]
UFDF_AMV_REFS = [
    ("AMV-3011", "Size-Variants (SEC-HPLC)"),
    ("AMV-3019", "Protein Concentration by A280 (UV)"),
    ("AMV-3013", "Charge Variants (icIEF)"),
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


def cqas_by_keys(keys):
    """CQAs (selected by key, in the given order) that a step controls or clears.

    A downstream step (e.g. cation/anion exchange) *sets* no CQA — the impurity and
    size-variant CQAs are formed upstream and cleared here — so ``cqas_for`` returns
    nothing for it. This lists the CQAs it governs, in the requested order, with the
    same columns as :func:`cqas_for`."""
    keys = list(keys)
    d = cqa_reg[cqa_reg.key.isin(keys)].copy()
    d["__order"] = d["key"].apply(keys.index)
    d = d.sort_values("__order")
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
    sops = SOP_REFS if sops is None else sops
    amvs = AMV_REFS if amvs is None else amvs
    rows = [[sid, title, "SOP"] for sid, title in sops]
    rows += [[aid, title, "Method validation"] for aid, title in amvs]
    df = pd.DataFrame(rows, columns=["Reference", "Title", "Type"])
    return df.to_markdown(index=False)


# --------------------------------------------------------------------------- #
# Corpus-wide helpers (for the transfer / master documents, which span the      #
# whole document set and the whole process train rather than one unit op).      #
# --------------------------------------------------------------------------- #
def corpus_docs_md(doc_id=None):
    """Cross-reference table of the whole A-Mab document package.

    Lists the transfer/master documents and every per-unit-operation plan/report
    pair in process-step order, excluding ``doc_id`` (the current document)."""
    order = ["PTP-001", "RA-001", "PCMP-001"]
    for key in CFG.train_order:
        step = CFG.unit_op(key).step
        order += [f"PCP-{step:03d}", f"PCR-{step:03d}"]
    order.append("PCMR-001")
    rows = []
    for rid in order:
        if rid == doc_id or rid not in DOC_REGISTRY:
            continue
        cls, subject, _ = DOC_REGISTRY[rid]
        rows.append([rid, cls, subject])
    return pd.DataFrame(rows, columns=["Document ID", "Document class", "Subject"]).to_markdown(index=False)


# Editorial one-line role of each unit operation in the control strategy. Narrative
# only (no numbers); the quantitative facts are pulled from the CSVs elsewhere.
UNIT_OP_ROLE = {
    "bioreactor": "Forms the glycan, charge-variant and aggregate CQAs (design-space step)",
    "harvest": "Primary recovery and clarification; forms no product-quality CQA",
    "protein_a": "Capture; sets leached Protein A; principal HCP and DNA clearance",
    "viral_inactivation": "Low-pH hold; sets the cumulative XMuLV (enveloped) clearance",
    "cex": "Polish; principal aggregate reduction; major HCP/DNA/leached-PA clearance",
    "aex": "Flow-through polish; sets the cumulative MVM clearance; clears XMuLV/HCP/DNA",
    "virus_filtration": "Dedicated small-virus removal; principal MVM clearance",
    "ufdf": "Formulation / mass balance; delivers drug substance at target concentration",
}


def process_steps_df():
    """The drug-substance process train (Steps 3–10) with each step's principal role."""
    rows = []
    for key in CFG.train_order:
        uo = CFG.unit_op(key)
        rows.append([uo.step, UNIT_OP_TITLES.get(key, uo.name), UNIT_OP_ROLE.get(key, "")])
    return pd.DataFrame(rows, columns=["Step", "Unit operation", "Principal role"])


def cpp_params(kinds=("CPP", "WC-CPP")):
    """Parameters classified CPP or WC-CPP across the train (control-strategy summaries)."""
    d = param_reg[param_reg.classification.isin(list(kinds))].copy()
    d["NOR"] = d.apply(lambda r: _rng_str(r.nor_low, r.nor_high), axis=1)
    d = d.rename(columns={"unit_operation": "Unit operation", "parameter": "Parameter",
                          "unit": "Unit", "setpoint": "Set-point", "classification": "Class"})
    return d[["Unit operation", "Parameter", "Unit", "Set-point", "NOR", "Class"]]


def class_counts():
    """Parameter-classification counts across the whole train (dict, e.g. {'WC-CPP': 20, ...})."""
    return {k: int(v) for k, v in param_reg.classification.value_counts().to_dict().items()}
