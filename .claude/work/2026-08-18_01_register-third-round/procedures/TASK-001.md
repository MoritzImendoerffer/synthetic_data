# TASK-001 procedure — the two regex counts, from the never-saved measure into `check_style.py`

Read `state.json` → `TASK-001` first. Everything runs from the repository root under `uv run python`.

## 0. Before you touch anything

```bash
uv run python authoring/check_style.py --selftest | tail -1      # 4 of 4 human sources measured and passing
make test PY="uv run python" | tail -1                            # 88 passed
cat .claude/work/2026-08-17_01_register-second-round/measure_owner_reading.txt
uv run --extra discourse python .claude/work/2026-08-18_01_register-third-round/andclause.py 2>/dev/null
```

The first file is the table you are about to reproduce (its `', and '+clause` and `', not '`
columns). The second script prints the regex column beside the parser column. Keep both open.

## 1. Add the patterns, next to `INITIAL_CONNECTIVE` (line ~123)

```python
# Two more advisory counts, added 2026-08-18 after the project owner read the round-two PCR-003
# and named the balanced two-clause sentence — "…forms the … attributes of A-Mab, and this
# report bounds the culture conditions that set them" — as the thing that gave it away. Counted
# afterwards: 18–23 % of corpus sentences against 1.1–3.4 % in the four sources, and the round
# that drove ", so " to zero did not move it, because nothing printed it back.
#
# AND_CLAUSE is a FLOOR. It matches ", and" followed by a fixed list of clause openers, so it
# misses a second clause opening on a bare noun ("…, and osmolality was not"; "…, and both were
# retained"). Measured 2026-08-18 it undercounts the corpus by 2–6 points and matches the four
# sources within 0.5. The parser count in check_discourse.py is the other half; neither is a
# superset of the other, and both are printed. Gated by nothing.
AND_CLAUSE = re.compile(
    r",\s+and\s+(?:the|this|that|these|those|it|they|he|she|we|its|their|a|an|[a-z]+ing)\b", re.I)
NOT_TAIL = re.compile(r",\s+not\s+", re.I)
```

## 2. Count them in `measure()` (line ~291, beside `n_so` / `n_init` / `n_coord`)

```python
    n_and   = sum(1 for s in sents if AND_CLAUSE.search(s))
    n_not   = sum(1 for s in sents if NOT_TAIL.search(s))
```

and in the dict `m`, after `_pct_coord2`:

```python
        "_pct_and_clause":   100.0 * n_and / n,
        "_pct_not_tail":     100.0 * n_not / n,
        "_n_and_clause": n_and, "_n_not_tail": n_not,
```

`len(LIMITS)` stays 12. Do not touch `BANNED`.

## 3. Extend `packing_line()` (line ~358)

Append two figures **after** the 2+ coordinator figure, so the family reads left to right:

```python
            f"2+ clause coordinators {m['_pct_coord2']:4.1f} %, "
            f"', and '+clause {m['_pct_and_clause']:4.1f} % ({m['_n_and_clause']}/{m['_n_sent']}), "
            f"', not ' {m['_pct_not_tail']:4.1f} % ({m['_n_not_tail']}/{m['_n_sent']})  "
            f"[sources: 0.1-0.4 / 3.7-6.1 / 1.2-3.1 / 1.1-3.4 / 0.0-0.2]")
```

(The line gets long. If it wraps badly, break it into two `print`s in `render()`; the content is
what matters.)

## 4. Two rows in `compare()` (line ~485), before `(sentences of prose)`

```python
                       ("_pct_and_clause",   "% sentences with ', and ' + a second clause (floor; not gated)"),
                       ("_pct_not_tail",     "% sentences with mid-sentence ', not ' (not gated)"),
```

Add them to the existing tuple that prints `_pct_so_mid` / `_pct_initial_conn` / `_pct_coord2`.

## 5. Reproduce the round-two table

```bash
R0=.claude/work/2026-08-16_01_register-from-four-sources/pre-rewrite
R1=.claude/work/2026-08-17_01_register-second-round/pre-rewrite
uv run python authoring/check_style.py --compare \
   $R0/PCR-003_bioreactor.qmd $R1/PCR-003_bioreactor.qmd pc_package/PCR-003_bioreactor.qmd pc_package/PCP-003_bioreactor.qmd
```

Expected (PDA / A-Mab / ISPE TT / ISPE PV / PCR-003 r0 / r1 / r2 / PCP-003 r2):

```
% sentences with ', and ' + a second clause (floor; not gated)   3.4  1.1  1.3  3.1  24.9  21.0  22.6  18.2
% sentences with mid-sentence ', not ' (not gated)               0.2  0.0  0.1  0.0   0.0   0.0   4.3   0.0
```

If a value differs by more than 0.1, your regex differs from `andclause.py`. Diff them.

## 6. Nothing gated

```bash
uv run python authoring/check_style.py --selftest | tail -1        # 4 of 4
make style PY="uv run python" 2>&1 | grep -cE "^OK"                 # 24
make style PY="uv run python" 2>&1 | grep -cE "FAIL"                # 0
uv run python authoring/check_style.py pc_package/PCR-003_bioreactor.qmd | grep -E "clause packing|^OK"
```

## 7. `tests/test_style.py` — extend

```python
FIXTURE_AND = (
    "The screening study covered five parameters, and the remaining four were assessed one at a time. "
    "The design space rests on the response surface model, not on the screening fit. "
    "Galactosylation, high mannose, and afucosylation were measured on one separation. "
    "The step meets its criterion in every run."
)

def test_and_clause_and_not_tail():
    m, *_ = cs.measure(FIXTURE_AND)
    assert m["_n_sent"] == 4
    assert m["_n_and_clause"] == 1     # sentence 1 only; the Oxford comma in sentence 3 must NOT count
    assert m["_n_not_tail"] == 1       # sentence 2
```

```bash
make test PY="uv run python" | tail -1        # 89 passed
```

## 8. Done when

All acceptance lines in `state.json` → `TASK-001` are true. Record the two compare rows verbatim
and the new test count in `outcome`. Do not edit any `.qmd`, the guide or the exemplar here.
