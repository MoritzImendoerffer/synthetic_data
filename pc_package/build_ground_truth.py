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

import _pcpkg as P
import schema_ext as S
from check_grounding import CELL_SEP   # the one definition of a rendered cell boundary

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ground_truth")

UO = "bioreactor"
UO_NAME = "Production Bioreactor"
STEP = P.CFG.unit_op(UO).step
STEP_LABEL = f"{UO_NAME} (Step {STEP})"

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
                  "The production bioreactor forms the glycan, charge variant and aggregate "
                  "quality attributes of A-Mab, which places the widest part of the drug "
                  "substance control strategy at this one step")
    else:
        src = ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                  "A-Mab is produced by fed-batch culture of a recombinant Chinese hamster "
                  "ovary cell line in a stirred tank bioreactor")
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
                               "The characterization studies were executed in stirred tank "
                               "scale-down bioreactors qualified against the commercial "
                               "vessel under SOP-1001" if report
                               else "Execution will use bench-scale stirred tank bioreactors of "
                                    "equivalent design to the commercial vessels, operated "
                                    "under SOP-2003")],
        metadata=meta())
    vessel = S.Equipment(
        equipment_id="equip:production_bioreactor",
        equipment_name="15,000 L production bioreactor", equipment_type="bioreactor",
        site_name=P.RECEIVING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Product and unit operation" if report
                               else "Unit-operation description and prior knowledge",
                               "The culture in that bioreactor is grown at a working volume "
                               "of 15,000 L, fed on a defined schedule" if report
                               else "The commercial process operates at 15,000 L of culture")],
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
    "AMV-3010": ("Released N-glycan mapping by 2-AB HILIC-UPLC (SOP-3010, AMV-3010) reports "
                 "afucosylation, galactosylation and high mannose from one chromatogram"),
    "AMV-3011": ("size variants by SEC-HPLC (SOP-3011, AMV-3011) report aggregates"),
    "AMV-3012": "Host cell protein by ELISA (AMV-3012)",
    "AMV-3013": ("charge variants by imaged capillary isoelectric focusing (SOP-3013, "
                 "AMV-3013) report acidic variants"),
    "AMV-3014": "residual host cell DNA by qPCR (AMV-3014)",
}
# CQA key -> the fragment used for that attribute's attribute -> method assertion.
#
# One sentence states three of these relations, so quoting it whole made one span the anchor
# for four records at once. Each glycan attribute instead takes the slice of that sentence
# ending at its OWN analyte name, so the span names the method and that attribute and stops —
# which is what a human annotator marks, and what makes the span usable on its own. The method
# entity keeps the whole sentence, since it is the record the whole sentence is about.
CQA_METHOD_QUOTE = {k: METHOD_QUOTE[m] for k, m in CQA_METHOD.items()}
_GLYCAN_CLAUSE = "Released N-glycan mapping by 2-AB HILIC-UPLC (SOP-3010, AMV-3010) reports "
CQA_METHOD_QUOTE.update({
    "afucosylation": _GLYCAN_CLAUSE + "afucosylation",
    "galactosylation": _GLYCAN_CLAUSE + "afucosylation, galactosylation",
    "high_mannose": _GLYCAN_CLAUSE + "afucosylation, galactosylation and high mannose",
})

# Per-parameter classification sentence from the report's "Parameter classification"
# section. Each span opens on the parameter it classifies and carries the class and the
# reason, so it names both ends of the relation it anchors.
CLASS_QUOTE = {
    "Culture pH": ("Culture pH was classified WC-CPP"),
    "Culture temperature": ("Culture temperature was classified WC-CPP on the same control "
                            "argument"),
    "Dissolved CO2 (pCO2)": ("Dissolved CO2 was classified WC-CPP. It governs acidic variants "
                             "and carries significant terms on galactosylation as well"),
    "Osmolality": ("Osmolality was classified WC-CPP on screening evidence alone, which makes "
                   "it the only parameter in the register classified that way"),
    "Culture duration": ("Culture duration was classified WC-CPP. The largest single coefficient "
                         "anywhere in the study belongs to the duration term on galactosylation"),
    "Dissolved oxygen": ("Dissolved oxygen was classified KPP"),
    "Initial viable cell conc.": ("Initial viable cell concentration was classified KPP on the "
                                  "same basis. It sets the growth trajectory of the culture and "
                                  "with it the productivity of the run"),
    "Nutrient feed-1 volume": ("Nutrient feed-1 volume was classified KPP. The delivered volume "
                               "drives titer and the late-culture nutrient environment"),
    "Basal medium concentration": ("Basal medium concentration was classified GPP"),
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
                                   "a two-level fractional factorial in 5 factors at "
                                   "resolution V was used for screening" if report
                                   else "The fractional design is of resolution V. Therefore, the "
                                        "design estimates every main effect clear of every "
                                        "two-factor interaction")],
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
                                   "Face centred axial points were chosen so that no run falls "
                                   "outside the characterization range of any factor" if report
                                   else "The response-surface design is a face-centred central "
                                        "composite in the 4 factors that screening is expected "
                                        "to retain")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:br_sdm_qual", study_type="scale_down_qualification", unit_operation=UO_NAME,
            scale_down_model=SDM,
            source_references=[ref(doc_id, file_name, sec,
                                   "Scale-down model and its qualification",
                                   "At the qualification stage, the two scales were compared at "
                                   "set-point operation on growth, viability and titer "
                                   "trajectories, and on the five quality attributes measured "
                                   "at harvest" if report
                                   else "The qualification compares the bench system with"
                                        " 15,000 L data on the inputs and the outputs that "
                                        "matter here")],
            metadata=meta()),
        # Both documents carry the univariate assessment of initial viable cell concentration.
        S.StudyDesign(
            study_id="study:br_univariate", study_type="univariate", unit_operation=UO_NAME,
            factors=["Initial viable cell conc."], responses=["process performance"],
            associated_parameters=["param:initial_vcc"],
            source_references=[ref(doc_id, file_name, sec, "Univariate assessment",
                                   "Over the ranges assessed, no univariate variation of those "
                                   "four parameters moved a quality attribute outside its "
                                   "acceptance criterion" if report
                                   else "dissolved oxygen, initial viable cell concentration, basal "
                                        "medium concentration and nutrient feed-1 volume, and "
                                        "each of the four will be assessed separately")],
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
               "this plan sets out the studies that will define it"),
            st(2, "Nine process parameters are in scope, five studied multivariately and four univariately.",
               "Risk-based prioritization of parameters",
               "parameters will be studied over the ranges in the same table, one at a time"),
            st(3, "The study uses a screening fractional-factorial design followed by a "
                  "face-centred central composite design on a qualified bench-scale scale-down model.",
               "Response-surface design",
               "The response-surface design is a face-centred central composite in the 4 "
               "factors that screening is expected to retain"),
            st(4, "Models are acceptable when there is no significant lack of fit against the center-point pure error.",
               "Acceptance and decision criteria",
               "A response-surface model is adequate for the operating region when the overall "
               "regression is significant"),
            st(5, "The study must establish a multivariate operating region over which every "
                  "governed attribute is predicted to lie inside its acceptance criterion.",
               "Acceptance and decision criteria",
               "The operating region is acceptable when every attribute the step governs is "
               "predicted to meet the criterion"),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Culture pH, temperature, dissolved CO2, osmolality and culture duration are classified WC-CPP.",
           "Executive summary",
           "5 were classified WC-CPP, 3 KPP and 1 GPP"),
        # The re-authored report states the response set here instead of the peak viable cell
        # density and titre the previous revision gave, so the statement follows the document.
        st(2, "The five attributes measured as responses of the designed experiments are "
              "afucosylation, galactosylation, high mannose, acidic charge variants and aggregate.",
           "Product and unit operation",
           "The production bioreactor forms the glycan, charge variant and aggregate quality "
           "attributes of A-Mab"),
        st(3, "Within the design space the fitted response-surface models predict every measured "
              "attribute inside its in-process limit.",
           "Design space",
           "over which every attribute the step governs stays inside its in-process limit"),
        st(4, "The response-surface models describe the characterized region adequately and every "
              "overall F test reaches significance.",
           "Response-surface models",
           "The response surface models describe the characterized region adequately"),
        st(5, "There was no significant lack of fit relative to the center-point pure error.",
           "Response-surface models",
           "No lack of fit test reaches significance against the centre-point pure error"),
        st(6, "All bioreactor-set CQAs meet acceptance with margin at commercial scale.",
           "Conclusions",
           "All 7 attributes formed at the step meet the drug substance acceptance criteria "
           "at commercial scale"),
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
                               "That region is defined in the 4 well-controlled parameters "
                               "carried into the response surface design: culture pH, culture "
                               "temperature, culture duration and dissolved CO2")],
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
        "AMV-3015": "Turbidity in the centrate and in the clarified harvest is measured by "
                    "nephelometry",
        "AMV-3012": "HCP is measured by ELISA",
        "AMV-3014": "residual DNA by qPCR",
        "AMV-3011": "the size variant profile by SEC-HPLC",
    },
    "PCR-004": {
        "AMV-3015": "Turbidity is the primary in-process measure of clarification and was "
                    "determined by nephelometry",
        "AMV-3012": "host cell protein was measured by ELISA",
        "AMV-3014": "residual DNA by qPCR",
        "AMV-3011": "Aggregate was followed by SEC-HPLC",
    },
}
# Attributes the step CARRIES FORWARD (it forms and clears none): one
# (section title, fragment) per attribute. The two documents place them differently.
HATTR_QUOTE = {
    "PCP-004": {
        "turbidity": ("Purpose and scope",
                      "Post-clarification turbidity is the attribute by which the clarified "
                      "harvest is released to capture"),
        "hcp": ("Quality attributes in scope",
                "Host cell protein is the attribute in this table that most constrains the "
                "design of the downstream train"),
        "residual_dna": ("Quality attributes in scope",
                         "HCP and residual DNA are measured on the clarified harvest at every "
                         "studied condition"),
        "aggregates_hmw": ("Quality attributes in scope",
                           "Shear at the centrifuge feed zone is the only mechanism at this step "
                           "that could raise the level of high molecular weight species"),
    },
    "PCR-004": {
        "turbidity": ("Parameters, ranges and the knowledge space",
                      "the attribute by which the clarified harvest is accepted for capture"),
        "hcp": ("Quality attributes in scope",
                "Host cell protein is the most consequential of the three"),
        "residual_dna": ("Quality attributes in scope",
                         "Residual DNA is of very low criticality on its own, and is cleared by "
                         "a large margin downstream."),
        "aggregates_hmw": ("Quality attributes in scope",
                           "Aggregate is of high criticality and is the one attribute with a "
                           "plausible mechanism at this step"),
    },
}
# "no product-quality impact": one (section title, fragment) per parameter. Step 4
# runs NO designed experiment, so the claim rests on the null result of the
# univariate assessment and on the absence of a mechanism, not on a fitted model.
HNOIMPACT_QUOTE = {
    "PCP-004": {
        "Centrifugation (rcf)": ("Risk-based prioritization of parameters",
                                 "Neither settable parameter is linked to a critical quality "
                                 "attribute"),
        "Depth filter load": ("Risk-based prioritization of parameters",
                              "Neither settable parameter is linked to a critical quality "
                              "attribute"),
        "Post-clarification turbidity": ("Statistical methods",
                                         "no parameter at this step is linked to a critical "
                                         "quality attribute"),
    },
    "PCR-004": {
        "Centrifugation (rcf)": ("Product quality across the step",
                                 "No increase was seen over the centrifugation range assessed."),
        "Depth filter load": ("Product quality across the step",
                              "No quality attribute changed across clarification"),
        "Post-clarification turbidity": ("Parameter classification",
                                         "it has no demonstrated link to a quality attribute"),
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
                  "The step forms no product-quality attribute and is credited with no "
                  "impurity clearance")
    else:
        src = ref(doc_id, file_name, sec, "Purpose and scope",
                  "It forms no product quality attribute of its own")
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
                "It removes cells and cell debris from the production bioreactor broth by "
                "continuous disk-stack centrifugation")
        dep = ("Executive summary",
               "it clarifies the centrate through a depth filter train and a sterile filter")
        sdm_ref = ("Scale-down model and its qualification",
                   "A scale-down model of the harvest and clarification step was qualified "
                   "against commercial-scale data before the study")
    else:
        cent = ("Unit-operation description and prior knowledge",
                "The same continuous disk-stack centrifuge and the same graded depth filter train")
        dep = ("Unit-operation description and prior knowledge",
               "Depth filtration retains the fine particles that the centrifuge does not remove")
        sdm_ref = ("Purpose and scope",
                   "a qualified scale-down model of the commercial harvest train")
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
    """Rendered ``@tbl-params`` rows of the harvest pair, keyed by parameter name."""
    return param_rows(HUO, classified, floatfmt=None if classified else ".0f")


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
           "No designed experiment was executed at this step, and none is reported." if report
           else "Each settable parameter will be studied at its low characterization edge, at "
                "its set-point and at its high characterization edge")
    qual = ("Scale-down model and its qualification",
            "Qualification compared step yield and post-clarification turbidity between the "
            "model and the commercial-scale process at the target condition" if report
            else "Qualification will use triplicate model runs on a common feed.")
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
               "The work is Stage 1 process design under the lifecycle approach to process "
               "validation"),
            st(2, "The step sets no critical quality attribute; the attributes in scope are the "
                  "ones it carries forward to the purification train.",
               "Quality attributes in scope",
               "The attributes in scope are the ones it carries forward to the purification train"),
            st(3, "Each parameter is varied across its characterization range with the other "
                  "parameters held at their set-points.",
               "Statistical methods",
               "Each parameter will be varied across its characterization range while the other "
               "parameters are held at their set-points"),
            st(4, "The operation is judged against process-performance criteria (turbidity, "
                  "recovery and filter-train pressure) because it forms no CQA.",
               "Acceptance and decision criteria",
               "Three of them are process performance criteria (turbidity, recovery and filter "
               "train pressure)."),
            st(5, "The operation delivers the clarified harvest that the Protein A capture step "
                  "(Step 5) receives.",
               "Purpose and scope",
               "it delivers the clarified harvest that the Protein A capture step (Step 5) "
               "receives"),
            st(6, "No response-surface model will be fitted and no design space will be claimed "
                  "for this step.",
               "Statistical methods",
               "No response surface model will be fitted, and no design space will be claimed "
               "for this step."),
        ])]
    yw = P.csv("yield_waterfall.csv")
    hy = float(yw[yw.step == HSTEP].iloc[0].step_yield)
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Harvest and clarification forms no critical quality attribute and reduces none; "
              "the attributes formed upstream pass through it unchanged.",
           "Product and unit operation",
           "The step forms no critical quality attribute and reduces none"),
        st(2, f"The step recovers {P.pct(hy)} of the product presented to it in the nominal "
              f"commercial-scale simulation.",
           "Step yield and mass balance",
           "The step recovers almost all of the product presented to it."),
        st(3, "Clarification met its in-process expectation across the ranges studied, with a "
              "single turbidity excursion above the normal operating range at near-maximum "
              "depth-filter loading (DEV-004-02), which was retained.",
           "Clarification performance and filter capacity",
           "Clarification met its in-process expectation across the ranges studied, with one "
           "excursion that is described below."),
        st(4, "No quality attribute changed across clarification over the ranges assessed.",
           "Product quality across the step", "No quality attribute changed across clarification"),
        st(5, "Centrifugation force and depth-filter loading are key process parameters and "
              "post-clarification turbidity is a general process parameter; the step carries no "
              "critical process parameter.",
           "Conclusions",
           "Centrifugation force and depth-filter loading are key process parameters and "
           "post-clarification turbidity is a general process parameter"),
        st(6, "No designed experiment was executed at this step and it contributes no design "
              "space to the drug substance.",
           "Design space", "This step contributes no design space"),
        st(7, "Clearance of the impurity burden the step carries forward is credited to the "
              "purification train (PCR-005, PCR-007, PCR-008) and not to this step.",
           "Impurity burden carried to Protein A capture",
           "Clearance is a property of the purification train and not of this step."),
        st(8, "Two deviations were recorded; neither altered a parameter classification, a "
              "characterized range or a conclusion of the report.",
           "Deviations from the plan",
           "Neither altered a parameter classification, a characterized range or a conclusion "
           "of this report."),
        st(9, "The outcome of the report rolls up into the Process Characterization Master "
              "Report (PCMR-001).",
           "Conclusions", "The outcome rolls up into PCMR-001."),
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
    """One PAR per parameter, each anchored on its row of @tbl-par.

    The step runs no designed experiment, so PCR-004 builds @tbl-par by renaming the
    characterization range of the parameter table: the PAR *is* the characterized range
    here. Rebuilt from the same expression so each record anchors on its own row.
    """
    df = P.report_params(HUO).rename(columns={"Char. range": "Proven acceptable range"})
    df = df[["Parameter", "Unit", "Set-point", "NOR", "Proven acceptable range", "Class"]]
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
# DoE factors (the four multivariate parameters) vs the two univariate GPPs.
PA_MULTIVARIATE = ["Protein load", "Elution buffer pH", "Load flow rate", "End of pool collect"]
PA_UNIVARIATE = ["Operating temperature", "Bed height"]
PA_WCCPP = ["Protein load", "Elution buffer pH"]      # drive eluate-pool HCP
PA_KPP = ["Load flow rate", "End of pool collect"]    # drive step yield

