# TASK-002 — the launch prompt for PCR-007

**This is the regime under test.** The prompt is `authoring/RUNNER.md`'s own invocation line plus
the file it writes into and the one halt rule, and nothing else. Do not add a rule, an example, a
measure or a list. If the RUNNER as rebuilt turns out to need something, that is a finding for the
results page (TASK-005), not an edit to this prompt. Given to ONE agent, model `claude-opus-5`, in a
fresh context, by a session that has NOT opened `pc_package/PCR-007_cex.qmd`.

Before launching, TASK-001 must be complete: the brief rebuilt (§2b present, §5d absent), the
DRAFT scaffold instantiated and executing, `blind-key.md` written and unopened.

---

> Author `PCR-007` (Cation Exchange Chromatography, Step 7) per `authoring/RUNNER.md`, into
> `pc_package/PCR-007_cex.DRAFT.qmd`, which is already instantiated from the template. Write the
> whole document in one pass, in the order `authoring/section_plan.yaml` → `report_doe` gives.
>
> Read, and read nothing else for facts or voice: `authoring/RUNNER.md` (the loop),
> `authoring/out/PCR-007.brief.md` (every number comes from here through the helper inventory;
> §2b is the step's mechanism), `authoring/section_plan.yaml`, `authoring/STORY_BIBLE.md`,
> `authoring/WRITING_GUIDE.md`, `authoring/REGISTER_EXEMPLAR.md`. `pc_package/_pcpkg.py` and
> `pc_package/doe_report.py` may be read for function signatures. Do not open any
> `pc_package/*.qmd`, `authoring/rhetorical/` or `authoring/history/`.
>
> Every value is an inline `{python}` expression; a value with no helper becomes
> `<<NEEDS: …>>`, never a typed number. Gate as you go with
> `uv run python authoring/check_render.py pc_package/PCR-007_cex.DRAFT.qmd --render` and fix
> what it reports yourself, in this context. When it passes, render the pdf:
> `cd pc_package && PATH="$PWD/../.venv/bin:$PATH" quarto render PCR-007_cex.DRAFT.qmd --to pdf`.
>
> Report: which model you are, how many `check_render` passes you needed, the pdf result, the
> sentence and word counts, and any `<<NEEDS:>>` left (there should be none).

---

## After the agent reports

1. `uv run python authoring/check_render.py pc_package/PCR-007_cex.DRAFT.qmd --render` — read the
   correctness lines, the tic gate's pass/fail and the glyph line. Nothing else goes into the outcome.
2. `grep -c '<<NEEDS' pc_package/PCR-007_cex.DRAFT.qmd` → 0. If not 0: the helper is missing.
   Extend `_pcpkg.py` / `doe_report.py`, `make test`, rebuild the brief, re-invoke the SAME agent
   with the helper's name. Record it.
3. Typed-measurement grep (state.json TASK-002 acceptance) — every hit listed and inside an
   inline expression, table code or a statistical convention.
4. Section headings against `section_plan.yaml` `report_doe`, in order.
5. Sentence / word / page count: `check_style.sentences(check_style.prose_from_qmd(path))`, the
   count only; pages from the fresh pdf.
6. `git status --short pc_package/` → only the untracked DRAFT and its renders.
7. Outcome: model, passes needed, render, glyphs, `<<NEEDS>>`, sentences, words, pages. Nothing else.
