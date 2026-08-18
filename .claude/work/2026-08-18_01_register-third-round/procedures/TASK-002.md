# TASK-002 procedure — passive rate and the parser's and-clause count in `check_discourse.py`

Read `state.json` → `TASK-002` first, then `exploration.md` §6b, then this unit's `andclause.py`.
Everything here needs the extra: `uv run --extra discourse python …`.

## 0. Before

```bash
uv run --extra discourse python -c "import spacy; spacy.load('en_core_web_sm'); print('ok')"
uv run --extra discourse python .claude/work/2026-08-18_01_register-third-round/andclause.py 2>/dev/null
uv run --extra discourse python authoring/check_discourse.py --cap pc_package/PCR-003_bioreactor.qmd | tail -5
```

Keep `andclause.py`'s output open: its `parser ', and'+clause` column is what you reproduce.

## 1. The two counts, inside `copula_front()` (line ~76) — ONE loop, ONE denominator

Rename to `copula_front_passive_and(nlp, sents, cap=None)` (or keep the name and widen the return;
`measure()` is the only caller). Inside the existing per-sentence loop, after `root`/`subj` are
found and `n += 1`:

```python
        # passive: any token carrying a passive dependency. Round two's measure_owner_reading.txt
        # counted it this way; keep it identical so the series stays comparable.
        passive += int(any(t.dep_ in ("nsubjpass", "auxpass") for t in doc))
        # ', and' + a second finite clause with its own subject: the parser's half of the count.
        # (The regex half is in check_style.AND_CLAUSE.) Ported from andclause.parser_and_clause.
        andc += int(_and_clause(doc))
```

with, at module level:

```python
def _and_clause(doc) -> bool:
    """A coordinating 'and', preceded by a comma, whose conjunct is a finite clause with its own
    subject. Misses long coordinated noun phrases the small model mis-attaches (two of the three
    sentences the owner quoted on 2026-08-18); check_style.AND_CLAUSE covers those. Neither is a
    superset of the other, so both are printed."""
    for tok in doc:
        if tok.dep_ == "cc" and tok.lower_ == "and" and tok.i > 0 and doc[tok.i - 1].text == ",":
            for conj in tok.head.children:
                if (conj.dep_ == "conj" and conj.i > tok.i and conj.pos_ in ("VERB", "AUX")
                        and any(c.dep_ in ("nsubj", "nsubjpass", "expl") for c in conj.children)):
                    return True
    return False
```

Return `cop, front, passive, andc, n`. In `measure()` add:

```python
            "passive_pct": pct(passive, n), "passive": [passive, n],
            "and_clause_pct": pct(andc, n), "and_clause": [andc, n],
```

## 2. Two rows in the text table (line ~138), after front field

```python
                            ("passive_pct", "passive", "passive construction % (passive/n) — a BAND, sources 54-60"),
                            ("and_clause_pct", "and_clause", "', and '+clause, parser % (and/n)")):
```

Widen `width` if the label overflows. The docstring gains two lines describing the two measures
and stating **band, never floor** for the passive.

## 3. Reproduce

```bash
uv run --extra discourse python authoring/check_discourse.py --cap \
    pc_package/PCR-003_bioreactor.qmd pc_package/PCP-003_bioreactor.qmd 2>/dev/null
```

Expected parser and-clause row (from `andclause.py`, ±0.5 on the source columns because the cap
bites there; exact on the corpus columns because both documents are under 450 sentences):

| | PDA | A-Mab | ISPE TT | ISPE PV | PCR-003 | PCP-003 |
|---|---|---|---|---|---|---|
| `, and`+clause parser | 3.2 (26/…) | 1.2 (13/…) | 0.9 (6/…) | 2.8 (23/…) | **24.9 (105/…)** | **24.6 (50/…)** |
| passive | (capped) | (capped) | (capped) | (capped) | **35.4 (146/413)** | (measure it) |

**The passive figure will NOT equal round two's 34.4 % (145/421), and that is expected.** Measured
2026-08-18 by `/plan` on the committed PCR-003: 146 passive sentences (round two's heredoc ran on
the DRAFT before promotion; one sentence changed) over **413** on the copula loop's denominator
(sentences with a root and a subject) = **35.4 %**, against 146/421 = 34.7 % over all sentences.
The denominators differ by the eight sentences with no root/subject. Do not "fix" it with a second
loop — one denominator for copula, front, passive and and-clause is the point. TASK-006's page
reports the `check_discourse` figure and footnotes the round-two heredoc figure with this reason.

Also run **without** `--cap` once and record the source passive columns; they should be close to
54.3 / 59.8 / 59.6 / 58.4 (the round-two uncapped values) but again on the copula denominator.

## 4. `--json`, and degradation

```bash
uv run --extra discourse python authoring/check_discourse.py --json --cap --no-sources pc_package/PCR-003_bioreactor.qmd | grep -E "passive|and_clause"
uv sync                                                          # base env
uv run python authoring/check_discourse.py pc_package/PCR-003_bioreactor.qmd; echo "exit=$?"   # one line, 0
make test PY="uv run python" | tail -1                           # passes
make style PY="uv run python" | tail -1                          # passes
uv sync --extra discourse                                        # put it back
```

## 5. Done when

Every acceptance line in `state.json` → `TASK-002` is true; `outcome` records the reproduced
row, the passive figures on both denominators with the explanation, and the degradation proof.
