"""PCR-009 Version 2.0, the characterization report of small virus retentive filtration (Step 9), re-analysed
under INV-001 and INV-002: its ground-truth annex (``build()``).

The kinds of record follow the Version 2.0 report builders with a designed experiment (``pcr_006.py``,
``pcr_003.py``) and the concept ids follow the Version 1.0 builder of this report (``build_report_vf``) and
the Version 2.0 builder of its plan (``pcp_009.py``): the inventory and the revision layer; the step, its
scale-down model and the two sites; the two parameters, with the class and the classification argument of
the report; the three attributes the step is judged against (the two cumulative viral clearance attributes
and fragments); the three analytical methods; the capability records; the two modular viral clearance
contributions; the fitted models (the planned full quadratic of every output with a criterion, the selected
models and the screening models); the two study events; the document relationships and the explicit
non-claims; the three studies of the execution-window table; the design space; the proven acceptable
ranges; the criteria of the criteria-change table (Version 1.0 superseded, Version 2.0 in force); the
assertions; the report statements, grouped by the chapters of the report; the concepts; and the rhetorical
spans of ``authoring/rhetorical/PCR-009.spans.yaml``.

Every table of the report is a complex table (``T.frame`` or a ``T.`` builder), read back through
``qmd_ctables`` from the object the report printed, or a markdown string of a ``_pcpkg`` helper
(``related_docs_md``, ``dev_register``, ``discrepancy_register``), read back with ``md_string_rows``, so each
row quote is the rendered row, with ``table_header=rows.header``. Every prose quote is a span of the
``.qmd`` found by ``S`` (a unique prefix of the source, run to the end of its sentence or to a given end
string) and rendered as the ``.docx`` reads it (``render``: the inline expressions evaluated in the report's
own namespace, a cross-reference resolved to its rendered number, typographic quotes and apostrophes), so no
value and no quote is typed here. ``q`` refuses a span that crosses a citation, and ``build()`` refuses to
return an annex with a quote that does not ground or a weak anchor.

The proven acceptable ranges are recorded as the report prints them: the "PAR (set-point)" column of the
PAR table goes to ``par_at_setpoint`` as printed, and the report's description of the two analyses is
recorded in its own words. Nothing is added to it (registered discrepancy D-001).
"""
from __future__ import annotations

import os
import re

import _pcpkg as P
import build_ground_truth as G
import schema_ext as S
from check_grounding import normalize, specificity_report

DOC = "PCR-009"
FILE = "PCR-009_virus_filtration.docx"
QMD = "PCR-009_virus_filtration.qmd"
UO = "virus_filtration"
#: The scale-down model as the report names it (Executive summary, Section 3.1).
SDM_NAME = "scale-down model of the commercial step"

_INTRO = "Introduction"
_PRIOR = "Prior knowledge and quality risk basis"
_MM = "Materials and methods"
_SD = "Study design"
_RES = "Results"
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
    "stats": (_MM, "Statistical methods"),
    "factors": (_SD, "Factors, ranges and the knowledge space"),
    "scr_design": (_SD, "Screening design"),
    "rsm_design": (_SD, "Response-surface design"),
    "uni_design": (_SD, "Univariate assessment"),
    "centre": (_RES, "Centre-point performance and reproducibility"),
    "screening": (_RES, "Factor effects in the screening design"),
    "rsm": (_RES, "Response-surface models"),
    "mech": (_RES, "Mechanistic interpretation"),
    "ds": ("Design space",),
    "par": ("Proven acceptable ranges",),
    "cap": ("Process capability and robustness",),
    "class": ("Parameter classification",),
    "cs": ("Contribution to the control strategy",),
    "disc": ("Discussion",),
    "concl": ("Conclusions",),
    "record": (_REC,),
    "events": (_REC, _EV),
    "dev1": (_REC, _EV, "DEV-009-01, transient excursion of the filtration pressure"),
    "dev2": (_REC, _EV, "DEV-009-02, membrane lot flux below the value typical for the vendor"),
    "pds": (_REC, "Discrepancies from the plan"),
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
CHAPTERS = ["Executive summary", "Introduction", _PRIOR, _MM, _SD, _RES, "Design space",
            "Proven acceptable ranges", "Process capability and robustness", "Parameter classification",
            "Contribution to the control strategy", "Discussion", "Conclusions", _REC]


def _sid(sec):
    return f"{DOC}_sec_{sec}"


def _source():
    return open(os.path.join(G.HERE, QMD), encoding="utf-8").read()


def _raw_prose():
    """The .qmd outside its code chunks, as written (line structure kept)."""
    return re.sub(r"```\{python\}.*?```", " ", _source(), flags=re.S)


