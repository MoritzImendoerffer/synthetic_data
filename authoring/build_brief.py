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
      f"reviewed by owner: {m.get('reviewed_by_owner') or 'not yet'}"
      + (f"; NOT yet read by the owner: {', '.join(m['pending_owner_review'])}"
         if m.get("pending_owner_review") else "")
      + "). This is the physical "
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


def _model_adequacy_section(doc_id, key, is_report) -> str:
    """PCMP-001 §7.2 and INV-002 for one step: the status of each model, and for a report the
    augmentation and the re-evaluation it must carry."""
    import pandas as _pd
    b = io.StringIO()
    w = b.write
    m = P.csv("model_adequacy.csv")
    m = m[m["step_key"] == key]
    w("### Model adequacy (PCMP-001 §7.2) and INV-002 — `csv(\"model_adequacy.csv\")`\n\n")
    w("Full quadratic models of the PLANNED runs against §7.2, and the remedy INV-002 gave each "
      "failing model:\n\n")
    cols = ["response", "n", "k", "R2", "predR2", "gap", "p_lof", "adequate", "effects", "m_required",
            "remedy", "reason"]
    w(m[cols].round(3).to_markdown(index=False) + "\n\n")
    if not is_report:
        w("A plan is prospective: it states the full quadratic model and the §7.2 criteria. It does "
          "not describe INV-002, the augmentation or a refit, which came after the plan.\n\n")
        return b.getvalue()
    rows = []
    for resp in [r for r in m["response"]]:
        r = D.fit(key, "rsm", resp)
        rows.append({"response": resp, "status": r["status"], "scale": r.get("transform") or "raw",
                     "runs": r["n"], "block": r["block"],
                     "terms": " ".join(r["names"]) or "(none)", "R2": round(r["R2"], 3),
                     "predR2": round(r["predR2"], 3), "gap": round(r["gap"], 3),
                     "nor_met": D.nor_met(key, resp)})
    w("The model each output ENDS UP WITH (`D.fit(UO, \"rsm\", resp)`; `D.model_status`), by the model "
      "selection of INV-002 corrective action CA3 (Box-Cox scale, lowest AICc over all hierarchical "
      "submodels of the full quadratic, block kept; `amab_process/adequacy.select_model`): "
      "\"selected\" = the selected model meets PCMP-001 §7.2; \"none\" = it does not, and the output is "
      "judged on its measured results (`D.measured_met`) and sets no range. `transform` \"log\" = the "
      "output is modelled on the log scale (a prediction is a median; a scale-down offset is a ratio). "
      "Every prediction, PAR and NOR judgement in the report uses this model. The model selection is a "
      "discrepancy from the plan, in `discrepancy_register(DOC)` (PCMP-001 is not changed); describe the "
      "procedure in the statistical methods and the discrepancy section:\n\n"
      + _pd.DataFrame(rows).to_markdown(index=False) + "\n\n")
    if D.has_augmentation(key):
        pds = [d for d in P.PLAN_DISCREPANCIES.get(doc_id, []) if "Augmentation" in d["subject"]]
        a = P.csv(f"doe_{key}_aug.csv")
        w(f"**Augmentation ({pds[0]['id'] if pds else 'discrepancy'}).** {len(a)} runs, study "
          f"{a['study'].iloc[0]}, block 2, runs {int(a['run'].min())}–{int(a['run'].max())}. The report "
          "carries: the additional runs as an appendix (`T.doe_results(UO, \"aug\")`), an "
          "explanation (why: the planned model failed §7.2; the number of runs from INV-002, cited, "
          "not recalculated), the re-evaluation of every model on all runs with a block term "
          "(`T.model_reevaluation(UO)`), and the discrepancy from the plan. Fit on the planned runs "
          "only with `D.fit(UO, \"rsm\", resp, runs=\"planned\", form=\"full\")`.\n\n")
    else:
        w("This step was not augmented. Where a model is refitted, the report says that PCMP-001 "
          "§7.2 provides the refit, names the terms kept and cites INV-002 for the rule "
          "(`T.model_reevaluation(UO)`).\n\n")
    return b.getvalue()


