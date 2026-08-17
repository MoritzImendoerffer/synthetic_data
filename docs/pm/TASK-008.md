---
type: pm-task
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
task: TASK-008
status: todo
kind: measurement
title: "Measure round two against rounds zero and one with one method, apply the stopping rule, and record the owner's reading"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-008 — Measure round two against rounds zero and one with one method, apply the stopping rule, and record the owner's reading

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-008.md in this work unit — numbered steps, code, commands and the output each must print. Follow it top to bottom.  ONE METHOD FOR ALL THREE POINTS. The pilot's plan quoted chaining 'before' values (30.0 / 37.2) that did not reproduce (31.0 / 35.1) because two runs measured differently. Measure round zero, one and two in one invocation each of check_style.py --compare and check_discourse.py, and quote only those.  THE STOPPING RULE IS FIXED IN ADVANCE — it is in decisions.stopping_rule_edges and in the proposal; do not move an edge after seeing the number. If a number sits within measurement noise of an edge, say so and let the owner decide, but write the plan's edge down first.  THE OWNER'S READING IS THE HUMAN CHECK (owner decision 3). Ask for it after TASK-007, on the rendered pdf, before this page is finished, and quote it. If the owner reads it as still obviously machine-written, what they quote is the next unit's target — record it as such, verbatim, the way exploration.md §1 did.  THE HYPOTHESIS UNDER TEST is stated on the pilot page: does giving the author the measurement change the outcome, when giving them examples did not? Answer it in one sentence, per document, per measure.  ALSO REPORT the two round-one findings: does the new PCR-003 state the commercial scale, and did any inline name land as an agreeing subject.

## Acceptance criteria

- [ ] the results page has a table per measure with SEVEN columns — PDA TR 60, A-Mab, ISPE TT, ISPE PV, then round zero (b0361f1, .claude/work/2026-08-16_01_register-from-four-sources/pre-rewrite/), round one (f06f1a7, this unit's pre-rewrite/), round two (pc_package/) — for BOTH documents, every cell with its denominator
- [ ] measures: mid-sentence ', so ' %, sentence-initial connective %, 2+ coordinators %, connective repertoire (rate and distinct), topic chaining %, copula %, front field %, 'its'/'their'/'it is' per 1000 words, and the register gate's own five length numbers — all produced by check_style.py --compare and check_discourse.py (with and without --cap stated), never quoted from this plan or from the pilot page
- [ ] the stopping rule from decisions.stopping_rule_edges is applied line by line and the verdict is one sentence: 'Track 2 opens' or 'stop and change the target', with the line that decided it
- [ ] the owner's reading is recorded: whether the re-authored pair is still immediately recognisable as machine-written, and the sentences the owner quotes as giving it away — as a section, verbatim, dated; the page says the reading is not blind and why that was accepted
- [ ] the register gate headroom question is answered again: pct_under_15 and pct_over_40 for both documents against the band and the four sources
- [ ] if any measure moved backwards, the page names the substitution that paid for it, counted (round one's model: 25 possessives → 23 copulas)
- [ ] docs/results/README.md gains a row saying why the run happened
- [ ] register_analysis.ipynb gains a §14 that reproduces the tables from the two scripts, or the page states that the scripts alone are the method and the notebook is superseded for these measures

**Depends on:** [[TASK-007]]

## Documents it is about

- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- [[2026-08-XX-register-round-two]] — `docs/results/2026-08-XX-register-round-two.md`
- [[README]] — `docs/results/README.md`
- `authoring/register_analysis.ipynb`
