"""Pre-characterization risk content for RA-001.

Reuses the curated failure-mode / effect / control ``CONTENT`` dict from
``risk_assessment/build_fmea.py`` (the single content source retained for RA-001,
per ``CLAUDE.md``) together with the A-Mab risk-ranking-and-filtering (RRF)
study-type rule (Tables 5.16/5.17; ``refs/grounding/amab_risk.json``) to produce,
per process parameter, the **pre-characterization** risk and the **assigned
characterization study type** — the scope that feeds each ``PCP-00N``.

Only *initial* (pre-characterization) scoring and the study-type decision are used:
the residual RPN and the CPP/WC-CPP classification are OUTPUTS of the studies, not
inputs to this assessment. The study-type decision (multivariate vs univariate) is
the RRF decision recorded in ``config/parameters.yaml`` (the ``study`` field); the
CQA(s) at risk, prospective failure mode and effect come from ``CONTENT``; the
severity comes from the A-Mab CQA severity map; the initial occurrence/detection
follow the same pre-characterization logic as the FMEA source.
"""
from __future__ import annotations

import os
import re
import sys

import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_RA = os.path.join(_ROOT, "risk_assessment")
if _RA not in sys.path:
    sys.path.insert(0, _RA)

import build_fmea as _F  # noqa: E402  curated CONTENT + severity maps

from _pcpkg import CFG, cqa_reg, UNIT_OP_TITLES, st  # noqa: E402

CONTENT = _F.CONTENT
CQA_SEVERITY = _F.CQA_SEVERITY

# Pre-characterization (initial) occurrence and detection scores, on the A-Mab scales in
# ``config/parameters.yaml`` (``risk.occurrence_scale`` / ``risk.detection_scale``). Held as
# module constants so ``ra_rows`` and the methodology tables RA-001 renders read one
# definition; a literal repeated in both would let the document and the register disagree.
O_QUALITY = 7        # effect on the attribute is not yet quantified
O_PERFORMANCE = 4    # platform-controlled, performance only
D_VIRAL = 10         # viral clearance is not measurable on a routine batch
D_QUALITY = 8        # not seen in-process; caught by release testing
D_PERFORMANCE = 6    # seen at a downstream step before release

_CQA_NAME = {r["key"]: r["cqa"] for _, r in cqa_reg.iterrows()}


def _cqa_label(cqas):
    if cqas == ["performance"]:
        return "process performance"
    return ", ".join(_CQA_NAME.get(c, c) for c in cqas)


def _is_viral(cqas):
    return ("lrv_xmulv" in cqas) or ("lrv_mvm" in cqas)


def ra_rows():
    """Per-parameter pre-characterization risk and assigned study type (list of dicts)."""
    rows = []
    for key in CFG.train_order:
        uo = CFG.unit_op(key)
        title = UNIT_OP_TITLES.get(key, uo.name)
        for p in uo.parameters:
            c = CONTENT.get((key, p.key))
            if not c:
                c = dict(cqas=["performance"], fm="Parameter outside characterized range",
                         eff="No significant product-quality impact expected")
            cqas = c["cqas"]
            quality = cqas != ["performance"]
            sev = max(CQA_SEVERITY.get(x, 4) for x in cqas)
            viral = _is_viral(cqas)
            # pre-characterization (initial) occurrence/detection — same logic as the FMEA source:
            # a quality-impacting parameter has an uncertain effect and poor in-process detection.
            o_init = O_QUALITY if quality else O_PERFORMANCE
            d_init = D_VIRAL if viral else (D_QUALITY if quality else D_PERFORMANCE)
            rpn_init = sev * o_init * d_init
            # RRF study-type decision (Table 5.16): a parameter carried into the unit
            # operation's designed experiment (studies.DOE_FACTORS) is studied multivariately;
            # a quality-impacting parameter studied outside the DoE is a justified univariate
            # study; a performance-only parameter is studied univariately.
            is_doe_factor = p.key in st.DOE_FACTORS.get(key, [])
            if is_doe_factor:
                study = "multivariate DoE"
            elif quality:
                study = "univariate (justified)"
            else:
                study = "univariate"
            if quality and sev >= CFG.risk["thresholds"]["cpp_severity"]:
                prio = "High"
            elif quality:
                prio = "Medium"
            else:
                prio = "Low"
            rows.append(dict(step=uo.step, key=key, unit_op=title, param=p.name, pkey=p.key,
                             cqas=cqas, cqa_label=_cqa_label(cqas), severity=sev, quality=quality,
                             o_init=o_init, d_init=d_init, rpn_init=rpn_init,
                             study=study, priority=prio, fm=c["fm"], eff=c["eff"]))
    return rows


