"""Build the ground-truth annexes for the bioreactor PC Plan/Report pair.

The annexes are derived from the SAME seeded CSVs the Quarto documents render
(``outputs/data/*.csv`` via ``_pcpkg``), so every value in the ground truth
matches the corresponding document by construction. Verbatim ``quote`` fields are
short fragments of the authored prose that appear in the rendered text. Each
annex validates against ``schema_ext.GroundTruthAnnex``.

Run:  python build_ground_truth.py
Writes: ground_truth/PCP-003.json, ground_truth/PCR-003.json
"""
from __future__ import annotations

import json
import os
import re
import numpy as np  # Rev 2.0 helpers (acceptance_criteria_layer)

import _pcpkg as P
import schema_ext as S
from check_grounding import CELL_SEP   # the one definition of a rendered cell boundary

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ground_truth")

UO = "bioreactor"
UO_NAME = "Production Bioreactor"
STEP = P.CFG.unit_op(UO).step
STEP_LABEL = f"{UO_NAME} (Step {STEP})"

SCALE_L = f"{P.V['commercial_scale_l']:,}"   # as the documents render it

PCP_FILE = "PCP-003_bioreactor.docx"
PCR_FILE = "PCR-003_bioreactor.docx"


# --------------------------------------------------------------------------- #
# Reference data (straight from the seeded registers).                         #
# --------------------------------------------------------------------------- #
PARAM_ROWS = P.param_reg[P.param_reg.unit_operation == UO_NAME].to_dict("records")
CQA_ROWS = P.cqa_reg[P.cqa_reg.set_by == UO].to_dict("records")

PARAM_CONCEPT = {
    "Culture pH": "param:culture_ph",
    "Culture temperature": "param:culture_temperature",
    "Dissolved CO2 (pCO2)": "param:dissolved_co2",
    "Osmolality": "param:osmolality",
    "Culture duration": "param:culture_duration",
    "Dissolved oxygen": "param:dissolved_oxygen",
    "Initial viable cell conc.": "param:initial_vcc",
    "Basal medium concentration": "param:medium_concentration",
    "Nutrient feed-1 volume": "param:feed1_volume",
}
CQA_CONCEPT = {
    "afucosylation": "attr:afucosylation", "galactosylation": "attr:galactosylation",
    "high_mannose": "attr:high_mannose", "aggregates_hmw": "attr:aggregates_hmw",
    "acidic_variants": "attr:acidic_variants", "hcp": "attr:hcp",
    "residual_dna": "attr:residual_dna",
}
# CQA key -> validated method that measures it in this unit op.
CQA_METHOD = {
    "afucosylation": "AMV-3010", "galactosylation": "AMV-3010", "high_mannose": "AMV-3010",
    "acidic_variants": "AMV-3013", "aggregates_hmw": "AMV-3011",
    "hcp": "AMV-3012", "residual_dna": "AMV-3014",
}
METHODS = [
    ("AMV-3010", "N-Glycan Map (2-AB HILIC-UPLC)", "chromatography",
     ["afucosylation", "high mannose", "galactosylation"],
     ["afucosylation", "galactosylation", "high_mannose"]),
    ("AMV-3011", "Size-Variants (SEC-HPLC)", "chromatography",
     ["aggregate", "monomer", "fragments"], ["aggregates_hmw"]),
    ("AMV-3012", "Host-Cell Protein ELISA", "immunoassay", ["host-cell protein"], ["hcp"]),
    ("AMV-3013", "Charge Variants (icIEF)", "electrophoresis",
     ["acidic variants", "main peak", "basic variants"], ["acidic_variants"]),
    ("AMV-3014", "Residual DNA (qPCR)", "qPCR", ["residual host-cell DNA"], ["residual_dna"]),
]


def meta(basis="explicit", conf="high"):
    return S.ExtractionMetadata(
        extraction_source="human", basis=basis, confidence=conf,
        human_review_status="accepted", reviewer="MSAT (synthetic ground truth)",
    )


def par_basis_text(uo_key, cqa_label):
    """Acceptance basis for a ProvenAcceptableRange, derived from the engine.

    These strings used to be written out per step, which meant the annex asserted a basis
    the analysis no longer used the moment the criteria moved. The basis is now read from
    ``doe_report`` for the response behind the table row, so it cannot drift from the
    criterion the PAR was actually computed against."""
    import doe_report as D
    resp = next((r for r in D.responses(uo_key)
                 if D.RESP_LABEL.get(r, r) == cqa_label), None)
    if resp is None:
        return ("Acceptance criterion applied to this attribute at the outlet of the step.")
    lo, hi, stype = D.effective_acceptance(uo_key, resp)
    limit = f"at or above {lo:.3g}" if stype == "lower" else f"at or below {hi:.3g}"
    if D.acceptance_basis(uo_key, resp) == "drug substance":
        if stype == "lower":
            return ("Step-level required log-reduction, back-calculated from the cumulative "
                    "viral-clearance requirement minus the clearance credited to the other "
                    "orthogonal steps (modular viral-safety claim under ICH Q5A(R2)); the "
                    f"step contribution must be {limit} log10.")
        return ("Drug-substance specification for the attribute, applied directly at the "
                f"outlet of this step ({limit}). No downstream clearance is credited against "
                "it, so the specification is itself the binding in-process criterion.")
    ent = ((D.CFG.ipc_limits.get("steps") or {}).get(uo_key, {}) or {}).get(resp) or {}
    if "from_capability" in ent:
        k = D.CFG.ipc_limits.get("capability_alert_sigma")
        return ("In-process alert limit set from demonstrated capability at "
                f"mean + {k:g} standard deviations ({limit}). The attribute is not modified "
                "downstream, so the drug-substance specification already applies here and is "
                "the wider of the two; capability is what binds.")
    if "from_modular_claim" in ent:
        a = D.CFG.ipc_limits.get("viral_assay_allowance")
        return ("In-process criterion set from the log-reduction claimed for this step in the "
                f"modular clearance table, less an assay allowance of {a:g} log10 ({limit}).")
    m = (ent.get("from_ds_backcalc") or {}).get("margin")
    return ("In-process limit carried back from the drug-substance specification through the "
            "clearance the downstream steps deliver in the nominal train, then divided by an "
            f"assurance margin of {m:g} ({limit}).")


def ref(doc_id, file_name, section_id, section_title, quote, table_title=None, table_id=None,
        table_header=None):
    """A SourceReference. ``table_header`` is the rendered header row of the anchor table.

    Pass ``rows.header`` from :func:`row_quotes` whenever the quote is a row of that table:
    the row alone does not say which column is which (see ``schema_ext.SourceReference``).
    """
    return S.SourceReference(
        document_id=doc_id, document_title=P.DOC_REGISTRY[doc_id][0], file_name=file_name,
        section_id=section_id, section_title=section_title,
        heading_path=[section_title], table_id=table_id, table_title=table_title, quote=quote,
        table_header=table_header,
    )


def _join_cells(cells):
    """Join the cells of one rendered row the way ``check_grounding.docx_text`` reads them.

    Whitespace is collapsed after joining, so an empty cell reads as the bare separator on both
    sides of the comparison rather than dropping out of the row. The cell text is kept exactly
    as the DataFrame holds it — including "log₁₀", which two rendered documents disagree about
    (see ``check_grounding.SCRIPT_DIGITS``); reconciling that is the checker's job, so the
    annex keeps the form the data uses.
    """
    return re.sub(r"\s+", " ", CELL_SEP.join(c.strip() for c in cells)).strip()


def row_quotes(df, keys, floatfmt=None):
    """``{key -> rendered table row}`` for a table the document renders.

    A quote has two jobs, and grounding is only the first. A table caption or a bare label
    grounds perfectly well while attesting nothing: one span then stands in for every row of
    the table, so the reference says "somewhere in this document" instead of naming the
    evidence. Anchoring each record on **its own row** gives a span that carries both ends of
    the relation — the parameter and its set-point, the attribute and its acceptance
    criterion — which is what makes the annex usable for attribution and evidence retrieval.

    ``_md_rows`` reproduces the rendered row from the same DataFrame the document renders, so
    the quote stays verbatim and stays correct when the seed changes.
    ``check_grounding.specificity_report`` flags the alternative.

    The result also carries ``.header`` — the rendered header row of the same table — to pass
    as ``ref(..., table_header=rows.header)``. A row says ``"… | 6.75–6.95 | 6.6–7.1 | …"``
    and only the header says which of the two is the normal operating range.
    """
    out = RowQuotes(zip(list(keys), _md_rows(df, floatfmt)))
    out.header = _join_cells(str(c) for c in df.columns)
    return out


class RowQuotes(dict):
    """``{key -> rendered row}`` plus the rendered ``header`` row they share."""
    header: str = ""


# --------------------------------------------------------------------------- #
# Version 2.0: complex tables, revision history, acceptance criteria            #
# --------------------------------------------------------------------------- #
def ctable_rows(table, keys=None):
    """``{key -> rendered row}`` for a :class:`ctable.CTable` the document prints.

    Pass the table from the SAME builder call the document makes (``T.iac_derivation(["cex"])``),
    so the rows are the rendered rows. A row continuing a vertical merge starts with an empty
    cell (``"| …"``), exactly as ``check_grounding.docx_text`` reads it; its merged label lives in
    the row above, so the record that anchors on it must carry that label itself. ``.header`` is
    every header row, joined as the DOCX reads them.
    """
    rows = table.rows()
    keys = list(range(len(rows))) if keys is None else list(keys)
    if len(keys) != len(rows):
        raise ValueError(f"{table.label}: {len(keys)} keys for {len(rows)} rows")
    out = RowQuotes(zip(keys, rows))
    out.header = re.sub(r"\s+", " ", CELL_SEP.join(table.header_rows())).strip()
    return out


def revision_layer(doc_id, file_name, section="Revision history"):
    """(supersedes, [RevisionEntry]) anchored on the rendered revision-history rows."""
    import pandas as _pd
    hist = P.revision_history(doc_id)
    rows = [ln for ln in hist.splitlines()[2:] if ln.strip()]
    entries = []
    for ln in rows:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        entries.append(S.RevisionEntry(
            revision=cells[0], effective_date=cells[1], description=cells[2],
            source=ref(doc_id, file_name, f"{doc_id}_rev", section, _join_cells(cells),
                       table_header=_join_cells(["Version", "Effective date", "Description of change"]))))
    sup = None if doc_id == P.INV["id"] else f"{doc_id} Version {P.REV1['rev']}"
    return sup, entries


def acceptance_criteria_layer(doc_id, file_name, section, table, steps=None):
    """AcceptanceCriterionRecord list from a ``T.criteria_change(steps)`` table the document
    prints: one superseded Version 1.0 record and one in-force Version 2.0 record per row that has
    them, each anchored on that row."""
    import tables as T
    new = P.csv("iac.csv")
    old = P.csv("criteria_rev1.csv")
    if steps:
        new, old = new[new["step_key"].isin(steps)], old[old["step_key"].isin(steps)]
    # the row order of criteria_change: steps in train order, then the union of responses
    rq = ctable_rows(table)
    keys = sorted(set(zip(new["step"], new["step_key"], new["response"])) |
                  set(zip(old["step"], old["step_key"], old["response"])))
    by_step = {}
    for _, sk, resp in keys:
        by_step.setdefault(sk, []).append(resp)
    order = [(sk, r) for sk in sorted(by_step, key=lambda k: P.CFG.unit_op(k).step) for r in by_step[sk]]
    if len(order) != len(rq):
        raise ValueError(f"criteria_change rows {len(rq)} != records {len(order)}")
    out = []
    for i, (sk, resp) in enumerate(order):
        q = ref(doc_id, file_name, f"{doc_id}_crit", section, rq[i], table_title=table.caption,
                table_id=table.label, table_header=rq.header)
        o = old[(old["step_key"] == sk) & (old["response"] == resp)]
        nrow = new[(new["step_key"] == sk) & (new["response"] == resp)]
        cqa = (nrow.iloc[0]["cqa"] if not nrow.empty else o.iloc[0]["cqa"])
        unit = P.CFG.cqa(cqa)["unit"]
        if not o.empty:
            r = o.iloc[0]
            out.append(S.AcceptanceCriterionRecord(
                step=sk, attribute=cqa, low=None if r["low"] == 0 else float(r["low"]),
                high=None if not np.isfinite(r["high"]) else float(r["high"]), unit=unit,
                basis=str(r["rule"]), revision=P.REV1["rev"], status="superseded", source=q))
        if not nrow.empty:
            r = nrow.iloc[0]
            out.append(S.AcceptanceCriterionRecord(
                step=sk, attribute=cqa, low=None if r["iac_low"] == 0 else float(r["iac_low"]),
                high=None if not np.isfinite(r["iac_high"]) else float(r["iac_high"]), unit=unit,
                basis=str(r["basis"]), revision=P.REV2["rev"], status="in force", source=q))
    return out


# --------------------------------------------------------------------------- #
# The three tables every unit-operation pair anchors on.                       #
#                                                                              #
# Each rebuilds the table from the helper the .qmd renders, so a record can    #
# anchor on its own row instead of on the caption every row of the table       #
# shares. Pass the SAME key order and floatfmt the document uses: the row text #
# depends on both, and a mismatch is an ungrounded quote rather than a silent  #
# wrong answer (check_grounding is the gate).                                  #
# --------------------------------------------------------------------------- #
def param_rows(uo_key, classified, floatfmt=None):
    """Rendered ``@tbl-params`` rows, keyed by parameter name.

    The report table carries the final classification and the report's ranges; the plan
    table carries the ranges to be studied, so each document gets its own row text.
    """
    df = P.report_params(uo_key) if classified else P.plan_params(uo_key)
    return row_quotes(df, df["Parameter"], floatfmt)


def cqa_rows(keys, floatfmt=None, uo_key=None):
    """Rendered ``@tbl-cqa`` rows, keyed by attribute key.

    ``uo_key`` selects ``cqas_for`` (the attributes a step *sets*); ``keys`` selects
    ``cqas_by_keys`` (the attributes it governs, in the document's own order — which
    differs between a plan and its report, and changes the rendered rows).
    """
    df = P.cqas_for(uo_key) if uo_key else P.cqas_by_keys(keys)
    return row_quotes(df, keys, floatfmt)


def par_rows(uo_key, floatfmt=None):
    """Rendered ``@tbl-par`` rows, keyed by ``(CQA, parameter)`` — the PAR table's own key."""
    import doe_report as D
    df = D.par_table(uo_key)
    return row_quotes(df, list(zip(df["CQA"], df["Parameter"])), floatfmt)


def title_block_quote(doc_id):
    """The title-block rows that declare this document's identity.

    ``"Process Characterization Plan"`` alone appears in the title, the title-block table and
    the abbreviation list, so it cannot say *which* document is meant. The document ID and the
    declared class together are unique in every document of the corpus. They are two
    consecutive rows of the two-column title block, so the span crosses a row boundary — which
    reads as one more cell separator, since ``docx_text`` marks cells and not rows.
    """
    return CELL_SEP.join(["Document ID", doc_id, "Document class", P.DOC_REGISTRY[doc_id][0]])


# --------------------------------------------------------------------------- #
# Entity builders (shared shape; source references differ per document).       #
# --------------------------------------------------------------------------- #
def build_step(doc_id, file_name, sec, report):
    if report:
        src = ref(doc_id, file_name, sec, "Executive summary",
                  "The step forms the three glycan attributes, the charge variant distribution and the aggregate level of the harvested pool.")
    else:
        src = ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                  "The production bioreactor is a fed-batch culture of a recombinant CHO "
                  "cell line that secretes A-Mab into the medium")
    return S.ProcessStep(
        step_id="step:production_bioreactor", step_name=UO_NAME, step_number=str(STEP),
        unit_operation=UO_NAME,
        description="Fed-batch mammalian cell culture at 15,000 L working volume; the only step of "
                    "the drug substance process at which product-quality attributes are formed.",
        input_materials=["inoculum", "basal medium", "nutrient feed"],
        output_materials=["clarified culture (harvest feed)"],
        equipment=["15,000 L production bioreactor", "bench-scale stirred-tank scale-down model"],
        source_references=[src], metadata=meta(),
    )


def build_equipment(doc_id, file_name, sec, report):
    # Neither document names a 2 L vessel any more; both describe a bench-scale
    # stirred-tank model of the commercial vessel, so the entity follows the text.
    sdm = S.Equipment(
        equipment_id="equip:sdm_bench", equipment_name="bench-scale stirred-tank scale-down model",
        equipment_type="bioreactor (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Scale-down model and its qualification",
                               "The studies were executed on bench scale stirred tank bioreactors qualified as a model of the commercial vessel under SOP-1001." if report
                               else "The studies will be executed in bench-scale stirred tank "
                                    "bioreactors of the same design class as the commercial "
                                    "production vessel")],
        metadata=meta())
    vessel = S.Equipment(
        equipment_id="equip:production_bioreactor",
        equipment_name="15,000 L production bioreactor", equipment_type="bioreactor",
        site_name=P.RECEIVING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Product and unit operation" if report
                               else "Purpose and scope",
                               "The culture is inoculated from the N-1 seed bioreactor, fed with a single nutrient feed during the run and harvested after about 17 days." if report
                               else f"operated at conditions equivalent to the {SCALE_L} L "
                                    f"commercial production vessel")],
        metadata=meta())
    return [vessel, sdm]


def build_sites(doc_id, file_name, sec):
    return [
        S.ManufacturingSite(site_id="site:cambridge", site_name=P.SENDING_SITE, site_role="sending",
                            location="Cambridge, MA",
                            source_references=[ref(doc_id, file_name, sec, "Title block",
                                                   "Cambridge, MA (Development)")],
                            metadata=meta()),
        S.ManufacturingSite(site_id="site:grafton", site_name=P.RECEIVING_SITE, site_role="receiving",
                            location="Grafton, WI",
                            source_references=[ref(doc_id, file_name, sec, "Title block",
                                                   "Grafton, WI (Commercial DS)")],
                            metadata=meta()),
    ]


def build_params(doc_id, file_name, sec, classified):
    caption = ("Process parameters of the production bioreactor, with set-points, ranges, final "
               "classification and supporting study type."
               if classified else
               "Process parameters in scope, with set-points, ranges to be studied, normal "
               "operating ranges and the type of study each will receive.")
    # Each parameter anchors on its own row of that table, not on the shared caption.
    rows = param_row_quotes(classified)
    out = []
    for r in PARAM_ROWS:
        name = r["parameter"]
        ptype = r["classification"] if classified else "unclassified"
        rat = None
        if classified:
            if r["classification"] == "WC-CPP":
                rat = "Significantly affects the glycan/charge-variant CQAs but reliably controlled within the design space."
            elif r["classification"] == "KPP":
                rat = "Affects process performance/consistency without a significant CQA impact."
            elif r["classification"] == "GPP":
                rat = "No meaningful CQA or performance impact over a wide range."
        out.append(S.ProcessParameter(
            parameter_id=PARAM_CONCEPT[name], parameter_name=name, parameter_type=ptype,
            unit=r["unit"], target_value=f"{r['setpoint']:g}",
            NOR=f"{r['nor_low']:g}–{r['nor_high']:g} {r['unit']}",
            PAR=f"{r['par_low']:g}–{r['par_high']:g} {r['unit']}",
            associated_step=STEP_LABEL, rationale_for_criticality=rat,
            source_references=[ref(doc_id, file_name, sec,
                                   "Factors, ranges and the knowledge space" if classified
                                   else "Factors, ranges and study type",
                                   rows[name], table_title=caption,
                                   table_id=f"{doc_id}_tab_params",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


def param_row_quotes(classified):
    """Rendered ``@tbl-params`` rows of the bioreactor pair, keyed by parameter name.

    The report table carries the final classification and the report's ranges; the plan table
    carries the ranges to be studied. Each document therefore gets its own row text.
    """
    df = P.report_params(UO) if classified else P.plan_params(UO)
    return row_quotes(df, df["Parameter"])


def cqa_row_quotes(report):
    """Rendered ``@tbl-cqa`` rows of the bioreactor pair, keyed by attribute key.

    The report renders the same table with ``floatfmt=".0f"``, so the Tool #1 score prints
    without a decimal and the two documents need different row text.
    """
    df = P.cqas_for(UO)
    keys = P.cqa_reg[P.cqa_reg.set_by == UO]["key"]
    return row_quotes(df, keys, ".0f" if report else None)


def build_cqas(doc_id, file_name, sec, report):
    sec_title = "Quality attributes in scope"
    if report:
        table_title = "Quality attributes set or generated at the production bioreactor."
    else:
        table_title = ("Quality attributes formed at the production bioreactor, with drug "
                       "substance acceptance criteria and criticality.")
    rows = cqa_row_quotes(report)
    out = []
    for r in CQA_ROWS:
        key = r["key"]
        out.append(S.QualityAttribute(
            attribute_id=CQA_CONCEPT[key], attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"],
            acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            # The attribute -> method linkage is anchored in the plan (Analytical methods).
            analytical_method=None if report else CQA_METHOD[key], associated_steps=[STEP_LABEL],
            rationale_for_criticality=f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = {r['tool1_score']}.",
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref(doc_id, file_name, sec, sec_title, rows[key],
                                   table_title=table_title, table_id=f"{doc_id}_tab_cqa",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


# Per-method grounded fragment from the plan's "Analytical methods" section.
METHOD_QUOTE = {
    "AMV-3010": ("The released N-glycan map by 2-AB HILIC-UPLC measures afucosylation, "
                 "galactosylation and high mannose from a single preparation"),
    "AMV-3011": "Size exclusion chromatography measures the high molecular weight aggregate.",
    "AMV-3012": "The host cell protein ELISA",
    "AMV-3013": "Imaged capillary isoelectric focusing measures the acidic charge variants.",
    "AMV-3014": "The host cell protein ELISA and the residual DNA qPCR",
}
# CQA key -> the fragment used for that attribute's attribute -> method assertion.
#
# One sentence states three of these relations, so quoting it whole made one span the anchor
# for four records at once. Each glycan attribute instead takes the slice of that sentence
# ending at its OWN analyte name, so the span names the method and that attribute and stops —
# which is what a human annotator marks, and what makes the span usable on its own. The method
# entity keeps the whole sentence, since it is the record the whole sentence is about.
CQA_METHOD_QUOTE = {k: METHOD_QUOTE[m] for k, m in CQA_METHOD.items()}
_GLYCAN_CLAUSE = "The released N-glycan map by 2-AB HILIC-UPLC measures "
CQA_METHOD_QUOTE.update({
    "afucosylation": _GLYCAN_CLAUSE + "afucosylation",
    "galactosylation": _GLYCAN_CLAUSE + "afucosylation, galactosylation",
    "high_mannose": _GLYCAN_CLAUSE + "afucosylation, galactosylation and high mannose",
})

# Per-parameter classification sentence from the report's "Parameter classification"
# section. Each span opens on the parameter it classifies and carries the class and the
# reason, so it names both ends of the relation it anchors.
CLASS_QUOTE = {
    "Culture pH": ("Culture pH is a well controlled critical process parameter."),
    "Culture temperature": ("Culture temperature is a well controlled critical process parameter."),
    "Dissolved CO2 (pCO2)": ("A rise in dissolved carbon dioxide lowers the acidic charge variant fraction, by the largest single coefficient measured in this study, and it lowers galactosylation."),
    "Osmolality": ("A rise in osmolality lowers galactosylation and the acidic charge variant fraction, both significantly in screening, and it was held at its set-point in the response-surface stage"),
    "Culture duration": ("A longer culture lowers galactosylation and afucosylation, by the largest main effects in the study, raises aggregate, and raises the host cell protein and DNA load carried into harvest."),
    "Dissolved oxygen": ("Dissolved oxygen is a key process parameter."),
    "Initial viable cell conc.": ("A higher inoculation density brings the culture to its peak viable cell concentration sooner, which raises the integral of viable cell concentration over the run and with it the titer."),
    "Nutrient feed-1 volume": ("It replenishes glucose, amino acids and glycosylation precursors, and within the range assessed the culture is fed to excess, so the parameter raises the titer rather than the glycan fractions."),
    "Basal medium concentration": ("Basal medium concentration is a general process parameter."),
}


SDM = "bench-scale stirred-tank scale-down model"


def build_methods(doc_id, file_name, sec):
    out = []
    for mid, mname, mtype, analytes, attrs in METHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[CQA_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods",
                                   METHOD_QUOTE[mid])],
            metadata=meta()))
    return out


def build_studies(doc_id, file_name, report):
    sec = "Study execution" if report else "Study design"
    n_scr, n_rsm = P.doe_runs(UO, "screening"), P.doe_runs(UO, "rsm")
    studies = [
        S.StudyDesign(
            study_id="study:br_screening", study_type="screening_doe",
            design_name="resolution-V two-level fractional factorial", unit_operation=UO_NAME,
            factors=["Culture pH", "Culture temperature", "Dissolved CO2 (pCO2)",
                     "Osmolality", "Culture duration"],
            responses=["afucosylation", "galactosylation", "high_mannose",
                       "acidic_variants", "aggregates_hmw"],
            n_runs=n_scr, n_center_points=P.doe_centre_points(UO, "screening"), scale_down_model=SDM,
            associated_parameters=[PARAM_CONCEPT[f] for f in
                                   ["Culture pH", "Culture temperature", "Dissolved CO2 (pCO2)",
                                    "Osmolality", "Culture duration"]],
            source_references=[ref(doc_id, file_name, sec, "Screening design",
                                   "A 19-run screening design identified the active factors and their interactions" if report
                                   else "The screening design is a 16 run half fraction of the "
                                        "full 32 run two level factorial in the 5 multivariate "
                                        "parameters")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:br_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=UO_NAME,
            factors=["Culture pH", "Culture temperature", "Culture duration", "Dissolved CO2 (pCO2)"],
            responses=["afucosylation", "galactosylation", "high_mannose",
                       "acidic_variants", "aggregates_hmw"],
            n_runs=n_rsm, n_center_points=P.doe_centre_points(UO, "rsm"), scale_down_model=SDM,
            associated_parameters=[PARAM_CONCEPT[f] for f in
                                   ["Culture pH", "Culture temperature", "Culture duration",
                                    "Dissolved CO2 (pCO2)"]],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "The axial runs sit on the faces of the cube rather than outside it, so no run was executed at a setting beyond the characterization ranges in Table 5 ." if report
                                   else "The response surface design is a face centred central "
                                        "composite design in 4 of the 5 multivariate "
                                        "parameters")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:br_sdm_qual", study_type="scale_down_qualification", unit_operation=UO_NAME,
            scale_down_model=SDM,
            source_references=[ref(doc_id, file_name, sec,
                                   "Scale-down model and its qualification",
                                   "Confidence in the scale-down model rests on its qualification against commercial-scale data at the set-point and on the reproducibility of its centre points" if report
                                   else "The comparison covers the viable cell density "
                                        "profile, viability at harvest, titer and the")],
            metadata=meta()),
        # Both documents carry the univariate assessment of initial viable cell concentration.
        S.StudyDesign(
            study_id="study:br_univariate", study_type="univariate", unit_operation=UO_NAME,
            factors=["Initial viable cell conc."], responses=["process performance"],
            associated_parameters=["param:initial_vcc"],
            source_references=[ref(doc_id, file_name, sec, "Univariate assessment",
                                   "The univariate assessment supports the classification of these four parameters in §9 and their ranges in Table 5 ." if report
                                   else "4 parameters will be assessed one at a time.")],
            metadata=meta()),
    ]
    return studies


# --------------------------------------------------------------------------- #
# Assertions (relations) + rationales.                                         #
# --------------------------------------------------------------------------- #
def build_assertions(doc_id, file_name, report):
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote, header=None):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote,
                                   table_header=header)],
            metadata=meta()))

    # step -> parameters and step -> quality attributes (both docs). Each assertion anchors on
    # the table row naming the parameter or the attribute, so the span carries both ends of the
    # relation rather than a caption shared by every row.
    prow = param_row_quotes(report)
    crow = cqa_row_quotes(report)
    for name, cid in PARAM_CONCEPT.items():
        add("step:production_bioreactor", "step_has_parameter", cid,
            f"{UO_NAME} has process parameter {name}.",
            "Factors, ranges and the knowledge space" if report else "Factors, ranges and study type",
            prow[name], prow.header)
    for r in CQA_ROWS:
        add("step:production_bioreactor", "step_has_quality_attribute", CQA_CONCEPT[r["key"]],
            f"{UO_NAME} sets/controls {r['cqa']}.", "Quality attributes in scope",
            crow[r["key"]], crow.header)
    # attribute -> method (anchored in the plan, which names the method per attribute)
    if not report:
        for r in CQA_ROWS:
            add(CQA_CONCEPT[r["key"]], "attribute_measured_by_method", f"method:{CQA_METHOD[r['key']]}",
                f"{r['cqa']} is measured by {CQA_METHOD[r['key']]}.", "Analytical methods",
                CQA_METHOD_QUOTE[r["key"]])
    # attribute -> acceptance criterion (both docs state acceptance criteria). The row carries
    # the criterion next to the attribute it belongs to, which a sentence about the table
    # cannot do.
    for r in CQA_ROWS:
        add(CQA_CONCEPT[r["key"]], "attribute_has_acceptance_criterion",
            f"lit:{r['key']}_acc", f"{r['cqa']} acceptance: {r['acc_low']:g}–{r['acc_high']:g} {r['unit']}.",
            "Quality attributes in scope", crow[r["key"]], crow.header)
    # results only in the report: parameter impacts / non-impacts. Each classification
    # sentence of §9 is quoted against the parameter it classifies.
    if report:
        for k in ["Culture pH", "Culture temperature", "Dissolved CO2 (pCO2)",
                  "Osmolality", "Culture duration"]:
            add(PARAM_CONCEPT[k], "parameter_impacts_attribute", "attr:afucosylation",
                "Parameter significantly affects the glycan/charge-variant CQAs (WC-CPP).",
                "Parameter classification", CLASS_QUOTE[k])
        for k in ["Dissolved oxygen", "Initial viable cell conc.", "Nutrient feed-1 volume"]:
            add(PARAM_CONCEPT[k], "parameter_does_not_significantly_impact_attribute",
                "attr:afucosylation",
                "Parameter affects performance without a significant CQA impact (KPP).",
                "Parameter classification", CLASS_QUOTE[k])
        add("param:medium_concentration", "parameter_does_not_significantly_impact_attribute",
            "attr:afucosylation", "No meaningful impact over a wide range (GPP).",
            "Parameter classification", CLASS_QUOTE["Basal medium concentration"])

    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


# --------------------------------------------------------------------------- #
# Concepts (entity-linking canonical targets).                                 #
# --------------------------------------------------------------------------- #
def build_concepts():
    from annex_contract.concepts import Concept, ConceptStore
    cs = [Concept(concept_id="step:production_bioreactor", concept_type="PROCESS_STEP",
                  canonical_name=UO_NAME, aliases=["production bioreactor", "Step 3", "fed-batch culture"],
                  review_status="human_verified")]
    for name, cid in PARAM_CONCEPT.items():
        cs.append(Concept(concept_id=cid, concept_type="PROCESS_PARAMETER", canonical_name=name,
                          review_status="human_verified"))
    for r in CQA_ROWS:
        cs.append(Concept(concept_id=CQA_CONCEPT[r["key"]], concept_type="QUALITY_ATTRIBUTE",
                          canonical_name=r["cqa"], aliases=[r["key"]], review_status="human_verified"))
    for mid, mname, *_ in METHODS:
        cs.append(Concept(concept_id=f"method:{mid}", concept_type="ANALYTICAL_METHOD",
                          canonical_name=mname, aliases=[mid], review_status="human_verified"))
    return ConceptStore(run_id="gt-bioreactor", concepts=cs)


# --------------------------------------------------------------------------- #
# Report-section (extractive summary) targets.                                 #
# --------------------------------------------------------------------------- #
def build_report_sections(doc_id, file_name, report):
    from annex_contract.summaries import ReportSection, ReportStatement
    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-003 defines the Stage 1 characterization of the A-Mab production bioreactor (Step 3).",
               "Purpose and scope",
               "This plan defines the studies that will characterize the step"),
            st(2, "Nine process parameters are in scope, five studied multivariately and four univariately.",
               "Risk-based prioritization of parameters",
               "5 parameters were assigned to the multivariate design and 4 to univariate assessment"),
            st(3, "The study uses a screening fractional-factorial design followed by a "
                  "face-centred central composite design on a qualified bench-scale scale-down model.",
               "Response-surface design",
               "The response surface design is a face centred central composite design in 4 "
               "of the 5 multivariate parameters"),
            st(4, "A response-surface model is adequate for prediction when the lack-of-fit test "
                  "does not reject against the centre-point pure error, when the predicted "
                  "coefficient of determination tracks the adjusted one, and when the residual "
                  "diagnostics show no structure.",
               "Acceptance and decision criteria",
               "the lack of fit test of \u00a75.5 does not reject at p < 0.05 against the pure "
               "error from the centre points"),
            st(5, "The study must establish an operating region over the well controlled "
                  "parameters within which every modelled attribute is predicted to meet its "
                  "acceptance criterion.",
               "Acceptance and decision criteria",
               "An operating region will be declared over the well controlled parameters where "
               "the response surface models predict that every modelled attribute"),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Culture pH, temperature, dissolved CO2, osmolality and culture duration are classified WC-CPP.",
           "Executive summary",
           "Of the 9 parameters, 5 were classified as well controlled critical process parameters, 3 as key process parameters and 1 as a general process parameter."),
        # The re-authored report states the response set here instead of the peak viable cell
        # density and titre the previous revision gave, so the statement follows the document.
        st(2, "The five attributes measured as responses of the designed experiments are "
              "afucosylation, galactosylation, high mannose, acidic charge variants and aggregate.",
           "Product and unit operation",
           "The step forms the three glycan attributes, the charge variant distribution and the aggregate level of the harvested pool."),
        st(3, "Within the design space the fitted response-surface models predict every measured "
              "attribute inside its in-process limit.",
           "Design space",
           "The design space is the region of the four modelled parameters over which every attribute governed here meets its in-process criterion."),
        st(4, "The response-surface models describe the characterized region adequately and every "
              "overall F test reaches significance.",
           "Response-surface models",
           "The response-surface models account for between 91 and 97 % of the variance in the five responses."),
        st(5, "There was no significant lack of fit relative to the center-point pure error.",
           "Response-surface models",
           "No response shows significant lack of fit against the centre-point pure error."),
        st(6, "All bioreactor-set CQAs meet acceptance with margin at commercial scale.",
           "Conclusions",
           "All 7 quality attributes set at this step meet their drug substance acceptance criteria at commercial scale in a simulation of 2,000 batches."),
    ])]


def build_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:bioreactor", unit_operation=UO_NAME,
        parameters=["param:culture_ph", "param:culture_temperature",
                    "param:culture_duration", "param:dissolved_co2"],
        quality_attributes_constrained=[CQA_CONCEPT[r["key"]] for r in CQA_ROWS],
        definition="The part of the characterized region in culture pH, culture temperature, "
                   "culture duration and dissolved CO2 within which the fitted response-surface "
                   "models predict every measured attribute inside its in-process limit. It is "
                   "smaller than the characterized region, and galactosylation is the attribute "
                   "that excludes most of it.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "The design space of this step is the multivariate region of culture pH, culture temperature, culture duration and dissolved carbon dioxide")],
        metadata=meta())]


# --------------------------------------------------------------------------- #
# Report-only discourse / PAR layers (PCR-003).                                #
# --------------------------------------------------------------------------- #
# These three layers annotate the REPORT (PCR-003) only; the plan (PCP-003)     #
# does not carry them. proven_acceptable_ranges is derived from the same DoE     #
# engine that renders @tbl-par; weak_claims and rhetorical_spans are read from   #
# the authoring/ annotation files, whose quotes are verbatim report prose.       #
# --------------------------------------------------------------------------- #
PAR_SEC = "Proven acceptable ranges"
# Per-CQA grounded fragment from the report's Proven-acceptable-ranges section.
PAR_CQA_QUOTE = {
    "Afucosylation": "Proven acceptable range for afucosylation against its governing parameter.",
    "Galactosylation": "Proven acceptable range for galactosylation against its governing parameter.",
    "High mannose": "Proven acceptable range for high mannose against its governing parameter.",
    "Acidic variants": "Proven acceptable range for acidic charge variants against its governing parameter.",
    "Aggregates (HMW)": "Proven acceptable range for aggregate against its governing parameter.",
}
_PAR_GENERAL_QUOTE = ("The acceptance criteria are the in-process limits for this step and not "
                      "the drug substance specifications")


def build_proven_acceptable_ranges(doc_id, file_name):
    """One ProvenAcceptableRange per governed CQA x response-surface parameter, from the
    same DoE engine (``doe_report.par_table``) that renders @tbl-par in the report."""
    import doe_report as D
    par = D.par_table(UO)
    # Each combination anchors on its own row of @tbl-par. The per-attribute prose used
    # before said which attribute was governed but not which parameter's range was proven,
    # so one span stood in for every parameter of that attribute.
    rows = par_rows(UO)
    out = []
    for i, r in enumerate(par.to_dict("records"), 1):
        cqa, param, unit = r["CQA"], r["Parameter"], (r["Unit"] or "")
        char = f"{r['Char. range']} {unit}".strip()
        out.append(S.ProvenAcceptableRange(
            par_id=f"{doc_id}-PAR{i:02d}", unit_operation=UO_NAME,
            quality_attribute=cqa, parameter=param,
            characterization_range=char,
            par_at_setpoint=f"{r['PAR (set-point)']} {unit}".strip(),
            par_nor_propagated=f"{r['PAR (NOR)']} {unit}".strip(),
            acceptance_basis=par_basis_text(UO, cqa),
            source_references=[ref(doc_id, file_name, f"{doc_id}_sec_par", PAR_SEC,
                                   rows[(cqa, param)], table_id=f"{doc_id}_tab_par",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


def _document_text(file_name):
    """Text of the RENDERED document in ``check_grounding``'s comparison form.

    Must be the ``.docx``, not the ``.qmd``: ``check_grounding.py`` is the authority and it
    reads the rendered file. A quote carrying a number exists only in the rendered text (the
    source has a ``{python}`` inline expression there), so matching against the ``.qmd``
    would silently drop exactly the quotes that ground perfectly well. Falls back to the
    source only when nothing has been rendered yet, and says so.

    Compare candidate quotes with :func:`_present`, never with a bare ``in``: this text is
    normalised (whitespace collapsed, script digits folded) and a raw quote is not, so a
    span carrying "log₁₀" tests absent against a document that plainly contains it. That
    mismatch cost a build — the curated PCR-003 rhetorical layer failed wholesale.
    """
    docx = os.path.join(HERE, file_name)
    if os.path.exists(docx):
        from check_grounding import docx_text
        return docx_text(docx)
    qmd = os.path.join(HERE, os.path.splitext(file_name)[0] + ".qmd")
    if os.path.exists(qmd):
        from check_grounding import normalize
        print(f"note  {file_name} not rendered yet; presence checks fall back to the .qmd, "
              f"which will under-count any quote containing a rendered number.")
        return normalize(open(qmd, encoding="utf-8").read())
    return ""


def _present(quote, text):
    """Is ``quote`` in ``text``, under the same normalisation ``check_grounding`` applies?"""
    from check_grounding import normalize
    return normalize(quote) in text


def build_weak_claims(doc_id, file_name):
    """Labeled unsupported/overstated claims from ``authoring/weak_claims.yaml``.

    **Currently emits nothing: the planted weak-claim feature is retired** and no document
    contains a registered claim. See ``authoring/WEAK_CLAIMS.md``. The short version is that
    the claims were injected AFTER authoring, so against a finished document they read as
    contradictions of the neighbouring prose rather than as claims that merely lack support
    — which changes the benchmark task and passes every gate undetected.

    A registered claim whose quote is not in the current ``.qmd`` is therefore skipped with
    an informational note rather than emitted, so "no planted claims" is a clean, buildable
    state instead of a guaranteed ``check_grounding`` failure. The function is kept so the
    layer can be revived without rework — but only by naming the claims in the authoring
    brief and having the single author write them into the argument in one pass.
    """
    import yaml
    path = os.path.join(HERE, "..", "authoring", "weak_claims.yaml")
    with open(path) as fh:
        data = yaml.safe_load(fh)
    prose = _document_text(file_name)
    sec_title = {"results": "Results", "exec_summary": "Executive summary"}
    out, skipped = [], []
    for c in data.get("claims", {}).get(doc_id, []):
        sec = c.get("section")
        quote = " ".join(c["quote"].split())
        if prose and not _present(quote, prose):
            skipped.append(c["id"])
            continue
        out.append(S.WeakClaim(
            claim_id=c["id"], section=sec, weakness_type=c["weakness_type"],
            source_reference=ref(doc_id, file_name, f"{doc_id}_sec_{sec}",
                                 sec_title.get(sec, "Results"), quote),
            rationale=" ".join(c["rationale"].split()),
            correct_version=" ".join(c["correct_version"].split()),
            metadata=meta(basis="explicit", conf="high")))
    if skipped:
        print(f"note  {doc_id}: {len(skipped)} registered weak claim(s) are not in "
              f"{file_name} and so are not in the annex "
              f"({', '.join(skipped)}). This is EXPECTED: the planted weak-claim feature is "
              f"retired (see authoring/WEAK_CLAIMS.md). No action needed.")
    return out


def build_rhetorical_spans(doc_id, file_name):
    """Rhetorical / argument-structure spans over the report, from
    ``authoring/rhetorical/<doc_id>.spans.yaml``. Each quote is verbatim report prose.

    The spans are curated against a specific revision of the document, so re-authoring it
    invalidates them wholesale. A span whose quote no longer appears is skipped with a
    warning; the layer must then be re-curated against the new text. Skipping keeps the
    rest of the annex buildable instead of failing every span at once.
    """
    import yaml
    path = os.path.join(HERE, "..", "authoring", "rhetorical", f"{doc_id}.spans.yaml")
    if not os.path.exists(path):
        return []
    with open(path) as fh:
        data = yaml.safe_load(fh)
    # One section id for the whole layer, when the file asks for one. The eight documents
    # converted from Python builders in 2026-08 all bucketed their spans under a flat
    # ``<DOC>_sec_rhet``; the key keeps that so the conversion moved no byte of any annex.
    # Without it the id is per section, which is what PCR-003 uses.
    flat_sec_id = data.get("section_id")
    prose = _document_text(file_name)
    out, skipped = [], 0
    for s in data.get("spans", []):
        sec = s.get("section")
        quote = " ".join(s["quote"].split())
        if prose and not _present(quote, prose):
            skipped += 1
            continue
        out.append(S.RhetoricalSpan(
            span_id=s["id"], section=sec, role=s["role"],
            source_reference=ref(doc_id, file_name, flat_sec_id or f"{doc_id}_sec_{sec}",
                                 sec or "body", quote),
            supported_by=s.get("supported_by") or [],
            restates=s.get("restates"), bounds=s.get("bounds")))
    if skipped:
        # Hard failure, not a warning. A curated span layer that no longer matches its
        # document degrades SILENTLY: the build still succeeds, check_grounding still
        # reports 0 ungrounded (a dropped span contributes no quote to check), and the
        # annex simply ships thinner than intended. PCR-003 shipped with an entirely
        # empty rhetorical layer that way. If a spans file exists it must match the
        # current text, so make the mismatch stop the build.
        raise SystemExit(
            f"FAIL  {doc_id}: {skipped} of {len(data.get('spans', []))} rhetorical span(s) "
            f"do not appear in {file_name}.\n"
            f"      The document has been re-authored or re-rendered since the layer was "
            f"curated.\n"
            f"      Re-curate authoring/rhetorical/{doc_id}.spans.yaml against the current "
            f"rendered text, or delete it to drop the layer deliberately.")
    return out


# --------------------------------------------------------------------------- #
# Assemble the two annexes.                                                     #
# --------------------------------------------------------------------------- #
COMMON_EXT = [
    "ProcessParameter.parameter_type widened with WC-CPP, GPP",
    "DocumentInventoryItem.predicted_document_type: process_characterization_plan / _report added",
    "QualityAttribute.criticality_level / tool1_score / tool2_severity added",
    "StudyDesign (new model)", "DesignSpace (new model)",
]


def inventory(doc_id, file_name, dtype):
    return S.DocumentInventoryItem(
        document_id=doc_id, file_name=file_name, predicted_document_type=dtype,
        product_name_candidates=["A-Mab"], process_name_candidates=[UO_NAME],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "production bioreactor", "design of experiments",
                     "critical quality attributes", "design space", "parameter classification"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc_id][0]}'.",
        source_references=[ref(doc_id, file_name, "Title block", "Title block",
                               title_block_quote(doc_id))],
        metadata=meta())


def build_plan():
    doc, f = "PCP-003", PCP_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_uo",
                                  process_steps=[build_step(doc, f, f"{doc}_sec_uo", report=False)],
                                  equipment=build_equipment(doc, f, f"{doc}_sec_uo", report=False),
                                  sites=build_sites(doc, f, f"{doc}_sec_uo")),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=build_cqas(doc, f, f"{doc}_sec_cqa", report=False)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=build_params(doc, f, f"{doc}_sec_param", classified=False)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_study",
                                  analytical_methods=build_methods(doc, f, f"{doc}_sec_study")),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Parameter study-type (multivariate/univariate) has no ProcessParameter field; captured via StudyDesign.factors.",
            "The Plan states classification is an OUTPUT; parameter_type left 'unclassified' here.",
        ],
        inventory=inventory(doc, f, "process_characterization_plan"),
        entities=entities,
        studies=build_studies(doc, f, report=False),
        report_sections=build_report_sections(doc, f, report=False),
        assertions=build_assertions(doc, f, report=False), concepts=build_concepts())


def build_report():
    doc, f = "PCR-003", PCR_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_exec",
                                  process_steps=[build_step(doc, f, f"{doc}_sec_exec", report=True)],
                                  equipment=build_equipment(doc, f, f"{doc}_sec_exec", report=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=build_params(doc, f, f"{doc}_sec_param", classified=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=build_cqas(doc, f, f"{doc}_sec_cqa", report=True)),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT + [
            "ProvenAcceptableRange (new model) — per-CQA x parameter PAR (at-set-point / NOR-propagated)",
            "WeakClaim (new model) — LABELED unsupported/overstated claims (benchmark negatives)",
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "Process-capability (Cpk) values have no dedicated field; reported as report_sections statements.",
            "proven_acceptable_ranges mirror @tbl-par (doe_report.par_table); weak_claims and "
            "rhetorical_spans are sourced from authoring/ annotation files with verbatim report quotes.",
        ],
        inventory=inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=build_studies(doc, f, report=True),
        design_spaces=build_design_spaces(doc, f),
        proven_acceptable_ranges=build_proven_acceptable_ranges(doc, f),
        report_sections=build_report_sections(doc, f, report=True),
        assertions=build_assertions(doc, f, report=True), concepts=build_concepts(),
        weak_claims=build_weak_claims(doc, f),
        rhetorical_spans=build_rhetorical_spans(doc, f))


# =========================================================================== #
# Harvest and Clarification (Step 4) — PCP-004 / PCR-004.                       #
# --------------------------------------------------------------------------- #
# Additive, self-contained builders for the non-DoE harvest pair. They reuse   #
# only the unit-operation-agnostic helpers (meta, ref, COMMON_EXT) and never   #
# touch the bioreactor globals above, so the bioreactor annexes are unchanged. #
# Harvest forms no product-quality CQA, so there are no QualityAttribute        #
# entities and no design space; the operation is characterized univariately.   #
# =========================================================================== #
HUO = "harvest"
HUO_NAME = P.CFG.unit_op(HUO).name              # "Harvest / Clarification" (matches the CSV)
HSTEP = P.CFG.unit_op(HUO).step                 # 4
HSTEP_LABEL = f"Harvest and Clarification (Step {HSTEP})"

PCP4_FILE = "PCP-004_harvest.docx"
PCR4_FILE = "PCR-004_harvest.docx"

HPARAM_ROWS = P.param_reg[P.param_reg.unit_operation == HUO_NAME].to_dict("records")
HPARAM_CONCEPT = {
    "Centrifugation (rcf)": "param:centrifuge_rcf",
    "Depth filter load": "param:depth_filter_load",
    "Post-clarification turbidity": "param:post_clarification_turbidity",
}
# Attributes harvest monitors (it sets/clears none of them): the feed-clarity
# measure it controls plus the upstream-formed impurity load it carries forward.
HATTR_CONCEPT = {
    "turbidity": "attr:post_clarification_turbidity",
    "hcp": "attr:hcp",
    "residual_dna": "attr:residual_dna",
    "aggregates_hmw": "attr:aggregates_hmw",
}
HATTR_NAME = {
    "turbidity": "Post-clarification turbidity",
    "hcp": "Host Cell Protein (HCP) load",
    "residual_dna": "Residual DNA load",
    "aggregates_hmw": "Aggregates (HMW)",
}
HMETHODS = [
    ("AMV-3015", "Turbidity by Nephelometry (NTU)", "nephelometry",
     ["post-clarification turbidity"], ["turbidity"]),
    ("AMV-3012", "Host-Cell Protein ELISA", "immunoassay", ["host-cell protein"], ["hcp"]),
    ("AMV-3014", "Residual DNA (qPCR)", "qPCR", ["residual host-cell DNA"], ["residual_dna"]),
    ("AMV-3011", "Size-Variants (SEC-HPLC)", "chromatography",
     ["aggregate", "monomer"], ["aggregates_hmw"]),
]
# Both documents call the model "a scale-down model of the commercial harvest train"
# (PCP-004 §1) / "a scale-down model of the harvest and clarification step" (PCR-004 §3.1).
HSDM = "scale-down model of the commercial harvest train"

# --------------------------------------------------------------------------- #
# Per-document grounded fragments. Each is a verbatim span of the RENDERED      #
# document (see check_grounding.py), chosen number-free wherever the number is  #
# not the point, so a reseed cannot break the grounding.                        #
# --------------------------------------------------------------------------- #
# Analytical methods: one fragment per method, from each document's
# "Analytical methods" section, which names the method against its analyte.
HMETHOD_QUOTE = {
    "PCP-004": {
        "AMV-3015": "Turbidity by nephelometry (AMV-3015) measures the fine particulate and colloidal material the filters pass",
        "AMV-3012": "Host cell protein by ELISA (AMV-3012) measures the impurity burden of the clarified harvest",
        "AMV-3014": "Residual DNA by qPCR (AMV-3014) measures the second product of lysis",
        "AMV-3011": "Size variants by SEC-HPLC (AMV-3011) measure the high molecular weight content of the antibody before and after the step.",
    },
    "PCR-004": {
        "AMV-3015": "Turbidity was measured by nephelometry under AMV-3015 on the centrifuge feed, the centrate and the clarified harvest",
        "AMV-3012": "Host cell protein was measured by ELISA under AMV-3012",
        "AMV-3014": "residual DNA by quantitative polymerase chain reaction under AMV-3014",
        "AMV-3011": "host cell protein, residual DNA or aggregate in the clarified harvest at any setting studied",
    },
}
# Attributes the step CARRIES FORWARD (it forms and clears none): one
# (section title, fragment) per attribute. The two documents place them differently.
HATTR_QUOTE = {
    "PCP-004": {
        "turbidity": ("Purpose and scope",
                      "it is the in-process measurement by which clarified harvest is released to capture"),
        "hcp": ("Quality attributes in scope",
                "Host cell protein is the response through which the lysis argument of §4.1 is tested, and it is the attribute that rises most when cells break during the operation."),
        "residual_dna": ("Quality attributes in scope",
                         "Host cell protein and residual DNA in the clarified harvest will be compared with the same measurements on the unclarified culture that produced it."),
        "aggregates_hmw": ("Quality attributes in scope",
                           "by unfolding the antibody at a shear or air-liquid interface, which raises high molecular weight content"),
    },
    "PCR-004": {
        "turbidity": ("Parameters, ranges and the knowledge space",
                      "delivers a clarified, filtered feed to Protein A capture"),
        "hcp": ("Quality attributes in scope",
                "Host Cell Protein (HCP) has the tightest capability at a process capability index of 6.14"),
        "residual_dna": ("Quality attributes in scope",
                         "Host cell protein and DNA clearance is credited to Protein A capture, cation exchange and anion exchange"),
        "aggregates_hmw": ("Quality attributes in scope",
                           "Aggregate can rise at harvest only if the antibody unfolds at the shear rate of the centrifuge feed zone or at an air-liquid interface created in a foaming transfer."),
    },
}
# "no product-quality impact": one (section title, fragment) per parameter. Step 4
# runs NO designed experiment, so the claim rests on the null result of the
# univariate assessment and on the absence of a mechanism, not on a fitted model.
HNOIMPACT_QUOTE = {
    "PCP-004": {
        "Centrifugation (rcf)": ("Risk-based prioritization of parameters",
                                 "No parameter of this step was ranked high enough to require a multivariate design."),
        "Depth filter load": ("Risk-based prioritization of parameters",
                              "No parameter of this step was ranked high enough to require a multivariate design."),
        "Post-clarification turbidity": ("Statistical methods",
                                         "No response-surface model will be fitted for this step and no Monte-Carlo propagation of a fitted model will be performed, because no multivariate design is run here."),
    },
    "PCR-004": {
        "Centrifugation (rcf)": ("Product quality across the step",
                                 "No quality attribute of A-Mab changed measurably across harvest and clarification at any condition studied."),
        "Depth filter load": ("Product quality across the step",
                              "In every case the difference between the two was within the precision of the method that measured it."),
        "Post-clarification turbidity": ("Parameter classification",
                                         "no quality attribute of A-Mab changes with it"),
    },
}
# Per-parameter classification rationale, paraphrasing PCR-004 §9 (report only).
HPARAM_RATIONALE = {
    "Centrifugation (rcf)": "Key process parameter: governs solids removal and therefore the load "
                            "presented to the depth filter; no effect on any quality attribute was "
                            "seen over the characterized range.",
    "Depth filter load": "Key process parameter: governs filter capacity and post-clarification "
                         "turbidity, and is readily controlled by fixing the filter area to the "
                         "batch volume.",
    "Post-clarification turbidity": "General process parameter: an outcome of the two settings "
                                    "above, with no demonstrated link to a quality attribute, "
                                    "monitored as the acceptance measure for the feed to capture.",
}


def h_step(doc_id, file_name, sec, report):
    if report:
        src = ref(doc_id, file_name, sec, "Executive summary",
                  "The step forms no quality attribute of the antibody")
    else:
        src = ref(doc_id, file_name, sec, "Purpose and scope",
                  "The step forms no quality attribute of the antibody.")
    return S.ProcessStep(
        step_id="step:harvest_clarification", step_name=HUO_NAME, step_number=str(HSTEP),
        unit_operation=HUO_NAME,
        description="Primary recovery: continuous disk-stack centrifugation followed by depth "
                    "and sterile filtration; clarifies the broth and defines the feed to "
                    "Protein A capture. Forms no product-quality attribute and is credited with "
                    "no impurity clearance; the HCP, DNA and aggregate burden it carries forward "
                    "is cleared downstream (PCR-005, PCR-007, PCR-008).",
        input_materials=["production-bioreactor harvest (whole broth)"],
        output_materials=["clarified harvest (Protein A capture feed)"],
        equipment=["continuous disk-stack centrifuge", "depth filter train", "sterile filter",
                   HSDM],
        source_references=[src], metadata=meta())


def h_equipment(doc_id, file_name, sec, report):
    if report:
        cent = ("Executive summary",
                "The culture fluid leaving the production bioreactor is fed continuously to a disk-stack centrifuge, which sediments cells and the larger cell debris under a centrifugal field.")
        dep = ("Executive summary",
               "That material is removed on a train of positively charged depth filters, and the clarified harvest is passed through a sterilising-grade filter into the capture step.")
        sdm_ref = ("Scale-down model and its qualification",
                   "The characterization was executed on a scale-down model of the commercial harvest operation, qualified under SOP-1001.")
    else:
        cent = ("Unit-operation description and prior knowledge",
                "At commercial scale the operation is a continuous disk-stack centrifugation followed by depth filtration and a sterilizing grade filter")
        dep = ("Unit-operation description and prior knowledge",
               "That material is removed on a depth filter train, whose media are positively charged and therefore adsorb DNA fragments and fine debris in addition to retaining particles by size.")
        sdm_ref = ("Purpose and scope",
                   "The characterization runs will be executed on a scale-down model of the harvest train, qualified under SOP-1001 before the first characterization run.")
    sdm = S.Equipment(
        equipment_id="equip:clarification_sdm", equipment_name=HSDM,
        equipment_type="clarification (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec, sdm_ref[0], sdm_ref[1])],
        metadata=meta())
    centrifuge = S.Equipment(
        equipment_id="equip:disk_stack_centrifuge", equipment_name="continuous disk-stack centrifuge",
        equipment_type="centrifuge", site_name=P.RECEIVING_SITE,
        source_references=[ref(doc_id, file_name, sec, cent[0], cent[1])],
        metadata=meta())
    depth = S.Equipment(
        equipment_id="equip:depth_filter", equipment_name="depth filter train",
        equipment_type="filter", site_name=P.RECEIVING_SITE,
        source_references=[ref(doc_id, file_name, sec, dep[0], dep[1])],
        metadata=meta())
    return [centrifuge, depth, sdm]


def h_sites(doc_id, file_name, sec):
    return [
        S.ManufacturingSite(site_id="site:cambridge", site_name=P.SENDING_SITE, site_role="sending",
                            location="Cambridge, MA",
                            source_references=[ref(doc_id, file_name, sec, "Title block",
                                                   "Cambridge, MA (Development)")],
                            metadata=meta()),
        S.ManufacturingSite(site_id="site:grafton", site_name=P.RECEIVING_SITE, site_role="receiving",
                            location="Grafton, WI",
                            source_references=[ref(doc_id, file_name, sec, "Title block",
                                                   "Grafton, WI (Commercial DS)")],
                            metadata=meta()),
    ]


def h_params(doc_id, file_name, sec, classified):
    # Verbatim caption of @tbl-params in each rendered document.
    caption = ("Parameters of the harvest and clarification step, with set-points, normal "
               "operating ranges, characterized ranges, final classification and study type."
               if classified else
               "Parameters to be studied, with set-points, characterization ranges, normal "
               "operating ranges and study type.")
    # PCP-004 renders this table with floatfmt=".0f" (the rcf column); PCR-004 takes the
    # automatic format. Each parameter anchors on its own row, not on the shared caption.
    rows = h_param_rows(classified)
    out = []
    for r in HPARAM_ROWS:
        name = r["parameter"]
        ptype = r["classification"] if classified else "unclassified"
        out.append(S.ProcessParameter(
            parameter_id=HPARAM_CONCEPT[name], parameter_name=name, parameter_type=ptype,
            unit=r["unit"], target_value=f"{r['setpoint']:g}",
            NOR=f"{r['nor_low']:g}–{r['nor_high']:g} {r['unit']}",
            PAR=f"{r['par_low']:g}–{r['par_high']:g} {r['unit']}",
            associated_step=HSTEP_LABEL,
            rationale_for_criticality=HPARAM_RATIONALE[name] if classified else None,
            source_references=[ref(doc_id, file_name, sec,
                                   "Parameters, ranges and the knowledge space" if classified
                                   else "Factors, ranges and study type",
                                   rows[name], table_title=caption,
                                   table_id=f"{doc_id}_tab_params",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


def h_param_rows(classified):
    """Rendered ``@tbl-params`` rows of the harvest pair, keyed by parameter name.

    Both documents of the pair now render the set-point with a thousands separator, so neither
    needs the ``.0f`` override the earlier PCP-004 table did (re-anchored 2026-08-20, TASK-025).
    """
    return param_rows(HUO, classified, floatfmt=None)


def h_methods(doc_id, file_name, sec, report):
    quotes = HMETHOD_QUOTE[doc_id]
    out = []
    for mid, mname, mtype, analytes, attrs in HMETHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[HATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods", quotes[mid])],
            metadata=meta()))
    return out


def h_studies(doc_id, file_name, report):
    # Step 4 runs NO designed experiment: only a one-factor-at-a-time ranging of the two
    # settable parameters (turbidity is an outcome, not a factor) plus the SDM qualification.
    uni = ("Univariate assessment",
           "Design space No design space is defined for harvest and clarification, and none is claimed." if report
           else "They are the lower edge of the range studied, the lower limit of the normal operating range, the set-point, the upper limit of the normal operating range and the upper edge of the range studied")
    qual = ("Scale-down model and its qualification",
            "The qualification compared the model against commercial-scale data from the A-Mab engineering campaign on centrate turbidity, clarified harvest turbidity, product recovery and the host cell protein and DNA content of the clarified harvest." if report
            else "Qualification will compare the model with the commercial train at the set-point condition on the same culture.")
    return [
        S.StudyDesign(
            study_id="study:hv_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=HUO_NAME,
            factors=["Centrifugation (rcf)", "Depth filter load"],
            responses=["product recovery (step yield)", "post-clarification turbidity",
                       "depth-filter differential pressure"],
            scale_down_model=HSDM,
            associated_parameters=list(HPARAM_CONCEPT.values()),
            source_references=[ref(doc_id, file_name, "Study design", uni[0], uni[1])],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:hv_sdm_qual", study_type="scale_down_qualification",
            unit_operation=HUO_NAME, scale_down_model=HSDM,
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   qual[0], qual[1])],
            metadata=meta()),
    ]


def h_concepts():
    from annex_contract.concepts import Concept, ConceptStore
    cs = [Concept(concept_id="step:harvest_clarification", concept_type="PROCESS_STEP",
                  canonical_name=HUO_NAME,
                  aliases=["harvest", "clarification", "primary recovery", "Step 4"],
                  review_status="human_verified")]
    for name, cid in HPARAM_CONCEPT.items():
        cs.append(Concept(concept_id=cid, concept_type="PROCESS_PARAMETER", canonical_name=name,
                          review_status="human_verified"))
    for key, cid in HATTR_CONCEPT.items():
        cs.append(Concept(concept_id=cid, concept_type="QUALITY_ATTRIBUTE",
                          canonical_name=HATTR_NAME[key], aliases=[key],
                          review_status="human_verified"))
    for mid, mname, *_ in HMETHODS:
        cs.append(Concept(concept_id=f"method:{mid}", concept_type="ANALYTICAL_METHOD",
                          canonical_name=mname, aliases=[mid], review_status="human_verified"))
    return ConceptStore(run_id="gt-harvest", concepts=cs)


def h_assertions(doc_id, file_name, report):
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote, header=None):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote, table_header=header)],
            metadata=meta()))

    # step -> parameter, each on its own row of @tbl-params. The sentence that introduces the
    # table says the step has parameters; the row says WHICH parameter, at which set-point.
    prow = h_param_rows(report)
    param_sec = ("Parameters, ranges and the knowledge space" if report
                 else "Factors, ranges and study type")
    for name, cid in HPARAM_CONCEPT.items():
        add("step:harvest_clarification", "step_has_parameter", cid,
            f"{HUO_NAME} has process parameter {name}.", param_sec, prow[name], prow.header)
    # The step FORMS and CLEARS none of these: it carries the upstream-formed impurity and
    # aggregate burden forward to capture, and monitors turbidity as the feed-clarity measure.
    for key, cid in HATTR_CONCEPT.items():
        a_sec, a_quote = HATTR_QUOTE[doc_id][key]
        verb = ("monitors" if key == "turbidity" else "carries forward")
        add("step:harvest_clarification", "step_has_quality_attribute", cid,
            f"{HUO_NAME} {verb} {HATTR_NAME[key]}; it forms and clears none of the "
            f"product-quality attributes.", a_sec, a_quote)
    # attribute -> method
    for mid, mname, mtype, analytes, attrs in HMETHODS:
        for a in attrs:
            add(HATTR_CONCEPT[a], "attribute_measured_by_method", f"method:{mid}",
                f"{HATTR_NAME[a]} is measured by {mid}.", "Analytical methods",
                HMETHOD_QUOTE[doc_id][mid])
    # no-CQA-impact of the operating parameters (both docs make this claim, and the
    # report makes it from a null univariate result rather than from a fitted model)
    for name, cid in HPARAM_CONCEPT.items():
        ni_sec, ni_quote = HNOIMPACT_QUOTE[doc_id][name]
        add(cid, "parameter_does_not_significantly_impact_attribute", "attr:aggregates_hmw",
            f"{name} has no significant product-quality (CQA) impact.", ni_sec, ni_quote)
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def h_report_sections(doc_id, file_name, report):
    from annex_contract.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-004 defines the Stage 1 (process design) characterization of the A-Mab "
                  "harvest and clarification operation (Step 4).",
               "Purpose and scope",
               "it forms part of the Stage 1 process design record for the commercial process"),
            st(2, "The step sets no critical quality attribute; the attributes in scope are the "
                  "ones it carries forward to the purification train.",
               "Quality attributes in scope",
               "Table 4: Quality attributes in scope at harvest, with the drug substance acceptance criteria."),
            st(3, "Each parameter is varied across its characterization range with the other "
                  "parameters held at their set-points.",
               "Statistical methods",
               "Every parameter not varied in a run will be held at its set-point, and the set-points are those given in Table 6 ."),
            st(4, "The operation is judged against process-performance criteria (turbidity, "
                  "recovery and filter-train pressure) because it forms no CQA.",
               "Acceptance and decision criteria",
               "The comparison will cover centrate turbidity, solids removal, host cell protein and DNA in the clarified harvest, filter pressure at the end of the load, and step yield."),
            st(5, "The operation delivers the clarified harvest that the Protein A capture step "
                  "(Step 5) receives.",
               "Purpose and scope",
               "What it decides is the condition of the feed delivered to Protein A capture"),
            st(6, "No response-surface model will be fitted and no design space will be claimed "
                  "for this step.",
               "Statistical methods",
               "No response-surface model will be fitted for this step and no Monte-Carlo propagation of a fitted model will be performed, because no multivariate design is run here."),
        ])]
    yw = P.csv("yield_waterfall.csv")
    hy = float(yw[yw.step == HSTEP].iloc[0].step_yield)
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Harvest and clarification forms no critical quality attribute and reduces none; "
              "the attributes formed upstream pass through it unchanged.",
           "Product and unit operation",
           "No critical quality attribute of A-Mab responds to a parameter of this step"),
        st(2, f"The step recovers {P.pct(hy)} of the product presented to it in the nominal "
              f"commercial-scale simulation.",
           "Step yield and mass balance",
           "The step recovered 97.7% of the product mass presented to it and delivered a clarified harvest at 5 NTU at the set-point."),
        st(3, "Clarification met its in-process expectation across the ranges studied, with a "
              "single turbidity excursion above the normal operating range at near-maximum "
              "depth-filter loading (DEV-004-02), which was retained.",
           "Clarification performance and filter capacity",
           "Clarification performance was unchanged across the middle and upper part of the centrifugal field range and across the lower part of the depth filter load range."),
        st(4, "No quality attribute changed across the step: aggregate, charge variants and "
              "glycan attributes were the same leaving the step as entering it, at every "
              "setting studied.",
           "Product quality across the step",
           "No quality attribute of the antibody changed measurably across the step at any setting studied."),
        st(5, "Of the 3 parameters, 2 were classified as key process parameters and 1 as a general process parameter.; the step carries no "
              "critical process parameter.",
           "Conclusions",
           "Of the 3 parameters, 2 were classified as key process parameters and 1 as a general process parameter."),
        st(6, "The step was characterized univariately, no response-surface model was fitted "
              "and it contributes no design space to the drug substance.",
           "Design space", "No design space is defined for harvest and clarification, and none is claimed."),
        st(7, "Clearance of the impurity burden the step carries forward is credited to the "
              "purification train (PCR-005, PCR-007, PCR-008) and not to this step.",
           "Impurity burden carried to Protein A capture",
           "it is cleared by Protein A capture, cation exchange and anion exchange as reported in PCR-005, PCR-007 and PCR-008"),
        st(8, "Two deviations were recorded; neither altered a parameter classification, a "
              "characterized range or a conclusion of the report.",
           "Deviations from the plan",
           "Both were investigated, both were dispositioned as retained, and neither affected product quality."),
        st(9, "The outcome of the report rolls up into the Process Characterization Master "
              "Report (PCMR-001).",
           "Conclusions", "The results of this report are consolidated in PCMR-001."),
    ])]


# --------------------------------------------------------------------------- #
# Proven acceptable ranges (PCR-004 only).                                     #
# --------------------------------------------------------------------------- #
# Step 4 fits no response-surface model, so there is no NOR-propagated PAR and no
# per-CQA PAR: the acceptance basis is the pair of in-process criteria of the step,
# and each characterized range is proven acceptable over its full width.
# quality_attribute is left UNSET (schema_ext makes it Optional): this step governs no CQA,
# so its PARs are per-parameter. Putting an explanatory sentence in an identifier field
# would be read as an attribute id by any consumer keying on it.
HPAR_BASIS = ("Process-performance criteria of the step, not a drug-substance specification: "
              "recovery of the product and delivery of a clarified harvest fit for capture. "
              "No response-surface model was fitted, so no NOR-propagated PAR is reported.")
HPAR_QUOTE = {
    "Post-clarification turbidity": "in the sense that clarified harvest across that range was "
                                    "acceptable to capture",
}
_HPAR_GENERAL_QUOTE = ("each range is proven acceptable over its full width for the "
                       "process-performance criteria of the step")
HPAR_CAPTION = ("Proven acceptable ranges for the harvest and clarification parameters. The "
                "proven acceptable range is the univariately characterized range in each case.")


def h_proven_acceptable_ranges(doc_id, file_name):
    """One PAR per parameter, each anchored on its own row of @tbl-par.

    The step runs no designed experiment, so the PAR *is* the characterized range for the two
    settable parameters, and post-clarification turbidity carries an acceptance range on the
    material the step produces rather than a range an operator may move. PCR-004 renders all three
    as rows of one table, so each record anchors on the row that names its parameter and carries
    the table header with it, which is what says which column is the PAR.

    Re-anchored 2026-08-20 (TASK-051) against attempt 2, which renders @tbl-par again. Attempt 1
    stated the same three ranges in prose and carried no table, and this builder anchored on those
    sentences instead; the row anchor is the stronger of the two and is restored here.
    """
    df = P.report_params(HUO).rename(columns={"Char. range": "Proven acceptable range"})
    df = df[["Parameter", "Unit", "Set-point", "NOR", "Proven acceptable range"]]
    rows = row_quotes(df, df["Parameter"])
    out = []
    for i, r in enumerate(HPARAM_ROWS, 1):
        name = r["parameter"]
        rng = f"{r['par_low']:g}–{r['par_high']:g} {r['unit']}"
        out.append(S.ProvenAcceptableRange(
            par_id=f"{doc_id}-PAR{i:02d}", unit_operation=HUO_NAME,
            quality_attribute=None, parameter=name,
            characterization_range=rng,
            par_at_setpoint=rng,          # proven over the full characterized width
            par_nor_propagated=None,      # no fitted model to propagate through
            acceptance_basis=HPAR_BASIS,
            source_references=[ref(doc_id, file_name, f"{doc_id}_sec_par",
                                   "Proven acceptable ranges", rows[name],
                                   table_title=HPAR_CAPTION,
                                   table_id=f"{doc_id}_tab_par",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


def h_inventory(doc_id, file_name, dtype):
    return S.DocumentInventoryItem(
        document_id=doc_id, file_name=file_name, predicted_document_type=dtype,
        product_name_candidates=["A-Mab"], process_name_candidates=[HUO_NAME],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "harvest and clarification", "primary recovery",
                     "centrifugation", "depth filtration", "univariate characterization",
                     "parameter classification"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc_id][0]}'.",
        source_references=[ref(doc_id, file_name, "Title block", "Title block",
                               title_block_quote(doc_id))],
        metadata=meta())


def build_plan_harvest():
    doc, f = "PCP-004", PCP4_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_uo",
                                  process_steps=[h_step(doc, f, f"{doc}_sec_uo", report=False)],
                                  equipment=h_equipment(doc, f, f"{doc}_sec_uo", report=False),
                                  sites=h_sites(doc, f, f"{doc}_sec_uo")),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=h_params(doc, f, f"{doc}_sec_param", classified=False)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=h_methods(doc, f, f"{doc}_sec_methods", report=False)),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Harvest forms no product-quality CQA; no QualityAttribute entities or DesignSpace are present.",
            "No designed experiment is planned for this step: the only StudyDesign entries are a "
            "one-factor-at-a-time ranging and the scale-down model qualification.",
            "Process-performance measures (yield, turbidity, differential pressure) have no dedicated field; captured via report_sections/assertions.",
            "The Plan states classification is an OUTPUT; parameter_type left 'unclassified' here.",
        ],
        inventory=h_inventory(doc, f, "process_characterization_plan"),
        entities=entities,
        studies=h_studies(doc, f, report=False),
        report_sections=h_report_sections(doc, f, report=False),
        assertions=h_assertions(doc, f, report=False), concepts=h_concepts())


def build_report_harvest():
    doc, f = "PCR-004", PCR4_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_exec",
                                  process_steps=[h_step(doc, f, f"{doc}_sec_exec", report=True)],
                                  equipment=h_equipment(doc, f, f"{doc}_sec_exec", report=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=h_params(doc, f, f"{doc}_sec_param", classified=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=h_methods(doc, f, f"{doc}_sec_methods", report=True)),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT + [
            "ProvenAcceptableRange (new model) — per-parameter PAR against process-performance "
            "criteria (no CQA, no fitted model, so no NOR-propagated value)",
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "Harvest forms no product-quality CQA; no QualityAttribute entities or DesignSpace are present.",
            "No designed experiment was executed and no response-surface model was fitted: the "
            "report states this explicitly and claims no design space for the step.",
            "ProvenAcceptableRange.quality_attribute has no applicable value here; the acceptance "
            "basis is carried in acceptance_basis instead.",
            "Process-performance results (step yield, turbidity) have no dedicated field; reported as report_sections statements.",
            "rhetorical_spans are verbatim report prose annotating the step's negative argument "
            "(no design executed, no design space claimed, no clearance credit taken) and the "
            "credit it hands to PCR-005 / PCR-007 / PCR-008; PCR-004 carries no weak_claims.",
        ],
        inventory=h_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=h_studies(doc, f, report=True),
        proven_acceptable_ranges=h_proven_acceptable_ranges(doc, f),
        report_sections=h_report_sections(doc, f, report=True),
        assertions=h_assertions(doc, f, report=True), concepts=h_concepts(),
        rhetorical_spans=build_rhetorical_spans(doc, f))


# =========================================================================== #
# Protein A Chromatography (Step 5) — PCP-005 / PCR-005.                        #
# --------------------------------------------------------------------------- #
# Additive, self-contained builders for the Protein A DoE pair. They reuse only #
# the unit-operation-agnostic helpers (meta, ref, COMMON_EXT) and never touch   #
# the bioreactor/harvest globals above. Protein A introduces one CQA (leached   #
# Protein A) and is the principal clearance step for HCP and DNA; the DoE is a   #
# four-factor full-factorial screen + face-centred CCD in load / elution pH /   #
# flow / end-of-collect.                                                         #
# =========================================================================== #
PAUO = "protein_a"
PAUO_NAME = P.CFG.unit_op(PAUO).name             # "Protein A Chromatography"
PASTEP = P.CFG.unit_op(PAUO).step                # 5
PASTEP_LABEL = f"{PAUO_NAME} (Step {PASTEP})"

PCP5_FILE = "PCP-005_protein_a.docx"
PCR5_FILE = "PCR-005_protein_a.docx"

PAPARAM_ROWS = P.param_reg[P.param_reg.unit_operation == PAUO_NAME].to_dict("records")
PAPARAM_CONCEPT = {
    "Protein load": "param:pa_load",
    "Elution buffer pH": "param:pa_elution_ph",
    "Load flow rate": "param:pa_flow",
    "End of pool collect": "param:pa_end_collect",
    "Operating temperature": "param:pa_temperature",
    "Bed height": "param:pa_bed_height",
}
# The Version 1.0 per-entity quote tables and pa_* builders were removed on 2026-10-08: both
# Protein A documents are annexed from their Version 2.0 text in the Version 2.0 section below.


def _pa_cqa_row(key):
    return P.cqa_reg[P.cqa_reg.key == key].iloc[0].to_dict()


# build_plan_protein_a() — PCP-005 Version 2.0 — is in the Version 2.0 section below.


# build_report_protein_a() — PCR-005 Version 2.0 — is in the Version 2.0 section below.


# =========================================================================== #
# Low-pH Viral Inactivation (Step 6) — PCP-006 / PCR-006.                       #
# --------------------------------------------------------------------------- #
# Additive, self-contained builders for the viral-inactivation DoE pair. The    #
# step sets the (cumulative) XMuLV clearance CQA and can increase aggregate; the #
# DoE is a three-factor full-factorial screen + face-centred CCD in inactivation #
# pH / hold time / temperature. pH is the only true CPP in the process, and the  #
# report argues that from the data: the upper pH edge is where the NOR-          #
# propagated PAR stops short of the characterization range and where the worst   #
# characterized corner falls marginally below the back-calculated step floor —   #
# reported as an absence of assurance, not a demonstrated failure. The lower pH  #
# edge is inherited from platform data and explicitly not demonstrated here. The #
# step contributes nothing to MVM and claims no HCP clearance.                   #
# =========================================================================== #
VIUO = "viral_inactivation"
VIUO_NAME = P.CFG.unit_op(VIUO).name             # "Low-pH Viral Inactivation"
VISTEP = P.CFG.unit_op(VIUO).step                # 6
VISTEP_LABEL = f"{VIUO_NAME} (Step {VISTEP})"

PCP6_FILE = "PCP-006_viral_inactivation.docx"
PCR6_FILE = "PCR-006_viral_inactivation.docx"

VIPARAM_ROWS = P.param_reg[P.param_reg.unit_operation == VIUO_NAME].to_dict("records")
VIPARAM_CONCEPT = {
    "Inactivation pH": "param:vi_ph",
    "Hold time": "param:vi_hold_time",
    "Temperature": "param:vi_temperature",
    "A-Mab concentration": "param:vi_protein_conc",
}
VI_MULTIVARIATE = ["Inactivation pH", "Hold time", "Temperature"]
VI_UNIVARIATE = ["A-Mab concentration"]
VI_CPP = ["Inactivation pH"]                 # dominant XMuLV factor; the only CPP
VI_WCCPP = ["Hold time", "Temperature"]      # affect both LRF and aggregate

# Both documents tabulate three attributes across the step: the CQA it sets, and the
# two attributes formed at the bioreactor that the acid hold can move.
VI_CQA_KEYS = ["lrv_xmulv", "aggregates_hmw", "acidic_variants"]
VIATTR_CONCEPT = {
    "lrv_xmulv": "attr:lrv_xmulv", "aggregates_hmw": "attr:aggregates_hmw",
    "acidic_variants": "attr:acidic_variants",
}
VIATTR_NAME = {
    "lrv_xmulv": "Viral clearance — XMuLV", "aggregates_hmw": "Aggregates (HMW)",
    "acidic_variants": "Acidic charge variants",
}
VI_CQA_METHOD = {"lrv_xmulv": "AMV-3017", "aggregates_hmw": "AMV-3011",
                 "acidic_variants": "AMV-3013"}
VIMETHODS = [
    ("AMV-3017", "XMuLV Infectivity Titre (TCID50)", "infectivity_assay",
     ["XMuLV infectious titre"], ["lrv_xmulv"]),
    ("AMV-3011", "Size-Variants (SEC-HPLC)", "chromatography",
     ["aggregate", "monomer"], ["aggregates_hmw"]),
    ("AMV-3013", "Charge Variants (icIEF)", "electrophoresis",
     ["acidic variants"], ["acidic_variants"]),
]


# Per-attribute grounded fragment from each document's "Quality attributes in scope"
# section (plan §4.2 / report §2.2).
VI_CQA_QUOTE = {
    False: {  # PCP-006
        "lrv_xmulv": ("Enveloped virus clearance is of very high criticality and is the attribute "
                      "the step exists to deliver"),
        "aggregates_hmw": ("Aggregate is a high criticality attribute that this step adds to rather than removes."),
        "acidic_variants": ("Acidic charge variants are of very low criticality and are formed mainly in the production bioreactor."),
    },
    True: {  # PCR-006
        "lrv_xmulv": "Clearance of XMuLV is the attribute the hold itself produces",
        "aggregates_hmw": "Aggregate rises during the hold and is reduced at cation exchange",
        "acidic_variants": ("Acidic charge variants rise during the hold and are of very low "
                            "criticality"),
    },
}

# Per-parameter grounded fragment from the report's "Parameter classification" section
# (the two WC-CPPs) and from the plan's "Risk-based prioritization of parameters".
VI_WCCPP_QUOTE = {
    "Hold time": ("Hold time was classified as a well controlled critical process parameter. It "
                  "affects two critical quality attributes in opposite directions"),
    "Temperature": ("Temperature was classified as a well controlled critical process parameter. "
                    "Warming the pool accelerates both the acid denaturation of the envelope "
                    "glycoproteins and the association of partially unfolded antibody"),
}
VI_PLAN_RANK_QUOTE = {
    "Inactivation pH": ("Inactivation pH was ranked highest because the inactivation rate depends on it most steeply of the three, and because the same acid conditions set how far the antibody is unfolded and therefore how fast aggregate forms during the hold."),
    "Hold time": ("Hold time and temperature were ranked with it because a longer hold and a warmer hold each raise the log reduction of XMuLV and the aggregate content of the pool together."),
    "Temperature": "hold time integrates a rate constant that pH and temperature both set",
}

# Per-method grounded fragment from each document's "Analytical methods" section.
VIMETHOD_QUOTE = {
    False: {  # PCP-006
        "AMV-3017": "XMuLV infectivity will be determined by TCID50 under AMV-3017",
        "AMV-3011": "aggregate content by SEC-HPLC under AMV-3011",
        "AMV-3013": ("acidic charge variants by icIEF under AMV-3013"),
    },
    True: {  # PCR-006
        "AMV-3017": "XMuLV titre was determined by infectivity assay under AMV-3017",
        "AMV-3011": "aggregate by size-exclusion chromatography under AMV-3011",
        "AMV-3013": "charge variants by imaged capillary isoelectric focusing under AMV-3013",
    },
}


def _vi_cqa_row(key):
    return P.cqa_reg[P.cqa_reg.key == key].iloc[0].to_dict()


def vi_step(doc_id, file_name, sec, report):
    if report:
        src = ref(doc_id, file_name, sec, "Executive summary",
                  "The low-pH viral inactivation step holds the Protein A eluate at acid pH "
                  "for a defined time before it is neutralised and passed to cation exchange "
                  "chromatography")
    else:
        src = ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                  "The step brings the Protein A eluate to acid pH, holds it there for a defined time and then neutralises it to the condition at which cation exchange is loaded.")
    return S.ProcessStep(
        step_id="step:viral_inactivation", step_name=VIUO_NAME, step_number=str(VISTEP),
        unit_operation=VIUO_NAME,
        description="Dedicated viral-clearance step: the Protein A eluate is held at low pH to "
                    "inactivate enveloped viruses (XMuLV), then neutralized. Sets the cumulative "
                    "XMuLV clearance and can increase aggregate during the hold; ineffective "
                    "against the non-enveloped parvovirus model MVM.",
        input_materials=["Protein A eluate pool"],
        output_materials=["neutralized inactivated pool (cation-exchange feed)"],
        equipment=["low-pH inactivation vessel", "scale-down inactivation model"],
        source_references=[src], metadata=meta())


def vi_equipment(doc_id, file_name, sec, report):
    sdm = S.Equipment(
        equipment_id="equip:vi_sdm", equipment_name="scale-down inactivation model",
        equipment_type="viral inactivation (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Scale-down model and its qualification",
                               "a scale-down model of the commercial hold vessel, operated "
                               "under SOP-2009 and qualified under SOP-1001" if report
                               else "The studies will be run in bench-scale hold vessels operated under the same principles as the commercial hold.")],
        metadata=meta())
    if report:
        return [sdm]
    return [
        S.Equipment(equipment_id="equip:vi_vessel",
                    equipment_name="commercial-scale low-pH inactivation vessel",
                    equipment_type="inactivation vessel", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec,
                                           "Scale-down model and its qualification",
                                           "The model will match the commercial step in the pH the pool is titrated to, the temperature it is held at and the time it is held for")],
                    metadata=meta()),
        sdm,
    ]


def vi_sites(doc_id, file_name, sec):
    return [
        S.ManufacturingSite(site_id="site:cambridge", site_name=P.SENDING_SITE, site_role="sending",
                            location="Cambridge, MA",
                            source_references=[ref(doc_id, file_name, sec, "Title block",
                                                   "Cambridge, MA (Development)")],
                            metadata=meta()),
        S.ManufacturingSite(site_id="site:grafton", site_name=P.RECEIVING_SITE, site_role="receiving",
                            location="Grafton, WI",
                            source_references=[ref(doc_id, file_name, sec, "Title block",
                                                   "Grafton, WI (Commercial DS)")],
                            metadata=meta()),
    ]


def vi_params(doc_id, file_name, sec, classified):
    caption = ("Parameters of the low-pH viral inactivation step, with set-points, normal "
               "operating ranges, characterization ranges and final classification."
               if classified else
               "Parameters, ranges and study type for the planned characterization.")
    rats = {"CPP": "Largest effect on virus inactivation of any parameter studied; its proven "
                   "acceptable range under the robustness analysis stops inside the characterized "
                   "range; and it is set by a titration to an endpoint, which is a less reliable "
                   "operation than holding a timer or a jacket temperature. It is controlled to "
                   "the narrowest normal operating range of the step and is the only critical "
                   "process parameter of the step.",
            "WC-CPP": "Linked to a critical quality attribute — it affects the log reduction and "
                      "also governs aggregate — but it is controlled by the automation and "
                      "recorded continuously, and its proven acceptable ranges leave margin "
                      "beyond the normal operating range on every attribute in scope.",
            "GPP": "It does not enter the acid denaturation of the viral envelope, and its normal "
                   "operating range is its entire characterization range, so the Protein A pool "
                   "specification that already bounds it is the only control required."}
    out = []
    rows = param_rows(VIUO, classified)   # each parameter on its own @tbl-params row
    for r in VIPARAM_ROWS:
        name = r["parameter"]
        ptype = r["classification"] if classified else "unclassified"
        out.append(S.ProcessParameter(
            parameter_id=VIPARAM_CONCEPT[name], parameter_name=name, parameter_type=ptype,
            unit=r["unit"], target_value=f"{r['setpoint']:g}",
            NOR=f"{r['nor_low']:g}–{r['nor_high']:g} {r['unit']}",
            PAR=f"{r['par_low']:g}–{r['par_high']:g} {r['unit']}",
            associated_step=VISTEP_LABEL,
            rationale_for_criticality=rats.get(r["classification"]) if classified else None,
            source_references=[ref(doc_id, file_name, sec,
                                   "Factors, ranges and the knowledge space" if classified
                                   else "Factors, ranges and study type",
                                   rows[name], table_title=caption,
                                   table_id=f"{doc_id}_tab_params",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


def vi_cqas(doc_id, file_name, sec, report):
    quotes = VI_CQA_QUOTE[report]
    caption = ("Quality attributes measured across the low-pH viral inactivation step." if report
               else "Quality attributes in scope for the low-pH viral inactivation step.")
    out = []
    rows = cqa_rows(VI_CQA_KEYS)   # each attribute on its own @tbl-cqa row
    for key in VI_CQA_KEYS:
        r = _vi_cqa_row(key)
        out.append(S.QualityAttribute(
            attribute_id=VIATTR_CONCEPT[key], attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"],
            acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            analytical_method=None if report else VI_CQA_METHOD[key],
            associated_steps=[VISTEP_LABEL],
            rationale_for_criticality=f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = {r['tool1_score']}.",
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref(doc_id, file_name, sec, "Quality attributes in scope",
                                   rows[key], table_title=caption,
                                   table_id=f"{doc_id}_tab_cqa",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


def vi_methods(doc_id, file_name, sec, report):
    quotes = VIMETHOD_QUOTE[report]
    out = []
    for mid, mname, mtype, analytes, attrs in VIMETHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[VIATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods", quotes[mid])],
            metadata=meta()))
    return out


def vi_studies(doc_id, file_name, report):
    sec = "Study design"
    n_scr, n_rsm = P.doe_runs(VIUO, "screening"), P.doe_runs(VIUO, "rsm")
    return [
        S.StudyDesign(
            study_id="study:vi_screening", study_type="screening_doe",
            design_name="two-level full factorial", unit_operation=VIUO_NAME,
            factors=VI_MULTIVARIATE,
            responses=["xmulv_lrf", "aggregate_out_pct", "acidic_variants"],
            n_runs=n_scr, n_center_points=P.doe_centre_points(VIUO, "screening"), scale_down_model="scale-down inactivation model",
            associated_parameters=[VIPARAM_CONCEPT[f] for f in VI_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Screening design",
                                   "Screening used a two-level full factorial in the three "
                                   "multivariate parameters" if report
                                   else "The screening design is a full factorial in the 3 multivariate factors")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vi_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=VIUO_NAME,
            factors=VI_MULTIVARIATE,
            responses=["xmulv_lrf", "aggregate_out_pct", "acidic_variants"],
            n_runs=n_rsm, n_center_points=P.doe_centre_points(VIUO, "rsm"), scale_down_model="scale-down inactivation model",
            associated_parameters=[VIPARAM_CONCEPT[f] for f in VI_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "The response-surface design was a face-centred central "
                                   "composite design in the same three parameters" if report
                                   else "All 3 factors will be carried into the response-surface design whatever the screening result.")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vi_sdm_qual", study_type="scale_down_qualification",
            unit_operation=VIUO_NAME, scale_down_model="scale-down inactivation model",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "Qualification compared the model with at-scale data on the "
                                   "inputs and the outputs of the step" if report
                                   else "The model will be accepted as representative when no statistically significant difference is found between scales at α = 0.05 for the three responses")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vi_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=VIUO_NAME,
            factors=VI_UNIVARIATE,
            responses=["xmulv_lrf", "aggregate_out_pct", "acidic_variants"],
            associated_parameters=[VIPARAM_CONCEPT[f] for f in VI_UNIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Univariate assessment",
                                   "A-Mab concentration was assessed one parameter at a time" if report
                                   else "The ranking placed inactivation pH, hold time and temperature in the group warranting multivariate evaluation, and A-Mab concentration in the group whose range can be supported by a univariate study.")],
            metadata=meta()),
    ]


def vi_concepts():
    from annex_contract.concepts import Concept, ConceptStore
    cs = [Concept(concept_id="step:viral_inactivation", concept_type="PROCESS_STEP",
                  canonical_name=VIUO_NAME,
                  aliases=["viral inactivation", "low-pH hold", "low-pH viral inactivation", "Step 6"],
                  review_status="human_verified")]
    for name, cid in VIPARAM_CONCEPT.items():
        cs.append(Concept(concept_id=cid, concept_type="PROCESS_PARAMETER", canonical_name=name,
                          review_status="human_verified"))
    for key in ["lrv_xmulv", "aggregates_hmw", "acidic_variants"]:
        cs.append(Concept(concept_id=VIATTR_CONCEPT[key], concept_type="QUALITY_ATTRIBUTE",
                          canonical_name=VIATTR_NAME[key], aliases=[key],
                          review_status="human_verified"))
    for mid, mname, *_ in VIMETHODS:
        cs.append(Concept(concept_id=f"method:{mid}", concept_type="ANALYTICAL_METHOD",
                          canonical_name=mname, aliases=[mid], review_status="human_verified"))
    return ConceptStore(run_id="gt-viral_inactivation", concepts=cs)


def vi_assertions(doc_id, file_name, report):
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote, header=None):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote,
                                   table_header=header)],
            metadata=meta()))

    param_sec = "Factors, ranges and the knowledge space" if report else "Factors, ranges and study type"
    prow = param_rows(VIUO, report)   # the row that NAMES this parameter
    for name, cid in VIPARAM_CONCEPT.items():
        add("step:viral_inactivation", "step_has_parameter", cid,
            f"{VIUO_NAME} has process parameter {name}.", param_sec, prow[name],
            prow.header)
    # step sets the XMuLV clearance CQA and carries the aggregate / acidic-variant risk
    add("step:viral_inactivation", "step_has_quality_attribute", "attr:lrv_xmulv",
        f"{VIUO_NAME} produces the XMuLV clearance credited to the step."
        if report else f"{VIUO_NAME} sets the cumulative XMuLV clearance.",
        "Quality attributes in scope",
        "Clearance of XMuLV is the attribute the hold itself produces" if report
        else "Table 4: Quality attributes in scope for this step, with drug substance acceptance and criticality.")
    for key in ["aggregates_hmw", "acidic_variants"]:
        add("step:viral_inactivation", "step_has_quality_attribute", VIATTR_CONCEPT[key],
            f"{VIUO_NAME} can raise {VIATTR_NAME[key]} during the low-pH hold; the attribute is "
            f"formed upstream and is not set here.", "Quality attributes in scope",
            VI_CQA_QUOTE[report][key])
    # The step's two explicit non-claims (no MVM, no HCP clearance) have no predicate in the
    # upstream vocabulary; they are carried as report_sections statements instead.
    # attribute -> method (plan only)
    if not report:
        for key in VI_CQA_METHOD:
            add(VIATTR_CONCEPT[key], "attribute_measured_by_method", f"method:{VI_CQA_METHOD[key]}",
                f"{VIATTR_NAME[key]} is measured by {VI_CQA_METHOD[key]}.", "Analytical methods",
                VIMETHOD_QUOTE[False][VI_CQA_METHOD[key]])
    # acceptance criterion for the viral-clearance CQA: cumulative, back-calculated to a step floor
    xr = _vi_cqa_row("lrv_xmulv")
    add("attr:lrv_xmulv", "attribute_has_acceptance_criterion", "lit:lrv_xmulv_acc",
        f"Cumulative XMuLV clearance acceptance: {xr['acc_low']:g}–{xr['acc_high']:g} {xr['unit']}; "
        f"the criterion applied to this step is the back-calculated step contribution.",
        "Quality attributes in scope",
        "its acceptance criterion is cumulative across the train rather than assigned to any "
        "single step" if report
        else "The drug substance requires a cumulative enveloped virus clearance of at least 16.7 log10 across the train.")
    # parameter -> attribute impacts / non-impacts
    if report:
        add("param:vi_ph", "parameter_impacts_attribute", "attr:lrv_xmulv",
            "Inactivation pH has the largest effect on virus inactivation of any parameter "
            "studied and is the only critical process parameter of the step.",
            "Parameter classification",
            "Inactivation pH was classified as a critical process parameter. It has the largest "
            "effect on virus inactivation of any parameter studied")
        for name in VI_WCCPP:
            add(VIPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:lrv_xmulv",
                f"{name} affects the log-reduction and also governs aggregate (WC-CPP).",
                "Parameter classification", VI_WCCPP_QUOTE[name])
        add("param:vi_hold_time", "parameter_impacts_attribute", "attr:acidic_variants",
            "Acidic charge variants respond to hold time alone over the characterized ranges, and "
            "no other term returned an estimate distinguishable from zero.",
            "Factor effects from the screening design",
            "Acidic charge variants responded to hold time alone")
        add("param:vi_ph", "parameter_does_not_significantly_impact_attribute", "attr:aggregates_hmw",
            "Inactivation pH had no detectable effect on aggregate over the characterized range; "
            "the aggregate model returns no term in pH, so the two constraints on the step are "
            "independent along the pH axis.",
            "Mechanistic interpretation",
            "Hold time and temperature are the two significant coefficients in the aggregate "
            "model, and inactivation pH returns none")
        add("param:vi_protein_conc", "parameter_does_not_significantly_impact_attribute", "attr:lrv_xmulv",
            "A-Mab concentration is a GPP: it does not enter the acid denaturation of the viral "
            "envelope, and its normal operating range equals its characterization range.",
            "Parameter classification",
            "A-Mab concentration was classified as a general process parameter. It does not "
            "enter the acid denaturation of the viral envelope")
    else:
        for name in VI_MULTIVARIATE:
            add(VIPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:lrv_xmulv",
                f"{name} was ranked for multivariate study on its credible impact on the "
                f"enveloped-virus inactivation and its potential to interact.",
                "Risk-based prioritization of parameters", VI_PLAN_RANK_QUOTE[name])
        add("param:vi_protein_conc", "parameter_does_not_significantly_impact_attribute", "attr:lrv_xmulv",
            "A-Mab concentration is expected to affect neither response over a wide range.",
            "Risk-based prioritization of parameters",
            "Association is a bimolecular event, so a more concentrated pool aggregates faster, but the concentration of the pool has no part in the inactivation chemistry.")
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def vi_report_sections(doc_id, file_name, report):
    from annex_contract.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote, also=()):
        """``also`` carries further ``(section, quote)`` pairs. The step states its two
        non-claims — no MVM clearance, no host cell protein clearance — in two different
        sections, so one statement needs two anchors."""
        refs = [ref(doc_id, file_name, sec, sec, quote)]
        refs += [ref(doc_id, file_name, s2, s2, q2) for s2, q2 in also]
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=refs)
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-006 defines the process characterization study for the A-Mab low-pH viral "
                  "inactivation step (Step 6), written before any characterization data exist.",
               "Purpose and scope",
               "Deliverables and schedule The deliverable of this plan is the Process Characterization Report for the step, PCR-006."),
            st(2, "Four process parameters are characterized; inactivation pH, hold time and "
                  "temperature are the multivariate factors and A-Mab concentration is univariate.",
               "Purpose and scope",
               "To measure the effect of inactivation pH, hold time and temperature on the log reduction of XMuLV, on the aggregate content of the neutralised pool and on the acidic charge variant content"),
            st(3, "The study uses a full-factorial screen followed by a face-centred "
                  "central-composite design on a qualified scale-down hold model.",
               "Response-surface design",
               "All 3 factors will be carried into the response-surface design whatever the screening result."),
            st(4, "Low-pH inactivation is enveloped-virus specific; the parvovirus claim rests on "
                  "anion exchange and virus filtration instead.",
               "Purpose and scope",
               "Low-pH inactivation, anion exchange and virus filtration each contribute an independent log reduction, and the modular claim is the sum of the three"),
            st(5, "The enveloped-virus acceptance criterion for this step is a back-calculated "
                  "step contribution, not the cumulative drug-substance requirement.",
               "Acceptance and decision criteria",
               "The criterion that applies to this step alone is therefore not the cumulative figure but the contribution the step must deliver for the cumulative figure to hold"),
            st(6, "The clearance claim will be framed conservatively, from the worst case of the "
                  "operating region rather than the mean at the set-point.",
               "Acceptance and decision criteria",
               "The response-surface model is the predictive model, and it is the only model from which an operating region, a proven acceptable range or a prediction at an untested setting will be derived."),
            st(7, "The operating region must satisfy every response criterion at the same time, "
                  "evaluated from the fitted models with the other parameters varying within "
                  "their normal operating ranges.",
               "Acceptance and decision criteria",
               "At each of 81 points across the characterization range of the parameter of interest, 2,000 Monte-Carlo draws are taken with the other parameters sampled within their normal operating ranges"),
            st(8, "The pH criterion is two-sided and decisive for this step: its upper edge is set "
                  "by the log-reduction criterion and its lower edge by the aggregate criterion.",
               "Acceptance and decision criteria",
               "A parameter whose response crosses its criterion steeply needs tighter control than one whose response approaches it slowly"),
            st(9, "Proven acceptable ranges will be reported in two forms, and the analysis that "
                  "propagates the other parameters across their normal operating ranges is the "
                  "reported default.",
               "Proven acceptable ranges (planned analysis)",
               "Aggregate and acidic charge variant samples will be drawn after neutralisation, because those are the values the cation exchange step receives."),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Inactivation pH was classified as a critical process parameter, hold time and "
              "temperature as well controlled critical process parameters, and A-Mab "
              "concentration as a general process parameter.",
           "Executive summary",
           "Inactivation pH was classified as a critical process parameter, hold time and "
           "temperature as well controlled critical process parameters, and A-Mab concentration "
           "as a general process parameter"),
        st(2, "The screening model identifies which parameters are active; the response-surface "
              "model is the predictive model behind every range and every prediction in the "
              "report.",
           "Statistical methods",
           "its estimates are refined by the response-surface model, which is the predictive "
           "model used for every range and every prediction in this report"),
        st(3, "The pH dependence of clearance is curved: the gain in clearance from lowering the "
              "pH falls away toward the acid edge of the characterized range.",
           "Mechanistic interpretation",
           "The negative curvature in pH says that the gain in clearance from lowering the pH "
           "falls away toward the acid edge of the range."),
        st(4, "At the high-pH, short-hold, low-temperature corner of the characterized region the "
              "predicted log reduction falls below the required step contribution, so that corner "
              "lies outside the design space and an edge of failure exists inside the knowledge "
              "space.",
           "Design space",
           "so that corner lies outside the design space and an edge of failure exists inside the "
           "knowledge space"),
        st(5, "The attribute and parameter combinations that return less than the full "
              "characterization range are the ones that constrain the step: hold time against "
              "aggregate, and inactivation pH against the XMuLV log reduction factor.",
           "Proven acceptable ranges",
           "The remaining 2 return less, and they are the combinations that constrain the step"),
        st(6, "Cumulative XMuLV clearance is the tightest of the three capabilities the step "
              "influences.",
           "Process capability and robustness",
           "Clearance of XMuLV is the tightest of the three"),
        st(7, "The step is the largest single contributor to the cumulative XMuLV claim, and it "
              "is not the whole claim.",
           "Process capability and robustness",
           "The step is the largest single contributor, and it is not the whole claim."),
        st(8, "The step is credited with no parvovirus clearance and claims no host cell protein "
              "clearance.",
           "Contribution to the control strategy",
           "A non-enveloped parvovirus has no lipid envelope for acid to disrupt, so a low-pH "
           "hold does not inactivate it, and the MVM claim rests entirely on anion exchange and "
           "virus filtration",
           [("Product and unit operation",
             "the extent is not predictable from the parameters studied here, and no host cell "
             "protein clearance is claimed for this step")]),
        st(9, "The acidic charge-variant replicates returned the same value, so the pure-error "
              "sum of squares is zero and lack of fit cannot be evaluated for that response.",
           "Response-surface models",
           "so the pure-error sum of squares is zero, the lack-of-fit test cannot be evaluated"),
        st(10, "The lower bound of the characterized pH range was set by prior platform "
               "experience of antibody precipitation, not by a result of this study.",
            "Platform and prior-product knowledge",
            "Prior experience also set the lower bound of the pH range studied."),
    ])]


def vi_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:viral_inactivation", unit_operation=VIUO_NAME,
        parameters=["param:vi_ph", "param:vi_hold_time", "param:vi_temperature"],
        quality_attributes_constrained=["attr:lrv_xmulv", "attr:aggregates_hmw"],
        definition="The set of combinations of inactivation pH, hold time and temperature at which "
                   "the response-surface models predict a step log reduction factor at or above "
                   "the back-calculated step contribution and pool aggregate at or below the "
                   "in-process criterion the step is judged against. Aggregate is the binding "
                   "constraint: it rejects the largest part of the grid evaluated over the "
                   "characterized ranges, the log reduction factor rejects a small remainder, and "
                   "acidic charge variants reject none. Two corners fall outside the region — the "
                   "highest pH with the shortest hold at the lowest temperature, where the "
                   "predicted log reduction falls below the required step contribution, and the "
                   "corner with pH, hold time and temperature all at their high edges, where the "
                   "predicted aggregate exceeds the in-process criterion. Every corner of the "
                   "normal operating ranges lies inside the region.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "The operating region is therefore bounded by the aggregate the "
                               "hold forms and cation exchange removes, and not by the virus "
                               "inactivation the hold delivers")],
        metadata=meta())]


# --------------------------------------------------------------------------- #
# Report-only PAR / discourse layers (PCR-006 only).                            #
# --------------------------------------------------------------------------- #
# proven_acceptable_ranges derive from the same DoE engine that renders @tbl-par  #
# (doe_report.par_table); rhetorical_spans annotate the report's argument         #
# structure. Both quote verbatim, plain-prose fragments of the rendered report.   #
# PCR-006 carries NO weak_claims. These layers are report-only (the plan omits    #
# them); the plan-side builders above are untouched.                              #
# --------------------------------------------------------------------------- #
VI_PAR_SEC = "Proven acceptable ranges"
# Per-CQA grounded fragment from the report's Proven-acceptable-ranges section.
VI_PAR_CQA_QUOTE = {
    "XMuLV LRF (log₁₀)": ("The criterion applied to this step is the required step contribution, "
                          "obtained by subtracting the clearance credited to anion exchange and "
                          "virus filtration from the cumulative requirement"),
}
_VI_PAR_GENERAL_QUOTE = ("For acidic variants the criterion is the drug "
                         "substance specification given in")


def vi_proven_acceptable_ranges(doc_id, file_name):
    """One ProvenAcceptableRange per governed CQA x response-surface parameter, from the
    same DoE engine (``doe_report.par_table``) that renders @tbl-par in the report. Aggregate
    and acidic variants use the drug-substance specification; the viral-clearance CQA uses the
    back-calculated step floor (the modular required log-reduction) as the acceptance basis."""
    import doe_report as D
    par = D.par_table(VIUO)
    out = []
    # Each attribute x parameter combination on its own @tbl-par row: the
    # per-attribute prose said which attribute was governed, never which
    # parameter's range was proven.
    rows = par_rows(VIUO)
    for i, r in enumerate(par.to_dict("records"), 1):
        cqa, param, unit = r["CQA"], r["Parameter"], (r["Unit"] or "")
        char = f"{r['Char. range']} {unit}".strip()
        basis = par_basis_text(VIUO, cqa)
        out.append(S.ProvenAcceptableRange(
            par_id=f"{doc_id}-PAR{i:02d}", unit_operation=VIUO_NAME,
            quality_attribute=cqa, parameter=param,
            characterization_range=char,
            par_at_setpoint=f"{r['PAR (set-point)']} {unit}".strip(),
            par_nor_propagated=f"{r['PAR (NOR)']} {unit}".strip(),
            acceptance_basis=basis,
            source_references=[ref(doc_id, file_name, f"{doc_id}_sec_par", VI_PAR_SEC,
                                   rows[(cqa, param)],
                                   table_id=f"{doc_id}_tab_par",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


def vi_inventory(doc_id, file_name, dtype):
    return S.DocumentInventoryItem(
        document_id=doc_id, file_name=file_name, predicted_document_type=dtype,
        product_name_candidates=["A-Mab"], process_name_candidates=[VIUO_NAME],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "low-pH viral inactivation", "viral clearance",
                     "XMuLV log-reduction", "design of experiments", "parameter classification"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc_id][0]}'.",
        source_references=[ref(doc_id, file_name, "Title block", "Title block",
                               title_block_quote(doc_id))],
        metadata=meta())


def build_plan_viral_inactivation():
    doc, f = "PCP-006", PCP6_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_uo",
                                  process_steps=[vi_step(doc, f, f"{doc}_sec_uo", report=False)],
                                  equipment=vi_equipment(doc, f, f"{doc}_sec_uo", report=False),
                                  sites=vi_sites(doc, f, f"{doc}_sec_uo")),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=vi_cqas(doc, f, f"{doc}_sec_cqa", report=False)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=vi_params(doc, f, f"{doc}_sec_param", classified=False)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=vi_methods(doc, f, f"{doc}_sec_methods", report=False)),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "The XMuLV criterion for this step is a back-calculated step contribution (cumulative "
            "requirement minus the clearance credited to AEX and virus filtration) under the "
            "modular ICH Q5A(R2) approach; the claim is to be framed at the worst case of the "
            "operating region, not at the set-point mean.",
            "MVM is not inactivated at low pH; the step is credited with enveloped-virus clearance "
            "only and no HCP clearance is claimed.",
            "The Plan states classification is an OUTPUT; parameter_type left 'unclassified' here.",
        ],
        inventory=vi_inventory(doc, f, "process_characterization_plan"),
        entities=entities,
        studies=vi_studies(doc, f, report=False),
        report_sections=vi_report_sections(doc, f, report=False),
        assertions=vi_assertions(doc, f, report=False), concepts=vi_concepts())


def build_report_viral_inactivation():
    doc, f = "PCR-006", PCR6_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_exec",
                                  process_steps=[vi_step(doc, f, f"{doc}_sec_exec", report=True)],
                                  equipment=vi_equipment(doc, f, f"{doc}_sec_exec", report=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=vi_params(doc, f, f"{doc}_sec_param", classified=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=vi_cqas(doc, f, f"{doc}_sec_cqa", report=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=vi_methods(doc, f, f"{doc}_sec_methods", report=True)),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT + [
            "ProvenAcceptableRange (new model) — per-CQA x parameter PAR (at-set-point / "
            "NOR-propagated); the viral CQA uses a back-calculated step floor",
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "XMuLV clearance is a modular claim under ICH Q5A(R2). The credited step contribution "
            "in the modular ledger comes from the process model; the response-surface model of "
            "this study predicts the set-point value independently, and the report credits the "
            "measured reduction as a minimum because the infectivity assay reads a lower bound "
            "on the affected samples.",
            "The step contributes nothing to MVM clearance and claims no HCP clearance; both are "
            "stated as explicit non-claims and have no predicate in the upstream assertion "
            "vocabulary, so they are carried as report_sections statements.",
            "Acidic variants are a deterministic function of hold time in the seeded model (zero "
            "centre-point SD, exact fit, no pure error), so their lack of fit is untestable and "
            "the report states their fit statistics are uninformative.",
            "Process-capability (Cpk) values have no dedicated field; reported as report_sections statements.",
            "proven_acceptable_ranges mirror @tbl-par (doe_report.par_table); rhetorical_spans are "
            "verbatim report prose; PCR-006 carries no weak_claims.",
        ],
        inventory=vi_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=vi_studies(doc, f, report=True),
        design_spaces=vi_design_spaces(doc, f),
        proven_acceptable_ranges=vi_proven_acceptable_ranges(doc, f),
        report_sections=vi_report_sections(doc, f, report=True),
        assertions=vi_assertions(doc, f, report=True), concepts=vi_concepts(),
        rhetorical_spans=build_rhetorical_spans(doc, f))


# =========================================================================== #
# Cation Exchange Chromatography (Step 7) — PCP-007 / PCR-007.                  #
# --------------------------------------------------------------------------- #
# Additive, self-contained builders for the CEX polishing DoE pair. The step    #
# sets NO CQA: it is the only step in the train that reduces aggregate, and a    #
# major clearance step for HCP, residual DNA and leached Protein A, all formed   #
# upstream. The DoE is a four-factor full-factorial screen + face-centred CCD in #
# load / wash-conductivity / elution-pH / stop-collect; flow is a univariate GPP.#
# All four multivariate factors are WC-CPP (each affects aggregate or HCP).      #
# Two framing points the report makes and the annex follows: (a) pool HCP is an  #
# in-process value, not a failed criterion — the step is judged on its clearance #
# factor and on delivering a load AEX can finish, with the further AEX clearance #
# credited to PCR-008 and the cumulative position to PCMR-001; (b) aggregate is  #
# the opposite case — CEX is the last aggregate-reduction step, so the DS limit   #
# genuinely binds here and the step carries it alone. No response shows           #
# significant curvature, and the yield model is direction-only (pred. R2 0.20).   #
# =========================================================================== #
CXUO = "cex"
CXUO_NAME = P.CFG.unit_op(CXUO).name             # "Cation Exchange Chromatography"
CXSTEP = P.CFG.unit_op(CXUO).step                # 7
CXSTEP_LABEL = f"{CXUO_NAME} (Step {CXSTEP})"

PCP7_FILE = "PCP-007_cex.docx"
PCR7_FILE = "PCR-007_cex.docx"

CXPARAM_ROWS = P.param_reg[P.param_reg.unit_operation == CXUO_NAME].to_dict("records")
CXPARAM_CONCEPT = {
    "Protein load": "param:cex_load",
    "Load/Wash conductivity": "param:cex_wash_cond",
    "Elution buffer pH": "param:cex_elution_ph",
    "Elution stop collect": "param:cex_stop_collect",
    "Elution flow rate": "param:cex_flow",
}
# The four DoE factors (all WC-CPP) vs the univariate GPP.
CX_MULTIVARIATE = ["Protein load", "Load/Wash conductivity", "Elution buffer pH",
                   "Elution stop collect"]
CX_UNIVARIATE = ["Elution flow rate"]
CX_AGG_DRIVERS = ["Protein load", "Elution buffer pH", "Elution stop collect"]  # -> aggregate
CX_HCP_DRIVER = "Load/Wash conductivity"                                        # -> HCP

# CEX sets no CQA; it controls/clears these (formed upstream).
CX_CQA_KEYS = ["aggregates_hmw", "hcp", "residual_dna", "leached_protein_a"]
CXATTR_CONCEPT = {
    "aggregates_hmw": "attr:aggregates_hmw", "hcp": "attr:hcp",
    "residual_dna": "attr:residual_dna", "leached_protein_a": "attr:leached_protein_a",
}
CXATTR_NAME = {
    "aggregates_hmw": "Aggregates (HMW)", "hcp": "Host Cell Protein (HCP)",
    "residual_dna": "Residual DNA", "leached_protein_a": "Leached Protein A",
}
CX_CQA_METHOD = {"aggregates_hmw": "AMV-3011", "hcp": "AMV-3012",
                 "residual_dna": "AMV-3014", "leached_protein_a": "AMV-3016"}
CXMETHODS = [
    ("AMV-3011", "Size-Variants (SEC-HPLC)", "chromatography",
     ["aggregate", "monomer"], ["aggregates_hmw"]),
    ("AMV-3012", "Host-Cell Protein ELISA", "immunoassay", ["host-cell protein"], ["hcp"]),
    ("AMV-3014", "Residual DNA (qPCR)", "qPCR", ["residual host-cell DNA"], ["residual_dna"]),
    ("AMV-3016", "Leached Protein A by ELISA (ppm)", "immunoassay",
     ["leached Protein A"], ["leached_protein_a"]),
]


def _cx_cqa_row(key):
    return P.cqa_reg[P.cqa_reg.key == key].iloc[0].to_dict()


def cx_step(doc_id, file_name, sec, report):
    if report:
        src = ref(doc_id, file_name, sec, "Executive summary",
                  "Cation exchange chromatography is the first of the two polishing steps in "
                  "the A-Mab drug substance process")
    else:
        src = ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                  "humanized IgG1 platform for three previous products (X-Mab, Y-Mab and "
                  "Z-Mab) and throughout A-Mab clinical and engineering manufacture")
    return S.ProcessStep(
        step_id="step:cex", step_name=CXUO_NAME, step_number=str(CXSTEP),
        unit_operation=CXUO_NAME,
        description="Bind-and-elute cation-exchange polishing: the only step in the train "
                    "that reduces aggregate, and a major clearance step for HCP with modular "
                    "clearance of residual DNA and leached Protein A. Forms no product-quality "
                    "CQA; every attribute it governs is formed upstream and reduced here.",
        input_materials=["neutralized viral-inactivation pool (cation-exchange feed)"],
        output_materials=["cation-exchange eluate pool (anion-exchange feed)"],
        equipment=["cation-exchange column", "scale-down chromatography column"],
        source_references=[src], metadata=meta())


def cx_equipment(doc_id, file_name, sec, report):
    sdm = S.Equipment(
        equipment_id="equip:cex_sdm_column", equipment_name="scale-down chromatography column",
        equipment_type="chromatography column (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Scale-down model and its qualification",
                               "The study was executed on a laboratory-scale chromatography "
                               "system operated as a model of the commercial column" if report
                               else "The studies will be run on a laboratory column packed "
                                    "with the same resin type and to the same bed height as the "
                                    "commercial column, and operated at the same linear "
                                    "velocities.")],
        metadata=meta())
    if report:
        return [sdm]
    return [
        S.Equipment(equipment_id="equip:cex_column",
                    equipment_name="commercial-scale cation-exchange polishing column",
                    equipment_type="chromatography column", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec,
                                           "Scale-down model and its qualification",
                                           "The studies will be executed on a qualified "
                                           "scale-down model of the commercial column")],
                    metadata=meta()),
        sdm,
    ]


def cx_sites(doc_id, file_name, sec):
    return [
        S.ManufacturingSite(site_id="site:cambridge", site_name=P.SENDING_SITE, site_role="sending",
                            location="Cambridge, MA",
                            source_references=[ref(doc_id, file_name, sec, "Title block",
                                                   "Cambridge, MA (Development)")],
                            metadata=meta()),
        S.ManufacturingSite(site_id="site:grafton", site_name=P.RECEIVING_SITE, site_role="receiving",
                            location="Grafton, WI",
                            source_references=[ref(doc_id, file_name, sec, "Title block",
                                                   "Grafton, WI (Commercial DS)")],
                            metadata=meta()),
    ]


def cx_params(doc_id, file_name, sec, classified):
    caption = ("Cation exchange process parameters, with set-points, normal operating ranges, "
               "characterization ranges, final classification and study type."
               if classified else
               "Parameters in scope, with the ranges to be studied and the assigned study type.")
    rats = {"WC-CPP": "Demonstrated effect on pool aggregate and/or pool host cell protein, and "
                      "held reliably inside the operating region either by an instrument that "
                      "reads during the cycle or by a calculation completed before it starts.",
            "GPP": "No effect on any governed attribute across the characterization range; its "
                   "action is on cycle time."}
    out = []
    rows = param_rows(CXUO, classified)   # each parameter on its own @tbl-params row
    for r in CXPARAM_ROWS:
        name = r["parameter"]
        ptype = r["classification"] if classified else "unclassified"
        out.append(S.ProcessParameter(
            parameter_id=CXPARAM_CONCEPT[name], parameter_name=name, parameter_type=ptype,
            unit=r["unit"], target_value=f"{r['setpoint']:g}",
            NOR=f"{r['nor_low']:g}–{r['nor_high']:g} {r['unit']}",
            PAR=f"{r['par_low']:g}–{r['par_high']:g} {r['unit']}",
            associated_step=CXSTEP_LABEL,
            rationale_for_criticality=rats.get(r["classification"]) if classified else None,
            source_references=[ref(doc_id, file_name, sec,
                                   "Factors, ranges and the knowledge space" if classified
                                   else "Factors, ranges and study type",
                                   rows[name], table_title=caption,
                                   table_id=f"{doc_id}_tab_params",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


# Both documents introduce the four governed attributes one criticality tier at a time,
# so each CQA is anchored on the sentence that introduces it rather than on a shared span.
CX_CQA_TABLE_CAPTION = {
    True: ("Quality attributes controlled and cleared by the cation exchange step, with their "
           "drug substance acceptance criteria and criticality."),
    False: ("Quality attributes this step controls or clears, with drug-substance acceptance "
            "criteria."),
}
CX_CQA_QUOTE = {
    False: {  # PCP-007
        "aggregates_hmw": ("Aggregate is the attribute the step governs most directly, at high "
                           "criticality"),
        "hcp": ("Host cell protein is of moderate to high criticality and is cleared by three "
                "steps in sequence"),
        "residual_dna": ("residual DNA is of very low criticality and clears by a wide margin "
                         "across the three chromatography steps"),
        "leached_protein_a": ("leached Protein A is formed at the capture step (PCP-005) and is "
                              "reduced here and again at anion exchange, at low to moderate "
                              "criticality"),
    },
    True: {  # PCR-007
        "aggregates_hmw": ("Aggregate carries a high criticality and is measured as high molecular "
                           "weight species by size-exclusion chromatography"),
        "hcp": ("Host cell protein carries a moderate to high criticality and is measured by "
                "immunoassay"),
        "residual_dna": ("Residual DNA and leached Protein A carry low criticality and large "
                         "capability margins"),
        "leached_protein_a": ("Residual DNA and leached Protein A carry low criticality and large "
                              "capability margins"),
    },
}


def cx_cqas(doc_id, file_name, sec, report):
    quotes = CX_CQA_QUOTE[report]
    caption = CX_CQA_TABLE_CAPTION[report]
    out = []
    rows = cqa_rows(CX_CQA_KEYS)   # each attribute on its own @tbl-cqa row
    for key in CX_CQA_KEYS:
        r = _cx_cqa_row(key)
        out.append(S.QualityAttribute(
            attribute_id=CXATTR_CONCEPT[key], attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"],
            acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            analytical_method=None if report else CX_CQA_METHOD[key],
            associated_steps=[CXSTEP_LABEL],
            rationale_for_criticality=f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = {r['tool1_score']}.",
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref(doc_id, file_name, sec, "Quality attributes in scope",
                                   rows[key], table_title=caption,
                                   table_id=f"{doc_id}_tab_cqa",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


# Per-method grounded fragment from each document's analytical-methods section.
CXMETHOD_QUOTE = {
    False: {  # PCP-007
        "AMV-3011": ("Pool aggregate will be measured by size exclusion chromatography under "
                     "AMV-3011"),
        "AMV-3012": ("Host cell protein will be measured by enzyme linked immunosorbent assay "
                     "under AMV-3012"),
        "AMV-3014": ("Residual DNA will be measured by quantitative polymerase chain reaction "
                     "under AMV-3014"),
        "AMV-3016": "leached Protein A by enzyme linked immunosorbent assay under AMV-3016",
    },
    True: {  # PCR-007
        "AMV-3011": ("Pool aggregate was measured as the high molecular weight fraction by "
                     "size-exclusion high-performance liquid chromatography under AMV-3011"),
        "AMV-3012": ("Pool host cell protein was measured by enzyme-linked immunosorbent assay "
                     "under AMV-3012"),
        "AMV-3014": ("Residual DNA was measured by quantitative polymerase chain reaction under "
                     "AMV-3014"),
        "AMV-3016": "leached Protein A by enzyme-linked immunosorbent assay under AMV-3016",
    },
}


def cx_methods(doc_id, file_name, sec, report):
    quotes = CXMETHOD_QUOTE[report]
    out = []
    for mid, mname, mtype, analytes, attrs in CXMETHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[CXATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods", quotes[mid])],
            metadata=meta()))
    return out


def cx_studies(doc_id, file_name, report):
    sec = "Study design"
    n_scr, n_rsm = P.doe_runs(CXUO, "screening"), P.doe_runs(CXUO, "rsm")
    responses = ["aggregate_out_pct", "hcp_out_ng_mg", "step_yield"]
    return [
        S.StudyDesign(
            study_id="study:cex_screening", study_type="screening_doe",
            design_name="two-level full factorial", unit_operation=CXUO_NAME,
            factors=CX_MULTIVARIATE, responses=responses,
            n_runs=n_scr, n_center_points=P.doe_centre_points(CXUO, "screening"), scale_down_model="scale-down chromatography column",
            associated_parameters=[CXPARAM_CONCEPT[f] for f in CX_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Screening design",
                                   "The screening study was a two-level full factorial in the "
                                   "four multivariate factors" if report
                                   else "The design as planned estimates every main effect "
                                        "and every two factor interaction independently.")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:cex_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=CXUO_NAME,
            factors=CX_MULTIVARIATE, responses=responses,
            n_runs=n_rsm, n_center_points=P.doe_centre_points(CXUO, "rsm"), scale_down_model="scale-down chromatography column",
            associated_parameters=[CXPARAM_CONCEPT[f] for f in CX_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "The response-surface study was a face-centred central "
                                   "composite design in the same four factors" if report
                                   else "The response surface study is a face centred central "
                                        "composite design in the 4 factors of the screening "
                                        "study")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:cex_sdm_qual", study_type="scale_down_qualification",
            unit_operation=CXUO_NAME, scale_down_model="scale-down chromatography column",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "Qualification of the model compared the small-scale "
                                   "system with the at-scale process on the attributes that "
                                   "enter and leave the step" if report
                                   else "Packing quality will be verified before each campaign "
                                        "by plate count and peak asymmetry")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:cex_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=CXUO_NAME,
            factors=CX_UNIVARIATE, responses=["step yield", "pool aggregate", "pool HCP"],
            associated_parameters=[CXPARAM_CONCEPT[f] for f in CX_UNIVARIATE],
            source_references=[ref(doc_id, file_name, "Study design", "Univariate assessment",
                                   "Elution flow rate was assessed one at a time" if report
                                   else "Elution flow rate will be assessed one factor at a "
                                        "time.")],
            metadata=meta()),
    ]


def cx_concepts():
    from annex_contract.concepts import Concept, ConceptStore
    cs = [Concept(concept_id="step:cex", concept_type="PROCESS_STEP",
                  canonical_name=CXUO_NAME,
                  aliases=["cation exchange", "CEX", "cation-exchange polishing", "Step 7"],
                  review_status="human_verified")]
    for name, cid in CXPARAM_CONCEPT.items():
        cs.append(Concept(concept_id=cid, concept_type="PROCESS_PARAMETER", canonical_name=name,
                          review_status="human_verified"))
    for key in CX_CQA_KEYS:
        cs.append(Concept(concept_id=CXATTR_CONCEPT[key], concept_type="QUALITY_ATTRIBUTE",
                          canonical_name=CXATTR_NAME[key], aliases=[key],
                          review_status="human_verified"))
    for mid, mname, *_ in CXMETHODS:
        cs.append(Concept(concept_id=f"method:{mid}", concept_type="ANALYTICAL_METHOD",
                          canonical_name=mname, aliases=[mid], review_status="human_verified"))
    return ConceptStore(run_id="gt-cex", concepts=cs)


def cx_assertions(doc_id, file_name, report):
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote, header=None):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote,
                                   table_header=header)],
            metadata=meta()))

    param_sec = "Factors, ranges and the knowledge space" if report else "Factors, ranges and study type"
    prow = param_rows(CXUO, report)   # the row that NAMES this parameter
    for name, cid in CXPARAM_CONCEPT.items():
        add("step:cex", "step_has_parameter", cid,
            f"{CXUO_NAME} has process parameter {name}.", param_sec, prow[name],
            prow.header)
    # The step SETS no CQA. Aggregate is the one it carries alone (no downstream step
    # reduces it); HCP, DNA and leached Protein A are cleared here and again downstream.
    add("step:cex", "step_has_quality_attribute", "attr:aggregates_hmw",
        f"{CXUO_NAME} is the last step in the train that reduces aggregate, so the "
        f"drug-substance aggregate content is set by what this step delivers.",
        "Quality attributes in scope",
        "cation exchange is the last step in the train that reduces the high molecular weight "
        "fraction, so no step after this one removes what this step leaves in the pool" if report
        else "no step downstream of cation exchange dissociates high molecular weight "
             "species, so the aggregate that leaves this step reaches the drug substance as "
             "aggregate")
    # Re-anchored 2026-08-19 onto the re-authored report. The old anchor was one clause
    # shared by all three records, which named none of them. §2.2 gives host cell protein a
    # sentence of its own and names residual DNA and leached Protein A together in the
    # sentence that says why neither was measured as a design response.
    cleared_quote = ({
        "hcp": ("Host cell protein is the second. It is cleared by three chromatography steps "
                "in series"),
        "residual_dna": ("Residual DNA and leached Protein A are cleared across the step but "
                         "were not measured as design responses"),
        "leached_protein_a": ("Residual DNA and leached Protein A are cleared across the step "
                              "but were not measured as design responses"),
    } if report else {
        "hcp": "host cell protein and DNA enter with the harvested cell culture fluid",
        "residual_dna": "host cell protein and DNA enter with the harvested cell culture fluid",
        "leached_protein_a": "leached Protein A is released from the capture resin",
    })
    for key in ["hcp", "residual_dna", "leached_protein_a"]:
        add("step:cex", "step_has_quality_attribute", CXATTR_CONCEPT[key],
            f"{CXUO_NAME} clears {CXATTR_NAME[key]} (formed upstream; not set here).",
            "Quality attributes in scope", cleared_quote[key])
    # attribute -> method (plan only; the report does not restate the linkage)
    if not report:
        for key in CX_CQA_METHOD:
            add(CXATTR_CONCEPT[key], "attribute_measured_by_method", f"method:{CX_CQA_METHOD[key]}",
                f"{CXATTR_NAME[key]} is measured by {CX_CQA_METHOD[key]}.", "Analytical methods",
                CXMETHOD_QUOTE[False][CX_CQA_METHOD[key]])
    # Acceptance criterion for aggregate — the one attribute whose drug-substance limit
    # binds at this step, because no later operation can correct it.
    agg = _cx_cqa_row("aggregates_hmw")
    # The assertion TEXT differs between the pair because the two documents say different
    # things. PCP-007 was re-authored on 2026-08-18 and now derives a pool criterion for
    # aggregate by carrying the drug-substance criterion through unchanged; PCR-007 has not been
    # re-authored in this round and keeps the wording that matches its own text. Leaving this
    # unconditional silently rewrote the PCR-007 annex, which is outside the batch.
    add("attr:aggregates_hmw", "attribute_has_acceptance_criterion", "lit:aggregates_hmw_acc",
        (f"Aggregate acceptance: {agg['acc_low']:g}–{agg['acc_high']:g} {agg['unit']} at drug "
         f"substance. No step downstream of cation exchange reduces the high molecular weight "
         f"fraction, so that criterion is also the ceiling at this pool, and the in-process "
         f"limit the study is judged against is derived from it by a safety factor." if report else
         f"Aggregate acceptance: {agg['acc_low']:g}–{agg['acc_high']:g} {agg['unit']} at drug "
         f"substance; no later step of the train reduces aggregate, so the pool criterion is "
         f"carried back from it."),
        "Proven acceptable ranges" if report else "Acceptance and decision criteria",
        "For aggregate no step downstream of cation exchange reduces the high molecular weight "
        "fraction, so the ceiling at this pool is the drug-substance criterion itself" if report
        else "For aggregate the in-process criterion is the tighter of the two")
    # parameter -> attribute impacts / non-impacts
    if report:
        add("param:cex_load", "parameter_impacts_attribute", "attr:aggregates_hmw",
            "Protein load carries the largest effect on the attributes this step clears and on "
            "step yield, and its proven acceptable range against aggregate is the one that "
            "constrains the design space (WC-CPP).",
            "Parameter classification",
            "It carries the largest effect on both cleared attributes and on step yield, and its "
            "proven acceptable range against aggregate is the one that constrains the design "
            "space")
        add("param:cex_wash_cond", "parameter_impacts_attribute", "attr:hcp",
            "Load and wash conductivity carries the largest effect on pool host cell protein and "
            "no effect on pool aggregate (WC-CPP).",
            "Parameter classification",
            "It carries the largest effect on pool host cell protein and no effect on aggregate")
        add("param:cex_elution_ph", "parameter_impacts_attribute", "attr:aggregates_hmw",
            "Elution buffer pH raises pool aggregate across its range and interacts with protein "
            "load in doing so (WC-CPP).",
            "Parameter classification",
            "It raises pool aggregate across its range and interacts with protein load in doing so")
        add("param:cex_stop_collect", "parameter_impacts_attribute", "attr:aggregates_hmw",
            "A later elution stop collect point raises pool aggregate across its range and "
            "recovers monomer at the same time (WC-CPP).",
            "Parameter classification",
            "A later stop point raises pool aggregate across its range and recovers monomer at "
            "the same time")
        add("param:cex_wash_cond", "parameter_does_not_significantly_impact_attribute",
            "attr:aggregates_hmw",
            "Load and wash conductivity had no detectable effect on pool aggregate; the null "
            "result is retained in the knowledge space.",
            "Screening: factor effects",
            "Load and wash conductivity had no detectable effect on aggregate")
        add("param:cex_flow", "parameter_does_not_significantly_impact_attribute",
            "attr:aggregates_hmw",
            "Elution flow rate showed no demonstrated effect across its characterization range, "
            "so it was not carried into the multivariate design and does not enter the design "
            "space (GPP).",
            "Univariate assessment",
            "Because flow rate carries no demonstrated effect, it was not carried into the "
            "multivariate design")
    else:
        for name in CX_MULTIVARIATE:
            add(CXPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:aggregates_hmw",
                f"{name} was ranked for multivariate study on its potential impact on the "
                f"attributes this step governs and on its potential to interact.",
                "Risk-based prioritization of parameters", prow[name], prow.header)
        add("param:cex_flow", "parameter_does_not_significantly_impact_attribute",
            "attr:aggregates_hmw",
            "Elution flow rate is expected to act through residence time and peak sharpness "
            "alone, neither of which is expected to interact with the other four parameters.",
            "Risk-based prioritization of parameters",
            "since it changes the residence time of the antibody in the pores of the resin "
            "rather than the strength with which the antibody binds the ligand")
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def cx_report_sections(doc_id, file_name, report):
    from annex_contract.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-007 states the studies that will establish the operating ranges of the "
                  "A-Mab cation exchange polishing step (Step 7), a Stage 1 process-design "
                  "activity.",
               "Purpose and scope",
               "This plan describes the Stage 1 characterization of the cation exchange "
               "chromatography step, which is Step 7 of the drug substance train"),
            st(2, "Five process parameters are characterized; four are assigned to the multivariate "
                  "design and the elution flow rate to univariate assessment.",
               "Risk-based prioritization of parameters",
               "Elution flow rate was assigned to a univariate assessment"),
            st(3, "The study uses a full-factorial screen followed by a face-centred central-composite "
                  "design on a scale-down column.",
               "Response-surface design",
               "The response surface study is a face centred central composite design in the 4 "
               "factors of the screening study"),
            # Re-anchored 2026-08-18. The re-authored plan calls the step the "aggregate polishing
            # step" and makes the clearance point through the attribute register rather than in one
            # sentence of the scope, so the statement is carried by the sentence that does the work:
            # aggregate cannot be recovered downstream.
            st(4, "Cation exchange is the aggregate polishing step of the train, and the aggregate "
                  "content of its pool sets the aggregate content of the drug substance.",
               "Acceptance and decision criteria",
               "the aggregate that leaves this step reaches the drug substance as aggregate"),
            # Rewritten 2026-08-18. The previous statement said pool aggregate is judged against the
            # DRUG-SUBSTANCE limit at this step. The re-authored plan gives aggregate a POOL
            # criterion too: it carries the drug-substance criterion through unchanged and leaves
            # the assurance margin to cover the whole difference. Both attributes now have a pool
            # criterion, derived two different ways, and the statement says so.
            st(5, "Both governed attributes are judged against a pool criterion rather than a "
                  "drug-substance criterion: host cell protein because anion exchange still "
                  "reduces it, aggregate because no later step does.",
               "Acceptance and decision criteria",
               "The in-process criterion is the level the eluate pool of this step must meet."),
            # Rewritten 2026-08-18. The previous statement said an above-limit pool "constrains
            # anion exchange and is reconciled in PCMR-001". The re-authored plan does not say
            # that -- it neither uses the word reconcile nor makes PCMR-001 the place the two steps
            # meet. What it does say about the host cell protein pool criterion is why the margin
            # is there, which is the claim the statement now carries.
            st(6, "Each in-process criterion is divided by a safety factor, which keeps the pool "
                  "inside the drug-substance criterion when a downstream step delivers less "
                  "clearance than it delivers at its set-point.",
               "Acceptance and decision criteria",
               "The safety factor keeps the pool inside the drug substance criterion where a "
               "downstream step delivers less clearance than it delivers at its set-point."),
            # Replaced 2026-08-18. The previous statement described a worst-case aggregate
            # challenge run separately from the designed experiments. The re-authored plan has no
            # such section and does not contain the word "worst" anywhere, so the statement is
            # replaced by the decision rule the plan does state for a model that fails.
            st(7, "A response whose model is not adequate is reported as characterized by its "
                  "data rather than by a model, and no design space and no proven acceptable "
                  "range are derived from it.",
               "Acceptance and decision criteria",
               "A response whose model is not adequate will be reported as characterized by its "
               "data rather than by a model"),
        ])]
    # Re-anchored and rewritten 2026-08-19 against the re-authored PCR-007. Every statement
    # below was read back against the new text: st1 dropped a KPP claim the report never makes,
    # st2 no longer says no other step changes aggregate (the new §8 says the bioreactor forms it
    # and the low-pH hold raises it, and that only this step reduces it), st6-st8 follow the new
    # in-process-limit framing of §7.1, and st9 now carries the commercial-scale capability
    # result rather than repeating st2.
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "No parameter at this step is a critical process parameter: the four quality-linked "
              "parameters are well-controlled critical process parameters, set or measured by "
              "instrumented systems, and the elution flow rate is a general process parameter.",
           "Parameter classification",
           "No parameter was classified as a critical process parameter. All four quality-linked "
           "parameters are set or measured by instrumented systems"),
        st(2, "Aggregate is reduced only at this step, so the aggregate capability of the drug "
              "substance rests on cation exchange in a way that the impurity capabilities, which "
              "are shared with other steps, do not.",
           "Process capability and robustness",
           "the aggregate capability of the drug substance rests on this step in a way that the "
           "impurity capabilities do not"),
        st(3, "Pool host cell protein is governed by the load and wash conductivity and by protein "
              "load, acting in opposite directions and through their interaction.",
           "Screening: factor effects",
           "Host cell protein levels were affected by load and wash conductivity and by protein "
           "load, in opposite directions, and a significant interaction between the two was "
           "identified"),
        st(4, "The pool aggregate and pool host cell protein response-surface models predict a "
              "withheld run about as well as they describe the runs they were fitted to, and both "
              "are used for prediction on that basis.",
           "Response-surface models",
           "which means the models predict a withheld run about as well as they describe the runs "
           "they were fitted to"),
        st(5, "No response shows significant curvature over the ranges studied: each response "
              "changes linearly with each parameter, the interactions carry the whole departure "
              "from additivity, and no edge of failure lies inside the characterized region.",
           "Mechanistic interpretation",
           "None of the four quadratic terms is significant in any of the three models. Over the "
           "ranges studied each response changes linearly with each parameter"),
        st(6, "The step yield model is not predictive and is used only to confirm the protein load "
              "effect, so no yield claim in the report depends on prediction.",
           "Discussion",
           "is used only to confirm the protein load effect, so no yield claim in this report "
           "depends on prediction"),
        st(7, "Pool host cell protein is judged against an in-process limit rather than the "
              "drug-substance criterion, because the pool is an intermediate that the anion "
              "exchange step reduces further.",
           "Proven acceptable ranges",
           "comparing the pool against the drug-substance criterion would report a failure that "
           "does not exist"),
        st(8, "Host cell protein, residual DNA and leached Protein A are cleared by Protein A "
              "capture, by this step and by anion exchange, and the ranges and controls the other "
              "two steps contribute are reported in PCR-005 and PCR-008.",
           "Contribution to the control strategy",
           "Host cell protein, residual DNA and leached Protein A are cleared by Protein A "
           "capture, by this step and by anion exchange, and the ranges and controls those steps "
           "contribute are in PCR-005 and PCR-008"),
        st(9, "At commercial scale the four attributes this step clears meet their drug-substance "
              "criteria, and host cell protein is the tightest of the four.",
           "Conclusions",
           "At commercial scale the four quality attributes this step clears meet their "
           "drug-substance criteria, the tightest among them being host cell protein"),
        st(10, "Both deviations recorded during execution were detected after the affected run, "
               "were investigated to a root cause and were dispositioned as retained.",
            "Deviations from the plan",
            "Both were detected after the affected run rather than during it, both were "
            "investigated to a root cause, and both were dispositioned as retained"),
    ])]


def cx_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:cex", unit_operation=CXUO_NAME,
        parameters=["param:cex_load", "param:cex_wash_cond", "param:cex_elution_ph",
                    "param:cex_stop_collect"],
        quality_attributes_constrained=["attr:aggregates_hmw", "attr:hcp"],
        definition="The part of the characterized four-dimensional region in protein load, "
                   "load/wash conductivity, elution buffer pH and the stop collect criterion in "
                   "which both governed attributes stay within their in-process limits. Aggregate "
                   "is the attribute that constrains it more, and the corner at which protein "
                   "load, elution buffer pH and the stop collect criterion sit together at the "
                   "unfavourable edge of their normal operating ranges lies outside the region: "
                   "the prediction there is below the drug-substance limit but above the "
                   "in-process limit, which is that limit divided by a safety factor because no "
                   "downstream step removes aggregate. Pool host cell protein is judged against a "
                   "limit carried back from the drug-substance criterion through the "
                   "anion-exchange clearance.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "The design space of this step is the region of the four "
                               "well-controlled critical process parameters over which pool "
                               "aggregate and pool host cell protein remain within their "
                               "in-process limits")],
        metadata=meta())]


# --------------------------------------------------------------------------- #
# Report-only PAR / discourse layers (PCR-007 only).                            #
# --------------------------------------------------------------------------- #
# proven_acceptable_ranges derive from the same DoE engine that renders @tbl-par  #
# (doe_report.par_table). Both responses are judged against the in-process limit   #
# of the step and not against the drug-substance criterion: §7.1 derives the host   #
# cell protein limit by carrying the drug-substance criterion back through the      #
# anion-exchange clearance and dividing by a safety factor, and the aggregate limit #
# by dividing the drug-substance criterion itself, because no later step reduces    #
# aggregate. Both therefore return an interval for every parameter, and protein     #
# load against aggregate is the range that binds. PCR-007 carries NO weak_claims.   #
# These layers are report-only; the plan omits them.                                #
# --------------------------------------------------------------------------- #
CX_PAR_SEC = "Proven acceptable ranges"


def _par_interval(value, unit):
    """A PAR cell with its parameter unit appended, when the cell is an interval.

    ``doe_report.par_table`` returns a range for a response the criterion admits and a short
    phrase ("none (...)") for one it does not, and a unit may only be appended to the first."""
    text = str(value)
    return f"{text} {unit}".strip() if unit and "–" in text else text


def cx_proven_acceptable_ranges(doc_id, file_name):
    """One ProvenAcceptableRange per governed response x response-surface parameter, from the
    same DoE engine (``doe_report.par_table``) that renders @tbl-par in the report. The
    acceptance basis is read back from the engine by ``par_basis_text``, so it states the
    criterion the interval was actually computed against: for this step that is the in-process
    limit of each response, which §7.1 of the report derives from the drug-substance criterion.
    Both responses return an interval for every parameter on that basis."""
    import doe_report as D
    par = D.par_table(CXUO)
    out = []
    # Each attribute x parameter combination on its own @tbl-par row: the
    # per-attribute prose said which attribute was governed, never which
    # parameter's range was proven.
    rows = par_rows(CXUO)
    for i, r in enumerate(par.to_dict("records"), 1):
        cqa, param, unit = r["CQA"], r["Parameter"], (r["Unit"] or "")
        char = f"{r['Char. range']} {unit}".strip()
        # The unit belongs to the PARAMETER, so it is appended to any interval the engine
        # returns. It used to be dropped for pool HCP, back when that response returned no
        # interval at all against the drug-substance criterion; against the in-process limit
        # of §7.1 it returns a range like every other row, and the range needs its unit.
        out.append(S.ProvenAcceptableRange(
            par_id=f"{doc_id}-PAR{i:02d}", unit_operation=CXUO_NAME,
            quality_attribute=cqa, parameter=param,
            characterization_range=char,
            par_at_setpoint=_par_interval(r["PAR (set-point)"], unit),
            par_nor_propagated=_par_interval(r["PAR (NOR)"], unit),
            acceptance_basis=par_basis_text(CXUO, cqa),
            source_references=[ref(doc_id, file_name, f"{doc_id}_sec_par", CX_PAR_SEC,
                                   rows[(cqa, param)],
                                   table_id=f"{doc_id}_tab_par",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


def cx_inventory(doc_id, file_name, dtype):
    return S.DocumentInventoryItem(
        document_id=doc_id, file_name=file_name, predicted_document_type=dtype,
        product_name_candidates=["A-Mab"], process_name_candidates=[CXUO_NAME],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "cation-exchange chromatography", "aggregate clearance",
                     "host-cell protein clearance", "design of experiments", "parameter classification"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc_id][0]}'.",
        source_references=[ref(doc_id, file_name, "Title block", "Title block",
                               title_block_quote(doc_id))],
        metadata=meta())


def build_plan_cex():
    doc, f = "PCP-007", PCP7_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_uo",
                                  process_steps=[cx_step(doc, f, f"{doc}_sec_uo", report=False)],
                                  equipment=cx_equipment(doc, f, f"{doc}_sec_uo", report=False),
                                  sites=cx_sites(doc, f, f"{doc}_sec_uo")),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=cx_cqas(doc, f, f"{doc}_sec_cqa", report=False)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=cx_params(doc, f, f"{doc}_sec_param", classified=False)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=cx_methods(doc, f, f"{doc}_sec_methods", report=False)),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "CEX sets no CQA; the QualityAttribute entities are the CQAs it controls/clears (formed upstream).",
            "Pool aggregate and pool HCP are in-process responses with no released spec; captured via StudyDesign.responses. Aggregate is nonetheless judged against the DS limit here, because no downstream step reduces it.",
            "Pool HCP carries a second, step-level criterion (clearance factor) alongside the DS limit, because three steps deliver that limit together; the reconciliation is deferred to PCMR-001.",
            "The Plan states classification is an OUTPUT; parameter_type left 'unclassified' here.",
        ],
        inventory=cx_inventory(doc, f, "process_characterization_plan"),
        entities=entities,
        studies=cx_studies(doc, f, report=False),
        report_sections=cx_report_sections(doc, f, report=False),
        assertions=cx_assertions(doc, f, report=False), concepts=cx_concepts())


def build_report_cex():
    doc, f = "PCR-007", PCR7_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_exec",
                                  process_steps=[cx_step(doc, f, f"{doc}_sec_exec", report=True)],
                                  equipment=cx_equipment(doc, f, f"{doc}_sec_exec", report=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=cx_params(doc, f, f"{doc}_sec_param", classified=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=cx_cqas(doc, f, f"{doc}_sec_cqa", report=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=cx_methods(doc, f, f"{doc}_sec_methods", report=True)),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT + [
            "ProvenAcceptableRange (new model) — per-response x parameter PAR (at-set-point / NOR-propagated); both responses use a drug-substance specification as the acceptance basis",
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "CEX sets no CQA; the QualityAttribute entities are the CQAs it controls/clears (formed upstream).",
            "Pool aggregate and pool HCP are in-process responses with no released spec; reported via studies/report_sections. Both are judged against an in-process limit derived in §7.1, not against the DS criterion: for HCP the DS criterion is carried back through the AEX clearance and divided by a safety factor, for aggregate the DS criterion is the pool ceiling itself (no later step reduces it) and is divided by a larger safety factor.",
            "Pool HCP above the DS criterion is the expected result for an intermediate and is not a failed acceptance criterion. Against the in-process limit the PAR analysis returns an interval for every parameter. The further AEX clearance is credited to PCR-008 and the cumulative position across the train to PCMR-001.",
            "No response shows significant curvature, and the step-yield model is direction-only (predicted R^2 0.20); the two attribute models carry every prediction.",
            "Process-capability (Cpk) values have no dedicated field; reported as report_sections statements.",
            "proven_acceptable_ranges mirror @tbl-par (doe_report.par_table); rhetorical_spans are verbatim report prose; PCR-007 carries no weak_claims.",
        ],
        inventory=cx_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=cx_studies(doc, f, report=True),
        design_spaces=cx_design_spaces(doc, f),
        proven_acceptable_ranges=cx_proven_acceptable_ranges(doc, f),
        report_sections=cx_report_sections(doc, f, report=True),
        assertions=cx_assertions(doc, f, report=True), concepts=cx_concepts(),
        rhetorical_spans=build_rhetorical_spans(doc, f))


# =========================================================================== #
# Anion Exchange Chromatography (Step 8) — PCP-008 / PCR-008.                   #
# --------------------------------------------------------------------------- #
# Additive, self-contained builders for the AEX flow-through polishing DoE      #
# pair. Unlike CEX, AEX SETS one CQA of its own — the cumulative MVM             #
# (parvovirus) clearance claim — and is a major clearance step for enveloped    #
# virus (XMuLV), HCP, residual DNA and leached Protein A. The DoE is a           #
# four-factor full-factorial screen + face-centred CCD in load-pH /             #
# wash1-conductivity / load-conductivity / load; the operating flow rate is a    #
# univariate WC-CPP (bounded by the conditions at which clearance was            #
# demonstrated). All five parameters are WC-CPP; protein load and flow rate are  #
# null results retained in the knowledge space. Three deviations are documented  #
# in the report (DEV-008-01 non-representative deamidated load → both designs     #
# invalidated and re-executed; DEV-008-02 descending-edge UV collection set-point #
# corrected by modelling + verification runs; DEV-008-03 wash-buffer pH excursion #
# retained); the annex captures the DoE-grounded entities of the requalified      #
# execution.                                                                     #
# =========================================================================== #
AXUO = "aex"
AXUO_NAME = P.CFG.unit_op(AXUO).name             # "Anion Exchange Chromatography"
AXSTEP = P.CFG.unit_op(AXUO).step                # 8
AXSTEP_LABEL = f"{AXUO_NAME} (Step {AXSTEP})"

PCP8_FILE = "PCP-008_aex.docx"
PCR8_FILE = "PCR-008_aex.docx"

AXPARAM_ROWS = P.param_reg[P.param_reg.unit_operation == AXUO_NAME].to_dict("records")
AXPARAM_CONCEPT = {
    "Load pH": "param:aex_load_ph",
    "Equil/Wash-1 conductivity": "param:aex_wash1_cond",
    "Load conductivity": "param:aex_load_cond",
    "Protein load": "param:aex_load",
    "Operating flow rate": "param:aex_flow",
}
# The four DoE factors (WC-CPP, multivariate) vs the univariate WC-CPP flow rate.
AX_MULTIVARIATE = ["Load pH", "Equil/Wash-1 conductivity", "Load conductivity", "Protein load"]
AX_UNIVARIATE = ["Operating flow rate"]
AX_HCP_DRIVERS = ["Load pH", "Equil/Wash-1 conductivity"]     # -> flow-through-pool HCP
AX_VIRAL_DRIVERS = ["Load pH", "Load conductivity"]           # -> XMuLV / MVM log-reduction

# AEX sets lrv_mvm; it controls/clears the others. MVM first (the CQA it sets).
AX_CQA_KEYS = ["lrv_mvm", "lrv_xmulv", "hcp", "residual_dna", "leached_protein_a"]
AXATTR_CONCEPT = {
    "lrv_mvm": "attr:lrv_mvm", "lrv_xmulv": "attr:lrv_xmulv", "hcp": "attr:hcp",
    "residual_dna": "attr:residual_dna", "leached_protein_a": "attr:leached_protein_a",
}
AXATTR_NAME = {
    "lrv_mvm": "Viral clearance — MVM (parvovirus)",
    "lrv_xmulv": "Viral clearance — XMuLV (enveloped)",
    "hcp": "Host Cell Protein (HCP)", "residual_dna": "Residual DNA",
    "leached_protein_a": "Leached Protein A",
}
AX_CQA_METHOD = {"lrv_mvm": "AMV-3018", "lrv_xmulv": "AMV-3017", "hcp": "AMV-3012",
                 "residual_dna": "AMV-3014", "leached_protein_a": "AMV-3016"}
AXMETHODS = [
    ("AMV-3012", "Host-Cell Protein ELISA", "immunoassay", ["host-cell protein"], ["hcp"]),
    ("AMV-3014", "Residual DNA (qPCR)", "qPCR", ["residual host-cell DNA"], ["residual_dna"]),
    ("AMV-3016", "Leached Protein A by ELISA (ppm)", "immunoassay",
     ["leached Protein A"], ["leached_protein_a"]),
    ("AMV-3017", "XMuLV Infectivity Titre (TCID50)", "infectivity_assay",
     ["XMuLV infectious titre"], ["lrv_xmulv"]),
    ("AMV-3018", "MVM Infectivity Titre (TCID50/qPCR)", "infectivity_assay",
     ["MVM infectious titre"], ["lrv_mvm"]),
]


def _ax_cqa_row(key):
    return P.cqa_reg[P.cqa_reg.key == key].iloc[0].to_dict()


def ax_step(doc_id, file_name, sec, report):
    if report:
        src = ref(doc_id, file_name, sec, "Executive summary",
                  "Anion exchange is Step 8 and the last chromatographic step of the train.")
    else:
        src = ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                  "This plan defines the Stage 1 process characterization study for the anion exchange chromatography step of the A-Mab drug substance process, Step 8 of the purification train.")
    return S.ProcessStep(
        step_id="step:aex", step_name=AXUO_NAME, step_number=str(AXSTEP),
        unit_operation=AXUO_NAME,
        description="Flow-through anion-exchange polishing: the final chromatographic step of "
                    "the process. Sets the cumulative MVM (parvovirus) viral-clearance claim and "
                    "is a major clearance step for enveloped virus (XMuLV), HCP, residual DNA and "
                    "leached Protein A. The product transmits while impurities and virus bind.",
        input_materials=["cation-exchange eluate pool (anion-exchange feed)"],
        output_materials=["anion-exchange flow-through pool (virus-filtration feed)"],
        equipment=["anion-exchange column", "scale-down chromatography column"],
        source_references=[src], metadata=meta())


def ax_equipment(doc_id, file_name, sec, report):
    sdm = S.Equipment(
        equipment_id="equip:aex_sdm_column", equipment_name="scale-down chromatography column",
        equipment_type="chromatography column (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Scale-down model and its qualification",
                               "The model was qualified under SOP-1001 by operating it at the commercial set-points and comparing its input and output attributes with the corresponding at-scale data" if report
                               else "The study will be executed on a scale-down model of the commercial anion exchange column, qualified under SOP-1001.")],
        metadata=meta())
    if report:
        return [sdm]
    return [
        S.Equipment(equipment_id="equip:aex_column",
                    equipment_name="commercial-scale anion-exchange polishing column",
                    equipment_type="chromatography column", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec,
                                           "Scale-down model and its qualification",
                                           "the commercial anion exchange column")],
                    metadata=meta()),
        sdm,
    ]


def ax_sites(doc_id, file_name, sec):
    return [
        S.ManufacturingSite(site_id="site:cambridge", site_name=P.SENDING_SITE, site_role="sending",
                            location="Cambridge, MA",
                            source_references=[ref(doc_id, file_name, sec, "Title block",
                                                   "Cambridge, MA (Development)")],
                            metadata=meta()),
        S.ManufacturingSite(site_id="site:grafton", site_name=P.RECEIVING_SITE, site_role="receiving",
                            location="Grafton, WI",
                            source_references=[ref(doc_id, file_name, sec, "Title block",
                                                   "Grafton, WI (Commercial DS)")],
                            metadata=meta()),
    ]


def ax_params(doc_id, file_name, sec, classified):
    caption = ("Characterized process parameters, ranges studied and final classification."
               if classified else
               "Parameters to be studied, with set-points, characterization ranges, normal "
               "operating ranges and study type.")
    rats = {"WC-CPP": "Every parameter of the step changes either the charge of the bound "
                      "species or the ionic strength that screens it, and both changes move the "
                      "clearance of a very high criticality attribute. It is designated well "
                      "controlled because the control capability of the equipment is tighter "
                      "than the range, so the risk of falling outside the design space is low."}
    out = []
    rows = param_rows(AXUO, classified)   # each parameter on its own @tbl-params row
    for r in AXPARAM_ROWS:
        name = r["parameter"]
        ptype = r["classification"] if classified else "unclassified"
        out.append(S.ProcessParameter(
            parameter_id=AXPARAM_CONCEPT[name], parameter_name=name, parameter_type=ptype,
            unit=r["unit"], target_value=f"{r['setpoint']:g}",
            NOR=f"{r['nor_low']:g}–{r['nor_high']:g} {r['unit']}",
            PAR=f"{r['par_low']:g}–{r['par_high']:g} {r['unit']}",
            associated_step=AXSTEP_LABEL,
            rationale_for_criticality=rats.get(r["classification"]) if classified else None,
            source_references=[ref(doc_id, file_name, sec,
                                   "Factors, ranges and the knowledge space" if classified
                                   else "Factors, ranges and study type",
                                   rows[name], table_title=caption,
                                   table_id=f"{doc_id}_tab_params",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


# Both documents split the CQAs across two tables: the one attribute the step SETS
# (cumulative MVM clearance) and the attributes it clears but does not set. Each CQA
# is anchored on the caption of the table that carries it.
AX_CQA_SET_CAPTION = {
    True: "Critical quality attribute set by the anion exchange step.",
    False: "Critical quality attribute set by the anion exchange step.",
}
AX_CQA_CLEARED_CAPTION = {
    True: "Quality attributes cleared but not set by the anion exchange step.",
    False: "Quality attributes governed or cleared by this step.",
}


def ax_cqas(doc_id, file_name, sec, report):
    out = []
    rows = cqa_rows(AX_CQA_KEYS)   # each attribute on its own @tbl-cqa row
    for key in AX_CQA_KEYS:
        r = _ax_cqa_row(key)
        sets_it = key == "lrv_mvm"
        caption = (AX_CQA_SET_CAPTION if sets_it else AX_CQA_CLEARED_CAPTION)[report]
        out.append(S.QualityAttribute(
            attribute_id=AXATTR_CONCEPT[key], attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"],
            acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            analytical_method=None if report else AX_CQA_METHOD[key],
            associated_steps=[AXSTEP_LABEL],
            rationale_for_criticality=f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = {r['tool1_score']}.",
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref(doc_id, file_name, sec, "Quality attributes in scope",
                                   rows[key], table_title=caption,
                                   table_id=f"{doc_id}_tab_cqa_set" if sets_it
                                   else f"{doc_id}_tab_cqa_cleared",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


# Per-method grounded fragment from each document's "Analytical methods" section.
AXMETHOD_QUOTE = {
    False: {  # PCP-008
        "AMV-3012": "Pool host cell protein will be measured by ELISA (AMV-3012)",
        "AMV-3014": "Residual DNA will be measured by qPCR (AMV-3014)",
        "AMV-3016": "leached Protein A by ELISA (AMV-3016)",
        # Both viral methods are named in one sentence; each takes the shortest contiguous
        # slice of it that names itself (see CQA_METHOD_QUOTE for the same treatment).
        "AMV-3017": ("Infectivity of xenotropic murine leukaemia virus will be measured by TCID50 (AMV-3017)"),
        "AMV-3018": "infectivity of minute virus of mice by TCID50 with a qPCR confirmation (AMV-3018)",
    },
    True: {  # PCR-008
        "AMV-3012": "Pool host cell protein was measured by the host cell protein enzyme-linked immunosorbent assay AMV-3012.",
        "AMV-3014": "residual DNA and leached Protein A are measured under AMV-3014 and AMV-3016",
        "AMV-3016": "Leached Protein A is acidic and binds the ligand while the antibody passes through",
        # Both viral methods are named in one sentence; each takes the shortest contiguous
        # slice of it that names itself, as the plan branch above does.
        "AMV-3017": "XMuLV and MVM titres were measured by infectivity assay under AMV-3017 and AMV-3018",
        "AMV-3018": "XMuLV and MVM titres were measured on the load and on the pool of every run",
    },
}


def ax_methods(doc_id, file_name, sec, report):
    quotes = AXMETHOD_QUOTE[report]
    out = []
    for mid, mname, mtype, analytes, attrs in AXMETHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[AXATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods", quotes[mid])],
            metadata=meta()))
    return out


def ax_studies(doc_id, file_name, report):
    sec = "Study design"
    n_scr, n_rsm = P.doe_runs(AXUO, "screening"), P.doe_runs(AXUO, "rsm")
    responses = ["hcp_out_ng_mg", "xmulv_lrf", "mvm_lrf", "step_yield"]
    return [
        S.StudyDesign(
            study_id="study:aex_screening", study_type="screening_doe",
            design_name="two-level full factorial", unit_operation=AXUO_NAME,
            factors=AX_MULTIVARIATE, responses=responses,
            n_runs=n_scr, n_center_points=P.doe_centre_points(AXUO, "screening"), scale_down_model="scale-down chromatography column",
            associated_parameters=[AXPARAM_CONCEPT[f] for f in AX_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Screening design",
                                   "In a full factorial no main effect is aliased with a two-factor interaction and every two-factor interaction is estimated in its own right" if report
                                   else "A full factorial in these parameters estimates every main effect and every two-factor interaction without confounding")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:aex_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=AXUO_NAME,
            factors=AX_MULTIVARIATE, responses=responses,
            n_runs=n_rsm, n_center_points=P.doe_centre_points(AXUO, "rsm"), scale_down_model="scale-down chromatography column",
            associated_parameters=[AXPARAM_CONCEPT[f] for f in AX_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "The axial points sit on the faces of the coded cube and not outside it, so every run of the design is inside the characterization ranges of Table 6" if report
                                   else "The same parameters will be studied in a face-centred central composite design of 28 runs.")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:aex_sdm_qual", study_type="scale_down_qualification",
            unit_operation=AXUO_NAME, scale_down_model="scale-down chromatography column",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "The model was qualified under SOP-1001 by operating it at the commercial set-points and comparing its input and output attributes with the corresponding at-scale data"
                                   if report
                                   else "Qualification will compare the model against commercial-equivalent runs on step yield, pool host cell protein, residual DNA, leached Protein A, the pressure across the bed and the shape of the flow-through peak.")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:aex_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=AXUO_NAME,
            factors=AX_UNIVARIATE,
            responses=["flow-through-pool HCP", "XMuLV log-reduction", "MVM log-reduction", "step yield"],
            associated_parameters=[AXPARAM_CONCEPT[f] for f in AX_UNIVARIATE],
            source_references=[ref(doc_id, file_name, "Study design", "Univariate assessment",
                                   "Operating flow rate was assessed one factor at a time and was not a factor of either design"
                                   if report
                                   else "Operating flow rate was assigned to a univariate assessment")],
            metadata=meta()),
    ]


def ax_concepts():
    from annex_contract.concepts import Concept, ConceptStore
    cs = [Concept(concept_id="step:aex", concept_type="PROCESS_STEP",
                  canonical_name=AXUO_NAME,
                  aliases=["anion exchange", "AEX", "anion-exchange polishing",
                           "flow-through polish", "Step 8"],
                  review_status="human_verified")]
    for name, cid in AXPARAM_CONCEPT.items():
        cs.append(Concept(concept_id=cid, concept_type="PROCESS_PARAMETER", canonical_name=name,
                          review_status="human_verified"))
    for key in AX_CQA_KEYS:
        cs.append(Concept(concept_id=AXATTR_CONCEPT[key], concept_type="QUALITY_ATTRIBUTE",
                          canonical_name=AXATTR_NAME[key], aliases=[key],
                          review_status="human_verified"))
    for mid, mname, *_ in AXMETHODS:
        cs.append(Concept(concept_id=f"method:{mid}", concept_type="ANALYTICAL_METHOD",
                          canonical_name=mname, aliases=[mid], review_status="human_verified"))
    return ConceptStore(run_id="gt-aex", concepts=cs)


def ax_assertions(doc_id, file_name, report):
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote, header=None):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote,
                                   table_header=header)],
            metadata=meta()))

    param_sec = "Factors, ranges and the knowledge space" if report else "Factors, ranges and study type"
    prow = param_rows(AXUO, report)   # the row that NAMES this parameter
    for name, cid in AXPARAM_CONCEPT.items():
        add("step:aex", "step_has_parameter", cid,
            f"{AXUO_NAME} has process parameter {name}.", param_sec, prow[name],
            prow.header)
    # step sets the MVM clearance CQA; clears XMuLV, HCP, DNA and leached Protein A
    add("step:aex", "step_has_quality_attribute", "attr:lrv_mvm",
        f"{AXUO_NAME} sets the cumulative MVM (parvovirus) clearance claim.",
        "Product and unit operation" if report else "Quality attributes in scope",
        "It is the cumulative clearance of MVM, the non-enveloped model virus" if report
        else "The step sets one critical quality attribute")
    # Each cleared attribute on its own row of the cleared-attribute table. The sentence that
    # says the step clears four attributes names none of them.
    crow = cqa_rows(AX_CQA_KEYS)
    for key in ["lrv_xmulv", "hcp", "residual_dna", "leached_protein_a"]:
        add("step:aex", "step_has_quality_attribute", AXATTR_CONCEPT[key],
            f"{AXUO_NAME} clears {AXATTR_NAME[key]}.", "Quality attributes in scope",
            crow[key], crow.header)
    # attribute -> method (plan only; the report does not restate the linkage)
    if not report:
        for key in AX_CQA_METHOD:
            add(AXATTR_CONCEPT[key], "attribute_measured_by_method", f"method:{AX_CQA_METHOD[key]}",
                f"{AXATTR_NAME[key]} is measured by {AX_CQA_METHOD[key]}.", "Analytical methods",
                AXMETHOD_QUOTE[False][AX_CQA_METHOD[key]])
    # acceptance criterion for the CQA the step sets
    mvm = _ax_cqa_row("lrv_mvm")
    add("attr:lrv_mvm", "attribute_has_acceptance_criterion", "lit:lrv_mvm_acc",
        f"MVM clearance acceptance: ≥ {mvm['acc_low']:g} {mvm['unit']}.",
        "Quality attributes in scope",
        "it is a very high criticality attribute of the viral safety category" if report
        else "Critical quality attribute set by the anion exchange step.")
    # parameter -> attribute relations. In the requalified execution only the three
    # chemistry parameters are active; protein load and flow rate are null results and
    # are WC-CPP on bounding logic, so they carry a "does not significantly impact" edge.
    if report:
        add("param:aex_load_ph", "parameter_impacts_attribute", "attr:lrv_mvm",
            "Load pH carries the largest effect on both viral-clearance responses and the largest "
            "effect on host cell protein clearance, and it sets the position of the binding "
            "equilibrium for every bound species (WC-CPP).",
            "Parameter classification",
            "Load pH changes the charge carried by the acidic host cell proteins and by the virus particles, and it has the largest main effect on pool host cell protein and on both log reduction factors.")
        add("param:aex_wash1_cond", "parameter_impacts_attribute", "attr:hcp",
            "Equil/Wash-1 conductivity carries the largest effect on pool HCP and interacts with "
            "load pH; it is the only parameter whose normal operating range extends past the "
            "range the robustness analysis supports (WC-CPP).",
            "Parameter classification",
            "The equilibration and wash-1 conductivity has the largest effect on pool host cell protein of any parameter studied and is the parameter that bounds the operating region.")
        add("param:aex_load_cond", "parameter_impacts_attribute", "attr:lrv_mvm",
            "Load conductivity carries a significant effect on the clearance of both model "
            "viruses and no effect on host cell protein clearance (WC-CPP).",
            "Parameter classification",
            "It was classified as a well-controlled critical process parameter, because the conductivity of the load is fixed by the cation exchange eluate and its adjustment")
        add("param:aex_load", "parameter_does_not_significantly_impact_attribute", "attr:hcp",
            "Protein load had no demonstrated effect on any response over the characterized "
            "range, because the impurity mass reaching the ligand stays far below the capacity of "
            "the bed; it is classified WC-CPP because the mass of impurity delivered to the "
            "ligand rises with it, not because an effect was measured.",
            "Mechanistic interpretation",
            "Within the range studied here the impurity mass carried onto the column is far below the ligand capacity, so protein load was expected to have little effect.")
        add("param:aex_flow", "parameter_does_not_significantly_impact_attribute", "attr:lrv_mvm",
            "Operating flow rate showed no effect over the range studied in the univariate "
            "assessment; it is classified WC-CPP because flow is set and recorded by the "
            "chromatography skid and its range is wide relative to the control capability of the "
            "equipment.",
            "Parameter classification",
            "It was classified as a well-controlled critical process parameter on the basis of the univariate assessment")
    else:
        for name in AX_MULTIVARIATE:
            add(AXPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:hcp",
                f"{name} was ranked for multivariate study on its potential impact on a CQA and "
                f"its potential to interact with other parameters.",
                "Risk-based prioritization of parameters", prow[name], prow.header)
        add("param:aex_flow", "parameter_impacts_attribute", "attr:lrv_mvm",
            "Operating flow rate acts on this step through residence time and is assessed "
            "univariately.",
            "Univariate assessment",
            "binding of the small, highly charged impurities is fast relative to the residence time at every flow rate in the range")
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def ax_report_sections(doc_id, file_name, report):
    from annex_contract.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-008 defines the process characterization study for the A-Mab anion-exchange polishing step (Step 8).",
               "Purpose and scope",
               "Purpose and scope This plan defines the Stage 1 process characterization study for the anion exchange chromatography step"),
            st(2, "Five process parameters are characterized; four are studied in the multivariate DoE and the flow rate univariately.",
               "Factors, ranges and study type",
               "Table 7 lists the parameters, their set-points, the range that will be studied, the normal operating range and the study type assigned in RA-001."),
            st(3, "The study uses a full-factorial screen followed by a face-centred central-composite design on a scale-down column.",
               "Response-surface design", "The same parameters will be studied in a face-centred central composite design of 28 runs."),
            st(4, "Anion exchange sets the cumulative parvovirus (MVM) clearance claim and also governs XMuLV clearance, HCP, residual DNA and leached Protein A.",
               "Quality attributes in scope", "The step sets one critical quality attribute"),
            st(5, "The study must establish a multivariate operating region over which every governed response is predicted to stay within its acceptance criterion.",
               "Acceptance and decision criteria",
               "The multivariate operating region will be declared over the part of the characterized region in which every governed response meets its criterion simultaneously."),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Every characterized parameter is classified as a well controlled critical process "
              "parameter; the step has no CPP requiring a narrower control than the equipment "
              "already provides, and no KPP and no GPP.",
           "Parameter classification",
           "All 5 parameters of this step are therefore well-controlled critical process parameters and none is a critical process parameter."),
        st(2, "Anion exchange and virus filtration are the only two steps credited with MVM "
              "clearance.",
           "Executive summary",
           "The tightest capability in the drug substance is the cumulative MVM clearance, at Cpk 1.51, and this step is one of the two that carry it."),
        st(3, "Pool HCP is governed by the equilibration and wash conductivity and by load pH "
              "acting in opposite directions, together with a significant interaction between "
              "them.",
           "Screening factor effects",
           "Load pH and the equilibration and wash-1 conductivity carry the response, at -5.34 and 6.19 ng/mg per half range"),
        st(4, "The response-surface models — not the screening models — are the predictive models "
              "behind every prediction, the design space and the proven acceptable ranges.",
           "Response-surface design",
           "Every prediction, every proven acceptable range and every statement about the operating region is taken from the response-surface models and not from the screening fits."),
        st(5, "The protein load by wash-conductivity interaction seen in the invalidated first "
              "execution is indistinguishable from zero in the requalified data, which confirms "
              "the DEV-008-01 root cause.",
           "DEV-008-01, non-representative load in the first execution",
           "The requalified data confirm the root cause."),
        st(6, "Three deviations were recorded, investigated and dispositioned; the one that "
              "invalidated the first execution of both designs was resolved by re-executing them "
              "in full on a requalified load.",
           "Conclusions",
           "One of them invalidated the first execution of both designs and forced a full re-execution on requalified material."),
        st(7, "Cumulative MVM clearance carries the tightest process-capability index of any "
              "attribute in the drug substance.",
           "Process capability and robustness",
           "The tightest capability in the drug substance is the cumulative MVM clearance, at Cpk 1.51"),
        st(8, "The normal operating ranges are not entirely inside the design space: the corner "
              "combining the bottom of the load pH range with the top of the equilibration and "
              "wash conductivity range exceeds the in-process limit for pool HCP.",
           "Design space",
           "The normal operating ranges of Table 6 sit inside the characterized region on every axis."),
    ])]


def ax_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:aex", unit_operation=AXUO_NAME,
        parameters=["param:aex_load_ph", "param:aex_load_cond", "param:aex_wash1_cond"],
        quality_attributes_constrained=["attr:lrv_mvm", "attr:lrv_xmulv", "attr:hcp"],
        definition="The region of the characterized parameters over which the fitted "
                   "response-surface models predict that pool HCP, XMuLV clearance and MVM "
                   "clearance all meet their criteria. Pool HCP is the only response that "
                   "constrains it: the rejected part of the characterized region is the corner "
                   "that combines low load pH with high equilibration and wash-1 conductivity, "
                   "and both viral responses meet their criteria everywhere inside the "
                   "characterized ranges. Protein load imposes no boundary on any plane, and the "
                   "principal plane of the region is load pH against equilibration/wash-1 "
                   "conductivity. The normal operating ranges are not entirely inside the region: "
                   "at the same corner, with load pH at the bottom of its range and "
                   "equilibration/wash-1 conductivity at the top of its own, the predicted pool "
                   "HCP exceeds the in-process limit.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "The design space of this step is the part of the characterized region in which every criterion of §3.5 is met.")],
        metadata=meta())]


# --------------------------------------------------------------------------- #
# Report-only discourse / PAR layers (PCR-008 only).                            #
# --------------------------------------------------------------------------- #
# proven_acceptable_ranges derive from the same DoE engine that renders @tbl-par #
# (doe_report.par_table); rhetorical_spans annotate the report's argument         #
# structure. Both quote verbatim, plain-prose fragments of the rendered report.   #
# PCR-008 carries NO weak_claims. These layers are report-only (the plan omits    #
# them); the plan-side builders above are untouched.                              #
# --------------------------------------------------------------------------- #
AX_PAR_SEC = "Proven acceptable ranges"
# Per-CQA grounded fragment from the report's Proven-acceptable-ranges section.
AX_PAR_CQA_QUOTE = {
    "Pool HCP (ng/mg)": ("for pool HCP the criterion is the drug substance specification, which is "
                         "applied directly to the pool because no later step clears HCP"),
    "XMuLV LRF (log₁₀)": ("whereas for the two viral clearance responses the criterion is the step "
                          "contribution back-calculated from the cumulative requirement"),
    "MVM LRF (log₁₀)": ("whereas for the two viral clearance responses the criterion is the step "
                        "contribution back-calculated from the cumulative requirement"),
}
_AX_PAR_GENERAL_QUOTE = ("Neither viral attribute is restricted anywhere")


def ax_proven_acceptable_ranges(doc_id, file_name):
    """One ProvenAcceptableRange per governed CQA x response-surface parameter, from the
    same DoE engine (``doe_report.par_table``) that renders @tbl-par in the report. Pool HCP
    uses the drug-substance specification as its ceiling; the two viral-clearance CQAs use a
    back-calculated step floor (the modular required log-reduction) as the acceptance basis."""
    import doe_report as D
    par = D.par_table(AXUO)
    out = []
    # Each attribute x parameter combination on its own @tbl-par row: the
    # per-attribute prose said which attribute was governed, never which
    # parameter's range was proven.
    rows = par_rows(AXUO)
    for i, r in enumerate(par.to_dict("records"), 1):
        cqa, param, unit = r["CQA"], r["Parameter"], (r["Unit"] or "")
        char = f"{r['Char. range']} {unit}".strip()
        viral = "LRF" in cqa
        basis = (
            "Step-level required log-reduction, back-calculated from the cumulative viral-clearance "
            "requirement minus the clearance credited to the other orthogonal steps (modular "
            "viral-safety claim under ICH Q5A(R2))."
            if viral else
            "Drug-substance host-cell-protein specification, applied as the upper (ceiling) "
            "acceptance limit.")
        out.append(S.ProvenAcceptableRange(
            par_id=f"{doc_id}-PAR{i:02d}", unit_operation=AXUO_NAME,
            quality_attribute=cqa, parameter=param,
            characterization_range=char,
            par_at_setpoint=f"{r['PAR (set-point)']} {unit}".strip(),
            par_nor_propagated=f"{r['PAR (NOR)']} {unit}".strip(),
            acceptance_basis=par_basis_text(AXUO, cqa),
            source_references=[ref(doc_id, file_name, f"{doc_id}_sec_par", AX_PAR_SEC,
                                   rows[(cqa, param)],
                                   table_id=f"{doc_id}_tab_par",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


def ax_inventory(doc_id, file_name, dtype):
    return S.DocumentInventoryItem(
        document_id=doc_id, file_name=file_name, predicted_document_type=dtype,
        product_name_candidates=["A-Mab"], process_name_candidates=[AXUO_NAME],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "anion-exchange chromatography", "viral clearance",
                     "host-cell protein clearance", "design of experiments", "parameter classification"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc_id][0]}'.",
        source_references=[ref(doc_id, file_name, "Title block", "Title block",
                               title_block_quote(doc_id))],
        metadata=meta())


def build_plan_aex():
    doc, f = "PCP-008", PCP8_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_uo",
                                  process_steps=[ax_step(doc, f, f"{doc}_sec_uo", report=False)],
                                  equipment=ax_equipment(doc, f, f"{doc}_sec_uo", report=False),
                                  sites=ax_sites(doc, f, f"{doc}_sec_uo")),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=ax_cqas(doc, f, f"{doc}_sec_cqa", report=False)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=ax_params(doc, f, f"{doc}_sec_param", classified=False)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=ax_methods(doc, f, f"{doc}_sec_methods", report=False)),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "AEX sets one CQA (cumulative MVM clearance); the other QualityAttribute entities are the CQAs it controls/clears (formed/introduced upstream).",
            "Flow-through-pool HCP and step-LRF are in-process/modular responses; captured via StudyDesign.responses.",
            "The Plan states classification is an OUTPUT; parameter_type left 'unclassified' here.",
        ],
        inventory=ax_inventory(doc, f, "process_characterization_plan"),
        entities=entities,
        studies=ax_studies(doc, f, report=False),
        report_sections=ax_report_sections(doc, f, report=False),
        assertions=ax_assertions(doc, f, report=False), concepts=ax_concepts())


def build_report_aex():
    doc, f = "PCR-008", PCR8_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_exec",
                                  process_steps=[ax_step(doc, f, f"{doc}_sec_exec", report=True)],
                                  equipment=ax_equipment(doc, f, f"{doc}_sec_exec", report=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=ax_params(doc, f, f"{doc}_sec_param", classified=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=ax_cqas(doc, f, f"{doc}_sec_cqa", report=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=ax_methods(doc, f, f"{doc}_sec_methods", report=True)),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT + [
            "ProvenAcceptableRange (new model) — per-CQA x parameter PAR (at-set-point / NOR-propagated); the viral CQAs use a back-calculated step floor",
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "AEX sets one CQA (cumulative MVM clearance); the other QualityAttribute entities are the CQAs it controls/clears.",
            "Three deviations (DEV-008-01 non-representative deamidated-load re-execution; DEV-008-02 permissive UV pool-stop corrected by modelling + verification runs; DEV-008-03 out-of-range wash-buffer lot retained) are narrative; the annex captures the DoE-grounded entities and the requalified-load results reported.",
            "Process-capability (Cpk) values have no dedicated field; reported as report_sections statements.",
            "proven_acceptable_ranges mirror @tbl-par (doe_report.par_table); rhetorical_spans are verbatim report prose; PCR-008 carries no weak_claims.",
        ],
        inventory=ax_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=ax_studies(doc, f, report=True),
        design_spaces=ax_design_spaces(doc, f),
        proven_acceptable_ranges=ax_proven_acceptable_ranges(doc, f),
        report_sections=ax_report_sections(doc, f, report=True),
        assertions=ax_assertions(doc, f, report=True), concepts=ax_concepts(),
        rhetorical_spans=build_rhetorical_spans(doc, f))


# =========================================================================== #
# Small-Virus Retentive Filtration (Step 9) — PCP-009 / PCR-009.                #
# --------------------------------------------------------------------------- #
# Additive, self-contained builders for the virus-filtration DoE pair. Like     #
# CEX, the step sets NO CQA: it is the dedicated small-virus removal step and    #
# the principal contributor to the cumulative MVM (parvovirus) log-reduction,    #
# with a major enveloped-virus (XMuLV) log-reduction, all credited as           #
# orthogonal/modular clearance under ICH Q5A(R2). The DoE is a compact           #
# two-factor full-factorial screen + face-centred CCD in volumetric load /       #
# filtration pressure. With two factors the screen is NOT near-saturated, so the  #
# usual screening-identifies/RSM-predicts framing is adapted: the RSM remains the #
# predictive model because its axial runs test linearity and its larger           #
# replicated centre gives the pure-error estimate. Load is the only resolved      #
# effect (MVM clearance falls with load, reported adverse-first and then          #
# bounded); XMuLV clearance and step yield are null results whose fits are NOT    #
# used predictively. Both parameters are WC-CPP — load because it is              #
# quality-linked to MVM clearance, pressure on bounding logic (ICH Q5A(R2) ties   #
# the claim to the conditions under which it was demonstrated). The design space  #
# is the whole characterized rectangle. No univariate parameter.                  #
# =========================================================================== #
VFUO = "virus_filtration"
VFUO_NAME = P.CFG.unit_op(VFUO).name             # "Small Virus Retentive Filtration"
VFSTEP = P.CFG.unit_op(VFUO).step                # 9
VFSTEP_LABEL = f"{VFUO_NAME} (Step {VFSTEP})"

PCP9_FILE = "PCP-009_virus_filtration.docx"
PCR9_FILE = "PCR-009_virus_filtration.docx"

VFPARAM_ROWS = P.param_reg[P.param_reg.unit_operation == VFUO_NAME].to_dict("records")
VFPARAM_CONCEPT = {
    "Filtration volume (load)": "param:vf_filtration_volume",
    "Filtration pressure": "param:vf_pressure",
}
# Both DoE factors (WC-CPP, multivariate); there is no univariate parameter.
VF_MULTIVARIATE = ["Filtration volume (load)", "Filtration pressure"]

# Virus filtration sets no CQA; it controls/clears the two viral-clearance CQAs (MVM first,
# the CQA it principally drives), expressed as the cumulative cross-step log-reduction.
VF_CQA_KEYS = ["lrv_mvm", "lrv_xmulv"]
VFATTR_CONCEPT = {"lrv_mvm": "attr:lrv_mvm", "lrv_xmulv": "attr:lrv_xmulv"}
VFATTR_NAME = {
    "lrv_mvm": "Viral clearance — MVM (parvovirus)",
    "lrv_xmulv": "Viral clearance — XMuLV (enveloped)",
}
VF_CQA_METHOD = {"lrv_mvm": "AMV-3018", "lrv_xmulv": "AMV-3017"}
VFMETHODS = [
    ("AMV-3018", "MVM Infectivity Titre (TCID50/qPCR)", "infectivity_assay",
     ["MVM infectious titre"], ["lrv_mvm"]),
    ("AMV-3017", "XMuLV Infectivity Titre (TCID50)", "infectivity_assay",
     ["XMuLV infectious titre"], ["lrv_xmulv"]),
]


def _vf_cqa_row(key):
    return P.cqa_reg[P.cqa_reg.key == key].iloc[0].to_dict()


def vf_step(doc_id, file_name, sec, report):
    if report:
        src = ref(doc_id, file_name, sec, "Executive summary",
                  "the dedicated small virus removal step of the A-Mab drug substance process")
    else:
        src = ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                  "The step is the dedicated small virus removal operation of the purification train and the principal source of MVM clearance.")
    return S.ProcessStep(
        step_id="step:virus_filtration", step_name=VFUO_NAME, step_number=str(VFSTEP),
        unit_operation=VFUO_NAME,
        description="Small-virus retentive (size-exclusion) filtration: the dedicated "
                    "virus-removal step. Retains virus larger than the membrane rating while "
                    "the antibody monomer transmits. Sets no product-quality CQA; it is the "
                    "principal contributor to the cumulative MVM (parvovirus) log-reduction "
                    "and a major contributor to the enveloped-virus (XMuLV) log-reduction, "
                    "credited as orthogonal/modular clearance under ICH Q5A(R2).",
        input_materials=["anion-exchange flow-through pool (virus-filtration feed)"],
        output_materials=["virus-filtration pool (UF/DF feed)"],
        equipment=["small-virus retentive filter", "scale-down filtration model"],
        source_references=[src], metadata=meta())


def vf_equipment(doc_id, file_name, sec, report):
    sdm = S.Equipment(
        equipment_id="equip:vf_sdm", equipment_name="scale-down filtration model",
        equipment_type="virus filtration (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Scale-down model and its qualification",
                               "a small scale spiking model of the commercial filtration step, "
                               "qualified under SOP-1001" if report
                               else "Qualify a scale-down model of the small virus retentive filtration step, and show that it represents the commercial step for virus retention, for flux decay and for step yield.")],
        metadata=meta())
    if report:
        return [sdm]
    return [
        S.Equipment(equipment_id="equip:vf_filter",
                    equipment_name="commercial-scale small-virus retentive filter",
                    equipment_type="virus-retentive filter", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec,
                                           "Scale-down model and its qualification",
                                           "the same membrane type and the same membrane chemistry as the commercial step")],
                    metadata=meta()),
        sdm,
    ]


def vf_sites(doc_id, file_name, sec):
    return [
        S.ManufacturingSite(site_id="site:cambridge", site_name=P.SENDING_SITE, site_role="sending",
                            location="Cambridge, MA",
                            source_references=[ref(doc_id, file_name, sec, "Title block",
                                                   "Cambridge, MA (Development)")],
                            metadata=meta()),
        S.ManufacturingSite(site_id="site:grafton", site_name=P.RECEIVING_SITE, site_role="receiving",
                            location="Grafton, WI",
                            source_references=[ref(doc_id, file_name, sec, "Title block",
                                                   "Grafton, WI (Commercial DS)")],
                            metadata=meta()),
    ]


def vf_params(doc_id, file_name, sec, classified):
    caption = ("Characterized parameters of the step, with set-point, normal operating range, "
               "characterization range, final classification and study type."
               if classified else
               "Parameters to be studied, with set-points, characterization ranges and normal "
               "operating ranges.")
    rats = {"WC-CPP": "Either quality-linked through a demonstrated effect on MVM clearance (the "
                      "volumetric-load limit), or held inside the range in which the clearance "
                      "claim was demonstrated even though no effect was resolved; in both cases "
                      "the risk of leaving the range is low because the parameter is measured "
                      "directly during the run."}
    out = []
    rows = param_rows(VFUO, classified)   # each parameter on its own @tbl-params row
    for r in VFPARAM_ROWS:
        name = r["parameter"]
        ptype = r["classification"] if classified else "unclassified"
        out.append(S.ProcessParameter(
            parameter_id=VFPARAM_CONCEPT[name], parameter_name=name, parameter_type=ptype,
            unit=r["unit"], target_value=f"{r['setpoint']:g}",
            NOR=f"{r['nor_low']:g}–{r['nor_high']:g} {r['unit']}",
            PAR=f"{r['par_low']:g}–{r['par_high']:g} {r['unit']}",
            associated_step=VFSTEP_LABEL,
            rationale_for_criticality=rats.get(r["classification"]) if classified else None,
            source_references=[ref(doc_id, file_name, sec,
                                   "Factors, ranges and the knowledge space" if classified
                                   else "Factors, ranges and study type",
                                   rows[name], table_title=caption,
                                   table_id=f"{doc_id}_tab_params",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


# Both documents carry the two viral-clearance CQAs in a single table; each CQA is
# anchored on the caption of the table that carries its row (the AEX pattern).
VF_CQA_CAPTION = {
    True: ("Viral-clearance quality attributes governed by the step, with the cumulative "
           "acceptance criteria for the drug substance and the criticality assigned under Tool #1."),
    False: "Quality attributes governed by the small-virus retentive filtration step.",
}


def vf_cqas(doc_id, file_name, sec, report):
    caption = VF_CQA_CAPTION[report]
    out = []
    rows = cqa_rows(VF_CQA_KEYS)   # each attribute on its own @tbl-cqa row
    for key in VF_CQA_KEYS:
        r = _vf_cqa_row(key)
        out.append(S.QualityAttribute(
            attribute_id=VFATTR_CONCEPT[key], attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"],
            acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            analytical_method=None if report else VF_CQA_METHOD[key],
            associated_steps=[VFSTEP_LABEL],
            rationale_for_criticality=f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = {r['tool1_score']}.",
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref(doc_id, file_name, sec, "Quality attributes in scope",
                                   rows[key], table_title=caption,
                                   table_id=f"{doc_id}_tab_cqa",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


# Per-method grounded fragment from each document's "Analytical methods" section.
VFMETHOD_QUOTE = {
    False: {  # PCP-009
        "AMV-3018": "MVM will be titred by TCID50 with qPCR confirmation",
        "AMV-3017": "XMuLV by TCID50",
    },
    True: {  # PCR-009
        # Both methods are named in one sentence of the report's analytical-methods section;
        # each takes the shortest contiguous slice of it that names itself.
        "AMV-3018": "MVM was titrated by the method validated under AMV-3018",
        "AMV-3017": "XMuLV by the method validated under AMV-3017",
    },
}


def vf_methods(doc_id, file_name, sec, report):
    quotes = VFMETHOD_QUOTE[report]
    out = []
    for mid, mname, mtype, analytes, attrs in VFMETHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[VFATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods", quotes[mid])],
            metadata=meta()))
    return out


def vf_studies(doc_id, file_name, report):
    sec = "Study design"
    n_scr, n_rsm = P.doe_runs(VFUO, "screening"), P.doe_runs(VFUO, "rsm")
    responses = ["mvm_lrf", "xmulv_lrf", "step_yield"]
    return [
        S.StudyDesign(
            study_id="study:vf_screening", study_type="screening_doe",
            design_name="two-level full factorial", unit_operation=VFUO_NAME,
            factors=VF_MULTIVARIATE, responses=responses,
            n_runs=n_scr, n_center_points=P.doe_centre_points(VFUO, "screening"), scale_down_model="scale-down filtration model",
            associated_parameters=[VFPARAM_CONCEPT[f] for f in VF_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Screening design",
                                   "The screening design is a two-level full factorial in both "
                                   "parameters" if report
                                   else "With 2 factors the full factorial is executed, so both main effects and the interaction are estimated free of aliasing.")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vf_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=VFUO_NAME,
            factors=VF_MULTIVARIATE, responses=responses,
            n_runs=n_rsm, n_center_points=P.doe_centre_points(VFUO, "rsm"), scale_down_model="scale-down filtration model",
            associated_parameters=[VFPARAM_CONCEPT[f] for f in VF_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "a face-centred central composite design in the same two "
                                   "parameters" if report
                                   else "The response-surface study will be a face-centred central composite design in both factors, 12 runs in total.")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vf_sdm_qual", study_type="scale_down_qualification",
            unit_operation=VFUO_NAME, scale_down_model="scale-down filtration model",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "Qualification compared the model with at-scale data on the "
                                   "input and output attributes of the step" if report
                                   else "Triplicate runs of the scale-down system will be operated at the set-points in Table 6 on representative anion exchange pool")],
            metadata=meta()),
    ]


def vf_concepts():
    from annex_contract.concepts import Concept, ConceptStore
    cs = [Concept(concept_id="step:virus_filtration", concept_type="PROCESS_STEP",
                  canonical_name=VFUO_NAME,
                  aliases=["virus filtration", "small-virus retentive filtration",
                           "nanofiltration", "VF", "Step 9"],
                  review_status="human_verified")]
    for name, cid in VFPARAM_CONCEPT.items():
        cs.append(Concept(concept_id=cid, concept_type="PROCESS_PARAMETER", canonical_name=name,
                          review_status="human_verified"))
    for key in VF_CQA_KEYS:
        cs.append(Concept(concept_id=VFATTR_CONCEPT[key], concept_type="QUALITY_ATTRIBUTE",
                          canonical_name=VFATTR_NAME[key], aliases=[key],
                          review_status="human_verified"))
    for mid, mname, *_ in VFMETHODS:
        cs.append(Concept(concept_id=f"method:{mid}", concept_type="ANALYTICAL_METHOD",
                          canonical_name=mname, aliases=[mid], review_status="human_verified"))
    return ConceptStore(run_id="gt-vf", concepts=cs)


def vf_assertions(doc_id, file_name, report):
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote, header=None):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote,
                                   table_header=header)],
            metadata=meta()))

    param_sec = "Factors, ranges and the knowledge space" if report else "Factors, ranges and study type"
    prow = param_rows(VFUO, report)   # the row that NAMES this parameter
    for name, cid in VFPARAM_CONCEPT.items():
        add("step:virus_filtration", "step_has_parameter", cid,
            f"{VFUO_NAME} has process parameter {name}.", param_sec, prow[name],
            prow.header)
    # step is the principal MVM-removal mechanism; a major clearance step for XMuLV
    add("step:virus_filtration", "step_has_quality_attribute", "attr:lrv_mvm",
        f"{VFUO_NAME} is the principal contributor to the cumulative MVM (parvovirus) clearance.",
        "Executive summary" if report else "Unit-operation description and prior knowledge",
        "it is the largest single contributor to the parvovirus clearance claimed for the process"
        if report
        else "Subtracting the clearance credited to the other steps of the train leaves this step a floor of 3.89 log10 for MVM and 3.65 log10 for XMuLV.")
    add("step:virus_filtration", "step_has_quality_attribute", "attr:lrv_xmulv",
        f"{VFUO_NAME} is a major clearance step for enveloped virus (XMuLV).",
        "Product and unit operation" if report else "Unit-operation description and prior knowledge",
        "The claim made for the step is a log reduction factor for two model viruses, the "
        "parvovirus MVM and the enveloped retrovirus XMuLV" if report
        else "XMuLV is cleared by all three viral safety steps and by the chromatography steps that make no claim, so the cumulative XMuLV requirement is met with a wide margin.")
    # attribute -> method (plan only; the report does not restate the linkage)
    if not report:
        for key in VF_CQA_METHOD:
            add(VFATTR_CONCEPT[key], "attribute_measured_by_method", f"method:{VF_CQA_METHOD[key]}",
                f"{VFATTR_NAME[key]} is measured by {VF_CQA_METHOD[key]}.", "Analytical methods",
                VFMETHOD_QUOTE[False][VF_CQA_METHOD[key]])
    # acceptance criterion for the CQA the step principally drives. Both documents state
    # that the criterion is cumulative over the train, not a per-step release limit.
    mvm = _vf_cqa_row("lrv_mvm")
    add("attr:lrv_mvm", "attribute_has_acceptance_criterion", "lit:lrv_mvm_acc",
        f"MVM clearance acceptance: ≥ {mvm['acc_low']:g} {mvm['unit']} (cumulative).",
        "Quality attributes in scope",
        "Both acceptance criteria are cumulative over the process and are stated as a minimum "
        "log reduction" if report
        else "Acceptance and decision criteria Three kinds of criterion apply to this study.")
    # parameter -> attribute impacts / non-impacts
    if report:
        add("param:vf_filtration_volume", "parameter_impacts_attribute", "attr:lrv_mvm",
            "Volumetric load has a demonstrated effect on MVM clearance — the only effect resolved "
            "at this step — so it is quality-linked and classified WC-CPP.",
            "Parameter classification",
            "Classified WC-CPP. The load has a demonstrated effect on MVM clearance")
        add("param:vf_pressure", "parameter_does_not_significantly_impact_attribute", "attr:lrv_mvm",
            "The main effect of filtration pressure on MVM clearance was not significant in either "
            "design. It is classified WC-CPP because it is linked to the attribute through the "
            "shallow maximum in pressure and through the bound it places on the operating range.",
            "Parameter classification",
            "Its main effect on MVM clearance was not significant in either design")
    else:
        for name in VF_MULTIVARIATE:
            add(VFPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:lrv_mvm",
                f"{name} was ranked high enough in RA-001 to require multivariate evaluation of its "
                f"potential effect on the credited viral log-reduction.",
                "Risk-based prioritization of parameters",
                "Both parameters will be studied multivariately.")
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def vf_report_sections(doc_id, file_name, report):
    from annex_contract.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote, also=()):
        """``also`` carries further ``(section, quote)`` pairs. The classification result is
        stated in two halves in two sections — both parameters WC-CPP in the summary, no CPP
        and no key or general parameter in the classification section — so that statement
        needs two anchors."""
        refs = [ref(doc_id, file_name, sec, sec, quote)]
        refs += [ref(doc_id, file_name, s2, s2, q2) for s2, q2 in also]
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=refs)
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-009 defines the characterization study that will bound the operating ranges "
                  "of the A-Mab small-virus retentive filtration step (Step 9).",
               "Purpose and scope",
               "This plan describes the characterization study for Step 9 of the drug substance train, the small virus retentive filtration step"),
            st(2, "Two process parameters (volumetric load and filtration pressure) are characterized "
                  "in a compact two-factor multivariate design.",
               "Factors, ranges and study type",
               "The study covers the 2 process parameters of the step and the 3 responses listed in Table 8 ."),
            st(3, "The study uses a two-factor full-factorial screen followed by a face-centred "
                  "central composite design on a scale-down filtration model.",
               "Response-surface design",
               "The response-surface study will be a face-centred central composite design in both factors, 12 runs in total."),
            st(4, "Virus filtration provides the largest single MVM reduction in the train and a "
                  "substantial XMuLV reduction.",
               "Unit-operation description and prior knowledge",
               "Subtracting the clearance credited to the other steps of the train leaves this step a floor of 3.89 log10 for MVM and 3.65 log10 for XMuLV."),
            st(5, "The study must establish the maximum volumetric load at which the back-calculated "
                  "step-level MVM criterion is still met, capped at the upper edge of the "
                  "characterized range.",
               "Load limit and operating region",
               "the maximum load and the pressure range will be established on A-Mab material"),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Both process parameters (volumetric load and filtration pressure) were classified as "
              "well controlled critical process parameters; neither is a CPP and the step carries "
              "no key or general process parameter.",
           "Executive summary",
           "Both parameters were classified as well controlled critical process parameters",
           [("Parameter classification",
             "Neither parameter was classified as a critical process parameter, and no parameter "
             "of this step is a key or general process parameter")]),
        st(2, "MVM (parvovirus) retention falls as the volumetric load on the membrane rises, and "
              "the load is the parameter that bounds the clearance claim.",
           "Mechanistic interpretation",
           "Retention therefore falls as the load rises, and the load is the parameter that bounds "
           "the clearance claim"),
        st(3, "XMuLV clearance and step yield have no active factor; both are reported as robust "
              "over the characterized region rather than as fitted surfaces used predictively.",
           "Response-surface models",
           "Both responses are reported as robust over the characterized region rather than as "
           "fitted surfaces"),
        st(4, "Only the MVM response-surface model is adequate, and it is the predictive model on "
              "which the design space and the proven acceptable ranges rest.",
           "Response-surface models", "The model for MVM LRF is adequate."),
        st(5, "The filtration volume carries the only significant term in the MVM response-surface "
              "model.",
           "Response-surface models", "The filtration volume carries the only significant term"),
        st(6, "Lack of fit for the MVM model is not rejected at the stated significance level, but "
              "the margin is not large and the pure error it is tested against rests on few "
              "degrees of freedom.",
           "Response-surface models",
           "the quadratic form is not rejected at α = 0.05. The margin is not large"),
        st(7, "The design space is bounded in one direction only: the excluded part of the "
              "characterized region is the high load region, because the load is the only active "
              "factor.",
           "Design space",
           "The excluded part is the high load region, and its boundary runs almost vertically in "
           "Figure 1 because the load is the only active factor"),
        st(8, "The reported viral-clearance capability is a property of the whole process and not "
              "of this step alone.",
           "Process capability and robustness",
           "The capability of both attributes is a property of the process and not of this step"),
        st(9, "Cumulative MVM clearance carries the tightest process-capability index in the drug "
              "substance register.",
           "Process capability and robustness",
           "Cumulative MVM clearance is the tightest capability in the drug substance register"),
        # New in this report: the NOR-propagated PAR of the load stops below the upper edge of
        # its normal operating range, so the maximum load carried forward is the PAR.
        st(10, "The proven acceptable range of the filtration volume under propagation of the "
               "filtration pressure ends below the upper limit of the normal operating range, so "
               "the maximum load carried into Stage 2 is the proven acceptable range and not the "
               "normal operating range.",
            "Proven acceptable ranges",
            "the maximum load carried into Stage 2 is the proven acceptable range and not the "
            "normal operating range"),
    ])]


def vf_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:vf", unit_operation=VFUO_NAME,
        parameters=["param:vf_filtration_volume", "param:vf_pressure"],
        quality_attributes_constrained=["attr:lrv_mvm", "attr:lrv_xmulv"],
        definition="The part of the characterized rectangle in volumetric load and filtration "
                   "pressure over which both governed attributes meet the log-reduction credited "
                   "to the step. The region is bounded in one direction only: the excluded part is "
                   "the high-load part of the characterized range, because volumetric load is the "
                   "only active factor and MVM clearance falls as the load rises. The XMuLV "
                   "requirement is met with a wide margin everywhere and excludes none of the "
                   "region. Filtration pressure is bounded because ICH Q5A(R2) ties the clearance "
                   "claim to the conditions under which it was demonstrated, not because an effect "
                   "was measured. The region is evaluated on mean predictions, so the operating "
                   "limits carried into Stage 2 are taken from the narrower proven acceptable "
                   "ranges instead.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "the region of the filtration volume and the filtration pressure "
                               "over which both governed attributes meet the log reduction "
                               "credited to the step")],
        metadata=meta())]


# --------------------------------------------------------------------------- #
# Report-only PAR layer (PCR-009 only).                                         #
# --------------------------------------------------------------------------- #
# proven_acceptable_ranges derive from the same DoE engine that renders @tbl-par  #
# (doe_report.par_table). Both governed attributes are viral-clearance responses, #
# so both acceptance bases are the step floor back-calculated from the cumulative #
# requirement (modular claim under ICH Q5A(R2)). Quotes are plain-prose fragments #
# of the report's Proven-acceptable-ranges section.                               #
# --------------------------------------------------------------------------- #
VF_PAR_SEC = "Proven acceptable ranges"
VF_PAR_CQA_QUOTE = {
    "MVM LRF (log₁₀)": ("Low-pH inactivation is credited with no MVM clearance at all, because a "
                        "non-enveloped parvovirus is not inactivated by low pH."),
    "XMuLV LRF (log₁₀)": ("Figure 4 shows the corresponding picture for XMuLV, where the response "
                          "is flat and the margin to the limit is large throughout"),
}
_VF_PAR_GENERAL_QUOTE = ("The result that matters is the ceiling on filtration volume")


def vf_proven_acceptable_ranges(doc_id, file_name):
    """One ProvenAcceptableRange per governed viral-clearance CQA x parameter, from the same
    DoE engine (``doe_report.par_table``) that renders @tbl-par in the report. Neither CQA has
    a drug-substance specification a single step can be measured against, so both use the
    back-calculated step floor (cumulative requirement minus the credit taken by the other
    orthogonal steps) as the acceptance basis."""
    import doe_report as D
    par = D.par_table(VFUO)
    out = []
    # Each attribute x parameter combination on its own @tbl-par row: the
    # per-attribute prose said which attribute was governed, never which
    # parameter's range was proven.
    rows = par_rows(VFUO)
    for i, r in enumerate(par.to_dict("records"), 1):
        cqa, param, unit = r["CQA"], r["Parameter"], (r["Unit"] or "")
        out.append(S.ProvenAcceptableRange(
            par_id=f"{doc_id}-PAR{i:02d}", unit_operation=VFUO_NAME,
            quality_attribute=cqa, parameter=param,
            characterization_range=f"{r['Char. range']} {unit}".strip(),
            par_at_setpoint=f"{r['PAR (set-point)']} {unit}".strip(),
            par_nor_propagated=f"{r['PAR (NOR)']} {unit}".strip(),
            acceptance_basis=par_basis_text(VFUO, cqa),
            source_references=[ref(doc_id, file_name, f"{doc_id}_sec_par", VF_PAR_SEC,
                                   rows[(cqa, param)],
                                   table_id=f"{doc_id}_tab_par",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


def vf_inventory(doc_id, file_name, dtype):
    return S.DocumentInventoryItem(
        document_id=doc_id, file_name=file_name, predicted_document_type=dtype,
        product_name_candidates=["A-Mab"], process_name_candidates=[VFUO_NAME],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "virus filtration", "viral clearance",
                     "small-virus retention", "design of experiments", "parameter classification"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc_id][0]}'.",
        source_references=[ref(doc_id, file_name, "Title block", "Title block",
                               title_block_quote(doc_id))],
        metadata=meta())


def build_plan_vf():
    doc, f = "PCP-009", PCP9_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_uo",
                                  process_steps=[vf_step(doc, f, f"{doc}_sec_uo", report=False)],
                                  equipment=vf_equipment(doc, f, f"{doc}_sec_uo", report=False),
                                  sites=vf_sites(doc, f, f"{doc}_sec_uo")),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=vf_cqas(doc, f, f"{doc}_sec_cqa", report=False)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=vf_params(doc, f, f"{doc}_sec_param", classified=False)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=vf_methods(doc, f, f"{doc}_sec_methods", report=False)),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Virus filtration sets no CQA; the QualityAttribute entities are the viral-clearance CQAs it controls/clears (cumulative, cross-step).",
            "Per-step MVM/XMuLV log-reductions are modular contributions with no released spec; captured via StudyDesign.responses.",
            "The Plan states classification is an OUTPUT; parameter_type left 'unclassified' here.",
        ],
        inventory=vf_inventory(doc, f, "process_characterization_plan"),
        entities=entities,
        studies=vf_studies(doc, f, report=False),
        report_sections=vf_report_sections(doc, f, report=False),
        assertions=vf_assertions(doc, f, report=False), concepts=vf_concepts())


def build_report_vf():
    doc, f = "PCR-009", PCR9_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_exec",
                                  process_steps=[vf_step(doc, f, f"{doc}_sec_exec", report=True)],
                                  equipment=vf_equipment(doc, f, f"{doc}_sec_exec", report=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=vf_params(doc, f, f"{doc}_sec_param", classified=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=vf_cqas(doc, f, f"{doc}_sec_cqa", report=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=vf_methods(doc, f, f"{doc}_sec_methods", report=True)),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT + [
            "ProvenAcceptableRange (new model) — per-CQA x parameter PAR (at-set-point / "
            "NOR-propagated); both viral CQAs use a back-calculated step floor",
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "Virus filtration sets no CQA; the QualityAttribute entities are the viral-clearance CQAs it controls/clears (cumulative, cross-step).",
            "Per-step MVM/XMuLV log-reductions are modular contributions with no released spec; reported via studies/report_sections.",
            "Two-factor design: the screening model is not near-saturated, so the usual screening-identifies/RSM-predicts split is adapted — the RSM stays the predictive model because its axial runs test linearity and its larger replicated centre gives the pure-error estimate.",
            "XMuLV log-reduction and step yield produced no significant term; their response-surface fits are robustness evidence and are explicitly not used predictively, so no DesignSpace or model claim is recorded for them.",
            "Process-capability (Cpk) values have no dedicated field; reported as report_sections statements.",
            "proven_acceptable_ranges mirror @tbl-par (doe_report.par_table); rhetorical_spans are verbatim report prose; PCR-009 carries no weak_claims.",
        ],
        inventory=vf_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=vf_studies(doc, f, report=True),
        design_spaces=vf_design_spaces(doc, f),
        proven_acceptable_ranges=vf_proven_acceptable_ranges(doc, f),
        report_sections=vf_report_sections(doc, f, report=True),
        assertions=vf_assertions(doc, f, report=True), concepts=vf_concepts(),
        rhetorical_spans=build_rhetorical_spans(doc, f))


# =========================================================================== #
# Ultrafiltration / Diafiltration (Step 10) — PCP-010 / PCR-010.                #
# --------------------------------------------------------------------------- #
# Additive, self-contained builders for the non-DoE UF/DF pair. Like harvest,   #
# UF/DF forms and clears no product-quality CQA, so there are no QualityAttribute #
# entities and no design space — the report says so in as many words ("This step  #
# has no design space"). No screening and no response-surface design was planned   #
# or run, and RA-001 required none, so the only studies are the univariate ranging #
# and the scale-down qualification. The step monitors the size- and charge-variant #
# attributes of its own AMV panel to confirm they are neither formed nor cleared.  #
# Formulation characterization is DEFERRED (not omitted) to the drug-product       #
# development programme, with the scope boundary set in PTP-001.                   #
# =========================================================================== #
UFUO = "ufdf"
UFUO_NAME = P.CFG.unit_op(UFUO).name             # "Ultrafiltration / Diafiltration (formulation)"
UFSTEP = P.CFG.unit_op(UFUO).step                # 10
UFSTEP_LABEL = f"Ultrafiltration / Diafiltration (Step {UFSTEP})"

PCP10_FILE = "PCP-010_ufdf.docx"
PCR10_FILE = "PCR-010_ufdf.docx"

UFPARAM_ROWS = P.param_reg[P.param_reg.unit_operation == UFUO_NAME].to_dict("records")
UFPARAM_CONCEPT = {
    "Number of diavolumes": "param:ufdf_diavolumes",
    "Transmembrane pressure": "param:ufdf_tmp",
    "Final DS concentration": "param:ufdf_final_conc",
}
# Product-quality attributes UF/DF monitors (it sets/clears none of them): confirmed
# unchanged across the operation. Concentration is a process attribute, not a CQA.
UFATTR_CONCEPT = {
    "aggregates_hmw": "attr:aggregates_hmw",
    "acidic_variants": "attr:acidic_variants",
}
UFATTR_NAME = {
    "aggregates_hmw": "Aggregates (HMW)",
    "acidic_variants": "Acidic charge variants (deamidation)",
}
UFMETHODS = [
    ("AMV-3019", "Protein Concentration by A280 (UV)", "spectroscopy",
     ["protein concentration"], []),
    ("AMV-3011", "Size-Variants (SEC-HPLC)", "chromatography",
     ["aggregate", "monomer"], ["aggregates_hmw"]),
    ("AMV-3013", "Charge Variants (icIEF)", "electrophoresis",
     ["acidic variants", "main peak", "basic variants"], ["acidic_variants"]),
]
# Per-document, per-method grounded fragment from the "Analytical methods" section.
# (The plan spells the size-variant method out; the report abbreviates it to SEC-HPLC.)
UFMETHOD_QUOTE = {
    False: {  # PCP-010
        "AMV-3019": "Protein concentration is measured by A280 under AMV-3019",
        "AMV-3011": "Aggregate is measured by SEC under AMV-3011",
        "AMV-3013": "Charge variants are measured by icIEF under AMV-3013",
    },
    True: {   # PCR-010
        # All three methods are named in one sentence of the report's analytical-methods
        # section; each takes the shortest contiguous slice of it that names itself.
        "AMV-3019": "Protein concentration was measured by ultraviolet absorbance (AMV-3019)",
        "AMV-3011": "aggregate by size exclusion chromatography (AMV-3011)",
        "AMV-3013": "charge variants by imaged capillary isoelectric focusing (AMV-3013)",
    },
}
# Anchor for the two monitored attributes. The plan states the claim in the caption of its
# monitored-attribute table: the attributes are measured across the step, and neither is set
# nor cleared here. The report states it per attribute in "Quality attributes in scope", so
# the report branch anchors each attribute on the sentence that names it.
UFATTR_TABLE_QUOTE = {
    False: ("Quality attributes measured across the step, with drug substance acceptance criteria."),
}
UFATTR_REPORT_QUOTE = {
    "aggregates_hmw": ("Aggregate is the attribute at risk. The antibody is held at its highest "
                       "concentration of the whole process in this step"),
    "acidic_variants": ("Acidic charge variants are measured because asparagine deamidation runs "
                        "faster as the pH rises"),
}
# Per-parameter classification sentence from the report's "Parameter classification"
# section: each says the parameter is a KPP and why no quality attribute is at stake.
UFCLASS_QUOTE = {
    "Number of diavolumes": (
        "Number of diavolumes. Classified as a key process parameter. It determines the "
        "completeness of the buffer exchange and therefore the composition of the formulated "
        "drug substance, and it had no resolvable effect on aggregate or on charge variants "
        "over the range studied"),
    "Transmembrane pressure": (
        "Transmembrane pressure. Classified as a key process parameter. Raising it drives more "
        "permeate through the membrane and shortens the step, and it had no resolvable effect "
        "on product quality"),
    "Final DS concentration": (
        "Final drug substance concentration. Classified as a key process parameter. It is a "
        "drug substance specification the step must meet, and it had no resolvable effect on "
        "aggregate"),
}
# Per-parameter sentence from the report that gives the binding condition of each proven
# acceptable range: the low edge of the diavolume range, which is also the low edge of the
# normal operating range; the pressure edge the recorded excursion stayed inside; and the low
# edge of the concentration range, which is acceptable for quality but below the formulated
# target.
UFPAR_QUOTE = {
    "Number of diavolumes": ("A count below the lower edge leaves more process buffer behind, "
                             "which is the outcome that matters, and the lower edge of the range "
                             "studied is also the lower edge of the normal operating range"),
    "Transmembrane pressure": ("The maximum pressure stayed inside the characterized range for "
                               "the parameter"),
    "Final DS concentration": ("The lower edge of the range for the final drug substance "
                               "concentration is an acceptable condition for product quality but "
                               "not for the formulation"),
}
# Both documents describe the scale-down system as a tangential-flow filtration system;
# neither calls it "bench-scale", so the entity follows the text.
UFSDM = "scale-down tangential-flow filtration system"


def uf_step(doc_id, file_name, sec, report):
    if report:
        src = ref(doc_id, file_name, sec, "Executive summary",
                  "Ultrafiltration and diafiltration is the last operation of the A-Mab drug "
                  "substance process")
    else:
        src = ref(doc_id, file_name, sec, "Purpose and scope",
                  "The UF/DF step concentrates the antibody and exchanges the process buffer for the formulation buffer.")
    return S.ProcessStep(
        step_id="step:ufdf", step_name=UFUO_NAME, step_number=str(UFSTEP),
        unit_operation=UFUO_NAME,
        description="Final ultrafiltration / diafiltration (tangential-flow filtration): "
                    "ultrafiltration concentrates the virus-filtration pool and diafiltration "
                    "exchanges it into the final formulation buffer, delivering the drug "
                    "substance at its target concentration. Forms no product-quality attribute; "
                    "a formulation / mass-balance operation.",
        input_materials=["virus-filtration pool (UF/DF feed)"],
        output_materials=["A-Mab drug substance (formulated)"],
        equipment=["ultrafiltration / diafiltration membrane (TFF)", UFSDM],
        source_references=[src], metadata=meta())


def uf_equipment(doc_id, file_name, sec, report):
    membrane = S.Equipment(
        equipment_id="equip:ufdf_membrane",
        equipment_name="ultrafiltration / diafiltration membrane (TFF)",
        equipment_type="tangential-flow-filtration membrane", site_name=P.RECEIVING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Product and unit operation" if report
                               else "Unit-operation description and prior knowledge",
                               "operated as tangential flow filtration on a membrane whose pores "
                               "pass buffer salts and small solutes and retain the antibody"
                               if report
                               else "Both operations run across a tangential flow membrane whose pores pass buffer salts and retain the antibody.")],
        metadata=meta())
    sdm = S.Equipment(
        equipment_id="equip:ufdf_sdm", equipment_name=UFSDM,
        equipment_type="ultrafiltration / diafiltration (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec, "Scale-down model and its qualification",
                               "a scale-down tangential flow filtration system, EQ-TFF-142, "
                               "qualified as a model of the commercial skid under SOP-1001"
                               if report else "the bench scale TFF skid EQ-TFF-142")],
        metadata=meta())
    return [membrane, sdm]


def uf_sites(doc_id, file_name, sec):
    return [
        S.ManufacturingSite(site_id="site:cambridge", site_name=P.SENDING_SITE, site_role="sending",
                            location="Cambridge, MA",
                            source_references=[ref(doc_id, file_name, sec, "Title block",
                                                   "Cambridge, MA (Development)")],
                            metadata=meta()),
        S.ManufacturingSite(site_id="site:grafton", site_name=P.RECEIVING_SITE, site_role="receiving",
                            location="Grafton, WI",
                            source_references=[ref(doc_id, file_name, sec, "Title block",
                                                   "Grafton, WI (Commercial DS)")],
                            metadata=meta()),
    ]


def uf_params(doc_id, file_name, sec, classified):
    caption = ("Parameters of the ultrafiltration / diafiltration step, with set-points, normal "
               "operating ranges, characterization ranges, final classification and study type."
               if classified else
               "Parameters to be studied, with set-points, characterization ranges and normal "
               "operating ranges.")
    rats = {"KPP": "Governs buffer-exchange completeness, permeate flux and operation duration, or "
                   "the final drug-substance concentration — process performance only; no failure "
                   "mode at this step reaches a critical quality attribute."}
    out = []
    rows = param_rows(UFUO, classified)   # each parameter on its own @tbl-params row
    for r in UFPARAM_ROWS:
        name = r["parameter"]
        ptype = r["classification"] if classified else "unclassified"
        out.append(S.ProcessParameter(
            parameter_id=UFPARAM_CONCEPT[name], parameter_name=name, parameter_type=ptype,
            unit=r["unit"], target_value=f"{r['setpoint']:g}",
            NOR=f"{r['nor_low']:g}–{r['nor_high']:g} {r['unit']}",
            PAR=f"{r['par_low']:g}–{r['par_high']:g} {r['unit']}",
            associated_step=UFSTEP_LABEL,
            rationale_for_criticality=rats.get(r["classification"]) if classified else None,
            source_references=[ref(doc_id, file_name, sec,
                                   "Study design" if classified
                                   else "Factors, ranges and study type",
                                   rows[name], table_title=caption,
                                   table_id=f"{doc_id}_tab_params",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


def uf_methods(doc_id, file_name, sec, report):
    qmap = UFMETHOD_QUOTE[bool(report)]
    out = []
    for mid, mname, mtype, analytes, attrs in UFMETHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[UFATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods", qmap[mid])],
            metadata=meta()))
    return out


def uf_studies(doc_id, file_name, report):
    """Only two studies exist for this step: the one-factor-at-a-time ranging and the
    scale-down qualification. No screening and no response-surface design was planned or
    run, and RA-001 required none, so no DoE StudyDesign is asserted."""
    sec = "Univariate assessment"
    return [
        S.StudyDesign(
            study_id="study:ufdf_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=UFUO_NAME,
            factors=["Number of diavolumes", "Transmembrane pressure", "Final DS concentration"],
            responses=["step yield", "buffer exchange", "final DS concentration", "mass balance"],
            scale_down_model=UFSDM,
            associated_parameters=list(UFPARAM_CONCEPT.values()),
            source_references=[ref(doc_id, file_name, sec, sec,
                                   "The parameter under test was set at the lower edge of its "
                                   "characterized range, at its set-point and at the upper edge, "
                                   "while the other two parameters were held at their set-points"
                                   if report else
                                   "Each parameter will be run at 3 levels, which are the two edges of its characterization range")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:ufdf_sdm_qual", study_type="scale_down_qualification",
            unit_operation=UFUO_NAME, scale_down_model=UFSDM,
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "The model was qualified by comparing the inputs and the "
                                   "outputs of the step at the two scales" if report
                                   else "will be compared with the pilot and commercial record on step yield")],
            metadata=meta()),
    ]


def uf_concepts():
    from annex_contract.concepts import Concept, ConceptStore
    cs = [Concept(concept_id="step:ufdf", concept_type="PROCESS_STEP",
                  canonical_name=UFUO_NAME,
                  aliases=["UF/DF", "ultrafiltration", "diafiltration",
                           "tangential-flow filtration", "formulation", "Step 10"],
                  review_status="human_verified")]
    for name, cid in UFPARAM_CONCEPT.items():
        cs.append(Concept(concept_id=cid, concept_type="PROCESS_PARAMETER", canonical_name=name,
                          review_status="human_verified"))
    for key, cid in UFATTR_CONCEPT.items():
        cs.append(Concept(concept_id=cid, concept_type="QUALITY_ATTRIBUTE",
                          canonical_name=UFATTR_NAME[key], aliases=[key],
                          review_status="human_verified"))
    for mid, mname, *_ in UFMETHODS:
        cs.append(Concept(concept_id=f"method:{mid}", concept_type="ANALYTICAL_METHOD",
                          canonical_name=mname, aliases=[mid], review_status="human_verified"))
    return ConceptStore(run_id="gt-ufdf", concepts=cs)


def uf_assertions(doc_id, file_name, report):
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote, header=None):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote,
                                   table_header=header)],
            metadata=meta()))

    prow = param_rows(UFUO, report)   # the row that NAMES this parameter
    param_sec = "Study design" if report else "Factors, ranges and study type"
    for name, cid in UFPARAM_CONCEPT.items():
        add("step:ufdf", "step_has_parameter", cid,
            f"{UFUO_NAME} has process parameter {name}.", param_sec, prow[name],
            prow.header)
    # UF/DF monitors the two attributes of its own AMV panel; it neither forms nor clears
    # them. The table caption of each document states exactly that, so it is the anchor.
    for key, cid in UFATTR_CONCEPT.items():
        add("step:ufdf", "step_has_quality_attribute", cid,
            f"{UFUO_NAME} monitors {UFATTR_NAME[key]} across the operation; the attribute is "
            f"neither formed nor cleared here.",
            "Quality attributes in scope",
            UFATTR_REPORT_QUOTE[key] if report else UFATTR_TABLE_QUOTE[False])
    # attribute -> method (methods that measure a monitored product-quality attribute)
    for mid, mname, mtype, analytes, attrs in UFMETHODS:
        for a in attrs:
            add(UFATTR_CONCEPT[a], "attribute_measured_by_method", f"method:{mid}",
                f"{UFATTR_NAME[a]} is measured by {mid}.", "Analytical methods",
                UFMETHOD_QUOTE[bool(report)][mid])
    # No-CQA-impact of the operating parameters. The report classifies each parameter
    # individually (§8); the plan makes the claim mechanistically for all three at once.
    plan_no_impact_sec = "Unit-operation description and prior knowledge"
    plan_no_impact_quote = ("the step sets no CQA of its own and the three parameters reach the product by different routes")
    for name, cid in UFPARAM_CONCEPT.items():
        sec_ = "Parameter classification" if report else plan_no_impact_sec
        quote_ = UFCLASS_QUOTE[name] if report else plan_no_impact_quote
        add(cid, "parameter_does_not_significantly_impact_attribute", "attr:aggregates_hmw",
            f"{name} has no significant drug-substance product-quality (CQA) impact; it is a "
            f"key process parameter.", sec_, quote_)
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def uf_report_sections(doc_id, file_name, report):
    from annex_contract.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-010 defines the process characterization study for the A-Mab ultrafiltration and diafiltration step (Step 10).",
               "Purpose and scope",
               "This plan defines the process characterization studies for the ultrafiltration and diafiltration step of the A-Mab drug substance process"),
            st(2, "The step forms no critical quality attribute and makes no clearance claim.",
               "Purpose and scope",
               "The step is not where the quality attributes of A-Mab are formed."),
            st(3, "RA-001 assigned every parameter of the step to univariate assessment.",
               "Risk-based prioritization of parameters", "Proven acceptable ranges (planned analysis) A PAR will be assigned to each parameter from its univariate series."),
            st(4, "No drug substance attribute is formed or cleared at the step; two attributes are monitored across it.",
               "Quality attributes in scope", "The step is the last of the drug substance process, and no step downstream of it clears or modifies either attribute"),
            st(5, "The study will confirm that aggregate content and charge variant distribution are unchanged across the step.",
               "Objectives",
               "Determine the effect of the number of diavolumes, the transmembrane pressure and the final DS concentration on the aggregate content and the charge variant distribution of the drug substance"),
            st(6, "No screening and no response-surface design is planned, and no design space will be claimed for the step.",
               "Univariate assessment", "No response surface model will be fitted for this step, because the design carries no factorial structure and no interaction or curvature term can be estimated from it."),
            st(7, "Formulation characterization is out of scope; the formulation is The composition of the formulation buffer is fixed by that programme and is treated in these studies as a constant..",
               "Purpose and scope", "The composition of the formulation buffer is fixed by that programme and is treated in these studies as a constant."),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "The step sets no critical quality attribute; two attributes are nevertheless "
              "measured across it.",
           "Quality attributes in scope", "The step sets no critical quality attribute."),
        st(2, "The step forms no quality attribute of the antibody, removes no impurity that the "
              "control strategy credits, and claims no viral clearance.",
           "Product and unit operation",
           "The step forms no quality attribute of the antibody. It removes no impurity that the "
           "control strategy credits, and no viral clearance is claimed for it"),
        st(3, "The outputs of the step are the drug substance concentration and the completeness "
              "of the buffer exchange.",
           "Executive summary",
           "The outputs of the step are the drug substance concentration and the completeness of "
           "the buffer exchange"),
        st(4, "The buffer exchange is complete over the whole diavolume range studied: both edges "
              "leave the residual process buffer component far below what the formulation "
              "tolerates.",
           "Buffer exchange",
           "both edges leave that residual far below what the formulation tolerates"),
        st(5, "The number of diavolumes, the transmembrane pressure and the final drug substance "
              "concentration were all classified as key process parameters.",
           "Parameter classification",
           "parameters of the step were therefore classified as key process parameters (KPP)"),
        st(6, "No parameter of the step was classified as critical, as well-controlled critical or "
              "as general, because none of them affects a critical quality attribute.",
           "Parameter classification",
           "No parameter of this step was classified as critical or as well-controlled critical, "
           "and none was classified as a general process parameter"),
        st(7, "The step has no design space; it is described by its operating ranges and by the "
              "proven acceptable ranges of the parameters instead.",
           "Operating ranges in place of a design space", "This step has no design space"),
        st(8, "No designed experiment was run at the step: the risk assessment assigned no "
              "parameter of it to one, and no statistical model was fitted.",
           "Statistical methods",
           "A model requires a designed experiment, and the risk assessment assigned no parameter "
           "of this step to one"),
        # Replaces the deferred-formulation statement the previous report carried: the
        # re-authored report does not mention formulation characterization at all, and this
        # is the finding that takes its place in the summary.
        st(9, "There is no characterized margin below the normal operating range for the "
              "diavolume count or for transmembrane pressure, because the lower edge of the "
              "normal operating range sits on the lower edge of the characterized range for both.",
           "Factors, ranges and the knowledge space",
           "For the diavolume count and for transmembrane pressure the lower edge of the normal "
           "operating range sits on the lower edge of the characterized range, so there is no "
           "characterized margin below the normal operating range for either"),
        st(10, "The outcome of the step rolls up into the Process Characterization Master Report "
               "(PCMR-001).",
            "Conclusions", "its outcome rolls up into PCMR-001"),
    ])]


def uf_proven_acceptable_ranges(doc_id, file_name):
    """One ProvenAcceptableRange per parameter (report only).

    The step governs no quality attribute, so the acceptance basis is the process-performance
    criteria of PCP-010 rather than a drug-substance specification, and the report states that
    the PAR of each parameter is its full characterization range. There is no fitted
    response-surface model, so ``par_nor_propagated`` is deliberately null."""
    sec = "Proven acceptable ranges"
    sid = f"{doc_id}_sec_par"
    # The report has no @tbl-par: it states that the PAR of each parameter IS its
    # characterization range in @tbl-params, so that row is where the range lives. The
    # sentence saying so held every record before, and named no parameter.
    rows = param_rows(UFUO, True)
    out = []
    for i, r in enumerate(UFPARAM_ROWS, 1):
        name, unit = r["parameter"], r["unit"]
        rng = f"{r['par_low']:g}–{r['par_high']:g} {unit}"
        out.append(S.ProvenAcceptableRange(
            par_id=f"{doc_id}-PAR{i:02d}", unit_operation=UFUO_NAME,
            # Left UNSET: the step governs no CQA, so its PARs are per-parameter.
            # schema_ext makes the field Optional precisely for the two non-DoE steps.
            quality_attribute=None,
            parameter=name, characterization_range=rng, par_at_setpoint=rng,
            par_nor_propagated=None,
            acceptance_basis="The range over which the parameter was assessed and over which the "
                             "step delivered drug substance at target concentration with the "
                             "buffer exchange complete and with no resolvable change in the "
                             "monitored attributes. The step governs no critical quality "
                             "attribute and no model was fitted, so no range is back-calculated "
                             "from an attribute limit and no NOR-propagated analysis was run.",
            source_references=[ref(doc_id, file_name, sid, sec, rows[name],
                                   table_id=f"{doc_id}_tab_params",
                                   table_header=rows.header),
                               ref(doc_id, file_name, sid, sec, UFPAR_QUOTE[name])],
            metadata=meta()))
    return out


def uf_inventory(doc_id, file_name, dtype):
    return S.DocumentInventoryItem(
        document_id=doc_id, file_name=file_name, predicted_document_type=dtype,
        product_name_candidates=["A-Mab"], process_name_candidates=[UFUO_NAME],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "ultrafiltration", "diafiltration",
                     "formulation", "tangential-flow filtration", "parameter classification"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc_id][0]}'.",
        source_references=[ref(doc_id, file_name, "Title block", "Title block",
                               title_block_quote(doc_id))],
        metadata=meta())


def build_plan_ufdf():
    doc, f = "PCP-010", PCP10_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_uo",
                                  process_steps=[uf_step(doc, f, f"{doc}_sec_uo", report=False)],
                                  equipment=uf_equipment(doc, f, f"{doc}_sec_uo", report=False),
                                  sites=uf_sites(doc, f, f"{doc}_sec_uo")),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=uf_params(doc, f, f"{doc}_sec_param", classified=False)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=uf_methods(doc, f, f"{doc}_sec_methods", report=False)),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "UF/DF forms and clears no drug-substance product-quality CQA; no QualityAttribute "
            "entities and no DesignSpace are present. The two attributes of @tbl-cqa are monitored "
            "only, and are carried as concepts plus step_has_quality_attribute assertions.",
            "No DoE: the plan states that no screening and no response-surface design is planned "
            "and that no design space will be claimed, so the only studies are the univariate "
            "ranging and the scale-down qualification.",
            "Process-performance measures (buffer exchange, final concentration, step yield, mass "
            "balance) have no dedicated field; captured via studies/report_sections/assertions.",
            "Formulation characterization is deferred to the drug product development programme "
            "(scope boundary in PTP-001); it is out of scope of this drug-substance pair.",
            "The Plan states classification is an OUTPUT; parameter_type left 'unclassified' here.",
        ],
        inventory=uf_inventory(doc, f, "process_characterization_plan"),
        entities=entities,
        studies=uf_studies(doc, f, report=False),
        report_sections=uf_report_sections(doc, f, report=False),
        assertions=uf_assertions(doc, f, report=False), concepts=uf_concepts())


def build_report_ufdf():
    doc, f = "PCR-010", PCR10_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_exec",
                                  process_steps=[uf_step(doc, f, f"{doc}_sec_exec", report=True)],
                                  equipment=uf_equipment(doc, f, f"{doc}_sec_exec", report=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=uf_params(doc, f, f"{doc}_sec_param", classified=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=uf_methods(doc, f, f"{doc}_sec_methods", report=True)),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT + [
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "UF/DF forms and clears no drug-substance product-quality CQA; no QualityAttribute "
            "entities and no DesignSpace are present — the report opens its ranges section with "
            "'This step has no design space' and gives the reason.",
            "No DoE was run and none was required by RA-001, so the only StudyDesign records are "
            "the univariate ranging and the scale-down qualification; there are no screening or "
            "response-surface effect/coefficient objects to annotate.",
            "ProvenAcceptableRange requires a quality attribute; this step governs none, so the "
            "field records that explicitly and par_nor_propagated is null (no fitted model to "
            "propagate the NOR through).",
            "Process-performance results (step yield, mass balance, final concentration) have no "
            "dedicated field; reported as report_sections statements.",
            "rhetorical_spans are verbatim report prose; PCR-010 carries no weak_claims.",
        ],
        inventory=uf_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=uf_studies(doc, f, report=True),
        proven_acceptable_ranges=uf_proven_acceptable_ranges(doc, f),
        report_sections=uf_report_sections(doc, f, report=True),
        assertions=uf_assertions(doc, f, report=True), concepts=uf_concepts(),
        rhetorical_spans=build_rhetorical_spans(doc, f))


# =========================================================================== #
# PTP-001 — Process Transfer Plan (Cambridge Development -> Grafton Commercial). #
# --------------------------------------------------------------------------- #
# A corpus-spanning document (not a single unit op): the ground truth captures  #
# the two sites, the process train (Steps 3-10), the CQAs preserved across the  #
# transfer, and — the distinctive object for this document type — the transfer  #
# gaps (TransferGap + transfer_has_gap assertions).                              #
# =========================================================================== #
PTP_FILE = "PTP-001_transfer.docx"

# The six transfer gaps of PTP-001 §8, each stated adverse-first with its impact on the
# transfer, the action that closes it and the owner of that action. None is closed by the
# plan itself, so every status is "open".
# (gap_id, gap_area, description, impact, mitigation, status,
#  prose-quote (§8 narrative), table-quote (Table 10 gap label), action-quote (Table 10 action))
PTP_GAPS = [
    # Rebuilt 2026-08-21 (TASK-037) against the re-authored transfer plan. The gap register is
    # not a re-wording of the previous one: the plan now carries SEVEN gaps against the previous
    # six, drops the "no point in the design space will have been run at commercial scale" and
    # "Protein A resin has no platform bridging" entries, and adds the harvest/UF-DF design gap
    # and the buffer preparation gap. Table 9 renders Gap | Impact | Action that closes it |
    # Owner, so the table quote is the gap label and the action quote is the action cell.
    # (gap_id, gap_area, description, impact, mitigation, status,
    #  prose-quote (§8 narrative), table-quote (Table 9 gap label), action-quote (Table 9 action))
    ("GAP-01", "process",
     "The scale-down models are qualified against the development train only, so every "
     "characterization conclusion reaches commercial scale through the model rather than "
     "through a commercial batch.",
     "Characterization conclusions reach commercial scale only through the model.",
     "Qualify each model against the receiving-site equipment train and record the comparison "
     "in the characterization plan for the step; owned by MSAT at the sending site.",
     "open",
     "The first two gaps set the schedule, because each requires laboratory work at a site that "
     "has not yet performed it",
     "Scale-down models are qualified against the development train only",
     "Qualify each model against the receiving site equipment train, and record the comparison "
     "in the characterization plan for the step"),
    ("GAP-02", "analytical_method",
     "The validated analytical methods are not qualified at the receiving site.",
     "Comparability results and in-process results cannot be generated or interpreted at the "
     "receiving site.",
     "Transfer and requalify every method under a written protocol; owned by Analytical "
     "Development.",
     "open",
     "neither can be closed by a document review",
     "Analytical methods are not qualified at the receiving site",
     "Transfer and requalify every method in Table 8 under a written protocol"),
    ("GAP-03", "process",
     "Harvest and clarification and the ultrafiltration and diafiltration step carry no "
     "multivariate design, so their operating ranges rest on univariate work and platform "
     "experience.",
     "Operating ranges for these two steps rest on univariate work and platform experience.",
     "State the limitation in PCP-004 and PCP-010 and support the ranges with univariate data "
     "and prior knowledge; owned by MSAT at the sending site.",
     "open",
     "The gap on harvest and UF/DF will still be open when the campaign ends, because no "
     "multivariate design is planned for either step at any point in the programme",
     "Harvest and UF/DF carry no multivariate design",
     "State the limitation in PCP-004 and PCP-010, and support the ranges with univariate data "
     "and prior knowledge"),
    ("GAP-04", "control_strategy",
     "Parameter classification is not established until PCMR-001 is approved, so the master "
     "batch record cannot be finalized before then.",
     "The master batch record cannot be finalized.",
     "Draft the batch record after PCMR-001 is approved and run engineering batches against the "
     "process description; owned by MSAT at the receiving site.",
     "open",
     "The remaining gaps are closed by sequencing, by training or by a bounded qualification "
     "study",
     "Parameter classification is not established until PCMR-001 is approved",
     "Draft the batch record after PCMR-001 is approved, and run engineering batches against the "
     "process description"),
    ("GAP-05", "process",
     "Buffer preparation moves from per-experiment preparation at the sending site to central "
     "preparation and hold at the receiving site.",
     "Buffer hold time and stability are not covered by development data.",
     "Qualify buffer hold times at the receiving site before the engineering batches; owned by "
     "MSAT at the receiving site.",
     "open",
     "none of them requires a change to the process itself",
     "Buffer preparation moves from per experiment preparation to central preparation and hold",
     "Qualify buffer hold times at the receiving site before the engineering batches"),
    ("GAP-06", "validation",
     "The viral clearance claims are established at small scale only and cannot be verified at "
     "commercial scale.",
     "The claims cannot be verified at commercial scale.",
     "Retain the modular small-scale claims and control the load conditions they depend on "
     "through the batch record; owned by MSAT at the sending site.",
     "open",
     "A gap must be closed before the qualification campaign starts, or its residual risk must "
     "be assessed and accepted under the quality system",
     "Viral clearance claims are established at small scale only",
     "Retain the modular small scale claims, and control the load conditions they depend on "
     "through the batch record"),
    ("GAP-07", "quality_system",
     "Operators at the receiving site have not run this process.",
     "An execution error during qualification would invalidate a batch.",
     "Train operators on the master batch record and run engineering batches before "
     "qualification; owned by Manufacturing at the receiving site.",
     "open",
     "Gaps were identified by comparing what the receiving site holds today against what the "
     "qualification campaign requires",
     "Operators at the receiving site have not run this process",
     "Train operators on the master batch record and run engineering batches before "
     "qualification"),
]
PTP_GAP_TABLE = ("Transfer gaps, closing actions, owners and the evidence that closes each",
                 "PTP-001_tab_gaps")
PTP_STEP_KEYS = list(P.CFG.train_order)
PTP_CQA_ROWS = P.cqa_reg.to_dict("records")


def ptp_inventory():
    return S.DocumentInventoryItem(
        document_id="PTP-001", file_name=PTP_FILE, predicted_document_type="process_transfer_plan",
        product_name_candidates=["A-Mab"], process_name_candidates=["A-Mab drug substance"],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["technology transfer", "process transfer", "site equivalency",
                     "gap analysis", "PPQ", "control strategy"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY['PTP-001'][0]}'.",
        source_references=[ref("PTP-001", PTP_FILE, "Title block", "Title block",
                               title_block_quote("PTP-001"))],
        metadata=meta())


def ptp_sites():
    return [
        S.ManufacturingSite(site_id="site:cambridge", site_name=P.SENDING_SITE, site_role="sending",
                            location="Cambridge, MA",
                            source_references=[ref("PTP-001", PTP_FILE, "PTP-001_sec_sites",
                                                   "Sending and receiving sites", "Cambridge, MA")],
                            metadata=meta()),
        S.ManufacturingSite(site_id="site:grafton", site_name=P.RECEIVING_SITE, site_role="receiving",
                            location="Grafton, WI",
                            source_references=[ref("PTP-001", PTP_FILE, "PTP-001_sec_sites",
                                                   "Sending and receiving sites", "Grafton, WI")],
                            metadata=meta()),
    ]


def ptp_steps():
    rows = train_row_quotes()
    out = []
    for key in PTP_STEP_KEYS:
        uo = P.CFG.unit_op(key)
        title = P.UNIT_OP_TITLES.get(key, uo.name)
        out.append(S.ProcessStep(
            step_id=f"step:{key}", step_name=title, step_number=str(uo.step),
            unit_operation=title, description=P.UNIT_OP_ROLE.get(key, ""),
            source_references=[ref("PTP-001", PTP_FILE, "PTP-001_sec_process",
                                   "Product and process description", rows[key],
                                   table_title="The A-Mab drug substance process train and the "
                                               "principal role of each step",
                                   table_id="PTP-001_tab_train")],
            metadata=meta()))
    return out


def ptp_cqas():
    # PTP-001 renders the whole register as @tbl-cqa. The bare attribute name grounded and
    # attested nothing: it names the record and says none of what the record claims.
    rows = cqa_rows(list(P.cqa_reg["key"]))
    out = []
    for r in PTP_CQA_ROWS:
        out.append(S.QualityAttribute(
            attribute_id=f"attr:{r['key']}", attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"], acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref("PTP-001", PTP_FILE, "PTP-001_sec_process",
                                   "Product and process description", rows[r["key"]],
                                   table_header=rows.header,
                                   table_title="A-Mab drug substance quality attributes, "
                                               "acceptance criteria and criticality",
                                   table_id="PTP-001_tab_cqa")],
            metadata=meta()))
    return out


def ptp_gaps():
    """The six §8 gaps: narrative anchor + the Table 10 gap label for each."""
    out = []
    tab_title, tab_id = PTP_GAP_TABLE
    for gid, area, desc, impact, mit, status, prose_q, table_q, _action_q in PTP_GAPS:
        out.append(S.TransferGap(
            gap_id=gid, gap_area=area, description=desc, impact=impact, mitigation=mit,
            status=status,
            source_references=[
                ref("PTP-001", PTP_FILE, "PTP-001_sec_gaps", "Gap analysis", prose_q),
                ref("PTP-001", PTP_FILE, "PTP-001_sec_gaps", "Gap analysis", table_q,
                    table_title=tab_title, table_id=tab_id),
            ],
            metadata=meta()))
    return out


def ptp_concepts():
    from annex_contract.concepts import Concept, ConceptStore
    cs = [Concept(concept_id="process:amab_ds", concept_type="PROCESS",
                  canonical_name="A-Mab drug-substance process",
                  aliases=["A-Mab DS process", "A-Mab drug substance"], review_status="human_verified")]
    for key in PTP_STEP_KEYS:
        uo = P.CFG.unit_op(key)
        cs.append(Concept(concept_id=f"step:{key}", concept_type="PROCESS_STEP",
                          canonical_name=P.UNIT_OP_TITLES.get(key, uo.name),
                          aliases=[key, f"Step {uo.step}"], review_status="human_verified"))
    for r in PTP_CQA_ROWS:
        cs.append(Concept(concept_id=f"attr:{r['key']}", concept_type="QUALITY_ATTRIBUTE",
                          canonical_name=r["cqa"], aliases=[r["key"]], review_status="human_verified"))
    for sid, name in [("site:cambridge", P.SENDING_SITE), ("site:grafton", P.RECEIVING_SITE)]:
        cs.append(Concept(concept_id=sid, concept_type="MANUFACTURING_SITE", canonical_name=name,
                          review_status="human_verified"))
    return ConceptStore(run_id="gt-ptp", concepts=cs)


def ptp_assertions():
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote, table_title=None, table_id=None,
            table_header=None):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"PTP-001-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref("PTP-001", PTP_FILE, "PTP-001_sec", sec, quote,
                                   table_title=table_title, table_id=table_id,
                                   table_header=table_header)],
            metadata=meta()))

    train_rows = train_row_quotes()
    for key in PTP_STEP_KEYS:
        uo = P.CFG.unit_op(key)
        title = P.UNIT_OP_TITLES.get(key, uo.name)
        add("process:amab_ds", "process_has_step", f"step:{key}",
            f"The A-Mab drug-substance process has the step {title}.",
            "Product and process description", train_rows[key],
            table_header=train_rows.header,
            table_title="The A-Mab drug substance process train and the principal role of each step",
            table_id="PTP-001_tab_train")
    # transfer -> gap, anchored on the closing action recorded for the gap in Table 10.
    tab_title, tab_id = PTP_GAP_TABLE
    for gid, area, desc, impact, mit, status, prose_q, table_q, action_q in PTP_GAPS:
        add("transfer:amab_ds", "transfer_has_gap", f"gap:{gid}",
            f"The transfer has {area} gap {gid}: {desc}", "Gap analysis", action_q,
            table_title=tab_title, table_id=tab_id)
    # a couple of preserved-CQA acceptance-criterion links. The cumulative viral-clearance
    # limits carry their own sentence in §2; HCP is anchored on the Table 4 lead-in.
    # Re-anchored 2026-08-21 onto the re-authored §2 lead-in to Table 4, which is the span that
    # names the attributes together with the criterion and the criticality each one carries.
    acc_quote = {
        "lrv_mvm": "The drug substance from those batches will be compared against the acceptance "
                   "criteria in Table 4",
        "hcp": "Table 4 lists the 10 quality attributes that the transfer must preserve, with the "
               "acceptance criterion and the criticality assigned to each",
    }
    for key in ["lrv_mvm", "hcp"]:
        r = P.cqa_reg[P.cqa_reg.key == key].iloc[0].to_dict()
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{key}_acc",
            f"{r['cqa']} acceptance: {r['acc_low']:g}–{r['acc_high']:g} {r['unit']}.",
            "Product and process description", acc_quote[key])
    return AssertionStore(run_id="gt-PTP-001", assertions=A, rationales=[])


def ptp_report_sections():
    from annex_contract.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"PTP-001-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref("PTP-001", PTP_FILE, "PTP-001_sec", sec, quote)])
    return [ReportSection(section_id="PTP-001-summary", title="Transfer plan summary", statements=[
        st(1, "PTP-001 governs the transfer of the A-Mab drug-substance manufacturing process from "
              "the sending development site to the receiving commercial drug-substance site.",
           "Purpose and scope",
           "This plan governs the transfer of the A-Mab drug substance manufacturing process"),
        st(2, "PTP-001 is the parent document of the A-Mab process characterization package: RA-001, "
              "PCMP-001, the per-step plans and reports and PCMR-001 all derive from it.",
           "Purpose and scope",
           "This plan is the parent document of the A-Mab process characterization package"),
        # Rewritten 2026-08-21: the re-authored plan does not state its prospectivity as a claim
        # about itself. What it does say is what the package is for, which is the supportable form.
        st(3, "Each plan in the package commits a study and each report records what that study "
              "found, and the set exists to justify the operating ranges and the control strategy "
              "the receiving site will run.",
           "Purpose and scope",
           "each report records what that study found, and the set as a whole exists to justify "
           "the operating ranges and the control strategy that the receiving site will run"),
        st(4, "The transfer covers the manufacturing process, the analytical methods that test "
              "the intermediates and the drug substance, and the control strategy that connects "
              "the two.",
           "Purpose and scope",
           "The transfer covers the manufacturing process, the analytical methods that test the "
           "intermediates and the drug substance, and the control strategy that connects the two"),
        # Rewritten 2026-08-21: the re-authored plan does not gloss the ICH Q10 definition of
        # technology transfer. It states what this plan governs, which is the same relation
        # between the two sites without the definitional frame.
        st(5, "The plan governs the transfer of the A-Mab drug substance manufacturing process "
              "from the development site to the commercial manufacturing site.",
           "Purpose and scope",
           "This plan governs the transfer of the A-Mab drug substance manufacturing process from "
           "the development site to the commercial manufacturing site"),
        st(6, "The characterization scope table gives, per unit operation, how many parameters "
              "enter the campaign and how the study type splits between multivariate and "
              "univariate work.",
           "Scale-down model and comparability strategy",
           "how many parameters enter the campaign, how the study type splits between "
           "multivariate and univariate work"),
        # Rewritten 2026-08-21: the re-authored plan makes the same point through the gap
        # register rather than through a claim about the process description, so the statement
        # follows the register.
        st(7, "Parameter classification is not established until PCMR-001 is approved, so the "
              "master batch record cannot be finalized before then.",
           "Gap analysis",
           "Parameter classification is not established until PCMR-001 is approved"),
        # Rewritten 2026-08-21: the register now carries SEVEN gaps, not six, and the plan no
        # longer says none is closed by it. It says a gap must be closed before qualification
        # starts or its residual risk assessed and accepted.
        st(8, "Gaps were identified by comparing what the receiving site holds today against what "
              "the qualification campaign requires, and a gap must be closed before the campaign "
              "starts or its residual risk assessed and accepted under the quality system.",
           "Gap analysis",
           "A gap must be closed before the qualification campaign starts, or its residual risk "
           "must be assessed and accepted under the quality system"),
        st(9, "Characterization is the Stage 1 process design work of the validation lifecycle "
              "and process performance qualification is Stage 2, which follows this transfer.",
           "Process performance qualification strategy",
           "Characterization is the Stage 1 process design work of that lifecycle, and process "
           "performance qualification is Stage 2"),
    ])]


def build_transfer_plan():
    doc, f = "PTP-001", PTP_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_sites", sites=ptp_sites()),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_process",
                                  process_steps=ptp_steps(), quality_attributes=ptp_cqas()),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Transfer plan spans the whole process train; entities are the sites, the Step 3-10 process steps and the CQAs preserved across the transfer.",
            "The distinctive objects are the TransferGap entries (transfer_has_gap assertions); each gap is anchored twice, on its §8 narrative statement and on its row of the gap table.",
            "Strictly prospective: the document reports no characterization outcome, so the annex carries no parameter classification, no capability and no design space. The only counts asserted are the prospective study-type allocation (multivariate / univariate).",
        ],
        inventory=ptp_inventory(),
        entities=entities,
        transfer_gaps=ptp_gaps(),
        report_sections=ptp_report_sections(),
        assertions=ptp_assertions(), concepts=ptp_concepts())


# =========================================================================== #
# RA-001 — Pre-Characterization Process Risk Assessment.                        #
# --------------------------------------------------------------------------- #
# Corpus-spanning, pre-characterization: the ground truth captures the CQA       #
# criticality framework, the process parameters as prospective risk subjects     #
# (parameter_type left 'unclassified' — classification is an OUTPUT of the        #
# studies), and the parameter -> CQA-at-risk relations that drive the            #
# study-type assignment. Reuses the curated CONTENT via ra_content.              #
# =========================================================================== #
RA_FILE = "RA-001_risk_assessment.docx"
RA_ATTR_NAME = {r["key"]: r["cqa"] for _, r in P.cqa_reg.iterrows()}
# The two steps whose parameters reach no quality attribute state that fact in their own
# §4 subsection; those sentences anchor the performance-only (non-impact) assertions.
# Header of the leading columns each RA-001 partial row covers. A partial row needs a
# partial header: the two must have the same number of cells or the header mislabels them.
# Re-cut 2026-08-21 (TASK-037): the re-authored RA-001 renders ra_content.ra_detail_df() per
# step with the Step column dropped, so the row carries the EFFECT between the failure mode
# and the attributes, and the last column is named "CQA(s) at risk".
RA_RANK_HEADER = _join_cells(["Parameter", "Potential failure mode", "Potential effect",
                              "CQA(s) at risk"])
RA_ASSIGN_HEADER = _join_cells(["Unit operation", "Parameter"])
RA_CQA_HEADER_3 = _join_cells(["Quality attribute", "Category", "Acceptance"])

# Re-anchored 2026-08-21 (TASK-037). The re-authored RA-001 does not assert the absence in the
# abstract for either step. It states the mechanism that makes each failure a performance failure
# and not a quality one, so the anchor is that mechanism sentence.
RA_PERF_STEP_QUOTE = {
    "harvest": "A depth filter loaded beyond its rated area passes particulate instead of "
               "retaining it, and the turbidity of the clarified harvest rises",
    "ufdf": "a transmembrane pressure outside its range changes the processing time rather than "
            "the material",
}


def ra_cqa_entities():
    # One strong anchor beats two weak ones: the rendered register row names the attribute,
    # its acceptance criterion, its criticality, the Tool #1 score, the severity it confers
    # and the step that sets it — every field this record carries.
    import ra_content as RC
    rows = row_quotes(RC.cqa_table(), P.cqa_reg["key"])
    out = []
    for r in P.cqa_reg.to_dict("records"):
        out.append(S.QualityAttribute(
            attribute_id=f"attr:{r['key']}", attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"], acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            rationale_for_criticality=f"A-Mab Tool #1 = Impact × Uncertainty = {int(r['tool1_score'])}; "
                                      f"Tool #2 severity = {int(r['tool2_severity'])}.",
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[
                ref("RA-001", RA_FILE, "RA-001_sec_cqa", "Quality attributes at risk",
                    rows[r["key"]],
                    table_title="Quality attributes, criticality and the severity each confers",
                    table_id="RA-001_tab_cqa", table_header=rows.header),
            ],
            metadata=meta()))
    return out


def ra_param_entities(rows):
    out = []
    for r in rows:
        p = P.CFG.unit_op(r["key"]).param(r["pkey"])
        prio = r["priority"]
        rationale = (f"Prospective (pre-characterization) risk: could impact {r['cqa_label']} "
                     f"(severity {r['severity']}); assigned to {r['study']}. "
                     f"Classification is an output of the study."
                     if r["quality"] else
                     f"No credible CQA risk; affects process performance only; assigned to {r['study']}.")
        out.append(S.ProcessParameter(
            parameter_id=f"param:{r['key']}_{r['pkey']}", parameter_name=r["param"],
            parameter_type="unclassified", unit=p.unit, target_value=f"{p.setpoint:g}",
            NOR=f"{p.nor[0]:g}–{p.nor[1]:g} {p.unit}",
            PAR=f"{p.prange[0]:g}–{p.prange[1]:g} {p.unit}",
            associated_step=f"{r['unit_op']} (Step {r['step']})",
            rationale_for_criticality=rationale,
            source_references=[
                # the parameter's row of the per-step ranking table: parameter, prospective
                # failure mode and the attribute(s) that failure mode could reach
                ref("RA-001", RA_FILE, "RA-001_sec_rank",
                    "Parameter risk ranking by unit operation",
                    _join_cells([r["param"], r["fm"], r["eff"], r["cqa_label"]]),
                    table_title=f"Pre-characterization risk ranking, {r['unit_op']}",
                    table_id=f"RA-001_tab_rank_{r['key']}", table_header=RA_RANK_HEADER),
                # the parameter's row of the campaign-wide assignment table
                ref("RA-001", RA_FILE, "RA-001_sec_assign", "Characterization study assignment",
                    _join_cells([r["unit_op"], r["param"]]),
                    table_title="Characterization study assignment for every parameter",
                    table_id="RA-001_tab_assign", table_header=RA_ASSIGN_HEADER),
            ],
            metadata=meta()))
    return out


def ra_concepts(rows):
    from annex_contract.concepts import Concept, ConceptStore
    cs = []
    seen_steps = []
    for r in rows:
        if r["key"] not in seen_steps:
            seen_steps.append(r["key"])
            cs.append(Concept(concept_id=f"step:{r['key']}", concept_type="PROCESS_STEP",
                              canonical_name=r["unit_op"],
                              aliases=[r["key"], f"Step {r['step']}"],
                              review_status="human_verified"))
        cs.append(Concept(concept_id=f"param:{r['key']}_{r['pkey']}",
                          concept_type="PROCESS_PARAMETER", canonical_name=r["param"],
                          review_status="human_verified"))
    for key, name in RA_ATTR_NAME.items():
        cs.append(Concept(concept_id=f"attr:{key}", concept_type="QUALITY_ATTRIBUTE",
                          canonical_name=name, aliases=[key], review_status="human_verified"))
    return ConceptStore(run_id="gt-ra", concepts=cs)


def ra_assertions(quality_rows, perf_rows):
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def rref(sec_id, sec_title, quote, table_title=None, table_id=None, table_header=None):
        return ref("RA-001", RA_FILE, sec_id, sec_title, quote,
                   table_title=table_title, table_id=table_id, table_header=table_header)

    def add(subj, pred, obj, text, refs):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"RA-001-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text, source_references=refs, metadata=meta()))

    def rank_ref(r):
        """The parameter's row of its step ranking table: parameter, failure mode, attributes.

        The leading cells of the rendered row, joined the way the document reads back
        (``_join_cells``); the trailing severity and RPN cells are outside the relation this
        reference attests."""
        return rref("RA-001_sec_rank", "Parameter risk ranking by unit operation",
                    _join_cells([r["param"], r["fm"], r["eff"], r["cqa_label"]]),
                    table_title=f"Pre-characterization risk ranking, {r['unit_op']}",
                    table_id=f"RA-001_tab_rank_{r['key']}", table_header=RA_RANK_HEADER)

    def assign_ref(r):
        """The parameter's row of the campaign-wide study-assignment table."""
        return rref("RA-001_sec_assign", "Characterization study assignment",
                    _join_cells([r["unit_op"], r["param"]]),
                    table_title="Characterization study assignment for every parameter",
                    table_id="RA-001_tab_assign", table_header=RA_ASSIGN_HEADER)

    # step -> parameter: every parameter assessed here belongs to a named unit operation and
    # leaves this document with a study type (the assessment's actual output).
    for r in quality_rows + perf_rows:
        add(f"step:{r['key']}", "step_has_parameter", f"param:{r['key']}_{r['pkey']}",
            f"{r['unit_op']} has process parameter {r['param']}, which this assessment assigns to "
            f"{r['study']}.", [assign_ref(r)])
    # attribute -> acceptance criterion: the register that confers severity on the parameters.
    for r in P.cqa_reg.to_dict("records"):
        add(f"attr:{r['key']}", "attribute_has_acceptance_criterion", f"lit:{r['key']}_acc",
            f"{r['cqa']} acceptance: {r['acc_low']:g}–{r['acc_high']:g} {r['unit']}.",
            [rref("RA-001_sec_cqa", "Quality attributes at risk",
                  _join_cells([r["cqa"], r["category"],
                               f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"]),
                  table_title="Quality attributes, criticality and the severity each confers",
                  table_id="RA-001_tab_cqa", table_header=RA_CQA_HEADER_3)])
    # parameter -> attribute AT RISK. Prospective only: the failure mode is postulated and the
    # attribute is the one it could reach, not one the parameter is shown to move.
    for r in quality_rows:
        pid = f"param:{r['key']}_{r['pkey']}"
        for cqa_key in r["cqas"]:
            add(pid, "parameter_impacts_attribute", f"attr:{cqa_key}",
                f"{r['param']} carries a prospective (pre-characterization) risk to "
                f"{RA_ATTR_NAME.get(cqa_key, cqa_key)}: the postulated failure mode could reach "
                f"the attribute, and the size of the effect is not yet measured.",
                [rank_ref(r)])
    # performance-only parameters: no credible route to any quality attribute.
    for r in perf_rows:
        pid = f"param:{r['key']}_{r['pkey']}"
        add(pid, "parameter_does_not_significantly_impact_attribute", "attr:aggregates_hmw",
            f"{r['param']} has no credible route to a quality attribute and is ranked at the "
            f"process-performance severity band.",
            [rref("RA-001_sec_rank", "Parameter risk ranking by unit operation",
                  RA_PERF_STEP_QUOTE[r["key"]]), rank_ref(r)])
    return AssertionStore(run_id="gt-RA-001", assertions=A, rationales=[])


def ra_report_sections():
    from annex_contract.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"RA-001-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref("RA-001", RA_FILE, "RA-001_sec", sec, quote)])
    # Re-anchored and rewritten 2026-08-21 (TASK-037) against the re-authored risk assessment.
    # Every statement was read back against the new text. The document no longer states its own
    # prospectivity, no longer names the "justified univariate" class in its campaign totals
    # (it folds that parameter into the univariate count, giving 22 and 15 against the previous
    # 22, 14 and 1), and no longer carries a sentence about amending the assignment. Statements
    # that asserted those things are replaced by what the document does say.
    return [ReportSection(section_id="RA-001-summary", title="Risk assessment summary", statements=[
        st(1, "RA-001 records the risk assessment made on the A-Mab drug substance process before "
              "any characterization study was executed.",
           "Purpose and scope",
           "This document records the risk assessment made on the A-Mab drug substance process "
           "before any characterization study was executed"),
        st(2, "Its consumers are the characterization plans, one per unit operation, which take "
              "the study type assigned here and set out how that study will be run.",
           "Outputs and downstream use",
           "Its consumers are the characterization plans, one for each unit operation, which take "
           "the study type assigned here and set out how that study will be run"),
        st(3, "No parameter is assigned a study type on the risk priority number alone.",
           "Risk assessment methodology",
           "No parameter is assigned a study type on the number alone"),
        st(4, "The scores in the register are initial scores and no residual risk is reported.",
           "Parameter risk ranking by unit operation",
           "Scores are initial scores and no residual risk is reported"),
        st(5, "Where a parameter could affect more than one attribute, the severity of the most "
              "severe of them is used.",
           "Risk assessment methodology",
           "Where a parameter could affect more than one attribute, the severity of the most "
           "severe of them is used"),
        st(6, "Occurrence and detection are assigned before any effect has been measured, and by "
              "class rather than parameter by parameter.",
           "Risk assessment methodology",
           "Occurrence and detection are assigned before any effect has been measured, and they "
           "are assigned by class rather than parameter by parameter"),
        st(7, "The initial risk priority number is the product of the three scores.",
           "Risk assessment methodology",
           "The initial risk priority number is the product of the three scores"),
        st(8, "A viral clearance claim is made from a spiking study on a qualified small scale "
              "model, because neither an in-process control nor a release test on the drug "
              "substance measures the log reduction the hold achieves.",
           "Risk assessment methodology",
           "the claim is made instead from a spiking study on a qualified small scale model"),
        st(9, "Of the 37 parameters, 21 are scored against at least one quality attribute and 16 "
              "against process performance alone.",
           "Parameter risk ranking by unit operation",
           "Of the 37 parameters, 21 are scored against at least one quality attribute and 16 "
           "against process performance alone"),
        st(10, "The highest initial risk priority number in the assessment is reached by three of "
               "the four parameters of one step.",
            "Parameter risk ranking by unit operation",
            "3 reach the top of the register at 700, which is the highest initial risk priority "
            "number in the assessment"),
        st(11, "The campaign scope is 22 parameters in a multivariate design and 15 in univariate "
               "assessment; no parameter is excluded from study.",
            "Characterization study assignment",
            "Of the 37 parameters, 22 are assigned to a multivariate design and 15 to univariate "
            "assessment"),
        st(12, "Across the register the risk priority number runs from 96 to 700 and takes five "
               "distinct values, because occurrence and detection are assigned by class.",
            "Risk assessment methodology",
            "Across the register it runs from 96 to 700 and takes 5 distinct values, because "
            "occurrence and detection are assigned by class"),
        st(13, "An effect that depends on a second parameter cannot be found by moving one "
               "parameter at a time, and that is what sets the study type.",
            "Risk assessment methodology",
            "The second sets the study type, because an effect that depends on a second parameter "
            "cannot be found by moving one parameter at a time"),
        st(14, "The capture study measures leached Protein A in the pool across the designed "
               "experiment, so the ranges this assessment scopes are bounded against it even "
               "though no parameter is ranked on it.",
            "Assumptions and limitations",
            "The capture study measures leached Protein A in the pool across the designed "
            "experiment, so the ranges this assessment scopes are bounded against it even though "
            "no parameter is ranked on it"),
    ])]


def ra_inventory():
    return S.DocumentInventoryItem(
        document_id="RA-001", file_name=RA_FILE, predicted_document_type="risk_assessment",
        product_name_candidates=["A-Mab"], process_name_candidates=["A-Mab drug substance"],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["risk assessment", "risk ranking and filtering", "study-type assignment",
                     "CQA criticality", "process characterization scope", "pre-characterization"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY['RA-001'][0]}'.",
        source_references=[ref("RA-001", RA_FILE, "Title block", "Title block",
                               title_block_quote("RA-001"))],
        metadata=meta())


def build_risk_assessment():
    import ra_content as RC
    rows = RC.ra_rows()
    quality_rows = [r for r in rows if r["quality"]]
    perf_rows = [r for r in rows if not r["quality"] and r["key"] in ("harvest", "ufdf")]
    doc = "RA-001"
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=ra_cqa_entities()),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_assign",
                                  parameters=ra_param_entities(quality_rows + perf_rows)),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Pre-characterization: parameter_type is left 'unclassified' (CPP/WC-CPP/KPP/GPP is an OUTPUT of the studies, not this assessment).",
            "The study-type assignment (multivariate DoE / justified univariate / univariate) and the prospective severity/initial-RPN ranking are reported via report_sections and parameter rationales.",
            "parameter_impacts_attribute here is a PROSPECTIVE (at-risk) relation, not a demonstrated effect; each is anchored on the ranking row that states the postulated failure mode and the attribute it could reach.",
            "No residual RPN and no design space are recorded, because the document states neither: the control strategy that would reduce the risk does not yet exist.",
        ],
        inventory=ra_inventory(),
        entities=entities,
        report_sections=ra_report_sections(),
        assertions=ra_assertions(quality_rows, perf_rows),
        concepts=ra_concepts(quality_rows + perf_rows))


# =========================================================================== #
# PCMP-001 — Process Characterization Master Plan.                              #
# --------------------------------------------------------------------------- #
# Umbrella plan over the per-unit-operation plans. The ground truth captures the #
# process train (Steps 3-10), the CQA framework and the master-plan narrative.   #
# =========================================================================== #
PCMP_FILE = "PCMP-001_master_plan.docx"


def train_row_quotes():
    """Rendered rows of the process-train table, keyed by step.

    PCMP-001, PTP-001 and PCMR-001 all render ``process_steps_df()``, so one set of rows
    serves all three. The row carries the step number, the unit operation and its principal
    role; the bare unit-operation title carries none of that and recurs throughout each
    document as a heading.
    """
    return row_quotes(P.process_steps_df(), P.CFG.train_order)


def _corpus_steps(doc, file, sec_id, sec_title, rows=None, roles=None, table_title=None):
    """One ProcessStep per step of the train, anchored on its row of the process-train table.

    ``rows`` and ``roles`` default to ``process_steps_df()``. A document that prints its own
    version of the table (PCMP-001 Version 2.0 rewrites the harvest role) passes the rows it
    rendered, keyed by step, and the role each row states."""
    rows = train_row_quotes() if rows is None else rows
    roles = P.UNIT_OP_ROLE if roles is None else roles
    out = []
    for key in P.CFG.train_order:
        uo = P.CFG.unit_op(key)
        title = P.UNIT_OP_TITLES.get(key, uo.name)
        out.append(S.ProcessStep(
            step_id=f"step:{key}", step_name=title, step_number=str(uo.step),
            unit_operation=title, description=roles.get(key, ""),
            source_references=[ref(doc, file, sec_id, sec_title, rows[key],
                                   table_title=table_title, table_header=rows.header)],
            metadata=meta()))
    return out


def _corpus_step_concepts():
    from annex_contract.concepts import Concept
    cs = [Concept(concept_id="process:amab_ds", concept_type="PROCESS",
                  canonical_name="A-Mab drug-substance process",
                  aliases=["A-Mab DS process", "A-Mab drug substance"], review_status="human_verified")]
    for key in P.CFG.train_order:
        uo = P.CFG.unit_op(key)
        cs.append(Concept(concept_id=f"step:{key}", concept_type="PROCESS_STEP",
                          canonical_name=P.UNIT_OP_TITLES.get(key, uo.name),
                          aliases=[key, f"Step {uo.step}"], review_status="human_verified"))
    for r in P.cqa_reg.to_dict("records"):
        cs.append(Concept(concept_id=f"attr:{r['key']}", concept_type="QUALITY_ATTRIBUTE",
                          canonical_name=r["cqa"], aliases=[r["key"]], review_status="human_verified"))
    return cs


# build_master_plan() — PCMP-001 Version 2.0 — is in the Version 2.0 section below.


# =========================================================================== #
# PCMR-001 — Process Characterization Master Report (roll-up of PCR-003…010).   #
# --------------------------------------------------------------------------- #
# Consolidates the per-unit-operation reports. Every per-record quote below is   #
# the RENDERED TABLE ROW, rebuilt here from the same seeded register the report  #
# renders (@tbl-train, @tbl-cqa, @tbl-cpp, @tbl-cap, @tbl-viral, @tbl-dev), so   #
# the span literally carries both ends of the relation it anchors and follows    #
# the register on a reseed. Narrative quotes are number-free wherever the number  #
# is not the point. The campaign deviation register (§8.1, 17 rows) has no        #
# upstream model and is captured as rhetorical_spans of role                      #
# 'deviation_disposition', one span per register row.                            #
# =========================================================================== #
PCMR_FILE = "PCMR-001_master_report.docx"

# Editorial labels the report puts in the registers it renders (prose only — every
# number in these tables is read from the seeded CSVs).
PCMR_VC_MECH = {
    "Low-pH Viral Inactivation": "Chemical inactivation of the viral envelope",
    "Anion Exchange (AEX)": "Charge-based partition in flow-through mode",
    "Virus Filtration": "Size-based retention by the membrane",
    "Cumulative": "",
}
PCMR_VC_REPORT = {"Low-pH Viral Inactivation": "PCR-006", "Anion Exchange (AEX)": "PCR-008",
                  "Virus Filtration": "PCR-009", "Cumulative": ""}
PCMR_VC_STEP = {"Low-pH Viral Inactivation": "viral_inactivation",
                "Anion Exchange (AEX)": "aex", "Virus Filtration": "virus_filtration"}
PCMR_DEV_STEP = {"bioreactor": "Bioreactor", "harvest": "Harvest", "protein_a": "Protein A",
                 "viral_inactivation": "Low-pH hold", "cex": "CEX", "aex": "AEX",
                 "virus_filtration": "Virus filtration", "ufdf": "UF/DF"}
# Table captions, used verbatim as the SourceReference.table_title of a row quote.
PCMR_TAB = {
    "train": ("PCMR-001_tab_train", "The A-Mab drug substance process train, with each step's "
                                    "principal role in the control strategy."),
    "cqa": ("PCMR-001_tab_cqa", "Consolidated drug substance quality attribute outcomes."),
    "cap": ("PCMR-001_tab_cap", "Commercial-scale process capability for every drug substance "
                                "quality attribute."),
    "cpp": ("PCMR-001_tab_cpp", "Parameters linked to a quality attribute, with their set-points "
                                "and normal operating ranges."),
    "viral": ("PCMR-001_tab_viral", "Modular viral clearance by step, with the mechanism claimed "
                                    "for each and the report that establishes it."),
    "dev": ("PCMR-001_tab_dev", "The complete deviation register for the characterization "
                                "campaign."),
}


def _md_rows(df, floatfmt=None):
    """Every rendered row of a ``_pcpkg.show``-style table, cells joined by ``CELL_SEP``.

    ``show`` emits ``df.to_markdown(index=False, floatfmt=...)`` and Quarto turns each markdown
    row into a docx table row, which ``check_grounding.docx_text`` reads back with its cell
    boundaries marked as ``" | "``. Rebuilding the row from the same DataFrame therefore
    reproduces the rendered row verbatim — which is what lets a per-record quote span the whole
    relation instead of a generic sentence about it.

    The separator is the cell boundary, not decoration: without it "3 Production Bioreactor
    Forms the glycan ... CQAs" is one undifferentiated span, and a consumer cannot tell which
    token is the step number and which is the role the row assigns it.

    ``floatfmt`` defaults to whatever ``show`` would have chosen for this table
    (``_pcpkg._auto_floatfmt``), because a row rebuilt in a different format is a row that
    does not ground: a 9,000 g set-point rendered as ``9,000`` by the document and as
    ``9e+03`` here matches nothing. Pass it explicitly only where the ``.qmd`` does.
    """
    fmt = floatfmt or P._auto_floatfmt(df)
    return [_join_cells(line.strip().strip("|").split("|"))
            for line in df.to_markdown(index=False, floatfmt=fmt).splitlines()[2:]]


def _grid_rows(df, maxcolwidths):
    """Same, for the deviation register, which §8.1 renders as a wrapped *grid* table.

    tabulate wraps each cell to ``maxcolwidths`` and pandoc joins the wrapped lines of a cell
    into one paragraph, so the rendered row is the wrapped cells concatenated column by column
    (a cell broken at a hyphen therefore renders as e.g. "re- assayed", which this reproduces)
    and then separated by ``CELL_SEP`` like any other row.
    """
    blocks, cur = [], []
    for line in df.to_markdown(index=False, tablefmt="grid",
                               maxcolwidths=maxcolwidths).splitlines():
        if line.startswith("+"):
            if cur:
                blocks.append(cur)
            cur = []
        else:
            cur.append(line)
    if cur:
        blocks.append(cur)
    rows = []
    for blk in blocks[1:]:                       # blocks[0] is the header
        cells = [""] * len(blk[0].strip().strip("|").split("|"))
        for line in blk:
            for i, part in enumerate(c.strip() for c in line.strip().strip("|").split("|")):
                if part:
                    cells[i] = f"{cells[i]} {part}".strip()
        rows.append(_join_cells(cells))
    return rows


def _pcmr_registers():
    """The six registers PCMR-001 renders, as {record key -> rendered row text}."""
    train = train_row_quotes()          # the same rows PCMP-001 and PTP-001 anchor on

    # Re-cut 2026-08-21 (TASK-037) against the re-authored master report, which builds both of
    # these tables itself. The register table is now CQA | Category | Acceptance | Criticality |
    # Tool #1 with no capability columns, and the capability table is CQA | Crit. | Spec |
    # Acceptance | Mean ± SD | Cpk with the raw `two_sided` spelling kept and Cpk to ONE decimal.
    # The previous revision rendered one merged table with "Set by" and Cpk to two decimals.
    out = P.cqa_reg.copy()
    out["Acceptance"] = out.apply(lambda r: f"{r.acc_low:g}–{r.acc_high:g} {r.unit}", axis=1)
    cqa_df = (out.rename(columns={"cqa": "CQA", "category": "Category",
                                  "criticality": "Criticality", "tool1_score": "Tool #1"})
                 [["CQA", "Category", "Acceptance", "Criticality", "Tool #1"]])
    cqa = row_quotes(cqa_df, out.key)

    keys = list(P.cqa_reg["key"])
    cap_tbl = P.cap_for(keys).copy()
    cap_tbl["Cpk"] = cap_tbl["Cpk"].map(lambda v: f"{v:,.1f}")   # the table groups thousands
    cap = row_quotes(cap_tbl, P.cap[P.cap.key.isin(keys)].key, ",.1f")

    q = P.param_reg[P.param_reg.classification.isin(["CPP", "WC-CPP"])]
    par = row_quotes(P.cpp_params(), zip(q.unit_operation, q.parameter))

    # Re-cut 2026-08-21 (TASK-037). The re-authored @tbl-viral drops the Mechanism and Report
    # columns (the mechanisms are given in the prose of §6.2 instead) and renders the log values
    # with %g rather than to two decimals, so 7.10 renders as 7.1 and 0.00 as 0.
    vt = P.csv("viral_clearance.csv").copy()
    viral_df = (vt.rename(columns={"step": "Step", "XMuLV": "XMuLV LRF (log10)",
                                   "MVM": "MVM LRF (log10)"})
                  [["Step", "XMuLV LRF (log10)", "MVM LRF (log10)"]])
    viral = row_quotes(viral_df, vt.step, "g")

    # And the deviation register is now Report | Deviation | Summary | Disposition, with the
    # step and the root cause dropped and the disposition rendered as the raw csv word.
    dv = P.csv("deviations.csv").copy()
    dv["Disposition"] = dv["disposition"].str.replace("_", " ", regex=False)
    dev_df = (dv.rename(columns={"doc_id": "Report", "dev_id": "Deviation",
                                 "summary": "Summary"})
                [["Report", "Deviation", "Summary", "Disposition"]])
    dev = row_quotes(dev_df, dv.dev_id)
    return train, cqa, cap, par, viral, dev


(PCMR_TRAIN_ROW, PCMR_CQA_ROW, PCMR_CAP_ROW,
 PCMR_PAR_ROW, PCMR_VC_ROW, PCMR_DEV_ROW) = _pcmr_registers()

# Which step is credited with which cumulative viral-clearance CQA in @tbl-viral. The low-pH
# hold is deliberately absent from MVM: it contributes 0.00 log10 against a non-enveloped
# parvovirus, and the report says so.
PCMR_VC_CREDIT = [
    ("viral_inactivation", "lrv_xmulv"), ("aex", "lrv_xmulv"), ("aex", "lrv_mvm"),
    ("virus_filtration", "lrv_xmulv"), ("virus_filtration", "lrv_mvm"),
]
PCMR_VC_ROW_FOR = {v: PCMR_VC_ROW[k] for k, v in PCMR_VC_STEP.items()}


def pcmr_dev_spans(doc, f):
    """The 17 rows of the campaign deviation register, as ``deviation_disposition`` spans.

    These stay in code while every other rhetorical span moved to
    ``authoring/rhetorical/*.spans.yaml``: each quote is a rendered row of @tbl-dev built from
    ``outputs/deviations.csv``, so freezing it into a curated file would hard-code data that
    a reseed changes. The curated prose spans of PCMR-001 are in its spans file; these are
    appended to them. Anchoring each row on itself means the disposition of a deviation is
    attested by a span that contains it, not by the section that discusses it.
    """
    out = []
    for dev_id, row in PCMR_DEV_ROW.items():
        out.append(S.RhetoricalSpan(
            span_id=f"{doc}-{dev_id}", section="The register", role="deviation_disposition",
            source_reference=ref(doc, f, f"{doc}_sec_dev", "The register", row,
                                 table_title=PCMR_TAB["dev"][1], table_id=PCMR_TAB["dev"][0]),
            supported_by=[], restates=None, bounds=None))
    return out


def pcmr_steps(doc, f):
    """The Step 3-10 train, each anchored on its row of @tbl-train."""
    out = []
    for key in P.CFG.train_order:
        uo = P.CFG.unit_op(key)
        title = P.UNIT_OP_TITLES.get(key, uo.name)
        out.append(S.ProcessStep(
            step_id=f"step:{key}", step_name=title, step_number=str(uo.step),
            unit_operation=title, description=P.UNIT_OP_ROLE.get(key, ""),
            source_references=[ref(doc, f, f"{doc}_sec_process",
                                   "Process description and performance", PCMR_TRAIN_ROW[key],
                                   table_header=PCMR_TRAIN_ROW.header,
                                   table_title=PCMR_TAB["train"][1],
                                   table_id=PCMR_TAB["train"][0])],
            metadata=meta()))
    return out


def pcmr_cqas(doc, f):
    """The 10 drug-substance CQA outcomes: the @tbl-cqa row (attribute, criticality, acceptance,
    the step the register assigns it to, the simulated DS result) plus the @tbl-cap row."""
    out = []
    for r in P.cqa_reg.to_dict("records"):
        key = r["key"]
        out.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"], acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            associated_steps=[P.UNIT_OP_TITLES.get(r["set_by"], r["set_by"])],
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            rationale_for_criticality=f"A-Mab Tool #1 = Impact × Uncertainty = "
                                      f"{int(r['tool1_score'])}; Tool #2 severity = "
                                      f"{int(r['tool2_severity'])}.",
            source_references=[
                ref(doc, f, f"{doc}_sec_cqa", "Consolidated quality attribute outcomes",
                    PCMR_CQA_ROW[key], table_title=PCMR_TAB["cqa"][1],
                    table_header=PCMR_CQA_ROW.header,
                    table_id=PCMR_TAB["cqa"][0]),
                ref(doc, f, f"{doc}_sec_cap", "Process capability", PCMR_CAP_ROW[key],
                    table_header=PCMR_CAP_ROW.header,
                    table_title=PCMR_TAB["cap"][1], table_id=PCMR_TAB["cap"][0]),
            ],
            metadata=meta()))
    return out


def _pcmr_param_key(uo_name, param_name):
    """(register unit-operation name, register parameter name) -> (step key, parameter key)."""
    for key in P.CFG.train_order:
        uo = P.CFG.unit_op(key)
        if uo.name != uo_name:
            continue
        for p in uo.parameters:
            if p.name == param_name:
                return key, p.key
    return None, None


def pcmr_quality_linked_params():
    """The quality-linked (CPP / WC-CPP) parameters @tbl-cpp restates by name in this report."""
    rows = []
    for r in P.param_reg[P.param_reg.classification.isin(["CPP", "WC-CPP"])].to_dict("records"):
        key, pkey = _pcmr_param_key(r["unit_operation"], r["parameter"])
        rows.append(dict(r, key=key, pkey=pkey,
                         row=PCMR_PAR_ROW[(r["unit_operation"], r["parameter"])]))
    return rows


def pcmr_params(doc, f, rows):
    out = []
    for r in rows:
        out.append(S.ProcessParameter(
            parameter_id=f"param:{r['key']}_{r['pkey']}", parameter_name=r["parameter"],
            parameter_type=r["classification"], unit=r["unit"],
            target_value=f"{r['setpoint']:g}",
            NOR=f"{r['nor_low']:g}–{r['nor_high']:g} {r['unit']}",
            associated_step=f"{r['unit_operation']} (Step {int(r['step'])})",
            rationale_for_criticality=(
                f"Classified {r['classification']} in {r['unit_operation']}: impact on a quality "
                f"attribute demonstrated in the step report; the class is consolidated here, not "
                f"re-derived."),
            source_references=[ref(doc, f, f"{doc}_sec_class", "Parameter classification summary",
                                   r["row"], table_title=PCMR_TAB["cpp"][1],
                                   table_header=PCMR_PAR_ROW.header,
                                   table_id=PCMR_TAB["cpp"][0])],
            metadata=meta()))
    return out


def pcmr_concepts(rows):
    from annex_contract.concepts import Concept
    cs = _corpus_step_concepts()
    for r in rows:
        cs.append(Concept(concept_id=f"param:{r['key']}_{r['pkey']}",
                          concept_type="PROCESS_PARAMETER", canonical_name=r["parameter"],
                          review_status="human_verified"))
    return cs


def build_master_report():
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    from annex_contract.concepts import ConceptStore
    from annex_contract.summaries import ReportSection, ReportStatement
    doc, f = "PCMR-001", PCMR_FILE
    A, n = [], [0]
    # Campaign scope, read from the same seeded registers the report renders (never typed).
    counts = P.class_counts()
    n_par, n_cqa = len(P.param_reg), len(P.cqa_reg)
    n_multi = int((P.param_reg.study == "multivariate").sum())
    n_uni = int((P.param_reg.study == "univariate").sum())
    devs = P.csv("deviations.csv")
    n_dev = int(P.V["n_deviations"])
    n_dev_docs = int(devs.doc_id.nunique())
    n_dev_ret = int((devs.disposition == "retained").sum())
    cap_min = P.cap.loc[P.cap.Cpk.idxmin()]
    q_rows = pcmr_quality_linked_params()

    def add(subj, pred, obj, text, refs):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text, source_references=refs, metadata=meta()))

    def train_ref(key):
        """The step's row of @tbl-train: number, unit operation and its role in the strategy."""
        return ref(doc, f, f"{doc}_sec_process", "Process description and performance",
                   PCMR_TRAIN_ROW[key], table_title=PCMR_TAB["train"][1],
                   table_header=PCMR_TRAIN_ROW.header,
                   table_id=PCMR_TAB["train"][0])

    def cqa_ref(key):
        """The attribute's row of @tbl-cqa: attribute, criticality, acceptance, the step the
        register assigns it to, and the simulated drug-substance result."""
        return ref(doc, f, f"{doc}_sec_cqa", "Consolidated quality attribute outcomes",
                   PCMR_CQA_ROW[key], table_title=PCMR_TAB["cqa"][1],
                    table_header=PCMR_CQA_ROW.header,
                   table_id=PCMR_TAB["cqa"][0])

    def viral_ref(step_key):
        """The step's row of @tbl-viral: mechanism claimed and the log10 credited per virus."""
        return ref(doc, f, f"{doc}_sec_viral", "Viral clearance summary",
                   PCMR_VC_ROW_FOR[step_key], table_title=PCMR_TAB["viral"][1],
                   table_header=PCMR_VC_ROW.header,
                   table_id=PCMR_TAB["viral"][0])

    for key in P.CFG.train_order:
        title = P.UNIT_OP_TITLES.get(key, P.CFG.unit_op(key).name)
        add("process:amab_ds", "process_has_step", f"step:{key}",
            f"The A-Mab drug-substance process has the step {title}.", [train_ref(key)])
    # attribute -> the step the consolidated register assigns it to, and its acceptance criterion.
    # Both are carried by the same @tbl-cqa row, so the span contains both ends of the relation.
    for r in P.cqa_reg.to_dict("records"):
        key, set_by = r["key"], r["set_by"]
        refs = [cqa_ref(key)]
        if (set_by, key) in PCMR_VC_CREDIT:
            refs.append(viral_ref(set_by))
        add(f"step:{set_by}", "step_has_quality_attribute", f"attr:{key}",
            f"{P.UNIT_OP_TITLES.get(set_by, set_by)} is the step the consolidated register "
            f"assigns {r['cqa']} to — the step that forms it, or for a cumulative clearance "
            f"attribute the step that completes the claim.", refs)
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{key}_acc",
            f"{r['cqa']} acceptance: {r['acc_low']:g}–{r['acc_high']:g} {r['unit']}.",
            [cqa_ref(key)])
    # the modular viral-clearance credit that @tbl-cqa does not carry: the contributing steps
    # that are not the register's "set by" step. The low-pH hold is absent from MVM on purpose.
    for step_key, attr_key in PCMR_VC_CREDIT:
        if (step_key, attr_key) in {(r["set_by"], r["key"]) for r in P.cqa_reg.to_dict("records")}:
            continue
        add(f"step:{step_key}", "step_has_quality_attribute", f"attr:{attr_key}",
            f"{P.UNIT_OP_TITLES.get(step_key, step_key)} carries a named, independent module of "
            f"the cumulative clearance claim for "
            f"{P.cqa_reg[P.cqa_reg.key == attr_key].iloc[0]['cqa']}.", [viral_ref(step_key)])
    # step -> the quality-linked parameters the control strategy must hold inside a design space.
    for r in q_rows:
        add(f"step:{r['key']}", "step_has_parameter", f"param:{r['key']}_{r['pkey']}",
            f"{r['unit_operation']} has quality-linked process parameter {r['parameter']}, "
            f"consolidated here as {r['classification']}.",
            [ref(doc, f, f"{doc}_sec_class", "Parameter classification summary", r["row"],
                 table_header=PCMR_PAR_ROW.header,
                 table_title=PCMR_TAB["cpp"][1], table_id=PCMR_TAB["cpp"][0])])

    def stx(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc, f, f"{doc}_sec", sec, quote)])
    # Re-anchored and rewritten 2026-08-21 (TASK-037) against the re-authored master report.
    # Every statement was read back against the new text. The report now folds the 15 retained
    # deviations, the classification counts and the yield into different sentences, states the
    # capability caveats in a section called "The bound on the claims in this report" rather than
    # "Limitations", and ends on readiness rather than on a reading instruction.
    report_sections = [ReportSection(section_id=f"{doc}-summary", title="Master report summary", statements=[
        stx(1, "PCMR-001 consolidates the Stage 1 process characterization of the A-Mab drug "
               "substance process and states the outcome of the campaign as a whole.",
            "Executive summary",
            "This report consolidates the Stage 1 process characterization of the A-Mab drug "
            "substance process and states the outcome of the campaign as a whole"),
        stx(2, f"All {n_cqa} drug substance quality attributes met their acceptance criteria in "
               f"the commercial scale simulation, and every simulated batch met every criterion "
               f"at once.",
            "Executive summary",
            "Every one of the 2,000 simulated batches met every criterion at once"),
        stx(3, "The lowest capability index was 1.51 on cumulative MVM clearance and the next "
               "lowest 1.53 on cumulative XMuLV clearance, both viral safety attributes judged "
               "against a one sided requirement.",
            "Executive summary",
            "The lowest capability index was 1.51 on cumulative MVM clearance, and the next "
            "lowest was 1.53 on cumulative XMuLV clearance"),
        stx(4, "The capability index reported per attribute is the one sided index against the "
               "acceptance limit that applies to that attribute.",
            "Process capability",
            "the capability index is the one sided index against the acceptance limit that "
            "applies to that attribute"),
        stx(5, "Cumulative viral clearance is 18.87 log10 for XMuLV against a requirement of "
               "16.7 log10, and 10.03 log10 for MVM against a requirement of 8.6 log10.",
            "Viral clearance summary",
            "Cumulative viral clearance is 18.87 log10 for XMuLV against a requirement of 16.7 "
            "log10, and 10.03 log10 for MVM against a requirement of 8.6 log10"),
        stx(6, "The cumulative claim is additive only because the crediting steps remove virus by "
               "mechanisms independent of one another, so a virus resistant to one step is not "
               "thereby resistant to the next.",
            "Viral clearance summary",
            "The claim is only additive if the steps remove virus by mechanisms that are "
            "independent of one another, so that a virus resistant to one step is not thereby "
            "resistant to the next"),
        stx(7, "Of the 37 parameters, 1 was classified as a critical process parameter, 20 as "
               "well controlled critical, 10 as key and 6 as general process parameters.",
            "Parameter classification summary",
            "1 was classified as a critical process parameter, 20 as well controlled critical "
            "process parameters, 10 as key process parameters and 6 as general process "
            "parameters"),
        stx(8, "The single critical process parameter is the inactivation pH of Step 6.",
            "Parameter classification summary",
            "The single critical process parameter is the inactivation pH of Step 6"),
        stx(9, "An intermediate carries every impurity at the level the steps before it left, and "
               "the steps that clear the remainder have not yet run, so the drug substance limit "
               "is the wrong yardstick for it.",
            "Overall control strategy",
            "An intermediate carries every impurity at the level the steps before it left, and "
            "the steps that clear the remainder have not yet run"),
        stx(10, "A nominal batch delivers 54.6 kg of drug substance at an overall step yield of "
                "83.2 %.",
            "Process description and performance",
            "A nominal batch delivers 54.6 kg of drug substance at an overall step yield of 83.2 %"),
        stx(11, "Of 17 deviations recorded across the 8 executed studies, 15 were retained with "
                "the affected data kept and a documented impact assessment, 1 invalidated a study "
                "and 1 was corrected by modelling and confirmed by verification runs.",
            "Deviations across the campaign",
            "15 were retained, which means the affected data were kept and the report carries a "
            "documented impact assessment for them"),
        stx(12, "The campaign covered 37 process parameters across 8 unit operations, of which 22 "
                "were studied multivariately in 236 designed runs.",
            "Executive summary",
            "The campaign covered 37 process parameters across 8 unit operations, of which 22 "
            "were studied multivariately in 236 designed runs"),
        stx(13, "The edges of the characterized regions have not been run at commercial scale.",
            "What remains for Stage 2",
            "The edges of the characterized regions have not been run at commercial scale"),
        stx(14, "The capability figures are model based predictions from simulated batches, and "
                "the qualification batches will be the first commercial measurement of the drug "
                "substance distribution.",
            "What remains for Stage 2",
            "The capability figures in §5 are model based predictions from simulated batches, and "
            "the qualification batches will be the first commercial measurement of the drug "
            "substance distribution"),
        stx(15, "The scale-down models have been qualified but not confirmed against commercial "
                "material for this process.",
            "What remains for Stage 2",
            "The scale-down models have been qualified but not confirmed against commercial "
            "material for this process"),
        stx(16, "The viral clearance figures are from spiked scale-down runs.",
            "The bound on the claims in this report",
            "The viral clearance figures are from spiked scale-down runs"),
        stx(17, "Where the report states a margin, that margin is the distance between a "
                "prediction and a limit, and Stage 2 is what turns the prediction into a "
                "measurement.",
            "The bound on the claims in this report",
            "that margin is the distance between a prediction and a limit, and Stage 2 is what "
            "turns the prediction into a measurement"),
    ])]
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_process",
                                  process_steps=pcmr_steps(doc, f)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=pcmr_cqas(doc, f)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_class",
                                  parameters=pcmr_params(doc, f, q_rows)),
    ]
    inv = S.DocumentInventoryItem(
        document_id=doc, file_name=f, predicted_document_type="process_characterization_master_report",
        product_name_candidates=["A-Mab"], process_name_candidates=["A-Mab drug substance"],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "master report", "process capability",
                     "viral clearance", "parameter classification", "control strategy",
                     "deviations"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc][0]}'.",
        source_references=[ref(doc, f, "Title block", "Title block", title_block_quote(doc))],
        metadata=meta())
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT + [
            "RhetoricalSpan (new model) — argument-structure roles over the report prose, and "
            "one span per row of the campaign deviation register (no upstream deviation model)",
        ],
        out_of_schema_notes=[
            "Master report rolls up the per-unit-operation reports; entities are the Step 3-10 "
            "process steps, the 10 consolidated drug-substance CQA outcomes, and the 21 "
            "quality-linked parameters that @tbl-cpp restates by name in this document.",
            "Per-record quotes are the RENDERED TABLE ROW (@tbl-train, @tbl-cqa, @tbl-cap, "
            "@tbl-cpp, @tbl-viral, @tbl-dev), rebuilt from the same seeded register, so each "
            "span carries both ends of the relation it anchors rather than a sentence about it.",
            "Process capability has no dedicated field: each attribute's Cpk is carried on the "
            "QualityAttribute reference to its @tbl-cap row. The report claims NO numeric "
            "minimum capability index — the one-sided-index convention is cited as practice "
            "only — so no minimum is asserted here.",
            "Viral clearance is modular: step_has_quality_attribute is asserted for every step "
            "@tbl-viral credits. The low-pH hold is deliberately NOT credited for MVM (0.00 "
            "log10, non-enveloped parvovirus), and no clearance is claimed for Protein A "
            "capture or cation exchange.",
            "HCP meets its limit only after anion exchange; the Protein A and cation-exchange "
            "pool values are in-process results, so no drug-substance acceptance criterion is "
            "asserted against them.",
            "The 17-row campaign deviation register (§8.1) has no upstream model and is captured "
            "as rhetorical_spans of role 'deviation_disposition', one per register row (15 "
            "retained, 1 invalidated_and_re_executed, 1 corrected_by_modelling_and_verification_"
            "runs), with the §8.2-8.4 narrative as further spans. PCMR-001 carries no weak_claims.",
        ],
        inventory=inv, entities=entities, report_sections=report_sections,
        assertions=AssertionStore(run_id=f"gt-{doc}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id="gt-pcmr", concepts=pcmr_concepts(q_rows)),
        rhetorical_spans=build_rhetorical_spans(doc, f) + pcmr_dev_spans(doc, f))


# =========================================================================== #
# Version 2.0 — the re-authored documents: PCP-005, PCMP-001, INV-001.          #
# --------------------------------------------------------------------------- #
# Fitted to the Version 2.0 text, never the reverse. Each builder reads the     #
# document's own tables back through ``qmd_namespace``, which runs the code      #
# chunks of the .qmd itself, so a row quote is rebuilt from the very expression  #
# that rendered the row. A value in a record is read from the same CSVs and      #
# helpers the document used; nothing is typed.                                   #
# =========================================================================== #
import contextlib as _contextlib
import io as _io

_QMD_NS: dict = {}
#: ``qmd name -> {tbl- label -> (CTable, DataFrame or None)}``, filled by :func:`qmd_namespace`;
#: read it through :func:`qmd_ctables`.
_QMD_CT: dict = {}


def qmd_namespace(qmd_name):
    """Run a document's own code chunks; return ``(namespace, tables)``.

    Several Version 2.0 documents build their tables inline, in a chunk of the ``.qmd`` rather
    than through a ``_pcpkg`` helper (INV-001 builds all eight of its flat tables that way).
    Re-typing that code here would be a second copy of the document's logic that could drift
    from the first. Running the chunks instead reproduces each table from the expression that
    rendered it, which is what ``row_quotes`` needs to stay verbatim on a reseed.

    ``show`` and the document's own ``md`` are replaced after the setup chunk by recorders, so
    ``tables`` maps each ``tbl-`` label to ``(kind, DataFrame, floatfmt, caption)``. ``kind`` is
    ``"show"`` (``df.to_markdown``, read back with :func:`row_quotes`) or ``"md"`` (cells printed
    as ``str``, read back with :func:`_join_cells`). Chunks that draw a figure are skipped.
    The namespace is cached: INV-001's setup re-fits every response surface and takes a while.

    A complex table (``T.frame(...).show()``, ``T.<builder>(...).show()``) is not a ``show``
    call and does not appear in ``tables``. Every one the chunks print is recorded on the side,
    with the DataFrame ``T.frame`` was given, and :func:`qmd_ctables` returns them.
    """
    if qmd_name in _QMD_NS:
        return _QMD_NS[qmd_name]
    import ctable as _ctable
    import tables as _tables
    src = open(os.path.join(HERE, qmd_name), encoding="utf-8").read()
    chunks = re.findall(r"```\{python\}\n(.*?)```", src, flags=re.S)
    ns, tables, cur = {"__name__": f"qmd:{qmd_name}"}, {}, {}
    shown, frames = {}, {}
    _ct_show0, _frame0 = _ctable.CTable.show, _tables.frame

    def _show(df, floatfmt=None):
        cur["t"] = ("show", df.copy(), floatfmt)

    def _md(df, widths=None):
        cur["t"] = ("md", df.copy(), None)

    def _ct_show(self):
        shown[self.label] = self
        return _ct_show0(self)

    def _frame(df, caption, label, *a, **kw):
        frames[label] = df.reset_index(drop=True).copy()
        return _frame0(df, caption, label, *a, **kw)

    cwd = os.getcwd()
    os.chdir(HERE)
    _ctable.CTable.show, _tables.frame = _ct_show, _frame
    try:
        with _contextlib.redirect_stdout(_io.StringIO()):
            for i, code in enumerate(chunks):
                if i and "plt." in code:
                    continue
                cur.clear()
                exec(compile(code, f"{qmd_name}#chunk{i}", "exec"), ns)   # noqa: S102
                if i == 0:
                    ns["show"], ns["md"] = _show, _md
                lab = (re.search(r"#\|\s*label:\s*(tbl-[\w-]+)", code)
                       or re.search(r"\{#(tbl-[\w-]+)\}", code))
                if lab and "t" in cur:
                    cap = (re.search(r'#\|\s*tbl-cap:\s*"(.*)"', code)
                           or re.search(r'print\(f?": (.*?) \{\{?#tbl-', code))
                    tables[lab.group(1)] = cur["t"] + (cap.group(1) if cap else None,)
    finally:
        _ctable.CTable.show, _tables.frame = _ct_show0, _frame0
        os.chdir(cwd)
    _QMD_NS[qmd_name] = (ns, tables)
    _QMD_CT[qmd_name] = {lab: (t, frames.get(lab)) for lab, t in shown.items()}
    return ns, tables


def qmd_ctables(qmd_name):
    """``{tbl- label -> (CTable, DataFrame or None)}``: every complex table the document prints.

    The CTable is the object the chunk printed, so ``ctable_rows`` on it gives the rendered rows
    from the very call that rendered them. The DataFrame is the one ``T.frame`` was given (row
    ``i`` of it is body row ``i`` of the table), so a record can be keyed by a column of it;
    it is ``None`` for a table built by another ``T.`` builder, which the builder can call again.
    """
    qmd_namespace(qmd_name)
    return _QMD_CT[qmd_name]


def captured_rows(cap, keys=None):
    """``{key -> rendered row}`` (+ ``.header``) for a table captured by :func:`qmd_namespace`."""
    kind, df, ff = cap[0], cap[1], cap[2]
    keys = list(range(len(df))) if keys is None else list(keys)
    if kind == "show":
        return row_quotes(df, keys, ff)
    out = RowQuotes(zip(keys, [_join_cells(r) for r in df.astype(str).values.tolist()]))
    out.header = _join_cells(str(c) for c in df.columns)
    return out


def md_string_rows(md):
    """``{first cell -> rendered row}`` for a table a helper returns as a markdown string
    (``related_docs_md``, ``corpus_docs_md``, ``all_sop_table``), read as the DOCX reads it."""
    lines = [ln for ln in md.splitlines() if ln.strip()]

    def cells(ln):
        return [c.strip() for c in ln.strip().strip("|").split("|")]
    out = RowQuotes((cells(ln)[0], _join_cells(cells(ln))) for ln in lines[2:])
    out.header = _join_cells(cells(lines[0]))
    return out


def rev2_layer(doc, f):
    """version, effective date, supersedes and revision history of a Version 2.0 document."""
    ver, eff = P.doc_version(doc)
    sup, hist = revision_layer(doc, f)
    return dict(version=ver, effective_date=eff, supersedes=sup, revision_history=hist)


def rev2_inventory(doc, f, dtype, process, topics):
    ver, eff = P.doc_version(doc)
    return S.DocumentInventoryItem(
        document_id=doc, file_name=f, predicted_document_type=dtype,
        product_name_candidates=["A-Mab"], process_name_candidates=[process],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[eff],
        main_topics=topics,
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc][0]}'.",
        source_references=[ref(doc, f, "Title block", "Title block", title_block_quote(doc))],
        metadata=meta())


def _adders(doc, f):
    """(assertions, add, statements, st) — the two record factories every builder uses."""
    from annex_contract.assertions import EvidenceBackedAssertion
    from annex_contract.summaries import ReportStatement
    A, ST = [], []

    def add(subj, pred, obj, text, sec, quote, header=None, table_title=None, table_id=None):
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc}-A{len(A) + 1:03d}", subject_id=subj, predicate=pred,
            object_id=obj, assertion_text=text,
            source_references=[ref(doc, f, f"{doc}_sec", sec, quote, table_title=table_title,
                                   table_id=table_id, table_header=header)],
            metadata=meta()))

    def st(text, sec, quote, header=None, table_title=None):
        ST.append(ReportStatement(
            statement_id=f"{doc}-S{len(ST) + 1:02d}", statement_text=text, confidence="high",
            review_status="accepted",
            source_references=[ref(doc, f, f"{doc}_sec", sec, quote, table_title=table_title,
                                   table_header=header)]))
    return A, add, ST, st


def _site_entities(doc, f, sec):
    return [
        S.ManufacturingSite(site_id="site:cambridge", site_name=P.SENDING_SITE, site_role="sending",
                            location="Cambridge, MA",
                            source_references=[ref(doc, f, sec, "Title block", P.SENDING_SITE)],
                            metadata=meta()),
        S.ManufacturingSite(site_id="site:grafton", site_name=P.RECEIVING_SITE,
                            site_role="receiving", location="Grafton, WI",
                            source_references=[ref(doc, f, sec, "Title block", P.RECEIVING_SITE)],
                            metadata=meta()),
    ]


#: Validation reference -> method type. The kind of assay, not a value: nothing here is in a CSV.
METHOD_TYPE = {
    "AMV-3010": "chromatography", "AMV-3011": "chromatography", "AMV-3012": "immunoassay",
    "AMV-3013": "electrophoresis", "AMV-3014": "qPCR", "AMV-3015": "nephelometry",
    "AMV-3016": "immunoassay", "AMV-3017": "infectivity assay", "AMV-3018": "infectivity assay",
    "AMV-3019": "UV spectrophotometry", "AMV-3020": "capillary electrophoresis",
}
#: Validation reference -> the attributes it measures in this corpus (method-to-analyte links).
METHOD_ATTRS = {
    "AMV-3010": ["afucosylation", "galactosylation", "high_mannose"],
    "AMV-3011": ["aggregates_hmw"], "AMV-3012": ["hcp"], "AMV-3013": ["acidic_variants"],
    "AMV-3014": ["residual_dna"], "AMV-3016": ["leached_protein_a"], "AMV-3017": ["lrv_xmulv"],
    "AMV-3018": ["lrv_mvm"], "AMV-3020": ["fragments_lmw"],
}
#: Validation reference -> the token ``T.methods_by_study`` prints for that method.
SIZE_VARIANT_TOKEN = {"AMV-3011": "SEC", "AMV-3020": "nrCE-SDS"}
#: Chronology "kind" -> StudyDesign.study_type. Hold, comparability, retest and an invalidated
#: first execution have no study type in the schema and are left out (see out_of_schema_notes).
STUDY_TYPE = {"qualification": "scale_down_qualification", "screening": "screening_doe",
              "rsm": "response_surface_doe", "univariate": "univariate"}
REV2_EXT = [
    "RevisionEntry / GroundTruthAnnex.supersedes (new) — the revision layer, anchored on the "
    "rendered revision-history rows",
    "AcceptanceCriterionRecord (new) — step acceptance criteria tagged with the revision that "
    "applied them and whether they are in force or superseded",
]


def _attr_key_by_label():
    """Rendered attribute label (``tables.ATTR_NAME`` / CQA register name) -> attribute key."""
    import tables as T
    out = {v: k for k, v in T.ATTR_NAME.items()}
    out.update({r["cqa"]: r["key"] for r in P.cqa_reg.to_dict("records")})
    return out


def _attr_concepts(keys):
    from annex_contract.concepts import Concept
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))
    return [Concept(concept_id=f"attr:{k}", concept_type="QUALITY_ATTRIBUTE",
                    canonical_name=names.get(k, k), aliases=[k], review_status="human_verified")
            for k in keys]


def _method_concepts(amvs, names):
    from annex_contract.concepts import Concept
    return [Concept(concept_id=f"method:{a}", concept_type="ANALYTICAL_METHOD",
                    canonical_name=names[a], aliases=[a], review_status="human_verified")
            for a in amvs]


def size_variant_refs(doc, f, sec, steps, token, text, lead=2):
    """References to the rows of ``T.methods_by_study(steps)`` that name ``token`` ("SEC" or
    "nrCE-SDS") as a method used in a study. A row that occurs more than once in the document
    (two continuation rows can read alike) is ambiguous and is not used.

    ``lead`` is the number of label cells before the method cells: the step and the attribute.
    A table of one step has no step column (``tables._drop_step_column``), so pass ``lead=1``
    for it, or its first method cell is read as a label."""
    import tables as T
    from check_grounding import normalize
    t = T.methods_by_study(steps)
    rows = ctable_rows(t)
    out = []
    for row in rows.values():
        methods = row.split(CELL_SEP)[lead:]
        if not any(token in re.split(r"[ ,]+", m) for m in methods):
            continue
        if text.count(normalize(row)) != 1:
            continue
        out.append(ref(doc, f, f"{doc}_sec", sec, row, table_title=t.caption, table_id=t.label,
                       table_header=rows.header))
    return out


def _unrendered_note(ids):
    """An out-of-schema note for chronology rows the data carries and the rendered text does not.

    The annex is fitted to the document. A study added to the configuration after the document
    was rendered has no row in it, so it gets no record, and the annex says so rather than
    dropping it silently."""
    if not ids:
        return []
    return [f"Studies in outputs/data/study_chronology.csv with no row in the rendered document "
            f"(added to the data after it was rendered): {', '.join(ids)}. They have no record "
            f"here; the document must be re-rendered before they can be annexed."]


# --------------------------------------------------------------------------- #
# PCP-005 — Process Characterization Plan, Protein A (Step 5), Version 2.0.     #
# --------------------------------------------------------------------------- #
#: Attribute cells of PCP-005 @tbl-methods -> attribute key. Step yield is a performance
#: attribute with no CQA of its own; it is the concept attr:step_yield.
PA2_METHOD_ATTR = {
    "Pool host cell protein (ng/mg)": "hcp", "Leached Protein A (ppm)": "leached_protein_a",
    "Step yield": "step_yield", "Fragments, LMW (%)": "fragments_lmw",
    "Aggregates, HMW (%)": "aggregates_hmw", "Acidic variants (%)": "acidic_variants",
    "Residual DNA": "residual_dna",
}


def build_plan_protein_a():
    """PCP-005 Version 2.0: the protocol amendment issued under INV-001.

    Fitted to the Version 2.0 text. Most of its tables are complex tables (``T.frame``), read
    back through :func:`qmd_ctables` from the object the plan printed. The parameter table shows
    the NOR the studies were planned and judged against (``nor_char_*``), not the narrower NOR
    that PCR-005 Version 2.0 put in force, so the parameter records carry that NOR.
    """
    import doe_report as D
    import tables as T
    from annex_contract.assertions import AssertionStore
    from annex_contract.concepts import Concept, ConceptStore
    from annex_contract.discourse import DocumentRelationship, ExplicitNonClaim
    from annex_contract.summaries import ReportSection
    doc, f = "PCP-005", PCP5_FILE
    qmd = "PCP-005_protein_a.qmd"
    ns, tabs = qmd_namespace(qmd)
    ct = qmd_ctables(qmd)
    A, add, ST, st = _adders(doc, f)
    text = _document_text(f)

    def sid(s):
        return f"{doc}_sec_{s}"

    # ---- the rendered tables, rebuilt from the objects the plan printed ---------------------
    pt, pdf_ = ct["tbl-params"]                                     # T.frame, by parameter
    prow = ctable_rows(pt, pdf_["Parameter"])
    cdf = tabs["tbl-cqas"][1]                                       # show(), "DS criterion" column
    by_label = _attr_key_by_label()
    ckeys = [by_label[n] for n in cdf["CQA"]]
    crow = captured_rows(tabs["tbl-cqas"], ckeys)
    mt, mdf = ct["tbl-methods"]                                     # T.frame, by row index
    mrow = ctable_rows(mt)
    amv_of = {}                                                     # method title -> AMV id
    for amv, title in ns["AMV_ALL"]:
        if amv_of.setdefault(title, amv) != amv:
            raise ValueError(f"two validations are titled {title!r}")
    mdf = mdf.assign(AMV=[amv_of[m] for m in mdf["Method"]])
    sop_t, sop_df = ct["tbl-sop"]                                   # T.sop_references, by reference
    soprow = ctable_rows(sop_t, sop_df["Reference"])
    ot, odf = ct["tbl-outcrit"]                                     # T.frame, by response
    resp_by_label = {D.RESP_LABEL[r]: r for r in list(D.responses(PAUO))
                     + D.fragment_responses(PAUO)}
    orow = ctable_rows(ot, [resp_by_label[o] for o in odf["Attribute"]])
    chdf = tabs["tbl-chrono"][1]
    chrow = captured_rows(tabs["tbl-chrono"], chdf["Study"])      # @tbl-chrono, by study id
    rel = md_string_rows(P.related_docs_md(doc))                  # @tbl-related
    iac_t = ct["tbl-iac"][0]                                        # T.iac_derivation([UO])
    iac = ns["IAC"]                                                 # D.iac_table(UO), by response
    iacrow = ctable_rows(iac_t, [by_label[c.split(CELL_SEP)[0]] for c in iac_t.rows()])
    cap = {k: v[3] for k, v in tabs.items()}
    cap["tbl-related"] = "Documents related to this plan."         # printed by related_docs_md
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))

    # ---- entities ------------------------------------------------------------------------
    step = S.ProcessStep(
        step_id="step:protein_a", step_name=PAUO_NAME, step_number=str(PASTEP),
        unit_operation=PAUO_NAME,
        description="The capture step of the purification train, operated in bind and elute "
                    "mode. The resin binds the antibody from the clarified harvest, most host "
                    "cell protein and DNA leave in the flow-through and the wash, and the "
                    "antibody is eluted at low pH and passed to low-pH viral inactivation "
                    "(Step 6) without neutralization. The step adds leached Protein A ligand.",
        input_materials=["clarified harvest"],
        output_materials=["Protein A eluate at elution pH (low-pH viral inactivation load)"],
        equipment=["laboratory scale-down column packed with the commercial Protein A resin"],
        source_references=[
            ref(doc, f, sid("purpose"), "Purpose and scope",
                "Protein A chromatography is the capture step of the A-Mab purification train."),
            ref(doc, f, sid("purpose"), "Purpose and scope",
                "The antibody is then eluted at low pH and passed to low-pH viral inactivation "
                "(Step 6) without neutralization.")],
        metadata=meta())
    equipment = [S.Equipment(
        equipment_id="equip:pa_sdm_column",
        equipment_name="laboratory column packed with the commercial Protein A resin",
        equipment_type="chromatography column (scale-down model)", site_name=P.SENDING_SITE,
        source_references=[ref(doc, f, sid("sdm"), "Scale-down model and its qualification",
                               "The scale-down model is a laboratory column packed with the "
                               "commercial Protein A resin.")],
        metadata=meta())]
    preg = P.param_reg[P.param_reg.unit_operation == PAUO_NAME].set_index("parameter")
    params = []
    for name, row in prow.items():
        r = preg.loc[name]
        params.append(S.ProcessParameter(
            parameter_id=PAPARAM_CONCEPT[name], parameter_name=name,
            parameter_type="unclassified", unit=r["unit"], target_value=f"{r['setpoint']:g}",
            NOR=f"{r['nor_char_low']:g}–{r['nor_char_high']:g} {r['unit']}",
            PAR=f"{r['par_low']:g}–{r['par_high']:g} {r['unit']}",
            associated_step=PASTEP_LABEL,
            source_references=[ref(doc, f, sid("factors"), "Factors, ranges and study type", row,
                                   table_title=pt.caption, table_id=f"{doc}_tab_params",
                                   table_header=prow.header)],
            metadata=meta()))
    method_of = {}
    for _, r in mdf.iterrows():
        method_of.setdefault(PA2_METHOD_ATTR[r["Attribute"]], r["AMV"])
    attrs = []
    for i, key in enumerate(ckeys):
        r = _pa_cqa_row(key)
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"], acceptance_criteria=[f"{cdf['DS criterion'].iloc[i]} (drug substance)"],
            analytical_method=method_of.get(key), associated_steps=[PASTEP_LABEL],
            rationale_for_criticality=f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = "
                                      f"{r['tool1_score']}.",
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref(doc, f, sid("cqas"), "Quality attributes in scope", crow[key],
                                   table_title=cap["tbl-cqas"], table_id=f"{doc}_tab_cqas",
                                   table_header=crow.header)],
            metadata=meta()))
    by_amv = {}
    for i, r in mdf.iterrows():
        by_amv.setdefault(r["AMV"], []).append(i)
    methods = []
    for amv, idx in by_amv.items():
        keys = [PA2_METHOD_ATTR[mdf.loc[i, "Attribute"]] for i in idx]
        methods.append(S.AnalyticalMethod(
            method_id=amv, method_name=mdf.loc[idx[0], "Method"], method_type=METHOD_TYPE.get(amv),
            analytes=[mdf.loc[i, "Attribute"] for i in idx],
            associated_attributes=[f"attr:{k}" for k in keys], validation_status="validated",
            source_references=[ref(doc, f, sid("analytics"), "Analytical methods", mrow[i],
                                   table_title=mt.caption, table_id=f"{doc}_tab_methods",
                                   table_header=mrow.header) for i in idx]
            # the methods table names the method by its title; the procedures table ties the
            # title to the validation reference
            + [ref(doc, f, sid("related"), "Related documents", soprow[amv],
                   table_title=sop_t.caption, table_id=f"{doc}_tab_sop", table_header=soprow.header)]
            + (size_variant_refs(doc, f, "Analytical methods", [PAUO], SIZE_VARIANT_TOKEN[amv],
                                 text, lead=1) if amv in SIZE_VARIANT_TOKEN else []),
            metadata=meta()))
    nc = [
        ExplicitNonClaim(
            non_claim_id=f"{doc}-NC01", subject="viral clearance", unit_operation=PAUO_NAME,
            statement="No viral clearance claim is made for the Protein A step, although it "
                      "removes some virus, and no spiking study is planned.",
            handled_elsewhere="low-pH inactivation, anion exchange and virus filtration "
                              "(PCMP-001, viral clearance claims)",
            source_references=[ref(doc, f, sid("purpose"), "Purpose and scope",
                                   "Although Protein A chromatography removes some virus, no "
                                   "viral clearance claim is made for this step")],
            metadata=meta()),
        ExplicitNonClaim(
            non_claim_id=f"{doc}-NC02", subject="short bed at high protein load",
            unit_operation=PAUO_NAME,
            statement="A short bed combined with a high protein load is not studied, and no claim "
                      "is made for it.",
            rationale="Bed height is fixed for each packed column and is studied one factor at a "
                      "time at the set-point load, so the short bed is not run at high protein load.",
            source_references=[ref(doc, f, sid("risk"), "Risk-based prioritization of parameters",
                                   "A short bed combined with a high protein load, where "
                                   "breakthrough is most likely, is therefore not studied, and no "
                                   "claim is made for it.")],
            metadata=meta()),
        ExplicitNonClaim(
            non_claim_id=f"{doc}-NC03", subject="resin life cycle", unit_operation=PAUO_NAME,
            statement="The re-use limit, cleaning and sanitization of the resin are outside the "
                      "scope of the plan.",
            handled_elsewhere="SOP-2008",
            source_references=[ref(doc, f, sid("purpose"), "Purpose and scope",
                                   "is governed by the resin life-cycle procedure SOP-2008 and is "
                                   "outside the scope of this plan")],
            metadata=meta()),
        ExplicitNonClaim(
            non_claim_id=f"{doc}-NC04", subject="effect of feed quality", unit_operation=PAUO_NAME,
            statement="The effect of feed quality on the step is not estimated, because each "
                      "design is loaded from one feed.",
            handled_elsewhere="PCP-003 and PCP-004",
            source_references=[ref(doc, f, sid("operation"), "Operation",
                                   "The effect of feed quality on the step is therefore not "
                                   "estimated in this plan.")],
            metadata=meta()),
    ]
    kind_of = {"Rolls up into": "rolls_up_into", "Parent — master plan": "executed_under",
               "Parent — risk basis for study scope": "scoped_by",
               "Parent — transfer scope": "scoped_by"}
    rels = []
    for target, row in rel.items():
        txt = row.split(CELL_SEP)[-1]
        rels.append(DocumentRelationship(
            relationship_id=f"{doc}-R{len(rels) + 1:02d}", kind=kind_of.get(txt, "references"),
            source_document_id=doc, target_document_ref=target, statement=txt,
            source_references=[ref(doc, f, sid("related"), "Related documents", row,
                                   table_title=cap["tbl-related"], table_header=rel.header)],
            metadata=meta()))
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=sid("purpose"),
                                  process_steps=[step], sites=_site_entities(doc, f, sid("purpose")),
                                  non_claims=[nc[0], nc[2]]),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("related"),
                                  document_relationships=rels),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("cqas"), quality_attributes=attrs),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("risk"), non_claims=[nc[1]]),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("sdm"), equipment=equipment),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("operation"), non_claims=[nc[3]]),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("analytics"),
                                  analytical_methods=methods),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("factors"), parameters=params),
    ]

    # ---- studies: each on its own row of the execution-window table, plus its design -----
    fac = [P.CFG.unit_op(PAUO).param(k).name for k in D.screening_factors(PAUO)]
    uni = [p.name for p in P.CFG.unit_op(PAUO).parameters if p.study != "multivariate"]
    resp_scr = list(D.responses(PAUO))
    resp_rsm = resp_scr + [r for r in D.fragment_responses(PAUO, "rsm") if r == "lmw_cesds_pct"]
    # Keyed by the KIND of study, not by its id, so any study the chronology carries is handled.
    # The prose spans name the study by its id; one that the rendered text does not contain is a
    # quote this builder expected and the document does not have, so it fails loudly below.
    def prose(kind, sid_):
        return {
            "qualification": [("Scale-down model and its qualification",
                               f"The model is qualified under the scale-down model qualification "
                               f"procedure SOP-1001 in study {sid_}, the scale-down model "
                               f"qualification, before the first run of the screening design.")],
            "screening": [("Screening design", f"The screening design (study {sid_}) is a full "
                                               f"two-level factorial design"),
                          ("Screening design", f"with {ns['fact_scr']} factorial runs and "
                                               f"{ns['cp_scr']} centre points, {ns['n_scr']} runs "
                                               f"in all")],
            "rsm": [("Response-surface design", f"The response-surface design (study {sid_}) is a "
                                                f"face-centred central composite design"),
                    ("Response-surface design", f"It has {ns['fact_rsm']} factorial runs, "
                                                f"{ns['n_axial']} axial runs at the faces of the "
                                                f"cube (coded −1 and +1) and {ns['cp_rsm']} centre "
                                                f"points, {ns['n_rsm']} runs in all.")],
            "univariate": [("Univariate assessment", f"Operating temperature and bed height are "
                                                     f"studied one factor at a time (study {sid_})")],
        }.get(kind, [])
    design = {"screening": dict(design_name="full two-level factorial", factors=fac,
                                responses=resp_scr, n_runs=P.doe_runs(PAUO, "screening"),
                                n_center_points=P.doe_centre_points(PAUO, "screening")),
              "rsm": dict(design_name="face-centred central composite design", factors=fac,
                          responses=resp_rsm, n_runs=P.doe_runs(PAUO, "rsm"),
                          n_center_points=P.doe_centre_points(PAUO, "rsm")),
              "univariate": dict(design_name="one factor at a time, duplicate runs at each end of "
                                             "the range studied", factors=uni, responses=resp_scr),
              "qualification": dict(responses=resp_scr)}
    studies, unrendered = [], []
    for _, r in ns["CH"].iterrows():
        stype = STUDY_TYPE.get(r["kind"])
        if stype is None:
            continue
        if not _present(chrow[r["id"]], text):
            unrendered.append(r["id"])
            continue
        d = design[r["kind"]]
        refs = [ref(doc, f, sid("chrono"), "Deliverables and schedule", chrow[r["id"]],
                    table_title=cap["tbl-chrono"], table_id=f"{doc}_tab_chrono",
                    table_header=chrow.header)]
        refs += [ref(doc, f, sid("design"), sec, q) for sec, q in prose(r["kind"], r["id"])]
        studies.append(S.StudyDesign(
            study_id=f"study:{r['id']}", study_type=stype, unit_operation=PAUO_NAME,
            scale_down_model="laboratory column packed with the commercial Protein A resin",
            associated_parameters=[PAPARAM_CONCEPT[x] for x in d.get("factors", [])],
            source_references=refs,
            metadata=meta(), **d))

    # ---- assertions ------------------------------------------------------------------------
    for name, row in prow.items():
        add("step:protein_a", "step_has_parameter", PAPARAM_CONCEPT[name],
            f"{PAUO_NAME} has process parameter {name}.", "Factors, ranges and study type", row,
            prow.header, pt.caption)
    role = {"leached_protein_a": "introduces {n}, the only CQA the step introduces",
            "hcp": "is the principal point of clearance for {n}",
            "residual_dna": "is the principal point of clearance for {n}",
            "fragments_lmw": "partly clears {n}",
            "aggregates_hmw": "does not separate {n} from monomer; aggregate is measured on every "
                              "pool by SEC for information and is not a response of the designs"}
    for key in ckeys:
        add("step:protein_a", "step_has_quality_attribute", f"attr:{key}",
            f"{PAUO_NAME} " + role[key].format(n=names[key]) + ".", "Quality attributes in scope",
            crow[key], crow.header, cap["tbl-cqas"])
    for i, r in mdf.iterrows():
        key = PA2_METHOD_ATTR[r["Attribute"]]
        add(f"attr:{key}", "attribute_measured_by_method", f"method:{r['AMV']}",
            f"{r['Attribute']} is measured by {r['AMV']} ({r['Method']}) on: {r['Samples']}. "
            f"Purpose: {r['Purpose']}.", "Analytical methods", mrow[i], mrow.header, mt.caption)
    for resp, row in orow.items():
        if resp == "step_yield":
            continue
        o = odf[odf["Attribute"] == D.RESP_LABEL[resp]].iloc[0]
        key = D.RESP_TO_CQA.get(resp, resp)
        basis = "carried back" + (", widened" if bool(iac.loc[resp, "widened"]) else "")
        offset = ("after the scale-down offset is subtracted" if resp in ns["SDM_JUDGED"]
                  else "with no scale-down offset, because the qualification has no result for it")
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{PAUO}_{key}_iac",
            f"At the Protein A step, {o['Attribute']} is judged against the Version 2.0 "
            f"intermediate acceptance criterion {o['Criterion']} ({basis}), on the upper end of the "
            f"95 % prediction interval of a single batch, {offset}.",
            "Acceptance and decision criteria", row, orow.header, ot.caption)
    hold = "Hold study of the Protein A eluate"
    agg_bx, acid_bx = ns["agg_bx"], ns["acid_bx"]
    hold_q = (f"The criteria in force for that output, from the table of intermediate acceptance "
              f"criteria in PCMP-001, are ≤ {agg_bx[1]:.2f} % HMW for aggregate and "
              f"{acid_bx[0]:g}–{acid_bx[1]:g} % for acidic variants.")
    add("attr:aggregates_hmw", "attribute_has_acceptance_criterion", "lit:pa_hold_aggregates",
        f"The held Protein A eluate carries the criterion in force for the production bioreactor "
        f"output for aggregate, ≤ {agg_bx[1]:.2f} % HMW.", hold, hold_q)
    add("attr:acidic_variants", "attribute_has_acceptance_criterion", "lit:pa_hold_acidic",
        f"The held Protein A eluate carries the criterion in force for the production bioreactor "
        f"output for acidic variants, {acid_bx[0]:g}–{acid_bx[1]:g} %.", hold, hold_q)
    add("attr:fragments_lmw", "attribute_has_acceptance_criterion", "lit:pa_hold_fragments",
        f"The held Protein A eluate is judged for fragments against the Protein A pool criterion, "
        f"≤ {ns['frag_iac']:.2f} % by nrCE-SDS.", hold,
        f"For fragments the criterion is that of the Protein A pool, ≤ {ns['frag_iac']:.2f} % by "
        f"nrCE-SDS.")
    prior = "Unit-operation description and prior knowledge"
    q_hcp = ("Pool host cell protein is expected to rise with protein load and as elution buffer "
             "pH falls, and the two may interact")
    add(PAPARAM_CONCEPT["Protein load"], "parameter_impacts_attribute", "attr:hcp",
        "Pool host cell protein is expected to rise with protein load.",
        "Risk-based prioritization of parameters", q_hcp)
    add(PAPARAM_CONCEPT["Elution buffer pH"], "parameter_impacts_attribute", "attr:hcp",
        "Pool host cell protein is expected to rise as elution buffer pH falls.",
        "Risk-based prioritization of parameters", q_hcp)
    add(PAPARAM_CONCEPT["Elution buffer pH"], "parameter_impacts_attribute", "attr:fragments_lmw",
        "A lower elution buffer pH may add acid-catalysed hinge hydrolysis, and so fragments, "
        "during elution.", prior,
        "A lower elution pH may add a little acid-catalysed hinge hydrolysis during elution.")
    add(PAPARAM_CONCEPT["Protein load"], "parameter_impacts_attribute", "attr:leached_protein_a",
        "Leached Protein A in ppm is expected to fall as protein load rises, if a similar amount "
        "of ligand leaches in each cycle.", prior,
        "If a similar amount of ligand leaches in each cycle, leached Protein A in ppm falls as "
        "protein load rises")
    add(PAPARAM_CONCEPT["Load flow rate"], "parameter_impacts_attribute", "attr:step_yield",
        "Step yield is expected to fall with load flow rate, mainly at high load.", prior,
        "Yield is therefore expected to fall with flow rate mainly at high load.")
    add(PAPARAM_CONCEPT["End of pool collect"], "parameter_impacts_attribute", "attr:step_yield",
        "Extending the end of pool collect is expected to raise step yield.", prior,
        "Extending the end of pool collect recovers the tail of the elution peak and raises yield.")

    # ---- report sections -------------------------------------------------------------------
    chg = "Changes in this revision"
    sdm = "Scale-down model and its qualification"
    st("PCP-005 is the protocol for the process characterization of the Protein A chromatography "
       "step (Step 5), and applies PCMP-001 to the step.", "Purpose and scope",
       "This plan is the protocol for the process characterization of the Protein A "
       "chromatography step (Step 5) of the A-Mab drug substance process.")
    st(f"Of the {ns['n_par']} process parameters, {ns['n_multi']} are studied in a screening "
       f"design followed by a response-surface design, and {ns['n_uni']} one factor at a time.",
       "Purpose and scope",
       f"Of these, {ns['n_multi']} are studied in a screening design followed by a "
       f"response-surface design, and {ns['n_uni']} are studied one factor at a time.")
    st("Version 2.0 is a protocol amendment issued under INV-001 after the studies of the step "
       "had been executed.", chg,
       f"This Version 2.0 is a protocol amendment issued after that execution, under the "
       f"investigation {P.INV['id']}.")
    st("Version 1.0 of the plan contained no approved criterion for the step.", chg,
       "For this step, Version 1.0 of this plan contained no approved plan criterion.")
    st(f"The Version 2.0 criterion for pool host cell protein, {ns['hcp_iac']:,.0f} ng/mg, is wider "
       f"than the Version 1.0 analysis limit of {ns['rev1_hcp']:,.0f} ng/mg that Version 1.0 of "
       f"PCR-005 applied.", chg,
       f"The Version 2.0 criterion for pool host cell protein, {ns['hcp_iac']:,.0f} ng/mg, is "
       f"wider than the Version 1.0 analysis limit of {ns['rev1_hcp']:,.0f} ng/mg.")
    st("The Version 1.0 analysis limit was never an approved criterion, so the wider Version 2.0 "
       "criterion does not loosen one.", chg,
       "The Version 1.0 limit was never an approved criterion, so the wider Version 2.0 criterion "
       "does not loosen one.")
    st("The intermediate acceptance criteria are derived without data from the Protein A studies, "
       "so they may be applied to studies already executed.", chg,
       "Because this derivation uses no data from the Protein A studies, it may be applied to "
       "studies that were already executed.")
    st("The amendment adds no run, removes none and repeats none; factors, ranges and designs "
       "are those of Version 1.0.", chg,
       "No run is added, removed or repeated by this amendment.")
    st("The drug substance criteria do not apply to the Protein A pool directly; each output "
       "with a downstream dependence is judged against an intermediate acceptance criterion.",
       "Quality attributes in scope",
       "The drug substance criteria do not apply to the Protein A pool directly.")
    st("SEC overstates fragments in the Protein A pool, so fragments are measured by nrCE-SDS and "
       "SEC fragment results are not used for any decision.", prior,
       "For this reason SEC overstates fragments in the Protein A pool, and nrCE-SDS does not "
       "(INV-001 finding 6).")
    st("For a quantity compared at both scales that has a criterion, each scale-down result is "
       "translated to manufacturing scale by subtracting the offset before it is judged.", sdm,
       "For a quantity that is compared at both scales and has a criterion, each scale-down result "
       "is translated to manufacturing scale by subtracting the offset before it is judged.")
    st("The model is qualified for such a quantity when its conclusion over the NOR is the same "
       "with the offset at either end of its confidence interval.", sdm,
       "The model is qualified for such a quantity when its conclusion over the NOR is the same "
       "with the offset at either end of the confidence interval.")
    st("Fragments are not measured in the scale-down qualification, so they carry no offset and "
       "are judged as the response-surface model predicts them.", sdm,
       "The qualification therefore has no fragment result at either scale, and fragments carry "
       "no offset.")
    st("Leached Protein A is expected to be lower in the laboratory column than at manufacturing "
       "scale, because the manufacturing load is held longer before capture.",
       "Risks and assumptions",
       "Leached Protein A is expected to be lower in the laboratory column than at manufacturing "
       "scale, because the manufacturing load is held longer before capture")
    st("The difference between the scales for leached Protein A is its offset, and it is "
       "subtracted as every offset is.", sdm,
       "This difference is the offset of leached Protein A, and it is subtracted as every offset "
       "is.")
    st("The response-surface model is the predictive model of the step, and every prediction "
       "and every PAR in PCR-005 comes from it.", "Statistical methods",
       "The response-surface model is the predictive model of the step, and every prediction and "
       "every PAR in PCR-005 comes from it.")
    st("The NOR-propagated PAR, judged on the 95 % prediction interval of a single batch, is the "
       "one that supports a claim.", "The two analyses",
       "The NOR-propagated PAR is the one that supports a claim.")
    st("A PAR is never claimed beyond the range studied.", "Factors, ranges and study type",
       "A PAR is never claimed beyond the range studied (PCMP-001, proven acceptable ranges).")
    narrowed, notes = list(ns["NARROWED"]), pt.notes_text().split(CELL_SEP)
    if len(narrowed) != len(notes):
        raise ValueError(f"{pt.label}: {len(notes)} notes for {len(narrowed)} narrowed NORs")
    for p, note in zip(narrowed, notes):
        nor_now = P.CFG.unit_op(PAUO).param(p.key).nor
        st(f"The {p.name.lower()} NOR in this plan, {p.nor[0]:g}–{p.nor[1]:g} {p.unit}, is the NOR "
           f"against which the studies were planned and judged; PCR-005 Version 2.0 narrowed it to "
           f"{nor_now[0]:g}–{nor_now[1]:g} {p.unit}.", "Factors, ranges and study type", note,
           table_title=pt.caption)
    for key, row in iacrow.items():
        r = iac[iac["cqa"] == key].iloc[0]
        moved = (" It is in force at a widened value: the A-Mab confidence bound of a downstream "
                 "step replaced a platform worst case." if bool(r["widened"]) else "")
        st(f"The intermediate acceptance criterion for {names[key]} at the Protein A step "
           f"is the drug substance criterion carried back through a downstream clearance fold of "
           f"{T.num(r['downstream_fold'])} and an increase of {T.num(r['downstream_added'])}, with "
           f"no margin: {T.crit(r['iac_low'], r['iac_high'], r['spec_type'])}.{moved}",
           "Intermediate acceptance criteria", row, iacrow.header, iac_t.caption)
    st(f"From the platform worst cases alone, the criterion for pool host cell protein was "
       f"{ns['hcp_apriori']:,.0f} ng/mg; the cation exchange bound widened it.",
       "Intermediate acceptance criteria",
       f"From the platform worst cases alone, the derivation gave {ns['hcp_apriori']:,.0f} ng/mg.")
    st(f"The criterion for leached Protein A stays at its a priori value of {ns['lpa_apriori']:g} "
       f"ppm, because leached Protein A is not a response of the cation exchange or anion exchange "
       f"designs and its platform values cannot be checked in this campaign.",
       "Intermediate acceptance criteria",
       f"The criterion for leached Protein A is at its a priori value of {ns['lpa_apriori']:g} ppm, "
       f"because leached Protein A is not a response of the cation exchange or anion exchange "
       f"designs, so its platform values cannot be checked in this campaign.")

    concepts = [Concept(concept_id="step:protein_a", concept_type="PROCESS_STEP",
                        canonical_name=PAUO_NAME,
                        aliases=["Protein A", "Protein A capture", "capture step", "Step 5"],
                        review_status="human_verified")]
    concepts += [Concept(concept_id=cid, concept_type="PROCESS_PARAMETER", canonical_name=name,
                         review_status="human_verified") for name, cid in PAPARAM_CONCEPT.items()]
    concepts += _attr_concepts(ckeys + ["acidic_variants"])
    concepts.append(Concept(concept_id="attr:step_yield", concept_type="PERFORMANCE_ATTRIBUTE",
                            canonical_name="Step yield", aliases=["yield"],
                            review_status="human_verified"))
    concepts += _method_concepts(list(by_amv), {a: mdf.loc[i[0], "Method"]
                                                for a, i in by_amv.items()})
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], **rev2_layer(doc, f),
        schema_extensions_used=COMMON_EXT + REV2_EXT,
        out_of_schema_notes=[
            "Classification is a result of the study, so every parameter_type is 'unclassified'. "
            "ProcessParameter.NOR is the NOR the studies were planned and judged against, which "
            "is the NOR the plan prints; the narrower protein load NOR that PCR-005 Version 2.0 "
            "put in force is a statement anchored on the footnote of the parameter table. "
            "ProcessParameter.PAR carries the range studied, as everywhere in the corpus; the plan "
            "claims no proven acceptable range.",
            "The hold study S-PA-HLD and the nrCE-SDS retest of retained samples S-PA-RET have no "
            "StudyDesign.study_type. They appear only as rows of the execution-window table.",
            "acceptance_criteria holds the rows of the criteria-change table (Version 1.0 analysis "
            "limit, superseded, and the Version 2.0 criteria, in force). The criteria the held "
            "eluate carries are the production bioreactor output criteria in force and the "
            "Protein A pool criterion for fragments, applied to a hold, so they are assertions "
            "and not AcceptanceCriterionRecords of this step.",
            "Step yield is a performance attribute with no acceptance criterion; it is the concept "
            "attr:step_yield in the prior-knowledge assertions.",
            "The methods table names each method by its title. Each AnalyticalMethod record is "
            "also anchored on the row of the procedures table that ties the title to its AMV.",
            "The planned design matrices (Appendices A and B), the factor letter codes and the "
            "table of downstream values the criteria rest on are not represented row by row. No "
            "rhetorical_spans: the Version 1.0 annex carried none for this plan, and none were "
            "curated for Version 2.0. weak_claims is empty.",
        ] + _unrendered_note(unrendered),
        inventory=rev2_inventory(doc, f, "process_characterization_plan", PAUO_NAME,
                                 ["process characterization", "Protein A chromatography",
                                  "protocol amendment", "intermediate acceptance criteria",
                                  "scale-down offset", "design of experiments", "hold study"]),
        entities=entities, studies=studies,
        report_sections=[ReportSection(section_id=f"{doc}-summary", title="Plan summary",
                                       statements=ST)],
        assertions=AssertionStore(run_id=f"gt-{doc}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{doc}", concepts=concepts),
        acceptance_criteria=acceptance_criteria_layer(doc, f, chg, T.criteria_change([PAUO]),
                                                      [PAUO]))


# --------------------------------------------------------------------------- #
# PCR-005 — Process Characterization Report, Protein A (Step 5), Version 2.0.   #
# --------------------------------------------------------------------------- #
def build_report_protein_a():
    """PCR-005 Version 2.0: the Protein A report re-analysed under INV-001.

    Fitted to the Version 2.0 text. The record types follow the Version 1.0 builder (parameters
    with their final class, the attributes, the methods, the studies, the design space, the PARs
    of ``doe_report.par_table``, assertions and report statements); every quote is new.
    """
    import doe_report as D
    import tables as T
    from annex_contract.assertions import AssertionStore
    from annex_contract.concepts import Concept, ConceptStore
    from annex_contract.discourse import DocumentRelationship, ExplicitNonClaim
    from annex_contract.results import Deviation, ProcessCapability, StatisticalModelFit
    from annex_contract.summaries import ReportSection
    doc, f = "PCR-005", PCR5_FILE
    ns, tabs = qmd_namespace("PCR-005_protein_a.qmd")
    A, add, ST, st = _adders(doc, f)
    cap = {k: v[3] for k, v in tabs.items()}
    text = _document_text(f)
    by_label = _attr_key_by_label()
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))

    def sid(s):
        return f"{doc}_sec_{s}"

    # ---- the rendered tables ---------------------------------------------------------------
    prow = param_rows(PAUO, classified=True)                       # @tbl-params
    cdf = tabs["tbl-cqa"][1]
    ckeys = [by_label[n] for n in cdf["CQA"]]
    crow = cqa_rows(ckeys)                                          # @tbl-cqa
    chdf = tabs["tbl-chronology"][1]
    chrow = captured_rows(tabs["tbl-chronology"], chdf["Study"])
    rel = md_string_rows(P.related_docs_md(doc))
    sops = md_string_rows(P.sop_table(sops=ns["sops_pa"], amvs=ns["amvs_pa"]))
    devrow = md_string_rows(P.dev_register(doc))
    crt = ns["cr"]                                                  # T.criteria_results(UO)
    crres = ctable_rows(crt, [by_label[r.split(CELL_SEP)[0]] for r in crt.rows()])
    pt = D.par_table(PAUO)
    parrow = par_rows(PAUO)
    capdf = tabs["tbl-cap"][1]
    caprow = captured_rows(tabs["tbl-cap"], [by_label[c] for c in capdf["CQA"]])
    adf = tabs["tbl-adequacy"][1]
    arow = captured_rows(tabs["tbl-adequacy"])
    coef = {k: (tabs[t][1], captured_rows(tabs[t], tabs[t][1]["Term"]))
            for k, t in [("hcp", "tbl-coef-hcp"), ("frag", "tbl-coef-frag")]}
    sy_df = tabs["tbl-scr-yield"][1]
    sy_row = captured_rows(tabs["tbl-scr-yield"], sy_df["Term"])
    letter = {v: k for k, v in D.factor_letters(PAUO).items()}     # "A" -> "load"
    pname = {p.key: p.name for p in P.CFG.unit_op(PAUO).parameters}

    # ---- entities --------------------------------------------------------------------------
    step = S.ProcessStep(
        step_id="step:protein_a", step_name=PAUO_NAME, step_number=str(PASTEP),
        unit_operation=PAUO_NAME,
        description="The capture step of the purification train, operated in bind and elute "
                    "mode. It removes most of the host cell protein and DNA of the clarified "
                    "harvest, partly clears fragments, and adds leached Protein A ligand. The "
                    "eluate passes to low-pH viral inactivation (Step 6) without neutralization.",
        input_materials=["clarified harvest"],
        output_materials=["Protein A eluate at elution pH (low-pH viral inactivation load)"],
        equipment=["laboratory column packed with the commercial Protein A resin"],
        source_references=[
            ref(doc, f, sid("exec"), "Executive summary",
                "Protein A chromatography is the capture step of the purification train."),
            ref(doc, f, sid("intro"), "Product and unit operation",
                "A low-pH buffer elutes the antibody into a small volume, and the eluate passes to "
                "low-pH viral inactivation (Step 6) without neutralization.")],
        metadata=meta())
    equipment = [S.Equipment(
        equipment_id="equip:pa_sdm_column",
        equipment_name="laboratory column packed with the commercial Protein A resin",
        equipment_type="chromatography column (scale-down model)", site_name=P.SENDING_SITE,
        source_references=[ref(doc, f, sid("sdm"), "Scale-down model and its qualification",
                               "The scale-down model is a laboratory column packed with the "
                               "commercial Protein A resin")],
        metadata=meta())]
    class_q = {name: f"{name} was classified as a {cls}." for name, cls in
               zip(tabs["tbl-params"][1]["Parameter"], tabs["tbl-params"][1]["Class"])}
    params = []
    for r in PAPARAM_ROWS:
        name = r["parameter"]
        params.append(S.ProcessParameter(
            parameter_id=PAPARAM_CONCEPT[name], parameter_name=name,
            parameter_type=r["classification"], unit=r["unit"], target_value=f"{r['setpoint']:g}",
            NOR=f"{r['nor_low']:g}–{r['nor_high']:g} {r['unit']}",
            PAR=f"{r['par_low']:g}–{r['par_high']:g} {r['unit']}",
            associated_step=PASTEP_LABEL,
            rationale_for_criticality=f"Classified {r['classification']} under SOP-4001 by the "
                                      f"decision logic of PCMP-001 §7.7 (Parameter classification).",
            source_references=[
                ref(doc, f, sid("factors"), "Factors, ranges and the knowledge space", prow[name],
                    table_title=cap["tbl-params"], table_id=f"{doc}_tab_params",
                    table_header=prow.header),
                ref(doc, f, sid("class"), "Parameter classification", class_q[name])],
            metadata=meta()))
    attrs = []
    for i, key in enumerate(ckeys):
        r = _pa_cqa_row(key)
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"], acceptance_criteria=[f"{cdf['Acceptance'].iloc[i]} (drug substance)"],
            associated_steps=[PASTEP_LABEL],
            rationale_for_criticality=f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = "
                                      f"{r['tool1_score']}.",
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref(doc, f, sid("cqa"), "Quality attributes in scope", crow[key],
                                   table_title=cap["tbl-cqa"], table_id=f"{doc}_tab_cqa",
                                   table_header=crow.header)],
            metadata=meta()))
    meth_prose = {
        "AMV-3012": ("hcp", "Pool host cell protein was measured by ELISA (AMV-3012)"),
        "AMV-3016": ("leached_protein_a", "Leached Protein A was measured by ELISA (AMV-3016)"),
        "AMV-3019": ("step_yield", "from the protein concentration by absorbance at 280 nm "
                                   "(AMV-3019)"),
        "AMV-3020": ("fragments_lmw", "Fragments were measured by nrCE-SDS (AMV-3020, under "
                                      "SOP-3015)"),
        "AMV-3011": ("aggregates_hmw", "SEC (AMV-3011) remains the method for aggregate"),
        "AMV-3013": ("acidic_variants", "Acidic variants in the hold study were measured by icIEF "
                                        "(AMV-3013)"),
        "AMV-3014": ("residual_dna", "and residual DNA by qPCR (AMV-3014)"),
    }
    amv_name = dict(ns["amvs_pa"])
    methods = []
    for amv, name in ns["amvs_pa"]:
        key, q = meth_prose[amv]
        attrs_m = [key] + (["fragments_lmw"] if amv == "AMV-3011" else [])
        methods.append(S.AnalyticalMethod(
            method_id=amv, method_name=name, method_type=METHOD_TYPE.get(amv),
            associated_attributes=[f"attr:{a}" for a in attrs_m], validation_status="validated",
            source_references=[ref(doc, f, sid("analytics"), "Analytical methods", sops[amv],
                                   table_title="Controlled procedures and method validations",
                                   table_header=sops.header),
                               ref(doc, f, sid("analytics"), "Analytical methods", q)]
            + (size_variant_refs(doc, f, "Analytical methods", [PAUO], SIZE_VARIANT_TOKEN[amv],
                                 text) if amv in SIZE_VARIANT_TOKEN else []),
            metadata=meta()))
    capab = []
    for key, row in caprow.items():
        c = capdf[capdf["CQA"] == names[key]].iloc[0]
        capab.append(ProcessCapability(
            capability_id=f"{doc}-CAP{len(capab) + 1:02d}", quality_attribute=f"attr:{key}",
            index_name="Cpk", index_value=float(c["Cpk"]), specification_side=c["Spec"],
            acceptance_range=c["Acceptance"], mean=c["Mean ± SD"].split(" ± ")[0],
            standard_deviation=c["Mean ± SD"].split(" ± ")[1],
            unit=P.CFG.cqa(key)["unit"], basis="simulated", n_batches=int(ns["mc_n"].replace(",", ""))
            if isinstance(ns["mc_n"], str) else int(ns["mc_n"]),
            source_references=[ref(doc, f, sid("cap"), "Process capability and robustness", row,
                                   table_title=cap["tbl-cap"], table_id=f"{doc}_tab_cap",
                                   table_header=caprow.header)],
            metadata=meta()))

    def _num(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return None
    resp_of = {"Pool HCP (ng/mg)": "pool_hcp_ng_mg", "Step yield": "step_yield"}
    resp_of.update({D.RESP_LABEL[r]: r for r in list(D.responses(PAUO)) + D.fragment_responses(PAUO)})
    fits = []
    for i, row in arow.items():
        a = adf.iloc[i]
        fits.append(StatisticalModelFit(
            model_fit_id=f"{doc}-FIT{i + 1:02d}", response=resp_of.get(a["Response"], a["Response"]),
            unit_operation=PAUO_NAME, model_form=a["Model"], n_runs=P.doe_runs(PAUO, "rsm"),
            r_squared=_num(a["R²"]), adjusted_r_squared=_num(a["Adj. R²"]),
            predicted_r_squared=_num(a["Pred. R²"]), p_value=_num(a["Model p"]),
            lack_of_fit_p=_num(a["Lack of fit p"]),
            adequacy_statement=f"Criteria 2 to 4 of PCP-005 §7 met: {a['Criteria 2–4 met']}.",
            source_references=[ref(doc, f, sid("rsm"), "Response-surface models", row,
                                   table_title=cap["tbl-adequacy"], table_id=f"{doc}_tab_adequacy",
                                   table_header=arow.header)],
            metadata=meta()))
    dev_sec = {
        "DEV-005-01": ("DEV-005-01. Elution buffer pH below target on a response-surface run",
                       "The run was analysed at its design setting, so the error in pH enters the "
                       "model as part of the residual of this run."),
        "DEV-005-02": ("DEV-005-02. Leached Protein A result initially out of trend",
                       "The investigation attributed the first result to suspected carryover in "
                       "the ELISA."),
        "DEV-005-03": ("DEV-005-03. Scale-down equivalence not demonstrable with the planned "
                       "set-point runs",
                       "The root cause is a number of replicates too small for the margin the "
                       "plan set."),
    }
    facts = P.dev_facts(doc)
    devs = []
    for did, row in devrow.items():
        r = facts[facts["dev_id"] == did].iloc[0]
        sec, q = dev_sec.get(did, ("Deviations from the plan", None))
        refs = [ref(doc, f, sid("dev"), "Deviations from the plan", row,
                    table_header=devrow.header),
                ref(doc, f, sid("disc"), "Discussion",
                    "The three deviations of the study did not change its conclusions")]
        if q and _present(q, text):
            refs.append(ref(doc, f, sid("dev"), sec, q))
        devs.append(Deviation(
            deviation_id=did, summary=row.split(CELL_SEP)[1], unit_operation=PAUO_NAME,
            detected_during=row.split(CELL_SEP)[2], disposition=row.split(CELL_SEP)[3],
            no_impact_on_conclusions=True, source_references=refs, metadata=meta()))
    nc = [
        ExplicitNonClaim(
            non_claim_id=f"{doc}-NC01", subject="viral clearance", unit_operation=PAUO_NAME,
            statement="No viral clearance claim is made for the Protein A step.",
            handled_elsewhere="low-pH inactivation, anion exchange and virus filtration; "
                              "consolidated in PCMR-001",
            source_references=[ref(doc, f, sid("intro"), "Product and unit operation",
                                   "Although Protein A chromatography removes some virus, no viral "
                                   "clearance claim is made for this step")],
            metadata=meta()),
        ExplicitNonClaim(
            non_claim_id=f"{doc}-NC02", subject="short bed at high protein load",
            unit_operation=PAUO_NAME,
            statement="A short bed at the upper end of the load range was not characterized and "
                      "no claim is made for it.",
            source_references=[ref(doc, f, sid("class"), "Parameter classification",
                                   "A short bed at the upper end of the load range was not "
                                   "characterized, and no claim is made for it.")],
            metadata=meta()),
        ExplicitNonClaim(
            non_claim_id=f"{doc}-NC03", subject="PAR for leached Protein A and fragments",
            unit_operation=PAUO_NAME,
            statement="No PAR is claimed for leached Protein A or fragments, because no adequate "
                      "model results for them; both met their criteria in every run.",
            source_references=[ref(doc, f, sid("par"),
                                   "Proven acceptable ranges per attribute and parameter",
                                   "For leached Protein A and fragments the table rows come from "
                                   "models that are not adequate, and no PAR is claimed from them.")],
            metadata=meta()),
        ExplicitNonClaim(
            non_claim_id=f"{doc}-NC04", subject="effect of feed quality", unit_operation=PAUO_NAME,
            statement="The effect of feed quality on the step was not estimated.",
            handled_elsewhere="PCR-003 and PCR-004",
            source_references=[ref(doc, f, sid("operation"), "Operation",
                                   "The effect of feed quality on the step was therefore not "
                                   "estimated in these studies.")],
            metadata=meta()),
        ExplicitNonClaim(
            non_claim_id=f"{doc}-NC05", subject="step yield at manufacturing scale",
            unit_operation=PAUO_NAME,
            statement="The step yield model is not used for any range or prediction, because the "
                      "scale-down model was not shown equivalent for step yield.",
            source_references=[ref(doc, f, sid("sdm"), "Scale-down model and its qualification",
                                   "No known scale effect applies to step yield.")],
            metadata=meta()),
    ]
    kind_of = {"Rolls up into": "rolls_up_into", "Sibling — paired document": "executed_under",
               "Parent — risk basis for study scope": "scoped_by",
               "Parent — transfer scope": "scoped_by"}
    rels = [DocumentRelationship(
        relationship_id=f"{doc}-R{i + 1:02d}", kind=kind_of.get(row.split(CELL_SEP)[-1], "references"),
        source_document_id=doc, target_document_ref=target, statement=row.split(CELL_SEP)[-1],
        source_references=[ref(doc, f, sid("basis"), "Regulatory and scientific basis", row,
                               table_header=rel.header)],
        metadata=meta()) for i, (target, row) in enumerate(rel.items())]
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=sid("exec"), process_steps=[step],
                                  sites=_site_entities(doc, f, sid("exec"))),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("intro"),
                                  non_claims=[nc[0]], document_relationships=rels),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("cqa"), quality_attributes=attrs),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("sdm"), equipment=equipment,
                                  non_claims=[nc[4]]),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("operation"), non_claims=[nc[3]]),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("analytics"),
                                  analytical_methods=methods),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("factors"), parameters=params),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("rsm"), model_fits=fits),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("par"), non_claims=[nc[2]]),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("cap"), capabilities=capab),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("class"), non_claims=[nc[1]]),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("dev"), deviations=devs),
    ]

    # ---- studies: every study of a schema type the chronology carries ---------------------
    fac = [pname[k] for k in D.screening_factors(PAUO)]
    uni = [p.name for p in P.CFG.unit_op(PAUO).parameters if p.study != "multivariate"]
    resp_scr = list(D.responses(PAUO))
    resp_rsm = resp_scr + [r for r in D.fragment_responses(PAUO, "rsm") if r == "lmw_cesds_pct"]

    def prose(kind, sid_):
        return {
            "qualification": [("Scale-down model and its qualification",
                               f"The model was qualified under SOP-1001 in study {sid_} ("),
                              ("Scale-down model and its qualification",
                               f"and in the supplementary study {sid_} (")],
            "screening": [("Screening design", "Because the design is a full factorial, no effect "
                                               "is aliased with another")],
            "rsm": [("Response-surface design", "was a face-centred central composite design in "
                                                "the same")],
            "univariate": [("Univariate assessment", "Operating temperature and bed height were "
                                                     f"studied one factor at a time in study {sid_}")],
        }.get(kind, [])
    design = {"screening": dict(design_name="full two-level factorial", factors=fac,
                                responses=resp_scr, n_runs=P.doe_runs(PAUO, "screening"),
                                n_center_points=P.doe_centre_points(PAUO, "screening")),
              "rsm": dict(design_name="face-centred central composite design", factors=fac,
                          responses=resp_rsm, n_runs=P.doe_runs(PAUO, "rsm"),
                          n_center_points=P.doe_centre_points(PAUO, "rsm")),
              "univariate": dict(design_name="one factor at a time at the low and high end of the "
                                             "range studied", factors=uni, responses=resp_scr),
              "qualification": dict(responses=["pool_hcp_ng_mg", "step_yield",
                                               "leached_protein_a_ppm"])}
    studies, unrendered = [], []
    for sid_, r in ns["chron"].iterrows():
        stype = STUDY_TYPE.get(r["kind"])
        if stype is None:
            continue
        if not _present(chrow[sid_], text):
            unrendered.append(sid_)
            continue
        d = design[r["kind"]]
        refs = [ref(doc, f, sid("chrono"), "Factors, ranges and the knowledge space", chrow[sid_],
                    table_title=cap["tbl-chronology"], table_id=f"{doc}_tab_chrono",
                    table_header=chrow.header)]
        refs += [ref(doc, f, sid("design"), sec, q) for sec, q in prose(r["kind"], sid_)
                 if _present(q, text)]
        studies.append(S.StudyDesign(
            study_id=f"study:{sid_}", study_type=stype, unit_operation=PAUO_NAME,
            scale_down_model="laboratory column packed with the commercial Protein A resin",
            associated_parameters=[PAPARAM_CONCEPT[x] for x in d.get("factors", [])],
            source_references=refs, metadata=meta(), **d))

    # ---- design space and the proven acceptable ranges -------------------------------------
    design_spaces = [S.DesignSpace(
        design_space_id="ds:protein_a", unit_operation=PAUO_NAME,
        parameters=[PAPARAM_CONCEPT["Protein load"], PAPARAM_CONCEPT["Elution buffer pH"]],
        quality_attributes_constrained=["attr:hcp"],
        definition="The region in protein load and elution buffer pH, the two WC-CPPs, over which "
                   "pool host cell protein meets its intermediate acceptance criterion. Leached "
                   "Protein A and fragments met their criteria in every run and step yield has no "
                   "criterion, so they do not constrain it. The excluded region is the corner of "
                   "high protein load and low elution buffer pH; the claim is made through the "
                   "NOR-propagated PARs.",
        source_references=[ref(doc, f, sid("ds"), "Design space",
                               "The design space of this step is the region in protein load and "
                               "elution buffer pH, the two WC-CPPs, over which pool host cell "
                               "protein meets its intermediate acceptance criterion.")],
        metadata=meta())]
    no_model = {D.RESP_LABEL["leached_protein_a_ppm"], D.RESP_LABEL["lmw_cesds_pct"]}
    iac = D.iac_table(PAUO).set_index("response")
    pars = []
    for i, r in enumerate(pt.to_dict("records"), 1):
        cqa, param, unit = r["CQA"], r["Parameter"], (r["Unit"] or "")
        resp = next(x for x in list(D.responses(PAUO)) + D.fragment_responses(PAUO)
                    if D.RESP_LABEL.get(x) == cqa)
        ia = iac.loc[resp]
        basis = (f"Intermediate acceptance criterion {T.crit(ia['iac_low'], ia['iac_high'], ia['spec_type'])} "
                 f"({ia['basis']}), derived a priori by PCMP-001 §7.3: the drug substance criterion "
                 f"{T.crit(ia['ds_low'], ia['ds_high'], ia['spec_type'])} carried back through the "
                 f"platform worst case of the downstream steps (clearance fold "
                 f"{T.num(ia['downstream_fold'])}, increase {T.num(ia['downstream_added'])}), with "
                 f"no margin.")
        if cqa in no_model:
            basis += (" The report claims no PAR from this row, because no adequate model results "
                      "for this output.")
        pars.append(S.ProvenAcceptableRange(
            par_id=f"{doc}-PAR{i:02d}", unit_operation=PAUO_NAME, quality_attribute=cqa,
            parameter=param, characterization_range=f"{r['Char. range']} {unit}".strip(),
            par_at_setpoint=f"{r['PAR (set-point)']} {unit}".strip()
            if not str(r["PAR (set-point)"]).startswith("none") else str(r["PAR (set-point)"]),
            par_nor_propagated=f"{r['PAR (NOR)']} {unit}".strip()
            if not str(r["PAR (NOR)"]).startswith("none") else str(r["PAR (NOR)"]),
            acceptance_basis=basis,
            source_references=[ref(doc, f, sid("par"),
                                   "Proven acceptable ranges per attribute and parameter",
                                   parrow[(cqa, param)], table_title=cap["tbl-par"],
                                   table_id=f"{doc}_tab_par", table_header=parrow.header)],
            metadata=meta()))

    # ---- assertions ------------------------------------------------------------------------
    for name, cid in PAPARAM_CONCEPT.items():
        add("step:protein_a", "step_has_parameter", cid,
            f"{PAUO_NAME} has process parameter {name}, classified "
            f"{tabs['tbl-params'][1].set_index('Parameter').loc[name, 'Class']}.",
            "Factors, ranges and the knowledge space", prow[name], prow.header, cap["tbl-params"])
    role = {"leached_protein_a": "introduces {n}, the only attribute of the CQA register it introduces",
            "hcp": "is the principal point of clearance for {n}",
            "residual_dna": "is the principal point of clearance for {n}",
            "fragments_lmw": "partly clears {n}",
            "aggregates_hmw": "does not separate {n} from monomer; aggregate was measured for "
                              "information"}
    for key in ckeys:
        add("step:protein_a", "step_has_quality_attribute", f"attr:{key}",
            f"{PAUO_NAME} " + role[key].format(n=names[key]) + ".", "Quality attributes in scope",
            crow[key], crow.header, cap["tbl-cqa"])
    for amv, (key, q) in meth_prose.items():
        add(f"attr:{key}", "attribute_measured_by_method", f"method:{amv}",
            f"{names.get(key, 'Step yield')} is measured by {amv} ({amv_name[amv]}).",
            "Analytical methods", q)
    for key, row in crres.items():
        c = row.split(CELL_SEP)
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{PAUO}_{key}_iac",
            f"At the Protein A step {c[0]} is judged against its intermediate acceptance criterion "
            f"{c[1]}; the model predicts {c[2]} at the set-point and {c[3]} over the NOR.",
            "Outputs against their criteria over the NOR", row, crres.header, crt.caption)
    hdf, hrow = coef["hcp"]
    for term in ["A", "B", "D", "C"]:
        h = hdf.set_index("Term").loc[term]
        name = pname[letter[term]]
        sig = h["Sig."].strip() != ""
        add(PAPARAM_CONCEPT[name],
            "parameter_impacts_attribute" if sig else "parameter_does_not_significantly_impact_attribute",
            "attr:hcp",
            f"{name} ({term}) has a response-surface coefficient on pool host cell protein of "
            f"{h['Coef.']:,.0f} ng/mg per half range (p = {h['p-value']:.3g})"
            + ("." if sig else ", not significant."), "Pool host cell protein", hrow[term],
            hrow.header, cap["tbl-coef-hcp"])
    fdf, frow = coef["frag"]
    fb = fdf.set_index("Term").loc["B"]
    add(PAPARAM_CONCEPT["Elution buffer pH"], "parameter_impacts_attribute", "attr:fragments_lmw",
        f"Fragments by nrCE-SDS fall slightly as elution buffer pH rises (coefficient "
        f"{fb['Coef.']:.3f} % per half range, p = {fb['p-value']:.3g}); the fragment model as a "
        f"whole is not significant.", "Fragments by nrCE-SDS", frow["B"], frow.header,
        cap["tbl-coef-frag"])
    for term in ["D", "A", "C"]:
        y = sy_df.set_index("Term").loc[term]
        name = pname[letter[term]]
        add(PAPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:step_yield",
            f"{name} ({term}) changes step yield by {100 * y['Effect']:.1f} percentage points across "
            f"its range in the screening design.", "Screening: factor effects", sy_row[term],
            sy_row.header, cap["tbl-scr-yield"])

    # ---- report sections -------------------------------------------------------------------
    ex = "Executive summary"
    st("Version 2.0 re-analyses the experiments of Version 1.0 against the criteria of PCMP-001 "
       "Version 2.0, issued under INV-001, and adds fragments by nrCE-SDS.", ex,
       "It re-analyses the same experiments as Version 1.0 against the criteria of PCMP-001 "
       "Version 2.0, issued under INV-001, and adds the fragment results by nrCE-SDS.")
    st("Protein load and elution buffer pH are WC-CPPs, load flow rate and end of pool collect "
       "KPPs, and operating temperature and bed height GPPs; the step has no CPP.", ex,
       "No parameter of the step was classified as a CPP.")
    st("With the planned set-point runs the scale-down model could not demonstrate equivalence "
       "whatever the means were (DEV-005-03); supplementary runs were made with the margins "
       "unchanged.", "Changes in this revision",
       "The planned set-point runs could not demonstrate equivalence whatever the means were")
    st("Leached Protein A is consistently lower in the scale-down model, an expected scale effect "
       "from the longer hold of the manufacturing load before capture, which this study does not "
       "test; the difference was accepted.", "Scale-down model and its qualification",
       "Its expected cause is the longer hold of the clarified harvest before capture at "
       "manufacturing scale, which gives host cell proteases more time to cleave ligand from the "
       "resin.")
    st("The scale-down model was not shown equivalent for step yield, so the step yield model is "
       "not used for any range or prediction, and the KPP classes rest on the direction of the "
       "yield effects.", ex,
       "The KPP classes of load flow rate and end of pool collect rest on the direction of the "
       "yield effects, which both designs show, and not on the model")
    st("Pool host cell protein rises with protein load and as elution buffer pH falls, the two "
       "interact, and it falls as end of pool collect is extended.", ex,
       "Pool host cell protein rises with protein load and as elution buffer pH falls, and the two "
       "parameters interact.")
    st("The full quadratic model for step yield failed the predictive criterion and was replaced "
       "by a reduced model with the terms significant in both designs.", ex,
       "The full quadratic model fails the predictive criterion, and a reduced model with the terms "
       "significant in both designs meets criteria 2 to 4 of PCP-005 §7.")
    st("No response-surface model meets criterion 5; the conclusions on pool host cell protein "
       "rest on an influence analysis, a departure from the plan.", "Deviations from the plan",
       "The analysis departed from the plan in one place.")
    st("The effect of end of pool collect on pool host cell protein and its interactions have "
       "opposite signs in the two designs, for a reason that was not identified.", ex,
       "The difference is larger than the noise of the screening design, and its cause was not "
       "identified")
    st("Load flow rate did not raise pool host cell protein as the mechanism predicts.", ex,
       "Load flow rate did not raise pool host cell protein as the mechanism predicts.")
    st("Every output met its intermediate acceptance criterion across the NOR, and the "
       "NOR-propagated PAR of elution buffer pH for pool host cell protein is the only one narrower "
       "than its range studied.", "Parameter classification",
       "the only one whose NOR-propagated PAR is narrower than its range studied")
    st("The Protein A eluate may be held at elution pH for the full hold studied at both "
       "temperatures; fragments rose at both, with no temperature dependence shown.",
       "Hold study of the Protein A eluate",
       "so the data do not show that fragmentation depends on temperature")
    st("No difference from the set-point runs was detected at either end of the ranges of "
       "operating temperature and bed height, and with two runs at each end the intervals are "
       "wide.", "Univariate assessment",
       "With two runs at each end the intervals are wide, so the study excludes only effects "
       "larger than their upper bounds.")
    st("The Version 2.0 criterion for pool host cell protein is wider than the Version 1.0 limit, "
       "which was never approved and is replaced by a criterion derived without data from the "
       "studies it judges.", "Changes in this revision",
       "The Version 1.0 limit was never approved and appears in no approved plan, and it is "
       "replaced by a criterion derived without data from the studies it judges.")
    st("The step yield effects describe the scale-down model; their size at manufacturing scale "
       "is not established.", "Scale-down model and its qualification",
       "Their direction, which both designs show, supports the KPP classes in")
    st("In the NOR-propagated analysis the model coefficients are drawn from their estimated "
       "covariance in every simulated run, together with the residual.", "Acceptance basis",
       "In the NOR-propagated analysis the model coefficients are drawn from their estimated "
       "covariance in every simulated run, together with the residual.")

    concepts = [Concept(concept_id="step:protein_a", concept_type="PROCESS_STEP",
                        canonical_name=PAUO_NAME,
                        aliases=["Protein A", "Protein A capture", "capture step", "Step 5"],
                        review_status="human_verified")]
    concepts += [Concept(concept_id=cid, concept_type="PROCESS_PARAMETER", canonical_name=name,
                         review_status="human_verified") for name, cid in PAPARAM_CONCEPT.items()]
    concepts += _attr_concepts(ckeys + ["acidic_variants"])
    concepts.append(Concept(concept_id="attr:step_yield", concept_type="PERFORMANCE_ATTRIBUTE",
                            canonical_name="Step yield", aliases=["yield"],
                            review_status="human_verified"))
    concepts += _method_concepts([a for a, _ in ns["amvs_pa"]], amv_name)
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], **rev2_layer(doc, f),
        schema_extensions_used=COMMON_EXT + REV2_EXT + [
            "ProvenAcceptableRange (new model) — per output x parameter PAR at set-point and "
            "NOR-propagated, from doe_report.par_table",
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "ProvenAcceptableRange keeps the field name par_at_setpoint although the value is "
            "computed with the other factors at the design centre (registered discrepancy D-001). "
            "For this step the set-point of every design factor is the centre of its range studied.",
            "The leached Protein A and fragment PAR rows come from models that are not adequate; "
            "the report claims no PAR from them, and their acceptance_basis says so.",
            "The hold study S-PA-HLD and the nrCE-SDS retest S-PA-RET have no StudyDesign.study_type "
            "and have no study record; the hold result is a report statement. S-PA-SDM2 (DEV-005-03) "
            "is a scale_down_qualification record.",
            "The scale-down qualification table, the univariate result tables, the residual checks, "
            "the centre-point tables, the screening and coefficient tables other than those cited "
            "by assertions, the hold table and the design matrices are not represented row by row.",
            "The Cpk of leached Protein A is recorded as printed; the report states it is not "
            "meaningful because the simulated values lie below the limit of quantitation.",
            "Step yield is a performance attribute with no criterion (concept attr:step_yield).",
            "rhetorical_spans re-curated against the Version 2.0 text "
            "(authoring/rhetorical/PCR-005.spans.yaml). weak_claims is empty.",
        ] + _unrendered_note(unrendered),
        inventory=rev2_inventory(doc, f, "process_characterization_report", PAUO_NAME,
                                 ["process characterization", "Protein A chromatography",
                                  "affinity capture", "intermediate acceptance criteria",
                                  "design of experiments", "parameter classification",
                                  "scale-down model qualification"]),
        entities=entities, studies=studies, design_spaces=design_spaces,
        proven_acceptable_ranges=pars,
        report_sections=[ReportSection(section_id=f"{doc}-summary", title="Report summary",
                                       statements=ST)],
        assertions=AssertionStore(run_id=f"gt-{doc}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{doc}", concepts=concepts),
        rhetorical_spans=build_rhetorical_spans(doc, f),
        acceptance_criteria=acceptance_criteria_layer(doc, f, "Changes in this revision",
                                                      T.criteria_change([PAUO]), [PAUO]))


# --------------------------------------------------------------------------- #
# PCMP-001 — Process Characterization Master Plan, Version 2.0.                 #
# --------------------------------------------------------------------------- #
def _iac_ctable_keys(table):
    """(step key, attribute key) of every row of ``T.iac_derivation()``, read off the rows.

    A row continuing a vertical merge starts with empty cells and carries only its step; its
    attribute is the one named by the last row that opened a merge."""
    import tables as T
    attr_of = {v: k for k, v in T.ATTR_NAME.items()}
    step_of = {v: k for k, v in T.STEP_NAME.items()}
    keys, cur = [], None
    for row in table.rows():
        cells = row.split(CELL_SEP)
        if cells[0].strip() in attr_of:
            cur = attr_of[cells[0].strip()]
        step = next(step_of[c.strip()] for c in cells if c.strip() in step_of)
        keys.append((step, cur))
    return keys


def _pbs_keys():
    """(step key, parameter name) of every row of ``T.parameters_by_step()``, in its order."""
    p = P.csv("parameter_classification.csv")
    keys = []
    for k in P.CFG.train_order:
        keys += [(k, n) for n in p[p["step"] == P.CFG.unit_op(k).step]["parameter"]]
    return keys


def _in_force_records(doc, f, sec, table):
    """In-force Version 2.0 AcceptanceCriterionRecords, one per row of a printed
    ``T.iac_derivation(...)`` table and anchored on that row."""
    iac = P.csv("iac.csv")
    rows = ctable_rows(table, _iac_ctable_keys(table))
    out = []
    for (sk, cqa), row in rows.items():
        r = iac[(iac["step_key"] == sk) & (iac["cqa"] == cqa)].iloc[0]
        out.append(S.AcceptanceCriterionRecord(
            step=sk, attribute=cqa, low=None if r["iac_low"] == 0 else float(r["iac_low"]),
            high=None if not np.isfinite(r["iac_high"]) else float(r["iac_high"]),
            unit=P.CFG.cqa(cqa)["unit"], basis=str(r["basis"]), revision=P.REV2["rev"],
            status="in force",
            source=ref(doc, f, f"{doc}_crit", sec, row, table_title=table.caption,
                       table_id=table.label, table_header=rows.header)))
    return out, rows


def build_master_plan():
    """PCMP-001 Version 2.0: the master plan reissued with a-priori intermediate criteria.

    Fitted to the Version 2.0 text. Its tables are complex tables (``T.frame``, ``T.CTable`` and
    the ``T.`` builders), read back through :func:`qmd_ctables` from the object the plan printed;
    only the process-train table is still a ``show`` table. The parameter table shows the NOR in
    force, so the parameter records carry that NOR, and each NOR a Version 2.0 report narrowed is
    a statement anchored on its footnote.
    """
    import doe_report as D
    import tables as T
    from annex_contract.assertions import AssertionStore
    from annex_contract.concepts import Concept, ConceptStore
    from annex_contract.discourse import DocumentRelationship
    from annex_contract.results import ModularContribution
    from annex_contract.summaries import ReportSection
    doc, f = "PCMP-001", PCMP_FILE
    qmd = "PCMP-001_master_plan.qmd"
    ns, tabs = qmd_namespace(qmd)
    ct = qmd_ctables(qmd)
    A, add, ST, st = _adders(doc, f)
    text = _document_text(f)
    cap = {k: v[3] for k, v in tabs.items()}

    def sid(s):
        return f"{doc}_sec_{s}"
    tdf = tabs["tbl-train"][1]                                     # show(steps_tab)
    train = captured_rows(tabs["tbl-train"], P.CFG.train_order)
    cqa_t, cdf = ct["tbl-cqa"]                                      # T.frame, ordered by category
    key_of = dict(zip(P.cqa_reg["cqa"], P.cqa_reg["key"]))
    cdf = cdf.assign(key=[key_of[c] for c in cdf["CQA"]]).set_index("key")
    crow = ctable_rows(cqa_t, cdf.index)
    pbs = ct["tbl-parameters-by-step"][0]                           # T.parameters_by_step()
    prow = ctable_rows(pbs, _pbs_keys())
    eq_t = ct["tbl-equipment"][0]                                   # T.calibration_windows(...)
    eqdf = T.calibration_windows_data()                             # row i is body row i
    eqrow = ctable_rows(eq_t)
    if len(eqrow) != len(eqdf):
        raise ValueError(f"{eq_t.label}: {len(eqrow)} rows for {len(eqdf)} studies")
    des_t = ct["tbl-designs"][0]                                    # T.CTable from design_tab
    drow = ctable_rows(des_t, ns["doe_keys"])
    ch_t, chdf = ct["tbl-chronology"]                               # T.frame(chrono_tab)
    chrow = ctable_rows(ch_t, chdf["Study"])
    pl_t, pldf = ct["tbl-plans"]                                    # T.frame(plan_tab)
    plrow = ctable_rows(pl_t, pldf["Plan"])
    vc_t, vc = ct["tbl-viral"]                                      # T.frame(vc_tab)
    vcrow = ctable_rows(vc_t, vc["Virus"])
    sop_t, sop_df = ct["tbl-sops"]                                  # T.sop_references(...)
    sops = ctable_rows(sop_t, sop_df["Reference"])
    iac_t = ct["tbl-iac"][0]                                        # T.iac_derivation()
    in_force, iacrow = _in_force_records(doc, f, "Intermediate acceptance criteria", iac_t)
    iac = P.csv("iac.csv")

    # ---- entities --------------------------------------------------------------------------
    steps = _corpus_steps(doc, f, sid("purpose"), "Purpose and scope", rows=train,
                          roles={k: tdf.loc[tdf["Step"] == P.CFG.unit_op(k).step,
                                            "Principal role"].iloc[0] for k in P.CFG.train_order},
                          table_title=cap["tbl-train"])
    attrs = []
    for r in P.cqa_reg.to_dict("records"):
        c = cdf.loc[r["key"]]
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{r['key']}", attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"], acceptance_criteria=[f"{c['Acceptance']} (drug substance)"],
            associated_steps=[c["Formed or set at"]],
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref(doc, f, sid("cqa"), "Critical quality attribute framework",
                                   crow[r["key"]], table_title=cqa_t.caption,
                                   table_id=f"{doc}_tab_cqa", table_header=crow.header)],
            metadata=meta()))
    preg = P.csv("parameter_classification.csv")
    params, pid = [], {}
    for (k, name), row in prow.items():
        uo = P.CFG.unit_op(k)
        pk = next(q.key for q in uo.parameters if q.name == name)
        r = preg[(preg["step"] == uo.step) & (preg["parameter"] == name)].iloc[0]
        pid[(k, name)] = f"param:{k}_{pk}"
        params.append(S.ProcessParameter(
            parameter_id=pid[(k, name)], parameter_name=name,
            parameter_type=r["classification"], unit=r["unit"],
            target_value=f"{r['setpoint']:g}",
            NOR=f"{r['nor_low']:g}–{r['nor_high']:g} {r['unit']}",
            PAR=f"{uo.param(pk).prange[0]:g}–{uo.param(pk).prange[1]:g} {r['unit']}",
            associated_step=f"{P.UNIT_OP_TITLES[k]} (Step {uo.step})",
            rationale_for_criticality=(f"Classified {r['classification']} in PCR-{uo.step:03d} "
                                       f"under SOP-4001; carried here, not re-derived."),
            source_references=[ref(doc, f, sid("risk"), "Risk-based prioritization", row,
                                   table_title=pbs.caption, table_id=f"{doc}_tab_params",
                                   table_header=prow.header)],
            metadata=meta()))
    eq_ids = list(dict.fromkeys(eqdf["Equipment"]))
    first_row = {e: list(eqdf.index[eqdf["Equipment"] == e])[0] for e in eq_ids}
    equipment = [S.Equipment(
        equipment_id=f"equip:{e}", equipment_name=e,
        equipment_type=eqdf.loc[first_row[e], "Description"], site_name=P.SENDING_SITE,
        # the first row of each system names it; the rows below continue its merged cells
        source_references=[ref(doc, f, sid("sdm"), "Scale-down model strategy", eqrow[first_row[e]],
                               table_title=eq_t.caption, table_id=f"{doc}_tab_eq",
                               table_header=eqrow.header)],
        metadata=meta()) for e in eq_ids]
    methods, amv_names = [], {}
    for rid, row in sops.items():
        if not rid.startswith("AMV-"):
            continue
        amv_names[rid] = sop_df.loc[sop_df["Reference"] == rid, "Title"].iloc[0]
        methods.append(S.AnalyticalMethod(
            method_id=rid, method_name=amv_names[rid], method_type=METHOD_TYPE.get(rid),
            associated_attributes=[f"attr:{a}" for a in METHOD_ATTRS.get(rid, [])],
            validation_status="validated",
            source_references=[ref(doc, f, sid("sdm"), "Scale-down model strategy", row,
                                   table_title=sop_t.caption, table_id=f"{doc}_tab_sops",
                                   table_header=sops.header)]
            + (size_variant_refs(doc, f, "Method for fragments", None, SIZE_VARIANT_TOKEN[rid],
                                 text) if rid in SIZE_VARIANT_TOKEN else []),
            metadata=meta()))
    claims = P.CFG.raw()["iac"]["viral_claims"]
    vkey = {"lrv_xmulv": "xmulv_lrf", "lrv_mvm": "mvm_lrf"}
    vstep = {"viral_inactivation": "Low-pH viral inactivation", "aex": "Anion exchange",
             "virus_filtration": "Virus filtration"}
    contributions = []
    vcum = P.csv("iac_viral_cumulative.csv")
    for (virus, row), r in zip(vcrow.items(), vcum.itertuples()):
        for sk, col in vstep.items():
            if vkey[r.cqa] not in claims[sk]:
                continue
            contributions.append(ModularContribution(
                contribution_id=f"{doc}-VC{len(contributions) + 1:02d}",
                quantity=f"Viral clearance — {virus}", unit_operation=P.UNIT_OP_TITLES[sk],
                step_value=f"{claims[sk][vkey[r.cqa]]:g}", cumulative_value=f"{r.claimed_sum:.2f}",
                requirement=f"{r.required:g}", unit="log10",
                contributing_steps=[P.UNIT_OP_TITLES[s] for s in vstep
                                    if s != sk and vkey[r.cqa] in claims[s]],
                source_references=[ref(doc, f, sid("viral"), "Viral clearance claims", row,
                                       table_title=vc_t.caption, table_id=f"{doc}_tab_viral",
                                       table_header=vcrow.header)],
                metadata=meta()))
    rels = []
    for plan, row in plrow.items():
        rels.append(DocumentRelationship(
            relationship_id=f"{doc}-R{len(rels) + 1:02d}", kind="references",
            source_document_id=doc, target_document_ref=plan,
            statement=f"{plan} is a Process Characterization Plan under PCMP-001.",
            source_references=[ref(doc, f, sid("register"), "Register of characterization plans",
                                   row, table_title=pl_t.caption, table_header=plrow.header)],
            metadata=meta()))
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=sid("purpose"), process_steps=steps,
                                  sites=_site_entities(doc, f, sid("purpose"))),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("cqa"), quality_attributes=attrs),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("risk"), parameters=params),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("sdm"), equipment=equipment,
                                  analytical_methods=methods),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("viral"),
                                  contributions=contributions),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("register"),
                                  document_relationships=rels),
    ]

    # ---- studies: every study of a schema type, on its chronology row (+ its design row) ---
    chrono = P.csv("study_chronology.csv")
    # the study run after the Version 1.0 reports: a discrepancy from PCP-005, not a deviation
    sdm2_q = (f"One supplementary qualification study of the Protein A scale-down model, "
              f"{ns['post_ids']} ({ns['post_window']}), ran afterwards, while {ns['inv_id']} was "
              f"open.")
    studies, unrendered = [], []
    for _, r in chrono.iterrows():
        stype = STUDY_TYPE.get(r["kind"])
        if stype is None:
            continue
        if not _present(chrow[r["id"]], text):
            unrendered.append(r["id"])
            continue
        k, uo = r["step"], P.CFG.unit_op(r["step"])
        refs = [ref(doc, f, sid("schedule"), "Deliverables and schedule", chrow[r["id"]],
                    table_title=ch_t.caption, table_id=f"{doc}_tab_chrono",
                    table_header=chrow.header)]
        if r["id"] == ns["post_id"]:
            refs.append(ref(doc, f, sid("sdm"), "Scale-down model strategy", sdm2_q))
        kw = {}
        if r["kind"] in ("screening", "rsm"):
            refs.append(ref(doc, f, sid("stats"), "Designs", drow[k], table_title=des_t.caption,
                            table_id=f"{doc}_tab_designs", table_header=drow.header))
            fac = D.screening_factors(k) if r["kind"] == "screening" else D.rsm_factors(k)
            kw = dict(factors=[uo.param(x).name for x in fac],
                      associated_parameters=[f"param:{k}_{x}" for x in fac],
                      n_runs=P.doe_runs(k, r["kind"]),
                      n_center_points=P.doe_centre_points(k, r["kind"]),
                      design_name=("two-level factorial" if r["kind"] == "screening"
                                   else "central composite design"))
        elif r["kind"] == "univariate":
            ps = [p for p in uo.parameters if p.study != "multivariate"]
            kw = dict(factors=[p.name for p in ps],
                      associated_parameters=[f"param:{k}_{p.key}" for p in ps])
        studies.append(S.StudyDesign(
            study_id=f"study:{r['id']}", study_type=stype, unit_operation=P.UNIT_OP_TITLES[k],
            source_references=refs, metadata=meta(), **kw))

    # ---- assertions ------------------------------------------------------------------------
    for k in P.CFG.train_order:
        add("process:amab_ds", "process_has_step", f"step:{k}",
            f"The A-Mab drug substance process has the step {P.UNIT_OP_TITLES[k]}.",
            "Purpose and scope", train[k], train.header, cap["tbl-train"])
    for (k, name), row in prow.items():
        add(f"step:{k}", "step_has_parameter", pid[(k, name)],
            f"{P.UNIT_OP_TITLES[k]} has process parameter {name}.", "Risk-based prioritization",
            row, prow.header, pbs.caption)
    set_by = dict(zip(P.cqa_reg["key"], P.cqa_reg["set_by"]))
    for r in P.cqa_reg.to_dict("records"):
        c = cdf.loc[r["key"]]
        add(f"step:{set_by[r['key']]}", "step_has_quality_attribute", f"attr:{r['key']}",
            f"{r['cqa']} is formed or set at {c['Formed or set at']}.",
            "Critical quality attribute framework", crow[r["key"]], crow.header, cqa_t.caption)
        add(f"attr:{r['key']}", "attribute_has_acceptance_criterion", f"lit:{r['key']}_ds",
            f"{r['cqa']} drug substance acceptance criterion: {c['Acceptance']}.",
            "Critical quality attribute framework", crow[r["key"]], crow.header, cqa_t.caption)
    for (sk, cqa), row in iacrow.items():
        r = iac[(iac["step_key"] == sk) & (iac["cqa"] == cqa)].iloc[0]
        add(f"attr:{cqa}", "attribute_has_acceptance_criterion", f"lit:{sk}_{cqa}_iac",
            f"The {T.STEP_NAME[sk]} output is judged for {T.ATTR_NAME[cqa]} against the "
            f"intermediate acceptance criterion {T.crit(r['iac_low'], r['iac_high'], r['spec_type'])} "
            f"({r['basis']}).", "Intermediate acceptance criteria", row, iacrow.header,
            iac_t.caption)
    step_of_study = dict(zip(chrono["id"], chrono["step"]))
    for e in eq_ids:
        i = first_row[e]
        k = step_of_study[eqdf.loc[i, "Study"]]
        add(f"step:{k}", "step_uses_equipment", f"equip:{e}",
            f"Study {eqdf.loc[i, 'Study']} of {P.UNIT_OP_TITLES[k]} used {e} "
            f"({eqdf.loc[i, 'Description']}).", "Scale-down model strategy", eqrow[i],
            eqrow.header, eq_t.caption)

    # ---- the one superseded criterion the master plan states, and the report sections -----
    r1 = ns["r1_cex_agg"]
    superseded = [S.AcceptanceCriterionRecord(
        step="cex", attribute="aggregates_hmw", low=None, high=float(r1["high"]),
        unit=P.CFG.cqa("aggregates_hmw")["unit"], basis=str(r1["rule"]), revision=P.REV1["rev"],
        status="superseded",
        source=ref(doc, f, f"{doc}_crit", "Changes in this revision",
                   f"In Version 1.0 the cation exchange pool was judged against an aggregate limit "
                   f"of {ns['r1_cex_agg_hi']} % HMW."))]
    chg = "Changes in this revision"
    verif = "Verification of the platform worst cases"
    st("PCMP-001 governs the Stage 1 process characterization of the A-Mab drug substance "
       "process, under the Process Transfer Plan PTP-001.", "Purpose and scope",
       "This plan governs the Stage 1 process characterization of the A-Mab drug substance process.")
    st("Each step plan, PCP-003 to PCP-010, applies the master plan to one step and should state "
       "any departure from it with the reason.", "Purpose and scope",
       "Each Process Characterization Plan (PCP-003 to PCP-010) applies this framework to one step.")
    st("Version 1.0 of the master plan defined no criteria for step outputs; Version 2.0 is "
       "issued under INV-001.", chg, "Version 1.0 of this plan defined no criteria for step outputs.")
    st("Version 2.0 defines intermediate acceptance criteria for the step outputs by a rule that "
       "uses no data from the studies it judges.", chg,
       "The rule that derives them uses no data from the studies it judges.")
    st("The intermediate acceptance criteria replace the Version 1.0 step criteria, the corrective "
       "action for INV-001 findings 1 and 2.", chg,
       "They replace the Version 1.0 step criteria described above (INV-001 findings 1 and 2).")
    st("Version 2.0 qualifies each scale-down model by its offset from manufacturing scale, not by "
       "a test of equivalence, and states every judgement against a criterion at manufacturing "
       "scale.", chg,
       "It qualifies each scale-down model by its offset from manufacturing scale, not by a test "
       "of equivalence, and states every judgement against a criterion at manufacturing scale")
    st(f"Version 1.0 judged the cation exchange pool against an aggregate limit of "
       f"{ns['r1_cex_agg_hi']} % HMW; Version 2.0 credits no later step with aggregate removal, so "
       f"the pool carries the drug substance criterion, {ns['cex_agg_iac']} %.", chg,
       "The cation exchange pool therefore carries the drug substance criterion itself")
    st("A scale-down model is qualified for each output by the offset between the scales, and "
       "every judgement of a scale-down result against a criterion first subtracts that offset.",
       "Scale-down model qualification",
       "It is qualified by the offset between the scales, not by a test of equivalence.")
    st(f"{ns['post_ids']} ran after the Version 1.0 reports were approved, to narrow the confidence "
       f"interval of the offset for host cell protein in the Protein A pool; PCR-005 records it as "
       f"discrepancy {ns['pd_id']} from {ns['pd_plan']}, not as a deviation.",
       "Scale-down model strategy",
       f"They are work that the Protein A plan {ns['pd_plan']} did not foresee, and the Protein A "
       f"report {ns['pd_report']} records them as discrepancy {ns['pd_id']} from that plan.")
    st(f"Version 2.0 sets nrCE-SDS ({ns['cesds_amv']}) as the method for fragments in every study "
       f"at every step from {ns['amd_date']} ({ns['amd_id']}).", "Method for fragments",
       f"From {ns['amd_date']}, fragments are measured by nrCE-SDS ({ns['cesds_amv']}, under "
       f"{ns['cesds_sop']}) in every study at every step.")
    st("The screening model identifies effects, and the response-surface model is the predictive "
       "model from which every prediction, PAR and design space in the package comes.",
       "Models, and what each model is for",
       "Every prediction, every PAR and every design space in the package comes from it.")
    st("No report should claim prediction from a screening model.",
       "Models, and what each model is for",
       "No report should claim prediction from a screening model.")
    st("For a quality attribute the NOR-propagated analysis compares the 95 % prediction interval "
       "of a single batch with the criterion.", "Proven acceptable ranges",
       "For a quality attribute it compares the 95 % prediction interval of a single batch, "
       "because a single batch is what must meet the criterion.")
    st("For viral clearance the NOR-propagated analysis compares the worst case within the NOR: "
       "the lowest mean predicted log reduction over every combination of NOR low, set-point and "
       "NOR high of the other factors must meet the claim of the step.",
       "Proven acceptable ranges", "For viral clearance it compares the worst case within the NOR.")
    st("The NOR-propagated PAR is the one that supports a claim.", "Proven acceptable ranges",
       "The NOR-propagated PAR is the one that supports a claim.")
    st("A PAR that reaches the edge of the characterized range is reported as reaching it, and no "
       "claim is made beyond it.", "Proven acceptable ranges",
       "A PAR that reaches the edge of the characterized range is reported as reaching it, and no "
       "claim is made beyond it.")
    st("Each drug substance criterion is carried backward through the train using the platform "
       "worst case of each downstream step, with no margin applied.",
       "Intermediate acceptance criteria",
       "Each drug substance criterion is carried backward through the train, step by step, using "
       "the worst case that each downstream step showed on the platform.")
    st(f"For host cell protein the Protein A pool criterion is {ns['pa_hcp_iac']} ng/mg, widened "
       f"from {ns['pa_hcp_apriori']} ng/mg a priori by the cation exchange bound, and the cation "
       f"exchange pool criterion stays at {ns['cex_hcp_iac']} ng/mg.",
       "Intermediate acceptance criteria",
       f"The Protein A pool criterion is therefore {ns['pa_hcp_iac']} ng/mg, and the cation "
       f"exchange pool criterion stays at {ns['cex_hcp_iac']} ng/mg.")
    st(f"Of the {ns['n_iac']} intermediate acceptance criteria, {ns['n_apriori']} are in force at "
       f"their a priori value and verification changed {ns['n_moved']}.",
       "Intermediate acceptance criteria",
       f"{ns['n_apriori']} are in force at their a priori value and verification changed "
       f"{ns['n_moved']}.")
    st("Verification may change a criterion in either direction: an A-Mab worst case worse than "
       "the platform tightens it, and a better 95 % confidence bound from an adequate model "
       "widens it.", verif, "Verification may change a criterion in either direction, by the "
                            "following rule.")
    st("In both directions the confidence bound, on its unfavourable side, replaces the platform "
       "value, and the point prediction never does.", verif,
       "In both directions the bound, on its unfavourable side, replaces the platform value, and "
       "the point prediction never does.")
    st(f"Of the {ns['n_verif']} platform worst cases the criteria assume, {ns['n_verif_testable']} "
       f"can be checked against the response-surface designs of {ns['vtest_steps']}.", verif,
       f"Of these, {ns['n_verif_testable']} are responses of the response-surface designs of "
       f"{ns['vtest_steps']}, and they can be checked.")
    st(f"The 95 % confidence bound replaced the platform value for {ns['vwid_list']}.", verif,
       f"The 95 % confidence bound was better than the platform worst case for {ns['vwid_list']}, "
       f"and these bounds replaced the platform values.")
    st(f"For {ns['vinad_list']} the bound was also better, but the model does not meet the "
       f"adequacy criteria, so the platform values stand.", verif,
       f"For {ns['vinad_list']} the bound was also better, but the model does not meet the "
       f"adequacy criteria, so the platform values stand.")
    st("The aggregate clearance of cation exchange within its NOR is lower than the platform worst "
       "case, which tightened the aggregate criteria upstream of cation exchange.", verif,
       "Verification found that the aggregate clearance of cation exchange within its NOR is lower "
       "than the platform worst case.")
    st("The viral clearance claims meet the cumulative requirements with little room, so a step "
       "that falls short of its claim cannot be made up by another step.", "Viral clearance claims",
       "A step that falls short of its claim therefore cannot be made up by the surplus of another "
       "step.")
    st(f"A Cpk of at least {ns['cpk_target']} is expected of a CQA in routine manufacture, and a "
       f"CQA below {ns['cpk_min']} needs an action in the control strategy.",
       "Capability and the probability of an out-of-specification drug substance",
       f"A Cpk of at least {ns['cpk_target']} is expected of a CQA in routine manufacture.")
    st("Acidic variants have a two-sided criterion, and their capability is assessed against "
       "both ends.", "Capability, and the integrated model",
       "and their capability is assessed against both ends.")
    st("In Version 1.0 each step plan was approved before the first characterization run of its "
       "step, and each report after the data of all its studies were complete; PCMR-001 is "
       "written last.", "Deliverables and schedule",
       "In Version 1.0 each step plan was approved before the first characterization run of its "
       "step, and each report after the data of all its studies were complete.")
    # the NORs a Version 2.0 report narrowed: the table prints the NOR in force and footnotes it
    notes = {n.split(" ", 1)[0]: n for n in pbs.notes_text().split(CELL_SEP)}
    n_narrowed = 0
    for (k, name), row in prow.items():
        # the marker is its own run, so it reads " c1)" after the NOR; a row continuing the
        # merged step cell starts with "| ", so the NOR is not at a fixed cell index
        m = re.search(r"\s(c\d+\))(?=\s|$)", row)
        if not m:
            continue
        p = P.CFG.unit_op(k).param(next(q.key for q in P.CFG.unit_op(k).parameters
                                        if q.name == name))
        n_narrowed += 1
        st(f"At Version 2.0, PCR-{P.CFG.unit_op(k).step:03d} narrowed the NOR of "
           f"{name[0].lower() + name[1:]} at {T.STEP_NAME[k]} from "
           f"{p.nor_characterized[0]:g}–{p.nor_characterized[1]:g} to "
           f"{p.nor[0]:g}–{p.nor[1]:g} {p.unit}; the table gives the NOR in force.",
           "Risk-based prioritization", notes[m.group(1)], table_title=pbs.caption)
    if n_narrowed != sum(list(p.nor) != list(p.nor_characterized)
                         for k in P.CFG.train_order for p in P.CFG.unit_op(k).parameters):
        raise ValueError(f"{pbs.label}: a narrowed NOR has no footnote marker")

    concepts = _corpus_step_concepts()
    concepts += [Concept(concept_id=pid[k], concept_type="PROCESS_PARAMETER", canonical_name=k[1],
                         aliases=[f"{k[1]} ({T.STEP_NAME[k[0]]})"], review_status="human_verified")
                 for k in prow]
    concepts += _method_concepts(list(amv_names), amv_names)
    concepts += [Concept(concept_id=f"equip:{e}", concept_type="EQUIPMENT", canonical_name=e,
                         review_status="human_verified") for e in eq_ids]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], **rev2_layer(doc, f),
        schema_extensions_used=COMMON_EXT + REV2_EXT,
        out_of_schema_notes=[
            "The master plan spans the whole train: entities are the Step 3-10 process steps, the "
            "CQA register, every parameter of the train with the class its report assigned and "
            "the NOR in force, the instrumented scale-down systems and the method validations of "
            "the package. Each NOR a Version 2.0 report narrowed is a report statement anchored "
            "on its footnote of the parameter table.",
            "acceptance_criteria holds one in-force Version 2.0 record per row of the intermediate "
            "acceptance criteria table (the plan prints no criteria-change table), plus the one "
            "Version 1.0 limit the plan states, the cation exchange aggregate limit, as superseded. "
            "The in-force records that verification moved carry a value with an A-Mab confidence "
            "bound in it; their a priori values are stated in prose and were never in force, so "
            "they have no record.",
            "Studies are every chronology row of a schema study type. Hold studies, the method "
            "comparability study S-CEX-FRC, the nrCE-SDS retests and the invalidated first anion "
            "exchange execution S-AEX-SUP have no StudyDesign.study_type and are left out. The "
            "supplementary qualification study S-PA-SDM2 is a discrepancy from PCP-005 that "
            "PCR-005 records, not a deviation, and the schema has no record for a plan "
            "discrepancy; it is a report statement.",
            "Each instrumented system is anchored on the first row of its group in the calibration "
            "table, which names it; the rows below continue its merged cells.",
            "The campaign thresholds for model adequacy and capability, the decision statistics, "
            "the verification rule and the classification rules have no schema field; they are "
            "report_sections statements.",
            "The size-variant methods table anchors the SEC (AMV-3011) and nrCE-SDS (AMV-3020) "
            "method records on the rows that name each method and occur once in the document.",
            "No rhetorical_spans: the Version 1.0 annex carried none for the master plan, and none "
            "were curated for Version 2.0. weak_claims is empty.",
        ] + _unrendered_note(unrendered),
        inventory=rev2_inventory(doc, f, "process_characterization_master_plan",
                                 "A-Mab drug substance",
                                 ["process characterization", "master plan", "CQA framework",
                                  "intermediate acceptance criteria", "scale-down model",
                                  "statistical approach", "viral clearance"]),
        entities=entities, studies=studies,
        report_sections=[ReportSection(section_id=f"{doc}-summary", title="Master plan summary",
                                       statements=ST)],
        assertions=AssertionStore(run_id=f"gt-{doc}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id="gt-pcmp", concepts=concepts),
        acceptance_criteria=superseded + in_force)


# --------------------------------------------------------------------------- #
# INV-001 — Investigation Report, Version 1.0 (new in the Version 2.0 package). #
# --------------------------------------------------------------------------- #
INV_FILE = "INV-001_investigation.docx"


def build_investigation():
    """INV-001: the investigation that reissued the package at Version 2.0."""
    import tables as T
    from annex_contract.assertions import AssertionStore
    from annex_contract.concepts import Concept, ConceptStore
    from annex_contract.discourse import DocumentRelationship, ExplicitNonClaim
    from annex_contract.results import Deviation, ModularContribution, ProcessCapability
    from annex_contract.summaries import ReportSection
    doc, f = P.INV["id"], INV_FILE
    ns, tabs = qmd_namespace("INV-001_investigation.qmd")
    A, add, ST, st = _adders(doc, f)
    cap = {k: v[3] for k, v in tabs.items()}
    by_label = _attr_key_by_label()

    def sid(s):
        return f"{doc}_sec_{s}"
    md = ns["margin_df"]
    mrow = captured_rows(tabs["tbl-margins"], zip(md["step"], md["cqa"]))
    capdf = tabs["tbl-cap-limits"][1]
    crow = captured_rows(tabs["tbl-cap-limits"], [by_label[a] for a in capdf["Attribute"]])
    pldf = tabs["tbl-plan-dates"][1]
    plrow = captured_rows(tabs["tbl-plan-dates"], pldf["Plan"])
    eq_t = T.calibration_windows()
    eqdf = T.calibration_windows_data()
    eqrow = ctable_rows(eq_t)
    cap["tbl-calibration"] = eq_t.caption
    psdf = tabs["tbl-par-change"][1]
    psrow = captured_rows(tabs["tbl-par-change"], psdf["Report"])
    rd = ns["res_df"]
    rrow = captured_rows(tabs["tbl-results"], zip(rd["step"], rd["cqa"]))
    rsdf = tabs["tbl-results"][1]
    vdf = tabs["tbl-viral"][1]
    vrow = captured_rows(tabs["tbl-viral"])
    cadf = tabs["tbl-capa"][1]
    carow = captured_rows(tabs["tbl-capa"], cadf["No."])
    docs = md_string_rows(P.corpus_docs_md(doc))
    f1, f2 = ns["f1"], ns["f2"]

    # ---- entities --------------------------------------------------------------------------
    step_of_study = dict(zip(ns["chron"]["id"], ns["chron"]["step"]))
    eq_ids = list(dict.fromkeys(eqdf["Equipment"]))
    equipment = [S.Equipment(
        equipment_id=f"equip:{e}", equipment_name=e, site_name=P.SENDING_SITE,
        source_references=[ref(doc, f, sid("f5"), "F5. Approval and execution dates missing from "
                               "the records", eqrow[i], table_title=cap["tbl-calibration"],
                               table_id=f"{doc}_tab_calibration", table_header=eqrow.header)
                           for i in eqdf.index[eqdf["Equipment"] == e][:1]],
        metadata=meta()) for e in eq_ids]
    acid = ns["acid"]
    capdesc = "F4. Acidic variants assessed against one end of a two-sided range"
    capab = [
        ProcessCapability(
            capability_id=f"{doc}-CAP01", quality_attribute="attr:acidic_variants",
            index_name="Cpk (both ends)", index_value=round(float(ns["acid_cpk"]), 2),
            specification_side="two_sided",
            acceptance_range=f"{ns['ds_acid_lo']:g}–{ns['ds_acid_hi']:g} %",
            mean=f1(ns["acid_mean"]), standard_deviation=f2(ns["acid_sd"]), unit="%",
            basis="simulated", n_batches=int(acid["n"]), claimed_process_minimum=True,
            source_references=[
                ref(doc, f, sid("f4"), capdesc,
                    f"Computed against both ends, the index is {f2(ns['acid_cpk'])}, and the lower "
                    f"end governs it."),
                ref(doc, f, sid("summary"), "Summary",
                    f"the lowest capability index of the drug substance is that of acidic variants, "
                    f"at {f2(ns['v2_min_cpk'])}, against its lower limit")],
            metadata=meta()),
        ProcessCapability(
            capability_id=f"{doc}-CAP02", quality_attribute="attr:acidic_variants",
            index_name="Cpk as printed in Version 1.0 (upper end only)",
            index_value=round(float(ns["acid_cpu"]), 1), specification_side="upper",
            acceptance_range=f"{ns['ds_acid_lo']:g}–{ns['ds_acid_hi']:g} %", unit="%",
            basis="simulated", n_batches=int(acid["n"]),
            source_references=[ref(doc, f, sid("f4"), capdesc,
                                   f"The capability index beside it was computed against the upper "
                                   f"end alone and printed as {f1(ns['acid_cpu'])}.")],
            metadata=meta()),
        ProcessCapability(
            capability_id=f"{doc}-CAP03", quality_attribute=f"attr:{ns['v1_min_key']}",
            index_name="Cpk (lowest of the drug substance as reported in PCMR-001 Version 1.0)",
            index_value=round(float(ns["v1_min_cpk"]), 2), unit="log10", basis="simulated",
            n_batches=int(acid["n"]), claimed_process_minimum=True,
            source_references=[ref(doc, f, sid("f4"), capdesc,
                                   f"PCMR-001 reported the lowest capability index of the drug "
                                   f"substance as {f2(ns['v1_min_cpk'])}, for MVM clearance.")],
            metadata=meta()),
    ]
    vrows = ns["_vv"]
    vcum = P.csv("iac_viral_cumulative.csv").set_index("cqa")
    contributions = []
    for (i, row), v in zip(vrow.items(), vrows):
        cqa = "lrv_xmulv" if v[1] == "XMuLV" else "lrv_mvm"
        contributions.append(ModularContribution(
            contribution_id=f"{doc}-VC{i + 1:02d}", quantity=f"Viral clearance — {v[1]}",
            unit_operation=v[0], step_value=v[3], requirement=v[2],
            cumulative_value=f"{vcum.loc[cqa, 'claimed_sum']:.2f}", unit="log10",
            source_references=[ref(doc, f, sid("impact"), "Impact by document", row,
                                   table_title=cap["tbl-viral"], table_id=f"{doc}_tab_viral",
                                   table_header=vrow.header)],
            metadata=meta()))
    from check_grounding import normalize as _normalize
    sdm2_q = (f"For this reason, {ns['n_sdm_sup']} supplementary set-point runs (study S-PA-SDM2) "
              f"were made from {ns['sdm2_start']} to {ns['sdm2_end']}, and the margin was not "
              f"changed.")
    text = _document_text(f)
    sv_t = T.methods_by_study()
    sv_rows = ctable_rows(sv_t)
    sv_methods = [S.AnalyticalMethod(
        method_id=tok, method_name=name, method_type=mtype,
        associated_attributes=[f"attr:{a}" for a in attrs_], validation_status="validated",
        source_references=size_variant_refs(doc, f, "F6. Fragments by SEC in the capture matrices",
                                             None, tok, text)
        + [ref(doc, f, sid("abbr"), "Abbreviations", abbr)],
        metadata=meta()) for tok, name, mtype, attrs_, abbr in [
        ("SEC", "size-exclusion chromatography", "chromatography",
         ["aggregates_hmw", "fragments_lmw"], CELL_SEP.join(["SEC", "size-exclusion chromatography"])),
        ("nrCE-SDS", "non-reduced capillary electrophoresis with sodium dodecyl sulfate",
         "capillary electrophoresis", ["fragments_lmw"],
         CELL_SEP.join(["nrCE-SDS", "non-reduced capillary electrophoresis with sodium dodecyl sulfate"]))]]
    dev = [
        Deviation(
            deviation_id=doc,
            summary="The acceptance criteria against which each step was judged in the proven "
                    "acceptable range analysis were not in any protocol approved before the studies "
                    "ran; they were set at analysis time, after the data were known.",
            detected_during="QA review of PCMR-001 Version 1.0 for BLA readiness",
            disposition=f"Classified {P.INV['classification']}; closed with the corrective and "
                        f"preventive actions open and tracked",
            impact_statement="No GMP batch was dispositioned on these documents; no product impact.",
            no_impact_on_conclusions=False,
            source_references=[
                ref(doc, f, sid("summary"), "Summary",
                    "They had been set at analysis time, after the data were known."),
                ref(doc, f, sid("summary"), "Summary",
                    f"The investigation was classified as {P.INV['classification']}.")],
            metadata=meta()),
        Deviation(
            deviation_id="DEV-008-01", unit_operation=P.UNIT_OP_TITLES["aex"],
            summary="The first execution of the anion exchange design was invalidated and the "
                    "design was re-executed; the invalidated execution had measured fragments by "
                    "SEC.", disposition="re-executed",
            source_references=[ref(doc, f, sid("f6"), "F6. Fragments by SEC in the capture matrices",
                                   "Its invalidated first execution had used SEC.")],
            metadata=meta()),
        Deviation(
            deviation_id="DEV-005-03", unit_operation=P.UNIT_OP_TITLES["protein_a"],
            summary=f"The {ns['n_sdm_planned']} planned set-point runs of the Protein A scale-down "
                    f"qualification could never demonstrate equivalence against the margin of "
                    f"PCP-005, because the confidence interval alone was wider than the margin.",
            detected_during="Version 2.0 re-analysis of the Protein A scale-down qualification",
            disposition=f"{ns['n_sdm_sup']} supplementary set-point runs made (study S-PA-SDM2); "
                        f"margin not changed",
            impact_statement="The runs add scale-down data only and change no characterization "
                             "data that Version 1.0 analysed.",
            no_impact_on_conclusions=True,
            source_references=[
                ref(doc, f, sid("scope"), "Scope",
                    "because the confidence interval alone was wider than the margin (DEV-005-03)"),
                ref(doc, f, sid("scope"), "Scope", sdm2_q)],
            metadata=meta()),
    ]
    nc = [
        ExplicitNonClaim(
            non_claim_id=f"{doc}-NC01", subject="computation of a proven acceptable range",
            statement="How the other parameters are held or varied while one parameter is scanned "
                      "is not reviewed by the investigation.",
            source_references=[ref(doc, f, sid("scope"), "Scope",
                                   "The computation of a proven acceptable range itself")],
            metadata=meta()),
        ExplicitNonClaim(
            non_claim_id=f"{doc}-NC02", subject="the experiments",
            statement="The experiments are not reviewed; the re-analysis uses the same experimental "
                      "data as Version 1.0 and no experiment was run for it.",
            source_references=[ref(doc, f, sid("scope"), "Scope",
                                   "The experiments are not reviewed either.")],
            metadata=meta()),
        ExplicitNonClaim(
            non_claim_id=f"{doc}-NC03", subject="study deviation dispositions",
            statement="The study deviations recorded in the step reports keep the disposition those "
                      "reports give them.", handled_elsewhere="the step reports PCR-003 to PCR-010",
            source_references=[ref(doc, f, sid("scope"), "Scope",
                                   "the study deviations recorded in the step reports keep the "
                                   "disposition those reports give them")],
            metadata=meta()),
        ExplicitNonClaim(
            non_claim_id=f"{doc}-NC04", subject="product impact",
            statement="There is no product impact: no GMP batch was manufactured or dispositioned "
                      "on these documents and Version 1.0 was not used in a submission.",
            source_references=[ref(doc, f, sid("product"), "Product impact",
                                   "No GMP batch of A-Mab was manufactured or dispositioned on the "
                                   "basis of these documents")],
            metadata=meta()),
        ExplicitNonClaim(
            non_claim_id=f"{doc}-NC05", subject="preventive action for contributing causes 3 and 4",
            statement="No preventive action adds a second review of the specification type used in "
                      "a capability calculation, and none creates the procedural step for method "
                      "decisions.",
            source_references=[ref(doc, f, sid("capa"), "Corrective and preventive actions",
                                   "Two causes have no preventive action.")],
            metadata=meta()),
    ]
    rels = []
    for target, row in docs.items():
        rels.append(DocumentRelationship(
            relationship_id=f"{doc}-R{len(rels) + 1:02d}", kind="references",
            source_document_id=doc, target_document_ref=target,
            statement=f"{target} is in the scope of the investigation, at Version 1.0.",
            source_references=[ref(doc, f, sid("scope"), "Scope", row,
                                   table_title="Documents in the scope of the investigation, all "
                                               "at Version 1.0 when it was opened.",
                                   table_header=docs.header)],
            metadata=meta()))
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=sid("summary"), deviations=[dev[0]]),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("scope"),
                                  document_relationships=rels, non_claims=nc[:3]),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("f4"), capabilities=capab),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("f5"), equipment=equipment),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("f6"), deviations=[dev[1]],
                                  analytical_methods=sv_methods),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("scope_sdm2"),
                                  deviations=[dev[2]]),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("impact"),
                                  contributions=contributions, non_claims=[nc[3]]),
        S.SectionEntityExtraction(document_id=doc, section_id=sid("capa"), non_claims=[nc[4]]),
    ]

    # ---- assertions ------------------------------------------------------------------------
    for (sk, cqa), row in mrow.items():
        r = md[(md["step"] == sk) & (md["cqa"] == cqa)].iloc[0]
        add(f"attr:{cqa}", "attribute_has_acceptance_criterion", f"lit:{sk}_{cqa}_v1",
            f"Version 1.0 judged the {T.STEP_NAME[sk]} output for {T.ATTR_NAME[cqa]} against "
            f"≤ {T.num(r['crit'])}, the nominal back-calculation divided by a safety factor of "
            f"{f1(r['margin'])} (superseded).", "F2. Safety factors chosen so that each step passed "
            "at its set-point", row, mrow.header, cap["tbl-margins"])
    for cqa, row in crow.items():
        c = capdf[capdf["Attribute"] == T.ATTR_NAME[cqa]].iloc[0]
        add(f"attr:{cqa}", "attribute_has_acceptance_criterion", f"lit:bioreactor_{cqa}_v1",
            f"Version 1.0 judged the production bioreactor output for {T.ATTR_NAME[cqa]} against "
            f"an upper alert limit of {c['Version 1.0 upper criterion']}, the capability mean plus "
            f"{ns['sigma']:g} SD (superseded).",
            "F3. Capability limits judged against the data they came from", row, crow.header,
            cap["tbl-cap-limits"])
    for (sk, cqa), row in rrow.items():
        r = rsdf[(rsdf["Step"] == T.STEP_NAME[sk]) & (rsdf["Attribute"] == T.ATTR_NAME[cqa])].iloc[0]
        add(f"attr:{cqa}", "attribute_has_acceptance_criterion", f"lit:{sk}_{cqa}_iac",
            f"Under Version 2.0 the {T.STEP_NAME[sk]} output for {T.ATTR_NAME[cqa]} is judged "
            f"against {r['Version 2.0 criterion']}; over the NOR the model predicts "
            f"{r['Range over the NOR']} ({r['Met across the NOR'].lower()}).",
            "Impact by document", row, rrow.header, cap["tbl-results"])
    for e in eq_ids:
        i = list(eqdf.index[eqdf["Equipment"] == e])[0]
        k = step_of_study[eqdf.loc[i, "Study"]]
        add(f"step:{k}", "step_uses_equipment", f"equip:{e}",
            f"Study {eqdf.loc[i, 'Study']} of {P.UNIT_OP_TITLES[k]} used {e}.",
            "F5. Approval and execution dates missing from the records", eqrow[i], eqrow.header,
            cap["tbl-calibration"])
    agg_row = next(r for r in sv_rows.values()
                   if r.split(CELL_SEP)[1] == "Aggregates, HMW" and "SEC" in r.split(CELL_SEP)[2:]
                   and text.count(_normalize(r)) == 1)
    add("attr:aggregates_hmw", "attribute_measured_by_method", "method:SEC",
        "Aggregate (HMW) is measured by SEC.", "F6. Fragments by SEC in the capture matrices",
        agg_row, sv_rows.header, sv_t.caption)
    add("attr:fragments_lmw", "attribute_measured_by_method", "method:nrCE-SDS",
        f"From {P.AMD['date']} fragments are measured by nrCE-SDS in every study at every step.",
        "F6. Fragments by SEC in the capture matrices",
        "From that date, fragments were measured by nrCE-SDS in every study, at every step, so "
        "that one method spans the train.")

    # ---- report sections: summary, findings, root cause, impact, actions, closure ----------
    sec_sum, sec_inv = "Summary", "Investigation"
    st(f"QA opened {doc} on {P.INV['opened']} during the review of PCMR-001 Version 1.0 for BLA "
       f"readiness.", sec_sum,
       f"On {P.INV['opened']}, Quality Assurance opened {doc} during the review of PCMR-001 "
       f"Version 1.0 for BLA readiness.")
    st("The root cause is that PCMP-001 Version 1.0 required a criterion for each step but gave no "
       "rule for deriving one, so the criteria were derived during the analysis.", "Root cause",
       "The root cause is that PCMP-001 Version 1.0 required a criterion for each step but gave "
       "no rule for deriving one (F1).")
    st("F1: the step criteria were defined after the data were seen and outside the approved "
       "protocols.", "F1. Criteria defined after the data were seen",
       "The step criteria were defined after the data were seen and outside the approved protocols.")
    st(f"F2: the R1 safety factors ranged from {f1(ns['m_lo'])} to {f1(ns['m_hi'])}, with no "
       f"recorded reason, and were chosen with the result in view.",
       "F2. Safety factors chosen so that each step passed at its set-point",
       "The factors were therefore chosen with the result in view.")
    st("F3: the bioreactor limits were alert limits at the capability mean plus a multiple of the "
       "SD, computed from the capability data they were then used to judge.",
       "F3. Capability limits judged against the data they came from",
       "A limit of this kind is an alert limit for trending.")
    st("F4: acidic variants were assessed for capability against one end of a two-sided range.",
       capdesc, "Computed against both ends, the index is")
    st("F5: the Version 1.0 title blocks misstated the plan approval dates and the reports gave "
       "no execution dates; every plan was approved before its first study and no study ran on "
       "equipment out of calibration.", "F5. Approval and execution dates missing from the records",
       "No plan was approved after its studies, and none of these studies was run on equipment "
       "out of calibration.")
    st("F6: SEC fragment results from the capture matrices are biased high by an amount that "
       "matters for a fragment criterion, and the method decision never reached the documents.",
       "F6. Fragments by SEC in the capture matrices",
       "SEC fragment results from the capture matrices are therefore biased high by an amount "
       "that matters for a fragment criterion.")
    st("Every Version 1.0 criterion depends on data from the studies it was used to judge.",
       "The Version 1.0 criteria",
       "Every Version 1.0 criterion therefore depends on data from the studies it was used to judge.")
    st("Applying the Version 2.0 criteria to studies already executed is acceptable because their "
       "derivation uses no data from those studies.", "The Version 2.0 criteria",
       "Applying these criteria to studies already executed is acceptable because their derivation "
       "uses no data from those studies.")
    st(f"Of the {ns['n_ver']} platform worst cases that could be tested, {ns['n_ver_met']} were "
       f"confirmed; aggregate at cation exchange was not, and {ns['n_tight']} aggregate criteria "
       f"upstream of it were tightened.", "Verification of the platform worst cases",
       "One assumption was not confirmed.")
    for rep, row in psrow.items():
        r = psdf[psdf["Report"] == rep].iloc[0]
        st(f"In {rep}, of the {r['Entries in Version 1.0']} NOR-propagated proven acceptable ranges "
           f"of Version 1.0, {r['Unchanged']} are unchanged, {r['Wider']} wider and "
           f"{r['Narrower']} narrower in the re-analysis, and {r['New in Version 2.0']} are new.",
           "Impact by document", row, psrow.header, cap["tbl-par-change"])
    st("Where a proven acceptable range changed, it widened far more often than it narrowed.",
       "Impact by document",
       "Where a range changed, it widened far more often than it narrowed.")
    st("There is no product impact.", "Product impact", "There is no product impact.")
    for no, row in carow.items():
        r = cadf[cadf["No."] == no].iloc[0]
        st(f"{no}: {r['Action']} (owner {r['Owner function']}, due {r['Due']}, {r['Status']}).",
           "Corrective and preventive actions", row, carow.header, cap["tbl-capa"])
    for plan, row in plrow.items():
        r = pldf[pldf["Plan"] == plan].iloc[0]
        st(f"{plan} was approved on {r['Approved']}, before its first study started on "
           f"{r['First study started']}; its Version 1.0 title block printed "
           f"{r['Date in Version 1.0 title block']}.",
           "F5. Approval and execution dates missing from the records", row, plrow.header,
           cap["tbl-plan-dates"])
    st("The corrective actions are verified effective when QA repeats the review that triggered "
       "the investigation on PCMR-001 Version 2.0.", "Effectiveness check",
       "That review checks three things.")
    st(f"{doc} was closed on {P.INV['closed']} with its remaining actions open and tracked to "
       f"completion.", "Conclusion and closure",
       f"{doc} was closed on {P.INV['closed']}, with its remaining actions open and tracked to "
       f"completion under the effectiveness check in §8.")

    keys = list(dict.fromkeys(list(rd["cqa"]) + list(md["cqa"])))
    concepts = [Concept(concept_id="process:amab_ds", concept_type="PROCESS",
                        canonical_name="A-Mab drug-substance process", review_status="human_verified")]
    concepts += [Concept(concept_id=f"step:{k}", concept_type="PROCESS_STEP",
                         canonical_name=P.UNIT_OP_TITLES[k], aliases=[T.STEP_NAME[k]],
                         review_status="human_verified") for k in P.CFG.train_order]
    concepts += _attr_concepts(keys)
    concepts += [Concept(concept_id=f"equip:{e}", concept_type="EQUIPMENT", canonical_name=e,
                         review_status="human_verified") for e in eq_ids]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], **rev2_layer(doc, f),
        schema_extensions_used=COMMON_EXT + REV2_EXT + [
            "DocumentInventoryItem.predicted_document_type: investigation_report added"],
        out_of_schema_notes=[
            "The six findings, the root cause, the contributing causes and the effectiveness check "
            "have no schema model; they are report_sections statements. Each corrective and "
            "preventive action and each plan approval date is a statement anchored on its own row.",
            "acceptance_criteria holds the criteria-change table of §3.3: every Version 1.0 step "
            "criterion as superseded and every Version 2.0 criterion as in force. The Version 1.0 "
            "rule (R1 to R4) and, for R1, its safety factor are in the record basis or the "
            "assertions anchored on the safety-factor table.",
            "The capability records are simulated values the investigation reports: the Version 2.0 "
            "two-sided index for acidic variants, and two Version 1.0 values it corrects (the "
            "one-sided acidic variant index and the MVM minimum PCMR-001 Version 1.0 reported).",
            "The S-CEX-FRC method comparability replicates and the worst-case verification table "
            "are not represented row by row; the verification is a statement. The size-variant "
            "methods table anchors the SEC and nrCE-SDS method records on the rows that name each "
            "method and occur once in the document.",
            "The only study of a schema type is S-PA-SDM2, the supplementary qualification of "
            "DEV-005-03 that ran during the investigation. No parameters and no CQA register "
            "of its own. No rhetorical_spans (none were curated). weak_claims is empty.",
        ],
        inventory=rev2_inventory(doc, f, "investigation_report", "A-Mab drug substance",
                                 ["investigation", "acceptance criteria", "proven acceptable range",
                                  "root cause", "CAPA", "fragments method", "capability"]),
        entities=entities,
        studies=[S.StudyDesign(
            study_id="study:S-PA-SDM2", study_type="scale_down_qualification",
            design_name=f"{ns['n_sdm_sup']} supplementary set-point runs",
            unit_operation=P.UNIT_OP_TITLES["protein_a"],
            source_references=[ref(doc, f, sid("scope"), "Scope", sdm2_q)], metadata=meta())],
        report_sections=[ReportSection(section_id=f"{doc}-summary", title="Investigation summary",
                                       statements=ST)],
        assertions=AssertionStore(run_id=f"gt-{doc}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{doc}", concepts=concepts),
        acceptance_criteria=acceptance_criteria_layer(doc, f, "The Version 1.0 criteria",
                                                      T.criteria_change()))


#: (document id, builder) for the whole corpus, in build order.
BUILDERS = [
    ("PCP-003", lambda: build_plan()), ("PCR-003", lambda: build_report()),
    ("PCP-004", lambda: build_plan_harvest()), ("PCR-004", lambda: build_report_harvest()),
    ("PCP-005", lambda: build_plan_protein_a()), ("PCR-005", lambda: build_report_protein_a()),
    ("PCP-006", lambda: build_plan_viral_inactivation()),
    ("PCR-006", lambda: build_report_viral_inactivation()),
    ("PCP-007", lambda: build_plan_cex()), ("PCR-007", lambda: build_report_cex()),
    ("PCP-008", lambda: build_plan_aex()), ("PCR-008", lambda: build_report_aex()),
    ("PCP-009", lambda: build_plan_vf()), ("PCR-009", lambda: build_report_vf()),
    ("PCP-010", lambda: build_plan_ufdf()), ("PCR-010", lambda: build_report_ufdf()),
    ("PTP-001", lambda: build_transfer_plan()),
    ("RA-001", lambda: build_risk_assessment()),
    ("PCMP-001", lambda: build_master_plan()),
    ("INV-001", lambda: build_investigation()),
    ("PCMR-001", lambda: build_master_report()),
]

#: Documents whose builder has been rewritten against the Rev 2.0 text. A document NOT in this
#: set still has its Rev 1.0 .docx in pc_package/ and its Rev 1.0 annex in ground_truth/, and its
#: builder would now read Rev 2.0 helper values that the Rev 1.0 text does not contain, so it is
#: skipped and its annex kept as it is. This keeps check_grounding green at every step of the
#: Rev 2.0 campaign (work unit 2026-10-08_01_rev2-campaign). When every document is in the set,
#: delete this mechanism.
REV2_READY: set = {"INV-001", "PCMP-001", "PCP-005", "PCR-005"}


def main():
    os.makedirs(OUT, exist_ok=True)
    for doc_id, build in BUILDERS:
        if doc_id not in REV2_READY:
            print(f"kept {doc_id}: Rev 1.0 annex (document not yet re-authored for Rev 2.0)")
            continue
        annex = build()
        path = os.path.join(OUT, f"{annex.document_id}.json")
        with open(path, "w") as fh:
            # serialize_as_any: the vendored models annotate `list[SourceReference]` against
            # the CONTRACT class, and pydantic serializes to the declared annotation — so
            # `table_header`, which lives on the schema_ext subclass, is dropped from every
            # such reference with no warning. Duck-typed serialization keeps it. Verified on
            # pydantic 2.13.4; check_grounding gates the field, so a silent drop would show
            # up there rather than in a silently thinner annex.
            json.dump(annex.model_dump(mode="json", serialize_as_any=True), fh,
                      indent=2, ensure_ascii=False)
        ne = sum(len(s.process_steps) + len(s.parameters) + len(s.quality_attributes)
                 + len(s.analytical_methods) + len(s.equipment) + len(s.sites) for s in annex.entities)
        print(f"wrote {path}: {ne} entities, {len(annex.studies)} studies, "
              f"{len(annex.assertions.assertions)} assertions, "
              f"{len(annex.concepts.concepts)} concepts")


if __name__ == "__main__":
    main()