# Attributes: the one CQA the step SETS, and the two impurity CQAs it clears. The
# cleared pair are listed in the documents with their drug-substance criteria, but
# neither is judged against that criterion at the outlet of this step.
PA_CQA_KEYS = ["leached_protein_a", "hcp", "residual_dna"]
PAATTR_CONCEPT = {
    "leached_protein_a": "attr:leached_protein_a",
    "hcp": "attr:hcp", "residual_dna": "attr:residual_dna",
    "aggregates_hmw": "attr:aggregates_hmw",
}
PAATTR_NAME = {
    "leached_protein_a": "Leached Protein A", "hcp": "Host Cell Protein (HCP)",
    "residual_dna": "Residual DNA", "aggregates_hmw": "Aggregates (HMW)",
}
PA_CQA_METHOD = {"leached_protein_a": "AMV-3016", "hcp": "AMV-3012", "residual_dna": "AMV-3014"}
PAMETHODS = [
    ("AMV-3016", "Leached Protein A by ELISA (ppm)", "immunoassay",
     ["leached Protein A"], ["leached_protein_a"]),
    ("AMV-3012", "Host-Cell Protein ELISA", "immunoassay", ["host-cell protein"], ["hcp"]),
    ("AMV-3014", "Residual DNA (qPCR)", "qPCR", ["residual host-cell DNA"], ["residual_dna"]),
    ("AMV-3011", "Size-Variants (SEC-HPLC)", "chromatography",
     ["aggregate", "monomer"], ["aggregates_hmw"]),
]

# --------------------------------------------------------------------------- #
# Per-entity grounded fragments. Every string below is a verbatim substring of  #
# the RENDERED document named in the comment (check_grounding.py is the gate).  #
# --------------------------------------------------------------------------- #
# Analytical methods: the sentence that links each method to its analyte.
# Plan §5.3 / Report §3.3, both titled "Analytical methods".
PA_METHOD_QUOTE = {
    "AMV-3016": ("Leached Protein A is measured by ELISA under AMV-3016",
                 "Leached Protein A was measured by ELISA under AMV-3016 and is reported in ppm"),
    "AMV-3012": ("host cell protein by the platform ELISA under AMV-3012",
                 "Pool host cell protein was measured by ELISA under AMV-3012 and is reported as "
                 "ng of host cell protein per mg of antibody"),
    "AMV-3014": ("Residual DNA is measured by qPCR under AMV-3014",
                 "residual DNA by qPCR under AMV-3014"),
    "AMV-3011": ("aggregate by SEC-HPLC under AMV-3011",
                 "size variants by SEC-HPLC under AMV-3011"),
}
# Quality attributes, from "Quality attributes in scope" (plan §4.2 / report §2.2).
PA_CQA_QUOTE = {
    "leached_protein_a": ("Leached Protein A is formed here and nowhere else in the process",
                          "The step sets one quality attribute of its own"),
    "hcp": ("this step is the principal point of its removal",
            "the capture step delivers the single largest reduction of the purification train"),
    "residual_dna": ("Residual DNA carries the lowest criticality of the four attributes and is "
                     "cleared across three steps",
                     "Residual DNA is of very low criticality and clears to well below its limit "
                     "across the train"),
}
# Table captions carrying the attribute rows (report splits set vs cleared over two tables).
PA_CQA_TABLE_PLAN = ("Quality attributes governed or monitored at the capture step, with their "
                     "drug-substance acceptance criteria.")
PA_CQA_TABLE_REPORT = {
    "leached_protein_a": ("Quality attribute set by the Protein A step, with acceptance criterion "
                          "and criticality assigned under the Tool #1 impact and uncertainty ranking."),
    "hcp": "Quality attributes formed upstream and cleared by the Protein A step.",
    "residual_dna": "Quality attributes formed upstream and cleared by the Protein A step.",
}
# Report §9 "Parameter classification": the sentence that justifies each classification.
PA_CLASS_QUOTE = {
    "Protein load": ("Load carries the second largest coefficient on pool host cell protein and "
                     "interacts with elution buffer pH"),
    "Elution buffer pH": ("Elution pH carries the largest coefficient of any term on pool host "
                          "cell protein and the only significant curvature"),
    "Load flow rate": ("Load flow rate is classified as a key process parameter, since flow "
                       "affects step yield significantly and reduces it at high load through the "
                       "load by flow interaction"),
    "End of pool collect": ("The parameter is classified as key on that basis and is monitored as "
                            "a performance parameter"),
    "Operating temperature": ("In operation it is held within a narrow band by the chromatography "
                              "chamber EQ-CHR-118"),
    "Bed height": ("is fixed in operation by the packing acceptance criteria in SOP-2008"),
}
# Plan §4.1 / §6.4: the prior-knowledge expectation stated for each parameter before the study.
PA_PRIOR_QUOTE = {
    "Protein load": ("Unit-operation description and prior knowledge",
                     "a high load is expected to raise the host cell protein carried into the eluate"),
    "Elution buffer pH": ("Unit-operation description and prior knowledge",
                          "both pool host cell protein and leached Protein A are expected to rise "
                          "as the elution pH falls"),
    "Load flow rate": ("Unit-operation description and prior knowledge",
                       "its effect is expected on step yield and not on the quality attributes"),
    "Operating temperature": ("Univariate assessment",
                              "Temperature acts on binding kinetics and on the rate of ligand "
                              "hydrolysis, and both processes are slow compared with the residence "
                              "time of the step"),
    "Bed height": ("Univariate assessment",
                   "Bed height acts on residence time at a fixed linear velocity, so its influence "
                   "is already spanned by the load flow rate factor"),
}
# Report §7 "Proven acceptable ranges": one fragment per response of @tbl-par.
PA_PAR_QUOTE = {
    "Pool HCP (ng/mg)": ("The in-process limit is, and against it every pool host cell protein "
                         "row returns a range"),
    "Leached Protein A (ppm)": ("Its whole characterization range is proven acceptable for every "
                                "parameter at set-point"),
}
PA_PAR_TABLE = ("Proven acceptable ranges by governed attribute and parameter, at set-point and "
                "with the remaining factors propagated across their normal operating ranges.")
PA_PAR_BASIS = {
    "Pool HCP (ng/mg)": ("The drug-substance host-cell-protein limit, drawn for reference only: it "
                         "does not apply at the outlet of the capture step, so no proven acceptable "
                         "range is claimed. The pool level is an in-process value carried to the "
                         "polishing steps (PCR-007, PCR-008) and consolidated in PCMR-001."),
    "Leached Protein A (ppm)": ("Drug-substance specification for leached Protein A, the only "
                                "quality attribute this step sets, applied as an upper limit; the "
                                "capture step makes no viral-clearance claim."),
}


def _pa_cqa_row(key):
    return P.cqa_reg[P.cqa_reg.key == key].iloc[0].to_dict()


def pa_step(doc_id, file_name, sec, report):
    if report:
        src = ref(doc_id, file_name, sec, "Executive summary",
                  "Protein A chromatography is the capture step of the A-Mab drug substance "
                  "process and the first chromatographic operation in the purification train")
    else:
        src = ref(doc_id, file_name, sec, "Purpose and scope",
                  "It sets one quality attribute, leached Protein A, and it is the principal point "
                  "of host cell protein and residual DNA removal in the process")
    return S.ProcessStep(
        step_id="step:protein_a", step_name=PAUO_NAME, step_number=str(PASTEP),
        unit_operation=PAUO_NAME,
        description="Affinity capture on Protein A resin, operated in bind-and-elute mode: binds "
                    "the antibody from clarified harvest, is the principal point of host cell "
                    "protein and residual DNA removal, and sets leached Protein A — the only "
                    "quality attribute the step forms. Makes no viral-clearance and no aggregate-"
                    "clearance claim, and does not modify the attributes formed in cell culture.",
        input_materials=["clarified harvest (Protein A load)"],
        output_materials=["Protein A eluate pool (viral-inactivation feed)"],
        equipment=["Protein A affinity column", "scale-down chromatography column"],
        source_references=[src], metadata=meta())


def pa_equipment(doc_id, file_name, sec, report):
    # Both documents describe the scale-down model in "Scale-down model and its
    # qualification" (plan §5.1 / report §3.1); only the plan names the commercial column.
    sdm = S.Equipment(
        equipment_id="equip:pa_sdm_column", equipment_name="scale-down chromatography column",
        equipment_type="chromatography column (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Scale-down model and its qualification",
                               "A scale-down chromatography system was qualified as a model of "
                               "the manufacturing-scale step under SOP-1001" if report
                               else "a bench-scale column that is a qualified model of the "
                                    "commercial step")],
        metadata=meta())
    if report:
        return [sdm]
    return [
        S.Equipment(equipment_id="equip:pa_column",
                    equipment_name="commercial-scale Protein A capture column",
                    equipment_type="chromatography column", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec,
                                           "Scale-down model and its qualification",
                                           "column efficiency falls inside the range recorded for "
                                           "the commercial column")],
                    metadata=meta()),
        sdm,
    ]


def pa_sites(doc_id, file_name, sec):
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


def pa_params(doc_id, file_name, sec, classified):
    caption = ("Process parameters of the Protein A step, with set-point, normal operating range, "
               "characterization range, final classification and study type."
               if classified else
               "Parameters of the capture step, with set-point, characterization range, normal "
               "operating range and the study type assigned by RA-001.")
    rats = {"WC-CPP": "Carries a large effect on pool host cell protein — the impurity load the "
                      "polishing steps have to handle — and is reliably controlled within its "
                      "normal operating range, so the risk of an undetected excursion is low.",
            "KPP": "Governs step yield / process performance without an effect on the quality "
                   "attribute this step sets.",
            "GPP": "Held within a narrow band by equipment design or fixed at column packing, and "
                   "ranked below the threshold for multivariate study."}
    rows = param_rows(PAUO, classified)   # each parameter on its own @tbl-params row
    out = []
    for r in PAPARAM_ROWS:
        name = r["parameter"]
        ptype = r["classification"] if classified else "unclassified"
        out.append(S.ProcessParameter(
            parameter_id=PAPARAM_CONCEPT[name], parameter_name=name, parameter_type=ptype,
            unit=r["unit"], target_value=f"{r['setpoint']:g}",
            NOR=f"{r['nor_low']:g}–{r['nor_high']:g} {r['unit']}",
            PAR=f"{r['par_low']:g}–{r['par_high']:g} {r['unit']}",
            associated_step=PASTEP_LABEL,
            rationale_for_criticality=rats.get(r["classification"]) if classified else None,
            source_references=[ref(doc_id, file_name, sec,
                                   "Factors, ranges and the knowledge space" if classified
                                   else "Factors, ranges and study type",
                                   rows[name], table_title=caption,
                                   table_id=f"{doc_id}_tab_params",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


def pa_cqas(doc_id, file_name, sec, report):
    """The one attribute the step SETS plus the two it clears.

    The cleared attributes carry a drug-substance acceptance criterion, but the step is
    not judged against it at its own outlet. It is judged against an in-process limit,
    carried back from the drug-substance limit through the clearance the downstream steps
    deliver. The DS acceptance is still recorded as the attribute's criterion, and the
    step-level position is carried by the assertions and report_sections.
    """
    rows = pa_cqa_rows(report)
    out = []
    for key in PA_CQA_KEYS:
        r = _pa_cqa_row(key)
        table_title = PA_CQA_TABLE_REPORT[key] if report else PA_CQA_TABLE_PLAN
        out.append(S.QualityAttribute(
            attribute_id=PAATTR_CONCEPT[key], attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"],
            acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']} (drug substance)"],
            analytical_method=None if report else PA_CQA_METHOD[key],
            associated_steps=[PASTEP_LABEL],
            rationale_for_criticality=f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = {r['tool1_score']}.",
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref(doc_id, file_name, sec, "Quality attributes in scope",
                                   rows[key], table_title=table_title,
                                   table_id=f"{doc_id}_tab_cqa", table_header=rows.header)],
            metadata=meta()))
    return out


def pa_cqa_rows(report):
    """Rendered attribute rows of the Protein A pair, keyed by attribute key.

    The report splits the register in two: the attribute the step SETS (``cqas_for``) and the
    ones it clears (``cqas_by_keys``), each its own table. The plan renders one table in its
    own order. Both tables share a header, so the rows can be merged into one lookup.
    """
    if report:
        rows = cqa_rows(["leached_protein_a"], uo_key=PAUO)
        rows.update(cqa_rows(["hcp", "residual_dna"]))
        return rows
    return cqa_rows(["leached_protein_a", "hcp", "residual_dna", "aggregates_hmw"])


def pa_methods(doc_id, file_name, sec, report):
    out = []
    for mid, mname, mtype, analytes, attrs in PAMETHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[PAATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods",
                                   PA_METHOD_QUOTE[mid][1 if report else 0])],
            metadata=meta()))
    return out


def pa_studies(doc_id, file_name, report):
    sec = f"{doc_id}_sec_study"
    n_scr, n_rsm = P.doe_runs(PAUO, "screening"), P.doe_runs(PAUO, "rsm")
    responses = ["pool_hcp_ng_mg", "step_yield", "leached_protein_a_ppm"]
    studies = [
        S.StudyDesign(
            study_id="study:pa_screening", study_type="screening_doe",
            design_name="two-level full factorial", unit_operation=PAUO_NAME,
            factors=PA_MULTIVARIATE, responses=responses,
            n_runs=n_scr, n_center_points=P.doe_centre_points(PAUO, "screening"), scale_down_model="scale-down chromatography column",
            associated_parameters=[PAPARAM_CONCEPT[f] for f in PA_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Screening design",
                                   "The screening was executed as a two-level full factorial in "
                                   "the four multivariate factors with"
                                   if report
                                   else "A two-level full factorial in the 4 multivariate factors "
                                        "will be run")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:pa_rsm", study_type="response_surface_doe",
            design_name="face-centred central composite design", unit_operation=PAUO_NAME,
            factors=PA_MULTIVARIATE, responses=responses,
            n_runs=n_rsm, n_center_points=P.doe_centre_points(PAUO, "rsm"), scale_down_model="scale-down chromatography column",
            associated_parameters=[PAPARAM_CONCEPT[f] for f in PA_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "a face-centred central composite design in the same four factors"
                                   if report
                                   else "A face-centred central composite design will follow in the "
                                        "same 4 factors")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:pa_sdm_qual", study_type="scale_down_qualification",
            unit_operation=PAUO_NAME, scale_down_model="scale-down chromatography column",
            source_references=[ref(doc_id, file_name, f"{doc_id}_sec_methods",
                                   "Scale-down model and its qualification",
                                   "The scale-down model was compared with manufacturing-scale "
                                   "performance on the attributes that matter for the claims in "
                                   "this report"
                                   if report
                                   else "triplicate scale-down runs at the set-point condition will "
                                        "be compared with the corresponding at-scale data")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:pa_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=PAUO_NAME,
            factors=PA_UNIVARIATE, responses=responses,
            associated_parameters=[PAPARAM_CONCEPT[f] for f in PA_UNIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Univariate assessment",
                                   "Operating temperature and bed height were assessed one "
                                   "parameter at a time over the characterization ranges in"
                                   if report
                                   else "Operating temperature and bed height will be assessed one "
                                        "factor at a time")],
            metadata=meta()),
    ]
    return studies


def pa_concepts():
    from annex_contract.concepts import Concept, ConceptStore
    cs = [Concept(concept_id="step:protein_a", concept_type="PROCESS_STEP",
                  canonical_name=PAUO_NAME,
                  aliases=["Protein A", "Protein A capture", "affinity capture", "Step 5"],
                  review_status="human_verified")]
    for name, cid in PAPARAM_CONCEPT.items():
        cs.append(Concept(concept_id=cid, concept_type="PROCESS_PARAMETER", canonical_name=name,
                          review_status="human_verified"))
    for key in ["leached_protein_a", "hcp", "residual_dna"]:
        cs.append(Concept(concept_id=PAATTR_CONCEPT[key], concept_type="QUALITY_ATTRIBUTE",
                          canonical_name=PAATTR_NAME[key], aliases=[key],
                          review_status="human_verified"))
    for mid, mname, *_ in PAMETHODS:
        cs.append(Concept(concept_id=f"method:{mid}", concept_type="ANALYTICAL_METHOD",
                          canonical_name=mname, aliases=[mid], review_status="human_verified"))
    return ConceptStore(run_id="gt-protein_a", concepts=cs)


