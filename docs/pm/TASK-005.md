---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-005
status: done
kind: annex
title: "Promote the new PCP-005: render, re-anchor its annex, re-ground the corpus"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-005", "PCR-005"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-005 — Promote the new PCP-005: render, re-anchor its annex, re-ground the corpus

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

48 quotes, no spans. PCR-005's region is report=True in the same pa_* functions — change only the report=False branches.

## Acceptance criteria

- [x] runs ONLY on D7 = PASS; ANNEX-A-BATCH.md for one document: `git mv -f` DRAFT -> PCP-005_protein_a.qmd, both formats rendered explicitly, no missing glyph on the FRESH pdf, page count recorded
- [x] the Protein A region of build_ground_truth.py (`pa_*`, report=False branches) re-anchored: prose quotes moved to the sentence that names the record, table rows left to rebuild, every report_sections/statement read against the new text; no rhetorical layer for a plan
- [x] 20/20 annexes valid; `GROUNDING_STRICT_ANCHORS=1 check_grounding.py` -> OK PCP-005 with 0 ungrounded and N/N across 20 annexes (N printed; 2084 today, any change explained), 0 weak anchors; `git status --short` exactly the document's qmd/docx/pdf, build_ground_truth.py, ground_truth/PCP-005.json; `git diff --stat outputs/` empty; make test, make style 24 OK

**Depends on:** [[TASK-003]]

## What was built

Promoted 2026-08-19 per ANNEX-A-BATCH for one document: DRAFT -> pc_package/PCP-005_protein_a.qmd, both formats rendered explicitly, no missing glyph on the fresh pdf, 31 pages (unchanged). No rhetorical layer (a plan).

Annex (fresh agent, verified by me): 26 of PCP-005's 66 quotes re-anchored, plan branches only, all hunks inside the Protein A block (lines 1571–2209): PA_METHOD_QUOTE 4 (serving 7 records), pa_step 1, pa_equipment 2, pa_studies 3, PA_PRIOR_QUOTE 5, pa_assertions 2 acceptance quotes, pa_report_sections 6 statements. Statements and assertions rewritten where the new plan says something different: pool HCP is judged against an in-process limit (numbers pulled through doe_report.effective_acceptance and CFG.ipc_limits, the same calls the document renders, never typed; report branch untouched behind an if report split); expected-direction assertions now per parameter in the plan's own terms (new PA_PRIOR_CLAIM dict; bed height leaves HCP unchanged; the leached-Protein-A half of the old pH assertion dropped because the new §4.1 expects it flat); leached Protein A acceptance moved to §7; S01–S06 restated to the plan's wording (S06 is now about a factor, in §5.5). Non-gated captions and one out_of_schema_note corrected on the plan side. PCR-005.json byte-identical.

Gates, run by me: 20/20 annexes valid; `GROUNDING_STRICT_ANCHORS=1 check_grounding.py` -> OK PCP-005: 66 quotes, 0 ungrounded; OK PCR-005: 123 quotes, 0 ungrounded; 2084/2084 quotes grounded across 20 annexes, exit 0; weak_claims 0 in all 20; `git status --short` -> exactly PCP-005_protein_a.{qmd,docx,pdf}, build_ground_truth.py, ground_truth/PCP-005.json (plus the four untracked B1 DRAFT scaffolds prepared in advance); `git diff --stat outputs/` empty; make test 95; make style 24 OK / 0 FAIL. N unchanged at 2084.

## Documents it is about

- **PCP-005** — `pc_package/PCP-005_protein_a.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`

## Files it touched

- `pc_package/PCP-005_protein_a.qmd`
- `pc_package/PCP-005_protein_a.docx`
- `pc_package/PCP-005_protein_a.pdf`
- `pc_package/build_ground_truth.py`
- `pc_package/ground_truth/PCP-005.json`
