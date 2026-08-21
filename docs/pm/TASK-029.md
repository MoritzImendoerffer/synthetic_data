---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-029
status: blocked
kind: document
title: "Author PCP-007 (Cation Exchange Chromatography (Step 7)) in one pass under the rebuilt apparatus, with one content-review cycle"
generated: true
waiting_on: another task
tags: [pm/task, pm/blocked]
about: ["PCP-006", "PCP-007"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-029 — Author PCP-007 (Cation Exchange Chromatography (Step 7)) in one pass under the rebuilt apparatus, with one content-review cycle

**Epic:** [[epic]] · **Status:** `blocked` · **Waiting on:** another task · **Board:** [[_Board]]

## Why it exists

49 annex quotes, 0 rhetorical spans to re-anchor later in this batch's annex task. PCP-007 is at an earlier round (round three / Track D / round two); re-done so the corpus has ONE register. BLOCKED by D8 B3 = FAIL blind (2026-08-21): the owner preferred the pre-campaign PCP-006 in the sampled reading, so under D8's rule the batches do not continue until the owner releases B4. The owner's amendment of 2026-08-21 keeps the promoted documents but is a disposition, not a release — B2 needed a separate word after its FAIL and B4 does too.

## Acceptance criteria

- [ ] procedures/AUTHOR-A-DOCUMENT.md followed with <DOC>=PCP-007, <uokey>=cex, <outline>=plan: brief rebuilt fresh (`## 2b` 1, `## 5d` 0, §5c None); DRAFT instantiated from the template and executing; ONE agent (`opus`, fresh context) launched with the §2 prompt verbatim and nothing else
- [ ] the transcript audit (§3) shows Reads of only the allowed inputs and code, and an empty `suspect` list — no --review, check_discourse, measure_, sentence-listing or rewrite script, no other .qmd; if not empty, the draft is set aside as evidence and a fresh agent re-launched with the same prompt, and the outcome says so
- [ ] `check_render.py pc_package/PCP-007_cex.DRAFT.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS:>>, tic gate OK, docx renders; fresh pdf with no missing glyph; every section of section_plan.yaml `plan` present in order; typed-measurement grep hits only statistical conventions or code, each listed
- [ ] no registered discrepancy for this document, stated
- [ ] the content review (§4): run 1 filed as content-review-PCP-007.md; if any question read 'no', ONE return to the same author and a second fresh judge filed as run 2; the outcome states run-1/run-2 counts per question and 'promotable on content' or not — either way the document proceeds to its batch's annex task
- [ ] outcome records ONLY: model (self-reported), check_render passes, render, glyphs, <<NEEDS>>, sentences, words, pages, audit result, review counts — no style row, no frame count; `git status --short pc_package/` shows only the untracked DRAFT(s) of this batch

**Depends on:** [[TASK-026]]

## Documents it is about

- **PCP-006** — `pc_package/PCP-006_viral_inactivation.qmd`
- **PCP-007** — `pc_package/PCP-007_cex.qmd`

## Files it touched

- `pc_package/PCP-007_cex.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCP-007.md`
