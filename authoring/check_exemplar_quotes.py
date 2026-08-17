#!/usr/bin/env python3
"""Verify every blockquote in REGISTER_EXEMPLAR.md is verbatim from its cited source.

    uv run python authoring/check_exemplar_quotes.py

The register exemplar's whole value is that its passages are real human regulatory prose.
If a quote is paraphrased, the corpus is being taught a voice that nobody actually writes in
— which is precisely the failure mode the exemplar was rebuilt to fix. This script re-checks
every blockquote against the four source extracts in ``refs/text/`` and reports the extract
page each one was found on. Run it after editing the exemplar.

The source is chosen by the name in the attribution line, so an attribution must carry
exactly one of the names in ``SRC`` below: "A-Mab", "PDA TR 60", "ISPE Technology Transfer",
"ISPE Practical Implementation". A quote naming none or several is skipped, as a passage
that two sources share cannot be attributed to one of them.

Matching tolerates PDF-extraction artifacts only, never word changes: collapsed whitespace,
line-break hyphenation, the Symbol-font private-use glyphs (U+F0B0 degree, U+F0B7 bullet),
A-Mab's U+2015/U+2016 quote marks, and running headers/footers.

Exit 0 iff every quote is verbatim.
"""
import re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = {
    'PDA TR 60':                    ROOT / 'refs/text/pda60.txt',
    'A-Mab':                        ROOT / 'refs/text/amab.txt',
    'ISPE Technology Transfer':     ROOT / 'refs/text/ispe_tt.txt',
    'ISPE Practical Implementation': ROOT / 'refs/text/ispe_pv.txt',
}


BOILER = [
    r'Licensed to [^\n]*Prohibited\.',
    r'Technical Report No\. 60',
    r'© 20\d\d Parenteral Drug Association, Inc\.',
    r'Product Development and Realisation Case Study A-Mab',
    r'CMC Biotech Working Group',
    r'The CMC Biotech Working Group',
    # The ISPE guides stamp a four-line DRM footer on every page. A quote that spans a
    # page break has the whole block sitting inside it.
    r'Downloaded from https://guidance-docs\.ispe\.org/[^\n]*',
    r'For personal use only\. No other uses without permission\.',
    r'Copyright © 20\d\d International Society for Pharmaceutical Engineering\. All rights reserved\.',
    r'For individual use only\. © Copyright ISPE 20\d\d\. All rights reserved\.',
    # Running headers. Anchored to a whole line, because both phrases also occur inside
    # real sentences and stripping them there would let a paraphrase through.
    r'^\s*ISPE Good Practice Guide:\s*$',
    r'^\s*Technology Transfer\s*$',
    r'^\s*Practical Implementation of the Lifecycle Approach to Process Validation\s*$',
    r'Page \d+ of \d+',
    r'===== \[\w+\] PAGE \d+ =====',
    r'^\s*\d{1,3}\s*$',
]


def norm(t: str) -> str:
    for b in BOILER:
        t = re.sub(b, ' ', t, flags=re.M)
    t = unicodedata.normalize('NFKD', t)
    t = t.replace('’', "'").replace('‘', "'")
    t = t.replace('\u201c', '"').replace('\u201d', '"')
    # A-Mab's PDF layer renders curly quotes as U+2015 / U+2016
    t = t.replace('\u2015', '"').replace('\u2016', '"')
    t = t.replace('\uf0b0', '°').replace('\uf0b7', ' ').replace('\uf0a7', ' ')
    t = re.sub(r'\s*°\s*', '°', t)
    t = re.sub(r'-\n\s*', '', t)             # "mul-\ntiple" -> "multiple"
    t = re.sub(r'(\w)-[ \t]+(\w)', r'\1-\2', t)  # "scaled- down" -> "scaled-down"
    t = t.replace('\u2013', '-').replace('\u2014', '-')
    t = re.sub(r'\s+', ' ', t)
    return t.lower().strip()


def pages(path):
    """[(page_no, normalized_text)] plus a whole-doc normalized blob."""
    raw = path.read_text()
    out, cur, page = [], [], 0
    for line in raw.split('\n'):
        m = re.match(r'===== \[\w+\] PAGE (\d+) =====', line)
        if m:
            if cur:
                out.append((page, '\n'.join(cur)))
            page, cur = int(m.group(1)), []
        else:
            cur.append(line)
    if cur:
        out.append((page, '\n'.join(cur)))
    return out


CACHE = {}
for name, p in SRC.items():
    pg = pages(p)
    # normalized full text, plus a page index built on a rolling join so that quotes
    # spanning a page break still match
    joined = norm('\n'.join(t for _, t in pg))
    CACHE[name] = (pg, joined, [(n, norm(t)) for n, t in pg])

md = (ROOT / 'authoring/REGISTER_EXEMPLAR.md').read_text()

# blockquote blocks followed by an attribution line "> — SOURCE, p. N"
blocks = re.findall(r'((?:^>.*\n)+)', md, flags=re.M)
checked = failed = 0
for b in blocks:
    lines = [l[1:].strip() for l in b.strip().split('\n')]
    attrib = [l for l in lines if l.startswith('—')]
    if not attrib:
        continue
    body = ' '.join(l for l in lines if not l.startswith('—') and l)
    if len(body) < 55:
        continue
    named = [name for name in SRC if name in attrib[-1]]
    if len(named) != 1:
        continue                      # unattributed, or shared between two sources
    src = named[0]
    claimed = attrib[-1]
    checked += 1
    q = norm(body)
    _, joined, pagelist = CACHE[src]
    nohy = lambda x: x.replace('-', '')
    if q in joined or nohy(q) in nohy(joined):
        hits = [n for n, t in pagelist if q[:120] in t]
        loc = f"p. {hits[0]}" if hits else "spans a page break"
        ok = 'ok  '
        note = f"found on {loc}"
    else:
        ok = 'FAIL'
        failed += 1
        # find the longest matching prefix to localise the divergence
        lo, hi = 0, len(q)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if q[:mid] in joined:
                lo = mid
            else:
                hi = mid - 1
        note = f"diverges at char {lo}: ...{q[max(0,lo-60):lo+80]}..."
    print(f"{ok}  [{claimed}] {note}")
    if ok == 'FAIL':
        print(f"      quote starts: {body[:90]}...")

print(f"\n{checked} quotes checked, {failed} failed")
sys.exit(1 if failed else 0)
