"""PCP-009 Version 2.0, the characterization plan of small-virus retentive filtration (Step 9), issued
under INV-001 as a protocol amendment: its ground-truth annex (``build()``).

The kinds of record follow the step-plan models in ``build_ground_truth`` (``build_plan_viral_
inactivation`` for PCP-006, ``build_plan_protein_a``, ``build_plan_bioreactor``) and the concept ids
follow the Version 1.0 builder of this plan (``build_plan_vf``): the inventory and the revision layer,
the step, its scale-down model and the two sites, the two parameters, the three attributes the step is
judged against (the two cumulative viral clearance attributes and fragments), the three analytical
methods, the document relationships and the explicit non-claims, the three studies of the step, the
assertions, the plan statements, the concepts, and the criteria of the criteria-change table (Version
1.0 superseded, Version 2.0 in force). A plan claims no proven acceptable range and draws no design
space, so it has neither record.

Every table of the plan is a complex table (``T.frame`` or a ``T.`` builder), read back through
``qmd_ctables`` from the object the plan printed, so each row quote comes from the call that rendered
the row, with ``table_header=rows.header``. The related-documents table is the markdown string of
``related_docs_md``. Every prose quote is a sentence of the ``.qmd`` (or a slice of one that stops
short of a cross-reference or a citation) copied with its inline expressions and evaluated in the
plan's own namespace (``qmd_inline``); ``q`` refuses a snippet that is not a span of the ``.qmd``
prose, so no quote is typed here. ``build()`` refuses to return an annex with a quote that does not
ground or a weak anchor.

The first proven-acceptable-range analysis is recorded as the plan states it, and nothing is added
to it.
"""
from __future__ import annotations

import os
import re

import _pcpkg as P
import build_ground_truth as G
import schema_ext as S
from check_grounding import normalize, specificity_report

DOC = "PCP-009"
FILE = "PCP-009_virus_filtration.docx"
QMD = "PCP-009_virus_filtration.qmd"
UO = "virus_filtration"
#: The scale-down model as the plan names it (Section 5.1).
SDM_NAME = "laboratory scale filtration system"

_PRIOR = "Prior knowledge and quality risk basis"
_MM = "Materials and methods"
_SD = "Study design"
#: Section key -> heading path as the document renders it. ``_check_sections`` checks every title
#: against the headings of the .qmd, so a renamed section fails loudly instead of mislabelling.
SEC = {
    "title": ("Title block",),
    "purpose": ("Purpose and scope",),
    "changes": ("Purpose and scope", "Changes in this revision"),
    "objectives": ("Objectives",),
    "related": ("Related documents",),
    "uo": (_PRIOR, "Unit-operation description and prior knowledge"),
    "cqa": (_PRIOR, "Quality attributes in scope"),
    "risk": (_PRIOR, "Risk-based prioritization of parameters"),
    "sdm": (_MM, "Scale-down model and its qualification"),
    "operation": (_MM, "Operation"),
    "analytical": (_MM, "Analytical methods"),
    "sampling": (_MM, "Sampling plan"),
    "stats": (_MM, "Statistical methods"),
    "factors": (_SD, "Factors, ranges and study type"),
    "screening": (_SD, "Screening design"),
    "rsm": (_SD, "Response-surface design"),
    "univariate": (_SD, "Univariate assessment"),
    "criteria": ("Acceptance and decision criteria",),
    "par": ("Proven acceptable ranges (planned analysis)",),
    "data": ("Data management and integrity",),
    "roles": ("Roles and responsibilities",),
    "schedule": ("Deliverables and schedule",),
    "risks": ("Risks and assumptions",),
    "approvals": ("Approvals",),
    "app_a": ("Appendix A. Planned screening design matrix",),
    "app_b": ("Appendix B. Planned response-surface design matrix",),
}
#: Relationship cell of the related-documents table -> DocumentRelationship.kind (others: references).
REL_KIND = {"Rolls up into": "rolls_up_into", "Parent — master plan": "executed_under",
            "Parent — risk basis for study scope": "scoped_by", "Parent — transfer scope": "scoped_by"}


def _sid(sec):
    return f"{DOC}_sec_{sec}"


def _source():
    return open(os.path.join(G.HERE, QMD), encoding="utf-8").read()


def _prose():
    """The .qmd outside its code chunks, in the comparison form (``normalize``)."""
    return normalize(re.sub(r"```\{python\}.*?```", " ", _source(), flags=re.S))


def _check_sections():
    """Every heading of SEC is a heading of the .qmd (outside its code chunks)."""
    prose = re.sub(r"```\{python\}.*?```", "", _source(), flags=re.S)
    heads = set(re.findall(r"^#+ (.+?)(?: \{[^}]*\})?\s*$", prose, flags=re.M))
    missing = sorted({t for path in SEC.values() for t in path if t != "Title block"} - heads)
    if missing:
        raise ValueError(f"{DOC}: section titles not in the document: {missing}")


def _smart(s):
    """Prose as pandoc renders it: straight double quotes become typographic pairs and a straight
    apostrophe a typographic one. Table cells are raw markup and keep the straight forms."""
    return re.sub(r'"([^"]*)"', "“\\1”", s).replace("'", "’")


def _cells(row):
    """The cells of a rendered row: a continuation row keeps its empty first cell."""
    return [c.strip() for c in row.split("|")]


def _nomark(s):
    """A cell without its footnote marker ("Spiking model^a)^" -> "Spiking model")."""
    return re.sub(r"\^[a-z]\)\^", "", str(s)).strip()


def _walk(o, fields, out):
    if isinstance(o, dict):
        for f in fields:
            if isinstance(o.get(f), str):
                out.append(o[f])
        for v in o.values():
            _walk(v, fields, out)
    elif isinstance(o, list):
        for v in o:
            _walk(v, fields, out)
    return out


def _gate(annex, text):
    """The grounding gate, applied before the annex is returned: every quote and table header is a
    verbatim span of the rendered document, and no quote is a weak anchor
    (``check_grounding.specificity_report``)."""
    d = annex.model_dump(mode="json", serialize_as_any=True)
    miss = [q for q in _walk(d, ("quote", "table_header"), []) if normalize(q) not in text]
    weak = specificity_report(d, text)
    if miss or weak:
        raise ValueError(f"{DOC}: {len(miss)} ungrounded quote(s), {len(weak)} weak anchor(s):\n  "
                         + "\n  ".join([f"ungrounded: {q!r}" for q in miss] + [f"weak: {w}" for w in weak]))