def pa_assertions(doc_id, file_name, report):
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

    # step -> parameter on the parameter's own row. The summary sentence counts the
    # parameters; only the row names one.
    prow = param_rows(PAUO, report)
    param_sec = ("Factors, ranges and the knowledge space" if report
                 else "Factors, ranges and study type")
    for name, cid in PAPARAM_CONCEPT.items():
        add("step:protein_a", "step_has_parameter", cid,
            f"{PAUO_NAME} has process parameter {name}.", param_sec, prow[name], prow.header)
    # The step SETS leached Protein A and clears HCP and DNA.
    crow = pa_cqa_rows(report)
    add("step:protein_a", "step_has_quality_attribute", "attr:leached_protein_a",
        f"{PAUO_NAME} sets leached Protein A, the only quality attribute it forms.",
        "Quality attributes in scope", crow["leached_protein_a"], crow.header)
    for key in ["hcp", "residual_dna"]:
        add("step:protein_a", "step_has_quality_attribute", PAATTR_CONCEPT[key],
            f"{PAUO_NAME} is the principal clearance step for {PAATTR_NAME[key]}.",
            "Quality attributes in scope", crow[key], crow.header)
    # attribute -> method (plan only; the report links method to response, not to CQA)
    if not report:
        for key in PA_CQA_METHOD:
            add(PAATTR_CONCEPT[key], "attribute_measured_by_method", f"method:{PA_CQA_METHOD[key]}",
                f"{PAATTR_NAME[key]} is measured by {PA_CQA_METHOD[key]}.", "Analytical methods",
                PA_METHOD_QUOTE[PA_CQA_METHOD[key]][0])
    # Acceptance criteria. Both are drug-substance criteria: the leached Protein A limit is
    # the direct responsibility of this step, the HCP limit is explicitly NOT applied here.
    lpa = _pa_cqa_row("leached_protein_a")
    add("attr:leached_protein_a", "attribute_has_acceptance_criterion", "lit:leached_protein_a_acc",
        f"Leached Protein A acceptance: {lpa['acc_low']:g}–{lpa['acc_high']:g} {lpa['unit']} "
        f"at drug substance.",
        "Quality attributes in scope",
        "Leached Protein A keeps the drug-substance criterion itself, which is the "
        "conservative choice at a capture step" if report
        else "the criterion of 5 ppm is the direct responsibility of this study")
    hcp = _pa_cqa_row("hcp")
    add("attr:hcp", "attribute_has_acceptance_criterion", "lit:hcp_acc",
        f"Host cell protein acceptance: {hcp['acc_low']:g}–{hcp['acc_high']:g} {hcp['unit']} at "
        f"drug substance; the criterion is not applied at the outlet of this step.",
        "Proven acceptable ranges" if report else "Acceptance and decision criteria",
        "pool host cell protein is judged against an in-process limit carried back from the "
        "drug-substance criterion through the clearance the polishing steps deliver" if report
        else "Pool host cell protein will be judged against the drug-substance criterion of 100 ng/mg")
    # parameter -> attribute impacts / non-impacts
    if report:
        # Report §9: one classification sentence quoted against the parameter it classifies.
        for name in PA_WCCPP:
            add(PAPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:hcp",
                f"{name} carries a large effect on pool host cell protein (WC-CPP).",
                "Parameter classification", PA_CLASS_QUOTE[name])
        add(PAPARAM_CONCEPT["Load flow rate"], "parameter_does_not_significantly_impact_attribute",
            "attr:hcp", "Load flow rate acts on step yield and on no quality attribute in scope (KPP).",
            "Parameter classification", PA_CLASS_QUOTE["Load flow rate"])
        add(PAPARAM_CONCEPT["End of pool collect"], "parameter_does_not_significantly_impact_attribute",
            "attr:leached_protein_a",
            "End of pool collect has no effect on the attribute the step sets (KPP).",
            "Parameter classification", PA_CLASS_QUOTE["End of pool collect"])
        for name in PA_UNIVARIATE:
            add(PAPARAM_CONCEPT[name], "parameter_does_not_significantly_impact_attribute",
                "attr:leached_protein_a",
                f"{name} is not an operating variable of the multivariate design (GPP).",
                "Parameter classification", PA_CLASS_QUOTE[name])
        # The headline robustness finding: NO parameter affects the attribute the step sets.
        # The sentence that says so quantifies over the parameters and names none of them, so
        # each record takes §9's per-parameter classification sentence, which states the same
        # null result for one named parameter. The effect tables are no use here: they key on
        # the coded factor letters, so a row names "A", not "Protein load".
        for name in PA_MULTIVARIATE:
            add(PAPARAM_CONCEPT[name], "parameter_does_not_significantly_impact_attribute",
                "attr:leached_protein_a",
                f"{name} had no significant effect on leached Protein A over the ranges studied.",
                "Parameter classification", PA_CLASS_QUOTE[name])
    else:
        # Plan: the prior-knowledge expectation stated for each parameter before execution.
        for name in PA_WCCPP:
            sec_title, quote = PA_PRIOR_QUOTE[name]
            add(PAPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:hcp",
                f"{name} is expected to affect the pool host cell protein.", sec_title, quote)
        for name in ["Load flow rate"] + PA_UNIVARIATE:
            sec_title, quote = PA_PRIOR_QUOTE[name]
            add(PAPARAM_CONCEPT[name], "parameter_does_not_significantly_impact_attribute",
                "attr:hcp", f"{name} is expected to affect only process performance.",
                sec_title, quote)
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def pa_report_sections(doc_id, file_name, report):
    from annex_contract.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    n_pools = P.doe_runs(PAUO, "screening") + P.doe_runs(PAUO, "rsm")
    lpa = _pa_cqa_row("leached_protein_a")
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-005 defines the Stage-1 characterization study of the A-Mab Protein A "
                  "capture step (Step 5).",
               "Purpose and scope", "This plan defines the Stage-1 characterization study for that step"),
            st(2, "Four parameters are assigned to multivariate study and two to univariate "
                  "assessment.",
               "Purpose and scope",
               "This plan covers the 4 process parameters that RA-001 assigned to multivariate "
               "study and the 2 parameters it assigned to univariate study"),
            st(3, "The study uses a full-factorial screen followed by a face-centred central "
                  "composite design on a qualified scale-down column.",
               "Response-surface design",
               "A face-centred central composite design will follow in the same 4 factors"),
            st(4, "Protein A sets leached Protein A and is the principal point of host cell protein "
                  "and residual DNA removal.",
               "Purpose and scope",
               "It sets one quality attribute, leached Protein A, and it is the principal point of "
               "host cell protein and residual DNA removal in the process"),
            st(5, "The operating region will be declared as the multivariate subset of the "
                  "characterization ranges over which every attribute with a criterion stays inside it.",
               "Acceptance and decision criteria",
               "The operating region will be declared as the multivariate subset of the "
               "characterization ranges over which every attribute with a criterion is predicted "
               "to stay inside that criterion."),
            st(6, "A response with no significant term is pre-declared as a robustness result, and "
                  "no operating limit is derived from an effect the study could not resolve.",
               "Acceptance and decision criteria",
               "A response with no significant term is a result and will be reported as one."),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Two parameters are classified WC-CPP, two KPP and two GPP, and no parameter of the "
              "step required designation as a critical process parameter.",
           "Executive summary",
           "No parameter at this step was classified as a critical process parameter."),
        st(2, "Protein load and elution buffer pH are the two well-controlled critical process "
              "parameters, both through their effect on pool host cell protein.",
           "Parameter classification",
           "Elution buffer pH is classified as a well-controlled critical process parameter."),
        st(3, "The design space is the multivariate region in all four multivariate parameters, "
              "and the operative constraint is a joint one on protein load and elution buffer pH; "
              "load flow rate and end of pool collect do not bound it.",
           "Design space",
           "Load flow rate and end of pool collect do not bound the region within the "
           "characterized ranges"),
        st(4, "Pool host cell protein is well described and its predicted coefficient of "
              "determination supports prediction; step yield is adequate but descriptive.",
           "Response-surface models", "Pool host cell protein is modelled well."),
        st(5, "Leached Protein A showed no significant parameter effect; its model is retained as "
              "knowledge-space evidence of that robustness and is not used predictively.",
           "Response-surface models",
           "This report therefore makes no predictive use of it, with the treatment of the "
           "attribute set out below"),
        st(6, f"The operative result for leached Protein A is model-free: all {n_pools} pools "
              f"assayed met the {lpa['acc_high']:g} {lpa['unit']} acceptance criterion.",
           "Response-surface models",
           "However, the criterion applied here is the drug-substance specification, which is "
           "applied to the capture pool conservatively"),
        st(7, "The drug-substance host cell protein criterion applies to the drug substance and "
              "not to the Protein A pool, so the pool is judged against an in-process limit "
              "carried back through the clearance the polishing steps deliver.",
           "Quality attributes in scope",
           "An intermediate has to be judged against a criterion that applies to an "
           "intermediate."),
        st(8, "At drug substance the three impurity attributes the step governs all clear their "
              "limits with margin, and that margin is the combined result of three clearance steps.",
           "Process capability and robustness",
           "those figures are a statement about the process as a whole and not about this step "
           "alone"),
    ])]


def pa_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:protein_a", unit_operation=PAUO_NAME,
        parameters=[PAPARAM_CONCEPT[f] for f in PA_MULTIVARIATE],
        # The design space is bounded by the one attribute the step SETS. Pool host cell
        # protein is an in-process value that the report explicitly does not judge against
        # the drug-substance criterion here, so it does not constrain the region.
        quality_attributes_constrained=["attr:leached_protein_a"],
        definition="The multivariate region in protein load, elution buffer pH, load flow rate and "
                   "end of pool collect over which both governed impurity attributes stay within "
                   "the criteria that apply to this pool. Leached Protein A does not constrain the "
                   "region. What bounds it is the pool host cell protein handed to the polishing "
                   "steps (PCR-007, PCR-008), judged against an in-process limit carried back from "
                   "the drug-substance limit through their clearance and consolidated in PCMR-001.",
        source_references=[ref(doc_id, file_name, f"{doc_id}_sec_ds", "Design space",
                               "the region in protein load, elution buffer pH, load flow rate "
                               "and end of pool collect over which the fitted response-surface "
                               "models")],
        metadata=meta())]


def pa_proven_acceptable_ranges(doc_id, file_name):
    """One ProvenAcceptableRange per governed response x multivariate parameter, from the
    same DoE engine (``doe_report.par_table``) that renders @tbl-par in §7 of the report.

    The pool host cell protein rows are measured against the in-process limit for this
    pool, not the drug-substance criterion, which does not apply at the outlet of a capture
    step. Before that limit existed the analysis reported "none (set-point breaches)" here,
    against a limit the step never claimed to meet."""
    import doe_report as D
    rows = par_rows(PAUO)   # one row per governed attribute x parameter
    out = []
    for i, r in enumerate(D.par_table(PAUO).to_dict("records"), 1):
        cqa, param, unit = r["CQA"], r["Parameter"], (r["Unit"] or "")
        out.append(S.ProvenAcceptableRange(
            par_id=f"{doc_id}-PAR{i:02d}", unit_operation=PAUO_NAME,
            quality_attribute=cqa, parameter=param,
            characterization_range=f"{r['Char. range']} {unit}".strip(),
            par_at_setpoint=f"{r['PAR (set-point)']} {unit}".strip()
            if not str(r["PAR (set-point)"]).startswith("none") else str(r["PAR (set-point)"]),
            par_nor_propagated=f"{r['PAR (NOR)']} {unit}".strip()
            if not str(r["PAR (NOR)"]).startswith("none") else str(r["PAR (NOR)"]),
            acceptance_basis=par_basis_text(PAUO, cqa),
            source_references=[ref(doc_id, file_name, f"{doc_id}_sec_par",
                                   "Proven acceptable ranges", rows[(cqa, param)],
                                   table_title=PA_PAR_TABLE, table_id=f"{doc_id}_tab_par",
                                   table_header=rows.header)],
            metadata=meta()))
    return out


def pa_inventory(doc_id, file_name, dtype):
    return S.DocumentInventoryItem(
        document_id=doc_id, file_name=file_name, predicted_document_type=dtype,
        product_name_candidates=["A-Mab"], process_name_candidates=[PAUO_NAME],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "Protein A chromatography", "affinity capture",
                     "host-cell protein clearance", "design of experiments", "parameter classification"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc_id][0]}'.",
        source_references=[ref(doc_id, file_name, "Title block", "Title block",
                               title_block_quote(doc_id))],
        metadata=meta())


def build_plan_protein_a():
    doc, f = "PCP-005", PCP5_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_uo",
                                  process_steps=[pa_step(doc, f, f"{doc}_sec_uo", report=False)],
                                  equipment=pa_equipment(doc, f, f"{doc}_sec_uo", report=False),
                                  sites=pa_sites(doc, f, f"{doc}_sec_uo")),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=pa_cqas(doc, f, f"{doc}_sec_cqa", report=False)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=pa_params(doc, f, f"{doc}_sec_param", classified=False)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=pa_methods(doc, f, f"{doc}_sec_methods", report=False)),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Pool host cell protein is an in-process response with no step-level spec; captured via "
            "StudyDesign.responses. QualityAttribute.acceptance_criteria holds the drug-substance "
            "criterion, which the plan states is applied only as a conservative reference here.",
            "The Plan states classification is an OUTPUT; parameter_type left 'unclassified' here.",
        ],
        inventory=pa_inventory(doc, f, "process_characterization_plan"),
        entities=entities,
        studies=pa_studies(doc, f, report=False),
        report_sections=pa_report_sections(doc, f, report=False),
        assertions=pa_assertions(doc, f, report=False), concepts=pa_concepts())


def build_report_protein_a():
    doc, f = "PCR-005", PCR5_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_exec",
                                  process_steps=[pa_step(doc, f, f"{doc}_sec_exec", report=True)],
                                  equipment=pa_equipment(doc, f, f"{doc}_sec_exec", report=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=pa_params(doc, f, f"{doc}_sec_param", classified=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=pa_cqas(doc, f, f"{doc}_sec_cqa", report=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=pa_methods(doc, f, f"{doc}_sec_methods", report=True)),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT + [
            "ProvenAcceptableRange (new model) — per-response x parameter PAR (at-set-point / "
            "NOR-propagated), measured against the in-process limit for the pool where the "
            "drug-substance criterion does not apply at this step",
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "Pool host cell protein is an in-process response judged against an in-process limit "
            "carried back from the drug-substance limit through the CEX and AEX clearance; the "
            "train-wide position is deferred to PCR-007 / PCR-008 / PCMR-001.",
            "Leached Protein A is a robustness result, not a modelled response: no parameter is "
            "significant and the fitted surface is retained as knowledge-space evidence only. It is "
            "carried as a StudyDesign response and in report_sections, never as a predictive model.",
            "Process-capability (Cpk) values have no dedicated field; reported as report_sections statements.",
            "rhetorical_spans are verbatim report prose; the leached-Protein-A cluster (claim + "
            "statistical justifications + the bounded_conclusion that retains the model as "
            "knowledge-space evidence only) is the report's central argument; PCR-005 carries no "
            "weak_claims.",
        ],
        inventory=pa_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=pa_studies(doc, f, report=True),
        design_spaces=pa_design_spaces(doc, f),
        proven_acceptable_ranges=pa_proven_acceptable_ranges(doc, f),
        report_sections=pa_report_sections(doc, f, report=True),
        assertions=pa_assertions(doc, f, report=True), concepts=pa_concepts(),
        rhetorical_spans=build_rhetorical_spans(doc, f))


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
        "aggregates_hmw": ("Aggregate is of high criticality and is formed at this step and not "
                           "cleared by it"),
        "acidic_variants": ("Acidic charge variants are of very low criticality and are monitored "
                            "as a guard on acid exposure"),
    },
    True: {  # PCR-006
        "lrv_xmulv": "Enveloped-virus clearance is the attribute the step sets",
        "aggregates_hmw": ("the acid hold is a recognized source of both, and because a hold long "
                           "enough to guarantee clearance must be shown not to damage the product"),
        "acidic_variants": ("Aggregate is of high criticality and acidic variants of very low "
                            "criticality"),
    },
}

# Per-parameter grounded fragment from the report's "Parameter classification" section
# (the two WC-CPPs) and from the plan's "Risk-based prioritization of parameters".
VI_WCCPP_QUOTE = {
    "Hold time": ("Hold time is a well-controlled critical process parameter. It has the second "
                  "largest effect on clearance and it governs both aggregate and acidic variants"),
    "Temperature": ("Temperature is a well-controlled critical process parameter. Its effect on "
                    "clearance is real but the smallest of the three, and it also raises "
                    "aggregate."),
}
VI_PLAN_RANK_QUOTE = {
    "Inactivation pH": ("Inactivation pH ranks highest on both scales. It drives the inactivation "
                        "kinetics directly, it drives acid-induced aggregation directly"),
    "Hold time": ("Hold time and temperature act on the same kinetics as pH, which is where the "
                  "interaction risk lies"),
    "Temperature": "Temperature acts on aggregation as well, so it appears in both mechanisms.",
}

# Per-method grounded fragment from each document's "Analytical methods" section.
VIMETHOD_QUOTE = {
    False: {  # PCP-006
        "AMV-3017": "XMuLV infectivity will be measured as a TCID50 titre under AMV-3017",
        "AMV-3011": "Size variants will be measured by SEC under AMV-3011.",
        "AMV-3013": ("Charge variants will be measured by imaged capillary isoelectric focusing "
                     "under AMV-3013."),
    },
    True: {  # PCR-006
        "AMV-3017": "XMuLV infectivity was measured as a TCID50 titre under AMV-3017",
        "AMV-3011": "Aggregate was measured by SEC-HPLC under AMV-3011",
        "AMV-3013": "charge variants by icIEF under AMV-3013",
    },
}


