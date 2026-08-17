# TASK-003 procedure — `check_discourse.py` behind an optional spaCy extra

Read `state.json` → `TASK-003` first. Owner decision: spaCy is **optional**. The corpus must
build, render, annex and ground on a checkout that never installed it.

## 1. `pyproject.toml` — the optional group

Add after the `dependencies = [...]` list:

```toml
[project.optional-dependencies]
# Parser for authoring/check_discourse.py (advisory register diagnostics). Nothing in
# make test / style / corpus needs it. Install with: uv sync --extra discourse
discourse = [
    "spacy>=3.8,<3.9",
    "en-core-web-sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl",
]
```

Then:

```bash
uv lock                       # regenerates uv.lock; must succeed
uv sync --extra discourse     # installs spacy + the model into .venv
uv run --extra discourse python -c "import spacy; spacy.load('en_core_web_sm'); print('ok')"   # ok
```

If `uv lock` rejects the direct URL, the syntax is `name @ url` exactly as above (PEP 508). If it
complains the wheel's name is `en_core_web_sm` (underscores), use that spelling — match the wheel's
metadata name.

## 2. `requirements-discourse.txt` — the pip mirror

```
# Optional: parser for authoring/check_discourse.py. pip install -r requirements-discourse.txt
spacy>=3.8,<3.9
https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
```

`requirements.txt` is not edited.

## 3. `authoring/check_discourse.py` — write this file

```python
#!/usr/bin/env python3
"""Discourse diagnostics for one or more corpus documents, against the four human sources.

    uv run --extra discourse python authoring/check_discourse.py pc_package/PCR-003_bioreactor.qmd
    uv run --extra discourse python authoring/check_discourse.py --cap --json <qmd> ...

Three measures a writer cannot self-verify without a parser, printed with denominators and the
four source columns so the gap is legible:

  topic chaining  % of sentences whose subject names something the previous sentence mentioned
                  (NOUN/PROPN/ADJ lemma overlap) or is a pronoun
  copula          % of sentences whose ROOT lemma is "be"
  front field     % of sentences with any non-punctuation token before the subject phrase

ADVISORY, NEVER A GATE. A floor on chaining is met by typing a pronoun. Nothing in make test,
make style or make corpus calls this, and it must not be added there.

spaCy is an OPTIONAL extra (`uv sync --extra discourse`). Without it this script prints one
line and exits 0.

--cap reproduces the caps register_analysis.ipynb section 13 used (600 sentences for
chaining, 450 for copula/front field), so the numbers on docs/results/2026-08-17-register-pilot.md
can be reproduced exactly. Without --cap every sentence is measured.

Reuses check_style.prose_from_qmd / prose_from_extract / sentences / HUMAN_SOURCES so it
measures the same text the register gate does.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from check_style import HUMAN_SOURCES, prose_from_extract, prose_from_qmd, sentences  # noqa: E402

DEGRADE = ("check_discourse: spaCy is not installed; this diagnostic is optional. "
           "Install with `uv sync --extra discourse` and re-run. (exit 0)")

CAP_CHAIN, CAP_COPFRONT = 600, 450   # the notebook's caps


def load_nlp():
    try:
        import spacy
    except ImportError:
        return None
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        return None


def prep(text: str) -> list[str]:
    # The notebook parses the gate's sentence list with the NUM placeholder made numeric.
    return [s.replace("NUM", "12.3") for s in sentences(text)]


def topic_chaining(nlp, sents, cap=None):
    docs = [nlp(s) for s in (sents[:cap] if cap else sents)]
    chained = pairs = 0
    for prev, cur in zip(docs, docs[1:]):
        subj = next((t for t in cur if t.dep_ in ("nsubj", "nsubjpass")), None)
        if subj is None:
            continue
        pairs += 1
        prev_l = {t.lemma_.lower() for t in prev if t.pos_ in ("NOUN", "PROPN", "ADJ")}
        subj_l = {t.lemma_.lower() for t in subj.subtree if t.pos_ in ("NOUN", "PROPN", "ADJ")}
        chained += bool(subj_l & prev_l) or subj.pos_ == "PRON"
    return chained, pairs


def copula_front(nlp, sents, cap=None):
    cop = front = n = 0
    for s in (sents[:cap] if cap else sents):
        doc = nlp(s)
        root = next((t for t in doc if t.dep_ == "ROOT"), None)
        subj = next((t for t in doc if t.dep_ in ("nsubj", "nsubjpass")), None)
        if root is None or subj is None:
            continue
        n += 1
        cop += int(root.lemma_ == "be")
        start = min(t.i for t in subj.subtree)
        front += bool([t for t in doc[:start] if not t.is_punct and not t.is_space])
    return cop, front, n


def measure(nlp, text, cap):
    sents = prep(text)
    ch, pairs = topic_chaining(nlp, sents, CAP_CHAIN if cap else None)
    cop, front, n = copula_front(nlp, sents, CAP_COPFRONT if cap else None)
    pct = lambda a, b: 100.0 * a / b if b else 0.0
    return {"chaining_pct": pct(ch, pairs), "chaining": [ch, pairs],
            "copula_pct": pct(cop, n), "copula": [cop, n],
            "front_pct": pct(front, n), "front": [front, n],
            "n_sentences": len(sents)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("qmd", nargs="*")
    ap.add_argument("--cap", action="store_true",
                    help="reproduce the notebook's caps (600 sentences chaining, 450 copula/front)")
    ap.add_argument("--json", action="store_true", help="machine-readable output for build_brief.py")
    ap.add_argument("--no-sources", action="store_true", help="skip the four human columns")
    a = ap.parse_args()

    nlp = load_nlp()
    if nlp is None:
        print(DEGRADE)
        return 0

    cols = []
    if not a.no_sources:
        for name, fname, lo, hi in HUMAN_SOURCES:
            path = os.path.join(ROOT, "refs", "text", fname)
            if os.path.exists(path):
                cols.append((name, measure(nlp, prose_from_extract(path, lo, hi), a.cap)))
    for q in a.qmd:
        if not os.path.exists(q):
            print(f"FAIL  no such file: {q}")
            return 1
        cols.append((os.path.basename(q), measure(nlp, prose_from_qmd(q), a.cap)))

    if a.json:
        print(json.dumps({"cap": a.cap, "columns": dict(cols)}, indent=1))
        return 0

    width = max(len(n) for n, _ in cols) + 2
    print("discourse diagnostics (advisory, never gated)" + ("  [notebook caps]" if a.cap else ""))
    print(f"{'measure':<40s}" + "".join(f"{n:>{width}s}" for n, _ in cols))
    for key, cnt, label in (("chaining_pct", "chaining", "topic chaining % (chained/pairs)"),
                            ("copula_pct", "copula", "copula main verb % (copula/n)"),
                            ("front_pct", "front", "adjunct front field % (front/n)")):
        print(f"{label:<40s}" + "".join(
            f"{m[key]:>{width - 12}.1f} ({m[cnt][0]}/{m[cnt][1]})".rjust(width) for _, m in cols))
    print(f"{'(sentences of prose)':<40s}" + "".join(f"{m['n_sentences']:>{width}d}" for _, m in cols))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

The column formatting is a suggestion; keep the values and denominators. If a cell overflows,
widen `width`.

## 4. Reproduce the pilot's numbers

```bash
uv run --extra discourse python authoring/check_discourse.py --cap \
    pc_package/PCR-003_bioreactor.qmd pc_package/PCP-003_bioreactor.qmd
