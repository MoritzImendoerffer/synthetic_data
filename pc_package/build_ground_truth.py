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
        src = ref(doc_id, file_name, sec, "Executive summary",
                  "The production bioreactor is the step at which the design space for the "
                  "A-Mab drug substance is defined")
    else:
        src = ref(doc_id, file_name, sec, "Purpose and scope",
                  "The step is a fed-batch mammalian cell culture operated at a commercial "
                  "scale of 15,000 L")
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
                               "The scale-down model is a bench-scale stirred-tank bioreactor system "
                               "of the same design family as the commercial vessel" if report
                               else "bench-scale stirred tank bioreactors qualified as a model of the "
                                    "commercial vessel under SOP-1001")],
        metadata=meta())
    vessel = S.Equipment(
        equipment_id="equip:production_bioreactor",
        equipment_name="15,000 L production bioreactor", equipment_type="bioreactor",
        site_name=P.RECEIVING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Product and unit operation" if report else "Purpose and scope",
                               "The production bioreactor is a fed-batch culture operated at "
                               "15,000 L working volume" if report
                               else "a fed-batch mammalian cell culture operated at a commercial "
                                    "scale of 15,000 L")],
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
                                   caption, table_title=caption,
                                   table_id=f"{doc_id}_tab_params")],
            metadata=meta()))
    return out


def build_cqas(doc_id, file_name, sec, report):
    sec_title = "Quality attributes in scope"
    if report:
        quote = table_title = "Quality attributes set or generated at the production bioreactor."
    else:
        quote = table_title = ("Quality attributes formed at the production bioreactor, with drug "
                               "substance acceptance criteria and criticality.")
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
            source_references=[ref(doc_id, file_name, sec, sec_title, quote,
                                   table_title=table_title, table_id=f"{doc_id}_tab_cqa")],
            metadata=meta()))
    return out


# Per-method grounded fragment from the plan's "Analytical methods" section.
METHOD_QUOTE = {
    "AMV-3010": ("The glycan attributes are measured by released N-glycan mapping, which reports "
                 "afucosylation, galactosylation and high mannose from a single injection"),
    "AMV-3011": "aggregates are measured by size exclusion chromatography (SEC-HPLC)",
    "AMV-3012": "Host cell protein is measured by immunoassay",
    "AMV-3013": "acidic charge variants by imaged capillary isoelectric focusing (icIEF)",
    "AMV-3014": "residual DNA by quantitative polymerase chain reaction (qPCR)",
}
# CQA key -> the same fragment, used for the attribute -> method assertions.
CQA_METHOD_QUOTE = {k: METHOD_QUOTE[m] for k, m in CQA_METHOD.items()}

# Per-parameter classification sentence from the report's "Parameter classification"
# section (§9). "Dissolved CO2" is quoted without its leading subscripted name.
CLASS_QUOTE = {
    "Culture pH": ("Culture pH is a WC-CPP, since it is the dominant parameter for high mannose "
                   "and for aggregate and is active for every other response"),
    "Culture temperature": ("Culture temperature is a WC-CPP, since it is active for high mannose, "
                            "galactosylation and acidic variants"),
    "Dissolved CO2 (pCO2)": ("is a WC-CPP, since it carries the largest effect on acidic variants "
                             "and a large effect on galactosylation"),
    "Osmolality": ("Osmolality is a WC-CPP, since it showed a significant effect on acidic "
                   "variants and on galactosylation in screening"),
    "Culture duration": ("Culture duration is a WC-CPP, since it carries the largest single effect "
                         "measured in this study"),
    "Dissolved oxygen": ("Dissolved oxygen is a KPP, because prior platform work links it to "
                         "specific productivity and to titre and not to any attribute formed here"),
    "Initial viable cell conc.": ("found its effect to be on the growth trajectory, on the integral "
                                  "of viable cell concentration and on titre, and not on any "
                                  "quality attribute of this step"),
    "Nutrient feed-1 volume": ("Nutrient feed volume is a KPP, because it governs nutrient "
                               "sufficiency through the production phase and hence titre"),
    "Basal medium concentration": ("Basal medium concentration is a GPP, because platform "
                                   "multivariate work found no link to a quality attribute of "
                                   "this step"),
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
            n_runs=n_scr, n_center_points=3, scale_down_model=SDM,
            associated_parameters=[PARAM_CONCEPT[f] for f in
                                   ["Culture pH", "Culture temperature", "Dissolved CO2 (pCO2)",
                                    "Osmolality", "Culture duration"]],
            source_references=[ref(doc_id, file_name, sec, "Screening design",
                                   "it is of Resolution V, which means that no main effect is "
                                   "aliased with a two-factor interaction" if report
                                   else "The fraction is a half fraction of resolution V, so every "
                                        "main effect and every two-factor interaction is estimable")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:br_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=UO_NAME,
            factors=["Culture pH", "Culture temperature", "Culture duration", "Dissolved CO2 (pCO2)"],
            responses=["afucosylation", "galactosylation", "high_mannose",
                       "acidic_variants", "aggregates_hmw"],
            n_runs=n_rsm, n_center_points=4, scale_down_model=SDM,
            associated_parameters=[PARAM_CONCEPT[f] for f in
                                   ["Culture pH", "Culture temperature", "Culture duration",
                                    "Dissolved CO2 (pCO2)"]],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "Since the axial points sit on the faces of the cube, no run is "
                                   "required outside the characterized range of any factor" if report
                                   else "A face-centred central composite design will be executed")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:br_sdm_qual", study_type="scale_down_qualification", unit_operation=UO_NAME,
            scale_down_model=SDM,
            source_references=[ref(doc_id, file_name, sec,
                                   "Scale-down model and its qualification",
                                   "Qualification compared the small-scale culture with the "
                                   "commercial-equivalent process at target conditions" if report
                                   else "Qualification will compare replicate runs at set-point "
                                        "against the commercial and pilot scale record for the "
                                        "same conditions")],
            metadata=meta()),
        # Both documents carry the univariate assessment of initial viable cell concentration.
        S.StudyDesign(
            study_id="study:br_univariate", study_type="univariate", unit_operation=UO_NAME,
            factors=["Initial viable cell conc."], responses=["process performance"],
            associated_parameters=["param:initial_vcc"],
            source_references=[ref(doc_id, file_name, sec, "Univariate assessment",
                                   "Initial viable cell concentration was assessed one at a time "
                                   "over its characterized range" if report
                                   else "will be assessed one factor at a time")],
            metadata=meta()),
    ]
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
            "Factors, ranges and the knowledge space" if report else "Factors, ranges and study type",
            "gives every parameter of the step with its set-point, its normal operating range, its "
            "characterized range, its final classification and the study that supports it" if report
            else "with their set-points, the ranges to be studied, the normal operating ranges and "
                 "the type of study each will receive")
    cqa_quote = ("Quality attributes set or generated at the production bioreactor." if report else
                 "Quality attributes formed at the production bioreactor, with drug substance "
                 "acceptance criteria and criticality.")
    for r in CQA_ROWS:
        add("step:production_bioreactor", "step_has_quality_attribute", CQA_CONCEPT[r["key"]],
            f"{UO_NAME} sets/controls {r['cqa']}.", "Quality attributes in scope", cqa_quote)
    # attribute -> method (anchored in the plan, which names the method per attribute)
    if not report:
        for r in CQA_ROWS:
            add(CQA_CONCEPT[r["key"]], "attribute_measured_by_method", f"method:{CQA_METHOD[r['key']]}",
                f"{r['cqa']} is measured by {CQA_METHOD[r['key']]}.", "Analytical methods",
                CQA_METHOD_QUOTE[r["key"]])
    # attribute -> acceptance criterion (both docs state acceptance criteria)
    acc_quote = ("with their acceptance criterion, criticality level and Tool #1 score" if report
                 else "Table 4 gives their drug substance acceptance criteria together with the "
                      "criticality assigned to each")
    for r in CQA_ROWS:
        add(CQA_CONCEPT[r["key"]], "attribute_has_acceptance_criterion",
            f"lit:{r['key']}_acc", f"{r['cqa']} acceptance: {r['acc_low']:g}–{r['acc_high']:g} {r['unit']}.",
            "Quality attributes in scope", acc_quote)
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
               "Purpose and scope",
               "This plan defines the process characterization studies for the production bioreactor"),
            st(2, "Nine process parameters are in scope, eight studied multivariately and one univariately.",
               "Factors, ranges and study type",
               "Of the 9 parameters in scope, 8 are assigned to multivariate study and 1 to "
               "univariate assessment."),
            st(3, "The study uses a screening fractional-factorial design followed by a "
                  "face-centred central composite design on a qualified bench-scale scale-down model.",
               "Response-surface design", "A face-centred central composite design will be executed"),
            st(4, "Models are acceptable when there is no significant lack of fit against the center-point pure error.",
               "Acceptance and decision criteria",
               "the lack of fit F test is not significant against pure error at the same level"),
            st(5, "The study must establish a multivariate operating region over which every "
                  "governed attribute is predicted to lie inside its acceptance criterion.",
               "Acceptance and decision criteria",
               "The operating region will be declared as the set of factor combinations over which "
               "the fitted models predict every governed attribute to lie inside its acceptance criterion"),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Culture pH, temperature, dissolved CO2, osmolality and culture duration are classified WC-CPP.",
           "Executive summary", "5 are well-controlled critical process parameters (WC-CPP)"),
        st(2, f"The nominal fed-batch reaches a peak VCD of {P.V['peak_vcd_e6']} x10^6 cells/mL and titer of {P.V['nominal_titer_g_per_l']} g/L.",
           "Product and unit operation", "supports growth to a peak viable cell density of"),
        st(3, "Within the design space the fitted response-surface models predict every measured "
              "attribute inside acceptance, with one galactosylation corner excluded.",
           "Design space",
           "Within that region the fitted response-surface models predict mean attribute levels "
           "inside acceptance"),
        st(4, "The response-surface models are adequate for all five responses and predictive for four of them.",
           "Response-surface models",
           "The response-surface models are adequate for all 5 responses and predictive for four of them"),
        st(5, "There was no significant lack of fit relative to the center-point pure error.",
           "Response-surface models", "Lack of fit is not significant for any response"),
        st(6, "All bioreactor-set CQAs meet acceptance with margin at commercial scale.",
           "Process capability and robustness",
           "The step meets its acceptance criteria at commercial scale with margin on every "
           "attribute it forms"),
    ])]


