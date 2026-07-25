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

import _pcpkg as P
import schema_ext as S

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


def ref(doc_id, file_name, section_id, section_title, quote, table_title=None, table_id=None):
    return S.SourceReference(
        document_id=doc_id, document_title=P.DOC_REGISTRY[doc_id][0], file_name=file_name,
        section_id=section_id, section_title=section_title,
        heading_path=[section_title], table_id=table_id, table_title=table_title, quote=quote,
    )


# --------------------------------------------------------------------------- #
# Entity builders (shared shape; source references differ per document).       #
# --------------------------------------------------------------------------- #
def build_step(doc_id, file_name, sec, report):
    if report:
        src = ref(doc_id, file_name, sec, "Executive summary", "A-Mab production bioreactor (Step 3)")
    else:
        src = ref(doc_id, file_name, sec, "Unit-operation description",
                  "the only upstream operation that forms product-quality CQAs")
    return S.ProcessStep(
        step_id="step:production_bioreactor", step_name=UO_NAME, step_number=str(STEP),
        unit_operation=UO_NAME,
        description="Fed-batch mammalian cell culture at 15,000 L working volume; the only "
                    "upstream operation that forms product-quality CQAs.",
        input_materials=["inoculum", "basal medium", "nutrient feed"],
        output_materials=["clarified culture (harvest feed)"],
        equipment=["15,000 L production bioreactor", "2 L scale-down model"],
        source_references=[src], metadata=meta(),
    )


def build_equipment(doc_id, file_name, sec, report):
    sdm = S.Equipment(
        equipment_id="equip:sdm_2l", equipment_name="2 L scale-down model",
        equipment_type="bioreactor (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Study execution" if report else "Unit-operation description",
                               "2 L scale-down model" if report
                               else "characterized on a qualified 2 L scale-down model")],
        metadata=meta())
    if report:
        # The report does not restate the 15,000 L vessel; only the SDM is named.
        return [sdm]
    return [
        S.Equipment(equipment_id="equip:production_bioreactor",
                    equipment_name="15,000 L production bioreactor", equipment_type="bioreactor",
                    site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec, "Unit-operation description",
                                           "operated at 15,000 L working volume")],
                    metadata=meta()),
        sdm,
    ]


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
    caption = ("Production-bioreactor process parameters, set-points, ranges and post-characterization classification."
               if classified else
               "Production-bioreactor parameters, set-points, characterization ranges and planned study type.")
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
                                   "Parameters and classification" if classified
                                   else "Parameters and ranges to be characterized",
                                   caption, table_title=caption,
                                   table_id=f"{doc_id}_tab_params")],
            metadata=meta()))
    return out


def build_cqas(doc_id, file_name, sec, report):
    if report:
        sec_title = "Process capability and robustness"
        quote = "CQA distributions and process capability"
        table_title = "Commercial-scale process capability for the bioreactor-set CQAs"
    else:
        sec_title = "Quality attributes in scope"
        quote = "set or principally controlled by the production bioreactor"
        table_title = "CQAs in scope for the production-bioreactor characterization"
    out = []
    for r in CQA_ROWS:
        key = r["key"]
        out.append(S.QualityAttribute(
            attribute_id=CQA_CONCEPT[key], attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"],
            acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            # The report does not restate the method linkage; the plan does (Study design).
            analytical_method=None if report else CQA_METHOD[key], associated_steps=[STEP_LABEL],
            rationale_for_criticality=f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = {r['tool1_score']}.",
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref(doc_id, file_name, sec, sec_title, quote,
                                   table_title=table_title, table_id=f"{doc_id}_tab_cqa")],
            metadata=meta()))
    return out


def build_methods(doc_id, file_name, sec):
    out = []
    for mid, mname, mtype, analytes, attrs in METHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[CQA_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods",
                                   "measured by the validated methods")],
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
            n_runs=n_scr, n_center_points=3, scale_down_model="2 L scale-down model",
            associated_parameters=[PARAM_CONCEPT[f] for f in
                                   ["Culture pH", "Culture temperature", "Dissolved CO2 (pCO2)",
                                    "Osmolality", "Culture duration"]],
            source_references=[ref(doc_id, file_name, sec, sec,
                                   "a resolution-V two-level fractional factorial")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:br_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=UO_NAME,
            factors=["Culture pH", "Culture temperature", "Culture duration", "Dissolved CO2 (pCO2)"],
            responses=["afucosylation", "galactosylation", "high_mannose",
                       "acidic_variants", "aggregates_hmw"],
            n_runs=n_rsm, n_center_points=4, scale_down_model="2 L scale-down model",
            associated_parameters=[PARAM_CONCEPT[f] for f in
                                   ["Culture pH", "Culture temperature", "Culture duration",
                                    "Dissolved CO2 (pCO2)"]],
            source_references=[ref(doc_id, file_name, sec, sec,
                                   "face-centred central-composite")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:br_sdm_qual", study_type="scale_down_qualification", unit_operation=UO_NAME,
            scale_down_model="2 L scale-down model",
            source_references=[ref(doc_id, file_name, sec, sec,
                                   "qualified against at-scale reference data")],
            metadata=meta()),
    ]
    if not report:
        # The univariate assessment is described only in the plan.
        studies.append(S.StudyDesign(
            study_id="study:br_univariate", study_type="univariate", unit_operation=UO_NAME,
            factors=["Initial viable cell conc."], responses=["process performance"],
            associated_parameters=["param:initial_vcc"],
            source_references=[ref(doc_id, file_name, sec, sec,
                                   "evaluated one factor at a time")],
            metadata=meta()))
    return studies


# --------------------------------------------------------------------------- #
# Assertions (relations) + rationales.                                         #
# --------------------------------------------------------------------------- #
def build_assertions(doc_id, file_name, report):
    from app.models.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote)], metadata=meta()))

    # step -> parameters and step -> quality attributes (both docs)
    for name, cid in PARAM_CONCEPT.items():
        add("step:production_bioreactor", "step_has_parameter", cid,
            f"{UO_NAME} has process parameter {name}.",
            "Study design" if report else "Factors, ranges and study type",
            "Nine parameters were studied" if report else "process parameters")
    for r in CQA_ROWS:
        if report:
            add("step:production_bioreactor", "step_has_quality_attribute", CQA_CONCEPT[r["key"]],
                f"{UO_NAME} sets/controls {r['cqa']}.", "Process capability and robustness",
                "bioreactor-set CQA")
        else:
            add("step:production_bioreactor", "step_has_quality_attribute", CQA_CONCEPT[r["key"]],
                f"{UO_NAME} sets/controls {r['cqa']}.", "Quality attributes in scope",
                "set or principally controlled by the production bioreactor")
    # attribute -> method (plan only; the report does not restate the method linkage)
    if not report:
        for r in CQA_ROWS:
            add(CQA_CONCEPT[r["key"]], "attribute_measured_by_method", f"method:{CQA_METHOD[r['key']]}",
                f"{r['cqa']} is measured by {CQA_METHOD[r['key']]}.", "Analytical methods",
                "measured by the validated methods")
    # attribute -> acceptance criterion (both docs state acceptance criteria)
    for r in CQA_ROWS:
        add(CQA_CONCEPT[r["key"]], "attribute_has_acceptance_criterion",
            f"lit:{r['key']}_acc", f"{r['cqa']} acceptance: {r['acc_low']:g}–{r['acc_high']:g} {r['unit']}.",
            "Quality attributes in scope" if not report else "Executive summary", "acceptance criteria")
    # results only in the report: parameter impacts / non-impacts
    if report:
        for cid in [PARAM_CONCEPT[k] for k in
                    ["Culture pH", "Culture temperature", "Dissolved CO2 (pCO2)",
                     "Osmolality", "Culture duration"]]:
            add(cid, "parameter_impacts_attribute", "attr:afucosylation",
                "Parameter significantly affects the glycan/charge-variant CQAs (WC-CPP).",
                "Parameter classification", "significantly affect the glycan and charge-variant CQAs")
        for cid in [PARAM_CONCEPT[k] for k in
                    ["Dissolved oxygen", "Initial viable cell conc.", "Nutrient feed-1 volume"]]:
            add(cid, "parameter_does_not_significantly_impact_attribute", "attr:afucosylation",
                "Parameter affects performance without a significant CQA impact (KPP).",
                "Parameter classification", "do not significantly impact the CQAs")
        add("param:medium_concentration", "parameter_does_not_significantly_impact_attribute",
            "attr:afucosylation", "No meaningful impact over a wide range (GPP).",
            "Parameter classification", "No meaningful impact on CQAs or performance")

    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


