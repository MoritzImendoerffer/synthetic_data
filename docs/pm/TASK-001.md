---
type: pm-task
epic: 2026-08-19_01_fourth-round-one-document
sprint: 2026-08-19_01_fourth-round-one-document
task: TASK-001
status: todo
kind: mechanism
title: "Fix the launch prompt, the blind key and the reading protocol before anything is written"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-007"]
---

> [!warning] Generated from `.claude/work/2026-08-19_01_fourth-round-one-document/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-001 — Fix the launch prompt, the blind key and the reading protocol before anything is written

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

This is the probe's TASK-002 for a whole document. The prompt is the experiment: it is the RUNNER's own invocation line and nothing more, because the RUNNER as rebuilt IS the regime under test. Do not add a rule; if RUNNER.md is found wanting, that is a finding for the results page, not a fix in the prompt. If the owner has overruled D5 by now, substitute the document everywhere and re-check §5c.

## Acceptance criteria

- [ ] procedures/TASK-002.md holds the launch prompt VERBATIM: 'Author PCR-007 (Cation Exchange Chromatography, Step 7) per authoring/RUNNER.md, into pc_package/PCR-007_cex.DRAFT.qmd …', naming exactly the five inputs of RUNNER.md step 3 plus _pcpkg.py / doe_report.py for signatures, forbidding every pc_package/*.qmd and authoring/rhetorical/, and containing NO measure, NO grep list and NO checklist of moves — `grep -cE 'so |, and the|, which|passive|%|per 1k|per 100' procedures/TASK-002.md` reports only hits inside the RUNNER's own words if any, listed in the outcome
- [ ] authoring/out/PCR-007.brief.md rebuilt fresh (`uv run python authoring/build_brief.py PCR-007`): `grep -c '## 2b'` -> 1 with 'reviewed by owner: 2026-08-19'; `grep -c '## 5d'` -> 0; `grep -c '## 5c'` -> 1 and it says no assignment for PCR-007
- [ ] pc_package/PCR-007_cex.DRAFT.qmd instantiated from authoring/template.qmd (DOC=PCR-007, UO=cex, title from DOC_REGISTRY, template comment block deleted); `uv run python authoring/check_render.py pc_package/PCR-007_cex.DRAFT.qmd` executes the empty scaffold; untracked
- [ ] blind-key.md exists with one line `new = A` or `new = B` from `python -c "import secrets; print(secrets.choice('AB'))"`, created before the agent is launched, not opened in the session until TASK-004's reading is recorded
- [ ] procedures/READING.md states what the owner will be given (A.pdf, B.pdf, both whole documents), the suggested subset (Executive summary; Results §5.1–5.4; Design space; Discussion), the two questions (which sentences read as machine prose, with A or B; which reads as a paper), and the pass rule verbatim from decisions.pass_rule
- [ ] the total words the agent will read is printed in the outcome (brief + WRITING_GUIDE + section_plan + STORY_BIBLE + REGISTER_EXEMPLAR; exploration §1 measured 21,403) and none of those files contains a counter (`grep -c 'per 1k\|per 100\|% of sentences' authoring/WRITING_GUIDE.md authoring/section_plan.yaml authoring/STORY_BIBLE.md authoring/out/PCR-007.brief.md` -> 0 each; REGISTER_EXEMPLAR.md is exempt where it quotes a source)

## Documents it is about

- **PCR-007** — `pc_package/PCR-007_cex.qmd`

## Files it touched

- `.claude/work/2026-08-19_01_fourth-round-one-document/procedures/TASK-002.md`
- `.claude/work/2026-08-19_01_fourth-round-one-document/blind-key.md`
- `.claude/work/2026-08-19_01_fourth-round-one-document/procedures/READING.md`
- [[PCR-007.brief]] — `authoring/out/PCR-007.brief.md`
- `pc_package/PCR-007_cex.DRAFT.qmd`
