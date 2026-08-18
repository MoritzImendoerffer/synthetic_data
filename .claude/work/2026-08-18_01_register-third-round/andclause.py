"""Compare three ways of counting the ', and ' two-clause sentence."""
import re, sys, os
sys.path.insert(0, "authoring")
from check_style import prose_from_qmd, prose_from_extract, sentences, HUMAN_SOURCES
import spacy
nlp = spacy.load("en_core_web_sm")

# A. round-two regex: comma + and + fixed clause-opener list (a proxy)
RX_A = re.compile(r",\s+and\s+(?:the|this|that|these|those|it|they|he|she|we|its|their|a|an|[a-z]+ing)\b", re.I)

def parser_and_clause(doc):
    """B. spaCy: a coordinating 'and' whose conjunct is a finite clause with its own subject."""
    for tok in doc:
        if tok.dep_ == "cc" and tok.lower_ == "and":
            head = tok.head
            # the conjunct that 'and' introduces is a sibling of `head` with dep conj
            for conj in head.children:
                if conj.dep_ == "conj" and conj.i > tok.i:
                    has_subj = any(c.dep_ in ("nsubj", "nsubjpass", "expl") for c in conj.children)
                    verbal   = conj.pos_ in ("VERB", "AUX")
                    if has_subj and verbal:
                        # comma before the 'and' is what the owner's shape has
                        prev = doc[tok.i - 1] if tok.i > 0 else None
                        yield (prev is not None and prev.text == ",")
    return

def count(label, text):
    S = sentences(text)
    n = len(S)
    a = sum(1 for s in S if RX_A.search(s))
    b_comma = b_any = 0
    for s in S:
        hits = list(parser_and_clause(nlp(s.replace("NUM", "12.3"))))
        if hits:
            b_any += 1
            if any(hits): b_comma += 1
    print(f"{label:22s} n={n:4d}   regex {100*a/n:5.1f}% ({a:3d})   "
          f"parser ', and'+clause {100*b_comma/n:5.1f}% ({b_comma:3d})   parser any 'and'+clause {100*b_any/n:5.1f}% ({b_any:3d})")

for name, fn, lo, hi in HUMAN_SOURCES:
    count(name, prose_from_extract(os.path.join("refs/text", fn), lo, hi))
print()
R0=".claude/work/2026-08-16_01_register-from-four-sources/pre-rewrite"
R1=".claude/work/2026-08-17_01_register-second-round/pre-rewrite"
for lab, p in (("PCR-003 round zero", f"{R0}/PCR-003_bioreactor.qmd"),
               ("PCR-003 round one",  f"{R1}/PCR-003_bioreactor.qmd"),
               ("PCR-003 round two",  "pc_package/PCR-003_bioreactor.qmd"),
               ("PCP-003 round two",  "pc_package/PCP-003_bioreactor.qmd")):
    count(lab, prose_from_qmd(p))
