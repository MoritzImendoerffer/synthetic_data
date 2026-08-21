---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-034
status: todo
kind: document
title: "Author PCMP-001 (A-Mab Drug Substance) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCMP-001"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-034 — Author PCMP-001 (A-Mab Drug Substance) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

43 annex quotes, 0 rhetorical spans to re-anchor later in this batch's annex task. Corpus-level document: no §2b (no single step).

## Acceptance criteria

- [ ] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PCMP-001, <uokey>=None, <outline>=master_plan: brief rebuilt fresh (`## 2b` 0, `## 5d` 0, §5c None); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [ ] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [ ] `check_render.py pc_package/PCMP-001_None.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `master_plan` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [ ] no registered discrepancy for this document, stated
- [ ] the content review (§4): run 1 filed as content-review-PCMP-001.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [ ] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

## Documents it is about

- **PCMP-001** — `pc_package/PCMP-001_master_plan.qmd`

## Files it touched

- `pc_package/PCMP-001_None.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCMP-001.md`
