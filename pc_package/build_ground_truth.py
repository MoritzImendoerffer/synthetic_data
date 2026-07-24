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


def main():
    os.makedirs(OUT, exist_ok=True)
    for annex in (build_plan(), build_report()):
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