def _vi_cqa_row(key):
    return P.cqa_reg[P.cqa_reg.key == key].iloc[0].to_dict()


def vi_step(doc_id, file_name, sec, report):
    if report:
        src = ref(doc_id, file_name, sec, "Executive summary",
                  "The Protein A eluate is titrated into an acidic hold, held for a defined time "
                  "under temperature control, and neutralized before it is loaded onto cation "
                  "exchange")
    else:
        src = ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                  "The step is a hold, and its position in the train is fixed by the pH of the "
                  "Protein A eluate")
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
                               "a scaled hold vessel operated under SOP-2009 and qualified under "
                               "SOP-1001" if report
                               else "The scale-down model is a jacketed hold vessel with overhead "
                                    "mixing")],
        metadata=meta())
    if report:
        return [sdm]
    return [
        S.Equipment(equipment_id="equip:vi_vessel",
                    equipment_name="commercial-scale low-pH inactivation vessel",
                    equipment_type="inactivation vessel", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec,
                                           "Scale-down model and its qualification",
                                           "matched to the commercial step on the variables that "
                                           "govern the outcome")],
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
    rats = {"CPP": "Largest effect on enveloped-virus clearance; a normal operating range only "
                   "0.2 pH units wide; robustness to co-variation of the other parameters is lost "
                   "before the top of the characterized range is reached; and an excursion cannot "
                   "be corrected once the hold has begun. The only CPP in the process.",
            "WC-CPP": "Linked to a critical quality attribute — it affects the log-reduction and "
                      "also governs aggregate — but it is measured continuously, can be corrected "
                      "before neutralization, and retains its whole characterization range as a "
                      "proven acceptable range under co-variation.",
            "GPP": "No mechanism links it to acid-mediated inactivation, and its normal operating "
                   "range is its entire characterization range, so it places no constraint on the "
                   "eluate delivered by Protein A."}
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
                                   "The screening study was a two-level full factorial in the "
                                   "three multivariate parameters" if report
                                   else "The screening design is a two-level full factorial in "
                                        "the multivariate factors")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vi_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=VIUO_NAME,
            factors=VI_MULTIVARIATE,
            responses=["xmulv_lrf", "aggregate_out_pct", "acidic_variants"],
            n_runs=n_rsm, n_center_points=P.doe_centre_points(VIUO, "rsm"), scale_down_model="scale-down inactivation model",
            associated_parameters=[VIPARAM_CONCEPT[f] for f in VI_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "The response-surface study was a face-centred central "
                                   "composite design in the same three factors" if report
                                   else "The response-surface design is a face-centred central "
                                        "composite in the same factors")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vi_sdm_qual", study_type="scale_down_qualification",
            unit_operation=VIUO_NAME, scale_down_model="scale-down inactivation model",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "Qualification compared the model with the at-scale step on "
                                   "input and output attributes measured by the same validated "
                                   "methods" if report
                                   else "Qualification will compare the model against at-scale "
                                        "platform records")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vi_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=VIUO_NAME,
            factors=VI_UNIVARIATE,
            responses=["xmulv_lrf", "aggregate_out_pct", "acidic_variants"],
            associated_parameters=[VIPARAM_CONCEPT[f] for f in VI_UNIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Univariate assessment",
                                   "A-Mab concentration was assessed one factor at a time" if report
                                   else "A-Mab concentration will be studied one factor at a time")],
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
        f"{VIUO_NAME} sets the cumulative XMuLV clearance.", "Quality attributes in scope",
        "Enveloped-virus clearance is the attribute the step sets" if report
        else "The step sets one critical quality attribute and puts two others at risk")
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
        "it is the only attribute in the table whose acceptance criterion is cumulative across "
        "the process" if report
        else "Enveloped virus clearance is cumulative across the process and is not delivered "
             "here alone")
    # parameter -> attribute impacts / non-impacts
    if report:
        add("param:vi_ph", "parameter_impacts_attribute", "attr:lrv_xmulv",
            "Inactivation pH has the largest effect on enveloped-virus clearance and is the only "
            "CPP in the drug substance process.",
            "Parameter classification",
            "Inactivation pH is a critical process parameter. It has the largest effect on "
            "enveloped-virus clearance")
        for name in VI_WCCPP:
            add(VIPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:lrv_xmulv",
                f"{name} affects the log-reduction and also governs aggregate (WC-CPP).",
                "Parameter classification", VI_WCCPP_QUOTE[name])
        add("param:vi_hold_time", "parameter_impacts_attribute", "attr:acidic_variants",
            "Acidic charge variants respond to hold time alone; the response carries no replicate "
            "variation, so its fit statistics are uninformative and lack of fit cannot be tested.",
            "Centre-point performance and reproducibility",
            "lack of fit can be tested for aggregate and for the log reduction factor but not for "
            "acidic variants")
        add("param:vi_ph", "parameter_does_not_significantly_impact_attribute", "attr:aggregates_hmw",
            "Inactivation pH had no detectable effect on aggregate over the characterized range; "
            "the null result is retained in the knowledge space as evidence of robustness.",
            "Screening: factor effects",
            "the onset was not reached, and pH is retained in the knowledge space for aggregate "
            "as evidence that the attribute is robust to it down to pH 3.2")
        add("param:vi_protein_conc", "parameter_does_not_significantly_impact_attribute", "attr:lrv_xmulv",
            "A-Mab concentration is a GPP: no mechanism links it to acid-mediated inactivation, "
            "and its normal operating range equals its characterization range.",
            "Parameter classification",
            "A-Mab concentration is a general process parameter. No mechanism links it to "
            "acid-mediated inactivation")
    else:
        for name in VI_MULTIVARIATE:
            add(VIPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:lrv_xmulv",
                f"{name} was ranked for multivariate study on its credible impact on the "
                f"enveloped-virus inactivation and its potential to interact.",
                "Risk-based prioritization of parameters", VI_PLAN_RANK_QUOTE[name])
        add("param:vi_protein_conc", "parameter_does_not_significantly_impact_attribute", "attr:lrv_xmulv",
            "A-Mab concentration is expected to affect neither response over a wide range.",
            "Risk-based prioritization of parameters",
            "Virus inactivation at fixed pH is a solution-phase reaction whose rate does not "
            "depend on the antibody concentration")
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def vi_report_sections(doc_id, file_name, report):
    from annex_contract.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-006 defines the process characterization study for the A-Mab low-pH viral "
                  "inactivation step (Step 6), written before any characterization data exist.",
               "Purpose and scope",
               "This plan defines the process characterization study for the step"),
            st(2, "Four process parameters are characterized; inactivation pH, hold time and "
                  "temperature are the multivariate factors and A-Mab concentration is univariate.",
               "Purpose and scope",
               "(inactivation pH, hold time and temperature) will be studied in a multivariate design"),
            st(3, "The study uses a full-factorial screen followed by a face-centred "
                  "central-composite design on a qualified scale-down hold model.",
               "Response-surface design",
               "The response-surface design is a face-centred central composite in the same factors"),
            st(4, "Low-pH inactivation is enveloped-virus specific; the parvovirus claim rests on "
                  "anion exchange and virus filtration instead.",
               "Purpose and scope",
               "Minute virus of mice is not inactivated at low pH, so this step is credited with "
               "enveloped virus clearance only, and the parvovirus claim rests on anion exchange "
               "and virus filtration"),
            st(5, "The enveloped-virus acceptance criterion for this step is a back-calculated "
                  "step contribution, not the cumulative drug-substance requirement.",
               "Acceptance and decision criteria",
               "The enveloped virus criterion is a step contribution and not a cumulative figure."),
            st(6, "The clearance claim will be framed conservatively, from the worst case of the "
                  "operating region rather than the mean at the set-point.",
               "Acceptance and decision criteria",
               "The claim made for the step will be the reduction demonstrated at the worst case "
               "of the operating region"),
            st(7, "The operating region must satisfy every response criterion at the same time, "
                  "evaluated from the fitted models with the other parameters varying within "
                  "their normal operating ranges.",
               "Acceptance and decision criteria",
               "It will be evaluated from the fitted response-surface models with the remaining "
               "parameters varying within their normal operating ranges, and not from the mean "
               "prediction alone"),
            st(8, "The pH criterion is two-sided and decisive for this step: its upper edge is set "
                  "by the log-reduction criterion and its lower edge by the aggregate criterion.",
               "Acceptance and decision criteria",
               "The pH criterion is two-sided, and it is the decisive one for this step"),
            st(9, "Proven acceptable ranges will be reported in two forms, and the analysis that "
                  "propagates the other parameters across their normal operating ranges is the "
                  "reported default.",
               "Proven acceptable ranges (planned analysis)",
               "which makes it the reported default, because it is the condition under which the "
               "step will actually be operated"),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Inactivation pH is classified as a critical process parameter and is the only one "
              "so classified in the A-Mab drug substance process.",
           "Executive summary",
           "Inactivation pH is classified as a critical process parameter, and it is the only "
           "parameter in the drug substance process to carry that classification"),
        st(2, "The response-surface models — not the screening model — are the predictive models "
              "behind the operating region, the proven acceptable ranges and the capability "
              "assessment.",
           "Response-surface models",
           "The response-surface models are adequate for aggregate and for the XMuLV log reduction "
           "factor, and they are the models used for the operating region, the proven acceptable "
           "ranges and the capability assessment"),
        st(3, "The pH dependence of clearance is strongly asymmetric about the set-point: almost "
              "all of the step's sensitivity to pH lies above it.",
           "Mechanistic interpretation",
           "Almost all of the sensitivity of the step to pH lies above the set-point."),
        st(4, "At the worst corner of the characterized ranges the shortfall against the required "
              "step contribution is smaller than the model's residual standard error, so it is "
              "reported as an absence of assurance and not a demonstrated failure.",
           "Design space",
           "the corner is not shown to fail so much as shown to provide no assurance of passing, "
           "and it lies outside the operating region for that reason"),
        st(5, "Exactly one proven acceptable range is narrower than its characterization range — "
              "inactivation pH against the log reduction factor, under co-variation of the other "
              "parameters within their normal operating ranges.",
           "Proven acceptable ranges", "One further entry is narrower than its characterized range."),
        st(6, "Cumulative enveloped-virus clearance is the tightest of the three capabilities the "
              "step influences.",
           "Process capability and robustness",
           "Enveloped-virus clearance is the tightest of the three by a wide margin."),
        st(7, "The low-pH hold supplies the largest single contribution to enveloped-virus "
              "clearance and none of the parvovirus clearance.",
           "Process capability and robustness",
           "The low-pH hold supplies the largest single contribution to enveloped-virus clearance "
           "and none of the parvovirus clearance"),
        st(8, "The step is credited with no parvovirus clearance and no host-cell-protein "
              "clearance.",
           "Conclusions",
           "It is credited with no parvovirus clearance and no host cell protein clearance"),
        st(9, "Acidic variants returned no replicate variation, so lack of fit is testable for "
              "aggregate and for the log reduction factor but not for that response.",
           "Centre-point performance and reproducibility",
           "lack of fit can be tested for aggregate and for the log reduction factor but not for "
           "acidic variants"),
        st(10, "The lower pH edge is a platform stability boundary inherited from prior products "
               "and was not demonstrated in this study, so the two-sided pH constraint is "
               "demonstrated on one side only.",
            "Discussion",
            "The lower edge of the pH range is a platform boundary rather than a demonstrated one, "
            "so the two-sided character of the pH constraint is demonstrated on one side and "
            "inherited on the other"),
    ])]


