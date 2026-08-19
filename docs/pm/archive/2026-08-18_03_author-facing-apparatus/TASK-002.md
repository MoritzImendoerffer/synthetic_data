---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-002
status: done
kind: mechanism
title: "Build the probe scaffold: the setup code, the ten-line guide, the stripped brief, the excerpt, and the blind key"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-005"]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-002 — Build the probe scaffold: the setup code, the ten-line guide, the stripped brief, the excerpt, and the blind key

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

The guide is the only new prose in the regime and its wording is the experiment's variable, so write it positively and stop: it says what to do, never what the corpus did wrong. Do not paste any sentence from WRITING_GUIDE.md into it. The EXCERPT is not authoring — it is a verbatim copy of shipped text under an identical scaffold so that A.pdf and B.pdf differ only in the prose. If the shipped SETUP chunk needs a helper the two subsections do not use, keep it anyway: the point is that both files compute the same numbers. §5c is removed from the brief copy only because PCR-005 carries no registered discrepancy (exploration §2), so the section is empty for it; say so in the outcome.

## Acceptance criteria

- [x] probe-setup.py holds lines 52–260 of pc_package/PCR-005_protein_a.qmd as code only: every comment line reduced to the helper or scalar names it introduces, no sentence of prose; `grep -c '^#' probe-setup.py` is reported and each remaining comment is a bare label
- [x] PCR-005_protein_a.PROBE.qmd is authoring/template.qmd instantiated (DOC=PCR-005, UO=protein_a, title from DOC_REGISTRY, template comment block deleted) whose SETUP chunk is probe-setup.py verbatim, whose body is exactly two placeholder headings `## Response-surface models` and `## Mechanistic interpretation` under `# Results`, and no Approvals/Abbreviations/References sections; `uv run python authoring/check_render.py pc_package/PCR-005_protein_a.PROBE.qmd --lax-style` executes every chunk with no error
- [x] PCR-005_protein_a.EXCERPT.qmd is the same scaffold with lines 747–876 of the shipped PCR-005 pasted verbatim as the body; `cd pc_package && PATH="$PWD/../.venv/bin:$PATH" quarto render PCR-005_protein_a.EXCERPT.qmd --to pdf` succeeds and check_render reports no missing glyph on that pdf; `diff <(sed -n 747,876p PCR-005_protein_a.qmd) <(body of EXCERPT)` is empty
- [x] probe-guide.md is at most 12 lines and 250 words (`wc -l`, `wc -w`); it contains, in this order: who the reader is (an assessor reading a BLA); the role sentence 'You are the process scientist who ran this study. Explain the response surfaces and what they mean physically, as you would in a paper.'; numbers only as inline `{python}` expressions from probe-setup.py and the brief's §7, `<<NEEDS: …>>` if none fits; the four hard tics (no em-dash, no semicolon splice, no bold in a sentence, no coined hyphenated compound); one sentence of context (this follows a subsection on screening effects and Table 5.8 already reported the coefficients); it contains NO percentage, NO sentence-length number, NO ✗ example, NO list of phrases to search for, and NO reference to WRITING_GUIDE.md, section_plan.yaml, REGISTER_EXEMPLAR.md or check_style.py (`grep -c` for each of those names → 0)
- [x] PCR-005.brief.probe.md is authoring/out/PCR-005.brief.md with §5c and §5d removed and nothing else changed (`grep -c '## 5d\|## 5c' ` → 0; §1–§4b, §5, §6, §7 present); `wc -w` printed
- [x] blind-key.md exists, contains one line `probe = A` or `probe = B` chosen by `python -c "import secrets; print(secrets.choice('AB'))"`, and is created in this task, before any authoring
- [x] the total words the probe agent will read — probe-guide.md + PCR-005.brief.probe.md + authoring/STORY_BIBLE.md + probe-setup.py — is printed in the outcome (expected under 6,000 against the pilot's 29,454)
- [x] `git status --short pc_package/` shows only the two untracked files and their renders; nothing tracked changed

## What was built

Built by build_probe_scaffold.py (saved in the unit, re-runnable), not by hand.

probe-setup.py: the shipped SETUP chunk body (PCR-005_protein_a.qmd lines 38–257 — the plan said 52–260 from the first comment; the chunk itself opens at 36 and its body is 38–257) plus a three-line header. 223 lines, 886 words, 13 comment lines: the header and ten bare section labels ('# acceptance criteria', '# the nominal train'…), one trailing '# noqa'. No sentence of prose.

PCR-005_protein_a.PROBE.qmd: authoring/template.qmd instantiated (DOC_REGISTRY gives 'Process Characterization Report' / 'Protein A Chromatography (Step 5)'), template comment block removed, SETUP = probe-setup.py verbatim, body = `# Results` + `## Response-surface models` + `## Mechanistic interpretation` each over an HTML placeholder comment, no Approvals/Abbreviations/References. `check_render.py --lax-style`: 'OK all chunks exec, all inline expressions eval, no <<NEEDS:>> markers'; the numeral lint (advisory) flags the two `top=6` code lines in the appendix, as it does in the shipped file.

PCR-005_protein_a.EXCERPT.qmd: same scaffold, body = shipped lines 747–876 verbatim (Python `in` check: True, 130 lines). Rendered to PDF (157,604 bytes); check_render: 'no missing glyphs'.

ONE ADDITION TO BOTH SCAFFOLDS, recorded: an unnumbered appendix after the body carrying the two screening-effect tables (@tbl-eff-hcp, @tbl-eff-yield) as code chunks copied from the shipped file. The shipped excerpt cross-references both and they live in the subsection before it; without them Quarto prints '?@tbl-eff-hcp' in the excerpt and marks it. The probe carries the identical appendix so the two PDFs stay parallel; the guide's context line tells the agent the two labels exist.

probe-guide.md: 10 lines, 240 words. In order: the reader; the role sentence verbatim; finding-then-evidence; the numbers rule (inline expressions from probe-setup.py / brief §7, <<NEEDS>>); name the physical cause; terms of art; the four tics; one context sentence. grep for WRITING_GUIDE / section_plan / REGISTER_EXEMPLAR / check_style / '%' / '✗' → 0 each. BEYOND THE PLAN'S LIST and recorded so it can be struck before TASK-003: rules 3 (finding then evidence), 5 (name the physical cause: which species, which interaction, which property, which direction) and 6 (terms of art). All three are positive and none supplies content; rule 5 asks for mechanism the way section_plan.yaml already did, so it does not confound the hypothesis that the regime, not the request, produced the hollow warrants. Overrulable.

PCR-005.brief.probe.md: build_brief.py PCR-005 (fresh, --extra discourse) with §5c and §5d removed as one span (4,060 chars); §1–§4b, §5, §6, §7 present; 2,581 words against 3,362. §5c was empty for PCR-005 in effect (no registered discrepancy — exploration §2).

blind-key.md: one line, drawn with secrets.choice('AB'), created before any authoring; not opened in this conversation.

Total words the agent will read: probe-guide.md + PCR-005.brief.probe.md + STORY_BIBLE.md + probe-setup.py = 5,746, against the pilot's 29,454.

`git status --short pc_package/` → only the untracked PROBE.qmd, EXCERPT.qmd and EXCERPT.pdf.

## Documents it is about

- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`

## Files it touched

- `pc_package/PCR-005_protein_a.PROBE.qmd`
- `pc_package/PCR-005_protein_a.EXCERPT.qmd`
- `.claude/work/2026-08-18_03_author-facing-apparatus/probe-setup.py`
- `.claude/work/2026-08-18_03_author-facing-apparatus/probe-guide.md`
- `.claude/work/2026-08-18_03_author-facing-apparatus/PCR-005.brief.probe.md`
- `.claude/work/2026-08-18_03_author-facing-apparatus/blind-key.md`
- `.claude/work/2026-08-18_03_author-facing-apparatus/build_probe_scaffold.py`
