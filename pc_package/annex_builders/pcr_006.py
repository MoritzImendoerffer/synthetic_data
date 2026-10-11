"""PCR-006 Version 2.0, the characterization report of low-pH viral inactivation (Step 6), re-analysed
under INV-001 and INV-002: its ground-truth annex (``build()``).

The kinds of record follow the model builder for a Version 2.0 report with a designed experiment,
``build_ground_truth.build_report_protein_a`` (PCR-005), and the concept ids follow the Version 1.0
builder of this report (``build_report_viral_inactivation``) and the Version 2.0 builder of its plan
(``build_plan_viral_inactivation``): the inventory and the revision layer; the step, its scale-down
model and the two sites; the four parameters, with the class and the classification argument of the
report; the four attributes the step is judged against; the four analytical methods; the capability
records; the modular XMuLV contribution; the fitted models (the planned full quadratic of every output,
the selected models and the screening models); the two study events; the document relationships and the
explicit non-claims; the studies of the execution-window table that have a schema study type; the design
space; the proven acceptable ranges; the criteria of the criteria-change table (Version 1.0 superseded,
Version 2.0 in force); the assertions; the report statements, grouped by the chapters of the report; the
concepts; and the rhetorical spans of ``authoring/rhetorical/PCR-006.spans.yaml``.

Every table of the report is a complex table (``T.frame`` or a ``T.`` builder), read back through
``qmd_ctables`` from the object the report printed, or a markdown string of a ``_pcpkg`` helper
(``related_docs_md``, ``dev_register``, ``discrepancy_register``), read back with ``md_string_rows``,
so each row quote is the rendered row, with ``table_header=rows.header``. Every prose quote is a span of
the ``.qmd`` copied with its inline expressions and rendered as the ``.docx`` reads it (``_render``:
the inline expressions evaluated in the report's own namespace, a subscript as its own run, italics
dropped, a cross-reference resolved to its rendered number, typographic apostrophes), so no value is
typed here. ``q`` refuses a snippet that is not a span of the ``.qmd`` prose or that crosses a
citation, and ``build()`` refuses to return an annex with a quote that does not ground or a weak anchor.

The proven acceptable ranges are recorded as the report states them: the "PAR (set-point)" column of
the PAR table goes to ``par_at_setpoint`` as printed, and the report's description of the two analyses
is recorded in its own words. Nothing is added to it.
"""
from __future__ import annotations

import os
import re

import _pcpkg as P
import build_ground_truth as G
import schema_ext as S
from check_grounding import normalize, specificity_report

DOC = "PCR-006"
FILE = "PCR-006_viral_inactivation.docx"
QMD = "PCR-006_viral_inactivation.qmd"
UO = "viral_inactivation"
#: The scale-down model as the report names it (Section 3.1), the same vessel as PCP-006 names.
SDM_NAME = "temperature-controlled vessel at laboratory scale"

_INTRO = "Introduction"
_PRIOR = "Prior knowledge and quality risk basis"
_MM = "Materials and methods"
_SD = "Study design"
_RES = "Results"
_RSM = "Response-surface models"
_PAR = "Proven acceptable ranges"
_NOR = "The set-points and ranges in force, and the decisions behind them"
_REC = "Study events and discrepancies from the plan"
_EV = "Study events"
_PDS = "Discrepancies from the plan"
#: Section key -> heading path as the .qmd writes it (a heading may carry an inline expression, which
#: ``_title`` renders). ``_check_sections`` checks every title against the headings of the .qmd, so a
#: renamed section fails loudly instead of mislabelling its references.
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
    "stats": (_MM, "Statistical methods"),
    "factors": (_SD, "Factors, ranges and the knowledge space"),
    "scr_design": (_SD, "Screening design"),
    "rsm_design": (_SD, "Response-surface design"),
    "uni_design": (_SD, "Univariate assessment"),
    "centre": (_RES, "Centre-point performance and reproducibility"),
    "screening": (_RES, "Screening: factor effects"),
    "rsm": (_RES, _RSM),
    "near": (_RES, _RSM, "Models near the selected one"),
    "influence": (_RES, _RSM, "Influence analysis"),
    "mech": (_RES, "Mechanistic interpretation"),
    "ds": ("Design space",),
    "iac": (_PAR, "The acceptance basis"),
    "criteria": (_PAR, "The outputs against their criteria"),
    "hold": (_PAR, "Hold of the neutralized pool"),
    "par": (_PAR, "The ranges of the three factors"),
    "nor": (_PAR, _NOR),
    "ofat": (_PAR, _NOR, "Quality attributes at the new pH set-point"),
    "cex": (_PAR, _NOR, "Cation exchange on material from the step at the new pH set-point"),
    "wc": (_PAR, _NOR, "Confirmation runs at the low end of the pH PAR"),
    "uni": (_PAR, "A-Mab concentration"),
    "verif": (_PAR, "Verification of the platform worst cases"),
    "cap": ("Process capability and robustness",),
    "class": ("Parameter classification",),
    "cs": ("Contribution to the control strategy",),
    "disc": ("Discussion",),
    "concl": ("Conclusions",),
    "record": (_REC,),
    "events": (_REC, _EV),
    "dev1": (_REC, _EV, "DEV-006-01, hold-time record discrepancy between the control system and the "
                        "manual log"),
    "dev2": (_REC, _EV, "DEV-006-02, cytotoxicity of the XMuLV infectivity assay at low dilution"),
    "pds": (_REC, _PDS),
    "pd7": (_REC, _PDS, "`{python} PD_CONC`, XMuLV clearance not measured in the concentration study"),
    "pd8": (_REC, _PDS, "`{python} PD_POOL`, input pool of the design runs not tested"),
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
CHAPTERS = ["Executive summary", "Introduction", _PRIOR, _MM, _SD, _RES, "Design space", _PAR,
            "Process capability and robustness", "Parameter classification",
            "Contribution to the control strategy", "Discussion", "Conclusions", _REC]


def _sid(sec):
    return f"{DOC}_sec_{sec}"


def _source():
    return open(os.path.join(G.HERE, QMD), encoding="utf-8").read()


def _prose():
    """The .qmd outside its code chunks, in the comparison form (``normalize``)."""
    return normalize(re.sub(r"```\{python\}.*?```", " ", _source(), flags=re.S))


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


def _xrefs(text):
    """``{label -> rendered cross-reference}`` ("sec-iac" -> "Section 7.1", "tbl-par" -> "Table 23").

    A section number follows the numbering of the headings (an unnumbered heading takes none), as the
    rendered document prints it. A table or figure number is read off the rendered caption ("Table 23:
    <caption>"), with the caption taken from the chunk that prints it: a complex table's own caption, or
    the ``tbl-cap``/``fig-cap`` option of a labelled chunk."""
    out, counters = {}, [0] * 6
    for lvl, _, attrs in _headings():
        if ".unnumbered" in attrs or attrs.strip() == "-":
            continue
        counters[lvl - 1] += 1
        counters[lvl:] = [0] * (6 - lvl)
        lab = re.search(r"#(sec-[\w-]+)", attrs)
        if lab:
            out[lab.group(1)] = "Section " + ".".join(str(c) for c in counters[:lvl])
    caps = {}
    for code in re.findall(r"```\{python\}\n(.*?)```", _source(), flags=re.S):
        lab = re.search(r"#\|\s*label:\s*((?:tbl|fig)-[\w-]+)", code)
        cap = re.search(r'#\|\s*(?:tbl|fig)-cap:\s*"(.*)"', code)
        if lab and cap:
            caps[lab.group(1)] = cap.group(1)
    for lab, (tab, _) in G.qmd_ctables(QMD).items():
        caps.setdefault(lab, tab.caption)
    for lab, cap in caps.items():
        word = "Table" if lab.startswith("tbl-") else "Figure"
        m = re.search(word + r" (\d+): " + re.escape(normalize(cap)), text)
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
    """A rendered cell without its trailing footnote markers ("Lower 95 % confidence bound a)")."""
    return re.sub(r"(?:\s[a-z]\))+$", "", str(cell)).strip()


