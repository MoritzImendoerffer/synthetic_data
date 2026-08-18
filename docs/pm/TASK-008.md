---
type: pm-task
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
task: TASK-008
status: partly
kind: measurement
title: "Measure round two against rounds zero and one with one method, apply the stopping rule, and record the owner's reading"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/partly]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-008 — Measure round two against rounds zero and one with one method, apply the stopping rule, and record the owner's reading

**Epic:** [[epic]] · **Status:** `partly` · **Waiting on:** the assistant · **Board:** [[_Board]]

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

## What was built

MEASURED AND WRITTEN; ONE ACCEPTANCE LINE OPEN. docs/results/2026-08-18-register-round-two.md carries every table the acceptance asks for, with seven columns per measure (four sources, three rounds) for both documents and a denominator on every rate. The owner's reading is not recorded, because it has not been given; the page says so in place rather than omitting the section, and the D1 decision note now separates the numbers half (answered) from the reading half (open).

ONE METHOD, THREE POINTS. Round zero (b0361f1), round one (f06f1a7) and round two were measured in ONE invocation each of check_style.py --compare and check_discourse.py, per decisions.same_method_all_three_points. Raw output is in the work unit as measure_style.txt, measure_discourse.txt, measure_discourse_cap.txt and measure_possessive.txt, and every number on the page was re-verified against those files by script, not by eye.

THE STOPPING RULE HOLDS ON EVERY LINE, and no edge was moved after the numbers were seen:
  ', so '        edge <= 1.0 %   PCP-003 0.0   PCR-003 0.0    holds
  opens on conn. edge >= 3.0 %   PCP-003 4.9   PCR-003 4.0    holds
  chaining       >= 32.4 / 28.7  PCP-003 46.0  PCR-003 46.1   holds (rose, did not merely hold)
  copula         <= 29.6 / 34.5  PCP-003 21.9  PCR-003 25.7   holds (fell in both)
  register gate  passes both     OK            OK             holds
No line is within 0.5 points of its edge, so nothing is a judgement call. VERDICT: Track 2 opens on the numbers.

THE PROPOSAL'S ORIGINAL RULE ALSO CLEARS, and it was not applied. Its dropped bar was 'chaining clears roughly 45 % in both genres and neither copula nor front field regresses'. Chaining is at 46.0 and 46.1, copula fell in both and front field roughly doubled in both. The rule dropped for being unreachable by authoring instructions is cleared by the round that stopped aiming at it.

THE HYPOTHESIS: five of five measures moved in both genres, against one of five in the pilot. The page states what this round CANNOT separate: it changed three things at once (the rule became a substitution, the count is printed on every render, the brief carries the document's own figure). What it does add is that measures NOBODY ASKED FOR moved furthest -- chaining and front field were printed as context and never set as goals, and both moved more than any pilot measure did. The reading offered is that one well-stated substitution reorganised the sentence and the rest followed the reorganisation rather than the instruction.

TWO OVERSHOOTS RECORDED AS SUCH, neither a regression. ', so ' at 0.0 % is below every source (0.1-0.4), so the licensed use went out with the fault, in both genres. PCP-003 carries ZERO possessives in 4,783 words against a stated band of 0.27-0.40 its and 0.50-0.96 their. Both are the possessive lesson repeating: a rule stated as a substitution is executed to exhaustion. Neither costs anything measurable here; both are the first things to watch in Track 2.

HEADROOM ANSWERED: splitting sentences cost PCP-003 3.2 points of pct_under_15 (20.4 -> 23.6 against a 32.0 ceiling) and cost PCR-003 nothing -- it fell 22.7 -> 19.5, because splitting a packed sentence into two 20-word sentences moves mass out of the long tail without creating short ones. Both rose on pct_over_40, away from the 3.0 floor. The plan predicted 5-8 points; the real figure is 3.2 and -3.2.

THE TWO ROUND-ONE FINDINGS ARE CLOSED. The round-one PCR-003 never stated the commercial scale (grep count 0); round two states it three times through V['commercial_scale_l'], first in the executive summary. The 'acidic variants is' agreement fault occurs once in round one and zero times in round two in either document.

THE NOTEBOOK: not extended. The page states that check_style.py and check_discourse.py ARE the method for clause packing, chaining, copula and front field, and that register_analysis.ipynb §13 is superseded for those measures because it applied 600/450 sentence caps the scripts make optional. The notebook stays the method for what the scripts do not cover. This is the second option the procedure allows, chosen because a notebook cell that shells out to a script is a second copy of the method, which is what produced the pilot's irreproducible 'before' values.

docs/results/README.md gains its row. TO FINISH THIS TASK: fold the owner's reading into the page's 'The owner's reading' section, verbatim and dated, and settle D1.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- [[2026-08-XX-register-round-two]] — `docs/results/2026-08-XX-register-round-two.md`
- [[README]] — `docs/results/README.md`
- `authoring/register_analysis.ipynb`
