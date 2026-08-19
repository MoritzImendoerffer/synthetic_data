---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-010
status: done
kind: mechanism
title: "Add the four content questions to the reviewer's checklist and calibrate them on the excerpt and the probe"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-010 — Add the four content questions to the reviewer's checklist and calibrate them on the excerpt and the probe

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Runs only on D4 = PASS. The calibration is the check that the questions see what the reading saw; the excerpt is a known-bad text with eight owner-quoted sentences and the probe is the text the owner accepted. The judge's freshness matters (results §5.6 — the annex reviewer had the same blind spot): give it the checklist and the two texts and nothing else. Whether an LLM judge is a sufficient reviewer stays an open question in the proposal; this task makes the question testable, it does not settle it.

## Acceptance criteria

- [x] REVIEW_CHECKLIST.md gains a 'Content' block of exactly four questions: (1) does every `because`, `since`, `governs`, `sets` name a physical cause? (2) is every technical term a term of art in the chromatography / cell-culture literature? (3) can each sentence in a mechanism paragraph be disagreed with on its own? (4) does any sentence tell the reader how to file the finding it just stated? — and one line on how it is run: by a fresh-context agent given only the checklist and the text, or by the owner; a 'no' on any of the four blocks promotion
- [x] content-review-calibration.md records the four answers, per sentence flagged, for pc_package/PCR-005_protein_a.EXCERPT.qmd and for the PROBE, produced by a fresh-context agent (model recorded) that has read neither the guide nor any counter; the excerpt must flag question (4) on at least the sentences the owner quoted in docs/results/2026-08-18-track-d-stopped.md §4 (#1, #3, #8) and question (1)/(2) on #6 and #7 — if it does not, the questions are reworded and re-run once, and the rewording recorded
- [x] the annex procedure for the next round (a new procedures/REVIEW-BEFORE-PROMOTION.md in this unit, referenced from RUNNER.md step 5) states that the content review runs BEFORE a draft is promoted and where its answers are filed

**Depends on:** [[TASK-007]], [[TASK-005]]

## What was built

authoring/REVIEW_CHECKLIST.md gains a 'Content — what a sentence commits to' block: four questions with what a 'no' looks like (the owner's own examples), who answers (a fresh-context agent given only the block and the text, or the owner), and 'a no on any of the four blocks promotion'. procedures/REVIEW-BEFORE-PROMOTION.md (this unit) says who, the verbatim prompt, what is filed and the disposition rule; RUNNER.md step 5's review line points at it via REVIEW_CHECKLIST.md.

Calibration (content-review-calibration.md): four fresh-context Opus 5 judges (two runs × two texts), each given the four questions and one PDF, told nothing else. RUN 1 on the shipped text: #1, #3 flagged Q4; #2 Q1+Q4; #4 Q4; #6 Q2 ('aggressiveness of desorption is a coinage'); #8 Q1; #7 NOT flagged (the clause after the colon supplies the cause) — four of five targets. Reworded ONCE, as the plan allows: Q1 now asks for the cause 'in the clause where the verb stands, and not only in a clause that follows a colon or in the next sentence' (the owner's objection to #6/#7 stated as a rule); applied to the checklist and the procedure. RUN 2 on the shipped text: #6 Q1+Q2, #7 Q1, #8 Q1, #5 Q3 (new), #1 #2 #3 Q4 — seven of the eight owner-quoted sentences flagged; #8 lands on Q1 in both runs and never on Q4, which is recorded as the one persistent gap against the literal target and not reworded again. The judge also found a fault nobody had named: 'predicted coefficient / adjusted coefficient' for predicted / adjusted R² (three times).

The probe (the text the owner preferred) is NOT clean under the same judge: Q1 no (five 'acts on/through/sets' clauses whose direction arrives one sentence late), Q3 no (three announcement sentences), Q4 yes (five, then seven), Q2 yes — stable across both runs and at roughly a third of the shipped Q4 rate per sentence. So the checklist as written would send a probe-quality draft back once with the sentences named, which is the intended behaviour. One judge catch was a real domain error shared with authoring/mechanism/protein_a.yaml — histidine is already protonated across the elution pH range, so a within-range mechanism cannot rest on it — and the file's `elution_ph` entry was corrected in this task (residual affinity and the carboxylate contacts; the histidine story is why low pH elutes at all). make test 95 passed.

## Files it touched

- [[REVIEW_CHECKLIST]] — `authoring/REVIEW_CHECKLIST.md`
- `.claude/work/2026-08-18_03_author-facing-apparatus/content-review-calibration.md`
- `.claude/work/2026-08-18_03_author-facing-apparatus/procedures/REVIEW-BEFORE-PROMOTION.md`
- `authoring/mechanism/protein_a.yaml`
