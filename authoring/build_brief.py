#!/usr/bin/env python3
"""Generate the grounded authoring brief for one A-Mab characterization document.

    uv run python authoring/build_brief.py PCR-003
    uv run python authoring/build_brief.py PCR-003 PCP-003 PCR-008 ...

Writes ``authoring/out/<DOC>.brief.md`` — the single author's grounded fact sheet and,
crucially, the **helper inventory**: the exact callables that turn the seeded model into
inline expressions. Every number in the authored document comes from here; without it the
author emits ``<<NEEDS:>>``.

The brief is generated from ``config`` -> the model -> ``outputs/`` via the ``_pcpkg`` /
``doe_report`` helpers ONLY. It never reads a ``pc_package/*.qmd``: the corpus reports are
prior knowledge (distilled once into ``authoring/``), not a runtime dependency. The
pipeline therefore runs on a blank repo with no first-pass documents present.
"""
from __future__ import annotations

import inspect
import io
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PCPKG = os.path.join(ROOT, "pc_package")
OUT = os.path.join(HERE, "out")
if PCPKG not in sys.path:
    sys.path.insert(0, PCPKG)

import _pcpkg as P          # noqa: E402
import doe_report as D      # noqa: E402
from amab_process import studies as st  # noqa: E402

# Steps with a DoE (CLAUDE.md). Detected primarily from data; this is the fallback.
DOE_KEYS = {"bioreactor", "protein_a", "viral_inactivation", "cex", "aex",
            "virus_filtration"}

# Per-step controlled-document list prefixes in _pcpkg (irregular; bioreactor uses the
# package defaults SOP_REFS / AMV_REFS). Infra config, not a document value.
SOP_PREFIX_BY_KEY = {
    "harvest": "HARVEST", "protein_a": "PROTEIN_A", "viral_inactivation": "VIRAL_INACT",
    "cex": "CEX", "aex": "AEX", "virus_filtration": "VIRUS_FILT", "ufdf": "UFDF",
}

# Response -> CQA-register key hint, to suggest a cqas_by_keys([...]) selection for a
# clearance step. A DISPLAY AID only (marked "verify" in the brief); the author confirms
# the governed set from the story bible and the CQA register.
RESP_TO_CQA = {
    "hcp_out_ng_mg": "hcp", "pool_hcp_ng_mg": "hcp", "xmulv_lrf": "lrv_xmulv",
    "mvm_lrf": "lrv_mvm", "leached_protein_a_ppm": "leached_protein_a",
    "aggregate_out_pct": "aggregates_hmw", "residual_dna": "residual_dna",
}


def _load_config_deviations():
    cfg = yaml.safe_load(open(os.path.join(ROOT, "config", "parameters.yaml")))
    return cfg.get("deviations", {})


def _is_doe(key):
    if key is None:
        return False
    try:
        return P.doe_runs(key, "screening") > 0
    except Exception:
        return key in DOE_KEYS


def _superseded_kinds(key):
    """Kinds ('screening'/'rsm') for which a REAL superseded first-execution dataset
    exists (outputs/data/doe_<key>_<kind>_superseded.csv). Empty until a re-executed
    deviation is seeded (task 9)."""
    if key is None:
        return []
    found = []
    for kind in ("screening", "rsm"):
        f = os.path.join(P.DATA, f"doe_{key}_{kind}_superseded.csv")
        if os.path.exists(f):
            found.append(kind)
    return found


def _md_table_or_note(md, empty="_(none)_"):
    return md if (md and md.strip()) else empty


# Helpers that return a pre-rendered markdown STRING (print() them under `#| output: asis`)
# rather than a DataFrame (which is emitted with show()). Mixing these up is a common trap.
STRING_HELPERS = {"title_block", "related_docs_md", "sop_table", "corpus_docs_md",
                  "dev_register"}


