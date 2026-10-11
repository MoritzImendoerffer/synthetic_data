"""PCR-008 Version 2.0, the characterization report of anion exchange chromatography (Step 8), re-analysed
under INV-001 and INV-002: its ground-truth annex (``build()``).

The kinds of record follow the Version 2.0 report builders with a designed experiment (``pcr_009.py``,
``pcr_006.py``, ``pcr_003.py``) and the concept ids follow the Version 1.0 builder of this report
(``build_report_aex``) and the Version 2.0 builder of its plan (``pcp_008.py``): the inventory and the
revision layer; the step, its scale-down model and the two sites; the five parameters, with the class and the
classification argument of the report; the six attributes of the attribute table (the two cumulative viral
clearance attributes, host cell protein, residual DNA, leached Protein A and fragments); the analytical
methods; the capability records; the two modular viral clearance contributions; the fitted models (the planned
full quadratic of every output with a criterion, the full quadratic with a block on all runs, the selected
models and the screening models); the three study events; the document relationships and the explicit
non-claims; the studies of the execution-window table that have a schema study type; the design space; the
proven acceptable ranges; the criteria of the criteria-change table (Version 1.0 superseded, Version 2.0 in
force); the assertions; the report statements, grouped by the chapters of the report; the concepts; and the
rhetorical spans of ``authoring/rhetorical/PCR-008.spans.yaml``.

Every table of the report is a complex table (``T.frame`` or a ``T.`` builder), read back through
``qmd_ctables`` from the object the report printed, or a markdown string of a ``_pcpkg`` helper
(``related_docs_md``, ``dev_register``, ``discrepancy_register``), read back with ``md_string_rows``, so each
row quote is the rendered row, with ``table_header=rows.header``. Every prose quote is a span of the ``.qmd``
found by ``S_`` (a unique prefix of the source, run to the end of its sentence or to a given end string) and
rendered as the ``.docx`` reads it (``render``: the inline expressions evaluated in the report's own
namespace, a cross-reference resolved to its rendered number, typographic quotes and apostrophes), so no value
and no quote is typed here. ``q`` refuses a span that crosses a citation, and ``build()`` refuses to return an
annex with a quote that does not ground or a weak anchor.

The proven acceptable ranges are recorded as the report prints them: the "PAR (set-point)" column of the PAR
table goes to ``par_at_setpoint`` as printed, and the report's description of the two analyses is recorded in
its own words. Nothing is added to it (registered discrepancy D-001). The coding of protein load about the
middle of its range (PD-008-09) is recorded only as the report states it, in its statistical methods, its
study design and its discrepancy register.
"""
from __future__ import annotations

import os
import re

import _pcpkg as P
import build_ground_truth as G
import schema_ext as S
from check_grounding import normalize, specificity_report

DOC = "PCR-008"
FILE = "PCR-008_aex.docx"
QMD = "PCR-008_aex.qmd"
UO = "aex"
STEP_ID = "step:aex"
SDM_ID = "equip:aex_sdm_column"
#: The scale-down model as the report names it (Section 3.1).
SDM_NAME = "scale-down model of the commercial anion exchange column"

_INTRO = "Introduction"
_PRIOR = "Prior knowledge and quality risk basis"
_MM = "Materials and methods"
_STAT = "Statistical methods"
_SD = "Study design"
_RES = "Results"
_RSM = "Response-surface models"
_PAR = "Proven acceptable ranges"
_REC = "Study events and discrepancies from the plan"
_EV = "Study events"
#: Section key -> heading path as the .qmd writes it. ``_check_sections`` checks every title against the
#: headings of the .qmd, so a renamed section fails loudly instead of mislabelling its references.
SEC = {
    "title": ("Title block",),
    "exec": ("Executive summary",),
    "uo": (_INTRO, "Product and unit operation"),
    "objectives": (_INTRO, "Objectives"),
    "basis": (_INTRO, "Regulatory and scientific basis"),
    "changes": (_INTRO, "Changes in this revision"),
    "platform": (_PRIOR, "Platform and prior-product knowledge"),
    "cqa": (_PRIOR, "Quality attributes in scope"),
    "risk": (_PRIOR, "Risk-based prioritization and parameter selection"),
    "sdm": (_MM, "Scale-down model and its qualification"),
    "operation": (_MM, "Operation"),
    "analytics": (_MM, "Analytical methods"),
    "sampling": (_MM, "Sampling plan"),
    "stats": (_MM, _STAT),
    "coding": (_MM, _STAT, "Coding and the screening model"),
    "selection": (_MM, _STAT, "The response-surface models and their selection"),
    "logscale": (_MM, _STAT, "The log scale"),
    "adequacy": (_MM, _STAT, "Model adequacy"),
    "judgement": (_MM, _STAT, "Judgement over the NOR"),
    "par_method": (_MM, _STAT, "Proven acceptable ranges and the design space"),
    "cap_method": (_MM, _STAT, "Capability and other comparisons"),
    "factors": (_SD, "Factors, ranges and the knowledge space"),
    "scr_design": (_SD, "Screening design"),
    "rsm_design": (_SD, "Response-surface design"),
    "uni_design": (_SD, "Univariate assessment"),
    "centre": (_RES, "Centre-point performance and reproducibility"),
    "screening": (_RES, "Screening: factor effects"),
    "selected": (_RES, _RSM, "Selected models and their adequacy"),
    "coef": (_RES, _RSM, "Coefficients, analysis of variance and effect sizes"),
    "reeval": (_RES, _RSM, "The augmentation and the re-evaluation"),
    "near": (_RES, _RSM, "Models within 2 AICc units"),
    "influence": (_RES, _RSM, "Residuals and influential runs"),
    "surfaces": (_RES, _RSM, "Response surfaces and diagnostics"),
    "flow": (_RES, "Univariate assessment of operating flow rate"),
    "dna": (_RES, "Residual DNA and leached Protein A"),
    "mech": (_RES, "Mechanistic interpretation"),
    "ds": ("Design space",),
    "par_basis": (_PAR, "Acceptance basis"),
    "par_results": (_PAR, "Outputs against their criteria"),
    "par_ranges": (_PAR, "Proven acceptable ranges of the multivariate parameters"),
    "par_flow": (_PAR, "Operating flow rate"),
    "verif": (_PAR, "Verification of the platform worst case"),
    "cap": ("Process capability and robustness",),
    "class": ("Parameter classification",),
    "cs": ("Contribution to the control strategy",),
    "disc": ("Discussion",),
    "concl": ("Conclusions",),
    "record": (_REC,),
    "events": (_REC, _EV),
    "dev1": (_REC, _EV, "DEV-008-01, a non-representative load in the first execution"),
    "dev2": (_REC, _EV, "DEV-008-02, the pool-collection set-point"),
    "dev3": (_REC, _EV, "DEV-008-03, an equilibration and wash buffer below its pH range"),
    "pds": (_REC, "Discrepancies from the plan"),
    "app_a": ("Appendix A — Screening design matrix and responses",),
    "app_b": ("Appendix B — Response-surface design matrix and responses",),
    "app_c": ("Appendix C — Full effect and coefficient tables",),
    "app_d": ("Appendix D — Analytical methods summary",),
}
#: Relationship cell of the related-documents table -> DocumentRelationship.kind (others: references).
REL_KIND = {"Rolls up into": "rolls_up_into", "Sibling — paired document": "executed_under",
            "Parent — master plan": "executed_under",
            "Parent — risk basis for study scope": "scoped_by", "Parent — transfer scope": "scoped_by"}
#: The report's statements are grouped by the chapters of the report, in this order.
CHAPTERS = ["Executive summary", _INTRO, _PRIOR, _MM, _SD, _RES, "Design space", _PAR,
            "Process capability and robustness", "Parameter classification", "Contribution to the control strategy",
            "Discussion", "Conclusions", _REC, "Appendix A — Screening design matrix and responses",
            "Appendix B — Response-surface design matrix and responses",
            "Appendix C — Full effect and coefficient tables", "Appendix D — Analytical methods summary"]
#: Validation reference -> attribute keys it measures in this report (the methods summary, Appendix D).
METHOD_ATTR = {"AMV-3012": ["hcp"], "AMV-3014": ["residual_dna"], "AMV-3016": ["leached_protein_a"],
               "AMV-3017": ["lrv_xmulv"], "AMV-3018": ["lrv_mvm"], "AMV-3020": ["fragments_lmw"],
               "AMV-3019": ["step_yield"], "AMV-3013": []}


def _sid(sec):
    return f"{DOC}_sec_{sec}"


def _source():
    return open(os.path.join(G.HERE, QMD), encoding="utf-8").read()


def _raw_prose():
    """The .qmd outside its code chunks, as written (line structure kept)."""
    return re.sub(r"```\{python\}.*?```", " ", _source(), flags=re.S)


def _headings():
    """``[(level, title, attributes)]`` of the .qmd, outside its code chunks, in document order."""
    prose = re.sub(r"```\{python\}.*?```", "", _source(), flags=re.S)
    return [(len(m.group(1)), m.group(2), m.group(3) or "")
            for m in re.finditer(r"^(#+) (.+?)(?: \{([^}]*)\})?\s*$", prose, flags=re.M)]


def _check_sections():
    """Every heading of SEC is a heading of the .qmd (outside its code chunks)."""
    heads = {t for _, t, _ in _headings()}
    missing = sorted({t for path in SEC.values() for t in path if t != "Title block"} - heads)
    if missing:
        raise ValueError(f"{DOC}: section titles not in the document: {missing}")


def _md_captions():
    """``{tbl- label -> caption}`` of the markdown tables the chunks print (``print(": <caption> {#tbl-x}")``)."""
    return {m.group(2): m.group(1)
            for m in re.finditer(r'print\(": (.*?) \{#(tbl-[\w-]+)\}"\)', _source())}


def _xrefs(text):
    """``{label -> rendered cross-reference}`` ("sec-par" -> "Section 9", "tbl-par" -> "Table 22").

    A section number follows the numbering of the headings (an unnumbered heading takes none), as the
    rendered document prints it. A table or figure number is read off the rendered caption ("Table 22:
    <caption>"), with the caption taken from the object or chunk that prints it."""
    out, counters = {}, [0] * 6
    for lvl, _, attrs in _headings():
        if ".unnumbered" in attrs or attrs.strip() == "-":
            continue
        counters[lvl - 1] += 1
        counters[lvl:] = [0] * (6 - lvl)
        lab = re.search(r"#(sec-[\w-]+)", attrs)
        if lab:
            out[lab.group(1)] = "Section " + ".".join(str(c) for c in counters[:lvl])
    caps = dict(_md_captions())
    for code in re.findall(r"```\{python\}\n(.*?)```", _source(), flags=re.S):
        lab = re.search(r"#\|\s*label:\s*((?:tbl|fig)-[\w-]+)", code)
        cap = re.search(r'#\|\s*(?:tbl|fig)-cap:\s*"(.*)"', code)
        if lab and cap:
            caps[lab.group(1)] = cap.group(1)
    for lab, (tab, _) in G.qmd_ctables(QMD).items():
        caps.setdefault(lab, tab.caption)
    for lab, cap in caps.items():
        word = "Table" if lab.startswith("tbl-") else "Figure"
        m = (re.search(word + r" (\d+): " + re.escape(normalize(cap)), text)
             or re.search(word + r" (\d+): " + re.escape(normalize(cap.replace("'", "’"))), text))
        if m:
            out[lab] = f"{word} {m.group(1)}"
    return out


def _smart(s):
    """Prose as pandoc renders it: straight double quotes become typographic pairs, a straight apostrophe a
    typographic one, and the .docx reads a closing quote as its own run (a space follows it)."""
    s = re.sub(r'"([^"]*)"', "“\\1”", s).replace("'", "’")
    return re.sub(r"”(?=\S)", "” ", s)


def _cells(row):
    """The cells of a rendered row: a continuation row keeps its empty leading cells."""
    return [c.strip() for c in row.split("|")]


def _unmark(cell):
    """A rendered cell without its trailing footnote markers ("13.9 a)", "≥ 16.7 b)")."""
    return re.sub(r"(?:\s[a-z]\))+$", "", str(cell)).strip()


def _num(cell):
    """A number as the document prints it, back to a float ("−0.3398", "2,785.30", "×0.979 a)"); None for a
    cell that is not one ("< 0.001", "n.a.")."""
    s = _unmark(cell).replace("−", "-").replace(",", "").lstrip("×")
    try:
        return float(s)
    except ValueError:
        return None


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