def build_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:bioreactor", unit_operation=UO_NAME,
        parameters=["param:culture_ph", "param:culture_temperature",
                    "param:culture_duration", "param:dissolved_co2"],
        quality_attributes_constrained=[CQA_CONCEPT[r["key"]] for r in CQA_ROWS],
        definition="The characterized region in culture pH, culture temperature, culture duration "
                   "and dissolved CO2 within which the fitted response-surface models predict every "
                   "measured attribute inside acceptance, with one galactosylation corner excluded.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "The design space for this step is the characterized region in the "
                               "four response-surface factors")],
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
_PAR_GENERAL_QUOTE = ("Every characterized range is a proven acceptable range for every attribute "
                      "this step governs")


def build_proven_acceptable_ranges(doc_id, file_name):
    """One ProvenAcceptableRange per governed CQA x response-surface parameter, from the
    same DoE engine (``doe_report.par_table``) that renders @tbl-par in the report."""
    import doe_report as D
    par = D.par_table(UO)
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
            acceptance_basis=(
                "Drug-substance specification for the CQA (the study's released-glycan, "
                "size-variant or charge-variant limit), applied as the ceiling, floor or "
                "two-sided window; the production bioreactor forms no viral-clearance CQA."),
            source_references=[ref(doc_id, file_name, f"{doc_id}_sec_par", PAR_SEC,
                                   PAR_CQA_QUOTE.get(cqa, _PAR_GENERAL_QUOTE))],
            metadata=meta()))
    return out


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
    qmd = os.path.join(HERE, os.path.splitext(file_name)[0] + ".qmd")
    prose = ""
    if os.path.exists(qmd):
        prose = re.sub(r"\s+", " ", open(qmd, encoding="utf-8").read())
    sec_title = {"results": "Results", "exec_summary": "Executive summary"}
    out, skipped = [], []
    for c in data.get("claims", {}).get(doc_id, []):
        sec = c.get("section")
        quote = " ".join(c["quote"].split())
        if prose and quote not in prose:
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
              f"{os.path.basename(qmd)} and so are not in the annex "
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
    qmd = os.path.join(HERE, os.path.splitext(file_name)[0] + ".qmd")
    prose = ""
    if os.path.exists(qmd):
        prose = re.sub(r"\s+", " ", open(qmd, encoding="utf-8").read())
    out, skipped = [], 0
    for s in data.get("spans", []):
        sec = s.get("section")
        quote = " ".join(s["quote"].split())
        if prose and quote not in prose:
            skipped += 1
            continue
        out.append(S.RhetoricalSpan(
            span_id=s["id"], section=sec, role=s["role"],
            source_reference=ref(doc_id, file_name, f"{doc_id}_sec_{sec}", sec or "body", quote),
            supported_by=s.get("supported_by") or [],
            restates=s.get("restates"), bounds=s.get("bounds")))
    if skipped:
        print(f"WARN  {doc_id}: {skipped} rhetorical span(s) no longer match the document "
              f"and were dropped. Re-curate authoring/rhetorical/{doc_id}.spans.yaml "
              f"against the current text.")
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
           "Executive summary", "are classified well-controlled CPP (WC-CPP)"),
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
           "Executive summary", "classified CPP"),
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
                                   caption, table_title=caption,
                                   table_id=f"{doc_id}_tab_cqa_set" if sets_it
                                   else f"{doc_id}_tab_cqa_cleared")],
            metadata=meta()))
    return out


# Per-method grounded fragment from each document's "Analytical methods" section.
AXMETHOD_QUOTE = {
    False: {  # PCP-008
        "AMV-3012": "Pool host cell protein will be measured by ELISA (AMV-3012)",
        "AMV-3014": "residual DNA by qPCR (AMV-3014)",
        "AMV-3016": "leached Protein A by ELISA (AMV-3016)",
        "AMV-3017": ("Retrovirus and parvovirus titres will be measured by infectivity assay in "
                     "the containment laboratory (AMV-3017 and AMV-3018)"),
        "AMV-3018": ("Retrovirus and parvovirus titres will be measured by infectivity assay in "
                     "the containment laboratory (AMV-3017 and AMV-3018)"),
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
            n_runs=n_scr, n_center_points=3, scale_down_model="scale-down chromatography column",
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
            n_runs=n_rsm, n_center_points=4, scale_down_model="scale-down chromatography column",
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
    param_quote = ("with their set-points, their normal operating ranges, the ranges studied and "
                   "their final classification" if report else
                   "The parameters to be studied, their set-points, their characterization ranges "
                   "and their normal operating ranges are given in")
    for name, cid in AXPARAM_CONCEPT.items():
        add("step:aex", "step_has_parameter", cid,
            f"{AXUO_NAME} has process parameter {name}.", param_sec, param_quote)
    # step sets the MVM clearance CQA; clears XMuLV, HCP, DNA and leached Protein A
    add("step:aex", "step_has_quality_attribute", "attr:lrv_mvm",
        f"{AXUO_NAME} sets the cumulative MVM (parvovirus) clearance claim.",
        "Quality attributes in scope",
        "The step sets one critical quality attribute (CQA)" if report
        else "This step sets one quality attribute")
    cleared_quote = ("The step also clears four attributes that it does not set" if report else
                     "The step also governs several attributes that are formed or set elsewhere")
    for key in ["lrv_xmulv", "hcp", "residual_dna", "leached_protein_a"]:
        add("step:aex", "step_has_quality_attribute", AXATTR_CONCEPT[key],
            f"{AXUO_NAME} clears {AXATTR_NAME[key]}.", "Quality attributes in scope",
            cleared_quote)
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
                "Risk-based prioritization of parameters",
                "the potential impact of the parameter on a critical quality attribute, and its "
                "potential to interact with other parameters")
        add("param:aex_flow", "parameter_impacts_attribute", "attr:lrv_mvm",
            "Operating flow rate acts on this step through residence time and is assessed "
            "univariately.",
            "Univariate assessment",
            "Flow rate acts on this step through residence time")
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def ax_report_sections(doc_id, file_name, report):
    from app.models.summaries import ReportSection, ReportStatement

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
_AX_PAR_GENERAL_QUOTE = ("Each characterized parameter is proven acceptable across its entire "
                         "characterization range, for every quality attribute the step governs")


def ax_proven_acceptable_ranges(doc_id, file_name):
    """One ProvenAcceptableRange per governed CQA x response-surface parameter, from the
    same DoE engine (``doe_report.par_table``) that renders @tbl-par in the report. Pool HCP
    uses the drug-substance specification as its ceiling; the two viral-clearance CQAs use a
    back-calculated step floor (the modular required log-reduction) as the acceptance basis."""
    import doe_report as D
    par = D.par_table(AXUO)
    out = []
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
            acceptance_basis=basis,
            source_references=[ref(doc_id, file_name, f"{doc_id}_sec_par", AX_PAR_SEC,
                                   AX_PAR_CQA_QUOTE.get(cqa, _AX_PAR_GENERAL_QUOTE))],
            metadata=meta()))
    return out


