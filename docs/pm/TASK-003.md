---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-003
status: done
kind: document
title: "Re-author PCP-007 in one pass, as a DRAFT"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-007"]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-003 — Re-author PCP-007 in one pass, as a DRAFT

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/AUTHOR-A-DOCUMENT.md. Outline `plan`. Baseline for this document is in measure_baseline_style.txt / measure_baseline_discourse.txt and is printed to the author by brief §5d. Annex exposure at promotion: 67 quotes, 0 rhetorical spans. Currently 28 pp. THE PASSIVE IS A BAND AND NEVER A FLOOR. PILOT, and one of the three the project owner reads. A plan: the genre that fell into the copula/expletive trade twice.

## Acceptance criteria

- [x] the current text is preserved first: `cp pc_package/PCP-007_cex.qmd .claude/work/2026-08-18_02_register-track-d/pre-rewrite/` and it equals `git show HEAD:pc_package/PCP-007_cex.qmd`
- [x] `uv run --extra discourse python authoring/build_brief.py PCP-007` regenerated first; §5d carries all twelve rows and §5c is empty for this document
- [x] ONE agent authors the whole document in one pass from WRITING_GUIDE.md, REGISTER_EXEMPLAR.md, STORY_BIBLE.md, section_plan.yaml -> plan and the PCP-007 brief; it reads no pc_package/*.qmd and no authoring/rhetorical/*.spans.yaml
- [x] `uv run python authoring/check_render.py pc_package/PCP-007_cex.DRAFT.qmd --render` passes including the style gate; the pdf is rendered SEPARATELY with the venv on PATH and glyph-checked fresh; the packing line is copied verbatim into the completion note
- [x] `grep -c '<<NEEDS' <draft>` is 0 and no typed measurement survives the numeral advisory except statistical conventions
- [x] `grep -c 'screening retained\|screening identified\|the design carries\|the model identifies\|the study selected' <draft>` is 0
- [x] the committed pc_package/PCP-007_cex.qmd and all 20 annexes are untouched; git status shows only the DRAFT and its untracked renders

**Depends on:** [[TASK-001]], [[TASK-002]]

## What was built

PCP-007 re-authored in one pass by claude-opus-5, as pc_package/PCP-007_cex.DRAFT.qmd. Outline `plan`. Not promoted -- that is TASK-006.

Final clause packing line, verbatim:

   --    clause packing (diagnostic, never gated)         ', so ' mid-sentence  0.0 % of sentences (0/219), opens with a connective  4.6 % (10/219), 2+ clause coordinators  1.8 %, ', and '+clause  0.0 % (0/219), ', not '  0.0 % (0/219)  [sources: 0.1-0.4 / 3.7-6.1 / 1.2-3.1 / 1.1-3.4 / 0.0-0.2]

Against brief §5d: ', so ' 10.7 -> 0.0 (target <=1.0); opens with a connective 0.0 -> 4.6 (>=3.0); 2+ coordinators 5.6 -> 1.8; ', and '+clause regex 20.4 -> 0.0 (<=3.4); ', not ' 0.0 -> 0.0 (<=0.2).

Register table: 219 sentences, 5183 words. All twelve gated rows ok -- mean 23.7 (20.0-30.5), median 23.0 (18.0-26.5), over 40 words 7.3 (3.0-21.5), over 55 words 0.5 (<=9.5), under 15 words 19.2 (15.0-32.0), em-dashes 0.0, semicolons 0.0, colons 0.6, parentheses 5.8 (3.0-14.5), bold 0.0, coined compounds 0.0, "rather than" 0.0. Connectives 6.0 per 1k, 8 of 9 distinct. "OK register is within the human-source envelope."

Parser rows (check_discourse --cap), previous revision -> now: topic chaining 39.3 -> 59.2 % (129/218), which is inside the source range 57.0-61.9 for the first time; copula 16.7 -> 13.7 % (30/219), so it FELL rather than rose, and the copula/expletive trade the plan genre fell into twice did not happen; front field 12.5 -> 20.5 %; passive 63.0 -> 58.0 % (127/219), inside the 53-68 rule band; ', and '+clause parser 27.1 -> 0.5 %.

PDF: rendered separately with the venv on PATH and glyph-checked on the FRESH pdf -- 30 pp, no missing glyphs. Plans band is 23-31 pp. Down from 33 pp because appendices A and B now carry the coded design matrices only, which is what section_plan.yaml specifies; the duplicate natural-unit matrices were dropped. Structure, not filler.

Verified by me, not taken on the agent's word: <<NEEDS:>> 0; the five false-agent phrases 0; ', so ' / ', and the' / ', and this' / ', and both' / ', and it' / ', and each' / ', not ' all 0; no {python} expression as the subject of an agreeing verb; one typed-measurement advisory hit, a 95 % predictive interval, which is a statistical convention the advisory exempts. git diff over tracked files is empty, so the committed .qmd, every other document and all 20 annexes are untouched.

The agent reports D-001 was avoided rather than touched: at cex the set-point of all four RSM factors is the midpoint of the characterization range, so the plan's set-point statement is true for this step, and §8 says so explicitly. Brief §5c is None for PCP-007. TASK-006 re-verifies every registered discrepancy verbatim, which is where that claim gets checked rather than believed.

## Documents it is about

- **PCP-007** — `pc_package/PCP-007_cex.qmd`

## Files it touched

- `pc_package/PCP-007_cex.DRAFT.qmd`
- [[PCP-007.brief]] — `authoring/out/PCP-007.brief.md`
- `.claude/work/2026-08-18_02_register-track-d/pre-rewrite/PCP-007_cex.qmd`