def build():
    import doe_report as D
    import tables as T
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    from annex_contract.concepts import Concept, ConceptStore
    from annex_contract.discourse import DocumentRelationship, ExplicitNonClaim
    from annex_contract.summaries import ReportSection, ReportStatement

    _check_sections()
    ns, _ = G.qmd_namespace(QMD)
    ct = G.qmd_ctables(QMD)
    text = G._document_text(FILE)
    prose_src = _prose()
    meta = G.meta

    def q(src):
        """A prose span of the .qmd as it renders. ``src`` must be copied from the .qmd."""
        if normalize(src) not in prose_src:
            raise ValueError(f"{DOC}: not a span of the .qmd prose: {src!r}")
        return _smart(G.qmd_inline(ns, src))

    def t(txt):
        """Annex text with the plan's own values (inline expressions evaluated in its namespace)."""
        return G.qmd_inline(ns, txt)

    def ref(sec, quote, table=None, rows=None, caption=None, label=None):
        r = G.ref(DOC, FILE, _sid(sec), SEC[sec][-1], quote,
                  table_title=caption if table is None else table.caption,
                  table_id=label if table is None else table.label,
                  table_header=None if rows is None else rows.header)
        r.heading_path = list(SEC[sec])
        return r

    def keyed(label, keys, name_of, cell=None):
        """The rendered rows of the CTable the plan printed under ``label``, keyed. Every row must
        name its own record (in cell ``cell``, or anywhere): a mis-keyed row grounds and attests the
        wrong thing."""
        tab = ct[label][0]
        rows = G.ctable_rows(tab, keys)
        bad = [k for k, row in rows.items()
               if not (_cells(row)[cell] == name_of(k) if cell is not None else name_of(k) in row)]
        if bad:
            raise ValueError(f"{DOC} {label}: rows keyed to records they do not name: {bad}")
        return tab, rows

    # ---- names and values of the plan -------------------------------------------------------
    UO_NAME, STEP_LABEL = G.VFUO_NAME, G.VFSTEP_LABEL
    VI_NAME = P.CFG.unit_op("viral_inactivation").name
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))
    reg = P.cqa_reg.set_index("key")
    by_label = G._attr_key_by_label()
    resp_of_label = {v: k for k, v in ns["_lab"].items()}       # the labels the plan's tables use
    iac = ns["_iac"].set_index("cqa")                            # D.iac_table(UO)
    PC = G.VFPARAM_CONCEPT                                       # parameter name -> concept id
    Vol, Prs = ns["Vol"], ns["Prs"]
    pc_vol, pc_prs = PC[Vol], PC[Prs]

    # ---- the rendered tables, from the objects the plan printed ------------------------------
    pdf_ = ct["tbl-params"][1]
    pt, prow = keyed("tbl-params", list(pdf_["Parameter"]), str, cell=0)
    ldf = ct["tbl-legend"][1]
    lt, lrow = keyed("tbl-legend", list(ldf["Factor"]), str, cell=1)
    cq_df = ct["tbl-cqa"][1]
    ckeys = [by_label[n] for n in cq_df["CQA"]]
    cq_t, crow = keyed("tbl-cqa", ckeys, lambda k: names[k], cell=1)
    as_df = ct["tbl-assays"][1]
    as_t, arow = keyed("tbl-assays", list(as_df["Method validation"]), str, cell=2)
    sop_df = ct["tbl-sops"][1]
    sop_t, soprow = keyed("tbl-sops", list(sop_df["Reference"]), str, cell=1)
    sdm_df = ct["tbl-sdm"][1]
    sdm_t, sdmrow = keyed("tbl-sdm", list(sdm_df["Output"]), str, cell=1)
    w_df = ct["tbl-windows"][1]
    w_t, wrow = keyed("tbl-windows", list(w_df["Study"]), str, cell=0)
    ikeys = [by_label[_cells(r)[0]] for r in ct["tbl-iac"][0].rows()]
    iac_t, irow = keyed("tbl-iac", ikeys, lambda k: T.ATTR_NAME[k], cell=0)
    mtx = {}
    for kind, label, pm in (("screening", "tbl-matrix-scr", ns["pm_scr"]),
                            ("rsm", "tbl-matrix-rsm", ns["pm_rsm"])):
        mtx[kind] = keyed(label, [int(r) for r in pm["Run"]], str, cell=1)
    rel = G.md_string_rows(P.related_docs_md(DOC))
    rel_cap, rel_label = "Related documents.", "tbl-related"   # printed after related_docs_md
    if normalize(f"{rel_cap} {rel.header}") not in text:
        raise ValueError(f"{DOC}: the related-documents caption no longer reads {rel_cap!r}")

    # ---- prose spans used by more than one record ----------------------------------------------
    q_scope = q("This plan describes the characterization study for Step 9 of the drug substance train, the small virus retentive filtration step.")
    q_role = q("The step is the dedicated small virus removal operation of the purification train and the principal source of clearance of minute virus of mice (MVM).")
    q_load = q("The load is the flow-through pool of the anion exchange step.")
    q_out = q("Its output, the filtrate pool, is also judged against the criterion for fragments")
    q_sdm = q("The study will be run on a laboratory scale filtration system fitted with the same membrane type and the same membrane chemistry as the commercial step.")
    q_multi = q("Both parameters will be studied multivariately.")
    q_rule = q("This criticality was assigned by rule, because a viral contamination would directly harm the patient (master plan PCMP-001 §3).")
    q_low = q("Fragments are of low criticality.")
    q_resp = q("The responses of the designs are the log reduction factors (LRF) of MVM and of xenotropic murine leukemia virus (XMuLV), fragments and step yield.")
    q_cumul = q("The cumulative viral clearance claim for the drug substance is consolidated across all three viral safety steps in PCMR-001, and this study establishes only the contribution of Step 9.")
    q_sched = q("The study is scheduled against the transfer programme in PTP-001, and its report rolls up into PCMR-001 with the reports of the other two viral safety steps.")
    q_xm = q("It is retained completely while the membrane is intact, and its clearance is insensitive to the operating parameters over any range that can be run.")
    q_expect = q("supports the expectation that MVM retention falls with volumetric load while XMuLV retention does not")
    q_mvm_rest = q("The cumulative MVM requirement therefore rests on the claims of anion exchange chromatography and of this step alone (PCMP-001 §7.4).")

    # ==== entities ================================================================================
    step = S.ProcessStep(
        step_id="step:virus_filtration", step_name=UO_NAME, step_number=str(G.VFSTEP),
        unit_operation=UO_NAME,
        description="The dedicated small virus removal operation of the purification train. The membrane "
                    "removes virus by size: it retains the parvovirus MVM, which sits close to the pore "
                    "size cut-off, and the much larger retrovirus XMuLV, while the antibody passes "
                    "through. The load is the anion exchange flow-through pool and the output is the "
                    "filtrate pool. The step is the principal source of MVM clearance and forms no "
                    "quality attribute.",
        input_materials=["anion exchange flow-through pool"],
        output_materials=["filtrate pool"],
        equipment=[SDM_NAME],
        source_references=[ref("purpose", q_scope), ref("purpose", q_role), ref("operation", q_load),
                           ref("cqa", q_out)],
        metadata=meta())
    equipment = [S.Equipment(
        equipment_id="equip:vf_sdm", equipment_name=SDM_NAME,
        equipment_type="virus filtration system (scale-down model)",
        source_references=[ref("sdm", q_sdm)], metadata=meta())]
    sites = G._site_entities(DOC, FILE, _sid("title"))

    pp = ns["_pp"].set_index("Parameter")                       # plan_params, as the plan printed it
    params = []
    for name, row in prow.items():
        r = pp.loc[name]
        unit = r["Unit"]
        params.append(S.ProcessParameter(
            parameter_id=PC[name], parameter_name=name, parameter_type="unclassified", unit=unit,
            target_value=f"{r['Set-point']} {unit}", NOR=f"{r['NOR']} {unit}",
            PAR=f"{r['Range studied']} {unit}", associated_step=STEP_LABEL,
            study_type=str(r["Study type"]),
            source_references=[ref("factors", row, pt, prow), ref("factors", lrow[name], lt, lrow),
                               ref("factors", q_multi)],
            metadata=meta()))

    method_of = {D.RESP_TO_CQA[resp_of_label[o]]: a
                 for o, a in zip(as_df["Output"], as_df["Method validation"])}
    attrs = []
    for key in ckeys:
        r = reg.loc[key]
        acc = cq_df.loc[cq_df["CQA"] == r["cqa"], "Acceptance"].iloc[0]
        viral = key.startswith("lrv_")
        why = (f"Very high, assigned by rule because a viral contamination would directly harm the "
               f"patient (PCMP-001 §3); Tool #1 score {r['tool1_score']}." if viral
               else f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = {r['tool1_score']}.")
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=r["cqa"], attribute_type="CQA", unit=r["unit"],
            acceptance_criteria=[f"{acc} (drug substance)"], analytical_method=method_of.get(key),
            associated_steps=[STEP_LABEL], rationale_for_criticality=why,
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[ref("cqa", crow[key], cq_t, crow), ref("cqa", q_rule if viral else q_low)],
            metadata=meta()))

    q_amv_vir = q("The method validations AMV-3018 and AMV-3017 cover the infectivity assays for the model viruses")
    q_method = {"AMV-3018": [("analytical", q("MVM will be titred by TCID50 with qPCR confirmation")),
                             ("related", q_amv_vir)],
                "AMV-3017": [("analytical", q("XMuLV by TCID50.")), ("related", q_amv_vir)],
                "AMV-3020": [("analytical", q("Fragments are measured by nrCE-SDS under change 2.")),
                             ("related", q("AMV-3020 covers the fragment method."))]}
    methods = []
    for _, r in as_df.iterrows():
        amv = r["Method validation"]
        key = D.RESP_TO_CQA[resp_of_label[r["Output"]]]
        methods.append(S.AnalyticalMethod(
            method_id=amv, method_name=r["Method"], method_type=G.METHOD_TYPE.get(amv),
            analytes=[r["Output"]], associated_attributes=[f"attr:{key}"], validation_status="validated",
            source_references=[ref("analytical", arow[amv], as_t, arow),
                               ref("related", soprow[amv], sop_t, soprow)]
            + [ref(s, x) for s, x in q_method[amv]],
            metadata=meta()))

    # explicit non-claims, by section
    nc, nc_at = [], {}

    def nclaim(sec, subject, statement, quotes, rationale=None, elsewhere=None, uo=UO_NAME):
        refs = [ref(s, x) for s, x in quotes]
        nc.append(ExplicitNonClaim(
            non_claim_id=f"{DOC}-NC{len(nc) + 1:02d}", subject=subject, unit_operation=uo,
            statement=statement, rationale=rationale, handled_elsewhere=elsewhere,
            source_references=refs, metadata=meta()))
        nc_at.setdefault(sec, []).append(nc[-1])

    nclaim("purpose", "qualification of the membrane",
           "The plan does not qualify the membrane; its qualification is held by the filter manufacturer "
           "and is not repeated.",
           [("purpose", q("Qualification of the membrane itself is held by the filter manufacturer and is not repeated here."))],
           elsewhere="the filter manufacturer")
    nclaim("purpose", "cumulative viral clearance claim for the drug substance",
           f"The study establishes only the contribution of Step {G.VFSTEP} to viral clearance; the "
           f"cumulative claim for the drug substance is consolidated across all three viral safety steps "
           f"in PCMR-001.", [("purpose", q_cumul)], elsewhere="PCMR-001")
    nclaim("purpose", "process validation at commercial scale",
           "Process validation at commercial scale is not covered by the study.",
           [("purpose", q("Process validation at commercial scale is covered by the validation programme and not by this study."))],
           elsewhere="the validation programme")
    nclaim("uo", "change in fragments across the step",
           "The step is not expected to change the fragment level of its load.",
           [("uo", q("The step is therefore not expected to change the fragment level of its load."))],
           rationale="Fragments, the clipped species of the antibody, are smaller than the intact antibody "
                     "and pass the pores in the same way.")
    nclaim("cqa", "quality attribute formed by the step", "The step forms no quality attribute.",
           [("cqa", q("The step forms no quality attribute."))],
           rationale="It contributes log reduction to the two viral safety attributes, both cumulative "
                     "requirements on the drug substance met by several steps together, and its filtrate "
                     "pool is judged against the criterion for fragments.")
    nclaim("cqa", "MVM clearance claim of low pH inactivation",
           "Of the steps that carry a viral clearance claim, low pH inactivation makes none for MVM.",
           [("cqa", q("Of the steps that carry a viral clearance claim, low pH inactivation makes none for MVM, because MVM is non-enveloped and low pH acts on the lipid envelope.")),
            ("cqa", q_mvm_rest)],
           rationale="MVM is non-enveloped and low pH acts on the lipid envelope.",
           elsewhere="the claims of anion exchange chromatography and of this step", uo=VI_NAME)
    nclaim("cqa", "drug substance viral clearance criteria at the step",
           "The cumulative acceptance values of the two viral safety attributes cannot be applied to one "
           "step.",
           [("cqa", q("are cumulative across the process and cannot be applied to one step."))])
    nclaim("cqa", "quality criterion for step yield",
           "Step yield is judged against no quality criterion; it is a process performance response that "
           "is measured and reported.",
           [("cqa", q("No drug substance attribute maps to it, so it will be measured and reported but judged against no quality criterion."))],
           rationale="Step yield is a process performance response, and no drug substance attribute maps "
                     "to it.")
    nclaim("sdm", "scale offset of the two LRF and fragments",
           "The two LRF and fragments are not compared at both scales, so their offset is unknown, not "
           "zero, and they are judged as the scale-down model predicts them.",
           [("sdm", q("The two LRF and fragments are not compared at both scales.")),
            ("sdm", q("Their offset is unknown, not zero, and they are judged as the scale-down model predicts them (PCMP-001 §7.1)."))],
           rationale="Virus cannot be spiked into a manufacturing batch; under PCMP-001 §7.1 the "
                     "representativeness of the log reductions rests on the spiking model and that of the "
                     "fragment result on the mechanism of the step.")
    nclaim("operation", "interruption of flow",
           "The claim made from the study applies to uninterrupted operation only; an interruption of flow "
           "at commercial scale is a deviation outside the operating region the study will define, and the "
           "ranges do not cover it.",
           [("operation", q("The claim made from this study applies to uninterrupted operation, because an interruption of flow allows virus held in the pore structure to diffuse through it.")),
            ("operation", q("An interruption at commercial scale is a deviation and lies outside the operating region this study will define.")),
            ("risks", q("The ranges it produces do not cover an interruption of flow"))],
           rationale="An interruption of flow allows virus held in the pore structure to diffuse through it.",
           elsewhere="assessment as a deviation against the mechanism of the step")
    nclaim("analytical", "allowance for assay variability",
           "The criteria of Version 2.0 carry no allowance for the variability of the infectivity assays.",
           [("analytical", q("The criteria of this revision carry no allowance for it (change 1)."))],
           rationale="The infectivity assays carry their own variability.")
    nclaim("univariate", "univariate study", "No parameter of the step is assigned to univariate study.",
           [("univariate", q("No parameter of this step is assigned to univariate study."))],
           rationale="Both parameters are factors of the two designs, and the remaining operating variables "
                     "are held at their set-points under SOP-2012 and supported by platform experience.")
    nclaim("criteria", "thresholds for normality and for the residual standard error",
           "Version 1.0 set no threshold for the departure from normality on the normal quantile plot or for "
           "the residual standard error against the distance to the criterion.",
           [("criteria", q("Version 1.0 set no threshold for the departure from normality on the normal quantile plot or for the residual standard error against the distance to the criterion, and PCR-009 states how it judges them."))],
           elsewhere="PCR-009")
    nclaim("criteria", "verification of platform worst cases",
           "No criterion relies on a platform worst case of this step, so there is none to verify.",
           [("criteria", q("No criterion relies on a platform worst case of this step, so PCR-009 has none to verify."))])
    nclaim("criteria", "numerical thresholds for the classification",
           "Neither PCMP-001 nor SOP-4001 sets a number for the size of an effect across the PAR or for the "
           "margin between the PAR and the NOR.",
           [("criteria", q("Neither PCMP-001 nor SOP-4001 sets a number for either, so PCR-009 states both and gives the reason for each class."))],
           elsewhere="PCR-009")
    nclaim("par", "PAR beyond the range studied",
           "A proven acceptable range that reaches the edge of the characterization range is reported as "
           "reaching it, and no claim is made beyond it.",
           [("par", q("A proven acceptable range that reaches the edge of the characterization range is reported as reaching it, and no claim is made beyond it."))])
    nclaim("par", "proven acceptable ranges", "The plan claims no proven acceptable range.",
           [("par", q("The ranges themselves will be reported in PCR-009."))], elsewhere="PCR-009")
    nclaim("schedule", "instrumented scale-down systems in the study record",
           "The record names none of the instrumented scale-down systems under calibration and change "
           "control of PCMP-001 Table 5.1 for the studies of the step.",
           [("schedule", q("The record names none of the instrumented scale-down systems under calibration and change control of PCMP-001 Table 5.1 for these studies."))])

    # document relationships: the rows of the related-documents table, then the prose
    rels = []

    def relation(kind, target, statement, sec, quote, table_row=False):
        r_ = (ref(sec, quote, rows=rel, caption=rel_cap, label=rel_label) if table_row
              else ref(sec, quote))
        rels.append(DocumentRelationship(
            relationship_id=f"{DOC}-R{len(rels) + 1:02d}", kind=kind, source_document_id=DOC,
            target_document_ref=target, statement=statement, source_references=[r_], metadata=meta()))

    for target, row in rel.items():
        txt = _cells(row)[-1]
        relation(REL_KIND.get(txt, "references"), target, txt, "related", row, table_row=True)
    relation("references", "PCR-009", "The criteria of Version 2.0 govern the analysis that PCR-009 "
             "Version 2.0 presents.", "purpose",
             q("and its criteria govern the analysis that the report PCR-009 Version 2.0 presents."))
    relation("references", "PCMR-001", "The cumulative viral clearance claim for the drug substance is "
             "consolidated across the three viral safety steps in PCMR-001.", "purpose", q_cumul)
    relation("references", "INV-002", "The investigation of the response-surface models below the "
             "model-adequacy criteria of PCMP-001 §7.2; PCR-009 applies its corrective actions.", "changes",
             q("The revision history also names INV-002, the investigation of the response-surface models that fell below the model-adequacy criteria of PCMP-001 §7.2."))
    relation("references", ns["AMD"]["id"], "The analytical method decision that set nrCE-SDS for "
             "fragments in every study at every step.", "changes",
             q("This method was set for every study at every step from `{python} AMD_DATE` by the analytical method decision AMD-001 (PCMP-001 §7.8), and both designs of the step started after that date"))
    relation("references", "PTP-001", "The study is scheduled against the transfer programme of PTP-001.",
             "schedule", q_sched)
    relation("rolls_up_into", "PCMR-001", "The report of the study rolls up into PCMR-001 with the "
             "reports of the other two viral safety steps.", "schedule", q_sched)
    relation("references", "PCR-008", "The characterization of anion exchange, the step that supplies "
             "the load, is reported in PCR-008.", "risks",
             q("Anion exchange is the step immediately upstream and its own characterization is reported in the anion exchange report PCR-008."))

    entities = [
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("purpose"), process_steps=[step],
                                  sites=sites, non_claims=nc_at["purpose"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("related"),
                                  document_relationships=rels),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("uo"), non_claims=nc_at["uo"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cqa"), quality_attributes=attrs,
                                  non_claims=nc_at["cqa"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("sdm"), equipment=equipment,
                                  non_claims=nc_at["sdm"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("operation"),
                                  non_claims=nc_at["operation"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("analytical"),
                                  analytical_methods=methods, non_claims=nc_at["analytical"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("factors"), parameters=params),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("univariate"),
                                  non_claims=nc_at["univariate"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("criteria"),
                                  non_claims=nc_at["criteria"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("par"), non_claims=nc_at["par"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("schedule"),
                                  non_claims=nc_at["schedule"]),
    ]

    # ==== studies: each on its row of the execution-window table, its prose and its design matrix ==
    factors = list(prow)                                          # the parameter names, table order
    if set(factors) != {P.CFG.unit_op(UO).param(k).name for k in D.rsm_factors(UO)}:
        raise ValueError(f"{DOC}: the parameter table no longer lists the factors of the designs")
    prose = {
        "qualification": [("sdm", q("Qualification will follow the scale-down model procedure SOP-1001, in study `{python} ID_SDM`.")),
                          ("sdm", q("on representative anion exchange pool, and the flux decay profile, the step yield and the post-use integrity test result will be compared with the corresponding manufacturing scale records.")),
                          ("sdm", q("The manufacturing-scale data set is the records of `{python} n_m` batches."))],
        "screening": [("screening", q("The screening study `{python} ID_SCR` will be a two-level factorial in both factors with centre point replicates, `{python} n_scr` runs in total.")),
                      ("screening", q("Of these, `{python} n_fac_scr` runs are the factorial points at the corners of the characterization ranges and `{python} cp_scr` are replicates of the centre point.")),
                      ("purpose", q_resp)],
        "rsm": [("rsm", q("The response-surface study `{python} ID_RSM` will be a face-centred central composite design in both factors, `{python} n_rsm` runs in total.")),
                ("rsm", q("It is made up of `{python} n_fac_rsm` factorial points, `{python} n_ax_rsm` axial points and `{python} cp_rsm` centre point replicates.")),
                ("purpose", q_resp)],
    }
    design = {
        # no n_runs: the qualification compares scale-down runs with manufacturing-scale batches,
        # which is not a design (tests/test_config.py checks n_runs against the seeded designs)
        "qualification": dict(responses=["step_yield"]),
        "screening": dict(design_name="two-level full factorial with centre point replicates",
                          factors=factors, responses=list(D.responses(UO)) + D.fragment_responses(UO, "screening"),
                          n_runs=ns["n_scr"], n_center_points=ns["cp_scr"]),
        "rsm": dict(design_name="face-centred central composite design", factors=factors,
                    responses=list(D.responses(UO)) + D.fragment_responses(UO, "rsm"),
                    n_runs=ns["n_rsm"], n_center_points=ns["cp_rsm"]),
    }
    if (P.doe_runs(UO, "screening"), P.doe_centre_points(UO, "screening")) != (ns["n_scr"], ns["cp_scr"]) or \
            (P.doe_runs(UO, "rsm"), P.doe_centre_points(UO, "rsm")) != (ns["n_rsm"], ns["cp_rsm"]):
        raise ValueError(f"{DOC}: the plan's run counts disagree with the seeded designs")
    extra = {"qualification": [ref("sdm", sdmrow[o], sdm_t, sdmrow) for o in sdmrow
                               if _nomark(sdm_df.loc[sdm_df["Output"] == o, "Compared at both scales"].iloc[0]) == "Yes"]
             + [ref("related", soprow["SOP-1001"], sop_t, soprow)]}
    for kind, (mt_, mrows) in mtx.items():
        extra[kind] = [ref("app_a" if kind == "screening" else "app_b", row_, mt_, mrows)
                       for row_ in mrows.values()]
    studies, unrendered = [], []
    for _, r in ns["_ch"].iterrows():
        stype = G.STUDY_TYPE.get(r["kind"])
        if stype is None:
            continue
        if not G._present(wrow[r["id"]], text):
            unrendered.append(r["id"])
            continue
        d = design[r["kind"]]
        refs = [ref("schedule", wrow[r["id"]], w_t, wrow)]
        refs += [ref(s, x) for s, x in prose[r["kind"]]] + extra[r["kind"]]
        studies.append(S.StudyDesign(
            study_id=f"study:{r['id']}", study_type=stype, unit_operation=UO_NAME,
            scale_down_model=SDM_NAME, associated_parameters=[PC[x] for x in d.get("factors", [])],
            source_references=refs, metadata=meta(), **d))

    # ==== assertions ==============================================================================
    A = []

    def add(subj, pred, obj, txt, refs):
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{DOC}-A{len(A) + 1:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=txt, source_references=refs, metadata=meta()))

    add("step:virus_filtration", "step_uses_equipment", "equip:vf_sdm",
        f"The scale-down model of {UO_NAME} is a {SDM_NAME} fitted with the same membrane type and the "
        f"same membrane chemistry as the commercial step.", [ref("sdm", q_sdm)])
    for name, row in prow.items():
        add("step:virus_filtration", "step_has_parameter", PC[name],
            f"{UO_NAME} has process parameter {name}.", [ref("factors", row, pt, prow)])
    role = {"lrv_mvm": "contributes log reduction to {n}, a cumulative requirement on the drug substance",
            "lrv_xmulv": "contributes log reduction to {n}, a cumulative requirement on the drug substance",
            "fragments_lmw": "has its filtrate pool judged against the drug substance criterion for {n}"}
    for key in ckeys:
        add("step:virus_filtration", "step_has_quality_attribute", f"attr:{key}",
            f"{UO_NAME} " + role[key].format(n=names[key]) + ".", [ref("cqa", crow[key], cq_t, crow)])
    for _, r in as_df.iterrows():
        amv, key = r["Method validation"], D.RESP_TO_CQA[resp_of_label[r["Output"]]]
        add(f"attr:{key}", "attribute_measured_by_method", f"method:{amv}",
            f"{names[key]} is measured by {amv} ({r['Method'][0].lower() + r['Method'][1:]}); the plan "
            f"reports it as {r['Output']}.",
            [ref("analytical", arow[amv], as_t, arow)])
    for key, row in irow.items():
        x = iac.loc[key]
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{UO}_{key}_iac",
            f"At the small virus retentive filtration step, {names[key]} is judged against the Version "
            f"{P.REV2['rev']} intermediate acceptance criterion "
            f"{T.crit(x['iac_low'], x['iac_high'], x['spec_type'])} ({x['basis']}).",
            [ref("criteria", row, iac_t, irow)])
    # expectations stated from prior knowledge and the risk assessment, not results
    add(pc_vol, "parameter_impacts_attribute", "attr:lrv_mvm",
        f"MVM retention is expected to fall as the {ns['vol']} rises, as fouling carries the flux onto "
        f"the largest pores; the highest load of a batch is where retention is weakest.",
        [ref("uo", q("MVM breakthrough therefore rises with the volume filtered per unit area, and the highest load of a batch is the point at which retention is weakest.")),
         ref("risk", q("The `{python} vol` was ranked high because MVM retention falls as the volume filtered per unit area rises, once fouling has carried the flux onto the largest pores.")),
         ref("uo", q_expect)])
    add(pc_prs, "parameter_impacts_attribute", "attr:lrv_mvm",
        "MVM retention is expected to depend on the filtration pressure: a low pressure or a stop in flow "
        "lets virus held in the pore structure diffuse through, and a high pressure drives more filtrate "
        "through the largest open pores.",
        [ref("uo", q("A low transmembrane pressure or an interruption of flow can also allow virus held within the pore structure to diffuse through, so pressure is controlled as well as volume.")),
         ref("risk", q("The `{python} prs` was ranked high because a loss of pressure or a stop in flow lets MVM already held in the pore structure diffuse forward into the filtrate, and because a rise in pressure drives more filtrate through the pores that remain open.")),
         ref("factors", q("High pressures are included because they raise the flux and compress the fouling layer, so more filtrate passes through the largest open pores and MVM retention is expected to fall."))])
    add(pc_vol, "parameter_does_not_significantly_impact_attribute", "attr:lrv_xmulv",
        f"XMuLV clearance is expected to be insensitive to the {ns['vol']}: the virus is retained "
        f"completely while the membrane is intact.", [ref("uo", q_xm), ref("uo", q_expect)])
    add(pc_prs, "parameter_does_not_significantly_impact_attribute", "attr:lrv_xmulv",
        f"XMuLV clearance is expected to be insensitive to the {ns['prs']}: the virus is retained "
        f"completely while the membrane is intact.", [ref("uo", q_xm)])
    add(pc_vol, "parameter_impacts_attribute", "attr:step_yield",
        f"Step yield is expected to be high and to fall slowly as the {ns['vol']} rises, because the "
        f"fouling layer and the product held in it grow with the volume filtered.",
        [ref("uo", q("Yield is therefore expected to be high and to fall slowly as the volumetric load rises.")),
         ref("uo", q("The fouling layer, and the product held in it, grow with the volume filtered."))])

    # ==== plan statements =========================================================================
    ST = []

    def st(txt, refs):
        ST.append(ReportStatement(
            statement_id=f"{DOC}-S{len(ST) + 1:03d}", statement_text=txt, confidence="high",
            review_status="accepted", source_references=refs))

    def sq(sec, src, txt=None, extra_=()):
        """A statement of one prose span: ``src`` is the .qmd source of the span, ``txt`` the statement
        (the span itself where it reads on its own). ``extra_`` cites further ``(section, source)``
        spans a paraphrase draws on."""
        st(t(txt) if txt else q(src), [ref(sec, q(src))] + [ref(s, q(x)) for s, x in extra_])

    # Purpose and scope
    sq("purpose", "The A-Mab drug substance process is being transferred from the development site in `{python} SENDING_LOCATION`, to the commercial drug substance site in `{python} RECEIVING_LOCATION`, under the Process Transfer Plan PTP-001.")
    sq("purpose", "Stage 1 process characterization supports that transfer by establishing which process parameters affect product quality and by defining the ranges within which the commercial process may be operated",
       "Stage 1 process characterization supports the transfer by establishing which process parameters affect product quality and by defining the ranges within which the commercial process may be operated.")
    st(f"PCP-009 describes the characterization study for Step {G.VFSTEP}, the small virus retentive "
       f"filtration step, the dedicated small virus removal operation and the principal source of MVM "
       f"clearance.", [ref("purpose", q_scope), ref("purpose", q_role)])
    sq("purpose", """The commercial process runs at a production bioreactor scale of `{python} f"{V['commercial_scale_l']:,}"` L.""")
    sq("purpose", "Its clearance is orthogonal to the two other viral safety steps, low pH inactivation (Step 6) and anion exchange chromatography (Step 8), because it removes virus by size rather than by inactivation or by binding",
       "The clearance of the step is orthogonal to the two other viral safety steps, low pH inactivation and anion exchange chromatography, because it removes virus by size rather than by inactivation or by binding.")
    st(t("The study covers the `{python} k_fac` process parameters of the step, `{python} vol` and `{python} prs`."),
       [ref("purpose", q("The study covers the `{python} k_fac` process parameters of the step.")),
        ref("purpose", q("They are `{python} vol`, the volume of load filtered per square metre of membrane, and `{python} prs`."))])
    st(q_resp, [ref("purpose", q_resp)])
    sq("purpose", "The study will be executed on a qualified scale-down model, on load material representative of the anion exchange pool that feeds the step at commercial scale.")
    sq("purpose", "Version 2.0 of this plan is an amendment issued after the studies of this step had run",
       "Version 2.0 of PCP-009 is an amendment issued after the studies of the step had run.")
    # Changes in this revision
    sq("changes", "Version 1.0 of this plan was approved on `{python} V1_APPROVED`, before the first study of the step began on `{python} first_start`.",
       "Version 1.0 of PCP-009 was approved on `{python} V1_APPROVED`, before the first study of the step began on `{python} first_start`.")
    sq("changes", "Version 2.0 replaces it and is issued under the investigation INV-001.",
       "Version 2.0 replaces Version 1.0 and is issued under the investigation INV-001.")
    sq("changes", "Quality Assurance opened INV-001 on `{python} INV_OPEN` after its review of the master report PCMR-001 Version 1.0 for readiness of the Biologics License Application, and closed it on `{python} INV_CLOSE` with the classification `{python} INV_CLASS`.")
    sq("changes", "INV-001 found that the criteria used to judge each step in the proven acceptable range (PAR) analysis had been set after the data were seen and were in no approved protocol (finding 1).")
    sq("changes", "Its corrective action CA2 amends each step plan with the criteria and the fragment method of the master plan PCMP-001 Version 2.0.",
       "Corrective action CA2 of INV-001 amends each step plan with the criteria and the fragment method of the master plan PCMP-001 Version 2.0.")
    sq("changes", "PCR-009 applies its corrective actions, the model selection for every response-surface output and the refit of the models below the adequacy criteria.",
       "PCR-009 applies the corrective actions of INV-002: the model selection for every response-surface output and the refit of the models below the adequacy criteria.",
       extra_=[("changes", "The revision history also names INV-002, the investigation of the response-surface models that fell below the model-adequacy criteria of PCMP-001 §7.2.")])
    sq("changes", "The design, the sampling, the spiking and the decision rules of Version 1.0 are kept word for word where the changes below do not replace them.",
       "The design, the sampling, the spiking and the decision rules of Version 1.0 are kept word for word where the changes of Version 2.0 do not replace them.")
    sq("changes", "Each output with a criterion is judged against the intermediate acceptance criterion (IAC) that PCMP-001 §7.3 and §7.4 derive for it",
       "Each output of the step with a criterion is judged against the intermediate acceptance criterion (IAC) that PCMP-001 §7.3 and §7.4 derive for it.")
    sq("changes", "The MVM LRF and the XMuLV LRF are each held to the platform claim of this step, `{python} f2(c_mvm)` log10.")
    sq("changes", "Version 1.0 judged them against the nominal log reduction of the step less `{python} f2(v1_allow)` log10 for assay variability, which gave `{python} f2(r1_mvm)` for MVM and `{python} f2(r1_xmulv)` for XMuLV.",
       "Version 1.0 judged the two LRF against the nominal log reduction of the step less `{python} f2(v1_allow)` log10 for assay variability, `{python} f2(r1_mvm)` for MVM and `{python} f2(r1_xmulv)` for XMuLV.")
    sq("changes", "These limits were written into the compiled text of Version 1.0 when the package was compiled, and they were not approved with the plan (INV-001 finding 1).",
       "The Version 1.0 limits for the two LRF were written into the compiled text of Version 1.0 when the package was compiled and were not approved with the plan (INV-001 finding 1).")
    sq("changes", "Both Version 2.0 criteria are lower than these limits.",
       "Both Version 2.0 LRF criteria are lower than the Version 1.0 limits.")
    sq("changes", "The compiled text also quoted a floor for each virus, the cumulative requirement less the nominal clearance of the other steps (`{python} f2(floor_m)` for MVM and `{python} f2(floor_x)` for XMuLV), to show the margin of the cumulative claim.")
    sq("changes", "PCMP-001 §7.4 replaces the floor with a check that the platform claims of the steps sum to the cumulative requirement",
       "PCMP-001 §7.4 replaces the floor with a check that the platform claims of the steps sum to the cumulative requirement.")
    sq("changes", "Fragments are added as an output, with the drug substance criterion of ≤ `{python} f2(c_frag)` %, because no step after this one changes them.")
    sq("changes", "They enter the objectives, the operating range, the design space and the proven acceptable ranges in the same way as the two LRF.",
       "Fragments enter the objectives, the operating range, the design space and the proven acceptable ranges in the same way as the two LRF.")
    st(t("Fragments are measured by nrCE-SDS, the method that the analytical method decision AMD-001 set for every study at every step from `{python} AMD_DATE`; both designs of the step started after that date."),
       [ref("changes", q("Fragments are measured by non-reduced capillary electrophoresis with sodium dodecyl sulfate (nrCE-SDS).")),
        ref("changes", q("This method was set for every study at every step from `{python} AMD_DATE` by the analytical method decision AMD-001 (PCMP-001 §7.8), and both designs of the step started after that date"))])
    sq("changes", "Version 1.0 did not assess fragments at this step.")
    sq("changes", "The model is qualified by its offset from manufacturing scale (PCMP-001 §7.1).",
       "The scale-down model is qualified by its offset from manufacturing scale (PCMP-001 §7.1).")
    sq("changes", 'This replaces the Version 1.0 acceptance test, "The model will be accepted where no statistically significant difference is found between the scales in yield or in flux decay at the end of the load."',
       "Qualification by offset replaces the Version 1.0 acceptance test of no statistically significant difference between the scales in yield or in flux decay at the end of the load.")
    sq("changes", "so PCMP-001 §7.1 also replaces three Version 1.0 rules that made the qualification a gate.",
       "PCMP-001 §7.1 replaces three Version 1.0 rules that made the qualification of the scale-down model a gate, among them the rule that the screening runs would not begin until the acceptance test had been met.",
       extra_=[("changes", "The first is the rule that the screening runs would not begin until the acceptance test had been met.")])
    sq("changes", "The outputs that Version 1.0 compares at both scales, the flux decay profile, the step yield and the post-use integrity test result, are kept.")
    sq("changes", "The Version 1.0 conditions for accepting a fitted model as predictive are kept",
       "The Version 1.0 conditions for accepting a fitted model as predictive are kept, and the adequacy criteria of PCMP-001 §7.2 are added.",
       extra_=[("changes", "The adequacy criteria of PCMP-001 §7.2 are added.")])
    sq("changes", 'The remedy of PCMP-001 §7.2 replaces the Version 1.0 consequence, "Where a model fails these checks, the affected response will be reported descriptively and no range will be claimed from it."',
       "The remedy of PCMP-001 §7.2 replaces the Version 1.0 consequence that a response whose model fails the checks is reported descriptively and no range is claimed from it.")
    sq("changes", "The two LRF are judged at the worst case within the normal operating range (NOR).",
       "The two LRF are judged at the worst case within the NOR: the mean predicted LRF at the least favourable combination of NOR low, set-point and NOR high of the other parameter (PCMP-001 §6.4).",
       extra_=[("changes", "That is the mean predicted LRF at the least favourable combination of NOR low, set-point and NOR high of the other parameter (PCMP-001 §6.4).")])
    sq("changes", "Fragments are judged on the `{python} pi_pct` % prediction interval of a single batch, which now includes the uncertainty of the fitted coefficients.")
    sq("changes", "Version 1.0 judged every output on the `{python} pi_pct` % prediction interval of the response from a Monte-Carlo simulation of the fitted model.")
    sq("changes", "A platform worst case is the lowest clearance fold or the largest increase seen on the platform for a step, from which a criterion upstream of that step was derived.")
    sq("changes", "The record now gives the execution window of each study of the step",
       "The record now gives the execution window of each study of the step, which the Version 1.0 records did not (INV-001 finding 5).",
       extra_=[("changes", "which the Version 1.0 records did not (INV-001 finding 5).")])
    sq("changes", "The compiled text of Version 1.0 carried `{python} V1_REPORTS`, the date on which the Version 1.0 reports were approved, in its title block in place of the date on which this plan was approved.",
       "The compiled text of Version 1.0 carried `{python} V1_REPORTS`, the approval date of the Version 1.0 reports, in its title block in place of the approval date of the plan.")
    sq("changes", "It also carried the step criteria that had been set at analysis, added to the plan text when the package was compiled, without a revision of the approved plan (INV-001 finding 1).",
       "The compiled text of Version 1.0 also carried the step criteria set at analysis, added to the plan text when the package was compiled, without a revision of the approved plan (INV-001 finding 1).")
    sq("changes", "The design space is drawn on the statistic of PCMP-001 §6.2, the single-batch limit for fragments and the mean for viral clearance",
       "The design space is drawn on the statistic of PCMP-001 §6.2, the single-batch limit for fragments and the mean for viral clearance; Version 1.0 drew the operating region and the design space on the mean predictions of the response-surface model.",
       extra_=[("changes", "Version 1.0 drew the operating region and the design space on the predictions of the response-surface model, which are mean values.")])
    sq("changes", "Under it a parameter affects an attribute when a term that contains the parameter is significant (§6.2), and the class of an affected parameter follows from the size of its effect across its PAR and from the margin between the PAR and the NOR (§7.7).",
       "The Version 1.0 classification rule is kept word for word, and under the rule of PCMP-001 Version 2.0 that is added, a parameter affects an attribute when a term that contains it is significant (§6.2), and the class of an affected parameter follows from the size of its effect across its PAR and the margin between the PAR and the NOR (§7.7).",
       extra_=[("changes", "Classification. The Version 1.0 rule is kept word for word.")])
    sq("changes", "Version 1.0 judged the risk of operating outside the design space from the control capability of the commercial equipment.")
    sq("changes", "The centre points of the screening design do detect curvature, although they cannot attribute it to a factor",
       "Version 2.0 corrects the Version 1.0 statement that a two-level design carries no estimate of curvature: the centre points of the screening design detect curvature, although they cannot attribute it to a factor.",
       extra_=[("changes", "Version 1.0 stated that a two-level design carries no estimate of curvature.")])
    sq("changes", "An integrity test bounds only the defects it can detect, so the sentence now says that such a membrane has no defect large enough for the test to detect",
       "An integrity test bounds only the defects it can detect, so a membrane that passes the post-use integrity test has no defect large enough for the test to detect; Version 1.0 said it has no pore large enough to pass a retrovirus.",
       extra_=[("changes", "Version 1.0 also stated that a membrane that passes the post-use integrity test has no pore large enough to pass a retrovirus.")])
    sq("changes", "The description of step yield now names the hold-up that the Version 1.0 expectation of a slowly falling yield rests on, the product held in the fouling layer, which grows with the volume filtered",
       "The description of step yield now names the hold-up that the expectation of a slowly falling yield rests on, the product held in the fouling layer, which grows with the volume filtered.")
    sq("changes", "The design is unchanged.", "The design of the study is unchanged at Version 2.0.")
    # Objectives
    sq("objectives", "Qualify a scale-down model of the small virus retentive filtration step, and show that it represents the commercial step for virus retention, for flux decay and for step yield.",
       "Objective: qualify a scale-down model of the small virus retentive filtration step and show that it represents the commercial step for virus retention, for flux decay and for step yield.")
    sq("objectives", "affect the two viral clearance responses and the step yield, in what direction and by how much.",
       "Objective: determine which of the parameters affect the two viral clearance responses and the step yield, in what direction and by how much.")
    sq("objectives", "Fit a response-surface model for each response over the characterization ranges, and establish whether it predicts the mean response adequately.",
       "Objective: fit a response-surface model for each response over the characterization ranges and establish whether it predicts the mean response adequately.")
    sq("objectives", "Derive a proven acceptable range for each parameter against each of the two viral clearance responses",
       "Objective: derive a proven acceptable range for each parameter against each of the two viral clearance responses.")
    sq("objectives", "Classify each parameter under SOP-4001 and define what the step contributes to the control strategy and to the modular viral clearance claim.",
       "Objective: classify each parameter under SOP-4001 and define what the step contributes to the control strategy and to the modular viral clearance claim.")
    sq("objectives", "Change 1 adds fragments to objectives 2 to 4, and change 3 sets how the scale-down model of objective 1 is qualified",
       "Fragments are added to the objectives on the parameter effects, the response-surface models and the proven acceptable ranges.")
    st("The screening design identifies the parameters that have an effect; the response-surface model is "
       "the predictive model, and every range claimed in PCR-009 will be derived from it.",
       [ref("objectives", q("The screening design identifies the parameters that have an effect.")),
        ref("objectives", q("The response-surface model is the predictive model, and every range claimed in PCR-009 will be derived from it."))])
    # Related documents
    sq("related", "The risk assessment RA-001 sets the study scope, PCP-009 plans the study and the report PCR-009 presents it, and PCR-009 rolls up into the master report PCMR-001",
       "RA-001 sets the study scope, PCP-009 plans the study, and PCR-009 presents it and rolls up into the master report PCMR-001.")
    st("The operation procedure SOP-2012 governs operation of the step and the pre-use and post-use "
       "integrity tests.",
       [ref("related", q("The operation procedure SOP-2012 governs operation of the step and the pre-use and post-use integrity tests")),
        ref("related", soprow["SOP-2012"], sop_t, soprow)])
    # Unit-operation description and prior knowledge
    sq("uo", "The membrane carries a pore size distribution chosen to retain the smallest viruses of concern, the parvoviruses, while the antibody passes through.",
       extra_=[("uo", "The step removes virus by size.")])
    sq("uo", "Retention is a sieving mechanism, so it depends on the integrity of the pore structure and on how the effective pore size of the membrane changes as it fouls over the course of a batch.")
    sq("uo", "MVM sits close to the pore size cut-off, and its retention depends on the fraction of pores at the large end of the distribution and on the flow through them.")
    sq("uo", "As the membrane fouls with product and with residual impurity, flux redistributes toward the least fouled and largest pores, and small virus can pass.")
    sq("uo", "XMuLV is many times larger than the pores.",
       "XMuLV is many times larger than the pores and is retained completely while the membrane is intact.",
       extra_=[("uo", "It is retained completely while the membrane is intact, and its clearance is insensitive to the operating parameters over any range that can be run.")])
    sq("uo", "Membrane integrity is confirmed after each batch by the post-use integrity test under the operation procedure SOP-2012, and a membrane that passes that test has no defect large enough for the test to detect.")
    sq("uo", "The antibody is small enough to pass the pores freely, so step yield is limited only by product held up in the fouling layer on the membrane and in the system.")
    sq("uo", "It has been used to manufacture three previously licensed humanized IgG1 antibodies, X-Mab, Y-Mab and Z-Mab, and to supply A-Mab clinical material, with the same filter type and the same mode of operation",
       "The step is a platform operation, used to manufacture X-Mab, Y-Mab and Z-Mab and to supply A-Mab clinical material, with the same filter type and the same mode of operation.",
       extra_=[("uo", "The step is a platform operation.")])
    sq("uo", "The mechanism of removal is size exclusion and does not depend on the identity of the antibody, so the platform experience justifies the ranges chosen",
       "The mechanism of removal is size exclusion and does not depend on the identity of the antibody, so the platform experience justifies the ranges chosen.")
    sq("uo", "The material presented to the filter is the anion exchange flow-through pool of the A-Mab process, and how that pool fouls the membrane is specific to the product, so the maximum load and the pressure range will be established on A-Mab material.")
    # Quality attributes in scope
    sq("cqa", "both of which are cumulative requirements on the drug substance and are met by several steps together.",
       "The two viral safety attributes to which the step contributes log reduction are cumulative requirements on the drug substance and are met by several steps together.")
    st("The filtrate pool of the step is judged against the drug substance criterion for fragments.",
       [ref("cqa", q_out)])
    sq("cqa", "Both viral safety attributes are of very high criticality, and the risk they carry is patient safety rather than efficacy.",
       extra_=[("cqa", "This criticality was assigned by rule, because a viral contamination would directly harm the patient (master plan PCMP-001 §3).")])
    sq("cqa", "MVM is the harder of the two for this step.",
       "MVM is the harder of the two viruses for this step; the cumulative MVM requirement rests on the claims of anion exchange chromatography and of this step alone (PCMP-001 §7.4).",
       extra_=[("cqa", "The cumulative MVM requirement therefore rests on the claims of anion exchange chromatography and of this step alone (PCMP-001 §7.4).")])
    sq("cqa", "They are formed in culture and during the harvest hold, by proteases released from lysed cells, and the register assigns them to harvest (PCMP-001 §3).",
       "Fragments are of low criticality; they are formed in culture and during the harvest hold, by proteases released from lysed cells, and the register assigns them to harvest (PCMP-001 §3).",
       extra_=[("cqa", "Fragments are of low criticality.")])
    # Risk-based prioritization of parameters
    sq("risk", "The risk assessment RA-001 ranked the parameters of every unit operation twice, once for the potential impact of the parameter on quality attributes and once for its potential to interact with other parameters",
       "RA-001 ranked the parameters of every unit operation twice, once for their potential impact on quality attributes and once for their potential to interact with other parameters.")
    sq("risk", "Parameters scoring high on either ranking were assigned to multivariate study, parameters scoring lower were assigned to univariate study, and parameters supported by platform knowledge alone were assigned to neither.")
    sq("risk", "For this step the assessment placed `{python} n_multi` parameters in the multivariate group and `{python} n_uni` in the univariate group.")
    sq("risk", "The `{python} vol` decides how much of the membrane is still open and pressure decides how fast the filtrate crosses what is left, so the fall in MVM retention with load is expected to be steeper at the top of the pressure range than at the bottom.",
       "An interaction of `{python} vol` and `{python} prs` on MVM retention is expected: the fall in retention with load is expected to be steeper at the top of the pressure range than at the bottom, and the designs must be able to estimate it.",
       extra_=[("risk", "The designs must be able to estimate that interaction.")])
    sq("risk", "No parameter of this step was left out of the study on the basis of prior knowledge alone.")
    sq("risk", "The risk assessment recorded that the platform claim for this step is a viral safety claim, and that a claim of that kind should be supported by product specific data even where the mechanism is well understood.")
    # Scale-down model and its qualification
    sq("sdm", "The model is scaled on membrane area, so that the volumetric load in `{python} u_vol`, the transmembrane pressure and the flux per unit area are the same as at commercial scale.")
    st("Load material, filtration temperature and the hold-up volume per unit area are matched to the "
       "commercial step, because the pool fouls the membrane, temperature sets the viscosity and the flux, "
       "and the hold-up limits the step yield.",
       [ref("sdm", q("Load material will be matched because the product and the residual impurity the pool carries are what foul the membrane, and a cleaner pool fouls it more slowly.")),
        ref("sdm", q("Filtration temperature will be matched because a higher temperature lowers the viscosity of the pool and raises the flux at a given pressure.")),
        ref("sdm", q("The hold-up volume per unit area will be matched because it fixes how much product is left wetting the membrane and the tubing at the end of a run, which is what limits the step yield."))])
    st(t("The qualification study `{python} ID_SDM` follows the scale-down model procedure SOP-1001."),
       [ref("sdm", q("Qualification will follow the scale-down model procedure SOP-1001, in study `{python} ID_SDM`.")),
        ref("related", soprow["SOP-1001"], sop_t, soprow)])
    sq("sdm", "The offset of an output is the mean of the scale-down runs at set-point minus the mean of the manufacturing-scale batches, reported with its two-sided `{python} off_ci` % confidence interval, each end of which is a one-sided `{python} off_one` % confidence bound.",
       extra_=[("sdm", "The model is qualified by the offset rule of the master plan PCMP-001 (§7.1).")])
    sq("sdm", "The model is qualified for an output when the conclusion against its criterion over the NOR is the same with the offset at either end of that interval.",
       "The scale-down model is qualified for an output when the conclusion against its criterion over the NOR is the same with the offset at either end of its confidence interval.")
    sq("sdm", "Step yield and flux decay have no criterion at this step, so their offsets are recorded and no conclusion depends on them.",
       extra_=[("sdm", "An output with no criterion at the step has its offset recorded only.")])
    sq("sdm", "The qualification runs are made, and the offsets estimated, before the first screening run.")
    sq("sdm", "The decision whether the model is qualified for an output is made at analysis, because it needs the response-surface model of the step.")
    sq("sdm", "Virus cannot be spiked into a manufacturing batch, so every clearance figure claimed for this step comes from the scale-down model",
       "Virus cannot be spiked into a manufacturing batch, so every clearance figure claimed for the step comes from the scale-down model.")
    sq("sdm", "Under PCMP-001 §7.1 the representativeness of the log reductions rests on the spiking model described above, and that of the fragment result on the mechanism of the step",
       "Under PCMP-001 §7.1 the representativeness of the log reductions rests on the spiking model, and that of the fragment result on the mechanism of the step.")
    for o, row in sdmrow.items():
        r = sdm_df[sdm_df["Output"] == o].iloc[0]
        if _nomark(r["Compared at both scales"]) == "No":
            txt = (f"{o} is not compared at both scales. It is judged against {r['Criterion']}, and its "
                   f"basis at manufacturing scale is the {_nomark(r['Basis at manufacturing scale']).lower()}.")
        else:
            txt = (f"{o} is compared at both scales and has no criterion at the step, so its offset is "
                   f"recorded only.")
        st(txt, [ref("sdm", row, sdm_t, sdmrow)])
    sq("sdm", "The qualification will be repeated if the membrane type, the filtration temperature or the composition of the load material changes, and PCR-009 will state the qualification result before it reports any log reduction.")
    # Operation
    sq("operation", "Each run will be operated at constant transmembrane pressure to the volumetric load set by the design point, and the filtrate will be collected in fractions across the load.")
    sq("operation", "Before each run the filter will be wetted and its integrity tested, and after each run the post-use integrity test will be performed, both under SOP-2012.")
    sq("operation", "A run whose post-use integrity test fails will be excluded from the analysis and recorded as a deviation, because a failed integrity test means the membrane was not intact and the log reduction measured across it says nothing about the step.")
    sq("operation", "Each design point will be executed once, with both model viruses spiked into the load before filtration.")
    sq("operation", "Step yield will be determined from the same run by protein mass balance, from the ultraviolet absorbance of the load and of the pooled filtrate.")
    sq("operation", "Runs will be executed in randomized order within each design.")
    sq("operation", "Filtration will be continuous.", "Filtration in the study runs is continuous.")
    # Analytical methods
    sq("analytical", "The log reduction factor of a run is the base ten logarithm of the total virus in the spiked load divided by the total virus in the filtrate, with both totals taken over the volume actually filtered.")
    sq("analytical", "Cytotoxicity and interference controls will be run for the load matrix and the filtrate matrix, and a spike recovery control will be run for each virus stock",
       "Cytotoxicity and interference controls will be run for the load matrix and the filtrate matrix, and a spike recovery control for each virus stock.")
    sq("analytical", "Where no virus is detected in the filtrate, the titre will be reported at the limit of detection of the assay and the log reduction reported as a lower bound rather than as a point value.")
    # Sampling plan
    sq("sampling", "Samples will be taken from the load before spiking, from the spiked load, and from the filtrate.",
       extra_=[("sampling", "The filtrate will be sampled as sequential fractions across the volumetric load and as a pool at the end of the run.")])
    sq("sampling", "Fractionating the filtrate allows the log reduction to be resolved against the volume filtered within a single run, which is the variable that degrades MVM retention as the membrane fouls.")
    sq("sampling", "Each spiked load sample and each filtrate sample will be assayed for both model viruses.")
    sq("sampling", "The unspiked load and the unspiked filtrate pool will be assayed for protein concentration for the yield calculation.")
    sq("sampling", "Every sample will be identified by run number and by the volumetric load at which it was taken, and the identity will be recorded at the time of sampling.")
    # Statistical methods
    sq("stats", "Effects will be reported as the change in the response over half the characterization range.")
    sq("stats", "The screening design will be analysed with a model carrying both main effects and their interaction.")
    sq("stats", "The response-surface design will be analysed with the full quadratic model in both factors",
       "The response-surface design will be analysed with the full quadratic model in both factors.")
    sq("stats", "Coefficients will be reported with their standard errors and p-values, and effects significant at α = `{python} g(a_eff)` will be treated as real.")
    sq("stats", "The lack of fit will be tested against the pure error estimated from the centre point replicates.")
    sq("stats", "The centre point replicates also give the reproducibility of each response, which will be reported as a coefficient of variation and used as the pure error term.")
    sq("stats", "These are the adjusted and the predicted R², the model F-test, a regression of the absolute residuals on the predicted value and of the residuals on run order, and Cook's distance for each run",
       "For the adequacy criteria of PCMP-001 §7.2 the analysis adds the adjusted and the predicted R², the model F-test, a regression of the absolute residuals on the predicted value and of the residuals on run order, and Cook's distance for each run.",
       extra_=[("stats", "Change 4 adds the statistics that the adequacy criteria of PCMP-001 §7.2 need.")])
    sq("stats", "Fragments are judged against their criterion on the prediction interval of a single batch, because the criterion applies to each batch.")
    sq("stats", "The two LRF are judged on the mean predicted LRF at the least favourable combination of NOR low, set-point and NOR high of the other parameter, because viral clearance is validated at worst-case conditions (PCMP-001 §6.4).")
    sq("stats", "Every judgement against a criterion is stated at manufacturing scale (PCMP-001 §7.1).",
       "Every judgement against a criterion is stated at manufacturing scale (PCMP-001 §7.1), and at this step no output with a criterion has a measured offset.",
       extra_=[("stats", "At this step no output with a criterion has a measured offset.")])
    st("Analyses will be performed under the design of experiments procedure SOP-1002.",
       [ref("stats", q("Analyses will be performed under the design of experiments procedure SOP-1002.")),
        ref("related", soprow["SOP-1002"], sop_t, soprow)])
    sq("stats", "The analysis will be run from a script under version control with a fixed random seed, so that every number in PCR-009 can be regenerated from the raw data.")
    # Factors, ranges and study type
    sq("factors", "The set-points and the NOR are those the studies were planned against, and neither was changed at Version 2.0.")
    sq("factors", "The characterization range for the `{python} vol` runs from the lower NOR edge to `{python} g(FV.prange[1])` `{python} u_vol`, which lies above the upper NOR edge of `{python} g(FV.nor[1])` `{python} u_vol`.")
    sq("factors", "The range was widened upward only, because MVM retention falls as the volumetric load rises and holds steady below the set-point.",
       "The range of the `{python} vol` was widened upward only, because MVM retention falls as the volumetric load rises and holds steady below the set-point.",
       extra_=[("factors", "The edge of acceptable performance therefore lies above the NOR and not below it, and a range extended downward would consume runs where nothing changes.")])
    sq("factors", "The pressure range runs from `{python} g(FP.prange[0])` to `{python} g(FP.prange[1])` `{python} u_prs` and is widened on both sides of the NOR of `{python} g(FP.nor[0])` to `{python} g(FP.nor[1])` `{python} u_prs`.")
    sq("factors", "Low pressures are included because a low transmembrane pressure allows retained virus to diffuse through the pore structure.")
    sq("factors", "Both edges are reachable by the commercial equipment, so a range that covers them supports the deviation assessment as well as the operating limits.")
    sq("factors", "Both characterization ranges extend further above the NOR than below it.")
    st(t("Both parameters, `{python} vol` and `{python} prs`, will be studied multivariately."),
       [ref("factors", q_multi)])
    # Screening design
    sq("screening", "With `{python} k_fac` factors the full factorial is executed, so both main effects and the interaction are estimated free of aliasing.")
    sq("screening", "The centre points detect curvature but cannot attribute it to a factor, and curvature is resolved at the response-surface stage.")
    sq("screening", "The interaction model also leaves `{python} df_lof_scr` degree of freedom for lack of fit, so its fit statistics overstate how well it fits (PCMP-001 §6.2).",
       "The screening interaction model leaves `{python} df_lof_scr` degree of freedom for lack of fit, so its fit statistics overstate how well it fits (PCMP-001 §6.2).")
    sq("screening", "The screening runs establish the size and direction of the two effects, and the reproducibility of the infectivity assays from the centre point replicates, before the response-surface runs are committed.")
    # Response-surface design
    sq("rsm", "The axial points sit on the edges of the characterization ranges rather than beyond them.",
       "The axial points of the response-surface design sit on the edges of the characterization ranges rather than beyond them, because settings outside the ranges are not settings the step may be claimed for.",
       extra_=[("rsm", "are not settings the step may be claimed for, so the face-centred form is used.")])
    sq("rsm", "The design supports the full quadratic model, which allows the response to curve against the volumetric load.",
       "The response-surface design supports the full quadratic model, which allows the response to curve against the volumetric load.")
    sq("rsm", "Curvature is expected there, because the flux redistribution that lets small virus through accelerates as the membrane fouls, and a model that could only fit a straight line would over-predict retention at the top of the range.",
       "Curvature against the volumetric load is expected, because the flux redistribution that lets small virus through accelerates as the membrane fouls, and a straight-line model would over-predict retention at the top of the range.")
    sq("rsm", "The `{python} cp_rsm` replicates of the centre point give the pure error term for the lack of fit test",
       "The `{python} cp_rsm` replicates of the centre point of the response-surface design give the pure error term for the lack of fit test and an estimate of run to run reproducibility that does not depend on the model.",
       extra_=[("rsm", "and an estimate of run to run reproducibility that does not depend on the model.")])
    # Univariate assessment
    sq("univariate", "are factors of the two designs above, and the remaining operating variables of the step are held at their set-points under SOP-2012 and are supported by platform experience.",
       "Both parameters are factors of the two designs, and the remaining operating variables of the step are held at their set-points under SOP-2012 and are supported by platform experience.")
    sq("univariate", "Where the study finds an effect that the two designs cannot separate, a univariate confirmation run may be added.",
       extra_=[("univariate", "Any such run will be justified against the data that prompted it and reported in PCR-009 with the same acceptance criteria as the designed runs.")])
    # Acceptance and decision criteria
    sq("criteria", "A fitted response-surface model will be accepted as predictive where the lack of fit test is not significant at α = `{python} g(a_lof)` against the pure error from the centre point replicates, where the residuals show no trend against the predicted value and no material departure from normality, and where the residual standard error is small against the distance between the predicted response and its criterion.",
       extra_=[("criteria", "The following rule of Version 1.0 for the fitted models is kept.")])
    sq("criteria", "The model F-test is significant at α = `{python} g(a_eff)`, the level set for model terms.",
       "Adequacy criterion 1 of PCMP-001 §7.2: the model F-test is significant at α = `{python} g(a_eff)`, the level set for model terms.",
       extra_=[("criteria", "Change 4 adds the four adequacy criteria of the master plan PCMP-001 (§7.2), which a model must also meet.")])
    sq("criteria", "Lack of fit against pure error is not significant at α = `{python} g(a_lof)`.",
       "Adequacy criterion 2 of PCMP-001 §7.2: lack of fit against pure error is not significant at α = `{python} g(a_lof)`.")
    sq("criteria", "Predicted R² falls short of R² by no more than `{python} f2(gap)`.",
       "Adequacy criterion 3 of PCMP-001 §7.2, the limit on overfitting: predicted R² falls short of R² by no more than `{python} f2(gap)`.",
       extra_=[("criteria", "A model that fits its own runs much better than it predicts left-out runs has more terms than the data support.")])
    sq("criteria", "The absolute residuals are regressed on the predicted value, and the residuals on run order, each at α = `{python} g(a_res)`, and a significant slope counts as a pattern.",
       "Adequacy criterion 4 of PCMP-001 §7.2: the residuals show no pattern against predicted values or run order, tested by regressing the absolute residuals on the predicted value and the residuals on run order, each at α = `{python} g(a_res)`.",
       extra_=[("criteria", "The residuals show no pattern against predicted values or run order, and no single run dominates the fit.")])
    sq("criteria", "A run whose Cook's distance exceeds `{python} g(cook_k)`/n, a conventional cut-off where n is the number of runs, dominates the fit.")
    sq("criteria", "A model that fails the lack-of-fit test or the limit on overfitting is either refitted with a justified change of terms or transformation, or it is not used to set a range.",
       extra_=[("changes", "A model that fails the lack-of-fit test or the limit on overfitting is now either refitted with a justified change of terms or transformation, or it is not used to set a range.")])
    sq("criteria", "Where no adequate model results, PCR-009 should report the response descriptively, against the criterion, over the runs of the design (PCMP-001 §7.2).")
    sq("criteria", "The two LRF are each held to the platform claim of the step, `{python} f2(c_mvm)` log10, the log reduction that the step delivered on the platform with X-Mab, Y-Mab and Z-Mab (PCMP-001 §7.4).")
    sq("criteria", "For each virus, the claims of the steps that clear it are summed and checked against the cumulative requirement of the drug substance.")
    sq("criteria", "For XMuLV the claims of low pH inactivation, anion exchange and this step sum to `{python} f2(sum_x)` log10 against a requirement of `{python} g(req_x)`.")
    sq("criteria", "For MVM the claims of anion exchange and this step sum to `{python} f2(sum_m)` against `{python} g(req_m)`.",
       "For MVM the claims of anion exchange and this step sum to `{python} f2(sum_m)` log10 against a requirement of `{python} g(req_m)`: this step claims `{python} f2(c_mvm)` and anion exchange `{python} f2(aex_m)`.",
       extra_=[("criteria", "Of that sum, this step claims `{python} f2(c_mvm)` and anion exchange `{python} f2(aex_m)`.")])
    sq("criteria", "Each step is judged against its own claim, so a shortfall at this step is not made up by another step.")
    for key, row in irow.items():
        x = iac.loc[key]
        c = T.crit(x["iac_low"], x["iac_high"], x["spec_type"])
        how = (f"is the platform claim of the step: {c}." if x["basis"] == "platform claim"
               else f"is the drug substance criterion, because no downstream step changes it: {c}."
               if x["basis"] == "drug substance"
               else f"is the drug substance criterion carried back through the downstream steps: {c}.")
        st(f"The intermediate acceptance criterion for {names[key]} at the small virus retentive filtration "
           f"step " + how, [ref("criteria", row, iac_t, irow)])
    sq("criteria", "Fragments carry the drug substance criterion, because no step after this one changes them.",
       "Fragments carry the drug substance criterion, because no step after this one changes them, and are judged on nrCE-SDS results only (PCMP-001 §7.8).",
       extra_=[("criteria", "They are judged on nrCE-SDS results only (PCMP-001 §7.8).")])
    sq("criteria", "It will be reported with the operating region and used to show what the region costs in product, and no acceptance decision will rest on it.",
       "Step yield carries no criterion; it will be reported with the operating region to show what the region costs in product, and no acceptance decision will rest on it.",
       extra_=[("criteria", "Step yield carries no criterion.")])
    sq("criteria", "Their derivation uses no result of these studies, because the platform claims come from the platform history and the fragment criterion is the drug substance criterion (PCMP-001 §7.3).",
       "The criteria were issued after the studies of the step had run, and their derivation uses no result of these studies, because the platform claims come from the platform history and the fragment criterion is the drug substance criterion (PCMP-001 §7.3).",
       extra_=[("criteria", "The criteria were issued after the studies of this step had run.")])
    sq("criteria", "Each report checks the platform worst cases of its own step on which criteria upstream rely (PCMP-001 §7.5).")
    sq("criteria", "Where the A-Mab worst case predicted within the NOR is worse than the platform worst case, the one-sided `{python} ver_pct` % prediction bound of a single batch replaces the platform value, and the criteria upstream become stricter.")
    sq("criteria", "Where that bound is better than the platform value, it replaces the platform value only if the response-surface model behind it meets the first three adequacy criteria of PCMP-001 §7.2 (a significant model, no significant lack of fit and the limit on overfitting) and is not an exact fit.",
       "Where the prediction bound is better than the platform value, it replaces the platform value, and the criteria upstream become wider, only if the response-surface model behind it meets the first three adequacy criteria of PCMP-001 §7.2 and is not an exact fit.",
       extra_=[("criteria", "The criteria upstream then become wider.")])
    sq("criteria", "The fourth criterion, on the residuals and on influential runs, does not decide the change, and the report that gives the bound examines it and states whether the bound depends on a single run.")
    sq("criteria", "The criteria in force for this step equal their a priori values",
       "The criteria in force for the step equal their a priori values.")
    sq("criteria", "An operating range for a parameter will be declared where the response-surface model predicts that both viral clearance responses meet their criteria across that range.")
    sq("criteria", "The design space for the step is the part of the characterized region where both viral clearance responses meet their criteria at the same time, and PCR-009 will report its size from the fitted models rather than assert that it is the whole characterized region.",
       extra_=[("criteria", "Fragments enter the operating range and the design space in the same way (change 1).")])
    sq("criteria", "Under change 8 a setting of the two parameters lies inside the design space when fragments meet their criterion at both ends of the `{python} pi_pct` % prediction interval of a single run, and each LRF meets its claim on its mean prediction (PCMP-001 §6.2).",
       "A setting of the two parameters lies inside the design space when fragments meet their criterion at both ends of the `{python} pi_pct` % prediction interval of a single run, and each LRF meets its claim on its mean prediction (PCMP-001 §6.2).")
    sq("criteria", "A parameter with a proven acceptable range for several outputs carries the intersection of the ranges into the control strategy (PCMP-001 §7.6).")
    st("Each parameter will be classified under SOP-4001 from the outcome of the study.",
       [ref("criteria", q("Each parameter will be classified under SOP-4001 from the outcome of the study.")),
        ref("related", soprow["SOP-4001"], sop_t, soprow)])
    sq("criteria", "A parameter whose variability affects a critical quality attribute will be classified as a CPP, or as a WC-CPP where the risk of operating outside the design space is low given the control capability of the commercial equipment.")
    sq("criteria", "A parameter that affects process performance but no quality attribute will be classified as a KPP, and a parameter with neither effect as a GPP",
       "A parameter that affects process performance but no quality attribute will be classified as a KPP, and a parameter with neither effect as a GPP.")
    sq("criteria", "Under change 9 an attribute is affected by a parameter when a term that contains the parameter is significant at α = `{python} g(a_eff)` (PCMP-001 §6.2).",
       "An attribute is affected by a parameter when a term that contains the parameter is significant at α = `{python} g(a_eff)` (PCMP-001 §6.2), and the class of an affected parameter is decided on the size of its effect across its PAR and on the margin between the PAR and the NOR (PCMP-001 §7.7).",
       extra_=[("criteria", "The class of an affected parameter is then decided on the size of its effect across its PAR and on the margin between the PAR and the NOR (PCMP-001 §7.7).")])
    sq("criteria", "The study will be considered successful where the scale-down model is qualified, both viral clearance models are accepted as predictive, and a proven acceptable range containing the NOR is established for each parameter against each of the two viral clearance responses.")
    sq("criteria", "Where no such range exists, PCR-009 will report the range that does exist and the operating limit that follows from it.")
    sq("criteria", 'Under PCMP-001 Version 2.0 fragments are judged in the same way (change 1), and PCR-009 states how it reads "the scale-down model is qualified" for this step, given the outputs that the qualification compares',
       "Under PCMP-001 Version 2.0 fragments are judged in the same way in the success criterion, and PCR-009 states how it reads that the scale-down model is qualified, given the outputs that the qualification compares.")
    # Proven acceptable ranges (planned analysis)
    sq("par", "A proven acceptable range is the range of a parameter over which the response meets its criterion, given a stated treatment of the other parameters",
       "A proven acceptable range is the range of a parameter over which the response meets its criterion, given a stated treatment of the other parameters.")
    sq("par", "Two analyses will be run for each parameter and each of the two viral clearance responses, and both will be reported.",
       "Two proven acceptable range analyses will be run for each parameter and each of the two viral clearance responses and for fragments, and both will be reported.",
       extra_=[("par", "Change 1 adds fragments to them.")])
    sq("par", "The first holds the other parameter at its set-point and scans the parameter of interest across its characterization range on a grid of `{python} D.PAR_GRID_SETPOINT` points, using the fitted response-surface model.",
       "The first proven acceptable range analysis holds the other parameter at its set-point and scans the parameter of interest across its characterization range on a grid of `{python} D.PAR_GRID_SETPOINT` points, using the fitted response-surface model.")
    sq("par", "It answers what the parameter may do while the rest of the step is operated at target.",
       "The first analysis answers what the parameter may do while the rest of the step is operated at target.")
    sq("par", "Its range is the contiguous interval around the set-point over which the mean prediction meets the criterion (PCMP-001 §6.4).",
       "The range of the first analysis is the contiguous interval around the set-point over which the mean prediction meets the criterion (PCMP-001 §6.4).")
    sq("par", "The second, the NOR-propagated analysis, scans the parameter of interest across its characterization range on a grid of `{python} D.PAR_GRID` points, as PCMP-001 §6.4 defines it.")
    sq("par", "For fragments, the analysis draws `{python} mc_n` values of the other parameter at each grid point from a normal distribution centred on its set-point, with a standard deviation of the NOR width divided by `{python} nor_sd`, clipped to the characterization range.",
       "For fragments, the NOR-propagated analysis draws `{python} mc_n` values of the other parameter at each grid point from a normal distribution centred on its set-point, with a standard deviation of the NOR width divided by `{python} nor_sd`, clipped to the characterization range; each draw carries the model residual and the uncertainty of the fitted coefficients.",
       extra_=[("par", "Each draw carries the model residual and the uncertainty of the fitted coefficients.")])
    sq("par", "The `{python} pi_pct` % prediction interval of a single batch runs from the `{python} lo_pct`th to the `{python} hi_pct`th percentile of the simulated batches, and its upper end must not exceed the criterion.")
    sq("par", "For the two LRF, the other parameter is set at each grid point to its NOR low, its set-point and its NOR high, and the lowest of the three mean predicted LRF must meet the claim of the step.",
       "In the NOR-propagated analysis of the two LRF, the other parameter is set at each grid point to its NOR low, its set-point and its NOR high, and the lowest of the three mean predicted LRF must meet the claim of the step.")
    sq("par", "Viral clearance is validated at worst-case conditions, so a claim that held only on average over the NOR would not support a validated log reduction.")
    sq("par", "Where the two analyses disagree, the range from the second is the one carried into the control strategy, because the commercial process holds each parameter somewhere within its normal operating range and not at its set-point.")
    sq("par", "The reported range in each case is the contiguous interval that contains the set-point.")
    sq("par", "Where the predicted response leaves acceptance inside the characterization range, the proven acceptable range is narrower than the range studied, and PCR-009 will state the value at which the response crosses its criterion.")
    sq("par", "Where an output does not meet its criterion even at the set-point, PCR-009 reports that no proven acceptable range exists for it and states the consequence for the NOR (PCMP-001 §7.6).")
    sq("par", "Each proven acceptable range will be reported with a plot of the response against the parameter, with the acceptance limit drawn, the acceptable region shaded green, and the set-point and the NOR marked.",
       extra_=[("par", "The two analyses will be shown as the two panels of one figure.")])
    # Data management and integrity
    sq("data", "Raw data will be recorded at the time of the activity, in the electronic laboratory notebook for the process runs and in the laboratory information management system for the analytical results.")
    sq("data", "Records will meet the ALCOA+ expectations, and the audit trails of both systems will be retained for the life of the application",
       "Records will meet the ALCOA+ expectations, and the audit trails of both systems will be retained for the life of the application.")
    sq("data", "The fitted models, the tables and the figures of PCR-009 will be generated from the exported data by a single reproducible run of the analysis script, and a second reviewer will confirm that the reported numbers come from that run.",
       extra_=[("data", "Analytical results will be transferred to the analysis by controlled file export.")])
    sq("data", "Any manual entry of a value into the analysis is a data integrity finding.")
    sq("data", "Each study record gives its execution window and the calibration status of any instrumented system it used, as INV-001 preventive action PA3 requires (PCMP-001 §5).")
    sq("data", "A deviation that invalidates a design point will be dispositioned before the affected runs are analysed, and where the disposition is to repeat the affected runs, the superseded data will be retained and referenced rather than deleted.",
       extra_=[("data", "Deviations from this plan will be recorded when they occur and reported in PCR-009 with their assessed impact on the study.")])
    # Roles and responsibilities
    sq("roles", "The receiving site reviews the ranges before they are fixed, because a range the commercial equipment cannot hold is of no use in the control strategy",
       "The receiving site reviews the ranges before they are fixed, because a range the commercial equipment cannot hold is of no use in the control strategy.")
    # Deliverables and schedule
    sq("schedule", "It will report the qualification of the scale-down model, the screening effects, the response-surface models with their diagnostics, the proven acceptable ranges, the design space of the step, the parameter classification and the contribution of the step to the control strategy and to the modular viral clearance claim.",
       "The deliverable of the study is PCR-009, which will report the qualification of the scale-down model, the screening effects, the response-surface models with their diagnostics, the proven acceptable ranges, the design space of the step, the parameter classification and the contribution of the step to the control strategy and to the modular viral clearance claim.",
       extra_=[("schedule", "The deliverable of the study is PCR-009.")])
    sq("schedule", "It will also tabulate the offsets of the step (PCMP-001 §7.1).",
       "PCR-009 will also tabulate the offsets of the step (PCMP-001 §7.1).")
    sq("schedule", "The study will be executed in four phases, in this order.",
       "The study will be executed in four phases, in order: the qualification of the scale-down model, the screening runs and their analysis, the response-surface runs and their analysis, and the proven acceptable range analysis, the classification and the report.",
       extra_=[("schedule", "Qualification of the scale-down model, against the criterion"),
               ("schedule", "The screening runs and their analysis."),
               ("schedule", "The response-surface runs and their analysis."),
               ("schedule", "The proven acceptable range analysis, the classification and the report.")])
    sq("schedule", "Version 1.0 fixed no calendar dates in advance",
       "Version 1.0 fixed no calendar dates in advance; the plan records the execution windows of the studies, as INV-001 preventive action PA3 requires.",
       extra_=[("schedule", "records the execution windows of the studies, as INV-001 preventive action PA3 requires.")])
    sq("schedule", "The studies of this step ran one after the other.",
       extra_=[("schedule", "A window runs from the first to the last day of runs of its study.")])
    # Risks and assumptions
    sq("risks", "The clearance claim for this step rests entirely on a scale-down model, because virus cannot be spiked at manufacturing scale.",
       "The clearance claim for the step rests entirely on a scale-down model, because virus cannot be spiked at manufacturing scale.")
    sq("risks", "The mitigation is to re-scale the model on membrane area and on hold-up volume and to repeat the qualification, and any change made to the model will be recorded in PCR-009.",
       "Against the reliance of the clearance claim on the scale-down model, the mitigation is to re-scale the model on membrane area and on hold-up volume and to repeat the qualification, and any change made to the model will be recorded in PCR-009.",
       extra_=[("risks", "The clearance claim for this step rests entirely on a scale-down model, because virus cannot be spiked at manufacturing scale.")])
    sq("risks", "A spike that fouls the membrane differently from unspiked process material would bias the measured log reduction, and the bias would be largest at the top of the volumetric range, which is the part of the range the claim depends on.",
       extra_=[("risks", "Spiking adds material to the load, and retention depends on how the membrane fouls.")])
    sq("risks", "The virus stock will therefore be clarified before addition and its volume kept small against the load volume, and the flux decay of the spiked runs will be compared with that of the unspiked qualification runs.",
       "The virus stock will be clarified before addition and its volume kept small against the load volume, and the flux decay of the spiked runs will be compared with that of the unspiked qualification runs.")
    sq("risks", "The log reduction that can be measured is bounded by the titre of the spiked load and by the limit of detection of the infectivity assay.")
    sq("risks", "The load will therefore be spiked to a titre that allows the criterion to be demonstrated with margin, and the achieved titre will be reported with each run.",
       "The load will be spiked to a titre that allows the criterion to be demonstrated with margin, and the achieved titre will be reported with each run.")
    sq("risks", "The study assumes that the anion exchange pool used in the runs represents commercial material.",
       extra_=[("risks", "Pool from a run that was itself out of trend will not be used, and the load material used in each filtration run will be identified in PCR-009.")])
    sq("risks", "The study assumes uninterrupted filtration", "The study assumes uninterrupted filtration.")
    sq("risks", "Material supply is the principal risk to the schedule.",
       "Material supply is the principal risk to the schedule: each design point consumes anion exchange pool, and the runs will be scheduled against pool availability.",
       extra_=[("risks", "Each design point consumes anion exchange pool, and the runs will be scheduled against pool availability rather than against a fixed calendar.")])
    # Approvals
    sq("approvals", "This plan takes effect when it has been approved by the functions listed in the approval record at the front of this document.",
       "PCP-009 takes effect when it has been approved by the functions listed in its approval record.")
    sq("approvals", "after approval requires a revision of this plan and re-approval before the affected runs are executed.",
       "A change to the factors, to the ranges or to the acceptance criteria after approval requires a revision of the plan and re-approval before the affected runs are executed; a change made after the affected runs have been executed will be reported in PCR-009 as a deviation from the plan.",
       extra_=[("approvals", "A change made after the affected runs have been executed will be reported in PCR-009 as a deviation from this plan.")])
    sq("approvals", "This revision was issued after the runs of this step, under corrective action CA2 of the investigation INV-001, which amends the step plans with the criteria and the fragment method",
       "Version 2.0 was issued after the runs of the step, under corrective action CA2 of INV-001, which amends the step plans with the criteria and the fragment method.")
    # Appendices
    sq("app_a", "and the coded levels −1, 0 and +1 correspond to the low edge, the midpoint and the high edge of each characterization range",
       "In the planned design matrices the coded levels −1, 0 and +1 correspond to the low edge, the midpoint and the high edge of each characterization range.")
    sq("app_a", "The executed matrices with their measured responses will appear in the appendices of PCR-009.")
    sq("app_b", "The axial runs carry one factor at an edge of its characterization range and the other at the midpoint, and the centre point is replicated `{python} cp_rsm` times.",
       "In the planned response-surface design the axial runs carry one factor at an edge of its characterization range and the other at the midpoint, and the centre point is replicated `{python} cp_rsm` times.")
    sq("app_b", "The execution order within each design will be randomized, so the run numbers in these tables identify the design point and not the sequence in which it will be run.")

    # ==== concepts ================================================================================
    concepts = [Concept(concept_id="step:virus_filtration", concept_type="PROCESS_STEP", canonical_name=UO_NAME,
                        aliases=["small virus retentive filtration", "virus filtration", P.DOC_REGISTRY[DOC][1],
                                 f"Step {G.VFSTEP}"],
                        review_status="human_verified")]
    alias = {pc_vol: [ns["vol"], "volumetric load"], pc_prs: [ns["prs"], "transmembrane pressure"]}
    concepts += [Concept(concept_id=PC[n], concept_type="PROCESS_PARAMETER", canonical_name=n,
                         aliases=alias[PC[n]], review_status="human_verified") for n in prow]
    concepts += G._attr_concepts(ckeys)
    concepts.append(Concept(concept_id="attr:step_yield", concept_type="PERFORMANCE_ATTRIBUTE",
                            canonical_name="Step yield", aliases=["step yield", "yield"],
                            review_status="human_verified"))
    title_of = dict(zip(sop_df["Reference"], sop_df["Title"]))
    concepts += [Concept(concept_id=f"method:{m.method_id}", concept_type="ANALYTICAL_METHOD",
                         canonical_name=title_of[m.method_id], aliases=[m.method_id, m.method_name],
                         review_status="human_verified") for m in methods]

    # ==== the annex ===============================================================================
    annex = S.GroundTruthAnnex(
        document_id=DOC, document_title=f"{P.DOC_REGISTRY[DOC][0]} — {P.DOC_REGISTRY[DOC][1]}",
        document_class=P.DOC_REGISTRY[DOC][0], **G.rev2_layer(DOC, FILE),
        schema_extensions_used=G.COMMON_EXT + G.REV2_EXT,
        out_of_schema_notes=[
            "Classification is a result of the study, so every parameter_type is 'unclassified'. No "
            "set-point or NOR of the step changed at Version 2.0 (the plan states it), so "
            "ProcessParameter.target_value and NOR are the values of the parameter table, which are also "
            "the values in force. ProcessParameter.PAR carries the range studied, as everywhere in the "
            "corpus; the plan claims no proven acceptable range. The parameter table no longer prints the "
            "study type: study_type comes from the plan's own parameter frame and is anchored on the "
            "sentence that states it. Each parameter is also anchored on its row of the coded factor "
            "legend.",
            "The step forms no quality attribute. The QualityAttribute records are the two cumulative viral "
            "clearance attributes, to which the step contributes log reduction, and fragments, against "
            "whose criterion its filtrate pool is judged; their acceptance_criteria are the drug substance "
            "criteria of the attribute table. The step criteria are attribute_has_acceptance_criterion "
            "assertions and statements on the rows of the intermediate acceptance criteria table.",
            "acceptance_criteria holds the rows of the criteria-change table: the Version 1.0 analysis "
            "limits of the two LRF (superseded) and the Version 2.0 criteria (in force); fragments had no "
            "Version 1.0 criterion. The two LRF are judged on the mean predicted LRF at the least favourable "
            "NOR combination of the other parameter, fragments per batch. The modular claim (the platform "
            "claims of the steps that clear each virus, summed against the cumulative requirement) is in "
            "statements.",
            "Step yield is a process performance response with no criterion; it is the concept "
            "attr:step_yield in the prior-knowledge assertion and in the study responses. The rows of the "
            "table of outputs carried to manufacturing scale are statements.",
            "The qualification study compares scale-down runs with manufacturing-scale batches, which is not "
            "a design, so its StudyDesign has no n_runs; the flux decay profile and the post-use integrity "
            "test result it also compares have no response key and are not listed as responses. The "
            "screening and response-surface StudyDesign records are anchored on every row of their planned "
            "design matrix (Appendices A and B); the four factorial rows read alike in both matrices.",
            "Each AnalyticalMethod record is anchored on its row of the methods table, on its row of the "
            "procedures table and on the sentences that name the method. The concept of a method carries "
            "the title of its validation as canonical name and the method of the methods table as alias.",
            "parameter_impacts_attribute and parameter_does_not_significantly_impact_attribute assertions are "
            "the plan's stated expectations from prior knowledge and the risk assessment, not results.",
            "The roles table and the abbreviations are not represented. No rhetorical_spans (a plan has no "
            "spans file). weak_claims is empty.",
        ] + G._unrendered_note(unrendered),
        inventory=G.rev2_inventory(DOC, FILE, "process_characterization_plan", UO_NAME,
                                   ["process characterization", "small virus retentive filtration",
                                    "viral clearance", "MVM and XMuLV log reduction", "protocol amendment",
                                    "intermediate acceptance criteria", "modular viral clearance claim",
                                    "scale-down offset", "spiking model", "design of experiments"]),
        entities=entities, studies=studies,
        report_sections=[ReportSection(section_id=f"{DOC}-summary", title="Plan summary", statements=ST)],
        assertions=AssertionStore(run_id=f"gt-{DOC}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{DOC}", concepts=concepts),
        acceptance_criteria=G.acceptance_criteria_layer(DOC, FILE, SEC["changes"][-1],
                                                        ct["tbl-criteria-change"][0], [UO]))
    _gate(annex, text)
    return annex
