#!/usr/bin/env python3
"""Register gate — is the prose plain technical English, or is it AI-flavoured?

    uv run python authoring/check_style.py pc_package/PCR-003_bioreactor.qmd
    uv run python authoring/check_style.py --selftest        # the human sources must pass
    uv run python authoring/check_style.py <qmd> --report    # numbers only, never fails
    uv run python authoring/check_style.py <qmd>... --compare  # table vs the human sources

Why this exists
---------------
The corpus's first-pass reports were written to a guide whose voice exemplar had been
distilled from an earlier AI-written report, so the register drifted into a recognisable
machine idiom: 34-word average sentences, an em-dash aside in every third sentence, a
semicolon splice in every fourth, coined compound superlatives, and a "what this means"
coda welded onto every paragraph.

The thresholds below are not taste. They are read off the two published human documents
the corpus is built on:

    refs/text/pda60.txt   PDA Technical Report No. 60, Process Validation (2013)
    refs/text/amab.txt    A-Mab: A Case Study in Bioprocess Development (2009)

``--selftest`` runs the gate against both of them. **Any threshold this file asserts must
be one that real human regulatory prose passes** — if a rule fails the self-test, the rule
is wrong, not the source. Tighten a threshold only after re-running the self-test.

Scope: prose only. Code chunks, YAML, tables, captions, cross-reference labels, the
abbreviations run and inline ``{python}`` expressions are stripped before measuring, so
the metrics describe what the assessor actually reads.
"""
from __future__ import annotations

import argparse
import os
import re
import statistics as stat
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# --------------------------------------------------------------------------------------
# Thresholds. Every one of these is satisfied by BOTH human sources (see --selftest).
# --------------------------------------------------------------------------------------
# Each entry is (lo, hi, description); None means unbounded on that side.
#
# Several bands are TWO-SIDED on purpose. Capping sentence length alone pushes an author
# into staccato prose — 17-word averages and 40 % of sentences under 15 words — which is
# just as unlike real regulatory writing as the 34-word sprawl it replaced. Human technical
# prose sits in a band, not at a minimum, so the gate enforces a band.
LIMITS = {
    # sentence-length distribution ------------------------------------------------
    "mean_len":      (20.0, 28.0, "mean sentence length (words)"),
    "median_len":    (18.0, 25.0, "median sentence length (words)"),
    "pct_over_40":   ( 3.0, 16.0, "% of sentences over 40 words"),
    "pct_over_55":   ( None, 7.5, "% of sentences over 55 words"),
    "pct_under_15":  (15.0, 32.0, "% of sentences under 15 words"),
    # punctuation habits, per 1000 words -------------------------------------------
    "em_dash":       (None,  2.5, "em-dashes per 1k words"),
    "semicolon":     (None,  4.5, "semicolons per 1k words"),
    "colon":         (None,  5.5, "colons per 1k words"),
    "paren":         ( 3.0, 14.0, "parenthetical openings per 1k words"),
    "bold":          (None,  1.0, "**bold** spans per 1k words"),
    # lexical habits, per 1000 words -----------------------------------------------
    "multi_hyphen":  (None,  1.5, "coined 3+-part hyphenated compounds per 1k words"),
    "rather_than":   (None,  0.8, '"rather than" per 1k words'),
    "therefore":     (None,  1.2, '"therefore" per 1k words'),
}


def _band(lo, hi) -> str:
    if lo is None:
        return f"<={hi}"
    if hi is None:
        return f">={lo}"
    return f"{lo}-{hi}"

# Standard multi-part hyphenations that are terminology, not coinage.
HYPHEN_ALLOW = {
    "quality-by-design", "state-of-control", "lack-of-fit", "scale-up/scale-down",
    "minute-virus-of-mice", "batch-to-batch", "one-to-one", "out-of-specification",
    "first-in-class", "end-to-end", "seed-to-production", "time-of-flight",
    "design-of-experiments", "day-to-day", "case-by-case", "step-by-step",
    "point-of-use", "real-time", "worst-case", "in-process",
}