def vi_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:viral_inactivation", unit_operation=VIUO_NAME,
        parameters=["param:vi_ph", "param:vi_hold_time", "param:vi_temperature"],
        quality_attributes_constrained=["attr:lrv_xmulv", "attr:aggregates_hmw"],
        definition="The set of combinations of inactivation pH, hold time and temperature at which "
                   "the response-surface model predicts a step log-reduction factor at or above "
                   "the back-calculated step contribution and pool aggregate at or below the "
                   "drug-substance limit. The aggregate constraint is never binding inside the "
                   "characterized ranges, so the region is set by the clearance constraint alone "
                   "and its principal plane is pH against hold time. The single excluded corner is "
                   "the highest pH with the shortest hold at the lowest temperature, where the "
                   "prediction falls marginally below the floor by less than the model's residual "
                   "standard error.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "The region is therefore defined by the clearance constraint alone, "
                               "and its principal plane is pH against hold time")],
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
            "this study predicts the set-point value independently and the report reconciles the "
            "two within the residual standard error.",
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
                  "The same resin and buffer system are used across the Novacyte humanized IgG1 "
                  "platform, on which three licensed antibodies (X-Mab, Y-Mab and Z-Mab) have "
                  "been manufactured in the same elution mode")
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
                               "All characterization runs were performed in a qualified "
                               "scale-down model of the commercial cation exchange step" if report
                               else "The model holds the bed height, the linear flow velocity, "
                                    "the protein load per litre of resin and the load, wash and "
                                    "elution volumes in column volumes at the commercial values")],
        metadata=meta())
    if report:
        return [sdm]
    return [
        S.Equipment(equipment_id="equip:cex_column",
                    equipment_name="commercial-scale cation-exchange polishing column",
                    equipment_type="chromatography column", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec,
                                           "Scale-down model and its qualification",
                                           "A scale-down chromatography system will be "
                                           "qualified as a model of the commercial cation "
                                           "exchange step before any characterization run is "
                                           "executed")],
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
        "AMV-3011": ("Size variants, including the aggregate response, are measured by size "
                     "exclusion chromatography under AMV-3011"),
        "AMV-3012": "host cell protein by ELISA under AMV-3012",
        "AMV-3014": "residual DNA by quantitative PCR under AMV-3014",
        "AMV-3016": "leached Protein A by ELISA under AMV-3016",
    },
    True: {  # PCR-007
        "AMV-3011": ("Pool aggregate was measured as high molecular weight species by "
                     "size-exclusion chromatography (SEC-HPLC) under AMV-3011"),
        "AMV-3012": "host cell protein by immunoassay (ELISA) under AMV-3012",
        "AMV-3014": ("residual DNA by quantitative polymerase chain reaction (qPCR) under "
                     "AMV-3014"),
        "AMV-3016": "leached Protein A by immunoassay under AMV-3016",
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
                                   "The screening design was a two-level full factorial in the "
                                   "four multivariate factors" if report
                                   else "Every main effect and every two-factor interaction is "
                                        "therefore estimable without aliasing, as the interaction "
                                        "ranking in §4.3 requires")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:cex_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=CXUO_NAME,
            factors=CX_MULTIVARIATE, responses=responses,
            n_runs=n_rsm, n_center_points=P.doe_centre_points(CXUO, "rsm"), scale_down_model="scale-down chromatography column",
            associated_parameters=[CXPARAM_CONCEPT[f] for f in CX_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "The response-surface design was a face-centred central "
                                   "composite design in the same four factors" if report
                                   else "The parameters carried forward from screening enter a "
                                        "face-centred central composite design of")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:cex_sdm_qual", study_type="scale_down_qualification",
            unit_operation=CXUO_NAME, scale_down_model="scale-down chromatography column",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "Qualification of the model rests on the agreement of its "
                                   "output attributes with the commercial-scale process at "
                                   "equivalent operating conditions" if report
                                   else "column efficiency will be verified by plate count and "
                                        "peak asymmetry under "
                                        "SOP-1001")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:cex_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=CXUO_NAME,
            factors=CX_UNIVARIATE, responses=["step yield", "pool aggregate", "pool HCP"],
            associated_parameters=[CXPARAM_CONCEPT[f] for f in CX_UNIVARIATE],
            source_references=[ref(doc_id, file_name, "Study design", "Univariate assessment",
                                   "The elution flow rate was assessed univariately across its "
                                   "characterization range" if report
                                   else "That design therefore supports a proven acceptable "
                                        "range for flow rate at the set-points of the other four "
                                        "parameters only")],
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
        "Aggregate is the attribute for which this step is the last opportunity" if report
        else "Because no later step of the train reduces aggregate, the content of the pool "
             "carries through to the drug substance")
    cleared_quote = ("each of which enters the step from an upstream operation and leaves it "
                     "reduced" if report else
                     "attributes in scope are formed upstream and are only reduced here")
    for key in ["hcp", "residual_dna", "leached_protein_a"]:
        add("step:cex", "step_has_quality_attribute", CXATTR_CONCEPT[key],
            f"{CXUO_NAME} clears {CXATTR_NAME[key]} (formed upstream; not set here).",
            "Quality attributes in scope", cleared_quote)
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
        (f"Aggregate acceptance: {agg['acc_low']:g}–{agg['acc_high']:g} {agg['unit']}, applied "
         f"directly to this pool." if report else
         f"Aggregate acceptance: {agg['acc_low']:g}–{agg['acc_high']:g} {agg['unit']} at drug "
         f"substance; no later step of the train reduces aggregate, so the pool criterion is "
         f"carried back from it."),
        "Quality attributes in scope" if report else "Acceptance and decision criteria",
        "with their drug substance acceptance criteria and criticality" if report
        else "The aggregate criterion is derived differently, because no later step of the train "
             "reduces the level once the pool has been collected")
    # parameter -> attribute impacts / non-impacts
    if report:
        add("param:cex_load", "parameter_impacts_attribute", "attr:aggregates_hmw",
            "Protein load has the largest effect on pool aggregate and the second largest on "
            "pool host cell protein (WC-CPP).",
            "Parameter classification",
            "It has the largest effect on pool aggregate, which is the attribute this step "
            "carries, and the second largest on pool host cell protein")
        add("param:cex_wash_cond", "parameter_impacts_attribute", "attr:hcp",
            "Load/wash conductivity governs pool host cell protein and has no detectable effect "
            "on pool aggregate (WC-CPP).",
            "Parameter classification",
            "It governs pool host cell protein and has no detectable effect on pool aggregate")
        add("param:cex_elution_ph", "parameter_impacts_attribute", "attr:aggregates_hmw",
            "Elution buffer pH has the second largest effect on pool aggregate and interacts with "
            "protein load (WC-CPP).",
            "Parameter classification",
            "It has the second largest effect on pool aggregate and it interacts with protein load")
        add("param:cex_stop_collect", "parameter_impacts_attribute", "attr:aggregates_hmw",
            "The stop collect criterion affects pool aggregate through how much of the descending "
            "edge enters the pool (WC-CPP).",
            "Parameter classification",
            "It affects pool aggregate through how much of the descending edge enters the pool")
        add("param:cex_wash_cond", "parameter_does_not_significantly_impact_attribute",
            "attr:aggregates_hmw",
            "Load/wash conductivity has no detectable effect on pool aggregate; the null result is "
            "retained in the knowledge space.",
            "Parameter classification",
            "Load and wash conductivity has no effect on pool aggregate")
        add("param:cex_flow", "parameter_does_not_significantly_impact_attribute",
            "attr:aggregates_hmw",
            "Elution flow rate showed no effect on any governed attribute across its "
            "characterization range (GPP).",
            "Parameter classification",
            "The univariate assessment found no effect on any governed attribute across its "
            "characterization range")
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
            "because flow rate acts through two mechanisms alone, residence time and peak "
            "sharpness")
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
               "The scope of this plan runs from the load of the neutralized viral inactivation "
               "pool to the end of eluate collection"),
            st(2, "Five process parameters are characterized; four are assigned to the multivariate "
                  "design and the elution flow rate to univariate assessment.",
               "Risk-based prioritization of parameters",
               "Elution flow rate was assigned to the univariate group"),
            st(3, "The study uses a full-factorial screen followed by a face-centred central-composite "
                  "design on a scale-down column.",
               "Response-surface design",
               "The parameters carried forward from screening enter a face-centred central "
               "composite design of"),
            # Re-anchored 2026-08-18. The re-authored plan calls the step the "aggregate polishing
            # step" and makes the clearance point through the attribute register rather than in one
            # sentence of the scope, so the statement is carried by the sentence that does the work:
            # aggregate cannot be recovered downstream.
            st(4, "Cation exchange is the aggregate polishing step of the train, and the aggregate "
                  "content of its pool sets the aggregate content of the drug substance.",
               "Purpose and scope",
               "Pool purity cannot be recovered downstream, because no later step of the "
               "purification train reduces aggregate"),
            # Rewritten 2026-08-18. The previous statement said pool aggregate is judged against the
            # DRUG-SUBSTANCE limit at this step. The re-authored plan gives aggregate a POOL
            # criterion too: it carries the drug-substance criterion through unchanged and leaves
            # the assurance margin to cover the whole difference. Both attributes now have a pool
            # criterion, derived two different ways, and the statement says so.
            st(5, "Both governed attributes are judged against a pool criterion rather than a "
                  "drug-substance criterion: host cell protein because anion exchange still "
                  "reduces it, aggregate because no later step does.",
               "Acceptance and decision criteria",
               "The pool is an intermediate and cannot be judged against a drug-substance "
               "criterion where later steps still reduce the attribute"),
            # Rewritten 2026-08-18. The previous statement said an above-limit pool "constrains
            # anion exchange and is reconciled in PCMR-001". The re-authored plan does not say
            # that -- it neither uses the word reconcile nor makes PCMR-001 the place the two steps
            # meet. What it does say about the host cell protein pool criterion is why the margin
            # is there, which is the claim the statement now carries.
            st(6, "The host cell protein pool criterion carries an assurance margin, so it works "
                  "as an in-process control rather than as a break-even point that would require "
                  "every later step to deliver nominal clearance exactly.",
               "Acceptance and decision criteria",
               "because the margin holds it above the value at which the drug substance would "
               "depend on every later step delivering nominal clearance exactly"),
            # Replaced 2026-08-18. The previous statement described a worst-case aggregate
            # challenge run separately from the designed experiments. The re-authored plan has no
            # such section and does not contain the word "worst" anywhere, so the statement is
            # replaced by the decision rule the plan does state for a model that fails.
            st(7, "A response whose model fails any of the four acceptance conditions is reported "
                  "without a design space claim, and the parameters governing it are held at their "
                  "normal operating ranges.",
               "Acceptance and decision criteria",
               "Where a model fails any of the four conditions, the response will be reported "
               "without a design space claim"),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "All four multivariate parameters are well-controlled CPPs and the elution flow rate is "
              "a general process parameter; no CPP and no KPP is assigned at this step.",
           "Parameter classification",
           "All 4 quality-linked parameters are well controlled, and the one remaining parameter "
           "(the elution flow rate) is a general process parameter"),
        st(2, "The aggregate capability belongs to the cation exchange step alone, because no other "
              "step in the train changes the attribute.",
           "Process capability and robustness",
           "This capability belongs to the cation exchange step alone, because no other step in the "
           "train changes the attribute"),
        st(3, "Pool host cell protein is governed by the load and wash conductivity and by protein "
              "load, acting in opposite directions and through their interaction.",
           "Screening: factor effects",
           "Pool host cell protein is affected by the conductivity of the load and wash buffer, by "
           "protein load, and by the interaction between them"),
        st(4, "The pool-aggregate and pool-HCP response-surface models keep their accuracy on data "
              "they have not seen, and both are used for prediction on that basis.",
           "Response-surface models",
           "both models are used for prediction in this report on that basis"),
        st(5, "No response shows significant curvature over the ranges studied, so the fitted surfaces "
              "are planes with an interaction twist and there is no edge of failure inside the region.",
           "Response-surface models",
           "No quadratic term is significant for any of the three responses"),
        st(6, "The step yield model is not predictive and is used only for the direction and the "
              "approximate size of the protein-load effect.",
           "Discussion",
           "which is too low for the model to be used for prediction at a stated condition"),
        st(7, "Pool host cell protein above the drug-substance criterion is the correct result for an "
              "intermediate and is not a failed acceptance criterion; the step is judged on its "
              "clearance factor.",
           "Proven acceptable ranges",
           "That corner is therefore outside the operating region this step claims"),
        st(8, "The further host cell protein clearance is credited to anion exchange in PCR-008 and "
              "the cumulative position across the train is consolidated in PCMR-001.",
           "Executive summary",
           "the cumulative position across the train is consolidated in PCMR-001"),
        st(9, "Aggregate meets its drug-substance criterion at commercial scale and this step carries "
              "that attribute alone.",
           "Conclusions", "and this step carries that attribute alone"),
        st(10, "Two deviations were recorded and both were dispositioned as retained, with no effect "
               "on any fitted model, operating-region boundary or classification.",
            "Deviations from the plan",
            "Both were dispositioned as retained, which means the affected run stayed in the analysis "
            "rather than being excluded or repeated"),
    ])]


def cx_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:cex", unit_operation=CXUO_NAME,
        parameters=["param:cex_load", "param:cex_wash_cond", "param:cex_elution_ph",
                    "param:cex_stop_collect"],
        quality_attributes_constrained=["attr:aggregates_hmw"],
        definition="The part of the characterized four-dimensional region in protein load, "
                   "load/wash conductivity, elution buffer pH and the stop collect criterion in "
                   "which both governed attributes stay within their in-process limits. Aggregate "
                   "is the governing attribute, and its worst corner (all four parameters at their "
                   "upper edges) lies outside the region: it is below the drug-substance limit but "
                   "above the in-process limit, which is that limit divided by an assurance margin "
                   "because no downstream step removes aggregate. Pool host cell protein is judged "
                   "against a limit carried back from the drug-substance criterion through the "
                   "anion-exchange clearance.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "The design space for this step is the part of the characterized "
                               "four-dimensional region in which both governed attributes stay "
                               "within their in-process limits")],
        metadata=meta())]


# --------------------------------------------------------------------------- #
# Report-only PAR / discourse layers (PCR-007 only).                            #
# --------------------------------------------------------------------------- #
# proven_acceptable_ranges derive from the same DoE engine that renders @tbl-par  #
# (doe_report.par_table). Aggregate is proven acceptable across every full         #
# characterization range; pool HCP returns "none (set-point breaches)" against the #
# drug-substance criterion, which the report narrates as the correct result for an #
# intermediate — the step is judged on its clearance factor and on the step-level  #
# ceiling derived from the anion-exchange clearance factor (PCR-008). PCR-007       #
# carries NO weak_claims. These layers are report-only; the plan omits them.        #
# --------------------------------------------------------------------------- #
CX_PAR_SEC = "Proven acceptable ranges"
CX_PAR_QUOTE = {
    "Aggregates (HMW, %)": ("For aggregate the two analyses separate, and the separation is the "
                            "informative part"),
    "Pool HCP (ng/mg)": ("For host cell protein the analysis returns a range for every parameter"),
}
_CX_PAR_GENERAL_QUOTE = ("the criterion applied to each is the in-process limit for this "
                         "step rather than the criterion the drug substance itself must meet")


def cx_proven_acceptable_ranges(doc_id, file_name):
    """One ProvenAcceptableRange per governed response x response-surface parameter, from the
    same DoE engine (``doe_report.par_table``) that renders @tbl-par in the report. Both
    responses use a drug-substance specification as the acceptance basis — this step has no
    viral-clearance response, so nothing is back-calculated from a cumulative requirement.
    For pool HCP the drug-substance criterion does not apply to the intermediate, so the
    analysis returns no interval; the basis records why that is the expected result."""
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
        hcp = "HCP" in cqa
        basis = (
            "Drug-substance host-cell-protein specification, applied as the upper acceptance "
            "limit. It is not a step criterion: the cation-exchange pool is an intermediate, so "
            "the predicted pool level sits above it across the whole region and no interval is "
            "returned. The step is judged instead on its clearance factor and on the step-level "
            "ceiling back-calculated from the anion-exchange clearance factor (PCR-008); on that "
            "basis every characterized range is acceptable."
            if hcp else
            "Drug-substance aggregate specification, applied as the upper acceptance limit "
            "directly to this pool, because no downstream operation reduces aggregate.")
        out.append(S.ProvenAcceptableRange(
            par_id=f"{doc_id}-PAR{i:02d}", unit_operation=CXUO_NAME,
            quality_attribute=cqa, parameter=param,
            characterization_range=char,
            par_at_setpoint=f"{r['PAR (set-point)']} {unit}".strip() if not hcp
            else r["PAR (set-point)"],
            par_nor_propagated=f"{r['PAR (NOR)']} {unit}".strip() if not hcp
            else r["PAR (NOR)"],
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
            "Pool aggregate and pool HCP are in-process responses with no released spec; reported via studies/report_sections. Aggregate is the exception that binds here: CEX is the last aggregate-reduction step, so the DS limit applies directly to this pool and the step carries it alone.",
            "Pool HCP is an in-process value, not a failed criterion. The PAR analysis returns no interval against the DS criterion because the pool is an intermediate; the step is judged on its 78-fold clearance factor and on a step-level ceiling back-calculated from the AEX clearance factor. The further AEX clearance is credited to PCR-008 and the cumulative position to PCMR-001.",
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
                  "Anion exchange chromatography (AEX) is the final purification step in the "
                  "A-Mab drug substance process")
    else:
        src = ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                  "Anion exchange chromatography is the final purification step in the A-Mab "
                  "downstream process")
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
                               "A laboratory-scale chromatography system was qualified as a model "
                               "of the commercial step" if report
                               else "The study will be run on a laboratory scale-down model (SDM)")],
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
    rats = {"WC-CPP": "Either linked to a critical quality attribute or bounds the conditions "
                      "under which the viral-clearance claim is made; low risk of leaving the "
                      "design space, since the region is wide relative to the control capability "
                      "of the equipment."}
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
    False: "Quality attribute set by this step, with its acceptance criterion.",
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
        "AMV-3014": "residual DNA by qPCR (AMV-3014)",
        "AMV-3016": "leached Protein A by ELISA (AMV-3016)",
        # Both viral methods are named in one sentence; each takes the shortest contiguous
        # slice of it that names itself (see CQA_METHOD_QUOTE for the same treatment).
        "AMV-3017": ("Retrovirus and parvovirus titres will be measured by infectivity assay in "
                     "the containment laboratory (AMV-3017"),
        "AMV-3018": "the containment laboratory (AMV-3017 and AMV-3018)",
    },
    True: {  # PCR-008
        "AMV-3012": ("Pool HCP was measured by the process-specific enzyme-linked immunosorbent "
                     "assay validated under AMV-3012"),
        "AMV-3014": "residual DNA by quantitative polymerase chain reaction (AMV-3014)",
        "AMV-3016": "leached Protein A by enzyme-linked immunosorbent assay (AMV-3016)",
        "AMV-3017": ("infectivity titres for XMuLV and MVM were determined under AMV-3017 and "
                     "AMV-3018 respectively"),
        "AMV-3018": ("infectivity titres for XMuLV and MVM were determined under AMV-3017 and "
                     "AMV-3018 respectively"),
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
                                   "The design estimates all main effects and all two-factor "
                                   "interactions" if report
                                   else "A full factorial was chosen over a fractional design")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:aex_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=AXUO_NAME,
            factors=AX_MULTIVARIATE, responses=responses,
            n_runs=n_rsm, n_center_points=P.doe_centre_points(AXUO, "rsm"), scale_down_model="scale-down chromatography column",
            associated_parameters=[AXPARAM_CONCEPT[f] for f in AX_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "The axial points sit on the faces of the cube, so the design "
                                   "stays inside the characterized ranges" if report
                                   else "face-centred central composite design (CCD)")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:aex_sdm_qual", study_type="scale_down_qualification",
            unit_operation=AXUO_NAME, scale_down_model="scale-down chromatography column",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "Qualification compared the laboratory model with "
                                   "commercial-scale batch data on the input and output attributes "
                                   "of the step" if report
                                   else "Qualification will compare the model against at-scale data "
                                        "from A-Mab clinical manufacture")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:aex_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=AXUO_NAME,
            factors=AX_UNIVARIATE,
            responses=["flow-through-pool HCP", "XMuLV log-reduction", "MVM log-reduction", "step yield"],
            associated_parameters=[AXPARAM_CONCEPT[f] for f in AX_UNIVARIATE],
            source_references=[ref(doc_id, file_name, "Study design", "Univariate assessment",
                                   "Operating flow rate was assessed one factor at a time across "
                                   "its characterized range" if report
                                   else "Operating flow rate will be assessed one factor at a time")],
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
        "Quality attributes in scope",
        "The step sets one critical quality attribute (CQA)" if report
        else "This step sets one quality attribute")
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
        "its acceptance criterion is cumulative across the process and expressed as a log "
        "reduction factor" if report
        else "Quality attribute set by this step, with its acceptance criterion.")
    # parameter -> attribute relations. In the requalified execution only the three
    # chemistry parameters are active; protein load and flow rate are null results and
    # are WC-CPP on bounding logic, so they carry a "does not significantly impact" edge.
    if report:
        add("param:aex_load_ph", "parameter_impacts_attribute", "attr:lrv_mvm",
            "Load pH has the largest effect on both viral-clearance responses and the second "
            "largest on pool HCP (WC-CPP).",
            "Parameter classification",
            "Load pH is a WC-CPP because it has the largest effect on both viral clearance responses")
        add("param:aex_wash1_cond", "parameter_impacts_attribute", "attr:hcp",
            "Equil/Wash-1 conductivity is the governing parameter for pool HCP and interacts with "
            "load pH (WC-CPP).",
            "Parameter classification",
            "Equilibration and wash-1 conductivity is a WC-CPP because it is the governing "
            "parameter for pool HCP and interacts with load pH")
        add("param:aex_load_cond", "parameter_impacts_attribute", "attr:lrv_mvm",
            "Load conductivity carries the second largest effect on both clearance responses and "
            "defines one axis of the viral-clearance constraint (WC-CPP).",
            "Parameter classification",
            "Load conductivity is a WC-CPP because it is the second largest effect on both "
            "clearance responses")
        add("param:aex_load", "parameter_does_not_significantly_impact_attribute", "attr:hcp",
            "Protein load had no significant effect on any response over the characterized range; "
            "it is classified WC-CPP because the viral-clearance claim is bounded by the maximum "
            "load at which clearance was demonstrated, not because an effect was measured.",
            "Screening: factor effects", "Protein load is inactive on every response")
        add("param:aex_flow", "parameter_does_not_significantly_impact_attribute", "attr:lrv_mvm",
            "Operating flow rate showed no effect in the univariate assessment; it is classified "
            "WC-CPP on the same bounding logic, since the spiking runs supporting the clearance "
            "claim were executed at the maximum flow rate.",
            "Parameter classification",
            "Operating flow rate is a WC-CPP on the same bounding logic, since it showed no effect "
            "in the univariate assessment across its characterized range")
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
            "Flow rate acts on this step through residence time")
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
               "This plan defines the process characterization study for anion exchange chromatography"),
            st(2, "Five process parameters are characterized; four are studied in the multivariate DoE and the flow rate univariately.",
               "Factors, ranges and study type",
               "The parameters to be studied, their set-points, their characterization ranges and "
               "their normal operating ranges are given in"),
            st(3, "The study uses a full-factorial screen followed by a face-centred central-composite design on a scale-down column.",
               "Response-surface design", "face-centred central composite design (CCD)"),
            st(4, "Anion exchange sets the cumulative parvovirus (MVM) clearance claim and also governs XMuLV clearance, HCP, residual DNA and leached Protein A.",
               "Quality attributes in scope", "This step sets one quality attribute"),
            st(5, "The study must establish a multivariate operating region over which every governed response is predicted to stay within its acceptance criterion.",
               "Acceptance and decision criteria",
               "The operating region will be declared as the multivariate set of parameter settings "
               "over which every governed response is predicted by the response-surface model to "
               "stay within its acceptance criterion"),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Every characterized parameter is classified as a well-controlled critical process "
              "parameter; no CPP, KPP or GPP is assigned at this step.",
           "Parameter classification",
           "classified as well-controlled critical process parameters under SOP-4001, because each "
           "of them is either linked to a critical quality attribute or bounds the conditions under "
           "which a clearance claim is made"),
        st(2, "Anion exchange and small-virus retentive filtration are the only two steps credited "
              "with MVM clearance, and anion exchange is the step that sets the cumulative claim.",
           "Quality attributes in scope",
           "Anion exchange and small-virus retentive filtration are the only two steps credited "
           "with MVM clearance"),
        st(3, "Pool HCP is governed by equilibration/wash-1 conductivity and load pH acting in "
              "opposite directions, together with a significant interaction between them.",
           "Screening: factor effects", "Pool HCP is governed by two factors and by their interaction"),
        st(4, "The pool-HCP, XMuLV-clearance and MVM-clearance response-surface models are adequate "
              "and are the basis of the operating region.",
           "Response-surface models",
           "The response-surface models are adequate for the three quality responses and are the "
           "basis of the operating region"),
        st(5, "The protein-load main effect and the protein-load x wash-conductivity interaction "
              "seen in the invalidated first execution are absent from the requalified data, which "
              "confirms the DEV-008-01 root cause.",
           "Non-representative load material in the first execution",
           "Both terms are absent from the requalified data, which is the result the deamidation "
           "mechanism predicts and which confirms the root cause"),
        st(6, "Three deviations were recorded, investigated and resolved; none altered a parameter "
              "classification or a boundary of the operating region.",
           "Conclusions",
           "Three deviations were recorded, investigated and resolved, one of which invalidated the "
           "first execution of both designs"),
        st(7, "The cumulative MVM clearance claim carries the tightest process-capability index of "
              "any attribute in the drug substance process.",
           "Process capability and robustness",
           "The MVM clearance claim carries the tightest capability in the table and in the whole "
           "drug substance process"),
    ])]