# --------------------------------------------------------------------------- #
# Concepts (entity-linking canonical targets).                                 #
# --------------------------------------------------------------------------- #
def build_concepts():
    from app.models.concepts import Concept, ConceptStore
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
    from app.models.summaries import ReportSection, ReportStatement
    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-003 defines the Stage 1 characterization of the A-Mab production bioreactor (Step 3).",
               "Purpose and scope", "defines the Stage 1 (Process Design) characterization"),
            st(2, "Nine process parameters are characterized against the bioreactor-set CQAs.",
               "Factors, ranges and study type", "Nine parameters are in scope"),
            st(3, "The study uses a screening fractional-factorial design followed by a response-surface design on a 2 L scale-down model.",
               "Response-surface design", "face-centred central-composite design"),
            st(4, "Models are acceptable when there is no significant lack of fit against the center-point pure error.",
               "Acceptance and decision criteria", "no significant lack of fit"),
            st(5, "The study must establish a design space over which every in-scope CQA is satisfied simultaneously.",
               "Acceptance and decision criteria",
               "a design space exists over which every in-scope CQA is satisfied simultaneously"),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Culture pH, temperature, dissolved CO2, osmolality and culture duration are classified WC-CPP.",
           "Executive summary", "are classified **well-controlled CPP (WC-CPP)**"),
        st(2, f"The nominal fed-batch reaches a peak VCD of {P.V['peak_vcd_e6']} x10^6 cells/mL and titer of {P.V['nominal_titer_g_per_l']} g/L.",
           "Center-point performance and reproducibility", "peak viable cell density"),
        st(3, "All in-scope CQAs meet acceptance and a multivariate design space was established.",
           "Design space", "the multivariate region"),
        st(4, "The response-surface models are adequate for all five CQAs.",
           "Response-surface models", "response-surface models are adequate for all five CQAs"),
        st(5, "There was no significant lack of fit relative to the center-point pure error.",
           "Response-surface models", "no significant lack of fit"),
        st(6, "All bioreactor-set CQAs meet acceptance with margin at commercial scale.",
           "Process capability and robustness", "minimum capability"),
    ])]


def build_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:bioreactor", unit_operation=UO_NAME,
        parameters=["param:culture_ph", "param:culture_temperature",
                    "param:culture_duration", "param:dissolved_co2"],
        quality_attributes_constrained=[CQA_CONCEPT[r["key"]] for r in CQA_ROWS],
        definition="Multivariate region in culture pH, temperature, duration and dissolved CO2 over "
                   "which every cell-culture CQA is satisfied simultaneously.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "multivariate region of culture pH, temperature, culture duration and dissolved CO")],
        metadata=meta())]


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
                               P.DOC_REGISTRY[doc_id][0])],
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
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Process-capability (Cpk) values have no dedicated field; reported as report_sections statements.",
        ],
        inventory=inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=build_studies(doc, f, report=True),
        design_spaces=build_design_spaces(doc, f),
        report_sections=build_report_sections(doc, f, report=True),
        assertions=build_assertions(doc, f, report=True), concepts=build_concepts())


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


def h_step(doc_id, file_name, sec, report):
    if report:
        src = ref(doc_id, file_name, sec, "Executive summary",
                  "harvest and clarification operation (Step 4)")
    else:
        src = ref(doc_id, file_name, sec, "Unit-operation description",
                  "removes cells and particulates but does not form, remove or modify any "
                  "product-quality attribute")
    return S.ProcessStep(
        step_id="step:harvest_clarification", step_name=HUO_NAME, step_number=str(HSTEP),
        unit_operation=HUO_NAME,
        description="Primary recovery: continuous disk-stack centrifugation followed by depth "
                    "and sterile filtration; clarifies the culture and defines the feed to "
                    "Protein A. Forms no product-quality attribute.",
        input_materials=["production-bioreactor harvest (culture broth)"],
        output_materials=["clarified harvest (Protein A load)"],
        equipment=["continuous disk-stack centrifuge", "depth filter", "sterile filter",
                   "bench-scale clarification model"],
        source_references=[src], metadata=meta())


def h_equipment(doc_id, file_name, sec, report):
    sec_title = "Study execution" if report else "Unit-operation description"
    sdm = S.Equipment(
        equipment_id="equip:clarification_sdm", equipment_name="bench-scale clarification model",
        equipment_type="clarification (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec, sec_title,
                               "qualified bench-scale clarification model")],
        metadata=meta())
    centrifuge = S.Equipment(
        equipment_id="equip:disk_stack_centrifuge", equipment_name="continuous disk-stack centrifuge",
        equipment_type="centrifuge", site_name=P.RECEIVING_SITE,
        source_references=[ref(doc_id, file_name, sec, sec_title,
                               "continuous disk-stack centrifugation")],
        metadata=meta())
    depth = S.Equipment(
        equipment_id="equip:depth_filter", equipment_name="depth filter", equipment_type="filter",
        site_name=P.RECEIVING_SITE,
        source_references=[ref(doc_id, file_name, sec, sec_title,
                               "depth-filter and sterile-filter clarification"
                               if not report else "depth filter and a sterile")],
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
    caption = ("Harvest / clarification process parameters, set-points, ranges and post-characterization classification."
               if classified else
               "Harvest / clarification parameters, set-points, characterization ranges and planned study type.")
    rats = {"KPP": "Governs recovery, clarity and filter capacity (process performance) without a CQA impact.",
            "GPP": "Monitored output attribute with a wide acceptable range and no product-quality consequence."}
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
            rationale_for_criticality=rats.get(r["classification"]) if classified else None,
            source_references=[ref(doc_id, file_name, sec,
                                   "Parameters and classification" if classified
                                   else "Parameters and ranges to be characterized",
                                   caption, table_title=caption,
                                   table_id=f"{doc_id}_tab_params")],
            metadata=meta()))
    return out


def h_methods(doc_id, file_name, sec, report):
    quote = "measured by validated methods" if report else "measured by the validated methods"
    out = []
    for mid, mname, mtype, analytes, attrs in HMETHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[HATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods", quote)],
            metadata=meta()))
    return out


def h_studies(doc_id, file_name, report):
    sec = "Study design"
    return [
        S.StudyDesign(
            study_id="study:hv_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=HUO_NAME,
            factors=["Centrifugation (rcf)", "Depth filter load", "Post-clarification turbidity"],
            responses=["step yield", "post-clarification turbidity", "depth-filter throughput"],
            scale_down_model="bench-scale clarification model",
            associated_parameters=list(HPARAM_CONCEPT.values()),
            source_references=[ref(doc_id, file_name, sec, sec, "one factor at a time")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:hv_sdm_qual", study_type="scale_down_qualification",
            unit_operation=HUO_NAME, scale_down_model="bench-scale clarification model",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "qualified against at-scale reference data")],
            metadata=meta()),
    ]


def h_concepts():
    from app.models.concepts import Concept, ConceptStore
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
    from app.models.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote)], metadata=meta()))

    param_quote = ("parameters were studied" if report else "parameters are in scope")
    param_sec = ("Parameters, ranges and the knowledge space" if report
                 else "Parameters, ranges and study type")
    for name, cid in HPARAM_CONCEPT.items():
        add("step:harvest_clarification", "step_has_parameter", cid,
            f"{HUO_NAME} has process parameter {name}.", param_sec, param_quote)
    # harvest monitors (does not set) the feed-clarity and impurity-load attributes
    for key, cid in HATTR_CONCEPT.items():
        add("step:harvest_clarification", "step_has_quality_attribute", cid,
            f"{HUO_NAME} monitors {HATTR_NAME[key]} to confirm feed consistency.",
            "Quality attributes and process-performance measures",
            "sets or modifies no product-quality CQA")
    # attribute -> method
    for mid, mname, mtype, analytes, attrs in HMETHODS:
        for a in attrs:
            add(HATTR_CONCEPT[a], "attribute_measured_by_method", f"method:{mid}",
                f"{HATTR_NAME[a]} is measured by {mid}.", "Analytical methods",
                "measured by validated methods" if report else "measured by the validated methods")
    # no-CQA-impact of the operating parameters (both docs make this claim)
    no_impact_quote = ("does not significantly impact any CQA" if report
                       else "no credible risk of impact to a product-quality CQA")
    no_impact_sec = ("Parameter classification" if report
                     else "Risk-based prioritization of parameters")
    for name, cid in HPARAM_CONCEPT.items():
        add(cid, "parameter_does_not_significantly_impact_attribute", "attr:aggregates_hmw",
            f"{name} has no significant product-quality (CQA) impact.", no_impact_sec, no_impact_quote)
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def h_report_sections(doc_id, file_name, report):
    from app.models.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-004 defines the Stage 1 characterization of the A-Mab harvest and clarification operation (Step 4).",
               "Purpose and scope", "defines the Stage 1 (Process Design) characterization"),
            st(2, "Harvest and clarification has no impact on the product-quality CQAs, which pass through unchanged.",
               "Objectives", "no impact on the product-quality CQAs"),
            st(3, "Each parameter is studied one factor at a time across its characterization range.",
               "Risk-based prioritization of parameters", "one factor at a time"),
            st(4, "The operation is characterized against process-performance measures because it sets no CQA.",
               "Quality attributes and process-performance measures", "sets or modifies no product-quality CQA"),
            st(5, "The operation defines the clarified feed delivered to Protein A capture.",
               "Unit-operation description and prior knowledge", "defines the feed to Protein A"),
        ])]
    yw = P.csv("yield_waterfall.csv")
    hy = float(yw[yw.step == 4].iloc[0].step_yield)
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Harvest and clarification sets or modifies no product-quality CQA; the CQAs pass through unchanged.",
           "Quality attributes and process-performance measures", "sets or modifies no product-quality CQA"),
        st(2, f"The clarification step yield is {P.pct(hy)} at the nominal condition.",
           "Clarification performance and reproducibility", "clarification step yield"),
        st(3, "The post-clarification turbidity is within its normal operating range, confirming a consistent feed to Protein A.",
           "Clarification performance and reproducibility", "post-clarification turbidity"),
        st(4, "The characterization confirms that harvest and clarification has no product-quality impact.",
           "No product-quality impact", "no product-quality impact"),
        st(5, "Centrifugation force and depth-filter load are KPP; post-clarification turbidity is a monitored GPP.",
           "Parameter classification", "Post-clarification turbidity — GPP"),
        st(6, "This report rolls up into the Process Characterization Master Report (PCMR-001).",
           "Conclusions", "rolls up into the Process Characterization Master Report"),
    ])]


