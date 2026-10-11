"""RA-001 Version 2.0, the pre-characterization process risk assessment of the A-Mab drug substance
process, reissued under corrective action CA3 of INV-001: its ground-truth annex (``build()``).

RA-001 has no designed experiment, no registered discrepancy and no weak claim. The concept ids and
the kinds of record follow the Version 1.0 builder (``build_risk_assessment``): the attribute register
as ``QualityAttribute`` records, every process parameter of the train as a ``ProcessParameter`` with
its initial risk and the study type assigned to it, the step -> parameter relations, the drug
substance criteria and the parameter -> attribute relations the failure modes put at risk (a
prospective relation, not a measured effect) as assertions, and the statements of the document. The
Version 2.0 layers follow the corpus-level model ``build_master_plan`` (PCMP-001) and the Version 2.0
plan builders: the revision layer, the process train and the two sites, the document relationships,
the explicit non-claims, and the statements, one report section per top-level section.

Every table of RA-001 is a complex table (``T.frame``), read back through ``qmd_ctables`` from the
object the document printed, so each row quote comes from the call that rendered the row, with
``table_header=rows.header``. The related-documents table and the title block are the markdown
strings of ``related_docs_md`` and ``title_block``. Every prose quote is a sentence of the ``.qmd``
(or a slice of one that stops short of a cross-reference, a citation or a quoted label), copied with
its inline expressions and evaluated in the document's own namespace (``qmd_inline``); ``q`` refuses
a snippet that is not a span of the ``.qmd`` prose, so no quote and no value is typed here.
``build()`` refuses to return an annex with a quote that does not ground or a weak anchor.
"""
from __future__ import annotations

import math
import os
import re

import _pcpkg as P
import build_ground_truth as G
import schema_ext as S
from check_grounding import CELL_SEP, normalize, specificity_report

DOC = "RA-001"
FILE = "RA-001_risk_assessment.docx"
QMD = "RA-001_risk_assessment.qmd"

_RANK = "Parameter risk ranking by unit operation"
#: Section key -> heading path as the document renders it. ``_check_sections`` checks every title
#: against the headings of the .qmd, so a renamed section fails loudly instead of mislabelling. The
#: subsections of the ranking are the unit operations, titled as ``UNIT_OP_TITLES`` names them.
SEC = {
    "title": ("Title block",),
    "purpose": ("Purpose and scope",),
    "changes": ("Purpose and scope", "Changes in this revision"),
    "method": ("Risk assessment methodology",),
    "cqa": ("Quality attributes at risk",),
    "ranking": (_RANK,),
    **{f"rk_{k}": (_RANK, P.UNIT_OP_TITLES[k]) for k in P.CFG.train_order},
    "assignment": ("Characterization study assignment",),
    "assumptions": ("Assumptions and limitations",),
    "outputs": ("Outputs and downstream use",),
    "approvals": ("Approvals",),
}


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
    """The cells of a rendered row: a continuation row keeps its empty leading cells."""
    return [c.strip() for c in row.split("|")]


def _unmark(cell):
    """A rendered cell without its trailing footnote marker ("Post-clarification turbidity a)")."""
    return re.sub(r"(?:\s[a-z]\))+$", "", str(cell)).strip()


