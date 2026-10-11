"""PCR-007 Version 2.0, the characterization report of cation exchange chromatography (Step 7), re-analysed
under INV-001 and INV-002: its ground-truth annex (``build()``).

The kinds of record follow the Version 2.0 report builders with a designed experiment (``pcr_009.py``,
``pcr_006.py``) and the concept ids follow the Version 1.0 builder of this report (``build_report_cex``) and the
Version 2.0 builder of its plan (``pcp_007.py``: ``step:cex``, ``param:cex_*``, ``equip:cex_sdm_column``,
``equip:<chamber>``): the inventory and the revision layer; the step, its scale-down model, the instrumented
chamber of the response-surface study and the two sites; the five parameters, with the class and the
classification argument of the report; the five attributes the step clears (aggregate, host cell protein and
fragments, judged against intermediate acceptance criteria, and residual DNA and leached Protein A, which carry
no criterion at this step); the seven method validations; the capability records of the drug substance; the
fitted models (the planned full quadratic of every output with a criterion, the selected models, the screening
models and the two models of the clearance of residual DNA and leached Protein A); the two study events; the
document relationships and the explicit non-claims; the four studies of the execution-window table that have a
study type; the design space; the proven acceptable ranges; the criteria of the criteria-change table (Version
1.0 superseded, Version 2.0 in force); the assertions; the report statements, grouped by the chapters of the
report; the concepts; and the rhetorical spans of ``authoring/rhetorical/PCR-007.spans.yaml``.

Every table of the report is a complex table (``T.frame`` or a ``T.`` builder), read back through
``qmd_ctables`` from the object the report printed, or a markdown string of a ``_pcpkg`` helper
(``related_docs_md``, ``dev_register``, ``discrepancy_register``), read back with ``md_string_rows``, so each
row quote is the rendered row, with ``table_header=rows.header``. Every prose quote is a span of the ``.qmd``
found by ``S_`` (a unique prefix of the source, run to the end of its sentence or to a given end string) and
rendered as the ``.docx`` reads it (``render``: the inline expressions evaluated in the report's own namespace,
a cross-reference resolved to its rendered number, typographic quotes and apostrophes), so no value and no
quote is typed here. ``q`` refuses a span that crosses a citation, and ``build()`` refuses to return an annex
with a quote that does not ground or a weak anchor.

The proven acceptable ranges are recorded as the report prints them: the "PAR at set-point" column of the PAR
table goes to ``par_at_setpoint`` as printed, and the report's description of the two analyses is recorded in
its own words. Nothing is added to it (registered discrepancy D-001).
"""
from __future__ import annotations

import os
import re

import _pcpkg as P
import build_ground_truth as G
import schema_ext as S
from check_grounding import normalize, specificity_report

DOC = "PCR-007"
FILE = "PCR-007_cex.docx"
QMD = "PCR-007_cex.qmd"
UO = "cex"
STEP_ID = "step:cex"
SDM_ID = "equip:cex_sdm_column"
#: The scale-down model as the report names it (Executive summary).
SDM_NAME = "scale-down model of the commercial column"
#: Method validation -> method type, for the validation the shared table does not list (a kind, not a value).
METHOD_TYPE = dict(G.METHOD_TYPE, **{"AMV-3221": "chromatography"})