def _prose():
    """The .qmd outside its code chunks, in the comparison form (``normalize``)."""
    return normalize(_raw_prose())


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
    """``{label -> rendered cross-reference}`` ("sec-par" -> "Section 7", "tbl-par" -> "Table 20").

    A section number follows the numbering of the headings (an unnumbered heading takes none), as the
    rendered document prints it. A table or figure number is read off the rendered caption ("Table 20:
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
    """A rendered cell without its trailing footnote markers ("2 a)", "5.20 b)")."""
    return re.sub(r"(?:\s[a-z]\))+$", "", str(cell)).strip()


def _num(cell):
    """A number as the document prints it, back to a float ("−0.866", "2,000", "5.20 b)"); None for a
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
    fx = ns["fx"]
    pv = ns["pv"]
    FAC = list(ns["FAC"])                                         # ["filtration_volume", "pressure"]
    PRM = {k: ns["uo"].param(k) for k in FAC}
    NAME = {k: PRM[k].name for k in FAC}
    UNIT = {k: PRM[k].unit for k in FAC}
    LET = ns["LET"]
    RESP4 = list(ns["RESP4"])
    LAB2, LAB, RUNIT = ns["_lab2"], ns["_lab"], ns["_unit"]
    FT, RI = ns["FT"], ns["RI"]
    UO_NAME, STEP_LABEL = G.VFUO_NAME, G.VFSTEP_LABEL
    PC = G.VFPARAM_CONCEPT                                        # parameter name -> concept id
    pkey = {NAME[k]: k for k in FAC}
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))
    reg = P.cqa_reg.set_index("key")
    by_label = G._attr_key_by_label()
    resp_attr = {"mvm_lrf": "lrv_mvm", "xmulv_lrf": "lrv_xmulv", "lmw_cesds_pct": "fragments_lmw",
                 "step_yield": "step_yield"}
    attr_resp = {v: k for k, v in resp_attr.items()}
    lab2_resp = {LAB2[r]: r for r in RESP4}
    CL_M, CL_X, CR_F = ns["CL_M"], ns["CL_X"], ns["CR_F"]
    iac_ = ns["IAC9"].set_index("response")

    # ---- the rendered tables, from the objects the report printed --------------------------------
    pdf_ = ct["tbl-params"][1]
    pt_t, prow = keyed("tbl-params", list(pdf_["Parameter"]), str, cell=1)
    pdf_ = pdf_.set_index("Parameter")
    cq_df = ct["tbl-cqa"][1]
    ckeys = [by_label[n] for n in cq_df["CQA"]]
    cq_t, crow = keyed("tbl-cqa", ckeys, lambda k: names[k], cell=1)
    cq_df = cq_df.set_index(np.array(ckeys))
    sop_df = ct["tbl-sops"][1]
    sop_t, soprow = keyed("tbl-sops", list(sop_df["Reference"]), str, cell=1)
    amv_title = dict(zip(sop_df["Reference"], sop_df["Title"]))
    appd_df = ct["tbl-appd"][1]
    appd_t, appdrow = keyed("tbl-appd", list(appd_df["AMV"]), str, cell=2)
    win_df = ct["tbl-windows"][1]
    win_t, winrow = keyed("tbl-windows", list(win_df["Study"]), str, cell=0)
    off_t, offrow = keyed("tbl-sdm-offsets", ["step_yield"], lambda k: "Step yield (%)", cell=0)
    ikeys = [by_label[_cells(r)[0]] for r in ct["tbl-iac"][0].rows()]
    iac_t, irow = keyed("tbl-iac", ikeys, lambda k: T.ATTR_NAME[k], cell=0)
    crkeys = [by_label[_cells(r)[0]] for r in ct["tbl-criteria-virus-filtration"][0].rows()]
    cr_t, crrow = keyed("tbl-criteria-virus-filtration", crkeys, lambda k: T.ATTR_NAME[k], cell=0)
    rvkeys = [by_label[_cells(r)[0]] for r in ct["tbl-reeval-virus-filtration"][0].rows()]
    rv_t, rvrow = keyed("tbl-reeval-virus-filtration", rvkeys, lambda k: T.ATTR_NAME[k], cell=0)
    cen_df = ct["tbl-centre"][1]
    cen_t, cenrow = keyed("tbl-centre", list(zip(ffill(cen_df["Design"]), cen_df["Response"])),
                          lambda k: k[1], cell=1)
    sf_df = ct["tbl-scr-fit"][1]
    sf_t, sfrow = keyed("tbl-scr-fit", [lab2_resp[x] for x in sf_df["Response"]], lambda r: LAB2[r], cell=0)
    se_df = ct["tbl-scr-effects"][1]
    se_t, serow = keyed("tbl-scr-effects", list(zip(ffill(se_df["Response"]), se_df["Term"])),
                        lambda k: k[1], cell=1)
    se_lab = {r: f"{LAB2[r]} ({RUNIT[r]})" for r in RESP4}          # the response cell of the effects tables
    ad_t = ct["tbl-adequacy"][0]
    ad_keys = [lab2_resp[_cells(r)[0]] for r in ad_t.rows()]
    ad_t, adrow = keyed("tbl-adequacy", ad_keys, lambda r: LAB2[r], cell=0)
    inf_t = ct["tbl-influence"][0]
    inf_keys = [lab2_resp[_cells(r)[0]] for r in inf_t.rows()]
    inf_t, infrow = keyed("tbl-influence", inf_keys, lambda r: LAB2[r], cell=0)
    cm_df = ct["tbl-coef-mvm"][1]
    cm_t, cmrow = keyed("tbl-coef-mvm", list(cm_df["Term"]), str, cell=0)
    an_df = ct["tbl-anova-mvm"][1]
    an_t, anrow = keyed("tbl-anova-mvm", list(an_df["Source"]), str, cell=0)
    del_df = ct["tbl-deletion"][1]
    del_t, delrow = keyed("tbl-deletion", list(range(len(del_df))), lambda i: re.sub(r"\^.*", "", str(del_df["Run deleted"].iloc[i])),
                          cell=0)
    par_df = ct["tbl-par"][1]
    par_keys = list(zip(ffill(par_df["CQA"]), par_df["Parameter"]))
    par_t, parrow = keyed("tbl-par", par_keys, lambda k: k[1], cell=1)
    cap_df = ct["tbl-capability"][1]
    capkeys = [by_label[n] for n in cap_df["Attribute"]]
    cap_t, caprow = keyed("tbl-capability", capkeys, lambda k: names[k], cell=0)
    cap_df = cap_df.set_index(np.array(capkeys))
    as_df = ct["tbl-appc-scr"][1]
    as_t, asrow = keyed("tbl-appc-scr", list(zip(ffill(as_df["Response"]), as_df["Term"])), lambda k: k[1], cell=1)
    asel_df = ct["tbl-appc-sel"][1]
    asel_t, aselrow = keyed("tbl-appc-sel", list(zip(ffill(asel_df["Output"]), asel_df["Term"])),
                            lambda k: k[1], cell=1)
    af_df = ct["tbl-appc-full"][1]
    af_t, afrow = keyed("tbl-appc-full", list(zip(ffill(af_df["Output"]), af_df["Term"])), lambda k: k[1], cell=1)
    sel_lab = {r: (f"{LAB2[r]} ({RUNIT[r] if r != 'lmw_cesds_pct' else '%'})").replace("(% points)", "(%)")
               for r in RESP4}                                       # the output cell of Appendix C
    mbs_t = ct["tbl-methods-by-study"][0]
    mbsrow = present_header(G.ctable_rows(mbs_t))
    mtx = {}
    for kind, label in (("screening", "tbl-doe-virus-filtration-screening"), ("rsm", "tbl-doe-virus-filtration-rsm")):
        tab = ct[label][0]
        mtx[kind] = (tab, present_header(G.ctable_rows(tab, [int(_cells(r)[0]) for r in tab.rows()])))
    rel, rel_cap = md_rows(P.related_docs_md(DOC), "tbl-related")
    devrow, dev_cap = md_rows(P.dev_register(DOC), "tbl-events")
    pdrow, pd_cap = md_rows(P.discrepancy_register(DOC), "tbl-discrepancies")
    PDS = {d["id"]: d for d in ns["PDS"]}

    def pdref(pid, sec="pds"):
        return ref(sec, pdrow[pid], rows=pdrow, caption=pd_cap, label="tbl-discrepancies")

    # ==== entities ===================================================================================
    q_step1 = Q("The step removes virus by size.")
    q_step2 = Q("It is the dedicated small virus removal operation")
    q_filters = Q("The small virus retentive filtration step filters the flow-through pool")
    q_run = Q("The step is run at a set filtration pressure")
    q_forms = Q("The step forms no quality attribute.")
    step = S.ProcessStep(
        step_id="step:virus_filtration", step_name=UO_NAME, step_number=str(G.VFSTEP), unit_operation=UO_NAME,
        description=t("Step 9 of the A-Mab drug substance process. The step filters the flow-through pool of anion "
                      "exchange through a membrane whose pore size distribution retains the parvoviruses while the "
                      "antibody passes, at a set filtration pressure, in psi, up to a set filtration volume, the volume "
                      "of load filtered per square metre of membrane, in L/m2. It removes virus by size, is the "
                      "principal source of MVM clearance and also carries a claim for XMuLV, each of "
                      "`{python} fx(CL_M)` log10 in the modular viral clearance claim. The step forms no quality "
                      "attribute; its filtrate is judged against the drug substance criterion for fragments, because "
                      "no later step changes them."),
        input_materials=["flow-through pool of anion exchange"],
        output_materials=["filtrate (load of UF/DF)"],
        equipment=[SDM_NAME],
        source_references=[ref("exec", q_step1), ref("exec", q_step2), ref("uo", q_filters), ref("uo", q_run),
                           ref("uo", q_forms)],
        metadata=meta())
    q_sdm1 = Q("It was run on a scale-down model of the commercial step", "a scale-down model of the commercial step")
    q_sdm2 = Q("The scale-down model uses the same filter type as manufacturing")
    q_sdm3 = Q("The volumetric load in L/m2 and the filtration pressure of the model")
    equipment = [S.Equipment(
        equipment_id="equip:vf_sdm", equipment_name=SDM_NAME,
        equipment_type="virus filtration (scale-down model and spiking model)", site_name=P.SENDING_SITE,
        source_references=[ref("exec", q_sdm1), ref("sdm", q_sdm2), ref("sdm", q_sdm3)],
        metadata=meta())]
    sites = G._site_entities(DOC, FILE, _sid("title"))

    # -- parameters: the table row, the PAR row for MVM, and the sentences of the classification argument --
    PAR_V_N, PAR_P_N, PAR_V_S = ns["PAR_V_N"], ns["PAR_P_N"], ns["PAR_V_S"]
    MARG_V, EFF_V = ns["MARG_V"], ns["EFF_V"]
    LAB_M, LAB_X, LAB_F = ns["LAB_M"], ns["LAB_X"], ns["LAB_F"]
    q_cls_both = Q("Both parameters were classified as well-controlled critical process parameters (WC-CPP).")
    cls_quotes = {
        "filtration_volume": [
            q_cls_both,
            Q("A term containing the parameter is significant for MVM LRF"),
            Q("Across its NOR-propagated PAR, "),
            Q("The volumetric load is set by the volume of load applied to a filter of known area"),
            Q("The parameter was classified as a WC-CPP on this margin and this control.")],
        "pressure": [
            q_cls_both,
            Q("No term containing the parameter is significant for any output, in either design"),
            Q("No effect of pressure on an attribute was therefore detected within"),
            Q("The parameter was classified as a WC-CPP on that basis"),
            Q("No effect of filtration pressure was detected, and its class follows the A-Mab case study")],
    }
    M_LO, M_EDGE = ns["M_LO"], ns["M_EDGE"]
    head = "Classified {c} under SOP-4001 (PCP-009 §7, PCMP-001 §7.7). "
    rationale = {
        "filtration_volume": head.format(c=ns["CLASS_V"]) + (
            f"A term containing the parameter is significant for MVM LRF ({pv(FT['mvm_lrf']['p'])}); across the "
            f"range studied the mean MVM LRF falls by {fx(-EFF_V)} log10 and across its NOR-propagated PAR of "
            f"{PAR_V_N} L/m2 by {fx(M_LO - M_EDGE)} log10, for an attribute of very high criticality. The PAR "
            f"extends {MARG_V:g} L/m2 beyond the upper NOR edge and its lower edge is the end of the range studied; "
            f"the volumetric load is set by the volume of load applied to a filter of known area, so it can be held "
            f"within its NOR. Neither PCMP-001 nor SOP-4001 sets a number for the size of the effect or the margin, "
            f"so the class is a judgement of the report on this margin and this control. With run 5 deleted the PAR "
            f"would reach the end of the range studied and the class would be the same."),
        "pressure": head.format(c=ns["CLASS_P"]) + (
            f"No term containing the parameter is significant for any output in either design (MVM LRF "
            f"{pv(ns['PF_B_P'])} for the main effect and {pv(ns['PF_B2_P'])} for the square in the full quadratic, "
            f"XMuLV LRF {pv(ns['XB_P'])} in its selected model, which is not adequate), so the class does not "
            f"follow from the rule of PCP-009 §7. It follows the A-Mab case study, which classes both parameters "
            f"of the step as WC-CPP, and the scope of the viral clearance claim, which holds only for the pressures "
            f"of the spiking runs, {ns['rng_s'](ns['RNG_P'])} psi, and for uninterrupted flow. The PAR of the "
            f"parameter is the whole range studied."),
    }
    params = []
    for name, row in prow.items():
        k = pkey[name]
        r = pdf_.loc[name]
        unit = r["Unit"]
        par_nor = PAR_V_N if k == "filtration_volume" else PAR_P_N
        refs = [ref("factors", row, pt_t, prow), ref("par", parrow[(LAB_M, name)], par_t, parrow)]
        refs += [ref("exec" if i == 0 else "class", x) for i, x in enumerate(cls_quotes[k])]
        params.append(S.ProcessParameter(
            parameter_id=PC[name], parameter_name=name, parameter_type=ns["PR"].loc[name, "Class"], unit=unit,
            target_value=f"{r['Set-point']} {unit}", NOR=f"{r['NOR']} {unit}", PAR=f"{par_nor} {unit}",
            associated_step=STEP_LABEL, rationale_for_criticality=rationale[k], study_type="multivariate",
            source_references=refs, metadata=meta()))

    # -- attributes: the register row, the row of the criterion derivation and the row of the outputs against
    # their criteria --------------------------------------------------------------------------------------
    q_vh = Q("Both viral safety attributes are of very high criticality.")
    q_mvm = Q("MVM is the virus whose retention the operating parameters of this step can degrade.")
    q_frag = Q("Fragments are of low criticality.")
    attr_prose = {"lrv_mvm": [("cqa", q_vh), ("cqa", q_mvm)],
                  "lrv_xmulv": [("cqa", q_vh), ("uo", Q("XMuLV, an enveloped retrovirus, is many times larger"))],
                  "fragments_lmw": [("cqa", q_frag),
                                    ("uo", Q("Its filtrate is also judged against the drug substance criterion for "
                                             "fragments"))]}
    method_of = {"lrv_mvm": "AMV-3018", "lrv_xmulv": "AMV-3017", "fragments_lmw": "AMV-3020"}
    for k_, a_ in method_of.items():
        if appd_df.loc[appd_df["AMV"] == a_, "Output"].iloc[0] != LAB2[attr_resp[k_]]:
            raise ValueError(f"{DOC}: the methods summary no longer pairs {k_} with {a_}")
    attrs = []
    for key in ckeys:
        r = cq_df.loc[key]
        unit_step = reg.loc[key, "unit"].replace(" (cumulative)", "")
        crit = [f"{r['Acceptance']} (drug substance)",
                f"{_unmark(_cells(irow[key])[-2])} {unit_step} (intermediate acceptance criterion, filtrate of the "
                f"step{', platform claim of the step' if key.startswith('lrv_') else ''})"]
        viral = key.startswith("lrv_")
        why = (f"Very high by rule for viral clearance, because a viral contamination would harm the patient directly "
               f"(Tool #1 score {r['Tool #1']})." if viral else
               f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = {r['Tool #1']}.")
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=names[key], attribute_type="CQA",
            unit=reg.loc[key, "unit"], acceptance_criteria=crit, analytical_method=method_of[key],
            associated_steps=[STEP_LABEL], rationale_for_criticality=why,
            criticality_level=r["Criticality"], tool1_score=int(r["Tool #1"]),
            tool2_severity=int(reg.loc[key, "tool2_severity"]),
            source_references=[ref("cqa", crow[key], cq_t, crow), ref("par", irow[key], iac_t, irow),
                               ref("par", crrow[key], cr_t, crrow)]
            + [ref(s_, x) for s_, x in attr_prose[key]],
            metadata=meta()))

    # -- analytical methods: the procedure row, the methods-summary row, the clause that names the method, and
    # for nrCE-SDS the row of the methods-by-study table ---------------------------------------------------
    q_meth = {"AMV-3018": Q("MVM was titred by TCID50 with qPCR confirmation (AMV-3018)", "(AMV-3018)"),
              "AMV-3017": Q("XMuLV by TCID50 (AMV-3017)", "(AMV-3017)"),
              "AMV-3020": Q("fragments by nrCE-SDS (AMV-3020)", "(AMV-3020)")}
    methods = []
    for amv in [a for a in sop_df["Reference"] if a.startswith("AMV-")]:
        key = {v: k for k, v in method_of.items()}[amv]
        out_ = appd_df.loc[appd_df["AMV"] == amv].iloc[0]
        methods.append(S.AnalyticalMethod(
            method_id=amv, method_name=amv_title[amv], method_type=G.METHOD_TYPE.get(amv),
            analytes=[out_["Output"]], associated_attributes=[f"attr:{key}"], validation_status="validated",
            source_references=[ref("analytics", soprow[amv], sop_t, soprow),
                               ref("app_d", appdrow[amv], appd_t, appdrow), ref("analytics", q_meth[amv])]
            + (G.size_variant_refs(DOC, FILE, title("analytics"), [UO], G.SIZE_VARIANT_TOKEN[amv], text, lead=1)
               if amv in G.SIZE_VARIANT_TOKEN else []),
            metadata=meta()))

    # -- capability: one record per row of the capability table ----------------------------------------
    CAPT, N_MC = ns["CAPT"], int(ns["N_MC"])
    q_cap_vir = Q("The Cpk of the cumulative MVM clearance is")
    q_cap_frag = Q("The Cpk of fragments is")
    cap_prose = {"lrv_mvm": q_cap_vir, "lrv_xmulv": q_cap_vir, "fragments_lmw": q_cap_frag}
    capab = []
    for key, row in caprow.items():
        c = cap_df.loc[key]
        mean_, sd_ = [x.strip() for x in c["Mean ± SD"].split("±")]
        capab.append(ProcessCapability(
            capability_id=f"{DOC}-CAP{len(capab) + 1:02d}", quality_attribute=f"attr:{key}", index_name="Cpk",
            index_value=_num(c["Cpk"]),
            specification_side={"lower": "lower", "upper": "upper"}.get(CAPT.loc[key, "spec_type"], "two_sided"),
            acceptance_range=c["Criterion"], mean=mean_, standard_deviation=sd_, unit=reg.loc[key, "unit"],
            basis="simulated", n_batches=N_MC, unit_operation=UO_NAME,
            source_references=[ref("cap", row, cap_t, caprow), ref("cap", cap_prose[key])],
            metadata=meta()))

    # -- the modular viral clearance claims ------------------------------------------------------------
    q_sum_x = Q("For XMuLV the claims of low-pH viral inactivation")
    q_sum_m = Q("For MVM the claims of anion exchange")
    q_cs_m = Q("The step contributes `{python} fx(CL_M)` log10 to the cumulative MVM claim")
    q_cs_x = Q("It contributes `{python} fx(CL_X)` log10 to the cumulative XMuLV claim")
    title_of = P.UNIT_OP_TITLES
    step_of = lambda k: f"{title_of[k]} (Step {P.CFG.unit_op(k).step})"   # noqa: E731
    contributions = [
        ModularContribution(
            contribution_id=f"{DOC}-MC01", quantity=names["lrv_mvm"], unit_operation=UO_NAME,
            step_value=f"{fx(CL_M)} log10", cumulative_value=f"{fx(ns['SUM_M'])} log10",
            requirement=f"≥ {ns['REQ_M']:g} log10", unit="log10", contributing_steps=[step_of("aex")],
            source_references=[ref("par", q_sum_m), ref("cs", q_cs_m)], metadata=meta()),
        ModularContribution(
            contribution_id=f"{DOC}-MC02", quantity=names["lrv_xmulv"], unit_operation=UO_NAME,
            step_value=f"{fx(CL_X)} log10", cumulative_value=f"{fx(ns['SUM_X'])} log10",
            requirement=f"≥ {ns['REQ_X']:g} log10", unit="log10",
            contributing_steps=[step_of("viral_inactivation"), step_of("aex")],
            source_references=[ref("par", q_sum_x), ref("cs", q_cs_x)], metadata=meta())]

    # -- fitted models ---------------------------------------------------------------------------------
    fac_of = {v: k for k, v in LET.items()}

    def term_label(term):
        """A term of the coefficient tables ("A", "AB", "B²") in words."""
        base = term.rstrip("²")
        name = " × ".join(NAME[fac_of[x]].lower() for x in base)
        return name + ("²" if term.endswith("²") else "")

    def sig_of(p_):
        return p_.startswith("<") or (_num(p_) is not None and _num(p_) < float(ns["ALPHA"]))

    def terms_of(rows_, out_lab, cols):
        """The terms of one output's block of an Appendix C table, besides the intercept, as printed.
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

    # the full quadratic model PCP-009 §5.5 planned, on the planned runs (re-evaluation table)
    q_full = Q("The full quadratic did not meet the limit on overfitting for any output with a criterion.")
    for key, row in rvrow.items():
        c = _cells(row)
        resp = attr_resp[key]
        used = _unmark(c[5]) + (" (no adequate model; the output is judged on its measured results)"
                                if c[5].endswith(" a)") else "")
        fit_rec(resp, "full quadratic (planned, PCP-009 §5.5)",
                [ref("rsm", row, rv_t, rvrow), ref("rsm", q_full)]
                + [ref("app_c", afrow[k_], af_t, afrow) for k_ in afrow if k_[0] == sel_lab[resp]],
                n_runs=int(c[1]), r_squared=_num(c[2]), predicted_r_squared=_num(c[3]),
                adequacy_statement=f"Planned full quadratic on the {c[1]} planned runs: R² {c[2]}, predicted R² "
                                   f"{c[3]}, R² minus predicted R² {c[4]}, above the limit on overfitting; not used "
                                   f"for any conclusion of Version 2.0. The model the output uses under the model "
                                   f"selection (PD-009-01): {used}.",
                terms=terms_of(afrow, sel_lab[resp], {"coef": 2, "se": 3, "p": 4}))

    def adeq(resp):
        c = _cells(adrow[resp])           # Output | Terms | R² | Adj. R² | Pred. R² | Residual SD | p | Met | p | Met | Gap | Met
        return dict(terms=c[1], r2=c[2], adj=c[3], pred=c[4], sd=c[5], p=c[6], p_met=c[7], lof=c[8],
                    lof_met=c[9], gap=c[10], gap_met=c[11])

    def infl(resp):
        c = _cells(infrow[resp])          # Output | abs. residuals | order | largest | F median | 4/n | F | Met
        return dict(spread=c[1], order=c[2], largest=c[3], fmed=c[4], over=c[5], over_f=c[6], met=c[7])

    def centre_kw(resp):
        cc = cen[("Response surface", LAB[resp])]
        return dict(replicate_n=int(cc[2]), replicate_mean=cc[3], replicate_sd=cc[4], replicate_cv=cc[5])

    # MVM LRF: a straight line in filtration volume; fails the criterion on residuals and influential runs
    a_, i_ = adeq("mvm_lrf"), infl("mvm_lrf")
    mod, lof = _cells(anrow["Model"]), _cells(anrow["Lack of fit"])
    q_mvm_line = Q("MVM LRF is modelled by a straight line in filtration volume")
    q_mvm_pass = Q("The model therefore passes the F-test, shows no lack of fit and meets the limit on overfitting.")
    q_mvm_fail = Q("The model of MVM LRF does not meet the criterion on residuals and influential runs.")
    q_run5 = Q("Run 5, at `{python} fx(COOK5)`, also exceeds the median of F(p, n − p)")
    fit_rec("mvm_lrf", "selected model (PD-009-01), raw scale, terms besides the intercept: filtration volume (A)",
            [ref("rsm", q_mvm_line), ref("rsm", q_mvm_pass), ref("rsm", q_mvm_fail), ref("rsm", q_run5),
             ref("rsm", adrow["mvm_lrf"], ad_t, adrow), ref("rsm", infrow["mvm_lrf"], inf_t, infrow),
             ref("rsm", anrow["Model"], an_t, anrow), ref("rsm", anrow["Lack of fit"], an_t, anrow),
             ref("centre", cenrow[("Response surface", LAB["mvm_lrf"])], cen_t, cenrow)]
            + [ref("rsm", cmrow[k_], cm_t, cmrow) for k_ in cmrow],
            n_runs=int(FT["mvm_lrf"]["n"]), r_squared=_num(a_["r2"]), adjusted_r_squared=_num(a_["adj"]),
            predicted_r_squared=_num(a_["pred"]), f_statistic=_num(mod[4]), p_value=_num(mod[5]),
            lack_of_fit_p=_num(lof[5]), rmse=_num(a_["sd"]),
            adequacy_statement=(
                f"Passes the model F-test (p {a_['p']}), shows no lack of fit (p {a_['lof']}) and meets the limit on "
                f"overfitting (R² minus predicted R² {a_['gap']}); fails the criterion on residuals and influential "
                f"runs of PCMP-001 §7.2: residual trends p {i_['spread']} and {i_['order']}, runs {i_['over']} above "
                f"4/n, run {i_['over_f']} above the median of F(p, n − p) of {i_['fmed']} (largest Cook's distance "
                f"{i_['largest']}). Used for the ranges and the design space although it fails that criterion "
                f"(PD-009-02); no single deletion changed the judgement over the NOR."),
            terms=[ModelTerm(term=k_, factor=term_label(k_), coefficient=_num(_cells(r_)[1]),
                             standard_error=_num(_cells(r_)[2]), t_statistic=_num(_cells(r_)[3]),
                             p_value=_num(_cells(r_)[4]), significant=sig_of(_cells(r_)[4]))
                   for k_, r_ in cmrow.items() if k_ != "Intercept"],
            **centre_kw("mvm_lrf"))
    # XMuLV LRF: pressure alone, not adequate
    a_, i_ = adeq("xmulv_lrf"), infl("xmulv_lrf")
    q_x1 = Q("XMuLV LRF has no adequate model. The selected model carries pressure alone", "XMuLV LRF has no adequate model.")
    q_x2 = Q("The selected model carries pressure alone")
    fit_rec("xmulv_lrf", "selected model (PD-009-01), raw scale, terms besides the intercept: filtration pressure (B); "
                         "not adequate",
            [ref("rsm", q_x1), ref("rsm", q_x2), ref("rsm", adrow["xmulv_lrf"], ad_t, adrow),
             ref("rsm", infrow["xmulv_lrf"], inf_t, infrow)]
            + [ref("app_c", aselrow[k_], asel_t, aselrow) for k_ in aselrow if k_[0] == sel_lab["xmulv_lrf"]],
            n_runs=int(FT["xmulv_lrf"]["n"]), r_squared=_num(a_["r2"]), adjusted_r_squared=_num(a_["adj"]),
            predicted_r_squared=_num(a_["pred"]), p_value=_num(a_["p"]), lack_of_fit_p=_num(a_["lof"]),
            rmse=_num(a_["sd"]),
            adequacy_statement=(
                f"Not adequate by PCMP-001 §7.2: the model F-test is not significant (p {a_['p']}) and R² minus "
                f"predicted R² is {a_['gap']}, above the limit on overfitting; the lack of fit is not significant (p "
                f"{a_['lof']}) and the criterion on residuals and influential runs is met. XMuLV LRF is judged on its "
                f"measured results and has no PAR."),
            terms=terms_of(aselrow, sel_lab["xmulv_lrf"], {"coef": 2, "se": 3, "t": 4, "p": 5}),
            **centre_kw("xmulv_lrf"))
    # fragments and step yield: intercept-only models
    q_f1 = Q("The selected model of fragments is intercept-only, with a mean of")
    q_f2 = Q("Its residuals show no departure from normality (Shapiro-Wilk `{python} pv(SW['lmw_cesds_pct'])`)")
    q_y1 = Q("The selected model of step yield is intercept-only, with a mean of")
    for resp, extra in (("lmw_cesds_pct", [q_f1, q_f2]), ("step_yield", [q_y1])):
        a_, i_ = adeq(resp), infl(resp)
        fit_rec(resp, "selected model (PD-009-01), raw scale, intercept only",
                [ref("rsm", x) for x in extra] + [ref("rsm", adrow[resp], ad_t, adrow),
                                                  ref("rsm", infrow[resp], inf_t, infrow),
                                                  ref("app_c", aselrow[(sel_lab[resp], "Intercept")], asel_t, aselrow)],
                n_runs=int(FT[resp]["n"]), r_squared=_num(a_["r2"]), adjusted_r_squared=_num(a_["adj"]),
                predicted_r_squared=_num(a_["pred"]), lack_of_fit_p=_num(a_["lof"]), rmse=_num(a_["sd"]),
                adequacy_statement=(
                    f"Intercept-only model: no F-test applies; lack of fit p {a_['lof']}; R² minus predicted R² "
                    f"{a_['gap']}, fixed by the number of runs, within the limit on overfitting; criterion on "
                    f"residuals and influential runs {i_['met'].lower()} (runs above 4/n: {i_['over']}). The output "
                    f"does not depend on the parameters within the range studied."
                    + (" Step yield is a process performance output with no criterion." if resp == "step_yield" else "")),
                terms=[], **centre_kw(resp))
    # the screening models: both main effects and their interaction, used for no prediction
    for resp, row in sfrow.items():
        c = _cells(row)                   # Response | R² | Adj. R² | Pred. R² | Model F-test p | Curvature p
        cs_ = cen[("Screening", LAB[resp])]
        fit_rec(resp, "screening model: both main effects and their interaction in coded units",
                [ref("screening", row, sf_t, sfrow),
                 ref("centre", cenrow[("Screening", LAB[resp])], cen_t, cenrow)]
                + [ref("screening", serow[(se_lab[resp], tm)], se_t, serow) for tm in ("A", "B", "AB")]
                + [ref("app_c", asrow[(se_lab[resp], tm)], as_t, asrow) for tm in ("A", "B", "AB")],
                n_runs=int(ns["n_scr"]), r_squared=_num(c[1]), adjusted_r_squared=_num(c[2]),
                predicted_r_squared=_num(c[3]), p_value=_num(c[4]), lack_of_fit_p=_num(c[5]),
                adequacy_statement=(f"Screening model, used to identify effects and for no prediction; model F-test p "
                                    f"{c[4]}; the one-degree-of-freedom lack of fit tests curvature, p {c[5]}. Four "
                                    f"parameters on {ns['N_SCR_PTS']} distinct design points, so its fit statistics "
                                    f"overstate how well it fits."),
                terms=terms_of(asrow, se_lab[resp], {"effect": 2, "coef": 3, "se": 4, "t": 5, "p": 6}),
                replicate_n=int(cs_[2]), replicate_mean=cs_[3], replicate_sd=cs_[4], replicate_cv=cs_[5])

    # -- study events --------------------------------------------------------------------------------------
    EV = ns["EV"]
    dev_prose = {
        "DEV-009-01": [("dev1", Q("During in-process pressure monitoring the filtration pressure of one run rose")),
                       ("dev1", Q("The investigation attributed the excursion to an overshoot of the pump ramp.")),
                       ("dev1", Q("The record names neither the run, nor its set pressure")),
                       ("dev1", Q("If the run was a response-surface run, its deletion leaves the judgement")),
                       ("dev1", Q("The run was retained in the analysis."))],
        "DEV-009-02": [("dev2", Q("The pre-use flux verification of membrane lot")),
                       ("dev2", Q("The investigation attributed the low flux to variation of membrane permeability")),
                       ("dev2", Q("The lot may therefore have been used for several runs")),
                       ("dev2", Q("Whether it changed the retention of MVM was not tested")),
                       ("dev2", Q("The record does not link the lot to run 5."))],
    }
    dev_impact = {
        "DEV-009-01": t("The peak of `{python} dev_009_01_pmax_psi` psi lies inside the range studied, "
                        "`{python} rng_s(RNG_P)` psi, over which no term containing pressure was significant for any "
                        "output. The record names neither the run, nor its set pressure, nor the duration; the run was "
                        "analysed at its design setting and retained. If it was a response-surface run its deletion "
                        "leaves the judgement over the NOR unchanged; if a screening run, its result enters only the "
                        "screening effects and the judgement of XMuLV LRF, every measured result of which met the "
                        "claim; if a qualification run, only the offset of step yield, on which no conclusion depends."),
        "DEV-009-02": t("The pre-use flux of membrane lot `{python} LOT` was `{python} dev_009_02_flux_deficit_pct` % "
                        "below the value typical for the vendor. No record names the runs made on the lot, so it may "
                        "have been used for several runs and the deletion of one run at a time does not bound its "
                        "effect. Whether the lower permeability changed the retention of MVM was not tested, so the "
                        "effect of the event on the results cannot be assessed from the record; every run made on the "
                        "lot was retained."),
    }
    devs = []
    for did, row in devrow.items():
        c = _cells(row)
        devs.append(Deviation(
            deviation_id=did, summary=c[1], unit_operation=UO_NAME, detected_during=c[2], disposition=c[3],
            impact_statement=dev_impact[did], no_impact_on_conclusions=(did == "DEV-009-01"),
            source_references=[ref("events", row, rows=devrow, caption=dev_cap, label="tbl-events")]
            + [ref(s_, x) for s_, x in dev_prose[did]],
            metadata=meta()))
        if str(EV.loc[did, "disposition"]) != "retained":
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
    q_inv1 = Q("It is issued under the QA investigation")
    q_inv2 = Q("This revision also applies the second investigation")
    q_cap_steps = Q("For MVM these are anion exchange (PCR-008) and this step")
    relation("executed_under", "PCP-009", "The plan paired with the report is PCP-009.", "uo",
             Q("The plan paired with this report is PCP-009."))
    relation("executed_under", "PCMP-001", "Version 2.0 judges each output against the intermediate acceptance "
             "criteria of the master plan PCMP-001 Version 2.0.", "exec",
             Q("Version 2.0 judges each output against the intermediate acceptance criteria of the master plan"))
    relation("rolls_up_into", "PCMR-001", "The results of the report roll up into the master report PCMR-001, which "
             "consolidates the cumulative viral clearance claim.", "exec",
             Q("The results of this report roll up into the master report PCMR-001"))
    relation("references", "PTP-001", "The study supports the transfer of the process from Cambridge, MA, to "
             "Grafton, WI, under PTP-001.", "exec", Q("The study followed the characterization plan PCP-009"))
    relation("scoped_by", "RA-001", "RA-001 assigned both parameters of the step to multivariate study and none to "
             "univariate study.", "risk", Q("For this step RA-001 assigned its"))
    relation("references", "INV-001", "Version 2.0 is issued under INV-001.", "changes", q_inv1)
    relation("references", "INV-002", "The revision applies INV-002, which applied the model-adequacy criteria of "
             "PCMP-001 §7.2 to every response-surface model with a criterion.", "changes", q_inv2)
    relation("references", "PCR-008", "Anion exchange (PCR-008) is the other step that claims MVM clearance and one of "
             "the steps that claim XMuLV clearance.", "cap", q_cap_steps)
    relation("references", "PCR-006", "Low-pH viral inactivation (PCR-006) is one of the three steps that claim XMuLV "
             "clearance.", "cap", q_cap_steps)
    relation("references", "PCMR-001", "PCMR-001 consolidates the ranges, the classes and the viral clearance claims "
             "of the step with those of the other steps.", "cs",
             Q("PCMR-001 consolidates these ranges, the classes and the viral clearance claims"))

    # -- explicit non-claims, by section --------------------------------------------------------------------
    ncs, nc_at = [], {}

    def nclaim(sec, subject, statement, quotes, rationale=None, elsewhere=None):
        ncs.append(ExplicitNonClaim(
            non_claim_id=f"{DOC}-NC{len(ncs) + 1:02d}", subject=subject, unit_operation=UO_NAME,
            statement=statement, rationale=rationale, handled_elsewhere=elsewhere,
            source_references=[ref(s_, x) for s_, x in quotes], metadata=meta()))
        nc_at.setdefault(sec, []).append(ncs[-1])

    nclaim("changes", "XMuLV PARs of Version 1.0", "The XMuLV LRF PARs that Version 1.0 gave from its full quadratic "
           "model are withdrawn, because XMuLV LRF has no adequate model and therefore no PAR.",
           [("changes", Q("These PARs are withdrawn, because XMuLV LRF has no adequate model and therefore no PAR.")),
            ("par", Q("XMuLV LRF has no adequate model and therefore no PAR (n.a. in"))])
    nclaim("changes", "deviations", "The report records no deviation: a process characterization study is not GMP "
           "manufacture, so events of execution are study events and departures from the plan are discrepancies "
           "from the plan.",
           [("record", Q("A process characterization study is not GMP manufacture and raises no deviation."))])
    nclaim("sdm", "scale-down offset of the two LRF and of fragments", "The two LRF and fragments were not compared at "
           "the two scales, so their offset is unknown rather than zero, and they are judged as the scale-down model "
           "gives them.",
           [("sdm", Q("The two LRF and fragments were not compared at the two scales.")),
            ("sdm", Q("Their offset is unknown, not zero, and they are judged as the scale-down model gives them"))],
           rationale="Virus cannot be spiked into a manufacturing batch; the clearance figures rest on the spiking "
                     "model, the fragment results on the mechanism of the step.")
    nclaim("sdm", "post-use integrity test results of the qualification runs", "No result of the post-use integrity "
           "test is recorded for the qualification runs or the design runs, although Version 1.0 stated that every run "
           "passed it.",
           [("sdm", Q("Version 1.0 of this report stated that every run passed its post-use integrity test"))],
           elsewhere="PD-009-03, PD-009-04")
    nclaim("analytics", "aggregate at this step", "Aggregate was not measured at this step.",
           [("analytics", Q("Aggregate was not measured at this step."))])
    nclaim("analytics", "LRF as a lower bound", "Whether any filtrate titre was below the limit of detection, which would "
           "make its LRF a lower bound, cannot be read from the record.",
           [("analytics", Q("Whether any filtrate titre was below the limit of detection"))], elsewhere="PD-009-04")
    nclaim("factors", "claims beyond the ranges studied", "No claim of the report extends beyond the ranges studied, "
           "which form the knowledge space of the step.",
           [("factors", Q("The ranges studied form the knowledge space of the step"))])
    nclaim("uni_design", "univariate study", "No parameter of the step was assigned to univariate study, and no "
           "univariate confirmation run was made.",
           [("uni_design", Q("No parameter of this step was assigned to univariate study.")),
            ("uni_design", Q("PCP-009 §6.4 allowed a univariate confirmation run"))])
    nclaim("rsm", "augmentation of the response-surface design", "The step was not augmented: viral clearance is not a "
           "drug substance test, so no further run was spiked with virus, and fragments had no effect to resolve.",
           [("rsm", Q("Viral clearance is not a drug substance test, so no further run was spiked with virus")),
            ("rsm", Q("The step was therefore not augmented."))], elsewhere="INV-002")
    nclaim("mech", "interruption of flow", "The designs did not study an interruption of flow, so the condition of "
           "uninterrupted filtration rests on the mechanism and not on these data.",
           [("mech", Q("Within the pressures studied, pressure had no detected effect on any output")),
            ("cs", Q("An interruption at commercial scale is assessed against the mechanism of the step"))])
    nclaim("mech", "completeness of XMuLV retention", "The data do not show whether XMuLV retention was complete.",
           [("mech", Q("Every LRF in the record is a point value, and the record does not say whether any filtrate titre"))])
    nclaim("mech", "change of fragments across the step", "The expectation that the step does not change fragments "
           "cannot be tested on these data, because fragments were measured in the filtrate and not in the load.",
           [("mech", Q("The expectation that the step does not change fragments cannot be tested on these data"))],
           rationale="It rests on the size of the clipped species against the pores.")
    nclaim("ds", "confirmation of the design space at manufacturing scale", "The design space is not confirmed at "
           "manufacturing scale at its edges, because virus cannot be spiked at that scale.",
           [("ds", Q("The design space is not confirmed at manufacturing scale at its edges"))])
    nclaim("par", "verification of platform worst cases", "No criterion of an earlier step rests on a platform worst case "
           "of the step, so the report has no worst case to verify.",
           [("par", Q("No criterion of an earlier step rests on a platform worst case of this step"))])
    nclaim("par", "range of filtration pressure beyond the range studied", "The PAR of filtration pressure for MVM is the "
           "whole range studied, and no claim is made beyond it.",
           [("par", Q("The PAR of filtration pressure for MVM is the whole range studied in both analyses"))])
    nclaim("par", "PAR of XMuLV LRF", "XMuLV LRF has no adequate model and therefore no PAR; every measured result met "
           "the claim.", [])
    nc_at["par"][-1].source_references = [ref("par", parrow[(LAB_X, NAME[k])], par_t, parrow) for k in FAC]
    nclaim("par", "PAR figures", "Of the PAR figures PCP-009 §8 planned, only the figure of filtration volume for MVM "
           "is given.", [("par", Q("PCP-009 §8 planned a figure for each PAR"))], elsewhere="PD-009-07")
    nclaim("disc", "variation between membrane lots", "Variation between membrane lots was not studied.",
           [("disc", Q("The record names a membrane lot only in DEV-009-02"))])
    nclaim("disc", "events that affected several runs", "The deletion of each response-surface run in turn does not "
           "cover an event that affected several runs, such as the membrane lot of DEV-009-02.",
           [("disc", Q("It does not cover an event that affected several runs, such as the membrane lot"))])

    entities = [
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("exec"), process_steps=[step], sites=sites,
                                  equipment=equipment),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("uo"), document_relationships=rels),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("changes"), non_claims=nc_at["changes"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cqa"), quality_attributes=attrs),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("sdm"), non_claims=nc_at["sdm"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("analytics"), analytical_methods=methods,
                                  non_claims=nc_at["analytics"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("factors"), parameters=params,
                                  non_claims=nc_at["factors"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("uni_design"), non_claims=nc_at["uni_design"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("rsm"), model_fits=fits, non_claims=nc_at["rsm"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("mech"), non_claims=nc_at["mech"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("ds"), non_claims=nc_at["ds"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("par"), contributions=contributions,
                                  non_claims=nc_at["par"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cap"), capabilities=capab),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("disc"), non_claims=nc_at["disc"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("record"), deviations=devs),
    ]

    # ==== studies: each on its row of the execution-window table, its prose, its data rows ======================
    names_fac = [NAME[k] for k in FAC]
    CHR = ns["CHR"]
    study_spec = {
        "S-VF-SDM": dict(study_type="scale_down_qualification",
                         design_name="set-point runs of the scale-down model against manufacturing-scale batches",
                         responses=["step_yield"],
                         prose=[("sdm", Q("The qualification runs were made in study S-VF-SDM")),
                                ("sdm", Q("The study compared `{python} OFF_Y['n_sd']` scale-down runs")),
                                ("sdm", Q("The comparison therefore rests on step yield alone."))],
                         rows=[("sdm", offrow["step_yield"], off_t, offrow),
                               ("analytics", soprow["SOP-1001"], sop_t, soprow)],
                         pds=["PD-009-03"]),
        "S-VF-DOE": dict(study_type="screening_doe", design_name="two-level full factorial with centre points",
                         factors=names_fac, responses=RESP4,
                         n_runs=P.doe_runs(UO, "screening"), n_center_points=P.doe_centre_points(UO, "screening"),
                         prose=[("scr_design", Q("The screening study S-VF-DOE was a two-level full factorial")),
                                ("scr_design", Q("With two factors the full factorial estimates both main effects"))],
                         rows=[("app_a", r_, mtx["screening"][0], mtx["screening"][1])
                               for r_ in mtx["screening"][1].values()],
                         pds=["PD-009-04"]),
        "S-VF-RSM": dict(study_type="response_surface_doe", design_name="face-centred central composite design",
                         factors=names_fac, responses=RESP4,
                         n_runs=P.doe_runs(UO, "rsm"), n_center_points=P.doe_centre_points(UO, "rsm"),
                         prose=[("rsm_design", Q("The response-surface study S-VF-RSM was a face-centred central")),
                                ("rsm_design", Q("The axial runs sit on the edges of the ranges studied"))],
                         rows=[("app_b", r_, mtx["rsm"][0], mtx["rsm"][1]) for r_ in mtx["rsm"][1].values()],
                         pds=["PD-009-04"]),
    }
    studies, unrendered = [], []
    for sid_ in CHR[CHR["step"] == UO].index:
        if sid_ not in winrow or not G._present(winrow[sid_], text):
            unrendered.append(sid_)
            continue
        spec = dict(study_spec[sid_])
        prose_, rows_, pds_ = spec.pop("prose"), spec.pop("rows"), spec.pop("pds")
        refs = [ref("factors", winrow[sid_], win_t, winrow)]
        refs += [ref(s_, x) for s_, x in prose_]
        refs += [ref(s_, r_, tab_, rr_) for s_, r_, tab_, rr_ in rows_]
        refs += [pdref(p_) for p_ in pds_]
        studies.append(S.StudyDesign(
            study_id=f"study:{sid_}", unit_operation=UO_NAME, scale_down_model=SDM_NAME,
            associated_parameters=[PC[x] for x in spec.get("factors", [])],
            source_references=refs, metadata=meta(), **spec))

    # ==== design space and the proven acceptable ranges =====================================================
    q_ds = [Q("The design space of the step is the part of the characterized region"),
            Q("A setting lies inside it when the mean predicted MVM LRF meets its claim"),
            Q("XMuLV LRF has no adequate model and draws no boundary"),
            Q("The points outside are those at"),
            Q("Between the grid points the boundary lies at"),
            Q("The NOR of both parameters lies inside the design space")]
    DSG = ns["DSG"]
    design_spaces = [S.DesignSpace(
        design_space_id="ds:virus_filtration", unit_operation=UO_NAME,
        parameters=[PC[n] for n in names_fac], quality_attributes_constrained=["attr:lrv_mvm", "attr:fragments_lmw"],
        definition=t("The part of the characterized region (`{python} rng_s(RNG_V)` L/m2 by `{python} rng_s(RNG_P)` "
                     "psi) in which every output with a criterion meets it at once, each on the statistic on which it is "
                     "judged (PCMP-001 §6.2): the mean predicted MVM LRF meets its claim and both ends of the 95 % "
                     "prediction interval of a single run for fragments lie within their criterion. Evaluated on a grid "
                     "of `{python} GRID_N` by `{python} GRID_N` points; `{python} DS_IN` of the `{python} DS_N` points "
                     "lie inside, `{python} fx(DS_PCT, 0)` % of the characterized region. The points outside are those "
                     "at the top of the volume range; between grid points the boundary lies at "
                     "`{python} fx(CROSS_V, 1)` L/m2 at every pressure, because the selected model of MVM LRF has no "
                     "pressure term. Fragments exclude no point, and XMuLV LRF, which has no adequate model, draws no "
                     "boundary. The NOR of both parameters lies inside the design space, and the characterized region "
                     "is the knowledge space. With run 5 or run 7 deleted the selected model meets the claim over the "
                     "whole characterized region."),
        source_references=[ref("ds", x) for x in q_ds] + [ref("rsm", delrow[0], del_t, delrow)], metadata=meta())]
    if DSG["binding"] != "mvm_lrf":
        raise ValueError(f"{DOC}: the design space is no longer bounded by MVM LRF, as the text says")

    def basis_of(resp):
        ia = iac_.loc[resp]
        stat = ("the mean predicted LRF at the least favourable combination of NOR low, set-point and NOR high of the "
                "other parameter" if resp == "mvm_lrf" else
                "the 95th percentile of simulated single batches with the other parameter drawn about its set-point")
        return (f"Intermediate acceptance criterion {T.crit(ia['iac_low'], ia['iac_high'], ia['spec_type'])} "
                f"({ia['basis']}) of PCMP-001 Version 2.0; NOR-propagated analysis judged on {stat}, on the selected "
                f"response-surface model.")
    q_par_v = Q("The PAR of filtration volume for MVM ends inside the range studied in both analyses.")
    q_par_v2 = Q("It is `{python} PAR_V_S` L/m2 in the first analysis")
    q_par_f = Q("The selected model of fragments is intercept-only, and its interval lies below the criterion everywhere")
    q_par_p = Q("The PAR of filtration pressure for MVM is the whole range studied in both analyses")
    PT = ns["PT"]
    pars = []
    for (lab_, pname), row in parrow.items():
        if lab_ == LAB_X:
            continue                                   # no adequate model, no PAR (a non-claim)
        resp = {LAB_M: "mvm_lrf", LAB_F: "lmw_cesds_pct"}[lab_]
        c = _cells(row)
        eng = PT[(PT["CQA"] == lab_) & (PT["Parameter"] == pname)].iloc[0]
        if (c[2], c[5], c[6]) != (eng["Char. range"], eng["PAR (set-point)"], eng["PAR (NOR)"]):
            raise ValueError(f"{DOC}: the PAR table no longer prints the engine's ranges for {lab_}, {pname}")
        u = UNIT[pkey[pname]]
        prose_ = ([q_par_v, q_par_v2] if (resp, pname) == ("mvm_lrf", NAME["filtration_volume"]) else
                  [q_par_p] if resp == "mvm_lrf" else [q_par_f])
        pars.append(S.ProvenAcceptableRange(
            par_id=f"{DOC}-PAR{len(pars) + 1:02d}", unit_operation=UO_NAME, quality_attribute=lab_,
            parameter=pname, characterization_range=f"{c[2]} {u}", par_at_setpoint=f"{c[5]} {u}",
            par_nor_propagated=f"{c[6]} {u}", acceptance_basis=basis_of(resp),
            source_references=[ref("par", row, par_t, parrow)] + [ref("par", x) for x in prose_], metadata=meta()))

    # ==== assertions ======================================================================================
    AS = []

    def add(subj, pred, obj, txt, refs):
        AS.append(EvidenceBackedAssertion(
            assertion_id=f"{DOC}-A{len(AS) + 1:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=txt, source_references=refs, metadata=meta()))

    add("step:virus_filtration", "step_uses_equipment", "equip:vf_sdm",
        f"The studies of {UO_NAME} were run on a {SDM_NAME}, which uses the same filter type as manufacturing, with "
        f"the load scaled by membrane area.", [ref("sdm", q_sdm2)])
    for name, row in prow.items():
        add("step:virus_filtration", "step_has_parameter", PC[name],
            f"{UO_NAME} has process parameter {name}, classified {ns['PR'].loc[name, 'Class']}, studied "
            f"multivariately in both designs.", [ref("factors", row, pt_t, prow)])
    role = {"lrv_mvm": "contributes log reduction to the cumulative requirement for {n}, of which it is the principal "
                       "source",
            "lrv_xmulv": "contributes log reduction to the cumulative requirement for {n}",
            "fragments_lmw": "is judged against the drug substance criterion for {n}, because no later step changes them"}
    for key in ckeys:
        add("step:virus_filtration", "step_has_quality_attribute", f"attr:{key}",
            f"{UO_NAME} " + role[key].format(n=names[key]) + "; the attribute is judged at the output of the step "
            "against an intermediate acceptance criterion.", [ref("cqa", crow[key], cq_t, crow)])
    for amv, row in appdrow.items():
        if amv not in method_of.values():
            continue
        out_ = appd_df.loc[appd_df["AMV"] == amv].iloc[0]
        key = {v: k for k, v in method_of.items()}[amv]
        add(f"attr:{key}", "attribute_measured_by_method", f"method:{amv}",
            f"{names[key]} is measured at the step by {out_['Technique'][0].lower() + out_['Technique'][1:]} ({amv}), "
            f"reported as {out_['Reportable value']}.", [ref("app_d", row, appd_t, appdrow)])
    for key in ckeys:
        ic, cr = _cells(irow[key]), _cells(crrow[key])
        ia = iac_.loc[attr_resp[key]]
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{UO}_{key}_iac",
            f"At the small virus retentive filtration step {names[key]} is judged against the Version 2.0 intermediate "
            f"acceptance criterion {_unmark(ic[-2])} ({ia['basis']}), derived from the drug substance criterion "
            f"{_unmark(ic[1])}; met across the NOR: {_unmark(cr[-1])}.",
            [ref("par", irow[key], iac_t, irow), ref("par", crrow[key], cr_t, crrow)])

    # parameter effects: filtration volume on MVM LRF from the coefficient row of the selected model; every
    # other pair on its row of the screening effects table (no term significant), and pressure on XMuLV LRF on
    # its row of the selected model, which is not adequate
    c_a = _cells(cmrow["A"])
    add(PC[NAME["filtration_volume"]], "parameter_impacts_attribute", "attr:lrv_mvm",
        t(f"Filtration volume (A) lowers MVM LRF: coefficient {c_a[1]} log10 per coded unit, p {c_a[4]} in the selected "
          f"model, a fall of `{{python}} fx(-EFF_V)` log10 across the range studied."),
        [ref("rsm", cmrow["A"], cm_t, cmrow), ref("screening", serow[(se_lab["mvm_lrf"], "A")], se_t, serow)])
    for resp, key in (("mvm_lrf", "lrv_mvm"), ("xmulv_lrf", "lrv_xmulv"), ("lmw_cesds_pct", "fragments_lmw"),
                      ("step_yield", "step_yield")):
        for k in FAC:
            if (resp, k) == ("mvm_lrf", "filtration_volume"):
                continue
            lt = LET[k]
            c = _cells(serow[(se_lab[resp], lt)])
            refs = [ref("screening", serow[(se_lab[resp], lt)], se_t, serow)]
            txt = (f"{NAME[k]} ({lt}) on {LAB2[resp]}: screening effect {c[2]} {RUNIT[resp]} across the range studied, "
                   f"p {c[4]}, not significant")
            if (resp, k) == ("mvm_lrf", "pressure"):
                af_ = _cells(afrow[(sel_lab[resp], "B")])
                refs.append(ref("app_c", afrow[(sel_lab[resp], "B")], af_t, afrow))
                txt += f"; in the full quadratic of the planned runs the main effect of pressure has p {af_[4]}"
            if (resp, k) == ("xmulv_lrf", "pressure"):
                as_ = _cells(aselrow[(sel_lab[resp], "B")])
                refs.append(ref("app_c", aselrow[(sel_lab[resp], "B")], asel_t, aselrow))
                txt += f"; the selected model carries pressure (p {as_[5]}) but is not adequate"
            add(PC[NAME[k]], "parameter_does_not_significantly_impact_attribute", f"attr:{key}", txt + ".", refs)

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
    sq("exec", "This report presents the Stage 1 process characterization")
    sq("exec", "It analyses each response-surface output with the model that a model selection chose")
    sq("exec", "Filtration volume was the only parameter with a detected effect.")
    sq("exec", "Across the range studied, from")
    sq("exec", "No term containing filtration pressure was significant for any output.")
    sq("exec", "The selected model of MVM LRF passes the model F-test of PCMP-001 §7.2")
    sq("exec", "It fails the criterion on residuals and influential runs, because one run moves the fit")
    sq("exec", "That run, run 5, is the run at")
    sq("exec", "Fragments and step yield did not depend on either parameter.")
    sq("exec", "Each output with a criterion met its intermediate acceptance criterion across the normal operating range")
    sq("exec", "There the mean predicted MVM LRF is")
    sq("exec", "Every measured XMuLV LRF, from")
    sq("exec", "For fragments the upper 95 % limit of a single run within the NOR is")
    sq("exec", "The proven acceptable range (PAR) of filtration volume for MVM is")
    sq("exec", "The design space covers `{python} fx(DS_PCT, 0)` % of the characterized region on the grid")
    sq("exec", "With run 5 deleted, the PAR of filtration volume and the design space would both reach")
    sq("exec", "The integrated model of the train gives a process capability index (Cpk) of")
    sq("exec", "No simulated batch fell below either cumulative requirement.")
    sq("exec", "Two study events were recorded")
    sq("exec", "Every run concerned was retained in the analysis, as Version 1.0 recorded")
    sq("exec", "The register of discrepancies holds")
    sq("exec", "Two concern the analysis, the model selection (PD-009-01)")
    sq("exec", "Four record results and comparisons that PCP-009 required")
    sq("exec", "The last records the analyses that the plan does not contain")

    # -- Introduction: objectives (PCP-009 §2, read from the numbered list of the .qmd) and changes ------------
    src_all = _source()
    obj_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n## Objectives", 1)[1].split("\n## ", 1)[0], flags=re.M)
    if len(obj_list) != 5:
        raise ValueError(f"{DOC}: {len(obj_list)} numbered objectives under '## Objectives', the text says five")
    sq("objectives", "The objectives of the study were those of PCP-009 §2.")
    for i, obj in enumerate(obj_list, 1):
        st("objectives", f"Objective {i} of PCP-009 §2: {clean(q(obj))}", [ref("objectives", q(obj))])
    sq("objectives", "Version 2.0 of the plan adds fragments to objectives 2 to 4.")
    sq("objectives", "The response-surface model is the predictive model, and every range in this report comes from it.")
    sq("uo", "The commercial process runs at a production bioreactor scale of")
    sq("uo", "The clearance of the step is orthogonal to that of low-pH viral inactivation", "removes virus by size and "
       "not by inactivation or by binding")
    sq("uo", "Step yield is a process performance output with no criterion.")
    sq("basis", "The study belongs to Stage 1, process design, of the lifecycle approach", "of the lifecycle approach "
       "to process validation")
    sq("basis", "Viral clearance is evaluated under ICH Q5A(R2).")
    sq("changes", "INV-001 found that the criteria used to judge each step in the PAR analysis")
    sq("changes", "They were applied at analysis and appear in no approved plan.")
    sq("changes", "Acceptance criteria. MVM LRF and XMuLV LRF are each judged against the platform claim")
    sq("changes", "Version 1.0 judged them against the rule", "against the rule",
       txt="Version 1.0 judged MVM LRF and XMuLV LRF against the rule `{python} R1_RULE`, which gave "
           "`{python} fx(R1_M)` for MVM and `{python} fx(R1_X)` for XMuLV.",
       extra=[("changes", "which gave `{python} fx(R1_M)` for MVM")])
    sq("changes", "Fragments are added as an output, with the drug substance criterion of")
    sq("changes", "Fragment method. Fragments are measured by non-reduced capillary electrophoresis")
    sq("changes", "Statistic that decides the verdict. Viral clearance is judged on the mean predicted LRF")
    sq("changes", "Version 1.0 judged every output on a 95 % interval for a single batch")
    sq("changes", "Models. Each response-surface output is analysed by the model selection that INV-002 adopted")
    sq("changes", "Under it XMuLV LRF has no adequate model and is judged on its measured results")
    sq("changes", "Scale-down model. The model is qualified by its offset from manufacturing scale")
    sq("changes", "Record. The execution window of every study is now given")
    sq("changes", "The data, the designs, the NOR and the set-points of the step did not change.")
    sq("changes", "Recomputed under the Version 1.0 criteria, statistic and model")
    sq("changes", "Under Version 2.0 they are")

    # -- Prior knowledge and quality risk basis ----------------------------------------------------------
    sq("platform", "Their history gives the platform claim of the step")
    sq("platform", "How the anion exchange pool of A-Mab fouls the membrane is specific to the product")
    sq("platform", "MVM retention is therefore expected to fall as the volume filtered per unit area rises")
    sq("platform", "PCP-009 §6.3 also expected the fall to accelerate toward the top of the volume range")
    sq("platform", "PCP-009 expected MVM retention to fall at high pressure")
    sq("platform", "On that reasoning the plan expected the fall of MVM retention with load to be steeper")
    sq("platform", "It is retained while the membrane is intact, so its clearance is expected not to depend")
    sq("platform", "PCP-009 expected yield to be high and to fall slowly as the load rises.")
    sq("cqa", "The acceptance values of the two viral safety attributes are cumulative requirements")
    sq("cqa", "They are met by the claims of several steps together and cannot be applied to one step.")
    sq("cqa", "The cumulative MVM requirement of")
    sq("cqa", "The sponsor set the criterion of")
    for key, row in crow.items():
        c = _cells(row)
        srow("cqa", f"{names[key]}: drug substance criterion {c[2]}, criticality {c[3]}, Tool #1 score {c[4]}.", row,
             cq_t, crow)
    sq("risk", "Parameters ranked high on either ranking were assigned to multivariate study")
    sq("risk", "Filtration volume was ranked high because fouling shifts the flow to the larger pores")
    sq("risk", "Filtration pressure was ranked high because a loss of pressure or a stop of flow")
    sq("risk", "No parameter of the step was left out of the study on prior knowledge alone")

    # -- Materials and methods --------------------------------------------------------------------------
    sq("sdm", "PCP-009 §5.1 named three outputs for this comparison")
    sq("sdm", "The record holds step yield alone.")
    sq("sdm", "The flux decay profile and the post-use integrity test results are not recorded for either scale")
    sq("sdm", "The model is qualified by the offset rule of PCMP-001 §7.1.")
    sq("sdm", "The model is qualified for an output when the conclusion against its criterion over the NOR is the same")
    sq("sdm", "Step yield has no criterion at this step, so its offset is recorded")
    sq("sdm", "The mean step yield was")
    c = _cells(offrow["step_yield"])
    srow("sdm", f"Scale-down model offset of step yield (scale-down minus manufacturing scale): {c[5]} percentage points, "
                f"{ns['OFF_CI']:g} % confidence interval {c[6]}; {_unmark(c[7])}; qualification {_unmark(c[8])}.",
         offrow["step_yield"], off_t, offrow)
    sq("sdm", "Virus cannot be spiked into a manufacturing batch, so every clearance figure of this report comes from",
       "rests on the spiking model")
    sq("sdm", "No output with a criterion therefore has a measured offset")
    sq("operation", "PCP-009 §5.2 specifies the flow-through pool of anion exchange as the load of every run")
    sq("operation", "Each design point was run once")
    sq("operation", "Both model viruses were spiked into the load of every run")
    sq("operation", "PCP-009 §5.4 asked instead for an unspiked load and an unspiked filtrate pool")
    sq("operation", "The record gives the yield of each spiked run as a single value.")
    sq("operation", "PCP-009 §5.2 required the filter of each run to be integrity tested before and after the run")
    sq("operation", "No integrity test result is recorded for any design run (PD-009-04), and no run was excluded.")
    sq("operation", "The claim made from these runs applies to uninterrupted filtration")
    sq("analytics", "The LRF of a run is the base-ten logarithm of the total virus in the spiked load")
    sq("analytics", "The record holds one LRF per run for each virus.")
    sq("analytics", "It does not hold the titres of the spiked load and the filtrate")
    sq("analytics", "Every LRF in the record is a point value. Whether", "Every LRF in the record is a point value.")
    sq("analytics", "Both designs ran after the method decision AMD-001")
    sq("analytics", "The method has a limit of quantitation of")
    sq("sampling", "PCP-009 §5.4 planned samples of the load before spiking")
    sq("sampling", "The record holds one result per run for each output")
    sq("sampling", "The log reduction therefore cannot be resolved against the volume filtered within a run")
    sq("stats", "Both factors were coded to −1 and +1 at the ends of the range studied")
    sq("stats", "A coded coefficient is the change in the response over half the range studied")
    sq("stats", "Terms significant at α =")
    sq("stats", "An effect is twice the coded coefficient")
    sq("stats", "The screening model identifies effects.")
    sq("stats", "Each response-surface output was analysed by model selection")
    sq("stats", "Every interval at this step contained both 0 and 1")
    sq("stats", "Every submodel was fitted, and the one with the lowest AICc was selected.")
    sq("stats", "On these data a stepwise search in either direction would have stopped at the same model")
    sq("stats", "An intercept-only model states that the output does not depend on the parameters")
    sq("stats", "An output with no adequate model is judged on its measured results and sets no range.")
    sq("stats", "The model fails the criterion only where a run's Cook's distance exceeds the median of the F")
    sq("stats", "Normality is judged on the normal quantile plot and by the Shapiro-Wilk test")
    sq("stats", "Several analyses of this report are not in PCP-009 (PD-009-07).")
    sq("stats", "Viral clearance was judged on the mean predicted LRF at the least favourable of these combinations")
    sq("stats", "Fragments were judged on the exact 95 % prediction interval of a single run at each combination")
    sq("stats", "No offset was applied, because no output with a criterion has a measured offset at this step")
    sq("stats", "Capability was estimated from the integrated model of the train (PCMP-001 §6.5)")

    # -- Study design ---------------------------------------------------------------------------------------
    for name, row in prow.items():
        c = _cells(row)
        srow("factors", f"{name} (code {c[0]}): set-point {c[3]} {c[2]}, NOR {c[4]} {c[2]}, range studied {c[5]} "
                        f"{c[2]}.", row, pt_t, prow)
    sq("factors", "The NOR and the set-points were not changed at Version 2.0")
    sq("factors", "It was widened upward only, because MVM retention was expected to fall as the load rises")
    sq("factors", "Low pressures were included because a low pressure was expected to let retained virus diffuse")
    sq("factors", "Each window runs from the first to the last day of runs of its study")
    sq("factors", "The record names no instrumented system under calibration and change control")
    sq("scr_design", "The interaction model fits four parameters to")
    sq("scr_design", "The one degree of freedom left for lack of fit tests for curvature.")
    sq("rsm_design", "The design supports the full quadratic model in both factors.")

    # -- Results ----------------------------------------------------------------------------------------------
    sq("centre", "In the response-surface design the SD of the four centre points was")
    sq("centre", "The three MVM centre points of the screening design spread more widely")
    sq("centre", "The variance of the centre points of each design is its pure error")
    for (dsg, rlab), row in cenrow.items():
        c = _cells(row)
        srow("centre", f"{dsg} design, centre points of {rlab}: n {c[2]}, mean {c[3]}, SD {c[4]}, CV {c[5]} %.", row,
             cen_t, cenrow)
    sq("screening", "Filtration volume had the only significant effect in the screening design")
    sq("screening", "Raising it from")
    sq("screening", "The effect of pressure on MVM LRF")
    sq("screening", "The F-test of the whole screening model of MVM LRF gave")
    sq("screening", "No term was significant for XMuLV LRF, fragments or step yield.")
    sq("screening", "The centre points of the screening design showed curvature for fragments.")
    sq("screening", "The three centre points read")
    sq("screening", "In the response-surface design the four centre points read")
    sq("screening", "The difference between the two estimates")
    sq("screening", "In size both estimates are at most")
    sq("screening", "No other response showed curvature in the screening design")
    sq("screening", "The screening results identify the effects, and the response-surface design gives the predictive")
    sq("rsm", "Its R² exceeded its predicted R² by")
    sq("rsm", "Its adjusted R² was")
    sq("rsm", "INV-002 named a refit as the remedy for each of them.")
    sq("rsm", "The model selection gave a straight line in filtration volume for MVM LRF")
    sq("rsm", "The Box-Cox interval of λ contains both 0 and 1, so the raw scale was kept.")
    sq("rsm", "The intercept, ")
    sq("rsm", "The coefficient of filtration volume is")
    sq("rsm", "Across the range studied the mean LRF therefore falls by")
    sq("rsm", "The model F-test is significant (")
    sq("rsm", "The residual SD of the model is")
    sq("rsm", "The residuals show no departure from normality (Shapiro-Wilk `{python} pv(SW['mvm_lrf'])`")
    sq("rsm", "The next model by AICc adds the main effect of pressure")
    sq("rsm", "Neither residual trend is significant")
    sq("rsm", "Runs 2 and 5 have a Cook's distance above")
    sq("rsm", "Run 5 is an axial run at the lowest filtration volume")
    sq("rsm", "Its LRF, ")
    sq("rsm", "Its leverage, ")
    sq("rsm", "Run 2, a factorial run at the lowest volume and the highest pressure")
    sq("rsm", "Both flagged runs were deleted in turn")
    sq("rsm", "Every other run of the design was deleted in the same way")
    sq("rsm", "Every deletion leaves filtration volume as the only term of the selected model")
    sq("rsm", "The deletion of run 5 flattens the line")
    sq("rsm", "The NOR-propagated PAR of filtration volume then reaches the end of the range studied")
    sq("rsm", "The deletion of run 2 steepens the line to")
    sq("rsm", "With run 3 or run 7 deleted, the Box-Cox interval of the remaining runs excludes 1")
    sq("rsm", "Across the single deletions the upper PAR edge of filtration volume lies between")
    sq("rsm", "No deletion changes the judgement over the NOR, and the NOR lies")
    sq("rsm", "The model of all runs, which gives a narrower range of volume than the model without run 5")
    for i, row in delrow.items():
        c = _cells(row)
        lead = "No run deleted" if c[0] == "none" else f"Run {_unmark(c[0])} ({c[1]}, Cook's distance {c[2]}) deleted"
        srow("rsm", f"{lead}: {c[3]} scale; mean LRF at the least favourable NOR combination {_unmark(c[4])} log10; "
                    f"upper edge of the NOR-propagated PAR of filtration volume {c[5]} L/m2; design space {c[6]} % of "
                    f"the grid.", row, del_t, delrow)
    sq("rsm", "XMuLV LRF is therefore judged on its measured results, all")
    sq("rsm", "The intercept-only model lies")
    sq("rsm", "It predicts a mean LRF of")
    sq("rsm", "The lack of fit is not significant (`{python} pv(FF['p_lof'])`)")
    sq("rsm", "Both conditions kept from Version 1.0, normal residuals and a residual SD small")
    sq("rsm", "For an intercept-only model R² is zero")
    sq("rsm", "Run 9, a centre run, has a Cook's distance of")
    sq("rsm", "The deletion of run 9, or of any other single run, leaves an intercept-only model")
    sq("rsm", "Fragments would then have no adequate model and no PAR")
    sq("rsm", "The judgement over the NOR, the range carried into the control strategy")
    sq("rsm", "The model with filtration volume lies")
    sq("rsm", "The MVM LRF falls with volume at every pressure of the response-surface design")
    st("rsm", "Figure caption: the measured results of both designs against filtration volume, with the claim or "
              "criterion of each output and the NOR shaded.", [ref("rsm", fig_cap("fig-measured", 1),
                                                                      label="fig-measured")])
    sq("mech", "The fall of MVM LRF with filtration volume is the effect that the mechanism of the step predicts.")
    sq("mech", "As the membrane fouls, the flux shifts toward the largest pores")
    sq("mech", "The data show the effect as a fall of")
    sq("mech", "The data do not show three other effects that PCP-009 expected from the same mechanism.")
    sq("mech", "In the full quadratic of the planned runs the square of filtration volume is positive")
    sq("mech", "Within `{python} rng_s(RNG_V)` L/m2 the decline is consistent with a straight line")
    sq("mech", "The main effect of pressure in the full quadratic is")
    sq("mech", "The square of pressure is negative")
    sq("mech", "The interaction in the full quadratic is")
    sq("mech", "Within the range studied no dependence of the volume effect on pressure was detected")
    sq("mech", "A term that is not significant is not shown to be absent")
    sq("mech", "For operation, the MVM LRF is therefore lowest at the highest volume filtered")
    sq("mech", "The results for XMuLV LRF agree with the expectation")
    sq("mech", "Fragments did not depend on either parameter, and their level in the filtrate ranged from")
    sq("mech", "The model with filtration volume, the next by AICc, falls with load as PCP-009 expected")
    sq("mech", "The data therefore do not show whether the loss in the fouling layer grows faster")

    # -- Design space -----------------------------------------------------------------------------------------
    sq("ds", "Of the `{python} DS_N` grid points")
    sq("ds", "Fragments exclude no point.")
    sq("ds", "Drawn on the mean prediction of fragments as well, the design space is the same")
    sq("ds", "Movement within the design space is not a change from the point of view of a regulatory filing",
       "a change from the point of view of a regulatory filing under ICH Q8(R2), but it is evaluated under the change "
       "management system of the quality system")
    sq("ds", "At the boundary itself a single run meets the claim only about half the time")
    sq("ds", "At the least favourable NOR combination the lower end of the two-sided 95 % prediction interval")
    sq("ds", "Deleting run 5, the axial run at")
    sq("ds", "The selected model of step yield is intercept-only, so the predicted mean yield is")

    # -- Proven acceptable ranges ---------------------------------------------------------------------------
    sq("par", "Each output of the step with a criterion is judged against its intermediate acceptance criterion")
    sq("par", "MVM LRF and XMuLV LRF are each held to the platform claim of this step")
    sq("par", "The claims of the steps that clear each virus are summed and checked against the cumulative requirement")
    sq("par", "The LRF claimed for this step is therefore one of three claims for XMuLV and one of two for MVM.")
    sq("par", "Each step is judged against its own claim, so a shortfall at this step is not made up by another step.")
    sq("par", "Fragments carry the drug substance criterion")
    for key, row in irow.items():
        c = _cells(row)
        srow("par", f"Intermediate acceptance criterion of the step for {names[key]}: {_unmark(c[-2])}, basis "
                    f"{_unmark(c[-1]).lower()}, from the drug substance criterion {_unmark(c[1])}.", row, iac_t, irow)
    sq("par", "The criteria of this step were derived without its data.")
    sq("par", "The criteria in force equal their values derived in this way, because no verification changed them.")
    sq("par", "The fragment criteria of the earlier steps do assume that no later step changes fragments")
    sq("par", "That assumption rests on the mechanism of the step")
    sq("par", "MVM LRF met its claim, with a mean predicted LRF of")
    sq("par", "XMuLV LRF met its claim on its measured results.")
    sq("par", "Fragments met their criterion, with an upper 95 % limit of a single run of")
    for key, row in crrow.items():
        c = _cells(row)
        srow("par", f"{names[key]} against its criterion {c[1]} over the NOR: at the set-point {_unmark(c[2])}, range "
                    f"over the NOR {_unmark(c[3])}, 95 % limits of a single run over the NOR {_unmark(c[4])}; met "
                    f"across the NOR: {c[5]}.", row, cr_t, crrow)
    sq("par", "Two analyses give the PAR of each parameter for each output with a criterion and an adequate model")
    sq("par", "The first scans the parameter across its range studied on a grid of")
    sq("par", "The second is the NOR-propagated analysis of PCMP-001 §6.4.")
    sq("par", "For viral clearance the other parameter is set at each grid point to its NOR low")
    sq("par", "The range reported is the contiguous range that contains the set-point")
    sq("par", "An output with no adequate model has no PAR")
    sq("par", "The mean prediction crosses the claim at")
    sq("par", "Below that volume the selected model predicts a mean LRF above the claim at every pressure")
    sq("par", "The NOR of filtration volume,")
    sq("par", "The lower edge of the PAR is the lower end of the range studied")
    sq("par", "Across the PAR the mean predicted LRF falls from")
    sq("par", "The two panels give nearly the same edge, because the selected model has no pressure term.")
    st("par", "Figure caption: the proven acceptable range of filtration volume for MVM LRF, the first analysis (left) "
              "and the NOR-propagated analysis (right), with the claim of the step and the NOR.",
       [ref("par", fig_cap("fig-par-mvm", 1), label="fig-par-mvm")])
    sq("par", "With two parameters and no interaction term in any selected model")
    sq("par", "The design space is the characterized region below the volume at which MVM LRF crosses its claim")
    sq("par", "A movement of filtration volume within its PAR keeps the step inside the design space")

    # -- Process capability and robustness -----------------------------------------------------------------------
    sq("cap", "Capability at commercial scale was estimated from the integrated model of the train")
    sq("cap", "The capability of the cumulative clearance therefore depends on those steps as well as on this one.")
    sq("cap", "Both are above the target of")
    sq("cap", "No simulated batch fell outside any of the three criteria.")
    sq("cap", "With none of")
    sq("cap", "That bound covers the sampling of the simulation and not the uncertainty")
    sq("cap", "The tail of a normal distribution with the simulated mean and SD gives")
    sq("cap", "Within this step, the claim is judged on the response-surface model")
    sq("cap", "The capability adds the variation of the parameters within their NOR")

    # -- Parameter classification -------------------------------------------------------------------------------
    sq("class", "The parameters were classified under SOP-4001.")
    sq("class", "Under the rule of PCP-009 §7 a parameter affects an attribute when a term")
    sq("class", "Neither PCMP-001 nor SOP-4001 sets a number for either.")
    sq("class", "The class of filtration volume below is therefore a judgement on the values given.")
    sq("class", "With run 5 deleted the PAR would reach the end of the range studied, and the class would be the same.")
    sq("class", "The step has two critical process parameters, both of the well-controlled kind.")
    sq("class", "Neither parameter had a detected effect on step yield.")

    # -- Contribution to the control strategy -------------------------------------------------------------------
    sq("cs", "The step contributes two parameter ranges, a condition of operation")
    sq("cs", "Filtration volume is held within its NOR of")
    sq("cs", "Filtration pressure is held within")
    sq("cs", "The range carried into the control strategy for each parameter is the intersection of its PARs")
    sq("cs", "For both parameters that is the PAR for MVM LRF")
    sq("cs", "Filtration is uninterrupted, because the claim does not cover an interruption of flow.")
    sq("cs", "Each filter is integrity tested after use under SOP-2012.")
    sq("cs", "The post-use test of a parvovirus filter is designed to detect a loss of small virus retention.")
    sq("cs", "Viral clearance cannot be tested on a batch, so the claim rests on the operation of the step")
    sq("cs", "Fragments are tested at release of the drug substance by nrCE-SDS against the criterion of")

    # -- Discussion -----------------------------------------------------------------------------------------------
    sq("disc", "As the volume filtered per square metre rises, the membrane fouls")
    sq("disc", "The study measured this fall as a straight line from")
    sq("disc", "The claim of `{python} fx(CL_M)` log10 holds on the mean prediction up to")
    sq("disc", "The `{python} N_BELOW` measured MVM results below the claim")
    sq("disc", "The scale-down model compared step yield alone with manufacturing scale")
    sq("disc", "The clearance claims therefore rest on the spiking model, as ICH Q5A(R2) provides",
       "and the fragment results on the mechanism of the step")
    sq("disc", "How far the fouling of the scale-down membrane represents the commercial filter")
    sq("disc", "Deleting run 5 or run 7 carries the upper PAR edge")
    sq("disc", "The ranges reported come from all runs and are the narrower ones.")
    sq("disc", "Under every deletion the edge lies")
    sq("disc", "The residual SD of a model sets the standard errors of its terms.")
    sq("disc", "For the selected model of MVM LRF it is")
    sq("disc", "In the full quadratic of the planned runs the terms that PCP-009 expected have standard errors")
    sq("disc", "Effects of that size are not resolved by")
    sq("disc", "The record lacks several results that PCP-009 required")
    sq("disc", "The record holds no spike titre and no limit of detection")
    sq("disc", "It also holds no integrity test result for any run")

    # -- Conclusions (the numbered list of the .qmd) ----------------------------------------------------------
    con_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n# Conclusions", 1)[1].split("\n# ", 1)[0], flags=re.M)
    if len(con_list) != 10:
        raise ValueError(f"{DOC}: {len(con_list)} numbered conclusions, the report has ten")
    for i, con in enumerate(con_list, 1):
        # a conclusion is several sentences; its statement anchors on its first sentence
        first = S_(con[:40])
        st("concl", f"Conclusion {i}: {clean(q(con))}", [ref("concl", q(first))])

    # -- Study events and discrepancies from the plan -------------------------------------------------------------
    sq("record", "PCP-009 calls a departure from the plan a deviation.")
    sq("record", "This report records the events of execution that Version 1.0 recorded as study events")
    sq("events", "It recorded that every run concerned in either event was retained in the analysis.")
    sq("events", "The record does not name the runs, so no run can be analysed at its recorded conditions")
    sq("events", "Every run of the response-surface design was therefore deleted in turn")
    sq("events", "Nor does it cover the screening runs")
    sq("dev1", "Version 1.0 recorded the peak as an excursion above the NOR")
    sq("dev1", "The reference for an excursion is the set pressure of the run")
    sq("dev1", "An overshoot rises above the set pressure, so the run was set below")
    sq("dev1", "The peak lies inside the range studied")
    sq("dev2", "The record names the MVM infectivity method")
    sq("dev2", "Version 1.0 recorded that every run made on the lot was retained.")
    sq("dev2", "A lower permeability lowers the flux at a given pressure.")
    for pid, row in pdrow.items():
        d = PDS[pid]
        srow("pds", f"Discrepancy {pid} from PCP-009, {d['subject']}: planned {d['planned']}; done {d['done']}; reason "
                    f"{d['reason']}.", row, rows_=pdrow, caption=pd_cap, label="tbl-discrepancies")
    sq("pds", "The full quadratic that PCP-009 planned failed the limit on overfitting for every output")
    sq("pds", "Under the plan no output with a criterion would therefore have had an adequate model.")
    sq("pds", "This report compared the criteria that the verification gives with the full quadratic models")
    sq("pds", "For this step they are the same, and so are the judgement of each output over the NOR")
    sq("pds", "The PARs and the design space of MVM LRF come from the model of all runs.")
    sq("pds", "No conclusion of this report depends on the qualification")
    sq("pds", "Without the flux decay profile, whether the scale-down membrane fouls like the commercial filter")
    sq("pds", "The record cannot show that each membrane was intact")
    sq("pds", "No run was excluded for a failed integrity test, because no test result is recorded.")
    sq("pds", "The record names no method for the step yield")
    sq("pds", "Whether the spiked load fouled the membrane differently from unspiked process material is not shown.")
    sq("pds", "PCP-009 §12 named that bias as largest at the top of the volume range")

    sections = []
    for chap in CHAPTERS:
        stmts = [x for c_, x in STS if c_ == chap]
        if stmts:
            sections.append(ReportSection(section_id=f"{DOC}-sec{len(sections) + 1:02d}", title=chap,
                                          statements=stmts))
    if sum(len(s_.statements) for s_ in sections) != len(STS):
        raise ValueError(f"{DOC}: statements outside the chapters of the report")

    # ==== concepts ===========================================================================================
    concepts = [Concept(concept_id="step:virus_filtration", concept_type="PROCESS_STEP", canonical_name=UO_NAME,
                        aliases=["small virus retentive filtration", "virus filtration", P.DOC_REGISTRY[DOC][1],
                                 f"Step {G.VFSTEP}"],
                        review_status="human_verified")]
    alias = {"filtration_volume": ["filtration volume", "load", "volumetric load"],
             "pressure": ["pressure", "filtration pressure"]}
    concepts += [Concept(concept_id=PC[NAME[k]], concept_type="PROCESS_PARAMETER", canonical_name=NAME[k],
                         aliases=alias[k], review_status="human_verified") for k in FAC]
    concepts += G._attr_concepts(ckeys)
    concepts.append(Concept(concept_id="attr:step_yield", concept_type="PERFORMANCE_ATTRIBUTE",
                            canonical_name="Step yield", aliases=["step yield", "yield"],
                            review_status="human_verified"))
    concepts += G._method_concepts([m.method_id for m in methods], amv_title)
    concepts.append(Concept(concept_id="equip:vf_sdm", concept_type="EQUIPMENT", canonical_name=SDM_NAME,
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
            "No set-point or NOR of the step changed at Version 2.0, so ProcessParameter.target_value and NOR are the "
            "values of the parameter table, which are also the values in force. ProcessParameter.PAR is the "
            "NOR-propagated PAR for MVM LRF, the range carried into the control strategy (PCMP-001 §7.6), which is "
            "also the intersection over the outputs with an adequate model. rationale_for_criticality carries the "
            "classification argument of the report, each parameter anchored on its own sentences of it.",
            "The step forms no quality attribute. The QualityAttribute records are the two cumulative viral clearance "
            "attributes, to which the step contributes log reduction, and fragments, against whose drug substance "
            "criterion its filtrate is judged. acceptance_criteria holds the drug substance criterion of the CQA "
            "register and the Version 2.0 intermediate acceptance criterion of the step; acceptance_criteria (the "
            "annex layer) holds the rows of the criteria-change table, Version 1.0 superseded and Version 2.0 in "
            "force. Step yield is a process performance output with no criterion: the concept attr:step_yield.",
            "proven_acceptable_ranges: the rows of the PAR table for MVM LRF and fragments, with par_at_setpoint and "
            "par_nor_propagated as the columns 'PAR (set-point)' and 'PAR (NOR)' print them, and the report's "
            "description of the two analyses in its own words, in report statements anchored on its sentences. "
            "XMuLV LRF has no adequate model and no PAR: its two rows (n.a.) anchor an explicit non-claim.",
            "The schema has no record type for a discrepancy from the plan. PD-009-01 to PD-009-07 are report "
            "statements anchored on their rows of the discrepancy register; the studies they concern carry that row "
            "as a source reference.",
            "The report records no deviation: a characterization study is not GMP manufacture, so the two events of "
            "execution are study events, under the numbers Version 1.0 gave them (DEV-009-01, DEV-009-02). They are "
            "Deviation records, the schema's only record type for an event of execution. no_impact_on_conclusions is "
            "true for DEV-009-01, which the report bounds in every case the record leaves open, and false for "
            "DEV-009-02, whose effect the report says cannot be assessed from the record.",
            "Studies: every row of the execution-window table has a StudyDesign record. Only the two designs carry "
            "n_runs, which the corpus test reserves for the seeded DoE designs. The qualification compares step yield "
            "alone; the flux decay profile and the post-use integrity test it was planned to compare are not "
            "recorded (PD-009-03).",
            "StatisticalModelFit: the planned full quadratic of each output with a criterion (the re-evaluation table, "
            "with the terms of Appendix C), the selected models of MVM LRF (passes the first three adequacy criteria, "
            "fails the criterion on residuals and influential runs, used for the ranges and the design space, "
            "PD-009-02), of XMuLV LRF (not adequate), of fragments and of step yield (intercept-only), and the four "
            "screening models. A p-value printed as '< 0.001' has no float value; its term carries significant=true. "
            "The deletion of every response-surface run in turn is in report statements, one per row of the deletion "
            "table.",
            "parameter_impacts_attribute: filtration volume on MVM LRF, on its row of the coefficient table of the "
            "selected model. parameter_does_not_significantly_impact_attribute: every other parameter and output on "
            "its row of the screening effects table, with the full quadratic row for pressure on MVM LRF and the row "
            "of the selected (not adequate) model for pressure on XMuLV LRF.",
            "The ModularContribution records are the platform claims of the step against the two cumulative "
            "requirements; cumulative_value is the sum of the platform claims the report states, not a measured "
            "clearance. The capability of the cumulative clearance is a property of the train.",
            "The equipment id equip:vf_sdm follows the Version 1.0 report and the PCP-009 Version 2.0 annex.",
            "rhetorical_spans: authoring/rhetorical/PCR-009.spans.yaml, re-curated against the Version 2.0 text in the "
            "same pass as this builder. weak_claims is empty.",
        ] + G._unrendered_note(unrendered),
        inventory=G.rev2_inventory(DOC, FILE, "process_characterization_report", UO_NAME,
                                   ["process characterization", "small virus retentive filtration", "viral clearance",
                                    "MVM and XMuLV log reduction", "intermediate acceptance criteria",
                                    "modular viral clearance claim", "design of experiments", "model selection",
                                    "influential runs", "scale-down model qualification", "parameter classification"]),
        entities=entities, studies=studies, design_spaces=design_spaces, proven_acceptable_ranges=pars,
        report_sections=sections, assertions=AssertionStore(run_id=f"gt-{DOC}", assertions=AS, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{DOC}", concepts=concepts),
        weak_claims=[], rhetorical_spans=G.build_rhetorical_spans(DOC, FILE),
        acceptance_criteria=G.acceptance_criteria_layer(DOC, FILE, title("changes"), ct["tbl-criteria-change"][0],
                                                        [UO]))
    _gate(annex, text)
    return annex
