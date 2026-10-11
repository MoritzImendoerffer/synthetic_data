"""PCR-010 Version 2.0, the characterization report of ultrafiltration and diafiltration (Step 10),
re-analysed under INV-001: its ground-truth annex (``build()``).

UF/DF has no designed experiment. The report rests on the univariate study S-UFDF-UNI2 (five levels of
each parameter, in duplicate, made during the re-analysis, PD-010-01), on the scale-down qualification
S-UFDF-SDM, and on a check of the PCMP-001 assumption that no step after cation exchange changes
aggregate (PD-010-08), whose bound tightens the aggregate criterion of the cation exchange pool. The
annex records what the document presents and nothing it does not claim: no design space (an explicit
non-claim), proven acceptable ranges that are the ranges studied, with no NOR-propagated analysis.

The kinds of record follow the Version 2.0 report builders ``pcr_006.py`` and ``pcr_003.py``: the
inventory and the revision layer; the step, the two TFF skids and the membrane, the two sites; the three
parameters with the class and the classification argument of the report; the three attributes in scope;
the three analytical methods; the capability records; the process performance measures; the elements of
the control strategy; the fitted models (the fifteen slopes, the exponential fit of the buffer exchange
and the main-effects fit of the verification); the two study events; the document relationships and the
explicit non-claims; the three studies; the proven acceptable ranges; the acceptance criteria the report
states; the assertions; the report statements, grouped by the chapters of the report; the concepts; and
the rhetorical spans of ``authoring/rhetorical/PCR-010.spans.yaml``.

Every table of the report is a complex table (``T.frame`` or a ``T.`` builder), read back through
``qmd_ctables`` from the object the report printed, or a markdown string of a ``_pcpkg`` helper
(``related_docs_md``, ``dev_register``, ``discrepancy_register``), read back with ``md_string_rows``,
so each row quote is the rendered row, with ``table_header=rows.header``. Every prose quote is a span of
the ``.qmd`` copied with its inline expressions and rendered as the ``.docx`` reads it (``render``), so no
value is typed here. ``q`` refuses a snippet that is not a span of the ``.qmd`` prose or that crosses a
citation, and ``build()`` refuses to return an annex with a quote that does not ground or a weak anchor.

The module-level helpers (``_headings``, ``_xrefs``, ``_smart``, ``_gate``, ...) are those of
``pcr_006.py``, copied because they read this module's own ``QMD``; they are candidates for a shared
module.
"""
from __future__ import annotations

import os
import re

import _pcpkg as P
import build_ground_truth as G
import schema_ext as S
from check_grounding import normalize, specificity_report

DOC = "PCR-010"
FILE = G.PCR10_FILE                                   # "PCR-010_ufdf.docx"
QMD = "PCR-010_ufdf.qmd"
UO = "ufdf"
#: Concept ids kept from the Version 1.0 builder of this report and the Version 2.0 builder of its plan.
STEP_ID = "step:ufdf"
SDM_ID = "equip:ufdf_sdm"
SKID2_ID = "equip:ufdf_sdm_skid2"
MEMBRANE_ID = "equip:ufdf_membrane"

_INTRO = "Introduction"
_PRIOR = "Prior knowledge and quality risk basis"
_MM = "Materials and methods"
_SD = "Study design"
_RES = "Results"
_PAR = "Proven acceptable ranges"
_REC = "Study events and discrepancies from the plan"
_EV = "Study events"
_PDS = "Discrepancies from the plan"
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
    "repro": (_RES, "Reproducibility of the duplicate runs"),
    "effects": (_RES, "Effects of the parameters"),
    "agg": (_RES, "Aggregate"),
    "acidic": (_RES, "Acidic charge variants"),
    "buffer": (_RES, "Buffer exchange"),
    "yield": (_RES, "Step yield and final concentration"),
    "mech": (_RES, "Mechanistic interpretation"),
    "ds": ("Design space",),
    "basis_par": (_PAR, "Acceptance basis"),
    "criteria": (_PAR, "Results against the criteria"),
    "par": (_PAR, "Proven acceptable ranges of the parameters"),
    "cap": ("Process capability and robustness",),
    "class": ("Parameter classification",),
    "control": ("Contribution to the control strategy",),
    "disc": ("Discussion",),
    "concl": ("Conclusions",),
    "record": (_REC,),
    "events": (_REC, _EV),
    "dev1": (_REC, _EV, "DEV-010-01, transmembrane pressure above the NOR"),
    "dev2": (_REC, _EV, "DEV-010-02, final concentration below target"),
    "pds": (_REC, _PDS),
    "app_a": ("Appendix A. Results of the univariate study",),
    "app_b": ("Appendix B. Runs of the scale-down qualification",),
    "app_c": ("Appendix C. Analytical methods summary",),
}
#: Relationship cell of the related-documents table -> DocumentRelationship.kind (others: references).
REL_KIND = {"Rolls up into": "rolls_up_into", "Sibling — paired document": "executed_under",
            "Parent — master plan": "executed_under",
            "Parent — risk basis for study scope": "scoped_by", "Parent — transfer scope": "scoped_by"}
#: The report's statements are grouped by the chapters of the report, in this order.
CHAPTERS = ["Executive summary", _INTRO, _PRIOR, _MM, _SD, _RES, "Design space", _PAR,
            "Process capability and robustness", "Parameter classification",
            "Contribution to the control strategy", "Discussion", "Conclusions", _REC,
            "Appendix A. Results of the univariate study", "Appendix B. Runs of the scale-down qualification"]


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
    """``{label -> rendered cross-reference}`` ("sec-buffer" -> "Section 5.5", "tbl-pars" -> "Table 10")."""
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
        md = re.search(r'print\(": (.*?) \{#(tbl-[\w-]+)\}"\)', code)
        if md:
            caps[md.group(2)] = md.group(1)
    for lab, (tab, _) in G.qmd_ctables(QMD).items():
        caps.setdefault(lab, tab.caption)
    for lab, cap in caps.items():
        word = "Table" if lab.startswith("tbl-") else "Figure"
        m = re.search(word + r" (\d+): " + re.escape(normalize(cap)), text)
        if m:
            out[lab] = f"{word} {m.group(1)}"
    return out, caps


def _smart(s):
    """Prose as pandoc renders it: straight double quotes become typographic pairs and a straight
    apostrophe a typographic one."""
    return re.sub(r'"([^"]*)"', "“\\1”", s).replace("'", "’")


def _cells(row):
    """The cells of a rendered row: a continuation row keeps its empty leading cells."""
    return [c.strip() for c in row.split("|")]


def _unmark(cell):
    """A rendered cell without its trailing footnote markers ("< 0.001 a)")."""
    return re.sub(r"(?:\s[a-z]\))+$", "", str(cell)).strip()


def _num(cell):
    """A number as the document prints it, back to a float; None for a cell that is not one."""
    s = _unmark(cell).replace("−", "-").replace(",", "")
    s = re.sub(r"^p = ", "", s)
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
    """Every quote and table header is a verbatim span of the rendered document, and no quote is a weak
    anchor (``check_grounding.specificity_report``)."""
    d = annex.model_dump(mode="json", serialize_as_any=True)
    miss = [q for q in _walk(d, ("quote", "table_header"), []) if normalize(q) not in text]
    weak = specificity_report(d, text)
    if miss or weak:
        raise ValueError(f"{DOC}: {len(miss)} ungrounded quote(s), {len(weak)} weak anchor(s):\n  "
                         + "\n  ".join([f"ungrounded: {q!r}" for q in miss] + [f"weak: {w}" for w in weak]))


def _rows_once(rows, text):
    """The rows of ``rows`` that occur exactly once in the rendered text (a continuation row of a merged
    column can read like another one after a reseed), keeping ``.header``."""
    out = G.RowQuotes((k, r) for k, r in rows.items() if text.count(normalize(r)) == 1)
    out.header = rows.header
    return out


