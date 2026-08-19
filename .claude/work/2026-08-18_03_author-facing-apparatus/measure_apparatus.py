#!/usr/bin/env python3
"""Every measure the apparatus probe publishes, from one file, with every denominator.

    uv run --extra discourse python .claude/work/2026-08-18_03_author-facing-apparatus/measure_apparatus.py \
        pc_package/PCR-005_protein_a.EXCERPT.qmd pc_package/PCR-005_protein_a.PROBE.qmd
    uv run --extra discourse python .../measure_apparatus.py --blocks frames $(ls pc_package/*.qmd)
    uv run --extra discourse python .../measure_apparatus.py --spans
    uv run --extra discourse python .../measure_apparatus.py --check-baseline $(ls pc_package/*.qmd)

This is ``measure_trackd.py`` from work unit ``2026-08-18_02_register-track-d`` (TASK-002 there),
COPIED here on 2026-08-18 and extended with one block. It was copied rather than imported because
the predecessor's file is a shipped record and an import across work units breaks the day one of
them is archived; it still reads the predecessor's two committed baseline files, because a second
copy of a baseline is a second baseline. ``--check-baseline`` must keep reproducing both.

**No number this unit publishes may come from anywhere but this script.** The failure it closes is
recorded in ``docs/results/2026-08-18-track-d-stopped.md`` §9: the trailing-relative,
``acts through``, ``follows from`` and ``mechanistic_warrant`` counts in that page's §3 and §5.6
were produced by session heredocs and could not be re-run. Block five below is those counts with
code behind them. Where a committed pattern does NOT reproduce the page's hand count, the
disagreement is printed next to the row (``FRAMES_DISAGREE``) instead of the pattern being tuned
to the number.

It prints five blocks:

  style       exactly ``check_style.py --compare``, which is what measure_baseline_style.txt is
  discourse   exactly ``check_discourse.py``, which is what measure_baseline_discourse.txt is
  extra       the measures round three had to compute by hand: the staccato, ``, which`` and its
              neighbours, and the possessives
  rule        one row per document, the Track D stopping rule, with a verdict
  frames      NEW: the trailing-relative family and the mechanism frames the owner's Track D
              reading named, per 100 sentences, sources first
  --spans     NEW, separate switch: the ``mechanistic_warrant`` spans across
              authoring/rhetorical/*.spans.yaml, and which of them carry a flagged frame

WRAPS THE TWO GATES, DOES NOT RE-IMPLEMENT THEM. check_style.measure and check_discourse.measure
are the authority for blocks one and two; sentence splitting and prose extraction for every other
block come from check_style too. A second implementation of a measure is a second answer to the
same question.

TWO DENOMINATORS EXIST, ON PURPOSE. check_style's per-1000-word rates divide by the words inside
its sentence list; the possessive block divides by ``len(text.split())``, the whole prose. The
frames block divides OCCURRENCES by the sentence count, exactly as ``SENT_PATTERNS`` does, because
that is what reproduces the results page (513 ``, which`` in 5,226 sentences = 9.82).
"""
from __future__ import annotations

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "authoring"))

from check_style import (  # noqa: E402
    HUMAN_SOURCES, compare, measure as style_measure, prose_from_extract, prose_from_qmd,
    sentences,
)

# The two committed baselines live in the predecessor unit and are read from there. Not copied.
PRED = os.path.join(HERE, "..", "2026-08-18_02_register-track-d")
BASE_STYLE = os.path.join(PRED, "measure_baseline_style.txt")
BASE_DISC = os.path.join(PRED, "measure_baseline_discourse.txt")

# --------------------------------------------------------------------------------------
# Block three. The measures round three computed in a session and left in a .txt with no
# method behind it. Each pattern below was recovered by re-deriving round three's published
# figures for all four human sources and keeping only the pattern that reproduces them.
# --------------------------------------------------------------------------------------
SHORT_WORDS = 15      # "short sentence", the same threshold as check_style.pct_under_15
RUN_MIN = 3           # a staccato run is three or more short sentences in a row