def build():  # noqa: C901 - one document, one builder, in the order of the report
    import numpy as np
    import tables as T
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    from annex_contract.concepts import Concept, ConceptStore
    from annex_contract.discourse import DocumentRelationship, ExplicitNonClaim
    from annex_contract.results import (Deviation, ModelTerm, ModularContribution, ProcessCapability,
                                        StatisticalModelFit)
    from annex_contract.summaries import ReportSection, ReportStatement

    _check_sections()
    ns, _shown = G.qmd_namespace(QMD)
    ct = G.qmd_ctables(QMD)
    text = G._document_text(FILE)
    raw = _raw_prose()
    prose_src = normalize(raw)
    xref = _xrefs(text)
    md_caps = _md_captions()
    meta = G.meta

    def render(src):
        """A span of the .qmd as the .docx reads it."""
        s = G.qmd_inline(ns, src)
        if "[@" in s:
            raise ValueError(f"{DOC}: a quote crosses a citation, end it before: {src!r}")
        if "$" in s:
            raise ValueError(f"{DOC}: a quote crosses inline mathematics: {src!r}")
        s = re.sub(r"@((?:sec|tbl|fig)-[\w-]*\w)", lambda m: f" {xref[m.group(1)]} ", s)
        return re.sub(r"\s+", " ", _smart(s)).strip()

    def S_(prefix, upto=None):
        """The .qmd source of one span: the unique occurrence of ``prefix`` in the prose, run to the end of
        its sentence (a full stop outside an inline expression, followed by a space or the end of the line),
        or to the end of ``upto``. A span never crosses a line."""
        hits = [m.start() for m in re.finditer(re.escape(prefix), raw)]
        if len(hits) != 1:
            raise ValueError(f"{DOC}: {len(hits)} occurrences of the prefix {prefix!r} in the .qmd prose")
        i = hits[0]
        if upto is not None:
            j = raw.index(upto, i) + len(upto)
        else:
            tick, j = False, i
            while True:
                c = raw[j]
                if c == "`":
                    tick = not tick
                elif c == "\n":
                    raise ValueError(f"{DOC}: no end of sentence after {prefix!r}")
                elif c == "." and not tick and (j + 1 == len(raw) or raw[j + 1] in " \n"):
                    j += 1
                    break
                j += 1
        span = raw[i:j]
        if "\n" in span:
            raise ValueError(f"{DOC}: the span of {prefix!r} crosses a line")
        return span

    def S_first(item, n=45):
        """The first sentence of a list item, by the shortest prefix of at least ``n`` characters that is unique."""
        while True:
            pre = item[:n]
            if len(re.findall(re.escape(pre), raw)) == 1 or n >= len(item):
                return S_(pre)
            n += 5

    def q(src):
        """A prose span of the .qmd as it renders. ``src`` must be a span of the .qmd prose."""
        if normalize(src) not in prose_src:
            raise ValueError(f"{DOC}: not a span of the .qmd prose: {src!r}")
        return render(src)

    def Q(prefix, upto=None):
        return q(S_(prefix, upto))

    def t(txt):
        """Annex text with the report's own values (inline expressions evaluated in its namespace)."""
        return G.qmd_inline(ns, txt)

    def title(sec):
        return SEC[sec][-1]

    def ref(sec, quote, table=None, rows=None, caption=None, label=None):
        r = G.ref(DOC, FILE, _sid(sec), title(sec), quote,
                  table_title=caption if table is None else table.caption,
                  table_id=label if table is None else table.label,
                  table_header=None if rows is None else rows.header)
        r.heading_path = list(SEC[sec])
        return r

    def present_header(rows):
        """The header of a table as the .docx reads it: two footnote markers in one header cell render
        side by side ("a)b)"), which ``ctable_rows`` joins with a space."""
        if normalize(rows.header) not in text:
            rows.header = re.sub(r"([a-z]\)) (?=[a-z]\))", r"\1", rows.header)
        if normalize(rows.header) not in text:
            raise ValueError(f"{DOC}: a table header does not ground: {rows.header!r}")
        return rows

    def keyed(label, keys, name_of, cell=None):
        """The rendered rows of the CTable the report printed under ``label``, keyed. Every row must name its
        own record (in cell ``cell``, footnote markers aside, or anywhere): a mis-keyed row grounds and
        attests the wrong thing."""
        tab = ct[label][0]
        rows_ = present_header(G.ctable_rows(tab, keys))
        bad = [k for k, row in rows_.items()
               if not (_unmark(_cells(row)[cell]) == name_of(k) if cell is not None else name_of(k) in row)]
        if bad:
            raise ValueError(f"{DOC} {label}: rows keyed to records they do not name: {bad}")
        miss = [k for k, row in rows_.items() if normalize(row) not in text]
        if miss:
            raise ValueError(f"{DOC} {label}: rows that do not ground: {miss}")
        return tab, rows_

    def unambiguous(rows_):
        """A table whose first cell is merged: a continuation row that occurs more than once in the document reads
        like the rows of other blocks, so its span runs from the row that opens its block to its own row, joined as
        the .docx reads them; every other row stays itself."""
        out_, block = G.RowQuotes(), []
        out_.header = rows_.header
        for k_, row in rows_.items():
            if _cells(row)[0]:
                block = []
            block.append(row)
            out_[k_] = row if text.count(normalize(row)) == 1 else G.CELL_SEP.join(block)
        return out_

    def ffill(col):
        out_, cur_ = [], None
        for v in col:
            cur_ = v if v else cur_
            out_.append(cur_)
        return out_

    def first_cells(label, i=0):
        return ffill([_cells(r)[i] for r in ct[label][0].rows()])

    def md_rows(md, label):
        rows_ = G.md_string_rows(md)
        # a markdown table is markdown: pandoc renders its straight apostrophes typographic
        for k_, v_ in list(rows_.items()):
            if normalize(v_) not in text and normalize(_smart(v_)) in text:
                rows_[k_] = _smart(v_)
        bad = [k_ for k_, v_ in rows_.items() if normalize(v_) not in text]
        if bad:
            raise ValueError(f"{DOC} {label}: rows that do not ground: {bad}")
        cap = md_caps[label]
        if normalize(f"{cap} {rows_.header}") not in text:
            raise ValueError(f"{DOC}: the caption of {label} no longer reads {cap!r}")
        return rows_, cap

    def fig_cap(label):
        """The caption of figure ``label``, from the option of the chunk that draws it."""
        code = next(c_ for c_ in re.findall(r"```\{python\}\n(.*?)```", _source(), flags=re.S)
                    if re.search(r"#\|\s*label:\s*" + re.escape(label) + r"\s*$", c_, flags=re.M))
        cap = re.search(r'#\|\s*fig-cap:\s*"(.*)"', code).group(1)
        if normalize(cap) not in text:
            raise ValueError(f"{DOC}: the caption of {label} does not ground: {cap!r}")
        return re.sub(r"\s+", " ", cap)

    # ---- names and values of the report ----------------------------------------------------------
    fx = ns["fx"]
    PRM = ns["P"]                                                 # parameter key -> config parameter
    FS = list(ns["FS"])                                           # the four multivariate parameters
    UNI = list(ns["UNI"])                                         # ["flow"]
    ALLP = FS + UNI
    NAME = {k: PRM[k].name for k in ALLP}
    UNIT = {k: PRM[k].unit for k in ALLP}
    LET = ns["LET"]
    D = ns["D"]
    HCP, XM, MV, YLD, FRAG = ns["HCP"], ns["XM"], ns["MV"], ns["YLD"], ns["FRAG"]
    RESP5 = [HCP, XM, MV, YLD, FRAG]
    CRIT_OUT = list(ns["CRIT_OUT"])
    RL, RU = ns["RL"], ns["RU"]
    OLAB = {r: f"{RL[r]} ({RU[r]})" for r in RESP5}              # the output cell of most result tables
    lab_resp = {v: k for k, v in OLAB.items()}
    UO_NAME, STEP_LABEL = G.AXUO_NAME, G.AXSTEP_LABEL
    PC = G.AXPARAM_CONCEPT                                        # parameter name -> concept id
    pkey = {NAME[k]: k for k in ALLP}
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))
    reg = P.cqa_reg.set_index("key")
    by_label = G._attr_key_by_label()
    resp_attr = {HCP: "hcp", XM: "lrv_xmulv", MV: "lrv_mvm", FRAG: "fragments_lmw", YLD: "step_yield"}
    attr_resp = {v: k for k, v in resp_attr.items()}
    CL_X, CL_M = ns["CL_X"], ns["CL_M"]
    CHRON = ns["CHRON"]
    SAY = {HCP: "pool host cell protein", XM: "the XMuLV LRF", MV: "the MVM LRF", YLD: "step yield", FRAG: "fragments"}

    def lc1(x):
        """A cell as the start of a clause: lower case, unless it opens with an acronym ("XMuLV infectivity")."""
        return x if len(x) > 1 and x[1].isupper() else x[:1].lower() + x[1:]

    def terms_txt(resp):
        tt = rsm(resp)["terms"]
        return "no term besides the block" if tt.startswith("None") else tt
    FIT = ns["FIT"]

    # ---- the rendered tables, from the objects the report printed --------------------------------
    pdf_ = ct["tbl-params"][1]
    pt_t, prow = keyed("tbl-params", list(pdf_["Parameter"]), str, cell=2)
    pdf_ = pdf_.set_index("Parameter")
    cq_df = ct["tbl-cqa"][1]
    ckeys = [by_label[n] for n in cq_df["Attribute"]]
    cq_t, crow = keyed("tbl-cqa", ckeys, lambda k: names[k], cell=1)
    cq_df = cq_df.set_index(np.array(ckeys))
    sop_df = ct["tbl-sops"][1]
    sop_t, soprow = keyed("tbl-sops", list(sop_df["Reference"]), str, cell=1)
    amv_title = dict(zip(sop_df["Reference"], sop_df["Title"]))
    ms_df = ct["tbl-methods-summary"][1]
    ms_t, msrow = keyed("tbl-methods-summary", list(ms_df["Method"]), str, cell=0)
    ms_df = ms_df.set_index("Method")
    st_df = ct["tbl-studies"][1]
    win_t, winrow = keyed("tbl-studies", list(st_df["Study"]), str, cell=1)
    off_lab = {"Host cell protein (ng/mg)": "hcp", "Step yield (%)": "step_yield",
               "Column efficiency (plates/m)": "plates", "Peak asymmetry": "asymmetry"}
    off_keys = [off_lab[_cells(r)[0]] for r in ct["tbl-sdm-offsets"][0].rows()]
    off_t, offrow = keyed("tbl-sdm-offsets", off_keys, lambda k: {v: k_ for k_, v in off_lab.items()}[k], cell=0)
    ikeys = [by_label[_cells(r)[0]] for r in ct["tbl-iac"][0].rows()]
    iac_t, irow = keyed("tbl-iac", ikeys, lambda k: T.ATTR_NAME[k], cell=0)
    crkeys = [by_label[_cells(r)[0]] for r in ct["tbl-criteria-aex"][0].rows()]
    cr_t, crrow = keyed("tbl-criteria-aex", crkeys, lambda k: T.ATTR_NAME[k], cell=0)
    rvkeys = [by_label[_cells(r)[0]] for r in ct["tbl-reeval-aex"][0].rows()]
    rv_t, rvrow = keyed("tbl-reeval-aex", rvkeys, lambda k: T.ATTR_NAME[k], cell=0)
    cen_df = ct["tbl-centre"][1]
    cen_t, cenrow = keyed("tbl-centre", list(zip(ffill(cen_df["Design"]), cen_df["Output"])), lambda k: k[1], cell=1)
    sc_df = ct["tbl-screening"][1]
    sc_t, scrow = keyed("tbl-screening", [lab_resp[x] for x in sc_df["Output"]], lambda r: OLAB[r], cell=0)
    rm_df = ct["tbl-rsm-models"][1]
    rm_t, rmrow = keyed("tbl-rsm-models", [lab_resp[x] for x in rm_df["Output"]], lambda r: OLAB[r], cell=0)
    ad_keys = [lab_resp[_cells(r)[0]] for r in ct["tbl-adequacy"][0].rows()]
    ad_t, adrow = keyed("tbl-adequacy", ad_keys, lambda r: OLAB[r], cell=0)
    co_df = ct["tbl-coef"][1]
    co_t, corow = keyed("tbl-coef", list(zip(ffill(co_df["Output"]), co_df["Term"])), lambda k: k[1], cell=1)
    COLAB = {HCP: f"{RL[HCP]} (ln ng/mg)", XM: f"{RL[XM]} (log10)", MV: f"{RL[MV]} (log10)"}
    an_df = ct["tbl-anova"][1]
    an_t, anrow = keyed("tbl-anova", list(zip(ffill(an_df["Output"]), an_df["Source"])), lambda k: k[1], cell=1)
    ne_df = ct["tbl-near"][1]
    ne_t, nerow = keyed("tbl-near", list(zip(ffill(ne_df["Output"]), ne_df["ΔAICc"])), lambda k: k[1], cell=1)
    in_df = ct["tbl-influence"][1]
    in_t, inrow = keyed("tbl-influence", list(zip(ffill(in_df["Output"]), in_df["Run"])), lambda k: k[1], cell=1)
    fl_df = ct["tbl-flow"][1]
    fl_t, flrow = keyed("tbl-flow", list(zip(ffill(fl_df["Setting"]), fl_df["Run"])), lambda k: k[1], cell=2)
    dna_df = ct["tbl-dna"][1]
    dna_lab = {"Residual DNA (pg/mg)": "residual_dna", "Leached Protein A (ppm)": "leached_protein_a"}
    dna_t, dnarow = keyed("tbl-dna", [dna_lab[x] for x in dna_df["Attribute"]],
                          lambda k: {v: k_ for k_, v in dna_lab.items()}[k], cell=0)
    par_df = ct["tbl-par"][1]
    par_keys = list(zip(ffill(par_df["CQA"]), par_df["Parameter"]))
    par_t, parrow = keyed("tbl-par", par_keys, lambda k: k[1], cell=1)
    par_lab = {D.RESP_LABEL[r]: r for r in CRIT_OUT}
    parrow = unambiguous(parrow)
    ver_t, verrow = keyed("tbl-iac-verification", ["hcp", "leached_protein_a"], lambda k: T.ATTR_NAME.get(k, names[k])
                          .split(" (")[0], cell=1)
    bd_df = ct["tbl-bound"][1]
    bd_t, bdrow = keyed("tbl-bound", list(bd_df["Analysis"]), str, cell=0)
    cap_df = ct["tbl-cap"][1]
    capkeys = [by_label[n] for n in cap_df["Attribute"]]
    cap_t, caprow = keyed("tbl-cap", capkeys, lambda k: names[k], cell=0)
    cap_df = cap_df.set_index(np.array(capkeys))
    ef_df = ct["tbl-effects-all"][1]
    ef_t, efrow = keyed("tbl-effects-all", list(zip(ffill(ef_df["Output"]), ef_df["Term"])), lambda k: k[1], cell=1)
    cr2_df = ct["tbl-coef-rest"][1]
    cr2_t, cr2row = keyed("tbl-coef-rest", list(zip(ffill(cr2_df["Output"]), cr2_df["Term"])), lambda k: k[1],
                          cell=1)
    mbs_t = ct["tbl-methods-by-study"][0]
    mbsrow = present_header(G.ctable_rows(mbs_t))
    mtx = {}
    for kind, label in (("screening", "tbl-doe-aex-screening"), ("rsm", "tbl-doe-aex-rsm"),
                        ("aug", "tbl-doe-aex-aug"), ("scr_sup", "tbl-doe-aex-screening-sup"),
                        ("rsm_sup", "tbl-doe-aex-rsm-sup")):
        tab = ct[label][0]
        mtx[kind] = (tab, present_header(G.ctable_rows(tab, [int(_cells(r)[0]) for r in tab.rows()])))
    rel, rel_cap = md_rows(P.related_docs_md(DOC), "tbl-related")
    devrow, dev_cap = md_rows(P.dev_register(DOC), "tbl-events")
    pdrow, pd_cap = md_rows(P.discrepancy_register(DOC), "tbl-discrepancies")
    PDS = {d["id"]: d for d in ns["PDS"]}

    def pdref(pid, sec="pds"):
        return ref(sec, pdrow[pid], rows=pdrow, caption=pd_cap, label="tbl-discrepancies")

    # ==== entities ===================================================================================
    q_flow_mode = Q("The step is operated in flow-through mode and is the last chromatography step")
    q_clears = Q("It clears host cell protein, residual DNA, leached Protein A and virus.")
    q_step8 = Q("Anion exchange chromatography is Step 8 of the train.")
    q_ligand = Q("The resin carries a quaternary amine ligand with a fixed positive charge.")
    q_passes = Q("At the load pH the antibody carries a net positive charge and passes through the bed")
    q_loaded = Q("The column is equilibrated, loaded with the cation exchange pool adjusted to its target pH")
    q_single = Q("The step processes the cation exchange pool of a single batch at commercial scale")
    step = S.ProcessStep(
        step_id=STEP_ID, step_name=UO_NAME, step_number=str(G.AXSTEP), unit_operation=UO_NAME,
        description=t("Step 8 of the A-Mab drug substance process, operated in flow-through mode, the last "
                      "chromatography step before virus filtration. The resin carries a quaternary amine ligand with "
                      "a fixed positive charge. At the load pH the antibody carries a net positive charge and passes "
                      "through the bed, while residual DNA, the acidic part of the host cell protein population, "
                      "leached Protein A and virus particles bind. The column is equilibrated, loaded with the cation "
                      "exchange pool adjusted to its target pH and conductivity, and chased with the first wash "
                      "buffer; the pool is collected from the start of the load to the end of the chase. The register "
                      "of critical quality attributes assigns to the step the cumulative MVM clearance, and it "
                      "contributes a modular XMuLV claim: `{python} CL_X` log10 for XMuLV and `{python} CL_M` log10 "
                      "for MVM."),
        input_materials=["cation exchange pool adjusted to the target pH and conductivity of the load"],
        output_materials=["flow-through pool (load of virus filtration)"],
        equipment=[SDM_NAME],
        source_references=[ref("exec", q_flow_mode), ref("exec", q_clears), ref("uo", q_step8),
                           ref("uo", q_ligand), ref("uo", q_passes), ref("uo", q_loaded), ref("uo", q_single)],
        metadata=meta())
    q_sdm1 = Q("The studies were executed on a scale-down model of the commercial anion exchange column")
    q_sdm2 = Q("The model keeps the bed height, the linear flow velocity, the protein load in grams")
    q_sdm3 = Q("The resin, the buffers and the packing method are the same as at commercial scale.")
    equipment = [S.Equipment(
        equipment_id=SDM_ID, equipment_name=SDM_NAME, equipment_type="chromatography column (scale-down model)",
        site_name=P.SENDING_SITE,
        source_references=[ref("sdm", q_sdm1), ref("sdm", q_sdm2), ref("sdm", q_sdm3)], metadata=meta())]
    sites = G._site_entities(DOC, FILE, _sid("title"))

    # -- parameters: the table row, the PAR rows (multivariate) or the PAR sentence (flow rate), and the
    # sentences of the classification argument -------------------------------------------------------------
    cls_src = {k: next(ln[2:] for ln in raw.splitlines() if ln.startswith(f"- {NAME[k]} (WC-CPP).")) for k in ALLP}
    cls_quotes = {
        "load_ph": [Q("Load pH acts on pool host cell protein and on both LRFs"),
                    Q("Its NOR lies inside every proven acceptable range."),
                    Q("The load is adjusted to its target pH before it is applied"),
                    Q("Load pH was classified as a WC-CPP.")],
        "wash1_cond": [Q("Equil/Wash-1 conductivity acts on pool host cell protein, a critical quality attribute"),
                       Q("The conductivity is set when the buffer is prepared."),
                       Q("Equil/Wash-1 conductivity was classified as a WC-CPP.")],
        "load_cond": [Q("Load conductivity lowers both LRFs (p < 0.001)"),
                      Q("The load is adjusted to its target conductivity before it is applied."),
                      Q("Load conductivity was classified as a WC-CPP.")],
        "load": [Q("The selected XMuLV model carries the interaction of protein load with load pH"),
                 Q("The class of WC-CPP is a conservative judgement on that term."),
                 Q("Protein load was classified as a WC-CPP.")],
        "flow": [Q("No effect of flow rate was detected."),
                 Q("The class of WC-CPP is a judgement on the scope of the viral clearance claim."),
                 Q("Operating flow rate was classified as a WC-CPP, so that it is held within the conditions")],
    }
    q_par_flow = Q("Every result at both ends of the range met the host cell protein criterion, so the range")
    q_intersect = Q("For a parameter that acts on several attributes the range carried into the control strategy")
    par_of = {}
    for k in FS:
        vals = {_cells(ct["tbl-par"][0].rows()[par_keys.index((lab_, NAME[k]))])[6] for lab_ in par_lab}
        par_of[k] = ns["INTERSECT_PH"] if k == "load_ph" else vals.pop()
        if k != "load_ph" and vals:
            raise ValueError(f"{DOC}: the NOR-propagated ranges of {k} differ between outputs; the text says none does")
    par_of["flow"] = ns["RNGS"]["flow"].replace(f" {UNIT['flow']}", "")
    params = []
    for name, row in prow.items():
        k = pkey[name]
        r = pdf_.loc[name]
        unit = r["Unit"]
        refs = [ref("factors", row, pt_t, prow)]
        if k in FS:
            refs += [ref("par_ranges", parrow[(lab_, name)], par_t, parrow) for lab_ in par_lab]
            if k == "load_ph":
                refs.append(ref("par_ranges", q_intersect))
        else:
            refs.append(ref("par_flow", q_par_flow))
        refs += [ref("class", x) for x in cls_quotes[k]]
        bullet = clean_(render(cls_src[k]))
        u_ = "" if unit == "pH" else f" {unit}"
        params.append(S.ProcessParameter(
            parameter_id=PC[name], parameter_name=name, parameter_type=PRM[k].classification, unit=unit,
            target_value=f"{r['Set-point']}{u_}", NOR=f"{r['NOR']}{u_}", PAR=f"{par_of[k]}{u_}",
            associated_step=STEP_LABEL,
            rationale_for_criticality="Classified under SOP-4001 by the decision logic of PCMP-001 §7.7. " + bullet,
            study_type="multivariate" if k in FS else "univariate", source_references=refs, metadata=meta()))

    # -- attributes: the register row, and for an output with a criterion the row of the criterion derivation
    # and the row of the outputs against their criteria; residual DNA and leached Protein A on their rows of
    # the residual DNA table ---------------------------------------------------------------------------------
    q_vh = Q("The two viral clearance attributes carry very high criticality by rule")
    q_mvm_set = Q("The register of critical quality attributes assigns the cumulative MVM clearance to this step")
    q_xm_claim = Q("The step also contributes a modular XMuLV clearance claim.")
    q_hcp_ds = Q("For pool host cell protein and fragments they equal the drug substance criteria")
    q_mon = Q("Residual DNA and leached Protein A have no intermediate acceptance criterion at this step")
    q_frag_mech = Q("Fragments of the antibody carry its positive charge at the load pH and flow through with it.")
    attr_prose = {"lrv_mvm": [("cqa", q_vh), ("uo", q_mvm_set)],
                  "lrv_xmulv": [("cqa", q_vh), ("uo", q_xm_claim)],
                  "hcp": [("cqa", q_hcp_ds)],
                  "residual_dna": [("cqa", q_mon)],
                  "leached_protein_a": [("cqa", q_mon)],
                  "fragments_lmw": [("cqa", q_hcp_ds), ("platform", q_frag_mech)]}
    method_of = {k: a for a, ks in METHOD_ATTR.items() for k in ks}
    for k_, a_ in method_of.items():
        if a_ not in ms_df.index:
            raise ValueError(f"{DOC}: the methods summary no longer lists {a_} for {k_}")
    DSC, TS1 = "Drug substance\ncriterion", "Tool #1\nscore"
    attrs = []
    for key in ckeys:
        r = cq_df.loc[key]
        crit = [f"{_unmark(_cells(crow[key])[3])} (drug substance)"]
        refs = [ref("cqa", crow[key], cq_t, crow)]
        if key in irow:
            ic = _cells(irow[key])
            crit.append(f"{_unmark(ic[-2])} {reg.loc[key, 'unit'].replace(' (cumulative)', '')} (intermediate "
                        f"acceptance criterion at the output of the step, {_unmark(ic[-1])})")
            refs += [ref("par_basis", irow[key], iac_t, irow), ref("par_results", crrow[key], cr_t, crrow)]
        else:
            refs.append(ref("dna", dnarow[key], dna_t, dnarow))
        viral = key.startswith("lrv_")
        why = (f"Very high by rule for viral clearance, because a viral contamination would harm the patient directly "
               f"(Tool #1 score {r[TS1]})." if viral else
               f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = {r[TS1]}.")
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=names[key], attribute_type="CQA",
            unit=reg.loc[key, "unit"], acceptance_criteria=crit, analytical_method=method_of[key],
            associated_steps=[STEP_LABEL], rationale_for_criticality=why, criticality_level=r["Criticality"],
            tool1_score=int(r[TS1]), tool2_severity=int(reg.loc[key, "tool2_severity"]),
            source_references=refs + [ref(s_, x) for s_, x in attr_prose[key]], metadata=meta()))

    # -- analytical methods: the procedure row, the methods-summary row, the sentence that names the method,
    # and for nrCE-SDS the row of the methods-by-study table ---------------------------------------------------
    q_meth = {"AMV-3012": Q("Pool host cell protein was measured by ELISA (AMV-3012)"),
              "AMV-3019": Q("Step yield is the mass of antibody in the pool divided by the mass loaded"),
              "AMV-3014": Q("Residual DNA was measured by qPCR (AMV-3014)"),
              "AMV-3013": Q("The charge variant profile of the load was measured by icIEF (AMV-3013).")}
    q_meth["AMV-3016"] = q_meth["AMV-3014"]
    q_meth["AMV-3017"] = Q("The infectivity of XMuLV was measured by TCID50 (AMV-3017)")
    q_meth["AMV-3018"] = q_meth["AMV-3017"]
    q_meth["AMV-3020"] = Q("Fragments were measured by nrCE-SDS (AMV-3020, under SOP-3015)")
    methods = []
    for amv in [a for a in sop_df["Reference"] if a.startswith("AMV-")]:
        m_ = ms_df.loc[amv]
        methods.append(S.AnalyticalMethod(
            method_id=amv, method_name=amv_title[amv], method_type=G.METHOD_TYPE.get(amv),
            analytes=[m_["Measured in this report"]], associated_attributes=[f"attr:{k}" for k in METHOD_ATTR[amv]],
            validation_status="validated",
            source_references=[ref("analytics", soprow[amv], sop_t, soprow),
                               ref("app_d", msrow[amv], ms_t, msrow), ref("analytics", q_meth[amv])]
            + (G.size_variant_refs(DOC, FILE, title("analytics"), [UO], G.SIZE_VARIANT_TOKEN[amv], text, lead=1)
               if amv in G.SIZE_VARIANT_TOKEN else []),
            metadata=meta()))

    # -- capability: one record per row of the capability table ----------------------------------------
    CAP, N_MC = ns["CAP"], int(ns["N_MC"])
    q_cap_vir = Q("The cumulative MVM clearance has the lowest Cpk,")
    q_cap_hf = Q("Pool host cell protein has a Cpk of")
    q_cap_dna = Q("Residual DNA has a Cpk of")
    q_cap_lpa = Q("Leached Protein A has a Cpk of")
    cap_prose = {"lrv_mvm": q_cap_vir, "lrv_xmulv": q_cap_vir, "hcp": q_cap_hf, "fragments_lmw": q_cap_hf,
                 "residual_dna": q_cap_dna, "leached_protein_a": q_cap_lpa}
    capab = []
    for key, row in caprow.items():
        c = cap_df.loc[key]
        mean_, sd_ = [x.strip() for x in c["Mean ± SD"].split("±")]
        capab.append(ProcessCapability(
            capability_id=f"{DOC}-CAP{len(capab) + 1:02d}", quality_attribute=f"attr:{key}", index_name="Cpk",
            index_value=_num(c["Cpk"]),
            specification_side={"lower": "lower", "upper": "upper"}.get(CAP.loc[key, "spec_type"], "two_sided"),
            acceptance_range=c[DSC], mean=mean_, standard_deviation=sd_,
            unit=reg.loc[key, "unit"], basis="simulated", n_batches=N_MC, unit_operation=UO_NAME,
            source_references=[ref("cap", row, cap_t, caprow), ref("cap", cap_prose[key])],
            metadata=meta()))

    # -- the modular viral clearance claims ------------------------------------------------------------
    q_sum_x = Q("The XMuLV claims of low-pH viral inactivation, anion exchange and virus filtration sum to")
    q_sum_m = Q("The MVM claims of anion exchange and virus filtration sum to")
    q_cs_v = Q("The step contributes `{python} CL_X` log10 for XMuLV and `{python} CL_M` log10 for MVM to the")
    title_of = P.UNIT_OP_TITLES
    step_of = lambda k: f"{title_of[k]} (Step {P.CFG.unit_op(k).step})"   # noqa: E731
    contributions = [
        ModularContribution(
            contribution_id=f"{DOC}-MC01", quantity=names["lrv_mvm"], unit_operation=UO_NAME,
            step_value=f"{CL_M} log10", cumulative_value=f"{ns['SUM_M']} log10", requirement=f"≥ {ns['REQ_M']} log10",
            unit="log10", contributing_steps=[step_of("virus_filtration")],
            source_references=[ref("par_basis", q_sum_m), ref("cs", q_cs_v)], metadata=meta()),
        ModularContribution(
            contribution_id=f"{DOC}-MC02", quantity=names["lrv_xmulv"], unit_operation=UO_NAME,
            step_value=f"{CL_X} log10", cumulative_value=f"{ns['SUM_X']} log10", requirement=f"≥ {ns['REQ_X']} log10",
            unit="log10", contributing_steps=[step_of("viral_inactivation"), step_of("virus_filtration")],
            source_references=[ref("par_basis", q_sum_x), ref("cs", q_cs_v)], metadata=meta())]

    # -- fitted models ---------------------------------------------------------------------------------
    fac_of = {v: k for k, v in LET.items()}

    def term_label(term):
        """A term of the coefficient tables ("A", "AD", "Block") in words."""
        if term == "Block":
            return "block (augmentation runs against planned runs, coded −1 and +1)"
        return " × ".join(ns["pn"](fac_of[x]) for x in term)

    def sig_of(p_):
        return p_.startswith("<") or (_num(p_) is not None and _num(p_) < float(ns["ALPHA"]))

    def terms_of(rows_, out_lab, cols):
        """The terms of one output's block of a coefficient or effect table, besides the intercept, as printed.
        ``cols`` names the cell index of each field ("effect", "coef", "se", "t", "p")."""
        out_ = []
        for (o_, term), row in rows_.items():
            if o_ != out_lab or term == "Intercept":
                continue
            c_ = _cells(row)
            g_ = {f: (_num(c_[i]) if f != "p" else c_[i]) for f, i in cols.items()}
            out_.append(ModelTerm(term=term, factor=term_label(term), effect=g_.get("effect"),
                                  coefficient=g_.get("coef"), standard_error=g_.get("se"),
                                  t_statistic=g_.get("t"), p_value=_num(g_["p"]), significant=sig_of(g_["p"])))
        return out_

    cen = {k: _cells(row) for k, row in cenrow.items()}
    fits = []

    def fit_rec(resp, form, refs, **kw):
        fits.append(StatisticalModelFit(
            model_fit_id=f"{DOC}-FIT{len(fits) + 1:02d}", response=resp, unit_operation=UO_NAME,
            model_form=form, source_references=refs, metadata=meta(), **kw))

    # the full quadratic model PCP-008 planned, on the planned runs; with a block on all runs where the
    # augmentation measured the output (re-evaluation table)
    q_full = Q("The plan's full quadratic models of all four outputs with a criterion failed its limit on overfitting.")
    q_full_hcp = Q("On all `{python} n_all` runs with a block term the same model meets the lack of fit test")
    for key, row in rvrow.items():
        c = _cells(row)
        resp = attr_resp[key]
        used = _unmark(c[-1])
        fit_rec(resp, "full quadratic (planned, PCP-008 §5.5), planned runs",
                [ref("reeval", row, rv_t, rvrow)] + ([ref("changes", q_full)] if resp == HCP else []),
                n_runs=int(c[1]), r_squared=_num(c[2]), predicted_r_squared=_num(c[3]),
                adequacy_statement=f"Planned full quadratic on the {c[1]} planned runs: R² {c[2]}, predicted R² {c[3]}, "
                                   f"R² minus predicted R² {c[4]}, above the limit on overfitting of PCMP-001 §7.2. "
                                   f"The model the output uses under the model selection (PD-008-02): {used}.")
        if len(c) >= 12:
            fit_rec(resp, "full quadratic with a block term, all runs (planned and augmentation)",
                    [ref("reeval", row, rv_t, rvrow)] + ([ref("reeval", q_full_hcp)] if resp == HCP else []),
                    n_runs=int(c[5]), r_squared=_num(c[6]), predicted_r_squared=_num(c[7]), lack_of_fit_p=_num(c[9]),
                    adequacy_statement=f"Full quadratic with a block term on all {c[5]} runs: R² {c[6]}, predicted R² "
                                       f"{c[7]}, R² minus predicted R² {c[8]}, lack of fit p {c[9]}, block p {c[10]}.")

    def adeq(resp):
        c = _cells(adrow[resp])       # Output | F p | LOF p | gap | abs. residuals p | order p | Cook (run) | Adequate
        return dict(p=c[1], lof=c[2], gap=c[3], spread=c[4], order=c[5], cook=c[6], ok=c[7])

    def rsm(resp):
        c = _cells(rmrow[resp])       # Output | Scale | Runs | Terms | R² | Adj. R² | Pred. R²
        return dict(scale=c[1], n=int(c[2]), terms=c[3], r2=c[4], adj=c[5], pred=c[6])

    def centre_kw(design, resp):
        cc = cen[(design, OLAB[resp])]
        return dict(replicate_n=int(cc[2]), replicate_mean=cc[3], replicate_sd=cc[4], replicate_cv=_unmark(cc[5]))

    def infl_refs(resp):
        return [ref("influence", row, in_t, inrow) for (o_, _), row in inrow.items() if o_ == RL[resp]]

    q_sel = {HCP: [Q("Pool host cell protein is modelled on the log scale on all"),
                   Q("Its Box-Cox λ is"),
                   Q("The residual standard deviation on the log scale,")],
             XM: [Q("The XMuLV LRF is modelled on the raw scale on the"),
                  Q("Protein load enters that model through the interaction")],
             MV: [Q("The MVM LRF is modelled on the raw scale with load pH and load conductivity.")]}
    for resp in (HCP, XM, MV):
        a_, m_ = adeq(resp), rsm(resp)
        mod, lof = _cells(anrow[(RL[resp], "Model")]), _cells(anrow[(RL[resp], "Lack of fit")])
        refs = ([ref("selected" if i == 0 else ("logscale" if "λ" in x else "coef"), x)
                 for i, x in enumerate(q_sel[resp])]
                + [ref("selected", rmrow[resp], rm_t, rmrow), ref("selected", adrow[resp], ad_t, adrow),
                   ref("coef", anrow[(RL[resp], "Model")], an_t, anrow),
                   ref("coef", anrow[(RL[resp], "Lack of fit")], an_t, anrow),
                   ref("centre", cenrow[("Response surface", OLAB[resp])], cen_t, cenrow)]
                + [ref("coef", row, co_t, corow) for (o_, _), row in corow.items() if o_ == COLAB[resp]]
                + infl_refs(resp))
        fit_rec(resp, f"selected model (PD-008-02), {m_['scale'].lower()} scale, terms: {m_['terms']}",
                refs, n_runs=m_["n"], r_squared=_num(m_["r2"]), adjusted_r_squared=_num(m_["adj"]),
                predicted_r_squared=_num(m_["pred"]), f_statistic=_num(mod[5]), p_value=_num(mod[6]),
                lack_of_fit_p=_num(lof[6]), rmse=round(float(FIT[HCP]["rmse"]), 3) if resp == HCP else None,
                adequacy_statement=(
                    f"Meets each adequacy criterion of PCMP-001 §7.2: model F-test p {a_['p']}, lack of fit p "
                    f"{a_['lof']}, R² minus predicted R² {a_['gap']}, residual trends p {a_['spread']} (absolute "
                    f"residuals on the predicted values) and {a_['order']} (residuals on the run order), largest Cook's "
                    f"distance {a_['cook']}, below the median of F(p, n − p). Selected by the model selection of INV-002 "
                    f"corrective action CA3; {m_['scale'].lower()} scale"
                    + (", with a block term for the augmentation runs." if resp == HCP else ", on the planned runs.")),
                terms=terms_of(corow, COLAB[resp], {"coef": 2, "se": 3, "t": 4, "p": 5}),
                **centre_kw("Response surface", resp))
    q_none = Q("The selected models of step yield and fragments contain no term besides the block")
    q_noF = Q("These two models have no F-test, so the model F-test criterion does not apply to them")
    for resp in (YLD, FRAG):
        a_, m_ = adeq(resp), rsm(resp)
        fit_rec(resp, f"selected model (PD-008-02), {m_['scale'].lower()} scale, no term besides the intercept and "
                      f"the block",
                [ref("selected", q_none), ref("selected", q_noF), ref("selected", rmrow[resp], rm_t, rmrow),
                 ref("selected", adrow[resp], ad_t, adrow),
                 ref("centre", cenrow[("Response surface", OLAB[resp])], cen_t, cenrow)]
                + [ref("app_c", row, cr2_t, cr2row) for (o_, _), row in cr2row.items() if o_ == OLAB[resp]]
                + infl_refs(resp),
                n_runs=m_["n"], r_squared=_num(m_["r2"]), adjusted_r_squared=_num(m_["adj"]),
                predicted_r_squared=_num(m_["pred"]), lack_of_fit_p=_num(a_["lof"]),
                adequacy_statement=(
                    f"No term besides the intercept and the block: no model F-test applies (the report reads that "
                    f"criterion as not applicable); lack of fit p {a_['lof']}; R² minus predicted R² {a_['gap']}; "
                    f"residuals on the run order p {a_['order']}; largest Cook's distance {a_['cook']}, below the "
                    f"median of F(p, n − p). The output shows no dependence on the parameters within the ranges "
                    f"studied, at the precision of the runs."
                    + (" Step yield is a process performance attribute with no criterion." if resp == YLD else "")),
                terms=terms_of(cr2row, OLAB[resp], {"coef": 2, "se": 3, "t": 4, "p": 5}),
                **centre_kw("Response surface", resp))
    # the screening models: every main effect and every two-factor interaction, used for no prediction
    for resp, row in scrow.items():
        c = _cells(row)                   # Output | R² | Adj. R² | Pred. R² | Model p | Lack of fit p | Terms
        fit_rec(resp, "screening model: every main effect and every two-factor interaction in coded units",
                [ref("screening", row, sc_t, scrow),
                 ref("centre", cenrow[("Screening", OLAB[resp])], cen_t, cenrow)]
                + [ref("app_c", r_, ef_t, efrow) for (o_, _), r_ in efrow.items() if o_ == OLAB[resp]],
                n_runs=int(ns["n_scr"]), r_squared=_num(c[1]), adjusted_r_squared=_num(c[2]),
                predicted_r_squared=_num(c[3]), p_value=_num(c[4]), lack_of_fit_p=_num(c[5]),
                adequacy_statement=(f"Screening model, used to identify effects and for no prediction; model F-test p "
                                    f"{c[4]}, lack of fit p {c[5]}; terms significant at {float(ns['ALPHA']):g} "
                                    f"(effect across the range): {c[6]}."),
                terms=terms_of(efrow, OLAB[resp], {"effect": 2, "coef": 3, "se": 4, "t": 5, "p": 6}),
                **centre_kw("Screening", resp))

    # -- study events --------------------------------------------------------------------------------------
    dev_prose = {
        "DEV-008-01": [("dev1", Q("The first execution of the screening and response-surface designs (study S-AEX-SUP")),
                       ("dev1", Q("The investigation found that the cation exchange eluate had been held for")),
                       ("dev1", Q("Both designs were therefore invalidated and re-executed on the requalified lot")),
                       ("dev1", Q("The data of the first execution are retained and were used only to confirm the cause")),
                       ("dev1", Q("The interaction appeared only on the deamidated load."))],
        "DEV-008-02": [("dev2", Q("In both executions of the designs, the trailing-edge UV set-point")),
                       ("dev2", Q("At `{python} dev_008_02_uv_pool_stop_original_mau` mAU collection therefore ended")),
                       ("dev2", Q("It does not hold their results, and this report does not use them.")),
                       ("dev2", Q("A fixed UV cut can still remove a different share of the trailing tail"))],
        "DEV-008-03": [("dev3", Q("The equilibration and first wash buffer used on one screening run, lot LOT-BUF-8815")),
                       ("dev3", Q("The cause was an error at the titration end point during buffer preparation.")),
                       ("dev3", Q("Each of the `{python} n_scr` screening runs was therefore deleted in turn.")),
                       ("dev3", Q("Every prediction, range and judgement of this report comes from the response-surface"))],
    }
    dev_impact = {
        "DEV-008-01": t("The first execution (study S-AEX-SUP) ran on load lot LOT-CEX-8842, deamidated after a hold of "
                        "`{python} dev_008_01_neutralized_hold_h` h after neutralization, and pool host cell protein "
                        "rose steeply with protein load at high Equil/Wash-1 conductivity. Both designs were invalidated "
                        "under PCP-008 §7 and re-executed in full on the requalified lot LOT-CEX-8851. The data of the "
                        "first execution were used only to confirm the cause; no range, class or clearance claim rests "
                        "on them."),
        "DEV-008-02": t("The trailing-edge UV set-point that ends pool collection was "
                        "`{python} dev_008_02_uv_pool_stop_original_mau` mAU in both executions, against the corrected "
                        "`{python} dev_008_02_uv_pool_stop_corrected_mau` mAU, so collection ended earlier. The set-point "
                        "was the same in every run of the two executions, but a fixed UV cut can remove a different "
                        "share of the trailing tail at different settings and so change an estimated effect; the record "
                        "holds no data on that and does not give the set-point of the augmentation runs. The block term "
                        "detected no shift between the planned and the augmentation runs. The results of the verification "
                        "runs are not in the record and are not used."),
        "DEV-008-03": t("The buffer lot LOT-BUF-8815 had a pH of `{python} dev_008_03_buffer_ph_measured` against its "
                        "acceptance limit of `{python} dev_008_03_buffer_ph_low_limit`. The record does not name the run, "
                        "so each screening run was deleted in turn: the significant terms of pool host cell protein and "
                        "XMuLV did not change, those of MVM, step yield and fragments did for some deletions. The event "
                        "affected the screening design only, which sets no range; every prediction, range and judgement "
                        "comes from the response-surface design."),
    }
    no_impact = {"DEV-008-01": True, "DEV-008-02": False, "DEV-008-03": True}
    devs = []
    for did, row in devrow.items():
        c = _cells(row)
        devs.append(Deviation(
            deviation_id=did, summary=c[1], unit_operation=UO_NAME, detected_during=c[2], disposition=c[3],
            impact_statement=dev_impact[did], no_impact_on_conclusions=no_impact[did],
            source_references=[ref("events", row, rows=devrow, caption=dev_cap, label="tbl-events")]
            + [ref(s_, x) for s_, x in dev_prose[did]],
            metadata=meta()))

    # -- document relationships: the rows of the related-documents table, then the prose ------------------
    rels = []

    def relation(kind, target, statement, sec, quote, table_row=False):
        r_ = (ref(sec, quote, rows=rel, caption=rel_cap, label="tbl-related") if table_row else ref(sec, quote))
        rels.append(DocumentRelationship(
            relationship_id=f"{DOC}-R{len(rels) + 1:02d}", kind=kind, source_document_id=DOC,
            target_document_ref=target, statement=statement, source_references=[r_], metadata=meta()))

    for target, row in rel.items():
        txt = _cells(row)[-1]
        relation(REL_KIND.get(txt, "references"), target, txt, "uo", row, table_row=True)
    relation("executed_under", "PCP-008", "The studies were run under the characterization plan PCP-008.", "exec",
             Q("The studies were run under the characterization plan PCP-008"))
    relation("executed_under", "PCMP-001", "The report states its results against PCP-008 Version 2.0 and the master "
             "plan PCMP-001 Version 2.0.", "basis", Q("This report states its results against PCP-008 Version 2.0"))
    relation("rolls_up_into", "PCMR-001", "The results roll up into the master report PCMR-001, which consolidates the "
             "cumulative viral clearance claim.", "exec", Q("The results roll up into the master report PCMR-001"))
    relation("references", "PTP-001", "The process is being transferred from the development site to the commercial "
             "drug substance site under the Process Transfer Plan PTP-001.", "uo",
             Q("The process is being transferred from the development site in"))
    relation("scoped_by", "RA-001", "RA-001 ranked each parameter on its potential impact and its potential to "
             "interact, and assigned four parameters of the step to the designs and one to a univariate assessment.",
             "risk", Q("The risk assessment RA-001 ranked each parameter"))
    relation("references", "INV-001", "Version 2.0 is issued under INV-001, which found that the acceptance criteria "
             "of Version 1.0 had been set after the data were seen.", "exec",
             Q("INV-001 found that the acceptance criteria of Version 1.0 had been set after the data were seen."))
    relation("references", "INV-002", "Version 2.0 is also issued under INV-002, which applied the model adequacy "
             "criteria of PCMP-001 §7.2 to the response-surface models.", "changes",
             Q("Version 2.0 is also issued under the investigation"))
    relation("references", "PCP-007", "The load is the cation exchange pool, characterized under PCP-007.", "risk",
             Q("The load is the cation exchange pool, whose attributes are set by the preceding step"))
    q_cs_steps = Q("which PCMR-001 consolidates with the claims of low-pH viral inactivation", "virus filtration (PCR-009)")
    relation("references", "PCR-006", "PCMR-001 consolidates the viral clearance claims of the step with those of "
             "low-pH viral inactivation (PCR-006).", "cs", q_cs_steps)
    relation("references", "PCR-009", "PCMR-001 consolidates the viral clearance claims of the step with those of virus "
             "filtration (PCR-009).", "cs", q_cs_steps)
    q_cs_hcp = Q("The upstream criteria of the Protein A pool (PCR-005) and the cation exchange pool (PCR-007)")
    relation("references", "PCR-005", "The Protein A pool criterion for host cell protein (PCR-005) relies on the "
             "verified clearance of the step.", "cs", q_cs_hcp)
    relation("references", "PCR-007", "The cation exchange pool criterion for host cell protein (PCR-007) relies on the "
             "verified clearance of the step.", "cs", q_cs_hcp)

    # -- explicit non-claims, by section --------------------------------------------------------------------
    ncs, nc_at = [], {}

    def nclaim(sec, subject, statement, quotes, rationale=None, elsewhere=None):
        ncs.append(ExplicitNonClaim(
            non_claim_id=f"{DOC}-NC{len(ncs) + 1:02d}", subject=subject, unit_operation=UO_NAME,
            statement=statement, rationale=rationale, handled_elsewhere=elsewhere,
            source_references=[ref(s_, x) for s_, x in quotes], metadata=meta()))
        nc_at.setdefault(sec, []).append(ncs[-1])

    nclaim("platform", "change of fragments across the step", "The expectation that the step leaves fragments at the "
           "level at which they enter it was not tested, because fragments were measured in the pool only.",
           [("platform", Q("This study measured fragments in the pool only, so that expectation was not tested here."))])
    nclaim("risk", "quality of the load", "The study varied the parameters of the step and did not vary the quality of "
           "its load.", [("risk", Q("This study varied the parameters of the anion exchange step and did not vary"))],
           elsewhere="PCP-007")
    nclaim("sdm", "bed pressure", "The pressure across the bed, which PCP-008 §5.1 lists among the compared outputs, "
           "was not measured in the qualification.",
           [("sdm", Q("The pressure across the bed, which PCP-008 §5.1 lists among the compared outputs"))],
           elsewhere="PD-008-04")
    nclaim("sdm", "scale-down offset of residual DNA and leached Protein A", "No offset could be estimated for residual "
           "DNA or leached Protein A, because every pool result was below the LOQ at both scales.",
           [("sdm", Q("It also measured residual DNA and leached Protein A in the pools"))])
    nclaim("sdm", "scale-down offset of fragments and viral clearance", "Fragments and viral clearance were not "
           "compared at the two scales; their offset is unknown, not zero, and they are judged as the scale-down model "
           "gives them.",
           [("sdm", Q("The qualification did not compare fragments or viral clearance at the two scales.")),
            ("sdm", Q("Their offset is unknown, not zero, and they are judged as the scale-down model gives them"))])
    nclaim("sdm", "qualification of the spiking model", "The qualification of the spiking model that PCP-008 §5.1 "
           "required is not in the record.",
           [("sdm", Q("Neither that qualification nor the bed pressure is in the record of this study"))],
           elsewhere="PD-008-04")
    nclaim("operation", "records of execution", "The record does not name the chromatography system, its calibration, "
           "the resin lot, the acceptance of the packed column, or the buffer lot and analyst of each run.",
           [("operation", Q("It does not name the chromatography system on which the studies ran"))],
           elsewhere="PD-008-07")
    nclaim("operation", "comparison of load lots", "The record holds no comparison of load lots.",
           [("operation", Q("The record therefore holds no comparison of load lots"))], elsewhere="PD-008-06")
    nclaim("analytics", "aggregate at this step", "Aggregate was not a response of the designs, because PCMP-001 sets no "
           "aggregate criterion at this step.",
           [("analytics", Q("Aggregate was not a response of the designs"))])
    nclaim("sampling", "viral clearance, residual DNA and leached Protein A in the augmentation runs", "The augmentation "
           "runs measured no viral clearance and no residual DNA or leached Protein A.",
           [("sampling", Q("They measured no viral clearance, because the augmentation design")),
            ("sampling", Q("They measured no residual DNA or leached Protein A either"))], elsewhere="PD-008-08")
    nclaim("sampling", "virus assay controls", "The record holds the LRFs and not the cytotoxicity and interference "
           "controls or the detection limits that PCP-008 §5.4 required.",
           [("sampling", Q("The record of this study holds the LRFs and not those controls"))], elsewhere="PD-008-05")
    nclaim("uni_design", "interaction of flow rate with other parameters", "The univariate assessment cannot resolve an "
           "interaction between flow rate and another parameter.",
           [("uni_design", Q("A univariate assessment cannot resolve an interaction between flow rate")),
            ("disc", Q("The univariate assessment of flow rate cannot detect an interaction"))])
    nclaim("coef", "effect of protein load on XMuLV", "The interaction of load pH and protein load is not established as "
           "an effect of protein load, because the other XMuLV model within 2 AICc units drops it.",
           [("coef", Q("It is therefore not established as an effect of protein load."))])
    nclaim("near", "cause of the difference of the interaction between the designs", "The data do not identify why the "
           "interaction of load pH and Equil/Wash-1 conductivity on the log scale differs between the two designs.",
           [("near", Q("The data do not identify its cause."))])
    nclaim("flow", "flow rate at the lower end for viral clearance, and fragments, DNA and Protein A", "The lower end of "
           "the flow-rate range was not spiked, and fragments, residual DNA and leached Protein A were not measured in "
           "the flow-rate study.",
           [("flow", Q("For viral clearance the evidence is one spiked run at")),
            ("flow", Q("Fragments, residual DNA and leached Protein A were not measured in this study."))])
    nclaim("dna", "movement of residual DNA and leached Protein A with the parameters", "No pool result of residual DNA "
           "or leached Protein A was quantified, so a movement of either with a parameter could not be detected, and a "
           "pool result below the LOQ cannot show the DNA criterion met.",
           [("dna", Q("Because no pool result was quantified, a movement of either attribute")),
            ("dna", Q("so a pool result below the LOQ cannot show that criterion met", "show that criterion met."))])
    nclaim("dna", "confirmation of the leached Protein A platform worst case", "The study cannot confirm the platform "
           "worst case of leached Protein A clearance, and the platform value stands.",
           [("dna", Q("A load that carried less than twice the LOQ cannot confirm that value"))])
    nclaim("mech", "explanation of the split between the conductivities", "The explanation of why each conductivity acts "
           "on one kind of impurity only was not tested.",
           [("mech", Q("One explanation consistent with the data, which this study did not test"))])
    nclaim("mech", "binding of antibody on a deamidated load", "The explanation that antibody bound on the deamidated "
           "load was not tested further, and the data show no loss of yield where the interaction appeared.",
           [("mech", Q("The data therefore show no loss of yield where the interaction appeared"))])
    nclaim("ds", "confirmation of the design space at scale", "The design space is not confirmed at scale at its edges, "
           "and Stage 2 confirms performance inside the NOR only.",
           [("ds", Q("It is not confirmed at scale at its edges, and Stage 2 confirms performance inside the NOR only."))])
    nclaim("par_ranges", "PAR figure for fragments", "No PAR figure is drawn for fragments, whose model has no term.",
           [("par_ranges", Q("No figure is drawn for fragments, whose model has no term"))], elsewhere="PD-008-08")
    nclaim("par_flow", "range of flow rate for fragments, and the lower end for viral clearance", "No range of flow "
           "rate is claimed for fragments, and the effect of a longer residence time at the lower end was not tested.",
           [("par_flow", Q("A longer residence time at the lower end is not expected to lower binding")),
            ("par_flow", Q("Fragments were not measured in the flow-rate study, and no range of flow rate is claimed"))])
    nclaim("verif", "clearance at the edges of the characterized range", "The verification bound covers the NOR only; at "
           "the edges of the characterized range clearance was worse.",
           [("verif", Q("First, it covers the NOR only.")),
            ("verif", Q("At the edges of the characterized range clearance was worse."))])
    nclaim("verif", "host cell protein species the ELISA does not detect", "The record covers neither the clearance of "
           "the host cell protein species the ELISA does not detect nor a test that would find them.",
           [("verif", Q("Nothing in the record covers them, and for that share an excursion would not be detected"))])
    nclaim("cs", "hold limit of the neutralized cation exchange pool", "The study sets no value for the hold of the "
           "neutralized cation exchange pool before anion exchange; the need for such a limit is carried forward to "
           "PCMR-001.", [("cs", Q("This study sets no value for the hold of the neutralized cation exchange pool"))],
           elsewhere="PCMR-001")
    nclaim("cs", "resin life cycle", "Resin packing, sanitization and life cycle are outside this study.",
           [("cs", Q("Resin packing, sanitization and life cycle are controlled under SOP-2008"))], elsewhere="SOP-2008")
    nclaim("concl", "completion of the study as the plan defines it", "The record cannot show that the study is complete "
           "as PCP-008 §7 item 8 defines it, because it cannot show whether the centre run of the flow-rate study was "
           "dispositioned when it was dropped.",
           [("concl", Q("The record therefore cannot show that the study is complete as the plan defines it."))],
           elsewhere="PD-008-03")
    nclaim("record", "deviations", "The report records no deviation: a process characterization study is not GMP "
           "manufacture, so events of execution are study events and departures from the plan are discrepancies from "
           "the plan.",
           [("record", Q("A process characterization study is not GMP manufacture and raises no deviation."))])
    nclaim("dev2", "results of the verification runs of DEV-008-02", "The results of the verification runs named for "
           "DEV-008-02 are not in the record and are not used.",
           [("dev2", Q("It does not hold their results, and this report does not use them."))])
    nclaim("dev2", "pool-collection set-point of the augmentation runs", "The record does not give the pool-collection "
           "set-point of the augmentation runs.",
           [("dev2", Q("The record does not give the set-point of the augmentation runs."))])

    entities = [
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("exec"), process_steps=[step], sites=sites,
                                  equipment=equipment),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("uo"), document_relationships=rels),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cqa"), quality_attributes=attrs),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("analytics"), analytical_methods=methods),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("factors"), parameters=params),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("selected"), model_fits=fits),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("par_basis"), contributions=contributions),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cap"), capabilities=capab),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("record"), deviations=devs),
    ]
    for sec_, items in nc_at.items():
        entities.append(S.SectionEntityExtraction(document_id=DOC, section_id=_sid(sec_), non_claims=items))

    # ==== studies: each on its row of the execution-window table, its prose, its data rows ======================
    fac_names = [NAME[k] for k in FS]
    study_spec = {
        "S-AEX-SDM": dict(study_type="scale_down_qualification",
                          design_name="set-point runs of the scale-down model against manufacturing-scale batches",
                          responses=[HCP, YLD, "column efficiency", "peak asymmetry"],
                          prose=[("sdm", Q("The qualification study S-AEX-SDM")),
                                 ("sdm", Q("It compared step yield, pool host cell protein, column efficiency"))],
                          rows=[("sdm", r_, off_t, offrow) for r_ in offrow.values()]
                          + [("analytics", soprow["SOP-1001"], sop_t, soprow)],
                          pds=["PD-008-04"]),
        "S-AEX-SCR": dict(study_type="screening_doe", design_name="two-level full factorial with centre points",
                          factors=fac_names, responses=RESP5,
                          n_runs=P.doe_runs(UO, "screening"), n_center_points=P.doe_centre_points(UO, "screening"),
                          prose=[("scr_design", Q("The four multivariate parameters were studied in a two-level full")),
                                 ("scr_design", Q("A full factorial in four parameters estimates every main effect"))],
                          rows=[("app_a", r_, mtx["screening"][0], mtx["screening"][1])
                                for r_ in mtx["screening"][1].values()],
                          pds=["PD-008-07", "PD-008-09"]),
        "S-AEX-RSM": dict(study_type="response_surface_doe", design_name="face-centred central composite design",
                          factors=fac_names, responses=RESP5,
                          n_runs=P.doe_runs(UO, "rsm"), n_center_points=P.doe_centre_points(UO, "rsm"),
                          prose=[("rsm_design", Q("The same parameters were studied in a face-centred central composite")),
                                 ("rsm_design", Q("The design adds `{python} n_axial` axial runs at the faces of the cube"))],
                          rows=[("app_b", r_, mtx["rsm"][0], mtx["rsm"][1]) for r_ in mtx["rsm"][1].values()],
                          pds=["PD-008-02", "PD-008-09"]),
        "S-AEX-UNI": dict(study_type="univariate",
                          design_name="one factor at a time, each end of the characterized range in duplicate and one "
                                      "spiked run at the upper end, the other parameters at their set-points",
                          factors=[NAME["flow"]], responses=[HCP, YLD, XM, MV],
                          prose=[("uni_design", Q("Operating flow rate was assessed one factor at a time, with the other")),
                                 ("uni_design", Q("Each end of its characterized range,")),
                                 ("uni_design", Q("One spiked run at the upper end, the shortest residence time"))],
                          rows=[("flow", r_, fl_t, flrow) for r_ in flrow.values()],
                          pds=["PD-008-03"]),
        "S-AEX-AUG": dict(study_type="response_surface_doe",
                          design_name=t("D-optimal augmentation of `{python} n_aug` runs, executed as a second block "
                                        "of the face-centred central composite design"),
                          factors=fac_names, responses=[HCP, YLD, FRAG],
                          prose=[("rsm_design", Q("In `{python} AUG_MONTH` the design was augmented by `{python} n_aug` runs in a",
                                                          "runs in a D-optimal augmentation")),
                                 ("rsm_design", Q("INV-002 decided its rule on"))],
                          rows=[("app_b", r_, mtx["aug"][0], mtx["aug"][1]) for r_ in mtx["aug"][1].values()],
                          pds=["PD-008-01"]),
    }
    studies, unrendered, untyped = [], [], []
    for sid_ in CHRON.index:
        if sid_ not in winrow or not G._present(winrow[sid_], text):
            unrendered.append(sid_)
            continue
        if sid_ not in study_spec:
            untyped.append(sid_)
            continue
        spec = dict(study_spec[sid_])
        prose_, rows_, pds_ = spec.pop("prose"), spec.pop("rows"), spec.pop("pds")
        refs = [ref("factors" if sid_ != "S-AEX-SDM" else "sdm", winrow[sid_], win_t, winrow)]
        refs += [ref(s_, x) for s_, x in prose_]
        refs += [ref(s_, r_, tab_, rr_) for s_, r_, tab_, rr_ in rows_]
        refs += [pdref(p_) for p_ in pds_]
        studies.append(S.StudyDesign(
            study_id=f"study:{sid_}", unit_operation=UO_NAME, scale_down_model=SDM_NAME,
            associated_parameters=[PC[x] for x in spec.get("factors", [])],
            source_references=refs, metadata=meta(), **spec))
    if untyped != ["S-AEX-SUP"]:
        raise ValueError(f"{DOC}: studies with no schema study type: {untyped}; the builder expects only S-AEX-SUP")

    # ==== design space and the proven acceptable ranges =====================================================
    DS = ns["DS"]
    q_ds = [Q("The design space is the region of the four multivariate parameters in which every output"),
            Q("It is drawn on the single-batch limit for pool host cell protein and fragments"),
            Q("On the grid of `{python} DS_N` levels per parameter it covers"),
            Q("MVM clearance excludes"),
            Q("The excluded region lies at low load pH and high load conductivity."),
            Q("The whole NOR lies inside the design space, because every combination")]
    constrained = [f"attr:{resp_attr[r]}" for r in CRIT_OUT if DS["per_response"][r] > 0]
    design_spaces = [S.DesignSpace(
        design_space_id="ds:aex", unit_operation=UO_NAME, parameters=[PC[n] for n in fac_names],
        quality_attributes_constrained=constrained,
        definition=t("The region of the four multivariate parameters (load pH, Equil/Wash-1 conductivity, load "
                     "conductivity and protein load) in which every output with a criterion meets it at once, drawn on "
                     "the single-batch limit (the 95 % prediction interval of a single run) for pool host cell protein "
                     "and fragments and on the mean prediction for viral clearance (PCMP-001 §6.2). On a grid of "
                     "`{python} DS_N` levels per parameter (`{python} f\"{DS['n_points']:,}\"` points) it covers "
                     "`{python} fx(100 * DSF, 1)` % of the characterized region. MVM clearance excludes "
                     "`{python} fx(100 * DS['per_response'][MV], 2)` % of the grid and XMuLV clearance "
                     "`{python} fx(100 * DS['per_response'][XM], 2)` %, and pool host cell protein and fragments exclude "
                     "no grid point. The excluded region lies at low load pH and high load conductivity. The whole NOR "
                     "lies inside the design space, which lies inside the characterized region, the knowledge space of "
                     "the study. Not confirmed at scale at its edges."),
        source_references=[ref("ds", x) for x in q_ds], metadata=meta())]
    if DS["binding"] != MV:
        raise ValueError(f"{DOC}: the design space is no longer bounded by MVM clearance, as the text says")

    iac_ = D.iac_table(UO).set_index("response")

    def basis_of(resp):
        ia = iac_.loc[resp]
        stat = ("the lowest mean prediction over the combinations of NOR low, set-point and NOR high of the other "
                "parameters" if resp in (XM, MV) else
                "the 97.5th percentile of simulated batches with the other parameters drawn within their NORs")
        return (f"Intermediate acceptance criterion {T.crit(ia['iac_low'], ia['iac_high'], ia['spec_type'])} "
                f"({ia['basis']}) of PCMP-001 Version 2.0; NOR-propagated analysis judged on {stat}, on the selected "
                f"response-surface model.")
    q_par_set = Q("Every range in the column headed")
    q_par_nor = Q("Every NOR-propagated range contains its NOR, and all but two span the characterized range.")
    q_par_ph = Q("The NOR-propagated ranges of load pH end at")
    pars = []
    for (lab_, pname), row in parrow.items():
        resp = par_lab[lab_]
        c = _cells(ct["tbl-par"][0].rows()[par_keys.index((lab_, pname))])
        u = UNIT[pkey[pname]]
        u_ = "" if u == "pH" else f" {u}"
        prose_ = [q_par_ph] if (resp in (XM, MV) and pkey[pname] == "load_ph") else []
        pars.append(S.ProvenAcceptableRange(
            par_id=f"{DOC}-PAR{len(pars) + 1:02d}", unit_operation=UO_NAME, quality_attribute=lab_,
            parameter=pname, characterization_range=f"{c[2]}{u_}", par_at_setpoint=f"{c[5]}{u_}",
            par_nor_propagated=f"{c[6]}{u_}", acceptance_basis=basis_of(resp),
            source_references=[ref("par_ranges", row, par_t, parrow)] + [ref("par_ranges", x) for x in prose_],
            metadata=meta()))

    # ==== assertions ======================================================================================
    AS = []

    def add(subj, pred, obj, txt, refs):
        AS.append(EvidenceBackedAssertion(
            assertion_id=f"{DOC}-A{len(AS) + 1:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=txt, source_references=refs, metadata=meta()))

    add(STEP_ID, "step_uses_equipment", SDM_ID,
        f"The studies of {UO_NAME} were executed on a {SDM_NAME}, qualified under SOP-1001, which keeps the bed height, "
        f"the linear flow velocity and the protein load of the commercial step.", [ref("sdm", q_sdm1), ref("sdm", q_sdm2)])
    for name, row in prow.items():
        k = pkey[name]
        add(STEP_ID, "step_has_parameter", PC[name],
            f"{UO_NAME} has process parameter {name}, classified {PRM[k].classification}, studied "
            f"{'in the screening and response-surface designs' if k in FS else 'one factor at a time'}.",
            [ref("factors", row, pt_t, prow)])
    role = {"lrv_mvm": "is assigned the cumulative clearance of {n} by the register",
            "lrv_xmulv": "contributes a modular claim to the cumulative clearance of {n}",
            "hcp": "clears {n}, judged in its pool against the drug substance criterion",
            "residual_dna": "clears {n}, monitored and not modelled",
            "leached_protein_a": "clears {n}, monitored and not modelled",
            "fragments_lmw": "has {n} judged in its pool against the drug substance criterion"}
    for key in ckeys:
        add(STEP_ID, "step_has_quality_attribute", f"attr:{key}", f"{UO_NAME} " + role[key].format(n=names[key]) + ".",
            [ref("cqa", crow[key], cq_t, crow)])
    for amv, ks in METHOD_ATTR.items():
        for key in ks:
            m_ = ms_df.loc[amv]
            add(f"attr:{key}", "attribute_measured_by_method", f"method:{amv}",
                f"{names.get(key, 'Step yield')} is measured in this report by {amv} ({m_['Title']}): "
                f"{lc1(m_['Measured in this report'])}, precision "
                f"{m_['Precision']}, LOQ {m_['LOQ']}.", [ref("app_d", msrow[amv], ms_t, msrow)])
    for key in ikeys:
        ic, cr = _cells(irow[key]), _cells(crrow[key])
        ia = iac_.loc[attr_resp[key]]
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{UO}_{key}_iac",
            f"At the anion exchange step {names[key]} is judged against the Version 2.0 intermediate acceptance "
            f"criterion {_unmark(ic[-2])} {RU[attr_resp[key]] if attr_resp[key] != FRAG else '%'} ({ia['basis']}), "
            f"derived from the drug substance criterion {_unmark(ic[1])} {reg.loc[key, 'unit']}; "
            f"met across the NOR: {_unmark(cr[-1])}.",
            [ref("par_basis", irow[key], iac_t, irow), ref("par_results", crrow[key], cr_t, crrow)])

    # parameter effects: each term of a selected model with terms on its coefficient row (and the screening
    # effect row); no detected effect on the screening effect row of the parameter for that output
    impacts = [("load_ph", HCP, "A"), ("wash1_cond", HCP, "B"), ("load_ph", XM, "A"), ("load_cond", XM, "C"),
               ("load_ph", MV, "A"), ("load_cond", MV, "C")]
    verb = {("load_ph", HCP): "lowers", ("wash1_cond", HCP): "raises", ("load_ph", XM): "raises",
            ("load_cond", XM): "lowers", ("load_ph", MV): "raises", ("load_cond", MV): "lowers"}
    for k, resp, lt in impacts:
        c = _cells(corow[(COLAB[resp], lt)])
        s_ = _cells(efrow[(OLAB[resp], lt)])
        if (float(_num(c[2])) < 0) != (verb[(k, resp)] == "lowers"):
            raise ValueError(f"{DOC}: the sign of {k} on {resp} no longer agrees with the text")
        add(PC[NAME[k]], "parameter_impacts_attribute", f"attr:{resp_attr[resp]}",
            f"{NAME[k]} ({lt}) {verb[(k, resp)]} {SAY[resp]}: coefficient "
            f"{c[2]} per coded unit{' on the natural log scale' if resp == HCP else ' log10'}, p {c[5]} in the selected "
            f"response-surface model; screening effect {s_[2]} {RU[resp]} across the range, p {s_[6]}.",
            [ref("coef", corow[(COLAB[resp], lt)], co_t, corow), ref("app_c", efrow[(OLAB[resp], lt)], ef_t, efrow)])
    no_effect = [("load_cond", HCP), ("load", HCP), ("wash1_cond", XM), ("wash1_cond", MV), ("load", MV),
                 ("load_ph", YLD), ("wash1_cond", YLD), ("load_cond", YLD), ("load", YLD),
                 ("wash1_cond", FRAG), ("load_cond", FRAG)]
    for k, resp in no_effect:
        lt = LET[k]
        s_ = _cells(efrow[(OLAB[resp], lt)])
        if sig_of(s_[6]):
            raise ValueError(f"{DOC}: the screening effect of {k} on {resp} is now significant")
        sel = FIT[resp]["names"]
        if any(k in x.split(":") or x == f"{k}^2" for x in sel):
            raise ValueError(f"{DOC}: the selected model of {resp} now carries {k}")
        add(PC[NAME[k]], "parameter_does_not_significantly_impact_attribute", f"attr:{resp_attr[resp]}",
            f"{NAME[k]} ({lt}) on {SAY[resp]}: screening effect {s_[2]} {RU[resp]} across the range, p {s_[6]}, not "
            f"significant; the selected response-surface model ({lc1(terms_txt(resp))}) carries no term containing it.",
            [ref("app_c", efrow[(OLAB[resp], lt)], ef_t, efrow), ref("selected", rmrow[resp], rm_t, rmrow)])
    q_flow_hcp = Q("At manufacturing scale, pool host cell protein was")
    q_flow_ns = Q("Neither difference is significant at")
    for resp in (HCP, YLD):
        add(PC[NAME["flow"]], "parameter_does_not_significantly_impact_attribute", f"attr:{resp_attr[resp]}",
            t(f"Operating flow rate on {'pool host cell protein' if resp == HCP else 'step yield'}: the difference "
              f"between the two ends of the range ("
              + ("`{python} fx(-FT_HCP['diff'], 1)` ng/mg lower at the upper end, `{python} pe(FT_HCP['p'])`"
                 if resp == HCP else "`{python} fx(FT_YLD['diff'], 1)` percentage points higher at the upper end, "
                                     "`{python} pe(FT_YLD['p'])`")
              + ") is not significant at `{python} f'{ALPHA:g}'` by a two-sided t-test."),
            [ref("flow", q_flow_hcp), ref("flow", q_flow_ns)])

    # ==== report statements, grouped by the chapters of the report =========================================
    STS = []

    def st(sec, txt, refs):
        STS.append((SEC[sec][0], ReportStatement(
            statement_id=f"{DOC}-S{len(STS) + 1:03d}", statement_text=txt, confidence="high",
            review_status="accepted", source_references=refs)))

    def sq(sec, prefix, upto=None, txt=None, extra=()):
        """A statement of one prose span (by its prefix in the .qmd), ``txt`` the statement where it is not the
        span itself, ``extra`` further ``(section, prefix)`` spans it draws on."""
        span = Q(prefix, upto)
        st(sec, t(txt) if txt else clean_(span), [ref(sec, span)] + [ref(s_, Q(x)) for s_, x in extra])

    def srow(sec, txt, row, tab=None, rows_=None, caption=None, label=None):
        st(sec, txt, [ref(sec, row, tab, rows_, caption=caption, label=label)])

    # -- Executive summary -----------------------------------------------------------------------------
    for p_ in ("This report presents the Stage 1 process characterization of the anion exchange step",
               "The register of critical quality attributes assigns to it the cumulative clearance",
               "This Version 2.0 is issued under two QA investigations.",
               "INV-002 found that the response-surface models did not meet",
               "Four parameters (load pH, Equil/Wash-1 conductivity, load conductivity and protein load) were studied",
               "the response-surface design was augmented by `{python} n_aug` runs, a number",
               "The first execution of both designs ran on a deamidated load",
               "A study event is an event during execution that Version 1.0 recorded",
               "Each response-surface output was analysed by the model selection of INV-002 corrective action CA3, and",
               "Pool host cell protein is modelled on the log scale and depends on",
               "The log reduction factors (LRFs) of both viruses depend on load pH and load conductivity",
               "The selected response-surface models of step yield and fragments contain no term, so they show",
               "Every output with a criterion met its intermediate acceptance criterion at every combination",
               "At the least favourable combination the mean XMuLV LRF was",
               "The design space covers `{python} fx(100 * DSF, 1)` % of a grid",
               "MVM clearance bounds the design space where load pH is low",
               "The NOR-propagated range of a parameter is the range over which",
               "For XMuLV and MVM the NOR-propagated range of load pH ends inside the characterized range",
               "The scale-down model is qualified for pool host cell protein, the one compared output",
               "The host cell protein clearance of the step was verified against its platform worst case",
               "A platform worst case is the lowest clearance, or the largest increase",
               "At manufacturing scale, with the offset of the scale-down model at its estimate",
               "It replaced the platform value and widened the host cell protein criteria",
               "The bound does not depend on a single run.",
               "It does depend on the model selection, because the plan's full quadratic model fails",
               "With the offset at the unfavourable end of its 90 % interval it would be",
               "All five parameters were classified as well-controlled critical process parameters (WC-CPP).",
               "In the integrated process model of `{python} f\"{N_MC:,}\"` simulated batches, the cumulative MVM",
               "The record holds three study events from the execution",
               "Three of them are changes to the work, namely",
               "They concern the qualification of the scale-down model, virus assay controls"):
        sq("exec", p_)
    sq("exec", "For pool host cell protein the upper end of the 95 % prediction interval of a single run, a one-sided "
               "97.5 % limit, reached at most `{python} fx(NPL_HCP, 1)` ng/mg against")
    sq("exec", "Every proven acceptable range contains its NOR. The NOR-propagated range of a parameter is",
       "contains its NOR.")

    # -- Introduction ------------------------------------------------------------------------------------
    sq("uo", "A-Mab is a humanized IgG1 monoclonal antibody whose primary mechanism of action", "antibody-dependent cellular cytotoxicity")
    sq("uo", "It is purified on the platform train of Protein A capture")
    sq("uo", "The commercial process runs at a bioreactor scale of")
    sq("uo", "These are residual DNA, the acidic part of the host cell protein population")
    sq("uo", "It clears host cell protein, residual DNA and leached Protein A, which are formed upstream")
    src_all = _source()
    obj_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n## Objectives", 1)[1].split("\n## ", 1)[0], flags=re.M)
    if len(obj_list) != 6:
        raise ValueError(f"{DOC}: {len(obj_list)} numbered objectives under '## Objectives', the text says six")
    for i, obj in enumerate(obj_list, 1):
        first = S_first(obj)
        st("objectives", f"Objective {i} of PCP-008 §2: {clean_(q(obj))}", [ref("objectives", q(first))])
    sq("basis", "The study is part of Stage 1, process design, of the lifecycle approach", "lifecycle approach to process validation")
    sq("basis", "Prior knowledge and risk assessment identify the parameters that may affect")
    sq("basis", "The viral clearance of this step is a modular claim under ICH Q5A(R2)", "modular claim under ICH Q5A(R2)")
    sq("basis", "Each claimed step is studied in its own spiking model")
    sq("changes", "Version 1.0 of this report was approved on")
    sq("changes", "INV-001 found that the criteria used to judge each step in the proven acceptable range analysis")
    sq("changes", "Version 1.0 of this report judged pool host cell protein against")
    sq("changes", "That limit was the drug substance limit carried back through the nominal clearance")
    sq("changes", "Version 1.0 judged the two viruses against the cumulative requirement minus")
    sq("changes", "These limits were applied at analysis and appear in no approved plan.")
    sq("changes", "Version 2.0 judges the step against the intermediate acceptance criteria that PCMP-001 Version 2.0")
    sq("changes", "The host cell protein criterion of Version 2.0 is wider than the Version 1.0 limit")
    sq("changes", "Fragments are judged at this step for the first time, by nrCE-SDS")
    sq("changes", "The proven acceptable ranges moved with the criteria.")
    sq("changes", "Against the Version 1.0 limit, as Version 1.0 computed it")
    sq("changes", "Against the Version 2.0 criterion every range for pool host cell protein spans")
    sq("changes", "Against the stricter viral clearance criteria the NOR-propagated ranges of load pH end at")
    sq("changes", "Under INV-002 the response-surface design was augmented, and every output is analysed by model")
    sq("changes", "The scale-down model is now qualified for each output by its offset from manufacturing scale")
    sq("changes", "The host cell protein clearance of the step is verified against its platform worst case, and that")
    sq("changes", "The record separates the study events of the execution from the discrepancies from the plan")
    sq("changes", "The execution window of every study is given")
    sq("changes", "No NOR or set-point of this step changed at Version 2.0.")

    # -- Prior knowledge and quality risk basis ----------------------------------------------------------
    sq("platform", "The platform anion exchange step has been used to manufacture three earlier humanized IgG1", "to supply A-Mab clinical studies")
    sq("platform", "It also gave the two platform worst cases of this step on which the criteria of the upstream steps")
    sq("platform", "The platform claims of the step are")
    sq("platform", "Load pH is therefore expected to lower pool host cell protein and to raise both LRFs.")
    sq("platform", "Step yield is therefore not expected to depend on load pH within the range studied.")
    sq("platform", "Equil/Wash-1 conductivity is therefore expected to raise pool host cell protein")
    sq("platform", "For this reason PCP-008 §4.1 expected the effect of Equil/Wash-1 conductivity on host cell protein")
    sq("platform", "Within the range studied the impurity mass is expected to stay below that capacity")
    sq("platform", "They are the species most likely to show an effect of flow rate")
    sq("platform", "Its clearance is expected to be large and robust to the parameters.")
    sq("platform", "On the platform no step after cation exchange changes the fragment level")
    sq("platform", "For both model viruses, clearance is expected to fall as the load pH drops")
    sq("platform", "MVM is not inactivated by low pH, so this step and the virus filter carry the whole MVM claim")
    sq("cqa", "All `{python} len(cqa_reg)` attributes of the register are critical quality attributes")
    sq("cqa", "An effect on host cell protein or on fragments is therefore an effect on a critical quality attribute")
    sq("cqa", "This step contributes one of three claims for XMuLV and one of two for MVM.")
    sq("cqa", "Step yield is a process performance attribute and carries no criterion.")
    for key, row in crow.items():
        c = _cells(row)
        srow("cqa", f"{names[key]}: role at the step {ffill([_cells(r)[0] for r in crow.values()])[ckeys.index(key)].lower()}, "
                    f"drug substance criterion {_unmark(c[3])}, criticality {c[4]}, Tool #1 score {c[5]}.", row, cq_t, crow)
    sq("risk", "Parameters ranked high on both were assigned to the designed studies")
    sq("risk", "Load pH, Equil/Wash-1 conductivity and load conductivity ranked highest")
    sq("risk", "Protein load was included because the impurity mass loaded onto the column scales with it")
    sq("risk", "Host cell proteins and DNA are expected to bind fast relative to the residence time")

    # -- Materials and methods --------------------------------------------------------------------------
    sq("sdm", "Scaling on these variables holds the residence time and the impurity mass per unit of ligand")
    sq("sdm", "It ended before the first execution of the designs began on")
    sq("sdm", "The offset of an output is the mean of the scale-down runs minus the mean of the manufacturing batches")
    sq("sdm", "Its offset is therefore the ratio of the geometric means, and a scale-down value is divided by it.")
    sq("sdm", "The model is qualified for an output when the conclusion against its criterion over the NOR is the same")
    sq("sdm", "Pool host cell protein, the only compared output with a criterion at this step, has a ratio of")
    sq("sdm", "Its criterion is met over the NOR with the offset at its estimate and at both ends of the interval")
    sq("sdm", "The scale-down column gave fewer plates per metre than the manufacturing columns, and the 90 %")
    sq("sdm", "No conclusion of this report depends on column efficiency.")
    sq("sdm", "For viral clearance it rests on the spiking model.")
    sq("sdm", "The centre points of each design were separate runs of the step.")
    for k_, row in offrow.items():
        c = _cells(row)
        srow("sdm", f"Scale-down offset of {c[0]} (scale-down minus manufacturing scale): estimate {_unmark(c[-4])}, 90 % "
                    f"confidence interval {_unmark(c[-3])}; met over the NOR (low/est./high): {_unmark(c[-2])}; "
                    f"qualified: {_unmark(c[-1])}.", row, off_t, offrow)
    sq("operation", "The step was operated as at commercial scale, under SOP-2011.")
    sq("operation", "PCP-008 §5.2 requires the resin, the buffers and the column packing to meet platform specification")
    sq("operation", "The record does not show that they did.")
    sq("operation", "The re-executed screening and response-surface designs ran on one requalified load lot")
    sq("operation", "The record does not name the load lot of the qualification study")
    sq("operation", "Lot LOT-CEX-8851 had expired on")
    sq("operation", "The block term of the models estimates a shift between the planned runs and the augmentation runs")
    sq("analytics", "The re-executed designs ran after that date and measured fragments by nrCE-SDS")
    sq("analytics", "The precision of each method bounds the smallest effect the study can resolve")
    sq("analytics", "The repeatability of the infectivity assays is")
    st("analytics", "Size-variant methods by design: " + "; ".join(clean_(r_) for r_ in mbsrow.values()) + ".",
       [ref("analytics", r_, mbs_t, mbsrow) for r_ in mbsrow.values()])
    sq("sampling", "The flow-through pool of every run was sampled, and the pool sample carries the responses.")
    sq("sampling", "The load results in the record are residual DNA and leached Protein A on the")
    sq("sampling", "The record does not show that load and pool samples were retained frozen")
    sq("sampling", "Residual DNA and leached Protein A were measured in the load and the pool of every planned")
    sq("sampling", "The augmentation runs measured pool host cell protein, step yield and fragments.")
    sq("sampling", "Each LRF is the log10 ratio of the total infectivity in the spiked load", "(PCP-008 §5.4)")
    sq("coding", "Each multivariate parameter was coded so that the ends of its characterized range are")
    sq("coding", "For load pH, Equil/Wash-1 conductivity and load conductivity the middle of the range is the set-point.")
    sq("coding", "For protein load the middle is")
    sq("coding", "PCP-008 §5.5 placed the set-point at 0, and for protein load the design was laid out")
    sq("coding", "The screening data were fitted by ordinary least squares")
    sq("coding", "An effect is twice the coded coefficient, which is the change in the response")
    sq("coding", "The screening model identifies effects.")
    sq("coding", "It is not the predictive model, and no range is derived from it.")
    sq("selection", "PCP-008 planned the full quadratic model in the four multivariate parameters.")
    sq("selection", "chooses the log scale where its 95 % interval for λ contains 0")
    sq("selection", "Among all hierarchical submodels of the full quadratic, the one with the lowest AICc is selected.")
    sq("selection", "For four parameters there are")
    sq("selection", "Where the design has a second block, the augmentation runs, a block term is kept")
    sq("selection", "This report counts the terms of a model without the intercept and the block term.")
    sq("selection", "The search is exhaustive.")
    sq("selection", "Across the outputs of the campaign, a backward stepwise search would have stopped")
    sq("selection", "At this step a forward search would have stopped at a worse model for XMuLV")
    sq("selection", "Where other models lie within 2 AICc units of the selected one, the selected model decides")
    sq("selection", "A feature that only some of them carry is not treated as an established effect.")
    sq("logscale", "Pool host cell protein is the one output modelled on the log scale.")
    sq("logscale", "A purification step removes a share of what is present")
    sq("logscale", "With the selected terms fitted on the raw scale, the residual standard deviation is")
    sq("logscale", "On the log scale the two halves give")
    sq("logscale", "The criterion stays in its own unit, ng/mg, and the effects are fold changes.")
    sq("logscale", "At the least favourable combination within the NOR the predicted value is")
    sq("logscale", "The predicted value is the median of the output, its geometric mean")
    sq("logscale", "The upper prediction limit, which decides against an upper criterion, is not affected by that.")
    adq_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n### Model adequacy", 1)[1].split("\n### ", 1)[0], flags=re.M)
    if len(adq_list) != 4:
        raise ValueError(f"{DOC}: {len(adq_list)} numbered adequacy criteria, the text says four")
    for i, a_ in enumerate(adq_list, 1):
        st("adequacy", f"Adequacy criterion {i} of PCMP-001 §7.2: {clean_(q(a_))}", [ref("adequacy", q(a_))])
    sq("adequacy", "PCMP-001 §7.2 does not say how the model F-test criterion applies to a model with no term.")
    sq("adequacy", "Such a model has no F-test, and this report reads that criterion as not applicable to it.")
    sq("adequacy", "The absolute residuals were regressed on the predicted values, and the residuals on the order")
    sq("adequacy", "A run with a Cook's distance above")
    sq("adequacy", "The model fails the criterion only where a run's Cook's distance exceeds the median")
    sq("judgement", "A quality attribute is judged on a single batch, because its criterion applies to each batch.")
    sq("judgement", "The interval is two-sided, so its upper end is a one-sided 97.5 % limit.")
    sq("judgement", "A quality attribute meets its criterion over the NOR when every interval lies within it")
    sq("judgement", "Viral clearance is judged on the mean predicted LRF at the least favourable of the")
    sq("judgement", "Pool host cell protein is divided by its offset before it is judged.")
    sq("par_method", "Two analyses were run for each pair of a parameter and an attribute with a criterion")
    sq("par_method", "The first, in the column headed")
    sq("par_method", "The second, the NOR-propagated analysis, scans the parameter over")
    sq("par_method", "For a quality attribute, each other parameter is drawn")
    sq("par_method", "For viral clearance the other parameters are set to each of their")
    sq("par_method", "A range is reported only where it is contiguous and contains the set-point")
    sq("par_method", "The NOR-propagated range is the one that supports a claim.")
    sq("par_method", "A grid point lies inside when the 95 % prediction interval of a single run lies within the criterion")
    sq("cap_method", "The model runs `{python} f\"{N_MC:,}\"` simulated batches through every step")
    sq("cap_method", "PCP-008 §7 sets no numerical threshold for an effect of flow rate")
    sq("cap_method", "An effect of flow rate on pool host cell protein or step yield was tested by a two-sided t-test")
    sq("cap_method", "An apparent effect on an LRF no larger than the repeatability of its infectivity assay")
    sq("cap_method", "They are the models within 2 AICc units of each selected model")

    # -- Study design ------------------------------------------------------------------------------------
    sq("factors", "The augmentation was made during the Version 2.0 re-analysis, after Version 1.0 of this report")
    for sid_, row in winrow.items():
        c = _cells(row)
        srow("factors", f"Study {sid_} ({c[2]}): executed {c[3]} to {c[4]}.", row, win_t, winrow)
    sq("factors", "The characterized range is wider than the NOR at both ends for every parameter.")
    sq("factors", "The edge of the operating region therefore lies inside the data", "claimed only over settings that were run")
    sq("factors", "The load pH range lies below the pH at which a fraction of the antibody would begin to bind")
    sq("factors", "For protein load that is")
    for name, row in prow.items():
        c = _cells(row)
        srow("factors", f"{name}: set-point {c[4]} {c[3]}, NOR {c[5]}, characterized range {c[6]}; "
                        f"{'code ' + c[1] + ', designed experiments' if c[1] != '–' else 'one factor at a time'}.",
             row, pt_t, prow)
    sq("scr_design", "The centre points estimate pure error and give a test for curvature.")
    sq("scr_design", "The runs were executed in randomized order on load lot LOT-CEX-8851")
    sq("rsm_design", "Its quadratic terms allow for clearance that rises more steeply")
    sq("rsm_design", "It calculated the number of runs as the smallest augmentation")
    sq("rsm_design", "The plan did not foresee the augmentation, and it is recorded as the discrepancy")
    sq("uni_design", "PCP-008 §6.4 planned the low, the centre and the high setting.")
    sq("uni_design", "No run was made at the centre, and the qualification runs at set-point serve as the reference")
    sq("uni_design", "Its claims therefore rest on the assumption that the effect of flow rate does not depend")

    # -- Results -------------------------------------------------------------------------------------------
    sq("centre", "Pool host cell protein is the least precise output in relative terms.")
    sq("centre", "Its coefficient of variation in the response-surface design is")
    sq("centre", "The standard deviations of the LRFs at the centre point")
    for (des, lab_), row in cenrow.items():
        c = _cells(row)
        cv_ = (f"CV {c[5]} %" if _num(c[5]) is not None else "CV not given for a log reduction factor")
        srow("centre", f"{des} centre points, {lab_}: {c[2]} runs, mean {c[3]}, SD {c[4]}, {cv_}.", row,
             cen_t, cenrow)
    sq("screening", "Load pH and Equil/Wash-1 conductivity acted on pool host cell protein in opposite directions")
    sq("screening", "Load pH raised both LRFs and load conductivity lowered them.")
    sq("screening", "No term was significant for step yield.")
    sq("screening", "For fragments the interaction of load pH and protein load was significant")
    sq("screening", "The directions agree with the expectations of")
    sq("screening", "No effect of load conductivity on host cell protein and no effect of Equil/Wash-1 conductivity")
    sq("screening", "The screening models of")
    sq("screening", "This type of design identifies effects but cannot fit curvature")
    sq("selected", "Every selected model meets each criterion that applies to it.")
    sq("selected", "The residual regressions found no trend for any output.")
    sq("selected", "Cook's distance flagged at least one run in every model except that of MVM")
    sq("coef", "On the log scale the effects on pool host cell protein are fold changes.")
    sq("coef", "From the low to the high end of its range, load pH multiplies pool host cell protein by")
    sq("coef", "The two coefficients,")
    sq("coef", "The block term is `{python} fx(bBlk, 3)` on the log scale")
    sq("coef", "Across its range, load pH raises the XMuLV LRF by")
    sq("coef", "Load conductivity lowers them by")
    sq("coef", "For each virus the effects of load pH and load conductivity are equal in size")
    sq("coef", "The interaction of load pH and protein load makes the effect of protein load on the XMuLV LRF depend")
    sq("coef", "From the lowest to the highest protein load, the model lowers the XMuLV LRF by")
    sq("coef", "The interaction is significant")
    sq("coef", "Both changes are of the size of the repeatability of the XMuLV assay")
    sq("reeval", "On the planned runs the full quadratic model of pool host cell protein failed the limit on overfitting")
    sq("reeval", "Once models are selected, pool host cell protein did not need the augmentation to pass PCMP-001 §7.2.")
    sq("reeval", "The model selected on the `{python} n_rsm` planned runs alone has the same scale and terms")
    sq("reeval", "On the planned runs alone it also meets the criterion over the NOR")
    sq("reeval", "A model selected on the same runs it is judged on passes an optimistic check")
    sq("reeval", "The model selected on the planned runs predicted")
    sq("reeval", "Step yield is the one output whose model the augmentation changed.")
    sq("reeval", "On the planned runs alone its selected model, in")
    sq("reeval", "On all runs the selected model contains no term and meets each criterion that applies to it.")
    for (lab_, da), row in nerow.items():
        c = _cells(row)
        r_ = lab_resp[lab_]
        stat = (f"upper end of the 95 % prediction interval {c[3]}" if c[3] != "n.a." else f"lowest mean {c[4]}")
        srow("near", f"{lab_}: model within 2 AICc units (ΔAICc {da}) with {c[2].lower() if c[2] != 'None' else 'no term'}; "
                     f"{stat}; met over the NOR: {c[5]}" + ("; the selected model." if float(da) == 0 else "."),
             row, ne_t, nerow)
        _ = r_
    sq("near", "All contain load pH and Equil/Wash-1 conductivity.")
    sq("near", "None contains the interaction of protein load and Equil/Wash-1 conductivity")
    sq("near", "For XMuLV the other model drops protein load and its interaction with load pH.")
    sq("near", "For MVM the two other models add an interaction of load pH and load conductivity")
    sq("near", "Under every model within 2 AICc units each output meets its criterion over the NOR")
    sq("near", "The lower edge of the NOR-propagated range of load pH lies between")
    sq("near", "The share of the grid inside the design space lies between")
    sq("near", "For pool host cell protein and fragments the upper end of the 95 % prediction interval of a single run "
               "stays below the criterion everywhere")
    sq("near", "The interaction of load pH and Equil/Wash-1 conductivity on pool host cell protein, which PCP-008 expected")
    sq("near", "On the log scale it stays significant in the screening data")
    sq("near", "The difference between the two log-scale estimates is significant")
    sq("near", "The response-surface model, fitted on")
    sq("influence", "No run exceeded the median of the F distribution, so every model meets the fourth criterion")
    for (lab_, run), row in inrow.items():
        c = _cells(row)
        srow("influence", f"{lab_}, run {run}: Cook's distance {c[2]} (flag {c[3]}, failure {c[4]}); model selected "
                          f"without the run: {c[5]}; met over the NOR: {_unmark(c[6])}.", row, in_t, inrow)
    sq("influence", "Deleting a flagged run left every judgement over the NOR unchanged")
    sq("influence", "Deletion changed the selected model in")
    sq("influence", "With run `{python} int(DEL_X6[\"run\"])` deleted, the XMuLV model moves to the log scale")
    sq("influence", "The lower edge of the NOR-propagated range of load pH for XMuLV then moves from")
    sq("influence", "The selected terms of these")
    sq("surfaces", "Pool host cell protein falls with load pH, rises with Equil/Wash-1 conductivity")
    sq("surfaces", "Both LRFs rise with load pH, fall with load conductivity")
    sq("surfaces", "The selected models of pool host cell protein and MVM contain no interaction")
    for lab_ in ("fig-contours-wash", "fig-contours-cond", "fig-diag-hcp", "fig-diag-xmulv", "fig-diag-mvm"):
        st("surfaces", f"Figure caption: {fig_cap(lab_)}", [ref("surfaces", fig_cap(lab_), label=lab_)])
    sq("flow", "Step yield was `{python} fx(FT_YLD[\"diff\"], 1)` percentage points higher")
    sq("flow", "With `{python} n_flow_rep` runs at each end the comparison has")
    sq("flow", "Every result met the host cell protein criterion, the highest at")
    sq("flow", "The spiked run at the upper end, the shortest residence time in the range, gave")
    sq("flow", "Both lie inside the 95 % prediction interval of a single run at the set-point")
    sq("flow", "For pool host cell protein and step yield the data show no effect of flow rate")
    for (set_, run), row in flrow.items():
        c = _cells(row)
        srow("flow", f"Flow-rate study, {_unmark(set_).lower()}, run {run}: pool host cell protein {c[3]} ng/mg, step "
                     f"yield {c[4]} %, XMuLV LRF {c[5]}, MVM LRF {c[6]}.", row, fl_t, flrow)
    sq("dna", "Every pool result of both attributes was below its LOQ")
    sq("dna", "The loads carried")
    sq("dna", "The clearance factor of each run is therefore more than its load divided by the LOQ.")
    sq("dna", "These lower bounds are set by the assays, not by the step.")
    sq("dna", "For residual DNA, the LOQ of the qPCR")
    sq("dna", "It is set far below the limit of 10 ng per dose that the WHO recommends", "that the WHO recommends")
    sq("dna", "The integrated process model assumes an anion exchange DNA log reduction of")
    sq("dna", "This study shows more than")
    sq("dna", "For leached Protein A, the Protein A criterion relies on a platform worst case of")
    for key, row in dnarow.items():
        c = _cells(row)
        srow("dna", f"{c[0]}: load {c[1]} over the runs; pool {c[2]}; LOQ {c[3]}; clearance factor at least {c[4]}; "
                    f"clearance relied on elsewhere: {c[5]}.", row, dna_t, dnarow)
    sq("mech", "Load pH and Equil/Wash-1 conductivity act on pool host cell protein, and load pH and load conductivity")
    sq("mech", "A higher load pH lies above the isoelectric point of more of the host cell proteins")
    sq("mech", "A higher Equil/Wash-1 conductivity shields the charge of the weakly bound host cell proteins")
    sq("mech", "The log scale of the host cell protein model is the form a purification step gives.")
    sq("mech", "Each parameter changes the share of host cell protein that passes")
    sq("mech", "In ng/mg, Equil/Wash-1 conductivity raises pool host cell protein more at the low end of load pH")
    sq("mech", "Two results do not follow the expectations of")
    sq("mech", "The mechanism expected each conductivity to act on both kinds of impurity")
    sq("mech", "Protein load had no detected effect on pool host cell protein")
    sq("mech", "The selected model of step yield contains no term, as expected for a step")
    sq("mech", "The invalidated first execution shows how the step responds to a load that is not representative.")
    sq("mech", "PCP-008 §12 expected that a load with more acidic variants carries antibody")
    sq("mech", "In the invalidated execution the runs at high protein load and high Equil/Wash-1 conductivity gave")
    sq("mech", "No term of either model of step yield was significant in that execution")

    # -- Design space --------------------------------------------------------------------------------------
    sq("ds", "With every output on its mean prediction, which serves as a comparison only")
    sq("ds", "On the mean prediction at the lowest load pH studied")
    sq("ds", "At the same load pH and the highest protein load studied")
    sq("ds", "The design space in turn lies inside the characterized region")
    sq("ds", "Within the NOR a single run can still fall below a viral claim.")
    sq("ds", "At the least favourable combination the lower end of the 95 % prediction interval of a single run is")
    sq("ds", "The design space is a model of the scale-down data.")
    sq("ds", "Movement within the design space is not a change under ICH Q8(R2)", "change under ICH Q8(R2)")

    # -- Proven acceptable ranges --------------------------------------------------------------------------
    sq("par_basis", "Each output is judged against its intermediate acceptance criterion, derived in PCMP-001 §7.3")
    sq("par_basis", "No step after anion exchange changes host cell protein or fragments on the platform")
    sq("par_basis", "For the two viruses the step is held to its platform claim")
    sq("par_basis", "A shortfall of this step therefore cannot be made up by another step.")
    sq("par_basis", "The derivation uses no data of these studies")
    for key, row in irow.items():
        c = _cells(row)
        srow("par_basis", f"Intermediate acceptance criterion of the step for {names[key]}: {_unmark(c[-2])}, basis "
                          f"{_unmark(c[-1]).lower()}, from the drug substance criterion {_unmark(c[1])}.",
             row, iac_t, irow)
    sq("par_results", "That of fragments reached at most")
    sq("par_results", "The mean LRF at the least favourable combination was")
    sq("par_results", "For both viruses that combination has load pH at its NOR low")
    sq("par_results", "Equil/Wash-1 conductivity enters neither model, and protein load does not enter the MVM model.")
    sq("par_results", "For pool host cell protein the upper end of the 95 % prediction interval of a single run, a "
                      "one-sided 97.5 % limit, reached at most `{python} fx(NPL_HCP, 1)` ng/mg, which leaves")
    for key, row in crrow.items():
        c = _cells(row)
        srow("par_results", f"{names[key]} against its criterion {c[1]} over the NOR: mean predicted at the set-point "
                            f"{_unmark(c[2])}, range over the NOR {_unmark(c[3])}, 95 % limits of a single run over the "
                            f"NOR {_unmark(c[4])}; met across the NOR: {c[5]}.", row, cr_t, crrow)
    st("par_ranges", clean_(q_par_set), [ref("par_ranges", q_par_set)])
    st("par_ranges", clean_(q_par_nor), [ref("par_ranges", q_par_nor)])
    st("par_ranges", clean_(q_par_ph), [ref("par_ranges", q_par_ph)])
    sq("par_ranges", "The table rounds these edges inward, so it prints them as")
    sq("par_ranges", "Their lower edges lie `{python} MARG_TXT` below the lower end of the NOR")
    sq("par_ranges", "Every other multivariate parameter carries its characterized range.")
    sq("par_ranges", "For pool host cell protein the plotted parameter is Equil/Wash-1 conductivity")
    sq("par_ranges", "The effect of load pH on pool host cell protein and that of load conductivity on each virus")
    sq("par_ranges", "PCP-008 asks for a figure of each range against the parameter that governs it.")
    sq("par_ranges", "The MVM figure is drawn against load pH, while the coefficient of load conductivity")
    for lab_ in ("fig-par-hcp", "fig-par-xmulv", "fig-par-mvm"):
        st("par_ranges", f"Figure caption: {fig_cap(lab_)}", [ref("par_ranges", fig_cap(lab_), label=lab_)])
    sq("par_flow", "The proven acceptable range of operating flow rate rests on the univariate study")
    sq("par_flow", "For viral clearance, the spiked run at")
    sq("verif", "The host cell protein criteria of the Protein A pool and the cation exchange pool assume")
    sq("verif", "This report verifies that assumption by the rule of PCMP-001 §7.5")
    sq("verif", "The clearance factor is the host cell protein of the load divided by the predicted pool value")
    sq("verif", "That value is the scale-down prediction divided by the offset of the scale-down model at its estimate")
    sq("verif", "The load is taken as the cation exchange pool of the process model at set-point")
    sq("verif", "The factor is evaluated at every combination of NOR low, set-point and NOR high, with the NOR")
    sq("verif", "The criteria in force were derived from these runs.")
    for key, row in verrow.items():
        c = _cells(row)
        if key == "hcp":
            srow("verif", f"Platform worst case of anion exchange for host cell protein ({c[2].lower()}): platform "
                          f"{c[3]}; this campaign at the edges {c[4]}, within the NOR {c[5]}, 95 % bound {c[6]}; "
                          f"outcome {_unmark(c[7]).lower()}.", row, ver_t, verrow)
        else:
            srow("verif", f"Platform worst case of anion exchange for leached Protein A: platform {c[3]}; "
                          f"{_unmark(c[4])} in this campaign.", row, ver_t, verrow)
    sq("verif", "On this model of the planned runs the lowest predicted clearance factor within the NOR is")
    sq("verif", "The model of all `{python} n_all` runs, which")
    sq("verif", "The one-sided 95 % prediction bound of a single batch at the least favourable combination is")
    sq("verif", "The model behind it meets the first three adequacy criteria of PCMP-001 §7.2")
    sq("verif", "By the widening rule of the master plan (PCMP-001 §7.5) the bound replaced the platform value.")
    sq("verif", "The Protein A pool criterion widened from")
    sq("verif", "On all `{python} n_all` runs the bound would be")
    sq("verif", "The bound rests on a model that meets all four adequacy criteria")
    sq("verif", "Run `{python} EDGE_RUN`, at the low end of load pH")
    sq("verif", "Screening run `{python} SCR_EDGE_RUN` gave a lower factor still")
    sq("verif", "Second, the bound depends on the model selection.")
    sq("verif", "The plan's full quadratic model of the planned runs gives a bound of")
    sq("verif", "The two upstream criteria would then have stayed at")
    sq("verif", "Third, the bound is sensitive to the offset of the scale-down model.")
    sq("verif", "At the unfavourable end of its 90 % interval,")
    sq("verif", "In the model of the planned runs, runs")
    sq("verif", "Deleting each of the `{python} n_rsm` runs in turn gives bounds from")
    sq("verif", "Every one is better than the platform value on a model that meets the first three criteria")
    for i_, row in bdrow.items():
        c = _cells(row)
        srow("verif", f"Host cell protein clearance bound of anion exchange, {c[0][0].lower() + c[0][1:]}: {c[1]} runs, "
                      f"{c[2]}-fold; better than the platform value: {c[3]}; model meets criteria 1 to 3: {c[4]}.",
             row, bd_t, bdrow)
    risk_list = re.findall(r"^\d+\. (.+)$", src_all.split("The widening is argued by its risk", 1)[1].split("\n# ", 1)[0],
                           flags=re.M)
    if len(risk_list) != 4:
        raise ValueError(f"{DOC}: {len(risk_list)} parts of the risk argument, the text says four")
    for i, it in enumerate(risk_list, 1):
        first = S_first(it)
        st("verif", f"Risk argument of the widening, part {i} of PCMP-001 §7.5: {clean_(q(it))}", [ref("verif", q(first))])

    # -- Process capability and robustness -----------------------------------------------------------------------
    sq("cap", "Capability at commercial scale comes from the integrated process model of")
    sq("cap", "Each Cpk is set against the target of")
    sq("cap", "Both are cumulative over several steps, and this step contributes one claim to each.")
    sq("cap", "No simulated batch fell outside any criterion of the table.")
    sq("cap", "The normal tail probability is")
    sq("cap", "Two of the Cpk values describe assumptions more than this step.")
    sq("cap", "The capability of residual DNA therefore rests on that model input, which this study does not confirm.")
    sq("cap", "Residual DNA has no intermediate acceptance criterion, because the platform history gives no")
    sq("cap", "It is judged instead on the pools of this step, all below the LOQ of")
    sq("cap", "The simulation varies each parameter within its NOR and carries no source of commercial variability")

    # -- Parameter classification -------------------------------------------------------------------------------
    sq("class", "Parameters were classified under SOP-4001 by the decision logic of the A-Mab case study", "as PCMP-001 §7.7 states it")
    sq("class", "It is well controlled (WC-CPP) when its risk of falling outside its acceptable range is low")
    sq("class", "Every attribute of the register is a critical quality attribute (PCMP-001 §3), so an effect")
    sq("class", "An attribute is affected by a parameter when a term that contains the parameter is significant at")
    sq("class", "No plan sets a threshold for practical relevance, so where it decides a class this report names")
    sq("class", "No numerical threshold exists either for how far inside its acceptable range a parameter must be held")
    sq("class", "All five parameters were classified as WC-CPP.")
    sq("class", "The other XMuLV model within 2 AICc units drops the interaction, so the interaction is not established")
    sq("class", "By the rule of PCMP-001 §7.7 alone, a parameter with no demonstrated effect")
    sq("class", "The claims of this step were demonstrated only inside the flow-rate range studied")

    # -- Contribution to the control strategy -------------------------------------------------------------------
    sq("cs", "This step contributes the following to the control strategy of the drug substance")
    cs_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n# Contribution to the control strategy", 1)[1]
                         .split("\n# ", 1)[0], flags=re.M)
    if len(cs_list) != 7:
        raise ValueError(f"{DOC}: {len(cs_list)} items of the control strategy, the report has seven")
    cs_first = {2: q_cs_v, 3: q_cs_hcp}
    for i, it in enumerate(cs_list, 1):
        span = cs_first.get(i) or q(S_first(it))
        st("cs", f"Control strategy item {i}: {clean_(q(it))}", [ref("cs", span)])

    # -- Discussion -----------------------------------------------------------------------------------------------
    for p_ in ("The step behaves as a charge-based flow-through polish.",
               "Within the NOR every output meets its criterion.",
               "The viral clearance claims have the smallest margins,",
               "The design space ends where those two settings meet, outside the NOR.",
               "Confidence in the scale-down model is greatest for pool host cell protein",
               "Fragments lie far below their criterion, but the expectation that the step leaves",
               
               "In every run of the two executions of the designs the pool-collection set-point",
               "The verification of the host cell protein clearance widened the criteria of two upstream steps.",
               "It does depend on the model selection, and it is sensitive to the scale-down offset",
               "For the host cell protein species the ELISA detects, the risk of the widening is the producer's",
               "The augmentation of `{python} PD_AUG` was decided before any new run",
               "For pool host cell protein and fragments the planned runs alone give the same models",
               "The screening results it could affect are those of MVM, step yield and fragments",
               "Four limitations remain.",
               "The residual DNA clearance of the step cannot be shown by an assay",
               "The studies assumed that the resin performs within its qualified life cycle"):
        sq("disc", p_)
    sq("disc", "The viral clearance results are those of a small-scale spiking study", "small-scale spiking study")

    # -- Conclusions (the numbered list of the .qmd) and the completion rule ---------------------------------------
    con_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n# Conclusions", 1)[1].split("\n# ", 1)[0], flags=re.M)
    if len(con_list) != 8:
        raise ValueError(f"{DOC}: {len(con_list)} numbered conclusions, the report has eight")
    for i, con in enumerate(con_list, 1):
        first = S_first(con)
        st("concl", f"Conclusion {i}: {clean_(q(con))}", [ref("concl", q(first))])
    sq("concl", "PCP-008 §7 item 8 judges the study complete when five conditions hold.")
    sq("concl", "The first condition is met")
    sq("concl", "The third is met, because every selected model is adequate")
    sq("concl", "For the second, every run of the designs was executed")
    sq("concl", "The record gives the qualification runs at set-point as its replacement")

    # -- Study events and discrepancies from the plan -------------------------------------------------------------
    sq("record", "This report records what departed from the expected course in two registers.")
    sq("record", "The discrepancies from the plan are every departure from PCP-008 Version 2.0")
    sq("record", "PCP-008 §7 and §9 call a departure from the plan a deviation")
    sq("dev1", "The load lot LOT-CEX-8842 carried")
    sq("dev1", "In that execution pool host cell protein rose steeply with protein load at high Equil/Wash-1")
    sq("dev1", "The screening effect of the interaction of protein load and Equil/Wash-1 conductivity was")
    sq("dev1", "Of the runs at high protein load and high Equil/Wash-1 conductivity,")
    sq("dev1", "The event was detected during the charge-variant verification of the load material")
    sq("dev1", "Under PCP-008 §7, a design executed on material outside the release profile")
    sq("dev1", "The requalified data confirm the cause.")
    sq("dev1", "In the re-executed screening design the same interaction is")
    sq("dev1", "No run of the re-executed designs or of the augmentation exceeded")
    sq("dev1", "The first execution measured fragments by SEC")
    sq("dev1", "PCP-008 §7 sets no numerical limit for the release profile of the load.")
    sq("dev1", "It holds no result for the host cell protein content, protein concentration, pH or conductivity")
    sq("dev2", "The event was detected during the reconciliation of the pool fractions after execution")
    sq("dev2", "On the falling trailing edge of the peak a higher set-point is reached earlier.")
    sq("dev2", "The record gives the outcome as corrected by modelling and verification runs")
    sq("dev2", "Within the two executions the set-point was the same in every run.")
    sq("dev2", "The block term of the model of pool host cell protein")
    sq("dev3", "The run was retained in the analysis.")
    sq("dev3", "The buffer pH is not a factor of the designs, so no setting correction applies.")
    sq("dev3", "A lower buffer pH weakens the binding of acidic impurities during equilibration and the chase")
    sq("dev3", "The record does not name the run")
    sq("dev3", "The significant terms of pool host cell protein and XMuLV did not change with any deletion")
    sq("dev3", "For MVM, step yield and fragments the set of significant terms changed with")
    sq("dev3", "The event affected the screening design only, which identifies effects and sets no range.")
    for pid, row in pdrow.items():
        d = PDS[pid]
        srow("pds", f"Discrepancy {pid} from PCP-008, {d['subject'][0].lower() + d['subject'][1:]}: planned "
                    f"{d['planned']}; done {d['done']}; reason {d['reason']}.", row, rows_=pdrow, caption=pd_cap,
             label="tbl-discrepancies")
    for p_ in ("Its effect on each selected model and judgement was computed",
               "For pool host cell protein the selected model has the same scale and terms on the planned runs alone",
               "For fragments the selected model has no term on either set of runs.",
               "Step yield has no adequate model on the planned runs alone and an adequate model with no term",
               "is the refit with a justified change of terms or transformation that PCMP-001 §7.2 allows",
               "At this step no criterion moved, and no judgement over the NOR differs",
               "The selection does decide whether the host cell protein bound of this step widens the upstream",
               "the flow-rate study cannot show curvature in the effect of flow rate within the range.",
               "The comparison between the two ends does not need a centre run",
               "The reference runs at set-point were made before the designs began.",
               "supports no conclusion of this report.",
               "The viral clearance results do rest on the spiking model, and the match of the spiked load",
               "an effect of the sample matrix on the assay cannot be excluded for these results.",
               "were not compared, the block term and the prediction of the augmentation runs",
               "This holds for pool host cell protein.",
               "a run cannot be traced to its inputs, and the effect of DEV-008-03 could only be bracketed",
               "residual DNA and leached Protein A were below the LOQ in every pool in which they were measured",
               "The coefficients of the two models without a term are given in Appendix C.",
               "This report states the completion rule of PCP-008 §7 item 8 and reports against it",
               "were set at analysis, after the data were known.",
               "They are a two-sided t-test at"):
        sq("pds", p_)

    # -- Appendices: every row of the design matrices --------------------------------------------------------------
    APP = {"screening": ("app_a", "Screening design (S-AEX-SCR)"), "scr_sup": ("app_a", "Invalidated first execution, "
           "screening design (S-AEX-SUP)"), "rsm": ("app_b", "Response-surface design (S-AEX-RSM)"),
           "aug": ("app_b", "Augmentation (S-AEX-AUG)"), "rsm_sup": ("app_b", "Invalidated first execution, "
           "response-surface design (S-AEX-SUP)")}
    for kind, (sec, lab_) in APP.items():
        tab, rows_ = mtx[kind]
        for run, row in rows_.items():
            c = _cells(row)
            fac = ", ".join(f"{ns['pn'](k)} {c[2 + i]}" for i, k in enumerate(FS))
            if kind == "aug":
                resp_txt = f"pool host cell protein {c[6]} ng/mg, step yield {c[7]} %, fragments {c[8]} %"
            else:
                resp_txt = (f"pool host cell protein {c[6]} ng/mg, XMuLV LRF {c[7]}, MVM LRF {c[8]}, step yield "
                            f"{c[9]} %, fragments {c[10]} %")
            srow(sec, f"{lab_}, run {run}: {fac}; {resp_txt}.", row, tab, rows_)
    sq("app_a", "The run order was randomized at execution.")
    for (lab_, term), row in efrow.items():
        c = _cells(row)
        srow("app_c", f"Screening effect of {term} on {lab_}: effect {c[2]}, coefficient {c[3]}, standard error {c[4]}, "
                      f"t {c[5]}, p {c[6]}.", row, ef_t, efrow)
    for (lab_, term), row in cr2row.items():
        c = _cells(row)
        srow("app_c", f"Selected model of {lab_}, {term}: coefficient {c[2]}, standard error {c[3]}, t {c[4]}, p {c[5]}.",
             row, cr2_t, cr2row)
    for amv, row in msrow.items():
        c = _cells(row)
        srow("app_d", f"{amv} ({c[1]}): {c[2]}; precision {c[3]}; LOQ {c[4]}.", row, ms_t, msrow)

    sections = []
    for chap in CHAPTERS:
        stmts = [x for c_, x in STS if c_ == chap]
        if stmts:
            sections.append(ReportSection(section_id=f"{DOC}-sec{len(sections) + 1:02d}", title=chap,
                                          statements=stmts))
    if sum(len(s_.statements) for s_ in sections) != len(STS):
        raise ValueError(f"{DOC}: statements outside the chapters of the report")

    # ==== concepts ===========================================================================================
    concepts = [Concept(concept_id=STEP_ID, concept_type="PROCESS_STEP", canonical_name=UO_NAME,
                        aliases=["anion exchange", "anion exchange chromatography", "anion exchange step",
                                 P.DOC_REGISTRY[DOC][1], f"Step {G.AXSTEP}"],
                        review_status="human_verified")]
    alias = {"load_ph": ["load pH"],
             "wash1_cond": ["Equil/Wash-1 conductivity", "conductivity of the equilibration and first wash buffer"],
             "load_cond": ["load conductivity"], "load": ["protein load"],
             "flow": ["operating flow rate", "flow rate"]}
    concepts += [Concept(concept_id=PC[NAME[k]], concept_type="PROCESS_PARAMETER", canonical_name=NAME[k],
                         aliases=alias[k], review_status="human_verified") for k in ALLP]
    concepts += G._attr_concepts(ckeys)
    concepts.append(Concept(concept_id="attr:step_yield", concept_type="PERFORMANCE_ATTRIBUTE",
                            canonical_name="Step yield", aliases=["step yield", "yield"],
                            review_status="human_verified"))
    concepts += G._method_concepts([m.method_id for m in methods], amv_title)
    concepts.append(Concept(concept_id=SDM_ID, concept_type="EQUIPMENT", canonical_name=SDM_NAME,
                            aliases=["scale-down model", "scale-down column", "spiking model"],
                            review_status="human_verified"))

    # ==== the annex =========================================================================================
    annex = S.GroundTruthAnnex(
        document_id=DOC, document_title=f"{P.DOC_REGISTRY[DOC][0]} — {P.DOC_REGISTRY[DOC][1]}",
        document_class=P.DOC_REGISTRY[DOC][0], **G.rev2_layer(DOC, FILE),
        schema_extensions_used=G.COMMON_EXT + G.REV2_EXT + [
            "ProvenAcceptableRange (new model) — per attribute x parameter PAR, the two analyses of PCMP-001 "
            "§6.4 as the report prints them",
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "No set-point or NOR of the step changed at Version 2.0, so ProcessParameter.target_value and NOR are the "
            "values of the parameter table, which are also the values in force. ProcessParameter.PAR is the range "
            "carried into the control strategy: for a multivariate parameter the intersection of its NOR-propagated "
            "ranges over the outputs with a criterion (PCMP-001 §7.6), which the report states for load pH; for "
            "operating flow rate the range the report states as proven acceptable for pool host cell protein from the "
            "univariate study. rationale_for_criticality carries the classification argument of the report for the "
            "parameter, each parameter anchored on its own sentences of it.",
            "The QualityAttribute records are the six attributes of the attribute table: the cumulative MVM clearance "
            "(assigned to the step by the register), the cumulative XMuLV clearance (a modular claim), host cell "
            "protein, residual DNA and leached Protein A (cleared) and fragments (judged in the pool). "
            "acceptance_criteria holds the drug substance criterion and, for the four outputs with one, the Version 2.0 "
            "intermediate acceptance criterion of the step; residual DNA and leached Protein A have none at this step "
            "and are anchored on their rows of the residual DNA table. acceptance_criteria (the annex layer) holds the "
            "rows of the criteria-change table, Version 1.0 superseded and Version 2.0 in force. Step yield is a process "
            "performance attribute with no criterion: the concept attr:step_yield.",
            "proven_acceptable_ranges: the sixteen rows of the PAR table, with par_at_setpoint and par_nor_propagated as "
            "the columns 'PAR (set-point)' and 'PAR (NOR)' print them, and the report's description of the two analyses "
            "in its own words, in report statements anchored on its sentences. The PAR of operating flow rate is not a "
            "row of that table; it is in ProcessParameter.PAR and in report statements.",
            "The schema has no record type for a discrepancy from the plan. PD-008-01 to PD-008-10 are report statements "
            "anchored on their rows of the discrepancy register, each with the report's own sentences about it; the "
            "studies they concern carry that row as a source reference. The coding of protein load (PD-008-09) is "
            "recorded only as the report states it.",
            "The report records no deviation: a characterization study is not GMP manufacture, so the three events of "
            "execution are study events, under the numbers Version 1.0 gave them (DEV-008-01 to DEV-008-03). They are "
            "Deviation records, the schema's only record type for an event of execution. no_impact_on_conclusions is "
            "true for DEV-008-01 (the designs were re-executed and no range, class or claim rests on the first "
            "execution) and DEV-008-03 (screening only, which sets no range), and false for DEV-008-02, which the report "
            "says can change an estimated effect and for which the record holds no data.",
            "Studies: every row of the execution-window table with a schema study type has a StudyDesign record. The "
            "invalidated first execution S-AEX-SUP has no study type in the schema and has no record; its design "
            "matrices are report statements of Appendices A and B, and the event is DEV-008-01. Only the screening and "
            "response-surface designs carry n_runs, which the corpus test reserves for the seeded DoE designs; the "
            "augmentation S-AEX-AUG (a second block of the response-surface design) carries its runs in its rows.",
            "StatisticalModelFit: the planned full quadratic of each output with a criterion on the planned runs and, "
            "where the augmentation measured the output, with a block term on all runs (the re-evaluation table); the "
            "selected models of the five outputs (pool host cell protein on the log scale, both LRFs on the raw scale on "
            "the planned runs, step yield and fragments with no term besides the block), each meeting PCMP-001 §7.2 as "
            "the report judges it; and the five screening models. A p-value printed as '< 0.001' has no float value; "
            "its term carries significant=true. The models within 2 AICc units and the deletions of flagged runs are "
            "report statements, one per row of their tables.",
            "parameter_impacts_attribute: every term of a selected model with terms, on its coefficient row, with the "
            "screening effect row. The interaction of load pH and protein load in the selected XMuLV model is not "
            "asserted as an effect of protein load, because the report says it is not established as one (an explicit "
            "non-claim). parameter_does_not_significantly_impact_attribute: each parameter and output whose screening "
            "effect is not significant and whose selected model carries no term containing it, and operating flow rate "
            "on pool host cell protein and step yield from the t-tests of the flow-rate study. The screening "
            "interaction of load pH and protein load on fragments is recorded in report statements only.",
            "The ModularContribution records are the platform claims of the step against the two cumulative "
            "requirements; cumulative_value is the sum of the platform claims the report states, not a measured "
            "clearance. The capability of the cumulative clearance is a property of the train.",
            "The concept ids follow the Version 1.0 report and the PCP-008 Version 2.0 annex (step:aex, param:aex_*, "
            "equip:aex_sdm_column).",
            "rhetorical_spans: authoring/rhetorical/PCR-008.spans.yaml, re-curated against the Version 2.0 text in the "
            "same pass as this builder. weak_claims is empty.",
        ] + G._unrendered_note(unrendered),
        inventory=G.rev2_inventory(DOC, FILE, "process_characterization_report", UO_NAME,
                                   ["process characterization", "anion exchange chromatography", "flow-through mode",
                                    "host cell protein clearance", "viral clearance", "MVM and XMuLV log reduction",
                                    "intermediate acceptance criteria", "verification of platform worst cases",
                                    "design of experiments", "model selection", "log scale",
                                    "scale-down model qualification", "parameter classification"]),
        entities=entities, studies=studies, design_spaces=design_spaces, proven_acceptable_ranges=pars,
        report_sections=sections, assertions=AssertionStore(run_id=f"gt-{DOC}", assertions=AS, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{DOC}", concepts=concepts),
        weak_claims=[], rhetorical_spans=G.build_rhetorical_spans(DOC, FILE),
        acceptance_criteria=G.acceptance_criteria_layer(DOC, FILE, title("changes"), ct["tbl-criteria-change"][0],
                                                        [UO]))
    _gate(annex, text)
    return annex


def clean_(s):
    """A rendered span as statement text: the spaces of a cross-reference and of a closing quote closed up."""
    s = re.sub(r"\(\s+", "(", s)
    return re.sub(r"\s+([,.;:)])", r"\1", s)
