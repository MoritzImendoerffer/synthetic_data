#!/usr/bin/env python3
"""Generate the grounded authoring brief for one A-Mab characterization document.

    uv run python authoring/build_brief.py PCR-003
    uv run python authoring/build_brief.py PCR-003 PCP-003 PCR-008 ...

Writes ``authoring/out/<DOC>.brief.md`` — the single author's grounded fact sheet and,
crucially, the **helper inventory**: the exact callables that turn the seeded model into
inline expressions. Every number in the authored document comes from here; without it the
author emits ``<<NEEDS:>>``.

The brief is generated from ``config`` -> the model -> ``outputs/`` via the ``_pcpkg`` /
``doe_report`` helpers ONLY. It never reads a ``pc_package/*.qmd`` for content: the corpus
reports are prior knowledge (distilled once into ``authoring/``), not a runtime dependency.
Under --review only (since 2026-08-19) §5d measures the previous revision's register (numbers only, through
``check_style.measure``) so the author starts knowing where it stood; on a blank repo it
prints "no previous revision". The pipeline therefore runs on a blank repo with no
first-pass documents present.
"""
from __future__ import annotations

import glob
import inspect
import io
import json
import os
import subprocess
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PCPKG = os.path.join(ROOT, "pc_package")
OUT = os.path.join(HERE, "out")
if PCPKG not in sys.path:
    sys.path.insert(0, PCPKG)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import _pcpkg as P          # noqa: E402
import check_style as cs    # noqa: E402
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


# The four source columns of the register measures. Read through check_style so the brief
# cannot drift from the gate; check_style prints the packing figures on every run.
def _register_columns() -> dict:
    cols = {}
    for name, fname, lo, hi in cs.HUMAN_SOURCES:
        path = os.path.join(ROOT, "refs", "text", fname)
        if os.path.exists(path):
            cols[name] = cs.measure(cs.prose_from_extract(path, lo, hi))[0]
    return cols


def _previous_revision_path(doc_id: str, key) -> str | None:
    """This document's committed source, or None. Used ONLY to measure its register.

    Not a content input and not a voice model: §5d prints numbers from it and never a word
    of its prose. On a blank repo there is nothing here and the section says so.
    """
    if key is not None:
        p = os.path.join(PCPKG, f"{doc_id}_{key}.qmd")
        return p if os.path.exists(p) else None
    hits = sorted(glob.glob(os.path.join(PCPKG, f"{doc_id}_*.qmd")))
    return hits[0] if hits else None


def _discourse_measures(path: str | None) -> tuple[dict, dict | None]:
    """``check_discourse.py --json --cap``: the four source columns and this document.

    Measured live rather than carried as constants, so the row cannot go stale against a
    re-extraction of the sources. One subprocess covers all five columns; it costs about 35 s
    of parsing per brief, which is the price of the numbers being current.

    Returns ({} , None) when spaCy is absent — the extra is optional and the brief still
    builds (CLAUDE.md, Environment).
    """
    argv = [sys.executable, os.path.join(HERE, "check_discourse.py"), "--json", "--cap"]
    out = subprocess.run(argv + ([path] if path else []),
                         capture_output=True, text=True).stdout
    if not out.lstrip().startswith("{"):
        return {}, None                      # the one-line degrade message
    cols = json.loads(out)["columns"]
    mine = cols.pop(os.path.basename(path)) if path else None
    return cols, mine


