---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-002
status: todo
kind: mechanism
title: "Build the probe scaffold: the setup code, the ten-line guide, the stripped brief, the excerpt, and the blind key"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-005"]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-002 — Build the probe scaffold: the setup code, the ten-line guide, the stripped brief, the excerpt, and the blind key

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

The guide is the only new prose in the regime and its wording is the experiment's variable, so write it positively and stop: it says what to do, never what the corpus did wrong. Do not paste any sentence from WRITING_GUIDE.md into it. The EXCERPT is not authoring — it is a verbatim copy of shipped text under an identical scaffold so that A.pdf and B.pdf differ only in the prose. If the shipped SETUP chunk needs a helper the two subsections do not use, keep it anyway: the point is that both files compute the same numbers. §5c is removed from the brief copy only because PCR-005 carries no registered discrepancy (exploration §2), so the section is empty for it; say so in the outcome.

## Acceptance criteria

- [ ] probe-setup.py holds lines 52–260 of pc_package/PCR-005_protein_a.qmd as code only: every comment line reduced to the helper or scalar names it introduces, no sentence of prose; `grep -c '^#' probe-setup.py` is reported and each remaining comment is a bare label
- [ ] PCR-005_protein_a.PROBE.qmd is authoring/template.qmd instantiated (DOC=PCR-005, UO=protein_a, title from DOC_REGISTRY, template comment block deleted) whose SETUP chunk is probe-setup.py verbatim, whose body is exactly two placeholder headings `## Response-surface models` and `## Mechanistic interpretation` under `# Results`, and no Approvals/Abbreviations/References sections; `uv run python authoring/check_render.py pc_package/PCR-005_protein_a.PROBE.qmd --lax-style` executes every chunk with no error
- [ ] PCR-005_protein_a.EXCERPT.qmd is the same scaffold with lines 747–876 of the shipped PCR-005 pasted verbatim as the body; `cd pc_package && PATH="$PWD/../.venv/bin:$PATH" quarto render PCR-005_protein_a.EXCERPT.qmd --to pdf` succeeds and check_render reports no missing glyph on that pdf; `diff <(sed -n 747,876p PCR-005_protein_a.qmd) <(body of EXCERPT)` is empty
- [ ] probe-guide.md is at most 12 lines and 250 words (`wc -l`, `wc -w`); it contains, in this order: who the reader is (an assessor reading a BLA); the role sentence 'You are the process scientist who ran this study. Explain the response surfaces and what they mean physically, as you would in a paper.'; numbers only as inline `{python}` expressions from probe-setup.py and the brief's §7, `<<NEEDS: …>>` if none fits; the four hard tics (no em-dash, no semicolon splice, no bold in a sentence, no coined hyphenated compound); one sentence of context (this follows a subsection on screening effects and Table 5.8 already reported the coefficients); it contains NO percentage, NO sentence-length number, NO ✗ example, NO list of phrases to search for, and NO reference to WRITING_GUIDE.md, section_plan.yaml, REGISTER_EXEMPLAR.md or check_style.py (`grep -c` for each of those names → 0)
- [ ] PCR-005.brief.probe.md is authoring/out/PCR-005.brief.md with §5c and §5d removed and nothing else changed (`grep -c '## 5d\|## 5c' ` → 0; §1–§4b, §5, §6, §7 present); `wc -w` printed
- [ ] blind-key.md exists, contains one line `probe = A` or `probe = B` chosen by `python -c "import secrets; print(secrets.choice('AB'))"`, and is created in this task, before any authoring
- [ ] the total words the probe agent will read — probe-guide.md + PCR-005.brief.probe.md + authoring/STORY_BIBLE.md + probe-setup.py — is printed in the outcome (expected under 6,000 against the pilot's 29,454)
- [ ] `git status --short pc_package/` shows only the two untracked files and their renders; nothing tracked changed

## Documents it is about

- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`

## Files it touched

- `pc_package/PCR-005_protein_a.PROBE.qmd`
- `pc_package/PCR-005_protein_a.EXCERPT.qmd`
- `.claude/work/2026-08-18_03_author-facing-apparatus/probe-setup.py`
- `.claude/work/2026-08-18_03_author-facing-apparatus/probe-guide.md`
- `.claude/work/2026-08-18_03_author-facing-apparatus/PCR-005.brief.probe.md`
- `.claude/work/2026-08-18_03_author-facing-apparatus/blind-key.md`
