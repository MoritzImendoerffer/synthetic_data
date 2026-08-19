---
type: pm-task
epic: 2026-08-19_01_fourth-round-one-document
sprint: 2026-08-19_01_fourth-round-one-document
task: TASK-001
status: done
kind: mechanism
title: "Fix the launch prompt, the blind key and the reading protocol before anything is written"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-007"]
---

> [!warning] Generated from `.claude/work/2026-08-19_01_fourth-round-one-document/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-001 — Fix the launch prompt, the blind key and the reading protocol before anything is written

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

This is the probe's TASK-002 for a whole document. The prompt is the experiment: it is the RUNNER's own invocation line and nothing more, because the RUNNER as rebuilt IS the regime under test. Do not add a rule; if RUNNER.md is found wanting, that is a finding for the results page, not a fix in the prompt. If the owner has overruled D5 by now, substitute the document everywhere and re-check §5c.

## Acceptance criteria

- [x] procedures/TASK-002.md holds the launch prompt VERBATIM: 'Author PCR-007 (Cation Exchange Chromatography, Step 7) per authoring/RUNNER.md, into pc_package/PCR-007_cex.DRAFT.qmd …', naming exactly the five inputs of RUNNER.md step 3 plus _pcpkg.py / doe_report.py for signatures, forbidding every pc_package/*.qmd and authoring/rhetorical/, and containing NO measure, NO grep list and NO checklist of moves — `grep -cE 'so |, and the|, which|passive|%|per 1k|per 100' procedures/TASK-002.md` reports only hits inside the RUNNER's own words if any, listed in the outcome
- [x] authoring/out/PCR-007.brief.md rebuilt fresh (`uv run python authoring/build_brief.py PCR-007`): `grep -c '## 2b'` -> 1 with 'reviewed by owner: 2026-08-19'; `grep -c '## 5d'` -> 0; `grep -c '## 5c'` -> 1 and it says no assignment for PCR-007
- [x] pc_package/PCR-007_cex.DRAFT.qmd instantiated from authoring/template.qmd (DOC=PCR-007, UO=cex, title from DOC_REGISTRY, template comment block deleted); `uv run python authoring/check_render.py pc_package/PCR-007_cex.DRAFT.qmd` executes the empty scaffold; untracked
- [x] blind-key.md exists with one line `new = A` or `new = B` from `python -c "import secrets; print(secrets.choice('AB'))"`, created before the agent is launched, not opened in the session until TASK-004's reading is recorded
- [x] procedures/READING.md states what the owner will be given (A.pdf, B.pdf, both whole documents), the suggested subset (Executive summary; Results §5.1–5.4; Design space; Discussion), the two questions (which sentences read as machine prose, with A or B; which reads as a paper), and the pass rule verbatim from decisions.pass_rule
- [x] the total words the agent will read is printed in the outcome (brief + WRITING_GUIDE + section_plan + STORY_BIBLE + REGISTER_EXEMPLAR; exploration §1 measured 21,403) and none of those files contains a counter (`grep -c 'per 1k\|per 100\|% of sentences' authoring/WRITING_GUIDE.md authoring/section_plan.yaml authoring/STORY_BIBLE.md authoring/out/PCR-007.brief.md` -> 0 each; REGISTER_EXEMPLAR.md is exempt where it quotes a source)

## What was built

procedures/TASK-002.md holds the launch prompt: RUNNER.md's invocation line, the DRAFT file, the six inputs (RUNNER, brief, section_plan, STORY_BIBLE, WRITING_GUIDE, REGISTER_EXEMPLAR) plus _pcpkg/doe_report for signatures, the ban on pc_package/*.qmd, authoring/rhetorical/ and authoring/history/, the <<NEEDS>> rule, the check_render loop and the report line. `grep -nE 'so |, and the|, which|passive|%|per 1k|per 100'` on it -> no hits at all. procedures/READING.md holds the owner's text, the suggested subset, the two questions and the pass rule verbatim.

Brief rebuilt fresh: authoring/out/PCR-007.brief.md — `## 2b` -> 1 with 'reviewed by owner: 2026-08-19'; `## 5d` -> 0; `## 5c` -> 1, 'None. No registered discrepancy is assigned to this document'. Counters in the author's inputs: `grep -c 'per 1k|per 100|% of sentences'` -> 0 for WRITING_GUIDE.md, section_plan.yaml, STORY_BIBLE.md, the brief. Total words the agent reads: 21,403 (brief + guide + plan + bible + exemplar).

pc_package/PCR-007_cex.DRAFT.qmd instantiated from authoring/template.qmd (DOC_REGISTRY: 'Process Characterization Report' / 'Cation Exchange Chromatography (Step 7)' / cex), template comment block removed, no placeholder token left; check_render on the empty scaffold: '2 python chunk(s), 0 inline expression(s) / OK all chunks exec'. Untracked.

blind-key.md: one line `new = A|B` from secrets.choice, written before the agent exists, not opened in the session. D5 not overruled by the owner at this point; PCR-007 stands.

## Documents it is about

- **PCR-007** — `pc_package/PCR-007_cex.qmd`

## Files it touched

- `.claude/work/2026-08-19_01_fourth-round-one-document/procedures/TASK-002.md`
- `.claude/work/2026-08-19_01_fourth-round-one-document/blind-key.md`
- `.claude/work/2026-08-19_01_fourth-round-one-document/procedures/READING.md`
- [[PCR-007.brief]] — `authoring/out/PCR-007.brief.md`
- `pc_package/PCR-007_cex.DRAFT.qmd`