def _num(cell):
    """A number as the document prints it, back to a float ("−0.612", "16,000", "0.27 a)"); None for a
    cell that is not one ("< 0.001", "n.a.")."""
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
    import doe_report as D
    import numpy as np
    import tables as T
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    from annex_contract.concepts import Concept, ConceptStore
    from annex_contract.discourse import DocumentRelationship, ExplicitNonClaim
    from annex_contract.results import (Deviation, ModelTerm, ModularContribution, ProcessCapability,
                                        StatisticalModelFit)
    from annex_contract.summaries import ReportSection, ReportStatement

    _check_sections()
    ns, shown = G.qmd_namespace(QMD)
    ct = G.qmd_ctables(QMD)
    text = G._document_text(FILE)
    prose_src = _prose()
    xref = _xrefs(text)
    meta = G.meta

    def render(src):
        """A span of the .qmd as the .docx reads it."""
        s = G.qmd_inline(ns, src)
        if "[@" in s:
            raise ValueError(f"{DOC}: a quote crosses a citation, end it before: {src!r}")
        s = re.sub(r"@((?:sec|tbl|fig)-[\w-]*\w)", lambda m: f" {xref[m.group(1)]} ", s)
        s = re.sub(r"~([^~\s]+)~", r" \1 ", s)            # a subscript is a run of its own
        s = re.sub(r"\*([^*\n]+)\*", r"\1", s)             # italics
        return re.sub(r"\s+", " ", _smart(s)).strip()

    def q(src):
        """A prose span of the .qmd as it renders. ``src`` must be copied from the .qmd."""
        if normalize(src) not in prose_src:
            raise ValueError(f"{DOC}: not a span of the .qmd prose: {src!r}")
        return render(src)

    def t(txt):
        """Annex text with the report's own values (inline expressions evaluated in its namespace)."""
        return G.qmd_inline(ns, txt)

    def title(sec):
        return render(SEC[sec][-1]) if "`" in SEC[sec][-1] else SEC[sec][-1]

    def ref(sec, quote, table=None, rows=None, caption=None, label=None):
        r = G.ref(DOC, FILE, _sid(sec), title(sec), quote,
                  table_title=caption if table is None else table.caption,
                  table_id=label if table is None else table.label,
                  table_header=None if rows is None else rows.header)
        r.heading_path = [render(x) if "`" in x else x for x in SEC[sec]]
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
        """The rendered rows of the CTable the report printed under ``label``, keyed. Every row must
        name its own record (in cell ``cell``, footnote markers aside, or anywhere): a mis-keyed row
        grounds and attests the wrong thing."""
        tab = ct[label][0]
        rows_ = present_header(G.ctable_rows(tab, keys))
        bad = [k for k, row in rows_.items()
               if not (_unmark(_cells(row)[cell]) == name_of(k) if cell is not None else name_of(k) in row)]
        if bad:
            raise ValueError(f"{DOC} {label}: rows keyed to records they do not name: {bad}")
        return tab, rows_

    def fig_cap(label, n):
        """The first ``n`` sentences of the caption of figure ``label``, from the option of the chunk that draws it."""
        code = next(c_ for c_ in re.findall(r"```\{python\}\n(.*?)```", _source(), flags=re.S)
                    if re.search(r"#\|\s*label:\s*" + re.escape(label) + r"\s*$", c_, flags=re.M))
        cap = re.search(r'#\|\s*fig-cap:\s*"(.*)"', code).group(1)
        out_ = " ".join(re.findall(r"[^.]+\.", cap)[:n]).strip()
        if normalize(out_) not in text:
            raise ValueError(f"{DOC}: the caption of {label} does not ground: {out_!r}")
        return re.sub(r"\s+", " ", out_)

    def note_span(label, start):
        """The sentence of the notes of the complex table ``label`` that starts with ``start``, as printed."""
        notes = " ".join(t_ for _, t_ in ct[label][0].notes)
        m = re.search(re.escape(start) + r"[^.]*\.", notes)
        if not m or normalize(m.group(0)) not in text:
            raise ValueError(f"{DOC}: no note of {label} starts with {start!r}")
        return m.group(0)

    def md_rows(md, label):
        rows_ = G.md_string_rows(md)
        # a markdown table is markdown: pandoc renders its straight apostrophes typographic ("report’s")
        for k_, v_ in list(rows_.items()):
            if normalize(v_) not in text and normalize(_smart(v_)) in text:
                rows_[k_] = _smart(v_)
        cap = ns_caps[label]
        if normalize(f"{cap} {rows_.header}") not in text:
            raise ValueError(f"{DOC}: the caption of {label} no longer reads {cap!r}")
        return rows_, cap

    # ---- names and values of the report ----------------------------------------------------------
    fx, g, pv, wu = ns["fx"], ns["g"], ns["pv"], ns["wu"]           # wu: "pH 3.4", "110 min", as the report writes
    FAC, PK, NAME, UNIT = list(ns["FAC"]), list(ns["PK"]), ns["NAME"], ns["UNIT"]
    NOR, CLS = ns["NOR"], ns["CLS"]
    A_, X_, AC_, FR_ = ns["A"], ns["X"], ns["AC"], ns["FR"]                 # the four response keys
    FIT, RI, LAB = ns["FIT"], ns["RI"], ns["LAB"]
    UO_NAME, STEP_LABEL = G.VIUO_NAME, G.VISTEP_LABEL
    PC = G.VIPARAM_CONCEPT                                                 # parameter name -> concept id
    pkey = {NAME[k]: k for k in PK}
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))
    reg = P.cqa_reg.set_index("key")
    by_label = G._attr_key_by_label()
    resp_attr = {A_: "aggregates_hmw", X_: "lrv_xmulv", AC_: "acidic_variants", FR_: "fragments_lmw"}
    attr_resp = {v: k for k, v in resp_attr.items()}
    ns_caps = {}
    for code in re.findall(r"```\{python\}\n(.*?)```", _source(), flags=re.S):
        lab = re.search(r"#\|\s*label:\s*(tbl-[\w-]+)", code)
        cap = re.search(r'#\|\s*tbl-cap:\s*"(.*)"', code)
        if lab and cap:
            ns_caps[lab.group(1)] = cap.group(1)

    # ---- the rendered tables, from the objects the report printed --------------------------------
    pdf_ = ct["tbl-params"][1]
    pt_t, prow = keyed("tbl-params", list(pdf_["Parameter"]), str, cell=0)
    pdf_ = pdf_.set_index("Parameter")
    leg = G.captured_rows(shown["tbl-legend"], list(shown["tbl-legend"][1]["Factor"]))
    leg_cap = shown["tbl-legend"][3]
    cq_df = ct["tbl-cqa"][1]
    ckeys = [by_label[n] for n in cq_df["Attribute"]]
    cq_t, crow = keyed("tbl-cqa", ckeys, lambda k: names[k], cell=0)
    cq_df = cq_df.set_index(np.array(ckeys))
    sop_df = ct["tbl-sops"][1]
    sop_t, soprow = keyed("tbl-sops", list(sop_df["Reference"]), str, cell=1)
    amv_title = dict(zip(sop_df["Reference"], sop_df["Title"]))
    appd_df = ct["tbl-appd"][1]
    appd_t, appdrow = keyed("tbl-appd", list(appd_df["Method validation"]), str, cell=3)
    ch_df = ct["tbl-chronology"][1]
    ch_t, chrow = keyed("tbl-chronology", list(ch_df["Study"]), str, cell=1)
    off_t, offrow = keyed("tbl-sdm-offsets", [by_label[_cells(r)[0]] for r in ct["tbl-sdm-offsets"][0].rows()],
                          lambda k: T.ATTR_NAME[k], cell=0)
    ikeys = [by_label[_cells(r)[0]] for r in ct["tbl-iac"][0].rows()]
    iac_t, irow = keyed("tbl-iac", ikeys, lambda k: T.ATTR_NAME[k], cell=0)
    crkeys = [by_label[_cells(r)[0]] for r in ct["tbl-criteria-viral-inactivation"][0].rows()]
    cr_t, crrow = keyed("tbl-criteria-viral-inactivation", crkeys, lambda k: T.ATTR_NAME[k], cell=0)
    rvkeys = [by_label[_cells(r)[0]] for r in ct["tbl-reeval-viral-inactivation"][0].rows()]
    rv_t, rvrow = keyed("tbl-reeval-viral-inactivation", rvkeys, lambda k: T.ATTR_NAME[k], cell=0)
    cen_df = ct["tbl-centre"][1]
    cen_t, cenrow = keyed("tbl-centre", list(zip(cen_df["Design"], cen_df["Response"])),
                          lambda k: k[1], cell=1)
    sf_df = ct["tbl-screen-fit"][1]
    sf_t, sfrow = keyed("tbl-screen-fit", list(sf_df["Response"]), str, cell=0)
    se_df = ct["tbl-screen-eff"][1]
    se_resp = se_df["Response"].replace("", np.nan).ffill()
    se_t, serow = keyed("tbl-screen-eff", list(zip(se_resp, se_df["Term"])), lambda k: k[1], cell=1)
    coef = {}
    for r_, lab_ in ((A_, "tbl-coef-agg"), (X_, "tbl-coef-xmulv")):
        coef[r_] = keyed(lab_, list(ct[lab_][1]["Term"]), str, cell=0) + (ct[lab_][1].set_index("Term"),)
    anova = {}
    for r_, lab_ in ((A_, "tbl-anova-agg"), (X_, "tbl-anova-xmulv")):
        anova[r_] = keyed(lab_, list(ct[lab_][1]["Source"]), str, cell=0) + (ct[lab_][1].set_index("Source"),)
    ap_df = ct["tbl-appc-rsm"][1]
    ap_out = ap_df["Output"].replace("", np.nan).ffill()
    ap_t, aprow = keyed("tbl-appc-rsm", list(zip(ap_out, ap_df["Term"])), lambda k: k[1], cell=1)
    near_df = ct["tbl-near"][1]
    near_t, nearrow = keyed("tbl-near", list(range(len(near_df))), lambda i: near_df["Terms"].iloc[i], cell=2)
    inf_df = ct["tbl-influence"][1]
    inf_t, infrow = keyed("tbl-influence", list(range(len(inf_df))), lambda i: inf_df["Run deleted"].iloc[i],
                          cell=1)
    par_t, parrow = keyed("tbl-par", FAC, lambda k: f"{NAME[k]} ({UNIT[k]})", cell=0)
    nc_df = ct["tbl-nor-change"][1]
    nc_t, ncrow = keyed("tbl-nor-change", list(nc_df["Parameter"]), str, cell=0)
    mg_df = ct["tbl-par-margins"][1]
    mg_t, mgrow = keyed("tbl-par-margins", list(mg_df["Factor"]), str, cell=0)
    oe_name = {"Aggregate": "aggregates_hmw", "Fragments": "fragments_lmw", "Acidic variants": "acidic_variants"}
    oe_t, oerow = keyed("tbl-vi-ofat-effects", [oe_name[_cells(r)[0]] for r in ct["tbl-vi-ofat-effects"][0].rows()],
                        lambda k: {v: n for n, v in oe_name.items()}[k], cell=0)
    of_t = ct["tbl-vi-ofat"][0]
    ofrow = present_header(G.ctable_rows(of_t))
    cvn_t = ct["tbl-cex-verification-n"][0]
    cvnrow = present_header(G.ctable_rows(cvn_t))
    cv_t = ct["tbl-cex-verification"][0]
    cvrow = present_header(G.ctable_rows(cv_t))
    wc_t = ct["tbl-vi-worst-case"][0]
    wcrow = present_header(G.ctable_rows(wc_t))
    uni_t = ct["tbl-uni"][0]
    unirow = present_header(G.ctable_rows(uni_t))
    hold_t = ct["tbl-hold-viral-inactivation"][0]
    holdrow = present_header(G.ctable_rows(hold_t))
    short = {T.ATTR_NAME[k].rsplit(" (", 1)[0]: k for k in T.ATTR_NAME}
    ver_t, verrow = keyed("tbl-iac-verification", [short[_cells(r)[1]] for r in ct["tbl-iac-verification"][0].rows()],
                          lambda k: T.ATTR_NAME[k].rsplit(" (", 1)[0], cell=1)
    cap_df = ct["tbl-cap"][1]
    capkeys = [by_label[n] for n in cap_df["Attribute"]]
    cap_t, caprow = keyed("tbl-cap", capkeys, lambda k: names[k], cell=0)
    cap_df = cap_df.set_index(np.array(capkeys))
    mbs_t = ct["tbl-methods-by-study"][0]
    mbsrow = present_header(G.ctable_rows(mbs_t))
    mtx = {}
    for kind, label in (("screening", "tbl-doe-viral-inactivation-screening"),
                        ("rsm", "tbl-doe-viral-inactivation-rsm")):
        tab = ct[label][0]
        mtx[kind] = (tab, present_header(G.ctable_rows(tab, [int(_cells(r)[0]) for r in tab.rows()])))
    rel, rel_cap = md_rows(P.related_docs_md(DOC), "tbl-related")
    devrow, dev_cap = md_rows(P.dev_register(DOC), "tbl-dev")
    pdrow, pd_cap = md_rows(P.discrepancy_register(DOC), "tbl-discrepancies")
    PDS = ns["PDS"]

    def pdref(pid, sec="pds"):
        return ref(sec, pdrow[pid], rows=pdrow, caption=pd_cap, label="tbl-discrepancies")

    # ==== entities ===================================================================================
    q_step = q("Low-pH viral inactivation is Step 6 of the A-Mab drug substance process.")
    q_hold = q("The Protein A eluate is held at acid pH for a set time and then neutralized.")
    q_inact = q("The hold inactivates enveloped viruses.")
    q_load = q("The neutralized pool is the load of cation exchange.")
    q_adjust = q("It is adjusted to the inactivation pH, held for the hold time at the set temperature and then "
                 "neutralized with base.")
    step = S.ProcessStep(
        step_id="step:viral_inactivation", step_name=UO_NAME, step_number=str(G.VISTEP),
        unit_operation=UO_NAME,
        description=t("Step 6 of the A-Mab drug substance process. The Protein A eluate is adjusted to the "
                      "inactivation pH, held for the hold time at the set temperature, then neutralized with "
                      "base and filtered. The hold inactivates enveloped viruses and contributes one of the "
                      "three claims that meet the cumulative XMuLV requirement, `{python} fx(claim)` log10. "
                      "The same conditions can add aggregate, fragments and acidic variants, which are formed "
                      "upstream. No MVM clearance and no host cell protein clearance is claimed for the step. "
                      "The neutralized pool is the load of cation exchange."),
        input_materials=["Protein A eluate"],
        output_materials=["neutralized pool (cation exchange load)"],
        equipment=[SDM_NAME],
        source_references=[ref("exec", q_step), ref("exec", q_hold), ref("exec", q_inact),
                           ref("uo", q_adjust), ref("uo", q_load)],
        metadata=meta())
    q_sdm = q("The scale-down model holds the Protein A eluate in a temperature-controlled vessel at laboratory "
              "scale.")
    q_sop = q("The model was operated under SOP-2009 and qualified under SOP-1001.")
    equipment = [S.Equipment(
        equipment_id="equip:vi_sdm_vessel", equipment_name=SDM_NAME,
        equipment_type="hold vessel (scale-down model and spiking model)", site_name=P.SENDING_SITE,
        source_references=[ref("sdm", q_sdm), ref("sdm", q_sop),
                           ref("sdm", q("It is the scale-down model, run on the same Protein A eluate and at "
                                        "the same inactivation pH, hold time and temperature."))],
        metadata=meta())]
    sites = G._site_entities(DOC, FILE, _sid("title"))

    # -- parameters: the table row, its rows in the tables of the ranges in force and of the margins, the
    # factor legend, and the sentences of the classification argument (Section 9) --------------------
    acid_rise, fr_rise = ns["acid_rise"], ns["fr_rise_range"]
    EFX, PX, EFA, PA = ns["EFX"], ns["PX"], ns["EFA"], ns["PA"]
    PARX, MARG = ns["PARX"], ns["MARG"]
    claim, crit_agg = ns["claim"], ns["crit_agg"]
    WC_X, INF5 = ns["WC_X"], ns["INF5"]
    dev_min = ns["dev_006_01_time_discrepancy_min"]
    nor_half = ns["nor_half_ph"]
    q_cls_all = q("Hold time and temperature were classified as well-controlled critical process parameters "
                  "(WC-CPPs), and A-Mab concentration as a general process parameter (GPP).")
    cls_quotes = {
        "ph": [q("Inactivation pH was classified as a critical process parameter (CPP)."),
               q("*Inactivation pH (CPP).* A rise in pH across the range studied lowers the XMuLV log reduction "
                 "by `{python} fx(abs(EFX[\"ph\"]))` log~10~ (`{python} pv(PX[\"ph\"])`), which is "
                 "`{python} fx(abs(EFX[\"ph\"]) / claim * 100, 0)` % of the claim."),
               q("The margin from the upper NOR edge to the PAR edge is `{python} fx(MARG[\"ph\"])` pH units, so a "
                 "drift of the size the NOR allows about the set-point would reach the edge of the PAR."),
               q("On it the risk is high and the parameter is a CPP.")],
        "hold_time": [q_cls_all,
                      q("*Hold time (WC-CPP).* A longer hold raises the XMuLV log reduction by "
                        "`{python} fx(EFX[\"hold_time\"])` log~10~ over the range studied "
                        "(`{python} pv(PX[\"hold_time\"])`) and aggregate by `{python} fx(EFA[\"hold_time\"], 3)` "
                        "percentage points over the same range (`{python} pv(PA[\"hold_time\"])`)."),
                      q("The effect on a CQA makes the parameter critical."),
                      q("On it the risk is low and the parameter is a WC-CPP.")],
        "temperature": [q_cls_all,
                        q("*Temperature (WC-CPP).* A warmer hold raises the XMuLV log reduction by "
                          "`{python} fx(EFX[\"temperature\"])` log~10~ over the range studied "
                          "(`{python} pv(PX[\"temperature\"])`) and aggregate by "
                          "`{python} fx(EFA[\"temperature\"], 3)` percentage points "
                          "(`{python} pv(PA[\"temperature\"])`)."),
                        q("The effect on a CQA makes it critical."),
                        q("so the risk of falling outside the acceptable range is low on the same judgement as "
                          "the hold time")],
        "protein_conc": [q_cls_all,
                         q("*A-Mab concentration (GPP).* No effect of the concentration was detected on aggregate, "
                           "on acidic variants or on the XMuLV log reduction across the whole range studied, which "
                           "is the whole NOR of the parameter (@sec-uni)."),
                         q("Four runs cannot establish the absence of an effect of that size, so for that attribute "
                           "the class rests not on the absence of a detected effect but on how the hold acts."),
                         q("On the evidence available the parameter affects no CQA and no performance attribute of "
                           "the step, so it is a GPP.")],
    }
    u2_d, u2_x_lo, u2_x_hi = ns["u2_d"], ns["u2_x_lo"], ns["u2_x_hi"]
    margin_x = WC_X["predicted"] - claim
    head = "Classified {c} under SOP-4001 by the decision logic of PCMP-001 §7.7. "
    rationale = {
        "ph": head.format(c=CLS["ph"]) + (
            f"A rise in pH across the range studied lowers the XMuLV log reduction by {fx(abs(EFX['ph']))} "
            f"log10 ({pv(PX['ph'])}), {fx(abs(EFX['ph']) / claim * 100, 0)} % of the claim, and the claim is "
            f"lost at the upper edge of the PAR of pH {PARX['ph']}. The pH of a large acidified pool is set by "
            f"acid addition and mixing, the least directly controlled of the three settings, and pH control at "
            f"manufacturing scale holds about {fx(nor_half)} pH units, the half-width of the NOR. The margin from "
            f"the upper NOR edge to the PAR edge is {fx(MARG['ph'])} pH units, so a drift of the size the NOR "
            f"allows would reach the PAR edge. No plan sets the margin at which that risk becomes high; on that "
            f"comparison, a judgement of the report, the risk is high."),
        "hold_time": head.format(c=CLS["hold_time"]) + (
            f"A longer hold raises the XMuLV log reduction by {fx(EFX['hold_time'])} log10 "
            f"({pv(PX['hold_time'])}) and aggregate by {fx(EFA['hold_time'], 3)} percentage points "
            f"({pv(PA['hold_time'])}) over the range studied, and raises acidic variants by {fx(acid_rise, 1)} "
            f"points and fragments by about {fx(fr_rise, 2)} points over that range; the effect on a CQA makes it "
            f"critical. The lower PAR edge for XMuLV clearance lies {g(MARG['hold_time'])} min below the NOR, "
            f"{fx(100 * MARG['hold_time'] / (NOR['hold_time'][1] - NOR['hold_time'][0]), 0)} % of the width of "
            f"the NOR and {fx(MARG['hold_time'] / dev_min, 0)} times the largest hold-time record error of the "
            f"studies ({g(dev_min)} min, DEV-006-01). No plan sets the margin at which the risk becomes low; on "
            f"that comparison, a judgement of the report, the risk is low."),
        "temperature": head.format(c=CLS["temperature"]) + (
            f"A warmer hold raises the XMuLV log reduction by {fx(EFX['temperature'])} log10 "
            f"({pv(PX['temperature'])}) and aggregate by {fx(EFA['temperature'], 3)} percentage points "
            f"({pv(PA['temperature'])}) over the range studied; the effect on a CQA makes it critical. The lower "
            f"PAR edge lies {fx(MARG['temperature'], 1)} °C below the NOR, "
            f"{fx(100 * MARG['temperature'] / (NOR['temperature'][1] - NOR['temperature'][0]), 0)} % of the width "
            f"of the NOR, and the hold is held near ambient in a jacketed vessel, so the risk of leaving the PAR "
            f"is low on the same judgement as hold time. The temperature term of the XMuLV model depends on run "
            f"{INF5['run']}; the effect on aggregate holds in every model selected after a deletion "
            f"({fx(ns['agg_temp_lo'], 3)} to {fx(ns['agg_temp_hi'], 3)} percentage points, "
            f"{pv(ns['agg_temp_p_max'])} at its weakest)."),
        "protein_conc": head.format(c=CLS["protein_conc"]) + (
            f"No effect of the concentration was detected on aggregate, acidic variants or the XMuLV log "
            f"reduction across the range studied, which is the whole NOR of the parameter. For XMuLV clearance "
            f"four runs put the difference at the high end of the range at {fx(-u2_d)} log10, 95 % confidence "
            f"interval {fx(u2_x_lo)} to {fx(u2_x_hi)} log10, which reaches further on the side of a loss than the "
            f"margin of {fx(margin_x)} log10 the claim has over the NOR, so for that attribute the class rests on "
            f"how the hold acts: the acid denatures the envelope of the virus, and the antibody neither shields "
            f"the envelope nor takes part in that reaction. Neither concentration study measured fragments, and "
            f"for that attribute the class rests on the cleavage reaction. The parameter affects no CQA and no "
            f"performance attribute of the step."),
    }
    params = []
    for name, row in prow.items():
        k = pkey[name]
        r = pdf_.loc[name]
        unit = r["Unit"]
        refs = [ref("factors", row, pt_t, prow)]
        if name in ncrow:
            refs.append(ref("nor", ncrow[name], nc_t, ncrow))
            refs.append(ref("nor", mgrow[name], mg_t, mgrow))
            refs.append(ref("factors", leg[name], rows=leg, caption=leg_cap, label="tbl-legend"))
        refs += [ref("exec" if i == 0 else "class", x) for i, x in enumerate(cls_quotes[k])]
        multi = r["Study"] == "multivariate"
        params.append(S.ProcessParameter(
            parameter_id=PC[name], parameter_name=name, parameter_type=r["Class"], unit=unit,
            target_value=wu(k, r["Set-point"]), NOR=wu(k, r["NOR"]),
            PAR=wu(k, PARX[k] if multi else r["Range studied"]), associated_step=STEP_LABEL,
            rationale_for_criticality=rationale[k], study_type=str(r["Study"]),
            source_references=refs, metadata=meta()))

    # -- attributes: the register row, the row of the criterion derivation and the row of the outputs
    # against their criteria ----------------------------------------------------------------------------
    q_formed = q("Aggregate and acidic variants are formed in the production bioreactor, and the register assigns "
                 "fragments to harvest and clarification, where proteases released from lysed cells clip the "
                 "antibody.")
    q_rule = q("XMuLV clearance was assigned very high criticality by rule, because a viral contamination would "
               "harm the patient directly whatever its score.")
    method_of = {"lrv_xmulv": "AMV-3017", "aggregates_hmw": "AMV-3011", "acidic_variants": "AMV-3013",
                 "fragments_lmw": "AMV-3020"}
    if any(appd_df.loc[appd_df["Method validation"] == a, "Output"].iloc[0] not in
           (T.ATTR_NAME[k].rsplit(" (", 1)[0], "XMuLV log reduction factor") for k, a in method_of.items()):
        raise ValueError(f"{DOC}: the methods summary no longer pairs each output with its validation")
    attrs = []
    for key in ckeys:
        r = cq_df.loc[key]
        crit = [f"{r['Drug substance criterion']} (drug substance)",
                f"{_cells(irow[key])[-2]} {P.CFG.cqa(key)['unit'].replace(' (cumulative)', '')} (intermediate "
                f"acceptance criterion, neutralized pool)"]
        viral = key.startswith("lrv_")
        why = (f"Very high by rule for viral clearance, whatever the Tool #1 score ({r['Tool #1 score']})."
               if viral else f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = {r['Tool #1 score']}.")
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=names[key], attribute_type="CQA",
            unit=reg.loc[key, "unit"], acceptance_criteria=crit, analytical_method=method_of[key],
            associated_steps=[STEP_LABEL], rationale_for_criticality=why,
            criticality_level=r["Criticality"], tool1_score=int(r["Tool #1 score"]),
            tool2_severity=int(reg.loc[key, "tool2_severity"]),
            source_references=[ref("cqa", crow[key], cq_t, crow), ref("iac", irow[key], iac_t, irow),
                               ref("criteria", crrow[key], cr_t, crrow),
                               ref("cqa", q_rule if viral else q_formed)],
            metadata=meta()))

    # -- analytical methods: the procedure row, the methods-summary row, the sentence that names the method,
    # and for the two size-variant methods the rows of the methods-by-study table that name them -----------
    q_meth = {"AMV-3017": q("XMuLV titre was measured as the 50 % tissue culture infectious dose (TCID50) under "
                            "AMV-3017"),
              "AMV-3011": q("aggregate by SEC under AMV-3011"),
              "AMV-3013": q("acidic variants by icIEF under AMV-3013"),
              "AMV-3020": q("fragments by nrCE-SDS under AMV-3020")}
    methods = []
    for amv in [a for a in sop_df["Reference"] if a.startswith("AMV-")]:
        key = {v: k for k, v in method_of.items()}[amv]
        out_ = appd_df.loc[appd_df["Method validation"] == amv].iloc[0]
        methods.append(S.AnalyticalMethod(
            method_id=amv, method_name=amv_title[amv], method_type=G.METHOD_TYPE.get(amv),
            analytes=[out_["Output"]], associated_attributes=[f"attr:{key}"], validation_status="validated",
            source_references=[ref("analytics", soprow[amv], sop_t, soprow),
                               ref("app_d", appdrow[amv], appd_t, appdrow), ref("analytics", q_meth[amv])]
            + (G.size_variant_refs(DOC, FILE, title("analytics"), [UO], G.SIZE_VARIANT_TOKEN[amv], text, lead=1)
               if amv in G.SIZE_VARIANT_TOKEN else []),
            metadata=meta()))

    # -- capability: one record per row of the capability table ----------------------------------------
    CAPD, n_mc = ns["CAPD"], int(ns["n_mc"])
    cap_prose = {
        "lrv_xmulv": q("Cumulative XMuLV clearance has a capability index of "
                       "`{python} fx(CAPD.loc[\"lrv_xmulv\", \"Cpk\"])` against its floor of "
                       "`{python} fx(xmulv_req, 1)` log~10~, which `{python} cpk_verdict(CAPD.loc[\"lrv_xmulv\", "
                       "\"Cpk\"])` (PCMP-001 §7.9)."),
        "acidic_variants": q("Of the attributes the hold can add to, acidic variants have the lowest capability "
                             "index, `{python} fx(CAPD.loc[\"acidic_variants\", \"Cpk\"])`, which "
                             "`{python} cpk_verdict(CAPD.loc[\"acidic_variants\", \"Cpk\"])`."),
        "aggregates_hmw": q("Aggregate and fragments have indices of "
                            "`{python} fx(CAPD.loc[\"aggregates_hmw\", \"Cpk\"], 1)` and "
                            "`{python} fx(CAPD.loc[\"fragments_lmw\", \"Cpk\"], 1)`, far above the target."),
    }
    cap_prose["fragments_lmw"] = cap_prose["aggregates_hmw"]
    capab = []
    side = {"lower": "lower", "upper": "upper"}
    for key, row in caprow.items():
        c = cap_df.loc[key]
        capab.append(ProcessCapability(
            capability_id=f"{DOC}-CAP{len(capab) + 1:02d}", quality_attribute=f"attr:{key}", index_name="Cpk",
            index_value=_num(c["Cpk"]), specification_side=side.get(CAPD.loc[key, "spec_type"], "two_sided"),
            acceptance_range=c["Drug substance criterion"], mean=c["Mean"], standard_deviation=c["SD"],
            unit=reg.loc[key, "unit"], basis="simulated", n_batches=n_mc, unit_operation=UO_NAME,
            source_references=[ref("cap", row, cap_t, caprow), ref("cap", cap_prose[key])],
            metadata=meta()))

    # -- the modular XMuLV claim -----------------------------------------------------------------------
    q_claims = q("Low-pH inactivation claims `{python} fx(claim)` log~10~, anion exchange `{python} fx(claim_aex)` "
                 "log~10~ and virus filtration `{python} fx(claim_vf)` log~10~, which sum to "
                 "`{python} fx(claims_sum)` log~10~ against a requirement of `{python} fx(xmulv_req, 1)` log~10~.")
    q_cum_exec = q("The drug substance requires a cumulative clearance of xenotropic murine leukemia virus (XMuLV) "
                   "of at least `{python} fx(xmulv_req, 1)` log~10~, which three steps claim together, and the "
                   "claim of this step is `{python} fx(claim)` log~10~ of it.")
    q_surplus = q("The surplus is `{python} fx(claims_sum - xmulv_req)` log~10~, so a shortfall at this step larger "
                  "than that cannot be made up by the other two claims.")
    title_of = P.UNIT_OP_TITLES
    contributions = [ModularContribution(
        contribution_id=f"{DOC}-MC01", quantity=names["lrv_xmulv"], unit_operation=UO_NAME,
        step_value=f"{fx(claim)} log10", cumulative_value=f"{fx(ns['claims_sum'])} log10",
        requirement=f"≥ {fx(ns['xmulv_req'], 1)} log10", unit="log10",
        contributing_steps=[f"{title_of[k]} (Step {P.CFG.unit_op(k).step})" for k in ("aex", "virus_filtration")],
        source_references=[ref("iac", q_claims), ref("exec", q_cum_exec), ref("iac", q_surplus)],
        metadata=meta())]

    # -- fitted models ---------------------------------------------------------------------------------
    def term_label(term):
        """A term of the coefficient tables ("A", "B²") in words."""
        letter = {v: k for k, v in D.factor_letters(UO).items()}
        base = term.rstrip("²")
        name = " × ".join(NAME[letter[x]].lower() if letter[x] != "ph" else "inactivation pH" for x in base)
        return name + ("²" if term.endswith("²") else "")

    def terms_of(rows_, prefix=None):
        """The terms of a coefficient table (or of one output's block of Appendix C), besides the intercept,
        as the table prints them."""
        out_ = []
        for kk, row in rows_.items():
            term = kk[1] if isinstance(kk, tuple) else kk
            if (prefix is not None and kk[0] != prefix) or term == "Intercept":
                continue
            cells_ = _cells(row)
            if isinstance(kk, tuple):                    # Appendix C: Output | Term | Coef. | SE | t | p | Sig.
                coef_, se_, t_, p_ = cells_[2:6]
            else:                                         # Term | Coefficient | Std. err. | t | p-value
                coef_, se_, t_, p_ = cells_[1:5]
            out_.append(ModelTerm(term=term, factor=term_label(term), coefficient=_num(coef_),
                                  standard_error=_num(se_), t_statistic=_num(t_), p_value=_num(p_),
                                  significant=(p_.startswith("<") or (_num(p_) or 1) < float(ns["ALPHA"]))))
        return out_

    cen = {(d, r): _cells(row) for (d, r), row in cenrow.items()}
    rsm_cen = {r: cen[("Response surface", r)] for (d, r) in cen if d == "Response surface"}
    fits = []

    def fit_rec(resp, form, refs, **kw):
        fits.append(StatisticalModelFit(
            model_fit_id=f"{DOC}-FIT{len(fits) + 1:02d}", response=resp, unit_operation=UO_NAME,
            model_form=form, source_references=refs, metadata=meta(), **kw))

    # the full quadratic model PCP-006 §5.5 planned, on the planned runs (re-evaluation table)
    for key, row in rvrow.items():
        c = _cells(row)
        resp = attr_resp[key]
        fit_rec(resp, "full quadratic (planned, PCP-006 §5.5)", [ref("rsm", row, rv_t, rvrow)],
                n_runs=int(c[1]), r_squared=_num(c[2]), predicted_r_squared=_num(c[3]),
                adequacy_statement=f"Planned full quadratic on the {c[1]} planned runs: R² {c[2]}, predicted R² "
                                   f"{c[3]}, R² minus predicted R² {c[4]}; the model the output ends up with under "
                                   f"the model selection (PD-006-04): {_unmark(c[5])}.")
    # the selected models of aggregate and of the XMuLV log reduction (all four criteria of PCMP-001 §7.2)
    sel_prose = {
        A_: q("The model explains R² = `{python} fx(FIT[A][\"R2\"], 3)` of the variation, with an adjusted R² of "
              "`{python} fx(FIT[A][\"adjR2\"], 3)`, and predicts left-out runs at predicted R² = "
              "`{python} fx(FIT[A][\"predR2\"], 3)`, a difference of `{python} fx(FIT[A][\"gap\"], 3)` against the "
              "limit of `{python} fx(GAPMAX)`."),
        X_: q("The model explains R² = `{python} fx(FIT[X][\"R2\"], 3)`, with an adjusted R² of "
              "`{python} fx(FIT[X][\"adjR2\"], 3)` and a predicted R² of `{python} fx(FIT[X][\"predR2\"], 3)`, a "
              "difference of `{python} fx(FIT[X][\"gap\"], 3)` between R² and predicted R², again within the "
              "limit."),
    }
    terms_prose = {A_: q("The selected model of aggregate carries `{python} terms_text(FIT[A][\"names\"])`."),
                   X_: q("The selected model of the XMuLV log reduction carries "
                         "`{python} terms_text(FIT[X][\"names\"])`.")}
    rmse_x = q("Its residual standard deviation is `{python} fx(FIT[X][\"rmse\"])` log~10~, close to the pure-error "
               "standard deviation of the centre points, `{python} fx(sd_pe_x)` log~10~, so the model leaves no "
               "more scatter than replicate runs at the same settings show.")
    cen_label = {A_: LAB[A_], X_: LAB[X_]}
    for resp in (A_, X_):
        f_ = FIT[resp]
        ri = RI[resp]
        tab, rows_, df_ = coef[resp]
        at, arows, adf = anova[resp]
        mod, lof = _cells(arows["Model"]), _cells(arows["Lack of fit"])
        cc = rsm_cen[cen_label[resp]]
        refs = [ref("rsm", terms_prose[resp]), ref("rsm", sel_prose[resp]), ref("rsm", arows["Model"], at, arows),
                ref("rsm", arows["Lack of fit"], at, arows),
                ref("centre", cenrow[("Response surface", cen_label[resp])], cen_t, cenrow)]
        if resp == X_:
            refs.append(ref("rsm", rmse_x))
        fit_rec(resp, f"selected model (PD-006-04), raw scale, terms besides the intercept: "
                      f"{ns['terms_text'](f_['names'])}",
                refs, n_runs=int(f_["n"]), r_squared=_num(fx(f_["R2"], 3)), adjusted_r_squared=_num(fx(f_["adjR2"], 3)),
                predicted_r_squared=_num(fx(f_["predR2"], 3)), f_statistic=_num(mod[4]),
                p_value=_num(mod[5]), lack_of_fit_p=_num(lof[5]),
                rmse=_num(fx(f_["rmse"])) if resp == X_ else None,
                adequacy_statement=(
                    f"Meets all four adequacy criteria of PCMP-001 §7.2: model F-test p {mod[5]}; lack of fit p "
                    f"{lof[5]}; R² minus predicted R² {fx(f_['gap'], 3)} against the limit of {fx(ns['GAPMAX'])}; "
                    f"absolute residuals on predicted values {pv(ri['p_spread'])} and residuals on run order "
                    f"{pv(ri['p_order'])}; largest Cook's distance {fx(ri['cook_max'])} at run {ri['cook_run']}, "
                    f"below the F limit of {fx(ri['f_limit'])}; runs {P.join_and(ri['over'])} above the cut-off "
                    f"of {fx(ns['cook_lim'])} examined by deletion (Section 5.3.2)."),
                terms=terms_of(rows_), replicate_n=int(cc[2]), replicate_mean=cc[3], replicate_sd=cc[4],
                replicate_cv=cc[5])
    # fragments: the selected model is not adequate (limit on overfitting); acidic variants fit exactly
    fr_prose = [q("For fragments the selected model carries `{python} terms_text(FIT[FR][\"names\"])`."),
                q("It is significant (`{python} pv(FIT[FR][\"p\"])`) and shows no lack of fit "
                  "(`{python} pv(FIT[FR][\"p_lof\"])`), but R² = `{python} fx(FIT[FR][\"R2\"], 3)` (adjusted R² "
                  "`{python} fx(FIT[FR][\"adjR2\"], 3)`) falls to predicted R² = `{python} fx(FIT[FR][\"predR2\"], 3)`, "
                  "a difference of `{python} fx(FIT[FR][\"gap\"], 3)` against the limit of `{python} fx(GAPMAX)`."),
                q("The model therefore has more terms than these data support, and it sets no range.")]
    fr_rep = q("Fragments, measured by nrCE-SDS on the retained samples of the response-surface design, reproduce to "
               "a standard deviation of `{python} fx(fr_c_sd, 3)` points about a mean of `{python} fx(fr_c_mean)` % "
               "over those `{python} c_rsm` runs.")
    ffr = FIT[FR_]
    fit_rec(FR_, f"selected model (PD-006-04), raw scale, terms besides the intercept: "
                 f"{ns['terms_text'](ffr['names'])}; not adequate",
            [ref("rsm", x) for x in fr_prose] + [ref("centre", fr_rep)]
            + [ref("app_c", aprow[k], ap_t, aprow) for k in aprow if k[0] == LAB[FR_]],
            n_runs=int(ffr["n"]), r_squared=_num(fx(ffr["R2"], 3)), adjusted_r_squared=_num(fx(ffr["adjR2"], 3)),
            predicted_r_squared=_num(fx(ffr["predR2"], 3)), p_value=_num(pv(ffr["p"]).split("= ")[-1]),
            lack_of_fit_p=_num(pv(ffr["p_lof"]).split("= ")[-1]),
            adequacy_statement=(f"Not adequate by PCMP-001 §7.2: R² minus predicted R² {fx(ffr['gap'], 3)} exceeds the "
                                f"limit of {fx(ns['GAPMAX'])}, so the model sets no range and fragments are judged on "
                                f"their measured results. It meets the criterion on residuals and influential runs "
                                f"({pv(RI[FR_]['p_spread'])}, {pv(RI[FR_]['p_order'])}; runs "
                                f"{P.join_and(RI[FR_]['over'])} above the cut-off for examination, none at the F "
                                f"limit)."),
            terms=terms_of(aprow, prefix=LAB[FR_]),
            replicate_n=int(ns["c_rsm"]), replicate_mean=fx(ns["fr_c_mean"]), replicate_sd=fx(ns["fr_c_sd"], 3))
    fit_rec(AC_, f"selected model (PD-006-04), terms besides the intercept: {ns['terms_text'](FIT[AC_]['names'])}; "
                 f"exact fit, not adequate",
            [ref("rsm", q("For the acidic variants the full quadratic reproduces every result exactly, as @sec-centre "
                          "shows, and the criteria of PCMP-001 §7.2 cannot be applied to such a fit (@sec-stats).")),
             ref("rsm", q("The model that the selection returns carries `{python} terms_text(FIT[AC][\"names\"])` and "
                          "is not adequate, so it sets no range and the attribute is judged on its measured "
                          "results.")),
             ref("centre", cenrow[("Response surface", LAB[AC_])], cen_t, cenrow)],
            n_runs=int(FIT[AC_]["n"]),
            adequacy_statement="Not adequate: the results carry no scatter at a given hold time, so there is no pure "
                               "error for the lack-of-fit test and no residual mean square for the model F-test; the "
                               "criteria of PCMP-001 §7.2 cannot be applied and an exact fit is never adequate.",
            replicate_n=int(rsm_cen[LAB[AC_]][2]), replicate_mean=rsm_cen[LAB[AC_]][3],
            replicate_sd=rsm_cen[LAB[AC_]][4], replicate_cv=rsm_cen[LAB[AC_]][5])
    # the screening models: main effects and two-factor interactions, used for no prediction
    se_by = {}
    for (resp_lab, term), row in serow.items():
        se_by.setdefault(resp_lab, []).append((term, row))
    lab_resp = {LAB[r]: r for r in (A_, X_, AC_)}
    for lab_, row in sfrow.items():
        c = _cells(row)
        resp = lab_resp[lab_]
        scr_terms = [ModelTerm(term=term, factor=term_label(term), effect=_num(_cells(r_)[2]),
                               coefficient=_num(_cells(r_)[3]), standard_error=_num(_cells(r_)[4]),
                               p_value=_num(_cells(r_)[5]), significant=bool(_cells(r_)[6]))
                     for term, r_ in se_by.get(lab_, [])]
        cs_ = cen[("Screening", lab_)]
        fit_rec(resp, "screening model: main effects and two-factor interactions in coded units",
                [ref("screening", row, sf_t, sfrow), ref("centre", cenrow[("Screening", lab_)], cen_t, cenrow)]
                + [ref("screening", r_, se_t, serow) for _, r_ in se_by.get(lab_, [])],
                n_runs=int(c[1]), r_squared=_num(c[2]), adjusted_r_squared=_num(c[3]), predicted_r_squared=_num(c[4]),
                f_statistic=_num(c[5]), p_value=_num(c[6]), rmse=_num(c[7]),
                adequacy_statement=("The model reproduces the acidic variant results exactly, so it has no residual "
                                    "and no test; its fit statistics carry no information." if resp == AC_ else
                                    f"Screening model, used to identify effects and for no prediction; F {c[5]}, "
                                    f"p {c[6]}, RMSE {c[7]}."),
                terms=scr_terms, replicate_n=int(cs_[2]), replicate_mean=cs_[3], replicate_sd=cs_[4],
                replicate_cv=cs_[5])

    # -- study events --------------------------------------------------------------------------------------
    DEVS = ns["DEVS"].set_index("dev_id")
    dev1_x, dev1_a = ns["dev1_x"], ns["dev1_a"]
    dev_prose = {
        "DEV-006-01": [("exec", q("A hold-time record discrepancy of `{python} g(dev_006_01_time_discrepancy_min)` "
                                  "min between the control system and the manual log (DEV-006-01) changes the "
                                  "predicted log reduction by `{python} fx(dev1_x, 3)` log~10~ and the predicted "
                                  "aggregate by `{python} fx(dev1_a, 3)` percentage points.")),
                       ("dev1", q("The root cause recorded is an offset between the clocks of the two records.")),
                       ("dev1", q("A hold-time error of that size changes the predicted XMuLV log reduction by "
                                  "`{python} fx(dev1_x, 3)` log~10~, which is smaller than the residual standard "
                                  "deviation of its model, `{python} fx(FIT[X][\"rmse\"])` log~10~, and smaller "
                                  "than the margin of `{python} fx(WC_X[\"predicted\"] - claim)` log~10~ at the "
                                  "least favourable NOR combination.")),
                       ("dev1", q("The record names no single run, so the event is assessed for the design as a "
                                  "whole.")),
                       ("dev1", q("Every run was analysed at its design settings and retained in the analysis."))],
        "DEV-006-02": [("exec", q("Cytotoxicity of the infectivity assay at low dilution (DEV-006-02) raises the "
                                  "lowest titre the assay can report, which can only make a computed log reduction "
                                  "smaller.")),
                       ("dev2", q("The root cause recorded is the matrix of the sample, and the record names no "
                                  "component of it.")),
                       ("dev2", q("The record names no affected run either, so the event is assessed for the study "
                                  "as a whole.")),
                       ("dev2", q("A higher limit for the output titre can only make a computed log reduction "
                                  "smaller, never larger.")),
                       ("screening", q("Cytotoxicity of the assay at low dilution raises that lowest titre, and a "
                                       "higher output titre makes a computed log reduction smaller, so DEV-006-02 is "
                                       "one possible contributor to the difference."))],
    }
    dev_impact = {
        "DEV-006-01": f"A hold-time error of {g(dev_min)} min changes the predicted XMuLV log reduction by "
                      f"{fx(dev1_x, 3)} log10, smaller than the residual standard deviation of its model "
                      f"({fx(FIT[X_]['rmse'])} log10) and than the margin of {fx(margin_x)} log10 at the least "
                      f"favourable NOR combination, and the predicted aggregate by {fx(dev1_a, 3)} percentage points "
                      f"against a margin of {fx(crit_agg - ns['UPL_A'])} points to the criterion. The record names "
                      f"no single run; every run was analysed at its design settings and retained.",
        "DEV-006-02": f"Cytotoxic wells cannot be read for infection, so the titre of an affected sample is read from "
                      f"higher dilutions (cytotoxicity recorded at a dilution factor of "
                      f"{g(ns['dev_006_02_cytotox_dilution'])}), which raises the lowest titre the assay can report; "
                      f"a higher limit for the output titre can only make a computed log reduction smaller. The "
                      f"record names no affected run; every run was retained. The report names the event as one "
                      f"possible contributor to the larger pH effect of the screening design, and the record names "
                      f"no cause.",
    }
    devs = []
    for did, row in devrow.items():
        c = _cells(row)
        devs.append(Deviation(
            deviation_id=did, summary=c[1], unit_operation=UO_NAME, detected_during=c[2], disposition=c[3],
            impact_statement=dev_impact[did], no_impact_on_conclusions=(did == "DEV-006-01"),
            source_references=[ref("events", row, rows=devrow, caption=dev_cap, label="tbl-dev")]
            + [ref(s_, x) for s_, x in dev_prose[did]],
            metadata=meta()))
        if str(DEVS.loc[did, "disposition"]) != "retained":
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
    q_inv1 = q("Version 2.0 is issued under the QA investigation `{python} INV[\"id\"]`, which QA opened on "
               "`{python} INV[\"opened\"]` after its review of PCMR-001 Version 1.0 for readiness of the Biologics "
               "License Application (BLA) and closed on `{python} INV[\"closed\"]` with the classification "
               "`{python} INV[\"classification\"]`.")
    q_inv2 = q("A second investigation, `{python} INV2[\"id\"]`, opened on `{python} INV2[\"opened\"]` and closed on "
               "`{python} INV2[\"closed\"]` with the classification `{python} INV2[\"classification\"]`, applied "
               "the model-adequacy criteria of PCMP-001 §7.2 to every response-surface model with a criterion.")
    q_rollup = q("The ranges, classes and controls of this report roll up into the Process Characterization Master "
                 "Report PCMR-001.")
    q_cum3 = q("The cumulative XMuLV requirement is met by this step together with anion exchange (PCR-008) and "
               "virus filtration (PCR-009).")
    q_formed2 = q("Aggregate and acidic variants are formed in the production bioreactor (PCR-003) and fragments "
                  "during harvest and clarification (PCR-004), and this step adds a bounded amount to each "
                  "(@sec-verif).")
    relation("executed_under", "PCP-006", "The studies were run under the plan PCP-006, with which the report is "
             "paired.", "uo", q("This report is paired with the plan PCP-006, under which the studies were run."))
    relation("executed_under", "PCMP-001", "The report presents the Stage 1 characterization of the step under its "
             "plan PCP-006 and the master plan PCMP-001.", "exec",
             q("This report presents the Stage 1 characterization of the step under its plan PCP-006 and the master "
               "plan PCMP-001"))
    relation("rolls_up_into", "PCMR-001", "The ranges, classes and controls of the report roll up into PCMR-001.",
             "exec", q_rollup)
    relation("references", "PTP-001", "The process is transferred under PTP-001 from the development site to the "
             "commercial drug substance site.", "uo",
             q("The process is transferred under the Process Transfer Plan PTP-001 from the development site in "
               "`{python} SENDING_LOCATION` to the commercial drug substance site in `{python} RECEIVING_LOCATION`, "
               "where it runs at the `{python} f\"{V['commercial_scale_l']:,}\"` L scale."))
    relation("scoped_by", "RA-001", "RA-001 assessed every parameter of the step before characterization began.",
             "risk", q("RA-001 assessed every parameter of the step before characterization began."))
    relation("references", "INV-001", "Version 2.0 is issued under INV-001.", "changes", q_inv1)
    relation("references", "INV-002", "INV-002 applied the model-adequacy criteria of PCMP-001 §7.2 to every "
             "response-surface model with a criterion; its corrective action CA3 is the model selection of this "
             "report.", "changes", q_inv2)
    relation("references", "PCR-005", "The Protein A step that supplies the eluate is characterized under PCR-005.",
             "operation", q("Each run starts from Protein A eluate produced at the set-points of the Protein A step, "
                            "which is characterized under PCR-005."))
    q_cex_ufdf = q("Those analyses are in PCR-007 and PCR-010, the characterization reports of cation exchange and of "
                   "UF/DF.")
    relation("references", "PCR-007", "The cation exchange verification that tightened the aggregate criterion of "
             "this step is in PCR-007, the characterization report of cation exchange.", "iac", q_cex_ufdf)
    relation("references", "PCR-010", "The UF/DF rise in aggregate that tightened the aggregate criterion of this step "
             "is in PCR-010, the characterization report of UF/DF.", "iac", q_cex_ufdf)
    relation("references", "PCR-003", "PCR-003 argues the widened aggregate criterion of the production bioreactor "
             "output and its risk.", "verif", q("PCR-003 argues the widened criterion and its risk for the bioreactor."))
    relation("references", "PCR-008", "Anion exchange (PCR-008) is one of the three claims that meet the cumulative "
             "XMuLV requirement.", "cs", q_cum3)
    relation("references", "PCR-009", "Virus filtration (PCR-009) is one of the three claims that meet the "
             "cumulative XMuLV requirement.", "cs", q_cum3)
    relation("references", "PCR-004", "Fragments are formed during harvest and clarification (PCR-004), and this "
             "step adds a bounded amount to them.", "cs", q_formed2)

    # -- explicit non-claims, by section --------------------------------------------------------------------
    ncs, nc_at = [], {}

    def nclaim(sec, subject, statement, quotes, rationale=None, elsewhere=None, uo=UO_NAME):
        ncs.append(ExplicitNonClaim(
            non_claim_id=f"{DOC}-NC{len(ncs) + 1:02d}", subject=subject, unit_operation=uo,
            statement=statement, rationale=rationale, handled_elsewhere=elsewhere,
            source_references=[ref(s_, x) for s_, x in quotes], metadata=meta()))
        nc_at.setdefault(sec, []).append(ncs[-1])

    nclaim("uo", "MVM clearance", "No clearance of the parvovirus MVM is claimed for the step.",
           [("uo", q("No claim is made for the parvovirus minute virus of mice (MVM), which has no lipid envelope "
                     "for low pH to disrupt.")),
            ("cs", q("MVM clearance is claimed by anion exchange and virus filtration, and this step claims none, "
                     "because a parvovirus has no lipid envelope for low pH to disrupt."))],
           rationale="A parvovirus has no lipid envelope for low pH to disrupt.",
           elsewhere="anion exchange and virus filtration")
    nclaim("uo", "host cell protein clearance", "No clearance of host cell protein is claimed for the step.",
           [("uo", q("No clearance of host cell protein is claimed for the step.")),
            ("cs", q("The criteria assume no change in host cell protein across this step, and no clearance of it "
                     "is claimed here (PCR-005)."))])
    nclaim("platform", "change in the glycan attributes", "The step was not expected to change the glycan "
           "attributes, which are formed in the production bioreactor and changed by no downstream step.",
           [("platform", q("The step was not expected to change the glycan attributes.")),
            ("platform", q("Those are formed in the production bioreactor, and no downstream step changes them "
                           "(PCMP-001 §3)."))],
           rationale="The glycan attributes are formed in the production bioreactor.")
    nclaim("sdm", "scale-down offset of fragments and of XMuLV clearance",
           "The qualification compared neither fragments nor XMuLV clearance at both scales, so the offset of each "
           "is unknown rather than zero, and both are judged as the laboratory model gives them.",
           [("sdm", q("The qualification compared neither fragments nor XMuLV clearance at both scales, so the "
                      "offset of each is unknown rather than zero.")),
            ("sdm", q("These two outputs are judged as the laboratory model gives them, with no translation to "
                      "manufacturing scale."))],
           rationale="For fragments the representativeness rests on the mechanism of the step; for viral clearance "
                     "on the spiking model, whose matrix, pH and temperature are those of manufacture.")
    nclaim("operation", "measured A-Mab concentration of the design runs",
           "The input pool was not tested, so the A-Mab concentration of the design runs is the value set and not a "
           "measured result.",
           [("operation", q("The input pool was not tested, so that is the value set and not a measured result "
                            "(PD-006-08)."))], elsewhere="PD-006-08")
    nclaim("analytics", "fragment results by SEC",
           "The SEC fragment results of the designs are kept in the record and used for no decision; the screening "
           "design has SEC fragment results only.",
           [("analytics", q("The screening samples were not retained, so the screening design has SEC fragment "
                            "results only.")),
            ("analytics", q("Those results are kept in the record and are used for no decision in this report."))],
           rationale="SEC reads fragments high in this matrix, because part of the host cell protein elutes in its "
                     "low molecular weight window (INV-001 finding 6).")
    nclaim("analytics", "fragment results of the qualification and concentration studies",
           "The qualification study and the two concentration studies measured no fragments, and no fragment result "
           "is claimed for any of them.",
           [("analytics", q("The qualification study and the two concentration studies measured no fragments, and "
                            "no fragment result is claimed for any of them."))])
    nclaim("stats", "prediction from the screening model", "No prediction of the report comes from the screening "
           "model; every prediction, PAR, the design space and the verification come from the response-surface "
           "model.",
           [("stats", q("Its centre points can detect curvature but cannot attribute it to a factor, so no "
                        "prediction in this report comes from it."))],
           rationale="The screening model identifies effects; its centre points cannot attribute curvature to a "
                     "factor.")
    nclaim("near", "predicted fragment levels", "The predicted levels of fragments are not carried into any "
           "conclusion of the report, and fragments set no range.",
           [("near", q("The selected model decides, so fragments set no range, and their predicted levels are not "
                       "carried into any conclusion of this report."))])
    nclaim("ds", "operation outside the region studied", "A move outside the region studied has no evidence in the "
           "report and needs new characterization data.",
           [("ds", q("A move outside the region studied has no evidence in this report and needs new "
                     "characterization data."))])
    nclaim("hold", "hold of a pool from the edge of the NOR", "The hold study bounds what a hold adds to a pool made "
           "at the set-points as characterized, not to a pool from the edge of the NOR.",
           [("hold", q("The conclusion covers that one pool, at the two temperatures and over the time tested.")),
            ("hold", q("The study used material made at the set-points as characterized, so it bounds what a hold "
                       "adds to a pool of that composition and not what it adds to a pool from the edge of the "
                       "NOR."))])
    nclaim("par", "proven acceptable ranges of acidic variants and fragments", "Acidic variants and fragments set no "
           "PAR, because neither has an adequate model.",
           [("par", q("Acidic variants and fragments have no adequate model, so neither sets a PAR."))],
           rationale="Their measured results meet their criteria throughout the designs, which span the region "
                     "studied.")
    nclaim("par", "ranges beyond the range studied", "A range that reaches the end of the range studied is reported "
           "as reaching it, and no claim is made beyond it.",
           [("par", note_span("tbl-par", "A range that reaches the end of the range studied"))])
    nclaim("ofat", "viral clearance at the new pH set-point", "S-VI-OFAT measured no viral clearance; it supports "
           "the new set-point for product quality only, and the clearance there comes from the model.",
           [("ofat", q("The study measured no viral clearance, so it supports the new set-point for product quality "
                       "only, and the clearance there comes from the model (@sec-criteria)."))])
    nclaim("uni", "range of A-Mab concentration for fragments", "The range of A-Mab concentration is not supported "
           "for fragments, which neither concentration study measured.",
           [("uni", q("The range is not supported for fragments, which neither study measured.")),
            ("uni", q("For that attribute the class of the parameter rests on the cleavage reaction itself."))],
           rationale="The samples of S-VI-UNI were not retained, and SEC is biased in this matrix.")
    nclaim("verif", "allowance for a hold beyond the NOR", "The aggregate criterion carries no allowance for a hold "
           "longer than the upper end of the NOR, which is a departure from the control strategy of the step.",
           [("verif", q("A hold longer than the upper end of the NOR is a departure from the control strategy of the "
                        "step, handled under the quality system of ICH Q10, and the criterion carries no allowance "
                        "for one."))], elsewhere="the quality system of ICH Q10")
    nclaim("cap", "change of the step for the acidic variant capability", "No change of the step is proposed on the "
           "ground of the acidic variant capability index, which the production bioreactor sets.",
           [("cap", q("A longer hold would raise the index, and no change of this step is proposed on that ground, "
                      "because the index is set by the level the production bioreactor forms and by its batch "
                      "spread."))], elsewhere="PCR-003")
    nclaim("changes", "deviations", "The report records no deviation: a process characterization study is not GMP "
           "manufacture, so events of execution are study events and departures from the plan are discrepancies "
           "from the plan.",
           [("changes", q("A process characterization study is not manufacture under good manufacturing practice "
                          "(GMP), so this report records no deviation, and the departures found in the re-analysis "
                          "are discrepancies from the plan (@sec-record)."))])

    entities = [
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("exec"), process_steps=[step], sites=sites,
                                  contributions=contributions),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("uo"), document_relationships=rels,
                                  non_claims=nc_at["uo"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("changes"), non_claims=nc_at["changes"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("platform"), non_claims=nc_at["platform"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cqa"), quality_attributes=attrs),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("sdm"), equipment=equipment,
                                  non_claims=nc_at["sdm"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("operation"), non_claims=nc_at["operation"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("analytics"), analytical_methods=methods,
                                  non_claims=nc_at["analytics"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("stats"), non_claims=nc_at["stats"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("factors"), parameters=params),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("rsm"), model_fits=fits),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("near"), non_claims=nc_at["near"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("ds"), non_claims=nc_at["ds"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("hold"), non_claims=nc_at["hold"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("par"), non_claims=nc_at["par"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("ofat"), non_claims=nc_at["ofat"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("uni"), non_claims=nc_at["uni"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("verif"), non_claims=nc_at["verif"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cap"), capabilities=capab,
                                  non_claims=nc_at["cap"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("record"), deviations=devs),
    ]

    # ==== studies: each on its row of the execution-window table, its prose, its data rows and the row of
    # the discrepancy register that records it ===============================================================
    pd_of = {s_: d["id"] for d in P.PLAN_DISCREPANCIES[DOC] for s_ in (d.get("studies") or [])}
    CHR = ns["CHR"]
    names_fac = [NAME[k] for k in FAC]
    conc = NAME["protein_conc"]
    cur, uni_rows = None, {}                          # the rows of tbl-uni by study (a merged first cell)
    for row in unirow.values():
        cur = _cells(row)[0] or cur
        uni_rows.setdefault(cur, []).append(row)
    study_spec = {
        "S-VI-SDM": dict(study_type="scale_down_qualification",
                         design_name="set-point runs of the scale-down model against manufacturing-scale batches",
                         responses=[A_, AC_],
                         prose=[("sdm", q("The qualification study S-VI-SDM ran from `{python} win(\"S-VI-SDM\")`, "
                                          "before the first characterization run.")),
                                ("sdm", q("It compared `{python} int(off_agg[\"n_sd\"])` runs of the scale-down "
                                          "model at set-point with `{python} int(off_agg[\"n_m\"])` "
                                          "manufacturing-scale batches, for aggregate and acidic variants in the "
                                          "neutralized pool."))],
                         rows=[(("sdm", r_, off_t, offrow)) for r_ in offrow.values()]
                         + [("analytics", soprow["SOP-1001"], sop_t, soprow)]),
        "S-VI-SCR": dict(study_type="screening_doe",
                         design_name="two-level full factorial with centre points", factors=names_fac,
                         responses=list(D.responses(UO)) + D.fragment_responses(UO, "screening"),
                         n_runs=P.doe_runs(UO, "screening"), n_center_points=P.doe_centre_points(UO, "screening"),
                         prose=[("scr_design", q("The screening design S-VI-SCR was a two-level full factorial "
                                                 "design in inactivation pH, hold time and temperature with "
                                                 "`{python} c_scr` centre points, `{python} n_scr` runs in all, "
                                                 "executed in random order from `{python} win(\"S-VI-SCR\")`.")),
                                ("scr_design", q("Every combination of the low and high ends of the three ranges "
                                                 "was run, so the design estimates all three main effects and all "
                                                 "three two-factor interactions without aliasing."))],
                         rows=[("app_a", r_, mtx["screening"][0], mtx["screening"][1])
                               for r_ in mtx["screening"][1].values()]),
        "S-VI-RSM": dict(study_type="response_surface_doe", design_name="face-centred central composite design",
                         factors=names_fac,
                         responses=list(D.responses(UO)) + D.fragment_responses(UO, "rsm"),
                         n_runs=P.doe_runs(UO, "rsm"), n_center_points=P.doe_centre_points(UO, "rsm"),
                         prose=[("rsm_design", q("The response-surface design S-VI-RSM was a face-centred central "
                                                 "composite design in the same three factors, with "
                                                 "`{python} n_fac_rsm` factorial runs, `{python} n_ax` axial runs "
                                                 "and `{python} c_rsm` centre points, `{python} n_rsm` runs in all, "
                                                 "executed in random order from `{python} win(\"S-VI-RSM\")`")),
                                ("rsm_design", q("The axial runs lie at the centres of the faces of the design "
                                                 "cube, at the ends of each range studied, so every run stayed "
                                                 "inside the range studied."))],
                         rows=[("app_b", r_, mtx["rsm"][0], mtx["rsm"][1]) for r_ in mtx["rsm"][1].values()]),
        "S-VI-UNI": dict(study_type="univariate",
                         design_name="one factor at a time, both ends of the range studied in duplicate",
                         factors=[conc], responses=[A_, AC_],
                         prose=[("uni_design", q("A-Mab concentration was assessed one factor at a time in study "
                                                 "S-VI-UNI, from `{python} win(\"S-VI-UNI\")`.")),
                                ("uni_design", q("The study measured aggregate and acidic variants only, which is "
                                                 "registered as PD-006-07, the clearance the concentration study "
                                                 "did not measure (@sec-record)."))],
                         rows=[("uni", r_, uni_t, unirow) for r_ in uni_rows["S-VI-UNI"]]),
        "S-VI-UNI2": dict(study_type="univariate",
                          design_name="confirmation study, both ends of the range studied in duplicate, XMuLV "
                                      "spiked", factors=[conc], responses=[X_, A_, AC_],
                          prose=[("uni", q("Study S-VI-UNI2 measured the XMuLV log reduction at both ends of the "
                                           "range, in duplicate, with the other parameters at their set-points as "
                                           "characterized.")),
                                 ("uni", q("It ran from `{python} win(\"S-VI-UNI2\")` and measured no fragments "
                                           "(@sec-methods)."))],
                          rows=[("uni", r_, uni_t, unirow) for r_ in uni_rows["S-VI-UNI2"]]),
        "S-VI-HLD": dict(study_type="univariate",
                         design_name="hold study: one neutralized pool made at the set-points as characterized, "
                                     "held at two temperatures and sampled over the hold",
                         factors=["hold time", "hold temperature"], responses=[A_, FR_, AC_],
                         prose=[("hold", q("One pool made at the set-points as characterized was held at "
                                           "`{python} join_and(H_TEMPS)` for `{python} H_DAYS` days, and aggregate, "
                                           "acidic variants and fragments were measured at every time point."))],
                         rows=[("hold", r_, hold_t, holdrow) for r_ in holdrow.values()]),
        "S-VI-OFAT": dict(study_type="one_factor_at_a_time",
                          design_name="the new inactivation pH set-point against the former one as control, over "
                                      "hold times in duplicate",
                          factors=[NAME["ph"], "hold time"], responses=[A_, FR_, AC_],
                          prose=[("ofat", q("Study S-VI-OFAT therefore held the pool at `{python} sp_t[\"ph\"]` "
                                            "against `{python} spc_t[\"ph\"]` as a control, at `{python} g(of_temp)` "
                                            "°C, over hold times of `{python} join_and([g(h) for h in of_hold])` "
                                            "min, in duplicate at each pH and hold time, `{python} of_n` runs per "
                                            "pH.")),
                                 ("ofat", q("Each attribute was analysed on the pH, as a two-level factor, and the "
                                            "hold time, so the difference between the two pH values is estimated at "
                                            "any hold time."))],
                          rows=[("ofat", r_, of_t, ofrow) for r_ in ofrow.values()]),
    }
    studies, unrendered, no_type = [], [], []
    for _, r in CHR.reset_index().iterrows():
        sid_ = r["id"]
        if sid_ not in chrow:
            if r["step"] == UO:
                unrendered.append(sid_)
            continue
        if sid_ not in study_spec:
            no_type.append(sid_)
            continue
        if not G._present(chrow[sid_], text):
            unrendered.append(sid_)
            continue
        spec = dict(study_spec[sid_])
        prose_, rows_ = spec.pop("prose"), spec.pop("rows")
        refs = [ref("uni_design", chrow[sid_], ch_t, chrow)]
        refs += [ref(s_, x) for s_, x in prose_]
        refs += [ref(s_, r_, tab_, rr_) for s_, r_, tab_, rr_ in rows_]
        if sid_ in pd_of:
            refs.append(pdref(pd_of[sid_]))
        studies.append(S.StudyDesign(
            study_id=f"study:{sid_}", unit_operation=UO_NAME, scale_down_model=SDM_NAME,
            associated_parameters=[PC[x] for x in spec.get("factors", []) if x in PC],
            source_references=refs, metadata=meta(), **spec))

    # ==== design space and the proven acceptable ranges =====================================================
    q_ds = [q("The design space of the step is the region of inactivation pH, hold time and temperature over "
              "which every attribute with a criterion at this step meets it."),
            q("Aggregate is inside when both ends of the `{python} PI` % prediction interval of a single run lie "
              "within its criterion at manufacturing scale, and the XMuLV log reduction is inside when its mean "
              "prediction reaches the claim."),
            q("Of the region studied, `{python} fx(100 * DSG[\"fraction\"], 1)` % meets the criteria of the two "
              "outputs that have an adequate model."),
            q("XMuLV clearance alone rejects `{python} fx(100 * DSG[\"per_response\"][X], 1)` % of the grid, and "
              "aggregate rejects none of it."),
            q("Acidic variants and fragments have no adequate model, so neither draws a boundary."),
            q("The NOR in force lies inside the design space, with the margins @sec-nor gives, and the region "
              "studied is the knowledge space of this report.")]
    design_spaces = [S.DesignSpace(
        design_space_id="ds:viral_inactivation", unit_operation=UO_NAME, parameters=[PC[n] for n in names_fac],
        quality_attributes_constrained=["attr:lrv_xmulv"],
        definition=t("The region of inactivation pH, hold time and temperature over which every attribute with a "
                     "criterion at the step meets it (PCP-006 §7.6), evaluated on a grid of `{python} grid_n` levels "
                     "of each factor over the ranges studied, `{python} f\"{DSG['n_points']:,}\"` points in all. "
                     "Aggregate is inside when both ends of the `{python} PI` % prediction interval of a single run "
                     "lie within its criterion at manufacturing scale, and the XMuLV log reduction is inside when "
                     "its mean prediction reaches the claim. `{python} fx(100 * DSG[\"fraction\"], 1)` % of the region "
                     "studied meets the criteria of the two outputs with an adequate model: XMuLV clearance alone "
                     "rejects `{python} fx(100 * DSG[\"per_response\"][X], 1)` % of the grid and aggregate none, so "
                     "the region is bounded by the clearance claim and not by product quality. Acidic variants and "
                     "fragments have no adequate model and draw no boundary; their measured results meet their "
                     "criteria across the designs. Judging both modelled outputs on their mean predictions gives "
                     "the same region. The NOR in force lies inside it, and the region studied is the knowledge "
                     "space."),
        source_references=[ref("ds", x) for x in q_ds], metadata=meta())]

    PT = ns["PT"]
    iac_ = D.iac_table(UO).set_index("response")

    def basis_of(resp):
        ia = iac_.loc[resp]
        stat = ("the mean prediction at the least favourable combination of NOR low, set-point and NOR high of "
                "the other two factors" if resp == X_ else
                "the 95 % prediction interval of a single batch at manufacturing scale, the other two factors "
                "varying within their NORs")
        return (f"Intermediate acceptance criterion {T.crit(ia['iac_low'], ia['iac_high'], ia['spec_type'])} "
                f"({ia['basis']}) of PCMP-001 Version 2.0, PCP-006 §7.2; judged on {stat}, on the selected "
                f"response-surface model.")
    q_agg_par = q("Aggregate meets its criterion across the whole range studied of each factor on the selected model, "
                  "so its PAR is the range studied in all three.")
    q_agg_fig = q("In @fig-par-agg the predicted aggregate rises from `{python} fx(AGG_H[RNG[\"hold_time\"][0]])` % "
                  "at `{python} g(RNG[\"hold_time\"][0])` min to `{python} fx(AGG_H[RNG[\"hold_time\"][1]])` % at "
                  "`{python} g(RNG[\"hold_time\"][1])` min with the other two factors at their set-points, a rise of "
                  "`{python} fx(agg_h_rise)` percentage points, against a criterion of `{python} fx(crit_agg)` %.")
    q_par_x = q("Its PAR is `{python} wu(\"ph\", PARX[\"ph\"])`, `{python} wu(\"hold_time\", PARX[\"hold_time\"])` and "
                "`{python} wu(\"temperature\", PARX[\"temperature\"])`.")
    pars = []
    for k in FAC:
        row = PT[(PT["CQA"] == LAB[X_]) & (PT["Parameter"] == NAME[k])].iloc[0]
        c = _cells(parrow[k])
        if (c[1], c[3], c[4]) != (row["Char. range"], row["PAR (set-point)"], row["PAR (NOR)"]):
            raise ValueError(f"{DOC}: the PAR table no longer prints the engine's ranges for {k}")
        pars.append(S.ProvenAcceptableRange(
            par_id=f"{DOC}-PAR{len(pars) + 1:02d}", unit_operation=UO_NAME, quality_attribute=LAB[X_],
            parameter=NAME[k], characterization_range=wu(k, c[1]), par_at_setpoint=wu(k, c[3]),
            par_nor_propagated=wu(k, c[4]), acceptance_basis=basis_of(X_),
            source_references=[ref("par", parrow[k], par_t, parrow), ref("par", q_par_x)], metadata=meta()))
    for k in FAC:
        row = PT[(PT["CQA"] == LAB[A_]) & (PT["Parameter"] == NAME[k])].iloc[0]
        if not (row["PAR (set-point)"] == row["PAR (NOR)"] == row["Char. range"]):
            raise ValueError(f"{DOC}: the aggregate PAR of {k} is no longer the range studied, as the text says")
        refs = [ref("par", q_agg_par)] + ([ref("par", q_agg_fig)] if k == "hold_time" else [])
        pars.append(S.ProvenAcceptableRange(
            par_id=f"{DOC}-PAR{len(pars) + 1:02d}", unit_operation=UO_NAME, quality_attribute=LAB[A_],
            parameter=NAME[k], characterization_range=wu(k, row["Char. range"]),
            par_at_setpoint=wu(k, row["PAR (set-point)"]), par_nor_propagated=wu(k, row["PAR (NOR)"]),
            acceptance_basis=basis_of(A_), source_references=refs, metadata=meta()))

    # ==== assertions ======================================================================================
    AS = []

    def add(subj, pred, obj, txt, refs):
        AS.append(EvidenceBackedAssertion(
            assertion_id=f"{DOC}-A{len(AS) + 1:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=txt, source_references=refs, metadata=meta()))

    add("step:viral_inactivation", "step_uses_equipment", "equip:vi_sdm_vessel",
        f"The scale-down model of {UO_NAME} holds the Protein A eluate in a {SDM_NAME}; the spiking model is the "
        f"same scale-down model.", [ref("sdm", q_sdm)])
    for name, row in prow.items():
        add("step:viral_inactivation", "step_has_parameter", PC[name],
            f"{UO_NAME} has process parameter {name}, classified {pdf_.loc[name, 'Class']}, studied "
            f"{pdf_.loc[name, 'Study']}ly.", [ref("factors", row, pt_t, prow)])
    role = {"lrv_xmulv": "contributes one of the three claims that meet the cumulative requirement for {n}",
            "aggregates_hmw": "can add to {n}, which is formed in the production bioreactor and removed at cation "
                              "exchange",
            "fragments_lmw": "can add to {n}, which the register assigns to harvest and clarification",
            "acidic_variants": "can add to {n}, which is formed in the production bioreactor"}
    for key in ckeys:
        add("step:viral_inactivation", "step_has_quality_attribute", f"attr:{key}",
            f"{UO_NAME} " + role[key].format(n=names[key]) + "; the attribute is judged at the output of the "
            "step against an intermediate acceptance criterion.", [ref("cqa", crow[key], cq_t, crow)])
    for amv, row in appdrow.items():
        out_ = appd_df.loc[appd_df["Method validation"] == amv].iloc[0]
        key = {v: k for k, v in method_of.items()}[amv]
        add(f"attr:{key}", "attribute_measured_by_method", f"method:{amv}",
            f"{names[key]} is measured by {out_['Technique'][0].lower() + out_['Technique'][1:]} ({amv}) in the "
            f"{out_['Sample'][0].lower() + out_['Sample'][1:]}, reported as {out_['Reportable']}.",
            [ref("app_d", row, appd_t, appdrow)])
    fr_sec_row = next(r_ for r_ in mbsrow.values() if _cells(r_)[0] == "Fragments, LMW")
    add("attr:fragments_lmw", "attribute_measured_by_method", "method:AMV-3011",
        "Both designs measured fragments by SEC, before the method decision; those results are biased in this "
        "matrix and used for no decision, and the fragment results of the response-surface design that are judged "
        "are by nrCE-SDS on its retained samples.",
        [ref("analytics", fr_sec_row, mbs_t, mbsrow),
         ref("analytics", q("Both designs ran before the method decision and measured fragments by SEC."))])
    for key in ckeys:
        ic, cr = _cells(irow[key]), _cells(crrow[key])
        ia = iac_.loc[attr_resp[key]]
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{UO}_{key}_iac",
            f"At the low-pH viral inactivation step {names[key]} is judged against the Version 2.0 intermediate "
            f"acceptance criterion {_unmark(ic[-2])} ({ia['basis']}), derived from the drug substance criterion "
            f"{_unmark(ic[1])}; met across the NOR in force: {_unmark(cr[-1])}.",
            [ref("iac", irow[key], iac_t, irow), ref("criteria", crrow[key], cr_t, crrow)])

    # parameter effects: the coefficient rows of the selected models, and the sentences that state the effects
    # of the attributes with no adequate model and of the univariate parameter
    letter_of = D.factor_letters(UO)
    alpha = float(ns["ALPHA"])
    for resp, key in ((X_, "lrv_xmulv"), (A_, "aggregates_hmw")):
        tab, rows_, _df = coef[resp]
        for k in FAC:
            lt = letter_of[k]
            if lt not in rows_:
                continue
            c = _cells(rows_[lt])
            sig = c[4].startswith("<") or (_num(c[4]) or 1) < alpha
            add(PC[NAME[k]], "parameter_impacts_attribute" if sig else
                "parameter_does_not_significantly_impact_attribute", f"attr:{key}",
                f"{NAME[k]} ({lt}) on {names[key]}: coefficient {c[1]} in coded units, p {c[4]} in the selected "
                f"model, " + ("significant." if sig else "not significant."),
                [ref("rsm", rows_[lt], tab, rows_)])
    add(PC[NAME["ph"]], "parameter_does_not_significantly_impact_attribute", "attr:aggregates_hmw",
        "The model selection dropped the pH term of aggregate, so no prediction of aggregate in the report depends "
        "on pH; the screening effect of pH on aggregate was not significant.",
        [ref("rsm", q("The selection dropped the pH term, so every prediction of aggregate in this report comes from "
                      "a model in which pH does not appear.")),
         ref("screening", serow[(LAB[A_], "A")], se_t, serow)])
    q_acid_t = q("The acidic variants grow with the hold time and with nothing else, by `{python} fx(acid_per60)` "
                 "percentage points per 60 min.")
    add(PC[NAME["hold_time"]], "parameter_impacts_attribute", "attr:acidic_variants",
        t("The acidic variants grow with the hold time, by `{python} fx(acid_per60)` percentage points per 60 min; "
          "their model is not adequate (exact fit), so the attribute is judged on its measured results."),
        [ref("mech", q_acid_t)])
    q_noscatter = q("There is no scatter about those values and no dependence on pH or temperature.")
    for k in ("ph", "temperature"):
        add(PC[NAME[k]], "parameter_does_not_significantly_impact_attribute", "attr:acidic_variants",
            f"In the designs and the first concentration study the acidic variants took one value per hold time, "
            f"with no dependence on {NAME[k].lower() if k != 'ph' else 'inactivation pH'}.",
            [ref("centre", q_noscatter)])
    q_fr_t = q("S-VI-OFAT resolved an increase of `{python} fx(OF.loc[FR, \"slope_60\"], 3)` percentage points per "
               "60 min at the two pH values it compared (@sec-ofat), in the direction cleavage in the hinge region "
               "leads one to expect.")
    add(PC[NAME["hold_time"]], "parameter_impacts_attribute", "attr:fragments_lmw",
        t("Fragments grow with the hold time: S-VI-OFAT resolved an increase of "
          "`{python} fx(OF.loc[FR, \"slope_60\"], 3)` percentage points per 60 min "
          "(`{python} pv(OF.loc[FR, \"p_slope\"])`); the model of fragments is not adequate."),
        [ref("mech", q_fr_t), ref("ofat", oerow["fragments_lmw"], oe_t, oerow)])
    q_fr_no = q("Fragments have no adequate model, and S-VI-OFAT found no effect of pH on them at the two pH values "
                "it compared")
    add(PC[NAME["ph"]], "parameter_does_not_significantly_impact_attribute", "attr:fragments_lmw",
        "The report states that S-VI-OFAT found no effect of inactivation pH on fragments at the two pH values it "
        "compared; the selected model of fragments is not adequate (limit on overfitting) and sets no range.",
        [ref("mech", q_fr_no)])
    q_conc_qa = q("For aggregate and acidic variants no effect of the concentration was detected within the range "
                  "studied.")
    for key in ("aggregates_hmw", "acidic_variants"):
        add(PC[conc], "parameter_does_not_significantly_impact_attribute", f"attr:{key}",
            f"No effect of A-Mab concentration on {names[key]} was detected within the range studied, in S-VI-UNI "
            f"and S-VI-UNI2.", [ref("uni", q_conc_qa)])
    add(PC[conc], "parameter_does_not_significantly_impact_attribute", "attr:lrv_xmulv",
        t("No effect of A-Mab concentration on the XMuLV log reduction was detected in S-VI-UNI2 "
          "(`{python} pv(u2_p)`), but four runs bound it loosely: the 95 % confidence interval of the difference at "
          "the high end, `{python} fx(u2_x_lo)` to `{python} fx(u2_x_hi)` log10, reaches further on the side of a loss "
          "than the margin of the claim over the NOR."),
        [ref("uni", q("No effect of the concentration on the inactivation was detected, which is what the hold acting "
                      "on the envelope of the virus leads one to expect (@sec-prior).")),
         ref("uni", q("Four runs bound that effect loosely."))])

    # ==== report statements, grouped by the chapters of the report =========================================
    STS = []

    def clean(s):
        """A rendered span as statement text: the subscript run and the spaces of a cross-reference closed up."""
        s = re.sub(r"\blog 10\b", "log10", s)
        s = re.sub(r"\(\s+", "(", s)
        return re.sub(r"\s+([,.;:)])", r"\1", s)

    def st(sec, txt, refs):
        STS.append((SEC[sec][0], ReportStatement(
            statement_id=f"{DOC}-S{len(STS) + 1:03d}", statement_text=txt, confidence="high",
            review_status="accepted", source_references=refs)))

    def sq(sec, src, txt=None, extra=()):
        """A statement of one prose span: ``src`` is the .qmd source of the span, ``txt`` the statement where it
        is not the span itself, ``extra`` further ``(section, source)`` spans a paraphrase draws on."""
        st(sec, t(txt) if txt else clean(q(src)), [ref(sec, q(src))] + [ref(s_, q(x)) for s_, x in extra])

    def srow(sec, txt, row, tab=None, rows_=None, caption=None, label=None):
        """A statement of one rendered row."""
        st(sec, txt, [ref(sec, row, tab, rows_, caption=caption, label=label)])

    # -- Executive summary ----------------------------------------------------------------------------------
    sq("exec", "The drug substance requires a cumulative clearance of xenotropic murine leukemia virus (XMuLV) of at "
               "least `{python} fx(xmulv_req, 1)` log~10~, which three steps claim together, and the claim of this "
               "step is `{python} fx(claim)` log~10~ of it.")
    sq("exec", "The studies were run in a scale-down model of the step, qualified for aggregate and acidic variants, and "
               "in a small-scale spiking model, at the development site in `{python} SENDING_LOCATION`.")
    sq("exec", "Inactivation pH, hold time and temperature were studied in a screening design of `{python} n_scr` runs "
               "and a response-surface design of `{python} n_rsm` runs.")
    sq("exec", "A-Mab concentration was studied one factor at a time.")
    sq("exec", "These characterization studies ran from `{python} char_start` to `{python} char_end`.")
    sq("exec", "`{python} W(len(RE_STUDIES)).capitalize()` further studies were made from `{python} re_start` to "
               "`{python} re_end`, during the Version 2.0 re-analysis and after the results of the designs were "
               "known.",
       "`{python} W(len(RE_STUDIES)).capitalize()` further studies were made from `{python} re_start` to "
       "`{python} re_end`, during the Version 2.0 re-analysis and after the results of the designs were known, and "
       "are registered as discrepancies from the plan.",
       extra=[("exec", "They are registered as discrepancies from the plan (@sec-record).")])
    sq("exec", "At the normal operating ranges (NORs) against which the studies were planned, the XMuLV claim was not "
               "met.",
       "At the NORs against which the studies were planned the XMuLV claim was not met: the lowest mean predicted log "
       "reduction was `{python} fx(WC_Xc[\"predicted\"])` log10, at `{python} wu(\"ph\", g(WC_Xc[\"settings\"][\"ph\"]))`, "
       "`{python} wu(\"hold_time\", g(WC_Xc[\"settings\"][\"hold_time\"]))` and "
       "`{python} wu(\"temperature\", g(WC_Xc[\"settings\"][\"temperature\"]))`, against the claim of "
       "`{python} fx(claim)` log10.",
       extra=[("exec", "The lowest mean predicted log reduction was `{python} fx(WC_Xc[\"predicted\"])` log~10~, at "
                       "`{python} wu(\"ph\", g(WC_Xc[\"settings\"][\"ph\"]))`, "
                       "`{python} wu(\"hold_time\", g(WC_Xc[\"settings\"][\"hold_time\"]))` and "
                       "`{python} wu(\"temperature\", g(WC_Xc[\"settings\"][\"temperature\"]))`, against the claim of "
                       "`{python} fx(claim)` log~10~.")])
    sq("exec", "The pH set-point and NOR were therefore moved to `{python} sp_t[\"ph\"]` and `{python} nor_t[\"ph\"]`, "
               "the hold-time NOR was narrowed to `{python} nor_t[\"hold_time\"]` with its set-point at "
               "`{python} sp_t[\"hold_time\"]`, and the temperature NOR was narrowed to `{python} nor_t[\"temperature\"]`.")
    sq("exec", "Across the NOR in force the lowest mean predicted log reduction is `{python} fx(WC_X[\"predicted\"])` "
               "log~10~, so the claim is met there.")
    sq("exec", "Aggregate, fragments and acidic variants meet their intermediate acceptance criteria across the NOR in "
               "force.")
    sq("exec", "The upper limit of the 95 % prediction interval of a single batch of aggregate is at most "
               "`{python} fx(UPL_A)` % HMW at manufacturing scale, against `{python} fx(crit_agg)` %.")
    sq("exec", "Fragments and acidic variants have no adequate model and are judged on their measured results, "
               "`{python} fx(MEAS[FR].min())` to `{python} fx(MEAS[FR].max())` % and `{python} fx(MEAS[AC].min(), 1)` "
               "to `{python} fx(MEAS[AC].max(), 1)` % respectively.")
    sq("exec", "The `{python} n_acid_flat` acidic variant results of the designs and the first concentration study show "
               "no scatter at a given hold time, so no adequacy test can be applied to that output.")
    sq("exec", "The selected models of aggregate and of the XMuLV log reduction meet all four model-adequacy criteria "
               "of PCMP-001 §7.2.")
    sq("exec", "`{python} W(len(RI[A][\"over\"]) + len(RI[X][\"over\"])).capitalize()` runs carry a Cook's distance "
               "above the cut-off at which PCP-006 §7.1 calls for an examination.",
       extra=[("exec", "Each was deleted in turn, the model selected again on the remaining `{python} n_rsm - 1` runs "
                       "and the output judged over the NOR again.")])
    sq("exec", "Under every one of those models the NOR in force lies inside the proven acceptable range (PAR) of each "
               "factor, the claim is met over the NOR, aggregate keeps its margin to its criterion, the move of the "
               "pH NOR remains necessary, and inactivation pH stays a critical process parameter, hold time and "
               "temperature well-controlled critical process parameters and A-Mab concentration a general process "
               "parameter.")
    sq("exec", "With run `{python} INF5[\"run\"]` deleted the temperature term leaves the XMuLV model and the XMuLV "
               "ranges widen.")
    sq("exec", "Temperature raises aggregate by `{python} fx(agg_temp_lo, 3)` to `{python} fx(agg_temp_hi, 3)` "
               "percentage points in every model after a deletion.")
    sq("exec", "The PARs are `{python} wu(\"ph\", PARX[\"ph\"])`, `{python} wu(\"hold_time\", PARX[\"hold_time\"])` and "
               "`{python} wu(\"temperature\", PARX[\"temperature\"])`.",
       extra=[("exec", "One edge of each is the setting at which the mean predicted log reduction falls to the claim, "
                       "and the other is the end of the range studied.")])
    sq("exec", "The NOR in force lies `{python} fx(MARG[\"ph\"])` pH units inside the upper pH edge, "
               "`{python} g(MARG[\"hold_time\"])` min inside the lower hold-time edge and "
               "`{python} fx(MARG[\"temperature\"], 1)` °C inside the lower temperature edge, and "
               "`{python} fx(MARG_OTH[\"ph\"])` pH units, `{python} g(MARG_OTH[\"hold_time\"])` min and "
               "`{python} fx(MARG_OTH[\"temperature\"], 1)` °C inside the three edges that are ends of the range "
               "studied.")
    sq("exec", "For XMuLV clearance the concentration study bounds the effect loosely, with four runs, so the GPP class "
               "rests for that attribute on how the hold acts.")
    sq("exec", "Within the NOR as characterized the step adds at most `{python} fx(v_agg[\"predicted_nor_bound95\"])` "
               "percentage points of aggregate at the one-sided `{python} VB` % prediction bound of a single batch, "
               "against the platform value of `{python} fx(v_agg[\"assumed\"])`.")
    sq("exec", "That bound moved the aggregate criterion of the production bioreactor output from "
               "`{python} fx(brx_tight)` to `{python} fx(brx_final)` % HMW.")
    sq("exec", "At a hold of `{python} g(RNG[\"hold_time\"][1])` min, outside the NOR, the step added up to "
               "`{python} fx(v_agg[\"observed_edge\"])` points.")
    sq("exec", "At the new pH set-point aggregate and fragments showed no effect of pH.")
    sq("exec", "Acidic variants were `{python} fx(abs(OF.loc[AC, \"ph_effect\"]))` percentage points lower at "
               "`{python} sp_t[\"ph\"]` than at `{python} spc_t[\"ph\"]`, a significant difference after adjustment "
               "(`{python} pv(OF.loc[AC, \"p_ph_holm\"])`) that was already present before the hold began and that is "
               "`{python} fx(abs(OF.loc[AC, \"ph_effect\"]))` points against a criterion "
               "`{python} fx(acid_hi - acid_lo, 1)` points wide.")
    sq("exec", "Cation exchange cleared aggregate and fragments from that material as the criteria assume.")
    sq("exec", "At the low end of the pH PAR, with hold time and temperature at the upper ends of their NORs, product "
               "quality met every criterion of the step and cation exchange cleared aggregate as required.")
    sq("exec", "For fragments every run cleared more than the required clearance factor, but the lower confidence bound "
               "of the three runs fell below it, so the rule fixed before the runs was not met.",
       extra=[("exec", "That was accepted on its risk, on the grounds PD-006-03 records and @sec-wc gives.")])
    sq("exec", "The neutralized pool met its criteria after `{python} H_DAYS` days at `{python} join_and(H_TEMPS)`.")
    sq("exec", "The capability index (Cpk) of cumulative XMuLV clearance is "
               "`{python} fx(CAPD.loc[\"lrv_xmulv\", \"Cpk\"])`, which `{python} cpk_verdict(CAPD.loc[\"lrv_xmulv\", "
               "\"Cpk\"])`.")
    sq("exec", "Acidic variants have the lowest Cpk of the attributes this step changes, "
               "`{python} fx(CAPD.loc[\"acidic_variants\", \"Cpk\"])`, which "
               "`{python} cpk_verdict(CAPD.loc[\"acidic_variants\", \"Cpk\"])`.",
       extra=[("exec", "The lower end of the criterion limits it."),
              ("exec", "The low-pH hold raises acidic variants, so it moves them away from the limit that binds.")])
    sq("exec", "The record of execution holds `{python} W(n_dev)` study events.",
       extra=[("exec", "The runs of both events were retained in the analysis.")])
    sq("exec", "`{python} W(len(PDS)).capitalize()` discrepancies from the plan are registered, "
               "`{python} W(len(RE_STUDIES))` of them studies made during the re-analysis (@sec-record).")

    # -- Introduction: objectives (PCP-006 §2, read from the numbered list of the .qmd) and changes ------------
    src_all = _source()
    obj_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n## Objectives", 1)[1].split("\n## ", 1)[0], flags=re.M)
    if len(obj_list) != 6:
        raise ValueError(f"{DOC}: {len(obj_list)} numbered objectives under '## Objectives', the text says six")
    sq("objectives", "PCP-006 §2 set six objectives for the studies, and this report answers each of them.")
    for i, obj in enumerate(obj_list, 1):
        st("objectives", f"Objective {i} of PCP-006 §2: {clean(q(obj))}", [ref("objectives", q(obj))])
    sq("changes", "Version 1.0 of this report was approved on `{python} rev1_date(DOC)`.")
    sq("changes", "The investigation found that the criteria used to judge each step in the PAR analysis were in no "
                  "approved protocol and had been set after the data were seen (`{python} INV[\"id\"]` finding 1).")
    sq("changes", "Each output of the step is judged against the intermediate acceptance criterion that PCMP-001 "
                  "Version 2.0 derives for it, and PCP-006 §7.2 states (@sec-iac).",
       extra=[("changes", "The Version 1.0 limits were applied at analysis and appear in no approved plan "
                          "(`{python} INV[\"id\"]` finding 1).")])
    sq("changes", "The Version 2.0 aggregate criterion of `{python} fx(crit_agg)` % HMW is wider than the Version 1.0 "
                  "limit of `{python} fx(agg_v1)` % and stricter than its own a priori value of "
                  "`{python} fx(agg_apriori, 1)` %, because the verification of two later steps tightened it.",
       extra=[("changes", "Cation exchange cleared less aggregate within its NOR than the platform worst case assumed, "
                          "and ultrafiltration and diafiltration (UF/DF) raises aggregate within its NOR, where "
                          "PCMP-001 assumed no change (@sec-iac).")])
    sq("changes", "The XMuLV criterion of `{python} fx(claim)` log~10~ is the platform claim of the step and is "
                  "stricter than the Version 1.0 value of `{python} fx(xmulv_v1)` log~10~, which was the cumulative "
                  "requirement minus the nominal clearance of the other steps in this campaign.")
    sq("changes", "Fragments are now an output of the step.",
       "Fragments are now an output of the step, judged on results by nrCE-SDS following the method decision "
       "`{python} AMD[\"id\"]` of `{python} AMD[\"date\"]`.",
       extra=[("changes", "They are judged on results by non-reduced capillary electrophoresis with sodium dodecyl "
                          "sulfate (nrCE-SDS), following the method decision `{python} AMD[\"id\"]` of "
                          "`{python} AMD[\"date\"]`.")])
    sq("changes", "Size exclusion chromatography (SEC) reads fragments high in the Protein A eluate and in the "
                  "neutralized pool, because part of the host cell protein in those matrices elutes in its low "
                  "molecular weight window (`{python} INV[\"id\"]` finding 6).")
    sq("changes", "Every result judged against a criterion for aggregate or acidic variants is stated at manufacturing "
                  "scale, by subtracting the offset of the scale-down model for that output (@sec-sdm).")
    sq("changes", "Every response-surface output is analysed by model selection, as corrective action CA3 of "
                  "`{python} INV2[\"id\"]` requires (@sec-stats).",
       extra=[("changes", "PCP-006 §5.5 prescribed the full quadratic model, and the change is registered as the "
                          "model-selection discrepancy PD-006-04 (@sec-record).")])
    sq("changes", "Version 1.0 fitted the full quadratic model of every output and set ranges from all of them.")
    sq("changes", "XMuLV clearance is judged on the mean predicted log reduction at the least favourable combination of the NOR, "
                  "which is the worst case PCMP-001 §6.4 sets for viral clearance (@sec-stats).",
       extra=[("changes", "Version 1.0 judged it on a single batch, as it judged the quality attributes.")])
    sq("changes", "The pH set-point and NOR, the hold-time set-point and NOR, and the temperature NOR are changed by "
                  "this revision (F1, @sec-nor).",
       extra=[("changes", "The studies were planned against the Version 1.0 values and run around them.")])
    sq("changes", "The Version 1.0 record gave no execution dates, so the equipment tables of the package appeared to "
                  "cite expired calibrations (`{python} INV[\"id\"]` finding 5).")
    sq("changes", "Every departure from the plan is recorded as a discrepancy from the plan and every event of "
                  "execution as a study event.")
    sq("changes", "The Version 1.0 analysis found the hold-time PAR for aggregate to end at "
                  "`{python} g(_edges(V1_AGG_T)[1])` min, because it judged aggregate against a limit three times "
                  "stricter than the criterion now in force.",
       extra=[("changes", "Under the Version 2.0 criterion that PAR covers the whole range studied.")])
    sq("changes", "The Version 1.0 analysis also found XMuLV clearance acceptable across the whole NOR as "
                  "characterized, against its criterion of `{python} fx(xmulv_v1)` log~10~, with a pH PAR ending at pH "
                  "`{python} g(_edges(V1_X_PH)[1])`.")
    sq("changes", "Against the platform claim and on the selected model, no XMuLV PAR exists at the NOR as "
                  "characterized, because the lowest mean prediction at the former pH set-point of "
                  "`{python} spc_t[\"ph\"]` is already below the claim (@sec-nor).")
    sq("changes", "Version 1.0 drew it on the mean prediction of every output, and "
                  "`{python} fx(100 * DSV1[\"fraction\"], 1)` % of the region studied met its criteria, bounded by "
                  "aggregate.")
    sq("changes", "Version 2.0 draws it on both ends of the `{python} PI` % prediction interval of a single batch for a "
                  "quality attribute and on the mean prediction for viral clearance, and "
                  "`{python} fx(100 * DSG[\"fraction\"], 1)` % of the region studied meets the criteria, bounded by "
                  "XMuLV clearance (@sec-ds).")
    sq("changes", "Aggregate and acidic variants met their criteria across the NOR under both revisions.")

    # -- Prior knowledge and quality risk basis --------------------------------------------------------------
    sq("platform", "The low-pH hold belongs to the Novacyte downstream platform and was used to manufacture three "
                   "earlier humanized IgG1 antibodies, X-Mab, Y-Mab and Z-Mab.")
    sq("platform", "That history supplies the platform claim for XMuLV clearance and the largest increases in aggregate, "
                   "fragments and acidic variants the step has shown on the platform.")
    sq("platform", "A longer hold and a warmer hold were each expected to raise the log reduction, and the effect of the "
                   "hold time was expected to be larger at low pH.")
    sq("platform", "Time at low pH also adds acidic variants, through direct acid-catalysed hydrolysis of side-chain "
                   "amides, and a small amount of acid-catalysed cleavage in the hinge region, which adds fragments.")
    sq("platform", "The criteria also assume no change in host cell protein across the step.")
    sq("risk", "Inactivation pH, hold time and temperature were assigned to multivariate study.",
       extra=[("risk", "A design that varies the three together was therefore needed to estimate the clearance and "
                       "the aggregate at their combinations.")])
    sq("risk", "A-Mab concentration was assigned to univariate study.",
       extra=[("risk", "No effect of the antibody concentration on the inactivation of the virus was expected.")])

    # -- Materials and methods ------------------------------------------------------------------------------
    sq("sdm", "The parameters of the step do not depend on scale, so inactivation pH, hold time, temperature and "
              "A-Mab concentration were set to the same values as in manufacture, and the additions of acid and base "
              "were scaled with the volume of the pool.")
    sq("sdm", "Aggregate is `{python} fx(off_agg[\"offset\"])` percentage points higher in the scale-down model and "
              "acidic variants `{python} fx(off_acid[\"offset\"])` points higher, and neither interval excludes zero.")
    sq("sdm", "Every result of these two outputs is translated to manufacturing scale by subtracting the offset of that "
              "output before it is compared with a criterion.")
    sq("sdm", "The model is qualified for an output when the conclusion against its criterion over the NOR is the same "
              "with the offset at either end of its interval (PCMP-001 §7.1).")
    sq("sdm", "Both conclusions hold at all three values of the offset, so the model is qualified for aggregate and for "
              "acidic variants.")
    for key, row in offrow.items():
        c = _cells(row)
        srow("sdm", f"Scale-down model offset of {names[key]} (scale-down minus manufacturing scale): {c[5]}, "
                    f"{ns['OFFCI']} % confidence interval {c[6]}; conclusion over the NOR met with the offset at the "
                    f"low end, estimate and high end: {c[7]}; qualified: {c[8]}.", row, off_t, offrow)
    sq("sdm", "The highest single result of the designs is `{python} fx(MEAS[FR].max())` %, which leaves "
              "`{python} fx(fr_margin)` points to the criterion of `{python} fx(crit_frag)` %.")
    sq("sdm", "Virus cannot be introduced into the manufacturing process, so XMuLV clearance was measured in the "
              "spiking model of the step")
    sq("sdm", "The virus load of a sample is its titre multiplied by the volume of the pool, and the log reduction "
              "factor (LRF) is the difference between the log~10~ load at the start and the log~10~ load at the end.")
    sq("sdm", "The small-scale result therefore represents the manufacturing step at that concentration, provided the "
              "whole pool reaches the inactivation pH.")
    sq("operation", "In both designs the A-Mab concentration was set to its set-point of "
                    "`{python} sp_t[\"protein_conc\"]`.")
    sq("analytics", "From `{python} AMD[\"date\"]`, nrCE-SDS is the method for fragments wherever fragments are measured "
                    "(PCMP-001 §7.8).")
    sq("analytics", "SEC remains the method for aggregate, which is read in a window the host cell protein of these "
                    "matrices does not reach.")
    sq("analytics", "The retained samples of the response-surface design were tested by nrCE-SDS in the re-test study "
                    "S-VI-RET, from `{python} win(\"S-VI-RET\")`, and the fragment results of the designs are those "
                    "`{python} n_rsm` results.", extra=[])
    st("analytics", t("The re-test study S-VI-RET of the retained samples of the response-surface design ran from "
                      "`{python} win(\"S-VI-RET\")`."), [ref("uni_design", chrow["S-VI-RET"], ch_t, chrow)])
    sq("analytics", "Of the studies made during the re-analysis, `{python} join_and(FR_RE)` measured fragments by "
                    "nrCE-SDS, and `{python} join_and(FR_RE_NOT)` measured none.")
    sq("sampling", "The record of both designs holds an LRF and a result for aggregate, acidic variants and fragments in "
                   "the neutralized pool for every run, `{python} n_scr` screening runs and `{python} n_rsm` "
                   "response-surface runs.")
    sq("sampling", "The increase across the step that the verification of the platform worst cases needs is therefore "
                   "taken against the aggregate level of the load in the process model at set-point, "
                   "`{python} fx(FEED_AGG)` % HMW (@sec-verif).")
    sq("stats", "A model term is significant when its p-value is below α = `{python} g(ALPHA)`, the level PCMP-001 §6.2 "
                "sets.")
    sq("stats", "The response-surface model is the predictive model, and every prediction, every PAR, the design space "
                "and the verification of the platform worst cases come from it.")
    sq("stats", "This report selects the model of each output instead, as corrective action CA3 of "
                "`{python} INV2[\"id\"]`, adopted on `{python} ca3_date`, requires for every report of the campaign.")
    sq("stats", "Among all `{python} N_SUB` submodels of the full quadratic that keep strong hierarchy, an interaction "
                "only with both its main effects and a square only with its main effect, the one with the lowest AICc "
                "is taken.")
    sq("stats", "The selected model is judged against the four adequacy criteria of PCMP-001 §7.2.")
    sq("stats", "A model that reproduces its results exactly is never adequate.")
    sq("stats", "Each of them is therefore judged through the `{python} PI` % prediction interval of a single run, which "
                "stands for a single batch, at every combination of NOR low, set-point and NOR high of the three "
                "factors, with the offset of the scale-down model applied.")
    sq("stats", "XMuLV clearance is judged on the mean predicted LRF at the least favourable of those combinations.")
    sq("stats", "One analysis of this report is in no plan.",
       "One analysis of the report is in no plan: where another model lies within 2 AICc units of the selected one, "
       "that model was fitted and its conclusions compared with those of the selected model, which decides; the "
       "comparison is registered within PD-006-04.",
       extra=[("stats", "Where another model lies within 2 AICc units of the selected one, that model was fitted and "
                        "its conclusions compared with those of the selected model, which decides.")])

    # -- Study design ---------------------------------------------------------------------------------------
    sq("factors", "The range studied is the characterized range of PCMP-001 and bounds the knowledge space within which "
                  "a PAR can be claimed.")
    sq("factors", "It lies away from the set-points the studies were run around")
    sq("factors", "The centre points therefore estimate pure error at the design centre, and each model predicts the "
                  "outputs at the set-point from the fitted surface rather than measuring them there.")
    sq("rsm_design", "PCP-006 §6.2 carried every factor with a detected effect into this design, and the screening had "
                     "detected an effect of each of the three on XMuLV clearance (@sec-screening).")
    sq("uni_design", "A study of one factor at a time cannot show whether the effect of the concentration depends on the "
                     "other parameters, and the designs, which held the concentration at its set-point, carry no "
                     "information on a concentration effect.")
    sq("uni_design", "Every characterization study closed before Version 1.0 of this report was approved on "
                     "`{python} rev1_date(DOC)`, and the first of them started after PCP-006 Version 1.0 was approved "
                     "on `{python} PLAN_APPROVAL[\"PCP-006\"]`.")
    sq("uni_design", "The set-points and NORs of this revision were decided on the results of the designs.",
       extra=[("uni_design", "The hold at the new pH set-point, S-VI-OFAT, and the cation exchange verification runs "
                             "tested that set-point after it had been decided, and the confirmation runs were made "
                             "after the hold-time NOR had been revised (@sec-nor).")])

    # -- Results --------------------------------------------------------------------------------------------
    sq("centre", "The XMuLV log reduction is the least precise response.")
    sq("centre", "The acidic variants gave the same result at every centre point of both designs, so their coefficient "
                 "of variation is zero.")
    sq("centre", "The consequence for the analysis is that no adequacy test can be applied to the model of this output "
                 "(@sec-rsm).")
    sq("centre", "The centre-point mean of the XMuLV log reduction was `{python} fx(d_centre)` log~10~ higher in the "
                 "screening design than in the response-surface design, which is "
                 "`{python} fx(d_centre / sd_pe_x, 1)` times the pure-error standard deviation of "
                 "`{python} fx(sd_pe_x)` log~10~ at the design centre.")
    sq("screening", "Each of the three factors changed the XMuLV log reduction.",
       extra=[("screening", "No interaction reached significance.")])
    sq("screening", "All three factors were therefore carried into the response-surface design, as PCP-006 §6.2 planned "
                    "for a factor with a detected effect.")
    sq("screening", "Aggregate responded to hold time and temperature.")
    sq("screening", "The effect of pH was `{python} fx(SE[A].loc[\"A\", \"Effect\"], 3)` points and did not reach "
                    "significance (`{python} pv(SE[A].loc[\"A\", \"p-value\"])`), and no interaction did either.")
    sq("screening", "The acidic variants gave an effect of hold time alone, of "
                    "`{python} fx(SE_AC.loc[\"B\", \"Effect\"], 1)` percentage points over the range studied, and no "
                    "residual scatter, so the fit statistics of that model carry no information (@tbl-screen-fit).")
    sq("screening", "The pH effect was therefore larger in the screening design than in the response-surface design, "
                    "`{python} fx(abs(_cmp[\"ph\"][\"scr\"]))` against `{python} fx(abs(_cmp[\"ph\"][\"rsm\"]))` "
                    "log~10~, and the difference is significant when the two estimates are compared against their "
                    "standard errors (`{python} pv(_cmp[\"ph\"][\"p\"])`).")
    sq("screening", "The response-surface model is the predictive model of this report, and it gives the smaller pH "
                    "effect, so the design space and the ranges rest on the smaller estimate.")
    sq("rsm", "The Box-Cox profile chose the raw scale for every output that has one.")
    sq("rsm", "On the full quadratic model of the planned runs the pH effect lies between `{python} fx(agg_ph_lo, 3)` and "
              "`{python} fx(agg_ph_hi, 3)` percentage points over the whole range studied, so these data bound a "
              "linear effect of pH on aggregate within about `{python} fx(max(abs(agg_ph_lo), abs(agg_ph_hi)), 2)` "
              "points.")
    sq("rsm", "Acidic variants and fragments have no adequate model.")
    sq("rsm", "Both selected models meet the criterion on residuals and influential runs, the fourth of PCMP-001 §7.2.")
    sq("rsm", "No run dominates either fit.",
       "No run dominates either fit: the largest Cook's distance is `{python} fx(RI[A][\"cook_max\"])` at run "
       "`{python} RI[A][\"cook_run\"]` for aggregate and `{python} fx(RI[X][\"cook_max\"])` at run "
       "`{python} RI[X][\"cook_run\"]` for the XMuLV log reduction, against F limits of "
       "`{python} fx(RI[A][\"f_limit\"])` and `{python} fx(RI[X][\"f_limit\"])`.",
       extra=[("rsm", "The largest Cook's distance is `{python} fx(RI[A][\"cook_max\"])` at run "
                      "`{python} RI[A][\"cook_run\"]` for aggregate and `{python} fx(RI[X][\"cook_max\"])` at run "
                      "`{python} RI[X][\"cook_run\"]` for the XMuLV log reduction, so neither model fails.")])
    sq("near", "For three outputs another model lies within 2 AICc units of the selected one.")
    for i, row in nearrow.items():
        r_ = near_df.iloc[i]
        out_lab = near_df["Output"].iloc[i]
        first = i == 0 or out_lab != near_df["Output"].iloc[i - 1]      # the selected model opens each output
        srow("near", f"{out_lab}: " + ("the selected model" if first else f"a model {r_['ΔAICc']} AICc units above "
                                                                         f"the selected one")
             + f" carries {r_['Terms']}; R² minus predicted R² {r_['R² minus predicted R²']}; all four criteria: "
               f"{r_['All four criteria']}; judgement over the NOR in force: {r_['Judgement over the NOR']}; met: "
               f"{r_['Met']}.", row, near_t, nearrow)
    sq("near", "For fragments the four models within 2 units disagree about the form of the surface.")
    sq("influence", "Every flagged run lies inside the range studied, and none was excluded from the analysis the rest "
                    "of this report uses.")
    for i, row in infrow.items():
        r_ = inf_df.iloc[i]
        out_lab = next(inf_df["Output"].iloc[j] for j in range(i, -1, -1) if inf_df["Output"].iloc[j])
        cook_ = r_["Cook's distance"]
        srow("influence", f"{out_lab}: with run {r_['Run deleted']} (Cook's distance {cook_}) "
                          f"deleted, the model selected carries {r_['Terms of the model then selected']}; first three "
                          f"criteria: {r_['First three criteria']}; judgement over the NOR in force: "
                          f"{r_['Judgement over the NOR in force']}; PARs: {r_['PARs']}.", row, inf_t, infrow)
    sq("influence", "Four conclusions of this report hold under every deletion.")
    sq("influence", "Two results of the XMuLV model do depend on run `{python} INF5[\"run\"]`.",
       extra=[("influence", "The PAR of each factor widens when the run is deleted.")])
    sq("influence", "The deletion of run `{python} INF4[\"run\"]` keeps all three terms and moves the PARs little.")
    sq("influence", "Over the NOR as characterized the claim fails under both deleted models as it does under the "
                    "selected model, at `{python} fx(INF[X][0][\"value_char\"])` and "
                    "`{python} fx(INF[X][1][\"value_char\"])` log~10~ against `{python} fx(WC_Xc[\"predicted\"])` "
                    "log~10~, so the decision to move the NOR does not rest on one run.")
    sq("mech", "The surface the data give is a plane in the three factors.")
    sq("mech", "The first-order description does not explain the plane, and the surface reported here is what the data "
               "give over the range studied.")
    sq("mech", "That is why the claim is most exposed to the inactivation pH (@sec-class).")
    sq("mech", "Within the NOR as characterized the predicted rise across the step is "
               "`{python} fx(v_agg[\"predicted_nor\"])` percentage points, with a single-batch bound of "
               "`{python} fx(v_agg[\"predicted_nor_bound95\"])` points (@sec-verif).")

    # -- Design space ------------------------------------------------------------------------------------------
    sq("ds", "The region is therefore bounded by the clearance claim and not by product quality, and its boundary is "
             "the contour drawn in @fig-xmulv.")
    sq("ds", "Judging both outputs on their mean predictions gives the same region, because aggregate stays far from its "
             "criterion at every point of the grid, so the choice of statistic does not move this boundary.")
    sq("ds", "Movement within the design space is not a change from a regulatory filing perspective, as ICH Q8(R2) "
             "states, and is assessed under the quality system of ICH Q10")
    sq("ds", "A move outside the NOR but inside the design space needs a prospective risk assessment under that system.")
    sq("ds", "The boundary is drawn on the mean predicted log reduction, so at the boundary itself a single batch falls "
             "below the claim about half the time, and the step is operated at the set-point with the margin @sec-nor "
             "states.")

    # -- Proven acceptable ranges: the acceptance basis, the outputs against their criteria, the hold ---------
    sq("iac", "No margin is applied.")
    sq("iac", "Within its NOR, cation exchange cleared less aggregate than its platform worst case, so the one-sided "
              "`{python} VB` % prediction bound of a single cation exchange batch, a clearance factor of "
              "`{python} fx(cex_fold_agg)`, replaced the platform value.")
    sq("iac", "UF/DF raises it within its NOR, so the one-sided `{python} VB` % prediction bound of a single UF/DF "
              "batch, a rise of `{python} fx(ufdf_agg, 3)` percentage points, is taken off the drug substance criterion.",
       "PCMP-001 assumed that no step after cation exchange changes aggregate. UF/DF raises it within its NOR, so the "
       "one-sided `{python} VB` % prediction bound of a single UF/DF batch, a rise of `{python} fx(ufdf_agg, 3)` "
       "percentage points, is taken off the drug substance criterion before it is carried back through cation exchange.",
       extra=[("iac", "PCMP-001 assumed that no step after cation exchange changes aggregate.")])
    sq("iac", "Together the two changes tightened the a priori criterion of `{python} fx(agg_apriori, 1)` % to the value "
              "in @tbl-iac.")
    sq("iac", "The criteria were derived after the studies ran, in PCMP-001 Version 2.0.",
       extra=[("iac", "That is acceptable because the derivation uses no result of the studies it judges.")])
    sq("criteria", "Every output meets its criterion.")
    sq("criteria", "The XMuLV log reduction is predicted at `{python} fx(X_SP)` log~10~ at the set-point.")
    sq("criteria", "The claim of `{python} fx(claim)` log~10~ is met there, with "
                   "`{python} fx(WC_X[\"predicted\"] - claim)` log~10~ to spare.")
    sq("criteria", "Of the `{python} len(MEAS[X])` individual results of the designs, `{python} x_below` lie below the "
                   "claim.")
    sq("hold", "PCP-006 planned no hold study, and Version 1.0 of this report had no hold result.")
    sq("hold", "PCP-006 sets no hold criterion.")
    sq("hold", "No plan sets that approach, and it was chosen after the hold results were known, which PD-006-05 "
               "records (@sec-record).")
    sq("hold", "Added to the `{python} fx(UPL_A)` % expected to enter the hold it gives `{python} fx(h_agg)` %, against "
               "the criterion of `{python} fx(crit_agg)` %.")
    sq("hold", "The upper limits for aggregate and fragments are met, and so are both ends of the acidic variant "
               "criterion.")
    sq("hold", "The record gives no reason for the difference.")

    # -- Proven acceptable ranges: the ranges as the report states them (the two analyses of PCMP-001 §6.4) -----
    sq("par", "The first analysis scans the factor across its range studied and compares the mean prediction with the criterion.")
    sq("par", "The second analysis is the one that supports a claim, because the range must hold while the rest of the "
              "operating point moves within its NOR.")
    q_fig_x, q_fig_a = fig_cap("fig-par-xmulv", 2), fig_cap("fig-par-agg", 2)
    st("par", "Figure caption: the left panel of the proven acceptable range of the inactivation pH for the XMuLV log "
              "reduction shows the mean prediction with the other two factors fixed, the right panel the median and the "
              "range of mean predictions over the NOR combinations of hold time and temperature.",
       [ref("par", q_fig_x, caption=None, label="fig-par-xmulv")])
    st("par", "Figure caption: the left panel of the proven acceptable range of the hold time for aggregate shows the "
              "mean prediction with the other two factors fixed, the right panel the median and the 95 % prediction "
              "interval of a single batch with pH and temperature varying within their NORs.",
       [ref("par", q_fig_a, caption=None, label="fig-par-agg")])
    sq("par", "The upper pH edge and the lower hold-time and temperature edges are where the mean predicted log "
              "reduction falls to the claim.")
    sq("par", "The other three edges are the ends of the ranges studied, so they are where the study stopped and not "
              "where the criterion fails.")
    sq("par", "The range carried into the control strategy is therefore the XMuLV range of each factor.")
    sq("par", "The ranges above and the design space of @sec-ds are two views of the same models.")

    # -- Proven acceptable ranges: the set-points and NORs in force and the three decisions --------------------
    sq("nor", "The studies were planned against the set-points and NORs of PCP-006 Version 1.0 and run around them.",
       extra=[("nor", "Against those values the XMuLV claim was not met.")])
    sq("nor", "Three decisions produced the values in force, each taken after the results of the designs were known.")
    sq("nor", "The hold-time NOR was narrowed to begin at the former set-point of `{python} spc_t[\"hold_time\"]`, giving "
              "`{python} wu(\"hold_time\", rg(ST1_NOR[\"hold_time\"][0], ST1_NOR[\"hold_time\"][1]))`, and the "
              "temperature NOR to `{python} nor_t[\"temperature\"]`.",
       "Decision 1: the hold-time NOR was narrowed to begin at the former set-point of `{python} spc_t[\"hold_time\"]`, "
       "giving `{python} wu(\"hold_time\", rg(ST1_NOR[\"hold_time\"][0], ST1_NOR[\"hold_time\"][1]))`, and the "
       "temperature NOR to `{python} nor_t[\"temperature\"]`; the model then put the pH at which the claim is lost at "
       "`{python} fx(ST_EDGE[1])`.",
       extra=[("nor", "With those ranges the model puts the pH at which the claim is lost at "
                      "`{python} fx(ST_EDGE[1])`.")])
    sq("nor", "The pH set-point was moved to `{python} sp_t[\"ph\"]` and the pH NOR to `{python} nor_t[\"ph\"]`, and the "
              "hold-time set-point to `{python} wu(\"hold_time\", g(ST2_SP[\"hold_time\"]))`, the middle of the "
              "hold-time NOR of the first decision.",
       "Decision 2: the pH set-point was moved to `{python} sp_t[\"ph\"]` and the pH NOR to `{python} nor_t[\"ph\"]`, "
       "and the hold-time set-point to `{python} wu(\"hold_time\", g(ST2_SP[\"hold_time\"]))`; the width of the pH NOR "
       "was kept and the range placed at the acid end of the NOR as characterized, leaving a margin of "
       "`{python} fx(ST_MARG2)` pH units to the pH at which the claim is lost.",
       extra=[("nor", "The upper pH NOR edge of `{python} wu(\"ph\", g(NOR[\"ph\"][1]))` then had a margin of "
                      "`{python} fx(ST_MARG2)` pH units to the pH at which the claim is lost.")])
    sq("nor", "Two studies support the new pH set-point, a hold of the pool at it against the former set-point "
              "(@sec-ofat) and cation exchange runs on material inactivated at it (@sec-cex).")
    sq("nor", "No plan sets a minimum margin, so the size that is enough is a judgement of this report.",
       "Decision 3: no plan sets a minimum margin; on the judgement of the report a margin of `{python} fx(ST_MARG2)` pH "
       "units was not accepted, and the hold-time NOR was narrowed again, to `{python} nor_t[\"hold_time\"]`, with its "
       "set-point at `{python} sp_t[\"hold_time\"]`, which puts the pH at which the claim is lost at "
       "`{python} fx(ST_EDGE[3])`, a margin of `{python} fx(ST_MARG3)` pH units from the upper pH NOR edge.",
       extra=[("nor", "With the ranges in force the model puts the pH at which the claim is lost at "
                      "`{python} fx(ST_EDGE[3])`, a margin of `{python} fx(ST_MARG3)` pH units from the upper pH NOR "
                      "edge, which was accepted.")])
    sq("nor", "Each pH is computed from the selected model at the shortest hold and the coolest temperature of the NOR "
              "of that stage.")
    for name, row in ncrow.items():
        c, k = _cells(row), pkey[name]
        srow("nor", f"{name}: set-point as characterized {wu(k, c[2])} and NOR as characterized {wu(k, c[3])}; "
                    f"set-point in force {wu(k, c[4])} and NOR in force {wu(k, c[5])} ({c[6]}).", row, nc_t, ncrow)
    for name, row in mgrow.items():
        c, k = _cells(row), pkey[name]
        mu = "pH units" if c[1] == "pH" else c[1]
        srow("nor", f"{name}: the NOR in force, {wu(k, c[2])}, lies inside the XMuLV PAR of {wu(k, c[3])}; the "
                    f"{c[4]} edge of the PAR binds, with a margin of {c[5]} {mu} to the NOR edge and {c[6]} {mu} to "
                    f"the set-point.", row, mg_t, mgrow)
    sq("nor", "The edge of the pH NOR that binds carries a margin of `{python} fx(MARG[\"ph\"])` pH units and the "
              "set-point `{python} fx(MARG_SP[\"ph\"])` pH units, both above the `{python} fx(nor_half_ph)` pH units "
              "of the judgement above.")
    sq("nor", "These changes are changes to the control strategy of the step.",
       extra=[("nor", "They were decided on the data of the studies reported here, which means the ranges in force were "
                      "chosen after the results were seen, and the confirmation runs of @sec-wc were made for that "
                      "reason.")])
    sq("nor", "The comparisons with the platform worst cases (@sec-verif) and with Version 1.0 use the NOR and "
              "set-points as characterized, which the studies were planned against, so that no change of a NOR moves a "
              "criterion or a Version 1.0 number.")

    # -- the study at the new pH set-point (S-VI-OFAT, PD-006-01) ---------------------------------------------
    sq("ofat", "PCP-006 planned no study at the Version 2.0 set-points.")
    sq("ofat", "The interaction was tested separately, and the three pH p-values were adjusted by Holm's method, because "
               "three attributes were tested.")
    for key, row in oerow.items():
        c = _cells(row)
        srow("ofat", f"S-VI-OFAT, {names[key]}, measured by {c[1]}: mean {c[2]} at the new pH set-point and {c[3]} at "
                     f"the former one; difference {c[4]}, p {c[5]}; pH × hold time p {c[6]}; change per 60 min {c[7]}; method "
                     f"repeatability SD {c[8]}; results at the new set-point {c[9]}, criterion of the step {c[10]}.",
             row, oe_t, oerow)
    sq("ofat", "Neither reached significance after adjustment, and each interval is narrow against the margin of the "
               "attribute to its criterion.")
    sq("ofat", "Three features place it before the hold rather than in it.",
       "The acidic variant difference at the new pH set-point is placed before the hold rather than in it: it was "
       "already present at time 0, it did not grow with hold time, and the response-surface model of the attribute "
       "carries no pH term.",
       extra=[("ofat", "The difference was already `{python} fx(abs(OF.loc[AC, \"diff_t0\"]))` points at time 0, in the "
                       "pH-adjusted load before any hold, where a hold effect cannot yet have acted."),
              ("ofat", "It did not grow with hold time (`{python} pv(OF.loc[AC, \"p_interaction\"])`), and a reaction "
                       "driven by the hold pH would.")])
    sq("ofat", "No plan sets a size at which a significant difference of this attribute would matter, so calling this "
               "one small against its criterion is a judgement of this report.")
    sq("ofat", "Every result at the new pH set-point meets the criterion of its attribute.")

    # -- the cation exchange verification runs (S-CEX-VER, PD-006-02) -------------------------------------------
    cvr = {_unmark(_cells(r_)[0]): r_ for r_ in cvrow.values()}
    wcr = {_unmark(_cells(r_)[0]): r_ for r_ in wcrow.values()}
    st("cex", t("Study S-CEX-VER, cation exchange runs on material at the new pH set-point, ran from "
                "`{python} win(\"S-CEX-VER\")` and is registered as PD-006-02."),
       [ref("uni_design", chrow["S-CEX-VER"], ch_t, chrow), pdref("PD-006-02")])
    sq("cex", "PCP-006 planned no downstream verification.")
    sq("cex", "The number of runs was fixed before the runs were made, by the simulation in @tbl-cex-verification-n.",
       extra=[("cex", "A verification passes when the one-sided `{python} VB` % lower confidence bound of the mean log "
                      "reduction value of the runs reaches the clearance factor the criteria rely on.")])
    sq("cex", "The larger of the two needs decided the study, so `{python} cv_n` runs were made.")
    for row in cvnrow.values():
        c = _cells(row)
        if c[0]:                                     # the first row of each attribute carries its inputs
            srow("cex", f"S-CEX-VER run count, {c[0].lower()}: clearance factor {c[1]} in the cation exchange data "
                        f"against {c[2]} that the criteria rely on, standard deviation of the log fold {c[3]}; "
                        f"runs needed {_unmark(c[7])}.", row, cvn_t, cvnrow)
    for lab_ in ("Geometric mean fold", "Lower 95 % confidence bound", "Result"):
        c = _cells(cvr[lab_])
        srow("cex", f"S-CEX-VER, {lab_.lower()}: aggregate {c[3]}, fragments {c[6]}.", cvr[lab_], cv_t, cvrow)
    sq("cex", "Both attributes passed.", extra=[("cex", "Every run cleared more than the required factor for both "
                                                        "attributes.")])
    sq("cex", "The cation exchange pool also met the criteria of that step, at most "
              "`{python} fx(CV.loc[\"aggregates_hmw\", \"pool_max\"])` % HMW against `{python} fx(cex_crit_agg)` % and "
              "`{python} fx(CV.loc[\"fragments_lmw\", \"pool_max\"])` % fragments against `{python} fx(cex_crit_frag)` "
              "%.")
    sq("cex", "The material from the step at its new pH set-point therefore behaves at cation exchange as the criteria "
              "of this step assume.")

    # -- the confirmation runs at the low end of the pH PAR (S-VI-WC, PD-006-03) --------------------------------
    st("wc", t("Study S-VI-WC, confirmation runs at the low end of the pH PAR with hold time and temperature at the "
               "upper ends of their NORs, ran from `{python} win(\"S-VI-WC\")` and is registered as PD-006-03."),
       [ref("uni_design", chrow["S-VI-WC"], ch_t, chrow), pdref("PD-006-03")])
    sq("wc", "PCP-006 planned no study at the Version 2.0 NOR.")
    sq("wc", "Product quality met every criterion of the step.")
    for lab_ in ("Geometric mean fold", "Lower 95 % confidence bound", "Result"):
        c = _cells(wcr[lab_])
        srow("wc", f"S-VI-WC, {lab_.lower()}: aggregate {c[3]}, fragments {c[6]}.", wcr[lab_], wc_t, wcrow)
    sq("wc", "For aggregate the rule is met.")
    sq("wc", "For fragments the rule is not met.")
    sq("wc", "The three runs are not pooled with the `{python} cv_n` runs of S-CEX-VER, which were made on different "
             "material, and no rule of the analysis was changed once the result was known.")
    sq("wc", "The failure was accepted on its risk, and PD-006-03 records the grounds.",
       extra=[("wc", "The risk of a lower fragment clearance at cation exchange therefore falls on the producer and not "
                     "on the patient."),
              ("wc", "Fragments are tested by nrCE-SDS at release, so an excursion would be detected on the drug "
                     "substance itself.")])
    sq("wc", "No criterion of this report rests on the failed bound.")
    sq("wc", "The acceptance was decided after the result was known.")

    # -- A-Mab concentration ------------------------------------------------------------------------------------
    sq("uni", "Both intervals contain zero, and both are narrow against the margin of "
              "`{python} fx(crit_agg - UPL_A)` points between the highest single-batch prediction over the NOR and the "
              "criterion.")
    sq("uni", "The range `{python} wu(\"protein_conc\", rg(conc_lo, conc_hi))` is therefore supported for these two "
              "attributes.")
    sq("uni", "For XMuLV clearance the class of the parameter therefore rests on how the hold acts (@sec-class).")
    sq("uni", "Of the four, `{python} u2_n_below` lie below the claim of `{python} fx(claim)` log~10~.")

    # -- Verification of the platform worst cases, and the widened aggregate criterion ---------------------------
    sq("verif", "Each assumption was checked on the response-surface models of this step, as PCMP-001 §7.5 requires.")
    cur = None
    for key, row in verrow.items():
        c = _cells(row)
        srow("verif", f"Platform worst case of the step for {names[key]} (largest increase, points): platform "
                      f"{c[3]}; this campaign at the edges of the range studied {c[4]}, within the NOR as "
                      f"characterized {c[5]}, one-sided 95 % bound of a single batch {c[6]}; outcome "
                      f"{_unmark(c[7])}.", row, ver_t, verrow)
    sq("verif", "Only aggregate moved a criterion.")
    sq("verif", "The bound is better than the platform value, and the selected model of aggregate meets every adequacy "
                "criterion of PCMP-001 §7.2.")
    sq("verif", "PCP-006 §7.4 also asks whether the bound depends on a single run.",
       "The bound does not depend on a single run: with each run that PCP-006 §7.1 flags deleted in turn it is at most "
       "`{python} fx(max(i_[\"bound\"] for i_ in INF[A]))` points, still below the platform value.",
       extra=[("verif", "With each run that PCP-006 §7.1 flags for examination deleted in turn, the bound is at most "
                        "`{python} fx(max(i_[\"bound\"] for i_ in INF[A]))` points, still below the platform value "
                        "(@sec-influence).")])
    sq("verif", "The bound therefore replaced the platform value, and the aggregate criteria of the steps upstream of "
                "this one were recalculated with it.")
    sq("verif", "The criterion affected is the aggregate criterion of the production bioreactor output.",
       "The criterion affected is the aggregate criterion of the production bioreactor output: a priori "
       "`{python} fx(brx_apriori, 1)` % HMW, tightened by the cation exchange verification and the UF/DF allowance to "
       "`{python} fx(brx_tight)` "
       "% and widened by the bound of this step to `{python} fx(brx_final)` %.",
       extra=[("verif", "The cation exchange verification and the UF/DF allowance tightened it to "
                        "`{python} fx(brx_tight)` %, and the bound of this step then widened it to "
                        "`{python} fx(brx_final)` %, which is stricter than the a priori value and wider than the value "
                        "those two changes alone would give.")])
    sq("verif", "The platform values are increases over a hold of `{python} g(RNG[\"hold_time\"][1])` min, and the bound "
                "of this step is the increase within a NOR whose longest hold is `{python} g(NORc[\"hold_time\"][1])` "
                "min, so the replacement reflects the shorter hold of the A-Mab NOR and not a more stable product.")
    sq("verif", "The aggregate model carries no pH term, and the NOR in force ends at the same longest hold and warmest "
                "temperature as the NOR as characterized, so the same bound covers the NOR in force.")
    sq("verif", "The widened criterion is an intermediate criterion at the production bioreactor, and the drug substance "
                "criterion for aggregate is unchanged, so the risk of the change falls on the producer and not on the "
                "patient.")
    sq("verif", "What the downstream steps must clear is the factor the criteria already credit, the aggregate clearance "
                "of cation exchange, which @sec-cex verified on material from this step.")
    sq("verif", "Aggregate is tested against its drug substance criterion by SEC at release.")
    sq("verif", "The bound of a single batch is `{python} fx(v_frag[\"predicted_nor_bound95\"])` points, which is not "
                "better than the platform value, so no replacement follows and the platform value stands in the "
                "fragment criterion of the Protein A output.")
    sq("verif", "The bound still does not replace it, because the model of the attribute fits the results exactly and "
                "the adequacy criteria of PCMP-001 §7.2 cannot be applied to it (@sec-rsm).",
       extra=[("verif", "The acidic variant criteria upstream of this step therefore stay at their a priori values.")])

    # -- Process capability and robustness -----------------------------------------------------------------------
    sq("cap", "Capability at commercial scale comes from the integrated model of the train, which runs "
              "`{python} f\"{n_mc:,}\"` simulated batches through every step with each parameter drawn within its NOR "
              "in force (PCMP-001 §6.5).")
    sq("cap", "This step contributes the largest of the three claims (@sec-iac).")
    sq("cap", "PCMP-001 §7.9 calls a value between the two acceptable and asks for the side of the criterion that limits "
              "it and the parameters that drive it, which PCMR-001 consolidates.")
    sq("cap", "No simulated batch falls outside the drug substance criterion for aggregate or for fragments, so each of "
              "those probabilities is below `{python} fx(100 * poos_bound, 2)` % at one-sided 95 % confidence, a bound "
              "that covers the sampling of the simulation and not the uncertainty of the integrated model itself.")
    sq("cap", "For acidic variants `{python} int(POOS.loc[\"acidic_variants\", \"n_oos\"])` of "
              "`{python} f\"{n_mc:,}\"` batches falls below the lower limit, and the tail probability of a normal "
              "distribution with the simulated mean and standard deviation is "
              "`{python} fx(100 * float(POOS.loc[\"acidic_variants\", \"p_oos_normal\"]), 2)` %.")
    sq("cap", "Three results bound the robustness of the step.")

    # -- Parameter classification -------------------------------------------------------------------------------
    sq("class", "Each parameter was classified under SOP-4001 by the decision logic of PCMP-001 §7.7.")
    sq("class", "Neither PCMP-001 nor SOP-4001 sets a numerical threshold for an effect that is practically relevant or "
                "for a PAR that is wide against its NOR.")
    sq("class", "The step therefore carries one CPP and two WC-CPPs.",
       extra=[("class", "A WC-CPP is a critical process parameter with good control capability, so all three are "
                        "critical and all three are controlled within the limits of the design space.")])

    # -- Contribution to the control strategy -------------------------------------------------------------------
    sq("cs", "The step contributes four things to the control strategy of the drug substance process, and PCMR-001 "
             "consolidates them with the other steps.")
    sq("cs", "*The claim and the ranges that assure it.* The step claims `{python} fx(claim)` log~10~ of XMuLV clearance, "
             "which it meets across the NOR in force at the least favourable combination (@sec-criteria).")
    sq("cs", "The set-points are `{python} sp_t[\"ph\"]`, `{python} sp_t[\"hold_time\"]` and "
             "`{python} sp_t[\"temperature\"]`.")
    sq("cs", "*Monitoring and testing.* XMuLV clearance cannot be measured in manufacture, so the claim rests on keeping "
             "inactivation pH, hold time and temperature within their NORs on every batch.")
    sq("cs", "*What this step hands to the next.* The neutralized pool is the load of cation exchange, which removes the "
             "aggregate the hold forms.")
    sq("cs", "The criteria of this step credit cation exchange with a clearance factor of `{python} fx(cex_fold_agg)` for "
             "aggregate and `{python} fx(cex_fold_frag)` for fragments, and @sec-cex verified both on material from "
             "the step at its new pH set-point.")
    sq("cs", "One lifecycle control follows from the verification.",
       "One lifecycle control follows from the verification: a change that extended the hold-time or temperature NOR "
       "beyond `{python} wu(\"hold_time\", g(NORc[\"hold_time\"][1]))` or "
       "`{python} wu(\"temperature\", g(NORc[\"temperature\"][1]))` would take routine manufacture outside the basis of "
       "the widened aggregate criterion of the production bioreactor output, and is assessed under the change "
       "management system of ICH Q10.",
       extra=[("cs", "A change that extended the hold-time or temperature NOR of this step beyond those ends would take "
                     "routine manufacture outside the basis of that criterion, and is assessed under the change "
                     "management system of ICH Q10")])

    # -- Discussion -----------------------------------------------------------------------------------------------
    sq("disc", "The step is understood well enough to be operated and transferred.")
    sq("disc", "What limits the step is not product quality but the clearance claim, which is why the design space of "
               "@sec-ds is bounded by the clearance contour and why the ranges in force were set from it.")
    sq("disc", "The ranges in force were decided on these data, after the results were seen (@sec-nor).")
    sq("disc", "Six limitations bound what this report claims.")
    for src_ in ("*The log reduction carries the variability of a cell-based assay.* Its coefficient of variation at "
                 "the centre points is `{python} fx(CVR.loc[LAB[X], \"%CV\"], 1)` %, the largest of any response.",
                 "*Two results depend on one run.* Both selected models meet every adequacy criterion, and no "
                 "conclusion over the NOR changed when a flagged run was deleted (@sec-influence).",
                 "*Two outputs have no adequate model.* Acidic variants and fragments are judged on their measured "
                 "results and set no range (@sec-criteria).",
                 "*Three approaches were set after the results they judge.* The model selection of corrective action "
                 "CA3 was adopted on `{python} ca3_date`, after the designs had been analysed.",
                 "*The input pool of the designs was not tested.* The increase across the step that the verification "
                 "needs is taken against the aggregate level of the load in the process model at set-point rather than "
                 "against a measured load (PD-006-08)."):
        sq("disc", src_)

    # -- Conclusions (the numbered list of the .qmd) ----------------------------------------------------------
    con_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n# Conclusions", 1)[1].split("\n# ", 1)[0], flags=re.M)
    if len(con_list) != 8:
        raise ValueError(f"{DOC}: {len(con_list)} numbered conclusions, the report has eight")
    for i, con in enumerate(con_list, 1):
        st("concl", f"Conclusion {i}: {clean(q(con))}", [ref("concl", q(con))])

    # -- Study events and discrepancies from the plan -------------------------------------------------------------
    sq("record", "A process characterization study is not manufacture under GMP, so this report records the events of "
                 "execution as study events, under the numbers Version 1.0 gave them, and every departure from the plan "
                 "as a discrepancy from the plan.")
    sq("pds", "A discrepancy is any departure from the plan this report states results against, whether work the plan "
              "did not foresee or a requirement of the plan that was not met.")
    for pid, row in pdrow.items():
        d = PDS[pid]
        srow("pds", f"Discrepancy {pid} from PCP-006, {d['subject']}: planned {d['planned']}; done {d['done']}; "
                    f"reason {d['reason']}.", row, rows_=pdrow, caption=pd_cap, label="tbl-discrepancies")
    sq("pds", "The remaining two are requirements of the plan that were not met, `{python} PD_CONC` and "
              "`{python} PD_POOL`, and the two subsections below describe them.")
    sq("pds", "The aggregate criterion of the production bioreactor output is `{python} fx(brx_final)` % HMW with the "
              "selection and `{python} fx(brx_agg_noca3)` % without it, because the verification bound of the cation "
              "exchange aggregate clearance comes from the selected model of that step (@sec-verif).")
    sq("pds", "The aggregate criterion of this step is `{python} fx(crit_agg)` % with the selection and "
              "`{python} fx(agg_wo_ca3)` % without it, for the same reason.")
    sq("pds", "The acidic variant criterion of the production bioreactor output is `{python} fx(brx_acid_ca3, 1)` % with "
              "the selection and `{python} fx(brx_acid_noca3, 1)` % without it.")
    sq("pds", "The bound this step contributes is nearly the same under either model of aggregate, "
              "`{python} fx(v_agg[\"predicted_nor_bound95\"])` percentage points on the selected model and "
              "`{python} fx(bound_full)` points on the full quadratic.")
    sq("pds", "Every conclusion over the NOR, every proven acceptable range and both scale-down qualifications of this "
              "step are the same under the criteria the full quadratic models would have given.")
    sq("pd7", "The study measured aggregate and acidic variants only, because spiking had been scheduled for the designed "
              "studies alone and no titre was taken in the concentration study.")
    sq("pd7", "The departure was found when the plan was compared with the study record during the Version 2.0 "
              "re-analysis, and Version 1.0 of this report did not notice it.")
    sq("pd8", "No input pool result is in the record of either design, because the input samples were not scheduled in "
              "the study record.")
    sq("pd8", "Every criterion of the step is on the output of the step, so no judgement of an output against its "
              "criterion is affected, and every run was retained in the analysis.")

    sections = []
    for chap in CHAPTERS:
        stmts = [x for c_, x in STS if c_ == chap]
        if stmts:
            sections.append(ReportSection(section_id=f"{DOC}-sec{len(sections) + 1:02d}", title=chap,
                                          statements=stmts))
    if sum(len(s_.statements) for s_ in sections) != len(STS):
        raise ValueError(f"{DOC}: statements outside the chapters of the report")

    # ==== concepts ===========================================================================================
    concepts = [Concept(concept_id="step:viral_inactivation", concept_type="PROCESS_STEP", canonical_name=UO_NAME,
                        aliases=["low-pH viral inactivation", "low-pH hold", "viral inactivation",
                                 P.DOC_REGISTRY[DOC][1], f"Step {G.VISTEP}"],
                        review_status="human_verified")]
    alias = {"ph": ["pH"], "hold_time": ["hold"], "temperature": ["hold temperature"],
             "protein_conc": ["antibody concentration", "concentration"]}
    concepts += [Concept(concept_id=PC[NAME[k]], concept_type="PROCESS_PARAMETER", canonical_name=NAME[k],
                         aliases=alias[k], review_status="human_verified") for k in PK]
    concepts += G._attr_concepts(ckeys)
    amvs = [m.method_id for m in methods]
    concepts += G._method_concepts(amvs, amv_title)
    concepts.append(Concept(concept_id="equip:vi_sdm_vessel", concept_type="EQUIPMENT", canonical_name=SDM_NAME,
                            aliases=["scale-down model", "spiking model"], review_status="human_verified"))

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
            "ProcessParameter.target_value and NOR are the set-point and NOR in force, which this revision changed "
            "for inactivation pH (set-point and NOR), hold time (set-point and NOR) and temperature (NOR). The "
            "studies were planned and run against the set-points and NORs as characterized; each multivariate "
            "parameter also anchors on its row of the table of set-points and ranges as characterized and in force, "
            "and the three decisions that produced the values in force are report statements. ProcessParameter.PAR "
            "is the NOR-propagated XMuLV PAR of a multivariate parameter, the range carried into the control "
            "strategy, and the range studied for A-Mab concentration. rationale_for_criticality carries the "
            "classification argument of Section 9, each parameter anchored on its own sentences of it.",
            "The QualityAttribute records are the four attributes judged at the output of the step. "
            "acceptance_criteria holds the drug substance criterion of the CQA register and the Version 2.0 "
            "intermediate acceptance criterion of the step; acceptance_criteria (the annex layer) holds the rows of "
            "the criteria-change table, Version 1.0 superseded and Version 2.0 in force.",
            "proven_acceptable_ranges: the three rows of the PAR table (XMuLV clearance, from the selected model), "
            "with par_at_setpoint and par_nor_propagated as the columns 'PAR (set-point)' and 'PAR (NOR)' print "
            "them, and the three aggregate ranges the text states ('its PAR is the range studied in all three'), "
            "both analyses equal to the range studied in doe_report.par_table. Acidic variants and fragments set no "
            "PAR (an explicit non-claim). The report's description of the two analyses is recorded in its own "
            "words, in report statements anchored on the sentences and figure captions that give it.",
            "The schema has no record type for a discrepancy from the plan. PD-006-01 to PD-006-08 are report "
            "statements anchored on their rows of the discrepancy register, and the studies they add carry that "
            "row as a source reference.",
            "The report records no deviation: a characterization study is not GMP manufacture, so the two events of "
            "execution are study events, under the numbers Version 1.0 gave them (DEV-006-01, DEV-006-02). They are "
            "Deviation records, the schema's only record type for an event of execution. no_impact_on_conclusions "
            "is true for DEV-006-01, whose effect the report bounds below the margins of the claim and of the "
            "aggregate criterion, and false for DEV-006-02, of which the report says only that it can make a "
            "computed log reduction smaller and is one possible contributor to the larger pH effect of the "
            "screening design.",
            "Studies: every row of the execution-window table with a schema study type has a StudyDesign record. "
            "S-VI-OFAT (the new pH set-point against the former one, over hold times) is one_factor_at_a_time; the "
            "hold study S-VI-HLD has no hold study type and is recorded as univariate (hold time at two "
            "temperatures, factors that are not process parameters). S-CEX-VER and S-VI-WC (verification runs at "
            "one setting) and the nrCE-SDS re-test S-VI-RET have no schema study type and no study record; their "
            "windows, rules and results are report statements anchored on their rows. Only the two designs carry "
            "n_runs, which the corpus test reserves for the seeded DoE designs.",
            "StatisticalModelFit: the planned full quadratic of each output (the re-evaluation table), the selected "
            "models of aggregate and of the XMuLV log reduction (all four adequacy criteria met), the selected "
            "models of fragments (not adequate, limit on overfitting) and of acidic variants (exact fit, not "
            "adequate), and the three screening models. A p-value printed as '< 0.001' has no float value; its "
            "term carries significant=true.",
            "parameter_impacts_attribute and parameter_does_not_significantly_impact_attribute: for the two "
            "modelled outputs, one assertion per factor on its row of the coefficient table of the selected model; "
            "for acidic variants and fragments, which have no adequate model, and for A-Mab concentration, the "
            "sentences of the report that state the effect.",
            "The ModularContribution records the platform claim of the step against the cumulative XMuLV "
            "requirement; cumulative_value is the sum of the three platform claims the report states, not a "
            "measured clearance. The capability of cumulative XMuLV clearance is a property of the train.",
            "The widening of the aggregate criterion of the production bioreactor output by the verification bound "
            "of this step is carried by the rows of the worst-case verification table and the report statements of "
            "Section 7.7; the bioreactor criterion itself belongs to the annexes of PCR-003 and PCMP-001.",
            "The equipment id equip:vi_sdm_vessel follows the PCP-006 Version 2.0 annex (the Version 1.0 report "
            "used equip:vi_sdm).",
            "rhetorical_spans: authoring/rhetorical/PCR-006.spans.yaml, re-curated against the Version 2.0 text in "
            "the same pass as this builder. weak_claims is empty.",
        ] + G._unrendered_note(unrendered),
        inventory=G.rev2_inventory(DOC, FILE, "process_characterization_report", UO_NAME,
                                   ["process characterization", "low-pH viral inactivation", "viral clearance",
                                    "XMuLV log reduction", "intermediate acceptance criteria",
                                    "design of experiments", "model selection", "normal operating range revision",
                                    "scale-down model qualification", "hold study",
                                    "verification of platform worst cases", "parameter classification"]),
        entities=entities, studies=studies, design_spaces=design_spaces, proven_acceptable_ranges=pars,
        report_sections=sections, assertions=AssertionStore(run_id=f"gt-{DOC}", assertions=AS, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{DOC}", concepts=concepts),
        weak_claims=[], rhetorical_spans=G.build_rhetorical_spans(DOC, FILE),
        acceptance_criteria=G.acceptance_criteria_layer(DOC, FILE, title("changes"), ct["tbl-criteria-change"][0],
                                                        [UO]))
    _gate(annex, text)
    return annex
