---
type: pm-task
epic: 2026-08-18_01_register-third-round
sprint: 2026-08-18_01_register-third-round
task: TASK-006
status: todo
kind: measurement
title: "Measure the four-point series by one method, apply the stopping rule, and record the owner's reading"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-18_01_register-third-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-006 — Measure the four-point series by one method, apply the stopping rule, and record the owner's reading

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

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

## Files it touched

- [[2026-08-XX-register-round-three]] — `docs/results/2026-08-XX-register-round-three.md`
- [[README]] — `docs/results/README.md`
