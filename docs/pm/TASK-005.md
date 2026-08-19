---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-005
status: todo
kind: annex
title: "Promote the new PCP-005: render, re-anchor its annex, re-ground the corpus"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCP-005", "PCR-005"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-005 — Promote the new PCP-005: render, re-anchor its annex, re-ground the corpus

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

48 quotes, no spans. PCR-005's region is report=True in the same pa_* functions — change only the report=False branches.

## Acceptance criteria

- [ ] runs ONLY on D7 = PASS; ANNEX-A-BATCH.md for one document: `git mv -f` DRAFT -> PCP-005_protein_a.qmd, both formats rendered explicitly, no missing glyph on the FRESH pdf, page count recorded
- [ ] the Protein A region of build_ground_truth.py (`pa_*`, report=False branches) re-anchored: prose quotes moved to the sentence that names the record, table rows left to rebuild, every report_sections/statement read against the new text; no rhetorical layer for a plan
- [ ] 20/20 annexes valid; `GROUNDING_STRICT_ANCHORS=1 check_grounding.py` -> OK PCP-005 with 0 ungrounded and N/N across 20 annexes (N printed; 2084 today, any change explained), 0 weak anchors; `git status --short` exactly the document's qmd/docx/pdf, build_ground_truth.py, ground_truth/PCP-005.json; `git diff --stat outputs/` empty; make test, make style 24 OK

**Depends on:** [[TASK-003]]

## Documents it is about

- **PCP-005** — `pc_package/PCP-005_protein_a.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`

## Files it touched

- `pc_package/PCP-005_protein_a.qmd`
- `pc_package/PCP-005_protein_a.docx`
- `pc_package/PCP-005_protein_a.pdf`
- `pc_package/build_ground_truth.py`
- `pc_package/ground_truth/PCP-005.json`
