"""PCP-008 Version 2.0: Process Characterization Plan, Anion Exchange Chromatography (Step 8).

The protocol amendment issued under INV-001 (and INV-002) for the flow-through polishing step, fitted
to the Version 2.0 text. The kinds of record follow the plan model builders in ``build_ground_truth``
(``build_plan_viral_inactivation``, ``build_plan_protein_a``, ``build_plan_bioreactor``); the concept
ids are those of the Version 1.0 builder of this document (``step:aex``, ``param:aex_*``,
``equip:aex_sdm_column``, ``equip:aex_column``).

Every complex table of the plan (``T.frame`` or a ``T.`` builder) is read back through
``qmd_ctables`` from the object the plan printed, so each row quote is the rendered row, with
``table_header=rows.header``. The related-documents, title-block and roles tables are markdown, read
with ``md_string_rows`` from the call that printed them. Every prose quote is a span of the ``.qmd``
copied with its inline expressions and evaluated in the plan's own namespace (``qmd_inline``), and
``q`` refuses a span that is not in the ``.qmd`` prose, so no value is typed here. ``build()`` refuses
to return an annex with a quote that does not ground or with a weak anchor.

The plan carries the registered discrepancy D-001 (``authoring/DISCREPANCIES.md``) and keeps the
Version 1.0 coding statement. The annex records both statements as the plan states them and nothing
that sets them against each other.
"""
from __future__ import annotations

import contextlib
import io
import os
import re

import _pcpkg as P
import build_ground_truth as G
import schema_ext as S
from build_ground_truth import (
    AXPARAM_CONCEPT, AXUO, AXUO_NAME, CELL_SEP, COMMON_EXT, METHOD_ATTRS, METHOD_TYPE, REV2_EXT,
    STUDY_TYPE, _attr_concepts, _attr_key_by_label, _method_concepts, _site_entities,
    _unrendered_note, acceptance_criteria_layer, ctable_rows, md_string_rows, meta, qmd_ctables,
    qmd_inline, qmd_namespace, rev2_inventory, rev2_layer,
)
from check_grounding import normalize, specificity_report

DOC = "PCP-008"
QMD = "PCP-008_aex.qmd"
FILE = G.PCP8_FILE                                   # "PCP-008_aex.docx"

#: Concept ids kept from the Version 1.0 builder of this document.
STEP_ID = "step:aex"
SDM_ID = "equip:aex_sdm_column"
COLUMN_ID = "equip:aex_column"

#: Relationship cell of @tbl-related -> DocumentRelationship.kind (as the other step plans map it;
#: "Sibling — paired document" and "Reason for this revision" fall back to "references").
REL_KIND = {"Rolls up into": "rolls_up_into", "Parent — master plan": "executed_under",
            "Parent — risk basis for study scope": "scoped_by",
            "Parent — transfer scope": "scoped_by"}

#: Section key -> heading path as the document renders it. ``build`` checks every title against the
#: headings of the .qmd, so a renamed section fails loudly instead of mislabelling its references.
SEC = {
    "title": ("Title block",),
    "purpose": ("Purpose and scope",),
    "changes": ("Purpose and scope", "Changes in this revision"),
    "objectives": ("Objectives",),
    "related": ("Related documents",),
    "uo": ("Prior knowledge and quality risk basis", "Unit-operation description and prior knowledge"),
    "cqas": ("Prior knowledge and quality risk basis", "Quality attributes in scope"),
    "risk": ("Prior knowledge and quality risk basis", "Risk-based prioritization of parameters"),
    "sdm": ("Materials and methods", "Scale-down model and its qualification"),
    "operation": ("Materials and methods", "Operation"),
    "analytical": ("Materials and methods", "Analytical methods"),
    "sampling": ("Materials and methods", "Sampling plan"),
    "stats": ("Materials and methods", "Statistical methods"),
    "factors": ("Study design", "Factors, ranges and study type"),
    "screening": ("Study design", "Screening design"),
    "rsm": ("Study design", "Response-surface design"),
    "univariate": ("Study design", "Univariate assessment"),
    "criteria": ("Acceptance and decision criteria",),
    "par": ("Proven acceptable ranges (planned analysis)",),
    "data": ("Data management and integrity",),
    "roles": ("Roles and responsibilities",),
    "schedule": ("Deliverables and schedule",),
    "risks": ("Risks and assumptions",),
    "approvals": ("Approvals",),
    "appA": ("Appendix A — Planned screening design matrix",),
    "appB": ("Appendix B — Planned response-surface design matrix",),
}


# --------------------------------------------------------------------------- #
# Local helpers. _smart, _walk and _gate are copied from annex_builders/       #
# inv_002.py; printed_table and md_caption are new here (candidates for        #
# build_ground_truth, named in the report).                                   #
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
    """The cells of a rendered row, as ``check_grounding.docx_text`` separates them (a continuation
    row of a merged column keeps its empty first cell)."""
    return [c.strip() for c in row.split("|")]


def _smart(s):
    """Prose as pandoc renders it: a straight apostrophe becomes a typographic one. Table cells and
    table notes are raw markup and keep the straight form, so only prose quotes go through this."""
    return s.replace("'", "’")


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


def printed_table(ns, src, label):
    """``(rows, caption)`` of a markdown table that a chunk prints itself and labels in the caption
    line it prints after the table (``print(md_table(...))`` then ``print(": ... {#tbl-x}")``).

    ``qmd_printed`` finds a chunk by its ``#| label:`` line, which such a chunk does not have, and
    ``qmd_namespace`` records only ``show``/``md`` calls. Re-running the chunk in the document's own
    namespace reproduces the table from the expression that rendered it; the caption line is cut off
    before ``md_string_rows`` reads the table as the DOCX reads it."""
    chunks = [c for c in re.findall(r"```\{python\}\n(.*?)```", src, flags=re.S)
              if "{#" + label + "}" in c]
    if len(chunks) != 1:
        raise ValueError(f"{DOC}: {len(chunks)} chunks print {label}")
    buf = io.StringIO()
    cwd = os.getcwd()
    os.chdir(G.HERE)
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(chunks[0], f"{QMD}#{label}", "exec"), ns)   # noqa: S102
    finally:
        os.chdir(cwd)
    lines = buf.getvalue().splitlines()
    cut = next(i for i, ln in enumerate(lines) if ln.startswith(": ") and "{#" + label + "}" in ln)
    caption = re.match(r": (.*?) \{#", lines[cut]).group(1)
    return md_string_rows("\n".join(lines[:cut])), caption