def ax_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:aex", unit_operation=AXUO_NAME,
        parameters=["param:aex_load_ph", "param:aex_load_cond", "param:aex_wash1_cond"],
        quality_attributes_constrained=["attr:lrv_mvm", "attr:lrv_xmulv", "attr:hcp"],
        definition="The intersection of two multivariate constraints: a viral-clearance constraint "
                   "set by load pH and load conductivity, and a pool-purity constraint set by load "
                   "pH and equilibration/wash-1 conductivity. Protein load and operating flow rate "
                   "are free within their characterized ranges. MVM clearance is the binding "
                   "attribute; the worst-case corner is low load pH with high load conductivity.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "The operating region for the anion exchange step is the "
                               "intersection of two multivariate constraints")],
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
                  "the dedicated size-based virus removal step of the A-Mab drug-substance process")
    else:
        src = ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                  "Small-virus retentive filtration is the last purification operation before "
                  "formulation, and its only purpose is virus removal")
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
                               "generated on a scale-down model of the commercial filtration step, "
                               "qualified under SOP-1001" if report
                               else "The study depends on a small-scale model that behaves like the "
                                    "commercial device")],
        metadata=meta())
    if report:
        return [sdm]
    return [
        S.Equipment(equipment_id="equip:vf_filter",
                    equipment_name="commercial-scale small-virus retentive filter",
                    equipment_type="virus-retentive filter", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec,
                                           "Scale-down model and its qualification",
                                           "the same filter construction and the same lot family as "
                                           "the commercial device")],
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
        "AMV-3018": "MVM is titrated by TCID50 with quantitative PCR confirmation under AMV-3018",
        "AMV-3017": "XMuLV is titrated by TCID50 under AMV-3017",
    },
    True: {  # PCR-009
        "AMV-3018": ("MVM titre was determined under AMV-3018 by a fifty per cent tissue culture "
                     "infectious dose assay"),
        "AMV-3017": ("XMuLV titre under AMV-3017 by a fifty per cent tissue culture infectious "
                     "dose assay"),
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
                                   "The screening study was a two-level full factorial in both "
                                   "parameters" if report
                                   else "The screening design is a two-level full factorial in the "
                                        "two factors")],
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
                                   else "a face-centred central composite design in the same two "
                                        "factors")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vf_sdm_qual", study_type="scale_down_qualification",
            unit_operation=VFUO_NAME, scale_down_model="scale-down filtration model",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "Qualification compared unspiked small-scale runs at the "
                                   "set-point with at-scale performance" if report
                                   else "will compare the scale-down device with commercial-scale "
                                        "batches at the centre condition")],
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
        "it is the principal contributor to the minute virus of mice (MVM) clearance claim" if report
        else "It provides the largest single MVM reduction in the train and a substantial XMuLV "
             "reduction")
    add("step:virus_filtration", "step_has_quality_attribute", "attr:lrv_xmulv",
        f"{VFUO_NAME} is a major clearance step for enveloped virus (XMuLV).",
        "Product and unit operation" if report else "Unit-operation description and prior knowledge",
        "XMuLV (xenotropic murine leukaemia virus) is a large enveloped retrovirus model and is "
        "retained with a wide size margin" if report
        else "XMuLV is retained with a wide margin at every load examined")
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
        "The acceptance criteria in Table 4 are cumulative and apply to the whole process." if report
        else "Their acceptance criteria apply to the purification train as a whole and not to any "
             "single step")
    # parameter -> attribute impacts / non-impacts
    if report:
        add("param:vf_filtration_volume", "parameter_impacts_attribute", "attr:lrv_mvm",
            "Volumetric load has a demonstrated effect on MVM clearance — the only effect resolved "
            "at this step — so it is quality-linked and classified WC-CPP.",
            "Parameter classification",
            "Filtration volume, expressed as load per unit membrane area, is a WC-CPP. It has a "
            "demonstrated effect on MVM clearance")
        add("param:vf_pressure", "parameter_does_not_significantly_impact_attribute", "attr:lrv_mvm",
            "No effect of filtration pressure was resolved on any of the three responses; it is "
            "classified WC-CPP on bounding logic, because ICH Q5A(R2) ties the clearance claim to "
            "the conditions under which it was demonstrated.",
            "Parameter classification", "No effect of pressure was resolved on any of the three responses")
    else:
        for name in VF_MULTIVARIATE:
            add(VFPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:lrv_mvm",
                f"{name} was ranked high enough in RA-001 to require multivariate evaluation of its "
                f"potential effect on the credited viral log-reduction.",
                "Risk-based prioritization of parameters",
                "Two parameters were ranked high enough to require multivariate evaluation, the "
                "volumetric load and the filtration pressure")
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def vf_report_sections(doc_id, file_name, report):
    from annex_contract.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-009 defines the characterization study that will bound the operating ranges "
                  "of the A-Mab small-virus retentive filtration step (Step 9).",
               "Purpose and scope",
               "this plan defines the characterization study that will bound its operating ranges"),
            st(2, "Two process parameters (volumetric load and filtration pressure) are characterized "
                  "in a compact two-factor multivariate design.",
               "Factors, ranges and study type",
               "The design covers the two parameters that RA-001 assigned to multivariate study"),
            st(3, "The study uses a two-factor full-factorial screen followed by a face-centred "
                  "central composite design on a scale-down filtration model.",
               "Response-surface design",
               "a face-centred central composite design in the same two factors"),
            st(4, "Virus filtration provides the largest single MVM reduction in the train and a "
                  "substantial XMuLV reduction.",
               "Unit-operation description and prior knowledge",
               "It provides the largest single MVM reduction in the train and a substantial XMuLV "
               "reduction"),
            st(5, "The study must establish the maximum volumetric load at which the back-calculated "
                  "step-level MVM criterion is still met, capped at the upper edge of the "
                  "characterized range.",
               "Load limit and operating region",
               "The maximum volumetric load carried into the control strategy will be the largest "
               "load at which the MVM criterion is met under that analysis"),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Both process parameters (volumetric load and filtration pressure) are well-controlled "
              "CPPs; the step carries no CPP and no key process parameter.",
           "Executive summary",
           "Both parameters are classified as well-controlled critical process parameters (WC-CPP), "
           "and the step carries no CPP and no key process parameter"),
        st(2, "MVM (parvovirus) clearance falls as the volumetric load on the membrane rises, and "
              "volumetric load is the only effect the study resolved.",
           "Executive summary", "MVM clearance falls as the volumetric load on the membrane rises"),
        st(3, "XMuLV clearance and step yield are robustness findings: no model term reached "
              "significance and neither fit is used predictively.",
           "Executive summary",
           "the two response-surface fits are reported as evidence of robustness and are not used "
           "predictively"),
        st(4, "Only the MVM response-surface model is adequate for prediction, and it is the "
              "predictive model on which the design space rests.",
           "Response-surface models", "Only the MVM model is adequate for prediction"),
        st(5, "Volumetric load dominates the MVM response-surface model; no other term reaches "
              "significance.",
           "Response-surface models", "Load dominates the MVM model"),
        st(6, "Lack of fit for the MVM model passes at the stated level but only marginally, and "
              "the limitation is carried explicitly.",
           "Response-surface models",
           "Lack of fit for the MVM model does not reach significance, but the margin is not "
           "comfortable"),
        st(7, "The adverse load trend is bounded: the worst case of the characterized region is the "
              "highest load, and it still meets the back-calculated step requirement.",
           "Design space", "The worst case within the characterized region is the highest load"),
        st(8, "The reported MVM capability is cumulative over the two steps credited with MVM "
              "clearance — this step and anion exchange (PCR-008) — and this step is the larger "
              "of the two contributions.",
           "Process capability and robustness",
           "The MVM figure in Table 16 is cumulative over the two steps credited with MVM clearance"),
        st(9, "The cumulative MVM clearance attribute carries the tightest process-capability index "
              "of any drug-substance attribute.",
           "Process capability and robustness",
           "the MVM attribute is the tightest capability of the drug substance"),
    ])]


def vf_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:vf", unit_operation=VFUO_NAME,
        parameters=["param:vf_filtration_volume", "param:vf_pressure"],
        quality_attributes_constrained=["attr:lrv_mvm", "attr:lrv_xmulv"],
        definition="The part of the characterized rectangle in volumetric load and filtration "
                   "pressure over which the response-surface model predicts an MVM log-reduction at "
                   "or above the required step contribution. Volumetric load is bounded below the "
                   "top of its characterized range, which is the parvovirus breakthrough edge, and "
                   "the XMuLV requirement is met with a wide margin everywhere. The region is effectively "
                   "one-dimensional — volumetric load is the only resolved effect, and filtration "
                   "pressure is bounded because ICH Q5A(R2) ties the clearance claim to the "
                   "conditions under which it was demonstrated, not because an effect was measured. "
                   "The worst case is the highest load at the highest pressure.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "the region of the characterized ranges over which the predicted MVM "
                               "log reduction meets the required step contribution")],
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
        "AMV-3019": "Protein concentration is measured by absorbance at 280 nm (AMV-3019)",
        "AMV-3011": "Size variants are measured by size exclusion chromatography (AMV-3011)",
        "AMV-3013": "charge variants by imaged capillary isoelectric focusing (AMV-3013)",
    },
    True: {   # PCR-010
        "AMV-3019": "Protein concentration is measured by absorbance at 280 nm (AMV-3019)",
        "AMV-3011": "Size variants are measured by SEC-HPLC (AMV-3011)",
        "AMV-3013": "charge variants by imaged capillary isoelectric focusing (AMV-3013)",
    },
}
# Caption of the monitored-attribute table in each document. It carries the distinctive
# claim of this step verbatim: the attributes are monitored, and neither is set/formed
# nor cleared here.
UFATTR_TABLE_QUOTE = {
    False: ("Drug substance attributes monitored across the step. Neither is set nor cleared "
            "here; both are measured to confirm that the step does not change them."),
    True: ("Quality attributes monitored across the ultrafiltration / diafiltration step. "
           "Neither is formed nor cleared here; both are monitored for preservation."),
}
# Per-parameter classification sentence from the report's "Parameter classification"
# section: each says the parameter is a KPP and why no quality attribute is at stake.
UFCLASS_QUOTE = {
    "Number of diavolumes": (
        "The number of diavolumes is a key process parameter, because it sets the completeness "
        "of buffer exchange, which is a performance attribute of the formulated pool and not a "
        "property of the molecule"),
    "Transmembrane pressure": (
        "Transmembrane pressure is a key process parameter. It governs flux, and therefore the "
        "duration of the operation"),
    "Final DS concentration": (
        "The final drug substance concentration is a key process parameter, and it is the "
        "deliverable of the step, so a value away from target is a process performance failure "
        "and not a quality failure"),
}
# Per-parameter sentence from the report's combined ranges / PAR section, which gives the
# binding condition of each proven acceptable range.
UFPAR_QUOTE = {
    "Number of diavolumes": ("the binding condition is the low edge, at which buffer exchange "
                             "is least complete"),
    "Transmembrane pressure": "and the excursion recorded in DEV-010-01 fell inside that range",
    "Final DS concentration": ("which is the range over which the size and charge variant "
                               "profiles of the pool were compared with those of the feed"),
}
# Both documents describe the scale-down system as a tangential-flow filtration system;
# neither calls it "bench-scale", so the entity follows the text.
UFSDM = "scale-down tangential-flow filtration system"


