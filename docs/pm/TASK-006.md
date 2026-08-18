---
type: pm-task
epic: 2026-08-18_01_register-third-round
sprint: 2026-08-18_01_register-third-round
task: TASK-006
status: partly
kind: measurement
title: "Measure the four-point series by one method, apply the stopping rule, and record the owner's reading"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/partly]
about: ["PCP-003"]
---

> [!warning] Generated from `.claude/work/2026-08-18_01_register-third-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-006 — Measure the four-point series by one method, apply the stopping rule, and record the owner's reading

**Epic:** [[epic]] · **Status:** `partly` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-006.md — the previous unit's TASK-008 procedure with four points and eight measures. ONE METHOD FOR ALL FOUR POINTS. Round zero, one and two are on disk (exploration §2 verified all three byte-identical to their commits); round three is pc_package/. Measure all four in one invocation each. THE STOPPING RULE IS FIXED IN decisions.stopping_rule_edges before this task runs. Do not move an edge. THE PREDICTION TO CHECK: exploration §3 predicts ', and '+clause overshoots to ~0 %. If it does, say so as an overshoot, not a win, and name what paid for it (semicolons? ', which'? shorter sentences? pct_under_15?). THE OWNER'S READING is the human check (owner decision, round two). Ask AFTER TASK-005 on the rendered pdf. Whatever is quoted becomes the next unit's target: count it, in that order — a reader found it, the count confirmed it — as rounds two and three both did.

## Acceptance criteria

- [ ] the page has, per measure, EIGHT columns — PDA TR 60, A-Mab, ISPE TT, ISPE PV, then PCR-003 round zero (b0361f1), one (f06f1a7), two (e7a4768), three (pc_package/) — plus a PCP-003 round-two control column where the measure exists for it, every cell with its denominator; produced by ONE invocation each of `check_style.py --compare` and `check_discourse.py` (uncapped as the numbers, --cap in a footnote), and by nothing else
- [ ] measures: the three new ones (', and '+clause regex AND parser, ', not ', passive) and the five from round two (', so ', initial connective, 2+ coordinators, chaining, copula) plus front field, connective repertoire, possessives, and the register gate's five length numbers
- [ ] the stopping rule from decisions.stopping_rule_edges is applied line by line, and the verdict is one sentence naming the line that decided it; the ONE-GENRE caveat is stated: a move in PCR-003 alone is 'moved in the report'
- [ ] the round-two overshoot prediction is checked: is ', and '+clause at or below the sources (1.1-3.4 %) or below ALL of them (an overshoot)? is passive inside the 54-60 band, or above it? say which and count it
- [ ] the three 'screening retained' sentences: are they gone, and what replaced them (quote the new sentence)
- [ ] the owner's reading is recorded verbatim and dated: is PCR-003 still immediately recognisable as machine-written, and which sentences give it away; the page says the reading is not blind (fourth read of this document) and why that was accepted; anything quoted is counted afterwards, in that order
- [ ] docs/results/README.md gains a row; the page states that the scripts are the method and the notebook is superseded for these measures

**Depends on:** [[TASK-005]]

## What was built

MEASUREMENT HALF COMPLETE; the owner's reading is outstanding and is D2 in docs/pm/decisions/.

Four points measured by ONE method, one invocation each, all five files at once: check_style.py --compare -> measure_style.txt, check_discourse.py -> measure_discourse.txt, --cap -> measure_discourse_cap.txt, plus measure_possessive.txt and measure_whatpaid.txt on the same prose extraction. All four points verified byte-identical to their commits (b0361f1, f06f1a7, e7a4768, and PCP-003 at e7a4768 as the control) with git show | diff -q BEFORE anything was measured.

THE THREE NEW MEASURES, round two -> round three:
  ', and '+clause regex   22.6 -> 0.5 %   (sources 1.1-3.4)
  ', and '+clause parser  25.4 -> 0.7 % (3/430)   (sources 1.0-3.4 uncapped)
  ', not '                 4.3 -> 0.0 %   (sources 0.0-0.2)
  passive        35.4 (146/413) -> 57.4 % (247/430)   (sources 56.9-64.0 on the same n)

THE FIVE FROM ROUND TWO ALL HELD, and two unasked-for measures moved a long way: copula 25.7 -> 16.5 % and adjunct front field 17.4 -> 30.2 %, the latter from below all four sources to inside their range. Nothing regressed on any printed measure.

THE STOPPING RULE: all EIGHT lines hold, no edge moved after the numbers were seen, and nothing sits within 0.5 pt of an edge so the owner-decides clause is not invoked. The line that decided the round is the passive.

THE PREDICTED OVERSHOOT HAPPENED AND IS NAMED AS ONE. ', and '+clause is below all four sources on BOTH halves of the pair (0.5 regex, 0.7 parser). Third overshoot in three rounds. The passive is inside the band, 0.5 pt above the lowest source, not above it.

WHAT PAID FOR IT, counted rather than asserted (measure_whatpaid.txt): not semicolons, which stayed at 1.37 % of sentences against a ceiling nobody approached. Two things paid. pct_under_15 rose 19.5 -> 26.1 against a 32.0 ceiling, which is sentence splitting and was predicted. And ', which' rose 9.50 -> 15.33 % of sentences against sources at 0.60-2.35 % -- coordination became subordination. That measure was already six times the sources and is now more than six times the highest of them. It is the strongest candidate for round four and it was found by measuring what paid, not by reading.

THE THREE 'screening retained' SENTENCES ARE GONE, all five forbidden strings at 0, each replaced in its own section by the passive participle the guide's worked correction gives, quoted side by side on the page. One instance of the same fault survives on purpose at line 879 and the page says why. The crude count falls 5 -> 2, one of which is a regex false positive.

EVERY CELL ON THE PAGE TRACES TO A MEASURE FILE, verified by script over all 71 table rows: the only numeric tokens not in a measure file are dates in paths, the stopping rule's own 2.0 pt edge, one derived difference (12.8), the notebook's 600/450 caps and the per-1000-words label. The two grep-only claims now carry their commands in the Verification block.

docs/results/README.md gained its row. The page states that the two scripts are the method and that register_analysis.ipynb §13 is superseded for these measures.

WHAT REMAINS: the owner's reading, recorded verbatim and dated, and the count of whatever it quotes, in that order. The page carries a '_Not yet recorded._' section. This is D2 in docs/pm/decisions/, which is where the machinery says an owner question belongs -- a task never waits on the project owner, a decisions note does.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`

## Files it touched

- [[2026-08-XX-register-round-three]] — `docs/results/2026-08-XX-register-round-three.md`
- [[README]] — `docs/results/README.md`