```

Expected (±0.5 pt; the counts should match exactly with spaCy 3.8 + model 3.8.0):

| | PDA TR 60 | A-Mab | ISPE TT | ISPE PV | PCR-003 | PCP-003 |
|---|---|---|---|---|---|---|
| chaining | 59.4 (332/559) | 59.0 (315/534) | 61.9 (348/562) | 57.0 (321/563) | 30.7 (127/414) | 34.4 (77/224) |
| copula | 17.6 (74/420) | 14.8 (61/412) | 22.4 (95/424) | 26.1 (110/422) | 32.5 (135/415) | 27.6 (62/225) |
| front | 27.1 (114/420) | 33.5 (138/412) | 35.6 (151/424) | 36.3 (153/422) | 9.2 (38/415) | 10.2 (23/225) |

If chaining is off by more than 0.5 pt, the most likely cause is `prep()` — the notebook
replaced `NUM` with `12.3` before parsing; do the same. If copula/front denominators differ, the
cap is applied to the wrong list. Do not adjust the expected numbers.

Then run once without `--cap` and note the full-text values in the task outcome; TASK-008 uses
the uncapped numbers for the round-two page and states so.

## 5. Prove it degrades

```bash
uv sync                                                        # base env, extra removed
uv run python authoring/check_discourse.py pc_package/PCR-003_bioreactor.qmd
# expect exactly the one DEGRADE line, and exit code 0:
echo $?
make test PY="uv run python" | tail -2                         # passes without spacy
make style PY="uv run python" | tail -2                        # passes without spacy
uv sync --extra discourse                                      # put it back for TASK-004+
```

## 6. Makefile — an optional target, wired to nothing

Add near `style:` (do NOT add it to `all`, `corpus`, `style` or `test`):

```make
# Advisory discourse diagnostics (topic chaining, copula, front field). Needs the optional
# extra: uv sync --extra discourse. Wired to nothing; without spaCy it prints one line.
discourse:
	$(PY) authoring/check_discourse.py $(PKG_DIR)/*.qmd
```

and a help line. Check: `grep -n "discourse" Makefile` shows only that block and the help line.

## 7. `CLAUDE.md` — one sentence in *Environment*

After the `uv sync` sentence: "spaCy is an **optional** extra (`uv sync --extra discourse`,
mirrored in `requirements-discourse.txt`) used only by the advisory `authoring/check_discourse.py`;
the corpus builds without it."

## 8. Done when

Every acceptance line in `state.json` → `TASK-003` is true. Record in `outcome`: the reproduced
table, the uncapped numbers, and the `uv lock` diff size. **Do not** import spaCy anywhere else
in the repository.
