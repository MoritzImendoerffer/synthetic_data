# Shared procedure — re-author ONE document in one pass, as a DRAFT

**Used by all 19 `document` tasks.** Read `state.json` → that task first: it names the document,
its `section_plan.yaml` outline, its annex exposure, and whether it carries a registered
discrepancy. This file is the tested loop from
`2026-08-18_01_register-third-round/procedures/TASK-004.md`, generalised.

Substitute `<DOC>` (e.g. `PCR-006`), `<uokey>` (`viral_inactivation`) and `<OUTLINE>`
(`report_doe`) throughout.

## 1. Preserve and brief

```bash
U=.claude/work/2026-08-18_02_register-track-d
mkdir -p $U/pre-rewrite
cp pc_package/<DOC>_<uokey>.qmd $U/pre-rewrite/
git show HEAD:pc_package/<DOC>_<uokey>.qmd | diff -q - $U/pre-rewrite/<DOC>_<uokey>.qmd && echo PRESERVED
uv run --extra discourse python authoring/build_brief.py <DOC>
grep -n "## 5c\|## 5d" authoring/out/<DOC>.brief.md      # both must be present
```

The `--extra discourse` matters: without it §5d loses the passive row, which is one of the three
measures this campaign added.

## 2. Instantiate

```bash
cp authoring/template.qmd pc_package/<DOC>_<uokey>.DRAFT.qmd
sed -i 's/__DOC_CLASS__/<the class from DOC_REGISTRY>/g; s/__DOC__/<DOC>/g; s/__UO_KEY__/<uokey>/g; s/__UO_TITLE__/<the title>/g' pc_package/<DOC>_<uokey>.DRAFT.qmd
```

Then delete the template's comment block. The file must stay in `pc_package/` so
`from _pcpkg import *`, `../outputs/…` and `reference.docx` resolve.

## 3. Launch ONE authoring agent, with this brief

> Author `<DOC>` per `authoring/RUNNER.md`, into `pc_package/<DOC>_<uokey>.DRAFT.qmd`, which is
> already instantiated from the template. Write the whole document in one pass, in the order
> `authoring/section_plan.yaml` → `<OUTLINE>` gives.
>
> Read, in this order, and nothing else for voice or facts: `authoring/WRITING_GUIDE.md` (all of
> it), `authoring/out/<DOC>.brief.md` (every number comes from here through the helper inventory;
> §5c names any registered discrepancy this document must carry, §5d gives the discourse targets
> and where this document currently stands), `authoring/section_plan.yaml`,
> `authoring/REGISTER_EXEMPLAR.md`, `authoring/STORY_BIBLE.md`. **Do not open any
> `pc_package/*.qmd`**, including this document's current text and every sibling, and do not open
> `authoring/rhetorical/`. Reading `pc_package/_pcpkg.py` and `pc_package/doe_report.py` for
> helper signatures is allowed — they are code, not documents.
>
> Rules that decide this round: one argument step per sentence — a consequence, contrast or
> recommendation opens the NEXT sentence with its connective, never rides on `, so …` or
> `, and …`; the definite article or the noun, never `it is`; name any set you count; a
> `{python}` expression that yields a name is never the subject of a verb that agrees with it; a
> study, a design, a model or a process is never the AGENT of retain, carry, identify or select —
> write the passive the sources would write. Every value is an inline `{python}` expression; a
> value with no helper becomes `<<NEEDS: …>>`, never a typed number.
>
> **The passive is a BAND and never a floor.** The four sources sit at 56.9–64.0 % of the
> sentences that have a root and a subject. Brief §5d prints where this document stands. If it is
> already inside or above that band, do not add passives; write them where the sources would and
> nowhere else.
>
> Search your draft before you finish, for each of: `, so `, `, and the`, `, and this`,
> `, and both`, `, and it`, `, and each`, `, not `, `screening retained`, `the design carries`,
> `the study selected`, `the model identifies`.
>
> Gate as you go: `uv run python authoring/check_render.py pc_package/<DOC>_<uokey>.DRAFT.qmd
> --render`. Read the `clause packing` line each time. On a HARD failure fix it yourself in the
> same context; do not hand off and do not start a fresh context. When it passes, render the pdf:
> `cd pc_package && PATH="$PWD/../.venv/bin:$PATH" quarto render <DOC>_<uokey>.DRAFT.qmd --to pdf`.
>
> Report: which model you are, the final `clause packing` line verbatim, the final register table
> verbatim, the pdf result, sentence and word counts, and any `<<NEEDS:>>` left (there should be
> none).

## 4. Check it yourself — do not take the agent's word

```bash
D=pc_package/<DOC>_<uokey>.DRAFT.qmd
uv run python authoring/check_render.py $D --render | tail -30
cd pc_package && PATH="$PWD/../.venv/bin:$PATH" quarto render <DOC>_<uokey>.DRAFT.qmd --to pdf && cd ..
uv run python authoring/check_render.py $D | grep -i glyph      # on the FRESH pdf
grep -c "<<NEEDS" $D                                             # 0
grep -c 'screening retained\|screening identified\|the design carries\|the model identifies\|the study selected' $D   # 0
grep -nE '`\{python\} [a-z_]*resp[a-z_.()]*`\s+(is|are|was|were)\b' $D    # nothing
grep -nE "\b[0-9]+(\.[0-9]+)?\s?(%|°C|mmHg|g/L|L\b|mM|h\b|days?)" $D      # each hit must be inside an inline expr or a statistical convention
git status --short pc_package/                                   # only the DRAFT and its untracked renders
```

**If the task's document carries a registered discrepancy**, open `authoring/discrepancies.yaml`,
find the assignment, and confirm the draft carries that commitment. The wording may differ; the
strength may not. `TASKS.md` item 7 is the failure mode and nothing automated catches it.

## 5. Done when

Every acceptance line in `state.json` for that task is true. Put in `outcome`: the model that
authored it, the final `clause packing` line, the register table, the pdf glyph result and the
page count. **Do not promote the draft** — that is the batch's annex task.