# Phrases that do not occur in the human sources and mark the machine register.
# Each is (regex, human-readable label). Zero tolerance — these are tics, not style.
BANNED = [
    (r"\bstated first\b",                          "rhetorical meta-commentary"),
    (r"\bconclusions?, stated\b",                   "rhetorical meta-commentary"),
    (r"\banswer[- ]first\b",                        "rhetorical meta-commentary"),
    (r"\bis worth (?:stating|noting|saying)\b",     "self-congratulating aside"),
    (r"\bwarrants? (?:explicit )?comment\b",        "self-congratulating aside"),
    (r"\bthe distinction that matters\b",           "self-congratulating aside"),
    (r"\bthe quantitative form of\b",               "abstract restatement"),
    (r"\b[a-z]+-[a-z]+-[a-z]+est\b",                "coined compound superlative"),
    (r"\b(?:richest|densest)\b",                    "coined superlative"),
    (r"\bdelve\b|\btapestry\b|\bmyriad\b",          "generic LLM vocabulary"),
    (r"\bunderscore[sd]?\b",                        "generic LLM vocabulary"),
    (r"\bmeticulous(?:ly)?\b|\bseamless(?:ly)?\b",  "generic LLM vocabulary"),
    (r"\bnavigat(?:e|ing) the\b",                   "generic LLM vocabulary"),
    (r"\bthat is the (?:reason|point)\b",           "essayistic aside"),
    (r"\bis not (?:a defect|an omission)\b",        "essayistic aside"),
    (r"\bthe one thing (?:it|this|the step)\b",     "essayistic aside"),
]

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(§“\"'])")
PROTECT = [
    (r"\be\.g\.", "e<D>g<D>"), (r"\bi\.e\.", "i<D>e<D>"), (r"\bcf\.", "cf<D>"),
    (r"\bet al\.", "et al<D>"), (r"\bvs\.", "vs<D>"), (r"\betc\.", "etc<D>"),
    (r"\bNo\.", "No<D>"), (r"\bFig\.", "Fig<D>"), (r"\bapprox\.", "approx<D>"),
    (r"\bInc\.", "Inc<D>"), (r"\bLtd\.", "Ltd<D>"), (r"\bDr\.", "Dr<D>"),
    (r"(\d)\.(\d)", r"\1<D>\2"),
]


# --------------------------------------------------------------------------------------
# Prose extraction
# --------------------------------------------------------------------------------------
SKIP_HEADINGS = ("abbreviation", "approval", "reference", "appendix")


def prose_from_qmd(path: str) -> str:
    """The text a reader actually reads: no YAML, code, tables, captions or xref labels."""
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)          # YAML front matter
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)                 # comments
    text = re.sub(r"^\s*```.*?^\s*```", " ", text, flags=re.S | re.M)   # fenced chunks
    text = re.sub(r"`\{python\}[^`]*`", "NUM", text)                    # inline expressions
    text = re.sub(r"\{\{<[^>]*>\}\}", " ", text)                        # shortcodes

    kept, skipping = [], False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#"):
            skipping = any(k in s.lower() for k in SKIP_HEADINGS)
            continue
        if skipping or not s:
            continue
        if s.startswith("|") or s.startswith(":") or s.startswith("::"):
            continue                                                    # tables, captions
        s = re.sub(r"^[-*]\s+", "", s)                                  # bullet markers
        kept.append(s)
    return "\n".join(kept)


def prose_from_extract(path: str, page_lo: int, page_hi: int) -> str:
    """Running prose from a page-marked source extract, between two page markers."""
    out, page = [], 0
    for line in open(path, encoding="utf-8"):
        m = re.match(r"===== \[\w+\] PAGE (\d+) =====", line)
        if m:
            page = int(m.group(1))
            continue
        if not (page_lo <= page <= page_hi):
            continue
        s = line.strip()
        if len(s) < 30 or s.startswith(("•", "-", "|")):
            continue
        if "Licensed to" in s or "Technical Report No" in s or "© 20" in s:
            continue
        if "CMC Biotech Working Group" in s or "Case Study A-Mab" in s:
            continue
        if re.match(r"^\d+(\.\d+)*\s", s) or re.match(r"^(Page|Table|Figure)\s", s):
            continue
        if sum(c.isdigit() for c in s) > len(s) / 4:                    # table dump
            continue
        out.append(s)
    return " ".join(out)


