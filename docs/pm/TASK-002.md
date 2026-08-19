---
type: pm-task
epic: 2026-08-19_01_fourth-round-one-document
sprint: 2026-08-19_01_fourth-round-one-document
task: TASK-002
status: todo
kind: document
title: "Author PCR-007 in one pass under the rebuilt apparatus: one agent, the RUNNER's inputs, nothing else"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-007"]
---

> [!warning] Generated from `.claude/work/2026-08-19_01_fourth-round-one-document/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-002 — Author PCR-007 in one pass under the rebuilt apparatus: one agent, the RUNNER's inputs, nothing else

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

The whole-document arc is the thing the probe could not test: an executive summary that matches the conclusions, cross-references that resolve, a SETUP chunk the agent derives from the helper inventory. If the agent writes <<NEEDS>> for a value that has no helper, that is real: extend _pcpkg.py/doe_report.py (a helper task, `make test` must stay 95+), rebuild the brief, and re-invoke the SAME agent with the new helper's name — never a fresh agent mid-document, never a typed number. Never open the shipped PCR-007 in the session that talks to the agent. Expect one to three check_render passes; record the number, it is data.

## Acceptance criteria

- [ ] one agent, model claude-opus-5 (its report names it), fresh context, launched with procedures/TASK-002.md verbatim; the transcript (audited by grep of tool inputs, not read) shows Reads of exactly authoring/out/PCR-007.brief.md, authoring/section_plan.yaml, authoring/STORY_BIBLE.md, authoring/WRITING_GUIDE.md, authoring/REGISTER_EXEMPLAR.md, authoring/RUNNER.md, and code under pc_package/*.py — and zero occurrences of any pc_package/*.qmd, authoring/rhetorical/, authoring/history/, check_style.py --review, or measure_ in any tool input
- [ ] the agent ran check_render.py as the RUNNER says (correctness + tic gate) and fixed its own code errors and tic failures in the same context; the session printed no measure back to it and no line of its check_render output beyond what the tool prints (which, since 2026-08-19, is the five gated rows and pass/fail)
- [ ] `uv run python authoring/check_render.py pc_package/PCR-007_cex.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, docx renders, tic gate OK; `cd pc_package && PATH="$PWD/../.venv/bin:$PATH" quarto render PCR-007_cex.DRAFT.qmd --to pdf` succeeds and check_render on the fresh pdf reports no missing glyph
- [ ] `grep -c '<<NEEDS' pc_package/PCR-007_cex.DRAFT.qmd` -> 0; the typed-measurement grep (`grep -nE "\b[0-9]+(\.[0-9]+)?\s?(%|°C|mmHg|g/L|L\b|mM|h\b|cm/hr|CV\b|mS/cm|days?)"`) hits only inside inline expressions, table code or statistical conventions — every hit listed in the outcome
- [ ] every section of section_plan.yaml report_doe is present in order (`grep -n '^# \|^## '` against the plan's headings), including Results §5.4 Mechanistic interpretation, Design space, PARs, Deviations (PCR-007 has seeded deviations — brief §5) and Appendices A–D
- [ ] the outcome records ONLY: model, render result, glyph result, <<NEEDS>> count, sentence count, word count, page count, and how many check_render passes the agent needed — no style row, no frame count, no discourse row
- [ ] `git status --short pc_package/` shows only the untracked DRAFT and its renders; the shipped PCR-007_cex.qmd/.docx/.pdf are untouched

**Depends on:** [[TASK-001]]

## Documents it is about

- **PCR-007** — `pc_package/PCR-007_cex.qmd`

## Files it touched

- `pc_package/PCR-007_cex.DRAFT.qmd`