def _discourse_section(doc_id: str, key) -> str:
    """§5d — the numbers this document is written against, and the rules as substitutions.

    **No generated example sentence.** The proposal suggested the brief could build worked
    chains from the document's own facts; a template-generated chain is machine prose handed
    to the author, which is the self-reference loop this repository has already paid for once.
    Worked corrections live in `WRITING_GUIDE.md`, written by a person. This section prints
    numbers and rules only.

    It is the pilot's finding made concrete: an author can execute and self-verify a
    substitution and cannot self-verify a rate. So the brief gives the substitution AND the
    rate, and `check_style.py` prints the rate back on every `check_render.py` run.
    """
    b = io.StringIO()
    w = b.write
    w("## 5d. Discourse targets — the numbers this document is written against\n\n")
    w("> Added 2026-08-17 (register round two). The previous revision of this document is "
      "measured here and nothing more: not a word of it is quoted, and it is not a voice "
      "model. `check_style.py` prints the first three rows back to you on every "
      "`check_render.py` run.\n\n")

    src = _register_columns()
    names = list(src)
    prev = _previous_revision_path(doc_id, key)
    mine = cs.measure(cs.prose_from_qmd(prev))[0] if prev else None

    w("| measure | " + " | ".join(names) + " | this document, previous revision |\n")
    w("|---|" + "---|" * (len(names) + 1) + "\n")
    rows = [("mid-sentence `, so ` (% of sentences) — target <= 1.0", "_pct_so_mid"),
            ("opens with a connective (% of sentences) — target >= 3.0", "_pct_initial_conn"),
            ("2+ clause coordinators (% of sentences)", "_pct_coord2"),
            ("mid-sentence `, and ` joining a second clause (%) — regex, a FLOOR; "
             "target <= 3.4", "_pct_and_clause"),
            ("mid-sentence `, not ` (%) — target <= 0.2", "_pct_not_tail"),
            ("sentences under 15 words (%) — band 15-32", "pct_under_15"),
            ("sentences over 40 words (%) — band 3-21.5", "pct_over_40")]
    for label, k in rows:
        cells = [f"{src[n][k]:.1f}" for n in names]
        cells.append(f"{mine[k]:.1f}" if mine else "no previous revision")
        w(f"| {label} | " + " | ".join(cells) + " |\n")

    dsrc, dmine = _discourse_measures(prev)
    if dsrc:
        disc_rows = [("topic chaining (%) — must not fall more than 2 pt", "chaining"),
                     ("copula main verb (%) — must not rise more than 2 pt", "copula"),
                     ("adjunct front field (%)", "front"),
                     ("sentences with a passive construction (%) — a BAND, never a floor",
                      "passive"),
                     ("`, and ` + a second clause, parser (%) — the other half of the regex row",
                      "and_clause")]
        for label, k in disc_rows:
            cells = [f"{dsrc[n][k + '_pct']:.1f}" for n in names if n in dsrc]
            cells.append(f"{dmine[k + '_pct']:.1f} ({dmine[k][0]}/{dmine[k][1]})"
                         if dmine else "no previous revision")
            w(f"| {label} | " + " | ".join(cells) + " |\n")
        w("\n_The five parser rows are `check_discourse.py --cap`: the sentence caps (600 "
          "chaining, 450 for the rest) the pilot's figures were measured under, so the columns "
          "are comparable with `docs/results/`. The corpus documents sit under both caps; only "
          "the source columns are affected. All but chaining divide by the sentences that have "
          "a root and a subject, which is a few fewer than the sentence count above, so the "
          "passive here reads a few tenths above the round-two page's figure for the same "
          "text._\n")
    else:
        w("| topic chaining / copula / front field / passive / `, and ` parser | "
          + " | ".join("—" for _ in names)
          + " | not measured — `uv sync --extra discourse` |\n")

    w("\n_The rules an author writes to are in `authoring/WRITING_GUIDE.md`; this table is the "
      "reviewer's, produced only under `build_brief.py --review`, and is never bound to an "
      "author. Measured 2026-08-19: the text the owner preferred sat at or beyond round-zero on "
      "every row above, so none of them is a target "
      "(docs/results/2026-08-19-apparatus-probe.md §3b)._\n\n")
    return b.getvalue()



