"""PCR-004 Version 2.0, the characterization report of harvest and clarification (Step 4), re-analysed
under INV-001: its ground-truth annex (``build()``).

Harvest runs no designed experiment. Its three parameters were studied one factor at a time in the
univariate study S-HAR-UNI2, made during the Version 2.0 re-analysis, and the clarified harvest was held
in the hold study S-HAR-HLD. PCMP-001 Table 7.1 sets no intermediate acceptance criterion for the
clarified harvest and Version 1.0 applied none, so the report prints no criteria-change table.

The kinds of record follow the Version 2.0 report builder ``annex_builders/pcr_006.py`` (the pattern of
structure and helper use), less what a step without a design does not have (a design space, response-
surface models, a modular contribution), and plus what a harvest report is made of: the linear
regressions of S-HAR-UNI2 (one ``StatisticalModelFit`` per regression), the performance measures of the
step (centrate turbidity, post-clarification turbidity, step yield) and the contributions of the step to
the control strategy. The concept ids are those of the Version 1.0 builder of this report and of the
Version 2.0 builder of its plan (``annex_builders/pcp_004.py``): ``step:harvest_clarification``, the
three ``param:`` ids of ``build_ground_truth.HPARAM_CONCEPT``, ``equip:clarification_sdm``,
``equip:disk_stack_centrifuge``, ``equip:depth_filter`` and ``equip:sterilizing_grade_filter``.

Every table of the report is a complex table (``T.frame`` or a ``T.`` builder), read back through
``qmd_ctables`` from the object the report printed, or a markdown string of a ``_pcpkg`` helper
(``dev_register``, ``discrepancy_register``), read back with ``md_string_rows``, so each row quote is the
rendered row, with ``table_header=rows.header``. Every prose quote is a span of the ``.qmd`` copied with
its inline expressions and rendered as the ``.docx`` reads it (the inline expressions evaluated in the
report's own namespace, a cross-reference resolved to its rendered number, typographic quotes), so no
value is typed here. ``q`` refuses a snippet that is not a span of the ``.qmd`` prose or that crosses a
citation, and ``build()`` refuses to return an annex with a quote that does not ground or a weak anchor.
"""
from __future__ import annotations

import os
import re

import _pcpkg as P
import build_ground_truth as G
import schema_ext as S
from check_grounding import normalize, specificity_report

DOC = "PCR-004"
FILE = G.PCR4_FILE                                   # "PCR-004_harvest.docx"
QMD = "PCR-004_harvest.qmd"
UO = "harvest"

#: Concept ids kept from the Version 1.0 builder of this report and the Version 2.0 builder of PCP-004.
STEP_ID = "step:harvest_clarification"
SDM_ID = "equip:clarification_sdm"
CENTRIFUGE_ID = "equip:disk_stack_centrifuge"
DEPTH_ID = "equip:depth_filter"
STERILE_ID = "equip:sterilizing_grade_filter"

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
    "uni_design": (_SD, "Univariate assessment"),
    "hold_design": (_SD, "Hold study of the clarified harvest"),
    "repro": (_RES, "Set-point reproducibility"),
    "rcf": (_RES, "Centrifugation (rcf)"),
    "dfl": (_RES, "Depth filter load"),
    "turb": (_RES, "Post-clarification turbidity"),
    "attrs": (_RES, "Quality attributes across the three series"),
    "hold": (_RES, "Hold-time stability of the clarified harvest"),
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
    "dev1": (_REC, _EV, "DEV-004-01, depth filter flush turbidity above its alert limit"),
    "dev2": (_REC, _EV, "DEV-004-02, post-clarification turbidity above the NOR on one run"),
    "pds": (_REC, "Discrepancies from the plan"),
    "app_a": ("Appendix A. Individual results of S-HAR-UNI2",),
    "app_b": ("Appendix B. Regression details",),
    "app_c": ("Appendix C. Analytical methods summary",),
}
#: The report's statements are grouped by the chapters of the report, in this order.
CHAPTERS = ["Executive summary", _INTRO, _PRIOR, _MM, _SD, _RES, "Design space", "Proven acceptable ranges",
            "Process capability and robustness", "Parameter classification",
            "Contribution to the control strategy", "Discussion", "Conclusions", _REC,
            "Appendix A. Individual results of S-HAR-UNI2", "Appendix B. Regression details",
            "Appendix C. Analytical methods summary"]


# --------------------------------------------------------------------------- #
# Local helpers. _check_sections, _xrefs, _smart, _cells, _unmark, _num, _walk #
# and _gate follow annex_builders/pcr_006.py; _xrefs also reads the caption of #
# a markdown table printed as ``print(": <caption> {#tbl-...}")``.             #
# --------------------------------------------------------------------------- #
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
    """``{label -> rendered cross-reference}`` ("sec-stats" -> "Section 3.5", "tbl-par" -> "Table 11").

    A section number follows the numbering of the headings (an unnumbered heading takes none). A table or
    figure number is read off the rendered caption ("Table 11: <caption>"), with the caption taken from the
    chunk that prints it: a complex table's own caption, the ``fig-cap`` option of a labelled chunk, or the
    caption line a markdown table is printed with."""
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
        md = re.search(r'print\(f?": (.*?) \{#(tbl-[\w-]+)\}"\)', code)
        if md:
            caps[md.group(2)] = md.group(1)
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
    """A rendered cell without its trailing footnote markers ("Acidic variants b)")."""
    return re.sub(r"(?:\s[a-z]\))+$", "", str(cell)).strip()