# OCCURRENCES over the whole prose, divided by the sentence count -- a rate per 100 sentences,
# NOT the share of sentences that carry one. The distinction is not cosmetic and it is not a
# choice: it is what reproduces round three's file. PCR-003 carries 67 ", which" in 66 sentences
# because one sentence has two, and the published 15.33 % is 67/437, not 66/437. The semicolon
# row separates the two further still -- PCR-003 has 6 semicolons and only 1 of them is inside a
# sentence the splitter kept, so counting sentences gives 0.23 against the published 1.37.
# ", which" is the measure that moved: round three traded coordinated clauses for trailing
# relatives and this rose 5.8 points while nothing printed it back to the author.
SENT_PATTERNS = [
    (", which",   re.compile(r",\s+which\b", re.I)),
    (", where",   re.compile(r",\s+where\b", re.I)),
    ("semicolon", re.compile(r";")),
    (", because", re.compile(r",\s+because\b", re.I)),
]

# Per 1000 words of whole prose. "the <noun> is" allows one optional word between the article
# and the verb ("the design space is", "the process is") -- that optional word is what makes it
# reproduce round three's four source counts exactly, 76 / 168 / 76 / 138.
WORD_PATTERNS = [
    ("its",           re.compile(r"\bits\b", re.I)),
    ("their",         re.compile(r"\btheir\b", re.I)),
    ("it is/was",     re.compile(r"\bit (?:is|was)\b", re.I)),
    ("the <noun> is", re.compile(r"\bthe \w+(?: \w+)? (?:is|are|was|were)\b", re.I)),
]

# `it is/was` is the ONE measure here that does not reproduce round three's file. This pattern
# gives 18 / 28 / 40 / 50 on the four sources against the published 22 / 28 / 41 / 50, and 3
# against 4 on PCP-003; it agrees on A-Mab, ISPE PV and PCR-003. Every candidate that lifts PDA
# to 22 overshoots the other three, so the shape of round three's pattern cannot be recovered
# from its output, and its method was never saved. The published figure is therefore not stale,
# it is uncheckable -- which is the failure this whole task exists to end. The number this
# script prints is the one with code behind it.
IT_IS_DISAGREES = ("round three published 22 / 28 / 41 / 50 on the sources and 4 on PCP-003; "
                   "this pattern gives 18 / 28 / 40 / 50 and 3. Its method was not saved.")
# For the record of what DOES reproduce: every other measure in this block matches round three's
# measure_staccato.txt and measure_whatpaid.txt exactly, on all four sources and on both
# documents those files cover -- the staccato runs, longest run and share; ", which"; ", where";
# the semicolon; ", because"; "its"; "their"; and "the <noun> is". Only "it is/was" does not.

# --------------------------------------------------------------------------------------
# Block five. The frames the owner's Track D reading named (docs/results/2026-08-18-track-d-stopped.md
# §3, §4, §5.6), which that page counted in session heredocs. OCCURRENCES per 100 sentences,
# sentence count from check_style.sentences over the same prose.
#
# What reproduces the page and what does not, measured 2026-08-18 over all 20 documents
# (5,226 sentences):
#   ", which"                513 (9.82)   reproduces
#   quantifier of which       20 (0.38)   reproduces ONLY with the list below, which carries no
#                                         numeral: with one|two|three added it reads 23, and the
#                                         page's own union (all trailing relatives 595 = 513 + 20
#                                         + 46 ", where" + 16 ", whose") is exact only at 20.
#   all trailing relatives   595 (11.39)  reproduces, as that union
#   acts on / acts through    63 (1.21)   reproduces
#   aggressive(ness)           2          reproduces
#   follows from the          14 (0.27)   page says 12 (0.23); singular-only "follows from the"
#                                         reads 10; no pattern reads 12. See FRAMES_DISAGREE.
#   governs / sets <noun>     97 (1.86)   page says 108 (2.07); "governs" alone is 67 and
#                                         "sets <determiner>" 30; no defensible pattern reads 108.
# The last two are printed with the disagreement beside them. The page's numbers came from an
# unsaved method and are uncheckable; the numbers here are the ones with code behind them.
# --------------------------------------------------------------------------------------
_Q = r"(?:none|all|both|each|some|most|several|many|neither|either)"
_DET = r"(?:the|a|an|its|their|this|that|these|those|how|which|what|whether)"
FRAME_PATTERNS = [
    # (label, regex, group) -- group "rel" rows are summed into "all trailing relatives"
    (", which",                 re.compile(r",\s+which\b", re.I),                     "rel"),
    ("<quantifier> of which",   re.compile(r"\b" + _Q + r"\s+of\s+which\b", re.I),   "rel"),
    (", where",                 re.compile(r",\s+where\b", re.I),                     "rel"),
    (", whose",                 re.compile(r",\s+whose\b", re.I),                     "rel"),
    ("acts on / acts through",  re.compile(r"\bacts?\s+(?:on|through)\b", re.I),      "mech"),
    ("follows from the",        re.compile(r"\bfollows?\s+from\s+the\b", re.I),      "mech"),
    ("governs / sets <noun>",   re.compile(r"\bgoverns\b|\bsets\s+" + _DET + r"\b", re.I), "mech"),
    ("aggressive(ness)",        re.compile(r"\baggressive(?:ness)?\b", re.I),         "mech"),
    ("behaves as",              re.compile(r"\bbehaves?\s+as\b", re.I),               "hollow"),
    ("physical chemistry",      re.compile(r"\bphysical chemistry\b", re.I),          "hollow"),
    ("consistent with the",     re.compile(r"\bconsistent with the\b", re.I),         "hollow"),
    ("confirms the expectation", re.compile(r"\bconfirms?\s+the\s+expectations?\b", re.I), "hollow"),
    ("by the mechanism",        re.compile(r"\bby the mechanism\b", re.I),            "hollow"),
]
FRAMES_DISAGREE = {
    "follows from the": "results page §3 says 12 (0.23) from an unsaved pattern; this reads 14",
    "governs / sets <noun>": "results page §3 says 108 (2.07) from an unsaved pattern; this reads 97",
}