def build():  # noqa: C901 - one document, one builder, in the order of the report
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    from annex_contract.concepts import Concept, ConceptStore
    from annex_contract.discourse import DocumentRelationship, ExplicitNonClaim
    from annex_contract.results import (ControlStrategyElement, Deviation, ModelTerm, PerformanceMeasure,
                                        ProcessCapability, StatisticalModelFit)
    from annex_contract.summaries import ReportSection, ReportStatement

    _check_sections()
    ns, _ = G.qmd_namespace(QMD)
    ct = G.qmd_ctables(QMD)
    text = G._document_text(FILE)
    prose_src = _prose()
    xref, caps = _xrefs(text)
    meta = G.meta
    src_all = _source()

    def render(src):
        """A span of the .qmd as the .docx reads it."""
        s = G.qmd_inline(ns, src)
        if "[@" in s:
            raise ValueError(f"{DOC}: a quote crosses a citation, end it before: {src!r}")
        s = re.sub(r"@((?:sec|tbl|fig)-[\w-]*\w)", lambda m: f" {xref[m.group(1)]} ", s)
        s = re.sub(r"\*([^*\n]+)\*", r"\1", s)
        return re.sub(r"\s+", " ", _smart(s)).strip()

    def q(src):
        """A prose span of the .qmd as it renders. ``src`` must be copied from the .qmd."""
        if normalize(src) not in prose_src:
            raise ValueError(f"{DOC}: not a span of the .qmd prose: {src!r}")
        return render(src)

    def t(txt):
        """Annex text with the report's own values (inline expressions evaluated in its namespace)."""
        return G.qmd_inline(ns, txt)

    def ref(sec, quote, table=None, rows=None, caption=None, label=None):
        r = G.ref(DOC, FILE, _sid(sec), SEC[sec][-1], quote,
                  table_title=caption if table is None else table.caption,
                  table_id=label if table is None else table.label,
                  table_header=None if rows is None else rows.header)
        r.heading_path = list(SEC[sec])
        return r

    def keyed(label, keys, name_of, cell=0):
        """The rendered rows of the CTable the report printed under ``label``, keyed. Every row must name
        its own record in cell ``cell`` (footnote markers aside): a mis-keyed row attests the wrong thing."""
        tab = ct[label][0]
        rows_ = G.ctable_rows(tab, keys)
        if normalize(rows_.header) not in text:
            raise ValueError(f"{DOC}: the header of {label} does not ground: {rows_.header!r}")
        bad = [k for k, row in rows_.items() if _unmark(_cells(row)[cell]) != name_of(k)]
        if bad:
            raise ValueError(f"{DOC} {label}: rows keyed to records they do not name: {bad}")
        return tab, rows_

    def md_rows(md, label):
        rows_ = G.md_string_rows(md)
        for k_, v_ in list(rows_.items()):
            if normalize(v_) not in text and normalize(_smart(v_)) in text:
                rows_[k_] = _smart(v_)
        cap = caps[label]
        if normalize(f"{cap} {rows_.header}") not in text:
            raise ValueError(f"{DOC}: the caption of {label} no longer reads {cap!r}")
        return rows_, cap

    def note_span(label, start):
        """The sentence of the notes of the complex table ``label`` that starts with ``start``."""
        notes = " ".join(t_ for _, t_ in ct[label][0].notes)
        m = re.search(re.escape(start) + r"[^.]*\.", notes)
        if not m or normalize(m.group(0)) not in text:
            raise ValueError(f"{DOC}: no note of {label} starts with {start!r}")
        return m.group(0)

    # ---- names and values of the report ----------------------------------------------------------
    fx, fg, pv, w = ns["fx"], ns["fg"], ns["pv"], ns["w"]
    PK, NAME, UNIT, CLS = list(ns["PK"]), ns["NAME"], ns["UNIT"], ns["CLS"]
    SP, NOR, RNG, PARS = ns["SP"], ns["NOR"], ns["RNG"], ns["PARS"]
    u_, nor_s, rng_s = ns["u_"], ns["nor_s"], ns["rng_s"]
    SL, SIG, AG, AC = ns["SL"], ns["SIG"], ns["AG"], ns["AC"]
    RESP, RLAB = list(ns["RESP"]), ns["RLAB"]
    SDM_EQ, UNI2_EQ, UNI_EQ = ns["SDM_EQ"], ns["UNI2_EQ"], ns["UNI_EQ"]
    SDM_ST, UNI_ST, UNI2_ST = ns["SDM_ID"], ns["UNI_ID"], ns["UNI2_ID"]
    PDS = {d["id"]: d for d in ns["PDS"]}
    PD = ns["PD"]
    UO_NAME, STEP_LABEL = G.UFUO_NAME, G.UFSTEP_LABEL
    PC = G.UFPARAM_CONCEPT                                          # parameter name -> concept id
    pkey = {NAME[k]: k for k in PK}
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))
    reg = P.cqa_reg.set_index("key")
    by_label = G._attr_key_by_label()
    sdm_name = f"bench-scale TFF skid {SDM_EQ}"
    skid2_name = f"second UF/DF TFF skid {UNI2_EQ}"
    if UNI_EQ != SDM_EQ:
        raise ValueError(f"{DOC}: the planned univariate study no longer ran on the skid of the qualification")

    # ---- the rendered tables, from the objects the report printed --------------------------------
    cq_df = ct["tbl-cqas"][1]
    ckeys = [by_label[n] for n in cq_df["CQA"]]
    cq_t, crow = keyed("tbl-cqas", ckeys, lambda k: names[k])
    cq_df = cq_df.set_index(cq_df["CQA"].map(by_label))
    off_lab = {"Aggregates, HMW (%)": AG, "Step yield (%)": "step_yield",
               "Final concentration (g/L)": "ds_concentration_g_per_l", "Permeate flux (LMH)": "flux_lmh"}
    off_t, offrow = keyed("tbl-sdm-offsets", [off_lab[_cells(r)[0]] for r in ct["tbl-sdm-offsets"][0].rows()],
                          lambda k: {v: n for n, v in off_lab.items()}[k])
    sop_df = ct["tbl-sops"][1]
    sop_t, soprow = keyed("tbl-sops", list(sop_df["Reference"]), str, cell=1)
    amv_title = dict(zip(sop_df["Reference"], sop_df["Title"]))
    smp_df = ct["tbl-sampling"][1]
    smp_t, smprow = keyed("tbl-sampling", list(smp_df["Sample"]), str)
    fa_df = ct["tbl-factors"][1]
    fa_t, farow = keyed("tbl-factors", [pkey[n] for n in fa_df["Parameter"]], lambda k: NAME[k])
    rp_df = ct["tbl-repro"][1]
    rlab_key = {v: k for k, v in RLAB.items()}
    rp_t, rprow = keyed("tbl-repro", [rlab_key[n] for n in rp_df["Output"]], lambda k: RLAB[k])
    sl_t = ct["tbl-slopes"][0]
    slkeys = [(k, r) for k in PK for r in RESP]
    slrow = G.ctable_rows(sl_t, slkeys)
    if normalize(slrow.header) not in text or len(slrow) != len(SL):
        raise ValueError(f"{DOC}: the slope table no longer prints one row per parameter and output")
    clab = ns["CLAB"]
    bad = [kr for kr, row in slrow.items() if _cells(row)[1] != clab[kr[1]]]
    if bad:
        raise ValueError(f"{DOC}: slope rows keyed to outputs they do not name: {bad}")
    lv_t = ct["tbl-levels"][0]
    lvrow = G.ctable_rows(lv_t)
    pa_t, parow = keyed("tbl-pars", [pkey[n] for n in ct["tbl-pars"][1]["Parameter"]], lambda k: NAME[k])
    cap_df = ct["tbl-capability"][1]
    capkeys = [by_label[n] for n in cap_df["CQA"]]
    cap_t, caprow = keyed("tbl-capability", capkeys, lambda k: names[k])
    cap_df = cap_df.set_index(cap_df["CQA"].map(by_label))
    cl_t, clrow = keyed("tbl-classification", [pkey[n] for n in ct["tbl-classification"][1]["Parameter"]],
                        lambda k: NAME[k])
    ms_df = ct["tbl-methods-summary"][1]
    ms_t, msrow = keyed("tbl-methods-summary", list(ms_df["Method\nvalidation"]), str, cell=2)
    ms_df = ms_df.set_index("Method\nvalidation")
    uni_t = ct["tbl-uni2"][0]
    unirow = _rows_once(G.ctable_rows(uni_t), text)
    run_t = ct["tbl-sdm-runs"][0]
    runrow = _rows_once(G.ctable_rows(run_t), text)
    rel, rel_cap = md_rows(P.related_docs_md(DOC), "tbl-related")
    devrow, dev_cap = md_rows(P.dev_register(DOC), "tbl-events")
    pdrow, pd_cap = md_rows(P.discrepancy_register(DOC), "tbl-discrepancies")

    def pdref(pid, sec="pds"):
        return ref(sec, pdrow[pid], rows=pdrow, caption=pd_cap, label="tbl-discrepancies")

    # ==== entities ===================================================================================
    q_step = q("Ultrafiltration and diafiltration (UF/DF) is Step `{python} STEP_N`, the last step of the A-Mab "
               "drug substance process.")
    q_does = q("It concentrates the antibody, exchanges the process buffer for the formulation buffer and delivers "
               "the drug substance at its target concentration of `{python} sp_s(\"final_conc\")`.")
    q_last = q("UF/DF is the last step of the train, and its product is the drug substance.")
    q_ops = q("A second concentration brings the retentate to the drug substance target, and a buffer flush "
              "recovers it.")
    q_receives = q("The step receives the filtrate pool of the small virus retentive filtration step.")
    step = S.ProcessStep(
        step_id=STEP_ID, step_name=UO_NAME, step_number=str(ns["STEP_N"]), unit_operation=UO_NAME,
        description=t("Step `{python} STEP_N`, the last step of the A-Mab drug substance process. Ultrafiltration "
                      "concentrates the filtrate pool of virus filtration, diafiltration at constant volume "
                      "exchanges the process buffer for the formulation buffer, a second concentration brings the "
                      "retentate to the drug substance target of `{python} sp_s(\"final_conc\")` and a buffer flush "
                      "recovers it. The step can add to aggregate and to the acidic charge variants, is credited "
                      "with no clearance of host cell protein, DNA or leached Protein A, and claims no viral "
                      "clearance. Its product is the drug substance."),
        input_materials=["virus filtration filtrate pool"], output_materials=["drug substance"],
        equipment=[sdm_name, skid2_name, "tangential flow membrane"],
        source_references=[ref("exec", q_step), ref("exec", q_does), ref("uo", q_last), ref("uo", q_ops),
                           ref("operation", q_receives)],
        metadata=meta())
    q_bench = q("The bench-scale model holds the crossflow and the membrane loading at their commercial values, "
                "both scaled by membrane area (PCMP-001 §5).")
    q_chem = q("The membrane chemistry, the nominal molecular weight cut-off and the feed channel geometry are those "
               "of the commercial skid.")
    q_qual = q("The qualification study `{python} SDM_ID` ran from `{python} SDM_START` to `{python} SDM_END` on the "
               "skid `{python} SDM_EQ`, under SOP-1001.")
    q_skid2 = q("It ran on `{python} UNI2_EQ`, a second UF/DF TFF skid, which was in calibration at execution, with "
                "its next calibration due on `{python} CALDUE[UNI2_EQ]`.")
    q_share = q("The two skids share their design and their membrane, so the hold-up and the surface that the "
                "antibody meets per gram, which cause the offsets, are expected to be alike.")
    q_membrane = q("The step works across a tangential flow membrane whose pores pass buffer salts and retain the "
                   "antibody.")
    q_mem_cs = q("The membrane chemistry and the membrane supplier are part of the qualified state of the step, and "
                 "a change to either requires a new risk assessment before these data are applied (PCP-010 §12).")
    equipment = [
        S.Equipment(equipment_id=SDM_ID, equipment_name=sdm_name,
                    equipment_type="tangential flow filtration skid (scale-down model)", site_name=P.SENDING_SITE,
                    source_references=[ref("sdm", q_bench), ref("sdm", q_chem), ref("sdm", q_qual)],
                    metadata=meta()),
        S.Equipment(equipment_id=SKID2_ID, equipment_name=skid2_name,
                    equipment_type="tangential flow filtration skid (scale-down model, second skid)",
                    site_name=P.SENDING_SITE,
                    source_references=[ref("uni_design", q_skid2), ref("sdm", q_share)], metadata=meta()),
        S.Equipment(equipment_id=MEMBRANE_ID, equipment_name="tangential flow membrane",
                    equipment_type="ultrafiltration membrane",
                    source_references=[ref("uo", q_membrane), ref("control", q_mem_cs)], metadata=meta()),
    ]
    sites = G._site_entities(DOC, FILE, _sid("title"))

    # -- parameters: the factors row, the PAR row, the classification row and the classification bullets --
    sDV, sT, sC = ns["sDV"], ns["sT"], ns["sC"]
    cls_quotes = {
        "diavolumes": [q("The `{python} nm[\"diavolumes\"]` was classified as a KPP."),
                       q("More diavolumes lower the residual process buffer, by a factor of `{python} fx(RB_FOLD)` "
                         "for each diavolume (@sec-buffer).")],
        "tmp": [q("TMP was classified as a KPP."),
                q("It has a significant effect on aggregate, a CQA (`{python} pe(sT[\"p\"])`)."),
                q("This report judges an effect of that size too small to be practically relevant, and the KPP "
                  "class of both TMP and the final DS concentration rests on that judgement.")],
        "final_conc": [q("The final DS concentration was classified as a KPP."),
                       q("It has a significant effect on aggregate, a CQA (`{python} pe(sC[\"p\"])`)."),
                       q("The bound of `{python} fx(UF_ALLOW, 3)` percentage points behind the criterion of the "
                         "cation exchange pool includes this effect too.")],
    }
    head = "Classified {c} under SOP-4001 by the rules of PCMP-001 §7.7. "
    UF_ALLOW, AGG_MARGIN = ns["UF_ALLOW"], ns["AGG_MARGIN"]
    rationale = {
        "diavolumes": head.format(c=CLS["diavolumes"]) + (
            f"More diavolumes lower the residual process buffer, by a factor of {fx(ns['RB_FOLD'])} for each "
            f"diavolume. The slopes on aggregate ({pv(sDV['p'])}) and on the acidic charge variants "
            f"({pv(SL[('diavolumes', AC)]['p'])}) were not significant, so no effect on either attribute was "
            f"detected within the range studied, at the precision of the duplicates. The NOR is a minimum of "
            f"{u_('diavolumes', NOR['diavolumes'][0])} and the PAR runs from that minimum to "
            f"{u_('diavolumes', PARS['diavolumes'][1])}."),
        "tmp": head.format(c=CLS["tmp"]) + (
            f"TMP has a significant effect on aggregate, a CQA ({pv(sT['p'])}): the slope raises aggregate by "
            f"{fx(ns['CH_T_NOR'])} percentage points across the NOR of {nor_s('tmp')} and by {fx(sT['ch'])} across "
            f"the PAR of {rng_s('tmp')}, against a margin of {fx(AGG_MARGIN)} percentage points between the highest "
            f"aggregate result and the criterion. The report judges an effect of that size too small to be "
            f"practically relevant, and the KPP class rests on that judgement; PCMP-001 and SOP-4001 set no "
            f"threshold for it. The effect is carried into product quality through the prediction bound of "
            f"{fx(UF_ALLOW, 3)} percentage points that sets the criterion of the cation exchange pool. Its effect "
            f"on the permeate flux was not measured across the TMP range."),
        "final_conc": head.format(c=CLS["final_conc"]) + (
            f"The final DS concentration sets the concentration of the drug substance, which followed it with a "
            f"slope of {fx(ns['sFC']['slope'], 3)}. It has a significant effect on aggregate, a CQA "
            f"({pv(sC['p'])}): the slope raises aggregate by {fx(ns['CH_C_NOR'])} percentage points across the NOR "
            f"of {nor_s('final_conc')} and by {fx(sC['ch'])} across the PAR of {rng_s('final_conc')}, against the "
            f"same margin of {fx(AGG_MARGIN)} percentage points. The KPP class rests on the judgement that the "
            f"effect is too small to be practically relevant, and the bound of {fx(UF_ALLOW, 3)} percentage points "
            f"behind the criterion of the cation exchange pool includes the effect."),
    }
    params = []
    for k in PK:
        name = NAME[k]
        refs = [ref("factors", farow[k], fa_t, farow), ref("par", parow[k], pa_t, parow),
                ref("class", clrow[k], cl_t, clrow)]
        refs += [ref("class", x) for x in cls_quotes[k]]
        params.append(S.ProcessParameter(
            parameter_id=PC[name], parameter_name=name, parameter_type=CLS[k], unit=UNIT[k],
            target_value=ns["sp_s"](k), NOR=nor_s(k), PAR=f"{fg(PARS[k][0])}–{fg(PARS[k][1])} {UNIT[k]}",
            associated_step=STEP_LABEL, rationale_for_criticality=rationale[k], study_type="univariate",
            source_references=refs, metadata=meta()))

    # -- attributes: the register row, the capability row and the sentence that says why it is in scope ----
    attr_prose = {
        "aggregates_hmw": q("It can add to aggregate, which can form at the membrane wall and in the recirculation "
                            "pump."),
        "acidic_variants": q("It can also add to the acidic charge variants, because deamidation continues while "
                             "the antibody is in solution on the skid (@sec-prior)."),
        "residual_dna": q("Residual DNA is in scope as an attribute of the drug substance that this step delivers."),
    }
    method_of = {"aggregates_hmw": "AMV-3011", "acidic_variants": "AMV-3013"}
    attrs = []
    for key in ckeys:
        r = cq_df.loc[key]
        ds_crit = r["Drug substance\ncriterion"]
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{key}", attribute_name=names[key], attribute_type="CQA",
            unit=reg.loc[key, "unit"],
            acceptance_criteria=[f"{ds_crit} (drug substance; no step follows UF/DF, so the "
                                 f"drug substance criterion applies directly)"],
            analytical_method=method_of.get(key), associated_steps=[STEP_LABEL],
            rationale_for_criticality=f"A-Mab Tool #1 Risk Score = Impact × Uncertainty = {r['Tool #1']}.",
            criticality_level=r["Criticality"], tool1_score=int(r["Tool #1"]),
            tool2_severity=int(reg.loc[key, "tool2_severity"]),
            source_references=[ref("cqa", crow[key], cq_t, crow), ref("cap", caprow[key], cap_t, caprow),
                               ref("uo" if key != "residual_dna" else "cqa", attr_prose[key])],
            metadata=meta()))

    # -- analytical methods: the procedure row, the methods-summary row and the sentence that names it ------
    q_meth = {"AMV-3011": q("Aggregate is measured by size exclusion chromatography (SEC) under AMV-3011 and "
                            "reported as the percentage of high molecular weight species (HMW)."),
              "AMV-3013": q("The acidic charge variants are measured by imaged capillary isoelectric focusing "
                            "(icIEF) under AMV-3013 and reported as the percentage of acidic species."),
              "AMV-3019": q("Protein concentration is measured by ultraviolet absorbance (A280) under AMV-3019, "
                            "and the final concentration and the step yield rest on that measurement.")}
    attr_of = {v: k for k, v in method_of.items()}
    methods = []
    for amv in [a for a in sop_df["Reference"] if a.startswith("AMV-")]:
        methods.append(S.AnalyticalMethod(
            method_id=amv, method_name=amv_title[amv], method_type=G.METHOD_TYPE.get(amv),
            analytes=[ms_df.loc[amv, "Output"]],
            associated_attributes=[f"attr:{attr_of[amv]}"] if amv in attr_of else [],
            validation_status="validated",
            source_references=[ref("analytics", soprow[amv], sop_t, soprow),
                               ref("app_c", msrow[amv], ms_t, msrow), ref("analytics", q_meth[amv])],
            metadata=meta()))

    # -- capability: one record per row of the capability table ----------------------------------------
    CAPT, N_MC = ns["CAPT"], int(ns["N_MC"])
    cap_prose = {
        "aggregates_hmw": q("Aggregate has a Cpk of `{python} fx(CPK_AG, 1)`, above the target, and no simulated "
                            "batch lay outside its criterion."),
        "acidic_variants": q("The acidic charge variants have a Cpk of `{python} fx(CPK_AC)` in the integrated "
                             "process model, between the minimum and the target."),
        "residual_dna": q("This level is not a measured result."),
    }
    side = {"upper": "upper", "lower": "lower"}
    capab = []
    for key, row in caprow.items():
        c = cap_df.loc[key]
        capab.append(ProcessCapability(
            capability_id=f"{DOC}-CAP{len(capab) + 1:02d}", quality_attribute=f"attr:{key}", index_name="Cpk",
            index_value=_num(c["Cpk"]), specification_side=side.get(str(CAPT.loc[key, "spec_type"]), "two_sided"),
            acceptance_range=c["Criterion"], mean=c["Mean"], standard_deviation=c["SD"],
            unit=str(CAPT.loc[key, "unit"]), basis="simulated", n_batches=N_MC, unit_operation=UO_NAME,
            source_references=[ref("cap", row, cap_t, caprow), ref("cap", cap_prose[key])], metadata=meta()))

    # -- process performance: step yield, final concentration, residual process buffer -------------------
    perf = [
        PerformanceMeasure(
            measure_id=f"{DOC}-PM01", measure_name="step yield", unit_operation=UO_NAME,
            value=t("`{python} fx(Y_MIN, 1)`–`{python} fx(Y_MAX, 1)` %, mean `{python} fx(Y_MEAN, 1)` %"), unit="%",
            basis=f"measured, all runs of {UNI2_ST}; no criterion, reported for information",
            source_references=[ref("yield", q("The step yield ranged from `{python} fx(Y_MIN, 1)` to "
                                              "`{python} fx(Y_MAX, 1)` %, with a mean of `{python} fx(Y_MEAN, 1)` %.")),
                               ref("repro", rprow["yield_pct"], rp_t, rprow)],
            metadata=meta()),
        PerformanceMeasure(
            measure_id=f"{DOC}-PM02", measure_name="final concentration", unit_operation=UO_NAME,
            value=t("`{python} fx(FC_OTH.min(), 1)`–`{python} fx(FC_OTH.max(), 1)` g/L at the target of "
                    "`{python} sp_s(\"final_conc\")`"), unit="g/L", normal_operating_range=nor_s("final_conc"),
            basis=f"measured by A280 in the diavolume and TMP series of {UNI2_ST}, run at the target",
            source_references=[ref("yield", q("In the other two series, run at the target of "
                                              "`{python} sp_s(\"final_conc\")`, the final concentration ranged from "
                                              "`{python} fx(FC_OTH.min(), 1)` to `{python} fx(FC_OTH.max(), 1)` g/L, "
                                              "inside the NOR of `{python} nor_s(\"final_conc\")`.")),
                               ref("repro", rprow["ds_concentration_g_per_l"], rp_t, rprow)],
            metadata=meta()),
        PerformanceMeasure(
            measure_id=f"{DOC}-PM03", measure_name="residual process buffer at the minimum number of diavolumes",
            unit_operation=UO_NAME,
            value=t("at most `{python} fx(RB_NORLO[\"max\"], 3)` % of the process buffer at "
                    "`{python} u_(\"diavolumes\", NOR[\"diavolumes\"][0])`"),
            unit="% of the process buffer", normal_operating_range=nor_s("diavolumes"),
            basis=f"measured, two runs of the diavolume series of {UNI2_ST}; no limit for what the formulation "
                  f"tolerates is in the study record",
            source_references=[ref("buffer", q("At the minimum of `{python} u_(\"diavolumes\", NOR[\"diavolumes\"][0])` "
                                               "the two results were `{python} fx(RB_NORLO[\"min\"], 3)` and "
                                               "`{python} fx(RB_NORLO[\"max\"], 3)` %.")),
                               ref("repro", rprow["residual_buffer_pct"], rp_t, rprow)],
            metadata=meta()),
    ]

    # -- the elements of the control strategy (the numbered list of Section 10) ---------------------------
    cs_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n# Contribution to the control strategy", 1)[1]
                         .split("\n# ", 1)[0], flags=re.M)
    if len(cs_list) != 4:
        raise ValueError(f"{DOC}: {len(cs_list)} numbered elements of the control strategy, the report has four")
    cs_meta = [("number of diavolumes, TMP and final DS concentration (KPPs)", "process control within the NORs"),
               ("aggregate rise across UF/DF", "criterion of the cation exchange pool; in-process TMP monitoring and "
                                               "final concentration check by A280"),
               ("buffer exchange", "minimum number of diavolumes; release of the drug substance against the limits "
                                   "of its formulation buffer"),
               ("membrane and formulation buffer", "qualified state of the step; change management")]
    cs_els = []
    for i, (item, (ctl, ctype)) in enumerate(zip(cs_list, cs_meta), 1):
        sent = re.split(r"(?<=\.) (?=[A-Z`])", item)
        cs_els.append(ControlStrategyElement(
            element_id=f"{DOC}-CS{i:02d}", description=re.sub(r"\s+([,.;:)])", r"\1", render(item)),
            unit_operation=UO_NAME, controls=ctl, control_type=ctype,
            source_references=[ref("control", q(sent[0] if i != 4 else sent[1]))], metadata=meta()))

    # -- fitted models ---------------------------------------------------------------------------------
    fits = []

    def fit_rec(resp, form, refs, **kw):
        fits.append(StatisticalModelFit(
            model_fit_id=f"{DOC}-FIT{len(fits) + 1:02d}", response=resp, unit_operation=UO_NAME,
            model_form=form, source_references=refs, metadata=meta(), **kw))

    N_SER, ALPHA = int(ns["N_SER"]), float(ns["ALPHA"])
    for (k, r), row in slrow.items():
        c = _cells(row)
        sig = (k, r) in SIG
        fit_rec(RLAB[r], f"simple linear regression of the individual results on the setting of {NAME[k].lower()} "
                         f"over {rng_s(k)}, the other parameters at their set-points ({UNI2_ST})",
                [ref("effects", row, sl_t, slrow)], n_runs=N_SER, p_value=_num(c[4]),
                adequacy_statement=(f"Change across the range studied {c[2]} {c[1].rsplit('(', 1)[1].rstrip(')')}, "
                                    f"95 % confidence interval {c[3]}, p {_unmark(c[4])}; slope "
                                    + ("significant" if sig else "not significant") + f" at α = {fg(ALPHA)}. The "
                                    "model-adequacy criteria of PCMP-001 §7.2 apply to response-surface models and "
                                    "not to these slopes."),
                terms=[ModelTerm(term=NAME[k], factor=NAME[k], effect=_num(c[2]), p_value=_num(c[4]),
                                 significant=sig)])
    RB_B, RB_R2 = ns["RB_B"], ns["RB_R2"]
    q_rb_stats = q("The buffer exchange was analysed by fitting the exponential decay that the mechanism predicts "
                   "(@sec-prior), as the natural logarithm of the residual process buffer regressed on the number of "
                   "diavolumes.")
    q_rb_fit = q("The slope of its natural logarithm on the number of diavolumes was `{python} fx(RB_B, 3)` (95 % "
                 "confidence interval `{python} fx(RB_LO, 3)` to `{python} fx(RB_HI, 3)`, R² = `{python} fx(RB_R2, 3)`).")
    q_rb_one = q("The interval includes −1, the slope that complete passage of the buffer species through the "
                 "membrane gives.")
    fit_rec(RLAB["residual_buffer_pct"],
            "natural logarithm of the residual process buffer regressed on the number of diavolumes, across the "
            f"runs of the diavolume series of {UNI2_ST} (one result per run)",
            [ref("stats", q_rb_stats), ref("buffer", q_rb_fit), ref("buffer", q_rb_one)],
            n_runs=N_SER, r_squared=_num(fx(RB_R2, 3)),
            adequacy_statement=t("Slope `{python} fx(RB_B, 3)` per diavolume, 95 % confidence interval "
                                 "`{python} fx(RB_LO, 3)` to `{python} fx(RB_HI, 3)`, which includes −1, the slope "
                                 "of complete passage of the buffer species through the membrane; a fall by a "
                                 "factor of `{python} fx(RB_FOLD)` per diavolume."),
            terms=[ModelTerm(term="number of diavolumes", factor=NAME["diavolumes"], coefficient=_num(fx(RB_B, 3)))])
    UF_PF, UF_PLOF, UF_GAP = ns["UF_PF"], ns["UF_PLOF"], ns["UF_GAP"]
    q_ver_fit = q("The aggregate results, with the aggregate offset subtracted, are fitted to the main effects of the "
                  "`{python} w(N_P)` parameters, with all runs pooled and no interaction term.")
    q_ver_three = q("The fit meets the first three criteria of PCMP-001 §7.2.")
    q_ver_stats = q("The model is significant (`{python} pe(UF_PF)`), it has no significant lack of fit "
                    "(`{python} pe(UF_PLOF)`), and R² exceeds predicted R² by `{python} fx(UF_GAP)`, within the limit "
                    "of `{python} fg(THRESHOLDS[\"max_r2_minus_pred_r2\"])`.")
    fit_rec("Aggregates, HMW (%), at manufacturing scale",
            f"main effects of {NAME['diavolumes'].lower()}, TMP and {NAME['final_conc'].lower()}, all runs of "
            f"{UNI2_ST} pooled, no interaction term, aggregate offset subtracted (verification of PCMP-001 §7.5, "
            f"{PD[8]})",
            [ref("basis_par", q_ver_fit), ref("basis_par", q_ver_three), ref("basis_par", q_ver_stats)],
            n_runs=int(ns["N_RUNS2"]), p_value=_num(f"{UF_PF:.3f}") if UF_PF >= 0.001 else None,
            lack_of_fit_p=_num(f"{UF_PLOF:.3f}"),
            adequacy_statement=t("Meets the first three criteria of PCMP-001 §7.2: model `{python} pe(UF_PF)`; lack "
                                 "of fit `{python} pe(UF_PLOF)`; R² minus predicted R² `{python} fx(UF_GAP)`, within "
                                 "the limit of `{python} fg(THRESHOLDS[\"max_r2_minus_pred_r2\"])`. Evaluated at every "
                                 "combination of NOR low, set-point and NOR high (upper value of the diavolumes "
                                 "`{python} u_(\"diavolumes\", DV_COMBO_HI)`): mean rise "
                                 "`{python} fx(UF_WORST_MEAN, 3)` and one-sided 95 % prediction bound of a single run "
                                 "`{python} fx(UF_ALLOW, 3)` percentage points above the set-point. Assumes the "
                                 "parameters act independently."))

    # -- study events --------------------------------------------------------------------------------------
    dev_prose = {
        "DEV-010-01": [("dev1", q("In-process TMP monitoring detected the excursion.")),
                       ("dev1", q("The investigation attributed it to a transient fouling of the membrane, and the run "
                                  "was retained.")),
                       ("dev1", q("With the offset lowered by that amount, every aggregate result at manufacturing "
                                  "scale would still meet the criterion."))],
        "DEV-010-02": [("dev2", q("The investigation attributed the shortfall to the residual hold-up volume of the "
                                  "skid, the property of the bench skid that @sec-sdm expects to lower its step "
                                  "yield.")),
                       ("dev2", q("The record gives neither the concentration after the correction nor the run.")),
                       ("dev2", q("The correction could have raised the aggregate of that run."))],
    }
    dev_impact = {
        "DEV-010-01": t("TMP rose to `{python} u_(\"tmp\", dev_010_01_tmp_max_psi)` during concentration, above the "
                        "NOR of `{python} nor_s(\"tmp\")` and within the range studied of `{python} rng_s(\"tmp\")`. "
                        "Had the run been a scale-down run of `{python} SDM_ID` held at that TMP throughout, the upper "
                        "end of the 95 % confidence interval of the TMP slope puts its effect at no more than "
                        "`{python} fx(DEV1_EFFECT_HI, 3)` percentage points, which would have raised the aggregate "
                        "offset by at most `{python} fx(DEV1_SHIFT, 3)` points; every aggregate result at "
                        "manufacturing scale would still meet the criterion. The record names neither the study nor "
                        "the run, and the run was retained."),
        "DEV-010-02": t("The final concentration check measured `{python} u_(\"final_conc\", "
                        "dev_010_02_conc_pre_g_per_l)` by A280 (`{python} EV2_METHOD`), below the target and inside "
                        "the NOR; the retentate was concentrated further to the target. Had the run been a scale-down "
                        "run of `{python} SDM_ID`, the aggregate offset lies between `{python} fx(OFF_DROP_LO, 3)` and "
                        "`{python} fx(OFF_DROP_HI, 3)` with any one scale-down run left out, and with the smallest the "
                        "highest aggregate result at manufacturing scale is `{python} fx(AGG_MAX_DROP)` % HMW, "
                        "`{python} fx(AGG_MARGIN_DROP)` points below the criterion. The record gives neither the "
                        "concentration after the correction nor the run, and the run was retained."),
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
    q_neither = q("Neither study event changes a conclusion.")
    devs[0].source_references.append(ref("concl", q_neither))
    devs[1].source_references.append(ref("concl", q_neither))

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
    relation("executed_under", "PCP-010", "The report gives the results of the characterization of the step under "
             "the plan PCP-010 and the master plan PCMP-001.", "exec",
             q("This report gives the results of the characterization of the step under the plan PCP-010 and the "
               "master plan PCMP-001."))
    relation("scoped_by", "RA-001", "RA-001 assigned the three parameters of the step to univariate study.", "risk",
             q("All `{python} w(N_P)` parameters of UF/DF were assigned to univariate study, and no designed "
               "experiment was planned for the step."))
    relation("rolls_up_into", "PCMR-001", "The ranges and classes of the report roll up into PCMR-001.", "exec",
             q("The ranges and classes of this report roll up into the master report PCMR-001."))
    relation("references", "INV-001", "Version 2.0 is issued under the QA investigation INV-001.", "changes",
             q("Version 2.0 is issued under the QA investigation INV-001."))
    q_pcr007 = q("The criterion of the cation exchange pool is tightened from `{python} fx(AG_HI)` to "
                 "`{python} fx(CEX_AG)` % HMW, and the cation exchange report PCR-007 judges its pool against that "
                 "value.")
    relation("references", "PCR-007", "The cation exchange report PCR-007 judges its pool against the aggregate "
             "criterion tightened by the UF/DF allowance.", "basis_par", q_pcr007)
    q_formed = q("The glycan variants and the acidic charge variants are formed in the production bioreactor "
                 "(PCR-003).")
    relation("references", "PCR-003", "The acidic charge variants and the glycan variants are formed in the "
             "production bioreactor, characterized in PCR-003.", "control", q_formed)
    relation("references", "PCR-004", "Fragments form by proteolytic clipping in culture and during the harvest hold "
             "(PCR-003, PCR-004).", "control",
             q("Fragments form by proteolytic clipping in culture and during the harvest hold (PCR-003, PCR-004), and "
               "slowly by hydrolysis of the hinge region in solution, and they are tested at release."))
    q_chrom = q("Host cell protein and residual DNA are cleared by the chromatography steps (PCR-005, PCR-007 and "
                "PCR-008).")
    for tgt in ("PCR-005", "PCR-008"):
        relation("references", tgt, f"Host cell protein and residual DNA are cleared by the chromatography steps, "
                 f"of which {tgt} is one.", "control", q_chrom)
    q_vc = q("Viral clearance is credited to low-pH viral inactivation, anion exchange and virus filtration (PCR-006, "
             "PCR-008 and PCR-009), and the cumulative claim is consolidated in PCMR-001.")
    for tgt in ("PCR-006", "PCR-009"):
        relation("references", tgt, f"Viral clearance is credited to {tgt} among the three clearance steps; UF/DF "
                 f"claims none.", "control", q_vc)
    relation("references", "PTP-001", "The receiving site will run the PPQ batches of the transfer protocol PTP-001 "
             "against the ranges and classes of the report.", "disc",
             q("The receiving site will run the process performance qualification (PPQ) batches of the transfer "
               "protocol PTP-001 against the ranges and classes of this report (PCMP-001 §2)."))

    # -- explicit non-claims, by section --------------------------------------------------------------------
    ncs, nc_at = [], {}

    def nclaim(sec, subject, statement, quotes, rationale=None, elsewhere=None):
        ncs.append(ExplicitNonClaim(
            non_claim_id=f"{DOC}-NC{len(ncs) + 1:02d}", subject=subject, unit_operation=UO_NAME,
            statement=statement, rationale=rationale, handled_elsewhere=elsewhere,
            source_references=[ref(s_, x) for s_, x in quotes], metadata=meta()))
        nc_at.setdefault(sec, []).append(ncs[-1])

    nclaim("uo", "viral clearance", "No viral clearance is claimed for UF/DF, and it contributes no log reduction to "
           "the cumulative claim.",
           [("uo", q("No viral clearance is claimed for it.")),
            ("basis", q("This step contributes no log reduction to it, and the cumulative claim is consolidated in "
                        "PCMR-001."))],
           elsewhere="low-pH viral inactivation, anion exchange and virus filtration (PCR-006, PCR-008, PCR-009)")
    nclaim("uo", "clearance of host cell protein, DNA and leached Protein A", "The step is credited with no clearance "
           "of host cell protein, DNA or leached Protein A.",
           [("uo", q("it is credited with no clearance of host cell protein, DNA or leached Protein A")),
            ("cap", q("No DNA clearance is credited to UF/DF."))],
           elsewhere="the chromatography steps (PCR-005, PCR-007, PCR-008)")
    nclaim("cqa", "change in the glycan variants", "The step is not expected to change the glycan variants, and they "
           "were not measured.",
           [("uo", q("The step is not expected to change the glycan variants of A-Mab")),
            ("cqa", q("The membrane retains the antibody whatever its glycoform, so the step is not expected to change "
                      "their distribution, and they were not measured."))],
           rationale="The membrane retains the antibody whatever its glycoform.")
    nclaim("cqa", "fragments", "Fragments were not measured in the studies of the step; PCMP-001 Table 7.1 assumes the "
           "step does not change them, and the drug substance is tested for fragments at release.",
           [("cqa", q("Version 1.0 left fragments out of the studies of this step, and PCP-010 keeps that scope.")),
            ("analytics", q("The studies of this step do not measure fragments, a scope that PCP-010 keeps from "
                            "Version 1.0."))])
    nclaim("changes", "deviations", "The report records no deviation: the events of execution are study events, "
           "because a process characterization study is not GMP manufacture.",
           [("record", q("A process characterization study is not GMP manufacture and raises no deviation.")),
            ("changes", q("The events of execution that Version 1.0 recorded as deviations are called study events, "
                          "because a process characterization study is not GMP manufacture."))])
    nclaim("changes", "what the formulation tolerates", "The report makes no claim about how much residual process "
           "buffer the formulation tolerates; the study record holds no such limit.",
           [("changes", q("The study record holds no limit for what the formulation tolerates, and this version makes "
                          "no such claim (@sec-buffer)."))])
    nclaim("sdm", "scale-down offsets of the acidic charge variants and the residual process buffer",
           "The acidic charge variants and the residual process buffer were not compared at both scales; their "
           "offsets are unknown, not zero, and both are judged as measured.",
           [("sdm", q("Their offsets are unknown, not zero, and both are judged as measured (PCMP-001 §7.1)."))],
           rationale="The kinetics of deamidation and the passage of the buffer species through the membrane do not "
                     "depend on the scale of the skid.")
    nclaim("sdm", "comparison of the two skids", "No run compared the two skids; the offsets of the first skid are "
           "applied to the results of the second.",
           [("sdm", q("The qualification measured the offsets on `{python} SDM_EQ` only, and no run compared the two "
                      "skids."))], elsewhere=PD[1])
    nclaim("sampling", "change across the step and retention of the antibody", "No load, pre-diafiltration or permeate "
           "sample was taken, so the change in aggregate and in the acidic charge variants across the step and the "
           "retention of the antibody by the membrane are not established.",
           [("sampling", q("The study therefore measures how the parameters change the final retentate, and not what "
                           "the step adds to its load.")),
            ("sampling", q("Without a permeate result the retention of the antibody by the membrane is not confirmed "
                           "either."))], elsewhere=PD[3])
    nclaim("stats", "response-surface model", "No response-surface model was fitted, because the study has no "
           "factorial structure and no interaction can be estimated from it.",
           [("stats", q("No response-surface model was fitted, because the study has no factorial structure and no "
                        "interaction can be estimated from it."))])
    nclaim("ds", "design space", "No design space is defined for UF/DF: a study that varies one parameter at a time "
           "gives no result where two parameters are away from their set-points at the same time.",
           [("ds", q("No design space is defined for UF/DF.")),
            ("ds", q("A study that varies one parameter at a time cannot define one, because it gives no result where "
                     "two parameters are away from their set-points at the same time."))],
           rationale="A design space is a multivariate region (ICH Q8(R2)).")
    nclaim("par", "PAR beyond the range studied and the NOR-propagated analysis", "No PAR is claimed beyond the range "
           "studied, and the second analysis of PCMP-001 §6.4 was not performed, because the step has no fitted model.",
           [("par", q("This step has no such model, so that analysis was not performed.")),
            ("par", q("Each PAR here is the range studied, and no claim is made beyond it (PCMP-001 §7.6)."))])
    nclaim("par", "interaction of TMP and the final DS concentration", "The interaction of TMP and the final DS "
           "concentration was not measured and cannot be excluded.",
           [("par", q("The interaction of TMP and the final DS concentration that @sec-risk describes was not "
                      "measured.")),
            ("par", q("The study cannot exclude an interaction, but one of that size is far outside the effects it "
                      "measured."))])
    nclaim("buffer", "the buffer-exchange criterion of PCP-010 and objective (iii)", "The buffer-exchange criterion of "
           "PCP-010 could not be judged as planned, and the number of diavolumes at which the retentate reaches the "
           "formulation buffer was not established (objective iii not met).",
           [("buffer", q("The study record holds no conductivity or pH reading (`{python} PD[2]`), so the criterion "
                         "could not be judged as planned.")),
            ("buffer", q("The study gives the residual process buffer after each number of diavolumes, but not that "
                         "number."))], elsewhere=f"{PD[2]}, {PD[7]}")
    nclaim("mech", "Donnan and volume-exclusion effects", "The study gives no evidence on the Donnan and "
           "volume-exclusion effects, because the pH and the excipient levels of the final retentate were not "
           "measured.",
           [("mech", q("It therefore gives no evidence on the Donnan and volume-exclusion effects that can move them "
                       "away from the values of the buffer at high concentration."))])
    nclaim("mech", "where in the step aggregate forms", "The explanation that extra diavolumes at the lower "
           "concentration of diafiltration add little aggregate is not tested.",
           [("mech", q("The study did not measure where in the step aggregate forms, so this explanation is not "
                       "tested."))])
    nclaim("cap", "capability of the acidic charge variants from the study's own results", "The report cannot confirm "
           "the simulated capability of the acidic charge variants from its own results.",
           [("cap", q("The results of this study do not confirm the simulated level.")),
            ("cap", q("The capability of the acidic charge variants therefore depends on the level that the upstream "
                      "steps deliver, and this report cannot settle it from its own results."))],
           elsewhere="PCMR-001")
    nclaim("class", "critical process parameters", "The step has no CPP and no well-controlled CPP.",
           [("class", q("The step has no CPP and no well-controlled CPP."))])

    entities = [
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("exec"), process_steps=[step], sites=sites),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("uo"), document_relationships=rels,
                                  non_claims=nc_at["uo"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("changes"), non_claims=nc_at["changes"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cqa"), quality_attributes=attrs,
                                  non_claims=nc_at["cqa"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("sdm"), equipment=equipment,
                                  non_claims=nc_at["sdm"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("analytics"), analytical_methods=methods),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("sampling"), non_claims=nc_at["sampling"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("stats"), non_claims=nc_at["stats"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("factors"), parameters=params),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("effects"), model_fits=fits),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("yield"), performance_measures=perf),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("buffer"), non_claims=nc_at["buffer"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("mech"), non_claims=nc_at["mech"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("ds"), non_claims=nc_at["ds"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("par"), non_claims=nc_at["par"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("cap"), capabilities=capab,
                                  non_claims=nc_at["cap"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("class"), non_claims=nc_at["class"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("control"), control_strategy=cs_els),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("record"), deviations=devs),
    ]

    # ==== studies ===========================================================================================
    sdm_out = [_cells(r)[0] for r in offrow.values()]
    studies = [
        S.StudyDesign(
            study_id=f"study:{SDM_ST}", study_type="scale_down_qualification",
            design_name="set-point runs of the bench-scale TFF model against manufacturing-scale batches",
            unit_operation=UO_NAME, responses=sdm_out, scale_down_model=sdm_name,
            source_references=[ref("sdm", q_qual),
                               ref("sdm", q("It compared `{python} w(N_SD)` runs of the model at the set-point "
                                            "condition with `{python} w(N_M)` batches at manufacturing scale.")),
                               ref("analytics", soprow["SOP-1001"], sop_t, soprow)]
            + [ref("sdm", r_, off_t, offrow) for r_ in offrow.values()]
            + [ref("app_b", r_, run_t, runrow) for r_ in runrow.values()] + [pdref(PD[5])],
            metadata=meta()),
        S.StudyDesign(
            study_id=f"study:{UNI_ST}", study_type="univariate",
            design_name="planned univariate study (PCP-010 §6.2): both edges of the range studied and the "
                        "set-point of each parameter; no result for any parameter effect is in the record",
            unit_operation=UO_NAME, factors=[NAME[k] for k in PK], scale_down_model=sdm_name,
            associated_parameters=[PC[NAME[k]] for k in PK],
            source_references=[ref("uni_design", q("PCP-010 §6.2 planned the univariate study `{python} UNI_ID`.")),
                               ref("uni_design", q("The planned study ran from `{python} UNI_START` to "
                                                   "`{python} UNI_END` on `{python} UNI_EQ`, the skid of the "
                                                   "qualification.")),
                               ref("uni_design", q("No result of it for any parameter effect is in the record, and "
                                                   "Version 1.0 described its outcome without one."))],
            metadata=meta()),
        S.StudyDesign(
            study_id=f"study:{UNI2_ST}", study_type="univariate",
            design_name="five levels of each parameter across its range studied, in duplicate, the other "
                        "parameters at their set-points; made during the re-analysis",
            unit_operation=UO_NAME, factors=[NAME[k] for k in PK],
            responses=[RLAB[r] for r in RESP], scale_down_model=skid2_name,
            associated_parameters=[PC[NAME[k]] for k in PK],
            source_references=[ref("uni_design", q("The further univariate study `{python} UNI2_ID` was made from "
                                                   "`{python} UNI2_START` to `{python} UNI2_END`, during the "
                                                   "re-analysis and after INV-001 closed on `{python} INV[\"closed\"]`.")),
                               ref("uni_design", q("Each parameter was run at `{python} w(N_LEV)` levels, in duplicate, "
                                                   "with the other two at their set-points.")),
                               ref("uni_design", q("The study has `{python} N_RUNS2` runs, `{python} w(N_SP2)` of them "
                                                   "at the set-point condition."))]
            + [ref("factors", farow[k], fa_t, farow) for k in PK]
            + [ref("sampling", smprow[s_], smp_t, smprow) for s_ in smprow]
            + [ref("app_a", r_, uni_t, unirow) for r_ in unirow.values()] + [pdref(PD[1])],
            metadata=meta()),
    ]

    # ==== proven acceptable ranges: one per parameter and attribute it rests on =============================
    q_par_ag = q("Every aggregate result met the criterion of `{python} CRIT_AG` at manufacturing scale, also with "
                 "the offset at the end of its interval that is least favourable to the criterion.")
    q_par_ac = q("Every result of the acidic charge variants lay within the criterion of `{python} CRIT_AC`, at both "
                 "ends.")
    basis = {AG: t("Drug substance criterion `{python} CRIT_AG` (no step follows UF/DF, PCMP-001 §7.6), judged on each "
                   "individual result at manufacturing scale (aggregate offset subtracted), with the other parameters "
                   "at their set-points (PCP-010 §8)."),
             AC: t("Drug substance criterion `{python} CRIT_AC`, both ends (no step follows UF/DF, PCMP-001 §7.6), "
                   "judged on each individual result as measured, with the other parameters at their set-points "
                   "(PCP-010 §8).")}
    alab = {AG: names["aggregates_hmw"], AC: names["acidic_variants"]}
    pars = []
    for resp, qq in ((AG, q_par_ag), (AC, q_par_ac)):
        for k in PK:
            pars.append(S.ProvenAcceptableRange(
                par_id=f"{DOC}-PAR{len(pars) + 1:02d}", unit_operation=UO_NAME, quality_attribute=alab[resp],
                parameter=NAME[k], characterization_range=rng_s(k),
                par_at_setpoint=f"{fg(PARS[k][0])}–{fg(PARS[k][1])} {UNIT[k]}", acceptance_basis=basis[resp],
                source_references=[ref("par", parow[k], pa_t, parow), ref("agg" if resp == AG else "acidic", qq)],
                metadata=meta()))

    # ==== acceptance criteria the report states =============================================================
    ACC_AG, ACC_AC = ns["ACC_AG"], ns["ACC_AC"]
    unit = {k: P.CFG.cqa(k)["unit"] for k in ckeys}
    q_crit = q("Aggregate must not exceed `{python} fg(AG_HI)` % HMW, and the acidic charge variants must lie between "
               "`{python} fg(AC_LO)` and `{python} fg(AC_HI)` %.")
    q_v1_ac = q("Version 1.0 read them against the upper limit of `{python} fg(AC_HI)` % alone (INV-001 finding 4), "
                "although Version 1.0 of the plan stated the two-sided criterion.")
    q_dna_crit = q("Residual DNA is judged in ng per dose, the unit of its criterion of `{python} fg(DNA_CRIT)` ng per "
                   "dose.")
    crit_sec = _sid("basis_par")
    acrit = [
        S.AcceptanceCriterionRecord(step=UO, attribute="aggregates_hmw", high=float(ACC_AG[1]),
                                    unit=unit["aggregates_hmw"], basis="drug substance", revision=P.REV2["rev"],
                                    status="in force", source=ref("basis_par", q_crit)),
        S.AcceptanceCriterionRecord(step=UO, attribute="acidic_variants", low=float(ACC_AC[0]), high=float(ACC_AC[1]),
                                    unit=unit["acidic_variants"], basis="drug substance, both ends",
                                    revision=P.REV2["rev"], status="in force", source=ref("basis_par", q_crit)),
        S.AcceptanceCriterionRecord(step=UO, attribute="acidic_variants", high=float(ACC_AC[1]),
                                    unit=unit["acidic_variants"],
                                    basis="drug substance upper limit alone, as Version 1.0 of the report read it "
                                          "(INV-001 finding 4); Version 1.0 of the plan stated the two-sided criterion",
                                    revision=P.REV1["rev"], status="superseded", source=ref("changes", q_v1_ac)),
        S.AcceptanceCriterionRecord(step=UO, attribute="residual_dna", high=float(ns["DNA_CRIT"]),
                                    unit=unit["residual_dna"],
                                    basis="drug substance, judged on the integrated process model",
                                    revision=P.REV2["rev"], status="in force", source=ref("cap", q_dna_crit)),
        S.AcceptanceCriterionRecord(step=UO, attribute="buffer_exchange", low=float(NOR["diavolumes"][0]),
                                    unit=UNIT["diavolumes"],
                                    basis="the minimum number of diavolumes, the lower edge of the one-sided NOR, "
                                          "with the formulation buffer of the drug substance confirmed against its "
                                          f"release limits ({PD[7]}); the conductivity plateau criterion of PCP-010 "
                                          "§7.2 could not be judged",
                                    revision=P.REV2["rev"], status="in force", source=pdref(PD[7])),
        S.AcceptanceCriterionRecord(step="cex", attribute="aggregates_hmw", high=float(fx(ns["CEX_AG"])),
                                    unit=unit["aggregates_hmw"],
                                    basis="cation exchange pool, tightened on verification: the drug substance "
                                          "criterion minus the one-sided 95 % prediction bound of a single run of the "
                                          f"aggregate rise across the NORs of UF/DF ({PD[8]})",
                                    revision=P.REV2["rev"], status="in force", source=ref("basis_par", q_pcr007)),
    ]
    del crit_sec

    # ==== assertions ======================================================================================
    AS = []

    def add(subj, pred, obj, txt, refs):
        AS.append(EvidenceBackedAssertion(
            assertion_id=f"{DOC}-A{len(AS) + 1:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=txt, source_references=refs, metadata=meta()))

    add(STEP_ID, "step_uses_equipment", SDM_ID, f"The scale-down model of {UO_NAME} is the {sdm_name}, on which the "
        f"qualification {SDM_ST} ran.", [ref("sdm", q_qual)])
    add(STEP_ID, "step_uses_equipment", SKID2_ID, f"The univariate study {UNI2_ST} ran on the {skid2_name}, with the "
        f"offsets of {SDM_EQ} applied ({PD[1]}).", [ref("uni_design", q_skid2)])
    add(STEP_ID, "step_uses_equipment", MEMBRANE_ID, f"{UO_NAME} works across a tangential flow membrane that passes "
        f"buffer salts and retains the antibody.", [ref("uo", q_membrane)])
    for k in PK:
        add(STEP_ID, "step_has_parameter", PC[NAME[k]],
            f"{UO_NAME} has process parameter {NAME[k]}, classified {CLS[k]}, studied univariately.",
            [ref("factors", farow[k], fa_t, farow)])
    for key in ckeys:
        add(STEP_ID, "step_has_quality_attribute", f"attr:{key}",
            f"{names[key]} is in scope at {UO_NAME}: {_cells(crow[key])[-1]}.", [ref("cqa", crow[key], cq_t, crow)])
    for amv, key in ((a, attr_of[a]) for a in msrow if a in attr_of):
        r = ms_df.loc[amv]
        add(f"attr:{key}", "attribute_measured_by_method", f"method:{amv}",
            f"{names[key]} is measured by {r['Technique'][0].lower() + r['Technique'][1:]} ({amv}) in the "
            f"{r['Sample'][0].lower() + r['Sample'][1:]}, reported as {r['Reported as']}.",
            [ref("app_c", msrow[amv], ms_t, msrow)])
    for key in ckeys:
        add(f"attr:{key}", "attribute_has_acceptance_criterion", f"lit:{UO}_{key}_ds",
            f"At UF/DF {names[key]} is judged against the drug substance criterion "
            f"{_cells(crow[key])[2]}; no step follows UF/DF, so PCMP-001 defines no intermediate acceptance "
            f"criterion for it.", [ref("cqa", crow[key], cq_t, crow)])
    add("attr:aggregates_hmw", "attribute_has_acceptance_criterion", "lit:cex_aggregates_hmw_iac",
        t("The aggregate criterion of the cation exchange pool is tightened from `{python} fx(AG_HI)` to "
          "`{python} fx(CEX_AG)` % HMW by the one-sided 95 % prediction bound of the aggregate rise across the NORs of "
          "UF/DF, `{python} fx(UF_ALLOW, 3)` percentage points."), [ref("basis_par", q_pcr007)])
    akey = {AG: "aggregates_hmw", AC: "acidic_variants"}
    for k in PK:
        for r in (AG, AC):
            row = slrow[(k, r)]
            c = _cells(row)
            sig = (k, r) in SIG
            add(PC[NAME[k]], "parameter_impacts_attribute" if sig else
                "parameter_does_not_significantly_impact_attribute", f"attr:{akey[r]}",
                f"{NAME[k]} on {names[akey[r]]} ({UNI2_ST}, {rng_s(k)}): change across the range studied {c[2]} "
                f"percentage points, 95 % confidence interval {c[3]}, p {_unmark(c[4])}; "
                + ("significant." if sig else "not significant."),
                [ref("effects", row, sl_t, slrow)])

    # ==== report statements, grouped by the chapters of the report =========================================
    STS = []

    def clean(s):
        s = re.sub(r"\(\s+", "(", s)
        return re.sub(r"\s+([,.;:)])", r"\1", s)

    def st(sec, txt, refs):
        STS.append((SEC[sec][0], ReportStatement(
            statement_id=f"{DOC}-S{len(STS) + 1:03d}", statement_text=txt, confidence="high",
            review_status="accepted", source_references=refs)))

    def sq(sec, src, txt=None, extra=()):
        st(sec, t(txt) if txt else clean(q(src)), [ref(sec, q(src))] + [ref(s_, q(x)) for s_, x in extra])

    def srow(sec, txt, row, tab=None, rows_=None, caption=None, label=None):
        st(sec, txt, [ref(sec, row, tab, rows_, caption=caption, label=label)])

    # -- Executive summary ----------------------------------------------------------------------------------
    sq("exec", "The step has no designed experiment.")
    sq("exec", "The risk assessment RA-001 assigned its `{python} w(N_P)` parameters, the `{python} nm[\"diavolumes\"]`, "
               "the `{python} nm[\"tmp\"]` (TMP) and the `{python} nm[\"final_conc\"]`, to univariate study.")
    sq("exec", "Version 1.0 of this report described the planned univariate study `{python} UNI_ID` without a result "
               "for any parameter effect.")
    sq("exec", "The results reported here come from a further univariate study, `{python} UNI2_ID`, made from "
               "`{python} UNI2_START` to `{python} UNI2_END`, after the QA investigation INV-001 had closed.")
    sq("exec", "The offsets are applied to the results of the second skid, because the two skids share their design "
               "and their membrane and the offsets are small against the criteria (`{python} PD1`).")
    sq("exec", "Every result met the drug substance criteria for aggregate (`{python} CRIT_AG`) and for the acidic "
               "charge variants (`{python} CRIT_AC`), at every level of every parameter.")
    sq("exec", "The proven acceptable range (PAR) of each parameter is therefore its range studied, "
               "`{python} rng_s(\"diavolumes\")`, `{python} rng_s(\"tmp\")` and `{python} rng_s(\"final_conc\")`.")
    sq("exec", "Aggregate in the final retentate rose with the final DS concentration (`{python} pe(sC[\"p\"])`) and "
               "with TMP (`{python} pe(sT[\"p\"])`).")
    sq("exec", "Across the ranges studied the two effects amount to `{python} fx(sC[\"ch\"])` and "
               "`{python} fx(sT[\"ch\"])` percentage points, and the highest result lay `{python} fx(AGG_MARGIN)` "
               "percentage points below the criterion.")
    sq("exec", "The A-Mab case study leaves UF/DF out, so no published source gave the size of this effect in advance.")
    sq("exec", "PCMP-001 assumed that no step after cation exchange changes aggregate.",
       "PCMP-001 assumed that no step after cation exchange changes aggregate; a check of that assumption on "
       "`{python} UNI2_ID` found a rise across the NORs of UF/DF of up to `{python} fx(UF_ALLOW, 3)` percentage points "
       "at the one-sided 95 % prediction bound of a single run (`{python} PD[8]`).",
       extra=[("exec", "A check of that assumption on `{python} UNI2_ID` found a rise of aggregate across the NORs of "
                       "UF/DF of up to `{python} fx(UF_ALLOW, 3)` percentage points, at the one-sided 95 % prediction "
                       "bound of a single run (`{python} PD[8]`).")])
    sq("exec", "This prediction bound of the aggregate rise across the step tightens the aggregate criterion of the "
               "cation exchange pool from `{python} fx(AG_HI)` to `{python} fx(CEX_AG)` % HMW.")
    sq("exec", "The residual process buffer fell by a factor of `{python} fx(RB_FOLD)` for each diavolume, the fall "
               "expected when the buffer species pass the membrane freely.")
    sq("exec", "The buffer-exchange criterion of PCP-010 rests on conductivity readings that are not in the study "
               "record, so it could not be judged as planned.")
    sq("exec", "All `{python} w(N_P)` parameters were classified as key process parameters (KPPs), and the step has no "
               "critical process parameter.")
    sq("exec", "In the integrated process model of `{python} N_MC_S` simulated batches the drug substance has a Cpk of "
               "`{python} fx(CPK_AG, 1)` for aggregate, `{python} fx(CPK_AC)` for the acidic charge variants and "
               "`{python} fx(CPK_DNA, 1)` for residual DNA, which is judged in ng per dose.")
    sq("exec", "This step can only raise the acidic charge variants, by deamidation, so it moves them away from that "
               "limit.")
    sq("exec", "At the mean of the study, with the simulated standard deviation, the Cpk would be "
               "`{python} fx(CPK_AC_MEAS)`, below the minimum, so this report cannot confirm the simulated capability "
               "from its own results (@sec-capability).")

    # -- Introduction ---------------------------------------------------------------------------------------
    sq("uo", "Aggregate and the acidic charge variants are therefore the attributes measured across the step.")
    sq("uo", "The residual process buffer, the step yield and the final concentration are measures of process "
             "performance.")
    obj_list = re.findall(r"^\(([ivx]+)\) (.+)$", src_all.split("\n## Objectives", 1)[1].split("\n## ", 1)[0],
                          flags=re.M)
    if len(obj_list) != 5:
        raise ValueError(f"{DOC}: {len(obj_list)} objectives under '## Objectives', the text has five")
    for num, obj in obj_list:
        st("objectives", f"Objective ({num}) of PCP-010: {clean(q(obj))}", [ref("objectives", q(obj))])
    sq("basis", "The case study leaves UF/DF out of its characterization ")
    sq("changes", "Version 1.0 of this report was approved on `{python} rev1_date(DOC)`.")
    sq("changes", "INV-001 found that the criteria used to judge each step in the PAR analysis had been set after the "
                  "data were seen and appeared in no approved plan (INV-001 finding 1).")
    sq("changes", "The master plan PCMP-001 was reissued as Version 2.0 with criteria derived a priori, and PCP-010 was "
                  "amended to apply it.")
    chg_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n## Changes in this revision", 1)[1]
                          .split("\n# ", 1)[0], flags=re.M)
    if len(chg_list) != 11:
        raise ValueError(f"{DOC}: {len(chg_list)} numbered changes, the report lists eleven")
    for i, item in enumerate(chg_list, 1):
        first = re.split(r"(?<=\.) (?=[A-Z`])", item)[0]
        st("changes", f"Change {i} of Version 2.0: {clean(q(first))}", [ref("changes", q(first))])
    sq("changes", "Two statements of Version 1.0 are reversed.")
    sq("changes", "Version 1.0 stated that no effect of any parameter on product quality was detected over the ranges "
                  "assessed.", extra=[("changes", "Aggregate rises with the final DS concentration and with TMP "
                                                  "(@sec-aggregate).")])

    # -- Prior knowledge and quality risk basis --------------------------------------------------------------
    sq("platform", "The step belongs to the platform train that was used for X-Mab, Y-Mab and Z-Mab (PCMP-001 §2).")
    sq("platform", "For this reason the final DS concentration was studied for A-Mab and was not carried over from the "
                   "platform.")
    sq("platform", "PCP-010 §4.1 expects the residual process buffer components to fall \"roughly exponentially\" with "
                   "the number of diavolumes.")
    sq("platform", "Aggregate was therefore expected to rise with TMP below the limiting flux, and it may still rise "
                   "above it.")
    sq("platform", "No source gave their size for A-Mab, so this study measures it (@sec-aggregate).")
    sq("platform", "The effect of a high final DS concentration and a high TMP on aggregate is this campaign's own "
                   "addition to the integrated process model (@sec-stats).")
    sq("platform", "The acidic charge variants were therefore expected to rise, if at all, with the number of "
                   "diavolumes and the final DS concentration, and to fall with TMP.")
    sq("cqa", "It is not measured across the step and has no intermediate criterion, so it is judged on the drug "
              "substance in the integrated process model (PCMP-001 §7.3, @sec-capability).")
    sq("cqa", "PCMP-001 Table 7.1 assumes that this step does not change fragments, and the drug substance is tested "
              "for fragments at release.")
    sq("risk", "The rise of aggregate with TMP may therefore be larger at a high final DS concentration than at a low "
               "one.")
    sq("risk", "A study that varies one factor at a time cannot resolve such an interaction.")

    # -- Materials and methods ------------------------------------------------------------------------------
    sq("sdm", "A slightly lower step yield and slightly more aggregate were expected at bench scale.")
    sq("sdm", "The scale-down runs were complete on `{python} SDM_END`, before the first characterization run of the "
              "step on `{python} UNI_START`, as PCMP-001 §7.1 requires.")
    sq("sdm", "The bench skid gave a mean aggregate `{python} fx(OFF[AG][\"offset\"])` percentage points higher and a "
              "mean step yield `{python} fx(-100 * OFF[\"step_yield\"][\"offset\"], 1)` percentage points lower than "
              "manufacturing scale.")
    for key, row in offrow.items():
        c = _cells(row)
        srow("sdm", f"Scale-down model offset of {c[0]} (scale-down minus manufacturing scale): {c[5]}, "
                    f"{ns['OFF_CI']} % confidence interval {c[6]}; qualification decision on a response-surface model: "
                    f"{_unmark(c[7])}, {_unmark(c[8])}.", row, off_t, offrow)
    sq("sdm", "The aggregate offset is therefore subtracted directly from each aggregate result of the final "
              "retentate.")
    sq("sdm", "This report keeps the logic of PCMP-001 §7.1, that a model is qualified for an output when the "
              "conclusion over the NOR is the same with the offset at its estimate and at either end of its interval.")
    sq("sdm", "All `{python} N_IN_NOR` aggregate results inside the NOR met the criterion in all three cases, so the "
              "model is qualified for aggregate under this approach.")
    sq("operation", "The composition of the formulation buffer is fixed by the drug product program and was a constant "
                    "of the studies.")
    sq("operation", "The study record of `{python} UNI2_ID` does not identify the load pool of its runs, so it cannot "
                    "show that one pool served the whole study (`{python} PD[4]`).")
    sq("analytics", "The record names neither the buffer species measured nor the method, and it holds no conductivity "
                    "or pH reading (`{python} PD[2]`).")
    sq("analytics", "A measured change is judged against the pure error of the study and not against the nominal "
                    "precision of the method.")
    for s_, row in smprow.items():
        c = _cells(row)
        srow("sampling", f"Sample '{s_}' ({c[1]}): tests planned in PCP-010 {c[2]}; results in the record of "
                         f"{UNI2_ST}: {c[3]}.", row, smp_t, smprow)
    sq("stats", "The criterion, and not the p-value, decides whether a range is acceptable.")
    sq("stats", "This study replicates every level, so the pure error is pooled over all of them (`{python} PD[6]`).")
    sq("stats", "The rule for the low end of the method range therefore does not apply to them, and the slope test "
                "alone decides.")
    sq("stats", "The PAR of a parameter is the contiguous span of levels over which every attribute measured on the "
                "final retentate met its criterion, with the other parameters at their set-points (PCP-010 §8).")
    sq("stats", "It cannot show the randomized order that PCP-010 §6.2 requires, and a drift over the course of the "
                "study could not be separated from a slope.")
    sq("stats", "The model includes the effects of the UF/DF parameters on aggregate and no effect of them on the "
                "acidic charge variants.")

    # -- Study design ---------------------------------------------------------------------------------------
    sq("factors", "Each range studied extends beyond the NOR at one end or at both, and it is the knowledge space "
                  "within which a PAR can be claimed.")
    sq("factors", "The study does not go below the minimum.")
    sq("factors", "A lower TMP lowers the flux and lengthens the operation, and the study does not characterize that "
                  "side.")
    sq("factors", "No PAR is claimed beyond the range studied (PCMP-001 §7.6).")
    sq("uni_design", "`{python} UNI2_ID` is not a designed experiment, and no run combines the levels of two "
                     "parameters.")
    sq("uni_design", "The effects, PARs and classes of this report rest on one parameter at a time.")
    sq("uni_design", "The study differs from the plan in its levels, its replicates and its skid (`{python} PD1`).")

    # -- Results --------------------------------------------------------------------------------------------
    for r, row in rprow.items():
        c = _cells(row)
        srow("repro", f"{c[0]} in {UNI2_ST}: pure error {c[1]} ({ns['PE_DF']} degrees of freedom); the "
                      f"{ns['N_SP2']} set-point runs gave mean {c[2]}, SD {c[3]}, lowest {c[4]}, highest {c[5]}.",
             row, rp_t, rprow)
    sq("effects", "Of the `{python} N_SLOPES` slopes, `{python} w(N_SIG)` were significant at α = `{python} fg(ALPHA)`.")
    sq("effects", "No slope of the acidic charge variants or of the step yield was significant, and neither TMP nor "
                  "the final DS concentration had a significant slope on the residual process buffer.")
    sq("agg", "Aggregate rose with the final DS concentration.")
    sq("agg", "Both changes across the range are larger than the pure error of `{python} fx(PE[AG][0], 3)` percentage "
              "points.")
    sq("agg", "This report judges both changes small against the criterion (`{python} PD[6]`).")
    sq("agg", "The data do not show that rise at the precision of the study, and an effect within the interval cannot "
              "be excluded.")
    sq("acidic", "A change of up to `{python} fx(AC_CH_BOUND, 1)` percentage points across a range therefore cannot be "
                 "excluded.")
    sq("acidic", "Without a load result the study cannot say how much the step adds at the set-point condition "
                 "(@sec-sampling).")
    sq("buffer", "The residual process buffer fell exponentially with the number of diavolumes (@fig-buffer).")
    sq("buffer", "Each diavolume removed `{python} fx(RB_REMOVED, 0)` % of the process buffer that remained, and the "
                 "residual fell by a factor of `{python} fx(RB_FOLD)` per diavolume.")
    sq("buffer", "The residual process buffer cannot stand in for the conductivity.")
    sq("buffer", "The buffer exchange is controlled instead by its minimum number of diavolumes, "
                 "`{python} u_(\"diavolumes\", NOR[\"diavolumes\"][0])`, the lower edge of a one-sided NOR.")
    sq("yield", "The step yield has no criterion and is reported for information.")
    sq("yield", "The final concentration followed its setting in the series of the final DS concentration, with a "
                "slope of `{python} fx(sFC[\"slope\"], 3)` (95 % confidence interval `{python} fx(sFC[\"lo\"], 3)` to "
                "`{python} fx(sFC[\"hi\"], 3)`).")
    sq("mech", "The rise of aggregate with the final DS concentration and with TMP is consistent with aggregate forming "
               "in the polarization layer at the membrane wall.")
    sq("mech", "The study did not measure the flux across the TMP range, so it cannot say on which side of the limiting "
               "flux the set-point lies.")
    sq("mech", "The study record does not give the duration of the runs, so the study cannot relate the acidic charge "
               "variants to the time in solution.")

    # -- Design space ----------------------------------------------------------------------------------------
    sq("ds", "The step is described instead by the univariate PAR of each parameter, which equals its range studied "
             "(@sec-pars).")
    sq("ds", "These data support the movement of one parameter within its PAR, with the others at their set-points.")
    sq("ds", "An excursion outside a NOR in manufacture is dispositioned against the PAR (PCP-010 §8).")

    # -- Proven acceptable ranges ------------------------------------------------------------------------------
    sq("basis_par", "No step follows UF/DF, so PCMP-001 Table 7.1 defines no IAC for it, and the drug substance "
                    "criteria apply directly (PCMP-001 §7.6).")
    sq("basis_par", "This study shows that two parameters of UF/DF raise aggregate within their NORs.")
    sq("basis_par", "PCP-010 §7.2 planned no verification at this step (`{python} PD[8]`).")
    sq("basis_par", "The one-sided 95 % prediction bound of a single run puts the rise at `{python} fx(UF_ALLOW, 3)` "
                    "percentage points.")
    sq("basis_par", "Here the bound replaces the assumption of no change, and every aggregate criterion upstream "
                    "carries it.")
    sq("basis_par", "Deamidation moves the acidic charge variants away from the lower limit of `{python} fg(AC_LO)` %, "
                    "which is the limiting side (@sec-capability), so the assumption errs on the safe side for that "
                    "limit.")
    sq("criteria", "Every attribute result of every level met its criterion, so every level is acceptable.")
    sq("criteria", "The largest significant change of an attribute across a range, `{python} fx(sC[\"ch\"])` percentage "
                   "points of aggregate for the final DS concentration, is `{python} fx(SHARE_C_CRIT, 1)` % of the "
                   "criterion of `{python} fg(AG_HI)` % HMW.")
    sq("criteria", "No level failed, so the rules for a failing level were not used, and the study record shows no "
                   "repeated run.")
    lv_par = None
    for row in lvrow.values():
        c = _cells(row)
        lv_par = c[0] or lv_par
        srow("criteria", f"{lv_par}, {c[1].lower()} level, setting {c[2]} (inside the NOR: {c[3].lower()}): aggregate "
                         f"at manufacturing scale {c[4]} % HMW, acidic charge variants {c[5]} %; every result met its "
                         f"criterion.", row, lv_t, lvrow)
    sq("par", "Each PAR rests on aggregate and the acidic charge variants, the attributes the study measured, and on no "
              "other attribute.")
    sq("par", "This report judges that no attribute approached its criterion at an edge, and no such runs were made.")
    sq("par", "An interaction would have to add a further `{python} fx(GAP_RNG)` percentage points there, about "
              "`{python} fx(RATIO_RNG, 0)` times the rise that the two slopes give, to bring that run to the "
              "criterion.")

    # -- Process capability and robustness -----------------------------------------------------------------------
    sq("cap", "A Cpk this large says only that the criterion lies far beyond the simulated batches.")
    sq("cap", "With none of `{python} N_MC_S` outside, the one-sided 95 % upper confidence bound of the probability of "
              "a batch outside is `{python} fx(P_UB_PCT, 2)` %.")
    sq("cap", "This step does not move the acidic charge variants toward that lower limit.")
    sq("cap", "At the mean of the study, `{python} fx(AC_MEAN, 1)` %, with the simulated standard deviation, the Cpk "
              "would be `{python} fx(CPK_AC_MEAS)`, below the minimum.")
    sq("cap", "It is computed from the DNA clearance that the integrated process model credits to each purification "
              "step, which is an input from outside the data of this step.")

    # -- Parameter classification -------------------------------------------------------------------------------
    sq("class", "The parameters were classified under SOP-4001 by the rules of PCMP-001 §7.7, which follow the "
                "decision logic of the A-Mab case study ")
    sq("class", "A significant effect on a CQA therefore makes a parameter critical unless the effect is too small to "
                "be practically relevant, and PCMP-001 and SOP-4001 set no threshold for that.")

    # -- Contribution to the control strategy -------------------------------------------------------------------
    sq("control", "The control strategy for the drug substance process is consolidated in PCMR-001.")

    # -- Discussion -----------------------------------------------------------------------------------------------
    sq("disc", "Two parameters of UF/DF, the final DS concentration and TMP, raise aggregate.")
    sq("disc", "They still matter upstream.")
    sq("disc", "Three points limit that confidence.")
    sq("disc", "The study record of `{python} UNI2_ID` is incomplete against the plan in ways that bear on its "
               "reading.")
    sq("disc", "The main scientific limitation is the univariate design, which cannot measure an interaction.")
    sq("disc", "Each slope rests on `{python} SLDF` degrees of freedom, so an effect smaller than the confidence "
               "intervals of @tbl-slopes may have gone undetected, for the acidic charge variants in particular.")
    sq("disc", "PCMR-001 assesses this attribute across the whole process.")

    # -- Conclusions (the numbered list of the .qmd) ----------------------------------------------------------
    con_list = re.findall(r"^\d+\. (.+)$", src_all.split("\n# Conclusions", 1)[1].split("\n# ", 1)[0], flags=re.M)
    if len(con_list) != 6:
        raise ValueError(f"{DOC}: {len(con_list)} numbered conclusions, the report has six")
    for i, con in enumerate(con_list, 1):
        sent = re.split(r"(?<=\.) (?=[A-Z`])", con)
        st("concl", f"Conclusion {i}: {clean(render(con))}", [ref("concl", q(sent[0]))])

    # -- Study events and discrepancies from the plan -------------------------------------------------------------
    sq("record", "PCP-010 §13 keeps the wording of Version 1.0, which records a departure from the plan during "
                 "execution as a deviation.")
    sq("record", "The discrepancies from the plan are the departures from PCP-010, both work that the plan did not "
                 "foresee and requirements of the plan that were not met.")
    sq("events", "The record of each event names neither the study nor the run in which it occurred.")
    sq("events", "No result of the planned study is in the record, so an event in one of its runs affects no result of "
                 "this report.")
    for pid, row in pdrow.items():
        d = PDS[pid]
        srow("pds", f"Discrepancy {pid} from PCP-010, {d['subject']}: planned {d['planned']}; done {d['done']}; "
                    f"reason {d['reason']}.", row, rows_=pdrow, caption=pd_cap, label="tbl-discrepancies")
    sq("pds", "No result for a parameter effect existed when it was made, so no conclusion rests on runs added after a "
              "result was known.")

    # -- Appendices ----------------------------------------------------------------------------------------------
    sq("app_a", "Aggregate is given as measured and at manufacturing scale, the result minus the aggregate offset of "
                "@tbl-sdm-offsets.")
    st("app_b", f"The qualification record does not name the manufacturing-scale batches.",
       [ref("app_b", note_span("tbl-sdm-runs", "The record does not name"))])

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
                        aliases=["UF/DF", "ultrafiltration and diafiltration", P.DOC_REGISTRY[DOC][1],
                                 f"Step {ns['STEP_N']}"], review_status="human_verified")]
    alias = {"diavolumes": ["diavolumes", "DV"], "tmp": ["TMP"], "final_conc": ["final concentration"]}
    concepts += [Concept(concept_id=PC[NAME[k]], concept_type="PROCESS_PARAMETER", canonical_name=NAME[k],
                         aliases=alias[k], review_status="human_verified") for k in PK]
    concepts += G._attr_concepts(ckeys)
    concepts += G._method_concepts([m.method_id for m in methods], amv_title)
    concepts += [Concept(concept_id=e.equipment_id, concept_type="EQUIPMENT", canonical_name=e.equipment_name,
                         review_status="human_verified") for e in equipment]

    # ==== the annex =========================================================================================
    annex = S.GroundTruthAnnex(
        document_id=DOC, document_title=f"{P.DOC_REGISTRY[DOC][0]} — {P.DOC_REGISTRY[DOC][1]}",
        document_class=P.DOC_REGISTRY[DOC][0], **G.rev2_layer(DOC, FILE),
        schema_extensions_used=G.COMMON_EXT + G.REV2_EXT + [
            "ProvenAcceptableRange (new model) — per attribute x parameter PAR; at a step without a fitted model "
            "only the range at set-point, which is the range studied",
            "RhetoricalSpan (new model) — argument-structure roles over the report prose",
        ],
        out_of_schema_notes=[
            "UF/DF has no designed experiment and the report defines no design space (an ExplicitNonClaim, with the "
            "reason the report gives). design_spaces is empty.",
            "ProcessParameter.target_value and NOR are the set-point and NOR in force; the NOR of the number of "
            "diavolumes is one-sided, a minimum ('≥ 7 DV'), as the report prints it. ProcessParameter.PAR is the "
            "univariate PAR, which equals the range studied. rationale_for_criticality carries the classification "
            "argument of the report, which names the KPP class of TMP and the final DS concentration as a judgement "
            "that their effect on aggregate is too small to be practically relevant.",
            "QualityAttribute records are the three attributes of the attribute table: aggregate and the acidic charge "
            "variants, measured in the final retentate, and residual DNA, not measured at the step and judged on the "
            "drug substance in the integrated process model. No step follows UF/DF, so the drug substance criterion "
            "applies directly and PCMP-001 defines no intermediate acceptance criterion.",
            "proven_acceptable_ranges: one record per parameter and per attribute the PAR rests on (aggregate at "
            "manufacturing scale and the acidic charge variants as measured, each judged per individual result). "
            "par_at_setpoint is the PAR of the PAR table; par_nor_propagated is unset, because the step has no fitted "
            "model and the report says the second analysis of PCMP-001 §6.4 was not performed.",
            "StatisticalModelFit: the fifteen slopes of the slope table (one per parameter and output, ModelTerm.effect "
            "the change across the range studied as printed), the exponential fit of the buffer exchange, and the "
            "main-effects fit of aggregate used for the verification of the PCMP-001 assumption (PD-010-08), judged "
            "on the first three criteria of PCMP-001 §7.2. A p-value printed as '< 0.001' has no float value.",
            "acceptance_criteria: the report prints no criteria-change table. The in-force records are the drug "
            "substance criteria for aggregate, the acidic charge variants (both ends) and residual DNA, the "
            "buffer-exchange criterion as PD-010-07 records it (the minimum number of diavolumes with release of the "
            "drug substance against its formulation buffer limits; attribute 'buffer_exchange', not a CQA), and the "
            "aggregate criterion of the cation exchange pool (step 'cex') that the UF/DF allowance tightens. The "
            "superseded record is the upper limit alone against which Version 1.0 read the acidic charge variants "
            "(INV-001 finding 4).",
            "PerformanceMeasure records: the step yield, the final concentration achieved in the series run at the "
            "target, and the residual process buffer at the minimum number of diavolumes, each on its sentence and "
            "its row of the reproducibility table. ControlStrategyElement records are the four numbered elements "
            "of Section 10.",
            "Studies: S-UFDF-SDM (scale-down qualification), S-UFDF-UNI (the planned univariate study, which ran but "
            "left no result for any parameter effect) and S-UFDF-UNI2 (the further univariate study of the "
            "re-analysis, PD-010-01, on the second skid). None carries n_runs, which the corpus test reserves for the "
            "seeded DoE designs; the run counts are in the cited prose. Of the appendix rows only those that occur "
            "once in the document are used.",
            "The schema has no record type for a discrepancy from the plan. PD-010-01 to PD-010-08 are report "
            "statements anchored on their rows of the discrepancy register; PD-010-01 also anchors S-UFDF-UNI2, "
            "PD-010-05 S-UFDF-SDM and PD-010-07 the buffer-exchange criterion.",
            "The report records no deviation: a characterization study is not GMP manufacture, so the two events of "
            "execution are study events, under the numbers Version 1.0 gave them (DEV-010-01, DEV-010-02). They are "
            "Deviation records, the schema's only record type for an event of execution; no_impact_on_conclusions is "
            "true for both, as the conclusions state.",
            "parameter_impacts_attribute and parameter_does_not_significantly_impact_attribute: one assertion per "
            "parameter and measured attribute, on its row of the slope table. Residual DNA has none: the integrated "
            "process model gives the UF/DF parameters no effect on it. The residual process buffer, the step yield "
            "and the final concentration are process outputs, recorded as model fits and statements.",
            "The equipment ids follow the PCP-010 Version 2.0 annex (equip:ufdf_sdm, equip:ufdf_membrane); the second "
            "skid of S-UFDF-UNI2 is equip:ufdf_sdm_skid2.",
            "rhetorical_spans: authoring/rhetorical/PCR-010.spans.yaml, re-curated against the Version 2.0 text in the "
            "same pass as this builder. weak_claims is empty.",
        ],
        inventory=G.rev2_inventory(DOC, FILE, "process_characterization_report", UO_NAME,
                                   ["process characterization", "ultrafiltration and diafiltration",
                                    "tangential flow filtration", "buffer exchange", "univariate study",
                                    "scale-down offset", "drug substance criteria",
                                    "verification of platform worst cases", "parameter classification",
                                    "process capability"]),
        entities=entities, studies=studies, design_spaces=[], proven_acceptable_ranges=pars,
        report_sections=sections, assertions=AssertionStore(run_id=f"gt-{DOC}", assertions=AS, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{DOC}", concepts=concepts),
        weak_claims=[], rhetorical_spans=G.build_rhetorical_spans(DOC, FILE),
        acceptance_criteria=acrit)
    _gate(annex, text)
    return annex
