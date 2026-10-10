"""INV-002 Version 1.0, the investigation of the response-surface models below the model-adequacy
criteria of PCMP-001 Version 2.0: its ground-truth annex (``build()``).

INV-002 is new in the Version 2.0 package, so there is no Version 1.0 builder. The kinds of record
follow the investigation model, ``build_ground_truth.build_investigation`` (INV-001): the inventory,
the investigation itself and the deviation it cites as ``Deviation`` records, the documents it
names as ``DocumentRelationship`` records, its explicit non-claims, the finding, root cause,
remedy rule, corrective and preventive actions and closure as report statements, and assertions
anchored on the rows or the clauses that state them. INV-002 is a document about models, so it
also carries one ``StatisticalModelFit`` per model it prints, the response-surface designs and the
two augmentation designs as ``StudyDesign`` records, and the criteria it prints as in-force
``AcceptanceCriterionRecord`` entries.

Every table of the document is a complex table (``T.frame`` or a ``T.`` builder), read back
through ``qmd_ctables`` from the object the document printed, so each row quote comes from the call
that rendered the row, with ``table_header=rows.header``. Every prose quote is a sentence of the
``.qmd`` copied with its inline expressions and evaluated in the document's own namespace
(``qmd_inline``); no value is typed here. ``build()`` refuses to return an annex with a quote that
does not ground or a weak anchor, so a stale quote fails here and names itself.
"""
from __future__ import annotations

import os
import re

import _pcpkg as P
import build_ground_truth as G
import schema_ext as S
from check_grounding import CELL_SEP, normalize, specificity_report

DOC = "INV-002"
FILE = "INV-002_model_adequacy.docx"
QMD = "INV-002_model_adequacy.qmd"

_SEL = "Model selection (corrective action CA3)"
_CHG = "What model selection changed"
#: Section key -> heading path as the document renders it. ``build`` checks every title against the
#: headings of the .qmd, so a renamed section fails loudly instead of mislabelling its references.
SEC = {
    "title": ("Title block",),
    "abbr": ("Abbreviations",),
    "summary": ("Summary",),
    "event": ("Event description",),
    "scope": ("Scope",),
    "finding": ("Finding",),
    "root": ("Root cause",),
    "rule": ("Remedy and decision rule",),
    "ss_method": ("Sample-size calculation", "Method"),
    "ss_dopt": ("Sample-size calculation", "D-optimal augmentation"),
    "ss_results": ("Sample-size calculation", "Results"),
    "ss_power": ("Sample-size calculation", "Power of the effects"),
    "designs": ("Augmentation designs",),
    "des_bio": ("Augmentation designs", "Production bioreactor"),
    "des_aex": ("Augmentation designs", "Anion exchange"),
    "sel_proc": (_SEL, "Procedure"),
    "sel_log": (_SEL, "Why a log scale, and what it changes"),
    "sel_search": (_SEL, "How the model is searched"),
    "sel_verif": (_SEL, "Verification of the platform worst cases"),
    "sel_changed": (_SEL, _CHG),
    "sel_aug": (_SEL, _CHG, "The augmentations"),
    "sel_none": (_SEL, _CHG, "Outputs with no adequate model"),
    "sel_exact": (_SEL, _CHG, "An output that fits exactly"),
    "sel_zero": (_SEL, _CHG, "Outputs with no detected effect"),
    "impact": ("Impact assessment",),
    "imp_crit": ("Impact assessment", "Acceptance criteria"),
    "imp_nor": ("Impact assessment", "Conclusions over the NOR"),
    "imp_other": ("Impact assessment", "Other documents"),
    "capa": ("Corrective and preventive actions",),
    "eff": ("Effectiveness check",),
    "close": ("Conclusion and closure",),
}


def _sid(sec):
    return f"{DOC}_sec_{sec}"


def _check_sections():
    """Every heading of SEC is a heading of the .qmd (outside its code chunks)."""
    src = open(os.path.join(G.HERE, QMD), encoding="utf-8").read()
    prose = re.sub(r"```\{python\}.*?```", "", src, flags=re.S)
    heads = set(re.findall(r"^#+ (.+?)(?: \{[^}]*\})?\s*$", prose, flags=re.M))
    missing = sorted({t for path in SEC.values() for t in path if t != "Title block"} - heads)
    if missing:
        raise ValueError(f"{DOC}: section titles not in the document: {missing}")


def _cells(row):
    """The cells of a rendered row (``ctable_rows``): a continuation row keeps its empty cells."""
    return [c.strip() for c in row.split("|")]


def _nofoot(x):
    """A cell without its footnote markers ("acidic variants a) , fragments" -> "acidic variants,
    fragments"). The word boundary keeps "(planned runs)" and "(fold)" whole."""
    return re.sub(r"\s+,", ",", re.sub(r"\s*\^?\b[a-z]\)\^?", "", str(x))).strip()


def _num(s):
    """A number as the document prints it, back to a float ("−1.83", "16,000")."""
    return float(str(s).replace("−", "-").replace(",", ""))


