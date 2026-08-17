# TASK-006 procedure — re-author `PCR-003` in one pass, as a DRAFT

Same procedure as `procedures/TASK-005.md`, with these substitutions and additions. **A different
agent from TASK-005's, and it never sees the PCP-003 draft.**

## 1. Preserve and brief

```bash
mkdir -p .claude/work/2026-08-17_01_register-second-round/pre-rewrite
cp pc_package/PCR-003_bioreactor.qmd .claude/work/2026-08-17_01_register-second-round/pre-rewrite/
git diff --quiet f06f1a7 -- pc_package/PCR-003_bioreactor.qmd && echo "round-one text is f06f1a7"
uv run python authoring/build_brief.py PCR-003
grep -n "## 5c\|## 5d\|D-002\|Commercial scale" authoring/out/PCR-003.brief.md
```

## 2. Instantiate

```bash
cp authoring/template.qmd pc_package/PCR-003_bioreactor.DRAFT.qmd
sed -i 's/__DOC_CLASS__/Process Characterization Report/g; s/__DOC__/PCR-003/g; s/__UO_KEY__/bioreactor/g; s/__UO_TITLE__/Production Bioreactor (Step 3)/g' pc_package/PCR-003_bioreactor.DRAFT.qmd
```

Delete the template comment block.

## 3. The agent brief — as in TASK-005 §3, with these changes

- "Process Characterization **Report**", outline `section_plan.yaml` → `report_doe` (bioreactor
  has screening + RSM data; use `doe_report` fully — the brief §4 lists the design).
- Add: "§5c of the brief carries **D-002**: the absolute claim must appear UNQUALIFIED in the
  sentence the brief specifies, followed by the narrower true elaboration. It is a registered
  benchmark item; do not soften it."
- Add: "The Discussion, when it counts the response-surface factors, names them (culture pH,
  temperature, culture duration, dissolved CO2 — pull the names through the helpers, not by
  typing). The Executive summary states the commercial scale through `V["commercial_scale_l"]`."
- Add: "The lack-of-fit and predicted-R² statements name the weakest response through
  `{python}` expressions placed after 'is' or a preposition, never as the subject of an agreeing
  verb."
- The previous revision sat at 8.0 % `, so `, 0.9 % initial connectives, chaining 30.7 %,
  `pct_under_15` 22.7 %.

## 4. Checks (as TASK-005 §4) plus

```bash
grep -c "<<NEEDS" pc_package/PCR-003_bioreactor.DRAFT.qmd                       # 0
grep -n 'V\["commercial_scale_l"\]' pc_package/PCR-003_bioreactor.DRAFT.qmd     # ≥ 1
```

D-002: `grep -n "D-002" -A 12 authoring/discrepancies.yaml` gives the absolute the report must
carry; find it in the draft (wording may differ, the unqualified absolute may not).

Runtime names as subjects: `grep -nE '`\{python\} [a-z_]*resp[a-z_.()]*`\s+(is|are|was|were)\b' pc_package/PCR-003_bioreactor.DRAFT.qmd`
must return nothing.

## 5. Baseline untouched — as TASK-005 §5, for `PCR-003`

Additionally `authoring/rhetorical/PCR-003.spans.yaml` must be unmodified in this task; TASK-007
re-curates it.

## 6. Done when

Every acceptance line in `state.json` → `TASK-006` is true; `outcome` records the model, the
final `clause packing` line, the register table and the pdf glyph result.