def uf_step(doc_id, file_name, sec, report):
    if report:
        src = ref(doc_id, file_name, sec, "Executive summary",
                  "Ultrafiltration and diafiltration is the last unit operation of the A-Mab "
                  "drug substance process")
    else:
        src = ref(doc_id, file_name, sec, "Purpose and scope",
                  "The step concentrates the virus-filtered pool, exchanges it into the "
                  "formulation buffer")
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
                               "a tangential-flow filtration operation on a membrane whose nominal "
                               "molecular weight cut-off retains the antibody and passes buffer "
                               "species" if report
                               else "concentrated against a retentive membrane")],
        metadata=meta())
    sdm = S.Equipment(
        equipment_id="equip:ufdf_sdm", equipment_name=UFSDM,
        equipment_type="ultrafiltration / diafiltration (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec, "Scale-down model and its qualification",
                               "The scale-down model is a tangential-flow filtration system "
                               "operated at the same membrane loading as the commercial skid"
                               if report else "a scale-down tangential flow filtration system")],
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
    sec = "Study design" if report else "Univariate assessment"
    return [
        S.StudyDesign(
            study_id="study:ufdf_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=UFUO_NAME,
            factors=["Number of diavolumes", "Transmembrane pressure", "Final DS concentration"],
            responses=["step yield", "buffer exchange", "final DS concentration", "mass balance"],
            scale_down_model=UFSDM,
            associated_parameters=list(UFPARAM_CONCEPT.values()),
            source_references=[ref(doc_id, file_name, sec, sec,
                                   "Each parameter was assessed at the edges of its "
                                   "characterization range with the other two at their set-points"
                                   if report else
                                   "Each parameter is run at both edges of its characterization "
                                   "range with the other two at their set-points")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:ufdf_sdm_qual", study_type="scale_down_qualification",
            unit_operation=UFUO_NAME, scale_down_model=UFSDM,
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "Qualification compared step yield and final concentration on "
                                   "the model against the commercial skid" if report
                                   else "compared with the corresponding commercial-scale records")],
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
            "Quality attributes in scope", UFATTR_TABLE_QUOTE[bool(report)])
    # attribute -> method (methods that measure a monitored product-quality attribute)
    for mid, mname, mtype, analytes, attrs in UFMETHODS:
        for a in attrs:
            add(UFATTR_CONCEPT[a], "attribute_measured_by_method", f"method:{mid}",
                f"{UFATTR_NAME[a]} is measured by {mid}.", "Analytical methods",
                UFMETHOD_QUOTE[bool(report)][mid])
    # No-CQA-impact of the operating parameters. The report classifies each parameter
    # individually (§8); the plan makes the claim mechanistically for all three at once.
    plan_no_impact_sec = "Unit-operation description and prior knowledge"
    plan_no_impact_quote = ("Each of these acts through hydraulics and mass balance, and none of "
                            "them acts through the chemistry that forms a quality attribute")
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
               "This plan defines the process characterization study for the ultrafiltration and "
               "diafiltration step"),
            st(2, "The step forms no critical quality attribute and makes no clearance claim.",
               "Purpose and scope",
               "The step forms no critical quality attribute, and no clearance claim is made for it"),
            st(3, "RA-001 assigned every parameter of the step to univariate assessment.",
               "Risk-based prioritization of parameters", "assigned all of them to univariate assessment"),
            st(4, "No drug substance attribute is formed or cleared at the step; two attributes are monitored across it.",
               "Quality attributes in scope", "No drug substance attribute is formed or cleared at this step"),
            st(5, "The study will confirm that aggregate content and charge variant distribution are unchanged across the step.",
               "Objectives",
               "Confirm that aggregate content and charge variant distribution are unchanged across the step"),
            st(6, "No screening and no response-surface design is planned, and no design space will be claimed for the step.",
               "Univariate assessment", "no design space will be claimed for this step"),
            st(7, "Formulation characterization is out of scope; the formulation is set by the drug product development programme.",
               "Purpose and scope", "set by the drug product development programme"),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "No critical quality attribute is assigned to the step; aggregate and charge variants are monitored across it.",
           "Quality attributes in scope", "No critical quality attribute is assigned to this step in the register"),
        st(2, "The drug substance quality attributes are those delivered to the step; no formation or clearance is attributed to it.",
           "Product quality across the operation",
           "The quality attributes of the drug substance are the attributes delivered to this step"),
        st(3, "The step delivers the drug substance at its target concentration in the formulation buffer.",
           "Executive summary",
           "What the step establishes is the delivery of the drug substance at its target "
           "concentration in the formulation buffer"),
        st(4, "Buffer exchange is complete at the low edge of the diavolume range.",
           "Concentration and buffer exchange", "Buffer exchange is complete at the low edge of the diavolume range"),
        st(5, "The number of diavolumes, the transmembrane pressure and the final drug substance concentration are all key process parameters.",
           "Parameter classification", "parameters of the step are key process parameters"),
        st(6, "No parameter of the step is critical or well-controlled critical, because no failure mode reaches a critical quality attribute.",
           "Parameter classification",
           "None is critical and none is well-controlled critical, because no failure mode at this "
           "step reaches a critical quality attribute"),
        st(7, "The step has no design space; the univariate data support a proven acceptable range per parameter instead.",
           "Operating ranges and proven acceptable ranges", "This step has no design space"),
        st(8, "No screening and no response-surface design was run at the step, and RA-001 required none.",
           "Study design",
           "No screening design and no response-surface design was run at this step, and none was "
           "required by RA-001"),
        st(9, "Formulation characterization is deferred to the drug product development programme, not omitted.",
           "Discussion", "Formulation characterization is deferred and not omitted"),
        st(10, "This report rolls up into the Process Characterization Master Report (PCMR-001).",
           "Conclusions", "they roll up into PCMR-001"),
    ])]