# The mechanistic_warrant audit (results page §5.6). A span "carries a flagged frame" when its
# quote matches one of these. The page counted 6 of 26 by hand; this pattern finds a seventh,
# PCR-006-R14 ("The surfaces behave as acid denaturation kinetics predict"), which is "behave as
# <X> predicts" -- a comparison, not the category-label frame the other six are. It is printed
# and left to the reader; the regex is a floor for a human judgement, not the judgement.
SPAN_FLAG = re.compile(r"\bbehaves?\s+as\b|\bacts?\s+(?:on|through)\b|\bfollows?\s+from\b"
                       r"|\baggressive", re.I)


def frames_measure(text: str) -> dict:
    sents = sentences(text)
    n = len(sents)
    out = {"_n_sent": n}
    rel = 0
    for label, pat, group in FRAME_PATTERNS:
        c = len(pat.findall(text))
        out[label] = c
        if group == "rel":
            rel += c
    out["all trailing relatives"] = rel
    return out


def print_frames_block(cols) -> None:
    print("\n== frames the Track D reading named, per 100 sentences (count) ==")
    ms = [(name, frames_measure(text)) for name, text in cols]
    width = max(len(n) for n, _ in ms) + 2
    lw = 30
    print(f"{'frame':<{lw}s}" + "".join(f"{n:>{width}s}" for n, _ in ms))

    def row(label, key):
        cells = []
        for _, m in ms:
            n = m["_n_sent"]
            cells.append(f"{100.0 * m[key] / n if n else 0.0:.2f} ({m[key]})".rjust(width))
        note = f"   [{FRAMES_DISAGREE[key]}]" if key in FRAMES_DISAGREE else ""
        print(f"{label:<{lw}s}" + "".join(cells) + note)

    for label, _, group in FRAME_PATTERNS:
        if group == "rel":
            row(label, label)
    row("all trailing relatives", "all trailing relatives")
    for label, _, group in FRAME_PATTERNS:
        if group == "mech":
            row(label, label)
    print(f"{'-- hollow-warrant frames':<{lw}s}")
    for label, _, group in FRAME_PATTERNS:
        if group == "hollow":
            row(label, label)
    print(f"{'(sentences)':<{lw}s}" + "".join(f"{m['_n_sent']:>{width}d}" for _, m in ms))
    # The corpus total, when more than one document was passed, so the results-page column
    # (all 20 documents as one) is printed rather than left to the reader to sum.
    docs = [(n, m) for n, m in ms if n.endswith(".qmd")]
    if len(docs) > 1:
        tot_n = sum(m["_n_sent"] for _, m in docs)
        print(f"\n  corpus total over {len(docs)} documents, {tot_n} sentences:")
        keys = [l for l, _, _ in FRAME_PATTERNS] + ["all trailing relatives"]
        for k in keys:
            c = sum(m[k] for _, m in docs)
            print(f"    {k:<28s} {100.0 * c / tot_n:6.2f} ({c})")


