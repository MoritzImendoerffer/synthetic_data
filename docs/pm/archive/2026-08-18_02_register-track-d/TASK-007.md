---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-007
status: done
kind: measurement
title: "Measure the pilot, take the owner's reading, and decide whether the remaining 16 run"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-003", "PCR-004", "PCR-005", "PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-007 — Measure the pilot, take the owner's reading, and decide whether the remaining 16 run

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-007.md. THIS IS THE DECISION POINT THE PILOT EXISTS FOR. The rule is fixed in decisions.pilot_stopping_rule below and no edge moves after the numbers are seen. If the pilot clears and the reading is acceptable, the remaining 16 run. If it does not, the round stops here and Track C -- rewriting the guide's own commentary -- becomes the candidate instead, having cost three documents rather than nineteen. PCR-003 IS THE CONTROL: it is already at the target register and this round does not touch it, so a measure that moves in the pilot and not in PCR-003 is the instruction rather than drift.

## Acceptance criteria

- [x] measure_trackd.py run over the three pilot documents plus PCR-003 (the untouched control) and the four sources, one invocation, saved to measure_pilot.txt
- [x] the pilot stopping rule below is applied line by line to each of the three, with a holds? column
- [x] the project owner's reading of the three rendered pdfs is recorded VERBATIM and dated, and whatever it quotes is counted afterwards, in that order
- [x] D3 is written as a decisions note with the numbers and both branches, and settled by the owner before any of TASK-008..TASK-028 starts

**Depends on:** [[TASK-006]]

## What was built

The pilot was measured, the owner read the three rendered PDFs, and D3 is settled: STOP. TASK-008..TASK-030 are cancelled and the remaining sixteen documents are not re-authored.

THE EIGHT NUMERIC CONDITIONS ALL HELD. ', so ' 0.0/0.0/0.0 against a band of <=1.0; opens with a connective 4.6/4.5/4.7 against >=3.0; ', and '+clause 0.0/2.1/0.5 against <=3.4; ', not ' 0.0 throughout against <=0.2; passive 58.0/54.3/57.8 inside 53-68; topic chaining +19.9/+4.8/+5.5 against its own baseline; copula -3.0/-8.6/-6.9 against a +2.0 ceiling; the register gate passing on all three. PCR-003, the untouched control, reads +-0.0 against its own baseline, which is what proves the table measures what it claims. measure_pilot.txt carries the run.

THE NINTH CONDITION, THE READING, FAILED. Recorded verbatim and dated in owner-reading-2026-08-18.md before anything it named was counted, which is the order the three previous rounds used. The owner quoted eight sentences across four messages, all from PCR-005, and asked three questions: can the formulation be stopped, should ', which is' be banned, and -- on "Protein load acts through the capacity of the bed" -- whether a scientific article would write that way.

WHAT THE QUOTES COUNT OUT TO, per 100 sentences against 3,338 sentences of published human source. Trailing relatives 1.20-2.97 in the sources against 11.39 in the corpus, 595 instances. ', which' 0.60-2.35 against 9.82. 'acts on / acts through' ZERO in all four sources against 63 in the corpus. 'follows from the' zero against 12. 'aggressive(ness)' zero against 2. The owner wondered whether "acts through the capacity of the bed" only read strangely to a non-native speaker; it does not, and the count says so.

THE FINDING THAT DECIDED IT. PCR-003 is the control, at ', which' 15.3, and it was accepted by the owner in round three. So the fault was not caused by the Track D instruction and was not introduced by the pilot. It is corpus-wide, predates all three rounds, and round three MEASURED it at 15.33 % and shipped anyway, because the number lived in a .txt file the author never saw. That falsifies D3's Option B as written, which blamed the guide.

THE VERDICT, AND IT IS A MEASUREMENT. Eight rewritten sentences -- the ones a paper would write, in the results page table -- were put through check_style.measure against the eight shipped ones. mean_len 20.8 -> 13.5 against a GATED floor of 20.0. pct_under_15 12.5 -> 55.6 % against a GATED ceiling of 32.0. THE REWRITES FAIL THE REGISTER GATE ON TWO OF ITS TWELVE GATED ROWS. Every move that improves the prose -- split the sentence, drop the gloss, state the inference separately -- drives both numbers at a gated edge, and round three is the confirmation: it split sentences, pct_under_15 went 19.5 -> 26.1 toward the ceiling, and its own results page recorded the resulting staccato as a regression. The gate built to stop machine register now enforces it.

Four further causes, in the results page §5: section_plan.yaml requires mechanism in four places while REGISTER_EXEMPLAR.md's fifteen reporting moves contain none about mechanism and the brief carries no domain prose at all; nothing in the verification stack asks whether a sentence commits to anything, because grounding checks provenance and the gates check surface form; three rounds tuned sentence architecture and every one of the owner's eight quotes is about commitment instead; and the self-reference ban is right but is not paired with any supply of human prose about this domain at sentence level.

THE REVIEW LAYER HAS THE SAME BLIND SPOT, INCLUDING THIS SESSION'S. rhetorical_spans is a labelled benchmark layer carrying 26 mechanistic_warrant spans across nine documents, and 6 of the 26 carry a flagged frame. Two are sentences the owner quoted; the rest are in PCR-004 and PCR-008, which this round never touched. The sentence in quote 8 is span PCR-005-R17 and I selected it in TASK-006 today, from a shortlist, as the clearest statement of mechanism in its section. It passed the authoring agent, the register gate and the annex review. All three were judging shape.

NOTHING IS REVERTED. The three pilot documents ship: re-authored, rendered, annexed, grounded, 2084/2084 with strict anchors and 0 weak anchors, 20/20 valid, make test 89, make style 24 OK / 0 FAIL, git diff outputs/ empty. TASK-001 and TASK-002 are mechanism work and stand.

WRITTEN UP: docs/results/2026-08-18-track-d-stopped.md, with the eight cited sentences beside what a paper would write, the gate measurement behind the verdict, and five things a fourth round would have to do differently.

## Documents it is about

- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-004** — `pc_package/PCR-004_harvest.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- `.claude/work/2026-08-18_02_register-track-d/measure_pilot.txt`
- [[D3-does-track-d-continue]] — `docs/pm/decisions/D3-does-track-d-continue.md`
