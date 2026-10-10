"""PCP-004 Version 2.0: Process Characterization Plan, Harvest and Clarification (Step 4).

The protocol amendment issued under INV-001 for the step that separates the antibody from the cells of
the production culture, fitted to the Version 2.0 text. Harvest runs no designed experiment: its three
parameters are studied one factor at a time, and PCMP-001 Table 7.1 sets no intermediate acceptance
criterion for the clarified harvest, so the plan prints no criteria-change table. The kinds of record
follow the step-plan models (``build_plan_viral_inactivation`` in ``build_ground_truth``, and
``annex_builders/pcp_010.py`` for the other step without a design); the concept ids are those of the
Version 1.0 builder of this document (``build_plan_harvest``: ``step:harvest_clarification``, the three
``param:`` ids of ``HPARAM_CONCEPT``, ``equip:clarification_sdm``, ``equip:disk_stack_centrifuge``,
``equip:depth_filter``, ``study:hv_sdm_qual``).

Every table of the plan is a complex table (``T.frame`` or ``T.sop_references``), read back through
``qmd_ctables`` from the object the plan printed, so each row quote is the rendered row, with
``table_header=rows.header``. The related-documents and title-block tables are the markdown their
helpers return. Every prose quote is a span of the ``.qmd`` copied with its inline expressions and
evaluated in the plan's own namespace (``qmd_inline``); ``q`` refuses a span that is not in the ``.qmd``
prose, so no value is typed here. ``build()`` refuses to return an annex with a quote that does not
ground or with a weak anchor.

The plan describes only the study that Version 1.0 planned (S-HAR-UNI) and the qualification of the
scale-down model; it does not mention the studies of the step made during the Version 2.0 re-analysis,
and they have no record here.
"""
from __future__ import annotations

import os
import re

import _pcpkg as P
import build_ground_truth as G
import schema_ext as S
from check_grounding import CELL_SEP, normalize, specificity_report

DOC = "PCP-004"
QMD = "PCP-004_harvest.qmd"
FILE = G.PCP4_FILE                                   # "PCP-004_harvest.docx"

#: Concept ids kept from the Version 1.0 builder of this document (``build_plan_harvest``).
STEP_ID = "step:harvest_clarification"
SDM_ID = "equip:clarification_sdm"
CENTRIFUGE_ID = "equip:disk_stack_centrifuge"
DEPTH_ID = "equip:depth_filter"
QUAL_ID = "study:hv_sdm_qual"          # the qualification has no study id in the plan or the chronology
#: New here: the third unit of the commercial train, the three parts of the scale-down model that the
#: Version 2.0 text names, and the Protein A column of the load challenge.
STERILE_ID = "equip:sterilizing_grade_filter"
SHEAR_ID = "equip:hv_bench_shear_device"
LABCENT_ID = "equip:hv_laboratory_centrifuge"
DISKS_ID = "equip:hv_filter_media_disks"
PACOL_ID = "equip:hv_protein_a_challenge_column"

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
    "cqas": (_PRIOR, "Quality attributes in scope"),
    "risk": (_PRIOR, "Risk-based prioritization of parameters"),
    "methods": (_MM,),
    "sdm": (_MM, "Scale-down model and its qualification"),
    "operation": (_MM, "Operation"),
    "analytical": (_MM, "Analytical methods"),
    "sampling": (_MM, "Sampling plan"),
    "stats": (_MM, "Statistical methods"),
    "design": (_SD,),
    "factors": (_SD, "Factors, ranges and study type"),
    "univariate": (_SD, "Univariate assessment"),
    "criteria": ("Acceptance and decision criteria",),
    "par": ("Proven acceptable ranges (planned analysis)",),
    "data": ("Data management and integrity",),
    "roles": ("Roles and responsibilities",),
    "schedule": ("Deliverables and schedule",),
    "risks": ("Risks and assumptions",),
    "approvals": ("Approvals",),
    "appA": ("Appendix A. Planned assessment levels",),
    "appB": ("Appendix B. Planned sampling and test schedule",),
}
#: Relationship cell of the related-documents table -> DocumentRelationship.kind (as the other step
#: plans map it; "Sibling — paired document" and "Reason for this revision" fall back to "references").
REL_KIND = {"Rolls up into": "rolls_up_into", "Parent — master plan": "executed_under",
            "Parent — risk basis for study scope": "scoped_by", "Parent — transfer scope": "scoped_by"}


# --------------------------------------------------------------------------- #
# Local helpers. _check_sections, _cells, _smart, _walk and _gate are copied   #
# from annex_builders/pcp_009.py, md_caption and head_of from pcp_008.py,      #
# rows_once from pcp_010.py. _render and _nomark are new here (candidates for  #
# build_ground_truth, named in the report).                                    #
# --------------------------------------------------------------------------- #
def _sid(sec):
    return f"{DOC}_sec_{sec}"


def _source():
    return open(os.path.join(G.HERE, QMD), encoding="utf-8").read()


def _check_sections(src):
    """Every heading of SEC is a heading of the .qmd (outside its code chunks)."""
    prose = re.sub(r"```\{python\}.*?```", "", src, flags=re.S)
    heads = set(re.findall(r"^#+ (.+?)(?: \{[^}]*\})?\s*$", prose, flags=re.M))
    missing = sorted({t for path in SEC.values() for t in path if t != "Title block"} - heads)
    if missing:
        raise ValueError(f"{DOC}: section titles not in the document: {missing}")


def _cells(row):
    """The cells of a rendered row: a continuation row keeps its empty first cell."""
    return [c.strip() for c in row.split("|")]


def _smart(s):
    """Prose as pandoc renders it: straight double quotes become typographic pairs and a straight
    apostrophe a typographic one. Table cells are raw markup and keep the straight forms."""
    return re.sub(r'"([^"]*)"', "“\\1”", s).replace("'", "’")


def _render(s):
    """A .qmd span as the DOCX reads it: typographic quotes (``_smart``), and pandoc's escaped space
    (backslash-space, a non-breaking space that the comparison folds to a space) as a plain space.
    ``qmd_inline`` evaluates the inline expressions and leaves the escape in place, so a span such as
    ``Step\\ `{python} uo.step``` would otherwise read "Step\\ 4" and never ground."""
    return _smart(s).replace("\\ ", " ")


def _nomark(cell):
    """A rendered cell without its footnote marker: ``T.frame`` renders ``Name^a)^`` as "Name a)"."""
    return re.sub(r"\s+[a-z]\)$", "", cell)


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


def md_caption(src, label):
    """The caption a chunk prints after a markdown table (``print(": <caption> {#label}")``)."""
    m = re.findall(r'print\(f?": (.*?) \{#' + re.escape(label) + r'\}"\)', src)
    if len(m) != 1:
        raise ValueError(f"{DOC}: {len(m)} captions printed for {label}")
    return m[0]


def rows_once(rows, text):
    """``{key -> row}`` (+ ``.header``) for the rows of ``rows`` that occur exactly once in the
    rendered ``text``. A continuation row of a merged column can read exactly like another one (the
    depth filter load levels read alike in the blocks of its two centrates), which makes it an
    ambiguous reference."""
    out = G.RowQuotes((k, r) for k, r in rows.items() if text.count(normalize(r)) == 1)
    out.header = rows.header
    return out


def head_of(rows, key):
    """For a continuation row of a merged first column, the row that opens its group (it carries the
    label the continuation row leaves empty)."""
    order = list(rows)
    for k2 in reversed(order[:order.index(key) + 1]):
        if _cells(rows[k2])[0]:
            return k2
    raise ValueError(f"{DOC}: no group head for {key}")