def print_spans_block() -> int:
    """The mechanistic_warrant spans and which carry a flagged frame. Exit 0 always."""
    import glob
    import yaml
    print("\n== mechanistic_warrant spans, authoring/rhetorical/*.spans.yaml ==")
    total, flagged = 0, []
    for f in sorted(glob.glob(os.path.join(ROOT, "authoring", "rhetorical", "*.spans.yaml"))):
        d = yaml.safe_load(open(f, encoding="utf-8"))
        spans = d if isinstance(d, list) else d.get("spans", [])
        for sp in spans:
            if sp.get("role") != "mechanistic_warrant":
                continue
            total += 1
            m = SPAN_FLAG.search(sp.get("quote", ""))
            if m:
                flagged.append((os.path.basename(f), sp["id"], m.group(0)))
    print(f"  {total} spans labelled mechanistic_warrant; {len(flagged)} carry a flagged frame:")
    for f, sid, frame in flagged:
        print(f"    {sid:<14s} {f:<24s} {frame!r}")
    print("  (results page §5.6 counted 6 by hand; a seventh, PCR-006-R14 'behave as ... predict',"
          " is a comparison and is listed, not judged)")
    return 0

# --------------------------------------------------------------------------------------
# The stopping rule, copied from state.json decisions.pilot_stopping_rule / corpus_stopping_rule.
# (label, key, lo, hi) -- None is unbounded on that side. Chaining and copula are per-document
# against that document's own baseline and are handled separately.
# --------------------------------------------------------------------------------------
RULE = [
    ("', so '",          "_pct_so_mid",       None, 1.0),
    ("opens w/ conn.",   "_pct_initial_conn", 3.0, None),
    ("', and '+clause",  "_pct_and_clause",   None, 3.4),
    ("', not '",         "_pct_not_tail",     None, 0.2),
]
PASSIVE_LO, PASSIVE_HI = 53.0, 68.0
COPULA_SLACK = 2.0     # copula may not sit more than 2 points above its own baseline
# The baseline files carry one decimal, so a document measured against its own baseline can
# differ by up to half a printed digit through rounding alone. Without this, every unchanged
# document reads "chaining -0.0, FAIL" -- which is what it did before the tolerance was added.
ROUND_TOL = 0.05

# The six cells procedures/TASK-002.md names as the fixture: "the ones a mistake would move".
# (block, baseline row label, column, expected value to one decimal)
FIXTURES = [
    ("discourse", "passive construction % (passive/n)", "PCP-005_protein_a.qmd", 66.7),
    ("discourse", "passive construction % (passive/n)", "PCP-008_aex.qmd", 67.7),
    ("discourse", "passive construction % (passive/n)", "RA-001_risk_assessment.qmd", 64.2),
    ("style", "% sentences with mid-sentence ', so ' (not gated)",
     "RA-001_risk_assessment.qmd", 14.6),
    ("style", "% sentences with ', and ' + a second clause (floor; not gated)",
     "PCR-004_harvest.qmd", 29.3),
    ("style", "% sentences with ', and ' + a second clause (floor; not gated)",
     "PCR-003_bioreactor.qmd", 0.5),
]


def staccato(sents: list[str]) -> tuple[int, int, int]:
    """(number of runs, longest run, sentences inside a run) of 3+ consecutive short sentences."""
    runs, cur = [], 0
    for s in sents:
        if len(s.split()) < SHORT_WORDS:
            cur += 1
            continue
        if cur >= RUN_MIN:
            runs.append(cur)
        cur = 0
    if cur >= RUN_MIN:
        runs.append(cur)
    return len(runs), (max(runs) if runs else 0), sum(runs)


def extra_measure(text: str) -> dict:
    sents = sentences(text)
    n, words = len(sents), len(text.split())
    n_runs, longest, inside = staccato(sents)
    out = {"_n_sent": n, "_n_words_prose": words,
           "staccato_runs": n_runs, "staccato_longest": longest,
           "staccato": [inside, n], "staccato_pct": 100.0 * inside / n if n else 0.0}
    for label, pat in SENT_PATTERNS:
        c = len(pat.findall(text))
        out[label] = [c, n]
        out[label + "_pct"] = 100.0 * c / n if n else 0.0
    for label, pat in WORD_PATTERNS:
        c = len(pat.findall(text))
        out[label] = [c, words]
        out[label + "_per1k"] = 1000.0 * c / words if words else 0.0
    return out