def ra_scope_df():
    """Risk-ranking + study-type table: parameter -> CQA(s) at risk -> severity -> RPN -> study type."""
    rows = ra_rows()
    return pd.DataFrame(
        [[r["step"], r["unit_op"], r["param"], r["cqa_label"], r["severity"],
          r["rpn_init"], r["study"], r["priority"]] for r in rows],
        columns=["Step", "Unit operation", "Parameter", "CQA(s) at risk",
                 "Sev.", "Init. RPN", "Study type", "Priority"])


def cqa_table():
    """The attribute (severity) register RA-001 renders in "Quality attributes at risk".

    Lives here rather than in the ``.qmd`` so that the document and the ground-truth annex
    build the same table from one definition. The annex anchors each ``QualityAttribute``
    record on its rendered row, which only works while the two agree exactly.
    """
    d = cqa_reg.copy()
    d["Acceptance"] = d.apply(lambda r: f"{r.acc_low:g}–{r.acc_high:g} {r.unit}", axis=1)
    d["Set by"] = d["set_by"].map(lambda k: UNIT_OP_TITLES.get(k, k))
    d["Severity"] = d["key"].map(lambda k: CQA_SEVERITY.get(k, 4))
    return d.rename(columns={"cqa": "Quality attribute", "category": "Category",
                             "criticality": "Criticality", "tool1_score": "Tool #1"})[
        ["Quality attribute", "Category", "Acceptance", "Criticality", "Tool #1",
         "Severity", "Set by"]]


def ra_detail_df():
    """Prospective failure-mode / effect table per parameter (for the appendix)."""
    rows = ra_rows()
    return pd.DataFrame(
        [[r["step"], r["param"], r["fm"], r["eff"], r["cqa_label"]] for r in rows],
        columns=["Step", "Parameter", "Potential failure mode", "Potential effect", "CQA(s) at risk"])


def ra_scale_df(kind):
    """One A-Mab scoring scale (``severity`` / ``occurrence`` / ``detection``) from config.

    ``config/parameters.yaml`` ``risk.*_scale`` carries the score, its band label and the
    meaning attached to it. RA-001 renders all three, because a risk assessment that gives
    scores without the scale behind them cannot be reviewed."""
    rows = CFG.risk[f"{kind}_scale"]
    return pd.DataFrame([[r["score"], r["label"], r["meaning"]] for r in rows],
                        columns=["Score", "Band", "Meaning"])


def ra_initial_score_rule_df():
    """How the pre-characterization occurrence and detection scores are assigned.

    The three parameter classes are mutually exclusive and exhaust the register, so the
    parameter counts in the last column sum to ``ra_summary()['n']``."""
    rows = ra_rows()

    def n(pred):
        return sum(1 for r in rows if pred(r))

    return pd.DataFrame([
        ["Impacts a viral-safety attribute", O_QUALITY, D_VIRAL,
         n(lambda r: r["quality"] and _is_viral(r["cqas"]))],
        ["Impacts another quality attribute", O_QUALITY, D_QUALITY,
         n(lambda r: r["quality"] and not _is_viral(r["cqas"]))],
        ["Process performance only", O_PERFORMANCE, D_PERFORMANCE,
         n(lambda r: not r["quality"])],
    ], columns=["Parameter class", "Occurrence", "Detection", "Parameters"])


def ra_study_rule_df():
    """The study-type decision rule, with the number of parameters reaching each outcome."""
    rows = ra_rows()
    n_multi = sum(1 for r in rows if r["study"] == "multivariate DoE")
    n_just = sum(1 for r in rows if r["study"] == "univariate (justified)")
    n_uni = sum(1 for r in rows if r["study"] == "univariate")
    return pd.DataFrame([
        ["multivariate DoE", "Effect expected to depend on the other parameters at the step", n_multi],
        ["univariate (justified)", "Impacts a quality attribute, studied outside the designed experiment", n_just],
        ["univariate", "Process performance only, no expected interaction at the step", n_uni],
        ["no study", "No attribute risk and a range already justified by prior knowledge",
         len(rows) - n_multi - n_just - n_uni],
    ], columns=["Study type", "Basis for the decision", "Parameters"])


def ra_step_overview_df():
    """Per step: parameters carried, how many are linked to a CQA, the study split, top RPN."""
    rows = ra_rows()
    out = []
    for key in CFG.train_order:
        uo = CFG.unit_op(key)
        rs = [r for r in rows if r["key"] == key]
        out.append([uo.step, UNIT_OP_TITLES.get(key, uo.name), len(rs),
                    sum(1 for r in rs if r["quality"]),
                    sum(1 for r in rs if r["study"] == "multivariate DoE"),
                    sum(1 for r in rs if r["study"] != "multivariate DoE"),
                    max(r["rpn_init"] for r in rs)])
    return pd.DataFrame(out, columns=["Step", "Unit operation", "Parameters", "CQA-linked",
                                      "Multivariate", "Univariate", "Highest init. RPN"])