# Argument-structure spans over the PCR-008 report. Each quote is a verbatim, plain-prose
# fragment of the rendered report (no inline expressions, no bold). Tuple fields:
# (suffix, role, section, quote, supported_by-suffixes, restates-suffix, bounds-suffix).
AX_RHET_SPANS = [
    ("R00", "claim", "Executive summary",
     "The step now provides a defined multivariate operating region over which viral clearance "
     "and pool purity both meet their criteria", [], None, None),
    ("R01", "problem_statement", "Executive summary",
     "The step sets the cumulative clearance claim for minute virus of mice (MVM)", [], None, None),
    ("R02", "claim", "Executive summary",
     "all of them were classified as well-controlled critical process parameters (WC-CPP)",
     [], None, None),
    ("R03", "claim", "Parameter classification",
     "No parameter at this step is classified as a critical process parameter, and none is "
     "classified as a key process parameter or a general process parameter", [], None, None),
    ("R04", "mechanistic_warrant", "Mechanistic interpretation",
     "Viral clearance behaves as a charge partitioning process, in which both model viruses are "
     "more strongly retained when they carry more negative charge and when fewer competing "
     "counter-ions are present", [], None, None),
    ("R05", "cross_step_credit", "Executive summary",
     "the cumulative MVM claim also rests on small-virus retentive filtration and the cumulative "
     "XMuLV claim rests on the low-pH hold as well", [], None, None),
    ("R06", "deviation_disposition", "Executive summary",
     "The most serious of them invalidated the first execution of both designs, because the load "
     "material carried an elevated acidic charge variant burden and was not representative of the "
     "commercial feed", [], None, None),
    ("R07", "bounded_conclusion", "Executive summary",
     "None of the three altered a parameter classification or a boundary of the operating region",
     [], None, None),
    ("R08", "deferral", "Executive summary",
     "contribution is consolidated with the rest of the train in PCMR-001", [], None, None),
    ("R09", "mechanistic_warrant", "Mechanistic interpretation",
     "at a higher pH the weakly acidic species carry more negative charge and remain bound even "
     "when the wash conductivity is raised, which is why the two sets of contours converge",
     [], None, None),
    ("R10", "mechanistic_warrant", "Mechanistic interpretation",
     "Its governing parameter is the conductivity of the equilibration and wash-1 buffer and not "
     "the conductivity of the load", [], None, None),
    ("R11", "claim", "Screening: factor effects",
     "Pool HCP is governed by two factors and by their interaction", ["R09", "R10"], None, None),
    ("R12", "justification", "Response-surface models",
     "because it is estimated with curvature in the model and on a design that supports it",
     [], None, None),
    ("R13", "hedge", "Response-surface models",
     "which suggests a slight flattening of the surface at high pH without providing evidence "
     "for it", [], None, None),
    ("R14", "hedge", "Centre-point performance and reproducibility",
     "most of the observed centre-point scatter in this response is analytical and not processing "
     "variation", [], None, None),
    ("R15", "bounded_conclusion", "Design space",
     "Three bounds apply to the design space claim.", [], None, None),
    ("R16", "claim", "Proven acceptable ranges",
     "The two analyses coincide in every row, and both equal the characterization range",
     [], None, None),
    ("R17", "bounded_conclusion", "Proven acceptable ranges",
     "That result is not a statement that any combination of extremes is acceptable",
     [], None, "R16"),
    ("R18", "cross_step_credit", "Contribution to the control strategy",
     "the cumulative MVM claim requires small-virus retentive filtration and the cumulative XMuLV "
     "claim requires the low-pH hold as well", [], None, None),
    ("R19", "deferral", "Contribution to the control strategy",
     "All contributions are consolidated in PCMR-001", [], None, None),
    ("R20", "deviation_disposition", "Non-representative load material in the first execution",
     "The first execution is retained as a controlled record and is referenced here only to "
     "confirm the root cause. It is not used in any analysis in this report", [], None, None),
    ("R21", "justification", "Collection criterion on the descending edge",
     "The verification demonstrates that the region holds at the corrected collection criterion",
     [], None, None),
    ("R22", "restatement", "Conclusions",
     "The anion exchange step is well characterized and robust over the ranges studied",
     [], "R00", None),
    ("R23", "bounded_conclusion", "Conclusions",
     "The step does not assure viral safety on its own, and it makes no claim for glycan variants, "
     "charge variants or aggregate", [], None, None),
    ("R24", "deviation_disposition", "Equilibration and wash-1 buffer pH excursion",
     "The deviation was retained with no re-execution", [], None, None),
]


def ax_rhetorical_spans(doc_id, file_name):
    """Rhetorical / argument-structure spans over the PCR-008 report (report-only)."""
    out = []
    for suffix, role, sec, quote, sup, res, bnd in AX_RHET_SPANS:
        out.append(S.RhetoricalSpan(
            span_id=f"{doc_id}-{suffix}", section=sec, role=role,
            source_reference=ref(doc_id, file_name, f"{doc_id}_sec_rhet", sec,
                                 " ".join(quote.split())),
            supported_by=[f"{doc_id}-{s}" for s in sup],
            restates=(f"{doc_id}-{res}" if res else None),
            bounds=(f"{doc_id}-{bnd}" if bnd else None)))
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
        rhetorical_spans=ax_rhetorical_spans(doc, f))