def _smart(s):
    """Prose as pandoc renders it: a straight apostrophe becomes a typographic one. Table cells and
    table notes are raw markup and keep the straight form, so only prose quotes go through this."""
    return s.replace("'", "’")


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
    import doe_report as D
    import tables as T
    from annex_contract.assertions import AssertionStore, EvidenceBackedAssertion
    from annex_contract.concepts import Concept, ConceptStore
    from annex_contract.discourse import DocumentRelationship, ExplicitNonClaim
    from annex_contract.results import Deviation, ModelTerm, ModularContribution, StatisticalModelFit
    from annex_contract.summaries import ReportSection, ReportStatement

    _check_sections()
    ns, _ = G.qmd_namespace(QMD)
    ct = G.qmd_ctables(QMD)
    text = G._document_text(FILE)
    meta = G.meta

    def q(src):
        """A prose sentence of the .qmd as it renders."""
        return _smart(G.qmd_inline(ns, src))

    def qn(src):
        """A table note of the .qmd as it renders (no typographic apostrophe)."""
        return G.qmd_inline(ns, src)

    def ref(sec, quote, table=None, rows=None):
        r = G.ref(DOC, FILE, _sid(sec), SEC[sec][-1], quote,
                  table_title=None if table is None else table.caption,
                  table_id=None if table is None else table.label,
                  table_header=None if rows is None else rows.header)
        r.heading_path = list(SEC[sec])
        return r

    def keyed(label, keys, name_of, starts=False):
        """The rendered rows of the CTable the document printed under ``label``, keyed. Every row
        must name its own record (or start with it): a mis-keyed row grounds and attests the wrong
        thing."""
        t = ct[label][0]
        rows = G.ctable_rows(t, keys)
        bad = [k for k, row in rows.items()
               if not (row.startswith(name_of(k)) if starts else name_of(k) in row)]
        if bad:
            raise ValueError(f"{DOC} {label}: rows keyed to records they do not name: {bad}")
        return t, rows

    def head_of(rows, key):
        """For a continuation row, the row that opens its merged group (it carries the label the
        continuation row leaves empty). Used as a second reference where a continuation row reads
        exactly like another one, so that the pair locates the record."""
        order = list(rows)
        lead = next(j for j, c in enumerate(_cells(rows[key])) if c)
        if lead == 0:
            raise ValueError(f"{DOC}: {key} opens its own group and reads like another row")
        for k2 in reversed(order[:order.index(key)]):
            if _cells(rows[k2])[lead - 1]:
                return k2
        raise ValueError(f"{DOC}: no group head for {key}")

    def row_refs(sec, t, rows, key):
        """The row of ``key``, and its group head where the row occurs more than once."""
        out = [ref(sec, rows[key], t, rows)]
        if text.count(normalize(rows[key])) > 1:
            out.append(ref(sec, rows[head_of(rows, key)], t, rows))
        return out

    A, ST = [], []

    def add(subj, pred, obj, txt, refs):
        A.append(EvidenceBackedAssertion(
            assertion_id=f"{DOC}-A{len(A) + 1:03d}", subject_id=subj, predicate=pred, object_id=obj,
            assertion_text=txt, source_references=refs, metadata=meta()))

    def st(sec, txt, refs):
        if not isinstance(refs, list):
            refs = [ref(sec, refs)]
        ST.append((SEC[sec][0], ReportStatement(
            statement_id=f"{DOC}-S{len(ST) + 1:03d}", statement_text=txt, confidence="high",
            review_status="accepted", source_references=refs)))

    def sq(sec, quote, txt=None, extra=()):
        """A statement of one prose sentence: ``quote`` is the .qmd source of the sentence, ``txt``
        the statement (the sentence itself where it reads on its own). ``extra`` cites the
        neighbouring sentences a paraphrase draws on, so every clause of ``txt`` has its span."""
        st(sec, q(txt) if txt else q(quote), [ref(sec, q(x)) for x in (quote, *extra)])

    # ---- names and data the document uses ------------------------------------------------------
    steps_all, ma, fail, KEYS = ns["steps_all"], ns["ma"], ns["fail"], ns["KEYS"]
    SEL_, AUG, FA = ns["SEL"], ns["AUG"], ns["FA"]
    HM, AV, HCP, AGG, EXF = ns["HM"], ns["AV"], ns["HCP"], ns["AGG"], ns["EXF"]
    HK, VI, run23, run23_dev = ns["HK"], ns["VI"], ns["run23"], ns["run23_dev"]
    f2, f3, p3, ptxt = ns["f2"], ns["f3"], ns["p3"], ns["ptxt"]
    attr_prose, cap1, lc = ns["attr_prose"], ns["cap1"], ns["lc"]
    rep, aug_id, aug_steps = ns["rep"], ns["aug_id"], ns["aug_steps"]
    CFG = P.CFG
    lab = T._attr_label
    iac = P.csv("iac.csv")
    cqa_of = {(r.step_key, r.response): r.cqa for r in iac.itertuples()}
    basis_of = {(r.step_key, r.response): str(r.basis) for r in iac.itertuples()}
    if set(KEYS) - set(cqa_of):
        raise ValueError(f"{DOC}: outputs with no criterion row: {sorted(set(KEYS) - set(cqa_of))}")
    UO = P.UNIT_OP_TITLES

    def step_label(k):
        return f"{UO[k]} (Step {CFG.unit_op(k).step})"

    def unit_of(a):
        m = re.search(r"\(([^)]*)\)$", T.ATTR_NAME[a])
        return m.group(1) if m else ""

    def attr_name(a):
        return re.sub(r"\s*\([^)]*\)$", "", T.ATTR_NAME[a])

    def pconcept(k, p):
        return f"param:{k}_{p}"

    def pname(k, p):
        return CFG.unit_op(k).param(p).name

    def nterms(n):
        return "no term" if int(n) == 0 else f"{int(n)} term{'s' if int(n) != 1 else ''}"

    # ---- the rendered tables, from the objects the document printed ------------------------------
    ch_t, ch_df = ct["tbl-chronology"]
    ch_t, chrow = keyed("tbl-chronology", list(ch_df["Date"]), str)
    sc_t, scrow = keyed("tbl-scope", steps_all, lambda k: T.STEP_NAME[k])
    fq_keys = [(k, r) for k in steps_all for r in ma[ma.step_key == k].response]
    fq_t, fqrow = keyed("tbl-model-adequacy", fq_keys, lambda key: lab(key[1], key[0]))
    rm_keys = list(zip(fail.step_key, fail.response))
    rm_t, rmrow = keyed("tbl-remedy", rm_keys, lambda key: lab(key[1], key[0]))
    ss_t, ssrow = keyed("tbl-sample-size", list(ns["curves"]), lambda key: lab(key[1], key[0]))
    pw = ns["pw"]
    pw_t, pwrow = keyed("tbl-power", list(zip(pw.k, pw.resp, pw.t)),
                        lambda key: T._terms_text([key[2]], key[0]))
    des = {}
    for k in aug_steps:
        runs = [int(x) for x in P.csv(f"doe_{k}_aug.csv")["run"]]
        des[k] = keyed(f"tbl-aug-design-{k.replace('_', '-')}", runs, lambda r: f"{r} | ", starts=True)
    sv_t, svrow = keyed("tbl-selected", KEYS, lambda key: lab(key[1], key[0]))
    sh_keys = [(key, which) for key in AUG for which in ("planned", "all")]

    def sh_name(kw):
        f = AUG[kw[0]]["sel_p" if kw[1] == "planned" else "sel_a"]
        return T._terms_text(f["names"], kw[0][0]) if f["names"] else "None"
    sh_t, shrow = keyed("tbl-sharpen", sh_keys, sh_name)
    apc = ns["apc"]
    ac_t, acrow = keyed("tbl-aug-check", list(zip(apc.step_key, apc.response)),
                        lambda key: lab(key[1], key[0]))
    none_sel = list(ns["none_sel"])
    mr_t, mrrow = keyed("tbl-measured", none_sel, lambda key: lab(key[1], key[0]))
    im_t, imrow = keyed("tbl-impact", list(zip(ma.step_key, ma.response)),
                        lambda key: cap1(attr_prose(key[1], key[0])))
    behind = [(s, r, ds, c) for s, r, ds, c, _, _ in ns["behind_rows"]]
    cr_t, crrow = keyed("tbl-criteria-ca3", behind, lambda key: T.STEP_NAME[key[2]])
    smoved = ns["smoved"]
    se_keys = list(zip(smoved.step_key, smoved.response))
    se_t, serow = keyed("tbl-ca3-sensitivity", se_keys,
                        lambda key: f"{T.STEP_NAME[key[0]]}, {attr_prose(key[1], key[0])}")
    capa_df = ct["tbl-capa"][1]
    ca_t, carow = keyed("tbl-capa", list(capa_df["ID"]), str)

    # ==== entities ================================================================================
    inv2 = P.INV2
    sites = G._site_entities(DOC, FILE, _sid("title"))

    # the investigation itself, and the deviation of PCR-005 it cites
    q_cls = q("""QA opened INV-002 on `{python} INV2["opened"]` and classified it as `{python} INV2["classification"]`, on the grounds recorded at opening (`{python} class_basis`).""")
    q_conf = q("""The investigation confirmed the classification as `{python} INV2["classification"]`, on the grounds recorded when it was opened""")
    q_count = q("""Of the `{python} n_models` full quadratic models in scope, `{python} n_fail` did not meet the limit on overfitting, which allows predicted R² to fall short of R² by at most `{python} gap_max_s`.""")
    q_noimp = q("The investigation has no product impact.")
    q_noimp2 = q("No batch was dispositioned on these models, and the Version 1.0 documents were on hold for BLA use.")
    q_closed = q("""INV-002 was closed on `{python} INV2["closed"]`.""")
    q_capa_ca3 = q("Model selection, corrective action CA3, replaced in the reports the refits by backward elimination of corrective action CA2.")
    q_refit23 = q("""The re-analysis fitted Protein A response-surface run `{python} run23` at its design elution buffer pH, as Version 1.0 had fitted it.""")
    dev_inv = Deviation(
        deviation_id=DOC,
        summary=q("""Of the `{python} n_models` full quadratic response-surface models that carry an acceptance criterion at their step, `{python} n_fail` did not meet the limit on overfitting of PCMP-001 §7.2, which allows predicted R² to fall short of R² by at most `{python} gap_max_s`, and the model of `{python} exf_phrase` reproduced every run exactly, so none of the three tests the investigation applies could be applied to it."""),
        detected_during=str(inv2["trigger"]),
        disposition=q("""Classified `{python} INV2["classification"]` and closed on `{python} INV2["closed"]`. Under the remedy rule approved on `{python} decided`, the production bioreactor design was augmented by `{python} m_step["bioreactor"]` runs for high mannose and acidic variants and the anion exchange design by `{python} m_step["aex"]` runs for host cell protein (corrective action CA1), and the other failing models were refitted (CA2); model selection then replaced the refits for every response-surface output (CA3). The re-evaluation on all runs of CA1, the application of CA3 in the Version 2.0 reports and the preventive actions were open at closure."""),
        impact_statement="No product impact: no batch was dispositioned on these models, and the Version 1.0 "
                         "documents were on hold for BLA use.",
        no_impact_on_conclusions=False,
        source_references=[ref("summary", q_count), ref("summary", q_cls), ref("capa", q_capa_ca3),
                           ref("close", q_conf), ref("imp_other", q_noimp), ref("close", q_closed)],
        metadata=meta())
    q_run23 = q("""The Version 2.0 analysis puts Protein A response-surface run `{python} run23` at the elution buffer pH recorded under deviation `{python} run23_dev`, `{python} f"{run23_ph:g}"` instead of the design pH of `{python} f"{run23_design:g}"` (discrepancy `{python} pd_ph`).""")
    q_run23_log = q("""Every model of pool host cell protein in this section puts response-surface run `{python} run23` at the elution buffer pH recorded under deviation `{python} run23_dev`, as the Version 2.0 analysis does""")
    q_run23_note = qn("""Protein A response-surface run `{python} run23` is at the elution buffer pH recorded under deviation `{python} run23_dev`.""")
    dev_pa = Deviation(
        deviation_id=run23_dev, unit_operation=UO["protein_a"],
        summary=q("""Protein A response-surface run `{python} run23` was made at an elution buffer pH of `{python} f"{run23_ph:g}"` instead of the design pH of `{python} f"{run23_design:g}"`."""),
        disposition=q("""The run is analysed at the pH recorded under the deviation in Version 2.0 (discrepancy `{python} pd_ph` of PCR-005); the re-analysis of INV-002 fitted it at its design pH, as Version 1.0 did."""),
        impact_statement=q("""At the recorded pH the full quadratic model of pool host cell protein fails the lack-of-fit test (`{python} ptxt(fq_rec["p_lof"])`); at either pH the same `{python} n_fail` models fail the limit on overfitting, and the selected model of pool host cell protein is adequate."""),
        no_impact_on_conclusions=False,
        source_references=[ref("finding", q_run23), ref("finding", q_refit23), ref("sel_log", q_run23_log),
                           ref("sel_changed", q_run23_note, sv_t)],
        metadata=meta())

    # the steps with a designed experiment, on their rows of the scope table
    size = {k: (int(_cells(scrow[k])[1]), int(_cells(scrow[k])[2])) for k in steps_all}
    steps_ent = [S.ProcessStep(
        step_id=f"step:{k}", step_name=T.STEP_NAME[k], step_number=str(CFG.unit_op(k).step),
        unit_operation=UO[k],
        description=f"A step with a designed experiment. Its planned face-centred response-surface design has "
                    f"{size[k][0]} runs, and the full quadratic model {size[k][1]} terms, intercept "
                    f"included. Attributes with an acceptance criterion at the step: "
                    f"{lc(_cells(scrow[k])[3])}.",
        source_references=[ref("scope", scrow[k], sc_t, scrow)], metadata=meta()) for k in steps_all]

    # the criteria the document prints: in force (sensitivity table), judged on measured results
    # (measured-results table), and the platform claim of low-pH viral inactivation (prose)
    q_claim6 = q("""The criterion is the platform claim of the step, `{python} f"{claim6:g}"` log10.""")
    crit_txt = {}       # (step, response) -> (printed criterion, label, reference)
    for key, row in serow.items():
        crit_txt[key] = (_cells(row)[1], "intermediate acceptance criterion in force",
                         ref("imp_crit", row, se_t, serow))
    for key, row in mrrow.items():
        crit_txt[key] = (_cells(row)[2], "criterion in force, judged on the measured results",
                         ref("sel_none", row, mr_t, mrrow))
    vk, vr = ns["vk"], ns["vr"]
    crit_txt[(vk, vr)] = (f"≥ {ns['claim6']:g}", "platform claim of the step", ref("imp_nor", q_claim6))
    q_ds = qn("""The a priori limits start from the drug substance limits of `{python} ds_txt`.""")
    q_risk = q("""The wider criteria concern host cell protein and aggregates, which are attributes of the drug substance specification, with limits of `{python} join_and(f"{v:g} {u} {CQA_PL[c]}" for c, (v, u) in ds_by_cqa.items() if c in risk_cqas)`.""")
    q_avlo = q("""The lower limit of the criterion is `{python} f"{av_floor:g}"` %, the lower limit of the drug substance specification carried to the step unchanged.""")
    ds_ref = {"acidic_variants": [ref("imp_crit", q_ds, cr_t), ref("imp_nor", q_avlo)],
              "aggregates_hmw": [ref("imp_crit", q_risk)], "hcp": [ref("imp_crit", q_risk)]}
    ds_crit = {c: f"≤ {v:g} {u} (drug substance limit)" for c, (v, u) in ns["ds_by_cqa"].items()}
    ds_crit["acidic_variants"] = (f"{ns['av_floor']:g}–{ns['ds_by_cqa']['acidic_variants'][0]:g} "
                                  f"{ns['ds_by_cqa']['acidic_variants'][1]} (drug substance specification)")

    # the methods the document names
    elisa = ns["elisa"]
    q_elisa = q("""The precision of the host cell protein ELISA (`{python} elisa["id"]`) is a percentage of the level, `{python} f"{elisa['precision_pct']:g}"` %, so the scatter of the results grows with the level.""")
    q_cesds = q("Every run was tested for host cell protein, step yield and fragments by non-reduced CE-SDS.")
    q_cesds_note = qn("Fragments have nrCE-SDS results in the response-surface designs only.")
    methods = [
        S.AnalyticalMethod(
            method_id=elisa["id"], method_name="Host cell protein ELISA",
            method_type=G.METHOD_TYPE[elisa["id"]], analytes=["host cell protein"],
            associated_attributes=["attr:hcp"],
            source_references=[ref("sel_log", q_elisa),
                               ref("abbr", G._join_cells(["ELISA", "enzyme-linked immunosorbent assay"]))],
            metadata=meta()),
        S.AnalyticalMethod(
            method_id="nrCE-SDS", method_name="non-reduced capillary electrophoresis with sodium dodecyl sulfate",
            method_type="capillary electrophoresis", analytes=["fragments (LMW)"],
            associated_attributes=["attr:fragments_lmw"],
            source_references=[ref("des_aex", q_cesds), ref("sel_none", q_cesds_note, mr_t),
                               ref("abbr", G._join_cells(["CE-SDS", "capillary electrophoresis with sodium "
                                                                  "dodecyl sulfate"]))],
            metadata=meta()),
    ]
    method_of = {"hcp": elisa["id"], "fragments_lmw": "nrCE-SDS"}

    # the quality attributes in scope, on the rows of the scope table that list them
    reg = set(P.cqa_reg["key"])
    attr_keys = list(dict.fromkeys(cqa_of[key] for key in KEYS))
    attrs = []
    for a in attr_keys:
        outs = [key for key in KEYS if cqa_of[key] == a]
        steps_a = list(dict.fromkeys(k for k, _ in outs))
        for k, r in outs:            # the scope row names the attribute in the words of the document
            if attr_prose(r, k).lower() not in _cells(scrow[k])[3].lower():
                raise ValueError(f"{DOC}: the scope row of {k} does not name {attr_prose(r, k)}")
        crit, refs = [], [ref("scope", scrow[k], sc_t, scrow) for k in steps_a]
        for key in outs:
            if key in crit_txt:
                c, label, r_ = crit_txt[key]
                crit.append(f"{c} {unit_of(a)} ({label}, {T.STEP_NAME[key[0]]})")
                refs.append(r_)
        if a in ds_crit:
            crit.append(ds_crit[a])
            refs += ds_ref[a]
        attrs.append(S.QualityAttribute(
            attribute_id=f"attr:{a}", attribute_name=attr_name(a),
            attribute_type="CQA" if a in reg else "unclassified", unit=unit_of(a),
            acceptance_criteria=crit, analytical_method=method_of.get(a),
            associated_steps=[step_label(k) for k in steps_a], source_references=refs, metadata=meta()))

    # ---- the models: full quadratic of the planned runs (the finding) ---------------------------
    def verdict_q(r):
        return ("not testable: exact fit" if r.exact else ("adequate" if r.adequate else "not adequate"))

    tests = ns["TESTS"]
    fits_finding = []
    for i, (key, row) in enumerate(fqrow.items(), 1):
        k, resp = key
        r = ma[(ma.step_key == k) & (ma.response == resp)].iloc[0]
        ex = bool(r.exact)
        pm = "n.t." if ex else p3(r.p_model)
        pl = "n.t." if ex else f3(r.p_lof)
        fits_finding.append(StatisticalModelFit(
            model_fit_id=f"{DOC}-FQ{i:02d}", response=resp, unit_operation=UO[k],
            model_form=f"full quadratic model of the planned runs, as Version 1.0 fitted it ({int(r.k)} terms, "
                       f"intercept included)" + (f"; Protein A response-surface run {run23} at its design "
                                                 f"elution buffer pH" if k == "protein_a" else ""),
            n_runs=int(r.n), r_squared=_num(f2(r.R2)), predicted_r_squared=_num(f2(r.predR2)),
            p_value=None if ex or pm.startswith("<") else _num(pm),
            lack_of_fit_p=None if ex else _num(pl),
            adequacy_statement=f"{verdict_q(r)} against the three tests of PCMP-001 §7.2 that INV-002 applies "
                               f"({tests}): model F-test p {pm}, lack-of-fit p {pl}, R² minus predicted R² "
                               f"{f2(r.gap)}.",
            source_references=[ref("finding", row, fq_t, fqrow)], metadata=meta()))
    fq_rec = ns["fq_rec"]
    q_fqrec = q("""With run `{python} run23` at its recorded pH, the full quadratic model of pool host cell protein fails the lack-of-fit test (`{python} ptxt(fq_rec["p_lof"])`), while it meets the model F-test and the limit on overfitting.""")
    fits_finding.append(StatisticalModelFit(
        model_fit_id=f"{DOC}-FQ{len(fits_finding) + 1:02d}", response=HK[1], unit_operation=UO[HK[0]],
        model_form=f"full quadratic model of the planned runs, with Protein A response-surface run {run23} at "
                   f"the elution buffer pH recorded under deviation {run23_dev}",
        lack_of_fit_p=_num(f3(fq_rec["p_lof"])),
        adequacy_statement="not adequate: fails the lack-of-fit test, while it meets the model F-test and the "
                           "limit on overfitting",
        source_references=[ref("finding", q_fqrec)], metadata=meta()))

    # ---- the models: selected under CA3, every output (Table 9) ---------------------------------
    scale_of = ns["scale_of"]

    def verdict_s(f):
        return ("not testable: exact fit" if f.get("exact") else
                ("adequate" if f["status"] == "selected" else "not adequate"))

    fits_sel = []
    for i, (key, row) in enumerate(svrow.items(), 1):
        k, resp = key
        f = SEL_[key]
        ex = bool(f.get("exact"))
        pm = "n.t." if ex else ("–" if not f["names"] else p3(f["p"]))
        pl = "n.t." if ex else f3(f["p_lof"])
        fits_sel.append(StatisticalModelFit(
            model_fit_id=f"{DOC}-SM{i:02d}", response=resp, unit_operation=UO[k],
            model_form=("model selected under corrective action CA3 (lowest AICc over the hierarchical submodels "
                        "of the full quadratic, block term kept), on every run in which the output was measured; "
                        + ("no scale chosen (exact fit)" if ex else f"{scale_of(f)} scale")
                        + ", " + nterms(len(f["names"])) + " besides the intercept and the block term"),
            n_runs=int(f["n"]), r_squared=_num(f2(f["R2"])), predicted_r_squared=_num(f2(f["predR2"])),
            p_value=None if pm in ("n.t.", "–") or pm.startswith("<") else _num(pm),
            lack_of_fit_p=None if ex else _num(pl),
            adequacy_statement=f"{verdict_s(f)} against the three tests of PCMP-001 §7.2 that INV-002 applies: "
                               f"model F-test p {pm}, lack-of-fit p {pl}, R² minus predicted R² {f2(f['gap'])}.",
            source_references=[ref("sel_changed", row, sv_t, svrow)], metadata=meta()))

    # ---- the models: the augmented outputs, planned and all runs (Table 10), and the planned model
    # with a block term on all runs that each augmentation was sized for (prose) ------------------
    def term_of(t, k):
        base = t[:-2] if t.endswith("^2") else t
        return ModelTerm(term=T._term_name(t, k), factor=None if ":" in t else pname(k, base))

    fits_aug = []
    for i, ((key, which), row) in enumerate(shrow.items(), 1):
        k, resp = key
        f = AUG[key]["sel_p" if which == "planned" else "sel_a"]
        fits_aug.append(StatisticalModelFit(
            model_fit_id=f"{DOC}-AU{i:02d}", response=resp, unit_operation=UO[k],
            model_form=("model selected under corrective action CA3 on "
                        + ("the planned runs" if which == "planned" else "all runs, the augmentation as a second block")
                        + f", {scale_of(f)} scale"),
            n_runs=int(f["n"]), r_squared=_num(f2(f["R2"])), predicted_r_squared=_num(f2(f["predR2"])),
            lack_of_fit_p=_num(f3(f["p_lof"])),
            adequacy_statement=f"meets the three tests on {'the planned runs' if which == 'planned' else 'all runs'}: "
                               f"model F-test p < 0.001, lack-of-fit p {f3(f['p_lof'])}, R² minus predicted R² "
                               f"{f2(f['gap'])}.",
            terms=[term_of(t, k) for t in f["names"]],
            source_references=[ref("sel_aug", row, sh_t, shrow)], metadata=meta()))
    q_fa = q("""On all runs it meets both for acidic variants and for host cell protein at anion exchange, with R² minus predicted R² of `{python} f2(FA[AV]["gap"])` and `{python} f2(FA[HCP]["gap"])`.""")
    q_fa_hm = q("""For high mannose it does not, because R² minus predicted R² is `{python} f2(FA[HM]["gap"])` against the limit of `{python} gap_max_s`.""")
    q_fa_hm2 = q("""Its lack-of-fit test is passed (`{python} ptxt(FA[HM]["p_lof"])`).""")
    for key in (AV, HCP, HM):
        f = FA[key]
        ok = key != HM
        fits_aug.append(StatisticalModelFit(
            model_fit_id=f"{DOC}-AU{len(fits_aug) + 1:02d}", response=key[1], unit_operation=UO[key[0]],
            model_form="full quadratic model with a block term on all runs, the planned model the augmentation "
                       "was sized for",
            lack_of_fit_p=None if ok else _num(f3(f["p_lof"])),
            adequacy_statement=(f"meets the lack-of-fit test and the limit on overfitting on all runs (R² minus "
                                f"predicted R² {f2(f['gap'])})" if ok else
                                f"meets the lack-of-fit test and not the limit on overfitting on all runs (R² minus "
                                f"predicted R² {f2(f['gap'])} against {ns['gap_max_s']})"),
            source_references=[ref("sel_aug", q_fa)] if ok else [ref("sel_aug", q_fa_hm), ref("sel_aug", q_fa_hm2)],
            metadata=meta()))

    # ---- documents, non-claims, the viral clearance ledger ---------------------------------------
    q_opened = q("""QA opened INV-002 on `{python} INV2["opened"]`, while INV-001 was still open.""")
    q_notreopen = q("INV-001, the investigation into acceptance criteria set after the data were seen, is not reopened.")
    q_rule_inv1 = q("The investigation into acceptance criteria set after the data were seen (INV-001) set that rule, and this investigation does not change it.")
    q_four = q("The process characterization master plan sets four model-adequacy criteria for a response-surface model (PCMP-001 §7.2)")
    q_noaug = q("The master plan names no augmentation.")
    q_pcmp_same = q("The master plan is not changed for model selection, which each report records as a discrepancy from its plan.")
    q_pcmr = q("This investigation requires the process characterization master report (PCMR-001) Version 2.0 to consolidate the conclusions of the step reports as they stand after the remedies and the model selection.")
    q_infl = q("""The Protein A report (PCR-005) Version 2.0, for example, is to record its analysis of influential runs as discrepancy `{python} pd_infl`.""")
    q_pcr6 = q("""On it the step claim is not met over the NOR as characterized, and the low-pH viral inactivation report (`{python} rep[vk]`) moves the NOR""")
    q_pcr3 = q("""The production bioreactor report (`{python} rep[bk]`) states how this result is handled.""")
    q_reeval = q("""The production bioreactor report (`{python} rep["bioreactor"]`) therefore re-evaluates every model of the step on all runs, including the `{python} n_bio_pass` models that met the three tests of the model-adequacy criteria""")
    rels = [
        DocumentRelationship(
            relationship_id=f"{DOC}-R01", kind="references", source_document_id=DOC, target_document_ref="INV-001",
            statement=q("""INV-002 was opened on `{python} INV2["opened"]`, while INV-001 was open. INV-001 set the rule that derives the intermediate acceptance criteria, which INV-002 does not change; INV-001 is not reopened, and the criteria fixed at its closure on `{python} INV["closed"]` rest on the models selected under INV-002 corrective action CA3."""),
            source_references=[ref("event", q_opened), ref("scope", q_rule_inv1), ref("imp_other", q_notreopen)],
            metadata=meta()),
        DocumentRelationship(
            relationship_id=f"{DOC}-R02", kind="references", source_document_id=DOC, target_document_ref="PCMP-001",
            statement="INV-002 applies the first three of the four model-adequacy criteria of PCMP-001 §7.2 as tests. "
                      "The master plan names no augmentation, and it is not changed for model selection, which "
                      "each report records as a discrepancy from its plan.",
            source_references=[ref("finding", q_four), ref("rule", q_noaug), ref("imp_other", q_pcmp_same)],
            metadata=meta()),
    ]
    extra = {"bioreactor": [ref("des_bio", q_reeval), ref("imp_nor", q_pcr3)],
             "protein_a": [ref("finding", q_infl)], "viral_inactivation": [ref("rule", q_pcr6)]}
    extra_txt = {
        "bioreactor": " It re-evaluates every model of the step on all runs, and it states how the result for "
                      "acidic variants at the least favourable combination of the NOR is handled.",
        "protein_a": f" It is to record its analysis of influential runs as discrepancy {ns['pd_infl']}.",
        "viral_inactivation": " It moves the NOR of low-pH viral inactivation, because the XMuLV step claim is "
                              "not met over the NOR as characterized.",
    }
    for k in steps_all:
        head = next(key for key in imrow if key[0] == k)
        aug_txt = (f" and the augmentation as {ns['pd_id'][k]}" if k in ns["pd_id"] else "")
        rels.append(DocumentRelationship(
            relationship_id=f"{DOC}-R{len(rels) + 1:02d}", kind="references", source_document_id=DOC,
            target_document_ref=rep[k],
            statement=f"{rep[k]} Version 2.0, the report of the {ns['step_prose'](k)} step, uses the model "
                      f"selected under corrective action CA3 for each output with a criterion, and records the "
                      f"model selection as discrepancy {ns['sel_pd'][k]} from its plan{aug_txt}." + extra_txt.get(k, ""),
            source_references=[ref("impact", imrow[head], im_t, imrow)] + extra.get(k, []), metadata=meta()))
    rels.append(DocumentRelationship(
        relationship_id=f"{DOC}-R{len(rels) + 1:02d}", kind="references", source_document_id=DOC,
        target_document_ref="PCMR-001",
        statement="INV-002 requires PCMR-001 Version 2.0 to consolidate the conclusions of the step reports as "
                  "they stand after the remedies and the model selection.",
        source_references=[ref("imp_other", q_pcmr)], metadata=meta()))

    def nc(subject, statement, quotes, rationale=None, elsewhere=None, uo=None):
        """An explicit non-claim on the sentences ``quotes`` ((section, quote) pairs). Its id is set
        once every non-claim exists, in the order of the document."""
        return ExplicitNonClaim(
            non_claim_id=f"{DOC}-NC", subject=subject, unit_operation=uo, statement=statement,
            rationale=rationale, handled_elsewhere=elsewhere,
            source_references=[ref(s_, x) for s_, x in quotes], metadata=meta())
    q_immediate = q("As an immediate action, no proven acceptable range, design space or judgement across the normal operating range (NOR) was set from a model that failed one of the three tests of the model-adequacy criteria while the investigation was open.")
    q_norange = q("No range was set from a failing model at Version 2.0.")
    q_noruns = q("No runs were made for them, because viral clearance is not tested on the drug substance.")
    q_nospike = q("No virus was spiked, so XMuLV and MVM clearance were not measured, and their models keep the planned runs alone.")
    q_nodev = q("No procedure and no GMP requirement was departed from, so neither is recorded as a deviation.")
    q_noamend = q("The process characterization master plan (PCMP-001) and the step plans are not amended.")
    q_fourth = q("The fourth criterion is judged by each step report for its own models.")
    q_noneset = q("None of these outputs sets a range.")
    ncs_scope = [
        nc("screening models", "The screening models are outside the scope of the investigation.",
           [("scope", "The screening models. They identify effects and set no range (PCMP-001 §6.2).")],
           rationale="They identify effects and set no range (PCMP-001 §6.2)."),
        nc("the rule that derives the intermediate acceptance criteria",
           "The rule that derives the intermediate acceptance criteria is outside the scope, and the "
           "investigation does not change it.", [("scope", q_rule_inv1)],
           elsewhere="INV-001, which set the rule; §9.1 of INV-002 reports how model selection entered the "
                     "verification behind the criteria"),
        nc("responses with no criterion at their step",
           "Responses with no criterion at their step, such as step yield, are outside the scope; no conclusion "
           "depends on them.",
           [("scope", "Responses with no criterion at their step, such as step yield. The reports select their "
                      "models in the same way, and no conclusion depends on them.")]),
        nc("univariate studies and the steps without a designed experiment",
           "The univariate studies and the two steps without a designed experiment, harvest and UF/DF, are "
           "outside the scope.",
           [("scope", "The univariate studies, and the two steps without a designed experiment (harvest and UF/DF).")]),
        nc("measured results of the augmentation runs",
           "The measured results of the augmentation runs and the ranges that follow from them are not given in "
           "the investigation.",
           [("scope", "The measured results of the augmentation runs and the ranges that follow from them. The "
                      "reports of the augmented steps give them.")],
           elsewhere=f"the reports of the augmented steps, {rep['bioreactor']} and {rep['aex']}"),
    ]
    ncs_other = {
        "finding": [nc("the fourth model-adequacy criterion (residual patterns, influential runs)",
                       "The investigation applies the first three criteria of PCMP-001 §7.2 as tests and states no "
                       "result for the fourth.", [("finding", q_fourth)],
                       elsewhere=f"each step report, for its own models (the Protein A report records its analysis "
                                 f"of influential runs as {ns['pd_infl']})")],
        "rule": [nc("augmentation runs for the viral clearance models",
                    "No augmentation runs were made for the viral clearance models, and no virus was spiked.",
                    [("rule", q_noruns), ("des_aex", q_nospike)],
                    rationale="Viral clearance is not tested on the drug substance; it is a process requirement, "
                              "demonstrated by spiking studies at worst-case conditions against a cumulative claim."),
                 nc("augmentation in the master plan",
                    "The master plan names no augmentation; augmentation is the rule of this investigation.",
                    [("rule", q_noaug)])],
        "impact": [nc("deviation", "Neither the augmentation nor the model selection is recorded as a "
                       "deviation.", [("impact", q_nodev)],
                      rationale="No procedure and no GMP requirement was departed from.",
                      elsewhere="the discrepancies from the plan that each report records"),
                   nc("amendment of PCMP-001 and the step plans",
                      "PCMP-001 and the step plans are not amended.", [("impact", q_noamend)])],
        "imp_other": [nc("product impact", "The investigation has no product impact.",
                         [("imp_other", q_noimp), ("imp_other", q_noimp2)],
                         rationale="No batch was dispositioned on these models, and the Version 1.0 documents were "
                                   "on hold for BLA use.")],
        "sel_proc": [nc("absence of an effect",
                        "A selected model with no term shows that no effect of the parameters was detected within the "
                        "range studied, not that there is none.",
                        [("sel_proc", "It says that no effect of the parameters was detected within the range "
                                      "studied. It does not show that there is none.")])],
        "ss_power": [nc("absence of an effect from a non-significant term",
                        "A non-significant interaction or curvature term in a re-evaluated model is not evidence that "
                        "the effect is absent.", [("ss_power", "It is not evidence that the effect is absent.")],
                        rationale=q("""Of the `{python} n_terms_pw` significant effects of the refits, `{python} n_pw_hi` have a power of at least `{python} target_s` at the size of the augmentation that was run, and the weakest a power of `{python} f2(weak_p)`."""))],
        "sel_aug": [nc("a change between the planned and the augmentation campaigns",
                       "The block term gives no evidence of a constant shift between the planned and the augmentation "
                       "runs, which is not evidence that nothing changed; a change in the aggregate effects between "
                       "the campaigns cannot be excluded.",
                       [("sel_aug", "That is not evidence that nothing changed between the two campaigns."),
                        ("sel_aug", q("""With only `{python} CC[AGG]["n"]` pairs the comparison has little power, so a change in the aggregate effects between the campaigns cannot be excluded."""))])],
        "sel_log": [nc("equal variance of the residuals",
                       "A test can fail to reject the assumption of equal variance but cannot show that it holds.",
                       [("sel_log", "A test can fail to reject the assumption of equal variance, but it cannot show "
                                    "that the assumption holds.")])],
        "ss_method": [nc("sizing for an effect the planned runs did not detect",
                         "The sample-size calculation does not size a design to find an effect that the planned runs "
                         "did not detect.",
                         [("ss_method", "An effect that the planned runs did not detect is not in the true model, so "
                                        "the calculation does not size a design to find it.")])],
        "close": [nc("ranges from failing models",
                     "No range was set from a model that failed one of the three tests, while the investigation was "
                     "open or at Version 2.0.", [("close", q_norange), ("event", q_immediate)])],
        "sel_none": [nc("ranges from outputs with no adequate model",
                        "None of the outputs with no adequate model sets a range.", [("sel_none", q_noneset)])],
    }
    vcum = ns["vcum"]
    q_vsum = q("""The claims of the three viral clearance steps add up to `{python} f"{vcum.claimed_sum:g}"` log10, against a cumulative requirement of `{python} f"{vcum.required:g}"` log10.""")
    contribution = ModularContribution(
        contribution_id=f"{DOC}-VC01", quantity="Viral clearance — XMuLV", unit_operation=UO[vk],
        step_value=f"{ns['claim6']:g}", cumulative_value=f"{vcum.claimed_sum:g}", requirement=f"{vcum.required:g}",
        unit="log10", source_references=[ref("imp_nor", q("""the platform claim of the step, `{python} f"{claim6:g}"` log10""")),
                                         ref("imp_nor", q_vsum)], metadata=meta())

    entities = [
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("title"), sites=sites),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("summary"), deviations=[dev_inv]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("event"), document_relationships=rels[:1]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("scope"), process_steps=steps_ent,
                                  quality_attributes=attrs, non_claims=ncs_scope),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("finding"), deviations=[dev_pa],
                                  model_fits=fits_finding, document_relationships=rels[1:2],
                                  non_claims=ncs_other["finding"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("rule"), non_claims=ncs_other["rule"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("ss_method"), non_claims=ncs_other["ss_method"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("ss_power"), non_claims=ncs_other["ss_power"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("des_aex"), analytical_methods=methods),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("sel_proc"), non_claims=ncs_other["sel_proc"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("sel_log"), non_claims=ncs_other["sel_log"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("sel_changed"), model_fits=fits_sel),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("sel_aug"), model_fits=fits_aug,
                                  non_claims=ncs_other["sel_aug"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("sel_none"), non_claims=ncs_other["sel_none"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("impact"), document_relationships=rels[2:-1],
                                  non_claims=ncs_other["impact"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("imp_nor"), contributions=[contribution]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("imp_other"), document_relationships=rels[-1:],
                                  non_claims=ncs_other["imp_other"]),
        S.SectionEntityExtraction(document_id=DOC, section_id=_sid("close"), non_claims=ncs_other["close"]),
    ]

    n_nc = 0                              # number the non-claims in the order of the document
    for e in entities:
        for nc_ in e.non_claims:
            n_nc += 1
            nc_.non_claim_id = f"{DOC}-NC{n_nc:02d}"

    # ==== studies: the planned response-surface designs and the two augmentations =================
    chron = ns["chron"]
    n_cp = int(ns["n_cp"])
    rsm_last_end, rsm_last_id = ns["rsm_last_end"], ns["rsm_last_id"]
    studies = []
    for k in steps_all:
        s_id = chron[(chron.kind == "rsm") & (chron.step == k)].index[0]
        if (P.doe_runs(k, "rsm"), P.doe_centre_points(k, "rsm")) != (size[k][0], n_cp):
            raise ValueError(f"{DOC}: the scope row of {k} disagrees with the seeded design")
        refs = [ref("scope", scrow[k], sc_t, scrow)]
        if s_id == rsm_last_id:
            refs.append(ref("event", chrow[rsm_last_end], ch_t, chrow))
        studies.append(S.StudyDesign(
            study_id=f"study:{s_id}", study_type="response_surface_doe",
            design_name="face-centred design approved in the plan of the step (the planned runs)",
            unit_operation=UO[k], responses=list(ma[ma.step_key == k].response), n_runs=size[k][0],
            n_center_points=n_cp, source_references=refs, metadata=meta()))
    aug_start, aug_end, m_step = ns["aug_start"], ns["aug_end"], ns["m_step"]
    meas = {"bioreactor": list(ns["bio_meas"]), "aex": list(ns["aex_meas"])}
    made = {k: q(f"""They were made in study `{{python}} aug_id["{k}"]`, from `{{python}} aug_start["{k}"]` to `{{python}} aug_end["{k}"]`.""")
            for k in aug_steps}
    start_row = {k: next(d for d in chrow if d == aug_start[k] and aug_id[k] in chrow[d]) for k in aug_steps}
    end_row = {k: next(d for d in chrow if d == aug_end[k] and aug_id[k] in chrow[d]) for k in aug_steps}
    for k in aug_steps:
        t, rows = des[k]
        factors = [c[len("coded_"):] for c in P.csv(f"doe_{k}_aug.csv").columns if c.startswith("coded_")]
        note = t.notes[0][1]
        if not note.startswith("Factors: "):
            raise ValueError(f"{DOC}: the factor note of {t.label} moved")
        sec = "des_bio" if k == "bioreactor" else "des_aex"
        studies.append(S.StudyDesign(
            study_id=f"study:{aug_id[k]}", study_type="response_surface_doe",
            design_name=f"D-optimal augmentation of {m_step[k]} runs, executed as a second block of the face-centred "
                        f"response-surface design",
            unit_operation=UO[k], factors=[pname(k, x) for x in factors], responses=meas[k],
            associated_parameters=[pconcept(k, x) for x in factors],
            source_references=[ref("event", chrow[start_row[k]], ch_t, chrow),
                               ref("event", chrow[end_row[k]], ch_t, chrow), ref(sec, made[k]),
                               ref(sec, note, t)] + [ref(sec, row, t, rows) for row in rows.values()],
            metadata=meta()))

    # ==== assertions ==============================================================================
    for key, row in fqrow.items():
        k, resp = key
        a = cqa_of[key]
        add(f"step:{k}", "step_has_quality_attribute", f"attr:{a}",
            f"{UO[k]} has an acceptance criterion for {attr_prose(resp, k)} and a response-surface model of it "
            f"in the scope of INV-002.", [ref("finding", row, fq_t, fqrow)])
    for key, (c, label, r_) in crit_txt.items():
        k, resp = key
        a = cqa_of[key]
        b = basis_of[key]
        add(f"attr:{a}", "attribute_has_acceptance_criterion", f"lit:{k}_{a}_iac",
            f"{cap1(ns['at_step'](k))} the output for {attr_prose(resp, k)} is judged against {c} {unit_of(a)} "
            f"({label}; basis: {b}).", [r_])
    # parameter effects, each on the row or the clause that states it
    for key in AUG:                       # the selected models of all runs that the reports use
        k, resp = key
        names = AUG[key]["sel_a"]["names"]
        mains = [t for t in names if ":" not in t and not t.endswith("^2")]
        row = shrow[(key, "all")]
        for p in mains:
            refs = [ref("sel_aug", row, sh_t, shrow)]
            if key == AV and p == "pH":
                refs.append(ref("imp_nor", q("""In the selected model acidic variants fall as `{python} pname(bk, "pH")` rises""")))
            if key == HCP:
                refs.append(ref("sel_aug", q("""It has the main effects of `{python} hcp_terms`, on the log scale.""")))
            add(pconcept(k, p), "parameter_impacts_attribute", f"attr:{cqa_of[key]}",
                f"{pname(k, p)} is a term of the model of {attr_prose(resp, k)} {ns['at_step'](k)} selected on all "
                f"runs, the model the report uses.", refs)
    fh = ns["fh"]
    for p in ns["mains_h"]:              # pool host cell protein, Protein A, log scale
        add(pconcept(HK[0], p), "parameter_impacts_attribute", "attr:hcp",
            f"Across the range studied, the selected model multiplies pool host cell protein by a factor of "
            f"{ns['fold_h'][p]:.2f} from the low to the high end of {lc(pname(HK[0], p))}.",
            [ref("sel_log", f"{ns['fold_h'][p]:.2f} for {ns['pname'](HK[0], p)}")])
    add(pconcept(HK[0], ns["FL"]), "parameter_impacts_attribute", "attr:hcp",
        f"{pname(HK[0], ns['FL'])} has a squared term in the selected model of pool host cell protein: from the low "
        f"end to the centre of its range the factor is {f2(ns['fl_lo'])}, and from the centre to the high end "
        f"{f2(ns['fl_hi'])}.",
        [ref("sel_log", q("""`{python} cap1(pname(HK[0], FL))` also has a squared term, so its factor depends on where along the range the change is made.""")),
         ref("sel_log", q("""From `{python} f"{pl_fl.prange[0]:g}"` to `{python} f"{fl_mid:g}"` `{python} pl_fl.unit` pool host cell protein changes by a factor of `{python} f2(fl_lo)`, and from `{python} f"{fl_mid:g}"` to `{python} f"{pl_fl.prange[1]:g}"` `{python} pl_fl.unit` by a factor of `{python} f2(fl_hi)`."""))])
    fva = ns["fva"]                      # aggregate at low-pH viral inactivation
    q_va_terms = q("""terms in `{python} fva_terms` only""")
    q_va_none = q("""none in `{python} pname(VI, "ph")`""")
    for p in fva["names"]:
        add(pconcept(VI, p), "parameter_impacts_attribute", "attr:aggregates_hmw",
            f"The selected model of aggregate at low-pH viral inactivation has a term in {lc(pname(VI, p))}.",
            [ref("sel_verif", q_va_terms)])
    add(pconcept(VI, "ph"), "parameter_does_not_significantly_impact_attribute", "attr:aggregates_hmw",
        "The selected model of aggregate at low-pH viral inactivation has no term in inactivation pH.",
        [ref("sel_verif", q_va_none)])
    q_x6 = q("""The selected model has the main effects of `{python} fit6_terms` only.""")
    for p in ns["fit6"]["names"]:        # XMuLV clearance at low-pH viral inactivation
        add(pconcept(vk, p), "parameter_impacts_attribute", "attr:lrv_xmulv",
            f"{pname(vk, p)} is a main effect of the selected model of XMuLV clearance at low-pH viral inactivation.",
            [ref("imp_nor", q_x6)])
    q_moves = q("""moves the NOR of `{python} moved6_txt`""")
    for p in ns["moved6"]:
        add(f"step:{vk}", "step_has_parameter", pconcept(vk, p),
            f"{UO[vk]} has process parameter {pname(vk, p)}, whose NOR the low-pH viral inactivation report "
            f"({rep[vk]}) moves.", [ref("imp_nor", q_moves)])
    add("attr:hcp", "attribute_measured_by_method", f"method:{elisa['id']}",
        f"Host cell protein is measured by ELISA ({elisa['id']}), whose precision is "
        f"{elisa['precision_pct']:g} % of the level.", [ref("sel_log", q_elisa)])
    add("attr:fragments_lmw", "attribute_measured_by_method", "method:nrCE-SDS",
        "Fragments are measured by non-reduced CE-SDS, in the response-surface designs and in the anion exchange "
        "augmentation runs.", [ref("des_aex", q_cesds), ref("sel_none", q_cesds_note, mr_t)])

    # ==== report statements =======================================================================
    # -- Summary
    sq("summary", "The Version 2.0 re-analysis of the A-Mab characterization campaign tested every response-surface model that carries an acceptance criterion at its step against the model-adequacy criteria of the process characterization master plan (PCMP-001 §7.2).")
    st("summary", q("""Of the `{python} n_models` full quadratic models in scope, `{python} n_fail` did not meet the limit on overfitting, which allows predicted R² to fall short of R² by at most `{python} gap_max_s`."""), [ref("summary", q_count)])
    sq("summary", """Besides these `{python} n_fail` models, the full quadratic model of `{python} exf_phrase` reproduced every run exactly, so none of the tests could be applied to it.""")
    sq("summary", """At the pH recorded for Protein A run `{python} run23`, the full quadratic model of pool host cell protein failed the lack-of-fit test.""")
    st("summary", q("""QA opened INV-002 on `{python} INV2["opened"]` and classified it as `{python} INV2["classification"]`, on the grounds recorded at opening: `{python} class_basis`."""), [ref("summary", q_cls)])
    sq("summary", "The root cause is that the plans prescribed the full quadratic model as the predictive model of each design, with no model selection.")
    sq("summary", "The Version 1.0 plans also set no numeric limit on how far predicted R² may fall below R², against which the size of a design could have been checked.")
    sq("summary", """A rule for the remedy of each failing model was approved on `{python} decided`, before any new run was made""")
    sq("summary", """The remedy rule gives `{python} n_aug_m` models an augmentation, in `{python} n_aug_steps` steps.""")
    sq("summary", """The production bioreactor design was augmented by `{python} m_step["bioreactor"]` runs for high mannose and acidic variants, in study `{python} aug_id["bioreactor"]`.""")
    sq("summary", """The anion exchange design was augmented by `{python} m_step["aex"]` runs for host cell protein, in study `{python} aug_id["aex"]`.""")
    sq("summary", """Each augmentation is the smallest D-optimal set of runs that gives a probability of success of at least `{python} target_s`.""")
    sq("summary", """On all runs that model meets both tests for `{python} join_and(attr_prose(r, k) for k, r in (AV, HCP))`, and it does not meet the limit on overfitting for `{python} attr_prose(HM[1], HM[0])`""",
       """On all runs the full quadratic model with a block term meets the lack-of-fit test and the limit on overfitting for `{python} join_and(attr_prose(r, k) for k, r in (AV, HCP))`, and it does not meet the limit on overfitting for `{python} attr_prose(HM[1], HM[0])`.""")
    sq("summary", """The other `{python} n_ref` failing models were refitted.""")
    sq("summary", """Model selection was adopted on `{python} sel_date` as corrective action CA3, for every response-surface output""",
       """Model selection was adopted on `{python} sel_date` as corrective action CA3, for every response-surface output.""")
    sq("summary", "Each output is modelled on the log or the raw scale, as its Box-Cox profile decides, by the submodel of the full quadratic with the lowest AICc, and that model is judged against the three tests.")
    sq("summary", "Once selected, the three models that the augmentations were made for meet the three tests on the planned runs alone, so the augmentations were not needed to pass them.")
    sq("summary", "The augmentation runs removed from two models of the production bioreactor, those of high mannose and aggregates, terms that the planned runs had suggested.")
    sq("summary", """Their models selected on the planned runs had predicted only `{python} int(hm_c.inside_pi)` and `{python} int(agg_c.inside_pi)` of the `{python} int(hm_c.n_new)` new runs within the 95 % prediction interval, fewer than a one-sided binomial test at the `{python} f"{eff_alpha:g}"` level allows.""",
       """The models of high mannose and aggregates selected on the planned runs had predicted only `{python} int(hm_c.inside_pi)` and `{python} int(agg_c.inside_pi)` of the `{python} int(hm_c.n_new)` new runs within the 95 % prediction interval, fewer than a one-sided binomial test at the `{python} f"{eff_alpha:g}"` level allows.""")
    sq("summary", "A check of a selected model against the three tests is optimistic, because the selection used the same runs.")
    sq("summary", """After selection, `{python} n_none_sel` outputs have no adequate model (`{python} none_sel_phrase`), and they are judged on their measured results.""")
    sq("summary", """Model selection was adopted before the investigation into acceptance criteria set after the data were seen (INV-001) closed on `{python} INV["closed"]`, so the intermediate acceptance criteria fixed at that closure rest on the selected models.""")
    sq("summary", """The verification of the platform worst cases widened `{python} n_w_in` of these criteria, for `{python} w_in_txt`, by replacing a platform worst case with the one-sided `{python} vb_pct` % prediction bound of a single A-Mab batch.""")
    sq("summary", """The criterion for `{python} w_in_tt_txt` was also tightened by another downstream step, and it is narrower than its a priori value.""")
    sq("summary", """Against the criteria that the same verification gives on the full quadratic models, model selection made `{python} n_wider` criteria wider, by `{python} pct_txt`, and kept the upper limit of acidic variants at the production bioreactor at its a priori value, which the full quadratic models would have widened""",
       """Against the criteria that the verification gives on the full quadratic models, model selection made `{python} n_wider` criteria wider, by `{python} pct_txt`, and kept the upper limit of acidic variants at the production bioreactor at its a priori value, which the full quadratic models would have widened.""")
    sq("summary", "Against the criteria without model selection, however, the scale-down model would not be qualified for host cell protein in the Protein A pool and at cation exchange.")
    sq("summary", "One is the lower prediction limit of acidic variants at the production bioreactor at the least favourable combination of the NOR",
       "This report gives the lower prediction limit of acidic variants at the production bioreactor at the least favourable combination of the NOR, from the model of all runs.")
    sq("summary", "The reports of the two augmented steps give the measured results of the new runs, the re-evaluation of every model and the ranges.")

    # -- Event description
    sq("event", """INV-001, the investigation into acceptance criteria set after the data were seen, was opened on `{python} INV["opened"]`.""")
    sq("event", "It followed the QA review of the process characterization master report (PCMR-001) Version 1.0 for BLA readiness, which found that the acceptance criteria of the proven acceptable range analysis had been set after the data were seen.",
       "INV-001 followed the QA review of the process characterization master report (PCMR-001) Version 1.0 for BLA readiness, which found that the acceptance criteria of the proven acceptable range analysis had been set after the data were seen.")
    sq("event", "Version 2.0 of the process characterization master plan (PCMP-001) also states campaign thresholds for model adequacy (PCMP-001 §7.2).")
    sq("event", "Version 1.0 of the master plan accepted a response-surface model when its terms were significant, its lack of fit was not significant against pure error and its predicted R² was consistent with its adjusted R².")
    sq("event", "Version 1.0 of the master plan left the numeric thresholds to the individual study.")
    sq("event", "The Version 1.0 reports fitted the full quadratic model to every response-surface design and applied the lack-of-fit test.")
    sq("event", """The re-analysis found `{python} n_fail` of the `{python} n_models` full quadratic models above the limit on overfitting.""")
    st("event", q("""QA opened INV-002 on `{python} INV2["opened"]`, while INV-001 was still open, and the recorded trigger is the re-analysis itself."""),
       [ref("event", q_opened), ref("event", q("The recorded trigger is the re-analysis itself."))])
    st("event", "As an immediate action, no proven acceptable range, design space or judgement across the NOR was set from a model that failed one of the three tests while the investigation was open.", [ref("event", q_immediate)])
    sq("event", "The Version 1.0 documents, whose ranges came from the full quadratic models, were already on hold for BLA use under INV-001.")
    sq("event", """The remedy rule, which assigns a remedy to each failing model, was approved within this investigation on `{python} decided`, together with the sample sizes and the augmentation designs.""")
    sq("event", """The first augmentation run started on `{python} first_start`.""")
    sq("event", """The root cause was recorded on `{python} sel_date`, and model selection was adopted on the same date as corrective action CA3.""")
    for d, row in chrow.items():
        c = _cells(row)
        st("event", f"{c[0]}: {c[1]}.", [ref("event", row, ch_t, chrow)])

    # -- Scope
    sq("scope", """These are `{python} n_models` models in the `{python} n_steps` steps with a designed experiment""",
       """The investigation covers every response-surface model that carries an acceptance criterion at its step: `{python} n_models` models in the `{python} n_steps` steps with a designed experiment.""",
       ["The investigation covers every response-surface model that carries an acceptance criterion at its step."])
    sq("scope", """The finding is that `{python} n_fail` of the full quadratic models, fitted to the runs of the planned face-centred design as the process characterization master plan prescribes (PCMP-001 §6.2), exceed the limit of `{python} gap_max_s` on R² minus predicted R².""")
    for k, row in scrow.items():
        c = _cells(row)
        failing = _nofoot(c[4])
        ex_note = (f" (the model of {attr_prose(EXF[1], EXF[0])} fits exactly, so no test can be applied)"
                   if k == EXF[0] else "")
        st("scope", f"{c[0]}: the planned face-centred design has {c[1]} runs and the full quadratic model {c[2]} "
                    f"terms, intercept included; attributes with a criterion: {lc(c[3])}; full quadratic model "
                    f"not adequate: {lc(failing)}{ex_note}.", [ref("scope", row, sc_t, scrow)])
    sq("scope", "A conclusion over the NOR is the judgement whether an output meets its criterion at every combination of NOR low, set-point and NOR high of the response-surface factors.")
    sq("scope", "The NOR as characterized is the NOR against which the studies were planned and run.")
    sq("scope", "The NOR in force is the NOR that a Version 2.0 report sets, where it moved one.")
    sq("scope", """The single-batch bound is the one-sided `{python} vb_pct` % prediction bound of a single batch.""")

    # -- Finding
    sq("finding", "The model F-test is significant at α = `{python} eff_a_s`.",
       """Criterion 1 of PCMP-001 §7.2: the model F-test is significant at α = `{python} eff_a_s`.""")
    sq("finding", "Lack of fit is not significant against pure error at α = `{python} lof_a_s`.",
       """Criterion 2 of PCMP-001 §7.2: lack of fit is not significant against pure error at α = `{python} lof_a_s`.""")
    sq("finding", "Predicted R² falls short of R² by at most `{python} gap_max_s`. This is the limit on overfitting.",
       """Criterion 3 of PCMP-001 §7.2, the limit on overfitting: predicted R² falls short of R² by at most `{python} gap_max_s`.""")
    sq("finding", "The residuals show no pattern against predicted values or run order, and no single run dominates the fit.",
       "Criterion 4 of PCMP-001 §7.2: the residuals show no pattern against predicted values or run order, and no single run dominates the fit.")
    sq("finding", "The prediction error sum of squares (PRESS) adds up the squared error of each run when it is predicted from a fit to all the other runs, and predicted R² is one minus PRESS divided by the total sum of squares")
    sq("finding", "A model that fails the lack-of-fit test or the limit on overfitting is either refitted with a justified change of terms or transformation, or it is not used to set a range.",
       "The master plan states the remedy for a model that fails: a model that fails the lack-of-fit test or the limit on overfitting is either refitted with a justified change of terms or transformation, or it is not used to set a range.")
    sq("finding", "This investigation applies the first three criteria as tests, because they decide whether a model of a design of this size can be adequate at all.")
    sq("finding", "In this document a model is called adequate when it meets the three tests.")
    st("finding", q_refit23, [ref("finding", q_refit23)])
    sq("finding", "Each step with a response-surface design has at least one model that fails.")
    sq("finding", """The `{python} n_fail` failing models all fail the limit on overfitting, with R² minus predicted R² from `{python} f2(gap_lo)` to `{python} f2(gap_hi)` against a limit of `{python} gap_max_s`.""")
    sq("finding", """With Protein A run `{python} run23` at its design pH, no model fails the lack-of-fit test, and the lowest lack-of-fit p-value among the failing models is `{python} f"{plof_min:.3f}"`.""")
    sq("finding", """With `{python} n_cp` centre points, however, pure error has `{python} df_pe` degrees of freedom, so the test has little power to find such an error.""",
       """With `{python} n_cp` centre points, pure error has `{python} df_pe` degrees of freedom, so the lack-of-fit test has little power to find a systematic error.""")
    sq("finding", """Of the failing models, `{python} n_fail_F` also fail the model F-test, with p-values from `{python} f"{fail_F_lo:.3f}"` to `{python} f"{fail_F_hi:.3f}"`.""")
    sq("finding", """They are `{python} fail_F_phrase`.""",
       """The failing models that also fail the model F-test are `{python} fail_F_phrase`.""")
    st("finding", q("""The Version 2.0 analysis puts Protein A response-surface run `{python} run23` at the elution buffer pH recorded under deviation `{python} run23_dev`, `{python} f"{run23_ph:g}"` instead of the design pH of `{python} f"{run23_design:g}"` (discrepancy `{python} pd_ph`)."""), [ref("finding", q_run23)])
    st("finding", q("""With run `{python} run23` at its recorded pH, the full quadratic model of pool host cell protein fails the lack-of-fit test (`{python} ptxt(fq_rec["p_lof"])`), while it meets the model F-test and the limit on overfitting."""), [ref("finding", q_fqrec)])
    sq("finding", """With run `{python} run23` at either pH, the same `{python} n_fail` models fail the limit on overfitting.""")
    sq("finding", """Model selection, corrective action CA3, covers every output""",
       "Because model selection, corrective action CA3, covers every output, the failing full quadratic model of pool host cell protein needs no separate remedy.",
       ["so the failing full quadratic model of pool host cell protein needs no separate remedy."])
    sq("finding", """Models with an effect that the design is too small for (`{python} n_eff` models).""",
       """`{python} n_eff` of the failing models have an effect that the design is too small for: the refit of the planned runs by backward elimination keeps at least one significant term.""",
       ["""keeps at least one term that is significant at α = `{python} eff_a_s`."""])
    sq("finding", """The full models of this group reach an R² of `{python} f2(r2_eff_lo)` to `{python} f2(r2_eff_hi)`.""",
       """The full models of the failing models with an effect reach an R² of `{python} f2(r2_eff_lo)` to `{python} f2(r2_eff_hi)`.""")
    sq("finding", """Models of attributes with no detected effect within the range studied (`{python} n_noeff` models).""",
       """`{python} n_noeff` of the failing models are of attributes with no detected effect within the range studied: the refit of the planned runs keeps no term besides the intercept.""",
       ["The refit of the planned runs keeps no term besides the intercept."])
    sq("finding", """The model F-test of the full model is not significant for any of them, and predicted R² is below zero, down to `{python} num_txt(pred_none_min, 2)` for `{python} pred_none_min_model`.""",
       """For the attributes with no detected effect the model F-test of the full model is not significant, and predicted R² is below zero, down to `{python} num_txt(pred_none_min, 2)` for `{python} pred_none_min_model`.""")
    sq("finding", """The refit keeps an effect on fragments at `{python} join_and(frag_eff_steps)`, and none at `{python} join_and(frag_none_steps)`.""")
    sq("finding", """`{python} n_met_full` meet all three tests and need no remedy""",
       """`{python} n_met_full` full quadratic models meet all three tests and need no remedy.""")
    sq("finding", """The re-analysis counted the last one, of `{python} exf_phrase`, among them as well, because none of its tests failed.""",
       """The re-analysis counted the full quadratic model of `{python} exf_phrase` among the models that meet the tests, because none of its tests failed.""")
    sq("finding", "With no residual there is no pure error for the lack-of-fit test and no residual mean square for the model F-test, so neither test can be applied, and an exact fit is not adequate.")

    # -- Root cause
    sq("root", "The primary cause is that the plans prescribed the full quadratic model as the predictive model of every response-surface design, with no model selection.")
    sq("root", "The full quadratic model keeps every main effect, two-factor interaction and squared term, whatever the data show.")
    sq("root", """With four factors, the full quadratic model has `{python} k4` terms, including the intercept, and the planned face-centred design has `{python} n4` runs.""")
    sq("root", """Low-pH viral inactivation has three factors, `{python} k3` terms and `{python} n3` runs.""")
    sq("root", """Virus filtration has two factors, `{python} k2` terms and `{python} n2` runs.""")
    sq("root", """The average leverage equals the number of terms divided by the number of runs, and in these designs it lies between `{python} f2(lev_lo)` and `{python} f2(lev_hi)`.""")
    sq("root", """Leverage differs from run to run, from `{python} f2(h_lo)` to `{python} f2(h_hi)` in these designs, so the enlargement at the average leverage understates the effect.""")
    sq("root", """That factor is `{python} f"{pr_lo:.1f}"` to `{python} f"{pr_hi:.1f}"` for these designs.""",
       """In expectation, PRESS is the residual sum of squares times a factor of `{python} f"{pr_lo:.1f}"` to `{python} f"{pr_hi:.1f}"` for these designs.""")
    sq("root", """It is therefore expected to be `{python} f"{pr_lo - 1:.1f}"` to `{python} f"{pr_hi - 1:.1f}"` times the share of the variation that the model leaves unexplained, one minus R².""",
       """R² minus predicted R² is expected to be `{python} f"{pr_lo - 1:.1f}"` to `{python} f"{pr_hi - 1:.1f}"` times one minus R², the share of the variation that the model leaves unexplained.""")
    sq("root", """The limit of `{python} gap_max_s` is then met, in expectation, only where R² is above `{python} f2(r2_need_lo)` to `{python} f2(r2_need_hi)`.""")
    sq("root", """has an R² of at least `{python} f2(r2_pass_min)`, and every model that failed the limit on overfitting has an R² of at most `{python} f2(r2_fail_max)`.""",
       """Every full quadratic model that met all three tests has an R² of at least `{python} f2(r2_pass_min)`, and every model that failed the limit on overfitting has an R² of at most `{python} f2(r2_fail_max)`.""")
    sq("root", """With the planned runs alone, the probability that the full quadratic model meets the lack-of-fit test and the limit on overfitting is `{python} f3(AUG[HM]["a0"])` for high mannose, `{python} f3(AUG[AV]["a0"])` for acidic variants and `{python} f3(AUG[HCP]["a0"])` for host cell protein at anion exchange.""")
    sq("root", "For such an attribute the full quadratic model fits only random variation, and each of its terms takes up part of it.",
       "For an attribute with no detected effect within the range studied the full quadratic model fits only random variation, and each of its terms takes up part of it.")
    sq("root", """R² stays between `{python} f2(r2_none_lo)` and `{python} f2(r2_none_hi)` while predicted R² is below zero.""",
       """For the attributes with no detected effect, R² stays between `{python} f2(r2_none_lo)` and `{python} f2(r2_none_hi)` while predicted R² is below zero.""")
    sq("root", "With no effect, R² minus predicted R² depends on the number of terms against the number of runs, not on the size of the noise, so it shrinks only as the runs outgrow the terms.")
    sq("root", """Their probability of success is at most `{python} f3(frag_flat_max)` at every size computed, up to the size of the planned design""",
       """The fragment models of Protein A and cation exchange have a probability of success of at most `{python} f3(frag_flat_max)` at every size computed, up to the size of the planned design.""")
    sq("root", "The contributing cause is that no plan checked the size of its design against the model it was to fit.")
    sq("root", "Version 1.0 of the process characterization master plan (PCMP-001) left the model-adequacy threshold to the individual study, and the Version 1.0 plans set none.")
    sq("root", """The limit of `{python} gap_max_s` on R² minus predicted R² came with Version 2.0 of the master plan.""")
    sq("root", """The last planned response-surface study ended on `{python} rsm_last_end`, before the investigation into acceptance criteria set after the data were seen (INV-001) was opened.""")
    sq("root", """The root cause was recorded on `{python} sel_date`.""")
    sq("root", "and the augmentations it gave had been decided before that date, under the full quadratic model that the plans prescribed.",
       "The remedy rule and the augmentations it gave had been decided before the root cause was recorded, under the full quadratic model that the plans prescribed.")

    # -- Remedy and decision rule
    st("rule", "The master plan names no augmentation.", [ref("rule", q_noaug)])
    sq("rule", "Augmentation is this investigation's rule, for a design too small for the model a decision needs.")
    sq("rule", "The A-Mab case study names the same remedy for a design that cannot resolve the terms a decision needs, which is to augment it",
       "The A-Mab case study names the same remedy, to augment a design that cannot resolve the terms a decision needs.")
    sq("rule", """QA approved the remedy rule on `{python} decided`, before any new run was made, and it was applied to every failing model in the same way""",
       """QA approved the remedy rule on `{python} decided`, before any new run was made, and it was applied to every failing model in the same way.""")
    sq("rule", """The number of runs is the smallest that gives a probability of success of at least `{python} target_s` that the planned model, the full quadratic with a block term, meets the lack-of-fit test and the limit on overfitting on all runs""",
       """Rule 1: a failing model of an attribute of the drug substance specification, on which the refit of the planned runs keeps an effect, is resolved by the smallest number of further runs that gives a probability of success of at least `{python} target_s` that the full quadratic with a block term meets the lack-of-fit test and the limit on overfitting on all runs.""",
       ["A failing model of an attribute of the drug substance specification, on which the refit of the planned runs keeps an effect, is resolved by further runs."])
    sq("rule", "It is a process requirement, demonstrated by spiking studies at worst-case conditions against a cumulative claim",
       "Rule 2: viral clearance is not tested on the drug substance; it is a process requirement, demonstrated by spiking studies at worst-case conditions against a cumulative claim, so its models are refitted and no augmentation spikes virus.",
       ["Its models are refitted, and no augmentation spikes virus."])
    sq("rule", "No augmentation is larger than the planned design.",
       "Rule 3: no augmentation is larger than the planned design, and where the target probability of success is not reached within that size the model is refitted.",
       ["Where the target probability of success is not reached within that size, the model is refitted."])
    sq("rule", "Every other failing model is refitted.", "Rule 4: every other failing model is refitted.")
    sq("rule", "A response with no adequate model, full or refitted, is judged on its measured results.",
       "Rule 5: a response with no adequate model, full or refitted, is judged on its measured results, and no model sets a range for it.",
       ["No model sets a range for it."])
    sq("rule", "Further runs make the estimate of every term of the full model more precise.")
    sq("rule", """The target of `{python} target_s` is `{python} assurance_basis`.""")
    sq("rule", "The cap on the size of an augmentation, the size of the planned design, keeps a remedy from becoming a new study.")
    sq("rule", "The remedy rule did not foresee a viral clearance model that bears on a decision.")
    sq("rule", "Under rule 2, which refits every viral clearance model and spikes no virus, the XMuLV model at low-pH viral inactivation was refitted, because viral clearance is not tested on the drug substance.")
    sq("rule", """The refit removes terms by hierarchical backward elimination at α = `{python} eff_a_s`, and it is corrective action CA2.""")
    sq("rule", "At each step, the least significant term that no remaining term contains is removed.")
    sq("rule", "In an augmented design the block term belongs to the design and is never removed.")
    sq("rule", "Model selection, corrective action CA3, later replaced the refit by backward elimination for every output, the outputs that CA2 had refitted included",
       "Model selection, corrective action CA3, later replaced the refit by backward elimination for every output, the outputs that CA2 had refitted included.")
    sq("rule", "The sample-size calculation rests on the refits.")
    sq("rule", "The designs span the characterized range, so a response whose measured results all meet the criterion is taken to meet it over the NOR.")
    sq("rule", "A modelled output must instead meet its criterion with the 95 % prediction interval of a single batch at every combination of NOR low, set-point and NOR high.")
    sq("rule", """The remedy rule gives `{python} n_aug_m` models an augmentation, `{python} n_aug_bio` at the production bioreactor and `{python} n_aug_aex` at anion exchange.""")
    sq("rule", """Of the `{python} n_ref` refitted models, `{python} n_viral` are models of viral clearance, `{python} n_noeff_r` have no effect to resolve and `{python} n_notr` have an effect but do not reach the target probability of success within the size of their planned design.""")
    sq("rule", """Of the viral clearance models, `{python} viral_reach_phrase` would reach the target with `{python} viral_reach_runs` further runs.""")
    sq("rule", """Their refits keep effects that the design cannot predict well, with R² minus predicted R² of `{python} none_gaps`.""",
       """The refits of `{python} none_phrase` are not adequate either: they keep effects that the design cannot predict well, with R² minus predicted R² of `{python} none_gaps`.""",
       ["""The refits of `{python} none_phrase` are not adequate either."""])
    for key, row in rmrow.items():
        c = _cells(row)
        k, resp = key
        mean_only = c[2] == "None, the mean only"
        runs_txt = (f"{c[3]} further runs" if c[3] != "–" else
                    "not computed, because the refit keeps no effect" if mean_only else
                    "not reached within the size of the planned design")
        st("rule", f"{T.STEP_NAME[k]}, {attr_prose(resp, k)}: the refit of the planned runs keeps "
                   f"{'no term, the mean only' if mean_only else c[2]}; runs needed for a probability of success of "
                   f"{ns['target_s']}: {runs_txt}; remedy: {lc(_nofoot(c[4]))}; reason: {lc(c[5])}.",
           row_refs("rule", rm_t, rmrow, key))

    # -- Sample-size calculation
    sq("ss_method", "The number of further runs is calculated by simulation, separately for each failing model with an effect.")
    sq("ss_method", "The simulation estimates the probability of success, which is the probability, at the effects estimated from the planned runs, that the planned model meets the second and the third of these tests once the design has been augmented by a given number of runs.")
    sq("ss_method", "The planned model is the full quadratic with a block term, on the raw scale, because that was the model the plans prescribed when the runs were sized.")
    sq("ss_method", "Its residual standard deviation is taken as the variation between runs.",
       "The refit of the planned runs by backward elimination is taken as the true model, and its residual standard deviation as the variation between runs.",
       ["is taken as the true model, with its fitted coefficients."])
    sq("ss_method", """For each size, `{python} f"{reps:,}"` data sets are simulated.""")
    sq("ss_method", "The model F-test is not simulated.")
    sq("ss_method", "Pure error comes from the replicated centre points of the planned design, because no augmentation repeats a point within its own block.")
    sq("ss_method", """Sizes are evaluated in steps of `{python} size_step` runs, up to the size of the planned design.""")
    sq("ss_method", """In `{python} n_dip` of the `{python} n_curves` curves it falls at least once from one size to the next""",
       """The probability of success falls at least once from one size to the next in `{python} n_dip` of the `{python} n_curves` curves, because the D-optimal augmentation of each size is a different set of points.""",
       ["The probability of success does not always rise with every further run, because the D-optimal augmentation of each size is a different set of points."])
    sq("ss_method", """The probability of success cannot rise much above `{python} f2(lof_ceiling)`.""")
    sq("ss_method", """A target of `{python} target_s` therefore asks that the limit on overfitting be met in about `{python} f"{100 * gap_needed:.0f}"` % of data sets.""")
    sq("ss_method", "The calculation assumes that the refit of the planned runs is the true model, that the error is normal with the same variance at every level, and that the two blocks differ by a constant at most.")
    sq("ss_method", """On the planned runs that the simulation used, model selection put `{python} len(log_curves_p)` of the outputs simulated here on the log scale (`{python} out_phrase(log_curves_p)`), and on all runs also `{python} out_phrase(log_curves_a)`.""")
    sq("ss_method", "Each curve uses its own stream of a pseudo-random number generator with a fixed seed, so the calculation gives the same result each time it is run.")
    sq("ss_method", "First, it simulates the planned runs again together with the augmentation runs, instead of holding the planned results at their measured values.",
       "The calculation simulates the planned runs again together with the augmentation runs, instead of holding the planned results at their measured values.")
    sq("ss_method", "Coefficients kept for that reason tend to lie further from zero than the effects they estimate, so the probability of success is optimistic.")
    sq("ss_dopt", "Each augmentation is drawn from the levels of the face-centred design, so every factor takes its low, centre or high level.")
    sq("ss_dopt", """For four factors this gives `{python} ncand4` candidate points.""")
    sq("ss_dopt", "The runs are chosen to maximise the determinant of the information matrix of the planned model, the full quadratic with a block term, with the planned runs held fixed in the first block.")
    sq("ss_dopt", "Ties go to the first candidate in a fixed order, so the design needs no random number.")
    sq("ss_dopt", "Their squared terms are therefore strongly correlated with each other, because every corner run sets all of them to one.",
       "In the face-centred designs of three and four factors the squared terms are strongly correlated with each other, because every corner run sets all of them to one.")
    sq("ss_dopt", "These points reduce the correlation between the squared terms.",
       "The points at the middle of an edge of the design cube, of which both D-optimal augmentations mostly consist, reduce the correlation between the squared terms.",
       ["Both D-optimal augmentations consist mostly of points at the middle of an edge of the design cube, with one factor at its centre level and the others at a limit"])
    sq("ss_dopt", """In the production bioreactor design the largest correlation between two squared terms falls from `{python} f2(sq_p)` on the planned runs to `{python} f2(sq_a)` on all runs.""")
    sq("ss_results", """The three models that the remedy rule augments reach a probability of success of `{python} target_s` within the size of their planned design.""")
    sq("ss_results", """High mannose needs `{python} AUG[HM]["m_req"]` further runs, with a probability of success of `{python} f3(AUG[HM]["a_req"])`.""")
    sq("ss_results", """Acidic variants need `{python} AUG[AV]["m_req"]`, with `{python} f3(AUG[AV]["a_req"])`.""",
       """Acidic variants need `{python} AUG[AV]["m_req"]` further runs, with a probability of success of `{python} f3(AUG[AV]["a_req"])`.""")
    sq("ss_results", """The production bioreactor design is therefore augmented by `{python} m_step["bioreactor"]` runs, the larger of the two, and at that size the probability of success for acidic variants is `{python} f3(AUG[AV]["a_step"])`.""")
    sq("ss_results", """Host cell protein at anion exchange needs `{python} AUG[HCP]["m_req"]` further runs, with `{python} f3(AUG[HCP]["a_req"])`, and the anion exchange design is augmented by that number.""")
    sq("ss_results", """The curves of `{python} viral_reach_phrase` cross the target within the size of the planned design.""")
    sq("ss_results", """The two models of low-pH viral inactivation rise with further runs but stay below the target up to the `{python} n_vi` runs of the planned design.""")
    sq("ss_results", """At that size their probability of success is `{python} f3(vi_curves["xmulv_lrf"])` for XMuLV clearance and `{python} f3(vi_curves[frag])` for fragments""",
       """At the `{python} n_vi` runs of the planned design the probability of success of the low-pH viral inactivation models is `{python} f3(vi_curves["xmulv_lrf"])` for XMuLV clearance and `{python} f3(vi_curves[frag])` for fragments.""")
    sq("ss_results", """The fragment models of Protein A and cation exchange stay at or below `{python} f3(frag_flat_max)` at every size.""")
    shown = [cc.text for cc in ss_t.header[1]]
    for key, row in ssrow.items():
        c = _cells(row)
        k, resp = key
        probs = [f"{v} with " + ("the planned runs alone" if m == "0" else f"{m} further runs")
                 for m, v in zip(shown, c[2:2 + len(shown)]) if v != "–"]
        need = (f"runs needed: {c[-2]}; lowest power at that size: {c[-1]}" if c[-2] != "–" else
                "the target is not reached within the size of the planned design")
        st("ss_results", f"{T.STEP_NAME[k]}, {attr_prose(resp, k)}: probability of success {'; '.join(probs)}; "
                         f"{need}.", [ref("ss_results", row, ss_t, ssrow)])
    sq("ss_power", "The augmentations are sized for the lack-of-fit test and the limit on overfitting, not for the power of each effect.")
    sq("ss_power", """The residual standard deviations of the refits behind these figures are `{python} f2(AUG[HM]["sd"])` percentage points for high mannose, `{python} f2(AUG[AV]["sd"])` percentage points for acidic variants and `{python} f2(AUG[HCP]["sd"])` `{python} attr_unit(HCP[1], HCP[0])` for host cell protein.""")
    sq("ss_power", """Of the `{python} n_terms_pw` effects, `{python} n_pw_hi` have a power of at least `{python} target_s`.""")
    sq("ss_power", """The weakest is `{python} weak_txt`, with a power of `{python} f2(weak_p)`.""")
    for key, row in pwrow.items():
        k, resp, t = key
        st("ss_power", f"{T.STEP_NAME[k]}, {attr_prose(resp, k)}: the effect {T._term_name(t, k)} of the refit has a power of "
                       f"{_cells(row)[-1]} at the size of the step's augmentation.", row_refs("ss_power", pw_t, pwrow, key))

    # -- Augmentation designs
    sq("designs", "Each augmentation was executed as a second block of its response-surface design, with the planned runs as the first block.")
    sq("designs", "The augmentation runs continue the run numbers of the planned design.")
    sq("designs", "They were executed in a randomized order, as the process characterization master plan requires (PCMP-001 §6.1), and the design tables give them in the order of the design.")
    sq("designs", """The two designs were approved on `{python} decided` with the remedy rule.""")
    st("des_bio", q("""The production bioreactor augmentation was made in study `{python} aug_id["bioreactor"]`, from `{python} aug_start["bioreactor"]` to `{python} aug_end["bioreactor"]`."""), [ref("des_bio", made["bioreactor"])])
    sq("des_bio", """Of these runs, `{python} S["bioreactor"]["edges"]` lie at the middle of an edge of the design cube and `{python} S["bioreactor"]["corners"]` at a corner.""",
       """Of the `{python} S["bioreactor"]["n"]` production bioreactor augmentation runs, `{python} S["bioreactor"]["edges"]` lie at the middle of an edge of the design cube and `{python} S["bioreactor"]["corners"]` at a corner.""")
    sq("des_bio", "The corner runs repeat settings that the planned factorial runs also used.")
    sq("des_bio", """Every run was tested for all `{python} n_bio` responses of the design (`{python} bio_resp_words`).""")
    st("des_bio", q("""The production bioreactor report (`{python} rep["bioreactor"]`) re-evaluates every model of the step on all runs, including the `{python} n_bio_pass` models that met the three tests on the planned runs."""), [ref("des_bio", q_reeval)])
    st("des_aex", q("""The anion exchange augmentation was made in study `{python} aug_id["aex"]`, from `{python} aug_start["aex"]` to `{python} aug_end["aex"]`."""), [ref("des_aex", made["aex"])])
    sq("des_aex", """Of these runs, `{python} S["aex"]["edges"]` lie at the middle of an edge of the design cube and `{python} S["aex"]["corners"]` at a corner, and the corner runs repeat planned factorial settings.""",
       """Of the `{python} S["aex"]["n"]` anion exchange augmentation runs, `{python} S["aex"]["edges"]` lie at the middle of an edge of the design cube and `{python} S["aex"]["corners"]` at a corner, and the corner runs repeat planned factorial settings.""")
    st("des_aex", "Every anion exchange augmentation run was tested for host cell protein, step yield and fragments by non-reduced CE-SDS.", [ref("des_aex", q_cesds)])
    st("des_aex", "No virus was spiked, so XMuLV and MVM clearance were not measured at anion exchange, and their models keep the planned runs alone.", [ref("des_aex", q_nospike)])

    # -- Model selection
    sq("sel_proc", """Model selection was adopted as corrective action CA3 on `{python} sel_date`, before the investigation into acceptance criteria set after the data were seen (INV-001) closed on `{python} INV["closed"]`.""")
    sq("sel_proc", "It replaced the analysis of every output, the refits of corrective action CA2 included.",
       "Model selection replaced the analysis of every output, the refits of corrective action CA2 included.")
    sq("sel_proc", "Each report with a response-surface design applies it to every output of the design, on all runs in which the output was measured.")
    sq("sel_proc", "The process characterization master plan (PCMP-001) is not changed.")
    sq("sel_proc", "The output is modelled on the log scale (λ = 0) where this interval contains 0 and excludes 1.",
       "The output is modelled on the log scale (λ = 0) where the 95 % interval of its Box-Cox profile likelihood contains 0 and excludes 1, and otherwise on the raw scale (λ = 1).",
       ["Otherwise it is modelled on the raw scale (λ = 1)."])
    sq("sel_proc", "The rule chooses between these two scales only, and only an output whose results are all positive can take the log scale.")
    sq("sel_proc", """On all runs this applies to `{python} eb_phrase`.""",
       """The raw scale is kept where the interval excludes both 0 and 1, which on all runs applies to `{python} eb_phrase`.""",
       ["Where the interval excludes both 0 and 1, the raw scale is kept."])
    sq("sel_proc", "The scale is chosen on the full quadratic before the search, so that the search compares every candidate on one scale.")
    sq("sel_proc", "Strong hierarchy allows an interaction only together with both of its main effects, and a squared term only together with its main effect.")
    sq("sel_proc", "The block term is kept in every candidate.")
    sq("sel_proc", "If it fails, no other candidate takes its place.",
       "If the selected model fails the three tests, no other candidate takes its place.")
    sq("sel_proc", "A model chosen as the best of many candidates fits those runs better than a model fixed in advance, so the check of a selected model against the three tests is optimistic.")
    sq("sel_proc", "For a log-scale output it is the same difference of the mean logarithms, reported as a ratio of geometric means, and a scale-down prediction is divided by it.",
       "For a log-scale output the scale-down offset is the difference of the mean logarithms, reported as a ratio of geometric means, and a scale-down prediction is divided by it.")
    sq("sel_proc", "A selected model with terms that passes is the predictive model of the output, and it sets the ranges of its step.")
    sq("sel_proc", """depends on the number of runs only, `{python} f2(gap_mean_only(n_lo))` for `{python} n_lo` runs and `{python} f2(gap_mean_only(n_hi))` for `{python} n_hi`, so for such a model the check reduces to the lack-of-fit test.""",
       """For a model of the mean alone on a single block, R² minus predicted R² depends on the number of runs only, `{python} f2(gap_mean_only(n_lo))` for `{python} n_lo` runs and `{python} f2(gap_mean_only(n_hi))` for `{python} n_hi`, so the check reduces to the lack-of-fit test.""")
    sq("sel_proc", "An output whose selected model fails, or fits exactly, has no adequate model.",
       "An output whose selected model fails, or fits exactly, has no adequate model.")
    sq("sel_log", "Host cell protein in the Protein A pool shows what the log scale does.")
    st("sel_log", q("""Every model of pool host cell protein in the section puts response-surface run `{python} run23` at the elution buffer pH recorded under deviation `{python} run23_dev`, as the Version 2.0 analysis does."""), [ref("sel_log", q_run23_log)])
    sq("sel_log", """Its range studied is `{python} f"{pl_ld.prange[0]:g}"` to `{python} f"{pl_ld.prange[1]:g}"` `{python} pl_ld.unit`, so one coded unit is `{python} f"{half_ld:g}"` `{python} pl_ld.unit`.""",
       """The range studied of protein load is `{python} f"{pl_ld.prange[0]:g}"` to `{python} f"{pl_ld.prange[1]:g}"` `{python} pl_ld.unit`, so one coded unit is `{python} f"{half_ld:g}"` `{python} pl_ld.unit`.""")
    sq("sel_log", """Its coefficient on the log scale is b = `{python} f3(b_ld)`.""",
       """The coefficient of protein load in the log-scale model of pool host cell protein is b = `{python} f3(b_ld)`.""")
    sq("sel_log", """Across the range studied, the selected model multiplies pool host cell protein by a factor of `{python} fold_txt`, from the low to the high end of each parameter.""")
    sq("sel_log", "A purification step removes a share of what is present, so a parameter changes the share that is removed, not a fixed amount.")
    st("sel_log", q("""The precision of the host cell protein ELISA (`{python} elisa["id"]`) is `{python} f"{elisa['precision_pct']:g}"` % of the level, so the scatter of the results grows with the level."""), [ref("sel_log", q_elisa)])
    sq("sel_log", "Effects that multiply look like an interaction when they are added on the raw scale.")
    sq("sel_log", """On the raw scale the full quadratic model needs the interaction `{python} int_h_txt` (`{python} ptxt(p_int_raw)`).""")
    sq("sel_log", """On the log scale the same interaction is not significant (`{python} ptxt(p_int_log)`), and the selected model has no interaction at all.""")
    sq("sel_log", "Least squares needs no assumption about the distribution of the residuals to estimate the coefficients.")
    sq("sel_log", """On the raw scale the standard deviation of the residuals is `{python} f"{sd_raw_lo:,.0f}"` `{python} hcp_unit` in the lower half of the predictions and `{python} f"{sd_raw_hi:,.0f}"` `{python} hcp_unit` in the upper half, `{python} f"{sd_raw_ratio:.2f}"` times as large.""")
    sq("sel_log", """On the log scale the same split gives `{python} f"{sd_log_lo:.3f}"` and `{python} f"{sd_log_hi:.3f}"` in natural-log units, `{python} f"{sd_log_ratio:.2f}"` times as large.""")
    sq("sel_log", """It puts λ at `{python} f2(bc_h["lambda"])`, with a 95 % interval from `{python} num_txt(bc_h["lo"], 2)` to `{python} num_txt(bc_h["hi"], 2)`.""",
       """The Box-Cox profile of the full quadratic model of pool host cell protein puts λ at `{python} f2(bc_h["lambda"])`, with a 95 % interval from `{python} num_txt(bc_h["lo"], 2)` to `{python} num_txt(bc_h["hi"], 2)`.""")
    sq("sel_log", "The interval contains 0 and excludes 1, so the data support the log scale and reject the raw scale.")
    sq("sel_log", """The scale-down offset is a ratio of geometric means, `{python} f2(off_h["offset"])` for pool host cell protein with a `{python} f"{100 * off_h['ci']:.0f}"` % confidence interval from `{python} f2(off_h["lo"])` to `{python} f2(off_h["hi"])`, and a scale-down prediction is divided by it.""")
    sq("sel_log", "It keeps its 95 % coverage, because the probability that ln y lies between two values is the probability that y lies between their antilogs.",
       "A prediction interval calculated on the log scale and transformed back keeps its 95 % coverage.")
    sq("sel_log", """At the least favourable combination of the NOR in force (`{python} wc_h_txt`), the model predicts ln y = `{python} f3(ln_w)` in the scale-down model.""")
    sq("sel_log", """This gives `{python} f3(ln_w)` ± `{python} f3(half_w)`.""",
       """On the log scale the two-sided 95 % prediction interval of a single batch at that combination is `{python} f3(ln_w)` ± `{python} f3(half_w)`.""")
    sq("sel_log", """Divided by the scale-down offset of `{python} f2(off_h["offset"])`, it runs from `{python} f"{wc_h['pi_low']:,.0f}"` to `{python} f"{wc_h['pi_high']:,.0f}"` `{python} hcp_unit` around a median of `{python} f"{wc_h['predicted']:,.0f}"` `{python} hcp_unit` at manufacturing scale""",
       """At manufacturing scale the interval runs from `{python} f"{wc_h['pi_low']:,.0f}"` to `{python} f"{wc_h['pi_high']:,.0f}"` `{python} hcp_unit` around a median of `{python} f"{wc_h['predicted']:,.0f}"` `{python} hcp_unit`.""")
    sq("sel_log", "The conclusion over the NOR uses this two-sided interval.")
    sq("sel_log", "The predicted value is the median of the output, its geometric mean, not its arithmetic mean.")
    sq("sel_log", """In the reports, `{python} n_log_sel` of the `{python} n_models` outputs with a criterion are modelled on the log scale.""")
    sq("sel_log", """They are `{python} log_sel_phrase`.""",
       """The outputs modelled on the log scale are `{python} log_sel_phrase`.""")
    sq("sel_search", "The goal of the search is the model with the lowest AICc among all hierarchical submodels of the full quadratic.")
    sq("sel_search", "AICc is the sum of a fit term, a penalty and a correction for small samples.")
    sq("sel_search", "The penalty is 2p, where p is the number of coefficients, the intercept included.")
    sq("sel_search", "A term is therefore kept only where it lowers the fit term by more than it raises the penalty and the correction.")
    sq("sel_search", """For the full quadratic model on `{python} n4` runs, p is `{python} p_full`, so the penalty is `{python} aic_pen`, and k is `{python} kk_full`, so the correction adds `{python} f"{aicc_corr:.1f}"`.""")
    sq("sel_search", """On the log scale the fit term is `{python} num_txt(AP_f["fit"])` for the full quadratic model and `{python} num_txt(AP_s["fit"])` for the selected model.""",
       """For pool host cell protein on the log scale the fit term is `{python} num_txt(AP_f["fit"])` for the full quadratic model and `{python} num_txt(AP_s["fit"])` for the selected model.""")
    sq("sel_search", """The full quadratic fits better by `{python} f"{d_fit:.1f}"`, but its penalty and correction together are larger by `{python} f"{d_pen:.1f}"`.""")
    sq("sel_search", """The selected model therefore has the lower AICc, `{python} num_txt(AP_s["aicc"])` against `{python} num_txt(AP_f["aicc"])` for the full quadratic model, a difference of `{python} f"{d_pen - d_fit:.1f}"`.""")
    sq("sel_search", """The search fits every candidate, `{python} f"{n_cand[4]:,}"` for a design with four factors, `{python} n_cand[3]` for three and `{python} n_cand[2]` for two, the model of the mean included.""")
    sq("sel_search", "It therefore stops where only a combination of changes would lower AICc further.",
       "A stepwise search adds or removes one term at a time and therefore stops where only a combination of changes would lower AICc further.")
    sq("sel_search", """On this campaign's data the two searches were compared for `{python} n_cmp` outputs with a criterion.""")
    sq("sel_search", """A backward stepwise search from the full quadratic would have stopped at a model with a higher AICc than the best candidate for `{python} n_bw` of them, a forward search from the mean for `{python} n_fw`, and one or the other for `{python} n_either`.""")
    sq("sel_search", """For `{python} attr_prose(EXK[1], EXK[0])` `{python} at_step(EXK[0])`, for example, the exhaustive search selects `{python} int(ex.n_terms)` terms with an AICc of `{python} num_txt(ex.aicc)`.""")
    sq("sel_search", """A backward search stops at `{python} int(ex.backward_terms)` terms (`{python} num_txt(ex.backward_aicc)`) and a forward search at `{python} int(ex.forward_terms)` terms (`{python} num_txt(ex.forward_aicc)`).""",
       """For the same output a backward search stops at `{python} int(ex.backward_terms)` terms (`{python} num_txt(ex.backward_aicc)`) and a forward search at `{python} int(ex.forward_terms)` terms (`{python} num_txt(ex.forward_aicc)`).""")
    sq("sel_search", "It decided by the p-value of each term.",
       "The backward elimination of corrective action CA2 decided by the p-value of each term.")
    sq("sel_search", "It also worked on the raw scale only.",
       "The backward elimination of corrective action CA2 worked on the raw scale only.")
    sq("sel_verif", "The verification of these worst cases uses the same model selection, on the planned runs of each downstream step.")
    sq("sel_verif", "Where the predicted value of a step is worse than the platform worst case, the bound replaces the platform value, and the criteria upstream of the step tighten.")
    sq("sel_verif", "and is not an exact fit, the bound replaces the platform value, and the criteria upstream widen.",
       "Where the single-batch bound is better than the platform worst case, on a selected model that meets the three tests and is not an exact fit, the bound replaces the platform value, and the criteria upstream widen.")
    sq("sel_verif", "A bound from a tolerance interval covers a stated share of all batches with a stated confidence, and it is wider.")
    sq("sel_verif", "The bound is pointwise at each combination, not simultaneous over them.")
    sq("sel_verif", "Neither of the two bounds behind the widenings depends on a single run.")
    sq("sel_verif", """These are runs `{python} join_and(str(x) for x in DA["runs"])` for host cell protein at anion exchange and runs `{python} join_and(str(x) for x in DV["runs"])` for aggregate at low-pH viral inactivation.""",
       """The runs whose Cook's distance exceeds `{python} f"{cook_f:g}"`/n are runs `{python} join_and(str(x) for x in DA["runs"])` for host cell protein at anion exchange and runs `{python} join_and(str(x) for x in DV["runs"])` for aggregate at low-pH viral inactivation.""",
       ["""For each bound, every run whose Cook's distance exceeds `{python} f"{cook_f:g}"`/n, with n the number of runs, was deleted in turn, and the model selection and the bound were computed again."""])
    sq("sel_verif", """Each time the selected model met the three tests and the bound stayed better than the platform value, from `{python} g3(DA["lo"])` to `{python} g3(DA["hi"])` against a fold of `{python} f"{DA['assumed']:g}"`, and from `{python} f3(DV["lo"])` to `{python} f3(DV["hi"])` against an increase of `{python} f2(DV["assumed"])` percentage points.""")
    sq("sel_verif", """The platform worst cases of the low-pH hold are increases over a hold of `{python} plat_hold` min.""")
    sq("sel_verif", """The A-Mab value is the increase within the NOR as characterized, which allows a hold of at most `{python} nor_hold_max` min.""")
    sq("sel_verif", "At low pH the antibody forms aggregate, and the aggregate grows with the time at that pH.")
    sq("sel_verif", """At the edges of the range studied, which include a hold of `{python} plat_hold` min, A-Mab adds up to `{python} f2(agg_edge)` percentage points of aggregate, more than the platform value of `{python} f2(agg_plat)`.""")
    sq("sel_verif", """Its single-batch bound of `{python} f3(agg_bound)` within the NOR as characterized is smaller than the platform value because that NOR ends at a shorter hold.""")
    sq("sel_verif", """The selected model of aggregate at low-pH viral inactivation has terms in `{python} fva_terms` only, and none in `{python} pname(VI, "ph")`.""")
    sq("sel_verif", """The NOR in force ends at the same longest `{python} pname(VI, "hold_time")`, `{python} f"{hold_p.nor[1]:g}"` `{python} hold_p.unit`, and the same highest `{python} pname(VI, "temperature")`, `{python} f"{temp_p.nor[1]:g}"` `{python} temp_p.unit`, as the NOR as characterized.""")
    sq("sel_verif", "The bound over the NOR as characterized therefore also covers the NOR in force.")
    sq("sel_verif", "For acidic variants the model at low pH fits exactly and is not adequate, so its bound replaces no platform value")
    sq("sel_changed", """Model selection gives an adequate model for `{python} n_sel_ok` of the `{python} n_models` outputs with a criterion.""")
    sq("sel_changed", "Every output whose full quadratic model met all three tests has an adequate selected model.")
    sq("sel_changed", """Of the `{python} n_fail` outputs whose full quadratic model failed, `{python} n_fail_ok` have an adequate selected model and `{python} len(none_fail)` have none.""")
    sq("sel_aug", "The augmentations were therefore not needed to pass these tests.",
       "The models of high mannose and acidic variants at the production bioreactor and of host cell protein at anion exchange meet the three tests on the planned runs alone once they are selected, so the augmentations were not needed to pass these tests.",
       ["They are the models of high mannose and acidic variants at the production bioreactor and of host cell protein at anion exchange."])
    sq("sel_aug", """Both started before model selection was adopted on `{python} sel_date`.""",
       """Both augmentations started before model selection was adopted on `{python} sel_date`.""")
    sq("sel_aug", "The anion exchange runs were still under way on that date, as were the production bioreactor runs, and both were completed.")
    st("sel_aug", q("""On all runs the full quadratic model with a block term meets the lack-of-fit test and the limit on overfitting for acidic variants and for host cell protein at anion exchange, with R² minus predicted R² of `{python} f2(FA[AV]["gap"])` and `{python} f2(FA[HCP]["gap"])`."""), [ref("sel_aug", q_fa)])
    st("sel_aug", q("""For high mannose that model does not meet the limit on overfitting on all runs, with R² minus predicted R² of `{python} f2(FA[HM]["gap"])` against the limit of `{python} gap_max_s`."""), [ref("sel_aug", q_fa_hm)])
    sq("sel_aug", """For high mannose, `{python} len(AUG[HM]["dropped"])` terms of the model selected on the planned runs are not in the model selected on all runs.""")
    sq("sel_aug", """On all runs the selected model of high mannose is on the log scale and has `{python} len(AUG[HM]["sel_a"]["names"])` terms (`{python} hm_all`).""")
    sq("sel_aug", "The scale changed with the second block as well, so part of the change in terms may come from the scale.")
    sq("sel_aug", """and the second block resolves `{python} len(AUG[AV]["added"])` further terms (`{python} av_added`).""",
       """For acidic variants every term of the model selected on the planned runs is kept on all runs, and the second block resolves `{python} len(AUG[AV]["added"])` further terms (`{python} av_added`).""")
    sq("sel_aug", "For host cell protein at anion exchange the selected model is the same on both sets of runs.")
    sq("sel_aug", """With `{python} int(hm_c.n_new)` new runs, that test rejects a model with fewer than `{python} int(hm_c.k_min)` inside.""",
       """With `{python} int(hm_c.n_new)` new runs, the one-sided binomial test at the `{python} f"{eff_alpha:g}"` level rejects a model with fewer than `{python} int(hm_c.k_min)` inside its 95 % prediction intervals.""")
    sq("sel_aug", """Only `{python} int(hm_c.inside_pi)` of the `{python} int(hm_c.n_new)` new runs fall inside the interval for high mannose and `{python} int(agg_c.inside_pi)` for aggregates at the production bioreactor, and the test rejects both models (`{python} ptxt(hm_c.p_binom)` and `{python} ptxt(agg_c.p_binom)`).""")
    sq("sel_aug", """Their prediction error is `{python} f"{hm_c.ratio:.1f}"` and `{python} f"{agg_c.ratio:.1f}"` times the residual standard deviation of the model.""",
       """The prediction error of the planned-run models of high mannose and aggregates is `{python} f"{hm_c.ratio:.1f}"` and `{python} f"{agg_c.ratio:.1f}"` times their residual standard deviation.""")
    sq("sel_aug", """For the other outputs the ratio is at most `{python} f"{others_ratio:.1f}"`, and every count passes the test.""")
    sq("sel_aug", """Its p-values give no evidence of one, the smallest being `{python} f"{block_p_min:.3f}"`.""",
       """The p-values of the block term of the models on all runs give no evidence of a constant shift between the planned and the augmentation runs, the smallest being `{python} f"{block_p_min:.3f}"`.""",
       ["The block term of the models on all runs tests for a constant shift between the planned and the augmentation runs."])
    sq("sel_aug", """The planned production bioreactor runs ended on `{python} bio_rsm_end` and the augmentation began on `{python} aug_start["bioreactor"]`.""")
    sq("sel_aug", """For high mannose these differences vary no more than run-to-run variation explains (`{python} ptxt(CC[HM]["p"])`).""",
       """At the repeated corners of the production bioreactor design, runs `{python} bio_corner_runs`, the differences between the augmentation and the planned results of high mannose vary no more than run-to-run variation explains (`{python} ptxt(CC[HM]["p"])`).""",
       ["""A change in an effect would show at the corners that the augmentation repeats, runs `{python} bio_corner_runs` at the production bioreactor, as unequal differences between the repeated and the planned results."""])
    sq("sel_aug", """For aggregates they vary more, though not significantly at the `{python} f"{100 * eff_a:g}"` % level (`{python} ptxt(CC[AGG]["p"])`).""",
       """For aggregates the differences at the repeated corners vary more, though not significantly at the `{python} f"{100 * eff_a:g}"` % level (`{python} ptxt(CC[AGG]["p"])`).""")
    sq("sel_aug", """On all runs, high mannose loses the interactions `{python} hm_int_txt` that the planned runs suggested.""")
    sq("sel_aug", """Aggregates lose the terms `{python} agg_drop_txt` and gain a curvature in `{python} agg_add_txt.replace("²", "")`.""",
       """On all runs aggregates at the production bioreactor lose the terms `{python} agg_drop_txt` and gain a curvature in `{python} agg_add_txt.replace("²", "")`.""")
    sq("sel_aug", "For acidic variants the model selected on the planned runs predicts every new run within its interval, and the model of all runs adds the terms that the second block resolves.")
    for key, row in acrow.items():
        c = _cells(row)
        k, resp = key
        tp, ta = (x.strip() for x in c[2].split("→"))
        sp, sa = (x.strip() for x in c[3].split("→"))
        st("sel_aug", f"{T.STEP_NAME[k]}, {attr_prose(resp, k)}: the model selected on the planned runs "
                      f"({nterms(tp)}, {sp.lower()} scale) predicts {c[4]} augmentation runs inside its 95 % "
                      f"prediction interval, with a prediction error {c[5]} times its residual standard deviation; "
                      f"the model selected on all runs has {nterms(ta)} on the {sa.lower()} scale and a block "
                      f"p-value of {c[6]}.",
           [ref("sel_aug", row, ac_t, acrow)])
    sq("sel_none", """After selection, `{python} n_none_sel` outputs have no adequate model.""")
    sq("sel_none", "Every measured result meets its criterion.",
       "Every measured result of the outputs with no adequate model meets its criterion.")
    st("sel_none", "None of the outputs with no adequate model sets a range.", [ref("sel_none", q_noneset)])
    for key, row in mrrow.items():
        c = _cells(row)
        k, resp = key
        u = unit_of(cqa_of[key])
        st("sel_none", f"{T.STEP_NAME[k]}, {attr_prose(resp, k)}: no adequate model; judged on its measured results "
                       f"against the criterion {c[2]} {u}: {c[3]} results, the most adverse {c[4]} {u}, a margin of "
                       f"{c[5]} {u}.",
           [ref("sel_none", row, mr_t, mrrow)])
    sq("sel_none", "XMuLV clearance at virus filtration is the one output for which model selection and the refit by backward elimination disagree on whether an adequate model exists.")
    sq("sel_none", "The refit had reduced it to its mean, which meets the lack-of-fit test and the limit on overfitting.",
       "The refit by backward elimination had reduced XMuLV clearance at virus filtration to its mean, which meets the lack-of-fit test and the limit on overfitting.")
    sq("sel_none", """Model selection keeps a term in `{python} vf_terms`, because that model has the lower AICc (`{python} num_txt(fv["aicc"])` against `{python} num_txt(aicc_mean_vf)` for the mean alone).""")
    sq("sel_none", """Its model F-test is not significant (`{python} ptxt(fv["p"])`), and its R² minus predicted R² of `{python} f2(fv["gap"])` exceeds the limit of `{python} gap_max_s`.""",
       """The model F-test of the selected model of XMuLV clearance at virus filtration is not significant (`{python} ptxt(fv["p"])`), and its R² minus predicted R² of `{python} f2(fv["gap"])` exceeds the limit of `{python} gap_max_s`.""")
    sq("sel_none", """The two models differ by `{python} f"{d_aicc_vf:.1f}"` in AICc.""")
    sq("sel_exact", """Every run at the same `{python} pname(VI, "hold_time")` returned the same value, in the screening and the response-surface designs alike, the replicated centre points included.""",
       """For acidic variants at low-pH viral inactivation every run at the same `{python} pname(VI, "hold_time")` returned the same value, in the screening and the response-surface designs alike, the replicated centre points included.""")
    sq("sel_exact", "A prediction interval would have zero width.")
    sq("sel_exact", "The Box-Cox profile likelihood is unbounded, so no scale is chosen and no interval is reported.")
    sq("sel_exact", """The upper limit of acidic variants at the production bioreactor therefore stays at its a priori value of `{python} T.num(av_in)` %.""")
    sq("sel_zero", """The selected models of `{python} n_zero_sel` outputs have no term.""")
    sq("sel_zero", """They are `{python} zero_sel_phrase`.""",
       """The outputs whose selected models have no term are `{python} zero_sel_phrase`.""")
    sq("sel_zero", "No effect of the parameters on them was detected within the ranges studied.")

    # -- Impact assessment
    sq("impact", "Model selection, corrective action CA3, replaces the full quadratic model of every output with a criterion in the report of its step.")
    sq("impact", "Each report records the augmentation and the model selection as discrepancies from its plan, identified as plan discrepancies (PD).")
    sq("impact", "A discrepancy from the plan records work or an analysis that the approved plan did not foresee.")
    sq("impact", "A deviation records a departure from a procedure or a GMP requirement.")
    st("impact", "No procedure and no GMP requirement was departed from, so neither the augmentation nor the model selection is recorded as a deviation.", [ref("impact", q_nodev)])
    sq("impact", """The production bioreactor report (`{python} rep["bioreactor"]`) records the production bioreactor augmentation as `{python} pd_id["bioreactor"]`, and the anion exchange report (`{python} rep["aex"]`) records the anion exchange augmentation as `{python} pd_id["aex"]`.""")
    sq("impact", """Each of the `{python} n_steps` reports with a response-surface design records the model selection (`{python} sel_pd_txt`).""")
    st("impact", "The process characterization master plan (PCMP-001) and the step plans are not amended.", [ref("impact", q_noamend)])
    rep_of = {}
    for key, row in imrow.items():
        c = _cells(row)
        k, resp = key
        if c[0]:
            rep_of[k] = (c[0], c[4])
        r_name, disc = rep_of[k]
        model = _nofoot(c[3])
        model = re.sub(r"^(Raw|Log), ", lambda m: f"{m.group(1).lower()} scale, ", model)
        pds = " and ".join(f"{i} ({w})" for i, w in re.findall(r"(PD-\d{3}-\d{2}), (augmentation|model selection)", disc))
        st("impact", f"{r_name.split()[0]} ({ns['step_prose'](k)}), {lc(c[1])}: remedy "
                     f"{lc(_nofoot(c[2])) if c[2] != '–' else 'none'}; model in the report: {lc(model)}"
                     + (f"; discrepancies from the plan recorded in {r_name.split()[0]}: {pds}" if c[0] else "")
           + ".", [ref("impact", row, im_t, imrow)])
    sq("imp_crit", "The verification of the platform worst cases behind the criteria in force therefore used the selected models of the planned runs",
       "The verification of the platform worst cases behind the criteria in force used the selected models of the planned runs.")
    sq("imp_crit", """The same verification on the full quadratic models, the analysis the plans prescribed, gives different values for `{python} n_cd` criteria.""")
    sq("imp_crit", """Against them, model selection made `{python} n_wider` criteria wider, by `{python} pct_txt`, and kept `{python} len(kept)` at its a priori value.""")
    sq("imp_crit", """The full quadratic model of host cell protein fails the limit on overfitting, so its single-batch bound of `{python} b_aex_f` cannot widen a criterion, and the platform worst-case clearance fold of `{python} p_aex` enters the derivation.""",
       """At anion exchange the full quadratic model of host cell protein fails the limit on overfitting, so its single-batch bound of `{python} b_aex_f` cannot widen a criterion, and the platform worst-case clearance fold of `{python} p_aex` enters the derivation.""")
    sq("imp_crit", """The selected model is adequate, and its bound of `{python} b_aex_s` replaces the platform fold.""",
       """The selected model of host cell protein at anion exchange is adequate, and its bound of `{python} b_aex_s` replaces the platform fold.""")
    sq("imp_crit", """The host cell protein criteria `{python} hcp_crit_txt` therefore widen, because both lie upstream of anion exchange.""")
    sq("imp_crit", """The selected model of aggregate is on the log scale with `{python} n_terms_cxa` terms, and it gives a different prediction and a different single-batch bound from the full quadratic model.""",
       """At cation exchange the selected model of aggregate is on the log scale with `{python} n_terms_cxa` terms, and it gives a different prediction and a different single-batch bound from the full quadratic model.""")
    sq("imp_crit", """It tightens the aggregate criteria `{python} agg_crit_txt`, which lie upstream of cation exchange, by a different amount on each model.""",
       """The cation exchange aggregate bound tightens the aggregate criteria `{python} agg_crit_txt`, which lie upstream of cation exchange, by a different amount on each model.""")
    sq("imp_crit", """For host cell protein the predicted fold meets the platform fold of `{python} p_cexh` on both models and its single-batch bound does not, so the platform fold stays on both, and no criterion moves because of host cell protein at cation exchange.""")
    sq("imp_crit", """The verification on the full quadratic models found that none of its tests failed and took its bound of `{python} g3(av_bound)` percentage points, which would have widened the upper limit of acidic variants at the production bioreactor to `{python} T.num(av_full)` %.""")
    sq("imp_crit", """The platform value of `{python} f2(av_plat)` therefore stays, and the upper limit keeps its a priori value of `{python} T.num(av_apriori)` %.""",
       """For acidic variants at low-pH viral inactivation the platform value of `{python} f2(av_plat)` stays, and the upper limit of acidic variants at the production bioreactor keeps its a priori value of `{python} T.num(av_apriori)` %.""")
    sq("imp_crit", "Judged against the criteria that the full quadratic models would have given, no output changes its conclusion over the NOR in force.")
    sq("imp_crit", """For host cell protein in the Protein A pool, the lower end of the `{python} pname(HK[0], PF)` range moves from `{python} f"{par_in[PF][0]:.2f}"` to `{python} f"{par_wo[PF][0]:.2f}"`, and both lie below the NOR of `{python} f"{pf_nor[0]:g}"` to `{python} f"{pf_nor[1]:g}"`.""")
    sq("imp_crit", """A scale-down model is qualified for an output when its conclusion over the NOR is the same with the offset at either end of its `{python} f"{100 * ci_off:.0f}"` % confidence interval (PCMP-001 §7.1).""")
    sq("imp_crit", "In both cases the low end of the offset interval decides.",
       "For host cell protein in the Protein A pool and at cation exchange, the low end of the offset interval decides whether the scale-down model would be qualified against the criteria without model selection.",
       ["Against the criteria without model selection, the scale-down model would not be qualified for host cell protein in the Protein A pool or at cation exchange."])
    sq("imp_crit", """In the Protein A pool, with the offset at the low end of its interval, a ratio of `{python} f2(QD[HK]["off"]["lo"])`, the upper limit of the two-sided 95 % prediction interval of a single batch over the NOR, at manufacturing scale, is `{python} f"{QD[HK]['lim_lo']:,.0f}"` `{python} QD[HK]["unit"]`.""")
    sq("imp_crit", """That is above the criterion of `{python} f"{QD[HK]['crit_wo']:,.0f}"` `{python} QD[HK]["unit"]` that the full quadratic models give, and below the criterion in force of `{python} f"{QD[HK]['crit_in']:,.0f}"` `{python} QD[HK]["unit"]`.""",
       """In the Protein A pool that limit is above the criterion of `{python} f"{QD[HK]['crit_wo']:,.0f}"` `{python} QD[HK]["unit"]` that the full quadratic models give, and below the criterion in force of `{python} f"{QD[HK]['crit_in']:,.0f}"` `{python} QD[HK]["unit"]`.""")
    sq("imp_crit", """At cation exchange, with the offset at `{python} f2(QD[CXH]["off"]["lo"])`, the same limit is `{python} f"{QD[CXH]['lim_lo']:,.0f}"` `{python} QD[CXH]["unit"]`, against `{python} f"{QD[CXH]['crit_wo']:,.0f}"` `{python} QD[CXH]["unit"]` without model selection and `{python} f"{QD[CXH]['crit_in']:,.0f}"` `{python} QD[CXH]["unit"]` in force.""")
    sq("imp_crit", "These two qualifications rest on the criteria that model selection widened.")
    st("imp_crit", q("""Host cell protein and aggregates are attributes of the drug substance specification, with limits of `{python} join_and(f"{v:g} {u} {CQA_PL[c]}" for c, (v, u) in ds_by_cqa.items() if c in risk_cqas)`."""), [ref("imp_crit", q_risk)])
    sq("imp_crit", "A step output at its criterion still gives a drug substance within its limit, as long as each downstream step clears at least the value that the derivation uses.")
    sq("imp_crit", """For host cell protein these are a fold of `{python} p_cexh` at cation exchange, the platform worst case, and `{python} b_aex_s` at anion exchange, its single-batch bound.""")
    sq("imp_crit", """For aggregates they are a fold of `{python} g3(cexa_fold_in)` at cation exchange and an increase of `{python} g3(via_add_in)` percentage points at low-pH viral inactivation, both single-batch bounds.""")
    sq("imp_crit", "The master plan states that each process parameter of each batch is drawn from a normal distribution centred on its set-point, with a standard deviation of one sixth of the width of its NOR (PCMP-001 §6.4 and §6.5).")
    sq("imp_crit", """None of the `{python} f"{n_mc_poos:,}"` batches that the integrated process model simulated gives an out-of-specification drug substance for either attribute.""")
    sq("imp_crit", """With no failure in `{python} f"{n_mc_poos:,}"` batches, the one-sided 95 % upper bound on the rate of failure is `{python} f"{100 * oos_ub:.2f}"` %.""")
    sq("imp_crit", """The augmentation runs moved no criterion. Both augmentations ended after INV-001 closed, on `{python} aug_end_txt`, and the verification uses only the planned runs of each step.""")
    sq("imp_crit", """Repeated on all runs of anion exchange, the verification gives the same bound for host cell protein, `{python} f"{b_aex_all:.3g}"`, so the augmentation runs would not have moved the criteria either.""")
    for key, row in crrow.items():
        c = _cells(row)
        s_, r_, ds_, cq_ = key
        crit_name = f"{T.STEP_NAME[s_]}, {attr_prose(r_, s_)} ({ns['attr_unit'](r_, s_)})"
        limits = (f"upper limit {c[1]} a priori, {c[2]} without model selection and {c[3]} in force; " if c[0] else "")
        st("imp_crit", f"{crit_name}: {limits}downstream worst case {lc(c[4])}: platform value {c[5]}, value in the "
                       f"derivation {_nofoot(c[6])} on the full quadratic model and {_nofoot(c[7])} on the selected model.",
           [ref("imp_crit", row, cr_t, crrow)])
    for key, row in serow.items():
        c = _cells(row)
        st("imp_crit", f"{c[0]}: criterion in force {c[1]}, without model selection {c[2]}; conclusion over the NOR "
                       f"(in force / without model selection) {c[3]}; proven acceptable ranges: {c[4]}; scale-down "
                       f"model qualified (in force / without model selection): {c[5]}.",
           [ref("imp_crit", row, se_t, serow)])
    sq("imp_nor", "For every output with a criterion the two give the same conclusion, at the NOR as characterized and at the NOR in force.",
       "For every output with a criterion the full quadratic model of the planned runs and the model that the report uses give the same conclusion over the NOR, at the NOR as characterized and at the NOR in force.")
    sq("imp_nor", "XMuLV clearance at low-pH viral inactivation is judged on the mean LRF at the least favourable combination of NOR low, set-point and NOR high, because viral clearance is validated at worst-case conditions (PCMP-001 §6.4).")
    st("imp_nor", q_vsum, [ref("imp_nor", q_vsum)])
    sq("imp_nor", """On it, the lowest mean LRF within the NOR as characterized is `{python} f2(y6.min())`, at `{python} worst6`, so the step claim is not met.""",
       """On the selected model the lowest mean XMuLV LRF of low-pH viral inactivation within the NOR as characterized is `{python} f2(y6.min())`, at `{python} worst6`, so the step claim is not met.""")
    sq("imp_nor", """The full quadratic model gives a lowest mean of `{python} f2(y6f.min())` and the same conclusion.""")
    sq("imp_nor", """The low-pH viral inactivation report (`{python} rep[vk]`) moves the NOR of `{python} moved6_txt`, and it states the conclusion over the NOR in force.""")
    sq("imp_nor", "Acidic variants at the production bioreactor are judged on the 95 % prediction interval of a single batch at every combination of NOR low, set-point and NOR high.")
    st("imp_nor", q("""The lower limit of the criterion for acidic variants at the production bioreactor is `{python} f"{av_floor:g}"` %, the lower limit of the drug substance specification carried to the step unchanged."""), [ref("imp_nor", q_avlo)])
    sq("imp_nor", """The least favourable combination therefore lies at the NOR high of `{python} pname(bk, "pH")`.""")
    sq("imp_nor", """On the selected model of all runs, the lower prediction limit at `{python} worst_b` is `{python} f"{av_lo:.1f}"` % at manufacturing scale, so the criterion is not met.""")
    sq("imp_nor", """The predicted median at the same settings is `{python} f"{av_med:.1f}"` %, `{python} av_med_word` the criterion.""")
    sq("imp_nor", """On the full quadratic model of the planned runs the lower prediction limit at the same settings is `{python} f"{avc_full['pi_low']:.1f}"` %, and the criterion is not met either.""")
    st("imp_nor", q("""The production bioreactor report (`{python} rep[bk]`) states how the result for acidic variants is handled."""), [ref("imp_nor", q_pcr3)])
    st("imp_other", "INV-001 is not reopened.", [ref("imp_other", q_notreopen)])
    sq("imp_other", "Its comparison of the proven acceptable ranges of Version 1.0 and Version 2.0 uses the models that Version 1.0 fitted, so that it shows what the change of criteria moved.",
       "The comparison in INV-001 of the proven acceptable ranges of Version 1.0 and Version 2.0 uses the models that Version 1.0 fitted, so that it shows what the change of criteria moved.")
    sq("imp_other", "The intermediate acceptance criteria in force rest on the selected models",
       "The intermediate acceptance criteria in force rest on the selected models.")
    sq("imp_other", "The augmentation is the rule of this investigation.")
    st("imp_other", "The master plan is not changed for model selection, which each report records as a discrepancy from its plan.", [ref("imp_other", q_pcmp_same)])
    st("imp_other", "PCMR-001 Version 2.0 is to consolidate the conclusions of the step reports as they stand after the remedies and the model selection.", [ref("imp_other", q_pcmr)])
    st("imp_other", "The investigation has no product impact.", [ref("imp_other", q_noimp)])

    # -- CAPA
    st("capa", q_capa_ca3, [ref("capa", q_capa_ca3)])
    sq("capa", "Corrective action CA1, the augmentation of the designs that the remedy rule names, has two parts.")
    sq("capa", "The augmentation runs of CA1 were complete at closure.")
    sq("capa", """The second part of CA1, the re-evaluation of the augmented designs on all runs, is carried by the Version 2.0 reports of the two steps, due on `{python} capa.loc["CA1", "due"]`, together with the models chosen by model selection.""")
    sq("capa", "Preventive action PA1, the sample-size calculation for each new characterization plan, checks each new design by simulation before its plan is approved, at the expected effects and with the analysis the plan states.")
    sq("capa", "used the full quadratic model, the analysis the Version 1.0 plans prescribed.",
       "The sample-size simulation of INV-002 used the full quadratic model, the analysis the Version 1.0 plans prescribed.")
    sq("capa", """Preventive action PA2 revises SOP-1002, `{python} sop1002`, so that a plan states its model-selection procedure.""")
    for key, row in carow.items():
        c = _cells(row)
        st("capa", f"{c[0]}: {c[1]} (owner {c[2]}, due {c[3]}); status at closure: {c[4]}.", [ref("capa", row, ca_t, carow)])

    # -- Effectiveness check
    sq("eff", """The actions are checked for effectiveness by `{python} EFFECTIVENESS2["due"]`.""")
    for i, item in enumerate(ns["eff_items"]):
        st("eff", f"Effectiveness check, part {i + 1}: {item}", [ref("eff", _smart(item))])
    sq("eff", "The second part asks for the three tests that this investigation applies",
       "The second part of the effectiveness check asks for the three tests that this investigation applies.")
    sq("eff", "Under a correct model each confirmation run falls inside its 95 % prediction interval with a probability of `{python} f2(cover)`, and the number inside follows a binomial distribution.")
    sq("eff", """With `{python} eff_n` confirmation runs at least `{python} binom_min(eff_n)` must fall inside, and with `{python} eff_n2` at least `{python} binom_min(eff_n2)`.""")
    sq("eff", "Applied to the augmentation runs of this investigation, the binomial test rejects the models of high mannose and aggregates at the production bioreactor that were selected on the planned runs")

    # -- Conclusion and closure
    st("close", q("""The investigation confirmed the classification as `{python} INV2["classification"]`, on the grounds recorded when it was opened."""), [ref("close", q_conf)])
    st("close", "No range was set from a failing model at Version 2.0.", [ref("close", q_norange)])
    sq("close", "The root cause is that the plans prescribed the full quadratic model as the predictive model, with no model selection, on designs that are small for it.")
    sq("close", """A remedy was assigned to every failing model by a rule approved before any new run, and both augmentations were run by `{python} last_end`.""")
    sq("close", "Model selection then replaced the refits for every output.")
    sq("close", """After selection `{python} n_none_sel` outputs have no adequate model, and every measured result of these outputs meets its criterion.""")
    sq("close", "The intermediate acceptance criteria in force were fixed on the selected models at the closure of the investigation into acceptance criteria set after the data were seen (INV-001).")
    sq("close", """Against the criteria that the full quadratic models give, model selection made `{python} n_wider` intermediate acceptance criteria wider and kept the upper limit of acidic variants at the production bioreactor at its a priori value.""")
    sq("close", "No conclusion over the NOR depends on that difference, and one proven acceptable range moves at its lower end, outside the NOR.")
    sq("close", "The qualification of the scale-down model for host cell protein in the Protein A pool and at cation exchange does depend on it.",
       "The qualification of the scale-down model for host cell protein in the Protein A pool and at cation exchange does depend on the difference between the criteria with and without model selection.")
    sq("close", "At closure the augmentation runs of corrective action CA1 and the refits of corrective action CA2 were complete.")
    sq("close", """The re-evaluation on all runs of CA1 and the application of model selection, corrective action CA3, in the Version 2.0 reports were open, due on `{python} capa.loc["CA3", "due"]`.""")
    sq("close", "The preventive actions were open.")
    st("close", q("""INV-002 was closed on `{python} INV2["closed"]`."""), [ref("close", q_closed)])

    order = list(dict.fromkeys(path[0] for path in SEC.values()))
    sections = []
    for title in order:
        stmts = [s_ for t_, s_ in ST if t_ == title]
        if stmts:
            sections.append(ReportSection(section_id=f"{DOC}-sec{len(sections) + 1:02d}", title=title,
                                          statements=stmts))

    # ==== acceptance criteria: the criteria in force that the document prints ======================
    acrit = []
    for key, (c, label, r_) in crit_txt.items():
        k, resp = key
        # the calls the document makes: ipc_limit for the sensitivity table, effective_acceptance for
        # the measured-results table and for the claim of low-pH viral inactivation
        lo, hi, stype = (D.ipc_limit if key in serow else D.effective_acceptance)(k, resp)
        same = (abs(float(lo) - float(ns["claim6"])) < 1e-9 if key == (vk, vr) else T.crit(lo, hi, stype) == c)
        if not same:          # each record states the criterion its anchor prints
            raise ValueError(f"{DOC}: criterion of {key} is not the printed {c!r}")
        acrit.append(S.AcceptanceCriterionRecord(
            step=k, attribute=cqa_of[key], low=None if stype == "upper" else float(lo),
            high=None if stype == "lower" else float(hi), unit=unit_of(cqa_of[key]), basis=basis_of[key],
            revision=P.REV2["rev"], status="in force", source=r_))

    # ==== concepts ================================================================================
    params_used = list(dict.fromkeys(
        [(a_.subject_id if a_.subject_id.startswith("param:") else a_.object_id) for a_ in A
         if a_.subject_id.startswith("param:") or a_.object_id.startswith("param:")]
        + [p for s_ in studies for p in s_.associated_parameters]))
    pkey = {pconcept(k, p.key): (k, p.key) for k in steps_all for p in CFG.unit_op(k).parameters}
    concepts = [Concept(concept_id="process:amab_ds", concept_type="PROCESS",
                        canonical_name="A-Mab drug-substance process", review_status="human_verified")]
    concepts += [Concept(concept_id=f"step:{k}", concept_type="PROCESS_STEP", canonical_name=UO[k],
                         aliases=[T.STEP_NAME[k]], review_status="human_verified") for k in CFG.train_order]
    names = dict(zip(P.cqa_reg["key"], P.cqa_reg["cqa"]))
    concepts += [Concept(concept_id=f"attr:{a}", concept_type="QUALITY_ATTRIBUTE", canonical_name=names.get(a, a),
                         aliases=[a, attr_name(a)], review_status="human_verified") for a in attr_keys]
    concepts.append(Concept(concept_id="attr:step_yield", concept_type="PERFORMANCE_ATTRIBUTE",
                            canonical_name="Step yield", aliases=["step yield"], review_status="human_verified"))
    concepts += [Concept(concept_id=c_, concept_type="PROCESS_PARAMETER", canonical_name=pname(*pkey[c_]),
                         aliases=[f"{pname(*pkey[c_])} ({T.STEP_NAME[pkey[c_][0]]})"], review_status="human_verified")
                 for c_ in params_used]
    concepts += [Concept(concept_id=f"method:{m.method_id}", concept_type="ANALYTICAL_METHOD",
                         canonical_name=m.method_name, aliases=[m.method_id], review_status="human_verified")
                 for m in methods]

    # ==== the annex ===============================================================================
    if normalize(CELL_SEP.join(["Supersedes", "—"])) not in text:
        raise ValueError(f"{DOC}: the title block no longer reads 'Supersedes | —'")
    layer = G.rev2_layer(DOC, FILE)
    layer["supersedes"] = None   # new in the Version 2.0 package: revision_layer special-cases INV-001 only
    annex = S.GroundTruthAnnex(
        document_id=DOC, document_title=f"{P.DOC_REGISTRY[DOC][0]} — {P.DOC_REGISTRY[DOC][1]}",
        document_class=P.DOC_REGISTRY[DOC][0], **layer,
        schema_extensions_used=G.COMMON_EXT + G.REV2_EXT + [
            "DocumentInventoryItem.predicted_document_type: investigation_report added"],
        out_of_schema_notes=[
            "The finding, the root cause and its contributing cause, the remedy rule, the sample-size "
            "calculation, the model selection procedure, the impact assessment, the effectiveness check and the "
            "closure have no schema model; they are report_sections statements, one section per top-level section "
            "of the document. Each row of the chronology, scope, remedy, sample-size, power, augmentation-check, "
            "measured-results, impact, criteria, sensitivity and CAPA tables is a statement anchored on its own "
            "row. Where a continuation row reads exactly like another one (two remedy rows, two power rows), the "
            "statement also cites the row that opens its merged group.",
            "Every model the document prints is a StatisticalModelFit: the full quadratic of the planned runs "
            "(Table 3, as Version 1.0 fitted it, Protein A run 23 at its design pH) and, from the prose, the same "
            "model of pool host cell protein with run 23 at its recorded pH; the model selected under corrective "
            "action CA3 for every output (Table 9); the selected models of the three augmented outputs on the "
            "planned runs and on all runs (Table 10, with their terms); and, from the prose, the full quadratic "
            "with a block term on all runs that each augmentation was sized for. The schema has no field for R² "
            "minus predicted R², the number of terms or the scale; they are in model_form and adequacy_statement. "
            "Numeric fields carry the values as printed; a p-value printed as '<0.001' or 'n.t.' is empty.",
            "The model-adequacy finding is the Deviation record INV-002 (the investigation itself, as INV-001 "
            "records itself). DEV-005-01, the deviation of PCR-005 that INV-002 cites for Protein A run 23, is a "
            "second Deviation record. The plan discrepancies the document names (PD-003-02, PD-003-03, PD-005-02, "
            "PD-005-03, PD-005-04, PD-006-04, PD-007-01, PD-008-01, PD-008-02, PD-009-01) have no schema record; "
            "they are in the document relationships to the reports that record them and in the statements of the "
            "impact table.",
            "studies holds the six planned response-surface designs (one per row of the scope table, with their "
            "runs and centre points; the study ids are those of the chronology) and the two D-optimal "
            "augmentations, each anchored on its chronology rows, its prose and every row of its design table. The "
            "augmentation is a second block of the response-surface design and has no study type of its own; it "
            "carries no n_runs, which the corpus test reserves for the seeded screening and response-surface "
            "designs, and its run count is in design_name. Only the augmentation design tables name every factor "
            "of a design, so only the augmentation records carry factors.",
            "acceptance_criteria holds the criteria in force that the document prints: the five of the sensitivity "
            "table, the four judged on measured results, and the platform claim of low-pH viral inactivation for "
            "XMuLV clearance. The criteria 'without model selection' are what a verification on the full quadratic "
            "models would have given and were never in force; they are in the statements of the criteria and "
            "sensitivity tables. INV-002 prints no criteria-change table, so it has no superseded record. The "
            "QualityAttribute records list the same criteria and the drug substance limits the document states; "
            "their attribute_type comes from the CQA register, which INV-002 does not restate.",
            "The proven acceptable range the document reports as moving (the lower end of elution buffer pH for "
            "pool host cell protein, in force and without model selection) is a statement and a row of the "
            "sensitivity table, not a ProvenAcceptableRange: the document gives its lower end only.",
            "Parameters have no register in INV-002 and no ProcessParameter record. The parameter effects it "
            "states are assertions on the row or clause that states each: the terms of the selected models of all "
            "runs of the augmented outputs (Table 10), the fold changes of pool host cell protein (§8.2), the terms "
            "of the aggregate model of low-pH viral inactivation (§8.4) and the main effects of its XMuLV model "
            "(§9.2).",
            "supersedes is empty: INV-002 is new in the Version 2.0 package and its title block reads "
            "'Supersedes —'.",
            "No rhetorical_spans (an investigation has no spans file). weak_claims is empty.",
        ],
        inventory=G.rev2_inventory(DOC, FILE, "investigation_report", "A-Mab drug substance",
                                   ["investigation", "model adequacy", "response-surface models", "root cause",
                                    "remedy rule", "sample-size calculation", "D-optimal augmentation",
                                    "model selection", "Box-Cox transformation", "AICc", "CAPA",
                                    "intermediate acceptance criteria", "worst-case verification",
                                    "scale-down model qualification"]),
        entities=entities, studies=studies, report_sections=sections,
        assertions=AssertionStore(run_id=f"gt-{DOC}", assertions=A, rationales=[]),
        concepts=ConceptStore(run_id=f"gt-{DOC}", concepts=concepts),
        weak_claims=[], rhetorical_spans=[], acceptance_criteria=acrit)
    _gate(annex, text)
    return annex
