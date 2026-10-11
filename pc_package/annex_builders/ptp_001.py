"""PTP-001 Version 2.0, the Process Transfer Plan of the A-Mab drug substance process, reissued under
corrective action CA3 of INV-001: its ground-truth annex (``build()``).

PTP-001 is a corpus-level plan. It has no designed experiment of its own, no registered discrepancy
(its brief's §5c is empty) and no weak claim. The kinds of record follow the corpus-level model
(``build_master_plan`` for PCMP-001) and the Version 1.0 builder of this plan (``build_transfer_plan``),
whose concept ids are kept: ``process:amab_ds``, ``step:<key>``, ``attr:<key>``, ``site:cambridge`` and
``site:grafton``, ``transfer:amab_ds`` and ``gap:GAP-0N``; the parameter ids are those of PCMP-001
(``param:<step>_<key>``). The annex holds the inventory and the revision layer; the two sites, the eight
steps, the eleven quality attributes, the 37 parameters as they stand at this revision, the method
validations, the two equipment trains, the control strategy elements and the modular viral clearance
claims; the document relationships and the explicit non-claims; the one study the plan names; the
seven transfer gaps; the assertions; the statements of every section; the concepts.

Six tables are complex tables (``T.frame``, ``T.parameters_by_step``, ``T.sop_references``), read back
through ``qmd_ctables`` from the object the plan printed. Six are pipe tables a chunk prints with
``md_table`` or ``corpus_docs_md``: ``_printed`` re-runs that chunk in the plan's own namespace and
``_flat_rows`` reads its rows as the DOCX reads them, each cross-reference replaced by the number the
rendered document gives it. Every row quote carries ``table_header=rows.header``. Every prose quote is
a span of the ``.qmd`` copied with its inline expressions and cross-references and rendered by ``q``
(the inline expressions evaluated in the plan's namespace, ``qmd_inline``; the cross-references
numbered, ``_xrefs``; the apostrophe made typographic, ``_smart``). ``q`` refuses a span that is not in
the ``.qmd`` prose, so no value is typed here, and ``build()`` refuses to return an annex with a quote
that does not ground or with a weak anchor.

Helpers new here, candidates for ``build_ground_truth``: ``_printed`` and ``_flat_rows`` (the rows of a
pipe table that a chunk prints with ``md_table``, re-run in the document's namespace with the
cross-references rendered; ``qmd_printed`` needs a ``#| label:`` that these chunks do not carry),
``_text`` (record text from a cell or a sentence, its cross-references dropped or rendered),
``_nomark`` for the footnote markers of ``T.parameters_by_step``, ``_lc`` (a cell continued after a
colon) and ``METHOD_TYPE_LOCAL`` (the method type of AMV-3021 and AMV-3221, which ``METHOD_TYPE``
lacks). ``_xrefs``, ``_smart``, ``_plain`` and
``_md_caption`` follow ``pcp_007.py``; ``_walk``, ``_gate`` and ``_check_sections`` follow ``pcp_009.py``.
"""
from __future__ import annotations

import contextlib
import io
import os
import re
from types import SimpleNamespace

import _pcpkg as P
import build_ground_truth as G
import schema_ext as S
from check_grounding import CELL_SEP, normalize, specificity_report

DOC = "PTP-001"
QMD = "PTP-001_transfer.qmd"
FILE = G.PTP_FILE                          # "PTP-001_transfer.docx"

_TR = "Transfer of the process, methods and control strategy"
#: Section key -> heading path as the document renders it. ``_check_sections`` checks every title
#: against the headings of the .qmd, so a renamed section fails loudly instead of mislabelling.
SEC = {
    "title": ("Title block",),
    "purpose": ("Purpose and scope",),
    "changes": ("Purpose and scope", "Changes in this revision"),
    "product": ("Product and process description",),
    "sites": ("Sending and receiving sites",),
    "equivalency": ("Site equivalency analysis",),
    "sdm": ("Scale-down model and comparability strategy",),
    "transfer": (_TR,),
    "process": (_TR, "The manufacturing process"),
    "methods": (_TR, "The analytical methods"),
    "control": (_TR, "The control strategy"),
    "ppq": ("Process performance qualification strategy",),
    "gaps": ("Gap analysis",),
    "roles": ("Roles and responsibilities",),
    "schedule": ("Deliverables and schedule",),
    "approvals": ("Approvals",),
}
#: The pipe tables the plan prints from a chunk (``md_table`` / ``corpus_docs_md``), by label.
FLAT = ("tbl-package", "tbl-train", "tbl-equivalency", "tbl-scope", "tbl-gaps", "tbl-deliverables")
#: A cross-reference in the .qmd prose (``@sec-sdm``, ``@tbl-gaps``).
_XREF = r"@(?:sec|tbl)-[\w-]+"
#: The kind of assay of the two method validations ``build_ground_truth.METHOD_TYPE`` does not list.
METHOD_TYPE_LOCAL = {"AMV-3021": "chromatography", "AMV-3221": "chromatography"}
#: How the principal role of a step in the process train table names each attribute. A step is
#: linked to an attribute (``step_has_quality_attribute``) where its role names it, so the links
#: follow the table the document prints.
ATTR_TOKEN = {"afucosylation": "glycan", "galactosylation": "glycan", "high_mannose": "glycan",
              "acidic_variants": "charge-variant", "aggregates_hmw": "aggregate",
              "fragments_lmw": "fragments", "hcp": "HCP", "residual_dna": "DNA",
              "leached_protein_a": "leached", "lrv_xmulv": "XMuLV", "lrv_mvm": "MVM"}
#: Transfer gap (row of the gap table, in order) -> (gap id of the Version 1.0 annex, gap area, a word
#: the gap cell must contain, so that a reordered table fails instead of mislabelling).
GAPS = [("GAP-01", "process", "Scale-down"), ("GAP-02", "analytical_method", "Analytical methods"),
        ("GAP-03", "process", "Harvest and UF/DF"), ("GAP-04", "control_strategy", "classification"),
        ("GAP-05", "process", "Buffer preparation"), ("GAP-06", "validation", "Viral clearance"),
        ("GAP-07", "quality_system", "Operators")]


# --------------------------------------------------------------------------- #
# Local helpers (see the module docstring for where each comes from).          #
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
    """The cells of a rendered row (a continuation row of a merged column keeps its empty first cell)."""
    return [c.strip() for c in row.split("|")]


def _lc(s):
    """A cell or sentence continued after a colon: its first letter lower-cased, unless it opens with
    an identifier or an abbreviation ("RA-001, the ...", "PCMR-001 and ...")."""
    return s if s[:2].isupper() else s[0].lower() + s[1:]


def _nomark(cell):
    """A cell without its footnote marker ("Dissolved oxygen a)" -> "Dissolved oxygen", "20–39 c1)" ->
    "20–39"), as ``T.parameters_by_step`` renders the markers."""
    return re.sub(r"\s+[a-z]\d*\)$", "", str(cell)).strip()


def _md_caption(src, label):
    """The caption a chunk prints after a pipe table (``print(": <caption> {#label}")``)."""
    m = re.findall(r'print\(f?": (.*?) \{#' + re.escape(label) + r'\}"\)', src)
    if len(m) != 1:
        raise ValueError(f"{DOC}: {len(m)} captions printed for {label}")
    return m[0]


def _printed(src, ns, label):
    """The pipe table that the chunk captioned ``label`` prints, re-run in the document's own
    namespace (``qmd_namespace``). The chunk prints ``md_table(...)`` or ``corpus_docs_md(...)``,
    which neither ``show`` nor ``md`` records, and carries no ``#| label:`` for ``qmd_printed``."""
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
    return [ln for ln in buf.getvalue().splitlines() if ln.startswith("|")]


def _smart(s, runs=True):
    """Prose as pandoc renders it: a straight double quote opens at the start or after a space or an
    opening bracket and closes everywhere else, and a straight apostrophe becomes a typographic one.
    ``runs``: a closing mark that punctuation follows reads ``” .`` in the extracted text."""
    s = re.sub(r'(^|[\s(\[])"', lambda m: m.group(1) + "“", s)
    s = s.replace('"', "”").replace("'", "’")
    if runs:
        s = re.sub(r"”(?=\S)", "” ", s)
    return s


def _xrefs(src, text, captions):
    """``{label -> rendered cross-reference}``: ``sec-sdm`` -> ``Section 5``, ``tbl-gaps`` -> ``Table 9``.

    A section number comes from the heading structure of the .qmd (numbered headings counted in
    order, ``.unnumbered`` ones skipped) and is checked against the heading as the .docx numbers it.
    A table number is read from the rendered caption line "Table N: <caption>", which must occur
    exactly once."""
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
    """Statement text from a .qmd sentence: a parenthesis of cross-references only is dropped, and any
    other cross-reference is refused, so that the statement is written out instead."""
    s = re.sub(r"\s*\((?:see )?" + _XREF + r"(?:(?:, | and )" + _XREF + r")*\)", "", s)
    if re.search(_XREF, s):
        raise ValueError(f"{DOC}: a statement keeps a cross-reference, write it out: {s[:100]!r}")
    return s