_INTRO = "Introduction"
_PRIOR = "Prior knowledge and quality risk basis"
_MM = "Materials and methods"
_SD = "Study design"
_RES = "Results"
_RSM = "Response-surface models"
_PAR = "Proven acceptable ranges"
_REC = "Study events and discrepancies from the plan"
_EV = "Study events"
_PDS = "Discrepancies from the plan"
#: Section key -> heading path as the .qmd writes it. ``_check_sections`` checks every title against the
#: headings of the .qmd, so a renamed section fails loudly instead of mislabelling its references.
SEC = {
    "title": ("Title block",),
    "exec": ("Executive summary",),
    "uo": (_INTRO, "Product and unit operation"),
    "objectives": (_INTRO, "Objectives"),
    "basis_reg": (_INTRO, "Regulatory and scientific basis"),
    "changes": (_INTRO, "Changes in this revision"),
    "platform": (_PRIOR, "Platform and prior-product knowledge"),
    "cqa": (_PRIOR, "Quality attributes in scope"),
    "risk": (_PRIOR, "Risk-based prioritization and parameter selection"),
    "sdm": (_MM, "Scale-down model and its qualification"),
    "operation": (_MM, "Operation"),
    "analytics": (_MM, "Analytical methods"),
    "sampling": (_MM, "Sampling plan"),
    "stats": (_MM, "Statistical methods"),
    "thresholds": (_MM, "Statistical methods", "Decisions for which the plan sets no threshold"),
    "factors": (_SD, "Factors, ranges and the knowledge space"),
    "scr_design": (_SD, "Screening design"),
    "rsm_design": (_SD, "Response-surface design"),
    "uni_design": (_SD, "Univariate assessment"),
    "centre": (_RES, "Centre-point performance and reproducibility"),
    "screening": (_RES, "Factor effects in the screening design"),
    "rsm": (_RES, _RSM),
    "rsm_agg": (_RES, _RSM, "Aggregate"),
    "rsm_hcp": (_RES, _RSM, "Host cell protein"),
    "influence": (_RES, _RSM, "Influential runs"),
    "near": (_RES, _RSM, "Models within two AICc units of the selected model"),
    "rsm_frag": (_RES, _RSM, "Fragments"),
    "rsm_yield": (_RES, _RSM, "Step yield"),
    "surfaces": (_RES, _RSM, "Response surfaces"),
    "dna_lpa": (_RES, "Residual DNA and leached Protein A"),
    "flow": (_RES, "Univariate assessment of elution flow rate"),
    "mech": (_RES, "Mechanistic interpretation"),
    "ds": ("Design space",),
    "basis": (_PAR, "Acceptance basis"),
    "criteria": (_PAR, "Outputs against their criteria"),
    "par": (_PAR, "Proven acceptable ranges per parameter"),
    "verif": (_PAR, "Verification of the platform worst cases"),
    "cap": ("Process capability and robustness",),
    "class": ("Parameter classification",),
    "cs": ("Contribution to the control strategy",),
    "disc": ("Discussion",),
    "concl": ("Conclusions",),
    "record": (_REC,),
    "events": (_REC, _EV),
    "dev1": (_REC, _EV, "DEV-007-01 Expired buffer lot in a screening run"),
    "dev2": (_REC, _EV, "DEV-007-02 Temperature excursion during a response-surface run"),
    "pds": (_REC, _PDS),
    "pd01": (_REC, _PDS, "PD-007-01 Model selection"),
    "pd02": (_REC, _PDS, "PD-007-02 Conclusions on a model that does not meet the residual criterion"),
    "pd03": (_REC, _PDS, "PD-007-03 Flow-rate study without the set-point run"),
    "pd04": (_REC, _PDS, "PD-007-04 Residual DNA offset recorded, not investigated"),
    "pd05": (_REC, _PDS, "PD-007-05 Load aggregate and host cell protein not recorded"),
    "pd06": (_REC, _PDS, "PD-007-06 Residual DNA and leached Protein A not measured on the screening runs"),
    "pd07": (_REC, _PDS, "PD-007-07 Flow-through, wash and strip fractions and the mass balance not recorded"),
    "pd08": (_REC, _PDS, "PD-007-08 Packing tests not recorded for each campaign"),
    "pd09": (_REC, _PDS, "PD-007-09 Fractionated runs not in the plan"),
    "pd10": (_REC, _PDS, "PD-007-10 Approaches where the plan sets no threshold, and step-level capability"),
    "pd11": (_REC, _PDS, "PD-007-11 Feed lots not recorded"),
    "pd12": (_REC, _PDS, "PD-007-12 Load/wash buffer named Tris in Version 1.0"),
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
    """``{label -> rendered cross-reference}`` ("sec-par" -> "Section 7", "tbl-par" -> "Table 24").

    A section number follows the numbering of the headings (an unnumbered heading takes none), as the
    rendered document prints it. A table or figure number is read off the rendered caption ("Table 24:
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
             or re.search(word + r" (\d+): " + re.escape(normalize(_smart(cap))), text))
        if m:
            out[lab] = f"{word} {m.group(1)}"
    return out


def _smart(s):
    """Prose as pandoc renders it: straight double quotes become typographic pairs and a straight
    apostrophe a typographic one. Table cells are raw markup and keep the straight forms."""
    return re.sub(r'"([^"]*)"', "“\\1”", s).replace("'", "’")


def _cells(row):
    """The cells of a rendered row: a continuation row keeps its empty leading cells."""
    return [c.strip() for c in row.split("|")]


def _unmark(cell):
    """A rendered cell without its trailing footnote markers ("0.76 d)", "≤ 4.90 b)")."""
    return re.sub(r"(?:\s[a-z]\))+$", "", str(cell)).strip()


def _num(cell):
    """A number as the document prints it, back to a float ("−0.2792", "2,785", "0.76 d)"); None for a
    cell that is not one ("< 0.001", "n.a.", "–")."""
    s = _unmark(cell).replace("−", "-").replace(",", "").replace("×", "")
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
    from annex_contract.results import Deviation, ModelTerm, ProcessCapability, StatisticalModelFit
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
        return tab, rows_

    def ffill(col):
        out_, cur_ = [], None
        for v in col:
            cur_ = v if v else cur_
            out_.append(cur_)
        return out_

    def md_rows(md, label):
        rows_ = G.md_string_rows(md)
        # a markdown table is markdown: pandoc renders its straight apostrophes typographic ("Cook’s")
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

    def fig_cap(label, n):
        """The first ``n`` sentences of the caption of figure ``label``, from the option of the chunk that draws it."""
        code = next(c_ for c_ in re.findall(r"```\{python\}\n(.*?)```", _source(), flags=re.S)
                    if re.search(r"#\|\s*label:\s*" + re.escape(label) + r"\s*$", c_, flags=re.M))
        cap = re.search(r'#\|\s*fig-cap:\s*"(.*)"', code).group(1)
        out_ = " ".join(re.findall(r"[^.]+\.", cap)[:n]).strip()
        if normalize(out_) not in text:
            raise ValueError(f"{DOC}: the caption of {label} does not ground: {out_!r}")
        return re.sub(r"\s+", " ", out_)

    # ---- names and values of the report ----------------------------------------------------------
    uo = ns["uo"]
    FAC = list(ns["FAC"])                               # ["load", "wash_cond", "elution_ph", "stop_collect"]
    KEYS = [p.key for p in uo.parameters]              # the four factors and the flow rate
    NAME = {k: ns["PN"][k] for k in KEYS}               # "Protein load", "Load/Wash conductivity", ...
    pn = ns["pn"]                                       # the names in prose ("load/wash conductivity")
    LET = ns["LET"]                                     # factor key -> letter code
    fac_of = {v: k for k, v in LET.items()}
    UO_NAME, STEP_LABEL = G.CXUO_NAME, G.CXSTEP_LABEL
    PC = G.CXPARAM_CONCEPT                              # parameter name -> concept id
    pkey = {NAME[k]: k for k in KEYS}
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))
    reg = P.cqa_reg.set_index("key")
    by_label = G._attr_key_by_label()
    RS = list(ns["RS"])                                 # aggregate, host cell protein, fragments, step yield
    LAB = ns["LAB"]                                     # response -> label of the tables
    resp_attr = {"aggregate_out_pct": "aggregates_hmw", "hcp_out_ng_mg": "hcp", "lmw_cesds_pct": "fragments_lmw",
                 "step_yield": "step_yield"}
    attr_resp = {v: k for k, v in resp_attr.items()}
    lab_resp = {LAB[r]: r for r in RS}
    AKEYS = ["aggregates_hmw", "fragments_lmw", "hcp", "residual_dna", "leached_protein_a"]
    CRIT_KEYS = ["aggregates_hmw", "hcp", "fragments_lmw"]
    IAC = ns["IAC"]
    FIT, TERMS = ns["FIT"], ns["TERMS"]
    ALPHA = float(ns["ALPHA"])
    EQ = ns["EQ"]
    CHAMBER_ID = f"equip:{EQ.name}"
    CHAMBER_NAME = f"{EQ['description']} {EQ.name}"
    PDS = {d["id"]: d for d in P.PLAN_DISCREPANCIES[DOC]}

    def tname(term):
        """A model term of the report's tables ("A", "AC", "D²") in words."""
        base = term.rstrip("²")
        return " × ".join(pn[fac_of[x]] for x in base) + ("²" if term.endswith("²") else "")

    def sig_of(p_):
        return p_.startswith("<") or (_num(p_) is not None and _num(p_) < ALPHA)

    # ---- the rendered tables, from the objects the report printed --------------------------------
    pdf_ = ct["tbl-params"][1]
    pt_t, prow = keyed("tbl-params", list(pdf_["Parameter"]), str, cell=0)
    pdf_ = pdf_.set_index("Parameter")
    lg_df = ct["tbl-legend"][1]
    lg_t, lgrow = keyed("tbl-legend", list(lg_df["Factor"]), str, cell=1)
    cq_df = ct["tbl-cqas"][1]
    ckeys = [by_label[n] for n in cq_df["CQA"]]
    if ckeys != AKEYS:
        raise ValueError(f"{DOC}: the attributes in scope are no longer {AKEYS}: {ckeys}")
    cq_t, crow = keyed("tbl-cqas", ckeys, lambda k: names[k], cell=1)
    cq_df = cq_df.set_index(np.array(ckeys))
    sop_df = ct["tbl-sops"][1]
    sop_t, soprow = keyed("tbl-sops", list(sop_df["Reference"]), str, cell=1)
    amv_title = dict(zip(sop_df["Reference"], sop_df["Title"]))
    md_df = ct["tbl-methods"][1]
    md_t, mdrow = keyed("tbl-methods", list(md_df["Method\nvalidation"]), str, cell=2)
    md_df = md_df.set_index("Method\nvalidation")
    win_df = ct["tbl-windows"][1]
    win_t, winrow = keyed("tbl-windows", list(win_df["Study"]), str, cell=0)
    off_keys = [_cells(r)[0] for r in ct["tbl-sdm-offsets"][0].rows()]
    off_t, offrow = keyed("tbl-sdm-offsets", off_keys, str, cell=0)
    ikeys = [by_label[_cells(r)[0]] for r in ct["tbl-iac"][0].rows()]
    iac_t, irow = keyed("tbl-iac", ikeys, lambda k: T.ATTR_NAME[k], cell=0)
    crkeys = [by_label[_cells(r)[0]] for r in ct["tbl-criteria-cex"][0].rows()]
    cr_t, crrow = keyed("tbl-criteria-cex", crkeys, lambda k: T.ATTR_NAME[k], cell=0)
    rvkeys = [by_label[_cells(r)[0]] for r in ct["tbl-reeval-cex"][0].rows()]
    rv_t, rvrow = keyed("tbl-reeval-cex", rvkeys, lambda k: T.ATTR_NAME[k], cell=0)
    cen_df = ct["tbl-centre"][1]
    cen_t, cenrow = keyed("tbl-centre", list(zip(ffill(cen_df["Design"]), cen_df["Response"])),
                          lambda k: k[1], cell=1)
    sf_df = ct["tbl-scr-fit"][1]
    sf_t, sfrow = keyed("tbl-scr-fit", [lab_resp[x] for x in sf_df["Response"]], lambda r: LAB[r], cell=0)
    se_df = ct["tbl-scr-effects"][1]
    se_t, serow = keyed("tbl-scr-effects", list(zip(ffill(se_df["Response"]), se_df["Term"])),
                        lambda k: k[1], cell=1)
    se_lab = {"aggregate_out_pct": LAB["aggregate_out_pct"], "hcp_out_ng_mg": LAB["hcp_out_ng_mg"],
              "step_yield": "Step yield (points)"}              # the response cell of the effects table
    ms_df = ct["tbl-model-summary"][1]
    ms_t, msrow = keyed("tbl-model-summary", [lab_resp[x] for x in ms_df["Output"]], lambda r: LAB[r], cell=0)
    rd_df = ct["tbl-resid"][1]
    rd_t, rdrow = keyed("tbl-resid", [lab_resp[x] for x in rd_df["Output"]], lambda r: LAB[r], cell=0)
    co_df = ct["tbl-rsm-coef"][1]
    co_t, corow = keyed("tbl-rsm-coef", list(zip([lab_resp[x] for x in ffill(co_df["Output"])], co_df["Term"])),
                        lambda k: k[1], cell=1)
    an_df = ct["tbl-anova"][1]
    an_t, anrow = keyed("tbl-anova", list(zip([lab_resp[x] for x in ffill(an_df["Output"])], an_df["Source"])),
                        lambda k: k[1], cell=1)
    yc_df = ct["tbl-yield-coef"][1]
    yc_t, ycrow = keyed("tbl-yield-coef", list(yc_df["Term"]), str, cell=0)
    dl_df = ct["tbl-deletion"][1]
    dl_t, dlrow = keyed("tbl-deletion", list(zip([lab_resp[x] for x in ffill(dl_df["Output"])],
                                                  dl_df["Run\ndeleted"])), lambda k: k[1], cell=1)
    nr_df = ct["tbl-near"][1]
    nr_keys = list(zip([lab_resp[x] for x in ffill(nr_df["Output"])], nr_df["Terms added (+)\nor removed (−)"]))
    nr_t, nrrow = keyed("tbl-near", nr_keys, lambda k: k[1], cell=2)
    fl_t = ct["tbl-flow"][0]
    flrow = present_header(G.ctable_rows(fl_t))
    fc_df = ct["tbl-flow-cmp"][1]
    fc_t, fcrow = keyed("tbl-flow-cmp", list(fc_df["Response"]), str, cell=0)
    par_df = ct["tbl-par"][1]
    par_keys = list(zip([lab_resp[x] for x in ffill(par_df["CQA"])], par_df["Parameter"]))
    par_t, parrow = keyed("tbl-par", par_keys, lambda k: k[1], cell=2)
    short = {T.ATTR_NAME[k].rsplit(" (", 1)[0]: k for k in T.ATTR_NAME}
    ver_t, verrow = keyed("tbl-iac-verification", [short[_cells(r)[1]] for r in ct["tbl-iac-verification"][0].rows()],
                          lambda k: T.ATTR_NAME[k].rsplit(" (", 1)[0], cell=1)
    capkeys = list(ns["CAPK"])
    cap_lab = ns["_lab_cap"]
    cap_df = ct["tbl-cap"][1]
    cap_t, caprow = keyed("tbl-cap", capkeys, lambda k: cap_lab[k], cell=0)
    cap_df = cap_df.set_index(np.array(capkeys))
    sc_t = ct["tbl-sec-cesds"][0]
    scrow = present_header(G.ctable_rows(sc_t))
    mbs_t = ct["tbl-methods-by-study"][0]
    present_header(G.ctable_rows(mbs_t))
    dna_t = ct["tbl-dna-lpa"][0]
    dnarow = present_header(G.ctable_rows(dna_t, [int(_cells(r)[0]) for r in dna_t.rows()]))
    mtx = {}
    for kind, label in (("screening", "tbl-doe-cex-screening"), ("rsm", "tbl-doe-cex-rsm")):
        tab = ct[label][0]
        mtx[kind] = (tab, present_header(G.ctable_rows(tab, [int(_unmark(_cells(r)[0])) for r in tab.rows()])))
    rel, rel_cap = md_rows(P.related_docs_md(DOC), "tbl-related")
    devrow, dev_cap = md_rows(P.dev_register(DOC), "tbl-events")
    pdrow, pd_cap = md_rows(P.discrepancy_register(DOC), "tbl-discrepancies")
    if sorted(pdrow) != sorted(PDS):
        raise ValueError(f"{DOC}: the discrepancy register no longer prints the discrepancies of the record")

    def pdref(pid, sec="pds"):
        return ref(sec, pdrow[pid], rows=pdrow, caption=pd_cap, label="tbl-discrepancies")

    def tref(sec, tab, rows_, key):
        return ref(sec, rows_[key], tab, rows_)

    # ==== entities ===================================================================================
    q_step1 = Q("Cation exchange chromatography is Step 7 of the A-Mab drug substance process")
    q_step2 = Q("The antibody is bound to the resin and eluted by a step change in pH")
    q_step3 = Q("Cation exchange is Step 7 of this train.")
    q_step4 = Q("It receives the neutralized pool of the low-pH viral inactivation step")
    q_mode = Q("The step is operated in bind and elute mode on a resin with a sulfonate ligand.")
    q_sep = Q("Aggregate binds more strongly than monomer and elutes later")
    step = S.ProcessStep(
        step_id=STEP_ID, step_name=UO_NAME, step_number=str(G.CXSTEP), unit_operation=UO_NAME,
        description=("Step 7 of the A-Mab drug substance process and its principal aggregate polishing step, operated "
                     "in bind and elute mode on a resin with a sulfonate ligand. The antibody is bound to the resin and "
                     "eluted by a step change in pH; the pool is collected between a threshold on the ascending edge of "
                     "the elution peak and the stop collect threshold on its descending edge, both read as absorbance "
                     "at 280 nm. Aggregate binds more strongly than monomer and elutes later, so the step separates the "
                     "two by where the pool is cut. The step clears host cell protein, residual DNA, leached Protein A "
                     "and part of the fragments, sets no quality attribute of its own and claims no viral clearance."),
        input_materials=["neutralized pool of the low-pH viral inactivation step"],
        output_materials=["eluate pool (load of anion exchange)"],
        equipment=[SDM_NAME, CHAMBER_NAME],
        source_references=[ref("exec", q_step1), ref("exec", q_step2), ref("uo", q_step3), ref("uo", q_step4),
                           ref("uo", q_mode), ref("uo", q_sep)],
        metadata=meta())
    q_sdm_exec = Q("The characterization studies ran from", "on a scale-down model of the commercial column")
    q_sdm1 = Q("The scale-down model is a laboratory column of the commercial resin type")
    q_sdm2 = Q("Load is expressed in grams of antibody per litre of resin")
    q_eq1 = Q("The record names an instrumented system for the response-surface study only")
    q_eq2 = Q("It was in calibration for the whole study, which closed on")
    equipment = [
        S.Equipment(equipment_id=SDM_ID, equipment_name=SDM_NAME,
                    equipment_type="chromatography column (scale-down model)", site_name=P.SENDING_SITE,
                    source_references=[ref("exec", q_sdm_exec), ref("sdm", q_sdm1), ref("sdm", q_sdm2)],
                    metadata=meta()),
        S.Equipment(equipment_id=CHAMBER_ID, equipment_name=CHAMBER_NAME,
                    equipment_type="instrumented chromatography system (scale-down)", site_name=P.SENDING_SITE,
                    source_references=[ref("operation", q_eq1), ref("operation", q_eq2),
                                       tref("operation", win_t, winrow, "S-CEX-RSM")],
                    metadata=meta())]
    if CHR_EQ := ns["CHR"].loc["S-CEX-RSM", "equipment"]:
        if f"equip:{CHR_EQ}" != CHAMBER_ID:
            raise ValueError(f"{DOC}: the response-surface study no longer names {CHAMBER_ID}")
    sites = G._site_entities(DOC, FILE, _sid("title"))

    # -- parameters: the table row, the code row, the PAR rows and the sentences of the classification ------
    cls_quotes = {
        "load": [Q("Protein load was classified as a WC-CPP."),
                 Q("It affects aggregate, through its main effect and its interactions with pH and stop collect"),
                 Q("Its proven acceptable range is the range studied, `{python} f\"{MARG['load']:g}\"` g/L resin")],
        "wash_cond": [Q("Load/wash conductivity was classified as a WC-CPP."),
                      Q("It affects host cell protein, through its main effect and its interaction with pH"),
                      Q("Its proven acceptable range is the range studied, `{python} f\"{MARG['wash_cond']:g}\"`")],
        "elution_ph": [Q("Elution buffer pH was classified as a WC-CPP."),
                       Q("It affects aggregate, through its main effect and its interactions with load and stop"),
                       Q("Its proven acceptable range is the range studied, `{python} f\"{MARG['elution_ph']:g}\"`")],
        "stop_collect": [Q("Elution stop collect was classified as a WC-CPP."),
                         Q("It affects aggregate, through its main effect, its curvature and its interactions"),
                         Q("Its proven acceptable range is the range studied, "
                           "`{python} f\"{MARG['stop_collect']:g}\"`")],
        "flow": [Q("Elution flow rate was classified as a GPP."),
                 Q("The class rests on a judgement of practical relevance, for which no plan sets a threshold."),
                 Q("This report therefore judges the effect too small to move residual DNA appreciably")],
    }
    head = "Classified {c} under SOP-4001 by the decision logic of PCMP-001 §7.7. "
    rationale = {
        "load": t("It affects aggregate, through its main effect and its interactions with elution buffer pH and "
                  "elution stop collect, and host cell protein, through its main effect. With the other factors at "
                  "their set-points, aggregate rises from `{python} num(AG_L[0])` % to `{python} num(AG_L[1])` % and "
                  "host cell protein from `{python} num(HC_L[0])` to `{python} num(HC_L[2])` ng/mg across the range of "
                  "`{python} prng('load', 'range')`. Its proven acceptable range for both attributes is the range "
                  "studied, `{python} f\"{MARG['load']:g}\"` g/L resin beyond each end of its NOR, and the load is set "
                  "by the mass of antibody applied per litre of resin."),
        "wash_cond": t("It affects host cell protein, through its main effect and its interaction with elution buffer "
                       "pH, and has no demonstrated effect on aggregate. Host cell protein falls from "
                       "`{python} num(HC_W[0])` to `{python} num(HC_W[1])` ng/mg across "
                       "`{python} prng('wash_cond', 'range')`. Its proven acceptable range is the range studied, "
                       "`{python} f\"{MARG['wash_cond']:g}\"` mS/cm beyond each end of its NOR."),
        "elution_ph": t("It affects aggregate, through its main effect and its interactions with protein load and "
                        "elution stop collect, and host cell protein through its interaction with conductivity. "
                        "Aggregate rises from `{python} num(AG_P[0])` % to `{python} num(AG_P[1])` % across "
                        "`{python} prng('elution_ph', 'range')`. Its proven acceptable range is the range studied, "
                        "`{python} f\"{MARG['elution_ph']:g}\"` pH units beyond each end of its NOR, the narrowest "
                        "margin of the four."),
        "stop_collect": t("It affects aggregate, through its main effect, its curvature and its interactions with load "
                          "and pH, in the direction opposite to the expectation of PCP-007 §4.1, for which the report "
                          "gives no cause. Aggregate is `{python} num(AG_S[0])` %, `{python} num(AG_S[1])` % and "
                          "`{python} num(AG_S[2])` % at the low end, the set-point and the high end of its range. Its "
                          "proven acceptable range is the range studied, `{python} f\"{MARG['stop_collect']:g}\"` AU "
                          "beyond each end of its NOR."),
        "flow": t("The class rests on a judgement of practical relevance, for which no plan sets a threshold. No "
                  "difference was detected in aggregate or host cell protein, and every result at both ends of the "
                  "range studied, `{python} prng('flow', 'range')`, met its criterion. Residual DNA clearance was "
                  "`{python} f\"{-FLOW['dna_lrv']['diff']:.2f}\"` log10 lower at the high end "
                  "(`{python} pq(FLOW['dna_lrv']['p'])`), so residual DNA is affected under PCMP-001 §6.2; the "
                  "difference is a factor of `{python} f\"{DNA_FLOW_F:.1f}\"` in the residual DNA of the pool, and if "
                  "the whole factor reached the drug substance its capability index would be "
                  "`{python} f\"{CPK_DNA_AT_F:.2f}\"`, above the target, so the report judges the effect too small to "
                  "move residual DNA appreciably in the drug substance. For step yield the study cannot exclude an "
                  "effect as large as that of protein load, and for fragments, which were not measured, the class "
                  "rests on the mechanism alone."),
    }
    params = []
    for name, row in prow.items():
        k = pkey[name]
        r = pdf_.loc[name]
        unit = r["Unit"]
        refs = [ref("factors", row, pt_t, prow)]
        if k in FAC:
            refs.append(tref("factors", lg_t, lgrow, name))
            refs += [tref("par", par_t, parrow, (resp, name)) for resp in ("aggregate_out_pct", "hcp_out_ng_mg")]
            par_ = _cells(parrow[("aggregate_out_pct", name)])[5]
            if par_ != _cells(parrow[("hcp_out_ng_mg", name)])[5]:
                raise ValueError(f"{DOC}: the NOR-propagated PARs of {name} differ between the two attributes")
            par_str = f"{par_} {unit}"
        else:
            refs += [tref("flow", fc_t, fcrow, fc) for fc in ("Residual DNA clearance (log10)", "Step yield (points)")]
            par_str = None
        refs += [ref("class", x) for x in cls_quotes[k]]
        params.append(S.ProcessParameter(
            parameter_id=PC[name], parameter_name=name, parameter_type=r["Class"], unit=unit,
            target_value=f"{r['Set-point']} {unit}", NOR=f"{r['NOR']} {unit}", PAR=par_str,
            associated_step=STEP_LABEL, rationale_for_criticality=head.format(c=r["Class"]) + rationale[k],
            study_type=r["Study type"].lower(), source_references=refs, metadata=meta()))
        if r["Class"] != ns["CLS"][k]:
            raise ValueError(f"{DOC}: the class of {name} in the table is not the class of the configuration")

    # -- attributes: the register row, the row of the criterion derivation and the row of the outputs against
    # their criteria (for the three outputs with a criterion), and the sentences that place each attribute -----
    q_agg = Q("Aggregate has the highest criticality of the five and is the attribute the step exists to control.")
    q_hcp = Q("Host cell protein is cleared here and at anion exchange, so the pool of this step must be one that")
    q_frag = Q("Fragments were measured by nrCE-SDS in the response-surface design")
    q_dnalpa = Q("Residual DNA and leached Protein A were measured across the step so that their clearance is known.")
    q_dna = Q("The residual DNA criterion of ≤")
    q_lpa = Q("Leached Protein A is judged in the Protein A pool, against a criterion of")
    q_noagg = Q("No later step removes aggregate, and UF/DF adds a little within its NOR.")
    q_nofrag = Q("No later step changes fragments in the derivation")
    attr_prose = {"aggregates_hmw": [("cqa", q_agg), ("uo", q_noagg)],
                  "hcp": [("cqa", q_hcp)],
                  "fragments_lmw": [("cqa", q_frag), ("basis", q_nofrag)],
                  "residual_dna": [("cqa", q_dnalpa), ("cqa", q_dna)],
                  "leached_protein_a": [("cqa", q_dnalpa), ("basis", q_lpa)]}
    method_of = {"aggregates_hmw": "AMV-3011", "hcp": "AMV-3012", "fragments_lmw": "AMV-3020",
                 "residual_dna": "AMV-3014", "leached_protein_a": "AMV-3016", "step_yield": "AMV-3019"}
    analyte_of = {"aggregates_hmw": "Aggregate (HMW)", "hcp": "Host cell protein", "fragments_lmw": "Fragments (LMW)",
                  "residual_dna": "Residual DNA", "leached_protein_a": "Leached Protein A",
                  "step_yield": "Step yield (antibody mass)"}
    for k_, a_ in method_of.items():
        if md_df.loc[a_, "Analyte"] != analyte_of[k_]:
            raise ValueError(f"{DOC}: the methods summary no longer pairs {k_} with {a_}")
    lpa_crit = t("≤ `{python} num(UP_PA_LPA['iac_high'])` ppm (intermediate acceptance criterion of the Protein A pool, "
                 "carried back through the platform worst cases of cation exchange and anion exchange)")
    attrs = []
    for key in ckeys:
        r = cq_df.loc[key]
        crit = [f"{r['Acceptance']} (drug substance)"]
        refs = [ref("cqa", crow[key], cq_t, crow)]
        if key in CRIT_KEYS:
            ic = _cells(irow[key])
            ia = IAC.loc[attr_resp[key]]
            apriori = T.crit(ia["iac_low"], ia["iac_high_apriori"], ia["spec_type"])
            bas = _unmark(ic[-1])
            crit.append(f"{_unmark(ic[-2])} {reg.loc[key, 'unit']} (intermediate acceptance criterion in force, pool "
                        f"of the step; {bas[0].lower() + bas[1:]}, a priori {apriori})")
            refs += [ref("basis", irow[key], iac_t, irow), ref("criteria", crrow[key], cr_t, crrow)]
        else:
            crit.append("no criterion at this step" + (f"; {lpa_crit}" if key == "leached_protein_a" else
                                                       "; judged on the drug substance only"))
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=names[key], attribute_type="CQA",
            unit=reg.loc[key, "unit"], acceptance_criteria=crit, analytical_method=method_of[key],
            associated_steps=[STEP_LABEL],
            rationale_for_criticality=f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = {r['Tool #1']}.",
            criticality_level=r["Criticality"], tool1_score=int(r["Tool #1"]),
            tool2_severity=int(reg.loc[key, "tool2_severity"]),
            source_references=refs + [ref(s_, x) for s_, x in attr_prose[key]], metadata=meta()))

    # -- analytical methods: the procedure row, the methods-summary row, the sentence that names the method, and
    # for SEC and nrCE-SDS the row of the methods-by-study table -------------------------------------------
    q_dna_m = Q("Residual DNA was measured by quantitative polymerase chain reaction (qPCR, AMV-3014)")
    q_meth = {"AMV-3011": Q("Pool aggregate was measured by size exclusion chromatography (SEC, AMV-3011)"),
              "AMV-3012": Q("Host cell protein was measured by enzyme-linked immunosorbent assay (ELISA, AMV-3012)"),
              "AMV-3014": q_dna_m, "AMV-3016": q_dna_m,
              "AMV-3020": Q("Fragments are judged on nrCE-SDS results only (AMV-3020, under SOP-3015)."),
              "AMV-3019": Q("Step yield was calculated from the antibody mass in the load and in the pool"),
              "AMV-3221": Q("Aggregate in the pool of the run was verified by")}
    key_of = {v: k for k, v in method_of.items()}
    methods = []
    for amv in [a for a in sop_df["Reference"] if a.startswith("AMV-")]:
        key = key_of.get(amv, "aggregates_hmw")
        refs = [ref("basis_reg", soprow[amv], sop_t, soprow)]
        if amv in mdrow:
            refs.append(tref("app_d", md_t, mdrow, amv))
        refs.append(ref("dev2" if amv == "AMV-3221" else "analytics", q_meth[amv]))
        if amv in G.SIZE_VARIANT_TOKEN:
            refs += G.size_variant_refs(DOC, FILE, title("analytics"), [UO], G.SIZE_VARIANT_TOKEN[amv], text, lead=1)
        analyte = (md_df.loc[amv, "Analyte"] if amv in mdrow else "Aggregate (HMW), verification determinations")
        methods.append(S.AnalyticalMethod(
            method_id=amv, method_name=amv_title[amv], method_type=METHOD_TYPE.get(amv), analytes=[analyte],
            associated_attributes=[f"attr:{key}"], validation_status="validated", source_references=refs,
            metadata=meta()))

    # -- capability: one record per row of the capability table ----------------------------------------
    q_cap_all = Q("Every index exceeds the target of")
    q_cap_hcp = Q("Host cell protein has the lowest index")
    q_cap_lpa = Q("The index of leached Protein A, ")
    q_cap_dna = Q("The simulated drug substance carries")
    cap_prose = {"aggregates_hmw": q_cap_all, "fragments_lmw": q_cap_all, "hcp": q_cap_hcp,
                 "residual_dna": q_cap_dna, "leached_protein_a": q_cap_lpa}
    NMC = int(ns["NMC"])
    capab = []
    for key, row in caprow.items():
        c = cap_df.loc[key]
        mean_, sd_ = [x.strip() for x in c["Mean ± SD"].split("±")]
        capab.append(ProcessCapability(
            capability_id=f"{DOC}-CAP{len(capab) + 1:02d}", quality_attribute=f"attr:{key}", index_name="Cpk",
            index_value=_num(c["Cpk"]), specification_side="upper", acceptance_range=c["Criterion"],
            mean=mean_, standard_deviation=sd_, unit=reg.loc[key, "unit"], basis="simulated", n_batches=NMC,
            unit_operation=UO_NAME,
            source_references=[ref("cap", row, cap_t, caprow), ref("cap", cap_prose[key])],
            metadata=meta()))

    # -- fitted models ---------------------------------------------------------------------------------
    cen = {k: _cells(row) for k, row in cenrow.items()}
    fits = []

    def fit_rec(resp, form, refs, **kw):
        fits.append(StatisticalModelFit(
            model_fit_id=f"{DOC}-FIT{len(fits) + 1:02d}", response=resp, unit_operation=UO_NAME,
            model_form=form, source_references=refs, metadata=meta(), **kw))

    def coef_terms(resp):
        """The terms of the coefficient table of a selected model, besides the intercept, as printed."""
        rows_ = ({k_[1]: r_ for k_, r_ in corow.items() if k_[0] == resp} if resp != "step_yield" else ycrow)
        out_ = []
        for term, r_ in rows_.items():
            if term == "Intercept":
                continue
            c_ = _cells(r_)[-5:] if resp != "step_yield" else _cells(r_)
            # (term, coefficient, SE, t, p)
            out_.append(ModelTerm(term=term, factor=tname(term), coefficient=_num(c_[1]), standard_error=_num(c_[2]),
                                  t_statistic=_num(c_[3]), p_value=_num(c_[4]), significant=sig_of(c_[4])))
        return out_

    def scr_terms(resp):
        out_ = []
        for (o_, term), r_ in serow.items():
            if o_ != se_lab[resp]:
                continue
            c_ = _cells(r_)
            out_.append(ModelTerm(term=term, factor=tname(term), effect=_num(c_[2]), standard_error=_num(c_[3]),
                                  t_statistic=_num(c_[4]), p_value=_num(c_[5]), significant=sig_of(c_[5])))
        return out_

    def summ(resp):
        c = _cells(msrow[resp])     # Output | Scale | Terms | R² | Adj. R² | Pred. R² | Gap | Model p | LoF p | Crit 4 | Adequate
        return dict(scale=c[1], terms=c[2], r2=c[3], adj=c[4], pred=c[5], gap=c[6], p=c[7], lof=c[8], c4=c[9],
                    adequate=c[10])

    def resid(resp):
        c = _cells(rdrow[resp])     # Output | Spread p | Order p | Largest Cook's | Flag limit | F median | Runs | Crit 4
        return dict(spread=c[1], order=c[2], cook=c[3], flag=c[4], fmed=c[5], over=c[6], met=c[7])

    def centre_kw(resp):
        cc = cen[("Response surface", LAB[resp])]
        return dict(replicate_n=int(cc[2]), replicate_mean=cc[3], replicate_sd=cc[4], replicate_cv=cc[5])

    # the full quadratic model PCP-007 §5.5 planned, on the planned runs (re-evaluation table)
    q_full = Q("The plan's full quadratic model was adequate on the planned runs for aggregate and host cell protein")
    q_full_f = Q("For fragments the full quadratic failed the limit on overfitting by a wide margin.")
    for key, row in rvrow.items():
        c = _cells(row)                 # Attribute | Runs | R² | Pred. R² | Gap | Model used
        resp = attr_resp[key]
        fit_rec(resp, "full quadratic (planned, PCP-007 §5.5)",
                [ref("rsm", row, rv_t, rvrow), ref("rsm", q_full_f if key == "fragments_lmw" else q_full)],
                n_runs=int(c[1]), r_squared=_num(c[2]), predicted_r_squared=_num(c[3]),
                adequacy_statement=(f"Planned full quadratic on the {c[1]} planned runs: R² {c[2]}, predicted R² "
                                    f"{c[3]}, R² minus predicted R² {c[4]}"
                                    + (", above the limit on overfitting" if _num(c[4]) > float(ns["GAPMAX"])
                                       else ", within the limit on overfitting")
                                    + f". Not used for any conclusion of Version 2.0; the model used under the model "
                                      f"selection (PD-007-01): {_unmark(c[5])}"
                                    + (" (no adequate model; the output is judged on its measured results)."
                                       if c[5].endswith(" a)") else ".")))

    # aggregate: log scale, eight terms, meets all four adequacy criteria
    a_, i_ = summ("aggregate_out_pct"), resid("aggregate_out_pct")
    mod, lof = _cells(anrow[("aggregate_out_pct", "Model")]), _cells(anrow[("aggregate_out_pct", "Lack of fit")])
    q_agg_m1 = Q("The aggregate model on the log scale has")
    q_agg_m2 = Q("The model F-test is significant (`{python} pq(FA['p'])`)")
    q_agg_m3 = Q("The residuals show no trend against the predicted values (`{python} pq(RI['aggregate_out_pct']")
    fit_rec("aggregate_out_pct", t("selected model (PD-007-01), log scale, terms besides the intercept: "
                                   "`{python} words('aggregate_out_pct')`"),
            [ref("rsm_agg", q_agg_m1), ref("rsm_agg", q_agg_m2), ref("rsm_agg", q_agg_m3),
             tref("rsm", ms_t, msrow, "aggregate_out_pct"), tref("rsm", rd_t, rdrow, "aggregate_out_pct"),
             tref("rsm_agg", an_t, anrow, ("aggregate_out_pct", "Model")),
             tref("rsm_agg", an_t, anrow, ("aggregate_out_pct", "Lack of fit")),
             tref("centre", cen_t, cenrow, ("Response surface", LAB["aggregate_out_pct"]))]
            + [tref("rsm_agg", co_t, corow, k_) for k_ in corow if k_[0] == "aggregate_out_pct"],
            n_runs=int(FIT["aggregate_out_pct"]["n"]), r_squared=_num(a_["r2"]), adjusted_r_squared=_num(a_["adj"]),
            predicted_r_squared=_num(a_["pred"]), f_statistic=_num(mod[5]), p_value=_num(mod[6]),
            lack_of_fit_p=_num(lof[6]),
            adequacy_statement=(
                f"Meets the four adequacy criteria of PCMP-001 §7.2: model F-test p {a_['p']}, lack of fit p "
                f"{a_['lof']}, R² minus predicted R² {a_['gap']}; residual trends p {i_['spread']} (spread) and "
                f"{i_['order']} (order); runs {i_['over']} above 4/n = {i_['flag']}, none above the median of F(p, n − p) "
                f"of {i_['fmed']} (largest Cook's distance {i_['cook']}). On the log scale each parameter multiplies the "
                f"output by a fixed factor; the conductivity term is kept by the selection although not significant."),
            terms=coef_terms("aggregate_out_pct"), **centre_kw("aggregate_out_pct"))
    # host cell protein: log scale, six terms, fails the fourth criterion on the order of execution
    a_, i_ = summ("hcp_out_ng_mg"), resid("hcp_out_ng_mg")
    mod, lof = _cells(anrow[("hcp_out_ng_mg", "Model")]), _cells(anrow[("hcp_out_ng_mg", "Lack of fit")])
    q_hcp_m1 = Q("The host cell protein model on the log scale has")
    q_hcp_m2 = Q("The model does not meet the fourth criterion.")
    q_hcp_m3 = Q("Its residuals fall with the order of execution")
    fit_rec("hcp_out_ng_mg", t("selected model (PD-007-01), log scale, terms besides the intercept: "
                               "`{python} words('hcp_out_ng_mg')`"),
            [ref("rsm_hcp", q_hcp_m1), ref("rsm_hcp", q_hcp_m2), ref("rsm_hcp", q_hcp_m3),
             tref("rsm", ms_t, msrow, "hcp_out_ng_mg"), tref("rsm", rd_t, rdrow, "hcp_out_ng_mg"),
             tref("rsm_agg", an_t, anrow, ("hcp_out_ng_mg", "Model")),
             tref("rsm_agg", an_t, anrow, ("hcp_out_ng_mg", "Lack of fit")),
             tref("centre", cen_t, cenrow, ("Response surface", LAB["hcp_out_ng_mg"]))]
            + [tref("rsm_agg", co_t, corow, k_) for k_ in corow if k_[0] == "hcp_out_ng_mg"],
            n_runs=int(FIT["hcp_out_ng_mg"]["n"]), r_squared=_num(a_["r2"]), adjusted_r_squared=_num(a_["adj"]),
            predicted_r_squared=_num(a_["pred"]), f_statistic=_num(mod[5]), p_value=_num(mod[6]),
            lack_of_fit_p=_num(lof[6]),
            adequacy_statement=t(
                f"Meets the first three adequacy criteria of PCMP-001 §7.2 (model F-test p {a_['p']}, lack of fit p "
                f"{a_['lof']}, R² minus predicted R² {a_['gap']}) and fails the fourth: the residuals fall with the "
                f"order of execution (p {i_['order']}), with no trend against the predicted values (p {i_['spread']}); "
                f"runs {i_['over']} above 4/n, none above the median of F(p, n − p). The drift amounts to a factor of "
                "`{python} f\"{HCP_DRIFT_F:.2f}\"` over the study; added to the highest single-run limit over the NOR it "
                "gives `{python} num(HCP_UPL_DRIFT)` ng/mg, below the criterion. Used for the ranges and the design "
                "space although it fails the fourth criterion (PD-007-02); the curvature in load is kept for "
                "prediction and not claimed as a finding."),
            terms=coef_terms("hcp_out_ng_mg"), **centre_kw("hcp_out_ng_mg"))
    # fragments: raw scale, not adequate (limit on overfitting)
    a_, i_ = summ("lmw_cesds_pct"), resid("lmw_cesds_pct")
    q_fr1 = Q("Fragments have no adequate model. The selected model keeps", "Fragments have no adequate model.")
    q_fr2 = Q("The selected model keeps `{python} words('lmw_cesds_pct')` on the raw scale.")
    q_fr3 = Q("Its F-test is significant (`{python} pq(FF['p'])`)")
    fit_rec("lmw_cesds_pct", t("selected model (PD-007-01), raw scale, terms besides the intercept: "
                               "`{python} words('lmw_cesds_pct')`; not adequate"),
            [ref("rsm_frag", q_fr1), ref("rsm_frag", q_fr2), ref("rsm_frag", q_fr3),
             tref("rsm", ms_t, msrow, "lmw_cesds_pct"), tref("rsm", rd_t, rdrow, "lmw_cesds_pct")],
            n_runs=int(FIT["lmw_cesds_pct"]["n"]), r_squared=_num(a_["r2"]), adjusted_r_squared=_num(a_["adj"]),
            predicted_r_squared=_num(a_["pred"]), p_value=_num(a_["p"]), lack_of_fit_p=_num(a_["lof"]),
            adequacy_statement=(
                f"Not adequate by PCMP-001 §7.2: R² minus predicted R² is {a_['gap']}, above the limit on overfitting, "
                f"although the model F-test is significant (p {a_['p']}) and the lack of fit is not (p {a_['lof']}). "
                f"Fragments are judged on their measured results; no range and no predicted level is derived from the "
                f"model, and no coefficient table is given for it."),
            terms=[ModelTerm(term=ns["D"]._term_label(tm, LET), factor=ns["tname"](tm)) for tm in TERMS["lmw_cesds_pct"]],
            **centre_kw("lmw_cesds_pct") if ("Response surface", LAB["lmw_cesds_pct"]) in cen else {})
    # step yield: raw scale, no criterion
    a_, i_ = summ("step_yield"), resid("step_yield")
    q_y1 = Q("Its selected model on the raw scale keeps")
    q_y2 = Q("The selected model has no stop collect term.")
    fit_rec("step_yield", t("selected model (PD-007-01), raw scale, terms besides the intercept: "
                            "`{python} words('step_yield')`"),
            [ref("rsm_yield", q_y1), ref("rsm_yield", q_y2), tref("rsm", ms_t, msrow, "step_yield"),
             tref("rsm", rd_t, rdrow, "step_yield")]
            + [tref("app_c", yc_t, ycrow, k_) for k_ in ycrow],
            n_runs=int(FIT["step_yield"]["n"]), r_squared=_num(a_["r2"]), adjusted_r_squared=_num(a_["adj"]),
            predicted_r_squared=_num(a_["pred"]), p_value=_num(a_["p"]), lack_of_fit_p=_num(a_["lof"]),
            adequacy_statement=(
                f"Step yield has no criterion and is reported for information. Model F-test p {a_['p']}, lack of fit p "
                f"{a_['lof']}, R² minus predicted R² {a_['gap']}; criterion on residuals and influential runs "
                f"{i_['met']}. Coefficients in percentage points per coded unit. With run 14 deleted the selection "
                f"replaces the load × conductivity interaction with a stop collect term."),
            terms=coef_terms("step_yield"), **centre_kw("step_yield"))
    # the screening models: main effects and two-factor interactions, used to identify effects only
    q_scr_id = Q("The screening model identifies effects.")
    for resp, row in sfrow.items():
        c = _cells(row)                   # Response | R² | Adj. R² | Pred. R² | Model p | Lack of fit p | Residual SD
        cs_ = cen[("Screening", LAB[resp])]
        fit_rec(resp, "screening model: all main effects and all two-factor interactions in coded units",
                [ref("screening", row, sf_t, sfrow), tref("centre", cen_t, cenrow, ("Screening", LAB[resp]))]
                + ([ref("stats", q_scr_id)] if resp == "aggregate_out_pct" else [])
                + [tref("app_c", se_t, serow, k_) for k_ in serow if k_[0] == se_lab[resp]],
                n_runs=int(ns["N_SCR"]), r_squared=_num(c[1]), adjusted_r_squared=_num(c[2]),
                predicted_r_squared=_num(c[3]), p_value=_num(c[4]), lack_of_fit_p=_num(c[5]), rmse=_num(c[6]),
                adequacy_statement=(f"Screening model, read for the effects it identifies and used for no prediction "
                                    f"(no quadratic terms, so it cannot describe curvature); model p {c[4]}, lack of "
                                    f"fit p {c[5]} against {ns['FS']['aggregate_out_pct']['df_pe']} degrees of "
                                    f"freedom for pure error, a weak test."),
                terms=scr_terms(resp), replicate_n=int(cs_[2]), replicate_mean=cs_[3], replicate_sd=cs_[4],
                replicate_cv=cs_[5])
    # the clearance of residual DNA (no term) and the pool level of leached Protein A (load, not claimed)
    q_dna_f1 = Q("The selected model of the clearance factor, on the log scale, has no term.")
    q_dna_f2 = Q("Within the range studied, therefore, the clearance of residual DNA does not depend on any")
    fit_rec("dna_clearance_factor", "selected model, log scale, intercept only (clearance factor of residual DNA, "
                                    "load over pool)",
            [ref("dna_lpa", q_dna_f1), ref("dna_lpa", q_dna_f2)], n_runs=int(ns["N_RSM"]), terms=[],
            adequacy_statement="Intercept-only model: within the range studied the clearance of residual DNA does not "
                               "depend on any of the four parameters, at the precision of the runs and of the qPCR "
                               "method.")
    q_lpa_f1 = Q("The model selection applied to the")
    q_lpa_f2 = Q("That fit leaves out the")
    lpa_fit = ns["LPA_FIT"]
    fit_rec("lpa_pool_ppm", "selected model, log scale, terms besides the intercept: protein load (quantified pools only)",
            [ref("dna_lpa", q_lpa_f1), ref("dna_lpa", q_lpa_f2)], n_runs=int(lpa_fit["n"]),
            p_value=float(lpa_fit["model"].pvalues["load"]),
            adequacy_statement=t("Fitted to the `{python} N_RSM - N_LPA_LOQ` pools quantified above the LOQ; it leaves "
                                 "out the `{python} N_LPA_LOQ` results below the LOQ, which include results at the "
                                 "highest load, so no dependence of leached Protein A on load is claimed."),
            terms=[ModelTerm(term="A", factor=pn["load"], coefficient=float(lpa_fit["model"].params["load"]),
                             p_value=float(lpa_fit["model"].pvalues["load"]))])

    # -- study events --------------------------------------------------------------------------------------
    DEVF = ns["DEVF"]
    dev_prose = {
        "DEV-007-01": [("dev1", Q("The load/wash buffer used in screening run")),
                       ("dev1", Q("The expiry was found in the documentation review after the study.")),
                       ("dev1", Q("The record gives the cause as an expiry date not checked at preparation.")),
                       ("dev1", Q("With the run excluded, the screening models find the same significant terms for all")),
                       ("dev1", Q("The screening design identifies effects and sets no range, so the run was retained."))],
        "DEV-007-02": [("dev2", Q("During response-surface run")),
                       ("dev2", Q("The excursion was found in the equipment history review of the chamber")),
                       ("dev2", Q("With the run excluded and the selection repeated, the host cell protein model keeps")),
                       ("dev2", Q("Both outputs still meet their criteria over the NOR, with highest single-run limits")),
                       ("dev2", Q("The run was retained."))],
    }
    dev_impact = {
        "DEV-007-01": t("The retained sample of lot `{python} LOT['id']`, expired on `{python} LOT['expiry']`, was "
                        "re-tested under `{python} SOP2103['id']`; the record gives no acceptance range for the values, "
                        "so the report does not judge the lot from them. The impact was judged from the data: the "
                        "studentized residuals of run `{python} RUN6` on the screening models were small, and with the "
                        "run excluded the screening models find the same significant terms for all three outputs. The "
                        "screening design identifies effects and sets no range, so the run was retained."),
        "DEV-007-02": t("Temperature is not a factor of the designs. The verification of aggregate by "
                        "`{python} dev_007_02_ver_n` SEC determinations under AMV-3221 decides nothing, because the "
                        "record gives neither their result nor a criterion. With run `{python} RUN14` excluded and the "
                        "selection repeated, aggregate and host cell protein still meet their criteria over the NOR "
                        "(highest single-run limits `{python} num(DEL14['aggregate_out_pct']['up_nor'])` % and "
                        "`{python} num(DEL14['hcp_out_ng_mg']['up_nor'])` ng/mg), the whole region studied still meets "
                        "them and the verification outcome is unchanged; the aggregate model loses its conductivity "
                        "term and the step yield model replaces its load × conductivity interaction with a stop collect "
                        "term. The run was retained."),
    }
    devs = []
    for did, row in devrow.items():
        c = _cells(row)
        devs.append(Deviation(
            deviation_id=did, summary=c[1], unit_operation=UO_NAME, detected_during=c[2], disposition=c[3],
            impact_statement=dev_impact[did], no_impact_on_conclusions=True,
            source_references=[ref("events", row, rows=devrow, caption=dev_cap, label="tbl-events")]
            + [ref(s_, x) for s_, x in dev_prose[did]],
            metadata=meta()))
        if str(DEVF.loc[did, "disposition"]) != "retained":
            raise ValueError(f"{DOC}: {did} is no longer retained; its record says it is")

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
    relation("executed_under", "PCP-007", "The report presents the Stage 1 characterization of the step under the plan "
             "PCP-007.", "exec", Q("This report presents the Stage 1 characterization of the step under the plan PCP-007",
                                   "under the plan PCP-007"))
    relation("executed_under", "PCMP-001", "PCMP-001 sets the common approach of the campaign, and PCP-007 applies it to "
             "the step.", "basis_reg", Q("The master plan PCMP-001 sets the common approach of the campaign"))
    relation("rolls_up_into", "PCMR-001", "The results of the report roll up, with those of the other steps, into the "
             "master report PCMR-001.", "cs", Q("The results of this report roll up, with those of the other steps"))
    relation("references", "PTP-001", "The process is being transferred from the development site to the commercial "
             "drug substance site under PTP-001.", "uo", Q("The process is being transferred from the development site"))
    relation("scoped_by", "RA-001", "Prior knowledge and RA-001 identified the parameters that may affect the quality "
             "attributes, and the risk ranking of RA-001 assigned the parameters to the multivariate designs, the "
             "univariate assessment or no new study.", "risk",
             Q("All process parameters of the step were carried into the risk ranking and filtering of RA-001",
               "risk ranking and filtering of RA-001"))
    q_inv = Q("It found that the criteria used to judge each step in the proven acceptable range analysis")
    relation("references", "INV-001", "Version 2.0 is issued under INV-001, which found that the criteria used in the "
             "proven acceptable range analysis had been set after the data were seen.", "changes", q_inv)
    relation("references", "INV-002", "INV-002 judged the response-surface models against the first three adequacy "
             "criteria of PCMP-001 §7.2; its corrective action CA3 analyses every response-surface output by model "
             "selection.", "changes", Q("Its corrective action CA3, adopted on"))
    relation("references", "PCR-006", "Two studies of the low-pH viral inactivation report PCR-006 (S-CEX-VER and S-VI-WC) "
             "ran this step on its scale-down model; their results and decisions belong to PCR-006.", "verif",
             Q("Both studies, their results and their decisions belong to PCR-006."))
    relation("references", "PCR-008", "The anion exchange report PCR-008 verified the platform worst case of anion "
             "exchange, and its bound widened the host cell protein criterion of this step.", "basis",
             Q("The anion exchange report PCR-008 verified that worst case"))
    relation("references", "PCR-010", "The UF/DF report PCR-010 gives the one-sided bound of the aggregate rise across "
             "UF/DF that tightens the aggregate criterion of this pool.", "basis",
             Q("The UF/DF report PCR-010 gives the one-sided"))
    relation("references", "PCR-003", "The verification of this report tightened the aggregate criteria of the low-pH "
             "pool and the bioreactor harvest, which PCR-006 and PCR-003 judge.", "cs",
             Q("The verification of this report tightened the aggregate criteria of the low-pH pool"))
    relation("references", "PCR-009", "Virus filtration removes virus (PCR-009); cation exchange claims no viral "
             "clearance.", "cs", Q("Virus filtration removes virus (PCR-009)."))

    # -- explicit non-claims, by section --------------------------------------------------------------------
    ncs, nc_at = [], {}

    def nclaim(sec, subject, statement, quotes, rationale=None, elsewhere=None):
        ncs.append(ExplicitNonClaim(
            non_claim_id=f"{DOC}-NC{len(ncs) + 1:02d}", subject=subject, unit_operation=UO_NAME,
            statement=statement, rationale=rationale, handled_elsewhere=elsewhere,
            source_references=[ref(s_, x) for s_, x in quotes], metadata=meta()))
        nc_at.setdefault(sec, []).append(ncs[-1])

    nclaim("uo", "viral clearance", "No viral clearance is claimed for cation exchange.",
           [("uo", Q("No viral clearance is claimed for cation exchange.")),
            ("cs", Q("Cation exchange claims no viral clearance."))],
           elsewhere="PCR-006, PCR-008, PCR-009")
    nclaim("uo", "quality attributes set at the step", "No quality attribute is set at this step; the drug substance "
           "register assigns none to it.",
           [("uo", Q("No quality attribute is set at this step.")),
            ("cqa", Q("The drug substance register assigns no quality attribute to this step."))])
    nclaim("changes", "change of NOR or set-point", "No NOR or set-point of the step was changed at Version 2.0.",
           [("changes", Q("The NOR and the set-point of each parameter of this step are the ones the studies were"))])
    nclaim("sdm", "scale-down offset of fragments", "Fragments were not compared at the two scales, so their offset is "
           "unknown rather than zero, and they are judged as the scale-down model gives them.",
           [("sdm", Q("The qualification did not compare fragments at both scales, so their offset is unknown, not zero.")),
            ("sdm", Q("Fragments are judged as the scale-down model gives them (PCMP-001 §7.1)."))],
           rationale="It rests on the assumption of PCP-007 §12 that fragments separate in the same way at both scales.")
    nclaim("sdm", "conclusions on the residual DNA offset", "No conclusion of the report depends on the offset of "
           "residual DNA, which has no criterion at this step.",
           [("sdm", Q("Residual DNA has no criterion at this step, so no conclusion of this report depends on its"))],
           elsewhere="PD-007-04")
    nclaim("analytics", "SEC fragment results of the screening design", "The SEC fragment results of the screening design "
           "are kept in the record and are not used for any decision; its samples were not retained for a retest by "
           "nrCE-SDS.", [("analytics", Q("Its samples were not retained for a retest by nrCE-SDS"))])
    nclaim("analytics", "fragments in the flow-rate study", "The flow-rate study measured no fragments, so it supports "
           "no range for fragments and the class of flow rate for fragments rests on the mechanism alone.",
           [("analytics", Q("The flow-rate study measured no fragments")),
            ("flow", Q("Fragments were not measured, so the study supports no range for fragments."))])
    nclaim("stats", "capability of the step", "The capability of the step itself, which PCP-007 §5.5 asked for, was not "
           "estimated; capability is given for the drug substance from the integrated model.",
           [("stats", Q("PCP-007 §5.5 also asked for the capability of the step, from the fitted models over draws "
                        "within the NOR.")),
            ("cap", Q("The capability of the step itself, which PCP-007 §5.5 asked for, was not estimated"))],
           elsewhere="PD-007-10")
    nclaim("thresholds", "runs on a lot out of trend", "The identification of runs made on a lot out of trend could not "
           "be made, because the record names no feed lot and no load result.",
           [("thresholds", Q("This decision could therefore not be made."))], elsewhere="PD-007-05, PD-007-11")
    nclaim("screening", "cause of the screening host cell protein result", "The record gives no cause for the difference "
           "between screening run and response-surface run at the corner of highest load and lowest conductivity, and "
           "the report offers none.",
           [("screening", Q("The record gives no cause for it, and this report offers none."))])
    nclaim("rsm_hcp", "curvature of host cell protein in load", "The curvature in load of the host cell protein model is "
           "kept for prediction and is not claimed as a finding, because it is smaller than the spread of the centre "
           "points.", [("rsm_hcp", Q("PCP-007 §12 states that an effect smaller than the spread of the centre points"))])
    nclaim("rsm_hcp", "cause of the run-order drift", "The record gives no cause for the run-order drift of the host "
           "cell protein residuals.", [("rsm_hcp", Q("The record gives no cause for the drift."))],
           elsewhere="PD-007-02, PD-007-11")
    nclaim("rsm_frag", "range and effects for fragments", "No range and no predicted level is derived for fragments, "
           "and no effect on fragments is claimed from their model, which does not meet PCMP-001 §7.2.",
           [("rsm_frag", Q("Fragments are therefore judged on their measured results, and no range and no predicted")),
            ("rsm_frag", Q("The stop collect term of the fragment model has the direction expected"))])
    nclaim("dna_lpa", "dependence of leached Protein A on load", "The data do not show a dependence of leached Protein A "
           "on load, and none is claimed.",
           [("dna_lpa", Q("That fit leaves out the", "and none is claimed."))])
    nclaim("mech", "cause of the stop collect results", "The mechanism does not explain the rise of aggregate with the "
           "stop collect setting or the absence of a stop collect term in the yield model, and the report gives no cause.",
           [("mech", Q("The mechanism of @sec-platform does not explain these results"))])
    nclaim("mech", "cause of the pH × conductivity interaction", "The pH × conductivity interaction on host cell protein "
           "was not expected, and the mechanism does not explain it.",
           [("mech", Q("The pH × conductivity interaction was not expected"))])
    nclaim("ds", "confirmation of the design space at manufacturing scale", "The design space has not been confirmed at "
           "manufacturing scale near the edges of the ranges studied, and it holds only at the set-point of elution "
           "flow rate and within the qualified life of the resin.",
           [("ds", Q("The design space has not been confirmed at manufacturing scale")),
            ("ds", Q("The claim also holds only at the set-point of elution flow rate"))])
    nclaim("par", "proven acceptable range of fragments", "Fragments have no adequate model, and no proven acceptable "
           "range is derived for them.",
           [("par", Q("Fragments have no adequate model, and no proven acceptable range is derived for them."))])
    nclaim("par", "ranges beyond the range studied", "Every proven acceptable range is the range studied, and no claim is "
           "made beyond it.", [("par", Q("Every range is the range studied, so each proven acceptable range reaches"))])
    nclaim("par", "ranges from residual DNA, leached Protein A and step yield", "No range is derived from residual DNA, "
           "leached Protein A or step yield, which have no criterion at this step.",
           [("basis", Q("Residual DNA, leached Protein A and step yield have no criterion at this step"))])
    nclaim("verif", "verification of the leached Protein A worst case", "Leached Protein A is not a response of the "
           "designs, so its platform value stands without verification by a model.",
           [("verif", Q("Leached Protein A. Leached Protein A is not a response of the designs"))])
    nclaim("cs", "in-process control of the pool", "The report proposes no in-process control or monitoring of the pool "
           "beyond its four contributions to the control strategy.",
           [("cs", Q("This report proposes no in-process control or monitoring of the pool"))])
    nclaim("dev1", "judgement of the expired lot from its re-test", "The record gives no acceptance range for the re-test "
           "values of the expired lot, so the report does not judge the lot from them.",
           [("dev1", Q("The record gives no acceptance range for these values"))])
    nclaim("dev2", "verification of aggregate in run 14", "The record gives neither the result of the verification "
           "determinations of run 14 nor a criterion, so the verification decides nothing in the report.",
           [("dev2", Q("The record gives neither the result of these determinations nor a criterion"))])

    entities = [
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("exec"), process_steps=[step], sites=sites,
                                  equipment=equipment),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("uo"), document_relationships=rels,
                                  non_claims=nc_at["uo"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("changes"), non_claims=nc_at["changes"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cqa"), quality_attributes=attrs),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("sdm"), non_claims=nc_at["sdm"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("analytics"), analytical_methods=methods,
                                  non_claims=nc_at["analytics"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("stats"), non_claims=nc_at["stats"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("thresholds"), non_claims=nc_at["thresholds"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("factors"), parameters=params),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("screening"), non_claims=nc_at["screening"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("rsm"), model_fits=fits),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("rsm_hcp"), non_claims=nc_at["rsm_hcp"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("rsm_frag"), non_claims=nc_at["rsm_frag"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("dna_lpa"), non_claims=nc_at["dna_lpa"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("mech"), non_claims=nc_at["mech"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("ds"), non_claims=nc_at["ds"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("par"), non_claims=nc_at["par"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("verif"), non_claims=nc_at["verif"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cap"), capabilities=capab),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cs"), non_claims=nc_at["cs"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("record"), deviations=devs),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("dev1"), non_claims=nc_at["dev1"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("dev2"), non_claims=nc_at["dev2"]),
    ]

    # ==== studies: each on its row of the execution-window table, its prose, its data rows ======================
    names_fac = [NAME[k] for k in FAC]
    CHR = ns["CHR"]
    study_spec = {
        "S-CEX-SDM": dict(study_type="scale_down_qualification",
                          design_name="set-point runs of the scale-down model against manufacturing-scale batches",
                          responses=["step_yield", "aggregate_out_pct", "hcp_out_ng_mg", "dna_pool_pg_mg",
                                     "lpa_pool_ppm", "plates_per_m", "asymmetry"],
                          prose=[("sdm", Q("The qualification study S-CEX-SDM ran from")),
                                 ("sdm", Q("It compared `{python} N_SD_Q` scale-down runs at the set-point")),
                                 ("sdm", Q("The model is qualified for both outputs that carry a criterion."))],
                          rows=[("sdm", offrow[k_], off_t, offrow) for k_ in offrow]
                          + [("basis_reg", soprow["SOP-1001"], sop_t, soprow)]),
        "S-CEX-SCR": dict(study_type="screening_doe", design_name="two-level full factorial with centre points",
                          factors=names_fac, responses=["aggregate_out_pct", "hcp_out_ng_mg", "step_yield",
                                                        "lmw_sec_pct"],
                          n_runs=P.doe_runs(UO, "screening"), n_center_points=P.doe_centre_points(UO, "screening"),
                          prose=[("scr_design", Q("The screening study S-CEX-SCR ran from")),
                                 ("scr_design", Q("A full factorial was chosen over a fraction because protein load"))],
                          rows=[("app_a", r_, mtx["screening"][0], mtx["screening"][1])
                                for r_ in mtx["screening"][1].values()]),
        "S-CEX-RSM": dict(study_type="response_surface_doe", design_name="face-centred central composite design",
                          factors=names_fac, responses=["aggregate_out_pct", "hcp_out_ng_mg", "lmw_cesds_pct",
                                                        "step_yield", "lmw_sec_pct", "dna_pool_pg_mg",
                                                        "lpa_pool_ppm"],
                          n_runs=P.doe_runs(UO, "rsm"), n_center_points=P.doe_centre_points(UO, "rsm"),
                          prose=[("rsm_design", Q("The response-surface study S-CEX-RSM ran from")),
                                 ("rsm_design", Q("The axial runs sit on the faces of the cube"))],
                          rows=[("app_b", r_, mtx["rsm"][0], mtx["rsm"][1]) for r_ in mtx["rsm"][1].values()]
                          + [("app_b", r_, dna_t, dnarow) for r_ in dnarow.values()]),
        "S-CEX-UNI": dict(study_type="univariate", design_name="each end of the range in duplicate, other parameters "
                                                               "at their set-points",
                          factors=[NAME["flow"]], responses=["aggregate_out_pct", "hcp_out_ng_mg", "step_yield",
                                                             "dna_pool_pg_mg", "lpa_pool_ppm"],
                          prose=[("uni_design", Q("The flow-rate study S-CEX-UNI ran from")),
                                 ("uni_design", Q("Elution flow rate was run at each end of its range")),
                                 ("uni_design", Q("A study of one factor at a time cannot show whether flow rate"))],
                          rows=[("flow", r_, fl_t, flrow) for r_ in flrow.values()]),
    }
    studies, unrendered, untyped = [], [], []
    for sid_ in CHR[CHR["step"] == UO].index:
        if sid_ not in winrow or not G._present(winrow[sid_], text):
            unrendered.append(sid_)
            continue
        if sid_ not in study_spec:
            untyped.append(sid_)
            continue
        spec = dict(study_spec[sid_])
        prose_, rows_ = spec.pop("prose"), spec.pop("rows")
        refs = [ref("operation", winrow[sid_], win_t, winrow)]
        refs += [ref(s_, x) for s_, x in prose_]
        refs += [ref(s_, r_, tab_, rr_) for s_, r_, tab_, rr_ in rows_]
        refs += [pdref(p_) for p_, d_ in PDS.items() if sid_ in (d_.get("studies") or [])]
        studies.append(S.StudyDesign(
            study_id=f"study:{sid_}", unit_operation=UO_NAME, scale_down_model=SDM_NAME,
            associated_parameters=[PC[x] for x in spec.get("factors", [])],
            source_references=refs, metadata=meta(), **spec))
    if sorted(untyped) != ["S-CEX-FRC", "S-CEX-VER"]:
        raise ValueError(f"{DOC}: studies of the step with no study type: {untyped}")

    # ==== design space and the proven acceptable ranges =====================================================
    q_ds = [Q("The design space of the step is the region of its four multivariate parameters"),
            Q("Aggregate and host cell protein enter through their selected models, at manufacturing scale."),
            Q("They constrain the region through their measured results in the scale-down model"),
            Q("On the grid of `{python} f\"{N_GRID:,}\"` points"),
            Q("No attribute bounds the region within the ranges studied."),
            Q("The NOR lies inside the ranges studied for every parameter, and inside the design space."),
            Q("That result rests on the widening of the host cell protein criterion"),
            Q("Four results bound this claim near the corner of highest load and lowest conductivity.")]
    DSG = ns["DSG"]
    design_spaces = [S.DesignSpace(
        design_space_id="ds:cex", unit_operation=UO_NAME, parameters=[PC[n] for n in names_fac],
        quality_attributes_constrained=["attr:aggregates_hmw", "attr:hcp", "attr:fragments_lmw"],
        definition=t("The region of the four multivariate parameters, within their ranges studied, over which every "
                     "output with a criterion meets it at both ends of the `{python} PI_PCT` % prediction interval of a "
                     "single run (PCMP-001 §6.2, PCP-007 §7.5): aggregate and host cell protein through their selected "
                     "models at manufacturing scale, fragments through their measured results in the scale-down model, "
                     "all of which met the criterion. On a grid of `{python} f\"{N_GRID:,}\"` points "
                     "`{python} f\"{100 * DSG['fraction']:.0f}\"` % of the region meets every criterion in force, and "
                     "the region drawn on the mean prediction is also the whole region. At the a priori host cell "
                     "protein criterion `{python} f\"{100 * DS_AP:.2f}\"` % of the grid would meet every criterion. "
                     "Host cell protein comes nearest to its criterion, with a highest single-run limit of "
                     "`{python} num(CUBE_UP['hcp_out_ng_mg'][0])` ng/mg at the corner of highest load and lowest "
                     "conductivity, outside the NOR. The NOR lies inside the design space. The claim is bounded near "
                     "that corner by one screening result above the criterion, by the other host cell protein models "
                     "within two AICc units, and by the run-order drift of host cell protein; it is not confirmed at "
                     "manufacturing scale near the edges of the ranges studied and holds only at the set-point of "
                     "elution flow rate and within the qualified life of the resin."),
        source_references=[ref("ds", x) for x in q_ds], metadata=meta())]
    if DSG["fraction"] != 1.0:
        raise ValueError(f"{DOC}: the design space no longer covers the whole region, as the text says")

    q_par_fig = {("aggregate_out_pct", "load"): fig_cap("fig-par-agg", 1),
                 ("hcp_out_ng_mg", "load"): fig_cap("fig-par-hcp-load", 1),
                 ("hcp_out_ng_mg", "wash_cond"): fig_cap("fig-par-hcp-cond", 1)}
    PART_M = ns["PART_M"]
    lab_eng = {"aggregate_out_pct": "Aggregates (HMW, %)", "hcp_out_ng_mg": "Pool HCP (ng/mg)"}
    pars = []
    for (resp, pname), row in parrow.items():
        c = _cells(row)                 # Attribute | Criterion | Parameter | Unit | PAR at set-point | PAR, NOR-propagated
        eng = PART_M[(PART_M["CQA"] == lab_eng[resp]) & (PART_M["Parameter"] == pname)].iloc[0]
        if (c[4], c[5]) != (eng["PAR (set-point)"], eng["PAR (NOR)"]):
            raise ValueError(f"{DOC}: the PAR table no longer prints the engine's ranges for {resp}, {pname}")
        k = pkey[pname]
        u = pdf_.loc[pname, "Unit"]
        ia = IAC.loc[resp]
        basis = (f"Intermediate acceptance criterion {T.crit(ia['iac_low'], ia['iac_high'], ia['spec_type'])} "
                 f"({ia['basis']}) of PCMP-001 Version 2.0, at manufacturing scale; set-point analysis on the median "
                 f"prediction of the selected log-scale model, and NOR-propagated analysis on the "
                 f"{ns['PI_UP']:g}th percentile of simulated single batches with the other factors drawn within their "
                 f"NORs.")
        refs = [ref("par", row, par_t, parrow), tref("factors", pt_t, prow, pname)]
        if (resp, k) in q_par_fig:
            refs.append(ref("par", q_par_fig[(resp, k)], label={"aggregate_out_pct": "fig-par-agg"}.get(
                resp, "fig-par-hcp-load" if k == "load" else "fig-par-hcp-cond")))
        pars.append(S.ProvenAcceptableRange(
            par_id=f"{DOC}-PAR{len(pars) + 1:02d}", unit_operation=UO_NAME, quality_attribute=LAB[resp],
            parameter=pname, characterization_range=f"{pdf_.loc[pname, 'Range studied']} {u}",
            par_at_setpoint=f"{c[4]} {u}", par_nor_propagated=f"{c[5]} {u}", acceptance_basis=basis,
            source_references=refs, metadata=meta()))

    # ==== assertions ======================================================================================
    AS = []

    def add(subj, pred, obj, txt, refs):
        AS.append(EvidenceBackedAssertion(
            assertion_id=f"{DOC}-A{len(AS) + 1:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=txt, source_references=refs, metadata=meta()))

    add(STEP_ID, "step_uses_equipment", SDM_ID,
        f"The studies of {UO_NAME} were run on a {SDM_NAME}, a laboratory column of the commercial resin type packed to "
        f"the commercial bed height and run at the commercial linear velocities.", [ref("sdm", q_sdm1)])
    add(STEP_ID, "step_uses_equipment", CHAMBER_ID,
        f"The response-surface study S-CEX-RSM was run in the {CHAMBER_NAME}, the only instrumented system the record "
        f"names, in calibration for the whole study.", [tref("operation", win_t, winrow, "S-CEX-RSM")])
    for name, row in prow.items():
        add(STEP_ID, "step_has_parameter", PC[name],
            f"{UO_NAME} has process parameter {name}, classified {pdf_.loc[name, 'Class']}, studied "
            f"{pdf_.loc[name, 'Study type'].lower()}ly.", [ref("factors", row, pt_t, prow)])
    role = {"aggregates_hmw": "is the principal aggregate polishing step for {n}, which no later step removes",
            "hcp": "clears {n}, which anion exchange clears again",
            "fragments_lmw": "clears part of {n}, judged against the drug substance criterion",
            "residual_dna": "clears {n}, which carries no criterion at this step",
            "leached_protein_a": "clears {n}, which carries no criterion at this step"}
    for key in ckeys:
        add(STEP_ID, "step_has_quality_attribute", f"attr:{key}",
            f"{UO_NAME} " + role[key].format(n=names[key]) + ".", [ref("cqa", crow[key], cq_t, crow)])
    for amv, row in mdrow.items():
        key = key_of[amv]
        m_ = md_df.loc[amv]
        add(f"attr:{key}", "attribute_measured_by_method", f"method:{amv}",
            f"{names.get(key, 'Step yield')} is measured at the step by {m_['Technique']} ({amv}), reported as "
            f"{m_['Reportable']}.", [ref("app_d", row, md_t, mdrow)])
    add("attr:aggregates_hmw", "attribute_measured_by_method", "method:AMV-3221",
        t("Aggregate in the pool of response-surface run `{python} RUN14` was verified by "
          "`{python} dev_007_02_ver_n` SEC determinations under AMV-3221; the record gives no result."),
        [ref("dev2", q_meth["AMV-3221"])])
    for key in CRIT_KEYS:
        ic, cr = _cells(irow[key]), _cells(crrow[key])
        ia = IAC.loc[attr_resp[key]]
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{UO}_{key}_iac",
            f"At the cation exchange step {names[key]} is judged against the Version 2.0 intermediate acceptance "
            f"criterion {_unmark(ic[-2])} ({ia['basis']}), derived from the drug substance criterion "
            f"{_unmark(ic[1])}; met across the NOR: {_unmark(cr[-1])}.",
            [ref("basis", irow[key], iac_t, irow), ref("criteria", crrow[key], cr_t, crrow)])

    # parameter effects on aggregate and host cell protein: every coefficient row of the selected model that
    # contains the parameter; a parameter affects the attribute when one of its terms is significant
    for resp, key in (("aggregate_out_pct", "aggregates_hmw"), ("hcp_out_ng_mg", "hcp")):
        crows = {k_[1]: r_ for k_, r_ in corow.items() if k_[0] == resp and k_[1] != "Intercept"}
        for k in FAC:
            lt = LET[k]
            mine = {tm: r_ for tm, r_ in crows.items() if lt in tm.rstrip("²")}
            if not mine:
                c = _cells(serow[(se_lab[resp], lt)])
                add(PC[NAME[k]], "parameter_does_not_significantly_impact_attribute", f"attr:{key}",
                    f"{NAME[k]} ({lt}) has no term in the selected model of {LAB[resp]}; its screening effect was "
                    f"{c[2]}, p {c[5]}, not significant.",
                    [tref("screening", se_t, serow, (se_lab[resp], lt))]
                    + ([ref("criteria", Q("Elution stop collect is not in the host cell protein model"))]
                       if (resp, k) == ("hcp_out_ng_mg", "stop_collect") else []))
                continue
            sig = {tm: sig_of(_cells(r_)[-1]) for tm, r_ in mine.items()}
            txt = "; ".join(f"{tm} ({tname(tm)}) coefficient {_cells(r_)[-4]}, p {_cells(r_)[-1]}"
                            for tm, r_ in mine.items())
            if any(sig.values()):
                add(PC[NAME[k]], "parameter_impacts_attribute", f"attr:{key}",
                    f"{NAME[k]} ({lt}) affects {LAB[resp]} in the selected log-scale model: {txt}.",
                    [tref("rsm_agg", co_t, corow, (resp, tm)) for tm in mine])
            else:
                add(PC[NAME[k]], "parameter_does_not_significantly_impact_attribute", f"attr:{key}",
                    f"{NAME[k]} ({lt}) has no significant term in the selected model of {LAB[resp]}: {txt}; no effect is "
                    f"demonstrated.",
                    [tref("rsm_agg", co_t, corow, (resp, tm)) for tm in mine]
                    + [tref("screening", se_t, serow, (se_lab[resp], lt))])
    # step yield: the coefficient rows of its selected model, and the stop collect tested directly
    for k in FAC:
        lt = LET[k]
        mine = {tm: r_ for tm, r_ in ycrow.items() if tm != "Intercept" and lt in tm.rstrip("²")}
        if mine and any(sig_of(_cells(r_)[-1]) for r_ in mine.values()):
            add(PC[NAME[k]], "parameter_impacts_attribute", "attr:step_yield",
                f"{NAME[k]} ({lt}) affects step yield in its selected model: "
                + "; ".join(f"{tm} coefficient {_cells(r_)[1]} percentage points per coded unit, p {_cells(r_)[-1]}"
                            for tm, r_ in mine.items()) + ".",
                [tref("app_c", yc_t, ycrow, tm) for tm in mine])
        else:
            c = _cells(serow[("Step yield (points)", lt)])
            refs = [tref("app_c", yc_t, ycrow, tm) for tm in mine] + [tref("screening", se_t, serow,
                                                                          ("Step yield (points)", lt))]
            txt = (f"{NAME[k]} ({lt}) has no significant effect on step yield: screening effect {c[2]} percentage "
                   f"points, p {c[5]}")
            if mine:
                txt += "; in the selected model " + "; ".join(f"{tm} p {_cells(r_)[-1]}" for tm, r_ in mine.items())
            if k == "stop_collect":
                refs.append(ref("rsm_yield", Q("The stop collect was also tested directly.")))
                txt += t("; tested directly, its term has `{python} pq(P_Y_STOP_FULL)` in the plan's full quadratic")
            add(PC[NAME[k]], "parameter_does_not_significantly_impact_attribute", "attr:step_yield", txt + ".", refs)
    # elution flow rate (univariate): the rows of the comparison of the two ends
    fl_lab = {"aggregates_hmw": LAB["aggregate_out_pct"], "hcp": LAB["hcp_out_ng_mg"],
              "step_yield": "Step yield (points)", "residual_dna": "Residual DNA clearance (log10)"}
    for key, lab_ in fl_lab.items():
        c = _cells(fcrow[lab_])           # Response | Comparison | High against low | 95 % CI | df | p | p, duplicates
        if key == "residual_dna":
            add(PC[NAME["flow"]], "parameter_impacts_attribute", "attr:residual_dna",
                f"Residual DNA clearance was lower at the high end of the flow-rate range ({c[1]} {c[2]} log10, 95 % CI "
                f"{c[3]}, p {c[5]}), so residual DNA is affected by flow rate under PCMP-001 §6.2; the report judges the "
                f"effect too small to move residual DNA appreciably in the drug substance (PCMP-001 §7.7), and with the "
                f"scatter of the duplicates alone the comparison would not reach significance (p {c[6]}).",
                [tref("flow", fc_t, fcrow, lab_), ref("class", cls_quotes["flow"][2])])
        else:
            extra = ("; the interval includes an effect as large as that of protein load, so the study cannot exclude "
                     "one" if key == "step_yield" else "")
            add(PC[NAME["flow"]], "parameter_does_not_significantly_impact_attribute",
                f"attr:{key}" if key != "step_yield" else "attr:step_yield",
                f"No effect of elution flow rate on {lab_} was detected: high end against low end, {c[1]} {c[2]}, 95 % CI "
                f"{c[3]}, p {c[5]}{extra}.", [tref("flow", fc_t, fcrow, lab_)])
    # residual DNA clearance and the four factors of the response-surface design
    for i, k in enumerate(FAC):
        add(PC[NAME[k]], "parameter_does_not_significantly_impact_attribute", "attr:residual_dna",
            f"The clearance of residual DNA does not depend on {pn[k]} within the range studied: the selected model of "
            f"its clearance factor has no term.", [ref("dna_lpa", q_dna_f1 if i < 2 else q_dna_f2)])

    # ==== report statements, grouped by the chapters of the report =========================================
    STS = []

    def clean(s):
        """A rendered span as statement text: the spaces of a cross-reference closed up."""
        s = re.sub(r"\(\s+", "(", s)
        return re.sub(r"\s+([,.;:)])", r"\1", s)

    def st(sec, txt, refs):
        STS.append((SEC[sec][0], ReportStatement(
            statement_id=f"{DOC}-S{len(STS) + 1:03d}", statement_text=txt, confidence="high",
            review_status="accepted", source_references=refs)))

    def sq(sec, prefix, upto=None, txt=None, extra=()):
        """A statement of one prose span (by its prefix in the .qmd), ``txt`` the statement where it is not the
        span itself, ``extra`` further ``(section, prefix)`` spans it draws on."""
        span = Q(prefix, upto)
        st(sec, t(txt) if txt else clean(span), [ref(sec, span)] + [ref(s_, Q(x)) for s_, x in extra])

    def srow(sec, txt, row, tab=None, rows_=None, caption=None, label=None):
        st(sec, txt, [ref(sec, row, tab, rows_, caption=caption, label=label)])

    # -- Executive summary -----------------------------------------------------------------------------
    sq("exec", "It sets no quality attribute of its own.")
    sq("exec", "During the re-analysis, two studies of the low-pH viral inactivation report ran this step")
    sq("exec", "Protein load, load/wash conductivity, elution buffer pH and elution stop collect were studied")
    sq("exec", "Elution flow rate was assessed one factor at a time.")
    sq("exec", "The scale-down model is qualified for aggregate and host cell protein by its offsets")
    sq("exec", "The a priori criterion is the value derived before the studies")
    sq("exec", "The criterion in force is that value after this campaign")
    sq("exec", "For host cell protein the qualification holds at the criterion in force of")
    sq("exec", "Aggregate and host cell protein met their intermediate acceptance criteria at every combination")
    sq("exec", "Its highest value over the NOR was")
    sq("exec", "The aggregate criterion is the drug substance criterion of")
    sq("exec", "Fragments have no adequate model and were judged on their measured results, which lay between")
    sq("exec", "On the single-run limit and at the criteria in force, the design space covers")
    sq("exec", "At the a priori host cell protein criterion it would cover")
    sq("exec", "The proven acceptable range of every parameter for aggregate and host cell protein is its range studied.")
    sq("exec", "The models of aggregate and host cell protein were selected on the log scale")
    sq("exec", "The host cell protein model does not meet the fourth, because its residuals drift")
    sq("exec", "The highest single-run limit over the NOR stays below the criterion with the whole drift added to it.")
    sq("exec", "Elution flow rate was classified as a general process parameter")
    sq("exec", "Within its NOR the step cleared aggregate less than the platform worst case on which")
    sq("exec", "The platform worst case for host cell protein was confirmed with the offset at its estimate.")
    sq("exec", "The platform worst case for fragments was confirmed by the rule of PCP-007 §7.6")
    sq("exec", "The fragment model behind that prediction does not meet PCMP-001 §7.2.")
    sq("exec", "The capability indices of the drug substance attributes that the step clears all exceed the target")
    sq("exec", "Version 1.0 recorded `{python} N_DEV` events of execution")
    sq("exec", "Both runs were retained in the analysis.")
    sq("exec", "Four concern the analysis and the scale-down model.")
    sq("exec", "Five concern records the plan required that are not in the study record.")
    sq("exec", "The other two are the fractionated runs of S-CEX-FRC")
    sq("exec", "The last corrects an error of Version 1.0 of this report")

    # -- Introduction: objectives (PCP-007 §2, read from the numbered list of the .qmd) and changes ------------
    src_all = _source()
    obj_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n## Objectives", 1)[1].split("\n## ", 1)[0], flags=re.M)
    if len(obj_list) != 6:
        raise ValueError(f"{DOC}: {len(obj_list)} numbered objectives under '## Objectives', the text says six")
    sq("objectives", "PCP-007 §2 sets six objectives.")
    for i, obj in enumerate(obj_list, 1):
        st("objectives", f"Objective {i} of PCP-007 §2: {clean(q(obj))}", [ref("objectives", q(obj))])
    sq("objectives", "Objectives 2 and 3 were amended at Version 2.0 of the plan")
    sq("uo", "Its drug substance is purified by Protein A chromatography")
    sq("uo", "Below its isoelectric point the antibody carries a net positive charge and binds the ligand.")
    sq("uo", "The pool is collected between a threshold on the ascending edge of the elution peak")
    sq("uo", "Host cell protein, residual DNA and leached Protein A that do not bind")
    sq("uo", "The pool of this step is therefore judged against the drug substance criterion less the largest rise")
    sq("uo", "Enveloped virus is claimed at low-pH inactivation, anion exchange and virus filtration",
       "and small viruses at anion exchange and virus filtration")
    sq("basis_reg", "The study belongs to Stage 1 of process validation", "the studies that support it are recorded")
    sq("basis_reg", "Prior knowledge and the risk assessment RA-001 identified the parameters")
    sq("basis_reg", "Where this report states a rule, it cites the section of the plan or the master plan that sets it.")
    sq("basis_reg", "The SOP and AMV numbers are placeholders.")
    sq("changes", "Version 1.0 of this report was approved on")
    sq("changes", "This revision changes the report in seven ways.")
    sq("changes", "Version 1.0 judged the pool against an aggregate limit of")
    sq("changes", "Each was the drug substance criterion carried back through the nominal clearance")
    sq("changes", "Version 2.0 judges the pool against the intermediate acceptance criteria of PCMP-001 §7.3")
    sq("changes", "Two criteria in force differ from their a priori values.")
    sq("changes", "The host cell protein criterion is wider than its a priori value of")
    sq("changes", "The aggregate criterion is tighter than the drug substance criterion of")
    sq("changes", "Fragments. Fragments are judged at this step for the first time")
    sq("changes", "The models. Every output of the response-surface design is analysed by model selection")
    sq("changes", "The scale-down model. The model is qualified for each output by its offset")
    sq("changes", "The judgement. Each quality attribute is judged on the")
    sq("changes", "The verification. The report verifies the platform worst cases")
    sq("changes", "The record. The execution window of each study is recorded")
    sq("changes", "Version 1.0 of this report stated that the load, the flow-through and the wash of each run were")
    sq("changes", "No result of those assays or of that release is in the record")
    sq("changes", "Version 1.0 of this report also named the load/wash buffer of screening run")
    sq("changes", "It was an acetate buffer (discrepancy PD-007-12).")
    sq("changes", "A NOR-propagated range is the range of one parameter over which its criterion is met")
    sq("changes", "Under the Version 1.0 limits and the Version 1.0 analysis, these ranges ended inside the NOR")
    sq("changes", "The upper end of the protein load NOR,")
    sq("changes", "Under Version 2.0 every output meets its criterion across the NOR")

    # -- Prior knowledge and quality risk basis ----------------------------------------------------------
    sq("platform", "The cation exchange step has been operated on the Novacyte humanized IgG1 platform",
       "A-Mab clinical and engineering manufacture")
    sq("platform", "The resin chemistry, the buffer system and the mode of operation are unchanged for A-Mab.")
    sq("platform", "Aggregate presents more positive charge to the ligand than monomer does")
    sq("platform", "At the load pH, host cell proteins with an isoelectric point below that pH")
    sq("platform", "A part of the host cell protein is held in association with the bound antibody")
    sq("platform", "DNA carries a strong negative charge and is repelled by the ligand")
    sq("platform", "Free leached Protein A does not bind under load conditions")
    sq("platform", "Fragments carry less positive charge than intact antibody")
    sq("platform", "PCP-007 §4.1 draws four expectations from this experience")
    sq("platform", "A higher protein load occupies more of the ligand.")
    sq("platform", "A higher load/wash conductivity is expected to strip more of the weakly bound host cell protein")
    sq("platform", "A higher elution buffer pH weakens binding and brings monomer and aggregate off closer together")
    sq("platform", "The stop collect point is an absorbance on the descending edge")
    sq("platform", "The plan adds that a higher conductivity is expected to remove more host cell protein at a high load")
    sq("platform", "Curvature was expected in the effects of elution stop collect and elution buffer pH")
    for key, row in crow.items():
        c = _cells(row)
        srow("cqa", f"{names[key]}: drug substance criterion {c[2]}, criticality {c[3]}, Tool #1 score {c[4]}.", row,
             cq_t, crow)
    sq("cqa", "Criticality was assigned with Tool #1 of the case study", "the uncertainty in that impact")
    sq("cqa", "Three of the five attributes are responses of the designs.")
    sq("cqa", "The plan does not treat them as responses of the designs")
    sq("cqa", "Step yield is a process performance attribute.")
    sq("risk", "Each parameter was ranked for its potential impact on a quality attribute",
       "a parameter with no data or rationale was ranked at the highest level")
    sq("risk", "Protein load, load/wash conductivity, elution buffer pH and elution stop collect were assigned to the")
    sq("risk", "Elution flow rate was assigned to a univariate assessment.")
    sq("risk", "Parameters fixed by equipment design or held to platform specification")
    sq("risk", "The range studied of each parameter is wider than its NOR at both ends")
    sq("risk", "The ranges were set from the control capability of the commercial equipment",
       "beyond the region in which it runs")
    sq("risk", "The elution buffer pH range stops short of incomplete elution at its low end")

    # -- Materials and methods --------------------------------------------------------------------------
    sq("sdm", "The outputs compared were step yield, pool aggregate, pool host cell protein")
    sq("sdm", "The offset of an output is the mean of the scale-down runs minus the mean of the manufacturing")
    sq("sdm", "For an output modelled on the log scale the offset is taken on that scale.")
    sq("sdm", "The model is qualified for an output with a criterion when the conclusion over the NOR is the same")
    for k_, row in offrow.items():
        c = _cells(row)
        srow("sdm", f"Scale-down offset of {k_} (scale-down minus manufacturing scale): scale-down {_unmark(c[-6])}, "
                    f"manufacturing {_unmark(c[-5])}, estimate {_unmark(c[-4])}, {ns['CI_PCT']} % CI {c[-3]}; met over the NOR "
                    f"(low/estimate/high) {_unmark(c[-2])}; qualified {_unmark(c[-1])}.", row, off_t, offrow)
    sq("sdm", "The aggregate ratio is")
    sq("sdm", "The host cell protein ratio is")
    sq("sdm", "That interval is wide, because it rests on")
    sq("sdm", "The qualification for host cell protein depends on the criterion it is judged against.")
    sq("sdm", "With the offset at the unfavourable end of its interval, the highest single-run limit over the NOR is")
    sq("sdm", "That meets the criterion in force of")
    sq("sdm", "Under the a priori criterion the model would therefore not be qualified for host cell protein")
    sq("sdm", "Among the outputs without a criterion, only residual DNA differed between the scales")
    sq("sdm", "The scale-down pools carried")
    sq("sdm", "Version 1.0 of the plan required the cause of such a difference to be established")
    sq("sdm", "That rests on the assumption, stated in PCP-007 §12, that fragments separate in the same way")
    sq("sdm", "The scale-down column keeps the bed height, the linear velocity and the collection thresholds")
    sq("sdm", "The centre-point runs of both designs were made at the set-point of every factor.")
    sq("sdm", "The scale-down column reproduces the chromatography of the commercial column")
    sq("sdm", "The conclusions of this report apply to the commercial step through the qualification above")
    sq("operation", "Each run followed the operation of SOP-2010.")
    sq("operation", "The wash used the same conductivity, because the platform holds load and wash conductivity equal")
    sq("operation", "Buffer composition, packing and resin storage were not varied.")
    sq("operation", "No packing result is recorded for the screening, response-surface and flow-rate campaigns "
                    "(discrepancy")
    sq("operation", "The record does not name the feed lot of any run (discrepancy PD-007-11).")
    sq("operation", "Every characterization study of the step closed by")
    for sid_, row in winrow.items():
        c = _cells(row)
        act = _unmark(c[1])
        srow("operation", f"Study {sid_}, {act[0].lower() + act[1:]}: executed from {c[2]} to {c[3]}; instrumented "
                          f"system {c[4]}.", row, win_t, winrow)
    sq("operation", "The screening design ran before the method decision")
    sq("operation", "Two studies of the low-pH viral inactivation report made cation exchange runs")
    sq("analytics", "Every response was measured by a validated method")
    sq("analytics", "From `{python} AMD['date']` every study that measures fragments")
    sq("analytics", "The screening design ran before the decision and has SEC fragment results only.")
    sq("analytics", "The response-surface design measured fragments by both methods on every run.")
    sq("analytics", "The decision followed the comparability study S-CEX-FRC")
    st("analytics", "Fragments by SEC and by nrCE-SDS on the same samples of study S-CEX-FRC: SEC minus nrCE-SDS for "
                    "each sample and replicate (the Protein A pool, the viral inactivation pool, the cation exchange "
                    "load, the fractions F2 to F5, the cation exchange pool and the anion exchange pool).",
       [ref("analytics", r_, sc_t, scrow) for r_ in scrow.values()])
    sq("analytics", "The samples included the fractions F2 to F5 of a run of this step")
    sq("analytics", "SEC read fragments high wherever the sample still carried host cell protein")
    sq("analytics", "In the Protein A pool, the viral inactivation pool and the cation exchange load it was")
    sq("analytics", "From the cation exchange pool onward the two methods agreed to within")
    sq("analytics", "SEC remains the method for aggregate, where no such interference applies.")
    sq("analytics", "Assay variability is part of the residual variance of each model")
    sq("analytics", "The ELISA for host cell protein has a precision of")
    sq("sampling", "PCP-007 §5.4 sampled each run at four points.")
    sq("sampling", "The record of the designs holds the pool results of every run.")
    sq("sampling", "Three parts of the sampling plan are not in the record.")
    sq("sampling", "No load result for aggregate or host cell protein is recorded for any run")
    sq("sampling", "The clearance factors for aggregate and host cell protein in this report are therefore calculated")
    sq("sampling", "Residual DNA and leached Protein A were not measured on the screening runs (discrepancy PD-007-06).")
    sq("sampling", "No result for the flow-through, wash or strip fractions is recorded")
    sq("sampling", "Replication is concentrated at the centre point.")
    sq("sampling", "The centre points ran at positions")
    sq("stats", "All factors were analysed in coded units.")
    sq("stats", "At this step the set-point of every factor is the centre of its range")
    sq("stats", "The screening design was analysed by ordinary least squares")
    sq("stats", "It is not the predictive model of the step, because a model without quadratic terms")
    sq("stats", "The response-surface model is the predictive model.")
    sq("stats", "Every judgement over the NOR, every proven acceptable range, the design space and the verification")
    sq("stats", "The plan prescribed the full quadratic model of each output")
    sq("stats", "Each output was instead analysed by the model selection of INV-002 corrective action CA3")
    sq("stats", "The scale was chosen from the Box-Cox profile of the full quadratic", "of the full quadratic")
    sq("stats", "The log scale is used where the")
    sq("stats", "On that scale, every hierarchical submodel of the full quadratic was fitted")
    sq("stats", "The selected model was judged against the four adequacy criteria of PCMP-001 §7.2.")
    sq("stats", "An output whose selected model fails one of the first three criteria has no adequate model.")
    sq("stats", "It estimates how well a model would predict new runs.")
    sq("stats", "The search is exhaustive because a stepwise search changes one term at a time")
    sq("stats", "On the data of this step a stepwise search, backward or forward")
    sq("stats", "For host cell protein a backward search would have stopped at a model of")
    sq("stats", "The Box-Cox profile chose the log scale for aggregate")
    sq("stats", "It kept the raw scale for fragments, whose interval contains 1.")
    sq("stats", "This is the behaviour expected of a purification step")
    sq("stats", "For these two outputs the evidence for the log scale is the Box-Cox profile.")
    sq("stats", "The residuals themselves do not show the scatter growing with the level on the raw scale.")
    sq("stats", "For the full quadratic on the raw scale, the residual SD in the upper half")
    sq("stats", "neither difference is large enough to decide the scale", txt="At the number of runs of the design neither "
       "difference in the residual SD between the halves of the predictions is large enough to decide the scale.",
       extra=[])
    sq("stats", "On the log scale the criteria stay in their own units")
    sq("stats", "A prediction interval is calculated on the log scale and transformed back")
    sq("stats", "At the least favourable NOR combination for host cell protein the median is")
    sq("stats", "The predicted value is the median of the output, its geometric mean")
    sq("stats", "The model F-test is significant at α =")
    sq("stats", "Lack of fit against the pure error of the centre points is not significant at α =")
    sq("stats", "Predicted R² falls short of R² by no more than")
    sq("stats", "The absolute residuals regressed on the predicted values, and the residuals regressed")
    sq("stats", "A model with no term has no F-test, so the first criterion does not apply to it.")
    sq("stats", "An output with a selected model that fails the fourth criterion is still used")
    sq("stats", "For each such model this report states the size of the trend")
    sq("stats", "Where other models lie within `{python} f\"{DAICC:g}\"` AICc units of the selected one, they are reported")
    sq("stats", "A quality attribute is judged on a single batch.")
    sq("stats", "The judgement over the NOR asks whether the exact")
    sq("stats", "The interval is two-sided, so its upper end is a one-sided")
    sq("stats", "The design space is the set of settings within the ranges studied")
    sq("stats", "Two proven acceptable ranges are computed for each parameter and each output with a criterion")
    sq("stats", "The set-point analysis scans the parameter across its range with the other factors at their set-points")
    sq("stats", "The NOR-propagated analysis scans the parameter at")
    sq("stats", "Each draw takes its own fitted coefficients from their sampling distribution and its own residual.")
    sq("stats", "A setting is accepted where the")
    sq("stats", "The range reported is the contiguous accepted interval that contains the set-point.")
    sq("stats", "The NOR-propagated range is the one that supports a claim.")
    sq("stats", "The verification of the platform worst cases follows PCP-007 §7.6.")
    sq("stats", "The clearance factor is the level that the nominal batch of the process model brings")
    sq("stats", "For aggregate and host cell protein the prediction is first converted to manufacturing scale")
    sq("stats", "Fragments have no measured offset and enter as the scale-down model gives them.")
    sq("stats", "The model gives the lowest clearance factor over the")
    sq("stats", "Capability is estimated for the drug substance from the integrated model of the train, which simulates")
    sq("thresholds", "PCP-007 §7 lists six decisions of Version 1.0 for which no numerical threshold was set")
    sq("thresholds", "Three of the decisions could not be made as planned, because the records they need are missing.")
    sq("thresholds", "In the response-surface design the clearance factor of residual DNA was analysed")
    sq("thresholds", "Leached Protein A could not be analysed in that way")
    sq("thresholds", "The record holds plate count and peak asymmetry for the qualification runs only")
    sq("thresholds", "The distance of a prediction from its criterion is expressed in standard deviations")
    sq("thresholds", "The record holds no flow-through, wash or strip result, so no mass balance was made")
    sq("thresholds", "For each response of the flow-rate study, the difference between the mean results")
    sq("thresholds", "The CI uses the residual SD of the same response in the response-surface design")
    sq("thresholds", "The record names no feed lot for any run of the designs")
    sq("thresholds", "The range is supported for an attribute when every individual result at both ends")
    sq("thresholds", "It is not supported for an attribute the study did not measure.")

    # -- Study design ---------------------------------------------------------------------------------------
    for name, row in prow.items():
        c = _cells(row)
        srow("factors", f"{name}: set-point {c[2]} {c[1]}, NOR {c[3]} {c[1]}, range studied {c[4]} {c[1]}, class "
                        f"{c[5]}, {c[6].lower()} study.", row, pt_t, prow)
    sq("factors", "The range studied is the knowledge space of the step.")
    sq("factors", "The NOR is the range in which routine manufacture is controlled")
    sq("scr_design", "It is a two-level full factorial in the four factors")
    sq("scr_design", "It estimates every main effect and every two-factor interaction independently.")
    sq("scr_design", "The runs were executed in a randomized order")
    sq("rsm_design", "It is a face-centred central composite design in the same four factors")
    sq("rsm_design", "The design adds the quadratic terms that the screening design cannot estimate.")
    sq("rsm_design", "All four screening factors were carried into it.")
    sq("rsm_design", "The design therefore did not need the augmentation that PCP-007 §6.3 requires")
    sq("uni_design", "The plan also required a run at the set-point, which was not made")
    sq("uni_design", "Pool aggregate, pool host cell protein, step yield, and residual DNA and leached Protein A")
    sq("uni_design", "That limit was accepted because flow rate sets the residence time in the resin")

    # -- Results ----------------------------------------------------------------------------------------------
    sq("centre", "These runs measure the reproducibility of the scale-down model under study conditions")
    for (dsg, rlab), row in cenrow.items():
        c = _cells(row)
        srow("centre", f"{dsg} design, centre points of {rlab}: n {c[2]}, mean {c[3]}, SD {c[4]}, CV {c[5]} %.", row,
             cen_t, cenrow)
    sq("centre", "Host cell protein was the least reproducible response in both designs")
    sq("centre", "This agrees with the expectation of PCP-007 §5.3.")
    sq("centre", "Aggregate varied by")
    sq("centre", "The pure error has")
    sq("screening", "Each model is significant, and none shows significant lack of fit.")
    sq("screening", "With `{python} FS['aggregate_out_pct']['df_pe']` degrees of freedom for pure error that test is weak")
    for resp, row in sfrow.items():
        c = _cells(row)
        srow("screening", f"Screening model of {LAB[resp]}: R² {c[1]}, adjusted R² {c[2]}, predicted R² {c[3]}, model p "
                          f"{c[4]}, lack of fit p {c[5]}, residual SD {c[6]}.", row, sf_t, sfrow)
    sq("screening", "Aggregate was impacted by protein load, elution buffer pH and elution stop collect.")
    sq("screening", "Across the range studied, load raised pool aggregate by")
    sq("screening", "Significant interactions were found between load and pH")
    sq("screening", "Load/wash conductivity had no significant effect on aggregate")
    sq("screening", "Host cell protein was impacted by load/wash conductivity and protein load.")
    sq("screening", "Across the range, conductivity lowered pool host cell protein by")
    sq("screening", "On the raw scale, two effects that are additive on the log scale appear as an interaction")
    sq("screening", "Step yield fell with protein load by")
    sq("screening", "Over those corners the host cell protein results of the two designs did not differ systematically")
    sq("screening", "The largest difference was at the corner of")
    sq("screening", "There, screening run")
    sq("screening", "The screening result is the one result of either design above its criterion of")
    sq("screening", "It lies above the upper `{python} PI_PCT` % single-run limit that the response-surface model gives")
    sq("screening", "The corner lies outside the NOR of all four parameters.")
    sq("screening", "On the log scale the two runs differ by")
    sq("screening", "The response-surface model stays the predictive model")
    sq("rsm", "The models of aggregate and host cell protein meet the first three criteria.")
    sq("rsm", "The aggregate model also meets the fourth, and the host cell protein model does not.")
    sq("rsm", "The selected fragment model fails the limit on overfitting, so fragments have no adequate model.")
    for resp, row in msrow.items():
        c = _cells(row)
        srow("rsm", f"Selected model of {LAB[resp]}: {c[1]} scale, {c[2]} terms, R² {c[3]}, adjusted R² {c[4]}, "
                    f"predicted R² {c[5]}, gap {c[6]}, model p {c[7]}, lack of fit p {c[8]}, criterion 4 {c[9]}, "
                    f"adequate {c[10].lower()}.", row, ms_t, msrow)
    sq("rsm", "INV-002 assigned that model a refit")
    sq("rsm", "Under corrective action CA3 the fragment model was selected instead")
    sq("rsm", "This step was not augmented.")
    sq("rsm", "Only the run-order test of host cell protein falls below its level")
    for resp, row in rdrow.items():
        c = _cells(row)
        srow("rsm", f"Residuals and influential runs of the selected model of {LAB[resp]}: spread p {c[1]}, order p "
                    f"{c[2]}, largest Cook's distance {c[3]}, flag limit {c[4]}, median of F(p, n − p) {c[5]}, runs "
                    f"flagged {c[6]}, criterion 4 {c[7]}.", row, rd_t, rdrow)
    sq("rsm_agg", "It explains `{python} f\"{100 * FA['R2']:.1f}\"` % of the variation")
    sq("rsm_agg", "Runs `{python} join_and(RI['aggregate_out_pct']['over'])` have a Cook")
    sq("rsm_agg", "From the low to the high end of its range, protein load multiplies pool aggregate by")
    sq("rsm_agg", "There the interactions do not act")
    sq("rsm_agg", "The conductivity term, kept by the selection, has")
    sq("rsm_agg", "The interactions make load act more strongly at a high pH")
    sq("rsm_agg", "From the low to the high end of the load range, aggregate rises by a factor of")
    sq("rsm_agg", "The stop collect has a significant curvature")
    sq("rsm_agg", "No curvature in pH was found.")
    sq("rsm_agg", "The residuals scatter about zero with no trend that the spread test detects")
    st("rsm_agg", "Figure caption: the diagnostics of the selected aggregate model on the log scale.",
       [ref("rsm_agg", fig_cap("fig-diag-agg", 1), label="fig-diag-agg")])
    sq("rsm_hcp", "It explains `{python} f\"{100 * FH['R2']:.1f}\"` % of the variation")
    sq("rsm_hcp", "The model F-test is significant (`{python} pq(FH['p'])`)")
    sq("rsm_hcp", "Runs `{python} join_and(RIH['over'])` have a Cook")
    sq("rsm_hcp", "From the low to the high end of its range, with the other factors at their set-points, protein load")
    sq("rsm_hcp", "The two effects are of the same size within their standard errors.")
    sq("rsm_hcp", "With the other factors at their set-points the model gives `{python} num(HC_L[0])`")
    sq("rsm_hcp", "The selected model keeps a negative curvature in load")
    sq("rsm_hcp", "Its coefficient, ")
    sq("rsm_hcp", "Elution buffer pH has no significant main effect")
    sq("rsm_hcp", "From the low to the high end of the conductivity range, host cell protein falls by a factor of")
    sq("rsm_hcp", "The load × pH term is kept with")
    sq("rsm_hcp", "On the log scale the full quadratic gives the load × conductivity term")
    st("rsm_hcp", "Figure caption: the diagnostics of the selected host cell protein model on the log scale.",
       [ref("rsm_hcp", fig_cap("fig-diag-hcp", 1), label="fig-diag-hcp")])
    sq("rsm_hcp", "The slope is `{python} fm(RIH['order_slope'], 4)` per run on the log scale")
    sq("rsm_hcp", "Added in full to the highest single-run limit over the NOR, ")
    sq("rsm_hcp", "The conclusion over the NOR therefore does not depend on the trend.")
    sq("rsm_hcp", "Outside the NOR it can.")
    sq("rsm_hcp", "Added to the highest single-run limit over the whole region studied")
    sq("rsm_hcp", "Added to the highest limit over the NOR with the offset at the unfavourable end of its interval")
    sq("rsm_hcp", "The edge of the design space and the qualification for host cell protein are therefore sensitive")
    st("rsm_hcp", "Figure caption: the residuals of the selected host cell protein model against the order of execution.",
       [ref("rsm_hcp", fig_cap("fig-hcp-order", 1), label="fig-hcp-order")])
    sq("influence", "Each run with a Cook")
    sq("influence", "With any one of these runs deleted, aggregate and host cell protein still meet their criteria")
    sq("influence", "The terms of the selected models do change.")
    sq("influence", "Every deletion changes the aggregate model")
    sq("influence", "Deleting run `{python} RIH['over'][0]` or run")
    sq("influence", "The choice of scale for host cell protein therefore rests on these two runs")
    for (resp, run), row in dlrow.items():
        c = _cells(row)
        lead = "No run deleted" if c[1] == "none" else f"Run {c[1]} deleted"
        srow("influence", f"{LAB[resp]}, {lead}: {c[2]} scale, {c[3]} terms; highest single-run limit over the NOR "
                          f"{c[4]}; region inside {c[5]} %; lowest clearance factor in the NOR {c[6]}; bound of a single "
                          f"batch {c[7]}.", row, dl_t, dlrow)
    sq("near", "For aggregate, the one other model differs only by leaving out the conductivity main effect")
    sq("near", "For host cell protein, `{python} len(NEAR_ALT['hcp_out_ng_mg'])` other models differ")
    sq("near", "All of them meet the first three adequacy criteria and give the same judgement over the NOR.")
    sq("near", "Three results differ among the host cell protein models.")
    sq("near", "First, `{python} len(HCP_ALT_OUT)` of the")
    sq("near", "That part lies at the lowest conductivity and at loads of")
    sq("near", "Second, `{python} len(HCP_ALT_UNQ)` models give a highest single-run limit")
    sq("near", "Under them the scale-down model would not be qualified for host cell protein.")
    sq("near", "Third, `{python} len(HCP_ALT_NC)` models give a lowest clearance factor within the NOR of")
    sq("near", "Under any of them, rule 1 of PCMP-001 §7.5 would replace the platform value")
    sq("near", "They show that the qualification for host cell protein, the verification of its platform worst case")
    for (resp, terms), row in nrrow.items():
        c = _cells(row)
        srow("near", f"{LAB[resp]}, {'the selected model' if terms == 'selected model' else 'model ' + terms}: "
                     f"{c[1]} AICc units above the best, gap {c[3]}, highest single-run limit over the NOR {c[4]}, "
                     f"qualified {c[5].lower()}, region outside {c[6]} %, lowest clearance factor in the NOR {c[7]}.",
             row, nr_t, nrrow)
    sq("rsm_frag", "The only other model within `{python} f\"{DAICC:g}\"` AICc units fails the same limit.")
    sq("rsm_frag", "Every one of the `{python} len(FRAG_MEAS)` nrCE-SDS results")
    sq("rsm_frag", "The gap of the fragment model lies close to its limit.")
    sq("rsm_frag", "With run `{python} FRAG_DEL_ADQ[0]` or run")
    sq("rsm_yield", "Step yield has no criterion.")
    sq("rsm_yield", "With the other factors at their set-points the model gives `{python} num(100 * Y_SP)` %")
    sq("rsm_yield", "Its term has `{python} pq(P_Y_STOP_FULL)` in the plan")
    sq("rsm_yield", "The selection is sensitive to one run.")
    sq("rsm_yield", "Run `{python} RUN14` is the run with the temperature excursion.")
    sq("rsm_yield", "With it deleted, the selection keeps")
    sq("rsm_yield", "In that model the stop collect term is")
    sq("surfaces", "The surfaces are medians in the scale-down model for aggregate and host cell protein.")
    st("surfaces", "Figure caption: the predicted pool aggregate, host cell protein and step yield over protein load and "
                   "load/wash conductivity.", [ref("surfaces", fig_cap("fig-surf-load", 1), label="fig-surf-load")])
    st("surfaces", "Figure caption: the predicted pool aggregate, host cell protein and step yield over elution buffer pH "
                   "and elution stop collect.", [ref("surfaces", fig_cap("fig-surf-elution", 1),
                                                     label="fig-surf-elution")])
    sq("dna_lpa", "Residual DNA was quantified in the load and the pool of all")
    sq("dna_lpa", "The load carried")
    sq("dna_lpa", "The process model credits the step with")
    sq("dna_lpa", "Leached Protein A was quantified in the load of every run")
    sq("dna_lpa", "In `{python} N_RSM - N_LPA_LOQ` pools it was quantified at")
    sq("dna_lpa", "In the other `{python} N_LPA_LOQ` pools it lay below the LOQ of")
    sq("dna_lpa", "The offset of leached Protein A in @tbl-sdm-offsets is a ratio")
    sq("dna_lpa", "Every response-surface run cleared leached Protein A by more than the platform worst case of")
    sq("flow", "Aggregate and host cell protein are stated at manufacturing scale.")
    sq("flow", "Every result at both ends met its criterion, so the range studied of")
    fl_rate = ffill([_unmark(_cells(r_)[0]) for r_ in flrow.values()])
    for i, row in flrow.items():
        c = _cells(row)
        st("flow", f"Flow-rate study, flow rate {fl_rate[i]} cm/hr, run {c[1]}: aggregate (%) {c[2]}, host cell "
                   f"protein (ng/mg) {c[3]}, yield (%) {c[4]}, residual DNA in the load (pg/mg) {c[5]} and in the pool "
                   f"(pg/mg) {c[6]}, DNA clearance (log10) {c[7]}, leached Protein A (ppm) {c[8]}.",
           [ref("flow", row, fl_t, flrow)])
    sq("flow", "No difference was detected in aggregate, host cell protein or step yield.")
    sq("flow", "For aggregate and host cell protein the differences between the ends")
    sq("flow", "For step yield the interval of the difference")
    sq("flow", "The study is too small to exclude such an effect on yield.")
    sq("flow", "Residual DNA clearance was `{python} f\"{-FLOW['dna_lrv']['diff']:.2f}\"` log10 lower at the high end than")
    sq("flow", "It is the only response of the study for which the comparison reaches p <")
    sq("flow", "It rests on two runs at each end, and the lowest clearance")
    sq("flow", "Residual DNA was not measured in the screening design, so there is no screening effect")
    sq("flow", "With the scatter of the duplicates alone, the DNA comparison would not reach significance")
    sq("flow", "That estimate of the scatter rests on two pairs of runs.")
    sq("flow", "Both pools at the high end carried leached Protein A below the LOQ")
    sq("flow", "The study detected no effect of flow rate on aggregate or host cell protein comparable in size")
    sq("flow", "It detected none on yield, but it cannot exclude one as large as the effect of protein load.")
    sq("flow", "Flow rate was not carried into a multivariate study.")
    sq("flow", "Residual DNA clearance was significantly lower at the high end of the flow-rate range.")
    sq("mech", "Protein load and elution buffer pH acted on aggregate in the directions expected.")
    sq("mech", "A higher load occupies more of the ligand and broadens the elution peaks")
    sq("mech", "A higher pH lowers the positive charge of both species")
    sq("mech", "The positive load × pH interaction fits the same picture")
    sq("mech", "Within this range conductivity has no demonstrated effect on aggregate, as expected.")
    sq("mech", "The elution stop collect acted on aggregate in the opposite direction")
    sq("mech", "A higher setting stops collection earlier on the descending edge")
    sq("mech", "In both designs aggregate instead rose as the setting rose")
    sq("mech", "Protein load and load/wash conductivity acted on host cell protein in the directions expected.")
    sq("mech", "More load leaves more host cell protein held with the bound antibody")
    sq("mech", "On the log scale each acts as a constant factor")
    sq("mech", "A change with load of the share that conductivity removes was not found.")
    sq("mech", "Residual DNA clearance did not depend on any of the four factors of the response-surface design")
    sq("mech", "The lower clearance at the highest flow rate is not explained by that mechanism either.")
    sq("mech", "Leached Protein A was cleared by a modest factor")
    sq("mech", "Yield fell with load, as expected when broader peaks lose more monomer at their edges.")

    # -- Design space -----------------------------------------------------------------------------------------
    sq("ds", "Fragments have no adequate model and no measured offset.")
    sq("ds", "The region drawn on the mean prediction, for comparison, is also the whole region")
    sq("ds", "At the a priori criterion of `{python} C_HCP_AP` ng/mg,")
    sq("ds", "The `{python} N_AP_OUT` points outside lie at")
    sq("ds", "Host cell protein comes nearest to its criterion.")
    sq("ds", "Its highest single-run limit over the region is")
    sq("ds", "The highest single-run limit of aggregate is")
    sq("ds", "Screening run `{python} S9_RUN` at such a corner gave host cell protein above the criterion")
    sq("ds", "Of the other host cell protein models within")
    sq("ds", "At that corner each design has a single run")
    sq("ds", "With the run-order drift of host cell protein added, ")
    sq("ds", "Under ICH Q8(R2), working within an approved design space does not need a regulatory change",
       "does not need a regulatory change")
    sq("ds", "The NOR of this step was not changed, and the plan")

    # -- Proven acceptable ranges ---------------------------------------------------------------------------
    sq("basis", "Each output is judged against its intermediate acceptance criterion (PCMP-001 §7.3).")
    sq("basis", "The rule carries each drug substance criterion backward through the train")
    sq("basis", "The derivation of the a priori criteria uses no result of the studies they judge.")
    for key, row in irow.items():
        c = _cells(row)
        bas = _unmark(c[-1])
        srow("basis", f"Intermediate acceptance criterion of the step for {names[key]}: {_unmark(c[-2])}, basis "
                      f"{bas[0].lower() + bas[1:]}, from the drug substance criterion {_unmark(c[1])} through a downstream "
                      f"clearance factor of {c[2]} and an increase of {c[3]}.", row, iac_t, irow)
    sq("basis", "PCMP-001 assumed that none adds any either")
    sq("basis", "UF/DF raises aggregate within its NOR.")
    sq("basis", "Carried back from the drug substance criterion, that bound tightens the criterion of this pool to")
    sq("basis", "The tightening changes no conclusion of this report")
    sq("basis", "For host cell protein the drug substance criterion of")
    sq("basis", "With the platform worst case of anion exchange, a clearance factor of")
    sq("basis", "The criterion in force is therefore")
    sq("basis", "That widening is argued here by its risk, in the four parts of PCMP-001 §7.5.")
    sq("basis", "A wider criterion lets the pool of this step carry up to")
    sq("basis", "If anion exchange then cleared only its platform worst case, the drug substance could carry")
    sq("basis", "The risk falls on the producer where such a result is detected")
    sq("basis", "Host cell protein is a release test of the drug substance, by the ELISA AMV-3012")
    sq("basis", "Its reagent covers")
    sq("basis", "Anion exchange must clear `{python} f\"{HCP_DSF:.2f}\"`-fold")
    sq("basis", "The bound in force comes from the")
    sq("basis", "On all `{python} N_AEX_RSM + N_AEX_AUG` of its runs")
    sq("basis", "The bound holds within the NOR of anion exchange.")
    sq("basis", "No simulated batch of the integrated model exceeded the host cell protein criterion")
    sq("basis", "The widening changes no conclusion of this report over the NOR.")
    sq("basis", "The highest single-run limit of the pool over the NOR, `{python} num(UPL['hcp_out_ng_mg'])`")
    sq("basis", "The widening does decide two results outside that judgement.")
    sq("basis", "At the a priori criterion the scale-down model would not be qualified for host cell protein")
    sq("basis", "The proven acceptable ranges would not change.")
    sq("basis", "The platform history gives no worst-case DNA clearance for the steps after Protein A")
    sq("criteria", "Every output meets its criterion across the NOR.")
    for key, row in crrow.items():
        c = _cells(row)
        srow("criteria", f"{names[key]} against its criterion {c[1]}: mean predicted by the response-surface model, or "
                         f"measured results where it has none, at the set-point {_unmark(c[2])} and over the NOR "
                         f"{_unmark(c[3])}; 95 % limits of a single run over the NOR {_unmark(c[4])}; met across the "
                         f"NOR: {c[5]}.", row, cr_t, crrow)
    sq("criteria", "Aggregate has a median of")
    sq("criteria", "The least favourable combination is")
    sq("criteria", "Host cell protein has a median of")
    sq("criteria", "No predicted value over the NOR comes near its criterion.")
    sq("criteria", "At the least favourable combinations the median lies")
    sq("criteria", "Fragments are judged on their measured results, all below their criterion")
    sq("par", "The set-point analysis gives the range of one parameter with the rest of the step at target.")
    sq("par", "The NOR-propagated analysis gives the range over which the")
    sq("par", "Since each range is the range studied, each NOR edge lies inside its proven acceptable range")
    sq("par", "@fig-par-agg plots aggregate against protein load, which has the largest main effect on it.")
    sq("par", "For host cell protein the main effects of load and conductivity are of the same size")
    sq("par", "A proven acceptable range is a statement about one parameter while the others are held")
    sq("par", "The design space is a statement about the four together")
    sq("par", "At this step, at the criteria in force, both cover the whole range studied.")
    sq("par", "For elution flow rate, the range of")
    sq("verif", "The criteria upstream of this step assume that cation exchange clears each attribute")
    for key, row in verrow.items():
        c = _cells(row)
        if key == "leached_protein_a":
            txt = f"Platform worst case of cation exchange for {names[key]}: clearance factor {c[3]}; {_unmark(c[4])}."
        else:
            txt = (f"Platform worst case of cation exchange for {names[key]}: lowest clearance factor {c[3]}; this "
                   f"campaign, lowest at the edges of the range studied {c[4]}, lowest within the NOR {c[5]}, one-sided "
                   f"95 % bound of a single batch {c[6]}; outcome {_unmark(c[7]).lower()}.")
        srow("verif", txt, row, ver_t, verrow)
    sq("verif", "Aggregate. Within its NOR the step cleared aggregate less than the platform worst case of")
    sq("verif", "At manufacturing scale the lowest clearance factor predicted was "
                "`{python} num(VER.loc['aggregates_hmw', 'predicted_nor'])`, at")
    sq("verif", "By rule 1 of PCMP-001 §7.5 the one-sided")
    sq("verif", "The criterion of the low-pH pool moved from")
    sq("verif", "The criterion of the bioreactor harvest moved from")
    sq("verif", "The bound comes from the `{python} N_RSM` runs of the response-surface design")
    sq("verif", "With each flagged run deleted the lowest predicted factor stays below the platform value")
    sq("verif", "The plan's full quadratic would have given a bound of")
    sq("verif", "That tightening is argued by its risk, in the four parts of PCMP-001 §7.5.")
    sq("verif", "A stricter criterion lowers the aggregate that the low-pH pool and the harvest may carry.")
    sq("verif", "It lowers the patient")
    sq("verif", "No step after cation exchange removes aggregate, so the aggregate of this pool reaches the drug")
    sq("verif", "An excursion of a pool upstream beyond its tightened criterion would therefore be detected")
    sq("verif", "Cation exchange must clear `{python} num(VER.loc['aggregates_hmw', 'predicted_nor_bound95'])`-fold")
    sq("verif", "No later step is credited with any clearance of aggregate.")
    sq("verif", "No simulated batch exceeded the aggregate criterion of the drug substance")
    sq("verif", "Two studies of the low-pH viral inactivation report ran this step at its set-point")
    sq("verif", "They tested whether cation exchange clears aggregate and fragments by the factors")
    sq("verif", "In S-CEX-VER (discrepancy PD-006-02) and S-VI-WC (PD-006-03) every run cleared aggregate by")
    sq("verif", "For fragments, S-CEX-VER met its factor.")
    sq("verif", "In S-VI-WC every run cleared fragments by more than")
    sq("verif", "Host cell protein. At manufacturing scale the lowest clearance factor predicted within the NOR")
    sq("verif", "The bound of a single batch, `{python} num(VER.loc['hcp', 'predicted_nor_bound95'])`")
    sq("verif", "The same outcome follows with each flagged run deleted.")
    sq("verif", "It does not follow under every model within")
    sq("verif", "The verification converts the scale-down prediction to manufacturing scale with the offset")
    sq("verif", "Its outcome for host cell protein depends on that estimate.")
    sq("verif", "With the offset at the unfavourable end of its interval the lowest factor would be")
    sq("verif", "With the offset at the favourable end the lowest factor would be")
    sq("verif", "For aggregate the outcome is the same at either end of its interval")
    sq("verif", "Fragments. The lowest clearance factor that the fragment model predicts within the NOR")
    sq("verif", "By the rule of PCP-007 §7.6 the assumption is therefore confirmed")
    sq("verif", "The fragment model behind this confirmation does not meet the limit on overfitting")
    sq("verif", "The fragment criteria of the Protein A pool")
    sq("verif", "Every response-surface run cleared more than that factor")

    # -- Process capability and robustness -----------------------------------------------------------------------
    sq("cap", "Capability is estimated for the drug substance from the integrated model of the train (PCMP-001 §6.5).")
    for key, row in caprow.items():
        c = cap_df.loc[key]
        srow("cap", f"Drug substance capability of {names[key]}: criterion {c['Criterion']}, criticality "
                    f"{c['Criticality']}, mean ± SD {c['Mean ± SD']}, Cpk {c['Cpk']}, simulated batches outside "
                    f"{c['Batches outside']}.", row, cap_t, caprow)
    sq("cap", "No simulated batch fell outside any of the five criteria.")
    sq("cap", "With `{python} f\"{NMC:,}\"` batches that bounds the probability")
    sq("cap", "The bound covers the sampling of the simulation and not the uncertainty of the integrated model itself.")
    sq("cap", "Leached Protein A is judged instead by the criterion of the Protein A pool")
    sq("cap", "The dose is A-Mab")
    sq("cap", "That result depends on inputs from outside this step")
    sq("cap", "The pool of this step alone carried up to")
    sq("cap", "The derivation of the criteria credits no later step with removing aggregate")
    sq("cap", "It shares the clearance of host cell protein, residual DNA and leached Protein A with anion exchange.")
    sq("cap", "The robustness of the step within its NOR is shown by the margins of")

    # -- Parameter classification -------------------------------------------------------------------------------
    sq("class", "Parameters were classified under SOP-4001 by the decision logic of the A-Mab case study",
       "by the decision logic of the A-Mab case study")
    sq("class", "A key process parameter affects process performance and has no effect on a CQA within its range.")
    sq("class", "PCMP-001 §7.7 adds that", 'make a parameter critical"')
    sq("class", "An attribute is called affected by a parameter when a term that contains the parameter is significant")
    sq("class", "No numerical threshold is set for practical relevance")
    sq("class", "Each class below is therefore stated with the size of the effect across the proven acceptable range")
    sq("class", "No difference was detected in aggregate or host cell protein, and every result met its criterion")
    sq("class", "The difference is a factor of")
    sq("class", "If the whole factor reached the drug substance, its mean would be")
    sq("class", "The study therefore does not show that flow rate leaves yield unchanged.")
    sq("class", "Fragments were not measured in the flow-rate study, so for fragments the class rests on")
    sq("class", "Of the `{python} N_PAR` parameters, `{python} N_WC` are critical process parameters")
    sq("class", "Each WC-CPP has a proven acceptable range equal to its range studied")

    # -- Contribution to the control strategy -------------------------------------------------------------------
    sq("cs", "The step contributes four elements to the control strategy of the drug substance.")
    sq("cs", "Parameter ranges. The four WC-CPPs are controlled within their NORs")
    sq("cs", "Elution flow rate is controlled within its NOR as a GPP.")
    sq("cs", "The host cell protein criterion of the Protein A pool, ")
    sq("cs", "The criteria this step hands on. The pool must meet")
    sq("cs", "It must meet `{python} C_AGG` % of aggregate so that the rise across UF/DF keeps the drug substance")
    sq("cs", "It meets both across the NOR, with highest single-run limits of")
    sq("cs", "Release testing. The drug substance criteria of")
    sq("cs", "For aggregate and fragments the register names the method, SEC and nrCE-SDS.")
    sq("cs", "The conclusions of this report hold for resin within the cycle count qualified under SOP-2008.")
    sq("cs", "Low-pH viral inactivation inactivates enveloped virus (PCR-006).")
    sq("cs", "Anion exchange clears host cell protein, residual DNA, leached Protein A and virus after this step")

    # -- Discussion -----------------------------------------------------------------------------------------------
    sq("disc", "A higher protein load and a higher elution buffer pH raise aggregate in the pool.")
    sq("disc", "A higher protein load also raises host cell protein, because more of it is held with the bound")
    sq("disc", "A higher load/wash conductivity lowers host cell protein")
    sq("disc", "A higher stop collect setting raises aggregate, against the expected mechanism.")
    sq("disc", "Neither result is explained.")
    sq("disc", "Confidence in the scale-down model rests on the offsets of")
    sq("disc", "For aggregate the offset is close to 1 and well determined.")
    sq("disc", "For host cell protein the ratio is known only to within its interval of")
    sq("disc", "The model is qualified for host cell protein at the criterion in force.")
    sq("disc", "It would not be qualified at the a priori criterion, under")
    sq("disc", "Screening run `{python} RUN6` was made with the expired buffer lot.")
    sq("disc", "With it deleted, the screening models find the same significant terms.")
    sq("disc", "Response-surface run `{python} RUN14` had the temperature excursion.")
    sq("disc", "With it deleted, the judgement over the NOR, the design space and the outcome of the verification are")
    sq("disc", "Deleting run `{python} RUN14` does change two selected models.")
    sq("disc", "The discrepancies from the plan fall into three groups.")
    sq("disc", "The analysis departs from the plan in the model selection")
    sq("disc", "The selection changed the terms of the models but no conclusion over the NOR.")
    sq("disc", "The run-order drift of the host cell protein residuals, a factor of")
    sq("disc", "The execution departs from the plan in the flow-rate study without its set-point run")
    sq("disc", "The record lacks the load results, the residual DNA and leached Protein A results")
    sq("disc", "The missing load results matter most")
    sq("disc", "Apart from these groups, discrepancy PD-007-12 corrects the name of the load/wash buffer")
    sq("disc", "Five limitations remain.")
    sq("disc", "Scale. The scale-down model does not reproduce the hold times")
    sq("disc", "The process performance qualification (PPQ) batches of Stage 2")
    sq("disc", "The corner of highest load and lowest conductivity. One screening result there exceeded")
    sq("disc", "The corner lies outside the NOR of every parameter.")
    sq("disc", "The size of the flow-rate study.")
    sq("disc", "Fragments. Fragments have no adequate model and no offset.")
    sq("disc", "Their judgement rests on measured results in the scale-down model")
    sq("disc", "Resin life cycle. The conclusions hold within the qualified life of the resin")

    # -- Conclusions (the numbered list of the .qmd) ----------------------------------------------------------
    con_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n# Conclusions", 1)[1].split("\n# ", 1)[0], flags=re.M)
    if len(con_list) != 7:
        raise ValueError(f"{DOC}: {len(con_list)} numbered conclusions, the report has seven")
    for i, con in enumerate(con_list, 1):
        st("concl", f"Conclusion {i}: {clean(q(con))}", [ref("concl", q(con))])

    # -- Study events and discrepancies from the plan -------------------------------------------------------------
    sq("record", "The Version 1.0 plans called a departure from the plan a deviation.")
    sq("record", "This report records two kinds of entry instead.")
    sq("record", "Study events are the events of execution that Version 1.0 recorded")
    sq("record", "Discrepancies from the plan are departures from the approved plan PCP-007")
    sq("events", "The studies of this step recorded")
    sq("dev1", "The lot is an acetate load/wash buffer, and Version 1.0 of this report named it a Tris buffer in error")
    sq("dev1", "A lot that is within its expiry date when it is prepared can still be expired when it is used")
    sq("dev1", "Under `{python} SOP2103['id']`")
    sq("dev1", "That pH lies in the buffering range of acetate.")
    sq("dev1", "The impact was judged from the data.")
    sq("dev1", "Its studentized residuals on the screening models were")
    sq("dev2", "The record gives neither the temperature set-point nor a permitted range.")
    sq("dev2", "Temperature is not a factor of the designs.")
    sq("dev2", "At its precision of")
    sq("dev2", "The impact of the run was judged from its residuals instead.")
    sq("dev2", "Its studentized residuals on the selected models were")
    sq("dev2", "The lowest predicted clearance factor of aggregate stays below the platform value.")
    sq("dev2", "The step yield model replaces its")
    for pid, row in pdrow.items():
        d = PDS[pid]
        srow("pds", f"Discrepancy {pid} from PCP-007, {d['subject']}: planned {d['planned']}; done {d['done']}; reason "
                    f"{d['reason']}.", row, rows_=pdrow, caption=pd_cap, label="tbl-discrepancies")
    sq("pd01", "PCP-007 prescribed the full quadratic model of each response-surface output.")
    sq("pd01", "The selection changed the terms of every model and put aggregate and host cell protein on the log")
    sq("pd01", "It changed no conclusion over the NOR.")
    sq("pd01", "With the plan's full quadratic, aggregate and host cell protein also meet their criteria")
    sq("pd01", "Through the anion exchange model, the selection also widened the host cell protein criterion")
    sq("pd01", "That widening decides the qualification of the scale-down model for host cell protein")
    sq("pd01", "It also moved the bound that tightened the aggregate criteria upstream")
    sq("pd02", "PCP-007 required models that meet every adequacy criterion of PCMP-001 §7.2.")
    sq("pd02", "The host cell protein model meets the first three and fails the fourth")
    sq("pd02", "It was used for the ranges and the design space.")
    sq("pd02", "The trend amounts to a factor of")
    sq("pd02", "No run of any model has a Cook")
    sq("pd02", "The flagged runs were each deleted and the selection repeated, which the plan provides")
    sq("pd02", "Outside the NOR the drift would move the edge of the design space")
    sq("pd03", "PCP-007 §6.4 required the flow-rate study at the ends of the range and at the set-point.")
    sq("pd03", "Each end was run in duplicate, and no run was made at the set-point.")
    sq("pd03", "They were made in a different study, before the characterization runs")
    sq("pd03", "The comparison of the two ends does not depend on them.")
    sq("pd04", "Version 1.0 of PCP-007 accepted the scale-down model only where no compared attribute differed")
    sq("pd04", "Residual DNA differed at that level")
    sq("pd04", "Under PCMP-001 Version 2.0 §7.1 a scale-down model may differ in mean from manufacturing scale")
    sq("pd05", "PCP-007 §5.4 and §12 required aggregate and host cell protein to be measured in the load")
    sq("pd05", "No load result for either attribute is in the record.")
    sq("pd05", "The clearance factors of this report are taken against the process model at set-point")
    sq("pd05", "The pool results and the judgements against the criteria do not depend on the load.")
    sq("pd05", "The clearance factors and the verification of the platform worst cases do")
    sq("pd06", "PCP-007 §5.4 required residual DNA and leached Protein A on every run of both designs.")
    sq("pd06", "They were measured on the response-surface runs only.")
    sq("pd06", "The analysis of both attributes rests on the")
    sq("pd07", "PCP-007 §5.4 required the flow-through, wash and strip fractions to be sampled")
    sq("pd07", "No fraction result and no mass balance is in the record")
    sq("pd07", "Where host cell protein is removed within the step")
    sq("pd08", "A change in packing between or within campaigns therefore cannot be excluded from the record.")
    sq("pd09", "The study S-CEX-FRC was made and is reported, and it is in neither version of the plan.")
    sq("pd09", "Its fractionated run collected the eluate in fractions")
    sq("pd09", "Its results support the method decision for fragments")
    sq("pd10", "PCP-007 §7 and §8 name the evidence for seven decisions but no threshold.")
    sq("pd10", "This report states and applies its own approach for each")
    sq("pd10", "Three of the decisions could not be made as planned, because the packing records")
    sq("pd10", "Capability is given for the drug substance from the integrated model instead")
    sq("pd11", "PCP-007 §6.2 required the feed lot of every run to be recorded")
    sq("pd11", "A lot effect therefore cannot be separated from the run-order drift of host cell protein")
    sq("pd12", "Version 1.0 of this report named the load/wash buffer of lot")
    sq("pd12", "The lot is an acetate load/wash buffer.")
    sq("pd12", "The name in Version 1.0 was a transcription error, found in the Version 2.0 review.")
    sq("pd12", "The re-test pH of the lot,")
    sq("pd12", "The correction changes no result of this report.")

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
                        aliases=["cation exchange", "cation exchange chromatography", "CEX", P.DOC_REGISTRY[DOC][1],
                                 f"Step {G.CXSTEP}"],
                        review_status="human_verified")]
    alias = {"load": ["protein load", "load"], "wash_cond": ["load/wash conductivity", "conductivity"],
             "elution_ph": ["elution buffer pH", "pH"], "stop_collect": ["elution stop collect", "stop collect"],
             "flow": ["elution flow rate", "flow rate"]}
    concepts += [Concept(concept_id=PC[NAME[k]], concept_type="PROCESS_PARAMETER", canonical_name=NAME[k],
                         aliases=alias[k] + ([f"factor {LET[k]}"] if k in LET else []), review_status="human_verified")
                 for k in KEYS]
    concepts += G._attr_concepts(ckeys)
    concepts.append(Concept(concept_id="attr:step_yield", concept_type="PERFORMANCE_ATTRIBUTE",
                            canonical_name="Step yield", aliases=["step yield", "yield"],
                            review_status="human_verified"))
    concepts += G._method_concepts([m.method_id for m in methods], amv_title)
    concepts.append(Concept(concept_id=SDM_ID, concept_type="EQUIPMENT", canonical_name=SDM_NAME,
                            aliases=["scale-down model", "scale-down column", "laboratory column"],
                            review_status="human_verified"))
    concepts.append(Concept(concept_id=CHAMBER_ID, concept_type="EQUIPMENT", canonical_name=CHAMBER_NAME,
                            aliases=[EQ.name, "chamber"], review_status="human_verified"))

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
            "values of the parameter table, which are also the values in force. For the four multivariate parameters "
            "ProcessParameter.PAR is the NOR-propagated PAR, which is the range studied for both aggregate and host "
            "cell protein. Elution flow rate (GPP, univariate) has no PAR: the report states only that its range "
            "studied is supported by its own data for aggregate and host cell protein. rationale_for_criticality "
            "carries the classification argument of the report, each parameter anchored on its own sentences of it.",
            "The step sets no quality attribute. The QualityAttribute records are the five attributes the step clears "
            "(the attributes-in-scope table). acceptance_criteria holds the drug substance criterion of the register "
            "and, for aggregate, host cell protein and fragments, the Version 2.0 intermediate acceptance criterion of "
            "the pool in force with its a priori value; residual DNA and leached Protein A carry no criterion at this "
            "step. acceptance_criteria (the annex layer) holds the rows of the criteria-change table, Version 1.0 "
            "superseded and Version 2.0 in force. Step yield is a process performance attribute with no criterion: "
            "the concept attr:step_yield.",
            "proven_acceptable_ranges: the eight rows of the PAR table (aggregate and host cell protein against the "
            "four multivariate parameters), with par_at_setpoint and par_nor_propagated as the columns 'PAR at "
            "set-point' and 'PAR, NOR-propagated' print them; characterization_range is the range studied of the "
            "parameter table. The report's description of the two analyses is in report statements in its own words. "
            "Fragments have no adequate model and no PAR: an explicit non-claim.",
            "The schema has no record type for a discrepancy from the plan. PD-007-01 to PD-007-12 are report "
            "statements anchored on their rows of the discrepancy register; the studies they concern carry that row "
            "as a source reference.",
            "The report records no deviation: a characterization study is not GMP manufacture, so the two events of "
            "execution are study events, under the numbers Version 1.0 gave them (DEV-007-01, DEV-007-02). They are "
            "Deviation records, the schema's only record type for an event of execution; no_impact_on_conclusions is "
            "true for both, which the report judged from the data (the deletion of the run) and retained.",
            "Studies: S-CEX-SDM, S-CEX-SCR, S-CEX-RSM and S-CEX-UNI have StudyDesign records, each anchored on its row "
            "of the execution-window table. Only the two designs carry n_runs, which the corpus test reserves for the "
            "seeded DoE designs. The fractionated run and method comparability S-CEX-FRC (PD-007-09) has no study type "
            "in the schema, and the cation exchange runs S-CEX-VER and S-VI-WC belong to PCR-006 (PD-006-02, "
            "PD-006-03); the three are report statements on their rows of the execution-window table.",
            "StatisticalModelFit: the planned full quadratic of each output with a criterion (the re-evaluation "
            "table), the selected models of aggregate (log scale, all four adequacy criteria met), host cell protein "
            "(log scale, fails the criterion on residuals and influential runs, used for the ranges and the design "
            "space, PD-007-02), fragments (not adequate, no coefficient table, so its terms carry no values) and step "
            "yield, the three screening models, and the two models of the residual DNA clearance factor and of pool "
            "leached Protein A. A p-value printed as '< 0.001' has no float value; its term carries significant=true. "
            "The deletion of each flagged run and the models within two AICc units are report statements, one per row "
            "of their tables.",
            "parameter_impacts_attribute / parameter_does_not_significantly_impact_attribute: for aggregate and host "
            "cell protein, each multivariate parameter on every coefficient row of the selected model that contains "
            "it (a parameter affects the attribute when one of its terms is significant at the α of PCMP-001 §6.2), "
            "or on its screening effect row where the selected model has no term in it; for step yield on the rows of "
            "its selected model or of the screening model; elution flow rate on the rows of the comparison of the two "
            "ends; residual DNA clearance on the sentences that state its selected model has no term.",
            "The equipment ids equip:cex_sdm_column and equip:<chamber> follow the Version 1.0 report and the PCP-007 "
            "Version 2.0 annex.",
            "rhetorical_spans: authoring/rhetorical/PCR-007.spans.yaml, re-curated against the Version 2.0 text in the "
            "same pass as this builder. weak_claims is empty.",
        ] + G._unrendered_note(unrendered),
        inventory=G.rev2_inventory(DOC, FILE, "process_characterization_report", UO_NAME,
                                   ["process characterization", "cation exchange chromatography", "aggregate clearance",
                                    "host cell protein clearance", "intermediate acceptance criteria",
                                    "verification of platform worst cases", "design of experiments",
                                    "model selection", "log-scale models", "scale-down model qualification",
                                    "parameter classification"]),
        entities=entities, studies=studies, design_spaces=design_spaces, proven_acceptable_ranges=pars,
        report_sections=sections, assertions=AssertionStore(run_id=f"gt-{DOC}", assertions=AS, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{DOC}", concepts=concepts),
        weak_claims=[], rhetorical_spans=G.build_rhetorical_spans(DOC, FILE),
        acceptance_criteria=G.acceptance_criteria_layer(DOC, FILE, title("changes"), ct["tbl-criteria-change"][0],
                                                        [UO]))
    _gate(annex, text)
    return annex
