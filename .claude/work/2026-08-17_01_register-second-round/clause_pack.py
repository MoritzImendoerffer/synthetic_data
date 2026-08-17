"""Quick diagnostic: how many argument steps does a sentence carry?

Counts, per document, the share of sentences that join two or more clauses with
comma+coordinator (", so ", ", and ", ", but ", ", since ", ", because ", ", which ") and
the share with three or more, plus mid-sentence ", so " and sentence-initial connectives.
Corpus documents vs the four human sources, same prose extraction as the gate.
"""
import re, sys, os
sys.path.insert(0, "authoring")
from check_style import (prose_from_qmd, prose_from_extract, sentences, HUMAN_SOURCES)

CLAUSE = re.compile(r",\s+(so|and|but|since|because|which|while|whereas|yet)\s+", re.I)
SO_MID = re.compile(r",\s+so\s+", re.I)
INITIAL = re.compile(r"^(However|Therefore|Consequently|As a result|In addition|For this reason|"
                     r"By contrast|In contrast|For example|Thus|Hence|Nevertheless|Nonetheless|"
                     r"Moreover|Furthermore|Instead|Rather|First|Second|Third|Finally|Overall)\b,?", re.I)
NUM_REF = re.compile(r"\bthe (two|three|four|five|six|seven|eight|nine|ten) that\b", re.I)
SO_AND = re.compile(r",\s+so\s+.*,\s+and\s+", re.I)

def stats(name, text):
    S = sentences(text)
    n = len(S)
    k = [len(CLAUSE.findall(s)) for s in S]
    ge2 = sum(1 for x in k if x >= 2)
    ge3 = sum(1 for x in k if x >= 3)
    so = sum(1 for s in S if SO_MID.search(s))
    soand = sum(1 for s in S if SO_AND.search(s))
    ini = sum(1 for s in S if INITIAL.match(s))
    numref = sum(1 for s in S if NUM_REF.search(s))
    print(f"{name:22s} n={n:5d}  >=2coord {100*ge2/n:5.1f}%  >=3coord {100*ge3/n:4.1f}%  "
          f"', so ' {100*so/n:4.1f}%  ', so … , and ' {100*soand/n:4.1f}%  "
          f"initial-connective {100*ini/n:4.1f}%  'the N that' {numref}")

for name, fn, lo, hi in HUMAN_SOURCES:
    stats(name, prose_from_extract(os.path.join("refs/text", fn), lo, hi))
print()
W = ".claude/work/2026-08-16_01_register-from-four-sources/pre-rewrite"
for label, p in (("PCR-003 before", f"{W}/PCR-003_bioreactor.qmd"),
                 ("PCR-003 after", "pc_package/PCR-003_bioreactor.qmd"),
                 ("PCP-003 before", f"{W}/PCP-003_bioreactor.qmd"),
                 ("PCP-003 after", "pc_package/PCP-003_bioreactor.qmd"),
                 ("PCR-008 (untouched)", "pc_package/PCR-008_aex.qmd"),
                 ("PCR-005 (untouched)", "pc_package/PCR-005_protein_a.qmd")):
    stats(label, prose_from_qmd(p))

# print the ", so … , and" sentences from PCR-003 after
print()
for s in sentences(prose_from_qmd("pc_package/PCR-003_bioreactor.qmd")):
    if SO_AND.search(s):
        print("-", s)
