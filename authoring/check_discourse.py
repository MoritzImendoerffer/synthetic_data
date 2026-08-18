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
  passive         % of sentences carrying a passive dependency (nsubjpass or auxpass)
  ', and '+clause % of sentences where a comma + "and" introduces a second finite clause with
                  its own subject

The passive figure is a BAND, never a floor: the four sources sit at 54-60 % of all their
sentences, or 57-64 % on the denominator this script uses, and the corpus plans are already
inside it, so a floor would push a genre that is already right the wrong way.
The and-clause count is the parser's half of a pair; the regex half is check_style.AND_CLAUSE,
and neither is a superset of the other (see _and_clause).

All five share one sentence list, and the last four share one denominator n.

ADVISORY, NEVER A GATE. A floor on chaining is met by typing a pronoun. Nothing in make test,
make style or make corpus calls this, and it must not be added there.

spaCy is an OPTIONAL extra (`uv sync --extra discourse`). Without it this script prints one
line and exits 0.

--cap reproduces the caps register_analysis.ipynb section 13 used (600 sentences for
chaining, 450 for the other four), so the numbers on docs/results/2026-08-17-register-pilot.md
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


def _and_clause(doc) -> bool:
    """A coordinating "and", preceded by a comma, whose conjunct is a finite clause with its own
    subject. Misses long coordinated noun phrases the small model mis-attaches, which is two of
    the three sentences the project owner quoted on 2026-08-18; check_style.AND_CLAUSE covers
    those and misses a second clause opening on a bare noun. Neither is a superset of the other,
    so both are printed and neither is gated."""
    for tok in doc:
        if tok.dep_ == "cc" and tok.lower_ == "and" and tok.i > 0 and doc[tok.i - 1].text == ",":
            for conj in tok.head.children:
                if (conj.dep_ == "conj" and conj.i > tok.i and conj.pos_ in ("VERB", "AUX")
                        and any(c.dep_ in ("nsubj", "nsubjpass", "expl") for c in conj.children)):
                    return True
    return False


def copula_front_passive_and(nlp, sents, cap=None):
    """Four counts over one sentence list, so all four report on the same denominator."""
    cop = front = passive = andc = n = 0
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
        # Counted here rather than in a loop of their own so that passive, and-clause, copula
        # and front field all divide by this n. Round two's heredoc divided the passive by every
        # sentence instead, which is why its figure for a document is a few tenths lower.
        passive += int(any(t.dep_ in ("nsubjpass", "auxpass") for t in doc))
        andc += int(_and_clause(doc))
    return cop, front, passive, andc, n


def measure(nlp, text, cap):
    sents = prep(text)
    ch, pairs = topic_chaining(nlp, sents, CAP_CHAIN if cap else None)
    cop, front, passive, andc, n = copula_front_passive_and(
        nlp, sents, CAP_COPFRONT if cap else None)
    pct = lambda a, b: 100.0 * a / b if b else 0.0
    return {"chaining_pct": pct(ch, pairs), "chaining": [ch, pairs],
            "copula_pct": pct(cop, n), "copula": [cop, n],
            "front_pct": pct(front, n), "front": [front, n],
            "passive_pct": pct(passive, n), "passive": [passive, n],
            "and_clause_pct": pct(andc, n), "and_clause": [andc, n],
            "n_sentences": len(sents)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("qmd", nargs="*")
    ap.add_argument("--cap", action="store_true",
                    help="reproduce the notebook's caps (600 sentences chaining, 450 for the rest)")
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

    rows = (("chaining_pct", "chaining", "topic chaining % (chained/pairs)"),
            ("copula_pct", "copula", "copula main verb % (copula/n)"),
            ("front_pct", "front", "adjunct front field % (front/n)"),
            ("passive_pct", "passive", "passive construction % (passive/n)"),
            ("and_clause_pct", "and_clause", "', and '+clause, parser % (and/n)"))
    width = max(len(n) for n, _ in cols) + 2
    lw = max(len(label) for _, _, label in rows) + 2
    print("discourse diagnostics (advisory, never gated)" + ("  [notebook caps]" if a.cap else ""))
    print("  the passive rate is a BAND and never a floor: the four sources run 54-60 % of all "
          "their sentences,\n  and 57-64 % on this table's denominator n, which is the sentences "
          "that have a root and a subject.\n  The and-clause count is the parser's half of a "
          "pair, and the regex half is check_style.AND_CLAUSE.\n  Copula, front field, passive "
          "and and-clause all divide by that same n.")
    print(f"{'measure':<{lw}s}" + "".join(f"{n:>{width}s}" for n, _ in cols))
    for key, cnt, label in rows:
        print(f"{label:<{lw}s}" + "".join(
            f"{m[key]:.1f} ({m[cnt][0]}/{m[cnt][1]})".rjust(width) for _, m in cols))
    print(f"{'(sentences of prose)':<{lw}s}"
          + "".join(f"{m['n_sentences']:>{width}d}" for _, m in cols))
    return 0


if __name__ == "__main__":
    sys.exit(main())