def h_inventory(doc_id, file_name, dtype):
    return S.DocumentInventoryItem(
        document_id=doc_id, file_name=file_name, predicted_document_type=dtype,
        product_name_candidates=["A-Mab"], process_name_candidates=[HUO_NAME],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "harvest and clarification", "primary recovery",
                     "centrifugation", "depth filtration", "parameter classification"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc_id][0]}'.",
        source_references=[ref(doc_id, file_name, "Title block", "Title block",
                               P.DOC_REGISTRY[doc_id][0])],
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
            "Process-performance measures (yield, turbidity, throughput) have no dedicated field; captured via report_sections/assertions.",
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
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Harvest forms no product-quality CQA; no QualityAttribute entities or DesignSpace are present.",
            "Process-performance results (step yield, turbidity) have no dedicated field; reported as report_sections statements.",
        ],
        inventory=h_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=h_studies(doc, f, report=True),
        report_sections=h_report_sections(doc, f, report=True),
        assertions=h_assertions(doc, f, report=True), concepts=h_concepts())


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

# Attributes: the one CQA the step introduces, and the two impurity CQAs it clears.
PA_CQA_KEYS = ["leached_protein_a", "hcp"]
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


def _pa_cqa_row(key):
    return P.cqa_reg[P.cqa_reg.key == key].iloc[0].to_dict()


def pa_step(doc_id, file_name, sec, report):
    if report:
        src = ref(doc_id, file_name, sec, "Executive summary",
                  "Protein A capture chromatography step (Step 5)")
    else:
        src = ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                  "the first and largest reduction of HCP and residual DNA")
    return S.ProcessStep(
        step_id="step:protein_a", step_name=PAUO_NAME, step_number=str(PASTEP),
        unit_operation=PAUO_NAME,
        description="Affinity capture on Protein A resin: binds and concentrates the product "
                    "from the clarified harvest, provides the first and largest reduction of "
                    "HCP and residual DNA, and introduces leached Protein A. Forms no "
                    "product-quality CQA established in cell culture.",
        input_materials=["clarified harvest (Protein A load)"],
        output_materials=["Protein A eluate pool (viral-inactivation feed)"],
        equipment=["Protein A affinity column", "scale-down chromatography column"],
        source_references=[src], metadata=meta())


def pa_equipment(doc_id, file_name, sec, report):
    sec_title = "Study execution" if report else "Scale-down model and its qualification"
    sdm = S.Equipment(
        equipment_id="equip:pa_sdm_column", equipment_name="scale-down chromatography column",
        equipment_type="chromatography column (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Study execution" if report else "Scale-down model and its qualification",
                               "qualified scale-down chromatography column" if report
                               else "scale-down Protein A column")],
        metadata=meta())
    if report:
        return [sdm]
    return [
        S.Equipment(equipment_id="equip:pa_column",
                    equipment_name="commercial-scale Protein A capture column",
                    equipment_type="chromatography column", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec, "Purpose and scope",
                                           "commercial-scale Protein A capture step")],
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
    caption = ("Protein A process parameters, set-points, ranges and post-characterization classification."
               if classified else
               "Protein A parameters, set-points, characterization ranges and planned study type.")
    rats = {"WC-CPP": "Significantly affects the eluate-pool HCP and the impurity load presented "
                       "downstream; reliably controlled within the operating region.",
            "KPP": "Governs step yield / process performance without a significant CQA impact.",
            "GPP": "No meaningful CQA or performance impact over a wide range."}
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
                                   caption, table_title=caption,
                                   table_id=f"{doc_id}_tab_params")],
            metadata=meta()))
    return out


def pa_cqas(doc_id, file_name, sec, report):
    out = []
    for key in PA_CQA_KEYS:
        r = _pa_cqa_row(key)
        if key == "leached_protein_a":
            sec_title, quote = "Quality attributes in scope", "Protein A introduces one CQA"
        else:  # hcp — the principal CQA the step clears
            if report:
                sec_title = "Process capability and robustness"
            else:
                sec_title = "Quality attributes in scope"
            quote = "principal clearance step for host-cell protein"
        out.append(S.QualityAttribute(
            attribute_id=PAATTR_CONCEPT[key], attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"],
            acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            analytical_method=None if report else PA_CQA_METHOD[key],
            associated_steps=[PASTEP_LABEL],
            rationale_for_criticality=f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = {r['tool1_score']}.",
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref(doc_id, file_name, sec, sec_title, quote,
                                   table_title="CQA introduced by the Protein A step, with "
                                               "acceptance criterion and criticality",
                                   table_id=f"{doc_id}_tab_cqa")],
            metadata=meta()))
    return out


def pa_methods(doc_id, file_name, sec, report):
    quote = "measured by validated methods" if report else "measured by the validated methods"
    out = []
    for mid, mname, mtype, analytes, attrs in PAMETHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[PAATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods", quote)],
            metadata=meta()))
    return out


def pa_studies(doc_id, file_name, report):
    sec = "Study execution" if report else "Study design"
    n_scr, n_rsm = P.doe_runs(PAUO, "screening"), P.doe_runs(PAUO, "rsm")
    studies = [
        S.StudyDesign(
            study_id="study:pa_screening", study_type="screening_doe",
            design_name="two-level full factorial", unit_operation=PAUO_NAME,
            factors=PA_MULTIVARIATE,
            responses=["pool_hcp_ng_mg", "step_yield", "leached_protein_a_ppm"],
            n_runs=n_scr, n_center_points=3, scale_down_model="scale-down chromatography column",
            associated_parameters=[PAPARAM_CONCEPT[f] for f in PA_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Screening design",
                                   "a two-level full factorial in the four multivariate factors")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:pa_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=PAUO_NAME,
            factors=PA_MULTIVARIATE,
            responses=["pool_hcp_ng_mg", "step_yield", "leached_protein_a_ppm"],
            n_runs=n_rsm, n_center_points=4, scale_down_model="scale-down chromatography column",
            associated_parameters=[PAPARAM_CONCEPT[f] for f in PA_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "face-centred central-composite")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:pa_sdm_qual", study_type="scale_down_qualification",
            unit_operation=PAUO_NAME, scale_down_model="scale-down chromatography column",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "qualified against at-scale reference data")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:pa_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=PAUO_NAME,
            factors=PA_UNIVARIATE, responses=["step yield", "eluate-pool HCP"],
            associated_parameters=[PAPARAM_CONCEPT[f] for f in PA_UNIVARIATE],
            source_references=[ref(doc_id, file_name, "Study design", "Univariate assessment",
                                   "evaluated one factor at a time")],
            metadata=meta()),
    ]
    return studies


