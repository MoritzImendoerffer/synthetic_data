---
type: pm-artifacts
tags: [pm]
---

# The artifacts a task has to leave standing

What a build produces, and what every task is checked against before it is `done`. Counts are from
an unmodified checkout on 2026-08-16.

## What is on disk

| Artifact | Count | Where it comes from |
|---|---|---|
| corpus documents (`.qmd`) | 20 | authored once, one pass each |
| rendered `.docx` | 21 | `make corpus` — 20 documents plus `reference.docx`, which is a build **input** and is not regenerable |
| rendered `.pdf` | 20 | `make corpus` |
| ground-truth annexes | 20 | `pc_package/build_ground_truth.py` |
| datasets | 34 files in `outputs/data/` | `make data` from `config/parameters.yaml` |
| figures | 13 in `outputs/figures/` | `make figures` |

The first-pass documents in `pc_package/first_pass/` are kept for comparison only. They are never
an input to anything.

## The gates, and what each one prints

```bash
make test PY="uv run python"                       # 85 passed
make style PY="uv run python"                      # register gate, every .qmd
cd pc_package && uv run python build_ground_truth.py \
  && uv run python validate_annex.py \             # 20/20 annexes valid
  && GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py
                                                   # 2084/2084 quotes grounded, 0 weak anchors
uv run python authoring/check_render.py <doc>.qmd --render   # eval, render, PDF glyphs, style
```

**Quote a gate by its numbers, not by the word "passes".** Every one of them prints a count with a
denominator for that reason.

## The two traps that cost the most time

**`PY=` is not enough for `make corpus`.** Quarto starts its own Jupyter kernel and resolves
`python3` from `PATH`, not from `PY`. Put the venv on `PATH` for the whole build:

```bash
PATH="$PWD/.venv/bin:$PATH" make corpus PY="uv run python"
```

**A render can succeed and still be wrong.** Before `check_render.py` gained its PDF glyph check,
398 missing-glyph boxes shipped across 8 documents: `≥ 4.93` rendered as `␀ 4.93`, which turns a
clearance floor into a point value.

## What must not drift

- **`outputs/data/doe_*.csv` and `effects_*.csv`** shift in the deep decimals when regenerated in
  a different library environment. The committed CSVs are the baseline. `git diff` any `outputs/`
  change and commit only intended data.
- **The 21 tracked `.docx`.** While iterating on a document, author under
  `pc_package/<DOC>_<uokey>.DRAFT.qmd`, whose `.docx` is untracked.
- **`authoring/DISCREPANCIES.md`.** D-001 and D-002 are deliberate benchmark items. Fixing one
  without removing its entry deletes the benchmark item silently.
- **`weak_claims` is empty in all 20 annexes on `main`**, without exception. Labeled weak claims
  live only on `feature/weak-claims-via-brief`, which is carried forward by rebasing and never
  merged back.
