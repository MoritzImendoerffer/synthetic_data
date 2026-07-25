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

_CQA_NAME = {r["key"]: r["cqa"] for _, r in cqa_reg.iterrows()}


def _cqa_label(cqas):
    if cqas == ["performance"]:
        return "process performance"
    return ", ".join(_CQA_NAME.get(c, c) for c in cqas)


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
            viral = ("lrv_xmulv" in cqas) or ("lrv_mvm" in cqas)
            # pre-characterization (initial) occurrence/detection — same logic as the FMEA source:
            # a quality-impacting parameter has an uncertain effect and poor in-process detection.
            o_init = 7 if quality else 4
            d_init = 10 if viral else (8 if quality else 6)
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
            if quality and sev >= 8:
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


def ra_detail_df():
    """Prospective failure-mode / effect table per parameter (for the appendix)."""
    rows = ra_rows()
    return pd.DataFrame(
        [[r["step"], r["param"], r["fm"], r["eff"], r["cqa_label"]] for r in rows],
        columns=["Step", "Parameter", "Potential failure mode", "Potential effect", "CQA(s) at risk"])


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