def pa_concepts():
    from app.models.concepts import Concept, ConceptStore
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
    from app.models.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote)], metadata=meta()))

    param_sec = "Factors, ranges and the knowledge space" if report else "Factors, ranges and study type"
    param_quote = "Six parameters were studied" if report else "Six parameters are in scope"
    for name, cid in PAPARAM_CONCEPT.items():
        add("step:protein_a", "step_has_parameter", cid,
            f"{PAUO_NAME} has process parameter {name}.", param_sec, param_quote)
    # step introduces leached Protein A; clears HCP and DNA
    add("step:protein_a", "step_has_quality_attribute", "attr:leached_protein_a",
        f"{PAUO_NAME} introduces leached Protein A.", "Quality attributes in scope",
        "Protein A introduces one CQA")
    for key in ["hcp", "residual_dna"]:
        add("step:protein_a", "step_has_quality_attribute", PAATTR_CONCEPT[key],
            f"{PAUO_NAME} provides the first and principal clearance of {PAATTR_NAME[key]}.",
            "Process capability and robustness" if report else "Quality attributes in scope",
            "principal clearance step for host-cell protein")
    # attribute -> method (plan only; the report does not restate the linkage)
    if not report:
        for key in PA_CQA_METHOD:
            add(PAATTR_CONCEPT[key], "attribute_measured_by_method", f"method:{PA_CQA_METHOD[key]}",
                f"{PAATTR_NAME[key]} is measured by {PA_CQA_METHOD[key]}.", "Analytical methods",
                "measured by the validated methods")
    # acceptance criterion for the introduced CQA (both docs show the table caption)
    lpa = _pa_cqa_row("leached_protein_a")
    add("attr:leached_protein_a", "attribute_has_acceptance_criterion", "lit:leached_protein_a_acc",
        f"Leached Protein A acceptance: {lpa['acc_low']:g}–{lpa['acc_high']:g} {lpa['unit']}.",
        "Quality attributes in scope", "acceptance criterion")
    # parameter -> attribute impacts / non-impacts
    if report:
        for name in PA_WCCPP:
            add(PAPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:hcp",
                f"{name} significantly affects the eluate-pool HCP (WC-CPP).",
                "Parameter classification", "significantly affects the eluate-pool HCP")
        for name in PA_KPP:
            add(PAPARAM_CONCEPT[name], "parameter_does_not_significantly_impact_attribute", "attr:hcp",
                f"{name} governs step yield without a significant CQA impact (KPP).",
                "Parameter classification", "do not significantly affect a product-quality CQA")
        for name in PA_UNIVARIATE:
            add(PAPARAM_CONCEPT[name], "parameter_does_not_significantly_impact_attribute", "attr:hcp",
                f"{name} has no meaningful CQA or performance impact (GPP).",
                "Parameter classification", "No meaningful impact on the CQAs")
    else:
        for name in PA_WCCPP:
            add(PAPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:hcp",
                f"{name} carries a credible impact to the eluate-pool HCP.",
                "Risk-based prioritization of parameters", "credible impact to the eluate-pool HCP")
        for name in PA_UNIVARIATE:
            add(PAPARAM_CONCEPT[name], "parameter_does_not_significantly_impact_attribute", "attr:hcp",
                f"{name} is expected to affect only process performance.",
                "Risk-based prioritization of parameters", "expected to affect only process performance")
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def pa_report_sections(doc_id, file_name, report):
    from app.models.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-005 defines the Stage 1 characterization of the A-Mab Protein A capture step (Step 5).",
               "Purpose and scope", "defines the Stage 1 (Process Design) characterization"),
            st(2, "Six process parameters are characterized; protein load and elution pH are the primary factors for the eluate-pool HCP.",
               "Factors, ranges and study type", "Six parameters are in scope"),
            st(3, "The study uses a full-factorial screen followed by a face-centred central-composite design on a scale-down column.",
               "Response-surface design", "face-centred central-composite design"),
            st(4, "Protein A is the principal clearance step for host-cell protein and residual DNA.",
               "Unit-operation description and prior knowledge", "principal clearance step for host-cell protein"),
            st(5, "The study must establish a multivariate operating region over which the eluate-pool HCP is controlled.",
               "Acceptance and decision criteria",
               "a multivariate operating region exists over which the eluate-pool HCP is controlled"),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Protein load and elution pH are classified WC-CPP; they drive the eluate-pool HCP.",
           "Executive summary", "are classified **well-controlled CPP (WC-CPP)**"),
        st(2, f"The nominal step recovers {P.pct(float(P.csv('yield_waterfall.csv').query('step==5').iloc[0].step_yield))} of the loaded product.",
           "Executive summary", "delivers an eluate-pool HCP of approximately"),
        st(3, "A multivariate operating region in protein load and elution pH was established.",
           "Executive summary", "multivariate operating region (design space) in protein load and elution pH"),
        st(4, "The pool-HCP and step-yield response-surface models are adequate and predictive.",
           "Response-surface models", "adequate and predictive"),
        st(5, "Leached Protein A shows no significant parameter effect and is reported as robust.",
           "Response-surface models", "reported as robust rather than"),
        st(6, "Protein A is the principal clearance step for host-cell protein and residual DNA.",
           "Process capability and robustness", "principal clearance step for host-cell protein and residual DNA"),
    ])]


def pa_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:protein_a", unit_operation=PAUO_NAME,
        parameters=["param:pa_load", "param:pa_elution_ph"],
        quality_attributes_constrained=["attr:hcp", "attr:leached_protein_a"],
        definition="Multivariate region in protein load and elution pH over which the eluate-pool "
                   "HCP is controlled so the polishing steps clear the drug-substance HCP to its limit.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "multivariate region of protein load and elution pH")],
        metadata=meta())]


def pa_inventory(doc_id, file_name, dtype):
    return S.DocumentInventoryItem(
        document_id=doc_id, file_name=file_name, predicted_document_type=dtype,
        product_name_candidates=["A-Mab"], process_name_candidates=[PAUO_NAME],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "Protein A chromatography", "affinity capture",
                     "host-cell protein clearance", "design of experiments", "parameter classification"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc_id][0]}'.",
        source_references=[ref(doc_id, file_name, "Title block", "Title block",
                               P.DOC_REGISTRY[doc_id][0])],
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
            "Eluate-pool HCP is an in-process response with no released spec; captured via StudyDesign.responses.",
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
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Eluate-pool HCP is an in-process response with no released spec; reported via studies/report_sections.",
            "Process-capability (Cpk) values have no dedicated field; reported as report_sections statements.",
        ],
        inventory=pa_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=pa_studies(doc, f, report=True),
        design_spaces=pa_design_spaces(doc, f),
        report_sections=pa_report_sections(doc, f, report=True),
        assertions=pa_assertions(doc, f, report=True), concepts=pa_concepts())


# =========================================================================== #
# Low-pH Viral Inactivation (Step 6) — PCP-006 / PCR-006.                       #
# --------------------------------------------------------------------------- #
# Additive, self-contained builders for the viral-inactivation DoE pair. The    #
# step sets the (cumulative) XMuLV clearance CQA and can increase aggregate; the #
# DoE is a three-factor full-factorial screen + face-centred CCD in inactivation #
# pH / hold time / temperature. pH is the only true CPP in the process.          #
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

VI_CQA_KEYS = ["lrv_xmulv", "aggregates_hmw"]
VIATTR_CONCEPT = {
    "lrv_xmulv": "attr:lrv_xmulv", "aggregates_hmw": "attr:aggregates_hmw",
    "acidic_variants": "attr:acidic_variants",
}
VIATTR_NAME = {
    "lrv_xmulv": "Viral clearance — XMuLV", "aggregates_hmw": "Aggregates (HMW)",
    "acidic_variants": "Acidic charge variants",
}
VI_CQA_METHOD = {"lrv_xmulv": "AMV-3017", "aggregates_hmw": "AMV-3011"}
VIMETHODS = [
    ("AMV-3017", "XMuLV Infectivity Titre (TCID50)", "infectivity_assay",
     ["XMuLV infectious titre"], ["lrv_xmulv"]),
    ("AMV-3011", "Size-Variants (SEC-HPLC)", "chromatography",
     ["aggregate", "monomer"], ["aggregates_hmw"]),
    ("AMV-3013", "Charge Variants (icIEF)", "electrophoresis",
     ["acidic variants"], ["acidic_variants"]),
]


def _vi_cqa_row(key):
    return P.cqa_reg[P.cqa_reg.key == key].iloc[0].to_dict()


def vi_step(doc_id, file_name, sec, report):
    if report:
        src = ref(doc_id, file_name, sec, "Executive summary",
                  "low-pH viral inactivation step (Step 6)")
    else:
        src = ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                  "the dedicated inactivation step of the A-Mab purification train")
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
                               "Study execution" if report else "Scale-down model and its qualification",
                               "qualified scale-down inactivation model" if report
                               else "small-scale inactivation model")],
        metadata=meta())
    if report:
        return [sdm]
    return [
        S.Equipment(equipment_id="equip:vi_vessel",
                    equipment_name="commercial-scale low-pH inactivation vessel",
                    equipment_type="inactivation vessel", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec, "Purpose and scope",
                                           "commercial-scale low-pH inactivation step")],
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
    caption = ("Low-pH inactivation process parameters, set-points, ranges and post-characterization classification."
               if classified else
               "Low-pH inactivation parameters, set-points, characterization ranges and planned study type.")
    rats = {"CPP": "Dominant factor for the enveloped-virus log-reduction (a Severity->=8 "
                   "viral-safety CQA) with a narrow, high-consequence window; the only CPP.",
            "WC-CPP": "Significantly affects both the log-reduction and aggregate; reliably "
                      "controlled by timed, temperature-controlled operation.",
            "GPP": "No meaningful impact on the log-reduction or aggregate over a wide range."}
    out = []
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
                                   caption, table_title=caption,
                                   table_id=f"{doc_id}_tab_params")],
            metadata=meta()))
    return out