# =========================================================================== #
# Small-Virus Retentive Filtration (Step 9) — PCP-009 / PCR-009.                #
# --------------------------------------------------------------------------- #
# Additive, self-contained builders for the virus-filtration DoE pair. Like     #
# CEX, the step sets NO CQA: it is the dedicated small-virus removal step and    #
# the principal contributor to the cumulative MVM (parvovirus) log-reduction,    #
# with a major enveloped-virus (XMuLV) log-reduction, all credited as           #
# orthogonal/modular clearance under ICH Q5A(R2). The DoE is a compact           #
# two-factor full-factorial screen + face-centred CCD in volumetric load /       #
# filtration pressure; both parameters are WC-CPP (load governs the credited     #
# MVM clearance; pressure is controlled to preserve filter performance and       #
# retention, confirmed by a post-use integrity test). No univariate parameter.   #
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
                  "small-virus retentive filtration step (Step 9)")
    else:
        src = ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                  "the dedicated virus-removal step of the A-Mab purification train")
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
                               "qualified scale-down virus-filtration model" if report
                               else "scale-down virus-filtration model")],
        metadata=meta())
    if report:
        return [sdm]
    return [
        S.Equipment(equipment_id="equip:vf_filter",
                    equipment_name="commercial-scale small-virus retentive filter",
                    equipment_type="virus-retentive filter", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec, "Purpose and scope",
                                           "commercial-scale small-virus retentive filtration step")],
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
    caption = ("Virus-filtration process parameters, set-points, ranges and post-characterization classification."
               if classified else
               "Virus-filtration parameters, set-points, characterization ranges and planned study type.")
    rats = {"WC-CPP": "Governs the credited MVM log-reduction (the volumetric-load limit) or is "
                      "controlled within a defined range to preserve filter performance and the "
                      "validated retention; reliably controlled within the operating region."}
    out = []
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
                                   caption, table_title=caption,
                                   table_id=f"{doc_id}_tab_params")],
            metadata=meta()))
    return out


def vf_cqas(doc_id, file_name, sec, report):
    quotes = {"lrv_mvm": "the principal MVM-removal mechanism"}
    default_quote = "principal clearance step for the two model viruses"
    out = []
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
                                   quotes.get(key, default_quote),
                                   table_title="Viral-clearance CQAs to which the virus-filtration step contributes",
                                   table_id=f"{doc_id}_tab_cqa")],
            metadata=meta()))
    return out


def vf_methods(doc_id, file_name, sec, report):
    quote = "measured by validated methods" if report else "measured by the validated methods"
    out = []
    for mid, mname, mtype, analytes, attrs in VFMETHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[VFATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods", quote)],
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
            n_runs=n_scr, n_center_points=3, scale_down_model="scale-down filtration model",
            associated_parameters=[VFPARAM_CONCEPT[f] for f in VF_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Screening design",
                                   "a two-level full factorial in the two factors")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vf_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=VFUO_NAME,
            factors=VF_MULTIVARIATE, responses=responses,
            n_runs=n_rsm, n_center_points=4, scale_down_model="scale-down filtration model",
            associated_parameters=[VFPARAM_CONCEPT[f] for f in VF_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "face-centred central-composite")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vf_sdm_qual", study_type="scale_down_qualification",
            unit_operation=VFUO_NAME, scale_down_model="scale-down filtration model",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "qualified against at-scale reference data")],
            metadata=meta()),
    ]


def vf_concepts():
    from app.models.concepts import Concept, ConceptStore
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
    param_quote = "Two parameters were studied" if report else "Two parameters are in scope"
    for name, cid in VFPARAM_CONCEPT.items():
        add("step:virus_filtration", "step_has_parameter", cid,
            f"{VFUO_NAME} has process parameter {name}.", param_sec, param_quote)
    # step is the principal MVM-removal mechanism; a major clearance step for XMuLV
    add("step:virus_filtration", "step_has_quality_attribute", "attr:lrv_mvm",
        f"{VFUO_NAME} is the principal contributor to the cumulative MVM (parvovirus) clearance.",
        "Quality attributes in scope", "the principal MVM-removal mechanism")
    add("step:virus_filtration", "step_has_quality_attribute", "attr:lrv_xmulv",
        f"{VFUO_NAME} is a major clearance step for enveloped virus (XMuLV).",
        "Quality attributes in scope", "principal clearance step for the two model viruses")
    # attribute -> method (plan only; the report does not restate the linkage)
    if not report:
        for key in VF_CQA_METHOD:
            add(VFATTR_CONCEPT[key], "attribute_measured_by_method", f"method:{VF_CQA_METHOD[key]}",
                f"{VFATTR_NAME[key]} is measured by {VF_CQA_METHOD[key]}.", "Analytical methods",
                "measured by the validated methods")
    # acceptance criterion for the CQA the step principally drives
    mvm = _vf_cqa_row("lrv_mvm")
    add("attr:lrv_mvm", "attribute_has_acceptance_criterion", "lit:lrv_mvm_acc",
        f"MVM clearance acceptance: ≥ {mvm['acc_low']:g} {mvm['unit']} (cumulative).",
        "Quality attributes in scope", "acceptance criterion")
    # parameter -> attribute impacts / non-impacts
    if report:
        add("param:vf_filtration_volume", "parameter_impacts_attribute", "attr:lrv_mvm",
            "Volumetric load is the single significant factor for the credited MVM log-reduction "
            "and defines the volumetric-load limit (WC-CPP).",
            "Parameter classification", "The single significant factor for the credited MVM log-reduction")
        add("param:vf_pressure", "parameter_does_not_significantly_impact_attribute", "attr:lrv_mvm",
            "Filtration pressure has no significant effect on retention over the range studied but "
            "is controlled within a defined range to preserve filter performance and retention (WC-CPP).",
            "Parameter classification", "No significant effect on retention over the range studied")
    else:
        for name in VF_MULTIVARIATE:
            add(VFPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:lrv_mvm",
                f"{name} carries a credible risk to the credited viral log-reduction or must be "
                f"controlled to preserve filter performance.",
                "Risk-based prioritization of parameters",
                "a credible risk to the credited viral log-reduction")
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def vf_report_sections(doc_id, file_name, report):
    from app.models.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-009 defines the Stage 1 characterization of the A-Mab small-virus retentive filtration step (Step 9).",
               "Purpose and scope", "defines the Stage 1 (Process Design) characterization"),
            st(2, "Two process parameters (volumetric load and filtration pressure) are characterized in a compact two-factor DoE.",
               "Factors, ranges and study type", "Two parameters are in scope"),
            st(3, "The study uses a full-factorial screen followed by a face-centred central-composite design on a scale-down filtration model.",
               "Response-surface design", "face-centred central-composite design"),
            st(4, "Virus filtration is the principal contributor to the cumulative MVM clearance and a major contributor to the XMuLV clearance.",
               "Purpose and scope", "principal contributor to the cumulative MVM (parvovirus) log-reduction"),
            st(5, "The study must establish a volumetric-load limit over which the credited small-virus log-reduction is preserved.",
               "Acceptance and decision criteria",
               "a volumetric-load limit exists at or below which the credited MVM log-reduction is preserved"),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Both process parameters (volumetric load and filtration pressure) are well-controlled CPPs.",
           "Executive summary", "Both parameters are classified"),
        st(2, "The MVM (parvovirus) log-reduction declines with increasing volumetric load and is insensitive to pressure.",
           "Executive summary", "declines with increasing volumetric load and is insensitive to filtration pressure"),
        st(3, "The enveloped virus (XMuLV) is retained essentially completely across the design, with no breakthrough.",
           "Mechanistic interpretation", "retained essentially completely"),
        st(4, "The MVM log-reduction response-surface model is adequate and identifies the volumetric load as the single significant factor.",
           "Response-surface model", "identifies the volumetric load as the single significant factor"),
        st(5, "Virus filtration is the principal contributor to the drug-substance MVM-clearance capability.",
           "Process capability and robustness", "the principal contributor"),
        st(6, "The credited viral log-reduction is substantiated conservatively at the worst-case (maximum-load) condition per ICH Q5A(R2).",
           "Executive summary", "substantiated conservatively at the worst-case"),
    ])]


def vf_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:vf", unit_operation=VFUO_NAME,
        parameters=["param:vf_filtration_volume", "param:vf_pressure"],
        quality_attributes_constrained=["attr:lrv_mvm"],
        definition="Operating region defined principally by a volumetric-load limit: the credited "
                   "MVM log-reduction is preserved with margin at or below the upper NOR bound on "
                   "volumetric load, with filtration pressure controlled within its NOR, over which "
                   "retention is insensitive to pressure.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "defined principally by a volumetric-load limit")],
        metadata=meta())]


