#!/usr/bin/env python3
"""Discourse diagnostics for one or more corpus documents, against the four human sources.

    uv run --extra discourse python authoring/check_discourse.py pc_package/PCR-003_bioreactor.qmd
    uv run --extra discourse python authoring/check_discourse.py --cap --json <qmd> ...

Three measures a writer cannot self-verify without a parser, printed with denominators and the
four source columns so the gap is legible:

  topic chaining  % of sentences whose subject names something the previous sentence mentioned
                  (NOUN/PROPN/ADJ lemma overlap) or is a pronoun
  copula          % of sentences whose ROOT lemma is "be"
  front field     % of sentences with any non-punctuation token before the subject phrase

ADVISORY, NEVER A GATE. A floor on chaining is met by typing a pronoun. Nothing in make test,
make style or make corpus calls this, and it must not be added there.

spaCy is an OPTIONAL extra (`uv sync --extra discourse`). Without it this script prints one
line and exits 0.

--cap reproduces the caps register_analysis.ipynb section 13 used (600 sentences for
chaining, 450 for copula/front field), so the numbers on docs/results/2026-08-17-register-pilot.md
can be reproduced exactly. Without --cap every sentence is measured.

Reuses check_style.prose_from_qmd / prose_from_extract / sentences / HUMAN_SOURCES so it
measures the same text the register gate does.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from check_style import HUMAN_SOURCES, prose_from_extract, prose_from_qmd, sentences  # noqa: E402

DEGRADE = ("check_discourse: spaCy is not installed; this diagnostic is optional. "
           "Install with `uv sync --extra discourse` and re-run. (exit 0)")

CAP_CHAIN, CAP_COPFRONT = 600, 450   # the notebook's caps


def load_nlp():
    try:
        import spacy
    except ImportError:
        return None
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        return None


def prep(text: str) -> list[str]:
    # The notebook parses the gate's sentence list with the NUM placeholder made numeric.
    return [s.replace("NUM", "12.3") for s in sentences(text)]


def topic_chaining(nlp, sents, cap=None):
    docs = [nlp(s) for s in (sents[:cap] if cap else sents)]
    chained = pairs = 0
    for prev, cur in zip(docs, docs[1:]):
        subj = next((t for t in cur if t.dep_ in ("nsubj", "nsubjpass")), None)
        if subj is None:
            continue
        pairs += 1
        prev_l = {t.lemma_.lower() for t in prev if t.pos_ in ("NOUN", "PROPN", "ADJ")}
        subj_l = {t.lemma_.lower() for t in subj.subtree if t.pos_ in ("NOUN", "PROPN", "ADJ")}
        chained += bool(subj_l & prev_l) or subj.pos_ == "PRON"
    return chained, pairs


def copula_front(nlp, sents, cap=None):
    cop = front = n = 0
    for s in (sents[:cap] if cap else sents):
        doc = nlp(s)
        root = next((t for t in doc if t.dep_ == "ROOT"), None)
        subj = next((t for t in doc if t.dep_ in ("nsubj", "nsubjpass")), None)
        if root is None or subj is None:
            continue
        n += 1
        cop += int(root.lemma_ == "be")
        start = min(t.i for t in subj.subtree)
        front += bool([t for t in doc[:start] if not t.is_punct and not t.is_space])
    return cop, front, n


def measure(nlp, text, cap):
    sents = prep(text)
    ch, pairs = topic_chaining(nlp, sents, CAP_CHAIN if cap else None)
    cop, front, n = copula_front(nlp, sents, CAP_COPFRONT if cap else None)
    pct = lambda a, b: 100.0 * a / b if b else 0.0
    return {"chaining_pct": pct(ch, pairs), "chaining": [ch, pairs],
            "copula_pct": pct(cop, n), "copula": [cop, n],
            "front_pct": pct(front, n), "front": [front, n],
            "n_sentences": len(sents)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("qmd", nargs="*")
    ap.add_argument("--cap", action="store_true",
                    help="reproduce the notebook's caps (600 sentences chaining, 450 copula/front)")
    ap.add_argument("--json", action="store_true", help="machine-readable output for build_brief.py")
    ap.add_argument("--no-sources", action="store_true", help="skip the four human columns")
    a = ap.parse_args()

    nlp = load_nlp()
    if nlp is None:
        print(DEGRADE)
        return 0

    cols = []
    if not a.no_sources:
        for name, fname, lo, hi in HUMAN_SOURCES:
            path = os.path.join(ROOT, "refs", "text", fname)
            if os.path.exists(path):
                cols.append((name, measure(nlp, prose_from_extract(path, lo, hi), a.cap)))
    for q in a.qmd:
        if not os.path.exists(q):
            print(f"FAIL  no such file: {q}")
            return 1
        cols.append((os.path.basename(q), measure(nlp, prose_from_qmd(q), a.cap)))
    if not cols:
        print("nothing to measure")
        return 0

    if a.json:
        print(json.dumps({"cap": a.cap, "columns": dict(cols)}, indent=1))
        return 0

    width = max(len(n) for n, _ in cols) + 2
    print("discourse diagnostics (advisory, never gated)" + ("  [notebook caps]" if a.cap else ""))
    print(f"{'measure':<40s}" + "".join(f"{n:>{width}s}" for n, _ in cols))
    for key, cnt, label in (("chaining_pct", "chaining", "topic chaining % (chained/pairs)"),
                            ("copula_pct", "copula", "copula main verb % (copula/n)"),
                            ("front_pct", "front", "adjunct front field % (front/n)")):
        print(f"{label:<40s}" + "".join(
            f"{m[key]:.1f} ({m[cnt][0]}/{m[cnt][1]})".rjust(width) for _, m in cols))
    print(f"{'(sentences of prose)':<40s}" + "".join(f"{m['n_sentences']:>{width}d}" for _, m in cols))
    return 0


if __name__ == "__main__":
    sys.exit(main())
