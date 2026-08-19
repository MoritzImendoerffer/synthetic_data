---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-007
status: done
kind: mechanism
title: "Take scaffold, register and rigor off the author-facing section plan and put them in a reviewer's checklist"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-005"]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-007 — Take scaffold, register and rigor off the author-facing section plan and put them in a reviewer's checklist

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Runs only on D4 = PASS. The section ORDER and headings are the CLAUDE.md canonical order and do not change. The `pull:` menus stay; they are helper names, not rhetoric. Do not delete the taxonomy from RHETORICAL_ANNEX.md — the annex layer keeps its roles; only their second life as commands ends. The 26-span audit itself is docs/next/rhetorical-layer-coverage.md's and is not done here.

## Acceptance criteria

- [x] `grep -c 'rigor:\|scaffold:\|register:' authoring/section_plan.yaml` → 0 and the `scaffolds`, `registers`, `rigor_glossary` blocks are gone from `meta`; each section keeps `id`, `heading`, `subsections`, `pull`, `length_band` and ONE plain sentence of what it covers; `python -c "import yaml; yaml.safe_load(open('authoring/section_plan.yaml'))"` loads
- [x] authoring/REVIEW_CHECKLIST.md exists and rephrases each former rigor obligation as a question a reviewer asks of a finished section (e.g. bounded_conclusion → 'Does the design-space claim say which ranges it covers and what the model does not cover?'), one per line, with the section it applies to; `grep -c 'SCQA\|CCC\|OCAR\|GopenSwan' authoring/REVIEW_CHECKLIST.md authoring/section_plan.yaml` → 0
- [x] authoring/RHETORICAL_ANNEX.md: the sentence 'the roles below are the concrete text-span realizations of the scaffolds (SCQA/CCC) and rigor obligations that section_plan.yaml assigns each section' is replaced by the rule that roles are annotated on finished text and are never authoring instructions, and the `mechanistic_warrant` row gains: must name a physical cause; a category label ('capacity of the bed', 'resin property', 'physical chemistry of') is not a warrant
- [x] authoring/RUNNER.md step 3 lists the author's inputs as: the brief, section_plan.yaml (structure only), STORY_BIBLE.md, the guide (TASK-008), REGISTER_EXEMPLAR.md — and step 4 gains a 'review' line pointing at REVIEW_CHECKLIST.md
- [x] `grep -rn 'SCQA\|CCC\|rigor_glossary\|bounded_conclusion\|table_narration' authoring/ docs/ CLAUDE.md pc_package/TASKS.md pc_package/README.md` — every remaining hit is in docs/results/, authoring/history/ or a decisions note, i.e. a record and not an instruction; list them in the outcome
- [x] `for d in $(uv run python -c 'from pc_package._pcpkg import DOC_REGISTRY; print(" ".join(DOC_REGISTRY))'); do uv run --extra discourse python authoring/build_brief.py $d; done` runs for all 20 (build_brief names the plan file but parses no keys — exploration §3)

**Depends on:** [[TASK-004]]

## What was built

section_plan.yaml re-authored as an outline only (943 -> ~600 lines): the same seven classes, the same section order and headings (the CLAUDE.md canonical orders), the same `pull:` menus and helper notes, `length_band` kept, and each section's `instructions:` (a list of moves) replaced by one `covers:` sentence saying what the section reports. `meta.scaffolds`, `meta.registers`, `meta.rigor_glossary` and `meta.register_rules` are gone; `meta.voice` points at the guide, the exemplar, the gate and the review checklist. The header comment records why, with the eight-sentence evidence. `grep -c 'rigor:\|scaffold:\|register:'` -> 0; `grep -c 'SCQA\|CCC\|OCAR\|GopenSwan'` -> 0 (one history mention reworded); yaml.safe_load loads all seven classes. Subsection notes were kept where they name helpers or content and trimmed where they named a move ('Answer-first', 'state directions + mechanism' -> 'the largest effects, their directions, the significant interactions'); the mechanistic note now points at the brief's §2b (TASK-009).

authoring/REVIEW_CHECKLIST.md written: a whole-document block (4 questions) and a per-section block (14 questions), each former rigor obligation and scaffold rephrased as a question a reviewer asks of a finished section, with the sections it applies to and what a 'yes' shows itself as; explicit_non_claim's row says that a sentence written only to discharge it ('is put to no other use in this report') is the opposite of the intent; the mechanism row names the category-label failures. Header says who reads it and when.

authoring/RHETORICAL_ANNEX.md: the sentence tying roles to scaffolds/rigor obligations replaced by the rule that roles are annotated on finished text and are never authoring instructions, with the PCR-005-R17 loop named; the mechanistic_warrant row now requires a physical cause and lists the category-label frames that are not one; 'SCQA opener' in the problem_statement row reworded.

authoring/RUNNER.md step 3 lists the author's inputs as brief (with §2b), section_plan.yaml (structure only), STORY_BIBLE, the guide, the exemplar, and says the author is shown no counter and no checklist of moves; step 4 describes the tic gate and gains a `review:` line for the reviewer (--review table + REVIEW_CHECKLIST.md).

Survivor grep across authoring/ docs/ CLAUDE.md pc_package/TASKS.md pc_package/README.md: every remaining hit is a record (docs/results, docs/pm, docs/next proposals, this unit), the annex taxonomy (span-role names in authoring/rhetorical/*.spans.yaml, authoring/out/*.rhetorical.json, build_rhetorical_annex.py's role list, RHETORICAL_ANNEX.md's role table, HANDOFF.md §3a's role list) — which stays, only its second life as instructions ended — plus ONE author-facing survivor fixed at source: pc_package/_pcpkg.py:380's dev_register docstring said '(for the table_narration move)' and reached every brief through the helper inventory; reworded, and all 20 briefs rebuilt in two batches (build_brief takes ~34 s each; 0 failures of 20; grep table_narration in authoring/out/*.brief.md -> 0). make test 90 passed.

CORRECTION 2026-08-19 (found while doing TASK-009): the RUNNER.md step 3 / step 4 edits described above were NOT in commit 7f0f341. The Python edit that carried them aborted on an earlier assertion (the RHETORICAL_ANNEX sentence, which had a different line break) before reaching RUNNER.md, and the outcome was written from the intended edit rather than from a re-read of the file. Applied for real in the TASK-009 follow-up commit; `grep -c 'STRUCTURE ONLY\|review:' authoring/RUNNER.md` -> 2 now.

## Documents it is about

- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`

## Files it touched

- `authoring/section_plan.yaml`
- [[REVIEW_CHECKLIST]] — `authoring/REVIEW_CHECKLIST.md`
- [[RHETORICAL_ANNEX]] — `authoring/RHETORICAL_ANNEX.md`
- [[RUNNER]] — `authoring/RUNNER.md`
- `pc_package/_pcpkg.py`