# Authors look for a capability, not a name. The alphabetical listing below answers
# "what does `par_nor_propagated` do?" but not "how do I check a worst-case corner?" —
# and the second question is the one that gets asked. Every helper is still listed in
# full afterwards; this is an index into it, by the job the author is trying to do.
HELPERS_BY_JOB = [
    ("Predict a response where the design did not run — a worst-case corner, a NOR edge, "
     "an edge-of-failure scan", [
        ("D.predict(key, resp, coded={..}|natural={..})", "the fitted model at your settings"),
        ("D.to_coded(key, factor, value)", "natural units to coded, and to_natural back"),
        ("D.meets_acceptance(key, resp, values)", "does each prediction meet the criterion"),
     ]),
    ("State what a response must achieve", [
        ("D.acceptance_for(key, resp)",
         "back-calculates the STEP floor for a viral response; never hand-calculate one"),
     ]),
    ("Show a design matrix in a PROTOCOL, where no result may appear", [
        ("D.planned_matrix_df(key, kind, coded=True)", "response columns stripped"),
     ]),
    ("Show the design and the effects in a REPORT", [
        ("D.coded_matrix_df / D.design_matrix_df", "appendix matrices, responses included"),
        ("D.screening_effects_df / D.rsm_coeff_df", "effects and coefficients"),
        ("D.fit_summary_df / D.anova_lof_df", "model adequacy and lack of fit"),
        ("D.center_cv_df(key, kind)", "centre-point reproducibility, the pure-error term"),
     ]),
    ("Report proven acceptable ranges", [
        ("D.par_table(key)", "per CQA x factor, both analyses"),
        ("D.governing_factor(key, resp)", "the factor with the largest RSM main effect"),
        ("D.fig_par(key, resp, factor)", "green-shaded acceptable region"),
        ("D.par_at_design_centre(...)",
         "holds the OTHER factors at the range MIDPOINT, not the set-point — read "
         "authoring/DISCREPANCIES.md D-001 before describing it"),
     ]),
    ("Parameters, ranges and classification", [
        ("plan_params(key)", "PROSPECTIVE: no classification, for a PCP"),
        ("report_params(key)", "includes the outcome classification, for a PCR"),
        ("CFG.unit_op(key).param(name)", ".setpoint / .nor / .prange"),
     ]),
    ("Quality attributes", [
        ("cqas_for(key)", "only what the step SETS — empty for most downstream steps"),
        ("cqas_by_keys([..])", "what the step controls or clears; use this downstream"),
        ("all_cqas()", "the whole register, for a corpus-level document"),
     ]),
    ("Capability", [
        ("cap_for([keys])", "one-sided Cpk per CQA"),
        ("V['min_cpk']", "a RESULT. No grounded acceptance threshold exists — do not invent one"),
     ]),
    ("Deviations", [
        ("dev_register(doc_id)", "markdown STRING — print() it, do not show() it"),
        ("dev_facts(doc_id)", "structured rows"),
        ("dev_* module scalars", "the magnitudes, already grounded"),
     ]),
    ("Cross-references and controlled documents", [
        ("related_docs_md(doc) / corpus_docs_md(doc)", "markdown STRINGs — print() them"),
        ("sop_table(sops, amvs)", "per step; all_sop_table() for the campaign-wide register"),
     ]),
    ("Corpus-level tables, for the parent documents", [
        ("process_steps_df()", "the train and each step's role"),
        ("char_scope_df()", "parameters and study-type split per step"),
        ("equipment_df()", "instrumented scale-down systems"),
     ]),
]


def _weak_claim_assignments(doc_id: str) -> str:
    """The labeled benchmark negatives this document is assigned, if any.

    Surfaced to the author BEFORE writing, which is the whole point. The previous design
    planted these into finished documents, where a claim cannot be merely unsupported —
    it lands in prose that has already settled the question and so reads as a
    contradiction of its neighbour. Written in one pass instead, the surrounding argument
    accommodates the claim and it stays an overreach rather than a self-contradiction.
    See authoring/WEAK_CLAIMS.md.
    """
    path = os.path.join(HERE, "weak_claims.yaml")
    if not os.path.exists(path):
        return ""
    with open(path) as fh:
        data = yaml.safe_load(fh) or {}
    claims = (data.get("claims") or {}).get(doc_id) or []
    if not claims:
        return ""

    b = io.StringIO()
    b.write("## 5b. Assigned weak claims — WRITE THESE, and nothing else ungrounded\n\n")
    b.write("> This document carries labeled benchmark negatives. They are the **only** "
            "ungrounded claims you may write; every other claim must be fully supported "
            "(WRITING_GUIDE §7a).\n>\n"
            "> Each must end up **unsupported, not contradicted**. Write it into the "
            "argument so the surrounding prose accommodates it.\n>\n"
            "> **Move the claim, never the document.** If a neighbouring sentence rebuts "
            "it, relocate the claim. Do not soften the neighbour, do not delete a grounded "
            "statement, and do not remove a citation elsewhere to make an uncited claim "
            "blend. Smoothing the document around a planted claim turns a local negative "
            "into a diffuse weakening of the report, which is worse than the problem this "
            "design exists to solve. If you do change anything in service of the claim, "
            "say so in your report so it can be checked on its own merits.\n>\n"
            "> It must read as ordinary in-register prose. A negative a reader spots by "
            "style rather than by checking the evidence is worthless.\n\n")
    for c in claims:
        a = c.get("assignment") or {}
        b.write(f"### {c['id']} — `{c['weakness_type']}` (section: {c.get('section', '?')})\n\n")
        b.write(f"- **The grounded fact it distorts:** {' '.join((a.get('distorts') or '').split())}\n")
        b.write(f"- **Write:** {' '.join((a.get('write') or '').split())}\n")
        b.write(f"- **Placement:** {' '.join((a.get('placement') or '').split())}\n\n")
    b.write("Do not mark these in the text in any way. After the document renders, the "
            "maintainer records your exact wording in the registry so the annex can label "
            "it — that step reads the document, it never edits it.\n\n")
    return b.getvalue()


