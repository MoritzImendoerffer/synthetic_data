# TASK-005 procedure — re-author `PCP-003` in one pass, as a DRAFT

Read `state.json` → `TASK-005` first. TASK-006 (`PCR-003`) follows the same procedure with the
other document; **run them as two separate agents that never see each other's draft.** They may
run at the same time.

## 1. Preserve round one and regenerate the brief

```bash
mkdir -p .claude/work/2026-08-17_01_register-second-round/pre-rewrite
cp pc_package/PCP-003_bioreactor.qmd .claude/work/2026-08-17_01_register-second-round/pre-rewrite/
git diff --quiet f06f1a7 -- pc_package/PCP-003_bioreactor.qmd && echo "round-one text is f06f1a7"   # must print
uv run python authoring/build_brief.py PCP-003
grep -n "## 5c\|## 5d\|D-001\|Commercial scale" authoring/out/PCP-003.brief.md      # all four present
```

If §5d shows "no previous revision", TASK-004 is not done — stop.

## 2. Instantiate the template as a DRAFT

```bash
cp authoring/template.qmd pc_package/PCP-003_bioreactor.DRAFT.qmd
sed -i 's/__DOC_CLASS__/Process Characterization Plan/g; s/__DOC__/PCP-003/g; s/__UO_KEY__/bioreactor/g; s/__UO_TITLE__/Production Bioreactor (Step 3)/g' pc_package/PCP-003_bioreactor.DRAFT.qmd
```

Then delete the template's comment block (it says "TEMPLATE — do not author here"). The file must
stay in `pc_package/` so `from _pcpkg import *` resolves.

## 3. Launch ONE authoring agent with this brief (copy it; fill nothing else in)

> Author `PCP-003` (Production Bioreactor, Step 3 — Process Characterization **Plan**) per
> `authoring/RUNNER.md`, into `pc_package/PCP-003_bioreactor.DRAFT.qmd`, which is already
> instantiated from the template. Write the whole document in one pass, in the order
> `authoring/section_plan.yaml` → `plan` gives.
>
> Read, in this order, and nothing else for voice or facts: `authoring/WRITING_GUIDE.md` (all of
> it; §2d, §2d bis and §4 changed on 2026-08-17), `authoring/out/PCP-003.brief.md` (every number
> comes from here through the helper inventory in §7; §5c names the registered discrepancy this
> document must carry, §5d gives the discourse targets and where the previous revision stood),
> `authoring/section_plan.yaml`, `authoring/REGISTER_EXEMPLAR.md`, `authoring/STORY_BIBLE.md`.
> **Do not open any `pc_package/*.qmd`**, including the previous `PCP-003` and the `PCR-003`
> draft; `authoring/check_blank_repo.sh` exists to prove this is possible.
>
> Rules that decide this round: one argument step per sentence — a consequence, contrast or
> recommendation opens the next sentence with its connective, never rides on `, so …` or
> `, and …`; the definite article or the noun, never `it is`; name any set you count; a
> `{python}` expression that yields a name is never the subject of a verb that agrees with it;
> state the commercial scale through `V["commercial_scale_l"]`. Every value is an inline
> `{python}` expression; a value with no helper becomes `<<NEEDS: …>>`, never a typed number.
>
> Gate as you go: `uv run python authoring/check_render.py pc_package/PCP-003_bioreactor.DRAFT.qmd --render`.
> It prints a line beginning `clause packing (diagnostic, never gated)`; read it each time. The
> register bands are hard; `pct_under_15` has a 32 % ceiling and the previous revision sat at
> 20.4 %, so splitting sentences has room but not unlimited room. On a HARD failure fix it
> yourself in the same context; do not hand off. When it passes, also run
> `cd pc_package && quarto render PCP-003_bioreactor.DRAFT.qmd --to pdf` and report the last
> `clause packing` line and the last register table verbatim.

Record which model authored the document (RUNNER.md asks for it) in the task `outcome`.

## 4. When the agent reports back, check yourself

```bash
uv run python authoring/check_render.py pc_package/PCP-003_bioreactor.DRAFT.qmd --render | tail -30
cd pc_package && quarto render PCP-003_bioreactor.DRAFT.qmd --to pdf && cd ..
grep -c "<<NEEDS" pc_package/PCP-003_bioreactor.DRAFT.qmd                 # 0
grep -n 'V\["commercial_scale_l"\]' pc_package/PCP-003_bioreactor.DRAFT.qmd   # ≥ 1
```

D-001: open `authoring/discrepancies.yaml`, find D-001's `registered_sentence` / commitment
description, and confirm the draft carries the at-set-point commitment the brief's §5c specifies
(the wording may differ; the commitment may not).

Typed numbers: `grep -nE "\b[0-9]+(\.[0-9]+)?\s?(%|°C|mmHg|g/L|L\b|mM|h\b|days?)" pc_package/PCP-003_bioreactor.DRAFT.qmd`
— every hit must be inside a `{python}` expression or a caption built from one. A bare typed
measurement is a HARD failure; send it back to the same agent.

## 5. Baseline untouched

```bash
git status --short pc_package/ authoring/out/
```

Must show only: `?? pc_package/PCP-003_bioreactor.DRAFT.qmd` (+ its untracked .docx/.pdf) and
`M authoring/out/PCP-003.brief.md`. If `pc_package/PCP-003_bioreactor.qmd` or any
`ground_truth/*.json` is modified, something wrote to the wrong file — restore it with
`git checkout -- <that one file>` (one file by name, never the directory).

## 6. Done when

Every acceptance line in `state.json` → `TASK-005` is true. Put in `outcome`: the model that
authored it, the final `clause packing` line, the register table, and the pdf glyph result. **Do
not** promote the draft here — that is TASK-007.