def vf_inventory(doc_id, file_name, dtype):
    return S.DocumentInventoryItem(
        document_id=doc_id, file_name=file_name, predicted_document_type=dtype,
        product_name_candidates=["A-Mab"], process_name_candidates=[VFUO_NAME],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "virus filtration", "viral clearance",
                     "small-virus retention", "design of experiments", "parameter classification"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc_id][0]}'.",
        source_references=[ref(doc_id, file_name, "Title block", "Title block",
                               P.DOC_REGISTRY[doc_id][0])],
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
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Virus filtration sets no CQA; the QualityAttribute entities are the viral-clearance CQAs it controls/clears (cumulative, cross-step).",
            "Per-step MVM/XMuLV log-reductions are modular contributions with no released spec; reported via studies/report_sections.",
            "Process-capability (Cpk) values have no dedicated field; reported as report_sections statements.",
        ],
        inventory=vf_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=vf_studies(doc, f, report=True),
        design_spaces=vf_design_spaces(doc, f),
        report_sections=vf_report_sections(doc, f, report=True),
        assertions=vf_assertions(doc, f, report=True), concepts=vf_concepts())


# =========================================================================== #
# Ultrafiltration / Diafiltration (Step 10) — PCP-010 / PCR-010.                #
# --------------------------------------------------------------------------- #
# Additive, self-contained builders for the non-DoE UF/DF pair. Like harvest,   #
# UF/DF forms no product-quality CQA, so there are no QualityAttribute entities  #
# and no design space; it is a formulation / mass-balance operation evaluated    #
# univariately. It monitors the size- and charge-variant attributes to confirm   #
# they are unchanged. The formulation characterization proper is reported under  #
# the drug-product program (out of scope of this drug-substance pair).           #
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


def uf_step(doc_id, file_name, sec, report):
    if report:
        src = ref(doc_id, file_name, sec, "Executive summary",
                  "final ultrafiltration / diafiltration (UF/DF) operation (Step 10)")
    else:
        src = ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                  "the final drug-substance operation of the A-Mab train")
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
        equipment=["ultrafiltration / diafiltration membrane (TFF)", "bench-scale UF/DF model"],
        source_references=[src], metadata=meta())


def uf_equipment(doc_id, file_name, sec, report):
    membrane = S.Equipment(
        equipment_id="equip:ufdf_membrane",
        equipment_name="ultrafiltration / diafiltration membrane (TFF)",
        equipment_type="tangential-flow-filtration membrane", site_name=P.RECEIVING_SITE,
        source_references=[ref(doc_id, file_name, sec, "Operation",
                               "concentrated by ultrafiltration")],
        metadata=meta())
    sdm = S.Equipment(
        equipment_id="equip:ufdf_sdm", equipment_name="bench-scale UF/DF model",
        equipment_type="ultrafiltration / diafiltration (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec, "Scale-down model and its qualification",
                               "qualified bench-scale UF/DF (tangential-flow-filtration) model")],
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
    caption = ("UF/DF process parameters, set-points, ranges and post-characterization classification."
               if classified else
               "UF/DF parameters, set-points, characterization ranges and planned study type.")
    rats = {"KPP": "Governs buffer-exchange completeness, permeate flux/process time or the final "
                   "concentration (process performance) without a drug-substance CQA impact."}
    out = []
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
                                   "Parameters, ranges and the knowledge space" if classified
                                   else "Parameters, ranges and study type",
                                   caption, table_title=caption,
                                   table_id=f"{doc_id}_tab_params")],
            metadata=meta()))
    return out


def uf_methods(doc_id, file_name, sec, report):
    quote = "measured by validated methods" if report else "measured by the validated methods"
    out = []
    for mid, mname, mtype, analytes, attrs in UFMETHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[UFATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods", quote)],
            metadata=meta()))
    return out


def uf_studies(doc_id, file_name, report):
    sec = "Study design"
    return [
        S.StudyDesign(
            study_id="study:ufdf_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=UFUO_NAME,
            factors=["Number of diavolumes", "Transmembrane pressure", "Final DS concentration"],
            responses=["step yield", "buffer-exchange completeness", "final DS concentration"],
            scale_down_model="bench-scale UF/DF model",
            associated_parameters=list(UFPARAM_CONCEPT.values()),
            source_references=[ref(doc_id, file_name, sec, sec, "one factor at a time")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:ufdf_sdm_qual", study_type="scale_down_qualification",
            unit_operation=UFUO_NAME, scale_down_model="bench-scale UF/DF model",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "qualified against at-scale reference data")],
            metadata=meta()),
    ]


def uf_concepts():
    from app.models.concepts import Concept, ConceptStore
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
    from app.models.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote)], metadata=meta()))

    param_quote = ("parameters were evaluated" if report else "parameters are in scope")
    param_sec = ("Parameters, ranges and the knowledge space" if report
                 else "Parameters, ranges and study type")
    for name, cid in UFPARAM_CONCEPT.items():
        add("step:ufdf", "step_has_parameter", cid,
            f"{UFUO_NAME} has process parameter {name}.", param_sec, param_quote)
    # UF/DF monitors (does not set) the product-quality attributes to confirm they are unchanged
    for key, cid in UFATTR_CONCEPT.items():
        add("step:ufdf", "step_has_quality_attribute", cid,
            f"{UFUO_NAME} monitors {UFATTR_NAME[key]} to confirm it is unchanged across the operation.",
            "Quality attributes and process-performance measures",
            "sets or modifies no drug-substance product-quality CQA")
    # attribute -> method (methods that measure a product-quality attribute)
    for mid, mname, mtype, analytes, attrs in UFMETHODS:
        for a in attrs:
            add(UFATTR_CONCEPT[a], "attribute_measured_by_method", f"method:{mid}",
                f"{UFATTR_NAME[a]} is measured by {mid}.", "Analytical methods",
                "measured by validated methods" if report else "measured by the validated methods")
    # no-CQA-impact of the operating parameters (both docs make this claim)
    no_impact_quote = ("none significantly impacts any drug-substance CQA" if report
                       else "no credible risk of impact to a drug-substance product-quality CQA")
    no_impact_sec = ("Parameter classification" if report
                     else "Risk-based prioritization of parameters")
    for name, cid in UFPARAM_CONCEPT.items():
        add(cid, "parameter_does_not_significantly_impact_attribute", "attr:aggregates_hmw",
            f"{name} has no significant drug-substance product-quality (CQA) impact.",
            no_impact_sec, no_impact_quote)
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def uf_report_sections(doc_id, file_name, report):
    from app.models.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-010 defines the Stage 1 evaluation of the A-Mab final ultrafiltration / diafiltration operation (Step 10).",
               "Purpose and scope", "defines the Stage 1 (Process Design) evaluation"),
            st(2, "UF/DF has no impact on the drug-substance product-quality CQAs, which pass through unchanged.",
               "Objectives", "no impact on the drug-substance product-quality CQAs"),
            st(3, "Each parameter is evaluated one factor at a time across its characterization range.",
               "Risk-based prioritization of parameters", "one factor at a time"),
            st(4, "The operation is evaluated against process-performance measures because it sets no drug-substance CQA.",
               "Quality attributes and process-performance measures", "sets or modifies no drug-substance product-quality CQA"),
            st(5, "The formulation characterization is conducted and reported under the drug-product development program.",
               "Purpose and scope", "drug-product development program"),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "UF/DF sets or modifies no drug-substance product-quality CQA; the CQAs pass through unchanged.",
           "Quality attributes and process-performance measures", "sets or modifies no drug-substance product-quality CQA"),
        st(2, "The operation concentrates and buffer-exchanges the pool to the drug-substance target.",
           "No product-quality impact", "no drug-substance product-quality impact"),
        st(3, "The drug substance is delivered at its target concentration.",
           "Process performance and consistency", "delivers drug substance of consistent concentration"),
        st(4, "The number of diavolumes, the transmembrane pressure and the final DS concentration are all KPP.",
           "Parameter classification", "final DS concentration — KPP"),
        st(5, "No UF/DF parameter is a CPP because the operation forms no drug-substance product-quality attribute.",
           "Parameter classification", "No UF/DF parameter is a CPP"),
        st(6, "This report rolls up into the Process Characterization Master Report (PCMR-001).",
           "Conclusions", "rolls up into the Process Characterization Master Report"),
    ])]