def vi_cqas(doc_id, file_name, sec, report):
    quotes = {"lrv_xmulv": "sets the (cumulative) enveloped-virus clearance CQA",
              "aggregates_hmw": "risk of aggregate formation during the low-pH hold"}
    out = []
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
                                   quotes[key],
                                   table_title="Viral-clearance CQA set by the low-pH inactivation step",
                                   table_id=f"{doc_id}_tab_cqa")],
            metadata=meta()))
    return out


def vi_methods(doc_id, file_name, sec, report):
    quote = "measured by validated methods" if report else "measured by the validated methods"
    out = []
    for mid, mname, mtype, analytes, attrs in VIMETHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[VIATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods", quote)],
            metadata=meta()))
    return out


def vi_studies(doc_id, file_name, report):
    sec = "Study execution" if report else "Study design"
    n_scr, n_rsm = P.doe_runs(VIUO, "screening"), P.doe_runs(VIUO, "rsm")
    return [
        S.StudyDesign(
            study_id="study:vi_screening", study_type="screening_doe",
            design_name="two-level full factorial", unit_operation=VIUO_NAME,
            factors=VI_MULTIVARIATE,
            responses=["xmulv_lrf", "aggregate_out_pct", "acidic_variants"],
            n_runs=n_scr, n_center_points=3, scale_down_model="scale-down inactivation model",
            associated_parameters=[VIPARAM_CONCEPT[f] for f in VI_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Screening design",
                                   "a two-level full factorial in the three multivariate factors")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vi_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=VIUO_NAME,
            factors=VI_MULTIVARIATE,
            responses=["xmulv_lrf", "aggregate_out_pct", "acidic_variants"],
            n_runs=n_rsm, n_center_points=4, scale_down_model="scale-down inactivation model",
            associated_parameters=[VIPARAM_CONCEPT[f] for f in VI_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "face-centred central-composite")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vi_sdm_qual", study_type="scale_down_qualification",
            unit_operation=VIUO_NAME, scale_down_model="scale-down inactivation model",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "qualified against at-scale reference data")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vi_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=VIUO_NAME,
            factors=VI_UNIVARIATE, responses=["XMuLV log-reduction", "aggregate"],
            associated_parameters=[VIPARAM_CONCEPT[f] for f in VI_UNIVARIATE],
            source_references=[ref(doc_id, file_name, "Study design", "Univariate assessment",
                                   "evaluated one factor at a time")],
            metadata=meta()),
    ]


def vi_concepts():
    from app.models.concepts import Concept, ConceptStore
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
    from app.models.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote)], metadata=meta()))

    param_sec = "Factors, ranges and the knowledge space" if report else "Factors, ranges and study type"
    param_quote = "Four parameters were studied" if report else "Four parameters are in scope"
    for name, cid in VIPARAM_CONCEPT.items():
        add("step:viral_inactivation", "step_has_parameter", cid,
            f"{VIUO_NAME} has process parameter {name}.", param_sec, param_quote)
    # step sets the XMuLV clearance CQA and carries the aggregate risk
    add("step:viral_inactivation", "step_has_quality_attribute", "attr:lrv_xmulv",
        f"{VIUO_NAME} sets the cumulative XMuLV clearance.", "Quality attributes in scope",
        "sets the (cumulative) enveloped-virus clearance CQA")
    add("step:viral_inactivation", "step_has_quality_attribute", "attr:aggregates_hmw",
        f"{VIUO_NAME} can increase aggregate during the low-pH hold.", "Quality attributes in scope",
        "risk of aggregate formation during the low-pH hold")
    # attribute -> method (plan only)
    if not report:
        for key in VI_CQA_METHOD:
            add(VIATTR_CONCEPT[key], "attribute_measured_by_method", f"method:{VI_CQA_METHOD[key]}",
                f"{VIATTR_NAME[key]} is measured by {VI_CQA_METHOD[key]}.", "Analytical methods",
                "measured by the validated methods")
    # acceptance criterion for the viral-clearance CQA
    xr = _vi_cqa_row("lrv_xmulv")
    add("attr:lrv_xmulv", "attribute_has_acceptance_criterion", "lit:lrv_xmulv_acc",
        f"Cumulative XMuLV clearance acceptance: {xr['acc_low']:g}–{xr['acc_high']:g} {xr['unit']}.",
        "Quality attributes in scope", "acceptance criterion")
    # parameter -> attribute impacts / non-impacts
    if report:
        add("param:vi_ph", "parameter_impacts_attribute", "attr:lrv_xmulv",
            "Inactivation pH is the dominant factor for the enveloped-virus log-reduction (CPP).",
            "Parameter classification", "dominant factor for the enveloped-virus")
        for name in VI_WCCPP:
            add(VIPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:lrv_xmulv",
                f"{name} significantly affects the log-reduction and aggregate (WC-CPP).",
                "Parameter classification", "significantly affects both the log-reduction")
        add("param:vi_protein_conc", "parameter_does_not_significantly_impact_attribute", "attr:lrv_xmulv",
            "A-Mab concentration has no meaningful CQA impact (GPP).",
            "Parameter classification", "No meaningful impact on the log-reduction")
    else:
        for name in VI_MULTIVARIATE:
            add(VIPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:lrv_xmulv",
                f"{name} carries a credible impact to the enveloped-virus inactivation.",
                "Risk-based prioritization of parameters",
                "credible impact to the enveloped-virus inactivation")
        add("param:vi_protein_conc", "parameter_does_not_significantly_impact_attribute", "attr:lrv_xmulv",
            "A-Mab concentration is expected to affect neither response over a wide range.",
            "Risk-based prioritization of parameters", "expected to affect neither over a wide range")
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def vi_report_sections(doc_id, file_name, report):
    from app.models.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-006 defines the Stage 1 characterization of the A-Mab low-pH viral inactivation step (Step 6).",
               "Purpose and scope", "defines the Stage 1 (Process Design) characterization"),
            st(2, "Four process parameters are characterized; inactivation pH, hold time and temperature are the DoE factors.",
               "Factors, ranges and study type", "Four parameters are in scope"),
            st(3, "The study uses a full-factorial screen followed by a face-centred central-composite design.",
               "Response-surface design", "face-centred central-composite design"),
            st(4, "Low-pH inactivation is enveloped-virus specific; MVM is cleared orthogonally by AEX and virus filtration.",
               "Unit-operation description and prior knowledge",
               "clearance is provided orthogonally by anion exchange and small-virus filtration"),
            st(5, "The study must establish a design space over which the XMuLV log-reduction is assured and aggregate stays within limit.",
               "Acceptance and decision criteria",
               "a design space exists over which the XMuLV log-reduction is assured"),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Inactivation pH is classified CPP — the only true critical process parameter in the process.",
           "Executive summary", "classified **CPP**"),
        st(2, "At the nominal condition the step delivers a robust XMuLV log-reduction.",
           "Executive summary", "delivers an XMuLV log-reduction of approximately"),
        st(3, "Low-pH inactivation provides no clearance of the non-enveloped model virus MVM.",
           "Executive summary", "no clearance of the non-enveloped model virus MVM"),
        st(4, "A design space in inactivation pH and hold time was established.",
           "Executive summary", "design space in inactivation pH and hold time was established"),
        st(5, "The aggregate model is excellent; the XMuLV log-reduction model is adequate with no significant lack of fit.",
           "Response-surface models", "XMuLV log-reduction model is adequate"),
        st(6, "The step is the largest single contributor to the enveloped-virus clearance.",
           "Process capability and robustness", "largest single contributor to the enveloped-virus clearance"),
    ])]


def vi_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:viral_inactivation", unit_operation=VIUO_NAME,
        parameters=["param:vi_ph", "param:vi_hold_time"],
        quality_attributes_constrained=["attr:lrv_xmulv", "attr:aggregates_hmw"],
        definition="Region in inactivation pH and hold time over which the XMuLV log-reduction is "
                   "assured with margin and aggregate remains within its limit.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "region of inactivation pH and hold time")],
        metadata=meta())]