def _num(cell):
    """A number as the document prints it, back to a float ("−0.65", "575,000"); None for a cell that is
    not one ("< 0.001", "–")."""
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
    import tables as T
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    from annex_contract.concepts import Concept, ConceptStore
    from annex_contract.discourse import DocumentRelationship, ExplicitNonClaim
    from annex_contract.results import (ControlStrategyElement, Deviation, ModelTerm, PerformanceMeasure,
                                        ProcessCapability, StatisticalModelFit)
    from annex_contract.summaries import ReportSection, ReportStatement

    _check_sections()
    ns, _shown = G.qmd_namespace(QMD)
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
        """The rendered rows of the CTable the report printed under ``label``, keyed. Every row must name
        its own record (in cell ``cell``, footnote markers aside, or anywhere): a mis-keyed row grounds and
        attests the wrong thing."""
        tab = ct[label][0]
        rows_ = present_header(G.ctable_rows(tab, keys))
        bad = [k for k, row in rows_.items()
               if not (_unmark(_cells(row)[cell]) == name_of(k) if cell is not None else name_of(k) in row)]
        if bad:
            raise ValueError(f"{DOC} {label}: rows keyed to records they do not name: {bad}")
        return tab, rows_

    def md_rows(md, label):
        rows_ = G.md_string_rows(md)
        # a markdown table is markdown: pandoc renders its straight apostrophes typographic ("report’s")
        for k_, v_ in list(rows_.items()):
            if normalize(v_) not in text and normalize(_smart(v_)) in text:
                rows_[k_] = _smart(v_)
        cap = md_caps[label]
        if normalize(f"{cap} {rows_.header}") not in text:
            raise ValueError(f"{DOC}: the caption of {label} no longer reads {cap!r}")
        return rows_, cap

    def fig_cap(label, n):
        """The first ``n`` sentences of the caption of figure ``label``, from the option of its chunk."""
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

    md_caps = {}
    for code in re.findall(r"```\{python\}\n(.*?)```", _source(), flags=re.S):
        m_ = re.search(r'print\(f?": (.*?) \{#(tbl-[\w-]+)\}"\)', code)
        if m_:
            md_caps[m_.group(2)] = m_.group(1)

    # ---- names and values of the report ------------------------------------------------------------
    PRM, KEYS, NAME, UNIT, CLS = ns["P"], list(ns["KEYS"]), ns["NAME"], ns["UNIT"], ns["CLS"]
    SP_, NOR_, RNG_, PAR_ = ns["SP_"], ns["NOR_"], ns["RNG_"], ns["PAR_"]
    REG, RLAB, FMT, SIG = ns["REG"], ns["RLAB"], ns["FMT"], ns["SIG"]
    CHECK, ATTRS = ns["CHECK"], list(ns["ATTRS"])
    pv, n1, n2, fp = ns["pv"], ns["n1"], ns["n2"], ns["fp"]
    MARG, PAR = ns["MARG"], ns["PAR"]
    UNI1, UNI2, HLD = ns["UNI1"], ns["UNI2"], ns["HLD"]
    PDS = ns["PDS"]
    ALPHA = ns["ALPHA"]
    uo = P.CFG.unit_op(UO)
    UO_NAME = G.HUO_NAME
    STEP_LABEL = G.HSTEP_LABEL
    PC = {k: G.HPARAM_CONCEPT[NAME[k]] for k in KEYS}             # parameter key -> concept id
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))
    reg = P.cqa_reg.set_index("key")
    resp_attr = {"hcp_out_ng_mg": "hcp", "dna_out_pg_mg": "residual_dna",
                 "aggregate_out_pct": "aggregates_hmw", "lmw_cesds_pct": "fragments_lmw"}
    if set(resp_attr) != set(ATTRS):
        raise ValueError(f"{DOC}: the attribute responses of the report are {ATTRS}")

    # ---- the rendered tables, from the objects the report printed ------------------------------------
    pdf_ = ct["tbl-params"][1]
    pt_t, prow = keyed("tbl-params", KEYS, lambda k: NAME[k], cell=0)
    ALAB = ns["ALAB"]
    alab_key = {v: k for k, v in ALAB.items()}
    cq_df = ct["tbl-cqa"][1].copy()
    for col in cq_df.columns:
        cq_df[col] = cq_df[col].map(lambda v: re.sub(r"\^[a-z]\)\^", "", v) if isinstance(v, str) else v)
    ckeys = [alab_key[n] for n in cq_df["CQA"]]
    cq_t, crow = keyed("tbl-cqa", ckeys, lambda k: ALAB[k], cell=1)
    cq_df.index = ckeys
    sop_df = ct["tbl-sops"][1]
    sop_t, soprow = keyed("tbl-sops", list(sop_df["Reference"]), str, cell=1)
    amv_title = dict(zip(sop_df["Reference"], sop_df["Title"]))
    resp_t = ct["tbl-responses"][0]
    resprow = present_header(G.ctable_rows(resp_t))
    lev_df = ct["tbl-levels"][1]
    lev_t = ct["tbl-levels"][0]
    levrow = present_header(G.ctable_rows(lev_t))
    rep_t, reprow = keyed("tbl-reproducibility", list(ns["RORDER"]), lambda k: RLAB[k], cell=0)
    clar_t = ct["tbl-clarification"][0]
    clarrow = present_header(G.ctable_rows(clar_t))
    reg_t, regrow = keyed("tbl-regression", list(REG), lambda k: RLAB[k[1]], cell=1)
    regd_t, regdrow = keyed("tbl-regression-detail", list(REG), lambda k: RLAB[k[1]], cell=1)
    hold_t = ct["tbl-hold-harvest"][0]
    holdrow = present_header(G.ctable_rows(hold_t))
    hj_t = ct["tbl-hold-judgement"][0]
    hjrow = present_header(G.ctable_rows(hj_t))
    par_df = ct["tbl-par"][1]
    par_t = ct["tbl-par"][0]
    parrow = present_header(G.ctable_rows(par_t))
    cap_df = ct["tbl-capability"][1]
    capkeys = [alab_key[n] for n in cap_df["Attribute"]]
    cap_t, caprow = keyed("tbl-capability", capkeys, lambda k: ALAB[k], cell=0)
    all_t = ct["tbl-results-all"][0]
    allrow = present_header(G.ctable_rows(all_t))
    ms_df = ct["tbl-methods-summary"][1]
    ms_t, msrow = keyed("tbl-methods-summary", [re.sub(r"\^[a-z]\)\^", "", a) for a in ms_df["Method validation"]],
                        str, cell=2)
    devrow, dev_cap = md_rows(P.dev_register(DOC), "tbl-events")
    pdrow, pd_cap = md_rows(P.discrepancy_register(DOC), "tbl-discrepancies")

    def pdref(pid, sec="pds"):
        return ref(sec, pdrow[pid], rows=pdrow, caption=pd_cap, label="tbl-discrepancies")

    # rows of the merged tables, by the record they name
    def first_rows(rows_, n_per):
        """The first row of each block of ``n_per`` rows (the row that carries the merged label)."""
        vals = list(rows_.values())
        return [vals[i] for i in range(0, len(vals), n_per)]

    lev_first = dict(zip(KEYS, first_rows(levrow, int(ns["NLEV"]))))
    for k in KEYS:
        if not _cells(lev_first[k])[0].startswith(NAME[k]):
            raise ValueError(f"{DOC}: the levels table no longer opens the block of {k} with its name")
    par_rows = list(parrow.values())
    par_of = {k: (par_rows[2 * i], par_rows[2 * i + 1]) for i, k in enumerate(KEYS)}
    for k in KEYS:
        if not _cells(par_of[k][0])[0].startswith(NAME[k]):
            raise ValueError(f"{DOC}: the PAR table no longer opens the rows of {k} with its name")
    hj_rows = list(hjrow.values())
    hj_of = {"aggregates_hmw": [hj_rows[0], hj_rows[1]], "acidic_variants": hj_rows[2:6],
             "fragments_lmw": [hj_rows[6], hj_rows[7]]}
    for key, rows_ in hj_of.items():
        if _unmark(_cells(rows_[0])[0]) != T.ATTR_NAME[key]:
            raise ValueError(f"{DOC}: the hold judgement no longer opens the rows of {key} with its name")
    resp_rows = list(resprow.values())

    # ==== entities ===================================================================================
    q_step_exec = q("At commercial scale the step clarifies the contents of a `{python} SCALE_L` L production "
                    "bioreactor by continuous disk-stack centrifugation, depth filtration and sterilizing-grade "
                    "filtration, and it delivers the clarified harvest to Protein A capture.")
    q_between = q("Harvest and clarification, Step 4, lies between the production bioreactor and Protein A capture.")
    q_train = q("The culture passes a continuous disk-stack centrifuge, a train of depth filters and a "
                "sterilizing-grade filter, in that order (SOP-2005 and SOP-2006).")
    q_removes = q("The step removes cells and cell debris.")
    q_held = q("The clarified harvest is then held until capture.")
    step = S.ProcessStep(
        step_id=STEP_ID, step_name=UO_NAME, step_number=str(uo.step), unit_operation=UO_NAME,
        description=t("Step 4 of the A-Mab drug substance process, between the production bioreactor and Protein "
                      "A capture. At commercial scale it is run once per batch on the contents of a "
                      "`{python} SCALE_L` L production bioreactor: the culture passes a continuous disk-stack "
                      "centrifuge, a train of depth filters and a sterilizing-grade filter, and the clarified "
                      "harvest is held until capture. The step removes cells and cell debris. It is not credited "
                      "with clearing any impurity, and no viral clearance is claimed for it. Its settings change "
                      "the feed to capture: a clarification that removes less passes more fine material, and an "
                      "operation that breaks more cells releases more host cell protein and DNA. The drug "
                      "substance CQA register assigns fragments to the step, because proteases from lysed cells "
                      "continue to clip the antibody while the clarified harvest is held."),
        input_materials=["contents of the production bioreactor at the end of culture"],
        output_materials=["clarified harvest, held until Protein A capture"],
        equipment=["continuous disk-stack centrifuge", "depth filter train", "sterilizing-grade filter", G.HSDM],
        source_references=[ref("exec", q_step_exec), ref("uo", q_between), ref("uo", q_removes),
                           ref("uo", q_held)],
        metadata=meta())
    sites = G._site_entities(DOC, FILE, _sid("title"))
    q_obj1 = q("Qualify a scale-down model of the commercial harvest train and show that it represents the "
               "centrifugation and depth filtration performance of that train.")
    q_three = q("PCP-004 §5.1 planned a scale-down model of the harvest train in three parts, each matched on the "
                "quantity that drives its own mechanism.")
    q_noqual = q("No laboratory-scale disk-stack centrifuge exists, only a pilot-scale one.")
    sop5, sop6 = soprow["SOP-2005"], soprow["SOP-2006"]
    equipment = [
        S.Equipment(
            equipment_id=SDM_ID, equipment_name=G.HSDM,
            equipment_type="scale-down model of the harvest train (feed-zone shear, sedimentation and depth "
                           "filtration), not qualified (PD-004-03)",
            site_name=P.SENDING_SITE,
            source_references=[ref("objectives", q_obj1), ref("sdm", q_three), ref("sdm", q_noqual)],
            metadata=meta()),
        S.Equipment(
            equipment_id=CENTRIFUGE_ID, equipment_name="continuous disk-stack centrifuge",
            equipment_type="centrifuge (commercial scale)",
            source_references=[ref("uo", q_train), ref("analytics", sop5, sop_t, soprow)], metadata=meta()),
        S.Equipment(
            equipment_id=DEPTH_ID, equipment_name="depth filter train",
            equipment_type="depth filters with positively charged media (commercial scale)",
            source_references=[ref("uo", q_train), ref("analytics", sop6, sop_t, soprow),
                               ref("platform", q("Its media are positively charged, so they adsorb part of the DNA "
                                                 "and fine debris as well as retaining particles by size."))],
            metadata=meta()),
        S.Equipment(
            equipment_id=STERILE_ID, equipment_name="sterilizing-grade filter",
            equipment_type="filter (commercial scale)",
            source_references=[ref("uo", q_train), ref("analytics", sop6, sop_t, soprow)], metadata=meta()),
    ]

    # -- parameters: the table row, the first row of the levels table, the first row of the PAR table and
    # the sentence of Section 9 that gives the class ------------------------------------------------------
    q_cls = {
        "centrifuge_g": [q('Centrifugation (rcf) was classified as a `{python} CLS["centrifuge_g"]`.'),
                         q("It changed the clarity of the feed to capture."),
                         q("The class rests on host cell protein, residual DNA, aggregate and fragments in the "
                           "clarified harvest, the attributes the study measured.")],
        "depth_filter_load": [q('Depth filter load was classified as a `{python} CLS["depth_filter_load"]`.'),
                              q("The upper limit of its NOR lies on the edge of that range at the scale of an "
                                "unqualified model, and the turbidity of the clarified harvest, tested on every "
                                "batch, is the control that detects a filter that approaches its capacity "
                                "(@sec-control).")],
        "turbidity": [q('Post-clarification turbidity was classified as a `{python} CLS["turbidity"]`.'),
                      q("This class is a judgement."),
                      q("By the rule above a GPP also has no effect on process performance, and the data do not "
                        "show that for turbidity.")],
    }
    rationale = {
        "centrifuge_g": t(
            'Classified `{python} CLS["centrifuge_g"]` under SOP-4001 by the rule of PCMP-001 §7.7: it changed the '
            'clarity of the feed to capture and no effect on a quality attribute or on step yield was detected. '
            'Across its proven acceptable range of `{python} PAR_["centrifuge_g"]` centrate turbidity changed by '
            '`{python} n1(PARCHG_CEN1)` NTU and post-clarification turbidity by `{python} n2(PARCHG_CRCF)` NTU, '
            'with every result below the clarification limit; across the NOR the change in post-clarification '
            'turbidity is smaller than the repeatability limit of the turbidity method. The margin of the range to '
            'the NOR is `{python} pv("centrifuge_g", MARG["centrifuge_g"][0])` at each end. The class rests on '
            'host cell protein, residual DNA, aggregate and fragments in the clarified harvest.'),
        "depth_filter_load": t(
            'Classified `{python} CLS["depth_filter_load"]` under SOP-4001 by the rule of PCMP-001 §7.7: it changed '
            'post-clarification turbidity by `{python} n2(PARCHG_CDFL)` NTU across its proven acceptable range of '
            '`{python} PAR_["depth_filter_load"]`, the turbidity exceeded the clarification limit at '
            '`{python} pv("depth_filter_load", TOP_DFL)`, and no effect on a quality attribute or on step yield '
            'was detected. The margin of the range to the NOR is '
            '`{python} pv("depth_filter_load", MARG["depth_filter_load"][0])` below and none above; the turbidity '
            'of the clarified harvest, tested on every batch, is the control that detects a filter that '
            'approaches its capacity.'),
        "turbidity": t(
            'Classified `{python} CLS["turbidity"]` under SOP-4001 as a judgement of the report: the parameter is '
            'measured, not set, and over `{python} PAR_["turbidity"]` no effect on a quality attribute of the '
            'clarified harvest or on step yield was detected. The margin of its proven acceptable range to the '
            'NOR is none at the lower end and `{python} pv("turbidity", MARG["turbidity"][1])` at the upper end. '
            'By the rule a GPP also has no effect on process performance, which the data do not show: the '
            'expected effect on Protein A capture was not measured, because the load challenge was not run '
            '(PD-004-05).'),
    }
    params = []
    for k in KEYS:
        refs = [ref("factors", prow[k], pt_t, prow), ref("uni_design", lev_first[k], lev_t, levrow),
                ref("par", par_of[k][0], par_t, parrow)]
        refs += [ref("class", x) for x in q_cls[k]]
        params.append(S.ProcessParameter(
            parameter_id=PC[k], parameter_name=NAME[k], parameter_type=CLS[k], unit=UNIT[k],
            target_value=SP_[k], NOR=NOR_[k], PAR=PAR_[k], associated_step=STEP_LABEL,
            rationale_for_criticality=rationale[k], study_type=PRM[k].study, source_references=refs,
            metadata=meta()))

    # -- quality attributes: the register row, the rows of the hold judgement and of the capability table --
    q_three_in = q("The three are in scope because cell breakage in the centrifuge and the filters adds host cell "
                   "protein and DNA, and because an air-liquid interface can unfold the antibody and add aggregate.")
    attr_prose = {"hcp": [q_three_in], "residual_dna": [q_three_in, q("Residual DNA has very low criticality.")],
                  "aggregates_hmw": [q_three_in],
                  "fragments_lmw": [q("The drug substance CQA register assigns fragments to this step (PCMP-001 "
                                      "Table 3.1).")],
                  "acidic_variants": [q("Acidic variants enter scope through the hold study only.")]}
    method_of = {"hcp": "AMV-3012", "residual_dna": "AMV-3014", "aggregates_hmw": "AMV-3011",
                 "fragments_lmw": "AMV-3020", "acidic_variants": "AMV-3013"}
    AGG_C_, ACID_C_, FRAG_C_ = ns["AGG_C_"], ns["ACID_C_"], ns["FRAG_C_"]
    extra_crit = {
        "aggregates_hmw": [f"{AGG_C_} (criterion of the production bioreactor output, which passes through harvest "
                           f"unchanged to the load of Protein A capture; used to judge the held clarified harvest)"],
        "acidic_variants": [f"{ACID_C_} (criterion of the production bioreactor output, which passes through "
                            f"harvest unchanged to the load of Protein A capture; used to judge the held clarified "
                            f"harvest)"],
        "fragments_lmw": ["no criterion at harvest or at the production bioreactor; the held clarified harvest is "
                          "compared with the drug substance criterion"],
        "hcp": ["no criterion at harvest"],
        "residual_dna": ["no intermediate acceptance criterion at any step; judged on the drug substance only"],
    }
    attrs = []
    for key in ckeys:
        r = cq_df.loc[key]
        refs = [ref("cqa", crow[key], cq_t, crow)]
        if key in hj_of:
            refs.append(ref("hold", hj_of[key][0], hj_t, hjrow))
        if key in caprow:
            refs.append(ref("cap", caprow[key], cap_t, caprow))
        refs += [ref("cqa", x) for x in attr_prose[key]]
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=names[key], attribute_type="CQA",
            unit=reg.loc[key, "unit"],
            acceptance_criteria=[f"{_unmark(r['Acceptance'])} (drug substance)"] + extra_crit[key],
            analytical_method=method_of[key], associated_steps=[STEP_LABEL],
            rationale_for_criticality=f"A-Mab Tool #1 score = impact score × uncertainty score = {r['Tool #1']}.",
            criticality_level=r["Criticality"], tool1_score=int(r["Tool #1"]),
            tool2_severity=int(reg.loc[key, "tool2_severity"]), source_references=refs, metadata=meta()))

    # -- performance measures: the set-point row of the reproducibility table and the row of the responses
    # table that names the sample and the method ----------------------------------------------------------
    SPSTAT = ns["SPSTAT"]
    perf = []
    perf_spec = [
        ("centrate_turbidity_ntu", "centrate turbidity", 0, None,
         q("The centrate is collected, sampled and passed over the depth filter train at constant flux to the load "
           "of the run, and then over a sterilizing-grade filter.")),
        ("clarified_turbidity_ntu", "post-clarification turbidity", 1, NOR_["turbidity"],
         q("Post-clarification turbidity measures the fine particulate and colloidal material that the filters "
           "passed.")),
        ("step_yield_pct", "step yield", 6, None,
         q("The record names no method for the antibody concentration on which step yield rests, and PCP-004 named "
           "none.")),
    ]
    for rk, nm, ri, nor_, qx in perf_spec:
        rr_ = reprow[rk]
        c = _cells(rr_)
        perf.append(PerformanceMeasure(
            measure_id=f"{DOC}-PM{len(perf) + 1:02d}", measure_name=nm, unit_operation=UO_NAME,
            value=f"{c[1]} (mean of the {ns['N_SPR']} runs at the set-point, SD {c[2]})",
            unit=ns["RUNIT"][rk] if rk != "step_yield_pct" else "%",
            basis=f"S-HAR-UNI2, every parameter at its set-point; pooled RSD of the duplicates at every level "
                  f"{c[4]} % on {c[5]} degrees of freedom; at the scale of the study",
            normal_operating_range=nor_, in_process_only=True,
            source_references=[ref("repro", rr_, rep_t, reprow),
                               ref("analytics", resp_rows[ri], resp_t, resprow),
                               ref("operation" if ri == 0 else ("platform" if ri == 1 else "analytics"), qx)],
            metadata=meta()))

    # -- analytical methods: the procedure row, the methods-summary row, the sentence that names the method,
    # and the rows of the responses table that name it ---------------------------------------------------
    q_meth = {"AMV-3015": q("Turbidity by nephelometry (AMV-3015) measured the centrate and the clarified harvest."),
              "AMV-3012": q("Host cell protein by ELISA (AMV-3012) and residual DNA by qPCR (AMV-3014) measured the "
                            "impurity burden of the clarified harvest."),
              "AMV-3011": q('Aggregate was measured by SEC-HPLC, validated under `{python} SECM["id"]` '
                            '(`{python} SECM["sop"]`).'),
              "AMV-3020": q('Fragments were measured by non-reduced CE-SDS (nrCE-SDS), validated under '
                            '`{python} CESDS["id"]` (`{python} CESDS["sop"]`)'),
              "AMV-3013": q("In the hold study, charge variants by icIEF (AMV-3013) measured acidic variants.")}
    q_meth["AMV-3014"] = q_meth["AMV-3012"]
    resp_of = {"AMV-3015": [0, 1], "AMV-3012": [2], "AMV-3014": [3], "AMV-3011": [4, 7], "AMV-3020": [8],
               "AMV-3013": [9]}
    analyte_of = {a: _cells(msrow[a])[0] for a in msrow}
    attr_of_amv = {v: k for k, v in method_of.items()}
    methods = []
    for amv in [a for a in sop_df["Reference"] if a.startswith("AMV-")]:
        if not all(amv in resp_rows[i] for i in resp_of[amv]):
            raise ValueError(f"{DOC}: the responses table no longer names {amv} where the annex reads it")
        methods.append(S.AnalyticalMethod(
            method_id=amv, method_name=amv_title[amv], method_type=G.METHOD_TYPE.get(amv),
            analytes=[analyte_of[amv]],
            associated_attributes=[f"attr:{attr_of_amv[amv]}"] if amv in attr_of_amv else [],
            validation_status="validated",
            source_references=[ref("analytics", soprow[amv], sop_t, soprow),
                               ref("app_c", msrow[amv], ms_t, msrow), ref("analytics", q_meth[amv])]
            + [ref("analytics", resp_rows[i], resp_t, resprow) for i in resp_of[amv]],
            metadata=meta()))

    # -- capability: one record per row of the capability table ----------------------------------------
    CAPT, N_MC = ns["CAPT"], int(ns["N_MC"])
    q_cap_all = q("Every Cpk lies above the target of `{python} CPK_TARGET` that PCMP-001 §7.9 sets for a CQA in "
                  "routine manufacture, and so above its minimum of `{python} CPK_MIN`.")
    q_cap_frag = q("Their drug substance Cpk is `{python} n2(CPK_FRAG)`, from a simulated mean of "
                   "`{python} n2(MC_FRAG)` % against the criterion of `{python} FRAG_C_`.")
    capab = []
    for key, row in caprow.items():
        c = _cells(row)
        capab.append(ProcessCapability(
            capability_id=f"{DOC}-CAP{len(capab) + 1:02d}", quality_attribute=f"attr:{key}", index_name="Cpk",
            index_value=_num(c[5]), specification_side="upper", acceptance_range=c[2], mean=c[3],
            standard_deviation=c[4], unit=reg.loc[key, "unit"], basis="simulated", n_batches=N_MC,
            unit_operation=UO_NAME,
            source_references=[ref("cap", row, cap_t, caprow),
                               ref("cap", q_cap_frag if key == "fragments_lmw" else q_cap_all)],
            metadata=meta()))
        if str(CAPT.loc[key, "spec_type"]) not in ("upper", "nan") and "≤" not in c[2]:
            raise ValueError(f"{DOC}: {key} is no longer judged against an upper limit")

    # -- the linear regressions of S-HAR-UNI2: one fit per row of the regression table ------------------
    N_PER, N_SPR, DF_SP, DF_RES = int(ns["N_PER"]), int(ns["N_SPR"]), int(ns["DF_SP"]), int(ns["DF_RES"])
    fits = []
    for (pk, rk), row in regrow.items():
        c, d = _cells(row), _cells(regdrow[(pk, rk)])
        chk = (pk, rk) == CHECK
        sig = bool(SIG[(pk, rk)])
        verdict = ("a check of the challenge: the measured turbidity of the prepared material against its target "
                   "level, not an effect" if chk else
                   ("significant at α = " if sig else "not significant at α = ") + f"{ALPHA:g}")
        fits.append(StatisticalModelFit(
            model_fit_id=f"{DOC}-FIT{len(fits) + 1:02d}", response=RLAB[rk], unit_operation=UO_NAME,
            model_form=f"simple linear regression on the setting of {NAME[pk].lower() if pk != 'turbidity' else 'the target level of post-clarification turbidity'}, "
                       f"the other parameters at their set-points (S-HAR-UNI2)",
            n_runs=N_PER, r_squared=_num(c[5]), p_value=_num(c[4]), rmse=_num(d[4]),
            adequacy_statement=(
                f"Change over the range studied {c[2]}, 95 % confidence interval {c[3]}, p {c[4]}, on the variation "
                f"between the {N_SPR} runs with every parameter at set-point ({DF_SP} degrees of freedom), the error "
                f"term of PCP-004 §5.4 and §5.5; on the residual error ({DF_RES} degrees of freedom) {d[5]}, p {d[6]}; "
                f"R² {c[5]}, residual SD {d[4]}, with no threshold set for either; {verdict}."),
            terms=[ModelTerm(term="slope", factor=NAME[pk], coefficient=_num(d[2]), p_value=_num(c[4]),
                             significant=sig)],
            source_references=[ref("attrs", row, reg_t, regrow), ref("app_b", regdrow[(pk, rk)], regd_t, regdrow)],
            metadata=meta()))

    # -- study events ---------------------------------------------------------------------------------
    q_nobear = q("S-HAR-UNI has no data in the record and no result of it enters this report, so neither event "
                 "bears on a conclusion.")
    dev_prose = {
        "DEV-004-01": [("dev1", q("During the pre-use flush of a depth filter of lot LOT-DF-4408, the turbidity of "
                                  "the flush was `{python} gn(dev_004_01_flush_turbidity_ntu)` NTU, above the alert "
                                  "limit of the flush.")),
                       ("dev1", q("The investigation found the initial flush volume insufficient.")),
                       ("dev1", q("The lot was within its expiry date, `{python} lot_df_4408_expiry`.")),
                       ("events", q_nobear)],
        "DEV-004-02": [("dev2", q("In-process turbidity monitoring (AMV-3015) found a post-clarification turbidity "
                                  "above the NOR on one run, with a highest value of "
                                  "`{python} gn(dev_004_02_turbidity_max_ntu)` NTU against the upper NOR limit of "
                                  "`{python} CLAR_`.")),
                       ("dev2", q("The investigation found loading of the depth filter near its maximum as the "
                                  "cause.")),
                       ("dev2", q('The event is of the same kind as the result of S-HAR-UNI2 at '
                                  '`{python} pv("depth_filter_load", TOP_DFL)`, where both runs exceeded the limit '
                                  '(@sec-res-dfl).')),
                       ("events", q_nobear)],
    }
    dev_impact = {
        "DEV-004-01": t("A depth filter flush turbidity of `{python} gn(dev_004_01_flush_turbidity_ntu)` NTU, above the "
                        "alert limit of the flush, on lot LOT-DF-4408, which was within its expiry date "
                        "(`{python} lot_df_4408_expiry`); the investigation found the initial flush volume "
                        "insufficient, and Version 1.0 retained the run in the analysis of S-HAR-UNI. S-HAR-UNI has no "
                        "data in the record and no result of it enters the report, so the event bears on no "
                        "conclusion."),
        "DEV-004-02": t("A post-clarification turbidity of up to `{python} gn(dev_004_02_turbidity_max_ntu)` NTU on one "
                        "run against the upper NOR limit of `{python} CLAR_`; the investigation found loading of the "
                        "depth filter near its maximum as the cause, and Version 1.0 retained the run in the analysis "
                        "of S-HAR-UNI. The event is of the same kind as the result of S-HAR-UNI2 at "
                        "`{python} pv(\"depth_filter_load\", TOP_DFL)`. S-HAR-UNI has no data in the record, so the "
                        "event bears on no conclusion."),
    }
    EVD = ns["EV"].set_index("dev_id")
    devs = []
    for did, row in devrow.items():
        c = _cells(row)
        if str(EVD.loc[did, "disposition"]) != "retained":
            raise ValueError(f"{DOC}: {did} is no longer retained; its record says it is")
        devs.append(Deviation(
            deviation_id=did, summary=c[1], unit_operation=UO_NAME, detected_during=c[2], disposition=c[3],
            impact_statement=dev_impact[did], no_impact_on_conclusions=True,
            source_references=[ref("events", row, rows=devrow, caption=dev_cap, label="tbl-events")]
            + [ref(s_, x) for s_, x in dev_prose[did]],
            metadata=meta()))

    # -- document relationships, from the prose (the report prints no related-documents table) ---------
    rels = []

    def relation(kind, target, statement, sec, quote):
        rels.append(DocumentRelationship(
            relationship_id=f"{DOC}-R{len(rels) + 1:02d}", kind=kind, source_document_id=DOC,
            target_document_ref=target, statement=statement, source_references=[ref(sec, quote)], metadata=meta()))

    q_clear3 = q("Protein A capture and the two ion exchange steps clear the host cell protein and DNA that cell "
                 "breakage releases (PCR-005, PCR-007 and PCR-008).")
    relation("executed_under", "PCP-004", "The study was planned in PCP-004, the plan of the step.", "exec",
             q("The study was planned in PCP-004."))
    relation("references", "PCMP-001", "PCMP-001 Version 2.0 sets no intermediate acceptance criterion for the "
             "clarified harvest; the criteria of the production bioreactor output pass through harvest unchanged.",
             "cqa", q("PCMP-001 Version 2.0 sets no intermediate acceptance criterion for the clarified harvest "
                      "(PCMP-001 Table 7.1)."))
    relation("rolls_up_into", "PCMR-001", "The contributions of the step to the control strategy roll up into "
             "PCMR-001, which consolidates the control strategy of the train.", "cs",
             q("These contributions roll up into PCMR-001, which consolidates the control strategy of the train."))
    relation("references", "PTP-001", "The ranges and classes of the report are those against which the process "
             "performance qualification batches planned in PTP-001 will be run at the receiving site.", "cs",
             q("The ranges and classes are those against which the `{python} N_PPQ` process performance "
               "qualification batches planned in PTP-001 will be run at the receiving site."))
    relation("scoped_by", "RA-001", "The parameters of the study and the study type of each follow the "
             "pre-characterization risk assessment RA-001.", "risk",
             q("The parameters of the study and the study type of each follow the pre-characterization risk "
               "assessment RA-001."))
    relation("references", "INV-001", "Version 2.0 is issued under the QA investigation INV-001.", "changes",
             q('Version `{python} VER` is issued under the QA investigation `{python} INV["id"]`, which examined '
               'acceptance criteria set after data review for the analysis of proven acceptable ranges.'))
    relation("references", "PCR-003", "PCR-003 gives the derivation of the aggregate and acidic variant criteria of "
             "the production bioreactor output and the argument for the change of the aggregate criterion.", "cqa",
             q("PCR-003 gives the derivation of both and the argument for the change of the aggregate criterion."))
    relation("references", "PCR-003", "PCR-003 sets the monitoring of acidic variants at harvest of every "
             "production batch, as part of the mitigation of the acidic-variant risk it accepted.", "cs",
             q('PCR-003 sets the monitoring of acidic variants at harvest of every production batch, with an action '
               'limit of `{python} n2(AM["action_limit"])` %, as part of the mitigation of the acidic-variant risk '
               'it accepted.'))
    for tgt, step_nm in (("PCR-005", "Protein A capture"), ("PCR-007", "cation exchange"),
                         ("PCR-008", "anion exchange")):
        relation("references", tgt, f"{step_nm[0].upper() + step_nm[1:]} ({tgt}) clears the host cell protein and "
                 f"DNA that cell breakage at harvest releases.", "risk", q_clear3)
    q_viab = q("Viability at the end of culture is a property of the culture and is characterized in PCP-003 and "
               "PCR-003, not here.")
    relation("references", "PCP-003", "Viability at the end of culture is characterized in PCP-003 and PCR-003.",
             "platform", q_viab)

    # -- explicit non-claims, by section ----------------------------------------------------------------
    ncs, nc_at = [], {}

    def nclaim(sec, subject, statement, quotes, rationale=None, elsewhere=None):
        ncs.append(ExplicitNonClaim(
            non_claim_id=f"{DOC}-NC{len(ncs) + 1:02d}", subject=subject, unit_operation=UO_NAME,
            statement=statement, rationale=rationale, handled_elsewhere=elsewhere,
            source_references=[ref(s_, x) for s_, x in quotes], metadata=meta()))
        nc_at.setdefault(sec, []).append(ncs[-1])

    q_noclear = q("It is not credited with clearing any impurity, and no viral clearance is claimed for it.")
    nclaim("uo", "viral clearance", "No viral clearance is claimed for the step, and no spiking study was made.",
           [("uo", q_noclear),
            ("basis", q("No viral clearance is claimed for this step, and no spiking study was made"))])
    nclaim("uo", "clearance of an impurity", "The step is not credited with clearing host cell protein, DNA or "
           "aggregate; the depth filter media adsorb part of the DNA, but no clearance is claimed for it.",
           [("uo", q_noclear), ("cqa", q("The step is not credited with clearing any of them.")),
            ("cqa", q("The depth filter media adsorb part of the DNA, but no clearance is claimed for it."))],
           elsewhere="Protein A capture, cation exchange and anion exchange (PCR-005, PCR-007, PCR-008)")
    nclaim("platform", "viability at the end of culture", "Viability at the end of culture is a property of the "
           "culture and is not characterized in this report.", [("platform", q_viab)],
           elsewhere="PCP-003 and PCR-003")
    nclaim("sdm", "offset to manufacturing scale", "The scale-down model was not qualified, so every result is at the "
           "scale of the study with no offset to manufacturing scale; the offset of every output is unknown, not "
           "zero, and the study does not predict the concentration of an impurity in a commercial batch.",
           [("sdm", q("No qualification was made (PD-004-03).")),
            ("sdm", q("The offset of every output is unknown, not zero.")),
            ("sdm", q("It does not predict the concentration of an impurity in a commercial batch."))],
           rationale="No laboratory-scale disk-stack centrifuge exists, only a pilot-scale one.")
    nclaim("stats", "response-surface model and propagation", "No response-surface model is fitted for the step and "
           "no Monte Carlo propagation of a fitted model is made; a range from the study holds with the other "
           "parameters at their set-points.",
           [("stats", q("No response-surface model is fitted for this step, and no Monte Carlo propagation of a "
                        "fitted model is made (PCP-004 §5.5)."))])
    nclaim("stats", "fragments level entering the hold", "The fragments level taken to enter the hold is not the "
           "highest level expected in routine manufacture, because a longer culture within its NOR carries more "
           "fragments into harvest and no result of the campaign measures that increase.",
           [("stats", q("The fragments level that enters the hold is therefore not the highest level expected in "
                        "routine manufacture.")),
            ("stats", q("A longer culture within its NOR ends at lower viability and carries more fragments into "
                        "harvest (@sec-platform), and no result of the campaign measures that increase."))])
    nclaim("factors", "ranges beyond the range studied", "No proven acceptable range is claimed beyond the range "
           "studied of a parameter, which is its knowledge space.",
           [("factors", q("The range studied of each parameter is its knowledge space, and no proven acceptable range "
                          "is claimed beyond it."))])
    nclaim("uni_design", "material a filter near capacity passes", "The turbidity range is a range of turbidity "
           "delivered to capture; no claim is made about the material that a depth filter near capacity passes.",
           [("uni_design", q("The turbidity range of @sec-par is therefore a range of turbidity delivered to capture, "
                             "and no claim is made about the material that a filter near capacity passes (PCP-004 "
                             "§12)."))],
           rationale="The turbidity material was prepared by adding centrate to clarified filtrate and carries the "
                     "particle size distribution of the centrate.")
    nclaim("uni_design", "Protein A load challenge and filter pressure", "The column pressure and the cycle yield of "
           "the Protein A load challenge and the pressure the filter train develops have no result.",
           [("uni_design", q("The turbidity series was not loaded onto a scale-down Protein A column, and the pressure "
                             "that the filter train develops was not measured (PD-004-05).")),
            ("uni_design", q("The column pressure and the cycle yield of the Protein A load challenge (PCP-004 §6.2) "
                             "therefore have no result."))], elsewhere="PD-004-05")
    nclaim("hold_design", "culture of the held pool", "The record does not name the culture from which the pool of "
           "the hold study was made, so the levels of the pool itself are not used in the judgement.",
           [("hold_design", q("The record does not name the culture from which the pool was made.")),
            ("hold", q("The levels of the pool itself are therefore not used."))])
    nclaim("turb", "effect of turbidity on Protein A capture", "The effect of the turbidity of the clarified harvest "
           "on capture itself was not measured.",
           [("turb", q("The effect on capture itself, which the mechanism expects through fouling of the Protein A "
                       "bed, was not measured, because the Protein A load challenge was not run (@sec-univariate)."))],
           elsewhere="PD-004-05")
    nclaim("attrs", "ranges for acidic variants", "Acidic variants were not measured in S-HAR-UNI2, and no range of "
           "the report is supported for them.",
           [("attrs", q("Acidic variants were not measured in S-HAR-UNI2, and no range of this report is supported "
                        "for them."))])
    nclaim("attrs", "a verdict on host cell protein and residual DNA at harvest", "Host cell protein and residual DNA "
           "have no criterion at harvest; their results are reported for information and are neither met nor not "
           "met.",
           [("attrs", q("Host cell protein and residual DNA have no criterion at harvest, so their results are "
                        "reported for information and are neither met nor not met."))])
    nclaim("mech", "particle size", "The study did not measure particle size; the levelling off of centrate "
           "turbidity is only consistent with particles too small to settle.",
           [("mech", q("The study did not measure particle size."))])
    nclaim("mech", "cell breakage in a commercial feed zone", "The absence of a detected rise in host cell protein "
           "or DNA at the higher fields does not show that a commercial feed zone breaks no cells at the highest "
           "field.",
           [("mech", q("The model was not qualified, and PCP-004 §5.1 expected a bench model to under-represent "
                       "lysis, so this result does not show that a commercial feed zone breaks no cells at the "
                       "highest field."))])
    nclaim("ds", "design space", "No design space is claimed for the step; no multivariate design was run, and no "
           "combination of two parameters away from their set-points is claimed.",
           [("ds", q("No design space is claimed for this step.")),
            ("ds", q("Each proven acceptable range of @sec-par holds with the other parameters at their set-points, "
                     "and no combination of two parameters away from their set-points is claimed."))],
           rationale="A design space is a multivariate region, and no multivariate design was run (PCP-004 §8).")
    nclaim("par", "performance of Protein A capture over the turbidity PAR", "The proven acceptable range of "
           "post-clarification turbidity does not cover the performance of Protein A capture.",
           [("par", q("It does not cover the performance of Protein A capture, because the load challenge was not "
                      "made (PD-004-05)."))], elsewhere="PD-004-05")
    nclaim("cap", "capability of the outputs of harvest", "The study gives no capability for the outputs of "
           "harvest; it has no model of the step from which batches could be simulated.",
           [("cap", q("This study gives no capability for the outputs of harvest.")),
            ("cap", q("It has no model of the step from which batches could be simulated, and its results are at the "
                      "scale of the study."))])
    nclaim("cs", "a limit for the hold of the clarified harvest", "The report sets no limit for the hold of the "
           "clarified harvest, which is not a parameter of PCP-004; bioburden and endotoxin were not part of the "
           "hold study.",
           [("cs", q("The hold of the clarified harvest is not a parameter of PCP-004, and this report sets no limit "
                     "for it.")),
            ("cs", q("Bioburden and endotoxin were not part of the hold study, so a hold time in manufacturing needs "
                     "that support as well."))])
    nclaim("cs", "control of a quality attribute at harvest", "No quality attribute is controlled at harvest.",
           [("cs", q("No quality attribute is controlled at harvest."))],
           elsewhere="clearance at Protein A capture, cation exchange and anion exchange; drug substance release")
    nclaim("changes", "deviations", "The report raises no deviation: a process characterization study is not GMP "
           "manufacture, so events of execution are study events and departures from PCP-004 are discrepancies "
           "from the plan.",
           [("changes", q("The record. A process characterization study is not GMP manufacture, so this report "
                          "raises no deviation."))])

    # -- contributions to the control strategy (Section 10) -----------------------------------------------
    cse = []

    def cs_el(desc, controls, ctype, quotes):
        cse.append(ControlStrategyElement(
            element_id=f"{DOC}-CS{len(cse) + 1:02d}", description=desc, unit_operation=UO_NAME,
            controls=controls, control_type=ctype, source_references=[ref("cs", x) for x in quotes],
            metadata=meta()))

    cs_el(t('Centrifugation (rcf) and depth filter load are controlled within their NORs, `{python} NOR_["centrifuge_g"]` '
            'and `{python} NOR_["depth_filter_load"]`, as KPPs.'),
          "centrifugation (rcf); depth filter load", "parameter control within the NOR",
          [q('Centrifugation (rcf) and depth filter load are controlled within their NORs, '
             '`{python} NOR_["centrifuge_g"]` and `{python} NOR_["depth_filter_load"]`, as KPPs.')])
    cs_el(t('The turbidity of the clarified harvest is measured on every batch by nephelometry (AMV-3015) as an '
            'in-process control against its NOR of `{python} NOR_["turbidity"]`, whose upper limit is the '
            'clarification limit; it is the measurement by which the clarified harvest is released to capture, and '
            'it detects a centrifuge that clarifies poorly, a depth filter near its capacity and an excursion of the '
            'filter load, whose upper NOR limit lies on the edge of its proven acceptable range.'),
          "post-clarification turbidity", "in-process monitoring",
          [q('The turbidity of the clarified harvest is measured on every batch by nephelometry (AMV-3015) as an '
             'in-process control (PCP-004 §4.1 and §8), against its NOR of `{python} NOR_["turbidity"]`.'),
           q("The control detects a centrifuge that clarifies poorly or a depth filter near its capacity."),
           q("The upper NOR limit of depth filter load lies on the edge of its proven acceptable range, so this test "
             "is the control that detects an excursion of the filter load.")])
    cs_el("No quality attribute is controlled at harvest: host cell protein and DNA are controlled by their clearance "
          "at Protein A capture, cation exchange and anion exchange, and fragments are judged at the downstream steps "
          "and tested at release of the drug substance by nrCE-SDS.",
          "host cell protein; residual DNA; fragments", "downstream clearance and release testing",
          [q("Host cell protein and DNA are controlled by their clearance at Protein A capture, cation exchange and "
             "anion exchange (PCR-005, PCR-007 and PCR-008), and residual DNA by that clearance, not by a release test"),
           q("They are judged at the downstream steps against the criteria of PCMP-001 Table 7.1 and tested at "
             "release of the drug substance by nrCE-SDS.")])
    cs_el(t('On one pool, the hold study supports a hold of the clarified harvest of up to `{python} HOLD_D` days at '
            '`{python} COLD` or at `{python} WARM` for aggregate, fragments and the upper limit of acidic variants; a '
            'cold hold slows the rise of fragments and acidic variants. No hold limit is set.'),
          "hold of the clarified harvest", "procedural (hold time and temperature)",
          [q("On one pool, the hold study supports a hold of up to `{python} HOLD_D` days at `{python} COLD` or at "
             "`{python} WARM` for aggregate, fragments and the upper limit of acidic variants, the attributes it "
             "measured."),
           q("A cold hold slows the rise of fragments and acidic variants.")])
    cs_el(t('PCR-003 sets the monitoring of acidic variants at harvest of every production batch, with an action limit '
            'of `{python} n2(AM["action_limit"])` %; the time and the temperature of a sample before it is tested bear '
            'on that monitoring, because acidic variants rise in a clarified harvest held warm.'),
          "acidic variants at harvest", "in-process monitoring (set by PCR-003)",
          [q('The hold study shows that acidic variants rise in a clarified harvest held at `{python} WARM`, by '
             '`{python} n2(HC[("acidic_pct", WARM)]["end"])` percentage points in `{python} HOLD_D` days, so the time '
             'and the temperature of a sample before it is tested bear on that monitoring.')])

    entities = [
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("exec"), process_steps=[step], sites=sites),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("uo"), equipment=equipment,
                                  document_relationships=rels, non_claims=nc_at["uo"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("changes"), non_claims=nc_at["changes"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("platform"), non_claims=nc_at["platform"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cqa"), quality_attributes=attrs),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("sdm"), non_claims=nc_at["sdm"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("analytics"), analytical_methods=methods),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("stats"), non_claims=nc_at["stats"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("factors"), parameters=params,
                                  non_claims=nc_at["factors"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("uni_design"), non_claims=nc_at["uni_design"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("hold_design"), non_claims=nc_at["hold_design"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("repro"), performance_measures=perf),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("turb"), non_claims=nc_at["turb"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("attrs"), model_fits=fits,
                                  non_claims=nc_at["attrs"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("mech"), non_claims=nc_at["mech"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("ds"), non_claims=nc_at["ds"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("par"), non_claims=nc_at["par"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cap"), capabilities=capab,
                                  non_claims=nc_at["cap"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cs"), control_strategy=cse,
                                  non_claims=nc_at["cs"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("record"), deviations=devs),
    ]

    # ==== studies: each on its prose, its data rows and the row of the discrepancy register that records it
    pd_of = {s_: d["id"] for d in P.PLAN_DISCREPANCIES[DOC] for s_ in (d.get("studies") or [])}
    names_fac = [NAME[k] for k in KEYS]
    hold_resp = [T.ATTR_NAME["aggregates_hmw"], T.ATTR_NAME["fragments_lmw"], T.ATTR_NAME["acidic_variants"]]
    study_spec = {
        UNI1: dict(study_type="univariate",
                   design_name="univariate study of each parameter (Version 1.0), described and narrated without a "
                               "result for any parameter effect; no data in the record",
                   factors=names_fac,
                   prose=[("uni_design", q("S-HAR-UNI, the univariate study of Version 1.0, ran from "
                                           "`{python} WIN[UNI1]`.")),
                          ("uni_design", q("Version 1.0 described it and narrated its outcome, but gave no result for "
                                           "any parameter effect, and it has no data in the record."))],
                   rows=[]),
        UNI2: dict(study_type="univariate",
                   design_name=t("one factor at a time, `{python} NLEV` levels per parameter in duplicate, the other "
                                 "parameters at their set-points; post-clarification turbidity as a challenge"),
                   factors=names_fac, responses=[RLAB[r] for r in ns["RORDER"]],
                   prose=[("uni_design", q("S-HAR-UNI2 was made from `{python} WIN[UNI2]` to give the harvest "
                                           "parameters recorded results (PD-004-01).")),
                          ("uni_design", q("Each parameter was run at `{python} NLEV` levels "
                                           "(`{python} join_and(LEVNAMES)`) in duplicate, with the other parameters at "
                                           "their set-points.")),
                          ("uni_design", q("That gives `{python} N_RUNS` runs in three series of `{python} N_SER`."))],
                   rows=[("uni_design", r_, lev_t, levrow) for r_ in levrow.values()]
                   + [("app_a", r_, all_t, allrow) for r_ in allrow.values()]),
        HLD: dict(study_type="univariate",
                  design_name=t("hold study: one pool of clarified harvest made at the set-point of the step, held at "
                                "`{python} COLD` and at `{python} WARM` for `{python} HOLD_D` days and sampled on days "
                                "`{python} join_and(DAYS)`"),
                  factors=["hold time", "hold temperature"], responses=hold_resp,
                  prose=[("hold_design", q("The hold study S-HAR-HLD was made from `{python} WIN[HLD]` (PD-004-02).")),
                         ("hold_design", q("One pool of clarified harvest, made at the set-point of the step, was held "
                                           "at `{python} COLD` and at `{python} WARM` for `{python} HOLD_D` days and "
                                           "sampled as @sec-sampling describes."))],
                  rows=[("hold", r_, hold_t, holdrow) for r_ in holdrow.values()]),
    }
    studies = []
    for sid_, spec in study_spec.items():
        spec = dict(spec)
        prose_, rows_ = spec.pop("prose"), spec.pop("rows")
        refs = [ref(s_, x) for s_, x in prose_] + [ref(s_, r_, tab_, rr_) for s_, r_, tab_, rr_ in rows_]
        if sid_ in pd_of:
            refs.append(pdref(pd_of[sid_]))
        studies.append(S.StudyDesign(
            study_id=f"study:{sid_}", unit_operation=UO_NAME, scale_down_model=G.HSDM,
            associated_parameters=[G.HPARAM_CONCEPT[x] for x in spec.get("factors", []) if x in G.HPARAM_CONCEPT],
            source_references=refs, metadata=meta(), **spec))

    # ==== the proven acceptable ranges: each parameter on its two rows of the PAR table and its sentence ==
    q_par = {
        "centrifuge_g": q('Its proven acceptable range is the whole range studied, `{python} PAR_["centrifuge_g"]`, and '
                          'the NOR of `{python} NOR_["centrifuge_g"]` lies inside it with '
                          '`{python} pv("centrifuge_g", MARG["centrifuge_g"][0])` of margin at each end.'),
        "depth_filter_load": q('Its proven acceptable range is bounded at the last level that passed and runs from '
                               '`{python} RLO_["depth_filter_load"]` to '
                               '`{python} pv("depth_filter_load", PAR["depth_filter_load"][1])`.'),
        "turbidity": q('Its proven acceptable range, `{python} PAR_["turbidity"]`, answers a different question from '
                       'the clarification criterion.'),
    }
    attrs4 = "host cell protein, residual DNA, aggregates (HMW) and fragments (LMW) in the clarified harvest"
    basis = {
        "centrifuge_g": t("PCP-004 §7 criteria 1 and 3 (impurity release and product quality), judged by the slope "
                          "against the setting at α = `{python} ALPHA` because the samples before the step were not "
                          "taken: no slope detected. Criterion 2 (clarification), each result of post-clarification "
                          "turbidity ≤ `{python} CLAR_`: met at every level. The range is bounded at the levels "
                          "tested, holds with the other parameters at their set-points and is stated at the scale of "
                          "the study."),
        "depth_filter_load": t("PCP-004 §7 criteria 1 and 3 (impurity release and product quality), judged by the "
                               "slope against the setting at α = `{python} ALPHA`: no slope detected. Criterion 2 "
                               "(clarification), each result of post-clarification turbidity ≤ `{python} CLAR_`: not met "
                               "at `{python} pv(\"depth_filter_load\", TOP_DFL)`, so the range is bounded at the last "
                               "level that passed. It holds for centrate from the set-point field, with the other "
                               "parameters at their set-points, at the scale of the study; the upper limit of the NOR "
                               "lies on its edge."),
        "turbidity": t("PCP-004 §7 criteria 1 and 3 (impurity release and product quality) alone, judged by the slope "
                       "against the challenge level at α = `{python} ALPHA`: no slope detected. Criterion 2 does not "
                       "apply, because the turbidity of the series is the challenge level itself. The range does not "
                       "cover the performance of Protein A capture; a harvest setting must still deliver turbidity "
                       "within the NOR of `{python} NOR_[\"turbidity\"]`."),
    }
    pars = []
    for k in KEYS:
        r0 = _cells(par_of[k][0])
        if (r0[1], r0[5]) != (f"{ns['fg'](PRM[k].prange[0])}–{ns['fg'](PRM[k].prange[1])}",
                              f"{ns['fg'](PAR[k][0])}–{ns['fg'](PAR[k][1])}"):
            raise ValueError(f"{DOC}: the PAR table no longer prints the range studied and the PAR of {k}")
        pars.append(S.ProvenAcceptableRange(
            par_id=f"{DOC}-PAR{len(pars) + 1:02d}", unit_operation=UO_NAME,
            quality_attribute=attrs4 + ("" if k == "turbidity" else "; post-clarification turbidity"),
            parameter=NAME[k], characterization_range=RNG_[k], par_at_setpoint=PAR_[k], par_nor_propagated=None,
            acceptance_basis=basis[k],
            source_references=[ref("par", par_of[k][0], par_t, parrow), ref("par", par_of[k][1], par_t, parrow),
                               ref("par", q_par[k])],
            metadata=meta()))

    # ==== acceptance criteria: the decision criteria of PCP-004 §7 as the report applies them, and the
    # criteria the held clarified harvest is judged against ===============================================
    crit_sec = f"{DOC}_crit"

    def cref(sec, quote, table=None, rows=None):
        r = ref(sec, quote, table, rows)
        r.section_id = crit_sec
        return r
    q_c1 = q("Host cell protein and residual DNA in the clarified harvest are compared with the same measurements "
             "on the unclarified culture that produced it.")
    c1_basis = t("PCP-004 §7 decision criterion 1 (impurity release), of Version 1.0 in its words: {what} in the "
                 "clarified harvest is compared with the unclarified culture that produced it, and a level passes when "
                 "no increase is detected at α = `{python} ALPHA`, or when a detected increase is smaller than the "
                 "method can resolve. With no result for the unclarified culture, the report judges it by the slope "
                 "against the setting. A comparison, not a numeric limit.")
    acrit = [S.AcceptanceCriterionRecord(step=UO, attribute=key, basis=c1_basis.replace("{what}", names[key]),
                                         revision=P.REV2["rev"], status="in force", source=cref("par", q_c1))
             for key in ("hcp", "residual_dna")]
    acrit.append(S.AcceptanceCriterionRecord(
        step=UO, attribute="turbidity", high=float(ns["CLAR_LIM"]), unit=UNIT["turbidity"],
        basis="PCP-004 §7 decision criterion 2 (clarification), of Version 1.0 in its words: each result of "
              "post-clarification turbidity in the centrifugation (rcf) and depth filter load series at or below the "
              "upper limit of its NOR, which is set from production experience and not derived from a measured "
              "effect on Protein A capture; not applicable to the turbidity series.",
        revision=P.REV2["rev"], status="in force",
        source=cref("par", q("Post-clarification turbidity is compared with the upper limit of its NOR, "
                             "`{python} CLAR_`."))))
    acrit.append(S.AcceptanceCriterionRecord(
        step=UO, attribute="aggregates_hmw",
        basis=t("PCP-004 §7 decision criterion 3 (product quality), of Version 1.0 in its words: aggregate is compared "
                "before and after the step, and a level passes when no increase is detected at α = `{python} ALPHA`. "
                "With no result before the step, the report judges it by the slope against the setting."),
        revision=P.REV2["rev"], status="in force",
        source=cref("par", q("Aggregate is compared before and after the step, and a level passes when no increase is "
                             "detected at α = `{python} ALPHA`."))))
    acrit.append(S.AcceptanceCriterionRecord(
        step=UO, attribute="fragments_lmw",
        basis="Judged as PCP-004 §7 decision criterion 3 (product quality), by the slope against the setting; PCP-004 "
              "lists fragments in scope but names them neither as a response of its study nor in its criteria.",
        revision=P.REV2["rev"], status="in force", source=cref("par", q("Fragments were judged the same way."))))
    for key, (lo, hi) in (("aggregates_hmw", (None, ns["AGG_C"][1])), ("acidic_variants", ns["ACID_C"][:2]),
                          ("fragments_lmw", (None, ns["FRAG_DS"][1]))):
        acrit.append(S.AcceptanceCriterionRecord(
            step=UO, attribute=key, low=None if lo is None else float(lo), high=float(hi),
            unit=reg.loc[key, "unit"],
            basis=("Drug substance criterion, used to judge the held clarified harvest: PCMP-001 sets no fragments "
                   "criterion for the load of Protein A capture, and none in the train is stricter."
                   if key == "fragments_lmw" else
                   "Criterion of the production bioreactor output (PCMP-001 Table 7.1), which passes through harvest "
                   "unchanged to the load of Protein A capture; used to judge the held clarified harvest (PCMP-001 "
                   "Version 2.0 §5). PCMP-001 sets no intermediate acceptance criterion for the clarified harvest."),
            revision=P.REV2["rev"], status="in force", source=cref("hold", hj_of[key][0], hj_t, hjrow)))

    # ==== assertions ======================================================================================
    AS = []

    def add(subj, pred, obj, txt, refs):
        AS.append(EvidenceBackedAssertion(
            assertion_id=f"{DOC}-A{len(AS) + 1:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=txt, source_references=refs, metadata=meta()))

    add(STEP_ID, "step_uses_equipment", SDM_ID, f"The study of {UO_NAME} was planned on a {G.HSDM} in three parts; "
        f"the model was not qualified.", [ref("sdm", q_three)])
    add(STEP_ID, "step_uses_equipment", CENTRIFUGE_ID, f"{UO_NAME} uses a continuous disk-stack centrifuge (SOP-2005).",
        [ref("analytics", sop5, sop_t, soprow)])
    add(STEP_ID, "step_uses_equipment", DEPTH_ID, f"{UO_NAME} uses a train of depth filters (SOP-2006).",
        [ref("analytics", sop6, sop_t, soprow)])
    add(STEP_ID, "step_uses_equipment", STERILE_ID, f"{UO_NAME} uses a sterilizing-grade filter (SOP-2006).",
        [ref("analytics", sop6, sop_t, soprow)])
    for k in KEYS:
        add(STEP_ID, "step_has_parameter", PC[k],
            f"{UO_NAME} has process parameter {NAME[k]}, classified {CLS[k]}, studied {PRM[k].study}ly, set-point "
            f"{SP_[k]}, NOR {NOR_[k]}.", [ref("factors", prow[k], pt_t, prow)])
    role = {"hcp": "carries {n} from the culture and can add to it by cell breakage; it clears none",
            "residual_dna": "carries {n} from the culture and can add to it by cell breakage; it clears none",
            "aggregates_hmw": "carries {n} from the culture and could add to it at an air-liquid interface",
            "fragments_lmw": "is assigned {n} by the drug substance CQA register, because clipping continues in the "
                             "held clarified harvest",
            "acidic_variants": "brings {n} into scope through the hold study only"}
    for key in ckeys:
        add(STEP_ID, "step_has_quality_attribute", f"attr:{key}",
            f"{UO_NAME} " + role[key].format(n=names[key]) + ".", [ref("cqa", crow[key], cq_t, crow)])
    for amv, row in msrow.items():
        if amv not in attr_of_amv:
            continue
        key = attr_of_amv[amv]
        c = _cells(row)
        add(f"attr:{key}", "attribute_measured_by_method", f"method:{amv}",
            f"{names[key]} is measured by {c[1].split(' ')[0]} ({amv}), reported as {c[3]}, precision of a single "
            f"result {c[4]}, LOQ {c[5]}.", [ref("app_c", row, ms_t, msrow)])
    for key in ckeys:
        r = cq_df.loc[key]
        extra = [ref("hold", hj_of[key][0], hj_t, hjrow)] if key in hj_of else []
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{UO}_{key}_criterion",
            f"{names[key]}: drug substance criterion {_unmark(r['Acceptance'])}; at harvest, "
            + extra_crit[key][0] + ".", [ref("cqa", crow[key], cq_t, crow)] + extra)
    # parameter effects on the four attributes the study measured: the row of the regression table
    for (pk, rk), row in regrow.items():
        if rk not in resp_attr:
            continue
        c = _cells(row)
        key = resp_attr[rk]
        sig = bool(SIG[(pk, rk)])
        add(PC[pk], "parameter_impacts_attribute" if sig else "parameter_does_not_significantly_impact_attribute",
            f"attr:{key}",
            f"{NAME[pk]} on {names[key]} in the clarified harvest (S-HAR-UNI2): change over the range studied {c[2]} "
            f"(95 % confidence interval {c[3]}), p {c[4]}, " + ("significant" if sig else "no slope detected")
            + f" at α = {ALPHA:g}.", [ref("attrs", row, reg_t, regrow)])

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

    def sq(sec, src, txt=None, extra=()):
        """A statement of one prose span: ``src`` is the .qmd source of the span, ``txt`` the statement where it
        is not the span itself, ``extra`` further ``(section, source)`` spans a paraphrase draws on."""
        st(sec, t(txt) if txt else clean(q(src)), [ref(sec, q(src))] + [ref(s_, q(x)) for s_, x in extra])

    def srow(sec, txt, row, tab=None, rows_=None, caption=None, label=None):
        """A statement of one rendered row."""
        st(sec, txt, [ref(sec, row, tab, rows_, caption=caption, label=label)])

    # -- Executive summary ----------------------------------------------------------------------------------
    sq("exec", "This report presents the process characterization of harvest and clarification, Step 4 of the A-Mab "
               "drug substance process, at Version `{python} VER`.")
    sq("exec", "The drug substance CQA register nevertheless assigns fragments to this step, because proteases from "
               "lysed cells continue to clip the antibody while the clarified harvest is held.")
    sq("exec", "The report supports the transfer of the process from the development site in "
               "`{python} SENDING_LOCATION` to the commercial drug substance site in `{python} RECEIVING_LOCATION`.")
    sq("exec", "Version 1.0 of this report described a univariate study of each parameter, S-HAR-UNI "
               "(`{python} WIN[UNI1]`), and narrated its outcome without a result for any parameter effect.",
       extra=[("exec", "That study has no data in the record.")])
    sq("exec", "During the Version 2.0 re-analysis, after the QA investigation INV-001 closed, two further studies "
               "were made.")
    sq("exec", "In the univariate study S-HAR-UNI2 (`{python} WIN[UNI2]`) each parameter was run at `{python} NLEV` "
               "levels in duplicate, with the other parameters at their set-points.")
    sq("exec", "In the hold study S-HAR-HLD (`{python} WIN[HLD]`) one pool of clarified harvest was held at two "
               "temperatures for `{python} HOLD_D` days.")
    sq("exec", "PCP-004 foresaw neither study, and each is recorded as a discrepancy from the plan (PD-004-01 and "
               "PD-004-02).")
    sq("exec", "The scale-down model of the harvest train was not qualified, because no laboratory-scale disk-stack "
               "centrifuge exists (PD-004-03).")
    sq("exec", "Every result is therefore stated at the scale of the study, and its offset from manufacturing scale is "
               "unknown, not zero.")
    sq("exec", "Five further discrepancies record what the study did not do as the plan set out.",
       "Five further discrepancies record what the study did not do as the plan set out: the culture and the centrate "
       "were not sampled, the filter pressure and the Protein A load challenge were not measured, the depth filter load "
       "series was run only on centrate from the set-point field, records of execution were not kept, and the report "
       "states the rules the plan leaves open (PD-004-04 to PD-004-08).",
       extra=[("exec", "The culture and the centrate were not sampled, the filter pressure and the Protein A load "
                       "challenge were not measured, the depth filter load series was run only on centrate from the "
                       "set-point field, records of execution were not kept, and this report states the rules the plan "
                       "leaves open (PD-004-04 to PD-004-08).")])
    sq("exec", "Turbidity responded to the parameters, and no effect on a quality attribute was detected.")
    sq("exec", 'Centrate turbidity fell from a mean of `{python} n1(CEN[lo_g])` NTU at `{python} RLO_["centrifuge_g"]` '
               'to `{python} n1(CEN[hi_g])` NTU at `{python} RHI_["centrifuge_g"]`.')
    sq("exec", 'Post-clarification turbidity stayed at or below `{python} n2(max(MAX_CLAR_RCF, PREVR.max()))` NTU across '
               'the whole range of centrifugation (rcf) and across depth filter load up to '
               '`{python} pv("depth_filter_load", PREV_DFL)`.')
    sq("exec", 'Both runs at `{python} pv("depth_filter_load", TOP_DFL)` exceeded the clarification limit of '
               '`{python} CLAR_`.')
    sq("exec", 'Across the NOR of centrifugation (rcf) the change in post-clarification turbidity, '
               '`{python} n2(PS_CRCF["chg"])` NTU, is smaller than the repeatability limit of the turbidity method, the '
               'smallest difference between two single results that the method tells apart.')
    sq("exec", "No slope against the setting was detected for host cell protein, residual DNA, aggregate, fragments or "
               "step yield in any of the three series, at α = `{python} ALPHA`.")
    sq("exec", "The A-Mab assumption is therefore kept.",
       extra=[("exec", "The study supports it for the parameters, the ranges and the attributes it measured, and it did "
                       "not measure the culture before harvest.")])
    sq("exec", 'The proven acceptable range of centrifugation (rcf) is the whole range studied, '
               '`{python} PAR_["centrifuge_g"]`, with `{python} pv("centrifuge_g", MARG["centrifuge_g"][0])` of margin '
               'at each end of its NOR.')
    sq("exec", 'The proven acceptable range of depth filter load is `{python} PAR_["depth_filter_load"]`, bounded by the '
               'clarification limit.',
       extra=[("exec", "The upper limit of its NOR lies on that edge, so the range leaves no margin above the NOR.")])
    sq("exec", 'The proven acceptable range of post-clarification turbidity, which is measured and not set, is '
               '`{python} PAR_["turbidity"]` for the attributes measured in the clarified harvest.',
       extra=[("exec", 'It does not cover the performance of Protein A capture, and a harvest setting must still deliver '
                       'turbidity within the NOR of `{python} NOR_["turbidity"]` (@sec-par).')])
    sq("exec", "Centrifugation (rcf) and depth filter load were classified as KPPs, because each changed the clarity of "
               "the feed to capture and no effect of either on a quality attribute was detected.")
    sq("exec", "Post-clarification turbidity was classified as a GPP.")
    sq("exec", "No parameter of the step is a CPP or a WC-CPP.")
    sq("exec", 'At `{python} WARM` the held clarified harvest gained `{python} n2(HC[("lmw_cesds_pct", WARM)]["end"])` '
               'percentage points of fragments, `{python} n2(HC[("acidic_pct", WARM)]["end"])` of acidic variants and '
               '`{python} n2(HC[("hmw_pct", WARM)]["end"])` of aggregate in `{python} HOLD_D` days.',
       extra=[("exec", "At `{python} COLD` the changes were smaller.")])
    sq("exec", "The held pool was judged against the criteria for the load of Protein A capture.")
    sq("exec", "For each attribute the highest level expected to enter the hold was added to the largest change from day "
               "`{python} DAYS[0]`, by rules this report chose after the results were known (@sec-stats).")
    sq("exec", "Aggregate, fragments and the upper limit for acidic variants met their criteria.")
    sq("exec", "The lowest level of acidic variants expected to enter the hold already lies below the lower limit, and "
               "PCR-003 reports that result with the acceptance of its risk.")
    sq("exec", "In a Monte Carlo simulation of the whole train through the step models, the drug substance Cpk for "
               "fragments is `{python} n2(CPK_FRAG)`, above the target of `{python} CPK_TARGET` set in PCMP-001.")
    sq("exec", "Version 1.0 recorded two study events in S-HAR-UNI, a depth filter flush turbidity above its alert "
               "limit (DEV-004-01) and a post-clarification turbidity above the NOR on one run (DEV-004-02).",
       extra=[("exec", "That study has no data in the record, so neither event bears on this report.")])

    # -- Introduction ----------------------------------------------------------------------------------------
    sq("uo", "At commercial scale it is run once per batch on the contents of a `{python} SCALE_L` L production "
             "bioreactor.")
    sq("uo", "Its settings change the feed to Protein A capture in two ways.",
       extra=[("uo", "A clarification that removes fewer cells and less debris passes more fine material to capture."),
              ("uo", "An operation that breaks more cells releases more host cell protein and DNA into the clarified "
                     "harvest.")])
    sq("uo", "Proteases released by dead and lysing cells clip the antibody in the reactor, and clipping continues in "
             "the clarified harvest, because clarification removes the cells but not the proteases already in solution.")
    sq("uo", "PCMP-001 sets no criterion for fragments at harvest, and fragments are judged at the downstream steps "
             "(PCMP-001 Table 7.1).")
    src_all = _source()
    obj_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n## Objectives", 1)[1].split("\n## ", 1)[0], flags=re.M)
    if len(obj_list) != 5:
        raise ValueError(f"{DOC}: {len(obj_list)} numbered objectives under '## Objectives', the text says five")
    sq("objectives", "PCP-004 §2 set five objectives for the study, given here in its numbering:",
       "PCP-004 §2 set five objectives for the study, given in the report in its numbering.")
    for i, obj in enumerate(obj_list, 1):
        st("objectives", f"Objective {i} of PCP-004 §2: {clean(q(obj))}", [ref("objectives", q(obj))])
    sq("objectives", "Objective 1, the qualification of the scale-down model, was not met, because no qualification "
                     "was made (@sec-sdm).")
    sq("objectives", "Objective 2, the effect of the field, was met in part.",
       extra=[("objectives", "The effect of the field on the clarity of the centrate was established, and no effect on "
                             "host cell protein or DNA in the clarified harvest was detected (@sec-res-rcf)."),
              ("objectives", "The release by cell breakage itself was not established, because the culture before "
                             "harvest was not sampled (PD-004-04).")])
    sq("objectives", "Objective 3, the effect of depth filter load, was met for the particulate content of the clarified "
                     "harvest and not for the filter pressure, which was not measured (PD-004-05).")
    sq("objectives", "Objective 4, whether the step alters the size variants and how turbidity affects the material "
                     "presented to capture, was met in part.",
       extra=[("objectives", "The study shows whether a parameter changed aggregate or fragments in the clarified "
                             "harvest, but it did not measure the antibody before the step, and the Protein A load "
                             "challenge that was to show the effect of turbidity on capture was not run "
                             "(@sec-univariate).")])
    sq("objectives", "Objective 5, the proven acceptable ranges and the evidence for the classes, was met within the "
                     "limits stated in @sec-par.")
    sq("basis", "The study is part of the Stage 1 process design record of the commercial process")
    sq("basis", "Criticality is treated as a continuum, as ICH Q8(R2) describes")
    sq("basis", "A proven acceptable range is the range of a parameter over which the step has been shown to meet its "
                "criteria, with the other parameters held at their set-points")
    sq("basis", "The case study notes that the assumption might not hold in a real process.")
    sq("changes", "Version 1.0 of this report was approved on `{python} V1_DATE`.")
    sq("changes", 'QA opened the investigation on `{python} INV["opened"]`, after its review of the master report '
                  'PCMR-001 Version 1.0 for BLA readiness, and closed it on `{python} INV["closed"]` with the '
                  'classification `{python} INV["classification"]`.')
    sq("changes", "The investigation found that the criteria used to judge each step in the proven acceptable range "
                  "analysis had been set after the data were seen and were in no approved protocol (INV-001 finding 1).")
    sq("changes", "Version 1.0 applied no such criterion to this step, and PCMP-001 Version 2.0 sets no intermediate "
                  "acceptance criterion for the clarified harvest (@sec-attributes).")
    sq("changes", "This revision changes the report in seven ways.")
    sq("changes", "This revision reports the univariate study S-HAR-UNI2, made from `{python} WIN[UNI2]`, after INV-001 "
                  "closed (PD-004-01).",
       extra=[("changes", "Every parameter effect, proven acceptable range and class in this report rests on "
                          "S-HAR-UNI2.")])
    sq("changes", "The clarified harvest was held at two temperatures for `{python} HOLD_D` days in study S-HAR-HLD, "
                  "from `{python} WIN[HLD]` (PD-004-02).")
    sq("changes", "The drug substance CQA register of Version 2.0 assigns fragments to this step.",
       extra=[("changes", 'S-HAR-UNI2 and S-HAR-HLD measured them by nrCE-SDS, the method PCMP-001 Version 2.0 sets for '
                          'fragments at every step after the analytical method decision `{python} AMD["id"]` of '
                          '`{python} AMD["date"]` (PCMP-001 §7.8).')])
    sq("changes", "S-HAR-UNI closed before that decision and did not measure fragments.")
    sq("changes", "The qualification that PCP-004 required before the first characterization run was not made.",
       extra=[("changes", "This revision records it as discrepancy PD-004-03 and states every result at the scale of "
                          "the study.")])
    sq("changes", "The two events of execution that Version 1.0 recorded keep their numbers, DEV-004-01 and DEV-004-02, "
                  "and are reported as study events.")
    sq("changes", "The records of Version 1.0 gave no execution dates (INV-001 finding 5), and the execution window of "
                  "each study is now recorded.")
    sq("changes", "S-HAR-UNI ran from `{python} WIN[UNI1]`, after PCP-004 Version 1.0 was approved on `{python} PLAN_V1`.")
    sq("changes", 'Version 1.0 gave the whole range studied, `{python} RNG_["depth_filter_load"]`, as the proven '
                  'acceptable range of depth filter load, with the NOR of every parameter inside its proven acceptable '
                  'range.',
       extra=[("changes", 'In this revision the range ends at '
                          '`{python} pv("depth_filter_load", PAR["depth_filter_load"][1])`, and the upper limit of the '
                          'NOR lies on its edge (@sec-par).')])
    sq("changes", "Version 1.0 also described a qualified scale-down model with a laboratory disk-stack centrifuge and "
                  "no difference between the scales.",
       extra=[("changes", "No such centrifuge exists, and no qualification was made.")])
    sq("changes", "The classes of the three parameters are unchanged.")

    # -- Prior knowledge and quality risk basis --------------------------------------------------------------
    sq("platform", "It was used for three earlier antibodies, X-Mab, Y-Mab and Z-Mab, and the equipment, the grade of "
                   "the filter media and the control scheme are unchanged for A-Mab (PCP-004 §4.1).")
    sq("platform", "They give the direction in which each parameter is expected to act, and the size of each effect for "
                   "A-Mab is what this study measured.")
    sq("platform", "A higher field therefore clarifies more completely.", extra=[("platform", "It can also break more cells.")])
    sq("platform", "Cells broken in the feed zone release host cell protein and DNA into the centrate, and they leave fine "
                   "debris that is harder to capture.")
    sq("platform", "As retained solids fill the void space of the matrix and occupy its charged sites, the pressure drop "
                   "rises and more fine material passes.")
    sq("platform", "It matters because this material reaches the Protein A column, where it fouls the bed and shortens "
                   "the working life of the resin.")
    sq("platform", "Harvest does not clear host cell protein.")
    sq("platform", "Within normal operation that exposure is brief, so aggregate is not expected to change.")
    sq("platform", "It continues in the clarified harvest, and its rate rises with temperature, so a harvest held cold "
                   "clips more slowly than one held at room temperature.")
    sq("platform", "That source rises with cell lysis and shear, and so it could rise with the field.")
    sq("platform", "PCP-004 keeps the assumption, and the criteria of PCMP-001 Version 2.0 rest on it (@sec-attributes).")
    exp_src = src_all.split("Three expectations follow for the study:", 1)[1].split("\n## ", 1)[0]
    exp_list = re.findall(r"^\d+\. (.+)$", exp_src, flags=re.M)
    if len(exp_list) != 3:
        raise ValueError(f"{DOC}: {len(exp_list)} expectations, the text says three")
    for i, e in enumerate(exp_list, 1):
        st("platform", f"Expectation {i} of the study: {clean(q(e))}", [ref("platform", q(e))])
    for key in ckeys:
        r = cq_df.loc[key]
        srow("cqa", f"{names[key]} is in scope at harvest: drug substance criterion {_unmark(r['Acceptance'])}, "
                    f"criticality {r['Criticality']}, Tool #1 score {r['Tool #1']}.", crow[key], cq_t, crow)
    sq("cqa", "PCP-004 placed four of these attributes in scope.")
    sq("cqa", "It is measured because DNA fragments and nucleosomes foul depth filters and Protein A resin, so it "
              "describes the condition of the feed.")
    sq("cqa", "Against its drug substance criterion, the DNA clearance credited downstream exceeds what the train must "
              "remove by about `{python} n1(DNA_MARGIN)` log10 (@sec-capability).")
    sq("cqa", "The derivation of PCMP-001 §7.3 credits harvest with no change in any attribute, so the criteria of the "
              "production bioreactor output pass through it unchanged to the load of Protein A capture.")
    sq("cqa", "For aggregate that criterion is `{python} AGG_C_`.",
       extra=[("cqa", "It is the drug substance criterion of ≤ `{python} gn(AGG_DS)` % carried back through three "
                      "steps.")])
    sq("cqa", 'These are the aggregate increase of UF/DF (`{python} n2(AGG_UFDF["predicted_nor_bound95"])` percentage '
              'points), the aggregate clearance of cation exchange (`{python} n2(AGG_CEX["predicted_nor_bound95"])`-fold) '
              'and the aggregate increase of low-pH viral inactivation (`{python} n2(AGG_VI["predicted_nor_bound95"])` '
              'percentage points).',
       extra=[("cqa", "All three are values verified for A-Mab at manufacturing scale (PCMP-001 §7.5).")])
    sq("cqa", "PCMP-001 had assumed that no step after cation exchange changes aggregate, and the increase across UF/DF "
              "replaces that assumption.")
    sq("cqa", 'The aggregate criterion is stricter than ≤ `{python} n2(agg_row["iac_high_apriori"])` %, the value carried '
              'back through the platform worst cases before they were verified for A-Mab.')
    sq("cqa", 'For acidic variants the criterion is `{python} ACID_C_`, the drug substance criterion of '
              '`{python} n1(ACID_DS[0])`–`{python} n1(ACID_DS[1])` % carried back through the platform increase of low-pH '
              'viral inactivation (`{python} n2(acid_row["downstream_added"])` percentage points).')
    sq("cqa", "These criteria rest on the assumption that harvest changes no attribute, and this report uses them to "
              "judge the held clarified harvest (@sec-hold).")
    sq("cqa", "Fragments have no criterion at harvest or at the production bioreactor.")
    sq("cqa", "Residual DNA has no intermediate acceptance criterion at any step, because the platform history gives no "
              "worst-case DNA clearance for the steps after Protein A, so no criterion can be carried back (PCMP-001 "
              "§7.3).", extra=[("cqa", "It is judged on the drug substance only.")])
    sq("risk", "RA-001 ranked each parameter on its potential to affect a quality attribute and on its potential to "
               "interact with another parameter, and it assigned a study type from the combined ranking.")
    sq("risk", "It brought `{python} N_PAR` parameters of this step into scope and assigned each of them to univariate "
               "study.")
    sq("risk", "No parameter was ranked high enough to require a multivariate design, so no screening or response-surface "
               "design was run for this step (PCMP-001 §2).")
    sq("risk", "A poorly chosen setting at harvest was therefore expected to load capture more heavily without changing "
               "the drug substance.")
    sq("risk", "For post-clarification turbidity the lower edge of the range studied is the lower limit of the NOR, and "
               "only the upper edge extends beyond it.")
    sq("risk", "A range that stops at the NOR limits cannot show where the operation begins to fail, and an excursion "
               "beyond a NOR limit would then have no data behind it.")

    # -- Materials and methods ------------------------------------------------------------------------------
    sq("sdm", "Cell damage in the feed zone was to be reproduced in a bench shear device at the energy dissipation rate "
              "calculated for the commercial feed zone.")
    sq("sdm", "Sedimentation was to be reproduced in a laboratory centrifuge at the relative centrifugal field of the "
              "commercial bowl and at a matched ratio of flow to sigma factor.")
    sq("sdm", "Depth filtration was to be reproduced with disks of the commercial filter media, at the same flux and to "
              "the same load per unit area.")
    sq("sdm", "The plan required the model to be qualified against the commercial train under SOP-1001 before the first "
              "characterization run.")
    sq("sdm", "The results of the univariate study S-HAR-UNI2 and the hold study S-HAR-HLD are therefore reported at the "
              "scale of the study, with no offset to manufacturing scale.")
    sq("sdm", "PCMP-001 §5 asks a report to state the consequence where the model is not qualified for an output.")
    sq("sdm", "The proven acceptable range of depth filter load, which that limit bounds (@sec-par), is therefore a range "
              "at the scale of the study, and the capacity of the commercial filter train per unit area may differ.")
    sq("sdm", "PCP-004 had left this output out of the planned comparison, so its offset would have been unknown even "
              "with a qualified model.")
    sq("sdm", "No criterion depends on them, and their offsets would only have been recorded (PCMP-001 §7.1).")
    sq("sdm", "The conclusions on these attributes are that no parameter changed them within the range studied.",
       extra=[("sdm", "An offset that is the same at every level of a series, as a difference or as a ratio, leaves a "
                      "slope of zero at zero, and the conclusions rest on that."),
              ("sdm", "A scale effect that differs between levels would not be seen.")])
    sq("sdm", "A rise of host cell protein or DNA with the field could therefore be steeper at commercial scale than at "
              "the scale of the study.")
    sq("sdm", "The changes over the hold are differences within one pool.")
    sq("sdm", "The study therefore uses its results to bound ranges and to establish the direction and the approximate "
              "size of each effect, as PCP-004 §5.1 intended.")
    sq("operation", "Each run is a single pass of the whole harvest through the model train, in the order of the "
                    "commercial operation.")
    sq("operation", "The culture is taken from the production bioreactor scale-down model at the end of culture, at the "
                    "conditions characterized in PCP-003.")
    sq("operation", "Temperature is held at the commercial set-point throughout, and the time between the end of culture "
                    "and the end of clarification is held constant.")
    sq("operation", "The record of the univariate study S-HAR-UNI2 gives, for each run, the parameter varied, its level "
                    "and setting, the replicate and the results.")
    sq("operation", "It holds none of the records of execution that PCP-004 required (PD-004-07).")
    sq("operation", "The record also does not name the culture of each run, so the analysis by culture that PCP-004 §12 "
                    "provides for a series run on more than one culture could not be made.")
    sq("analytics", 'The qualified performance of that method is recorded under AMV-3221, with a precision of '
                    '`{python} gn(SEC_Q["precision_pct"])` % RSD for a single result and a limit of quantitation of '
                    '`{python} n2(SEC_Q["loq"])` % HMW.')
    sq("analytics", "Host cell protein and DNA are reported per mg of antibody, so they rest on that concentration too.")
    sq("analytics", "Fragments were measured by nrCE-SDS on every sample of the univariate study S-HAR-UNI2 and the hold "
                    "study S-HAR-HLD, and neither study has a fragment result by SEC.")
    sq("analytics", "That bias grows with the host cell protein present, and a clarified harvest carries more host cell "
                    "protein than any later intermediate.")
    for i, row in enumerate(resp_rows):
        c = _cells(row)
        if text.count(normalize(row)) != 1:
            continue
        study = next(_cells(resp_rows[j])[0] for j in range(i, -1, -1) if _cells(resp_rows[j])[0])
        sample = next(_cells(resp_rows[j])[1] for j in range(i, -1, -1) if _cells(resp_rows[j])[1])
        meth = _unmark(c[3])
        resp_ = c[2][0].lower() + c[2][1:]
        srow("analytics", f"In {study}, {resp_} of the {sample.lower()} was a response, "
             + ("with no method named." if meth == "none named" else f"measured by {meth}."), row, resp_t, resprow)
    sq("sampling", "PCP-004 §5.4 planned four sample points in every run.",
       extra=[("sampling", "They were the unclarified culture before the feed to the centrifuge starts, the centrate, the "
                           "filtrate after depth filtration and the clarified harvest after sterilizing-grade filtration "
                           "(PCP-004 Appendix B).")])
    sq("sampling", "The unclarified culture was to be the reference against which impurity release and any change in the "
                   "size variants are judged.")
    sq("sampling", "The record of the univariate study S-HAR-UNI2 holds results for the clarified harvest and the "
                   "turbidity of the centrate.")
    sq("sampling", "It holds no result for the unclarified culture or for the filtrate after depth filtration, and no host "
                   "cell protein or DNA result for the centrate, because these samples were not scheduled in the study "
                   "record (PD-004-04).")
    sq("sampling", "In the turbidity series the centrate turbidity is not reported, because the material of each level was "
                   "prepared by adding centrate (@sec-univariate).")
    sq("sampling", "The set-point condition appears in the centrifugation (rcf) and the depth filter load series, which "
                   "gives `{python} N_SPR` runs at which every parameter was at its set-point and the clarified harvest "
                   "was not adjusted.")
    sq("sampling", "Each sample was tested for aggregate by SEC, fragments by nrCE-SDS and acidic variants by icIEF.")
    sq("stats", "Each response of the univariate study S-HAR-UNI2 was analysed against the setting of the parameter "
                "varied in its series, by linear regression on the `{python} N_PER` runs of the series.")
    sq("stats", "The `{python} N_SPR` runs with every parameter at set-point give that estimate on `{python} DF_SP` degrees "
                "of freedom, and the slopes are tested, and their intervals calculated, against it.")
    sq("stats", "A response is affected by a parameter when its slope is significant at that level.")
    sq("stats", "No threshold is set for either, and no decision rests on them.")
    sq("stats", "With the residual error of the regression, on `{python} DF_RES` degrees of freedom, in place of the "
                "set-point replicates, the same slopes are significant and no other.")
    sq("stats", "Each change is reported over the whole range studied, as the slope times the width of the range, with "
                "its 95 % confidence interval.")
    sq("stats", "PCP-004 sets no size for the smallest difference a method tells apart (PD-004-08).",
       extra=[("stats", "This report takes it as the repeatability limit, the difference that two single results exceed "
                        "by chance with a probability of 5 %.")])
    sq("stats", "The study made `{python} N_TESTS` such tests, apart from the check of the turbidity challenge "
                "(@sec-res-turbidity).")
    sq("stats", "PCP-004 §5.5 allows a quadratic term where the relationship is not linear, and it names no test for "
                "curvature.", extra=[("stats", "None was fitted.")])
    sq("stats", "The variation between the set-point replicates does not include such a departure from a straight line, "
                "so for a response that is not linear the interval of the slope understates its uncertainty.")
    sq("stats", "Every result of turbidity, host cell protein and DNA lies above the limit of quantitation of its method, "
                "so no result was excluded.")
    sq("stats", "This report therefore judges both criteria on the slope against the setting, the analysis PCP-004 §5.5 "
                "sets for every response.")
    sq("stats", "PCMP-001 Version 2.0 §5 judges a held pool against the criteria it must meet on entering the next step.")
    sq("stats", "Two rules of the judgement are this report's own, chosen after the results of the hold study S-HAR-HLD "
                "were known.")
    sq("stats", "For aggregate and acidic variants it is the end of the two-sided 95 % prediction interval of a single "
                "batch over the NOR of the production bioreactor, at manufacturing scale (PCR-003).")
    sq("stats", "For fragments, which the bioreactor designs did not measure, it is the highest result of S-HAR-UNI2.")
    sq("stats", "The expected level after the hold is the level that enters plus that change, and it meets the criterion "
                "or it does not.")
    sq("stats", "A change smaller than the difference between the two results of the pool on day `{python} DAYS[0]` is "
                "not taken as resolved.")

    # -- Study design ---------------------------------------------------------------------------------------
    for k in KEYS:
        c = _cells(prow[k])
        srow("factors", f"{NAME[k]} ({UNIT[k]}): set-point {c[2]}, NOR {c[3]}, range studied {c[4]}, class {c[5]}; "
                        f"studied one factor at a time.", prow[k], pt_t, prow)
    sq("factors", "The set-points and the NORs are those against which the study was planned.",
       extra=[("factors", "None was changed at Version 2.0.")])
    sq("factors", "Post-clarification turbidity is the response of the other two parameters, so its range is the range of "
                  "turbidity presented to capture, not a range of settings dialled in at the centrifuge.")
    sq("uni_design", "S-HAR-UNI2 also measured fragments, which PCP-004 does not name as a response of its study.")
    sq("uni_design", "For depth filter load they are the same.")
    sq("uni_design", 'For centrifugation (rcf) the two inner levels, `{python} pv("centrifuge_g", EXTRA["centrifuge_g"][0])` '
                     'and `{python} pv("centrifuge_g", EXTRA["centrifuge_g"][1])`, lie outside the NOR of '
                     '`{python} NOR_["centrifuge_g"]`.')
    sq("uni_design", 'For post-clarification turbidity the levels of `{python} pv("turbidity", EXTRA["turbidity"][0])` and '
                     '`{python} pv("turbidity", EXTRA["turbidity"][1])` were run in place of the upper NOR limit of '
                     '`{python} NORHI_["turbidity"]` that the plan named.')
    sq("uni_design", "Of the NOR limits, `{python} NOTRUN_TXT` were therefore not run as levels.",
       extra=[("uni_design", "In both series the NOR lies between levels that were run, so the ranges of @sec-par still "
                             "cover it.")])
    sq("uni_design", "Three elements of the planned design were not run.",
       extra=[("uni_design", "The depth filter load series was run once, on centrate from the set-point field, and the "
                             "turbidity series on material from it (PD-004-06).")])
    sq("uni_design", "The range of depth filter load in @sec-par therefore holds for centrate produced at the set-point "
                     "field.")
    sq("uni_design", "In the turbidity series the clarified filtrate was adjusted to each level with centrate, the "
                     "turbidity of each preparation was measured, and the attributes were recorded.")
    sq("uni_design", "Material prepared this way carries the particle size distribution of the centrate it was made from, "
                     "which is not the distribution that a depth filter at the end of its capacity would pass.")
    sq("hold_design", "PCP-004 placed the hold of the clarified harvest outside its scope (PCP-004 §1), and Version 1.0 of "
                      "the plan did not foresee a hold study.")

    # -- Results --------------------------------------------------------------------------------------------
    sq("repro", "The duplicates of turbidity, host cell protein and DNA scattered by about the precision of their "
                "methods, with pooled relative standard deviations of "
                '`{python} n1(POOL["clarified_turbidity_ntu"][0])`, `{python} n1(POOL["hcp_out_ng_mg"][0])` and '
                '`{python} n1(POOL["dna_out_pg_mg"][0])` % against `{python} n1(METH["AMV-3015"]["precision_pct"])`, '
                '`{python} n1(METH["AMV-3012"]["precision_pct"])` and `{python} n1(METH["AMV-3014"]["precision_pct"])` % '
                'for a single result of the method.')
    sq("repro", "Assay variation is therefore most of the variation between runs of these responses.")
    sq("repro", 'Residual DNA had the widest scatter among the set-point runs, `{python} n1(SPCV["dna_out_pg_mg"])` % RSD, '
                'from `{python} sig3(DNA_SPR[0])` to `{python} sig3(DNA_SPR[1])` pg/mg.')
    for rk, row in reprow.items():
        if rk in ("centrate_turbidity_ntu", "clarified_turbidity_ntu", "step_yield_pct"):
            continue                                          # the rows of the performance measures
        c = _cells(row)
        srow("repro", f"{RLAB[rk]} in S-HAR-UNI2: mean {c[1]} and SD {c[2]} ({c[3]} % RSD) over the {N_SPR} runs at "
                      f"the set-point; pooled RSD of the duplicates at every level {c[4]} % on {c[5]} degrees of "
                      f"freedom; method precision {_unmark(c[6])} % RSD.", row, rep_t, reprow)
    sq("rcf", 'Centrate turbidity fell as the field rose, from a mean of `{python} n1(CEN[lo_g])` NTU at '
              '`{python} RLO_["centrifuge_g"]` to `{python} n1(CEN[sp_g])` NTU at the set-point and '
              '`{python} n1(CEN[hi_g])` NTU at `{python} RHI_["centrifuge_g"]`.')
    sq("rcf", "Most of the fall lay below the set-point.",
       extra=[("rcf", 'Of the fall of `{python} n1(CEN_FALL1)` NTU across the range, `{python} n0(100 * CEN_FRAC)` % took '
                      'place between `{python} RLO_["centrifuge_g"]` and `{python} SP_["centrifuge_g"]`.')])
    sq("rcf", 'The slope across the range was `{python} rr("centrifuge_g", "centrate_turbidity_ntu")` NTU (95 % '
              'confidence interval `{python} ci("centrifuge_g", "centrate_turbidity_ntu")` NTU, '
              '`{python} pR("centrifuge_g", "centrate_turbidity_ntu")`).')
    sq("rcf", "The results do not fall on a straight line.", extra=[("rcf", "They level off above the set-point.")])
    sq("rcf", 'The repeatability limit of the turbidity method at the mean of the set-point runs is '
              '`{python} n2(PS_CEN["res"])` NTU, so the change is material.',
       'Across the NOR of centrifugation (rcf) the slope gives a change in centrate turbidity of '
       '`{python} n1(PS_CEN["chg"])` NTU, against a repeatability limit of the turbidity method of '
       '`{python} n2(PS_CEN["res"])` NTU at the mean of the set-point runs, so the change is material.',
       extra=[("rcf", 'Across the NOR of `{python} NOR_["centrifuge_g"]` the slope gives a change of '
                      '`{python} n1(PS_CEN["chg"])` NTU.')])
    sq("rcf", 'Post-clarification turbidity fell slightly with the field, by '
              '`{python} n2(-REG[("centrifuge_g", "clarified_turbidity_ntu")]["chg"])` NTU across the range (95 % '
              'confidence interval `{python} ci("centrifuge_g", "clarified_turbidity_ntu")` NTU, '
              '`{python} pR("centrifuge_g", "clarified_turbidity_ntu")`).')
    sq("rcf", 'Across the NOR the slope gives a change of `{python} n2(PS_CRCF["chg"])` NTU, smaller than the '
              'repeatability limit of `{python} n2(PS_CRCF["res"])` NTU.',
       extra=[("rcf", "The effect is therefore detected and not material.")])
    sq("rcf", 'The highest result was `{python} n2(MAX_CLAR_RCF)` NTU, at `{python} pv("centrifuge_g", MAX_CLAR_RCF_AT)`, '
              'so every level met the clarification limit of `{python} CLAR_`.')
    sq("rcf", 'Host cell protein came closest, with a change of `{python} rr("centrifuge_g", "hcp_out_ng_mg")` ng/mg across '
              'the range (95 % confidence interval `{python} ci("centrifuge_g", "hcp_out_ng_mg")` ng/mg, '
              '`{python} pR("centrifuge_g", "hcp_out_ng_mg")`).')
    sq("rcf", "The interval includes no change, and its point estimate is a fall, not the rise that more cell breakage at "
              "a higher field would give.")
    clar_vals = list(clarrow.values())
    for i, row in enumerate(clar_vals):
        c = _cells(row)
        pk = "centrifuge_g" if i < int(ns["NLEV"]) else "depth_filter_load"
        srow("dfl" if pk == "depth_filter_load" else "rcf",
             f"{NAME[pk]} at {c[1]} {UNIT[pk]}: centrate turbidity {c[2]} NTU (mean {c[3]} NTU), post-clarification "
             f"turbidity {c[4]} NTU; clarification criterion met: {c[5]}.", row, clar_t, clarrow)
    st("rcf", fig_cap("fig-turbidity", 1), [ref("rcf", fig_cap("fig-turbidity", 1),
                                                 caption=fig_cap("fig-turbidity", 1), label="fig-turbidity")])
    sq("dfl", 'Post-clarification turbidity stayed between `{python} n2(DFL_LOW_RANGE[0])` and '
              '`{python} n2(DFL_LOW_RANGE[1])` NTU from `{python} RLO_["depth_filter_load"]` to '
              '`{python} pv("depth_filter_load", LOW3_DFL[-1])`.')
    sq("dfl", 'Both results at `{python} pv("depth_filter_load", PREV_DFL)`, `{python} n2(PREVR[0])` and '
              '`{python} n2(PREVR[1])` NTU, were higher than every result at the lower loads, and both lay below the '
              'limit.')
    sq("dfl", 'Both results at `{python} pv("depth_filter_load", TOP_DFL)`, `{python} T.num(TOPR[0])` and '
              '`{python} T.num(TOPR[1])` NTU, exceeded the clarification limit of `{python} CLAR_`.')
    sq("dfl", 'Depth filter load therefore failed the clarification criterion at '
              '`{python} pv("depth_filter_load", TOP_DFL)` and met it at every lower level.')
    sq("dfl", 'Across the NOR of `{python} NOR_["depth_filter_load"]` the slope gives a change of '
              '`{python} n2(PS_CDFL["chg"])` NTU, and the level means changed by `{python} n2(DFL_NOR_MEAN_CHG)` NTU.',
       extra=[("dfl", 'Both exceed the repeatability limit of `{python} n2(PS_CDFL["res"])` NTU, so the effect is '
                      'material.')])
    sq("dfl", "The decision on the range rests on the individual results against the limit.")
    sq("dfl", 'No slope was detected for centrate turbidity (`{python} pR("depth_filter_load", "centrate_turbidity_ntu")`), '
              'as expected, because the centrate is made before the filter and the whole series used centrate from one '
              'field.')
    sq("dfl", 'The change in residual DNA across the range was `{python} rr("depth_filter_load", "dna_out_pg_mg")` pg/mg '
              '(95 % confidence interval `{python} ci("depth_filter_load", "dna_out_pg_mg")` pg/mg, '
              '`{python} pR("depth_filter_load", "dna_out_pg_mg")`).')
    sq("dfl", "The study therefore gives no evidence of such a change, at the precision of the qPCR and of the runs.")
    sq("turb", 'The measured turbidity of the prepared material tracked its target, with a slope of '
               '`{python} n2(REG[CHECK]["slope"])` NTU per NTU of target and an R² of `{python} n3(REG[CHECK]["r2"])`.')
    sq("turb", "The preparation therefore gave the challenge levels intended, from `{python} n2(TURB_MEAS[0])` to "
               "`{python} T.num(TURB_MEAS[1])` NTU.")
    sq("turb", 'Step yield came closest, with a change of `{python} rr("turbidity", "step_yield_pct")` percentage points '
               'across the range (95 % confidence interval `{python} ci("turbidity", "step_yield_pct")`, '
               '`{python} pR("turbidity", "step_yield_pct")`).')
    sq("turb", "No difference in these attributes of the material presented to capture was therefore detected across "
               "its turbidity.")
    sq("attrs", "Across the three series no slope was detected for any quality attribute at α = `{python} ALPHA`.")
    sq("attrs", 'The widest interval end reached `{python} n0(CI_REL["hcp_out_ng_mg"])` % of the set-point mean for host '
                'cell protein, `{python} n0(CI_REL["dna_out_pg_mg"])` % for residual DNA, '
                '`{python} n0(CI_REL["aggregate_out_pct"])` % for aggregate and `{python} n0(CI_REL["lmw_cesds_pct"])` % '
                'for fragments.', extra=[("attrs", "The data do not exclude a change of up to that size across a range.")])
    sq("attrs", "The comparison is least precise for residual DNA, whose method and runs scatter most "
                "(@sec-reproducibility).")
    sq("attrs", 'Across all `{python} N_RUNS` runs, aggregate ranged from `{python} n2(BAND["aggregate_out_pct"][0])` to '
                '`{python} n2(BAND["aggregate_out_pct"][1])` %, well below `{python} AGG_C_`, the aggregate criterion of '
                'the production bioreactor output, which passes through harvest unchanged.')
    sq("attrs", 'Fragments ranged from `{python} n2(BAND["lmw_cesds_pct"][0])` to `{python} n2(BAND["lmw_cesds_pct"][1])` '
                '%, below the drug substance criterion of `{python} FRAG_C_`.')
    sq("attrs", 'The `{python} N_SPR` set-point runs of S-HAR-UNI2 averaged `{python} n2(FRAG_SP)` % fragments, and the '
                'process model at set-point carries `{python} n2h(FRAG_NOM["bioreactor"])` % at the end of culture.')
    sq("attrs", "These results keep the A-Mab assumption that harvest has no impact on product quality",
       extra=[("attrs", "Turbidity responded to the parameters, and no effect on the attributes was detected within the "
                        "ranges studied, at the precision of the runs.")])
    sq("attrs", "The support has three limits.",
       extra=[("attrs", "The study measured the attributes in the clarified harvest only, so the change across the "
                        "step, against the culture before harvest, was not measured."),
              ("attrs", "Each parameter was varied with the others at their set-points, so no combination of two "
                        "parameters away from their set-points is covered.")])
    sq("attrs", "The criteria of the production bioreactor output pass through harvest unchanged (@sec-attributes), and "
                "that use assumes the step itself changes no attribute.")
    st("attrs", fig_cap("fig-attributes", 1), [ref("attrs", fig_cap("fig-attributes", 1),
                                                    caption=fig_cap("fig-attributes", 1), label="fig-attributes")])
    hold_vals = list(holdrow.values())
    temps = list(ns["TEMPS"])
    for i, row in enumerate(hold_vals):
        c = _cells(row)
        temp = temps[i // len(ns["DAYS"])]
        srow("hold", f"Clarified harvest held at {temp}, day {c[1]}: aggregate (HMW, SEC) {c[2]} %, fragments (LMW, "
                     f"nrCE-SDS) {c[3]} %, acidic variants {c[4]} %.", row, hold_t, holdrow)
    sq("hold", 'Fragments rose at every time point, from `{python} n2(HC[("lmw_cesds_pct", WARM)]["d0"])` % on day '
               '`{python} DAYS[0]` to `{python} n2(HC[("lmw_cesds_pct", WARM)]["vals"][-1])` % on day `{python} HOLD_D`, '
               'by `{python} n2(HC[("lmw_cesds_pct", WARM)]["end"])` percentage points.')
    sq("hold", 'Acidic variants rose by `{python} n2(HC[("acidic_pct", WARM)]["end"])` percentage points, all of it after '
               'day `{python} DAYS[1]`, and aggregate by `{python} n2(HC[("hmw_pct", WARM)]["end"])`.')
    sq("hold", "At `{python} COLD` neither aggregate nor acidic variants showed a trend.")
    sq("hold", 'Acidic variants stayed within `{python} n2(ACID_COLD_MAX)` percentage points of their result on day '
               '`{python} DAYS[0]`, which is less than the standard deviation of a single icIEF result at that level, '
               '`{python} n2(ICIEF_SD)` points.')
    sq("hold", 'That change is a little larger than the `{python} n2(D0DIFF["lmw_cesds_pct"])` points between the two '
               'results of the pool on day `{python} DAYS[0]`.')
    sq("hold", "The largest change of fragments from day `{python} DAYS[0]` was `{python} n1(WARM_COLD_FRAG)` times as "
               "large at `{python} WARM` as at `{python} COLD`.")
    sq("hold", 'The pool entered the hold with `{python} n2(H_D0_AGG[0])` and `{python} n2(H_D0_AGG[1])` % aggregate on day '
               '`{python} DAYS[0]`, below every set-point run of S-HAR-UNI2, whose mean was '
               '`{python} n2(SPSTAT["aggregate_out_pct"][0])` %, and its culture is not recorded (@sec-hold-design).')
    sq("hold", "Each change over the hold is added to the level expected to enter it, the highest for an upper limit and "
               "the lowest for the lower limit of acidic variants.")
    sq("hold", 'After `{python} HOLD_D` days at `{python} WARM` the expected level of aggregate is `{python} n2(HA["after"])` '
               '%, against the criterion of `{python} AGG_C_`, and the expected level of fragments is '
               '`{python} n2(HF["after"])` %, against `{python} FRAG_C_`.')
    sq("hold", 'The upper limit for acidic variants is met, at `{python} n1(HAU["after"])` % against '
               '`{python} n1(ACID_C[1])` %.', extra=[("hold", "The lower limit is not met.")])
    sq("hold", 'The lowest level expected to enter the hold, `{python} n1(ENTER[("acidic_pct", "lower")])` %, already lies '
               'below the lower limit of `{python} n1(ACID_C[0])` %, and PCR-003 reports that result for the production '
               'bioreactor with the acceptance of its risk.')
    cur_attr, cur_lim, cur_ent = "", "", ""
    for row in hj_rows:
        c = _cells(row)
        cur_attr = _unmark(c[0]) or cur_attr
        cur_lim = _unmark(c[2]) or cur_lim
        cur_ent = c[3] or cur_ent
        srow("hold", f"{cur_attr}, {cur_lim} limit, held {ns['HOLD_D']} days at {c[4]}: level entering the hold "
                     f"{_unmark(cur_ent)}, largest change {c[5]}, expected level after the hold {c[6]}; met: "
                     f"{_unmark(c[7])}.", row, hj_t, hjrow)
    sq("mech", "A higher field raises the settling velocity of cells and debris, so more of them reach a disc and are "
               "captured before the fluid leaves the stack.")
    sq("mech", "That is consistent with a remaining turbidity carried by particles too small to settle in the time "
               "available at any field studied.")
    sq("mech", "No rise in host cell protein or DNA was detected at the higher fields.")
    sq("mech", "A higher field passed less turbidity to the depth filter, which then had less fine material to pass.")
    sq("mech", "The second effect the mechanism allows, finer debris from broken cells, was not seen, which agrees with "
               "the absence of a detected rise in host cell protein and DNA.")
    sq("mech", "This is the shape the mechanism predicts for media that approach saturation, in which retained solids fill "
               "the void space and occupy the charged sites until fine material passes.")
    sq("mech", 'The study places the onset of the rise between `{python} pv("depth_filter_load", PREV_DFL)` and '
               '`{python} pv("depth_filter_load", TOP_DFL)` for centrate made at the set-point field.')
    sq("mech", "Centrate from a lower field carries more turbidity (@sec-res-rcf) and is expected to saturate the media at "
               "a lower load.", extra=[("mech", "The bracket that PCP-004 planned in order to measure this was not run.")])
    sq("mech", 'Across the range of centrifugation (rcf) fragments changed by `{python} rr("centrifuge_g", "lmw_cesds_pct")` '
               'percentage points (95 % confidence interval `{python} ci("centrifuge_g", "lmw_cesds_pct")`, '
               '`{python} pR("centrifuge_g", "lmw_cesds_pct")`), so the data show no dependence on the field at that '
               'precision.')
    sq("mech", "The hold study showed that fragments depend on temperature, as clipping by proteases predicts.")
    sq("mech", "Acidic variants followed the same pattern, because deamidation also runs faster at a higher temperature.")
    sq("mech", "The time and the temperature of the hold therefore change how far fragments and acidic variants rise "
               "before capture.")

    # -- Design space, proven acceptable ranges --------------------------------------------------------------
    sq("ds", "A design space is a multivariate region, and no multivariate design was run here (PCP-004 §8).")
    sq("ds", "One interaction is expected on mechanistic grounds.",
       extra=[("ds", "A lower field passes more solids to the depth filter and would bring the capacity of the media "
                     "forward, so the range of depth filter load holds for centrate produced at the set-point field.")])
    sq("ds", "Operation outside a NOR and inside the proven acceptable range is supported by this study for the "
             "attributes it measured, and a planned change is assessed under change control")
    sq("par", "PCP-004 §7 sets four decision criteria.",
       extra=[("par", "They are those of Version 1.0, in its words, and no result of the studies was used to set or "
                      "change them.")])
    sq("par", "A level passes when no increase is detected at α = `{python} ALPHA`, or when a detected increase is "
              "smaller than the method can resolve.")
    sq("par", "With no result for the unclarified culture, a parameter passes over its range where no slope against the "
              "setting is detected for either impurity (@sec-stats).")
    sq("par", "The criterion asks whether a harvest setting delivers clarified harvest within the NOR.")
    sq("par", "The basis of `{python} CLAR_` is the NOR itself, which is set from production experience.",
       extra=[("par", "It is not derived from a measured effect on Protein A capture.")])
    sq("par", "In the turbidity series the turbidity is the challenge level itself, so the criterion does not apply "
              "there.")
    sq("par", "With no result before the step, a parameter passes over its range where no slope against the setting is "
              "detected for aggregate.")
    sq("par", "Step yield is reported and not gated.",
       extra=[("par", 'Every result lay between `{python} n1(BAND["step_yield_pct"][0])` and '
                      '`{python} n1(BAND["step_yield_pct"][1])` %, against a mean of `{python} n1(YIELD_SP)` % for the '
                      'set-point runs, and no slope against the setting was detected for it in any series.')])
    sq("par", "A parameter meets the criteria over a range when every level in that range passes the first three.",
       extra=[("par", "Where a level fails, the range is bounded at the last level that passed (PCP-004 §7 and §8).")])
    sq("par", "PCP-004 §8 left four rules to this report (PD-004-08).")
    sq("par", "A size for the smallest difference a method tells apart in the impurity release criterion is not needed, "
              "because no slope was detected for host cell protein or DNA.")
    sq("par", "For post-clarification turbidity, whose series is a challenge, the range is decided by the impurity release "
              "and product quality criteria alone.")
    sq("par", "A rule to combine two depth filter load series, on centrate from `{python} RLO_[\"centrifuge_g\"]` and from "
              "`{python} RHI_[\"centrifuge_g\"]`, is not needed, because only one series was run.")
    for k in KEYS:
        r0, r1 = _cells(par_of[k][0]), _cells(par_of[k][1])
        srow("par", f"{NAME[k]} ({UNIT[k]}), impurity release and product quality by slope: result closest to the "
                    f"criterion {r0[4]}; PAR {r0[5]} against a range studied of {r0[1]} and a NOR of {r0[2]}, margin to "
                    f"the NOR {r0[6]} (below / above).", par_of[k][0], par_t, parrow)
        srow("par", f"{NAME[k]} ({UNIT[k]}), clarification criterion"
                    + (f" ({r1[3].split(', ', 1)[1]})" if ", " in r1[3] else "") + f": {_unmark(r1[4])}.",
             par_of[k][1], par_t, parrow)
    sq("par", "Centrifugation (rcf) met the clarification criterion at every level, and no slope was detected in its "
              "series for the impurities or for aggregate.")
    sq("par", 'Depth filter load failed the clarification criterion at `{python} pv("depth_filter_load", TOP_DFL)`.',
       extra=[("par", "The upper limit of the NOR coincides with that edge.")])
    sq("par", "A NOR limit on the edge of the proven range leaves no margin for the ordinary variability of the "
              "commercial operation (PCP-004 §8).")
    sq("par", 'The lower limit of the NOR lies `{python} pv("depth_filter_load", MARG["depth_filter_load"][0])` inside the '
              'range.')
    sq("par", "PCP-004 §7 asks for a failure to be investigated before the range is reported, and the record holds no "
              "investigation beyond the results themselves.")
    sq("par", "The failure is therefore taken as the capacity of the media and not as an error of the runs.",
       extra=[("par", "The response rose steeply between the two highest levels, as the saturation of the media predicts "
                      "(@sec-mechanism).")])
    sq("par", "Post-clarification turbidity met the impurity release and product quality criteria over the whole range "
              "studied.")
    sq("par", "It is the range over which the turbidity challenge showed no effect on the attributes measured in the "
              "clarified harvest.")
    sq("par", 'A harvest setting must still deliver clarified harvest within the NOR of `{python} NOR_["turbidity"]`, and '
              'every batch is monitored against that NOR (@sec-control).')
    sq("par", 'The upper limit of the NOR lies `{python} pv("turbidity", MARG["turbidity"][1])` inside the range.')

    # -- Process capability and robustness ------------------------------------------------------------------
    sq("cap", "The capability of the drug substance comes from the Monte Carlo simulation of the whole train described "
              "in @sec-stats.")
    sq("cap", "No simulated batch fell outside any of these criteria.")
    sq("cap", "With none of `{python} cn(N_MC)` batches outside, the one-sided 95 % upper bound of the probability of an "
              "out of specification batch is `{python} n2(100 * UB0)` %.",
       extra=[("cap", "That bound covers the sampling of the simulation and not the uncertainty of the step models.")])
    sq("cap", "Fragments are the attribute that the register assigns to harvest.")
    sq("cap", 'The process model at set-point carries `{python} n2h(FRAG_NOM["bioreactor"])` % fragments at the end of '
              'culture and `{python} n2h(FRAG_NOM["ufdf"])` % in the drug substance.')
    sq("cap", "The set-point runs of S-HAR-UNI2 carried a mean of `{python} sig3(DNA_SP)` pg DNA per mg of antibody.")
    sq("cap", "The drug substance criterion is ≤ `{python} gn(DNA_DS)` ng per dose, so the purification train must remove "
              "about `{python} n1(DNA_LOG_NEEDED)` log10 of DNA.")
    sq("cap", 'The step models credit Protein A capture, cation exchange and anion exchange with '
              '`{python} gn(DNA_LRV["protein_a"])`, `{python} gn(DNA_LRV["cex"])` and `{python} gn(DNA_LRV["aex"])` log10 '
              'of DNA clearance.',
       extra=[("cap", "These clearances are inputs that the configuration of the process model sets, not results of this "
                      "study.")])
    sq("cap", "Host cell protein and aggregate depend in the same way on the purification steps that clear them.")

    # -- Parameter classification -------------------------------------------------------------------------
    sq("class", "Parameters were classified under SOP-4001 by the rule of PCMP-001 §7.7.")
    sq("class", "A parameter that affects a CQA is a CPP or a WC-CPP, and the two differ in the risk that the parameter "
                "falls outside its acceptable range in operation.")
    sq("class", "A parameter that affects process performance and no CQA is a KPP, and one that affects neither is a GPP.")
    sq("class", "Neither PCMP-001 nor SOP-4001 sets a numerical threshold for a practically relevant effect, so each class "
                "below states the size of each effect across the proven acceptable range and the margin of that range to "
                "the NOR.")
    sq("class", 'Across its proven acceptable range of `{python} PAR_["centrifuge_g"]` centrate turbidity changed by '
                '`{python} n1(PARCHG_CEN1)` NTU and post-clarification turbidity by `{python} n2(PARCHG_CRCF)` NTU, with '
                'every result below the clarification limit.')
    sq("class", 'It changed post-clarification turbidity by `{python} n2(PARCHG_CDFL)` NTU across its proven acceptable '
                'range of `{python} PAR_["depth_filter_load"]`, where every result lay between '
                '`{python} n2(DFL_LOW_RANGE[0])` and `{python} n2(PREVR[1])` NTU, and the turbidity exceeded the '
                'clarification limit at `{python} pv("depth_filter_load", TOP_DFL)`.')
    sq("class", 'Its basis is that over `{python} PAR_["turbidity"]` no effect on a quality attribute of the clarified '
                'harvest or on step yield was detected.')
    sq("class", "The mechanism expects turbidity to affect Protein A capture through fouling of the bed, and that effect "
                "was not measured, because the Protein A load challenge was not run (PD-004-05).")
    sq("class", "No effect of a parameter of this step on a CQA was detected within the range studied, so the step has no "
                "CPP and no WC-CPP.",
       extra=[("class", "This agrees with the A-Mab assumption that harvest has no impact on product quality.")])

    # -- Contribution to the control strategy -------------------------------------------------------------
    sq("cs", "Harvest contributes to the second.")
    sq("cs", "The upper limit of that NOR is the clarification limit.")
    sq("cs", "PCP-004 §5.3 makes it the measurement by which the clarified harvest is released to capture.")
    sq("cs", "Fragments have no criterion at harvest.")
    sq("cs", "The fragment level taken to enter the hold is not the highest expected in routine manufacture (@sec-stats).")

    # -- Discussion ---------------------------------------------------------------------------------------
    sq("disc", "The harvest train of A-Mab behaves as the platform mechanisms predict.")
    sq("disc", "Settling velocity rises with the centrifugal field, so less turbidity reaches the depth filter at a higher "
               "field, and most of that fall lies below the set-point.")
    sq("disc", 'The depth filter keeps its clarity until its load approaches the capacity of the media, which for centrate '
               'from the set-point field lies between `{python} pv("depth_filter_load", PREV_DFL)` and '
               '`{python} pv("depth_filter_load", TOP_DFL)` at the scale of the study.')
    sq("disc", "Fragments and acidic variants change with the time and the temperature of the hold, not with the "
               "operation of the step.")
    sq("disc", "Confidence in the scale-down model is the main limitation.")
    sq("disc", "The model was not qualified, so no output has a known offset from manufacturing scale, and the results "
               "give directions and approximate sizes, not commercial levels.")
    sq("disc", "With the upper NOR limit of depth filter load on the edge of its proven acceptable range, a lower capacity "
               "at commercial scale would place that limit beyond the edge, and the turbidity test on every batch is the "
               "control that would detect it.")
    sq("disc", "Cell breakage at the highest field may also be greater in the commercial feed zone than in the study, so "
               "the absence of a rise in host cell protein and DNA holds at the scale of the study.")
    sq("disc", "The results rest on two studies that PCP-004 did not plan.")
    sq("disc", "Every parameter result comes from the univariate study made during the re-analysis (PD-004-01), not from "
               "the planned study.")
    sq("disc", "The culture before harvest, the filter pressure and the Protein A load challenge were not measured, the "
               "depth filter load series was not run on centrate from both ends of the range of centrifugation (rcf), "
               "three NOR limits were not run as levels, and the records of execution were not kept.")
    sq("disc", "Where the plan left a rule open, such as the smallest difference a method must tell apart, this report "
               "states the rule it applied (PD-004-08).")
    sq("disc", "In routine manufacture the turbidity test on every batch detects poor clarification, and the purification "
               "steps clear host cell protein and DNA.")
    sq("disc", "The process performance qualification batches at the receiving site will run the step at commercial scale "
               "within its NORs (PTP-001).")

    # -- Conclusions (the numbered list of the .qmd) ---------------------------------------------------------
    con_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n# Conclusions", 1)[1].split("\n# ", 1)[0], flags=re.M)
    if len(con_list) != 7:
        raise ValueError(f"{DOC}: {len(con_list)} numbered conclusions, the report has seven")
    for i, con in enumerate(con_list, 1):
        st("concl", f"Conclusion {i}: {clean(q(con))}", [ref("concl", q(con))])

    # -- Study events and discrepancies from the plan --------------------------------------------------------
    sq("record", "PCP-004 calls a change made during execution that is not a revision of the plan a deviation (PCP-004 "
                 "§13).")
    sq("record", "It records the events of execution that Version 1.0 recorded as study events, under the numbers "
                 "Version 1.0 gave them, and the departures from PCP-004 as discrepancies from the plan.")
    sq("events", "Version 1.0 recorded `{python} N_EV` study events, both in S-HAR-UNI.")
    sq("pds", "The record holds `{python} N_PD` departures from PCP-004 as discrepancies from the plan (@tbl-discrepancies).")
    for pid, row in pdrow.items():
        d = PDS[pid]
        srow("pds", f"Discrepancy {pid} from PCP-004, {d['subject']}: planned {d['planned']}; done {d['done']}; "
                    f"reason {d['reason']}.", row, rows_=pdrow, caption=pd_cap, label="tbl-discrepancies")
    pd_prose = {
        "PD-004-01": "S-HAR-UNI2 was made during the Version 2.0 re-analysis, from `{python} WIN[UNI2]`, to give the "
                     "harvest parameters the recorded results that Version 1.0 lacked.",
        "PD-004-02": "It was made because Version 2.0 judges a held intermediate against its intermediate acceptance "
                     "criteria and Version 1.0 had no hold result to judge.",
        "PD-004-03": "Every result is therefore reported at the scale of the study, with no offset to manufacturing "
                     "scale, and @sec-sdm states the consequence for each output.",
        "PD-004-04": "The study therefore shows whether a parameter changed an attribute of the clarified harvest, not "
                     "whether the step changed it.",
        "PD-004-05": "Objective 3 is met for the particulate content of the clarified harvest only, and the effect of "
                     "turbidity on capture is not known (@sec-res-turbidity).",
        "PD-004-06": "The interaction between the two parameters is therefore not bracketed, and the range of depth filter "
                     "load holds for centrate from the set-point field (@sec-design-space).",
        "PD-004-07": "The conditions under which each run was made can therefore not be confirmed from the record beyond "
                     "its setting.",
        "PD-004-08": "It also judges the impurity release and product quality criteria on the slope of each result, "
                     "because the samples those criteria need were not taken (PD-004-04).",
    }
    if set(pd_prose) != set(pdrow):
        raise ValueError(f"{DOC}: the discrepancies of the register are {sorted(pdrow)}")
    for pid in pdrow:
        sq("pds", pd_prose[pid], t(f"{pid}: ") + clean(q(pd_prose[pid])))

    # -- Appendices -------------------------------------------------------------------------------------------
    sq("app_a", "@tbl-results-all gives every result of the univariate study S-HAR-UNI2, by parameter, setting and run.")
    st("app_a", note_span("tbl-results-all", "Not reported for the turbidity series"),
       [ref("app_a", note_span("tbl-results-all", "Not reported for the turbidity series"), all_t)])
    sq("app_b", "The two error terms lead to the same decisions at α = `{python} ALPHA`.")
    st("app_b", note_span("tbl-regression-detail", "The slope is in the unit of the response per unit of the parameter"),
       [ref("app_b", note_span("tbl-regression-detail", "The slope is in the unit of the response per unit of the "
                                                         "parameter"), regd_t)])
    sq("app_c", "@tbl-methods-summary summarizes the analytical methods of this report, with the precision of a single "
                "result and the limit of quantitation from the record of each method.")

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
                        aliases=["harvest and clarification", "harvest", "clarification", "primary recovery",
                                 P.DOC_REGISTRY[DOC][1], f"Step {uo.step}"],
                        review_status="human_verified")]
    alias = {"centrifuge_g": ["centrifugation", "rcf", "relative centrifugal field", "centrifugal field", "field"],
             "depth_filter_load": ["filter load", "load"],
             "turbidity": ["turbidity of the clarified harvest", "clarified harvest turbidity"]}
    concepts += [Concept(concept_id=PC[k], concept_type="PROCESS_PARAMETER", canonical_name=NAME[k],
                         aliases=alias[k], review_status="human_verified") for k in KEYS]
    concepts += G._attr_concepts(ckeys)
    concepts += G._method_concepts([m.method_id for m in methods], amv_title)
    concepts += [Concept(concept_id=e.equipment_id, concept_type="EQUIPMENT", canonical_name=e.equipment_name,
                         aliases=(["scale-down model", "model train"] if e.equipment_id == SDM_ID else []),
                         review_status="human_verified") for e in equipment]

    # ==== the annex =========================================================================================
    annex = S.GroundTruthAnnex(
        document_id=DOC, document_title=f"{P.DOC_REGISTRY[DOC][0]} — {P.DOC_REGISTRY[DOC][1]}",
        document_class=P.DOC_REGISTRY[DOC][0], **G.rev2_layer(DOC, FILE),
        schema_extensions_used=G.COMMON_EXT + G.REV2_EXT + [
            "ProvenAcceptableRange (new model) — per-parameter PAR from a univariate study, decided by the decision "
            "criteria of PCP-004 §7 (no fitted model, so no NOR-propagated value)",
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "Harvest runs no designed experiment: the three parameters were studied one factor at a time in "
            "S-HAR-UNI2 (made during the Version 2.0 re-analysis, PD-004-01), the report claims no design space, and "
            "no response-surface model was fitted. StatisticalModelFit holds the simple linear regressions of "
            "S-HAR-UNI2, one per row of the regression table, with the change over the range studied, its interval "
            "and p-value on the set-point replicates (the error term PCP-004 names) in adequacy_statement and the "
            "residual-error version as the sensitivity of Appendix B; the turbidity-on-target regression is the check "
            "of the challenge, not an effect. A p-value printed as '< 0.001' has no float value.",
            "ProcessParameter.target_value and NOR are the set-point and NOR against which the study was planned, "
            "unchanged at Version 2.0. ProcessParameter.PAR is the proven acceptable range the report states, with "
            "the other parameters at their set-points and at the scale of the study. rationale_for_criticality carries "
            "the classification argument of Section 9.",
            "The QualityAttribute records are the five attributes of the attribute table. acceptance_criteria holds "
            "the drug substance criterion and what applies at harvest: PCMP-001 sets no intermediate acceptance "
            "criterion for the clarified harvest; the aggregate and acidic variant criteria of the production "
            "bioreactor output pass through harvest unchanged to the load of Protein A capture and are used only to "
            "judge the held clarified harvest; fragments are compared with the drug substance criterion there.",
            "acceptance_criteria (the annex layer): the report prints no criteria-change table and Version 1.0 applied "
            "no criterion to this step, so there is no superseded record. The in-force records are the decision "
            "criteria of PCP-004 §7 as the report applies them (impurity release for host cell protein and residual "
            "DNA, clarification for post-clarification turbidity, product quality for aggregate and, judged the same "
            "way, fragments), each anchored on its sentence, and the three criteria the held clarified harvest is "
            "judged against, each anchored on its row of the hold judgement.",
            "PerformanceMeasure records: centrate turbidity, post-clarification turbidity (also a parameter of the "
            "step, measured not set) and step yield, as set-point means of S-HAR-UNI2 at the scale of the study. Step "
            "yield is reported and not gated, and the record names no method for it.",
            "ControlStrategyElement records: the five contributions of Section 10 (the KPPs within their NORs, the "
            "turbidity in-process control, no quality attribute controlled at harvest, the hold, and the acidic "
            "variant monitoring PCR-003 sets at harvest).",
            "Studies: S-HAR-UNI (Version 1.0, no data in the record), S-HAR-UNI2 and the hold study S-HAR-HLD, which "
            "has no hold study type and is recorded as univariate (hold time at two temperatures, factors that are not "
            "process parameters). No study carries n_runs, which the corpus test reserves for the seeded DoE designs. "
            "The qualification of the scale-down model was not made (PD-004-03) and has no study record.",
            "The schema has no record type for a discrepancy from the plan. PD-004-01 to PD-004-08 are report "
            "statements anchored on their rows of the discrepancy register, and the studies they add carry that row "
            "as a source reference.",
            "The report raises no deviation: a characterization study is not GMP manufacture. The two events of "
            "execution of Version 1.0 are study events under the numbers Version 1.0 gave them (DEV-004-01, "
            "DEV-004-02), recorded as Deviation records, the schema's only record type for an event of execution. "
            "no_impact_on_conclusions is true for both: S-HAR-UNI has no data in the record and no result of it "
            "enters the report.",
            "parameter_impacts_attribute / parameter_does_not_significantly_impact_attribute: one assertion per "
            "parameter and per attribute of the clarified harvest (host cell protein, residual DNA, aggregate, "
            "fragments), each on its row of the regression table; no slope was detected for any of them. Acidic "
            "variants were not measured in S-HAR-UNI2 and have no such assertion.",
            "The report prints no related-documents table; the document relationships are anchored on the sentences "
            "that name each document.",
            "rhetorical_spans: authoring/rhetorical/PCR-004.spans.yaml, re-curated against the Version 2.0 text in "
            "the same pass as this builder. weak_claims is empty.",
        ],
        inventory=G.rev2_inventory(DOC, FILE, "process_characterization_report", UO_NAME,
                                   ["process characterization", "harvest and clarification", "primary recovery",
                                    "univariate characterization", "linear regression", "proven acceptable range",
                                    "scale-down model not qualified", "hold study", "parameter classification",
                                    "discrepancies from the plan"]),
        entities=entities, studies=studies, design_spaces=[], proven_acceptable_ranges=pars,
        report_sections=sections, assertions=AssertionStore(run_id=f"gt-{DOC}", assertions=AS, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{DOC}", concepts=concepts),
        weak_claims=[], rhetorical_spans=G.build_rhetorical_spans(DOC, FILE), acceptance_criteria=acrit)
    _gate(annex, text)
    return annex
