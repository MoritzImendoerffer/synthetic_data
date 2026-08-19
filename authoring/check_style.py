#!/usr/bin/env python3
"""Register gate — is the prose plain technical English, or is it AI-flavoured?

    uv run python authoring/check_style.py pc_package/PCR-003_bioreactor.qmd
    uv run python authoring/check_style.py --selftest        # the human sources must pass
    uv run python authoring/check_style.py <qmd> --report    # numbers only, never fails
    uv run python authoring/check_style.py <qmd> --review    # the REVIEWER's table (advisory rows)
    uv run python authoring/check_style.py <qmd>... --compare  # table vs the human sources

Why this exists
---------------
The corpus's first-pass reports were written to a guide whose voice exemplar had been
distilled from an earlier AI-written report, so the register drifted into a recognisable
machine idiom: 34-word average sentences, an em-dash aside in every third sentence, a
semicolon splice in every fourth, coined compound superlatives, and a "what this means"
coda welded onto every paragraph.

The thresholds below are not taste. They are read off the four published human documents
the corpus is built on:

    refs/text/pda60.txt    PDA Technical Report No. 60, Process Validation (2013)
    refs/text/amab.txt     A-Mab: A Case Study in Bioprocess Development (2009)
    refs/text/ispe_tt.txt  ISPE Good Practice Guide: Technology Transfer (2023)
    refs/text/ispe_pv.txt  ISPE GPG: Practical Implementation of the Lifecycle Approach (2023)

``--selftest`` runs the gate against all four. **Any threshold this file asserts must be one
that real human regulatory prose passes** — if a rule fails the self-test, the rule is wrong,
not the source. Tighten a threshold only after re-running the self-test.

The two ISPE guides were added on 2026-08-16 and they write longer sentences than the first
two, so several ceilings moved up. Read the numbers per source in the self-test output rather
than the band: the band is now the union of four house styles, and writing at its edge is not
the same as writing like any of them.

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
# The human sources the envelope is read off
# --------------------------------------------------------------------------------------
# Four, not two. Ten of the twenty corpus documents are plans and neither original source is
# a plan, which is why the two ISPE guides were extracted.
#
# The page ranges are the running-prose chapters, taken from each guide's own contents page
# rather than estimated. Front matter is title pages and acknowledgement lists; the
# appendices are case studies and statistical tables, and reading into them measures table
# cells as though they were sentences. Appendix 1 begins on extract page 97 of ISPE TT and
# page 113 of ISPE PV, so the body ends just before each.
HUMAN_SOURCES = [
    ("PDA TR 60",        "pda60.txt",   18,  80),
    ("A-Mab case study", "amab.txt",    60, 175),
    ("ISPE TT",          "ispe_tt.txt", 30,  96),
    ("ISPE PV",          "ispe_pv.txt", 30, 112),
]

# --------------------------------------------------------------------------------------
# Thresholds. Every one of these is satisfied by all four human sources (see --selftest).
# --------------------------------------------------------------------------------------
# Each entry is (lo, hi, description); None means unbounded on that side.
#
# TWO SETS SINCE 2026-08-19, and the difference is who reads them.
#
# GATED is what fails a build: the punctuation and lexical tics that sit at or near zero in all
# four human sources and mark the machine register from across the room — the em-dash aside,
# the semicolon splice, the colon, bold inside a sentence, the coined three-part compound —
# plus the BANNED phrase list below. An author sees pass/fail on these and nothing else.
#
# ADVISORY is the sentence-length distribution, the parenthesis rate and "rather than". They
# are printed under --review for a REVIEWER and never shown to an author, and they fail
# nothing. The reason is measured, not argued: on 2026-08-19 the project owner read the same
# two subsections of PCR-005 written under two regimes, blind, and preferred "clearly" the one
# that FAILED this gate as it then stood — % over 40 words at 1.1 against a floor of 3.0 and
# "rather than" at 1.6 per 1k against a ceiling of 0.8, with mean length, median length and
# % under 15 all within a tenth of their edge — over the shipped text that passed every row.
# A band that a good paragraph fails is a broken band, and a band printed back to the author
# is a target: three rounds moved these numbers and the reader did not read them
# (docs/results/2026-08-19-apparatus-probe.md §3). The edges have NOT been moved; the rows
# stopped being gated. `paren` had a floor of 3.0 and moves with the length rows because a
# floor on parentheses is a floor on a habit, not a tic.
#
# The values are unchanged from 2026-08-16, when five ceilings moved up as the two ISPE guides
# joined the self-test. Each is set to clear the widest source (ISPE PV on four of the five:
# 30.2 mean, 26.0 median, 20.8 % over 40 words, 9.0 % over 55; ISPE TT sets the parenthesis
# ceiling at 14.2). Several bands are TWO-SIDED on purpose: capping length alone pushed an
# author into staccato prose once, and human prose sits in a band. That is still true, and it
# is now the reviewer's band to read.
GATED = {
    # punctuation habits, per 1000 words -------------------------------------------
    "em_dash":       (None,  2.5, "em-dashes per 1k words"),
    "semicolon":     (None,  4.5, "semicolons per 1k words"),
    "colon":         (None,  5.5, "colons per 1k words"),
    "bold":          (None,  1.0, "**bold** spans per 1k words"),
    # lexical habits, per 1000 words -----------------------------------------------
    "multi_hyphen":  (None,  1.5, "coined 3+-part hyphenated compounds per 1k words"),
}
ADVISORY = {
    # sentence-length distribution ------------------------------------------------
    "mean_len":      (20.0, 30.5, "mean sentence length (words)"),
    "median_len":    (18.0, 26.5, "median sentence length (words)"),
    "pct_over_40":   ( 3.0, 21.5, "% of sentences over 40 words"),
    "pct_over_55":   ( None, 9.5, "% of sentences over 55 words"),
    "pct_under_15":  (15.0, 32.0, "% of sentences under 15 words"),
    "paren":         ( 3.0, 14.5, "parenthetical openings per 1k words"),
    "rather_than":   (None,  0.8, '"rather than" per 1k words'),
}
# The union, IN THE ORDER THE TABLES HAVE ALWAYS PRINTED. `--compare`, the committed baseline
# tables in .claude/work/*/measure_baseline_style.txt and the measurement scripts that
# reproduce them iterate LIMITS and depend on this row order. Do not reorder it.
LIMITS = {k: (ADVISORY | GATED)[k] for k in (
    "mean_len", "median_len", "pct_over_40", "pct_over_55", "pct_under_15",
    "em_dash", "semicolon", "colon", "paren", "bold", "multi_hyphen", "rather_than")}

# The connectives WRITING_GUIDE 4b recommends. Counted and printed on every run, and gated by
# nothing.
#
# There used to be a `"therefore": (None, 1.2)` entry in LIMITS. Measured across the corpus on
# 2026-08-16, "therefore" was the ONLY connective still in service — "However", "For example",
# "By contrast", "In addition", "Consequently" and "Note that" came to zero in all twenty
# documents, against 46 and 12 for the first two in A-Mab alone. So the one rule the gate had
# about connectives pushed down on the last one left, and removing it is the whole of the fix.
#
# It is not replaced by a rate over the other eight. A floor on a connective is met by typing
# the word, not by writing the sentence that needs it, and a produced connective is a worse
# tell than an absent one. This stays a diagnosis for a human to read.
CONNECTIVES = ("however", "therefore", "in addition", "for this reason", "since",
               "once", "as a result", "by contrast", "consequently")

# Clause packing. The corpus reasons INSIDE the sentence — a premise, a consequence and a
# recommendation joined by ", so … , and …" — where the four sources end the sentence and open
# the next one with a connective. Measured 2026-08-17 over the same prose this gate reads:
# mid-sentence ", so " in 6-11 % of corpus sentences against 0.1-0.4 % in all four sources;
# sentence-initial connectives in 0-2 % against 3.7-6.1 %. Printed, gated by nothing: a
# ceiling on ", so " is met by writing ", and" or ";", so the whole family is printed together.
CLAUSE_COORD = re.compile(r",\s+(?:so|and|but|since|because|which|while|whereas|yet)\s+", re.I)
SO_MID = re.compile(r",\s+so\s+", re.I)
INITIAL_CONNECTIVE = re.compile(
    r"^(?:However|Therefore|Consequently|As a result|In addition|For this reason|By contrast|"
    r"In contrast|For example|Thus|Hence|Nevertheless|Nonetheless|Moreover|Furthermore|"
    r"Instead|Rather|First|Second|Third|Finally|Overall)\b,?", re.I)

# Two more advisory counts, added 2026-08-18 after the project owner read the round-two PCR-003
# and named the balanced two-clause sentence — "…forms the … attributes of A-Mab, and this
# report bounds the culture conditions that set them" — as the thing that gave it away. Counted
# afterwards: 18-23 % of corpus sentences against 1.1-3.4 % in the four sources, and the round
# that drove ", so " to zero did not move it, because nothing printed it back.
#
# AND_CLAUSE is a FLOOR. It matches ", and" followed by a fixed list of clause openers, so it
# misses a second clause opening on a bare noun ("…, and osmolality was not"; "…, and both were
# retained"). Measured 2026-08-18 it undercounts the corpus by 2-6 points and matches the four
# sources within 0.5. The parser count in check_discourse.py is the other half; neither is a
# superset of the other, and both are printed. Gated by nothing.
AND_CLAUSE = re.compile(
    r",\s+and\s+(?:the|this|that|these|those|it|they|he|she|we|its|their|a|an|[a-z]+ing)\b", re.I)
NOT_TAIL = re.compile(r",\s+not\s+", re.I)


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

# Per-page furniture in the source extracts. Left in, it is measured as prose: the two ISPE
# guides stamp a four-line DRM footer on every page, which alone put 300 of ISPE TT's 470
# short sentences into the count and pushed "under 15 words" to 41 % against a human band of
# 15-32 %. These strings cannot occur inside a real sentence, so a substring test is safe.
EXTRACT_BOILER = (
    "Licensed to", "Technical Report No", "© 20",                  # PDA TR 60
    "CMC Biotech Working Group", "Case Study A-Mab",               # A-Mab
    "Downloaded from", "For personal use only",                    # ISPE, both guides
    "No other uses without permission", "For individual use only",
    "Copyright ISPE", "guidance-docs.ispe.org",
)

# Running headers, which DO occur inside real sentences ("... the ISPE Good Practice Guide:
# Technology Transfer [41] provides ..."), so they are matched as a whole line only.
EXTRACT_HEADERS = frozenset({
    "Practical Implementation of the Lifecycle Approach to Process Validation",
    "Technology Transfer",
    "ISPE Good Practice Guide:",
})


def prose_from_qmd(path: str) -> str:
    """The text a reader actually reads: no YAML, code, tables, captions or xref labels."""
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)          # YAML front matter
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)                 # comments
    text = re.sub(r"^\s*```.*?^\s*```", " ", text, flags=re.S | re.M)   # fenced chunks
    text = re.sub(r"`\{python\}[^`]*`", "NUM", text)                    # inline expressions
    text = re.sub(r"\{\{<[^>]*>\}\}", " ", text)                        # shortcodes
    # Markdown images are a caption plus a path, not prose. Left in, the caption fuses
    # with the preceding sentence (its "!" is not a sentence boundary) and inflates the
    # measured length of both, which is a measurement artifact rather than a style fault.
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)(\{[^}]*\})?", " ", text)

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
        if s in EXTRACT_HEADERS:
            continue
        if len(s) < 30 or s.startswith(("•", "-", "|")):
            continue
        if any(b in s for b in EXTRACT_BOILER):
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
    n_so = sum(1 for s in sents if SO_MID.search(s))
    n_init = sum(1 for s in sents if INITIAL_CONNECTIVE.match(s))
    n_coord = sum(1 for s in sents if len(CLAUSE_COORD.findall(s)) >= 2)
    n_and   = sum(1 for s in sents if AND_CLAUSE.search(s))
    n_not   = sum(1 for s in sents if NOT_TAIL.search(s))
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
        "_n_sent": n,
        "_n_words": words,
        "_connectives": Counter(
            {c: len(re.findall(rf"\b{c}\b", scan, re.I)) for c in CONNECTIVES}
        ),
        "_pct_so_mid":       100.0 * n_so / n,
        "_pct_initial_conn": 100.0 * n_init / n,
        "_pct_coord2":       100.0 * n_coord / n,
        "_pct_and_clause":   100.0 * n_and / n,
        "_pct_not_tail":     100.0 * n_not / n,
        "_n_so_mid": n_so, "_n_initial_conn": n_init, "_n_coord2": n_coord,
        "_n_and_clause": n_and, "_n_not_tail": n_not,
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


def evaluate(m: dict, limits: dict | None = None) -> list[tuple[str, float, str, str]]:
    """Return the failing checks as (key, value, band, description).

    A document is judged on GATED only. The self-test passes LIMITS, the union, because a
    band that real human prose fails is wrong whether it gates or advises.
    """
    if m.get("_n_sent", 0) < MIN_SENTENCES:
        return []
    bad = []
    for key, (lo, hi, desc) in (limits or GATED).items():
        v = m.get(key)
        if v is None:
            continue
        if (hi is not None and v > hi) or (lo is not None and v < lo):
            bad.append((key, v, _band(lo, hi), desc))
    return bad


def connective_line(m: dict) -> str:
    """The connective repertoire, as one advisory line. Nothing here can fail a document.

    Printed because the absence is invisible otherwise: a document using "therefore" nine
    times and nothing else reads as monotonous long before a reader can say why.
    """
    used = {c: n for c, n in m["_connectives"].items() if n}
    rate = 1000.0 * sum(used.values()) / m["_n_words"]
    detail = ", ".join(f"{c} {n}" for c, n in m["_connectives"].most_common() if n) or "none"
    return (f"{'connectives (diagnostic, never gated)':<48s} {rate:6.1f}  "
            f"per 1k words, {len(used)}/{len(CONNECTIVES)} distinct: {detail}")


def packing_line(m: dict) -> str:
    """Clause packing, as one advisory line. Nothing here can fail a document."""
    return (f"{'clause packing (diagnostic, never gated)':<48s} "
            f"', so ' mid-sentence {m['_pct_so_mid']:4.1f} % of sentences "
            f"({m['_n_so_mid']}/{m['_n_sent']}), "
            f"opens with a connective {m['_pct_initial_conn']:4.1f} % "
            f"({m['_n_initial_conn']}/{m['_n_sent']}), "
            f"2+ clause coordinators {m['_pct_coord2']:4.1f} %, "
            f"', and '+clause {m['_pct_and_clause']:4.1f} % "
            f"({m['_n_and_clause']}/{m['_n_sent']}), "
            f"', not ' {m['_pct_not_tail']:4.1f} % "
            f"({m['_n_not_tail']}/{m['_n_sent']})  "
            f"[sources: 0.1-0.4 / 3.7-6.1 / 1.2-3.1 / 1.1-3.4 / 0.0-0.2]")


def render(name: str, m: dict, hits: list, compounds: Counter, longest: list,
           verbose: bool, review: bool = False) -> list:
    """Print one document's result.

    Default (the author's view): the sentence and word count, the GATED rows, the banned
    phrases. Under ``review`` (the reviewer's view): the ADVISORY rows with their bands as
    well, the connective and clause-packing lines, and with ``verbose`` the coined compounds
    and the longest sentences. The split is deliberate — see the comment above GATED.
    """
    print(f"== {name} ==")
    print(f"   {m['_n_sent']} sentences, {m['_n_words']} words of prose")
    if m["_n_sent"] < MIN_SENTENCES:
        print(f"   NOTE  under {MIN_SENTENCES} sentences: thresholds are reported but not "
              f"enforced (too small a sample).")
    bad_keys = {b[0] for b in evaluate(m)}
    for key, (lo, hi, desc) in GATED.items():
        flag = "FAIL" if key in bad_keys else "ok  "
        print(f"   {flag}  {desc:<48s} {m[key]:6.1f}  ({_band(lo, hi)})  [gated]")
    if review:
        for key, (lo, hi, desc) in ADVISORY.items():
            out = (hi is not None and m[key] > hi) or (lo is not None and m[key] < lo)
            note = "  <- outside the source band" if out else ""
            print(f"   --    {desc:<48s} {m[key]:6.1f}  ({_band(lo, hi)})  [advisory]{note}")
        print(f"   --    {connective_line(m)}")
        print(f"   --    {packing_line(m)}")
    bad = evaluate(m)
    if hits:
        print(f"\n   BANNED PHRASES ({len(hits)}):")
        for label, frag, ctx in hits[:20]:
            print(f"     [{label}] {frag!r}")
            print(f"        ...{ctx.strip()}...")
    if review and verbose and compounds:
        print("\n   coined compounds:",
              ", ".join(f"{w}({c})" for w, c in compounds.most_common(15)))
    if review and verbose and longest:
        print("\n   longest sentences:")
        for s in longest:
            print(f"     [{len(s.split())}w] {s[:190]}...")
    return bad


def check_file(path: str, verbose: bool, report_only: bool, review: bool = False) -> int:
    m, hits, compounds, longest = measure(prose_from_qmd(path))
    if not m:
        print(f"WARN  no prose found in {path}")
        return 0
    bad = render(os.path.relpath(path, ROOT), m, hits, compounds, longest, verbose, review)
    if report_only:
        return 0
    if bad or hits:
        print(f"\nFAIL  {len(bad)} gated threshold(s) exceeded, {len(hits)} banned phrase(s).")
        print("      Fix the prose, not the gate: see authoring/WRITING_GUIDE.md §4.")
        return 1
    print("\nOK    no gated tic and no banned phrase.")
    return 0


def selftest(verbose: bool, review: bool = True) -> int:
    """The gate must pass real human regulatory prose. If it does not, the gate is wrong.

    A source that is not on disk is a FAILURE, not a skip. The extracts are committed, so a
    missing one means the tree is broken — and the old behaviour was to print SKIP and exit 0,
    which meant a run that measured nothing at all reported the same success as a run that
    measured everything.
    """
    rc, measured, missing = 0, [], []
    for name, fname, lo, hi in HUMAN_SOURCES:
        path = os.path.join(ROOT, "refs", "text", fname)
        if not os.path.exists(path):
            print(f"MISS  {name} (human): {os.path.relpath(path, ROOT)} missing "
                  f"(run scripts/extract_sources.py)\n")
            missing.append(name)
            continue
        m, hits, compounds, longest = measure(prose_from_extract(path, lo, hi))
        render(f"{name} (human), extract pp. {lo}-{hi}",
               m, hits, compounds, longest, verbose, review)
        bad = evaluate(m, LIMITS)     # the union: an advisory band a source fails is wrong too
        if bad or hits:
            print(f"\nFAIL  {name} does not pass its own gate — RELAX the threshold(s) "
                  f"above; human prose defines the envelope.\n")
            rc = 1
        else:
            print("\nOK    human source passes.\n")
            measured.append(name)

    print(f"self-test: {len(measured)} of {len(HUMAN_SOURCES)} human sources measured and "
          f"passing ({', '.join(measured) or 'none'})")
    if missing:
        print(f"FAIL  {len(missing)} source(s) not on disk: {', '.join(missing)}. "
              f"The envelope is only as wide as what was measured.")
        rc = 1
    return rc


def compare(paths: list[str]) -> int:
    """Side-by-side table: the given documents against all four human sources.

    This is the diagnostic that motivated the gate. It makes the register gap legible in
    one screen instead of twelve pass/fail lines.
    """
    cols = []
    for name, fname, lo, hi in HUMAN_SOURCES:
        path = os.path.join(ROOT, "refs", "text", fname)
        if os.path.exists(path):
            cols.append((name + " (human)", measure(prose_from_extract(path, lo, hi))[0]))
    for p in paths:
        cols.append((os.path.basename(p), measure(prose_from_qmd(p))[0]))
    cols = [(n, m) for n, m in cols if m]
    if not cols:
        print("nothing to compare")
        return 0

    width = max(len(n) for n, _ in cols) + 2
    print(f"{'metric':<62s}{'band':>11s}" + "".join(f"{n:>{width}s}" for n, _ in cols))
    for key, (lo, hi, desc) in LIMITS.items():
        row = f"{desc:<62s}{_band(lo, hi):>11s}"
        for _, m in cols:
            row += f"{m[key]:>{width}.1f}"
        print(row + ("   [gated]" if key in GATED else "   [advisory]"))
    print(f"{'connectives per 1k words (not gated)':<62s}{'':>11s}"
          + "".join(f"{1000.0 * sum(m['_connectives'].values()) / m['_n_words']:>{width}.1f}"
                   for _, m in cols))
    print(f"{'  of the nine, how many are used at all':<62s}{'':>11s}"
          + "".join(f"{sum(1 for n in m['_connectives'].values() if n):>{width}d}"
                   for _, m in cols))
    for key, label in (("_pct_so_mid",       "% sentences with mid-sentence ', so ' (not gated)"),
                       ("_pct_initial_conn", "% sentences opening with a connective (not gated)"),
                       ("_pct_coord2",       "% sentences with 2+ clause coordinators (not gated)"),
                       ("_pct_and_clause",   "% sentences with ', and ' + a second clause (floor; not gated)"),
                       ("_pct_not_tail",     "% sentences with mid-sentence ', not ' (not gated)")):
        print(f"{label:<62s}{'':>11s}" + "".join(f"{m[key]:>{width}.1f}" for _, m in cols))
    print(f"{'(sentences of prose)':<62s}{'':>11s}"
          + "".join(f"{m['_n_sent']:>{width}d}" for _, m in cols))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("qmd", nargs="*")
    ap.add_argument("--selftest", action="store_true",
                    help="run the gate against the human source documents")
    ap.add_argument("--compare", action="store_true",
                    help="table of the given documents against all four human sources")
    ap.add_argument("--report", action="store_true",
                    help="print metrics but always exit 0")
    ap.add_argument("--review", action="store_true",
                    help="the reviewer's view: the advisory rows, bands, connectives and clause "
                         "packing as well as the gated tics (never shown to an author)")
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
        rc = max(rc, check_file(q, a.verbose, a.report, a.review))
    if not a.selftest and not a.qmd:
        ap.print_help()
    return rc


if __name__ == "__main__":
    sys.exit(main())