def vi_inventory(doc_id, file_name, dtype):
    return S.DocumentInventoryItem(
        document_id=doc_id, file_name=file_name, predicted_document_type=dtype,
        product_name_candidates=["A-Mab"], process_name_candidates=[VIUO_NAME],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "low-pH viral inactivation", "viral clearance",
                     "XMuLV log-reduction", "design of experiments", "parameter classification"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc_id][0]}'.",
        source_references=[ref(doc_id, file_name, "Title block", "Title block",
                               P.DOC_REGISTRY[doc_id][0])],
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
            "XMuLV clearance is claimed conservatively per ICH Q5A, not from the RSM model.",
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
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "XMuLV clearance is claimed conservatively per ICH Q5A, not from the RSM model.",
            "Process-capability (Cpk) values have no dedicated field; reported as report_sections statements.",
        ],
        inventory=vi_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=vi_studies(doc, f, report=True),
        design_spaces=vi_design_spaces(doc, f),
        report_sections=vi_report_sections(doc, f, report=True),
        assertions=vi_assertions(doc, f, report=True), concepts=vi_concepts())


# =========================================================================== #
# Cation Exchange Chromatography (Step 7) — PCP-007 / PCR-007.                  #
# --------------------------------------------------------------------------- #
# Additive, self-contained builders for the CEX polishing DoE pair. The step    #
# sets NO CQA: it is the principal aggregate-reduction (polish) step and a major #
# clearance step for HCP, residual DNA and leached Protein A, all formed         #
# upstream. The DoE is a four-factor full-factorial screen + face-centred CCD in #
# load / wash-conductivity / elution-pH / stop-collect; flow is a univariate GPP.#
# All four multivariate factors are WC-CPP (each affects aggregate or HCP).      #
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
                  "cation-exchange (CEX) polishing chromatography step (Step 7)")
    else:
        src = ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                  "the first polishing step of the A-Mab purification train")
    return S.ProcessStep(
        step_id="step:cex", step_name=CXUO_NAME, step_number=str(CXSTEP),
        unit_operation=CXUO_NAME,
        description="Bind-and-elute cation-exchange polishing: the principal "
                    "aggregate-reduction step of the process, and a major clearance step "
                    "for HCP with modular clearance of residual DNA and leached Protein A. "
                    "Forms no product-quality CQA; the CQAs it governs are formed upstream.",
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
                               "qualified scale-down cation-exchange column" if report
                               else "scale-down cation-exchange column")],
        metadata=meta())
    if report:
        return [sdm]
    return [
        S.Equipment(equipment_id="equip:cex_column",
                    equipment_name="commercial-scale cation-exchange polishing column",
                    equipment_type="chromatography column", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec, "Purpose and scope",
                                           "commercial-scale cation-exchange polishing step")],
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
    caption = ("Cation-exchange process parameters, set-points, ranges and post-characterization classification."
               if classified else
               "Cation-exchange parameters, set-points, characterization ranges and planned study type.")
    rats = {"WC-CPP": "Significantly affects the eluate-pool aggregate and/or HCP presented "
                      "downstream; reliably controlled within the operating region.",
            "GPP": "No meaningful CQA or performance impact over a wide range."}
    out = []
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
                                   caption, table_title=caption,
                                   table_id=f"{doc_id}_tab_params")],
            metadata=meta()))
    return out


def cx_cqas(doc_id, file_name, sec, report):
    quotes = {"aggregates_hmw": "principal reduction step for the high-molecular-weight aggregate"}
    default_quote = "major clearance step for the impurity CQAs formed upstream"
    out = []
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
                                   quotes.get(key, default_quote),
                                   table_title="CQAs controlled by the cation-exchange step",
                                   table_id=f"{doc_id}_tab_cqa")],
            metadata=meta()))
    return out


def cx_methods(doc_id, file_name, sec, report):
    quote = "measured by validated methods" if report else "measured by the validated methods"
    out = []
    for mid, mname, mtype, analytes, attrs in CXMETHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[CXATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods", quote)],
            metadata=meta()))
    return out


def cx_studies(doc_id, file_name, report):
    sec = "Study execution" if report else "Study design"
    n_scr, n_rsm = P.doe_runs(CXUO, "screening"), P.doe_runs(CXUO, "rsm")
    responses = ["aggregate_out_pct", "hcp_out_ng_mg", "step_yield"]
    return [
        S.StudyDesign(
            study_id="study:cex_screening", study_type="screening_doe",
            design_name="two-level full factorial", unit_operation=CXUO_NAME,
            factors=CX_MULTIVARIATE, responses=responses,
            n_runs=n_scr, n_center_points=3, scale_down_model="scale-down chromatography column",
            associated_parameters=[CXPARAM_CONCEPT[f] for f in CX_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Screening design",
                                   "a two-level full factorial in the four multivariate factors")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:cex_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=CXUO_NAME,
            factors=CX_MULTIVARIATE, responses=responses,
            n_runs=n_rsm, n_center_points=4, scale_down_model="scale-down chromatography column",
            associated_parameters=[CXPARAM_CONCEPT[f] for f in CX_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "face-centred central-composite")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:cex_sdm_qual", study_type="scale_down_qualification",
            unit_operation=CXUO_NAME, scale_down_model="scale-down chromatography column",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "qualified against at-scale reference data")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:cex_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=CXUO_NAME,
            factors=CX_UNIVARIATE, responses=["step yield", "eluate-pool aggregate", "eluate-pool HCP"],
            associated_parameters=[CXPARAM_CONCEPT[f] for f in CX_UNIVARIATE],
            source_references=[ref(doc_id, file_name, "Study design", "Univariate assessment",
                                   "evaluated one factor at a time")],
            metadata=meta()),
    ]


def cx_concepts():
    from app.models.concepts import Concept, ConceptStore
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
    from app.models.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote)], metadata=meta()))

    param_sec = "Factors, ranges and the knowledge space" if report else "Factors, ranges and study type"
    param_quote = "Five parameters were studied" if report else "Five parameters are in scope"
    for name, cid in CXPARAM_CONCEPT.items():
        add("step:cex", "step_has_parameter", cid,
            f"{CXUO_NAME} has process parameter {name}.", param_sec, param_quote)
    # step is the principal aggregate polish; clears HCP, DNA and leached Protein A
    add("step:cex", "step_has_quality_attribute", "attr:aggregates_hmw",
        f"{CXUO_NAME} is the principal aggregate-reduction step.", "Quality attributes in scope",
        "principal reduction step for the high-molecular-weight aggregate")
    for key in ["hcp", "residual_dna", "leached_protein_a"]:
        add("step:cex", "step_has_quality_attribute", CXATTR_CONCEPT[key],
            f"{CXUO_NAME} clears {CXATTR_NAME[key]} (formed upstream).",
            "Quality attributes in scope",
            "major clearance step for the impurity CQAs formed upstream")
    # attribute -> method (plan only; the report does not restate the linkage)
    if not report:
        for key in CX_CQA_METHOD:
            add(CXATTR_CONCEPT[key], "attribute_measured_by_method", f"method:{CX_CQA_METHOD[key]}",
                f"{CXATTR_NAME[key]} is measured by {CX_CQA_METHOD[key]}.", "Analytical methods",
                "measured by the validated methods")
    # acceptance criterion for the principal CQA the step governs
    agg = _cx_cqa_row("aggregates_hmw")
    add("attr:aggregates_hmw", "attribute_has_acceptance_criterion", "lit:aggregates_hmw_acc",
        f"Aggregate acceptance: {agg['acc_low']:g}–{agg['acc_high']:g} {agg['unit']}.",
        "Quality attributes in scope", "acceptance criterion")
    # parameter -> attribute impacts / non-impacts
    if report:
        add("param:cex_load", "parameter_impacts_attribute", "attr:aggregates_hmw",
            "Protein load significantly affects the eluate-pool aggregate and HCP (WC-CPP).",
            "Parameter classification", "Significantly affects both the eluate-pool aggregate")
        add("param:cex_wash_cond", "parameter_impacts_attribute", "attr:hcp",
            "Load/wash conductivity is the dominant factor for HCP clearance (WC-CPP).",
            "Parameter classification", "The dominant factor for HCP clearance")
        for name in ["Elution buffer pH", "Elution stop collect"]:
            add(CXPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:aggregates_hmw",
                f"{name} significantly affects the eluate-pool aggregate (WC-CPP).",
                "Parameter classification", "Each significantly affects the eluate-pool aggregate")
        add("param:cex_flow", "parameter_does_not_significantly_impact_attribute", "attr:aggregates_hmw",
            "Elution flow rate has no meaningful CQA or performance impact (GPP).",
            "Parameter classification", "No meaningful impact on the CQAs or on performance")
    else:
        for name in CX_MULTIVARIATE:
            add(CXPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:aggregates_hmw",
                f"{name} carries a credible impact to the eluate-pool aggregate or HCP.",
                "Risk-based prioritization of parameters",
                "a credible main-effect and interaction risk to the eluate-pool aggregate or HCP")
        add("param:cex_flow", "parameter_does_not_significantly_impact_attribute", "attr:aggregates_hmw",
            "Elution flow rate is expected to affect only process performance.",
            "Risk-based prioritization of parameters",
            "expected to affect only process performance over a wide range")
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def cx_report_sections(doc_id, file_name, report):
    from app.models.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-007 defines the Stage 1 characterization of the A-Mab cation-exchange polishing step (Step 7).",
               "Purpose and scope", "defines the Stage 1 (Process Design) characterization"),
            st(2, "Five process parameters are characterized; four are studied in the multivariate DoE and the flow rate univariately.",
               "Factors, ranges and study type", "Five parameters are in scope"),
            st(3, "The study uses a full-factorial screen followed by a face-centred central-composite design on a scale-down column.",
               "Response-surface design", "face-centred central-composite design"),
            st(4, "Cation exchange is the principal aggregate-reduction step and a major clearance step for HCP, DNA and leached Protein A.",
               "Quality attributes in scope", "principal reduction step for the high-molecular-weight aggregate"),
            st(5, "The study must establish a multivariate operating region over which the eluate-pool aggregate and HCP are controlled.",
               "Acceptance and decision criteria",
               "a multivariate operating region exists over which the eluate-pool aggregate and HCP are controlled"),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "All four multivariate parameters are well-controlled CPPs and the elution flow rate is a general process parameter.",
           "Parameter classification", "the four multivariate parameters are well-controlled CPPs"),
        st(2, "Cation exchange is the principal aggregate-reduction step of the process.",
           "Process capability and robustness", "principal aggregate-reduction step of the process"),
        st(3, "Pool HCP is governed by the load/wash conductivity and protein load through a significant load × conductivity interaction.",
           "Screening: factor effects", "significant load × conductivity interaction"),
        st(4, "The aggregate and pool-HCP response-surface models are adequate and predictive.",
           "Response-surface models", "adequate and predictive"),
        st(5, "The step yield is governed by protein load and is otherwise robust.",
           "Discussion", "governed by protein load and is otherwise robust"),
        st(6, "Cation exchange is the principal contributor to the drug-substance aggregate capability.",
           "Conclusions", "principal contributor to the drug-substance aggregate"),
    ])]


