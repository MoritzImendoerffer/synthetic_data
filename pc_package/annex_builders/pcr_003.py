"""PCR-003 Version 2.0, the characterization report of the production bioreactor (Step 3), re-analysed under
INV-001 and INV-002: its ground-truth annex (``build()``).

The kinds of record follow the model builder for a Version 2.0 report with a designed experiment
(``annex_builders/pcr_006.py``, after ``build_ground_truth.build_report_protein_a``), and the concept ids follow the
Version 1.0 builder of this report (``build_ground_truth.build_report``) and the Version 2.0 builder of its plan
(``build_plan_bioreactor``): the inventory and the revision layer; the step, the production vessel, the scale-down
model, the pCO2 probe and the two sites; the nine parameters, with the class and the classification argument of
Section 9; the seven attributes the CQA register assigns to the step; the five analytical methods; the capability
records; the fitted models (the selected model of each output on all runs, the plan's full quadratic on the planned
runs and on all runs, the models selected on the planned runs alone against the augmentation runs, and the
screening models); the two study events; the document relationships and the explicit non-claims; the elements of
the control strategy the report recommends; the six studies of the execution-window table; the design space; the
proven acceptable ranges; the criteria of the criteria-change table (Version 1.0 superseded, Version 2.0 in force);
the assertions; the report statements, grouped by the chapters of the report; the concepts; and the rhetorical spans
of ``authoring/rhetorical/PCR-003.spans.yaml``.

The complex tables (``T.frame`` or a ``T.`` builder) are read back through ``qmd_ctables`` from the object the
report printed, the ``show`` tables through ``captured_rows``, the document's own pipe tables (``md``) from the
frames its functions return, and the markdown strings of the ``_pcpkg`` helpers (``related_docs_md``,
``dev_register``, ``discrepancy_register``) with ``md_string_rows``. Each row quote is the rendered row, with
``table_header=rows.header``. A continuation row of the PAR table reads alike for several attributes (the merged
attribute cell is empty), so each PAR record anchors on the rows from the head of its attribute block to its own row,
a contiguous span that names the attribute and the parameter. Every prose quote is a span of the ``.qmd`` copied
with its inline expressions and rendered as the ``.docx`` reads it (``render``), so no value is typed here. ``q``
records a snippet that is not a span of the ``.qmd`` prose, and ``build()`` refuses to return an annex with such a
snippet, a quote that does not ground or a weak anchor.

The registered discrepancy D-002 (``authoring/DISCREPANCIES.md``) is recorded as the document states it: the
ProcessStep description and one report statement carry the sentence of Section 1.1 that the production bioreactor
is the only step of the drug substance process at which product quality attributes are formed. It is neither
corrected nor labelled here.
"""
from __future__ import annotations

import contextlib
import io
import os
import re

import _pcpkg as P
import build_ground_truth as G
import schema_ext as S
from check_grounding import CELL_SEP, normalize, specificity_report

DOC = "PCR-003"
FILE = "PCR-003_bioreactor.docx"
QMD = "PCR-003_bioreactor.qmd"
UO = "bioreactor"
#: The scale-down model as the report names it (Section 3.1); PCP-003 names it the same way.
SDM_NAME = "bench-scale stirred-tank bioreactors"

_INTRO = "Introduction"
_PRIOR = "Prior knowledge and quality risk basis"
_MM = "Materials and methods"
_SD = "Study design"
_RES = "Results"
_RSM = "Response-surface models"
_PAR = "Proven acceptable ranges"
_REC = "Study events and discrepancies from the plan"
#: Section key -> heading path as the .qmd writes it. ``_check_sections`` checks every title against the headings of
#: the .qmd, so a renamed section fails loudly instead of mislabelling its references. The subsections of the record
#: (one per study event and per discrepancy) are added from the headings themselves, below.
SEC = {
    "title": ("Title block",),
    "exec": ("Executive summary",),
    "product": (_INTRO, "Product and unit operation"),
    "objectives": (_INTRO, "Objectives"),
    "regulatory": (_INTRO, "Regulatory and scientific basis"),
    "changes": (_INTRO, "Changes in this revision"),
    "platform": (_PRIOR, "Platform and prior-product knowledge"),
    "cqa": (_PRIOR, "Quality attributes in scope"),
    "risk": (_PRIOR, "Risk-based prioritization and parameter selection"),
    "sdm": (_MM, "Scale-down model and its qualification"),
    "operation": (_MM, "Cell line, media and culture operation"),
    "analytical": (_MM, "Analytical methods"),
    "sampling": (_MM, "Sampling plan"),
    "stats": (_MM, "Statistical methods"),
    "factors": (_SD, "Factors, ranges and the knowledge space"),
    "scr_design": (_SD, "Screening design"),
    "rsm_design": (_SD, "Response-surface design"),
    "uni_design": (_SD, "Univariate assessment"),
    "osm_design": (_SD, "Osmolality study"),
    "chronology": (_SD, "Execution of the studies"),
    "centre": (_RES, "Centre-point performance and reproducibility"),
    "screening": (_RES, "Screening: factor effects"),
    "models": (_RES, _RSM, "Selected models and their adequacy"),
    "residuals": (_RES, _RSM, "Residual patterns and influential runs"),
    "effects": (_RES, _RSM, "Effects of the parameters"),
    "augmentation": (_RES, _RSM, "What the augmentation changed"),
    "near": (_RES, _RSM, "Near-equivalent models"),
    "univariate": (_RES, "Univariate assessment"),
    "osmolality": (_RES, "Osmolality study"),
    "mech": (_RES, "Mechanistic interpretation"),
    "ds": ("Design space",),
    "criteria": (_PAR, "Acceptance criteria"),
    "criteria_results": (_PAR, "Outputs against their criteria over the NOR"),
    "par": (_PAR, "PARs"),
    "par_uni": (_PAR, "Univariate parameters and osmolality"),
    "cap": ("Process capability and robustness",),
    "class": ("Parameter classification",),
    "control": ("Contribution to the control strategy",),
    "disc": ("Discussion",),
    "concl": ("Conclusions",),
    "record": (_REC,),
    "app_a": ("Appendix A. Screening design matrix and responses",),
    "app_b": ("Appendix B. Response-surface design matrix and responses",),
    "app_c": ("Appendix C. Full effect and coefficient tables",),
    "app_d": ("Appendix D. Analytical methods summary",),
}
#: Relationship cell of the related-documents table -> DocumentRelationship.kind (others: references).
REL_KIND = {"Rolls up into": "rolls_up_into", "Sibling — paired document": "executed_under",
            "Parent — master plan": "executed_under",
            "Parent — risk basis for study scope": "scoped_by", "Parent — transfer scope": "scoped_by"}
#: The report's statements are grouped by the chapters of the report, in this order.
CHAPTERS = ["Executive summary", _INTRO, _PRIOR, _MM, _SD, _RES, "Design space", _PAR,
            "Process capability and robustness", "Parameter classification",
            "Contribution to the control strategy", "Discussion", "Conclusions", _REC]


def _sid(sec):
    return f"{DOC}_sec_{sec}"


def _source():
    return open(os.path.join(G.HERE, QMD), encoding="utf-8").read()


def _chunks():
    return re.findall(r"```\{python\}\n(.*?)```", _source(), flags=re.S)


def _prose():
    """The .qmd outside its code chunks, in the comparison form (``normalize``)."""
    return normalize(re.sub(r"```\{python\}.*?```", " ", _source(), flags=re.S))


def _headings():
    """``[(level, title, attributes)]`` of the .qmd, outside its code chunks, in document order."""
    prose = re.sub(r"```\{python\}.*?```", "", _source(), flags=re.S)
    return [(len(m.group(1)), m.group(2), m.group(3) or "")
            for m in re.finditer(r"^(#+) (.+?)(?: \{([^}]*)\})?\s*$", prose, flags=re.M)]


# the subsections of the record: "dev1", "dev2" (study events), "pd01" ... "pd13" (discrepancies from the plan)
for _lvl, _t, _a in _headings():
    if _lvl == 2 and re.match(r"DEV-003-0\d, ", _t):
        SEC[f"dev{int(_t[8:10])}"] = (_REC, _t)
    elif _lvl == 2 and re.match(r"PD-003-\d\d, ", _t):
        SEC[f"pd{_t[7:9]}"] = (_REC, _t)


def _check_sections():
    """Every heading of SEC is a heading of the .qmd (outside its code chunks)."""
    heads = {t for _, t, _ in _headings()}
    missing = sorted({t for path in SEC.values() for t in path if t != "Title block"} - heads)
    if missing:
        raise ValueError(f"{DOC}: section titles not in the document: {missing}")


def _xrefs(text, caps):
    """``{label -> rendered cross-reference}`` ("sec-changes" -> "Section 1.4", "tbl-par" -> "Table 24").

    A section number follows the numbering of the headings (an unnumbered heading takes none), as the rendered
    document prints it. A table or figure number is read off the rendered caption ("Table 24: <caption>"), with the
    caption taken from the chunk that prints it (``caps``)."""
    out, counters = {}, [0] * 6
    for lvl, _, attrs in _headings():
        if ".unnumbered" in attrs or attrs.strip() == "-":
            continue
        counters[lvl - 1] += 1
        counters[lvl:] = [0] * (6 - lvl)
        lab = re.search(r"#(sec-[\w-]+)", attrs)
        if lab:
            out[lab.group(1)] = "Section " + ".".join(str(c) for c in counters[:lvl])
    for lab, cap in caps.items():
        word = "Table" if lab.startswith("tbl-") else "Figure"
        # a caption may itself refer to a table ("The factor codes are in @tbl-factors."): match the text before it
        m = re.search(word + r" (\d+): " + re.escape(normalize(cap.split(" @")[0])), text)
        if m:
            out[lab] = f"{word} {m.group(1)}"
    return out


def _smart(s):
    """Prose as pandoc renders it: straight double quotes become typographic pairs and a straight apostrophe a
    typographic one. Table cells are raw markup and keep the straight forms."""
    return re.sub(r'"([^"]*)"', "“\\1”", s).replace("'", "’")


def _cells(row):
    """The cells of a rendered row: a continuation row keeps its empty leading cells."""
    return [c.strip() for c in row.split("|")]


def _unmark(cell):
    """A rendered cell without its trailing footnote markers ("4 a)")."""
    return re.sub(r"(?:\s[a-z]\))+$", "", str(cell)).strip()


def _nomark(cell):
    """A rendered cell without any of its footnote markers ("Carried back, tightened a) and widened b)"), for annex
    text."""
    return re.sub(r"\s[a-z]\)(?=[\s,;]|$)", "", str(cell)).strip()


def _num(cell):
    """A number as the document prints it, back to a float ("−0.9714", "2,000", "0.27 a)"); None for a cell that
    is not one ("< 0.001", "n.a.")."""
    s = _unmark(cell).replace("−", "-").replace(",", "")
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
    """The grounding gate, applied before the annex is returned: every quote and table header is a verbatim span of
    the rendered document, and no quote is a weak anchor (``check_grounding.specificity_report``)."""
    d = annex.model_dump(mode="json", serialize_as_any=True)
    miss = [q for q in _walk(d, ("quote", "table_header"), []) if normalize(q) not in text]
    weak = specificity_report(d, text)
    if miss or weak:
        raise ValueError(f"{DOC}: {len(miss)} ungrounded quote(s), {len(weak)} weak anchor(s):\n  "
                         + "\n  ".join([f"ungrounded: {q!r}" for q in miss] + [f"weak: {w}" for w in weak]))


def _printed_captions(ns, marker):
    """``[(label, caption)]`` of the tables that the chunk containing ``marker`` prints in a loop (Appendix C): the
    chunk is run again in the document's namespace and its caption lines are read from what it prints."""
    code = [c for c in _chunks() if marker in c]
    if len(code) != 1:
        raise ValueError(f"{DOC}: {len(code)} chunks contain {marker!r}")
    buf, cwd = io.StringIO(), os.getcwd()
    os.chdir(G.HERE)
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code[0], f"{QMD}#{marker}", "exec"), ns)   # noqa: S102
    finally:
        os.chdir(cwd)
    return [(m.group(2), m.group(1)) for m in re.finditer(r"^: (.*) \{#(tbl-[\w-]+)\}$", buf.getvalue(), flags=re.M)]


def _block_spans(rows_):
    """For a table whose first cell is merged: ``{key -> span}``, where the span runs from the row that opens the
    key's block (the row that names it in the first cell) to the key's own row, joined as the .docx reads them. A
    continuation row that reads like rows of other blocks is ambiguous on its own; the span names its block."""
    out, block = {}, []
    for k, row in rows_.items():
        if _cells(row)[0]:
            block = []
        block.append(row)
        out[k] = CELL_SEP.join(block)
    return out