def uf_inventory(doc_id, file_name, dtype):
    return S.DocumentInventoryItem(
        document_id=doc_id, file_name=file_name, predicted_document_type=dtype,
        product_name_candidates=["A-Mab"], process_name_candidates=[UFUO_NAME],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "ultrafiltration", "diafiltration",
                     "formulation", "tangential-flow filtration", "parameter classification"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc_id][0]}'.",
        source_references=[ref(doc_id, file_name, "Title block", "Title block",
                               P.DOC_REGISTRY[doc_id][0])],
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
            "UF/DF forms no drug-substance product-quality CQA; no QualityAttribute entities or DesignSpace are present.",
            "Process-performance measures (yield, buffer-exchange completeness, final concentration) have no dedicated field; captured via report_sections/assertions.",
            "Formulation characterization is reported under the drug-product program (out of scope of this DS pair).",
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
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "UF/DF forms no drug-substance product-quality CQA; no QualityAttribute entities or DesignSpace are present.",
            "Process-performance results (step yield, final concentration) have no dedicated field; reported as report_sections statements.",
            "Formulation characterization is reported under the drug-product program (out of scope of this DS pair).",
        ],
        inventory=uf_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=uf_studies(doc, f, report=True),
        report_sections=uf_report_sections(doc, f, report=True),
        assertions=uf_assertions(doc, f, report=True), concepts=uf_concepts())


# =========================================================================== #
# PTP-001 — Process Transfer Plan (Cambridge Development -> Grafton Commercial). #
# --------------------------------------------------------------------------- #
# A corpus-spanning document (not a single unit op): the ground truth captures  #
# the two sites, the process train (Steps 3-10), the CQAs preserved across the  #
# transfer, and — the distinctive object for this document type — the transfer  #
# gaps (TransferGap + transfer_has_gap assertions).                              #
# =========================================================================== #
PTP_FILE = "PTP-001_transfer.docx"

# (gap_id, gap_area, description, impact, mitigation, status, verbatim-quote)
PTP_GAPS = [
    ("GAP-01", "equipment",
     "The commercial-scale chromatography skids and production bioreactor at the receiving site "
     "differ in make and control system from the development equipment.",
     "Operating ranges and control response may differ at commercial scale.",
     "Engineering runs and equipment qualification confirm that the CPP and WC-CPP ranges transfer.",
     "open", "commercial-scale chromatography skids and production bioreactor"),
    ("GAP-02", "analytical_method",
     "The validated release and characterization methods must be transferred and co-validated at "
     "the receiving-site QC laboratory.",
     "Method bias between sites could confound the comparability assessment.",
     "Method-transfer protocols with cross-site precision and accuracy acceptance criteria are executed before PPQ.",
     "in_progress", "transferred and co-validated at the receiving-site QC laboratory"),
    ("GAP-03", "facility",
     "The Grafton commercial drug-substance facility and its utilities require qualification for A-Mab manufacture.",
     "Facility fit, segregation and environmental controls must be demonstrated for the process.",
     "Facility, utility and equipment qualification is completed before the engineering and PPQ batches.",
     "open", "facility and its utilities require qualification for A-Mab manufacture"),
    ("GAP-04", "materials",
     "The resin, virus-retentive membrane, depth-filter media and cell-culture media/feed lots at "
     "commercial scale differ from the development lots.",
     "Raw-material and consumable lot-to-lot variability could affect clearance, yield or product quality.",
     "Raw-material and consumable lot bridging with incoming specifications and resin/membrane life-cycle control is applied.",
     "open", "differ from the development lots"),
    ("GAP-05", "process",
     "The characterized CPPs, WC-CPPs and the multivariate design spaces must be confirmed at commercial scale.",
     "Scale effects on the design space and on the cumulative viral clearance must be verified.",
     "The Stage-2 PPQ campaign confirms the CPP ranges, the design spaces and the cumulative viral clearance at commercial scale.",
     "open", "must be confirmed at commercial scale"),
    ("GAP-06", "control_strategy",
     "The per-CQA control strategy defined during characterization must be implemented in the "
     "receiving-site master batch records and in-process-control plan.",
     "Incomplete transfer of in-process controls and limits could weaken the control of a CQA.",
     "The control strategy is transferred by mapping every in-process control and limit into the master batch records and confirming them in PPQ.",
     "in_progress", "must be implemented in the"),
]
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
                               P.DOC_REGISTRY["PTP-001"][0])],
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
    out = []
    for key in PTP_STEP_KEYS:
        uo = P.CFG.unit_op(key)
        title = P.UNIT_OP_TITLES.get(key, uo.name)
        out.append(S.ProcessStep(
            step_id=f"step:{key}", step_name=title, step_number=str(uo.step),
            unit_operation=title, description=P.UNIT_OP_ROLE.get(key, ""),
            source_references=[ref("PTP-001", PTP_FILE, "PTP-001_sec_process",
                                   "Product and process description", title)],
            metadata=meta()))
    return out


def ptp_cqas():
    out = []
    for r in PTP_CQA_ROWS:
        out.append(S.QualityAttribute(
            attribute_id=f"attr:{r['key']}", attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"], acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref("PTP-001", PTP_FILE, "PTP-001_sec_process",
                                   "Product and process description", r["cqa"],
                                   table_title="Drug-substance CQAs preserved across the transfer",
                                   table_id="PTP-001_tab_cqa")],
            metadata=meta()))
    return out


def ptp_gaps():
    out = []
    for gid, area, desc, impact, mit, status, quote in PTP_GAPS:
        out.append(S.TransferGap(
            gap_id=gid, gap_area=area, description=desc, impact=impact, mitigation=mit,
            status=status,
            source_references=[ref("PTP-001", PTP_FILE, "PTP-001_sec_gaps", "Gap analysis", quote)],
            metadata=meta()))
    return out


def ptp_concepts():
    from app.models.concepts import Concept, ConceptStore
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
    from app.models.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"PTP-001-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref("PTP-001", PTP_FILE, "PTP-001_sec", sec, quote)], metadata=meta()))

    for key in PTP_STEP_KEYS:
        uo = P.CFG.unit_op(key)
        title = P.UNIT_OP_TITLES.get(key, uo.name)
        add("process:amab_ds", "process_has_step", f"step:{key}",
            f"The A-Mab drug-substance process has the step {title}.",
            "Product and process description", title)
    for gid, area, desc, impact, mit, status, quote in PTP_GAPS:
        add("transfer:amab_ds", "transfer_has_gap", f"gap:{gid}",
            f"The transfer has {area} gap {gid}: {desc}", "Gap analysis", quote)
    # a couple of preserved-CQA acceptance-criterion links
    for key in ["lrv_mvm", "hcp"]:
        r = P.cqa_reg[P.cqa_reg.key == key].iloc[0].to_dict()
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{key}_acc",
            f"{r['cqa']} acceptance: {r['acc_low']:g}–{r['acc_high']:g} {r['unit']}.",
            "Product and process description", "acceptance criteria")
    return AssertionStore(run_id="gt-PTP-001", assertions=A, rationales=[])


