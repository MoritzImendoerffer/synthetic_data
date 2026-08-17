# TASK-001 procedure — advisory packing counts in `check_style.py`

Read `state.json` → `TASK-001` first (acceptance + notes). This file is the step-by-step.
Everything below runs from the repository root with `uv run python …`.

## 0. Before you touch anything

```bash
uv run python authoring/check_style.py --selftest | tail -3      # expect: "self-test: 4 of 4 human sources measured and passing"
make test PY="uv run python" | tail -2                            # expect: 85 passed
uv run python .claude/work/2026-08-17_01_register-second-round/clause_pack.py
```

The last command prints the table you are about to reproduce inside the gate. Keep its output
open; your numbers must match it.

## 1. Add the patterns, next to `CONNECTIVES` (line ~112 of `authoring/check_style.py`)

Insert after the `CONNECTIVES = (...)` tuple:

```python
# Clause packing. The corpus reasons INSIDE the sentence — a premise, a consequence and a
# recommendation joined by ", so … , and …" — where the four sources end the sentence and open
# the next one with a connective. Measured 2026-08-17 over the same prose this gate reads:
# mid-sentence ", so " in 6–11 % of corpus sentences against 0.1–0.4 % in all four sources;
# sentence-initial connectives in 0–2 % against 3.7–6.1 %. Printed, gated by nothing: a
# ceiling on ", so " is met by writing ", and" or ";", so the whole family is printed together.
CLAUSE_COORD = re.compile(r",\s+(?:so|and|but|since|because|which|while|whereas|yet)\s+", re.I)
SO_MID = re.compile(r",\s+so\s+", re.I)
INITIAL_CONNECTIVE = re.compile(
    r"^(?:However|Therefore|Consequently|As a result|In addition|For this reason|By contrast|"
    r"In contrast|For example|Thus|Hence|Nevertheless|Nonetheless|Moreover|Furthermore|"
    r"Instead|Rather|First|Second|Third|Finally|Overall)\b,?", re.I)
```

## 2. Count them in `measure()` (line ~263)

`measure()` already has `sents = sentences(text)` and `n = len(sents)`. Add, before the `m = {`
dict is built:

```python
    n_so    = sum(1 for s in sents if SO_MID.search(s))
    n_init  = sum(1 for s in sents if INITIAL_CONNECTIVE.match(s))
    n_coord = sum(1 for s in sents if len(CLAUSE_COORD.findall(s)) >= 2)
```

and add to the dict `m`, next to `"_connectives"`:

```python
        "_pct_so_mid":       100.0 * n_so / n,
        "_pct_initial_conn": 100.0 * n_init / n,
        "_pct_coord2":       100.0 * n_coord / n,
        "_n_so_mid": n_so, "_n_initial_conn": n_init, "_n_coord2": n_coord,
```

Keys start with `_` so `evaluate()` (which iterates `LIMITS`, not `m`) never sees them. **Do not
add anything to `LIMITS`.** `len(LIMITS)` stays 12.

## 3. Print one advisory line in `render()` (line ~352, right after the connective line)

Add a helper beside `connective_line()`:

```python
def packing_line(m: dict) -> str:
    """Clause packing, as one advisory line. Nothing here can fail a document."""
    return (f"{'clause packing (diagnostic, never gated)':<48s} "
            f"', so ' mid-sentence {m['_pct_so_mid']:4.1f} % of sentences "
            f"({m['_n_so_mid']}/{m['_n_sent']}), "
            f"opens with a connective {m['_pct_initial_conn']:4.1f} % "
            f"({m['_n_initial_conn']}/{m['_n_sent']}), "
            f"2+ clause coordinators {m['_pct_coord2']:4.1f} %  "
            f"[sources: 0.1-0.4 / 3.7-6.1 / 1.2-3.1]")
```

and in `render()` after `print(f"   --    {connective_line(m)}")`:

```python
    print(f"   --    {packing_line(m)}")
```

## 4. Add three rows to `compare()` (line ~447, after the two connective rows)

```python
    for key, label in (("_pct_so_mid",       "% sentences with mid-sentence ', so ' (not gated)"),
                       ("_pct_initial_conn", "% sentences opening with a connective (not gated)"),
                       ("_pct_coord2",       "% sentences with 2+ clause coordinators (not gated)")):
        print(f"{label:<50s}{'':>11s}" + "".join(f"{m[key]:>{width}.1f}" for _, m in cols))
```

Put this **before** the final `(sentences of prose)` row so the denominators stay last.

## 5. Check the numbers

```bash
uv run python authoring/check_style.py --compare pc_package/PCR-003_bioreactor.qmd pc_package/PCP-003_bioreactor.qmd
```

Expected (columns PDA TR 60 / A-Mab / ISPE TT / ISPE PV / PCR-003 / PCP-003):

```
% sentences with mid-sentence ', so ' (not gated)     0.1   0.3   0.4   0.4   8.0  10.6
% sentences opening with a connective (not gated)     4.8   6.1   4.2   3.7   0.9   1.8
% sentences with 2+ clause coordinators (not gated)   2.3   1.2   1.5   3.1   5.4   9.3
```

If a value differs by more than 0.1, your regex differs from `clause_pack.py`. Diff them; do not
"fix" the expected numbers.

## 6. Prove nothing is gated

```bash
uv run python authoring/check_style.py --selftest | tail -3      # 4 of 4 … passing
make style PY="uv run python" | tail -3                           # exit 0, no new FAIL
uv run python authoring/check_style.py pc_package/PCR-003_bioreactor.qmd | grep -E "clause packing|OK|FAIL"
```

The last must show the packing line AND `OK    register is within the human-source envelope.`

## 7. Add `tests/test_style.py`

```python
"""The register gate's sentence splitter and its advisory clause-packing counts."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "authoring"))
import check_style as cs

FIXTURE = (
    "The tests rest on four replicates, so a result bounds the evidence, and the case is open. "
    "Therefore, the model is provisional. "
    "The range was set wider than the control range, so that the study measures robustness. "
    "The step meets its criterion."
)

def test_sentences_splits_four():
    assert len(cs.sentences(FIXTURE)) == 4

def test_packing_counts():
    m, *_ = cs.measure(FIXTURE)
    assert m["_n_so_mid"] == 2          # sentences 1 and 3
    assert m["_n_initial_conn"] == 1    # "Therefore, …"
    assert m["_n_coord2"] == 1          # sentence 1: ", so" and ", and"
    assert m["_n_sent"] == 4

def test_limits_unchanged():
    assert len(cs.LIMITS) == 12
    assert not any(k.startswith("_pct_") for k in cs.LIMITS)
```

Note: `measure()` returns `{}` for fewer than… no — `measure()` returns numbers for any sentence
count; only `evaluate()` skips under `MIN_SENTENCES`. If `test_sentences_splits_four` fails, the
fixture's fourth sentence has fewer than 4 words for `sentences()`' `4 <= len <= 150` filter —
lengthen it, do not change the filter.

```bash
make test PY="uv run python" | tail -2         # expect: 88 passed (85 + 3)
```

## 8. Done when

All acceptance lines in `state.json` → `TASK-001` are true. Record in the task's `outcome`: the
three compare rows verbatim and the new test count. Do not edit any `.qmd`, the guide, or the
exemplar in this task.