def _discrepancy_assignments(doc_id: str) -> str:
    """The registered discrepancies this document is required to carry, if any.

    A registered discrepancy lives in prose, so it survives only as long as nobody
    re-authors the document holding it. D-002 did not survive: PCR-003 was re-authored, the
    sentence was not written again, and authoring/DISCREPANCIES.md went on calling the item
    open. Nothing failed, because no gate reads that registry.

    Surfacing the assignment here puts these on the same footing as the weak claims: named
    before the document is written, so the author builds them into the argument, and never
    restored afterwards. See authoring/discrepancies.yaml.
    """
    path = os.path.join(HERE, "discrepancies.yaml")
    if not os.path.exists(path):
        return ""
    with open(path) as fh:
        data = yaml.safe_load(fh) or {}
    items = (data.get("items") or {}).get(doc_id) or []
    if not items:
        return ""

    b = io.StringIO()
    b.write("## 5c. Registered discrepancies — this document must carry these\n\n")
    b.write("> `authoring/DISCREPANCIES.md` registers a small number of **genuine "
            "inconsistencies** that a competent review should catch. They are deliberate "
            "benchmark items, and each one lives in the prose of a particular document. "
            "Yours carries the following.\n>\n"
            "> Write each in your own words, in register, where the assignment says. Then "
            "leave it alone. **Do not reconcile it** with another document, with the data, "
            "or with a later section of your own report, and do not qualify it into "
            "something true. Correcting one deletes a benchmark item.\n>\n"
            "> This is not the weak-claims layer. These are not labeled in the annex, so "
            "nothing in the document or its ground truth reveals them.\n\n")
    for it in items:
        a = it.get("assignment") or {}
        b.write(f"### {it['id']} — `{it.get('kind', '?')}`\n\n")
        b.write(f"- **State:** {' '.join((a.get('state') or '').split())}\n")
        if a.get("write_next"):
            b.write(f"- **Then write:** {' '.join(a['write_next'].split())}\n")
        b.write(f"- **Why it is there:** {' '.join((a.get('why') or '').split())}\n")
        b.write(f"- **Placement:** {' '.join((a.get('placement') or '').split())}\n")
        if a.get("do_not"):
            b.write(f"- **Do not:** {' '.join(a['do_not'].split())}\n")
        b.write("\n")
    return b.getvalue()


def _helper_by_job():
    out = ["**Find a helper by the job you are doing.** The full alphabetical listing "
           "follows; this is an index into it.\n"]
    for job, calls in HELPERS_BY_JOB:
        out.append(f"- **{job}**")
        for call, note in calls:
            out.append(f"    - `{call}` — {note}")
    return "\n".join(out) + "\n\n"


def _helper_lines(module, mod_name, prefix=""):
    lines = []
    for name, obj in sorted(vars(module).items()):
        if name.startswith("_") or not inspect.isfunction(obj):
            continue
        if getattr(obj, "__module__", None) != mod_name:
            continue
        try:
            sig = str(inspect.signature(obj))
        except (ValueError, TypeError):
            sig = "(...)"
        doc = (inspect.getdoc(obj) or "").strip().split("\n")[0]
        tag = ("  ⟶ returns a markdown STRING — `print()` it (NOT `show()`)"
               if name in STRING_HELPERS else "")
        lines.append(f"- `{prefix}{name}{sig}` — {doc}{tag}" if doc
                     else f"- `{prefix}{name}{sig}`{tag}")
    return lines