def ptp_report_sections():
    from app.models.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"PTP-001-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref("PTP-001", PTP_FILE, "PTP-001_sec", sec, quote)])
    return [ReportSection(section_id="PTP-001-summary", title="Transfer plan summary", statements=[
        st(1, "PTP-001 defines the strategy and scope for transferring the A-Mab drug-substance process from the sending site to the receiving site.",
           "Purpose and scope", "strategy and scope for transferring the A-Mab drug-substance"),
        st(2, "The transfer is a knowledge transfer of the characterized process understanding, confirmed by site-equivalency analysis, engineering runs and a commercial-scale PPQ campaign.",
           "Transfer strategy", "knowledge transfer"),
        st(3, "The commercial process operates at 15,000 L and delivers approximately 54.6 kg of drug substance.",
           "Product and process description", "kg of drug substance"),
        st(4, "Of the 37 process parameters, 21 are critical and their commercial-scale control must be confirmed.",
           "Transfer of the manufacturing process", "are critical"),
        st(5, "The gap analysis identifies the differences that must be resolved before or during the transfer.",
           "Gap analysis", "differences that must be resolved"),
        st(6, "Commercial-scale confirmation is provided by a Stage-2 PPQ campaign and reported in PCMR-001.",
           "PPQ and batch strategy", "Stage-2 process performance qualification"),
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
            "The distinctive objects are the TransferGap entries (transfer_has_gap assertions).",
            "CPP/WC-CPP counts and the commercial-scale capability are reported as report_sections statements (no dedicated field).",
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


def ra_cqa_entities():
    out = []
    for r in P.cqa_reg.to_dict("records"):
        out.append(S.QualityAttribute(
            attribute_id=f"attr:{r['key']}", attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"], acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            rationale_for_criticality=f"A-Mab Tool #1 = Impact × Uncertainty = {int(r['tool1_score'])}; "
                                      f"Tool #2 severity = {int(r['tool2_severity'])}.",
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref("RA-001", RA_FILE, "RA-001_sec_cqa", "CQA criticality framework",
                                   r["cqa"], table_title="Drug-substance CQA criticality framework",
                                   table_id="RA-001_tab_cqa")],
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
            source_references=[ref("RA-001", RA_FILE, "RA-001_sec_rank",
                                   "Process-parameter risk ranking and study-type assignment",
                                   r["param"], table_title="Pre-characterization risk ranking",
                                   table_id="RA-001_tab_rank")],
            metadata=meta()))
    return out


def ra_concepts(rows):
    from app.models.concepts import Concept, ConceptStore
    cs = []
    for r in rows:
        cs.append(Concept(concept_id=f"param:{r['key']}_{r['pkey']}",
                          concept_type="PROCESS_PARAMETER", canonical_name=r["param"],
                          review_status="human_verified"))
    for key, name in RA_ATTR_NAME.items():
        cs.append(Concept(concept_id=f"attr:{key}", concept_type="QUALITY_ATTRIBUTE",
                          canonical_name=name, aliases=[key], review_status="human_verified"))
    return ConceptStore(run_id="gt-ra", concepts=cs)


def ra_assertions(quality_rows, perf_rows):
    from app.models.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"RA-001-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref("RA-001", RA_FILE, "RA-001_sec", sec, quote)], metadata=meta()))

    for r in quality_rows:
        pid = f"param:{r['key']}_{r['pkey']}"
        for cqa_key in r["cqas"]:
            add(pid, "parameter_impacts_attribute", f"attr:{cqa_key}",
                f"{r['param']} carries a prospective risk to {RA_ATTR_NAME.get(cqa_key, cqa_key)} "
                f"(pre-characterization).",
                "Process-parameter risk ranking and study-type assignment",
                "carry a credible prospective risk to a CQA")
    for r in perf_rows:
        pid = f"param:{r['key']}_{r['pkey']}"
        add(pid, "parameter_does_not_significantly_impact_attribute", "attr:aggregates_hmw",
            f"{r['param']} carries no credible CQA risk and affects only process performance.",
            "Process-parameter risk ranking and study-type assignment",
            "affect only process performance")
    return AssertionStore(run_id="gt-RA-001", assertions=A, rationales=[])


def ra_report_sections():
    from app.models.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"RA-001-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref("RA-001", RA_FILE, "RA-001_sec", sec, quote)])
    return [ReportSection(section_id="RA-001-summary", title="Risk assessment summary", statements=[
        st(1, "RA-001 prioritizes the A-Mab process parameters for characterization and assigns each a study type before the studies are executed.",
           "Purpose and scope", "prioritizes the A-Mab drug-substance process parameters"),
        st(2, "It is the first, pre-hoc risk assessment of the A-Mab lifecycle of iterative risk assessments.",
           "Purpose and scope", "lifecycle of iterative risk assessments"),
        st(3, "The assessment does not classify parameters as CPP/WC-CPP/KPP/GPP — that is an output of the characterization studies.",
           "Purpose and scope", "does not classify parameters"),
        st(4, "Of the 37 parameters, 21 carry a credible prospective risk to a CQA and are prioritized for study.",
           "Process-parameter risk ranking and study-type assignment", "carry a credible prospective risk to a CQA"),
        st(5, "Parameters carrying a credible CQA risk are assigned to a multivariate DoE.",
           "Characterization scope", "assigned to a multivariate DoE"),
        st(6, "The characterization scope is carried into each Process Characterization Plan.",
           "Characterization scope", "carried into each Process Characterization Plan"),
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
                               P.DOC_REGISTRY["RA-001"][0])],
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
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_rank",
                                  parameters=ra_param_entities(quality_rows + perf_rows)),
    ]
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Pre-characterization: parameter_type is left 'unclassified' (CPP/WC-CPP/KPP/GPP is an OUTPUT of the studies, not this assessment).",
            "The study-type assignment (multivariate DoE / justified univariate / univariate) and the prospective severity/initial-RPN ranking are reported via report_sections and parameter rationales.",
            "parameter_impacts_attribute here is a PROSPECTIVE (at-risk) relation, not a demonstrated effect.",
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


def _corpus_steps(doc, file, sec_id, sec_title):
    out = []
    for key in P.CFG.train_order:
        uo = P.CFG.unit_op(key)
        title = P.UNIT_OP_TITLES.get(key, uo.name)
        out.append(S.ProcessStep(
            step_id=f"step:{key}", step_name=title, step_number=str(uo.step),
            unit_operation=title, description=P.UNIT_OP_ROLE.get(key, ""),
            source_references=[ref(doc, file, sec_id, sec_title, title)], metadata=meta()))
    return out


def _corpus_cqas(doc, file, sec_id, sec_title, table_title, table_id):
    out = []
    for r in P.cqa_reg.to_dict("records"):
        out.append(S.QualityAttribute(
            attribute_id=f"attr:{r['key']}", attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"], acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref(doc, file, sec_id, sec_title, r["cqa"],
                                   table_title=table_title, table_id=table_id)],
            metadata=meta()))
    return out