def _inv2_section() -> str:
    """The facts of INV-002: the failing models, the rule, the sample sizes, the augmentations, and
    the consequences the reports draw."""
    b = io.StringIO()
    w = b.write
    ma = P.CFG.raw()["campaign"]["model_adequacy"]
    w("### INV-002 facts\n\n")
    w(f"- **Rule** (config `campaign.model_adequacy`, decided {ma['decided']}): augmentation for an "
      "attribute of the drug substance specification on which the refit of the planned runs keeps "
      f"an effect; a refit for every other failing model; target assurance {ma['assurance']}; "
      f"{ma['reps']} simulated data sets per size; sizes in steps of {ma['step']}; no augmentation "
      "larger than the planned design; viral clearance is not a drug substance test "
      f"({', '.join(ma['not_specification'])}), so its models are refitted and no virus is spiked.\n")
    w(f"- **Root cause and CA3** (config `selection_adopted`, {ma.get('selection_adopted')}): the plans "
      "prescribed the full quadratic as the predictive model and no model selection. Corrective action CA3 "
      "analyses every response-surface output by model selection: the Box-Cox scale (log where the 95 % "
      "interval contains 0 and excludes 1), the lowest AICc over all hierarchical submodels of the full "
      "quadratic by exhaustive search (stepwise can stop at a worse model), a block term kept, the "
      "selected model judged against PCMP-001 §7.2 (and a significant F-test when it has terms), an output "
      "with no adequate model judged on its measured results, a scale-down offset on the scale of the "
      "model (`amab_process/adequacy.select_model`). PCMP-001 is not changed: each DoE report records it "
      "as a discrepancy from its plan. INV-002 describes every procedure it applied, including this one.\n")
    w(f"- **Criteria:** fixed at the closure of {P.INV['id']} ({P.INV['closed']}) from the planned designs, "
      "with the verification of platform worst cases on the models CA3 selects (adopted before that "
      "date). The augmentations, which ended after that date, move none. `csv(\"iac_full.csv\")` and "
      "`csv(\"iac_verification_full.csv\")` give the same verification on the full quadratic models, "
      "the planned analysis: the criteria as they would have been without CA3. CA3 changed these:\n\n")
    a, f_ = P.csv("iac.csv"), P.csv("iac_full.csv")
    mm = f_.merge(a, on=["step_key", "response"], suffixes=("_full", "_in_force"))
    ch = mm[(mm["iac_high_full"].round(6) != mm["iac_high_in_force"].round(6))
            | (mm["iac_low_full"].round(6) != mm["iac_low_in_force"].round(6))]
    w(ch[["step_key", "response", "iac_high_apriori_in_force", "iac_high_full", "basis_full",
          "iac_high_in_force", "basis_in_force"]].round(3).to_markdown(index=False) + "\n\n")
    vf, vs = P.csv("iac_verification_full.csv"), P.csv("iac_verification.csv")
    vv = vf.merge(vs, on=["step_key", "cqa"], suffixes=("_full", "_selected"))
    w("  The verification rows behind them (full quadratic against selected model):\n\n")
    w(vv[["step_key", "cqa", "assumed_full", "predicted_nor_bound95_full", "model_adequate_full",
          "widening_supported_full", "predicted_nor_bound95_selected", "model_adequate_selected",
          "widening_supported_selected"]].dropna(subset=["predicted_nor_bound95_full"])
       .round(4).to_markdown(index=False) + "\n\n")
    w("- **The augmentations, honestly** (owner's option a, 2026-10-09): sized and made under the plan's "
      "model (the planned full quadratic failed §7.2). Once models are selected, the models they were "
      "made for are adequate on the planned runs alone (the status table below, column `status` with the "
      "planned runs: compare `model_adequacy.csv` with `D.fit(step, \"rsm\", resp, runs=\"planned\")`), so "
      "they were not needed for adequacy; they sharpen the estimates. Say so; the step reports give the "
      "results of the new runs.\n")
    w("- **Owner's instruction (2026-10-08):** \"calculate the required sample size to resolve these "
      "effects by additional runs for DoEs on unit operations which affect the drug substance "
      "specification, for the others, reduce the model.\"\n\n")
    w("Failing models and their remedy — `csv(\"model_adequacy.csv\")`:\n\n")
    m = P.csv("model_adequacy.csv")
    w(m[~m["adequate"].astype(bool)].round(3).to_markdown(index=False) + "\n\n")
    w("Per-step augmentation — `csv(\"augmentation_plan.csv\")`:\n\n")
    w(P.csv("augmentation_plan.csv").to_markdown(index=False) + "\n\n")
    w("Augmentation studies (chronology):\n\n")
    ch = P.csv("study_chronology.csv")
    w(ch[ch["kind"] == "augmentation"].to_markdown(index=False) + "\n\n")
    w("Model status after the remedies (`D.model_status(step, resp)`), and the NOR judgement:\n\n")
    rows = []
    for _, r in m.iterrows():
        f = D.fit(r["step_key"], "rsm", r["response"])
        rows.append({"step": r["step_key"], "response": r["response"], "status": f["status"],
                     "runs": f["n"], "terms": len(f["names"]), "gap": round(f["gap"], 3),
                     "nor_met": D.nor_met(r["step_key"], r["response"])})
    import pandas as _pd
    w(_pd.DataFrame(rows).to_markdown(index=False) + "\n\n")
    w("Discrepancies from the plan that the augmentations are: "
      + "; ".join(f"{d['id']} ({doc}): {d['done']}" for doc, ds in P.PLAN_DISCREPANCIES.items()
                  for d in ds if "Augmentation" in d["subject"]) + ".\n\n")
    w("Figure: `D.fig_assurance()` — the probability of success against the number of further runs, one line "
      "per failing model with an effect (viral clearance dotted), the target dashed. Print it in "
      "a chunk with `#| label: fig-assurance` and a `#| fig-cap:`.\n\n")
    w(f"CAPA (`CAPA2`):\n\n{P.CAPA2.to_markdown(index=False)}\n\nEffectiveness check: "
      f"{P.EFFECTIVENESS2}\n\n")
    return b.getvalue()


