# TASK-003 — the probe launch prompt

**This file IS the experiment.** The prompt between the rules below is given to ONE agent,
model `claude-opus-5`, verbatim, and nothing else is said to it before it reports. Do not add a
rule, do not add a warning, do not add an example, do not print a measure back to it. If it asks a
question, answer only with a fact from the four files it is allowed to read.

Before launching, confirm TASK-002 is complete: `blind-key.md` exists, `probe-guide.md` is at
most 12 lines, `PCR-005.brief.probe.md` has no §5c/§5d, `PCR-005_protein_a.PROBE.qmd` executes
under `check_render.py --lax-style`. The session that launches the agent must not have opened
`pc_package/PCR-005_protein_a.qmd` in the same context.

Substitute `$U` with `.claude/work/2026-08-18_03_author-facing-apparatus`.

---

> Write two subsections of a process characterization report for the Protein A chromatography
> step of the A-Mab monoclonal antibody process: `## Response-surface models` and
> `## Mechanistic interpretation`, in that order, into `pc_package/PCR-005_protein_a.PROBE.qmd`,
> replacing the two placeholder headings under `# Results`. Leave the SETUP chunk and the front
> matter as they are.
>
> Read, and read nothing else for facts or voice:
>
> - `$U/probe-guide.md` — how to write it, one page.
> - `$U/PCR-005.brief.probe.md` — the facts of this study and the helper inventory (§7). Every
>   number in your text is an inline `` `{python} …` `` expression built from §7 or from the
>   scalars in the SETUP chunk; never type a number. If no helper gives a value you need, write
>   `<<NEEDS: what>>` in its place and keep writing.
> - `authoring/STORY_BIBLE.md` — the world these documents live in.
> - `$U/probe-setup.py` — the SETUP chunk of the file you are writing into, so you know which
>   scalars and figures exist (`fits_rsm`, `rcoef`, `rcoef_p`, `n_sig_rsm`, `cp_rsm`, `cvr`,
>   `lpa_*`, `D.fit_summary_df`, `D.rsm_coeff_df`, `D.anova_lof_df`, `D.fig_rsm_contours`,
>   `D.fig_diagnostics`).
> - `pc_package/_pcpkg.py` and `pc_package/doe_report.py`, for function signatures only.
>
> Do not open any other file under `pc_package/` or `authoring/`.
>
> The first subsection reports the fitted response-surface models for the three responses
> (adequacy, the terms that matter, lack of fit, diagnostics), narrating the tables and figures
> the SETUP chunk provides. The second explains why the surfaces have the shape they have, from
> the physical chemistry of affinity capture, and what that means for how the step should be
> operated. You are the process scientist who ran this study. Write it as you would write it for
> a paper.
>
> Write once. Do not run any checker. When the two subsections are written, report: which model
> you are, the number of sentences and words you wrote, and any `<<NEEDS:>>` you left.

---

## After the agent reports

1. Render: `cd pc_package && PATH="$PWD/../.venv/bin:$PATH" quarto render PCR-005_protein_a.PROBE.qmd --to pdf`.
2. `uv run python authoring/check_render.py pc_package/PCR-005_protein_a.PROBE.qmd --lax-style`
   — chunks execute, glyphs present. **Read only the correctness and glyph lines. Do not read the
   register table into the outcome, and do not tell the agent anything it says.**
3. `grep -c '<<NEEDS' pc_package/PCR-005_protein_a.PROBE.qmd` → 0 expected.
4. If a chunk the agent wrote fails on a code error, re-invoke the same agent once with the
   traceback and the words "fix the code, change no prose", then re-render. Record that it
   happened. If a hand-typed number is found, record it as a finding and leave the prose.
5. Sentence and word count via `check_style.sentences(check_style.prose_from_qmd(path))` — the
   count only, nothing else from that module.
6. `git status --short pc_package/` → only the untracked PROBE/EXCERPT files.
7. Outcome in `state.json`: model, render result, glyph result, `<<NEEDS>>` count, sentences,
   words. Nothing else. The reading comes next and it comes first.