def sentences(text: str) -> list[str]:
    t = re.sub(r"\s+", " ", text)
    t = re.sub(r"\[@[^\]]*\]", "", t)                                   # bib citations
    # Cross-references become a capitalised placeholder rather than being deleted. A
    # sentence that OPENS with "@tbl-cqa shows ..." would otherwise lose its capital and be
    # merged into the preceding sentence, inflating the measured length of both.
    t = re.sub(r"[@#]\w+[-\w]*", "Ref", t)                              # xrefs / labels
    t = re.sub(r"\*\*|\*|`", "", t)                                     # markdown emphasis
    for pat, rep in PROTECT:
        t = re.sub(pat, rep, t)
    out = []
    for s in SENT_SPLIT.split(t):
        s = s.replace("<D>", ".").strip()
        if 4 <= len(s.split()) <= 150:
            out.append(s)
    return out


# --------------------------------------------------------------------------------------
# Measurement
# --------------------------------------------------------------------------------------
def measure(text: str) -> tuple[dict, list, Counter, list]:
    sents = sentences(text)
    if not sents:
        return {}, [], Counter(), []
    lens = [len(s.split()) for s in sents]
    n, words = len(sents), sum(lens)
    scan = re.sub(r"[@#]\w+[-\w]*", "", re.sub(r"\[@[^\]]*\]", "", text))

    def per1k(pattern: str) -> float:
        return 1000.0 * len(re.findall(pattern, scan, re.I)) / words

    compounds = Counter(
        w for w in re.findall(r"\b[a-z]+(?:-[a-z]+){2,}\b", scan.lower())
        if w not in HYPHEN_ALLOW
    )
    m = {
        "mean_len": stat.mean(lens),
        "median_len": stat.median(lens),
        "pct_over_40": 100.0 * sum(1 for x in lens if x > 40) / n,
        "pct_over_55": 100.0 * sum(1 for x in lens if x > 55) / n,
        "pct_under_15": 100.0 * sum(1 for x in lens if x < 15) / n,
        "em_dash": per1k("—"),
        "semicolon": per1k(";"),
        "colon": per1k(":"),
        "paren": per1k(r"\("),
        "bold": per1k(r"\*\*"),
        "multi_hyphen": 1000.0 * sum(compounds.values()) / words,
        "rather_than": per1k(r"\brather than\b"),
        "therefore": per1k(r"\btherefore\b"),
        "_n_sent": n,
        "_n_words": words,
    }
    hits = []
    for pat, label in BANNED:
        for mt in re.finditer(pat, scan, re.I):
            lo = max(0, mt.start() - 55)
            hits.append((label, mt.group(0), scan[lo:mt.end() + 55].replace("\n", " ")))
    longest = sorted(sents, key=lambda s: -len(s.split()))[:5]
    return m, hits, compounds, longest


# A distribution needs a sample. Below this many sentences the percentages are noise, so
# only the banned-phrase check applies (this is what lets the blank-repo probe through).
MIN_SENTENCES = 40


def evaluate(m: dict) -> list[tuple[str, float, str, str]]:
    """Return the failing checks as (key, value, band, description)."""
    if m.get("_n_sent", 0) < MIN_SENTENCES:
        return []
    bad = []
    for key, (lo, hi, desc) in LIMITS.items():
        v = m.get(key)
        if v is None:
            continue
        if (hi is not None and v > hi) or (lo is not None and v < lo):
            bad.append((key, v, _band(lo, hi), desc))
    return bad


def render(name: str, m: dict, hits: list, compounds: Counter, longest: list,
           verbose: bool) -> list:
    print(f"== {name} ==")
    print(f"   {m['_n_sent']} sentences, {m['_n_words']} words of prose")
    if m["_n_sent"] < MIN_SENTENCES:
        print(f"   NOTE  under {MIN_SENTENCES} sentences: distribution thresholds are "
              f"reported but not enforced (too small a sample).")
    bad_keys = {b[0] for b in evaluate(m)}
    for key, (lo, hi, desc) in LIMITS.items():
        flag = "FAIL" if key in bad_keys else "ok  "
        note = ""
        if key in bad_keys and lo is not None and m[key] < lo:
            note = "  <- TOO LOW"
        print(f"   {flag}  {desc:<48s} {m[key]:6.1f}  ({_band(lo, hi)}){note}")
    bad = evaluate(m)
    if hits:
        print(f"\n   BANNED PHRASES ({len(hits)}):")
        for label, frag, ctx in hits[:20]:
            print(f"     [{label}] {frag!r}")
            print(f"        ...{ctx.strip()}...")
    if verbose and compounds:
        print("\n   coined compounds:",
              ", ".join(f"{w}({c})" for w, c in compounds.most_common(15)))
    if verbose and longest:
        print("\n   longest sentences:")
        for s in longest:
            print(f"     [{len(s.split())}w] {s[:190]}...")
    return bad


