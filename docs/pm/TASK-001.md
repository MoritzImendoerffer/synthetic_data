---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-001
status: todo
kind: mechanism
title: "Fix the pilot's inputs before the agent exists: PCP-005 brief, scaffold, blind key, reading protocol"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCP-005"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-001 — Fix the pilot's inputs before the agent exists: PCP-005 brief, scaffold, blind key, reading protocol

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

The regime is frozen. Do not add a rule to the prompt.

## Acceptance criteria

- [ ] `uv run python authoring/build_brief.py PCP-005`: `grep -c '## 2b'` -> 1 with 'reviewed by owner: 2026-08-19'; `## 5d` -> 0; §5c 'None'
- [ ] pc_package/PCP-005_protein_a.DRAFT.qmd instantiated from the template (AUTHOR-A-DOCUMENT.md §1), check_render executes the empty scaffold; untracked
- [ ] blind-key-PCP-005.md written by secrets.choice before the agent is launched and not opened in the session (not even indirectly: print no page counts)
- [ ] the total words the agent reads printed (exploration §2: 21,415) and `grep -c 'per 1k|per 100|% of sentences'` -> 0 on WRITING_GUIDE.md, section_plan.yaml, STORY_BIBLE.md, the brief
- [ ] procedures/AUTHOR-A-DOCUMENT.md and READING.md present (written at plan time) and unchanged

## Documents it is about

- **PCP-005** — `pc_package/PCP-005_protein_a.qmd`

## Files it touched

- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/blind-key-PCP-005.md`
- [[PCP-005.brief]] — `authoring/out/PCP-005.brief.md`
- `pc_package/PCP-005_protein_a.DRAFT.qmd`
