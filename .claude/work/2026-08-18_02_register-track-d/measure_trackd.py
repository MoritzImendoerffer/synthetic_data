#!/usr/bin/env python3
"""Every measure Track D publishes, from one file, with every denominator.

    uv run --extra discourse python .claude/work/2026-08-18_02_register-track-d/measure_trackd.py \
        $(ls pc_package/*.qmd)
    uv run --extra discourse python .../measure_trackd.py --check-baseline $(ls pc_package/*.qmd)

**No number this round publishes may come from anywhere but this script.** The same failure has
happened twice. Round two's owner-reading counts lived in a heredoc in the session that produced
them, were in no file, and round three's first task had to reconstruct them. The proposal's Track C
figure -- 1.5 % ``, so `` in WRITING_GUIDE.md, "measured 2026-08-17" -- came from an unsaved method
and re-measured at 3.77 % the next day. The two are not comparable and the older one cannot be
checked. A number without a committed method is not stale, it is uncheckable.

It prints four blocks:

  style       exactly ``check_style.py --compare``, which is what measure_baseline_style.txt is
  discourse   exactly ``check_discourse.py``, which is what measure_baseline_discourse.txt is
  extra       the measures round three had to compute by hand and must not have to again:
              the staccato, ``, which`` and its neighbours, and the possessives
  rule        one row per document, the pilot/corpus stopping rule of state.json, with a verdict

``--check-baseline`` re-derives blocks one and two and compares every cell against the two
committed baseline files, to one decimal. That is the acceptance test for this script: if it
disagrees with the baseline, the script is wrong and the baseline is right.

WRAPS THE TWO GATES, DOES NOT RE-IMPLEMENT THEM. check_style.measure and check_discourse.measure
are the authority for everything in blocks one and two; this file adds only block three's measures,
which no gate computes. A second implementation of a measure is a second answer to the same
question.

TWO DENOMINATORS EXIST, ON PURPOSE. check_style's per-1000-word rates divide by the words inside
its sentence list; the possessive block divides by ``len(text.split())``, the whole prose. They
differ by up to 19 % (ISPE TT: 18,731 against 22,216, because the sentence splitter drops
list-shaped lines). The possessive block keeps the whole-prose denominator because that is the one
round three published and this script has to reproduce it.
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

BASE_STYLE = os.path.join(HERE, "measure_baseline_style.txt")
BASE_DISC = os.path.join(HERE, "measure_baseline_discourse.txt")

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
    base_names = (baseline_names(BASE_DISC, DISC_LABEL_W, expected_names(paths, ""))
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
    names = baseline_names(BASE_STYLE, STYLE_COL_0, expected_names(paths, " (human)"))
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
        for i, (name, _) in enumerate(cols):
            colname = names[i] if i < len(names) else None
            if colname is None:
                bad += 1
                continue
            want = base[desc][i]
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
    dnames = baseline_names(BASE_DISC, DISC_LABEL_W, expected_names(paths, ""))
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
    ap.add_argument("qmd", nargs="+")
    ap.add_argument("--no-sources", action="store_true", help="skip the four human columns")
    ap.add_argument("--check-baseline", action="store_true",
                    help="compare blocks one and two against the two committed baseline files")
    ap.add_argument("--blocks", default="style,discourse,extra,rule")
    a = ap.parse_args()

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
    return 0


if __name__ == "__main__":
    sys.exit(main())