def build(doc_id: str) -> str:
    if doc_id not in P.DOC_REGISTRY:
        raise SystemExit(f"unknown document id: {doc_id} (see _pcpkg.DOC_REGISTRY)")
    cls, subject, key = P.DOC_REGISTRY[doc_id]
    is_report = doc_id.startswith("PCR-")
    is_plan = doc_id.startswith("PCP-")
    step = int(doc_id.split("-")[1]) if doc_id[:4] in ("PCP-", "PCR-") else None
    uo_title = None
    role = None
    if key is not None:
        uo = P.CFG.unit_op(key)
        uo_title = f"{P.UNIT_OP_TITLES.get(key, uo.name)} (Step {uo.step})"
        role = P.UNIT_OP_ROLE.get(key, "")
    doe = _is_doe(key)
    superseded = _superseded_kinds(key)

    b = io.StringIO()
    w = b.write

    w(f"# Authoring brief — {doc_id}: {subject}\n\n")
    w("> Generated by `authoring/build_brief.py` from config -> model -> outputs via "
      "`_pcpkg`/`doe_report`. **Do not edit.** Every number in the document is an inline "
      "`{python}` expression built from the helper inventory (§7), never typed "
      "(WRITING_GUIDE §6). Bound to the author with `WRITING_GUIDE.md`, `section_plan.yaml`, "
      "`REGISTER_EXEMPLAR.md`, `STORY_BIBLE.md`.\n>\n"
      "> **This brief is a data sheet, not a style model.** It is written in terse note form "
      "with dashes, bold labels and fragments because it is a lookup table. The report's prose "
      "must not read like it. For voice, use `REGISTER_EXEMPLAR.md` (verbatim passages from "
      "PDA TR 60 and the A-Mab case study) and the measurable targets in WRITING_GUIDE §4.\n\n")

    # 1. Identity ---------------------------------------------------------------
    w("## 1. Identity\n\n")
    w(f"- **Document:** {doc_id} — {cls}\n")
    w(f"- **Subject:** {subject}\n")
    if key is not None:
        w(f"- **Unit operation:** {uo_title} · key `{key}`\n")
        w(f"- **Role in control strategy:** {role}\n")
        w(f"- **DoE step:** {'yes' if doe else 'no (univariate / qualitative — do NOT fabricate a DoE)'}\n")
    else:
        w("- **Scope:** corpus-level document (no single unit operation)\n")
    # Which outline in section_plan.yaml this document follows. The corpus-level documents
    # each have their own, and saying "n/a" here left four authors to guess.
    CORPUS_OUTLINE = {"PTP-001": "transfer_plan", "RA-001": "risk_assessment",
                      "PCMP-001": "master_plan", "PCMR-001": "master_report"}
    outline = ("report_doe" if (is_report and doe) else "report_nondoe" if is_report
               else "plan" if is_plan else CORPUS_OUTLINE.get(doc_id, "n/a"))
    w(f"- **Doc-type outline:** `section_plan.yaml` -> `{outline}`\n")
    if superseded:
        w(f"- **Superseded study present:** yes — real re-executed dataset(s) for "
          f"{', '.join(superseded)} (see §5). Reference it; analyse the requalified data.\n")
    w("\n")

    # 2. CQAs -------------------------------------------------------------------
    if key is not None:
        w("## 2. Quality attributes\n\n")
        w("### CQAs this step SETS — `cqas_for(\"%s\")`\n\n" % key)
        w(_md_table_or_note(P.cqas_for(key).to_markdown(index=False),
                            "_(sets no CQA of its own — a clearance/polish step; select "
                            "the governed CQAs with `cqas_by_keys([...])`)_") + "\n\n")
        if doe:
            w("### DoE responses measured — `D.responses(\"%s\")`\n\n" % key)
            for r in D.responses(key):
                hint = RESP_TO_CQA.get(r)
                w(f"- `{r}` → **{D.RESP_LABEL.get(r, r)}**"
                  + (f"  · suggests CQA key `{hint}` (verify)\n" if hint else "\n"))
            w("\n")
        w("### CQA register — keys for `cqas_by_keys([...])` and `cap_for([...])`\n\n")
        reg = P.cqa_reg[["key", "cqa", "set_by", "criticality"]].copy()
        w(reg.to_markdown(index=False) + "\n\n")

    # 3. Parameters -------------------------------------------------------------
    if key is not None:
        w("## 3. Parameters\n\n")
        if is_plan:
            w("`plan_params(\"%s\")` (Range studied + NOR + study type; NO classification):\n\n" % key)
            w(P.plan_params(key).to_markdown(index=False) + "\n\n")
        else:
            w("`report_params(\"%s\")` (set-point, NOR, PAR, final class, study):\n\n" % key)
            w(P.report_params(key).to_markdown(index=False) + "\n\n")

    # 4. DoE structure ----------------------------------------------------------
    if key is not None and doe:
        w("## 4. DoE structure\n\n")
        w(f"- **Screening factors** (`st.DOE_FACTORS`): {st.DOE_FACTORS[key]}\n")
        w(f"- **RSM factors** (`st.RSM_TOP` / first-4 default): {D.rsm_factors(key)}\n")
        w(f"- **Responses** (`st.DOE_RESPONSES`): {st.DOE_RESPONSES[key]}\n")
        w(f"- **Run counts:** screening = `doe_runs(\"{key}\",\"screening\")` "
          f"= {P.doe_runs(key, 'screening')}; rsm = `doe_runs(\"{key}\",\"rsm\")` "
          f"= {P.doe_runs(key, 'rsm')}\n")
        w("- **Factor legend (coded A–…):**\n\n")
        w(D.factor_legend_df(key).to_markdown(index=False) + "\n\n")

    # 4b. Proven acceptable ranges (computed live by doe_report) -----------------
    if key is not None and doe:
        w("## 4b. Proven acceptable ranges (computed)\n\n")
        w("Acceptance = the study drug-substance specs (impurities / formed CQAs); a "
          "viral-clearance CQA uses the back-calculated step floor (cumulative requirement "
          "minus the other steps' credited clearance). `D.acceptance_for(UO, resp)` returns "
          "the right criterion. Two flavours per CQA×parameter — at set-point and "
          "NOR-propagated (Monte-Carlo of the fitted model). Table: `D.par_table(UO)`; plot a "
          "governed CQA with `D.fig_par(UO, resp, D.governing_factor(UO, resp))` "
          "(parameter x, response y, acceptable region shaded green, set-point + NOR marked).\n\n")
        try:
            w(D.par_table(key).to_markdown(index=False) + "\n\n")
            gov = {r: D.governing_factor(key, r) for r in D.responses(key)
                   if D.acceptance_for(key, r) is not None}
            if gov:
                w("Governing factor per governed CQA (representative plot): "
                  + ", ".join(f"`{r}`→`{f}`" for r, f in gov.items()) + "\n\n")
        except Exception as e:  # noqa: BLE001
            w(f"_(PAR table unavailable: {e})_\n\n")

    # 5. Deviations -------------------------------------------------------------
    w("## 5. Deviations — structured facts (author writes the prose; Option A)\n\n")
    reg_md = P.dev_register(doc_id)
    if not reg_md.strip():
        w("_No seeded deviations for this document._\n\n")
    else:
        w("Register — `dev_register(\"%s\")`:\n\n" % doc_id)
        w(reg_md + "\n\n")
        events = _load_config_deviations().get("events", {}).get(doc_id, [])
        if events:
            w("Structured facts (from `config/parameters.yaml` `deviations.events`; the "
              "canonical single source — the author writes the investigation prose from "
              "these, numbers via the scalars below):\n\n")
            for e in events:
                w(f"- **{e.get('id')}** — {e.get('summary','')}\n")
                for fld in ("type", "detected_during", "root_cause", "disposition",
                            "equipment", "lot", "method", "superseded"):
                    if fld in e:
                        w(f"    - {fld}: `{e[fld]}`\n")
                if e.get("values"):
                    w(f"    - values: {e['values']}\n")
            w("\n")
        # dev_* scalars exposed as module globals for THIS doc. Naming rule (_pcpkg):
        # scalar = <dev-id>.lower().replace('-','_') + '_' + <field>, e.g. DEV-003-01 ->
        # dev_003_01_offset_mmhg. Match by the doc's deviation-id prefixes.
        dev_prefixes = tuple(
            e.get("id", "").lower().replace("-", "_") + "_"
            for e in _load_config_deviations().get("events", {}).get(doc_id, [])
            if e.get("id"))
        scal = {n: v for n, v in P.DEV_SCALARS.items()
                if dev_prefixes and n.startswith(dev_prefixes)}
        if scal:
            w("Deviation scalars available as inline expressions (module globals — "
              "`` `{python} <name>` ``):\n\n")
            for n, v in sorted(scal.items()):
                w(f"- `{n}` = {v}\n")
            w("\n")
    if superseded:
        w("### Superseded study (real re-executed dataset)\n\n")
        w("A deviation invalidated the first execution and it was re-run. The first-"
          "execution data are seeded and exposed for reference (root-cause confirmation), "
          "**not** for the reported analysis:\n\n")
        for kind in superseded:
            w(f"- `doe_{key}_{kind}_superseded.csv` — first (invalidated) {kind} execution; "
              f"compare against the reported `doe_{key}_{kind}.csv` via the `_superseded` "
              f"helper variants (§7). State the anomaly, that designs were invalidated and "
              f"re-executed, and confirm root cause from the requalified data.\n")
        w("\n")

    # 6. Cross-references -------------------------------------------------------
    w(_weak_claim_assignments(doc_id))
    w(_discrepancy_assignments(doc_id))
    w("## 6. Cross-references\n\n")
    if step is not None:
        w("Related documents — `related_docs_md(\"%s\")`:\n\n" % doc_id)
        w(P.related_docs_md(doc_id) + "\n\n")
    else:
        w("Corpus documents — `corpus_docs_md(\"%s\")`:\n\n" % doc_id)
        w(P.corpus_docs_md(doc_id) + "\n\n")
    if key is not None:
        prefix = SOP_PREFIX_BY_KEY.get(key)
        sops = getattr(P, f"{prefix}_SOP_REFS", P.SOP_REFS) if prefix else P.SOP_REFS
        amvs = getattr(P, f"{prefix}_AMV_REFS", P.AMV_REFS) if prefix else P.AMV_REFS
        sop_name = f"{prefix}_SOP_REFS" if prefix else "SOP_REFS"
        amv_name = f"{prefix}_AMV_REFS" if prefix else "AMV_REFS"
        w(f"SOP/AMV subset for this step — `sop_table(sops={sop_name}, amvs={amv_name})`:\n\n")
        w(P.sop_table(sops=sops, amvs=amvs) + "\n\n")

    # 7. Helper inventory -------------------------------------------------------
    w("## 7. Helper inventory — pull numbers through these (the menu)\n\n")
    w(_helper_by_job())
    w("Import in the setup chunk: `from _pcpkg import *` and `import doe_report as D`. "
      "Every measurement is a `` `{python} EXPR` `` inline expression or a helper call "
      "printed under `#| output: asis`. Identifiers (SOP/AMV/doc IDs, ICH names, coded "
      "levels) are written plainly.\n\n")
    w("### `_pcpkg` (imported flat)\n\n")
    w("\n".join(_helper_lines(P, "_pcpkg")) + "\n\n")
    w("### `doe_report` (import as `D`)\n\n")
    w("\n".join(_helper_lines(D, "doe_report", prefix="D.")) + "\n\n")
    w("### Constants & globals\n\n")
    w("- `SYN_BANNER`, `PRODUCT`, `COMPANY`, `EFFECTIVE_DATE`, `VERSION` — front-matter.\n")
    w("- `V` — `outputs/report_values.json` dict (e.g. `` `{python} f\"{V['n_monte_carlo']:,}\"` ``).\n")
    w("- `CFG` — config; `CFG.unit_op(key).param(name).nor` / `.prange` for NOR/PAR edges.\n")
    w("- `D.RESP_LABEL` — response-key → display label.\n")
    if key is not None:
        w("- `cqas_for`/`cqas_by_keys`/`cap_for` return DataFrames; emit with "
          "`show(df, floatfmt=...)` under `#| output: asis`.\n")
    w("\n---\n_Generated by build_brief.py — regenerate after any config/model change._\n")

    return b.getvalue()


def main(argv):
    if len(argv) < 2:
        raise SystemExit(__doc__)
    os.makedirs(OUT, exist_ok=True)
    for doc_id in argv[1:]:
        text = build(doc_id)
        path = os.path.join(OUT, f"{doc_id}.brief.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"wrote {os.path.relpath(path, ROOT)}  ({len(text):,} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