def _mechanism_section(key: str) -> str:
    """§2b — the physical chemistry of the step, from authoring/mechanism/<key>.yaml.

    Prose written from domain knowledge and read once by the project owner (the file says
    when); no number in it, so a reseed cannot stale it. This is the supply for the mechanism
    the reports are asked to explain: until 2026-08-19 nothing carried it, and an author asked
    for a mechanism and given none wrote category labels in its place
    (docs/results/2026-08-18-track-d-stopped.md §5.2).
    """
    import yaml
    path = os.path.join(ROOT, "authoring", "mechanism", f"{key}.yaml")
    if not os.path.exists(path):
        return ("## 2b. Mechanism — how the step works\n\n_No mechanism file at "
                f"`authoring/mechanism/{key}.yaml`. Write one before authoring; see "
                "`authoring/mechanism/README.md`._\n\n")
    m = yaml.safe_load(open(path, encoding="utf-8"))
    b = io.StringIO()
    w = b.write
    w("## 2b. Mechanism — how the step works\n\n")
    w(f"> From `authoring/mechanism/{key}.yaml` ({m.get('source', 'domain knowledge')}; "
      f"reviewed by owner: {m.get('reviewed_by_owner') or 'not yet'}). This is the physical "
      "chemistry the report's mechanistic prose rests on. It carries no number on purpose: "
      "the effects, their signs and their sizes come from the fitted models in §4 and §7, and "
      "the report says what the data show and why the chemistry makes that expected or "
      "surprising.\n\n")
    w("**Overview.** " + " ".join(str(m.get("overview", "")).split()) + "\n\n")
    names = {r["key"]: r["cqa"] for r in P.cqa_reg[["key", "cqa"]].to_dict("records")}
    names.update({k: v for k, v in getattr(D, "RESP_LABEL", {}).items() if k not in names})
    if m.get("cqas"):
        w("**Quality attributes and responses**\n\n")
        for k, text in m["cqas"].items():
            w(f"- **{names.get(k, k)}:** " + " ".join(str(text).split()) + "\n")
        w("\n")
    if m.get("parameters"):
        w("**Parameters**\n\n")
        pnames = {}
        try:
            pnames = {q.key: q.name for q in P.CFG.unit_op(key).parameters}
        except Exception:
            pass
        # Display names only. The YAML keys are config identifiers (`do`, `co2`, `ivcc`), not
        # abbreviations, and the owner's read of 2026-08-19 said so: an author sees "Dissolved
        # oxygen", never "do".
        for k, text in m["parameters"].items():
            w(f"- **{pnames.get(k, k)}:** " + " ".join(str(text).split()) + "\n")
        w("\n")
    return b.getvalue()


def _discrepancy_assignments(doc_id: str) -> str:
    """The registered discrepancies this document is required to carry, if any.

    A registered discrepancy lives in prose, so it survives only as long as nobody
    re-authors the document holding it. Nothing surfaced D-001 or D-002 to an author before
    this section existed: re-author PCR-003 and the sentence is simply not written again,
    while `authoring/DISCREPANCIES.md` goes on calling the item open. Nothing fails, because
    no gate reads that registry and `check_grounding.py` only inspects
    ``SourceReference.quote``.

    Losing the prose half alone is worse than losing the item. D-002's other half is a
    generated ``ProcessStep.description``, so it survives a re-author and the annex is left
    asserting something the document no longer says.

    **The section is always emitted, empty when the document carries nothing.** An absent
    section cannot be told apart from a mechanism that has silently stopped working, and
    "my brief has no discrepancies section" is exactly what an author would have seen while
    this was broken.

    Assignments come from ``authoring/discrepancies.yaml``. This is not the weak-claims
    layer, which lives only on ``feature/weak-claims-via-brief``; see that file's header.
    """
    b = io.StringIO()
    b.write("## 5c. Registered discrepancies — this document must carry these\n\n")

    path = os.path.join(HERE, "discrepancies.yaml")
    data = yaml.safe_load(open(path)) if os.path.exists(path) else {}
    items = ((data or {}).get("items") or {}).get(doc_id) or []

    if not items:
        b.write("**None.** No registered discrepancy is assigned to this document, so every "
                "claim you write must be internally consistent, consistent with the other "
                "documents in the corpus, and consistent with the data. The registry is "
                "`authoring/DISCREPANCIES.md`; an *unregistered* inconsistency is a bug.\n\n")
        return b.getvalue()

    b.write("> `authoring/DISCREPANCIES.md` registers a small number of **genuine "
            "inconsistencies** that a competent review should catch. They are deliberate "
            "benchmark items, and each one lives in the prose of a particular document. "
            "Yours carries the following.\n>\n"
            "> Write each in your own words, in register, where the assignment says. Then "
            "leave it alone. **Do not reconcile it** with another document, with the data, "
            "or with a later section of your own report, and do not qualify it into "
            "something true. Correcting one deletes a benchmark item.\n>\n"
            "> These are not labeled in the annex, so nothing in the document or its ground "
            "truth reveals them. Every other claim you write is still grounded.\n\n")
    for it in items:
        a = it.get("assignment") or {}
        b.write(f"### {it['id']} — `{it.get('kind', '?')}`\n\n")
        if a.get("registered_sentence"):
            # The sentence as the registry records it. Quoted rather than described, because
            # a paraphrase of a registered discrepancy is very easily a *qualified* version,
            # and a qualified D-002 is true and therefore no longer a benchmark item.
            b.write("> " + ' '.join(a["registered_sentence"].split()) + "\n>\n"
                    "> — the sentence this document currently carries. Write this claim. Your "
                    "wording may differ; its strength may not.\n\n")
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


