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
    """
    return dict(zip(list(keys), _md_rows(df, floatfmt)))


def title_block_quote(doc_id):
    """The title-block row that declares this document's identity.

    ``"Process Characterization Plan"`` alone appears in the title, the title-block table and
    the abbreviation list, so it cannot say *which* document is meant. The document ID and the
    declared class together are unique in every document of the corpus.
    """
    return f"Document ID {doc_id} Document class {P.DOC_REGISTRY[doc_id][0]}"


# --------------------------------------------------------------------------- #
# Entity builders (shared shape; source references differ per document).       #
# --------------------------------------------------------------------------- #
def build_step(doc_id, file_name, sec, report):
    if report:
        # Two references. The first is the rendered process-train row, which carries the step
        # number, the unit operation and its role in one span. The second is the §1.1 sentence
        # that states the absolute the description repeats — see the D-002 note below.
        train = P.process_steps_df()
        src = [ref(doc_id, file_name, sec, "Product and unit operation",
                   row_quotes(train, train["Unit operation"])[UO_NAME]),
               ref(doc_id, file_name, sec, "Product and unit operation",
                   "The production bioreactor is the only step of the drug substance process "
                   "at which product quality attributes are formed.")]
    else:
        src = [ref(doc_id, file_name, sec, "Purpose and scope",
                   "The bioreactor is Step 3 of the drug substance process and is operated as "
                   "a fed-batch cell culture at 15,000 L"),
               ref(doc_id, file_name, sec, "Purpose and scope",
                   "It is the step at which the glycosylation, charge variant and aggregate "
                   "attributes of A-Mab are formed")]
    return S.ProcessStep(
        step_id="step:production_bioreactor", step_name=UO_NAME, step_number=str(STEP),
        unit_operation=UO_NAME,
        # ------------------------------------------------------------------------------ #
        # REGISTERED DISCREPANCY D-002 — DO NOT "CORRECT" THIS DESCRIPTION.               #
        # ------------------------------------------------------------------------------ #
        # The absolute below is FALSE against outputs/data/cqa_register.csv, whose set_by
        # column assigns leached Protein A to protein_a, XMuLV clearance to
        # viral_inactivation and MVM clearance to aex. PCR-003 §1.1 asserts it anyway, as a
        # registered benchmark item, and this field repeats it verbatim in BOTH PCP-003.json
        # and PCR-003.json so that the ground truth itself asserts something false. That is
        # the point: it is the one place in the corpus where a system is tested on finding an
        # error in its own supervision rather than in the prose, and no gate can see it
        # because check_grounding only inspects SourceReference.quote.
        # Narrowing it (as this branch once did) silently deletes the benchmark item.
        # See authoring/DISCREPANCIES.md D-002 and authoring/discrepancies.yaml (annex_note).
        description="Fed-batch mammalian cell culture at 15,000 L working volume; the only "
                    "step of the drug substance process at which product quality attributes "
                    "are formed. The glycosylation and charge variant distributions are "
                    "established inside the cell and in the culture fluid, and the platform "
                    "purification train does not modify them.",
        input_materials=["inoculum", "basal medium", "nutrient feed"],
        output_materials=["clarified culture (harvest feed)"],
        equipment=["15,000 L production bioreactor", "bench-scale stirred-tank scale-down model"],
        source_references=src, metadata=meta(),
    )


def build_equipment(doc_id, file_name, sec, report):
    # Neither document names a 2 L vessel any more; both describe a bench-scale
    # stirred-tank model of the commercial vessel, so the entity follows the text.
    sdm = S.Equipment(
        equipment_id="equip:sdm_bench", equipment_name="bench-scale stirred-tank scale-down model",
        equipment_type="bioreactor (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Scale-down model and its qualification",
                               "The scale-down system is a stirred-tank bioreactor of the same "
                               "geometry and with the same control capability as the commercial "
                               "vessel" if report
                               else "a bench-scale stirred tank bioreactor system that has been "
                                    "qualified as a model of the commercial vessel under SOP-1001")],
        metadata=meta())
    vessel = S.Equipment(
        equipment_id="equip:production_bioreactor",
        equipment_name="15,000 L production bioreactor", equipment_type="bioreactor",
        site_name=P.RECEIVING_SITE,
        # Both re-authored documents state the commercial working volume in their opening
        # description of the step, so each vessel record anchors on the sentence that carries
        # the volume rather than on a passage that merely contrasts the two scales.
        source_references=[ref(doc_id, file_name, sec,
                               "Product and unit operation" if report else "Purpose and scope",
                               "The step is operated as a fed-batch culture at a working volume "
                               "of 15,000 L, with pH, temperature and dissolved oxygen under "
                               "closed-loop control" if report
                               else "is operated as a fed-batch cell culture at 15,000 L")],
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
    # The rendered @tbl-params captions of the two re-authored documents.
    caption = ("Production-bioreactor parameters, ranges, study type and final classification."
               if classified else
               "Production bioreactor parameters, ranges and study type. The range studied is "
               "the characterization range and is not a proven acceptable range.")
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
                                   table_id=f"{doc_id}_tab_params")],
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
        table_title = ("Quality attributes set by the production bioreactor, with acceptance "
                       "criteria and assigned criticality.")
    else:
        table_title = ("Quality attributes formed at the production bioreactor, with acceptance "
                       "criteria and criticality.")
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
                                   table_title=table_title, table_id=f"{doc_id}_tab_cqa")],
            metadata=meta()))
    return out


# Per-method grounded fragment from the plan's "Analytical methods" section (PCP-003 §5.3).
# Each fragment names both the attribute class and the method that measures it, which is the
# relation the AnalyticalMethod and attribute_measured_by_method records assert.
METHOD_QUOTE = {
    "AMV-3010": ("Released N-glycan mapping by 2-AB HILIC-UPLC (SOP-3010, validated under "
                 "AMV-3010) reports afucosylation, galactosylation and high mannose from a "
                 "single separation"),
    "AMV-3011": ("Aggregates are measured by SEC-HPLC (SOP-3011, AMV-3011) and reported as the "
                 "high molecular weight percentage"),
    "AMV-3012": "Host cell protein by ELISA (SOP-3012, AMV-3012)",
    "AMV-3013": "Acidic charge variants are measured by icIEF (SOP-3013, AMV-3013)",
    "AMV-3014": "residual DNA by qPCR (SOP-3014, AMV-3014)",
}
# CQA key -> the same fragment, used for the attribute -> method assertions.
CQA_METHOD_QUOTE = {k: METHOD_QUOTE[m] for k, m in CQA_METHOD.items()}

# Per-parameter classification sentence from the report's "Parameter classification"
# section (§9). The re-authored report opens each classification paragraph with the parameter,
# its class abbreviation and the attributes (or the performance measures) that carry it, so one
# sentence per parameter carries both ends of the relation.
CLASS_QUOTE = {
    "Culture pH": ("Culture pH is a WC-CPP. It has a significant effect on four of the five "
                   "measured attributes and it is the governing parameter for high mannose and "
                   "for aggregate."),
    "Culture temperature": ("Culture temperature is a WC-CPP. It affects galactosylation, high "
                            "mannose and acidic variants, and it interacts with pH."),
    "Dissolved CO2 (pCO2)": ("pCO₂ is a WC-CPP. It carries the largest single effect in the "
                             "screening study, on acidic charge variants, and a substantial "
                             "effect on galactosylation."),
    "Osmolality": ("Osmolality is a WC-CPP. It has significant effects on galactosylation and on "
                   "acidic variants in the screening study"),
    "Culture duration": ("Culture duration is a WC-CPP. It carries the largest effect on "
                         "galactosylation and the largest main effect on afucosylation, and it "
                         "is one of the two parameters in the dominant interaction."),
    "Dissolved oxygen": ("Dissolved oxygen is a KPP. It drives peak viable cell density and titre "
                         "and no effect of it on a quality attribute has been demonstrated."),
    "Initial viable cell conc.": ("Initial viable cell concentration is a KPP, on the same basis. "
                                  "It sets the growth trajectory and the integral of viable "
                                  "cells, and therefore titre, without a demonstrated quality "
                                  "effect."),
    "Nutrient feed-1 volume": ("Nutrient feed-1 volume is a KPP. It is critical to titre and is "
                               "delivered gravimetrically"),
    "Basal medium concentration": ("Basal medium concentration is a GPP. It affects titre, no "
                                   "effect of it on a quality attribute was demonstrated over "
                                   "the range studied"),
}
# Which attribute each WC-CPP classification sentence actually names. §9 is attribute-specific,
# so a blanket "impacts afucosylation" object would be false for four of the five: the pH
# paragraph names high mannose and aggregate, the pCO2 paragraph acidic variants.
CLASS_IMPACTS = {
    "Culture pH": "attr:high_mannose",
    "Culture temperature": "attr:high_mannose",
    "Dissolved CO2 (pCO2)": "attr:acidic_variants",
    "Osmolality": "attr:galactosylation",
    "Culture duration": "attr:galactosylation",
}
# Every CLASS_QUOTE now comes from §9; no parameter needs a different section.
CLASS_SECTION = {}

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
                                   "The screening study was a two-level design in the 5 "
                                   "multivariate factors, executed as a half fraction of "
                                   "resolution V with 3 centre points, for 19 runs in total."
                                   if report
                                   else "The 16 factorial runs are a half fraction of the 32 run "
                                        "full factorial, chosen at resolution V so that every "
                                        "main effect and every two-factor interaction is "
                                        "estimable clear of the others")],
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
                                   "The response-surface study was a face-centred central "
                                   "composite design in the 4 factors carried forward from "
                                   "screening (culture pH, culture temperature, culture duration "
                                   "and pCO₂), with 4 centre points, for 28 runs in total."
                                   if report
                                   else "The response-surface study is a face-centred central "
                                        "composite design in the subset of factors that "
                                        "screening identifies as active")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:br_sdm_qual", study_type="scale_down_qualification", unit_operation=UO_NAME,
            scale_down_model=SDM,
            source_references=[ref(doc_id, file_name, sec,
                                   "Scale-down model and its qualification",
                                   "Replicate set-point runs on the scale-down system were "
                                   "compared against commercial-scale engineering batches on the "
                                   "process performance measures (peak viable cell density, "
                                   "harvest viability, titre) and on the full quality panel"
                                   if report
                                   else "Qualification will compare replicate bench-scale runs at "
                                        "the target condition against the at-scale data set from "
                                        "the A-Mab engineering and clinical campaigns")],
            metadata=meta()),
        # Both re-authored documents name the same FOUR univariate parameters in this section
        # (PCP-003 §6.4, PCR-003 §4.4). The record used to list initial viable cell
        # concentration alone, which under-stated the study against both documents.
        S.StudyDesign(
            study_id="study:br_univariate", study_type="univariate", unit_operation=UO_NAME,
            factors=["Dissolved oxygen", "Initial viable cell conc.",
                     "Basal medium concentration", "Nutrient feed-1 volume"],
            responses=["process performance"],
            associated_parameters=[PARAM_CONCEPT[f] for f in
                                   ["Dissolved oxygen", "Initial viable cell conc.",
                                    "Basal medium concentration", "Nutrient feed-1 volume"]],
            source_references=[ref(doc_id, file_name, sec, "Univariate assessment",
                                   "Four parameters were assessed one at a time: dissolved "
                                   "oxygen, initial viable cell concentration, basal medium "
                                   "concentration and nutrient feed-1 volume." if report
                                   else "Dissolved oxygen, initial viable cell concentration, "
                                        "basal medium concentration and nutrient feed-1 volume "
                                        "will each be assessed one at a time")],
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

    def add(subj, pred, obj, text, sec, quote):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote)], metadata=meta()))

    # step -> parameters and step -> quality attributes (both docs). Each assertion anchors on
    # the table row naming the parameter or the attribute, so the span carries both ends of the
    # relation rather than a caption shared by every row.
    param_rows = param_row_quotes(report)
    cqa_rows = cqa_row_quotes(report)
    for name, cid in PARAM_CONCEPT.items():
        add("step:production_bioreactor", "step_has_parameter", cid,
            f"{UO_NAME} has process parameter {name}.",
            "Factors, ranges and the knowledge space" if report else "Factors, ranges and study type",
            param_rows[name])
    for r in CQA_ROWS:
        add("step:production_bioreactor", "step_has_quality_attribute", CQA_CONCEPT[r["key"]],
            f"{UO_NAME} sets/controls {r['cqa']}.", "Quality attributes in scope",
            cqa_rows[r["key"]])
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
            "Quality attributes in scope", cqa_rows[r["key"]])
    # results only in the report: parameter impacts / non-impacts. Each quote names BOTH the
    # parameter and the attribute the report links it to (CLASS_IMPACTS) — the re-authored §9
    # is attribute-specific, so a blanket "impacts afucosylation" would now be wrong for
    # temperature, osmolality and pCO2.
    if report:
        for k, obj in CLASS_IMPACTS.items():
            add(PARAM_CONCEPT[k], "parameter_impacts_attribute", obj,
                f"{k} is a well-controlled critical process parameter and the report links it to "
                f"{obj.split(':')[1].replace('_', ' ')}.",
                CLASS_SECTION.get(k, "Parameter classification"), CLASS_QUOTE[k])
        # High mannose is the very-high-criticality attribute of the step, and §5.2 reports a
        # screening null for pCO2, osmolality and culture duration. Only OSMOLALITY carries a
        # standing non-impact record. §5.4 reports that pCO2 and culture duration both interact
        # significantly with culture pH on this response in the response-surface model
        # ("Neither pCO₂ nor culture duration has a significant main effect on this response.
        # Both interact significantly with culture pH"), so an unqualified non-impact assertion
        # for those two would contradict the report's own final model. Osmolality was not
        # carried into the response-surface design, so its null rests on screening alone and
        # nothing in the report qualifies it.
        add("param:osmolality", "parameter_does_not_significantly_impact_attribute",
            "attr:high_mannose",
            "Osmolality shows no significant effect on high mannose over the ranges screened, "
            "and its null result rests on the screening study alone.",
            "Screening: factor effects",
            "Osmolality was not carried into the response-surface design, so its null result on "
            "this attribute rests on the screening study alone")
        hm_interact = ("Neither pCO₂ nor culture duration has a significant main effect on this "
                       "response. Both interact significantly with culture pH")
        add("param:dissolved_co2", "parameter_impacts_attribute", "attr:high_mannose",
            "pCO2 has no significant MAIN effect on high mannose, but it interacts significantly "
            "with culture pH in the response-surface model, so its influence on the attribute is "
            "conditional on pH and small beside the pH main effect.",
            "Mechanistic interpretation", hm_interact)
        add("param:culture_duration", "parameter_impacts_attribute", "attr:high_mannose",
            "Culture duration has no significant MAIN effect on high mannose, but it interacts "
            "significantly with culture pH in the response-surface model, so its influence on "
            "the attribute is conditional on pH.",
            "Mechanistic interpretation", hm_interact)
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
               "This plan describes the process characterization studies that will be performed "
               "on the A-Mab production bioreactor before the drug substance process is qualified "
               "at the receiving site"),
            st(2, "Nine process parameters are in scope, five studied multivariately and four univariately.",
               "Purpose and scope",
               "of which 5 will be studied in a multivariate design and 4 will be assessed one at "
               "a time"),
            st(3, "The study uses a screening fractional-factorial design followed by a "
                  "face-centred central composite design on a qualified bench-scale scale-down model.",
               "Study design",
               "A screening study resolves which of the 5 multivariate parameters are active on "
               "which response, and a response-surface study over the active subset produces the "
               "predictive model"),
            st(4, "Models are acceptable when there is no significant lack of fit against the center-point pure error.",
               "Acceptance and decision criteria",
               "when the lack of fit is not significant against pure error"),
            st(5, "The design space will be declared over the part of the characterized space in "
                  "which the fitted model predicts every attribute in scope to lie inside its "
                  "acceptance criterion.",
               "Acceptance and decision criteria",
               "The design space will be declared over that part of the characterized space in "
               "which the fitted response-surface model predicts every attribute in Table 4 to "
               "lie within its acceptance criterion"),
        ])]
    # Two statements had to be CORRECTED, not merely re-anchored, against the re-authored
    # report. The excluded corner is now a PREDICTED exceedance only — §6 states the fitted
    # value of 40.27 % and nowhere claims galactosylation was measured above the limit — and
    # §5.3 reports every response-surface model as retaining predictive value, not four of the
    # five. The old statements asserted the opposite of the document on both points.
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Nine parameters were characterized: five well-controlled critical process "
              "parameters, three key process parameters and one general process parameter.",
           "Parameter classification",
           "The step has 5 well-controlled critical process parameters, 3 key process parameters "
           "and 1 general process parameter."),
        st(2, "The step sets seven quality attributes; high mannose is the only one at very high "
              "criticality and it carries the highest Tool #1 score.",
           "Quality attributes in scope",
           "High mannose carries the highest score in the table, because its impact on clearance "
           "and its residual uncertainty are both high, and it is the only attribute of the seven "
           "at very high criticality"),
        st(3, "The design space is the characterized region less one corner: at low pH, low "
              "dissolved CO2, short duration and high temperature the model predicts "
              "galactosylation above its upper limit.",
           "Design space",
           "the fitted model predicts galactosylation of 40.27 % against an upper limit of 40 %"),
        st(4, "The exclusion covers three of the 194,481 grid points examined, every one of them "
              "failing on galactosylation, and no other response fails anywhere in the region.",
           "Design space",
           "Every one of those points fails on galactosylation, and no other response fails "
           "anywhere in the region"),
        st(5, "The response-surface models are adequate for all five responses and each retains "
              "predictive value on runs it has not seen.",
           "Response-surface models",
           "The models are adequate for all five responses and each of them retains predictive "
           "value on runs it has not seen"),
        st(6, "There was no significant lack of fit relative to the centre-point pure error.",
           "Response-surface models", "Lack of fit is not significant for any response."),
        st(7, "Every attribute the step sets meets its acceptance criterion at commercial scale, "
              "the tightest capability being High Mannose at a one-sided Cpk of 1.94.",
           "Process capability and robustness",
           "Every attribute meets its acceptance criterion, and the tightest capability is "
           "comfortable. High Mannose is the binding attribute with a one-sided Cpk of 1.94."),
        st(8, "Every proven acceptable range spans the whole characterization range, so the "
              "binding constraint on operation is the multivariate corner and not any "
              "univariate range.",
           "Proven acceptable ranges",
           "The binding constraint on the operating region at this step is the multivariate "
           "corner, not any univariate proven acceptable range."),
    ])]


def build_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:bioreactor", unit_operation=UO_NAME,
        parameters=["param:culture_ph", "param:culture_temperature",
                    "param:culture_duration", "param:dissolved_co2"],
        # The FIVE measured responses only. Host cell protein and residual DNA are set by this
        # step but are not design responses (§2.2), carry no response-surface model, and appear
        # in neither the grid evaluation nor Table 16 — so the region constrains neither, and a
        # record listing all seven would claim more than §6 evaluates.
        quality_attributes_constrained=[CQA_CONCEPT[r["key"]] for r in CQA_ROWS
                                        if r["key"] not in ("hcp", "residual_dna")],
        definition="The region of culture pH, culture temperature, culture duration and dissolved "
                   "CO2, with osmolality at its normal operating range, bounded by the "
                   "characterization ranges, over which the fitted response-surface models "
                   "predict that all five measured attributes meet their acceptance criteria — "
                   "LESS the excluded vertex at culture pH 6.6, 36 °C, 15 days and 40 mmHg, where "
                   "the model predicts galactosylation at 40.27 % against an upper limit of "
                   "40 %. The exceedance is a model PREDICTION; the report makes no claim that "
                   "galactosylation was measured above the limit at that vertex. Defined on mean "
                   "predictions from the qualified scale-down model; its edges are not confirmed "
                   "at commercial scale.",
        # Two references: the definition of the region, and the sentence that excludes the corner.
        # A record claiming the region satisfies every CQA everywhere would now be false.
        source_references=[
            ref(doc_id, file_name, "Design space", "Design space",
                "The design space for the production bioreactor is a multivariate region in "
                "culture pH, culture temperature, culture duration and pCO₂, with osmolality at "
                "its normal operating range, over which every attribute the step sets remains "
                "within its acceptance criterion."),
            ref(doc_id, file_name, f"{doc_id}_sec_exec", "Executive summary",
                "One corner of the characterized region is excluded from the design space.")],
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
PAR_TABLE = ("Proven acceptable ranges by attribute and parameter. The set-point analysis holds "
             "the other factors at their set-points; the NOR analysis varies them within their "
             "normal operating ranges by Monte-Carlo of the fitted model.")


def build_proven_acceptable_ranges(doc_id, file_name):
    """One ProvenAcceptableRange per governed CQA x response-surface parameter, from the
    same DoE engine (``doe_report.par_table``) that renders @tbl-par in the report.

    Each record is anchored on its OWN rendered @tbl-par row, which carries the attribute, the
    parameter, the characterization range and both proven acceptable ranges in one span — the
    whole of the relation the record asserts. The former per-attribute figure captions grounded
    four records apiece on a caption that named no parameter.
    """
    import doe_report as D
    par = D.par_table(UO)
    rows = _md_rows(par, P._auto_floatfmt(par))
    out = []
    for i, (r, row) in enumerate(zip(par.to_dict("records"), rows), 1):
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
                "two-sided window; the production bioreactor forms no viral-clearance CQA. "
                "Both analyses move one parameter at a time, so neither can see the excluded "
                "multivariate vertex of the design space (§6) — the binding constraint on "
                "operation is that corner and not any range in this table."),
            source_references=[ref(doc_id, file_name, f"{doc_id}_sec_par", PAR_SEC, row,
                                   table_title=PAR_TABLE, table_id=f"{doc_id}_tab_par")],
            metadata=meta()))
    return out


def _document_text(file_name):
    """Whitespace-collapsed text of the RENDERED document, for presence checks.

    Must be the ``.docx``, not the ``.qmd``: ``check_grounding.py`` is the authority and it
    reads the rendered file. A quote carrying a number exists only in the rendered text (the
    source has a ``{python}`` inline expression there), so matching against the ``.qmd``
    would silently drop exactly the quotes that ground perfectly well. Falls back to the
    source only when nothing has been rendered yet, and says so.
    """
    docx = os.path.join(HERE, file_name)
    if os.path.exists(docx):
        from check_grounding import docx_text
        return re.sub(r"\s+", " ", docx_text(docx))
    qmd = os.path.join(HERE, os.path.splitext(file_name)[0] + ".qmd")
    if os.path.exists(qmd):
        print(f"note  {file_name} not rendered yet; presence checks fall back to the .qmd, "
              f"which will under-count any quote containing a rendered number.")
        return re.sub(r"\s+", " ", open(qmd, encoding="utf-8").read())
    return ""


def build_weak_claims(doc_id, file_name):
    """Labeled unsupported/overstated claims from ``authoring/weak_claims.yaml``.

    The registry is two-phase, and the order is the whole design. A claim is ``assigned``
    before the document is written, so it reaches the author through the brief and is
    written INTO the argument; its wording is ``captured`` afterwards by reading the
    rendered document. Injecting a claim into finished prose was tried first and failed —
    against a document that has already settled the question, the claim reads as a
    contradiction of its neighbour rather than as a claim that merely lacks support, which
    silently changes the benchmark task and passes every gate. See
    ``authoring/WEAK_CLAIMS.md``.

    Three states, none of them silent: assigned-but-uncaptured prints a note (expected
    until the document is authored); a captured quote that no longer appears in the
    document is a hard failure (re-read the document and re-record the wording — never
    edit the document to match the registry); a document with no assignment emits nothing.
    """
    import yaml
    path = os.path.join(HERE, "..", "authoring", "weak_claims.yaml")
    with open(path) as fh:
        data = yaml.safe_load(fh)
    prose = _document_text(file_name)
    sec_title = {"results": "Results", "exec_summary": "Executive summary",
                 "capability": "Process capability and robustness",
                 "prior_knowledge": "Prior knowledge and quality risk basis"}
    out, pending, missing = [], [], []
    for c in data.get("claims", {}).get(doc_id, []):
        cap = c.get("captured") or {}
        raw = cap.get("quote")
        if not raw:
            pending.append(c["id"])          # assigned, document not yet authored
            continue
        sec = c.get("section")
        quote = " ".join(raw.split())
        if prose and quote not in prose:
            missing.append(c["id"])          # captured wording no longer in the document
            continue
        out.append(S.WeakClaim(
            claim_id=c["id"], section=sec, weakness_type=c["weakness_type"],
            source_reference=ref(doc_id, file_name, f"{doc_id}_sec_{sec}",
                                 sec_title.get(sec, "Results"), quote),
            rationale=" ".join((cap.get("rationale") or "").split()),
            correct_version=" ".join((cap.get("correct_version") or "").split()),
            metadata=meta(basis="explicit", conf="high")))
    if pending:
        print(f"note  {doc_id}: {len(pending)} weak claim(s) assigned but not yet captured "
              f"({', '.join(pending)}). Expected until the document is authored and its "
              f"wording recorded in authoring/weak_claims.yaml.")
    if missing:
        # The document was re-authored and the recorded wording went with it. Do NOT edit
        # the document to match; re-read it and re-record the author's new wording.
        raise SystemExit(
            f"FAIL  {doc_id}: {len(missing)} captured weak claim(s) no longer appear in "
            f"{file_name} ({', '.join(missing)}).\n"
            f"      Re-read the rendered document and update `captured.quote` in "
            f"authoring/weak_claims.yaml to the author's current wording.")
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
    prose = _document_text(file_name)
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
        # A curated span layer that no longer matches its document degrades SILENTLY: the
        # build succeeds, check_grounding still reports 0 ungrounded (a dropped span
        # contributes no quote to check), and the annex just ships thinner than intended.
        # PCR-003 shipped an entirely empty rhetorical layer that way. So this is a build
        # FAILURE — but a deferred one. Raising here aborts before the remaining annexes
        # are written, which blocks every other document during a legitimate re-authoring
        # cycle and hides any second problem behind the first. Collect, report at the end.
        BUILD_ERRORS.append(
            f"{doc_id}: {skipped} of {len(data.get('spans', []))} rhetorical span(s) do not "
            f"appear in {file_name}. The document was re-authored or re-rendered since the "
            f"layer was curated. Re-curate authoring/rhetorical/{doc_id}.spans.yaml against "
            f"the current rendered text, or delete it to drop the layer deliberately.")
    return out


# --------------------------------------------------------------------------- #
# Assemble the two annexes.                                                     #
# --------------------------------------------------------------------------- #
# Deferred build failures. Collected so every annex is still written and every problem is
# reported, rather than the first one aborting the run. main() exits non-zero if non-empty.
BUILD_ERRORS: list[str] = []

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
        weak_claims=build_weak_claims(doc, f),
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Parameter study-type (multivariate/univariate) has no ProcessParameter field; captured via StudyDesign.factors.",
            "The Plan states classification is an OUTPUT; parameter_type left 'unclassified' here.",
            "ProcessStep.description repeats registered discrepancy D-002 verbatim, as in "
            "PCR-003.json: the absolute that the bioreactor is the only step at which product "
            "quality attributes are formed. PCP-003 itself makes only the narrower, true claim; "
            "the annex carries the false absolute deliberately, so the ground truth is itself "
            "wrong on this point. See authoring/DISCREPANCIES.md D-002.",
        ],
        inventory=inventory(doc, f, "process_characterization_plan"),
        entities=entities,
        studies=build_studies(doc, f, report=False),
        report_sections=build_report_sections(doc, f, report=False),
        assertions=build_assertions(doc, f, report=False), concepts=build_concepts())


def build_report():
    doc, f = "PCR-003", PCR_FILE
    entities = [
        # The re-authored report introduces the step and the two vessels in §1.1, not in the
        # executive summary, so the entity block is keyed on the unit-operation section.
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_uo",
                                  process_steps=[build_step(doc, f, f"{doc}_sec_uo", report=True)],
                                  equipment=build_equipment(doc, f, f"{doc}_sec_uo", report=True)),
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
            "Per-record quotes are the RENDERED TABLE ROW (@tbl-params, @tbl-cqa, @tbl-par), "
            "rebuilt from the same seeded register, so each span carries both ends of the "
            "relation it anchors rather than a caption shared by every row.",
            "The design space is the characterized region LESS one vertex (culture pH 6.6, "
            "36 C, 15 days, 40 mmHg) at which the fitted model PREDICTS galactosylation of "
            "40.27 % against a 40 % limit. The report states the exceedance as a prediction "
            "only; it makes no claim that galactosylation was measured above the limit at that "
            "vertex, and no record here does either. No record asserts that the characterized "
            "region meets every acceptance criterion everywhere.",
            "Both proven-acceptable-range analyses move ONE parameter at a time, so the PAR "
            "records cannot see that vertex; the binding constraint on operation is the "
            "multivariate corner and not any row of @tbl-par.",
            "parameter_impacts_attribute is asserted against the attribute the report actually "
            "names for that parameter (CLASS_IMPACTS). Culture temperature and osmolality are "
            "NOT claimed to move afucosylation.",
            "High mannose carries ONE non-impact record, for osmolality, whose screening null "
            "the report leaves unqualified because osmolality was not carried into the "
            "response-surface design. pCO2 and culture duration have no significant MAIN effect "
            "on high mannose but interact significantly with culture pH in the response-surface "
            "model (§5.4), so each is recorded as parameter_impacts_attribute with the "
            "conditionality stated, not as a non-impact.",
            "ProcessStep.description repeats registered discrepancy D-002 verbatim in this "
            "annex and in PCP-003.json: the absolute that the bioreactor is the only step at "
            "which product quality attributes are formed. It is FALSE against "
            "outputs/data/cqa_register.csv (set_by assigns leached Protein A to protein_a, "
            "XMuLV clearance to viral_inactivation, MVM clearance to aex) and is kept "
            "deliberately. See authoring/DISCREPANCIES.md D-002.",
            "WC-003-01 and WC-003-02 are registered benchmark negatives (support=unsupported). "
            "They carry no ordinary assertion and no rhetorical `claim` span; the sentence "
            "attributing platform experience for dissolved oxygen is deliberately NOT used as "
            "the anchor for the dissolved-oxygen non-impact assertion.",
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
# Two names exist for this step and they are not interchangeable. UNIT_OP_TITLES is what the
# documents RENDER, so it is what every entity value and every table-row lookup must use — an
# annex naming a unit operation something no document says is not grounded. CFG.unit_op().name
# is the CONFIG spelling, which survives only inside the generated CSVs, so it is what the
# param_reg filter must use. char_scope_df once rendered the config spelling, which is how one
# document came to name this step two ways in two tables; _pcpkg now titles it.
HUO_NAME = P.UNIT_OP_TITLES[HUO]                # "Harvest and Clarification" (rendered)
HUO_CSV = P.CFG.unit_op(HUO).name               # "Harvest / Clarification" (matches the CSV)
HSTEP = P.CFG.unit_op(HUO).step                 # 4
HSTEP_LABEL = f"Harvest and Clarification (Step {HSTEP})"

PCP4_FILE = "PCP-004_harvest.docx"
PCR4_FILE = "PCR-004_harvest.docx"

HPARAM_ROWS = P.param_reg[P.param_reg.unit_operation == HUO_CSV].to_dict("records")
HPARAM_CONCEPT = {
    "Centrifugation (rcf)": "param:centrifuge_rcf",
    "Depth filter load": "param:depth_filter_load",
    "Post-clarification turbidity": "param:post_clarification_turbidity",
}
H_P_TURB = P.CFG.unit_op(HUO).param("turbidity")

# Attributes each document puts in scope. The step forms and clears none of them; both
# documents render the drug-substance register for the ones the clarified harvest carries,
# and each attribute record therefore anchors on ITS OWN rendered row. The two documents
# scope the table differently, which is why the key lists differ: the re-authored plan
# tables the three attributes the purification train has to clear (PCP-004 §4.2), while the
# re-authored report tables every attribute present in the harvested stream (PCR-004 §2.2)
# so that "none of them is modified across the step" is a claim about all of them.
HATTR_KEYS = {
    "PCP-004": ["hcp", "residual_dna", "aggregates_hmw"],
    "PCR-004": ["hcp", "residual_dna", "aggregates_hmw", "afucosylation",
                "galactosylation", "high_mannose", "acidic_variants"],
}
HATTR_CONCEPT = {k: f"attr:{k}" for k in
                 ["hcp", "residual_dna", "aggregates_hmw", "afucosylation",
                  "galactosylation", "high_mannose", "acidic_variants"]}
# Turbidity is the one stream property the step itself controls. Both documents call it an
# attribute of the stream AND carry it in the parameter register, so it has both concepts.
HATTR_CONCEPT["turbidity"] = "attr:post_clarification_turbidity"
# Names come from the register the documents render, not from a local spelling.
HATTR_NAME = {r["key"]: r["cqa"] for r in P.cqa_reg.to_dict("records")}
HATTR_NAME["turbidity"] = "Post-clarification turbidity"
# Acceptance criterion exactly as the rendered register row states it.
HATTR_ACCEPT = {r["key"]: f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"
                for r in P.cqa_reg.to_dict("records")}

HMETHODS = [
    ("AMV-3015", "Turbidity by Nephelometry (NTU)", "nephelometry",
     ["post-clarification turbidity"], ["turbidity"]),
    ("AMV-3012", "Host-Cell Protein ELISA", "immunoassay", ["host-cell protein"], ["hcp"]),
    ("AMV-3014", "Residual DNA (qPCR)", "qPCR", ["residual host-cell DNA"], ["residual_dna"]),
    ("AMV-3011", "Size-Variants (SEC-HPLC)", "chromatography",
     ["aggregate", "monomer"], ["aggregates_hmw"]),
]
# PCP-004 §5.1 calls it "a scale-down model of the recovery train"; PCR-004 §3.1 describes
# the same thing as "a scale-down laboratory system ... qualified as a model of the
# commercial harvest and clarification operation".
HSDM = "scale-down model of the recovery train"

# --------------------------------------------------------------------------- #
# Per-document grounded fragments. Each is a verbatim span of the RENDERED      #
# document (see check_grounding.py), chosen number-free wherever the number is  #
# not the point, so a reseed cannot break the grounding. Anything that is a     #
# TABLE relation is anchored on its rendered row instead (row_quotes), so the   #
# fragments below are only for relations the documents state in prose.          #
# --------------------------------------------------------------------------- #
# Analytical methods: the sentence in each document's "Analytical methods" section that
# names the analyte against the method, which is the relation the attribute -> method
# assertions carry. (The AnalyticalMethod entities themselves anchor on their own row of
# the rendered controlled-document table.) One sentence covers the HCP and DNA methods in
# both documents, which is how both were written.
HMETHOD_QUOTE = {
    "PCP-004": {
        "AMV-3015": "Turbidity in the centrate and in the clarified pool is measured by "
                    "nephelometry (AMV-3015)",
        "AMV-3012": "Host cell protein is measured by ELISA (AMV-3012) and residual DNA by "
                    "qPCR (AMV-3014)",
        "AMV-3014": "Host cell protein is measured by ELISA (AMV-3012) and residual DNA by "
                    "qPCR (AMV-3014)",
        "AMV-3011": "Aggregate is measured by size-exclusion chromatography (AMV-3011) across "
                    "the step",
    },
    "PCR-004": {
        "AMV-3015": "Turbidity by nephelometry (AMV-3015) is the primary in-process method of "
                    "the step.",
        "AMV-3012": "Host cell protein by ELISA (AMV-3012) and residual DNA by qPCR (AMV-3014) "
                    "quantify the impurity burden delivered to capture.",
        "AMV-3014": "Host cell protein by ELISA (AMV-3012) and residual DNA by qPCR (AMV-3014) "
                    "quantify the impurity burden delivered to capture.",
        "AMV-3011": "Size variants by SEC (AMV-3011) measure the aggregate content of the "
                    "bioreactor sample and of the clarified harvest",
    },
}
# Turbidity is not in either register table, so its "carried / monitored" record is the one
# attribute record that anchors on prose. Each document states the relation once.
HTURB_QUOTE = {
    "PCP-004": ("Unit operation description and prior knowledge",
                "Turbidity is treated as a parameter in its own right, because the clarified "
                "harvest is released to capture against a turbidity limit."),
    "PCR-004": ("Factors, ranges and the knowledge space",
                "It is an attribute of the stream, but it is the attribute against which the "
                "clarified harvest is accepted for loading onto capture"),
}
# "no product-quality impact" — REPORT ONLY. PCP-004 is prospective and says so: it records
# only that RA-001 scored no quality path, and it states of the one attribute with a
# mechanism that the study "will confirm and not assume" that it passes through unchanged.
# Asserting a characterization outcome out of a plan that declines to assume it is a false
# record, so the plan carries no such assertion. The report's null result is real (§5.2,
# §5.6, §9) and each parameter has its own sentence stating it.
HNOIMPACT_QUOTE = {
    "Centrifugation (rcf)": ("Centrifugation across its characterization range",
                             "Applied centrifugal field governs the solids load passed to the "
                             "depth filter train, and it has no effect on any product quality "
                             "attribute."),
    "Depth filter load": ("Parameter classification",
                          "It acts directly on post-clarification turbidity, it produced the "
                          "only excursion of the study when its upper edge was combined with "
                          "the low centrifugation edge, and it showed no effect on any quality "
                          "attribute."),
    # Built from the same Parameter object the document renders, so a reseeded range keeps
    # the quote verbatim.
    "Post-clarification turbidity": (
        "Parameter classification",
        "no quality attribute of the drug substance depends on its value inside "
        f"{format(float(H_P_TURB.prange[0]), ',g')} to "
        f"{format(float(H_P_TURB.prange[1]), ',g')} NTU"),
}
# PCP-004 §6.2 states the design in one sentence, with the series count rendered from the
# parameter register. Built from the register here so a reseed cannot break the grounding.
H_PLAN_UNI_QUOTE = (f"The study is a set of {len(HPARAM_ROWS)} univariate series, one per "
                    "parameter, executed on the qualified scale-down model.")
# Per-parameter classification rationale, from PCR-004 §9 (report only).
HPARAM_RATIONALE = {
    "Centrifugation (rcf)": "Key process parameter: it governs the solids load the depth filter "
                            "train carries, and it showed no effect on any quality attribute "
                            "anywhere in the characterized range; it is held inside its normal "
                            "operating range because process consistency depends on it.",
    "Depth filter load": "Key process parameter: it acts directly on post-clarification "
                         "turbidity and produced the only excursion of the study when its upper "
                         "edge was combined with the low centrifugation edge, and it showed no "
                         "effect on any quality attribute.",
    "Post-clarification turbidity": "General process parameter: the acceptance condition the "
                                    "clarified harvest meets before capture, measured on every "
                                    "batch, with no quality attribute of the drug substance "
                                    "depending on its value inside the characterized range.",
}


def h_step(doc_id, file_name, sec, report):
    """The unit operation itself, anchored on the rendered row that names it.

    The plan renders the process train (``@tbl-train``) and the report renders the campaign
    scope table (``@tbl-scope``); both carry a row that names step 4, the unit operation and
    what it is for, which is a better anchor than a sentence about it. Each is paired with
    the one sentence of its document that states the negative the step record turns on.
    """
    if report:
        scope = P.char_scope_df()
        src = [ref(doc_id, file_name, sec, "Appendix B — Characterization scope of the campaign",
                   row_quotes(scope, scope["Unit operation"],
                              P._auto_floatfmt(scope))[HUO_NAME],
                   table_title=("Characterization scope by unit operation, with the number of "
                                "parameters assigned to multivariate and to univariate study."),
                   table_id=f"{doc_id}_tab_scope"),
               ref(doc_id, file_name, sec, "Product and unit operation",
                   "The step forms no quality attribute of its own, so there is nothing here "
                   "for a design space to protect.")]
    else:
        train = P.process_steps_df()
        src = [ref(doc_id, file_name, sec, "Unit operation description and prior knowledge",
                   row_quotes(train, train["Unit operation"],
                              P._auto_floatfmt(train))["Harvest and Clarification"],
                   table_title=("The A-Mab drug substance process train and the principal role "
                                "of each step."),
                   table_id=f"{doc_id}_tab_train"),
               ref(doc_id, file_name, sec, "Purpose and scope",
                   "The step forms no product quality attribute.")]
    return S.ProcessStep(
        step_id="step:harvest_clarification", step_name=HUO_NAME, step_number=str(HSTEP),
        unit_operation=HUO_NAME,
        description="Primary recovery: whole cell broth is separated by continuous disk-stack "
                    "centrifugation and the centrate is clarified through a depth filter train "
                    "and a sterile filter, delivering the feed to Protein A capture. Both stages "
                    "are physical separations: the step forms no product-quality attribute and "
                    "removes no soluble impurity, so the host cell protein, DNA and aggregate "
                    "burden generated during culture passes forward and is cleared downstream "
                    "(PCR-005, PCR-007, PCR-008). No viral clearance is claimed for it.",
        input_materials=["production-bioreactor harvest (whole broth)"],
        output_materials=["clarified harvest (Protein A capture feed)"],
        equipment=["continuous disk-stack centrifuge", "depth filter train", "sterile filter",
                   HSDM],
        source_references=src, metadata=meta())


def h_equipment(doc_id, file_name, sec, report):
    if report:
        cent = ("Product and unit operation",
                "Whole cell broth is fed continuously to a disk-stack centrifuge, which sediments "
                "cells and the larger cell debris under an applied relative centrifugal field "
                "(rcf)")
        dep = ("Product and unit operation",
               "the centrate is then passed through a depth filter train, which retains the "
               "finer colloidal material that the centrifuge does not remove")
        sdm_ref = ("Scale-down model and its qualification",
                   "A scale-down laboratory system was qualified as a model of the commercial "
                   "harvest and clarification operation, under SOP-1001.")
    else:
        cent = ("Unit operation description and prior knowledge",
                "Continuous disk-stack centrifugation removes the cells and the larger debris "
                "from the culture broth")
        dep = ("Unit operation description and prior knowledge",
               "depth filtration then removes the fines that the centrifuge leaves behind")
        sdm_ref = ("Scale-down model and its qualification",
                   "The studies will be run on a scale-down model of the recovery train, "
                   "qualified against commercial scale data under SOP-1001.")
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


def h_param_rows(classified):
    """Rendered ``@tbl-params`` rows of the harvest pair, keyed by parameter name.

    ``show`` picks a per-column float format, and the set-point column of this step is a
    column of plain magnitudes, so 9000 renders as ``9,000`` and not as ``9e+03``. Rebuild
    the row with the same choice or the anchor is not the row the reader sees.
    """
    df = P.report_params(HUO) if classified else P.plan_params(HUO)
    return row_quotes(df, df["Parameter"], P._auto_floatfmt(df))


def h_params(doc_id, file_name, sec, classified):
    # Verbatim caption of @tbl-params in each rendered document. The caption is metadata
    # here; each parameter anchors on its OWN row, which carries the set-point, both ranges
    # and (in the report) the final classification.
    caption = ("Harvest and clarification parameters, with set-point, normal operating range, "
               "characterization range, final classification and study type."
               if classified else
               "Parameters to be studied, with set-points, normal operating ranges, "
               "characterization ranges and study type.")
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
                                   "Factors, ranges and the knowledge space" if classified
                                   else "Factors, ranges and study type",
                                   rows[name], table_title=caption,
                                   table_id=f"{doc_id}_tab_params")],
            metadata=meta()))
    return out


def h_sop_rows():
    """Rendered rows of the controlled-document table both harvest documents print.

    ``sop_table`` builds the frame from ``HARVEST_SOP_REFS`` + ``HARVEST_AMV_REFS`` and
    prints it with ``to_markdown``, so the same frame reproduces the rendered row: the
    method identifier, its validated title and its type in one span.
    """
    rows = [[sid, title, "SOP"] for sid, title in P.HARVEST_SOP_REFS]
    rows += [[aid, title, "Method validation"] for aid, title in P.HARVEST_AMV_REFS]
    df = P.pd.DataFrame(rows, columns=["Reference", "Title", "Type"])
    return row_quotes(df, df["Reference"])


def h_methods(doc_id, file_name, sec, report):
    caption = ("Controlled procedures and validated analytical methods applied to this step."
               if report else
               "Controlled procedures and validated analytical methods for Step 4.")
    rows = h_sop_rows()
    out = []
    for mid, mname, mtype, analytes, attrs in HMETHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[HATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods", rows[mid],
                                   table_title=caption, table_id=f"{doc_id}_tab_sops")],
            metadata=meta()))
    return out


def h_univariate_runs():
    """Number of distinct conditions in the planned univariate schedule (PCP-004 Appendix A).

    The schedule takes each parameter to five levels — both characterization edges, both
    normal-operating edges and its set-point — and runs a coincident level once. Turbidity's
    normal operating range and characterization range share their lower edge, so its series
    carries one run fewer. Derived from the same Parameter objects the plan renders, never
    counted off the rendered table.
    """
    n = 0
    for key in ("centrifuge_g", "depth_filter_load", "turbidity"):
        p = P.CFG.unit_op(HUO).param(key)
        n += len({p.prange[0], p.nor[0], p.setpoint, p.nor[1], p.prange[1]})
    return n


def h_studies(doc_id, file_name, report):
    """The two study objects of Step 4: a univariate series per parameter, and the SDM
    qualification. No designed experiment exists at this step in either document.

    All THREE parameters are factors. An earlier version of this record listed only the two
    settable ones and called turbidity an outcome; the re-authored documents run turbidity as
    a series of its own (PCP-004 §6.2 and its Appendix A schedule, PCR-004 §4.2), so the
    two-factor record understated the study against both.
    """
    factors = [r["parameter"] for r in HPARAM_ROWS]
    if report:
        uni = ("Univariate assessment",
               "Each parameter was varied across its characterization range with the other two "
               "held at their set-points, which is the design RA-001 assigned and PCP-004 "
               "approved.")
        qual = ("Scale-down model and its qualification",
                "The qualification compared centrate turbidity, post-filter turbidity and "
                "product recovery against the commercial-scale record across replicate runs")
        responses = ["product recovery (step yield)", "post-clarification turbidity",
                     "host cell protein and residual DNA delivered to capture",
                     "size variants across the step"]
        n_runs = None
    else:
        uni = ("Univariate assessment", H_PLAN_UNI_QUOTE)
        qual = ("Scale-down model and its qualification",
                "Qualification will compare the model against commercial scale data at the "
                "set-point condition for product recovery, centrate turbidity, "
                "post-clarification turbidity, host cell protein and residual DNA.")
        responses = ["product recovery (step yield)", "post-clarification turbidity",
                     "depth filter differential pressure and throughput",
                     "host cell protein and residual DNA delivered to capture",
                     "aggregate across the step"]
        n_runs = h_univariate_runs()
    return [
        S.StudyDesign(
            study_id="study:hv_univariate", study_type="univariate",
            design_name="univariate series, one per parameter, others held at set-point",
            unit_operation=HUO_NAME, factors=factors, responses=responses, n_runs=n_runs,
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
                  aliases=["harvest", "clarification", "primary recovery", "Step 4",
                           "Harvest and Clarification"],
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


def h_cqa_rows(doc_id):
    """Rendered ``@tbl-cqa`` rows of one harvest document, keyed by attribute key.

    Each row carries the attribute, its category, its drug-substance acceptance criterion and
    its assigned criticality — both ends of the two relations the annex asserts about it.
    """
    keys = HATTR_KEYS[doc_id]
    df = P.cqas_by_keys(keys)
    return row_quotes(df, keys, P._auto_floatfmt(df))


def h_assertions(doc_id, file_name, report):
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec, quote, table_title=None, table_id=None):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote,
                                   table_title=table_title, table_id=table_id)],
            metadata=meta()))

    # step -> parameter: the rendered parameter row, which names the parameter, its set-point
    # and the range it was (or will be) studied over.
    param_rows = h_param_rows(report)
    param_sec = ("Factors, ranges and the knowledge space" if report
                 else "Factors, ranges and study type")
    for name, cid in HPARAM_CONCEPT.items():
        add("step:harvest_clarification", "step_has_parameter", cid,
            f"{HUO_NAME} has process parameter {name}.", param_sec, param_rows[name],
            table_id=f"{doc_id}_tab_params")
    # step -> quality attribute, and attribute -> acceptance criterion. The step FORMS and
    # CLEARS none of them: it carries the burden generated during culture forward to capture.
    # Both records anchor on the attribute's own row of the register table each document
    # renders, which carries the attribute and its acceptance criterion in one span.
    cqa_rows = h_cqa_rows(doc_id)
    cqa_sec = "Quality attributes in scope"
    for key in HATTR_KEYS[doc_id]:
        add("step:harvest_clarification", "step_has_quality_attribute", HATTR_CONCEPT[key],
            f"{HUO_NAME} carries {HATTR_NAME[key]} forward to the purification train; it "
            f"neither forms nor removes it.", cqa_sec, cqa_rows[key],
            table_id=f"{doc_id}_tab_cqa")
        add(HATTR_CONCEPT[key], "attribute_has_acceptance_criterion", HATTR_ACCEPT[key],
            f"{HATTR_NAME[key]} has drug-substance acceptance criterion "
            f"{HATTR_ACCEPT[key]}; the criterion is not applied at the outlet of this step.",
            cqa_sec, cqa_rows[key], table_id=f"{doc_id}_tab_cqa")
    # Turbidity is the one stream property this step controls, and it is in neither register
    # table, so it anchors on the sentence that states the relation.
    t_sec, t_quote = HTURB_QUOTE[doc_id]
    add("step:harvest_clarification", "step_has_quality_attribute",
        HATTR_CONCEPT["turbidity"],
        f"{HUO_NAME} monitors {HATTR_NAME['turbidity']} as the measure against which the "
        f"clarified harvest is accepted for Protein A capture.", t_sec, t_quote)
    # attribute -> method
    for mid, mname, mtype, analytes, attrs in HMETHODS:
        for a in attrs:
            add(HATTR_CONCEPT[a], "attribute_measured_by_method", f"method:{mid}",
                f"{HATTR_NAME[a]} is measured by {mid}.", "Analytical methods",
                HMETHOD_QUOTE[doc_id][mid])
    # No-CQA-impact: REPORT ONLY. PCP-004 is prospective and explicitly declines to assume the
    # outcome ("which the study will confirm and not assume"), so a plan-sourced no-impact
    # assertion would be ground truth for a result that does not exist when the plan is
    # written. The report states the null result per parameter, and each has its own sentence.
    if report:
        for name, cid in HPARAM_CONCEPT.items():
            ni_sec, ni_quote = HNOIMPACT_QUOTE[name]
            add(cid, "parameter_does_not_significantly_impact_attribute", "attr:aggregates_hmw",
                f"{name} showed no effect on any product-quality attribute over the "
                f"characterized range.", ni_sec, ni_quote)
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def h_report_sections(doc_id, file_name, report):
    from annex_contract.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-004 defines the Stage 1 characterization studies that will support the "
                  "commercial operating ranges of harvest and clarification (Step 4).",
               "Purpose and scope",
               "This plan defines the characterization studies that will support the commercial "
               "operating ranges for the step."),
            st(2, "The plan is prospective: it carries no results, and the outcome is reported "
                  "in PCR-004.",
               "Purpose and scope",
               "The plan is prospective, so no results appear in it, and the outcome is "
               "reported in PCR-004."),
            st(3, "The step forms no quality attribute of its own; the attributes in scope are "
                  "the ones the clarified harvest carries into the purification train.",
               "Quality attributes in scope",
               "Three attributes are nevertheless in scope, because the clarified harvest "
               "carries them into the purification train"),
            st(4, "Each parameter is studied as its own univariate series on the qualified "
                  "scale-down model, with the other parameters held at their set-points.",
               "Univariate assessment", H_PLAN_UNI_QUOTE),
            st(5, "No screening design and no response-surface design are planned for the step.",
               "Univariate assessment",
               "No screening design and no response-surface design are planned for this step."),
            st(6, "A confirmation set run at the least favourable normal-operating corner tests "
                  "the assumption that the parameters act independently.",
               "Univariate assessment",
               "These runs are the direct test of the assumption that the parameters act "
               "independently"),
            st(7, "No multivariate design space is claimed for the step, because none is "
                  "studied.",
               "Proven acceptable ranges (planned analysis)",
               "This step has no multivariate design space, because none was studied and none "
               "is claimed."),
            st(8, "No process capability index is calculated for the step, because it has no "
                  "quality attribute of its own.",
               "Statistical methods",
               "No process capability index will be calculated for this step."),
            st(9, "Parameter classification is an outcome of the study and is stated in "
                  "PCR-004, not in this plan.",
               "Acceptance and decision criteria",
               "The class of each harvest parameter is an outcome of the study and is stated in "
               "PCR-004, not here."),
            st(10, "No viral clearance is claimed for harvest or for clarification.",
                "Purpose and scope",
                "No viral clearance is claimed for harvest or for clarification"),
        ])]
    perf = P.step_performance(HSTEP)
    perf_rows = row_quotes(perf, perf["Metric"], ",g")
    cls = P.param_reg[P.param_reg.unit_operation == HUO_CSV]["classification"].value_counts()
    n_kpp, n_gpp = int(cls.get("KPP", 0)), int(cls.get("GPP", 0))
    capr = P.cap[P.cap.key == "hcp"].iloc[0]
    cap_rows = row_quotes(P.cap_for(["hcp", "residual_dna", "aggregates_hmw"]),
                          ["Aggregates (HMW)", "Host Cell Protein (HCP)", "Residual DNA"])
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Harvest and clarification forms no critical quality attribute, and none of the "
              "attributes present in the harvested stream is modified across it.",
           "Executive summary", "The step forms no critical quality attribute."),
        st(2, f"The nominal batch recovered "
              f"{P.pct(float(perf[perf.Metric.str.startswith('Step yield')].iloc[0]['Nominal batch']))}"
              f" of the product mass entering the step.",
           "Nominal performance and mass balance",
           perf_rows["Step yield (fraction of input product mass)"]),
        st(3, "One post-clarification turbidity value fell outside the normal operating range, "
              "on the bounding run that combined the high depth-filter loading edge with the "
              "low centrifugation edge; it stayed inside the characterization range and the run "
              "was retained (DEV-004-02).",
           "Depth filter loading and clarification capacity",
           "The bounding condition that combines the high loading edge with the low "
           "centrifugation edge produced the only post-clarification turbidity in the study "
           "that fell outside a normal operating range."),
        st(4, "No product quality attribute of A-Mab is altered across the step; every paired "
              "comparison lay within the precision of its method.",
           "Product quality across the step",
           "No product quality attribute of A-Mab is altered by harvest and clarification."),
        st(5, f"The step carries {n_kpp} key process parameters and {n_gpp} general process "
              f"parameter, and no critical or well controlled critical process parameter.",
           "Parameter classification",
           "No parameter of this step is a critical process parameter or a well controlled "
           "critical process parameter."),
        st(6, "No design space is defined for the step, because it neither forms nor clears a "
              "quality attribute and no response-surface model was fitted.",
           "Design space", "No design space is defined for harvest and clarification."),
        st(7, "The proven acceptable range of every parameter is its full characterization "
              "range, with the normal operating range inside it.",
           "The ranges",
           "the proven acceptable range is the full characterization range, and the normal "
           "operating range sits inside it with margin on both sides"),
        st(8, "The step takes no clearance credit: reduction of host cell protein and residual "
              "DNA toward the drug-substance limits is delivered by PCR-005, PCR-007 and "
              "PCR-008.",
           "Contribution to the control strategy",
           "The step does not reduce host cell protein or residual DNA toward the drug "
           "substance limits, and that reduction is delivered by Protein A capture, cation "
           "exchange and anion exchange."),
        st(9, f"No capability is attributed to the step itself; host cell protein is the "
              f"tightest of the three attributes it carries forward, at a commercial-scale "
              f"capability index of {float(capr.Cpk):.2f} against an upper limit of "
              f"{float(capr.acc_high):g} ng/mg, and that margin is earned downstream.",
           "What is and is not attributed to this step",
           cap_rows["Host Cell Protein (HCP)"]),
        st(10, "Both recorded deviations were investigated and retained; no run was excluded "
               "and no range or classification depends on a deviated condition.",
            "Deviations from the plan",
            "No run was excluded, no result was recalculated, and no range or classification in "
            "this report depends on a deviated condition."),
        st(11, "The report rolls up into the Process Characterization Master Report (PCMR-001).",
            "Executive summary", "This report rolls up into the master report PCMR-001."),
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
# The "Acceptance basis" cell PCR-004 §7.2 prints against each parameter. It is prose the
# report states, not a value from the model, and it is reproduced here for two reasons: it is
# the acceptance basis the annex records, and it is part of the rendered row each PAR record
# anchors on. Keyed by parameter so a reordered register cannot silently mis-pair them.
HPAR_BASIS_CELL = {
    "Centrifugation (rcf)": "Clarified harvest delivered inside the turbidity range studied; "
                            "step yield maintained",
    "Depth filter load": "Depth filter capacity sufficient for the batch volume; clarified "
                         "harvest delivered inside the turbidity range studied",
    "Post-clarification turbidity": "Feed acceptable to Protein A capture; in-process limit, no "
                                    "drug substance criterion",
}
HPAR_CAPTION = ("Proven acceptable ranges of the harvest and clarification parameters, with the "
                "performance basis on which each is proven.")


def h_par_table():
    """The rendered ``@tbl-par`` frame of PCR-004, rebuilt from the same register.

    The report builds it as the parameter table's NOR and characterization columns, plus a
    proven-acceptable-range column equal to the characterization range (§7.2: for every
    parameter the proven acceptable range is the full characterization range) and the
    per-parameter acceptance basis. Rebuilding it here is what lets each PAR record anchor on
    its own rendered row rather than on the shared caption.
    """
    df = P.report_params(HUO)[["Parameter", "Unit", "NOR", "Char. range"]].copy()
    df["Proven acceptable range"] = df["Char. range"]
    df["Acceptance basis"] = [HPAR_BASIS_CELL[p] for p in df["Parameter"]]
    return df


def h_proven_acceptable_ranges(doc_id, file_name):
    par_tbl = h_par_table()
    rows = row_quotes(par_tbl, par_tbl["Parameter"], P._auto_floatfmt(par_tbl))
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
            acceptance_basis=(f"{HPAR_BASIS_CELL[name]}. Process-performance criteria of the "
                              "step, not a drug-substance specification; no response-surface "
                              "model was fitted, so no NOR-propagated PAR is reported and the "
                              "two bounding conditions stand in for the co-variation a "
                              "Monte-Carlo analysis would cover."),
            source_references=[ref(doc_id, file_name, f"{doc_id}_sec_par", "The ranges",
                                   rows[name], table_title=HPAR_CAPTION,
                                   table_id=f"{doc_id}_tab_par")],
            metadata=meta()))
    return out


# --------------------------------------------------------------------------- #
# Report-only discourse layer (PCR-004 only).                                   #
# --------------------------------------------------------------------------- #
# Argument-structure spans over the PCR-004 report. Each quote is a verbatim,    #
# plain-prose fragment of the RENDERED report (checked against the .docx, not    #
# the .qmd: inline expressions render to numbers), chosen number-free wherever   #
# possible so a reseed cannot break grounding. Harvest is the corpus's clearest  #
# negative argument — no design was run, no design space is claimed, no CQA is   #
# set — so the layer is dominated by claims about what the step does NOT do,     #
# the mechanistic warrants that license them, and the credit handed to           #
# PCR-005 / PCR-007 / PCR-008. PCR-004 carries NO weak_claims. Tuple fields:     #
# (suffix, role, section, quote, supported_by-suffixes, restates, bounds).       #
#                                                                               #
# Two traps in this document, both found the hard way:                           #
#  * a Quarto cross-reference renders as "Section 5.2 ." with the space before   #
#    the stop, so a quote must not END at one — stop the span before it.         #
#  * inline expressions render to numbers; a quote that spans one is grounded    #
#    but reseed-fragile, so cut the span before the number where the number is   #
#    not the point of the span.                                                  #
# --------------------------------------------------------------------------- #
H_RHET_SPANS = [
    # ---- Executive summary: the thesis and its bounds -----------------------------
    ("R00", "claim", "Executive summary",
     "The step forms no critical quality attribute.", ["R06", "R25", "R36"], None, None),
    ("R01", "claim", "Executive summary",
     "The parameters of the step therefore act on process performance, and they were "
     "characterized against clarification efficiency and product yield", ["R06"], None, None),
    ("R02", "claim", "Executive summary",
     "none of the three moved a quality attribute anywhere it was tested",
     ["R36"], None, None),
    ("R03", "cross_step_credit", "Executive summary",
     "that result is delivered by the three chromatographic clearance steps reported in "
     "PCR-005, PCR-007 and PCR-008 and not by harvest", [], None, None),
    ("R04", "deviation_disposition", "Executive summary",
     "Both were investigated, both were dispositioned as retained, and neither changed a "
     "parameter classification or a reported range", [], None, None),
    ("R05", "bounded_conclusion", "Executive summary",
     "The step is well understood over the ranges studied, those ranges are justified for "
     "Stage 2, and every conclusion here is bounded by them, by the qualified scale-down "
     "model, and by a feed drawn from a culture operated inside the endpoint ranges "
     "characterized in PCR-003", [], None, "R00"),
    # ---- §1 Introduction: the mechanism that licenses the thesis ------------------
    ("R06", "mechanistic_warrant", "Product and unit operation",
     "Both stages are physical separations. Neither introduces a chemical condition capable "
     "of altering the antibody (no pH shift, no elution buffer, no hold at a denaturing "
     "condition), and neither discriminates between product variants.", [], None, None),
    ("R07", "claim", "Product and unit operation",
     "The step forms no quality attribute of its own, so there is nothing here for a design "
     "space to protect.", ["R06"], None, None),
    ("R08", "cross_step_credit", "Regulatory and scientific basis",
     "No log reduction is credited to this step anywhere in the package, and none is claimed "
     "here.", [], None, None),
    # ---- §2 Prior knowledge: the expectations the study was built to test ---------
    ("R09", "justification", "Platform and prior-product knowledge",
     "This experience constitutes prior product knowledge and may be applied directly to "
     "A-Mab, because the separation is governed by particle size and density and not by any "
     "property that differs between these molecules.", [], None, None),
    ("R10", "mechanistic_warrant", "Platform and prior-product knowledge",
     "Depth filter loading governs how much of the available filter capacity is consumed, so "
     "it determines how close the train runs to breakthrough.", [], None, None),
    ("R11", "problem_statement", "Platform and prior-product knowledge",
     "One mechanism could in principle link this step to a quality attribute. Hydrodynamic "
     "shear in the feed zone of a disk-stack centrifuge can damage protein, and shear induced "
     "damage would appear as an increase in high molecular weight species (HMW), which is "
     "measured by size exclusion chromatography (AMV-3011).", [], None, None),
    ("R12", "cross_step_credit", "Quality attributes in scope",
     "Host cell protein is reduced by Protein A capture (PCR-005), by cation exchange "
     "(PCR-007) and by anion exchange (PCR-008).", [], None, None),
    ("R13", "justification", "Risk-based prioritization and parameter selection",
     "None of them has a path to a critical quality attribute", [], None, None),
    ("R14", "hedge", "Risk-based prioritization and parameter selection",
     "Those are pre-characterization scores, and the decision they feed is the study type and "
     "not a classification.", [], None, None),
    ("R15", "justification", "Risk-based prioritization and parameter selection",
     "Opening them further would have added knowledge space with no prospect of a quality "
     "finding.", [], None, None),
    # ---- §3 Materials and methods: what the model does and does not warrant -------
    ("R16", "bounded_conclusion", "Scale-down model and its qualification",
     "The model reproduces the separation that the commercial equipment performs and the "
     "product recovery it achieves, but it does not reproduce the full shear history of a "
     "commercial disk stack, because feed zone geometry does not scale linearly with "
     "throughput.", [], None, None),
    ("R17", "hedge", "Scale-down model and its qualification",
     "Any claim in this report that rests on shear is therefore supported by the size variant "
     "measurement across the step and by platform experience, and not by the model alone.",
     [], None, None),
    ("R18", "deferral", "Scale-down model and its qualification",
     "the qualification report is held under SOP-1001 and is not reproduced here",
     [], None, None),
    ("R19", "justification", "Statistical methods",
     "A screening fit is not used to predict, because it is near-saturated and carries no "
     "curvature.", [], None, None),
    ("R20", "claim", "Statistical methods",
     "so no screening design was run, no response surface model was fitted, and no design "
     "space is defined at this step", ["R13", "R19"], None, None),
    ("R21", "bounded_conclusion", "Statistical methods",
     "A univariate study supports a proven acceptable range (PAR) for one parameter at a "
     "time, with the others held at their set-points, but it does not resolve interactions "
     "between parameters and it cannot define a multivariate operating region. This report "
     "claims only what that design supports.", [], None, "R20"),
    # ---- §4 Study design ----------------------------------------------------------
    ("R22", "problem_statement", "Univariate assessment",
     "These two conditions bound the interaction that the univariate scans cannot resolve, "
     "and they are the only multi-parameter conditions the study contains.", [], None, None),
    # ---- §5 Results ---------------------------------------------------------------
    ("R23", "claim", "Nominal performance and mass balance",
     "Step yield was characterized as independent of all three parameters over the ranges "
     "studied.", [], None, None),
    ("R24", "claim", "Centrifugation across its characterization range",
     "Applied centrifugal field governs the solids load passed to the depth filter train, and "
     "it has no effect on any product quality attribute.", ["R25"], None, None),
    ("R25", "justification", "Centrifugation across its characterization range",
     "There was no increase in high molecular weight species at the high edge (SEC-HPLC, "
     "AMV-3011), which is the evidence that bears on the shear mechanism", [], None, None),
    ("R26", "hedge", "Centrifugation across its characterization range",
     "Shear in the feed zone of a commercial centrifuge does not scale from this model, so "
     "the finding is supportive and not conclusive, and it is confirmed at scale in Stage 2.",
     [], None, None),
    ("R27", "claim", "Depth filter loading and clarification capacity",
     "The bounding condition that combines the high loading edge with the low centrifugation "
     "edge produced the only post-clarification turbidity in the study that fell outside a "
     "normal operating range.", ["R28"], None, None),
    ("R28", "mechanistic_warrant", "Depth filter loading and clarification capacity",
     "A depth filter approaching the end of its capacity behaves that way, because retained "
     "solids reduce the available depth and progressively less of the challenge is captured.",
     [], None, None),
    ("R29", "justification", "Depth filter loading and clarification capacity",
     "so it is a real change in the stream and not analytical variation", [], None, None),
    ("R30", "claim", "Depth filter loading and clarification capacity",
     "Nothing about that excursion touches product quality.", ["R31"], None, None),
    ("R31", "justification", "Depth filter loading and clarification capacity",
     "The paired comparisons of host cell protein, residual DNA and size variants across the "
     "step were within method precision on the affected run, as they were on every other run "
     "of the study.", [], None, None),
    ("R32", "justification", "Post-clarification turbidity",
     "A centrifuge that under-performs and a depth filter train that is over-loaded both end "
     "at the same observable, so a single in-process measurement covers both failure modes "
     "and no separate test of centrate quality is required for batch release.",
     [], None, None),
    ("R33", "mechanistic_warrant", "Impurity burden delivered to capture",
     "That is the expected result, because both impurities are soluble and both stages of "
     "this operation are particle separations.", [], None, None),
    ("R34", "cross_step_credit", "Impurity burden delivered to capture",
     "The burden entering capture is controlled upstream, by holding the culture endpoint "
     "inside the ranges that PCR-003 characterizes, and it is reduced downstream by the three "
     "chromatographic steps", [], None, None),
    ("R35", "claim", "Product quality across the step",
     "No product quality attribute of A-Mab is altered by harvest and clarification.",
     ["R36", "R06"], None, None),
    ("R36", "justification", "Product quality across the step",
     "Every paired comparison across the step lay within the precision of its method, at the "
     "set-point condition and at both edges of all three parameter ranges", [], None, None),
    ("R37", "bounded_conclusion", "Product quality across the step",
     "The finding is bounded by the scale-down limitation in Section 3.1 and by the precision "
     "of the SEC method (AMV-3011).", [], None, "R35"),
    ("R38", "hedge", "Product quality across the step",
     "it does not by itself close the question at commercial scale", [], None, None),
    # ---- §6 Design space ----------------------------------------------------------
    ("R39", "claim", "Design space",
     "No design space is defined for harvest and clarification.", ["R40", "R36"], None, None),
    ("R40", "justification", "Design space",
     "There is no attribute for such a region to protect, no response surface model from "
     "which to construct one, and no interaction between the three parameters that a "
     "multivariate region would need to describe.", [], None, None),
    ("R41", "bounded_conclusion", "Design space",
     "Three bounds apply to everything in this section, and they apply again wherever this "
     "report states a result.", [], None, "R39"),
    ("R42", "deferral", "Design space",
     "The design space of the A-Mab drug substance is defined at the steps that set and clear "
     "quality attributes, and it is consolidated in PCMR-001.", [], None, None),
    # ---- §7 Proven acceptable ranges ----------------------------------------------
    ("R43", "claim", "The ranges",
     "the proven acceptable range is the full characterization range, and the normal "
     "operating range sits inside it with margin on both sides", ["R44"], None, None),
    ("R44", "justification", "Acceptance basis",
     "No model was fitted at this step, so each range is established directly from the "
     "univariate scans, with the two bounding conditions of Section 4.2 standing in for the "
     "co-variation that the Monte-Carlo analysis would otherwise cover.", [], None, None),
    ("R45", "bounded_conclusion", "The ranges",
     "These are also univariate ranges, determined one parameter at a time with the others at "
     "their set-points, so they are not a multivariate region and the only evidence about "
     "combinations is the two bounding conditions.", [], None, "R43"),
    # ---- §8 Process capability -----------------------------------------------------
    ("R46", "claim", "What is and is not attributed to this step",
     "No commercial-scale process capability is attributed to harvest and clarification.",
     ["R47"], None, None),
    ("R47", "justification", "What is and is not attributed to this step",
     "A capability index compares the distribution of an attribute against its acceptance "
     "criterion, and this step sets no attribute for which such a comparison exists, so "
     "reporting one for the step would credit it with control that it does not exercise.",
     [], None, None),
    ("R48", "cross_step_credit", "What is and is not attributed to this step",
     "Every one of those results is earned downstream, by the steps named in Section 2.2 for "
     "the two impurities and by cation exchange (PCR-007) for aggregate.", [], None, None),
    ("R49", "bounded_conclusion", "Robustness of the step itself",
     "so the robustness holds for a feed drawn from a culture operated inside the endpoint "
     "ranges of PCR-003. Confirmation at commercial scale is a Stage 2 activity and is not "
     "claimed here.", [], None, "R23"),
    # ---- §9 Parameter classification ------------------------------------------------
    ("R50", "claim", "Parameter classification",
     "No parameter of this step is a critical process parameter or a well controlled critical "
     "process parameter.", ["R51", "R36"], None, None),
    ("R51", "justification", "Parameter classification",
     "That outcome follows directly from the register: no critical quality attribute is set "
     "here, and no parameter of the step has a demonstrated effect on one.", [], None, None),
    ("R52", "justification", "Parameter classification",
     "The null results behind those classifications are retained in the knowledge space and "
     "are not dropped, since they are the evidence that allows the step to be operated to "
     "process performance limits alone", [], None, None),
    # ---- §10 Control strategy --------------------------------------------------------
    ("R53", "cross_step_credit", "Contribution to the control strategy",
     "The step does not reduce host cell protein or residual DNA toward the drug substance "
     "limits, and that reduction is delivered by Protein A capture, cation exchange and anion "
     "exchange.", [], None, None),
    ("R54", "deferral", "Contribution to the control strategy",
     "They are consolidated across the process in PCMR-001.", [], None, None),
    # ---- §11-12 Discussion and conclusions -------------------------------------------
    ("R55", "hedge", "Discussion",
     "Confidence in the scale-down model is high for what the model was used to conclude, and "
     "it is lower for one specific question.", [], None, None),
    ("R56", "bounded_conclusion", "Discussion",
     "A univariate design cannot resolve interactions, so the only evidence about parameter "
     "combinations is the two bounding conditions", [], None, "R43"),
    ("R57", "claim", "Conclusions",
     "Harvest and clarification is well understood over the ranges characterized, and it is "
     "ready to support Stage 2 at the ranges reported.", ["R36", "R52"], None, None),
    ("R58", "restatement", "Conclusions",
     "None is quality-linked, and the proven acceptable range of each is its full "
     "characterization range", [], "R43", None),
    # ---- §13 Deviations ---------------------------------------------------------------
    ("R59", "deviation_disposition", "Deviations from the plan",
     "Each was investigated, each was assessed for impact on the study and on the material, "
     "and each was dispositioned as retained.", [], None, None),
    ("R60", "deviation_disposition", "DEV-004-01, depth filter pre-use flush",
     "The delivered volume was short of the specified volume, and the root cause was recorded "
     "as an insufficient initial flush volume.", [], None, None),
    ("R61", "justification", "DEV-004-01, depth filter pre-use flush",
     "Pre-use flush turbidity is measured on flush water before any product contact, so it "
     "reports on the condition of the filter media and not on the product stream.",
     [], None, None),
    ("R62", "deviation_disposition", "DEV-004-02, post-clarification turbidity excursion",
     "The deviation was dispositioned as retained, and the run is included in this report.",
     ["R63", "R31"], None, None),
    ("R63", "justification", "DEV-004-02, post-clarification turbidity excursion",
     "the root cause was recorded as depth filter loading near its maximum", [], None, None),
    ("R64", "claim", "DEV-004-02, post-clarification turbidity excursion",
     "The excursion also earns its place in the control strategy.", [], None, None),
    ("R65", "restatement", "Conclusions",
     "It delivers the process impurity burden generated during culture to Protein A capture "
     "and removes none of it, so its contribution to the impurity attributes is the delivery "
     "of a consistently clarified feed.", [], "R53", None),
]


def h_rhetorical_spans(doc_id, file_name):
    """Rhetorical / argument-structure spans over the PCR-004 report (report-only)."""
    out = []
    for suffix, role, sec, quote, sup, res, bnd in H_RHET_SPANS:
        out.append(S.RhetoricalSpan(
            span_id=f"{doc_id}-{suffix}", section=sec, role=role,
            source_reference=ref(doc_id, file_name, f"{doc_id}_sec_rhet", sec,
                                 " ".join(quote.split())),
            supported_by=[f"{doc_id}-{s}" for s in sup],
            restates=(f"{doc_id}-{res}" if res else None),
            bounds=(f"{doc_id}-{bnd}" if bnd else None)))
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
        weak_claims=build_weak_claims(doc, f),
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Harvest forms no product-quality CQA and no DesignSpace is present. The attributes "
            "the clarified harvest carries into the purification train are captured as "
            "assertions on the rendered register rows, not as QualityAttribute entities, "
            "because this step neither sets nor governs them.",
            "No designed experiment is planned for this step: the only StudyDesign entries are "
            "the univariate series (one per parameter) and the scale-down model qualification.",
            "The planned confirmation set (§6.2) runs the other parameters at the least "
            "favourable normal-operating corner. It is a multi-parameter corner check with no "
            "matching StudyDesign.study_type, so it is carried in report_sections instead.",
            "Process-performance measures (yield, turbidity, differential pressure) have no dedicated field; captured via report_sections/assertions.",
            "The Plan states classification is an OUTPUT; parameter_type left 'unclassified' here.",
            "The plan is prospective and explicitly declines to assume the quality outcome "
            "('which the study will confirm and not assume'), so it carries NO "
            "parameter_does_not_significantly_impact_attribute assertions; those exist only in "
            "PCR-004, where the null result was actually observed.",
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
        weak_claims=build_weak_claims(doc, f),
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT + [
            "ProvenAcceptableRange (new model) — per-parameter PAR against process-performance "
            "criteria (no CQA, no fitted model, so no NOR-propagated value)",
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "Harvest forms no product-quality CQA and no DesignSpace is present. The seven "
            "attributes present in the harvested stream are captured as assertions on their "
            "rendered register rows, not as QualityAttribute entities, because the step "
            "neither sets nor governs any of them.",
            "No designed experiment was executed and no response-surface model was fitted: the "
            "report states this explicitly and claims no design space for the step.",
            "The two bounding conditions of §4.2 are multi-parameter corner runs with no "
            "matching StudyDesign.study_type; they are carried in report_sections and in the "
            "rhetorical layer instead.",
            "ProvenAcceptableRange.quality_attribute has no applicable value here; the acceptance "
            "basis is carried in acceptance_basis instead.",
            "Process-performance results (step yield, turbidity, commercial-scale capability of "
            "the attributes carried forward) have no dedicated field; reported as "
            "report_sections statements anchored on their rendered table rows.",
            "rhetorical_spans are verbatim report prose annotating the step's negative argument "
            "(no design executed, no design space claimed, no clearance credit taken) and the "
            "credit it hands to PCR-005 / PCR-007 / PCR-008; PCR-004 carries no weak_claims.",
        ],
        inventory=h_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=h_studies(doc, f, report=True),
        proven_acceptable_ranges=h_proven_acceptable_ranges(doc, f),
        report_sections=h_report_sections(doc, f, report=True),
        assertions=h_assertions(doc, f, report=True), concepts=h_concepts(),
        rhetorical_spans=h_rhetorical_spans(doc, f))


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
# The report names the chamber the design runs were executed in (§3.1); its description and
# calibration status come from the seeded equipment register, never typed.
PA_CHAMBER_ID = "EQ-CHR-118"
# Significance level both documents state (a statistical convention, not a seeded value —
# the same literal the .qmd carries as ALPHA); several quotes render it.
PA_ALPHA = 0.05
PA_WCCPP = ["Protein load", "Elution buffer pH"]      # drive eluate-pool HCP
PA_KPP = ["Load flow rate", "End of pool collect"]    # drive step yield

# Attributes. Both re-authored documents split the register into two rendered tables: the
# one CQA the step SETS (plan Table 4 / report Table 4) and the attributes carried into the
# step from upstream, which it reduces or passes through (plan Table 5 / report Table 5).
# Aggregate is in that second table in both documents — the step passes it through unchanged
# and PCR-007 polishes it — so the annex now carries it as well.
PA_CQA_SET_KEYS = ["leached_protein_a"]
PA_CQA_UPSTREAM_KEYS = ["hcp", "residual_dna", "aggregates_hmw"]
PA_CQA_KEYS = PA_CQA_SET_KEYS + PA_CQA_UPSTREAM_KEYS
PAATTR_CONCEPT = {
    "leached_protein_a": "attr:leached_protein_a",
    "hcp": "attr:hcp", "residual_dna": "attr:residual_dna",
    "aggregates_hmw": "attr:aggregates_hmw",
}
PAATTR_NAME = {
    "leached_protein_a": "Leached Protein A", "hcp": "Host Cell Protein (HCP)",
    "residual_dna": "Residual DNA", "aggregates_hmw": "Aggregates (HMW)",
}
PA_CQA_METHOD = {"leached_protein_a": "AMV-3016", "hcp": "AMV-3012",
                 "residual_dna": "AMV-3014", "aggregates_hmw": "AMV-3011"}
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
# Both documents were re-authored, so every prose fragment here was re-anchored #
# against the new text. Table relations are NOT anchored on prose or on a       #
# caption at all: they take their own rendered row through row_quotes(), which  #
# rebuilds the row from the same DataFrame the document renders, so the span    #
# carries both ends of the relation and follows the seed.                       #
# --------------------------------------------------------------------------- #
# Analytical methods: the sentence that names the analyte AND the method that
# measures it. Plan §5.3 / Report §3.3, both titled "Analytical methods".
PA_METHOD_QUOTE = {
    "AMV-3016": ("leached Protein A is measured on the same pool sample by the ELISA of AMV-3016",
                 "Leached Protein A is measured by the ELISA validated under AMV-3016."),
    "AMV-3012": ("Pool HCP is measured on the eluate pool by the host cell protein ELISA of "
                 "AMV-3012",
                 "Pool host cell protein is measured by the ELISA validated under AMV-3012."),
    "AMV-3014": ("Residual DNA (AMV-3014) and size variants by SEC (AMV-3011) are measured on the "
                 "load and on the pool of the centre-point runs.",
                 "residual DNA by qPCR (AMV-3014)"),
    "AMV-3011": ("size variants by SEC (AMV-3011) are measured on the load and on the pool of the "
                 "centre-point runs",
                 "Size variants are measured by SEC-HPLC (AMV-3011)"),
}
# Rendered captions of the two attribute tables, per document. The caption is metadata on the
# reference (table_title); the QUOTE is always the attribute's own row — see pa_cqa_rows().
PA_CQA_TABLE = {
    ("plan", "set"): "The drug substance quality attribute set by the capture step.",
    ("plan", "up"): "Drug substance quality attributes cleared or carried through the capture step.",
    ("report", "set"): ("The quality attribute set by the Protein A step, with its criticality "
                        "from the A-Mab Tool #1 assessment."),
    ("report", "up"): ("Attributes carried into the Protein A step from upstream, which the step "
                       "reduces or passes through."),
}
# Report §9 "Parameter classification": the sentence that names the parameter, states its class
# and gives the finding the class rests on — both ends of the relation in one span.
PA_CLASS_QUOTE = {
    "Protein load": ("Protein load is a well-controlled critical process parameter. It has a "
                     "significant effect on pool HCP and interacts with elution buffer pH"),
    "Elution buffer pH": ("Elution buffer pH is a well-controlled critical process parameter. It "
                          "carries the largest effect on pool HCP of any parameter studied"),
    "Load flow rate": ("Load flow rate is a key process parameter. Its effect on pool HCP does not "
                       "reach significance in the predictive model"),
    "End of pool collect": ("End of pool collect is a key process parameter. It carries the "
                            "largest effect on step yield of any parameter in the study, and it "
                            "also has a significant effect on pool HCP"),
    "Operating temperature": ("Operating temperature is a general process parameter. The "
                              "univariate assessment linked it to no quality attribute across its "
                              "characterization range"),
    "Bed height": ("Bed height is a general process parameter. It was assessed univariately, it is "
                   "linked to no quality attribute"),
}
# Plan §4.1 / §4.3 / §6.4: the prior-knowledge expectation stated for each parameter before the
# study runs. Tuple is (rendered section title, verbatim fragment).
PA_PRIOR_QUOTE = {
    "Protein load": ("Unit-operation description and prior knowledge",
                     "Protein load is expected to be the dominant parameter for pool HCP"),
    "Elution buffer pH": ("Unit-operation description and prior knowledge",
                          "Elution buffer pH is expected to act on pool HCP in the opposite "
                          "direction"),
    "Load flow rate": ("Risk-based prioritization of parameters",
                       "Load flow rate and end of pool collect were carried into the multivariate "
                       "design for a different reason, since neither is expected to move product "
                       "quality on its own"),
    "Operating temperature": ("Univariate assessment",
                              "Operating temperature acts on binding kinetics and on the stability "
                              "of the immobilized ligand, and platform manufacture has not shown "
                              "an effect of temperature on pool quality"),
    "Bed height": ("Univariate assessment",
                   "Bed height acts on the step through residence time, and residence time is "
                   "already varied in the multivariate design through the load flow rate"),
}
# Report §7 caption. The PAR records quote their own @tbl-par row, not this caption.
PA_PAR_TABLE = ("Proven acceptable ranges by attribute and parameter, from the fitted "
                "response-surface models.")


def _pa_cqa_row(key):
    return P.cqa_reg[P.cqa_reg.key == key].iloc[0].to_dict()


def pa_cqa_rows():
    """``{attribute key -> its own rendered attribute-table row}``.

    Both documents render the same two DataFrames — ``cqas_for(protein_a)`` for the attribute
    the step sets and ``cqas_by_keys([...])`` for the attributes it carries in from upstream —
    with the same default float format, so one row map serves plan and report. The row names
    the attribute, its acceptance criterion, its criticality and its Tool #1 score, which is
    the whole of what a QualityAttribute record asserts.
    """
    rows = row_quotes(P.cqas_for(PAUO), PA_CQA_SET_KEYS)
    rows.update(row_quotes(P.cqas_by_keys(PA_CQA_UPSTREAM_KEYS), PA_CQA_UPSTREAM_KEYS))
    return rows


def pa_param_rows(classified):
    """``{parameter name -> its own rendered @tbl-params row}``.

    The report table carries the final classification (Parameter / Unit / Set-point / NOR /
    Char. range / Class / Study); the plan table carries the ranges to be studied and the
    study type RA-001 assigned. Different column orders, so each document gets its own rows.
    """
    df = P.report_params(PAUO) if classified else P.plan_params(PAUO)
    return row_quotes(df, df["Parameter"])


def pa_ph_cap():
    """Upper edge of the NOR-propagated PAR for elution buffer pH, from the DoE engine.

    This is the number both documents render as the cap on the design space (report §6 and
    §12): above it the upper bound of the 95 % predictive interval for leached Protein A
    reaches the acceptance criterion. It is read from ``doe_report``, never typed.
    """
    import doe_report as D
    return float(D.par_nor_propagated(PAUO, D.responses(PAUO)[2], "elution_ph")["par_nat"][1])


def pa_step(doc_id, file_name, sec, report):
    # Two references each: the span that fixes the step's position in the train, and the span
    # that states what it does to product quality (sets one attribute, clears two).
    if report:
        src = [ref(doc_id, file_name, sec, "Executive summary",
                   "Protein A affinity chromatography is the capture step of the A-Mab drug "
                   "substance process and the first chromatographic operation in the purification "
                   "train."),
               ref(doc_id, file_name, sec, "Executive summary",
                   "It is the step at which leached Protein A enters the process, and it provides "
                   "the principal clearance of host cell protein and residual DNA.")]
    else:
        src = [ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                   "Protein A capture is Step 5, between clarification and low-pH viral "
                   "inactivation."),
               ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                   "Two things happen to product quality across the step, since host cell protein "
                   "and residual DNA are cleared and a small amount of the Protein A ligand "
                   "leaches from the resin into the pool.")]
    return S.ProcessStep(
        step_id="step:protein_a", step_name=PAUO_NAME, step_number=str(PASTEP),
        unit_operation=PAUO_NAME,
        description="Affinity capture on Protein A resin, operated in bind-and-elute mode: binds "
                    "the antibody from clarified harvest, is the principal point of host cell "
                    "protein and residual DNA removal, and sets leached Protein A — the only "
                    "quality attribute the step forms. Makes no viral clearance and no aggregate "
                    "clearance claim, and does not modify the glycan and charge variant attributes "
                    "formed in cell culture.",
        input_materials=["clarified harvest (Protein A load)"],
        output_materials=["Protein A eluate pool (viral-inactivation feed)"],
        equipment=["Protein A affinity column", "scale-down chromatography column"],
        source_references=src, metadata=meta())


def pa_equipment(doc_id, file_name, sec, report):
    # Both documents describe the scale-down model in "Scale-down model and its
    # qualification" (plan §5.1 / report §3.1). Only the plan names the commercial column;
    # only the report names the chamber the runs were executed in.
    sdm = S.Equipment(
        equipment_id="equip:pa_sdm_column", equipment_name="scale-down chromatography column",
        equipment_type="chromatography column (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Scale-down model and its qualification",
                               "The characterization was executed on a qualified laboratory-scale "
                               "model of the commercial capture step, operated under SOP-2007 and "
                               "qualified under SOP-1001." if report
                               else "The study will be executed on a scale-down model of the "
                                    "commercial capture column, qualified under SOP-1001 before "
                                    "any design run is executed.")],
        metadata=meta())
    if report:
        # New in the re-authored report: the qualified chromatography chamber is named, with
        # its calibration status, in "Scale-down model and its qualification".
        eq = P.equipment_df().set_index("Equipment").loc[PA_CHAMBER_ID]
        chamber = S.Equipment(
            equipment_id="equip:pa_chamber", equipment_name=PA_CHAMBER_ID,
            equipment_type=str(eq["Description"]), site_name=P.SENDING_SITE,
            source_references=[ref(doc_id, file_name, sec,
                                   "Scale-down model and its qualification",
                                   f"The runs were executed in the temperature-controlled "
                                   f"chromatography chamber {PA_CHAMBER_ID}, which was "
                                   f"{eq['Calibration status']} and whose next calibration was due "
                                   f"{eq['Next calibration due']}.")],
            metadata=meta())
        return [sdm, chamber]
    return [
        S.Equipment(equipment_id="equip:pa_column",
                    equipment_name="commercial-scale Protein A capture column",
                    equipment_type="chromatography column", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec,
                                           "Scale-down model and its qualification",
                                           "Bed height is matched to the commercial column for "
                                           "the qualification runs and for every run of the "
                                           "multivariate designs")],
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
    # The rendered @tbl-params captions of the two re-authored documents. The caption is
    # metadata; each parameter anchors on ITS OWN row of that table.
    caption = ("Parameters of the Protein A step, with the ranges studied and the "
               "classification resulting from this study."
               if classified else
               "Process parameters of the capture step, the ranges to be studied and the study "
               "type assigned by RA-001.")
    rats = {"WC-CPP": "Carries a significant effect on pool host cell protein — the impurity load "
                      "the polishing steps have to handle — and is verified by measurement before "
                      "use, so an excursion outside the design space is unlikely.",
            "KPP": "Governs step yield / process consistency; not linked to the quality attribute "
                   "this step sets, and its effect on pool host cell protein (where it has one) is "
                   "controlled downstream and not here.",
            "GPP": "Assessed univariately and linked to no quality attribute over its "
                   "characterization range."}
    rows = pa_param_rows(classified)
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
                                   table_id=f"{doc_id}_tab_params")],
            metadata=meta()))
    return out


def pa_cqas(doc_id, file_name, sec, report):
    """The one attribute the step SETS plus the three it carries in from upstream.

    Every criterion here is a DRUG SUBSTANCE criterion. Neither document treats any of them
    as an in-process limit on the capture pool — the report says so in §7 ("Neither is an
    in-process limit for the capture pool") and then reports that the pool does not meet the
    host cell protein limit at any setting studied. The criterion is therefore recorded as the
    attribute's drug-substance acceptance, and the step-level position is carried by the
    assertions, the PAR rows and the report sections.

    Each record anchors on its own rendered row of the attribute table, which carries the
    attribute, its criterion, its criticality and its Tool #1 score in one span.
    """
    rows = pa_cqa_rows()
    kind = "report" if report else "plan"
    out = []
    for key in PA_CQA_KEYS:
        r = _pa_cqa_row(key)
        table_title = PA_CQA_TABLE[(kind, "set" if key in PA_CQA_SET_KEYS else "up")]
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
                                   table_id=f"{doc_id}_tab_cqa")],
            metadata=meta()))
    return out


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
    cp_rsm = P.doe_centre_points(PAUO, "rsm")
    rsm_df = P.csv(f"doe_{PAUO}_rsm.csv")
    n_rsm_fact = int((rsm_df.run_type == "factorial").sum())
    n_rsm_ax = int((rsm_df.run_type == "axial").sum())
    n_mv = len(PA_MULTIVARIATE)
    # The report states the response-surface design with its run counts, which are seeded
    # values; the quote is rebuilt from the same CSV the document counts them from.
    rsm_quote_report = (f"The design is a face-centred central composite design of {n_rsm} runs: "
                        f"{n_rsm_fact} factorial runs, {n_rsm_ax} axial runs on the faces of the "
                        f"cube and {cp_rsm} replicated centre points.")
    scr_quote_plan = (f"The screening study is a two-level full factorial in the {n_mv} "
                      f"multivariate parameters with replicated centre points.")
    rsm_quote_plan = (f"The response-surface study is a face-centred central composite design in "
                      f"the same {n_mv} parameters.")
    responses = ["pool_hcp_ng_mg", "step_yield", "leached_protein_a_ppm"]
    studies = [
        S.StudyDesign(
            study_id="study:pa_screening", study_type="screening_doe",
            design_name="two-level full factorial", unit_operation=PAUO_NAME,
            factors=PA_MULTIVARIATE, responses=responses,
            n_runs=n_scr, n_center_points=P.doe_centre_points(PAUO, "screening"), scale_down_model="scale-down chromatography column",
            associated_parameters=[PAPARAM_CONCEPT[f] for f in PA_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Screening design",
                                   "The screening study was a two-level full factorial in the four "
                                   "multivariate parameters, augmented with centre points."
                                   if report else scr_quote_plan)],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:pa_rsm", study_type="response_surface_doe",
            design_name="face-centred central composite design", unit_operation=PAUO_NAME,
            factors=PA_MULTIVARIATE, responses=responses,
            n_runs=n_rsm, n_center_points=P.doe_centre_points(PAUO, "rsm"), scale_down_model="scale-down chromatography column",
            associated_parameters=[PAPARAM_CONCEPT[f] for f in PA_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   rsm_quote_report if report else rsm_quote_plan)],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:pa_sdm_qual", study_type="scale_down_qualification",
            unit_operation=PAUO_NAME, scale_down_model="scale-down chromatography column",
            source_references=[ref(doc_id, file_name, f"{doc_id}_sec_methods",
                                   "Scale-down model and its qualification",
                                   "Qualification compared the small-scale system against "
                                   "commercial-equivalent runs on the inputs and the outputs that "
                                   "matter to this step" if report
                                   else "Qualification will compare replicate runs of the "
                                        "scale-down model at the set-point against the at-scale "
                                        "data recorded for the same step in clinical "
                                        "manufacture")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:pa_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=PAUO_NAME,
            factors=PA_UNIVARIATE, responses=responses,
            associated_parameters=[PAPARAM_CONCEPT[f] for f in PA_UNIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Univariate assessment",
                                   "Operating temperature and bed height were assessed one "
                                   "parameter at a time" if report
                                   else "Operating temperature and bed height will be assessed one "
                                        "parameter at a time")],
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
    for key in PA_CQA_KEYS:
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

    def add(subj, pred, obj, text, sec, quote):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote)], metadata=meta()))

    # step -> parameter: each assertion anchors on that parameter's OWN rendered @tbl-params
    # row, which names the parameter, its set-point and its ranges. The former single sentence
    # ("The step carries 6 process parameters") stood in for all six records and named none.
    param_sec = ("Factors, ranges and the knowledge space" if report
                 else "Factors, ranges and study type")
    param_rows = pa_param_rows(report)
    for name, cid in PAPARAM_CONCEPT.items():
        add("step:protein_a", "step_has_parameter", cid,
            f"{PAUO_NAME} has process parameter {name}.", param_sec, param_rows[name])
    # The step SETS leached Protein A; it carries HCP, DNA and aggregate in from upstream.
    add("step:protein_a", "step_has_quality_attribute", "attr:leached_protein_a",
        f"{PAUO_NAME} sets leached Protein A, the only quality attribute it forms.",
        "Product and unit operation" if report else "Quality attributes in scope",
        "That released ligand is the quality attribute the step sets." if report
        else "The step sets one quality attribute of the drug substance and acts on three others.")
    upstream_quote = {
        "hcp": ("Affinity capture provides the principal clearance, and cation exchange and anion "
                "exchange clear further",
                "host cell protein is the one this step influences most, and it is the response "
                "the multivariate design was built around"),
        "residual_dna": ("Residual DNA is cleared by a mechanism that does not depend on the "
                         "parameters in Table 7",
                         "Residual DNA is of very low criticality and is reduced by a fixed "
                         "mechanism, since DNA does not bind the ligand and passes into the flow "
                         "through."),
        "aggregates_hmw": ("affinity capture under platform conditions does not modify it, so "
                           "aggregate is monitored across the step and is polished at cation "
                           "exchange",
                           "they are formed in the bioreactor and are not resolved by affinity "
                           "capture, so the step is treated as passing them through unchanged"),
    }
    upstream_text = {
        "hcp": f"{PAUO_NAME} provides the principal clearance of host cell protein; the "
               f"remaining reduction is delivered by cation and anion exchange.",
        "residual_dna": f"{PAUO_NAME} reduces residual DNA by a mechanism that does not depend on "
                        f"the parameters studied here.",
        "aggregates_hmw": f"{PAUO_NAME} does not resolve aggregate; the step passes it through "
                          f"unchanged and cation exchange polishes it.",
    }
    for key in PA_CQA_UPSTREAM_KEYS:
        add("step:protein_a", "step_has_quality_attribute", PAATTR_CONCEPT[key],
            upstream_text[key], "Quality attributes in scope",
            upstream_quote[key][1 if report else 0])
    # attribute -> method (plan only; the report links method to response, not to CQA)
    if not report:
        for key in PA_CQA_METHOD:
            add(PAATTR_CONCEPT[key], "attribute_measured_by_method", f"method:{PA_CQA_METHOD[key]}",
                f"{PAATTR_NAME[key]} is measured by {PA_CQA_METHOD[key]}.", "Analytical methods",
                PA_METHOD_QUOTE[PA_CQA_METHOD[key]][0])
    # Acceptance criteria. Both are DRUG SUBSTANCE criteria, and neither is an in-process limit
    # on the capture pool. The re-authored report is explicit that the pool does NOT meet the
    # host cell protein limit at any setting studied, so the old annex wording ("the criterion
    # is not applied at the outlet of this step") is replaced by what the document states.
    lpa, hcp = _pa_cqa_row("leached_protein_a"), _pa_cqa_row("hcp")
    ds_spec_quote = (f"Both criteria in this section are the study-provided drug substance "
                     f"specifications: {lpa['acc_low']:g}–{lpa['acc_high']:g} ppm for leached "
                     f"Protein A and {hcp['acc_low']:g}–{hcp['acc_high']:g} ng/mg for host cell "
                     f"protein. Neither is an in-process limit for the capture pool")
    plan_spec_quote = (f"Pool HCP is judged against the drug substance limit of "
                       f"{hcp['acc_high']:g} ng/mg and leached Protein A against "
                       f"{lpa['acc_high']:g} ppm")
    # The PLAN is prospective and may not state an outcome; the two texts differ for that
    # reason, and only the report's records what the study found.
    add("attr:leached_protein_a", "attribute_has_acceptance_criterion", "lit:leached_protein_a_acc",
        (f"Leached Protein A acceptance: {lpa['acc_low']:g}–{lpa['acc_high']:g} {lpa['unit']} at "
         f"drug substance. It is the attribute this step sets, and the report records it as met in "
         f"the capture pool itself." if report else
         f"Leached Protein A acceptance: {lpa['acc_low']:g}–{lpa['acc_high']:g} {lpa['unit']} at "
         f"drug substance. The plan applies the drug substance ceiling to the eluate pool, which "
         f"it states is conservative because the ion exchange steps clear the attribute before "
         f"drug substance."),
        "Proven acceptable ranges" if report else "Proven acceptable ranges (planned analysis)",
        ds_spec_quote if report else plan_spec_quote)
    add("attr:hcp", "attribute_has_acceptance_criterion", "lit:hcp_acc",
        (f"Host cell protein acceptance: {hcp['acc_low']:g}–{hcp['acc_high']:g} {hcp['unit']} at "
         f"drug substance. It is not an in-process limit for the capture pool, which does not meet "
         f"it at any setting studied; the limit is met after the cation and anion exchange steps."
         if report else
         f"Host cell protein acceptance: {hcp['acc_low']:g}–{hcp['acc_high']:g} {hcp['unit']} at "
         f"drug substance. The plan judges the pool against it as an in-process reference only, "
         f"and pre-declares that if the pool does not meet it across the region the region will be "
         f"declared on leached Protein A alone."),
        "Proven acceptable ranges" if report else "Proven acceptable ranges (planned analysis)",
        ("For pool HCP no proven acceptable range is returned for any parameter under either "
         "analysis, and the reason is that the capture pool does not meet the drug substance "
         "limit at any setting studied." if report else plan_spec_quote))
    # parameter -> attribute impacts / non-impacts
    if report:
        # Report §9: one classification sentence per parameter, naming the parameter, its class
        # and the finding the class rests on.
        for name in PA_WCCPP:
            add(PAPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:hcp",
                f"{name} carries a significant effect on pool host cell protein (WC-CPP).",
                "Parameter classification", PA_CLASS_QUOTE[name])
        # NEW against the re-authored report: end of pool collect is no longer effect-free on
        # pool host cell protein. Its coefficient is significant and negative, and the report
        # classifies it KPP because that attribute is controlled downstream, not because the
        # effect is absent.
        add(PAPARAM_CONCEPT["End of pool collect"], "parameter_impacts_attribute", "attr:hcp",
            "End of pool collect carries a significant negative effect on pool host cell protein; "
            "it is classified KPP because that attribute is controlled by the downstream polishing "
            "steps and not here.",
            "Parameter classification", PA_CLASS_QUOTE["End of pool collect"])
        add(PAPARAM_CONCEPT["Load flow rate"], "parameter_does_not_significantly_impact_attribute",
            "attr:hcp",
            "Load flow rate has no effect on pool host cell protein that reaches significance in "
            "the predictive model; it is controlled for process consistency (KPP).",
            "Parameter classification", PA_CLASS_QUOTE["Load flow rate"])
        for name in PA_UNIVARIATE:
            add(PAPARAM_CONCEPT[name], "parameter_does_not_significantly_impact_attribute",
                "attr:leached_protein_a",
                f"{name} was assessed univariately and linked to no quality attribute over its "
                f"characterization range (GPP).",
                "Parameter classification", PA_CLASS_QUOTE[name])
        # The robustness finding on the attribute the step SETS. It is a "no effect resolved"
        # result, not a "no effect exists" result, and the report keeps that distinction:
        # elution buffer pH carries the one term that reaches alpha, so it gets its own record
        # rather than being folded into a blanket claim the document no longer makes.
        for name in ["Protein load", "Load flow rate", "End of pool collect"]:
            add(PAPARAM_CONCEPT[name], "parameter_does_not_significantly_impact_attribute",
                "attr:leached_protein_a",
                f"No effect of {name.lower()} on leached Protein A was resolved by either design "
                f"over the ranges studied.",
                "Response-surface models",
                "The response-surface study confirms the screening result for pool HCP and for "
                "step yield, adds the curvature the two-level design could not see, and again "
                "resolves nothing for leached Protein A.")
        add(PAPARAM_CONCEPT["Elution buffer pH"],
            "parameter_does_not_significantly_impact_attribute", "attr:leached_protein_a",
            "No effect of elution buffer pH on leached Protein A is treated as demonstrated: the "
            "quadratic term in elution buffer pH is the only term in that model to reach "
            f"α = {PA_ALPHA:g}, and the model containing it is not significant overall. The term is "
            "nonetheless carried into the proven acceptable range analysis, where it is the reason "
            "the NOR-propagated range for this parameter stops short of the characterization "
            "range.",
            "Response-surface models",
            f"For leached Protein A the only term reaching {PA_ALPHA:g} is the quadratic in "
            f"elution buffer pH.")
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
    import doe_report as D
    lpa, hcp = _pa_cqa_row("leached_protein_a"), _pa_cqa_row("hcp")
    prm = P.report_params(PAUO)
    n_mv = int((prm["Study"] == "multivariate").sum())
    n_uv = len(prm) - n_mv
    cls = prm["Class"].value_counts().to_dict()
    scr = P.csv(f"doe_{PAUO}_screening.csv")
    rsm = P.csv(f"doe_{PAUO}_rsm.csv")
    lpa_key = D.responses(PAUO)[2]
    lpa_meas_hi = float(max(scr[lpa_key].max(), rsm[lpa_key].max()))
    ph_cap = pa_ph_cap()
    capr = P.cap.set_index("key")
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-005 defines the Stage-1 characterization study that will bound the ranges "
                  "registered for commercial manufacture of the A-Mab capture step.",
               "Purpose and scope",
               "the ranges that will be registered for commercial manufacture of A-Mab are not yet "
               "bounded by data on this product. This plan defines the study that will bound them."),
            st(2, f"{n_mv} parameters are assigned to multivariate study and {n_uv} to univariate "
                  f"assessment, following the risk ranking in RA-001.",
               "Purpose and scope",
               f"of which {n_mv} will be studied in a multivariate design and {n_uv} will be "
               f"assessed one at a time, following the risk ranking in RA-001"),
            st(3, "The study uses a full-factorial screen followed by a face-centred central "
                  "composite design on a qualified scale-down column.",
               "Response-surface design",
               f"The response-surface study is a face-centred central composite design in the same "
               f"{n_mv} parameters."),
            st(4, "The capture step sets one drug substance quality attribute and acts on three "
                  "others.",
               "Quality attributes in scope",
               "The step sets one quality attribute of the drug substance and acts on three "
               "others."),
            st(5, "The operating region will be declared from the response-surface models, on the "
                  "criterion that applies to each governed attribute across the region.",
               "Acceptance and decision criteria",
               "The operating region will be declared acceptable when the response-surface models "
               "predict that every governed attribute meets the criterion that applies to it "
               "across the region"),
            # The plan pre-declares the fallback the report then had to take. A plan may state a
            # rule; it may not state an outcome, so this is written as the conditional it is.
            st(6, "The plan pre-declares what to do if the pool does not meet the host cell "
                  "protein reference across the region: declare the region on leached Protein A "
                  "alone and resolve host cell protein across the train in PCMR-001.",
               "Acceptance and decision criteria",
               "Where the pool does not meet that reference across the region, the region will be "
               "declared on leached Protein A alone"),
            st(7, "An effect that cannot be separated from assay and process noise is "
                  "pre-declared to be reported as not detected over the range studied.",
               "Risks and assumptions",
               "An effect that cannot be separated from that noise will be reported as not "
               "detected over the range studied."),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, f"{cls.get('WC-CPP', 0)} parameters are classified WC-CPP, {cls.get('KPP', 0)} KPP "
              f"and {cls.get('GPP', 0)} GPP, and no parameter of the step is a critical process "
              f"parameter.",
           "Executive summary",
           f"The outcome is {cls.get('WC-CPP', 0)} well-controlled critical process parameters, "
           f"{cls.get('KPP', 0)} key process parameters and {cls.get('GPP', 0)} general process "
           f"parameters. No parameter at this step is a critical process parameter"),
        st(2, "Protein load and elution buffer pH are the two well-controlled critical process "
              "parameters, both through their effect on pool host cell protein.",
           "Parameter classification",
           "Elution buffer pH is a well-controlled critical process parameter. It carries the "
           "largest effect on pool HCP of any parameter studied"),
        # CORRECTED against the re-authored report. The region is NOT the whole characterized
        # region any more: it is capped in elution buffer pH by the leached Protein A
        # robustness limit of §7.
        st(3, f"The design space is the characterized region in the four multivariate parameters "
              f"with elution buffer pH capped at {ph_cap:.3g}, the robustness limit derived in the "
              f"proven acceptable range analysis.",
           "Design space",
           "The design space of the capture step is the characterized region in the four "
           "multivariate parameters, bounded above in elution buffer pH by the robustness limit "
           "derived in Section 7"),
        st(4, "Pool host cell protein is the one predictive model of the step; its predicted "
              "coefficient of determination is close to its adjusted value.",
           "Response-surface models",
           "the gap between the adjusted and predicted values is small, so the model predicts a "
           "held-out run about as well as it fits the runs it was built on"),
        st(5, "Step yield is modelled for description and bounding only: its predicted "
              "coefficient of determination is much lower than its adjusted value.",
           "Response-surface models",
           "That model is used below to describe the direction and the size of the yield effects "
           "and to bound the yield across the region."),
        st(6, "The leached Protein A model is not significant overall and its predicted "
              "coefficient of determination is negative, so no predictive claim is made for it.",
           "Response-surface models",
           "and its predicted R² is negative, so no predictive claim is made for it at all"),
        st(7, f"The operative result for leached Protein A is the measured one: the attribute met "
              f"its {lpa['acc_low']:g}–{lpa['acc_high']:g} {lpa['unit']} criterion in both "
              f"designs, at a highest measured value of {lpa_meas_hi:.2f} {lpa['unit']}.",
           "Conclusions",
           f"Leached Protein A, the attribute this step sets, met its acceptance criterion of "
           f"{lpa['acc_low']:g}–{lpa['acc_high']:g} ppm in both designs, at a highest measured "
           f"value of {lpa_meas_hi:.2f} ppm"),
        st(8, f"The design space caps elution buffer pH at {ph_cap:.3g} because the upper bound of "
              f"the 95 % predictive interval for leached Protein A reaches the criterion above "
              f"that pH.",
           "Conclusions",
           f"The design space caps elution buffer pH at {ph_cap:.3g}, because above that point the "
           f"upper bound of the 95 % predictive interval for this attribute reaches the criterion"),
        st(9, "No proven acceptable range is returned for pool host cell protein against any "
              "parameter, because the capture pool does not meet the drug substance limit at any "
              "setting studied.",
           "Proven acceptable ranges",
           "For pool HCP no proven acceptable range is returned for any parameter under either "
           "analysis, and the reason is that the capture pool does not meet the drug substance "
           "limit at any setting studied."),
        st(10, "That is the expected result for a capture step: host cell protein is cleared by "
               "three chromatography steps in series and the criterion applies to the drug "
               "substance, not to an intermediate pool.",
            "Proven acceptable ranges",
            "Host cell protein is cleared by three chromatography steps in series, and the "
            "criterion applies to the drug substance and not to an intermediate pool."),
        st(11, f"At drug substance host cell protein is the tightest of the three attributes the "
               f"step governs, at Cpk = {capr.loc['hcp', 'Cpk']:.2f} against a limit of "
               f"{capr.loc['hcp', 'acc_high']:g} {hcp['unit']}, and that capability belongs to the "
               f"three clearance steps in series and not to capture alone.",
            "Process capability and robustness",
            f"Host cell protein has the tightest capability of the three, at Cpk = "
            f"{capr.loc['hcp', 'Cpk']:.2f}, with a simulated mean of "
            f"{capr.loc['hcp', 'mean']:.1f} {hcp['unit']} against a limit of "
            f"{capr.loc['hcp', 'acc_high']:g} {hcp['unit']}"),
        st(12, "Both deviations were dispositioned as retained, and neither changed a fitted "
               "effect, a classification or the operating region.",
            "Deviations from the plan",
            "Both were dispositioned as retained, which means the affected data were kept in the "
            "reported analysis."),
    ])]


def pa_design_spaces(doc_id, file_name):
    """The design space of the capture step, as the RE-AUTHORED report defines it.

    CORRECTION. The previous annex said the region was the whole characterized region and
    that leached Protein A therefore constrained nothing. The re-authored report says the
    opposite: leached Protein A IS the binding attribute, and the region is capped in elution
    buffer pH at the NOR-propagated robustness limit, because above it the upper bound of the
    95 % predictive interval reaches the acceptance criterion. Pool host cell protein still
    does not bound the region — but not because it is met; the pool does not meet the drug
    substance limit anywhere in the region, and that limit belongs to the train.
    """
    lpa = _pa_cqa_row("leached_protein_a")
    ph_cap = pa_ph_cap()
    return [S.DesignSpace(
        design_space_id="ds:protein_a", unit_operation=PAUO_NAME,
        parameters=[PAPARAM_CONCEPT[f] for f in PA_MULTIVARIATE],
        quality_attributes_constrained=["attr:leached_protein_a"],
        definition=(
            f"The characterized region in protein load, elution buffer pH, load flow rate and end "
            f"of pool collect, bounded above in elution buffer pH at {ph_cap:.3g}. Leached Protein "
            f"A — the only quality attribute the step sets — is the binding attribute: above that "
            f"pH the upper bound of the 95 % predictive interval reaches its acceptance criterion "
            f"of {lpa['acc_low']:g}–{lpa['acc_high']:g} {lpa['unit']}. Pool host cell protein does "
            f"not bound the region, because its drug substance limit is not an in-process limit "
            f"for the capture pool; the pool meets it nowhere in the region and the clearance is "
            f"completed by the polishing steps (PCR-007, PCR-008), consolidated in PCMR-001."),
        source_references=[
            ref(doc_id, file_name, f"{doc_id}_sec_ds", "Design space",
                "The design space of the capture step is the characterized region in the four "
                "multivariate parameters, bounded above in elution buffer pH by the robustness "
                "limit derived in Section 7"),
            ref(doc_id, file_name, f"{doc_id}_sec_ds", "Design space",
                f"The design space itself is that region with elution buffer pH capped at "
                f"{ph_cap:.3g}")],
        metadata=meta())]


def pa_proven_acceptable_ranges(doc_id, file_name):
    """One ProvenAcceptableRange per governed response x multivariate parameter, from the
    same DoE engine (``doe_report.par_table``) that renders @tbl-par in §7 of the report.

    Each record now anchors on ITS OWN rendered row, which carries the attribute, the
    parameter, the characterization range and both proven acceptable ranges in one span. The
    two per-attribute prose fragments this replaced each stood in for four records and named
    no parameter.

    The pool host cell protein rows carry no range, and the report gives the reason plainly:
    the capture pool does not meet the drug substance limit at any setting studied. That is
    not a failure of the step — the limit applies to the drug substance and is met after the
    two ion exchange steps.
    """
    import doe_report as D
    lpa, hcp = _pa_cqa_row("leached_protein_a"), _pa_cqa_row("hcp")
    basis = {
        "Pool HCP (ng/mg)": (
            f"Drug substance specification for host cell protein "
            f"({hcp['acc_low']:g}–{hcp['acc_high']:g} {hcp['unit']}), applied as the upper limit "
            f"for this analysis. The report states it is not an in-process limit for the capture "
            f"pool: the pool does not meet it at any setting studied, so no proven acceptable "
            f"range is returned for any parameter under either analysis. The limit is met after "
            f"the cation and anion exchange steps (PCR-007, PCR-008) and consolidated in "
            f"PCMR-001."),
        "Leached Protein A (ppm)": (
            f"Drug substance specification for leached Protein A "
            f"({lpa['acc_low']:g}–{lpa['acc_high']:g} {lpa['unit']}), the only quality attribute "
            f"this step sets, applied as an upper limit. The whole characterization range is "
            f"proven acceptable for protein load, load flow rate and end of pool collect under "
            f"both analyses; elution buffer pH is the exception, where the NOR-propagated range "
            f"stops short of the characterization range because the upper bound of the 95 % "
            f"predictive interval reaches the criterion. That bound comes from a quadratic term "
            f"in a model that is not significant overall, so the report treats it as a "
            f"conservative limit and not as a demonstrated edge of failure. The capture step "
            f"makes no viral clearance claim."),
    }
    par = D.par_table(PAUO)
    rows = _md_rows(par, P._auto_floatfmt(par))
    out = []
    for i, (r, row) in enumerate(zip(par.to_dict("records"), rows), 1):
        cqa, param, unit = r["CQA"], r["Parameter"], (r["Unit"] or "")
        out.append(S.ProvenAcceptableRange(
            par_id=f"{doc_id}-PAR{i:02d}", unit_operation=PAUO_NAME,
            quality_attribute=cqa, parameter=param,
            characterization_range=f"{r['Char. range']} {unit}".strip(),
            par_at_setpoint=f"{r['PAR (set-point)']} {unit}".strip()
            if not str(r["PAR (set-point)"]).startswith("none") else str(r["PAR (set-point)"]),
            par_nor_propagated=f"{r['PAR (NOR)']} {unit}".strip()
            if not str(r["PAR (NOR)"]).startswith("none") else str(r["PAR (NOR)"]),
            acceptance_basis=basis[cqa],
            source_references=[ref(doc_id, file_name, f"{doc_id}_sec_par",
                                   "Proven acceptable ranges", row,
                                   table_title=PA_PAR_TABLE, table_id=f"{doc_id}_tab_par")],
            metadata=meta()))
    return out


# --------------------------------------------------------------------------- #
# Report-only discourse layer (PCR-005 only).                                   #
# --------------------------------------------------------------------------- #
# Re-anchored wholesale after PCR-005 was re-authored: every span of the         #
# previous layer quoted prose that no longer exists. Rationale, roles and edges  #
# are documented on pa_rhet_spans() below; it is part of the annex rebuild, not  #
# a later annotation pass.                                                       #
# --------------------------------------------------------------------------- #
def pa_rhet_spans():
    """Argument-structure spans over the RE-AUTHORED PCR-005.

    Every span here is a verbatim, plain-prose fragment of the RENDERED report (the .docx,
    not the .qmd: inline expressions render to numbers). The report was re-authored, so the
    whole previous layer was dead prose and every span below is new. Quotes are kept
    number-free wherever the sentence allows it, and where a seeded number is load-bearing
    the quote is rebuilt from the model rather than typed.

    Three arguments carry the report and the spans follow them.

    1. The leached Protein A result. No factor effect was resolved in either design, the
       response-surface model is not significant overall and its predicted coefficient of
       determination is negative, and the centre points show pure error large enough that
       only a large effect could have been seen. The report therefore refuses a predictive
       claim and lets the measured maximum bound the attribute.
    2. The one place that argument still bites: the quadratic term in elution buffer pH is
       the only term to reach alpha, and although the report declines to treat it as a
       demonstrated effect it carries it into the proven acceptable range analysis, where it
       stops the NOR-propagated range short and caps the design space. The previous annex
       asserted the opposite — that the region was unconstrained — which the new text
       contradicts outright.
    3. The in-process framing of pool host cell protein: the capture pool meets the drug
       substance limit nowhere in the region, that is the expected result for a capture step,
       and the clearance is completed by PCR-007 and PCR-008 (cross_step_credit).

    PCR-005 carries NO weak_claims, so no span here competes with a labeled negative.
    Tuple fields: (suffix, role, section, quote, supported_by-suffixes, restates, bounds).
    """
    ph_cap = pa_ph_cap()
    return [
        # -- Executive summary: the three headline positions ---------------------------- #
        ("R00", "claim", "Executive summary",
         "The screening design identified which factors are active. The response-surface model "
         "is the predictive model and the basis of the design space.", ["R18"], None, None),
        ("R01", "claim", "Executive summary",
         "No factor effect on leached Protein A was resolved, and no predictive claim is made "
         "for that response.", ["R20", "R21", "R14"], None, None),
        ("R02", "bounded_conclusion", "Executive summary",
         "That model resolves no factor effect, so the measured figure is the one that bounds "
         "the result.", [], None, "R01"),
        ("R03", "claim", "Executive summary",
         f"Once the pure error of the response is propagated, the upper bound of the 95 % "
         f"predictive interval reaches the criterion above elution buffer pH {ph_cap:.3g}, which "
         f"is why the design space is capped there", ["R33", "R23"], None, None),
        ("R04", "claim", "Executive summary",
         "No claim is made that this step assures the drug substance limit for host cell "
         "protein.", ["R36"], None, None),
        ("R05", "cross_step_credit", "Executive summary",
         "so the cation and anion exchange steps deliver the remaining clearance (PCR-007 and "
         "PCR-008)", [], None, None),
        ("R06", "bounded_conclusion", "Executive summary",
         "Within those bounds the step is well understood over the ranges studied, its operating "
         "region is defined, and its results roll up into PCMR-001.", [], None, None),
        # -- Introduction and prior knowledge -------------------------------------------- #
        ("R07", "mechanistic_warrant", "Product and unit operation",
         "Capture therefore does three things at once: it recovers the product, it removes the "
         "bulk of the impurity burden carried out of cell culture, and it introduces a small "
         "amount of ligand released from the resin.", [], None, None),
        ("R08", "bounded_conclusion", "Product and unit operation",
         "so neither attribute meets its drug substance criterion at this point in the train and "
         "neither is expected to", [], None, None),
        ("R09", "mechanistic_warrant", "Platform and prior-product knowledge",
         "Affinity capture is inherently robust, because the separation rests on a specific "
         "interaction between the ligand and the Fc region and not on a balance of weak forces "
         "that shifts with buffer composition.", [], None, None),
        ("R10", "claim", "Platform and prior-product knowledge",
         "The purpose of this study was therefore to confirm and bound known platform behaviour, "
         "not to discover it.", ["R09"], None, None),
        ("R11", "problem_statement", "Platform and prior-product knowledge",
         "The platform expectation was that release is small and roughly constant across the "
         "operating window, and that its cycle-to-cycle variability is comparable to the "
         "precision of the assay. This study was designed to test that expectation and not to "
         "assume it.", [], None, None),
        ("R12", "deferral", "Platform and prior-product knowledge",
         "which concluded that independent characterization would be required and that bridging "
         "from platform data would not be acceptable. Nothing in this report supports a resin "
         "change.", [], None, None),
        ("R13", "cross_step_credit", "Quality attributes in scope",
         "It is also cleared by the two ion exchange steps, so the level in the drug substance is "
         "not the level in the capture pool.", [], None, None),
        # -- Methods: the rules the results are judged by --------------------------------- #
        ("R15", "bounded_conclusion", "Scale-down model and its qualification",
         "It reproduces the hydrodynamics and the chemistry of the separation, but it does not "
         "reproduce the resin cycle history of a commercial campaign, so all runs were executed "
         "on resin within the early part of its validated life.", [], None, None),
        ("R16", "justification", "Statistical methods",
         "The predicted value is computed by leave-one-out prediction, so a model that fits its "
         "own data and predicts a held-out run poorly is visible.", [], None, None),
        ("R17", "justification", "Statistical methods",
         "A response for which no term is significant is reported as robust to the factors over "
         "the ranges studied, and the factors are retained in the knowledge space as evidence of "
         "that robustness.", [], None, None),
        ("R18", "claim", "Response-surface design",
         "This is the predictive model of the step and the basis of the design space in "
         "Section 6", [], None, None),
        # -- Results: reproducibility, screening, response surface ------------------------ #
        ("R14", "justification", "Centre-point performance and reproducibility",
         "A response with this much pure error can only resolve a large effect, which is the "
         "correct context for the leached Protein A results below.", [], None, None),
        ("R19", "problem_statement", "Centre-point performance and reproducibility",
         "so the two designs give different accounts of how reproducible this response is",
         [], None, None),
        ("R20", "justification", "Screening: factor effects",
         "which is what a model returns when its terms explain less than the degrees of freedom "
         "they consume, and no factor effect on leached Protein A was resolved by the screening "
         "design", [], None, None),
        ("R22", "hedge", "Screening: factor effects",
         "These are identifications, not predictions.", [], None, None),
        ("R21", "justification", "Response-surface models",
         "and its predicted R² is negative, so no predictive claim is made for it at all",
         [], None, None),
        ("R26", "claim", "Response-surface models",
         "Only one of these three models is predictive.", ["R27", "R21"], None, None),
        ("R27", "justification", "Response-surface models",
         "the gap between the adjusted and predicted values is small, so the model predicts a "
         "held-out run about as well as it fits the runs it was built on", [], None, None),
        ("R28", "hedge", "Response-surface models",
         "Its predicted R² is the limit on how closely any single value read off it should be "
         "taken, and the yield figures quoted in Section 6 and Section 8 carry that limit with "
         "them.", [], None, None),
        ("R29", "hedge", "Response-surface models",
         "a narrow pass should not be read as a demonstration that the quadratic form is "
         "complete", [], None, None),
        ("R23", "justification", "Response-surface models",
         f"For leached Protein A the only term reaching {PA_ALPHA:g} is the quadratic in elution "
         f"buffer pH.", [], None, None),
        ("R24", "hedge", "Response-surface models",
         "that single term is not treated as a demonstrated effect", [], None, None),
        ("R25", "deferral", "Response-surface models",
         "It is carried into the proven acceptable range analysis in Section 7 because doing so "
         "is conservative, and it is identified there as the reason one range is bounded.",
         [], None, None),
        # -- Mechanistic interpretation --------------------------------------------------- #
        ("R31", "mechanistic_warrant", "Mechanistic interpretation",
         "The interaction term is negative because the second route gates the first: impurity "
         "that was co-adsorbed only reaches the pool if the elution is aggressive enough to "
         "release it.", [], None, None),
        ("R32", "mechanistic_warrant", "Mechanistic interpretation",
         "Above the set-point the elution is already selective and the remaining species stay on "
         "the column, so the response flattens.", [], None, None),
        ("R40", "claim", "Mechanistic interpretation",
         "Over the ranges studied the data do not support that for this response, and the sign of "
         "the effect is the opposite one.", [], None, None),
        ("R42", "mechanistic_warrant", "Mechanistic interpretation",
         "Ligand release is set by the chemistry of the resin and by its cycle history, both of "
         "which were held constant, and the elution pH range studied here is not wide enough to "
         "move it against the run-to-run variability of the step.", [], None, None),
        ("R43", "claim", "Mechanistic interpretation",
         "Taken together, these mechanisms are why the operating region has to be multivariate "
         "and not a set of four independent ranges.", ["R31"], None, None),
        # -- Design space ------------------------------------------------------------------ #
        ("R30", "claim", "Design space",
         "The design space of the capture step is the characterized region in the four "
         "multivariate parameters, bounded above in elution buffer pH by the robustness limit "
         "derived in Section 7", ["R33"], None, None),
        ("R46", "justification", "Design space",
         "That corner is not excluded from the design space, because pool HCP is not an "
         "acceptance criterion at this step.", [], None, None),
        ("R47", "hedge", "Design space",
         "Those are mean levels from a model that resolves no factor effect, so the measured "
         "results bound the attribute better than the model does.", [], None, None),
        ("R48", "bounded_conclusion", "Design space",
         "The region is defined on a qualified scale-down model with resin early in its validated "
         "life and a single representative feed, so it is claimed for the commercial step through "
         "the qualification described in Section 3 and no further.", [], None, "R30"),
        # -- Proven acceptable ranges -------------------------------------------------------- #
        ("R33", "justification", "Proven acceptable ranges",
         "The binding attribute is leached Protein A and the binding statistic is the upper bound "
         "of the 95 % predictive interval, which reaches the acceptance criterion near the top of "
         "the pH range once the pure error of the response is propagated with it.",
         [], None, None),
        ("R34", "hedge", "Proven acceptable ranges",
         "It is therefore a conservative limit produced by an imprecise response, and not a "
         "demonstrated edge of failure.", [], None, None),
        ("R36", "justification", "Proven acceptable ranges",
         "For pool HCP no proven acceptable range is returned for any parameter under either "
         "analysis, and the reason is that the capture pool does not meet the drug substance "
         "limit at any setting studied.", [], None, None),
        ("R37", "claim", "Proven acceptable ranges",
         "This is the expected result for a capture step and not an adverse finding about it.",
         ["R38"], None, None),
        ("R38", "justification", "Proven acceptable ranges",
         "Host cell protein is cleared by three chromatography steps in series, and the criterion "
         "applies to the drug substance and not to an intermediate pool.", [], None, None),
        ("R39", "cross_step_credit", "Proven acceptable ranges",
         "The linkage is made in PCR-007 and PCR-008 and consolidated in PCMR-001", [], None, None),
        ("R49", "claim", "Proven acceptable ranges",
         "Where a whole characterization range is proven acceptable, as it is for three of the "
         "four parameters, the binding constraint on the operating region is not that univariate "
         "range at all; it is the corner of the multivariate region", ["R43"], None, None),
        # -- Capability and classification ----------------------------------------------------- #
        ("R41", "cross_step_credit", "Process capability and robustness",
         "That capability is a property of the three clearance steps acting in series and not of "
         "capture alone.", [], None, None),
        ("R50", "hedge", "Process capability and robustness",
         "A capability index of that size is not a useful discriminator and should not be read as "
         "one.", [], None, None),
        ("R51", "claim", "Process capability and robustness",
         "The attribute the step sets is in specification at the point it is created.",
         ["R02"], None, None),
        ("R52", "bounded_conclusion", "Process capability and robustness",
         "All of them are estimated from qualified scale-down models with parameters varying "
         "inside their NORs, so they describe the process as it is intended to be run and not its "
         "behaviour at the edges of the design space.", [], None, "R51"),
        ("R53", "claim", "Parameter classification",
         "No parameter at this step requires the most stringent class.", ["R54"], None, None),
        ("R54", "justification", "Parameter classification",
         "Affinity capture is an inherently robust separation, and the two quality-linked "
         "parameters are both measured directly before use.", [], None, None),
        ("R55", "justification", "Parameter classification",
         "Neither acts on the attribute this step sets, and the effect end of pool collect "
         "carries on pool HCP is small and is managed by the downstream polishing steps, so both "
         "are classified on process consistency and their ranges are justified on that basis.",
         [], None, None),
        # -- Control strategy and discussion ------------------------------------------------- #
        ("R44", "claim", "Contribution to the control strategy",
         "The step does not control host cell protein to its drug substance criterion, and the "
         "control strategy does not claim that it does.", ["R36"], None, None),
        ("R45", "cross_step_credit", "Contribution to the control strategy",
         "Those credits belong to PCR-007 and PCR-008.", [], None, None),
        ("R56", "deferral", "Contribution to the control strategy",
         "but the modular claim for A-Mab rests on low-pH inactivation, anion exchange and "
         "small-virus retentive filtration, and it is consolidated in PCMR-001", [], None, None),
        ("R57", "problem_statement", "Discussion",
         "The result that most constrains what can be claimed is the leached Protein A model.",
         [], None, None),
        ("R58", "restatement", "Discussion",
         "It is that they do not influence it enough to be seen against the step’s own "
         "run-to-run variation across the ranges studied, which is the more useful statement for "
         "a control strategy and the weaker one for a mechanistic claim.", [], "R01", None),
        ("R59", "hedge", "Discussion",
         "It is quoted here as the limit on how precisely the absolute level transfers to the "
         "commercial step.", [], None, None),
        ("R60", "bounded_conclusion", "Discussion",
         "The design space is not confirmed at scale at the edges of its ranges, since the study "
         "was executed on a scale-down model and the commercial step is run near its set-point.",
         [], None, "R30"),
        # -- Deviations ------------------------------------------------------------------------ #
        ("R61", "deviation_disposition", "DEV-005-01 — elution buffer prepared below target pH",
         "The run was therefore retained with its design setting.", ["R62"], None, None),
        ("R62", "justification", "DEV-005-01 — elution buffer prepared below target pH",
         "The recorded response is consistent with that setting and not with the offset the "
         "buffer record implies, and the leverage the run has on the fit is small, so keeping it "
         "does not materially change the fitted surface.", [], None, None),
        ("R63", "claim", "DEV-005-01 — elution buffer prepared below target pH",
         "The deviation is nonetheless the reason the control strategy in Section 10 keeps buffer "
         "pH release testing as a named control.", [], None, None),
        ("R64", "deviation_disposition",
         "DEV-005-02 — leached Protein A result out of trend on first assay",
         "The deviation was dispositioned as retained and no re-execution was required.",
         ["R65"], None, None),
        ("R65", "justification",
         "DEV-005-02 — leached Protein A result out of trend on first assay",
         "no conclusion of this report depends on the value of any single leached Protein A "
         "result", [], None, None),
    ]


def pa_rhetorical_spans(doc_id, file_name):
    """Rhetorical / argument-structure spans over the PCR-005 report (report-only)."""
    out = []
    for suffix, role, sec, quote, sup, res, bnd in pa_rhet_spans():
        out.append(S.RhetoricalSpan(
            span_id=f"{doc_id}-{suffix}", section=sec, role=role,
            source_reference=ref(doc_id, file_name, f"{doc_id}_sec_rhet", sec,
                                 " ".join(quote.split())),
            supported_by=[f"{doc_id}-{s}" for s in sup],
            restates=(f"{doc_id}-{res}" if res else None),
            bounds=(f"{doc_id}-{bnd}" if bnd else None)))
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
        weak_claims=build_weak_claims(doc, f),
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Pool host cell protein is an in-process response with no step-level spec; captured via "
            "StudyDesign.responses. QualityAttribute.acceptance_criteria holds the drug substance "
            "criterion, which the plan states it applies to the pool only as a conservative "
            "reference, and whose fallback (declare the region on leached Protein A alone and "
            "resolve host cell protein across the train) it pre-declares in §7.",
            "The Plan states classification is an OUTPUT; parameter_type left 'unclassified' here.",
            "PROSPECTIVE DOCUMENT: nothing here records an outcome. Every statement is a design, a "
            "rule or an expectation stated before execution; the results are in PCR-005.",
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
        weak_claims=build_weak_claims(doc, f),
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT + [
            "ProvenAcceptableRange (new model) — per-response x parameter PAR (at-set-point / "
            "NOR-propagated), including the 'none (set-point breaches)' rows for a response whose "
            "drug substance criterion the capture pool does not meet at any setting studied",
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "Pool host cell protein is an in-process response with no step-level spec. Its drug "
            "substance criterion is not an in-process limit for the capture pool, and the report "
            "records that the pool does not meet it at any setting studied, so no PAR is returned "
            "for it and the train-wide position is deferred to PCR-007 / PCR-008 / PCMR-001.",
            "Leached Protein A is a robustness result, not a modelled response: no factor effect "
            "was resolved in either design and the response-surface model is not significant "
            "overall with a negative predicted R², so it is never used predictively. The quadratic "
            "term in elution buffer pH is the one term to reach alpha; the report declines to "
            "treat it as demonstrated but carries it conservatively into the PAR analysis, where "
            "it stops the NOR-propagated range short and caps the design space in that parameter.",
            "DesignSpace.definition therefore records a CAPPED region, not the whole characterized "
            "region. The previous annex asserted the opposite; the re-authored report contradicts "
            "it, so the record was corrected rather than re-anchored.",
            "ProcessParameter.PAR carries the at-set-point proven acceptable range (which equals "
            "the characterization range for every parameter here). The NOR-propagated range, "
            "which is narrower for elution buffer pH, is on the ProvenAcceptableRange records.",
            "Process-capability (Cpk) values have no dedicated field; reported as report_sections statements.",
            "rhetorical_spans are verbatim report prose; the leached-Protein-A cluster (claim + "
            "statistical justifications + the bounded_conclusion that lets the measured maximum "
            "bound the attribute) is the report's central argument; PCR-005 carries no weak_claims, "
            "so no span competes with a labeled negative.",
        ],
        inventory=pa_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=pa_studies(doc, f, report=True),
        design_spaces=pa_design_spaces(doc, f),
        proven_acceptable_ranges=pa_proven_acceptable_ranges(doc, f),
        report_sections=pa_report_sections(doc, f, report=True),
        assertions=pa_assertions(doc, f, report=True), concepts=pa_concepts(),
        rhetorical_spans=pa_rhetorical_spans(doc, f))


# =========================================================================== #
# Low-pH Viral Inactivation (Step 6) — PCP-006 / PCR-006.                       #
# --------------------------------------------------------------------------- #
# Additive, self-contained builders for the viral-inactivation DoE pair, fitted #
# to the RE-AUTHORED documents. The step sets the (cumulative) XMuLV clearance   #
# CQA and adds to aggregate and to acidic variants; the DoE is a three-factor    #
# full-factorial screen + face-centred CCD in inactivation pH / hold time /      #
# temperature, and pH is the only CPP of the step.                               #
#                                                                               #
# What the re-authored report concludes — the annex is fitted to THIS, and the   #
# previous annex asserted the opposite of the first item:                        #
#   * The worst characterized corner (highest pH, shortest hold, lowest          #
#     temperature) FAILS. The fitted model predicts below the back-calculated    #
#     step floor and executed runs measured below it. The corner is excluded     #
#     from the operating region, and the report refuses to argue the shortfall   #
#     away as noise ("the same argument would prevent the corner from being      #
#     declared acceptable"). It is a demonstrated failure, not an absence of     #
#     assurance.                                                                 #
#   * Exactly one proven acceptable range is narrower than its characterization  #
#     range: inactivation pH against the log reduction factor, under co-variation #
#     of the other two parameters inside their normal operating ranges.          #
#   * The step claims no parvovirus (MVM) clearance and no host cell protein     #
#     clearance; both are explicit non-claims.                                   #
#   * The report does NOT present the lower pH edge as an inherited, undemonstrat- #
#     ed bound, so the record that said so was dropped rather than re-anchored.  #
# PCR-006 carries no weak claim. PCP-006 carries WC-006-01 (§4.1, missing        #
# citation): no assertion and no rhetorical span here anchors on that sentence.  #
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
VIPARAM_CLASS = {r["parameter"]: r["classification"] for r in VIPARAM_ROWS}
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


# Both documents render their tables through ``_pcpkg.show`` (``df.to_markdown`` with the
# automatic per-column float formats), so rebuilding a row from the same DataFrame reproduces
# the rendered row verbatim. A per-record quote can then span the whole relation — the
# parameter with its set-point, ranges and (in the report) its classification; the attribute
# with its acceptance criterion and criticality; the proven acceptable range with the two
# analyses that produced it — instead of a caption every record of the table would share.
VI_TAB = {                                   # kind -> (table id, caption as rendered)
    "plan_params": ("PCP-006_tab_params",
                    "Parameters, ranges and study type for the low-pH hold."),
    "report_params": ("PCR-006_tab_params",
                      "Parameters of the low-pH viral inactivation step, with set-points, normal "
                      "operating ranges, characterization ranges and final classification."),
    "plan_cqa": ("PCP-006_tab_cqas", "Quality attributes governed by the low-pH hold."),
    "report_cqa": ("PCR-006_tab_cqa",
                   "Quality attributes governed by the low-pH viral inactivation step, with "
                   "acceptance criteria and criticality."),
    "acc": ("PCP-006_tab_acc", "Acceptance criteria for the measured responses."),
    "par": ("PCR-006_tab_par",
            "Proven acceptable ranges by attribute and parameter, with the characterization range "
            "for comparison."),
    "cap": ("PCR-006_tab_cap",
            "Commercial-scale capability for the attributes governed by this step."),
}
_VI_ROWS: dict = {}


def _vi_rows(kind):
    """Rendered rows of a table one of the two documents renders, keyed for lookup.

    ``plan_params`` / ``report_params`` are keyed by parameter name, ``cqa`` and ``cap`` by
    CQA key, ``acc`` by the quality-attribute name the acceptance row names, ``par`` by
    ``(CQA, parameter)``.
    """
    if not _VI_ROWS:
        import doe_report as D
        pp, rp = P.plan_params(VIUO), P.report_params(VIUO)
        cq, acc = P.cqas_by_keys(VI_CQA_KEYS), D.acceptance_table(VIUO)
        cap = P.cap_for(VI_CQA_KEYS)
        cap_keys = P.cap[P.cap.key.isin(VI_CQA_KEYS)]["key"].tolist()
        par = D.par_table(VIUO)
        _VI_ROWS.update(
            plan_params=row_quotes(pp, pp["Parameter"], P._auto_floatfmt(pp)),
            report_params=row_quotes(rp, rp["Parameter"], P._auto_floatfmt(rp)),
            cqa=row_quotes(cq, VI_CQA_KEYS, P._auto_floatfmt(cq)),
            acc=row_quotes(acc, acc["Quality attribute"], P._auto_floatfmt(acc)),
            cap=row_quotes(cap, cap_keys, P._auto_floatfmt(cap)),
            par=row_quotes(par, zip(par["CQA"], par["Parameter"]), P._auto_floatfmt(par)),
        )
    return _VI_ROWS[kind]


# Per-attribute grounded fragment from the report's "Quality attributes in scope" (§2.2). Each
# names the attribute and what the step does to it; the acceptance criterion and the
# criticality are anchored on the rendered @tbl-cqa row instead.
VI_CQA_QUOTE = {
    "lrv_xmulv": "XMuLV clearance is the attribute this step sets.",
    "aggregates_hmw": ("It is formed upstream, added to here, and polished downstream, so this "
                       "step’s obligation is to bound its own increment."),
    "acidic_variants": ("Acidic charge variants are of very low criticality, and the attribute is "
                        "carried in scope because the hold adds to the level formed upstream and "
                        "that increment has to be bounded."),
}

# Per-parameter grounded fragment from the report's "Parameter classification" (§9). The
# classification itself is carried by the rendered @tbl-params row; these spans carry the
# reasoning the report gives for it.
VI_CLASS_QUOTE = {
    "Inactivation pH": ("Inactivation pH is a critical process parameter. It carries the largest "
                        "effect on the attribute this step sets, its control band is narrow "
                        "relative to the characterized range, and it is the parameter that defines "
                        "the excluded corner of the design space."),
    "Hold time": ("Hold time is a well-controlled critical process parameter. It has a significant "
                  "effect on all three responses, and it is the only parameter that moves clearance "
                  "and product quality in opposite directions."),
    # stops before the inline effect estimate
    "Temperature": ("Temperature is a well-controlled critical process parameter. Its effect on "
                    "clearance is significant but is the smallest of the three"),
    "A-Mab concentration": ("A-Mab concentration is a general process parameter. The univariate "
                            "assessment covered the full range over which Protein A eluate is "
                            "delivered, and no effect on a quality attribute governed by this step "
                            "was demonstrated"),
}

# The plan ranks the parameters in §4.3. One sentence carries all three multivariate
# parameters and names the mechanism (the inactivation rate) each is ranked on.
VI_PLAN_RANK_QUOTE = ("Inactivation pH, hold time and temperature all enter the inactivation rate, "
                      "they act on the product at the same time, and there is no prior basis for "
                      "assuming that their effects stay additive across the full width of the "
                      "characterization ranges.")

# Per-method grounded fragment from each document's "Analytical methods" section.
VIMETHOD_QUOTE = {
    False: {  # PCP-006 §5.3
        "AMV-3017": ("Enveloped-virus inactivation is measured as the XMuLV log reduction factor by "
                     "infectivity titration (AMV-3017)"),
        "AMV-3011": ("Aggregate content is measured by size exclusion chromatography (SEC-HPLC, "
                     "AMV-3011) and reported as the percentage of high molecular weight species."),
        "AMV-3013": ("Acidic charge variants are measured by imaged capillary isoelectric focusing "
                     "(icIEF, AMV-3013) and reported as the percentage area of the acidic region."),
    },
    True: {  # PCR-006 §3.3
        "AMV-3017": "XMuLV infectivity was determined by TCID50 titration under AMV-3017.",
        "AMV-3011": ("Pool aggregate was determined by SEC-HPLC under AMV-3011 and reported as a "
                     "percentage of high molecular weight species."),
        "AMV-3013": ("Acidic charge variants were determined by icIEF under AMV-3013 and reported "
                     "as a percentage of the total charge variant profile."),
    },
}


def _vi_cqa_row(key):
    return P.cqa_reg[P.cqa_reg.key == key].iloc[0].to_dict()


def vi_step(doc_id, file_name, sec, report):
    if report:
        src = ref(doc_id, file_name, sec, "Executive summary",
                  "The Protein A eluate is titrated to a low pH, held for a defined time at "
                  "controlled temperature, and neutralised before cation exchange chromatography "
                  "(Step 7).")
    else:
        src = ref(doc_id, file_name, sec, "Purpose and scope",
                  "It receives the Protein A eluate, which is already acidic, titrates it to the "
                  "target pH, holds it under mixing for a defined time at a controlled "
                  "temperature, and neutralises it for the cation exchange step that follows")
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
    """Both documents separate two small-scale models, and the annex follows them.

    The hold itself is run on a scale-down model of the commercial vessel; virus can only be
    introduced at small scale, so clearance is measured on a *separate* spiking model. The
    previous annex carried one record for both, which is why the spiking model is added here.
    """
    qual_sec = "Scale-down model and its qualification"
    sdm = S.Equipment(
        equipment_id="equip:vi_sdm", equipment_name="scale-down inactivation model",
        equipment_type="viral inactivation (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec, qual_sec,
                               "The scale-down model is a jacketed, mixed vessel operated with the "
                               "same pH, temperature and hold profile as the commercial step."
                               if report
                               else "The studies are executed on a scale-down model of the "
                                    "commercial hold vessel, qualified under SOP-1001 before the "
                                    "first characterization run.")],
        metadata=meta())
    spike = S.Equipment(
        equipment_id="equip:vi_spike_model", equipment_name="small-scale virus spiking model",
        equipment_type="viral clearance (spiking model)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec, qual_sec,
                               "Virus can only be introduced at small scale, so the spiking model "
                               "must also be shown to hold the feed matrix, the spike volume and "
                               "the neutralisation step within the limits under which the "
                               "clearance is claimed" if report
                               else "Virus clearance is measured on a separate small-scale spiking "
                                    "model, which is what a clearance claim requires")],
        metadata=meta())
    if report:
        return [sdm, spike]
    return [
        S.Equipment(equipment_id="equip:vi_vessel",
                    equipment_name="commercial-scale low-pH inactivation vessel",
                    equipment_type="inactivation vessel", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec, qual_sec,
                                           "The scale-dependent variables are vessel geometry, "
                                           "mixing time, titration rate and the ratio of surface "
                                           "area to volume, and they are set so that the titration "
                                           "and neutralisation profiles match the commercial "
                                           "records.")],
                    metadata=meta()),
        sdm, spike,
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
    """Every parameter anchors on its own rendered row of @tbl-params in its own document.

    The plan row carries the set-point, both ranges and the study type; the report row carries
    the same plus the final classification, which is what the ``parameter_type`` of the report
    record asserts. The report records previously shared the table caption, so one span stood
    in for four parameters and named none of them.
    """
    rats = {"CPP": "Largest effect on the attribute the step sets, a control band narrow relative "
                   "to the characterized range, and the parameter that defines the corner excluded "
                   "from the design space. An excursion in the unfavourable direction costs "
                   "clearance rather than product quality.",
            "WC-CPP": "Significant effect on a critical quality attribute, but held well inside "
                      "the range that keeps every attribute in acceptance — hold time by a timer "
                      "against the control system clock, temperature by a jacket — and the whole "
                      "characterized range is proven acceptable for every attribute.",
            "GPP": "No effect on any quality attribute governed by the step was demonstrated over "
                   "the full range in which the Protein A eluate is delivered, so the whole "
                   "delivered range is proven acceptable and no control beyond routine monitoring "
                   "of the eluate is required."}
    rows = _vi_rows("report_params" if classified else "plan_params")
    tab_id, caption = VI_TAB["report_params" if classified else "plan_params"]
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
                                   rows[name], table_title=caption, table_id=tab_id)],
            metadata=meta()))
    return out


def vi_cqas(doc_id, file_name, sec, report):
    # Both documents render the same three-row attribute table from ``cqas_by_keys``, so each
    # attribute anchors on its own rendered row: the row carries the acceptance criterion, the
    # criticality and the Tool #1 score this record asserts.
    rows = _vi_rows("cqa")
    tab_id, caption = VI_TAB["report_cqa" if report else "plan_cqa"]
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
                                   rows[key], table_title=caption, table_id=tab_id)],
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
                                   "A full factorial was chosen over a fraction because the "
                                   "factors are few enough that every two-factor interaction (AB, "
                                   "AC and BC) can be estimated independently of the main effects."
                                   if report
                                   else "A full factorial estimates all three main effects and all "
                                        "three two-factor interactions without aliasing, which a "
                                        "fractional design in three factors could not do")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vi_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=VIUO_NAME,
            factors=VI_MULTIVARIATE,
            responses=["xmulv_lrf", "aggregate_out_pct", "acidic_variants"],
            n_runs=n_rsm, n_center_points=P.doe_centre_points(VIUO, "rsm"), scale_down_model="scale-down inactivation model",
            associated_parameters=[VIPARAM_CONCEPT[f] for f in VI_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "The axial points sit on the faces of the cube (the "
                                   "face-centred convention), so the design stays inside the "
                                   "characterized ranges and does not require any factor to be set "
                                   "beyond an edge that has been justified." if report
                                   else "The response-surface study is a face-centred central "
                                        "composite design (CCD) in the same three factors.")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vi_sdm_qual", study_type="scale_down_qualification",
            unit_operation=VIUO_NAME, scale_down_model="scale-down inactivation model",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "Qualification followed SOP-1001, under which the model was "
                                   "operated at the target conditions and its input and output "
                                   "attributes were compared with the commercial-scale batch data"
                                   if report
                                   else "Qualification compares replicate runs at the set-point "
                                        "against the commercial-scale record for the same "
                                        "operation.")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vi_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=VIUO_NAME,
            factors=VI_UNIVARIATE,
            responses=["xmulv_lrf", "aggregate_out_pct", "acidic_variants"],
            associated_parameters=[VIPARAM_CONCEPT[f] for f in VI_UNIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Univariate assessment",
                                   "A-Mab concentration was assessed one factor at a time across "
                                   "its full range with the kinetic factors at their set-points."
                                   if report
                                   else "Each condition is spiked and assayed as a full run, so "
                                        "the univariate results are directly comparable with the "
                                        "centre points of the multivariate designs.")],
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

    def add(subj, pred, obj, text, sec, quote, table=None):
        n[0] += 1
        tab_id, caption = VI_TAB[table] if table else (None, None)
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote,
                                   table_title=caption, table_id=tab_id)], metadata=meta()))

    # Every step->parameter and step->attribute relation is anchored on the rendered row that
    # carries both ends of it. In the report the parameter row also carries the classification.
    param_sec = "Factors, ranges and the knowledge space" if report else "Factors, ranges and study type"
    param_tab = "report_params" if report else "plan_params"
    param_rows = _vi_rows(param_tab)
    for name, cid in VIPARAM_CONCEPT.items():
        add("step:viral_inactivation", "step_has_parameter", cid,
            f"{VIUO_NAME} has process parameter {name}"
            + (f", classified {VIPARAM_CLASS[name]}." if report else "."),
            param_sec, param_rows[name], table=param_tab)
    cqa_tab = "report_cqa" if report else "plan_cqa"
    cqa_rows = _vi_rows("cqa")
    for key in VI_CQA_KEYS:
        if key == "lrv_xmulv":
            txt = f"{VIUO_NAME} sets the cumulative XMuLV clearance."
        elif report:
            txt = (f"{VIUO_NAME} adds to {VIATTR_NAME[key]} during the low-pH hold; the attribute "
                   f"is formed upstream and is not set here.")
        else:
            # The plan states the increment and the obligation to bound it; only the report
            # states upstream formation for both attributes, so the plan record stops short.
            txt = (f"{VIUO_NAME} can add to {VIATTR_NAME[key]} during the low-pH hold, and the "
                   f"study is designed to bound the increment.")
        add("step:viral_inactivation", "step_has_quality_attribute", VIATTR_CONCEPT[key], txt,
            "Quality attributes in scope", cqa_rows[key], table=cqa_tab)
    # The step's two explicit non-claims (no MVM, no HCP clearance) have no predicate in the
    # upstream vocabulary; they are carried as report_sections statements instead.
    # attribute -> method (plan only)
    if not report:
        for key in VI_CQA_METHOD:
            add(VIATTR_CONCEPT[key], "attribute_measured_by_method", f"method:{VI_CQA_METHOD[key]}",
                f"{VIATTR_NAME[key]} is measured by {VI_CQA_METHOD[key]}.", "Analytical methods",
                VIMETHOD_QUOTE[False][VI_CQA_METHOD[key]])
    # Acceptance criterion for the viral-clearance CQA: cumulative over the credited steps, so
    # what binds THIS step is the back-calculated contribution. The plan anchors on the rendered
    # acceptance row, which carries the response, the criterion and the basis in one span.
    xr = _vi_cqa_row("lrv_xmulv")
    add("attr:lrv_xmulv", "attribute_has_acceptance_criterion", "lit:lrv_xmulv_acc",
        f"Cumulative XMuLV clearance acceptance: {xr['acc_low']:g}–{xr['acc_high']:g} {xr['unit']}; "
        f"the criterion applied to this step is the back-calculated step contribution.",
        "Proven acceptable ranges" if report else "Acceptance and decision criteria",
        "For XMuLV it is the contribution this step must make to the cumulative claim, which is "
        "the cumulative requirement less the clearance credited to the other steps" if report
        else _vi_rows("acc")[xr["cqa"]], table=None if report else "acc")
    # parameter -> attribute impacts / non-impacts
    if report:
        add("param:vi_ph", "parameter_impacts_attribute", "attr:lrv_xmulv",
            "Inactivation pH carries the largest effect on the attribute the step sets and is the "
            "parameter that defines the corner excluded from the design space, so it is "
            "classified CPP.",
            "Parameter classification", VI_CLASS_QUOTE["Inactivation pH"])
        for name in VI_WCCPP:
            add(VIPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:lrv_xmulv",
                f"{name} has a significant effect on the log reduction factor and is classified "
                f"WC-CPP.", "Parameter classification", VI_CLASS_QUOTE[name])
        for name in VI_WCCPP:
            add(VIPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:aggregates_hmw",
                f"{name} raises the pool aggregate level; pH does not.", "Screening: factor effects",
                "The pool aggregate is driven by hold time and temperature, and not by pH.")
        add("param:vi_hold_time", "parameter_impacts_attribute", "attr:acidic_variants",
            "Acidic charge variants rise with hold time and with nothing else in this step. (The "
            "response carries no replicate variation, so its fit statistics are uninformative; "
            "that is stated separately in the report summary.)",
            "Response-surface models",
            "The physical content of that row is simply that the acidic charge variant level rises "
            "with hold time and with nothing else in this step.")
        add("param:vi_ph", "parameter_does_not_significantly_impact_attribute", "attr:aggregates_hmw",
            "Inactivation pH had no demonstrated effect on the pool aggregate across the range "
            "studied; the null result is retained in the knowledge space.",
            "Screening: factor effects",
            "pH remains in the knowledge space as a factor with no demonstrated effect on "
            "aggregate across the range studied.")
        add("param:vi_protein_conc", "parameter_does_not_significantly_impact_attribute", "attr:lrv_xmulv",
            "A-Mab concentration is a GPP: the univariate assessment covered the full delivered "
            "range and demonstrated no effect on any attribute the step governs.",
            "Parameter classification", VI_CLASS_QUOTE["A-Mab concentration"])
    else:
        for name in VI_MULTIVARIATE:
            add(VIPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:lrv_xmulv",
                f"{name} was ranked for multivariate study because it enters the inactivation rate "
                f"and its effect cannot be assumed additive with the other two.",
                "Risk-based prioritization of parameters", VI_PLAN_RANK_QUOTE)
        add("param:vi_protein_conc", "parameter_does_not_significantly_impact_attribute", "attr:lrv_xmulv",
            "A-Mab concentration is not expected to affect the inactivation kinetics, which is why "
            "it is assessed one factor at a time.",
            "Univariate assessment",
            "The rate of inactivation at low pH is set by the three multivariate factors (pH, "
            "temperature, duration of the exposure), and it is not expected to depend materially "
            "on the concentration of the antibody in which the virus is suspended.")
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def vi_report_sections(doc_id, file_name, report):
    from annex_contract.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        # §1 states the scope of the study as counts taken from the parameter register and the
        # response set, so the statement and the span it is anchored on are built from those.
        import doe_report as D
        n_mv = sum(1 for r in VIPARAM_ROWS if r["study"] == "multivariate")
        n_uv = len(VIPARAM_ROWS) - n_mv
        n_resp = len(D.responses(VIUO))
        scope_quote = (f"The plan covers the {len(VIPARAM_ROWS)} process parameters of the low-pH "
                       f"hold and the {n_resp} responses measured across them. Of those "
                       f"parameters, {n_mv} enter a multivariate design and {n_uv} is assessed one "
                       f"factor at a time")
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-006 defines the process characterization study for the A-Mab low-pH viral "
                  "inactivation step (Step 6) and fixes its acceptance and decision criteria "
                  "before any data exist.",
               "Purpose and scope",
               "This plan defines the studies that will characterize the step, and it fixes the "
               "acceptance and decision criteria before any data are generated."),
            st(2, f"The step has {len(VIPARAM_ROWS)} process parameters in scope; inactivation "
                  f"pH, hold time and temperature are the multivariate factors and A-Mab "
                  f"concentration is univariate.",
               "Purpose and scope", scope_quote),
            st(3, "The study uses a full-factorial screen followed by a face-centred "
                  "central-composite design on a qualified scale-down hold model.",
               "Response-surface design",
               "The response-surface study is a face-centred central composite design (CCD) in the "
               "same three factors."),
            st(4, "No host cell protein clearance is claimed for the step: precipitation at low pH "
                  "is removed by the depth filtration that follows neutralisation, but the extent "
                  "is not predictable.",
               "Purpose and scope",
               "the extent of that clearance is not predictable and no HCP claim will be made for "
               "this step"),
            st(5, "The enveloped-virus criterion for this step is a floor back-calculated from the "
                  "cumulative requirement, not the cumulative requirement itself, and the step is "
                  "expected to deliver more than the floor.",
               "Acceptance and decision criteria",
               "That figure is a floor and not a target. The step is expected to deliver more than "
               "the floor, and the margin above it is what allows the cumulative claim to survive "
               "a weak result at one of the three contributing steps."),
            st(6, "Proven acceptable ranges will be reported from two analyses, and the one that "
                  "propagates the other parameters across their normal operating ranges is the "
                  "robustness criterion the control strategy uses.",
               "Proven acceptable ranges (planned analysis)",
               "so this analysis is a robustness criterion, it is expected to give the narrower of "
               "the two ranges, and it is the one the control strategy uses"),
            st(7, "The criteria are applied as a set: the study passes only when the scale-down "
                  "model is qualified, every response model is adequate, and the design space "
                  "contains the normal operating ranges.",
               "Acceptance and decision criteria",
               "The study passes when three conditions hold together: the scale-down model is "
               "qualified, every response model is adequate, and the design space defined from "
               "those models contains the normal operating ranges of the parameters."),
            st(8, "The low edge of the pH range is a platform boundary: earlier work placed "
                  "antibody precipitation just below it, so the range was not extended further.",
               "Unit-operation description and prior knowledge",
               "Earlier univariate work on the platform found that antibody precipitation can "
               "occur just below the low edge of that range, so it was not extended further."),
            st(9, "The worst case for viral safety is named before execution as the corner at the "
                  "highest pH, the shortest hold and the lowest temperature, and it is to be "
                  "reported whether or not it passes.",
               "Acceptance and decision criteria",
               "For viral safety the worst case is the corner at the highest pH, the shortest hold "
               "and the lowest temperature."),
            st(10, "Parameter classification is an output of the study, so the plan states the "
                   "decision rule only and reports no classification.",
                "Acceptance and decision criteria",
                "The classification is an output of the study and it is reported in PCR-006, so "
                "this plan states the decision rule and stops there."),
            st(11, "A failed criterion is not handled by widening the design space; the range is "
                   "narrowed or the set-point moved, and the change is justified against the same "
                   "models.",
                "Acceptance and decision criteria",
                "A failed criterion is not handled by widening the design space."),
            st(12, "The screening model is close to saturated and is used for identification only; "
                   "the response-surface model is the predictive model behind the design space and "
                   "the proven acceptable ranges.",
                "Statistical methods",
                "It is used to identify which factors and which interactions are active, and it is "
                "not used as a predictive model."),
        ])]
    # ------------------------------------------------------------------ #
    # PCR-006. Statement 4 is the record that mattered most in this pass: the previous annex
    # asserted the worst corner was "an absence of assurance and not a demonstrated failure".
    # The re-authored report says the opposite — the corner fails in the model AND failed in
    # the executed data — so the statement is corrected rather than re-anchored.
    # ------------------------------------------------------------------ #
    import doe_report as D
    cpk = float(P.cap.set_index("key").loc["lrv_xmulv", "Cpk"])
    par_hi = D.par_nor_propagated(VIUO, "xmulv_lrf", "ph")["par_nat"][1]
    vc = P.csv("viral_clearance.csv").set_index("step")
    vi_mvm = float(vc.loc[D.VIRAL_STEP_ROW[VIUO], "MVM"])
    n_steps = int((vc.index != "Cumulative").sum())
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Inactivation pH is classified as a critical process parameter; hold time and "
              "temperature are well-controlled critical process parameters and A-Mab "
              "concentration is a general process parameter.",
           "Executive summary", "Inactivation pH is classified as a critical process parameter."),
        st(2, "The screening design identifies the active factors and the response-surface model "
              "is the predictive model behind the operating region.",
           "Executive summary",
           "The screening design identifies the active factors. The response-surface model is the "
           "predictive model and the basis of the operating region."),
        st(3, "Inactivation pH is the dominant factor on the XMuLV log reduction factor, and "
              "clearance falls as pH rises.",
           "Screening: factor effects",
           "pH is the dominant factor on the log reduction factor."),
        st(4, "The corner combining the highest pH with the shortest hold and the lowest "
              "temperature fails: the fitted model predicts below the required step contribution "
              "and executed runs measured below it. The corner is excluded from the operating "
              "region, and the report declines to argue the shortfall away as noise.",
           "Design space", "The corner fails in the model, and it failed in the executed data."),
        st(5, f"Exactly one proven acceptable range is narrower than its characterization range — "
              f"inactivation pH against the log reduction factor, which narrows to an upper edge "
              f"of {par_hi:.2f} under co-variation of the other parameters within their normal "
              f"operating ranges.",
           "Proven acceptable ranges",
           f"The pH range narrows under the second analysis, from the full characterization range "
           f"to an upper edge of {par_hi:.2f}."),
        st(6, f"Cumulative XMuLV clearance is the tightest of the three capabilities the step "
              f"governs, at a one-sided Cpk of {cpk:.2f}.",
           "Process capability and robustness",
           f"XMuLV clearance is the tightest of them by a wide margin, at a one-sided Cpk of "
           f"{cpk:.2f}."),
        st(7, f"The low-pH hold supplies the largest single contribution to the cumulative XMuLV "
              f"claim of the {n_steps} credited steps.",
           "Executive summary", f"which is the largest single contribution of the {n_steps} "
                                f"credited steps"),
        st(8, f"The step claims no clearance of non-enveloped virus; its MVM contribution is "
              f"{vi_mvm:.1f} log₁₀, and no host cell protein clearance is claimed either.",
           "Executive summary",
           f"No clearance of non-enveloped virus is claimed for this step, and its MVM "
           f"contribution is reported as {vi_mvm:.1f} log₁₀"),
        st(9, "The acidic charge variant response returned no replicate variation in either "
              "design, so its pure error is zero, lack of fit cannot be tested and the study "
              "bounds the increment without estimating its variability.",
           "Discussion",
           "The acidic charge variant response returned no replicate variation in either design, "
           "so the study bounds the magnitude of the deamidation increment but provides no useful "
           "estimate of its variability."),
        st(10, "The response-surface model for the log reduction factor has a low predicted "
               "coefficient of determination because the infectivity assay carries much of the "
               "observed variance, so it is a model of mean behaviour and not a batch-level "
               "assurance statement.",
            "Discussion",
            "The response-surface model for the log reduction factor has a low predicted "
            "coefficient of determination, because the infectivity assay contributes a large part "
            "of the observed variance, and it should be read as a model of mean behaviour and not "
            "as a batch-level assurance statement."),
        st(11, "No interaction was significant in either design — the three kinetic factors act "
               "additively over the ranges studied — so every classification rests on a main "
               "effect demonstrated in its own right.",
            "Parameter classification",
            "The absence of any significant interaction in either design means that no parameter "
            "is classified on the strength of a combination effect."),
        st(12, "Two deviations were recorded, both dispositioned as retained, and neither changed "
               "a fitted effect, a parameter classification or the operating region.",
            "Executive summary",
            "Both were investigated and dispositioned as retained, and neither altered a parameter "
            "classification or the reported operating region."),
    ])]


def vi_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:viral_inactivation", unit_operation=VIUO_NAME,
        parameters=["param:vi_ph", "param:vi_hold_time", "param:vi_temperature"],
        quality_attributes_constrained=["attr:lrv_xmulv", "attr:aggregates_hmw"],
        definition="The characterized cube of inactivation pH, hold time and temperature, less the "
                   "corner that combines the highest pH with the shortest hold and the lowest "
                   "temperature. Inside the region the response-surface model predicts a step log "
                   "reduction factor at or above the back-calculated step contribution, and both "
                   "product quality constraints are inactive over the whole cube, so the region is "
                   "set by the clearance constraint alone and its principal plane is pH against "
                   "hold time. The excluded corner is a demonstrated failure and not a margin "
                   "call: the fitted model predicts below the floor there and executed runs "
                   "measured below it. The predicted shortfall is smaller than the model's "
                   "residual standard error, and the report declines to use that as a defence, "
                   "because the same argument would prevent the corner being declared acceptable.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "The design space is therefore the characterized cube less that "
                               "corner, and its principal plane is pH against hold time")],
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


def vi_proven_acceptable_ranges(doc_id, file_name):
    """One ProvenAcceptableRange per governed CQA x response-surface parameter, from the
    same DoE engine (``doe_report.par_table``) that renders @tbl-par in §7 of the report.

    Each record anchors on ITS OWN rendered row, which carries the attribute, the parameter,
    the characterization range and both proven acceptable ranges in one span. The two
    per-attribute prose fragments this replaced each stood in for several records and named no
    parameter; both are also dead after the re-authoring.

    Aggregate and acidic variants are judged against the drug substance specification; the
    viral-clearance CQA is judged against the back-calculated step floor. Only one row is
    narrower than its characterization range — inactivation pH against the log reduction
    factor, under co-variation of the other two parameters inside their normal operating
    ranges — and the report states the residual margin above the pH control band.
    """
    import doe_report as D
    par = D.par_table(VIUO)
    rows = _vi_rows("par")
    tab_id, caption = VI_TAB["par"]
    out = []
    for i, r in enumerate(par.to_dict("records"), 1):
        cqa, param, unit = r["CQA"], r["Parameter"], (r["Unit"] or "")
        char = f"{r['Char. range']} {unit}".strip()
        viral = "LRF" in cqa
        narrower = str(r["PAR (NOR)"]) != str(r["Char. range"])
        basis = (
            "Step-level required log reduction, back-calculated from the cumulative XMuLV "
            "requirement minus the clearance credited to anion exchange and small-virus retentive "
            "filtration (modular viral-safety claim under ICH Q5A(R2))."
            if viral else
            "Drug-substance specification for the attribute, applied at the outlet of the step.")
        if narrower:
            basis += (" This is the only entry whose NOR-propagated range stops short of the "
                      "characterization range: the 95 % predictive interval reaches the required "
                      "step contribution before the top of the pH range when hold time and "
                      "temperature co-vary inside their control bands.")
        out.append(S.ProvenAcceptableRange(
            par_id=f"{doc_id}-PAR{i:02d}", unit_operation=VIUO_NAME,
            quality_attribute=cqa, parameter=param,
            characterization_range=char,
            par_at_setpoint=f"{r['PAR (set-point)']} {unit}".strip(),
            par_nor_propagated=f"{r['PAR (NOR)']} {unit}".strip(),
            acceptance_basis=basis,
            source_references=[ref(doc_id, file_name, f"{doc_id}_sec_par", VI_PAR_SEC,
                                   rows[(cqa, param)], table_title=caption, table_id=tab_id)],
            metadata=meta()))
    return out


# Argument-structure spans over the RE-AUTHORED PCR-006. Every span of the previous layer
# quoted prose that no longer exists, so the layer was re-curated wholesale as part of this
# annex rebuild — not deferred to a later annotation pass. Each quote is a verbatim,
# plain-prose fragment of the RENDERED report (no inline expressions, no table cells), and
# every ``supported_by`` edge points at the span that actually carries the evidence for the
# claim. Tuple fields:
# (suffix, role, section, quote, supported_by-suffixes, restates-suffix, bounds-suffix).
#
# Two edges are worth reading: the exclusion of the worst corner (R03) is supported by the
# executed-data finding (R30) and by the report's refusal to treat a shortfall inside the noise
# as a defence (R31); and "every classification rests on a main effect demonstrated in its own
# right" (R39) is supported by the screening finding of no significant interaction (R13).
VI_RHET_SPANS = [
    ("R00", "problem_statement", "Product and unit operation",
     "The step is a balance between these two effects, and characterizing it means bounding both.",
     [], None, None),
    ("R01", "claim", "Executive summary",
     "Inactivation pH is classified as a critical process parameter.", ["R38"], None, None),
    ("R02", "claim", "Executive summary",
     "The screening design identifies the active factors. The response-surface model is the "
     "predictive model and the basis of the operating region.", [], None, None),
    ("R03", "claim", "Executive summary",
     "That corner is excluded from the operating region.", ["R30", "R31"], None, None),
    ("R04", "bounded_conclusion", "Executive summary",
     "The step assures a defined enveloped-virus inactivation increment and a bounded product "
     "quality cost. It does not by itself assure the viral safety of the drug substance.",
     [], None, None),
    ("R05", "deferral", "Executive summary",
     "This report rolls up into PCMR-001.", [], None, None),
    ("R06", "bounded_conclusion", "Regulatory and scientific basis",
     "Clearance data are generated at small scale with a deliberately spiked feed, because virus "
     "cannot be introduced into a manufacturing process.", [], None, None),
    ("R07", "claim", "Platform and prior-product knowledge",
     "Prior knowledge sets a clear mechanistic expectation, and the study was designed to test it.",
     [], None, None),
    ("R08", "bounded_conclusion", "Platform and prior-product knowledge",
     "If the data contradict any of these expectations, the platform justification for the step "
     "would have to be re-examined.", [], None, "R07"),
    ("R09", "justification", "Risk-based prioritization and parameter selection",
     "A range that only covers the control band cannot distinguish a robust parameter from an "
     "unstudied one, and it leaves no room for movement within the design space later in the "
     "lifecycle.", [], None, None),
    ("R10", "claim", "Centre-point performance and reproducibility",
     "The step is highly reproducible in the two product quality responses and considerably less "
     "so in the log reduction factor.", ["R11"], None, None),
    ("R11", "justification", "Centre-point performance and reproducibility",
     "A reported log reduction factor is the difference of two titrations, so the scatter seen "
     "between replicate holds is consistent with analytical variation alone.", [], None, None),
    ("R12", "hedge", "Centre-point performance and reproducibility",
     "it should be read as a property of how the attribute responds to this step, not as evidence "
     "of unusual analytical precision.", [], None, None),
    ("R13", "claim", "Screening: factor effects",
     "The screening study identified pH, hold time and temperature as active, and found no "
     "significant interaction between any pair of them.", ["R14"], None, None),
    ("R14", "justification", "Screening: factor effects",
     "All three effects have the direction prior knowledge predicted.", [], None, None),
    ("R15", "claim", "Screening: factor effects",
     "That null result matters to the design of the step, because it means the pH needed for "
     "inactivation can be chosen on viral clearance grounds alone, without trading it against "
     "aggregate", [], None, None),
    ("R16", "bounded_conclusion", "Screening: factor effects",
     "pH remains in the knowledge space as a factor with no demonstrated effect on aggregate "
     "across the range studied.", [], None, "R15"),
    ("R17", "bounded_conclusion", "Screening: factor effects",
     "The magnitudes above are estimated from a design with two levels per factor, so they "
     "describe a plane through the region and cannot represent curvature.", [], None, None),
    ("R18", "claim", "Response-surface models",
     "The response-surface study confirms the screening result, adds curvature in pH on the log "
     "reduction factor, and gives two adequate predictive models.", ["R23"], None, None),
    ("R19", "hedge", "Response-surface models",
     "The log reduction model is weaker and needs to be described carefully.", [], None, None),
    ("R20", "justification", "Response-surface models",
     "The gap between those two figures is the signature of a response whose replicate scatter is "
     "large relative to its systematic variation, which is what the centre-point analysis above "
     "shows for this assay.", [], None, None),
    ("R21", "bounded_conclusion", "Response-surface models",
     "The model is used to predict mean log reduction inside the characterized region. It is not "
     "used as an assurance statement about a single batch", ["R20"], None, "R18"),
    ("R22", "hedge", "Response-surface models",
     "it is treated here as a suggestion supported by one borderline term. It is not presented as "
     "an established feature of the surface.", [], None, None),
    ("R23", "justification", "Response-surface models",
     "so the quadratic form is adequate for the data and the unexplained variation is consistent "
     "with pure error", [], None, None),
    ("R24", "hedge", "Response-surface models",
     "The acidic charge variant model is reported for completeness and carries no statistical "
     "weight.", [], None, None),
    ("R25", "mechanistic_warrant", "Mechanistic interpretation",
     "A model in which pH, hold time and temperature act additively on a logarithmic measure of "
     "survival is what that mechanism predicts, and it is what the coefficients show.",
     [], None, None),
    ("R26", "mechanistic_warrant", "Mechanistic interpretation",
     "The likely reason is that the antibody is already below the pH of its acid-labile "
     "conformational transition even at the top of the range studied, so a further reduction in "
     "pH changes the exposure very little.", [], None, None),
    ("R27", "claim", "Mechanistic interpretation",
     "The surfaces have the shape the underlying chemistry predicts, and that agreement is part "
     "of the evidence for the step.", ["R25", "R26"], None, None),
    ("R28", "claim", "Mechanistic interpretation",
     "The practical consequence of these three mechanisms is that the step cannot be described by "
     "independent ranges on its parameters.", ["R25", "R26"], None, None),
    ("R29", "claim", "Design space",
     "The binding constraint is viral clearance.", [], None, None),
    ("R30", "justification", "Design space",
     "The corner fails in the model, and it failed in the executed data.", [], None, None),
    ("R31", "justification", "Design space",
     "A shortfall inside the noise cannot be argued away as noise, because the same argument would "
     "prevent the corner from being declared acceptable. The corner is excluded.", [], None, None),
    ("R32", "bounded_conclusion", "Design space",
     "It is a claim about mean predicted responses from a fitted model, so the reliability at the "
     "boundary of the region is lower than it is at the centre, and it should not be read as an "
     "assurance figure for an individual batch.", [], None, "R29"),
    ("R33", "bounded_conclusion", "Proven acceptable ranges",
     "The whole studied range of every parameter is proven acceptable for those two attributes, "
     "and it stays acceptable when the other two parameters move within their normal operating "
     "ranges.", [], None, None),
    ("R34", "claim", "Proven acceptable ranges",
     "These ranges and the design space answer different questions, and the two are not "
     "interchangeable.", [], None, None),
    ("R35", "bounded_conclusion", "Proven acceptable ranges",
     "Both statements are bounded by the characterization ranges and by the fitted model.",
     [], None, "R34"),
    ("R36", "cross_step_credit", "Process capability and robustness",
     "None of these figures belongs to this step alone, and the clearance figure least of all.",
     [], None, None),
    ("R37", "bounded_conclusion", "Process capability and robustness",
     "Two bounds apply, since the estimate assumes parameters inside their normal operating ranges "
     "and a qualified scale-down model, and it will be confirmed at commercial scale during "
     "Stage 2.", [], None, None),
    ("R38", "justification", "Parameter classification",
     "It is classified below pH because it is set by a timer against a controlled clock (the "
     "distributed control system record), its whole characterized range is proven acceptable for "
     "every attribute, and the risk of leaving the design space through hold time alone is very "
     "low.", [], None, None),
    ("R39", "claim", "Parameter classification",
     "Every classification above rests on a main effect demonstrated in its own right.",
     ["R13"], None, None),
    ("R40", "claim", "Contribution to the control strategy",
     "The step does not deliver viral safety on its own.", ["R41"], None, None),
    ("R41", "cross_step_credit", "Contribution to the control strategy",
     "it makes no contribution at all to the parvovirus claim, which rests on the anion exchange "
     "step (PCR-008) and the small-virus retentive filtration step (PCR-009)", [], None, None),
    ("R42", "deferral", "Contribution to the control strategy",
     "the cumulative claim is consolidated in PCMR-001", [], None, None),
    ("R43", "restatement", "Discussion",
     "The operating region follows directly from those relationships, and the only boundary that "
     "binds is the clearance requirement at the corner where the highest pH meets the shortest "
     "hold and the lowest temperature.", [], "R29", None),
    ("R44", "justification", "Discussion",
     "The mitigating evidence is that the corner requires all three factors to be at their least "
     "favourable edge at once, that the normal operating ranges are far from it", [], None, None),
    ("R45", "deviation_disposition", "Discussion",
     "The residual position is that the corner is excluded from the design space and the step is "
     "not operated there.", ["R44"], None, None),
    ("R46", "hedge", "Discussion",
     "Confidence in the scale-down model is high for the operating ranges and is necessarily "
     "qualified for the clearance claim.", [], None, None),
    ("R47", "bounded_conclusion", "Discussion",
     "The relationship between that preparation and an adventitious contaminant is an assumption "
     "of the method and not a result of this study", [], None, None),
    ("R48", "bounded_conclusion", "Discussion",
     "Three further limitations should be recorded.", [], None, None),
    ("R49", "problem_statement", "Deviations from the plan",
     "Neither was detected by an in-process control at the time it occurred.", [], None, None),
    ("R50", "deviation_disposition", "Deviations from the plan",
     "Each was investigated, its root cause was established, its impact on the reported results "
     "was assessed, and both were dispositioned as retained.", [], None, None),
    ("R51", "deviation_disposition", "DEV-006-01: hold-time record discrepancy",
     "The run was retained with the distributed control system value, and the fitted effects are "
     "unchanged.", [], None, None),
    ("R52", "justification", "DEV-006-02: infectivity assay cytotoxicity at low dilution",
     "A bias of that sign cannot create an apparent clearance that does not exist, and it cannot "
     "mask a failing corner, since it can only make a reported value too small.", [], None, None),
    ("R53", "deviation_disposition", "DEV-006-02: infectivity assay cytotoxicity at low dilution",
     "The affected results were retained and the analysis was not repeated.", ["R52"], None, None),
]


def vi_rhetorical_spans(doc_id, file_name):
    """Rhetorical / argument-structure spans over the PCR-006 report (report-only)."""
    out = []
    for suffix, role, sec, quote, sup, res, bnd in VI_RHET_SPANS:
        out.append(S.RhetoricalSpan(
            span_id=f"{doc_id}-{suffix}", section=sec, role=role,
            source_reference=ref(doc_id, file_name, f"{doc_id}_sec_rhet", sec,
                                 " ".join(quote.split())),
            supported_by=[f"{doc_id}-{s}" for s in sup],
            restates=(f"{doc_id}-{res}" if res else None),
            bounds=(f"{doc_id}-{bnd}" if bnd else None)))
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
        weak_claims=build_weak_claims(doc, f),
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "The XMuLV criterion for this step is a back-calculated step contribution (cumulative "
            "requirement minus the clearance credited to AEX and virus filtration) under the "
            "modular ICH Q5A(R2) approach. The plan states it as a floor and not a target.",
            "Proven acceptable ranges are to be reported from two analyses — the other parameters "
            "held at their set-points, and propagated across their normal operating ranges with a "
            "95 % predictive interval — and the propagated analysis is the robustness criterion "
            "the control strategy uses.",
            "The plan makes no host cell protein clearance claim for the step. Unlike the paired "
            "report it states no MVM non-claim, so the annex carries none.",
            "The Plan states classification is an OUTPUT; parameter_type left 'unclassified' here.",
            "PCP-006 carries one labeled weak claim (WC-006-01, §4.1, missing citation). No "
            "assertion and no report_sections statement in this annex anchors on that sentence.",
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
        weak_claims=build_weak_claims(doc, f),
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
            "The design space is the characterized cube LESS the corner at the highest pH, the "
            "shortest hold and the lowest temperature. That corner is a demonstrated failure — "
            "the fitted model predicts below the required step contribution and executed runs "
            "measured below it — and there is no field for an excluded sub-region, so it is "
            "carried in the DesignSpace definition and in a report_sections statement.",
            "The step contributes nothing to MVM clearance and claims no HCP clearance; both are "
            "stated as explicit non-claims and have no predicate in the upstream assertion "
            "vocabulary, so they are carried as report_sections statements.",
            "Acidic variants are a deterministic function of hold time in the seeded model (zero "
            "centre-point SD, exact fit, no pure error), so lack of fit cannot be tested and the "
            "report states that its fit statistics carry no information.",
            "Process-capability (Cpk) values have no dedicated field; reported as report_sections statements.",
            "proven_acceptable_ranges mirror @tbl-par (doe_report.par_table) and each anchors on "
            "its own rendered row; rhetorical_spans are verbatim report prose, re-curated with "
            "this annex after the report was re-authored; PCR-006 carries no weak_claims.",
        ],
        inventory=vi_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=vi_studies(doc, f, report=True),
        design_spaces=vi_design_spaces(doc, f),
        proven_acceptable_ranges=vi_proven_acceptable_ranges(doc, f),
        report_sections=vi_report_sections(doc, f, report=True),
        assertions=vi_assertions(doc, f, report=True), concepts=vi_concepts(),
        rhetorical_spans=vi_rhetorical_spans(doc, f))


# =========================================================================== #
# Cation Exchange Chromatography (Step 7) — PCP-007 / PCR-007.                  #
# --------------------------------------------------------------------------- #
# Additive, self-contained builders for the CEX polishing DoE pair, fitted to    #
# the RE-AUTHORED documents. The step sets NO CQA: it is the LAST step of the    #
# train at which aggregate is reduced, and a major clearance step for HCP, with  #
# further clearance of residual DNA and leached Protein A — all formed upstream. #
# The DoE is a four-factor full-factorial screen + face-centred CCD in load /    #
# wash-conductivity / elution-pH / stop-collect; flow is a univariate GPP. All    #
# four multivariate factors are WC-CPP; the step has no CPP and no KPP.           #
#                                                                               #
# What the re-authored documents say — the annex is fitted to THIS, and several  #
# records of the previous annex asserted something neither document supports:    #
#   * NOTHING is back-calculated at this step. Both documents state it outright  #
#     ("No back calculation is needed at this step"; "no step-level requirement   #
#     had to be back-calculated from a cumulative claim"). The old annex invented #
#     a "step-level ceiling back-calculated from the AEX clearance factor" and    #
#     judged pool HCP against it; that ceiling does not exist. Pool HCP is        #
#     measured against the DRUG SUBSTANCE specification, the set-point prediction #
#     breaches it, and the PAR table therefore returns no interval for any        #
#     parameter. The report states this plainly: "Measured against the drug        #
#     substance specification, this step has no proven acceptable range for host  #
#     cell protein."                                                              #
#   * The operating region is the whole characterized region ONLY as far as pool  #
#     aggregate is concerned; for pool HCP it is bounded by what AEX can clear,   #
#     and "no operating region can be declared here on the basis of the drug      #
#     substance host cell protein limit".                                         #
#   * The commercial-scale capability figures belong to the DRUG SUBSTANCE and    #
#     not to this step alone. Aggregate is the attribute this step "effectively   #
#     decides", because no later operation reduces it — which is weaker than the  #
#     old annex's "this capability belongs to the cation exchange step alone".    #
#   * The plan sets NO in-process limit on pool HCP and no second, step-level     #
#     criterion. The old annex asserted one in both documents.                     #
#   * The plan has no worst-case aggregate challenge; that record was dropped.    #
# Curvature: no quadratic term is significant for either impurity response. The   #
# yield model is direction-only. Neither document carries a weak claim.           #
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
# The attribute RA-001 records for each parameter, which is the scope the PLAN inherits and
# the relation its prioritization assertions carry. Conductivity is scored on host cell
# protein clearance alone — both documents say so, and the report finds no conductivity
# effect on pool aggregate in either design.
CX_RA_ATTRS = {
    "Protein load": ["aggregates_hmw", "hcp"],       # "Reduced aggregate and HCP clearance"
    "Load/Wash conductivity": ["hcp"],               # "Reduced HCP clearance"
    "Elution buffer pH": ["aggregates_hmw"],         # "Alters aggregate distribution and yield"
    "Elution stop collect": ["aggregates_hmw"],      # "Minor increase in pool aggregate"
    "Elution flow rate": ["aggregates_hmw"],         # "Affects peak shape and yield (minor …)"
}

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
# Two further validated methods the RE-AUTHORED report names and the plan does not: the
# UV concentration assay that step yield is calculated from, and the verification-qualified
# aggregate method used for the DEV-007-02 verification runs. They appear only in the
# report's Appendix D performance table, so they are anchored on that table's rows.
CX_REPORT_ONLY_METHODS = [
    ("AMV-3019", "Protein Concentration by A280 (UV)", "spectroscopy",
     ["protein concentration"], []),
    ("AMV-3221", "Aggregate by SEC-HPLC (verification-qualified)", "chromatography",
     ["aggregate"], ["aggregates_hmw"]),
]
# Methods with a row in the report's Appendix D performance table (AMV-3011 and AMV-3014
# have no validated-performance record, so the report says where theirs are held).
CX_PERF_IDS = ["AMV-3011", "AMV-3012", "AMV-3014", "AMV-3016", "AMV-3019", "AMV-3221"]


def _cx_cqa_row(key):
    return P.cqa_reg[P.cqa_reg.key == key].iloc[0].to_dict()


# Both documents render every table through ``_pcpkg.show`` (``df.to_markdown`` with the
# automatic per-column float formats), so rebuilding a row from the same DataFrame reproduces
# the rendered row verbatim. A per-record quote can then span the whole relation — the
# parameter with its set-point, ranges and (in the report) its classification; the attribute
# with its acceptance criterion and criticality; the proven acceptable range with the two
# analyses that produced it — instead of a caption that every record of the table would share.
CX_TAB = {                                   # kind -> (table id, caption as rendered)
    "plan_params": ("PCP-007_tab_params",
                    "Process parameters, characterization ranges, normal operating ranges and "
                    "study type."),
    "report_params": ("PCR-007_tab_params",
                      "Process parameters of the cation exchange step. The characterization "
                      "range is the range studied, not a proven acceptable range; the proven "
                      "acceptable ranges are computed in §7."),
    "plan_cqa": ("PCP-007_tab_cqa",
                 "Quality attributes this step governs, with acceptance criteria and "
                 "criticality."),
    "report_cqa": ("PCR-007_tab_cqa",
                   "Quality attributes controlled by the cation exchange step, with the drug "
                   "substance acceptance criterion, the assigned criticality and the Tool #1 "
                   "score."),
    "plan_sops": ("PCP-007_tab_sops",
                  "Controlled procedures and validated analytical methods for the study."),
    "report_sops": ("PCR-007_tab_sops",
                    "Controlled documents and validated analytical methods for the cation "
                    "exchange step."),
    "risk": ("PCP-007_tab_risk",
             "Pre-characterization effects, risk scores and assigned study type for the "
             "parameters of the step (RA-001)."),
    "par": ("PCR-007_tab_par",
            "Proven acceptable ranges for each governed attribute and parameter, from the "
            "at-set-point analysis and from the NOR-propagated Monte-Carlo analysis of the "
            "fitted response-surface model."),
    "cap": ("PCR-007_tab_cap",
            "Commercial-scale capability of the quality attributes governed by the cation "
            "exchange step. Cpk is one-sided against the upper acceptance limit."),
    "methperf": ("PCR-007_tab_methperf",
                 "Validated performance of the analytical methods used at the cation exchange "
                 "step."),
}
_CX_ROWS: dict = {}


def _cx_rows(kind):
    """Rendered rows of a table one of the two documents renders, keyed for lookup.

    ``plan_params`` / ``report_params`` and ``risk`` are keyed by parameter name, ``cqa`` and
    ``cap`` by CQA key, ``sops`` / ``methperf`` by the reference identifier, ``par`` by
    ``(CQA, parameter)``.
    """
    if not _CX_ROWS:
        import doe_report as D
        pp, rp = P.plan_params(CXUO), P.report_params(CXUO)
        cq, cap = P.cqas_by_keys(CX_CQA_KEYS), P.cap_for(CX_CQA_KEYS)
        cap_keys = P.cap[P.cap.key.isin(CX_CQA_KEYS)]["key"].tolist()
        par = D.par_table(CXUO)
        ra = P.ra_scope(CXUO).drop(columns=["Prospective failure mode", "Priority"])
        sop_rows = [[s, t, "SOP"] for s, t in P.CEX_SOP_REFS]
        sop_rows += [[a, t, "Method validation"] for a, t in P.CEX_AMV_REFS]
        sop = P.pd.DataFrame(sop_rows, columns=["Reference", "Title", "Type"])
        mp = P.method_perf_df()
        mp = mp[mp["Method"].isin(CX_PERF_IDS)].sort_values("Method").reset_index(drop=True)
        _CX_ROWS.update(
            plan_params=row_quotes(pp, pp["Parameter"], P._auto_floatfmt(pp)),
            report_params=row_quotes(rp, rp["Parameter"], P._auto_floatfmt(rp)),
            cqa=row_quotes(cq, CX_CQA_KEYS, P._auto_floatfmt(cq)),
            cap=row_quotes(cap, cap_keys, P._auto_floatfmt(cap)),
            par=row_quotes(par, zip(par["CQA"], par["Parameter"]), P._auto_floatfmt(par)),
            risk=row_quotes(ra, ra["Parameter"], P._auto_floatfmt(ra)),
            sops=row_quotes(sop, sop["Reference"]),
            methperf=row_quotes(mp, mp["Method"], P._auto_floatfmt(mp)),
        )
    return _CX_ROWS[kind]


def cx_step(doc_id, file_name, sec, report):
    if report:
        # §1.1 names the step, its number and both of its neighbours in one span.
        src = [ref(doc_id, file_name, sec, "Product and unit operation",
                   "Cation exchange is Step 7. It receives the neutralized pool of the low-pH "
                   "hold and delivers the load of the anion exchange step"),
               ref(doc_id, file_name, sec, "Quality attributes in scope",
                   "The step sets no quality attribute of its own. Aggregate, host cell protein "
                   "and residual DNA are established upstream in the bioreactor and the harvest, "
                   "and leached Protein A appears at the capture step (PCR-005)")]
    else:
        src = [ref(doc_id, file_name, sec, "Purpose and scope",
                   "The step is operated in bind and elute mode on a strong cation exchange "
                   "resin"),
               ref(doc_id, file_name, sec, "Purpose and scope",
                   "The step forms no quality attribute of its own. Every attribute in scope is "
                   "established upstream")]
    return S.ProcessStep(
        step_id="step:cex", step_name=CXUO_NAME, step_number=str(CXSTEP),
        unit_operation=CXUO_NAME,
        # "last step at which aggregate is reduced" is what both documents state; the earlier
        # "only step in the train that reduces aggregate" is stronger than either supports.
        description="Bind-and-elute cation-exchange polishing: the last step of the train at "
                    "which high molecular weight aggregate is reduced, and a major clearance "
                    "step for HCP, with further clearance of residual DNA and leached Protein A. "
                    "Forms no product-quality CQA; every attribute it governs is formed upstream "
                    "and reduced here.",
        input_materials=["neutralized viral-inactivation pool (cation-exchange feed)"],
        output_materials=["cation-exchange eluate pool (anion-exchange feed)"],
        equipment=["cation-exchange column", "scale-down chromatography column"],
        source_references=src, metadata=meta())


def cx_equipment(doc_id, file_name, sec, report):
    sdm = S.Equipment(
        equipment_id="equip:cex_sdm_column", equipment_name="scale-down chromatography column",
        equipment_type="chromatography column (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Scale-down model and its qualification",
                               "The studies were executed on a qualified scale-down model of the "
                               "commercial cation exchange step, operated under SOP-2010 and "
                               "qualified under SOP-1001" if report
                               else "It uses the same resin, the same bed height and the same "
                                    "linear velocity as the commercial column, load is expressed "
                                    "in grams of product per litre of resin")],
        metadata=meta())
    if report:
        return [sdm]
    return [
        S.Equipment(equipment_id="equip:cex_column",
                    equipment_name="commercial-scale cation-exchange polishing column",
                    equipment_type="chromatography column", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec,
                                           "Scale-down model and its qualification",
                                           "Every run of this study will be executed on a "
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
    kind = "report_params" if classified else "plan_params"
    tab_id, caption = CX_TAB[kind]
    rows = _cx_rows(kind)
    rats = {"WC-CPP": "Demonstrated effect on pool aggregate or on pool host cell protein, with a "
                      "low risk of leaving the design space in routine operation because the "
                      "parameter is calculated and verified before the run, measured in line, set "
                      "by a released buffer or triggered automatically on the ultraviolet trace.",
            "GPP": "The univariate assessment returned no link to a quality attribute of the step "
                   "across the characterization range; the parameter acts through residence time "
                   "and column efficiency and not through the chemistry of binding."}
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
                                   rows[name], table_title=caption, table_id=tab_id)],
            metadata=meta()))
    return out


def cx_cqas(doc_id, file_name, sec, report):
    """One QualityAttribute per governed attribute, anchored on its own rendered row.

    Both documents render the same register through ``cqas_by_keys``, so the row carries the
    attribute, its category, its drug-substance acceptance criterion, its criticality and its
    Tool #1 score in one span. The captions differ between the two documents.
    """
    tab_id, caption = CX_TAB["report_cqa" if report else "plan_cqa"]
    rows = _cx_rows("cqa")
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
                                   rows[key], table_title=caption, table_id=tab_id)],
            metadata=meta()))
    return out


# Per-method prose fragment naming BOTH the attribute and the method that measures it. Used
# for the attribute_measured_by_method assertions (the plan states the linkage explicitly;
# the report states it in one sentence for three of the four methods).
CXMETHOD_QUOTE = {
    False: {  # PCP-007 §5.3
        "AMV-3011": ("Aggregate is measured by size exclusion chromatography (AMV-3011) and "
                     "reported as the percentage of high molecular weight species"),
        "AMV-3012": ("HCP is measured by enzyme-linked immunosorbent assay (AMV-3012) and "
                     "reported against the product concentration in nanograms per milligram"),
        "AMV-3014": ("Residual DNA is measured by quantitative PCR (AMV-3014) and leached "
                     "Protein A by ELISA (AMV-3016)"),
        "AMV-3016": ("Residual DNA is measured by quantitative PCR (AMV-3014) and leached "
                     "Protein A by ELISA (AMV-3016)"),
    },
    True: {  # PCR-007 §3.3
        "AMV-3011": ("Pool aggregate was measured by size-exclusion chromatography under "
                     "AMV-3011, and it is the primary assay of the study"),
        "AMV-3012": ("Pool host cell protein was measured by ELISA under AMV-3012, residual DNA "
                     "by qPCR under AMV-3014 and leached Protein A by ELISA under AMV-3016"),
        "AMV-3014": ("Pool host cell protein was measured by ELISA under AMV-3012, residual DNA "
                     "by qPCR under AMV-3014 and leached Protein A by ELISA under AMV-3016"),
        "AMV-3016": ("Pool host cell protein was measured by ELISA under AMV-3012, residual DNA "
                     "by qPCR under AMV-3014 and leached Protein A by ELISA under AMV-3016"),
    },
}
# The two report-only methods are named where the report uses them, not in the shared list.
CX_EXTRA_METHOD_QUOTE = {
    "AMV-3019": ("step yield was calculated from the protein mass in the pool and in the load "
                 "using protein concentration by ultraviolet absorbance (AMV-3019)"),
    "AMV-3221": ("The verification runs of DEV-007-02 used a separate verification-qualified "
                 "aggregate method (AMV-3221)"),
}


def cx_methods(doc_id, file_name, sec, report):
    """Validated methods, each anchored on its own rendered controlled-document row.

    The row carries the identifier, the validated title and the document type in one span,
    which is the relation the entity records. The two report-only methods have no row in that
    table — they are named in the prose and carry a row in the report's Appendix D performance
    table, which is what they are anchored on.
    """
    tab_id, caption = CX_TAB["report_sops" if report else "plan_sops"]
    rows = _cx_rows("sops")
    out = []
    for mid, mname, mtype, analytes, attrs in CXMETHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[CXATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods", rows[mid],
                                   table_title=caption, table_id=tab_id)],
            metadata=meta()))
    if not report:
        return out
    perf_id, perf_caption = CX_TAB["methperf"]
    perf = _cx_rows("methperf")
    for mid, mname, mtype, analytes, attrs in CX_REPORT_ONLY_METHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[CXATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[
                ref(doc_id, file_name, f"{doc_id}_sec_appd", "Appendix D — Analytical methods "
                    "summary", perf[mid], table_title=perf_caption, table_id=perf_id),
                ref(doc_id, file_name, sec, "Analytical methods", CX_EXTRA_METHOD_QUOTE[mid])],
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
                                   "A full factorial estimates every main effect and every "
                                   "two-factor interaction without aliasing, which a fractional "
                                   "design of this size could not do" if report
                                   else "Fractioning would save little and would alias "
                                        "interactions with main effects")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:cex_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=CXUO_NAME,
            factors=CX_MULTIVARIATE, responses=responses,
            n_runs=n_rsm, n_center_points=P.doe_centre_points(CXUO, "rsm"), scale_down_model="scale-down chromatography column",
            associated_parameters=[CXPARAM_CONCEPT[f] for f in CX_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "The axial points sit on the faces and not beyond them, so no "
                                   "run exceeds the characterization range of any parameter and "
                                   "the model is never extrapolated within its own data" if report
                                   else "The axial points sit on the faces of the cube, so no run "
                                        "leaves the characterization range of any factor")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:cex_sdm_qual", study_type="scale_down_qualification",
            unit_operation=CXUO_NAME, scale_down_model="scale-down chromatography column",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "Qualification compared the model against "
                                   "commercial-equivalent runs on the attributes that enter and "
                                   "leave the step" if report
                                   else "Triplicate runs at the set-point of every parameter will "
                                        "be compared with commercial scale data for product "
                                        "yield, pool volume, aggregate clearance, HCP clearance "
                                        "and leached Protein A")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:cex_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=CXUO_NAME,
            factors=CX_UNIVARIATE, responses=["step yield", "pool aggregate", "pool HCP"],
            associated_parameters=[CXPARAM_CONCEPT[f] for f in CX_UNIVARIATE],
            source_references=[ref(doc_id, file_name, "Study design", "Univariate assessment",
                                   "It was kept out of the multivariate design for a mechanistic "
                                   "reason. Flow rate changes residence time and column "
                                   "efficiency" if report
                                   else "Elution flow rate will be assessed one at a time, with "
                                        "every other parameter held at its set-point")],
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

    def add(subj, pred, obj, text, sec, quote, table_title=None, table_id=None):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote,
                                   table_title=table_title, table_id=table_id)],
            metadata=meta()))

    # Each step_has_parameter record is anchored on ITS OWN rendered parameter row, which
    # carries the parameter, its set-point, both ranges and (in the report) its classification.
    param_kind = "report_params" if report else "plan_params"
    param_tab, param_caption = CX_TAB[param_kind]
    param_rows = _cx_rows(param_kind)
    param_sec = ("Factors, ranges and the knowledge space" if report
                 else "Factors, ranges and study type")
    for name, cid in CXPARAM_CONCEPT.items():
        add("step:cex", "step_has_parameter", cid,
            f"{CXUO_NAME} has process parameter {name}.", param_sec, param_rows[name],
            table_title=param_caption, table_id=param_tab)
    # The step SETS no CQA. Aggregate is the one it effectively decides (no later operation
    # reduces it); HCP, DNA and leached Protein A are cleared here and again downstream. Each
    # record anchors on its own row of the governed-attribute table.
    cqa_tab, cqa_caption = CX_TAB["report_cqa" if report else "plan_cqa"]
    cqa_rows = _cx_rows("cqa")
    add("step:cex", "step_has_quality_attribute", "attr:aggregates_hmw",
        f"{CXUO_NAME} is the last step in the train that reduces aggregate, so the "
        f"drug-substance aggregate content is effectively decided by what this step delivers.",
        "Quality attributes in scope", cqa_rows["aggregates_hmw"],
        table_title=cqa_caption, table_id=cqa_tab)
    for key in ["hcp", "residual_dna", "leached_protein_a"]:
        add("step:cex", "step_has_quality_attribute", CXATTR_CONCEPT[key],
            f"{CXUO_NAME} clears {CXATTR_NAME[key]} (formed upstream; not set here).",
            "Quality attributes in scope", cqa_rows[key],
            table_title=cqa_caption, table_id=cqa_tab)
    # attribute -> method. Both documents state the linkage in their analytical-methods
    # section, in prose that names both ends.
    for key in CX_CQA_KEYS:
        add(CXATTR_CONCEPT[key], "attribute_measured_by_method", f"method:{CX_CQA_METHOD[key]}",
            f"{CXATTR_NAME[key]} is measured by {CX_CQA_METHOD[key]}.", "Analytical methods",
            CXMETHOD_QUOTE[report][CX_CQA_METHOD[key]])
    # Acceptance criteria — one record per attribute, on the row that carries the limit. The
    # aggregate limit is the one that binds AT this step, because no later operation reduces
    # aggregate; the other three are drug-substance limits the train delivers together.
    for key in CX_CQA_KEYS:
        r = _cx_cqa_row(key)
        add(CXATTR_CONCEPT[key], "attribute_has_acceptance_criterion", f"lit:{key}_acc",
            f"{CXATTR_NAME[key]} acceptance: {r['acc_low']:g}–{r['acc_high']:g} {r['unit']} "
            f"(drug-substance criterion)"
            + (", applied directly to this pool because no later operation reduces aggregate."
               if key == "aggregates_hmw" else "."),
            "Quality attributes in scope", cqa_rows[key],
            table_title=cqa_caption, table_id=cqa_tab)
    # parameter -> attribute impacts / non-impacts
    if report:
        add("param:cex_load", "parameter_impacts_attribute", "attr:aggregates_hmw",
            "Protein load is the only parameter with a significant effect on all three responses "
            "and carries the largest effect on two of them (WC-CPP).",
            "Parameter classification",
            "Protein load is a well-controlled critical process parameter, because it is the only "
            "parameter with a significant effect on all three responses and the largest effect on "
            "two of them")
        add("param:cex_load", "parameter_impacts_attribute", "attr:hcp",
            "Protein load weakens host cell protein clearance as well as aggregate clearance, "
            "because it reduces the resolution of the separation.",
            "Mechanistic interpretation",
            "Protein load weakens both clearances because it reduces resolution")
        add("param:cex_wash_cond", "parameter_impacts_attribute", "attr:hcp",
            "Load/wash conductivity is the governing parameter of pool host cell protein "
            "(WC-CPP).",
            "Parameter classification",
            "Load/wash conductivity is a well-controlled critical process parameter. It is the "
            "governing parameter of pool host cell protein")
        add("param:cex_elution_ph", "parameter_impacts_attribute", "attr:aggregates_hmw",
            "Elution buffer pH raises pool aggregate across its range and interacts with protein "
            "load (WC-CPP).",
            "Parameter classification",
            "Elution buffer pH is a well-controlled critical process parameter, since it raises "
            "pool aggregate")
        add("param:cex_stop_collect", "parameter_impacts_attribute", "attr:aggregates_hmw",
            "The stop collect criterion raises pool aggregate across its range and interacts with "
            "protein load and elution buffer pH (WC-CPP).",
            "Parameter classification",
            "Elution stop collect is a well-controlled critical process parameter. It raises pool "
            "aggregate")
        add("param:cex_wash_cond", "parameter_does_not_significantly_impact_attribute",
            "attr:aggregates_hmw",
            "Load/wash conductivity has no significant effect on pool aggregate in either design; "
            "the null result is retained in the knowledge space.",
            "Parameter classification",
            "Load/wash conductivity has no significant effect on pool aggregate in either design")
        add("param:cex_flow", "parameter_does_not_significantly_impact_attribute",
            "attr:aggregates_hmw",
            "The univariate assessment of the elution flow rate returned no link to a quality "
            "attribute of the step over the range studied (GPP).",
            "Parameter classification",
            "that assessment returned no link to a quality attribute of the step, and the "
            "parameter stays in the knowledge space as evidence of robustness over that range")
    else:
        # The plan's scope decision is a table relation: RA-001's prospective effect and the
        # assigned study type for each parameter. Each record anchors on its own row of that
        # table, and each names the attribute RA-001 actually records for that parameter —
        # NOT aggregate for all four. RA-001 scores load/wash conductivity on host cell
        # protein clearance alone, and the plan's own mechanism section says the same, so an
        # assertion that conductivity impacts aggregate would contradict both documents (and
        # the report, which finds no conductivity effect on aggregate in either design).
        risk_tab, risk_caption = CX_TAB["risk"]
        risk_rows = _cx_rows("risk")
        ra_effect = dict(zip(P.ra_scope(CXUO)["Parameter"], P.ra_scope(CXUO)["Effect"]))
        for name, keys in CX_RA_ATTRS.items():
            for key in keys:
                add(CXPARAM_CONCEPT[name], "parameter_impacts_attribute", CXATTR_CONCEPT[key],
                    f"RA-001 records the prospective effect of {name} as \"{ra_effect[name]}\", "
                    f"which is why the parameter is in scope against {CXATTR_NAME[key]}. No "
                    f"effect has been measured at the time this plan is approved.",
                    "Risk-based prioritization of parameters", risk_rows[name],
                    table_title=risk_caption, table_id=risk_tab)
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def cx_report_sections(doc_id, file_name, report):
    from annex_contract.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-007 defines the Stage 1 characterization study for the A-Mab cation-exchange "
                  "polishing step (Step 7) and fixes its acceptance and decision criteria before "
                  "any data exist.",
               "Purpose and scope",
               "This plan defines the Stage 1 characterization study for the cation exchange "
               "chromatography step of the A-Mab drug substance process"),
            st(2, "A parameter that can affect a quality attribute is carried into the designed "
                  "experiment; a parameter that acts on process performance alone is assessed one "
                  "factor at a time.",
               "Risk-based prioritization of parameters",
               "A parameter that can affect a quality attribute is carried into the designed "
               "experiment of the step, and a parameter that acts on process performance alone is "
               "assessed one at a time"),
            st(3, "The response-surface design is a face-centred central composite whose axial "
                  "points sit on the faces of the cube, so no run leaves the characterization "
                  "range of any factor.",
               "Response-surface design",
               "The axial points sit on the faces of the cube, so no run leaves the "
               "characterization range of any factor"),
            st(4, "Reducing high molecular weight aggregate is the principal duty of the step, "
                  "which also clears host cell protein, residual DNA and leached Protein A.",
               "Purpose and scope",
               "Its principal duty is the reduction of high molecular weight aggregate, and it "
               "also delivers a large part of the clearance of host cell protein (HCP), residual "
               "DNA and leached Protein A"),
            st(5, "The aggregate criterion binds at this step, because no later step reduces "
                  "aggregate, so an aggregate range is a range the commercial process is held to.",
               "Proven acceptable ranges (planned analysis)",
               "The criterion for aggregate binds at this step, because no later step reduces "
               "aggregate, so an aggregate range is a range the commercial process is held to"),
            st(6, "The plan sets no in-process limit on pool host cell protein, because the drug "
                  "substance criterion applies to the drug substance and not to the pool of an "
                  "intermediate step.",
               "Acceptance and decision criteria",
               "This plan therefore sets no in-process limit on pool HCP"),
            st(7, "A pool host cell protein level above the drug substance criterion is not by "
                  "itself a failure of this step, because anion exchange provides further "
                  "clearance downstream.",
               "Acceptance and decision criteria",
               "so a pool HCP level above the drug substance criterion is not by itself a failure "
               "of this step"),
            st(8, "The response-surface model, and not the screening model, is the predictive "
                  "model of the step and the basis of the design space and the proven acceptable "
                  "ranges.",
               "Statistical methods",
               "This model, and not the screening model, is the predictive model of the step"),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "No parameter of the step required the critical process parameter designation and "
              "none is a key process parameter; the four multivariate parameters are "
              "well-controlled CPPs and the elution flow rate is a general process parameter.",
           "Parameter classification",
           "No parameter of this step required the more stringent critical process parameter "
           "designation, and none is a key process parameter"),
        st(2, "Aggregate is the attribute this step effectively decides, because no later "
              "operation in the train reduces it.",
           "Process capability and robustness",
           "Aggregate is the one this step effectively decides, because no later operation "
           "reduces it"),
        st(3, "Pool host cell protein is driven by load/wash conductivity and by protein load, "
              "and no other term reaches significance.",
           "Screening: factor effects",
           "Pool host cell protein is driven by load/wash conductivity and protein load, and no "
           "other term reaches significance"),
        st(4, "Neither impurity response-surface model is over-fitted, and both are used to "
              "predict a mean level at a new setting inside the region.",
           "Response-surface models",
           "Neither model is over-fitted, and both can be used to predict a mean level at a new "
           "setting inside the region"),
        st(5, "Three two-factor interactions are significant in the pool aggregate "
              "response-surface model and none of the four quadratic terms is, so that surface is "
              "close to planar with an interaction twist.",
           "Response-surface models",
           "Three two-factor interactions are significant and none of the four quadratic terms "
           "is, so the surface is close to planar with an interaction twist"),
        st(6, "The step yield model cannot support a prediction at a new setting, so the yield "
              "result is reported as a trend and is excluded from the design-space argument.",
           "Response-surface models",
           "A model with a predicted coefficient of determination of that size cannot support a "
           "prediction at a new setting, so the yield result is reported below as a trend and is "
           "excluded from the design-space argument"),
        st(7, "Measured against the drug substance specification, the step has no proven "
              "acceptable range for host cell protein.",
           "Proven acceptable ranges",
           "Measured against the drug substance specification, this step has no proven acceptable "
           "range for host cell protein"),
        st(8, "No operating region can be declared at this step on the basis of the drug substance "
              "host cell protein limit, because the pool is an intermediate.",
           "Design space",
           "no operating region can be declared here on the basis of the drug substance host cell "
           "protein limit"),
        st(9, "All four attributes the step governs meet their drug substance acceptance criteria "
              "at commercial scale, and host cell protein is the tightest of them.",
           "Process capability and robustness",
           "All four attributes the step governs meet their drug substance acceptance criteria at "
           "commercial scale, and host cell protein is the tightest of them"),
        st(10, "The capability figures belong to the drug substance and not to this step alone, "
               "and the credit divides differently for each attribute.",
            "Process capability and robustness",
            "These capabilities belong to the drug substance and not to this step alone, and the "
            "credit divides differently for each attribute"),
        st(11, "The step takes no viral clearance credit; the modular claim rests on PCR-006, "
               "PCR-008 and PCR-009.",
            "Contribution to the control strategy",
            "The step also takes no viral clearance credit, and the modular claim rests on "
            "PCR-006, PCR-008 and PCR-009"),
        st(12, "Two deviations were recorded; both were retained after investigation and neither "
               "altered an effect estimate, a classification or a range.",
            "Conclusions",
            "Both were retained after investigation, and neither altered an effect estimate, a "
            "classification or a range"),
    ])]


def cx_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:cex", unit_operation=CXUO_NAME,
        parameters=["param:cex_load", "param:cex_wash_cond", "param:cex_elution_ph",
                    "param:cex_stop_collect"],
        quality_attributes_constrained=["attr:aggregates_hmw"],
        # As far as POOL AGGREGATE is concerned the region is the whole characterized box: the
        # fitted model meets the aggregate limit everywhere on a uniform grid, including the
        # worst corner (all four parameters at their upper edges). Pool HCP is the other half of
        # the report's answer, and it is NOT judged against a back-calculated step ceiling —
        # the report states that no step-level requirement had to be back-calculated. The pool
        # is an intermediate, its predicted level is above the drug-substance criterion, and the
        # region is bounded for that attribute by what anion exchange can clear (PCR-008).
        definition="The whole of the characterized four-dimensional region in protein load, "
                   "load/wash conductivity, elution buffer pH and the stop collect criterion, as "
                   "far as pool aggregate is concerned: the fitted model meets the aggregate "
                   "acceptance limit across the whole region, including the worst corner (all "
                   "four parameters at their upper edges), so aggregate does not constrain the "
                   "region. For pool host cell protein the region is bounded by what the anion "
                   "exchange step can clear. The predicted pool level at the set-point is above "
                   "the drug-substance host-cell-protein specification, so no operating region "
                   "can be declared here on the basis of that limit.",
        source_references=[ref(doc_id, file_name, "Design space", "Design space",
                               "The operating region of this step is the whole characterized "
                               "region as far as pool aggregate is concerned, and it is bounded "
                               "for pool host cell protein by what the anion exchange step can "
                               "clear"),
                           ref(doc_id, file_name, "Design space", "Design space",
                               "Aggregate does not constrain the region. The multivariate region "
                               "for that attribute is the characterized region itself")],
        metadata=meta())]


# --------------------------------------------------------------------------- #
# Report-only PAR / discourse layers (PCR-007 only).                            #
# --------------------------------------------------------------------------- #
# proven_acceptable_ranges derive from the same DoE engine that renders @tbl-par  #
# (doe_report.par_table), and each record is anchored on ITS OWN rendered row of   #
# that table. Aggregate is proven acceptable across every full characterization    #
# range under both analyses; pool HCP returns "none (set-point breaches)" for      #
# every parameter, because the predicted pool level at the set-point is above the  #
# drug-substance criterion. The report does NOT rescue that with a back-calculated #
# step ceiling — it says the opposite ("no step-level requirement had to be         #
# back-calculated from a cumulative claim") and records the result plainly:         #
# "this step has no proven acceptable range for host cell protein". The clearance   #
# that brings HCP to the drug-substance level is shared with anion exchange         #
# (PCR-008). PCR-007 carries NO weak_claims. These layers are report-only.          #
# --------------------------------------------------------------------------- #
CX_PAR_SEC = "Proven acceptable ranges"


def cx_proven_acceptable_ranges(doc_id, file_name):
    """One ProvenAcceptableRange per governed response x response-surface parameter, from the
    same DoE engine (``doe_report.par_table``) that renders @tbl-par in the report.

    Each record is anchored on its own rendered row, which carries the attribute, the
    parameter, the characterization range and both computed ranges in one span. Both
    responses use a drug-substance specification as the acceptance basis; the report states
    that neither is a viral-clearance attribute, so no step-level requirement was
    back-calculated from a cumulative claim. For pool HCP the predicted pool level at the
    set-point is above that specification, so neither analysis returns an interval — the
    basis records that, and records where the remaining clearance comes from.
    """
    import doe_report as D
    par = D.par_table(CXUO)
    tab_id, caption = CX_TAB["par"]
    rows = _cx_rows("par")
    hcp_acc = _cx_cqa_row("hcp")
    agg_acc = _cx_cqa_row("aggregates_hmw")
    out = []
    for i, r in enumerate(par.to_dict("records"), 1):
        cqa, param, unit = r["CQA"], r["Parameter"], (r["Unit"] or "")
        char = f"{r['Char. range']} {unit}".strip()
        hcp = "HCP" in cqa
        basis = (
            f"Drug-substance host-cell-protein specification "
            f"({hcp_acc['acc_high']:g} {hcp_acc['unit']}), applied as the upper acceptance limit. "
            f"Nothing is back-calculated here: neither response is a viral-clearance attribute, "
            f"so no step-level requirement was derived from a cumulative claim. The "
            f"cation-exchange pool is an intermediate and its predicted level at the set-point is "
            f"above the specification, so no interval containing the set-point can satisfy the "
            f"criterion under either analysis and the table records none for every parameter. "
            f"Measured against that specification the step has no proven acceptable range for "
            f"host cell protein; the clearance that brings the attribute to the drug-substance "
            f"level is shared with anion exchange (PCR-008)."
            if hcp else
            f"Drug-substance aggregate specification "
            f"({agg_acc['acc_high']:g} {agg_acc['unit']}), applied as the upper acceptance limit "
            f"directly to this pool, because no downstream operation reduces aggregate. Both "
            f"analyses return the full characterization range, so the result is robust to "
            f"co-variation of the other parameters inside their normal operating ranges.")
        out.append(S.ProvenAcceptableRange(
            par_id=f"{doc_id}-PAR{i:02d}", unit_operation=CXUO_NAME,
            quality_attribute=cqa, parameter=param,
            characterization_range=char,
            par_at_setpoint=f"{r['PAR (set-point)']} {unit}".strip() if not hcp
            else r["PAR (set-point)"],
            par_nor_propagated=f"{r['PAR (NOR)']} {unit}".strip() if not hcp
            else r["PAR (NOR)"],
            acceptance_basis=basis,
            source_references=[ref(doc_id, file_name, f"{doc_id}_sec_par", CX_PAR_SEC,
                                   rows[(cqa, param)], table_title=caption, table_id=tab_id)],
            metadata=meta()))
    return out


# Argument-structure spans over the PCR-007 report. Each quote is a verbatim, plain-prose
# fragment of the rendered report (no inline expressions, no bold). Tuple fields:
# (suffix, role, section, quote, supported_by-suffixes, restates-suffix, bounds-suffix).
CX_RHET_SPANS = [
    # --- the gap the study was run to close -------------------------------------------- #
    ("R00", "problem_statement", "Platform and prior-product knowledge",
     "These expectations fix the sign of each effect, but they do not fix its size, and they say "
     "nothing about which interactions matter over the ranges the process will be operated "
     "across", [], None, None),
    # --- executive summary: what is and is not claimed ---------------------------------- #
    ("R01", "claim", "Executive summary",
     "The step forms no quality attribute of its own, so its role in the control strategy is "
     "clearance and not formation", [], None, None),
    ("R02", "claim", "Executive summary",
     "Across the whole characterized region the predicted pool aggregate stays below its "
     "acceptance limit", [], None, None),
    ("R03", "claim", "Executive summary",
     "The step also does not bring pool host cell protein within the drug substance specification "
     "on its own", [], None, None),
    ("R04", "cross_step_credit", "Executive summary",
     "the remaining clearance is provided by the anion exchange step (PCR-008)", [], None, None),
    ("R05", "bounded_conclusion", "Executive summary",
     "The step is characterized over the ranges given in §4, on a scale-down model qualified "
     "against commercial-equivalent data, and the results roll up into PCMR-001", [], None, None),
    # --- scale-down warrant and its bound ----------------------------------------------- #
    ("R06", "bounded_conclusion", "Scale-down model and its qualification",
     "The model supports statements about how the pool attributes respond to the parameters of "
     "the step, because the separation mechanism is preserved, but it does not support statements "
     "about commercial column packing, wall effects at diameter, or the state of the resin after "
     "many cycles", [], None, None),
    # --- reproducibility -------------------------------------------------------------- #
    ("R07", "hedge", "Centre-point performance and reproducibility",
     "The practical consequence is that a small change in host cell protein clearance is harder "
     "to detect at this step than a small change in aggregate clearance", [], None, None),
    # --- screening: what is active, and on what mechanism ------------------------------- #
    ("R08", "mechanistic_warrant", "Mechanistic interpretation",
     "As the column approaches its capacity the monomer peak broadens and overlaps the more "
     "strongly retained aggregate and the more weakly retained host cell protein, so more of each "
     "ends up inside the collected pool", [], None, None),
    ("R09", "mechanistic_warrant", "Mechanistic interpretation",
     "Host cell proteins bind through weaker and more heterogeneous electrostatic contacts than "
     "the antibody does, so raising the ionic strength of the wash displaces them while the "
     "product stays bound", [], None, None),
    ("R10", "mechanistic_warrant", "Mechanistic interpretation",
     "A higher elution pH weakens the interaction of the strongly bound aggregate and moves it "
     "forward into the elution peak, and a later stop collect takes more of that edge into the "
     "pool", [], None, None),
    ("R11", "claim", "Screening: factor effects",
     "Pool aggregate is driven by protein load, elution buffer pH and elution stop collect",
     ["R08", "R10"], None, None),
    ("R12", "claim", "Screening: factor effects",
     "Pool host cell protein is driven by load/wash conductivity and protein load, and no other "
     "term reaches significance", ["R08", "R09"], None, None),
    ("R13", "bounded_conclusion", "Screening: factor effects",
     "These are identification results. The magnitudes above were estimated from a design with no "
     "curvature terms, and they are refined by the response-surface model in §5.3, which is the "
     "model used for prediction, for the operating region and for the proven acceptable ranges",
     [], None, None),
    # --- the predictive models and their diagnostics ------------------------------------ #
    ("R14", "justification", "Response-surface models",
     "The gap between the adjusted and the predicted value is small in both cases", [], None,
     None),
    ("R15", "justification", "Response-surface models",
     "Lack of fit is not significant for any of the three responses", [], None, None),
    ("R16", "justification", "Response-surface models",
     "The residuals show no structure against the predicted value in either case, the normal "
     "quantile plot is close to linear, and the actual against predicted plot sits on the "
     "identity line over the whole range of the response", [], None, None),
    ("R17", "claim", "Response-surface models",
     "Neither model is over-fitted, and both can be used to predict a mean level at a new setting "
     "inside the region", ["R14", "R15", "R16"], None, None),
    ("R18", "hedge", "Response-surface models",
     "A model with a predicted coefficient of determination of that size cannot support a "
     "prediction at a new setting, so the yield result is reported below as a trend and is "
     "excluded from the design-space argument", [], None, None),
    ("R19", "claim", "Response-surface models",
     "Three two-factor interactions are significant and none of the four quadratic terms is, so "
     "the surface is close to planar with an interaction twist", [], None, None),
    ("R20", "hedge", "Response-surface models",
     "The second term is retained as an empirical part of the fitted surface, and it is not read "
     "as evidence that elution pH governs host cell protein clearance", [], None, None),
    ("R21", "claim", "Mechanistic interpretation",
     "One consequence of these mechanisms is that the step has no internal conflict between its "
     "two impurity responses", ["R22"], None, None),
    ("R22", "mechanistic_warrant", "Mechanistic interpretation",
     "Raising the wash conductivity improves host cell protein clearance at no cost in pool "
     "aggregate, because conductivity does not appear in the aggregate model at either the "
     "screening or the response-surface stage", [], None, None),
    # --- the region ------------------------------------------------------------------- #
    ("R23", "justification", "Design space",
     "The fitted model meets the aggregate acceptance limit at 100 % of a uniform grid over the "
     "characterized region", [], None, None),
    ("R24", "claim", "Design space",
     "The operating region of this step is the whole characterized region as far as pool "
     "aggregate is concerned, and it is bounded for pool host cell protein by what the anion "
     "exchange step can clear", ["R17", "R23"], None, None),
    ("R25", "claim", "Design space",
     "no operating region can be declared here on the basis of the drug substance host cell "
     "protein limit", [], None, None),
    ("R26", "bounded_conclusion", "Design space",
     "Three bounds apply to the region", [], None, "R24"),
    ("R27", "bounded_conclusion", "Design space",
     "Movement outside the characterization ranges is not supported here and requires new data",
     [], None, None),
    # --- proven acceptable ranges ------------------------------------------------------- #
    ("R28", "justification", "Proven acceptable ranges",
     "The ranges do not narrow when the other parameters vary inside their normal operating "
     "ranges, so the result is robust to co-variation and not only to a single-parameter "
     "excursion", [], None, None),
    ("R29", "claim", "Proven acceptable ranges",
     "For pool aggregate the two analyses coincide, and the whole characterization range of every "
     "parameter is proven acceptable", ["R28"], None, None),
    ("R30", "justification", "Proven acceptable ranges",
     "no interval containing the set-point can satisfy the criterion under either analysis",
     [], None, None),
    ("R31", "claim", "Proven acceptable ranges",
     "Measured against the drug substance specification, this step has no proven acceptable range "
     "for host cell protein", ["R30"], None, None),
    ("R32", "cross_step_credit", "Proven acceptable ranges",
     "The step delivers an intermediate, the clearance that brings host cell protein to the drug "
     "substance level is shared with anion exchange (PCR-008)", [], None, None),
    # --- capability -------------------------------------------------------------------- #
    ("R33", "claim", "Process capability and robustness",
     "All four attributes the step governs meet their drug substance acceptance criteria at "
     "commercial scale, and host cell protein is the tightest of them", [], None, None),
    ("R34", "hedge", "Process capability and robustness",
     "These capabilities belong to the drug substance and not to this step alone, and the credit "
     "divides differently for each attribute", [], None, "R33"),
    ("R35", "cross_step_credit", "Process capability and robustness",
     "Host cell protein is shared across three steps", [], None, None),
    ("R36", "bounded_conclusion", "Process capability and robustness",
     "The estimate carries two bounds", [], None, "R33"),
    # --- classification and control strategy -------------------------------------------- #
    ("R37", "claim", "Parameter classification",
     "No parameter of this step required the more stringent critical process parameter "
     "designation, and none is a key process parameter", [], None, None),
    ("R38", "cross_step_credit", "Contribution to the control strategy",
     "The step does not control host cell protein to the drug substance level on its own, and the "
     "anion exchange step supplies the remaining clearance (PCR-008)", [], None, None),
    ("R39", "deferral", "Contribution to the control strategy",
     "The consolidated control strategy for the drug substance is in PCMR-001", [], None, None),
    # --- discussion -------------------------------------------------------------------- #
    ("R40", "bounded_conclusion", "Discussion",
     "Three limitations remain", [], None, None),
    ("R41", "hedge", "Discussion",
     "Should the commercial control capability for any of the four prove worse than the "
     "scale-down experience suggests, the classification is the element that would be revisited "
     "first, since the effects themselves are established", [], None, None),
    # --- deviations -------------------------------------------------------------------- #
    ("R42", "deviation_disposition", "Deviations from the plan",
     "Both were retained, which means the affected run stayed inside the data set used for the "
     "models", [], None, None),
    ("R43", "deviation_disposition",
     "Expired buffer lot in a screening run (DEV-007-01)",
     "The run was retained, the effect estimates in §5.2 include it, and no other run in either "
     "design used this lot", [], None, None),
    ("R44", "deviation_disposition",
     "Column inlet temperature excursion in a response-surface run (DEV-007-02)",
     "The run was retained. Temperature is not a characterized parameter of this step, so the "
     "excursion changes no coefficient in Table 13 or Table 15", [], None, None),
    # --- conclusions ------------------------------------------------------------------- #
    ("R45", "restatement", "Conclusions",
     "Each of the four multivariate parameters carries a proven acceptable range equal to its "
     "whole characterization range for that attribute, under both analyses of §7", [], "R29",
     None),
    ("R46", "bounded_conclusion", "Conclusions",
     "The cation exchange step is characterized over the ranges in Table 5 and is robust across "
     "them for the attribute it is there to reduce", [], None, None),
]


def cx_rhetorical_spans(doc_id, file_name):
    """Rhetorical / argument-structure spans over the PCR-007 report (report-only)."""
    out = []
    for suffix, role, sec, quote, sup, res, bnd in CX_RHET_SPANS:
        out.append(S.RhetoricalSpan(
            span_id=f"{doc_id}-{suffix}", section=sec, role=role,
            source_reference=ref(doc_id, file_name, f"{doc_id}_sec_rhet", sec,
                                 " ".join(quote.split())),
            supported_by=[f"{doc_id}-{s}" for s in sup],
            restates=(f"{doc_id}-{res}" if res else None),
            bounds=(f"{doc_id}-{bnd}" if bnd else None)))
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
        weak_claims=build_weak_claims(doc, f),
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "CEX sets no CQA; the QualityAttribute entities are the CQAs it controls/clears (formed upstream).",
            "Pool aggregate and pool HCP are in-process responses with no released spec; captured via StudyDesign.responses. Aggregate is nonetheless judged against the DS limit here, because no later step reduces it.",
            "The plan sets NO in-process limit and no second, step-level criterion on pool HCP: §7 says so outright ('This plan therefore sets no in-process limit on pool HCP'). It commits instead to reporting the fitted pool-HCP model and carrying it into PCP-008 and PCMR-001. An earlier annex asserted a step-level criterion here that the plan does not contain.",
            "Nothing is back-calculated at this step: §8 states that no back calculation is needed, because the step carries no viral-clearance claim.",
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
        weak_claims=build_weak_claims(doc, f),
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT + [
            "ProvenAcceptableRange (new model) — per-response x parameter PAR (at-set-point / NOR-propagated); both responses use a drug-substance specification as the acceptance basis",
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "CEX sets no CQA; the QualityAttribute entities are the CQAs it controls/clears (formed upstream).",
            "Pool aggregate and pool HCP are in-process responses with no released spec; reported via studies/report_sections. Aggregate is the exception that binds here: CEX is the last step of the train at which aggregate is reduced, so the DS limit applies directly to this pool and §8 calls it the attribute this step 'effectively decides'.",
            "Pool HCP is measured against the DRUG SUBSTANCE specification and the set-point prediction breaches it, so the PAR analysis returns no interval for any parameter. §7 records the outcome plainly: 'Measured against the drug substance specification, this step has no proven acceptable range for host cell protein.' Nothing is back-calculated — §7 states that no step-level requirement had to be derived from a cumulative claim. An earlier annex asserted a back-calculated step-level ceiling against which every range was acceptable; the report contains no such ceiling.",
            "The operating region is the whole characterized region only as far as pool aggregate is concerned; for pool HCP it is bounded by what AEX can clear, and §6 states that no operating region can be declared here on the basis of the DS HCP limit.",
            "Commercial-scale capability belongs to the DRUG SUBSTANCE and not to this step alone (§8); the step 'effectively decides' aggregate only. Cpk values have no dedicated field and are reported as report_sections statements.",
            "No quadratic term is significant for either impurity response, and the step-yield model is direction-only; the two attribute models carry every prediction.",
            "proven_acceptable_ranges mirror @tbl-par (doe_report.par_table), one record per rendered row; rhetorical_spans are verbatim report prose; PCR-007 carries no weak_claims.",
        ],
        inventory=cx_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=cx_studies(doc, f, report=True),
        design_spaces=cx_design_spaces(doc, f),
        proven_acceptable_ranges=cx_proven_acceptable_ranges(doc, f),
        report_sections=cx_report_sections(doc, f, report=True),
        assertions=cx_assertions(doc, f, report=True), concepts=cx_concepts(),
        rhetorical_spans=cx_rhetorical_spans(doc, f))


# =========================================================================== #
# Anion Exchange Chromatography (Step 8) — PCP-008 / PCR-008.                   #
# --------------------------------------------------------------------------- #
# Additive, self-contained builders for the AEX flow-through polishing DoE      #
# pair. Unlike CEX, AEX SETS one CQA of its own — the cumulative MVM             #
# (parvovirus) clearance claim — and is a major clearance step for enveloped    #
# virus (XMuLV), HCP, residual DNA and leached Protein A. The DoE is a           #
# four-factor full-factorial screen + face-centred CCD in load-pH /             #
# wash1-conductivity / load-conductivity / load; the operating flow rate is a    #
# univariate WC-CPP. All five parameters are WC-CPP. The design space is the     #
# WHOLE characterized region in all four multivariate parameters (no attribute   #
# cuts it back), and §6 states the worst case is NOT one of its corners, so no   #
# corner is recorded as the binding condition. Protein load is a resolved null   #
# retained in the knowledge space; the report reports NO effect estimate for the #
# flow rate, so that parameter carries no effect edge at all. Three deviations   #
# are documented in the report (DEV-008-01 non-representative deamidated load →   #
# both designs                                                                    #
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
    # Two spans: the sentence that places the step in the train, and the one that gives it a
    # step number. Together they carry both ends of "step 8 = anion exchange".
    if report:
        src = [ref(doc_id, file_name, sec, "Executive summary",
                   "Anion exchange chromatography is the final chromatographic step in the "
                   "A-Mab drug substance process"),
               ref(doc_id, file_name, sec, "Product and unit operation",
                   "Anion exchange chromatography is Step 8 and the last chromatographic "
                   "operation before the virus filter")]
    else:
        src = [ref(doc_id, file_name, sec, "Purpose and scope",
                   "Anion exchange chromatography is the final chromatographic step of the "
                   "A-Mab drug substance process, and it is operated in the flow-through mode"),
               ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                   "The anion exchange step is a flow-through polish.")]
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
        source_references=src, metadata=meta())


def ax_equipment(doc_id, file_name, sec, report):
    sdm = S.Equipment(
        equipment_id="equip:aex_sdm_column", equipment_name="scale-down chromatography column",
        equipment_type="chromatography column (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Scale-down model and its qualification",
                               "The studies were executed on a laboratory-scale column qualified "
                               "as a model of the commercial step under SOP-1001" if report
                               else "Every run in this study will be performed on a qualified "
                                    "scale-down model of the commercial column")],
        metadata=meta())
    if report:
        return [sdm]
    return [
        S.Equipment(equipment_id="equip:aex_column",
                    equipment_name="commercial-scale anion-exchange polishing column",
                    equipment_type="chromatography column", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec, "Risks and assumptions",
                                           "The principal risk to this study is that the "
                                           "scale-down model does not represent the commercial "
                                           "column")],
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


# The parameter table each document renders. Every ProcessParameter is anchored on ITS OWN
# rendered row (``row_quotes``), so the span carries the parameter, its set-point, its NOR and
# its characterization range — both ends of every relation the record states. The caption
# grounds too, but one caption standing in for five parameters attests nothing.
AX_PARAM_TABLE = {
    False: ("Factors, ranges and study type",
            "Parameters of the anion exchange step, with the ranges to be studied, the normal "
            "operating ranges and the assigned study type."),
    True: ("Factors, ranges and the knowledge space",
           "Process parameters, ranges, study type and final classification."),
}
# The report's parameter-classification section states, per parameter, why it is a WC-CPP.
# The classified entity carries that sentence as a second reference.
AX_CLASS_SENTENCE = {
    "Load pH": ("Load pH is a well controlled critical process parameter with the largest main "
                "effect on both viral responses and the second largest on host cell protein, "
                "and it appears in both governing planes of the design space"),
    "Equil/Wash-1 conductivity": (
        "Equilibration and wash-1 conductivity is a well controlled critical process parameter. "
        "It has the largest main effect on pool host cell protein and it interacts with load pH."),
    "Load conductivity": (
        "Load conductivity is a well controlled critical process parameter. It has the second "
        "largest main effect on both viral responses and no resolved effect on host cell "
        "protein."),
    "Protein load": (
        "Protein load is a well controlled critical process parameter, although no effect of "
        "protein load on any governed attribute was resolved in either design, which is evidence "
        "that the resin capacity is not approached within the studied range."),
    "Operating flow rate": (
        "Operating flow rate is a well controlled critical process parameter. It was assessed "
        "univariately, and this report presents no effect estimate for it"),
}
# The common part of the classification argument, stated once in the report.
AX_WC_CPP_RATIONALE = (
    "Both classes cover parameters whose variability can affect a critical quality attribute; "
    "the difference is the risk of leaving the design space. That risk is low for every "
    "parameter of this step, because the design space extends to the full characterized range "
    "and the normal operating ranges sit inside it.")


def _ax_param_rows(report):
    """``{parameter -> rendered row}`` of the parameter table each document renders."""
    df = P.report_params(AXUO) if report else P.plan_params(AXUO)
    return row_quotes(df, df["Parameter"], P._auto_floatfmt(df))


def ax_params(doc_id, file_name, sec, classified):
    sec_title, caption = AX_PARAM_TABLE[classified]
    rows = _ax_param_rows(classified)
    out = []
    for r in AXPARAM_ROWS:
        name = r["parameter"]
        ptype = r["classification"] if classified else "unclassified"
        src = [ref(doc_id, file_name, sec, sec_title, rows[name],
                   table_title=caption, table_id=f"{doc_id}_tab_params")]
        if classified:
            src.append(ref(doc_id, file_name, sec, "Parameter classification",
                           AX_CLASS_SENTENCE[name]))
        out.append(S.ProcessParameter(
            parameter_id=AXPARAM_CONCEPT[name], parameter_name=name, parameter_type=ptype,
            unit=r["unit"], target_value=f"{r['setpoint']:g}",
            NOR=f"{r['nor_low']:g}–{r['nor_high']:g} {r['unit']}",
            PAR=f"{r['par_low']:g}–{r['par_high']:g} {r['unit']}",
            associated_step=AXSTEP_LABEL,
            rationale_for_criticality=AX_WC_CPP_RATIONALE if classified else None,
            source_references=src, metadata=meta()))
    return out


# The two documents group the CQA register differently. The plan renders all five attributes in
# one table; the report splits the one attribute the step SETS (cumulative MVM clearance) from
# the four it controls or clears. Each attribute is anchored on its own rendered row, which
# carries the attribute, its acceptance criterion and its criticality in one span.
AX_PLAN_CQA_ORDER = ["lrv_mvm", "lrv_xmulv", "hcp", "leached_protein_a", "residual_dna"]
AX_REPORT_CQA_ORDER = ["hcp", "residual_dna", "leached_protein_a", "lrv_xmulv", "lrv_mvm"]
AX_CQA_TABLE = {
    False: ("tbl-cqa", "Quality attributes governed by the anion exchange step, with acceptance "
                       "criteria and criticality from the drug substance register."),
    True: ("tbl-cqa-scope", "Quality attributes the anion exchange step controls or clears."),
}
AX_CQA_SET_TABLE = ("tbl-cqa-set",
                    "Critical quality attribute assigned to the anion exchange step.")


def _ax_cqa_rows(report):
    """``{cqa key -> rendered row}`` of the CQA table(s) the document renders."""
    order = AX_REPORT_CQA_ORDER if report else AX_PLAN_CQA_ORDER
    df = P.cqas_by_keys(order)
    rows = row_quotes(df, order, P._auto_floatfmt(df))
    if report:
        # @tbl-cqa-set renders the MVM row on its own; the two render identically.
        one = P.cqas_for(AXUO)
        rows["lrv_mvm"] = row_quotes(one, ["lrv_mvm"], P._auto_floatfmt(one))["lrv_mvm"]
    return rows


def ax_cqas(doc_id, file_name, sec, report):
    rows = _ax_cqa_rows(report)
    out = []
    for key in AX_CQA_KEYS:
        r = _ax_cqa_row(key)
        sets_it = report and key == "lrv_mvm"
        tid, ttitle = AX_CQA_SET_TABLE if sets_it else AX_CQA_TABLE[report]
        out.append(S.QualityAttribute(
            attribute_id=AXATTR_CONCEPT[key], attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"],
            acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            # Both documents name the validated method for every attribute in scope (PCP-008 §5.3,
            # PCR-008 §3.3), so the linkage is recorded on both sides.
            analytical_method=AX_CQA_METHOD[key],
            associated_steps=[AXSTEP_LABEL],
            rationale_for_criticality=f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = {r['tool1_score']}.",
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref(doc_id, file_name, sec, "Quality attributes in scope",
                                   rows[key], table_title=ttitle,
                                   table_id=f"{doc_id}_{tid}")],
            metadata=meta()))
    return out


# Per-method grounded fragment stating which analyte the method measures. Both documents make
# the linkage, in different words; the plan prospectively, the report as executed.
AXMETHOD_QUOTE = {
    False: {  # PCP-008 §5.3
        "AMV-3012": "Pool host cell protein is measured by ELISA (AMV-3012)",
        "AMV-3014": "residual DNA is measured by qPCR (AMV-3014)",
        "AMV-3016": "the leached Protein A ELISA (AMV-3016)",
        "AMV-3017": "XMuLV titre is measured by an infectivity assay (AMV-3017)",
        "AMV-3018": "MVM titre by infectivity with a molecular confirmation (AMV-3018)",
    },
    True: {  # PCR-008 §3.3
        "AMV-3012": ("Pool host cell protein was measured by the process-specific ELISA "
                     "(AMV-3012) and is reported in nanograms per milligram of antibody"),
        "AMV-3014": ("Residual DNA and leached Protein A were measured in the pool by AMV-3014 "
                     "and AMV-3016 respectively"),
        "AMV-3016": ("Residual DNA and leached Protein A were measured in the pool by AMV-3014 "
                     "and AMV-3016 respectively"),
        "AMV-3017": "XMuLV and MVM titres were measured by infectivity assay (AMV-3017 and AMV-3018)",
        "AMV-3018": "XMuLV and MVM titres were measured by infectivity assay (AMV-3017 and AMV-3018)",
    },
}


def _ax_method_rows():
    """``{method id -> rendered row}`` of the controlled-document table (same in both documents).

    ``_pcpkg.sop_table`` builds this frame; the row carries the method number, its title and its
    type, which is the relation the AnalyticalMethod record states.
    """
    import pandas as pd
    rows = [[aid, title, "Method validation"] for aid, title in P.AEX_AMV_REFS]
    df = pd.DataFrame(rows, columns=["Reference", "Title", "Type"])
    return row_quotes(df, df["Reference"])


def _ax_perf_rows(report):
    """``{method id -> rendered row}`` of the validated-performance table.

    Only four of the six methods carry a performance record, so this supplements the
    controlled-document row rather than replacing it.
    """
    if report:
        df = P.method_perf_df(precision_with_unit=True)
        df = df[df["Method"].isin([a for a, _ in P.AEX_AMV_REFS])]
    else:
        df = P.method_perf_for(P.AEX_AMV_REFS, precision_with_unit=True)
    return row_quotes(df, df["Method"], P._auto_floatfmt(df))


def ax_methods(doc_id, file_name, sec, report):
    doc_rows, perf_rows = _ax_method_rows(), _ax_perf_rows(report)
    perf_sec = "Analytical methods summary" if report else "Analytical methods"
    out = []
    for mid, mname, mtype, analytes, attrs in AXMETHODS:
        src = [ref(doc_id, file_name, sec, "Related documents" if not report
                   else "Analytical methods", doc_rows[mid],
                   table_title="Controlled procedures and validated analytical methods",
                   table_id=f"{doc_id}_tab_sops")]
        if mid in perf_rows:
            src.append(ref(doc_id, file_name, sec, perf_sec, perf_rows[mid],
                           table_title="Validated performance of the analytical methods",
                           table_id=f"{doc_id}_tab_methods"))
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[AXATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=src, metadata=meta()))
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
                                   "The design estimates every main effect and every two-factor "
                                   "interaction without confounding" if report
                                   else "A full factorial was chosen in preference to a "
                                        "fractional design because a design in 4 factors is "
                                        "small enough to afford it")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:aex_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=AXUO_NAME,
            factors=AX_MULTIVARIATE, responses=responses,
            n_runs=n_rsm, n_center_points=P.doe_centre_points(AXUO, "rsm"), scale_down_model="scale-down chromatography column",
            associated_parameters=[AXPARAM_CONCEPT[f] for f in AX_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "The axial points sit on the faces of the cube rather than "
                                   "outside it, so the design does not require the step to be run "
                                   "beyond the characterization ranges" if report
                                   else "The axial points sit on the faces of the cube and not "
                                        "outside it")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:aex_sdm_qual", study_type="scale_down_qualification",
            unit_operation=AXUO_NAME, scale_down_model="scale-down chromatography column",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "The qualification compared the scale-down model with "
                                   "commercial-scale data on the attributes that enter and leave "
                                   "the step" if report
                                   else "Qualification will compare the model against commercial "
                                        "scale data at set-point conditions")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:aex_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=AXUO_NAME,
            factors=AX_UNIVARIATE,
            # PCP-008 commits to measuring the four study responses at each flow-rate setting.
            # PCR-008 reports NO effect estimate for flow rate on any governed attribute and
            # leaves the univariate runs in the study record, so the report attests no responses.
            responses=[] if report else
            ["flow-through-pool HCP", "XMuLV log-reduction", "MVM log-reduction", "step yield"],
            associated_parameters=[AXPARAM_CONCEPT[f] for f in AX_UNIVARIATE],
            source_references=[ref(doc_id, file_name, "Study design", "Univariate assessment",
                                   "Operating flow rate was assessed one factor at a time across "
                                   "its characterization range with the other parameters at their "
                                   "set-points" if report
                                   else "Operating flow rate will be assessed one factor at a "
                                        "time.")],
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


# Prospective risk basis. RA-001's output for this step is reproduced in the plan as a table
# whose row names the parameter, the failure mode, the attribute the failure would hit and the
# study type assigned. Each plan-side parameter->attribute edge is anchored on that row.
AX_RA_TARGET = {
    "Load pH": ["attr:hcp", "attr:lrv_mvm"],
    "Equil/Wash-1 conductivity": ["attr:hcp"],
    "Load conductivity": ["attr:lrv_mvm"],
    "Protein load": ["attr:hcp"],
}
# Demonstrated effects in the report. Each edge is anchored on the parameter's own row of the
# screening effect table AND on the sentence of the results section that states the finding.
AX_EFFECT_ROW = {
    ("Load pH", "mvm_lrf"): "load_ph",
    ("Load pH", "xmulv_lrf"): "load_ph",
    ("Load pH", "hcp_out_ng_mg"): "load_ph",
    ("Load conductivity", "mvm_lrf"): "load_cond",
    ("Load conductivity", "xmulv_lrf"): "load_cond",
    ("Equil/Wash-1 conductivity", "hcp_out_ng_mg"): "wash1_cond",
}


def _ax_top_effect_rows(response):
    """``{term -> rendered row}`` of the report's ``top_effects`` table for one response."""
    df = P.top_effects(AXUO, response)
    return row_quotes(df, df.iloc[:, 0], P._auto_floatfmt(df))


def _ax_acceptance_rows():
    """``{cqa key -> rendered row}`` of the plan's acceptance-criteria table.

    The row carries the response, the attribute, the criterion the study must meet and the
    basis of that criterion — all four ends of the relation the assertion states.
    """
    import doe_report as D
    df = D.acceptance_table(AXUO)
    by_name = row_quotes(df, df["Quality attribute"], P._auto_floatfmt(df))
    return {k: by_name[_ax_cqa_row(k)["cqa"]] for k in ("hcp", "lrv_xmulv", "lrv_mvm")}


def ax_assertions(doc_id, file_name, report):
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, refs):
        """``refs`` is a list of (section title, quote) pairs — never a shared caption."""
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, q) for sec, q in refs],
            metadata=meta()))

    param_sec, _ = AX_PARAM_TABLE[report]
    prows, crows = _ax_param_rows(report), _ax_cqa_rows(report)
    # step -> parameter, each on its own rendered parameter row (set-point, NOR, range).
    for name, cid in AXPARAM_CONCEPT.items():
        add("step:aex", "step_has_parameter", cid,
            f"{AXUO_NAME} has process parameter {name}.", [(param_sec, prows[name])])
    # The step SETS the cumulative MVM clearance claim.
    sets_quote = ("The step is assigned one critical quality attribute of its own, the clearance "
                  "of minute virus of mice, which the register rates of very high criticality."
                  if report else
                  "The cumulative clearance of MVM is assigned to this step in the drug substance "
                  "CQA register.")
    add("step:aex", "step_has_quality_attribute", "attr:lrv_mvm",
        f"{AXUO_NAME} sets the cumulative MVM (parvovirus) clearance claim.",
        [("Quality attributes in scope", sets_quote),
         ("Quality attributes in scope", crows["lrv_mvm"])])
    cleared_quote = ("The step also governs, or contributes to, four further attributes that are "
                     "set or formed elsewhere in the process." if report else
                     "The quality attributes this step governs are listed in")
    for key in ["lrv_xmulv", "hcp", "residual_dna", "leached_protein_a"]:
        add("step:aex", "step_has_quality_attribute", AXATTR_CONCEPT[key],
            f"{AXUO_NAME} clears {AXATTR_NAME[key]}.",
            [("Quality attributes in scope", cleared_quote),
             ("Quality attributes in scope", crows[key])])
    # attribute -> method. Both documents state the linkage; the controlled-document row is
    # carried alongside the prose so the record names the method number and its title too.
    mrows = _ax_method_rows()
    for key in AX_CQA_METHOD:
        mid = AX_CQA_METHOD[key]
        add(AXATTR_CONCEPT[key], "attribute_measured_by_method", f"method:{mid}",
            f"{AXATTR_NAME[key]} is measured by {mid}.",
            [("Analytical methods", AXMETHOD_QUOTE[report][mid]),
             ("Analytical methods" if report else "Related documents", mrows[mid])])
    # Acceptance criteria. The drug-substance criterion sits in the CQA row; the step-level
    # criterion the study is judged against is separate and is stated in both documents.
    mvm, hcp, xmulv = (_ax_cqa_row("lrv_mvm"), _ax_cqa_row("hcp"), _ax_cqa_row("lrv_xmulv"))
    if report:
        step_crit = {
            "lrv_mvm": ("Proven acceptable ranges",
                        "For MVM the cumulative requirement is 8.6 log10, the other credited "
                        "steps contribute 5.32 log10, and the requirement on this step is "
                        "therefore 3.28 log10"),
            "lrv_xmulv": ("Proven acceptable ranges", "For XMuLV the same calculation gives "
                                                      "3.78 log10"),
            "hcp": ("Proven acceptable ranges",
                    "For pool host cell protein the criterion is the drug substance "
                    "specification, an upper limit of 100 ng/mg"),
        }
    else:
        acc = _ax_acceptance_rows()
        step_crit = {k: ("Acceptance and decision criteria", acc[k]) for k in acc}
    add("attr:lrv_mvm", "attribute_has_acceptance_criterion", "lit:lrv_mvm_acc",
        f"MVM clearance acceptance is cumulative across the process: ≥ {mvm['acc_low']:g} "
        f"{mvm['unit']}; the contribution required of this step is back-calculated from it.",
        [("Quality attributes in scope", crows["lrv_mvm"]), step_crit["lrv_mvm"]])
    add("attr:lrv_xmulv", "attribute_has_acceptance_criterion", "lit:lrv_xmulv_acc",
        f"XMuLV clearance acceptance is cumulative across the process: ≥ {xmulv['acc_low']:g} "
        f"{xmulv['unit']}; the contribution required of this step is back-calculated from it.",
        [("Quality attributes in scope", crows["lrv_xmulv"]), step_crit["lrv_xmulv"]])
    add("attr:hcp", "attribute_has_acceptance_criterion", "lit:hcp_acc",
        f"Pool HCP is judged directly against the drug-substance specification of "
        f"≤ {hcp['acc_high']:g} {hcp['unit']}.",
        [("Quality attributes in scope", crows["hcp"]), step_crit["hcp"]])
    # parameter -> attribute relations.
    if report:
        # Demonstrated effects. Load pH and load conductivity govern both viral responses;
        # load pH and equil/wash-1 conductivity govern pool HCP.
        eff = {r: _ax_top_effect_rows(r)
               for r in ["mvm_lrf", "xmulv_lrf", "hcp_out_ng_mg"]}
        viral_quote = ("Both viral responses are governed by the load pH and the load "
                       "conductivity, and by neither of the other two factors.")
        hcp_quote = ("Pool host cell protein is governed by the equilibration and wash-1 "
                     "conductivity and by the load pH, and the two interact")
        for pname, resp, attr, txt in [
            ("Load pH", "mvm_lrf", "attr:lrv_mvm",
             "Load pH carries the largest effect on the MVM log reduction factor."),
            ("Load pH", "xmulv_lrf", "attr:lrv_xmulv",
             "Load pH carries the largest effect on the XMuLV log reduction factor."),
            ("Load conductivity", "mvm_lrf", "attr:lrv_mvm",
             "Load conductivity carries the second largest effect on the MVM log reduction "
             "factor, in the opposite direction to load pH."),
            ("Load conductivity", "xmulv_lrf", "attr:lrv_xmulv",
             "Load conductivity carries the second largest effect on the XMuLV log reduction "
             "factor, in the opposite direction to load pH."),
        ]:
            add(AXPARAM_CONCEPT[pname], "parameter_impacts_attribute", attr, txt,
                [("Screening: factor effects", viral_quote),
                 ("Screening: factor effects", eff[resp][AX_EFFECT_ROW[(pname, resp)]]),
                 ("Parameter classification", AX_CLASS_SENTENCE[pname])])
        for pname, txt in [
            ("Equil/Wash-1 conductivity",
             "Equilibration and wash-1 conductivity carries the largest effect on pool HCP."),
            ("Load pH",
             "Load pH carries the second largest effect on pool HCP, in the opposite direction "
             "to the wash-1 conductivity, and the two interact."),
        ]:
            add(AXPARAM_CONCEPT[pname], "parameter_impacts_attribute", "attr:hcp", txt,
                [("Screening: factor effects", hcp_quote),
                 ("Screening: factor effects",
                  eff["hcp_out_ng_mg"][AX_EFFECT_ROW[(pname, "hcp_out_ng_mg")]])])
        # Protein load: a resolved null over the studied range, and the report says so.
        add("param:aex_load", "parameter_does_not_significantly_impact_attribute", "attr:hcp",
            "No effect of protein load on any governed attribute was resolved in either design, "
            "which the report reads as evidence that the resin capacity for impurity binding is "
            "not approached anywhere in the studied load range.",
            [("Parameter classification", AX_CLASS_SENTENCE["Protein load"]),
             ("Mechanistic interpretation",
              "The absence of a protein load effect on any response is the most useful negative "
              "result of the study")])
        # Operating flow rate carries NO effect edge in this report. §4.4 states that no effect
        # estimate for it is reported and that its classification rests on mechanism and on the
        # control the skid applies, not on a measured effect. An earlier annex asserted that it
        # "showed no effect in the univariate assessment"; the report does not support that.
    else:
        rows = row_quotes(P.ra_scope(AXUO), P.ra_scope(AXUO)["Parameter"])
        attr_name = {"attr:hcp": "pool host cell protein",
                     "attr:lrv_mvm": "MVM clearance", "attr:lrv_xmulv": "XMuLV clearance"}
        for pname in AX_MULTIVARIATE:
            for attr in AX_RA_TARGET[pname]:
                add(AXPARAM_CONCEPT[pname], "parameter_impacts_attribute", attr,
                    f"RA-001 carried {pname} into the multivariate design on its prospective "
                    f"impact on {attr_name[attr]}; the effect is to be quantified by this study, "
                    f"not assumed.",
                    [("Risk-based prioritization of parameters", rows[pname])])
        # The flow-rate row of the risk table renders across a line break, so the parameter is
        # anchored on the mechanistic sentence that justifies its univariate assignment.
        add("param:aex_flow", "parameter_impacts_attribute", "attr:lrv_mvm",
            "Operating flow rate acts on this step through residence time and is assessed "
            "univariately for that reason.",
            [("Univariate assessment", "Flow rate acts on the separation through residence time")])
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def ax_report_sections(doc_id, file_name, report):
    from annex_contract.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-008 defines the process characterization study for the A-Mab anion-exchange "
                  "polishing step (Step 8), and it states no findings.",
               "Purpose and scope",
               "This plan defines the process characterization study for that step"),
            st(2, "Five process parameters will be characterized; four are studied in the "
                  "multivariate designs and the operating flow rate univariately.",
               "Factors, ranges and study type",
               "The parameters, their set-points, the ranges to be studied and the normal "
               "operating ranges are given in"),
            st(3, "The multivariate work is a two-level full-factorial screen followed by a "
                  "face-centred central-composite design in the same four factors.",
               "Response-surface design",
               "The response-surface study is a face-centred central composite design in the "
               "same 4 factors"),
            st(4, "The cumulative MVM clearance claim is assigned to this step, and the claim "
                  "rests on anion exchange and small-virus retentive filtration together, because "
                  "a parvovirus is not inactivated by the low-pH hold.",
               "Quality attributes in scope",
               "MVM is a non-enveloped parvovirus, so it is not inactivated by the low-pH hold at "
               "Step 6, and the claim rests on the anion exchange step and the small virus "
               "retentive filter together."),
            st(5, "No parameter of the step is left unstudied, so the study scope is the whole "
                  "parameter set of the unit operation.",
               "Risk-based prioritization of parameters",
               "No parameter of this step was left unstudied, so the study scope is the whole "
               "parameter set of the unit operation and not a filtered subset of it."),
            st(6, "The operating region will be declared acceptable only when the fitted "
                  "response-surface models predict every governed attribute inside its criterion "
                  "across the whole region.",
               "Acceptance and decision criteria",
               "The operating region will be declared acceptable when the fitted response-surface "
               "models predict every governed attribute inside its criterion across the whole "
               "region"),
            st(7, "The plan sets no numerical capability threshold; the report will argue each Cpk "
                  "from the margin to the limit and the criticality of the attribute.",
               "Statistical methods", "This plan sets no numerical capability threshold."),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Every parameter of the step is classified as a well-controlled critical process "
              "parameter; none is a CPP, and none is a KPP or GPP.",
           "Parameter classification",
           "Every parameter of the step is classified well controlled critical process parameter, "
           "and no parameter is classified critical process parameter."),
        st(2, "The design space is the whole characterized region in the four multivariate "
              "parameters, because no governed attribute cuts it back anywhere inside the ranges "
              "studied.",
           "Design space",
           "The design space for this step is the whole characterized region in the 4 "
           "multivariate parameters"),
        st(3, "Pool host cell protein is governed by equilibration/wash-1 conductivity and load pH "
              "acting in opposite directions, together with a significant interaction between "
              "them.",
           "Screening: factor effects",
           "Pool host cell protein is governed by the equilibration and wash-1 conductivity and "
           "by the load pH, and the two interact"),
        st(4, "The response-surface models for pool HCP and for both viral responses describe "
              "their responses adequately and are the predictive basis of the design space; the "
              "screening models are not.",
           "Response-surface models",
           "The response-surface models describe the three governed responses adequately and are "
           "the predictive basis of the design space"),
        st(5, "The protein-load main effect and the protein-load x wash-conductivity interaction "
              "seen in the invalidated first execution do not survive in the requalified data, "
              "which confirms the DEV-008-01 root cause.",
           "DEV-008-01: non-representative load in the first execution",
           "Competition for a finite number of binding sites is exactly what produces a load by "
           "conductivity interaction, and its disappearance when the competing species are "
           "removed confirms the root cause"),
        st(6, "Three deviations were recorded and closed; one invalidated the first execution of "
              "both designs, and none of the three changed a parameter classification or the "
              "operating region.",
           "Conclusions",
           "3 deviations were recorded and closed. One invalidated the first execution of both "
           "designs, which were re-executed in full, and none of the three changed a parameter "
           "classification or the operating region."),
        st(7, "The cumulative MVM clearance carries the tightest process-capability index of any "
              "A-Mab drug substance attribute.",
           "Process capability and robustness",
           "The cumulative MVM clearance is the tightest capability in Table 19 and the tightest "
           "of any A-Mab drug substance attribute, with a Cpk of 1.51"),
        st(8, "The step does not deliver the cumulative MVM requirement on its own: the claim is "
              "shared with small-virus retentive filtration, and low-pH inactivation contributes "
              "nothing against a parvovirus.",
           "Contribution to the control strategy",
           "Against MVM the low-pH step contributes nothing, so the cumulative claim of 10.03 "
           "log10 rests on this step and the virus filter together"),
        st(9, "No effect estimate for operating flow rate is reported; its classification rests on "
              "the mechanism and on the control the skid applies, not on a measured effect.",
           "Parameter classification",
           "Operating flow rate is a well controlled critical process parameter. It was assessed "
           "univariately, and this report presents no effect estimate for it"),
    ])]


def ax_design_spaces(doc_id, file_name):
    # PCR-008 §6 declares the design space to be the WHOLE characterized region in all four
    # multivariate parameters — no attribute cuts it back — and states explicitly that the worst
    # case is NOT one of its corners: the MVM surface carries positive squared terms, so its
    # minimum lies inside the box. An earlier annex asserted an intersection of two constraints
    # in three parameters with a worst-case corner; the report contradicts both.
    return [S.DesignSpace(
        design_space_id="ds:aex", unit_operation=AXUO_NAME,
        parameters=["param:aex_load_ph", "param:aex_wash1_cond", "param:aex_load_cond",
                    "param:aex_load"],
        quality_attributes_constrained=["attr:lrv_mvm", "attr:lrv_xmulv", "attr:hcp"],
        definition="The whole characterized region in the four multivariate parameters. Every "
                   "governed attribute is predicted to meet its acceptance criterion everywhere "
                   "in it, so no attribute cuts the region back inside the ranges studied. The "
                   "region has two principal planes: viral clearance governed by load pH and load "
                   "conductivity, and pool HCP governed by load pH and equilibration/wash-1 "
                   "conductivity. Protein load appears in neither and enters only as the range "
                   "over which the other three were studied. MVM clearance is the binding "
                   "attribute, and its worst case is not a corner — the lowest predicted value "
                   "lies inside the region, found by a refined grid search. The claim is a "
                   "statement about mean response levels on a qualified scale-down model.",
        source_references=[
            ref(doc_id, file_name, "Design space", "Design space",
                "The design space for this step is the whole characterized region in the 4 "
                "multivariate parameters"),
            ref(doc_id, file_name, "Design space", "Design space",
                "The MVM model carries positive squared terms in the equilibration and wash-1 "
                "conductivity and in the protein load")],
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
# Per-CQA grounded fragment stating the acceptance BASIS, from §7 of the report. The record
# itself is anchored on its own rendered @tbl-par row; this sentence is the second reference,
# and it is the one that carries the basis field.
AX_PAR_BASIS_QUOTE = {
    False: ("For pool host cell protein the criterion is the drug substance specification, an "
            "upper limit of 100 ng/mg"),
    True: ("For the two viral attributes the drug substance criterion is a cumulative log "
           "reduction across the process, so the criterion that applies to this step is the "
           "required step contribution, obtained by subtracting the clearance credited to the "
           "other steps from the cumulative requirement"),
}


def ax_proven_acceptable_ranges(doc_id, file_name):
    """One ProvenAcceptableRange per governed CQA x response-surface parameter, from the
    same DoE engine (``doe_report.par_table``) that renders @tbl-par in the report. Pool HCP
    uses the drug-substance specification as its ceiling; the two viral-clearance CQAs use a
    back-calculated step floor (the modular required log-reduction) as the acceptance basis.

    Each record is anchored on ITS OWN rendered row, which carries the attribute, the parameter,
    the characterization range and both PAR columns — the whole relation in one span.
    """
    import doe_report as D
    par = D.par_table(AXUO)
    rows = _md_rows(par, P._auto_floatfmt(par))
    out = []
    for i, (r, row) in enumerate(zip(par.to_dict("records"), rows), 1):
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
            source_references=[
                ref(doc_id, file_name, f"{doc_id}_sec_par", AX_PAR_SEC, row,
                    table_title="Proven acceptable ranges per governed attribute and parameter, "
                                "from both analyses.",
                    table_id=f"{doc_id}_tab_par"),
                ref(doc_id, file_name, f"{doc_id}_sec_par", AX_PAR_SEC,
                    AX_PAR_BASIS_QUOTE[viral])],
            metadata=meta()))
    return out


# Argument-structure spans over the PCR-008 report. Each quote is a verbatim, plain-prose
# fragment of the rendered report (no inline expressions, no bold). Tuple fields:
# (suffix, role, section, quote, supported_by-suffixes, restates-suffix, bounds-suffix).
AX_RHET_SPANS = [
    # --- Executive summary: the whole-document claim and what carries it ----------------
    ("R00", "claim", "Executive summary",
     "Every governed attribute meets its acceptance criterion everywhere in the characterized "
     "region", ["R01", "R02"], None, None),
    ("R01", "justification", "Executive summary",
     "There the fitted model predicts an MVM log reduction factor of 3.50 against a step "
     "requirement of 3.28 log10, a margin of about 0.7 residual standard deviations of the model",
     [], None, None),
    ("R02", "justification", "Executive summary",
     "The normal operating range sits well inside that region, and the lowest MVM log reduction "
     "factor predicted anywhere inside it is 4.19", [], None, None),
    ("R03", "problem_statement", "Executive summary",
     "The critical quality attribute assigned to this step is the clearance of minute virus of "
     "mice (MVM), which the drug substance register rates of very high criticality",
     [], None, None),
    ("R04", "claim", "Executive summary",
     "All of them are classified as well controlled critical process parameters. The step has no "
     "critical process parameter and no key process parameter.", ["R19"], None, None),
    ("R05", "cross_step_credit", "Executive summary",
     "Small virus retentive filtration (PCR-009) contributes the larger single increment to the "
     "cumulative claim, and the two mechanisms are independent of each other", [], None, None),
    ("R06", "deviation_disposition", "Executive summary",
     "The load material used in that execution had an out of trend acidic charge variant content, "
     "the designs were re-executed in full on a requalified load, and the analysis reported here "
     "is the re-executed one", [], None, None),
    ("R07", "deferral", "Executive summary",
     "The outcome of this report rolls up into the master report (PCMR-001)", [], None, None),
    # --- Screening: what the design can and cannot carry ---------------------------------
    ("R08", "problem_statement", "Screening design",
     "The design is nonetheless near-saturated, spending most of its degrees of freedom on the "
     "model and leaving few for residual error, so the residual is estimated from few degrees of "
     "freedom and the adequacy statistics that depend on it are unstable", [], None, None),
    ("R09", "claim", "Screening: factor effects",
     "Pool host cell protein is governed by the equilibration and wash-1 conductivity and by the "
     "load pH, and the two interact", ["R10", "R12"], None, None),
    ("R10", "justification", "Screening: factor effects",
     "Raising the wash-1 conductivity across its studied range raised pool host cell protein by "
     "12.1 ng/mg (p < 0.001). Raising the load pH across its studied range lowered it by 11.9 "
     "ng/mg (p < 0.001).", [], None, None),
    ("R11", "mechanistic_warrant", "Mechanistic interpretation",
     "That is why host cell protein responds to the conductivity of the equilibration and wash-1 "
     "buffer while virus does not", [], None, None),
    ("R12", "mechanistic_warrant", "Mechanistic interpretation",
     "At low wash conductivity the weakly bound host cell protein species stay on the column "
     "whatever the load pH was, so the pH effect is muted. At high wash conductivity those species "
     "are displaced into the pool, and the load pH then decides how strongly they were bound in "
     "the first place.", [], None, None),
    ("R13", "bounded_conclusion", "Screening: factor effects",
     "The screening design identifies the active factors. The response-surface model in §5.3 is "
     "the predictive model and the basis of the design space.", [], None, "R09"),
    ("R14", "deferral", "Screening: factor effects",
     "All 4 are retained in the knowledge space, and the full effect table is in Appendix C",
     [], None, None),
    # --- Response-surface adequacy -------------------------------------------------------
    ("R15", "claim", "Response-surface models",
     "The response-surface models describe the three governed responses adequately and are the "
     "predictive basis of the design space", ["R16", "R17"], None, None),
    ("R16", "justification", "Response-surface models",
     "For the three governed responses the coefficient of determination lies between 0.898 and "
     "0.934, the adjusted value does not fall below 0.787, and every model F test is significant",
     [], None, None),
    ("R17", "justification", "Response-surface models",
     "In both cases the lack of fit mean square is of the same order as the pure error mean "
     "square. The quadratic surface therefore describes the data no worse than replicate runs "
     "describe each other, which is the condition under which a response surface may be used to "
     "interpolate.", [], None, None),
    ("R18", "hedge", "Response-surface models",
     "The predicted coefficient of determination is lowest for MVM at 0.394", [], None, None),
    ("R19", "justification", "Parameter classification",
     "That risk is low for every parameter here, because the design space extends to the full "
     "characterized range and the normal operating ranges in Table 6 sit inside it",
     [], None, None),
    ("R20", "hedge", "Centre-point performance and reproducibility",
     "The centre-point standard deviation for MVM is 0.34 log10, which is of the same order as "
     "the assay itself, so it bounds the step’s own variation in MVM clearance and does not "
     "measure it", [], None, None),
    # --- Design space --------------------------------------------------------------------
    ("R21", "claim", "Design space",
     "The design space for this step is the whole characterized region in the 4 multivariate "
     "parameters", ["R22", "R23"], None, None),
    ("R22", "justification", "Design space",
     "There the model predicts an MVM log reduction factor of 3.50 against the step requirement "
     "of 3.28 log10 derived in §7, and an XMuLV log reduction factor of 5.00 against 3.78 log10",
     [], None, None),
    ("R23", "justification", "Design space",
     "Searching the normal operating box the same way, the lowest predicted MVM log reduction "
     "factor is 4.19, a margin of 0.91 log10 or about 2.8 residual standard deviations",
     [], None, None),
    ("R24", "mechanistic_warrant", "Design space",
     "The MVM model carries positive squared terms in the equilibration and wash-1 conductivity "
     "and in the protein load", [], None, None),
    ("R25", "bounded_conclusion", "Design space",
     "Three bounds apply to this claim and none of them is removable by more analysis of these "
     "data", [], None, "R21"),
    ("R26", "bounded_conclusion", "Response-surface models",
     "It is the reason the design space claim in §6 is stated at the level of the mean response "
     "and is not extended to an assurance statement at the edge of the region", [], None, "R21"),
    # --- Proven acceptable ranges --------------------------------------------------------
    ("R27", "claim", "Proven acceptable ranges",
     "For every attribute and every parameter the two analyses agree, and both span the full "
     "characterization range", [], None, None),
    ("R28", "bounded_conclusion", "Proven acceptable ranges",
     "Since no univariate proven acceptable range is binding, the constraint on the operating "
     "region is the multivariate worst case identified in §6 and not any single parameter limit "
     "in Table 18", [], None, "R27"),
    # --- Capability ----------------------------------------------------------------------
    ("R29", "claim", "Process capability and robustness",
     "The cumulative MVM clearance is the tightest capability in Table 19 and the tightest of any "
     "A-Mab drug substance attribute, with a Cpk of 1.51", ["R30"], None, None),
    ("R30", "justification", "Process capability and robustness",
     "Its simulated mean is 10.38 log10 with a standard deviation of 0.40, against a requirement "
     "of 8.6 log10, and the lowest simulated batch was 9.08 log10", [], None, None),
    ("R31", "cross_step_credit", "Process capability and robustness",
     "Of the cumulative 10.03 log10 of MVM clearance, this step is credited with 4.71 log10 and "
     "small virus retentive filtration with 5.32 log10 (PCR-009)", [], None, None),
    ("R32", "bounded_conclusion", "Process capability and robustness",
     "It is a prediction to be confirmed at commercial scale during process performance "
     "qualification, which has not been executed", [], None, "R29"),
    # --- The protein-load null result ----------------------------------------------------
    ("R33", "claim", "Mechanistic interpretation",
     "The absence of a protein load effect on any response is the most useful negative result of "
     "the study", ["R34"], None, None),
    ("R34", "mechanistic_warrant", "Mechanistic interpretation",
     "If the resin capacity for impurity binding were being approached at the top of the load "
     "range, the clearance responses would fall and the effect would appear as an interaction "
     "between load and conductivity. No such term is significant in either design.",
     [], None, None),
    ("R35", "bounded_conclusion", "Mechanistic interpretation",
     "The one caveat is that the studied range is bounded, and this study says nothing about "
     "loads above its upper edge", [], None, "R33"),
    # --- Control strategy and discussion --------------------------------------------------
    ("R36", "cross_step_credit", "Contribution to the control strategy",
     "Against MVM the low-pH step contributes nothing, so the cumulative claim of 10.03 log10 "
     "rests on this step and the virus filter together", [], None, None),
    ("R37", "deferral", "Contribution to the control strategy",
     "The consolidated claim is reported in PCMR-001", [], None, None),
    ("R38", "problem_statement", "Discussion",
     "The interaction is the one expectation the study did not meet.", [], None, None),
    ("R39", "bounded_conclusion", "Discussion",
     "Three limitations bound what the report claims.", [], None, None),
    # --- Deviations ------------------------------------------------------------------------
    ("R40", "claim", "DEV-008-01: non-representative load in the first execution",
     "Competition for a finite number of binding sites is exactly what produces a load by "
     "conductivity interaction, and its disappearance when the competing species are removed "
     "confirms the root cause", ["R41"], None, None),
    ("R41", "justification", "DEV-008-01: non-representative load in the first execution",
     "The protein load effect falls from 35.6 ng/mg (p = 0.002) to 0.9 ng/mg (p = 0.491), and the "
     "interaction between protein load and wash-1 conductivity falls from 34.8 ng/mg (p = 0.002) "
     "to 0.2 ng/mg (p = 0.860)", [], None, None),
    ("R42", "deviation_disposition", "DEV-008-01: non-representative load in the first execution",
     "The disposition was to invalidate both designs for the purpose of defining the operating "
     "region and to re-execute them in full on a requalified, representative load", [], None, None),
    ("R43", "deviation_disposition", "DEV-008-02: pool collection set-point on the trailing edge",
     "The disposition is that the corrected set-point is fixed in the batch record and the "
     "reported operating region is unchanged", [], None, None),
    ("R44", "hedge", "DEV-008-02: pool collection set-point on the trailing edge",
     "The verification therefore confirms that the corrected set-point produces host cell protein "
     "of the same order as the models predict, and it does not resolve a difference smaller than "
     "that half-width", [], None, None),
    ("R45", "deviation_disposition",
     "DEV-008-03: equilibration and wash-1 buffer released below its pH range",
     "The disposition is retained without adjustment, a corrective action was raised against the "
     "buffer preparation procedure", ["R46"], None, None),
    ("R46", "justification",
     "DEV-008-03: equilibration and wash-1 buffer released below its pH range",
     "Lower pH reduces both viral clearance and host cell protein clearance, which means the "
     "excursion biases the affected run towards worse apparent performance and cannot flatter the "
     "result", [], None, None),
    # --- Conclusions ------------------------------------------------------------------------
    ("R47", "restatement", "Conclusions",
     "The design space is the full characterized region.", [], "R21", None),
    ("R48", "bounded_conclusion", "Conclusions",
     "Confirmation at commercial scale is a Stage 2 activity and has not been performed",
     [], None, "R47"),
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
        weak_claims=build_weak_claims(doc, f),
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "AEX sets one CQA (cumulative MVM clearance); the other QualityAttribute entities are the CQAs it controls/clears (formed/introduced upstream). The plan renders all five in one table.",
            "Flow-through-pool HCP and step-LRF are in-process/modular responses; captured via StudyDesign.responses.",
            "The Plan states classification is an OUTPUT; parameter_type left 'unclassified' here.",
            "Every entity and assertion is anchored on its own rendered table row where the document renders one (parameters, CQAs, methods, risk-assessment scope, acceptance criteria); prose anchors are used only for relations no table carries.",
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
        weak_claims=build_weak_claims(doc, f),
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT + [
            "ProvenAcceptableRange (new model) — per-CQA x parameter PAR (at-set-point / NOR-propagated); the viral CQAs use a back-calculated step floor",
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "AEX sets one CQA (cumulative MVM clearance); the other QualityAttribute entities are the CQAs it controls/clears. The report splits them across @tbl-cqa-set and @tbl-cqa-scope, and each attribute is anchored on its own row.",
            "Three deviations (DEV-008-01 non-representative deamidated-load re-execution; DEV-008-02 permissive UV pool-stop corrected by modelling + verification runs; DEV-008-03 out-of-range wash-buffer lot retained) are narrative; the annex captures the DoE-grounded entities and the requalified-load results reported.",
            "Process-capability (Cpk) values have no dedicated field; reported as report_sections statements.",
            "The design space is the WHOLE characterized region in all four multivariate parameters; §6 states that the worst case is not one of its corners, so no corner is recorded as the binding condition.",
            "Operating flow rate carries NO parameter->attribute assertion: §4.4 reports no effect estimate for it, and §9 classifies it on mechanism and control capability rather than on a measured effect.",
            "proven_acceptable_ranges mirror @tbl-par (doe_report.par_table), one record per rendered row; rhetorical_spans are verbatim report prose; PCR-008 carries no weak_claims.",
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
# filtration pressure. The 2^2 screen is a FULL factorial, so nothing is aliased, #
# but the report is explicit that the factorial part is exactly saturated: the    #
# residual degrees of freedom come from the centre points alone, the standard     #
# errors are wide and NONE of the three screening models is significant overall.  #
# The response-surface model is the predictive model. Load is the only resolved   #
# effect (MVM clearance falls with load, reported adverse-first and then          #
# bounded); XMuLV clearance and step yield are null results whose fits are NOT    #
# used predictively. Both parameters are WC-CPP — load because it is              #
# quality-linked to MVM clearance, pressure because the null result is the        #
# evidence for the class and the filter must stay inside the window in which its  #
# retention was established. The design space is the whole characterized region.  #
# No univariate parameter.                                                        #
#                                                                                 #
# Re-anchored 2026-07-28 against the re-authored PCP-009 / PCR-009. Every record   #
# that states a table relation is anchored on its OWN rendered row (row_quotes);   #
# the prose anchors were re-read from the rendered .docx.                          #
# =========================================================================== #
VFUO = "virus_filtration"
VFUO_NAME = P.UNIT_OP_TITLES[VFUO]               # "Small-Virus Retentive Filtration" (rendered)
VFUO_CSV = P.CFG.unit_op(VFUO).name              # "Small Virus Retentive Filtration" (CSV only)
VFSTEP = P.CFG.unit_op(VFUO).step                # 9
VFSTEP_LABEL = f"{VFUO_NAME} (Step {VFSTEP})"

PCP9_FILE = "PCP-009_virus_filtration.docx"
PCR9_FILE = "PCR-009_virus_filtration.docx"

VFPARAM_ROWS = P.param_reg[P.param_reg.unit_operation == VFUO_CSV].to_dict("records")
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
        # Two references: the sentence that places the step in the train, and the sentence
        # that names its load and its product — the two ends of input_materials /
        # output_materials, which a single "the step removes virus" sentence would not carry.
        src = [ref(doc_id, file_name, sec, "Product and unit operation",
                   "Small-virus retentive filtration is Step 9 of the drug substance process, "
                   "and it sits between the final chromatographic polish and formulation."),
               ref(doc_id, file_name, sec, "Product and unit operation",
                   "It receives the anion exchange flow-through pool as its load")]
    else:
        src = [ref(doc_id, file_name, sec, "Unit-operation description and prior knowledge",
                   "The anion exchange pool is passed through a pre-wetted small virus "
                   "retentive filter, the filter is chased with buffer to recover the product "
                   "held up in the device, and the filter is integrity tested after use "
                   "(SOP-2012).")]
    return S.ProcessStep(
        step_id="step:virus_filtration", step_name=VFUO_NAME, step_number=str(VFSTEP),
        unit_operation=VFUO_NAME,
        # The report may rank the step's contribution, because @tbl-vc gives the step-by-step
        # split. The plan is written before any data exist, so its description states the role
        # the step is being characterized for and not an outcome of the study it plans.
        description=("Small-virus retentive (size-exclusion) filtration: the dedicated "
                     "virus-removal step. Retains virus larger than the membrane rating while "
                     "the antibody monomer transmits. Sets no product-quality CQA; it is the "
                     "largest single contributor to the cumulative MVM (parvovirus) "
                     "log-reduction and a contributor to the enveloped-virus (XMuLV) "
                     "log-reduction, credited as orthogonal/modular clearance under "
                     "ICH Q5A(R2)." if report else
                     "Small-virus retentive (size-exclusion) filtration: the dedicated "
                     "virus-removal step. Retains virus larger than the membrane rating while "
                     "the antibody monomer transmits. Sets no product-quality CQA; it "
                     "contributes to the cumulative MVM (parvovirus) and enveloped-virus "
                     "(XMuLV) log-reductions, credited as orthogonal/modular clearance under "
                     "ICH Q5A(R2). The size of each contribution is what the planned study "
                     "quantifies."),
        input_materials=["anion-exchange flow-through pool (virus-filtration feed)"],
        output_materials=["virus-filtration pool (UF/DF feed)"],
        equipment=["small-virus retentive filter", "scale-down filtration model"],
        source_references=src, metadata=meta())


def vf_equipment(doc_id, file_name, sec, report):
    sdm = S.Equipment(
        equipment_id="equip:vf_sdm", equipment_name="scale-down filtration model",
        equipment_type="virus filtration (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Scale-down model and its qualification",
                               "All characterization runs were executed on a qualified scale-down "
                               "model of the commercial filtration step, operated under SOP-2012 "
                               "and qualified under SOP-1001." if report
                               else "The clearance claim rests entirely on a scale-down model, "
                                    "because virus cannot be introduced into a manufacturing "
                                    "batch.")],
        metadata=meta())
    if report:
        return [sdm]
    return [
        S.Equipment(equipment_id="equip:vf_filter",
                    equipment_name="commercial-scale small-virus retentive filter",
                    equipment_type="virus-retentive filter", site_name=P.RECEIVING_SITE,
                    source_references=[ref(doc_id, file_name, sec,
                                           "Scale-down model and its qualification",
                                           "the same membrane chemistry, the same retentive "
                                           "structure and the same housing geometry as the "
                                           "commercial filter")],
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


# The report's classification section argues each parameter separately, and the two arguments
# are different in kind: load is classified on a demonstrated effect, pressure on a bounded
# null result. Each classified parameter therefore carries its own classification sentence as a
# second reference, alongside its rendered @tbl-params row.
VF_CLASS_SENTENCE = {
    "Filtration volume (load)": (
        "Filtration volume (load), WC-CPP. It has a demonstrated and quantified effect on MVM "
        "clearance, which is a very high criticality attribute, so it cannot be a general "
        "process parameter."),
    "Filtration pressure": (
        "Filtration pressure, WC-CPP. No effect of pressure on any response reached significance "
        "over 8–30 psi, and that null result is the evidence for the class, not an absence of "
        "evidence."),
}
# The common part of the classification argument, stated once in the report (§9).
VF_WC_CPP_RATIONALE = (
    "Each is linked to a critical quality attribute, and each has a low risk of leaving the "
    "design space in routine operation: the load is fixed when the filter area is chosen for a "
    "batch and does not drift during operation, and the pressure is easy to control and is "
    "monitored continuously.")


def vf_params(doc_id, file_name, sec, classified):
    caption = ("Process parameters of the step, with normal operating range, characterization "
               "range and final classification."
               if classified else
               "Parameters, ranges and study type for the planned characterization.")
    # Anchor each parameter on its own rendered row of @tbl-params, so the span carries the
    # parameter together with the set-point, the ranges and (in the report) the classification
    # the record states. The caption grounds too, but one caption cannot attest two rows.
    df = P.report_params(VFUO) if classified else P.plan_params(VFUO)
    rows = row_quotes(df, df["Parameter"], P._auto_floatfmt(df))
    out = []
    for r in VFPARAM_ROWS:
        name = r["parameter"]
        ptype = r["classification"] if classified else "unclassified"
        src = [ref(doc_id, file_name, sec,
                   "Factors, ranges and the knowledge space" if classified
                   else "Factors, ranges and study type",
                   rows[name], table_title=caption, table_id=f"{doc_id}_tab_params")]
        if classified:
            src.append(ref(doc_id, file_name, sec, "Parameter classification",
                           VF_CLASS_SENTENCE[name]))
        out.append(S.ProcessParameter(
            parameter_id=VFPARAM_CONCEPT[name], parameter_name=name, parameter_type=ptype,
            unit=r["unit"], target_value=f"{r['setpoint']:g}",
            NOR=f"{r['nor_low']:g}–{r['nor_high']:g} {r['unit']}",
            PAR=f"{r['par_low']:g}–{r['par_high']:g} {r['unit']}",
            associated_step=VFSTEP_LABEL,
            rationale_for_criticality=VF_WC_CPP_RATIONALE if classified else None,
            source_references=src, metadata=meta()))
    return out


# Both documents render the two viral-clearance CQAs from the same register call, so both can
# anchor each CQA on its OWN rendered row: the span then carries the attribute together with
# the cumulative acceptance criterion and the Tool #1 criticality the record states.
VF_CQA_CAPTION = {
    True: "Quality attributes governed by the step, from the drug-substance CQA register.",
    False: "Critical quality attributes to which this step contributes.",
}


def _vf_cqa_rows():
    df = P.cqas_by_keys(VF_CQA_KEYS)
    return row_quotes(df, VF_CQA_KEYS, P._auto_floatfmt(df))


def vf_cqas(doc_id, file_name, sec, report):
    caption = VF_CQA_CAPTION[report]
    rows = _vf_cqa_rows()
    out = []
    for key in VF_CQA_KEYS:
        r = _vf_cqa_row(key)
        out.append(S.QualityAttribute(
            attribute_id=VFATTR_CONCEPT[key], attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"],
            acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            # Both documents name the validated method for each attribute — the plan in §5.3,
            # the report in @tbl-analyte, which pairs each method with the response it supplies.
            analytical_method=VF_CQA_METHOD[key],
            associated_steps=[VFSTEP_LABEL],
            rationale_for_criticality=f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = {r['tool1_score']}.",
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref(doc_id, file_name, sec, "Quality attributes in scope",
                                   rows[key], table_title=caption,
                                   table_id=f"{doc_id}_tab_cqa")],
            metadata=meta()))
    return out


# Per-method grounded fragment stating which analyte each method titrates. Both documents make
# the linkage in one sentence of "Analytical methods"; these are the two halves of it, so the
# span carries the method and its analyte together.
VFMETHOD_QUOTE = {
    False: {  # PCP-009 §5.3
        "AMV-3018": "MVM titre is measured by TCID50 with qPCR confirmation (AMV-3018)",
        "AMV-3017": "XMuLV titre by TCID50 (AMV-3017)",
    },
    True: {  # PCR-009 §3.3
        "AMV-3018": ("MVM titre is determined by AMV-3018, which combines a TCID50 endpoint "
                     "assay with a qPCR confirmation"),
        "AMV-3017": "XMuLV titre is determined by AMV-3017, a TCID50 endpoint assay",
    },
}
# The report pairs method, analyte and reported response in @tbl-analyte; the plan states the
# validated performance of each method in @tbl-methods. Each AnalyticalMethod entity is anchored
# on its own row of whichever table its document renders.
VF_ANALYTE = {
    "AMV-3018": ("Minute virus of mice (MVM)", "MVM LRF"),
    "AMV-3017": ("Xenotropic murine leukaemia virus (XMuLV)", "XMuLV LRF"),
}
VFMETHOD_TABLE = {
    True: ("Validated analytical methods and the response each supplies.", "tab_analyte"),
    False: ("Validated performance of the analytical methods used for the study.", "tab_methods"),
}


def _vf_method_rows(report):
    """``{method id -> rendered row}`` of the method table each document renders."""
    if report:
        import pandas as pd
        df = pd.DataFrame(
            [[mid, title, VF_ANALYTE[mid][0], VF_ANALYTE[mid][1]]
             for mid, title in P.VIRUS_FILT_AMV_REFS],
            columns=["Method", "Title", "Analyte", "Reported response"])
    else:
        df = P.method_perf_for(P.VIRUS_FILT_AMV_REFS, precision_with_unit=True)
    return row_quotes(df, df["Method"], P._auto_floatfmt(df))


def vf_methods(doc_id, file_name, sec, report):
    rows = _vf_method_rows(report)
    caption, tid = VFMETHOD_TABLE[report]
    out = []
    for mid, mname, mtype, analytes, attrs in VFMETHODS:
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[VFATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=[ref(doc_id, file_name, sec, "Analytical methods", rows[mid],
                                   table_title=caption, table_id=f"{doc_id}_{tid}")],
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
            # The sentence carries the design type, the centre-point count and the run count,
            # which are the three fields the record states.
            source_references=[ref(doc_id, file_name, sec, "Screening design",
                                   "The screening design is a two-level full factorial in the two "
                                   "parameters, augmented with 3 centre points, giving 7 runs in "
                                   "total." if report
                                   else "The screening study is a full factorial in the 2 factors "
                                        "at two levels, augmented with 3 replicated centre "
                                        "points, giving 7 runs")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vf_rsm", study_type="response_surface_doe",
            design_name="face-centred central-composite design", unit_operation=VFUO_NAME,
            factors=VF_MULTIVARIATE, responses=responses,
            n_runs=n_rsm, n_center_points=P.doe_centre_points(VFUO, "rsm"), scale_down_model="scale-down filtration model",
            associated_parameters=[VFPARAM_CONCEPT[f] for f in VF_MULTIVARIATE],
            source_references=[ref(doc_id, file_name, sec, "Response-surface design",
                                   "The response-surface design is a face-centred central "
                                   "composite design in the same two parameters, with 4 centre "
                                   "points and 12 runs." if report
                                   else "The response-surface study is a face-centred central "
                                        "composite design in the same 2 factors, with 19 runs "
                                        "across the two stages and 12 runs in this one")],
            metadata=meta()),
        S.StudyDesign(
            study_id="study:vf_sdm_qual", study_type="scale_down_qualification",
            unit_operation=VFUO_NAME, scale_down_model="scale-down filtration model",
            source_references=[ref(doc_id, file_name, "Materials and methods",
                                   "Scale-down model and its qualification",
                                   "Qualification compared the scale-down device with "
                                   "commercial-scale data at the target condition, using flux "
                                   "decay across the filtration, filtrate quality and step yield "
                                   "as the performance measures." if report
                                   else "Qualification will compare the small-scale system "
                                        "against commercial-scale data on three points: the flux "
                                        "profile through the load, product recovery, and the "
                                        "quality of the filtrate.")],
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

    def add(subj, pred, obj, text, sec, quote, quote2=None):
        n[0] += 1
        quotes = [quote] + ([quote2] if quote2 else [])
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, q) for q in quotes],
            metadata=meta()))

    import doe_report as D
    cqa_rows = _vf_cqa_rows()

    # step -> parameter. The report names each parameter in §3.2 with what the operator sets, so
    # the span carries both ends of the relation; the plan has no equivalent sentence, so each
    # parameter is anchored on its own rendered @tbl-params row.
    plan_pdf = P.plan_params(VFUO)
    plan_param_rows = row_quotes(plan_pdf, plan_pdf["Parameter"], P._auto_floatfmt(plan_pdf))
    report_param_quote = {
        "Filtration volume (load)": ("The volumetric load is fixed by the batch volume and the "
                                     "installed membrane area, and it is the quantity the "
                                     "operator manages when the filter area is selected for a "
                                     "batch."),
        "Filtration pressure": "The filtration pressure is set at the start of the filtration and held",
    }
    for name, cid in VFPARAM_CONCEPT.items():
        add("step:virus_filtration", "step_has_parameter", cid,
            f"{VFUO_NAME} has process parameter {name}.",
            "Operation" if report else "Factors, ranges and study type",
            report_param_quote[name] if report else plan_param_rows[name])
    # step -> scale-down model. Every clearance number in either document is conditional on it.
    add("step:virus_filtration", "step_uses_equipment", "equip:vf_sdm",
        "Viral clearance is measured on a qualified scale-down spiking model, because virus "
        "cannot be introduced into a manufacturing batch." if report
        else "The planned clearance runs are executed on a scale-down model that must be "
             "qualified against commercial-scale data before the study starts.",
        "Scale-down model and its qualification",
        "All characterization runs were executed on a qualified scale-down model of the "
        "commercial filtration step, operated under SOP-2012 and qualified under SOP-1001."
        if report
        else "The clearance claim rests entirely on a scale-down model, because virus cannot be "
             "introduced into a manufacturing batch.")
    # step -> viral-clearance attributes. The REPORT can say which contribution is the largest,
    # because @tbl-vc gives the step-by-step split; the PLAN is written before any data exist
    # and says only that MVM sets the retention challenge and XMuLV is expected to be retained
    # with a wide margin. The plan record must not borrow the report's finding.
    add("step:virus_filtration", "step_has_quality_attribute", "attr:lrv_mvm",
        f"{VFUO_NAME} is the largest single contributor to the cumulative MVM (parvovirus) "
        f"clearance claimed for A-Mab drug substance." if report
        else f"MVM sets the retention challenge for {VFUO_NAME}: it is the smallest model virus, "
             f"and the step is studied against it.",
        "Executive summary" if report else "Unit-operation description and prior knowledge",
        "it is the largest single contributor to the parvovirus clearance claimed for A-Mab "
        "drug substance" if report
        else "MVM is the smallest of the model viruses used for a monoclonal antibody process, "
             "and it therefore sets the retention challenge for this step.")
    add("step:virus_filtration", "step_has_quality_attribute", "attr:lrv_xmulv",
        f"{VFUO_NAME} contributes to the cumulative enveloped-virus (XMuLV) clearance of the "
        f"drug substance; it is not the largest contributor to it." if report
        else f"XMuLV is the enveloped model virus at {VFUO_NAME}, and the plan expects it to be "
             f"retained with a wide margin.",
        "Product and unit operation" if report else "Unit-operation description and prior knowledge",
        "it contributes to two attributes of the drug substance: the cumulative clearance of "
        "minute virus of mice (MVM) as the parvovirus model, and the cumulative clearance of "
        "xenotropic murine leukaemia virus (XMuLV) as the enveloped model" if report
        else "XMuLV is much larger and is expected to be retained with a wide margin.")
    # attribute -> method. Both documents state the linkage: the plan in one sentence of §5.3,
    # the report in @tbl-analyte, whose row pairs the method with the analyte it titrates.
    method_rows = _vf_method_rows(report)
    for key in VF_CQA_KEYS:
        mid = VF_CQA_METHOD[key]
        add(VFATTR_CONCEPT[key], "attribute_measured_by_method", f"method:{mid}",
            f"{VFATTR_NAME[key]} is measured by {mid}.", "Analytical methods",
            method_rows[mid] if report else VFMETHOD_QUOTE[False][mid])
    # Cumulative acceptance criteria. Each is anchored on its own rendered @tbl-cqa row, which
    # carries the attribute and its cumulative criterion in one span. Neither is a per-step
    # release limit; both documents say so, and the step floor is a separate, derived quantity.
    for key in VF_CQA_KEYS:
        r = _vf_cqa_row(key)
        add(VFATTR_CONCEPT[key], "attribute_has_acceptance_criterion", f"lit:{key}_acc",
            f"{VFATTR_NAME[key]} acceptance: ≥ {r['acc_low']:g} {r['unit']} (cumulative across "
            f"the purification train, not a per-step limit).",
            "Quality attributes in scope", cqa_rows[key])
    # The step-level criterion is DERIVED from the cumulative requirement, not specified. Both
    # documents render it as its own @tbl-acceptance row, which carries the response, the
    # attribute, the criterion and the basis together.
    acc = D.acceptance_table(VFUO)
    acc_rows = row_quotes(acc, acc["Quality attribute"], P._auto_floatfmt(acc))
    for key in VF_CQA_KEYS:
        add(VFATTR_CONCEPT[key], "attribute_has_acceptance_criterion", f"lit:{key}_step_floor",
            f"Step-level contribution required of {VFUO_NAME} for {VFATTR_NAME[key]}, "
            f"back-calculated as the cumulative requirement less the clearance credited to the "
            f"other orthogonal steps.",
            "Acceptance and decision criteria" if not report else "Proven acceptable ranges",
            acc_rows[VFATTR_NAME[key]])
    # parameter -> attribute impacts / non-impacts
    if report:
        add("param:vf_filtration_volume", "parameter_impacts_attribute", "attr:lrv_mvm",
            "Volumetric load has a demonstrated and quantified effect on MVM clearance — the "
            "only effect resolved at this step — so it is quality-linked and classified WC-CPP.",
            "Parameter classification", VF_CLASS_SENTENCE["Filtration volume (load)"])
        add("param:vf_pressure", "parameter_does_not_significantly_impact_attribute", "attr:lrv_mvm",
            "No effect of filtration pressure on any response reached significance over the "
            "characterized pressure range; the null result is the evidence for the WC-CPP class, "
            "not an absence of evidence.",
            "Parameter classification", VF_CLASS_SENTENCE["Filtration pressure"])
        # Both parameters are null against enveloped-virus clearance. Each is anchored on its own
        # rendered row of the XMuLV screening effect table, which carries the term and its
        # p-value, plus the sentence that names the response the table belongs to.
        xm = D.screening_effects_df(VFUO, "xmulv_lrf")
        xm_rows = row_quotes(xm, xm["Term"], P._auto_floatfmt(xm))
        for name, code in (("Filtration volume (load)", "A"), ("Filtration pressure", "B")):
            add(VFPARAM_CONCEPT[name], "parameter_does_not_significantly_impact_attribute",
                "attr:lrv_xmulv",
                f"{name} has no resolved effect on enveloped-virus (XMuLV) clearance over the "
                f"characterized range; the screening term does not reach significance.",
                "Screening: factor effects", xm_rows[code],
                "Enveloped-virus clearance shows no significant dependence on either parameter")
    else:
        # The plan states a risk-based STUDY ASSIGNMENT, not a demonstrated effect. Each
        # parameter is anchored on its own rendered @tbl-risk row, which carries the parameter,
        # the prospective failure mode, the affected attribute and the assigned study.
        ra = P.ra_scope(VFUO)
        ra_rows = row_quotes(ra, ra["Parameter"], P._auto_floatfmt(ra))
        for name in VF_MULTIVARIATE:
            add(VFPARAM_CONCEPT[name], "parameter_impacts_attribute", "attr:lrv_mvm",
                f"{name} was ranked high enough in RA-001 to require multivariate evaluation of "
                f"its potential effect on the credited viral log-reduction.",
                "Risk-based prioritization of parameters", ra_rows[name])
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def vf_report_sections(doc_id, file_name, report):
    from annex_contract.summaries import ReportSection, ReportStatement
    import doe_report as D

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        # PCP-009 is prospective: "It is written before any data exist and contains no findings."
        # No statement here may state an outcome of the study it plans.
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-009 defines the characterization studies for the A-Mab small-virus "
                  "retentive filtration step (Step 9), and it is written before any data exist.",
               "Purpose and scope",
               "this plan defines the studies that will characterize it"),
            st(2, "Both process parameters (volumetric load and filtration pressure) are assigned "
                  "to one multivariate design, and each characterization range contains the "
                  "normal operating range and extends above it.",
               "Factors, ranges and study type",
               "Both parameters are assigned to the multivariate design, and each characterization "
               "range contains its normal operating range and extends well above it."),
            st(3, "The study uses a two-factor full-factorial screen followed by a face-centred "
                  "central composite design on a qualified scale-down model.",
               "Response-surface design",
               "The response-surface study is a face-centred central composite design in the same "
               "2 factors"),
            st(4, "MVM sets the retention challenge for the step, because it is the smallest of "
                  "the model viruses; XMuLV is larger and is expected to be retained with a wide "
                  "margin.",
               "Unit-operation description and prior knowledge",
               "MVM is the smallest of the model viruses used for a monoclonal antibody process, "
               "and it therefore sets the retention challenge for this step."),
            st(5, "The study will define the region of the two parameters over which the step "
                  "meets its required log reduction for both model viruses.",
               "Objectives",
               "Define the region of the two parameters over which the step meets its required "
               "log reduction for both model viruses."),
            st(6, "The two step-level clearance criteria are derived, not specified: each is the "
                  "cumulative drug-substance requirement less the clearance credited to the "
                  "other steps, so each moves if that credit changes.",
               "Acceptance and decision criteria",
               "The two viral clearance criteria are step contributions and are derived, not "
               "specified."),
            st(7, "The plan separates the two designs in advance: the screening design identifies "
                  "the active factors and the response-surface model is the predictive model and "
                  "the sole basis of the design space and the proven acceptable ranges.",
               "Statistical methods",
               "The response-surface model is the predictive model, and it alone is the basis of "
               "the design space and of the proven acceptable ranges in §8."),
            st(8, "A clearance result below the limit of quantitation is censored rather than "
                  "measured, so the model for that response will be fitted to the uncensored "
                  "runs and the censored runs reported alongside.",
               "Analytical methods",
               "Such a result is censored, not measured, and a censored value cannot be treated "
               "as an observation in a regression without biasing the fit."),
            st(9, "The step does not by itself satisfy the cumulative clearance requirement for "
                  "either model virus, and the plan says so before the study begins.",
               "Purpose and scope",
               "The step does not by itself satisfy the cumulative clearance requirement for "
               "either model virus"),
        ])]
    coef = D.rsm_coeff_df(VFUO, "mvm_lrf")
    coef_rows = row_quotes(coef, coef["Term"], P._auto_floatfmt(coef))
    fit = D.fit_summary_df(VFUO, "rsm")
    fit_rows = row_quotes(fit, fit["Response"], P._auto_floatfmt(fit))
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "Both process parameters (volumetric load and filtration pressure) are well-controlled "
              "CPPs; the step carries no CPP and no key process parameter.",
           "Executive summary",
           "Both parameters carried into the study, filtration volume and filtration pressure, "
           "are classified as well-controlled critical process parameters. The step has no "
           "critical process parameter and no key process parameter."),
        st(2, "The volumetric load is the only parameter with a demonstrated effect on any "
              "response, and the effect is a decline in MVM (parvovirus) clearance as the load "
              "rises.",
           "Executive summary",
           "The volumetric load is the only parameter with a demonstrated effect on any response."),
        st(3, "XMuLV clearance and step yield are null results: neither model was significant, so "
              "no predictive model is claimed for either and neither constrains the operating "
              "region.",
           "Response-surface models",
           "No predictive model is claimed for enveloped-virus clearance or for step yield at "
           "this step"),
        st(4, "Only the MVM (parvovirus) response-surface model is adequate and predictive, and it "
              "is the model on which the design space rests.",
           "Response-surface models",
           "One of the three response-surface models is adequate and predictive, and it is the "
           "model for the response that governs the step."),
        # The re-authored report does NOT argue that the two-factor screen escapes the usual
        # near-saturation caution. It says the opposite: the factorial part is exactly saturated,
        # the residual degrees of freedom come from the centre points alone, and none of the
        # three screening models is significant overall.
        st(5, "A full factorial in two factors confounds nothing, but the factorial part is "
              "exactly saturated: the residual degrees of freedom come from the centre points "
              "alone, so the screening standard errors are wide and no screening model is "
              "significant overall.",
           "Screening design",
           "A full factorial in two factors estimates both main effects and the interaction "
           "without confounding, so the factorial part is exactly saturated."),
        st(6, "The quadratic term in load does not reach significance in the response-surface "
              "model, so the load effect is carried by its linear term.",
           "Response-surface models", coef_rows["A²"]),
        st(7, "The MVM model has a modest predicted coefficient of determination, so it is used "
              "to define an operating region and to predict mean levels inside it, and not for "
              "precise point predictions at the corners.",
           "Response-surface models",
           "and to predict mean levels inside it, and not to make point predictions at the "
           "corners with a claimed precision"),
        st(8, "The worst case of the design space is the corner at the highest load and the "
              "highest pressure, and the fitted model still predicts more MVM clearance there "
              "than the step is required to contribute.",
           "Design space",
           "The worst case in that region is the corner at the highest load and the highest "
           "pressure."),
        st(9, "The reported capability figures are properties of the whole train and not of this "
              "step: parvovirus clearance is delivered jointly with anion exchange (PCR-008).",
           "Process capability and robustness", "Neither capability figure belongs to this step alone."),
        # The report compares the two viral attributes with each other. It makes no claim about
        # the rest of the drug-substance register, and none is recorded here.
        st(10, "Cumulative parvovirus clearance is the tighter of the two viral-clearance "
               "capabilities, and it is the attribute this step contributes most to.",
            "Process capability and robustness",
            "The parvovirus figure is the tighter capability of the two, and it is the one this "
            "step contributes most to."),
        st(11, "The MVM response-surface model is significant with a predicted coefficient of "
               "determination well below its fitted value, which is the gap the report carries "
               "into every claim made from the model.",
            "Response-surface models", fit_rows["MVM LRF (log₁₀)"]),
        st(12, "Two deviations were recorded, both were dispositioned as retained, and neither "
               "changed a fitted effect, a parameter classification or the operating region.",
            "Discussion",
            "Neither changed a fitted effect, a classification or the operating region, and both "
            "are reported in full in §13."),
    ])]


def vf_design_spaces(doc_id, file_name):
    return [S.DesignSpace(
        design_space_id="ds:vf", unit_operation=VFUO_NAME,
        parameters=["param:vf_filtration_volume", "param:vf_pressure"],
        quality_attributes_constrained=["attr:lrv_mvm", "attr:lrv_xmulv"],
        definition="The whole characterized region in volumetric load and filtration pressure: "
                   "everywhere inside the characterized ranges the response-surface model keeps "
                   "the MVM log-reduction above the back-calculated step requirement, and measured "
                   "XMuLV clearance stayed above its requirement at every executed run. The "
                   "region has one principal plane, load against pressure, because those are the "
                   "only two parameters of the step; the load axis is what constrains it, because "
                   "load is the only parameter with a resolved effect, and the pressure axis is "
                   "carried because the demonstration that clearance is insensitive to pressure "
                   "holds only across the pressure range that was studied. The worst case is the "
                   "corner at the highest load and the highest pressure, and the two pressure "
                   "edges differ there by far less than the residual scatter of the model, so "
                   "load alone sets the worst case.",
        source_references=[
            ref(doc_id, file_name, "Design space", "Design space",
                "The design space of the step is the whole characterized region, bounded by the "
                "load and pressure ranges studied."),
            ref(doc_id, file_name, "Design space", "Design space",
                "The model predicts an MVM log reduction of 4.48 there, against a required step "
                "contribution of 3.89 log, leaving a margin of 0.59 log.")],
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


def vf_proven_acceptable_ranges(doc_id, file_name):
    """One ProvenAcceptableRange per governed viral-clearance CQA x parameter, from the same
    DoE engine (``doe_report.par_table``) that renders @tbl-par in the report. Neither CQA has
    a drug-substance specification a single step can be measured against, so both use the
    back-calculated step floor (cumulative requirement minus the credit taken by the other
    orthogonal steps) as the acceptance basis.

    Each record is anchored on its own rendered row of @tbl-par: the row names the CQA, the
    parameter, the characterization range and both proven acceptable ranges, so the span
    carries the whole relation the record states rather than a sentence discussing it."""
    import doe_report as D
    par = D.par_table(VFUO)
    rows = _md_rows(par)
    out = []
    for i, (r, row) in enumerate(zip(par.to_dict("records"), rows), 1):
        cqa, param, unit = r["CQA"], r["Parameter"], (r["Unit"] or "")
        out.append(S.ProvenAcceptableRange(
            par_id=f"{doc_id}-PAR{i:02d}", unit_operation=VFUO_NAME,
            quality_attribute=cqa, parameter=param,
            characterization_range=f"{r['Char. range']} {unit}".strip(),
            par_at_setpoint=f"{r['PAR (set-point)']} {unit}".strip(),
            par_nor_propagated=f"{r['PAR (NOR)']} {unit}".strip(),
            acceptance_basis=(
                "Step-level required log-reduction, back-calculated from the cumulative "
                "viral-clearance requirement minus the clearance credited to the other orthogonal "
                "steps (modular viral-safety claim under ICH Q5A(R2))."),
            source_references=[ref(doc_id, file_name, f"{doc_id}_sec_par", VF_PAR_SEC, row,
                                   table_title=("Proven acceptable ranges per governed quality "
                                                "attribute and parameter, from both analyses."),
                                   table_id=f"{doc_id}_tab_par")],
            metadata=meta()))
    return out


# --------------------------------------------------------------------------- #
# Report-only rhetorical layer (PCR-009 only).                                  #
# --------------------------------------------------------------------------- #
# Argument-structure spans over the PCR-009 report. Each quote is a verbatim,    #
# plain-prose fragment of the RENDERED report (no inline expressions, no bold);  #
# number-free wherever the argument allows, so a reseed cannot break grounding.  #
# Re-anchored 2026-07-28: the report was re-authored, so all 37 previous spans   #
# died at once. This is the argument the NEW text makes.                         #
#                                                                                #
# The spine is adverse-first: the only resolved effect is the decline of MVM     #
# clearance with volumetric load, which is stated, mechanistically warranted,     #
# then bounded (worst characterized corner, the model's own predicted R², the     #
# scale-down spiking model). The design-side spans carry what is specific to this #
# step and what CHANGED with the re-authoring: the 2^2 screen confounds nothing   #
# but is EXACTLY SATURATED, so the residual comes from the centre points alone,   #
# the standard errors are wide and no screening model is significant overall      #
# (R09/R10/R11) — which is why the response-surface model is the predictive one   #
# (R12/R13). The two null responses are annotated as findings, not as gaps.       #
# NOTE: the closing sentence of "Process capability and robustness" is the        #
# registered weak claim WC-009-01 (support = unsupported, emitted from            #
# authoring/weak_claims.yaml). It carries NO rhetorical span and NO assertion by  #
# design; the grounded bounds it omits are annotated instead (R29 the scale-down  #
# and Stage-2 bound, R20/R25/R28 the model and range bounds, R41 the conclusion   #
# that hands viral safety to the cumulative claim). Tuple fields:                 #
# (suffix, role, section, quote, supported_by-suffixes, restates-suffix,          #
#  bounds-suffix).                                                                #
# --------------------------------------------------------------------------- #
VF_RHET_SPANS = [
    # --- Executive summary: the adverse finding first, then its scope ------------------ #
    ("R01", "claim", "Executive summary",
     "The volumetric load is the only parameter with a demonstrated effect on any response.",
     ["R15", "R17", "R23"], None, None),
    ("R02", "claim", "Executive summary",
     "Neither the XMuLV model nor the step yield model was significant over the ranges studied, "
     "so no predictive model is claimed for either.", ["R17"], None, None),
    ("R03", "hedge", "Executive summary",
     "Those two null results are reported as evidence of robustness and are carried into the "
     "knowledge space", [], None, None),
    ("R04", "deferral", "Executive summary",
     "the cumulative claim is consolidated in PCMR-001", [], None, None),
    # --- Introduction: mechanism and the modular framework ---------------------------- #
    ("R05", "mechanistic_warrant", "Product and unit operation",
     "The membrane retains particles above its pore-size distribution while the antibody monomer "
     "passes, so clearance depends on the physical dimensions of the virus and on how much "
     "material the retentive layer has already seen.", [], None, None),
    ("R06", "cross_step_credit", "Product and unit operation",
     "Low-pH inactivation destroys the lipid envelope of enveloped virus (PCR-006), and anion "
     "exchange removes virus by charge-based binding in flow-through mode (PCR-008).",
     [], None, None),
    ("R07", "claim", "Product and unit operation",
     "A filtration step that works on size alone therefore adds clearance that does not share a "
     "failure mode with either of them.", ["R05", "R06"], None, None),
    # --- Prior knowledge: what the study was for -------------------------------------- #
    ("R08", "problem_statement", "Platform and prior-product knowledge",
     "Prior knowledge therefore transfers to A-Mab, and the purpose of this study is to confirm "
     "and bound the platform behaviour for this molecule.", [], None, None),
    ("R09", "justification", "Platform and prior-product knowledge",
     "The load range was extended well beyond the routine ceiling in order to find where "
     "clearance stops being sufficient, and the pressure range was extended to both operating "
     "limits of the filter so that a null result would be a bounded null result.", [], None, None),
    ("R10", "problem_statement", "Platform and prior-product knowledge",
     "Neither expectation was treated as established for A-Mab before the study, and both are "
     "tested in §5.", [], None, None),
    # --- Study design: a full factorial that is nonetheless exactly saturated ---------- #
    ("R11", "justification", "Screening design",
     "A full factorial in two factors estimates both main effects and the interaction without "
     "confounding, so the factorial part is exactly saturated.", [], None, None),
    ("R12", "problem_statement", "Screening design",
     "It is not to quantify that effect precisely, and this design could not do so.",
     [], None, None),
    ("R13", "justification", "Screening design",
     "With three model terms and 7 runs the residual carries few degrees of freedom, so the "
     "standard errors are wide and the test has limited power.", [], None, None),
    ("R14", "claim", "Response-surface design",
     "The screening design identifies which parameters are active, and the response-surface "
     "model is the predictive model and the basis of the design space",
     ["R13", "R16"], None, None),
    ("R16", "justification", "Response-surface design",
     "Adding the axial points allows a squared term for each factor, so the model can describe "
     "curvature in the clearance surface.", [], None, None),
    ("R17", "justification", "Screening: factor effects",
     "Enveloped-virus clearance shows no significant dependence on either parameter",
     [], None, None),
    ("R15", "justification", "Screening: factor effects",
     "Volumetric load reduces MVM clearance by 1.61 log across the characterized load range, and "
     "it is the only term in Table 13 that reaches significance (p = 0.027).", [], None, None),
    # --- Results: reproducibility, then the two model verdicts ------------------------- #
    ("R18", "claim", "Response-surface models",
     "One of the three response-surface models is adequate and predictive, and it is the model "
     "for the response that governs the step.", ["R19"], None, None),
    ("R19", "justification", "Response-surface models",
     "The MVM model explains R² = 0.947 of the variation with an adjusted R² of 0.903, and the "
     "overall F test gives p = 0.0009.", [], None, None),
    ("R20", "bounded_conclusion", "Response-surface models",
     "Its predicted R² is 0.527, which is materially lower than the fitted R² and is the honest "
     "measure of how the model behaves on a run it has not seen, so predictions near the edge of "
     "the region should be read with that gap in mind.", [], None, "R18"),
    ("R21", "hedge", "Centre-point performance and reproducibility",
     "The observed run-to-run scatter is below the intermediate precision of the assay, so the "
     "reproducibility of the model cannot be resolved separately from the method at this sample "
     "size.", [], None, None),
    ("R22", "problem_statement", "Screening: factor effects",
     "None of the three screening models is significant overall at alpha = 0.05, including the "
     "MVM model, whose overall p-value is 0.096.", [], None, None),
    # --- Mechanistic interpretation ---------------------------------------------------- #
    ("R23", "mechanistic_warrant", "Mechanistic interpretation",
     "As the volumetric load rises, protein and other load components deposit within the "
     "retentive layer, and the passage available to a particle of parvovirus size changes with "
     "them.", [], None, None),
    ("R24", "mechanistic_warrant", "Mechanistic interpretation",
     "Over the range tested, pressure sets the flux, and with it the time the filtration takes, "
     "and it does not change what the membrane retains.", [], None, None),
    ("R25", "claim", "Mechanistic interpretation",
     "The practical consequence is that the two parameters can be treated as acting "
     "independently inside the region, so the operating region is close to a rectangle in the "
     "two parameters.", ["R24", "R53"], None, None),
    ("R53", "justification", "Response-surface models",
     "The interaction term is not significant, which means the effect of load on clearance does "
     "not depend on the pressure the filter is run at.", [], None, None),
    ("R26", "justification", "Mechanistic interpretation",
     "A multivariate design was still the right instrument, because independence is a finding of "
     "the study and not an assumption of it, and the interaction term had to be estimated in "
     "order to be dismissed.", [], None, None),
    ("R27", "mechanistic_warrant", "Mechanistic interpretation",
     "The membrane is therefore not plugging to any appreciable degree over the loads tested, "
     "and the decline in MVM clearance comes from a change in the retentive layer rather than "
     "from gross fouling.", [], None, None),
    # --- Design space ------------------------------------------------------------------ #
    ("R28", "claim", "Design space",
     "The design space of the step is the whole characterized region, bounded by the load and "
     "pressure ranges studied.", ["R18", "R29"], None, None),
    ("R29", "justification", "Design space",
     "The model predicts an MVM log reduction of 4.48 there, against a required step "
     "contribution of 3.89 log, leaving a margin of 0.59 log.", [], None, None),
    ("R30", "hedge", "Design space",
     "That difference is well inside the scatter of the model, so load alone sets the worst "
     "case, and a reader tracking the limiting condition of this step should track the load "
     "axis.", [], None, None),
    ("R31", "bounded_conclusion", "Design space",
     "Three bounds apply to this design space.", [], None, "R28"),
    # --- Proven acceptable ranges ------------------------------------------------------ #
    ("R32", "problem_statement", "Proven acceptable ranges",
     "The acceptance basis comes first, because for a viral clearance response it is not the "
     "drug substance specification.", [], None, None),
    ("R33", "claim", "Proven acceptable ranges",
     "Every entry in Table 19 spans the full characterization range, and the two analyses agree "
     "on every row.", ["R18"], None, None),
    ("R34", "claim", "Proven acceptable ranges",
     "It is the multivariate corner identified in §6, the point of highest load and highest "
     "pressure, where the margin over the requirement is smallest.", ["R29", "R33"], None, None),
    ("R35", "bounded_conclusion", "Proven acceptable ranges",
     "Two bounds apply to the ranges in Table 19", [], None, "R33"),
    # --- Capability: the honest counterpart of the registered weak claim WC-009-01, which #
    # --- closes this section and is deliberately NOT annotated as a claim span --------- #
    ("R36", "bounded_conclusion", "Process capability and robustness",
     "The estimate comes from Monte-Carlo simulation of 2,000 batches on qualified scale-down "
     "models, so it is a prediction of commercial-scale behaviour and not a measurement of it, "
     "and Stage 2 confirms it at scale.", [], None, None),
    ("R37", "cross_step_credit", "Process capability and robustness",
     "The low-pH hold contributes nothing to parvovirus clearance, because a non-enveloped virus "
     "is not inactivated by low pH, and it is not credited for it.", [], None, None),
    ("R38", "justification", "Process capability and robustness",
     "Filtration supplies 5.32 log of the 10.03 log cumulative parvovirus claim, and anion "
     "exchange supplies 4.71 log of it (PCR-008).", [], None, None),
    # --- Classification and control strategy ------------------------------------------- #
    ("R39", "claim", "Parameter classification",
     "Both parameters of the step are classified as well-controlled critical process parameters "
     "under SOP-4001.", ["R15", "R17"], None, None),
    ("R40", "problem_statement", "Parameter classification",
     "There is no parameter here whose control capability is poor relative to the width of its "
     "design space, which is the condition that would force the CPP designation.",
     [], None, None),
    ("R42", "cross_step_credit", "Contribution to the control strategy",
     "Parvovirus clearance is shared with anion exchange (PCR-008) and enveloped-virus clearance "
     "with the low-pH hold (PCR-006) and anion exchange.", [], None, None),
    ("R43", "deferral", "Contribution to the control strategy",
     "That independence is an argument about mechanism and not a measurement, and it is made in "
     "PCMR-001 where the whole claim is assembled.", [], None, None),
    # --- Discussion -------------------------------------------------------------------- #
    ("R44", "hedge", "Discussion",
     "Confidence in the scale-down model is good for the operating-range conclusions and is "
     "necessarily weaker for the clearance figures themselves.", [], None, None),
    ("R45", "bounded_conclusion", "Discussion",
     "Four limitations bound what this report establishes.", [], None, "R18"),
    # --- Conclusions: restatements of the two claims the report is built on ------------ #
    ("R46", "restatement", "Conclusions",
     "Volumetric load governs parvovirus clearance and is the only parameter with a demonstrated "
     "effect on any response.", [], "R01", None),
    ("R47", "restatement", "Conclusions",
     "Every proven acceptable range in §7 spans the whole characterization range under both "
     "analyses, so the binding constraint on the operating region is the multivariate corner and "
     "not any univariate range.", [], "R33", None),
    ("R48", "bounded_conclusion", "Conclusions",
     "These conclusions are bounded by the characterization ranges, by the fitted "
     "response-surface model and by the qualified small-scale spiking model on which clearance "
     "was measured.", [], None, "R46"),
    ("R41", "cross_step_credit", "Conclusions",
     "They do not by themselves establish viral safety, which is a cumulative claim consolidated "
     "in PCMR-001 and confirmed at commercial scale in Stage 2.", [], None, None),
    # --- Deviations -------------------------------------------------------------------- #
    ("R49", "justification",
     "DEV-009-01 — transient filtration-pressure excursion above the normal operating range",
     "The excursion peak is inside the characterization range of 8–30 psi, at a coded position "
     "of +0.27, so the affected run sits inside the region the study explored.", [], None, None),
    ("R50", "deviation_disposition",
     "DEV-009-01 — transient filtration-pressure excursion above the normal operating range",
     "The deviation is therefore retained, the affected run remains in the analysis, and the "
     "classification of filtration pressure in §9 is unchanged.", ["R49"], None, None),
    ("R51", "mechanistic_warrant",
     "DEV-009-02 — filter membrane lot flux below the vendor-typical value",
     "Flux is a permeability property of the membrane and is set by the open structure of the "
     "support, whereas retention is set by the pore-size distribution of the retentive layer, "
     "and the two are specified and released separately by the vendor.", [], None, None),
    ("R52", "deviation_disposition",
     "DEV-009-02 — filter membrane lot flux below the vendor-typical value",
     "The deviation is retained and the affected runs remain in the analysis.",
     ["R51"], None, None),
]


def vf_rhetorical_spans(doc_id, file_name):
    """Rhetorical / argument-structure spans over the PCR-009 report (report-only)."""
    out = []
    for suffix, role, sec, quote, sup, res, bnd in VF_RHET_SPANS:
        out.append(S.RhetoricalSpan(
            span_id=f"{doc_id}-{suffix}", section=sec, role=role,
            source_reference=ref(doc_id, file_name, f"{doc_id}_sec_rhet", sec,
                                 " ".join(quote.split())),
            supported_by=[f"{doc_id}-{s}" for s in sup],
            restates=(f"{doc_id}-{res}" if res else None),
            bounds=(f"{doc_id}-{bnd}" if bnd else None)))
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
        weak_claims=build_weak_claims(doc, f),
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
        weak_claims=build_weak_claims(doc, f),
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
            "Two-factor design: the 2^2 screen is FULL, not fractional, so no effect is aliased — but the report states that the factorial part is exactly saturated, the residual degrees of freedom come from the centre points alone, and no screening model is significant overall. The response-surface model is the predictive model and the basis of the design space.",
            "XMuLV log-reduction and step yield produced no significant term and both fits have negative predicted R²; they are robustness evidence and are explicitly not used predictively, so no DesignSpace or model claim is recorded for them.",
            "Process-capability (Cpk) values have no dedicated field; reported as report_sections statements.",
            "proven_acceptable_ranges mirror @tbl-par (doe_report.par_table), one record per rendered row; rhetorical_spans are verbatim report prose.",
            "PCR-009 carries one registered weak claim (WC-009-01, unbounded_generalization) at the close of the capability section. It is deliberately NOT covered by an assertion or a rhetorical span; the grounded statements that bound it (Stage-2 confirmation, the scale-down bound, the load limit) are annotated instead.",
        ],
        inventory=vf_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=vf_studies(doc, f, report=True),
        design_spaces=vf_design_spaces(doc, f),
        proven_acceptable_ranges=vf_proven_acceptable_ranges(doc, f),
        report_sections=vf_report_sections(doc, f, report=True),
        assertions=vf_assertions(doc, f, report=True), concepts=vf_concepts(),
        rhetorical_spans=vf_rhetorical_spans(doc, f))


# =========================================================================== #
# Ultrafiltration / Diafiltration (Step 10) — PCP-010 / PCR-010.                #
# --------------------------------------------------------------------------- #
# Additive, self-contained builders for the non-DoE UF/DF pair.                 #
#                                                                               #
# Re-anchored 2026-07-28 against the re-authored pair. Almost every prose quote  #
# in the previous version is gone with the prose it quoted, but three records    #
# were not merely unanchored — they asserted the OPPOSITE of what the new        #
# documents say, and they are corrected here rather than re-quoted:              #
#                                                                               #
#  1. PROVEN ACCEPTABLE RANGES. The old annex carried one ProvenAcceptableRange  #
#     per parameter, each saying "the PAR of each parameter is its              #
#     characterization range". PCR-010 §7 now opens "No proven acceptable range  #
#     is claimed for any parameter of this step", gives the reason (a PAR needs  #
#     a governed attribute and this step has none), and repeats the refusal in   #
#     the executive summary and the conclusions. The block is therefore EMPTY,   #
#     and ProcessParameter.PAR is null for both documents — the register's       #
#     par_low/par_high columns are what both documents render as the             #
#     CHARACTERIZATION range, and calling that a PAR is the very claim the       #
#     report declines to make.                                                   #
#  2. "PARAMETER DOES NOT SIGNIFICANTLY IMPACT ATTRIBUTE". The old annex made    #
#     that assertion for all three parameters in BOTH documents. It is false in  #
#     both. The plan is written before any data exist, names two mechanisms that #
#     could change product quality, and says "The class is an outcome of the     #
#     study and is not pre-judged in this plan". The report is more explicit     #
#     still: "The classification follows from the quality attribute register …   #
#     and not from a demonstrated null effect on one", and §5.4 records that the #
#     quality confirmation does not reach the edges of the characterization      #
#     ranges at all. No such assertion is emitted; the absence of a quality      #
#     LINKAGE is captured instead, which is what both documents actually argue.  #
#  3. MONITORED ATTRIBUTES. The old annex carried two attributes. Both documents #
#     now put THREE in scope (aggregate, acidic charge variants and residual     #
#     DNA), with different reasons in each: the plan does not assay residual DNA #
#     and lists it because the step fixes the per-dose basis, while the report   #
#     measures all three on the pool and reports capability for all three.       #
#                                                                               #
# The step still forms and clears no CQA, so there is no DesignSpace: PCR-010 §6 #
# says "This step contributes no element to the design space". No screening and  #
# no response-surface design was planned or run and RA-001 required none, so the #
# only studies are the univariate ranging and the scale-down qualification.      #
# Each record anchors on its own rendered table row where the relation lives in  #
# a table, and on the sentence that states it where it does not.                 #
# =========================================================================== #
UFUO = "ufdf"
UFUO_NAME = P.UNIT_OP_TITLES[UFUO]               # "Ultrafiltration / Diafiltration" (rendered)
UFUO_CSV = P.CFG.unit_op(UFUO).name              # "... (formulation)" (CSV only)
UFSTEP = P.CFG.unit_op(UFUO).step                # 10
UFSTEP_LABEL = f"Ultrafiltration / Diafiltration (Step {UFSTEP})"

PCP10_FILE = "PCP-010_ufdf.docx"
PCR10_FILE = "PCR-010_ufdf.docx"

UFPARAM_ROWS = P.param_reg[P.param_reg.unit_operation == UFUO_CSV].to_dict("records")
UFPARAM_CONCEPT = {
    "Number of diavolumes": "param:ufdf_diavolumes",
    "Transmembrane pressure": "param:ufdf_tmp",
    "Final DS concentration": "param:ufdf_final_conc",
}
# The three drug-substance attributes both documents put in scope, in the order both
# render them (the ``mon_keys`` / ``DS_KEYS`` list of the two SETUP chunks). The step sets
# and clears none of them; what differs between the pair is what is done with each.
UFATTR_KEYS = ["aggregates_hmw", "acidic_variants", "residual_dna"]
UFATTR_CONCEPT = {k: f"attr:{k}" for k in UFATTR_KEYS}
UFATTR_NAME = {r["key"]: r["cqa"] for r in P.cqa_reg.to_dict("records")}
UFMETHODS = [
    ("AMV-3019", "Protein Concentration by A280 (UV)", "spectroscopy",
     ["protein concentration"], []),
    ("AMV-3011", "Size-Variants (SEC-HPLC)", "chromatography",
     ["aggregate", "monomer"], ["aggregates_hmw"]),
    ("AMV-3013", "Charge Variants (icIEF)", "electrophoresis",
     ["acidic variants", "main peak", "basic variants"], ["acidic_variants"]),
]
# Both documents describe the scale-down system as a tangential flow filtration system, and
# neither hyphenates the compound, so the entity follows the text.
UFSDM = "scale-down tangential flow filtration system"
UFSKID = "EQ-TFF-142"


# --------------------------------------------------------------------------- #
# Rendered table rows. Every relation that lives in a table anchors on its own  #
# row, rebuilt from the DataFrame the document renders, so a record and the row #
# it cites cannot drift apart when the seed changes.                           #
# --------------------------------------------------------------------------- #
def _uf_sop_df():
    """The @tbl-refs frame both documents render (``sop_table`` emits markdown, not a frame)."""
    rows = [[sid, title, "SOP"] for sid, title in P.UFDF_SOP_REFS]
    rows += [[aid, title, "Method validation"] for aid, title in P.UFDF_AMV_REFS]
    return P.pd.DataFrame(rows, columns=["Reference", "Title", "Type"])


def uf_rows(report):
    """``{table -> {key -> rendered row}}`` for every table the pair renders."""
    prm = P.report_params(UFUO) if report else P.plan_params(UFUO)
    cqa = P.cqas_by_keys(UFATTR_KEYS)
    ra = P.ra_scope(UFUO)
    lv = P.univariate_levels(UFUO)
    refs = _uf_sop_df()
    perf = P.method_perf_for(P.UFDF_AMV_REFS, precision_with_unit=not report)
    out = {
        "params": row_quotes(prm, prm["Parameter"], P._auto_floatfmt(prm)),
        "cqa": row_quotes(cqa, UFATTR_KEYS, P._auto_floatfmt(cqa)),
        "risk": row_quotes(ra, ra["Parameter"], P._auto_floatfmt(ra)),
        "levels": row_quotes(lv, lv["Parameter"], P._auto_floatfmt(lv)),
        "refs": row_quotes(refs, refs["Reference"]),
        "methperf": row_quotes(perf, perf["Method"], P._auto_floatfmt(perf)),
    }
    if report:
        sp = P.step_performance(UFSTEP)
        cap = P.cap_for(UFATTR_KEYS)
        yld = P.yield_waterfall_df()
        reg = P.cqa_scope_df()
        dev = P.dev_facts("PCR-010").rename(
            columns={"dev_id": "Deviation", "summary": "Summary",
                     "detected_during": "Detected during", "disposition": "Disposition"})
        dev = dev[["Deviation", "Summary", "Detected during", "Disposition"]]
        out.update({
            "perf": row_quotes(sp, sp["Metric"], ",g"),
            "cap": row_quotes(cap, UFATTR_KEYS, P._auto_floatfmt(cap)),
            "yield": row_quotes(yld, yld["Step"], ".1f"),
            "register": row_quotes(reg, reg["CQA"], P._auto_floatfmt(reg)),
            "dev": row_quotes(dev, dev["Deviation"]),
        })
    return out


# --------------------------------------------------------------------------- #
# Per-document prose anchors.                                                  #
# --------------------------------------------------------------------------- #
# Analytical methods: each method anchors on its @tbl-refs row (reference, title and type in
# one span) and on the sentence of the analytical-methods section that says what it measures.
UFMETHOD_QUOTE = {
    False: {  # PCP-010 §5.3
        "AMV-3019": ("Protein concentration is measured by ultraviolet absorbance (AMV-3019), "
                     "which is also the method that decides whether a run met the concentration "
                     "target."),
        "AMV-3011": ("Aggregate is measured by size exclusion chromatography (AMV-3011) and "
                     "reported as the percentage of high molecular weight species."),
        "AMV-3013": ("Charge variants are measured by imaged capillary isoelectric focusing "
                     "(AMV-3013) and reported as the acidic variant percentage."),
    },
    True: {   # PCR-010 §3.3
        "AMV-3019": ("Protein concentration is measured by ultraviolet absorbance under AMV-3019, "
                     "and it is both the quantity that defines the endpoint of the second "
                     "concentration phase and a drug substance release test."),
        "AMV-3011": ("Aggregate is measured by size exclusion chromatography under AMV-3011 and "
                     "charge variants by imaged capillary isoelectric focusing under AMV-3013"),
        "AMV-3013": ("Aggregate is measured by size exclusion chromatography under AMV-3011 and "
                     "charge variants by imaged capillary isoelectric focusing under AMV-3013"),
    },
}
# Why each attribute is in scope. The two documents give DIFFERENT reasons for residual DNA —
# the plan does not assay it and carries it because the step fixes the per-dose basis, the
# report measures it on the pool and reports its capability — so the anchors are per document.
UFATTR_QUOTE = {
    False: {  # PCP-010 §4.2
        "aggregates_hmw": ("Aggregate is the attribute at risk. It is of high criticality, its "
                           "acceptance criterion is an upper limit, and both of the mechanisms "
                           "described in §4.1 act on it."),
        "acidic_variants": ("Acidic charge variants are of very low criticality and have a wide "
                            "acceptance range, so they are measured as confirmation and not as a "
                            "limit the step is expected to approach."),
        "residual_dna": ("Its acceptance criterion is expressed per dose, and this step brings "
                         "the drug substance to the concentration on which a dose is based, but "
                         "the membrane retains residual DNA together with the antibody, so "
                         "concentrating the pool changes neither quantity relative to the other."),
    },
    True: {   # PCR-010 §2.2
        "aggregates_hmw": ("Aggregate is the attribute with a mechanism at this step. It is "
                           "formed in the production bioreactor (PCR-003) and reduced principally "
                           "at cation exchange (PCR-007), and the concentration and recirculation "
                           "applied here are the last opportunity in the process to add to it."),
        "acidic_variants": ("Acidic charge variants are formed in the bioreactor and are "
                            "challenged by the low pH hold (PCR-006), and they are measured again "
                            "here because the drug substance is the material the specification "
                            "applies to."),
        "residual_dna": ("Residual DNA is cleared across the three chromatography steps and is "
                         "reported for the drug substance on a per dose basis, and that "
                         "conversion of basis is made at this step."),
    },
}
# The report classifies each parameter individually in §9 and gives the reason with it.
UFCLASS_QUOTE = {
    "Number of diavolumes": (
        "It sets the completeness of the buffer exchange, which is a formulation property of the "
        "drug substance and not a critical quality attribute, and it is counted from permeate "
        "mass and easy to hold."),
    "Transmembrane pressure": (
        "It governs the permeate flux and the processing time, and through shear at the membrane "
        "it has the most plausible route of the three to a quality effect. It is nevertheless "
        "classified on process performance, because this step governs no attribute against which "
        "such an effect could be classified."),
    "Final DS concentration": (
        "It is the endpoint of the step and it is measured on the drug substance at release, so "
        "it is controlled closely for reasons of process consistency and not of quality risk."),
}
UFCLASS_RATIONALE = {
    "Number of diavolumes": (
        "Key process parameter. It sets the completeness of the buffer exchange, which is a "
        "formulation property of the drug substance and not a critical quality attribute."),
    "Transmembrane pressure": (
        "Key process parameter. It governs permeate flux and processing time and carries the most "
        "plausible route of the three to a quality effect, but it is classified on process "
        "performance because the step governs no attribute against which such an effect could be "
        "classified."),
    "Final DS concentration": (
        "Key process parameter. It is the endpoint of the step and is measured on the drug "
        "substance at release, so it is controlled for process consistency and not for quality "
        "risk."),
}


def uf_step(doc_id, file_name, sec, report):
    if report:
        src = [ref(doc_id, file_name, sec, "Executive summary",
                   "Ultrafiltration and diafiltration is the last unit operation of the A-Mab "
                   "drug substance process, and it concentrates the virus filtrate, exchanges it "
                   "into the formulation buffer and delivers the drug substance at its target "
                   "concentration."),
               ref(doc_id, file_name, sec, "Product and unit operation",
                   "No critical quality attribute is formed at this step and none is cleared.")]
    else:
        src = [ref(doc_id, file_name, sec, "Purpose and scope",
                   "It concentrates the filtrate of the small virus retentive filtration step, "
                   "exchanges it into the formulation buffer and delivers the drug substance at "
                   "its target concentration"),
               ref(doc_id, file_name, sec, "Purpose and scope",
                   "No quality attribute in the drug substance register is assigned to this step, "
                   "and no viral clearance or impurity clearance is claimed for it.")]
    return S.ProcessStep(
        step_id="step:ufdf", step_name=UFUO_NAME, step_number=str(UFSTEP),
        unit_operation=UFUO_NAME,
        description="Final ultrafiltration / diafiltration (tangential flow filtration), run in "
                    "three phases: the load is concentrated, diafiltered at constant volume "
                    "against the formulation buffer, concentrated again to the drug substance "
                    "target and recovered from the skid with a buffer flush. Forms no critical "
                    "quality attribute and is credited with no impurity or virus clearance; a "
                    "formulation and mass-balance operation.",
        input_materials=["virus-filtration pool (UF/DF feed)"],
        output_materials=["A-Mab drug substance (formulated)"],
        equipment=["ultrafiltration / diafiltration membrane (TFF)", UFSDM, UFSKID],
        source_references=src, metadata=meta())


def uf_equipment(doc_id, file_name, sec, report):
    membrane = S.Equipment(
        equipment_id="equip:ufdf_membrane",
        equipment_name="ultrafiltration / diafiltration membrane (TFF)",
        equipment_type="tangential flow filtration membrane", site_name=P.RECEIVING_SITE,
        source_references=[ref(doc_id, file_name, sec,
                               "Product and unit operation" if report
                               else "Unit operation description and prior knowledge",
                               "a membrane whose nominal cut off retains the antibody while the "
                               "permeate carries the small solutes" if report else
                               "an ultrafiltration membrane whose nominal cut-off retains the "
                               "antibody and passes the buffer species")],
        metadata=meta())
    sdm = S.Equipment(
        equipment_id="equip:ufdf_sdm", equipment_name=UFSDM,
        equipment_type="ultrafiltration / diafiltration (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec, "Scale-down model and its qualification",
                               "The studies were executed on a scale-down tangential flow "
                               "filtration system qualified as a model of the commercial skid "
                               "under SOP-1001." if report else
                               "The study will be run on a scale-down tangential flow filtration "
                               "system that reproduces the commercial operation")],
        metadata=meta())
    skid = S.Equipment(
        equipment_id="equip:ufdf_skid", equipment_name=UFSKID,
        equipment_type="tangential flow filtration skid (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref(doc_id, file_name, sec, "Scale-down model and its qualification",
                               "The skid used for the studies (EQ-TFF-142) was in calibration at "
                               "execution" if report else
                               "The skid used for the study (EQ-TFF-142) is under calibration and "
                               "change control")],
        metadata=meta())
    return [membrane, sdm, skid]


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
    """One ProcessParameter per row of @tbl-params, anchored on that row.

    ``PAR`` is deliberately NULL in both documents. The parameter register's par_low/par_high
    columns are what both documents render as the CHARACTERIZATION range (the plan's "Range
    studied" column, the report's "Char. range"), and PCR-010 §7 states in its first sentence
    that no proven acceptable range is claimed for any parameter of this step. Filling the PAR
    field from those columns would put the exact claim the report refuses into the ground truth.
    """
    caption = ("Parameters characterized at the step, with the final classification."
               if classified else "Parameters, ranges and study type for the step.")
    rows = uf_rows(classified)["params"]
    out = []
    for r in UFPARAM_ROWS:
        name = r["parameter"]
        ptype = r["classification"] if classified else "unclassified"
        src = [ref(doc_id, file_name, sec,
                   "Parameters, ranges and the knowledge space" if classified
                   else "Factors, ranges and study type",
                   rows[name], table_title=caption, table_id=f"{doc_id}_tab_params")]
        if classified:
            src.append(ref(doc_id, file_name, sec, "Parameter classification", UFCLASS_QUOTE[name]))
        out.append(S.ProcessParameter(
            parameter_id=UFPARAM_CONCEPT[name], parameter_name=name, parameter_type=ptype,
            unit=r["unit"], target_value=f"{r['setpoint']:g}",
            NOR=f"{r['nor_low']:g}–{r['nor_high']:g} {r['unit']}",
            PAR=None,
            associated_step=UFSTEP_LABEL,
            rationale_for_criticality=UFCLASS_RATIONALE[name] if classified else None,
            source_references=src, metadata=meta()))
    return out


def uf_attributes(doc_id, file_name, sec, report):
    """The three drug-substance attributes of @tbl-cqa.

    Each attribute anchors on its own @tbl-cqa row, which carries the attribute, its acceptance
    criterion, its criticality and its Tool #1 score in one span. The report adds its @tbl-cap
    row (mean, SD and Cpk) and its Appendix C register row, which names the step that sets it.

    ``associated_steps`` is EMPTY in the plan and names the setting step only in the report.
    The register is the corpus's single source of truth for which step sets an attribute, but
    PCP-010 never renders it: §4.2 says only that "Every attribute in the register is set at an
    earlier step" and lists four of them without saying which sets which. The report renders the
    register in Appendix C, where each row reads "… Production Bioreactor PCR-003", so only
    there is the attribution attested by the document.
    """
    rows = uf_rows(report)
    caption = ("Drug substance quality attributes measured after the step." if report
               else "Drug substance quality attributes carried into the step.")
    out = []
    for key in UFATTR_KEYS:
        r = P.cqa_reg[P.cqa_reg.key == key].iloc[0]
        src = [ref(doc_id, file_name, sec, "Quality attributes in scope", rows["cqa"][key],
                   table_title=caption, table_id=f"{doc_id}_tab_cqa"),
               ref(doc_id, file_name, sec, "Quality attributes in scope",
                   UFATTR_QUOTE[bool(report)][key])]
        if report:
            src.append(ref(doc_id, file_name, sec, "Process capability and robustness",
                           rows["cap"][key]))
            src.append(ref(doc_id, file_name, sec,
                           "Appendix C — Drug substance quality attribute register",
                           rows["register"][UFATTR_NAME[key]]))
        else:
            src.append(ref(doc_id, file_name, sec, "Quality attributes in scope",
                           "Every attribute in the register is set at an earlier step"))
        out.append(S.QualityAttribute(
            attribute_id=UFATTR_CONCEPT[key], attribute_name=UFATTR_NAME[key],
            attribute_type="CQA", unit=str(r["unit"]),
            acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            analytical_method=({"aggregates_hmw": "AMV-3011",
                                "acidic_variants": "AMV-3013"}.get(key)),
            associated_steps=([P.UNIT_OP_TITLES[str(r["set_by"])]] if report else []),
            criticality_level=str(r["criticality"]), tool1_score=int(r["tool1_score"]),
            rationale_for_criticality=(
                "Measured on the pool this step delivers and reported for the drug substance; "
                "neither formed nor cleared at this step." if report else
                "Carried into the step by the pool; neither formed nor cleared here."),
            source_references=src, metadata=meta()))
    return out


def uf_methods(doc_id, file_name, sec, report):
    rows = uf_rows(report)
    qmap = UFMETHOD_QUOTE[bool(report)]
    out = []
    for mid, mname, mtype, analytes, attrs in UFMETHODS:
        src = [ref(doc_id, file_name, sec, "Analytical methods", rows["refs"][mid]),
               ref(doc_id, file_name, sec, "Analytical methods", qmap[mid])]
        if mid in rows["methperf"]:
            # AMV-3019 is the only method whose validated performance either document renders.
            src.append(ref(doc_id, file_name, sec,
                           "Appendix A — Analytical methods summary" if report
                           else "Analytical methods",
                           rows["methperf"][mid]))
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=mname, method_type=mtype, analytes=analytes,
            associated_attributes=[UFATTR_CONCEPT[a] for a in attrs], validation_status="validated",
            source_references=src, metadata=meta()))
    return out


def uf_studies(doc_id, file_name, report):
    """Only two studies exist for this step: the one-factor-at-a-time ranging and the
    scale-down qualification. No screening and no response-surface design was planned or
    run, and RA-001 required none, so no DoE StudyDesign is asserted.

    The two documents do not describe either study identically, and the annex follows each
    document rather than averaging them. PCR-010 §5.2 records that the univariate levels
    "were assessed against process performance criteria only, and no product quality result is
    reported at any of them", so the report's responses are process-performance responses; the
    plan's §7 criteria still include product quality at every condition. The plan states a run
    count (nine); the report does not, so ``n_runs`` is null there.
    """
    if report:
        uni = [ref(doc_id, file_name, f"{doc_id}_sec_design", "Univariate assessment",
                   "The characterization schedule took each parameter to both edges of its "
                   "characterization range with the other two held at their set-points, and the "
                   "set-point condition was the reference"),
               ref(doc_id, file_name, f"{doc_id}_sec_design",
                   "Characterization levels and process performance",
                   "were assessed against process performance criteria only, and no product "
                   "quality result is reported at any of them")]
        qual = [ref(doc_id, file_name, f"{doc_id}_sec_sdm",
                    "Scale-down model and its qualification",
                    "Qualification compared the model with commercial equivalent runs on the "
                    "quantities that leave the step, which are step yield, final concentration, "
                    "aggregate and charge variants.")]
        responses = ["permeate flux", "processing time", "final concentration at endpoint",
                     "product mass balance closure"]
        n_runs = None
    else:
        uni = [ref(doc_id, file_name, f"{doc_id}_sec_design", "Univariate assessment",
                   "Each parameter is taken to the low and high levels of its characterization "
                   "range with the other parameters at their set-points, and the set-point "
                   "condition itself is executed once as the reference for each parameter."),
               ref(doc_id, file_name, f"{doc_id}_sec_design", "Univariate assessment",
                   "The study is 9 runs in total: 6 runs at an edge and 3 at the set-point")]
        qual = [ref(doc_id, file_name, f"{doc_id}_sec_sdm",
                    "Scale-down model and its qualification",
                    "Qualification compares the small system with commercial and pilot data on "
                    "flux, on process time per diavolume and on the quality of the pool."),
                ref(doc_id, file_name, f"{doc_id}_sec_sdm",
                    "Scale-down model and its qualification",
                    "Step yield is recorded at both scales but is not one of the quantities "
                    "compared, because hold-up volume makes recovery scale dependent.")]
        responses = ["aggregate", "acidic charge variants", "final concentration", "step yield",
                     "permeate mass (diavolume verification)"]
        _lv = P.univariate_levels(UFUO)
        n_runs = int(_lv[["Low level", "High level"]].size + len(_lv))
    return [
        S.StudyDesign(
            study_id="study:ufdf_univariate", study_type="univariate",
            design_name="one-factor-at-a-time ranging", unit_operation=UFUO_NAME,
            factors=list(UFPARAM_CONCEPT), responses=responses, n_runs=n_runs,
            scale_down_model=UFSDM,
            associated_parameters=list(UFPARAM_CONCEPT.values()),
            source_references=uni, metadata=meta()),
        S.StudyDesign(
            study_id="study:ufdf_sdm_qual", study_type="scale_down_qualification",
            unit_operation=UFUO_NAME, scale_down_model=UFSDM,
            source_references=qual, metadata=meta()),
    ]


def uf_concepts():
    from annex_contract.concepts import Concept, ConceptStore
    cs = [Concept(concept_id="step:ufdf", concept_type="PROCESS_STEP",
                  canonical_name=UFUO_NAME,
                  aliases=["UF/DF", "ultrafiltration", "diafiltration",
                           "tangential flow filtration", "formulation", "Step 10"],
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
    """Relations both documents state.

    NOTE the one predicate that is deliberately ABSENT. The closed predicate vocabulary offers
    ``parameter_does_not_significantly_impact_attribute``, and the previous annex used it for
    all three parameters in both documents. Neither document supports it. The plan says "The
    class is an outcome of the study and is not pre-judged in this plan" and names two
    mechanisms that could change product quality; the report says the classification "follows
    from the quality attribute register … and not from a demonstrated null effect on one", and
    records that the quality confirmation does not reach the edges of the characterization
    ranges. A null-effect assertion would be the annex claiming what the report declines to
    claim, so none is emitted.
    """
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]
    rows = uf_rows(report)

    def add(subj, pred, obj, text, sec, quote):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc_id}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[ref(doc_id, file_name, sec, sec, quote)], metadata=meta()))

    param_sec = ("Parameters, ranges and the knowledge space" if report
                 else "Factors, ranges and study type")
    for r in UFPARAM_ROWS:
        name = r["parameter"]
        add("step:ufdf", "step_has_parameter", UFPARAM_CONCEPT[name],
            f"{UFUO_NAME} has process parameter {name}"
            + (f", classified {r['classification']}." if report else "."),
            param_sec, rows["params"][name])
    # step -> equipment. Every statement either document makes about the step's performance is
    # conditional on the scale-down system, and both say so in the same section.
    add("step:ufdf", "step_uses_equipment", "equip:ufdf_sdm",
        "The characterization of the step is executed on a qualified scale-down tangential flow "
        "filtration model of the commercial skid." if report else
        "The planned characterization runs are executed on a scale-down tangential flow "
        "filtration system that must be qualified under SOP-1001 before any run starts.",
        "Scale-down model and its qualification",
        "The studies were executed on a scale-down tangential flow filtration system qualified "
        "as a model of the commercial skid under SOP-1001." if report else
        "no study run may start before that system has been qualified under SOP-1001")
    # step -> attributes. NOT "sets" and NOT "clears": both documents say so explicitly, and the
    # two give different reasons for residual DNA, so the assertion text follows each document.
    for key in UFATTR_KEYS:
        if report:
            text = (f"{UFATTR_NAME[key]} is measured on the pool the step delivers and is "
                    f"reported for the drug substance; it is neither set nor cleared at the step.")
        elif key == "residual_dna":
            text = (f"{UFATTR_NAME[key]} is carried into the step and is in scope because the "
                    f"step fixes the concentration on which a dose is based; it is not assayed "
                    f"in this study.")
        else:
            text = (f"{UFATTR_NAME[key]} is carried into the step and is measured across it, to "
                    f"confirm that the operation does not change it.")
        add("step:ufdf", "step_has_quality_attribute", UFATTR_CONCEPT[key], text,
            "Quality attributes in scope", UFATTR_QUOTE[bool(report)][key])
    # attribute -> acceptance criterion, each on its own @tbl-cqa row, which carries the
    # attribute and its criterion in one span.
    for key in UFATTR_KEYS:
        r = P.cqa_reg[P.cqa_reg.key == key].iloc[0]
        add(UFATTR_CONCEPT[key], "attribute_has_acceptance_criterion", f"lit:{key}_acc",
            f"{UFATTR_NAME[key]} is accepted at {r['acc_low']:g}–{r['acc_high']:g} {r['unit']}.",
            "Quality attributes in scope", rows["cqa"][key])
    # attribute -> method. Only the two attributes this pair assays at the step are linked;
    # residual DNA is reported at the step but neither document names a method for it here.
    for mid, mname, mtype, analytes, attrs in UFMETHODS:
        for a in attrs:
            add(UFATTR_CONCEPT[a], "attribute_measured_by_method", f"method:{mid}",
                f"{UFATTR_NAME[a]} is measured by {mid}.", "Analytical methods",
                UFMETHOD_QUOTE[bool(report)][mid])
    return AssertionStore(run_id=f"gt-{doc_id}", assertions=A, rationales=[])


def uf_report_sections(doc_id, file_name, report):
    from annex_contract.summaries import ReportSection, ReportStatement

    def st(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc_id}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc_id, file_name, sec, sec, quote)])
    if not report:
        return [ReportSection(section_id=f"{doc_id}-summary", title="Plan summary", statements=[
            st(1, "PCP-010 defines the characterization study for the ultrafiltration and "
                  "diafiltration step and reports no results, because it is written before the "
                  "study is executed.",
               "Purpose and scope",
               "It is written before the study is executed and it reports no results."),
            st(2, "No quality attribute in the drug substance register is assigned to the step, "
                  "and no viral clearance or impurity clearance is claimed for it.",
               "Purpose and scope",
               "No quality attribute in the drug substance register is assigned to this step, "
               "and no viral clearance or impurity clearance is claimed for it."),
            st(3, "The step is characterized because it sets the concentration and the buffer of "
                  "the drug substance and because its ranges must be justified before transfer.",
               "Purpose and scope",
               "The step is characterized because it sets the concentration and the buffer of "
               "the drug substance, and because its operating ranges have to be justified before "
               "the process is transferred to the receiving site"),
            st(4, "Membrane selection, formulation buffer composition and the drug product "
                  "operations that follow the step are outside the scope of the plan.",
               "Purpose and scope",
               "Membrane selection, formulation buffer composition and the drug product "
               "operations that follow the step are outside the scope of this plan and of the "
               "drug substance characterization package."),
            st(5, "No drug substance quality attribute is formed or cleared at the step, and "
                  "three attributes are nevertheless in scope.",
               "Quality attributes in scope",
               "No drug substance quality attribute is formed or cleared at this step. Three "
               "attributes are nevertheless in scope"),
            st(6, "Aggregate is the attribute the study follows most closely, because both "
                  "mechanisms of the operation act on the size variant distribution.",
               "Unit operation description and prior knowledge",
               "Both act on the size variant distribution, which is why aggregate is the "
               "attribute followed most closely here."),
            st(7, "RA-001 carried all three parameters into the pre-characterization assessment "
                  "and assigned every one of them to univariate study.",
               "Risk-based prioritization of parameters",
               "RA-001 carried all 3 parameters of this step into the pre-characterization "
               "assessment and assigned every one of them to univariate study."),
            st(8, "No designed experiment is run at the step and no model is fitted to its data.",
               "Statistical methods",
               "No designed experiment is run at this step and no model is fitted to its data."),
            st(9, "The outcome of the study is a set of univariate acceptable ranges and a "
                  "classification per parameter, and not a multivariate design space.",
               "Statistical methods",
               "It is not a multivariate design space, and this plan claims nothing more for it."),
            st(10, "The study is nine runs: six at an edge of a characterization range and three "
                   "at the set-point condition.",
                "Univariate assessment",
                "The study is 9 runs in total: 6 runs at an edge and 3 at the set-point"),
            st(11, "The classification of each parameter is an outcome of the study and is not "
                   "pre-judged in the plan.",
                "Acceptance and decision criteria",
                "The class is an outcome of the study and is not pre-judged in this plan."),
            st(12, "The plan states that the report will give a proven acceptable range for each "
                   "parameter against aggregate and acidic charge variants.",
                "Proven acceptable ranges (planned analysis)",
                "The report will state a proven acceptable range (PAR) for each parameter, "
                "against the two attributes measured across the step, which are aggregate and "
                "acidic charge variants."),
            st(13, "Every planned proven acceptable range is bounded by the levels actually "
                   "executed and by the assumption that the other parameters sit at set-point.",
                "Proven acceptable ranges (planned analysis)",
                "It is bounded by the levels actually executed, and it is bounded by the "
                "assumption that the other parameters are at their set-points."),
            st(14, "Neither the plan nor its report will describe the result as a design space.",
                "Proven acceptable ranges (planned analysis)",
                "Neither this plan nor its report will describe the result as a design space."),
            st(15, "Step yield at small scale is reported as an indicator of consistent operation "
                   "and is not used to set the commercial yield expectation.",
                "Scale-down model and its qualification",
                "Step yield at small scale will therefore be reported as an indicator of "
                "consistent operation and will not be used to set the commercial yield expectation."),
        ])]
    return [ReportSection(section_id=f"{doc_id}-summary", title="Report summary", statements=[
        st(1, "The step forms no critical quality attribute and is credited with no impurity or "
              "virus clearance.",
           "Executive summary",
           "The step forms no critical quality attribute and is credited with no impurity or "
           "virus clearance."),
        st(2, "All three parameters of the step are classified as key process parameters, and "
              "none is critical or well controlled critical.",
           "Parameter classification",
           "All 3 parameters of this step are classified as key process parameters under the "
           "decision logic of SOP-4001, and none is a critical process parameter or a well "
           "controlled critical process parameter."),
        st(3, "The classification follows from the quality attribute register and not from a "
              "demonstrated null effect on an attribute.",
           "Parameter classification",
           "The classification follows from the quality attribute register, in which no drug "
           "substance attribute is set or cleared at this step, and not from a demonstrated null "
           "effect on one."),
        st(4, "The step contributes no element to the design space of the A-Mab drug substance "
              "process.",
           "Design space",
           "This step contributes no element to the design space of the A-Mab drug substance "
           "process."),
        st(5, "No proven acceptable range is claimed for any parameter of the step; what the "
              "study supports is an operating range whose acceptance basis is process performance.",
           "Proven acceptable ranges",
           "No proven acceptable range is claimed for any parameter of this step."),
        st(6, "At its set-points the step delivered a product yield of 97.1% and 54.6 kg of drug "
              "substance at 75 g/L, closing the train at a cumulative product yield of 83.2%.",
           "Executive summary",
           "At its set-points the step delivered a product yield of 97.1% and 54.6 kg of drug "
           "substance at 75 g/L, which closes the train at a cumulative product yield of 83.2%."),
        st(7, "The univariate levels were assessed against process performance criteria only, and "
              "no product quality result is reported at any of them.",
           "Characterization levels and process performance",
           "were assessed against process performance criteria only, and no product quality "
           "result is reported at any of them"),
        st(8, "The quality confirmation covers the normal operating ranges and does not extend to "
              "the edges of the characterization ranges.",
           "Product quality across the step",
           "It does not extend to the edges of the characterization ranges, where the evidence "
           "from this study is process performance only"),
        st(9, "Residual load buffer was not assayed; the completeness of the exchange is taken "
              "from the washout relation and not from a measurement.",
           "Executive summary",
           "Residual load buffer was not assayed, and the completeness of the exchange is taken "
           "from the washout relation given in §4.1."),
        st(10, "The drug substance attributes measured after the step meet their acceptance "
               "criteria at commercial scale with wide margin.",
            "Process capability and robustness",
            "The drug substance attributes measured after this step meet their acceptance "
            "criteria at commercial scale with wide margin"),
        st(11, "Acidic charge variants carry the tightest capability of the three attributes "
               "measured after the step, at a Cpk of 4.26.",
            "Process capability and robustness",
            "Acidic charge variants carry the tightest capability of the three, at a Cpk of 4.26"),
        st(12, "The tightest capability of the drug substance as a whole belongs to MVM "
               "parvovirus clearance, credited to anion exchange and virus filtration.",
            "Process capability and robustness",
            "It belongs to Viral clearance — MVM (parvovirus), at a Cpk of 1.51, and it is "
            "credited to anion exchange and small virus retentive filtration (PCR-008 and "
            "PCR-009), which are the two steps that clear parvovirus."),
        st(13, "The capability figures are estimates from qualified scale-down models and not "
               "measurements at commercial scale.",
            "Process capability and robustness",
            "They are estimates from qualified scale-down models under the sampling described in "
            "§3.5, and they are not measurements at commercial scale."),
        st(14, "No designed experiment was run at the step and none was planned, so the screening "
               "and response surface framework does not apply here.",
            "Statistical methods",
            "No designed experiment was run at this step, and none was planned, so the screening "
            "and response surface framework used at the six steps that carry designed experiments "
            "does not apply here."),
        st(15, "Interactions between the three parameters are not quantified, and the study "
               "cannot exclude one.",
            "Discussion",
            "which means that interactions between the three parameters are not quantified and "
            "that this study cannot exclude one"),
        st(16, "Two deviations were recorded; both were investigated and impact assessed, and "
               "both were dispositioned as retained.",
            "Deviations from the plan",
            "Both were investigated, both were impact assessed, and both were dispositioned as "
            "retained"),
        st(17, "Neither deviation changed a parameter range, a classification or a conclusion of "
               "the report.",
            "Conclusions",
            "Both deviations recorded during execution were investigated and retained, and "
            "neither changed a range, a classification or a conclusion."),
        st(18, "The outcome of the report rolls up into the Process Characterization Master "
               "Report (PCMR-001).",
            "Conclusions", "The outcome of this report rolls up into PCMR-001."),
    ])]


# --------------------------------------------------------------------------- #
# Report-only discourse layer (PCR-010 only).                                   #
# --------------------------------------------------------------------------- #
# Argument-structure spans over the re-authored PCR-010. Every quote is verbatim  #
# prose of the RENDERED report. The argument of a step that forms and clears       #
# nothing is largely an argument about what is NOT claimed, and the re-authored     #
# report is more careful about that than its predecessor: it refuses a design       #
# space, refuses a proven acceptable range, and refuses to read the KPP              #
# classification as a demonstrated null effect. The supported_by edges are the       #
# real evidence edges — the justification span is the sentence the claim span rests   #
# on. Tuple fields: (suffix, role, section, quote, supported_by, restates, bounds).    #
# PCR-010 carries NO registered weak claim, so no span is withheld for that layer.     #
# --------------------------------------------------------------------------- #
UF_RHET_SPANS = [
    ("R01", "claim", "Executive summary",
     "The step forms no critical quality attribute and is credited with no impurity or virus "
     "clearance.", ["R02", "R03"], None, None),
    ("R02", "mechanistic_warrant", "Platform and prior product knowledge",
     "The mechanism is also simple enough to state in advance, since a membrane that retains the "
     "antibody and passes small solutes changes the composition of the pool and leaves the "
     "product alone.", [], None, None),
    ("R03", "cross_step_credit", "Product and unit operation",
     "The glycan, charge variant and aggregate attributes are established in the production "
     "bioreactor (PCR-003), and host cell protein, residual DNA and leached Protein A are cleared "
     "by the chromatography steps (PCR-005, PCR-007 and PCR-008).", [], None, None),
    ("R04", "hedge", "Product and unit operation",
     "Some clearance of small solutes occurs across any membrane operation, but it is not "
     "predictable and no claim is made for it, so the impurity levels entering this step are "
     "taken to carry through unchanged to the drug substance.", [], None, None),
    ("R05", "problem_statement", "Platform and prior product knowledge",
     "Two mechanisms could break that expectation, and both were carried into the study.",
     [], None, None),
    ("R06", "mechanistic_warrant", "Platform and prior product knowledge",
     "Shear at the membrane surface can generate aggregate, and transmembrane pressure is the "
     "parameter that governs it. Holding the antibody at high concentration through the second "
     "concentration phase can do the same, and the final concentration is the parameter that "
     "governs that.", [], None, None),
    ("R07", "justification", "Platform and prior product knowledge",
     "RA-001 scored both as low risk on the platform history recorded there, but they are "
     "nevertheless the reason the characterization ranges were set wider than the normal "
     "operating ranges.", [], None, None),
    ("R08", "claim", "Quality attributes in scope",
     "Three drug substance attributes are measured on the pool this step delivers, and they are "
     "the attributes in scope for this report", ["R09"], None, None),
    ("R09", "mechanistic_warrant", "Quality attributes in scope",
     "Aggregate is the attribute with a mechanism at this step. It is formed in the production "
     "bioreactor (PCR-003) and reduced principally at cation exchange (PCR-007), and the "
     "concentration and recirculation applied here are the last opportunity in the process to add "
     "to it.", [], None, None),
    ("R10", "deferral", "Quality attributes in scope",
     "The glycan attributes, host cell protein and leached Protein A are covered by the reports "
     "for the steps that set or clear them, and the full register with those attributions is "
     "given in Appendix C.", [], None, None),
    ("R11", "justification", "Risk based prioritization and parameter selection",
     "The three parameters scored alike, and the reason is visible in the effect column, where "
     "none of the failure modes reaches a quality attribute.", [], None, None),
    ("R12", "claim", "Risk based prioritization and parameter selection",
     "On that basis the assessment concluded that a designed experiment was not justified and "
     "that univariate study of each range would support the operating limits the step needs.",
     ["R11"], None, None),
    ("R13", "problem_statement", "Risk based prioritization and parameter selection",
     "A low score is not the same as no study.", [], None, None),
    ("R14", "problem_statement", "Scale-down model and its qualification",
     "One feature of the model cannot be matched to the commercial skid by scaling, and it is the "
     "hold-up volume of the recirculation loop and the membrane housing, because buffer held "
     "there is recovered with the pool at the flush and dilutes it.", [], None, None),
    ("R15", "bounded_conclusion", "Scale-down model and its qualification",
     "It supports operating ranges for parameters that govern process performance, and it "
     "supports the statement that the drug substance attributes are unchanged across the step, "
     "but it is not asked to support a quality attribute claim of its own, because the step makes "
     "none.", [], None, "R31"),
    ("R16", "deferral", "Analytical methods",
     "Validated performance for the concentration method is given in Appendix A. Performance for "
     "the other two methods is held in their own validation reports.", [], None, None),
    ("R17", "mechanistic_warrant", "Parameters, ranges and the knowledge space",
     "Diafiltration removes a fully permeable solute exponentially, so the residual fraction of "
     "the load buffer after N diavolumes is e raised to the power minus N.", [], None, None),
    ("R18", "claim", "Parameters, ranges and the knowledge space",
     "The range covers a wide swing in the completeness of the exchange while leaving the "
     "exchanged species at trace level throughout it.", ["R17"], None, None),
    ("R19", "hedge", "Parameters, ranges and the knowledge space",
     "This is a design calculation for an ideal, fully permeable solute in a well mixed "
     "retentate, and it is the basis of the range and not a measured result.", [], None, None),
    ("R20", "justification", "Parameters, ranges and the knowledge space",
     "The mechanism that moves transmembrane pressure during a batch is membrane fouling, and "
     "fouling moves it upward, so the characterization range was extended on the high side only.",
     [], None, None),
    ("R21", "justification", "Parameters, ranges and the knowledge space",
     "A range that is narrow relative to the assay controlling it cannot be held, and this range "
     "is not narrow on that measure.", [], None, None),
    ("R22", "claim", "Univariate assessment",
     "A multivariate design was neither run nor needed.", ["R23", "R24"], None, None),
    ("R23", "justification", "Univariate assessment",
     "Interactions matter when two parameters act on the same quality attribute, and no parameter "
     "of this step is linked to one in the register, so there is no governed attribute on which "
     "an interaction could be estimated or classified.", [], None, None),
    ("R24", "justification", "Univariate assessment",
     "The three parameters also act through different mechanisms and are read out on different "
     "responses, and that is the second reason a factorial design would have added cost without "
     "adding process understanding.", [], None, None),
    ("R25", "claim", "Nominal batch performance and mass balance",
     "The step delivered drug substance at its target concentration and closed the product mass "
     "balance for the batch.", ["R26", "R27"], None, None),
    ("R26", "justification", "Nominal batch performance and mass balance",
     "The step delivered 54.6 kg of drug substance at 75 g/L, which is 728 L of pool.",
     [], None, None),
    ("R27", "justification", "Nominal batch performance and mass balance",
     "Product loss across the step was 2.9% of the mass entering it, and the platform attributes "
     "it to hold-up volume and to retention on the membrane.", [], None, None),
    ("R28", "problem_statement", "Characterization levels and process performance",
     "None of those is a quality criterion, and none of them could be, because no attribute of "
     "the drug substance register is set or cleared at this step.", [], None, None),
    ("R29", "justification", "Drug substance concentration and its measurement",
     "The method accounts for 22.0% of the observed variance in the reported concentration, so "
     "most of the spread seen between batches is process and not assay.", [], None, None),
    ("R30", "justification", "Drug substance concentration and its measurement",
     "One run finished its second concentration phase below target, at 71.5 g/L, and the "
     "shortfall of 3.5 g/L is 3.9 times the intermediate precision of the assay at the target, so "
     "it is a real difference and not a measurement artefact.", [], None, None),
    ("R31", "claim", "Product quality across the step",
     "The drug substance attributes measured after the step meet their acceptance criteria",
     ["R39", "R41"], None, None),
    ("R32", "bounded_conclusion", "Product quality across the step",
     "The quality confirmation covers the normal operating ranges of the three parameters, which "
     "is the region the simulated batches concentrate in.", [], None, "R31"),
    ("R33", "claim", "Design space",
     "This step contributes no element to the design space of the A-Mab drug substance process.",
     ["R34"], None, None),
    ("R34", "justification", "Design space",
     "None of the three parameters characterized here is linked to a critical quality attribute, "
     "so there is nothing at this step for a design space to assure.", [], None, None),
    ("R35", "bounded_conclusion", "Design space",
     "They rest on the scale-down model described in §3.1, whose warrant is process performance "
     "and unchanged quality and not a quality claim of its own.", [], None, "R33"),
    ("R36", "claim", "Proven acceptable ranges",
     "No proven acceptable range is claimed for any parameter of this step.", ["R37"], None, None),
    ("R37", "justification", "Proven acceptable ranges",
     "A proven acceptable range is the range of a parameter over which a named quality attribute "
     "stays inside its acceptance criterion, where the range is proven by supporting data, and "
     "that definition needs a governed attribute, which this step does not have.", [], None, None),
    ("R38", "cross_step_credit", "Proven acceptable ranges",
     "Aggregate is bounded at the production bioreactor and at cation exchange (PCR-003 and "
     "PCR-007), charge variants are bounded at the bioreactor and at the low pH hold (PCR-003 and "
     "PCR-006), and residual DNA is bounded across the three chromatography steps (PCR-005, "
     "PCR-007 and PCR-008).", [], None, None),
    ("R39", "justification", "Process capability and robustness",
     "Acidic charge variants carry the tightest capability of the three, at a Cpk of 4.26, with a "
     "mean of 22.3 % against a limit of 40 %, a margin of 17.7 %, and a highest simulated batch "
     "of 27.2 %.", [], None, None),
    ("R40", "claim", "Process capability and robustness",
     "The drug substance attributes measured after this step meet their acceptance criteria at "
     "commercial scale with wide margin", ["R39", "R41"], None, None),
    ("R41", "justification", "Process capability and robustness",
     "Aggregate is the most capable of the three, at a Cpk of 16.1.", [], None, None),
    ("R42", "hedge", "Process capability and robustness",
     "A step with no effect on an attribute contributes nothing to the spread of that attribute, "
     "which is why the capability of the drug substance is not by itself a sensitive test of this "
     "step.", [], None, None),
    ("R43", "cross_step_credit", "Process capability and robustness",
     "It belongs to Viral clearance — MVM (parvovirus), at a Cpk of 1.51, and it is credited to "
     "anion exchange and small virus retentive filtration (PCR-008 and PCR-009), which are the "
     "two steps that clear parvovirus.", [], None, None),
    ("R44", "bounded_conclusion", "Process capability and robustness",
     "They are estimates from qualified scale-down models under the sampling described in §3.5, "
     "and they are not measurements at commercial scale.", [], None, "R40"),
    ("R45", "claim", "Parameter classification",
     "All 3 parameters of this step are classified as key process parameters under the decision "
     "logic of SOP-4001, and none is a critical process parameter or a well controlled critical "
     "process parameter.", ["R46", "R47"], None, None),
    ("R46", "justification", "Parameter classification",
     "The classification follows from the quality attribute register, in which no drug substance "
     "attribute is set or cleared at this step, and not from a demonstrated null effect on one.",
     [], None, None),
    ("R47", "justification", "Parameter classification",
     "It is nevertheless classified on process performance, because this step governs no "
     "attribute against which such an effect could be classified.", [], None, None),
    ("R48", "restatement", "Contribution to the control strategy",
     "It controls no critical quality attribute, and it provides no impurity clearance credit and "
     "no viral clearance credit.", [], "R01", None),
    ("R49", "claim", "Discussion",
     "The step is understood well enough to transfer, and part of the reason is that there is "
     "little to understand, since a membrane that retains the antibody and passes small solutes "
     "changes the buffer and leaves the product alone.", ["R50"], None, None),
    ("R50", "justification", "Discussion",
     "The study confirmed that expectation against the drug substance attributes measured on the "
     "pool the step delivers, and it established ranges for the three parameters that govern how "
     "the step performs.", [], None, None),
    ("R51", "hedge", "Discussion",
     "Confidence in the scale-down model is high for process performance and adequate for what is "
     "claimed about quality.", [], None, None),
    ("R52", "bounded_conclusion", "Discussion",
     "The third is that the ranges hold for the membrane chemistry, the membrane loading and the "
     "formulation buffer used here.", [], None, "R49"),
    ("R53", "bounded_conclusion", "Discussion",
     "That conclusion follows from the absence of a quality linkage and not from a demonstration "
     "of robustness against a quality attribute, and it is bounded accordingly.", [], None, "R45"),
    ("R54", "justification",
     "DEV-010-01 — Transmembrane pressure excursion above the normal operating range",
     "Pressure rose through the first concentration phase and returned inside the control range "
     "once the diafiltration began, which is the signature of transient membrane fouling and not "
     "of a control failure, and the root cause was recorded on that basis.", [], None, None),
    ("R55", "deviation_disposition",
     "DEV-010-01 — Transmembrane pressure excursion above the normal operating range",
     "The run was retained, and no range or classification was changed.", ["R54"], None, None),
    ("R56", "justification", "DEV-010-02 — Final drug substance concentration below target",
     "The investigation traced the shortfall to residual hold-up volume. Buffer held in the "
     "recirculation loop and the membrane housing was recovered with the pool at the flush, and "
     "it diluted the pool below the concentration the phase had reached.", [], None, None),
    ("R57", "deviation_disposition",
     "DEV-010-02 — Final drug substance concentration below target",
     "The pool was returned to the skid, concentrated to target and confirmed by the ultraviolet "
     "absorbance method (AMV-3019).", ["R56"], None, None),
    ("R58", "restatement", "Conclusions",
     "All 3 parameters are classified as key process parameters and none is linked to a critical "
     "quality attribute, so the step contributes no element to the design space, and it claims no "
     "proven acceptable range, no impurity clearance and no viral clearance.", [], "R45", None),
]


def uf_rhetorical_spans(doc_id, file_name):
    """Rhetorical / argument-structure spans over the PCR-010 report (report-only)."""
    out = []
    for suffix, role, sec, quote, sup, res, bnd in UF_RHET_SPANS:
        out.append(S.RhetoricalSpan(
            span_id=f"{doc_id}-{suffix}", section=sec, role=role,
            source_reference=ref(doc_id, file_name, f"{doc_id}_sec_rhet", sec,
                                 " ".join(quote.split())),
            supported_by=[f"{doc_id}-{s}" for s in sup],
            restates=(f"{doc_id}-{res}" if res else None),
            bounds=(f"{doc_id}-{bnd}" if bnd else None)))
    return out


def uf_inventory(doc_id, file_name, dtype):
    return S.DocumentInventoryItem(
        document_id=doc_id, file_name=file_name, predicted_document_type=dtype,
        product_name_candidates=["A-Mab"], process_name_candidates=[UFUO_NAME],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["process characterization", "ultrafiltration", "diafiltration",
                     "formulation", "tangential flow filtration", "parameter classification"],
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
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=uf_attributes(doc, f, f"{doc}_sec_cqa",
                                                                   report=False)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=uf_params(doc, f, f"{doc}_sec_param", classified=False)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=uf_methods(doc, f, f"{doc}_sec_methods", report=False)),
    ]
    return S.GroundTruthAnnex(
        weak_claims=build_weak_claims(doc, f),
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "UF/DF forms and clears no drug-substance CQA, so there is no DesignSpace. The three "
            "attributes of @tbl-cqa are carried into the step: aggregate and acidic charge "
            "variants are measured across it, and residual DNA is in scope only because the step "
            "fixes the concentration on which a dose is based and is not assayed in this study.",
            "No DoE: the plan states that no designed experiment is run and no model is fitted, "
            "so the only studies are the univariate ranging (9 runs) and the scale-down "
            "qualification.",
            "ProcessParameter.PAR is null. The register's par_low/par_high columns are what the "
            "plan renders as the 'Range studied' (characterization) column, and the plan states "
            "that classification and the proven acceptable ranges are OUTPUTS of the study, so "
            "parameter_type is 'unclassified' and no PAR is recorded.",
            "No parameter_does_not_significantly_impact_attribute assertion is emitted. The plan "
            "is prospective, names two mechanisms that could change product quality, and says "
            "'The class is an outcome of the study and is not pre-judged in this plan'; a null-"
            "effect assertion would be a characterization outcome that cannot exist yet.",
            "Process-performance measures (buffer exchange, final concentration, step yield, mass "
            "balance) have no dedicated field; captured via studies/report_sections/assertions.",
            "PCP-010 §8 plans a proven acceptable range per parameter. Its report declines to "
            "claim one (PCR-010 §7); both records are true of their own document, and the "
            "difference is a plan-to-report divergence rather than an annex error.",
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
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=uf_attributes(doc, f, f"{doc}_sec_cqa",
                                                                   report=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_param",
                                  parameters=uf_params(doc, f, f"{doc}_sec_param", classified=True)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=uf_methods(doc, f, f"{doc}_sec_methods", report=True)),
    ]
    return S.GroundTruthAnnex(
        weak_claims=build_weak_claims(doc, f),
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT + [
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "No DesignSpace. PCR-010 §6 opens 'This step contributes no element to the design "
            "space of the A-Mab drug substance process' and gives the reason: none of its three "
            "parameters is linked to a critical quality attribute, so there is nothing for a "
            "design space to assure.",
            "proven_acceptable_ranges is EMPTY, and this is the correction the re-authored report "
            "forces. PCR-010 §7 states 'No proven acceptable range is claimed for any parameter "
            "of this step' — a PAR needs a governed attribute and the step has none — and repeats "
            "the refusal in the executive summary and the conclusions. The previous annex "
            "asserted the opposite (one PAR per parameter, each equal to the characterization "
            "range). ProcessParameter.PAR is null for the same reason; the register's "
            "par_low/par_high columns are rendered as the 'Char. range' column of @tbl-params.",
            "No parameter_does_not_significantly_impact_attribute assertion is emitted. §9 states "
            "that the classification 'follows from the quality attribute register … and not from "
            "a demonstrated null effect on one', and §5.4 records that the quality confirmation "
            "does not extend to the edges of the characterization ranges. The absence of a "
            "quality LINKAGE is captured instead, which is what the report argues.",
            "No DoE was run and none was planned, so the only StudyDesign records are the "
            "univariate ranging and the scale-down qualification; there are no screening or "
            "response-surface effect/coefficient objects to annotate. The univariate levels were "
            "judged on process performance only, so the study's responses are process responses.",
            "Process-performance results (step yield, product mass, mass balance, cumulative "
            "yield) and commercial-scale capability have no dedicated field; they are carried as "
            "report_sections statements and as QualityAttribute source references on the "
            "@tbl-cap rows.",
            "rhetorical_spans are verbatim report prose; PCR-010 carries no weak_claims, so no "
            "sentence is withheld from the assertion or span layers.",
        ],
        inventory=uf_inventory(doc, f, "process_characterization_report"),
        entities=entities, studies=uf_studies(doc, f, report=True),
        report_sections=uf_report_sections(doc, f, report=True),
        assertions=uf_assertions(doc, f, report=True), concepts=uf_concepts(),
        rhetorical_spans=uf_rhetorical_spans(doc, f))


# =========================================================================== #
# PTP-001 — Process Transfer Plan (Cambridge Development -> Grafton Commercial). #
# --------------------------------------------------------------------------- #
# A corpus-spanning document (not a single unit op): the ground truth captures  #
# the two sites, the process train (Steps 3-10), the CQAs the control strategy  #
# exists to control, the instrumented scale-down systems and the validated      #
# analytical methods the transfer depends on, and — the distinctive object for  #
# this document type — the transfer gaps (TransferGap + transfer_has_gap).      #
# =========================================================================== #
PTP_FILE = "PTP-001_transfer.docx"

# The six transfer gaps of PTP-001 §8. The re-authored plan carries a DIFFERENT register
# from the one this region was first written against, in two ways the annex has to follow
# rather than paper over:
#   * the gaps are keyed to materials, critical reagent lots, the unconfirmed design space,
#     scale-dependent matching, documentation and classification — not to the earlier set,
#     and the identifiers were reused for different subjects (the old GAP-01 was the
#     unconfirmed design space, which is now GAP-03);
#   * two of them, GAP-02 and GAP-04, are recorded "In progress" and not "Open", because
#     their mitigations have already started. Asserting "open" for those two would state
#     the opposite of the register the document renders. "None is closed" still holds, and
#     is a separate claim from "every one is open".
# Each entry is (gap_id, gap_area, the rendered cells of its row of @tbl-gaps, the §8
# narrative sentence that argues it). description / impact / mitigation / status are read
# out of the cells, so a record and the row it anchors on cannot drift apart.
PTP_GAPS = [
    ("GAP-01", "materials",
     ("GAP-01", "Materials",
      "Alternate Protein A resin has no platform bridging data",
      "Second resin cannot enter commercial use on platform data",
      "Independent characterization per RA-004 before use", "Open"),
     "The alternate Protein A resin cannot be qualified on platform data (GAP-01), because "
     "RA-004 assessed that resin and concluded that independent characterization is required, "
     "with no bridging from the platform data set."),
    ("GAP-02", "analytical_method",
     ("GAP-02", "Analytical method",
      "Critical reagent lots for the HCP and leached Protein A assays not bridged",
      "A reagent lot difference can present as an impurity difference",
      "Reagent bridging study during method transfer", "In progress"),
     "The two immunoassays are the transfer risk that surfaces last (GAP-02). HCP and leached "
     "Protein A are both measured by immunoassay, both depend on critical reagent lots, and "
     "both report on impurities the drug substance specification covers."),
    ("GAP-03", "validation",
     ("GAP-03", "Validation",
      "Design space not confirmed at commercial scale at the edges of its ranges",
      "Operation near a range edge rests on model prediction",
      "Qualification inside the NOR; edge moves under change control", "Open"),
     "The design space is defined on qualified scale-down models and is not confirmed at "
     "commercial scale at the edges of its ranges (GAP-03). Movement towards the edge of a "
     "range at the receiving site is supported by the fitted models and by the scale-down "
     "data, and not by experience at scale."),
    ("GAP-04", "equipment",
     ("GAP-04", "Equipment",
      "Scale-dependent parameters cannot be matched setting for setting",
      "Small-scale performance may not reproduce at scale",
      "Performance matching per SOP-1001, tested in engineering runs", "In progress"),
     "Scale-dependent parameters are matched on the performance they produce and not setting "
     "for setting (GAP-04), which is a weaker warrant than a direct match."),
    ("GAP-05", "documentation",
     ("GAP-05", "Documentation",
      "Procedures and method validations cited are sending site documents",
      "A batch record could cite a document the receiving site lacks",
      "Document mapping table issued with the process description", "Open"),
     "The characterization package cites sending site procedures and method validation records "
     "while the receiving site holds its own set, so a mapping table is issued with the process "
     "description (GAP-05)."),
    ("GAP-06", "control_strategy",
     ("GAP-06", "Control strategy",
      "Parameter classification is an output of the campaign, not yet complete",
      "The batch record cannot yet state which parameters are critical",
      "Interim operation to platform set-points and NORs", "Open"),
     "Parameter classification is an output of the campaign, so the batch record cannot yet "
     "state which parameters are critical (GAP-06)."),
]

PTP_STEP_KEYS = list(P.CFG.train_order)
PTP_CQA_KEYS = list(P.cqa_reg["key"])

# The rendered captions of the tables PTP-001 prints, as (table_title, table_id). The
# caption is metadata on the reference, never the anchor: the anchor is the row.
PTP_TABLES = {
    "train": ("The A-Mab drug substance process train and the role of each step.",
              "PTP-001_tab_train"),
    "cqa": ("Drug substance quality attributes, acceptance criteria and criticality.",
            "PTP-001_tab_cqa"),
    "equip": ("Instrumented scale-down systems used in the characterization studies.",
              "PTP-001_tab_equip"),
    "method": ("Validated performance records held for the analytical methods.",
               "PTP-001_tab_methods"),
    "gap": ("Transfer gap register, with the impact and the closing action for each gap.",
            "PTP-001_tab_gaps"),
}


_PTP_ROWS = None


def ptp_rows():
    """``{register -> {key -> rendered table row}}`` for every register PTP-001 prints.

    The plan renders five registers straight out of the seeded model (the process train, the
    CQA register, the scale-down equipment list, the analytical-method performance table) or
    out of its own §8 (the gap register). Rebuilding each row here from the same source keeps
    every record anchored on the span that carries both ends of what it asserts — the step
    and its role, the attribute and its acceptance criterion, the gap and its closing action —
    instead of on a caption that would stand in for the whole table.
    """
    global _PTP_ROWS
    if _PTP_ROWS is None:
        cq = P.all_cqas()
        eq = P.equipment_df()[["Equipment", "Description"]]
        meth = P.method_perf_df(precision_with_unit=True)
        _PTP_ROWS = {
            # ``train_row_quotes`` is shared with PCMP-001 and PCMR-001 and is defined further
            # down the file, so the registers are built on first use rather than at import.
            "train": train_row_quotes(),
            "cqa": row_quotes(cq, PTP_CQA_KEYS, P._auto_floatfmt(cq)),
            "equip": row_quotes(eq, eq["Equipment"]),
            "method": row_quotes(meth, meth["Method"], P._auto_floatfmt(meth)),
            # The gap register is authored prose in the .qmd, not a DataFrame; the rendered row
            # is its cells joined, which is what a docx table row collapses to.
            "gap": {g[0]: " ".join(g[2]) for g in PTP_GAPS},
        }
    return _PTP_ROWS


def _ptp_ref(section_id, section_title, quote, table=None):
    tt, tid = PTP_TABLES[table] if table else (None, None)
    return ref("PTP-001", PTP_FILE, f"PTP-001_sec_{section_id}", section_title, quote,
               table_title=tt, table_id=tid)


def ptp_inventory():
    return S.DocumentInventoryItem(
        document_id="PTP-001", file_name=PTP_FILE, predicted_document_type="process_transfer_plan",
        product_name_candidates=["A-Mab"], process_name_candidates=["A-Mab drug substance"],
        site_candidates=[P.SENDING_SITE, P.RECEIVING_SITE], date_candidates=[P.EFFECTIVE_DATE],
        main_topics=["technology transfer", "process transfer", "site equivalency",
                     "scale-down model", "analytical method transfer", "gap analysis",
                     "PPQ", "control strategy"],
        rationale=f"Title block declares document class '{P.DOC_REGISTRY['PTP-001'][0]}'.",
        source_references=[ref("PTP-001", PTP_FILE, "Title block", "Title block",
                               title_block_quote("PTP-001"))],
        metadata=meta())


def ptp_sites():
    """The two sites, each anchored on the §3 clause that names it AND gives its role.

    The bare location ("Cambridge, MA") occurs in the title block, in §1 and in §3, so it
    identifies nothing on its own; the clause carries both ends of the relation.
    """
    return [
        S.ManufacturingSite(
            site_id="site:cambridge", site_name=P.SENDING_SITE, site_role="sending",
            location="Cambridge, MA",
            source_references=[_ptp_ref("sites", "Sending and receiving sites",
                                        f"The sending site is {P.SENDING_SITE}")],
            metadata=meta()),
        S.ManufacturingSite(
            site_id="site:grafton", site_name=P.RECEIVING_SITE, site_role="receiving",
            location="Grafton, WI",
            source_references=[_ptp_ref("sites", "Sending and receiving sites",
                                        f"the receiving site is {P.RECEIVING_SITE}")],
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
            source_references=[_ptp_ref("process", "Product and process description",
                                        ptp_rows()["train"][key], table="train")],
            metadata=meta()))
    return out


def ptp_cqas():
    out = []
    for r in P.cqa_reg.to_dict("records"):
        out.append(S.QualityAttribute(
            attribute_id=f"attr:{r['key']}", attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"], acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[_ptp_ref("control_strategy", "Control strategy",
                                        ptp_rows()["cqa"][r["key"]], table="cqa")],
            metadata=meta()))
    return out


def ptp_equipment():
    """The instrumented scale-down systems §5 lists, each on its own row of @tbl-equip."""
    eq = P.equipment_df()
    out = []
    for r in eq.to_dict("records"):
        out.append(S.Equipment(
            equipment_id=f"equip:{r['Equipment']}", equipment_name=r["Equipment"],
            equipment_type=r["Description"], site_name=P.SENDING_SITE,
            source_references=[_ptp_ref("sdm", "Scale-down model and comparability strategy",
                                        ptp_rows()["equip"][r["Equipment"]], table="equip")],
            metadata=meta()))
    return out


def ptp_methods():
    """The validated analytical methods §6.2 tabulates, each on its own row of @tbl-methods.

    ``validation_status`` follows the register rather than the caption: one entry is recorded
    as verification-qualified and is not claimed as a full validation.
    """
    out = []
    for r in P.csv("dev_methods.csv").to_dict("records"):
        verified = "verification-qualified" in r["name"]
        out.append(S.AnalyticalMethod(
            method_id=r["id"], method_name=r["name"],
            validation_status="verification-qualified" if verified else "validated",
            source_references=[_ptp_ref("methods", "Analytical methods",
                                        ptp_rows()["method"][r["id"]], table="method")],
            metadata=meta()))
    return out


def ptp_gaps():
    """The six §8 gaps: the narrative sentence that argues each, plus its register row."""
    out = []
    for gid, area, cells, prose_q in PTP_GAPS:
        out.append(S.TransferGap(
            gap_id=gid, gap_area=area, description=cells[2], impact=cells[3],
            mitigation=cells[4], status=cells[5].lower().replace(" ", "_"),
            source_references=[
                _ptp_ref("gaps", "Gap analysis", prose_q),
                _ptp_ref("gaps", "Gap analysis", ptp_rows()["gap"][gid], table="gap"),
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
    for r in P.cqa_reg.to_dict("records"):
        cs.append(Concept(concept_id=f"attr:{r['key']}", concept_type="QUALITY_ATTRIBUTE",
                          canonical_name=r["cqa"], aliases=[r["key"]], review_status="human_verified"))
    for sid, name in [("site:cambridge", P.SENDING_SITE), ("site:grafton", P.RECEIVING_SITE)]:
        cs.append(Concept(concept_id=sid, concept_type="MANUFACTURING_SITE", canonical_name=name,
                          review_status="human_verified"))
    for r in P.csv("dev_methods.csv").to_dict("records"):
        cs.append(Concept(concept_id=f"method:{r['id']}", concept_type="ANALYTICAL_METHOD",
                          canonical_name=r["name"], aliases=[r["id"]],
                          review_status="human_verified"))
    for r in P.equipment_df().to_dict("records"):
        cs.append(Concept(concept_id=f"equip:{r['Equipment']}", concept_type="EQUIPMENT",
                          canonical_name=r["Description"], aliases=[r["Equipment"]],
                          review_status="human_verified"))
    for gid, _area, _cells, _q in PTP_GAPS:
        cs.append(Concept(concept_id=f"gap:{gid}", concept_type="TRANSFER_GAP",
                          canonical_name=gid, review_status="human_verified"))
    return ConceptStore(run_id="gt-ptp", concepts=cs)


def ptp_assertions():
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    A = []
    n = [0]

    def add(subj, pred, obj, text, sec_id, sec, quote, table=None):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"PTP-001-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text,
            source_references=[_ptp_ref(sec_id, sec, quote, table=table)],
            metadata=meta()))

    for key in PTP_STEP_KEYS:
        uo = P.CFG.unit_op(key)
        title = P.UNIT_OP_TITLES.get(key, uo.name)
        add("process:amab_ds", "process_has_step", f"step:{key}",
            f"The A-Mab drug-substance process has the step {title}.",
            "process", "Product and process description", ptp_rows()["train"][key], table="train")
    # transfer -> gap, anchored on the register row, which carries the gap, its impact, the
    # action that closes it and its status in one span.
    for gid, area, cells, _prose_q in PTP_GAPS:
        add("transfer:amab_ds", "transfer_has_gap", f"gap:{gid}",
            f"The transfer has {area} gap {gid}: {cells[2]} ({cells[5].lower()}).",
            "gaps", "Gap analysis", ptp_rows()["gap"][gid], table="gap")
    # Every attribute the control strategy governs, with the acceptance criterion @tbl-cqa
    # states for it. The row names the attribute and the criterion together.
    for r in P.cqa_reg.to_dict("records"):
        add(f"attr:{r['key']}", "attribute_has_acceptance_criterion", f"lit:{r['key']}_acc",
            f"{r['cqa']} acceptance: {r['acc_low']:g}–{r['acc_high']:g} {r['unit']}.",
            "control_strategy", "Control strategy", ptp_rows()["cqa"][r["key"]], table="cqa")
    return AssertionStore(run_id="gt-PTP-001", assertions=A, rationales=[])


def ptp_report_sections():
    from annex_contract.summaries import ReportSection, ReportStatement

    train = P.process_steps_df()
    first, last = int(train["Step"].min()), int(train["Step"].max())
    scope = P.char_scope_df()
    n_par = int(scope["Parameters"].sum())
    n_mv = int(scope["Multivariate"].sum())
    n_uv = int(scope["Univariate"].sum())
    n_cqa = len(P.cqa_reg)
    n_crit = int(P.cqa_reg["criticality"].isin(["H", "VH"]).sum())
    n_vh = int((P.cqa_reg["criticality"] == "VH").sum())
    n_viral = int((P.csv("viral_clearance.csv")["step"] != "Cumulative").sum())
    n_ppq = P.CFG.meta["n_ppq_batches"]

    items = [
        ("PTP-001 defines the scope of the transfer of the A-Mab drug substance process, the "
         "activities it comprises and the deliverables that must be complete before process "
         "performance qualification can start at the receiving site.",
         "purpose", "Purpose and scope",
         "this plan defines the scope of that transfer, the activities it comprises, and the "
         "deliverables that must be complete before process performance qualification can "
         "start at the receiving site"),
        ("PTP-001 is the parent of the A-Mab characterization campaign and states why each of "
         "its documents exists.",
         "purpose", "Purpose and scope",
         "This plan is the parent of that campaign and states why each of its documents exists"),
        (f"The scope of the plan is the drug substance process, Steps {first} to {last}, as it "
         f"will be operated at the receiving site.",
         "purpose", "Purpose and scope",
         f"The scope of this plan is the drug substance process, Steps {first} to {last}, as it "
         f"will be operated at the receiving site"),
        ("Technology transfer is an element of the pharmaceutical quality system and is expected "
         "to deliver the knowledge that lets the receiving site run the process as intended.",
         "purpose", "Purpose and scope",
         "Technology transfer is an element of the pharmaceutical quality system, and it is "
         "expected to deliver the knowledge that allows the receiving site to run the process "
         "as it was intended to run"),
        (f"Viral safety is modular: clearance comes from {n_viral} steps whose mechanisms are "
         f"independent of one another, and no single step carries the whole claim.",
         "process", "Product and process description",
         f"Clearance comes from {n_viral} steps whose mechanisms are independent of one another"),
        ("The site equivalency comparison shows that the receiving site holds equipment of the "
         "same class in the same sequence, under the same quality system.",
         "equivalency", "Site equivalency analysis",
         "The comparison shows that the receiving site holds equipment of the same class in the "
         "same sequence, under the same quality system"),
        ("The comparison does not show that the equipment holds every parameter to the range the "
         "process needs; that is established parameter by parameter in the characterization "
         "reports.",
         "equivalency", "Site equivalency analysis",
         "It does not show that the equipment holds every parameter to the range the process needs"),
        ("A scale-down model may support a range claim only where it has been qualified against "
         "data at scale for the step it represents.",
         "sdm", "Scale-down model and comparability strategy",
         "A scale-down model may support a range claim only where it has been qualified against "
         "data at scale for the step it represents (SOP-1001)"),
        (f"The characterization scope assigns {n_mv} of the {n_par} process parameters to "
         f"multivariate designs and {n_uv} to one-factor-at-a-time assessment, on the basis set "
         f"out in RA-001.",
         "sdm", "Scale-down model and comparability strategy",
         f"Of the {n_par} parameters in the process, {n_mv} are studied in multivariate designs "
         f"and {n_uv} are assessed one factor at a time"),
        ("Viral clearance is not measured on commercial batches: it is claimed from spiking "
         "studies on qualified small-scale models, and the commercial process is never spiked.",
         "methods", "Analytical methods",
         "Clearance is claimed from spiking studies executed on qualified small-scale models, "
         "and the commercial process is never spiked"),
        (f"The drug substance attribute register holds {n_cqa} attributes, of which {n_crit} are "
         f"of high or very high criticality and {n_vh} are of very high criticality.",
         "control_strategy", "Control strategy",
         f"The register holds {n_cqa} attributes, of which {n_crit} are of high or very high "
         f"criticality, and the {n_vh} of very high criticality are high mannose and the two "
         f"viral clearance claims"),
        ("The plan is prospective with respect to the control strategy: it defines no design "
         "space and classifies no parameter, because both are outputs of the characterization "
         "package.",
         "control_strategy", "Control strategy",
         "This plan defines no design space and classifies no parameter, since both are outputs "
         "of the characterization package and neither is created by the act of transfer"),
        ("Until PCMR-001 is approved the classifications carried in the batch record are "
         "provisional, and the receiving site operates to the platform set-points and normal "
         "operating ranges in the interim.",
         "control_strategy", "Control strategy",
         "Until PCMR-001 is approved, the classifications carried in the batch record are "
         "provisional"),
        ("Process performance qualification is Stage 2 of the lifecycle and follows this "
         "transfer.",
         "ppq", "Process performance qualification strategy",
         "Process performance qualification is Stage 2 of the lifecycle and it follows this "
         "transfer"),
        (f"Qualification is {n_ppq} consecutive commercial-scale drug substance batches run at "
         f"the set-points with every parameter inside its normal operating range.",
         "ppq", "Process performance qualification strategy",
         f"The receiving site manufactures {n_ppq} consecutive drug substance batches at "
         f"commercial scale, at the set-points, with every parameter held inside its normal "
         f"operating range"),
        ("Six gaps were identified during transfer planning and none of them is closed at the "
         "date of the plan.",
         "gaps", "Gap analysis",
         "Six gaps were identified during transfer planning, and none of them is closed at the "
         "date of this plan"),
        ("Two of the six gaps are recorded as in progress rather than open, because their "
         "mitigations have already started.",
         "gaps", "Gap analysis",
         "because their mitigations have already started, with reserve reagent lots held at the "
         "sending site (GAP-02) and the performance matching recorded as each scale-down model "
         "is qualified (GAP-04)"),
        ("GAP-02, GAP-04 and GAP-06 must close before qualification and are prerequisites for "
         "it; GAP-03 is carried into Stage 3 and is not closed by qualification at all.",
         "gaps", "Gap analysis",
         "GAP-02, GAP-04 and GAP-06 close before qualification and are prerequisites for it."),
    ]
    statements = [
        ReportStatement(statement_id=f"PTP-001-S{i:02d}", statement_text=text,
                        confidence="high", review_status="accepted",
                        source_references=[_ptp_ref(sec_id, sec, quote)])
        for i, (text, sec_id, sec, quote) in enumerate(items, start=1)
    ]
    return [ReportSection(section_id="PTP-001-summary", title="Transfer plan summary",
                          statements=statements)]


def build_transfer_plan():
    doc, f = "PTP-001", PTP_FILE
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_sites", sites=ptp_sites()),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_process",
                                  process_steps=ptp_steps()),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_sdm",
                                  equipment=ptp_equipment()),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=ptp_methods()),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_control_strategy",
                                  quality_attributes=ptp_cqas()),
    ]
    return S.GroundTruthAnnex(
        weak_claims=build_weak_claims(doc, f),
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Transfer plan spans the whole process train; entities are the two sites, the Step 3-10 process steps, the instrumented scale-down systems, the validated analytical methods and the attributes the control strategy governs.",
            "The distinctive objects are the TransferGap entries (transfer_has_gap assertions); each gap is anchored twice, on the §8 narrative sentence that argues it and on its row of the gap register.",
            "Gap status follows the register the document renders: four gaps are open and two (GAP-02, GAP-04) are in progress because their mitigations have already started. None is closed, which is a weaker claim than all being open.",
            "Strictly prospective: the document reports no characterization outcome, so the annex carries no parameter classification, no capability and no design space. The counts asserted are the prospective ones — the study-type allocation, the attribute register and the qualification batch count.",
        ],
        inventory=ptp_inventory(),
        entities=entities,
        transfer_gaps=ptp_gaps(),
        report_sections=ptp_report_sections(),
        assertions=ptp_assertions(), concepts=ptp_concepts(),
        rhetorical_spans=build_rhetorical_spans(doc, f))


# =========================================================================== #
# RA-001 — Pre-Characterization Process Risk Assessment.                        #
# --------------------------------------------------------------------------- #
# Corpus-spanning, pre-characterization: the ground truth captures the CQA       #
# criticality framework, all 37 process parameters as prospective risk subjects  #
# (parameter_type left 'unclassified' — classification is an OUTPUT of the        #
# studies), and the parameter -> CQA-at-risk relations that drive the            #
# study-type assignment. Reuses the curated CONTENT via ra_content.              #
#                                                                                #
# Three things this document does NOT record, and the annex must not either:      #
# a classification, an operating range or PAR, and a residual risk number. §1     #
# says "The assessment also defines no operating range and no design space" and   #
# §5 says "It fixes a study type but not a range", so no parameter record here    #
# carries a set-point, a NOR or a PAR — those belong to the PCP-00N annexes.      #
# =========================================================================== #
RA_FILE = "RA-001_risk_assessment.docx"
RA_ATTR_NAME = {r["key"]: r["cqa"] for _, r in P.cqa_reg.iterrows()}

# §4 of RA-001 gives every step two rendered tables — a risk ranking (parameter, attributes
# at risk, the three scores, initial RPN, priority band, assigned study type) and a
# prospective failure mode / effect table. Both are per parameter, so both give a row that
# names BOTH ends of the relation a record asserts. Everything in this region anchors on one
# of those rows, on the attribute-register row, or on the specific sentence that states the
# claim; nothing anchors on a caption. Section titles and table ids follow the rendered
# headings and the ``.qmd`` cross-reference labels.
RA_STEP_SEC = {
    "bioreactor": ("Production bioreactor (Step 3)", "Production bioreactor", "bio"),
    "harvest": ("Harvest and clarification (Step 4)", "Harvest and clarification", "harvest"),
    "protein_a": ("Protein A chromatography (Step 5)", "Protein A chromatography", "proteina"),
    "viral_inactivation": ("Low-pH viral inactivation (Step 6)", "Low-pH viral inactivation", "vi"),
    "cex": ("Cation exchange chromatography (Step 7)", "Cation exchange chromatography", "cex"),
    "aex": ("Anion exchange chromatography (Step 8)", "Anion exchange chromatography", "aex"),
    "virus_filtration": ("Small-virus retentive filtration (Step 9)",
                         "Small-virus retentive filtration", "vf"),
    "ufdf": ("Ultrafiltration and diafiltration (Step 10)",
             "Ultrafiltration and diafiltration", "ufdf"),
}

# The sentence in which the document itself states that a performance-only parameter reaches
# no quality attribute. Keyed by (step, parameter); a step-wide entry keyed by the step alone
# covers the parameters the step states collectively. These are the second reference on the
# non-impact assertions — the ranking row carries "process performance" and the Low band, the
# sentence carries the reason.
RA_PERF_PROSE = {
    "harvest": "Harvest forms no quality attribute and is credited with no clearance",
    "ufdf": "the step forms no quality attribute and is credited with no clearance",
    "bioreactor": "no product quality effect is expected for them over the ranges the "
                  "process uses",
    ("bioreactor", "medium_conc"):
        "that effect is too small to move the attribute within its acceptance range, so the "
        "parameter is carried on process performance and studied on its own",
    ("protein_a", "flow"):
        "Load flow rate and end of pool collect carry no attribute risk.",
    ("protein_a", "end_collect"):
        "Load flow rate and end of pool collect carry no attribute risk.",
    "protein_a": "No significant product quality impact is expected from either of them, even "
                 "for an excursion beyond the range proposed for characterization",
    "viral_inactivation": "No effect on inactivation kinetics, aggregation or charge variants "
                          "is expected over the concentration range the step sees",
    "cex": "Elution flow rate affects peak shape and yield and is studied on its own.",
}

# The attribute a non-impact assertion is stated AGAINST, where the document names one.
RA_PERF_OBJECT = {("bioreactor", "medium_conc"): "attr:afucosylation"}


def ra_step_rows():
    """``{step key -> (ranking rows, failure-mode rows)}`` plus the set of ambiguous rank rows.

    Rebuilt from the same DataFrames the document renders, so a quote stays verbatim when the
    seed changes. Reuse budget per ranking row: the parameter entity, ``step_has_parameter``
    and one ``parameter_impacts_attribute`` per attribute at risk. Culture pH and culture
    duration reach five attributes each, which is the corpus maximum at seven references on
    one span — still inside ``check_grounding.MAX_QUOTE_REUSE``.

    The second return value is the set of ranking rows that render identically at two steps.
    Protein A and anion exchange both rank a "Protein load" against host cell protein with the
    same three scores, so their rows are the same string and neither can say which step is
    meant. ``ra_rank_refs`` adds the failure-mode row in that case; failure-mode rows quote
    the step's own limit and are all unique.
    """
    from collections import Counter
    import ra_content as RC
    out = {}
    for key in P.CFG.train_order:
        score, mode = RC.ra_score_table(key), RC.ra_mode_table(key)
        out[key] = (row_quotes(score, score["Parameter"], P._auto_floatfmt(score)),
                    row_quotes(mode, mode["Parameter"], P._auto_floatfmt(mode)))
    seen = Counter(q for rank, _ in out.values() for q in rank.values())
    return out, {q for q, n in seen.items() if n > 1}


def ra_rank_ref(r, rows):
    """The parameter's row of its step's risk-ranking table.

    Carries the parameter, the attribute(s) it puts at risk, severity/occurrence/detection,
    the initial RPN, the priority band and the assigned study type — every field the
    parameter records in this document."""
    sec, title, tid = RA_STEP_SEC[r["key"]]
    return ref("RA-001", RA_FILE, f"RA-001_sec_rank_{r['key']}", sec,
               rows[r["key"]][0][r["param"]],
               table_title=f"{title} parameter risk ranking.",
               table_id=f"RA-001_tbl-risk-{tid}")


def ra_rank_refs(r, rows, ambiguous):
    """The ranking row, plus the failure-mode row when the ranking row is not unique."""
    out = [ra_rank_ref(r, rows)]
    if rows[r["key"]][0][r["param"]] in ambiguous:
        out.append(ra_mode_ref(r, rows))
    return out


def ra_mode_ref(r, rows):
    """The parameter's row of its step's prospective failure-mode table."""
    sec, title, tid = RA_STEP_SEC[r["key"]]
    return ref("RA-001", RA_FILE, f"RA-001_sec_rank_{r['key']}", sec,
               rows[r["key"]][1][r["param"]],
               table_title=f"{title} prospective failure modes and effects.",
               table_id=f"RA-001_tbl-fm-{tid}")


def ra_cqa_row_ref(key, rows):
    """The attribute's row of the §3 register: acceptance, criticality, Tool #1, severity, step."""
    return ref("RA-001", RA_FILE, "RA-001_sec_cqa", "Quality attributes at risk", rows[key],
               table_title="Drug substance quality attributes, their acceptance criteria, "
                           "criticality and severity.",
               table_id="RA-001_tbl-cqa")


def ra_cqa_entities():
    # One strong anchor beats two weak ones: the rendered register row names the attribute,
    # its acceptance criterion, its criticality, the Tool #1 score, the severity it confers
    # and the step that sets it — every field this record carries.
    import ra_content as RC
    rows = row_quotes(RC.cqa_table(), P.cqa_reg["key"])
    out = []
    for r in P.cqa_reg.to_dict("records"):
        # ------------------------------------------------------------------------------ #
        # tool2_severity is the severity THIS DOCUMENT renders, which is the A-Mab         #
        # severity map in ra_content.CQA_SEVERITY, not cqa_register.csv's tool2_severity.  #
        # ------------------------------------------------------------------------------ #
        # The two disagree for every attribute (high mannose 10 vs 7, leached Protein A 4
        # vs 5, XMuLV/MVM 10 vs 9), and RA-001 renders and argues the first: §2.1 says a
        # parameter that could move high mannose "sits at the top of the scale", and the
        # register row this record is anchored on shows Severity 10. Reading tool2_severity
        # off the CSV made the annex assert a number its own anchor contradicts.
        sev = int(RC.CQA_SEVERITY.get(r["key"], 4))
        out.append(S.QualityAttribute(
            attribute_id=f"attr:{r['key']}", attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"], acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            rationale_for_criticality=f"A-Mab Tool #1 (impact × uncertainty) = "
                                      f"{int(r['tool1_score'])}; severity conferred on a "
                                      f"parameter that can affect it = {sev}.",
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=sev,
            source_references=[ra_cqa_row_ref(r["key"], rows)],
            metadata=meta()))
    return out


def ra_param_entities(rows, step_rows):
    out = []
    for r in rows:
        p = P.CFG.unit_op(r["key"]).param(r["pkey"])
        rationale = (f"Prospective (pre-characterization) risk: could affect {r['cqa_label']} "
                     f"(severity {r['severity']}), initial RPN {r['rpn_init']}, {r['priority']} "
                     f"priority band; assigned to {r['study']}. Classification is an output of "
                     f"the study."
                     if r["quality"] else
                     f"Ranked against process performance and not against a quality attribute "
                     f"(initial RPN {r['rpn_init']}, {r['priority']} priority band); assigned to "
                     f"{r['study']}.")
        out.append(S.ProcessParameter(
            parameter_id=f"param:{r['key']}_{r['pkey']}", parameter_name=r["param"],
            # ---------------------------------------------------------------------------- #
            # NO target_value, NOR or PAR. RA-001 renders none of the three, and §1 states   #
            # "The assessment also defines no operating range and no design space" while §5  #
            # states "It fixes a study type but not a range". Carrying a set-point and two   #
            # ranges here made the gold assert something the document explicitly disclaims,  #
            # with no span in the document able to attest it. The ranges belong to the       #
            # PCP-00N annexes, whose documents render them.                                  #
            # ---------------------------------------------------------------------------- #
            parameter_type="unclassified", unit=p.unit,
            associated_step=f"{r['unit_op']} (Step {r['step']})",
            rationale_for_criticality=rationale,
            source_references=[
                # the risk-ranking row: parameter, attribute(s) at risk, the three scores,
                # initial RPN, priority band, assigned study type
                ra_rank_ref(r, step_rows),
                # the failure-mode row: parameter, postulated failure mode, its effect
                ra_mode_ref(r, step_rows),
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


def ra_assertions(rows, step_rows, ambiguous):
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    import ra_content as RC
    A = []
    n = [0]
    cqa_rows = row_quotes(RC.cqa_table(), P.cqa_reg["key"])

    def add(subj, pred, obj, text, refs):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"RA-001-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text, source_references=refs, metadata=meta()))

    def perf_prose_ref(r):
        """The sentence in which the document states this parameter reaches no attribute."""
        quote = RA_PERF_PROSE.get((r["key"], r["pkey"])) or RA_PERF_PROSE.get(r["key"])
        if not quote:
            return None
        sec = RA_STEP_SEC[r["key"]][0]
        return ref("RA-001", RA_FILE, f"RA-001_sec_rank_{r['key']}", sec, quote)

    # step -> parameter: every parameter assessed here belongs to a named unit operation and
    # leaves this document with a study type (the assessment's actual output). The ranking row
    # carries the parameter and the study type assigned to it, under the step's own section.
    for r in rows:
        add(f"step:{r['key']}", "step_has_parameter", f"param:{r['key']}_{r['pkey']}",
            f"{r['unit_op']} has process parameter {r['param']}, which this assessment assigns to "
            f"{r['study']}.", ra_rank_refs(r, step_rows, ambiguous))
    # attribute -> acceptance criterion, and attribute -> the step that sets it. Both are read
    # off the same register row, which carries the acceptance range and the "Set by" column.
    for r in P.cqa_reg.to_dict("records"):
        add(f"attr:{r['key']}", "attribute_has_acceptance_criterion", f"lit:{r['key']}_acc",
            f"{r['cqa']} acceptance: {r['acc_low']:g}–{r['acc_high']:g} {r['unit']}.",
            [ra_cqa_row_ref(r["key"], cqa_rows)])
        add(f"step:{r['set_by']}", "step_has_quality_attribute", f"attr:{r['key']}",
            f"The register records {r['cqa']} as set by "
            f"{P.UNIT_OP_TITLES.get(r['set_by'], r['set_by'])}.",
            [ra_cqa_row_ref(r["key"], cqa_rows)])
    # parameter -> attribute AT RISK. Prospective only: the failure mode is postulated and the
    # attribute is the one it could reach, not one the parameter is shown to move.
    for r in rows:
        if not r["quality"]:
            continue
        pid = f"param:{r['key']}_{r['pkey']}"
        for cqa_key in r["cqas"]:
            add(pid, "parameter_impacts_attribute", f"attr:{cqa_key}",
                f"{r['param']} carries a prospective (pre-characterization) risk to "
                f"{RA_ATTR_NAME.get(cqa_key, cqa_key)}: the postulated failure mode could reach "
                f"the attribute, and the size of the effect is not yet measured.",
                ra_rank_refs(r, step_rows, ambiguous))
    # Performance-only parameters. All 16 of them, not just the two steps that carry nothing
    # else: the document ranks every one at "process performance" in its step table and states
    # the reason in prose, so the ground truth covers the whole register of 37 parameters.
    for r in rows:
        if r["quality"]:
            continue
        pid = f"param:{r['key']}_{r['pkey']}"
        refs = ra_rank_refs(r, step_rows, ambiguous)
        prose = perf_prose_ref(r)
        if prose:
            refs.append(prose)
        # "Reaches no attribute at all" would be too strong for basal medium concentration:
        # §4.1 records a statistically significant but shallow prior-knowledge effect on
        # afucosylation and rules it "too small to move the attribute within its acceptance
        # range". That is exactly a NOT-SIGNIFICANT impact on a named attribute, so the object
        # is the attribute the document names, and the wording below tracks the rendered
        # "CQA(s) at risk" cell rather than overstating it.
        obj = RA_PERF_OBJECT.get((r["key"], r["pkey"]), "attr:aggregates_hmw")
        add(pid, "parameter_does_not_significantly_impact_attribute", obj,
            f"{r['param']} is ranked against process performance and not against a quality "
            f"attribute (initial RPN {r['rpn_init']}, {r['priority']} priority band); it is "
            f"assigned to {r['study']}.", refs)
    return AssertionStore(run_id="gt-RA-001", assertions=A, rationales=[])


def ra_report_sections():
    from annex_contract.summaries import ReportSection, ReportStatement

    import ra_content as RC
    ra, rc = RC.ra_summary(), RC.ra_counts()
    ov = RC.ra_step_overview_df()
    rule = RC.ra_initial_score_rule_df()
    rule_rows = row_quotes(rule, rule["Parameter class"], P._auto_floatfmt(rule))
    # Every number below is read from the same helpers the document renders it with; none is
    # typed. n_* mirror the doc-local scalars in the RA-001 SETUP chunk.
    n_steps = len(P.CFG.train_order)
    n_plain_uni = ra["n_univariate"] - ra["n_just_uni"]
    n_bioreactor_cqas = int((P.cqa_reg.set_by == "bioreactor").sum())
    n_other_cqas = int(len(P.cqa_reg) - n_bioreactor_cqas)
    n_steps_at_rpn_max = int((ov["Highest init. RPN"] == rc["rpn_max"]).sum())
    n_attr_max = max(len(r["cqas"]) for r in RC.ra_rows() if r["quality"])
    sev_band = P.CFG.risk["thresholds"]["cpp_severity"]
    n_viral_class = int(rule.loc[0, "Parameters"])
    n_other_quality_class = int(rule.loc[1, "Parameters"])
    n_perf_class = int(rule.loc[2, "Parameters"])

    def st(i, text, sec, *quotes):
        return ReportStatement(statement_id=f"RA-001-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[
                                   ref("RA-001", RA_FILE, "RA-001_sec", sec, q) for q in quotes])
    return [ReportSection(section_id="RA-001-summary", title="Risk assessment summary", statements=[
        st(1, "RA-001 decides which A-Mab process parameters are characterized and what kind of "
              "study each one receives; its output is a scope, not a result.",
           "Purpose and scope",
           "This assessment decides which process parameters of the A-Mab drug substance process "
           "are characterized, and what kind of study each one receives."),
        st(2, "The assessment is executed before any characterization study, so it draws on prior "
              "knowledge, the platform history and the process description alone.",
           "Purpose and scope",
           "It is performed before any characterization study is executed, so it draws on prior "
           "knowledge, the platform history and the process description alone."),
        st(3, "The assessment classifies no parameter: the critical, well controlled critical, key "
              "and general designations are an outcome of the studies and are recorded in PCR-003 "
              "through PCR-010.",
           "Purpose and scope",
           "Classification into critical, well controlled critical, key and general process "
           "parameters is an outcome of the studies, and it is recorded in the characterization "
           "reports PCR-003 through PCR-010."),
        st(4, "The assessment defines no operating range and no design space.",
           "Purpose and scope",
           "The assessment also defines no operating range and no design space, and it states only "
           "what must be studied and why."),
        st(5, f"The scope is the drug substance train of PTP-001: {n_steps} unit operations, "
              f"{ra['n']} process parameters and {rc['n_cqa']} drug substance quality attributes.",
           "Purpose and scope",
           f"That train has {n_steps} unit operations and {ra['n']} process parameters, and it "
           f"must control {rc['n_cqa']} drug substance quality attributes"),
        st(6, "Severity is a property of the attribute and not of the parameter, so a parameter is "
              "scored at the severity of the most severe attribute it could affect.",
           "Severity",
           "Severity is a property of the quality attribute and not of the parameter, so a "
           "parameter is scored at the severity of the most severe attribute it could affect"),
        st(7, f"The priority band follows severity alone: High at severity {sev_band} or above, "
              f"Medium for a less severe attribute, Low for a parameter that reaches no attribute.",
           "Severity",
           f"A parameter linked to an attribute of severity {sev_band} or above takes the High "
           f"band, a parameter linked to a less severe attribute takes the Medium band, and a "
           f"parameter that reaches no attribute takes the Low band."),
        st(8, "Occurrence and detection are scored by convention, because neither can be measured "
              "before the studies are run.",
           "Occurrence and detection before characterization",
           "Occurrence and detection are scored by convention in this assessment, because neither "
           "can be measured before the studies are run."),
        st(9, "A parameter that could reduce viral clearance takes the worst detection score, "
              "because clearance is not measured on a routine batch.",
           "Occurrence and detection before characterization",
           "A parameter that could reduce viral clearance receives the worst detection score, "
           "because clearance is not measured on a routine batch and its loss would not appear in "
           "release testing."),
        st(10, f"The {ra['n']} parameters fall into three mutually exclusive scoring classes: "
               f"{n_viral_class} impact a viral-safety attribute, {n_other_quality_class} impact "
               f"another quality attribute and {n_perf_class} affect process performance only.",
            "Occurrence and detection before characterization",
            rule_rows["Impacts a viral-safety attribute"],
            rule_rows["Impacts another quality attribute"],
            rule_rows["Process performance only"]),
        st(11, "The study type is decided by attribute risk and expected interaction, and the "
               "initial RPN is not one of the two inputs to that decision.",
            "The study type decision",
            "Two things decide the study type, and the initial RPN is not one of them"),
        st(12, "No residual risk number is produced, because a residual assessment needs the "
               "characterization results and the control strategy that follows from them; it is "
               "consolidated in PCMR-001.",
            "What this assessment does not produce",
            "It also produces no residual risk number, and a residual assessment needs the "
            "characterization results and the control strategy that follows from them, so it is "
            "performed after the studies report and is consolidated in PCMR-001."),
        st(13, f"The attribute register carries {rc['n_cqa']} attributes, of which "
               f"{rc['n_critical']} carry a high or very high criticality designation.",
            "Quality attributes at risk",
            f"The register carries {rc['n_cqa']} attributes, of which {rc['n_critical']} carry a "
            f"high or very high criticality designation."),
        st(14, "The two viral clearance attributes are cumulative across the process, so their "
               "acceptance criteria are a floor and not a window.",
            "Quality attributes at risk",
            "The two viral clearance attributes are expressed as a cumulative log reduction across "
            "the whole process, so their acceptance criteria are a floor and not a window."),
        st(15, f"The production bioreactor sets {n_bioreactor_cqas} of the {rc['n_cqa']} "
               f"attributes; the remaining {n_other_cqas} are set at the capture step, the low pH "
               f"hold and the anion exchange step.",
            "Quality attributes at risk",
            f"The production bioreactor sets {n_bioreactor_cqas} of the {rc['n_cqa']} attributes, "
            f"and the remaining {n_other_cqas} are set at the capture step, the low pH hold and "
            f"the anion exchange step"),
        st(16, f"The highest initial RPN is reached at {n_steps_at_rpn_max} steps, all of them "
               f"viral steps, and is shared by {rc['n_at_rpn_max']} parameters.",
            "Parameter risk ranking by unit operation",
            f"The highest initial RPN in the assessment is reached at {n_steps_at_rpn_max} steps, "
            f"and all of them are viral steps.",
            f"That number is shared by {rc['n_at_rpn_max']} parameters"),
        st(17, f"{rc['n_steps_no_cqa']} steps, harvest and UF/DF, carry no parameter linked to a "
               f"quality attribute and are assessed on process performance alone.",
            "Parameter risk ranking by unit operation",
            f"{rc['n_steps_no_cqa']} steps, harvest and UF/DF, carry no parameter linked to a "
            f"quality attribute at all, and both are assessed on process performance alone."),
        st(18, f"Every parameter is assigned a study: {ra['n_multivariate']} to a multivariate "
               f"designed experiment, {ra['n_just_uni']} to a justified univariate study and "
               f"{n_plain_uni} to univariate assessment on process performance.",
            "Characterization study assignment",
            f"The assessment assigns a study to every parameter it carries: "
            f"{ra['n_multivariate']} parameters go into a multivariate designed experiment, "
            f"{ra['n_just_uni']} is assigned a justified univariate study, and {n_plain_uni} are "
            f"assessed univariately on process performance."),
        st(19, "No parameter was filtered out as too low a risk to study.",
            "Characterization study assignment",
            "No parameter was filtered out as too low a risk to study."),
        st(20, f"A designed experiment is carried at {ra['n_doe_steps']} of the {n_steps} steps; "
               f"harvest and UF/DF carry none because no parameter at either is linked to a "
               f"quality attribute.",
            "Characterization study assignment",
            f"A designed experiment is carried at {ra['n_doe_steps']} of the {n_steps} steps.",
            "Harvest and UF/DF do not, because no parameter at either is linked to a quality "
            "attribute, and a multivariate design would resolve interactions with no quality "
            "consequence."),
        st(21, "The anion exchange operating flow rate is the one parameter that reaches the "
               "highest initial RPN and is still assigned a univariate study; it returns to the "
               "multivariate scope if the univariate result does not support the expectation.",
            "Anion exchange chromatography (Step 8)",
            "Operating flow rate is the one parameter in the assessment that reaches the highest "
            "initial RPN and is still not assigned to a designed experiment.",
            "If the univariate result does not support the expectation, the parameter returns to "
            "the multivariate scope."),
        st(22, "The assignment is prospective, is bounded in three ways, and is revisited when the "
               "studies report.",
            "Characterization study assignment",
            "This assignment is prospective, and it is bounded in three ways.",
            "The assignment is also revisited when the studies report."),
        st(23, "Leached Protein A has no operating parameter ranked against it, because the amount "
               "that leaches is governed by the resin and by its sanitization history; the capture "
               "study measures it as a step response instead.",
            "Assumptions and limitations",
            "no operating parameter in the list is linked to it, because the amount that leaches "
            "is governed by the resin and by its sanitization history under SOP-2008",
            "the capture study measures it as a step response instead (PCP-005)"),
        st(24, "The initial risk priority number ranks parameters against each other and does not "
               "measure risk on an absolute scale.",
            "Assumptions and limitations",
            "the risk priority number ranks parameters against each other and does not measure "
            "risk on an absolute scale"),
        st(25, f"Severity rewards no parameter for reaching several attributes at once: culture pH "
               f"and culture duration reach {n_attr_max} attributes each and still score below the "
               f"viral parameters.",
            "Assumptions and limitations",
            "Severity is taken from the most severe attribute a parameter can affect, and nothing "
            "in the score rewards a parameter for affecting several attributes at once.",
            f"Each of them is linked to {n_attr_max} attributes, and both still score below the "
            f"viral parameters, which are linked to one or two."),
        st(26, "Every quantitative statement about the effect of a parameter on an attribute "
               "belongs to the characterization reports and not to this document.",
            "Assumptions and limitations",
            "Every quantitative statement about the effect of a parameter on an attribute belongs "
            "to the characterization reports, and nothing in this document should be read as one."),
        st(27, "Each plan from PCP-003 to PCP-010 takes the share of the assignment belonging to "
               "its own step and sets the ranges and acceptance criteria for it.",
            "Outputs and downstream use",
            "Each plan from PCP-003 to PCP-010 takes the share belonging to its own step, sets the "
            "ranges and states the acceptance criteria"),
    ])]


# --------------------------------------------------------------------------- #
# Discourse layer (RA-001).                                                     #
# --------------------------------------------------------------------------- #
# RA-001 is not a report, but it argues: it decides a scope, and every decision  #
# in it is a claim with a stated warrant. The three arguments worth labelling    #
# are (a) what the assessment does and refuses to do, (b) why criticality and    #
# parameter risk are different scales, and (c) the one parameter that reaches    #
# the top of the RPN scale and is still kept out of a designed experiment, which #
# is carried on a mechanism and bounded by a return condition. Each quote is a   #
# verbatim, number-free fragment of the RENDERED document. Tuple fields:         #
# (suffix, role, section, quote, supported_by-suffixes, restates-suffix,         #
#  bounds-suffix).                                                               #
# --------------------------------------------------------------------------- #
RA_RHET_SPANS = [
    ("R00", "claim", "Purpose and scope",
     "This assessment decides which process parameters of the A-Mab drug substance process are "
     "characterized, and what kind of study each one receives.", ["R01"], None, None),
    ("R01", "justification", "Purpose and scope",
     "For every parameter carried in the process description it records the quality attribute "
     "that the parameter could put at risk, an initial risk priority number, and the study type "
     "assigned to it.", [], None, None),
    ("R02", "bounded_conclusion", "Purpose and scope",
     "The assessment also defines no operating range and no design space, and it states only what "
     "must be studied and why.", [], None, "R00"),
    ("R03", "claim", "Risk assessment methodology",
     "The product of the three is the risk priority number (RPN), and parameters are ranked on it.",
     ["R04"], None, None),
    ("R04", "justification", "Risk assessment methodology",
     "Severity comes from the quality attribute that the parameter could affect, occurrence "
     "describes how likely an effect on that attribute is thought to be, and detection describes "
     "whether the controls that exist today would find the failure, and how late.", [], None, None),
    ("R05", "mechanistic_warrant", "Severity",
     "Severity is a property of the quality attribute and not of the parameter, so a parameter is "
     "scored at the severity of the most severe attribute it could affect", [], None, None),
    ("R06", "claim", "Severity",
     "The priority band in the step tables of §4 follows the severity alone.", ["R05"], None, None),
    ("R07", "problem_statement", "Occurrence and detection before characterization",
     "Occurrence and detection are scored by convention in this assessment, because neither can be "
     "measured before the studies are run.", [], None, None),
    ("R08", "justification", "Occurrence and detection before characterization",
     "A parameter that could reduce viral clearance receives the worst detection score, because "
     "clearance is not measured on a routine batch and its loss would not appear in release "
     "testing.", [], None, None),
    ("R09", "claim", "Criticality and parameter risk are separate",
     "An attribute of very high criticality does not make every parameter that touches it a high "
     "risk parameter, and a parameter can score high because the process cannot yet detect the "
     "failure, even where the attribute itself is moderate.", ["R10"], None, None),
    ("R10", "justification", "Criticality and parameter risk are separate",
     "Attribute criticality is a property of the molecule and of what the attribute does in the "
     "patient, whereas the risk of a process parameter is scored on severity, occurrence and "
     "detection and is a property of the process and of how well that process is currently "
     "understood.", [], None, None),
    ("R11", "claim", "The study type decision",
     "Two things decide the study type, and the initial RPN is not one of them", ["R12"], None, None),
    ("R12", "justification", "The study type decision",
     "The first is whether an excursion in the parameter could reach a quality attribute. The "
     "second is whether the effect of the parameter is expected to depend on the other parameters "
     "at the same step.", [], None, None),
    ("R13", "deferral", "What this assessment does not produce",
     "It also produces no residual risk number, and a residual assessment needs the "
     "characterization results and the control strategy that follows from them, so it is performed "
     "after the studies report and is consolidated in PCMR-001.", [], None, None),
    ("R14", "claim", "Quality attributes at risk",
     "A batch that fails either of them cannot be brought back by reprocessing, and that is what "
     "puts both at the top of the scale.", ["R15"], None, None),
    ("R15", "mechanistic_warrant", "Quality attributes at risk",
     "The two viral clearance attributes are expressed as a cumulative log reduction across the "
     "whole process, so their acceptance criteria are a floor and not a window.", [], None, None),
    ("R16", "cross_step_credit", "Quality attributes at risk",
     "The enveloped virus claim takes independent contributions from the low pH hold, the anion "
     "exchange step and the virus filter.", [], None, None),
    ("R17", "mechanistic_warrant", "Quality attributes at risk",
     "The parvovirus claim rests on the anion exchange step and the virus filter alone, because a "
     "low pH hold does not inactivate a virus without an envelope.", [], None, None),
    ("R18", "claim", "Production bioreactor (Step 3)",
     "Culture pH reaches the highest initial RPN at the step because it is the only bioreactor "
     "parameter that could move high mannose, which is the one attribute the step forms that sits "
     "at the top of the severity scale.", [], None, None),
    ("R19", "mechanistic_warrant", "Production bioreactor (Step 3)",
     "Culture duration acts indirectly, because an extended culture is harvested at lower "
     "viability, which raises host cell protein and DNA in the harvest and can raise aggregate as "
     "well.", [], None, None),
    ("R20", "hedge", "Production bioreactor (Step 3)",
     "Basal medium concentration is a partial exception, because prior product knowledge records a "
     "statistically significant but shallow effect of medium concentration on afucosylation, and "
     "that effect is too small to move the attribute within its acceptance range", [], None, None),
    ("R21", "justification", "Protein A chromatography (Step 5)",
     "Both are taken into the designed experiment even so, because step yield is measured on the "
     "same runs and these are the two parameters that move it.", [], None, None),
    ("R22", "claim", "Low-pH viral inactivation (Step 6)",
     "Inactivation pH is the sharpest case in the assessment, because it carries a failure mode in "
     "both directions.", ["R23"], None, None),
    ("R23", "justification", "Low-pH viral inactivation (Step 6)",
     "The two failure modes act on different attributes and bound the acceptable range from both "
     "sides, which is why the parameter is taken into a designed experiment together with hold "
     "time and temperature.", [], None, None),
    ("R24", "problem_statement", "Anion exchange chromatography (Step 8)",
     "Operating flow rate is the one parameter in the assessment that reaches the highest initial "
     "RPN and is still not assigned to a designed experiment.", [], None, None),
    ("R25", "mechanistic_warrant", "Anion exchange chromatography (Step 8)",
     "Flow rate is expected to act through residence time, and not through the ionic conditions "
     "that govern how impurities and virus bind to the resin, so its effect should not interact "
     "with load pH or with conductivity.", [], None, None),
    ("R26", "claim", "Anion exchange chromatography (Step 8)",
     "The parameter is assigned a justified univariate study, and PCP-008 records that "
     "justification together with the range it studies.", ["R25"], None, None),
    ("R27", "bounded_conclusion", "Anion exchange chromatography (Step 8)",
     "If the univariate result does not support the expectation, the parameter returns to the "
     "multivariate scope.", [], None, "R26"),
    ("R28", "claim", "Characterization study assignment",
     "The assessment assigns a study to every parameter it carries", ["R29"], None, None),
    ("R29", "justification", "Characterization study assignment",
     "The parameter list contains only settings and in-process limits that the operator controls, "
     "and each of those is given at least the univariate work needed to justify its range.",
     [], None, None),
    ("R30", "restatement", "Characterization study assignment",
     "No parameter was filtered out as too low a risk to study.", [], "R28", None),
    ("R31", "justification", "Characterization study assignment",
     "Harvest and UF/DF do not, because no parameter at either is linked to a quality attribute, "
     "and a multivariate design would resolve interactions with no quality consequence.",
     [], None, None),
    ("R32", "mechanistic_warrant", "Characterization study assignment",
     "Each of them changes the chemical environment in which the product and the impurities bind, "
     "so their effects cannot be estimated one by one and then added together.", [], None, None),
    ("R33", "bounded_conclusion", "Characterization study assignment",
     "This assignment is prospective, and it is bounded in three ways.", [], None, "R28"),
    ("R34", "bounded_conclusion", "Characterization study assignment",
     "It fixes a study type but not a range.", [], None, "R28"),
    ("R35", "claim", "Assumptions and limitations",
     "The assessment assumes that the platform transfers, since A-Mab is made on the humanized "
     "IgG1 platform used for the three earlier products (X-Mab, Y-Mab and Z-Mab)", [], None, None),
    ("R36", "hedge", "Assumptions and limitations",
     "Where the mechanism at a step is the platform mechanism, that assumption is strong. Where "
     "A-Mab differs from the earlier products, it is weaker, and the characterization studies are "
     "the check on it.", [], None, None),
    ("R37", "claim", "Assumptions and limitations",
     "The parameter list is assumed to be complete.", [], None, None),
    ("R38", "justification", "Assumptions and limitations",
     "The register assigns that attribute to the capture step, and no operating parameter in the "
     "list is linked to it, because the amount that leaches is governed by the resin and by its "
     "sanitization history under SOP-2008.", [], None, None),
    ("R39", "claim", "Assumptions and limitations",
     "An assessment of operating parameters cannot cover an attribute of that kind", ["R38"],
     None, None),
    ("R40", "deferral", "Assumptions and limitations",
     "the capture study measures it as a step response instead (PCP-005)", [], None, None),
    ("R41", "bounded_conclusion", "Assumptions and limitations",
     "Occurrence and detection are conventions here and not measurements, and they are applied "
     "uniformly to whole classes of parameter, so the risk priority number ranks parameters "
     "against each other and does not measure risk on an absolute scale.", [], None, "R03"),
    ("R42", "hedge", "Assumptions and limitations",
     "Comparison of the number against an external threshold is not.", [], None, None),
    ("R43", "problem_statement", "Assumptions and limitations",
     "Severity is taken from the most severe attribute a parameter can affect, and nothing in the "
     "score rewards a parameter for affecting several attributes at once.", [], None, None),
    ("R44", "bounded_conclusion", "Assumptions and limitations",
     "The study assignment does not depend on it, because both parameters enter a designed "
     "experiment on either reading.", [], None, "R43"),
    ("R45", "hedge", "Assumptions and limitations",
     "The assessment cannot know effect sizes or interactions. It can only say where they are "
     "plausible.", [], None, None),
    ("R46", "deferral", "Assumptions and limitations",
     "Every quantitative statement about the effect of a parameter on an attribute belongs to the "
     "characterization reports, and nothing in this document should be read as one.",
     [], None, None),
    ("R47", "restatement", "Outputs and downstream use",
     "This assessment produces one output: the study type assigned to each process parameter, with "
     "the attribute risk that justifies it.", [], "R00", None),
    ("R48", "deferral", "Outputs and downstream use",
     "Each plan from PCP-003 to PCP-010 takes the share belonging to its own step, sets the ranges "
     "and states the acceptance criteria, and each report from PCR-003 to PCR-010 records the "
     "outcome and classifies the parameters of that step.", [], None, None),
]


def ra_rhetorical_spans(doc_id, file_name):
    """Argument-structure spans over RA-001."""
    out = []
    for suffix, role, sec, quote, sup, res, bnd in RA_RHET_SPANS:
        out.append(S.RhetoricalSpan(
            span_id=f"{doc_id}-{suffix}", section=sec, role=role,
            source_reference=ref(doc_id, file_name, f"{doc_id}_sec_rhet", sec,
                                 " ".join(quote.split())),
            supported_by=[f"{doc_id}-{s}" for s in sup],
            restates=(f"{doc_id}-{res}" if res else None),
            bounds=(f"{doc_id}-{bnd}" if bnd else None)))
    return out


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
    # Every parameter the document ranks, not a quality-impacting subset: §4 gives all 37 a
    # ranking row and a failure-mode row, and §2.2 states that the three scoring classes are
    # mutually exclusive and sum to the whole register.
    rows = RC.ra_rows()
    step_rows, ambiguous = ra_step_rows()
    doc = "RA-001"
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=ra_cqa_entities()),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_rank",
                                  parameters=ra_param_entities(rows, step_rows)),
    ]
    return S.GroundTruthAnnex(
        weak_claims=build_weak_claims(doc, RA_FILE),
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Pre-characterization: parameter_type is left 'unclassified' (CPP/WC-CPP/KPP/GPP is an OUTPUT of the studies, not this assessment).",
            "No set-point, NOR or PAR is recorded for any parameter. RA-001 renders none of them and states that it 'defines no operating range and no design space' and that it 'fixes a study type but not a range'; the ranges belong to the PCP-00N annexes.",
            "The study-type assignment (multivariate DoE / justified univariate / univariate) and the prospective severity/initial-RPN ranking are reported via report_sections and parameter rationales.",
            "parameter_impacts_attribute here is a PROSPECTIVE (at-risk) relation, not a demonstrated effect; each is anchored on the per-step risk-ranking row that names the parameter, the attribute(s) it could reach and the severity that attribute confers.",
            "QualityAttribute.tool2_severity carries the severity RA-001 renders in its attribute register (the A-Mab severity map), which is not the tool2_severity column of cqa_register.csv; the two differ for every attribute and the document is the authority for its own annex.",
            "No residual RPN and no design space are recorded, because the document states neither: the control strategy that would reduce the risk does not yet exist.",
        ],
        inventory=ra_inventory(),
        entities=entities,
        report_sections=ra_report_sections(),
        assertions=ra_assertions(rows, step_rows, ambiguous),
        concepts=ra_concepts(rows),
        rhetorical_spans=ra_rhetorical_spans(doc, RA_FILE))


# =========================================================================== #
# PCMP-001 — Process Characterization Master Plan.                              #
# --------------------------------------------------------------------------- #
# Umbrella plan over the per-unit-operation plans. The ground truth captures the #
# characterization scope per step (Steps 3-10), the CQA framework, the validated #
# analytical methods and the master-plan narrative. Prospective throughout: no   #
# result, no range, no classification and no capability figure is asserted.      #
# =========================================================================== #
PCMP_FILE = "PCMP-001_master_plan.docx"


def train_row_quotes():
    """Rendered rows of the process-train table, keyed by step.

    PTP-001 and PCMR-001 both render ``process_steps_df()``, so one set of rows serves both.
    The row carries the step number, the unit operation and its principal role; the bare
    unit-operation title carries none of that and recurs throughout each document as a
    heading.

    PCMP-001 no longer uses this. The re-authored master plan renders the characterization
    scope table instead of the process train, so its per-step records anchor on
    ``_pcmp_scope_rows`` below.
    """
    return row_quotes(P.process_steps_df(), P.CFG.train_order)


# --------------------------------------------------------------------------- #
# PCMP-001 renders NO process-train table. It is a campaign plan, not a process  #
# description: its per-step table is the CHARACTERIZATION SCOPE table            #
# (@tbl-scope), whose row carries the step number, the unit operation, the       #
# parameter count, the study-type split RA-001 assigned and the covering         #
# plan/report pair. That row is the anchor for every per-step record here.       #
# ``train_row_quotes`` above still serves PTP-001 and PCMR-001, which do render   #
# the train — nothing in this document quotes it, and the process-train rows the  #
# previous annex used were dead against the re-authored text.                    #
# --------------------------------------------------------------------------- #
PCMP_TAB = {
    "scope": ("PCMP-001_tab_scope",
              "Characterization scope by unit operation. Parameters carried into the "
              "campaign, the study-type split assigned by RA-001, and the covering "
              "documents."),
    "cqa": ("PCMP-001_tab_cqa",
            "Drug substance quality attributes in scope of the campaign, with acceptance "
            "criteria, criticality (Tool #1 score) and the governing process step."),
    "docs": ("PCMP-001_tab_docs",
             "Controlled procedures and validated analytical methods under which the "
             "characterization campaign is executed. Numbers are placeholders in this "
             "synthetic package."),
    "plans": ("PCMP-001_tab_plans",
              "Register of the characterization plans governed by this master plan, with "
              "their paired reports."),
}


def _pcmp_scope_rows():
    """Rendered rows of @tbl-scope, keyed by train key (the document's §4 table)."""
    df = P.char_scope_df()
    return df, row_quotes(df, P.CFG.train_order, P._auto_floatfmt(df))


def _pcmp_plan_rows():
    """Rendered rows of @tbl-plans — the plan/report pair that covers each step."""
    df = P.pd.DataFrame(
        [[f"PCP-{P.CFG.unit_op(k).step:03d}",
          P.DOC_REGISTRY[f"PCP-{P.CFG.unit_op(k).step:03d}"][1],
          f"PCR-{P.CFG.unit_op(k).step:03d}"] for k in P.CFG.train_order],
        columns=["Plan", "Subject", "Paired report"])
    return row_quotes(df, P.CFG.train_order)


def _pcmp_cqa_rows():
    """Rendered rows of @tbl-cqa, keyed by CQA key.

    The document builds this table as ``all_cqas()`` plus a ``Governing step`` column, so
    the row carries the attribute, its acceptance interval, its criticality, its Tool #1
    score AND the step the register names as governing it. The previous annex quoted the
    bare attribute name, which names neither the criterion nor the step and recurs in the
    prose around the table.
    """
    df = P.all_cqas().copy()
    df["Governing step"] = [f"Step {P.CFG.unit_op(s).step} — {P.UNIT_OP_TITLES[s]}"
                            for s in P.cqa_reg["set_by"]]
    return row_quotes(df, P.cqa_reg["key"], P._auto_floatfmt(df))


def _pcmp_doc_rows():
    """Rendered rows of @tbl-docs (``all_sop_table(include_base=True)``), keyed by ID.

    ``all_sop_table`` returns markdown rather than a DataFrame, so the row is rebuilt from
    that markdown exactly as ``_md_rows`` rebuilds one from ``show``.
    """
    rows = {}
    for line in P.all_sop_table(include_base=True).splitlines()[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows[cells[0]] = (cells[1], cells[2], " ".join(c for c in cells if c))
    return rows


# The sentence that qualifies the ACCEPTANCE COLUMN for each form of criterion. §3 states
# plainly that the column "prints an interval for every attribute, so a one-sided criterion
# appears there with both of its bounds" — so an annex record that carried the printed
# interval alone would assert a two-sided criterion the document explicitly denies for
# seven of the ten attributes. Each acceptance-criterion assertion therefore also anchors on
# the sentence that says which bound is in fact a limit.
def _pcmp_spec_form_quote(spec_type, n_two_sided, n_viral):
    return {
        "two_sided": (f"{n_two_sided} attributes carry a two-sided range, because both a low "
                      "and a high result are a quality concern (the glycan attributes)."),
        "upper": ("The process impurities and the size and charge variants carry an upper "
                  "limit only, since the concern is an elevated level."),
        "lower": (f"The {n_viral} viral safety attributes carry a lower limit, expressed as a "
                  "cumulative log reduction across the process."),
    }[spec_type]


def _pcmp_steps(doc, file):
    """One record per unit operation, anchored on its scope row and its register row."""
    sec_id, sec_title = f"{doc}_sec_scope", "Risk-based prioritization"
    scope, rows = _pcmp_scope_rows()
    plans = _pcmp_plan_rows()
    scope_tab, plan_tab = PCMP_TAB["scope"], PCMP_TAB["plans"]
    out = []
    for key in P.CFG.train_order:
        uo = P.CFG.unit_op(key)
        r = scope[scope["Step"] == uo.step].iloc[0]
        out.append(S.ProcessStep(
            # Two surface forms, one per anchor: the plan register says "Harvest and
            # Clarification", the scope table says "Harvest / Clarification". Both are
            # rendered, and each is attested by the row it is taken from.
            step_id=f"step:{key}", step_name=P.UNIT_OP_TITLES[key], step_number=str(uo.step),
            unit_operation=r["Unit operation"],
            # The only per-step description PCMP-001 gives is the characterization scope
            # it assigns the step. The process-train roles ("forms the glycan CQAs", …)
            # belong to PTP-001 and PCMR-001; this document never states them.
            description=(f"{r['Parameters']} parameters carried into the campaign, "
                         f"{r['Multivariate']} studied in a multivariate design and "
                         f"{r['Univariate']} univariately; covered by {r['Documents']}."),
            source_references=[
                ref(doc, file, sec_id, sec_title, rows[key],
                    table_title=scope_tab[1], table_id=scope_tab[0]),
                ref(doc, file, f"{doc}_sec_register", "Register of characterization plans",
                    plans[key], table_title=plan_tab[1], table_id=plan_tab[0])],
            metadata=meta()))
    return out


def _pcmp_cqas(doc, file):
    """One record per drug substance quality attribute, anchored on its own @tbl-cqa row."""
    sec_id, sec_title = f"{doc}_sec_cqa", "Critical quality attribute framework"
    rows = _pcmp_cqa_rows()
    tab = PCMP_TAB["cqa"]
    out = []
    for r in P.cqa_reg.to_dict("records"):
        out.append(S.QualityAttribute(
            attribute_id=f"attr:{r['key']}", attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"], acceptance_criteria=[f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"],
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            # tool2_severity is deliberately absent: @tbl-cqa renders the Tool #1 score only,
            # and PCMP-001 states no severity anywhere, so no span could attest one.
            associated_steps=[f"Step {P.CFG.unit_op(r['set_by']).step} — "
                              f"{P.UNIT_OP_TITLES[r['set_by']]}"],
            source_references=[ref(doc, file, sec_id, sec_title, rows[r["key"]],
                                   table_title=tab[1], table_id=tab[0])],
            metadata=meta()))
    return out


def _pcmp_methods(doc, file):
    """The validated analytical methods @tbl-docs registers, one record per rendered row."""
    sec_id, sec_title = f"{doc}_sec_methods", "Scale-down model strategy"
    rows = _pcmp_doc_rows()
    tab = PCMP_TAB["docs"]
    out = []
    for ref_id, (title, kind, row) in rows.items():
        if kind != "Method validation":
            continue
        out.append(S.AnalyticalMethod(
            method_id=ref_id, method_name=title, method_type=kind,
            # §1 states the campaign "uses those methods as validated"; the row's Type cell
            # is the span that says this reference is the method-validation document.
            validation_status="validated",
            source_references=[ref(doc, file, sec_id, sec_title, row,
                                   table_title=tab[1], table_id=tab[0])],
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


def build_master_plan():
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    from annex_contract.concepts import ConceptStore
    from annex_contract.summaries import ReportSection, ReportStatement
    import ra_content as RC
    doc, f = "PCMP-001", PCMP_FILE
    A, n = [], [0]
    # Campaign scope, from the same table the document renders and sums in its own SETUP
    # chunk (@tbl-scope), so the annex and the prose cannot disagree on a count.
    scope, scope_rows = _pcmp_scope_rows()
    n_steps = len(scope)
    n_params = int(scope["Parameters"].sum())
    n_multi = int(scope["Multivariate"].sum())
    n_uni = int(scope["Univariate"].sum())
    n_cqa = len(P.cqa_reg)
    n_critical = int(P.cqa_reg["criticality"].isin(["H", "VH"]).sum())
    n_viral = int((P.cqa_reg["category"] == "viral safety").sum())
    n_two_sided = int((P.cqa_reg["spec_type"] == "two_sided").sum())
    n_ppq, n_mc = P.V["n_ppq"], P.V["n_monte_carlo"]
    assert n_params == RC.ra_summary()["n"], "scope table and RA-001 disagree on parameter count"
    cqa_rows = _pcmp_cqa_rows()
    scope_tab, cqa_tab = PCMP_TAB["scope"], PCMP_TAB["cqa"]

    def add(subj, pred, obj, text, sec, quote, extra=(), table=None):
        n[0] += 1
        srcs = [ref(doc, f, f"{doc}_sec", sec, quote,
                    table_title=table[1] if table else None,
                    table_id=table[0] if table else None)]
        srcs += [ref(doc, f, f"{doc}_sec", s, q) for s, q in extra]
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text, source_references=srcs, metadata=meta()))

    # The train, anchored on the scope row that names the step and its study assignment.
    for key in P.CFG.train_order:
        uo = P.CFG.unit_op(key)
        add("process:amab_ds", "process_has_step", f"step:{key}",
            f"The A-Mab drug substance process has the step "
            f"{scope[scope['Step'] == uo.step].iloc[0]['Unit operation']}.",
            "Risk-based prioritization", scope_rows[key], table=scope_tab)

    # Every attribute, twice: the criterion it must meet, and the step @tbl-cqa names as
    # governing it. Both ends of each relation sit in the same rendered row.
    #
    # Two qualifications the document makes explicitly, carried as a second anchor rather
    # than dropped. (a) The acceptance column prints an interval even where only one bound
    # is a limit, so each criterion assertion also cites the sentence that says which bound
    # binds. (b) The governing-step column names the step that SETS the result, not the only
    # step involved: §3 says so for the two cumulative viral claims, and separately for host
    # cell protein and residual DNA, whose level is set by clearance downstream.
    gov_note = {
        "lrv_xmulv": ("Critical quality attribute framework",
                      "Those attributions name the step that sets the cumulative result, and "
                      "not the only step that clears virus."),
        "lrv_mvm": ("Critical quality attribute framework",
                    "Those attributions name the step that sets the cumulative result, and "
                    "not the only step that clears virus."),
        "hcp": ("Critical quality attribute framework",
                "Host cell protein and residual DNA arise in cell culture, but the level in "
                "drug substance is set by the clearance achieved in the purification train, "
                "and that clearance is characterized in PCP-005, PCP-007 and PCP-008."),
        "residual_dna": ("Critical quality attribute framework",
                         "Host cell protein and residual DNA arise in cell culture, but the "
                         "level in drug substance is set by the clearance achieved in the "
                         "purification train, and that clearance is characterized in PCP-005, "
                         "PCP-007 and PCP-008."),
    }
    for r in P.cqa_reg.to_dict("records"):
        key = r["key"]
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{key}_acc",
            f"{r['cqa']} acceptance: {r['acc_low']:g}–{r['acc_high']:g} {r['unit']} "
            f"({r['spec_type'].replace('_', '-')} criterion).",
            "Critical quality attribute framework", cqa_rows[key],
            extra=[("Critical quality attribute framework",
                    _pcmp_spec_form_quote(r["spec_type"], n_two_sided, n_viral))],
            table=cqa_tab)
    for r in P.cqa_reg.to_dict("records"):
        key, step = r["key"], r["set_by"]
        add(f"step:{step}", "step_has_quality_attribute", f"attr:{key}",
            f"{P.UNIT_OP_TITLES[step]} is the step the register names as governing "
            f"{r['cqa']}.",
            "Critical quality attribute framework", cqa_rows[key],
            extra=[gov_note[key]] if key in gov_note else (), table=cqa_tab)

    def stx(i, text, sec, quote):
        return ReportStatement(statement_id=f"{doc}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=[ref(doc, f, f"{doc}_sec", sec, quote)])
    report_sections = [ReportSection(section_id=f"{doc}-summary", title="Master plan summary", statements=[
        stx(1, "PCMP-001 governs the Stage 1 characterization of the A-Mab drug substance "
               f"process across the {n_steps} unit operations of the train (Steps 3 to 10).",
            "Purpose and scope",
            "This master plan governs the Stage 1 characterization of the A-Mab drug "
            "substance process."),
        stx(2, "The master plan states the common framework once so that each characterization "
               "plan carries only what is specific to its own unit operation.",
            "Purpose and scope",
            "Each characterization plan then carries only what is specific to its own unit "
            "operation."),
        stx(3, f"The campaign covers {n_params} process parameters and {n_cqa} drug substance "
               "quality attributes.",
            "Purpose and scope",
            f"The campaign covers {n_params} process parameters and {n_cqa} drug substance "
            "quality attributes."),
        stx(4, f"Of the {n_params} parameters, RA-001 assigns {n_multi} to a multivariate "
               f"design and {n_uni} to univariate study.",
            "Risk-based prioritization",
            f"Of the {n_params} parameters carried into the assessment, {n_multi} are assigned "
            f"to a multivariate design and {n_uni} to univariate study."),
        stx(5, "RA-001 sets the scope of the campaign, and the master plan does not repeat the "
               "assessment.",
            "Risk-based prioritization",
            "RA-001 sets the scope of the campaign, and this plan does not repeat the "
            "assessment."),
        stx(6, "The study-type assignment is prospective: it records what was known before the "
               "studies were executed and is revisited when the reports are written.",
            "Risk-based prioritization",
            "The assignment is prospective. It reflects what was known before the studies were "
            "executed, and it is revisited when the reports are written."),
        stx(7, f"The register carries {n_critical} attributes of high or very high criticality, "
               "and those are the ones treated as critical.",
            "Critical quality attribute framework",
            f"The register carries {n_critical} attributes of high or very high criticality, and "
            "those are the ones treated as critical"),
        stx(8, "The acceptance criteria are inputs to the campaign, taken from the clinical and "
               "non-clinical data package, and the plan does not re-derive them.",
            "Critical quality attribute framework",
            "They come from the clinical and non-clinical data package and from prior product "
            "experience, and this plan does not re-derive them."),
        stx(9, "Where a study shows that a criterion cannot be met across the ranges studied, "
               "the criterion is not adjusted to fit the result.",
            "Critical quality attribute framework",
            "the criterion is not adjusted to fit the result."),
        stx(10, "Every characterization study is executed on a scale-down model qualified against "
                "the commercial scale process before the study starts.",
            "Scale-down model strategy",
            "Every characterization study is executed on a scale-down model that has been "
            "qualified against the commercial scale process before the study starts."),
        stx(11, "The campaign uses the registered analytical methods as validated; validating "
                "them is outside the scope of this plan.",
            "Purpose and scope",
            "the campaign uses those methods as validated."),
        stx(12, "The screening model identifies the active parameters; the response-surface model "
                "is the predictive model and the basis of the design space.",
            "Common statistical approach",
            "The screening model identifies the active parameters, and the response-surface "
            "model is the predictive model and the basis of the design space."),
        stx(13, "The screening design is close to saturated, so its fit is not used to predict.",
            "Common statistical approach",
            "The screening design is close to saturated, and its fit is not used to predict."),
        stx(14, f"Capability is estimated by simulating {n_mc:,} commercial scale batches with "
                "every parameter drawn about its set-point.",
            "Common statistical approach",
            f"{n_mc:,} commercial scale batches are simulated with every parameter drawn about "
            "its set-point"),
        stx(15, "The plan sets no campaign-wide numeric threshold for capability; each step's "
                "plan states any threshold agreed for that step.",
            "Parameter classification",
            "This plan sets no campaign-wide numeric threshold for capability."),
        stx(16, "A capability figure is not by itself evidence that the process is in a state of "
                "control.",
            "Parameter classification",
            "A capability figure is not by itself evidence that the process is in a state of "
            "control."),
        stx(17, "Characterization on scale-down models does not qualify the commercial process; "
                f"that is the purpose of the {n_ppq} Stage 2 process performance qualification "
                "batches.",
            "Stage 1 characterization strategy",
            "Characterization on scale-down models does not qualify the commercial process. "
            f"That is the purpose of Stage 2, in which {n_ppq} process performance "
            "qualification batches are run at commercial scale under a separate protocol."),
        stx(18, "Each characterization report is issued once the studies in its plan are complete "
                "and analysed, and PCMR-001 is issued after the last of them.",
            "Deliverables and schedule",
            "Each report is issued after the studies in its plan are complete and analysed. "
            "PCMR-001 is issued after the last report and consolidates them."),
    ])]
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_scope",
                                  process_steps=_pcmp_steps(doc, f)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=_pcmp_cqas(doc, f)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_methods",
                                  analytical_methods=_pcmp_methods(doc, f)),
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
        weak_claims=build_weak_claims(doc, f),
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT,
        out_of_schema_notes=[
            "Master plan spans the whole train; entities are the Step 3-10 process steps, the CQA "
            "framework and the validated analytical methods the campaign is executed under.",
            "PCMP-001 renders no process-train table. Each process-step record is anchored on its "
            "row of the characterization scope table and on its row of the plan register, and its "
            "description is the study scope the plan assigns the step - the principal-role "
            "descriptions belong to PTP-001 and PCMR-001 and are not stated here.",
            "QualityAttribute.tool2_severity is deliberately absent: the attribute table renders "
            "the Tool #1 criticality score only, and no severity is stated anywhere in the "
            "document, so no span could attest one.",
            "The acceptance column prints an interval for every attribute even where the criterion "
            "is one-sided. Each attribute_has_acceptance_criterion assertion therefore carries a "
            "second reference to the sentence that states which bound is the limit, and the "
            "assertion text names the criterion form.",
            "step_has_quality_attribute records the GOVERNING step the attribute register names, "
            "not the only step that acts on the attribute. The two cumulative viral clearance "
            "claims and the two cell-culture-derived impurities carry a second reference to the "
            "sentence that qualifies the attribution.",
            "Strictly prospective: the plan carries no characterization results, no set-point, NOR "
            "or PAR, no design space and no parameter classification - those are outputs of the "
            "per-unit-operation studies. It also sets no campaign-wide numeric capability "
            "threshold, so no capability entity is asserted here.",
            "No rhetorical_spans layer. Per authoring/RHETORICAL_ANNEX.md the discourse layer "
            "covers the eight PCR-00N reports, PCMR-001 and RA-001; the plans (PCP-00N, PCMP-001, "
            "PTP-001) carry none, and PCMP-001 follows that corpus convention.",
        ],
        inventory=inv, entities=entities, report_sections=report_sections,
        assertions=AssertionStore(run_id=f"gt-{doc}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id="gt-pcmp", concepts=_corpus_step_concepts()))


# =========================================================================== #
# PCMR-001 — Process Characterization Master Report (roll-up of PCR-003…010).   #
# --------------------------------------------------------------------------- #
# Consolidates the per-unit-operation reports. Every per-record quote below is   #
# the RENDERED TABLE ROW, rebuilt here from the same seeded register the report  #
# renders (@tbl-train, @tbl-scope, @tbl-yield, @tbl-cqa-scope, @tbl-cqa-outcome, #
# @tbl-cpp, @tbl-cap, @tbl-viral, @tbl-methods, @tbl-dev, @tbl-equipment), so    #
# the span literally carries both ends of the relation it anchors and follows    #
# the register on a reseed. Narrative quotes are number-free wherever the number  #
# is not the point, and never contain a rendered cross-reference ("Table 6",      #
# "Section 4"): Quarto emits those from field codes, so the surrounding spacing    #
# is not the author's and a quote that spans one is fragile.                      #
#                                                                                 #
# Re-anchored 2026-07 against the re-authored text. What the previous annex        #
# asserted and this document does NOT say — each record was corrected, not merely  #
# re-quoted:                                                                       #
#   * a two-sided acceptance interval for every attribute. §3.2 states outright     #
#     that for the impurity, size-variant and charge-variant attributes "only the   #
#     upper limit is an acceptance limit", and that the lower figure printed in     #
#     @tbl-cqa-scope "is not an acceptance limit". The criterion asserted here is   #
#     therefore the one @tbl-cqa-outcome renders through the spec type.             #
#   * Tool #1 / Tool #2 criticality scores. This document renders the criticality   #
#     letter only; no span could attest a score, so none is carried.                #
#   * "no single step can be described as the host cell protein control", "Cation   #
#     exchange is the only aggregate clearance step", "No deviation changed a       #
#     parameter classification, an operating region or a viral clearance claim",    #
#     "Neither finding moved the associated attribute outside its limit". The       #
#     re-authored report makes none of these absolute claims; it says "principal    #
#     polishing step" and "not a property of any single step" instead.              #
#   * a capability convention "following the practice described in the process      #
#     validation literature". §5 says only that the report "sets no acceptance      #
#     threshold for the capability index".                                          #
# The campaign deviation register (§8, 17 rows) has no upstream model and is        #
# captured as rhetorical_spans of role 'deviation_disposition', one span per row.   #
# =========================================================================== #
PCMR_FILE = "PCMR-001_master_report.docx"

# @tbl-viral labels its credited steps in its own vocabulary; this maps each rendered
# label onto the train key the rest of the annex uses.
PCMR_VC_STEP = {"Low-pH Viral Inactivation": "viral_inactivation",
                "Anion Exchange (AEX)": "aex", "Virus Filtration": "virus_filtration"}
# Table captions, used verbatim as the SourceReference.table_title of a row quote.
PCMR_TAB = {
    "train": ("PCMR-001_tab_train",
              "The A-Mab drug substance process train and the role of each step."),
    "scope": ("PCMR-001_tab_scope",
              "Characterization scope by unit operation, with the covering plan and report."),
    "yield": ("PCMR-001_tab_yield",
              "Step and cumulative product yield across the drug substance train."),
    "cqa": ("PCMR-001_tab_cqa_scope",
            "The drug substance quality attribute register, with the step that sets each "
            "attribute and the report that characterizes it."),
    "outcome": ("PCMR-001_tab_cqa_outcome",
                "Simulated commercial-scale outcome for every drug substance quality attribute."),
    "cpp": ("PCMR-001_tab_cpp",
            "The quality-linked process parameters of the drug substance train, with their "
            "set-points and normal operating ranges."),
    "cap": ("PCMR-001_tab_cap",
            "Commercial-scale process capability for every drug substance quality attribute."),
    "viral": ("PCMR-001_tab_viral",
              "Modular viral clearance by credited step, in log10 reduction, against the drug "
              "substance requirement."),
    "methods": ("PCMR-001_tab_methods",
                "Validated performance of the analytical methods the campaign relies on."),
    "dev": ("PCMR-001_tab_dev",
            "Deviations recorded across the characterization campaign."),
    "equip": ("PCMR-001_tab_equipment",
              "Instrumented scale-down systems under calibration and change control."),
}


def _md_rows(df, floatfmt=None):
    """Every rendered row of a ``_pcpkg.show``-style table, whitespace-collapsed.

    ``show`` emits ``df.to_markdown(index=False, floatfmt=...)`` and Quarto turns each markdown
    row into a docx table row, whose cells are read back separated by whitespace. Rebuilding the
    row from the same DataFrame therefore reproduces the rendered row verbatim — which is what
    lets a per-record quote span the whole relation instead of a generic sentence about it.
    """
    rows = []
    for line in df.to_markdown(index=False, floatfmt=floatfmt or ".3g").splitlines()[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(" ".join(c for c in cells if c))
    return rows


def _pcmr_registers():
    """Every register PCMR-001 renders, as {record key -> rendered row text}.

    The re-authored report shows eleven tables, and each is rebuilt here from the same
    helper call the document makes, with the same ``floatfmt`` — plain ``show(df)`` means
    ``P._auto_floatfmt(df)``, and where the document passes a format explicitly (the yield
    waterfall, the capability table, the viral register) that format is repeated here.
    A row rebuilt any other way stops being verbatim on the first reseed.
    """
    train = train_row_quotes()                                   # @tbl-train (shared w/ PTP-001)

    scope_df = P.char_scope_df()                                 # @tbl-scope
    scope = row_quotes(scope_df, P.CFG.train_order, P._auto_floatfmt(scope_df))
    # @tbl-yield: the document passes this floatfmt because the automatic choice prints
    # 97.68 % as 97.7 and 100.0 % as 100.
    yld = row_quotes(P.yield_waterfall_df(), P.CFG.train_order, [".0f", "", ".1f", ".1f"])

    keys = list(P.cqa_reg["key"])
    reg_df = P.cqa_scope_df()                                    # @tbl-cqa-scope
    cqa = row_quotes(reg_df, keys, P._auto_floatfmt(reg_df))
    out_df = P.cqa_outcome_df()                                  # @tbl-cqa-outcome
    outcome = row_quotes(out_df, list(P.cap["key"]), P._auto_floatfmt(out_df))
    cap = row_quotes(P.cap_for(keys), list(P.cap[P.cap.key.isin(keys)]["key"]), ".2f")

    q = P.param_reg[P.param_reg.classification.isin(["CPP", "WC-CPP"])]
    par = dict(zip(zip(q.unit_operation, q.parameter), _md_rows(P.cpp_params())))

    vc_df = P.viral_clearance_df()                               # @tbl-viral
    viral = row_quotes(vc_df, list(vc_df["Step"]), ".2f")

    meth_df = P.method_perf_df(precision_with_unit=True)         # @tbl-methods
    methods = row_quotes(meth_df, list(meth_df["Method"]), P._auto_floatfmt(meth_df))
    dev_df = P.dev_register_all()                                # @tbl-dev
    dev = row_quotes(dev_df, list(dev_df["Deviation"]), P._auto_floatfmt(dev_df))
    eq_df = P.equipment_df()                                     # @tbl-equipment
    equip = row_quotes(eq_df, list(eq_df["Equipment"]), P._auto_floatfmt(eq_df))
    return train, scope, yld, cqa, outcome, cap, par, viral, methods, dev, equip


(PCMR_TRAIN_ROW, PCMR_SCOPE_ROW, PCMR_YIELD_ROW, PCMR_CQA_ROW, PCMR_OUT_ROW,
 PCMR_CAP_ROW, PCMR_PAR_ROW, PCMR_VC_ROW, PCMR_METHOD_ROW, PCMR_DEV_ROW,
 PCMR_EQUIP_ROW) = _pcmr_registers()

# Which step is credited with which cumulative viral-clearance CQA in @tbl-viral. The low-pH
# hold is deliberately absent from MVM: it contributes 0.00 log10 against a non-enveloped
# parvovirus, and the report says so.
PCMR_VC_CREDIT = [
    ("viral_inactivation", "lrv_xmulv"), ("aex", "lrv_xmulv"), ("aex", "lrv_mvm"),
    ("virus_filtration", "lrv_xmulv"), ("virus_filtration", "lrv_mvm"),
]
PCMR_VC_ROW_FOR = {v: PCMR_VC_ROW[k] for k, v in PCMR_VC_STEP.items()}

# Scalars the narrative spans quote. Each is read from the seeded model exactly as the
# document's inline expression reads it, so a reseed moves the quote and the sentence it
# anchors on together. Nothing below is typed.
_PCMR_CC = P.class_counts()
_PCMR_SCOPE_DF = P.char_scope_df()
_PCMR_DEV_DF = P.dev_register_all()
_PCMR_VC_DF = P.viral_clearance_df()
_PCMR_PSUM = P.csv("process_summary.csv").set_index("step")
_N = dict(
    n_params=int(P.V["n_parameters"]),
    n_quality_linked=int(P.V["n_cpp"]),
    n_cqa=len(P.cqa_reg),
    n_bio=int((P.cqa_reg.set_by == "bioreactor").sum()),
    n_cpp=_PCMR_CC["CPP"], n_wc=_PCMR_CC["WC-CPP"],
    n_kpp=_PCMR_CC["KPP"], n_gpp=_PCMR_CC["GPP"],
    n_dev=int(P.V["n_deviations"]),
    n_dev_reports=int(_PCMR_DEV_DF["Report"].nunique()),
    n_dev_retained=int((_PCMR_DEV_DF["Disposition"] == "retained").sum()),
    n_viral_steps=len(_PCMR_VC_DF) - 2,
    min_cpk=f"{float(P.V['min_cpk']):.2f}",
    yield_pct=P.pct(P.V["overall_yield"]),
    min_step_yield=f"{float(P.yield_waterfall_df()['Step yield (%)'].min()):.1f}",
    agg_fold=f"{float(_PCMR_PSUM.loc[7, 'aggregate_clearance_fold']):.1f}",
    hold_h=f"{float(P.dev_008_01_neutralized_hold_h):.0f}",
    ver_n=f"{float(P.dev_008_02_ver_n):.0f}",
)

# Narrative (non-tabular) argument structure of the report, re-anchored against the
# re-authored text; (id, role, section, quote, supported_by, restates, bounds). Quotes are
# number-free unless the number is the claim, and none of them spans a rendered
# cross-reference — Quarto writes "Table 6" and "Section 4" out of a field code, so the
# whitespace around them belongs to the renderer rather than to the author.
PCMR_RHET_SPANS = [
    # --- Executive summary: the thesis, its three supports, and the two bounds on it ----
    ("R00", "claim", "Executive summary",
     "The A-Mab drug substance process is characterized and its control strategy is defined.",
     ["R01", "R02", "R03"], None, None),
    ("R01", "justification", "Executive summary",
     f"The campaign carried {_N['n_params']} process parameters into study, of which "
     f"{_N['n_quality_linked']} are linked to a critical quality attribute and are held inside "
     f"the design space.", [], None, None),
    ("R02", "justification", "Executive summary",
     f"All {_N['n_cqa']} drug substance quality attributes met their acceptance criteria.",
     [], None, None),
    ("R03", "justification", "Executive summary",
     "Cumulative viral clearance exceeds its requirement for both model viruses.",
     [], None, None),
    ("R04", "bounded_conclusion", "Executive summary",
     "Capability, proven acceptable ranges and viral clearance are estimated from qualified "
     "scale-down models with the parameters held close to their set-points, so the edges of the "
     "design space have not been run at commercial scale and nothing in this report describes "
     "the behaviour of the process there.", [], None, "R00"),
    ("R05", "bounded_conclusion", "Executive summary",
     "Stage 2 has not been executed, so this report presents no process performance "
     "qualification data and makes no claim about the performance of any batch made at "
     "commercial scale.", [], None, "R00"),
    # --- Introduction ------------------------------------------------------------------
    ("R06", "deferral", "The campaign and its documents",
     "It does not repeat their analyses, and where a figure here comes from one of them, that "
     "report is named.", [], None, None),
    ("R07", "claim", "Scope of the characterization",
     "the response surface model is the predictive model, which makes it the basis of the "
     "design space and of the proven acceptable ranges reported in each unit operation report",
     [], None, None),
    ("R08", "bounded_conclusion", "Scope of the characterization",
     "Nothing in this report rests on a screening fit.", [], None, "R07"),
    ("R09", "justification", "Scope of the characterization",
     "Harvest and clarification (Step 4) and the ultrafiltration and diafiltration step "
     "(Step 10) carried none, because neither step forms a product quality attribute",
     [], None, None),
    # --- Process description and performance --------------------------------------------
    ("R10", "claim", "The process train",
     "The quality burden is not spread evenly across the train.", ["R11"], None, None),
    ("R11", "justification", "The process train",
     f"The production bioreactor sets {_N['n_bio']} of the {_N['n_cqa']} quality attributes, "
     f"which is more than any other step", [], None, None),
    ("R12", "bounded_conclusion", "Nominal batch performance",
     "Yield is a process performance attribute and not a quality attribute, so no step yield is "
     "an acceptance criterion.", [], None, None),
    ("R13", "justification", "Nominal batch performance",
     f"is reduced {_N['agg_fold']}-fold at cation exchange, which is why that step is described "
     f"as the principal aggregate polish", [], None, None),
    # --- Consolidated quality attribute outcomes -----------------------------------------
    ("R14", "cross_step_credit", "The attributes and where they are set",
     "Host cell protein and residual DNA are generated in the culture and are cleared by "
     "Protein A capture (PCR-005), cation exchange (PCR-007) and anion exchange (PCR-008).",
     [], None, None),
    ("R15", "cross_step_credit", "The attributes and where they are set",
     "Aggregate is formed in the bioreactor (PCR-003), rises across the low-pH hold (PCR-006) "
     "and is reduced at cation exchange (PCR-007), the principal polishing step for it.",
     [], None, None),
    ("R16", "mechanistic_warrant", "The attributes and where they are set",
     "The platform purification steps do not separate glycosylation variants of a monoclonal "
     "antibody", [], None, None),
    # §3.2 is where the report qualifies its own acceptance column: the lower figure printed
    # against a one-sided attribute is not a limit. Every acceptance-criterion assertion in
    # this annex is anchored on the @tbl-cqa-outcome row, which applies the spec type.
    ("R17", "problem_statement", "Outcome against the acceptance criteria",
     "because the specification for acidic charge variants is one-sided and the risk it "
     "addresses is an elevated level", [], None, None),
    ("R18", "hedge", "Outcome against the acceptance criteria",
     "whose simulated concentrations lie far below the limit, so its capability index is "
     "correspondingly large and carries no information beyond that", [], None, None),
    ("R19", "claim", "Outcome against the acceptance criteria",
     "High mannose and the two viral clearance attributes sit closest to their limits, and they "
     "are the attributes on which the operating region is effectively binding", [], None, None),
    ("R20", "cross_step_credit", "Outcome against the acceptance criteria",
     "The impurity attributes clear their limits by a wide margin, which is a property of a "
     "train in which the capture step and both polishing steps remove them, and not a property "
     "of any single step.", [], None, None),
    ("R21", "bounded_conclusion", "Outcome against the acceptance criteria",
     "The outcome in each row is a simulated one.", [], None, "R02"),
    ("R22", "bounded_conclusion", "Outcome against the acceptance criteria",
     "It is not a measurement of commercial equipment, and the attribute levels are confirmed "
     "at scale during Stage 2.", [], None, None),
    # --- Parameter classification --------------------------------------------------------
    ("R23", "justification", "The classification across the train",
     "The distinction between the two quality-linked classes is the risk of leaving the design "
     "space and not the size of the effect", [], None, None),
    ("R24", "claim", "The classification across the train",
     "The class therefore follows from the control capability of the equipment as much as from "
     "the result of the study.", ["R23"], None, None),
    ("R25", "bounded_conclusion", "The classification across the train",
     "every one of them is held within a normal operating range that lies at or inside the "
     "edges of the range characterized for it", [], None, None),
    ("R26", "justification", "The exceptions",
     "The parameter governs the enveloped-virus clearance claim, an attribute of very high "
     "criticality", [], None, None),
    ("R27", "hedge", "The exceptions",
     "so its classification rests on a bounding argument and not on a measured multivariate "
     "effect", [], None, None),
    ("R28", "justification", "Null results and what they are worth",
     "The absence of an effect over a characterized range is evidence that the attribute is "
     "robust to the parameter over that range, but it is not evidence about conditions outside "
     "it.", [], None, None),
    # --- Process capability ---------------------------------------------------------------
    ("R29", "cross_step_credit", "Process capability",
     "Both are governed by more than one step, so neither figure is the property of a single "
     "unit operation", [], None, None),
    ("R30", "claim", "Process capability",
     "This report sets no acceptance threshold for the capability index, and each index is "
     "reported with the margin between the simulated mean and the governing limit, which is the "
     "quantity a control decision acts on.", [], None, None),
    ("R31", "bounded_conclusion", "Process capability",
     "The capability estimate is built on qualified scale-down models and inherits their "
     "assumptions about feed states and about scale independence.", [], None, None),
    ("R32", "bounded_conclusion", "Process capability",
     "It describes the process operating near its set-points, so it says nothing about "
     "performance at the edges of the design space, which have not been run at commercial "
     "scale.", [], None, "R30"),
    # --- Viral clearance --------------------------------------------------------------------
    ("R33", "justification", "The modular claim",
     "The claim is modular in the sense of ICH Q5A, which means that each step was spiked and "
     "studied independently on a qualified small-scale model and the step increments are then "
     "added", [], None, None),
    ("R34", "mechanistic_warrant", "The modular claim",
     "because a parvovirus has no lipid envelope for low pH to act on", [], None, None),
    ("R35", "claim", "Orthogonality, and what is not claimed",
     "Adding the step increments is only defensible if the mechanisms are independent, and the "
     "three mechanisms differ.", ["R36"], None, None),
    ("R36", "mechanistic_warrant", "Orthogonality, and what is not claimed",
     "Low pH inactivates by disrupting the viral envelope, anion exchange partitions virus from "
     "product by charge in a step where the product flows through and the impurities bind, and "
     "virus filtration removes by size on a membrane rated for small non-enveloped viruses.",
     [], None, None),
    ("R37", "hedge", "Orthogonality, and what is not claimed",
     "The campaign did not study conditions that act on more than one step at once, so that "
     "expectation rests on the mechanisms and not on a cross-step experiment.", [], None, "R35"),
    ("R38", "bounded_conclusion", "Orthogonality, and what is not claimed",
     "No clearance is claimed for the Protein A step or for the cation exchange step",
     [], None, None),
    ("R39", "hedge", "Orthogonality, and what is not claimed",
     "Neither step was studied for viral clearance in this campaign, so the cumulative claim is "
     "conservative to the extent of whatever those two steps deliver.", ["R38"], None, "R03"),
    ("R40", "bounded_conclusion", "Orthogonality, and what is not claimed",
     "The log reduction values come from spiking studies on small-scale models and are not "
     "measurements of the commercial process.", [], None, None),
    # --- Control strategy --------------------------------------------------------------------
    ("R41", "justification", "What the control strategy has to do",
     "The two purposes need different evidence, which is why a key process parameter is "
     "controlled even though it was shown not to move a quality attribute", [], None, None),
    ("R42", "deferral", "Parameter control",
     "are reported per step and per attribute in the report for that step, and are not "
     "reproduced here", [], None, None),
    ("R43", "justification", "Release testing",
     "A release result arrives after the batch has been made, so testing at release cannot by "
     "itself control an attribute", [], None, None),
    ("R44", "claim", "Release testing",
     "For this reason the control strategy places the burden on the parameter ranges and the "
     "in-process controls, and uses release testing to confirm the outcome.",
     ["R43"], None, None),
    ("R45", "claim", "Life-cycle and feed-input controls",
     "One feed-input control follows from a deviation.", ["R46"], None, None),
    ("R46", "justification", "Life-cycle and feed-input controls",
     f"used a load that had been held neutralized for {_N['hold_h']} hours, which raised its "
     f"acidic charge variant content well above the level of routine material",
     [], None, None),
    ("R47", "bounded_conclusion", "What the control strategy does not cover",
     "It does not by itself show that the commercial process is in a state of control, which is "
     "the purpose of Stage 2 and of the continued process verification that follows it.",
     [], None, None),
    # --- Deviations ----------------------------------------------------------------------------
    ("R48", "problem_statement", "Deviations across the campaign",
     f"The campaign recorded {_N['n_dev']} deviations across the {_N['n_dev_reports']} unit "
     f"operation studies, and one of them invalidated a designed experiment.", [], None, None),
    ("R49", "deferral", "Deviations across the campaign",
     "The investigation, the root cause and the impact assessment for each are in the report "
     "named in the register, and are not repeated here.", [], None, None),
    ("R50", "deviation_disposition", "The deviation that invalidated a study",
     "A load in that condition is not representative of routine material, so the screening and "
     "response surface designs executed on it were invalidated for the purpose of defining an "
     "operating region, and both were re-executed in full on requalified load.",
     [], None, None),
    ("R51", "deviation_disposition", "The deviation that invalidated a study",
     "The analysis reported in PCR-008 is the re-execution, and the first execution is retained "
     "there as a superseded dataset and referenced to confirm the root cause.",
     ["R50"], None, None),
    ("R52", "deviation_disposition", "The deviation that invalidated a study",
     f"The effect on the pool was modelled and then checked against {_N['ver_n']} verification "
     f"runs, and PCR-008 gives the assessment.", [], None, None),
    ("R53", "deviation_disposition", "The retained deviations",
     f"In {_N['n_dev_retained']} cases the deviation was retained, which means the affected "
     f"data were kept in the analysis with an argument that bounds the impact.",
     [], None, None),
    ("R54", "bounded_conclusion", "The retained deviations",
     "Some are single-run excursions of a controlled parameter that stayed inside the range the "
     "study itself covered.", [], None, None),
    ("R55", "justification", "The retained deviations",
     "were found by checks that run independently of the study analysis, among them buffer "
     "release testing, in-process monitoring, equipment history review, pre-use verification "
     "and post-execution reconciliation", [], None, None),
    ("R56", "justification", "The retained deviations",
     "with their calibration status at the time the affected studies ran, and each was inside "
     "its calibration interval", [], None, None),
    # --- Conclusions ---------------------------------------------------------------------------
    ("R57", "restatement", "Conclusions and Stage 2 readiness",
     "The A-Mab drug substance process is characterized across Steps 3–10 and the campaign "
     "supports a defined control strategy.", [], "R00", None),
    ("R58", "claim", "Conclusions and Stage 2 readiness",
     "Every drug substance quality attribute met its acceptance criterion in the simulated "
     "commercial process.", [], None, None),
    ("R59", "bounded_conclusion", "Conclusions and Stage 2 readiness",
     "Nothing here rests on a screening model, and no proven acceptable range extends beyond "
     "the range its step characterized.", [], None, None),
    ("R60", "bounded_conclusion", "Conclusions and Stage 2 readiness",
     "The capability and clearance figures are estimated on qualified scale-down models and are "
     "not measured on commercial equipment", [], None, "R58"),
    ("R61", "bounded_conclusion", "Conclusions and Stage 2 readiness",
     "The viral clearance values come from small-scale spiking studies.", [], None, None),
    ("R62", "deferral", "Conclusions and Stage 2 readiness",
     "What remains is Stage 2.", [], None, None),
    ("R63", "restatement", "Conclusions and Stage 2 readiness",
     "This report does not qualify the commercial process, and it makes no claim about the "
     "performance of any batch made at commercial scale.", [], "R05", None),
]


def pcmr_rhetorical_spans(doc, f):
    """Argument-structure spans over PCMR-001, plus the 17-row campaign deviation register.

    Every register row is its own ``deviation_disposition`` span, anchored on the rendered
    @tbl-dev row (identifier, the report that investigates it, what happened, the route by
    which it was detected and its disposition), so the disposition of each deviation is
    attested by a span that contains it — not by the section that discusses it.
    """
    out = []
    for suffix, role, sec, quote, sup, res, bnd in PCMR_RHET_SPANS:
        out.append(S.RhetoricalSpan(
            span_id=f"{doc}-{suffix}", section=sec, role=role,
            source_reference=ref(doc, f, f"{doc}_sec_rhet", sec, " ".join(quote.split())),
            supported_by=[f"{doc}-{s}" for s in sup],
            restates=(f"{doc}-{res}" if res else None),
            bounds=(f"{doc}-{bnd}" if bnd else None)))
    for dev_id, row in PCMR_DEV_ROW.items():
        out.append(S.RhetoricalSpan(
            span_id=f"{doc}-{dev_id}", section="Deviations across the campaign",
            role="deviation_disposition",
            source_reference=ref(doc, f, f"{doc}_sec_dev", "Deviations across the campaign",
                                 row, table_title=PCMR_TAB["dev"][1],
                                 table_id=PCMR_TAB["dev"][0]),
            supported_by=[], restates=None, bounds=None))
    return out


def pcmr_steps(doc, f):
    """The Step 3-10 train, each anchored on three of its own rendered rows.

    @tbl-train carries the step number, the unit operation and its role in the control
    strategy; @tbl-scope carries what the campaign studied at that step and the plan/report
    pair that covers it; @tbl-yield carries what the step costs in product. Together they
    are what this document says about a step, and each is a row rather than a caption.
    """
    out = []
    for key in P.CFG.train_order:
        uo = P.CFG.unit_op(key)
        title = P.UNIT_OP_TITLES.get(key, uo.name)
        scope = _PCMR_SCOPE_DF[_PCMR_SCOPE_DF["Step"] == uo.step].iloc[0]
        out.append(S.ProcessStep(
            step_id=f"step:{key}", step_name=title, step_number=str(uo.step),
            unit_operation=title,
            description=(f"{P.UNIT_OP_ROLE.get(key, '')}. Characterization scope: "
                         f"{scope['Parameters']} parameters, {scope['Multivariate']} studied "
                         f"multivariately and {scope['Univariate']} univariately; covered by "
                         f"{scope['Documents']}."),
            source_references=[
                ref(doc, f, f"{doc}_sec_process", "The process train", PCMR_TRAIN_ROW[key],
                    table_title=PCMR_TAB["train"][1], table_id=PCMR_TAB["train"][0]),
                ref(doc, f, f"{doc}_sec_scope", "Scope of the characterization",
                    PCMR_SCOPE_ROW[key], table_title=PCMR_TAB["scope"][1],
                    table_id=PCMR_TAB["scope"][0]),
                ref(doc, f, f"{doc}_sec_process", "Nominal batch performance",
                    PCMR_YIELD_ROW[key], table_title=PCMR_TAB["yield"][1],
                    table_id=PCMR_TAB["yield"][0]),
            ],
            metadata=meta()))
    return out


def pcmr_cqas(doc, f):
    """The 10 drug-substance quality attributes, on three of their own rendered rows.

    ``acceptance_criteria`` carries the criterion **as the spec type applies it** —
    ``≤ 5 % HMW (SEC)``, ``≥ 16.7 log10 (cumulative)`` — which is what @tbl-cqa-outcome
    renders and what §3.2 insists on: for the impurity, size-variant and charge-variant
    attributes "only the upper limit is an acceptance limit", and the lower figure printed
    beside them in @tbl-cqa-scope "is not an acceptance limit". The printed interval is
    carried as well, but second, and only because the register row does render it.

    No Tool #1 or Tool #2 score is carried. This document renders the criticality letter and
    nothing else, so a score would be a value no span in it could attest.
    """
    out = []
    cap_by_key = P.cap.set_index("key")
    for r in P.cqa_reg.to_dict("records"):
        key = r["key"]
        crit = P._criterion_str(cap_by_key.loc[key])
        printed = f"{r['acc_low']:g}–{r['acc_high']:g} {r['unit']}"
        out.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"],
            acceptance_criteria=[crit] + ([] if printed == crit else [printed]),
            associated_steps=[P.UNIT_OP_TITLES.get(r["set_by"], r["set_by"])],
            criticality_level=r["criticality"],
            rationale_for_criticality=(
                f"Consolidated register criticality {r['criticality']}, carried into this "
                f"report from the per-step characterization in "
                f"PCR-{P.CFG.unit_op(r['set_by']).step:03d}. The A-Mab Tool #1 and Tool #2 "
                f"scores are not restated in this document."),
            source_references=[
                ref(doc, f, f"{doc}_sec_cqa", "The attributes and where they are set",
                    PCMR_CQA_ROW[key], table_title=PCMR_TAB["cqa"][1],
                    table_id=PCMR_TAB["cqa"][0]),
                ref(doc, f, f"{doc}_sec_outcome", "Outcome against the acceptance criteria",
                    PCMR_OUT_ROW[key], table_title=PCMR_TAB["outcome"][1],
                    table_id=PCMR_TAB["outcome"][0]),
                ref(doc, f, f"{doc}_sec_cap", "Process capability", PCMR_CAP_ROW[key],
                    table_title=PCMR_TAB["cap"][1], table_id=PCMR_TAB["cap"][0]),
            ],
            metadata=meta()))
    return out


# The analytes @tbl-methods names in a method title, and the drug substance attribute each
# names. The row is the anchor because the row is what pairs the method with the analyte it
# titrates. Four rows are deliberately absent:
#   * the glycan map names no single attribute (it covers all three glycan CQAs at once);
#   * turbidity and A280 are in the table for the other reason §7.5 gives — an in-process
#     control at harvest and the pool the formulation step delivers, not a DS attribute;
#   * THE TWO INFECTIVITY ASSAYS. They are in @tbl-methods, and it is tempting to pair them
#     with the two cumulative clearance attributes by name, but §7.4 says outright that those
#     attributes "are not confirmed in that way, because no test on the drug substance
#     measures them". They are process claims from spiked small-scale models. An annex that
#     asserted attribute_measured_by_method for them would state the opposite of the report.
PCMR_METHOD_ATTR = {"AMV-3221": "aggregates_hmw", "AMV-3012": "hcp",
                    "AMV-3016": "leached_protein_a"}


def pcmr_methods(doc, f):
    """The validated analytical methods @tbl-methods reports, one record per rendered row."""
    meth = P.method_perf_df(precision_with_unit=True)
    out = []
    for r in meth.to_dict("records"):
        mid = r["Method"]
        attr = PCMR_METHOD_ATTR.get(mid)
        out.append(S.AnalyticalMethod(
            method_id=mid, method_name=r["Title"], method_type="analytical method",
            # §7.5: "Every attribute in @tbl-cqa-outcome is measured by a validated method."
            validation_status="validated",
            associated_attributes=([P.cqa_reg[P.cqa_reg.key == attr].iloc[0]["cqa"]]
                                   if attr else []),
            source_references=[ref(doc, f, f"{doc}_sec_analytical", "Analytical control",
                                   PCMR_METHOD_ROW[mid], table_title=PCMR_TAB["methods"][1],
                                   table_id=PCMR_TAB["methods"][0])],
            metadata=meta()))
    return out


# @tbl-equipment describes two of the three scale-down systems by the unit operation they
# belong to; the chromatography chamber names no step, and three chromatography steps are in
# scope, so no step link is asserted for it.
PCMR_EQUIP_STEP = {"EQ-BRX-205": "bioreactor", "EQ-TFF-142": "ufdf"}


def pcmr_equipment(doc, f):
    """The instrumented scale-down systems @tbl-equipment registers, one record per row."""
    out = []
    for r in P.equipment_df().to_dict("records"):
        out.append(S.Equipment(
            equipment_id=r["Equipment"], equipment_name=r["Description"],
            # No site_name. The exec summary says the work was executed "at the sending site"
            # and the title block names that site, but @tbl-equipment pairs no system with a
            # site, so a site on this record would be an inference rather than a label.
            equipment_type="scale-down system",
            source_references=[ref(doc, f, f"{doc}_sec_dev_retained", "The retained deviations",
                                   PCMR_EQUIP_ROW[r["Equipment"]],
                                   table_title=PCMR_TAB["equip"][1],
                                   table_id=PCMR_TAB["equip"][0])],
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
                f"Classified {r['classification']} in {r['unit_operation']}: quality-linked, so "
                f"the commercial process is asked to hold the normal operating range given "
                f"here. §4.1 states that the class turns on the risk of leaving the design "
                f"space rather than on the size of the effect; the decision itself is made in "
                f"the report for the step and is consolidated, not re-derived, here."),
            source_references=[ref(doc, f, f"{doc}_sec_class",
                                   "The classification across the train", r["row"],
                                   table_title=PCMR_TAB["cpp"][1],
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
    meth = P.method_perf_df(precision_with_unit=True)
    for r in meth.to_dict("records"):
        cs.append(Concept(concept_id=f"method:{r['Method']}", concept_type="ANALYTICAL_METHOD",
                          canonical_name=r["Title"], aliases=[r["Method"]],
                          review_status="human_verified"))
    for r in P.equipment_df().to_dict("records"):
        cs.append(Concept(concept_id=f"equipment:{r['Equipment']}", concept_type="EQUIPMENT",
                          canonical_name=r["Description"], aliases=[r["Equipment"]],
                          review_status="human_verified"))
    return cs


def build_master_report():
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    from annex_contract.concepts import ConceptStore
    from annex_contract.summaries import ReportSection, ReportStatement
    doc, f = "PCMR-001", PCMR_FILE
    A, n = [], [0]
    # Campaign scope, read from the same seeded registers the report renders (never typed).
    n_cqa = len(P.cqa_reg)
    cap_by_key = P.cap.set_index("key")
    q_rows = pcmr_quality_linked_params()

    def add(subj, pred, obj, text, refs):
        n[0] += 1
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc}-A{n[0]:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=text, source_references=refs, metadata=meta()))

    def train_ref(key):
        """The step's row of @tbl-train: number, unit operation and its role in the strategy."""
        return ref(doc, f, f"{doc}_sec_process", "The process train", PCMR_TRAIN_ROW[key],
                   table_title=PCMR_TAB["train"][1], table_id=PCMR_TAB["train"][0])

    def cqa_ref(key):
        """The attribute's row of @tbl-cqa-scope: attribute, category, criticality, the printed
        acceptance interval, the step the register assigns it to and the covering report."""
        return ref(doc, f, f"{doc}_sec_cqa", "The attributes and where they are set",
                   PCMR_CQA_ROW[key], table_title=PCMR_TAB["cqa"][1],
                   table_id=PCMR_TAB["cqa"][0])

    def out_ref(key):
        """The attribute's row of @tbl-cqa-outcome: the criterion as its spec type applies it,
        the simulated commercial-scale range and the verdict."""
        return ref(doc, f, f"{doc}_sec_outcome", "Outcome against the acceptance criteria",
                   PCMR_OUT_ROW[key], table_title=PCMR_TAB["outcome"][1],
                   table_id=PCMR_TAB["outcome"][0])

    def viral_ref(step_key):
        """The step's row of @tbl-viral: the log10 credited to it for each model virus."""
        return ref(doc, f, f"{doc}_sec_viral", "The modular claim",
                   PCMR_VC_ROW_FOR[step_key], table_title=PCMR_TAB["viral"][1],
                   table_id=PCMR_TAB["viral"][0])

    for key in P.CFG.train_order:
        title = P.UNIT_OP_TITLES.get(key, P.CFG.unit_op(key).name)
        add("process:amab_ds", "process_has_step", f"step:{key}",
            f"The A-Mab drug-substance process has the step {title}.", [train_ref(key)])
    # attribute -> the step the consolidated register assigns it to, and its acceptance
    # criterion. The register row carries the first relation; the outcome row carries the
    # second, because it is the row that applies the spec type. §3.2 is explicit that the
    # lower figure printed against a one-sided attribute "is not an acceptance limit", so the
    # printed interval must not be asserted as the criterion.
    for r in P.cqa_reg.to_dict("records"):
        key, set_by = r["key"], r["set_by"]
        refs = [cqa_ref(key)]
        if (set_by, key) in PCMR_VC_CREDIT:
            refs.append(viral_ref(set_by))
        add(f"step:{set_by}", "step_has_quality_attribute", f"attr:{key}",
            f"{P.UNIT_OP_TITLES.get(set_by, set_by)} is the step the consolidated register "
            f"names as setting {r['cqa']}, and PCR-{P.CFG.unit_op(set_by).step:03d} is the "
            f"report that characterizes it.", refs)
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{key}_acc",
            f"{r['cqa']} is governed by the criterion "
            f"{P._criterion_str(cap_by_key.loc[key])}, and every simulated commercial batch "
            f"met it.", [out_ref(key)])
    # the modular viral-clearance credit that @tbl-cqa-scope does not carry: the contributing
    # steps that are not the register's "set by" step. The low-pH hold is absent from MVM on
    # purpose — @tbl-viral credits it 0.00 log10, and §6.1 says why.
    for step_key, attr_key in PCMR_VC_CREDIT:
        if (step_key, attr_key) in {(r["set_by"], r["key"]) for r in P.cqa_reg.to_dict("records")}:
            continue
        add(f"step:{step_key}", "step_has_quality_attribute", f"attr:{attr_key}",
            f"{P.UNIT_OP_TITLES.get(step_key, step_key)} carries a named, independent module of "
            f"the cumulative clearance claim for "
            f"{P.cqa_reg[P.cqa_reg.key == attr_key].iloc[0]['cqa']}.", [viral_ref(step_key)])
    # attribute -> the method that measures it, where the @tbl-methods row names the analyte in
    # the method title. The glycan map, turbidity and A280 rows name no single attribute.
    for mid, akey in PCMR_METHOD_ATTR.items():
        add(f"attr:{akey}", "attribute_measured_by_method", f"method:{mid}",
            f"{P.cqa_reg[P.cqa_reg.key == akey].iloc[0]['cqa']} is measured by {mid}, whose "
            f"validated performance this report carries.",
            [ref(doc, f, f"{doc}_sec_analytical", "Analytical control", PCMR_METHOD_ROW[mid],
                 table_title=PCMR_TAB["methods"][1], table_id=PCMR_TAB["methods"][0])])
    # step -> the quality-linked parameters the control strategy must hold inside a design space.
    for r in q_rows:
        add(f"step:{r['key']}", "step_has_parameter", f"param:{r['key']}_{r['pkey']}",
            f"{r['unit_operation']} has quality-linked process parameter {r['parameter']}, "
            f"consolidated here as {r['classification']}.",
            [ref(doc, f, f"{doc}_sec_class", "The classification across the train", r["row"],
                 table_title=PCMR_TAB["cpp"][1], table_id=PCMR_TAB["cpp"][0])])
    # step -> the scale-down system @tbl-equipment names by that unit operation.
    for eq_id, step_key in PCMR_EQUIP_STEP.items():
        add(f"step:{step_key}", "step_uses_equipment", f"equipment:{eq_id}",
            f"{P.UNIT_OP_TITLES.get(step_key, step_key)} is the unit operation the register "
            f"names for scale-down system {eq_id}, which was inside its calibration interval "
            f"when the affected studies ran.",
            [ref(doc, f, f"{doc}_sec_dev_retained", "The retained deviations",
                 PCMR_EQUIP_ROW[eq_id], table_title=PCMR_TAB["equip"][1],
                 table_id=PCMR_TAB["equip"][0])])

    def stx(i, text, sec, quote, *more):
        """A summary statement and the span(s) that attest it.

        ``more`` takes further ``(section, quote)`` pairs. A statement that joins two facts
        needs a span for each; a single quote carrying half of it attests half of it.
        """
        refs = [ref(doc, f, f"{doc}_sec", sec, quote)]
        refs += [ref(doc, f, f"{doc}_sec", s, q) for s, q in more]
        return ReportStatement(statement_id=f"{doc}-S{i:02d}", statement_text=text,
                               confidence="high", review_status="accepted",
                               source_references=refs)
    report_sections = [ReportSection(section_id=f"{doc}-summary", title="Master report summary", statements=[
        stx(1, "PCMR-001 rolls up the per-unit-operation reports PCR-003 to PCR-010 into one "
               "argument and does not repeat their analyses.",
            "The campaign and its documents",
            "It does not repeat their analyses, and where a figure here comes from one of them, "
            "that report is named."),
        stx(2, f"All {n_cqa} drug-substance quality attributes met their acceptance criteria on "
               f"a capability estimate simulated from the fitted step models.",
            "Executive summary",
            f"All {n_cqa} drug substance quality attributes met their acceptance criteria.",
            ("Executive summary",
             f"Capability was estimated by simulating {int(P.V['n_monte_carlo']):,} commercial "
             f"batches, with every parameter varying about its set-point on a spread set by its "
             f"normal operating range")),
        stx(3, f"The lowest capability index in the set is {_N['min_cpk']}, on the cumulative "
               f"MVM clearance.",
            "Executive summary",
            f"The lowest capability index in the set is {_N['min_cpk']}, for cumulative MVM "
            f"clearance"),
        stx(4, "The report sets no acceptance threshold for the capability index; each index is "
               "reported beside the margin between the simulated mean and the governing limit.",
            "Process capability",
            "This report sets no acceptance threshold for the capability index, and each index "
            "is reported with the margin between the simulated mean and the governing limit, "
            "which is the quantity a control decision acts on."),
        stx(5, "Cumulative viral clearance exceeds its requirement for both model viruses, as a "
               "modular claim summed over independently studied steps.",
            "The modular claim",
            "Cumulative viral clearance exceeds its requirement for both model viruses.",
            ("The modular claim",
             "The claim is modular in the sense of ICH Q5A, which means that each step was "
             "spiked and studied independently on a qualified small-scale model and the step "
             "increments are then added")),
        stx(6, "The three credited clearance mechanisms differ, which is what licenses adding "
               "the increments.",
            "Orthogonality, and what is not claimed",
            "Adding the step increments is only defensible if the mechanisms are independent, "
            "and the three mechanisms differ."),
        stx(7, f"Every parameter carried into the campaign is classified: {_N['n_cpp']} "
               f"critical, {_N['n_wc']} well-controlled critical, {_N['n_kpp']} key and "
               f"{_N['n_gpp']} general process parameters.",
            "The classification across the train",
            f"the counts are {_N['n_cpp']} critical process parameter, {_N['n_wc']} "
            f"well-controlled critical process parameters, {_N['n_kpp']} key process parameters "
            f"and {_N['n_gpp']} general process parameters"),
        stx(8, "Exactly one parameter in the campaign is classified as a critical process "
               "parameter: the pH of the low-pH viral inactivation hold.",
            "The exceptions",
            f"The process has {_N['n_cpp']} critical process parameter, the pH of the low-pH "
            f"viral inactivation hold."),
        stx(9, "Host cell protein and residual DNA are formed in the culture and cleared across "
               "three purification steps, so their margin is not a property of any single step.",
            "The attributes and where they are set",
            "Host cell protein and residual DNA are generated in the culture and are cleared by "
            "Protein A capture (PCR-005), cation exchange (PCR-007) and anion exchange "
            "(PCR-008).",
            ("Outcome against the acceptance criteria",
             "The impurity attributes clear their limits by a wide margin, which is a property "
             "of a train in which the capture step and both polishing steps remove them, and "
             "not a property of any single step.")),
        stx(10, f"Cumulative product yield across the train is {_N['yield_pct']}, reported as a "
                f"process-performance attribute that is not an acceptance criterion.",
            "Nominal batch performance",
            f"The cumulative yield is {_N['yield_pct']} and the lowest single-step yield is "
            f"{_N['min_step_yield']}% at the cation exchange step."),
        stx(11, f"{_N['n_dev']} deviations were recorded across the {_N['n_dev_reports']} unit "
                f"operation studies, and one of them invalidated a designed experiment.",
            "Deviations across the campaign",
            f"The campaign recorded {_N['n_dev']} deviations across the {_N['n_dev_reports']} "
            f"unit operation studies, and one of them invalidated a designed experiment."),
        stx(12, f"{_N['n_dev_retained']} deviations were retained, which means the affected data "
                f"were kept in the analysis under an argument that bounds the impact.",
            "The retained deviations",
            f"In {_N['n_dev_retained']} cases the deviation was retained, which means the "
            f"affected data were kept in the analysis with an argument that bounds the impact."),
        stx(13, "One deviation changed the control strategy: the neutralized hold time before "
                "anion exchange loading is now treated as a feed-input control.",
            "Life-cycle and feed-input controls",
            "One feed-input control follows from a deviation.",
            ("Life-cycle and feed-input controls",
             "The time the neutralized cation exchange pool is held before anion exchange "
             "loading is therefore treated as a control input for that step")),
        stx(14, "The report bounds its own claims: the edges of the design space have not been "
                "run at commercial scale.",
            "Conclusions and Stage 2 readiness",
            "they describe the process operating near its set-points, so they say nothing about "
            "the edges of the design space, which have not been run at scale",
            ("Process capability",
             "It describes the process operating near its set-points, so it says nothing about "
             "performance at the edges of the design space, which have not been run at "
             "commercial scale.")),
        stx(15, "Capability is estimated on qualified scale-down models, not measured on "
                "commercial equipment.",
            "Conclusions and Stage 2 readiness",
            "The capability and clearance figures are estimated on qualified scale-down models "
            "and are not measured on commercial equipment"),
        stx(16, "Viral clearance is measured in small-scale spiking studies, not on production "
                "material, and no drug substance test confirms it.",
            "Conclusions and Stage 2 readiness",
            "The viral clearance values come from small-scale spiking studies.",
            ("Orthogonality, and what is not claimed",
             "The log reduction values come from spiking studies on small-scale models and are "
             "not measurements of the commercial process."),
            ("Release testing",
             "viral clearance attributes are not confirmed in that way, because no test on the "
             "drug substance measures them")),
        stx(17, "No design space or proven acceptable range in the package rests on a screening "
                "fit or extends beyond the range its step characterized.",
            "Conclusions and Stage 2 readiness",
            "Nothing here rests on a screening model, and no proven acceptable range extends "
            "beyond the range its step characterized."),
        stx(18, "The report is explicit that it does not qualify the commercial process, which "
                "is what Stage 2 exists to do.",
            "Conclusions and Stage 2 readiness",
            "This report does not qualify the commercial process, and it makes no claim about "
            "the performance of any batch made at commercial scale."),
    ])]
    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_process",
                                  process_steps=pcmr_steps(doc, f)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_cqa",
                                  quality_attributes=pcmr_cqas(doc, f)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_class",
                                  parameters=pcmr_params(doc, f, q_rows)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_analytical",
                                  analytical_methods=pcmr_methods(doc, f)),
        S.SectionEntityExtraction(document_id=doc, section_id=f"{doc}_sec_dev_retained",
                                  equipment=pcmr_equipment(doc, f)),
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
        weak_claims=build_weak_claims(doc, f),
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], version=P.VERSION, effective_date=P.EFFECTIVE_DATE,
        schema_extensions_used=COMMON_EXT + [
            "RhetoricalSpan (new model) — argument-structure roles over the report prose, and "
            "one span per row of the campaign deviation register (no upstream deviation model)",
        ],
        out_of_schema_notes=[
            "Master report rolls up the per-unit-operation reports; entities are the Step 3-10 "
            "process steps, the 10 consolidated drug-substance quality attributes, the 21 "
            "quality-linked parameters @tbl-cpp restates by name, the 8 analytical methods "
            "@tbl-methods reports validated performance for, and the 3 instrumented scale-down "
            "systems @tbl-equipment registers.",
            "Per-record quotes are the RENDERED TABLE ROW (@tbl-train, @tbl-scope, @tbl-yield, "
            "@tbl-cqa-scope, @tbl-cqa-outcome, @tbl-cpp, @tbl-cap, @tbl-viral, @tbl-methods, "
            "@tbl-dev, @tbl-equipment), rebuilt from the same seeded register with the same "
            "floatfmt the document uses, so each span carries both ends of the relation it "
            "anchors rather than a sentence about it. No quote spans a rendered cross-reference "
            "('Table 6', 'Section 4'), whose surrounding whitespace comes from a field code.",
            "ACCEPTANCE CRITERIA ARE THE ONE-SIDED FORM. §3.2 states that for the impurity, "
            "size-variant and charge-variant attributes 'only the upper limit is an acceptance "
            "limit', and that the lower figure printed beside acidic charge variants in "
            "@tbl-cqa-scope 'is not an acceptance limit'. Every acceptance-criterion record is "
            "therefore the criterion @tbl-cqa-outcome renders through the spec type "
            "(<= 5 % HMW (SEC), >= 16.7 log10 (cumulative)); the printed interval is carried "
            "only as a secondary string on the entity, because the register row does render it.",
            "No Tool #1 or Tool #2 criticality score is carried. @tbl-cqa-scope renders the "
            "criticality letter and nothing else, so a score is a value no span in this "
            "document could attest. The scores live in RA-001 and PCMP-001, which render them.",
            "Process capability has no dedicated field: each attribute's Cpk is carried on the "
            "QualityAttribute reference to its @tbl-cap row. The report claims NO numeric "
            "minimum capability index — §5 says it 'sets no acceptance threshold for the "
            "capability index' — so no minimum is asserted here.",
            "Viral clearance is modular: step_has_quality_attribute is asserted for every step "
            "@tbl-viral credits. The low-pH hold is deliberately NOT credited for MVM (0.00 "
            "log10, non-enveloped parvovirus), and no clearance is claimed for Protein A "
            "capture or cation exchange.",
            "Host cell protein and residual DNA are formed in the culture and cleared across "
            "capture and both polishing steps (§3.1). The report makes no claim that any single "
            "step controls them, and none is asserted; the in-process pool values in §2.2 are "
            "nominal-batch figures, not acceptance criteria.",
            "attribute_measured_by_method is asserted only for the 3 @tbl-methods rows whose "
            "method title names one drug substance attribute that is measured on the drug "
            "substance. The glycan map covers three attributes at once; turbidity and A280 are "
            "in that table for the other reason §7.5 gives; and the two infectivity assays are "
            "NOT linked to the cumulative clearance attributes, because §7.4 states that those "
            "attributes 'are not confirmed in that way, because no test on the drug substance "
            "measures them'.",
            "step_uses_equipment is asserted only for the 2 @tbl-equipment rows whose "
            "description names a unit operation. The chromatography chamber names none and "
            "three chromatography steps are in scope, so no step link is claimed for it.",
            "The 17-row campaign deviation register (§8) has no upstream model and is captured "
            "as rhetorical_spans of role 'deviation_disposition', one per register row (15 "
            "retained, 1 invalidated_and_re_executed, 1 corrected_by_modelling_and_verification_"
            "runs), with the §8.1-8.2 narrative as further spans. PCMR-001 carries no "
            "weak_claims.",
        ],
        inventory=inv, entities=entities, report_sections=report_sections,
        assertions=AssertionStore(run_id=f"gt-{doc}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id="gt-pcmr", concepts=pcmr_concepts(q_rows)),
        rhetorical_spans=pcmr_rhetorical_spans(doc, f))


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
            json.dump(annex.model_dump(mode="json"), fh, indent=2, ensure_ascii=False)
        ne = sum(len(s.process_steps) + len(s.parameters) + len(s.quality_attributes)
                 + len(s.analytical_methods) + len(s.equipment) + len(s.sites) for s in annex.entities)
        print(f"wrote {path}: {ne} entities, {len(annex.studies)} studies, "
              f"{len(annex.assertions.assertions)} assertions, "
              f"{len(annex.concepts.concepts)} concepts")
    if BUILD_ERRORS:
        raise SystemExit("\nFAIL  " + str(len(BUILD_ERRORS)) + " annex layer(s) are stale:\n  "
                         + "\n  ".join(BUILD_ERRORS))


if __name__ == "__main__":
    main()
