---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-001
status: done
kind: mechanism
title: "Fix the pilot's inputs before the agent exists: PCP-005 brief, scaffold, blind key, reading protocol"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-005"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-001 — Fix the pilot's inputs before the agent exists: PCP-005 brief, scaffold, blind key, reading protocol

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

The regime is frozen. Do not add a rule to the prompt.

## Acceptance criteria

- [x] `uv run python authoring/build_brief.py PCP-005`: `grep -c '## 2b'` -> 1 with 'reviewed by owner: 2026-08-19'; `## 5d` -> 0; §5c 'None'
- [x] pc_package/PCP-005_protein_a.DRAFT.qmd instantiated from the template (AUTHOR-A-DOCUMENT.md §1), check_render executes the empty scaffold; untracked
- [x] blind-key-PCP-005.md written by secrets.choice before the agent is launched and not opened in the session (not even indirectly: print no page counts)
- [x] the total words the agent reads printed (exploration §2: 21,415) and `grep -c 'per 1k|per 100|% of sentences'` -> 0 on WRITING_GUIDE.md, section_plan.yaml, STORY_BIBLE.md, the brief
- [x] procedures/AUTHOR-A-DOCUMENT.md and READING.md present (written at plan time) and unchanged

## What was built

Brief rebuilt fresh: `## 2b` 1 ('reviewed by owner: 2026-08-19'), `## 5d` 0, §5c 'None'. pc_package/PCP-005_protein_a.DRAFT.qmd instantiated from the template ('Process Characterization Plan' / 'Protein A Chromatography (Step 5)' / protein_a), template comment removed, check_render on the empty scaffold OK; untracked. blind-key-PCP-005.md: one line from secrets.choice, written before the agent exists, not opened, no page count printed. Counters in the author's inputs: 0 in WRITING_GUIDE.md, section_plan.yaml, STORY_BIBLE.md, the brief. Total words the agent reads: 21,415. procedures/AUTHOR-A-DOCUMENT.md and READING.md unchanged since the plan. Model override stays `opus` (the owner asked about it and made no change).

## Documents it is about

- **PCP-005** — `pc_package/PCP-005_protein_a.qmd`

## Files it touched

- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/blind-key-PCP-005.md`
- [[PCP-005.brief]] — `authoring/out/PCP-005.brief.md`
- `pc_package/PCP-005_protein_a.DRAFT.qmd`
