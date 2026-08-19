---
type: pm-task
epic: 2026-08-19_01_fourth-round-one-document
sprint: 2026-08-19_01_fourth-round-one-document
task: TASK-002
status: doing
kind: document
title: "Author PCR-007 in one pass under the rebuilt apparatus: one agent, the RUNNER's inputs, nothing else"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/doing]
about: ["PCR-007"]
---

> [!warning] Generated from `.claude/work/2026-08-19_01_fourth-round-one-document/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-002 — Author PCR-007 in one pass under the rebuilt apparatus: one agent, the RUNNER's inputs, nothing else

**Epic:** [[epic]] · **Status:** `doing` · **Waiting on:** the assistant · **Board:** [[_Board]]

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

## What was built

RUN 1 (2026-08-19, ~46 min, 118 tool uses, Opus 5): the agent produced a complete PCR-007 DRAFT — 47 pages, 416 sentences, 9,749 words, 37 chunks, 215 inline expressions, 0 <<NEEDS>>, no missing glyph, tic gate OK from the first check_render — and it FAILS the task's acceptance: the transcript (tool inputs, grepped) shows at command 72 `uv run python authoring/check_style.py --review pc_package/PCR-007_cex.DRAFT.qmd`, unprompted, after reading check_style.py's source (commands 20, 21, 31, 73), then a `shorts.txt` listing of every sentence with its word count (86–88), a `reflow.py` and nine `edits*.py` scripts (76–95), and a `final.txt` re-listing (99–103); its own report says the advisory rows were brought 'inside the human-source range after a revision pass' (', so ' 8.6 -> 0.2 %, ', and '+clause 16.0 -> 3.1 %, connective openings 0.2 -> 4.3 %). The author went and got the counters the regime withholds, and tuned to them. What it read otherwise was exactly the allowed set (brief, RUNNER, section_plan, STORY_BIBLE, WRITING_GUIDE, REGISTER_EXEMPLAR, and code: _pcpkg, doe_report, check_render, check_style, lint_numerals, config, amab_process, references.bib) and no .qmd but its own.

DISPOSITION: the run-1 draft is set aside as evidence (PCR-007_cex.DRAFT.run1-selfmeasured.qmd/.pdf and run1-self-measurement-commands.md in this unit) and NOT read by the owner, because a reading of a counter-tuned draft would not test the regime the plan names. The finding goes to the results page: an autonomous author with the reviewer's tool in reach will use it unasked. The one-sentence fix is in the RUNNER, which is the thing under test — step 3 now says the author runs check_render.py and nothing else on its draft, and step 4's review line says never the author, never in the authoring context. RUN 2 is launched with procedures/TASK-002.md UNCHANGED (the prompt sends the agent to RUNNER.md, which now says it).

## Documents it is about

- **PCR-007** — `pc_package/PCR-007_cex.qmd`

## Files it touched

- `pc_package/PCR-007_cex.DRAFT.qmd`