def columns(paths: list[str], no_sources: bool):
    """(name, prose) per column: the four human sources first, then each document."""
    cols = []
    if not no_sources:
        for name, fname, lo, hi in HUMAN_SOURCES:
            p = os.path.join(ROOT, "refs", "text", fname)
            if os.path.exists(p):
                cols.append((name, prose_from_extract(p, lo, hi)))
    for p in paths:
        cols.append((os.path.basename(p), prose_from_qmd(p)))
    return cols


# --------------------------------------------------------------------------------------
# Baseline parsing. Both baseline files are fixed-width tables whose first column is a label
# and whose remaining columns are one per source/document. A cell is either a bare number or
# "12.3 (45/678)"; only the leading number is compared.
# --------------------------------------------------------------------------------------
# check_style.compare hard-codes a 62-character label field; check_discourse derives its own
# from its row labels, so ask it rather than guessing.
STYLE_LABEL_W = 62
STYLE_COL_0 = 62 + 11   # compare() prints a band column between the label and the first source
DISC_ROWS = (("chaining_pct", "chaining", "topic chaining % (chained/pairs)"),
             ("copula_pct", "copula", "copula main verb % (copula/n)"),
             ("front_pct", "front", "adjunct front field % (front/n)"),
             ("passive_pct", "passive", "passive construction % (passive/n)"),
             ("and_clause_pct", "and_clause", "', and '+clause, parser % (and/n)"))
DISC_LABEL_W = max(len(label) for _, _, label in DISC_ROWS) + 2

CELL = re.compile(r"\d")


def parse_baseline(path: str, label_width: int) -> dict:
    """{row label -> [leading number per column]} for every row that carries numbers.

    A cell is either "12.3" or "12.3 (45/678)"; only the leading number is read. Tokens that
    are not numbers are skipped, which is how the style table's band column ("20.0-30.5",
    "<=9.5") is passed over without a special case for it.
    """
    rows = {}
    for line in open(path, encoding="utf-8").read().splitlines():
        label, rest = line[:label_width].strip(), line[label_width:]
        if not label or not CELL.search(rest):
            continue
        vals = []
        for tok in re.findall(r"\S+(?: \(\d+/\d+\))?", rest):
            try:
                vals.append(float(tok.split()[0]))
            except ValueError:
                continue
        if vals:
            rows[label] = vals
    return rows


def print_style_block(paths: list[str]) -> None:
    print("== style (check_style.py --compare; reproduces measure_baseline_style.txt) ==")
    compare(paths)


def discourse_columns(cols):
    import check_discourse as D
    nlp = D.load_nlp()
    if nlp is None:
        return None
    return [(name, D.measure(nlp, text, False)) for name, text in cols]


def print_discourse_block(dcols) -> None:
    print("\n== discourse (check_discourse.py; reproduces measure_baseline_discourse.txt) ==")
    if dcols is None:
        print("  spaCy is not installed. Re-run with `uv run --extra discourse python ...`.")
        return
    rows = (("chaining_pct", "chaining", "topic chaining % (chained/pairs)"),
            ("copula_pct", "copula", "copula main verb % (copula/n)"),
            ("front_pct", "front", "adjunct front field % (front/n)"),
            ("passive_pct", "passive", "passive construction % (passive/n)"),
            ("and_clause_pct", "and_clause", "', and '+clause, parser % (and/n)"))
    width = max(len(n) for n, _ in dcols) + 2
    lw = max(len(label) for _, _, label in rows) + 2
    print(f"{'measure':<{lw}s}" + "".join(f"{n:>{width}s}" for n, _ in dcols))
    for key, cnt, label in rows:
        print(f"{label:<{lw}s}" + "".join(
            f"{m[key]:.1f} ({m[cnt][0]}/{m[cnt][1]})".rjust(width) for _, m in dcols))
    print(f"{'(sentences of prose)':<{lw}s}"
          + "".join(f"{m['n_sentences']:>{width}d}" for _, m in dcols))


