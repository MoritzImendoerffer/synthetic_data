---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-007
status: todo
kind: mechanism
title: "Take scaffold, register and rigor off the author-facing section plan and put them in a reviewer's checklist"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-007 — Take scaffold, register and rigor off the author-facing section plan and put them in a reviewer's checklist

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

Runs only on D4 = PASS. The section ORDER and headings are the CLAUDE.md canonical order and do not change. The `pull:` menus stay; they are helper names, not rhetoric. Do not delete the taxonomy from RHETORICAL_ANNEX.md — the annex layer keeps its roles; only their second life as commands ends. The 26-span audit itself is docs/next/rhetorical-layer-coverage.md's and is not done here.

## Acceptance criteria

- [ ] `grep -c 'rigor:\|scaffold:\|register:' authoring/section_plan.yaml` → 0 and the `scaffolds`, `registers`, `rigor_glossary` blocks are gone from `meta`; each section keeps `id`, `heading`, `subsections`, `pull`, `length_band` and ONE plain sentence of what it covers; `python -c "import yaml; yaml.safe_load(open('authoring/section_plan.yaml'))"` loads
- [ ] authoring/REVIEW_CHECKLIST.md exists and rephrases each former rigor obligation as a question a reviewer asks of a finished section (e.g. bounded_conclusion → 'Does the design-space claim say which ranges it covers and what the model does not cover?'), one per line, with the section it applies to; `grep -c 'SCQA\|CCC\|OCAR\|GopenSwan' authoring/REVIEW_CHECKLIST.md authoring/section_plan.yaml` → 0
- [ ] authoring/RHETORICAL_ANNEX.md: the sentence 'the roles below are the concrete text-span realizations of the scaffolds (SCQA/CCC) and rigor obligations that section_plan.yaml assigns each section' is replaced by the rule that roles are annotated on finished text and are never authoring instructions, and the `mechanistic_warrant` row gains: must name a physical cause; a category label ('capacity of the bed', 'resin property', 'physical chemistry of') is not a warrant
- [ ] authoring/RUNNER.md step 3 lists the author's inputs as: the brief, section_plan.yaml (structure only), STORY_BIBLE.md, the guide (TASK-008), REGISTER_EXEMPLAR.md — and step 4 gains a 'review' line pointing at REVIEW_CHECKLIST.md
- [ ] `grep -rn 'SCQA\|CCC\|rigor_glossary\|bounded_conclusion\|table_narration' authoring/ docs/ CLAUDE.md pc_package/TASKS.md pc_package/README.md` — every remaining hit is in docs/results/, authoring/history/ or a decisions note, i.e. a record and not an instruction; list them in the outcome
- [ ] `for d in $(uv run python -c 'from pc_package._pcpkg import DOC_REGISTRY; print(" ".join(DOC_REGISTRY))'); do uv run --extra discourse python authoring/build_brief.py $d; done` runs for all 20 (build_brief names the plan file but parses no keys — exploration §3)

**Depends on:** [[TASK-004]]

## Files it touched

- `authoring/section_plan.yaml`
- [[REVIEW_CHECKLIST]] — `authoring/REVIEW_CHECKLIST.md`
- [[RHETORICAL_ANNEX]] — `authoring/RHETORICAL_ANNEX.md`
- [[RUNNER]] — `authoring/RUNNER.md`
