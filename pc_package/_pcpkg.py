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

# Package dir and repo root = parent of pc_package/ (independent of the render CWD).
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from amab_process import load_config  # noqa: E402
from amab_process import studies as st  # noqa: E402  (re-exported)

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
    """Parameters to be studied (no post-hoc classification) — for a Plan."""
    uo = CFG.unit_op(key)
    d = param_reg[param_reg.unit_operation == uo.name].copy()
    d["Range studied"] = d.apply(lambda r: _rng_str(r.par_low, r.par_high), axis=1)
    d["NOR"] = d.apply(lambda r: _rng_str(r.nor_low, r.nor_high), axis=1)
    d = d.rename(columns={"parameter": "Parameter", "unit": "Unit", "setpoint": "Set-point",
                          "study": "Study type"})
    return d[["Parameter", "Unit", "Set-point", "Range studied", "NOR", "Study type"]]


def univariate_levels(key):
    """Planned evaluation levels for a step's univariately studied parameters — for a Plan.

    A protocol for a step with no designed experiment still has to show what will be run,
    and the analogue of a design matrix is the set of levels each parameter is taken to:
    the two edges of its characterization range, with its set-point as the reference
    condition and the other parameters held there. Values come from the same parameter
    register as ``plan_params``, so the schedule and the study-design table cannot
    disagree. Returns an empty frame for a step whose parameters are all multivariate."""
    uo = CFG.unit_op(key)
    rows = [[p.name, p.unit, p.prange[0], p.setpoint, p.prange[1], _rng_str(*p.nor)]
            for p in uo.parameters if p.study == "univariate"]
    return pd.DataFrame(rows, columns=["Parameter", "Unit", "Low level",
                                       "Reference (set-point)", "High level", "NOR"])


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
    """Markdown register of a report's seeded deviations (for the table_narration move).

    Columns: Deviation, Summary, Detected during, Disposition — sourced from
    outputs/data/deviations.csv (built from config/parameters.yaml). Returns an
    empty string for a document with no seeded deviations."""
    d = csv("deviations.csv")
    d = d[d["doc_id"] == doc_id].copy()
    if d.empty:
        return ""
    d = d.rename(columns={"dev_id": "Deviation", "summary": "Summary",
                          "detected_during": "Detected during", "disposition": "Disposition"})
    return d[["Deviation", "Summary", "Detected during", "Disposition"]].to_markdown(index=False)


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
def all_sop_table(include_base=False):
    """Every controlled document cited anywhere in the corpus, deduplicated and sorted.

    ``sop_table`` takes explicit lists, which suits a per-step document. The three parent
    documents (PTP-001, PCMP-001, PCMR-001) need the campaign-wide register instead, and
    each was building the union in its own SETUP chunk. This is that union.

    The union is built from the per-step ``<KEY>_SOP_REFS`` / ``<KEY>_AMV_REFS`` lists, so
    it omits the shared ``SOP_REFS`` / ``AMV_REFS`` registries — the defaults a step with
    no named subset draws on, which is how the bioreactor documents cite the culture
    operation SOPs and the N-glycan method. ``include_base=True`` folds those in, giving
    the complete register. It is off by default because the parent documents already
    published this table without them and their annex quotes anchor on those rows."""
    sops, amvs = ({}, {}) if not include_base else (dict(SOP_REFS), dict(AMV_REFS))
    for name, val in list(globals().items()):
        if name.endswith("_SOP_REFS") and isinstance(val, list):
            sops.update(dict(val))
        elif name.endswith("_AMV_REFS") and isinstance(val, list):
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
        # UNIT_OP_TITLES, not uo.name: the config name differs from the corpus title for
        # three steps ("Harvest / Clarification", "Small Virus Retentive Filtration",
        # "Ultrafiltration / Diafiltration (formulation)"), and PTP-001, PCMP-001, PCMR-001
        # and PCR-004 all render this table next to process_steps_df, which uses the titles.
        # A document naming one unit operation two ways in two tables is an unregistered
        # inconsistency, and those are bugs rather than benchmark items.
        rows.append([uo.step, UNIT_OP_TITLES.get(key, uo.name), len(ps), mv, len(ps) - mv,
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


def method_perf_df(precision_with_unit=False):
    """Validated performance of every analytical method the campaign relies on.

    ``dev_methods.csv`` (from ``config/parameters.yaml`` ``deviations.methods``) carries
    intermediate precision, LOQ, accuracy and the share of observed variance attributable
    to the method. A per-step report reaches one of these through an ``amv_*`` scalar; a
    parent document (analytical method transfer, campaign-level assay strategy) needs the
    whole register as one table, which is what this returns.

    ``precision_pct`` is an intermediate-precision %RSD for every method **except** the two
    infectivity assays, where the config records a log10 standard deviation. A per-step
    table that shows only %RSD methods can keep the default heading. A table that shows the
    whole register must pass ``precision_with_unit=True``, which renders each value with
    its own unit under the neutral heading "Intermediate precision"; otherwise the two
    log10 rows are published as %RSD. For the same reason, never rank the register on
    ``precision_pct`` without first restricting it to one unit — the log10 values are small
    for a reason that has nothing to do with precision."""
    d = csv("dev_methods.csv").copy()
    d["LOQ"] = d.apply(lambda r: f"{r.loq:g} {r.loq_unit}", axis=1)
    if precision_with_unit:
        prec = "Intermediate precision"
        d[prec] = d.apply(
            lambda r: f"{r.precision_pct:g} log10 SD" if "log10" in str(r.loq_unit)
            else f"{r.precision_pct:g} %RSD", axis=1)
    else:
        prec = "Precision (%RSD)"
        d = d.rename(columns={"precision_pct": prec})
    d = d.rename(columns={"id": "Method", "name": "Title",
                          "accuracy_pct": "Accuracy (%)",
                          "variance_fraction": "Variance share"})
    return d[["Method", "Title", prec, "LOQ", "Accuracy (%)", "Variance share"]]


def method_perf_for(ids, precision_with_unit=False):
    """The validated-performance rows for a named subset of analytical methods.

    ``method_perf_df`` returns the whole campaign register, which is what a parent
    document wants. A per-step report wants only the methods its own step uses, in the
    order its ``<KEY>_AMV_REFS`` list gives them. Pass either the AMV identifiers or the
    ``(id, title)`` pairs of such a list.

    ``dev_methods.csv`` carries validated performance for the methods the seeded
    deviation world needs, which is a subset of the methods a step cites. Identifiers with
    no performance row are simply absent from the result, so a document that shows this
    table must say where the remaining methods' performance is recorded."""
    ids = [x[0] if isinstance(x, (tuple, list)) else x for x in ids]
    d = method_perf_df(precision_with_unit=precision_with_unit)
    d = d[d["Method"].isin(ids)].copy()
    d["__order"] = d["Method"].apply(ids.index)
    return d.sort_values("__order").drop(columns="__order").reset_index(drop=True)


# Display labels (with units) for the nominal-batch metrics in process_summary.csv.
_STEP_METRIC_LABELS = {
    "step_yield": "Step yield (fraction of input product mass)",
    "product_mass_g": "Product mass out (g)",
    "titer_g_per_l": "Harvest titre (g/L)",
    "final_viability_pct": "Final culture viability (%)",
    "peak_vcd_e6": "Peak viable cell concentration (e6 cells/mL)",
    "turbidity_ntu": "Post-clarification turbidity (NTU)",
    "pool_hcp_ng_mg": "Pool host cell protein (ng/mg)",
    "leached_protein_a_ppm": "Leached Protein A (ppm)",
    "xmulv_lrf": "XMuLV log reduction (log10)",
    "mvm_lrf": "MVM log reduction (log10)",
    "aggregate_delta_pct": "Aggregate change across the step (% HMW)",
    "aggregate_out_pct": "Pool aggregate (% HMW)",
    "aggregate_clearance_fold": "Aggregate clearance (fold)",
    "hcp_clearance_fold": "Host cell protein clearance (fold)",
    "hcp_out_ng_mg": "Pool host cell protein (ng/mg)",
    "ds_concentration_g_per_l": "Drug substance concentration (g/L)",
    "residual_dna_ng_per_dose": "Residual DNA (ng/dose)",
}


def step_performance(step):
    """Nominal-batch performance of one process step, from ``process_summary.csv``.

    The seeded nominal batch is the at-set-point run every per-step report describes, so
    this is the step's own performance table. Only the columns the step actually populates
    are returned, which is why the shape differs from step to step.

    Emit it with ``show(step_performance(n), floatfmt=",g")``. One column holds a step yield
    of order 1 next to a product mass of order 1e4, so the automatic per-column format falls
    back to ``.3g`` and publishes the mass in scientific notation."""
    d = csv("process_summary.csv")
    row = d[d["step"] == int(step)]
    if row.empty:
        raise KeyError(f"no process-summary row for step {step!r}")
    row = row.iloc[0]
    rows = []
    for col in d.columns:
        if col in ("step", "unit_operation"):
            continue
        val = row[col]
        if pd.isna(val):
            continue
        rows.append([_STEP_METRIC_LABELS.get(col, col.replace("_", " ")), format(val, ",g")])
    return pd.DataFrame(rows, columns=["Metric", "Nominal batch"])


def harvest_impurity_load(**culture_setpoints):
    """Impurity burden the clarified harvest carries into Protein A capture.

    Harvest and clarification removes no soluble impurity: ``amab_process/unit_ops/harvest.py``
    copies the incoming attributes forward unchanged, so the clarified-harvest burden is the
    bioreactor output, and the culture endpoint sets it. This runs the bioreactor model
    deterministically (batch noise off) at its set-points, updated by any culture parameter
    passed as a keyword (e.g. ``harvest_impurity_load(duration=19)``), and returns what that
    operating point produces.

    Read these values through this helper, never off ``rsm.harvest_centre`` or ``rsm.linear``
    in the config. Those are coded-model terms and neither is a natural-unit quantity: the
    centre value omits the final-viability multiplier the model applies, and a linear
    coefficient is a change per coded unit over the half-range, not a change in ng/mg.

    Returns a dict: ``hcp`` (ng/mg), ``residual_dna`` (relative units, cleared downstream)
    and ``final_viability_pct``."""
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    from amab_process.unit_ops import Bioreactor  # noqa: PLC0415  (deferred: heavy import)
    res = Bioreactor(CFG).run(None, None, setpoints=culture_setpoints or None)
    return {"hcp": float(res.out.cqas["hcp"]),
            "residual_dna": float(res.out.cqas["residual_dna"]),
            "final_viability_pct": float(res.metrics["final_viability_pct"])}


def ra_scope(key):
    """RA-001's pre-characterization risk rows for one unit operation.

    The scope decision a PCP/PCR inherits: per parameter, the prospective failure mode and
    effect, the initial severity / occurrence / detection and RPN, the assigned study type
    and the priority. Sourced from ``ra_content`` (the curated content source for RA-001),
    so a step report and RA-001 cannot disagree about why a parameter was studied the way
    it was. ``ra_content`` imports this module, so the import is deferred to call time."""
    if _HERE not in sys.path:
        sys.path.insert(0, _HERE)
    import ra_content  # noqa: PLC0415  (deferred: ra_content imports _pcpkg)
    rows = [r for r in ra_content.ra_rows() if r["key"] == key]
    d = pd.DataFrame(rows)
    d = d.rename(columns={"param": "Parameter", "fm": "Prospective failure mode",
                          "eff": "Effect", "severity": "Sev.", "o_init": "Occ.",
                          "d_init": "Det.", "rpn_init": "Initial RPN",
                          "study": "Assigned study", "priority": "Priority"})
    return d[["Parameter", "Prospective failure mode", "Effect", "Sev.", "Occ.", "Det.",
              "Initial RPN", "Assigned study", "Priority"]]


def risk_scale(kind):
    """A score -> label map from the config risk scales ('severity', 'occurrence', 'detection')."""
    return {int(s["score"]): s["label"] for s in CFG.risk[f"{kind}_scale"]}


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


def yield_waterfall_df():
    """Step and cumulative product yield across the train (Steps 3-10).

    ``process_steps_df`` says what each step is for; this says what each step costs. The
    master report needs both, and the cumulative column is the one number a reader checks
    against the drug-substance mass. Emit it with an explicit ``floatfmt`` — the automatic
    per-column choice sees a step number next to two percentages and falls back to ``.3g``,
    which prints 97.68 % as 97.7 and 100.0 % as 100."""
    d = csv("yield_waterfall.csv").copy()
    d["Step yield (%)"] = 100.0 * d["step_yield"]
    d["Cumulative yield (%)"] = 100.0 * d["cumulative_yield"]
    d = d.rename(columns={"step": "Step", "unit_operation": "Unit operation"})
    return d[["Step", "Unit operation", "Step yield (%)", "Cumulative yield (%)"]]


def _criterion_str(row):
    """A CQA's governing acceptance limit, written the way its spec type applies it.

    ``cqas_for`` / ``cap_for`` render acceptance as ``low–high`` for every attribute, which
    is right beside a ``Spec`` column and wrong without one: for an impurity with an upper
    specification the lower figure is not an acceptance limit, and a table that shows a
    simulated minimum below it invites a reviewer to read a failure that is not there."""
    if row["spec_type"] == "upper":
        return f"≤ {row['acc_high']:g} {row['unit']}"
    if row["spec_type"] == "lower":
        return f"≥ {row['acc_low']:g} {row['unit']}"
    return f"{row['acc_low']:g}–{row['acc_high']:g} {row['unit']}"


def _meets_criterion(row):
    """True if the whole simulated distribution sits inside the CQA's acceptance criterion."""
    if row["spec_type"] == "upper":
        return bool(row["max"] <= row["acc_high"])
    if row["spec_type"] == "lower":
        return bool(row["min"] >= row["acc_low"])
    return bool(row["min"] >= row["acc_low"] and row["max"] <= row["acc_high"])


def cqa_scope_df():
    """The CQA register with the step that sets each attribute and the report that covers it.

    ``all_cqas`` gives the register as a per-step document needs it. A corpus-level document
    also needs the ``set_by`` column — the corpus's own statement of which unit operation
    each attribute belongs to — and the per-step report where its characterization lives."""
    d = cqa_reg.copy()
    d["Acceptance"] = d.apply(lambda r: f"{r.acc_low:g}–{r.acc_high:g} {r.unit}", axis=1)
    d["Set by"] = d["set_by"].map(lambda k: UNIT_OP_TITLES.get(k, k))
    d["Report"] = d["set_by"].map(lambda k: f"PCR-{CFG.unit_op(k).step:03d}")
    d = d.rename(columns={"cqa": "CQA", "category": "Category",
                          "criticality": "Criticality"})
    return d[["CQA", "Category", "Criticality", "Acceptance", "Set by", "Report"]]


def cqa_outcome_df():
    """Per-CQA outcome across the simulated commercial batches: range, criterion, verdict.

    ``cap_for`` answers "how capable is the process". The question a master report has to
    answer first is blunter: did any simulated batch miss its criterion. ``capability.csv``
    carries the minimum and maximum of the distribution, which ``cap_for`` drops, and the
    verdict is read off those against the spec type rather than against both bounds.

    There is deliberately no ``Spec`` column. ``_criterion_str`` has already applied the
    spec type, so a raw ``two_sided`` token beside a criterion that reads ``≤ 5`` would only
    repeat it; ``cap_for`` keeps the column because its acceptance column does not."""
    d = cap.copy()
    d["Criterion"] = d.apply(_criterion_str, axis=1)
    d["Simulated range"] = d.apply(lambda r: f"{r['min']:.4g} – {r['max']:.4g}", axis=1)
    d["Outcome"] = d.apply(lambda r: "met" if _meets_criterion(r) else "not met", axis=1)
    d = d.rename(columns={"cqa": "CQA"})
    return d[["CQA", "Criterion", "Simulated range", "Outcome"]]


def viral_clearance_df():
    """Modular viral clearance by claimed step, with the cumulative total and the requirement.

    ``viral_clearance.csv`` credits only the steps a claim is made for, so the cumulative row
    is the sum of exactly those. The requirement is the lower acceptance bound of the two
    viral-safety CQAs in ``cqa_register.csv``; joining it here keeps the comparison out of a
    document setup chunk. Emit with ``floatfmt=".2f"``: the automatic choice rounds a
    cumulative 10.03 to 10."""
    d = csv("viral_clearance.csv").rename(columns={"step": "Step", "XMuLV": "XMuLV LRF",
                                                   "MVM": "MVM LRF"})
    req = {"Step": "Requirement (drug substance)"}
    for col, key in (("XMuLV LRF", "lrv_xmulv"), ("MVM LRF", "lrv_mvm")):
        req[col] = float(cqa_reg[cqa_reg["key"] == key].iloc[0]["acc_low"])
    return pd.concat([d, pd.DataFrame([req])], ignore_index=True)


def dev_register_all():
    """Every seeded deviation in the campaign, with the report that investigates it.

    ``dev_register(doc_id)`` is the per-report view, and it is a markdown string because a
    per-step report prints it and narrates it. The campaign-level register is a DataFrame:
    the master report groups and counts it before showing it, and the report ID is what
    makes each row traceable to the investigation."""
    d = csv("deviations.csv").copy()
    d["Disposition"] = d["disposition"].str.replace("_", " ")
    d = d.rename(columns={"dev_id": "Deviation", "doc_id": "Report", "summary": "Summary",
                          "detected_during": "Detected during"})
    return d[["Deviation", "Report", "Summary", "Detected during", "Disposition"]]


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
