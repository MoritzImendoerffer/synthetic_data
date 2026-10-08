---
type: pm-task
epic: 2026-10-08_01_rev2-campaign
sprint: 2026-10-08_01_rev2-campaign
task: TASK-009
status: done
kind: mechanism
title: "Authoring artifacts per the owner's rule decisions; brief carries the new facts and table menu"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCMP-001"]
---

> [!warning] Generated from `.claude/work/2026-10-08_01_rev2-campaign/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-009 — Authoring artifacts per the owner's rule decisions; brief carries the new facts and table menu

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Acceptance criteria

- [x] WRITING_GUIDE: mechanism confined to interpretation/Discussion; report conventions section; selftest of check_style still passes
- [x] RUNNER: paired plan and PCMP-001 readable for content
- [x] section_plan.yaml has an investigation_report doc type and Revision history in every type
- [x] STORY_BIBLE has the chronology, the method decision and the INV-001 storyline
- [x] build_brief.py PCR-005 prints IAC, method plan, hold data and the ctable menu; D-001/D-002 still in §5c where they apply

**Depends on:** [[TASK-006]], [[TASK-007]], [[TASK-008]]

## What was built

section_plan.yaml: revision_history in 6 front_matter lists, 'Changes in this revision' (report intro + 4 purpose_scope), IAC basis in PAR/plan/master-plan sections, complex tables named, investigation_report type. WRITING_GUIDE: rule 1 (controlled report, not paper), rule 4 scoped, colon row corrected, paired plan for content, §6 complex tables, §7 report conventions; check_style --selftest 4/4. REVIEW_CHECKLIST: Version 2.0 block (4 questions), Q1 scoped. RUNNER: rendered paired plan + PCMP-001 readable for content. STORY_BIBLE §9b + 8 grounding rows + INV-001 in ID table. DISCREPANCIES: D-001 survives (INV scope), NOR-anchoring fix recorded. build_brief §4c (chronology, method plan, IAC, Rev1 criteria, par_table_rev1, verification, hold, comparability, table calls) + pending-owner-review flag. template: date, _tables.tex, import tables, revision history. CLAUDE.md updated. doe_report: decision_statistic (viral = mean LRF), NOR PAR anchored at set-point, par_table_rev1, fragment PARs, two-sided criterion text.

## Documents it is about

- **PCMP-001** — `pc_package/PCMP-001_master_plan.qmd`

## Files it touched

- `CLAUDE.md`
- [[WRITING_GUIDE]] — `authoring/WRITING_GUIDE.md`
- [[REVIEW_CHECKLIST]] — `authoring/REVIEW_CHECKLIST.md`
- [[RUNNER]] — `authoring/RUNNER.md`
- `authoring/section_plan.yaml`
- [[STORY_BIBLE]] — `authoring/STORY_BIBLE.md`
- [[DISCREPANCIES]] — `authoring/DISCREPANCIES.md`
- `authoring/build_brief.py`
- `authoring/template.qmd`
