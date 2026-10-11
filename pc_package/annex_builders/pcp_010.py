"""PCP-010 Version 2.0: Process Characterization Plan, Ultrafiltration / Diafiltration (Step 10).

The protocol amendment issued under INV-001 for the last step of the drug substance train, the one
step with neither a designed experiment nor an intermediate acceptance criterion. Fitted to the
Version 2.0 text. Every table of the plan is a complex table (``T.frame`` or ``T.sop_references``),
read back through ``qmd_ctables`` from the object the plan printed; the related-documents and
title-block tables are the markdown their helpers return. Every number in a quote or a record is read
from the plan's own namespace (``qmd_namespace``) or from the registers in ``_pcpkg``.

The plan prints no criteria-change table and no methods table, so the acceptance criteria are the
ones the plan states in prose and in its tables (the drug substance criteria apply directly, the
buffer-exchange criterion of Version 1.0 is kept, and Version 1.0 of PCR-010 read the acidic charge
variants against their upper limit alone), and each method is anchored on its sentence of
Analytical methods and its row of the procedures table.
"""
from __future__ import annotations

import re

import _pcpkg as P
import schema_ext as S
import build_ground_truth as G
from build_ground_truth import (
    CELL_SEP, COMMON_EXT, METHOD_TYPE, REV2_EXT, STUDY_TYPE, RowQuotes, UFPARAM_CONCEPT, UFUO_NAME,
    _adders, _attr_concepts, _attr_key_by_label, _document_text, _method_concepts, _present,
    _site_entities, _unrendered_note, ctable_rows, md_string_rows, meta, qmd_ctables, qmd_namespace,
    ref, rev2_inventory, rev2_layer,
)

DOC = "PCP-010"
QMD = "PCP-010_ufdf.qmd"
FILE = G.PCP10_FILE                                  # "PCP-010_ufdf.docx"

#: Relationship cell of @tbl-related -> DocumentRelationship.kind (as the other step plans map it).
REL_KIND = {"Rolls up into": "rolls_up_into", "Parent — master plan": "executed_under",
            "Parent — risk basis for study scope": "scoped_by",
            "Parent — transfer scope": "scoped_by"}

#: Concept ids kept from the Version 1.0 builder of this document.
STEP_ID = "step:ufdf"
SDM_ID = "equip:ufdf_sdm"
MEMBRANE_ID = "equip:ufdf_membrane"
SKID_ID = "equip:ufdf_commercial_skid"


# --------------------------------------------------------------------------- #
# Local helpers (candidates for build_ground_truth, named in the report).      #
# --------------------------------------------------------------------------- #
def cells(row):
    """The cells of one rendered row, as ``check_grounding.docx_text`` separates them."""
    return [c.strip() for c in row.split(CELL_SEP)]


def rows_once(rows, text):
    """``{key -> row}`` (+ ``.header``) for the rows of ``rows`` that occur exactly once in the
    rendered ``text``. A continuation row of a merged column can read exactly like another one
    (the three set-point rows of a univariate run table), which makes it an ambiguous reference;
    ``size_variant_refs`` applies the same test to the methods-by-study rows."""
    from check_grounding import normalize
    out = RowQuotes((k, r) for k, r in rows.items() if text.count(normalize(r)) == 1)
    out.header = rows.header
    return out