def _corpus_step_concepts():
    from app.models.concepts import Concept
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
    from app.models.assertions import AssertionStore, EvidenceBackedAssertion
    from app.models.concepts import ConceptStore
    from app.models.summaries import ReportSection, ReportStatement
    doc, f = "PCMP-001", PCMP_FILE
    A, n = [], [0]

    def add(subj, pred, obj, text, sec, quote):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text, source_references=[ref(doc, f, f"{doc}_sec", sec, quote)],
            metadata=meta()))
    for key in P.CFG.train_order:
        uo = P.CFG.unit_op(key)
        title = P.UNIT_OP_TITLES.get(key, uo.name)
        add("process:amab_ds", "process_has_step", f"step:{key}",
            f"The A-Mab drug-substance process has the step {title}.",
            "Overall characterization strategy", title)
    for key in ["lrv_mvm", "hcp", "aggregates_hmw"]:
        r = P.cqa_reg[P.cqa_reg.key == key].iloc[0].to_dict()
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{key}_acc",
            f"{r['cqa']} acceptance: {r['acc_low']:g}–{r['acc_high']:g} {r['unit']}.",
            "CQA framework", r["cqa"])

    def stx(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc, f, f"{doc}_sec", sec, quote)])
    report_sections = [ReportSection(section_id=f"{doc}-summary", title="Master plan summary", statements=[
        stx(1, "PCMP-001 is the umbrella plan governing the Stage 1 process characterization of the A-Mab drug-substance process.",
            "Purpose and scope", "umbrella plan governing the Stage 1"),
        stx(2, "The characterization covers 37 process parameters against 10 drug-substance CQAs on qualified scale-down models.",
            "Purpose and scope", "process parameters against"),
        stx(3, "The study scope and study-type assignment are set by the Pre-Characterization Process Risk Assessment (RA-001).",
            "Risk-based prioritization and study scope", "set by the Pre-Characterization Process Risk Assessment"),
        stx(4, "The response-surface model is the predictive / design-space model.",
            "Common statistical approach", "response-surface model is the predictive"),
        stx(5, "The master plan governs the eight per-unit-operation Process Characterization Plans.",
            "Per-unit-operation plans", "per-unit-operation Process Characterization Plans"),
        stx(6, "The per-unit-operation reports are consolidated in the Process Characterization Master Report (PCMR-001).",
            "Schedule", "consolidated in the Process Characterization Master Report"),
    ])]
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_strategy",
                                  process_steps=_corpus_steps(doc, f, f"{doc}_sec_strategy",
                                                              "Overall characterization strategy")),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=_corpus_cqas(doc, f, f"{doc}_sec_cqa",
                                                                  "CQA framework",
                                                                  "Drug-substance CQA framework",
                                                                  f"{doc}_tab_cqa")),
    ]
    inv = S.DocumentInventoryItem(
        document_id=doc, file_name=f, predicted_document_type="process_characterization_master_plan",
        product_name_candidates=["A-Mab"], process_name_candidates=["A-Mab drug substance"],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "master plan", "CQA framework",
                     "scale-down model", "statistical approach", "design of experiments"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc][0]}'.",
        source_references=[ref(doc, f, "Title block", "Title block", P.DOC_REGISTRY[doc][0])],
        metadata=meta())
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Master plan spans the whole train; entities are the Step 3-10 process steps and the CQA framework.",
            "The per-unit-operation plan register and the common statistical approach are reported via report_sections.",
        ],
        inventory=inv, entities=entities, report_sections=report_sections,
        assertions=AssertionStore(run_id=f"gt-{doc}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id="gt-pcmp", concepts=_corpus_step_concepts()))


# =========================================================================== #
# PCMR-001 — Process Characterization Master Report (roll-up of PCR-003…010).   #
# --------------------------------------------------------------------------- #
# Consolidates the per-unit-operation reports. The ground truth captures the     #
# process train (Steps 3-10) and the CQA outcomes; the parameter-classification  #
# counts and headline outcomes are report_sections statements (individual        #
# parameter names do not appear in the rendered text — only the class counts).   #
# =========================================================================== #
PCMR_FILE = "PCMR-001_master_report.docx"


def build_master_report():
    from app.models.assertions import AssertionStore, EvidenceBackedAssertion
    from app.models.concepts import ConceptStore
    from app.models.summaries import ReportSection, ReportStatement
    doc, f = "PCMR-001", PCMR_FILE
    A, n = [], [0]

    def add(subj, pred, obj, text, sec, quote):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text, source_references=[ref(doc, f, f"{doc}_sec", sec, quote)],
            metadata=meta()))
    for key in P.CFG.train_order:
        uo = P.CFG.unit_op(key)
        title = P.UNIT_OP_TITLES.get(key, uo.name)
        add("process:amab_ds", "process_has_step", f"step:{key}",
            f"The A-Mab drug-substance process has the step {title}.",
            "Process description and performance", title)
    # a few consolidated CQA relations (grounded in the CQA-outcomes narrative)
    add("step:bioreactor", "step_has_quality_attribute", "attr:afucosylation",
        "The production bioreactor forms and controls the glycan CQAs within its design space.",
        "Consolidated CQA outcomes", "formed and controlled in the production bioreactor")
    add("step:cex", "step_has_quality_attribute", "attr:aggregates_hmw",
        "Cation exchange polishes the aggregate CQA.",
        "Consolidated CQA outcomes", "polished at cation exchange")
    add("step:virus_filtration", "step_has_quality_attribute", "attr:lrv_mvm",
        "Viral clearance is delivered orthogonally across the low-pH inactivation, anion-exchange and virus-filtration steps.",
        "Consolidated CQA outcomes",
        "delivered orthogonally across the low-pH inactivation, anion-exchange and virus-filtration steps")
    for key in ["lrv_mvm", "hcp"]:
        r = P.cqa_reg[P.cqa_reg.key == key].iloc[0].to_dict()
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{key}_acc",
            f"{r['cqa']} acceptance: {r['acc_low']:g}–{r['acc_high']:g} {r['unit']}.",
            "Consolidated CQA outcomes", r["cqa"])

    def stx(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc, f, f"{doc}_sec", sec, quote)])
    report_sections = [ReportSection(section_id=f"{doc}-summary", title="Master report summary", statements=[
        stx(1, "PCMR-001 consolidates the Stage 1 characterization of the A-Mab drug-substance process, rolling up the per-unit-operation reports.",
            "Executive summary", "consolidates the Stage 1"),
        stx(2, "All 37 process parameters were classified: 1 CPP, 20 WC-CPP, 10 KPP and 6 GPP.",
            "Executive summary", "1 CPP, 20 WC-CPP"),
        stx(3, "All 10 drug-substance CQAs meet their acceptance criteria at commercial scale with Cpk >= 1.51.",
            "Executive summary", "meet their acceptance criteria at commercial scale"),
        stx(4, "The modular viral clearance meets its requirements with margin (18.87 / 10.03 log10 for XMuLV / MVM).",
            "Executive summary", "modular viral clearance meets its requirements with margin"),
        stx(5, "The integrated process delivers an overall drug-substance yield of 83.2% (~54.6 kg).",
            "Executive summary", "overall DS yield"),
        stx(6, "The process is ready for Stage 2 (Process Performance Qualification).",
            "Conclusions and Stage-2 readiness", "ready for Stage 2"),
    ])]
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_process",
                                  process_steps=_corpus_steps(doc, f, f"{doc}_sec_process",
                                                              "Process description and performance")),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=_corpus_cqas(doc, f, f"{doc}_sec_cqa",
                                                                  "Consolidated CQA outcomes",
                                                                  "Consolidated drug-substance CQA outcomes",
                                                                  f"{doc}_tab_cqa")),
    ]
    inv = S.DocumentInventoryItem(
        document_id=doc, file_name=f, predicted_document_type="process_characterization_master_report",
        product_name_candidates=["A-Mab"], process_name_candidates=["A-Mab drug substance"],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "master report", "process capability",
                     "viral clearance", "parameter classification", "control strategy"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY[doc][0]}'.",
        source_references=[ref(doc, f, "Title block", "Title block", P.DOC_REGISTRY[doc][0])],
        metadata=meta())
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Master report rolls up the per-unit-operation reports; entities are the Step 3-10 process steps and the consolidated CQA outcomes.",
            "Parameter classification is reported as counts (1 CPP / 20 WC-CPP / 10 KPP / 6 GPP); individual parameter names are in the per-UO reports, not restated here.",
            "Process-capability (min Cpk 1.51) and cumulative viral clearance (18.87 / 10.03) are report_sections statements (no dedicated field).",
        ],
        inventory=inv, entities=entities, report_sections=report_sections,
        assertions=AssertionStore(run_id=f"gt-{doc}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id="gt-pcmr", concepts=_corpus_step_concepts()))


def main():
    os.makedirs(OUT, exist_ok=True)
    # Only the RETAINED bioreactor (Step 3) and anion-exchange (Step 8) pairs are built.
    # The other first-pass documents were archived to first_pass/ (their annexes are frozen
    # under first_pass/ground_truth/); their builder functions remain defined below but are
    # intentionally not invoked. To rebuild an archived annex, add its builder back here and
    # point check_grounding at first_pass/ (see first_pass/README.md).
    for annex in (build_plan(), build_report(),          # PCP-003 / PCR-003 (bioreactor)
                  build_plan_aex(), build_report_aex()):  # PCP-008 / PCR-008 (anion exchange)
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
