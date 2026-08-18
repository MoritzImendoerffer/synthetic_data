---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-010
status: todo
kind: mechanism
title: "Add the four content questions to the reviewer's checklist and calibrate them on the excerpt and the probe"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-010 — Add the four content questions to the reviewer's checklist and calibrate them on the excerpt and the probe

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

Runs only on D4 = PASS. The calibration is the check that the questions see what the reading saw; the excerpt is a known-bad text with eight owner-quoted sentences and the probe is the text the owner accepted. The judge's freshness matters (results §5.6 — the annex reviewer had the same blind spot): give it the checklist and the two texts and nothing else. Whether an LLM judge is a sufficient reviewer stays an open question in the proposal; this task makes the question testable, it does not settle it.

## Acceptance criteria

- [ ] REVIEW_CHECKLIST.md gains a 'Content' block of exactly four questions: (1) does every `because`, `since`, `governs`, `sets` name a physical cause? (2) is every technical term a term of art in the chromatography / cell-culture literature? (3) can each sentence in a mechanism paragraph be disagreed with on its own? (4) does any sentence tell the reader how to file the finding it just stated? — and one line on how it is run: by a fresh-context agent given only the checklist and the text, or by the owner; a 'no' on any of the four blocks promotion
- [ ] content-review-calibration.md records the four answers, per sentence flagged, for pc_package/PCR-005_protein_a.EXCERPT.qmd and for the PROBE, produced by a fresh-context agent (model recorded) that has read neither the guide nor any counter; the excerpt must flag question (4) on at least the sentences the owner quoted in docs/results/2026-08-18-track-d-stopped.md §4 (#1, #3, #8) and question (1)/(2) on #6 and #7 — if it does not, the questions are reworded and re-run once, and the rewording recorded
- [ ] the annex procedure for the next round (a new procedures/REVIEW-BEFORE-PROMOTION.md in this unit, referenced from RUNNER.md step 5) states that the content review runs BEFORE a draft is promoted and where its answers are filed

**Depends on:** [[TASK-007]], [[TASK-005]]

## Files it touched

- [[REVIEW_CHECKLIST]] — `authoring/REVIEW_CHECKLIST.md`
- `.claude/work/2026-08-18_03_author-facing-apparatus/content-review-calibration.md`