# --------------------------------------------------------------------------- #
# The annex.                                                                   #
# --------------------------------------------------------------------------- #
def build():
    """The ``GroundTruthAnnex`` of PCP-008 Version 2.0."""
    import doe_report as D
    import tables as T
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    from annex_contract.concepts import Concept, ConceptStore
    from annex_contract.discourse import DocumentRelationship, ExplicitNonClaim
    from annex_contract.results import Deviation, ModularContribution
    from annex_contract.summaries import ReportSection, ReportStatement

    src = _source()
    _check_sections(src)
    prose_src = re.sub(r"```\{python\}.*?```", "", src, flags=re.S)
    ns, _ = qmd_namespace(QMD)
    ct = qmd_ctables(QMD)
    text = G._document_text(FILE)
    doc, f = DOC, FILE

    def ev(s):
        """A string in .qmd form, its inline expressions evaluated in the plan's namespace."""
        return _smart(qmd_inline(ns, s))

    def q(s):
        """A span of the .qmd prose as it renders. The span must be copied from the .qmd with its
        inline expressions, so a typed value fails here rather than grounding by coincidence."""
        if s not in prose_src:
            raise ValueError(f"{DOC}: not a span of the .qmd prose: {s[:90]!r}")
        return ev(s)

    def ref(sec, quote, caption=None, label=None, header=None):
        r = G.ref(doc, f, _sid(sec), SEC[sec][-1], quote, table_title=caption,
                  table_id=None if label is None else f"{doc}_tab_{label[4:].replace('-', '_')}",
                  table_header=header)
        r.heading_path = list(SEC[sec])
        return r

    def tref(sec, t, rows, key):
        """The rendered row ``key`` of the CTable ``t`` (``rows = ctable_rows(t, ...)``)."""
        return ref(sec, rows[key], t.caption, t.label, rows.header)

    def keyed(label, keys, name_of):
        """The rendered rows of the CTable printed under ``label``, keyed. Every row must name its own
        record: a mis-keyed row grounds and attests the wrong thing."""
        t = ct[label][0]
        rows = ctable_rows(t, keys)
        bad = [k for k, row in rows.items() if name_of(k) not in row]
        if bad:
            raise ValueError(f"{DOC} {label}: rows keyed to records they do not name: {bad}")
        return t, rows

    def head_of(rows, key):
        """For a continuation row of a merged first column, the row that opens its group (it carries
        the label the continuation row leaves empty)."""
        order = list(rows)
        for k2 in reversed(order[:order.index(key) + 1]):
            if _cells(rows[k2])[0]:
                return k2
        raise ValueError(f"{DOC}: no group head for {key}")

    A, ST = [], []

    def add(subj, pred, obj, txt, refs):
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{doc}-A{len(A) + 1:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=txt, source_references=refs, metadata=meta()))

    def st(txt, refs):
        ST.append(ReportStatement(
            statement_id=f"{doc}-S{len(ST) + 1:03d}", statement_text=txt, confidence="high",
            review_status="accepted", source_references=refs))

    def sq(sec, quote_src, txt=None, also=()):
        """A statement of one sentence of section ``sec``: ``quote_src`` is its .qmd source, ``txt``
        the statement in .qmd form (the sentence itself when omitted, with a full stop where the quote
        ends before a citation or a cross-reference). ``also`` cites further (section, source) spans
        the statement draws on, so every clause of it has its span."""
        txt_ = ev(txt) if txt else q(quote_src)
        st(txt_ if txt_.endswith(".") else txt_ + ".",
           [ref(sec, q(quote_src))] + [ref(s_, q(x)) for s_, x in also])

    # ---- names and data the plan uses ----------------------------------------------------------
    uo, prm, N = ns["uo"], ns["P"], ns["N"]
    UO_TITLE = ns["UO_TITLE"]
    if ns["UO"] != AXUO or UO_TITLE != G.AXSTEP_LABEL:
        raise ValueError(f"{DOC}: the plan is not the {AXUO} plan it is annexed as")
    INV, AMD, REV1 = ns["INV"], ns["AMD"], ns["REV1"]
    R, CRIT, ACC = ns["R"], ns["CRIT"], ns["ACC"]           # short key -> response / criterion text
    short_of = {D.RESP_TO_CQA[r]: k for k, r in R.items()}   # attribute key -> short key
    pi = ns["pi"]
    ids = ns["ids"]                                         # study kind -> study id
    CHR = ns["CHR"]
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))
    reg = P.cqa_reg.set_index("key")
    pkey = {p.name: k for k, p in prm.items()}              # parameter name -> key
    pcid = {k: AXPARAM_CONCEPT[p.name] for k, p in prm.items()}
    sdm_name = "scale-down model of the commercial anion exchange column"
    column_name = "commercial anion exchange column"

    # ---- the rendered tables, from the objects and calls that printed them -------------------
    pt, pdf_ = ct["tbl-params"]                                     # T.frame, by parameter name
    prow = ctable_rows(pt, pdf_["Parameter"])
    cd_t, cdrow = keyed("tbl-codes", list(ct["tbl-codes"][1]["Factor"]), str)   # T.frame, by factor
    cq_t, cq_df = ct["tbl-cqas"]                                    # T.frame, by attribute key
    by_label = _attr_key_by_label()
    ckeys = [by_label[n] for n in cq_df["CQA"]]
    crow = ctable_rows(cq_t, ckeys)
    if ckeys != list(ns["ROLE"]):
        raise ValueError(f"{DOC}: the attribute table does not follow the plan's role map")
    sop_t, sop_df = ct["tbl-sops"]                                  # T.sop_references, by reference
    soprow = ctable_rows(sop_t, sop_df["Reference"])
    eq_t, eq_df = ct["tbl-equipment"]                               # T.frame, by equipment id
    eqrow = ctable_rows(eq_t, eq_df["Equipment"])
    iac_t = ct["tbl-iac"][0]                                        # T.iac_derivation([UO])
    iac = ns["iac_here"].set_index("cqa")                           # D.iac_table(UO)
    iacrow = ctable_rows(iac_t, [by_label[_cells(r)[0]] for r in iac_t.rows()])
    win_t, win_df = ct["tbl-windows"]                               # T.frame, by study id
    winrow = ctable_rows(win_t, win_df["Study"])
    mtx = {"screening": ct["tbl-matrix-screening"][0], "rsm": ct["tbl-matrix-rsm"][0]}
    rel = md_string_rows(P.related_docs_md(doc))                    # @tbl-related
    rel_cap = md_caption(src, "tbl-related")
    tb = md_string_rows(P.title_block(doc, UO_TITLE))               # the title block, by field
    roles, roles_cap = printed_table(ns, src, "tbl-roles")          # md_table, by function

    # the parameter table prints the values the plan was written against; check them against the
    # namespace, and that no set-point or NOR moved at Version 2.0 (the records carry these values)
    for name, row in prow.items():
        p = prm[pkey[name]]
        c = _cells(row)                    # Study type | Parameter | Unit | Set-point | Range | NOR
        want = [name, p.unit, f"{p.setpoint_characterized:g}",
                f"{p.prange[0]:g}–{p.prange[1]:g}",
                f"{p.nor_characterized[0]:g}–{p.nor_characterized[1]:g}"]
        if c[1:] != want:
            raise ValueError(f"{pt.label}: row {c} does not read {want}")
    moved = [p.name for p in prm.values()
             if float(p.setpoint) != float(p.setpoint_characterized)
             or [float(x) for x in p.nor] != [float(x) for x in p.nor_characterized]]

    # ---- the step, the sites and the equipment ------------------------------------------------
    purpose, prior = SEC["purpose"][-1], SEC["uo"][-1]
    q_purpose = q("This plan sets out the Stage 1 process characterization of the anion exchange "
                  "chromatography step of the A-Mab drug substance process")
    q_step = q("The step is Step `{python} uo.step` of the train and the last chromatography step "
               "before virus filtration.")
    q_ft = q("It is operated in flow-through mode.")
    q_charge = q("At the load pH the antibody carries a net positive charge, because its isoelectric "
                 "point lies well above the pH of the load, and it passes through the bed.")
    q_these = q("These are residual DNA, the acidic part of the host cell protein population, leached "
                "Protein A and virus particles.")
    q_pool = q("The flow-through and the chase are collected as a single pool from the start of the "
               "load to the end of the chase.")
    q_hold = q("The pool is filtered and held for the virus filtration step, and the hold conditions "
               "are those of the commercial process.")
    q_load = q("The material loaded onto the step is the cation exchange pool, whose attributes are set "
               "by the preceding step, characterized under the cation exchange plan PCP-007.")
    step = S.ProcessStep(
        step_id=STEP_ID, step_name=AXUO_NAME, step_number=str(uo.step), unit_operation=AXUO_NAME,
        description=f"Step {uo.step} of the A-Mab drug substance train and its last chromatography "
                    f"step before virus filtration, operated in flow-through mode. The resin carries a "
                    f"quaternary amine ligand with a fixed positive charge. At the load pH the antibody "
                    f"carries a net positive charge and passes through the bed, while species with a net "
                    f"negative charge bind: residual DNA, the acidic part of the host cell protein "
                    f"population, leached Protein A and virus particles. The step carries a modular "
                    f"viral clearance claim for XMuLV and MVM. The flow-through and the chase are "
                    f"collected as one pool, which is filtered and held for the virus filtration step.",
        input_materials=["cation exchange pool, adjusted to the target pH and conductivity"],
        output_materials=["flow-through pool (flow-through and chase), filtered and held for the virus "
                          "filtration step"],
        equipment=[column_name, sdm_name, eq_df["Description"].iloc[0]],
        source_references=[ref("purpose", q_purpose), ref("purpose", q_step), ref("purpose", q_ft),
                           ref("uo", q_charge), ref("uo", q_these), ref("operation", q_pool),
                           ref("operation", q_hold), ref("risk", q_load)],
        metadata=meta())
    q_sdm = q("The study will be executed on a scale-down model of the commercial anion exchange column, "
              "qualified under SOP-1001.")
    q_same = q("The resin, the buffers and the packing method are the same as at commercial scale.")
    q_col = q("It is executed on a scale-down model of the commercial column")
    q_chamber = q("The chromatography system will be operated in a temperature-controlled chamber under "
                  "calibration and change control.")
    q_cal = q("its calibration status will be verified before the first run and confirmed at the end of "
              "the execution period")
    recv = next(k for k in roles if "receiving site" in k)
    equipment = [
        S.Equipment(
            equipment_id=SDM_ID, equipment_name=sdm_name,
            equipment_type="chromatography column (scale-down model)", site_name=P.SENDING_SITE,
            source_references=[ref("sdm", q_sdm), ref("sdm", q_same)], metadata=meta()),
        S.Equipment(
            equipment_id=f"equip:{CHR}", equipment_name=f"{eq_df['Description'].iloc[0]} {CHR}",
            equipment_type="instrumented chromatography system (scale-down)",
            site_name=P.SENDING_SITE,
            source_references=[tref("operation", eq_t, eqrow, CHR), ref("operation", q_chamber),
                               ref("operation", q_cal)],
            metadata=meta()),
        S.Equipment(
            equipment_id=COLUMN_ID, equipment_name=column_name,
            equipment_type="chromatography column (manufacturing scale)", site_name=P.RECEIVING_SITE,
            source_references=[ref("purpose", q_col),
                               ref("roles", roles[recv], roles_cap, "tbl-roles", roles.header)],
            metadata=meta()),
    ]

    # ---- parameters -----------------------------------------------------------------------------
    factors = SEC["factors"][-1]
    params = []
    for name, row in prow.items():
        p = prm[pkey[name]]
        refs = [tref("factors", pt, prow, name)]
        if name in cdrow:                     # the multivariate factors also have their code row
            refs.append(tref("factors", cd_t, cdrow, name))
        params.append(S.ProcessParameter(
            parameter_id=AXPARAM_CONCEPT[name], parameter_name=name, parameter_type="unclassified",
            unit=p.unit, target_value=f"{p.setpoint_characterized:g} {p.unit}",
            NOR=f"{p.nor_characterized[0]:g}–{p.nor_characterized[1]:g} {p.unit}",
            PAR=f"{p.prange[0]:g}–{p.prange[1]:g} {p.unit}",
            associated_step=UO_TITLE, study_type=p.study, source_references=refs, metadata=meta()))

    # ---- analytical methods: each on its sentence and its row of the procedures table ------------
    analytical = SEC["analytical"][-1]
    title_of = dict(ns["AMVS"])
    q_method = {
        "AMV-3012": q("Pool host cell protein will be measured by ELISA (AMV-3012) and reported in "
                      "nanograms per milligram of antibody."),
        "AMV-3013": q("The charge variant profile of the load will be measured by icIEF (AMV-3013) and "
                      "compared with the release profile of the cation exchange pool"),
        "AMV-3014": q("Residual DNA will be measured by qPCR (AMV-3014)"),
        "AMV-3016": q("leached Protein A by ELISA (AMV-3016)"),
        "AMV-3017": q("Infectivity of xenotropic murine leukaemia virus will be measured by TCID50 "
                      "(AMV-3017)"),
        "AMV-3018": q("infectivity of minute virus of mice by TCID50 with a qPCR confirmation (AMV-3018)"),
        "AMV-3020": q("Fragments will be measured by nrCE-SDS (AMV-3020, under the nrCE-SDS procedure "
                      "SOP-3015)."),
    }
    if set(q_method) != set(title_of):
        raise ValueError(f"{DOC}: method sentences {sorted(q_method)} != AMVs {sorted(title_of)}")
    for amv, quote in q_method.items():
        if amv not in quote:
            raise ValueError(f"{DOC}: the sentence of {amv} does not name it")
    analyte = {"AMV-3012": "pool host cell protein", "AMV-3013": "charge variant profile of the load",
               "AMV-3014": "residual DNA", "AMV-3016": "leached Protein A",
               "AMV-3017": "infectivity of xenotropic murine leukaemia virus",
               "AMV-3018": "infectivity of minute virus of mice", "AMV-3020": "fragments"}
    attrs_of = {amv: [k for k in METHOD_ATTRS.get(amv, []) if k in ckeys] for amv in title_of}
    method_of = {k: amv for amv, ks in attrs_of.items() for k in ks}
    procedure_of = {"AMV-3020": "SOP-3015"}               # named in the method's own sentence
    methods = []
    for amv in sorted(title_of):
        refs = [ref("analytical", q_method[amv]),
                tref("related", sop_t, soprow, amv)]
        if amv in procedure_of:
            refs.append(tref("related", sop_t, soprow, procedure_of[amv]))
        methods.append(S.AnalyticalMethod(
            method_id=amv, method_name=title_of[amv], method_type=METHOD_TYPE.get(amv),
            analytes=[analyte[amv]], associated_attributes=[f"attr:{k}" for k in attrs_of[amv]],
            validation_status="validated", source_references=refs, metadata=meta()))

    # ---- quality attributes ---------------------------------------------------------------------
    cqa_sec = SEC["cqas"][-1]
    acc_ds = dict(zip(ckeys, P.cqas_by_keys(ckeys)["Acceptance"]))   # the cell without its note marker
    attrs = []
    for i, key in enumerate(ckeys):
        score = int(cq_df["Tool #1"].iloc[i])
        why = (f"Very high by rule for viral clearance, whatever the Tool #1 score ({score})."
               if key.startswith("lrv") else
               f"A-Mab Tool #1 score = impact on safety and efficacy × uncertainty of that impact = {score}.")
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=reg.loc[key, "cqa"], attribute_type="CQA",
            unit=reg.loc[key, "unit"], acceptance_criteria=[f"{acc_ds[key]} (drug substance)"],
            analytical_method=method_of.get(key), associated_steps=[UO_TITLE],
            rationale_for_criticality=why, criticality_level=cq_df["Criticality"].iloc[i],
            tool1_score=score, tool2_severity=int(reg.loc[key, "tool2_severity"]),
            source_references=[tref("cqas", cq_t, crow, key)], metadata=meta()))

    # ---- modular viral clearance contributions --------------------------------------------------
    iac_all = ns["iac_all"]
    q_claims = q("""It claims `{python} f"{x_claim:g}"` log10 for XMuLV, of a cumulative requirement of `{python} f"{x_req:g}"` log10, and `{python} f"{m_claim:g}"` log10 for MVM, of a cumulative requirement of `{python} f"{m_req:g}"` log10""")
    q_sum = q("""The XMuLV claims of `{python} x_steps` sum to `{python} f"{x_sum:g}"` log10 against a cumulative requirement of `{python} f"{x_req:g}"` log10, and the MVM claims of `{python} m_steps` sum to `{python} f"{m_sum:g}"` log10 against `{python} f"{m_req:g}"` log10.""")
    contributions = []
    for key, claim, total, req in (("lrv_xmulv", ns["x_claim"], ns["x_sum"], ns["x_req"]),
                                   ("lrv_mvm", ns["m_claim"], ns["m_sum"], ns["m_req"])):
        others = [T.step_mid(k) for k in
                  iac_all[iac_all["cqa"] == key].sort_values("step")["step_key"] if k != AXUO]
        contributions.append(ModularContribution(
            contribution_id=f"{doc}-MC{len(contributions) + 1:02d}", quantity=names[key],
            unit_operation=AXUO_NAME, step_value=f"{claim:g}", cumulative_value=f"{total:g}",
            requirement=f"{req:g}", unit="log10", contributing_steps=others,
            source_references=[ref("cqas", q_claims), ref("par", q_sum),
                               tref("par", iac_t, iacrow, key)],
            metadata=meta()))

    # ---- explicit non-claims --------------------------------------------------------------------
    nc, nc_at = [], {}

    def nclaim(sec, subject, statement, quotes, rationale=None, elsewhere=None):
        """``quotes``: one .qmd span of ``sec``, or a list of (section, span) pairs."""
        pairs = [(sec, quotes)] if isinstance(quotes, str) else quotes
        nc.append(ExplicitNonClaim(
            non_claim_id=f"{doc}-NC{len(nc) + 1:02d}", subject=subject, unit_operation=AXUO_NAME,
            statement=statement, rationale=rationale, handled_elsewhere=elsewhere,
            source_references=[ref(s_, q(x)) for s_, x in pairs], metadata=meta()))
        nc_at.setdefault(sec, []).append(nc[-1])

    three = "Three activities lie outside this plan."
    nclaim("purpose", "resin packing, sanitization and life cycle",
           "Resin packing, sanitization and the life cycle of the resin are outside the plan; none of "
           "them is varied in the study.",
           [("purpose", three),
            ("purpose", "Resin packing, sanitization and life cycle are qualified under the resin "
                        "procedure SOP-2008, and none of them is varied here.")],
           elsewhere="SOP-2008")
    nclaim("purpose", "performance at commercial scale",
           "Performance at commercial scale is outside the plan; it is confirmed in Stage 2, whose "
           "batches run inside the NORs and do not test the edges of the ranges.",
           [("purpose", three),
            ("purpose", "Performance at commercial scale is confirmed in Stage 2, during process "
                        "performance qualification (PPQ), whose batches run inside the NORs and do not "
                        "test the edges of the ranges.")],
           elsewhere="Stage 2, process performance qualification (PPQ)")
    nclaim("purpose", "viral clearance of the small-virus retentive filter",
           "The study claims no clearance that belongs to the small-virus retentive filter.",
           [("purpose", three),
            ("purpose", "The small-virus retentive filter is characterized under its own plan, PCP-009, "
                        "and this study claims no clearance that belongs to that filter.")],
           elsewhere="PCP-009")
    nclaim("changes", "corrective actions of INV-002",
           "The corrective actions of INV-002, the model selection and the refits of the response "
           "surface models below the model adequacy criteria, are not applied in the plan.",
           "Its corrective actions, the model selection and the refits of the response surface models "
           "below those criteria, are applied in the paired report PCR-008.",
           elsewhere="PCR-008")
    nclaim("uo", "clearance of leached Protein A held in complex by the antibody",
           "No clearance is claimed for the fragments of the Protein A ligand held in complex by the "
           "antibody Fc.",
           "Fragments held in complex by the antibody Fc are removed only where the complex dissociates, "
           "and no clearance is claimed for that fraction.",
           rationale="They are removed only where the complex dissociates.")
    nclaim("uo", "aggregate",
           "Aggregate is not a response of the designs; PCMP-001 Version 2.0 sets no aggregate criterion "
           "in the pool of this step.",
           [("uo", "PCMP-001 Version 2.0 sets a criterion for antibody fragments (LMW) in the pool of "
                   "this step and no aggregate criterion (Table 7.1 of PCMP-001)."),
            ("uo", "and aggregate is not a response of the designs.")])
    nclaim("cqas", "acceptance criterion for step yield",
           "No acceptance criterion is applied to step yield at this step; it is measured on every run "
           "and reported as a performance attribute.",
           [("cqas", "It is measured on every run and reported, and no acceptance criterion is applied "
                     "to it at this step."),
            ("criteria", "Step yield carries no acceptance criterion at this step and will be reported "
                         "as a performance attribute.")],
           rationale="Step yield is a process performance attribute rather than a quality attribute.")
    nclaim("risk", "quality of the load",
           "The study does not vary the quality of its load, the cation exchange pool.",
           "This study varies the parameters of the anion exchange step and does not vary the quality of "
           "its load.",
           elsewhere="the cation exchange step, characterized under PCP-007")
    nclaim("risk", "parameters held to a platform specification",
           "Parameters held to a platform specification with no credible path to a quality attribute are "
           "not studied; an excursion in any of them is recorded as a deviation.",
           [("risk", "Parameters held to a platform specification with no credible path to a quality "
                     "attribute were not studied, and their ranges are carried from platform knowledge "
                     "and from the modular claims established on prior products."),
            ("risks", "It assumes that parameters not carried into the study are held to platform "
                      "specification, and an excursion in any of them will be recorded as a deviation "
                      "and assessed for impact in PCR-008.")],
           rationale="Their ranges are carried from platform knowledge and from the modular claims "
                     "established on prior products.")
    nclaim("sdm", "scale-down offsets of fragments and viral clearance",
           "Fragments and viral clearance are not compared at the two scales; their offsets are unknown, "
           "not zero, and they are judged as the scale-down model gives them.",
           [("sdm", "The qualification does not compare fragments or viral clearance at the two scales."),
            ("sdm", "Their offset is unknown, not zero, and they are judged as the scale-down model gives "
                    "them (PCMP-001 §7.1).")])
    nclaim("operation", "resin, buffers and column packing",
           "Resin, buffers and column packing are controlled to platform specification and are not "
           "characterized in the study.",
           [("operation", "Resin, buffers and column packing are controlled to platform specification."),
            ("operation", "These inputs are identity and quality controlled, and they are not "
                          "characterized in this study.")])
    nclaim("analytical", "SEC fragment results",
           "Fragments are not judged on SEC results; they are judged on nrCE-SDS results only.",
           [("analytical", "Fragments are judged on nrCE-SDS results only."),
            ("analytical", "SEC reads fragments high in samples that still carry host cell protein, "
                           "because part of the host cell protein elutes in its low molecular weight "
                           "window (INV-001 finding 6).")],
           rationale="SEC reads fragments high in samples that still carry host cell protein, because "
                     "part of the host cell protein elutes in its low molecular weight window.")
    nclaim("analytical", "separation of method variability from process variability",
           "The designs do not separate method variability from process variability; it enters the "
           "residual variance of the fitted models.",
           "Method variability enters the residual variance of the fitted models and is not separated "
           "from process variability by this design.")
    nclaim("sampling", "models of residual DNA and leached Protein A",
           "Residual DNA and leached Protein A are measured on the pool of every response surface run and "
           "monitored, but they are not fitted as responses of the design and set no range.",
           [("sampling", "Residual DNA and leached Protein A will be measured on the pool of every run in "
                         "the response surface design."),
            ("sampling", "and they are not fitted as responses of the design."),
            ("sampling", "Where either attribute moves with a parameter, the observation will be reported "
                         "and carried into the risk assessment rather than used to set a range.")])
    nclaim("stats", "operating region from the screening model",
           "No operating region is derived from the screening model, which identifies which parameters "
           "act on which response.",
           "The screening model identifies which parameters act on which response, and it is not the "
           "model from which an operating region is derived.")
    nclaim("stats", "commercial variability in the capability estimate",
           "The capability estimate carries no source of commercial variability that the scale-down model "
           "does not reproduce; confirmation at commercial scale is a Stage 2 activity.",
           "The estimate carries no source of commercial variability that the scale-down model does not "
           "reproduce, and confirmation at commercial scale is a Stage 2 activity",
           elsewhere="Stage 2")
    nclaim("univariate", "interaction between flow rate and another parameter",
           "The univariate assessment cannot resolve an interaction between flow rate and another "
           "parameter; its claim assumes that the effect of flow rate does not depend on where the other "
           "parameters sit.",
           "A univariate assessment cannot resolve an interaction between flow rate and another parameter, "
           "and the claim it supports is bounded by the assumption that the effect of flow rate does not "
           "depend on where the other parameters sit.")
    nclaim("univariate", "operating flow rate in the response surface model",
           "The univariate result for operating flow rate does not enter the response surface model.",
           "The result will support the range for flow rate as a proven acceptable range, and it will not "
           "enter the response surface model.")
    nclaim("criteria", "numerical thresholds for rules without one",
           "Several rules set no numerical threshold, in Version 1.0 or in PCMP-001 Version 2.0, and the "
           "revision adds none.",
           [("criteria", "Several rules set no numerical threshold, in Version 1.0 or in PCMP-001 Version "
                         "2.0, namely the load profile, the match of the spiked load, the comparison of a "
                         "second load lot, an effect of flow rate, an effect attributed to the infectivity "
                         "assay, how far inside its acceptable range a parameter must be held to be well "
                         "controlled and when its risk of leaving that range is high."),
            ("criteria", "This revision adds none, and PCR-008 states the approach it applies to each.")],
           elsewhere="PCR-008")
    nclaim("criteria", "use of data from an invalidated execution",
           "Data from an invalidated execution are not used to set a range, a classification or a "
           "clearance claim.",
           "Data from an invalidated execution will be retained and may be used to investigate and confirm "
           "the cause, and they will not be used to set a range, a classification or a clearance claim.")
    nclaim("criteria", "point prediction or confidence bound in the verification",
           "Neither the point prediction nor a confidence bound of the mean replaces a platform worst case "
           "in the verification.",
           "Neither the point prediction nor a confidence bound of the mean ever replaces it.")
    nclaim("criteria", "verification of the leached Protein A platform worst case",
           "The leached Protein A platform worst case is not verified; the platform value stands.",
           [("criteria", "For leached Protein A, PCMP-001 §7.5 lets the platform value stand, because "
                         "leached Protein A is monitored on the pools"),
            ("changes", "The leached Protein A value stands under that rule, because leached Protein A is "
                        "not a response of the designs")],
           rationale="Leached Protein A is monitored on the pools and is not a response of the designs.")
    nclaim("par", "range over a discontinuous set of acceptable settings",
           "No range is claimed for a pair whose acceptable settings do not form one contiguous interval "
           "containing the set-point; the discontinuity is reported as it stands.",
           "Where they do not, the discontinuity will be reported as it stands and no range will be claimed "
           "for that pair.")
    nclaim("par", "proven acceptable range beyond the characterization range",
           "A range that reaches the edge of the characterization range is reported as reaching it, and no "
           "claim is made beyond it.",
           "A range that reaches the edge of the characterization range is reported as reaching it, and no "
           "claim is made beyond it.")
    nclaim("schedule", "instrumented system named in the study record",
           "The record of execution names none of the instrumented scale-down systems of PCMP-001 Table 5.1 "
           "for the studies of the plan.",
           "The record names none of the instrumented scale-down systems under calibration and change "
           "control of PCMP-001 Table 5.1 for these studies.")
    nclaim("risks", "confirmation at scale at the edges of the ranges",
           "The operating region is not confirmed at scale at the edges of the ranges; Stage 2 confirms "
           "performance at commercial scale inside the NORs only.",
           "The operating region is not confirmed at scale at the edges of the ranges, and Stage 2 confirms "
           "performance at commercial scale inside the NORs only.",
           elsewhere="Stage 2")
    nclaim("appA", "results of the designs",
           "The plan shows no result of the designs; the executed matrices with their measured responses "
           "are reported in PCR-008.",
           "No result is shown, and the executed matrices with their measured responses will be reported in "
           "the appendices of PCR-008.",
           elsewhere="PCR-008 (appendices)")

    # ---- document relationships ------------------------------------------------------------------
    rels = []

    def relation(kind, target, statement, sec, quote, caption=None, label=None, header=None):
        rels.append(DocumentRelationship(
            relationship_id=f"{doc}-R{len(rels) + 1:02d}", kind=kind, source_document_id=doc,
            target_document_ref=target, statement=statement,
            source_references=[ref(sec, quote, caption, label, header)], metadata=meta()))
    for target, row in rel.items():
        txt = _cells(row)[-1]
        relation(REL_KIND.get(txt, "references"), target, txt, "related", row, rel_cap, "tbl-related",
                 rel.header)
    relation("supersedes", f"{doc} Version {REV1['rev']}", "Version 2.0 supersedes Version 1.0 of the "
             "plan.", "title", tb["Supersedes"], header=tb.header)
    relation("references", "PCP-009", "The small-virus retentive filter is characterized under its own "
             "plan, and this study claims no clearance that belongs to that filter.", "purpose",
             q("The small-virus retentive filter is characterized under its own plan, PCP-009, and this "
               "study claims no clearance that belongs to that filter."))
    relation("references", "PCP-007", "The cation exchange step, which sets the attributes of the load "
             "of this step, is characterized under the cation exchange plan.", "risk", q_load)
    q_inv2 = q("The revision is also issued under INV-002, which investigated response surface models that "
               "fell below the model adequacy criteria of PCMP-001 Version 2.0.")
    relation("references", "INV-002", "The revision is also issued under INV-002, the investigation of the "
             "response surface models below the model adequacy criteria of PCMP-001 Version 2.0.",
             "changes", q_inv2)
    q_amd = q("""The method decision `{python} AMD["id"]` of `{python} AMD["date"]` set this method for every study that measures fragments, at every step, so that one method spans the train (PCMP-001 §7.8).""")
    relation("references", AMD["id"], "The analytical method decision that set nrCE-SDS as the method for "
             "fragments in every study, at every step.", "analytical", q_amd)
    q_ptp = q("Version 1.0 committed no calendar dates, and the campaign schedule is held in PTP-001.")
    relation("references", "PTP-001", "The campaign schedule is held in the Process Transfer Plan.",
             "schedule", q_ptp)

    # ---- deviation recorded against the first execution -----------------------------------------
    sup = win_df.loc[win_df["Study"] == ids["superseded"]].iloc[0]
    deviation = Deviation(
        deviation_id=ns["dev_sup"],
        summary=f"The first execution of the screening and response surface designs (study "
                f"{ids['superseded']}, {sup['Start']} to {sup['End']}) was invalidated; PCR-008 records "
                f"the deviation.",
        unit_operation=AXUO_NAME, disposition="invalidated",
        source_references=[tref("schedule", win_t, winrow, ids["superseded"]),
                           ref("schedule", ns["WIN_NOTE"], win_t.caption, win_t.label)],
        metadata=meta())

    # ---- studies: each on its own row of the execution-window table, plus its design -------------
    mv_names = [prm[k].name for k in ns["MV"]]
    uv_names = [prm[k].name for k in ns["UV"]]
    resp = list(D.responses(AXUO))
    q_cp = q("The screening design includes `{python} c_scr` centre point replicates and the response "
             "surface design includes `{python} c_rsm`.")
    q_qual_cmp = q("Qualification will compare the model against commercial-equivalent runs on step yield, "
                   "pool host cell protein, residual DNA, leached Protein A, the pressure across the bed and "
                   "the shape of the flow-through peak.")
    design = {
        # no n_runs: the qualification compares scale-down runs with manufacturing batches, which is
        # not a design (tests/test_config.py matches n_runs against the seeded designs)
        "qualification": dict(
            responses=["step yield", "pool host cell protein", "residual DNA", "leached Protein A",
                       "pressure across the bed", "shape of the flow-through peak"],
            refs=[("sdm", q_qual_cmp),
                  ("sdm", """The qualification compares `{python} n_sd` scale-down runs at set-point with `{python} n_m` batches made at manufacturing scale (study `{python} ids["qualification"]`), and these runs and the offset estimates come before the first characterization run of the step.""")]),
        "screening": dict(
            design_name="two-level full factorial with centre points", factors=mv_names,
            responses=resp + D.fragment_responses(AXUO, "screening"),
            n_runs=int(ns["n_scr"]), n_center_points=int(ns["c_scr"]),
            refs=[("screening", "The `{python} n_mv` multivariate parameters will be studied in a "
                                "two-level full factorial design of `{python} n_fact` runs, augmented with "
                                "`{python} c_scr` centre points, for `{python} n_scr` runs in total."),
                  ("screening", """A full factorial in these parameters estimates every main effect and every two-factor interaction without confounding, which the interaction between `{python} N["load_ph"]` and `{python} P["wash1_cond"].name` requires.""")]),
        "rsm": dict(
            design_name="face-centred central composite design", factors=mv_names,
            responses=resp + D.fragment_responses(AXUO, "rsm"),
            n_runs=int(ns["n_rsm"]), n_center_points=int(ns["c_rsm"]),
            refs=[("rsm", "The same parameters will be studied in a face-centred central composite design "
                          "of `{python} n_rsm` runs."),
                  ("rsm", "The design adds `{python} n_axial` axial runs at the faces of the cube to "
                          "`{python} n_fact` factorial runs and `{python} c_rsm` centre points.")]),
        "univariate": dict(
            design_name="one factor at a time: the low, the centre and the high setting of the range "
                        "studied, every other parameter at its set-point, with one viral clearance run at "
                        "the high setting",
            factors=uv_names, responses=[R["hcp"], "step_yield"],
            refs=[("univariate", "with every other parameter held at its set-point."),
                  ("univariate", "The low, the centre and the high setting of the range will be executed, "
                                 "and pool host cell protein and step yield will be measured on each."),
                  ("univariate", "A viral clearance run at the high setting will be included, because "
                                 "residence time is the mechanism by which flow rate could act on clearance "
                                 "and the high setting is the shortest residence time in the range.")]),
    }
    if set(design["univariate"]["responses"]) - set(resp):
        raise ValueError(f"{DOC}: univariate responses are not responses of the step")
    studies, unrendered, skipped = [], [], []
    for r in ns["mine"].itertuples():
        stype = STUDY_TYPE.get(r.kind)
        if stype is None:
            skipped.append(r.id)
            continue
        if not G._present(winrow[r.id], text):
            unrendered.append(r.id)
            continue
        d = dict(design[r.kind])
        refs = [tref("schedule", win_t, winrow, r.id)]
        refs += [ref(s_, q(x)) for s_, x in d.pop("refs")]
        if r.kind in ("screening", "rsm"):
            refs.append(ref("sampling", q_cp))
            appx = "appA" if r.kind == "screening" else "appB"
            refs.append(ref(appx, mtx[r.kind].caption))
        studies.append(S.StudyDesign(
            study_id=f"study:{r.id}", study_type=stype, unit_operation=AXUO_NAME,
            scale_down_model=sdm_name,
            associated_parameters=[AXPARAM_CONCEPT[x] for x in d.get("factors", [])],
            source_references=refs, metadata=meta(), **d))
    if skipped != [ids["superseded"]]:
        raise ValueError(f"{DOC}: studies with no study type {skipped}, expected only the first execution")

    # ---- entities -------------------------------------------------------------------------------
    def section(key, **kw):
        return S.SectionEntityExtraction(document_id=doc, section_id=_sid(key),
                                         non_claims=nc_at.get(key, []), **kw)
    entities = [
        section("purpose", process_steps=[step], sites=_site_entities(doc, f, _sid("purpose")),
                equipment=[equipment[2]]),
        section("changes"),
        section("related", document_relationships=rels),
        section("uo"),
        section("cqas", quality_attributes=attrs, contributions=contributions),
        section("risk"),
        section("sdm", equipment=[equipment[0]]),
        section("operation", equipment=[equipment[1]]),
        section("analytical", analytical_methods=methods),
        section("sampling"),
        section("stats"),
        section("factors", parameters=params),
        section("univariate"),
        section("criteria"),
        section("par"),
        section("schedule", deviations=[deviation]),
        section("risks"),
        section("appA"),
    ]
    listed = {n_.non_claim_id for e in entities for n_ in e.non_claims}
    if listed != {n_.non_claim_id for n_ in nc}:
        raise ValueError(f"{DOC}: non-claims of sections with no entity record")

    # ---- assertions -----------------------------------------------------------------------------
    add(STEP_ID, "step_uses_equipment", SDM_ID,
        "The characterization studies of the anion exchange step are executed on a scale-down model of "
        "the commercial anion exchange column, qualified under SOP-1001.", [ref("sdm", q_sdm)])
    add(STEP_ID, "step_uses_equipment", f"equip:{CHR}",
        f"The plan identifies the temperature-controlled chromatography chamber {CHR} as the instrumented "
        f"system for the anion exchange characterization runs; the record of execution names no "
        f"instrumented system for these studies.",
        [tref("operation", eq_t, eqrow, CHR), ref("operation", q_chamber)])
    add(STEP_ID, "step_uses_equipment", COLUMN_ID,
        "At commercial scale the anion exchange step runs on the commercial column, of which the study "
        "uses a scale-down model.", [ref("purpose", q_col)])
    for name in prow:
        add(STEP_ID, "step_has_parameter", AXPARAM_CONCEPT[name],
            f"{AXUO_NAME} has process parameter {name}.", [tref("factors", pt, prow, name)])
    role_txt = {"Contributes a claim": "contributes a claim to {n}, which is cumulative across the steps "
                                       "that clear the virus",
                "Clears": "clears {n}, an impurity formed upstream and cleared by more than one step",
                "Passes unchanged": "passes {n} through unchanged on the platform, and fragments are "
                                    "judged in its pool"}
    for key in ckeys:
        refs = [tref("cqas", cq_t, crow, key)]
        head = head_of(crow, key)
        if head != key:                       # the role is the merged cell of the group's first row
            refs.append(tref("cqas", cq_t, crow, head))
        add(STEP_ID, "step_has_quality_attribute", f"attr:{key}",
            f"{AXUO_NAME} " + role_txt[ns["ROLE"][key]].format(n=names[key]) + ".", refs)
    for amv in sorted(title_of):
        for key in attrs_of[amv]:
            add(f"attr:{key}", "attribute_measured_by_method", f"method:{amv}",
                f"{names[key]} is measured by {amv} ({title_of[amv]}).",
                [ref("analytical", q_method[amv])])
    q_crit_qa = q("""Pool host cell protein must meet `{python} CRIT["hcp"]` and fragments `{python} CRIT["lmw"]`, each judged on a single batch through the `{python} pi` % prediction interval.""")
    q_crit_vc = q("""The log reduction factor of XMuLV must meet `{python} CRIT["x"]` and that of MVM `{python} CRIT["m"]`, each judged on the mean prediction at the least favourable combination of NOR low, set-point and NOR high of the multivariate parameters""")
    basis_txt = {"drug substance": "the drug substance criterion, because no step after anion exchange "
                                   "changes the attribute",
                 "platform claim": "the platform claim of the step"}
    for key, row in iacrow.items():
        x = iac.loc[key]
        r_ = R[short_of[key]]
        lo_, hi_, stype_ = ACC[short_of[key]]
        if (lo_, hi_) != (float(x["iac_low"]), float(x["iac_high"])):
            raise ValueError(f"{DOC}: the criterion of {key} in the plan's text is not its IAC row")
        stat = D.decision_statistic(r_)
        how = (f"on a single batch, through the {pi} % prediction interval" if stat == "batch" else
               "on the mean prediction at the least favourable combination of NOR low, set-point and NOR "
               "high of the multivariate parameters")
        scale = (", at manufacturing scale after the scale-down offset is subtracted"
                 if D.sdm_offset(AXUO, r_) is not None else
                 ", as the scale-down model gives it, its offset being unknown")
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{AXUO}_{key}_iac",
            f"At the anion exchange step, {names[key]} is judged against the Version 2.0 intermediate "
            f"acceptance criterion {CRIT[short_of[key]]} ({x['basis']}), {how}{scale}.",
            [tref("par", iac_t, iacrow, key),
             ref("criteria", q_crit_qa if stat == "batch" else q_crit_vc)])
    # the plan's stated expectations from prior knowledge (not results)
    q_rank = q("""The highest ranks went to `{python} N["load_ph"]`, `{python} N["wash1_cond"]` and `{python} N["load_cond"]`, because together they set how strongly an acidic host cell protein binds.""")
    q_low_ph = q("A low load pH and a high conductivity both weaken that binding, and together they let host "
                 "cell protein flow through with the antibody.")
    for k, how, quote in (
            ("load_ph", "At a higher load pH the pH lies above the isoelectric point of more of the host cell "
                        "proteins, so more of them carry a net negative charge and bind; a low load pH lets "
                        "host cell protein flow through with the antibody.",
             "At a higher load pH the pH lies above the isoelectric point of more of the host cell proteins, "
             "so more of them carry a net negative charge and bind."),
            ("wash1_cond", "A higher Equil/Wash-1 conductivity screens the electrostatic interaction and lets "
                           "weakly bound host cell protein pass with the antibody.",
             """A higher conductivity of the equilibration and first wash buffer, the `{python} P["wash1_cond"].name`, screens the electrostatic interaction and lets weakly bound host cell protein pass with the antibody."""),
            ("load_cond", "A higher load conductivity weakens the binding of the more weakly charged "
                          "impurities, so weakly charged host cell protein is the first to pass into the "
                          "pool.",
             "A higher load conductivity weakens the binding of the more weakly charged impurities, and as "
             "the ligand fills, more strongly charged species displace them, so weakly charged host cell "
             "protein is the first to pass into the pool.")):
        add(pcid[k], "parameter_impacts_attribute", "attr:hcp", how,
            [ref("uo", q(quote)), ref("risk", q_rank)] + ([ref("risk", q_low_ph)] if k == "load_ph" else []))
    add(pcid["load"], "parameter_does_not_significantly_impact_attribute", "attr:hcp",
        "Within the range studied, protein load is not expected to raise pool host cell protein: a higher "
        "load raises it only where the bound impurity approaches the capacity of the ligand, and the "
        "impurity mass is expected to stay below that capacity.",
        [ref("uo", q("Pool host cell protein is expressed per milligram of antibody, so a higher load raises "
                     "it only where the bound impurity approaches the capacity of the ligand and starts to "
                     "break through.")),
         ref("uo", q("Within the range studied the impurity mass is expected to stay below that capacity."))])
    q_vc_ph = q("For both viruses, clearance is expected to fall as the load pH drops toward the point at "
                "which the particle surface loses its negative charge, and as the conductivity rises")
    q_res = q("Flow rate sets the residence time in the bed.")
    q_slow = q("Virus particles are large and diffuse slowly to the ligand, so their clearance is the most "
               "likely to fall at a short residence time.")
    for key in ("lrv_xmulv", "lrv_mvm"):
        add(pcid["load_ph"], "parameter_impacts_attribute", f"attr:{key}",
            f"{names[key]} is expected to fall as the load pH drops toward the point at which the particle "
            f"surface loses its negative charge.", [ref("uo", q_vc_ph)])
    for key in ("lrv_xmulv", "lrv_mvm"):
        add(pcid["flow"], "parameter_impacts_attribute", f"attr:{key}",
            f"Operating flow rate sets the residence time in the bed, and {names[key]} is the response most "
            f"likely to fall at a short residence time, because virus particles diffuse slowly to the "
            f"ligand.", [ref("uo", q_res), ref("uo", q_slow)])
    add(pcid["load_ph"], "parameter_does_not_significantly_impact_attribute", "attr:step_yield",
        "Within the range studied, load pH is not expected to reduce step yield: the range is bounded above "
        "by the pH at which a fraction of the antibody would begin to bind.",
        [ref("factors", q("The load pH range is bounded above by the pH at which a fraction of the antibody "
                          "would begin to bind and yield would fall.")),
         ref("factors", q("so product loss is not expected anywhere in the design."))])

    # ---- report sections: the decisions, criteria and design of the plan -----------------------
    # purpose and scope
    sq("purpose", "This plan sets out the Stage 1 process characterization of the anion exchange "
                  "chromatography step of the A-Mab drug substance process",
       "PCP-008 sets out the Stage 1 process characterization of the anion exchange chromatography step "
       "of the A-Mab drug substance process.")
    sq("purpose", "The characterization supports the transfer of the process from the development site to "
                  "the commercial drug substance site under the Process Transfer Plan PTP-001.")
    sq("purpose", "The study covers the `{python} W(n_par)` process parameters that the risk assessment "
                  "RA-001 carried forward for this step.")
    sq("purpose", "Of these, `{python} W(n_mv)` are studied in a screening design and a response surface "
                  "design, and `{python} uv_mid` `{python} uv_verb` assessed one factor at a time.",
       "Of the `{python} W(n_par)` parameters, `{python} W(n_mv)` are studied in a screening design and a "
       "response surface design, and `{python} uv_mid` `{python} uv_verb` assessed one factor at a time.")
    sq("purpose", "The responses measured on the flow-through pool are host cell protein, the log reduction "
                  "factors of the two model viruses, step yield and fragments.")
    sq("purpose", "Residual DNA and leached Protein A are measured on the pool of every response surface run "
                  "and are monitored, not modelled")
    sq("purpose", """The commercial process is operated at a bioreactor scale of `{python} f"{V['commercial_scale_l']:,}"` L, and the anion exchange step processes the cation exchange pool derived from a single batch at that scale.""")
    # changes in this revision
    sq("changes", "Version 1.0 of this plan was approved on `{python} v1_date`, before the first study of "
                  "this step began on `{python} first_start` (the scale-down model qualification study "
                  "`{python} first_study`).",
       "Version 1.0 of PCP-008 was approved on `{python} v1_date`, before the first study of the step, the "
       "scale-down model qualification study `{python} first_study`, began on `{python} first_start`.")
    sq("changes", "Version 2.0 is the amendment of the step plans with the a priori criteria and the "
                  "fragment method that the QA investigation INV-001 calls for in its corrective action "
                  "CA2, and it is issued after the studies ran.")
    sq("changes", """QA opened INV-001 on `{python} INV["opened"]` after its review of the master report PCMR-001 Version 1.0 for BLA readiness, and closed it on `{python} INV["closed"]`.""")
    sq("changes", "INV-001 found that the criteria used to judge each step in the proven acceptable range "
                  "analysis had been set after the data were seen and were in no approved protocol "
                  "(INV-001 finding 1).")
    st("The revision is also issued under INV-002, which investigated the response surface models that "
       "fell below the model adequacy criteria of PCMP-001 Version 2.0.", [ref("changes", q_inv2)])
    sq("changes", "Version 2.0 keeps the designs, the sampling, the spiking and the decision rules of "
                  "Version 1.0 as Version 1.0 wrote them.")
    sq("changes", "Where the master plan PCMP-001 Version 2.0 sets a rule in place of one, the text gives "
                  "the rule of PCMP-001 and says so, and the list below names the Version 1.0 rule it "
                  "replaces.")
    sq("changes", "The outputs of the step are judged against the intermediate acceptance criteria that "
                  "PCMP-001 Version 2.0 derives a priori (its §7.3).")
    sq("changes", "Each drug substance criterion is carried back through the platform worst case of every "
                  "later step, that is the lowest clearance or the largest increase that the step showed "
                  "for X-Mab, Y-Mab and Z-Mab, with no margin.")
    sq("changes", "Version 1.0 judged every response on a single batch and did not say on which statistic "
                  "the operating region was drawn.")
    sq("changes", "The scale-down model is qualified for each output by its offset from manufacturing scale "
                  "(PCMP-001 §7.1), and whether it is qualified for an output is decided at analysis")
    sq("changes", "Version 1.0 tested for a difference between the scales and accepted the model only where "
                  "the test found no statistically significant difference, and it released no "
                  "characterization run on a model that had not passed.")
    sq("changes", """Fragments are judged at this step against the drug substance criterion, on results by nrCE-SDS (AMV-3020), the method that the method decision `{python} AMD["id"]` of `{python} AMD["date"]` set for every step""")
    sq("changes", "Version 1.0 did not list fragments as a response of this step and did not judge them.")
    sq("changes", "A response surface model is adequate when it passes the four conditions of PCMP-001 "
                  "§7.2.")
    sq("changes", """These are a significant model F-test, no significant lack of fit against pure error, a predicted R² within `{python} f"{gap_lim:.2f}"` of R² (the limit on overfitting), and residuals with no pattern and no run that dominates the fit.""",
       """The four conditions of PCMP-001 §7.2 are a significant model F-test, no significant lack of fit against pure error, a predicted R² within `{python} f"{gap_lim:.2f}"` of R² (the limit on overfitting), and residuals with no pattern and no run that dominates the fit.""")
    sq("changes", """Version 1.0 judged adequacy on the lack of fit test at p ≥ `{python} f"{alpha_lof:g}"` and an inspection of the residuals, and fixed no threshold for the coefficient of determination.""")
    sq("changes", "It allowed a model with significant lack of fit to be used for prediction where its "
                  "residual standard error was small against the margin to the limit, and it reported a "
                  "response with neither an adequate nor a justified model without a predictive model.",
       "Version 1.0 allowed a model with significant lack of fit to be used for prediction where its "
       "residual standard error was small against the margin to the limit.")
    sq("changes", """The criteria of the upstream steps rely on two platform worst cases of this step, a host cell protein clearance of at least `{python} f"{hcp_fold:g}"`-fold and a leached Protein A clearance of at least `{python} f"{lpa_fold:g}"`-fold.""")
    sq("changes", "PCR-008 verifies the host cell protein worst case on the response surface model of this "
                  "step, by the rule of PCMP-001 §7.5.")
    sq("changes", "The execution window of every study is recorded, as INV-001 preventive action PA3 "
                  "requires of every study record")
    sq("changes", "The Version 1.0 records gave no execution dates (INV-001 finding 5).")
    sq("changes", """Its title block carries `{python} REV1["effective"]`, the date on which the Version 1.0 reports were approved.""",
       """The title block of the frozen Version 1.0 text of the plan carries `{python} REV1["effective"]`, the date on which the Version 1.0 reports were approved.""")
    sq("changes", "which were added to the plan text when the package was compiled, without a revision of "
                  "the approved plan (INV-001 root cause 1).",
       "The step limits in the acceptance criteria of the frozen Version 1.0 text were added to the plan "
       "text when the package was compiled, without a revision of the approved plan (INV-001 root cause "
       "1).")
    sq("changes", "Capability is no longer estimated for this step alone.")
    sq("changes", """PCMP-001 Version 2.0 estimates it from the integrated process model of the train, against the drug substance criterion, and judges it in PCMR-001 against a Cpk of `{python} f"{CPK_TARGET:g}"`, expected in routine manufacture, and a Cpk of `{python} f"{CPK_MIN:g}"`, below which the control strategy needs an action""",
       """Capability is estimated from the integrated process model of the train against the drug substance criterion and judged in PCMR-001 against a Cpk of `{python} f"{CPK_TARGET:g}"`, expected in routine manufacture, and a Cpk of `{python} f"{CPK_MIN:g}"`, below which the control strategy needs an action.""")
    sq("changes", """An attribute is affected by a parameter when a term that contains the parameter is significant at α = `{python} f"{alpha:g}"` (PCMP-001 §6.2).""")
    sq("changes", "Version 1.0 did not define when a parameter acts on an attribute or when it is held well "
                  "inside its acceptable range, and it had no class for a critical parameter that is not "
                  "well controlled.")
    sq("changes", "Descriptive sentences of Version 1.0 that were scientifically wrong or imprecise are "
                  "corrected, without change to the design.")
    sq("changes", """The compiled text of Version 1.0 (change 7) judged pool host cell protein against `{python} f"{r1_hcp:.1f}"` ng/mg, the drug substance limit carried back through the nominal clearance of the later steps of this campaign and then divided by a margin of `{python} f"{r1_margin:g}"`.""")
    sq("changes", "Such margins differed by step and were chosen so that every step passed at its own "
                  "set-point (INV-001 finding 2).")
    sq("changes", "It judged the two model viruses against minimum step log reduction factors, each the "
                  "cumulative requirement minus the nominal clearance of the other steps of this campaign.",
       "The compiled text of Version 1.0 judged the two model viruses against minimum step log reduction "
       "factors, each the cumulative requirement minus the nominal clearance of the other steps of this "
       "campaign.")
    sq("changes", "The host cell protein criterion of Version 2.0 is wider than the Version 1.0 limit, and "
                  "the two viral clearance criteria are stricter.")
    # objectives
    for o in ("Quantify the effect of each studied parameter on pool host cell protein, on the log reduction "
              "factors for xenotropic murine leukaemia virus and minute virus of mice, and on step yield",
              "Define the multivariate operating region within which every governed quality attribute meets "
              "its criterion (a quality attribute on the single-batch limit and viral clearance on its mean "
              "prediction, as PCMP-001 Version 2.0 draws its design space), and state where the boundary of "
              "that region lies.",
              "Establish a proven acceptable range for each parameter and each attribute it governs, and "
              "confirm that the normal operating range falls inside it.",
              "Classify each parameter under the parameter classification procedure SOP-4001 from the "
              "effects demonstrated in the study and from the capability with which the parameter can be "
              "held.",
              "Determine whether the step meets its platform claims for both model viruses at the worst case "
              "within the NOR, and justify the Stage 2 ranges and this step's part of the control strategy.",
              """Verify the host cell protein clearance of this step against its platform worst case, `{python} f"{hcp_fold:g}"`-fold, on which the host cell protein criteria of the upstream steps rely."""):
        sq("objectives", o, "Objective: " + o[0].lower() + o[1:].rstrip(".") + ".")
    sq("objectives", "and the effect of each multivariate parameter on fragments.",
       "Objective: quantify the effect of each multivariate parameter on fragments.")
    # related documents
    sq("related", "RA-001 fixes the parameters and the ranges carried into the study, and PCR-008 will "
                  "report the executed study against this plan.")
    sq("related", "The scale-down model procedure SOP-1001 governs the qualification of the model, the "
                  "design of experiments procedure SOP-1002 the design and the statistical analysis of the "
                  "multivariate studies, and the operating procedure SOP-2011 the operation of the step "
                  "itself.")
    # prior knowledge
    sq("uo", "The resin carries a quaternary amine ligand with a fixed positive charge.")
    sq("uo", "Yield in flow-through mode is high, because the ligand repels the positively charged antibody.")
    sq("uo", "Product is lost only where part of the antibody comes close enough to neutral charge at the "
             "load pH to bind, and the range of load pH is set to avoid that.")
    sq("uo", "Whether an impurity binds depends on its net charge at the load pH and on how strongly the "
             "ionic strength of the buffer screens that charge.")
    sq("uo", "The effect of conductivity therefore depends on the load pH, and an interaction between the "
             "two is expected.",
       "The effect of conductivity depends on the load pH, so an interaction between them is expected and "
       "the design must be able to estimate it free of confounding.",
       also=[("uo", "The design must be able to estimate it free of confounding")])
    sq("uo", "A higher protein load brings more impurity mass onto each litre of resin.")
    sq("uo", "Binding at equilibrium does not depend on residence time, but the time a species needs to "
             "reach the ligand does.")
    sq("uo", "Particles of the retrovirus model, XMuLV, carry a net negative charge at the load pH and bind "
             "the ligand by the same electrostatic interaction as the acidic impurities.")
    sq("uo", "The parvovirus model, MVM, has no envelope and is small, and its capsid also carries a net "
             "negative charge at the load pH, so it binds by the same mechanism.")
    sq("uo", "The XMuLV claim of this step is orthogonal to that of low-pH inactivation, which acts on the "
             "viral envelope and not on the surface charge.")
    sq("uo", "MVM is not inactivated by low pH, so this step and the virus filter carry the whole claim for "
             "it.")
    sq("uo", "Residual DNA is a polyanion at every pH in the range studied and binds the ligand strongly.",
       "Residual DNA is a polyanion at every pH in the range studied and binds the ligand strongly, so its "
       "clearance is expected to be robust to the operating parameters.",
       also=[("uo", "Its clearance is expected to be robust to the operating parameters")])
    sq("uo", "Leached Protein A carries a net negative charge at the load pH and binds while the antibody "
             "passes through, so the step is expected to clear the ligand fragments that the capture step "
             "releases.")
    sq("uo", "The platform anion exchange step has been used to manufacture three previously licensed "
             "humanized IgG1 antibodies, X-Mab, Y-Mab and Z-Mab, and through A-Mab clinical supply")
    # quality attributes in scope
    st(ev("""The step claims `{python} f"{x_claim:g}"` log10 of XMuLV clearance, of a cumulative requirement of `{python} f"{x_req:g}"` log10, and `{python} f"{m_claim:g}"` log10 of MVM clearance, of a cumulative requirement of `{python} f"{m_req:g}"` log10."""),
       [ref("cqas", q_claims)])
    sq("cqas", "It clears `{python} W(n_cleared)` impurities that are formed upstream and cleared by more "
               "than one step, host cell protein, residual DNA and leached Protein A.",
       "The step clears `{python} W(n_cleared)` impurities that are formed upstream and cleared by more "
       "than one step: host cell protein, residual DNA and leached Protein A.")
    sq("cqas", "Fragments pass through the step unchanged on the platform and are judged in its pool.")
    sq("cqas", "The two viral clearance attributes carry very high criticality by rule, because a viral "
               "contamination would harm the patient directly, whatever their score (master plan PCMP-001 "
               "§3).")
    sq("cqas", "For host cell protein and fragments they equal the drug substance criteria, and for viral "
               "clearance they are the claims of this step.",
       "The criteria for the outputs of the step equal the drug substance criteria for host cell protein "
       "and fragments, and are the claims of the step for viral clearance.")
    # risk-based prioritization
    sq("risk", "Each parameter of the step was ranked in the risk assessment RA-001 on its potential impact "
               "on a critical quality attribute and on its potential to interact with other parameters, and "
               "the study type was assigned from the ranking.")
    sq("risk", "Parameters ranked high on both counts were assigned to the multivariate design.")
    sq("risk", "Parameters ranked high on impact but low on interaction were assigned to a univariate "
               "assessment.")
    sq("risk", "The outcome for this step is `{python} n_mv` parameters in the multivariate design and "
               "`{python} n_uv` assessed one at a time")
    sq("risk", """The design also includes `{python} N["load"]`, because the impurity mass loaded onto the column scales with it, and the ligand has a finite capacity for the species it binds.""")
    sq("risk", """`{python} P["flow"].name` was assigned to a univariate assessment, because binding of the small, highly charged impurities is fast relative to the residence time at every flow rate in the range.""")
    # scale-down model
    sdm = "sdm"
    sq(sdm, "The model keeps the bed height, the linear flow velocity, the protein load in grams of antibody "
            "per litre of resin, and the equilibration, load, wash and chase volumes expressed in column "
            "volumes.")
    sq(sdm, "Scaling on these variables holds the residence time and the impurity mass per unit of ligand "
            "equal to the commercial step.")
    sq(sdm, "PCMP-001 Version 2.0 replaces the acceptance rule of Version 1.0 by the offset rule of its "
            "§7.1.")
    sq(sdm, "The offset of an output is the mean of the scale-down runs at set-point minus the mean of the "
            "manufacturing-scale batches, reported with its two-sided `{python} ci_pct` % confidence "
            "interval, each end of which is a one-sided `{python} ci_one` % confidence bound.")
    sq(sdm, "Of the outputs compared, pool host cell protein is the only one with a criterion at this step",
       "Of the outputs compared at both scales, pool host cell protein is the only one with a criterion at "
       "the step, so the qualification decision concerns it alone.")
    sq(sdm, "Every judgement of a scale-down result for pool host cell protein against its criterion first "
            "subtracts the offset, so that ranges and conclusions are stated at manufacturing scale.")
    sq(sdm, "The model is qualified for pool host cell protein when the conclusion against its criterion "
            "over the NOR is the same with the offset at either end of its interval.")
    sq(sdm, "That conclusion is whether the output meets its criterion at every combination of NOR low, "
            "set-point and NOR high of the `{python} W(n_mv)` multivariate parameters.")
    sq(sdm, "It comes from the response surface model, so the decision is made at analysis and reported in "
            "PCR-008.",
       "The qualification decision comes from the response surface model, so it is made at analysis and "
       "reported in PCR-008.")
    sq(sdm, "A model whose conclusion changes between the two ends of the interval is not used for that "
            "output.")
    sq(sdm, "On the platform no step after cation exchange changes the fragment level (PCMP-001 §7.3), so the "
            "pool is expected to carry the fragments of its load at either scale.")
    sq(sdm, "The viral clearance runs will be executed on the same scale-down model in a dedicated "
            "containment laboratory, as a small-scale spiking study")
    sq(sdm, "The spiking model will be qualified separately, because adding a virus spike to the load changes "
            "the load itself.")
    sq(sdm, "That qualification will confirm that the spiked load matches the unspiked load in protein "
            "concentration, in pH and in conductivity, and that the spike volume stays below the fraction at "
            "which those attributes move.")
    sq(sdm, "Spiked and unspiked runs will be executed on matched load material, so that the clearance "
            "results and the impurity results describe the same step.")
    sq(sdm, "A replicate is a full independent execution of the step and not a repeat measurement of one "
            "pool, because a repeat injection estimates assay variability and lack of fit must be judged "
            "against the variability of the process.")
    # operation
    sq("operation", "The step will be operated as it is operated at commercial scale, under SOP-2011.")
    sq("operation", "The column is equilibrated with the equilibration buffer, loaded with the cation "
                    "exchange pool adjusted to the target pH and conductivity, and chased with the first wash "
                    "buffer.")
    sq("operation", "Each resin lot will be released against its certificate of analysis and packed and "
                    "tested under SOP-2008, and a packed column will be accepted on plate count and peak "
                    "asymmetry before use.")
    # analytical methods
    sq("analytical", "The precision of each assay and the number of runs therefore bound the smallest effect "
                     "the study can resolve on its response.")
    sq("analytical", "An apparent effect on a log reduction factor that is small relative to the variability "
                     "of the infectivity assay will be attributed to the assay rather than to the step.")
    # sampling
    sq("sampling", "Samples will be taken from the load and from the flow-through pool of every run.")
    st(ev("The screening design includes `{python} c_scr` centre point replicates and the response surface "
          "design includes `{python} c_rsm`, each executed as a separate run from a separate load "
          "aliquot."),
       [ref("sampling", q_cp),
        ref("sampling", q("Each replicate is executed as a separate run from a separate load aliquot"))])
    sq("sampling", "Load and pool samples will be retained frozen so that a response can be re-tested if an "
                   "assay result is invalidated.")
    sq("sampling", "The log reduction factor will be calculated from the total infectivity in the load and "
                   "the total infectivity in the pool.",
       "Viral clearance runs are sampled at the spiked load and at the pool, and the log reduction factor is "
       "calculated from the total infectivity in each.",
       also=[("sampling", "Viral clearance runs will be sampled at the spiked load and at the pool.")])
    sq("sampling", "Cytotoxicity and interference controls will be run for each matrix, and the detection "
                   "limit of the assay will be reported with any result that reaches it")
    # statistical methods (the coding statement as the plan states it)
    sq("stats", "Each parameter will be coded so that the set-point is 0 and the edges of the "
                "characterization range are ±1.")
    sq("stats", "Coding places the parameters on one scale, so that an effect estimated in coded units is "
                "comparable across parameters measured in different physical units.")
    sq("stats", "The screening data will be analysed by ordinary least squares with every main effect and "
                "every two-factor interaction in the model.")
    sq("stats", "An effect will be reported as twice the coded coefficient, which is the change in the "
                "response across the full characterization range of the parameter.")
    sq("stats", """Terms significant at p < `{python} f"{alpha:g}"` will be identified as active.""")
    sq("stats", "The response surface data will be analysed with a full quadratic model in the `{python} "
                "n_mv` multivariate parameters, fitted on the coded factors.",
       "The response surface data are analysed with a full quadratic model in the `{python} n_mv` "
       "multivariate parameters, fitted on the coded factors, and this is the predictive model of the "
       "study.",
       also=[("stats", "This is the predictive model of the study.")])
    sq("stats", "The operating region and the proven acceptable ranges of the multivariate parameters will be "
                "derived from it, and PCR-008 will report the coefficients, the analysis of variance and the "
                "diagnostics for each response.")
    sq("stats", "The model predicts the mean response, and at the edge of a region drawn on mean predictions a "
                "single batch meets its criterion only about half the time if variability is symmetrical.",
       "A quality attribute is judged on a single batch, because its criterion applies to each batch; at the "
       "edge of a region drawn on mean predictions a single batch meets its criterion only about half the "
       "time if variability is symmetrical.",
       also=[("stats", "A quality attribute is judged on a single batch, because its criterion applies to "
                       "each batch.")])
    sq("stats", "Each response surface model is reported with R², adjusted R² and predicted R², computed from "
                "the prediction error sum of squares, with the model F-test, and with the lack of fit test "
                "against pure error from the centre point replicates.")
    sq("stats", """The model F-test is significant at α = `{python} f"{alpha:g}"`.""",
       """Model adequacy condition 1: the model F-test is significant at α = `{python} f"{alpha:g}"`.""")
    sq("stats", """Lack of fit against pure error is not significant at α = `{python} f"{alpha_lof:g}"`.""",
       """Model adequacy condition 2: lack of fit against pure error is not significant at α = `{python} f"{alpha_lof:g}"`.""")
    sq("stats", """Predicted R² falls short of R² by no more than `{python} f"{gap_lim:.2f}"`.""",
       """Model adequacy condition 3, the limit on overfitting: predicted R² falls short of R² by no more than `{python} f"{gap_lim:.2f}"`.""")
    sq("stats", "The residuals show no pattern against the predicted values or the run order, and no single "
                "run dominates the fit.",
       "Model adequacy condition 4: the residuals show no pattern against the predicted values or the run "
       "order, and no single run dominates the fit.")
    sq("stats", """The absolute residuals are regressed on the predicted values, and the residuals are regressed on the run order, each at α = `{python} f"{res_alpha:g}"`.""")
    sq("stats", """A run with a Cook's distance above `{python} f"{cook_factor:g}"`/n is examined by deleting it and repeating the judgement.""")
    sq("stats", """The model fails this test only where a run's Cook's distance exceeds `{python} cook_fq_txt` of the F distribution with p and n − p degrees of freedom, where p is the number of model parameters and n the number of runs.""")
    sq("stats", """The factor of `{python} f"{cook_factor:g}"` is the usual convention, and for the `{python} n_rsm` runs of the response surface design the cut-off is `{python} f"{cook:.2f}"`.""")
    sq("stats", "A parameter with no active term in either model will be described as having no detectable "
                "effect on that response over the range studied.")
    sq("stats", """The model runs `{python} f"{V['n_monte_carlo']:,}"` simulated batches through every step in sequence, with each process parameter drawn from a normal distribution centred on its set-point, with a standard deviation of the width of its NOR divided by `{python} f"{sd_div:g}"`""",
       """Capability at commercial scale is estimated from the integrated process model of the train, which runs `{python} f"{V['n_monte_carlo']:,}"` simulated batches with each parameter drawn from a normal distribution centred on its set-point and a standard deviation of the width of its NOR divided by `{python} f"{sd_div:g}"`.""",
       also=[("stats", "Capability at commercial scale is estimated from the integrated process model of the "
                       "train (PCMP-001 §6.5).")])
    sq("stats", """A Cpk of at least `{python} f"{CPK_TARGET:g}"` is expected in routine manufacture, and a Cpk below `{python} f"{CPK_MIN:g}"` needs an action in the control strategy.""")
    sq("stats", "The same simulation gives, for each attribute, the probability that the drug substance is out "
                "of specification.")
    # factors, ranges and study type
    sq("factors", "The range studied is wider than the normal operating range for every parameter.")
    sq("factors", "A study confined to the normal operating range would place the edge of the operating region "
                  "outside the data, and a proven acceptable range may only be claimed over settings that "
                  "were actually run")
    sq("factors", "The conductivity of the equilibration and first wash buffer is set by buffer preparation and "
                  "is the more closely controlled of the two conductivities, and its range reflects the "
                  "spread that buffer preparation and column equilibration can produce.")
    sq("factors", "The conductivity of the load is set by the cation exchange pool and by its adjustment, so "
                  "its range reflects what the preceding step delivers rather than a choice made at this "
                  "step.")
    sq("factors", "The protein load range extends well above the set-point, because the impurity mass carried "
                  "with the antibody scales with the load and the ligand has a finite capacity for the bound "
                  "species.")
    # screening and response-surface designs
    sq("screening", "The centre points estimate pure error and give a test for curvature, and curvature at the "
                    "centre indicates that a quadratic model is needed.")
    sq("screening", "Runs will be executed in randomized order within one resin lot and one load lot.")
    sq("screening", "Where the design cannot be completed within one load lot, the lots should be treated as a "
                    "block and the block term reported with the effects.")
    sq("rsm", "Axial points placed at the faces keep every run inside the characterization range, which an "
              "axial distance beyond the faces would not.")
    sq("rsm", "The quadratic terms this design supports are needed because the net charge on a protein or a "
              "capsid surface changes most steeply near its isoelectric point, so clearance rises more "
              "sharply over the part of the load pH range that lies nearest the isoelectric point of the "
              "bound species than over the rest of it.")
    sq("rsm", "Where it cannot be executed on the same load lot as the screening design, the second lot will "
              "be compared with the first on charge variant profile, host cell protein and protein "
              "concentration before the runs begin.")
    # univariate assessment
    sq("univariate", "Binding of the small, highly charged impurities is fast relative to the residence time "
                     "at every flow rate in the range, so residence time is not expected to limit their "
                     "clearance anywhere in the design.")
    sq("univariate", "Should the assessment show an effect of flow rate on any response, the parameter will be "
                     "carried into a multivariate design before its range is claimed.")
    # acceptance and decision criteria
    crit = "criteria"
    sq(crit, "PCR-008 will report the executed study against each rule of this section, and a criterion that "
             "is not met will be dispositioned as a deviation rather than revised after the fact.")
    sq(crit, "The rules are those of Version 1.0, except where PCMP-001 Version 2.0 sets a rule in place of "
             "one, and each item below says which applies.")
    sq(crit, "The model is qualified for pool host cell protein when the conclusion over the NOR is the same "
             "with the offset at either end of its `{python} ci_pct` % confidence interval, and the decision "
             "is made at analysis",
       "Scale-down model (PCMP-001 Version 2.0): the model is qualified for pool host cell protein when the "
       "conclusion over the NOR is the same with the offset at either end of its `{python} ci_pct` % "
       "confidence interval; a model not qualified for an output is not used for that output.",
       also=[(crit, "A model not qualified for an output is not used for that output.")])
    sq(crit, "This replaces the Version 1.0 rule that accepted the model where a test found no statistically "
             "significant difference between the scales.")
    sq(crit, "Load material will be accepted as representative where its charge variant profile by icIEF, its "
             "host cell protein content, its protein concentration, its pH and its conductivity fall within "
             "the release profile of the cation exchange pool.")
    sq(crit, "Load material outside that profile is not representative of routine operation, and a design "
             "executed on it will be invalidated for the definition of the operating region and re-executed "
             "in full on a qualified load.")
    sq(crit, "A model that fails the lack of fit test or the limit on overfitting is either refitted with a "
             "justified change of terms or transformation, or it is not used to set a range (PCMP-001 §7.2).")
    sq(crit, "For the model behind a widening bound, PCMP-001 §7.5 asks only the first three conditions "
             "(item 7).")
    sq(crit, "This replaces the Version 1.0 rule that accepted a model on its lack of fit test and its residual "
             "diagnostics and allowed a model with significant lack of fit where its residual standard error "
             "was small against the margin to the limit.")
    st(ev("""Pool host cell protein must meet `{python} CRIT["hcp"]` and fragments `{python} CRIT["lmw"]`, each judged on a single batch through the `{python} pi` % prediction interval."""),
       [ref(crit, q_crit_qa)])
    st(ev("""The log reduction factor of XMuLV must meet `{python} CRIT["x"]` and that of MVM `{python} CRIT["m"]`, each judged on the mean prediction at the least favourable combination of NOR low, set-point and NOR high of the multivariate parameters."""),
       [ref(crit, q_crit_vc)])
    sq(crit, "The multivariate operating region will be declared over the part of the characterized region in "
             "which every governed response meets its criterion simultaneously.")
    sq(crit, "The normal operating range of every parameter must fall inside that region.")
    sq(crit, "Where it does not, the normal operating range will be narrowed in the control strategy and the "
             "change will be carried into PCMR-001.")
    sq(crit, "A setting lies inside it when every quality attribute meets its criterion at both ends of the "
             "`{python} pi` % prediction interval of a single run, and viral clearance meets its claim on its "
             "mean prediction.",
       "PCMP-001 Version 2.0 draws the operating region, its design space, on the single-batch limit: a "
       "setting lies inside it when every quality attribute meets its criterion at both ends of the "
       "`{python} pi` % prediction interval of a single run, and viral clearance meets its claim on its mean "
       "prediction.",
       also=[(crit, "PCMP-001 Version 2.0 draws this region, its design space, on the single-batch limit.")])
    sq(crit, "Each parameter will be classified under SOP-4001 from the effect demonstrated on a critical "
             "quality attribute and from the capability with which the parameter is held.")
    sq(crit, "A parameter that acts on a critical quality attribute and is held well inside its acceptable "
             "range is a well-controlled critical process parameter.")
    sq(crit, "A parameter that acts on process performance without acting on a quality attribute is a key "
             "process parameter.")
    sq(crit, "A parameter with no demonstrated effect on either is a general process parameter, and the range "
             "studied bounds that classification.")
    sq(crit, "Its §7.7 also classes a parameter with such an effect and a high risk of leaving its acceptable "
             "range as a critical process parameter.",
       "PCMP-001 §7.7 classes a parameter with an effect on an attribute and a high risk of leaving its "
       "acceptable range as a critical process parameter.")
    sq(crit, """The criteria of the upstream steps assume that this step clears host cell protein at least `{python} f"{hcp_fold:g}"`-fold and leached Protein A at least `{python} f"{lpa_fold:g}"`-fold.""")
    sq(crit, "The host cell protein criteria of the `{python} hcp_up` pools and the leached Protein A "
             "criterion of the `{python} lpa_up` pool are carried back through these values (PCMP-001 §7.3).")
    sq(crit, "The host cell protein assumption is checked in PCR-008 on the response surface model of pool "
             "host cell protein, with the clearance factor taken as the nominal host cell protein of the load "
             "divided by the predicted pool value, by the rule of PCMP-001 §7.5.")
    sq(crit, "The model is evaluated at every combination of NOR low, set-point and NOR high of the "
             "multivariate parameters, with the NOR and the set-point as characterized, so that a later change "
             "of a NOR does not move a criterion.")
    sq(crit, "Where the lowest clearance predicted within the NOR is below the platform value, the one-sided "
             "`{python} vb` % prediction bound of a single batch at the least favourable combination replaces "
             "the platform value, and the upstream criteria become stricter.")
    sq(crit, "Where that bound is better than the platform value, and the response surface model behind it "
             "meets the first three adequacy conditions of PCMP-001 §7.2 (a significant model, no significant "
             "lack of fit and the limit on overfitting) and is not an exact fit, the bound replaces the "
             "platform value and the upstream criteria become wider.")
    sq(crit, "The fourth condition, on the residuals and on influential runs, does not decide the change, and "
             "PCR-008 examines it and states whether the bound depends on a single run.")
    sq(crit, "The study will be judged complete when the scale-down model is qualified for pool host cell "
             "protein, every planned run is executed or dispositioned, every response has an adequate model "
             "or a stated reason for the absence of one, the proven acceptable ranges bracket the normal "
             "operating ranges, and the clearance of both model viruses meets the claims of this step at the "
             "worst case within the NOR.")
    sq(crit, "A change of a criterion by the verification of item 7 is argued by its risk in PCR-008.",
       "A change of a criterion by the verification is argued by its risk in PCR-008: who bears the risk, "
       "whether and where an excursion would be detected, what the downstream steps must then clear, and "
       "the probability that the drug substance is out of specification.",
       also=[(crit, "The report states who bears the risk, the patient or the producer, and whether and where "
                    "an excursion would be detected, by an in-process test or by a release test."),
             (crit, "It also states what the downstream steps must then clear, and the probability that the "
                    "drug substance is out of specification (PCMP-001 §7.5).")])
    # proven acceptable ranges (planned analysis), with the set-point PAR method as the plan states it
    par = "par"
    sq(par, "For host cell protein and fragments no step after anion exchange changes the attribute on the "
            "platform, so the drug substance criterion applies to the pool of this step.")
    sq(par, "For the two model viruses the step is held to its platform claim, the log reduction that it "
            "delivered on the platform.")
    st(ev("""The XMuLV claims of `{python} x_steps` sum to `{python} f"{x_sum:g}"` log10 against a cumulative requirement of `{python} f"{x_req:g}"` log10, and the MVM claims of `{python} m_steps` sum to `{python} f"{m_sum:g}"` log10 against `{python} f"{m_req:g}"` log10, so a shortfall of the anion exchange step against its claim cannot be made up by the surplus of another step."""),
       [ref(par, q_sum),
        ref(par, q("A shortfall of this step against its claim therefore cannot be made up by the surplus of "
                   "another step."))])
    sq(par, "No result of the studies under this plan enters the criteria of this step",
       "No result of the studies under the plan enters the criteria of the anion exchange step; each "
       "criterion is in force at its a priori value.",
       also=[(par, "shows each criterion in force at its a priori value.")])
    for key, row in iacrow.items():
        x = iac.loc[key]
        unit = re.search(r"\(([^)]*)\)$", T.ATTR_NAME[key]).group(1)   # as the row labels the attribute
        st(f"The intermediate acceptance criterion for {names[key]} at the anion exchange step is "
           f"{basis_txt[x['basis']]}: {T.crit(x['iac_low'], x['iac_high'], x['spec_type'])} {unit}.",
           [tref(par, iac_t, iacrow, key)])
    sq(par, "A proven acceptable range is the range of one parameter over which the attribute it governs "
            "stays within its criterion, with the other parameters held or varied as the analysis states.")
    sq(par, "Two analyses will be run for every pair of a parameter and an attribute it governs, and both "
            "will be reported.")
    sq(par, "The first holds the other parameters at their set-points and evaluates the fitted response "
            "surface model across the parameter's characterization range.",
       "The first proven acceptable range analysis holds the other parameters at their set-points and "
       "evaluates the fitted response surface model across the parameter's characterization range.")
    sq(par, "The second varies the other parameters within their normal operating ranges by Monte-Carlo "
            "simulation of the fitted model, including its residual variance, and reads the range over which "
            "the predictive interval of the response stays within the criterion.",
       "The second proven acceptable range analysis varies the other parameters within their normal "
       "operating ranges by Monte-Carlo simulation of the fitted model, including its residual variance, "
       "and reads the range over which the predictive interval of the response stays within the criterion.")
    sq(par, "The normal operating ranges in the control strategy will be set from the second analysis, and the "
            "first will be reported beside it.")
    sq(par, """Each other parameter is drawn from a normal distribution centred on its set-point, with a standard deviation equal to the width of its NOR divided by `{python} f"{sd_div:g}"`, and clipped to the characterization range.""",
       """In the NOR-propagated analysis (PCMP-001 §6.4) each other parameter is drawn from a normal distribution centred on its set-point, with a standard deviation equal to the width of its NOR divided by `{python} f"{sd_div:g}"`, and clipped to the characterization range.""",
       also=[(par, "PCMP-001 Version 2.0 (§6.4) defines the second analysis, which it calls the "
                   "NOR-propagated analysis, and what it compares with the criterion.")])
    sq(par, """The draw treats each NOR as ±`{python} f"{sd_div / 2:g}"` standard deviations of the routine variation of its parameter.""")
    sq(par, """For pool host cell protein and fragments the analysis compares the `{python} pi` % prediction interval of a single batch, from the `{python} f"{p_lo:g}"`th to the `{python} f"{p_hi:g}"`th percentile of the simulated batches, which includes the model residual and the uncertainty of the fitted coefficients.""")
    sq(par, "At each setting the other parameters are set to every combination of their NOR low, set-point and "
            "NOR high, `{python} n_comb` combinations in all, and the lowest mean predicted log reduction "
            "factor must meet the claim, because viral clearance is validated under worst-case conditions.",
       "For XMuLV and MVM the analysis sets the other parameters to every combination of their NOR low, "
       "set-point and NOR high, `{python} n_comb` combinations in all, and the lowest mean predicted log "
       "reduction factor must meet the claim.")
    sq(par, "For viral clearance this replaces the Version 1.0 rule, which judged clearance on the predictive "
            "interval of the simulated batches.")
    sq(par, """The analysis will be evaluated on a grid of `{python} D.PAR_GRID` settings across the characterization range, with `{python} f"{D.PAR_MC_N:,}"` Monte-Carlo draws at each setting, under a fixed random seed recorded with the analysis""")
    sq(par, "A range will be reported only where the acceptable settings form one contiguous interval "
            "containing the set-point.")
    sq(par, "The governing parameter is the multivariate parameter with the largest main effect on that "
            "attribute in the response surface model.",
       "For each governed attribute PCR-008 plots the response against its governing parameter, the "
       "multivariate parameter with the largest main effect on that attribute in the response surface model.",
       also=[(par, "For each governed attribute the report will also carry a plot of the response against its "
                   "governing parameter, with the acceptable region shaded green and the set-point and the "
                   "normal operating range marked.")])
    sq(par, "A range is proven acceptable for an attribute when the NOR-propagated analysis meets the "
            "criterion across it, and for a parameter that affects several attributes the range carried into "
            "the control strategy is the intersection of its ranges.")
    sq(par, "Where an output does not meet its criterion even at the set-point, PCR-008 reports that no proven "
            "acceptable range exists for that attribute and states the consequence for the NOR.")
    sq(par, "Where a proven acceptable range does not contain the whole normal operating range, the normal "
            "operating range will be narrowed rather than the criterion relaxed.")
    # data management and integrity
    sq("data", "Data generated under this plan will follow the ALCOA+ principles.")
    sq("data", "A run that is aborted or that departs from SOP-2011 will be recorded with the reason, and the "
               "disposition of its data will be decided before the analysis begins.")
    sq("data", "The Monte-Carlo analyses use a fixed random seed of `{python} D.PAR_SEED`, so that a reported "
               "range can be reproduced exactly from the same data.")
    sq("data", "Data will be reviewed by a second qualified person against the raw records before the analysis "
               "is run, and the review will be documented.")
    sq("data", "Deviations from this plan will be recorded and dispositioned in PCR-008 under the site "
               "deviation procedure, with an impact assessment for each.")
    # roles and responsibilities: one statement per row of the roles table
    for func, row in roles.items():
        resp_ = _cells(row)[1]
        st(f"{func}: {resp_[0].lower() + resp_[1:]}.",
           [ref("roles", row, roles_cap, "tbl-roles", roles.header)])
    sq("roles", """Statistics approves the designs before execution rather than after, since a design that cannot estimate the interaction between `{python} N["load_ph"]` and `{python} P["wash1_cond"].name` cannot be repaired by analysis.""")
    # deliverables and schedule
    sq("schedule", "The deliverable of this plan is PCR-008, the process characterization report for the anion "
                   "exchange step.")
    sq("schedule", "PCR-008 rolls up into the master report PCMR-001, which consolidates the cumulative viral "
                   "clearance claim across the contributing steps.")
    sq("schedule", "The screening design is executed next, then the response surface design, then the "
                   "univariate assessment.",
       "The study runs in four phases: the scale-down model qualification runs first, then the screening "
       "design, the response surface design and the univariate assessment.",
       also=[("schedule", "The study will run in four phases."),
             ("schedule", "The scale-down model qualification runs come first")])
    sq("schedule", "The viral clearance runs may run in parallel with the univariate assessment, because they "
                   "use a separate laboratory and separate load aliquots.")
    st("The plan gives the execution window of each of its studies, from its first run to its last, as "
       "INV-001 preventive action PA3 requires every study record to state; Version 1.0 committed no "
       "calendar dates.",
       [ref("schedule", q("from the date of the first run of each to the date of its last, as INV-001 "
                          "preventive action PA3 requires every study record to state.")),
        ref("schedule", q_ptp)])
    # risks and assumptions
    sq("risks", "The scale-down model may not represent the commercial column.")
    sq("risks", "The offsets of fragments and viral clearance are unknown, not zero, and their judgement rests "
                "on the spiked scale-down model and on the expectation that the step does not change the "
                "fragment level of its load.")
    sq("risks", "A load with more acidic charge variants carries more antibody whose net charge at the load pH "
                "is close to neutral, and part of it can bind, so the yield is at risk.")
    sq("risks", "The designs together require a large volume of cation exchange pool, and pooling several "
                "cation exchange batches to obtain it would blur the load attributes the study holds constant.")
    sq("risks", "Load lots will therefore be scheduled against the runs before execution begins.")
    sq("risks", "The study assumes that platform knowledge from X-Mab, Y-Mab and Z-Mab transfers to A-Mab at "
                "this step, because A-Mab has an isoelectric point well above the load pH range and passes "
                "through the bed as the platform antibodies do, and the platform buffer system is unchanged.")
    sq("risks", "It assumes the resin performs within its qualified life cycle over the execution period under "
                "SOP-2008.",
       "The study assumes the resin performs within its qualified life cycle over the execution period under "
       "SOP-2008.")
    # approvals
    sq("approvals", "Approval by Quality Assurance releases the study for execution.")
    sq("approvals", "A change to this plan after approval will be made by revising the plan and will be "
                    "approved by the same functions before the affected runs are executed.")
    sq("approvals", "This Version 2.0 is the amendment that INV-001 required of each step plan in its "
                    "corrective action CA2, the amendment of PCP-003 to PCP-010 with the criteria and the "
                    "fragment method, and it was issued after the runs and approved on its effective date, "
                    "`{python} ver_eff`.")
    # appendices (the coding of the planned matrices as the plan states it)
    sq("appA", "The runs are given in coded units, where the set-point is 0 and the edges of the "
               "characterization range are ±1.",
       "The planned design matrices give the runs in coded units, where the set-point is 0 and the edges of "
       "the characterization range are ±1.")
    sq("appA", "Run order will be randomized at execution.")
    sq("appB", "The axial runs sit at the faces of the cube, so no run lies outside the characterization "
               "range.")

    # ---- concepts -------------------------------------------------------------------------------
    concepts = [Concept(concept_id=STEP_ID, concept_type="PROCESS_STEP", canonical_name=AXUO_NAME,
                        aliases=["anion exchange", "anion exchange chromatography step",
                                 "anion exchange step", UO_TITLE, f"Step {uo.step}"],
                        review_status="human_verified")]
    alias = {"wash1_cond": ["conductivity of the equilibration and first wash buffer"],
             "load_cond": ["conductivity of the load"], "flow": ["flow rate"]}
    concepts += [Concept(concept_id=pcid[k], concept_type="PROCESS_PARAMETER", canonical_name=p.name,
                         aliases=sorted({N[k]} - {p.name}) + alias.get(k, []),
                         review_status="human_verified") for k, p in prm.items()]
    concepts += _attr_concepts(ckeys)
    concepts.append(Concept(concept_id="attr:step_yield", concept_type="PERFORMANCE_ATTRIBUTE",
                            canonical_name="Step yield", aliases=["step yield", "yield"],
                            review_status="human_verified"))
    concepts += _method_concepts(sorted(title_of), title_of)
    concepts += [Concept(concept_id=e.equipment_id, concept_type="EQUIPMENT",
                         canonical_name=e.equipment_name, review_status="human_verified")
                 for e in equipment]

    # ---- notes ----------------------------------------------------------------------------------
    nor_note = ("No set-point or NOR of the step changed at Version 2.0, so ProcessParameter.target_value "
                "and NOR are the values of the parameter table, which are also the values in force."
                if not moved else
                f"ProcessParameter.target_value and NOR are the values of the parameter table, against which "
                f"the studies were planned; the values in force differ for {', '.join(moved)}.")
    disc = [d for d in P.PLAN_DISCREPANCIES.get("PCR-008", []) if d.get("studies")]
    disc_txt = "; ".join(f"{', '.join(d['studies'])} ({d['id']})" for d in disc)
    annex = S.GroundTruthAnnex(
        document_id=doc, document_title=f"{P.DOC_REGISTRY[doc][0]} — {P.DOC_REGISTRY[doc][1]}",
        document_class=P.DOC_REGISTRY[doc][0], **rev2_layer(doc, f),
        schema_extensions_used=COMMON_EXT + REV2_EXT,
        out_of_schema_notes=[
            "Classification is a result of the study, so every parameter_type is 'unclassified'. "
            + nor_note + " ProcessParameter.PAR carries the range studied, as everywhere in the corpus; the "
            "plan claims no proven acceptable range, so there are no ProvenAcceptableRange records, and no "
            "DesignSpace record (the plan states how the operating region will be drawn, which is a "
            "statement). The four multivariate parameters are also anchored on their row of the coded "
            "factor legend.",
            f"studies holds the scale-down model qualification and the screening, response surface and "
            f"univariate studies, each on its row of the execution-window table and its design prose; the "
            f"screening and response-surface records also cite the sampling sentence that gives their centre "
            f"points and the caption of their planned matrix (Appendices A and B are not represented row by "
            f"row). The first execution of both designs, {ids['superseded']}, has no StudyDesign.study_type; "
            f"it is the Deviation record {ns['dev_sup']}, anchored on its row of the execution-window table "
            f"and on the table note. The qualification compares scale-down runs with manufacturing-scale "
            f"batches, which is not a design, so it has no n_runs, and its responses are the outputs as the "
            f"plan names them (pressure across the bed and peak shape have no response key). The univariate "
            f"study names the viral clearance run at the high setting in its design_name; the plan does not "
            f"say which virus it uses. "
            + (f"Studies of the step made after Version 1.0 are not studies of this plan; PCR-008 records "
               f"them as discrepancies from it: {disc_txt}." if disc else ""),
            "acceptance_criteria holds the rows of the criteria-change table (the Version 1.0 analysis "
            "limits, superseded, and the Version 2.0 criteria, in force; fragments have no Version 1.0 "
            "record). Host cell protein and fragments are judged on a single batch, viral clearance on the "
            "mean prediction at the least favourable NOR combination of the multivariate parameters; the "
            "attribute_has_acceptance_criterion assertions are anchored on the rows of the IAC table and on "
            "the sentence of the decision criteria that states each criterion.",
            "The procedures table ties each validation reference to its title; each AnalyticalMethod record "
            "is anchored on its sentence of the analytical methods section and on that row (nrCE-SDS also on "
            "the row of its procedure SOP-3015). icIEF (AMV-3013) measures the charge variant profile of the "
            "load for its qualification, not an output of the step, so that record has no associated "
            "attribute and no attribute_measured_by_method assertion.",
            "The two viral clearance contributions are ModularContribution records: the claim of the step, "
            "the sum of the claims of the contributing steps and the cumulative requirement, anchored on the "
            "sentences that state them and on the IAC row of each virus. The platform worst cases of the step "
            "that the upstream criteria rely on (host cell protein and leached Protein A clearance) are "
            "statements, not criteria of this step.",
            "parameter_impacts_attribute and parameter_does_not_significantly_impact_attribute assertions are "
            "the plan's stated expectations from prior knowledge, not results.",
            f"The temperature-controlled chamber {CHR} is the instrumented system the plan identifies for the "
            f"runs; the plan also states that the record of execution names no instrumented system for these "
            f"studies (an ExplicitNonClaim), so no StudyDesign is linked to it. The commercial column is an "
            f"Equipment record at the receiving site, anchored on the sentence that names it and on the "
            f"roles-table row of the receiving site.",
            "Each row of the roles table is a statement. The approvals table, the abbreviations and the "
            "planned design matrices row by row are not represented. No rhetorical_spans: a plan has none. "
            "weak_claims is empty.",
        ] + _unrendered_note(unrendered),
        inventory=rev2_inventory(doc, f, "process_characterization_plan", AXUO_NAME,
                                 ["process characterization", "anion exchange chromatography",
                                  "flow-through mode", "viral clearance", "host cell protein clearance",
                                  "protocol amendment", "intermediate acceptance criteria",
                                  "scale-down offset", "design of experiments",
                                  "platform worst-case verification"]),
        entities=entities, studies=studies,
        report_sections=[ReportSection(section_id=f"{doc}-summary", title="Plan summary", statements=ST)],
        assertions=AssertionStore(run_id=f"gt-{doc}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{doc}", concepts=concepts),
        weak_claims=[], rhetorical_spans=[],
        acceptance_criteria=acceptance_criteria_layer(doc, f, SEC["changes"][-1],
                                                      ct["tbl-criteria-change"][0], [AXUO]))
    _gate(annex, text)
    return annex
