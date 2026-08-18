---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-003
status: todo
kind: document
title: "Author the probe: two subsections, one agent, one pass, minimal regime, no counters"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-005"]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-003 — Author the probe: two subsections, one agent, one pass, minimal regime, no counters

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

This is the experiment. If the render fails on a code error in a chunk the agent wrote, fix the CODE in the same agent's context (one re-invocation, code only, no comment on the prose) and record that it happened. If it fails on prose (a broken inline expression the agent wrote to hit a number it had no helper for), the agent should have written <<NEEDS>>; treat a hand-typed number as a finding, record it, and leave the sentence — do not edit prose. Never show the agent a count. Never open the shipped PCR-005 in the same context that talks to the agent.

## Acceptance criteria

- [ ] one agent, model claude-opus-5, launched with procedures/TASK-003.md VERBATIM as its prompt and no other instruction; the agent's report names its model and it is claude-opus-5
- [ ] the agent read only: probe-guide.md, PCR-005.brief.probe.md, authoring/STORY_BIBLE.md, probe-setup.py, and pc_package/_pcpkg.py / pc_package/doe_report.py for signatures — the transcript shows no Read of any pc_package/*.qmd, authoring/WRITING_GUIDE.md, authoring/section_plan.yaml, authoring/REGISTER_EXEMPLAR.md, authoring/check_style.py or authoring/rhetorical/
- [ ] the agent ran no check_render.py and no check_style.py; the session did not print any measure back to it; the agent wrote once and stopped
- [ ] `cd pc_package && PATH="$PWD/../.venv/bin:$PATH" quarto render PCR-005_protein_a.PROBE.qmd --to pdf` succeeds; `uv run python authoring/check_render.py pc_package/PCR-005_protein_a.PROBE.qmd --lax-style` executes every chunk and reports no missing glyph on the fresh pdf; `grep -c '<<NEEDS' ` → 0; the typed-number grep from AUTHOR-A-DOCUMENT.md §4 (`grep -nE "\b[0-9]+(\.[0-9]+)?\s?(%|°C|mmHg|g/L|L\b|mM|h\b|days?)"`) hits only inside inline expressions or statistical conventions
- [ ] the two subsections carry the same headings as the excerpt and the body has at least 40 sentences (check_style.sentences on prose_from_qmd; MIN_SENTENCES=40, so the gate will evaluate it in TASK-005) — if under 40, the agent is NOT re-invoked; record the count and continue, the reading is still valid
- [ ] the outcome records ONLY: model, render result, glyph result, <<NEEDS>> count, sentence count, word count — no style row, no discourse row, no `, which` count
- [ ] `git status --short pc_package/` still shows only the untracked PROBE/EXCERPT files

**Depends on:** [[TASK-002]]

## Documents it is about

- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`

## Files it touched

- `pc_package/PCR-005_protein_a.PROBE.qmd`