def _unmark_raw(cell):
    """A DataFrame cell without its footnote markup ("Post-clarification turbidity^t)^")."""
    return re.sub(r"\^[a-z]\)\^", "", str(cell)).strip()


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
        """Annex text with the document's own values (inline expressions evaluated in its namespace)."""
        return G.qmd_inline(ns, txt)

    def ref(sec, quote, table=None, rows=None, caption=None, label=None):
        r = G.ref(DOC, FILE, _sid(sec), SEC[sec][-1], quote,
                  table_title=caption if table is None else table.caption,
                  table_id=label if table is None else table.label,
                  table_header=None if rows is None else rows.header)
        r.heading_path = list(SEC[sec])
        return r

    def keyed(label, keys, name_of, cell):
        """The rendered rows of the CTable the document printed under ``label``, keyed. Every row
        must name its own record in cell ``cell``: a mis-keyed row grounds and attests the wrong
        thing."""
        tab = ct[label][0]
        rows_ = G.ctable_rows(tab, keys)
        bad = [k for k, row in rows_.items() if _unmark(_cells(row)[cell]) != name_of(k)]
        if bad:
            raise ValueError(f"{DOC} {label}: rows keyed to records they do not name: {bad}")
        return tab, rows_

    def head_of(rows_, key):
        """For a continuation row, the row that opens its merged group (it carries the label the
        continuation row leaves empty)."""
        order = list(rows_)
        lead = next(j for j, c in enumerate(_cells(rows_[key])) if c)
        if lead == 0:
            raise ValueError(f"{DOC}: {key} opens its own group and reads like another row")
        for k2 in reversed(order[:order.index(key)]):
            if _cells(rows_[k2])[lead - 1]:
                return k2
        raise ValueError(f"{DOC}: no group head for {key}")

    def row_refs(sec, tab, rows_, key):
        """The row of ``key``, and its group head where the row reads exactly like another one
        (no row of RA-001 does today; a change to the register could make two alike)."""
        out = [ref(sec, rows_[key], tab, rows_)]
        if text.count(normalize(rows_[key])) > 1:
            out.append(ref(sec, rows_[head_of(rows_, key)], tab, rows_))
        return out

    # ---- the document's own data ---------------------------------------------------------------
    rows = ns["rows"]                                   # RC.ra_rows(), as the document scored them
    steps = list(ns["steps"])
    if steps != list(P.CFG.train_order):
        raise ValueError(f"{DOC}: the document's train is not the configured train")
    R = {(r["key"], r["pkey"]): r for r in rows}
    title = P.UNIT_OP_TITLES
    mid = ns["mid"]                                     # the step as a sentence names it
    stepno = {k: P.CFG.unit_op(k).step for k in steps}
    key_of_no = {v: k for k, v in stepno.items()}
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))
    cq = P.cqa_reg.set_index("key")
    reg = ns["reg"].set_index("key")                    # RC.cqa_table(): the criteria and severities printed
    reg31 = ns["reg31"]                                 # Table 3.1 as printed, in its row order
    set_by = dict(zip(P.cqa_reg["key"], P.cqa_reg["set_by"]))
    viral = ns["_viral"]                                # the document's own test for a viral attribute
    lc = ns["_lc"]

    def pid(key):
        return f"param:{key[0]}_{key[1]}"

    def plabel(key):
        return f"{R[key]['param']} ({T.STEP_NAME[key[0]]})"

    # ---- the rendered tables, from the objects the document printed -----------------------------
    tr_df = ct["tbl-train"][1]
    tr_t, trrow = keyed("tbl-train", [key_of_no[int(n)] for n in tr_df["Step"]], lambda k: title[k], 1)
    roles = dict(zip([key_of_no[int(n)] for n in tr_df["Step"]], tr_df["Principal role"]))
    sc_df = ct["tbl-scoring"][1]
    sc_t, scrow = keyed("tbl-scoring", list(zip(sc_df["Score"], sc_df["Parameter class"])),
                        lambda k: k[1], 1)
    ckeys = list(reg31["key"])
    cq_df = ct["tbl-cqa"][1]
    if list(cq_df["Quality attribute"]) != [names[k] for k in ckeys]:
        raise ValueError(f"{DOC}: the attribute table no longer lists the register in Table 3.1 order")
    cq_t, crow = keyed("tbl-cqa", ckeys, lambda k: names[k], 1)
    cq_notes = cq_t.notes_text().split(CELL_SEP)
    pkeys = [(r["key"], r["pkey"]) for r in rows]
    if list(ct["tbl-ranking"][1]["Parameter"]) != [r["param"] for r in rows]:
        raise ValueError(f"{DOC}: the ranking table no longer lists the parameters of the register")
    rk_t, rkrow = keyed("tbl-ranking", pkeys, lambda k: R[k]["param"], 2)
    fm = {}
    for k in steps:
        own = [r for r in rows if r["key"] == k]
        lab = next(lb for lb, (tab, df) in ct.items() if lb.startswith("tbl-fm-") and df is not None
                   and list(df["Parameter"]) == [r["param"] for r in own])
        fm[k] = keyed(lab, [(k, r["pkey"]) for r in own], lambda kk: R[kk]["param"], 0)
    pa_df = ct["tbl-params"][1]
    step_of_name = {T.STEP_NAME[k]: k for k in steps}
    pa_keys = []
    for s_, p_ in zip(pa_df["Step"], pa_df["Parameter"]):
        k = step_of_name[s_]
        pa_keys.append((k, next(r["pkey"] for r in rows if r["key"] == k and r["param"] == _unmark_raw(p_))))
    pa_t, parow = keyed("tbl-params", pa_keys, lambda k: R[k]["param"], 1)
    pa_val = {key: pa_df.iloc[i] for i, key in enumerate(pa_keys)}
    sp_df = ct["tbl-scope"][1]
    sp_t, sprow = keyed("tbl-scope", [key_of_no[int(n)] for n in sp_df["Step"]], lambda k: title[k], 1)
    sp_val = {key_of_no[int(r["Step"])]: r for _, r in sp_df.iterrows()}
    ap_df = ct["tbl-approvals"][1]
    ap_t, aprow = keyed("tbl-approvals", list(ap_df["Function"]), str, 0)
    corrections = []                                    # (table, rows, row, data) of both tables
    for lab in ("tbl-corrections", "tbl-corrections-2"):
        tab, df = ct[lab]
        rr = G.ctable_rows(tab)
        corrections += [(tab, rr, rr[i], df.iloc[i]) for i in rr]
    rel = G.md_string_rows(P.related_docs_md(DOC))
    rel_cap = re.search(r'print\(": (.*?) \{#tbl-related\}"\)', _source()).group(1)
    if normalize(f"{rel_cap} {rel.header}") not in text:
        raise ValueError(f"{DOC}: the related-documents caption no longer reads {rel_cap!r}")
    tb = G.md_string_rows(P.title_block(DOC, ns["UO_TITLE"]))

    # ==== entities ================================================================================
    #: The opening sentence of each unit operation's subsection, which says what the step does.
    OPEN = {
        "bioreactor": "The production bioreactor forms the glycan, charge variant and aggregate attributes of the drug substance.",
        "harvest": "Harvest separates the cells from the culture and clarifies the supernatant for capture.",
        "protein_a": "Capture binds the antibody from the clarified harvest and removes most of the host cell protein and DNA.",
        "viral_inactivation": "Holding the pool at low pH inactivates enveloped virus by disrupting the lipid envelope that XMuLV needs to enter a cell.",
        "cex": "The cation exchange step is the principal aggregate reduction step of the process.",
        "aex": "The anion exchange step is run in flow-through mode.",
        "virus_filtration": "The virus filter removes small non-enveloped virus by size and is the principal MVM clearance step.",
        "ufdf": "The formulation step concentrates the antibody and exchanges it into the drug substance buffer.",
    }
    process_steps = [S.ProcessStep(
        step_id=f"step:{k}", step_name=title[k], step_number=str(stepno[k]), unit_operation=title[k],
        description=roles[k],
        source_references=[ref("purpose", trrow[k], tr_t, trrow), ref(f"rk_{k}", q(OPEN[k]))],
        metadata=meta()) for k in steps]
    sites = G._site_entities(DOC, FILE, _sid("title"))

    # the parameters: each on its row of the ranking, of its step's failure-mode table and of the
    # parameter set handed to the plans
    def risk_text(r):
        return (f"Initial (pre-characterization) risk. Attribute(s) at risk: {r['cqa_label']}. Potential "
                f"failure mode: {r['fm']}; potential effect: {r['eff']}. Severity {r['severity']}, with "
                f"occurrence {r['o_init']} and detection {r['d_init']} assigned by class, gives an initial "
                f"RPN of {r['rpn_init']} and priority {r['priority']}; study type assigned: {r['study']}. "
                f"The assessment does not classify the parameter: its class is an output of the "
                f"characterization studies.")

    params = []
    for key in pkeys:
        r, x = R[key], pa_val[key]
        fm_t, fmrow = fm[key[0]]
        unit = x["Unit"]
        params.append(S.ProcessParameter(
            parameter_id=pid(key), parameter_name=r["param"], parameter_type="unclassified", unit=unit,
            target_value=f"{x['Set-point']} {unit}", NOR=f"{x['NOR']} {unit}",
            PAR=f"{x['Range studied']} {unit}", associated_step=f"{title[key[0]]} (Step {stepno[key[0]]})",
            rationale_for_criticality=risk_text(r), study_type=r["study"],
            source_references=row_refs("ranking", rk_t, rkrow, key)
            + row_refs(f"rk_{key[0]}", fm_t, fmrow, key) + row_refs("assignment", pa_t, parow, key),
            metadata=meta()))

    # the attribute register: each attribute on its row of Table 3.1, and on the prose that gives the
    # basis of its criticality where the document gives one
    crit = set(reg.index[reg["Criticality"].isin(["H", "VH"])])     # "high and very high" (Section 3)
    if len(crit) != ns["n_crit"]:
        raise ValueError(f"{DOC}: {len(crit)} critical attributes, the document counts {ns['n_crit']}")
    vir_rule = "The two viral clearance attributes carry very high criticality by rule, although their Tool #1 score is `{python} vir_t1`, because a viral contamination would harm the patient directly (PCMP-001 §3)."
    vir_sev = "Their severity follows from the very high criticality that the register gives viral clearance by rule (PCMP-001 §3)."
    QA_PROSE = {
        "high_mannose": ["High mannose has the highest Tool #1 score in the register, `{python} t1_max`.",
                         "High mannose glycans carry no core fucose, so they are expected to raise antibody dependent cellular cytotoxicity (ADCC) in the same way as afucosylation, and A-Mab acts on its target through ADCC."],
        "lrv_xmulv": [vir_rule, vir_sev],
        "lrv_mvm": [vir_rule, vir_sev],
        "acidic_variants": ["Acidic charge variants sit at the other end of the register, with a Tool #1 score of `{python} acid_t1` and a severity of `{python} acid_sev`.",
                            "Their impact is scored low because deamidation of A-Mab occurs at sites outside the binding region and outside the part of the Fc region that carries effector function, so the deamidated forms keep their activity."],
        "residual_dna": ["Residual DNA, with the lowest severity, `{python} dna_sev`, is treated the same way."],
        "fragments_lmw": ["Their criticality is `{python} frag_crit_word`, with a Tool #1 score of `{python} frag_t1`.",
                          "The A-Mab case study lists fragmentation among the typical quality attributes of an antibody but gives it no limit, and the sponsor set the criterion for fragments, `{python} frag_acc`, when they joined the register (PCMP-001 §3)."],
    }
    attrs = []
    for key in ckeys:
        c, g = cq.loc[key], reg.loc[key]
        sev = g["Severity"]
        scored = not (isinstance(sev, float) and math.isnan(sev))
        why = (f"Very high criticality, assigned by rule because a viral contamination would harm the "
               f"patient directly (PCMP-001 §3); Tool #1 score {int(g['Tool #1'])}."
               if viral({"cqas": [key]}) else
               f"Criticality {g['Criticality']}: Tool #1 score {int(g['Tool #1'])}, the product of impact and "
               f"uncertainty (Tool #1 of the A-Mab attribute assessment).")
        why += (f" Severity carried into this assessment: {int(sev)}." if scored else
                " No severity: the attribute joined the register after this assessment was made and was "
                "not scored.")
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=names[key],
            attribute_type="CQA" if key in crit else "unclassified", unit=c["unit"],
            acceptance_criteria=[f"{g['Acceptance']} (drug substance)"],
            analytical_method=None, associated_steps=[g["Set by"]], rationale_for_criticality=why,
            criticality_level=g["Criticality"], tool1_score=int(g["Tool #1"]),
            source_references=row_refs("cqa", cq_t, crow, key)
            + [ref("cqa", q(x)) for x in QA_PROSE.get(key, [])],
            metadata=meta()))

    # the one analytical method the document names: nrCE-SDS for fragments (PCMP-001 §7.8, AMD-001)
    q_frag_method = q("PCMP-001 Version 2.0 §7.8 sets non-reduced capillary electrophoresis with sodium dodecyl sulfate (nrCE-SDS) as the method for fragments, following the decision of `{python} amd_date` to change the fragment method (`{python} amd_id`).")
    amv_of_token = {v: k for k, v in G.SIZE_VARIANT_TOKEN.items()}
    frag_amv = amv_of_token["nrCE-SDS"]
    if "nrCE-SDS" not in reg.loc["fragments_lmw", "Acceptance"]:
        raise ValueError(f"{DOC}: the fragment criterion no longer names nrCE-SDS")
    method = S.AnalyticalMethod(
        method_id=frag_amv, method_name="nrCE-SDS", method_type=G.METHOD_TYPE.get(frag_amv),
        analytes=["fragments (low molecular weight species)"], associated_attributes=["attr:fragments_lmw"],
        source_references=[ref("changes", q_frag_method)], metadata=meta())
    attrs[ckeys.index("fragments_lmw")].analytical_method = frag_amv

    # the one study the document names: the first study of the campaign
    first = ns["chron"].loc[0]
    q_first = q("The first characterization study, `{python} first_id`, the qualification runs of the production bioreactor scale-down model, started on `{python} first_start`.")
    studies = [S.StudyDesign(
        study_id=f"study:{first['id']}", study_type=G.STUDY_TYPE[first["kind"]],
        unit_operation=title[first["step"]], source_references=[ref("changes", q_first)], metadata=meta())]

    # explicit non-claims, by section
    nc, nc_at = [], {}

    def nclaim(sec, subject, statement, quotes, rationale=None, elsewhere=None, uo=None):
        nc.append(ExplicitNonClaim(
            non_claim_id=f"{DOC}-NC{len(nc) + 1:02d}", subject=subject, unit_operation=uo,
            statement=statement, rationale=rationale, handled_elsewhere=elsewhere,
            source_references=[x if isinstance(x, S.SourceReference) else ref(s_, q(x)) for s_, x in quotes],
            metadata=meta()))
        nc_at.setdefault(sec, []).append(nc[-1])

    q_pcmr_resid = "PCMR-001 consolidates the reports and is where the risk that remains after characterization is addressed."
    q_sop4001 = "That classification follows the parameter classification procedure SOP-4001."
    q_pcmr_cls = "It is reported in the characterization report of each unit operation and consolidated in the master report PCMR-001."
    q_sop2008 = "This assessment attributed the amount released to the resin and its history of use, which are controlled under the resin life cycle procedure SOP-2008, and not to a parameter in"
    nclaim("purpose", "study results", "The assessment is prospective: it reports no study result, and no "
           "study result enters it.",
           [("purpose", "The assessment is prospective and reports no study result."),
            ("changes", "No study result enters this assessment, and it gives no final classification of any parameter.")])
    nclaim("purpose", "parameter classification (CPP, WC-CPP, KPP, GPP)",
           "The assessment does not classify parameters; each parameter is classified from the effects the "
           "characterization studies measure.",
           [("purpose", "The assessment does not classify parameters."), ("purpose", q_sop4001),
            ("purpose", q_pcmr_cls)],
           rationale="A parameter is classified from the effects that the characterization studies measure.",
           elsewhere="the characterization report of each unit operation, under SOP-4001, consolidated in PCMR-001")
    nclaim("purpose", "residual risk", "The assessment reports initial scores only; the risk that remains "
           "once the studies have reported is a separate assessment, which the document does not anticipate.",
           [("purpose", "The risk that remains once the studies have reported is a separate assessment, and nothing in this document anticipates it."),
            ("ranking", ref("ranking", rk_t.caption, caption=rk_t.caption, label=rk_t.label)),
            ("outputs", q_pcmr_resid)],
           elsewhere="PCMR-001")
    nclaim("purpose", "seed expansion train, drug product manufacture and the analytical methods",
           "The seed expansion train, drug product manufacture and the analytical methods themselves are "
           "outside the scope of the assessment.",
           [("purpose", "The seed expansion train, drug product manufacture and the analytical methods themselves are outside its scope.")])
    nclaim("method", "parameters given no new study",
           "The assessment assigns a study to every parameter: none is left without a new study on the "
           "strength of prior knowledge, although the A-Mab approach allows that outcome.",
           [("method", "The A-Mab approach also allows a parameter to be given no new study where prior knowledge supports its range."),
            ("method", "This assessment assigns no parameter to that outcome.")])
    nclaim("method", "critical and non-critical groups; control strategy",
           "The ranking orders the parameters against each other; it does not divide them into a critical "
           "and a non-critical group and it is not a control strategy.",
           [("method", "It does not divide them into a critical and a non-critical group, and it is not a control strategy."),
            ("method", "Both follow from the studies that this assessment scopes.")],
           rationale="Criticality is treated as a continuum and not as a binary split.",
           elsewhere="the characterization studies that the assessment scopes")
    nclaim("cqa", "fragments", "No parameter is scored against fragments and no severity is assigned to "
           "them.",
           [("cqa", "This assessment was made before fragments joined the register."),
            ("cqa", "No parameter is scored against fragments and no severity is assigned to them."),
            ("cqa", ref("cqa", cq_notes[[n.split(" ", 1)[1].startswith("Not scored.") for n in cq_notes].index(True)],
                        cq_t, caption=None))],
           rationale="Fragments joined the register at Version 2.0, after the assessment was made.")
    nclaim("cqa", "effect of a parameter on fragments",
           "Whether a parameter could change fragments is outside the assessment; the harvest hold, where "
           "fragments form, is not a parameter of the list assessed.",
           [("cqa", "Whether a parameter could change fragments is therefore outside this assessment."),
            ("cqa", "The harvest hold, where fragments form, is not a parameter of the list assessed here"),
            ("assumptions", "Fragments are outside this assessment, for the reasons given in")])
    nclaim("rk_harvest", "quality attribute at risk; designed experiment",
           "No parameter of harvest is scored against a quality attribute, and none is carried into a "
           "designed experiment.",
           [("rk_harvest", """Its `{python} ST["harvest"]["n"]` parameters are scored against process performance alone, and all of them sit at the floor of the ranking at `{python} rpn_min`."""),
            ("rk_harvest", "No parameter of this step is carried into a designed experiment."),
            ("rk_harvest", "The A-Mab case study assumes, for simplicity, that harvest has no impact on product quality")],
           rationale="The A-Mab case study assumes, for simplicity, that harvest has no impact on product quality.",
           uo=title["harvest"])
    nclaim("rk_protein_a", "leached Protein A", "No operating parameter of Protein A chromatography is scored "
           "against leached Protein A, although the attribute enters the process at this step.",
           [("rk_protein_a", "No operating parameter of this step is scored against leached Protein A, although the attribute enters the process here."),
            ("rk_protein_a", "Leached Protein A comes from the affinity ligand itself."),
            ("rk_protein_a", q_sop2008)],
           rationale="Leached Protein A comes from the affinity ligand itself; the assessment attributed the "
                     "amount released to the resin and its history of use, not to an operating parameter.",
           elsewhere="the resin life cycle procedure SOP-2008; the capture study measures leached Protein A "
                     "across its designed experiment",
           uo=title["protein_a"])
    nclaim("rk_viral_inactivation", "MVM clearance", "No parameter of low-pH viral inactivation is scored "
           "against MVM.",
           [("rk_viral_inactivation", "No parameter of this step is scored against MVM, because a parvovirus has no lipid envelope for low pH to disrupt (PCMP-001 §7.4).")],
           rationale="A parvovirus has no lipid envelope for low pH to disrupt.", uo=title["viral_inactivation"])
    nclaim("rk_cex", "quality attribute formed by the step", "Cation exchange chromatography forms no "
           "attribute of its own; it clears host cell protein, DNA and leached Protein A.",
           [("rk_cex", "It also clears host cell protein, DNA and leached Protein A, and it forms no attribute of its own.")],
           uo=title["cex"])
    nclaim("rk_virus_filtration", "parameter affecting process performance alone",
           "Small-virus retentive filtration has no parameter that affects process performance alone.",
           [("rk_virus_filtration", "The step has no parameter that affects process performance alone.")],
           uo=title["virus_filtration"])
    cor_ufdf = next(c for c in corrections if str(c[3]["Section"]) == "4.8")
    nclaim("rk_ufdf", "quality attribute formed or cleared by the step",
           "UF/DF forms and clears no attribute of the register; its parameters are scored against process "
           "performance alone.",
           [("rk_ufdf", "It forms and clears no attribute in"),
            ("rk_ufdf", """Its `{python} ST["ufdf"]["n"]` parameters are scored against process performance alone and sit at the floor of the ranking at `{python} rpn_min`."""),
            ("changes", ref("changes", cor_ufdf[2], cor_ufdf[0], cor_ufdf[1]))],
           rationale="Its final concentration is the drug substance concentration, which is measured and "
                     "released against a specification.", uo=title["ufdf"])
    nclaim("rk_ufdf", "characterization of UF/DF in the A-Mab case study",
           "The A-Mab case study gives no characterization of UF/DF, so the assessment of the step rests on "
           "platform experience alone.",
           [("rk_ufdf", "The A-Mab case study gives no characterization of this step"),
            ("rk_ufdf", "so the assessment rests on platform experience alone.")], uo=title["ufdf"])
    nclaim("assignment", "designed experiment at harvest and UF/DF",
           "No designed experiment is assigned to harvest or UF/DF, which have no parameter scored against a "
           "quality attribute.",
           [("assignment", "The remaining `{python} len(nodoe_steps)`, harvest and UF/DF, have no parameter scored against a quality attribute, and no designed experiment is assigned to them.")])
    nclaim("assignment", "exclusion from study on low risk",
           "No parameter is excluded from study on the ground that its risk is low.",
           [("assignment", "No parameter is excluded from study on the ground that its risk is low."),
            ("assignment", "Apart from the `{python} n_perf_doe` Protein A parameters carried into the capture design, they are studied one factor at a time, so that the ranges entered in the batch record rest on data and not on platform precedent alone.")])
    nclaim("assumptions", "parameters outside the transferred process description",
           "A parameter that is not in the process description transferred under PTP-001 is not assessed.",
           [("assumptions", "It is the list in the process description transferred under PTP-001, and a parameter that is not in that description is not assessed."),
            ("assumptions", "An equipment or facility difference at the receiving site that introduces a new parameter is handled under the transfer plan and requires this assessment to be revised.")],
           elsewhere="the transfer plan PTP-001, with a revision of this assessment")
    nclaim("assumptions", "likelihood of a failure",
           "A severity says nothing about how likely the process is to produce a failure.",
           [("assumptions", "That assessment scores impact and uncertainty and deliberately excludes manufacturing capability and detectability"),
            ("assumptions", "says nothing about how likely the process is to produce a failure.")],
           rationale="The quality attribute assessment that gives the severity scores impact and uncertainty "
                     "and excludes manufacturing capability and detectability.")
    nclaim("assumptions", "interaction of anion exchange residence time with the load chemistry",
           "No study as assigned can detect an interaction of residence time with load pH and conductivity at "
           "anion exchange.",
           [("assumptions", "No study as assigned can detect an interaction of residence time with load pH and conductivity."),
            ("assumptions", "The univariate result for flow rate therefore bounds the step only if that interaction is absent, as prior knowledge expects, and the anion exchange plan PCP-008 carries that justification.")],
           rationale="Operating flow rate is studied one factor at a time; prior knowledge expects no such "
                     "interaction.", elsewhere="PCP-008", uo=title["aex"])
    nclaim("assumptions", "interactions between unit operations", "Interactions between unit operations are "
           "not scored.",
           [("assumptions", "Interactions between unit operations are not scored."),
            ("assumptions", "That link is handled in the receiving step, where the pool is titrated to the set-point of inactivation pH, and not by a score in"),
            ("assumptions", "An attribute carried from one step to the next is judged against the intermediate acceptance criteria of PCMP-001 Version 2.0 §7.3, which carry each drug substance criterion back through the steps downstream.")],
           elsewhere="the receiving step; the intermediate acceptance criteria of PCMP-001 Version 2.0 §7.3")
    nclaim("assumptions", "measurement of A-Mab process behaviour",
           "No number in the document is a measurement of A-Mab process behaviour: the scores are judgements "
           "and the studies had not been run.",
           [("assumptions", "Finally, no number in this document is a measurement of A-Mab process behaviour."),
            ("assumptions", "The scores are judgements, the studies had not been run when the assessment was made, and the ranges in")])
    nclaim("assumptions", "proven acceptable ranges", "The ranges of the parameter set are ranges to be "
           "studied, not ranges shown to be acceptable.",
           [("assumptions", "are ranges to be studied and not ranges shown to be acceptable.")],
           elsewhere="the characterization report of each unit operation")
    nclaim("outputs", "change of a score or a study type at Version 2.0",
           "Version 2.0 changes no score and no study type; the method, the scores and the study assignment "
           "are those of Version 1.0.",
           [("outputs", "Version 2.0 changes no score and no study type"),
            ("changes", ref("changes", corrections[0][0].caption, caption=corrections[0][0].caption,
                            label=corrections[0][0].label)),
            ("approvals", "and confirms that the method, the scores and the study assignment are those of Version 1.0.")])

    # document relationships: the rows of the related-documents table, the title block, the plans
    # and reports of the scope table, and the documents the prose names
    rels = []

    def relation(kind, target, statement, refs):
        rels.append(DocumentRelationship(
            relationship_id=f"{DOC}-R{len(rels) + 1:02d}", kind=kind, source_document_id=DOC,
            target_document_ref=target, statement=statement, source_references=refs, metadata=meta()))

    for target, row in rel.items():
        txt = _cells(row)[-1]
        relation(G.PA5_REL_KIND.get(txt, "references"), target, txt,
                 [ref("purpose", row, rows=rel, caption=rel_cap, label="tbl-related")])
    relation("supersedes", f"{DOC} Version {P.REV1['rev']}", "Version 2.0 supersedes Version 1.0 of the "
             "assessment.", [ref("title", tb["Supersedes"], rows=tb)])
    relation("scoped_by", "PTP-001", "The Process Transfer Plan PTP-001 is the parent of the assessment: the "
             "parameters assessed are those of the process description it transfers.",
             [ref("purpose", q("The Process Transfer Plan PTP-001 is the parent of this assessment.")),
              ref("purpose", q("It moves the process from the development site in `{python} site_dev` to the commercial drug substance site in `{python} site_com`, and the parameters assessed here are those of the process description it transfers."))])
    relation("references", "SOP-4001", "Parameters are classified under the parameter classification "
             "procedure SOP-4001, in the characterization reports.", [ref("purpose", q(q_sop4001))])
    relation("references", "PCMR-001", "The classification of each parameter is reported in the "
             "characterization report of its unit operation and consolidated in PCMR-001.",
             [ref("purpose", q(q_pcmr_cls))])
    relation("references", ns["inv_id"], f"Version 2.0 of the assessment is issued under corrective action "
             f"CA3 of {ns['inv_id']}, whose finding 5 recorded the date the Version 1.0 title block carried.",
             [ref("changes", q("The QA investigation `{python} inv_id` recorded this as part of its finding 5, which concerns the dates in the Version 1.0 records.")),
              ref("changes", q("Its corrective action CA3 reissues the characterization reports, PTP-001, this assessment and PCMR-001 at Version 2.0.")),
              ref("changes", q("This assessment is reissued under it, effective `{python} eff2`."))])
    relation("references", ns["amd_id"], f"The analytical method decision of {ns['amd_date']} after which "
             f"PCMP-001 Version 2.0 §7.8 sets nrCE-SDS as the method for fragments.",
             [ref("changes", q_frag_method)])
    relation("references", "PCMP-001", "Where the assessment refers to acceptance criteria or to scale-down "
             "models, it refers to PCMP-001 Version 2.0.",
             [ref("changes", q("Where this document refers to acceptance criteria or to scale-down models, it refers to PCMP-001 Version 2.0."))])
    relation("references", "SOP-2008", "The resin and its history of use, to which the assessment "
             "attributes the amount of leached Protein A, are controlled under the resin life cycle "
             "procedure SOP-2008.", [ref("rk_protein_a", q(q_sop2008))])
    relation("references", "PCP-008", "The anion exchange plan PCP-008 records the justification of the "
             "univariate study of operating flow rate with the design.",
             [ref("rk_aex", q("The anion exchange plan PCP-008 records the justification with the design."))])
    for k in steps:
        plan, report = (x.strip() for x in str(sp_val[k]["Plan / report"]).split("/"))
        relation("references", plan, f"{plan} is the characterization plan of {title[k]} (Step {stepno[k]}), "
                 f"which takes up the study types and the ranges this assessment assigns to the step.",
                 [ref("assignment", sprow[k], sp_t, sprow)])
        relation("references", report, f"{report} is the characterization report of {title[k]} "
                 f"(Step {stepno[k]}).", [ref("assignment", sprow[k], sp_t, sprow)])
    relation("references", "PCMP-001", "PCMP-001 consumes the assessment at campaign level.",
             [ref("outputs", q("PCMP-001 consumes the assessment at campaign level."))])
    relation("references", "PCMR-001", "PCMR-001 consolidates the reports and is where the risk that remains "
             "after characterization is addressed.", [ref("outputs", q(q_pcmr_resid))])

    entities = [
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("purpose"), process_steps=process_steps,
                                  sites=sites, document_relationships=rels, non_claims=nc_at["purpose"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("changes"), analytical_methods=[method]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("method"), non_claims=nc_at["method"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cqa"), quality_attributes=attrs,
                                  non_claims=nc_at["cqa"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("ranking"), parameters=params),
    ] + [S.SectionEntityExtraction(document_id=DOC, section_id=_sid(f"rk_{k}"), non_claims=nc_at[f"rk_{k}"])
         for k in steps if f"rk_{k}" in nc_at] + [
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid(s_), non_claims=nc_at[s_])
        for s_ in ("assignment", "assumptions", "outputs")]

    # ==== assertions ==============================================================================
    A = []

    def add(subj, pred, obj, txt, refs):
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{DOC}-A{len(A) + 1:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=txt, source_references=refs, metadata=meta()))

    for k in steps:
        add("process:amab_ds", "process_has_step", f"step:{k}",
            f"The A-Mab drug substance process has the step {title[k]} (Step {stepno[k]}).",
            [ref("purpose", trrow[k], tr_t, trrow)])
    for key in pkeys:
        r = R[key]
        fm_t, fmrow = fm[key[0]]
        add(f"step:{key[0]}", "step_has_parameter", pid(key),
            f"{title[key[0]]} has process parameter {r['param']}, which this assessment assigns to "
            f"{r['study']}.",
            row_refs(f"rk_{key[0]}", fm_t, fmrow, key) + row_refs("ranking", rk_t, rkrow, key))
    for key in ckeys:
        g = reg.loc[key]
        add(f"step:{set_by[key]}", "step_has_quality_attribute", f"attr:{key}",
            (f"The register assigns the cumulative requirement {names[key]} to {g['Set by']}."
             if viral({"cqas": [key]}) else f"{names[key]} is formed or set at {g['Set by']}."),
            row_refs("cqa", cq_t, crow, key))
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{key}_ds",
            f"{names[key]} drug substance acceptance criterion: {g['Acceptance']}.",
            row_refs("cqa", cq_t, crow, key))
    add("attr:fragments_lmw", "attribute_measured_by_method", f"method:{frag_amv}",
        "Fragments are measured by nrCE-SDS, the method PCMP-001 Version 2.0 §7.8 sets for fragments after "
        "the analytical method decision; the criterion for fragments is stated on nrCE-SDS.",
        [ref("changes", q_frag_method)] + row_refs("cqa", cq_t, crow, "fragments_lmw"))

    # parameter -> attribute at risk: every relation of a failure-mode row, anchored on that row and on
    # the sentences of the step's subsection that name the parameter and the attribute together.
    #: (section, .qmd source of the span, the (step, parameter, attribute) relations it names)
    QREL = [
        ("rk_bioreactor", "A culture pH above its range is expected to raise high mannose and to lower galactosylation.",
         [("bioreactor", "pH", "high_mannose"), ("bioreactor", "pH", "galactosylation")]),
        ("rk_bioreactor", "Aggregate in the harvest is expected to rise with culture pH and afucosylation to fall.",
         [("bioreactor", "pH", "aggregates_hmw"), ("bioreactor", "pH", "afucosylation")]),
        ("rk_bioreactor", "Acidic variants are expected to rise with culture pH, because the deamidation of asparagine residues is catalysed by base.",
         [("bioreactor", "pH", "acidic_variants")]),
        ("rk_bioreactor", "A longer culture, or one harvested after viability has fallen, is expected to raise host cell protein and DNA in the harvest, because lysing cells release their protein and DNA into the medium.",
         [("bioreactor", "duration", "hcp"), ("bioreactor", "duration", "residual_dna")]),
        ("rk_bioreactor", "Aggregate is expected to rise with duration too, since antibody secreted early in the run is held at culture temperature until harvest.",
         [("bioreactor", "duration", "aggregates_hmw")]),
        ("rk_bioreactor", "Galactosylation is expected to fall late in the culture as the supply of UDP-galactose to the galactosyltransferase runs down.",
         [("bioreactor", "duration", "galactosylation")]),
        ("rk_bioreactor", "Afucosylation is expected to fall with duration as well, and the study has to bound that fall against the lower limit of the afucosylation criterion.",
         [("bioreactor", "duration", "afucosylation")]),
        ("rk_bioreactor", "Galactosylation is expected to rise with culture temperature, which raises the activity of the galactosyltransferase, and to fall as pCO2 and osmolality rise.",
         [("bioreactor", "temperature", "galactosylation"), ("bioreactor", "co2", "galactosylation"),
          ("bioreactor", "osmolality", "galactosylation")]),
        ("rk_bioreactor", "and temperature is also scored against afucosylation",
         [("bioreactor", "temperature", "afucosylation")]),
        ("rk_bioreactor", "Culture temperature, pCO2 and osmolality are each scored against galactosylation and acidic variants",
         [("bioreactor", "temperature", "acidic_variants"), ("bioreactor", "co2", "acidic_variants"),
          ("bioreactor", "osmolality", "acidic_variants")]),
        ("rk_protein_a", "Protein load and elution buffer pH are the `{python} len(pa_q)` parameters scored against a quality attribute, both against host cell protein at a severity of `{python} sev_pa`.",
         [("protein_a", "load", "hcp"), ("protein_a", "elution_ph", "hcp")]),
        ("rk_protein_a", "A protein load above its range is expected to raise host cell protein per milligram of antibody in the pool, because host cell protein that binds to the captured antibody is not removed by the wash, and more of it is expected to be bound per milligram of antibody on a more heavily loaded column.",
         [("protein_a", "load", "hcp")]),
        ("rk_protein_a", "A lower elution pH is expected to raise it as well, since a more acidic elution buffer releases host cell protein that the wash left bound to the resin.",
         [("protein_a", "elution_ph", "hcp")]),
        ("rk_viral_inactivation", "A pH above its range lowers the rate constant and leaves less virus inactivated in the same hold.",
         [("viral_inactivation", "ph", "lrv_xmulv")]),
        ("rk_viral_inactivation", "A hold shorter than its range leaves less virus inactivated at the same pH.",
         [("viral_inactivation", "hold_time", "lrv_xmulv")]),
        ("rk_viral_inactivation", "A temperature below its range lowers the rate constant too, and this matters most at the short end of the hold and the high end of the pH range, where the log reduction reached is smallest.",
         [("viral_inactivation", "temperature", "lrv_xmulv")]),
        ("rk_viral_inactivation", "A pH below its range exposes the antibody to conditions under which aggregation and precipitation have been seen on the platform.",
         [("viral_inactivation", "ph", "aggregates_hmw")]),
        ("rk_viral_inactivation", "A hold longer than its range is expected, from platform experience, to raise aggregate at any pH in the range.",
         [("viral_inactivation", "hold_time", "aggregates_hmw")]),
        ("rk_viral_inactivation", "Inactivation pH and hold time are therefore scored against aggregate as well.",
         [("viral_inactivation", "ph", "aggregates_hmw"), ("viral_inactivation", "hold_time", "aggregates_hmw")]),
        ("rk_cex", "Protein load, elution buffer pH and elution stop collect are scored against aggregate at a severity of `{python} sev_agg`",
         [("cex", "load", "aggregates_hmw"), ("cex", "elution_ph", "aggregates_hmw"),
          ("cex", "stop_collect", "aggregates_hmw")]),
        ("rk_cex", "and protein load is scored against host cell protein as well",
         [("cex", "load", "hcp")]),
        ("rk_cex", "Pool aggregate is expected to rise with protein load, elution buffer pH and elution stop collect.",
         [("cex", "load", "aggregates_hmw"), ("cex", "elution_ph", "aggregates_hmw"),
          ("cex", "stop_collect", "aggregates_hmw")]),
        ("rk_cex", "Aggregate elutes after the monomer, so collecting further down the tail of the elution peak takes more of it into the pool.",
         [("cex", "stop_collect", "aggregates_hmw")]),
        ("rk_cex", "A higher load leaves less resin per gram of antibody to separate the two.",
         [("cex", "load", "aggregates_hmw")]),
        ("rk_cex", "The conductivity of the load and wash is scored against host cell protein.",
         [("cex", "wash_cond", "hcp")]),
        ("rk_cex", "A conductivity below its range weakens the wash and leaves more host cell protein bound, to be eluted with the product.",
         [("cex", "wash_cond", "hcp")]),
        ("rk_aex", "It sets the charge on the impurities and on the virus, so a load pH below its range weakens the binding of host cell protein and of both model viruses at once.",
         [("aex", "load_ph", "hcp"), ("aex", "load_ph", "lrv_xmulv"), ("aex", "load_ph", "lrv_mvm")]),
        ("rk_aex", "Clearance is also expected to fall as load conductivity rises, because the counter-ions in the load compete with virus and impurity for the charged groups of the resin.",
         [("aex", "load_cond", "lrv_xmulv"), ("aex", "load_cond", "lrv_mvm")]),
        ("rk_aex", "The conductivity of the equilibration and wash-1 buffers and the protein load are scored against host cell protein.",
         [("aex", "wash1_cond", "hcp"), ("aex", "load", "hcp")]),
        ("rk_aex", "A higher wash conductivity weakens the binding of host cell protein in the same way.",
         [("aex", "wash1_cond", "hcp")]),
        ("rk_aex", "A higher protein load presents more impurity to a fixed volume of resin, so its binding capacity can be exceeded.",
         [("aex", "load", "hcp")]),
        ("rk_aex", "A higher flow rate shortens the residence time of the load in the bed, which gives a virus particle less time to reach and bind a charged site on the resin.",
         [("aex", "flow", "lrv_xmulv"), ("aex", "flow", "lrv_mvm")]),
        ("rk_virus_filtration", "Both of its parameters are scored against MVM clearance, and both reach `{python} rpn_max`.",
         [("virus_filtration", "filtration_volume", "lrv_mvm"), ("virus_filtration", "pressure", "lrv_mvm")]),
        ("rk_virus_filtration", "The log reduction is expected to fall as the volume filtered per unit area rises, because the retentive layer accumulates material and the chance of a parvovirus passing rises with it.",
         [("virus_filtration", "filtration_volume", "lrv_mvm")]),
        ("rk_virus_filtration", "Filtration pressure is scored against both model viruses, and it sets the driving force across that accumulating layer.",
         [("virus_filtration", "pressure", "lrv_mvm"), ("virus_filtration", "pressure", "lrv_xmulv")]),
        ("rk_virus_filtration", "Parvovirus filters of this kind can retain less virus at low pressure or low flux and after a pressure interruption, so the direction of a pressure effect on the log reduction is known.",
         [("virus_filtration", "pressure", "lrv_mvm")]),
    ]
    #: Performance-only parameters: the sentences that name what each puts at risk.
    PREL = [
        ("rk_bioreactor", "Initial viable cell concentration, basal medium concentration and nutrient feed-1 volume each raise the integral of viable cell concentration over their ranges, and titre rises with it.",
         [("bioreactor", "ivcc"), ("bioreactor", "medium_conc"), ("bioreactor", "feed_vol")]),
        ("rk_bioreactor", "Dissolved oxygen acts on peak viable cell density, titre and process consistency.",
         [("bioreactor", "do")]),
        ("rk_harvest", "A centrifugal force below its range leaves more cells and cell debris in the centrate.",
         [("harvest", "centrifuge_g")]),
        ("rk_harvest", "A depth filter loaded beyond its capacity passes particulate instead of retaining it, and the turbidity of the clarified harvest rises.",
         [("harvest", "depth_filter_load")]),
        ("rk_harvest", "Turbidity is measured on the clarified harvest, and particulate that reaches the capture column raises its back pressure.",
         [("harvest", "turbidity")]),
        ("rk_protein_a", "Load flow rate and end of pool collect are scored against step yield and against no quality attribute.",
         [("protein_a", "flow"), ("protein_a", "end_collect")]),
        ("rk_protein_a", "Yield is expected to fall when a high load is run at a high flow rate, because the antibody has less time to diffuse into the resin pores and part of it passes through the column unbound.",
         [("protein_a", "flow")]),
        ("rk_protein_a", "Yield is expected to rise as collection is carried further down the tail of the elution peak, up to the point where the pool is diluted without gaining product.",
         [("protein_a", "end_collect")]),
        ("rk_viral_inactivation", "A-Mab concentration is scored against process performance.",
         [("viral_inactivation", "protein_conc")]),
        ("rk_cex", "Elution flow rate is scored against step yield.", [("cex", "flow")]),
        ("rk_cex", "A higher elution flow rate broadens the elution peak, because the antibody has less time to diffuse out of the resin pores, and a broader peak dilutes the pool.",
         [("cex", "flow")]),
        ("rk_ufdf", "A number of diavolumes below its range leaves the buffer exchange incomplete.",
         [("ufdf", "diavolumes")]),
        ("rk_ufdf", "Beyond that point the concentration polarization layer at the membrane surface thickens and flux stops rising, so a transmembrane pressure outside its range is expected to change the processing time.",
         [("ufdf", "tmp")]),
        ("rk_ufdf", "The final concentration is the drug substance concentration itself, which is measured and released against a specification.",
         [("ufdf", "final_conc")]),
    ]
    #: What prior knowledge places no effect on, for a parameter scored on process performance, with the
    #: wording of the assertion (the document's own verb for each: "showed no effect", "places no effect").
    NREL = [
        ("rk_viral_inactivation", "Prior product experience showed no effect of concentration on the rate of inactivation, on aggregation or on charge variants over the range the pool reaches.",
         [("viral_inactivation", "protein_conc", "lrv_xmulv"), ("viral_inactivation", "protein_conc", "aggregates_hmw"),
          ("viral_inactivation", "protein_conc", "acidic_variants")],
         "Prior product experience showed no effect of {param} at the {step} step on {attr} (on the rate of "
         "inactivation, on aggregation or on charge variants) over the range the pool reaches; the parameter is "
         "scored against process performance."),
        ("rk_cex", "Prior knowledge places no effect of flow rate on pool aggregate large enough to score, so the parameter is studied one factor at a time.",
         [("cex", "flow", "aggregates_hmw")],
         "Prior knowledge places no effect of {param} at the {step} step on {attr} in the pool large enough to "
         "score; the parameter is scored against process performance and studied one factor at a time."),
    ]
    qspans, pspans, nspans = {}, {}, {}
    for sec, src, rel_ in QREL:
        for k, p, a in rel_:
            if a not in R[(k, p)]["cqas"]:
                raise ValueError(f"{DOC}: {src[:50]!r} names {k}/{p} -> {a}, which the register does not score")
            qspans.setdefault((k, p, a), []).append(ref(sec, q(src)))
    for sec, src, rel_ in PREL:
        for k, p in rel_:
            if R[(k, p)]["quality"]:
                raise ValueError(f"{DOC}: {k}/{p} is scored against a quality attribute")
            pspans.setdefault((k, p), []).append(ref(sec, q(src)))
    n_txt = {}
    for sec, src, rel_, wording in NREL:
        for k, p, a in rel_:
            if R[(k, p)]["quality"] or a in R[(k, p)]["cqas"]:
                raise ValueError(f"{DOC}: {k}/{p} -> {a} is not a non-impact of a performance parameter")
            nspans.setdefault((k, p, a), []).append(ref(sec, q(src)))
            n_txt[(k, p, a)] = wording.format(param=lc(R[(k, p)]["param"]), step=mid[k], attr=names[a])
    for key in pkeys:
        r = R[key]
        fm_t, fmrow = fm[key[0]]
        on_row = row_refs(f"rk_{key[0]}", fm_t, fmrow, key)
        if r["quality"]:
            for a in r["cqas"]:
                add(pid(key), "parameter_impacts_attribute", f"attr:{a}",
                    f"{r['param']} at the {mid[key[0]]} step is scored against {names[a]}: its potential "
                    f"failure mode could affect the attribute. A prospective (pre-characterization) relation; "
                    f"the size of the effect is not yet measured.",
                    on_row + qspans.get((*key, a), []))
        else:
            add(pid(key), "parameter_impacts_attribute", "attr:process_performance",
                f"{r['param']} at the {mid[key[0]]} step is scored against process performance alone: its "
                f"potential failure mode could affect process performance, and it puts no quality attribute "
                f"at risk. A prospective (pre-characterization) relation.",
                on_row + pspans.get(key, []))
    for (k, p, a), refs in nspans.items():
        add(pid((k, p)), "parameter_does_not_significantly_impact_attribute", f"attr:{a}", n_txt[(k, p, a)],
            row_refs(f"rk_{k}", *fm[k], (k, p)) + refs)
    unused = (set(qspans) - {(*key, a) for key in pkeys for a in R[key]["cqas"]}) | (set(pspans) - set(pkeys))
    if unused:
        raise ValueError(f"{DOC}: prose spans keyed to relations the register does not hold: {sorted(unused)}")

    # ==== statements ==============================================================================
    ST = []

    def st(sec, txt, refs):
        ST.append((SEC[sec][0], ReportStatement(
            statement_id=f"{DOC}-S{len(ST) + 1:03d}", statement_text=txt, confidence="high",
            review_status="accepted", source_references=refs)))

    def sq(sec, src, txt=None, extra=()):
        """A statement of one prose span: ``src`` is the .qmd source of the span, ``txt`` the statement
        (the span itself where it reads on its own). ``extra`` cites further ``(section, source)``
        spans a paraphrase draws on."""
        st(sec, t(txt) if txt else q(src), [ref(sec, q(src))] + [ref(s_, q(x)) for s_, x in extra])

    # Purpose and scope
    sq("purpose", "This document records the risk assessment made on the A-Mab drug substance process before any characterization study began.",
       "RA-001 records the risk assessment made on the A-Mab drug substance process before any characterization study began.")
    sq("purpose", "Its output is the scope of the characterization campaign.",
       "The output of the assessment is the scope of the characterization campaign.")
    sq("purpose", "For each process parameter it names the quality attributes the parameter could affect, the potential failure mode and its effect, an initial risk score and the type of study assigned to the parameter.",
       "For each process parameter the assessment names the quality attributes the parameter could affect, the potential failure mode and its effect, an initial risk score and the type of study assigned to the parameter.")
    sq("purpose", "The assessment is prospective and reports no study result.")
    sq("purpose", "A parameter is classified as a critical process parameter (CPP), a well-controlled critical process parameter (WC-CPP), a key process parameter (KPP) or a general process parameter (GPP) from the effects that the characterization studies measure.")
    sq("purpose", "The scores in this document are initial scores in the same sense.",
       "The scores in RA-001 are initial scores, made before any effect was measured; the risk that remains once the studies have reported is a separate assessment, which RA-001 does not anticipate.",
       extra=[("purpose", "The risk that remains once the studies have reported is a separate assessment, and nothing in this document anticipates it.")])
    sq("purpose", "The scope is the drug substance process from the production bioreactor to formulation.")
    sq("purpose", "lists the `{python} n_steps` unit operations and the principal role of each, and the assessment covers their `{python} n_par` process parameters.",
       "The assessment covers the `{python} n_par` process parameters of the `{python} n_steps` unit operations of the drug substance train.")
    st("purpose", t("The Process Transfer Plan PTP-001 is the parent of the assessment; it moves the process from "
                    "the development site in `{python} site_dev` to the commercial drug substance site in "
                    "`{python} site_com`."),
       [ref("purpose", q("The Process Transfer Plan PTP-001 is the parent of this assessment.")),
        ref("purpose", q("It moves the process from the development site in `{python} site_dev` to the commercial drug substance site in `{python} site_com`, and the parameters assessed here are those of the process description it transfers."))])
    sq("purpose", "The consumers of the assessment are the characterization plans PCP-003 to PCP-010, one for each unit operation.",
       extra=[("purpose", "Each plan takes the study type assigned here and sets out how the study is run.")])
    sq("purpose", "In this framework risk assessment is a lifecycle activity, not a single exercise",
       "Risk assessment is a lifecycle activity, not a single exercise, and RA-001 is the first assessment in that lifecycle.",
       extra=[("purpose", "This assessment is the first in that lifecycle.")])
    sq("purpose", "It draws on prior knowledge alone, because no A-Mab characterization data existed when it was made.",
       "The assessment draws on prior knowledge alone, because no A-Mab characterization data existed when it was made.")
    sq("purpose", "It is revisited when the characterization reports are available, and again once commercial experience has been gained.",
       "The assessment is revisited when the characterization reports are available, and again once commercial experience has been gained.")
    sq("purpose", "The approach follows the enhanced development approach of ICH Q8 and ICH Q11",
       "The approach follows the enhanced development approach of ICH Q8 and ICH Q11 and supports Stage 1 of the process validation lifecycle.",
       extra=[("purpose", "and supports Stage 1 of the process validation lifecycle")])
    # Changes in this revision
    sq("changes", "Version 1.0 of this assessment was approved on `{python} appr_v1`.",
       "Version 1.0 of RA-001 was approved on `{python} appr_v1`.")
    sq("changes", "That date falls after the approval of PTP-001 on `{python} appr_ptp` and before the approval of the Process Characterization Master Plan PCMP-001 on `{python} appr_pcmp`.",
       "The approval of Version 1.0 of RA-001 falls after the approval of PTP-001 on `{python} appr_ptp` and before the approval of the Process Characterization Master Plan PCMP-001 on `{python} appr_pcmp`.")
    st("changes", t("The first characterization study, `{python} first_id`, the qualification runs of the "
                    "production bioreactor scale-down model, started on `{python} first_start`, and every study "
                    "of the campaign started after the assessment was approved."),
       [ref("changes", q_first),
        ref("changes", q("Every study of the campaign started after this assessment was approved."))])
    sq("changes", "When the Version 1.0 package was compiled, the title block of this assessment carried `{python} v1_block`, the date of the compilation and of the approval of the Version 1.0 reports, in place of its own approval date.",
       "When the Version 1.0 package was compiled, the title block of RA-001 carried `{python} v1_block`, the date of the compilation and of the approval of the Version 1.0 reports, in place of its own approval date.")
    sq("changes", "QA opened the investigation on `{python} inv_open`, after its review of PCMR-001 Version 1.0 for readiness for the Biologics License Application (BLA), and closed it on `{python} inv_close`.",
       "QA opened `{python} inv_id` on `{python} inv_open`, after its review of PCMR-001 Version 1.0 for readiness for the Biologics License Application (BLA), and closed it on `{python} inv_close`.")
    sq("changes", "It records the approval date of Version 1.0 in the title block and in the revision history, and this section records the date on which the first characterization study started.",
       "Change 1: Version 2.0 records the approval date of Version 1.0 in the title block and in the revision history, and the date on which the first characterization study started.")
    sq("changes", "It gives the quality attribute register as it now stands",
       "Change 2: Version 2.0 gives the quality attribute register as it now stands, which adds fragments, the low molecular weight species formed when the antibody is clipped.",
       extra=[("changes", "The register adds fragments, the low molecular weight species formed when the antibody is clipped.")])
    sq("changes", "The register also prints each criterion by its type, as a lower limit, an upper limit or a range.",
       extra=[("changes", "Version 1.0 printed both ends of every criterion, so that viral clearance read as if it had an upper limit.")])
    sq("changes", "That plan qualifies each scale-down model by its offset from manufacturing scale (PCMP-001 §7.1).",
       "Change 3: where RA-001 refers to scale-down models it refers to PCMP-001 Version 2.0, which qualifies each scale-down model by its offset from manufacturing scale (PCMP-001 §7.1).")
    sq("changes", "It judges each step output on which a drug substance criterion depends against an intermediate acceptance criterion (PCMP-001 §7.3).",
       "PCMP-001 Version 2.0 judges each step output on which a drug substance criterion depends against an intermediate acceptance criterion (PCMP-001 §7.3).")
    sq("changes", "It corrects the descriptions of Version 1.0 that were wrong",
       "Change 4: Version 2.0 corrects the descriptions of Version 1.0 that were wrong; no score and no study type changes with them.")
    for tab, rr, row, x in corrections:
        st("changes", f"Description of Version 1.0 corrected at Version 2.0 (section {x['Section']}). Version 1.0: "
                      f"{x['Version 1.0']} Version 2.0: {x['Version 2.0']}", [ref("changes", row, tab, rr)])
    sq("changes", "They are those approved on `{python} appr_v1`, before the studies.",
       "The method, the scores, the ranking and the study assignment of RA-001 are unchanged at Version 2.0: they are those approved on `{python} appr_v1`, before the studies.")
    # Risk assessment methodology
    sq("method", "The method is risk ranking and filtering, applied to process parameters as in the A-Mab case study",
       "The method is risk ranking and filtering, applied to process parameters as in the A-Mab case study and within the quality risk management principles of ICH Q9.",
       extra=[("method", "and within the quality risk management principles of ICH Q9")])
    sq("method", "The first asks what the parameter could do to a quality attribute, or to process performance, if it moved outside the range over which the process is currently understood.",
       "Each parameter is put to two questions; the first asks what the parameter could do to a quality attribute, or to process performance, if it moved outside the range over which the process is currently understood, and it sets the score.",
       extra=[("method", "Each parameter is put to two questions."), ("method", "The first question sets the score.")])
    sq("method", "The second asks whether the effect of the parameter could depend on the setting of another parameter of the same unit operation.",
       "The second question asks whether the effect of the parameter could depend on the setting of another parameter of the same unit operation, and it sets the study type, because an effect that depends on a second parameter cannot be found by moving one parameter at a time.",
       extra=[("method", "The second sets the study type, because an effect that depends on a second parameter cannot be found by moving one parameter at a time.")])
    sq("method", "Severity is taken from the attribute at risk and not from the parameter.")
    sq("method", "It runs from `{python} sev_reg_min` to `{python} sev_reg_max` and is the severity assigned to the attribute in the quality attribute assessment, reproduced in",
       "Severity runs from `{python} sev_reg_min` to `{python} sev_reg_max` and is the severity assigned to the attribute in the quality attribute assessment.")
    sq("method", "Where a parameter could affect more than one attribute, the severity of the most severe of them is used.")
    sq("method", "A parameter that puts no quality attribute at risk takes a severity of `{python} sev_perf`, the value assigned to a process attribute such as step yield or titre.")
    sq("method", "Occurrence and detection are assigned before any effect has been measured, and they are assigned by class and not parameter by parameter.")
    for (score, cls), row in scrow.items():
        x = sc_df[(sc_df["Score"] == score) & (sc_df["Parameter class"] == cls)].iloc[0]
        st("method", f"{score} for the class '{cls}': {x['Value']}. Basis: {x['Basis']}.",
           [ref("method", row, sc_t, scrow)])
    sq("method", "The initial risk priority number (RPN) is the product of severity, occurrence and detection.")
    sq("method", "Across the assessment it runs from `{python} rpn_min` to `{python} rpn_max` and takes `{python} n_rpn` distinct values, because occurrence and detection are assigned by class.",
       "Across the assessment the initial RPN runs from `{python} rpn_min` to `{python} rpn_max` and takes `{python} n_rpn` distinct values, because occurrence and detection are assigned by class.")
    sq("method", "Within a class of parameter the RPN therefore differs only through severity.")
    sq("method", "Priority is High where an attribute of severity `{python} sev_hi` or above is at risk, Medium where a quality attribute of lower severity is at risk, and Low where only process performance is at risk.")
    sq("method", "No parameter is assigned a study type on its RPN alone.")
    sq("method", "The assessment uses `{python} n_types` study types.",
       "The assessment uses `{python} n_types` study types: " + P.join_and(ns["study_types"]) + ".",
       extra=[("method", "A parameter carried into the designed experiment of its unit operation is studied multivariately, which is the only way to estimate an effect that depends on a second parameter.")])
    sq("method", "A parameter that could affect a quality attribute but is not carried into the design is studied one factor at a time, and the reason it was left out of the design is recorded with it.",
       extra=[("method", "The A-Mab risk ranking and filtering approach permits this substitution where the study can be justified")])
    sq("method", "A parameter that puts no quality attribute at risk is studied one factor at a time unless it is carried into the design of its step",
       "A parameter that puts no quality attribute at risk is studied one factor at a time unless it is carried into the design of its step.")
    sq("method", "Each characterization plan states how the assigned study is executed.")
    sq("method", "Criticality is treated as a continuum and not as a binary split",
       "Criticality is treated as a continuum and not as a binary split.")
    # Quality attributes at risk
    sq("cqa", "The severity axis of the assessment comes from the quality attribute register.")
    sq("cqa", "gives the `{python} n_cqa` attributes of the drug substance as the register now stands.",
       "The register now holds `{python} n_cqa` attributes of the drug substance.",
       extra=[("cqa", "For each attribute it gives the acceptance criterion, the criticality, the severity carried into this assessment and the unit operation that forms the attribute.")])
    sq("cqa", "For the two cumulative viral clearance requirements it gives the unit operation to which the register assigns the requirement.")
    sq("cqa", "The criteria are those of the A-Mab case study, except the criterion for fragments",
       "The acceptance criteria are those of the A-Mab case study, except the criterion for fragments.")
    sq("cqa", "Criticality is the product of impact and uncertainty, which is Tool #1 of the A-Mab attribute assessment.")
    sq("cqa", "Attributes of high and very high criticality are called critical, and `{python} n_crit` of the `{python} n_cqa` attributes are critical on that definition.")
    sq("cqa", vir_rule)
    for key in ckeys:
        g = reg.loc[key]
        sev = g["Severity"]
        scored = not (isinstance(sev, float) and math.isnan(sev))
        st("cqa", (f"The severity carried into the assessment for {names[key]} is {int(sev)}." if scored else
                   f"{names[key]} carry no severity: the attribute joined the register after the assessment "
                   f"was made and was not scored."), row_refs("cqa", cq_t, crow, key))
    dose_i = [n.split(" ", 1)[1].startswith("Per dose") for n in cq_notes].index(True)
    dose = ns["DOSE"]
    st("cqa", f"The residual DNA criterion is per dose of {float(dose['mg_per_kg']):g} mg/kg, the dose of the A-Mab "
              f"case study, for a reference adult of {float(dose['body_weight_kg']):g} kg, which is "
              f"{ns['DOSE_MG']:g} mg of antibody; the body weight is an assumption.",
       [ref("cqa", cq_notes[dose_i], cq_t)] + row_refs("cqa", cq_t, crow, "residual_dna"))
    sq("cqa", "Of the `{python} n_cqa` attributes, `{python} n_bio` are formed in the production bioreactor.")
    sq("cqa", "The register assigns fragments to harvest, leached Protein A enters the process at the capture step, and each viral clearance requirement is assigned to one of the steps that clear virus.")
    sq("cqa", "The highest severity, `{python} sev_reg_max`, is carried by `{python} n_top_attr` attributes.",
       extra=[("cqa", "Both viral clearance attributes carry the highest severity for a different reason.")])
    sq("cqa", "The impact of the attribute is therefore scored on efficacy.",
       "The impact of high mannose is scored on efficacy, because high mannose glycans are expected to raise ADCC in the same way as afucosylation and A-Mab acts on its target through ADCC.",
       extra=[("cqa", "High mannose glycans carry no core fucose, so they are expected to raise antibody dependent cellular cytotoxicity (ADCC) in the same way as afucosylation, and A-Mab acts on its target through ADCC.")])
    sq("cqa", "Its uncertainty is scored above that of afucosylation, because the link rests on published literature and not on assays run with A-Mab.",
       "The uncertainty of high mannose is scored above that of afucosylation, because the link rests on published literature and not on assays run with A-Mab.")
    sq("cqa", "Each requirement is cumulative across the steps that clear the virus, which are low-pH viral inactivation, anion exchange and virus filtration for XMuLV, and anion exchange and virus filtration for MVM.")
    sq("cqa", "The register assigns each requirement to one step, and the claims of these steps add up to it (PCMP-001 §7.4).")
    sq("cqa", "A shortfall at one of these steps changes no property of the drug substance that a release test measures",
       "A shortfall in viral clearance at one of these steps changes no property of the drug substance that a release test measures; that enters the detection score, not the severity.",
       extra=[("cqa", "That no release test detects a shortfall enters the detection score")])
    sq("cqa", "The assessment still scores `{python} n_acid_par` bioreactor parameters against acidic variants.",
       extra=[("cqa", "The range of each parameter over which acidic variants stay within their criterion is one of the things the bioreactor study must establish.")])
    sq("cqa", "A low severity lowers the priority of a parameter and does not remove it from study.")
    sq("cqa", "Fragments are new to the register at Version 2.0.")
    sq("cqa", "The register assigns fragments to harvest, because proteases released from lysed cells clip the antibody in culture and during the harvest hold.")
    sq("cqa", "No parameter is scored against fragments and no severity is assigned to them.",
       "No parameter is scored against fragments and no severity is assigned to them, because the assessment was made before fragments joined the register.",
       extra=[("cqa", "This assessment was made before fragments joined the register.")])
    # Parameter risk ranking by unit operation
    sq("ranking", "Of the `{python} n_par` parameters, `{python} n_q` are scored against at least one quality attribute and `{python} n_perf` against process performance alone.")
    sq("ranking", "The ranking puts `{python} n_high` parameters at High priority, `{python} n_med` at Medium and `{python} n_low` at Low.")
    sq("ranking", "The highest RPN, `{python} rpn_max`, is reached by `{python} n_top` parameters, all of them at the steps with a viral clearance claim and all of them scored against viral clearance.")
    for key in pkeys:
        x = ct["tbl-ranking"][1].iloc[pkeys.index(key)]
        st("ranking", f"{x['Parameter']} ({title[key[0]]}, Step {stepno[key[0]]}): severity {x['Sev.']}, initial "
                      f"RPN {x['Init. RPN']}, study type {x['Study type']}, priority {x['Priority']}.",
           row_refs("ranking", rk_t, rkrow, key))
    for key in pkeys:
        r = R[key]
        fm_t, fmrow = fm[key[0]]
        st(f"rk_{key[0]}", f"{r['param']} ({title[key[0]]}): potential failure mode '{r['fm']}', with the "
                           f"potential effect '{r['eff']}'; attribute(s) at risk: {r['cqa_label']}.",
           row_refs(f"rk_{key[0]}", fm_t, fmrow, key))
    # production bioreactor
    sq("rk_bioreactor", """Of its `{python} ST["bioreactor"]["n"]` parameters, `{python} ST["bioreactor"]["nq"]` are scored against a quality attribute, all of them at a severity of `{python} sev_hi` or above.""",
       """Of the `{python} ST["bioreactor"]["n"]` parameters of the production bioreactor, `{python} ST["bioreactor"]["nq"]` are scored against a quality attribute, all of them at a severity of `{python} sev_hi` or above.""")
    sq("rk_bioreactor", """Culture pH is the only parameter outside the steps with a viral clearance claim that has a severity of `{python} sev_reg_max`, and it has the highest RPN in the step, `{python} ST["bioreactor"]["rpn_max"]`.""")
    sq("rk_bioreactor", "Culture pH and culture duration are each scored against `{python} n_attr_max` attributes, more than any other parameter in the assessment.")
    sq("rk_bioreactor", "Culture pH takes a severity of `{python} sev_bph` because high mannose is one of the attributes it puts at risk.")
    sq("rk_bioreactor", "A higher pH in the medium raises the pH in the Golgi, while the mannosidases and the galactosyltransferase work fastest under more acidic conditions.",
       "A higher culture pH raises the pH in the Golgi, while the mannosidases and the galactosyltransferase work fastest under more acidic conditions, so less mannose is trimmed from the glycans and less galactose is added to them.",
       extra=[("rk_bioreactor", "Less mannose is then trimmed from the glycans and less galactose is added to them.")])
    sq("rk_bioreactor", "Temperature is expected to act together with pH on the glycan attributes, because both act on the activity of the same glycan processing enzymes, the mannosidases and the galactosyltransferase.",
       "Culture temperature is expected to act together with culture pH on the glycan attributes, because both act on the activity of the same glycan processing enzymes, the mannosidases and the galactosyltransferase.",
       extra=[("rk_bioreactor", "An effect of that kind is estimated only by moving the two parameters together.")])
    sq("rk_bioreactor", "The `{python} len(bq)` parameters scored against a glycan, charge variant or aggregate attribute are therefore carried into one designed experiment.",
       "The `{python} len(bq)` bioreactor parameters scored against a glycan, charge variant or aggregate attribute are carried into one designed experiment.")
    sq("rk_bioreactor", """The other `{python} ST["bioreactor"]["nperf"]` parameters change how many cells the culture reaches and how much antibody each cell makes, and none of them is scored against a quality attribute.""",
       """The other `{python} ST["bioreactor"]["nperf"]` bioreactor parameters change how many cells the culture reaches and how much antibody each cell makes, and none of them is scored against a quality attribute.""")
    sq("rk_bioreactor", "Platform experience shows a statistically significant but shallow effect on afucosylation, too small to move the attribute across its criterion over the concentrations the process uses.",
       "Basal medium concentration has a statistically significant but shallow effect on afucosylation in platform experience, too small to move the attribute across its criterion, so it is scored on process performance and studied one factor at a time.",
       extra=[("rk_bioreactor", "The parameter is therefore scored on process performance and studied one factor at a time.")])
    sq("rk_bioreactor", "Nutrient feed-1 volume is treated in the same way, since platform experience shows only a slight effect on galactosylation.")
    # harvest
    sq("rk_harvest", "The failure modes are a centrifugal force outside its range, a depth filter loaded beyond its capacity and a high turbidity after clarification.",
       "The failure modes of harvest are a centrifugal force outside its range, a depth filter loaded beyond its capacity and a high turbidity after clarification.")
    sq("rk_harvest", "A particle settles faster the stronger the field acting on it, so a weaker field removes less of the fine debris in the time the material spends in the bowl.",
       extra=[("rk_harvest", "That debris then loads the depth filters.")])
    sq("rk_harvest", "A failure at this step is therefore seen before the batch is released.",
       "A failure at harvest is seen before the batch is released.")
    # Protein A
    sq("rk_protein_a", "The two parameters are expected to act together, and both are carried into the capture design.",
       "Protein load and elution buffer pH are expected to act together, and both are carried into the capture design.")
    sq("rk_protein_a", "Elution buffer pH therefore sets the pH of the pool before titration and the amount of acid needed to bring it to the hold set-point.",
       "The capture eluate is the load of the low-pH hold, so elution buffer pH sets the pH of the pool before titration and the amount of acid needed to bring it to the hold set-point.",
       extra=[("rk_protein_a", "The capture eluate is the load of the low-pH hold.")])
    sq("rk_protein_a", "Both parameters are carried into the capture design, so that the same design bounds step yield.",
       "Load flow rate and end of pool collect are carried into the capture design, so that the same design bounds step yield.")
    sq("rk_protein_a", "Operating temperature and bed height are studied one factor at a time.")
    sq("rk_protein_a", "The capture study measures leached Protein A in the pool across the designed experiment, so the ranges this assessment scopes are bounded against it even though no parameter is ranked on it.",
       extra=[("rk_protein_a", "The polishing steps clear what reaches them.")])
    # low-pH viral inactivation
    sq("rk_viral_inactivation", "The register assigns the cumulative XMuLV clearance requirement to this step.",
       "The register assigns the cumulative XMuLV clearance requirement to low-pH viral inactivation.")
    sq("rk_viral_inactivation", """Of its `{python} ST["viral_inactivation"]["n"]` parameters, `{python} n_vi_top` reach `{python} rpn_max`, the highest RPN in the assessment.""",
       """Of the `{python} ST["viral_inactivation"]["n"]` parameters of low-pH viral inactivation, `{python} n_vi_top` reach `{python} rpn_max`, the highest RPN in the assessment.""")
    sq("rk_viral_inactivation", "Inactivation of enveloped virus at low pH is close to first order over most of the hold, and it often tails as the titre approaches the limit of detection.")
    sq("rk_viral_inactivation", "Inactivation pH and temperature set the rate constant, and the hold time sets how long that rate acts.",
       extra=[("rk_viral_inactivation", "Where the inactivation is first order, the log reduction is proportional to the rate constant integrated over the hold.")])
    sq("rk_viral_inactivation", "The `{python} n_vi_top` parameters are studied in one designed experiment, because the log reduction depends on all of them together and none can be bounded with the others held at one setting.",
       "Inactivation pH, hold time and temperature are studied in one designed experiment, because the log reduction depends on all of them together and none can be bounded with the others held at one setting.")
    sq("rk_viral_inactivation", "Neither an in-process control nor a release test of the drug substance measures the log reduction that the hold achieves.",
       "Detection scores `{python} det_v` for the parameters of the hold that act on viral clearance, because neither an in-process control nor a release test of the drug substance measures the log reduction that the hold achieves; the claim is made from a spiking study in a qualified small-scale model.",
       extra=[("rk_viral_inactivation", "Detection scores `{python} det_v` for each of these parameters."),
              ("rk_viral_inactivation", "The viral clearance claim of the step is made instead from a spiking study in a qualified small-scale model")])
    # cation exchange
    sq("rk_cex", """Of its `{python} ST["cex"]["n"]` parameters, `{python} ST["cex"]["nq"]` are scored against a quality attribute.""",
       """Of the `{python} ST["cex"]["n"]` parameters of cation exchange chromatography, `{python} ST["cex"]["nq"]` are scored against a quality attribute.""")
    sq("rk_cex", "No step after cation exchange is credited with aggregate reduction, so aggregate that leaves this step in the pool reaches the drug substance.",
       extra=[("rk_cex", "Aggregate is the attribute that matters most here.")])
    sq("rk_cex", "Load and elution pH are expected to act together, since the resolution between monomer and aggregate depends on both.",
       "Protein load and elution buffer pH at cation exchange are expected to act together, since the resolution between monomer and aggregate depends on both.")
    # anion exchange
    sq("rk_aex", "At the load pH, DNA, virus and most host cell proteins carry a net negative charge and bind to the resin.",
       "Anion exchange is run in flow-through mode: at the load pH, DNA, virus and most host cell proteins carry a net negative charge and bind to the resin.")
    sq("rk_aex", "The load pH lies below the isoelectric point of A-Mab, which therefore carries a net positive charge and passes through, together with the basic host cell proteins.")
    sq("rk_aex", "The register assigns the cumulative MVM clearance requirement to this step",
       "The register assigns the cumulative MVM clearance requirement to anion exchange chromatography.")
    sq("rk_aex", """All `{python} ST["aex"]["n"]` of its parameters are scored against a quality attribute.""",
       """All `{python} ST["aex"]["n"]` parameters of anion exchange chromatography are scored against a quality attribute.""")
    sq("rk_aex", "Load pH is scored against `{python} n_aex_ph` attributes and reaches `{python} rpn_max`.")
    sq("rk_aex", "Load pH and load conductivity are expected to act together, since one sets the charge on each species and the other sets how strongly that charge is screened.")
    sq("rk_aex", "Operating flow rate is the one parameter in the assessment with a quality attribute at risk that is not carried into a designed experiment.")
    sq("rk_aex", "The parameter acts on the step through residence time alone, and prior knowledge places no interaction between residence time and the load chemistry.",
       "Operating flow rate acts on anion exchange through residence time alone, and prior knowledge places no interaction between residence time and the load chemistry, so it is bounded by moving it one factor at a time.",
       extra=[("rk_aex", "It is therefore bounded by moving it one factor at a time")])
    # small-virus retentive filtration
    sq("rk_virus_filtration", "Volumetric load is the parameter on which the step turns.",
       "Volumetric load is the parameter on which small-virus retentive filtration turns.")
    sq("rk_virus_filtration", "The exposure is largest at high volumetric load, where the layer is thickest.",
       extra=[("rk_virus_filtration", "Both parameters are therefore carried into the designed experiment.")])
    # UF/DF
    sq("rk_ufdf", "Each diavolume removes a fixed fraction of the buffer species left in the retentate, so the residual falls with the number of diavolumes and not with the time spent filtering.")
    sq("rk_ufdf", "Flux is expected to rise with transmembrane pressure until the membrane reaches the region in which flux no longer depends on pressure.")
    sq("rk_ufdf", "A failure of this parameter is therefore seen before the batch is released.",
       "A failure of the final drug substance concentration is seen before the batch is released.")
    # Characterization study assignment
    sq("assignment", "The study assignment is the main output of this assessment.")
    sq("assignment", "Of the `{python} n_par` parameters, `{python} n_mv` are assigned to a multivariate design and `{python} n_uni` to univariate study.")
    sq("assignment", "A designed experiment is assigned at `{python} len(doe_steps)` of the `{python} n_steps` unit operations.")
    for k in steps:
        x = sp_val[k]
        st("assignment", f"{title[k]} (Step {stepno[k]}): {x['Parameters']} parameters, {x['Quality']} scored against "
                         f"a quality attribute, {x['Multivariate']} assigned to a multivariate design and "
                         f"{x['Univariate']} to univariate study; plan and report {x['Plan / report']}.",
           [ref("assignment", sprow[k], sp_t, sprow)])
    sq("assignment", "The parameters assigned to a multivariate design are those judged able to act together with another parameter of the same unit operation.",
       extra=[("assignment", "The judgement was made from platform and prior product experience")])
    sq("assignment", "The capture step carries `{python} n_perf_doe` parameters into its design although they are scored against process performance alone, so that the same design bounds step yield.")
    sq("assignment", "It is the operating flow rate of the anion exchange step, which is scored against both viral clearance attributes and acts on the step through residence time alone.",
       "The one parameter marked univariate (justified) is the operating flow rate of the anion exchange step, which is scored against both viral clearance attributes and acts on the step through residence time alone.")
    sq("assignment", "A parameter that does not act together with the load chemistry can be bounded by moving it one factor at a time, and the anion exchange plan PCP-008 carries that justification with its design.")
    sq("assignment", "The lowest ranked parameters change step yield and process consistency, not a quality attribute.")
    sq("assignment", "gives the parameter set handed to the plans, with the set-point, the range to be studied and the normal operating range (NOR).",
       "RA-001 hands each plan its parameter set, with the set-point, the range to be studied and the normal operating range (NOR).")
    sq("assignment", "Against these NORs the range to be studied is wider at both ends for `{python} n_both` of the `{python} n_par` parameters, so that the edges of the characterized region lie outside the region in which the process is run",
       "Against the NORs the range to be studied is wider at both ends for `{python} n_both` of the `{python} n_par` parameters, so that the edges of the characterized region lie outside the region in which the process is run.")
    sq("assignment", "For `{python} n_low_sh` parameters the range studied and the NOR share their low end.",
       "For `{python} n_low_sh` parameters the range studied and the NOR share their low end: `{python} low_sh_txt`.",
       extra=[("assignment", "These are `{python} low_sh_txt`.")])
    sq("assignment", "For A-Mab concentration the NOR equals the range studied.")
    sq("assignment", "are those this assessment was made against, and PCMP-001 Version 2.0 Table 4.2 gives the values in force.",
       "The set-points and NORs of the parameter set are those the assessment was made against; PCMP-001 Version 2.0 Table 4.2 gives the values in force.")
    sq("assignment", "A parameter whose measured effect contradicts the judgement made here is reported as such in the report of its unit operation.",
       extra=[("assignment", "The assignment is prospective."),
              ("assignment", "It is revisited when the characterization reports are available.")])
    # Assumptions and limitations
    sq("assumptions", "The assessment assumes that platform behaviour transfers to A-Mab.",
       "The assessment assumes that platform behaviour transfers to A-Mab: that A-Mab responds to the same parameters in the same directions as the earlier humanized IgG1 antibodies X-Mab, Y-Mab and Z-Mab.",
       extra=[("assumptions", "The assumption is that A-Mab responds to the same parameters in the same directions."),
              ("assumptions", "The mechanisms it relies on were established on the earlier humanized IgG1 antibodies X-Mab, Y-Mab and Z-Mab and on A-Mab clinical and engineering experience")])
    sq("assumptions", "Where it does not, the characterization study finds it, which is one reason the ranges studied are wider than the NORs.")
    sq("assumptions", "The parameter list is assumed complete.")
    sq("assumptions", "Severity is taken from the quality attribute assessment and is not re-derived.")
    sq("assumptions", "Occurrence and detection are assigned by class, so the initial RPN takes only `{python} n_rpn` values across `{python} n_par` parameters.",
       extra=[("assumptions", "Ranking within a unit operation should therefore be read from severity, from the class of the attribute at risk and from the reasoning in")])
    sq("assumptions", "The judgement on which parameters act together is the weakest part of the assessment.",
       extra=[("assumptions", "A designed experiment estimates interactions only among the parameters it carries."),
              ("assumptions", "An interaction between a parameter in the design and one left out of it cannot be found by that design.")])
    sq("assumptions", "The clearest exposure is the operating flow rate of the anion exchange step, which is scored against both viral clearance attributes and studied one factor at a time.")
    sq("assumptions", "The clearest case is the elution pH of the capture step, which sets the starting pH of the low-pH hold.",
       "Material carries properties from one step to the next; the clearest case is the elution pH of the capture step, which sets the starting pH of the low-pH hold.",
       extra=[("assumptions", "Material does carry properties from one step to the next.")])
    # Outputs and downstream use
    sq("outputs", "This assessment produces three outputs.",
       "RA-001 produces three outputs: the ranking, which is the pre-characterization risk basis; the study types and their split per unit operation, which are the scope; and the parameter set that each plan takes up.")
    sq("outputs", "Each plan cites this assessment as its risk basis and takes the study type and the range to be studied.",
       extra=[("outputs", "It adds the scale-down model, the analytical methods, the sampling plan and the acceptance criteria.")])
    sq("outputs", "The scale-down model and the acceptance criteria follow PCMP-001 Version 2.0 (§7.1 and §7.3).")
    sq("outputs", "The report of the unit operation measures the effects, defines the operating region and classifies each parameter under SOP-4001.")
    sq("outputs", "It states once what the plans would otherwise each restate, including the number of parameters assigned to multivariate and to univariate study across the train (PCMP-001 Table 4.1).",
       "PCMP-001 states once what the plans would otherwise each restate, including the number of parameters assigned to multivariate and to univariate study across the train (PCMP-001 Table 4.1).")
    sq("outputs", "This assessment is changed only by revision.",
       "RA-001 is changed only by revision: a change to the parameter list, to the severity of an attribute or to an assigned study type is made by revising it, and the affected plans are revised with it.",
       extra=[("outputs", "A change to the parameter list, to the severity of an attribute or to an assigned study type is made by revising this document, and the affected plans are revised with it.")])
    # Approvals
    sq("approvals", "This assessment is approved by the functions in the approval record at the front of the document, with the responsibilities given in",
       "RA-001 is approved by the functions in the approval record at the front of the document.")
    for fn, row in aprow.items():
        x = ap_df[ap_df["Function"] == fn].iloc[0]
        st("approvals", f"{fn}: {x['Responsibility for this assessment']}.", [ref("approvals", row, ap_t, aprow)])

    order = list(dict.fromkeys(path[0] for path in SEC.values()))
    sections = []
    for ttl in order:
        stmts = [s_ for t_, s_ in ST if t_ == ttl]
        if stmts:
            sections.append(ReportSection(section_id=f"{DOC}-sec{len(sections) + 1:02d}", title=ttl,
                                          statements=stmts))

    # ==== concepts ================================================================================
    concepts = G._corpus_step_concepts()
    concepts += [Concept(concept_id=pid(key), concept_type="PROCESS_PARAMETER", canonical_name=R[key]["param"],
                         aliases=[plabel(key)], review_status="human_verified") for key in pkeys]
    concepts.append(Concept(concept_id="attr:process_performance", concept_type="PERFORMANCE_ATTRIBUTE",
                            canonical_name="Process performance", aliases=["process performance"],
                            review_status="human_verified"))
    concepts.append(Concept(concept_id=f"method:{frag_amv}", concept_type="ANALYTICAL_METHOD",
                            canonical_name=dict(P.AMV_REFS)[frag_amv], aliases=[frag_amv, "nrCE-SDS"],
                            review_status="human_verified"))

    # ==== the annex ===============================================================================
    n_q_rel = sum(len(R[k]["cqas"]) for k in pkeys if R[k]["quality"])
    annex = S.GroundTruthAnnex(
        document_id=DOC, document_title=f"{P.DOC_REGISTRY[DOC][0]} — {P.DOC_REGISTRY[DOC][1]}",
        document_class=P.DOC_REGISTRY[DOC][0], **G.rev2_layer(DOC, FILE),
        schema_extensions_used=[x for x in G.COMMON_EXT if not x.startswith("DesignSpace")] + G.REV2_EXT[:1],
        out_of_schema_notes=[
            "Pre-characterization: every parameter_type is 'unclassified'. The document does not classify "
            "parameters; CPP, WC-CPP, KPP and GPP are outputs of the characterization reports.",
            "Each ProcessParameter is anchored on its row of the ranking table (severity, initial RPN, study "
            "type, priority), of its step's failure-mode table (failure mode, effect, attributes at risk) and "
            "of the parameter set handed to the plans (unit, set-point, range studied, NOR). The schema has no "
            "field for the failure mode, the effect, the severity, the RPN or the priority; they are in "
            "rationale_for_criticality and in one statement per row of the ranking and of the failure-mode "
            "tables. study_type is the study type the ranking table assigns (multivariate DoE, univariate "
            "(justified), univariate). target_value and NOR are the values the assessment was made against, "
            "as the parameter-set table prints them (PCMP-001 Version 2.0 Table 4.2 gives the values in "
            "force), and PAR carries the range to be studied, as everywhere in the corpus: the document claims "
            "no proven acceptable range.",
            f"parameter_impacts_attribute is a prospective relation: the attribute a failure mode could reach, "
            f"not an effect shown. There is one per attribute in the 'Attribute(s) at risk' cell of each "
            f"failure-mode row ({n_q_rel} relations of {ns['n_q']} quality parameters), anchored on that row and "
            f"on the sentences of the step's subsection that name the parameter and the attribute together. "
            f"A parameter scored against process performance alone points at attr:process_performance, a "
            f"performance attribute standing for the cell 'process performance'. "
            f"parameter_does_not_significantly_impact_attribute holds only what the document states from prior "
            f"knowledge for a named attribute (A-Mab concentration at low-pH viral inactivation; elution flow "
            f"rate at cation exchange).",
            f"attribute_type is 'CQA' for the {ns['n_crit']} attributes of high or very high criticality, the "
            f"attributes the document calls critical (Section 3); the others carry 'unclassified', since the "
            f"schema has no non-critical value, and their criticality_level. tool2_severity is empty: the "
            f"document prints no A-Mab Tool #2 severity. The Severity column of Table 3.1 is the severity the "
            f"assessment carries (2 to 10, a different scale); it is in rationale_for_criticality and in one "
            f"statement per row, and fragments have none, because they were not scored.",
            f"The document names the fragment method, nrCE-SDS (PCMP-001 Version 2.0 §7.8, after "
            f"{ns['amd_id']}), but not its validation reference: the AnalyticalMethod and the concept carry the "
            f"corpus id of the nrCE-SDS method ({frag_amv}) so that the mention links to it.",
            f"studies holds the one study the document names, {first['id']}, the first study of the campaign; "
            f"RA-001 has no designed experiment and assigns the studies of the plans without naming them. No "
            f"design space, no proven acceptable range and no acceptance criterion of a step: the document "
            f"prints the drug substance criteria of the register (attribute_has_acceptance_criterion and "
            f"QualityAttribute.acceptance_criteria) and no criteria-change table.",
            "Each document relationship with a plan or a report is anchored on the row of the scope table that "
            "names both. Each row of the two tables of Version 1.0 descriptions corrected at Version 2.0, of "
            "the scoring table, of the scope table and of the approvals table is a statement anchored on its "
            "row. The abbreviations and the approval record are not represented.",
            "No rhetorical_spans (no spans file is curated for a risk assessment). weak_claims is empty.",
        ],
        inventory=G.rev2_inventory(DOC, FILE, "risk_assessment", "A-Mab drug substance",
                                   ["risk assessment", "pre-characterization", "risk ranking and filtering",
                                    "failure modes and effects", "initial risk priority number",
                                    "quality attribute register", "study-type assignment",
                                    "process characterization scope"]),
        entities=entities, studies=studies, report_sections=sections,
        assertions=AssertionStore(run_id=f"gt-{DOC}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{DOC}", concepts=concepts),
        weak_claims=[], rhetorical_spans=[])
    _gate(annex, text)
    return annex