def _setpoint_section(doc_id, key, is_report, is_plan) -> str:
    """Version 2.0 NOR and set-point decisions of a step (config ``nor_v2``/``setpoint_v2``) and the
    evidence behind them: the PAR margins in force and as characterized, and for low-pH inactivation
    and the production bioreactor the studies and judgements the owner's decisions rest on."""
    import pandas as _pd
    b = io.StringIO()
    w = b.write
    uo = P.CFG.unit_op(key)
    moved = [p for p in uo.parameters
             if list(p.nor) != list(p.nor_characterized) or p.setpoint != p.setpoint_characterized]
    if not moved and key not in ("viral_inactivation", "bioreactor"):
        return ""
    w("### Version 2.0 NOR and set-points, and the evidence (STORY_BIBLE §9b)\n\n")
    if moved:
        rows = []
        for p in moved:
            nc, nf = list(p.nor_characterized), list(p.nor)
            kind = ("moved" if (nf[1] - nf[0]) == (nc[1] - nc[0]) and nf != nc else
                    "narrowed" if nf != nc else "unchanged")
            rows.append({"parameter": p.name, "unit": p.unit,
                         "set-point as characterized": p.setpoint_characterized,
                         "NOR as characterized": f"{nc[0]:g}–{nc[1]:g}", "set-point in force": p.setpoint,
                         "NOR in force": f"{nf[0]:g}–{nf[1]:g}", "NOR change": kind,
                         "set-point change": "moved" if p.setpoint != p.setpoint_characterized else "unchanged"})
        w(_pd.DataFrame(rows).to_markdown(index=False) + "\n\n")
        w("The studies were planned and run around the values as characterized; the nominal batch and "
          "the verification of platform worst cases use them too. Monte Carlo, PPQ and every judgement "
          "across the NOR use the values in force (`Parameter.nor`, `.setpoint`); "
          "`with D.characterized_nor():` switches back. "
          + ("A plan states the values as characterized, the values its studies were planned against, "
             "and a footnote names the change the report made (`T.parameters_by_step` does this)."
             if is_plan else "") + "\n\n")
    if is_report:
        w("NOR-propagated PAR margins in force — `D.par_margins(UO)` (margins in the unit of the "
          "parameter; None where the PAR edge is the end of the range studied):\n\n")
        w(D.par_margins(key).round(3).to_markdown(index=False) + "\n\n")
        if moved:
            with D.characterized_nor():
                m0 = D.par_margins(key)
            w("The same as characterized — inside `D.characterized_nor()`:\n\n"
              + m0.round(3).to_markdown(index=False) + "\n\n")
    if key == "viral_inactivation" and is_report:
        with D.characterized_nor():
            met0 = D.nor_met(key, "xmulv_lrf")
        w(f"- XMuLV claim across the NOR (`D.nor_met(UO, \"xmulv_lrf\")`): as characterized {met0}, in force "
          f"{D.nor_met(key, 'xmulv_lrf')}. Owner, 2026-10-09: \"0.04 pH units is not controllable. 0.1 is "
          "already very tight for large scale production\" (the set-point had sat 0.04 pH units from the "
          "PAR edge of the NOR first decided). The set-points are re-centred in the NOR in force.\n")
        a = D.ofat_analysis()
        w("- **S-VI-OFAT (PD-006-01)** — `D.ofat_analysis()`, tables `T.vi_ofat()` (every result) and "
          "`T.ofat_effects()` (the analysis). An analysis of covariance per attribute (pH as a two-level "
          "factor, hold time), the pH p-values adjusted by Holm's method over the three attributes, the "
          "interaction tested separately, the difference at time 0 (`diff_t0`, the pH-adjusted load before "
          "any hold, where a hold effect cannot yet have acted):\n\n")
        w(a.drop(columns=["unit"]).round(4).to_markdown(index=False) + "\n\n")
        w("  Read it as a process scientist would. Aggregate and fragments rise with hold time and show no "
          "pH effect. An apparent pH difference in an attribute whose low-pH model has no pH term "
          "(`D.fit(UO, \"rsm\", resp)[\"names\"]`) that is already present at time 0 and does not grow with "
          "hold time (interaction) is not an effect of the hold pH: say so, with the method repeatability, "
          "and state the multiplicity. Every result is judged against the step's criterion (`met_nor`).\n\n")
        c = D.cex_verification_summary()
        w("- **S-CEX-VER (PD-006-02)** — `D.cex_verification_summary()`, tables `T.cex_verification_n()` "
          "(the simulation that set the number of runs) and `T.cex_verification_runs()` (the runs and the "
          "decision). The number of runs is the larger of the two attributes' needs; the decision is the "
          "one-sided 95 % lower confidence bound of the mean log fold against the fold the criteria rely on "
          "(`amab_process/adequacy.verification_runs`):\n\n")
        w(c.drop(columns=["folds"]).round(4).to_markdown(index=False) + "\n\n")
        ws, wh = D.vi_worst_case_summary()
        w("- **The decision revised, and S-VI-WC (PD-006-03)** — the hold-time NOR in force was revised after "
          "the margin analysis above (STORY_BIBLE §9b), and confirmation runs were made at the low end of the "
          "pH PAR with hold time and temperature at the upper ends of their NORs (`D.vi_worst_case_summary()`, table "
          "`T.vi_worst_case_runs()`). Hold output of each run against the step's criteria:\n\n")
        w(wh.round(3).to_markdown(index=False) + "\n\n")
        w("  Cation exchange on that material, by the same rule as S-CEX-VER:\n\n")
        w(ws.drop(columns=["folds"]).round(4).to_markdown(index=False) + "\n\n")
        w("  Where `passed` is False with `every_run_above` True, the pre-set rule is not met: say so plainly, "
          "and give the risk argument the owner accepted (decision 5a): even with no clearance by cation "
          "exchange the hold output meets the drug substance limit, the attribute is tested at release, and "
          "the patient risk is nil. Never pool these runs with S-CEX-VER.\n\n")
        w("- **Downstream clearance is sufficient** (owner): show it with the cation exchange model and the "
          "criteria (the worst-case verification of `T.worst_case_verification`, the folds the criteria rely "
          "on) and with the verification runs (`pool_max` against `pool_crit`, the cation exchange criteria). "
          "D-001 (the set-point PAR analysis at the design centre) stays as registered.\n\n")
    if key == "bioreactor" and is_report:
        wc = D.nor_worst_corner(key, "acidic_variants")
        po = P.csv("p_oos.csv").set_index("key").loc["acidic_variants"]
        w(f"- **Acidic variants (owner: option a).** Across the NOR (`D.nor_met`): "
          f"{D.nor_met(key, 'acidic_variants')}. Worst corner (`D.nor_worst_corner(UO, \"acidic_variants\")`, "
          f"manufacturing scale): {wc}. Drug substance probability out of specification "
          f"(`csv(\"p_oos.csv\")`): {int(po['n_oos'])} of {int(po['n'])} simulated batches outside, normal "
          f"approximation {po['p_oos_normal']:.3g} ({po['ppm_normal']:.0f} ppm). The risk is mainly the "
          "producer's: acidic variants have very low criticality and 18 % is a range-of-experience limit. "
          "Accepted on the plan's PAR method (the Monte Carlo PAR contains the NOR, with almost no margin in "
          "pH and pCO2; the corner is the worst case and is stated), with risk mitigation: acidic variants "
          "monitored at harvest (early detection, acceptable but weak), and alarm limits on pH and pCO2 "
          "inside the NOR on the side that lowers acidic variants.\n\n")
        oa = D.osmolality_analysis()
        w("- **S-BRX-OSM, the osmolality study (PD-003-01)** — `D.osmolality_analysis()` (manufacturing scale, "
          "the scale-down offset applied); osmolality set as `CFG.raw()[\"analytics\"][\"osmolality_study\"][\"control\"]` "
          "says; runs per level from `amab_process.analytics.osmolality_runs` (the prediction at the NOR high with a "
          "standard error of at most half the run-to-run SD). Owner's decision 6a: the risk that the worst-corner "
          "mean falls below the lower limit with osmolality at its NOR high is accepted as the producer's risk "
          "(a NOR is the range the process is routinely controlled in; narrowing it is not easy), with an "
          "osmolality alarm inside the NOR on its upper side added to the mitigation.\n\n")
        w(oa.round(3).to_markdown(index=False) + "\n\n")
    return b.getvalue()


