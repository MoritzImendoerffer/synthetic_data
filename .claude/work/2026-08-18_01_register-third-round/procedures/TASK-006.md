# TASK-006 procedure — four points, one method, the rule, the reading

**Follow `../../2026-08-17_01_register-second-round/procedures/TASK-008.md` top to bottom, with
these substitutions.** Read `state.json` → `decisions.stopping_rule_edges` before starting; the
edges are fixed and are not moved after the numbers are seen.

## The four points, on disk

| point | file |
|---|---|
| round zero (`b0361f1`) | `.claude/work/2026-08-16_01_register-from-four-sources/pre-rewrite/PCR-003_bioreactor.qmd` |
| round one (`f06f1a7`) | `.claude/work/2026-08-17_01_register-second-round/pre-rewrite/PCR-003_bioreactor.qmd` |
| round two (`e7a4768`) | `.claude/work/2026-08-18_01_register-third-round/pre-rewrite/PCR-003_bioreactor.qmd` |
| round three | `pc_package/PCR-003_bioreactor.qmd` |
| **control**: `PCP-003` round two | `pc_package/PCP-003_bioreactor.qmd` (unchanged since `e7a4768`) |

All verified byte-identical to their commits by `/explore` (exploration §2) and TASK-004.

## The runs (each ONE invocation, all five files, saved into this unit)

```bash
R0=.claude/work/2026-08-16_01_register-from-four-sources/pre-rewrite
R1=.claude/work/2026-08-17_01_register-second-round/pre-rewrite
R2=.claude/work/2026-08-18_01_register-third-round/pre-rewrite
W=.claude/work/2026-08-18_01_register-third-round
F="$R0/PCR-003_bioreactor.qmd $R1/PCR-003_bioreactor.qmd $R2/PCR-003_bioreactor.qmd pc_package/PCR-003_bioreactor.qmd pc_package/PCP-003_bioreactor.qmd"
uv run python authoring/check_style.py --compare $F               > $W/measure_style.txt
uv run --extra discourse python authoring/check_discourse.py $F        > $W/measure_discourse.txt
uv run --extra discourse python authoring/check_discourse.py --cap $F  > $W/measure_discourse_cap.txt
```

Possessives / `it is` / `the <noun> is`: the previous unit's `measure_possessive.txt` snippet, over
the five files → `$W/measure_possessive.txt`.

## The page: `docs/results/<today>-register-round-three.md`

The previous unit's TASK-008 skeleton, plus these sections:

- **What round two's reading named, four points** — the three new measures, regex AND parser for
  the and-clause, with the round-two heredoc figures footnoted (passive 34.4 on all sentences vs
  35.4 on the copula denominator — TASK-002's note says why).
- **The control column** — `PCP-003` at round two on every measure. State it: a move in `PCR-003`
  alone is "moved in the report".
- **The overshoot check** — is `, and `+clause below ALL sources (< 1.1 %)? Is passive above the
  band (> 60 %)? Name what paid for any move: semicolons (ceiling 4.5/1k), `, which`, `pct_under_15`.
- **The three "screening retained" sentences** — gone? what replaced them, quoted.
- **The stopping rule, line by line** — the eight conditions from `decisions.stopping_rule_edges`,
  a table with `holds?`, then the verdict sentence.
- **The owner's reading** — verbatim, dated, "not blind: fourth read", and whatever is quoted is
  counted afterwards, in that order, in a following section.

Every number from `$W/measure_*.txt`. Verify by script that every cell on the page is in a file,
as round two's TASK-008 did.

## `docs/results/README.md`

One row, saying why the run happened and linking the page.
