---
type: pm-task
epic: 2026-10-08_01_rev2-campaign
sprint: 2026-10-08_01_rev2-campaign
task: TASK-008
status: done
kind: mechanism
title: "Registry: INV-001, revision metadata, revision_history(), superseded references, Makefile, schema_ext"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
---

> [!warning] Generated from `.claude/work/2026-10-08_01_rev2-campaign/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-008 — Registry: INV-001, revision metadata, revision_history(), superseded references, Makefile, schema_ext

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Acceptance criteria

- [x] DOC_REGISTRY has INV-001; title_block shows Version 2.0 and the Rev 2.0 effective date
- [x] revision_history(DOC) renders Rev 1.0 / Rev 2.0 rows from config
- [x] make corpus loop includes INV-*

**Depends on:** [[TASK-001]]

## What was built

INV-001 in DOC_REGISTRY (QA-owned, v1.0, 2026-09-18); doc_version(); title_block shows Version 2.0 / 2026-09-30 / Supersedes; revision_history(); INV-001 in related_docs_md; SOP-3015/AMV-3020 nrCE-SDS; Makefile corpus loop includes INV-*; schema_ext: investigation_report type, RevisionEntry, AcceptanceCriterionRecord, supersedes/revision_history/acceptance_criteria on the annex; build_ground_truth BUILDERS + REV2_READY keeps Rev 1.0 annexes until each document is re-authored: 20/20 valid, 2089/2089 grounded.

## Files it touched

- `pc_package/_pcpkg.py`
- `pc_package/schema_ext.py`
- `Makefile`
- `CLAUDE.md`
