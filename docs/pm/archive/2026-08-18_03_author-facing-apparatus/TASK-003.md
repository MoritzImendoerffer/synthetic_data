---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-003
status: done
kind: document
title: "Author the probe: two subsections, one agent, one pass, minimal regime, no counters"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-005"]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-003 — Author the probe: two subsections, one agent, one pass, minimal regime, no counters

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

This is the experiment. If the render fails on a code error in a chunk the agent wrote, fix the CODE in the same agent's context (one re-invocation, code only, no comment on the prose) and record that it happened. If it fails on prose (a broken inline expression the agent wrote to hit a number it had no helper for), the agent should have written <<NEEDS>>; treat a hand-typed number as a finding, record it, and leave the sentence — do not edit prose. Never show the agent a count. Never open the shipped PCR-005 in the same context that talks to the agent.

## Acceptance criteria

- [x] one agent, model claude-opus-5, launched with procedures/TASK-003.md VERBATIM as its prompt and no other instruction; the agent's report names its model and it is claude-opus-5
- [x] the agent read only: probe-guide.md, PCR-005.brief.probe.md, authoring/STORY_BIBLE.md, probe-setup.py, and pc_package/_pcpkg.py / pc_package/doe_report.py for signatures — the transcript shows no Read of any pc_package/*.qmd, authoring/WRITING_GUIDE.md, authoring/section_plan.yaml, authoring/REGISTER_EXEMPLAR.md, authoring/check_style.py or authoring/rhetorical/
- [x] the agent ran no check_render.py and no check_style.py; the session did not print any measure back to it; the agent wrote once and stopped
- [x] `cd pc_package && PATH="$PWD/../.venv/bin:$PATH" quarto render PCR-005_protein_a.PROBE.qmd --to pdf` succeeds; `uv run python authoring/check_render.py pc_package/PCR-005_protein_a.PROBE.qmd --lax-style` executes every chunk and reports no missing glyph on the fresh pdf; `grep -c '<<NEEDS' ` → 0; the typed-number grep from AUTHOR-A-DOCUMENT.md §4 (`grep -nE "\b[0-9]+(\.[0-9]+)?\s?(%|°C|mmHg|g/L|L\b|mM|h\b|days?)"`) hits only inside inline expressions or statistical conventions
- [x] the two subsections carry the same headings as the excerpt and the body has at least 40 sentences (check_style.sentences on prose_from_qmd; MIN_SENTENCES=40, so the gate will evaluate it in TASK-005) — if under 40, the agent is NOT re-invoked; record the count and continue, the reading is still valid
- [x] the outcome records ONLY: model, render result, glyph result, <<NEEDS>> count, sentence count, word count — no style row, no discourse row, no `, which` count
- [x] `git status --short pc_package/` still shows only the untracked PROBE/EXCERPT files

**Depends on:** [[TASK-002]]

## What was built

One agent, fresh context (general-purpose subagent, model override `opus`), given procedures/TASK-003.md's prompt verbatim with $U substituted and nothing else. Its report names its model: Claude Opus 5 (`claude-opus-5[1m]`).

Transcript audited by grep only (the JSONL is not read into the session): Read tool file_path values are exactly probe-guide.md, PCR-005.brief.probe.md, authoring/STORY_BIBLE.md, probe-setup.py — one read each. Bash: `cat -n` of the PROBE.qmd it was writing into, `grep -n "^def …" doe_report.py`, `grep -n "def pct|def show" _pcpkg.py`, `sed -n` ranges of doe_report.py, and five python heredocs in the scratchpad that evaluated its own inline expressions against the SETUP globals and spliced its two sections into the file. Zero occurrences of WRITING_GUIDE, section_plan, REGISTER_EXEMPLAR, check_style, check_render, rhetorical/ or PCR-005_protein_a.qmd in any tool input. No check_render.py, no check_style.py; the session printed nothing back to it. It wrote once and stopped (21 tool uses, ~10 min).

Render: `quarto render PCR-005_protein_a.PROBE.qmd --to pdf` → Output created (204,509 bytes, 10 pages; the EXCERPT is 8 pages). check_render --lax-style: '10 python chunk(s), 72 inline expression(s) / OK all chunks exec, all inline expressions eval, no <<NEEDS:>> markers'; 'PROBE.pdf: no missing glyphs'. `grep -c '<<NEEDS'` → 0. Typed-measurement grep outside inline expressions → nothing. PDF metadata title identical in both files ('Process Characterization Report'), no source filename in it.

ONE CODE-ONLY FIX AFTER THE AGENT REPORTED, in both scaffolds and in probe-setup.py, recorded here: probe-setup.py had been extracted as lines 38–257 of the shipped file and line 257 is the chunk's closing fence, so both scaffolds carried an empty ``` ``` block after SETUP. Quarto rendered it silently, but check_render's fence parser desynchronised and reported '1 chunk, 0 inline expressions' — its dry-eval had covered nothing. Removed the one stray fence line (line 261) from PROBE.qmd and EXCERPT.qmd and the trailing fence from probe-setup.py; no prose line touched, excerpt re-verified verbatim (Python `in` check True); both files re-dry-evaluated (PROBE 10 chunks / 72 inline, EXCERPT 10 / 41, all OK) and both PDFs re-rendered and re-glyph-checked OK. The agent was not re-invoked.

Sentences and words via check_style.sentences(check_style.prose_from_qmd(path)) — the count only: PROBE 90 sentences, 1,829 words (the EXCERPT, same method: 59 / 1,333). Above MIN_SENTENCES, so TASK-005's gate run will evaluate it.

Recorded here on purpose and nowhere else: no style row, no discourse row, no frame count. The reading comes first.

`git status --short pc_package/` → only the untracked PROBE.qmd/.pdf and EXCERPT.qmd/.pdf.

## Documents it is about

- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`

## Files it touched

- `pc_package/PCR-005_protein_a.PROBE.qmd`