def print_extra_block(cols) -> None:
    print("\n== the measures round three computed by hand ==")
    ms = [(name, extra_measure(text)) for name, text in cols]
    width = max(len(n) for n, _ in ms) + 2
    lw = 56
    print(f"{'measure':<{lw}s}" + "".join(f"{n:>{width}s}" for n, _ in ms))
    print(f"{'staccato: sentences in a run of 3+ under 15 words':<{lw}s}"
          + "".join(f"{m['staccato_pct']:.1f} ({m['staccato'][0]}/{m['staccato'][1]})".rjust(width)
                   for _, m in ms))
    print(f"{'  runs / longest run':<{lw}s}"
          + "".join(f"{m['staccato_runs']} / {m['staccato_longest']}".rjust(width) for _, m in ms))
    for label, _ in SENT_PATTERNS:
        print(f"{'%s per 100 sentences (count/sentences)' % label:<{lw}s}"
              + "".join(f"{m[label + '_pct']:.1f} ({m[label][0]}/{m[label][1]})".rjust(width)
                       for _, m in ms))
    for label, _ in WORD_PATTERNS:
        note = "  [see IT_IS_DISAGREES]" if label == "it is/was" else ""
        print(f"{'%s per 1k words%s' % (label, note):<{lw}s}"
              + "".join(f"{m[label + '_per1k']:.2f} ({m[label][0]})".rjust(width) for _, m in ms))
    print(f"{'(words of prose / sentences)':<{lw}s}"
          + "".join(f"{m['_n_words_prose']} / {m['_n_sent']}".rjust(width) for _, m in ms))


def print_rule_block(paths: list[str], dcols) -> int:
    """One row per document, every stopping-rule measure with its denominator, and a verdict."""
    print("\n== stopping rule, one row per document ==")
    print("  bands: ', so ' <=1.0 · opens with a connective >=3.0 · ', and '+clause <=3.4 ·")
    print("         ', not ' <=0.2 · passive 53.0-68.0 · chaining >= own baseline ·")
    print("         copula <= own baseline + 2.0.  Chaining and copula need the discourse block.")
    base = parse_baseline(BASE_DISC, DISC_LABEL_W) if os.path.exists(BASE_DISC) else {}
    base_names = (baseline_names(BASE_DISC, DISC_LABEL_W, baseline_column_names(""))
                  if os.path.exists(BASE_DISC) else [])
    dmap = {n: m for n, m in (dcols or [])}
    heads = [label for label, _, _, _ in RULE] + ["passive", "chaining", "copula"]
    print(f"{'document':<32s}" + "".join(f"{h:>20s}" for h in heads) + "   verdict")
    worst = 0
    for p in paths:
        name = os.path.basename(p)
        m = style_measure(prose_from_qmd(p))[0]
        cells, fails = [], []
        for label, key, lo, hi in RULE:
            v, c = m[key], m[key.replace("_pct", "_n", 1)]
            ok = (hi is None or v <= hi) and (lo is None or v >= lo)
            cells.append(f"{v:.1f} ({c}/{m['_n_sent']})")
            if not ok:
                fails.append(label)
        d = dmap.get(name)
        if d:
            pv = d["passive_pct"]
            cells.append(f"{pv:.1f} ({d['passive'][0]}/{d['passive'][1]})")
            if not (PASSIVE_LO <= pv <= PASSIVE_HI):
                fails.append("passive")
            for label, key, cnt, cmp_ in (("chaining", "chaining_pct", "chaining", "ge"),
                                          ("copula", "copula_pct", "copula", "le")):
                v = d[key]
                b = baseline_value(base, base_names, name,
                                   "topic chaining % (chained/pairs)" if label == "chaining"
                                   else "copula main verb % (copula/n)")
                if b is None:
                    cells.append(f"{v:.1f} (no base)")
                    continue
                delta = v - b
                cells.append(f"{v:.1f} ({delta:+.1f})")
                if cmp_ == "ge" and delta < -ROUND_TOL:
                    fails.append("chaining")
                if cmp_ == "le" and delta > COPULA_SLACK + ROUND_TOL:
                    fails.append("copula")
        else:
            cells += ["-", "-", "-"]
        verdict = "PASS" if not fails else "FAIL: " + ", ".join(fails)
        worst = max(worst, 0 if not fails else 1)
        print(f"{name:<32s}" + "".join(c.rjust(20) for c in cells) + "   " + verdict)
    return worst