def build(doc_id: str, review: bool = False) -> str:
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
      "(WRITING_GUIDE §3). Bound to the author with `WRITING_GUIDE.md`, `section_plan.yaml`, "
      "`REGISTER_EXEMPLAR.md`, `STORY_BIBLE.md`.\n>\n"
      "> **This brief is a data sheet, not a style model.** It is written in terse note form "
      "with dashes, bold labels and fragments because it is a lookup table. The report's prose "
      "must not read like it. For voice, use `REGISTER_EXEMPLAR.md` (verbatim passages from "
      "the four published human sources) and the ten rules in WRITING_GUIDE §2. This brief "
      "carries no counter; the reviewer's table is `build_brief.py --review`.\n\n")

    # 1. Identity ---------------------------------------------------------------
    w("## 1. Identity\n\n")
    w(f"- **Document:** {doc_id} — {cls}\n")
    w(f"- **Subject:** {subject}\n")
    if key is not None:
        w(f"- **Unit operation:** {uo_title} · key `{key}`\n")
        w(f"- **Role in control strategy:** {role}\n")
        w(f"- **DoE step:** {'yes' if doe else 'no (univariate / qualitative — do NOT fabricate a DoE)'}\n")
        w("- **Commercial scale:** state it in the introduction, via "
          "`V[\"commercial_scale_l\"]` (config `meta.commercial_scale_l`). The round-one "
          "PCR-003 never stated the scale it characterizes.\n")
    else:
        w("- **Scope:** corpus-level document (no single unit operation)\n")
    w(f"- **Doc-type outline:** `section_plan.yaml` -> "
      f"`{'report_doe' if (is_report and doe) else 'report_nondoe' if is_report else 'plan' if is_plan else 'n/a'}`\n")
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

    # 2b. Mechanism -------------------------------------------------------------
    # Per-unit-operation documents only: the corpus-level four have no single step.
    if key is not None:
        w(_mechanism_section(key))

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

    # 5c. Registered discrepancies ----------------------------------------------
    # Always emitted, empty when none. A section that disappears when a document carries
    # nothing is indistinguishable from a section that stopped being generated.
    w(_discrepancy_assignments(doc_id))

    # 5d. Discourse targets ------------------------------------------------------
    # REVIEWER ONLY since 2026-08-19 (`--review`). Until then this section printed the previous
    # revision's counters to the author, and the round that removed them from the author's
    # inputs was preferred blind (docs/results/2026-08-19-apparatus-probe.md). A brief bound to
    # an author carries no counter.
    if review:
        w(_discourse_section(doc_id, key))

    # 6. Cross-references -------------------------------------------------------
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
    # RA-001's failure-mode, effect and study-type content lives in pc_package/ra_content.py,
    # which section_plan.yaml names as the content source for this document class but which the
    # inventory never listed. RA-001's author had to find it unaided on 2026-08-21; added so the
    # next one does not have to.
    if doc_id == "RA-001":
        import ra_content as RC
        w("### `ra_content` (import as `RC`) — the curated risk content for this document\n\n")
        w("> `authoring/section_plan.yaml` names this module as the content source for the "
          "pre-characterization risk assessment. The failure modes, effects and attributes at "
          "risk are curated here and joined to the seeded registers; they are not in the CSVs.\n\n")
        w("\n".join(_helper_lines(RC, "ra_content", prefix="RC.")) + "\n\n")
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
    review = "--review" in argv
    argv = [a for a in argv if a != "--review"]
    os.makedirs(OUT, exist_ok=True)
    for doc_id in argv[1:]:
        text = build(doc_id, review)
        path = os.path.join(OUT, f"{doc_id}.brief.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"wrote {os.path.relpath(path, ROOT)}  ({len(text):,} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