def _rev2_section(doc_id, key, is_report, is_plan, doe) -> str:
    """Version 2.0: the revision, the investigation, the criteria old and new, the methods, the
    chronology and the complex tables this document should carry. Facts only, all pulled."""
    import tables as T
    b = io.StringIO()
    w = b.write
    ver, eff = P.doc_version(doc_id)
    w("## 4c. Version 2.0 — revision facts\n\n")
    w(f"- **This document:** Version {ver}, effective {eff} (`doc_version(DOC)`). "
      + ("New document." if doc_id in P.INVESTIGATIONS else
         f"Supersedes Version {P.REV1['rev']} of {P.rev1_date(doc_id)}, frozen in "
         "`pc_package/superseded/rev1/`.") + "\n")
    w(f"- **Investigation:** {P.INV['id']}, {P.INV['title']}; opened {P.INV['opened']}, closed "
      f"{P.INV['closed']}; trigger: {P.INV['trigger']}; classification {P.INV['classification']} "
      "(`INV`).\n")
    w(f"- **Second investigation:** {P.INV2['id']}, {P.INV2['title']}; opened {P.INV2['opened']}, "
      f"closed {P.INV2['closed']}; trigger: {P.INV2['trigger']}; classification "
      f"{P.INV2['classification']} (`INV2`, `CAPA2`, `EFFECTIVENESS2`). It applied the model-adequacy "
      "criteria of PCMP-001 §7.2 to every response-surface model with a criterion, augmented the "
      "designs its rule names and refitted every other failing model. Its corrective action CA3 (model "
      f"selection), adopted on {P.CFG.raw()['campaign']['model_adequacy'].get('selection_adopted')}, before "
      f"{P.INV['id']} closed, is the analysis behind the criteria in force; the augmentation runs moved no "
      "criterion.\n")
    w(f"- **Method decision:** {P.AMD['id']}, {P.AMD['date']}: {P.AMD['title']} (`AMD`).\n")
    w("- **Revision history:** `revision_history(DOC)` under an unnumbered heading after the "
      "approvals. The story is STORY_BIBLE §9b; the findings are numbered there.\n")
    w("- **Abbreviations:** `abbreviations_table([(abbreviation, meaning), ...])`, the pairs this "
      "document uses (template.qmd).\n")
    pds = P.PLAN_DISCREPANCIES.get(doc_id, [])
    if pds:
        w("- **Discrepancies from the plan** (`discrepancy_register(DOC)`, `PLAN_DISCREPANCIES`). "
          "Every departure from the plan: work the plan did not foresee and a plan requirement that was "
          "not met, however late it was found. A process characterization study is not GMP manufacture "
          "and raises no deviation (owner, 2026-10-10). Never call one a deviation:\n")
        for d in pds:
            w(f"  - {d['id']}: {d['subject']}. Planned ({d['plan']}): {d['planned']}. Done: "
              f"{d['done']}. Reason: {d['reason']}.\n")
    w("\n")
    w("### Study chronology — `csv(\"study_chronology.csv\")`\n\n")
    ch = P.csv("study_chronology.csv")
    if key is not None:
        ch = ch[ch["step"] == key]
    w(ch.to_markdown(index=False) + "\n\n")
    if key is not None:
        mp = P.csv("method_plan.csv")
        mp = mp[mp["step"] == key]
        w("### Fragment method by study — `csv(\"method_plan.csv\")`\n\n")
        w(mp.to_markdown(index=False) + "\n\n")
        it = D.iac_table(key)
        if not it.empty:
            w("### Intermediate acceptance criteria for this step — `D.iac_table(UO)`\n\n")
            w(it.drop(columns=["iac_low_apriori"], errors="ignore").to_markdown(index=False) + "\n\n")
        r1 = D.rev1_criteria(key)
        if not r1.empty:
            w("### Version 1.0 criteria for this step — `D.rev1_criteria(UO)`\n\n")
            w(r1.to_markdown(index=False) + "\n\n")
        if doe and is_report:
            w("### What moved: the PAR table under Version 1.0 criteria — `D.par_table_rev1(UO)`\n\n"
              "The same models judged against the Version 1.0 criteria. Compare with §4b for "
              "'Changes in this revision'. Use only to say what moved; never present it as a "
              "result.\n\n")
            try:
                w(D.par_table_rev1(key).to_markdown(index=False) + "\n\n")
            except Exception as e:  # noqa: BLE001
                w(f"_(unavailable: {e})_\n\n")
        v = D.iac_verification(key)
        if not v.empty:
            w("### Platform worst cases this step verifies — `D.iac_verification(UO)`\n\n")
            w(v.to_markdown(index=False) + "\n\n")
        if key in D.st.DOE_FACTORS and (is_report or is_plan):
            w(_model_adequacy_section(doc_id, key, is_report))
        w(_setpoint_section(doc_id, key, is_report, is_plan))
        if key in ("harvest", "ufdf"):
            uni = P.csv("univariate_studies.csv")
            uni = uni[uni["step"] == key].dropna(axis=1, how="all")
            sid = uni["study"].iloc[0]
            w(f"### Univariate study {sid} — `csv(\"univariate_studies.csv\")`, rows of step `{key}`\n\n")
            w("Owner's decision 2026-10-08 (option A): each parameter at five levels in duplicate, the "
              "others at set-point. This is **not** a designed experiment; never call it one and "
              "never fit a multifactor model to it. Judge each response on its slope against the "
              "setting (`scipy.stats.linregress`, α = campaign `effect_alpha`) and on the level "
              "means against the criterion. "
              + ("Harvest keeps the source's assumption that the step has no impact on product "
                 "quality (A-Mab p.85, 'for simplicity'; 'This might not be true in a real life "
                 "scenario'): host cell protein and aggregate pass through, and differ only by "
                 "assay precision. Turbidity is a performance output, not an attribute. "
                 "Post-clarification turbidity is the outcome of the other two parameters. It was "
                 "studied as a challenge: clarified filtrate adjusted to each level with centrate, "
                 "the level measured, the attributes recorded (centrate turbidity not reported)."
                 if key == "harvest" else
                 "The source gives nothing for this step (A-Mab p.114: UF/DF 'not included in case "
                 "study'). The aggregate effect at high final concentration and high TMP is this "
                 "campaign's own finding; residual buffer and concentration are performance "
                 "outputs, not attributes.")
              + " Means by level:\n\n")
            means = uni.groupby(["parameter", "level", "value"], sort=False).mean(numeric_only=True)
            w(means.drop(columns=["replicate"]).round(4).to_markdown() + "\n\n")
            from scipy import stats as _st
            rows = []
            for par, g in uni.groupby("parameter", sort=False):
                for col in [c for c in uni.columns[6:] if g[c].notna().all()]:
                    fit = _st.linregress(g["value"], g[col])
                    rows.append({"parameter": par, "response": col, "slope": fit.slope, "p": fit.pvalue})
            import pandas as _pd
            w("Slopes against the setting:\n\n" + _pd.DataFrame(rows).to_markdown(index=False, floatfmt=".3g") + "\n\n")
        if key in ("harvest", "protein_a", "viral_inactivation"):
            # owner, 2026-10-09: no Version 1.0 document planned or reported a hold study; the hold
            # studies were made during the Version 2.0 re-analysis and each report records its own as a
            # discrepancy from the plan
            hstudy = P.CFG.raw()["analytics"]["holds"][key]["study"]
            hpd = [d for d in P.PLAN_DISCREPANCIES.get(f"PCR-{P.CFG.unit_op(key).step:03d}", [])
                   if hstudy in d.get("studies", [])]
            hchron = P.csv("study_chronology.csv").set_index("id").loc[hstudy]
            if is_plan:
                w(f"### Hold study — not a study of this plan\n\n- The hold study {hstudy} was made "
                  f"{hchron['start']} to {hchron['end']}, during the Version 2.0 re-analysis. Version 1.0 of "
                  "this plan did not foresee a hold study, and this amendment does not add one: the report "
                  f"records it as {hpd[0]['id']}, a discrepancy from the plan. Do not describe its design, "
                  "sampling or criterion as part of this plan.\n\n")
            else:
                w(f"### Hold-time stability — `T.hold_stability(\"{key}\")`, data `csv(\"hold_{key}.csv\")`\n\n")
                w(f"- Made {hchron['start']} to {hchron['end']}, during the Version 2.0 re-analysis and after "
                  f"AMD-001, so fragments by nrCE-SDS on every sample. Version 1.0 planned and reported no hold "
                  f"study: record it as {hpd[0]['id']} (`discrepancy_register(DOC)`), a discrepancy from the "
                  "plan, never as a deviation. The pool is the nominal set-point material of the step "
                  "model.\n\n")
                w(P.csv(f"hold_{key}.csv").round(3).to_markdown(index=False) + "\n\n")
        if key == "viral_inactivation":
            # the concentration study that measured no XMuLV clearance: a discrepancy from the plan, not a
            # deviation (owner, 2026-10-10; it was DEV-006-03)
            dv = next(e for e in P.PLAN_DISCREPANCIES["PCR-006"]
                      if e["subject"].startswith("XMuLV clearance not measured in the concentration study"))
            vc = P.CFG.raw()["analytics"]["vi_concentration"]
            if is_plan:
                w("### The A-Mab concentration study as Version 1.0 planned it\n\n- Version 1.0 of this "
                  "plan set the concentration study across the range studied, with the other three parameters "
                  "at their set-points, and required aggregate, acidic variants and XMuLV clearance on every "
                  "run. This amendment keeps that design. That S-VI-UNI measured no XMuLV clearance is a "
                  f"discrepancy from the plan the report records ({dv['id']}); the plan does not change to match "
                  "what was done.\n\n")
            else:
                u = P.csv("univariate_studies.csv")
                vu = u[u["study"] == vc["study"]][["level", "value", "replicate", "xmulv_lrf",
                                                     "aggregate_out_pct", "acidic_variants"]]
                w(f"### {dv['id']} and the confirmation study {vc['study']}\n\n- {dv['id']}: "
                  f"{dv['subject']}. Planned: {dv['planned']}. Done: {dv['done']}. Found in the Version 2.0 "
                  f"re-analysis; Version 1.0 of PCR-006 did not notice it (`discrepancy_register(DOC)`).\n"
                  "- The confirmation study, XMuLV-spiked holds at both ends of the concentration "
                  "range, in duplicate, other parameters at their set-points as characterized:\n\n")
                w(vu.round(3).to_markdown(index=False) + "\n\n")
        if key == "cex":
            w("### SEC against nrCE-SDS (S-CEX-FRC) — `T.method_comparability()`\n\n")
            c = P.csv("cex_fraction_comparability.csv")
            w(c.groupby("sample", sort=False)[["lmw_sec_pct", "lmw_cesds_pct", "difference"]]
              .mean().round(3).to_markdown() + "\n\n")
    else:
        if doc_id == P.INV2["id"]:
            w(_inv2_section())
        w("### Corpus-level tables\n\n")
        for name in ("iac.csv", "criteria_rev1.csv", "iac_verification.csv", "iac_viral_cumulative.csv", "p_oos.csv"):
            w(f"`csv(\"{name}\")`:\n\n" + P.csv(name).round(4).to_markdown(index=False) + "\n\n")
        c = P.csv("cex_fraction_comparability.csv")
        w("SEC against nrCE-SDS by sample (means of `cex_fraction_comparability.csv`):\n\n")
        w(c.groupby("sample", sort=False)[["lmw_sec_pct", "lmw_cesds_pct", "difference"]].mean().round(3).to_markdown() + "\n\n")
        r1 = P.csv("capability.csv")
        w("Capability (Version 2.0, acidic variants two-sided). Version 1.0's minimum Cpk was "
          "the one-sided value; recompute it as `(acc_high - mean) / (3 sd)` for acidic variants "
          "if it is needed, never type it:\n\n")
        w(r1[["key", "spec_type", "mean", "sd", "Cpl", "Cpu", "Cpk"]].round(3).to_markdown(index=False) + "\n\n")
    # the complex tables for this document
    w("### Complex tables this document should carry (pc_package/tables.py, `import tables as T`)\n\n")
    w("Print each in its own chunk with `#| output: asis` as `T.<builder>(...).show()`. Use the "
      "exact call below: the annex builder calls the same one to anchor its rows. A table of your "
      "own whose first column repeats is `T.frame(df, caption, label, merge=[...])`, never a pipe "
      "table (WRITING_GUIDE §6).\n\n")
    calls = []
    if key is not None:
        calls.append(f'T.methods_by_study(["{key}"])')
        if not D.iac_table(key).empty:
            calls.append(f'T.criteria_change(["{key}"])')
        if is_report and doe:
            calls += [f'T.criteria_results("{key}")', f'T.doe_results("{key}", "screening")',
                      f'T.doe_results("{key}", "rsm")']
            if not D.iac_verification(key).empty:
                calls.append(f'T.worst_case_verification(["{key}"])')
        if is_plan and not D.iac_table(key).empty:
            calls.append(f'T.iac_derivation(["{key}"])')
        if key in ("harvest", "protein_a", "viral_inactivation") and is_report:
            calls.append(f'T.hold_stability("{key}")')
        if key == "cex" and is_report:
            calls.append("T.method_comparability()")
        if key == "aex" and is_report:
            calls.append('T.doe_results("aex", "rsm", superseded=True)')
        has_sdm = key in set(P.csv("sdm_qualification.csv")["step"])
        if is_report and key in D.st.DOE_FACTORS:
            calls.append(f'T.model_reevaluation("{key}")')
            if D.has_augmentation(key):
                calls.append(f'T.doe_results("{key}", "aug")')
        if is_report and has_sdm:
            calls.append(f'T.sdm_offsets(["{key}"])')
            sdm_st = list(P.csv("sdm_qualification.csv").query("step == @key")["study"].unique())
            for d in P.PLAN_DISCREPANCIES.get(doc_id, []):
                extra = [s_ for s_ in d.get("studies", []) if s_ in sdm_st]
                if extra:                       # a discrepancy that added scale-down runs
                    planned = [s_ for s_ in sdm_st if s_ not in extra]
                    calls.append(f'T.sdm_offsets(["{key}"], studies={planned!r}, label="tbl-sdm-offsets-planned")')
        if is_report and key == "viral_inactivation":
            calls += ["T.vi_ofat()", "T.ofat_effects()", "T.cex_verification_n()", "T.cex_verification_runs()",
                      "T.vi_worst_case_runs()"]
    else:
        calls += {"INV-001": ["T.criteria_change()", "T.method_comparability()", "T.methods_by_study()",
                              "T.iac_derivation()", "T.worst_case_verification()", "T.calibration_windows()"],
                  "INV-002": ["T.model_adequacy()", "T.adequacy_remedy()", "T.sample_size()"]
                             + [f'T.augmentation_design("{k}")' for k in D.st.DOE_FACTORS if D.has_augmentation(k)],
                  "PCMR-001": ["T.iac_derivation()", "T.worst_case_verification()", "T.methods_by_study()",
                               "T.parameters_by_step()", "T.criteria_change()", "T.studies_overview()",
                               'T.pp_cqa_matrix("studied")', 'T.pp_cqa_matrix("affected")',
                               'T.model_effects_overview(["bioreactor", "protein_a", "viral_inactivation"], label="tbl-model-effects-1")',
                               'T.model_effects_overview(["cex", "aex", "virus_filtration"], label="tbl-model-effects-2")',
                               "T.sdm_offsets()"],
                  "PCMP-001": ["T.iac_derivation()", "T.methods_by_study()", "T.parameters_by_step()"],
                  "PTP-001": ["T.parameters_by_step()", "T.methods_by_study()"],
                  "RA-001": ["T.methods_by_study()"]}.get(doc_id, [])
    for c in calls:
        try:
            t = eval(c, {"T": T})
            w(f"- `{c}` — label `@{t.label}`: {t.caption}\n")
        except Exception as e:  # noqa: BLE001
            w(f"- `{c}` — unavailable ({e})\n")
    w("\n")
    return b.getvalue()


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
      "the four published human sources) and the eleven rules in WRITING_GUIDE §2. This brief "
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
        w("Acceptance = the step's intermediate acceptance criterion (Version 2.0, see §4c): "
          "`D.effective_acceptance(UO, resp)` returns it and `D.acceptance_basis(UO, resp)` says "
          "how it was set. Quality attributes are judged per batch (95 % predictive interval); "
          "viral clearance on the mean LRF across the NOR (`D.decision_statistic(resp)`). Two "
          "flavours per CQA×parameter: the 'PAR (set-point)' column and the NOR-propagated "
          "column. Table: `D.par_table(UO)`; plot a governed CQA with "
          "`D.fig_par(UO, resp, D.governing_factor(UO, resp))`.\n\n")
        try:
            w(D.par_table(key).to_markdown(index=False) + "\n\n")
            gov = {r: D.governing_factor(key, r) for r in D.responses(key)
                   if D.acceptance_for(key, r) is not None}
            if gov:
                w("Governing factor per governed CQA (representative plot): "
                  + ", ".join(f"`{r}`→`{f}`" for r, f in gov.items()) + "\n\n")
        except Exception as e:  # noqa: BLE001
            w(f"_(PAR table unavailable: {e})_\n\n")

    # 4c. Version 2.0 facts ------------------------------------------------------
    w(_rev2_section(doc_id, key, is_report, is_plan, doe))

    # 5. Deviations -------------------------------------------------------------
    w("## 5. Study events — structured facts (author writes the prose; Option A)\n\n")
    w("The events of execution that Version 1.0 recorded, under the DEV numbers it gave them. Version "
      "1.0 called them deviations. This document calls them study events, because a process "
      "characterization study is not GMP manufacture (owner, 2026-10-10). The config field `type` and "
      "the scalar prefix `dev_` keep their Version 1.0 names.\n\n")
    reg_md = P.dev_register(doc_id)
    if not reg_md.strip():
        w("_No study events for this document._\n\n")
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
            w("Study-event scalars available as inline expressions (module globals — "
              "`` `{python} <name>` ``):\n\n")
            for n, v in sorted(scal.items()):
                w(f"- `{n}` = {v}\n")
            w("\n")
    if superseded:
        w("### Superseded study (real re-executed dataset)\n\n")
        w("A study event invalidated the first execution and it was re-run. The first-"
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
    w("- Version 2.0: `REV1`, `REV2`, `INV`, `AMD`, `PLAN_APPROVAL`, `rev1_date(DOC)`, "
      "`CAPA` (DataFrame), `EFFECTIVENESS`, `THRESHOLDS`, `CPK_TARGET`, `CPK_MIN`.\n")
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