def _text(s, xr):
    """Record text from a cell or a sentence of the .qmd: a cross-reference that closes a parenthesis
    after other text is dropped with its comma, a parenthesis of cross-references only is dropped,
    and any other cross-reference is written as the document numbers it ("Table 8")."""
    s = re.sub(r",\s*" + _XREF + r"(?=\))", "", s)
    s = re.sub(r"\s*\((?:see )?" + _XREF + r"(?:(?:, | and )" + _XREF + r")*\)", "", s)
    s = re.sub(_XREF, lambda m: xr[m.group(0)[1:]], s)
    return re.sub(r"\s+", " ", s).strip()


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
    """The ``GroundTruthAnnex`` of PTP-001 Version 2.0."""
    import tables as T
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    from annex_contract.concepts import Concept, ConceptStore
    from annex_contract.discourse import DocumentRelationship, ExplicitNonClaim
    from annex_contract.results import ControlStrategyElement, ModularContribution
    from annex_contract.summaries import ReportSection, ReportStatement, TransferGap

    src = _source()
    _check_sections(src)
    prose_src = normalize(re.sub(r"```\{python\}.*?```", " ", src, flags=re.S))
    ns, _ = G.qmd_namespace(QMD)
    ct = G.qmd_ctables(QMD)
    text = G._document_text(FILE)
    meta = G.meta
    if (ns["DOC"], ns["UO"]) != (DOC, None):
        raise ValueError(f"{DOC}: the .qmd is not the transfer plan it is annexed as")

    captions = {lab: tab.caption for lab, (tab, _) in ct.items()}
    captions.update({lab: _md_caption(src, lab) for lab in FLAT})
    xr = _xrefs(src, text, captions)

    def render(s):
        return re.sub(r"\s+", " ", re.sub(_XREF, lambda m: f" {xr[m.group(0)[1:]]} ", s)).strip()

    def q(s):
        """A span of the .qmd prose as it renders. ``s`` must be copied from the .qmd with its inline
        expressions and cross-references, so a typed value fails here instead of grounding by
        coincidence."""
        if normalize(s) not in prose_src:
            raise ValueError(f"{DOC}: not a span of the .qmd prose: {s[:100]!r}")
        return re.sub(r"\s+", " ", _smart(render(G.qmd_inline(ns, s)))).strip()

    def t(s):
        """Statement text in .qmd form: its inline expressions evaluated in the plan's namespace."""
        return re.sub(r"\s+", " ", _smart(G.qmd_inline(ns, _plain(s)), runs=False)).strip()

    def ref(sec, quote, table=None, rows=None):
        r = G.ref(DOC, FILE, _sid(sec), SEC[sec][-1], quote,
                  table_title=None if table is None else table.caption,
                  table_id=None if table is None else f"{DOC}_tab_{table.label[4:].replace('-', '_')}",
                  table_header=None if rows is None else rows.header)
        r.heading_path = list(SEC[sec])
        return r

    def keyed(label, keys, name_of, cell):
        """The rendered rows of the CTable the plan printed under ``label``, keyed. Cell ``cell`` of
        every row must name its own record: a mis-keyed row grounds and attests the wrong thing."""
        tab = ct[label][0]
        rows = G.ctable_rows(tab, keys)
        bad = [k for k, row in rows.items() if _nomark(_cells(row)[cell]) != name_of(k)]
        if bad:
            raise ValueError(f"{DOC} {label}: rows keyed to records they do not name: {bad}")
        return tab, rows

    def flat_rows(label):
        """``(table, rows, cells)`` of a pipe table the plan prints: ``rows`` keyed by the first cell
        as the DOCX reads them (cross-references rendered), ``cells`` the source cells of each row."""
        lines = _printed(src, ns, label)
        raw = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines]
        rows = G.RowQuotes((r[0], G._join_cells([render(c) for c in r])) for r in raw[2:])
        if len(rows) != len(raw) - 2:
            raise ValueError(f"{DOC} {label}: two rows share a first cell")
        rows.header = G._join_cells([render(c) for c in raw[0]])
        return SimpleNamespace(label=label, caption=captions[label]), rows, {r[0]: r for r in raw[2:]}

    # ---- names and data the plan uses ----------------------------------------------------------
    steps = list(ns["steps"])                                       # train order
    uo_of = {k: P.CFG.unit_op(k) for k in steps}
    num_of = {k: uo_of[k].step for k in steps}
    key_of_num = {str(n): k for k, n in num_of.items()}
    title_of = dict(P.UNIT_OP_TITLES)
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))
    reg = P.cqa_reg.set_index("key")

    def report_of(k):
        return f"PCR-{num_of[k]:03d}"

    # ---- the rendered tables ---------------------------------------------------------------------
    pk_t, pk_rows, pk_cells = flat_rows("tbl-package")
    tr_t, tr_raw, tr_cells = flat_rows("tbl-train")
    trow = G.RowQuotes((key_of_num[n], r) for n, r in tr_raw.items())
    trow.header = tr_raw.header
    role_of = {key_of_num[n]: c[2] for n, c in tr_cells.items()}
    eq_t, eqrow, eq_cells = flat_rows("tbl-equivalency")
    sc_t, sc_raw, sc_cells = flat_rows("tbl-scope")
    srow = G.RowQuotes((key_of_num[n], r) for n, r in sc_raw.items())
    srow.header = sc_raw.header
    gp_t, gprow, gp_cells = flat_rows("tbl-gaps")
    dl_t, dlrow, dl_cells = flat_rows("tbl-deliverables")
    for k in steps:
        if (tr_cells[str(num_of[k])][1], sc_cells[str(num_of[k])][1]) != (title_of[k], uo_of[k].name):
            raise ValueError(f"{DOC}: the train or scope row of Step {num_of[k]} does not name {k}")

    cq_df = ct["tbl-cqa"][1]
    key_of_cqa = {v: k for k, v in names.items()}
    ckeys = [key_of_cqa[c] for c in cq_df["CQA"]]
    cq_t, crow = keyed("tbl-cqa", ckeys, lambda k: names[k], 1)
    cq = cq_df.assign(key=ckeys).set_index("key")
    pbs_t, prow = keyed("tbl-parameters-by-step", G._pbs_keys(), lambda kn: kn[1], 1)
    sop_df = ct["tbl-sops"][1]
    sop_t, soprow = keyed("tbl-sops", list(sop_df["Reference"]), str, 1)
    sop_title = dict(zip(sop_df["Reference"], sop_df["Title"]))
    me_df = ct["tbl-methods"][1]
    me_t, merow = keyed("tbl-methods", list(me_df["Reference"]), str, 0)
    me = me_df.set_index("Reference")
    ro_df = ct["tbl-roles"][1]
    ro_t, rorow = keyed("tbl-roles", list(ro_df["Function"]), str, 1)
    ch_df = ct["tbl-chronology"][1]
    ch_t, chrow = keyed("tbl-chronology", list(ch_df["Plan"]), str, 2)
    tb = G.md_string_rows(P.title_block(DOC, ns["UO_TITLE"]))      # the title block, by field
    title_t = SimpleNamespace(label="tbl-title-block", caption=None)
    amvs = [r for r in sop_df["Reference"] if r.startswith("AMV-")]

    # ---- record factories --------------------------------------------------------------------------
    A, ST = [], []

    def add(subj, pred, obj, txt, refs):
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{DOC}-A{len(A) + 1:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=txt, source_references=refs, metadata=meta()))

    def st(sec, txt, refs):
        ST.append((SEC[sec][0], ReportStatement(
            statement_id=f"{DOC}-S{len(ST) + 1:03d}",
            statement_text=txt if txt.endswith(".") else txt + ".", confidence="high",
            review_status="accepted", source_references=refs)))

    def sq(sec, src_, txt=None, also=()):
        """A statement of one prose span: ``src_`` is its .qmd source, ``txt`` the statement in .qmd
        form (the span itself where it reads on its own). ``also`` cites further (section, source)
        spans the statement draws on, so every clause of it has its span."""
        st(sec, t(txt if txt else src_), [ref(sec, q(src_))] + [ref(s_, q(x)) for s_, x in also])

    def tref(sec, tab, rows, key):
        return ref(sec, rows[key], tab, rows)

    # ==== entities ===================================================================================
    # -- sites: the title block names each, and Section 3 states its role
    Q_S1 = "The sending site is the development site of `{python} COMPANY` in `{python} SENDING_LOCATION`."
    Q_S2 = "The receiving site is the commercial drug substance site of `{python} COMPANY` in `{python} RECEIVING_LOCATION`."
    sites = [
        S.ManufacturingSite(site_id="site:cambridge", site_name=P.SENDING_SITE, site_role="sending",
                            location=P.SENDING_LOCATION,
                            source_references=[ref("title", tb["Development site"], title_t, tb),
                                               ref("sites", q(Q_S1))], metadata=meta()),
        S.ManufacturingSite(site_id="site:grafton", site_name=P.RECEIVING_SITE, site_role="receiving",
                            location=P.RECEIVING_LOCATION,
                            source_references=[ref("title", tb["Commercial drug substance site"], title_t, tb),
                                               ref("sites", q(Q_S2))], metadata=meta()),
    ]

    # -- steps: each on its row of the process train table, the scope table and the chronology table
    plan_of_step = {k: f"PCP-{num_of[k]:03d}" for k in steps}
    step_ents = []
    for k in steps:
        step_ents.append(S.ProcessStep(
            step_id=f"step:{k}", step_name=title_of[k], step_number=str(num_of[k]),
            unit_operation=title_of[k], description=role_of[k],
            source_references=[tref("product", tr_t, trow, k), tref("sdm", sc_t, srow, k),
                               tref("schedule", ch_t, chrow, plan_of_step[k])],
            metadata=meta()))

    # -- the step-attribute links that the principal role of each step states
    links = [(k, a) for k in steps for a in ckeys if ATTR_TOKEN[a] in role_of[k]]
    Q_GLYCAN = "The glycan is formed in the production bioreactor."
    Q_AGG_LOWPH = "Aggregate forms in the culture and again at low pH, during the elution from Protein A and the viral inactivation hold."
    Q_CEX_AGG = "Cation exchange reduces it, because the resin binds the high molecular weight species more strongly than the monomer, and these species stay on the column when the pool is cut."
    Q_FRAG = "The CQA register of PCMP-001 Version 2.0 assigns fragments to harvest, because proteases released from lysed cells clip the antibody in culture and during the harvest hold (PCMP-001 §3)."
    Q_VIR_REG = "The register assigns the XMuLV requirement to `{python} x_set_by` and the MVM requirement to `{python} m_set_by`, but each requirement is met by the sum of the claims of several steps (@sec-control)."
    # the steps at which the document says aggregate forms at low pH
    lowph = [k for k in steps if k in ("protein_a", "viral_inactivation")]
    links += [(k, "aggregates_hmw") for k in lowph if (k, "aggregates_hmw") not in links]
    link_prose = {(k, a): ("product", Q_GLYCAN) for k, a in links
                  if k == "bioreactor" and ATTR_TOKEN[a] == "glycan"}
    link_prose.update({(k, "aggregates_hmw"): ("product", Q_AGG_LOWPH) for k in lowph})
    link_prose[("cex", "aggregates_hmw")] = ("product", Q_CEX_AGG)
    link_prose[("harvest", "fragments_lmw")] = ("product", Q_FRAG)
    link_prose[(ns["_reg"].loc["lrv_xmulv", "set_by"], "lrv_xmulv")] = ("product", Q_VIR_REG)
    link_prose[(ns["_reg"].loc["lrv_mvm", "set_by"], "lrv_mvm")] = ("product", Q_VIR_REG)
    if not set(link_prose) <= set(links):
        raise ValueError(f"{DOC}: a prose link names no step-attribute link: {set(link_prose) - set(links)}")
    steps_of_attr = {a: [f"{title_of[k]} (Step {num_of[k]})" for k in steps if (k, a) in links] for a in ckeys}

    # -- quality attributes: each on its row of the attribute table
    mi = ns["_mi"]                                                   # the method record, by id
    method_of = {a: m for m, attrs in G.METHOD_ATTRS.items() for a in attrs if m in amvs}
    # the record that measures aggregate here is the one transferred: "AMV-3221 for aggregate"
    if "Aggregate" not in mi.loc["AMV-3221", "name"] or "AMV-3221" not in me.index:
        raise ValueError(f"{DOC}: AMV-3221 is no longer the transferred method for aggregate")
    method_of["aggregates_hmw"] = "AMV-3221"
    note_sents = re.split(r"(?<=\.) ", cq_t.notes[0][1])
    q_rule = next(s for s in note_sents if s.startswith("The two viral clearance attributes"))
    q_frag_crit = next(s for s in note_sents if "criterion for fragments" in s)
    Q_C24 = "The sponsor set the criterion for fragments, measured by non-reduced capillary electrophoresis with sodium dodecyl sulfate (nrCE-SDS), when fragments joined the CQA register of PCMP-001 Version 2.0."
    Q_K21 = 'Its criterion, no more than `{python} f"{dna_crit:g}"` ng per dose, is the acceptable range that the A-Mab case study claims, and the case study notes that DNA is consistently cleared from the process'
    attr_extra = {"fragments_lmw": [ref("product", q_frag_crit), ref("changes", q(Q_C24))],
                  "residual_dna": [ref("control", q(Q_K21))],
                  "lrv_xmulv": [ref("product", q_rule)], "lrv_mvm": [ref("product", q_rule)]}
    attrs = []
    for key in ckeys:
        c = cq.loc[key]
        viral = key.startswith("lrv_")
        why = (f"{q_rule} Tool #1 score {c['Tool #1']}." if viral
               else f"A-Mab Tool #1 score {c['Tool #1']}, the product of impact and uncertainty.")
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=names[key], attribute_type="CQA",
            unit=reg.loc[key, "unit"], acceptance_criteria=[f"{c['Acceptance']} (drug substance)"],
            analytical_method=method_of.get(key), associated_steps=steps_of_attr[key],
            rationale_for_criticality=why, criticality_level=c["Criticality"],
            tool1_score=int(c["Tool #1"]),
            source_references=[tref("product", cq_t, crow, key)] + attr_extra.get(key, []),
            metadata=meta()))

    # -- parameters: each on its row of the parameter table, with the values in force
    preg = P.csv("parameter_classification.csv")
    params, pid = [], {}
    for (k, name), row in prow.items():
        uo = uo_of[k]
        pk = next(x.key for x in uo.parameters if x.name == name)
        r = preg[(preg["step"] == uo.step) & (preg["parameter"] == name)].iloc[0]
        c = _cells(row)                       # Step | Parameter | Unit | Set-point | NOR | Range | Class
        if (c[2], c[6]) != (r["unit"], r["classification"]):
            raise ValueError(f"{pbs_t.label}: the row of {name} does not read {r['unit']}, {r['classification']}")
        u = r["unit"]

        def wu(v):
            return f"pH {v}" if u == "pH" else f"{v} {u}"
        nor = c[5] if _nomark(c[4]) == "as characterized" else _nomark(c[4])
        pid[(k, name)] = f"param:{k}_{pk}"
        params.append(S.ProcessParameter(
            parameter_id=pid[(k, name)], parameter_name=name, parameter_type=c[6], unit=u,
            target_value=wu(_nomark(c[3])), NOR=wu(nor), PAR=wu(c[5]),
            associated_step=f"{title_of[k]} (Step {uo.step})",
            study_type="multivariate" if r["study"] == "multivariate" else "univariate",
            rationale_for_criticality=(f"Classified {c[6]} in {report_of(k)} under SOP-4001; PTP-001 "
                                       f"carries the class of the report and does not re-derive it."),
            source_references=[tref("process", pbs_t, prow, (k, name))], metadata=meta()))
    if len(params) != ns["n_par"]:
        raise ValueError(f"{DOC}: {len(params)} parameter rows against {ns['n_par']} parameters in scope")

    # -- analytical methods: every method validation of the procedures table
    Q_C27 = "The nrCE-SDS method (SOP-3015, AMV-3020) is added to the methods to transfer (@sec-methods and @tbl-gaps), following the analytical method decision `{python} amd_id` of `{python} amd_date` as PCMP-001 Version 2.0 §7.8 sets it."
    Q_C29 = "The procedures and method validations in @tbl-sops now also include the product titre method by Protein A affinity HPLC (SOP-3016, AMV-3021), because the titre sets the protein load of a capture run, and the method for aggregate by SEC-HPLC (AMV-3221)."
    Q_C31 = "Beside the methods of the Version 1.0 table, it now includes the charge variant method by icIEF (AMV-3013), the residual DNA method by qPCR (AMV-3014) and the product titre method (AMV-3021)."
    Q_A3 = "The two infectivity titre assays of that record (AMV-3017 and AMV-3018) are not transferred."
    Q_A5 = "The host cell protein ELISA (AMV-3012) supports the host cell protein clearance argument across all three chromatography steps, and every judgement of host cell protein against an intermediate acceptance criterion rests on its results."
    Q_A8 = "Two records cover SEC, AMV-3011 for size variants and AMV-3221 for aggregate (@tbl-sops)."
    Q_A10 = "The product titre method by Protein A affinity HPLC (AMV-3021, under SOP-3016) measures the antibody in a clarified harvest."
    Q_A12 = "The master plan PCMP-001 Version 2.0 sets nrCE-SDS (AMV-3020, under SOP-3015) as the method for fragments, following the analytical method decision `{python} amd_id` of `{python} amd_date`, and keeps SEC as the method for aggregate (PCMP-001 §7.8)."
    Q_A14 = "The nrCE-SDS method is transferred and requalified like the methods in @tbl-methods."
    meth_prose = {"AMV-3012": [Q_A5], "AMV-3013": [Q_C31], "AMV-3014": [Q_C31], "AMV-3017": [Q_A3],
                  "AMV-3018": [Q_A3], "AMV-3011": [Q_A8], "AMV-3221": [Q_C29, Q_A8],
                  "AMV-3021": [Q_C29, Q_A10], "AMV-3020": [Q_C27, Q_A12, Q_A14]}
    meth_sec = {Q_A5: "methods", Q_C31: "changes", Q_A3: "methods", Q_A8: "methods", Q_C29: "changes",
                Q_A10: "methods", Q_C27: "changes", Q_A12: "methods", Q_A14: "methods"}
    attrs_of = {m: [a for a in ckeys if method_of.get(a) == m] for m in amvs}
    analyte = {"AMV-3011": ["size variants"], "AMV-3015": ["turbidity"],
               "AMV-3019": ["protein concentration"], "AMV-3021": ["product titre in clarified harvest"]}
    methods = []
    for m in amvs:
        name = me.loc[m, "Analytical method"] if m in me.index else sop_title[m]
        refs = [tref("process", sop_t, soprow, m)]
        if m in me.index:
            refs.append(tref("methods", me_t, merow, m))
        refs += [ref(meth_sec[x], q(x)) for x in meth_prose.get(m, [])]
        methods.append(S.AnalyticalMethod(
            method_id=m, method_name=name, method_type=G.METHOD_TYPE.get(m, METHOD_TYPE_LOCAL.get(m)),
            analytes=[names[a] for a in attrs_of[m]] or analyte.get(m, []),
            associated_attributes=[f"attr:{a}" for a in attrs_of[m]],
            validation_status="verification-qualified" if "verification-qualified" in name else "validated",
            source_references=refs, metadata=meta()))

    # -- equipment: the two trains the plan compares
    Q_C19 = "The manufacturing-scale reference is the development train at the sending site (@sec-sdm)."
    Q_M18 = "These batches come from the development train, the manufacturing-scale train at the sending site whose batches are the manufacturing-scale reference of each step's qualification (PCMP-001 §7.1)."
    Q_C22 = "The commercial train is now compared with the development train on the engineering batches, and the comparison is recorded in the engineering batch reports (@tbl-gaps)."
    Q_M33 = "The receiving site will run engineering batches on the commercial train before the qualification campaign starts."
    eq_first = next(iter(eqrow))                                    # "Equipment train and scale"
    equipment = [
        S.Equipment(equipment_id="equip:development_train", equipment_name="development train",
                    equipment_type="manufacturing-scale equipment train, the manufacturing-scale "
                                   "reference of the scale-down model qualification",
                    site_name=P.SENDING_SITE,
                    source_references=[ref("sdm", q(Q_M18)), ref("changes", q(Q_C19)),
                                       tref("equivalency", eq_t, eqrow, eq_first)], metadata=meta()),
        S.Equipment(equipment_id="equip:commercial_train", equipment_name="commercial equipment train",
                    equipment_type="commercial-scale equipment train at full working volume",
                    site_name=P.RECEIVING_SITE,
                    source_references=[tref("equivalency", eq_t, eqrow, eq_first), ref("sdm", q(Q_M33)),
                                       ref("changes", q(Q_C22))], metadata=meta()),
    ]

    # -- control strategy elements
    Q_K3 = "Parameter classification places every process parameter in a class and attaches a control to it."
    Q_K4 = "In-process limits bound what each intermediate may deliver to the next step."
    Q_K5 = "Release testing confirms the attributes of the drug substance against @tbl-cqa, with two exceptions."
    Q_K6 = "Residual DNA and viral clearance are met through the clearance that the characterization demonstrates, and no batch test measures them against their criteria."
    Q_K7 = "Classification is performed under the parameter classification procedure SOP-4001 on the evidence of the characterization studies."
    Q_K14 = "In the characterization, each step output on which a drug substance criterion depends is judged against an intermediate acceptance criterion, where PCMP-001 Version 2.0 §7.3 defines one."
    Q_R12 = "The batch record must carry every parameter classified as a critical or a well-controlled critical process parameter, `{python} n_crit` in all, with its set-point and its NOR."
    Q_R13 = "It must also carry the in-process controls and the sampling points that support them."
    Q_K24 = "The criterion is met through the clearance that the step reports show, and the master report PCMR-001 assesses the capability of the drug substance against it (PCMP-001 §7.3)."
    Q_K39 = "The load conditions on which each claim depends, such as the pH and the conductivity of the anion exchange load, are controlled by the batch record."
    cs, cs_at = [], {}

    def element(sec, desc, controls, ctype, quotes, uo=None):
        cs.append(ControlStrategyElement(
            element_id=f"{DOC}-CS{len(cs) + 1:02d}", description=desc, unit_operation=uo,
            controls=controls, control_type=ctype,
            source_references=[ref(s_, q(x)) for s_, x in quotes], metadata=meta()))
        cs_at.setdefault(sec, []).append(cs[-1])

    element("control", "Parameter classification places every process parameter in a class and attaches a "
            "control to it; it is performed under SOP-4001 on the evidence of the characterization studies.",
            "every process parameter", "parameter classification",
            [("control", Q_K3), ("control", Q_K7)])
    element("control", "In-process limits bound what each intermediate may deliver to the next step: each step "
            "output on which a drug substance criterion depends is judged against an intermediate acceptance "
            "criterion where PCMP-001 Version 2.0 §7.3 defines one.",
            "each intermediate", "in-process limits (intermediate acceptance criteria)",
            [("control", Q_K4), ("control", Q_K14)])
    element("control", "Release testing confirms the attributes of the drug substance against the drug substance "
            "acceptance criteria, except residual DNA and viral clearance.",
            "the drug substance quality attributes", "release testing", [("control", Q_K5)])
    element("process", t("The master batch record carries every CPP and WC-CPP, `{python} n_crit` in all, with "
                         "its set-point and its NOR, and the in-process controls and the sampling points that "
                         "support them."),
            "the critical and well-controlled critical process parameters", "master batch record",
            [("process", Q_R12), ("process", Q_R13)])
    element("control", "Residual DNA is met through the clearance that the step reports show; no batch test "
            "measures it, and PCMR-001 assesses the capability of the drug substance against its criterion.",
            names["residual_dna"], "process clearance", [("control", Q_K24), ("control", Q_K6)])
    element("control", "The load conditions on which each viral clearance claim depends, such as the pH and the "
            "conductivity of the anion exchange load, are controlled by the batch record.",
            "the load conditions of each viral clearance claim", "batch record", [("control", Q_K39)])

    # -- the modular viral clearance claims: each claimed step, on the sentence of its virus and the
    #    attribute row that carries the cumulative requirement
    Q_X = 'For XMuLV, `{python} x_claim_txt`, a sum of `{python} f"{x_sum:g}"` against a cumulative requirement of `{python} f"{x_req:g}"`.'
    Q_M = 'For MVM, `{python} m_claim_txt`, a sum of `{python} f"{m_sum:g}"` against `{python} f"{m_req:g}"`.'
    contributions = []
    for cqa, claims, tot, req, sent in (("lrv_xmulv", ns["x_claims"], ns["x_sum"], ns["x_req"], Q_X),
                                        ("lrv_mvm", ns["m_claims"], ns["m_sum"], ns["m_req"], Q_M)):
        if abs(sum(v for _, v in claims) - tot) > 1e-9:
            raise ValueError(f"{DOC}: the {cqa} claims do not sum to {tot}")
        for k, v in claims:
            contributions.append(ModularContribution(
                contribution_id=f"{DOC}-VC{len(contributions) + 1:02d}", quantity=names[cqa],
                unit_operation=title_of[k], step_value=f"{v:g}", cumulative_value=f"{tot:g}",
                requirement=f"{req:g}", unit="log10",
                contributing_steps=[title_of[o] for o, _ in claims if o != k],
                source_references=[ref("control", q(sent)), tref("product", cq_t, crow, cqa)],
                metadata=meta()))

    # -- explicit non-claims, by section
    nc, nc_at = [], {}

    def nclaim(sec, subject, statement, quotes, rationale=None, elsewhere=None, uo=None):
        nc.append(ExplicitNonClaim(
            non_claim_id=f"{DOC}-NC{len(nc) + 1:02d}", subject=subject, unit_operation=uo,
            statement=statement, rationale=rationale, handled_elsewhere=elsewhere,
            source_references=[ref(s_, q(x)) for s_, x in quotes], metadata=meta()))
        nc_at.setdefault(sec, []).append(nc[-1])

    Q_P12 = "Three activities are outside the scope of this plan."
    nclaim("purpose", "drug product manufacture, filling and finishing",
           "Drug product manufacture, filling and finishing are outside the scope of PTP-001; they are "
           "transferred under a separate plan.",
           [("purpose", "Drug product manufacture, filling and finishing are transferred under a separate plan."),
            ("purpose", Q_P12)], elsewhere="a separate transfer plan")
    nclaim("purpose", "cell bank manufacture and testing",
           "Cell bank manufacture and testing are outside the scope of PTP-001; they are governed by their "
           "own records.",
           [("purpose", "Cell bank manufacture and testing are governed by their own records."), ("purpose", Q_P12)],
           elsewhere="the records of the cell banks")
    nclaim("purpose", "execution of the process performance qualification campaign",
           "The execution of the PPQ campaign is outside PTP-001; the campaign is executed under its own "
           "protocol and reported separately.",
           [("purpose", "The execution of the process performance qualification (PPQ) campaign is also outside this plan."),
            ("purpose", Q_P12),
            ("purpose", "The campaign will be executed under its own protocol and reported separately.")],
           elsewhere="the qualification protocol and its report")
    nclaim("changes", "step acceptance criteria", "PTP-001 set no acceptance criteria for the step outputs.",
           [("changes", "This plan set no step criteria.")],
           elsewhere="the intermediate acceptance criteria of PCMP-001 Version 2.0 §7.3")
    nclaim("product", "separation of glycosylation variants by the purification steps",
           "None of the platform purification steps separates glycosylation variants under the conditions "
           "used, so control of the glycan attributes sits in cell culture.",
           [("product", "None of the platform purification steps separates glycosylation variants under the conditions used here"),
            ("product", "The glycan takes no part in that binding, so Protein A captures every glycan variant alike."),
            ("product", "Fucose, galactose and mannose carry no charge, so the two ion exchange steps, which separate by charge, do not resolve these variants either.")],
           rationale="Protein A binds the Fc region, where the glycan takes no part in the binding, and the "
                     "glycan sugars carry no charge, so neither affinity capture nor ion exchange resolves "
                     "the variants.", elsewhere="the production bioreactor (cell culture)")
    nclaim("product", "cumulative viral clearance in a step report",
           "No single step report claims the cumulative viral clearance of the train; the master report "
           "PCMR-001 states it.",
           [("product", "Each step is studied and claimed on its own, and no single step report claims the cumulative clearance of the train."),
            ("product", "The master report PCMR-001 states the cumulative clearance.")],
           rationale="The three viral clearance claims are modular in the sense of ICH Q5A.",
           elsewhere="PCMR-001")
    nclaim("equivalency", "measured outcome of the site equivalency assessment",
           "The site equivalency assessment is prospective and states no measured outcome: each row states "
           "what is compared and how a difference is managed.",
           [("equivalency", "The assessment is prospective."),
            ("equivalency", "Each row therefore states what is compared and how a difference is managed, not a measured outcome.")])
    nclaim("sdm", "scale offset of fragments and viral clearance",
           "The scale-down qualification does not compare fragments or viral clearance at both scales, so "
           "their offset is unknown, not zero.",
           [("sdm", "The qualification does not compare fragments or viral clearance at both scales."),
            ("sdm", "Their offset is unknown, not zero.")],
           rationale="Their representativeness rests on the mechanism of each step for fragments and on the "
                     "virus spiking studies for viral clearance (PCMP-001 §7.1).")
    Q_M30 = "The risk assessment RA-001 assigned no parameter of harvest (Step `{python} s_har`) or UF/DF (Step `{python} s_ufdf`) to multivariate study, so neither step carries a designed experiment."
    Q_G7 = "The gap on harvest and UF/DF will still be open when the characterization campaign ends, because no multivariate design is planned for either step at any point in the programme."
    nclaim("sdm", "designed experiment at harvest and UF/DF",
           "Neither harvest nor UF/DF carries a designed experiment, and none is planned for either step at "
           "any point in the programme.", [("sdm", Q_M30), ("gaps", Q_G7)],
           rationale="RA-001 assigned no parameter of either step to multivariate study.",
           elsewhere="univariate work and platform experience")
    nclaim("sdm", "interactions between the parameters of harvest and UF/DF",
           "No interaction between two parameters of harvest or of UF/DF is estimated.",
           [("sdm", "Their ranges rest on univariate work and on platform experience, and no interaction between two of their parameters is estimated (@sec-gaps).")])
    nclaim("methods", "transfer of the two infectivity titre assays",
           "The two infectivity titre assays (AMV-3017 and AMV-3018) are not transferred; they stay with the "
           "virus spiking studies at small scale at the sending site.",
           [("methods", Q_A3),
            ("methods", "They measure viral clearance in the virus spiking studies, which stay at small scale at the sending site (@tbl-gaps)."),
            ("changes", "It no longer includes the two infectivity titre assays (AMV-3017 and AMV-3018), which stay with the virus spiking studies at small scale (@sec-methods).")],
           elsewhere="the virus spiking studies at small scale, at the sending site")
    Q_A9 = "AMV-3221 is the one transferred, and @tbl-methods gives its qualified performance."
    nclaim("methods", "transfer of the SEC size variant method AMV-3011",
           "Of the two records that cover SEC, AMV-3011 for size variants is not the one transferred; "
           "AMV-3221 for aggregate is.", [("methods", Q_A8), ("methods", Q_A9)], elsewhere="AMV-3221")
    Q_A16 = "Its validation is AMV-3020 in @tbl-sops, from which the transfer protocol takes the values to be reproduced."
    nclaim("methods", "qualified performance of nrCE-SDS in the method record",
           "The record of qualified method performance holds no performance row for nrCE-SDS.",
           [("methods", "The method record holds no performance row for it."), ("methods", Q_A16)],
           elsewhere="its validation AMV-3020, from which the transfer protocol takes the values")
    nclaim("control", "batch testing of residual DNA and viral clearance against their criteria",
           "No batch test measures residual DNA or viral clearance against their criteria; both are met "
           "through the clearance that the characterization demonstrates.",
           [("control", Q_K6),
            ("changes", "Release testing does not test residual DNA or viral clearance against their criteria (@sec-control).")],
           elsewhere="the clearance demonstrated in the characterization")
    nclaim("control", "margin in the derivation of the intermediate acceptance criteria",
           "No margin is applied when the drug substance criterion is carried backward through the train.",
           [("control", "No margin is applied.")])
    nclaim("control", "study data in the derivation of the intermediate acceptance criteria",
           "The derivation of the intermediate acceptance criteria uses no data from the studies it judges.",
           [("control", "The derivation uses no data from the studies it judges.")])
    nclaim("control", "intermediate acceptance criterion for residual DNA",
           "Residual DNA has a drug substance criterion but no intermediate acceptance criterion.",
           [("control", "Residual DNA has a drug substance criterion but no intermediate acceptance criterion (PCMP-001 §7.3).")],
           elsewhere="the drug substance criterion, against which PCMR-001 assesses capability")
    Q_K26 = 'A release test could not show it, because the qPCR method (AMV-3014) quantifies DNA only down to `{python} f"{dna_loq:g}"` pg/mg, which is `{python} f"{dna_loq_dose:g}"` ng per dose, `{python} f"{dna_loq_x:,.0f}"` times the criterion.'
    nclaim("control", "release testing of residual DNA", "Residual DNA is not tested at release.",
           [("control", "It is not tested at release."), ("control", Q_K26)],
           rationale=t('The qPCR method (AMV-3014) quantifies DNA only down to `{python} f"{dna_loq:g}"` pg/mg, '
                       'which is `{python} f"{dna_loq_dose:g}"` ng per dose, `{python} f"{dna_loq_x:,.0f}"` times '
                       'the criterion.'),
           elsewhere="the clearance that the step reports show")
    Q_K27 = "XMuLV clearance rests on `{python} n_x` claimed steps and MVM clearance on `{python} n_m`, because the low-pH step carries no MVM claim."
    Q_K28 = "Low pH disrupts the lipid envelope of an enveloped virus such as XMuLV, and a parvovirus such as MVM has no envelope."
    nclaim("control", "MVM clearance claim of the low-pH step", "The low-pH step carries no MVM claim.",
           [("control", Q_K27), ("control", Q_K28)],
           rationale="Low pH disrupts the lipid envelope of an enveloped virus, and a parvovirus such as MVM "
                     "has no envelope.", uo=title_of["viral_inactivation"])
    nclaim("control", "viral clearance credit above a step's claim", "No step is credited above its claim.",
           [("control", "No step is credited above its claim (PCMP-001 §7.4).")],
           rationale="Each claimed step is held to its platform claim (PCMP-001 §7.4).")
    nclaim("ppq", "execution of the process performance qualification",
           "PTP-001 does not execute the process performance qualification; it states what must be in place "
           "before the campaign may start and the strategy the campaign will follow.",
           [("ppq", "This plan does not execute that demonstration."),
            ("ppq", "It states what must be in place before the campaign may start and the strategy the campaign will follow.")],
           elsewhere="the qualification campaign, under its own protocol")
    Q_Q7 = "Every parameter will be held at its set-point in @tbl-parameters-by-step, and no deliberate excursion will be run."
    nclaim("ppq", "deliberate excursions in the qualification campaign",
           "No deliberate excursion will be run in the qualification campaign.", [("ppq", Q_Q7)])
    nclaim("ppq", "challenge of the edges of the characterized ranges",
           "The qualification campaign will not challenge the edges of the characterized ranges.",
           [("ppq", "The campaign will not challenge the edges of the characterized ranges."),
            ("ppq", "Those edges are established at small scale, and a qualification batch is not a characterization experiment.")],
           rationale="The edges are established at small scale, and a qualification batch is not a "
                     "characterization experiment.", elsewhere="the characterization studies at small scale")
    nclaim("ppq", "variability of commercial manufacture over its life",
           "A qualification campaign of this size cannot capture the variability that commercial manufacture "
           "will show over its life.",
           [("ppq", "However, a campaign of this size cannot capture the variability that commercial manufacture will show over its life.")],
           elsewhere="continued process verification")
    nclaim("ppq", "acceptance criteria of the qualification campaign",
           "PTP-001 does not state the acceptance criteria of the qualification campaign; the qualification "
           "protocol states them.",
           [("ppq", "The acceptance criteria of the campaign will also be stated in the qualification protocol.")],
           elsewhere="the qualification protocol")
    nclaim("roles", "named persons of the transfer team",
           "PTP-001 names no person; the roster of the transfer team, kept outside the plan, assigns a "
           "named person to each function.",
           [("roles", "A named person is assigned to each function in the roster of the transfer team, which is kept outside this plan and revised as the team changes.")],
           elsewhere="the roster of the transfer team")
    nclaim("schedule", "calendar dates of the deliverables",
           "The deliverables are ordered by dependency, not by calendar dates; the transfer project schedule "
           "holds the planned dates.",
           [("schedule", "The order is one of dependency, not a calendar."),
            ("schedule", "The transfer project schedule holds the planned dates and is revised as the work proceeds.")],
           elsewhere="the transfer project schedule")

    # -- document relationships: the rows of the package table, the title block, then the prose
    rels = []

    def relation(kind, target, statement, refs):
        rels.append(DocumentRelationship(
            relationship_id=f"{DOC}-R{len(rels) + 1:02d}", kind=kind, source_document_id=DOC,
            target_document_ref=target, statement=statement, source_references=refs, metadata=meta()))

    for target, row in pk_rows.items():
        _, cls, subject = pk_cells[target]
        relation("references", target, f"{target} ({cls}: {subject}) is a document of the A-Mab "
                 f"characterization package, of which PTP-001 is the parent.", [tref("purpose", pk_t, pk_rows, target)])
    relation("supersedes", f"{DOC} Version {P.REV1['rev']}", "Version 2.0 supersedes Version 1.0 of the plan.",
             [ref("title", tb["Supersedes"], title_t, tb)])
    Q_RA = "The risk assessment RA-001 sets the scope of each study."
    relation("references", "RA-001", "The risk assessment RA-001 sets the scope of each characterization study.",
             [ref("purpose", q(Q_RA))])
    relation("references", "PCMP-001", "The master plan PCMP-001 sets the framework that the step plans apply.",
             [ref("purpose", q("The master plan PCMP-001 sets the framework that the step plans apply"))])
    relation("references", "PCMR-001", "The master report PCMR-001 consolidates the characterization reports.",
             [ref("purpose", q("the master report PCMR-001 consolidates the reports"))])
    Q_C2 = "Version 2.0 replaces it under corrective action CA3 of the QA investigation `{python} inv_id`, which reissues this plan, the risk assessment RA-001, the step reports PCR-003 to PCR-010 and the master report PCMR-001 at Version 2.0."
    relation("references", ns["inv_id"], t("The investigation `{python} inv_id` is the reason for Version 2.0 of "
                                            "PTP-001, which its corrective action CA3 reissues."),
             [ref("purpose", q("The investigation `{python} inv_id` is the reason for this revision")),
              ref("changes", q(Q_C2))])
    relation("references", ns["inv2_id"], t("The investigation `{python} inv2_id` concerns the adequacy of the "
                                             "response-surface models in the step reports."),
             [ref("purpose", q("the investigation `{python} inv2_id` concerns the adequacy of the response-surface models in the step reports"))])
    relation("references", ns["amd_id"], "The analytical method decision under which PCMP-001 Version 2.0 sets "
             "nrCE-SDS as the method for fragments; nrCE-SDS is added to the methods to transfer.",
             [ref("methods", q(Q_A12))])
    Q_K40 = "The master report PCMR-001 states the cumulative clearance and compares it with the acceptance criteria in @tbl-cqa."
    relation("references", "PCMR-001", "The master report PCMR-001 states the cumulative viral clearance and "
             "compares it with the drug substance acceptance criteria.", [ref("control", q(Q_K40))])

    def section(key, **kw):
        return S.SectionEntityExtraction(document_id=DOC, section_id=_sid(key), **kw)

    entities = [
        section("purpose", sites=sites, document_relationships=rels, non_claims=nc_at["purpose"]),
        section("changes", non_claims=nc_at["changes"]),
        section("product", process_steps=step_ents, quality_attributes=attrs, non_claims=nc_at["product"]),
        section("equivalency", non_claims=nc_at["equivalency"]),
        section("sdm", equipment=equipment, non_claims=nc_at["sdm"]),
        section("process", parameters=params, control_strategy=cs_at["process"]),
        section("methods", analytical_methods=methods, non_claims=nc_at["methods"]),
        section("control", control_strategy=cs_at["control"], contributions=contributions,
                non_claims=nc_at["control"]),
        section("ppq", non_claims=nc_at["ppq"]),
        section("roles", non_claims=nc_at["roles"]),
        section("schedule", non_claims=nc_at["schedule"]),
    ]

    # ==== studies: the one study the plan names ======================================================
    Q_C1 = "Version 1.0 of this plan was approved on `{python} appr_v1`, before the risk assessment RA-001 (`{python} ra_appr`), the master plan PCMP-001 (`{python} pcmp_appr`) and the first characterization study, the qualification of the production bioreactor scale-down model (`{python} first_study`), which started on `{python} first_start`."
    first = ns["chron"].set_index("id").loc[ns["first_study"]]
    if G.STUDY_TYPE.get(first["kind"]) != "scale_down_qualification":
        raise ValueError(f"{DOC}: {ns['first_study']} is no longer a scale-down qualification")
    studies = [S.StudyDesign(
        study_id=f"study:{ns['first_study']}", study_type=G.STUDY_TYPE[first["kind"]],
        unit_operation=title_of[first["step"]], source_references=[ref("changes", q(Q_C1))],
        metadata=meta())]

    # ==== transfer gaps ==============================================================================
    Q_G2 = "At this revision, the action on the scale-down models compares the engineering batches with the development train, the action on the analytical methods adds nrCE-SDS and leaves out the infectivity titre assays, and the action on parameter classification runs the engineering batches under the master batch record (@sec-changes)."
    Q_G4 = "The first two gaps, on the scale-down models and on the analytical methods, each need laboratory work at a site that has not yet done it."
    Q_G5 = "The gaps on parameter classification, buffer preparation and operator training are closed by sequencing, by a bounded qualification study and by training, and none of them needs a change to the process itself."
    Q_G6 = "The gaps on harvest and UF/DF and on viral clearance are not closed but managed, by the stated limitation and by keeping the claims made at small scale."
    Q_G8 = "It is accepted because the risk assessment RA-001 ranked none of the parameters of either step high and expected none of them to interact with another parameter (PCMP-001 Version 2.0 §4)."
    Q_E30 = "Buffer preparation and method transfer both need laboratory work at the receiving site, a study of buffer hold times and a transfer exercise for each method, and both are listed in @sec-gaps."
    gap_prose = {"GAP-01": [("gaps", Q_G2), ("gaps", Q_G4)],
                 "GAP-02": [("gaps", Q_G2), ("gaps", Q_G4), ("equivalency", Q_E30)],
                 "GAP-03": [("gaps", Q_G6), ("gaps", Q_G7), ("gaps", Q_G8)],
                 "GAP-04": [("gaps", Q_G2), ("gaps", Q_G5)],
                 "GAP-05": [("gaps", Q_G5), ("equivalency", Q_E30)],
                 "GAP-06": [("gaps", Q_G6)], "GAP-07": [("gaps", Q_G5)]}
    if len(gprow) != len(GAPS):
        raise ValueError(f"{DOC}: {len(gprow)} gap rows against {len(GAPS)} gaps")
    gaps = []
    for (gid, area, word), (gkey, row) in zip(GAPS, gprow.items()):
        if word not in gkey:
            raise ValueError(f"{DOC}: gap row {gkey!r} is not {gid} ({word})")
        gap, impact, action, owner = gp_cells[gkey]
        gaps.append(TransferGap(
            gap_id=gid, gap_area=area, description=gap, impact=impact,
            mitigation=f"{_text(action, xr)}. Owner: {owner}.", status="open",
            source_references=[tref("gaps", gp_t, gprow, gkey)] + [ref(s_, q(x)) for s_, x in gap_prose[gid]],
            metadata=meta()))

    # ==== assertions =================================================================================
    for k in steps:
        add("process:amab_ds", "process_has_step", f"step:{k}",
            f"The A-Mab drug substance process has the step {title_of[k]} (Step {num_of[k]}).",
            [tref("product", tr_t, trow, k)])
    for (k, name), row in prow.items():
        add(f"step:{k}", "step_has_parameter", pid[(k, name)],
            f"{title_of[k]} has process parameter {name}.", [tref("process", pbs_t, prow, (k, name))])
    for k, a in links:
        refs = []
        if ATTR_TOKEN[a] in role_of[k]:
            refs.append(tref("product", tr_t, trow, k))
        if (k, a) in link_prose:
            s_, x = link_prose[(k, a)]
            refs.append(ref(s_, q(x)))
        how = (f"Its principal role in the process train: {_lc(role_of[k])}." if ATTR_TOKEN[a] in role_of[k]
               else "Aggregate forms at low pH during the elution from Protein A and the viral inactivation hold.")
        add(f"step:{k}", "step_has_quality_attribute", f"attr:{a}",
            f"{title_of[k]} (Step {num_of[k]}) is linked to {names[a]}. {how}", refs)
    for key in ckeys:
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{key}_ds",
            f"{names[key]} drug substance acceptance criterion: {cq.loc[key, 'Acceptance']}.",
            [tref("product", cq_t, crow, key)])
    Q_A13 = "The receiving site therefore needs nrCE-SDS for fragments and SEC for aggregate."
    Q_K38 = 'The margin is also smaller than the intermediate precision of the infectivity titre assays, `{python} f"{x_prec:g}"` log10 for XMuLV (AMV-3017) and `{python} f"{m_prec:g}"` log10 for MVM (AMV-3018).'
    meas_prose = {"aggregates_hmw": [("methods", Q_A13)], "fragments_lmw": [("methods", Q_A13)],
                  "hcp": [("methods", Q_A5)], "residual_dna": [("control", Q_K26)],
                  "lrv_xmulv": [("control", Q_K38)], "lrv_mvm": [("control", Q_K38)]}
    for key in ckeys:
        m = method_of[key]
        refs = ([tref("methods", me_t, merow, m)] if m in me.index else [tref("process", sop_t, soprow, m)])
        if key == "fragments_lmw":
            refs.append(tref("product", cq_t, crow, key))
        refs += [ref(s_, q(x)) for s_, x in meas_prose.get(key, [])]
        mname = me.loc[m, "Analytical method"] if m in me.index else sop_title[m]
        add(f"attr:{key}", "attribute_measured_by_method", f"method:{m}",
            f"{names[key]} is measured by {m} ({mname}).", refs)
    for g in gaps:
        add("transfer:amab_ds", "transfer_has_gap", f"gap:{g.gap_id}",
            f"The transfer has the {g.gap_area.replace('_', ' ')} gap {g.gap_id}: {g.description}.",
            [g.source_references[0]])

    # ==== statements, section by section =============================================================
    # Purpose and scope
    sq("purpose", "This plan governs the transfer of the `{python} PRODUCT` drug substance manufacturing process from the development site of `{python} COMPANY` in `{python} SENDING_LOCATION` to its commercial drug substance site in `{python} RECEIVING_LOCATION`.",
       "PTP-001 governs the transfer of the `{python} PRODUCT` drug substance manufacturing process from the development site of `{python} COMPANY` in `{python} SENDING_LOCATION` to its commercial drug substance site in `{python} RECEIVING_LOCATION`.")
    sq("purpose", "The transfer covers the manufacturing process, the analytical methods that test the intermediates and the drug substance, and the control strategy that connects them.")
    sq("purpose", "This plan is the parent document of the `{python} PRODUCT` process characterization package.",
       "PTP-001 is the parent document of the `{python} PRODUCT` process characterization package.")
    sq("purpose", "The package has `{python} n_docs` documents, including this plan",
       "The process characterization package has `{python} n_docs` documents, including PTP-001.")
    sq("purpose", Q_RA)
    sq("purpose", "Each Process Characterization Plan (PCP-003 to PCP-010) commits the studies of its step, and each paired Process Characterization Report (PCR-003 to PCR-010) records what they found.")
    sq("purpose", "The master plan PCMP-001 sets the framework that the step plans apply, and the master report PCMR-001 consolidates the reports.")
    sq("purpose", "Together these documents justify the operating ranges and the control strategy that the receiving site will run.",
       "Together the documents of the package justify the operating ranges and the control strategy that the receiving site will run.")
    sq("purpose", "The package also holds two investigation reports of Quality Assurance.")
    sq("purpose", "The investigation `{python} inv_id` is the reason for this revision (@sec-changes), and the investigation `{python} inv2_id` concerns the adequacy of the response-surface models in the step reports.",
       "The investigation `{python} inv_id` is the reason for Version 2.0 of PTP-001, and the investigation `{python} inv2_id` concerns the adequacy of the response-surface models in the step reports.")
    sq("purpose", "This plan sets the conditions the campaign must meet before it may start and the strategy it will follow (@sec-ppq).",
       "PTP-001 sets the conditions the process performance qualification campaign must meet before it may start and the strategy it will follow.")
    sq("purpose", "The transfer follows ICH Q10, which places technology transfer within the pharmaceutical quality system",
       "The transfer follows ICH Q10, which places technology transfer within the pharmaceutical quality system, and the lifecycle approach to process validation.",
       also=[("purpose", "and the lifecycle approach to process validation")])
    sq("purpose", "In that lifecycle, process characterization belongs to Stage 1 (process design).",
       "In the lifecycle approach to process validation, process characterization belongs to Stage 1 (process design).")
    sq("purpose", "Stage 2 (process qualification) covers the qualification of the facility, equipment and utilities and the process performance qualification.")
    sq("purpose", "The enhanced development approach of ICH Q8 and ICH Q11 governs how the design space and the control strategy are defined")
    sq("purpose", "ICH Q9 governs the risk assessment that scopes the studies",
       "ICH Q9 governs the risk assessment that scopes the studies, and ICH Q5A governs the evaluation of viral safety.",
       also=[("purpose", "ICH Q5A governs the evaluation of viral safety")])
    sq("purpose", "The process model, the quality attribute framework and the risk method follow the published A-Mab case study")

    # Changes in this revision
    sq("changes", Q_C1, "Version 1.0 of PTP-001 was approved on `{python} appr_v1`, before the risk assessment RA-001 (`{python} ra_appr`), the master plan PCMP-001 (`{python} pcmp_appr`) and the first characterization study, the qualification of the production bioreactor scale-down model (`{python} first_study`), which started on `{python} first_start`.")
    sq("changes", Q_C2, "Version 2.0 replaces Version 1.0 under corrective action CA3 of the QA investigation `{python} inv_id`, which reissues PTP-001, the risk assessment RA-001, the step reports PCR-003 to PCR-010 and the master report PCMR-001 at Version 2.0.")
    sq("changes", "Quality Assurance opened the investigation on `{python} inv_opened`, after a review of the master report PCMR-001 Version 1.0 for readiness for the Biologics License Application (BLA), and closed it on `{python} inv_closed` with the classification `{python} inv_class`.",
       "Quality Assurance opened `{python} inv_id` on `{python} inv_opened`, after a review of the master report PCMR-001 Version 1.0 for readiness for the Biologics License Application (BLA), and closed it on `{python} inv_closed` with the classification `{python} inv_class`.")
    sq("changes", "The investigation found that the criteria used to judge each step in the proven acceptable range (PAR) analysis had been set after the data were seen and were in no approved protocol (`{python} inv_id` finding 1).")
    sq("changes", "The title block of Version 1.0 carried `{python} pkg_date`, the date on which the Version 1.0 package was compiled, in place of the date on which this plan was approved (`{python} inv_id` finding 5).",
       "The title block of Version 1.0 carried `{python} pkg_date`, the date on which the Version 1.0 package was compiled, in place of the date on which PTP-001 was approved (`{python} inv_id` finding 5).")
    sq("changes", "The revision history now gives the approval date.")
    sq("changes", "@sec-schedule records the approval date of each step plan and the execution window of the studies that Version 1.0 reported (@tbl-chronology).",
       "PTP-001 now records the approval date of each step plan and the execution window of the studies that Version 1.0 reported.")
    sq("changes", "Where this plan states what an intermediate is judged against, it now refers to the intermediate acceptance criteria of the master plan PCMP-001 Version 2.0 §7.3.",
       "Where PTP-001 states what an intermediate is judged against, it now refers to the intermediate acceptance criteria of the master plan PCMP-001 Version 2.0 §7.3.")
    sq("changes", "This applies to the comparison of the sites (@sec-sdm), the control strategy (@sec-control) and the qualification campaign (@sec-ppq).",
       "The reference to the intermediate acceptance criteria applies to the comparison of the sites, the control strategy and the qualification campaign.")
    sq("changes", "These criteria are derived a priori from the drug substance criteria and the platform worst case of each downstream step.",
       "The intermediate acceptance criteria are derived a priori from the drug substance criteria and the platform worst case of each downstream step.")
    sq("changes", "Version 1.0 referred to the limit that each characterization report would establish for its own step.")
    sq("changes", "The investigation found that the step limits had been set after the data were seen and were in no approved protocol (finding 1), that the aggregate and host cell protein limits carried the drug substance limit back through the nominal clearance of this campaign and divided it by a margin that differed by step (finding 2), and that the bioreactor limits for the glycans and acidic variants were computed from the capability data they were then used to judge (finding 3).",
       "`{python} inv_id` found that the step limits had been set after the data were seen and were in no approved protocol (finding 1), that the aggregate and host cell protein limits carried the drug substance limit back through the nominal clearance of the campaign and divided it by a margin that differed by step (finding 2), and that the bioreactor limits for the glycans and acidic variants were computed from the capability data they were then used to judge (finding 3).")
    sq("changes", "The viral clearance claims of `{python} viral_steps_txt` now refer to PCMP-001 Version 2.0 §7.4.")
    sq("changes", "Where this plan describes the qualification of the scale-down models (@sec-equivalency, @sec-sdm and @tbl-gaps), it now refers to the offset rule of PCMP-001 Version 2.0 §7.1.",
       "Where PTP-001 describes the qualification of the scale-down models, it now refers to the offset rule of PCMP-001 Version 2.0 §7.1.")
    sq("changes", "Under that rule a model is qualified for each output by its offset, the scale-down mean minus the manufacturing-scale mean, and not by a test of equivalence.",
       "Under the offset rule a model is qualified for each output by its offset, the scale-down mean minus the manufacturing-scale mean, and not by a test of equivalence.")
    sq("changes", "For the outputs that the qualification compares at both scales, every judgement against a criterion is stated at manufacturing scale.")
    sq("changes", Q_C19)
    sq("changes", "Version 1.0 said in @tbl-equivalency that the models are qualified against the commercial train before any study is run, which the order of @tbl-deliverables rules out.",
       "Version 1.0 said in its site equivalency table that the models are qualified against the commercial train before any study is run, which the dependency order of the deliverables rules out.")
    sq("changes", "Its gap action recorded that comparison in the step plans, which were approved before their studies.",
       "The gap action of Version 1.0 recorded that comparison in the step plans, which were approved before their studies.")
    sq("changes", Q_C22)
    sq("changes", "The quality attributes in @tbl-cqa now include fragments (low molecular weight species).",
       "The quality attributes of the drug substance now include fragments (low molecular weight species).")
    sq("changes", Q_C24)
    sq("changes", "The A-Mab case study lists fragmentation among the typical quality attributes of an antibody but gives it no limit (PCMP-001 §3).")
    sq("changes", "That register assigns fragments to harvest, so the description of harvest in @tbl-train and the basis on which the harvest gap is accepted (@sec-gaps) are restated.",
       "The CQA register of PCMP-001 Version 2.0 assigns fragments to harvest, so the description of harvest in the process train table and the basis on which the harvest gap is accepted are restated.")
    sq("changes", Q_C27)
    sq("changes", "This answers `{python} inv_id` finding 6, that size exclusion chromatography (SEC) reads fragments high in samples that still carry host cell protein.",
       "The addition of nrCE-SDS answers `{python} inv_id` finding 6, that size exclusion chromatography (SEC) reads fragments high in samples that still carry host cell protein.")
    sq("changes", Q_C29, "The procedures and method validations of PTP-001 now also include the product titre method by Protein A affinity HPLC (SOP-3016, AMV-3021), because the titre sets the protein load of a capture run, and the method for aggregate by SEC-HPLC (AMV-3221).")
    sq("changes", Q_C31, "Beside the methods of the Version 1.0 table, the table of methods to be transferred now includes the charge variant method by icIEF (AMV-3013), the residual DNA method by qPCR (AMV-3014) and the product titre method (AMV-3021).")
    sq("changes", "@sec-process now carries the parameter table as it stands at this revision (@tbl-parameters-by-step), with the set-point, NOR, characterized range and class of every parameter.",
       "PTP-001 now carries the parameter table as it stands at Version 2.0, with the set-point, NOR, characterized range and class of every parameter.")
    sq("changes", "It includes the set-points and NORs that `{python} chg_reports` changed at Version 2.0, and its footnotes give the value the studies were planned against.",
       "The parameter table includes the set-points and NORs that `{python} chg_reports` changed at Version 2.0, and its footnotes give the value the studies were planned against.")
    sq("changes", "@tbl-package lists the two investigation reports, `{python} inv_id` and `{python} inv2_id`, beside the plans and reports of the package.",
       "The package table lists the two investigation reports, `{python} inv_id` and `{python} inv2_id`, beside the plans and reports of the package.")
    sq("changes", "Statements of Version 1.0 about the product, the sites and the scale-down models that were wrong, or that the record now contradicts, are corrected.")
    sq("changes", "Version 1.0 linked both glycan attributes to ADCC, but galactose content raises the complement-dependent cytotoxicity of A-Mab, not its ADCC, and aggregate also forms at low pH (@sec-product).")
    sq("changes", "Protein A and cation exchange bind the antibody, and only anion exchange binds the impurities while the antibody flows through (@sec-product).")
    sq("changes", "The CQA register assigns each viral clearance requirement to one step, where Version 1.0 said that the requirements belong to no single step (@sec-product).")
    sq("changes", "The step roles in @tbl-train are those of the register at this revision.",
       "The step roles in the process train table are those of the CQA register at Version 2.0.")
    sq("changes", "The statement that a common quality system is a condition ICH Q10 places on the transfer is removed, and the handovers that Quality Assurance approves are the deliverables of @tbl-deliverables (@sec-sites).",
       "The statement that a common quality system is a condition ICH Q10 places on the transfer is removed, and the handovers that Quality Assurance approves are the deliverables of the transfer.")
    sq("changes", "Bed height, linear velocity and the load per membrane area are held constant across scale, and the virus filter and the UF/DF step run at a set pressure (@sec-equivalency and @sec-sdm).")
    sq("changes", "A narrower distribution of a parameter does not invalidate its range because every NOR lies within its characterized range, as @tbl-parameters-by-step shows (@sec-equivalency).",
       "A narrower distribution of a parameter does not invalidate its range because every NOR lies within its characterized range, as the parameter table shows.")
    sq("changes", "The other elements of @tbl-equivalency differ between the sites in ways that can affect the process, not only in documentation, and method transfer needs laboratory work as buffer preparation does (@sec-equivalency).",
       "The other elements of the site equivalency assessment differ between the sites in ways that can affect the process, not only in documentation, and method transfer needs laboratory work as buffer preparation does.")
    sq("changes", "Version 1.0 judged comparability against the acceptance criteria alone.")
    sq("changes", "As ICH Q5E expects, the engineering batches are now also compared with the development-train batches (@sec-sdm).")
    sq("changes", "Statements of Version 1.0 about the transfer elements, the qualification campaign and the gaps are corrected in the same way.")
    sq("changes", "A method transfer succeeds on accuracy within the limits the transfer protocol sets, not within a qualified range, and the protocol also sets the allowed difference between the sites (@sec-methods).")
    sq("changes", "XMuLV clearance rests on `{python} n_x` claimed steps and MVM clearance on `{python} n_m`, where Version 1.0 said that viral safety rests on three independent steps (@sec-control).")
    sq("changes", "Stage 2 of the lifecycle also covers the qualification of the facility, equipment and utilities (@sec-purpose and @sec-ppq).")
    sq("changes", "The qualification protocol, not the step plans, sets the sampling plan of the campaign, and post-clarification turbidity is measured, not set (@sec-ppq).")
    sq("changes", "In @tbl-gaps the first two gaps no longer set the schedule, which @sec-schedule gives, and the gaps on harvest and UF/DF and on viral clearance are managed, not closed.",
       "In the gap table the first two gaps no longer set the schedule, which the deliverables and schedule section gives, and the gaps on harvest and UF/DF and on viral clearance are managed, not closed.")
    sq("changes", "The engineering batches are run under the master batch record, which follows PCMR-001, as the deliverables of Version 1.0 have it (@tbl-deliverables).")
    sq("changes", "Version 1.0 also said that the engineering batches could run against the current process description (@sec-control and @tbl-gaps) and that operator training did not wait for PCMR-001 (@sec-schedule).")
    sq("changes", "These statements now follow the order of @tbl-deliverables.",
       "The statements on the engineering batches and on operator training now follow the dependency order of the deliverables.")
    sq("changes", "The scope of the transfer, the site analysis, the transfer elements, the gap analysis and the strategy for process performance qualification are otherwise as Version 1.0 stated them.")

    # Product and process description
    sq("product", "`{python} PRODUCT` is a humanized IgG1 monoclonal antibody.")
    sq("product", "Its primary mechanism of action is antibody-dependent cellular cytotoxicity (ADCC).",
       "The primary mechanism of action of `{python} PRODUCT` is antibody-dependent cellular cytotoxicity (ADCC).")
    sq("product", "An antibody without core fucose on its N-linked glycan binds the Fcγ receptor IIIa (FcγRIIIa) of natural killer cells more strongly, so the ADCC activity of A-Mab rises with afucosylation")
    sq("product", "Galactose content does not change the ADCC of A-Mab, but its complement-dependent cytotoxicity (CDC) rises with galactose content")
    sq("product", "Afucosylation and galactosylation are therefore quality attributes of the drug substance.")
    sq("product", "Protein A binds the Fc region at the interface of the CH2 and CH3 domains.")
    sq("product", "Control of the glycan attributes therefore sits in cell culture.")
    sq("product", "For this reason the transfer of the cell culture step carries more risk to product quality than the transfer of any single purification step.")
    sq("product", 'The drug substance is made at a production bioreactor working volume of `{python} f"{scale_l:,}"` L.')
    sq("product", "It leaves the final formulation step at a target concentration of `{python} ds_conc` g/L.",
       "The drug substance leaves the final formulation step at a target concentration of `{python} ds_conc` g/L.")
    sq("product", "The train has `{python} n_steps` unit operations, numbered Step `{python} step_first` to Step `{python} step_last` (@tbl-train).")
    sq("product", "The purification sequence is the platform sequence of the earlier humanized IgG1 products of `{python} COMPANY`, X-Mab, Y-Mab and Z-Mab.")
    sq("product", "Capture on Protein A is followed by a low-pH hold, cation exchange, anion exchange, small virus retentive filtration, and ultrafiltration with diafiltration (UF/DF).")
    sq("product", "The low-pH hold, the anion exchange step and the virus filter each carry a viral clearance claim.")
    sq("product", "The three claims are modular in the sense of ICH Q5A")
    sq("product", "@tbl-cqa lists the `{python} n_cqa` quality attributes that the transfer must preserve.",
       "The transfer must preserve `{python} n_cqa` quality attributes of the drug substance.")
    sq("product", "Criticality is a continuum, not a binary split into critical and non-critical, as in the case study",
       "Criticality is a continuum, not a binary split into critical and non-critical, as in the A-Mab case study and the risk principles of ICH Q9.",
       also=[("product", "and the risk principles of ICH Q9")])
    sq("product", "The attributes ranked high and very high drive the scope of the studies.")
    sq("product", "Afucosylation, galactosylation and high mannose depend on how far the cell processes the glycan in the Golgi.")
    sq("product", "That processing changes with the nutrient supply and with the dissolved gas concentrations in the bioreactor.",
       "The processing of the glycan in the Golgi changes with the nutrient supply and with the dissolved gas concentrations in the bioreactor.")
    sq("product", "Acidic charge variants accumulate through the deamidation of asparagine residues.")
    sq("product", "The rate of deamidation rises with pH and temperature, and the extent rises with the time the product spends at those conditions.")
    sq("product", Q_AGG_LOWPH)
    sq("product", Q_CEX_AGG, "Cation exchange reduces aggregate, because the resin binds the high molecular weight species more strongly than the monomer, and these species stay on the column when the pool is cut.")
    sq("product", Q_FRAG)
    sq("product", "Fragments are judged at the downstream steps.")
    sq("product", "Host cell protein, residual DNA and leached Protein A are removed by the chromatography steps.")
    sq("product", "Protein A and cation exchange bind the antibody and elute it away from most of these impurities.",
       "Protein A and cation exchange bind the antibody and elute it away from most of host cell protein, residual DNA and leached Protein A.")
    sq("product", "Anion exchange works the other way, binding the impurities while the antibody flows through.")
    sq("product", "The two viral clearance requirements are cumulative.")
    sq("product", Q_VIR_REG)

    # Sending and receiving sites
    sq("sites", Q_S1)
    sq("sites", Q_S2)
    sq("sites", "Both sites belong to the same sponsor and work under one pharmaceutical quality system and one change control procedure.")
    sq("sites", "A change to a set-point, a range or an analytical method during the transfer is therefore assessed once and applied at both sites.")
    sq("sites", "The development site keeps the qualified scale-down models, the execution and the statistical analysis of the characterization studies, and the authorship of the characterization plans and reports.")
    sq("sites", "It also keeps the process description and the justification of the operating ranges until those are approved.",
       "The development site also keeps the process description and the justification of the operating ranges until those are approved.")
    sq("sites", "The receiving site takes ownership of commercial manufacture.")
    sq("sites", "That ownership covers the master batch record, the operation of the equipment train at commercial scale, the engineering and qualification batches, and the routine testing that supports batch release.",
       "The ownership of commercial manufacture by the receiving site covers the master batch record, the operation of the equipment train at commercial scale, the engineering and qualification batches, and the routine testing that supports batch release.")
    sq("sites", "The division between the sites is one of work, not of accountability.")
    sq("sites", "Both sites review and approve the process description, and Quality Assurance at both sites approves each handover, that is each deliverable in @tbl-deliverables.",
       "Both sites review and approve the process description, and Quality Assurance at both sites approves each handover, that is each deliverable of the transfer.")
    sq("sites", "Where a characterization study supports a range that the receiving site cannot hold, the two sites resolve it together before the range is written into a batch record.")

    # Site equivalency analysis
    sq("equivalency", "Equivalency was assessed for each element that can carry a process difference between the two sites (@tbl-equivalency).")
    for el, row in eqrow.items():
        _, send, recv, how = eq_cells[el]
        st("equivalency", f"{el}: sending site, {_lc(send)}; receiving site, {_lc(recv)}. How the difference "
           f"is managed: {_lc(_text(how, xr))}", [tref("equivalency", eq_t, eqrow, el)])
    sq("equivalency", "The largest difference between the sites is scale.")
    sq("equivalency", 'The receiving site runs the production bioreactor at `{python} f"{scale_l:,}"` L, while the characterization studies run at the scale-down volumes qualified under SOP-1001 (Qualification of Scale-Down Models).')
    sq("equivalency", "In cell culture, scale acts through mixing and through gas transfer.")
    sq("equivalency", "At constant power per unit volume, mixing time rises with vessel volume.")
    sq("equivalency", "A bolus of feed therefore takes longer to disperse, and cells near the addition point spend longer at a high local concentration.")
    sq("equivalency", "Carbon dioxide is stripped less efficiently as the liquid column deepens, because a sparge bubble that rises through more liquid comes closer to equilibrium with the culture before it leaves.")
    sq("equivalency", "Oxygen crosses the same interface in the other direction, from the bubble into the culture.")
    sq("equivalency", "Its removal is therefore limited by the volume of gas that passes through the culture, while the oxygen supply is limited by the volumetric mass transfer coefficient (kLa) of the vessel.",
       "Carbon dioxide is far more soluble in the culture than oxygen, so its removal is limited by the volume of gas that passes through the culture, while the oxygen supply is limited by the volumetric mass transfer coefficient (kLa) of the vessel.",
       also=[("equivalency", "Carbon dioxide is far more soluble in the culture than oxygen.")])
    sq("equivalency", "For this reason oxygen supply and carbon dioxide removal are matched separately when a bioreactor model is qualified.")
    sq("equivalency", "In the purification steps, scale acts through column packing and through pressure.")
    sq("equivalency", "A chromatography column is scaled by holding the bed height and the linear velocity constant.")
    sq("equivalency", "This keeps the residence time of the mobile phase, but not the wall support that stabilizes a narrow bed.",
       "Holding the bed height and the linear velocity constant keeps the residence time of the mobile phase, but not the wall support that stabilizes a narrow bed.")
    sq("equivalency", "A wide commercial column can therefore lose plate count at a pressure drop that the model tolerates.")
    sq("equivalency", "The virus filter runs at a set filtration pressure, and the UF/DF step at a set transmembrane pressure.",
       "A filter is scaled by membrane area; the virus filter runs at a set filtration pressure, and the UF/DF step at a set transmembrane pressure.",
       also=[("equivalency", "A filter is scaled by membrane area.")])
    sq("equivalency", "In UF/DF the protein concentrates at the membrane surface (concentration polarization), and in the virus filter aggregates plug the pores.")
    sq("equivalency", "At a set pressure, a feed that carries more protein or more aggregate therefore gives a lower flux and, in the virus filter, a lower capacity.")
    sq("equivalency", "Automated control at the receiving site holds a parameter closer to its set-point than manual control does, and so narrows the distribution that the commercial process will deliver.",
       "The second difference between the sites is process control: automated control at the receiving site holds a parameter closer to its set-point than manual control does, and so narrows the distribution that the commercial process will deliver.",
       also=[("equivalency", "The second difference is process control.")])
    sq("equivalency", "A narrower distribution does not invalidate a range, because every NOR lies within the characterized range of its parameter (@tbl-parameters-by-step).")
    sq("equivalency", "Where the receiving site cannot hold a parameter inside the NOR that the characterization assumes, either the range must be widened by further study or the equipment must be changed.",
       also=[("equivalency", "The reverse case matters more.")])
    sq("equivalency", "The remaining elements in @tbl-equivalency differ between the sites in ways that can affect the process, and each is managed as the table states.",
       "The remaining elements of the site equivalency assessment differ between the sites in ways that can affect the process, and each is managed as the assessment states.")
    sq("equivalency", "Central preparation adds a hold before use, during which a buffer can take up carbon dioxide, which lowers its pH, and its bioburden can grow.")
    sq("equivalency", "Commercial raw material lots are a known source of variation in culture performance and glycosylation.")
    sq("equivalency", "The transferred methods are run by other analysts on other instruments.")
    sq("equivalency", Q_E30, "Buffer preparation and method transfer both need laboratory work at the receiving site, a study of buffer hold times and a transfer exercise for each method, and both are listed in the gap analysis.")

    # Scale-down model and comparability strategy
    sq("sdm", "They run on scale-down models, and every conclusion drawn from them reaches the commercial process through the qualification of those models.",
       "The characterization studies run on scale-down models, not at commercial scale, and every conclusion drawn from them reaches the commercial process through the qualification of those models.",
       also=[("sdm", "The characterization studies do not run at commercial scale.")])
    st("sdm", t("Scale-down model qualification is performed under SOP-1001 (Qualification of Scale-Down Models)."),
       [ref("sdm", q("Qualification is performed under SOP-1001 (Qualification of Scale-Down Models).")),
        tref("process", sop_t, soprow, "SOP-1001")])
    sq("sdm", "The lifecycle guidance expects a manufacturer to understand how far a laboratory model represents the commercial process")
    sq("sdm", "Parameters that do not depend on scale, such as pH, temperature and dissolved oxygen, are run at the values proposed for commercial manufacture.",
       also=[("sdm", "A model is set up in two parts.")])
    sq("sdm", "Parameters that depend on scale are set so that the model reproduces the performance of the commercial train.")
    sq("sdm", "In the production bioreactor these are agitation and gas flow, which are set to match the oxygen transfer and the carbon dioxide stripping of the commercial vessel.",
       "In the production bioreactor the scale-dependent parameters are agitation and gas flow, which are set to match the oxygen transfer and the carbon dioxide stripping of the commercial vessel.")
    sq("sdm", "For the chromatography steps the model keeps the bed height and the linear velocity of the manufacturing column, and so its residence time.")
    sq("sdm", "Load, wash and elution volumes are normalized to column volumes, and column efficiency is checked by plate count and peak asymmetry.")
    sq("sdm", "The virus filter model uses the same filter type at the same filtration pressure and load per membrane area.")
    sq("sdm", "The UF/DF model scales membrane loading and cross flow by membrane area at the same transmembrane pressure.")
    sq("sdm", "For a chromatography step those outputs are step yield, pool volume and the impurity levels in the pool.",
       "A scale-down model is compared with manufacturing scale on the outputs the step controls; for a chromatography step those outputs are step yield, pool volume and the impurity levels in the pool.",
       also=[("sdm", "The model is then compared with manufacturing scale on the outputs the step controls.")])
    sq("sdm", "For the production bioreactor they are viable cell concentration, titre and the product quality attributes the step forms.",
       "For the production bioreactor the outputs compared are viable cell concentration, titre and the product quality attributes the step forms.")
    sq("sdm", "Each model is qualified for each output separately, by the offset rule of the master plan PCMP-001 Version 2.0 §7.1.")
    sq("sdm", "The offset of an output is the mean of the scale-down runs at set-point minus the mean of the manufacturing-scale batches, with its two-sided `{python} offset_ci` % confidence interval.")
    sq("sdm", Q_M18, "The manufacturing-scale batches come from the development train, the manufacturing-scale train at the sending site whose batches are the manufacturing-scale reference of each step's qualification (PCMP-001 §7.1).")
    sq("sdm", "A model may differ in mean from manufacturing scale, provided the offset is known precisely enough.")
    sq("sdm", "For an output compared at both scales, every judgement of a scale-down result against a criterion therefore subtracts the offset first, so ranges and conclusions are stated at manufacturing scale.")
    sq("sdm", "A model is qualified for an output when the conclusion over the NOR is the same with the offset at either end of its interval.")
    sq("sdm", "The qualification runs are made, and the offset of each output is estimated, before the first characterization run of the step.")
    sq("sdm", "For a step with a response-surface design, the decision whether the model is qualified for an output is made at analysis, because the conclusion over the NOR comes from that model.")
    sq("sdm", "Their representativeness rests on the mechanism of each step for fragments, such as clipping by proteases released from lysed cells during the harvest hold, and on the virus spiking studies for viral clearance (PCMP-001 §7.1).",
       "The representativeness of the scale-down result rests on the mechanism of each step for fragments, such as clipping by proteases released from lysed cells during the harvest hold, and on the virus spiking studies for viral clearance (PCMP-001 §7.1).")
    for k in steps:
        _, uo_name, n_p, n_mv, n_uv, docs = sc_cells[str(num_of[k])]
        st("sdm", f"{uo_name} (Step {num_of[k]}): {n_p} parameters in scope, {n_mv} studied in multivariate "
           f"designs and {n_uv} one factor at a time; the characterization is covered by {docs}.",
           [tref("sdm", sc_t, srow, k)])
    sq("sdm", "Across the train, `{python} n_par` parameters are in scope.")
    sq("sdm", "Of these, `{python} n_mv` are studied in multivariate designs and `{python} n_uv` one factor at a time.",
       "Of the `{python} n_par` parameters in scope, `{python} n_mv` are studied in multivariate designs and `{python} n_uv` one factor at a time.")
    sq("sdm", "Comparability between the two sites is demonstrated on material, not on documents.")
    sq("sdm", Q_M33)
    sq("sdm", "Each batch will be sampled at every step and tested by the transferred methods.",
       "Each engineering batch will be sampled at every step and tested by the transferred methods.")
    sq("sdm", "Under ICH Q5E a change of manufacturing site is judged by comparing the quality attributes before and after the change, and meeting the acceptance criteria alone is generally not enough")
    sq("sdm", "The drug substance from the engineering batches will therefore be compared with the drug substance of the development-train batches on the attributes of @tbl-cqa that a batch test measures.",
       "The drug substance from the engineering batches will be compared with the drug substance of the development-train batches on the quality attributes that a batch test measures.")
    sq("sdm", "Each batch must also meet the acceptance criteria in @tbl-cqa, except residual DNA and viral clearance, whose criteria are met through clearance (@sec-control).",
       "Each engineering batch must also meet the drug substance acceptance criteria, except residual DNA and viral clearance, whose criteria are met through clearance.")
    sq("sdm", "Each intermediate will be compared with its intermediate acceptance criterion from PCMP-001 §7.3, where one is defined.")
    sq("sdm", "Prior knowledge from the earlier humanized IgG1 products supports the expectation that the platform purification steps behave the same way at both scales")
    sq("sdm", "The comparison of the engineering batches with the development-train batches tests that expectation.",
       "The comparison of the engineering batches with the development-train batches tests the expectation that the platform purification steps behave the same way at both scales.")

    # Transfer of the process, methods and control strategy
    sq("transfer", "The transfer is delivered in three parts.",
       "The transfer is delivered in three parts: the manufacturing process, the analytical methods and the control strategy.",
       also=[("transfer", "@sec-process covers the manufacturing process, @sec-methods the analytical methods and @sec-control the control strategy.")])

    # The manufacturing process
    sq("process", "The process description is the source document of the transfer.")
    sq("process", "It states the sequence of unit operations, the materials, the set-point of every parameter and the range within which each parameter may move.",
       "The process description states the sequence of unit operations, the materials, the set-point of every parameter and the range within which each parameter may move.")
    sq("process", "The characterization studies confirm the set-points and ranges, and in some cases narrow or move them.")
    sq("process", "The confirmed values are issued as a revision of the process description before the master batch record is drafted.")
    sq("process", "@tbl-parameters-by-step gives every process parameter with its set-point, NOR, characterized range and class as they stand at this revision.",
       "The parameter table of PTP-001 gives every process parameter with its set-point, NOR, characterized range and class as they stand at Version 2.0.")
    st("process", "The class of each parameter is the one assigned in the report of the step under the parameter "
       "classification procedure SOP-4001.",
       [ref("process", q("The class is the one assigned in the report of the step under the parameter classification procedure SOP-4001.")),
        tref("process", sop_t, soprow, "SOP-4001")])
    sq("process", "The set-point and the NOR are those in force.",
       "The set-point and the NOR of each parameter in the table are those in force.")
    sq("process", "Some of them were changed at Version 2.0 by the report of their step, after the studies.",
       "Some set-points and NORs were changed at Version 2.0 by the report of their step, after the studies.")
    sq("process", "`{python} chg_text`")
    sq("process", "The report of the step gives the reason for each change.")
    # the set-points and NORs changed at Version 2.0: each on the footnote the table gives it
    notes = {n.split(" ", 1)[0]: n for n in pbs_t.notes_text().split(CELL_SEP)}
    n_nor = n_sp = 0
    for (k, name), row in prow.items():
        marks = re.findall(r"\s(c\d+\))(?=\s|$)", row)
        if not marks:
            continue
        uo = uo_of[k]
        p = uo.param(next(x.key for x in uo.parameters if x.name == name))
        rep = report_of(k)

        def wu2(v, p=p):
            return f"pH {v}" if p.unit == "pH" else f"{v} {p.unit}"
        pname = f"{name[0].lower() + name[1:]} at {T.step_mid(k)}"
        for mk in marks:
            note = notes[mk]
            if note.endswith(f"the NOR as characterized ({rep})."):
                n_nor += 1
                st("process", f"At Version 2.0, {rep} {T.nor_change(p)} the NOR of {pname} from "
                   f"{wu2(f'{p.nor_characterized[0]:g}–{p.nor_characterized[1]:g}')} to "
                   f"{wu2(f'{p.nor[0]:g}–{p.nor[1]:g}')}; the parameter table gives the NOR in force.",
                   [ref("process", note, pbs_t), tref("process", pbs_t, prow, (k, name))])
            elif note.endswith(f"the set-point in the characterization plan ({rep})."):
                n_sp += 1
                st("process", f"At Version 2.0, {rep} moved the set-point of {pname} from "
                   f"{wu2(f'{p.setpoint_characterized:g}')} to {wu2(f'{p.setpoint:g}')}; the parameter table "
                   f"gives the set-point in force.",
                   [ref("process", note, pbs_t), tref("process", pbs_t, prow, (k, name))])
            else:
                raise ValueError(f"{pbs_t.label}: note {mk} of {name} is neither a NOR nor a set-point change")
    if (n_nor, n_sp) != (sum(1 for c in ns["chg"] if c[2]), sum(1 for c in ns["chg"] if c[3])):
        raise ValueError(f"{DOC}: the footnoted changes do not match the changes the plan states")
    sq("process", "The receiving site will draft the master batch record from the approved process description.")
    sq("process", Q_R12)
    sq("process", "Where a parameter is monitored but not held to a limit, the batch record should record the measured value without an acceptance criterion.",
       "Where a parameter is monitored but not held to a limit, the batch record should record the measured value without an acceptance criterion, so that a change in the value is visible without generating a deviation.",
       also=[("process", "A change in the value is then visible without generating a deviation.")])
    sq("process", "@tbl-sops lists the procedures and method validations referenced in this plan, which are the documents that support the transfer.",
       "The procedures and method validations referenced in PTP-001 are the documents that support the transfer.")
    sq("process", "The procedures for the operation of each unit operation will be reissued in the document system of the receiving site before the engineering batches are run.")
    st("process", "Three procedures stay with development, because the work they govern stays at the sending site: "
       "SOP-1001 governs scale-down model qualification, SOP-1002 the design and statistical analysis of the "
       "characterization studies, and SOP-4001 parameter classification.",
       [ref("process", q("Three procedures stay with development, because the work they govern stays at the sending site.")),
        ref("process", q("SOP-1001 governs scale-down model qualification, SOP-1002 the design and statistical analysis of the characterization studies, and SOP-4001 parameter classification.")),
        tref("process", sop_t, soprow, "SOP-1002")])
    sq("process", "Handover of the manufacturing process is complete when the process description, the master batch record, the bill of materials and the operator training records have been approved at the receiving site.")
    sq("process", "MSAT at the receiving site owns that approval, and Quality Assurance at both sites countersigns it.",
       "MSAT at the receiving site owns the approval of the handover of the manufacturing process, and Quality Assurance at both sites countersigns it.")

    # The analytical methods
    sq("methods", "The methods in scope are the release and characterization methods for the drug substance and the in-process methods that support the control of the intermediates.")
    sq("methods", "@tbl-methods lists the `{python} n_meth_t` methods to be transferred and the performance each demonstrated at qualification, from the record of qualified method performance (the method record).",
       "PTP-001 lists the `{python} n_meth_t` methods to be transferred and the performance each demonstrated at qualification, from the record of qualified method performance.")
    for m, row in merow.items():
        r = me.loc[m]
        st("methods", f"{m} ({r['Analytical method']}) is to be transferred; at qualification it demonstrated an "
           f"intermediate precision of {r['Intermediate precision']}, a limit of quantitation of "
           f"{r['Limit of quantitation']} and an accuracy of {r['Accuracy (%)']} %.",
           [tref("methods", me_t, merow, m)])
    sq("methods", Q_A5)
    sq("methods", 'It is also `{python} hcp_rank_txt` in @tbl-methods, at `{python} f"{hcp_prec:g}"` %.',
       'The host cell protein ELISA (AMV-3012) is also `{python} hcp_rank_txt` of the methods to be transferred, at `{python} f"{hcp_prec:g}"` %.')
    sq("methods", "Its transfer should therefore be completed and reviewed before the engineering batches are run.",
       "The transfer of the host cell protein ELISA should therefore be completed and reviewed before the engineering batches are run.")
    sq("methods", Q_A9, "AMV-3221, the SEC method for aggregate, is the one transferred, and its qualified performance is in the table of methods to be transferred.")
    sq("methods", Q_A10)
    sq("methods", "It is transferred because the titre sets the protein load of a capture run.",
       "The product titre method is transferred because the titre sets the protein load of a capture run.")
    sq("methods", Q_A12)
    sq("methods", Q_A13)
    sq("methods", Q_A14, "The nrCE-SDS method is transferred and requalified like the methods in the table of methods to be transferred.")
    sq("methods", Q_A16, "The validation of nrCE-SDS is AMV-3020, from which the transfer protocol takes the values to be reproduced.")
    sq("methods", "Each method will be transferred under a written protocol and requalified at the receiving site before it is used to test comparability material.")
    sq("methods", "A transfer is successful when the receiving site reproduces the qualified intermediate precision of the method and returns accuracy within the limits the transfer protocol sets, on a common set of samples.")
    sq("methods", "The protocol also sets the allowed difference between the results of the two sites.",
       "The transfer protocol also sets the allowed difference between the results of the two sites.")
    sq("methods", "If the receiving site cannot meet the qualified precision, the cause should be investigated and corrected before the exercise is repeated.")
    sq("methods", "A method may not be used for in-process or release testing until its transfer has passed.")
    sq("methods", "Analytical Development at the sending site owns the transfer protocols and the comparison of the two data sets.")
    sq("methods", "Quality Control at the receiving site executes the transfers.",
       "Quality Control at the receiving site executes the method transfers, and Quality Assurance approves the outcome.",
       also=[("methods", "Quality Assurance approves the outcome.")])
    sq("methods", "The person who executes a method transfer may not approve it.")

    # The control strategy
    sq("control", "The control strategy is the set of controls that together assure the quality of the drug substance.")
    sq("control", "In this transfer it has three layers.",
       "In the transfer the control strategy has three layers: parameter classification, in-process limits and release testing.",
       also=[("control", Q_K3), ("control", Q_K4), ("control", Q_K5)])
    sq("control", Q_K7)
    sq("control", "Each report classifies the parameters of its own step, and the master report PCMR-001 consolidates the classification for the whole train.")
    sq("control", "A parameter whose variability affects a quality attribute is a critical process parameter (CPP).")
    sq("control", "It is a well-controlled critical process parameter (WC-CPP) where the risk of leaving the design space is low.",
       "A parameter whose variability affects a quality attribute is a well-controlled critical process parameter (WC-CPP) where the risk of leaving the design space is low.")
    sq("control", "A parameter that affects process consistency without affecting quality is a key process parameter (KPP).")
    sq("control", "The remaining parameters are general process parameters (GPPs), which the batch record controls without a claim of criticality")
    sq("control", "At this revision the train has `{python} cls_txt` (@tbl-parameters-by-step).",
       "At Version 2.0 the train has `{python} cls_txt`.")
    sq("control", Q_K14)
    sq("control", "The criterion is the drug substance criterion carried backward through the train, using the worst case that each downstream step showed on the platform products X-Mab, Y-Mab and Z-Mab.",
       "The intermediate acceptance criterion is the drug substance criterion carried backward through the train, using the worst case that each downstream step showed on the platform products X-Mab, Y-Mab and Z-Mab.")
    sq("control", "Each step report checks the platform worst cases of its own step, and PCMP-001 §7.5 states when that check tightens or widens a criterion upstream.")
    sq("control", "The master plan gives `{python} n_iac` such criteria across `{python} n_iac_steps` steps.",
       "The master plan PCMP-001 gives `{python} n_iac` intermediate acceptance criteria across `{python} n_iac_steps` steps.")
    sq("control", Q_K21, 'The residual DNA criterion, no more than `{python} f"{dna_crit:g}"` ng per dose, is the acceptable range that the A-Mab case study claims, and the case study notes that DNA is consistently cleared from the process.')
    sq("control", "The dose is the weekly A-Mab dose of `{python} dose_mgkg` mg/kg",
       'The residual DNA criterion is expressed per dose: the weekly A-Mab dose of `{python} dose_mgkg` mg/kg, or `{python} f"{DOSE_MG:g}"` mg for a reference adult of `{python} dose_bw` kg, a body weight that the package assumes.',
       also=[("control", "The criterion is expressed per dose."),
             ("control", 'or `{python} f"{DOSE_MG:g}"` mg for a reference adult of `{python} dose_bw` kg, a body weight that this package assumes.')])
    sq("control", Q_K24, "The residual DNA criterion is met through the clearance that the step reports show, and the master report PCMR-001 assesses the capability of the drug substance against it (PCMP-001 §7.3).")
    sq("control", Q_K26, 'A release test could not show the residual DNA criterion, because the qPCR method (AMV-3014) quantifies DNA only down to `{python} f"{dna_loq:g}"` pg/mg, which is `{python} f"{dna_loq_dose:g}"` ng per dose, `{python} f"{dna_loq_x:,.0f}"` times the criterion.')
    sq("control", Q_K27)
    sq("control", Q_K28)
    sq("control", "The anion exchange step binds both viruses by their surface charge in flow-through mode, and the virus filter retains both by their size.")
    sq("control", "These mechanisms act on different properties of the virus particle.",
       "Low-pH inactivation, anion exchange and virus filtration act on different properties of the virus particle.")
    sq("control", "A particle that survives one step is therefore no more likely to survive the next, and the log reductions are added")
    sq("control", "Each claimed step is held to its platform claim (PCMP-001 §7.4).")
    sq("control", 'a sum of `{python} f"{x_sum:g}"` against a cumulative requirement of `{python} f"{x_req:g}"`',
       'For XMuLV the claims sum to `{python} f"{x_sum:g}"` log10 against a cumulative requirement of `{python} f"{x_req:g}"`.')
    sq("control", 'a sum of `{python} f"{m_sum:g}"` against `{python} f"{m_req:g}"`',
       'For MVM the claims sum to `{python} f"{m_sum:g}"` log10 against a cumulative requirement of `{python} f"{m_req:g}"`.')
    sq("control", "Both requirements are met by the claims alone, with `{python} margin_txt`.",
       "Both viral clearance requirements are met by the claims alone, with `{python} margin_txt`.")
    sq("control", "With these margins every claimed step is therefore needed, and a step that falls short of its claim cannot be made up by the others.")
    sq("control", Q_K38)
    sq("control", Q_K39)
    sq("control", Q_K40, "The master report PCMR-001 states the cumulative viral clearance and compares it with the drug substance acceptance criteria.")
    sq("control", "The control strategy is transferred when PCMR-001 has been approved and the classes it consolidates have been written into the master batch record.")
    sq("control", "The engineering batches and the qualification batches are both run under that batch record (@tbl-deliverables).",
       "The engineering batches and the qualification batches are both run under the master batch record.")

    # Process performance qualification strategy
    sq("ppq", "Process performance qualification is the part of Stage 2 that follows this transfer",
       "Process performance qualification is the part of Stage 2 that follows the transfer.")
    sq("ppq", "Stage 2 also covers the qualification of the facility, equipment and utilities, which condition 3 below requires before the campaign starts.",
       "Stage 2 also covers the qualification of the facility, equipment and utilities, which the third start condition requires before the qualification campaign starts.")
    sq("ppq", "Process performance qualification demonstrates that the commercial process, run by the receiving site with the transferred methods and control strategy, reproducibly delivers drug substance of the required quality.")
    sq("ppq", "The campaign will manufacture `{python} n_ppq` consecutive batches at commercial scale under the approved master batch record.",
       "The qualification campaign will manufacture `{python} n_ppq` consecutive batches at commercial scale under the approved master batch record.")
    sq("ppq", Q_Q7, "Every parameter will be held at its set-point in the parameter table during the qualification campaign, and no deliberate excursion will be run.")
    sq("ppq", "It is measured, not set, because it is the response of centrifugation (rcf) and depth filter load.",
       "Post-clarification turbidity is the exception: it is measured, not set, because it is the response of centrifugation (rcf) and depth filter load.",
       also=[("ppq", "Post-clarification turbidity is the exception.")])
    conds = re.findall(r"^\d\. (.+)$", src[src.index("The campaign may start when the following conditions are met:"):
                                         src.index("The qualification protocol will set the sampling plan")], flags=re.M)
    if len(conds) != 5:
        raise ValueError(f"{DOC}: {len(conds)} start conditions of the qualification campaign")
    for i, cond in enumerate(conds, 1):
        txt = re.sub(r"^The gaps in Section \d+", "The transfer gaps", _text(cond, xr))
        refs = [ref("ppq", q(cond))]
        if i == 1:
            refs.append(ref("ppq", q("The campaign may start when the following conditions are met:")))
        st("ppq", f"Start condition {i} of the qualification campaign: {_lc(txt)}", refs)
    sq("ppq", "The qualification protocol will set the sampling plan of the campaign, with more sampling and testing than routine manufacture, as the lifecycle guidance expects")
    sq("ppq", "The sampling plans of the step plans are for small-scale runs.")
    sq("ppq", "Each intermediate for which PCMP-001 Version 2.0 §7.3 defines an intermediate acceptance criterion will be tested against it, as in the characterization.",
       "In the qualification campaign each intermediate for which PCMP-001 Version 2.0 §7.3 defines an intermediate acceptance criterion will be tested against it, as in the characterization.")
    sq("ppq", "The master plan PCMP-001 plans the characterization campaign that produces the evidence, and the master report PCMR-001 consolidates it.")
    sq("ppq", "Both are approved before the qualification campaign starts.",
       "PCMP-001 and PCMR-001 are both approved before the qualification campaign starts.")
    sq("ppq", "Continued process verification begins when the qualification campaign is complete.")
    sq("ppq", "The receiving site will draft the monitoring plan during the campaign.")
    sq("ppq", "The plan may not be finalized until the campaign data are available, because its control limits are derived from the performance that the commercial process actually shows",
       "The monitoring plan may not be finalized until the campaign data are available, because its control limits are derived from the performance that the commercial process actually shows.")

    # Gap analysis
    sq("gaps", "The gaps in @tbl-gaps were identified at the approval of Version 1.0 of this plan, by comparing what the receiving site held with what the qualification campaign requires.",
       "The transfer gaps were identified at the approval of Version 1.0 of PTP-001, by comparing what the receiving site held with what the qualification campaign requires.")
    sq("gaps", "A gap must be closed before the qualification campaign starts, or its residual risk must be assessed and accepted under the quality system")
    sq("gaps", Q_G4)
    sq("gaps", Q_G6)
    sq("gaps", Q_G8, "The gap on harvest and UF/DF is accepted because the risk assessment RA-001 ranked none of the parameters of either step high and expected none of them to interact with another parameter (PCMP-001 Version 2.0 §4).")
    sq("gaps", "An interaction between two of them is therefore not expected to affect a quality attribute in @tbl-cqa.",
       "An interaction between two parameters of harvest or of UF/DF is therefore not expected to affect a drug substance quality attribute.")

    # Roles and responsibilities
    sq("roles", "The transfer is run by a joint team drawn from both sites.")
    sq("roles", "MSAT leads the team at each site, and Quality Assurance approves each handover.")
    for fn, row in rorow.items():
        site = ro_df.loc[ro_df["Function"] == fn, "Site"].iloc[0]
        resp = ro_df.loc[ro_df["Function"] == fn, "Responsibility"].iloc[0]
        where = "At both sites" if site == "Both" else f"At the {site.lower()} site"
        st("roles", f"{where}, {fn} {resp[0].lower() + resp[1:]}.", [tref("roles", ro_t, rorow, fn)])
    sq("roles", "Depending on the size of the team at the receiving site, one person may hold more than one function.")
    sq("roles", "The separations of duty in @sec-methods and @sec-approvals are the exception and are not waived.",
       "The separations of duty for a method transfer and for a revision of the plan are the exception and are not waived.")

    # Deliverables and schedule
    sq("schedule", "@tbl-deliverables lists what this plan commits to and the order in which the deliverables arrive.",
       "PTP-001 lists what it commits to and the order in which the deliverables arrive.")
    for d_, row in dlrow.items():
        _, owner, dep = dl_cells[d_]
        st("schedule", f"Deliverable of the transfer: {d_}. Owner: {owner}. It depends on "
           f"{_lc(dep.replace('This plan', 'PTP-001'))}.", [tref("schedule", dl_t, dlrow, d_)])
    sq("schedule", "The characterization work sets the duration of the transfer.")
    sq("schedule", "Neither the engineering batches nor the qualification campaign can start until PCMR-001 is approved, and PCMR-001 cannot be written until every characterization report is complete.")
    sq("schedule", "Equipment and utility qualification and method transfer do not wait on that chain.",
       "Equipment and utility qualification and method transfer do not wait on the characterization chain, and each can start when PTP-001 is approved.",
       also=[("schedule", "Each can start when this plan is approved (@tbl-deliverables).")])
    sq("schedule", "Operator training on the master batch record follows that record and is completed before the engineering batches (@tbl-equivalency).")
    sq("schedule", "This plan was approved on `{python} appr_v1`.",
       "Version 1.0 of PTP-001 was approved on `{python} appr_v1`.")
    sq("schedule", "The risk assessment RA-001 followed on `{python} ra_appr` and the master plan PCMP-001 on `{python} pcmp_appr`.")
    sq("schedule", "A window runs from the first day of the first study of the step to the last day of its last study.",
       "An execution window runs from the first day of the first study of the step to the last day of its last study.")
    sq("schedule", "Each step plan was approved before the first study of its step began.")
    sq("schedule", "The windows of several steps overlap.",
       "The execution windows of several steps overlap.")
    sq("schedule", "The `{python} n_v1` studies ran from `{python} first_start` to `{python} last_end`, and the Version 1.0 reports are dated `{python} pkg_date`.",
       "The `{python} n_v1` studies that Version 1.0 reported ran from `{python} first_start` to `{python} last_end`, and the Version 1.0 reports are dated `{python} pkg_date`.")
    for plan, row in chrow.items():
        r = ch_df.set_index("Plan").loc[plan]
        n = int(r["Studies"])
        st("schedule", f"{plan}, the plan of {r['Unit operation']} (Step {r['Step']}), was approved on "
           f"{r['Plan approved']}; the {n} {'study' if n == 1 else 'studies'} of the step that Version 1.0 "
           f"reported ran from {r['First study start']} to {r['Last study end']}.",
           [tref("schedule", ch_t, chrow, plan)])

    # Approvals
    sq("approvals", "This plan takes effect when the functions in the approval record at the front of this document have approved it.",
       "PTP-001 takes effect when the functions in its approval record have approved it.")
    sq("approvals", "A revision is required when the scope of the transfer changes, when a unit operation is added to the train or removed from it, or when a gap in @sec-gaps is closed by a route other than the action recorded against it.",
       "A revision of PTP-001 is required when the scope of the transfer changes, when a unit operation is added to the train or removed from it, or when a transfer gap is closed by a route other than the action recorded against it.")
    sq("approvals", "The author of a revision may not approve it.")

    order = list(dict.fromkeys(path[0] for k_, path in SEC.items() if k_ != "title"))
    report_sections = []
    for title in order:
        stmts = [s_ for t_, s_ in ST if t_ == title]
        if stmts:
            report_sections.append(ReportSection(section_id=f"{DOC}-sec{len(report_sections) + 1:02d}",
                                                 title=title, statements=stmts))

    # ==== concepts ===================================================================================
    concepts = [
        Concept(concept_id="process:amab_ds", concept_type="PROCESS", canonical_name="A-Mab drug substance process",
                aliases=["A-Mab drug substance manufacturing process", "A-Mab drug substance"],
                review_status="human_verified"),
        Concept(concept_id="transfer:amab_ds", concept_type="TECHNOLOGY_TRANSFER",
                canonical_name="Transfer of the A-Mab drug substance process",
                aliases=["the transfer", "process transfer"], review_status="human_verified"),
    ]
    for k in steps:
        al = [k, f"Step {num_of[k]}", uo_of[k].name, T.STEP_NAME[k], T.step_mid(k)]
        concepts.append(Concept(concept_id=f"step:{k}", concept_type="PROCESS_STEP", canonical_name=title_of[k],
                                aliases=[a for a in dict.fromkeys(al) if a != title_of[k]],
                                review_status="human_verified"))
    concepts += G._attr_concepts(ckeys)
    concepts += [Concept(concept_id=pid[kn], concept_type="PROCESS_PARAMETER", canonical_name=kn[1],
                         aliases=[f"{kn[1]} ({T.STEP_NAME[kn[0]]})"], review_status="human_verified")
                 for kn in prow]
    concepts += [Concept(concept_id=f"method:{m.method_id}", concept_type="ANALYTICAL_METHOD",
                         canonical_name=sop_title[m.method_id],
                         aliases=[a for a in dict.fromkeys([m.method_id, m.method_name]) if a != sop_title[m.method_id]],
                         review_status="human_verified") for m in methods]
    concepts += [Concept(concept_id=e.equipment_id, concept_type="EQUIPMENT", canonical_name=e.equipment_name,
                         review_status="human_verified") for e in equipment]
    concepts += [Concept(concept_id=s_.site_id, concept_type="MANUFACTURING_SITE", canonical_name=s_.site_name,
                         aliases=[s_.location], review_status="human_verified") for s_ in sites]
    concepts += [Concept(concept_id=f"gap:{g.gap_id}", concept_type="TRANSFER_GAP", canonical_name=g.description,
                         aliases=[g.gap_id], review_status="human_verified") for g in gaps]

    # ==== the annex ==================================================================================
    annex = S.GroundTruthAnnex(
        document_id=DOC, document_title=f"{P.DOC_REGISTRY[DOC][0]} — {P.DOC_REGISTRY[DOC][1]}",
        document_class=P.DOC_REGISTRY[DOC][0], **G.rev2_layer(DOC, FILE),
        schema_extensions_used=G.COMMON_EXT + G.REV2_EXT[:1],
        out_of_schema_notes=[
            "The transfer plan spans the whole train. Entities are the two sites, the Step "
            f"{ns['step_first']}-{ns['step_last']} process steps (each anchored on its rows of the process train, "
            "characterization scope and chronology tables), the eleven drug substance quality attributes, every "
            "parameter of the train with the set-point, NOR and class in force at Version 2.0 (PTP-001 carries "
            "the class of each step report and does not re-derive it), every method validation of the "
            "procedures table, the development train and the commercial equipment train, the control strategy "
            "elements and the modular viral clearance claims. ProcessParameter.PAR carries the characterized "
            "range, as everywhere in the corpus; the plan claims no proven acceptable range and draws no design "
            "space, so it has neither record.",
            "QualityAttribute.acceptance_criteria are the drug substance criteria of the attribute table; "
            "tool2_severity is left empty because PTP-001 does not state it. associated_steps and the "
            "step_has_quality_attribute assertions follow the principal role of each step in the process train "
            "table, plus the prose that states where aggregate forms at low pH; they are not the 'set_by' column "
            "of the CQA register, which PTP-001 does not print. QualityAttribute.analytical_method is the method "
            "the plan pairs with the attribute (for aggregate, AMV-3221, the SEC record transferred).",
            "acceptance_criteria is empty. PTP-001 sets no step criterion (an ExplicitNonClaim), prints no "
            "criteria-change table and no table of intermediate acceptance criteria; it refers to PCMP-001 "
            "Version 2.0 §7.3 and states only their number. The drug substance criteria are "
            "attribute_has_acceptance_criterion assertions on the attribute rows.",
            "The plan has no designed experiment of its own and lists no study, only the number of studies and "
            "the execution window of each step (statements on the chronology rows). The one study it names, "
            f"{ns['first_study']}, the first characterization study, is a StudyDesign without design fields.",
            "The seven transfer gaps keep the gap ids of the Version 1.0 annex; each is anchored on its row of the "
            "gap table and on the sentences of the gap analysis that say how it is closed or managed. Every gap "
            "is 'open': the plan closes none, and it says that the gaps on harvest and UF/DF and on viral "
            "clearance are managed, not closed. transfer_has_gap assertions have the subject transfer:amab_ds.",
            "Each ModularContribution is one claimed step of a cumulative viral clearance requirement, anchored on "
            "the sentence that states the claims of that virus and on the attribute row that carries the "
            "requirement. ControlStrategyElement records are the three layers of the control strategy, the "
            "contents of the master batch record, the clearance route for residual DNA and the batch-record "
            "control of the viral clearance load conditions.",
            "The rows of the six pipe tables (package, process train, site equivalency, characterization scope, "
            "gaps, deliverables) are rebuilt by re-running the chunk that prints each, with every "
            "cross-reference written as the rendered document numbers it. Each changed set-point and NOR is a "
            "statement anchored on its footnote of the parameter table and on its row.",
            "AnalyticalMethod records: every method validation of the procedures table, each anchored on its "
            "row there, the nine methods to be transferred also on their row of the methods table, and the "
            "methods the prose discusses on its sentences. The qualified performance of each transferred method "
            "is a statement on its row. AMV-3011 (SEC for size variants) and the two infectivity titre assays "
            "are not transferred (ExplicitNonClaim records); nrCE-SDS (AMV-3020) is transferred with no row in "
            "the record of qualified method performance. The concept of a method carries the title of its "
            "validation as canonical name.",
            "The approval table, the abbreviations and the procedure rows of the procedures table that the prose "
            "does not discuss are not represented. No rhetorical_spans (a plan has no spans file). weak_claims "
            "is empty, and the plan carries no registered discrepancy.",
        ],
        inventory=G.rev2_inventory(DOC, FILE, "process_transfer_plan", "A-Mab drug substance",
                                   ["technology transfer", "process transfer", "site equivalency",
                                    "scale-down model qualification", "comparability",
                                    "analytical method transfer", "control strategy",
                                    "intermediate acceptance criteria", "modular viral clearance claim",
                                    "gap analysis", "process performance qualification"]),
        entities=entities, studies=studies, report_sections=report_sections, transfer_gaps=gaps,
        assertions=AssertionStore(run_id=f"gt-{DOC}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{DOC}", concepts=concepts))
    _gate(annex, text)
    return annex