def uf_proven_acceptable_ranges(doc_id, file_name):
    """One ProvenAcceptableRange per parameter (report only).

    The step governs no quality attribute, so the acceptance basis is the process-performance
    criteria of PCP-010 rather than a drug-substance specification, and the report states that
    the PAR of each parameter is its full characterization range. There is no fitted
    response-surface model, so ``par_nor_propagated`` is deliberately null."""
    sec = "Operating ranges and proven acceptable ranges"
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
            acceptance_basis="Process-performance criteria of PCP-010 (buffer exchange, final "
                             "concentration, step yield and mass balance); no fitted "
                             "response-surface model exists for this step, so no NOR-propagated "
                             "analysis was run.",
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
            "Formulation characterization is deferred to the drug product development programme "
            "(scope boundary in PTP-001); it is out of scope of this drug-substance pair.",
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
    ("GAP-01", "process",
     "No point in the proposed design space will have been run at commercial scale when the "
     "characterization package completes: the studies are executed on scale-down models at the "
     "sending site and the engineering and PPQ batches are run at set-point.",
     "A scale-dependent effect at the edge of the characterized region (for example pCO2 "
     "accumulation at commercial working volume, or a longer mixing time in a larger vessel) "
     "would not appear in the characterization data at all.",
     "Qualification of every scale-down model under SOP-1001 with statistical comparison of "
     "performance across scales, followed by engineering runs and PPQ batches at set-point; "
     "owned by MSAT at both sites, evidenced by the SOP-1001 qualification records and PCMR-001.",
     "open",
     "No point in the proposed design space will have been run at commercial scale",
     "Design space not confirmed at commercial scale",
     "Scale-down qualification, engineering runs, PPQ at set-point"),
    ("GAP-02", "analytical_method",
     "None of the validated analytical methods has been executed for A-Mab at the receiving-site "
     "laboratory.",
     "In-process and release testing cannot be performed at the receiving site when the plan takes "
     "effect, and method variance is part of the variance that the capability projections in "
     "PCMR-001 must account for.",
     "The method-transfer sequence of §6.2, with comparative precision and accuracy criteria per "
     "method and an approved transfer report per AMV; Analytical Development owns the protocol and "
     "receiving-site Quality Control owns the execution. Until each report is approved the affected "
     "testing stays at the sending site.",
     "open",
     "In-process and release testing cannot therefore be performed there when this plan takes effect",
     "Analytical methods not qualified at the receiving site",
     "Method transfer protocol and report per method"),
    ("GAP-03", "control_strategy",
     "The control strategy that the receiving site must implement does not yet exist: every "
     "parameter carries a proposed set-point and a proposed normal operating range, but none "
     "carries a final classification and no proven acceptable range has been established.",
     "The master batch record cannot be issued in its final form and PPQ cannot start, so the "
     "transfer cannot be completed on the process description alone.",
     "The document sequence of Table 2 (RA-001, then the plans PCP-003 to PCP-010, then the reports "
     "PCR-003 to PCR-010, then PCMR-001), followed by classification under SOP-4001 and revision of "
     "the batch record; MSAT owns the sequence and Quality Assurance approves its output.",
     "open",
     "The control strategy that the receiving site must implement does not yet exist",
     "No parameter classification or control strategy",
     "followed by classification under SOP-4001 and revision of the batch record"),
    ("GAP-04", "validation",
     "Viral clearance cannot be measured in the commercial facility: spiking studies are performed "
     "only at scale-down and under containment, so the clearance claimed for the low-pH hold, for "
     "anion exchange and for virus filtration rests entirely on scale-down data.",
     "The cumulative XMuLV and MVM claims are supported by a modular argument across three steps "
     "and by the qualification of three scale-down models, and not by any commercial-scale "
     "measurement.",
     "The scale-down models for Steps 6, 8 and 9 are qualified to worst-case commercial conditions "
     "and the modular clearance studies are run to ICH Q5A; the receiving site then demonstrates in "
     "the engineering runs that it can hold the governing parameters of those steps.",
     "open",
     "Viral clearance cannot be measured in the commercial facility",
     "Viral clearance measurable only at scale-down",
     "Modular clearance studies to ICH Q5A; parameter control demonstrated"),
    ("GAP-05", "materials",
     "The Protein A capture step cannot inherit its ranges from platform data: RA-004 assessed the "
     "alternate Protein A resin and concluded that independent characterization is required, with "
     "no bridging from the platform data that supports the other steps of the train.",
     "The operating ranges of the capture step, and the leached Protein A attribute that the step "
     "sets, have no prior-knowledge basis and must be established experimentally before the "
     "transfer can complete.",
     "Full characterization of the step in PCP-005 and PCR-005, including the resin life-cycle and "
     "sanitization conditions governed by SOP-2008; Process Development at the sending site owns "
     "the action.",
     "open",
     "The Protein A capture step cannot inherit its ranges from platform data",
     "Protein A resin has no platform bridging (RA-004)",
     "Independent characterization of the capture step"),
    ("GAP-06", "facility",
     "The receiving site has no execution history for this process: no operator there has run an "
     "A-Mab batch, no buffer has been prepared at commercial scale to the A-Mab formulations, and "
     "the buffer hold times that the chromatography steps depend on have not been verified at that "
     "scale.",
     "The impact is concentrated in the first batches, where an execution error or an "
     "out-of-specification buffer lot would move the conductivity and pH of the chromatography "
     "loads, which are the governing parameters of the polishing and viral steps.",
     "Training against the transferred procedures, buffer preparation and expiry verification under "
     "SOP-2103, at least one engineering run per unit operation, and a readiness review before PPQ; "
     "receiving-site Manufacturing owns the action with MSAT support.",
     "open",
     "The receiving site has no execution history for this process",
     "No execution history at the receiving site",
     "Training, buffer verification under SOP-2103, engineering runs"),
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
    acc_quote = {
        "lrv_mvm": "the acceptance criteria given for them are the limits the transferred process "
                   "must meet at commercial scale",
        "hcp": "The attributes, their acceptance criteria and their criticality are given in Table",
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
        st(3, "The plan is strictly prospective: it records no characterization result and makes no "
              "claim about the outcome of any study it commissions.",
           "Purpose and scope", "It records no characterization result"),
        st(4, "The transfer covers the eight drug-substance unit operations (Steps 3 to 10), from "
              "the production bioreactor to the final ultrafiltration and diafiltration step.",
           "Purpose and scope",
           "from the production bioreactor through the final ultrafiltration and diafiltration step"),
        st(5, "Technology transfer under ICH Q10 is the transfer of product and process knowledge, "
              "so that the receiving site can realise the product.",
           "Purpose and scope",
           "the transfer of product and process knowledge between development and manufacturing"),
        st(6, "The characterization scope that supports the transfer assigns 22 of the 37 process "
              "parameters to multivariate study and 15 to univariate study, on the basis set out in RA-001.",
           "Scale-down model and comparability strategy",
           "22 are assigned to multivariate study and 15 to univariate study"),
        st(7, "The process description delivered at transfer carries set-points and proposed normal "
              "operating ranges only: no proven acceptable range and no parameter classification "
              "exists when the plan takes effect.",
           "Transfer of the process, methods and control strategy",
           "It does not carry proven acceptable ranges (PARs), and it does not carry parameter "
           "classifications"),
        st(8, "Six gaps separate what the receiving site holds today from what it needs in order to "
              "manufacture A-Mab under an approved control strategy, and none is closed by this plan.",
           "Gap analysis", "None of the six is closed by this plan"),
        st(9, "Commercial-scale confirmation is a Stage 2 PPQ campaign that confirms, and does not "
              "establish, the process design recorded in the Stage 1 characterization package.",
           "Process performance qualification strategy",
           "PPQ is Stage 2 of the process validation lifecycle, and it confirms at scale the "
           "process design established in Stage 1"),
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
RA_RANK_HEADER = _join_cells(["Parameter", "Potential failure mode", "Attribute(s) at risk"])
RA_ASSIGN_HEADER = _join_cells(["Unit operation", "Parameter"])
RA_CQA_HEADER_3 = _join_cells(["Quality attribute", "Category", "Acceptance"])

RA_PERF_STEP_QUOTE = {
    "harvest": "No parameter of the harvest step can change a product quality attribute",
    "ufdf": "No parameter of the ultrafiltration and diafiltration step forms or clears a "
            "quality attribute",
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
                    _join_cells([r["param"], r["fm"], r["cqa_label"]]),
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
                    _join_cells([r["param"], r["fm"], r["cqa_label"]]),
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
    return [ReportSection(section_id="RA-001-summary", title="Risk assessment summary", statements=[
        st(1, "RA-001 decides which A-Mab process parameters are characterized and by what kind of "
              "study; its output is the characterization scope, not a result.",
           "Purpose and scope",
           "decides which A-Mab process parameters are characterized, and by what kind of study"),
        st(2, "The assessment is executed before any characterization study, and the Process "
              "Characterization Plans carry out the scope it defines.",
           "Purpose and scope",
           "the assessment is performed before any characterization study is executed"),
        st(3, "The assessment classifies no parameter: the CPP, WC-CPP, KPP and GPP designations "
              "are outputs of the characterization studies and are assigned in PCR-003 to PCR-010 "
              "and consolidated in PCMR-001.",
           "Purpose and scope", "No parameter is classified in this assessment"),
        st(4, "The assessment calculates no residual risk, because the control strategy that would "
              "reduce the risk is not yet defined; what is recorded is the risk as it stands with "
              "the controls that exist today.",
           "Purpose and scope", "No residual risk is calculated for those parameters either"),
        st(5, "37 process parameters of the drug-substance train (Steps 3 to 10) are in scope.",
           "Purpose and scope",
           "process parameters of the drug-substance train leaves this document with an "
           "assigned study type"),
        st(6, "The severity of a parameter is inherited from the most critical attribute it can "
              "affect, so criticality never depends on how well a facility controls a parameter.",
           "Risk assessment methodology",
           "a parameter inherits the severity of the most critical attribute within reach"),
        st(7, "Occurrence and detection are scored as they stand before characterization, so the "
              "initial risk priority number is a ranking device on an ordinal scale.",
           "Risk assessment methodology",
           "Occurrence and detection are scored as they stand before characterization"),
        st(8, "Parameters that can reach a viral-clearance attribute take the lowest detection band, "
              "because clearance is demonstrated in small-scale spiking studies and is never "
              "measured on the batch.",
           "Risk assessment methodology",
           "clearance is demonstrated in small-scale spiking studies and is never measured on the batch"),
        st(9, "21 of the 37 parameters can affect at least one quality attribute; the remaining 16 "
              "act on process performance only.",
           "Parameter risk ranking by unit operation",
           "act on process performance only (titre, yield, filter capacity and buffer "
           "exchange)"),
        st(10, "The highest initial risk number in the assessment is 700, and every parameter that "
               "reaches it belongs to one of the three steps credited with viral clearance.",
            "Parameter risk ranking by unit operation",
            "The highest initial risk number in the assessment"),
        st(11, "The campaign scope is 22 parameters in a multivariate design, 14 in univariate "
               "assessment and 1 in a justified univariate assessment; no parameter is excluded "
               "from study.",
            "Characterization study assignment",
            "22 parameters are assigned to a multivariate design, 14 to univariate assessment and "
            "1 to a justified univariate assessment"),
        # The re-authored RA-001 no longer claims the assignment "predicts no design space" --
        # the phrase "design space" does not occur in the document at all. The statement is cut
        # back to the half the document does make: the assignment is prospective and each plan may
        # amend it. A statement is never left asserting more than its document says.
        st(12, "The assignment is prospective: each Process Characterization Plan may amend it "
               "before execution, and the report that follows may place a parameter differently.",
            "Characterization study assignment",
            "the assignment is prospective, since each Process Characterization Plan may amend it "
            "before execution"),
        # Replaced 2026-08-18. The previous statement said one attribute (leached Protein A) has
        # no parameter ranked against it. The re-authored document never says that -- it does not
        # contain the phrase, and mentions leached Protein A only as an attribute that enters at
        # the capture step. The quote would have been re-anchorable nowhere without inventing the
        # claim, so the statement is replaced by a limitation the document does state.
        st(13, "The initial risk priority number is ordinal, so a ratio between two of the numbers "
               "carries no meaning and only the rank order is used in the study assignment.",
            "Assumptions and limitations",
            "The risk priority number is ordinal, which means that a ratio between two of the "
            "numbers carries no meaning"),
        st(14, "Each step's assignment is handed to exactly one characterization plan.",
            "Outputs and downstream use",
            "Each of those plans takes the parameters of one unit operation, with the study type "
            "assigned here"),
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


def _corpus_steps(doc, file, sec_id, sec_title):
    rows = train_row_quotes()
    out = []
    for key in P.CFG.train_order:
        uo = P.CFG.unit_op(key)
        title = P.UNIT_OP_TITLES.get(key, uo.name)
        out.append(S.ProcessStep(
            step_id=f"step:{key}", step_name=title, step_number=str(uo.step),
            unit_operation=title, description=P.UNIT_OP_ROLE.get(key, ""),
            source_references=[ref(doc, file, sec_id, sec_title, rows[key],
                                   table_header=rows.header)], metadata=meta()))
    return out


def _corpus_cqas(doc, file, sec_id, sec_title, table_title, table_id, rows=None):
    """The whole CQA register, as the corpus-spanning documents carry it.

    ``rows`` is the rendered @tbl-cqa of that document, keyed by attribute key. The anchor was
    the bare attribute name before — a span that names the record and attests nothing about
    it, since the acceptance criterion and criticality the record carries are in the row.
    """
    rows = rows if rows is not None else cqa_rows(list(P.cqa_reg["key"]))
    out = []
    for r in P.cqa_reg.to_dict("records"):
        out.append(S.QualityAttribute(
            attribute_id=f"attr:{r['key']}", attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"], acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref(doc, file, sec_id, sec_title, rows[r["key"]],
                                   table_title=table_title, table_id=table_id,
                                   table_header=rows.header)],
            metadata=meta()))
    return out


def _master_plan_cqa_rows():
    """PCMP-001's @tbl-cqa: the register with the setting step inserted as column 2.

    The master plan is the only document that renders the register this way, so its rows
    differ from every other document's and have to be rebuilt from its own expression.
    """
    df = P.cqas_by_keys(list(P.cqa_reg["key"]))
    df.insert(1, "Set by", [P.UNIT_OP_TITLES[s] for s in P.cqa_reg["set_by"]])
    return row_quotes(df, P.cqa_reg["key"])


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


def build_master_plan():
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    from annex_contract.concepts import ConceptStore
    from annex_contract.summaries import ReportSection, ReportStatement
    import ra_content as RC
    doc, f = "PCMP-001", PCMP_FILE
    A, n = [], [0]
    # Campaign scope, straight from the risk assessment that the plan renders (never typed).
    _ra = RC.ra_summary()
    n_params, n_steps = _ra["n"], len(P.CFG.train_order)
    n_multi, n_uni = _ra["n_multivariate"], _ra["n_univariate"]

    def add(subj, pred, obj, text, sec, quote, header=None):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc, f, f"{doc}_sec", sec, quote, table_header=header)],
            metadata=meta()))
    train_rows = train_row_quotes()
    for key in P.CFG.train_order:
        uo = P.CFG.unit_op(key)
        title = P.UNIT_OP_TITLES.get(key, uo.name)
        add("process:amab_ds", "process_has_step", f"step:{key}",
            f"The A-Mab drug-substance process has the step {title}.",
            "Purpose and scope", train_rows[key], train_rows.header)
    for key in ["lrv_mvm", "hcp", "aggregates_hmw"]:
        r = P.cqa_reg[P.cqa_reg.key == key].iloc[0].to_dict()
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{key}_acc",
            f"{r['cqa']} acceptance: {r['acc_low']:g}–{r['acc_high']:g} {r['unit']}.",
            "Critical quality attribute framework", r["cqa"])

    # The three procedures by which a step's in-process limit is set (§ "Which criterion a
    # step is judged against"). Anchored on non-numeric fragments on purpose: the limits are
    # rules evaluated against the seeded model, so the VALUES move with meta.seed while the
    # procedure that produced them does not.
    # The in-process criterion the master plan works through in full (§ "Which criterion a
    # step is judged against"). `predicate` is a closed literal in the contract, so this is an
    # attribute_has_acceptance_criterion assertion and not an invented relation. The quote is
    # rebuilt from the same values the document renders, so it survives a change of meta.seed.
    IPC_SEC = "Which criterion a step is judged against"
    import doe_report as _D
    _pa_ipc = _D.effective_acceptance("protein_a", "pool_hcp_ng_mg")[1]
    add("attr:hcp", "attribute_has_acceptance_criterion", "lit:hcp_ipc_protein_a",
        f"Host cell protein at the capture step is judged against an in-process limit of "
        f"{_pa_ipc:,.0f} ng/mg, carried back from the drug substance specification through "
        f"the cation exchange and anion exchange clearance and divided by an assurance "
        f"margin, and not against the drug substance specification itself.",
        IPC_SEC,
        f"gives the in-process limit of {_pa_ipc:,.0f} ng/mg that PCP-005 and PCR-005 apply")

    def stx(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc, f, f"{doc}_sec", sec, quote)])
    report_sections = [ReportSection(section_id=f"{doc}-summary", title="Master plan summary", statements=[
        stx(1, "PCMP-001 defines the scope, the strategy and the common methods of the Stage 1 "
               "process characterization campaign for A-Mab drug substance.",
            "Purpose and scope",
            "defines the scope, the strategy and the common methods of the Stage 1 process "
            "characterization campaign"),
        stx(2, f"The campaign covers {n_params} process parameters across the {n_steps} unit "
               f"operations, of which {n_multi} are studied in multivariate designed experiments "
               f"and {n_uni} univariately.",
            "Stage 1 characterization strategy",
            f"The campaign covers {n_params} process parameters across the {n_steps} unit "
            f"operations. {n_multi} of them are studied in multivariate designed experiments "
            f"and {n_uni} are studied univariately"),
        stx(3, "The Pre-Characterization Process Risk Assessment (RA-001) decides how each "
               "parameter is studied and hands the study scope to the per-unit-operation plans.",
            "Risk-based prioritization", "The risk assessment decides how each parameter is studied"),
        stx(4, "Screening identifies which parameters have a measurable effect; the response-surface "
               "design is the predictive model from which an operating region or design space is derived.",
            "Common statistical approach",
            "The screening design identifies which parameters have a measurable effect on each "
            "response. The response surface design is the predictive model"),
        stx(5, "The master plan deliberately sets no single minimum capability index for the "
               "campaign; each per-unit-operation plan states the minimum index for its own step.",
            "Acceptance criteria framework",
            "This plan does not set one minimum capability index for the whole campaign"),
        stx(8, "Each step is judged against an in-process limit rather than the drug substance "
               "specification, because an intermediate pool is not the drug substance and the "
               "comparison is wrong in both directions.",
            IPC_SEC,
            "An intermediate pool is not the drug substance, and judging one against those "
            "specifications gives an answer that is wrong in both directions"),
        stx(9, "The campaign sets every in-process limit by one of three procedures, and which "
               "procedure applies is decided by what the downstream train does to the attribute.",
            IPC_SEC,
            "Which procedure applies depends on what the downstream train does to the "
            "attribute, not on the preference of the author"),
        stx(10, "The assurance margin applied after the backward calculation is what makes the "
                "limit a control; a limit set at the undivided ceiling would be a break-even "
                "point dependent on every downstream step delivering its nominal clearance.",
            IPC_SEC,
            "which is a break-even point and not a control"),
        stx(11, "No in-process limit is a typed number; each is a rule evaluated against the "
                "seeded process model, so a change to the process or to a clearance factor "
                "moves the limits with it.",
            IPC_SEC, "Each is a rule evaluated against the seeded process model"),
        stx(12, "Because an in-process limit is tighter than the specification it derives from, "
                "the design space for a step is generally smaller than its characterized region.",
            IPC_SEC,
            "It follows that the design space for a step is generally smaller than its "
            "characterized region"),
        stx(6, "Every per-unit-operation characterization protocol follows the structure and the "
               "methods defined in this master plan and adds only what is specific to its step.",
            "Register of characterization plans",
            "Every protocol follows the structure and the methods defined in this plan"),
        stx(7, "Each per-unit-operation report is issued once the studies of its step have been "
               "analysed, and the Process Characterization Master Report (PCMR-001) is issued after "
               "the last of them.",
            "Deliverables and schedule", "the master report is issued after the last of those reports"),
    ])]
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_scope",
                                  process_steps=_corpus_steps(doc, f, f"{doc}_sec_scope",
                                                              "Purpose and scope")),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=_corpus_cqas(
                                      doc, f, f"{doc}_sec_cqa",
                                      "Critical quality attribute framework",
                                      "Quality attributes in scope for the characterization "
                                      "campaign, with the step at which each is set, its acceptance "
                                      "criterion, its criticality level and its Tool #1 criticality score.",
                                      f"{doc}_tab_cqa", rows=_master_plan_cqa_rows())),
    ]
    inv = S.DocumentInventoryItem(
        document_id=doc, file_name=f, predicted_document_type="process_characterization_master_plan",
        product_name_candidates=["A-Mab"], process_name_candidates=["A-Mab drug substance"],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "master plan", "CQA framework",
                     "scale-down model", "statistical approach", "design of experiments"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc][0]}'.",
        source_references=[ref(doc, f, "Title block", "Title block", title_block_quote(doc))],
        metadata=meta())
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Master plan spans the whole train; entities are the Step 3-10 process steps and the CQA framework.",
            "The per-unit-operation plan register and the common statistical approach are reported via report_sections.",
            "Strictly prospective: the plan carries no characterization results, and it deliberately "
            "sets no campaign-wide minimum capability index, so no capability or classification "
            "entity is asserted here.",
        ],
        inventory=inv, entities=entities, report_sections=report_sections,
        assertions=AssertionStore(run_id=f"gt-{doc}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id="gt-pcmp", concepts=_corpus_step_concepts()))


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

    out = P.cqa_reg.merge(P.cap[["key", "mean", "sd", "Cpk"]], on="key")
    out["Acceptance"] = out.apply(lambda r: f"{r.acc_low:g}–{r.acc_high:g} {r.unit}", axis=1)
    out["Set by"] = out.set_by.map(P.UNIT_OP_TITLES)
    out["Drug substance"] = out.apply(lambda r: f"{r['mean']:.3g} ± {r['sd']:.2g}", axis=1)
    out["Cpk"] = out.Cpk.map(lambda v: f"{v:.2f}")
    cqa_df = (out.rename(columns={"cqa": "CQA", "criticality": "Criticality"})
                 [["CQA", "Criticality", "Acceptance", "Set by", "Drug substance", "Cpk"]])
    cqa = row_quotes(cqa_df, out.key, ".2f")

    keys = list(P.cqa_reg["key"])
    cap_tbl = P.cap_for(keys).copy()
    cap_tbl["Spec"] = cap_tbl["Spec"].str.replace("_", "-", regex=False)
    cap_tbl["Cpk"] = cap_tbl["Cpk"].map(lambda v: f"{v:.2f}")
    cap = row_quotes(cap_tbl, P.cap[P.cap.key.isin(keys)].key, ".2f")

    q = P.param_reg[P.param_reg.classification.isin(["CPP", "WC-CPP"])]
    par = row_quotes(P.cpp_params(), zip(q.unit_operation, q.parameter))

    vt = P.csv("viral_clearance.csv").copy()
    vt["Mechanism"] = vt.step.map(PCMR_VC_MECH)
    vt["Report"] = vt.step.map(PCMR_VC_REPORT)
    viral_df = (vt.rename(columns={"step": "Step", "XMuLV": "XMuLV (log₁₀)",
                                   "MVM": "MVM (log₁₀)"})
                  [["Step", "Mechanism", "XMuLV (log₁₀)", "MVM (log₁₀)", "Report"]])
    viral = row_quotes(viral_df, vt.step, ".2f")

    dv = P.csv("deviations.csv").copy()
    dv["Deviation"] = dv["dev_id"] + " (" + dv["doc_id"] + ")"
    dv["Step"] = dv["step"].map(PCMR_DEV_STEP)
    dv["Root cause"] = (dv["root_cause"].str.replace("_", " ", regex=False)
                        .str.replace("uv ", "UV ", regex=False))
    dv["Disposition"] = (dv["disposition"].str.replace("_", " ", regex=False)
                         .str.replace("re executed", "re-executed", regex=False))
    dev_df = (dv.rename(columns={"summary": "What happened"})
                [["Deviation", "Step", "What happened", "Root cause", "Disposition"]])
    dev = RowQuotes(zip(dv.dev_id, _grid_rows(dev_df, [20, 16, 30, 24, 18])))
    dev.header = _join_cells(dev_df.columns)
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
    report_sections = [ReportSection(section_id=f"{doc}-summary", title="Master report summary", statements=[
        stx(1, "PCMR-001 rolls up the per-unit-operation reports PCR-003 to PCR-010 into one "
               "argument and does not repeat their analyses.",
            "Executive summary",
            "this document consolidates those reports without repeating their analyses"),
        stx(2, f"All {n_cqa} drug-substance quality attributes meet their acceptance criteria at "
               f"commercial scale, on capability estimated by Monte-Carlo simulation of the "
               f"fitted step models.",
            "Executive summary",
            f"All {n_cqa} drug substance quality attributes meet their acceptance criteria at "
            f"commercial scale"),
        stx(3, f"The lowest capability index in the process is {float(cap_min.Cpk):.2f}, on the "
               f"cumulative MVM clearance, and the tightest product quality attribute is high "
               f"mannose.",
            "Executive summary",
            f"The lowest capability index in the process is {float(cap_min.Cpk):.2f}, for the "
            f"cumulative MVM clearance"),
        stx(4, "The report claims no numeric minimum capability index: it states only that "
               "capability is reported as a one-sided index against the applicable limit, "
               "following the practice of the process-validation literature.",
            "Process capability",
            "Capability is reported as a one-sided index against the acceptance limit that "
            "applies, following the practice described in the process validation literature "
            "for judging whether a process can meet a specification"),
        stx(5, "Cumulative viral clearance exceeds the requirement for both model viruses, as a "
               "modular claim summed over independent steps.",
            "Viral clearance summary",
            "Cumulative clearance exceeds the requirement for both model viruses"),
        stx(6, "The three credited clearance mechanisms are orthogonal, which is what licenses "
               "adding the increments; no single step carries the cumulative claim.",
            "Viral clearance summary", "orthogonal, which is what allows the increments to be added"),
        stx(7, f"All {n_par} process parameters carried into the campaign are classified, and "
               f"{counts['WC-CPP']} are well-controlled critical, {counts['KPP']} key and "
               f"{counts['GPP']} general process parameters.",
            "Parameter classification summary",
            f"{counts['WC-CPP']} parameters are well-controlled critical process parameters, "
            f"{counts['KPP']} are key process parameters and {counts['GPP']} are general "
            f"process parameters"),
        stx(8, "Exactly one parameter in the campaign is classified as a critical process "
               "parameter: the inactivation pH of the low-pH hold.",
            "Parameter classification summary",
            "The single critical process parameter is the inactivation pH of the low-pH hold"),
        stx(9, "Host cell protein reaches its drug-substance limit only after the last "
               "purification step; the Protein A and cation-exchange pool values are in-process "
               "results, not failed acceptance criteria.",
            "Host cell protein",
            "The intermediate values are in-process results and not failed acceptance criteria"),
        stx(10, f"Product yield across the train is {P.pct(P.V['overall_yield'])}, reported as a "
                f"process-performance attribute that constrains no design space.",
            "Process performance",
            f"Product yield across the train is {P.pct(P.V['overall_yield'])}"),
        stx(11, f"{n_dev} deviations were recorded across {n_dev_docs} reports; "
                f"{n_dev_ret} were retained with a documented impact assessment, one invalidated "
                f"and re-executed a complete designed experiment, and one was corrected by "
                f"modelling and verification runs.",
            "The register",
            f"{n_dev_ret} deviations were retained, which means the affected data were used as "
            f"executed with a documented impact assessment"),
        stx(12, "No deviation changed a parameter classification, an operating region or a viral "
                "clearance claim, but one control-strategy element did change.",
            "Campaign-level impact",
            "No deviation changed a parameter classification, an operating region or a viral "
            "clearance claim"),
        stx(13, f"The process understanding is multivariate where it needs to be: {n_multi} "
                f"parameters were studied in designed experiments and {n_uni} univariately.",
            "What the campaign established",
            f"{n_multi} parameters were studied in designed experiments and {n_uni} univariately"),
        stx(14, "The report bounds its own claims: design spaces are not confirmed at commercial "
                "scale at the edges of their ranges.",
            "Limitations",
            "Design spaces are not confirmed at commercial scale at the edges of their ranges"),
        stx(15, "Capability is estimated from qualified scale-down models with every parameter "
                "inside its normal operating range, not observed at commercial scale.",
            "Limitations", "Capability is estimated and not observed"),
        stx(16, "Viral clearance is measured in small-scale spiking studies, not on production "
                "material.",
            "Limitations", "Viral clearance is measured in small-scale spiking studies"),
        stx(17, "The characterization package supports entry into Stage 2, and the report is "
                "explicit that it evidences understanding rather than qualification.",
            "Stage 2 readiness",
            "This report should be read as the evidence that the process is understood well "
            "enough to be qualified, and not as evidence that it has been"),
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


def main():
    os.makedirs(OUT, exist_ok=True)
    # The whole 20-document corpus. Every document was re-authored in the 2026-07 register
    # correction, so every quote below was re-anchored against the CURRENT rendered text —
    # the annex is fitted to the document, never the reverse (see authoring/RUNNER.md §5).
    # The superseded first-pass annexes stay frozen under first_pass/ground_truth/.
    for annex in (
        build_plan(), build_report(),                                # PCP/PCR-003 bioreactor
        build_plan_harvest(), build_report_harvest(),                # PCP/PCR-004 harvest
        build_plan_protein_a(), build_report_protein_a(),            # PCP/PCR-005 protein A
        build_plan_viral_inactivation(),                             # PCP-006 low-pH VI
        build_report_viral_inactivation(),                           # PCR-006
        build_plan_cex(), build_report_cex(),                        # PCP/PCR-007 CEX
        build_plan_aex(), build_report_aex(),                        # PCP/PCR-008 AEX
        build_plan_vf(), build_report_vf(),                          # PCP/PCR-009 virus filt.
        build_plan_ufdf(), build_report_ufdf(),                      # PCP/PCR-010 UF/DF
        build_transfer_plan(),                                       # PTP-001
        build_risk_assessment(),                                     # RA-001
        build_master_plan(),                                         # PCMP-001
        build_master_report(),                                       # PCMR-001
    ):
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
