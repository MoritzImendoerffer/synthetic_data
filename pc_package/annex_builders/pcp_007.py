"""PCP-007 Version 2.0, the characterization plan of cation exchange chromatography (Step 7), issued
under INV-001 (and INV-002) as a protocol amendment: its ground-truth annex (``build()``).

The kinds of record follow the step-plan models in ``build_ground_truth`` (``build_plan_viral_
inactivation`` for PCP-006, ``build_plan_protein_a``, ``build_plan_bioreactor``) and the concept ids
follow the Version 1.0 builder of this plan (``build_plan_cex``: ``step:cex``, ``param:cex_*``,
``equip:cex_sdm_column``, ``equip:cex_column``): the inventory and the revision layer, the step, its
scale-down column, the commercial column and the instrumented chamber that the record names, the
two sites, the five parameters, the five attributes in scope, the five analytical methods, the
document relationships and the explicit non-claims, the four studies, the assertions, the plan
statements, the concepts, and the criteria of the criteria-change table (Version 1.0 superseded,
Version 2.0 in force). A plan claims no proven acceptable range and draws no design space, so it has
neither record.

Every table of the plan is a complex table (``T.frame`` or a ``T.`` builder), read back through
``qmd_ctables`` from the object the plan printed, so each row quote comes from the call that rendered
the row, with ``table_header=rows.header``. The related-documents table and the title block are the
markdown strings of ``related_docs_md`` and ``title_block``. Every prose quote is a span of the
``.qmd`` copied with its inline expressions and rendered by ``q``: the inline expressions evaluated
in the plan's own namespace (``qmd_inline``), each cross-reference replaced by the number the
rendered document gives it (``_xrefs``), and the quotation marks made typographic (``_smart``). ``q``
refuses a span that is not in the ``.qmd`` prose, so no value is typed here, and ``build()`` refuses
to return an annex with a quote that does not ground or with a weak anchor.

The plan carries no registered discrepancy. It keeps the Version 1.0 statement that the set-point
analysis holds the other factors at the centre of the design, which at this step is the set-point of
every factor; the annex records it as the plan states it.

Helpers new here, candidates for ``build_ground_truth``: ``_xrefs`` (the rendered form of every
``@sec-``/``@tbl-`` cross-reference, so a sentence that carries one can be quoted whole), ``_smart``
(pandoc's quotation marks, with the space ``docx_text`` reads after a closing mark that punctuation
follows) and ``_plain`` (statement text from a sentence, its cross-references dropped).
"""
from __future__ import annotations

import os
import re

import _pcpkg as P
import build_ground_truth as G
import schema_ext as S
from check_grounding import normalize, specificity_report

DOC = "PCP-007"
QMD = "PCP-007_cex.qmd"
FILE = G.PCP7_FILE                        # "PCP-007_cex.docx"
UO = G.CXUO                               # "cex"
UO_NAME = G.CXUO_NAME                     # "Cation Exchange Chromatography"
STEP_LABEL = G.CXSTEP_LABEL               # "Cation Exchange Chromatography (Step 7)"

#: Concept ids kept from the Version 1.0 builder of this document.
STEP_ID = "step:cex"
SDM_ID = "equip:cex_sdm_column"
COLUMN_ID = "equip:cex_column"
PC = G.CXPARAM_CONCEPT                    # parameter name -> concept id

#: Relationship cell of @tbl-related -> DocumentRelationship.kind (as the other step plans map it;
#: "Sibling — paired document" and "Reason for this revision" fall back to "references").
REL_KIND = {"Rolls up into": "rolls_up_into", "Parent — master plan": "executed_under",
            "Parent — risk basis for study scope": "scoped_by",
            "Parent — transfer scope": "scoped_by"}

_PRIOR = "Prior knowledge and quality risk basis"
_MM = "Materials and methods"
_SD = "Study design"
_AC = "Acceptance and decision criteria"
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
    "methods": (_MM, "Analytical methods"),
    "sampling": (_MM, "Sampling plan"),
    "stats": (_MM, "Statistical methods"),
    "factors": (_SD, "Factors, ranges and study type"),
    "screening": (_SD, "Screening design"),
    "rsm": (_SD, "Response-surface design"),
    "univariate": (_SD, "Univariate assessment"),
    "criteria": (_AC,),
    "qualification": (_AC, "Qualification of the scale-down model"),
    "adequacy": (_AC, "Model adequacy"),
    "iac": (_AC, "Intermediate acceptance criteria"),
    "judgement": (_AC, "Judgement of an output against its criterion"),
    "region": (_AC, "Operating region"),
    "verification": (_AC, "Verification of the platform worst cases"),
    "classification": (_AC, "Parameter classification"),
    "par": ("Proven acceptable ranges (planned analysis)",),
    "data": ("Data management and integrity",),
    "roles": ("Roles and responsibilities",),
    "schedule": ("Deliverables and schedule",),
    "risks": ("Risks and assumptions",),
    "approvals": ("Approvals",),
    "app_a": ("Appendix A. Planned screening design matrix",),
    "app_b": ("Appendix B. Planned response-surface design matrix",),
}

#: A cross-reference in the .qmd prose (``@sec-iac``, ``@tbl-params``).
_XREF = r"@(?:sec|tbl)-[\w-]+"


# --------------------------------------------------------------------------- #
# Local helpers. _walk, _gate and _check_sections follow annex_builders/       #
# pcp_009.py; _md_caption follows pcp_008.py; _xrefs, _smart and _plain are    #
# new here (candidates for build_ground_truth, named in the report).           #
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


def _md_caption(src, label):
    """The caption a chunk prints after a markdown table (``print(": <caption> {#label}")``)."""
    m = re.findall(r'print\(f?": (.*?) \{#' + re.escape(label) + r'\}"\)', src)
    if len(m) != 1:
        raise ValueError(f"{DOC}: {len(m)} captions printed for {label}")
    return m[0]


def _smart(s, runs=True):
    """Prose as pandoc renders it: a straight double quote opens at the start or after a space or an
    opening bracket and closes everywhere else, and a straight apostrophe becomes a typographic one.

    ``runs``: a quotation is a run of its own in the .docx, and ``docx_text`` reads the run boundary
    as a space, so a closing mark that punctuation follows directly reads ``” .`` and ``” ,`` in the
    text the gate compares against. A quote needs that space and a statement does not. Table cells
    are raw markup and keep the straight forms, so only prose goes through this."""
    s = re.sub(r'(^|[\s(\[])"', lambda m: m.group(1) + "“", s)
    s = s.replace('"', "”").replace("'", "’")
    if runs:
        s = re.sub(r"”(?=\S)", "” ", s)
    return s


def _xrefs(src, text, captions):
    """``{label -> rendered cross-reference}``: ``sec-iac`` -> ``Section 7.3``, ``tbl-params`` ->
    ``Table 5``.

    A section number comes from the heading structure of the .qmd (numbered headings counted in
    order, ``.unnumbered`` ones skipped) and is checked against the heading as the .docx numbers it
    ("7. Acceptance and decision criteria", "7.3 Intermediate acceptance criteria"). A table number
    is read from the rendered caption line "Table N: <caption>", which must occur exactly once. The
    rendered text puts a space on each side of a cross-reference (it is a field of its own), so
    ``q`` inserts the form with a space on each side and collapses the whitespace after."""
    out = {}
    prose = re.sub(r"```\{python\}.*?```", "", src, flags=re.S)
    n1 = n2 = 0
    for hashes, title, attrs in re.findall(r"^(#+) (.+?)(?: \{([^}]*)\})?[ \t]*$", prose, flags=re.M):
        if ".unnumbered" in attrs:
            continue
        if len(hashes) == 1:
            n1, n2 = n1 + 1, 0
            num, shown = f"{n1}", f"{n1}. {title}"
        elif len(hashes) == 2:
            n2 += 1
            num, shown = f"{n1}.{n2}", f"{n1}.{n2} {title}"
        else:
            raise ValueError(f"{DOC}: no numbering rule for a level-{len(hashes)} heading: {title!r}")
        if normalize(shown) not in text:
            raise ValueError(f"{DOC}: the rendered document does not number {title!r} as {num}")
        m = re.search(r"#(sec-[\w-]+)", attrs)
        if m:
            out[m.group(1)] = f"Section {num}"
    for label, cap in captions.items():
        hits = re.findall(r"Table (\d+): " + re.escape(normalize(cap)), text)
        if len(hits) != 1:
            raise ValueError(f"{DOC}: {len(hits)} rendered captions for {label}")
        out[label] = f"Table {hits[0]}"
    return out


def _plain(s):
    """Statement text from a .qmd sentence: a parenthesis of cross-references only is dropped, a
    cross-reference that closes a parenthesis is dropped with its "and", and any other
    cross-reference is refused, so that the statement is written out instead."""
    s = re.sub(r"\s*\((?:see )?" + _XREF + r"(?:(?:, | and )" + _XREF + r")*\)", "", s)
    s = re.sub(r" and " + _XREF + r"(?=\))", "", s)
    if re.search(_XREF, s):
        raise ValueError(f"{DOC}: a statement keeps a cross-reference, write it out: {s[:100]!r}")
    return s


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


