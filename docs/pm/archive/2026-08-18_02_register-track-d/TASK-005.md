---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-005
status: done
kind: document
title: "Re-author RA-001 in one pass, as a DRAFT"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["RA-001"]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-005 — Re-author RA-001 in one pass, as a DRAFT

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/AUTHOR-A-DOCUMENT.md. Outline `risk_assessment`. Baseline for this document is in measure_baseline_style.txt / measure_baseline_discourse.txt and is printed to the author by brief §5d. Annex exposure at promotion: 317 quotes, 0 rhetorical spans. Currently n/a. THE PASSIVE IS A BAND AND NEVER A FLOOR. PILOT, and one of the three the project owner reads. NEVER RE-AUTHORED, and the largest annex in the corpus at 317 quotes -- the worst case for re-anchoring, which is why it is in the pilot rather than discovered at task 25. Outline risk_assessment; content source is risk_assessment/build_fmea.py.

## Acceptance criteria

- [x] the current text is preserved first: `cp pc_package/RA-001_risk_assessment.qmd .claude/work/2026-08-18_02_register-track-d/pre-rewrite/` and it equals `git show HEAD:pc_package/RA-001_risk_assessment.qmd`
- [x] `uv run --extra discourse python authoring/build_brief.py RA-001` regenerated first; §5d carries all twelve rows and §5c is empty for this document
- [x] ONE agent authors the whole document in one pass from WRITING_GUIDE.md, REGISTER_EXEMPLAR.md, STORY_BIBLE.md, section_plan.yaml -> risk_assessment and the RA-001 brief; it reads no pc_package/*.qmd and no authoring/rhetorical/*.spans.yaml
- [x] `uv run python authoring/check_render.py pc_package/RA-001_risk_assessment.DRAFT.qmd --render` passes including the style gate; the pdf is rendered SEPARATELY with the venv on PATH and glyph-checked fresh; the packing line is copied verbatim into the completion note
- [x] `grep -c '<<NEEDS' <draft>` is 0 and no typed measurement survives the numeral advisory except statistical conventions
- [x] `grep -c 'screening retained\|screening identified\|the design carries\|the model identifies\|the study selected' <draft>` is 0
- [x] the committed pc_package/RA-001_risk_assessment.qmd and all 20 annexes are untouched; git status shows only the DRAFT and its untracked renders

**Depends on:** [[TASK-001]], [[TASK-002]]

## What was built

RA-001 re-authored in one pass by claude-opus-5, as pc_package/RA-001_risk_assessment.DRAFT.qmd. Outline `risk_assessment`; content source risk_assessment/build_fmea.py. Not promoted -- that is TASK-006. This document had never been re-authored, so this is the first time it leaves its original voice.

Final clause packing line, verbatim:

   --    clause packing (diagnostic, never gated)         ', so ' mid-sentence  0.0 % of sentences (0/190), opens with a connective  4.7 % (9/190), 2+ clause coordinators  0.0 %, ', and '+clause  0.5 % (1/190), ', not '  0.0 % (0/190)  [sources: 0.1-0.4 / 3.7-6.1 / 1.2-3.1 / 1.1-3.4 / 0.0-0.2]

Against brief §5d, where this document held two of the corpus's worst rows: ', so ' 14.6 -> 0.0, the highest of all 20 documents brought to the floor of the source band (target <=1.0); opens with a connective 0.0 -> 4.7 (>=3.0); 2+ coordinators 12.8 -> 0.0; ', and '+clause regex 23.8 -> 0.5 (<=3.4); ', not ' 0.6 -> 0.0 (<=0.2).

Register table: 190 sentences, 4118 words. All twelve gated rows ok -- mean 21.7, median 20.0, over 40 words 6.3, over 55 words 0.0, under 15 words 30.0 (band 15-32), em-dashes 0.0, semicolons 1.7, colons 2.2, parentheses 5.8, bold 0.0, coined compounds 0.0, "rather than" 0.0. Connectives 5.3 per 1k, 6 of 9 distinct. "OK register is within the human-source envelope."

Parser rows, previous revision -> now: topic chaining 39.1 -> 44.6 % (82/184), rose; copula 24.7 -> 17.8 % (33/185), fell; front field 6.8 -> 19.5 %; passive 64.2 -> 57.8 % (107/185); ', and '+clause parser 37.7 -> 1.1 %.

PDF: rendered separately, glyph-checked fresh -- 30 pp, no missing glyphs.

Verified by me: <<NEEDS:>> 0; false-agent phrases 0; all seven forbidden clause shapes 0; no expression-as-subject; no typed measurement at all. git diff over tracked files empty.

TWO THINGS THE AGENT FOUND AND ONE IT HIT. It removed a false uniqueness claim it met while writing -- an "only step at which every parameter reaches a quality attribute" statement about anion exchange, when virus filtration is 2 of 2 as well -- and pulled "Steps 6, 8 and 9" from the model rather than typing it. RA-001 carries no registered discrepancy (§5c: None), so an unregistered inconsistency is a bug and removing it was correct. It also reports verifying by hand that all 37 ranking rows, all 37 assignment rows and all 10 CQA rows are verbatim in the rendered docx, 0 misses of 84, which is the row half of the largest annex in the corpus at 317 quotes; the prose statements still need re-anchoring at TASK-006, as expected after any re-author.

OPERATIONAL FINDING FOR THE REMAINING BATCHES. The three parallel agents share one session scratchpad path, and another agent's file overwrote this one's working file mid-run. It recovered into a private subdirectory and nothing in the repository was affected, but the batch tasks TASK-008 onward run four documents at once, so each agent should be given a distinct scratch subdirectory in its brief.

## Documents it is about

- **RA-001** — `pc_package/RA-001_risk_assessment.qmd`

## Files it touched

- `pc_package/RA-001_risk_assessment.DRAFT.qmd`
- [[RA-001.brief]] — `authoring/out/RA-001.brief.md`
- `.claude/work/2026-08-18_02_register-track-d/pre-rewrite/RA-001_risk_assessment.qmd`