def check_file(path: str, verbose: bool, report_only: bool) -> int:
    m, hits, compounds, longest = measure(prose_from_qmd(path))
    if not m:
        print(f"WARN  no prose found in {path}")
        return 0
    bad = render(os.path.relpath(path, ROOT), m, hits, compounds, longest, verbose)
    if report_only:
        return 0
    if bad or hits:
        print(f"\nFAIL  {len(bad)} threshold(s) exceeded, {len(hits)} banned phrase(s).")
        print("      Fix the prose, not the gate: see authoring/WRITING_GUIDE.md §4 "
              "and authoring/REGISTER_EXEMPLAR.md.")
        return 1
    print("\nOK    register is within the human-source envelope.")
    return 0


def selftest(verbose: bool) -> int:
    """The gate must pass real human regulatory prose. If it does not, the gate is wrong."""
    sources = [
        ("PDA TR 60 (human)", os.path.join(ROOT, "refs", "text", "pda60.txt"), 18, 80),
        ("A-Mab case study (human)", os.path.join(ROOT, "refs", "text", "amab.txt"), 60, 175),
    ]
    rc = 0
    for name, path, lo, hi in sources:
        if not os.path.exists(path):
            print(f"SKIP  {name}: {os.path.relpath(path, ROOT)} missing "
                  f"(run scripts/extract_sources.py)")
            continue
        m, hits, compounds, longest = measure(prose_from_extract(path, lo, hi))
        bad = render(name, m, hits, compounds, longest, verbose)
        if bad or hits:
            print(f"\nFAIL  {name} does not pass its own gate — RELAX the threshold(s) "
                  f"above; human prose defines the envelope.\n")
            rc = 1
        else:
            print("\nOK    human source passes.\n")
    return rc


def compare(paths: list[str]) -> int:
    """Side-by-side table: the given documents against both human sources.

    This is the diagnostic that motivated the gate. It makes the register gap legible in
    one screen instead of thirteen pass/fail lines.
    """
    cols = []
    for name, path, lo, hi in [
        ("PDA TR 60", os.path.join(ROOT, "refs", "text", "pda60.txt"), 18, 80),
        ("A-Mab", os.path.join(ROOT, "refs", "text", "amab.txt"), 60, 175),
    ]:
        if os.path.exists(path):
            cols.append((name + " (human)", measure(prose_from_extract(path, lo, hi))[0]))
    for p in paths:
        cols.append((os.path.basename(p), measure(prose_from_qmd(p))[0]))
    cols = [(n, m) for n, m in cols if m]
    if not cols:
        print("nothing to compare")
        return 0

    width = max(len(n) for n, _ in cols) + 2
    print(f"{'metric':<50s}{'band':>11s}" + "".join(f"{n:>{width}s}" for n, _ in cols))
    for key, (lo, hi, desc) in LIMITS.items():
        row = f"{desc:<50s}{_band(lo, hi):>11s}"
        for _, m in cols:
            row += f"{m[key]:>{width}.1f}"
        print(row)
    print(f"{'(sentences of prose)':<50s}{'':>9s}"
          + "".join(f"{m['_n_sent']:>{width}d}" for _, m in cols))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("qmd", nargs="*")
    ap.add_argument("--selftest", action="store_true",
                    help="run the gate against the human source documents")
    ap.add_argument("--compare", action="store_true",
                    help="table of the given documents against both human sources")
    ap.add_argument("--report", action="store_true",
                    help="print metrics but always exit 0")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="also list coined compounds and the longest sentences")
    a = ap.parse_args()
    rc = 0
    if a.compare:
        return compare([q for q in a.qmd if os.path.exists(q)])
    if a.selftest:
        rc = max(rc, selftest(a.verbose))
    for q in a.qmd:
        if not os.path.exists(q):
            print(f"FAIL  no such file: {q}")
            rc = 1
            continue
        rc = max(rc, check_file(q, a.verbose, a.report))
    if not a.selftest and not a.qmd:
        ap.print_help()
    return rc


if __name__ == "__main__":
    sys.exit(main())