# --------------------------------------------------------------------------- #
# The annex.                                                                   #
# --------------------------------------------------------------------------- #
def build():
    """The ``GroundTruthAnnex`` of PCP-004 Version 2.0."""
    import doe_report as D
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    from annex_contract.concepts import Concept, ConceptStore
    from annex_contract.discourse import DocumentRelationship, ExplicitNonClaim
    from annex_contract.summaries import ReportSection, ReportStatement

    src = _source()
    _check_sections(src)
    prose_src = normalize(re.sub(r"```\{python\}.*?```", " ", src, flags=re.S))
    ns, _ = G.qmd_namespace(QMD)
    ct = G.qmd_ctables(QMD)
    text = G._document_text(FILE)
    meta = G.meta

    def t(s):
        """Text in .qmd form, its inline expressions evaluated in the plan's namespace."""
        return _render(G.qmd_inline(ns, s))

    def q(s):
        """A span of the .qmd prose as it renders. The span must be copied from the .qmd with its
        inline expressions, so a typed value fails here rather than grounding by coincidence."""
        if normalize(s) not in prose_src:
            raise ValueError(f"{DOC}: not a span of the .qmd prose: {s[:90]!r}")
        return t(s)

    def ref(sec, quote, table=None, rows=None, caption=None, label=None):
        lab = table.label if table is not None else label
        r = G.ref(DOC, FILE, _sid(sec), SEC[sec][-1], quote,
                  table_title=table.caption if table is not None else caption,
                  table_id=None if lab is None else f"{DOC}_tab_{lab[4:].replace('-', '_')}",
                  table_header=None if rows is None else rows.header)
        r.heading_path = list(SEC[sec])
        return r

    def tref(sec, table, rows, key):
        """The rendered row ``key`` of the CTable ``table`` (``rows = ctable_rows(table, ...)``)."""
        return ref(sec, rows[key], table, rows)

    def keyed(label, keys, name_of, cell, mark=False):
        """The rendered rows of the CTable the plan printed under ``label``, keyed. Every row must name
        its own record in cell ``cell``: a mis-keyed row grounds and attests the wrong thing."""
        tab = ct[label][0]
        rows = G.ctable_rows(tab, keys)
        bad = [k for k, row in rows.items()
               if (_nomark(_cells(row)[cell]) if mark else _cells(row)[cell]) != name_of(k)]
        if bad:
            raise ValueError(f"{DOC} {label}: rows keyed to records they do not name: {bad}")
        return tab, rows

    def notes(tab):
        """The notes of a CTable, as the DOCX reads them (one cell each)."""
        return [n.strip() for n in tab.notes_text().split(CELL_SEP) if n.strip()]

    # ---- names and values of the plan -----------------------------------------------------------
    uo = ns["uo"]
    if (ns["DOC"], ns["UO"], ns["UO_TITLE"]) != (DOC, G.HUO, G.HSTEP_LABEL):
        raise ValueError(f"{DOC}: the plan is not the {G.HUO} plan it is annexed as")
    UO, UO_NAME, UO_TITLE = G.HUO, G.HUO_NAME, G.HSTEP_LABEL
    prm = list(uo.parameters)
    rcf, dfl, turb = ns["rcf"], ns["dfl"], ns["turb"]
    f0, join_and = ns["f0"], ns["join_and"]
    pcid = {p.key: G.HPARAM_CONCEPT[p.name] for p in prm}
    INV, AMD, REV1 = ns["INV"], ns["AMD"], ns["REV1"]
    ALPHA, TURB_LIMIT = ns["ALPHA"], ns["TURB_LIMIT"]
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))
    reg = P.cqa_reg.set_index("key")
    by_label = G._attr_key_by_label()
    title_of = dict(ns["HARVEST_AMV_REFS"])
    # no criterion of this step comes from the derivation, Version 1.0 or the verification
    if not (D.iac_table(UO).empty and D.rev1_criteria(UO).empty and D.iac_verification(UO).empty):
        raise ValueError(f"{DOC}: the step now has an intermediate or a Version 1.0 analysis criterion")

    # ---- the rendered tables, from the objects the plan printed ----------------------------------
    pt, prow = keyed("tbl-params", [p.name for p in prm], str, cell=0, mark=True)
    for p in prm:
        c = _cells(prow[p.name])                 # Parameter | Unit | Set-point | Range studied | NOR
        want = [p.name, p.unit, f0(p.setpoint_characterized), f"{f0(p.prange[0])}–{f0(p.prange[1])}",
                f"{f0(p.nor_characterized[0])}–{f0(p.nor_characterized[1])}"]
        if [_nomark(c[0])] + c[1:] != want:
            raise ValueError(f"{pt.label}: row {c} does not read {want}")
    if [p.name for p in prm if _cells(prow[p.name])[0] != p.name] != [turb.name]:
        raise ValueError(f"{pt.label}: the note marker is no longer on the turbidity row alone")
    p_note = notes(pt)
    if len(p_note) != 1 or not p_note[0].startswith("a) "):
        raise ValueError(f"{pt.label}: expected the one note a), found {p_note}")
    p_note = p_note[0]
    moved = [p.name for p in prm
             if float(p.setpoint) != float(p.setpoint_characterized)
             or [float(x) for x in p.nor] != [float(x) for x in p.nor_characterized]]

    cq_df = ct["tbl-cqas"][1]
    ckeys = [by_label[n] for n in cq_df["CQA"]]
    if ckeys != list(ns["CQA_KEYS"]):
        raise ValueError(f"{DOC}: the attribute table does not list the plan's CQA_KEYS")
    cq_t, crow = keyed("tbl-cqas", ckeys, lambda k: names[k], cell=1)
    cq_notes = notes(cq_t)
    sop_df = ct["tbl-sops"][1]
    sop_t, soprow = keyed("tbl-sops", list(sop_df["Reference"]), str, cell=1)
    perf_df = ct["tbl-perf"][1]
    perf_t, perfrow = keyed("tbl-perf", list(perf_df["Reference"]), str, cell=0)
    perf_note = notes(perf_t)[0]
    roles_df = ct["tbl-roles"][1]
    roles_t, rolerow = keyed("tbl-roles", list(roles_df["Function"]), str, cell=0)
    lev_t, lev_df = ct["tbl-levels"]
    levrow = rows_once(G.ctable_rows(lev_t), text)
    lev_note = notes(lev_t)[0]
    smp_df = ct["tbl-sampling"][1]
    smp_t, smprow = keyed("tbl-sampling", list(smp_df["Sample point"]), str, cell=0)
    smp_note = notes(smp_t)[0]
    rel = G.md_string_rows(P.related_docs_md(DOC))
    rel_cap = md_caption(src, "tbl-related")
    if normalize(f"{rel_cap} {rel.header}") not in text:
        raise ValueError(f"{DOC}: the related-documents caption no longer reads {rel_cap!r}")
    tb = G.md_string_rows(P.title_block(DOC, UO_TITLE))
    recv = next(k for k in rolerow if "receiving site" in k)

    # the later studies of the step are not studies of this plan, and the plan does not name them
    disc = [d for d in P.PLAN_DISCREPANCIES.get("PCR-004", []) if d.get("studies")]
    later = sorted({s_ for d in disc for s_ in d["studies"]})
    if [s_ for s_ in later if s_ in text]:
        raise ValueError(f"{DOC}: the plan now names a later study of the step; annex it")

    # ---- prose spans used by more than one record ----------------------------------------------------
    s_scope = "This plan defines the process characterization study of harvest and clarification, Step\\ `{python} uo.step` of the A-Mab drug substance process."
    s_separates = "Harvest separates the antibody from the cells and the cell debris of the production culture."
    s_train = "The culture passes a continuous disk-stack centrifuge, a train of depth filters and a sterilizing-grade filter, in that order."
    s_feed = "The step determines the quality of the feed to Protein A capture."
    s_oneatatime = "Each is studied one factor at a time on a scale-down model of the harvest train"
    s_beyond = "over a range that extends beyond its normal operating range (NOR)."
    s_responses = "The responses are the impurity burden of the clarified harvest, its particulate content, the pressure that the filter train develops, the size-variant profile of the antibody across the step and the step yield."
    s_challenge = "In the turbidity series they also include the column pressure and the cycle yield of a Protein A load challenge."
    s_v1_approved = "Version 1.0 of this plan was approved on `{python} REV1_DATE`, before the univariate study `{python} UNI_ID` began on `{python} UNI_START`."
    s_applies = "This revision applies the rules of the master plan PCMP-001 Version 2.0 to this step."
    s_register = "The drug substance CQA register of Version 2.0 assigns fragments to this step, so fragments are added to the attributes in scope"
    s_amv3020 = "the nrCE-SDS method validation AMV-3020"
    s_amd = 'PCMP-001 Version 2.0 sets nrCE-SDS as the method for fragments at every step, following the analytical method decision AMD-001 of `{python} AMD["date"]` (PCMP-001 §7.8).'
    s_frag_uni = "Fragments were not among the responses of the univariate study of this plan, which closed before AMD-001."
    s_obj1 = "Qualify a scale-down model of the commercial harvest train and show that it represents the centrifugation and depth filtration performance of that train"
    s_obj2 = "Establish the effect of the centrifugal field, over `{python} f0(rcf.prange[0])` `{python} rcf.unit` to `{python} f0(rcf.prange[1])` `{python} rcf.unit`, on the clarity of the centrate and on the host cell protein and DNA released by cell breakage."
    s_obj5 = "Define a proven acceptable range for each parameter, determine whether the normal operating range lies inside the proven acceptable range, and provide the evidence on which each parameter will be classified under the parameter classification procedure SOP-4001 (corrected, change 7)."
    s_centrifuge = "At commercial scale the culture is fed continuously to a disk-stack centrifuge."
    s_settle = "In the disc stack a particle settles onto a disc, is captured there and slides outward to the bowl wall, from which the solids are discharged at intervals (corrected, change 7)."
    s_centrate = "The centrate therefore still carries the fine debris and the colloidal material that are too small to settle in the time available."
    s_depth = "The depth filter train removes that material."
    s_media = "Its media are positively charged, so they adsorb part of the DNA and fine debris as well as retaining particles by size."
    s_sterile = "The filtrate then passes the sterilizing-grade filter into the harvest vessel, where it is held until capture."
    s_breaks = "It can also break more cells."
    s_shear = "The culture is accelerated to the speed of the bowl in the feed zone, and the shear there rises with that speed, while the flow between the discs is laminar and low in shear (corrected, change 7)."
    s_broken = "Broken cells release host cell protein and DNA into the centrate, and they leave fine debris that is harder to capture."
    s_load_unit = "For this reason the parameter is expressed as the volume of centrate loaded per unit of media area, in `{python} dfl.unit` (corrected, change 7)."
    s_turb_meas = "`{python} cap(N_TURB)` measures the fine particulate and colloidal material that the filters passed."
    s_turb_notset = "It is not a set parameter."
    s_turb_field = "A higher centrifugal field lowers it, because fewer cells and less debris reach the filters, and it can also raise it, because more broken cells leave fine debris (corrected, change 7)."
    s_dna_vl = "Residual DNA has very low criticality."
    s_agg_less = "Aggregate has a higher criticality than host cell protein, but an effect on it is less expected, because the antibody meets such an interface only briefly."
    s_frag_def = "Fragments are clipped antibody, mostly cleaved in or near the hinge into Fab and Fab+Fc species."
    s_three = "The three are in scope because shear and air-liquid interfaces in the centrifuge and the filters can break cells, which adds host cell protein and DNA, and because an air-liquid interface in the feed zone or in a foaming transfer can unfold the antibody and add aggregate (corrected, change 7)."
    s_enter = "Host cell protein, DNA and aggregate enter harvest in the culture fluid and leave it in the clarified harvest."
    s_not_credited = "The step is not credited with clearing them."
    s_no_dna_claim = "but no clearance is claimed for it."
    s_cex = "Aggregate is reduced mainly at cation exchange."
    s_frag_crit = "The master plan PCMP-001 sets no criterion for fragments at this step, and they are judged at the downstream steps (PCMP-001 Table 7.1)."
    s_frag_noresp = "Fragments are not a response of the study in this plan."
    s_ds_not_ipc = "are to be met by the clearance that the purification train delivers after this step, and they are not in-process limits for the clarified harvest (corrected, change 7)."
    s_ra = "The parameters of this study and the study type of each follow the pre-characterization risk assessment RA-001."
    s_no_mv = "No parameter was ranked high enough to require a multivariate design, so no screening or response-surface design is planned for this step (PCMP-001 §2)."
    s_dna_share = "The depth filter media adsorb part of the DNA, and the share that they take up can change with the filter load."
    s_clear = "Protein A capture and the two ion exchange steps clear the host cell protein and DNA that cell breakage releases"
    s_upper_only = "For `{python} join_and(upper_only)` the lower edge of the range studied is the lower limit of the NOR, and only the upper edge extends beyond it (corrected, change 7)."
    s_sdm = "The characterization runs will be executed on a scale-down model of the harvest train, qualified under the scale-down model procedure SOP-1001 before the first characterization run."
    s_three_parts = "The model reproduces the commercial operation in three parts, and each part is matched on the quantity that drives its own mechanism and not on the size of the equipment."
    s_shear_dev = "Cell damage in the feed zone will be reproduced in a bench shear device operated at the energy dissipation rate calculated for the commercial feed zone."
    s_lab_cent = "Sedimentation will be reproduced in a laboratory centrifuge operated at the same relative centrifugal field as the commercial bowl and at a matched ratio of flow to sigma factor."
    s_sigma = "At each field of the series the bench feed rate will be set so that its ratio of flow to sigma factor equals that of the commercial centrifuge at the same field and the commercial feed rate (corrected, change 7)."
    s_disks = "Depth filtration will be reproduced with disks of the commercial filter media, run at the same flux and to the same load per unit area, so that a setting expressed in `{python} dfl.unit` carries across in the same way."
    s_qual_cmp = "Qualification will compare the model with the commercial train at the set-point condition on the same culture."
    s_qual_cover = "The comparison will cover centrate turbidity, solids removal, host cell protein and DNA in the clarified harvest, filter pressure at the end of the load, and step yield."
    s_qual_rep = "Replicate runs will be performed at each scale."
    s_qual_batch = "At commercial scale each replicate is a separate batch."
    s_impurity_crit = "Host cell protein and DNA are judged against the impurity release criterion"
    s_no_qual_rule = "This plan therefore sets no qualification rule, and PCR-004 states its approach."
    s_qual_rsm = "PCMP-001 §7.1 decides the qualification of an output with a criterion on the response-surface model of the step, which this step does not have."
    s_runs_ask = "PCMP-001 §7.1 also asks each step plan to name the number of runs at each scale and the manufacturing-scale data set."
    s_runs_none = "Version 1.0 named neither, and this amendment, issued after the study, does not add them."
    s_turb_offset = "The turbidity of the clarified harvest, which the clarification limit of `{python} f0(TURB_LIMIT)` `{python} turb.unit` judges (criterion 2), is not in the comparison, so its offset is unknown, not zero."
    s_sv_offset = "The size variants and the column pressure and the cycle yield of the Protein A load challenge are not in the comparison either."
    s_once = "A continuous disk-stack centrifuge passes the feed through its feed zone once."
    s_damage = "The cell damage that a bench model does not fully reproduce comes from the acceleration of the feed in the feed zone, which the shear device matches only in its energy dissipation rate, and from the periodic discharge of solids (corrected, change 7)."
    s_bound = "This study uses the model to bound ranges and to establish the direction and the approximate size of each effect."
    s_no_abs = "It does not use the model to predict the absolute impurity concentration of a commercial batch."
    s_amv3015 = "Turbidity by nephelometry (AMV-3015) measures the fine particulate and colloidal material the filters pass, and it is the in-process measurement by which clarified harvest is released to capture."
    s_amv_hcp_dna = "Host cell protein by ELISA (AMV-3012) and residual DNA by qPCR (AMV-3014) measure the impurity burden of the clarified harvest."
    s_amv3012 = "Host cell protein by ELISA (AMV-3012)"
    s_amv3014 = "residual DNA by qPCR (AMV-3014) measure the impurity burden of the clarified harvest."
    s_amv3011 = "Size variants by SEC-HPLC (AMV-3011) measure the high molecular weight content of the antibody before and after the step."
    s_amv3011_perf = "The performance of AMV-3011 is given in its own validation report."
    s_no_conc = "Version 1.0 named no method for the antibody concentration on which step yield rests, and this amendment names none."
    s_no_reps = "Version 1.0 set no number of replicates, and this amendment sets none."
    s_sv_centrate = "The centrate is not tested for size variants, so a change found at the last point could not be placed at the centrifuge or at the filters (corrected, change 7)."
    s_resolve = "An effect smaller than the method can resolve will be reported as detected and not material, with the comparison shown."
    s_decisions = "rest on the significance of a change, on its size against the resolution of the method, or on an absolute limit, and not on the fit of a predictive model (corrected, change 7)."
    s_no_curv = "Version 1.0 named no test for curvature, and this amendment adds none."
    s_no_adeq = "No adequacy threshold is set for the regressions."
    s_ofat = "The design is one factor at a time."
    s_no_inter = "It cannot determine an interaction between two parameters, where the effect of one parameter on a response depends on the level of the other."
    s_inter_exp = "One interaction is expected on mechanistic grounds, since a higher centrifugal field passes fewer solids to the depth filter and so changes the load that filter has to handle."
    s_bracketed = "That interaction will be bracketed and not estimated."
    s_two_centrates = "The depth filter load series will be run on centrate produced at `{python} G_LO` and again on centrate produced at `{python} G_HI`, so that the filter is challenged with both extremes of the solids load it can receive."
    s_no_coef = "The bracket bounds the filter response between the two solids loads the centrifuge can deliver, and it yields no coefficient for the interaction, so none will be reported."
    s_no_rsm = "No response-surface model will be fitted for this step and no Monte-Carlo propagation of a fitted model will be performed, because no multivariate design is run here."
    s_setpoints_only = "A range reported from this study therefore holds with the other parameters at their set-points, and it says nothing about two of them moving away from their set-points together."
    s_rng_rcf = "`{python} cap(N_RCF)` runs from `{python} span(rcf)`, so that the series covers both the lower fields, at which clarification is less complete, and the higher fields, at which more cells may break"
    s_rng_dfl = "`{python} cap(N_DFL)` runs to `{python} f0(dfl.prange[1])` `{python} dfl.unit`, which loads the media beyond the upper NOR limit of `{python} f0(dfl.nor_characterized[1])` `{python} dfl.unit` and past the point at which the pressure drop is expected to rise (corrected, change 7)."
    s_rng_turb = "`{python} cap(N_TURB)` is the response of the other two parameters, and the range in its row is the range over which turbidity will be presented to capture, not a range of settings that will be dialled in at the centrifuge."
    s_five = "Each parameter will be assessed at five levels."
    s_three_cs = "Three of the five are values that the control strategy uses, so the study reports directly on the limits it is meant to justify (corrected, change 7)."
    s_four_levels = "For `{python} COINCIDE` the lower edge of the range studied and the lower limit of the NOR coincide, so its series has four distinct levels."
    s_pa_column = "The turbidity series will be loaded onto a scale-down Protein A column held at the set-point conditions of the Protein A plan PCP-005, as a Protein A load challenge."
    s_no_lc_crit = "Version 1.0 set no criterion for these two responses, and this amendment sets none."
    s_no_capture = "No conclusion about the capture step will be drawn from these runs, and the characterization of capture itself is reported in PCR-005."
    s_no_iac = "PCMP-001 Table 7.1 sets no intermediate acceptance criterion for the clarified harvest, because the derivation credits harvest with no change in any attribute, so the criteria of the production bioreactor output pass through it unchanged."
    s_no_ver = "For the same reason the verification of platform worst cases (PCMP-001 §7.5) has no value to check at this step."
    s_crit1 = "Impurity release is the first criterion."
    s_crit1_cmp = "Host cell protein and residual DNA in the clarified harvest will be compared with the same measurements on the unclarified culture that produced it."
    s_crit1_pass = "A level passes when no increase is detected at α = `{python} ALPHA`, or when a detected increase is smaller than the resolution of the method that measured it"
    s_crit2_cmp = "Post-clarification turbidity of the clarified harvest will be compared with the upper limit of its normal operating range, `{python} f0(TURB_LIMIT)` `{python} turb.unit`."
    s_crit3 = "Product quality is the third."
    s_crit3_cmp = "High molecular weight content will be compared before and after the step, and a level passes when no increase is detected at α = `{python} ALPHA`."
    s_yield_ng = "Step yield is reported but is not gated."
    s_no_yield = "No numeric yield limit is set in this plan, because none follows from a product quality requirement at this step."
    s_par_rsm = "PCMP-001 §6.4 computes proven acceptable ranges from the response-surface model of a step, once with the other parameters held at their set-points and once with them drawn at random around their set-points."
    s_par_needs = "That method needs a response-surface model"
    s_par_combo = "and no combination of two parameters away from their set-points is claimed for this step."
    s_par_whole = "Where every level of a parameter meets the criteria, the proven acceptable range will be reported as the whole range studied and not as anything wider."
    s_v1_gave_no = "Version 1.0 gave no size for the resolution of a method in the impurity release criterion, no threshold for judging the regressions on their coefficient of determination and residual standard error, no rule for the proven acceptable range of the post-clarification turbidity series, and no rule for how the proven acceptable range of depth filter load follows from its two series, on centrate from `{python} G_LO` and from `{python} G_HI`."
    s_sets_none = "This amendment sets none of them, and PCR-004 states its approach to each."
    s_nor_in_par = "It will determine whether the normal operating range lies inside the proven acceptable range (corrected, change 7)."
    s_no_ds = "No design space is claimed for this step."
    s_ds_mv = "A design space is a multivariate region, and this study runs no multivariate design."
    s_provide = "What the study is to provide to the control strategy is a proven acceptable range for each parameter, the position of the normal operating range against it, and an in-process control on the turbidity of the clarified harvest (corrected, change 7)."
    s_no_thresh = "Neither PCMP-001 nor SOP-4001 sets a numerical threshold for a practically relevant effect."
    s_class_out = "Classification is an outcome of the study and is reported in PCR-004."
    s_deliverable = "The deliverable of this study is the Process Characterization Report for Harvest and Clarification, PCR-004."
    s_qual_first = "The scale-down model will be qualified first, and no characterization run will be executed until that qualification has been reviewed and accepted."
    s_no_dates = "Version 1.0 fixed no dates."
    s_ptp = "It held the schedule in the transfer plan PTP-001, where it was coordinated with the other characterization studies of the campaign and with the availability of the bioreactor scale-down model."
    s_window = "The study chronology of the campaign gives the execution window of the univariate study `{python} UNI_ID`, from its first day of execution on `{python} UNI_START` to its last on `{python} UNI_END` (PCMP-001 Table 9.1)."
    s_lysis = "and the model is expected to under-represent lysis (corrected, change 7)."
    s_mitigation = "The mitigation is that the study reports effects and ranges rather than absolute impurity levels"
    s_each_regression = "Each regression will therefore be reported with its coefficient of determination and its residual standard error and will be judged on those."
    s_pcr_state = "PCR-004 will therefore state, for each parameter, the size of each effect across the proven acceptable range and the margin of that range to the normal operating range, and it will give the reason for each class from those two quantities."
    s_frag_form = "Fragments form in the culture and continue to form in the clarified harvest"
    s_blend = "The blended material of the turbidity series carries the particle size distribution of centrate and not that of a saturated depth filter"
    s_blend_claim = "The turbidity range will therefore be reported as a range of turbidity delivered to capture, and no claim will be made about the specific material a filter at the end of its capacity would pass."
    s_run_twice = "the depth filter load series will be run twice, once on centrate from each end of the range studied for `{python} N_RCF`."

    # ==== entities ===================================================================================
    step = S.ProcessStep(
        step_id=STEP_ID, step_name=UO_NAME, step_number=str(uo.step), unit_operation=UO_NAME,
        description=f"Step {uo.step} of the A-Mab drug substance process. Harvest separates the antibody from "
                    f"the cells and the cell debris of the production culture: once per batch the contents "
                    f"of the {ns['SCALE_L']:,} L production bioreactor pass a continuous disk-stack "
                    f"centrifuge, a train of positively charged depth filters and a sterilizing-grade filter, "
                    f"and the clarified harvest is held in the harvest vessel until Protein A capture. The step "
                    f"determines the quality of the feed to capture. The centrifuge and the filters are not "
                    f"expected to change a quality attribute of the antibody, but cell breakage can release "
                    f"host cell protein and DNA, and fragments continue to form in the clarified harvest. The "
                    f"step is not credited with clearing host cell protein, DNA or aggregate, and no viral "
                    f"clearance is claimed for it.",
        input_materials=["contents of the production bioreactor at the end of culture"],
        output_materials=["clarified harvest, held in the harvest vessel until Protein A capture"],
        equipment=["continuous disk-stack centrifuge", "depth filter train", "sterilizing-grade filter", G.HSDM],
        source_references=[ref("purpose", q(s_scope)), ref("purpose", q(s_separates)),
                           ref("purpose", q(s_train)), ref("purpose", q(s_feed))],
        metadata=meta())
    sites = G._site_entities(DOC, FILE, _sid("title"))
    roles_recv = tref("roles", roles_t, rolerow, recv)
    equipment = [
        S.Equipment(
            equipment_id=SDM_ID, equipment_name=G.HSDM,
            equipment_type="scale-down model of the harvest train (feed-zone shear, sedimentation and depth "
                           "filtration)",
            site_name=P.SENDING_SITE,
            source_references=[ref("sdm", q(s_sdm)), ref("sdm", q(s_three_parts)), ref("objectives", q(s_obj1))],
            metadata=meta()),
        S.Equipment(
            equipment_id=CENTRIFUGE_ID, equipment_name="continuous disk-stack centrifuge",
            equipment_type="centrifuge (manufacturing scale)", site_name=P.RECEIVING_SITE,
            source_references=[ref("purpose", q(s_train)), ref("uo", q(s_centrifuge)), roles_recv],
            metadata=meta()),
        S.Equipment(
            equipment_id=DEPTH_ID, equipment_name="depth filter train",
            equipment_type="depth filters with positively charged media (manufacturing scale)",
            site_name=P.RECEIVING_SITE,
            source_references=[ref("uo", q(s_depth)), ref("uo", q(s_media)), roles_recv],
            metadata=meta()),
        S.Equipment(
            equipment_id=STERILE_ID, equipment_name="sterilizing-grade filter",
            equipment_type="filter (manufacturing scale)", site_name=P.RECEIVING_SITE,
            source_references=[ref("uo", q(s_sterile)), roles_recv],
            metadata=meta()),
        S.Equipment(
            equipment_id=SHEAR_ID, equipment_name="bench shear device",
            equipment_type="shear device (part of the scale-down model: cell damage in the feed zone)",
            site_name=P.SENDING_SITE, source_references=[ref("sdm", q(s_shear_dev))], metadata=meta()),
        S.Equipment(
            equipment_id=LABCENT_ID, equipment_name="laboratory centrifuge",
            equipment_type="centrifuge (part of the scale-down model: sedimentation)",
            site_name=P.SENDING_SITE, source_references=[ref("sdm", q(s_lab_cent))], metadata=meta()),
        S.Equipment(
            equipment_id=DISKS_ID, equipment_name="disks of the commercial filter media",
            equipment_type="depth filter media disks (part of the scale-down model: depth filtration)",
            site_name=P.SENDING_SITE, source_references=[ref("sdm", q(s_disks))], metadata=meta()),
        S.Equipment(
            equipment_id=PACOL_ID, equipment_name="scale-down Protein A column",
            equipment_type="chromatography column (scale-down model of Protein A capture), loaded with the "
                           "turbidity series as a Protein A load challenge",
            site_name=P.SENDING_SITE, source_references=[ref("univariate", q(s_pa_column))], metadata=meta()),
    ]
    eq = {e.equipment_id: e for e in equipment}

    # parameters: each on its row of the parameter table and on the sentence of §6.1 that states its range
    q_range = {rcf.key: q(s_rng_rcf), dfl.key: q(s_rng_dfl), turb.key: q(s_rng_turb)}
    params = []
    for p in prm:
        refs = [tref("factors", pt, prow, p.name), ref("factors", q_range[p.key])]
        if p.key == turb.key:                 # the note of the table: measured, not set, in two series
            refs.append(ref("factors", p_note, pt))
        params.append(S.ProcessParameter(
            parameter_id=pcid[p.key], parameter_name=p.name, parameter_type="unclassified", unit=p.unit,
            target_value=f"{f0(p.setpoint_characterized)} {p.unit}",
            NOR=f"{f0(p.nor_characterized[0])}–{f0(p.nor_characterized[1])} {p.unit}",
            PAR=f"{f0(p.prange[0])}–{f0(p.prange[1])} {p.unit}",
            associated_step=UO_TITLE, study_type=p.study, source_references=refs, metadata=meta()))

    # quality attributes: each on its row of the attribute table (and on the sentence that describes it)
    method_of = {k: amv for amv in title_of for k in G.METHOD_ATTRS.get(amv, []) if k in ckeys}
    acc_ds = dict(zip(ckeys, cq_df["Acceptance"]))
    attr_extra = {"residual_dna": s_dna_vl, "aggregates_hmw": s_agg_less, "fragments_lmw": s_frag_def}
    attrs = []
    for i, key in enumerate(ckeys):
        r = reg.loc[key]
        score = int(cq_df["Tool #1"].iloc[i])
        refs = [tref("cqas", cq_t, crow, key)]
        if key in attr_extra:
            refs.append(ref("cqas", q(attr_extra[key])))
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=r["cqa"], attribute_type="CQA", unit=r["unit"],
            acceptance_criteria=[f"{acc_ds[key]} (drug substance)"], analytical_method=method_of.get(key),
            associated_steps=[UO_TITLE],
            rationale_for_criticality=f"A-Mab Tool #1 score = impact score × uncertainty score = {score}.",
            criticality_level=cq_df["Criticality"].iloc[i], tool1_score=score,
            tool2_severity=int(r["tool2_severity"]), source_references=refs, metadata=meta()))

    # analytical methods: each on its sentence, its row of the procedures table and its performance row
    q_method = {"AMV-3015": [("analytical", s_amv3015)],
                "AMV-3012": [("analytical", s_amv_hcp_dna)],
                "AMV-3014": [("analytical", s_amv_hcp_dna)],
                "AMV-3011": [("analytical", s_amv3011), ("analytical", s_amv3011_perf)],
                "AMV-3020": [("changes", s_amv3020)]}
    if set(q_method) != set(title_of):
        raise ValueError(f"{DOC}: method sentences {sorted(q_method)} != AMVs {sorted(title_of)}")
    analyte = {"AMV-3015": "turbidity (the fine particulate and colloidal material the filters pass)",
               "AMV-3012": "host cell protein", "AMV-3014": "residual DNA",
               "AMV-3011": "size variants (high molecular weight content)", "AMV-3020": "fragments (LMW)"}
    methods = []
    for amv, title in ns["HARVEST_AMV_REFS"]:
        keys = [k for k in G.METHOD_ATTRS.get(amv, []) if k in ckeys]
        refs = [ref(s_, q(x)) for s_, x in q_method[amv]] + [tref("related", sop_t, soprow, amv)]
        if amv in perfrow:
            refs.append(tref("analytical", perf_t, perfrow, amv))
        methods.append(S.AnalyticalMethod(
            method_id=amv, method_name=title, method_type=G.METHOD_TYPE.get(amv), analytes=[analyte[amv]],
            associated_attributes=[f"attr:{k}" for k in keys], validation_status="validated",
            source_references=refs, metadata=meta()))

    # ---- explicit non-claims, by section -----------------------------------------------------------
    nc, nc_at = [], {}

    def nclaim(sec, subject, statement, quotes, rationale=None, elsewhere=None, extra=()):
        """``quotes``: one .qmd span of ``sec``, or a list of (section, span) pairs."""
        pairs = [(sec, quotes)] if isinstance(quotes, str) else quotes
        nc.append(ExplicitNonClaim(
            non_claim_id=f"{DOC}-NC{len(nc) + 1:02d}", subject=subject, unit_operation=UO_NAME,
            statement=statement, rationale=rationale, handled_elsewhere=elsewhere,
            source_references=[ref(s_, q(x)) for s_, x in pairs] + list(extra), metadata=meta()))
        nc_at.setdefault(sec, []).append(nc[-1])

    nclaim("purpose", "culture conditions",
           "The culture conditions, which set the viability at the end of culture, lie outside the plan; they "
           "are characterized under the production bioreactor plan PCP-003 and are not varied in the study.",
           [("purpose", "The culture conditions, which set the viability at the end of culture."),
            ("purpose", "The culture conditions are characterized under the production bioreactor plan PCP-003 and are not varied here.")],
           elsewhere="PCP-003, the production bioreactor plan")
    nclaim("purpose", "parameters of Protein A capture",
           "The parameters of Protein A capture lie outside the plan; in the study capture serves only as a "
           "Protein A load challenge at set-point conditions.",
           [("purpose", "The parameters of Protein A capture, which are characterized under the Protein A plan PCP-005."),
            ("purpose", "In this study capture serves only as a Protein A load challenge at set-point conditions")],
           elsewhere="PCP-005, the Protein A plan")
    nclaim("purpose", "number and arrangement of the depth filter stages",
           "The number and the arrangement of the depth filter stages lie outside the plan; the depth and sterile "
           "filtration procedure SOP-2006 fixes them.",
           "The number and the arrangement of the depth filter stages, which the depth and sterile filtration procedure SOP-2006 fixes.",
           elsewhere="SOP-2006", extra=[tref("related", sop_t, soprow, "SOP-2006")])
    nclaim("purpose", "viral clearance", "No viral clearance is claimed for the step, and no spiking study is "
           "included.", "No clearance is claimed for this step, and no spiking study is included")
    nclaim("purpose", "hold of the clarified harvest before capture",
           "The hold of the clarified harvest before capture lies outside the plan; its duration and its "
           "temperature are not parameters of the study.",
           [("purpose", "The hold of the clarified harvest before capture."),
            ("purpose", "Its duration and its temperature are not parameters of this study.")])
    nclaim("changes", "analysis-time criterion in Version 1.0",
           "No acceptance criterion set after the data were seen was applied to this step in Version 1.0.",
           "No such criterion was applied to this step in Version 1.0.")
    nclaim("changes", "fragments in the univariate study",
           "Fragments were not among the responses of the univariate study of the plan, which closed before the "
           "analytical method decision AMD-001; fragments are not a response of the study.",
           [("changes", s_frag_uni), ("cqas", s_frag_noresp)])
    nclaim("changes", "single-batch prediction interval and model-adequacy criteria",
           "The single-batch prediction interval of PCMP-001 §6.2 and the model-adequacy criteria of PCMP-001 "
           "§7.2 do not apply to the study, because they apply to response-surface models.",
           "The single-batch prediction interval of PCMP-001 §6.2 and the model-adequacy criteria of PCMP-001 §7.2 apply to response-surface models, and so not to this study",
           rationale="The study fits no response-surface model.", extra=[ref("stats", q(s_no_rsm))])
    nclaim("objectives", "parameter classes",
           "The plan assigns no parameter class; classification is an outcome of the study, reported in PCR-004.",
           s_class_out, elsewhere="PCR-004")
    nclaim("uo", "post-clarification turbidity as a set parameter",
           "Post-clarification turbidity is not a set parameter: it measures the material the filters passed, "
           "and it is measured, not set, in the centrifugation (rcf) and depth filter load series.",
           [("uo", s_turb_meas), ("uo", s_turb_notset)], extra=[ref("factors", p_note, pt)])
    nclaim("cqas", "clearance of host cell protein, DNA and aggregate",
           "The step is not credited with clearing host cell protein, DNA or aggregate; the depth filter media "
           "adsorb part of the DNA, but no clearance is claimed for it.",
           [("cqas", s_enter), ("cqas", s_not_credited), ("cqas", s_no_dna_claim)],
           elsewhere="Protein A capture and the two ion exchange steps (aggregate mainly at cation exchange)",
           extra=[ref("risk", q(s_clear)), ref("cqas", q(s_cex))])
    nclaim("cqas", "criterion for fragments at this step",
           "PCMP-001 sets no criterion for fragments at the step; fragments are judged at the downstream steps.",
           s_frag_crit, elsewhere="the downstream steps (PCMP-001 Table 7.1)")
    nclaim("cqas", "in-process limits for the clarified harvest",
           "The drug substance criteria of the attribute table are not in-process limits for the clarified "
           "harvest; they are to be met by the clearance that the purification train delivers after the step.",
           s_ds_not_ipc, elsewhere="the purification train after harvest")
    nclaim("risk", "multivariate design",
           "No screening or response-surface design is planned for the step, because no parameter was ranked "
           "high enough in RA-001 to require a multivariate design.", s_no_mv)
    nclaim("sdm", "rule for the qualification decision",
           "The plan sets no rule for the qualification decision of the scale-down model; PCR-004 states its "
           "approach.", [("sdm", s_qual_rsm), ("sdm", s_no_qual_rule)],
           rationale="PCMP-001 §7.1 decides the qualification of an output with a criterion on the "
                     "response-surface model of the step, and the step has none.",
           elsewhere="PCR-004")
    nclaim("sdm", "number of qualification runs and manufacturing-scale data set",
           "Neither Version 1.0 nor this amendment names the number of runs at each scale or the "
           "manufacturing-scale data set of the qualification.", [("sdm", s_runs_ask), ("sdm", s_runs_none)])
    nclaim("sdm", "scale-down offsets of turbidity, size variants and the load challenge",
           "The turbidity of the clarified harvest, the size variants and the column pressure and cycle yield of "
           "the Protein A load challenge are not in the qualification comparison, so their offsets are unknown, "
           "not zero.", [("sdm", s_turb_offset), ("sdm", s_sv_offset)])
    nclaim("sdm", "absolute impurity concentration at commercial scale",
           "The study does not use the scale-down model to predict the absolute impurity concentration of a "
           "commercial batch; it uses it to bound ranges and to establish the direction and the approximate size "
           "of each effect.", [("sdm", s_no_abs), ("sdm", s_bound)],
           rationale="The scale-down model is expected to under-represent lysis, and the mitigation of that risk "
                     "is that the study reports effects and ranges rather than absolute impurity levels.",
           extra=[ref("risks", q(s_lysis)), ref("risks", q(s_mitigation))])
    nclaim("analytical", "method for the antibody concentration",
           "Neither Version 1.0 nor this amendment names a method for the antibody concentration on which step "
           "yield rests.", s_no_conc)
    nclaim("sampling", "number of set-point replicates",
           "Neither Version 1.0 nor this amendment sets the number of replicates of the set-point condition.",
           s_no_reps, extra=[ref("appA", lev_note, lev_t)])
    nclaim("sampling", "size variants in the centrate",
           "The centrate is not tested for size variants, so a change in size variants found in the clarified "
           "harvest could not be placed at the centrifuge or at the filters.", s_sv_centrate)
    nclaim("stats", "test for curvature", "Neither Version 1.0 nor this amendment names a test for curvature.",
           s_no_curv)
    nclaim("stats", "adequacy threshold for the regressions",
           "No adequacy threshold is set for the regressions; each regression is reported with its coefficient of "
           "determination and its residual standard error and judged on those.",
           [("stats", s_no_adeq), ("stats", s_each_regression)])
    nclaim("stats", "interaction between the centrifugal field and the depth filter load",
           "The interaction between the centrifugal field and the depth filter load is bracketed, not "
           "estimated, and no coefficient for it will be reported.",
           [("stats", s_bracketed), ("stats", s_no_coef), ("stats", s_no_inter)],
           rationale="The design is one factor at a time and cannot determine an interaction between two "
                     "parameters.")
    nclaim("stats", "response-surface model and Monte-Carlo propagation",
           "No response-surface model will be fitted for the step and no Monte-Carlo propagation of a fitted "
           "model will be performed.", s_no_rsm, rationale="No multivariate design is run at the step.")
    nclaim("stats", "two parameters away from their set-points together",
           "A range reported from the study holds with the other parameters at their set-points and says "
           "nothing about two of them moving away from their set-points together; no such combination is "
           "claimed.", [("stats", s_setpoints_only), ("par", s_par_combo)])
    nclaim("univariate", "criterion for the load challenge responses",
           "Neither Version 1.0 nor this amendment sets a criterion for the column pressure or the cycle yield "
           "of the Protein A load challenge.", s_no_lc_crit)
    nclaim("univariate", "conclusions about the capture step",
           "No conclusion about the Protein A capture step will be drawn from the load challenge runs.",
           s_no_capture, elsewhere="PCR-005")
    nclaim("criteria", "intermediate acceptance criterion for the clarified harvest",
           "PCMP-001 Table 7.1 sets no intermediate acceptance criterion for the clarified harvest.", s_no_iac,
           rationale="The derivation credits harvest with no change in any attribute, so the criteria of the "
                     "production bioreactor output pass through it unchanged.")
    nclaim("criteria", "verification of platform worst cases",
           "The verification of platform worst cases (PCMP-001 §7.5) has no value to check at the step.",
           s_no_ver)
    nclaim("criteria", "numeric yield limit",
           "Step yield is reported but not gated, and no numeric yield limit is set in the plan.",
           [("criteria", s_yield_ng), ("criteria", s_no_yield)],
           rationale="No yield limit follows from a product quality requirement at this step.")
    nclaim("par", "proven acceptable range from a response-surface model",
           "The proven acceptable ranges are not computed by the method of PCMP-001 §6.4, which needs a "
           "response-surface model; they are determined from the levels tested.",
           [("par", s_par_rsm), ("par", s_par_needs)])
    nclaim("par", "proven acceptable range beyond the range studied",
           "A proven acceptable range will not be reported as wider than the range studied.", s_par_whole)
    nclaim("par", "rules that Version 1.0 left open",
           "Version 1.0 gave no size for the resolution of a method, no threshold for judging the regressions, "
           "no rule for the proven acceptable range of the turbidity series and no rule for combining the two "
           "depth filter load series, and this amendment sets none of them.",
           [("par", s_v1_gave_no), ("par", s_sets_none)], elsewhere="PCR-004")
    nclaim("par", "design space", "No design space is claimed for the step.",
           [("par", s_no_ds), ("par", s_ds_mv)],
           rationale="A design space is a multivariate region, and the study runs no multivariate design.")
    nclaim("par", "numerical threshold for a practically relevant effect",
           "Neither PCMP-001 nor SOP-4001 sets a numerical threshold for a practically relevant effect.",
           [("par", s_no_thresh), ("par", s_pcr_state)],
           elsewhere="PCR-004 states the size of each effect and the margin of each range")
    nclaim("schedule", "dates fixed in Version 1.0",
           "Version 1.0 fixed no dates; it held the schedule in the transfer plan PTP-001.",
           [("schedule", s_no_dates), ("schedule", s_ptp)], elsewhere="PTP-001")
    nclaim("risks", "material passed by a saturated depth filter",
           "No claim will be made about the specific material a depth filter at the end of its capacity would "
           "pass; the turbidity range is reported as a range of turbidity delivered to capture.",
           [("risks", s_blend_claim), ("risks", s_blend)],
           rationale="The blended material of the turbidity series carries the particle size distribution of "
                     "centrate and not that of a saturated depth filter.")

    # ---- document relationships: the rows of the related-documents table, then the prose ----------
    rels = []

    def relation(kind, target, statement, refs):
        rels.append(DocumentRelationship(
            relationship_id=f"{DOC}-R{len(rels) + 1:02d}", kind=kind, source_document_id=DOC,
            target_document_ref=target, statement=statement, source_references=refs, metadata=meta()))

    for target, row in rel.items():
        txt = _cells(row)[-1]
        relation(REL_KIND.get(txt, "references"), target, txt,
                 [ref("related", row, rows=rel, caption=rel_cap, label="tbl-related")])
    relation("supersedes", f"{DOC} Version {REV1['rev']}", "Version 2.0 supersedes Version 1.0 of the plan.",
             [ref("title", tb["Supersedes"], rows=tb)])
    relation("executed_under", "PCMP-001", "The revision applies the rules of the master plan PCMP-001 "
             "Version 2.0 to the step.", [ref("changes", q(s_applies))])
    relation("scoped_by", "RA-001", "The parameters of the study and the study type of each follow the "
             "pre-characterization risk assessment RA-001.", [ref("risk", q(s_ra))])
    relation("references", "PCP-003", "The culture for the study is taken from the production bioreactor "
             "scale-down model at the end of culture, at the conditions characterized under the production "
             "bioreactor plan PCP-003.",
             [ref("operation", q("The culture will be taken from the production bioreactor scale-down model at the end of culture, at the conditions characterized under the production bioreactor plan PCP-003."))])
    relation("references", "PCP-005", "The turbidity series is loaded onto a scale-down Protein A column held "
             "at the set-point conditions of the Protein A plan PCP-005.", [ref("univariate", q(s_pa_column))])
    relation("references", "PCR-005", "The characterization of Protein A capture is reported in PCR-005, and "
             "the load challenge draws no conclusion about it.", [ref("univariate", q(s_no_capture))])
    relation("references", "PCR-004", "The deliverable of the study is the paired report PCR-004.",
             [ref("schedule", q(s_deliverable))])
    relation("references", "PTP-001", "Version 1.0 held the schedule of the study in the transfer plan PTP-001.",
             [ref("schedule", q(s_ptp))])
    relation("references", AMD["id"], "The analytical method decision that set nrCE-SDS as the method for "
             "fragments at every step; fragments are not a response of the study of this plan.",
             [ref("changes", q(s_amd))])

    def section(key, **kw):
        return S.SectionEntityExtraction(document_id=DOC, section_id=_sid(key),
                                         non_claims=nc_at.get(key, []), **kw)
    entities = [
        section("purpose", process_steps=[step], sites=sites),
        section("changes"),
        section("objectives"),
        section("related", document_relationships=rels),
        section("uo", equipment=[eq[CENTRIFUGE_ID], eq[DEPTH_ID], eq[STERILE_ID]]),
        section("cqas", quality_attributes=attrs),
        section("risk"),
        section("sdm", equipment=[eq[SDM_ID], eq[SHEAR_ID], eq[LABCENT_ID], eq[DISKS_ID]]),
        section("analytical", analytical_methods=methods),
        section("sampling"),
        section("stats"),
        section("factors", parameters=params),
        section("univariate", equipment=[eq[PACOL_ID]]),
        section("criteria"),
        section("par"),
        section("schedule"),
        section("risks"),
    ]
    listed = {n_.non_claim_id for e in entities for n_ in e.non_claims}
    if listed != {n_.non_claim_id for n_ in nc}:
        raise ValueError(f"{DOC}: non-claims of sections with no entity record")

    # ==== studies ======================================================================================
    # the qualification of the scale-down model: planned in §5.1, run first (§11), and given no study id
    qual = S.StudyDesign(
        study_id=QUAL_ID, study_type="scale_down_qualification",
        design_name="comparison of the scale-down model with the commercial train at the set-point condition "
                    "on the same culture, with replicate runs at each scale (each commercial replicate a "
                    "separate batch); each output is judged by its offset from manufacturing scale (PCMP-001 "
                    "§7.1)",
        unit_operation=UO_NAME,
        responses=["centrate turbidity", "solids removal", "host cell protein in the clarified harvest",
                   "DNA in the clarified harvest", "filter pressure at the end of the load", "step yield"],
        scale_down_model=G.HSDM,
        source_references=[ref("sdm", q(s_qual_cmp)), ref("sdm", q(s_qual_cover)), ref("sdm", q(s_qual_rep)),
                           ref("sdm", q(s_qual_batch)), ref("schedule", q(s_qual_first)),
                           tref("related", sop_t, soprow, "SOP-1001")],
        metadata=meta())
    studies, unrendered = [qual], []
    uni = ns["uni"]
    if G.STUDY_TYPE.get(uni["kind"]) != "univariate" or len(ns["plan_st"]) != 1:
        raise ValueError(f"{DOC}: the study of the plan is no longer the one univariate study")
    q_window = q(s_window)
    if not G._present(q_window, text):
        unrendered.append(uni["id"])
    else:
        lev_refs = [ref("appA", row, lev_t, levrow) for row in levrow.values()]
        smp_refs = [ref("appB", row, smp_t, smprow) for row in smprow.values()]
        studies.append(S.StudyDesign(
            study_id=f"study:{uni['id']}", study_type="univariate",
            design_name=t("one factor at a time: each parameter at five planned levels (the edges of the range "
                          "studied, the limits of the NOR and the set-point), the other parameters at their "
                          "set-points, in randomized order within each series, with replicates of the set-point "
                          "condition distributed across each series; the depth filter load series run on "
                          "centrate produced at `{python} G_LO` and at `{python} G_HI`; the "
                          "`{python} N_TURB` series, with four distinct levels, on clarified harvest blended "
                          "with retained centrate and loaded onto a scale-down Protein A column as a load "
                          "challenge"),
            unit_operation=UO_NAME, factors=[p.name for p in prm],
            responses=["impurity burden of the clarified harvest (host cell protein and residual DNA)",
                       "particulate content of the clarified harvest (turbidity)",
                       "pressure developed by the filter train",
                       "size-variant profile of the antibody across the step (high molecular weight content)",
                       "step yield",
                       "column pressure of the Protein A load challenge (turbidity series)",
                       "cycle yield of the Protein A load challenge (turbidity series)"],
            scale_down_model=G.HSDM, associated_parameters=[pcid[p.key] for p in prm],
            source_references=[ref("schedule", q_window), ref("changes", q(s_v1_approved)),
                               ref("purpose", q(s_oneatatime)), ref("purpose", q(s_responses)),
                               ref("purpose", q(s_challenge)), ref("univariate", q(s_five)),
                               ref("univariate", q(s_four_levels)), ref("stats", q(s_two_centrates))]
            + lev_refs + smp_refs + [ref("appB", smp_note, smp_t)],
            metadata=meta()))

    # ==== assertions =================================================================================
    A = []

    def add(subj, pred, obj, txt, refs):
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{DOC}-A{len(A) + 1:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=txt, source_references=refs, metadata=meta()))

    add(STEP_ID, "step_uses_equipment", SDM_ID,
        "The characterization runs of harvest and clarification are executed on a scale-down model of the "
        "harvest train, qualified under SOP-1001 before the first characterization run.", [ref("sdm", q(s_sdm))])
    add(STEP_ID, "step_uses_equipment", CENTRIFUGE_ID,
        "At commercial scale the culture is fed continuously to a disk-stack centrifuge.",
        [ref("uo", q(s_centrifuge))])
    add(STEP_ID, "step_uses_equipment", DEPTH_ID,
        "The depth filter train removes the fine debris and colloidal material that the centrifuge passes; its "
        "positively charged media adsorb part of the DNA and fine debris as well as retaining particles by size.",
        [ref("uo", q(s_centrate)), ref("uo", q(s_depth)), ref("uo", q(s_media))])
    add(STEP_ID, "step_uses_equipment", STERILE_ID,
        "The filtrate of the depth filter train passes the sterilizing-grade filter into the harvest vessel, "
        "where it is held until capture.", [ref("uo", q(s_sterile))])
    add(STEP_ID, "step_uses_equipment", SHEAR_ID,
        "In the scale-down model, cell damage in the feed zone is reproduced in a bench shear device operated at "
        "the energy dissipation rate calculated for the commercial feed zone.", [ref("sdm", q(s_shear_dev))])
    add(STEP_ID, "step_uses_equipment", LABCENT_ID,
        "In the scale-down model, sedimentation is reproduced in a laboratory centrifuge at the relative "
        "centrifugal field of the commercial bowl and a matched ratio of flow to sigma factor.",
        [ref("sdm", q(s_lab_cent))])
    add(STEP_ID, "step_uses_equipment", DISKS_ID,
        "In the scale-down model, depth filtration is reproduced with disks of the commercial filter media, run "
        "at the commercial flux and to the same load per unit area.", [ref("sdm", q(s_disks))])
    for p in prm:
        add(STEP_ID, "step_has_parameter", pcid[p.key], f"{UO_NAME} has process parameter {p.name}.",
            [tref("factors", pt, prow, p.name)])
    role = {"hcp": ("carries host cell protein, which enters harvest in the culture fluid and leaves it in the "
                    "clarified harvest; the step is not credited with clearing it",
                    [("cqas", s_enter), ("cqas", s_not_credited)]),
            "residual_dna": ("carries residual DNA into the clarified harvest; the depth filter media adsorb part "
                             "of it, but no clearance is claimed for it",
                             [("risk", s_dna_share), ("cqas", s_no_dna_claim)]),
            "aggregates_hmw": ("can add aggregate where an air-liquid interface in the feed zone or in a foaming "
                               "transfer unfolds the antibody; aggregate is reduced mainly at cation exchange",
                               [("cqas", s_three), ("cqas", s_cex)]),
            "fragments_lmw": ("is assigned fragments by the drug substance CQA register of Version 2.0; fragments "
                              "form in the culture and continue to form in the clarified harvest",
                              [("changes", s_register), ("purpose", s_frag_form)])}
    for key in ckeys:
        refs = [tref("cqas", cq_t, crow, key)]
        head = head_of(crow, key)
        if head != key:                       # the category is the merged cell of the group's first row
            refs.append(tref("cqas", cq_t, crow, head))
        add(STEP_ID, "step_has_quality_attribute", f"attr:{key}", f"{UO_NAME} {role[key][0]}.",
            refs + [ref(s_, q(x)) for s_, x in role[key][1]])
    q_meas = {"hcp": [ref("analytical", q(s_amv3012))], "residual_dna": [ref("analytical", q(s_amv3014))],
              "aggregates_hmw": [ref("analytical", q(s_amv3011))],
              "fragments_lmw": [ref("changes", q(s_amd))]}
    for key in ckeys:
        amv = method_of[key]
        how = (" PCMP-001 Version 2.0 sets nrCE-SDS as the method for fragments at every step; fragments are not "
               "a response of the study in this plan." if key == "fragments_lmw" else "")
        add(f"attr:{key}", "attribute_measured_by_method", f"method:{amv}",
            f"{names[key]} is measured by {amv} ({title_of[amv]}).{how}", q_meas[key])
    crit1 = t("by the impurity release criterion of Version 1.0, kept in Version 2.0: compared with the "
              "unclarified culture that produced it, a level passes when no increase is detected at "
              "α = `{python} ALPHA`, or when a detected increase is smaller than the resolution of the method that "
              "measured it.")
    for key in ("hcp", "residual_dna"):
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{UO}_{key}_impurity_release",
            f"At harvest, {names[key]} in the clarified harvest is judged {crit1}",
            [ref("sdm", q(s_impurity_crit)), ref("criteria", q(s_crit1_cmp))])
    add("attr:aggregates_hmw", "attribute_has_acceptance_criterion", f"lit:{UO}_aggregates_hmw_product_quality",
        t("At harvest, the high molecular weight content is judged by the product quality criterion of Version "
          "1.0, kept in Version 2.0: compared before and after the step, a level passes when no increase is "
          "detected at α = `{python} ALPHA`."),
        [ref("criteria", q(s_crit3)), ref("criteria", q(s_crit3_cmp))])
    # the plan's stated expectations from the mechanism of the step (not results)
    for key in ("hcp", "residual_dna"):
        add(pcid[rcf.key], "parameter_impacts_attribute", f"attr:{key}",
            f"A higher centrifugal field is expected to break more cells, and broken cells release "
            f"{'host cell protein' if key == 'hcp' else 'DNA'} into the centrate; the study establishes the "
            f"effect of the centrifugal field on it.",
            [ref("uo", q(s_breaks)), ref("uo", q(s_broken)), ref("objectives", q(s_obj2))])
    add(pcid[dfl.key], "parameter_impacts_attribute", "attr:residual_dna",
        "The depth filter media adsorb part of the DNA, and the share they take up can change with the depth "
        "filter load.", [ref("risk", q(s_dna_share))])

    # ==== plan statements ============================================================================
    ST = []

    def st(txt, refs):
        ST.append(ReportStatement(
            statement_id=f"{DOC}-S{len(ST) + 1:03d}", statement_text=txt, confidence="high",
            review_status="accepted", source_references=refs))

    def sq(sec, src_, txt=None, also=()):
        """A statement of one sentence of section ``sec``: ``src_`` is its .qmd source, ``txt`` the
        statement in .qmd form (the sentence itself when omitted, with a full stop where the quote ends
        before a citation or a cross-reference). ``also`` cites further (section, source) spans."""
        txt_ = t(txt) if txt else q(src_)
        st(txt_ if txt_.endswith(".") else txt_ + ".",
           [ref(sec, q(src_))] + [ref(s_, q(x)) for s_, x in also])

    # Purpose and scope
    sq("purpose", s_scope, "PCP-004 defines the process characterization study of harvest and clarification, "
                           "Step `{python} uo.step` of the A-Mab drug substance process.")
    sq("purpose", "It states which parameters are studied, how the study is run and analysed, and the criteria by which its results are judged.",
       "PCP-004 states which parameters are studied, how the study is run and analysed, and the criteria by "
       "which its results are judged.")
    sq("purpose", "Version 2.0 amends Version 1.0 after the study ran", "Version 2.0 of PCP-004 amends Version "
       "1.0 after the study ran.")
    sq("purpose", s_separates)
    sq("purpose", s_train)
    sq("purpose", 'At commercial scale the step is run once per batch on the contents of a `{python} f"{SCALE_L:,}"`\\ L production bioreactor.')
    sq("purpose", "The centrifuge and the filters are not expected to change a quality attribute of the antibody.")
    sq("purpose", s_frag_form)
    sq("purpose", "That feed should carry little intact cell material and fine debris, and the operation should break few cells, because broken cells release host cell protein and DNA into it.",
       "The feed to Protein A capture should carry little intact cell material and fine debris, and the "
       "operation should break few cells, because broken cells release host cell protein and DNA into it.",
       also=[("purpose", s_feed)])
    st("Each parameter of the step is studied one factor at a time on a scale-down model of the harvest train, "
       "over a range that extends beyond its normal operating range (NOR).",
       [ref("purpose", q(s_oneatatime)), ref("purpose", q(s_beyond))])
    sq("purpose", s_responses, "The responses of the study are the impurity burden of the clarified harvest, its "
       "particulate content, the pressure that the filter train develops, the size-variant profile of the "
       "antibody across the step and the step yield.")
    sq("purpose", s_challenge, "In the turbidity series the responses also include the column pressure and the "
       "cycle yield of a Protein A load challenge.")
    sq("purpose", "The study supports the transfer of the drug substance process from the development site in `{python} SENDING_LOCATION` to the commercial drug substance site in `{python} RECEIVING_LOCATION`.")
    sq("purpose", "It forms part of the Stage 1 process design record of the commercial process",
       "The study forms part of the Stage 1 process design record of the commercial process.")
    sq("purpose", "Lower viability releases more host cell protein and DNA into the culture fluid before harvest.")
    # Changes in this revision
    sq("changes", s_v1_approved, "Version 1.0 of PCP-004 was approved on `{python} REV1_DATE`, before the "
       "univariate study `{python} UNI_ID` began on `{python} UNI_START`.")
    sq("changes", 'Version 2.0 is issued after that study ran, under the QA investigation `{python} INV["id"]`, which examined acceptance criteria that had been set after data review for the analysis of proven acceptable ranges.',
       'Version 2.0 is issued after the study ran, under the QA investigation `{python} INV["id"]`, which '
       'examined acceptance criteria that had been set after data review for the analysis of proven acceptable '
       'ranges.')
    sq("changes", 'QA opened the investigation on `{python} INV["opened"]`, after its review of the master report PCMR-001 Version 1.0 for BLA readiness, and closed it on `{python} INV["closed"]` with the classification `{python} INV["classification"]`.',
       'QA opened `{python} INV["id"]` on `{python} INV["opened"]`, after its review of the master report '
       'PCMR-001 Version 1.0 for BLA readiness, and closed it on `{python} INV["closed"]` with the '
       'classification `{python} INV["classification"]`.')
    sq("changes", "The investigation found that the criteria used to judge each step in the proven acceptable range (PAR) analysis had been set after the data were seen and were in no approved protocol (INV-001 finding 1).",
       "INV-001 found that the criteria used to judge each step in the proven acceptable range (PAR) analysis "
       "had been set after the data were seen and were in no approved protocol (INV-001 finding 1).")
    sq("changes", s_applies, "Version 2.0 applies the rules of the master plan PCMP-001 Version 2.0 to the step.")
    sq("changes", "PCMP-001 Version 2.0 derives intermediate acceptance criteria from the drug substance criteria and the platform worst cases, with no data from the studies they judge, and it verifies the platform worst cases on which they rely (PCMP-001 §7.3 and §7.5).")
    sq("changes", "The decision criteria of Version 1.0 are kept.",
       "The decision criteria of Version 1.0 are kept in Version 2.0 (change 1).")
    sq("changes", "PCMP-001 §7.1 judges a scale-down model by its offset from manufacturing scale, not by a test for a difference between the scales.")
    sq("changes", "This replaces the Version 1.0 acceptance criterion that no performance measure should differ between the scales at α = 0.05, with the model modified where one did.",
       "The offset rule replaces the Version 1.0 acceptance criterion that no performance measure should differ "
       "between the scales at α = 0.05, with the model modified where one did (change 2).")
    sq("changes", "The design and the procedure of the qualification are those of Version 1.0.")
    sq("changes", "Version 1.0 listed host cell protein, residual DNA and aggregate as the quality attributes in scope.")
    st("Because the drug substance CQA register of Version 2.0 assigns fragments to the step, fragments are "
       "added to the attributes in scope and the nrCE-SDS method validation AMV-3020 to the procedures of the "
       "plan (change 3).",
       [ref("changes", q(s_register)), ref("changes", q(s_amv3020))])
    sq("changes", s_amd)
    sq("changes", "This answers INV-001 finding 6, that size exclusion chromatography (SEC) overestimates low molecular weight species where host cell protein co-elutes.",
       "The method decision answers INV-001 finding 6, that size exclusion chromatography (SEC) overestimates "
       "low molecular weight species where host cell protein co-elutes.")
    sq("changes", s_frag_uni, "Fragments were not among the responses of the univariate study of PCP-004, which "
       "closed before AMD-001.")
    sq("changes", "PCMP-001 §6.2 sets the significance level for the campaign at α = `{python} ALPHA`, the level at which Version 1.0 of this plan already tested effects.",
       "PCMP-001 §6.2 sets the significance level for the campaign at α = `{python} ALPHA`, the level at which "
       "Version 1.0 of PCP-004 already tested effects.")
    sq("changes", "PCMP-001 Version 2.0 sets the rule by which each parameter is classified.")
    sq("changes", "An attribute is affected by a parameter when the effect of the parameter on it is significant at that level (PCMP-001 §6.2), and the class follows from the size of the effect across the proven acceptable range and the margin of that range to the NOR (PCMP-001 §7.7).")
    sq("changes", "Version 1.0 left the decision logic to SOP-4001 and the evidence of the study",
       "Version 1.0 left the decision logic of the classification to SOP-4001 and the evidence of the study.")
    st(t("The plan records the execution window of the univariate study `{python} UNI_ID` (change 6)."),
       [ref("changes", q("records the execution window of the univariate study `{python} UNI_ID`."))])
    sq("changes", 'The Version 1.0 title block carried `{python} REV1["effective"]`, the date on which the Version 1.0 reports were approved, in place of the approval date of this plan.',
       'The Version 1.0 title block of PCP-004 carried `{python} REV1["effective"]`, the date on which the Version '
       '1.0 reports were approved, in place of the approval date of the plan.')
    sq("changes", "The revision history now gives that approval date (INV-001 finding 5).",
       "The revision history of Version 2.0 gives the approval date of Version 1.0 (INV-001 finding 5).")
    sq("changes", "Where Version 1.0 set no value or rule that the report needs, this plan says so and sets none.",
       "Where Version 1.0 set no value or rule that the report needs, PCP-004 says so and sets none (change 7).")
    sq("changes", 'The descriptions of Version 1.0 listed below are corrected without a change to the design, and each corrected sentence is marked "(corrected, change 7)" where it stands.',
       'Change 7 corrects descriptions of Version 1.0 without a change to the design, and each corrected '
       'sentence is marked "(corrected, change 7)" where it stands.')
    # each correction of change 7: the Version 1.0 sentence, the correction, and the corrected sentence in place
    corrections = [
        ("Change 7 corrects the description of settling in the disc stack. Version 1.0 said that a particle that "
         "has not reached the bowl wall when the fluid leaves is swept out in the centrate; in a disc stack a "
         "particle settles onto a disc, is captured there and slides outward to the bowl wall.",
         ["Version 1.0 said that a particle that has not reached the bowl wall when the fluid leaves is swept out in the centrate.",
          "In a disc stack a particle settles onto a disc, is captured there and slides outward to the bowl wall."],
         [("uo", s_settle)]),
        ("Change 7 corrects the description of shear in the centrifuge. Version 1.0 said that shear in the feed "
         "zone and at the disc stack rises with the speed of the bowl; the shear acts in the feed zone, where the "
         "feed is accelerated to the speed of the bowl, and the flow between the discs is laminar and low in shear.",
         ["Version 1.0 said that shear in the feed zone and at the disc stack rises with the speed of the bowl.",
          "The shear acts in the feed zone, where the feed is accelerated to the speed of the bowl, and the flow between the discs is laminar and low in shear."],
         [("uo", s_shear)]),
        ("Change 7 corrects the description of the passes through the feed zone. Version 1.0 said that the "
         "centrifuge recirculates part of its contents, so that the fluid passes the feed zone more than once; a "
         "continuous disk-stack centrifuge passes the feed through its feed zone once, and the cell damage that a "
         "bench model does not fully reproduce comes from the acceleration of the feed in the feed zone and from "
         "the periodic discharge of solids.",
         ["Version 1.0 said that the centrifuge recirculates part of its contents, so that the fluid passes the feed zone more than once.",
          "A continuous disk-stack centrifuge passes the feed through its feed zone once, and the cell damage that a bench model does not fully reproduce comes from the acceleration of the feed in the feed zone and from the periodic discharge of solids."],
         [("sdm", s_once), ("sdm", s_damage), ("risks", s_lysis)]),
        ("Change 7 corrects the description of the field and the sigma factor. Version 1.0 said that a setting in "
         "`{python} rcf.unit` means the same thing at both scales; at each field of the series the bench feed rate "
         "is set so that its ratio of flow to sigma factor equals that of the commercial centrifuge at the same "
         "field and the commercial feed rate.",
         ["Version 1.0 said that a setting in `{python} rcf.unit` means the same thing at both scales.",
          "At each field of the series the bench feed rate is set so that its ratio of flow to sigma factor equals that of the commercial centrifuge at the same field and the commercial feed rate."],
         [("sdm", s_sigma)]),
        ("Change 7 corrects the description of turbidity and the field. Version 1.0 said that the field and the "
         "filter load produce the turbidity together; a higher field lowers the turbidity by passing fewer cells "
         "and less debris, and it can raise it by breaking more cells into fine debris.",
         ["Version 1.0 said that the field and the filter load produce the turbidity together.",
          "A higher field lowers it by passing fewer cells and less debris, and it can raise it by breaking more cells into fine debris."],
         [("uo", s_turb_field)]),
        ("Change 7 corrects the description of the depth filter load. Version 1.0 tied the saturation of the media "
         "to the mass of solids per unit area and carried the load in `{python} dfl.unit`; the load in "
         "`{python} dfl.unit` is the volume of centrate per unit of media area, and the solids that this volume "
         "carries set the saturation.",
         ["Version 1.0 tied the saturation of the media to the mass of solids per unit area and carried the load in `{python} dfl.unit`.",
          "The load in `{python} dfl.unit` is the volume of centrate per unit of media area, and the solids that this volume carries set the saturation."],
         [("uo", s_load_unit)]),
        ("Change 7 corrects the description of aggregate. Version 1.0 said that shear at the feed zone could unfold "
         "the antibody; an air-liquid interface, in the feed zone or in a foaming transfer, can unfold it, and "
         "shear breaks cells.",
         ["Version 1.0 said that shear at the feed zone could unfold the antibody.",
          "An air-liquid interface, in the feed zone or in a foaming transfer, can unfold it, and shear breaks cells."],
         [("cqas", s_three)]),
        ("Change 7 corrects the description of the ranges and the levels. Version 1.0 said that every range studied "
         "is wider than the NOR at both ends, that the depth filter load range reaches well beyond its upper NOR "
         "limit, and that every planned level is a value of the control strategy; for "
         "`{python} join_and(upper_only)` only the upper edge of the range studied extends beyond the NOR, the "
         "depth filter load range reaches beyond its upper NOR limit, and three of the five levels are values of "
         "the control strategy. A note to the parameter table adds that `{python} N_TURB` is measured, not set, in "
         "the `{python} N_RCF` and `{python} N_DFL` series.",
         ["Version 1.0 said that every range studied is wider than the NOR at both ends, that the depth filter load range reaches well beyond its upper NOR limit, and that every planned level is a value of the control strategy.",
          "For `{python} join_and(upper_only)` only the upper edge of the range studied extends beyond the NOR, the depth filter load range reaches beyond its upper NOR limit, and three of the five levels are values of the control strategy.",
          "adds that `{python} N_TURB` is measured, not set, in the `{python} N_RCF` and `{python} N_DFL` series."],
         [("risk", s_upper_only), ("factors", s_rng_dfl), ("univariate", s_three_cs)]),
        ("Change 7 corrects the description of the size-variant samples. Version 1.0 said that the intermediate "
         "sample points would not locate a change in the size-variant profile; a sample of the centrate would "
         "locate it, and the centrate is not tested for size variants.",
         ["Version 1.0 said that the intermediate sample points would not locate a change in the size-variant profile.",
          "A sample of the centrate would locate it, and the centrate is not tested for size variants."],
         [("sampling", s_sv_centrate)]),
        ("Change 7 corrects the description of the analysis. Version 1.0 said that a change smaller than the method "
         "can resolve would not be reported as an effect, that the decisions of its criteria rest on the size of an "
         "effect against the precision of its method, and that residual DNA lies close to the limit of quantitation "
         "of the qPCR; such a change is reported as detected and not material, the decisions also rest on "
         "significance and on an absolute limit, and the residual DNA of a clarified harvest lies far above that "
         "limit.",
         ["Version 1.0 said in its method section that a change smaller than the method can resolve would not be reported as an effect, that the decisions of its criteria rest on the size of an effect against the precision of its method, and that residual DNA lies close to the limit of quantitation of the qPCR.",
          "Such a change is reported as detected and not material",
          "the decisions also rest on significance and on an absolute limit, and the residual DNA of a clarified harvest lies far above that limit."],
         [("stats", s_resolve), ("stats", s_decisions)]),
        ("Change 7 corrects the presumed results of Version 1.0. Version 1.0 said that the study would confirm that "
         "the NOR lies inside the PAR, that the drug substance criteria are met by the clearance downstream, that "
         "the NOR will be shown nested inside the PAR, and what the step contributes to the control strategy; "
         "Version 2.0 states each as an intention.",
         ["Version 1.0 said that the study would confirm that the NOR lies inside the PAR, that the drug substance criteria are met by the clearance downstream, that the NOR will be shown nested inside the PAR, and what the step contributes to the control strategy.",
          "This plan states each as an intention."],
         [("objectives", s_obj5), ("cqas", s_ds_not_ipc), ("par", s_nor_in_par), ("par", s_provide)]),
    ]
    titles = [v[-1] for v in SEC.values()]
    for txt, said, where in corrections:
        at = join_and(sorted({SEC[s_][-1] for s_, _ in where}, key=titles.index))
        st(t(txt) + f" The corrected text stands, marked, in {at}.",
           [ref("changes", q(x)) for x in said] + [ref(s_, q(x)) for s_, x in where])
    sq("changes", "The design, the sampling, the procedures and the decision rules of Version 1.0 are otherwise kept in its words, except the descriptions corrected under change 7.")
    # Objectives
    for o in (s_obj1, s_obj2,
              "Establish the effect of depth filter load, over `{python} f0(dfl.prange[0])` `{python} dfl.unit` to `{python} f0(dfl.prange[1])` `{python} dfl.unit`, on the particulate content of the clarified harvest and on the pressure the filter train develops.",
              "Establish whether the step alters the size-variant profile of the antibody, and establish the effect of post-clarification turbidity, over `{python} f0(turb.prange[0])` `{python} turb.unit` to `{python} f0(turb.prange[1])` `{python} turb.unit`, on the material presented to capture."):
        sq("objectives", o, "Objective: " + o[0].lower() + o[1:].rstrip(".") + ".")
    sq("objectives", s_obj5, "Objective: define a proven acceptable range for each parameter, determine whether "
       "the normal operating range lies inside the proven acceptable range, and provide the evidence on which "
       "each parameter will be classified under the parameter classification procedure SOP-4001.")
    sq("objectives", s_class_out)
    # Related documents
    st("The risk assessment RA-001 decides which parameters are studied and by which type of study, and the "
       "paired report PCR-004 reports the study that PCP-004 sets out.",
       [ref("related", q("The risk assessment RA-001 decides which parameters are studied and by which type of study")),
        ref("related", q("and the paired report PCR-004 reports the study that this plan sets out."))])
    sops = [r_ for r_ in sop_df["Reference"] if r_.startswith("SOP-")]
    st("The procedures that govern the study are "
       + join_and([f"{r_} ({dict(zip(sop_df['Reference'], sop_df['Title']))[r_]})" for r_ in sops]) + ".",
       [tref("related", sop_t, soprow, r_) for r_ in sops])
    # Unit-operation description and prior knowledge
    sq("uo", s_centrifuge)
    sq("uo", "Cells and debris settle under the centrifugal field, at a velocity that rises with the field and with the difference between their density and the density of the medium.")
    sq("uo", s_settle, "In the disc stack a particle settles onto a disc, is captured there and slides outward "
       "to the bowl wall, from which the solids are discharged at intervals (a sentence corrected under change "
       "7).")
    sq("uo", "A higher feed rate shortens the time the fluid spends in the stack, so that more of the small particles escape capture.")
    sq("uo", s_centrate)
    st("The depth filter train removes the fine debris and the colloidal material that the centrate still "
       "carries; its media are positively charged, so they adsorb part of the DNA and fine debris as well as "
       "retaining particles by size.", [ref("uo", q(s_depth)), ref("uo", q(s_media)), ref("uo", q(s_centrate))])
    sq("uo", s_sterile, "The filtrate of the depth filter train passes the sterilizing-grade filter into the "
       "harvest vessel, where it is held until capture.")
    st("A higher centrifugal field clarifies more completely, because cells and debris settle faster and fewer "
       "escape capture, and it can also break more cells.",
       [ref("uo", q("A higher centrifugal field clarifies more completely, because cells and debris settle faster and fewer escape capture.")),
        ref("uo", q(s_breaks))])
    sq("uo", s_shear, "The culture is accelerated to the speed of the bowl in the feed zone, and the shear there "
       "rises with that speed, while the flow between the discs is laminar and low in shear (a sentence "
       "corrected under change 7).")
    sq("uo", s_broken)
    sq("uo", "The set-point balances clarification against cell breakage.",
       "The set-point of the centrifugal field balances clarification against cell breakage.")
    sq("uo", "A depth filter has a finite capacity for the solids and colloids that the centrifuge passes.")
    sq("uo", "As retained solids fill the void space of the matrix and occupy its charged sites, the pressure drop across the filter rises and more fine material passes.")
    sq("uo", "At the extreme, cells and debris are forced through the pores.",
       "At the extreme of depth filter loading, cells and debris are forced through the pores.")
    sq("uo", "How far the media are saturated depends on the volume of centrate that each unit of media area has received and on the solids that this volume carries.")
    sq("uo", s_load_unit, "For this reason depth filter load is expressed as the volume of centrate loaded per "
       "unit of media area, in `{python} dfl.unit` (a sentence corrected under change 7).")
    sq("uo", s_turb_field, "A higher centrifugal field lowers post-clarification turbidity, because fewer cells "
       "and less debris reach the filters, and it can also raise it, because more broken cells leave fine "
       "debris (a sentence corrected under change 7).")
    sq("uo", "It rises as the filter load approaches the capacity of the media.",
       "Post-clarification turbidity rises as the filter load approaches the capacity of the media.")
    sq("uo", "It is monitored on every batch as an in-process control.",
       "Post-clarification turbidity is monitored on every batch as an in-process control.",
       also=[("uo", s_turb_meas)])
    sq("uo", "It is listed among the parameters of the step because the particulate and colloidal load that it measures reaches the Protein A column, where it fouls the bed and shortens the working life of the resin.",
       "Post-clarification turbidity is listed among the parameters of the step because the particulate and "
       "colloidal load that it measures reaches the Protein A column, where it fouls the bed and shortens the "
       "working life of the resin.")
    sq("uo", "Harvest by continuous centrifugation and depth filtration is the platform recovery operation at `{python} COMPANY`.")
    sq("uo", "It was used for three earlier antibodies (X-Mab, Y-Mab and Z-Mab), and the equipment, the grade of the filter media and the control scheme are unchanged for A-Mab.",
       "The platform recovery operation was used for three earlier antibodies (X-Mab, Y-Mab and Z-Mab), and "
       "the equipment, the grade of the filter media and the control scheme are unchanged for A-Mab.")
    sq("uo", "The mechanisms above are therefore expected to hold for A-Mab, and the platform experience gives the approximate position of the operating point.",
       "The mechanisms of the step are therefore expected to hold for A-Mab, and the platform experience gives "
       "the approximate position of the operating point.")
    sq("uo", "Host cell protein and DNA enter harvest at a concentration that rises as the viability of the culture falls, because cells that died before harvest have already released their contents into the medium.")
    sq("uo", "Viability at the end of culture is a property of the A-Mab culture and is characterized under the production bioreactor plan PCP-003.")
    sq("uo", "The ranges in this plan are therefore established on A-Mab material.",
       "The ranges of PCP-004 are therefore established on A-Mab material.")
    sq("uo", "The A-Mab case study assumes, for simplicity, that harvest has no impact on product quality, and it notes that this might not hold in a real process")
    sq("uo", "This plan keeps that assumption, and the criteria of PCMP-001 Version 2.0 rest on it",
       "PCP-004 keeps the assumption that harvest has no impact on product quality, and the criteria of "
       "PCMP-001 Version 2.0 rest on it.")
    sq("uo", "The study tests it where cell breakage could release host cell protein and DNA, and where air-liquid interfaces could add aggregate.",
       "The study tests the assumption where cell breakage could release host cell protein and DNA, and where "
       "air-liquid interfaces could add aggregate.")
    # Quality attributes in scope
    sq("cqas", "lists the four quality attributes in scope, with the criticality and the drug substance criterion of each.",
       "The plan lists four quality attributes in scope, with the criticality and the drug substance criterion "
       "of each.")
    for key in ckeys:
        i = ckeys.index(key)
        refs = [tref("cqas", cq_t, crow, key)]
        head = head_of(crow, key)
        if head != key:
            refs.append(tref("cqas", cq_t, crow, head))
        st(f"{names[key]}, a {cq_df['Category'].iloc[i]}, has criticality {cq_df['Criticality'].iloc[i]}, a "
           f"Tool #1 score of {cq_df['Tool #1'].iloc[i]} and the drug substance criterion "
           f"{cq_df['Acceptance'].iloc[i]}.", refs)
    sq("cqas", "The Tool #1 score is the product of the impact score and the uncertainty score of the ranking tool of the A-Mab case study")
    st(cq_notes[0], [ref("cqas", cq_notes[0], cq_t)])
    st(f"For residual DNA a dose is {ns['DOSE']['mg_per_kg']:g} mg/kg (A-Mab case study) for a reference adult of "
       f"{ns['DOSE']['body_weight_kg']:g} kg, an assumption of the campaign, so {ns['DOSE_MG']:g} mg of antibody.",
       [ref("cqas", cq_notes[1], cq_t)])
    sq("cqas", s_enter)
    sq("cqas", s_three, "Host cell protein, DNA and aggregate are in scope because shear and air-liquid "
       "interfaces in the centrifuge and the filters can break cells, which adds host cell protein and DNA, and "
       "because an air-liquid interface in the feed zone or in a foaming transfer can unfold the antibody and "
       "add aggregate (a sentence corrected under change 7).")
    sq("cqas", s_agg_less)
    sq("cqas", s_dna_vl, "Residual DNA has very low criticality, and it is measured because DNA fragments and "
       "nucleosomes foul depth filters and Protein A resin, so it describes the condition of the feed even where "
       "its own criterion is far from binding.",
       also=[("cqas", "It is measured because DNA fragments and nucleosomes foul depth filters and Protein A resin, so it describes the condition of the feed even where its own criterion is far from binding.")])
    sq("cqas", s_frag_def)
    sq("cqas", "Clipping starts in the reactor, where proteases released by dead and lysing cells act on the secreted antibody.")
    sq("cqas", "It continues in the clarified harvest, because clarification removes the cells but not the proteases already in solution, and its rate rises with temperature.",
       "Clipping continues in the clarified harvest, because clarification removes the cells but not the "
       "proteases already in solution, and its rate rises with temperature.")
    sq("cqas", "A longer culture ends at lower viability and carries more protease into harvest.")
    sq("cqas", s_frag_crit)
    sq("cqas", s_ds_not_ipc, "The drug substance criteria of the attribute table are to be met by the clearance "
       "that the purification train delivers after the step, and they are not in-process limits for the "
       "clarified harvest (a sentence corrected under change 7).")
    # Risk-based prioritization of parameters
    sq("risk", s_ra)
    sq("risk", "RA-001 ranked each parameter on its potential to affect a quality attribute and on its potential to interact with another parameter, and it assigned a study type from the combined ranking.")
    sq("risk", "It brought `{python} n_par` parameters of this step into scope and assigned each of them to univariate study",
       "RA-001 brought `{python} n_par` parameters of the step into scope and assigned each of them to "
       "univariate study.")
    sq("risk", s_no_mv)
    sq("risk", "The feed rate follows the ratio of flow to sigma factor, the depth filtration runs at constant flux, and the temperature is held at the commercial set-point.",
       "The other operating conditions are held constant: the feed rate follows the ratio of flow to sigma "
       "factor, the depth filtration runs at constant flux, and the temperature is held at the commercial "
       "set-point.", also=[("risk", "The other operating conditions are held constant")])
    sq("risk", s_dna_share)
    sq("risk", s_clear, also=[("risk", "A poorly chosen setting is therefore expected to load capture more heavily without changing the drug substance.")],
       txt="Protein A capture and the two ion exchange steps clear the host cell protein and DNA that cell "
           "breakage releases, so a poorly chosen setting is expected to load capture more heavily without "
           "changing the drug substance.")
    sq("risk", "The range studied extends beyond the NOR at both ends for `{python} join_and(both_sides)`.")
    sq("risk", s_upper_only, "For `{python} join_and(upper_only)` the lower edge of the range studied is the "
       "lower limit of the NOR, and only the upper edge extends beyond it (a sentence corrected under change 7).")
    sq("risk", "A range that stops at the NOR limits cannot show where the operation begins to fail, and an excursion beyond a NOR limit would then be a deviation with no data behind it.")
    sq("risk", "The wider ranges also cover settings that the receiving site may need if its equipment differs from the development equipment.")
    # Materials and methods
    sq("methods", "The materials and methods are those of Version 1.0.",
       "The materials and methods of PCP-004 are those of Version 1.0.")
    sq("methods", "Where this amendment applies a rule of PCMP-001 Version 2.0, the text names it.")
    # Scale-down model and its qualification
    sq("sdm", s_sdm)
    sq("sdm", s_three_parts, "The scale-down model reproduces the commercial operation in three parts, and each "
       "part is matched on the quantity that drives its own mechanism and not on the size of the equipment.")
    sq("sdm", "Matching on volume or on bowl diameter alone would leave the shear at the feed zone, the settling in the bowl and the loading of the filter media free to differ between the scales.")
    sq("sdm", s_shear_dev)
    sq("sdm", s_lab_cent)
    sq("sdm", s_sigma, "At each field of the series the bench feed rate will be set so that its ratio of flow to "
       "sigma factor equals that of the commercial centrifuge at the same field and the commercial feed rate (a "
       "sentence corrected under change 7).")
    sq("sdm", s_disks)
    sq("sdm", s_qual_cmp, "Qualification will compare the scale-down model with the commercial train at the "
       "set-point condition on the same culture.")
    sq("sdm", s_qual_cover, "The qualification comparison will cover centrate turbidity, solids removal, host "
       "cell protein and DNA in the clarified harvest, filter pressure at the end of the load, and step yield.")
    st("Replicate qualification runs will be performed at each scale, and at commercial scale each replicate is a "
       "separate batch.", [ref("sdm", q(s_qual_rep)), ref("sdm", q(s_qual_batch))])
    sq("sdm", "PCMP-001 §7.1 replaces the Version 1.0 acceptance criterion of this comparison (change 2).",
       "PCMP-001 §7.1 replaces the Version 1.0 acceptance criterion of the qualification comparison (change 2).")
    sq("sdm", 'It judges each output by its offset, the mean of the scale-down runs at set-point minus the mean of the commercial batches, with its two-sided `{python} f"{OFFSET_CI * 100:.0f}"`\\ % confidence interval.',
       'PCMP-001 §7.1 judges each output of the qualification by its offset, the mean of the scale-down runs at '
       'set-point minus the mean of the commercial batches, with its two-sided '
       '`{python} f"{OFFSET_CI * 100:.0f}"` % confidence interval.')
    sq("sdm", "Step yield, centrate turbidity, solids removal and filter pressure have no criterion at this step, so their offsets would only be recorded.")
    sq("sdm", s_impurity_crit, "In the qualification, host cell protein and DNA are judged against the impurity "
       "release criterion (criterion 1).")
    sq("sdm", s_qual_rsm)
    sq("sdm", s_no_qual_rule, "PCP-004 sets no qualification rule for the scale-down model, and PCR-004 states "
       "its approach.")
    sq("sdm", s_runs_ask)
    sq("sdm", s_runs_none, "Version 1.0 named neither the number of runs at each scale nor the "
       "manufacturing-scale data set, and the amendment, issued after the study, does not add them.")
    sq("sdm", s_turb_offset)
    sq("sdm", s_sv_offset, "The size variants and the column pressure and the cycle yield of the Protein A load "
       "challenge are not in the qualification comparison either.")
    st("A continuous disk-stack centrifuge passes the feed through its feed zone once, and the cell damage that a "
       "bench model does not fully reproduce comes from the acceleration of the feed in the feed zone, which "
       "the shear device matches only in its energy dissipation rate, and from the periodic discharge of solids "
       "(a passage corrected under change 7).", [ref("sdm", q(s_once)), ref("sdm", q(s_damage))])
    sq("sdm", "The model therefore represents the field and the residence time well and that cell damage less well, and it is expected to under-represent lysis rather than to over-represent it.",
       "The scale-down model represents the field and the residence time well and the cell damage of the feed "
       "zone less well, and it is expected to under-represent lysis rather than to over-represent it.")
    sq("sdm", s_bound, "The study uses the scale-down model to bound ranges and to establish the direction and "
       "the approximate size of each effect.")
    sq("sdm", s_no_abs, "The study does not use the scale-down model to predict the absolute impurity "
       "concentration of a commercial batch.")
    # Operation
    sq("operation", "Each characterization run will be executed as a single pass of the whole harvest through the model train, in the order the commercial operation runs it.")
    sq("operation", "The culture will be taken from the production bioreactor scale-down model at the end of culture, at the conditions characterized under the production bioreactor plan PCP-003.")
    sq("operation", "Culture from the qualified bioreactor model matters here, because a culture that ends at lower viability enters harvest with more host cell protein already released into the medium and with more fragile cells.",
       "Culture from the qualified bioreactor model matters, because a culture that ends at lower viability "
       "enters harvest with more host cell protein already released into the medium and with more fragile "
       "cells.")
    sq("operation", "Both raise the impurity concentration of the clarified harvest, whatever the centrifuge does.",
       "More released host cell protein and more fragile cells both raise the impurity concentration of the "
       "clarified harvest, whatever the centrifuge does.")
    sq("operation", "Where the volume allows, one culture will be split between the levels of a parameter, so that the levels of a series are compared on the same material.")
    sq("operation", "The culture will be fed to the centrifuge model at the field setting for the run and at the matched ratio of flow to sigma factor.")
    sq("operation", "The centrate will be collected, sampled, and passed over the depth filter train at constant flux to the load per unit area for the run, and then over a sterilizing-grade filter into the harvest container.")
    sq("operation", "Temperature will be held at the commercial set-point throughout.",
       "In each characterization run the temperature will be held at the commercial set-point throughout.")
    sq("operation", "The time between the end of culture and the end of clarification will be held constant across the runs, since a longer hold on unclarified culture allows further lysis and would confound the comparison the study is making.")
    sq("operation", "Every parameter not varied in a run will be held at its set-point")
    # Analytical methods
    sq("analytical", s_amv3015)
    sq("analytical", s_amv3011)
    sq("analytical", s_no_conc)
    sq("analytical", s_amv3011_perf)
    for amv, row in perfrow.items():
        r_ = perf_df[perf_df["Reference"] == amv].iloc[0]
        st(f"{amv} ({r_['Method']}) has a validated precision of {r_['prec']} % RSD for a single result, a limit "
           f"of quantitation of {r_['LOQ']} and an accuracy of {r_['acc']} %.",
           [tref("analytical", perf_t, perfrow, amv)])
    st(perf_note, [ref("analytical", perf_note, perf_t)])
    sq("analytical", "Samples for host cell protein and for DNA will be assayed in one analytical campaign per parameter series, with the same reagent lots where the schedule allows.")
    sq("analytical", "A trend across the levels of a parameter should not be confounded by a change of reagent lot part way through the series.")
    # Sampling plan
    sq("sampling", "Samples will be drawn at four points in every run.")
    sq("sampling", "The points, the methods applied at each and the purpose of each are listed in Appendix B")
    sq("sampling", "The sample of unclarified culture is the reference for the whole study.")
    sq("sampling", "Impurity released by the operation can only be seen as a difference from what entered it, so that sample will be drawn from the production bioreactor scale-down model at the end of culture, immediately before the feed to the centrifuge starts, and it will be assayed in the same campaign as the samples that follow it.",
       "Impurity released by the operation can only be seen as a difference from what entered it, so the sample "
       "of unclarified culture will be drawn from the production bioreactor scale-down model at the end of "
       "culture, immediately before the feed to the centrifuge starts, and assayed in the same campaign as the "
       "samples that follow it.")
    sq("sampling", "It shows what the centrifuge passed and therefore what the depth filter was asked to remove, which is the quantity that the depth filter load runs on centrate from `{python} G_LO` and from `{python} G_HI` vary",
       "The centrate sample separates the two stages of the operation: it shows what the centrifuge passed and "
       "therefore what the depth filter was asked to remove, the quantity that the depth filter load runs on "
       "centrate from `{python} G_LO` and from `{python} G_HI` vary.",
       also=[("sampling", "The centrate sample separates the two stages of the operation.")])
    sq("sampling", "The sample after depth filtration and the sample after sterilizing-grade filtration are both clarified harvest, and the second of them is the material capture receives.")
    sq("sampling", "Each level will be sampled once at each point.")
    sq("sampling", "The set-point condition will be run in replicate across the execution of the study, and those replicates provide the estimate of run to run variability against which every effect is tested.")
    sq("sampling", s_no_reps)
    sq("sampling", "Samples for size variants will be drawn at the first and the last point only.")
    sq("sampling", "The antibody meets air-liquid interfaces only briefly in the operation, so the step is not expected to change the size-variant profile")
    sq("sampling", s_sv_centrate, "The centrate is not tested for size variants, so a change found at the last "
       "point could not be placed at the centrifuge or at the filters (a sentence corrected under change 7).")
    # Statistical methods
    sq("stats", "Each response will be analysed against the parameter that was varied, by linear regression on the levels run, with the replicates at the set-point condition providing an independent estimate of error.")
    sq("stats", "Effects will be tested at α = `{python} ALPHA`, the significance level set for the campaign (PCMP-001 §6.2).")
    sq("stats", "Where the relationship is not linear over the range, a quadratic term may be fitted, and the fit will be reported with the terms that were needed rather than with the terms that were planned.")
    sq("stats", s_no_curv)
    sq("stats", "Statistical significance and practical significance will be reported separately.")
    sq("stats", "A significant slope will be reported together with the change it predicts across the normal operating range of that parameter, and that change will be compared with the precision of the method that measured the response")
    sq("stats", s_resolve)
    sq("stats", s_no_adeq)
    sq("stats", s_decisions, "The decisions of the acceptance and decision criteria rest on the significance of a "
       "change, on its size against the resolution of the method, or on an absolute limit, and not on the fit "
       "of a predictive model (a sentence corrected under change 7).")
    sq("stats", s_each_regression, "Each regression will be reported with its coefficient of determination and its "
       "residual standard error and will be judged on those.")
    sq("stats", "Results below the limit of quantitation of a method will be reported as such and excluded from the regression, and the number excluded will be given with the fit.")
    sq("stats", s_ofat, "The design of the study is one factor at a time.")
    sq("stats", s_no_inter, "A one-factor-at-a-time design cannot determine an interaction between two parameters, "
       "where the effect of one parameter on a response depends on the level of the other.")
    sq("stats", s_inter_exp)
    sq("stats", s_bracketed, "The interaction of the centrifugal field and the depth filter load will be "
       "bracketed and not estimated.")
    sq("stats", s_two_centrates)
    sq("stats", s_no_coef)
    sq("stats", s_no_rsm)
    sq("stats", s_setpoints_only)
    # Study design and factors
    sq("design", "The study design is that of Version 1.0.", "The study design of PCP-004 is that of Version 1.0.")
    sq("factors", "The set-points and the NORs are those against which the study was planned.",
       "The set-points and the NORs of the parameter table are those against which the study was planned.")
    for p in prm:
        st(f"{p.name}: set-point {f0(p.setpoint_characterized)} {p.unit}, range studied "
           f"{f0(p.prange[0])}–{f0(p.prange[1])} {p.unit}, NOR {f0(p.nor_characterized[0])}–"
           f"{f0(p.nor_characterized[1])} {p.unit}; studied one factor at a time.",
           [tref("factors", pt, prow, p.name)])
    sq("factors", s_rng_rcf)
    sq("factors", s_rng_dfl, "`{python} cap(N_DFL)` runs to `{python} f0(dfl.prange[1])` `{python} dfl.unit`, "
       "which loads the media beyond the upper NOR limit of `{python} f0(dfl.nor_characterized[1])` "
       "`{python} dfl.unit` and past the point at which the pressure drop is expected to rise (a sentence "
       "corrected under change 7).")
    sq("factors", s_rng_turb)
    sq("factors", "The set-point column is the condition at which every parameter not being varied will be held",
       "The set-point of each parameter is the condition at which it is held while another parameter is varied, "
       "and the set-point condition is run in replicate across the execution of the study.",
       also=[("sampling", "The set-point condition will be run in replicate across the execution of the study, and those replicates provide the estimate of run to run variability against which every effect is tested.")])
    # Univariate assessment
    sq("univariate", s_five)
    sq("univariate", "They are the lower edge of the range studied, the lower limit of the normal operating range, the set-point, the upper limit of the normal operating range and the upper edge of the range studied, and they are listed in Appendix A",
       "The five levels are the lower edge of the range studied, the lower limit of the normal operating range, "
       "the set-point, the upper limit of the normal operating range and the upper edge of the range studied.")
    sq("univariate", s_three_cs, "Three of the five levels are values that the control strategy uses, so the "
       "study reports directly on the limits it is meant to justify (a sentence corrected under change 7).")
    sq("univariate", s_four_levels)
    sq("univariate", "Runs will be executed in randomized order within each parameter series.")
    sq("univariate", "A drift in the culture, in the equipment or in an assay over the execution of a series would otherwise be read as an effect of the parameter.",
       "Randomized order guards against a drift in the culture, in the equipment or in an assay over the "
       "execution of a series, which would otherwise be read as an effect of the parameter.")
    sq("univariate", "Replicates at the set-point condition will be distributed across a series rather than run together, for the same reason.")
    sq("univariate", "The `{python} N_RCF` series will be run first, because its outcome supplies the centrate produced at `{python} G_LO` and at `{python} G_HI` on which the depth filter load series is run")
    sq("univariate", "The depth filter load series will follow.",
       "The depth filter load series will follow the `{python} N_RCF` series.")
    sq("univariate", "The turbidity series will be run last, because the material for it is produced by the two series before it.")
    sq("univariate", "Clarified harvest at a target turbidity will be prepared by blending clarified harvest with retained centrate to the target turbidity for the level, which allows the turbidity presented to capture to be varied independently of the settings that produced it.")
    sq("univariate", "Blended material carries the particle size distribution of the centrate it was made from, and that is not identical to the distribution a depth filter at the end of its capacity would pass.")
    sq("univariate", s_pa_column)
    sq("univariate", "The responses are the pressure developed across the column over the load and the yield of the cycle.",
       "The responses of the Protein A load challenge are the pressure developed across the column over the "
       "load and the yield of the cycle.")
    sq("univariate", s_no_lc_crit, "Version 1.0 set no criterion for the column pressure and the cycle yield of "
       "the load challenge, and the amendment sets none.")
    # Acceptance and decision criteria
    sq("criteria", "The master plan PCMP-001 Version 2.0 derives an intermediate acceptance criterion for a step output by carrying the drug substance criterion back through the platform worst case of every downstream step, with no margin (PCMP-001 §7.3).")
    sq("criteria", s_no_iac)
    sq("criteria", s_no_ver)
    st("The criteria of the production bioreactor output that pass through harvest rest on the assumption that "
       "harvest changes no attribute, which the impurity release criterion (1) and the product quality "
       "criterion (3) test.",
       [ref("criteria", q("Those criteria therefore rest on the assumption that harvest changes no attribute")),
        ref("criteria", q("which the impurity release criterion (1) and the product quality criterion (3) below test."))])
    sq("criteria", "The decision criteria below are those of Version 1.0, in its words.",
       "The decision criteria of PCP-004 are those of Version 1.0, in its words.")
    sq("criteria", "The impurity release criterion (1) and the product quality criterion (3) compare results within a run, and the clarification criterion (2) is an absolute limit.")
    sq("criteria", "No result of the studies under this plan was used to set or change these criteria.",
       "No result of the studies under PCP-004 was used to set or change its decision criteria.")
    st("Impurity release is the first criterion: host cell protein and residual DNA in the clarified harvest "
       "will be compared with the same measurements on the unclarified culture that produced it.",
       [ref("criteria", q(s_crit1)), ref("criteria", q(s_crit1_cmp))])
    sq("criteria", s_crit1_pass, "Under the impurity release criterion a level passes when no increase is "
       "detected at α = `{python} ALPHA`, or when a detected increase is smaller than the resolution of the "
       "method that measured it.")
    sq("criteria", "A setting that releases more impurity than that lies outside the acceptable range of its parameter.")
    st(t("Clarification is the second criterion and the absolute one: post-clarification turbidity of the "
         "clarified harvest will be compared with the upper limit of its normal operating range, "
         "`{python} f0(TURB_LIMIT)` `{python} turb.unit`."),
       [ref("criteria", q("Clarification is the second criterion and the absolute one.")),
        ref("criteria", q(s_crit2_cmp))])
    sq("criteria", "A centrifuge setting or a filter load that delivers clarified harvest above that value has failed to clarify, whatever the impurity results show.")
    st(t("Product quality is the third criterion: high molecular weight content will be compared before and after "
         "the step, and a level passes when no increase is detected at α = `{python} ALPHA`."),
       [ref("criteria", q(s_crit3)), ref("criteria", q(s_crit3_cmp))])
    sq("criteria", s_yield_ng)
    sq("criteria", "Yield will be given for every level and compared with the set-point replicates.")
    sq("criteria", s_no_yield)
    sq("criteria", "A loss of yield at a level will be reported with its cause and will be weighed in the choice of the operating range.")
    sq("criteria", "It will not on its own place a level outside the proven acceptable range.",
       "A loss of yield will not on its own place a level outside the proven acceptable range.")
    sq("criteria", "A parameter meets the criteria over a range when every level in that range passes the first three criteria.")
    sq("criteria", "The proven acceptable range of the parameter is then that range, bounded at the levels tested")
    sq("criteria", "Where a level fails, the proven acceptable range is bounded at the last level that passed, and the failure should be investigated before the range is reported.")
    sq("criteria", "A failure at a level inside the normal operating range means the operating range in force is not supported by the data, and it should be raised to Manufacturing Science and to Quality Assurance before the study continues, so that the normal operating range or the control strategy can be changed under SOP-4001.")
    sq("criteria", "Deviations from this plan during execution will be recorded, investigated and reported in PCR-004 with their impact on the conclusions, whether or not the affected runs are retained.")
    # Proven acceptable ranges (planned analysis)
    sq("par", s_par_rsm)
    sq("par", "PCMP-001 §4 states that the range of a parameter studied univariately is supported by its own data, so the proven acceptable range of each parameter of this step will be determined from the levels tested, by the rule of Version 1.0 below.",
       "PCMP-001 §4 states that the range of a parameter studied univariately is supported by its own data, so "
       "the proven acceptable range of each parameter of the step will be determined from the levels tested, by "
       "the rule of Version 1.0.")
    sq("par", "A proven acceptable range is the range of a parameter over which the step has been shown to meet its criteria, with every other parameter held at its set-point")
    sq("par", "A range established by varying one parameter at a time holds while the other parameters are at their set-points")
    sq("par", "A proven acceptable range is also bounded by the levels tested.")
    sq("par", s_par_whole)
    sq("par", s_v1_gave_no)
    sq("par", s_sets_none, "The amendment sets none of these four, and PCR-004 states its approach to each.")
    sq("par", "For each parameter, PCR-004 will give the range studied, the criterion applied, the response that came closest to that criterion, and the proven acceptable range that follows.")
    sq("par", s_nor_in_par, "PCR-004 will determine whether the normal operating range lies inside the proven "
       "acceptable range (a sentence corrected under change 7).")
    sq("par", "Where the two coincide at an edge, that will be stated, because a normal operating limit sitting on the edge of the proven range leaves no margin for the ordinary variability of the commercial operation.",
       "Where the normal operating range and the proven acceptable range coincide at an edge, that will be "
       "stated, because a normal operating limit on the edge of the proven range leaves no margin for the "
       "ordinary variability of the commercial operation.")
    sq("par", s_provide, "What the study is to provide to the control strategy is a proven acceptable range for "
       "each parameter, the position of the normal operating range against it, and an in-process control on "
       "the turbidity of the clarified harvest (a sentence corrected under change 7).")
    sq("par", "The classification of each parameter under SOP-4001 will be made in PCR-004 on the evidence this study produces, and it will roll up into PCMR-001 with the other steps of the train.")
    sq("par", "PCMP-001 Version 2.0 sets the rule for that classification (change 5).",
       "PCMP-001 Version 2.0 sets the rule for the classification of the parameters (change 5).")
    sq("par", "An attribute is affected by a parameter when the effect of the parameter on it is significant at the significance level set for the campaign (PCMP-001 §6.2).")
    sq("par", "A critical process parameter (CPP) and a well-controlled critical process parameter (WC-CPP) both affect a CQA, and they differ in the risk that the parameter falls outside its acceptable range in operation.")
    sq("par", "A key process parameter (KPP) affects process performance and no CQA, and a general process parameter (GPP) affects neither (PCMP-001 §7.7).")
    sq("par", s_pcr_state,
       "PCR-004 will state, for each parameter, the size of each effect across the proven acceptable range and "
       "the margin of that range to the normal operating range, and it will give the reason for each class from "
       "those two quantities.", also=[("par", s_no_thresh)])
    # Data management and integrity
    sq("data", "Data from this study will be recorded, reviewed and retained under the site data governance procedures, and the ALCOA+ principles apply to every record the study produces.")
    sq("data", "Runs will be executed against a pre-approved batch record for the scale-down train.")
    sq("data", "Each entry will be made at the time it is observed and signed by the person who made it.")
    sq("data", "Analytical results will be acquired and stored in the validated laboratory information management system (LIMS), with the audit trail enabled and reviewed as part of result approval.")
    sq("data", "Equipment used to set or to measure a parameter of this study will be within its calibration at the time of use, and the calibration status will be recorded with the run.")
    sq("data", "The first and the last day of execution of each study will be recorded with its data, as PCMP-001 Version 2.0 requires, and PCMP-001 Table 9.1 records them for the univariate study `{python} UNI_ID`.")
    sq("data", "Raw data, the analysis script and the outputs of that script will be retained together, so that the tables in PCR-004 can be regenerated from the raw data without a manual step.")
    sq("data", "Any change to a recorded value will be made as a corrected entry, with the reason and the original value visible.")
    sq("data", "The analysis will be verified by a second person in Statistics, and the report will be reviewed by the functions in the approval record.")
    # Roles and responsibilities: one statement per row of the roles table
    sq("roles", "Process Development is responsible for the study.")
    for func, row in rolerow.items():
        resp_ = _cells(row)[1]
        st(f"{func}: {resp_[0].lower() + resp_[1:]}.", [tref("roles", roles_t, rolerow, func)])
    st("Two functions are engaged before execution: the analysis will be agreed with Statistics before the first "
       "run, and the commercial operation the scale-down model represents will be confirmed with Manufacturing "
       "Science at the receiving site before qualification.",
       [ref("roles", q("Two of these functions are engaged before execution.")),
        ref("roles", q("will be agreed with Statistics before the first run.")),
        ref("roles", q("The commercial operation the scale-down model represents will be confirmed with Manufacturing Science at the receiving site before qualification, since the model is matched to that operation and not to the development one"))])
    # Deliverables and schedule
    sq("schedule", s_deliverable)
    sq("schedule", "It will report the qualification of the scale-down model, the results of each parameter series, the proven acceptable ranges, the classification of each parameter and any deviation from this plan.",
       "PCR-004 will report the qualification of the scale-down model, the results of each parameter series, "
       "the proven acceptable ranges, the classification of each parameter and any deviation from the plan.")
    st(t("The study will run in four phases, in order: the qualification of the scale-down model, the "
         "`{python} N_RCF` series, the depth filter load series on centrate from the extremes of the "
         "centrifugation range, and the turbidity series on material prepared from both."),
       [ref("schedule", q("The study will run in four phases, in order.")),
        ref("schedule", q("The `{python} N_RCF` series will follow, then the depth filter load series on centrate from the extremes of the centrifugation range, then the turbidity series on material prepared from both."))])
    sq("schedule", s_qual_first)
    sq("schedule", "Analysis of a series may begin once the last analytical result of that series has been approved, and the report will be issued when all three series have been analysed.")
    sq("schedule", s_window)
    # Risks and assumptions
    sq("risks", "Five things could weaken the conclusions of this study, and each carries a mitigation or a bound (Version 1.0).")
    sq("risks", "A sixth item states the assumption on which the study rests.",
       "A sixth item of the risks states the assumption on which the study rests.")
    st("The scale-down model is the largest risk to the conclusions: a continuous disk-stack centrifuge is the "
       "hardest unit in the process to represent at bench scale, and the model is expected to under-represent "
       "lysis (a passage corrected under change 7).",
       [ref("risks", q("The scale-down model is the largest of them.")),
        ref("risks", q("A continuous disk-stack centrifuge is the hardest unit in this process to represent at bench scale")),
        ref("risks", q(s_lysis))])
    st("The mitigation is that the study reports effects and ranges rather than absolute impurity levels, and "
       "that the qualification compares the model with the commercial train on the responses that matter.",
       [ref("risks", q(s_mitigation)),
        ref("risks", q("compares the model with the commercial train on the responses that matter here."))])
    sq("risks", "The study assumes the culture is representative.")
    sq("risks", "A culture that ends at lower viability carries more debris and more broken cells into harvest, which raises both the solids load on the centrifuge and the host cell protein released before the run begins.")
    sq("risks", "Culture will therefore be taken from the qualified bioreactor scale-down model at its set-point condition, and the viability and the cell density of every culture used will be recorded with the run and reported in PCR-004.")
    sq("risks", "Material supply constrains what can be compared within a series.")
    sq("risks", "One culture may not provide enough volume for all five levels of a parameter at the scale of the model, so a series may span more than one culture.")
    sq("risks", "Where it does, the set-point replicates run on each culture provide the reference for the levels run on that culture, and the analysis will fit the culture as a block.",
       "Where a series spans more than one culture, the set-point replicates run on each culture provide the "
       "reference for the levels run on that culture, and the analysis will fit the culture as a block.")
    sq("risks", s_blend_claim, "Because the blended material of the turbidity series carries the particle size "
       "distribution of centrate and not that of a saturated depth filter, the turbidity range will be reported "
       "as a range of turbidity delivered to capture, and no claim will be made about the specific material a "
       "filter at the end of its capacity would pass.", also=[("risks", s_blend)])
    sq("risks", "Assay variability bounds the smallest effect the study can see")
    st("The study rests on the assumption that harvest has no impact on product quality, which the impurity "
       "release criterion and the product quality criterion test, for host cell protein and DNA released by cell "
       "breakage and for aggregate added at air-liquid interfaces.",
       [ref("risks", q("The assumption that harvest has no impact on product quality")),
        ref("risks", q("test it, for host cell protein and DNA released by cell breakage and for aggregate added at air-liquid interfaces."))])
    # Approvals
    sq("approvals", "This plan takes effect when it has been approved by every function in the approval record at the front of this document.",
       "PCP-004 takes effect when it has been approved by every function in its approval record.")
    sq("approvals", "Execution of the study did not begin before the approval of Version 1.0.")
    sq("approvals", "Any change to the plan after approval will be made as a revision to this document and approved by the same functions.")
    sq("approvals", "A change made during execution that is not a revision to this plan is a deviation")
    # Appendix A: the planned levels of each series, on the rows that occur once in the document
    order = list(dict.fromkeys(lev_df["Series"]))
    if order != [f"{ns['cap'](ns['nm'](p))} series" for p in prm]:
        raise ValueError(f"{lev_t.label}: the series {order} do not follow the parameters of the plan")
    for label, p in zip(order, prm):
        lv = ns["level_rows"](p)
        lv_txt = join_and([f"{v} ({r_[0].lower() + r_[1:]})" for r_, v in lv])
        mats = list(dict.fromkeys(lev_df.loc[lev_df["Series"] == label, "Material"]))
        rows_ = [ref("appA", row, lev_t, levrow) for i, row in levrow.items() if lev_df["Series"].iloc[i] == label]
        if len(mats) == 1:
            st(f"The {label[0].lower() + label[1:]} is run on {mats[0][0].lower() + mats[0][1:]} at {len(lv)} "
               f"distinct levels: {lv_txt}.", rows_)
        else:
            st(f"The {label[0].lower() + label[1:]} is run once on each of "
               f"{join_and([m[0].lower() + m[1:] for m in mats])}, each time at {len(lv)} levels: {lv_txt}.",
               rows_ + [ref("appA", q(s_run_twice))])
    st(lev_note, [ref("appA", lev_note, lev_t)])
    # Appendix B: one statement per sample point
    for point, row in smprow.items():
        r_ = smp_df[smp_df["Sample point"] == point].iloc[0]
        meths = [m.strip() for m in r_["Methods"].split(",")]
        st(f"Sample point “{point}”: tested for {join_and([meths[0][0].lower() + meths[0][1:]] + meths[1:])}; "
           f"purpose: {r_['Purpose'][0].lower() + r_['Purpose'][1:]}.", [tref("appB", smp_t, smprow, point)])
    st(f"The methods of the sampling schedule are {smp_note[0].lower() + smp_note[1:].rstrip('.')}.",
       [ref("appB", smp_note, smp_t)])

    # ==== acceptance criteria as the plan states them ===================================================
    # No criteria-change table: PCMP-001 Table 7.1 sets no intermediate acceptance criterion for the
    # clarified harvest and Version 1.0 applied no analysis-time criterion here. The criteria in force are
    # the decision criteria of Version 1.0, kept in its words.
    crit_sec = f"{DOC}_crit"

    def cref(quote):
        r = ref("criteria", quote)
        r.section_id = crit_sec
        return r
    q_pass = q(s_crit1_pass)
    rel_basis = t("Version 1.0 decision criterion 1 (impurity release), kept in Version 2.0: {what} in the "
                  "clarified harvest is compared with the unclarified culture that produced it, and a level passes "
                  "when no increase is detected at α = `{python} ALPHA`, or when a detected increase is smaller "
                  "than the resolution of the method that measured it (the plan sets no size for that resolution). "
                  "A comparison within a run, not a numeric limit.")
    acrit = [
        S.AcceptanceCriterionRecord(
            step=UO, attribute=key, low=None, high=None, unit=None,
            basis=rel_basis.replace("{what}", names[key]), revision=P.REV2["rev"], status="in force",
            source=cref(q_pass))
        for key in ("hcp", "residual_dna")]
    acrit.append(S.AcceptanceCriterionRecord(
        step=UO, attribute=turb.key, low=None, high=float(TURB_LIMIT), unit=turb.unit,
        basis="Version 1.0 decision criterion 2 (clarification), kept in Version 2.0: an absolute limit at the "
              "upper limit of the NOR of post-clarification turbidity; a centrifuge setting or a filter load that "
              "delivers clarified harvest above it has failed to clarify.",
        revision=P.REV2["rev"], status="in force", source=cref(q(s_crit2_cmp))))
    acrit.append(S.AcceptanceCriterionRecord(
        step=UO, attribute="aggregates_hmw", low=None, high=None, unit=None,
        basis=t("Version 1.0 decision criterion 3 (product quality), kept in Version 2.0: the high molecular "
                "weight content is compared before and after the step, and a level passes when no increase is "
                "detected at α = `{python} ALPHA`. A comparison within a run, not a numeric limit."),
        revision=P.REV2["rev"], status="in force", source=cref(q(s_crit3_cmp))))

    # ==== concepts ===================================================================================
    concepts = [Concept(concept_id=STEP_ID, concept_type="PROCESS_STEP", canonical_name=UO_NAME,
                        aliases=["harvest and clarification", "harvest", "clarification", "primary recovery",
                                 UO_TITLE, f"Step {uo.step}"],
                        review_status="human_verified")]
    alias = {rcf.key: ["centrifugal field", "relative centrifugal field", "rcf"],
             dfl.key: ["filter load", "load per unit area"],
             turb.key: ["turbidity", "turbidity of the clarified harvest"]}
    concepts += [Concept(concept_id=pcid[p.key], concept_type="PROCESS_PARAMETER", canonical_name=p.name,
                         aliases=alias[p.key], review_status="human_verified") for p in prm]
    concepts += G._attr_concepts(ckeys)
    concepts += G._method_concepts([a for a, _ in ns["HARVEST_AMV_REFS"]], title_of)
    concepts += [Concept(concept_id=e.equipment_id, concept_type="EQUIPMENT", canonical_name=e.equipment_name,
                         review_status="human_verified") for e in equipment]

    # ==== the annex ==================================================================================
    nor_note = ("No set-point or NOR of the step changed at Version 2.0, so ProcessParameter.target_value and "
                "NOR are the values of the parameter table, which are also the values in force."
                if not moved else
                f"ProcessParameter.target_value and NOR are the values of the parameter table, against which the "
                f"study was planned; the values in force differ for {', '.join(moved)}.")
    disc_txt = "; ".join(f"{', '.join(d['studies'])} ({d['id']})" for d in disc)
    annex = S.GroundTruthAnnex(
        document_id=DOC, document_title=f"{P.DOC_REGISTRY[DOC][0]} — {P.DOC_REGISTRY[DOC][1]}",
        document_class=P.DOC_REGISTRY[DOC][0], **G.rev2_layer(DOC, FILE),
        schema_extensions_used=G.COMMON_EXT + G.REV2_EXT,
        out_of_schema_notes=[
            "Classification is a result of the study, so every parameter_type is 'unclassified'. " + nor_note
            + " ProcessParameter.PAR carries the range studied, as everywhere in the corpus; the plan claims no "
            "proven acceptable range and no design space (it says so: ExplicitNonClaim records), so there are no "
            "ProvenAcceptableRange or DesignSpace records. Each parameter is anchored on its row of the parameter "
            "table and on its sentence of the factors section; post-clarification turbidity is a parameter as the "
            "plan lists it, measured, not set, in the other two series (the note of the table, also an "
            "ExplicitNonClaim).",
            "The step forms no quality attribute. The QualityAttribute records are the four attributes of the "
            "attribute table; their acceptance_criteria are the drug substance criteria printed there, which the "
            "plan states are not in-process limits for the clarified harvest (an ExplicitNonClaim). Fragments are "
            "assigned to the step by the CQA register but are not a response of the study.",
            "acceptance_criteria: the plan prints no criteria-change table, because PCMP-001 Table 7.1 sets no "
            "intermediate acceptance criterion for the clarified harvest and Version 1.0 applied no "
            "analysis-time criterion at the step. The records are the decision criteria of Version 1.0, kept in "
            "Version 2.0 and in force: criterion 1 (impurity release) for host cell protein and residual DNA and "
            "criterion 3 (product quality) for the high molecular weight content are comparisons within a run, "
            "so low, high and unit are empty and the basis states the rule; criterion 2 (clarification) is the "
            "absolute limit on post-clarification turbidity (attribute 'turbidity', the parameter key). Step yield "
            "is reported and not gated (an ExplicitNonClaim).",
            f"studies holds the univariate study {ns['UNI_ID']}, anchored on the sentence of the schedule that "
            f"gives its execution window, on its design sentences, on the rows of the planned levels (Appendix A) "
            f"that occur once in the document (the continuation rows of the depth filter load series read alike "
            f"in the blocks of its two centrates) and on the rows of the sampling schedule (Appendix B). Neither "
            f"StudyDesign carries n_runs or n_center_points: Version 1.0 set no number of set-point replicates, "
            f"and the qualification compares scale-down runs with manufacturing-scale batches. The qualification "
            f"of the scale-down model has no study id in the plan or in the study chronology, so its StudyDesign "
            f"keeps the Version 1.0 concept id {QUAL_ID} and has no execution window; its responses are the "
            f"outputs as the plan names them. "
            + (f"Studies of the step made after Version 1.0 are not studies of this plan, and the plan does not "
               f"mention them; PCR-004 records them as discrepancies from it: {disc_txt}." if disc else ""),
            "Each AnalyticalMethod record is anchored on its sentence of the analytical methods section (nrCE-SDS "
            "on the change that adds it), on its row of the procedures table and, for the three methods with "
            "validation data, on its row of the performance table. Turbidity by nephelometry (AMV-3015) measures "
            "post-clarification turbidity, a parameter, so that record has no associated attribute and no "
            "attribute_measured_by_method assertion.",
            "Equipment: the three units of the commercial train are at the receiving site, anchored on their "
            "sentences and on the roles-table row of the receiving site, which confirms the commercial operation; "
            "the scale-down model and its three parts (bench shear device, laboratory centrifuge, disks of the "
            "commercial filter media) are at the sending site, as the other plans place a scale-down model. The "
            "scale-down Protein A column of the load challenge is an Equipment record with no step_uses_equipment "
            "assertion: it is not equipment of the harvest step, and the plan does not identify it with the "
            "column of the Protein A plan.",
            "parameter_impacts_attribute assertions are the plan's stated expectations from the mechanism of the "
            "step, not results. attribute_has_acceptance_criterion assertions carry criterion 1 for host cell "
            "protein and residual DNA and criterion 3 for aggregate.",
            "Each correction of change 7 is a statement anchored on the Version 1.0 sentence, the correction and "
            "the corrected sentence where it stands (marked \"(corrected, change 7)\" in the document). Each row "
            "of the roles, performance, attribute, parameter and sampling tables is a statement. The approvals "
            "table and the abbreviations are not represented. No rhetorical_spans: a plan has none. weak_claims "
            "is empty.",
        ] + G._unrendered_note(unrendered),
        inventory=G.rev2_inventory(DOC, FILE, "process_characterization_plan", UO_NAME,
                                   ["process characterization", "harvest and clarification",
                                    "disk-stack centrifugation", "depth filtration", "univariate study",
                                    "protocol amendment", "scale-down offset", "impurity release",
                                    "clarification criterion"]),
        entities=entities, studies=studies,
        report_sections=[ReportSection(section_id=f"{DOC}-summary", title="Plan summary", statements=ST)],
        assertions=AssertionStore(run_id=f"gt-{DOC}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{DOC}", concepts=concepts),
        weak_claims=[], rhetorical_spans=[], acceptance_criteria=acrit)
    _gate(annex, text)
    return annex