def ra_score_table(key):
    """The risk-ranking rows for one unit operation, with the three scores exposed."""
    rows = [r for r in ra_rows() if r["key"] == key]
    return pd.DataFrame(
        [[r["param"], r["cqa_label"], r["severity"], r["o_init"], r["d_init"],
          r["rpn_init"], r["priority"], r["study"]] for r in rows],
        columns=["Parameter", "CQA(s) at risk", "Sev.", "Occ.", "Det.",
                 "Init. RPN", "Priority", "Study type"])


def _prospective(fm):
    """Re-frame a curated failure mode for a PRE-characterization document.

    ``CONTENT`` is written from the finished process, so several failure modes read
    "outside the characterized range". RA-001 is executed before any study is run and states
    so in §1 and §2.5, so in this document the same range is the one the process description
    *proposes* for characterization. Only the wording changes: the range itself is the
    config ``prange`` either way, and ``build_fmea.py`` keeps the original text for its own
    (post-characterization) use."""
    return _CHAR_RANGE_RE.sub("the range proposed for characterization", fm)


_CHAR_RANGE_RE = re.compile(r"\b(?:the\s+)?characterized range\b")


def ra_mode_table(key):
    """The prospective failure mode and effect for each parameter of one unit operation."""
    rows = [r for r in ra_rows() if r["key"] == key]
    return pd.DataFrame(
        [[r["param"], _prospective(r["fm"]), r["eff"]] for r in rows],
        columns=["Parameter", "Potential failure mode", "Potential effect"])


def ra_assignment_df():
    """The scope handed to each PCP: which parameters go multivariate, which univariate."""
    rows = ra_rows()
    out = []
    for key in CFG.train_order:
        uo = CFG.unit_op(key)
        rs = [r for r in rows if r["key"] == key]
        multi = [r["param"] for r in rs if r["study"] == "multivariate DoE"]
        uni = [r["param"] + (" (justified)" if r["study"] == "univariate (justified)" else "")
               for r in rs if r["study"] != "multivariate DoE"]
        out.append([uo.step, UNIT_OP_TITLES.get(key, uo.name),
                    ", ".join(multi) or "none", ", ".join(uni) or "none",
                    f"PCP-{uo.step:03d} / PCR-{uo.step:03d}"])
    return pd.DataFrame(out, columns=["Step", "Unit operation", "Multivariate DoE",
                                      "Univariate", "Documents"])


def ra_counts():
    """Scalar counts RA-001 states inline (attributes, scores, priority bands)."""
    rows = ra_rows()
    sev_max = max(r["severity"] for r in rows)
    rpn_max = max(r["rpn_init"] for r in rows)
    prio = {b: sum(1 for r in rows if r["priority"] == b) for b in ("High", "Medium", "Low")}
    return dict(
        n_cqa=len(cqa_reg),
        n_critical=int(cqa_reg["criticality"].isin(["H", "VH"]).sum()),
        n_cqa_sev_max=sum(1 for _, r in cqa_reg.iterrows()
                          if CQA_SEVERITY.get(r["key"], 4) == sev_max),
        n_steps=len(CFG.train_order),
        sev_max=sev_max,
        rpn_max=rpn_max,
        rpn_min=min(r["rpn_init"] for r in rows),
        n_at_rpn_max=sum(1 for r in rows if r["rpn_init"] == rpn_max),
        n_viral_params=sum(1 for r in rows if _is_viral(r["cqas"])),
        n_high=prio["High"], n_medium=prio["Medium"], n_low=prio["Low"],
        n_steps_no_cqa=sum(1 for key in CFG.train_order
                           if not any(r["quality"] for r in rows if r["key"] == key)),
    )


def ra_summary():
    """Counts that define the characterization scope handed to the PCPs."""
    rows = ra_rows()
    n = len(rows)
    n_quality = sum(1 for r in rows if r["quality"])
    n_multivariate = sum(1 for r in rows if r["study"] == "multivariate DoE")
    n_just_uni = sum(1 for r in rows if r["study"] == "univariate (justified)")
    n_univariate = n - n_multivariate
    doe_steps = sorted({r["step"] for r in rows if r["study"] == "multivariate DoE"})
    return dict(n=n, n_quality=n_quality, n_perf=n - n_quality,
                n_multivariate=n_multivariate, n_just_uni=n_just_uni, n_univariate=n_univariate,
                n_doe_steps=len(doe_steps), doe_steps=doe_steps)