def expected_names(paths: list[str], human_suffix: str) -> list[str]:
    """The column order both baselines were produced in: four sources, then the documents."""
    return ([n + human_suffix for n, _, _, _ in HUMAN_SOURCES]
            + [os.path.basename(p) for p in paths])


def baseline_column_names(human_suffix: str) -> list[str]:
    """The column order of the COMMITTED baselines, which is independent of what was passed.

    Both baseline files were produced over the four sources and then every ``pc_package/*.qmd``
    in sorted order. Deriving the column list from the caller's paths instead works only when
    the caller passes all twenty; a subset -- the pilot is four documents -- then shifts every
    column and the header check rejects the whole table, which is how the pilot table came back
    with "no base" in the chaining and copula cells. Reconstructing the baseline's own column
    list lets a subset be looked up by name.
    """
    import glob
    # Untracked working files -- <DOC>_<uo>.DRAFT.qmd, .PROBE.qmd, .EXCERPT.qmd -- were not
    # in the baseline and must not shift its columns; the uppercase suffix is the convention.
    docs = sorted(os.path.basename(q) for q in
                  glob.glob(os.path.join(ROOT, "pc_package", "*.qmd"))
                  if not re.search(r"\.[A-Z]+\.qmd$", os.path.basename(q)))
    return [n + human_suffix for n, _, _, _ in HUMAN_SOURCES] + docs


def baseline_names(path: str, col_offset: int, expect: list[str]) -> list[str]:
    """The header columns of a baseline file, VERIFIED against the order we expect.

    A source name contains spaces ("PDA TR 60"), so the header cannot be tokenised on
    whitespace -- doing that silently shifts every column and every comparison then reads the
    wrong document. Both tables are right-aligned in fields of one width, so the header is
    sliced at that width and each slice is checked against the name we expect there. A
    mismatch is reported and the column is dropped rather than compared against its neighbour.
    """
    width = max(len(n) for n in expect) + 2
    header = ""
    for line in open(path, encoding="utf-8").read().splitlines():
        if line.startswith("measure") or line.startswith("metric"):
            header = line
            break
    if not header:
        print(f"MISS  {os.path.basename(path)}: no header row")
        return []
    rest = header[col_offset:]
    got = []
    for i, name in enumerate(expect):
        cell = rest[i * width:(i + 1) * width].strip()
        if cell != name:
            print(f"MISS  {os.path.basename(path)} column {i}: header says {cell!r}, "
                  f"expected {name!r}")
            got.append(None)
        else:
            got.append(name)
    return got


def baseline_value(base: dict, names: list[str], col: str, row: str):
    if row not in base or col not in names:
        return None
    i = names.index(col)
    vals = base[row]
    return vals[i] if i < len(vals) else None


