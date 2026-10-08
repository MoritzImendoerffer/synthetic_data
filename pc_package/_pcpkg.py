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
from ctable import C, CTable  # noqa: E402,F401  (re-exported: complex tables, Rev 2.0)

CFG = load_config()
DATA = os.path.join(ROOT, "outputs", "data")
FIG = "../outputs/figures"  # markdown image paths are relative to a doc in pc_package/
V = json.load(open(os.path.join(ROOT, "outputs", "report_values.json")))

# Seeded deviation / lot / equipment / method scalars (the density-pass "messy
# campaign" facts). Originate in config/parameters.yaml -> amab_process/deviations.py
# -> report_values.json (single source of truth). Exposed here as bare module globals
# so documents can reference them as inline expressions, e.g. `{python} dev_007_02_tmax`
# or `{python} lot_buf_2287_expiry`. Guarded so a malformed or colliding key can never
# shadow a helper. Naming rule: scalar = <id>.lower().replace('-','_') + '_' + <field>.
DEV_SCALARS = V.get("dev_scalars", {})
for _dev_name, _dev_val in DEV_SCALARS.items():
    if _dev_name.isidentifier() and _dev_name not in globals():
        globals()[_dev_name] = _dev_val

# Package-wide document metadata. Rev 2.0 (INV-001): every Rev 1.0 document is reissued, and
# INV-001 is new at its own Version 1.0. Dates come from config campaign: (seed-independent).
CAMPAIGN = CFG.raw()["campaign"]
REVISIONS = CAMPAIGN["revisions"]                       # [{rev, effective, reason}, ...]
REV1, REV2 = REVISIONS[0], REVISIONS[-1]
INV = CAMPAIGN["investigation"]
AMD = CAMPAIGN["method_decision"]
EFFECTIVE_DATE = REV2["effective"]
VERSION = REV2["rev"]


PLAN_APPROVAL = CAMPAIGN.get("plan_approval", {})
CAPA = pd.DataFrame(CAMPAIGN.get("capa", []))
PLAN_DISCREPANCIES = CAMPAIGN.get("plan_discrepancies", {})   # {report: [{id, plan, planned, done, ...}]}
EFFECTIVENESS = CAMPAIGN.get("effectiveness_check", {})
THRESHOLDS = CAMPAIGN.get("thresholds", {})
CPK_TARGET = THRESHOLDS.get("cpk_target")
CPK_MIN = THRESHOLDS.get("cpk_minimum")


def rev1_date(doc_id):
    """Version 1.0 approval date: before the studies for a plan, the package date otherwise."""
    return PLAN_APPROVAL.get(doc_id, REV1["effective"])