def cx_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:cex", unit_operation=CXUO_NAME,
        parameters=["param:cex_load", "param:cex_wash_cond", "param:cex_elution_ph"],
        quality_attributes_constrained=["attr:aggregates_hmw", "attr:hcp"],
        definition="Multivariate region in protein load, wash conductivity and elution pH over "
                   "which the eluate-pool aggregate and HCP are controlled so the drug substance "
                   "meets its aggregate and HCP limits.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "multivariate region of the four well-controlled CPPs")],
        metadata=meta())]


def cx_inventory(doc_id, file_name, dtype):
    return S.DocumentInventoryItem(
        document_id=doc_id, file_name=file_name, predicted_document_type=dtype,
        product_name_candidates=["A-Mab"], process_name_candidates=[CXUO_NAME],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "cation-exchange chromatography", "aggregate clearance",
                     "host-cell protein clearance", "design of experiments", "parameter classification"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc_id][0]}'.",
        source_references=[ref(doc_id, file_name, "Title block", "Title block",
                               P.DOC_REGISTRY[doc_id][0])],
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
            "Eluate-pool aggregate and HCP are in-process responses with no released spec; captured via StudyDesign.responses.",
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
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "CEX sets no CQA; the QualityAttribute entities are the CQAs it controls/clears (formed upstream).",
            "Eluate-pool aggregate and HCP are in-process responses with no released spec; reported via studies/report_sections.",
            "Process-capability (Cpk) values have no dedicated field; reported as report_sections statements.",
        ],
        inventory=cx_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=cx_studies(doc, f, report=True),
        design_spaces=cx_design_spaces(doc, f),
        report_sections=cx_report_sections(doc, f, report=True),
        assertions=cx_assertions(doc, f, report=True), concepts=cx_concepts())


# =========================================================================== #
# Anion Exchange Chromatography (Step 8) — PCP-008 / PCR-008.                   #
# --------------------------------------------------------------------------- #
# Additive, self-contained builders for the AEX flow-through polishing DoE      #
# pair. Unlike CEX, AEX SETS one CQA of its own — the cumulative MVM             #
# (parvovirus) clearance claim — and is a major clearance step for enveloped    #
# virus (XMuLV), HCP, residual DNA and leached Protein A. The DoE is a           #
# four-factor full-factorial screen + face-centred CCD in load-pH /             #
# wash1-conductivity / load-conductivity / load; the operating flow rate is a    #
# univariate WC-CPP (residence-time / viral-clearance). All five parameters are  #
# WC-CPP. Two deviations are documented in the report (DEV-01 deamidated load →  #
# designs re-executed; DEV-02 pool-collection UV set-point corrected by          #
# modelling + verification runs); the annex captures the DoE-grounded entities.  #
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
                  "anion-exchange (AEX) polishing chromatography step (Step 8)")
    else:
        src = ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                  "the final polishing step of the A-Mab purification train")
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
                               "qualified scale-down anion-exchange column" if report
                               else "scale-down anion-exchange column")],
        metadata=meta())
    if report:
        return [sdm]
    return [
        S.Equipment(equipment_id="equip:aex_column",
                    equipment_name="commercial-scale anion-exchange polishing column",
                    equipment_type="chromatography column", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec, "Purpose and scope",
                                           "commercial-scale anion-exchange polishing step")],
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
    caption = ("Anion-exchange process parameters, set-points, ranges and post-characterization classification."
               if classified else
               "Anion-exchange parameters, set-points, characterization ranges and planned study type.")
    rats = {"WC-CPP": "Significantly affects the flow-through-pool HCP and/or the credited viral "
                      "log-reduction, or is controlled to preserve the residence time credited for "
                      "viral clearance; reliably controlled within the operating region."}
    out = []
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
                                   caption, table_title=caption,
                                   table_id=f"{doc_id}_tab_params")],
            metadata=meta()))
    return out


def ax_cqas(doc_id, file_name, sec, report):
    quotes = {"lrv_mvm": "sets one CQA of its own"}
    default_quote = ("major clearance step for the enveloped-virus (XMuLV) log-reduction and "
                     "for the process-related impurity CQAs")
    out = []
    for key in AX_CQA_KEYS:
        r = _ax_cqa_row(key)
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
                                   quotes.get(key, default_quote),
                                   table_title="CQAs in scope for the anion-exchange step",
                                   table_id=f"{doc_id}_tab_cqa")],
            metadata=meta()))
    return out


def ax_methods(doc_id, file_name, sec, report):
    quote = "measured by validated methods" if report else "measured by the validated methods"
    out = []
    for mid, mname, mtype, analytes, attrs in AXMETHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[AXATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods", quote)],
            metadata=meta()))
    return out


def ax_studies(doc_id, file_name, report):
    sec = "Study execution" if report else "Study design"
    n_scr, n_rsm = P.doe_runs(AXUO, "screening"), P.doe_runs(AXUO, "rsm")
    responses = ["hcp_out_ng_mg", "xmulv_lrf", "mvm_lrf", "step_yield"]
    return [
        S.StudyDesign(
            study_id="study:aex_screening", study_type="screening_doe",
            design_name="two-level full factorial", unit_operation=AXUO_NAME,
            factors=AX_MULTIVARIATE, responses=responses,
            n_runs=n_scr, n_center_points=3, scale_down_model="scale-down chromatography column",
            associated_parameters=[AXPARAM_CONCEPT[f] for f in AX_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Screening design",
                                   "a two-level full factorial in the four multivariate factors")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:aex_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=AXUO_NAME,
            factors=AX_MULTIVARIATE, responses=responses,
            n_runs=n_rsm, n_center_points=4, scale_down_model="scale-down chromatography column",
            associated_parameters=[AXPARAM_CONCEPT[f] for f in AX_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "face-centred central-composite")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:aex_sdm_qual", study_type="scale_down_qualification",
            unit_operation=AXUO_NAME, scale_down_model="scale-down chromatography column",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "qualified against at-scale reference data")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:aex_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=AXUO_NAME,
            factors=AX_UNIVARIATE,
            responses=["flow-through-pool HCP", "XMuLV log-reduction", "MVM log-reduction", "step yield"],
            associated_parameters=[AXPARAM_CONCEPT[f] for f in AX_UNIVARIATE],
            source_references=[ref(doc_id, file_name, "Study design", "Univariate assessment",
                                   "evaluated one factor at a time")],
            metadata=meta()),
    ]