def check_baseline(paths: list[str], dcols) -> int:
    """Every cell of blocks one and two against the two committed baselines, to one decimal."""
    bad = 0
    print("\n== --check-baseline ==")

    cols = columns(paths, False)
    names = baseline_names(BASE_STYLE, STYLE_COL_0, baseline_column_names(" (human)"))
    base = parse_baseline(BASE_STYLE, STYLE_LABEL_W)
    got = {n: style_measure(t)[0] for n, t in cols}
    from check_style import LIMITS
    style_rows = [(desc, key) for key, (_, _, desc) in LIMITS.items()] + [
        ("% sentences with mid-sentence ', so ' (not gated)", "_pct_so_mid"),
        ("% sentences opening with a connective (not gated)", "_pct_initial_conn"),
        ("% sentences with 2+ clause coordinators (not gated)", "_pct_coord2"),
        ("% sentences with ', and ' + a second clause (floor; not gated)", "_pct_and_clause"),
        ("% sentences with mid-sentence ', not ' (not gated)", "_pct_not_tail"),
    ]
    n_cell = 0
    for desc, key in style_rows:
        if desc not in base:
            print(f"MISS  style row not in baseline: {desc}")
            bad += 1
            continue
        for name, _ in cols:
            # The style baseline suffixes the four source columns " (human)"; the run names
            # them bare. The predecessor's TASK-007 commit switched to lookup by name and
            # forgot the suffix, so its --check-baseline skipped all four source columns as
            # MISS (68 lines) and compared 340 cells where its TASK-002 outcome records 408.
            colname = name if name in names else name + " (human)"
            if colname not in names:
                print(f"MISS  style column not in baseline: {name}")
                bad += 1
                continue
            want = base[desc][names.index(colname)]
            have = round(got[name][key], 1)
            n_cell += 1
            if abs(want - have) > 0.051:
                print(f"FAIL  style {desc} / {colname}: baseline {want}, script {have}")
                bad += 1
    print(f"style: {n_cell} cells compared, {bad} disagreement(s)")

    if dcols is None:
        print("discourse: SKIPPED, spaCy not installed -- run with `uv run --extra discourse`")
        return 1
    dbase = parse_baseline(BASE_DISC, DISC_LABEL_W)
    dnames = baseline_names(BASE_DISC, DISC_LABEL_W, baseline_column_names(""))
    d_bad, d_cell = 0, 0
    for key, row in (("chaining_pct", "topic chaining % (chained/pairs)"),
                     ("copula_pct", "copula main verb % (copula/n)"),
                     ("front_pct", "adjunct front field % (front/n)"),
                     ("passive_pct", "passive construction % (passive/n)"),
                     ("and_clause_pct", "', and '+clause, parser % (and/n)")):
        for name, m in dcols:
            want = baseline_value(dbase, dnames, name, row)
            if want is None:
                print(f"MISS  discourse {row} / {name}: not in baseline")
                d_bad += 1
                continue
            have = round(m[key], 1)
            d_cell += 1
            if abs(want - have) > 0.051:
                print(f"FAIL  discourse {row} / {name}: baseline {want}, script {have}")
                d_bad += 1
    print(f"discourse: {d_cell} cells compared, {d_bad} disagreement(s)")

    # The six named cells, printed one by one. A whole-table count of zero already covers them,
    # but the procedure names these six as the fixture and a reader should not have to trust a
    # total to see them.
    f_bad = 0
    smap = {n: m for n, m in ((n, style_measure(tx)[0]) for n, tx in cols)}
    skeys = {"% sentences with mid-sentence ', so ' (not gated)": "_pct_so_mid",
             "% sentences with ', and ' + a second clause (floor; not gated)": "_pct_and_clause"}
    dkeys = {"passive construction % (passive/n)": "passive_pct"}
    print("the six fixture cells:")
    for block, row, col, want in FIXTURES:
        if block == "style":
            have = round(smap[col][skeys[row]], 1)
            base_v = baseline_value(base, names, col, row)
        else:
            have = round(dict(dcols)[col][dkeys[row]], 1)
            base_v = baseline_value(dbase, dnames, col, row)
        ok = abs(have - want) <= 0.051 and base_v is not None and abs(base_v - want) <= 0.051
        f_bad += 0 if ok else 1
        print(f"  {'OK  ' if ok else 'FAIL'} {col:<30s} {row[:46]:<48s} "
              f"want {want:>5.1f}  script {have:>5.1f}  baseline {base_v}")
    return 1 if (bad or d_bad or f_bad) else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("qmd", nargs="*")
    ap.add_argument("--no-sources", action="store_true", help="skip the four human columns")
    ap.add_argument("--check-baseline", action="store_true",
                    help="compare blocks one and two against the two committed baseline files")
    ap.add_argument("--blocks", default="style,discourse,extra,rule,frames")
    ap.add_argument("--spans", action="store_true",
                    help="audit the mechanistic_warrant spans in authoring/rhetorical/ and exit")
    a = ap.parse_args()

    if a.spans:
        return print_spans_block()

    for p in a.qmd:
        if not os.path.exists(p):
            print(f"FAIL  no such file: {p}")
            return 1
    want = set(a.blocks.split(","))
    cols = columns(a.qmd, a.no_sources)
    dcols = discourse_columns(cols) if ("discourse" in want or "rule" in want
                                        or a.check_baseline) else None

    if a.check_baseline:
        return check_baseline(a.qmd, dcols)
    if "style" in want:
        print_style_block(a.qmd)
    if "discourse" in want:
        print_discourse_block(dcols)
    if "extra" in want:
        print_extra_block(cols)
    if "rule" in want:
        print_rule_block(a.qmd, dcols)
    if "frames" in want:
        print_frames_block(cols)
    return 0


if __name__ == "__main__":
    sys.exit(main())