def doc_version(doc_id):
    """(version, effective date) of a document at its current revision."""
    if doc_id == INV["id"]:
        return "1.0", INV["closed"]
    return VERSION, EFFECTIVE_DATE
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
    "INV-001": ("Investigation Report", CAMPAIGN["investigation"]["title"], None),
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
    ("SOP-3015", "Purity by Non-Reduced CE-SDS"),
    ("SOP-4001", "Process-Parameter Classification and Control-Strategy Definition"),
]
AMV_REFS = [
    ("AMV-3010", "N-Glycan Map (2-AB HILIC-UPLC)"),
    ("AMV-3011", "Size-Variants (SEC-HPLC)"),
    ("AMV-3012", "Host-Cell Protein ELISA"),
    ("AMV-3013", "Charge Variants (icIEF)"),
    ("AMV-3014", "Residual DNA (qPCR)"),
    ("AMV-3020", "Purity (non-reduced CE-SDS)"),
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


def _auto_floatfmt(df):
    """Per-column float formats: keep plain magnitudes plain, leave everything else at .3g.

    The default ``.3g`` renders a 9000 g set-point as ``9e+03`` and a 500,000 ng/mg burden
    as ``5e+05`` — a measurement disguised as a machine artifact. It is right for the rest
    of the corpus, though: a p-value of 1.7e-53 and an F of 3.9e+26 belong in scientific
    notation, so a blanket change would be worse than the bug.

    A column therefore switches to fixed notation only when it is unambiguously a column of
    plain magnitudes: every finite non-zero value at least 1, and the largest between 1000
    and 10 million. p-value and coefficient columns fail the lower bound; the degenerate
    F-statistics at the viral-inactivation step (order 1e26, which the report itself flags
    as uninformative) fail the upper one. Both keep ``.3g``, which is what they want.
    """
    import numpy as _np
    import pandas as _pd
    fmts = []
    for col in df.columns:
        s = df[col]
        fmt = ".3g"
        if _pd.api.types.is_numeric_dtype(s) and not _pd.api.types.is_bool_dtype(s):
            v = _np.abs(s.to_numpy(dtype=float))
            v = v[_np.isfinite(v) & (v != 0)]
            if v.size and v.min() >= 1 and 1000 <= v.max() < 1e7:
                whole = _np.allclose(v, _np.round(v))
                fmt = ",.0f" if whole else ",.1f"
        fmts.append(fmt)
    return fmts


def show(df, floatfmt=None):
    """Emit a DataFrame as a GitHub-markdown table (Quarto renders it to docx/pdf).

    ``floatfmt`` overrides the automatic per-column choice (see ``_auto_floatfmt``)."""
    print(df.to_markdown(index=False, floatfmt=floatfmt or _auto_floatfmt(df)))


param_reg = csv("parameter_classification.csv")
cqa_reg = csv("cqa_register.csv")
cap = csv("capability.csv")


def _rng_str(lo, hi):
    return f"{lo:g}–{hi:g}"


def plan_params(key):
    """Parameters to be studied (no post-hoc classification) — for a Plan. The NOR is the one the
    studies were planned against (``nor_char_*``), never a NOR a Version 2.0 report narrowed."""
    uo = CFG.unit_op(key)
    d = param_reg[param_reg.unit_operation == uo.name].copy()
    d["Range studied"] = d.apply(lambda r: _rng_str(r.par_low, r.par_high), axis=1)
    lo_, hi_ = ("nor_char_low", "nor_char_high") if "nor_char_low" in d else ("nor_low", "nor_high")
    d["NOR"] = d.apply(lambda r: _rng_str(r[lo_], r[hi_]), axis=1)
    d = d.rename(columns={"parameter": "Parameter", "unit": "Unit", "setpoint": "Set-point",
                          "study": "Study type"})
    return d[["Parameter", "Unit", "Set-point", "Range studied", "NOR", "Study type"]]


def report_params(key):
    """Parameters with final classification — for a Report.

    The range column is the **characterization range** (the DoE / knowledge-space edges),
    NOT a proven acceptable range: the PAR is a computed, per-CQA quantity (see
    ``doe_report.par_table`` and the report's Proven-acceptable-ranges section)."""
    uo = CFG.unit_op(key)
    d = param_reg[param_reg.unit_operation == uo.name].copy()
    d["NOR"] = d.apply(lambda r: _rng_str(r.nor_low, r.nor_high), axis=1)
    d["Char. range"] = d.apply(lambda r: _rng_str(r.par_low, r.par_high), axis=1)
    d = d.rename(columns={"parameter": "Parameter", "unit": "Unit", "setpoint": "Set-point",
                          "classification": "Class", "study": "Study"})
    return d[["Parameter", "Unit", "Set-point", "NOR", "Char. range", "Class", "Study"]]


def cqas_for(key):
    """CQAs primarily set/controlled by a unit operation, with acceptance criteria."""
    d = cqa_reg[cqa_reg.set_by == key].copy()
    d["Acceptance"] = d.apply(_acc_text, axis=1)
    d = d.rename(columns={"cqa": "CQA", "category": "Category", "criticality": "Criticality",
                          "tool1_score": "Tool #1"})
    return d[["CQA", "Category", "Acceptance", "Criticality", "Tool #1"]]


def _acc_text(r):
    """A CQA criterion as its spec type reads: a clearance has a floor only, an impurity a
    ceiling only. Version 1.0 printed both ends of the config range for every attribute, so
    viral clearance read "16.7–30" as if an upper limit on clearance existed."""
    st_ = getattr(r, "spec_type", "two_sided")
    if st_ == "lower":
        return f"≥ {r.acc_low:g} {r.unit}"
    if st_ == "upper":
        return f"≤ {r.acc_high:g} {r.unit}"
    return f"{r.acc_low:g}–{r.acc_high:g} {r.unit}"


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
    d["Acceptance"] = d.apply(_acc_text, axis=1)
    d = d.rename(columns={"cqa": "CQA", "category": "Category", "criticality": "Criticality",
                          "tool1_score": "Tool #1"})
    return d[["CQA", "Category", "Acceptance", "Criticality", "Tool #1"]]


def _acc_text(r):
    """A CQA criterion as its spec type reads: a clearance has a floor only, an impurity a
    ceiling only. Version 1.0 printed both ends of the config range for every attribute, so
    viral clearance read "16.7–30" as if an upper limit on clearance existed."""
    st_ = getattr(r, "spec_type", "two_sided")
    if st_ == "lower":
        return f"≥ {r.acc_low:g} {r.unit}"
    if st_ == "upper":
        return f"≤ {r.acc_high:g} {r.unit}"
    return f"{r.acc_low:g}–{r.acc_high:g} {r.unit}"


def cap_for(keys):
    """Commercial-scale capability rows for the given CQA keys."""
    d = cap[cap.key.isin(keys)].copy()
    d["Acceptance"] = d.apply(lambda r: _acc_text(r).replace(f" {r.unit}", ""), axis=1)
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


def doe_centre_points(key, kind):
    """Number of centre-point replicates in a DoE design.

    Read from the design rather than assumed. The ground-truth annexes previously carried
    these counts as literals; they happened to be right for every step, which is exactly
    what makes that pattern dangerous — a reseed or a design change updates the document
    and leaves the annex asserting the old value, and grounding cannot catch it because
    the number lives in a StudyDesign field rather than in a quote."""
    return int((csv(f"doe_{key}_{kind}.csv").run_type == "center").sum())


# --------------------------------------------------------------------------- #
# Deviation facts (density-pass narrated-deviation sections).                  #
# --------------------------------------------------------------------------- #
def dev_register(doc_id):
    """Markdown register of a report's seeded deviations, for the deviations section to introduce and walk.

    Columns: Deviation, Summary, Detected during, Disposition — sourced from
    outputs/data/deviations.csv (built from config/parameters.yaml). Returns an
    empty string for a document with no seeded deviations."""
    d = csv("deviations.csv")
    d = d[d["doc_id"] == doc_id].copy()
    if d.empty:
        return ""
    d = d.rename(columns={"dev_id": "Deviation", "summary": "Summary",
                          "detected_during": "Detected during", "disposition": "Disposition"})
    # dispositions are config tokens (supplementary_runs_executed); print them as words
    d["Disposition"] = d["Disposition"].astype(str).str.replace("_", " ")
    return d[["Deviation", "Summary", "Detected during", "Disposition"]].to_markdown(index=False)


def discrepancy_register(doc_id):
    """Markdown register of a report's discrepancies from its plan: what the plan foresaw, what
    was done, and why. A discrepancy is not a deviation (config ``campaign.plan_discrepancies``).
    Returns an empty string for a document with none."""
    ds = PLAN_DISCREPANCIES.get(doc_id, [])
    if not ds:
        return ""
    rows = [[d["id"], d["subject"], f"{d['plan']}: {d['planned']}", d["done"], d["reason"]] for d in ds]
    return md_table(["Discrepancy", "Subject", "Planned", "Done", "Reason"], rows, [12, 18, 22, 22, 26])


def dev_facts(doc_id):
    """Row(s) of the deviation register for a document (structured access)."""
    d = csv("deviations.csv")
    return d[d["doc_id"] == doc_id].reset_index(drop=True)


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
    ver, eff = doc_version(doc_id)
    rows = [
        ("Document ID", doc_id),
        ("Document class", cls),
        ("Title", f"{cls} — {subject}" if unit_op is None else f"{cls}: {unit_op}"),
        ("Product", PRODUCT),
        ("Version", ver),
        ("Effective date", eff),
        ("Supersedes", "—" if doc_id == INV["id"] else f"{doc_id} Version {REV1['rev']} ({rev1_date(doc_id)})"),
        ("Status", "Approved (synthetic)"),
        ("Document owner", "Quality Assurance (QA)" if doc_id == INV["id"]
         else "Manufacturing Science & Technology (MSAT)"),
        ("Sponsor / sites", f"{COMPANY}; {SENDING_SITE} → {RECEIVING_SITE}"),
    ]
    return md_table(["Field", "Value"], rows, [22, 78])


def md_table(header, rows, widths):
    """A pipe table with fixed relative column widths (``widths`` in percent).

    Pandoc sets a pipe table's column widths from the length of the dash runs in its separator
    line, but only when some line is longer than 72 characters. ``df.to_markdown()`` sizes the
    dashes to the content, so a short column such as "Version" got a width below its own header
    and the header overflowed into the next column (owner's comment 2026-10-08). Here the
    separator line is padded to more than 72 characters and the dashes follow ``widths``.
    Cells are written as they are, so a cell must not contain "|"."""
    sep = "|" + "|".join(":" + "-" * max(3, int(w)) for w in widths) + "|"
    out = ["| " + " | ".join(str(h) for h in header) + " |", sep]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def abbreviations_table(pairs):
    """The Abbreviations section as a two-column table, sorted case-insensitively.

    ``pairs`` is a list of ``(abbreviation, expansion)`` the author writes in the document."""
    rows = sorted(((a, e) for a, e in pairs), key=lambda p: p[0].lower())
    return md_table(["Abbreviation", "Meaning"], rows, [20, 80])


def revision_history(doc_id):
    """The revision-history table: every revision of the document, oldest first."""
    if doc_id == INV["id"]:
        rows = [["1.0", INV["closed"], "Initial issue"]]
    else:
        rows = [[r["rev"], rev1_date(doc_id) if r is REV1 else r["effective"],
                 r["reason"] + (f" (see {INV['id']})" if r is not REV1 else "")] for r in REVISIONS]
    return md_table(["Version", "Effective date", "Description of change"], rows, [12, 18, 70])


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
    order.append(INV["id"])
    rows = []
    for rid in order:
        if rid == doc_id:
            continue
        cls, subject, _ = DOC_REGISTRY[rid]
        rel = {"PTP-001": "Parent — transfer scope",
               "RA-001": "Parent — risk basis for study scope",
               "PCMP-001": "Parent — master plan",
               "PCMR-001": "Rolls up into",
               INV["id"]: "Reason for this revision",
               }.get(rid, "Sibling — paired document")
        rows.append([rid, f"{cls} ({subject})", rel])
    return md_table(["Document ID", "Title", "Relationship"], rows, [16, 54, 30])


def sop_table(sops=None, amvs=None):
    sops = SOP_REFS if sops is None else sops
    amvs = AMV_REFS if amvs is None else amvs
    rows = [[sid, title, "SOP"] for sid, title in sops]
    rows += [[aid, title, "Method validation"] for aid, title in amvs]
    return md_table(["Reference", "Title", "Type"], rows, [16, 62, 22])


# --------------------------------------------------------------------------- #
# Corpus-wide helpers (for the transfer / master documents, which span the      #
# whole document set and the whole process train rather than one unit op).      #
# --------------------------------------------------------------------------- #
def all_sop_table():
    """Every controlled document cited anywhere in the corpus, deduplicated and sorted.

    ``sop_table`` takes explicit lists, which suits a per-step document. The three parent
    documents (PTP-001, PCMP-001, PCMR-001) need the campaign-wide register instead, and
    each was building the union in its own SETUP chunk. This is that union."""
    sops, amvs = {}, {}
    for name, val in list(globals().items()):
        # `endswith("SOP_REFS")`, not `"_SOP_REFS"`: the base SOP_REFS / AMV_REFS lists do not
        # carry a step prefix, and requiring one silently excluded them. That dropped the
        # bioreactor operation procedures, every shared analytical SOP and one method validation
        # from a register whose docstring promises every controlled document in the corpus, so
        # PTP-001 and PCMP-001 rendered an operation SOP for Steps 4-10 and none for Step 3.
        # Found independently by three authors in the 2026-08-21 batch; fixed 2026-08-21.
        if name.endswith("SOP_REFS") and isinstance(val, list):
            sops.update(dict(val))
        elif name.endswith("AMV_REFS") and isinstance(val, list):
            amvs.update(dict(val))
    return sop_table(sorted(sops.items()), sorted(amvs.items()))


def all_cqas():
    """The full drug-substance CQA register, in config order.

    Equivalent to ``cqas_by_keys(list(cqa_reg["key"]))``, which is what the corpus-level
    documents were each writing out."""
    return cqas_by_keys(list(cqa_reg["key"]))


def char_scope_df():
    """Characterization scope per step: parameters, study-type split, covering documents.

    The natural parent-document table — it says what the campaign covers and which
    plan/report pair covers it. Derived from the parameter register and the train order,
    so a config change flows through."""
    rows = []
    for key in CFG.train_order:
        uo = CFG.unit_op(key)
        ps = uo.parameters
        mv = sum(1 for p in ps if p.study == "multivariate")
        rows.append([uo.step, uo.name, len(ps), mv, len(ps) - mv,
                     f"PCP-{uo.step:03d} / PCR-{uo.step:03d}"])
    return pd.DataFrame(rows, columns=["Step", "Unit operation", "Parameters",
                                       "Multivariate", "Univariate", "Documents"])


def equipment_df():
    """Instrumented scale-down systems under calibration and change control.

    Note ``cal_due`` is the NEXT calibration date and pre-dates the document effective
    date: the studies were executed before it, which is what ``calibration_status``
    records. Correct in a report of completed work; think before surfacing it in a
    prospective document, where a past date reads as overdue."""
    d = csv("dev_equipment.csv").rename(columns={
        "id": "Equipment", "description": "Description",
        "calibration_status": "Calibration status", "cal_due": "Next calibration due"})
    d["Calibration status"] = d["Calibration status"].str.replace("_", " ")
    return d


def corpus_docs_md(doc_id=None):
    """Cross-reference table of the whole A-Mab document package.

    Lists the transfer/master documents and every per-unit-operation plan/report
    pair in process-step order, excluding ``doc_id`` (the current document)."""
    order = ["PTP-001", "RA-001", "PCMP-001"]
    for key in CFG.train_order:
        step = CFG.unit_op(key).step
        order += [f"PCP-{step:03d}", f"PCR-{step:03d}"]
    order.append("PCMR-001")
    order.append(INV["id"])
    rows = []
    for rid in order:
        if rid == doc_id or rid not in DOC_REGISTRY:
            continue
        cls, subject, _ = DOC_REGISTRY[rid]
        rows.append([rid, cls, subject])
    return md_table(["Document ID", "Document class", "Subject"], rows, [16, 40, 44])


# Editorial one-line role of each unit operation in the control strategy. Narrative
# only (no numbers); the quantitative facts are pulled from the CSVs elsewhere.
UNIT_OP_ROLE = {
    "bioreactor": "Forms the glycan, charge-variant and aggregate CQAs (design-space step)",
    "harvest": "Primary recovery and clarification; forms no product-quality CQA",
    "protein_a": "Capture; principal HCP and DNA clearance; source of leached Protein A",
    "viral_inactivation": "Low-pH hold; inactivates enveloped virus (XMuLV credit)",
    "cex": "Polish; principal aggregate reduction; major HCP/DNA/leached-PA clearance",
    "aex": "Flow-through polish; clears HCP, DNA and virus (XMuLV and MVM credit)",
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