def build():  # noqa: C901 - one document, one builder, in the order of the report
    import numpy as np
    import tables as T
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    from annex_contract.concepts import Concept, ConceptStore
    from annex_contract.discourse import DocumentRelationship, ExplicitNonClaim
    from annex_contract.results import (ControlStrategyElement, Deviation, ModelTerm, ProcessCapability,
                                        StatisticalModelFit)
    from annex_contract.summaries import ReportSection, ReportStatement

    _check_sections()
    ns, shown = G.qmd_namespace(QMD)
    ct = G.qmd_ctables(QMD)
    text = G._document_text(FILE)
    prose_src = _prose()
    meta = G.meta
    appc_scr = _printed_captions(ns, "#tbl-scr-{_lab}")
    appc_coef = _printed_captions(ns, "#tbl-coef-{_lab}")
    caps = {}
    for code in _chunks():
        lab = re.search(r"#\|\s*label:\s*((?:tbl|fig)-[\w-]+)", code)
        cap = re.search(r'#\|\s*(?:tbl|fig)-cap:\s*"(.*)"', code)
        if lab and cap:
            caps[lab.group(1)] = cap.group(1)
        for m in re.finditer(r'print\(": (.*) \{#(tbl-[\w-]+)\}"\)', code):
            caps[m.group(2)] = m.group(1)
    for lab, (tab, _) in ct.items():
        caps.setdefault(lab, tab.caption)
    caps.update(dict(appc_scr + appc_coef))
    xref = _xrefs(text, caps)
    # a caption as the .docx reads it: a cross-reference is a run of its own ("... are in Table 8 .")
    caps = {lab: re.sub(r"\s+", " ", re.sub(r"@((?:sec|tbl|fig)-[\w-]*\w)", lambda m: f" {xref[m.group(1)]} ", cap))
            for lab, cap in caps.items()}
    not_spans = []

    def render(src):
        """A span of the .qmd as the .docx reads it."""
        s = G.qmd_inline(ns, src)
        if "[@" in s:
            raise ValueError(f"{DOC}: a quote crosses a citation, end it before: {src!r}")
        s = re.sub(r"@((?:sec|tbl|fig)-[\w-]*\w)", lambda m: f" {xref[m.group(1)]} ", s)
        s = re.sub(r"~([^~\s]+)~", r" \1 ", s)            # a subscript is a run of its own
        s = re.sub(r"\^([^^\s]+)\^", r" \1 ", s)          # and so is a superscript
        s = re.sub(r"\*([^*\n]+)\*", r"\1", s)             # italics
        return re.sub(r"\s+", " ", _smart(s)).strip()

    def q(src):
        """A prose span of the .qmd as it renders. ``src`` must be copied from the .qmd."""
        if normalize(src) not in prose_src:
            not_spans.append(src)
        return render(src)

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
        """The header of a table as the .docx reads it: two footnote markers in one header cell render side by side
        ("a)b)"), which ``ctable_rows`` joins with a space."""
        if normalize(rows.header) not in text:
            rows.header = re.sub(r"([a-z]\)) (?=[a-z]\))", r"\1", rows.header)
        if normalize(rows.header) not in text:
            raise ValueError(f"{DOC}: a table header does not ground: {rows.header!r}")
        return rows

    def keyed(label, keys, name_of, cell=None):
        """The rendered rows of the CTable the report printed under ``label``, keyed. Every row must name its own
        record (in cell ``cell``, footnote markers aside, or anywhere): a mis-keyed row grounds and attests the wrong
        thing."""
        tab = ct[label][0]
        rows_ = present_header(G.ctable_rows(tab, keys))
        bad = [k for k, row in rows_.items()
               if not (_unmark(_cells(row)[cell]) == name_of(k) if cell is not None else name_of(k) in row)]
        if bad:
            raise ValueError(f"{DOC} {label}: rows keyed to records they do not name: {bad}")
        return tab, rows_

    def first_cells(label):
        return [_unmark(_cells(r)[0]) for r in ct[label][0].rows()]

    def piped(rows_):
        """A pipe table is markdown, so pandoc renders its straight apostrophes as typographic ones ("Cook’s"); the
        complex tables are raw markup and keep the straight form."""
        for k, row in list(rows_.items()):
            if normalize(row) not in text and normalize(_smart(row)) in text:
                rows_[k] = _smart(row)
        return rows_

    def md_rows(md, label):
        rows_ = piped(G.md_string_rows(md))
        cap = caps[label]
        if normalize(f"{cap} {rows_.header}") not in text:
            raise ValueError(f"{DOC}: the caption of {label} no longer reads {cap!r}")
        return rows_, cap

    def frame_rows(df, key_col, label):
        """The rows of one of the report's own pipe tables (``md``), from the frame its function returns."""
        rows_ = piped(G.captured_rows(("md", df, None), list(df[key_col])))
        if normalize(f"{caps[label]} {rows_.header}") not in text:
            raise ValueError(f"{DOC}: the caption of {label} no longer reads {caps[label]!r}")
        return rows_

    def fig_cap(label, n):
        """The first ``n`` sentences of the caption of figure ``label``, as printed."""
        out_ = " ".join(re.findall(r"[^.]+\.", caps[label])[:n]).strip()
        if normalize(out_) not in text:
            raise ValueError(f"{DOC}: the caption of {label} does not ground: {out_!r}")
        return re.sub(r"\s+", " ", out_)

    # ---- names and values of the report ----------------------------------------------------------------
    PRM, uo = ns["PRM"], ns["uo"]
    FS, SFS, UNI, RESPS = list(ns["FS"]), list(ns["SFS"]), list(ns["UNI"]), list(ns["RESPS"])
    OUT, LTR, CLS, ANAME = ns["OUT"], ns["LTR"], ns["CLS"], ns["ANAME"]
    pv, fx = ns["pv"], ns["fx"]
    FIT, SIGT = ns["FIT"], ns["SIGT"]
    UO_NAME, STEP = uo.name, uo.step
    STEP_LABEL = f"{UO_NAME} (Step {STEP})"
    HAR_STEP = P.CFG.unit_op("harvest").step
    PC = {k: G.PARAM_CONCEPT[PRM[k].name] for k in PRM}
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))
    reg = P.cqa_reg.set_index("key")
    lab_key = dict(G._attr_key_by_label())
    lab_key.update({v: k for k, v in ANAME.items()})
    lab_key.update({"Host cell protein (ng/mg)": "hcp", "DNA (pg/mg)": "residual_dna"})
    pkey_of_name = {PRM[k].name: k for k in PRM}
    ALPHA = float(ns["ALPHA"])
    CS, N_MC = ns["CS"], int(ns["N_MC"])

    def low1(x):
        """A label inside a sentence: its first letter in lower case, unless it opens with an abbreviation ("pCO2",
        "DNA")."""
        return x if (x[:1].islower() or x[1:2].isupper()) else x[0].lower() + x[1:]

    def aname(key):
        """An attribute as the report's prose names it ("aggregate", "host cell protein")."""
        return OUT.get(key) or low1(ANAME[key].rsplit(" (", 1)[0])

    def wu(k, rng):
        """A range or value of parameter ``k`` with its unit, as the report writes it."""
        u = PRM[k].unit
        if u == "pH":
            return f"pH {rng}"
        return f"{rng} × {u}" if u.startswith("10") else f"{rng} {u}"

    def term_label(term):
        """A term of the coefficient tables ("A", "AE", "A²", "Block") in words, by the report's own ``tname``."""
        if term == "Block":
            return "block term (planned runs −1, augmentation runs +1)"
        base = term.rstrip("²")
        return ns["tname"](ns["lt_term"](base) + ("^2" if term.endswith("²") else ""))

    # ---- the rendered tables, from the objects the report printed --------------------------------------
    pcap_ = shown["tbl-params"]
    prow = G.captured_rows(pcap_, list(pcap_[1]["Parameter"]))
    params_cap = pcap_[3]
    pdf_ = pcap_[1].set_index("Parameter")
    leg = G.captured_rows(shown["tbl-factors"], list(shown["tbl-factors"][1]["Factor"]))
    leg_cap = shown["tbl-factors"][3]
    cq_df = shown["tbl-cqa"][1]
    ckeys = [lab_key[n] for n in cq_df["CQA"]]
    crow = G.captured_rows(shown["tbl-cqa"], ckeys)
    cq_cap = shown["tbl-cqa"][3]
    cq_df = cq_df.set_index(np.array(ckeys))
    so_t, sorow = keyed("tbl-sdm-offsets", [lab_key[c] for c in first_cells("tbl-sdm-offsets")],
                        lambda k: T.ATTR_NAME[k], cell=0)
    sop_df = ct["tbl-sops"][1]
    sop_t, soprow = keyed("tbl-sops", list(sop_df["Reference"]), str, cell=1)
    amv_title = dict(zip(sop_df["Reference"], sop_df["Title"]))
    mbs_t = ct["tbl-methods-by-study"][0]
    mbsrow = present_header(G.ctable_rows(mbs_t, first_cells("tbl-methods-by-study")))
    ch_df = ct["tbl-chronology"][1]
    ch_t, chrow = keyed("tbl-chronology", list(ch_df["Study"]), str, cell=0)
    cen_t, cenrow = keyed("tbl-centre", [lab_key[c] for c in first_cells("tbl-centre")],
                          lambda k: T.ATTR_NAME[k], cell=0)
    sc_df = ct["tbl-screening"][1]
    sc_t, scrow = keyed("tbl-screening", list(zip([lab_key[a] for a in sc_df["Attribute"]], sc_df["Term"])),
                        lambda k: k[1], cell=1)
    mo_df = ct["tbl-models"][1]
    mo_t, morow = keyed("tbl-models", [lab_key[a] for a in mo_df["Attribute"]], lambda k: T.ATTR_NAME[k], cell=0)
    rv_t, rvrow = keyed("tbl-reeval-bioreactor", [lab_key[c] for c in first_cells("tbl-reeval-bioreactor")],
                        lambda k: T.ATTR_NAME[k], cell=0)
    c4_df = ct["tbl-crit4"][1]
    c4_t, c4row = keyed("tbl-crit4", [lab_key[a] for a in c4_df["Attribute"]], lambda k: T.ATTR_NAME[k], cell=0)
    ef_df = ct["tbl-effect-size"][1]
    ef_t, efrow = keyed("tbl-effect-size", list(zip(ef_df["Attribute"], ef_df["Parameter"])), lambda k: k[1], cell=1)
    fac_of_cell = {ns["_cap"](ns["_short"](f)): f for f in FS}
    ef_by = {(lab_key[a], fac_of_cell[p_]): (a, p_) for a, p_ in efrow}
    ag_df = ct["tbl-augcheck"][1]
    ag_t, agrow = keyed("tbl-augcheck", [lab_key[a] for a in ag_df["Attribute"]], lambda k: T.ATTR_NAME[k], cell=0)
    uv_df = ct["tbl-univariate"][1]
    uv_t, uvrow = keyed("tbl-univariate", list(zip(uv_df["Parameter"], uv_df["End of range"], uv_df["Run"])),
                        lambda k: k[2], cell=2)
    uv_head = {pkey_of_name[k[0].rsplit(" (", 1)[0]]: row for k, row in uvrow.items() if _cells(row)[0]}
    ue_df = ct["tbl-uni-effects"][1]
    ue_t, uerow = keyed("tbl-uni-effects", list(zip(ue_df["Parameter"], ue_df["Attribute"])), lambda k: k[1], cell=1)
    ue_head = {pkey_of_name[k[0]]: row for k, row in uerow.items() if _cells(row)[0]}
    os_df = ct["tbl-osmolality"][1]
    os_t, osrow = keyed("tbl-osmolality", list(zip(os_df["Attribute"], os_df["Osmolality (mOsm/kg)"])),
                        lambda k: k[1], cell=3)
    os_head = {lab_key[k[0]]: row for k, row in osrow.items() if _cells(row)[0]}
    iac_t, iacrow = keyed("tbl-iac", [lab_key[c] for c in first_cells("tbl-iac")], lambda k: T.ATTR_NAME[k], cell=0)
    cr_t, crrow = keyed("tbl-criteria-bioreactor", [lab_key[c] for c in first_cells("tbl-criteria-bioreactor")],
                        lambda k: T.ATTR_NAME[k], cell=0)
    par_df = ct["tbl-par"][1]
    par_t, parrow = keyed("tbl-par", list(zip(par_df["CQA"], par_df["Parameter"])), lambda k: k[1], cell=2)
    par_span = _block_spans(parrow)
    cp_df = ct["tbl-capability"][1]
    cp_t, cprow = keyed("tbl-capability", list(cp_df["Attribute"]), str, cell=0)
    me_df = ct["tbl-methods"][1]
    me_t, merow = keyed("tbl-methods", list(me_df["Validation"]), str, cell=2)
    mtx = {}
    for kind in ("screening", "rsm", "aug"):
        lab_ = f"tbl-doe-bioreactor-{kind}"
        mtx[kind] = keyed(lab_, [int(c) for c in first_cells(lab_)], str, cell=0)
    coef_acid = frame_rows(shown["tbl-coef-acidic"][1], "Term", "tbl-coef-acidic")
    anova_acid = frame_rows(shown["tbl-anova-acidic"][1], "Source", "tbl-anova-acidic")
    coef = {"acidic_variants": (coef_acid, caps["tbl-coef-acidic"], "tbl-coef-acidic", "effects")}
    anova = {"acidic_variants": (anova_acid, caps["tbl-anova-acidic"], "tbl-anova-acidic", "effects")}
    others = [r for r in RESPS if r != "acidic_variants"]
    if len(appc_coef) != 2 * len(others) or len(appc_scr) != len(RESPS):
        raise ValueError(f"{DOC}: Appendix C prints {len(appc_scr)} screening and {len(appc_coef)} model tables")
    for i, r in enumerate(others):
        (lc, cc), (la, ca) = appc_coef[2 * i], appc_coef[2 * i + 1]
        if OUT[r] not in cc or OUT[r] not in ca or not lc.startswith("tbl-coef-") or not la.startswith("tbl-anova-"):
            raise ValueError(f"{DOC}: Appendix C tables out of order at {r}")
        coef[r] = (frame_rows(ns["coef_table"](r), "Term", lc), cc, lc, "app_c")
        anova[r] = (frame_rows(ns["anova_table"](r), "Source", la), ca, la, "app_c")
    scr_tab = {}
    for r, (ls, cs) in zip(RESPS, appc_scr):
        if OUT[r] not in cs:
            raise ValueError(f"{DOC}: Appendix C screening tables out of order at {r}")
        scr_tab[r] = (frame_rows(ns["scr_table"](r), "Term", ls), cs, ls)
    rel, rel_cap = md_rows(P.related_docs_md(DOC), "tbl-related")
    devrow, dev_cap = md_rows(P.dev_register(DOC), "tbl-dev-register")
    pdrow, pd_cap = md_rows(P.discrepancy_register(DOC), "tbl-disc-register")
    PDS = {d["id"]: d for d in P.PLAN_DISCREPANCIES[DOC]}
    if list(pdrow) != list(PDS):
        raise ValueError(f"{DOC}: the discrepancy register no longer lists {list(PDS)}")

    def pdref(pid, sec="record"):
        return ref(sec, pdrow[pid], rows=pdrow, caption=pd_cap, label="tbl-disc-register")

    def coef_ref(r, term):
        rows_, cap_, lab_, sec_ = coef[r]
        return ref(sec_, rows_[term], rows=rows_, caption=cap_, label=lab_)

    def anova_ref(r, src):
        rows_, cap_, lab_, sec_ = anova[r]
        return ref(sec_, rows_[src], rows=rows_, caption=cap_, label=lab_)

    # ==== entities ======================================================================================
    q_step = q("This report gives the results of the Stage 1 characterization of the production bioreactor, Step 3 "
               "of the A-Mab drug substance process.")
    q_forms = q("The production bioreactor is a fed-batch culture with a working volume of `{python} CS` L at commercial "
                "scale, and it forms the glycan, charge variant and aggregate quality attributes of A-Mab.")
    q_vessel = q("It is a fed-batch culture with a working volume of `{python} CS` L at commercial scale.")
    q_secrete = q("The cells secrete A-Mab into the medium over a culture of `{python} pv('duration', "
                  "PRM['duration'].setpoint)` at the set-point, and the culture fluid passes to harvest and "
                  "clarification (Step 4) at the end of the run.")
    # D-002 (authoring/DISCREPANCIES.md): recorded as the document states it, neither corrected nor labelled
    q_only = q("The production bioreactor is the only step of the A-Mab drug substance process at which product "
               "quality attributes are formed.")
    q_seed = q("Cells were thawed from the working cell bank and expanded through the seed train to the initial viable "
               "cell concentration of the run.")
    step = S.ProcessStep(
        step_id="step:production_bioreactor", step_name=UO_NAME, step_number=str(STEP), unit_operation=UO_NAME,
        description=t(f"Step {STEP} of the A-Mab drug substance process: a fed-batch culture with a working volume of "
                      "`{python} CS` L at commercial scale, in which the cells, expanded through the seed train from the "
                      "working cell bank, secrete A-Mab into the medium over a culture of "
                      "`{python} pv('duration', PRM['duration'].setpoint)` at the set-point. The production bioreactor "
                      "is the only step of the A-Mab drug substance process at which product quality attributes are "
                      "formed; it forms the glycan, charge variant and aggregate quality attributes of A-Mab. The "
                      f"culture fluid passes to harvest and clarification (Step {HAR_STEP}) at the end of the run."),
        input_materials=["cells expanded through the seed train to the initial viable cell concentration of the run",
                         "basal medium", "nutrient feed-1"],
        output_materials=[f"culture fluid at the end of the run (harvest and clarification, Step {HAR_STEP})"],
        equipment=[f"{CS} L production bioreactor", SDM_NAME],
        source_references=[ref("exec", q_step), ref("exec", q_forms), ref("product", q_secrete),
                           ref("product", q_only), ref("operation", q_seed)],
        metadata=meta())
    q_sdm = q("The studies were run in bench-scale stirred-tank bioreactors of the same design class as the commercial "
              "production vessel, with the same control scheme for pH, temperature, dissolved oxygen and nutrient "
              "addition.")
    q_probe = q("The pCO2 of each run was measured by the probe of the scale-down bioreactor system, EQ-BRX-205.")
    q_probe_due = q("Every study of PCP-003 ran in the scale-down bioreactor system whose pCO2 probe is EQ-BRX-205, "
                    "and each window closed before the next calibration of that probe was due on "
                    "`{python} PROBE_DUE`.")
    PROBE = ns["PROBE"]
    equipment = [
        S.Equipment(equipment_id="equip:production_bioreactor", equipment_name=f"{CS} L production bioreactor",
                    equipment_type="bioreactor (commercial production vessel)",
                    source_references=[ref("product", q_vessel)], metadata=meta()),
        S.Equipment(equipment_id="equip:sdm_bench", equipment_name=SDM_NAME,
                    equipment_type="bioreactor (scale-down model)", site_name=P.SENDING_SITE,
                    source_references=[ref("sdm", q_sdm),
                                       ref("sdm", q("The scale-down model was operated under the bioreactor procedure "
                                                    "SOP-2003."))],
                    metadata=meta()),
        S.Equipment(equipment_id=f"equip:{PROBE}", equipment_name=f"pCO2 probe {PROBE}",
                    equipment_type="pCO2 probe of the scale-down bioreactor system", site_name=P.SENDING_SITE,
                    source_references=[ref("sdm", q_probe), ref("chronology", q_probe_due),
                                       ref("chronology", chrow["S-BRX-SDM"], ch_t, chrow)],
                    metadata=meta()),
    ]
    sites = G._site_entities(DOC, FILE, _sid("title"))

    # -- parameters: the row of the parameter table, the row of the factor legend (multivariate parameters) or the
    # first rows of the two univariate tables (univariate parameters), and the sentences of the classification
    # argument (Section 9) -------------------------------------------------------------------------------------
    INT_TXT = ns["INT_TXT"]
    q_kpp = q("The classes of the three KPPs rest on their expected effect on growth and titre, which the record does "
              "not hold (PD-003-09).")
    cls_quotes = {
        "pH": [q("Culture pH is a WC-CPP."),
               q("It changes all `{python} words(len(CRIT_K))` critical attributes."),
               q("Its NOR-propagated PARs for the critical attributes span the range studied, and its PAR for acidic "
                 "variants ends `{python} fx(MARG_SD['pH'])` standard deviations of its routine variation above the NOR "
                 "high."),
               q("Base addition holds it at its set-point.")],
        "temperature": [q("Culture temperature is a WC-CPP."),
                        q("It changes afucosylation, galactosylation and high mannose, and its NOR-propagated PARs span "
                          "the range studied for every attribute."),
                        q("The vessel jacket holds it.")],
        "co2": [q("pCO2 is a WC-CPP."),
                q("It changes galactosylation and afucosylation, and its NOR-propagated PARs for these attributes span "
                  "the range studied."),
                q("Its PAR for acidic variants, an attribute of very low criticality, ends "
                  "`{python} fx(MARG_SD['co2'])` standard deviations of its routine variation above the NOR high."),
                q("The carbon dioxide fraction of the sparge gas holds it.")],
        "osmolality": [q("Osmolality was classified as a critical process parameter (CPP), because no PAR from a model "
                         "shows a wide margin between its acceptable range and its NOR."),
                       q("Osmolality is a CPP."),
                       q("It lowered galactosylation in the screening design and afucosylation in the osmolality study, "
                         "both critical attributes."),
                       q("It has no PAR from a model, because it was not a factor of the response-surface design, so its "
                         "PAR cannot be shown to be wide against its NOR."),
                       q("The risk of operating outside its acceptable range is therefore not shown to be low.")],
        "duration": [q("Culture duration is a WC-CPP."),
                     q("It changes galactosylation, afucosylation and aggregate, and its NOR-propagated PARs span the "
                       "range studied for every attribute."),
                     q("It is set by the day of harvest.")],
        "do": [q("Dissolved oxygen is a GPP."),
               q("No effect was detected on any attribute measured, at the precision of @tbl-uni-effects."),
               q("The culture is not limited by oxygen at either end of the range studied (@sec-platform), so no effect "
                 "on growth or titre is expected either.")],
        "ivcc": [q("The initial viable cell concentration is a KPP."),
                 q("It raised acidic variants, an attribute of very low criticality, by `{python} fx(UIV_D_MFG)` points "
                   "across its range, in a single significant result that may be a false positive (@sec-univariate), "
                   "and no effect on a critical attribute was detected."),
                 q("A higher initial concentration brings the culture to its peak cell density earlier and raises the "
                   "titre (@sec-platform), so it acts on process performance."), q_kpp],
        "medium_conc": [q("Basal medium concentration is a KPP."),
                        q("A higher concentration raises the supply of nutrients, and with it growth and titre "
                          "(PCP-003 §4.1), so it acts on process performance."), q_kpp],
        "feed_vol": [q("Nutrient feed-1 volume is a KPP."),
                     q("The feed supplies the glucose, amino acids and precursors for growth and titre (@sec-platform), "
                       "so it acts on process performance."),
                     q("The feed under-delivery of DEV-003-02 left the feed within its NOR (@sec-dev-02)."), q_kpp],
    }
    head = "Classified {c} under SOP-4001 by the decision logic of PCMP-001 §7.7. "
    kpp_tail = (" The class rests on that expected effect on growth and titre, which the record does not hold "
                "(PD-003-09).")
    rationale = {
        "pH": head.format(c=CLS["pH"]) + t(
            "Culture pH changes all `{python} words(len(CRIT_K))` critical attributes. Its NOR-propagated PARs for the "
            "critical attributes span the range studied, and its PAR for acidic variants ends "
            "`{python} fx(MARG_SD['pH'])` standard deviations of its routine variation above the NOR high. Base addition "
            "holds it at its set-point."),
        "temperature": head.format(c=CLS["temperature"]) + (
            "Culture temperature changes afucosylation, galactosylation and high mannose, and its NOR-propagated PARs "
            "span the range studied for every attribute. The vessel jacket holds it."),
        "co2": head.format(c=CLS["co2"]) + t(
            "pCO2 changes galactosylation and afucosylation, and its NOR-propagated PARs for these attributes span the "
            "range studied. Its PAR for acidic variants, an attribute of very low criticality, ends "
            "`{python} fx(MARG_SD['co2'])` standard deviations of its routine variation above the NOR high. The carbon "
            "dioxide fraction of the sparge gas holds it."),
        "osmolality": head.format(c=CLS["osmolality"]) + (
            "Osmolality lowered galactosylation in the screening design and afucosylation in the osmolality study, both "
            "critical attributes. It has no PAR from a model, because it was not a factor of the response-surface "
            "design, so its PAR cannot be shown to be wide against its NOR. At its NOR high the fitted mean of acidic "
            "variants lies below their lower limit at the least favourable combination of the other parameters, although "
            "the slope of the osmolality study is not significant. The risk of operating outside its acceptable range is "
            "therefore not shown to be low."),
        "duration": head.format(c=CLS["duration"]) + (
            "Culture duration changes galactosylation, afucosylation and aggregate, and its NOR-propagated PARs span the "
            "range studied for every attribute. It is set by the day of harvest."),
        "do": head.format(c=CLS["do"]) + (
            "No effect of dissolved oxygen was detected on any attribute measured, at the precision of the univariate "
            "comparison. The culture is not limited by oxygen at either end of the range studied, so no effect on growth "
            "or titre is expected either."),
        "ivcc": head.format(c=CLS["ivcc"]) + t(
            "The initial viable cell concentration raised acidic variants, an attribute of very low criticality, by "
            "`{python} fx(UIV_D_MFG)` points across its range, in a single significant result that may be a false "
            "positive, and no effect on a critical attribute was detected. A higher initial concentration brings the "
            "culture to its peak cell density earlier and raises the titre, so it acts on process performance.")
        + kpp_tail,
        "medium_conc": head.format(c=CLS["medium_conc"]) + (
            "No effect of basal medium concentration was detected on any attribute measured. A higher concentration "
            "raises the supply of nutrients, and with it growth and titre (PCP-003 §4.1), so it acts on process "
            "performance.") + kpp_tail,
        "feed_vol": head.format(c=CLS["feed_vol"]) + (
            "No effect of nutrient feed-1 volume was detected on any attribute measured. The feed supplies the glucose, "
            "amino acids and precursors for growth and titre, so it acts on process performance. The feed "
            "under-delivery of DEV-003-02 left the feed within its NOR.") + kpp_tail,
    }
    params = []
    for name, row in prow.items():
        k = pkey_of_name[name]
        r = pdf_.loc[name]
        refs = [ref("factors", row, rows=prow, caption=params_cap, label="tbl-params")]
        if name in leg:
            refs.append(ref("factors", leg[name], rows=leg, caption=leg_cap, label="tbl-factors"))
        if k in uv_head:
            refs += [ref("univariate", uv_head[k], uv_t, uvrow), ref("univariate", ue_head[k], ue_t, uerow)]
        refs += [ref("exec" if x.startswith("Osmolality was classified") else "class", x) for x in cls_quotes[k]]
        if k in INT_TXT:
            par_ = wu(k, INT_TXT[k])
        elif k in UNI:
            par_ = ns["range_txt"](k)
        else:
            par_ = None
        if r["Class"] != CLS[k]:
            raise ValueError(f"{DOC}: the class of {name} in the parameter table is not the class of the register")
        params.append(S.ProcessParameter(
            parameter_id=PC[k], parameter_name=name, parameter_type=r["Class"], unit=r["Unit"],
            target_value=pv(k, PRM[k].setpoint), NOR=ns["nor_txt"](k), PAR=par_, associated_step=STEP_LABEL,
            rationale_for_criticality=rationale[k], study_type=str(r["Study"]), source_references=refs,
            metadata=meta()))

    # -- attributes: the register row; for the five modelled attributes also the row of the criterion derivation and
    # the row of the outputs against their criteria; and the sentence that gives the criticality or the judgement --
    method_of = {"afucosylation": "AMV-3010", "galactosylation": "AMV-3010", "high_mannose": "AMV-3010",
                 "aggregates_hmw": "AMV-3011", "acidic_variants": "AMV-3013", "hcp": "AMV-3012",
                 "residual_dna": "AMV-3014"}
    for key, amv in method_of.items():
        if key not in G.METHOD_ATTRS[amv]:
            raise ValueError(f"{DOC}: {amv} does not measure {key}")
    q_vl = q("Acidic variants and residual DNA have very low criticality, and their drug substance criteria still apply "
             "(PCMP-001 §3).")
    q_hcp_dna = q("Host cell protein and residual DNA in the drug substance depend on the clearance of the downstream "
                  "steps, which the integrated model takes from Protein A, cation exchange and anion exchange (PCR-005, "
                  "PCR-007 and PCR-008).")
    attr_prose = {
        "afucosylation": [q("Antibody without core fucose binds the Fc gamma receptor IIIa (FcγRIIIa) on the effector "
                            "cell more strongly, which raises ADCC, so afucosylation is linked to efficacy.")],
        "galactosylation": [q("In the A-Mab studies complement-dependent cytotoxicity (CDC) rose with the galactose "
                              "content, while ADCC did not change")],
        "high_mannose": [q("High mannose species are cleared from the circulation faster than the fully processed "
                           "glycoforms, which gives high mannose the highest Tool #1 score of the step.")],
        "aggregates_hmw": [q("Aggregate is scored for its immunogenic potential.")],
        "acidic_variants": [q_vl],
        "hcp": [q("Host cell protein has moderate to high criticality (M-H)."),
                q("Host cell protein is first judged in the Protein A pool."), q_hcp_dna],
        "residual_dna": [q_vl, q("Residual DNA is judged on the drug substance only, because the platform history gives "
                                 "no worst-case DNA clearance for the steps after Protein A (PCMP-001 §7.3)."),
                         q_hcp_dna],
    }
    q_noiac = q("Neither has an intermediate acceptance criterion at this step.")
    IAC = ns["IAC"]
    cap_label = {lab_key[a]: a for a in cprow}
    attrs = []
    for key in ckeys:
        r = cq_df.loc[key]
        modelled = key in RESPS
        crit = [f"{r['Acceptance']} (drug substance)"]
        refs = [ref("cqa", crow[key], rows=crow, caption=cq_cap, label="tbl-cqa")]
        if modelled:
            ia = IAC.loc[key]
            crit.append(f"{T.crit(ia['iac_low'], ia['iac_high'], ia['spec_type'])} % (intermediate acceptance "
                        f"criterion, production bioreactor output, Version {ns['VER']})")
            refs += [ref("criteria", iacrow[key], iac_t, iacrow),
                     ref("criteria_results", crrow[key], cr_t, crrow)]
        else:
            refs += [ref("cap", cprow[cap_label[key]], cp_t, cprow), ref("cqa", q_noiac)]
        refs += [ref("cap" if x == q_hcp_dna else "cqa", x) for x in attr_prose[key]]
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=names[key], attribute_type="CQA", unit=reg.loc[key, "unit"],
            acceptance_criteria=crit, analytical_method=method_of[key], associated_steps=[STEP_LABEL],
            rationale_for_criticality=f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = {r['Tool #1']}.",
            criticality_level=r["Criticality"], tool1_score=int(r["Tool #1"]),
            tool2_severity=int(reg.loc[key, "tool2_severity"]), source_references=refs, metadata=meta()))

    # -- analytical methods: the procedure row, the methods-summary row (Appendix D), the sentence of Section 3.3
    # that names the method, and for SEC the row of the methods-by-study table that names it ---------------------
    q_impur = q("The host cell protein ELISA and the residual DNA qPCR measured the two impurities in the clarified "
                "harvest.")
    q_meth = {"AMV-3010": q("The released N-glycan map by 2-AB HILIC-UPLC measured afucosylation, galactosylation and "
                            "high mannose from one preparation, so the three glycan results of a run are not "
                            "independent measurements."),
              "AMV-3011": q("Size exclusion chromatography (SEC) measured aggregate as high molecular weight species "
                            "(HMW)."),
              "AMV-3013": q("Imaged capillary isoelectric focusing (icIEF) measured acidic variants."),
              "AMV-3012": q_impur, "AMV-3014": q_impur}
    me_by = me_df.set_index("Validation")
    methods = []
    for amv in [a for a in sop_df["Reference"] if a.startswith("AMV-")]:
        ks = [k for k, a in method_of.items() if a == amv]
        methods.append(S.AnalyticalMethod(
            method_id=amv, method_name=amv_title[amv], method_type=G.METHOD_TYPE.get(amv),
            analytes=[me_by.loc[amv, "Attributes"]], associated_attributes=[f"attr:{k}" for k in ks],
            validation_status="validated",
            source_references=[ref("analytical", soprow[amv], sop_t, soprow), ref("app_d", merow[amv], me_t, merow),
                               ref("analytical", q_meth[amv])]
            + (G.size_variant_refs(DOC, FILE, title("analytical"), [UO], G.SIZE_VARIANT_TOKEN[amv], text, lead=1)
               if amv in G.SIZE_VARIANT_TOKEN else []),
            metadata=meta()))

    # -- capability: one record per row of the capability table --------------------------------------------------
    CAPT = ns["CAPT"]
    q_cap_ac = q("The Cpk of acidic variants is `{python} fx(ACAP.Cpk)`, between the minimum and the target, and it is "
                 "limited by the lower limit, with an index of `{python} fx(ACAP.Cpl)` for the lower limit and "
                 "`{python} fx(ACAP.Cpu)` for the upper.")
    q_lowest = q("The lowest Cpk of the drug substance is that of acidic variants, `{python} fx(ACAP.Cpk)`, between the "
                 "minimum and the target of PCMP-001, and every other attribute that the step sets has a Cpk above the "
                 "target.")
    q_cap_agg = q("Aggregate in the drug substance lies far below its limit, at a mean of "
                  "`{python} pct(CAPT.loc['aggregates_hmw', 'mean'], 2)`, and it is judged on the prediction interval of "
                  "a single run over the NOR of this step (@sec-criteria-results) and of the steps after it.")
    cap_prose = {"acidic_variants": [("cap", q_cap_ac), ("concl", q_lowest)], "aggregates_hmw": [("cap", q_cap_agg)]}
    capab = []
    for lab_, row in cprow.items():
        key = lab_key[lab_]
        c = _cells(row)              # Attribute | Criticality | Criterion | Mean | SD | Cpk | Against | Batches | Tail
        capab.append(ProcessCapability(
            capability_id=f"{DOC}-CAP{len(capab) + 1:02d}", quality_attribute=f"attr:{key}", index_name="Cpk",
            index_value=_num(c[5]), specification_side={"upper": "upper", "lower": "lower"}.get(
                CAPT.loc[key, "spec_type"], "two_sided"),
            acceptance_range=c[2], mean=c[3], standard_deviation=c[4], unit=reg.loc[key, "unit"], basis="simulated",
            n_batches=N_MC, unit_operation=UO_NAME, claimed_process_minimum=(key == "acidic_variants"),
            source_references=[ref("cap", row, cp_t, cprow)] + [ref(s_, x) for s_, x in cap_prose.get(key, [])],
            metadata=meta()))
    if min(P.cap["Cpk"]) != P.cap.set_index("key").loc["acidic_variants", "Cpk"]:
        raise ValueError(f"{DOC}: acidic variants no longer carry the lowest Cpk of the drug substance")

    # -- fitted models -------------------------------------------------------------------------------------------
    fits = []

    def fit_rec(resp, form, refs, **kw):
        fits.append(StatisticalModelFit(
            model_fit_id=f"{DOC}-FIT{len(fits) + 1:02d}", response=resp, unit_operation=UO_NAME, model_form=form,
            source_references=refs, metadata=meta(), **kw))

    def terms_of(r):
        """The terms of the coefficient table of the selected model of ``r``, besides the intercept."""
        rows_ = coef[r][0]
        out_ = []
        for term, row in rows_.items():
            if term == "Intercept":
                continue
            c = _cells(row)                       # Term | Coef. | Std. err. | t | p-value | Sig.
            out_.append(ModelTerm(term=term, factor=term_label(term), coefficient=_num(c[1]), standard_error=_num(c[2]),
                                  t_statistic=_num(c[3]), p_value=_num(c[4]),
                                  significant=(c[4].startswith("<") or (_num(c[4]) or 1) < ALPHA)))
        return out_

    q_rawscale = q("The raw scale is used for `{python} join_and([OUT[r] for r in RAWR])`, and the log scale for "
                   "`{python} join_and([OUT[r] for r in LOGR])`.")
    cen_rsm = {k: _cells(row) for k, row in cenrow.items()}   # Attribute | n | Mean | SD | CV | n | Mean | SD | CV
    for r in RESPS:
        f_ = FIT[r]
        m, c4 = _cells(morow[r]), _cells(c4row[r])
        mod = _cells(anova[r][0]["Model"])
        cc = cen_rsm[r]
        refs = [ref("models", morow[r], mo_t, morow), ref("residuals", c4row[r], c4_t, c4row),
                anova_ref(r, "Model"), anova_ref(r, "Lack of fit"), ref("centre", cenrow[r], cen_t, cenrow)]
        refs += [coef_ref(r, term) for term in coef[r][0] if term != "Intercept"]
        if r == "afucosylation":
            refs.append(ref("models", q_rawscale))
        scale = m[1]
        fit_rec(r, f"selected model (PD-003-03), {scale} scale, {m[3]} terms besides the intercept and the block term, "
                   f"on all {f_['n']} runs: {ns['term_names'](f_['names'])}",
                refs, n_runs=int(f_["n"]), r_squared=_num(m[4]), adjusted_r_squared=_num(m[5]),
                predicted_r_squared=_num(m[6]), f_statistic=_num(mod[4]), p_value=_num(m[8]),
                lack_of_fit_p=_num(m[9]),
                adequacy_statement=(
                    f"Box-Cox λ {m[2]}, so the {scale} scale. Meets the first three adequacy criteria of PCMP-001 §7.2: "
                    f"model F-test p {m[8]}, lack of fit p {m[9]}, R² minus predicted R² {m[7]} against the limit of "
                    f"{fx(ns['GAPMAX'])}. Criterion on residuals and influential runs: {c4[6]} (spread p {c4[1]}, order "
                    f"p {c4[2]}, largest Cook's distance {c4[3]} against the F median {c4[4]}; runs above 4/n examined "
                    f"by deletion: {c4[5]})."),
                terms=terms_of(r), replicate_n=int(cc[5]), replicate_mean=cc[6], replicate_sd=cc[7],
                replicate_cv=cc[8])
    # the plan's full quadratic model, on the planned runs and on all runs with a block term (re-evaluation table)
    for r, row in rvrow.items():
        c = _cells(row)   # Attribute | Runs | R² | Pred. R² | Gap | Runs | R² | Pred. R² | Gap | LoF p | Block p | Model
        fit_rec(r, "full quadratic on the planned runs (PCP-003, raw scale)", [ref("models", row, rv_t, rvrow)],
                n_runs=int(c[1]), r_squared=_num(c[2]), predicted_r_squared=_num(c[3]),
                adequacy_statement=f"R² minus predicted R² {c[4]} against the limit of {fx(ns['GAPMAX'])} of PCMP-001 "
                                   f"§7.2" + (" (not met)" if _num(c[4]) > ns["GAPMAX"] else " (met)") + ".")
        fit_rec(r, "full quadratic on all runs with a block term (raw scale)", [ref("models", row, rv_t, rvrow)],
                n_runs=int(c[5]), r_squared=_num(c[6]), predicted_r_squared=_num(c[7]), lack_of_fit_p=_num(c[9]),
                adequacy_statement=f"R² minus predicted R² {c[8]} against the limit of {fx(ns['GAPMAX'])}"
                                   + (" (not met)" if _num(c[8]) > ns["GAPMAX"] else " (met)")
                                   + f"; lack of fit p {c[9]}; block p {c[10]}. The model used instead: "
                                     f"{_unmark(c[11])}.")
    # the models selected on the planned runs alone, against the augmentation runs (Section 5.3.4)
    q_poor = q("The models of `{python} join_and([OUT[r] for r in POOR])` predict them poorly, with a root mean square "
               "error of prediction `{python} fx(AUGC.loc['high_mannose', 'rmsep'] / AUGC.loc['high_mannose', "
               "'rmse_model'], 1)` and `{python} fx(AUGC.loc['aggregates_hmw', 'rmsep'] / AUGC.loc['aggregates_hmw', "
               "'rmse_model'], 1)` times their residual standard deviation.")
    q_aug_agg = q("For aggregate only `{python} AUG_IN_AGG` of the `{python} AUG_N` augmentation runs fall inside their "
                  "95 % prediction intervals, so the single-run intervals of aggregate understate the scatter between "
                  "runs.")
    poor = list(ns["POOR"])
    for r, row in agrow.items():
        c = _cells(row)   # Attribute | Scale, planned to all | inside the 95 % PI | RMSEP over residual SD | Block p
        refs = [ref("augmentation", row, ag_t, agrow)]
        if r in poor:
            refs.append(ref("augmentation", q_poor))
        if r == "aggregates_hmw":
            refs.append(ref("augmentation", q_aug_agg))
        fit_rec(r, f"selected model on the {ns['N_PLAN']} planned runs alone, {c[1].split(' to ')[0]} scale",
                refs, n_runs=int(ns["N_PLAN"]),
                adequacy_statement=f"Predicts {c[2]} augmentation runs inside their 95 % prediction intervals, with a "
                                   f"root mean square error of prediction {c[3]} times its residual standard deviation; "
                                   f"block term of the model selected on all runs p {c[4]}; scale on the planned runs "
                                   f"and on all runs: {c[1]}.")
    # the screening models: main effects and two-factor interactions in coded units, used to identify effects
    SCRF = ns["SCRF"]
    q_scr_nsig = q("The screening models of `{python} join_and([OUT[r] for r in SCR_NSIG_MODEL])` have no significant "
                   "model F-test (p `{python} pfmt(SCRF['afucosylation']['p'])` and p "
                   "`{python} pfmt(SCRF['high_mannose']['p'])`), so their individual effects identify candidates and no "
                   "more.")
    if list(ns["SCR_NSIG_MODEL"]) != ["afucosylation", "high_mannose"]:
        raise ValueError(f"{DOC}: the screening models without a significant F-test are no longer the two the text names")
    sig_by = {}
    for (rk, term), row in scrow.items():
        sig_by.setdefault(rk, []).append(row)
    cen_scr = cen_rsm
    for r in RESPS:
        rows_, cap_, lab_ = scr_tab[r]
        terms = []
        for term, row in rows_.items():
            c = _cells(row)                       # Term | Effect | Coef. | Std. err. | t | p-value | Sig.
            terms.append(ModelTerm(term=term, factor=term_label(term), effect=_num(c[1]), coefficient=_num(c[2]),
                                   standard_error=_num(c[3]), t_statistic=_num(c[4]), p_value=_num(c[5]),
                                   significant=(c[5].startswith("<") or (_num(c[5]) or 1) < ALPHA)))
        cs_ = cen_scr[r]
        f_ = SCRF[r]
        nsig = r in ns["SCR_NSIG_MODEL"]
        fit_rec(r, "screening model: main effects and two-factor interactions in coded units",
                [ref("app_c", row, rows=rows_, caption=cap_, label=lab_) for row in rows_.values()]
                + [ref("screening", row, sc_t, scrow) for row in sig_by.get(r, [])]
                + ([ref("screening", q_scr_nsig)] if nsig else []),
                n_runs=int(ns["N_SCR"]), p_value=float(f"{f_['p']:.3f}") if nsig else None,
                adequacy_statement=(t("Read only to identify active factors and interactions; it leaves "
                                      "`{python} words(SDF_LOF)` degree of freedom for lack of fit and "
                                      "`{python} words(SDF_PE)` for pure error. No screening model shows significant "
                                      "curvature (lack-of-fit p-values from `{python} fx(SCR_LOF_MIN, 3)` to "
                                      "`{python} fx(SCR_LOF_MAX, 3)` across the five).")
                                    + (" No significant model F-test, so its individual effects identify candidates "
                                       "and no more." if nsig else "")),
                terms=terms, replicate_n=int(cs_[1]), replicate_mean=cs_[2], replicate_sd=cs_[3], replicate_cv=cs_[4])

    # -- study events --------------------------------------------------------------------------------------------
    DEVS = ns["dev_facts"](DOC).set_index("dev_id")
    q_dev_both = q("The pCO2 probe drift in one screening run and the feed under-delivery to one centre-point batch "
                   "(DEV-003-01 and DEV-003-02) left their runs in the analysis.")
    dev_prose = {
        "DEV-003-01": [("exec", q_dev_both),
                       ("screening", q("Screening run 4 ran below its design setting of pCO2, because the pCO2 probe "
                                       "read high (study event DEV-003-01).")),
                       ("dev1", q("During screening run 4 the pCO2 probe of the scale-down system, EQ-BRX-205, read "
                                  "`{python} pv('co2', DRIFT)` higher than the offline reference, and the comparison of "
                                  "the two in in-process monitoring detected the drift.")),
                       ("dev1", q("The controller held the probe reading at the design level of "
                                  "`{python} pv('co2', R4_CO2)`, so the run ran at about `{python} pv('co2', R4_REC)`.")),
                       ("dev1", q("The record gives the cause as drift of the probe between two calibrations, and the "
                                  "equipment record shows the probe in calibration at the time of execution.")),
                       ("dev1", q("The run is analysed at its recorded setting, a shift of "
                                  "`{python} fx(abs(DRIFT_CODED), 3)` in coded units, in which 1 is the half-range of "
                                  "pCO2.")),
                       ("dev1", q("The response-surface design ran later on the same probe, and the record shows no "
                                  "recalibration between the two designs, so it does not show whether the probe read "
                                  "high in those runs too."))],
        "DEV-003-02": [("exec", q_dev_both),
                       ("dev2", q("A centre-point batch of the screening design received "
                                  "`{python} pct(float(dev_003_02_feed_deficit_pct))` less nutrient feed-1 than its "
                                  "target, from lot LOT-FED-3120.")),
                       ("dev2", q("The mass reconciliation after the run detected it, and its cause was a calibration "
                                  "offset of the feed pump.")),
                       ("dev2", q("The batch received a feed volume of about `{python} pv('feed_vol', FEED_DELIV, 1)`, "
                                  "inside the NOR of `{python} nor_txt('feed_vol')` and the range studied of "
                                  "`{python} range_txt('feed_vol')`, and the univariate study detected no effect of the "
                                  "nutrient feed-1 volume on any attribute across that range (@sec-univariate).")),
                       ("dev2", q("The record names the batch as a screening centre point but not its run number, and "
                                  "@tbl-centre gives the spread of the `{python} words(NC_SCR)` centre points."))],
    }
    dev_impact = {
        "DEV-003-01": t("The run is analysed at its recorded setting of `{python} pv('co2', R4_REC)` instead of its "
                        "design setting of `{python} pv('co2', R4_CO2)`, a shift of `{python} fx(abs(DRIFT_CODED), 3)` in "
                        "coded units. With the run at its design setting the set of significant screening effects is "
                        "the same for every attribute. With run 4 excluded the screening model keeps "
                        "`{python} words(R4['afucosylation']['excl_df'])` residual degrees of freedom, and fewer effects "
                        "reach significance for `{python} join_and([OUT[r] for r in R4_FEWER])`; for afucosylation the "
                        "same number, but not the same set. The run stayed in the analysis. The record names screening "
                        "run 4 only and does not show whether the probe read high in the response-surface runs, which "
                        "ran later on the same probe with no recalibration recorded."),
        "DEV-003-02": t("The batch received about `{python} pv('feed_vol', FEED_DELIV, 1)` of nutrient feed-1, inside "
                        "the NOR of `{python} nor_txt('feed_vol')`, and the univariate study detected no effect of the "
                        "nutrient feed-1 volume on any attribute across the range studied. The record names the batch "
                        "as a screening centre point but not its run number. The run stayed in the analysis."),
    }
    devs = []
    for did, row in devrow.items():
        c = _cells(row)              # Event | Summary | Detected during | Outcome
        if str(DEVS.loc[did, "disposition"]) != "retained":
            raise ValueError(f"{DOC}: {did} is no longer retained; its record says it is")
        devs.append(Deviation(
            deviation_id=did, summary=c[1], unit_operation=UO_NAME, detected_during=c[2], disposition=c[3],
            impact_statement=dev_impact[did], no_impact_on_conclusions=False,
            source_references=[ref("record", row, rows=devrow, caption=dev_cap, label="tbl-dev-register")]
            + [ref(s_, x) for s_, x in dev_prose[did]],
            metadata=meta()))

    # -- document relationships: the rows of the related-documents table, then the prose ---------------------------
    rels = []

    def relation(kind, target, statement, sec, quote, table_row=False):
        r_ = (ref(sec, quote, rows=rel, caption=rel_cap, label="tbl-related") if table_row else ref(sec, quote))
        rels.append(DocumentRelationship(
            relationship_id=f"{DOC}-R{len(rels) + 1:02d}", kind=kind, source_document_id=DOC,
            target_document_ref=target, statement=statement, source_references=[r_], metadata=meta()))

    for target, row in rel.items():
        txt = _cells(row)[-1]
        relation(REL_KIND.get(txt, "references"), target, txt, "product", row, table_row=True)
    q_inv_both = q("It replaces Version 1.0 after the QA investigations INV-001, on the acceptance criteria, and INV-002, "
                   "on the adequacy of the response-surface models (@sec-changes).")
    q_pcmp = q("It applies the strategy, the statistical methods and the acceptance criteria of PCMP-001 Version 2.0, "
               "and it rolls up into the Process Characterization Master Report PCMR-001.")
    q_downstream = q("Residual DNA is cleared by the same steps and judged at the drug substance only (PCR-005, PCR-007 "
                     "and PCR-008).")
    relation("executed_under", "PCP-003", "The report gives the results of the studies planned in PCP-003.", "product",
             q("This report gives the results of the studies planned in PCP-003."))
    relation("executed_under", "PCMP-001", "The report applies the strategy, the statistical methods and the acceptance "
             "criteria of PCMP-001 Version 2.0.", "product", q_pcmp)
    relation("rolls_up_into", "PCMR-001", "The report rolls up into the Process Characterization Master Report "
             "PCMR-001.", "product", q_pcmp)
    relation("scoped_by", "RA-001", "The risk assessment RA-001 set the scope of the studies.", "product",
             q("The risk assessment RA-001 set the scope of the studies."))
    relation("references", "PTP-001", "The characterization supports the transfer of the process from the development "
             "site to the commercial drug substance site under the Process Transfer Plan PTP-001.", "product",
             q("The characterization supports the transfer of the process from the development site in "
               "`{python} SENDING_LOCATION` to the commercial drug substance site in `{python} RECEIVING_LOCATION` under "
               "the Process Transfer Plan PTP-001."))
    relation("references", "INV-001", "Version 2.0 replaces Version 1.0 after the QA investigation INV-001, on the "
             "acceptance criteria.", "exec", q_inv_both)
    relation("references", "INV-002", "Version 2.0 replaces Version 1.0 after the QA investigation INV-002, on the "
             "adequacy of the response-surface models; its corrective action CA3 is the model selection of the report.",
             "exec", q_inv_both)
    relation("references", "PCR-007", "The cation exchange bound for the aggregate clearance, which tightened the "
             "aggregate criterion of the step, is in PCR-007.", "criteria",
             q("The one-sided 95 % prediction bound of a single batch there, "
               "`{python} fx(float(cex_agg.predicted_nor_bound95))`-fold, replaced the platform value (PCR-007)."))
    relation("references", "PCR-010", "The UF/DF bound for the aggregate increase, from the univariate study "
             "S-UFDF-UNI2, which tightened the aggregate criterion of the step, is in PCR-010.", "criteria",
             q("The one-sided 95 % prediction bound of a single run, "
               "`{python} fx(float(uf_agg.predicted_nor_bound95))` points, replaced the assumption of no increase "
               "(PCR-010)."))
    relation("references", "PCR-006", "The low-pH viral inactivation bound for the aggregate increase, which widened the "
             "aggregate criterion of the step, is in PCR-006, which also states whether it depends on a single run.",
             "criteria", q("PCR-006 gives the bound and states whether it depends on a single run, as PCMP-001 §7.5 "
                           "requires."))
    for target in ("PCR-005", "PCR-007", "PCR-008"):
        relation("references", target, "Host cell protein and residual DNA are cleared by Protein A, cation exchange "
                 "and anion exchange, which the reports PCR-005, PCR-007 and PCR-008 characterize.", "control",
                 q_downstream)
    relation("references", ns["AMD"]["id"], "The analytical method decision that moved the measurement of fragments to "
             "non-reduced CE-SDS changes no method of the report.", "changes",
             q("The analytical method decision AMD-001 of `{python} AMD['date']`, which moved the measurement of "
               "fragments to non-reduced CE-SDS, changes no method of this report (@tbl-methods-by-study)."))

    # -- explicit non-claims, by section ---------------------------------------------------------------------------
    ncs, nc_at = [], {}

    def nclaim(sec, subject, statement, quotes, rationale=None, elsewhere=None):
        ncs.append(ExplicitNonClaim(
            non_claim_id=f"{DOC}-NC{len(ncs) + 1:02d}", subject=subject, unit_operation=UO_NAME,
            statement=statement, rationale=rationale, handled_elsewhere=elsewhere,
            source_references=[ref(s_, x) for s_, x in quotes], metadata=meta()))
        nc_at.setdefault(sec, []).append(ncs[-1])

    nclaim("platform", "metabolite data", "The record holds no metabolite data with which to check the supply of "
           "glucose, amino acids and nucleotide sugar precursors directly.",
           [("platform", q("The record holds no metabolite data with which to check the supply directly."))])
    nclaim("cqa", "fragments", "Fragments are not an attribute of these studies.",
           [("cqa", q("The CQA register assigns fragments to harvest, and fragments have no intermediate acceptance "
                      "criterion at this step, so they are not an attribute of these studies.")),
            ("analytical", mbsrow["Fragments, LMW"])],
           rationale="The CQA register assigns fragments to harvest, and they have no intermediate acceptance criterion "
                     "at this step.", elsewhere="harvest")
    nclaim("cqa", "intermediate acceptance criteria for host cell protein and residual DNA",
           "Host cell protein and residual DNA were measured on the clarified harvest for information; neither has an "
           "intermediate acceptance criterion at this step, and the step carries no criterion for either in the "
           "clarified harvest.",
           [("cqa", q("Host cell protein and residual DNA were measured on the clarified harvest for information.")),
            ("sampling", q("The step carries no criterion for either."))],
           elsewhere="the Protein A pool (host cell protein) and the drug substance (residual DNA)")
    nclaim("risk", "PAR beyond the range studied", "No PAR is claimed beyond the range studied.",
           [("risk", q("No PAR is claimed beyond the range studied."))])
    nclaim("sdm", "cause of the aggregate offset", "The cause of the difference in aggregate between the scales is not "
           "known; it was accounted for through the offset and not investigated before the characterization runs.",
           [("sdm", q("That difference is accounted for through the offset and was not investigated before the "
                      "characterization runs (PD-003-13).")),
            ("sdm", q("Its cause is not known."))], elsewhere="PD-003-13")
    nclaim("operation", "inputs controlled to a platform specification", "Inputs controlled to a platform "
           "specification (medium and feed lots, gases, base) were tested on receipt and were not characterized.",
           [("operation", q("Inputs controlled to a platform specification, such as the medium and feed lots, the gases "
                            "and the base, were tested for identity and quality on receipt and were not "
                            "characterized."))])
    nclaim("stats", "prediction from the screening model", "The screening analysis was read only to identify active "
           "factors and interactions; every prediction, range and the design space come from the response-surface "
           "model.",
           [("stats", q("With so few, R² overstates how well the model would predict new runs, so the screening analysis "
                        "was read only to identify active factors and interactions.")),
            ("screening", q("The response-surface model re-estimates the effects of the `{python} words(len(FS))` "
                            "factors carried forward, in a design without aliases, and it is the model from which the "
                            "ranges and the design space are predicted."))])
    nclaim("stats", "variation between manufacturing batches in the prediction interval", "The single-run prediction "
           "interval includes neither the variation between manufacturing batches beyond the scatter between runs of "
           "the scale-down model nor the uncertainty of the offset.",
           [("stats", q("It does not include variation between manufacturing batches beyond that scatter, and it does "
                        "not include the uncertainty of the offset, which the qualification handles (@sec-sdm)."))],
           elsewhere="the qualification of the scale-down model")
    nclaim("stats", "correction for multiple univariate tests", "No correction for the number of univariate tests is "
           "applied.",
           [("univariate", q("No correction for the number of tests is applied, because none was set before the "
                             "result."))],
           rationale="None was set before the result.")
    nclaim("factors", "change of set-points or NORs at Version 2.0", "No NOR and no set-point of the step was changed "
           "at Version 2.0.",
           [("factors", q("No NOR and no set-point of this step was changed at Version 2.0."))])
    nclaim("osmolality", "effect of osmolality on acidic variants at the least favourable combination",
           "The osmolality study shows no significant effect of osmolality on acidic variants at the combination it "
           "tested, the fitted mean at the NOR high is not a finding, and the study does not give the interactions of "
           "osmolality with the other parameters.",
           [("osmolality", q("The study therefore shows no significant effect of osmolality on acidic variants at this "
                             "combination, and the fitted mean at the NOR high is not a finding.")),
            ("osmolality", q("It ran at that single combination, with osmolality set by sodium chloride independently of "
                             "pCO2, so it does not give the interactions of osmolality with the other parameters."))])
    nclaim("ds", "design space beyond the ranges studied", "The design space is conditioned on osmolality and the "
           "univariate parameters at their set-points, is not claimed beyond the ranges studied and is not confirmed at "
           "commercial scale at its edges.",
           [("ds", q("Osmolality and the `{python} words(len(UNI))` univariate parameters are held at their set-points, "
                     "so the design space is conditioned on them, and it is not claimed beyond the ranges studied.")),
            ("ds", q("The design space rests on the scale-down model and is not confirmed at commercial scale at its "
                     "edges."))])
    nclaim("criteria", "in-process test of aggregate", "No in-process test of aggregate exists at the step, so no batch "
           "fails there; the risk of the tighter criterion falls on the producer at release.",
           [("criteria", q("No in-process test of aggregate exists at this step, so no batch fails here, and the risk of "
                           "the tighter criterion falls on the producer at release, where SEC tests aggregate in the drug "
                           "substance against the limit of `{python} pct(DS_AGG, 1)` and detects an excursion."))],
           elsewhere="release testing of the drug substance by SEC")
    nclaim("par", "effect of the osmolality rise with pCO2 at scale", "The PAR of pCO2 for acidic variants does not "
           "include the effect of the rise of osmolality that comes with pCO2 at scale.",
           [("par", q("The PAR of pCO2 for acidic variants therefore does not include the effect of the osmolality rise "
                      "that comes with it at scale.")),
            ("pd06", q("Because osmolality was set independently of pCO2, the screening design and the osmolality study "
                       "estimate the two effects separately, and the PAR of pCO2 does not include the rise of osmolality "
                       "that comes with pCO2 at scale (@sec-par-table)."))])
    nclaim("par_uni", "PAR of osmolality", "Osmolality has no PAR from a model, and no range of osmolality beyond its NOR "
           "is claimed.",
           [("par_uni", q("Osmolality has no PAR from a model, because it was not a factor of the response-surface "
                          "design.")),
            ("par_uni", q("The osmolality study supports its NOR for every attribute except acidic variants, at the "
                          "single combination of the other parameters that it tested, and no range of osmolality beyond "
                          "its NOR is claimed."))],
           rationale="Osmolality was not a factor of the response-surface design.")
    nclaim("par_uni", "support of the initial viable cell concentration range at the least favourable combination",
           "The range of the initial viable cell concentration is not supported with the other parameters at their least "
           "favourable NOR settings for acidic variants.",
           [("par_uni", q("For the initial viable cell concentration the support does not extend to the other parameters "
                          "at their least favourable NOR settings for acidic variants (@sec-univariate)."))])
    nclaim("cap", "effect of the initial viable cell concentration in the capability", "The capability of acidic variants "
           "does not include the effect of the initial viable cell concentration found in the univariate study, and "
           "the verdict over the NOR does not include it either.",
           [("cap", q("It carries no effect of the initial viable cell concentration on acidic variants, so the "
                      "capability does not include the effect found in the univariate study.")),
            ("pd11", q("The verdict over the NOR and the capability of this report do not include the effect."))])
    nclaim("control", "edges of the ranges at commercial scale", "Process performance qualification runs the process at "
           "its set-points and does not test the edges of the ranges.",
           [("control", q("It confirms the process at scale near the centre of the NOR and does not test the edges of the "
                          "ranges."))], elsewhere="PPQ at the receiving site under PTP-001")
    nclaim("mech", "mechanistic explanation of the directions of four effects", "The mechanism of Section 2.1 does not "
           "explain the direction of the effect of culture duration on afucosylation, of pCO2 on galactosylation, "
           "afucosylation and acidic variants, or of culture pH on acidic variants, and does not account for the effect "
           "of the initial viable cell concentration on acidic variants.",
           [("mech", q("The mechanism of @sec-platform therefore does not explain the direction of the effect of culture "
                       "duration on afucosylation, of pCO2 on galactosylation, afucosylation and acidic variants, or of "
                       "culture pH on acidic variants, and it does not account for the effect of the initial viable cell "
                       "concentration on acidic variants (@sec-univariate)."))])
    nclaim("changes", "deviations", "The report records no deviation: a process characterization study is not GMP "
           "manufacture, so the events of execution are study events and every departure from PCP-003 is a "
           "discrepancy from the plan.",
           [("changes", q("A process characterization study is not GMP manufacture, so this report records them as "
                          "study events, and every departure from PCP-003 as a discrepancy from the plan."))])
    nclaim("pd09", "viable cell density, viability and titre", "Viable cell density, viability and titre are not in the "
           "record, and no criterion of the report depends on them.",
           [("pd09", q("The monitoring records cannot be recovered.")),
            ("pd09", q("No criterion of this report depends on these outputs."))])

    # -- the control strategy the step contributes (Section 10): eight elements, three of them recommendations ----
    src_all = _source()
    cs_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n# Contribution to the control strategy", 1)[1]
                         .split("\n# ", 1)[0], flags=re.M)
    if len(cs_list) != 8:
        raise ValueError(f"{DOC}: {len(cs_list)} numbered elements of the control strategy, the report has eight")
    MIT = ns["MIT"]
    cs_meta = [("process parameters", "process control (bioreactor control system)"),
               ("culture pH, pCO2 and culture temperature (acidic variants)", "combined alert in the control system "
                                                                              "(recommendation)"),
               ("acidic variants at harvest", f"action limit at harvest by icIEF ({MIT['method']}) (recommendation)"),
               ("acidic variants at harvest against the initial viable cell concentration", "trending (recommendation)"),
               ("key process parameters", "process control and mass reconciliation"),
               ("quality attributes the step sets", "specification (release testing of the drug substance)"),
               ("host cell protein and residual DNA", "downstream clearance"),
               ("process at commercial scale", "process performance qualification")]
    cs_els = []
    for i, (item, (ctl, ctype)) in enumerate(zip(cs_list, cs_meta), 1):
        sent = re.split(r"(?<=\.) (?=[A-Z`])", item)
        cs_els.append(ControlStrategyElement(
            element_id=f"{DOC}-CS{i:02d}", description=re.sub(r"\s+([,.;:)])", r"\1", render(item)),
            unit_operation=UO_NAME, controls=ctl, control_type=ctype,
            source_references=[ref("control", q(sent[0]))], metadata=meta()))

    entities = [
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("exec"), process_steps=[step], sites=sites),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("product"), equipment=equipment[:1],
                                  document_relationships=rels),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("changes"), non_claims=nc_at["changes"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("platform"), non_claims=nc_at["platform"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cqa"), quality_attributes=attrs,
                                  non_claims=nc_at["cqa"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("risk"), non_claims=nc_at["risk"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("sdm"), equipment=equipment[1:],
                                  non_claims=nc_at["sdm"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("operation"), non_claims=nc_at["operation"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("analytical"), analytical_methods=methods),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("stats"), non_claims=nc_at["stats"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("factors"), parameters=params,
                                  non_claims=nc_at["factors"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("models"), model_fits=fits),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("osmolality"), non_claims=nc_at["osmolality"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("mech"), non_claims=nc_at["mech"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("ds"), non_claims=nc_at["ds"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("criteria"), non_claims=nc_at["criteria"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("par"), non_claims=nc_at["par"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("par_uni"), non_claims=nc_at["par_uni"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cap"), capabilities=capab,
                                  non_claims=nc_at["cap"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("control"), control_strategy=cs_els,
                                  non_claims=nc_at["control"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("record"), deviations=devs),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("pd09"), non_claims=nc_at["pd09"]),
    ]

    # ==== studies: each on its row of the execution-window table, its prose, its data rows and the rows of the
    # discrepancy register that record it ==========================================================================
    CH = ns["CH"]
    pd_of = {}
    for d in P.PLAN_DISCREPANCIES[DOC]:
        for s_ in (d.get("studies") or []):
            pd_of.setdefault(s_, []).append(d["id"])
    pd_of.setdefault("S-BRX-UNI", []).extend(["PD-003-05", "PD-003-10"])
    for s_ in ("S-BRX-OSM", "S-BRX-AUG"):
        pd_of.setdefault(s_, []).append("PD-003-12")
    fac_names = {k: PRM[k].name for k in PRM}
    study_spec = {
        "S-BRX-SDM": dict(study_type="scale_down_qualification",
                          design_name="set-point runs of the scale-down model against manufacturing-scale batches",
                          responses=list(RESPS),
                          prose=[("sdm", q("The qualification study S-BRX-SDM (`{python} win('S-BRX-SDM')`) followed the "
                                           "scale-down model procedure SOP-1001.")),
                                 ("sdm", q("It compared `{python} words(N_SDM_SD)` runs of the scale-down model at the "
                                           "set-points with `{python} words(N_SDM_M)` manufacturing-scale batches of the "
                                           "A-Mab engineering and clinical campaigns."))],
                          rows=[("sdm", r_, so_t, sorow) for r_ in sorow.values()]
                          + [("analytical", soprow["SOP-1001"], sop_t, soprow)]),
        "S-BRX-SCR": dict(study_type="screening_doe",
                          design_name="resolution V half fraction of the two-level factorial design, with centre points",
                          factors=[fac_names[k] for k in SFS], responses=list(RESPS) + ["hcp", "residual_dna"],
                          n_runs=P.doe_runs(UO, "screening"), n_center_points=P.doe_centre_points(UO, "screening"),
                          prose=[("scr_design", q("The screening study S-BRX-SCR varied the `{python} words(len(SFS))` "
                                                  "multivariate parameters in a resolution V half fraction of the "
                                                  "two-level factorial design, with `{python} N_SCR - NC_SCR` factorial "
                                                  "runs and `{python} words(NC_SCR)` centre points, `{python} N_SCR` runs "
                                                  "in all.")),
                                 ("scr_design", q("At resolution V every main effect and every two-factor interaction can "
                                                  "be estimated clear of the others, and each is aliased only with "
                                                  "interactions of three factors or more."))],
                          rows=[("app_a", r_, mtx["screening"][0], mtx["screening"][1])
                                for r_ in mtx["screening"][1].values()]),
        "S-BRX-UNI": dict(study_type="univariate",
                          design_name="one factor at a time, both ends of the range studied in duplicate, the other "
                                      "parameters at their set-points",
                          factors=[fac_names[k] for k in UNI], responses=list(RESPS) + ["hcp", "residual_dna"],
                          prose=[("uni_design", q("The univariate study S-BRX-UNI (`{python} win('S-BRX-UNI')`) assessed "
                                                  "`{python} join_and(['dissolved oxygen', 'initial viable cell "
                                                  "concentration', 'basal medium concentration', 'nutrient feed-1 "
                                                  "volume'])` one at a time.")),
                                 ("uni_design", q("Duplicate runs were made at each end, `{python} len(UV)` runs in all, "
                                                  "to measure the variation between runs within the study "
                                                  "(PD-003-05)."))],
                          rows=[("univariate", r_, uv_t, uvrow) for r_ in uvrow.values()]),
        "S-BRX-RSM": dict(study_type="response_surface_doe", design_name="face-centred central composite design",
                          factors=[fac_names[k] for k in FS], responses=list(RESPS) + ["hcp", "residual_dna"],
                          n_runs=P.doe_runs(UO, "rsm"), n_center_points=P.doe_centre_points(UO, "rsm"),
                          prose=[("rsm_design", q("The response-surface study S-BRX-RSM varied "
                                                  "`{python} join_and([pname(k) for k in FS])` in a face-centred central "
                                                  "composite design.")),
                                 ("rsm_design", q("The design has `{python} N_FACT` factorial runs, `{python} N_AXIAL` "
                                                  "axial runs at the centres of the faces of the design cube and "
                                                  "`{python} words(NC_RSM)` centre points, `{python} N_PLAN` runs in "
                                                  "all."))],
                          rows=[("app_b", r_, mtx["rsm"][0], mtx["rsm"][1]) for r_ in mtx["rsm"][1].values()]),
        "S-BRX-OSM": dict(study_type="univariate",
                          design_name=t("osmolality at its NOR low, set-point and NOR high, `{python} words(OSM_N)` runs "
                                        "at each level, with the response-surface parameters at their least favourable "
                                        "NOR combination for acidic variants"),
                          factors=[fac_names["osmolality"]], responses=list(RESPS),
                          prose=[("osm_design", q("The osmolality study S-BRX-OSM (`{python} win('S-BRX-OSM')`) ran "
                                                  "osmolality at its NOR low, set-point and NOR high.")),
                                 ("osm_design", q("The study was made during the Version 2.0 re-analysis, after the "
                                                  "screening and response-surface results were known, and it is "
                                                  "recorded as the discrepancy PD-003-01."))],
                          rows=[("osmolality", r_, os_t, osrow) for r_ in osrow.values()]),
        "S-BRX-AUG": dict(study_type="response_surface_doe",
                          design_name=t("D-optimal augmentation of `{python} N_AUG` runs, executed as a second block of "
                                        "the face-centred central composite design"),
                          factors=[fac_names[k] for k in FS], responses=list(RESPS),
                          prose=[("rsm_design", q("The design was augmented with `{python} N_AUG` runs under INV-002, in "
                                                  "a D-optimal augmentation run as a second block, the study S-BRX-AUG "
                                                  "(`{python} win('S-BRX-AUG')`)")),
                                 ("rsm_design", q("INV-002 decided its rule on `{python} MA['decided']`, after the results "
                                                  "of the planned runs were known and before any augmentation run was "
                                                  "made."))],
                          rows=[("app_b", r_, mtx["aug"][0], mtx["aug"][1]) for r_ in mtx["aug"][1].values()]),
    }
    studies, unrendered = [], []
    for sid_, r in CH.iterrows():
        if r["step"] != UO:
            continue
        if sid_ not in chrow or not G._present(chrow[sid_], text):
            unrendered.append(sid_)
            continue
        spec = dict(study_spec[sid_])
        prose_, rows_ = spec.pop("prose"), spec.pop("rows")
        refs = [ref("chronology", chrow[sid_], ch_t, chrow)]
        refs += [ref(s_, x) for s_, x in prose_]
        refs += [ref(s_, r_, tab_, rr_) for s_, r_, tab_, rr_ in rows_]
        refs += [pdref(p_) for p_ in pd_of.get(sid_, [])]
        studies.append(S.StudyDesign(
            study_id=f"study:{sid_}", unit_operation=UO_NAME, scale_down_model=SDM_NAME,
            associated_parameters=[PC[pkey_of_name[x]] for x in spec.get("factors", [])],
            source_references=refs, metadata=meta(), **spec))

    # ==== design space and the proven acceptable ranges ============================================================
    DSG = ns["DSG"]
    q_ds = [q("The design space of this step is the region of the `{python} words(len(FS))` response-surface parameters "
              "over which every modelled attribute meets its intermediate acceptance criterion."),
            q("It is judged on the 95 % prediction interval of a single run at manufacturing scale, as PCMP-001 §6.2 "
              "requires."),
            q("A setting lies inside it when both ends of that interval lie within the criterion of every attribute."),
            q("On the grid of `{python} f\"{DSG['n_points']:,}\"` points, `{python} pct(100 * DSG['fraction'])` of the "
              "region studied lies inside the design space."),
            q("Its boundary is set by the lower limit of acidic variants, which excludes "
              "`{python} pct(100 * DSG['per_response']['acidic_variants'])` of the grid points."),
            q("Galactosylation excludes `{python} pct(100 * DSG['per_response']['galactosylation'])` and afucosylation "
              "`{python} pct(100 * DSG['per_response']['afucosylation'])`, and high mannose and aggregate exclude "
              "none.")]
    design_spaces = [S.DesignSpace(
        design_space_id="ds:bioreactor", unit_operation=UO_NAME, parameters=[PC[k] for k in FS],
        quality_attributes_constrained=[f"attr:{r}" for r in RESPS if DSG["per_response"][r] > 0],
        definition=t("The region of culture pH, culture temperature, culture duration and pCO2 over which every modelled "
                     "attribute meets its intermediate acceptance criterion, judged on the 95 % prediction interval of a "
                     "single run at manufacturing scale (both ends of the interval within the criterion of every "
                     "attribute), with osmolality and the univariate parameters at their set-points and not claimed "
                     "beyond the ranges studied. On a grid of `{python} f\"{DSG['n_points']:,}\"` points, "
                     "`{python} pct(100 * DSG['fraction'])` of the region studied lies inside it. Its boundary is set by "
                     "the lower limit of acidic variants, which excludes "
                     "`{python} pct(100 * DSG['per_response']['acidic_variants'])` of the grid points; galactosylation "
                     "excludes `{python} pct(100 * DSG['per_response']['galactosylation'])` and afucosylation "
                     "`{python} pct(100 * DSG['per_response']['afucosylation'])`, and high mannose and aggregate none. On "
                     "the mean prediction `{python} pct(100 * DSM['fraction'])` of the grid would lie inside. The NOR "
                     "does not lie entirely inside the design space (PD-003-08). The design space rests on the "
                     "scale-down model and is not confirmed at commercial scale at its edges."),
        source_references=[ref("ds", x) for x in q_ds] + [ref("ds", fig_cap("fig-design-space", 1),
                                                                caption=None, label="fig-design-space")],
        metadata=meta())]

    def basis_of(r):
        ia = IAC.loc[r]
        return (f"Intermediate acceptance criterion {T.crit(ia['iac_low'], ia['iac_high'], ia['spec_type'])} % "
                f"({ia['basis']}) of PCMP-001 Version 2.0. PAR, others at set-point: the mean prediction with the "
                f"other factors at their set-points; PAR, others across NOR: the 95 % interval of the simulated runs "
                f"with the other factors drawn across their NORs, the PAR that supports a claim. From the selected "
                f"model of the attribute on all runs, with the offset of the scale-down model applied.")
    PT = ns["PT"]
    pars = []
    for (lab_, pname_), row in parrow.items():
        r, k = lab_key[lab_], pkey_of_name[pname_]
        c = _cells(row)            # Attribute | Criterion | Parameter | Unit | NOR | Required | PAR sp | PAR NOR
        eng = PT[(PT["CQA"] == ns["D"].RESP_LABEL[r]) & (PT["Parameter"] == pname_)].iloc[0]
        if (c[6], c[7]) != (eng["PAR (set-point)"], eng["PAR (NOR)"]):
            raise ValueError(f"{DOC}: the PAR table no longer prints the engine's ranges for {r}, {k}")
        pars.append(S.ProvenAcceptableRange(
            par_id=f"{DOC}-PAR{len(pars) + 1:02d}", unit_operation=UO_NAME, quality_attribute=lab_,
            parameter=pname_, characterization_range=wu(k, eng["Char. range"]),
            par_at_setpoint=wu(k, c[6]), par_nor_propagated=wu(k, c[7]), acceptance_basis=basis_of(r),
            source_references=[ref("par", par_span[(lab_, pname_)], par_t, parrow)], metadata=meta()))

    # ==== assertions ===============================================================================================
    AS = []

    def add(subj, pred, obj, txt, refs):
        AS.append(EvidenceBackedAssertion(
            assertion_id=f"{DOC}-A{len(AS) + 1:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=txt, source_references=refs, metadata=meta()))

    add("step:production_bioreactor", "step_uses_equipment", "equip:sdm_bench",
        f"The studies of the {UO_NAME} were run in {SDM_NAME} of the same design class as the commercial production "
        f"vessel, with the same control scheme.", [ref("sdm", q_sdm)])
    add("step:production_bioreactor", "step_uses_equipment", "equip:production_bioreactor",
        f"The {UO_NAME} is a fed-batch culture with a working volume of {CS} L at commercial scale.",
        [ref("product", q_vessel)])
    add("step:production_bioreactor", "step_uses_equipment", f"equip:{PROBE}",
        f"The pCO2 of each scale-down run was measured by the probe {PROBE} of the scale-down bioreactor system.",
        [ref("sdm", q_probe)])
    for name, row in prow.items():
        k = pkey_of_name[name]
        add("step:production_bioreactor", "step_has_parameter", PC[k],
            f"The {UO_NAME} has process parameter {name}, classified {pdf_.loc[name, 'Class']} and studied "
            f"{pdf_.loc[name, 'Study']}ly.", [ref("factors", row, rows=prow, caption=params_cap, label="tbl-params")])
    for key in ckeys:
        add("step:production_bioreactor", "step_has_quality_attribute", f"attr:{key}",
            f"The CQA register assigns {names[key]} to the {UO_NAME}"
            + ("; it is a modelled response of the designs." if key in RESPS else
               "; it was measured on the clarified harvest for information."),
            [ref("cqa", crow[key], rows=crow, caption=cq_cap, label="tbl-cqa")])
    for key, amv in method_of.items():
        mr = me_by.loc[amv]
        add(f"attr:{key}", "attribute_measured_by_method", f"method:{amv}",
            f"{names[key]} is measured by {mr['Method']} ({amv}, procedure {mr['Procedure']}) in the {mr['Sample']}, "
            f"with a precision of {mr['Precision']}.", [ref("app_d", merow[amv], me_t, merow)])
    for key in RESPS:
        ia, cr = _cells(iacrow[key]), _cells(crrow[key])
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{UO}_{key}_iac",
            f"At the production bioreactor output {aname(key)} {'are' if aname(key).endswith('s') else 'is'} judged "
            f"against the Version {ns['VER']} intermediate "
            f"acceptance criterion {_nomark(ia[4])} % ({_nomark(ia[5])}), derived from the drug substance criterion "
            f"{ia[1]} %; 95 % limits of a single run over the NOR {_nomark(cr[4])} %; met across the NOR: {cr[5]}.",
            [ref("criteria", iacrow[key], iac_t, iacrow), ref("criteria_results", crrow[key], cr_t, crrow)])
    for key in ("hcp", "residual_dna"):
        c = _cells(cprow[cap_label[key]])
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{key}_acc",
            f"{aname(key)[0].upper() + aname(key)[1:]} carries the drug substance criterion {c[2]} "
            f"({reg.loc[key, 'unit']}) and no intermediate "
            f"acceptance criterion at the production bioreactor.",
            [ref("cqa", crow[key], rows=crow, caption=cq_cap, label="tbl-cqa"), ref("cap", cprow[cap_label[key]],
                                                                                     cp_t, cprow)])

    # parameter effects, for the response-surface parameters: one assertion per attribute and parameter, on the span
    # of the PAR table that names both (its "Required by objective 3" cell is the report's statement that the selected
    # model has a significant term in the parameter), the row of the effect-size table and the coefficient row of the
    # main effect where the selected model carries one
    for r in RESPS:
        for k in FS:
            key_ = (ANAME[r], PRM[k].name)
            c = _cells(parrow[key_])
            required = c[5] == "yes"
            if required != bool(SIGT[(r, k)]):
                raise ValueError(f"{DOC}: the PAR table says required={c[5]} for {r}, {k}; the model says otherwise")
            refs = [ref("par", par_span[key_], par_t, parrow)]
            txt = (f"{PRM[k].name} has a significant term in the selected model of {OUT[r]}, so a PAR is required by "
                   f"objective 3" if required else
                   f"{PRM[k].name} has no term in the selected model of {OUT[r]}; its PAR is given for information")
            if (r, k) in ef_by:
                e = _cells(efrow[ef_by[(r, k)]])
                refs.append(ref("effects", efrow[ef_by[(r, k)]], ef_t, efrow))
                txt += (f"; its main effect changes {OUT[r]} by {e[2]} percentage points over the range studied at "
                        f"manufacturing scale, {e[5]} % of the width of the criterion ({e[6]} by the report's own bands)")
            lt = LTR[k]
            if lt in coef[r][0]:
                cc_ = _cells(coef[r][0][lt])
                refs.append(coef_ref(r, lt))
                txt += f"; main-effect coefficient {cc_[1]} in coded units, p {cc_[4]}"
            add(PC[k], "parameter_impacts_attribute" if required else
                "parameter_does_not_significantly_impact_attribute", f"attr:{r}", txt + ".", refs)
    # osmolality: the screening effects and the osmolality study
    OSM_L = LTR["osmolality"]
    q_osm_scr = q("A higher osmolality lowers galactosylation by `{python} fx(abs(eff('galactosylation', OSM_L)))` points "
                  "(p `{python} pfmt(pef('galactosylation', OSM_L))`) and acidic variants by "
                  "`{python} fx(abs(eff('acidic_variants', OSM_L)))` points (p `{python} pfmt(pef('acidic_variants', "
                  "OSM_L))`) across its range, and its interactions with `{python} join_and([_short(INV_LTR[[c for c in t "
                  "if c != OSM_L][0]]) for t in OSM_INT_GA])` are significant for galactosylation.")
    q_osm_af = q("Afucosylation falls by `{python} fx(abs(OSM_CH['afucosylation']))` points across the NOR, with a "
                 "significant slope (p `{python} pfmt(OSM_P['afucosylation'])`), and galactosylation by "
                 "`{python} fx(abs(OSM_CH['galactosylation']))` points (p `{python} pfmt(OSM_P['galactosylation'])`).")
    osm_term = ns["_cap"](ns["tname"]("osmolality"))
    for r in RESPS:
        o = _cells(os_head[r])     # Attribute | Criterion | Change across the NOR (p) | level | mean | PI | meets | meets
        refs = [ref("osmolality", os_head[r], os_t, osrow)]
        scr_sig = (r, osm_term) in scrow
        if scr_sig:
            refs.append(ref("screening", scrow[(r, osm_term)], sc_t, scrow))
            refs.append(ref("screening", q_osm_scr))
        else:
            rows_, cap_, lab_ = scr_tab[r]
            refs.append(ref("app_c", rows_[OSM_L], rows=rows_, caption=cap_, label=lab_))
        osm_sig = r in ns["OSM_SIG"]
        if osm_sig:
            refs.append(ref("osmolality", q_osm_af))
        s_ = _cells((scrow[(r, osm_term)] if scr_sig else scr_tab[r][0][OSM_L]))
        scr_txt = (f"in the screening design osmolality changes {OUT[r]} by {s_[2] if scr_sig else s_[1]} points over "
                   f"its range, p {s_[3] if scr_sig else s_[5]}")
        add(PC["osmolality"], "parameter_impacts_attribute" if (scr_sig or osm_sig) else
            "parameter_does_not_significantly_impact_attribute", f"attr:{r}",
            f"Osmolality on {OUT[r]}: {scr_txt}; in the osmolality study, at the least favourable NOR combination of the "
            f"other parameters for acidic variants, the change across the NOR is {o[2]}"
            + (" (significant slope)." if osm_sig else " (slope not significant)."), refs)
    # the univariate parameters: one assertion per parameter and attribute, on its row of the univariate effects table
    q_ivcc = q("Acidic variants are `{python} fx(UIV_D_MFG)` points higher at the high end of the initial viable cell "
               "concentration than at the low end, with a 95 % confidence interval of ± `{python} fx(UIV_HW_MFG)` "
               "points (p `{python} pfmt(UIV['p'])`).")
    q_only_sig = q("It is the only significant result among the `{python} N_UV_TESTS` univariate tests of "
                   "@tbl-uni-effects.")
    for (pn, an), row in uerow.items():
        k, a = pkey_of_name[pn], lab_key[an]
        c = _cells(row)            # Parameter | Attribute | mean low | mean high | high minus low | CI half-width | p
        sig = c[6].startswith("<") or (_num(c[6]) or 1) < ALPHA
        refs = [ref("univariate", row, ue_t, uerow)]
        if sig:
            refs += [ref("univariate", q_ivcc), ref("univariate", q_only_sig)]
        lab_, unit_ = an.rsplit(" (", 1)
        what = (f"{OUT[a]} (percentage points at manufacturing scale)" if a in RESPS else
                f"{lab_[0].lower() + lab_[1:] if not lab_[:2].isupper() else lab_} in the clarified harvest "
                f"({unit_.rstrip(')')})")
        add(PC[k], "parameter_impacts_attribute" if sig else "parameter_does_not_significantly_impact_attribute",
            f"attr:{a}",
            f"{pn} on {what}: high minus low end of the range studied {c[4]} (95 % confidence half-width {c[5]}), "
            f"p {c[6]}, in the univariate study S-BRX-UNI with the other parameters at their set-points"
            + (", significant at the per-test level; it may be a false positive among the univariate tests."
               if sig else ", not significant."), refs)

    # ==== report statements, grouped by the chapters of the report =================================================
    STS = []

    def clean(s):
        """A rendered span as statement text: the spaces of a cross-reference closed up."""
        s = re.sub(r"\(\s+", "(", s)
        return re.sub(r"\s+([,.;:)])", r"\1", s)

    def st(sec, txt, refs):
        STS.append((SEC[sec][0], ReportStatement(
            statement_id=f"{DOC}-S{len(STS) + 1:03d}", statement_text=txt, confidence="high",
            review_status="accepted", source_references=refs)))

    def sq(sec, src, txt=None, extra=()):
        """A statement of one prose span: ``src`` is the .qmd source of the span, ``txt`` the statement where it is
        not the span itself, ``extra`` further ``(section, source)`` spans a paraphrase draws on."""
        st(sec, t(txt) if txt else clean(q(src)), [ref(sec, q(src))] + [ref(s_, q(x)) for s_, x in extra])

    def sqs(sec, *srcs):
        for s_ in srcs:
            sq(sec, s_)

    def srow(sec, txt, row, tab=None, rows_=None, caption=None, label=None):
        """A statement of one rendered row."""
        st(sec, txt, [ref(sec, row, tab, rows_, caption=caption, label=label)])

    # -- Executive summary ----------------------------------------------------------------------------------------
    sqs("exec",
        "This is Version `{python} VER` of the report.",
        "The scale-down model was compared with manufacturing scale in `{python} words(N_SDM_SD)` runs at the set-points "
        "against `{python} words(N_SDM_M)` manufacturing-scale batches.",
        "A screening design of `{python} N_SCR` runs varied the `{python} words(len(SFS))` parameters assigned to "
        "multivariate study, and a face-centred response-surface design of `{python} N_PLAN` runs then varied "
        "`{python} words(len(FS))` of them.",
        "Under INV-002, `{python} N_AUG` runs were added to the response-surface design as a second block, after the "
        "results of the planned runs were known.",
        "A univariate study varied the other `{python} words(len(UNI))` parameters one at a time.",
        "An osmolality study, made during the Version 2.0 re-analysis, varied osmolality with the other parameters at "
        "the combination of NOR settings least favourable for acidic variants.",
        "The response-surface model of each of the `{python} words(len(RESPS))` modelled attributes was selected on all "
        "`{python} N_ALL` runs, by the model selection that INV-002 adopted as its corrective action CA3.",
        "The scale comes from the Box-Cox profile, and the model is the one with the lowest AICc among all hierarchical "
        "submodels of the full quadratic.",
        "Every selected model meets the first three adequacy criteria of PCMP-001 §7.2, a significant model F-test, no "
        "significant lack of fit and predicted R² within `{python} fx(GAPMAX)` of R².")
    sq("exec", "For `{python} join_and([OUT[r] for r in RI_FAIL])` the absolute residuals rise with the predicted value, "
               "so these two models do not meet the fourth criterion, on residuals and influential runs.",
       extra=[("exec", "They were used with that trend sized against their criteria (PD-003-04).")])
    sqs("exec",
        "With each run flagged by its Cook's distance deleted in turn, every attribute kept its verdict over the normal "
        "operating range (NOR), and every proven acceptable range (PAR) still contained the NOR.",
        "Each attribute was judged on the 95 % prediction interval of a single run, at manufacturing scale, at every "
        "combination of NOR low, set-point and NOR high.",
        "Afucosylation, galactosylation, high mannose and aggregate meet their intermediate acceptance criteria.")
    sq("exec", "At `{python} words(N_FAIL_COMB)` of the `{python} N_NORCOMB` combinations, all with pCO2 at its NOR "
               "high, the interval reaches below the lower limit of `{python} pct(ACC['acidic_variants'][0])`.",
       "Acidic variants do not meet their intermediate acceptance criterion: at `{python} words(N_FAIL_COMB)` of the "
       "`{python} N_NORCOMB` combinations, all with pCO2 at its NOR high, the 95 % prediction interval of a single run "
       "reaches below the lower limit of `{python} pct(ACC['acidic_variants'][0])`.")
    sqs("exec",
        "At the least favourable combination the predicted median is `{python} pct(WCA['predicted'])`, a margin above "
        "the limit smaller than the bias of the model at the set-point, and about `{python} pct(WCA_IV_MED)` with the "
        "initial viable cell concentration at its NOR low.",
        "The NOR was not narrowed.",
        "The risk was accepted as the producer's.",
        "This report recommends a combined alert in the control system, which fires when `{python} ALERT_TXT` at the "
        "same time.",
        "It also recommends an action limit for acidic variants at harvest of `{python} pct(MIT['action_limit'], 2)`, "
        "and the trending of acidic variants against the initial viable cell concentration in production "
        "(@sec-control).",
        "All `{python} N_PAR` PARs computed with the other parameters varying across their NORs contain the NOR, and "
        "`{python} N_PAR - len(NARROW)` of them span the whole range studied.",
        "That every PAR contains the NOR rests on the `{python} N_AUG` augmentation runs and on the model selection.",
        "On the `{python} N_PLAN` planned runs alone, the PARs of culture pH, culture temperature and pCO2 for acidic "
        "variants do not contain it.",
        "The design space covers `{python} pct(100 * DSG['fraction'])` of the region studied, and its boundary is set "
        "by the lower limit of acidic variants.",
        "Culture pH, culture temperature, pCO2 and culture duration were classified as well-controlled critical process "
        "parameters (WC-CPPs).",
        "The initial viable cell concentration, basal medium concentration and nutrient feed-1 volume were classified as "
        "key process parameters (KPPs), and dissolved oxygen as a general process parameter (GPP).",
        "In the integrated model of the train the capability index of acidic variants in the drug substance is a Cpk of "
        "`{python} fx(ACAP.Cpk)`, between the minimum of `{python} fx(CPK_MIN)` and the target of "
        "`{python} fx(CPK_TARGET)`, and every other attribute that the step sets has a Cpk above the target.",
        "That model simulates manufacturing scale directly and carries no effect of the initial viable cell "
        "concentration on acidic variants (@sec-capability).",
        "The record of the step holds `{python} words(N_DEV)` study events and `{python} N_PD` discrepancies from the "
        "plan (@sec-record).",
        "Seven of the discrepancies are requirements of PCP-003 that the Version 2.0 re-analysis found unmet, among them "
        "the multivariate study that the univariate effect of the initial viable cell concentration on acidic variants "
        "calls for (PD-003-11).")

    # -- Introduction ------------------------------------------------------------------------------------------------
    sqs("product",
        "A-Mab is a humanized IgG1 monoclonal antibody whose main mechanism of action is antibody-dependent cellular "
        "cytotoxicity (ADCC).",
        "The production bioreactor is Step 3 of the drug substance process.",
        # D-002, recorded as the document states it
        "The production bioreactor is the only step of the A-Mab drug substance process at which product quality "
        "attributes are formed.",
        "Cation and anion exchange separate by net charge, and core fucose, galactose and mannose carry none, so no "
        "purification step retains one neutral glycoform in preference to another (PCP-003 §4.1).",
        "The neutral glycoforms of the drug substance are therefore those of the harvest.",
        "They are set mainly in the Golgi before secretion, and glycosidases released by lysed cells can trim them "
        "further in the culture fluid.",
        "Acidic variants form in the cell and in the culture fluid, mainly as asparagine deamidates, and aggregate forms "
        "as antibody molecules associate in the culture fluid.",
        "Both rise with the time the antibody spends at culture temperature.",
        "Host cell protein and DNA enter the culture fluid when cells die and lyse, so their load at harvest rises as "
        "viability falls late in the culture.")
    obj_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n## Objectives", 1)[1].split("\n## ", 1)[0], flags=re.M)
    if len(obj_list) != 5:
        raise ValueError(f"{DOC}: {len(obj_list)} numbered objectives under '## Objectives', the report has five")
    sq("objectives", "PCP-003 §2 sets the following objectives, and @sec-conclusions states the result against each.")
    for i, obj in enumerate(obj_list, 1):
        st("objectives", f"Objective {i} of PCP-003 §2: {clean(q(obj))}", [ref("objectives", q(obj))])
    sqs("regulatory",
        "They follow the enhanced approach of ICH Q8(R2) and ICH Q11.",
        "ICH Q8(R2) defines the design space and the proven acceptable range, and it treats the criticality of an "
        "attribute as a continuum.")
    st("regulatory", "The model selection uses the Box-Cox transformation and Akaike's information criterion with the "
                     "small-sample correction (AICc), and the augmentation of the response-surface design is D-optimal.",
       [ref("regulatory", q("The model selection uses the Box-Cox transformation and Akaike's information criterion with "
                            "the small-sample correction (AICc), and the augmentation of the response-surface design is "
                            "D-optimal"))])
    sqs("changes",
        "Version 1.0 of this report was approved on `{python} rev1_date(DOC)`.",
        "QA opened the investigation INV-001 on `{python} INV['opened']` after its review of the master report PCMR-001 "
        "Version 1.0 for BLA readiness, and closed it on `{python} INV['closed']` with the classification "
        "`{python} INV['classification']`.",
        "The investigation found that the criteria used to judge each step in the analysis of the proven acceptable "
        "ranges were in no approved protocol and had been set after the data were seen (INV-001 finding 1).",
        "For this step, the Version 1.0 limits of the glycans and acidic variants were the mean plus `{python} R1K` "
        "standard deviations of the capability data they were then used to judge (finding 3).",
        "The Version 1.0 aggregate limit was the drug substance limit, back-calculated through the nominal downstream "
        "clearance of this campaign and divided by a margin of `{python} R1M` (finding 2).",
        """Acidic variants carry the two-sided drug substance criterion of `{python} f"{DS_ACID[0]:g}–{DS_ACID[1]:g}"` %, and Version 1.0 assessed their capability against its upper end alone and judged their ranges against an upper limit alone, `{python} f"≤ {R1C.loc['acidic_variants', 'high']:.1f}"` % (finding 4).""",
        "The records gave no execution dates (finding 5).",
        "The second investigation, INV-002, was opened on `{python} INV2['opened']` and closed on "
        "`{python} INV2['closed']` with the classification `{python} INV2['classification']`.",
        "It found that the full quadratic models of `{python} join_and([OUT[r] for r in AUGR])` on the planned runs did "
        "not meet the limit on overfitting of PCMP-001 §7.2.")
    sq("changes", "Each output is judged against an intermediate acceptance criterion that PCMP-001 Version 2.0 derives "
                  "a priori from the drug substance criterion and the platform worst case of every downstream step "
                  "(@tbl-criteria-change).",
       extra=[("changes", "The Version 1.0 limits were applied at analysis and appeared in no approved plan.")])
    sqs("changes",
        "Every upper limit in force is higher than the Version 1.0 limit, and acidic variants now carry a lower limit of "
        "`{python} pct(ACC['acidic_variants'][0])`.",
        "Verification of the platform worst cases tightened the aggregate criterion and then widened it, to "
        "`{python} pct(AGG.iac_high, 2)` against `{python} pct(AGG.iac_high_apriori, 2)` a priori (@sec-criteria).",
        "Acidic variants are judged against both limits of their criterion, and their capability is assessed against "
        "both (@sec-capability).",
        "The scale-down model is qualified for each output by its offset from manufacturing scale, and every result "
        "judged against a criterion is stated at manufacturing scale (@sec-sdm).",
        "Every response-surface output is analysed by model selection on all runs of the design, with a block term "
        "(PD-003-03).",
        "The design was augmented by `{python} N_AUG` runs under INV-002 (PD-003-02).",
        "The osmolality study S-BRX-OSM was made during the re-analysis (PD-003-01).",
        "The execution window of every study is recorded, and for every study of PCP-003 the calibration status of the "
        "pCO2 probe (@sec-chronology).",
        "The results for host cell protein and DNA in the clarified harvest, which PCP-003 requires and Version 1.0 did "
        "not report, are given for information (@sec-sampling).")
    sq("changes", "The description of the control of culture pH is corrected.",
       "The description of the control of culture pH is corrected: Version 1.0 gave it as control by carbon dioxide and "
       "base addition, but carbon dioxide cannot set the pH where pCO2 is a factor of the designs.",
       extra=[("changes", "Version 1.0 gave it as control by carbon dioxide and base addition, but carbon dioxide cannot "
                          "set the pH where pCO2 is a factor of the designs (@sec-operation).")])
    sqs("changes",
        "Version 1.0 recorded the events of execution as deviations.",
        "The departures that the Version 2.0 re-analysis found are PD-003-07 to PD-003-13 (@sec-record).",
        "The Version 1.0 analysis judged the full quadratic models of the planned runs against the Version 1.0 limits.",
        "Judged so, `{python} len(REV1_OUT)` of the `{python} N_PAR` NOR-propagated PARs do not contain the NOR, and each "
        "of the `{python} words(len(REV1_OUT_R))` attributes has at least one such PAR.",
        "Judged against the criteria in force, the same models give the PAR of pCO2 for acidic variants as "
        "`{python} D._par_str(CO2_V1)` mmHg, short of the NOR high, as INV-001 reports.",
        "The PARs of this report come from the selected models on all runs (@sec-augmentation).",
        "The lower limit of acidic variants, which Version 1.0 did not apply, is the one criterion not met across the "
        "NOR (@sec-criteria-results).")

    # -- Prior knowledge and quality risk basis ----------------------------------------------------------------------
    sqs("platform",
        "Cell line construction, basal medium, feed strategy and the control of pH, temperature and dissolved oxygen are "
        "common to these products.",
        "The directions of the effects seen on the platform are carried into this study as expectations.",
        "Their sizes are not, and the fitted models of this study give them.",
        "Core fucose is added by a fucosyltransferase from GDP-fucose.",
        "The fraction of antibody secreted without core fucose therefore rises when the activity of that enzyme falls, "
        "when the donor is depleted or when the glycan spends less time in the Golgi.",
        "Terminal galactose is added by a galactosyltransferase from UDP-galactose.",
        "The donor and the manganese cofactor of the enzyme are depleted late in a fed-batch culture, so "
        "galactosylation is expected to fall as the culture ages.",
        "High mannose glycans remain when processing stops early, so their level rises when transit through the Golgi "
        "is fast relative to the processing enzymes or when those enzymes are inhibited.",
        "The harvested pool contains everything secreted during the run, so a longer culture weights it toward antibody "
        "made late, under depleted conditions.",
        "A higher culture pH raises the pH inside the cell and in the Golgi.",
        "A higher culture temperature raises the growth rate and the rate of every enzymatic and chemical reaction.",
        "Dissolved carbon dioxide forms bicarbonate and lowers the pH in the cytosol, so a higher pCO2 is expected to "
        "move each glycan in the direction opposite to a higher culture pH.",
        "A higher osmolality draws water out of the cell, slows its growth and changes the size of the nucleotide sugar "
        "pools.",
        "These four parameters act on the same enzymes and donor pools, so the effect of one on a glycan is expected to "
        "depend on the levels of the others (PCP-003 §4.1).",
        "Aggregate forms after secretion, while the antibody sits in the culture fluid at culture temperature.",
        "A culture pH closer to the isoelectric point raises it, because the net charge of the antibody falls and the "
        "repulsion between molecules weakens.",
        "Acidic variants are mainly products of asparagine deamidation, together with sialylated glycans and glycated "
        "lysines.",
        "Deamidation speeds up at a higher temperature and a higher pH.",
        "These routes do not respond to a parameter in the same direction, so the net direction of each parameter on "
        "acidic variants is read from the data.",
        "Dissolved oxygen supplies the oxygen for oxidative metabolism, and the culture is not expected to be limited by "
        "oxygen at either end of the range studied, so neither growth nor the glycans are expected to move across it.",
        "A higher initial viable cell concentration brings the culture to its peak viable cell density earlier and "
        "leaves more days in the productive phase, which raises the titre.",
        "A higher basal medium concentration and a larger nutrient feed-1 volume raise the supply of glucose, amino "
        "acids and nucleotide sugar precursors, which raises growth and titre.",
        "PCP-003 §4.1 expects none of these `{python} words(len(UNI))` parameters to move a glycan attribute at a fixed "
        "culture age within the ranges studied.")
    sqs("cqa",
        "@tbl-cqa lists the `{python} words(len(KEYS))` quality attributes that the drug substance CQA register assigns "
        "to the production bioreactor.",
        "The levels run from very low (VL) to very high (VH), and the attributes of high (H) and very high criticality "
        "are called critical.",
        "For this step the critical attributes are `{python} join_and([OUT[k] for k in CRIT_K])`.",
        "The `{python} words(len(RESPS))` modelled responses of the designs are afucosylation, galactosylation, high "
        "mannose, acidic variants and aggregate.",
        """A dose is `{python} f"{DOSE_MGKG:g}"` mg/kg, given weekly in A-Mab, for a reference adult of `{python} f"{DOSE_KG:g}"` kg, an assumption of this campaign.""")
    st("cqa", t("""The criterion of residual DNA, ≤ `{python} f"{DNA_CRIT:g}"` ng per dose, is the acceptable range that the A-Mab case study claims, which is met through the clearance of the purification train."""),
       [ref("cqa", q("""Its criterion, ≤ `{python} f"{DNA_CRIT:g}"` ng per dose, is the acceptable range that the A-Mab case study claims, which is met through the clearance of the purification train"""))])
    sqs("risk",
        "Parameters ranked high, or with a likely interaction, were assigned to multivariate study, and the others to "
        "univariate study (PCMP-001 §4).",
        "For the production bioreactor `{python} words(len(MV))` of the `{python} words(len(PRM))` parameters were "
        "assigned to multivariate study, namely `{python} join_and([pname(k) for k in MV])`.",
        "The effect of one is therefore expected to depend on the levels of the others, and only a design that varies "
        "them together can estimate that dependence.",
        "Dissolved oxygen, initial viable cell concentration, basal medium concentration and nutrient feed-1 volume were "
        "assigned to univariate study, because none of them is expected to move a glycan attribute at a fixed culture "
        "age (@sec-platform).",
        """The range studied of every parameter extends beyond its NOR at both ends, and it is between `{python} f"{min(RATIO):.1f}"` and `{python} f"{max(RATIO):.1f}"` times as wide as the NOR.""",
        "The wider range shows how each attribute responds beyond the edges of routine operation, and it sets the "
        "knowledge space within which a PAR can be claimed.")

    # -- Materials and methods ---------------------------------------------------------------------------------------
    sqs("sdm",
        "Parameters that do not depend on scale were run at the commercial set-points.",
        "A large vessel strips carbon dioxide less efficiently than a bench-scale vessel, so pCO2 was controlled to the "
        "level of each run and studied as a factor, over a range that spans the levels the commercial vessel reaches "
        "(PCP-003 §5.1).",
        "A scale-down model need not reproduce the manufacturing mean, provided the difference is known well enough "
        "that no conclusion depends on its exact size (PCMP-001 §7.1).",
        "The offset of an output is the mean of the scale-down runs minus the mean of the manufacturing batches, with "
        "its two-sided `{python} OFF_CI` % confidence interval.",
        "Every result of the scale-down studies that is judged against a criterion has the offset applied, so ranges "
        "and verdicts are stated at manufacturing scale.",
        "The model is qualified for an output when the verdict over the NOR, whether the output meets its criterion at "
        "every combination of NOR settings, is the same with the offset at either end of its interval.",
        "Acidic variants fail their criterion over the NOR with the offset at its estimate and at either end of its "
        "interval, so that verdict does not depend on the offset either.",
        """Only for aggregate does the interval exclude a ratio of 1, and the scale-down model gives about `{python} f"{AGG_OFF_PCT:.0f}"` % less aggregate than manufacturing scale.""",
        "PCP-003 Version 1.0 compared the means of the two scales by a test of no difference at that point, so the "
        "difference of the means was known before the first characterization run.",
        "The confidence intervals of @tbl-sdm-offsets and the decision whether the model is qualified for each output "
        "were computed at analysis, as PCMP-001 §7.1 allows.",
        "The viable cell density, the viability at harvest and the titre, which PCP-003 §5.1 also lists among the "
        "outputs compared, are not in the record of the qualification or of any characterization run (PD-003-09).",
        "The offset was estimated at the set-points only, and its use across the range studied is an assumption of "
        "PCP-003 §12.")
    for key, row in sorow.items():
        c = _cells(row)    # Output | Runs SDM | Runs Mfg | Mean SDM | Mean Mfg | Offset | CI | Met (low/est./high) | Q
        srow("sdm", f"Scale-down model offset of {aname(key)} (scale-down minus manufacturing scale, or their ratio on "
                    f"the log scale): {_unmark(c[5])}, {ns['OFF_CI']} % confidence interval {c[6]}; met over the NOR "
                    f"with the offset at the low end, estimate and high end: {c[7]}; qualified: {c[8]}.",
             row, so_t, sorow)
    sqs("operation",
        "The production bioreactor was operated in fed-batch mode under SOP-2003, with a single nutrient feed added on "
        "the platform schedule.",
        "Culture pH was held by base addition against the lactate that the culture produces, which lowers it.",
        "pCO2 was held at the level of each run by the fraction of carbon dioxide in the sparge gas, temperature by the "
        "vessel jacket and dissolved oxygen by sparging and agitation.",
        "This corrects the description of Version 1.0, which gave culture pH as controlled by carbon dioxide and base "
        "addition.",
        "Basal medium and feed were prepared under the media and feed procedure SOP-2004.",
        "Each factor of a design was held at the level the design gives for the run, every other parameter at its "
        "set-point, and the culture was harvested at the culture duration of the run.",
        "Osmolality was set by `{python} OSMC['control']`.",
        "PCP-003 does not state how osmolality is brought to its design level in a run in which pCO2 also varies "
        "(PD-003-06).",
        "The osmolality study used the same procedure, so the designs estimate the effects of osmolality and pCO2 "
        "separately.",
        "In a commercial vessel more base is added to hold the pH against a higher pCO2, which raises the osmolality as "
        "bicarbonate and sodium accumulate, and @sec-par-table states what follows for the PAR of pCO2.")
    sqs("analytical",
        "Each method was used within its validated range.",
        "Method precision contributes to the variation between centre points, and so to the pure error, and it sets a "
        "floor under the smallest effect the study can resolve.")
    sqs("sampling",
        "Each run was sampled at harvest, and the harvest sample was assayed for the `{python} words(len(RESPS))` "
        "modelled responses.",
        "Across the `{python} N_HD` runs assayed, host cell protein in the clarified harvest ranged from "
        "`{python} s3(HCP_MIN)` to `{python} s3(HCP_MAX)` ng/mg and DNA from `{python} s3(DNA_MIN)` to "
        "`{python} s3(DNA_MAX)` pg/mg.",
        "The culture was monitored through each run for viable cell density, viability and the principal metabolites "
        "under SOP-2003, and these records are not in the study record (PD-003-09).",
        "Each run carries the number it has in the standard order of its design, the \"Run\" column of the design "
        "tables in Appendices A and B, and this report cites runs by that number.",
        "The `{python} words(NC_SCR)` centre points of the screening design were made at positions "
        "`{python} join_and([str(x) for x in CP_ORDER['screening']])` of its `{python} N_SCR` runs, and the "
        "`{python} words(NC_RSM)` centre points of the response-surface design at positions "
        "`{python} join_and([str(x) for x in CP_ORDER['rsm']])` of its `{python} N_PLAN` runs.",
        "Of the augmentation runs, `{python} words(len(AUG_REP))` repeat a setting of the planned design (runs "
        "`{python} AUG_REP_A` repeat runs `{python} AUG_REP_P`).",
        "They lie in the other block, so the analysis does not count them as pure error, and the pure error of the "
        "models fitted to all runs comes from the centre points of the response-surface design.")
    sqs("stats",
        "Each factor was coded so that its set-point is 0 and the ends of its range studied are −1 and +1.",
        "For this step the set-point of every factor of the designs lies at the centre of its range studied, so the "
        "centre points of the designs are at the set-points.",
        "The screening data were fitted by least squares to the `{python} words(len(SFS))` main effects and the "
        "`{python} words(N_2FI_S)` two-factor interactions.",
        "An effect is twice the coded coefficient, the change in the response across the full range studied.",
        "The model has `{python} N_SCR_TERMS` terms with the intercept in `{python} N_SCR` runs.",
        "It leaves `{python} words(SDF_LOF)` degree of freedom for lack of fit and `{python} words(SDF_PE)` for pure "
        "error.",
        "Its lack-of-fit test compares the mean of the centre points with the mean of the factorial runs, which is the "
        "test for curvature.",
        "PCP-003 prescribes the full quadratic model of each response-surface output, with `{python} N_FULL` terms "
        "besides the intercept.",
        "The outputs were analysed instead by the model selection that INV-002 adopted on `{python} CA3_DATE` as its "
        "corrective action CA3, recorded as the discrepancy PD-003-03.",
        "An output is modelled on the log scale where that interval contains 0, the log, and excludes 1, the raw scale.",
        """Among all `{python} f"{NCAND:,}"` submodels of the full quadratic that keep hierarchy, the model with the lowest AICc is taken.""",
        "A submodel keeps hierarchy when it contains an interaction only with both its main effects, and a square only "
        "with its main effect.",
        "A stepwise search changes one term at a time and stops when no single change lowers AICc, so it can stop where "
        "only a combination of changes would lower it further.",
        "On the data of this step a forward search would have stopped at a model with a higher AICc for acidic "
        "variants, and a backward search for aggregate.",
        "The models were fitted to all `{python} N_ALL` runs, the `{python} N_PLAN` planned runs and the "
        "`{python} N_AUG` augmentation runs, with a block term coded −1 for the planned runs and +1 for the "
        "augmentation.",
        "A prediction is made with the block term at 0, the average of the two blocks.",
        "Of the modelled attributes, `{python} join_and([OUT[r] for r in LOGR])` are modelled on the log scale.",
        "For high mannose and acidic variants this is expected, because the precision of the glycan map and of icIEF is "
        "a percentage of the level (Appendix D).",
        "For aggregate the profile supports the log scale too, although the precision of SEC is an absolute amount.",
        """On the raw scale, the residual standard deviation of these outputs in the upper half of the predicted values is `{python} f"{min(RAWSPR[r][0] for r in LOGR):.2f}"` to `{python} f"{max(RAWSPR[r][0] for r in LOGR):.2f}"` times that in the lower half.""",
        "It keeps its 95 % coverage, because the probability that ln y lies between two values is the probability that "
        "y lies between their antilogs.",
        "The predicted value of a log-scale model is the median of the output, its geometric mean, and not its "
        "arithmetic mean.",
        "The first four restate the criteria of PCMP-001 §7.2.")
    sq("stats", """A run with a Cook's distance above `{python} f"{COOKF:g}"`/n, which is `{python} fx(COOK_LIM, 3)` for the `{python} N_ALL` runs of the models, is examined by deleting it and repeating the analysis.""")
    sqs("stats",
        "The models that do not meet the criterion on residuals and influential runs were used for the ranges and the "
        "design space, with each residual trend sized against the criterion of its output (PD-003-04).",
        "A quality attribute is judged on the exact 95 % prediction interval of a single run at each of the "
        "`{python} N_NORCOMB` combinations of NOR low, set-point and NOR high of the `{python} words(len(FS))` "
        "response-surface factors, with the offset applied.",
        "The interval comes from the t distribution and includes the uncertainty of the coefficients and the residual, "
        "the scatter between runs of the scale-down model.",
        "It is two-sided, so each of its ends is a one-sided 97.5 % limit.",
        "The set-point analysis holds the other factors at their set-points, scans the factor across its range studied "
        "at `{python} D.PAR_GRID_SETPOINT` points, and takes the contiguous range around the set-point over which the "
        "mean prediction meets the criterion.",
        """At each point it draws `{python} f"{D.PAR_MC_N:,}"` settings of the other factors, each from a normal distribution centred on its set-point with a standard deviation equal to the width of its NOR divided by `{python} f"{D.NOR_SD_DIVISOR:g}"`, clipped to the range studied.""",
        "The 2.5th percentile of the simulated runs must not fall below a lower limit, and the 97.5th percentile must "
        "not exceed an upper limit.",
        "The NOR-propagated PAR is the one that supports a claim.",
        """Capability at commercial scale was estimated from the integrated model of the train, which runs `{python} f"{N_MC:,}"` simulated batches through every step with each parameter drawn as in the NOR-propagated analysis (PCMP-001 §6.5).""",
        "Cpk is computed against the drug substance criterion, as the lower of the two one-sided indices for a two-sided "
        "criterion.",
        "PCP-003 §6.4 gives no test for a univariate difference.",
        """Each univariate parameter was judged on the difference between the mean of its two runs at the high end and the mean of its two runs at the low end of the range studied, by a t-test against the pooled standard deviation of the duplicate runs (PD-003-05, `{python} UV_DF` degrees of freedom), at the level of α = `{python} f"{ALPHA:g}"` that PCMP-001 §6.2 sets for a single test.""",
        "The results of the osmolality study were fitted by a straight line in osmolality, coded −1, 0 and +1 at the NOR "
        "low, the set-point and the NOR high.")

    # -- Study design -------------------------------------------------------------------------------------------------
    sqs("factors",
        "The set-point is the target of commercial operation, and the NOR is the band within which routine operation "
        "holds the parameter.",
        "The range studied is the knowledge space of this characterization.",
        "The codes were assigned in screening order and kept for the response-surface terms, so a factor carries the "
        "same letter throughout the report.")
    sqs("scr_design",
        "The design carries no squared term, so it can detect curvature but cannot attribute it to a factor.")
    sqs("rsm_design",
        "Osmolality was held at its set-point in every run.",
        "It also requires the factors carried into the design to be those that the screening identifies as active, "
        "with the design amended before execution if the subset differs.",
        "Osmolality was active in the screening (@sec-screening) and was not carried forward (PD-003-07).",
        "A failing model of an attribute of the drug substance specification on which the planned design shows an "
        "effect is augmented, and every other failing model is refitted.",
        "The number of runs is the smallest augmentation found in INV-002 to give a probability of at least "
        "`{python} fx(MA['assurance'])` that the full quadratic models of `{python} join_and([OUT[r] for r in AUGR])` "
        "meet the lack-of-fit test and the limit on overfitting.")
    sqs("uni_design",
        "Each parameter was run at the low and the high end of its range studied with every other parameter at its "
        "set-point, and the harvest was assayed for the `{python} words(len(RESPS))` responses and the two impurities.",
        "PCP-003 §6.4 plans one run at each end.",
        "The set-point reference of the study is the scale-down runs of the qualification study.")
    st("uni_design", "This design cannot show whether the effect of one of these parameters depends on the level of "
                     "another, so the range it supports is conditioned on the other parameters being at their "
                     "set-points.",
       [ref("uni_design", q("This design cannot show whether the effect of one of these parameters depends on the level "
                            "of another")),
        ref("uni_design", q("so the range it supports is conditioned on the other parameters being at their "
                            "set-points."))])
    sqs("osm_design",
        "The `{python} words(len(FS))` response-surface parameters were held at the combination of NOR settings least "
        "favourable for acidic variants, culture pH at `{python} pv('pH', WCA['settings']['pH'])`, culture temperature "
        "at `{python} pv('temperature', WCA['settings']['temperature'])`, culture duration at "
        "`{python} pv('duration', WCA['settings']['duration'])` and pCO2 at `{python} pv('co2', WCA['settings']['co2'])`.",
        """Each level had `{python} words(OSM_N)` runs, the smallest number for which the straight-line prediction at the NOR high has a standard error of at most `{python} f"{OSM_SE:g}"` times the standard deviation between runs.""")
    sqs("chronology",
        "The univariate study started on `{python} S0('S-BRX-UNI')`, before the response-surface study started on "
        "`{python} S0('S-BRX-RSM')`, against the sequence of PCP-003 §11 (PD-003-10).",
        "The records of the osmolality and augmentation studies name no equipment and state no calibration status of the "
        "pCO2 probe (PD-003-12).",
        "Host cell protein and DNA were measured in the clarified harvest of every run of the screening, "
        "response-surface and univariate designs.",
        "They were not measured on the qualification runs, on the augmentation runs or in the osmolality study.")
    for sid_, row in chrow.items():
        c = _cells(row)    # Study | Study type | Start | End | pCO2 probe | Calibration due
        srow("chronology", f"{sid_} ({low1(c[1])}) ran from {c[2]} to {c[3]}; "
                           f"pCO2 probe {c[4]}, next calibration due {c[5]}.", row, ch_t, chrow)

    # -- Results ------------------------------------------------------------------------------------------------------
    sqs("centre",
        "These replicates carry the variation between runs of the scale-down model and of the methods, and they are the "
        "pure error of the lack-of-fit test.",
        "High mannose is the least precise attribute at the centre point in both designs, with a coefficient of "
        "variation of `{python} pct(CV_HM_S)` in the screening design and `{python} pct(CV_HM_R)` in the "
        "response-surface design.",
        "That is several times the precision of the glycan map, `{python} pct(float(AMV3010.precision_pct))` of the "
        "result (Appendix D), so most of the variation in high mannose comes from the culture.",
        "The standard deviation of galactosylation at the centre point is `{python} fx(SD_GA_R)` points in the "
        "response-surface design against `{python} fx(SD_GA_S)` in the screening design.",
        "The larger value enters the lack-of-fit test of the galactosylation model as pure error, which is one reason "
        "why that test has the highest p-value of the `{python} words(len(RESPS))` models (@sec-models).")
    sqs("screening",
        "The screening models of `{python} join_and([OUT[r] for r in SCR_NSIG_MODEL])` have no significant model F-test "
        "(p `{python} pfmt(SCRF['afucosylation']['p'])` and p `{python} pfmt(SCRF['high_mannose']['p'])`), so their "
        "individual effects identify candidates and no more.",
        "No attribute shows significant curvature in the screening design, with lack-of-fit p-values from "
        "`{python} fx(SCR_LOF_MIN, 3)` to `{python} fx(SCR_LOF_MAX, 3)`, but with `{python} words(SDF_PE)` degrees of "
        "freedom for pure error that test detects only a large curvature.",
        "pCO2 has the largest effect on acidic variants, which fall by "
        "`{python} fx(abs(eff('acidic_variants', LTR['co2'])))` points from the low to the high end of its range.",
        "A higher culture pH also lowers acidic variants, and a higher culture temperature raises them.",
        "Culture duration has the largest effect on galactosylation, a fall of "
        "`{python} fx(abs(eff('galactosylation', LTR['duration'])))` points, and the interaction of culture pH with "
        "culture duration is nearly as large and of opposite sign.",
        "A higher pCO2 and a higher culture pH lower galactosylation, and a higher culture temperature raises it.",
        "A higher culture pH and a longer culture raise aggregate, by `{python} fx(eff('aggregates_hmw', LTR['pH']))` "
        "and `{python} fx(eff('aggregates_hmw', LTR['duration']))` points.",
        "A higher culture pH raises high mannose and a higher culture temperature lowers it.",
        "Afucosylation falls with a longer culture, and its interactions of culture pH with culture duration and with "
        "pCO2 are significant.",
        "Under PCP-003 §6.3 osmolality should therefore have been carried into the response-surface design, with the "
        "design amended before execution.",
        "It was not (PD-003-07).",
        "Appendix A shows the run at its design setting, and the analysis uses its recorded setting of "
        "`{python} pv('co2', R4_REC)`.",
        "The set of significant effects in @tbl-screening is the same with the run at its design setting (@sec-dev-01).")
    for (rk, term), row in scrow.items():
        c = _cells(row)    # Attribute | Term | Effect (points) | p-value
        srow("screening", f"Screening effect significant at α = {ns['ALPHA']:g} on {OUT[rk]}: {low1(c[1])}, "
                          f"{c[2]} points across the range studied, p {c[3]}.", row, sc_t, scrow)
    sqs("models",
        "For afucosylation the Box-Cox interval excludes both 0 and 1, so the rule keeps the raw scale although the "
        "profile does not support it either (@sec-residuals).",
        "Every selected model meets the model F-test (p < 0.001 for every model), the lack-of-fit test (p from "
        "`{python} fx(P_LOF_MIN, 3)` to `{python} fx(P_LOF_MAX, 3)`) and the limit on overfitting, with predicted R² at "
        "most `{python} fx(GAP_MAX, 3)` below R² against the limit of `{python} fx(GAPMAX)`.",
        "At the set-points, the selected models of afucosylation and acidic variants predict "
        "`{python} pct(CBIAS['afucosylation']['pred'], 2)` and `{python} pct(CBIAS['acidic_variants']['pred'], 2)` in "
        "the scale-down model.",
        "The means of the `{python} words(CBIAS['afucosylation']['n'])` centre points of the response-surface design are "
        "`{python} pct(CBIAS['afucosylation']['mean'], 2)` and `{python} pct(CBIAS['acidic_variants']['mean'], 2)`, with "
        "standard errors of `{python} fx(CBIAS['afucosylation']['se'])` and `{python} fx(CBIAS['acidic_variants']['se'])` "
        "points.",
        "At manufacturing scale the model of acidic variants predicts `{python} pct(SP_MFG['acidic_variants'], 2)` at the "
        "set-point, against a geometric mean of `{python} pct(SDM['acidic_variants']['mean_m'], 2)` in the "
        "manufacturing batches of the qualification.",
        "For acidic variants the difference lies in the unfavourable direction, because a model that predicts too high "
        "near the set-point overstates the distance to the lower limit.",
        "The predicted median at the least favourable NOR combination lies "
        "`{python} fx(WCA['predicted'] - ACC['acidic_variants'][0])` points above the lower limit, less than either "
        "difference at the set-point.",
        "If the model overstates acidic variants there by the same factor as at the centre points, the median at that "
        "combination is about `{python} pct(WCA_BIASED, 2)`, below the lower limit (@sec-criteria-results).",
        "On the planned runs the full quadratic models of `{python} join_and([OUT[r] for r in AUGR])` exceed the limit "
        "on overfitting, which is why the design was augmented.",
        "On all runs the full quadratic model of acidic variants meets the limit, but that of high mannose still exceeds "
        "it, with predicted R² `{python} fx(HM_FULLA_GAP, 2)` below R².",
        "The selected model of high mannose meets the limit, and the full quadratic model that the plan prescribes would "
        "leave high mannose without an adequate model on all runs.")
    sqs("residuals",
        "The selected models of `{python} join_and([OUT[r] for r in RI_PASS])` meet the criterion on residuals and "
        "influential runs, and those of `{python} join_and([OUT[r] for r in RI_FAIL])` do not (@tbl-crit4).",
        """For these two the absolute residuals rise with the predicted value, with a slope significant at `{python} join_and([f"p {pfmt(RI[r]['p_spread'])} for {OUT[r]}" for r in SPREAD])`.""",
        "No model shows a trend with the run order, and the lowest p-value of that test is `{python} fx(P_ORD_MIN, 3)`.",
        "No run has a Cook's distance above the F median of its model, which lies between "
        "`{python} fx(min(F_LIM), 3)` and `{python} fx(max(F_LIM), 3)` for these models.",
        "Across the `{python} words(len(RESPS))` models there are `{python} N_FLAG` such cases, on "
        "`{python} len(FLAG_RUNS)` different runs.",
        "For every attribute and every deleted run, the model selected without the run met the model F-test, the "
        "lack-of-fit test and the limit on overfitting, every attribute kept its verdict over the NOR, and every "
        "NOR-propagated PAR still contained the NOR.",
        "The share of the region studied that lies inside the design space ranged from `{python} pct(100 * min(DS_DEL))` "
        "to `{python} pct(100 * max(DS_DEL))`, against `{python} pct(100 * DSG['fraction'])` with all runs.",
        "The same model was selected in `{python} N_FLAG_SAME` of the `{python} N_FLAG` cases.",
        "For afucosylation, `{python} INFL_CHG['afucosylation'][0]`.",
        "For high mannose, `{python} INFL_CHG['high_mannose'][0]`.",
        "For acidic variants, `{python} join_and(INFL_CHG['acidic_variants'])`.",
        "For galactosylation it is `{python} fx(SPRD['galactosylation']['sd_lo'])` points in the lower half and "
        "`{python} fx(SPRD['galactosylation']['sd_hi'])` points in the upper half.",
        "For acidic variants it is `{python} fx(SPRD['acidic_variants']['sd_lo'], 3)` in the lower half and "
        "`{python} fx(SPRD['acidic_variants']['sd_hi'], 3)` in the upper half, on the log scale.",
        "For acidic variants the lowest prediction limit moves from `{python} pct(WCA['pi_low'], 2)` to "
        "`{python} pct(SPRD['acidic_variants']['lo'], 2)`, still below the lower limit.",
        "Judged with the standard deviation of each half, it still meets its criterion across the NOR, with prediction "
        "limits from `{python} pct(SPRD['afucosylation']['lo'], 2)` to `{python} pct(SPRD['afucosylation']['hi'], 2)`.")
    sqs("effects",
        "The coefficients of the selected models are in coded units, so each measures the change from the set-point to "
        "the end of the range of its factor.",
        "PCP-003 §7 calls an effect practically important when that change is large relative to the width of the "
        "criterion, and PCMP-001 §7.7 asks for the size of an effect beside its significance.",
        "@tbl-effect-size describes a change of a fifth of the width or more as large, of a tenth to a fifth as moderate "
        "and of less than a tenth as small.",
        "These bands are a judgement of this report, and no class rests on them (@sec-classification).",
        "Afucosylation falls as culture duration, culture pH, culture temperature and pCO2 rise.",
        "At the low end of the pH range a longer culture lowers afucosylation by `{python} fx(abs(DUR_AF_LO))` points "
        "across the range of culture duration, and at the high end of the pH range it changes it by "
        "`{python} fx(abs(DUR_AF_HI))` points.",
        "The squared term of culture pH is negative, so with the other factors at their set-points afucosylation is "
        "highest inside the pH range and falls toward both ends.",
        "Galactosylation falls with culture duration, pCO2 and culture pH, and rises with culture temperature.",
        "Across the range of culture duration galactosylation falls by `{python} fx(abs(DUR_GA_LO), 1)` points at the low "
        "end of the pH range and by `{python} fx(abs(DUR_GA_HI), 1)` points at the high end.",
        "Across the range of pCO2 it falls by `{python} fx(abs(CO2_GA_LO), 1)` and `{python} fx(abs(CO2_GA_HI), 1)` "
        "points.",
        "Across the range of culture temperature it rises by `{python} fx(TMP_GA_LO, 1)` points at the low end of the pH "
        "range and by `{python} fx(TMP_GA_HI, 1)` points at the high end.",
        "High mannose rises with culture pH, by a factor of `{python} fx(fold('high_mannose', 'pH'))` across its range, "
        "and falls with culture temperature, by a factor of `{python} fx(fold('high_mannose', 'temperature'))`.",
        "Acidic variants fall with pCO2, by a factor of `{python} fx(fold('acidic_variants', 'co2'))` across its range, "
        "and with culture pH, by a factor of `{python} fx(fold('acidic_variants', 'pH'))`.",
        "They rise with culture temperature, by a factor of `{python} fx(fold('acidic_variants', 'temperature'))`.",
        "The main effect of culture duration is a factor of `{python} fx(fold('acidic_variants', 'duration'))` and is "
        "not significant (p `{python} pfmt(P_DUR_AC)`).",
        """Of the terms of this model, only `{python} term_names(ACID_COMMON)` are carried by every model whose AICc lies within `{python} f"{NEAR_D:g}"` units of the lowest (@sec-near).""",
        "Aggregate rises with culture pH, by a factor of `{python} fx(fold('aggregates_hmw', 'pH'))` across its range, "
        "and with culture duration, by a factor of `{python} fx(fold('aggregates_hmw', 'duration'))`.",
        "The interaction of the two is negative on the log scale, so a longer culture multiplies aggregate by less at "
        "high pH than at low pH.",
        "The squared term of culture pH is negative, so the rise with pH flattens toward the top of the range.",
        "The surfaces are predictions of the scale-down model before the offset, and for a log-scale attribute they "
        "show the median.")
    for (a, p_), row in efrow.items():
        c = _cells(row)    # Attribute | Parameter | change over range | change over NOR | width | share | size
        srow("effects", f"Main effect of {low1(p_)} on {aname(lab_key[a])} "
                        f"at manufacturing scale: {c[2]} percentage points over the range studied and {c[3]} over the "
                        f"NOR, {c[5]} % of the criterion width of {c[4]} points ({c[6]}).", row, ef_t, efrow)
    sqs("augmentation",
        "The `{python} N_AUG` augmentation runs were added after the results of the planned runs were known, and every "
        "selected model is fitted to them.",
        "On the `{python} N_PLAN` planned runs alone, the selected models meet the model F-test, the lack-of-fit test and "
        "the limit on overfitting for every attribute.",
        "Their NOR-propagated PARs for acidic variants end at pH `{python} APA_TXT['pH'].split('–')[1]` for culture pH, "
        "start at `{python} APA_TXT['temperature'].split('–')[0]` °C for culture temperature and end at "
        "`{python} APA_TXT['co2'].split('–')[1]` mmHg for pCO2, so none of the three contains the NOR.",
        "At the least favourable NOR combination the predicted median is `{python} pct(ALT_PLAN['wc']['predicted'], 2)` "
        "and the lower prediction limit `{python} pct(ALT_PLAN['wc']['pi_low'], 2)`, and the design space covers "
        "`{python} pct(100 * ALT_PLAN['ds'])` of the region studied.",
        "With the plan's full quadratic model on all `{python} N_ALL` runs, the PAR of pCO2 ends at "
        "`{python} D._par_str(CO2_FULL).split('–')[1]` mmHg, the design space covers `{python} pct(100 * ALT_FULL['ds'])`, "
        "and high mannose exceeds the limit on overfitting.",
        "That every PAR contains the NOR, and that the design space covers `{python} pct(100 * DSG['fraction'])`, "
        "therefore rests on the augmentation runs and on the model selection together.",
        "A model selected on the same runs on which it is judged passes an optimistic check, and the augmentation runs "
        "are an independent one.",
        "The block term is not significant for any attribute (p ≥ `{python} fx(min(AUGC.block_p), 2)`), so a shift "
        "between the two blocks does not explain the misses.",
        "On all runs, the model of high mannose `{python} aug_txt('high_mannose')`.",
        "The model of aggregate `{python} aug_txt('aggregates_hmw')`.",
        "The model of acidic variants `{python} aug_txt('acidic_variants')`, and that of afucosylation "
        "`{python} aug_txt('afucosylation')`.",
        "The augmentation therefore changed what `{python} words(len(AUG_CHANGED))` of the `{python} words(len(RESPS))` "
        "models say, and for high mannose the interactions that the planned runs suggested are not supported by all "
        "runs.")
    sqs("near",
        """Besides the selected models, `{python} N_NEAR_OTHERS` models have an AICc within `{python} f"{NEAR_D:g}"` units of the lowest, `{python} join_and([('none' if NEAR_OTHERS[r] == 0 else str(NEAR_OTHERS[r])) + ' for ' + OUT[r] for r in RESPS])`.""",
        "Each of them meets the model F-test, the lack-of-fit test and the limit on overfitting, gives every attribute "
        "the same verdict over the NOR as the selected model and leaves the scale-down model qualified.",
        "They differ from the selected model by `{python} words(min(NEAR_DIFF))` to `{python} words(max(NEAR_DIFF))` "
        "terms.",
        "For afucosylation some carry `{python} term_names(NEAR['afucosylation']['vary'])`, for high mannose "
        "`{python} term_names(NEAR['high_mannose']['vary'])`, and for aggregate "
        "`{python} term_names(NEAR['aggregates_hmw']['vary'])`.",
        "For acidic variants they share only `{python} term_names(ACID_COMMON)`.")
    sqs("univariate",
        "The half-width of the 95 % confidence interval in @tbl-uni-effects is the precision of each comparison.",
        "For galactosylation, for example, a difference of `{python} fx(UV_HW['galactosylation'], 1)` points between the "
        "two ends of a range is detected about half the time, and a difference of `{python} fx(DET80, 1)` points with a "
        "probability of 80 %.",
        "Each was made at the level that PCMP-001 §6.2 sets for a single test, at which about one test in twenty with no "
        "real effect gives a significant result, so about `{python} fx(EXP_FP, 1)` such results are expected among them "
        "by chance.",
        "No effect of dissolved oxygen, basal medium concentration or nutrient feed-1 volume was detected on any "
        "attribute, at the precision given in @tbl-uni-effects, and no effect of the initial viable cell concentration "
        "was detected on any other attribute.",
        "PCP-003 §6.4 carries a univariate parameter into a multivariate study when it shows an effect on a quality "
        "attribute that the mechanism given in PCP-003 §4.3 does not account for.",
        "That mechanism, restated in @sec-platform, expects the initial viable cell concentration to change the number "
        "of viable cells and the titre, and no quality attribute.",
        "One route to acidic variants would be the time the antibody spends in the culture fluid at culture "
        "temperature, since a culture that starts at a higher cell concentration makes its antibody earlier.",
        "That route does not account for the effect.",
        "Culture duration sets the time in the culture fluid most directly, and it has no detectable main effect on "
        "acidic variants, in the screening design (p `{python} pfmt(P_DUR_AC_SCR)`) or in the response-surface model "
        "(p `{python} pfmt(P_DUR_AC)`).",
        "The parameter should therefore have been carried into a multivariate study and the plan amended, and that was "
        "not done (PD-003-11).",
        "A straight line between the two ends of the range puts acidic variants `{python} fx(abs(IV_NORLO_MFG))` points "
        "lower at the NOR low of the initial viable cell concentration than at its set-point, with the other parameters "
        "at their set-points.",
        "The response-surface and osmolality studies ran at the set-point of this parameter, so the verdict over the NOR "
        "in @sec-criteria-results does not include its effect.",
        "Added to the least favourable combination of the `{python} words(len(FS))` response-surface parameters, on the "
        "assumption that the effect does not depend on them, it would move the predicted median from "
        "`{python} pct(WCA['predicted'], 2)` to `{python} pct(WCA_IV_MED, 2)`, below the lower limit, and the lower "
        "prediction limit from `{python} pct(WCA['pi_low'], 2)` to `{python} pct(WCA_IV_LO, 2)`.",
        "The acceptance of the acidic-variant risk in @sec-criteria-results covers this combination on the same grounds.",
        "Acidic variants at harvest are to be trended against the initial viable cell concentration of each production "
        "batch, so that a false positive is found out.")
    sqs("osmolality",
        "The means in the table are values of the straight line fitted to the `{python} OSM_N * len(OSM_LV)` runs.",
        "For acidic variants the line falls by `{python} fx(abs(OSM_CH['acidic_variants']))` points across the NOR of "
        "osmolality, but its slope is not significant (p `{python} pfmt(OSM_P['acidic_variants'])`).",
        "Its fitted mean lies above the lower limit at the NOR low and at the set-point, and below it at the NOR high, at "
        "`{python} pct(OSM_AC_HI['mean'])`.",
        "The prediction interval of a single run reaches below the lower limit at every level, as the response-surface "
        "model showed at the set-point of osmolality.",
        "Every attribute other than acidic variants meets its criterion at every level.",
        "Its record names no equipment, so the calibration of the probe that held pCO2 at "
        "`{python} pv('co2', WCA['settings']['co2'])` is not documented (PD-003-12).",
        "The study was decided after the screening and response-surface results were known.")
    sqs("mech",
        "The fall is much larger at the low end of the pH range than at the high end.",
        "A galactosyltransferase whose rate depends on the pH of the Golgi predicts an interaction of culture pH with "
        "culture duration, but not its sign.",
        "Culture temperature raises galactosylation at high pH and has no effect at low pH.",
        "Afucosylation also falls with culture duration at low pH, and hardly at high pH.",
        "A higher pCO2 lowers galactosylation, afucosylation and acidic variants, in each case the direction of a higher "
        "culture pH.",
        """Osmolality was a factor of the screening design, at `{python} f"{PRM['osmolality'].prange[0]:g}"` and `{python} pv('osmolality', PRM['osmolality'].prange[1])`, set independently of pCO2, and it was held at its set-point in the response-surface design.""",
        "They fall as culture pH rises, although a higher pH speeds deamidation too.",
        "On the log scale the two effects multiply, so aggregate is highest after a long culture at high pH.",
        "High mannose rises with culture pH and falls with culture temperature.",
        "A high osmolality lowered them in the screening design, and a low initial viable cell concentration in the "
        "univariate study.",
        "Galactosylation approaches its upper limit at low pH, high temperature, short culture and low pCO2, but at the "
        "least favourable NOR combination its prediction interval stays "
        "`{python} fx(ACC['galactosylation'][1] - WCG['pi_high'], 1)` points below that limit.",
        "Routine operation is therefore limited by acidic variants, whose risk @sec-criteria-results accepts and "
        "@sec-control mitigates.")

    # -- Design space -------------------------------------------------------------------------------------------------
    sqs("ds",
        "On the mean prediction in place of the single-run interval, `{python} pct(100 * DSM['fraction'])` of the grid "
        "would lie inside.",
        "In the first, culture temperature and culture duration are at their set-points, and "
        "`{python} pct(100 * DS_SHARE[0])` of the NOR of culture pH and pCO2, at its corner of high pH and high pCO2, "
        "lies outside the design space.",
        "In the second, culture temperature is at its NOR low and culture duration at its NOR high, the settings least "
        "favourable for acidic variants, and `{python} pct(100 * DS_SHARE[1])` lies outside.",
        "The NOR therefore does not lie entirely inside the design space, and @sec-criteria-results gives the decision "
        "not to narrow it (PD-003-08).",
        "Each PAR of @sec-par-table holds while the other parameters vary about their set-points, and the design space "
        "holds at every combination of settings at once.")

    # -- Proven acceptable ranges: the criteria, the outputs against them, the decision not to narrow the NOR ----------
    sqs("criteria",
        "PCMP-001 §7.3 derives the criterion by back-calculation from the drug substance criterion, through the worst "
        "case of every downstream step on the platform, with no margin.",
        "Afucosylation, galactosylation and high mannose keep their drug substance criteria, because no downstream step "
        "changes them.",
        "The upper limit of acidic variants is the drug substance limit less the platform worst case of the increase "
        "across low-pH viral inactivation, `{python} fx(float(vi_acid.assumed))` points, which gives "
        "`{python} pct(ACC['acidic_variants'][1])`.",
        "In the low-pH response-surface design every run at the same hold time gave the same acidic-variant result, so "
        "the full quadratic model reproduces the results exactly, cannot be judged against PCMP-001 §7.2, and the "
        "platform value stands.",
        "The lower limit is the drug substance limit unchanged, which assumes that no downstream step lowers acidic "
        "variants (PCP-003 §12).",
        "The aggregate criterion is the drug substance limit less the aggregate increase across UF/DF, multiplied by "
        "the aggregate clearance factor of cation exchange, less the aggregate increase across low-pH viral "
        "inactivation.",
        "PCMP-001 assumed that no step after cation exchange changes aggregate, and from the platform values alone the "
        "criterion is `{python} pct(AGG.iac_high_apriori, 2)`.",
        "Verification of the platform worst cases at manufacturing scale changed all three terms (PCMP-001 §7.5).",
        "UF/DF raised aggregate within its NOR in the univariate study S-UFDF-UNI2.",
        "The cation exchange model predicted within its NOR a lowest clearance of "
        "`{python} fx(float(cex_agg.predicted_nor))`-fold at manufacturing scale, worse than the platform worst case of "
        "`{python} fx(float(cex_agg.assumed))`-fold.",
        "These two bounds alone would set the criterion at `{python} pct(AGG_TIGHT_ONLY, 2)`.",
        "The low-pH viral inactivation model gave a bound of `{python} fx(float(vi_agg.predicted_nor_bound95))` points "
        "for the increase, better than the platform value of `{python} fx(float(vi_agg.assumed))` points, on a model "
        "that meets the first three adequacy criteria of PCMP-001 §7.2 (PCR-006).",
        "The criterion in force is `{python} pct(AGG.iac_high, 2)`, stricter than the a priori value.",
        "It is computed from the unrounded terms, so the rounded values give "
        "`{python} pct((DS_AGG - round(float(uf_agg.predicted_nor_bound95), 2)) * round(float(cex_agg.predicted_nor_bound95), 2) - round(float(vi_agg.predicted_nor_bound95), 2), 2)`.",
        "The increase in @tbl-iac is the sum of the two increases, and the UF/DF increase is carried back through the "
        "clearance factor of cation exchange.",
        "PCMP-001 §7.5 asks for the risk of the change.",
        "The net change is a tightening.",
        "The widening alone moves the criterion `{python} fx(AGG.iac_high - AGG_TIGHT_ONLY)` points in the direction of "
        "a higher risk to the patient.",
        "To meet the drug substance limit, cation exchange must clear at least "
        "`{python} fx(float(cex_agg.predicted_nor_bound95))`-fold, low-pH viral inactivation must add no more than "
        "`{python} fx(float(vi_agg.predicted_nor_bound95))` points and UF/DF no more than "
        "`{python} fx(float(uf_agg.predicted_nor_bound95))` points.",
        "At the highest single-run level that the model of this step predicts within the NOR, "
        "`{python} pct(AGG_UP, 2)` at manufacturing scale, the drug substance would then carry at most "
        "`{python} pct(DS_AGG_EST, 2)`.",
        """None of the `{python} f"{N_MC:,}"` batches of the integrated model fell outside the aggregate criterion of the drug substance, which puts the probability below `{python} pct(100 * P_UB0, 2)` at one-sided 95 % confidence (@sec-capability).""",
        "The widening rests on the bound of the low-pH viral inactivation model, from the `{python} N_VI_RSM` runs of its "
        "response-surface design.",
        "That model has predicted R² `{python} fx(float(vi_agg.r2_minus_pred_r2), 3)` below R² and a lack-of-fit p-value "
        "of `{python} fx(float(vi_agg.p_lack_of_fit), 3)`, and it also meets the criterion on residuals and influential "
        "runs.",
        """The platform worst case is an increase over a hold of `{python} f"{VIH.prange[1]:g}"` min, while the NOR of the A-Mab hold as characterized ends at `{python} f"{VIH_MAX:g}"` min.""",
        "At the edges of the range studied, which include the longer hold, A-Mab added up to "
        "`{python} fx(float(vi_agg.observed_edge))` points, more than the platform value.",
        "The replacement therefore reflects the shorter hold of A-Mab and not a more stable product.",
        "It holds for routine manufacture, which is controlled within the hold-time NOR, and the NOR of hold time and "
        "temperature in force ends at the same longest hold and highest temperature as the NOR as characterized.",
        "Without the model selection of INV-002 corrective action CA3, the verification would have used the full "
        "quadratic models, and the aggregate criterion would be `{python} pct(ACC_WO['aggregates_hmw'][1], 2)`.",
        "The low-pH model of acidic variants is an exact fit, which cannot replace the platform value, so the "
        "acidic-variant criterion would not change.",
        "Judged against that aggregate criterion, aggregate keeps its verdict over the NOR, its PARs and the "
        "qualification of its scale-down model.")
    for key, row in iacrow.items():
        c = _cells(row)    # Attribute | DS criterion | Clearance factor | Increase | IAC | Basis
        srow("criteria", f"Intermediate acceptance criterion of {aname(key)} at the production bioreactor output: "
                         f"{_nomark(c[4])} %, from the drug substance criterion {c[1]} % through a downstream clearance "
                         f"factor of {c[2]} and an increase of {c[3]} ({_nomark(c[5])}).", row, iac_t, iacrow)
    sqs("criteria_results",
        "Afucosylation, galactosylation, high mannose and aggregate meet their criteria.",
        "At `{python} words(N_FAIL_COMB)` of the `{python} N_NORCOMB` combinations, all with pCO2 at its NOR high, the "
        "lower end of the prediction interval falls below `{python} pct(ACC['acidic_variants'][0])`.",
        "The least favourable combination is culture pH at its NOR high, culture temperature at its NOR low, culture "
        "duration at its NOR high and pCO2 at its NOR high.",
        "There the predicted median at manufacturing scale is `{python} pct(WCA['predicted'], 2)` and the prediction "
        "interval runs from `{python} pct(WCA['pi_low'], 2)` to `{python} pct(WCA['pi_high'], 2)`.",
        "The median lies `{python} fx(WCA['predicted'] - ACC['acidic_variants'][0])` points above the lower limit, less "
        "than the bias of the model at the set-point (@sec-models).",
        "With the initial viable cell concentration at its NOR low the median would fall to about "
        "`{python} pct(WCA_IV_MED, 2)` (@sec-univariate).",
        "The upper limit is met at every combination.",
        "The verdict is the same with the offset at either end of its interval (@sec-sdm).",
        "PCP-003 §7 requires the NOR to lie inside the region over which every modelled attribute meets its criterion, "
        "and the NOR to be narrowed until it does.",
        "Every combination that fails has pCO2 at its NOR high, so the NOR of pCO2 is the one whose narrowing would act "
        "on all of them.",
        "Some fail with culture pH at its set-point, so narrowing the NOR of culture pH alone would not restore the "
        "criterion.",
        "It was kept, and the risk accepted as the producer's, on the following grounds.")
    for key, row in crrow.items():
        c = _cells(row)    # Attribute | Criterion | mean at set-point | range over NOR | 95 % limits | Met
        srow("criteria_results", f"{aname(key)[0].upper() + aname(key)[1:]}, criterion {c[1]} %: mean "
                                 f"predicted at the set-point "
                                 f"{_nomark(c[2])} % and over the NOR {_nomark(c[3])} %; 95 % limits of a single run "
                                 f"over the NOR {_nomark(c[4])} %; met across the NOR: {c[5]}.", row, cr_t, crrow)
    grounds = re.findall(r"^\d+\. (.+)$", src_all.split("on the following grounds.", 1)[1].split("\n\nAt the least", 1)[0],
                         flags=re.M)
    if len(grounds) != 4:
        raise ValueError(f"{DOC}: {len(grounds)} grounds for keeping the NOR, the report gives four")
    for i, g_ in enumerate(grounds, 1):
        sent = re.split(r"(?<=\.) (?=[A-Z`])", g_)
        st("criteria_results", f"Ground {i} for keeping the NOR and accepting the risk as the producer's: "
                               f"{clean(render(g_))}", [ref("criteria_results", q(x)) for x in sent])
    sqs("criteria_results",
        "At the least favourable combination the fitted mean of the osmolality study lies below the lower limit at the "
        "NOR high of osmolality, although its slope is not significant (@sec-osmolality).",
        "The same acceptance covers that setting, and it covers the initial viable cell concentration at its NOR low, "
        "where the univariate effect would take the median below the lower limit (PD-003-11).",
        "For the control strategy that PCMR-001 consolidates, this report recommends a combined alert in the control "
        "system, which fires when `{python} ALERT_TXT` at the same time.",
        "It also recommends an action limit for acidic variants at harvest of `{python} pct(MIT['action_limit'], 2)`, "
        "and the trending of acidic variants against the initial viable cell concentration of each production batch "
        "(@sec-control).")

    # -- Proven acceptable ranges: the ranges -------------------------------------------------------------------------
    sqs("par",
        "A PAR is a range of a parameter within which the attribute is shown by supportive data to remain acceptable.",
        "The NOR-propagated analysis lets the other parameters vary across their NORs and judges the 95 % interval of "
        "the simulated runs, so it is stricter, and it is the PAR that supports a claim (PCMP-001 §6.4).",
        "Objective 3 requires a PAR where the selected model has a significant term in the parameter, "
        "`{python} N_SIGT` of the `{python} N_PAR` combinations.",
        "The other `{python} words(N_PAR - N_SIGT)`, `{python} NOSIG_TXT`, have no term in the parameter and are given "
        "for information.",
        "Every NOR-propagated PAR contains the NOR, and `{python} N_PAR - len(NARROW)` span the whole range studied.",
        "The exceptions are the PARs of culture pH and pCO2 for acidic variants.",
        "The PAR of culture pH ends `{python} fx(PMA.loc['pH', 'nor_hi'], 3)` pH units above the NOR high, and the PAR "
        "of pCO2 ends `{python} pv('co2', PMA.loc['co2', 'nor_hi'])` above it.",
        """Measured in standard deviations of the routine variation of each parameter, the width of its NOR divided by `{python} f"{D.NOR_SD_DIVISOR:g}"` (PCMP-001 §6.4), the margin is `{python} fx(MARG_SD['pH'])` for culture pH and `{python} fx(MARG_SD['co2'])` for pCO2.""",
        "In the set-point analysis every PAR spans the range studied.",
        "The range carried into the control strategy for each parameter is the intersection of its required PARs "
        "(PCP-003 §7, PCMP-001 §7.6).",
        "It is pH `{python} INT_TXT['pH']` for culture pH, `{python} INT_TXT['temperature']` °C for culture temperature, "
        "`{python} INT_TXT['duration']` days for culture duration and `{python} INT_TXT['co2']` mmHg for pCO2.",
        "The PAR of pCO2 is a range at the set-point of osmolality, because the response-surface model holds osmolality "
        "there.")
    for label_ in ("fig-par-afucosylation", "fig-par-galactosylation", "fig-par-high-mannose", "fig-par-acidic-variants",
                   "fig-par-aggregates"):
        cap1_ = fig_cap(label_, 1)
        st("par", f"Figure: {cap1_}", [ref("par", cap1_, caption=None, label=label_)])
    sqs("par_uni",
        "The ranges of the `{python} words(len(UNI))` univariate parameters are supported by their own data, with the "
        "other parameters at their set-points (PCMP-001 §4).",
        "Every result met its criterion at both ends of each range (@tbl-univariate), so the range studied of each "
        "parameter is supported for the `{python} words(len(RESPS))` attributes at that condition.")

    # -- Process capability and robustness ------------------------------------------------------------------------------
    sqs("cap",
        "Each Cpk is judged against the target of `{python} fx(CPK_TARGET)` and the minimum of `{python} fx(CPK_MIN)` of "
        "PCMP-001 §7.9.",
        "A Cpk between the two is acceptable, and a Cpk below the minimum needs an action in the control strategy.",
        "It does not use the response-surface models of this report, and it applies no scale-down offset, because it "
        "simulates manufacturing scale directly.",
        "Its drug substance means differ from the predictions of @tbl-criteria-bioreactor, for afucosylation "
        "`{python} pct(MC_MEAN['afucosylation'], 2)` against `{python} pct(SP_MFG['afucosylation'], 2)` predicted at "
        "the set-point.",
        "It draws every parameter of the step as the NOR-propagated analysis does, including osmolality, a higher level "
        "of which lowers acidic variants in its process model.",
        "A higher pCO2, a higher culture pH and a lower culture temperature move acidic variants toward the lower limit "
        "(@sec-effects).",
        "In the simulation `{python} words(int(PO.loc['acidic_variants', 'n_oos']))` of the `{python} f\"{N_MC:,}\"` "
        "batches fell outside the criterion.",
        "PCMR-001 consolidates this capability with the acceptance of the acidic-variant risk (@sec-criteria-results).",
        "Every other attribute that the step sets has a Cpk above the target, and none of the simulated batches fell "
        "outside its criterion.",
        "With no simulated batch outside, the probability of a batch outside is below `{python} pct(100 * P_UB0, 2)` at "
        "one-sided 95 % confidence.",
        "That bound covers the sampling of the simulation and not the uncertainty of the integrated model.")
    for lab_, row in cprow.items():
        c = _cells(row)
        srow("cap", f"Capability of the drug substance for {aname(lab_key[lab_])} ({c[1]} criticality), criterion {c[2]}: "
                    f"simulated mean {c[3]}, SD {c[4]}, Cpk {c[5]}, {c[6]}; {c[7]} of {N_MC:,} batches outside, normal "
                    f"tail {c[8]} per million.", row, cp_t, cprow)

    # -- Parameter classification ----------------------------------------------------------------------------------------
    sqs("class",
        "A parameter whose variation affects a critical quality attribute within the range studied is a CPP when the "
        "risk that it falls outside its acceptable range in operation is not low.",
        "It is a WC-CPP when that risk is low, because the parameter is readily controlled and its PAR is wide against "
        "its NOR.",
        "A parameter that affects process performance and no critical quality attribute is a KPP.",
        "A parameter with no relevant effect on either is a GPP.",
        "Neither PCMP-001 nor SOP-4001 sets a numerical threshold for a relevant effect or a wide PAR, so each class "
        "below is argued from the effects found and from the margin between each PAR and its NOR.",
        "The step has `{python} words(NCLS['WC-CPP'])` well-controlled critical process parameters, "
        "`{python} words(NCLS['CPP'])` CPP, `{python} words(NCLS['KPP'])` KPPs and `{python} words(NCLS['GPP'])` GPP.")

    # -- Contribution to the control strategy ------------------------------------------------------------------------
    sqs("control",
        "This step contributes the following elements to the control strategy of A-Mab.",
        "The combined alert, the action limit and the trending of items 2 to 4 are recommendations of this report, which "
        "PCMR-001 consolidates with those of the other steps.",
        "Culture pH is held by base addition, culture temperature by the vessel jacket, pCO2 by the carbon dioxide "
        "fraction of the sparge gas, osmolality through the base and feed additions, and culture duration by the day of "
        "harvest.",
        "A PAR is one-dimensional, so the PAR edge of one parameter holds only while the parameters that act with it "
        "stay within limits, and here those limits lie inside their NORs.",
        "Each limit is the most unfavourable value of its parameter at which the lower 95 % limit of a single run still "
        "meets the criterion of `{python} pct(ACC['acidic_variants'][0])`, with the other factors of the model at their "
        "unfavourable NOR edges.",
        "The alert covers every combination inside the NOR that fails the criterion.",
        "Osmolality is not a factor of the response-surface design, so the harvest action limit of item 3 covers it.",
        "The NOR is read as the range that the batch record controls, about ±3 standard deviations of the chance "
        "variation of each parameter (PCMP-001 §6.4).",
        "A result below it is found before purification, although it cannot change the batch.",
        "The delivered feed is checked by the mass reconciliation after the run, which detected DEV-003-02.",
        "The glycans, acidic variants and aggregate are tested there by the methods of @sec-analytical.",
        "The host cell protein that this step releases into the harvest is cleared by Protein A, cation exchange and "
        "anion exchange, and is judged at each of those steps and at the drug substance.")

    # -- Discussion ------------------------------------------------------------------------------------------------------
    sqs("disc",
        "The conclusions of this report rest on the scale-down model, whose offsets are known well enough that no "
        "verdict over the NOR depends on their exact size.",
        "Four facts limit how far that holds.",
        "The offset was estimated at the set-points only, so its use toward the edges of the range studied is an "
        "assumption.",
        "The carbon dioxide stripping of the commercial vessel was not matched, and osmolality was set independently of "
        "pCO2 (@sec-operation).",
        "The growth and titre of the runs are not in the record, so the model cannot be compared with manufacturing "
        "scale on process performance (PD-003-09).",
        "The difference in aggregate between the scales has no known cause (PD-003-13).")
    disc_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n# Discussion", 1)[1].split("\n# ", 1)[0], flags=re.M)
    if len(disc_list) != 5:
        raise ValueError(f"{DOC}: {len(disc_list)} numbered limitations in the Discussion, the report has five")
    for i, lim in enumerate(disc_list, 1):
        sent = re.split(r"(?<=\.) (?=[A-Z`])", lim)
        st("disc", f"Limitation {i}: {clean(render(lim))}", [ref("disc", q(x)) for x in sent])

    # -- Conclusions (the numbered list of the .qmd) -----------------------------------------------------------------
    con_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n# Conclusions", 1)[1].split("\n# ", 1)[0], flags=re.M)
    if len(con_list) != 7:
        raise ValueError(f"{DOC}: {len(con_list)} numbered conclusions, the report has seven")
    for i, con in enumerate(con_list, 1):
        sent = re.split(r"(?<=\.) (?=[A-Z`])", con)
        if i == 5:
            sent = [x for x in sent if not x.startswith("The lowest Cpk")]     # anchored on its capability record
            st("concl", f"Conclusion {i}: {clean(render(con))}", [ref("concl", q(x)) for x in sent]
               + [ref("concl", q_lowest)])
            continue
        st("concl", f"Conclusion {i}: {clean(render(con))}", [ref("concl", q(x)) for x in sent])

    # -- Study events and discrepancies from the plan ----------------------------------------------------------------
    sqs("record",
        "PCP-003 calls a departure from the plan a deviation.",
        "A process characterization study is not GMP manufacture, so this report records the events of execution as "
        "study events, under the numbers Version 1.0 gave them, and every departure from the plan as a discrepancy from "
        "the plan.",
        "A discrepancy is work that the plan did not foresee, or a requirement of the plan that was not met, however "
        "late it was found.")
    sqs("dev1",
        "With the run at its design setting instead, the set of significant effects is the same for every attribute.",
        "With run 4 excluded the screening model keeps `{python} words(R4['afucosylation']['excl_df'])` residual degrees "
        "of freedom.",
        "Fewer effects then reach significance for `{python} join_and([OUT[r] for r in R4_FEWER])`, and for "
        "afucosylation the same number, but not the same set.",
        "The record names screening run 4 only.")
    sqs("dev2",
        "The record shows `{python} words(int(dev_003_02_ver_n))` determinations of the glycans of the batch by the "
        "glycan map (SOP-3010, validated under AMV-3010).",
        "Their mean has a 95 % confidence interval of ± `{python} pct(float(dev_003_02_ci_hw), 2)` of the result.")
    for pid, row in pdrow.items():
        d = PDS[pid]
        srow(f"pd{pid[-2:]}", f"Discrepancy {pid} from PCP-003, {d['subject']}: planned {d['planned']}; done "
                              f"{d['done']}; reason {d['reason']}.", row, rows_=pdrow, caption=pd_cap,
             label="tbl-disc-register")
    sqs("pd01",
        "The osmolality study (@sec-osm-design) found a significant fall of afucosylation with osmolality, and no "
        "significant effect on acidic variants at the least favourable NOR combination of the other parameters "
        "(@sec-osmolality).",
        "Its fitted mean of acidic variants at the NOR high lies below the lower limit, and the acceptance of "
        "@sec-criteria-results covers that setting.")
    sqs("pd02",
        "The `{python} N_AUG` runs added under INV-002 changed the selected models of `{python} words(len(AUG_CHANGED))` "
        "attributes, and the models selected on the planned runs predict them poorly for high mannose and aggregate.",
        "The full quadratic model of high mannose still exceeds the limit on overfitting on all runs.")
    sqs("pd03",
        "With the plan's full quadratic model in place of the selected models, on all `{python} N_ALL` runs, high "
        "mannose would have no adequate model, and the PAR of pCO2 for acidic variants would not contain the NOR "
        "(@sec-augmentation).",
        "The selection also changes the criteria of this step through the verification of the downstream steps "
        "(@sec-criteria).")
    sqs("pd04",
        "The selected models of `{python} join_and([OUT[r] for r in RI_FAIL])` were used although their absolute "
        "residuals rise with the predicted value.",
        "With the standard deviation of the half of the predicted values in which each prediction lies, both attributes "
        "keep their verdict over the NOR (@sec-residuals).")
    sqs("pd05",
        "The duplicate runs give the pooled standard deviation of the study, with `{python} UV_DF` degrees of freedom, "
        "against which each univariate difference was tested, including the effect of the initial viable cell "
        "concentration on acidic variants (@sec-univariate).")
    sqs("pd07",
        "The screening showed osmolality active on acidic variants and on galactosylation (@sec-screening), and the "
        "Version 2.0 re-analysis of the screening results found that it had not been carried forward.",
        "Every prediction and PAR and the design space of this report are therefore conditioned on osmolality at its "
        "set-point.",
        "The osmolality study measured its effect at one combination of the other parameters (PD-003-01), and its "
        "interactions with them are known from the screening design only.")
    sqs("pd08",
        "Acidic variants do not meet their criterion over the NOR on the prediction interval of a single run "
        "(@sec-criteria-results), and the NOR was not narrowed as PCP-003 §7 requires.",
        "The Version 2.0 re-analysis against the criteria of PCMP-001 Version 2.0 found the departure.",
        "The risk was accepted as the producer's, on the grounds that @sec-criteria-results gives.",
        "A combined alert in the control system covers every failing combination inside the NOR.",
        "It fires when `{python} ALERT_TXT` at the same time.",
        "The action limit for acidic variants at harvest of `{python} pct(MIT['action_limit'], 2)` and the trending of "
        "@sec-control complete the mitigation.")
    sqs("pd09",
        "PCP-003 §5.4 requires the culture to be monitored for viable cell density and viability, and §5.1 lists both, "
        "with the titre, among the outputs of the qualification.",
        "Their absence means that the classes of the KPPs rest on platform knowledge for process performance "
        "(@sec-classification), and that the scale-down model was not compared with manufacturing scale on growth and "
        "titre.")
    sqs("pd10",
        "The univariate study started on `{python} S0('S-BRX-UNI')`, before the response-surface study started on "
        "`{python} S0('S-BRX-RSM')`, and the review of the execution dates under INV-001 found it.",
        "The sequence of PCP-003 §11 exists so that the factors of the response-surface design are chosen from the "
        "screening result.",
        "The screening study had ended on `{python} S1('S-BRX-SCR')`, before either study started, and the univariate "
        "parameters were assigned by RA-001 and were not candidates for the response-surface design.",
        "The order of the two studies therefore affects no analysis.")
    sqs("pd11",
        "The univariate study showed acidic variants `{python} fx(UIV_D_MFG)` points higher at the high end of the "
        "initial viable cell concentration than at the low end, at manufacturing scale (@sec-univariate).",
        "The mechanism of PCP-003 §4.3 does not account for the effect, so PCP-003 §6.4 carries the parameter into a "
        "multivariate study and amends the plan.",
        "That was not done, because the univariate results were not analysed in Version 1.0.",
        "The Version 2.0 re-analysis of the univariate results found the departure.",
        "With the parameter at its NOR low and the other parameters at their least favourable NOR combination, the "
        "effect would take the predicted median of acidic variants to about `{python} pct(WCA_IV_MED, 2)`, below the "
        "lower limit.",
        "The effect is the only significant result among `{python} N_UV_TESTS` univariate tests and may be a false "
        "positive.",
        "The risk acceptance of PD-003-08 is extended to that combination, and acidic variants at harvest are to be "
        "trended against the initial viable cell concentration of each production batch (@sec-control).")
    sqs("pd12",
        "The records of the osmolality study S-BRX-OSM and of the augmentation S-BRX-AUG name no equipment and state no "
        "calibration status of the pCO2 probe, which PCP-003 §9 and preventive action PA3 of INV-001 require.",
        "The review of the study record found the gap, and the records cannot be completed.",
        "If the studies used EQ-BRX-205, its next calibration was due on `{python} PROBE_DUE`, before both studies "
        "started.",
        "pCO2 varied from `{python} pv('co2', PRM['co2'].prange[0])` to `{python} pv('co2', PRM['co2'].prange[1])` in "
        "the `{python} N_AUG` augmentation runs and was held at `{python} pv('co2', WCA['settings']['co2'])` in the "
        "osmolality study, so the accuracy of those settings is not documented.",
        "A probe that read high, as in study event DEV-003-01, would put the true pCO2 below the recorded level.")
    sqs("pd13",
        "PCP-003 Version 1.0 qualified the scale-down model for an output only where the two scales showed no "
        "statistically significant difference at p < 0.05, and it required the source of any difference to be "
        "investigated before the characterization runs.",
        "For aggregate the two scales differ under that test (p `{python} pfmt(V1T['aggregates_hmw'])`), and no "
        "investigation was made before the screening study started.",
        "The re-analysis of the qualification against the Version 1.0 test found it.",
        "Under PCMP-001 Version 2.0 §7.1 a scale-down model may differ in mean from manufacturing scale where its offset "
        "is known precisely enough, so the Version 1.0 test was stricter than the use of the model needs.",
        "Aggregate is judged through its offset, a ratio of `{python} fx(SDM['aggregates_hmw']['offset'], 3)` with a "
        "`{python} OFF_CI` % confidence interval of `{python} fx(SDM['aggregates_hmw']['lo'], 3)` to "
        "`{python} fx(SDM['aggregates_hmw']['hi'], 3)`, and the model is qualified for it (@tbl-sdm-offsets).")

    if not_spans:
        raise ValueError(f"{DOC}: {len(not_spans)} snippet(s) are not spans of the .qmd prose:\n  "
                         + "\n  ".join(repr(x) for x in not_spans))
    sections = []
    for chap in CHAPTERS:
        stmts = [x for c_, x in STS if c_ == chap]
        if stmts:
            sections.append(ReportSection(section_id=f"{DOC}-sec{len(sections) + 1:02d}", title=chap,
                                          statements=stmts))
    if sum(len(s_.statements) for s_ in sections) != len(STS):
        raise ValueError(f"{DOC}: statements outside the chapters of the report")

    # ==== concepts =================================================================================================
    concepts = [Concept(concept_id="step:production_bioreactor", concept_type="PROCESS_STEP", canonical_name=UO_NAME,
                        aliases=["production bioreactor", f"Step {STEP}", "fed-batch culture",
                                 P.DOC_REGISTRY[DOC][1]], review_status="human_verified")]
    prose_name = {"ivcc": "initial viable cell concentration"}     # the name the prose uses for the parameter
    for name in prow:
        k = pkey_of_name[name]
        al = [n for n, c in G.PARAM_CONCEPT.items() if c == PC[k] and n != name]   # earlier names of the parameter
        short = ns["_short"](k)
        al += [x for x in (short, prose_name.get(k)) if x and x.lower() != name.lower()]
        if k in LTR:
            al.append(f"factor {LTR[k]}")
        concepts.append(Concept(concept_id=PC[k], concept_type="PROCESS_PARAMETER", canonical_name=name, aliases=al,
                                review_status="human_verified"))
    concepts += G._attr_concepts(ckeys)
    concepts += G._method_concepts([m.method_id for m in methods], amv_title)
    concepts += [Concept(concept_id="equip:production_bioreactor", concept_type="EQUIPMENT",
                         canonical_name=f"{CS} L production bioreactor", aliases=["commercial production vessel"],
                         review_status="human_verified"),
                 Concept(concept_id="equip:sdm_bench", concept_type="EQUIPMENT", canonical_name=SDM_NAME,
                         aliases=["scale-down model", "scale-down bioreactor system"], review_status="human_verified"),
                 Concept(concept_id=f"equip:{PROBE}", concept_type="EQUIPMENT", canonical_name=f"pCO2 probe {PROBE}",
                         aliases=[PROBE], review_status="human_verified")]

    # ==== the annex ================================================================================================
    annex = S.GroundTruthAnnex(
        document_id=DOC, document_title=f"{P.DOC_REGISTRY[DOC][0]} — {P.DOC_REGISTRY[DOC][1]}",
        document_class=P.DOC_REGISTRY[DOC][0], **G.rev2_layer(DOC, FILE),
        schema_extensions_used=G.COMMON_EXT + G.REV2_EXT + [
            "ProvenAcceptableRange (new model) — per attribute x parameter PAR, the two analyses of PCMP-001 §6.4 as "
            "the report prints them",
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "D-002 (authoring/DISCREPANCIES.md) is recorded as the document states it: ProcessStep.description and one "
            "report statement of the Introduction carry the sentence of Section 1.1 that the production bioreactor is "
            "the only step of the A-Mab drug substance process at which product quality attributes are formed. The "
            "annex neither corrects nor labels it.",
            "ProcessParameter.target_value and NOR are the set-point and NOR of the parameter table; no set-point or "
            "NOR of the step changed at Version 2.0 (the report says so). ProcessParameter.PAR is, for the four "
            "response-surface parameters, the range carried into the control strategy (the intersection of the "
            "required NOR-propagated PARs, Section 7.3); for the four univariate parameters, the range studied, which "
            "Section 7.4 supports with the other parameters at their set-points; and None for osmolality, which has no "
            "PAR from a model and for which no range beyond the NOR is claimed. rationale_for_criticality carries the "
            "classification argument of Section 9, each parameter anchored on its own sentences of it; the classes of "
            "osmolality (CPP), dissolved oxygen (GPP) and basal medium concentration (KPP) are those of the parameter "
            "register, argued by the rule of PCMP-001 §7.7.",
            "The QualityAttribute records are the seven attributes the CQA register assigns to the step. For the five "
            "modelled attributes acceptance_criteria holds the drug substance criterion and the Version 2.0 "
            "intermediate acceptance criterion; host cell protein and residual DNA carry the drug substance criterion "
            "only, because neither has an intermediate acceptance criterion at the step. acceptance_criteria (the annex "
            "layer) holds the rows of the criteria-change table, Version 1.0 superseded and Version 2.0 in force. The "
            "aggregate criterion, tightened by the cation exchange bound and widened by the low-pH viral inactivation "
            "bound, is carried by its rows of the derivation and criteria-change tables and by the report statements "
            "of Section 7.1.",
            "proven_acceptable_ranges: the twenty rows of the PAR table, with par_at_setpoint and par_nor_propagated "
            "as its columns 'PAR, others at set-point' and 'PAR, others across NOR' print them. The attribute cell of "
            "the table is merged, so a continuation row reads alike for several attributes; each record anchors on the "
            "contiguous span from the row that names its attribute to its own row. For this step the set-point of every "
            "factor of the designs is the centre of its range studied (the report says so).",
            "parameter_impacts_attribute and parameter_does_not_significantly_impact_attribute: for the four "
            "response-surface parameters, one assertion per attribute on its span of the PAR table, whose 'Required by "
            "objective 3' cell states whether the selected model has a significant term in the parameter, with the "
            "rows of the effect-size table and of the coefficient table where the model carries the main effect; for "
            "osmolality, on the screening effects and the osmolality study; for the four univariate parameters, one "
            "assertion per attribute on its row of the univariate effects table, host cell protein and DNA in the "
            "clarified harvest included (attr:hcp, attr:residual_dna).",
            "StatisticalModelFit: the selected model of each output on all runs (terms from the coefficient tables of "
            "Section 5.3.3 and Appendix C, F statistic from the analysis of variance, replicate statistics of the "
            "centre points of the response-surface design), the plan's full quadratic on the planned runs and on all "
            "runs with a block term (re-evaluation table), the model selected on the planned runs alone with its "
            "prediction of the augmentation runs (no fit statistics are printed for it), and the five screening models "
            "(terms from Appendix C; the model F-test p only for afucosylation and high mannose, the two the report "
            "prints, and the range of the lack-of-fit p-values in the adequacy statement, as the report gives it). A "
            "p-value printed as '< 0.001' has no float value: the selected models carry it in adequacy_statement, and a "
            "term with it carries significant=true.",
            "The schema has no record type for a discrepancy from the plan. PD-003-01 to PD-003-13 are report statements "
            "anchored on their rows of the discrepancy register and on the sentences of their subsections; the studies "
            "they record carry that row as a source reference.",
            "The report records no deviation: a process characterization study is not GMP manufacture, so the two "
            "events of execution are study events, under the numbers Version 1.0 gave them (DEV-003-01, DEV-003-02). "
            "They are Deviation records, the schema's only record type for an event of execution. "
            "no_impact_on_conclusions is false for both: the report states what each changes and does not say that "
            "either changes no conclusion; for DEV-003-01 it says the record does not show whether the probe read high "
            "in the response-surface runs.",
            "Studies: every row of the execution-window table has a StudyDesign record. The osmolality study S-BRX-OSM "
            "is univariate (its chronology kind); the augmentation S-BRX-AUG is a response-surface study without "
            "n_runs, which the corpus test reserves for the seeded screening and response-surface designs. Host cell "
            "protein and residual DNA are listed as responses of the three designs that measured them in the clarified "
            "harvest.",
            "ProcessCapability.claimed_process_minimum is true for acidic variants: Conclusion 5 states that the lowest "
            "Cpk of the drug substance is that of acidic variants, which the capability data of the whole train bear out.",
            "ControlStrategyElement records are the eight elements of Section 10; elements 2 to 4 (the combined alert, "
            "the action limit for acidic variants at harvest and the trending against the initial viable cell "
            "concentration) are recommendations of the report, which PCMR-001 consolidates.",
            "rhetorical_spans: authoring/rhetorical/PCR-003.spans.yaml, re-curated against the Version 2.0 text in the "
            "same pass as this builder. weak_claims is empty.",
        ] + G._unrendered_note(unrendered),
        inventory=G.rev2_inventory(DOC, FILE, "process_characterization_report", UO_NAME,
                                   ["process characterization", "production bioreactor", "fed-batch cell culture",
                                    "glycosylation", "intermediate acceptance criteria", "design of experiments",
                                    "model selection", "augmentation of the response-surface design",
                                    "scale-down model qualification", "osmolality study", "acidic variant risk",
                                    "parameter classification"]),
        entities=entities, studies=studies, design_spaces=design_spaces, proven_acceptable_ranges=pars,
        report_sections=sections, assertions=AssertionStore(run_id=f"gt-{DOC}", assertions=AS, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{DOC}", concepts=concepts),
        weak_claims=[], rhetorical_spans=G.build_rhetorical_spans(DOC, FILE),
        acceptance_criteria=G.acceptance_criteria_layer(DOC, FILE, title("changes"), ct["tbl-criteria-change"][0],
                                                        [UO]))
    _gate(annex, text)
    return annex