# --------------------------------------------------------------------------- #
# The annex.                                                                   #
# --------------------------------------------------------------------------- #
def build():
    """The ``GroundTruthAnnex`` of PCP-007 Version 2.0."""
    import doe_report as D
    import tables as T
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
    if (ns["DOC"], ns["UO"], ns["UO_TITLE"]) != (DOC, UO, STEP_LABEL):
        raise ValueError(f"{DOC}: the .qmd is not the {UO} plan it is annexed as")

    rel = G.md_string_rows(P.related_docs_md(DOC))                 # @tbl-related, by document id
    rel_cap = _md_caption(src, "tbl-related")
    if normalize(f"{rel_cap} {rel.header}") not in text:
        raise ValueError(f"{DOC}: the related-documents caption no longer reads {rel_cap!r}")
    captions = {lab: tab.caption for lab, (tab, _) in ct.items()}
    captions["tbl-related"] = rel_cap
    xr = _xrefs(src, text, captions)

    def q(s):
        """A span of the .qmd prose as it renders. ``s`` must be copied from the .qmd with its inline
        expressions and cross-references, so a typed value fails here instead of grounding by
        coincidence."""
        if normalize(s) not in prose_src:
            raise ValueError(f"{DOC}: not a span of the .qmd prose: {s[:100]!r}")
        s = G.qmd_inline(ns, s)
        s = re.sub(_XREF, lambda m: f" {xr[m.group(0)[1:]]} ", s)
        return re.sub(r"\s+", " ", _smart(s)).strip()

    def t(s):
        """Statement text in .qmd form: its inline expressions evaluated in the plan's namespace."""
        return re.sub(r"\s+", " ", _smart(G.qmd_inline(ns, _plain(s)), runs=False)).strip()

    def ref(sec, quote, table=None, rows=None, caption=None, label=None):
        lab = table.label if table is not None else label
        r = G.ref(DOC, FILE, _sid(sec), SEC[sec][-1], quote,
                  table_title=table.caption if table is not None else caption,
                  table_id=None if lab is None else f"{DOC}_tab_{lab[4:].replace('-', '_')}",
                  table_header=None if rows is None else rows.header)
        r.heading_path = list(SEC[sec])
        return r

    def tref(sec, tab, rows, key):
        """The rendered row ``key`` of the CTable ``tab`` (``rows = ctable_rows(tab, ...)``)."""
        return ref(sec, rows[key], tab, rows)

    def keyed(label, keys, name_of, cell):
        """The rendered rows of the CTable the plan printed under ``label``, keyed. Cell ``cell`` of
        every row must name its own record: a mis-keyed row grounds and attests the wrong thing."""
        tab = ct[label][0]
        rows = G.ctable_rows(tab, keys)
        bad = [k for k, row in rows.items() if _cells(row)[cell] != name_of(k)]
        if bad:
            raise ValueError(f"{DOC} {label}: rows keyed to records they do not name: {bad}")
        return tab, rows

    A, ST = [], []

    def add(subj, pred, obj, txt, refs):
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{DOC}-A{len(A) + 1:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=txt, source_references=refs, metadata=meta()))

    def st(txt, refs):
        ST.append(ReportStatement(
            statement_id=f"{DOC}-S{len(ST) + 1:03d}",
            statement_text=txt if txt.endswith(".") else txt + ".", confidence="high",
            review_status="accepted", source_references=refs))

    def sq(sec, src_, txt=None, also=()):
        """A statement of one prose span: ``src_`` is its .qmd source, ``txt`` the statement in .qmd
        form (the span itself where it reads on its own). ``also`` cites further (section, source)
        spans the statement draws on, so every clause of it has its span."""
        st(t(txt if txt else src_), [ref(sec, q(src_))] + [ref(s_, q(x)) for s_, x in also])

    # ---- names and data the plan uses ----------------------------------------------------------
    uo = ns["uo"]
    prm = {p.name: p for p in uo.parameters}                       # parameter name -> Parameter
    pkey = {p.key: p for p in uo.parameters}                       # parameter key -> Parameter
    nm = ns["nm"]                                                  # key -> name inside a sentence
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))
    reg = P.cqa_reg.set_index("key")
    by_label = G._attr_key_by_label()
    design_cqa = set(ns["design_cqa"])                             # attributes that are responses

    # ---- the rendered tables, from the objects and calls that printed them -------------------
    pt, prow = keyed("tbl-params", list(ct["tbl-params"][1]["Parameter"]), str, 0)
    ft, frow = keyed("tbl-factors", list(ct["tbl-factors"][1]["Factor"]), str, 1)
    cq_df = ct["tbl-cqa"][1]
    ckeys = [by_label[n] for n in cq_df["Quality attribute"]]
    if ckeys != list(ns["cq_keys"]):
        raise ValueError(f"{DOC}: the attribute table does not list the plan's attributes in order")
    cq_t, crow = keyed("tbl-cqa", ckeys, lambda k: names[k], 1)
    sop_df = ct["tbl-sops"][1]
    sop_t, soprow = keyed("tbl-sops", list(sop_df["Reference"]), str, 1)
    title_of = dict(zip(sop_df["Reference"], sop_df["Title"]))
    iac = ns["iac"].reset_index().set_index("cqa")                 # D.iac_table(UO), by attribute
    ikeys = [by_label[_cells(r)[0]] for r in ct["tbl-iac"][0].rows()]
    iac_t, irow = keyed("tbl-iac", ikeys, lambda k: T.ATTR_NAME[k], 0)
    ver = ns["ver"]                                                # D.iac_verification(UO), by attribute
    wc_t, wcrow = keyed("tbl-worst-cases", list(ver.index), ns["_attr"], 0)
    ro_t, rorow = keyed("tbl-roles", list(ct["tbl-roles"][1]["Function"]), str, 0)
    w_t, wrow = keyed("tbl-windows", list(ct["tbl-windows"][1]["Study"]), str, 1)
    mtx = {kind: keyed(label, [int(r) for r in ns[pm]["Run"]], str, 1)
           for kind, label, pm in (("screening", "tbl-matrix-screening", "pm_scr"),
                                   ("rsm", "tbl-matrix-rsm", "pm_rsm"))}
    tb = G.md_string_rows(P.title_block(DOC, ns["UO_TITLE"]))     # the title block, by field
    recv = next(k for k in rorow if k.startswith("Manufacturing Science"))

    # the parameter table prints the set-points and NORs the studies were planned against, which no
    # Version 2.0 decision moved at this step (the plan's setup asserts it); check each row against
    # the configuration, so that a record never carries a value its row does not show
    for name, row in prow.items():
        p = prm[name]
        c = _cells(row)                    # Parameter | Unit | Set-point | Range studied | NOR | Study type
        if (float(c[2]) != float(p.setpoint) or c[3] != f"{p.prange[0]:g}–{p.prange[1]:g}"
                or c[4] != f"{p.nor[0]:g}–{p.nor[1]:g}" or c[5].lower() != p.study):
            raise ValueError(f"{pt.label}: row {c} does not read the configuration of {name}")
    if set(frow) != {pkey[k].name for k in ns["mv"]}:
        raise ValueError(f"{DOC}: the coded factors are not the multivariate parameters")
    if [c_ == "Yes" for c_ in (_cells(r)[3] for r in wcrow.values())] != [k in design_cqa for k in wcrow]:
        raise ValueError(f"{DOC}: the worst-case table marks responses the designs do not have")
    if (P.doe_runs(UO, "screening"), P.doe_centre_points(UO, "screening")) != (ns["n_scr"], ns["cp_scr"]) or \
            (P.doe_runs(UO, "rsm"), P.doe_centre_points(UO, "rsm")) != (ns["n_rsm"], ns["cp_rsm"]):
        raise ValueError(f"{DOC}: the plan's run counts disagree with the seeded designs")

    # ---- prose spans of the plan, copied from the .qmd (q renders them) ----------------------
    # Purpose and scope
    P_TRANSFER = "The A-Mab drug substance process is being transferred from the development site in `{python} SENDING_LOCATION`, to the commercial drug substance site in `{python} RECEIVING_LOCATION`, under the Process Transfer Plan PTP-001."
    P_SCOPE = "This plan describes the Stage 1 characterization of the cation exchange chromatography step, which is Step `{python} STEP` of the drug substance train and its principal polishing operation."
    P_COLUMN = """The studies will be executed on a scale-down model of the commercial column, in support of a process that operates at a `{python} f"{V['commercial_scale_l']:,}"` L production bioreactor scale at the receiving site."""
    P_AIM = "Their purpose is to measure how far the aggregate content, the host cell protein content, the fragment content and the yield of the eluate pool move as each parameter is varied across the ranges in @tbl-params, to define the region over which the pool meets its criteria, and to justify the ranges and the controls that will be applied in commercial manufacture"
    P_COVER = "The scope of this plan covers the `{python} n_par` process parameters of the step, the size variant and impurity attributes the step clears, and the step yield."
    P_ASSIGN = "`{python} Wc(n_mv)` parameters will be studied in a multivariate design and `{python} W(n_uv)` will be assessed one at a time, on the assignment made in the risk assessment RA-001."
    P_FEED = "The feed to the step is the neutralized pool of the low-pH viral inactivation step, and its attributes are treated as inputs to the study rather than as factors of it."
    P_THREE = "Three activities lie outside this plan."
    P_RESIN = "Resin life cycle, sanitization and repacking are qualified separately under SOP-2008, and the studies here will be run on resin inside that qualified life."
    P_AMV = "Validation of the analytical methods is covered by the method validation reports in @tbl-sops, and this plan uses those methods as validated."
    P_STAGE2 = "Confirmation of the ranges at commercial scale belongs to Stage 2 and to the process performance qualification batches, which follow the transfer."
    P_NOVIRAL = "No viral clearance claim is made for the cation exchange step."
    P_CLAIMS = "Clearance of enveloped virus is claimed at the low-pH viral inactivation step, the anion exchange step and the virus filtration step, and clearance of small viruses at the anion exchange step and the virus filtration step."
    P_PCMR = "The cumulative claim is consolidated in the master report PCMR-001"
    P_CONTRIB = "Cation exchange contributes clearance of host cell protein, DNA and leached Protein A, and those contributions are within scope."
    # Changes in this revision
    CH_V1 = "Version 1.0 of this plan was approved on `{python} v1_date`, before the first study of the step started on `{python} first_start`."
    CH_RAN = "The studies it governs ran until `{python} last_end` (@sec-schedule)."
    CH_INV1 = 'Version 2.0, effective `{python} v2_date`, is issued after them under the Quality Assurance (QA) investigation INV-001 (`{python} INV["title"]`).'
    CH_OPEN = 'QA opened the investigation on `{python} INV["opened"]`, after reviewing the master report PCMR-001 Version 1.0 for the Biologics License Application (BLA).'
    CH_CLOSE = 'It closed the investigation on `{python} INV["closed"]` with the classification `{python} INV["classification"]`.'
    CH_FOUND = "INV-001 found that the criteria used to judge each step in the proven acceptable range (PAR) analysis had been set after the data were seen and outside the approved protocols."
    CH_CA2 = "This revision carries out its corrective action CA2, the amendment of the step plans with the criteria and the fragment method."
    CH_INV2 = 'The plan is reissued under INV-002 as well (`{python} INV2["title"]`).'
    CH_INV2B = "That investigation examined the response-surface models of the campaign that fall below the model adequacy criteria of the master plan PCMP-001 §7.2."
    CH_INV2C = "Its corrective actions are the augmentation of the designs that its rule names (CA1), the refit of every other failing model (CA2) and the selection of the model of every output (CA3)."
    CH_INV2D = "The reports apply them, PCR-007 for this step, and this plan does not."
    CH_KEEP = "This revision keeps the design and the sampling of Version 1.0 of this plan, and the wording of every Version 1.0 decision rule that PCMP-001 Version 2.0 does not replace."
    CH_DEPART = "Where a study departed from them, PCR-007 records the departure."
    CH_NAMES = "Each change below names the Version 1.0 text that it replaces."
    CH_TEN = "Changes 1 to 10 also name the rule of PCMP-001 Version 2.0, or the action of INV-001, that they apply, and change 11 corrects descriptions of Version 1.0 that were wrong."
    C1_A = "The step criteria are intermediate acceptance criteria."
    C1_B = "The Version 1.0 reports judged the pool against an aggregate limit of `{python} s_agg_v1` % high molecular weight species (HMW) and a host cell protein limit of `{python} s_hcp_v1` ng/mg."
    C1_C = "Each limit was the drug substance criterion carried back through the nominal clearance of the later steps in this campaign and then divided by a margin, `{python} s_agg_mg` for aggregate and `{python} s_hcp_mg` for host cell protein (INV-001 finding 2)."
    C1_D = "The limits were set at analysis and were written into the plan text when the package was compiled in `{python} s_compiled`, without a revision of the approved plan (INV-001 finding 1)."
    C1_E = "Version 2.0 judges the pool against the intermediate acceptance criteria of PCMP-001 §7.3, which are derived from the drug substance criteria and the platform worst cases of the downstream steps (@sec-iac)."
    C1_F = "A platform worst case is the lowest clearance factor, the level entering a step divided by the level leaving it, or the largest increase that the step showed for X-Mab, Y-Mab and Z-Mab."
    C1_G = "The host cell protein criterion uses a verified A-Mab value in place of a platform worst case, the bound of `{python} s_aex_b` for the clearance factor of anion exchange."
    C1_H = "The Version 2.0 criteria for aggregate and host cell protein are wider than the Version 1.0 limits."
    C1_I = "Because the criteria rest on platform numbers, @sec-uo no longer says that prior knowledge is not carried across as a numerical claim, or that every criterion rests on data generated under this plan."
    C2_A = "Fragments are judged at this step."
    C2_B = "Version 1.0 of this plan set no criterion for fragments, and the Version 1.0 report did not judge them."
    C2_C = 'Version 2.0 judges them against the drug substance criterion of `{python} s_frag` % (PCMP-001 §7.3), on results by non-reduced capillary electrophoresis with sodium dodecyl sulfate (nrCE-SDS) under the analytical method decision `{python} AMD["id"]` (PCMP-001 §7.8 and @sec-methods).'
    C2_D = "The decision answers INV-001 finding 6, that size exclusion chromatography (SEC) reads fragments high in samples that still carry host cell protein."
    C2_E = "The Version 1.0 sentences that named aggregate and host cell protein as the attributes judged, or counted the responses, now include fragments."
    C3_A = "The scale-down model is qualified for each output by its offset, not by a test of equivalence."
    C3_B = 'Version 1.0 of this plan read "the model will be accepted where no statistically significant difference is found on any of those attributes" and "Execution may begin once the plan is approved and the scale-down model has been accepted under §5.1".'
    C3_C = "Under PCMP-001 §7.1 the model is qualified for each output by its offset from manufacturing scale, and every judgement against a criterion is stated at manufacturing scale."
    C3_D = "The qualification runs and the offset estimates come before the first characterization run, and the decision whether the model is qualified for an output is made at analysis (@sec-sdm and @sec-qualification)."
    C3_E = "As PCMP-001 §7.1 requires of each step plan, this plan names the outputs compared, the number of runs at each scale and the manufacturing-scale data set."
    C4_A = "Model adequacy is judged by the four tests of PCMP-001 §7.2."
    C4_B = "Version 1.0 of this plan judged a model on four things together."
    C4_C = "They were the overall F-test at p < `{python} alpha`, the test for lack of fit, the closeness of R², adjusted R² and predicted R², for which it set no limit, and an examination of the residuals that identified any influential run, with no test and no cut-off."
    C4_D = 'Version 2.0 sets a limit of `{python} f"{gap:.2f}"` on the difference between R² and predicted R², and states the tests on the residuals and on influential runs with their thresholds (@sec-adequacy).'
    COOK_1 = "A run with a Cook's distance above `{python} s_cook`/n is examined by deleting it and repeating the judgement."
    COOK_2 = "The model fails this test only where a run's Cook's distance exceeds `{python} s_cook_fq` of the F distribution with p and n − p degrees of freedom, where p is the number of model parameters and n the number of runs."
    C4_E = 'Version 1.0 of this plan read "A response whose model is not adequate will be reported as characterized by its data rather than by a model, and no design space and no proven acceptable range will be derived from it."'
    C4_F = "Under PCMP-001 §7.2 a model that fails the test for lack of fit or the limit on overfitting is either refitted with a justified change of terms or transformation, or it is not used to set a range."
    C5_A = "The NOR-propagated analysis is defined."
    C5_B = "It is the second PAR analysis of @sec-par, which scans one parameter while each other parameter is drawn around its set-point across its normal operating range (NOR)."
    C5_C = "Version 1.0 of this plan already judged single batches in that analysis."
    C5_D = "It drew the other factors within their NORs without stating a distribution, and accepted a setting where the predicted values met the criterion across the draws."
    C5_E = "Version 2.0 draws each other factor from the normal distribution that PCMP-001 §6.4 defines, adds the uncertainty of the fitted coefficients to each draw, and accepts a setting where the `{python} s_pct_hi`th percentile of the simulated batches does not exceed the criterion."
    C6_A = "The operating region is drawn on the prediction interval of a single run."
    C6_B = 'Version 1.0 of this plan read "The operating region will be declared where the fitted models predict that both attributes in Table 7.1 meet their in-process criteria, evaluated over the studied ranges of the `{python} k` multivariate factors", which judged the mean prediction.'
    C6_C = "Under PCMP-001 §6.2 a setting lies inside the operating region when every output with a criterion meets that criterion at both ends of the `{python} s_pi` prediction interval of a single run (@sec-region)."
    C7_A = "The platform worst cases of this step are verified."
    C7_B = "PCR-007 checks the platform worst cases of cation exchange on which the criteria upstream rely, and the verification rule of PCMP-001 §7.5 decides whether a check tightens or widens a criterion (@sec-verification)."
    C7_C = "Version 1.0 of this plan had no such check, because it had no criteria derived from platform worst cases."
    C7_D = "Objective 6, to verify those worst cases, and the verification in the deliverables of @sec-schedule are added for it."
    C8_A = "Classification also applies two rules of PCMP-001 Version 2.0."
    C8_B = "The Version 1.0 rule, which classifies a parameter from the size of its effect and the risk that it moves outside the declared region, is kept word for word."
    C8_C = "PCMP-001 §6.2 calls an output affected by a parameter when a term that contains the parameter is significant, and PCMP-001 §7.7 asks the report to state the size of each effect beside its significance and to give the reason for each class."
    C8_D = "The change is that the words of the Version 1.0 rule, held comfortably inside the region or narrow relative to it, are judged on the effect across the PAR and on the margin of the PAR to the NOR, because neither PCMP-001 nor SOP-4001 sets a numerical threshold for them (@sec-classification)."
    C9_A = "Capability thresholds are set for the drug substance."
    C9_B = "As in Version 1.0, no minimum capability index is set for the outputs of this step."
    C9_C = "PCMP-001 §7.9 now sets a target and a minimum process capability index (Cpk), against which PCMR-001 judges the drug substance (@sec-stats)."
    C10_B = 'The Version 1.0 records gave no execution dates, and Version 1.0 of this plan read "No calendar dates are committed here."'
    C10_C = "The plan text compiled in `{python} s_compiled` carried in its title block `{python} rev1_eff`, the date on which the Version 1.0 reports were approved (INV-001 finding 5), and it carried the step criteria that change 1 replaces."
    C10_D = "As PCMP-001 Version 2.0 (§5 and §9) and INV-001 preventive action PA3 require, this revision records the execution window of each study, that is the dates of its first and last laboratory runs, and the calibration status of the instrumented system named in its record (@sec-schedule)."
    C10_E = "@sec-data adds the term discrepancy from the plan, for work that this plan does not foresee."
    C11_A = "Descriptions of Version 1.0 that were wrong are corrected, with no change to the design, and the expected directions of the four expectations of @sec-uo are unchanged."
    CH_DERIV = "The derivation of these criteria uses no result of the studies of this plan (PCMP-001 §7.3)."
    #: change 11: (what Version 1.0 said, what Version 2.0 says, the statement)
    C11 = [
        ("In @sec-purpose, Version 1.0 said that small viruses are claimed at the low-pH viral inactivation step.",
         "They are claimed at anion exchange and virus filtration only.",
         "Version 2.0 corrects the Version 1.0 statement that small viruses are claimed at the low-pH viral inactivation step: they are claimed at anion exchange and virus filtration only."),
        ("In @sec-uo, Version 1.0 said that most host cell proteins are acidic at the operating pH.",
         "They have an isoelectric point below the load pH, and the part that binds weakly or with the bound antibody is now named.",
         "Version 2.0 corrects the Version 1.0 statement that most host cell proteins are acidic at the operating pH: they have an isoelectric point below the load pH, and the part that binds weakly or with the bound antibody is now named."),
        ("Version 1.0 said that the leached Protein A in complex with the antibody is released when the antibody binds the ligand, and that its modest clearance is a property of the chemistry.",
         "That complex binds with the antibody, which limits the clearance, and @sec-cqa now says that free leached Protein A stays unbound.",
         "Version 2.0 corrects the Version 1.0 statement that the leached Protein A in complex with the antibody is released when the antibody binds the ligand: that complex binds with the antibody, which limits the clearance, and free leached Protein A stays unbound."),
        ("Version 1.0 said that at a high load weakly bound host cell protein finds fewer free ligand sites from which the wash would displace it.",
         "At a high load more of it is held in association with the bound antibody.",
         "Version 2.0 corrects the Version 1.0 statement that at a high load weakly bound host cell protein finds fewer free ligand sites from which the wash would displace it: at a high load more of it is held in association with the bound antibody."),
        ("Version 1.0 said that yield is lost at the two edges of the pool and named two losses on the trailing edge.",
         "The loss on the leading edge is now named.",
         "Version 1.0 named two losses of yield on the trailing edge of the pool; Version 2.0 also names the loss on the leading edge."),
        ("In @sec-risk, Version 1.0 said that the range of elution buffer pH stops short of the pH at which the antibody would no longer bind reproducibly.",
         "It stops short of incomplete elution at its low end and of elution of aggregate with the monomer at its high end.",
         "Version 2.0 corrects the Version 1.0 statement that the range of elution buffer pH stops short of the pH at which the antibody would no longer bind reproducibly: it stops short of incomplete elution at its low end and of elution of aggregate with the monomer at its high end."),
        ("In @sec-sdm, Version 1.0 called the centre point spread the only estimate of experimental error that the analysis uses.",
         "The residual of each fitted model is another, and the sentence is removed.",
         "Version 2.0 removes the Version 1.0 sentence that called the centre point spread the only estimate of experimental error that the analysis uses: the residual of each fitted model is another."),
        ("In @sec-operation, Version 1.0 described the collection thresholds as relative to the peak maximum, while its Table 6.1 set the stop collect in OD units, from `{python} s_sc_lo` to `{python} s_sc_hi` with a set-point of `{python} s_sc_sp`.",
         "The description now matches the design.",
         "Version 1.0 described the collection thresholds as relative to the peak maximum while its Table 6.1 set the stop collect in OD units, from `{python} s_sc_lo` to `{python} s_sc_hi` with a set-point of `{python} s_sc_sp`; Version 2.0 makes the description match the design."),
        ("Version 1.0 also said that one buffer sets the ionic strength of the load and the wash.",
         "The load is the adjusted pool, and the equal conductivities are a design choice of the platform.",
         "Version 2.0 corrects the Version 1.0 statement that one buffer sets the ionic strength of the load and the wash: the load is the adjusted pool, and the equal conductivities are a design choice of the platform."),
        ("The temperature control is named once, as controlled room temperature.", None,
         "Version 2.0 names the temperature control once, as controlled room temperature."),
        ('In @sec-screening, Version 1.0 said that a resolution IV fraction would alias the interactions of `{python} nm["load"]` with each other.',
         "It would alias each of them with the interaction of the other two factors.",
         'Version 2.0 corrects the Version 1.0 statement that a resolution IV fraction would alias the interactions of `{python} nm["load"]` with each other: it would alias each of them with the interaction of the other two factors.'),
        ("In @sec-risks, Version 1.0 said that the qualification and the centre point performance would confirm the first assumption.",
         "The designs test it against the expectations of @sec-uo.",
         "Version 2.0 corrects the Version 1.0 statement that the qualification and the centre point performance would confirm the first assumption: the designs test it against the expectations of the unit-operation description."),
    ]

    # Objectives
    OB_SIX = "The study has six objectives."
    OB = ["To quantify the relationship between each studied parameter and each response of the step, over ranges wider than the ranges in which the step will be operated.",
          "To define the multivariate region over which the fitted models predict that the aggregate, the host cell protein and the fragment content of the eluate pool all meet the criteria in @tbl-iac.",
          "To establish a proven acceptable range for each parameter against the aggregate, the host cell protein and the fragment content of the pool, both with the rest of the step at target and with the rest of the step varying within its normal operating ranges.",
          "To classify each parameter under SOP-4001, from the size of its demonstrated effect and from the capability with which the parameter is controlled.",
          "To state the ranges, in-process controls and monitoring this step contributes to the control strategy, and to justify them for Stage 2.",
          "To verify the platform worst cases of cation exchange on which the criteria upstream rely (@sec-verification)."]
    OB_V2 = "This objective is added at Version 2.0."
    OB_PCR = "The report PCR-007 will present the outcome against each of these objectives."
    # Related documents
    REL_RA = "The risk assessment RA-001 set the scope of the study, this plan executes that scope, and PCR-007 will report the outcome."
    REL_SOPS = "The controlled procedures and method validations that govern the work are listed in @tbl-sops."
    REL_PH = "The SOP and AMV numbers are placeholders."
    # Unit-operation description and prior knowledge
    U_MODE = "The cation exchange step is operated in bind and elute mode and is the principal aggregate polishing operation of the purification train."
    U_BIND = "Below its isoelectric point the antibody carries a net positive charge and binds the sulfonate ligand of the resin."
    U_ELUTE = "It is eluted by raising the pH of the elution buffer, which weakens the electrostatic attraction."
    U_AGG = "Aggregate presents more positive surface to the ligand than monomer does and is therefore retained more strongly, so it elutes later than monomer."
    U_RES = "The clearance the step achieves depends on how well the two species are resolved and on the point at which pool collection is stopped."
    U_IMP = "Host cell protein, DNA and leached Protein A are cleared because they carry a net negative charge at the load pH and are therefore not retained by the sulfonate ligand."
    U_HCP1 = "Most host cell proteins have an isoelectric point below the load pH, so they leave in the load flow through, and the weakly bound remainder is displaced during the wash."
    U_HCP2 = "A part of the host cell protein is held in association with the bound antibody, where the wash does not displace it, and it elutes with the antibody."
    U_DNA = "DNA carries a strong negative charge and is repelled by the ligand, so it passes through in the load and its clearance is large and insensitive to the operating parameters."
    U_LPA1 = "Leached Protein A and its fragments are acidic as well and do not bind under load conditions, but the leached Protein A that is in complex with the antibody binds with it, which limits the clearance."
    U_LPA2 = "The step therefore clears leached Protein A by a modest factor, which is not expected to depend on any parameter studied here."
    U_YIELD1 = "Yield is lost at the two edges of the pool."
    U_YIELD2 = "Monomer that elutes before collection starts is lost on the leading edge, and monomer that elutes after the stop collect point, or with the aggregate that is cut away, is lost on the trailing edge."
    U_FRAG1 = "Fragments carry less positive charge than intact antibody at the binding pH and elute on the leading side of the main peak, so the leading fractions are rich in fragments."
    U_FRAG2 = "A later start of collection leaves more of that edge out of the pool, and a later stop adds more of the trailing eluate, which carries few fragments."
    U_FRAG3 = "Both lower the fragment content of the pool."
    U_FRAG4 = "The step is expected to clear part of the fragment load, not all of it."
    U_PLAT = "The step has been operated on the Novacyte humanized immunoglobulin G1 (IgG1) platform for three previous products (X-Mab, Y-Mab and Z-Mab) and throughout A-Mab clinical and engineering manufacture"
    U_SAME = "The resin chemistry, the buffer system and the mode of operation are unchanged for A-Mab."
    U_EXP = "This experience establishes the mechanisms above and identifies the parameters worth studying."
    U_WC = "Prior knowledge also supplies the platform worst cases from which the criteria are derived (@sec-iac and @sec-verification)."
    U_DATA = "Every range reported in PCR-007 will rest on data generated under this plan."
    U_FOUR = "Four expectations follow from that experience, and the multivariate design is built to test them."
    E_LOAD1 = 'A higher `{python} nm["load"]` occupies more of the sulfonate ligand, so at the top of the studied range the column approaches its dynamic binding capacity.'
    E_LOAD2 = "As occupancy rises the monomer and the aggregate peak both broaden and overlap further, and a larger share of the host cell protein is held on the column through its association with the bound antibody, so that it escapes the wash and elutes with the antibody."
    E_LOAD3 = "Rising ligand occupancy is therefore expected to move aggregate clearance, host cell protein clearance and yield in the same direction, all three falling as load rises."
    E_COND1 = '`{python} Nm["wash_cond"]` sets the ionic strength that shields the charge on the ligand and on the bound species.'
    E_COND2 = "A higher conductivity is expected to strip more of the weakly bound host cell protein during the wash, while the antibody, which binds more strongly, stays bound."
    E_COND3 = "Its effect should fall on impurity clearance rather than on the aggregate separation, which happens during elution."
    E_PH1 = '`{python} Nm["elution_ph"]` sets the net charge on the antibody at the moment of elution.'
    E_PH2 = "A higher pH within the studied range weakens binding and brings monomer and aggregate off the column earlier and closer together, so it is expected to reduce the resolution on which aggregate clearance depends."
    E_SC1 = "Monomer elutes ahead of aggregate, so the material still leaving the column on the descending edge of the peak is progressively richer in aggregate."
    E_SC2 = "Stopping collection later therefore recovers more monomer from the tail and carries the leading part of the aggregate peak into the pool, and stopping earlier leaves both behind."
    E_SC3 = "The stop collect point is an absorbance on the descending edge (@tbl-params), so a lower setting stops collection later."
    E_INT = 'At a high load more host cell protein is held in association with the bound antibody, and a higher ionic strength weakens that association, so a higher `{python} nm["wash_cond"]` is expected to remove more host cell protein at a high load than at a low one.'
    E_FLOW1 = '`{python} Nm["flow"]` sets the residence time of the antibody in the pores of the resin during elution, and a longer residence time lets the antibody equilibrate more completely with the mobile phase and so sharpens the elution peak.'
    E_FLOW2 = "Over the range in @tbl-params, and at the particle size of the platform resin, the change in peak sharpness is expected to be too small to move the aggregate content of the pool."
    # Quality attributes in scope
    Q_REG = "The drug substance register of critical quality attributes (CQAs) assigns no quality attribute to the cation exchange step."
    Q_ORIGIN = "Aggregate is formed in the production bioreactor and is added to during the low-pH hold, host cell protein and DNA enter with the harvested cell culture fluid, leached Protein A is released from the capture resin, and fragments are formed in culture and during the harvest hold."
    Q_REMOVE = "This step removes them."
    Q_CRIT = "Criticality follows the continuum of ICH Q9 rather than a binary split"
    Q_TOOL = "and it was assigned with Tool #1 of the case study, which combines the impact of the attribute on safety and efficacy with the uncertainty in that impact"
    Q_RESP = "`{python} Wc(n_cq_resp)` of the `{python} W(n_cq)` attributes will be measured as responses of the designed experiments."
    Q_AGG = "Aggregate is the attribute the step exists to control and carries the highest criticality of the `{python} W(n_cq)`."
    Q_HCP = "Host cell protein is cleared here and again at the anion exchange step, so this step must hand on a pool that the remaining train can bring to the drug substance criterion."
    Q_FRAG = "Fragments are measured by nrCE-SDS in the response-surface design (@sec-methods)."
    Q_DNALPA = "Residual DNA and leached Protein A will be measured across the step so that their clearance is confirmed, and neither is treated as a response of the designed experiments, because DNA is repelled by the sulfonate ligand at every conductivity and pH in @tbl-params and free leached Protein A stays unbound over the same range."
    Q_DNALPA_A = "Residual DNA and leached Protein A will be measured across the step so that their clearance is confirmed"
    Q_DEP = "PCR-007 will report the clearance observed for both, and will claim a parameter dependence for neither unless the data show one."
    Q_YIELD1 = "Step yield is a process performance attribute rather than a quality attribute."
    Q_YIELD2 = "It is measured on every run because the monomer that is cut away with the aggregate is lost from the pool, so the aggregate clearance and the yield of a setting have to be read together."
    Q_YIELD3 = "It has no acceptance criterion in @tbl-cqa."
    # Risk-based prioritization of parameters
    R_RANK = "All process parameters of the cation exchange step were carried into the risk ranking and filtering exercise of RA-001, in which each parameter was given one ranking for its potential impact on a quality attribute and a second for its potential to interact with other parameters, and the two rankings were combined into a study assignment"
    R_HIGH = "Where no data or rationale were available to make an assessment, the parameter was ranked at the highest level."
    R_THREE = "The assignment produced three groups."
    R_MV = "`{python} Wc(n_mv)` parameters were assigned to the multivariate design."
    R_WHY = '`{python} Nm["load"]`, `{python} nm["elution_ph"]` and `{python} nm["stop_collect"]` each move the aggregate peak relative to the point at which collection stops, and `{python} nm["load"]` acts with the `{python} nm["wash_cond"]` to set how much weakly bound host cell protein survives the wash, so the effects of the `{python} W(n_mv)` on the pool cannot be assumed to add.'
    R_WHY_AGG = '`{python} Nm["load"]`, `{python} nm["elution_ph"]` and `{python} nm["stop_collect"]` each move the aggregate peak relative to the point at which collection stops'
    R_WHY_HCP = '`{python} nm["load"]` acts with the `{python} nm["wash_cond"]` to set how much weakly bound host cell protein survives the wash'
    R_UV = '`{python} Nm["flow"]` was assigned to a univariate assessment, since its expected effect on the separation is small (@sec-uo).'
    R_FIXED = "Parameters that are fixed by equipment design or held to platform specification, such as bed height, column packing quality and buffer composition, were not assigned a new study."
    R_FIXED2 = "Their ranges are supported by the platform knowledge space and by the operation and life cycle procedures in @tbl-sops."
    R_WIDE = "The ranges in @tbl-params are wider than the normal operating ranges in every case."
    R_SET = "Each was set from the control capability of the commercial equipment and from the range over which the platform has been operated, so that the study bounds the step beyond the region in which it will run and supports later movement within the region it defines"
    R_FAIL = "Ranges were not widened past the point at which the step would fail for a reason that is already understood."
    R_PH = 'The `{python} nm["elution_ph"]` range stops short of the pH at which the antibody would no longer elute completely, at its low end, or would elute together with its aggregate, at its high end, because a run at such a pH would confirm the mechanism and would tell the study nothing about the operating region.'

    # Scale-down model and its qualification
    S_COL = "The studies will be run on a laboratory column packed with the same resin type and to the same bed height as the commercial column, and operated at the same linear velocities."
    S_UNITS = "Protein load will be set in grams of antibody per litre of resin, and the equilibration, wash, elution and strip volumes will be set in column volumes, so that every parameter of the study is expressed at its commercial equivalent."
    S_PACK = "Packing quality will be verified before each campaign by plate count and peak asymmetry, and a column that fails either test will be repacked before use."
    S_SOP = "The model and its operation are described in SOP-1001 and SOP-2010."
    S_QRUNS = "The qualification runs will be made against commercial scale data before any characterization run is executed, and the offset of each output will be estimated from them."
    S_QCMP = "Qualification will compare the model and the commercial step at the set-point condition of @tbl-params on the attributes that enter and leave the step, which are step yield, pool aggregate, pool host cell protein, residual DNA and leached Protein A."
    S_QN = "The comparison will be made from replicate runs at small scale against the available at-scale batches, `{python} n_sdm` scale-down runs at set-point against `{python} n_mfg` A-Mab batches at manufacturing scale."
    S_PLATE = "Plate count and peak asymmetry are compared as well (PCMP-001 §5)."
    S_OFF = "The offset of an output is the mean of the scale-down runs at set-point minus the mean of the manufacturing-scale batches, with its two-sided `{python} s_offci` confidence interval."
    S_SIDE = "Each end of that interval is a one-sided `{python} s_side` confidence bound."
    S_DECIDE = "Whether the model is qualified for an output is decided at analysis, by the rule of @sec-qualification, because that decision needs the response-surface model."
    S_SUB = "Pool aggregate and pool host cell protein have a criterion at this step, and every judgement of them against it first subtracts the offset, so their ranges and conclusions are stated at manufacturing scale."
    S_OTHER = "The other outputs compared have no criterion at this step, so their offsets are recorded and no conclusion depends on them."
    S_NOFRAG = "The qualification does not compare fragments at both scales."
    S_UNK = "Their offset is unknown, not zero, and fragments are judged as the scale-down model gives them (PCMP-001 §7.1)."
    S_ASSUME = "That judgement rests on the assumption, stated in @sec-risks, that fragments separate in the same way at both scales."
    S_REPRO = "Reproducibility of the model will be re-established inside each designed experiment."
    S_CP = "The centre point runs of both designs are executed at the set-point of every factor, so their spread measures the reproducibility of the model under study conditions and provides the pure error term against which lack of fit is tested (see @sec-stats)."
    S_BOUND = "The claims this study makes are bounded by the scale-down model."
    S_NOTREP = "A scale-down column reproduces the chromatography of the commercial column, and it does not reproduce the hold times, the pool volumes or the mixing of the commercial suite."
    S_APPLY = "Conclusions drawn here apply to the commercial step through the qualification above, and they will be confirmed at scale during Stage 2."
    # Operation
    O_RECV = "The step receives the neutralized pool of the low-pH viral inactivation step."
    O_ADJ = "The pool is adjusted to the load conductivity given in @tbl-params and is loaded onto the equilibrated column at the target protein load."
    O_WASH = "The column is then washed at the same conductivity as the load."
    O_EQUAL = "The platform sets the two equal by design, so they are varied together and cannot be varied independently."
    O_ELU = "Elution is a step change to the elution buffer at the pH under study."
    O_COLLECT = "The pool is collected between a threshold on the ascending edge of the elution peak and the stop collect threshold on the descending edge, both read as ultraviolet absorbance (OD280)."
    O_STRIP = "After collection the column is stripped, sanitized and re-equilibrated under SOP-2008."
    O_INPUTS = "Buffer preparation, column packing and resin storage are held to platform specification and are governed by the procedures in @tbl-sops."
    O_NOTF = "They are identity and quality controlled inputs to this study rather than factors of it."
    O_TEMP = "Chromatography is performed at controlled room temperature and temperature is not varied, because the platform operates the step under the same control at both sites and the transfer introduces no difference in that control."
    # Analytical methods
    M_VALID = "Every response and every attribute in scope will be measured by a validated method."
    M_AGG = "Pool aggregate will be measured by size exclusion chromatography under AMV-3011 and reported as the percentage of high molecular weight species."
    M_HCP = "Host cell protein will be measured by enzyme-linked immunosorbent assay under AMV-3012 and reported per milligram of antibody, so that the reported value does not move with the concentration of the pool."
    M_DNALPA = "Residual DNA will be measured by quantitative polymerase chain reaction under AMV-3014, and leached Protein A by enzyme-linked immunosorbent assay under AMV-3016."
    M_DNA = "Residual DNA will be measured by quantitative polymerase chain reaction under AMV-3014"
    M_LPA = "leached Protein A by enzyme-linked immunosorbent assay under AMV-3016"
    M_YIELD = "Step yield will be calculated from the antibody mass in the pool and in the load, each determined by ultraviolet absorbance against the extinction coefficient of A-Mab."
    M_FRAG = "Fragments are measured by nrCE-SDS under AMV-3020."
    M_AMD = 'From `{python} AMD["date"]`, every study that measures fragments, at every step, measures them by nrCE-SDS, following the analytical method decision `{python} AMD["id"]`, so that one method spans the train (PCMP-001 §7.8).'
    M_T73 = "PCMP-001 Table 7.3 shows which method each design of the campaign used."
    M_ONLY = "Fragments are judged on the nrCE-SDS results only."
    M_VAR = "Assay variability is part of the residual variance of each fitted model, and it is part of the centre point spread that estimates pure error, so a response measured by a less precise assay will carry a wider prediction interval and a less sensitive lack of fit test."
    M_ATTR = "Where a predicted value sits within assay variability of its criterion, PCR-007 should attribute the result to the assay and should not claim an effect."
    M_REPRO = "Host cell protein is expected to be the least reproducible of the responses, and the centre point runs will establish whether that expectation holds."
    # Sampling plan
    SP_FOUR = "Each run will be sampled at four points."
    SP_LOAD = "The load will be sampled after conditioning, so that the aggregate, host cell protein, DNA and leached Protein A levels entering the step are known for every run."
    SP_FT = "The flow through and the wash will each be sampled as a single pooled fraction, which allows the host cell protein mass balance across the step to be closed."
    SP_POOL = "The eluate pool will be sampled after collection and mixing are complete, and it carries every response of the study."
    SP_STRIP = "A strip fraction will be sampled and retained, and will be tested only where a run fails to close its mass balance."
    SP_REP = "Replication is concentrated at the centre point."
    SP_CP = "The screening design carries `{python} cp_scr` centre point runs and the response-surface design carries `{python} cp_rsm`."
    SP_ORDER = "Samples will be assigned to analytical runs in an order that does not follow the design order, so that drift in an assay cannot align with a factor."
    SP_RET = "Retained samples will be held under the conditions and for the period stated in SOP-2010, so that a re-test is possible where a result is questioned."
    # Statistical methods
    T_CODED = "All factors will be analysed in coded units."
    T_CODE = "Each factor is coded so that its set-point is 0 and the edges of its studied range are −1 and +1, which makes the estimated effects comparable across factors carrying different units and makes the intercept the predicted response at the centre of the design."
    T_OLS = "The screening design will be analysed by ordinary least squares with all main effects and all two-factor interactions."
    T_EFFECT = "An effect will be reported as twice the coded coefficient, which is the change in the response across the full studied range of that factor."
    T_SIG = "Terms will be judged significant at p < `{python} alpha`."
    T_PURPOSE = "The purpose of the screening analysis is to identify which factors and which interactions change each response, and by how much across the studied range."
    T_NOTPRED = "It is not the predictive model of the step, since a model without quadratic terms cannot describe curvature, and the response-surface model is the model from which the operating region, the proven acceptable ranges and the capability estimate will all be derived."
    T_ALSO = "The judgement of each output over the NOR (@sec-judgement) and the verification of the platform worst cases (@sec-verification) also come from it."
    T_RSM = "The response-surface design will be analysed as a full quadratic model in its `{python} k` factors, with main effects, two-factor interactions and pure quadratic terms, `{python} n_terms` terms with the intercept."
    T_REPORT = "Each fitted model is reported with R², adjusted R² and predicted R², the last computed from the prediction error sum of squares (PRESS), with the model F-test and with the test for lack of fit against the pure error of the centre point runs."
    T_NOEFF = "A factor with no significant term in either model will be reported as having no demonstrated effect on that response."
    T_BOUNDED = "Such a statement is bounded by the range studied and by the power the design carries, and PCR-007 will state it in those terms rather than as an absence of effect in general."
    T_PI = "The `{python} s_pi` prediction interval of a single run that @sec-judgement uses is exact."
    T_PI2 = "It uses the t distribution and includes the residual variance and the uncertainty of the fitted coefficients."
    T_PI3 = "For pool aggregate and pool host cell protein it is computed at manufacturing scale, by subtracting the offset of @sec-sdm."
    T_MC = "Capability at commercial scale will be estimated by Monte Carlo simulation."
    T_MC2 = "`{python} Wc(V['n_monte_carlo'])` batches will be simulated with every parameter drawn within its normal operating range, the fitted models will be evaluated at each draw, and a one-sided capability index will be computed for each attribute in @tbl-iac against its criterion."
    T_NOCPK = "No minimum capability index is set as an acceptance criterion in this plan."
    T_RULE = "The decision rule is the one stated in @sec-criteria, and the capability estimate will be reported alongside it, with the margin between the predicted distribution and the limit, as supporting evidence."
    T_DS = "The capability of the drug substance is estimated from the integrated model of the train that PCMP-001 §6.5 defines."
    T_CPK = "PCMR-001 judges it against the campaign thresholds of PCMP-001 §7.9, a target process capability index (Cpk) of `{python} s_cpk_t` and a minimum of `{python} s_cpk_m`."
    # Factors, screening, response surface, univariate
    F_MV = "The `{python} n_mv` multivariate parameters enter both designs as the factors of @tbl-factors."
    F_CODES = "The letter codes are used for the model terms in PCR-007 and for the design matrices in Appendix A and Appendix B."
    C_DESIGN = "The screening study is a two-level full factorial in the `{python} k` multivariate factors, augmented with `{python} cp_scr` centre point runs, giving `{python} n_scr` runs in total."
    C_WHY = 'A full factorial was selected rather than a fraction, because the factor count is small and because `{python} nm["load"]` is expected to interact with each of the other `{python} W(k - 1)` factors, through the peak broadening that rising ligand occupancy produces.'
    C_ALIAS = "A resolution IV fraction would alias each of those interactions with the interaction of the other two factors (`{python} alias_txt`) and would leave the analysis unable to say which of them is active."
    C_EST = "The design as planned estimates every main effect and every two-factor interaction independently."
    C_RAND = "Runs will be executed in a randomized order, with the centre point runs distributed through the campaign rather than grouped, so that drift in the model or in the feed material appears in the centre point spread rather than in a factor effect."
    C_LOT = "All runs will be performed on a single conditioned feed lot where the available material allows it."
    C_LOTS = "Where more than one lot is required, the lot will be recorded with the run and the centre point runs will be balanced across lots."
    RS_DESIGN = "The response-surface study is a face-centred central composite design in the `{python} k` factors of the screening study, with `{python} n_fact_rsm` factorial runs, `{python} n_ax` axial runs and `{python} cp_rsm` centre point runs, giving `{python} n_rsm` runs in total."
    RS_FACES = "The axial runs are placed on the faces of the cube rather than beyond them, so that no run is executed outside the studied range of any factor."
    RS_ROT = "The studied ranges are already wider than the normal operating ranges, and a rotatable design would require settings outside them for which the step has no prior support."
    RS_QUAD = "The response-surface design adds the quadratic terms that the screening design cannot estimate."
    RS_CURV = 'Curvature is expected on `{python} nm["stop_collect"]` and on `{python} nm["elution_ph"]`.'
    RS_CUT = "Both change where the pool is cut relative to the aggregate peak, and because that peak has a maximum, equal steps in the cut point add unequal amounts of aggregate to the pool."
    RS_SEQ = "The two designs are executed in sequence and are analysed separately."
    RS_AUG = "Should the screening analysis identify an active factor that is not carried into the response-surface design, the design should be augmented before the operating region is declared, and the augmentation should be documented as a change to this plan under @sec-approvals."
    RS_ALL = "The response-surface design carries all `{python} k` screening factors, so this rule cannot apply at this step."
    V_ONE = '`{python} Nm["flow"]` will be assessed one factor at a time.'
    V_RUNS = "Runs will be executed at the low edge, the set-point and the high edge of the range given in @tbl-params, with every other parameter held at its set-point, and the responses that Version 1.0 listed in its §5.3 (`{python} uv_resp`) will be measured on each."
    V_WHAT = "The assessment will establish whether a longer residence time sharpens the elution peak enough to change the aggregate content or the yield of the pool over the studied range, and it will support the range within which flow rate is controlled in manufacture."
    V_INT = "A univariate assessment cannot determine whether flow rate interacts with the other parameters."
    V_WHY = "It is accepted on that basis here because flow rate changes the residence time of the antibody in the pores of the resin and with it the sharpness of the elution peak, and it changes neither the net charge on the antibody nor the ionic strength that sets how strongly the antibody is held, so an interaction with load, conductivity, elution pH or the collection window is not expected."
    V_MOVE = "Should the assessment show an effect on any response comparable in size with the effects estimated in the screening study, flow rate should be carried into a multivariate study before the operating region is declared."

    # Acceptance and decision criteria
    CR_FOUR = "Version 1.0 of this plan named four decisions, each with its own rule."
    CR_THEY = "They are the acceptance of the scale-down model, the adequacy of a model, the operating region and the classification of each parameter."
    CR_V2 = "PCMP-001 Version 2.0 replaces the first, extends the second and the third, and adds the judgement of each output against its criterion and the verification of the platform worst cases."
    CR_WORDS = "Several decisions of Version 1.0 rest on words for which it set no numerical threshold."
    CR_LIST = 'They are the claim of a parameter dependence for residual DNA and leached Protein A "unless the data show one" (@sec-cqa), the repacking of a column that fails the packing tests (@sec-sdm), the attribution of a result "within assay variability of its criterion" to the assay (@sec-methods), the test of the strip fraction when a run fails to close its mass balance (@sec-sampling), the move of elution flow rate into a multivariate study after an effect "comparable in size with the effects estimated in the screening study" (@sec-univariate) and the identification of the runs made on a lot "out of trend" (@sec-risks).'
    CR_NONE = "This revision sets none either, and PCR-007 states the approach it takes for each."
    QL_SEP = "The scale-down model is qualified for each output separately, by its offset from manufacturing scale and not by a test of equivalence (PCMP-001 §7.1)."
    QL_RULE = "For pool aggregate and pool host cell protein, the outputs compared at both scales that have a criterion at this step, the model is qualified when the conclusion over the NOR is the same with the offset at either end of its `{python} s_offci` confidence interval."
    QL_CONC = "The conclusion over the NOR is whether the output meets its criterion at every combination of NOR low, set-point and NOR high of the `{python} k` factors, judged as @sec-judgement states."
    QL_NOTUSED = "A model whose conclusion changes between the two ends of the interval is not used for that output."
    QL_CAUSE = "Where the cause of an offset is known, PCR-007 states it."
    QL_NOTQ = "Where the model is not qualified for an output, PCR-007 says so and states the consequence."
    MA_FOUR = "PCMP-001 §7.2 sets four criteria for the adequacy of a response-surface model, and this plan states them as tests."
    MA_1 = "The model F-test is significant at α = `{python} alpha`, the level PCMP-001 sets for model terms."
    MA_2 = "Lack of fit against the pure error of the centre point runs is not significant at α = `{python} alpha_lof`."
    MA_3 = 'Predicted R² falls short of R² by no more than `{python} f"{gap:.2f}"`, the limit on overfitting that PCMP-001 sets.'
    MA_3B = "A model that fits its own runs much better than it predicts runs left out of the fit has more terms than the data support."
    MA_4 = "The residuals show no pattern against the predicted values or the run order, and no single run dominates the fit."
    MA_4B = "The absolute residuals are regressed on the predicted values, and the residuals on the run order, and neither slope may be significant at α = `{python} alpha_res`."
    MA_NOSTAT = "PCMP-001 §7.2 states the fourth criterion without a statistic."
    MA_CAMP = "The two tests and their thresholds are those of the campaign, applied in the same way in every step plan."
    MA_ABS = "The absolute residuals are regressed because the residuals of a least squares fit have no slope against the predicted values by construction, while a scatter that grows with the level shows as a slope of their absolute values."
    MA_FAIL = "A model that fails the test for lack of fit or the limit on overfitting is either refitted with a justified change of terms or transformation, or it is not used to set a range (PCMP-001 §7.2)."
    MA_FLAG = "PCR-007 examines any run that the fourth test flags, and @sec-verification states which of the tests the model behind a widening bound must pass."
    MA_DESC = "Where no adequate model results, PCR-007 should report the response descriptively, against the criterion, over the runs of the design."
    MA_LOF = "Where lack of fit is significant, PCR-007 should state whether the cause is a missing term or an outlying run, and should establish that from the residuals rather than from the summary statistics alone."
    I_TABLE = "The quality criteria the pool is judged against are given in @tbl-iac."
    I_EACH = "Each is an intermediate acceptance criterion (IAC)."
    I_DERIVE = "PCMP-001 §7.3 derives it by carrying the drug substance criterion backward through the train, step by step, with the platform worst case of each downstream step, and no margin is applied."
    I_NOSTEP = "No step after cation exchange changes fragments in this derivation."
    I_DS = "The cation exchange pool is therefore judged against the drug substance criterion for fragments itself, `{python} s_frag` %."
    I_AAP = "The a priori derivation also assumed that no step after cation exchange changes aggregate, which made the aggregate criterion the drug substance criterion of `{python} s_ds_agg` %."
    I_UF = "PCMP-001 §7.3 sets an increase across UF/DF of up to `{python} s_uf_add` percentage points at the prediction bound of a single batch within the UF/DF NOR."
    I_AGG = "The aggregate criterion in force is the drug substance criterion less that increase, `{python} s_agg` %."
    I_HCP1 = "For host cell protein the drug substance criterion of `{python} s_ds_hcp` ng/mg is carried back through anion exchange."
    I_HCP2 = "With the platform worst case of anion exchange, a clearance factor of `{python} s_aex_pf`, the criterion is `{python} s_hcp_ap` ng/mg a priori."
    I_PCR8 = "The anion exchange report PCR-008 verified that worst case."
    I_BOUND = "It found a one-sided `{python} s_vb` prediction bound of a single batch of `{python} s_aex_b` for the clearance factor at the least favourable combination of the anion exchange NOR, better than the platform value, on a model that meets the first three adequacy criteria of PCMP-001 §7.2 and is not an exact fit."
    I_FORCE = "The bound therefore replaced the platform value, and the criterion in force is `{python} s_hcp` ng/mg."
    I_RISK = "PCR-008, the report that gave the bound, examines it and argues the change by its risk (PCMP-001 §7.5)."
    I_NONE = "Residual DNA, leached Protein A and step yield have no criterion at this step, so no range is derived from them."
    I_NODNA = "The platform history gives no worst-case DNA clearance for the steps after Protein A, so no DNA criterion can be carried back, and residual DNA is judged on the drug substance only."
    I_LPA = "Leached Protein A is judged in the Protein A pool, against a criterion carried back through the platform worst cases of cation exchange and anion exchange."
    J_QA = "Every output with a criterion at this step is a quality attribute."
    J_BATCH = "Its criterion applies to each batch, so each output is judged on a single batch."
    J_PI = "A response-surface model predicts the mean response, and a single batch scatters around that mean, so the judgement uses a prediction interval or bound of a single batch (@sec-stats)."
    J_FOUR = "Four analyses judge an output in this way."
    J_THEY = "They are the judgement over the NOR, the operating region (@sec-region), the NOR-propagated PAR (@sec-par) and the verification of the platform worst cases (@sec-verification)."
    J_NOR = "The judgement over the NOR asks whether the exact `{python} s_pi` prediction interval of a single run, at manufacturing scale, lies within the criterion at every one of the `{python} n_comb` combinations of NOR low, set-point and NOR high of the `{python} k` factors."
    J_UPPER = "All criteria at this step are upper limits, so the upper end of the interval decides."
    OR_DEF = "The operating region is the region of the `{python} k` multivariate factors, within their studied ranges, over which every output with a criterion in @tbl-iac meets that criterion at both ends of the `{python} s_pi` prediction interval of a single run, at manufacturing scale (PCMP-001 §6.2 and @sec-judgement)."
    OR_NAMES = "Version 1.0 also calls it the declared region, and PCMP-001 calls it the design space of the step."
    OR_INSIDE = "The declared region will lie inside the ranges studied, and the normal operating ranges will lie inside the declared region."
    OR_STATES = "PCR-007 states whether they do."
    OR_MARGIN = "PCR-007 will state the margin between the two and will identify the attribute and the parameter that bound the region most tightly."
    OR_WHOLE = "Where the models predict that a criterion is met across the whole studied range of a parameter, that will be reported as the finding, and the range will not be narrowed to manufacture a margin the data do not require."
    OR_YIELD = "Step yield has no quality criterion and does not bound the operating region."
    OR_YIELD2 = "It will be reported as a process performance attribute across the region, and a setting that meets every quality criterion at a cost in yield will be described as such rather than excluded."
    VR_ASSUME = "The criteria upstream of this step assume that cation exchange clears each attribute at least as well as its platform worst case, the lowest clearance factor seen for X-Mab, Y-Mab and Z-Mab."
    VR_CHECK = "PCR-007 checks those of `{python} s_checked`, which are responses of the designs (PCMP-001 §7.5)."
    VR_LPA = "Leached Protein A is not a response of the designs, so its platform value stands."
    VR_EVAL = "The check evaluates the response-surface model of this step at every combination of NOR low, set-point and NOR high of its `{python} k` factors, which are the NOR and the set-points the studies were planned against."
    VR_CF = "For the check, the clearance factor is the level that the nominal batch of the process model brings to this step, divided by the pool level that the response-surface model predicts."
    VR_GIVES = "The model gives the worst clearance factor that it predicts over these combinations, and the one-sided `{python} s_vb` prediction bound of a single batch at the least favourable combination, on its unfavourable side."
    VR_CONF = "The assumption that cation exchange clears an attribute at least as well as its platform worst case is confirmed when that worst predicted clearance factor is no lower than the platform worst case."
    VR_EDGE = "The values observed at the edges of the ranges studied, against the same nominal feed, are reported beside it for information."
    VR_1 = "Where the worst clearance factor predicted within the NOR is lower than the platform worst case, the prediction bound of a single batch replaces the platform value."
    VR_STRICT = "Every criterion upstream for that attribute is recalculated with it and becomes stricter."
    VR_2 = "Where the prediction bound of a single batch is better than the platform value, and the response-surface model behind it meets the first three adequacy criteria of @sec-adequacy (a significant model, no significant lack of fit and the limit on overfitting) and is not an exact fit, the bound replaces the platform value."
    VR_4TH = "The fourth criterion, on the residuals and on influential runs, does not decide the change."
    VR_EXAM = "PCR-007 examines the bound and states whether it depends on a single run."
    VR_WIDER = "Every criterion upstream for that attribute is recalculated with it and becomes wider."
    VR_3 = "Otherwise the platform value stands."
    VR_POINT = "The point prediction never replaces a platform value, and neither does a confidence bound of the mean, because each worst case concerns a quality attribute, which is judged on a single batch, and the platform value it may replace was itself the result of a single run."
    VR_ARGUE = "A report whose check changes a criterion argues the change by its risk (PCMP-001 §7.5)."
    VR_WHO = "It states who bears the risk, the patient or the producer."
    VR_DET = "It states whether an excursion of the step output beyond the changed criterion would be detected, and where, by an in-process test or by a release test."
    VR_DOWN = "It states what the downstream steps must then clear, and it gives the probability that the drug substance fails its specification in the integrated model of the train."
    CL_RULE = "A parameter will be classified under SOP-4001 from two things together, the size of the effect the study demonstrates on a quality attribute and the risk that the parameter moves outside the declared region in manufacture"
    CL_WC = "A parameter linked to a quality attribute and held comfortably inside the region by the commercial control system is a well-controlled critical process parameter."
    CL_CPP = "A parameter linked to a quality attribute whose control is narrow relative to the region is a critical process parameter."
    CL_KPP = "A parameter that changes yield or another performance attribute without changing a quality attribute is a key process parameter."
    CL_GPP = "A parameter that changes neither over the range studied is a general process parameter."
    CL_OUT = "The classifications themselves are outcomes and are reported in PCR-007."
    CL_TWO = "PCMP-001 Version 2.0 adds two rules to this one."
    CL_LINK = "A parameter is linked to an output, or affects it, when a term that contains the parameter is significant at α = `{python} alpha` (PCMP-001 §6.2)."
    CL_SIZE = "PCR-007 states the size of each effect across the PAR beside its significance, and the margin of the PAR to the NOR, and gives the reason for each class on those values (PCMP-001 §7.7)."
    CL_WORDS = 'Neither PCMP-001 nor SOP-4001 sets a numerical threshold for "held comfortably inside" or "narrow", so these two values are what the words are judged on.'
    CL_FLOW = 'For `{python} nm["flow"]` the range is the one that its univariate assessment supports (@sec-par).'

    # Proven acceptable ranges (planned analysis)
    PA_EACH = "A proven acceptable range will be determined for each parameter of the multivariate design against the aggregate, the host cell protein and the fragment content of the pool."
    PA_CRIT = "The criterion applied is the intermediate acceptance criterion for that attribute in @tbl-iac, so a proven acceptable range in this study is the range of a parameter over which the fitted model predicts that the eluate pool meets the level the step must hand on."
    PA_FLOW = '`{python} Nm["flow"]` is not a parameter of the multivariate design.'
    PA_FLOW2 = "Its range is supported by its own data, from the univariate assessment of @sec-univariate, as PCMP-001 §4 provides for a parameter studied one factor at a time."
    PA_NORULE = "Version 1.0 set no rule for judging that range against the criteria."
    PA_NOFRAG = "The flow-rate study measures no fragments, so its data do not support the range for fragments."
    PA_BOTH = "PCR-007 states the approach it takes for both."
    PA_TWO = "Two analyses will be run for every pair of parameter and attribute, and both will be reported."
    PA_FIRST = "The first evaluates the response-surface model across the studied range of the parameter with the other `{python} W(k - 1)` factors held at the centre of the design, which for every parameter of this step is its set-point (@tbl-params)."
    PA_TARGET = "It answers what one parameter can do while the rest of the step is at target."
    PA_SECOND = "The second propagates the normal operating ranges of the other `{python} W(k - 1)` factors."
    PA_GRID = "At each of `{python} s_grid` settings across the studied range of the parameter, `{python} s_mc` draws will be taken with the other factors distributed within their normal operating ranges, and the model will be evaluated at every draw."
    PA_ROUTINE = "The second analysis is the one that bounds routine operation."
    PA_NARROW = "It will in general return the narrower of the two ranges, because a setting that is acceptable with the rest of the step at target need not be acceptable when the rest of the step sits anywhere inside its normal operating ranges."
    PA_NAMES = "PCMP-001 Version 2.0 calls the first the set-point analysis and the second the NOR-propagated analysis (PCMP-001 §6.4)."
    PA_MEAN = "The set-point analysis judges the mean prediction at manufacturing scale."
    PA_DRAW = "In the NOR-propagated analysis each other factor is drawn from a normal distribution centred on its set-point, with a standard deviation of `{python} s_div` of the width of its NOR, and clipped to the studied range."
    PA_SPANS = "This assumes that the NOR spans ±`{python} s_ksd` standard deviations of the routine variation of the parameter."
    PA_COEF = "Each draw also takes its own set of fitted coefficients from their estimated sampling distribution, and its own residual, so the interval includes the model residual and the uncertainty of the coefficients."
    PA_PCT = "The `{python} s_pi` prediction interval of a single batch runs from the `{python} s_pct_lo`th to the `{python} s_pct_hi`th percentile of the simulated batches, and a setting is accepted where the `{python} s_pct_hi`th percentile, at manufacturing scale, does not exceed the criterion."
    PA_CLAIM = "The NOR-propagated PAR is the one that supports a claim."
    PA_CONT = "The reported proven acceptable range is the contiguous interval containing the set-point over which the criterion is met."
    PA_NONCONT = "Where the acceptable settings are not contiguous, the contiguous part containing the set-point will be reported and PCR-007 will state that this has been done."
    PA_WHOLE = "Where the criterion is met across the whole studied range, the proven acceptable range is the studied range, and the claim is bounded by that range and no wider."
    PA_INTER = "A parameter that affects several attributes has a PAR for each, and the range carried into the control strategy is their intersection."
    PA_NOPAR = "Where an output does not meet its criterion even at the set-point, PCR-007 reports that no PAR exists for that output and states the consequence for the NOR (PCMP-001 §7.6)."
    PA_PLOT = "Each output with a criterion in @tbl-iac will be reported with a plot of the predicted response against the parameter carrying the largest main effect on it, with the acceptable region shaded, the set-point marked and the normal operating range marked."
    PA_SEED = "The Monte Carlo component uses the fixed seed `{python} s_seed`, so a repeat of the analysis on the recorded data returns the same ranges."
    PA_ONE = "A proven acceptable range is a statement about one parameter while the others are held at defined settings."
    PA_REGION = "The operating region is a statement about the `{python} k` factors together, and a combination of settings that are each inside their proven acceptable range may still fall outside the region where an interaction is active."
    PA_BUILT = "Both will be reported, and the control strategy will be built on the region."
    # Data management and integrity
    D_ALCOA = "Data generated under this plan will be recorded and retained under the ALCOA+ principles, so that every result is attributable, legible, contemporaneous, original and accurate, and so that the record is complete, consistent, enduring and available."
    D_ELN = "Run conditions and observations will be recorded in the electronic laboratory notebook at the time of execution."
    D_CDS = "Chromatograms and their integration will be retained in the chromatography data system under audit trail."
    D_TRANS = "Analytical results will be transferred from the validated instrument systems into the study dataset without manual transcription wherever the systems support it, and any manual entry will be verified by a second person."
    D_RET = "The analysis dataset, the analysis scripts and the fitted models will be retained with the report, so that every number in PCR-007 can be traced to the run that produced it."
    D_CORR = "A recorded value may be changed after review only under the correction procedure, with the original value, the reason and the author retained."
    D_DEV = "Deviations from this plan will be recorded as they occur and will be reported in PCR-007 with their investigation, their root cause and their impact on the conclusions, whether or not a conclusion changes as a result."
    D_DISC = "Work that this plan does not foresee, and that no revision of it covers, is a discrepancy from the plan and not a deviation."
    D_REC = "PCR-007 records each discrepancy with what the plan foresaw, what was done and why."
    D_DATE = "The date of every laboratory run is recorded, so that the execution window of each study is part of the record (@sec-schedule)."
    # Roles and responsibilities
    RO_OWN = "Process Development and MSAT own this plan."
    RO_DO = "They design the studies, execute the runs on the scale-down model, analyse the data and author PCR-007."
    RO_OTHER = "The other functions in @tbl-roles review and approve within their own competence, and no function approves its own work."
    RO_PERSON = "A role may be held by more than one person, and one person may hold more than one role, provided that the person who reviews an analysis is not the person who performed it."
    RO_NAMES = "The names of the individuals holding each role at execution are recorded in the study file rather than in this plan, so that a change of personnel does not require a revision of the plan."
    # Deliverables and schedule
    SH_DELIV = "The deliverable of this plan is PCR-007."
    SH_REPORT = "It will report the execution of every study described here, the models fitted to the data, the operating region, the proven acceptable ranges, the capability estimate and the classification of each parameter."
    SH_CARRY = "It will also carry the design matrices as executed, including any run that was repeated, and every deviation recorded during the campaign."
    SH_ROLL = "PCR-007 rolls up into PCMR-001, which consolidates the characterization of the whole train."
    SH_V2 = "Under Version 2.0, PCR-007 also reports the offsets of the scale-down model and its qualification for each output, the verification of the platform worst cases of this step and every discrepancy from this plan."
    SH_FIVE = "The work runs in five phases."
    SH_Q = "The qualification runs of the scale-down model are made first, and no characterization run is executed until they are complete and the offsets estimated."
    SH_SCR = "The screening study follows, and its analysis identifies the factors and interactions that change each response."
    SH_RSM = "The response-surface study follows the screening analysis."
    SH_UNI = 'The univariate assessment of `{python} nm["flow"]` may run in parallel with either designed study, since it shares no material or equipment constraint with them.'
    SH_LAST = "Analysis, the proven acceptable range determination and the capability estimate are performed on the complete dataset, and the report is authored last."
    SH_PTP = "The schedule is held in PTP-001, which sequences this study against the other characterization studies of the campaign and against the Stage 2 activities that depend on them."
    SH_PAR = "The univariate assessment ran in parallel with the response-surface study."
    SH_EQ = '''The record names an instrumented system for the response-surface study only, the `{python} eq.loc[rsm_eq, "description"] + " " + rsm_eq`, one of the systems that PCMP-001 §5 lists under calibration and change control.'''
    SH_CAL = '''The chamber was in calibration for the whole study, which closed on `{python} S.loc["rsm", "end"]`, before its next calibration fell due on `{python} cal_due`.'''
    # Risks and assumptions
    RK_FOUR = "Four risks to the study are recognized, and each carries a response."
    RK_SDM = "The scale-down model may fail to represent the commercial column in a respect the qualification does not test."
    RK_CMP = "The qualification of @sec-sdm compares the attributes that enter and leave the step."
    RK_FLOW = "It does not compare the flow distribution inside the two columns, which plate count and peak asymmetry bound only indirectly."
    RK_LATER = "Should a difference in packing quality or flow distribution be identified later, the affected conclusions would have to be revisited at scale."
    RK_FEED = "The feed material may not be representative."
    RK_LOAD = "The load for these studies is the neutralized pool of the low-pH viral inactivation step, and its aggregate and host cell protein content set the starting point of every clearance the study measures."
    RK_MEAS = "Load attributes will be measured on every run and reported with the results, so that a clearance can be distinguished from a low starting level."
    RK_TREND = "Where a lot proves out of trend on any load attribute, the runs performed on it should be identified in PCR-007 and their influence on the fitted models assessed."
    RK_RESIN = "The resin may behave differently at a different point in its life cycle."
    RK_CYCLE = "All characterization runs will be performed on resin within the cycle count qualified under SOP-2008, and the conclusions of this study are bounded by that cycle count."
    RK_END = "Performance at the end of the qualified life is established by the life cycle study and not here."
    RK_ASSAY = "Assay variability may obscure a small effect."
    RK_SPREAD = "The centre point replicates give the reproducibility of each response under study conditions, and an effect smaller than that spread will not be claimed."
    RK_THREE = "Three assumptions are made."
    RK_A1 = "The first is that the platform mechanisms apply to A-Mab at this step, which the designs will test against the expectations of @sec-uo rather than assume."
    RK_A2 = "The second is that the parameters in @tbl-params are the parameters that matter, which the risk assessment RA-001 established and which this study can test only within its own factor set."
    RK_A3 = "The third is that a quadratic model describes the responses adequately over the studied ranges, which the lack of fit test of @sec-adequacy tests directly."
    RK_TWO = "Version 2.0 adds two assumptions."
    RK_A4 = "The fourth is that the NOR of each parameter spans ±`{python} s_ksd` standard deviations of its routine variation, on which the NOR-propagated analysis rests (@sec-par)."
    RK_A5 = "The fifth is that fragments separate in the same way at both scales, so that their judgement without an offset holds at manufacturing scale (@sec-sdm)."
    RK_KEEP = "The scale-down column keeps the bed height, the linear velocity and the collection thresholds of the commercial column, and its packing passes the same tests of plate count and peak asymmetry."
    # Approvals and appendices
    AP_BY = "This plan is approved by the functions recorded in the approval record at the front of this document."
    AP_EXEC = "Execution may begin once the plan is approved and the qualification runs of @sec-sdm have been made and the offsets estimated."
    AP_CHANGE = "Any change to the design, to the ranges or to the acceptance criteria after approval requires a revision of this plan carrying the same approvals, and the revision should be approved before the affected runs are executed."
    AP_CA2 = "This Version 2.0 is the amendment that INV-001 required as its corrective action CA2."
    AP_DATE = "It was issued after the runs and approved on its effective date, `{python} v2_date`."
    AA_GIVES = "@tbl-matrix-screening gives the planned screening design, in the coded levels and the letter codes of @tbl-factors, with −1 and +1 at the edges of the studied range of each factor."
    AA_LABELS = "The run numbers are labels rather than an execution sequence, since execution order will be randomized."
    AB_CORNERS = "The factorial runs repeat the corners of the screening design, and the axial runs sit on the faces of the cube at the edge of each factor's studied range."

    # ==== the step, the equipment and the sites ===================================================
    sdm_name = "laboratory column, the scale-down model of the commercial column"
    column_name = "commercial column"
    chamber_id = ns["rsm_eq"]                                      # the system the record names
    chamber_name = f"{ns['eq'].loc[chamber_id, 'description']} {chamber_id}"
    step = S.ProcessStep(
        step_id=STEP_ID, step_name=UO_NAME, step_number=str(ns["STEP"]), unit_operation=UO_NAME,
        description=(f"Step {ns['STEP']} of the A-Mab drug substance train and its principal polishing "
                     f"operation, operated in bind and elute mode. Below its isoelectric point the "
                     f"antibody binds the sulfonate ligand of the resin, and it is eluted by raising the "
                     f"pH of the elution buffer. Aggregate is retained more strongly and elutes later "
                     f"than monomer, so the step is the principal aggregate polishing operation of the "
                     f"train. Host cell protein, DNA and leached Protein A carry a net negative charge at "
                     f"the load pH and are cleared. The feed is the neutralized pool of the low-pH viral "
                     f"inactivation step, and the eluate pool carries every response of the study."),
        input_materials=["neutralized pool of the low-pH viral inactivation step"],
        output_materials=["eluate pool"],
        equipment=[sdm_name, column_name, chamber_name],
        source_references=[ref("purpose", q(P_SCOPE)), ref("uo", q(U_MODE)), ref("uo", q(U_BIND)),
                           ref("purpose", q(P_FEED)), ref("sampling", q(SP_POOL))],
        metadata=meta())
    eq_sdm = S.Equipment(
        equipment_id=SDM_ID, equipment_name=sdm_name,
        equipment_type="chromatography column (scale-down model)", site_name=P.SENDING_SITE,
        source_references=[ref("sdm", q(S_COL)), ref("sdm", q(S_PACK))], metadata=meta())
    eq_col = S.Equipment(
        equipment_id=COLUMN_ID, equipment_name=column_name,
        equipment_type="chromatography column (manufacturing scale)", site_name=P.RECEIVING_SITE,
        source_references=[ref("purpose", q(P_COLUMN)), tref("roles", ro_t, rorow, recv)],
        metadata=meta())
    eq_ch = S.Equipment(
        equipment_id=f"equip:{chamber_id}", equipment_name=chamber_name,
        equipment_type="instrumented chromatography system (scale-down)", site_name=P.SENDING_SITE,
        source_references=[ref("schedule", q(SH_EQ)), ref("schedule", q(SH_CAL))], metadata=meta())
    equipment = [eq_sdm, eq_col, eq_ch]

    # ==== parameters: each on its row of the parameter table (and of the coded factor table) ====
    pp = ns["pp_tab"].set_index("Parameter")                      # the frame the parameter table shows
    params = []
    for name in prow:
        p, r = prm[name], pp.loc[name]
        refs = [tref("factors", pt, prow, name)]
        if name in frow:                    # the multivariate factors also have their code row
            refs.append(tref("factors", ft, frow, name))
        params.append(S.ProcessParameter(
            parameter_id=PC[name], parameter_name=name, parameter_type="unclassified", unit=p.unit,
            target_value=f"{r['Set-point']} {p.unit}", NOR=f"{r['NOR']} {p.unit}",
            PAR=f"{r['Range studied']} {p.unit}", associated_step=STEP_LABEL, study_type=p.study,
            source_references=refs, metadata=meta()))

    # ==== analytical methods: each on its sentence and its row of the procedures table ==========
    amvs = [a for a in sop_df["Reference"] if a.startswith("AMV-")]
    q_method = {"AMV-3011": M_AGG, "AMV-3012": M_HCP, "AMV-3014": M_DNA, "AMV-3016": M_LPA,
                "AMV-3020": M_FRAG}
    if set(q_method) != set(amvs) or any(a not in s_ for a, s_ in q_method.items()):
        raise ValueError(f"{DOC}: the method sentences do not name the validations {amvs}")
    analyte = {"AMV-3011": "pool aggregate, as the percentage of high molecular weight species",
               "AMV-3012": "host cell protein, per milligram of antibody",
               "AMV-3014": "residual DNA", "AMV-3016": "leached Protein A", "AMV-3020": "fragments"}
    attrs_of = {a: [k for k in G.METHOD_ATTRS[a] if k in ckeys] for a in amvs}
    method_of = {k: a for a, ks in attrs_of.items() for k in ks}
    if set(method_of) != set(ckeys):
        raise ValueError(f"{DOC}: an attribute in scope has no method of the procedures table")
    methods = [S.AnalyticalMethod(
        method_id=a, method_name=title_of[a], method_type=G.METHOD_TYPE.get(a), analytes=[analyte[a]],
        associated_attributes=[f"attr:{k}" for k in attrs_of[a]], validation_status="validated",
        source_references=[ref("methods", q(q_method[a])), tref("related", sop_t, soprow, a)],
        metadata=meta()) for a in amvs]

    # ==== quality attributes: each on its row of the attribute table ============================
    acc_of = dict(zip(ckeys, ns["cq"]["Acceptance"]))
    attr_prose = {"aggregates_hmw": [("cqa", Q_AGG)], "fragments_lmw": [("cqa", Q_FRAG)],
                  "hcp": [("cqa", Q_HCP)], "residual_dna": [("cqa", Q_DNALPA)],
                  "leached_protein_a": [("cqa", Q_DNALPA), ("uo", U_LPA2)]}
    attrs = []
    for key in ckeys:
        r = reg.loc[key]
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=r["cqa"], attribute_type="CQA", unit=r["unit"],
            acceptance_criteria=[f"{acc_of[key]} (drug substance)"], analytical_method=method_of[key],
            associated_steps=[STEP_LABEL],
            rationale_for_criticality=(f"Assigned with Tool #1 of the A-Mab case study, which combines the "
                                       f"impact of the attribute on safety and efficacy with the "
                                       f"uncertainty in that impact; Tool #1 score {r['tool1_score']}."),
            criticality_level=r["criticality"], tool1_score=int(r["tool1_score"]),
            tool2_severity=int(r["tool2_severity"]),
            source_references=[tref("cqa", cq_t, crow, key)] + [ref(s_, q(x)) for s_, x in attr_prose[key]],
            metadata=meta()))

    # ==== explicit non-claims =====================================================================
    nc, nc_at = [], {}

    def nclaim(sec, subject, statement, quotes, rationale=None, elsewhere=None):
        """``quotes``: (section, .qmd span) pairs; the non-claim is filed under section ``sec``."""
        nc.append(ExplicitNonClaim(
            non_claim_id=f"{DOC}-NC{len(nc) + 1:02d}", subject=subject, unit_operation=UO_NAME,
            statement=statement, rationale=rationale, handled_elsewhere=elsewhere,
            source_references=[ref(s_, q(x)) for s_, x in quotes], metadata=meta()))
        nc_at.setdefault(sec, []).append(nc[-1])

    nclaim("purpose", "attributes of the feed",
           "The attributes of the feed, the neutralized pool of the low-pH viral inactivation step, are "
           "inputs to the study and not factors of it.", [("purpose", P_FEED)])
    nclaim("purpose", "resin life cycle, sanitization and repacking",
           "Resin life cycle, sanitization and repacking lie outside the plan; the studies are run on resin "
           "inside the life qualified under SOP-2008.",
           [("purpose", P_THREE), ("purpose", P_RESIN)], elsewhere="SOP-2008")
    nclaim("purpose", "validation of the analytical methods",
           "Validation of the analytical methods lies outside the plan, which uses the methods as validated.",
           [("purpose", P_THREE), ("purpose", P_AMV)], elsewhere="the method validation reports")
    nclaim("purpose", "confirmation of the ranges at commercial scale",
           "Confirmation of the ranges at commercial scale lies outside the plan.",
           [("purpose", P_THREE), ("purpose", P_STAGE2)],
           elsewhere="Stage 2 and the process performance qualification batches")
    nclaim("purpose", "viral clearance", "No viral clearance claim is made for the cation exchange step.",
           [("purpose", P_NOVIRAL), ("purpose", P_CLAIMS), ("purpose", P_PCMR)],
           elsewhere="the low-pH viral inactivation, anion exchange and virus filtration steps, consolidated "
                     "in PCMR-001")
    nclaim("changes", "corrective actions of INV-002",
           "The corrective actions of INV-002 (the augmentation of the designs its rule names, the refit of "
           "every other failing model and the selection of the model of every output) are not applied in "
           "the plan.", [("changes", CH_INV2C), ("changes", CH_INV2D)], elsewhere="PCR-007")
    nclaim("cqa", "quality attribute assigned to the step",
           "The drug substance register of CQAs assigns no quality attribute to the cation exchange step.",
           [("cqa", Q_REG)],
           rationale="The attributes in scope are formed upstream: aggregate in the production bioreactor "
                     "and during the low-pH hold, host cell protein and DNA with the harvested cell culture "
                     "fluid, leached Protein A at the capture resin, fragments in culture and during the "
                     "harvest hold. The step removes them.")
    nclaim("cqa", "residual DNA and leached Protein A as responses of the designs",
           "Residual DNA and leached Protein A are measured across the step to confirm their clearance, but "
           "neither is a response of the designed experiments, and no parameter dependence is claimed for "
           "either unless the data show one.", [("cqa", Q_DNALPA), ("cqa", Q_DEP)],
           rationale="DNA is repelled by the sulfonate ligand at every conductivity and pH studied, and free "
                     "leached Protein A stays unbound over the same range.",
           elsewhere="PCR-007 (the clearance observed for both)")
    nclaim("cqa", "acceptance criterion for step yield",
           "Step yield has no acceptance criterion; it is a process performance attribute.",
           [("cqa", Q_YIELD3), ("cqa", Q_YIELD1)])
    nclaim("risk", "parameters fixed by equipment design or held to platform specification",
           "Parameters fixed by equipment design or held to platform specification, such as bed height, "
           "column packing quality and buffer composition, are not assigned a new study.",
           [("risk", R_FIXED), ("risk", R_FIXED2)],
           rationale="Their ranges are supported by the platform knowledge space and by the operation and "
                     "life cycle procedures.")
    nclaim("sdm", "scale-down offset of fragments",
           "Fragments are not compared at both scales; their offset is unknown, not zero, and they are "
           "judged as the scale-down model gives them.", [("sdm", S_NOFRAG), ("sdm", S_UNK)],
           rationale="The judgement rests on the assumption that fragments separate in the same way at both "
                     "scales.")
    nclaim("sdm", "hold times, pool volumes and mixing of the commercial suite",
           "The scale-down column does not reproduce the hold times, the pool volumes or the mixing of the "
           "commercial suite.", [("sdm", S_NOTREP), ("sdm", S_APPLY)],
           elsewhere="confirmation at scale during Stage 2")
    nclaim("operation", "buffer preparation, column packing and resin storage",
           "Buffer preparation, column packing and resin storage are held to platform specification and are "
           "inputs to the study, not factors of it.", [("operation", O_INPUTS), ("operation", O_NOTF)])
    nclaim("operation", "chromatography temperature",
           "Temperature is not varied; chromatography is performed at controlled room temperature.",
           [("operation", O_TEMP)],
           rationale="The platform operates the step under the same control at both sites and the transfer "
                     "introduces no difference in that control.")
    nclaim("methods", "SEC fragment results",
           "Fragments are not judged on SEC results; they are judged on the nrCE-SDS results only.",
           [("methods", M_ONLY), ("changes", C2_D)],
           rationale="SEC reads fragments high in samples that still carry host cell protein (INV-001 "
                     "finding 6).")
    nclaim("methods", "effect within assay variability",
           "No effect is claimed where a predicted value sits within assay variability of its criterion; "
           "the result is attributed to the assay.", [("methods", M_ATTR)], elsewhere="PCR-007")
    nclaim("stats", "predictions from the screening model",
           "The screening model is not the predictive model of the step; the operating region, the proven "
           "acceptable ranges and the capability estimate are derived from the response-surface model.",
           [("stats", T_NOTPRED)], rationale="A model without quadratic terms cannot describe curvature.")
    nclaim("stats", "absence of effect in general",
           "A factor with no significant term in either model is reported as having no demonstrated effect, "
           "bounded by the range studied and the power of the design, and not as an absence of effect in "
           "general.", [("stats", T_NOEFF), ("stats", T_BOUNDED)])
    nclaim("stats", "minimum capability index for the outputs of the step",
           "No minimum capability index is set as an acceptance criterion for the outputs of the step.",
           [("stats", T_NOCPK), ("changes", C9_B)],
           elsewhere="PCMR-001, against the thresholds of PCMP-001 §7.9 for the drug substance")
    nclaim("univariate", "interaction of elution flow rate with the other parameters",
           "The univariate assessment cannot determine whether elution flow rate interacts with the other "
           "parameters, and no interaction is expected.", [("univariate", V_INT), ("univariate", V_WHY)],
           rationale="Flow rate changes the residence time of the antibody in the pores of the resin and the "
                     "sharpness of the elution peak, not the net charge on the antibody or the ionic strength "
                     "that sets how strongly it is held.")
    nclaim("criteria", "numerical thresholds for the words of Version 1.0",
           "Several decisions of Version 1.0 rest on words with no numerical threshold, and Version 2.0 sets "
           "none either.", [("criteria", CR_WORDS), ("criteria", CR_NONE)], elsewhere="PCR-007")
    nclaim("iac", "criteria for residual DNA, leached Protein A and step yield at the step",
           "Residual DNA, leached Protein A and step yield have no criterion at the cation exchange step, so "
           "no range is derived from them.", [("iac", I_NONE)])
    nclaim("iac", "DNA criterion carried back to the step",
           "No DNA criterion is carried back to the cation exchange step; residual DNA is judged on the drug "
           "substance only.", [("iac", I_NODNA)],
           rationale="The platform history gives no worst-case DNA clearance for the steps after Protein A.",
           elsewhere="the drug substance")
    nclaim("region", "step yield in the operating region",
           "Step yield does not bound the operating region; it is reported as a process performance "
           "attribute across the region.", [("region", OR_YIELD), ("region", OR_YIELD2)])
    nclaim("verification", "verification of the leached Protein A platform worst case",
           "The leached Protein A platform worst case of the step is not checked; its platform value stands.",
           [("verification", VR_LPA)], rationale="Leached Protein A is not a response of the designs.")
    nclaim("verification", "point prediction or confidence bound in the verification",
           "Neither the point prediction nor a confidence bound of the mean replaces a platform value.",
           [("verification", VR_POINT)],
           rationale="Each worst case concerns a quality attribute, judged on a single batch, and the platform "
                     "value it may replace was itself the result of a single run.")
    nclaim("classification", "classification of the parameters",
           "The plan classifies no parameter; the classifications are outcomes.",
           [("classification", CL_OUT)], elsewhere="PCR-007")
    nclaim("par", "range of elution flow rate for fragments",
           "The data of the flow-rate study do not support a range of elution flow rate for fragments.",
           [("par", PA_NOFRAG)], rationale="The flow-rate study measures no fragments.")
    nclaim("par", "proven acceptable range beyond the studied range",
           "Where the criterion is met across the whole studied range, the proven acceptable range is the "
           "studied range and no wider.", [("par", PA_WHOLE)])
    nclaim("risks", "flow distribution inside the columns",
           "The qualification does not compare the flow distribution inside the scale-down and the commercial "
           "column, which plate count and peak asymmetry bound only indirectly.",
           [("risks", RK_FLOW), ("risks", RK_LATER)])
    nclaim("risks", "performance at the end of the qualified resin life",
           "Performance at the end of the qualified resin life is not established by the study, whose "
           "conclusions are bounded by the qualified cycle count.", [("risks", RK_END), ("risks", RK_CYCLE)],
           elsewhere="the life cycle study")
    nclaim("risks", "effect smaller than the centre point spread",
           "An effect smaller than the centre point spread of a response will not be claimed.",
           [("risks", RK_SPREAD)])

    # ==== document relationships: the rows of the related-documents table, then the prose ========
    rels = []

    def relation(kind, target, statement, sec, quote, rows=None, caption=None, label=None):
        rels.append(DocumentRelationship(
            relationship_id=f"{DOC}-R{len(rels) + 1:02d}", kind=kind, source_document_id=DOC,
            target_document_ref=target, statement=statement,
            source_references=[ref(sec, quote, rows=rows, caption=caption, label=label)], metadata=meta()))

    for target, row in rel.items():
        txt = _cells(row)[-1]
        relation(REL_KIND.get(txt, "references"), target, txt, "related", row, rows=rel, caption=rel_cap,
                 label="tbl-related")
    relation("supersedes", f"{DOC} Version {P.REV1['rev']}", "Version 2.0 supersedes Version 1.0 of the plan.",
             "title", tb["Supersedes"], rows=tb)
    relation("scoped_by", "RA-001", "The risk assessment RA-001 set the scope of the study, and the plan "
             "executes that scope.", "related", q(REL_RA))
    relation("references", "PTP-001", "The A-Mab drug substance process is transferred to the commercial site "
             "under the Process Transfer Plan PTP-001.", "purpose", q(P_TRANSFER))
    relation("references", "PCMR-001", "The cumulative viral clearance claim is consolidated in the master "
             "report PCMR-001.", "purpose", q(P_PCMR))
    relation("references", "INV-001", "Version 2.0 is issued under the Quality Assurance investigation INV-001.",
             "changes", q(CH_INV1))
    relation("references", "INV-002", "The plan is reissued under INV-002 as well, the investigation of the "
             "response-surface models below the model adequacy criteria of PCMP-001 §7.2.", "changes",
             q(CH_INV2))
    relation("references", ns["AMD"]["id"], "The analytical method decision under which every study that "
             "measures fragments, at every step, measures them by nrCE-SDS.", "methods", q(M_AMD))
    relation("references", "PCR-008", "The anion exchange report verified the platform worst case of anion "
             "exchange for host cell protein, and its bound sets the host cell protein criterion of the step.",
             "iac", q(I_PCR8))
    relation("references", "PCR-007", "PCR-007 is the deliverable of the plan.", "schedule", q(SH_DELIV))
    relation("references", "PCMR-001", "PCR-007, the deliverable of the plan, rolls up into PCMR-001, which "
             "consolidates the characterization of the whole train.", "schedule", q(SH_ROLL))
    relation("references", "PTP-001", "The schedule of the study is held in PTP-001.", "schedule", q(SH_PTP))

    # ==== studies: each on its row of the execution-window table, its prose and its matrix ========
    mv_names = [pkey[k].name for k in ns["mv"]]
    uv_names = [pkey[k].name for k in ns["uv"]]
    resp = list(D.responses(UO))
    uv_resp = re.split(r", | and ", ns["uv_resp"])                # the responses as the plan lists them
    design = {
        # no n_runs: the qualification compares scale-down runs with manufacturing-scale batches,
        # which is not a design (tests/test_config.py matches n_runs against the seeded designs)
        "qualification": dict(
            responses=["step yield", "pool aggregate", "pool host cell protein", "residual DNA",
                       "leached Protein A", "plate count", "peak asymmetry"],
            refs=[("sdm", S_QRUNS), ("sdm", S_QCMP), ("sdm", S_QN), ("sdm", S_PLATE)]),
        "screening": dict(
            design_name="two-level full factorial with centre points", factors=mv_names,
            responses=resp,                 # the plan names no fragment response of the screening design
            n_runs=int(ns["n_scr"]), n_center_points=int(ns["cp_scr"]),
            refs=[("screening", C_DESIGN), ("screening", C_EST), ("sampling", SP_CP)]),
        "rsm": dict(
            design_name="face-centred central composite design", factors=mv_names,
            responses=resp + [ns["FRAG"]],  # fragments by nrCE-SDS, the only fragment result judged
            n_runs=int(ns["n_rsm"]), n_center_points=int(ns["cp_rsm"]),
            refs=[("rsm", RS_DESIGN), ("rsm", RS_FACES), ("sampling", SP_CP)]),
        "univariate": dict(
            design_name="one factor at a time: the low edge, the set-point and the high edge of the range "
                        "studied, every other parameter at its set-point",
            factors=uv_names, responses=uv_resp,
            refs=[("univariate", V_ONE), ("univariate", V_RUNS), ("schedule", SH_PAR)]),
    }
    studies, unrendered, skipped = [], [], []
    for r in ns["mine"].itertuples():
        stype = G.STUDY_TYPE.get(r.kind)
        if stype is None:
            skipped.append(r.id)
            continue
        if not G._present(wrow[r.id], text):
            unrendered.append(r.id)
            continue
        d = dict(design[r.kind])
        refs = [tref("schedule", w_t, wrow, r.id)] + [ref(s_, q(x)) for s_, x in d.pop("refs")]
        if r.kind in mtx:                   # every row of its planned design matrix
            mt_, mrows = mtx[r.kind]
            refs += [tref("app_a" if r.kind == "screening" else "app_b", mt_, mrows, k_) for k_ in mrows]
        studies.append(S.StudyDesign(
            study_id=f"study:{r.id}", study_type=stype, unit_operation=UO_NAME, scale_down_model=sdm_name,
            associated_parameters=[PC[x] for x in d.get("factors", [])], source_references=refs,
            metadata=meta(), **d))
    if skipped:
        raise ValueError(f"{DOC}: studies of the plan with no study type: {skipped}")

    # ==== entities, by section ====================================================================
    def section(key, **kw):
        return S.SectionEntityExtraction(document_id=DOC, section_id=_sid(key),
                                         non_claims=nc_at.get(key, []), **kw)
    entities = [
        section("purpose", process_steps=[step], sites=G._site_entities(DOC, FILE, _sid("title")),
                equipment=[eq_col]),
        section("changes"),
        section("related", document_relationships=rels),
        section("cqa", quality_attributes=attrs),
        section("risk"),
        section("sdm", equipment=[eq_sdm]),
        section("operation"),
        section("methods", analytical_methods=methods),
        section("stats"),
        section("factors", parameters=params),
        section("univariate"),
        section("criteria"),
        section("iac"),
        section("region"),
        section("verification"),
        section("classification"),
        section("par"),
        section("schedule", equipment=[eq_ch]),
        section("risks"),
    ]
    listed = {n_.non_claim_id for e in entities for n_ in e.non_claims}
    if listed != {n_.non_claim_id for n_ in nc}:
        raise ValueError(f"{DOC}: non-claims filed under a section with no entity record")

    # ==== assertions ==============================================================================
    add(STEP_ID, "step_uses_equipment", SDM_ID,
        "The characterization studies of the cation exchange step are run on a laboratory column packed "
        "with the same resin type and to the same bed height as the commercial column, and operated at the "
        "same linear velocities.", [ref("sdm", q(S_COL))])
    add(STEP_ID, "step_uses_equipment", COLUMN_ID,
        "At commercial scale the cation exchange step runs on the commercial column, of which the studies "
        "use a scale-down model.", [ref("purpose", q(P_COLUMN))])
    add(STEP_ID, "step_uses_equipment", f"equip:{chamber_id}",
        f"The record names the {chamber_name} as the instrumented system of the response-surface study of "
        f"the step.", [ref("schedule", q(SH_EQ))])
    for name in prow:
        add(STEP_ID, "step_has_parameter", PC[name], f"{UO_NAME} has process parameter {name}.",
            [tref("factors", pt, prow, name)])
    role = {"aggregates_hmw": ("removes {n}, which is formed upstream; aggregate is the attribute the step "
                               "exists to control", [("cqa", Q_AGG)]),
            "fragments_lmw": ("clears part of the {n} load, not all of it", [("uo", U_FRAG4)]),
            "hcp": ("clears {n}, which is cleared again at the anion exchange step", [("cqa", Q_HCP)]),
            "residual_dna": ("clears {n}, which is repelled by the ligand and passes through in the load",
                             [("cqa", Q_DNALPA_A), ("uo", U_DNA)]),
            "leached_protein_a": ("clears {n} by a modest factor, because the leached Protein A in complex "
                                  "with the antibody binds with it", [("cqa", Q_DNALPA_A), ("uo", U_LPA2)])}
    for key in ckeys:
        how, prose_ = role[key]
        add(STEP_ID, "step_has_quality_attribute", f"attr:{key}",
            f"{UO_NAME} " + how.format(n=names[key]) + ".",
            [tref("cqa", cq_t, crow, key)] + [ref(s_, q(x)) for s_, x in prose_])
    for a in amvs:
        for key in attrs_of[a]:
            add(f"attr:{key}", "attribute_measured_by_method", f"method:{a}",
                f"{names[key]} is measured by {a} ({title_of[a]}).",
                [ref("methods", q(q_method[a])), tref("related", sop_t, soprow, a)])
    q_iac = {"aggregates_hmw": I_AGG, "fragments_lmw": I_DS, "hcp": I_FORCE}
    for key in irow:
        x = iac.loc[key]
        unit = re.search(r"\(([^)]*)\)$", T.ATTR_NAME[key]).group(1)  # as the row labels the attribute
        if D.decision_statistic(x["response"]) != "batch":
            raise ValueError(f"{DOC}: {key} is not judged on a single batch, as the plan states")
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{UO}_{key}_iac",
            f"At the cation exchange step, {names[key]} is judged against the Version {P.REV2['rev']} "
            f"intermediate acceptance criterion {T.crit(x['iac_low'], x['iac_high'], x['spec_type'])} {unit} "
            f"({x['basis']}), on a single batch.",
            [tref("iac", iac_t, irow, key), ref("iac", q(q_iac[key]))])
    # the plan's stated expectations from prior knowledge (not results)
    pid = {k: PC[p.name] for k, p in pkey.items()}
    add(pid["load"], "parameter_impacts_attribute", "attr:aggregates_hmw",
        "A higher protein load is expected to lower aggregate clearance: as ligand occupancy rises the "
        "monomer and the aggregate peak broaden and overlap further.",
        [ref("uo", q(E_LOAD3)), ref("uo", q(E_LOAD2)), ref("risk", q(R_WHY))])
    add(pid["load"], "parameter_impacts_attribute", "attr:hcp",
        "A higher protein load is expected to lower host cell protein clearance: a larger share of the host "
        "cell protein is held on the column through its association with the bound antibody, escapes the "
        "wash and elutes with the antibody.",
        [ref("uo", q(E_LOAD3)), ref("uo", q(E_LOAD2)), ref("risk", q(R_WHY_HCP))])
    add(pid["load"], "parameter_impacts_attribute", "attr:step_yield",
        "A higher protein load is expected to lower step yield, together with aggregate and host cell "
        "protein clearance, as the column approaches its dynamic binding capacity.",
        [ref("uo", q(E_LOAD3)), ref("uo", q(E_LOAD1))])
    add(pid["wash_cond"], "parameter_impacts_attribute", "attr:hcp",
        "A higher load/wash conductivity is expected to strip more of the weakly bound host cell protein "
        "during the wash, and to remove more host cell protein at a high load than at a low one.",
        [ref("uo", q(E_COND2)), ref("uo", q(E_INT)), ref("risk", q(R_WHY_HCP))])
    add(pid["wash_cond"], "parameter_does_not_significantly_impact_attribute", "attr:aggregates_hmw",
        "The effect of load/wash conductivity is expected to fall on impurity clearance and not on the "
        "aggregate separation, which happens during elution.", [ref("uo", q(E_COND3))])
    add(pid["elution_ph"], "parameter_impacts_attribute", "attr:aggregates_hmw",
        "A higher elution buffer pH is expected to reduce the resolution on which aggregate clearance "
        "depends, bringing monomer and aggregate off the column earlier and closer together.",
        [ref("uo", q(E_PH2)), ref("risk", q(R_WHY))])
    add(pid["stop_collect"], "parameter_impacts_attribute", "attr:aggregates_hmw",
        "Stopping collection later, at a lower stop collect setting, is expected to carry the leading part "
        "of the aggregate peak into the pool.",
        [ref("uo", q(E_SC2)), ref("uo", q(E_SC3)), ref("risk", q(R_WHY))])
    add(pid["stop_collect"], "parameter_impacts_attribute", "attr:step_yield",
        "Stopping collection later is expected to recover more monomer from the tail of the peak; monomer "
        "that elutes after the stop collect point is lost on the trailing edge.",
        [ref("uo", q(E_SC2)), ref("uo", q(U_YIELD2))])
    add(pid["stop_collect"], "parameter_impacts_attribute", "attr:fragments_lmw",
        "A later stop of collection is expected to lower the fragment content of the pool, because it adds "
        "more of the trailing eluate, which carries few fragments.",
        [ref("uo", q(U_FRAG2)), ref("uo", q(U_FRAG3))])
    add(pid["flow"], "parameter_does_not_significantly_impact_attribute", "attr:aggregates_hmw",
        "Over the range studied, the change in peak sharpness that elution flow rate produces is expected "
        "to be too small to move the aggregate content of the pool.",
        [ref("uo", q(E_FLOW2)), ref("uo", q(E_FLOW1))])

    # ==== plan statements, in document order ======================================================
    # Purpose and scope
    sq("purpose", P_TRANSFER)
    sq("purpose", P_SCOPE, "PCP-007 describes the Stage 1 characterization of the cation exchange chromatography "
                           "step, which is Step `{python} STEP` of the drug substance train and its principal "
                           "polishing operation.")
    sq("purpose", P_COLUMN)
    sq("purpose", P_AIM, "The purpose of the studies is to measure how far the aggregate content, the host cell "
                         "protein content, the fragment content and the yield of the eluate pool move as each "
                         "parameter is varied across its range studied, to define the region over which the pool "
                         "meets its criteria, and to justify the ranges and the controls that will be applied in "
                         "commercial manufacture.")
    sq("purpose", P_COVER, "The scope of PCP-007 covers the `{python} n_par` process parameters of the step, the "
                           "size variant and impurity attributes the step clears, and the step yield.")
    sq("purpose", P_ASSIGN)
    sq("purpose", P_FEED)
    sq("purpose", P_CLAIMS, "No viral clearance claim is made for the cation exchange step: clearance of "
                            "enveloped virus is claimed at the low-pH viral inactivation step, the anion exchange "
                            "step and the virus filtration step, and clearance of small viruses at the anion "
                            "exchange step and the virus filtration step.", also=[("purpose", P_NOVIRAL)])
    sq("purpose", P_CONTRIB)
    # Changes in this revision
    sq("changes", CH_V1, "Version 1.0 of PCP-007 was approved on `{python} v1_date`, before the first study of the "
                         "step started on `{python} first_start`.")
    sq("changes", CH_RAN, "The studies governed by Version 1.0 ran until `{python} last_end`.")
    sq("changes", CH_INV1, 'Version 2.0, effective `{python} v2_date`, is issued after the studies under the '
                           'Quality Assurance investigation INV-001 (`{python} INV["title"]`).')
    sq("changes", CH_OPEN, 'QA opened INV-001 on `{python} INV["opened"]`, after reviewing the master report '
                           'PCMR-001 Version 1.0 for the Biologics License Application.')
    sq("changes", CH_CLOSE, 'QA closed INV-001 on `{python} INV["closed"]` with the classification '
                            '`{python} INV["classification"]`.')
    sq("changes", CH_FOUND)
    sq("changes", CH_CA2, "Version 2.0 carries out corrective action CA2 of INV-001, the amendment of the step "
                          "plans with the criteria and the fragment method.")
    sq("changes", CH_INV2, 'The plan is reissued under INV-002 as well (`{python} INV2["title"]`), the '
                           'investigation of the response-surface models of the campaign that fall below the '
                           'model adequacy criteria of PCMP-001 §7.2.', also=[("changes", CH_INV2B)])
    sq("changes", CH_INV2C, "The corrective actions of INV-002 are the augmentation of the designs that its rule "
                            "names (CA1), the refit of every other failing model (CA2) and the selection of the "
                            "model of every output (CA3); the reports apply them, PCR-007 for this step, and the "
                            "plan does not.", also=[("changes", CH_INV2D)])
    sq("changes", CH_KEEP, "Version 2.0 keeps the design and the sampling of Version 1.0 of the plan, and the "
                           "wording of every Version 1.0 decision rule that PCMP-001 Version 2.0 does not replace.")
    sq("changes", CH_DEPART, "Where a study departed from the design, the sampling or a decision rule of the plan, "
                             "PCR-007 records the departure.")
    sq("changes", CH_TEN, "Each change of Version 2.0 names the Version 1.0 text it replaces; changes 1 to 10 also "
                          "name the rule of PCMP-001 Version 2.0, or the action of INV-001, that they apply, and "
                          "change 11 corrects descriptions of Version 1.0 that were wrong.",
       also=[("changes", CH_NAMES)])
    sq("changes", C1_B, "Change 1, the step criteria are intermediate acceptance criteria: the Version 1.0 reports "
                        "judged the pool against an aggregate limit of `{python} s_agg_v1` % high molecular weight "
                        "species and a host cell protein limit of `{python} s_hcp_v1` ng/mg.",
       also=[("changes", C1_A)])
    sq("changes", C1_C, "Each Version 1.0 limit was the drug substance criterion carried back through the nominal "
                        "clearance of the later steps in the campaign and then divided by a margin, "
                        "`{python} s_agg_mg` for aggregate and `{python} s_hcp_mg` for host cell protein "
                        "(INV-001 finding 2).")
    sq("changes", C1_D, "The Version 1.0 limits were set at analysis and were written into the plan text when the "
                        "package was compiled in `{python} s_compiled`, without a revision of the approved plan "
                        "(INV-001 finding 1).")
    sq("changes", C1_E)
    sq("changes", C1_F)
    sq("changes", C1_G)
    sq("changes", C1_H)
    sq("changes", C1_I, "Because the criteria rest on platform numbers, the unit-operation description no longer "
                        "says that prior knowledge is not carried across as a numerical claim, or that every "
                        "criterion rests on data generated under the plan.")
    sq("changes", C2_B, "Change 2, fragments are judged at this step: Version 1.0 of the plan set no criterion for "
                        "fragments, and the Version 1.0 report did not judge them.", also=[("changes", C2_A)])
    sq("changes", C2_C, 'Version 2.0 judges fragments against the drug substance criterion of `{python} s_frag` % '
                        '(PCMP-001 §7.3), on results by non-reduced capillary electrophoresis with sodium dodecyl '
                        'sulfate (nrCE-SDS) under the analytical method decision `{python} AMD["id"]` (PCMP-001 '
                        '§7.8).')
    sq("changes", C2_D, "The analytical method decision answers INV-001 finding 6, that size exclusion "
                        "chromatography (SEC) reads fragments high in samples that still carry host cell protein.")
    sq("changes", C2_E)
    sq("changes", C3_A, "Change 3: the scale-down model is qualified for each output by its offset, not by a test of "
                        "equivalence.")
    sq("changes", C3_B, 'Version 1.0 of the plan read "the model will be accepted where no statistically '
                        'significant difference is found on any of those attributes" and "Execution may begin once '
                        'the plan is approved and the scale-down model has been accepted under §5.1".')
    sq("changes", C3_C)
    sq("changes", C3_D, "The qualification runs and the offset estimates come before the first characterization "
                        "run, and the decision whether the model is qualified for an output is made at analysis.")
    sq("changes", C3_E, "As PCMP-001 §7.1 requires of each step plan, PCP-007 names the outputs compared, the number "
                        "of runs at each scale and the manufacturing-scale data set.")
    sq("changes", C4_C, "Change 4: Version 1.0 judged a model on four things together, the overall F-test at "
                        "p < `{python} alpha`, the test for lack of fit, the closeness of R², adjusted R² and "
                        "predicted R², for which it set no limit, and an examination of the residuals that "
                        "identified any influential run, with no test and no cut-off.", also=[("changes", C4_B)])
    sq("changes", C4_D, 'Version 2.0 judges model adequacy by the four tests of PCMP-001 §7.2: it sets a limit of '
                        '`{python} f"{gap:.2f}"` on the difference between R² and predicted R², and states the tests '
                        'on the residuals and on influential runs with their thresholds.',
       also=[("changes", C4_A)])
    sq("changes", COOK_2, "Under change 4, a run with a Cook's distance above `{python} s_cook`/n is examined by "
                          "deleting it and repeating the judgement, and the model fails the test on influential "
                          "runs only where a run's Cook's distance exceeds `{python} s_cook_fq` of the F "
                          "distribution with p and n − p degrees of freedom, where p is the number of model "
                          "parameters and n the number of runs.", also=[("changes", COOK_1)])
    sq("changes", C4_E, 'Version 1.0 of the plan read "A response whose model is not adequate will be reported as '
                        'characterized by its data rather than by a model, and no design space and no proven '
                        'acceptable range will be derived from it."')
    sq("changes", C4_F)
    sq("changes", C5_B, "Change 5: the NOR-propagated analysis is the second PAR analysis, which scans one "
                        "parameter while each other parameter is drawn around its set-point across its normal "
                        "operating range (NOR).", also=[("changes", C5_A)])
    sq("changes", C5_D, "Version 1.0 already judged single batches in the NOR-propagated analysis; it drew the "
                        "other factors within their NORs without stating a distribution, and accepted a setting "
                        "where the predicted values met the criterion across the draws.", also=[("changes", C5_C)])
    sq("changes", C5_E)
    sq("changes", C6_B, 'Change 6, the operating region is drawn on the prediction interval of a single run: '
                        'Version 1.0 of the plan read "The operating region will be declared where the fitted '
                        'models predict that both attributes in Table 7.1 meet their in-process criteria, '
                        'evaluated over the studied ranges of the `{python} k` multivariate factors", which judged '
                        'the mean prediction.', also=[("changes", C6_A)])
    sq("changes", C6_C)
    sq("changes", C7_B, "Change 7: PCR-007 checks the platform worst cases of cation exchange on which the criteria "
                        "upstream rely, and the verification rule of PCMP-001 §7.5 decides whether a check tightens "
                        "or widens a criterion.", also=[("changes", C7_A)])
    sq("changes", C7_C)
    sq("changes", C7_D, "Objective 6, to verify the platform worst cases, and the verification in the deliverables "
                        "are added for the check.")
    sq("changes", C8_B, "Change 8: the Version 1.0 classification rule, which classifies a parameter from the size "
                        "of its effect and the risk that it moves outside the declared region, is kept word for "
                        "word, and two rules of PCMP-001 Version 2.0 are applied with it.", also=[("changes", C8_A)])
    sq("changes", C8_C)
    sq("changes", C8_D, "Under change 8, the words of the Version 1.0 rule, held comfortably inside the region or "
                        "narrow relative to it, are judged on the effect across the PAR and on the margin of the "
                        "PAR to the NOR, because neither PCMP-001 nor SOP-4001 sets a numerical threshold for them.")
    sq("changes", C9_C, "Change 9: PCMP-001 §7.9 now sets a target and a minimum process capability index (Cpk), "
                        "against which PCMR-001 judges the drug substance.", also=[("changes", C9_A)])
    sq("changes", C10_B, 'Change 10: the Version 1.0 records gave no execution dates, and Version 1.0 of the plan '
                         'read "No calendar dates are committed here."')
    sq("changes", C10_C)
    sq("changes", C10_D, "As PCMP-001 Version 2.0 (§5 and §9) and INV-001 preventive action PA3 require, Version "
                         "2.0 records the execution window of each study, that is the dates of its first and last "
                         "laboratory runs, and the calibration status of the instrumented system named in its "
                         "record.")
    sq("changes", C10_E, "Version 2.0 adds the term discrepancy from the plan, for work that the plan does not "
                         "foresee.")
    sq("changes", C11_A, "Change 11: descriptions of Version 1.0 that were wrong are corrected, with no change to "
                         "the design, and the expected directions of the four expectations of the unit-operation "
                         "description are unchanged.")
    for said, now, txt in C11:
        sq("changes", now or said, txt, also=[("changes", said)] if now else ())
    sq("changes", CH_DERIV)
    # Objectives
    for i, o in enumerate(OB):
        if i == 1:
            txt = ("Objective: to define the multivariate region over which the fitted models predict that the "
                   "aggregate, the host cell protein and the fragment content of the eluate pool all meet their "
                   "intermediate acceptance criteria.")
        elif i == len(OB) - 1:
            txt = ("Objective, added at Version 2.0: to verify the platform worst cases of cation exchange on "
                   "which the criteria upstream rely.")
        else:
            txt = "Objective: " + o[0].lower() + o[1:]
        sq("objectives", o, txt, also=[("objectives", OB_V2)] if i == len(OB) - 1 else ())
    sq("objectives", OB_PCR, "PCR-007 will present the outcome against each of the six objectives of the plan.",
       also=[("objectives", OB_SIX)])
    # Related documents
    sq("related", REL_RA, "The risk assessment RA-001 set the scope of the study, PCP-007 executes that scope, and "
                          "PCR-007 will report the outcome.")
    sq("related", REL_PH)
    st("The scale-down model and its operation are described in the scale-down model procedure SOP-1001 and the "
       "operating procedure SOP-2010.",
       [ref("sdm", q(S_SOP)), tref("related", sop_t, soprow, "SOP-1001"), tref("related", sop_t, soprow, "SOP-2010")])
    st(f"The procedures that govern the work include SOP-1002, {title_of['SOP-1002']}.",
       [ref("related", q(REL_SOPS)), tref("related", sop_t, soprow, "SOP-1002")])
    st("After collection the column is stripped, sanitized and re-equilibrated under SOP-2008, the procedure for "
       "the life cycle, packing and sanitization of the resin.",
       [ref("operation", q(O_STRIP)), tref("related", sop_t, soprow, "SOP-2008")])
    st(f"Each parameter will be classified under SOP-4001, {title_of['SOP-4001']}.",
       [ref("classification", q(CL_RULE)), tref("related", sop_t, soprow, "SOP-4001")])

    # Unit-operation description and prior knowledge
    sq("uo", U_MODE)
    sq("uo", U_BIND)
    sq("uo", U_ELUTE, "The antibody is eluted by raising the pH of the elution buffer, which weakens the "
                      "electrostatic attraction.")
    sq("uo", U_AGG)
    sq("uo", U_RES, "The aggregate clearance the step achieves depends on how well aggregate and monomer are "
                    "resolved and on the point at which pool collection is stopped.")
    sq("uo", U_IMP)
    sq("uo", U_HCP1)
    sq("uo", U_HCP2)
    sq("uo", U_DNA)
    sq("uo", U_LPA1)
    sq("uo", U_LPA2)
    sq("uo", U_YIELD2, "Yield is lost at the two edges of the pool: monomer that elutes before collection starts "
                       "is lost on the leading edge, and monomer that elutes after the stop collect point, or with "
                       "the aggregate that is cut away, is lost on the trailing edge.", also=[("uo", U_YIELD1)])
    sq("uo", U_FRAG1)
    sq("uo", U_FRAG2, "A later start of collection leaves more of the leading edge, rich in fragments, out of the "
                      "pool, and a later stop adds more of the trailing eluate, which carries few fragments; both "
                      "lower the fragment content of the pool.", also=[("uo", U_FRAG3)])
    sq("uo", U_FRAG4)
    sq("uo", U_PLAT)
    sq("uo", U_SAME)
    sq("uo", U_EXP, "Platform experience establishes the mechanisms of the step and identifies the parameters "
                    "worth studying.")
    sq("uo", U_WC, "Prior knowledge also supplies the platform worst cases from which the criteria are derived.")
    sq("uo", U_DATA)
    sq("uo", E_LOAD1, 'Expectation 1, from platform experience: a higher `{python} nm["load"]` occupies more of '
                      'the sulfonate ligand, so at the top of the studied range the column approaches its dynamic '
                      'binding capacity.', also=[("uo", U_FOUR)])
    sq("uo", E_LOAD2)
    sq("uo", E_COND1, '`{python} Nm["wash_cond"]` sets the ionic strength that shields the charge on the ligand '
                      'and on the bound species (expectation 2).')
    sq("uo", E_COND2)
    sq("uo", E_COND3, "The effect of load/wash conductivity should fall on impurity clearance rather than on the "
                      "aggregate separation, which happens during elution.")
    sq("uo", E_PH1, '`{python} Nm["elution_ph"]` sets the net charge on the antibody at the moment of elution '
                    '(expectation 3).')
    sq("uo", E_PH2)
    sq("uo", E_SC1, "Monomer elutes ahead of aggregate, so the material still leaving the column on the descending "
                    "edge of the peak is progressively richer in aggregate (expectation 4).")
    sq("uo", E_SC2)
    sq("uo", E_SC3)
    sq("uo", E_INT)
    sq("uo", E_FLOW1)
    sq("uo", E_FLOW2, "Over the range studied, and at the particle size of the platform resin, the change in peak "
                      "sharpness is expected to be too small to move the aggregate content of the pool.")
    # Quality attributes in scope
    sq("cqa", Q_ORIGIN, "Aggregate is formed in the production bioreactor and is added to during the low-pH hold, "
                        "host cell protein and DNA enter with the harvested cell culture fluid, leached Protein A "
                        "is released from the capture resin, and fragments are formed in culture and during the "
                        "harvest hold; the cation exchange step removes them.", also=[("cqa", Q_REMOVE)])
    st("Criticality follows the continuum of ICH Q9 rather than a binary split, and it was assigned with Tool #1 "
       "of the case study, which combines the impact of the attribute on safety and efficacy with the uncertainty "
       "in that impact.", [ref("cqa", q(Q_CRIT)), ref("cqa", q(Q_TOOL))])
    sq("cqa", Q_RESP)
    sq("cqa", Q_AGG, "Aggregate is the attribute the cation exchange step exists to control and carries the highest "
                     "criticality of the `{python} W(n_cq)` attributes in scope.")
    sq("cqa", Q_HCP)
    sq("cqa", Q_FRAG, "Fragments are measured by nrCE-SDS in the response-surface design.")
    sq("cqa", Q_YIELD2, "Step yield is a process performance attribute rather than a quality attribute; it is "
                        "measured on every run because the monomer that is cut away with the aggregate is lost "
                        "from the pool, so the aggregate clearance and the yield of a setting have to be read "
                        "together.", also=[("cqa", Q_YIELD1)])
    # Risk-based prioritization of parameters
    sq("risk", R_RANK, "All process parameters of the cation exchange step were carried into the risk ranking and "
                       "filtering exercise of RA-001, in which each parameter was given one ranking for its "
                       "potential impact on a quality attribute and a second for its potential to interact with "
                       "other parameters, and the two rankings were combined into a study assignment.")
    sq("risk", R_HIGH)
    sq("risk", R_MV, "The risk assignment produced three groups, and `{python} W(n_mv)` parameters were assigned "
                     "to the multivariate design.", also=[("risk", R_THREE)])
    st(t(R_WHY), [ref("risk", q(R_WHY_AGG)), ref("risk", q(R_WHY_HCP))])
    sq("risk", R_UV)
    sq("risk", R_WIDE, "The ranges studied are wider than the normal operating ranges in every case.")
    sq("risk", R_SET, "Each range studied was set from the control capability of the commercial equipment and from "
                      "the range over which the platform has been operated, so that the study bounds the step "
                      "beyond the region in which it will run and supports later movement within the region it "
                      "defines.")
    sq("risk", R_FAIL)
    sq("risk", R_PH)
    # Scale-down model and its qualification
    sq("sdm", S_COL)
    sq("sdm", S_UNITS)
    sq("sdm", S_PACK)
    sq("sdm", S_QRUNS)
    sq("sdm", S_QCMP, "Qualification will compare the model and the commercial step at the set-point condition on "
                      "the attributes that enter and leave the step: step yield, pool aggregate, pool host cell "
                      "protein, residual DNA and leached Protein A.")
    sq("sdm", S_QN)
    sq("sdm", S_PLATE)
    sq("sdm", S_OFF, "The offset of an output is the mean of the scale-down runs at set-point minus the mean of the "
                     "manufacturing-scale batches, with its two-sided `{python} s_offci` confidence interval, each "
                     "end of which is a one-sided `{python} s_side` confidence bound.", also=[("sdm", S_SIDE)])
    sq("sdm", S_DECIDE, "Whether the model is qualified for an output is decided at analysis, because that decision "
                        "needs the response-surface model.")
    sq("sdm", S_SUB)
    sq("sdm", S_OTHER)
    sq("sdm", S_ASSUME, "The judgement of fragments without an offset rests on the assumption that fragments "
                        "separate in the same way at both scales.")
    sq("sdm", S_CP, "Reproducibility of the model is re-established inside each designed experiment: the centre "
                    "point runs of both designs are executed at the set-point of every factor, so their spread "
                    "measures the reproducibility of the model under study conditions and provides the pure error "
                    "term against which lack of fit is tested.", also=[("sdm", S_REPRO)])
    sq("sdm", S_BOUND)
    # Operation
    sq("operation", O_RECV)
    sq("operation", O_ADJ, "The pool is adjusted to the load conductivity under study and is loaded onto the "
                           "equilibrated column at the target protein load.")
    sq("operation", O_WASH, "The column is then washed at the same conductivity as the load; the platform sets the "
                            "two equal by design, so they are varied together and cannot be varied independently.",
       also=[("operation", O_EQUAL)])
    sq("operation", O_ELU)
    sq("operation", O_COLLECT)
    # Analytical methods
    sq("methods", M_VALID)
    sq("methods", M_AGG)
    sq("methods", M_HCP)
    sq("methods", M_DNALPA)
    sq("methods", M_YIELD)
    sq("methods", M_FRAG)
    sq("methods", M_AMD)
    sq("methods", M_T73)
    sq("methods", M_VAR)
    sq("methods", M_REPRO)
    # Sampling plan
    sq("sampling", SP_LOAD, "Each run will be sampled at four points; the load will be sampled after conditioning, "
                            "so that the aggregate, host cell protein, DNA and leached Protein A levels entering the "
                            "step are known for every run.", also=[("sampling", SP_FOUR)])
    sq("sampling", SP_FT)
    sq("sampling", SP_POOL)
    sq("sampling", SP_STRIP)
    sq("sampling", SP_CP, "Replication is concentrated at the centre point: the screening design carries "
                          "`{python} cp_scr` centre point runs and the response-surface design carries "
                          "`{python} cp_rsm`.", also=[("sampling", SP_REP)])
    sq("sampling", SP_ORDER)
    sq("sampling", SP_RET)
    # Statistical methods
    sq("stats", T_CODE, "All factors will be analysed in coded units: each factor is coded so that its set-point is "
                        "0 and the edges of its studied range are −1 and +1, which makes the estimated effects "
                        "comparable across factors carrying different units and makes the intercept the predicted "
                        "response at the centre of the design.", also=[("stats", T_CODED)])
    sq("stats", T_OLS)
    sq("stats", T_EFFECT)
    sq("stats", T_SIG)
    sq("stats", T_PURPOSE)
    sq("stats", T_ALSO, "The judgement of each output over the NOR and the verification of the platform worst cases "
                        "also come from the response-surface model.")
    sq("stats", T_RSM)
    sq("stats", T_REPORT)
    sq("stats", T_PI, "The `{python} s_pi` prediction interval of a single run used to judge an output is exact: it "
                      "uses the t distribution and includes the residual variance and the uncertainty of the "
                      "fitted coefficients.", also=[("stats", T_PI2)])
    sq("stats", T_PI3, "For pool aggregate and pool host cell protein the prediction interval is computed at "
                       "manufacturing scale, by subtracting the offset of the scale-down model.")
    sq("stats", T_MC2, "Capability at commercial scale will be estimated by Monte Carlo simulation: "
                       "`{python} W(V['n_monte_carlo'])` batches will be simulated with every parameter drawn within "
                       "its normal operating range, the fitted models will be evaluated at each draw, and a "
                       "one-sided capability index will be computed for each attribute with an intermediate "
                       "acceptance criterion.", also=[("stats", T_MC)])
    sq("stats", T_RULE, "The capability estimate will be reported alongside the decision rule of the acceptance "
                        "criteria, with the margin between the predicted distribution and the limit, as supporting "
                        "evidence.")
    sq("stats", T_DS)
    sq("stats", T_CPK)

    # Factors, ranges and study type
    sq("factors", F_MV, "The `{python} n_mv` multivariate parameters enter both designs as the coded factors "
                        "`{python} codes[0]` to `{python} codes[-1]`.")
    for name, row in frow.items():
        st(f"In the screening and response-surface designs, {name} is coded as factor {_cells(row)[0]}.",
           [tref("factors", ft, frow, name)])
    sq("factors", F_CODES)
    # Screening design
    sq("screening", C_DESIGN)
    sq("screening", C_WHY)
    sq("screening", C_ALIAS)
    sq("screening", C_EST)
    sq("screening", C_RAND)
    sq("screening", C_LOT)
    sq("screening", C_LOTS)
    # Response-surface design
    sq("rsm", RS_DESIGN)
    sq("rsm", RS_FACES)
    sq("rsm", RS_ROT)
    sq("rsm", RS_QUAD)
    sq("rsm", RS_CUT, 'Curvature is expected on `{python} nm["stop_collect"]` and on `{python} nm["elution_ph"]`: '
                      'both change where the pool is cut relative to the aggregate peak, and because that peak has '
                      'a maximum, equal steps in the cut point add unequal amounts of aggregate to the pool.',
       also=[("rsm", RS_CURV)])
    sq("rsm", RS_SEQ)
    sq("rsm", RS_AUG, "Should the screening analysis identify an active factor that is not carried into the "
                      "response-surface design, the design should be augmented before the operating region is "
                      "declared, and the augmentation should be documented as a change to the plan.")
    sq("rsm", RS_ALL)
    # Univariate assessment
    sq("univariate", V_ONE)
    sq("univariate", V_RUNS, '`{python} Nm["flow"]` runs will be executed at the low edge, the set-point and the '
                             'high edge of its range studied, with every other parameter held at its set-point, and '
                             'the responses that Version 1.0 listed in its §5.3 (`{python} uv_resp`) will be '
                             'measured on each.')
    sq("univariate", V_WHAT)
    sq("univariate", V_WHY, "A univariate assessment cannot determine whether flow rate interacts with the other "
                            "parameters; it is accepted because flow rate changes the residence time of the antibody "
                            "in the pores of the resin and with it the sharpness of the elution peak, and changes "
                            "neither the net charge on the antibody nor the ionic strength that sets how strongly "
                            "the antibody is held, so an interaction with load, conductivity, elution pH or the "
                            "collection window is not expected.", also=[("univariate", V_INT)])
    sq("univariate", V_MOVE)
    # Acceptance and decision criteria
    sq("criteria", CR_THEY, "Version 1.0 of the plan named four decisions, each with its own rule: the acceptance of "
                            "the scale-down model, the adequacy of a model, the operating region and the "
                            "classification of each parameter.", also=[("criteria", CR_FOUR)])
    sq("criteria", CR_V2)
    sq("criteria", CR_LIST, 'The decisions of Version 1.0 that rest on words with no numerical threshold are the '
                            'claim of a parameter dependence for residual DNA and leached Protein A "unless the data '
                            'show one", the repacking of a column that fails the packing tests, the attribution of a '
                            'result "within assay variability of its criterion" to the assay, the test of the strip '
                            'fraction when a run fails to close its mass balance, the move of elution flow rate into '
                            'a multivariate study after an effect "comparable in size with the effects estimated in '
                            'the screening study" and the identification of the runs made on a lot "out of trend".')
    sq("qualification", QL_SEP)
    sq("qualification", QL_RULE)
    sq("qualification", QL_CONC, "The conclusion over the NOR is whether the output meets its criterion at every "
                                 "combination of NOR low, set-point and NOR high of the `{python} k` factors, judged "
                                 "on the prediction interval of a single run.")
    sq("qualification", QL_NOTUSED)
    sq("qualification", QL_CAUSE)
    sq("qualification", QL_NOTQ)
    sq("adequacy", MA_FOUR)
    sq("adequacy", MA_1, "Adequacy test 1: the model F-test is significant at α = `{python} alpha`, the level "
                         "PCMP-001 sets for model terms.")
    sq("adequacy", MA_2, "Adequacy test 2: lack of fit against the pure error of the centre point runs is not "
                         "significant at α = `{python} alpha_lof`.")
    sq("adequacy", MA_3, 'Adequacy test 3, the limit on overfitting: predicted R² falls short of R² by no more than '
                         '`{python} f"{gap:.2f}"`, because a model that fits its own runs much better than it '
                         'predicts runs left out of the fit has more terms than the data support.',
       also=[("adequacy", MA_3B)])
    sq("adequacy", MA_4B, "Adequacy test 4: the residuals show no pattern against the predicted values or the run "
                          "order, and no single run dominates the fit; the absolute residuals are regressed on the "
                          "predicted values, and the residuals on the run order, and neither slope may be "
                          "significant at α = `{python} alpha_res`.", also=[("adequacy", MA_4)])
    sq("adequacy", COOK_1, "Under adequacy test 4, a run with a Cook's distance above `{python} s_cook`/n is "
                           "examined by deleting it and repeating the judgement, and the model fails the test only "
                           "where a run's Cook's distance exceeds `{python} s_cook_fq` of the F distribution with p "
                           "and n − p degrees of freedom.", also=[("adequacy", COOK_2)])
    sq("adequacy", MA_NOSTAT, "PCMP-001 §7.2 states the fourth criterion without a statistic; the two tests and "
                              "their thresholds are those of the campaign, applied in the same way in every step "
                              "plan.", also=[("adequacy", MA_CAMP)])
    sq("adequacy", MA_ABS)
    sq("adequacy", MA_FAIL)
    sq("adequacy", MA_FLAG, "PCR-007 examines any run that the fourth test flags, and the verification of the "
                            "platform worst cases states which of the tests the model behind a widening bound must "
                            "pass.")
    sq("adequacy", MA_DESC)
    sq("adequacy", MA_LOF)
    sq("iac", I_EACH, "Each quality criterion the pool is judged against is an intermediate acceptance criterion "
                      "(IAC).", also=[("iac", I_TABLE)])
    sq("iac", I_DERIVE)
    sq("iac", I_DS, "No step after cation exchange changes fragments in the derivation, so the cation exchange "
                    "pool is judged against the drug substance criterion for fragments itself, `{python} s_frag` %.",
       also=[("iac", I_NOSTEP)])
    sq("iac", I_AGG, "The a priori aggregate criterion of the cation exchange pool is the drug substance criterion "
                     "of `{python} s_ds_agg` %, because the a priori derivation assumes that no later step changes "
                     "aggregate. PCMP-001 §7.3 sets an increase across UF/DF of up to `{python} s_uf_add` percentage "
                     "points at the single-batch prediction bound, and the criterion in force is the drug substance "
                     "criterion less that increase, `{python} s_agg` %.",
       also=[("iac", I_AAP), ("iac", I_UF)])
    sq("iac", I_HCP2, "For host cell protein the drug substance criterion of `{python} s_ds_hcp` ng/mg is carried "
                      "back through anion exchange, and with the platform worst case of anion exchange, a clearance "
                      "factor of `{python} s_aex_pf`, the criterion is `{python} s_hcp_ap` ng/mg a priori.",
       also=[("iac", I_HCP1)])
    sq("iac", I_BOUND, "PCR-008 verified the anion exchange worst case: it found a one-sided `{python} s_vb` "
                       "prediction bound of a single batch of `{python} s_aex_b` for the clearance factor at the "
                       "least favourable combination of the anion exchange NOR, better than the platform value, on "
                       "a model that meets the first three adequacy criteria of PCMP-001 §7.2 and is not an exact "
                       "fit.", also=[("iac", I_PCR8)])
    sq("iac", I_FORCE, "The bound replaced the platform value, and the host cell protein criterion in force at the "
                       "cation exchange step is `{python} s_hcp` ng/mg.")
    sq("iac", I_RISK)
    for key, row in irow.items():
        x = iac.loc[key]
        unit = re.search(r"\(([^)]*)\)$", T.ATTR_NAME[key]).group(1)
        crit_, ds_ = (T.crit(x[lo], x[hi], x["spec_type"]) for lo, hi in (("iac_low", "iac_high"), ("ds_low", "ds_high")))
        how = (f"the drug substance criterion {ds_} {unit}, because no step after cation exchange changes it"
               if x["basis"] == "drug substance" else
               f"the drug substance criterion {ds_} {unit} carried back through a downstream clearance factor of "
               f"{_cells(row)[2]} and an increase of {_cells(row)[3]} ({x['basis']}; {T.crit(x['iac_low_apriori'], x['iac_high_apriori'], x['spec_type'])} "
               f"{unit} a priori)")
        st(f"The intermediate acceptance criterion for {names[key]} at the cation exchange step is {crit_} {unit}: "
           f"{how}.", [tref("iac", iac_t, irow, key)])
    sq("iac", I_LPA)
    sq("judgement", J_BATCH, "Every output with a criterion at the cation exchange step is a quality attribute whose "
                             "criterion applies to each batch, so each output is judged on a single batch.",
       also=[("judgement", J_QA)])
    sq("judgement", J_PI, "A response-surface model predicts the mean response and a single batch scatters around "
                          "that mean, so the judgement uses a prediction interval or bound of a single batch.")
    sq("judgement", J_THEY, "Four analyses judge an output on a single batch: the judgement over the NOR, the "
                            "operating region, the NOR-propagated PAR and the verification of the platform worst "
                            "cases.", also=[("judgement", J_FOUR)])
    sq("judgement", J_NOR)
    sq("judgement", J_UPPER)
    sq("region", OR_DEF, "The operating region is the region of the `{python} k` multivariate factors, within their "
                         "studied ranges, over which every output with an intermediate acceptance criterion meets "
                         "that criterion at both ends of the `{python} s_pi` prediction interval of a single run, at "
                         "manufacturing scale (PCMP-001 §6.2).")
    sq("region", OR_NAMES)
    sq("region", OR_INSIDE, "The declared region will lie inside the ranges studied, and the normal operating ranges "
                            "will lie inside the declared region; PCR-007 states whether they do.",
       also=[("region", OR_STATES)])
    sq("region", OR_MARGIN)
    sq("region", OR_WHOLE)

    sq("verification", VR_ASSUME)
    sq("verification", VR_CHECK, "PCR-007 checks the platform worst cases of `{python} s_checked`, which are "
                                 "responses of the designs (PCMP-001 §7.5).")
    for key, row in wcrow.items():
        c = _cells(row)      # Attribute | Platform worst case (lowest clearance factor) | Criteria upstream | Response
        st(f"Platform worst case of cation exchange for {names[key]}: a lowest clearance factor of {c[1]}, on "
           f"which criteria upstream rely ({c[2]}); "
           + ("it is a response of the designs, so PCR-007 checks it." if key in design_cqa else
              "it is not a response of the designs, so its platform value stands."),
           [tref("verification", wc_t, wcrow, key)])
    sq("verification", VR_EVAL)
    sq("verification", VR_CF)
    sq("verification", VR_GIVES, "The response-surface model gives the worst clearance factor that it predicts over "
                                 "the NOR combinations, and the one-sided `{python} s_vb` prediction bound of a "
                                 "single batch at the least favourable combination, on its unfavourable side.")
    sq("verification", VR_CONF)
    sq("verification", VR_EDGE, "The values observed at the edges of the ranges studied, against the same nominal "
                                "feed, are reported beside the predicted worst case for information.")
    sq("verification", VR_1, "Verification rule 1 (PCMP-001 §7.5): where the worst clearance factor predicted "
                             "within the NOR is lower than the platform worst case, the prediction bound of a single "
                             "batch replaces the platform value, and every criterion upstream for that attribute is "
                             "recalculated with it and becomes stricter.", also=[("verification", VR_STRICT)])
    sq("verification", VR_2, "Verification rule 2: where the prediction bound of a single batch is better than the "
                             "platform value, and the response-surface model behind it meets the first three "
                             "adequacy criteria (a significant model, no significant lack of fit and the limit on "
                             "overfitting) and is not an exact fit, the bound replaces the platform value, and every "
                             "criterion upstream for that attribute is recalculated with it and becomes wider.",
       also=[("verification", VR_WIDER)])
    sq("verification", VR_4TH, "The fourth adequacy criterion, on the residuals and on influential runs, does not "
                               "decide a change of a platform value; PCR-007 examines the bound and states whether "
                               "it depends on a single run.", also=[("verification", VR_EXAM)])
    sq("verification", VR_3, "Verification rule 3: otherwise the platform value stands.")
    sq("verification", VR_ARGUE, "A report whose check changes a criterion argues the change by its risk "
                                 "(PCMP-001 §7.5): who bears the risk, the patient or the producer; whether an "
                                 "excursion of the step output beyond the changed criterion would be detected, and "
                                 "where, by an in-process test or by a release test; what the downstream steps must "
                                 "then clear; and the probability that the drug substance fails its specification "
                                 "in the integrated model of the train.",
       also=[("verification", VR_WHO), ("verification", VR_DET), ("verification", VR_DOWN)])
    sq("classification", CL_RULE, "A parameter will be classified under SOP-4001 from two things together, the size "
                                  "of the effect the study demonstrates on a quality attribute and the risk that the "
                                  "parameter moves outside the declared region in manufacture.")
    sq("classification", CL_WC)
    sq("classification", CL_CPP)
    sq("classification", CL_KPP)
    sq("classification", CL_GPP)
    sq("classification", CL_LINK, "PCMP-001 Version 2.0 adds two rules to the Version 1.0 classification rule; under "
                                  "the first, a parameter is linked to an output, or affects it, when a term that "
                                  "contains the parameter is significant at α = `{python} alpha` (PCMP-001 §6.2).",
       also=[("classification", CL_TWO)])
    sq("classification", CL_SIZE)
    sq("classification", CL_WORDS)
    sq("classification", CL_FLOW)
    # Proven acceptable ranges (planned analysis)
    sq("par", PA_EACH)
    sq("par", PA_CRIT, "The criterion applied in a proven acceptable range is the intermediate acceptance criterion "
                       "of the attribute, so a proven acceptable range in the study is the range of a parameter over "
                       "which the fitted model predicts that the eluate pool meets the level the step must hand on.")
    sq("par", PA_FLOW2, '`{python} Nm["flow"]` is not a parameter of the multivariate design; its range is supported '
                        'by its own data, from the univariate assessment, as PCMP-001 §4 provides for a parameter '
                        'studied one factor at a time.', also=[("par", PA_FLOW)])
    sq("par", PA_NORULE, "Version 1.0 set no rule for judging the range of elution flow rate against the criteria, "
                         "and PCR-007 states the approach it takes.", also=[("par", PA_BOTH)])
    sq("par", PA_TWO)
    sq("par", PA_FIRST, "The first PAR analysis evaluates the response-surface model across the studied range of the "
                        "parameter with the other `{python} W(k - 1)` factors held at the centre of the design, "
                        "which for every parameter of the cation exchange step is its set-point.")
    sq("par", PA_TARGET, "The first PAR analysis answers what one parameter can do while the rest of the step is at "
                         "target.")
    sq("par", PA_SECOND, "The second PAR analysis propagates the normal operating ranges of the other "
                         "`{python} W(k - 1)` factors.")
    sq("par", PA_GRID)
    sq("par", PA_NARROW, "The second analysis bounds routine operation and will in general return the narrower of "
                         "the two ranges, because a setting that is acceptable with the rest of the step at target "
                         "need not be acceptable when the rest of the step sits anywhere inside its normal operating "
                         "ranges.", also=[("par", PA_ROUTINE)])
    sq("par", PA_NAMES)
    sq("par", PA_MEAN)
    sq("par", PA_DRAW)
    sq("par", PA_SPANS, "The NOR-propagated analysis assumes that the NOR spans ±`{python} s_ksd` standard "
                        "deviations of the routine variation of the parameter.")
    sq("par", PA_COEF)
    sq("par", PA_PCT)
    sq("par", PA_CLAIM)
    sq("par", PA_CONT)
    sq("par", PA_NONCONT)
    sq("par", PA_INTER)
    sq("par", PA_NOPAR)
    sq("par", PA_PLOT, "Each output with an intermediate acceptance criterion will be reported with a plot of the "
                       "predicted response against the parameter carrying the largest main effect on it, with the "
                       "acceptable region shaded, the set-point marked and the normal operating range marked.")
    sq("par", PA_SEED)
    sq("par", PA_REGION, "A proven acceptable range is a statement about one parameter while the others are held "
                         "at defined settings; the operating region is a statement about the `{python} k` factors "
                         "together, and a combination of settings that are each inside their proven acceptable "
                         "range may still fall outside the region where an interaction is active.",
       also=[("par", PA_ONE)])
    sq("par", PA_BUILT, "Both the proven acceptable ranges and the operating region will be reported, and the "
                        "control strategy will be built on the region.")
    # Data management and integrity
    for s_ in (D_ALCOA, D_ELN, D_CDS, D_TRANS, D_RET, D_CORR, D_DEV, D_DISC, D_REC, D_DATE):
        sq("data", s_)
    # Roles and responsibilities
    sq("roles", RO_DO, "Process Development and MSAT own the plan; they design the studies, execute the runs on the "
                       "scale-down model, analyse the data and author PCR-007.", also=[("roles", RO_OWN)])
    sq("roles", RO_OTHER, "The other functions review and approve within their own competence, and no function "
                          "approves its own work.")
    for func, row in rorow.items():
        resp_ = _cells(row)[1]
        st(f"{func}: {resp_[0].lower() + resp_[1:]}.", [tref("roles", ro_t, rorow, func)])
    sq("roles", RO_PERSON)
    sq("roles", RO_NAMES)
    # Deliverables and schedule
    sq("schedule", SH_DELIV, "The deliverable of PCP-007 is PCR-007.")
    sq("schedule", SH_REPORT, "PCR-007 will report the execution of every study described in the plan, the models "
                              "fitted to the data, the operating region, the proven acceptable ranges, the "
                              "capability estimate and the classification of each parameter.")
    sq("schedule", SH_CARRY, "PCR-007 will also carry the design matrices as executed, including any run that was "
                             "repeated, and every deviation recorded during the campaign.")
    sq("schedule", SH_ROLL)
    sq("schedule", SH_V2)
    sq("schedule", SH_Q, "The work runs in five phases, and the qualification runs of the scale-down model are made "
                         "first: no characterization run is executed until they are complete and the offsets "
                         "estimated.", also=[("schedule", SH_FIVE)])
    sq("schedule", SH_SCR)
    sq("schedule", SH_RSM)
    sq("schedule", SH_UNI)
    sq("schedule", SH_LAST)
    sq("schedule", SH_PTP)
    sq("schedule", SH_PAR)
    sq("schedule", SH_EQ)
    sq("schedule", SH_CAL)
    # Risks and assumptions
    sq("risks", RK_SDM, "Risk 1: the scale-down model may fail to represent the commercial column in a respect the "
                        "qualification does not test; the qualification compares the attributes that enter and "
                        "leave the step.", also=[("risks", RK_FOUR), ("risks", RK_CMP)])
    sq("risks", RK_LOAD, "Risk 2: the feed material may not be representative; the load is the neutralized pool of "
                         "the low-pH viral inactivation step, and its aggregate and host cell protein content set "
                         "the starting point of every clearance the study measures.", also=[("risks", RK_FEED)])
    sq("risks", RK_MEAS)
    sq("risks", RK_TREND)
    sq("risks", RK_CYCLE, "Risk 3: the resin may behave differently at a different point in its life cycle; all "
                          "characterization runs will be performed on resin within the cycle count qualified under "
                          "SOP-2008, and the conclusions of the study are bounded by that cycle count.",
       also=[("risks", RK_RESIN)])
    sq("risks", RK_ASSAY, "Risk 4: assay variability may obscure a small effect.")
    sq("risks", RK_A1, "Assumption 1: the platform mechanisms apply to A-Mab at the cation exchange step, which the "
                       "designs will test against the expectations of the unit-operation description rather than "
                       "assume.", also=[("risks", RK_THREE)])
    sq("risks", RK_A2, "Assumption 2: the parameters of the parameter table are the parameters that matter, which "
                       "the risk assessment RA-001 established and which the study can test only within its own "
                       "factor set.")
    sq("risks", RK_A3, "Assumption 3: a quadratic model describes the responses adequately over the studied ranges, "
                       "which the lack of fit test tests directly.")
    sq("risks", RK_A4, "Assumption 4, added at Version 2.0: the NOR of each parameter spans ±`{python} s_ksd` "
                       "standard deviations of its routine variation, on which the NOR-propagated analysis rests.",
       also=[("risks", RK_TWO)])
    sq("risks", RK_A5, "Assumption 5, added at Version 2.0: fragments separate in the same way at both scales, so "
                       "that their judgement without an offset holds at manufacturing scale.")
    sq("risks", RK_KEEP)
    # Approvals and appendices
    sq("approvals", AP_BY, "PCP-007 is approved by the functions recorded in its approval record.")
    sq("approvals", AP_EXEC, "Execution may begin once the plan is approved and the qualification runs of the "
                             "scale-down model have been made and the offsets estimated.")
    sq("approvals", AP_CHANGE, "Any change to the design, to the ranges or to the acceptance criteria after approval "
                               "requires a revision of the plan carrying the same approvals, and the revision should "
                               "be approved before the affected runs are executed.")
    sq("approvals", AP_DATE, "Version 2.0 is the amendment that INV-001 required as its corrective action CA2; it was "
                             "issued after the runs and approved on its effective date, `{python} v2_date`.",
       also=[("approvals", AP_CA2)])
    sq("app_a", AA_GIVES, "The planned screening design is given in coded levels and letter codes, with −1 and +1 at "
                          "the edges of the studied range of each factor.")
    sq("app_a", AA_LABELS)
    sq("app_b", AB_CORNERS, "In the planned response-surface design the factorial runs repeat the corners of the "
                            "screening design, and the axial runs sit on the faces of the cube at the edge of each "
                            "factor's studied range.")

    # ==== concepts ================================================================================
    concepts = [Concept(concept_id=STEP_ID, concept_type="PROCESS_STEP", canonical_name=UO_NAME,
                        aliases=["cation exchange", "cation exchange step", "cation exchange chromatography step",
                                 STEP_LABEL, f"Step {ns['STEP']}"],
                        review_status="human_verified")]
    alias = {"wash_cond": ["conductivity"], "elution_ph": ["elution pH"],
             "stop_collect": ["stop collect point", "stop collect threshold"], "flow": ["flow rate"]}
    concepts += [Concept(concept_id=PC[p.name], concept_type="PROCESS_PARAMETER", canonical_name=p.name,
                         aliases=sorted({nm[k]} - {p.name}) + alias.get(k, []), review_status="human_verified")
                 for k, p in pkey.items()]
    concepts += G._attr_concepts(ckeys)
    concepts.append(Concept(concept_id="attr:step_yield", concept_type="PERFORMANCE_ATTRIBUTE",
                            canonical_name="Step yield", aliases=["step yield", "yield"],
                            review_status="human_verified"))
    concepts += G._method_concepts(amvs, title_of)
    concepts += [Concept(concept_id=e.equipment_id, concept_type="EQUIPMENT", canonical_name=e.equipment_name,
                         review_status="human_verified") for e in equipment]

    # ==== the annex ===============================================================================
    disc = [d for d in P.PLAN_DISCREPANCIES.get("PCR-007", []) if d.get("studies")]
    disc_txt = "; ".join(f"{', '.join(d['studies'])} ({d['id']})" for d in disc)
    annex = S.GroundTruthAnnex(
        document_id=DOC, document_title=f"{P.DOC_REGISTRY[DOC][0]} — {P.DOC_REGISTRY[DOC][1]}",
        document_class=P.DOC_REGISTRY[DOC][0], **G.rev2_layer(DOC, FILE),
        schema_extensions_used=G.COMMON_EXT + G.REV2_EXT,
        out_of_schema_notes=[
            "Classification is a result of the study, so every parameter_type is 'unclassified'. No set-point "
            "or NOR of the step changed at Version 2.0 (the plan's setup asserts it, and the plan uses one NOR "
            "throughout), so ProcessParameter.target_value and NOR are the values of the parameter table, which "
            "are also the values in force. ProcessParameter.PAR carries the range studied, as everywhere in the "
            "corpus. The plan claims no proven acceptable range and draws no design space, so there are no "
            "ProvenAcceptableRange or DesignSpace records; how the ranges and the operating region will be "
            "derived is in statements. The four multivariate parameters are also anchored on their row of the "
            "coded factor table.",
            "The step forms no quality attribute: the drug substance register assigns none to it (an "
            "ExplicitNonClaim). The QualityAttribute records are the five attributes in scope, formed upstream "
            "and cleared at this step; their acceptance_criteria are the drug substance criteria of the "
            "attribute table. Aggregate, host cell protein and fragments are responses of the designs; residual "
            "DNA and leached Protein A are measured across the step and are not (an ExplicitNonClaim). The step "
            "criteria are attribute_has_acceptance_criterion assertions and statements on the rows of the table "
            "of intermediate acceptance criteria.",
            "acceptance_criteria holds the rows of the criteria-change table: the Version 1.0 analysis limits of "
            "aggregate and host cell protein (superseded) and the Version 2.0 criteria (in force); fragments had "
            "no Version 1.0 criterion. All three outputs with a criterion are quality attributes judged on a "
            "single batch. The host cell protein criterion was widened when PCR-008 verified the anion exchange "
            "worst case; the plan's account of the derivation and of the bound is in statements.",
            "studies holds the scale-down model qualification and the screening, response-surface and "
            "univariate studies, each on its row of the execution-window table and on the sentences that "
            "describe it. The screening and response-surface records are also anchored on every row of their "
            "planned design matrix (Appendices A and B); the sixteen factorial rows read alike in both matrices. "
            "The qualification compares scale-down runs with manufacturing-scale batches, which is not a design, "
            "so it has no n_runs, and its responses are the outputs as the plan names them (plate count and peak "
            "asymmetry have no response key). The designs list the responses the plan states: fragments are a "
            "response of the response-surface design only, by nrCE-SDS, the one fragment result the plan judges, "
            "so no SEC fragment response is listed. The univariate study has no n_runs: the plan states its settings, "
            "not a run count, and its responses are those the plan lists. "
            + (f"Studies of the step made after Version 1.0 are not studies of this plan; PCR-007 records them "
               f"as discrepancies from it: {disc_txt}." if disc else
               "PCR-007 records no study outside the plan as a discrepancy."),
            "Each AnalyticalMethod record is anchored on its sentence of the analytical methods section and on "
            "its row of the procedures table; the concept of a method carries the title of its validation as "
            "canonical name.",
            "The platform worst cases of the step that the criteria upstream rely on are statements anchored on "
            "the rows of the worst-case table: they are assumptions of upstream criteria, not criteria of this "
            "step, and their verification is a result of PCR-007, not of the plan.",
            "parameter_impacts_attribute and parameter_does_not_significantly_impact_attribute assertions are the "
            "plan's stated expectations from prior knowledge, not results. The expected interaction of protein "
            "load and load/wash conductivity on host cell protein has no predicate of its own; it is cited by the "
            "assertion of load/wash conductivity on host cell protein and stated in a statement.",
            f"The {chamber_name} is the instrumented system the record names for the response-surface study; it "
            f"is an Equipment record with a step_uses_equipment assertion. The commercial column is an Equipment "
            f"record at the receiving site, anchored on the sentence that names it and on the roles-table row of "
            f"the receiving site.",
            "The first proven acceptable range analysis is recorded as the plan states it: the other factors held "
            "at the centre of the design, which at this step is the set-point of every factor.",
            "Each row of the roles table and of the coded factor table is a statement. The approvals table and "
            "the abbreviations are not represented. No rhetorical_spans: a plan has none. weak_claims is empty.",
        ] + G._unrendered_note(unrendered),
        inventory=G.rev2_inventory(DOC, FILE, "process_characterization_plan", UO_NAME,
                                   ["process characterization", "cation exchange chromatography",
                                    "bind and elute mode", "aggregate clearance", "host cell protein clearance",
                                    "protocol amendment", "intermediate acceptance criteria",
                                    "scale-down offset", "design of experiments",
                                    "platform worst-case verification"]),
        entities=entities, studies=studies,
        report_sections=[ReportSection(section_id=f"{DOC}-summary", title="Plan summary", statements=ST)],
        assertions=AssertionStore(run_id=f"gt-{DOC}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{DOC}", concepts=concepts),
        weak_claims=[], rhetorical_spans=[],
        acceptance_criteria=G.acceptance_criteria_layer(DOC, FILE, SEC["changes"][-1],
                                                        ct["tbl-criteria-change"][0], [UO]))
    _gate(annex, text)
    return annex