def build():
    """The ``GroundTruthAnnex`` of PCP-010 Version 2.0."""
    from annex_contract.assertions import AssertionStore
    from annex_contract.concepts import Concept, ConceptStore
    from annex_contract.discourse import DocumentRelationship, ExplicitNonClaim
    from annex_contract.summaries import ReportSection
    doc, f = DOC, FILE
    ns, _ = qmd_namespace(QMD)
    ct = qmd_ctables(QMD)
    A, add, ST, st = _adders(doc, f)
    text = _document_text(f)
    g, w = ns["g"], ns["w"]
    sp, nor, prg = ns["sp"], ns["nor"], ns["prg"]
    prm = ns["P"]                                                   # the plan's {key -> Parameter}
    pdv, ptmp, pconc = ns["pdv"], ns["ptmp"], ns["pconc"]
    INV, AMD, REV1 = ns["INV"], ns["AMD"], ns["REV1"]
    VER, EFF, STEP, UO_TITLE = ns["VER"], ns["EFF"], ns["STEP"], ns["UO_TITLE"]
    TFF, TFF_DUE = ns["TFF"], ns["TFF_DUE"]
    SDM_ST = ns["SDM_ST"]
    ACC_AGG, ACC_AV = ns["ACC_AGG"], ns["ACC_AV"]
    AMV_A280 = next(a for a, t in ns["UFDF_AMV_REFS"] if "A280" in t)

    def sec_id(s):
        return f"{doc}_sec_{s}"

    # ---- the rendered tables, rebuilt from the objects the plan printed ---------------------
    pt, pdf_ = ct["tbl-params"]                                     # T.frame, by parameter name
    prow = ctable_rows(pt, pdf_["Parameter"])
    cq_t, cq_df = ct["tbl-cqa"]                                     # T.frame, by attribute key
    by_label = _attr_key_by_label()
    ckeys = [by_label[n] for n in cq_df["Attribute"]]
    crow = ctable_rows(cq_t, ckeys)
    sop_t, sop_df = ct["tbl-sops"]                                  # T.sop_references, by reference
    soprow = ctable_rows(sop_t, sop_df["Reference"])
    so_t, so_df = ct["tbl-sdm-outputs"]                             # T.frame, by row index
    sorow = ctable_rows(so_t)
    smp_t, _ = ct["tbl-sampling"]                                   # T.frame, by row index
    smprow = ctable_rows(smp_t)
    win_t, win_df = ct["tbl-windows"]                               # T.frame, by study id
    winrow = ctable_rows(win_t, win_df["Study"])
    lev_t, _ = ct["tbl-levels"]                                     # T.frame, by row index
    levrow = rows_once(ctable_rows(lev_t), text)
    rel = md_string_rows(P.related_docs_md(doc))                    # @tbl-related
    rel_cap = "Related documents in the characterization package."  # printed after related_docs_md
    tb = md_string_rows(P.title_block(doc, UO_TITLE))               # the title block, by field
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))
    reg = P.cqa_reg.set_index("key")
    pkey = {p.name: k for k, p in prm.items()}                      # parameter name -> key
    sdm_name = f"bench-scale TFF skid {TFF}"

    # the attribute table names the method of each attribute ("SEC, AMV-3011")
    method_of = {}
    for key, m in zip(ckeys, cq_df["Method"]):
        method_of[key] = re.search(r"AMV-\d+", m).group(0)
    attrs_of = {}
    for key, amv in method_of.items():
        attrs_of.setdefault(amv, []).append(key)

    # the parameter table prints the values the plan states; they must be the namespace's
    for name, row in prow.items():
        p = prm[pkey[name]]
        c = cells(row)                     # Parameter | Unit | Set-point | Range studied | NOR
        want = [name, p.unit, g(sp(p)), f"{g(prg(p)[0])}–{g(prg(p)[1])}",
                f"{g(nor(p)[0])}–{g(nor(p)[1])}"]
        if c != want:
            raise ValueError(f"{pt.label}: row {c} does not read {want}")

    # ---- entities ------------------------------------------------------------------------
    purpose, prior = "Purpose and scope", "Unit-operation description and prior knowledge"
    sdm_sec, factors = "Scale-down model and its qualification", "Factors, ranges and study type"
    q_purpose = ("This plan defines the process characterization studies for the ultrafiltration "
                 "and diafiltration (UF/DF) step of the A-Mab drug substance process.")
    q_last = (f"UF/DF is Step {STEP}, the last step of the drug substance train, and it delivers the "
              f"drug substance at its target concentration of {g(sp(pconc))} g/L.")
    q_what = ("The UF/DF step concentrates the antibody and exchanges the process buffer for the "
              "formulation buffer.")
    q_receives = "The step receives the filtrate pool of the small virus retentive filtration step."
    step = S.ProcessStep(
        step_id=STEP_ID, step_name=UFUO_NAME, step_number=str(STEP), unit_operation=UFUO_NAME,
        description=f"The last step of the drug substance train. Ultrafiltration across a tangential "
                    f"flow membrane concentrates the antibody, diafiltration at constant volume "
                    f"exchanges the process buffer for the formulation buffer, and a second "
                    f"concentration brings the drug substance to its target of {g(sp(pconc))} g/L "
                    f"before a buffer flush recovers the retentate. The step can add to aggregate "
                    f"and to the acidic charge variants.",
        input_materials=["filtrate pool of the small virus retentive filtration step"],
        output_materials=[f"A-Mab drug substance in the formulation buffer at {g(sp(pconc))} g/L"],
        equipment=["commercial UF/DF skid", "tangential flow membrane", sdm_name],
        source_references=[ref(doc, f, sec_id("purpose"), purpose, q_purpose),
                           ref(doc, f, sec_id("purpose"), purpose, q_last),
                           ref(doc, f, sec_id("uo"), prior, q_what),
                           ref(doc, f, sec_id("operation"), "Operation", q_receives)],
        metadata=meta())
    q_sdm = (f"The studies are run on the bench-scale skid {TFF}, registered as the "
             f"{ns['TFF_DESC']} and held under calibration and change control.")
    q_cal = f"on the skid {TFF}, whose next calibration was due on {TFF_DUE}"
    q_membrane = ("Both operations run across a tangential flow membrane whose pores pass buffer "
                  "salts and retain the antibody.")
    q_same = ("The membrane chemistry, the nominal molecular weight cut-off and the feed channel "
              "geometry are those of the commercial skid.")
    q_obj_i = ("To estimate the offsets of a bench-scale tangential flow filtration (TFF) model of the "
               "commercial skid from manufacturing scale, as the basis of its qualification "
               "(PCMP-001 §7.1).")
    roles_t, roles_df = ct["tbl-roles"]
    rolerow = ctable_rows(roles_t, roles_df["Function"])
    q_receiving = rolerow["Process science at the receiving site"]
    equipment = [
        S.Equipment(
            equipment_id=SDM_ID, equipment_name=sdm_name,
            equipment_type="tangential flow filtration skid (scale-down model)",
            site_name=P.SENDING_SITE,
            source_references=[ref(doc, f, sec_id("sdm"), sdm_sec, q_sdm),
                               ref(doc, f, sec_id("schedule"), "Deliverables and schedule", q_cal)],
            metadata=meta()),
        S.Equipment(
            equipment_id=MEMBRANE_ID, equipment_name="tangential flow membrane",
            equipment_type="ultrafiltration membrane (tangential flow filtration)",
            source_references=[ref(doc, f, sec_id("uo"), prior, q_membrane),
                               ref(doc, f, sec_id("sdm"), sdm_sec, q_same)],
            metadata=meta()),
        S.Equipment(
            equipment_id=SKID_ID, equipment_name="commercial UF/DF skid",
            equipment_type="tangential flow filtration skid (manufacturing scale)",
            site_name=P.RECEIVING_SITE,
            source_references=[ref(doc, f, sec_id("objectives"), "Objectives", q_obj_i),
                               ref(doc, f, sec_id("roles"), "Roles and responsibilities",
                                   q_receiving, table_title=roles_t.caption,
                                   table_id=f"{doc}_tab_roles", table_header=rolerow.header)],
            metadata=meta()),
    ]
    # the per-parameter sentence of §6.1 that states the range studied against the NOR
    lead = {"diavolumes": "The number of diavolumes", "tmp": "The TMP",
            "final_conc": "The final DS concentration"}
    q_range = {k: f"{lead[k]} is studied from {g(prg(p)[0])} to {g(prg(p)[1])} {p.unit} against a "
                  f"NOR of {g(nor(p)[0])} to {g(nor(p)[1])} {p.unit}" for k, p in prm.items()}
    params = []
    for name, row in prow.items():
        p = prm[pkey[name]]
        params.append(S.ProcessParameter(
            parameter_id=UFPARAM_CONCEPT[name], parameter_name=name, parameter_type="unclassified",
            unit=p.unit, target_value=f"{g(sp(p))} {p.unit}",
            NOR=f"{g(nor(p)[0])}–{g(nor(p)[1])} {p.unit}",
            PAR=f"{g(prg(p)[0])}–{g(prg(p)[1])} {p.unit}",
            associated_step=UO_TITLE, study_type=p.study,
            source_references=[ref(doc, f, sec_id("factors"), factors, row, table_title=pt.caption,
                                   table_id=f"{doc}_tab_params", table_header=prow.header),
                               ref(doc, f, sec_id("factors"), factors, q_range[pkey[name]])],
            metadata=meta()))
    attrs = []
    for i, key in enumerate(ckeys):
        r = reg.loc[key]
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=r["cqa"], attribute_type="CQA",
            unit=r["unit"], acceptance_criteria=[f"{cq_df['Criterion'].iloc[i]} (drug substance)"],
            analytical_method=method_of[key], associated_steps=[UO_TITLE],
            rationale_for_criticality=f"A-Mab Tool #1 score = impact on safety and efficacy × "
                                      f"uncertainty of that impact = {cq_df['Tool #1 score'].iloc[i]}.",
            criticality_level=cq_df["Criticality"].iloc[i],
            tool1_score=int(cq_df["Tool #1 score"].iloc[i]), tool2_severity=int(r["tool2_severity"]),
            source_references=[ref(doc, f, sec_id("cqa"), "Quality attributes in scope", crow[key],
                                   table_title=cq_t.caption, table_id=f"{doc}_tab_cqa",
                                   table_header=crow.header)],
            metadata=meta()))
    # the sentence of Analytical methods that names each method
    q_method = {
        ns["AMV_SEC"]: (f"Aggregate is measured by size exclusion chromatography (SEC) under "
                        f"{ns['AMV_SEC']} and reported as the percentage of HMW species."),
        AMV_A280: f"Protein concentration is measured by ultraviolet absorbance (A280) under {AMV_A280}.",
        ns["AMV_ICIEF"]: (f"Charge variants are measured by imaged capillary isoelectric focusing "
                          f"(icIEF) under {ns['AMV_ICIEF']} and reported as the percentage of acidic "
                          f"species."),
    }
    analyte = {ns["AMV_SEC"]: names["aggregates_hmw"], ns["AMV_ICIEF"]: names["acidic_variants"],
               AMV_A280: "protein concentration"}
    methods = []
    for amv, title in ns["UFDF_AMV_REFS"]:
        keys = attrs_of.get(amv, [])
        methods.append(S.AnalyticalMethod(
            method_id=amv, method_name=title, method_type=METHOD_TYPE.get(amv),
            analytes=[analyte[amv]], associated_attributes=[f"attr:{k}" for k in keys],
            validation_status="validated",
            source_references=[ref(doc, f, sec_id("analytical"), "Analytical methods", q_method[amv]),
                               ref(doc, f, sec_id("related"), "Related documents", soprow[amv],
                                   table_title=sop_t.caption, table_id=f"{doc}_tab_sops",
                                   table_header=soprow.header)]
            + [ref(doc, f, sec_id("cqa"), "Quality attributes in scope", crow[k],
                   table_title=cq_t.caption, table_id=f"{doc}_tab_cqa", table_header=crow.header)
               for k in keys],
            metadata=meta()))

    # ---- explicit non-claims ---------------------------------------------------------------
    nc, nc_at = [], {}

    def nclaim(sec, subject, statement, title, quotes, rationale=None, elsewhere=None):
        nc.append(ExplicitNonClaim(
            non_claim_id=f"{doc}-NC{len(nc) + 1:02d}", subject=subject, unit_operation=UFUO_NAME,
            statement=statement, rationale=rationale, handled_elsewhere=elsewhere,
            source_references=[ref(doc, f, sec_id(s), t, q) for s, t, q in
                               ([(sec, title, quotes)] if isinstance(quotes, str) else quotes)],
            metadata=meta()))
        nc_at.setdefault(sec, []).append(nc[-1])

    cqa_sec = "Quality attributes in scope"
    nclaim("purpose", "drug product manufacture and formulation development",
           "Drug product manufacture and the development of the formulation are out of scope; the "
           "studies treat the composition of the formulation buffer as a constant.", purpose,
           [("purpose", purpose, "Drug product manufacture and the development of the formulation "
                                 "belong to the drug product program and are out of scope."),
            ("purpose", purpose, "That program fixes the composition of the formulation buffer, and "
                                 "the studies treat it as a constant.")],
           elsewhere="the drug product program")
    nclaim("purpose", "viral clearance", "No viral clearance is claimed for the UF/DF step.", purpose,
           [("purpose", purpose, "No viral clearance is claimed for this step."),
            ("cqa", cqa_sec, f"Viral clearance is credited to the {ns['CLAIMS_TXT']} steps, and the "
                             f"cumulative claim is consolidated in the master report PCMR-001")],
           elsewhere=f"the {ns['CLAIMS_TXT']} steps; the cumulative claim is consolidated in PCMR-001")
    nclaim("purpose", "glycan variants", "The step does not change the glycan variants of A-Mab, and "
           "they are not measured across it.", purpose,
           [("purpose", purpose, "The step does not change the glycan variants of A-Mab"),
            ("cqa", cqa_sec, "The membrane retains every glycoform of the antibody, so the step "
                             "cannot change their distribution.")],
           rationale="The membrane retains every glycoform of the antibody, so the step cannot change "
                     "their distribution.")
    nclaim("purpose", "clearance of host cell protein, residual DNA and leached Protein A",
           "No clearance of host cell protein, DNA or leached Protein A is credited to the step, and "
           "none of them is measured across it.", purpose,
           [("purpose", purpose, "no clearance of host cell protein, DNA or leached Protein A is "
                                 "credited to it"),
            ("cqa", cqa_sec, "Host cell protein, residual DNA and leached Protein A are cleared by the "
                             "chromatography steps before this one."),
            ("cqa", cqa_sec, "Table 7.1 of the master plan PCMP-001 credits this step with no clearance "
                             "of host cell protein or leached Protein A, and residual DNA is judged on "
                             "the drug substance only (PCMP-001 §7.3).")],
           elsewhere="the chromatography steps before UF/DF")
    nclaim("changes", "studies made after Version 1.0", "The amendment describes only the studies "
           "that Version 1.0 planned; work the plan did not foresee is recorded in PCR-010 as a "
           "discrepancy from the plan.", "Changes in this revision",
           [("changes", "Changes in this revision",
             "This document is that amendment of PCP-010, issued after the studies it governs were "
             "run, and it describes only the studies that Version 1.0 planned."),
            ("approvals", "Approvals", "Work that the plan did not foresee, and that departs from no "
                                       "approved procedure, is recorded in PCR-010 as a discrepancy "
                                       "from this plan.")],
           elsewhere="PCR-010, as discrepancies from this plan")
    nclaim("cqa", "fragments", "Fragments are not measured in the studies of the step, a scope kept "
           "from Version 1.0.", cqa_sec,
           [("cqa", cqa_sec, "Fragments are not measured either."),
            ("cqa", cqa_sec, "Version 1.0 left fragments out of the studies of this step, and this "
                             "amendment keeps that scope."),
            ("changes", "Changes in this revision",
             "The studies of this step do not measure fragments, a scope kept from Version 1.0")],
           rationale="PCMP-001 assumes that the step does not change fragments (PCMP-001 Table 7.1); "
                     "the step adds no protease and its physical route aggregates the antibody "
                     "without cleaving it, although hinge hydrolysis continues on the skid.",
           elsewhere="release testing of the drug substance for fragments")
    nclaim("risk", "interaction between the TMP and the final DS concentration",
           "The univariate design cannot resolve a possible interaction between the TMP and the final "
           "DS concentration.", "Risk-based prioritization of parameters",
           "A study that varies one factor at a time cannot resolve such an interaction.")
    nclaim("risk", "threshold for an attribute that approaches its criterion",
           "The plan sets no threshold for when a measured attribute approaches its criterion at an "
           "edge.", "Risk-based prioritization of parameters",
           "The threshold for “approaches” is left to the report PCR-010, because Version 1.0 set none.",
           elsewhere="PCR-010")
    nclaim("sdm", "offsets of the acidic charge variants and the buffer exchange",
           "The acidic charge variants and the buffer exchange are not compared at both scales, so "
           "their offsets are unknown and they are judged as the scale-down model measures them.",
           sdm_sec, "The qualification does not compare them at both scales, so their offsets are "
                    "unknown, and both are judged as the scale-down model measures them (PCMP-001 §7.1).")
    # ... and on the rows of the qualification-output table that say so
    both_col = next(c for c in so_df.columns if c.startswith("Compared"))
    not_compared = [i for i, v in enumerate(so_df[both_col]) if v != "Yes"]
    nc[-1].source_references.extend(
        ref(doc, f, sec_id("sdm"), sdm_sec, sorow[i], table_title=so_t.caption,
            table_id=f"{doc}_tab_sdm_outputs", table_header=sorow.header) for i in not_compared)
    nclaim("analytical", "validated assays for conductivity and pH",
           "The conductivity and pH readings that follow the buffer exchange are in-process readings "
           "from the skid instrumentation, not validated assays.", "Analytical methods",
           "These are in-process readings from the skid instrumentation, not validated assays.")
    nclaim("stats", "response-surface model", "No response-surface model will be fitted for the step.",
           "Statistical methods",
           "No response-surface model will be fitted for this step, because the design carries no "
           "factorial structure and no interaction term can be estimated from it.")
    nclaim("stats", "model-adequacy criteria", "The model-adequacy criteria of PCMP-001 §7.2 do not "
           "apply to the step.", "Statistical methods",
           "The model-adequacy criteria of PCMP-001 §7.2 apply to response-surface models and "
           "therefore do not apply here.")
    nclaim("factors", "characterization beyond the ranges studied", "The step will not be "
           "characterized outside the ranges studied, and no range wider than a range studied will be "
           "proposed.", factors,
           "The step will not be characterized outside these ranges, and no range wider than the range "
           "studied will be proposed in the report PCR-010.")
    nclaim("factors", "number of diavolumes below the lower edge of the NOR", "The study does not go "
           "below the lower edge of the diavolume NOR.", factors,
           "Below that edge the buffer exchange would be less complete, and the study does not go there.",
           rationale="Below that edge the buffer exchange would be less complete.")
    nclaim("factors", "TMP below the NOR", "The study does not characterize the TMP below the NOR.",
           factors,
           "A lower TMP would lengthen the operation, and with it the passes through the pump and the "
           "time for deamidation, and the study does not characterize that side beyond the NOR.")
    nclaim("crit_sdm", "rule for the qualification decision", "The plan sets no rule for the "
           "scale-down qualification decision, because the step has no response-surface model.",
           "Scale-down model",
           [("crit_sdm", "Scale-down model",
             "This step has no response-surface model, so the qualification decision cannot be made "
             "as PCMP-001 states it, and this plan sets no rule for it."),
            ("crit_sdm", "Scale-down model", "The report PCR-010 states the approach it takes.")],
           elsewhere="PCR-010")
    nclaim("crit_pq", "intermediate acceptance criterion", "PCMP-001 defines no intermediate "
           "acceptance criterion for the step, and the drug substance criteria apply directly.",
           "Product quality",
           "No step follows this one, so PCMP-001 Table 7.1 defines no IAC for it, and the drug "
           "substance criteria apply directly (PCMP-001 §7.6).",
           rationale="No step follows UF/DF.")
    nclaim("crit_pq", "verification of platform worst cases", "No verification of platform worst "
           "cases is planned at the step.", "Product quality",
           "The verification of platform worst cases in PCMP-001 §7.5 uses the response-surface model "
           "of a step, and no verification is planned at this step.")
    nclaim("crit_pq", "analysis of the pH and tolerance of the plateau", "The plan sets no analysis "
           "for the pH of the buffer exchange and no numerical tolerance for the plateau.",
           "Product quality",
           "Version 1.0 set no analysis for the pH and no numerical tolerance for the plateau, so the "
           "report PCR-010 states its approach to both.", elsewhere="PCR-010")
    nclaim("rules", "threshold for a small change", "Neither the plan nor PCMP-001 sets a threshold "
           "for a change that is small against the criterion.", "Decision rules",
           "The threshold for a change that is small against the criterion is left to PCR-010, because "
           "neither Version 1.0 nor PCMP-001 sets one.", elsewhere="PCR-010")
    nclaim("class", "parameter classes", "The plan assigns no parameter class; classification is an "
           "outcome of the studies.", "Classification",
           "The classification is an outcome of the studies and is reported in PCR-010.",
           elsewhere="PCR-010 (under SOP-4001)")
    nclaim("class", "numerical thresholds for a small effect or a wide PAR", "PCMP-001 and SOP-4001 "
           "set no numerical threshold for a small effect or a wide PAR.", "Classification",
           "PCMP-001 and SOP-4001 set no numerical threshold for a small effect or a wide PAR, so the "
           "report PCR-010 states the size of each effect across the PAR and the margin of the PAR to "
           "the NOR, and classifies on them.", elsewhere="PCR-010")
    nclaim("par", "NOR-propagated analysis", "The NOR-propagated analysis of PCMP-001 §6.4 is not "
           "performed for the step.", "Proven acceptable ranges (planned analysis)",
           "This step has no such model, so that analysis is not performed.",
           rationale="The analysis predicts the response from a fitted multivariate model, and the step "
                     "has none.")
    nclaim("par", "univariate PAR at combined range edges", "A univariate PAR does not describe the "
           "step when two parameters sit at their range edges at the same time.",
           "Proven acceptable ranges (planned analysis)",
           "It does not describe the step when two parameters sit at their range edges at the same time.")

    # ---- document relationships ------------------------------------------------------------
    rels = []

    def relation(kind, target, statement, sec, title, quote, header=None, table_title=None,
                 table_id=None):
        rels.append(DocumentRelationship(
            relationship_id=f"{doc}-R{len(rels) + 1:02d}", kind=kind, source_document_id=doc,
            target_document_ref=target, statement=statement,
            source_references=[ref(doc, f, sec_id(sec), title, quote, table_title=table_title,
                                   table_id=table_id, table_header=header)],
            metadata=meta()))
    for target, row in rel.items():
        txt = cells(row)[-1]
        relation(REL_KIND.get(txt, "references"), target, txt, "related", "Related documents", row,
                 rel.header, rel_cap, f"{doc}_tab_related")
    relation("supersedes", f"{doc} Version {REV1['rev']}", "Version 2.0 supersedes Version 1.0 of the "
             "plan.", "title", "Title block", tb["Supersedes"], tb.header)
    q_amd = (f"PCMP-001 Version 2.0 sets non-reduced CE-SDS (nrCE-SDS) as the method for fragments "
             f"wherever a study measures them, following the analytical method decision {AMD['id']} "
             f"of {AMD['date']} (PCMP-001 §7.8).")
    relation("references", AMD["id"], "The analytical method decision that made nrCE-SDS the method "
             "for fragments; the studies of this step do not measure fragments.", "changes",
             "Changes in this revision", q_amd)

    entities = [
        S.SectionEntityExtraction(document_id=doc, section_id=sec_id("purpose"),
                                  process_steps=[step], sites=_site_entities(doc, f, sec_id("purpose")),
                                  non_claims=nc_at["purpose"]),
        S.SectionEntityExtraction(document_id=doc, section_id=sec_id("changes"),
                                  non_claims=nc_at["changes"]),
        S.SectionEntityExtraction(document_id=doc, section_id=sec_id("objectives"),
                                  equipment=[equipment[2]]),
        S.SectionEntityExtraction(document_id=doc, section_id=sec_id("related"),
                                  document_relationships=rels),
        S.SectionEntityExtraction(document_id=doc, section_id=sec_id("uo"), equipment=[equipment[1]]),
        S.SectionEntityExtraction(document_id=doc, section_id=sec_id("cqa"), quality_attributes=attrs,
                                  non_claims=nc_at["cqa"]),
        S.SectionEntityExtraction(document_id=doc, section_id=sec_id("risk"), non_claims=nc_at["risk"]),
        S.SectionEntityExtraction(document_id=doc, section_id=sec_id("sdm"), equipment=[equipment[0]],
                                  non_claims=nc_at["sdm"]),
        S.SectionEntityExtraction(document_id=doc, section_id=sec_id("analytical"),
                                  analytical_methods=methods, non_claims=nc_at["analytical"]),
        S.SectionEntityExtraction(document_id=doc, section_id=sec_id("stats"),
                                  non_claims=nc_at["stats"]),
        S.SectionEntityExtraction(document_id=doc, section_id=sec_id("factors"), parameters=params,
                                  non_claims=nc_at["factors"]),
        S.SectionEntityExtraction(document_id=doc, section_id=sec_id("crit_sdm"),
                                  non_claims=nc_at["crit_sdm"]),
        S.SectionEntityExtraction(document_id=doc, section_id=sec_id("crit_pq"),
                                  non_claims=nc_at["crit_pq"]),
        S.SectionEntityExtraction(document_id=doc, section_id=sec_id("rules"),
                                  non_claims=nc_at["rules"]),
        S.SectionEntityExtraction(document_id=doc, section_id=sec_id("class"),
                                  non_claims=nc_at["class"]),
        S.SectionEntityExtraction(document_id=doc, section_id=sec_id("par"), non_claims=nc_at["par"]),
    ]

    # ---- studies: each on its own row of the execution-window table, plus its design -------
    compared = list(so_df.loc[so_df[both_col] == "Yes", "Output"])
    buffer_out = next(o for o in so_df["Output"] if o.startswith("Buffer exchange"))
    q_qual = (f"The qualification runs are made under SOP-1001, in study {SDM_ST.id}, where "
              f"{w(ns['N_SDM'])} runs at the set-point condition are compared with the pilot and "
              f"commercial record of the step on the step yield, the permeate flux at the set-point "
              f"TMP, the final concentration achieved and the change in aggregate content across the "
              f"step.")
    q_levels = (f"Each parameter is run at {w(ns['n_lev'])} levels, the two edges of its range studied "
                f"and its set-point, with the other {w(ns['n_par'] - 1)} parameters held at their "
                f"set-points.")
    q_runs = (f"The set-point condition is common to the {w(ns['n_par'])} series, so the study "
              f"consists of {w(ns['n_edge'])} edge runs and {w(ns['n_sp'])} replicates of the set-point "
              f"condition, {w(ns['n_runs'])} runs in all.")
    design = {
        # no n_runs or n_center_points on either study (tests/test_config.py matches them against
        # the designed experiments): the qualification compares scale-down runs with manufacturing
        # batches, and the univariate set-point replicates are not centre points of the ranges
        "qualification": dict(responses=compared,
                              refs=[("sdm", sdm_sec, q_qual)]),
        "univariate": dict(design_name="one factor at a time: each parameter at the two edges of its "
                                       "range studied and at its set-point, the other parameters at "
                                       "their set-points; the set-point condition is common to the "
                                       "series and replicated",
                           factors=[p.name for p in prm.values()],
                           responses=[names[k] for k in ckeys] + [buffer_out],
                           refs=[("univariate", "Univariate assessment", q_levels),
                                 ("univariate", "Univariate assessment", q_runs)]),
    }
    studies, unrendered = [], []
    for r in ns["plan_st"].itertuples():
        stype = STUDY_TYPE.get(r.kind)
        if stype is None:
            continue
        if not _present(winrow[r.id], text):
            unrendered.append(r.id)
            continue
        d = dict(design[r.kind])
        refs = [ref(doc, f, sec_id("schedule"), "Deliverables and schedule", winrow[r.id],
                    table_title=win_t.caption, table_id=f"{doc}_tab_windows",
                    table_header=winrow.header)]
        refs += [ref(doc, f, sec_id(s), t, q) for s, t, q in d.pop("refs")]
        if r.kind == "qualification":          # the outputs it compares at both scales
            refs += [ref(doc, f, sec_id("sdm"), sdm_sec, sorow[i], table_title=so_t.caption,
                         table_id=f"{doc}_tab_sdm_outputs", table_header=sorow.header)
                     for i in sorow if i not in not_compared]
        if r.kind == "univariate":             # its planned runs and its sampling points
            refs += [ref(doc, f, sec_id("appA"), "Appendix A. Planned univariate runs", q,
                         table_title=lev_t.caption, table_id=f"{doc}_tab_levels",
                         table_header=levrow.header) for q in levrow.values()]
            refs += [ref(doc, f, sec_id("sampling"), "Sampling plan", q, table_title=smp_t.caption,
                         table_id=f"{doc}_tab_sampling", table_header=smprow.header)
                     for q in smprow.values()]
        studies.append(S.StudyDesign(
            study_id=f"study:{r.id}", study_type=stype, unit_operation=UFUO_NAME,
            scale_down_model=sdm_name,
            associated_parameters=[UFPARAM_CONCEPT[x] for x in d.get("factors", [])],
            source_references=refs, metadata=meta(), **d))

    # ---- assertions ------------------------------------------------------------------------
    add(STEP_ID, "step_uses_equipment", SDM_ID,
        f"The characterization studies of the UF/DF step are run on the bench-scale skid {TFF}, the "
        f"scale-down model of the commercial skid.", sdm_sec, q_sdm)
    add(STEP_ID, "step_uses_equipment", MEMBRANE_ID,
        "The UF/DF step runs across a tangential flow membrane that passes buffer salts and retains "
        "the antibody.", prior, q_membrane)
    add(STEP_ID, "step_uses_equipment", SKID_ID,
        "The UF/DF step is run at manufacturing scale on the commercial skid, of which the bench-scale "
        "skid is the model.", "Objectives", q_obj_i)
    for name, row in prow.items():
        add(STEP_ID, "step_has_parameter", UFPARAM_CONCEPT[name],
            f"{UFUO_NAME} has process parameter {name}.", factors, row, prow.header, pt.caption)
    role = {"aggregates_hmw": "can add to {n}, the attribute most at risk at the step, from the high "
                              "antibody concentration at the membrane wall and from interfaces and "
                              "cavitation in the pump",
            "acidic_variants": "can add to {n}, because deamidation continues while the antibody is in "
                               "solution on the skid"}
    for key in ckeys:
        add(STEP_ID, "step_has_quality_attribute", f"attr:{key}",
            f"{UFUO_NAME} " + role[key].format(n=names[key]) + ".", cqa_sec, crow[key], crow.header,
            cq_t.caption)
    for amv, keys in attrs_of.items():
        for key in keys:
            add(f"attr:{key}", "attribute_measured_by_method", f"method:{amv}",
                f"{names[key]} is measured by {amv} ({dict(ns['UFDF_AMV_REFS'])[amv]}) on the load "
                f"pool and on the final retentate of every run.", "Analytical methods", q_method[amv])
    for i, key in enumerate(ckeys):
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:ufdf_{key}_ds",
            f"At the UF/DF step, {names[key]} in the final retentate of each run is judged against the "
            f"drug substance criterion {cq_df['Criterion'].iloc[i]}; PCMP-001 defines no intermediate "
            f"acceptance criterion for the step.", cqa_sec, crow[key], crow.header, cq_t.caption)
    pc = {k: UFPARAM_CONCEPT[p.name] for k, p in prm.items()}
    q_agg = ("On that basis the risk of aggregate formation is expected to rise with the final "
             "concentration, with the TMP and with the number of passes through the pump.")
    add(pc["final_conc"], "parameter_impacts_attribute", "attr:aggregates_hmw",
        "The risk of aggregate formation is expected to rise with the final DS concentration.", prior,
        q_agg)
    add(pc["tmp"], "parameter_impacts_attribute", "attr:aggregates_hmw",
        "The risk of aggregate formation is expected to rise with the TMP.", prior, q_agg)
    q_long = ("The operation lasts longer with more diavolumes, with a higher final concentration, "
              "which lowers the flux, and with a lower TMP below the flux limit.")
    q_deam = "The increase grows with the time in solution, at a rate that rises with pH and temperature."
    for k, how in (("diavolumes", "More diavolumes lengthen"),
                   ("final_conc", "A higher final DS concentration lowers the flux and lengthens"),
                   ("tmp", "A lower TMP below the flux limit lengthens")):
        add(pc[k], "parameter_impacts_attribute", "attr:acidic_variants",
            f"{how} the operation, and the increase in acidic charge variants by deamidation grows "
            f"with the time in solution.", prior, q_long)
        A[-1].source_references.append(ref(doc, f, f"{doc}_sec", prior, q_deam))

    # ---- report sections -------------------------------------------------------------------
    # The decisions, criteria and design of the plan, one statement per sentence that states them.
    # The rows of the qualification-output and sampling tables are anchored on the records they
    # attest (the studies and the offset non-claim), not restated here.
    chg = "Changes in this revision"
    risk = "Risk-based prioritization of parameters"
    stats = "Statistical methods"
    pq = "Product quality"
    par = "Proven acceptable ranges (planned analysis)"
    sched = "Deliverables and schedule"
    risks = "Risks and assumptions"

    def also(quote, sec):
        """A second anchor for the statement just made, when it joins two adjacent sentences."""
        ST[-1].source_references.append(ref(doc, f, f"{doc}_sec", sec, quote))

    st("PCP-010 defines the process characterization studies for the UF/DF step of the A-Mab drug "
       "substance process.", purpose, q_purpose)
    st(f"UF/DF is Step {STEP}, the last step of the drug substance train, and delivers the drug "
       f"substance at its target concentration of {g(sp(pconc))} g/L.", purpose, q_last)
    st(f"The process is being transferred from the development site in {ns['SENDING_LOCATION']} to the "
       f"commercial drug substance site in {ns['RECEIVING_LOCATION']}.", purpose,
       f"The process is being transferred from the development site in {ns['SENDING_LOCATION']} to the "
       f"commercial drug substance site in {ns['RECEIVING_LOCATION']}.")
    st(f"Version 1.0 of the plan was approved on {ns['V1_APPR']}, before the first study of the step "
       f"began on {ns['FIRST_START']}.", chg,
       f"Version 1.0 of this plan was approved on {ns['V1_APPR']}, before the first study of the step "
       f"began on {ns['FIRST_START']}.")
    st(f"Version {VER} is issued under the QA investigation {INV['id']}, which concerned the acceptance "
       f"criteria of the PAR analysis.", chg,
       f"Version {VER} is issued under the QA investigation {INV['id']}, which concerned the acceptance "
       f"criteria of the PAR analysis.")
    st(f"QA opened {INV['id']} on {INV['opened']}, after its review of PCMR-001 Version 1.0 for BLA "
       f"readiness, and closed it on {INV['closed']}.", chg,
       f"QA opened {INV['id']} on {INV['opened']}, after its review of the master report PCMR-001 "
       f"Version 1.0 for BLA readiness, and closed it on {INV['closed']}.")
    st(f"{INV['id']} found that the criteria used to judge each step in the PAR analysis had been set "
       f"after the data were seen, and that no approved plan contained them.", chg,
       f"The investigation found that the criteria used to judge each step in the PAR analysis had "
       f"been set after the data were seen, and that no approved plan contained them ({INV['id']} "
       f"finding 1).")
    st("As corrective actions, PCMP-001 was reissued as Version 2.0 with acceptance criteria derived a "
       "priori (CA1), and each step plan was amended with those criteria and with the method for "
       "fragments (CA2).", chg,
       f"As corrective actions, the master plan PCMP-001 was reissued as Version 2.0 with acceptance "
       f"criteria derived a priori ({INV['id']} corrective action CA1), and each step plan was amended "
       f"with those criteria and with the method for fragments (corrective action CA2).")
    st("The design, the ranges, the levels and the sampling points of Version 1.0 are unchanged, and so "
       "are its decision rules except where the list of changes says otherwise.", chg,
       "The design, the ranges, the levels and the sampling points of Version 1.0 are unchanged, and "
       "so are its decision rules except where the list below says otherwise.")
    st(f"The criteria for aggregate (at most {g(ACC_AGG[1])} % HMW) and for the acidic charge variants "
       f"({g(ACC_AV[0])} to {g(ACC_AV[1])} %) are the drug substance criteria, on the basis of PCMP-001 "
       f"Version 2.0.", chg,
       f"The criteria for aggregate, at most {g(ACC_AGG[1])} % high molecular weight species (HMW), and "
       f"for the acidic charge variants, {g(ACC_AV[0])} to {g(ACC_AV[1])} %, are the drug substance "
       f"criteria, on the basis of PCMP-001 Version 2.0")
    st("Version 1.0 of the plan stated the same criteria.", chg,
       "Version 1.0 of this plan stated the same criteria.")
    q_v1_av = (f"At analysis, however, the Version 1.0 report PCR-010 read the acidic charge variants "
               f"against their upper limit of {ns['V1_AV_HI']} % alone (INV-001 finding 4).")
    st(f"At analysis, the Version 1.0 report PCR-010 read the acidic charge variants against their "
       f"upper limit of {ns['V1_AV_HI']} % alone (INV-001 finding 4).", chg, q_v1_av)
    st("The plan keeps the two-sided criterion for the acidic charge variants, and PCR-010 records the "
       "departure.", chg, "This plan keeps the two-sided criterion, and PCR-010 records the departure.")
    st("The rule of Version 1.0 for the scale-down model is replaced by the offset rule of PCMP-001 "
       "§7.1.", chg,
       "The rule of Version 1.0 for the scale-down model is replaced by the offset rule of PCMP-001 §7.1")
    st("Aggregate and the acidic charge variants are each judged on single runs and not on a mean, as "
       "PCMP-001 §6.2 requires for a quality attribute.", chg,
       "Each is judged on single runs and not on a mean, as PCMP-001 §6.2 requires for a quality "
       "attribute")
    st(f"PCMP-001 Version 2.0 sets nrCE-SDS as the method for fragments wherever a study measures them, "
       f"following {AMD['id']} of {AMD['date']}.", chg, q_amd)
    st("The execution window of each study and the calibration status of its skid are given, which "
       "answers INV-001 finding 5.", chg,
       "This answers INV-001 finding 5, that the Version 1.0 records gave no execution dates and the "
       "equipment tables therefore appeared to cite expired calibrations.")
    st(f"The title block of Version 1.0 carried {REV1['effective']}, the date on which the Version 1.0 "
       f"reports were approved.", chg,
       f"The title block of Version 1.0 carried {REV1['effective']}, the date on which the Version 1.0 "
       f"reports were approved.")
    st("Under PCMP-001 §6.2 an attribute is called affected by a parameter when a term that contains "
       "the parameter is significant; the rule is added to the classification.", chg,
       "an attribute is called affected by a parameter when a term that contains the parameter is "
       "significant at that level")
    also("Two rules of PCMP-001 Version 2.0 are added to the classification", chg)
    st("Under PCMP-001 §7.7 a significant effect that is too small to move the attribute appreciably "
       "within the PAR does not by itself make a parameter critical; the rule is added to the "
       "classification.", chg,
       "a significant effect that is too small to move the attribute appreciably within the PAR does "
       "not by itself make a parameter critical")
    also("Two rules of PCMP-001 Version 2.0 are added to the classification", chg)
    st("The TMP and the final DS concentration share one route to the product, the polarization layer.",
       chg, "The TMP and the final DS concentration share one route, the polarization layer.")
    st("With the crossflow and the membrane loading matched per unit area, the antibody passes through "
       "the pump as often at bench scale as at commercial scale.", chg,
       "With the crossflow and the membrane loading matched per unit area, the passes are the same at "
       "both scales.")
    st("The studies determine the effect of the number of diavolumes, the TMP and the final DS "
       "concentration on aggregate and on the acidic charge variants of the drug substance.",
       "Objectives",
       "To determine the effect of the number of diavolumes, the TMP and the final DS concentration on "
       "aggregate and on the acidic charge variants of the drug substance")
    st("The studies establish the number of diavolumes at which the retentate reaches the formulation "
       "buffer, so that the lower edge of the operating range rests on data for A-Mab.", "Objectives",
       "To establish the number of diavolumes at which the retentate reaches the formulation buffer, so "
       "that the lower edge of the operating range rests on data for A-Mab and not on platform practice "
       "alone.")
    st(f"The studies establish a PAR for each of the {w(ns['n_par'])} parameters against the drug "
       f"substance criteria for aggregate and the acidic charge variants.", "Objectives",
       f"To establish a PAR for each of the {w(ns['n_par'])} parameters against the drug substance "
       f"criteria for aggregate and the acidic charge variants")
    st("The step is operated under SOP-2013, the scale-down model is qualified under SOP-1001, and the "
       "parameters are classified after the studies under SOP-4001.", "Related documents",
       "The step is operated under SOP-2013, the scale-down model is qualified under SOP-1001, and the "
       "parameters are classified after the studies under SOP-4001.")
    st("The antibody accumulates at the membrane wall in a polarization layer, where its concentration "
       "is higher than in the bulk retentate.", prior,
       "The membrane retains the antibody, so the antibody accumulates at the membrane wall in a "
       "polarization layer, where its concentration is higher than in the bulk retentate.")
    st("Aggregate can form at the membrane wall, where the antibody is most concentrated, and in the "
       "pump, where cavitation, air–liquid interfaces and particles shed by the pump can start it.",
       prior,
       "Aggregate can form at the wall, where the antibody is most concentrated, and in the pump, where "
       "cavitation, air–liquid interfaces and particles shed by the pump can start it.")
    st("The expectations for the step come from general knowledge of the tangential flow filtration "
       "of antibodies, not from the A-Mab case study.", prior,
       "The expectations in the rest of this section come from general knowledge of the tangential "
       "flow filtration of antibodies.")
    also("The A-Mab case study leaves the UF/DF step out", prior)
    st("Deamidation of asparagine residues continues for as long as the step keeps the antibody in "
       "solution.", prior,
       "The step keeps the antibody in solution for the length of the operation, and deamidation of "
       "asparagine residues continues during that time.")
    st("The final DS concentration is studied for A-Mab and is not carried over from the platform.",
       prior, "For this reason the final DS concentration is studied for A-Mab and is not carried over "
              "from the platform.")
    st(f"The studies measure {w(len(ckeys))} attributes of the drug substance across the step.", cqa_sec,
       f"The studies measure {w(len(ckeys))} attributes of the drug substance across the step.")
    st("Both attributes arrive with the load, and the studies measure what the step adds to each, "
       "against the load from the virus filtration step.", cqa_sec,
       "The studies measure what this step adds to each, against the load from the virus filtration "
       "step.")
    also("Both attributes arrive with the load.", cqa_sec)
    st(f"All {w(ns['n_par'])} parameters of the step were assigned to univariate study in RA-001.", risk,
       f"All {w(ns['n_par'])} parameters of this step were assigned to univariate study.")
    st("The effect of the TMP depends on the final DS concentration, and an interaction between them is "
       "possible.", risk,
       "The effect of the TMP depends on the final DS concentration, and an interaction between them is "
       "possible.")
    st("The scale-down model holds the crossflow and the membrane loading at their commercial values, "
       "both scaled by membrane area.", sdm_sec,
       "The model holds the crossflow and the membrane loading at their commercial values, both scaled "
       "by membrane area (PCMP-001 §5).")
    st("The share of the batch held up in the system cannot be matched: the bench system holds a "
       "larger share of its batch in its recirculation loop and has a larger ratio of surface to "
       "volume.", sdm_sec,
       "The bench system, however, holds a larger share of its batch in its recirculation loop and has "
       "a larger ratio of surface to volume.")
    also("One quantity cannot be matched, the share of the batch held up in the system.", sdm_sec)
    st(f"In study {SDM_ST.id}, {w(ns['N_SDM'])} runs at the set-point condition are compared with the "
       f"pilot and commercial record on the step yield, the permeate flux, the final concentration "
       f"achieved and the change in aggregate content across the step.", sdm_sec, q_qual)
    st(f"The offset of each output is the mean of the scale-down runs at set-point minus the mean of the "
       f"manufacturing-scale batches, reported with its two-sided {ns['CI']} % confidence interval.",
       sdm_sec,
       f"Under the master plan PCMP-001 §7.1 the offset of each output is the mean of the scale-down "
       f"runs at set-point minus the mean of the manufacturing-scale batches, reported with its "
       f"two-sided {ns['CI']} % confidence interval.")
    st("Every judgement of a scale-down aggregate result against its criterion first subtracts the "
       "aggregate offset, so the conclusion is stated at manufacturing scale.", sdm_sec,
       "Every judgement of a scale-down aggregate result against that criterion first subtracts the "
       "aggregate offset, as PCMP-001 §7.1 requires for an output with a criterion, so the conclusion "
       "is stated at manufacturing scale.")
    st(f"At the set-point condition the step runs {g(sp(pdv))} {pdv.unit} at a TMP of {g(sp(ptmp))} "
       f"{ptmp.unit} to a final concentration of {g(sp(pconc))} {pconc.unit}.", "Operation",
       f"At the set-point condition the step runs {g(sp(pdv))} {pdv.unit} at a TMP of {g(sp(ptmp))} "
       f"{ptmp.unit} to a final concentration of {g(sp(pconc))} {pconc.unit}.")
    st("All runs of the study are loaded from a single pool of the virus filtration step, so that the "
       "variability of the load does not confound the comparison between the levels of a parameter.",
       "Operation",
       "All runs of the study are loaded from a single pool of the virus filtration step, so that the "
       "variability of the load does not confound the comparison between the levels of a parameter.")
    st("A change across the step in the low aggregate content of A-Mab may be of the same size as the "
       "repeatability of the SEC method.", "Analytical methods",
       "The aggregate content of A-Mab drug substance is low, and a change across this step may be of "
       "the same size as the repeatability of the SEC method.")
    st(f"For each parameter and each response, the measured values are regressed on the level of the "
       f"parameter and the slope is tested against zero at α = {g(ns['ALPHA'])}.", stats,
       f"For each parameter and each response, the measured values will be regressed on the level of "
       f"the parameter over the range studied, and the slope will be tested against zero at "
       f"α = {g(ns['ALPHA'])}.")
    st("The set-point replicates give the pure error estimate of the combined process and assay "
       "variability, against which a change across a range is read.", stats,
       "Those replicates give the pure error estimate of the combined process and assay variability, "
       "against which a change across a range is read.")
    st("Under PCMP-001 §6.2 an attribute is called affected by a parameter when the slope is "
       "significant at that level.", stats,
       "under it an attribute is called affected by a parameter when the slope is significant at that "
       "level")
    st("The criterion rather than the p-value decides whether a range is acceptable.", stats,
       "the criterion rather than the p-value decides whether the range is acceptable")
    st("The buffer-exchange analysis reports the number of diavolumes at which the conductivity of the "
       "retentate has reached the plateau set by the formulation buffer.", stats,
       "The analysis reports the number of diavolumes at which the conductivity of the retentate has "
       "reached the plateau set by the formulation buffer and no further change is measured over the "
       "following diavolume.")
    st("The diavolume range extends above the NOR because more diavolumes mean more time on the skid "
       "and more passes through the pump.", factors,
       "The range extends above the NOR because more diavolumes mean more time on the skid and more "
       "passes through the pump.")
    st("The lower edge of the diavolume range is the lower edge of the NOR, the lowest count the "
       "commercial step will run.", factors,
       "Its lower edge is the lower edge of the NOR, which is the lowest count the commercial step will "
       "run, and the buffer exchange curve characterizes the step at that value.")
    st("The TMP range extends above the NOR because pressure above the flux limit compacts the "
       "polarization layer without raising throughput.", factors,
       "The range extends above the NOR because pressure above the flux limit compacts the "
       "polarization layer without raising throughput, so more of the antibody sits at the highest "
       "concentration at the wall.")
    st("An excursion of the final DS concentration above the target raises the risk of aggregation.",
       factors,
       "An excursion above the target raises the viscosity and the bulk concentration of the retentate, "
       "lowers the flux and lengthens the operation, and so raises the risk of aggregation.")
    st("An excursion of the final DS concentration below the target leaves the drug substance below "
       "the concentration that the drug product program expects.", factors,
       "An excursion below the target leaves the drug substance below the concentration that the drug "
       "product program expects.")
    st(f"Each parameter is run at {w(ns['n_lev'])} levels, the two edges of its range studied and its "
       f"set-point, with the other parameters at their set-points.", "Univariate assessment", q_levels)
    st(f"The univariate study consists of {w(ns['n_edge'])} edge runs and {w(ns['n_sp'])} replicates of "
       f"the set-point condition, {w(ns['n_runs'])} runs in all.", "Univariate assessment", q_runs)
    st("The order of execution will be randomized across the whole study.", "Univariate assessment",
       "The order of execution will be randomized across the whole study.")
    st("Under PCMP-001 a model is qualified for an output when the conclusion over the NOR is the same "
       "with the offset at either end of its confidence interval, drawn from the response-surface model "
       "of the step.", "Scale-down model",
       "Under PCMP-001 a model is qualified for an output when the conclusion over the NOR is the same "
       "with the offset at either end of its confidence interval, and that conclusion is drawn from the "
       "response-surface model of the step.")
    q_agg_crit = f"Aggregate must not exceed {g(ACC_AGG[1])} % HMW"
    q_av_crit = f"the acidic charge variants must lie between {g(ACC_AV[0])} and {g(ACC_AV[1])} %"
    st(f"The final retentate must contain no more than {g(ACC_AGG[1])} % HMW aggregate.", pq, q_agg_crit)
    st(f"The acidic charge variants of the final retentate must lie between {g(ACC_AV[0])} and "
       f"{g(ACC_AV[1])} %.", pq, q_av_crit)
    st("The drug substance criteria come from the CQA register, and no result of the studies of the "
       "plan enters them.", pq,
       "They come from the drug substance CQA register (PCMP-001 §3), and no result of the studies of "
       "this plan enters them.")
    st(f"The a priori derivation in PCMP-001 assumes that no step after {ns['LAST_AGG']} changes aggregate, "
       f"and that no step after {ns['LAST_AV']} changes the acidic charge variants.", pq,
       f"The a priori derivation in PCMP-001 assumes that no step after {ns['LAST_AGG']} changes aggregate, "
       f"and that no step after {ns['LAST_AV']} changes the acidic charge variants (PCMP-001 Table 7.1).")
    st("The UF/DF step can add to aggregate and to the acidic charge variants, and its studies measure "
       "what it adds.", pq,
       "This step can add to both, and the studies of this plan measure what it adds.")
    st(f"PCMP-001 Version {ns['VER']} sets the aggregate increase across UF/DF at {ns['UF_ADD']} percentage "
       f"points, the prediction bound of a single batch within its NOR, and every aggregate criterion of the "
       f"earlier steps carries that increase.", pq,
       f"PCMP-001 Version {ns['VER']} sets the aggregate increase across this step at {ns['UF_ADD']} "
       f"percentage points, the prediction bound of a single batch within its NOR, and every aggregate "
       f"criterion of the earlier steps carries that increase (PCMP-001 §7.3).")
    st("The buffer exchange is accepted when the conductivity and the pH of the retentate have reached "
       "the plateau of the formulation buffer, at or below the lower edge of the diavolume NOR; the "
       "criterion is that of Version 1.0.", pq,
       "The buffer exchange is accepted when the conductivity and the pH of the retentate have reached "
       "the plateau of the formulation buffer")
    also(f"at or below the lower edge of the diavolume NOR of {g(nor(pdv)[0])} {pdv.unit}", pq)
    also("The buffer-exchange criterion is that of Version 1.0.", pq)
    rules = [
        "A level of a parameter is acceptable when every attribute measured on the final retentate of "
        "that run meets its criterion.",
        "A parameter passes over its range studied when every level in the range is acceptable and the "
        "change measured across the range is small against the criterion.",
        "Where a level fails, the range is truncated at the last acceptable level, and the failing level "
        "is reported as an edge of failure.",
        "Where a failure occurs at a level inside the NOR, execution stops, and the operating range is "
        "reviewed with the receiving site and with QA before the study continues.",
        "Where a run fails for a reason attributable to the equipment or to the method, and not to the "
        "parameter under study, the run may be repeated once.",
    ]
    for q in rules:
        st(q, "Decision rules", q)
    st("A parameter whose variation over the characterized range affects no quality attribute, but "
       "whose control is needed for the step to perform consistently, is a key process parameter.",
       "Classification",
       "A parameter whose variation over the characterized range affects no quality attribute, but whose "
       "control is needed for the step to perform consistently, is classified as a key process "
       "parameter.")
    st("A parameter whose variation affects a quality attribute is critical, or well controlled critical "
       "where the risk of falling outside the design space is low.", "Classification",
       "A parameter whose variation affects a quality attribute is classified as critical, or as well "
       "controlled critical where the risk of falling outside the design space is low.")
    st("A parameter studied one factor at a time is classified by the same rules as one studied in a "
       "design.", "Classification",
       "a parameter studied one factor at a time is classified by the same rules as one studied in a "
       "design (PCMP-001 §4)")
    st("The PAR of a parameter is the contiguous span of levels over which every attribute measured on "
       "the final retentate met its criterion, with the other parameters at their set-points.", par,
       "The PAR of a parameter is the contiguous span of levels over which every attribute measured on "
       "the final retentate met its criterion, with the other parameters at their set-points.")
    st("A PAR cannot be wider than the range studied.", par,
       "A PAR cannot be wider than the range studied.")
    st("Where a PAR is wider than the NOR, the margin between them is what a deviation is dispositioned "
       "against.", par,
       "Where a PAR is wider than the NOR, the margin between them is what a deviation is dispositioned "
       "against.")
    st("Where a PAR is truncated at an edge of failure, the NOR should be reviewed against the truncated "
       "range before the step is transferred.", par,
       "Where a PAR is truncated at an edge of failure, the NOR should be reviewed against the truncated "
       "range before the step is transferred.")
    st("As INV-001 preventive action PA3 requires, the study record gives the execution dates of each "
       "study and the calibration status of the equipment it used.", "Data management and integrity",
       "As INV-001 preventive action PA3 requires, the study record also gives the execution dates of "
       "each study and the calibration status of the equipment it used.")
    st(f"Version {VER} is the amendment that INV-001 required of each step plan as a corrective action, "
       f"issued after the runs and approved on its effective date, {EFF}.", "Roles and responsibilities",
       f"This Version {VER} is the amendment that INV-001 required of each step plan as a corrective "
       f"action, issued after the runs and approved on its effective date, {EFF}.")
    st("The deliverable of the plan is the report PCR-010, the process characterization report for the "
       "step.", sched,
       "The deliverable of this plan is the report PCR-010, the process characterization report for the "
       "step.")
    st(f"The studies of the plan ran on the skid {TFF}, whose next calibration was due on {TFF_DUE}; the "
       f"qualification study ended before the univariate study began, and both windows closed before "
       f"that date.", sched,
       "The qualification study ended before the univariate study began, and both windows closed before "
       "the calibration due date.")
    also(q_cal, sched)
    st("If aggregate fails its criterion at bench scale, the condition will be repeated at pilot scale "
       "before an operating range is narrowed on the strength of the bench result.", risks,
       "If aggregate fails its criterion at bench scale, the condition will be repeated at pilot scale "
       "before an operating range is narrowed on the strength of the bench result.")
    st("The slope test of each series rests on few runs, and an effect that is small against the "
       "variability between runs may not reach significance.", risks,
       "The slope test of each series therefore rests on few runs, and an effect that is small against "
       "the variability between runs may not reach significance.")
    st("A change to the formulation would change the target of the buffer exchange and would invalidate "
       "the diavolume study.", risks,
       "A change to the formulation would change the target of the buffer exchange and would invalidate "
       "the diavolume study.")
    st("A change to the design, to the ranges or to the acceptance criteria after approval requires a "
       "revision of the plan before the affected runs are executed.", "Approvals",
       "A change to the design, to the ranges or to the acceptance criteria after approval requires a "
       "revision of this plan, approved by the same functions, before the affected runs are executed.")

    # ---- acceptance criteria as the plan states them ---------------------------------------
    # The plan prints no criteria-change table: PCMP-001 defines no IAC for the step and Version 1.0
    # applied no step criterion (criteria_rev1.csv has no row for it), so the records are the ones
    # the text states.
    unit = {k: P.CFG.cqa(k)["unit"] for k in ckeys}
    crit_sec = f"{doc}_crit"
    bx = sorow[next(i for i, o in enumerate(so_df["Output"]) if o == buffer_out)]
    acrit = [
        S.AcceptanceCriterionRecord(
            step=ns["UO"], attribute="aggregates_hmw", low=None, high=float(ACC_AGG[1]),
            unit=unit["aggregates_hmw"], basis="drug substance", revision=P.REV2["rev"],
            status="in force", source=ref(doc, f, crit_sec, pq, q_agg_crit)),
        S.AcceptanceCriterionRecord(
            step=ns["UO"], attribute="acidic_variants", low=float(ACC_AV[0]), high=float(ACC_AV[1]),
            unit=unit["acidic_variants"], basis="drug substance", revision=P.REV2["rev"],
            status="in force", source=ref(doc, f, crit_sec, pq, q_av_crit)),
        S.AcceptanceCriterionRecord(
            step=ns["UO"], attribute="acidic_variants", low=None, high=float(ns["_V1_AV"][1]),
            unit=unit["acidic_variants"],
            basis="drug substance upper limit alone, as the Version 1.0 report PCR-010 read it at "
                  "analysis (INV-001 finding 4); Version 1.0 of the plan stated the two-sided criterion",
            revision=P.REV1["rev"], status="superseded", source=ref(doc, f, crit_sec, chg, q_v1_av)),
        S.AcceptanceCriterionRecord(
            step=ns["UO"], attribute="buffer_exchange", low=None, high=float(nor(pdv)[0]),
            unit=pdv.unit,
            basis="Version 1.0 criterion, kept: the conductivity and pH of the retentate reach the "
                  "plateau of the formulation buffer at or below the lower edge of the diavolume NOR",
            revision=P.REV2["rev"], status="in force",
            source=ref(doc, f, crit_sec, sdm_sec, bx, table_title=so_t.caption,
                       table_id=f"{doc}_tab_sdm_outputs", table_header=sorow.header)),
    ]

    # ---- concepts ---------------------------------------------------------------------------
    concepts = [Concept(concept_id=STEP_ID, concept_type="PROCESS_STEP", canonical_name=UFUO_NAME,
                        aliases=["UF/DF", "ultrafiltration and diafiltration", UO_TITLE,
                                 f"Step {STEP}"],
                        review_status="human_verified")]
    alias = {"Number of diavolumes": ["diavolumes"], "Transmembrane pressure": ["TMP"],
             "Final DS concentration": ["final concentration"]}
    concepts += [Concept(concept_id=UFPARAM_CONCEPT[name], concept_type="PROCESS_PARAMETER",
                         canonical_name=name, aliases=alias.get(name, []),
                         review_status="human_verified") for name in prow]
    concepts += _attr_concepts(ckeys)
    concepts += _method_concepts([a for a, _ in ns["UFDF_AMV_REFS"]], dict(ns["UFDF_AMV_REFS"]))
    concepts += [Concept(concept_id=e.equipment_id, concept_type="EQUIPMENT",
                         canonical_name=e.equipment_name, review_status="human_verified")
                 for e in equipment]

    # ---- notes ------------------------------------------------------------------------------
    moved = [p.name for p in prm.values()
             if float(p.setpoint) != float(sp(p)) or [float(x) for x in p.nor] != [float(x) for x in nor(p)]]
    nor_note = ("No set-point or NOR of the step changed at Version 2.0, so ProcessParameter.target_value "
                "and NOR are the values of the parameter table, which are also the values in force."
                if not moved else
                f"ProcessParameter.target_value and NOR are the values of the parameter table, against "
                f"which the studies were planned; the values in force differ for {', '.join(moved)}.")
    disc = [d for d in P.PLAN_DISCREPANCIES.get("PCR-010", []) if d.get("studies")]
    disc_txt = "; ".join(f"{', '.join(d['studies'])} ({d['id']})" for d in disc)
    return S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], **rev2_layer(doc, f),
        schema_extensions_used=COMMON_EXT + REV2_EXT,
        out_of_schema_notes=[
            "Classification is a result of the study, so every parameter_type is 'unclassified'. "
            + nor_note + " ProcessParameter.PAR carries the range studied, as everywhere in the "
            "corpus; the plan claims no proven acceptable range, so there are no "
            "ProvenAcceptableRange records. Each parameter is anchored on its row of the parameter "
            "table and on its sentence of the factors section that states the range studied against "
            "the NOR.",
            "UF/DF has no designed experiment, no design space and no intermediate acceptance "
            "criterion. The studies of the plan are the scale-down qualification and the univariate "
            "study. Neither StudyDesign carries n_runs or n_center_points: the qualification compares "
            "scale-down runs with manufacturing-scale batches, and the set-point replicates of the "
            "univariate study are not centre points of the ranges studied; the run counts are "
            "statements. StudyDesign.responses name the outputs as the document names them (the "
            "attributes of the attribute table, the outputs of the scale-down qualification table), "
            "not response keys. "
            + (f"Studies of the step made after Version 1.0 are not studies of this plan; PCR-010 "
               f"records them as discrepancies from it: {disc_txt}." if disc else ""),
            "acceptance_criteria: the plan prints no criteria-change table. The in-force records are "
            "the drug substance criteria for aggregate and the acidic charge variants, which apply "
            "directly at the last step, as the product quality section states them, and the "
            "buffer-exchange criterion kept from Version 1.0 (attribute 'buffer_exchange', not a CQA: "
            "the number of diavolumes at or below which the conductivity and pH of the retentate must "
            "reach the plateau of the formulation buffer). The superseded record is the upper limit "
            "alone against which the Version 1.0 report read the acidic charge variants (INV-001 "
            "finding 4); Version 1.0 of the plan stated the two-sided criterion.",
            "The plan prints no methods table. Each AnalyticalMethod is anchored on its sentence of "
            "the analytical methods section and its row of the procedures table, and SEC and icIEF "
            "also on the row of the attribute table that names them. A280 measures the protein "
            "concentration, on which the final concentration achieved (a parameter) and the mass "
            "balance rest, so that record has no associated attribute and no "
            "attribute_measured_by_method assertion. Conductivity and pH are in-process readings, not "
            "methods, and appear as an ExplicitNonClaim.",
            "parameter_impacts_attribute assertions are the plan's stated expectations from prior "
            "knowledge, not results. The three acidic charge variant assertions rest on two sentences, "
            "the one that names how each parameter lengthens the operation and the one that says the "
            "increase grows with the time in solution.",
            "The rows of the qualification-output table anchor the records they attest: the outputs "
            "compared at both scales the qualification StudyDesign, the two outputs not compared the "
            "ExplicitNonClaim on their unknown offsets, and the buffer-exchange row its acceptance "
            "criterion. The sampling rows and the planned runs (Appendix A) anchor the univariate "
            "StudyDesign; of the run-settings rows only those that occur once in the document are "
            "used, because the three set-point rows read alike. The commercial skid is an Equipment "
            "record at the receiving site, anchored on the objective that names it and on the "
            "roles-table row of the receiving site. The approvals table, the abbreviations and the "
            "remaining rows of the roles table are not represented. No rhetorical_spans: a plan has "
            "none. weak_claims is empty.",
        ] + _unrendered_note(unrendered),
        inventory=rev2_inventory(doc, f, "process_characterization_plan", UFUO_NAME,
                                 ["process characterization", "ultrafiltration and diafiltration",
                                  "tangential flow filtration", "buffer exchange", "protocol amendment",
                                  "univariate study", "scale-down offset", "drug substance criteria"]),
        entities=entities, studies=studies,
        report_sections=[ReportSection(section_id=f"{doc}-summary", title="Plan summary",
                                       statements=ST)],
        assertions=AssertionStore(run_id=f"gt-{doc}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{doc}", concepts=concepts),
        acceptance_criteria=acrit)