def ax_concepts():
    from app.models.concepts import Concept, ConceptStore
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
    from app.models.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote)], metadata=meta()))

    param_sec = "Factors, ranges and the knowledge space" if report else "Factors, ranges and study type"
    param_quote = "Five parameters were studied" if report else "Five parameters are in scope"
    for name, cid in AXPARAM_CONCEPT.items():
        add("step:aex", "step_has_parameter", cid,
            f"{AXUO_NAME} has process parameter {name}.", param_sec, param_quote)
    # step sets the MVM clearance CQA; clears XMuLV, HCP, DNA and leached Protein A
    add("step:aex", "step_has_quality_attribute", "attr:lrv_mvm",
        f"{AXUO_NAME} sets the cumulative MVM (parvovirus) clearance claim.",
        "Quality attributes in scope", "sets one CQA of its own")
    for key in ["lrv_xmulv", "hcp", "residual_dna", "leached_protein_a"]:
        add("step:aex", "step_has_quality_attribute", AXATTR_CONCEPT[key],
            f"{AXUO_NAME} clears {AXATTR_NAME[key]}.", "Quality attributes in scope",
            "major clearance step for the enveloped-virus (XMuLV) log-reduction and "
            "for the process-related impurity CQAs")
    # attribute -> method (plan only; the report does not restate the linkage)
    if not report:
        for key in AX_CQA_METHOD:
            add(AXATTR_CONCEPT[key], "attribute_measured_by_method", f"method:{AX_CQA_METHOD[key]}",
                f"{AXATTR_NAME[key]} is measured by {AX_CQA_METHOD[key]}.", "Analytical methods",
                "measured by the validated methods")
    # acceptance criterion for the CQA the step sets
    mvm = _ax_cqa_row("lrv_mvm")
    add("attr:lrv_mvm", "attribute_has_acceptance_criterion", "lit:lrv_mvm_acc",
        f"MVM clearance acceptance: ≥ {mvm['acc_low']:g} {mvm['unit']}.",
        "Quality attributes in scope", "acceptance criterion")
    # parameter -> attribute impacts (all five are WC-CPP)
    if report:
        add("param:aex_load_ph", "parameter_impacts_attribute", "attr:hcp",
            "Load pH is the dominant factor for the flow-through-pool HCP and the viral log-reduction (WC-CPP).",
            "Parameter classification", "The dominant factor for the flow-through-pool HCP")
        add("param:aex_wash1_cond", "parameter_impacts_attribute", "attr:hcp",
            "Equil/Wash-1 conductivity significantly affects the flow-through-pool HCP (WC-CPP).",
            "Parameter classification", "Significantly affects the flow-through-pool HCP")
        add("param:aex_load_cond", "parameter_impacts_attribute", "attr:lrv_mvm",
            "Load conductivity is the second factor for the XMuLV and MVM log-reduction (WC-CPP).",
            "Parameter classification", "The second factor for the XMuLV and MVM log-reduction")
        add("param:aex_load", "parameter_impacts_attribute", "attr:hcp",
            "Protein load carries a credible risk to the impurity and viral load and is a WC-CPP; "
            "the load-related risk is localized to the load-material charge-variant quality.",
            "Parameter classification", "Carries a credible risk to the impurity and viral load")
        add("param:aex_flow", "parameter_impacts_attribute", "attr:lrv_mvm",
            "Operating flow rate is controlled as a WC-CPP to preserve the residence time credited for viral clearance.",
            "Parameter classification",
            "Controlled to preserve the minimum residence time credited for the viral-clearance claim")
    else:
        for name in AX_MULTIVARIATE:
            add(AXPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:hcp",
                f"{name} carries a credible impact to the flow-through-pool HCP or the viral log-reduction.",
                "Risk-based prioritization of parameters",
                "a credible main-effect and interaction risk to the flow-through-pool HCP or to the viral log-reduction")
        add("param:aex_flow", "parameter_impacts_attribute", "attr:lrv_mvm",
            "Operating flow rate acts on viral clearance through residence time and is a WC-CPP.",
            "Risk-based prioritization of parameters",
            "acts on the viral-clearance claim through residence time")
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def ax_report_sections(doc_id, file_name, report):
    from app.models.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-008 defines the Stage 1 characterization of the A-Mab anion-exchange polishing step (Step 8).",
               "Purpose and scope", "defines the Stage 1 (Process Design) characterization"),
            st(2, "Five process parameters are characterized; four are studied in the multivariate DoE and the flow rate univariately.",
               "Factors, ranges and study type", "Five parameters are in scope"),
            st(3, "The study uses a full-factorial screen followed by a face-centred central-composite design on a scale-down column.",
               "Response-surface design", "face-centred central-composite design"),
            st(4, "Anion exchange sets the MVM (parvovirus) clearance claim and is a major clearance step for XMuLV, HCP, DNA and leached Protein A.",
               "Quality attributes in scope", "sets one CQA of its own"),
            st(5, "The study must establish a multivariate operating region over which the flow-through-pool HCP and the credited viral clearance are controlled.",
               "Acceptance and decision criteria",
               "a multivariate operating region exists over which the flow-through-pool HCP"),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "All four multivariate parameters and the flow rate are well-controlled CPPs.",
           "Parameter classification", "the four multivariate parameters and the flow rate are all well-controlled CPPs"),
        st(2, "Anion exchange is the principal contributor to the cumulative MVM (parvovirus) clearance claim.",
           "Conclusions", "principal contributor to the cumulative MVM (parvovirus) clearance claim"),
        st(3, "Pool HCP is governed by load pH and the equilibration/wash-1 conductivity through a significant load-pH × conductivity interaction.",
           "Screening: factor effects", "significant load-pH × conductivity interaction"),
        st(4, "The flow-through-pool HCP, XMuLV-clearance and MVM-clearance response-surface models are adequate.",
           "Response-surface models",
           "response-surface models for the flow-through-pool HCP and the XMuLV and MVM log-reduction are adequate"),
        st(5, "In the requalified-load DoE the protein-load × conductivity interaction is statistically absent, confirming the DEV-01 root cause.",
           "Screening: factor effects", "statistically absent"),
        st(6, "Two deviations were recorded and resolved without impact to the operating region or the parameter classifications.",
           "Conclusions", "Two deviations were recorded and resolved"),
    ])]


def ax_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:aex", unit_operation=AXUO_NAME,
        parameters=["param:aex_load_ph", "param:aex_wash1_cond", "param:aex_load_cond", "param:aex_load"],
        quality_attributes_constrained=["attr:lrv_mvm", "attr:lrv_xmulv", "attr:hcp"],
        definition="Multivariate region in load pH, equilibration/wash-1 conductivity, load "
                   "conductivity and protein load over which the flow-through-pool HCP and the "
                   "credited MVM and XMuLV log-reduction are controlled so the drug substance meets "
                   "its HCP limit and its cumulative viral-clearance requirements.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "multivariate region of the four well-controlled CPPs")],
        metadata=meta())]


def ax_inventory(doc_id, file_name, dtype):
    return S.DocumentInventoryItem(
        document_id=doc_id, file_name=file_name, predicted_document_type=dtype,
        product_name_candidates=["A-Mab"], process_name_candidates=[AXUO_NAME],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "anion-exchange chromatography", "viral clearance",
                     "host-cell protein clearance", "design of experiments", "parameter classification"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc_id][0]}'.",
        source_references=[ref(doc_id, file_name, "Title block", "Title block",
                               P.DOC_REGISTRY[doc_id][0])],
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
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "AEX sets one CQA (cumulative MVM clearance); the other QualityAttribute entities are the CQAs it controls/clears.",
            "Deviations (DEV-01 load re-execution; DEV-02 pool-stop correction by modelling + verification runs) are narrative; the annex captures the DoE-grounded entities and the requalified-load results reported.",
            "Process-capability (Cpk) values have no dedicated field; reported as report_sections statements.",
        ],
        inventory=ax_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=ax_studies(doc, f, report=True),
        design_spaces=ax_design_spaces(doc, f),
        report_sections=ax_report_sections(doc, f, report=True),
        assertions=ax_assertions(doc, f, report=True), concepts=ax_concepts())


def main():
    os.makedirs(OUT, exist_ok=True)
    for annex in (build_plan(), build_report(), build_plan_harvest(), build_report_harvest(),
                  build_plan_protein_a(), build_report_protein_a(),
                  build_plan_viral_inactivation(), build_report_viral_inactivation(),
                  build_plan_cex(), build_report_cex(),
                  build_plan_aex(), build_report_aex()):
        path = os.path.join(OUT, f"{annex.document_id}.json")
        with open(path, "w") as fh:
            json.dump(annex.model_dump(mode="json"), fh, indent=2, ensure_ascii=False)
        ne = sum(len(s.process_steps) + len(s.parameters) + len(s.quality_attributes)
                 + len(s.analytical_methods) + len(s.equipment) + len(s.sites) for s in annex.entities)
        print(f"wrote {path}: {ne} entities, {len(annex.studies)} studies, "
              f"{len(annex.assertions.assertions)} assertions, "
              f"{len(annex.concepts.concepts)} concepts")


if __name__ == "__main__":
    main()
