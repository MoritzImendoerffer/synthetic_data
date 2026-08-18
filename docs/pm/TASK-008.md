---
type: pm-task
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
task: TASK-008
status: done
kind: measurement
title: "Measure round two against rounds zero and one with one method, apply the stopping rule, and record the owner's reading"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-008 — Measure round two against rounds zero and one with one method, apply the stopping rule, and record the owner's reading

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-008.md in this work unit — numbered steps, code, commands and the output each must print. Follow it top to bottom.  ONE METHOD FOR ALL THREE POINTS. The pilot's plan quoted chaining 'before' values (30.0 / 37.2) that did not reproduce (31.0 / 35.1) because two runs measured differently. Measure round zero, one and two in one invocation each of check_style.py --compare and check_discourse.py, and quote only those.  THE STOPPING RULE IS FIXED IN ADVANCE — it is in decisions.stopping_rule_edges and in the proposal; do not move an edge after seeing the number. If a number sits within measurement noise of an edge, say so and let the owner decide, but write the plan's edge down first.  THE OWNER'S READING IS THE HUMAN CHECK (owner decision 3). Ask for it after TASK-007, on the rendered pdf, before this page is finished, and quote it. If the owner reads it as still obviously machine-written, what they quote is the next unit's target — record it as such, verbatim, the way exploration.md §1 did.  THE HYPOTHESIS UNDER TEST is stated on the pilot page: does giving the author the measurement change the outcome, when giving them examples did not? Answer it in one sentence, per document, per measure.  ALSO REPORT the two round-one findings: does the new PCR-003 state the commercial scale, and did any inline name land as an agreeing subject.

## Acceptance criteria

- [x] the results page has a table per measure with SEVEN columns — PDA TR 60, A-Mab, ISPE TT, ISPE PV, then round zero (b0361f1, .claude/work/2026-08-16_01_register-from-four-sources/pre-rewrite/), round one (f06f1a7, this unit's pre-rewrite/), round two (pc_package/) — for BOTH documents, every cell with its denominator
- [x] measures: mid-sentence ', so ' %, sentence-initial connective %, 2+ coordinators %, connective repertoire (rate and distinct), topic chaining %, copula %, front field %, 'its'/'their'/'it is' per 1000 words, and the register gate's own five length numbers — all produced by check_style.py --compare and check_discourse.py (with and without --cap stated), never quoted from this plan or from the pilot page
- [x] the stopping rule from decisions.stopping_rule_edges is applied line by line and the verdict is one sentence: 'Track 2 opens' or 'stop and change the target', with the line that decided it
- [x] the owner's reading is recorded: whether the re-authored pair is still immediately recognisable as machine-written, and the sentences the owner quotes as giving it away — as a section, verbatim, dated; the page says the reading is not blind and why that was accepted
- [x] the register gate headroom question is answered again: pct_under_15 and pct_over_40 for both documents against the band and the four sources
- [x] if any measure moved backwards, the page names the substitution that paid for it, counted (round one's model: 25 possessives → 23 copulas)
- [x] docs/results/README.md gains a row saying why the run happened
- [x] register_analysis.ipynb gains a §14 that reproduces the tables from the two scripts, or the page states that the scripts alone are the method and the notebook is superseded for these measures

**Depends on:** [[TASK-007]]

## What was built

COMPLETE. The owner's reading was given on 2026-08-18 and is recorded verbatim. docs/results/2026-08-18-register-round-two.md carries every table the acceptance asks for, with seven columns per measure (four sources, three rounds) for both documents and a denominator on every rate. The owner's reading is recorded verbatim and dated, with the note that it is not blind and why that was accepted.

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

THE OWNER'S READING, 2026-08-18: still immediately clear, on the FIRST sentence of the report. Three faults named, none of them the packing fault this round targeted, none measured before today: (1) the balanced two-clause sentence -- a statement, comma, 'and', then a second independent clause that restates or qualifies it -- which the owner calls 'a typical way of formulating sentences which seems to be intrinsic to claude models'; (2) a false agency, 'the 4 factors that screening retained', with the diagnosis 'you are trying to avoid passive terms at all costs. As a result the writing style sounds a bit unnatural'; (3) the contrastive tail '... rest on it, not on the near saturated screening fit'.

COUNTED AFTER THE READING (measure_owner_reading.txt; a reader found it, then the count confirmed it):
  ', and ' + clause opener:  sources 1.1-3.4 %   PCP-003 20.8 -> 17.7 -> 18.2 %   PCR-003 24.9 -> 21.0 -> 22.6 %   -- SIX TO TWENTY TIMES the source rate and UNMOVED by this round; it rose slightly in both. check_style counts mid-sentence ', so ' and sentences with TWO OR MORE coordinators, so a sentence with exactly one ', and ' joining two clauses is caught by neither. WRITING_GUIDE §2d already forbids it in words; the author executed the ', so ' half, which is the half a printed number made checkable.
  ', not ' contrastive tail:  sources 0.0-0.2 %   PCR-003 0.0 -> 0.0 -> 4.3 % (18 sentences) -- A REGRESSION THIS ROUND CREATED. §4b already says the sources almost never build 'not X but Y'; nothing measures it. Likely mechanism: the round's own substitution moved the contrast out of ', so ' and into ', not'. The exploration predicted escape routes and listed ', and', '; ' and ', which'; this is one nobody listed.
  passive constructions:  sources 54.3-59.8 %   PCP-003 70.8 -> 58.0 -> 54.7 % (inside the band)   PCR-003 44.1 -> 41.6 -> 34.4 % (twenty points below every source, falling every round). The cost is not only tonal: avoiding a passive forces an agent, and where there is none the author invents one, which is exactly the 'screening retained' error. §4b already says the sources use the passive heavily.

WHAT THIS DOES TO THE HYPOTHESIS, and it is the most useful thing on the page: every measure printed back to the author moved, and the three faults the owner named are precisely the three that were not printed back -- two of them forbidden by rules the guide already states in words. So the finding is narrower and less comfortable than 'telling the author the number works': an author executes exactly what is measured and printed, and leaves everything else where it was, INCLUDING RULES IT HAS READ. The ceiling on this approach is the coverage of the measures.

VERDICT. The stopping rule holds on every line, which settles D1's first half. Under option A (numbers decide) Track 2 opens now. Under option B (the plan's assumption) the reading blocks it and the three faults become the next target. The page states both and does not choose; D1 is the owner's and is updated with the reading, the counts and the argument on each side.

The page also names what the next round would measure: ', and ' + clause opener and ', not ' beside the packing line in check_style.py (printed, gated by nothing), and the passive rate in check_discourse.py as a BAND not a floor -- the plan is inside it and the report is under it, so a floor would push the plan the wrong way. The false agency is not reachable by any of them and belongs in the guide beside the runtime-noun rule.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- [[2026-08-XX-register-round-two]] — `docs/results/2026-08-XX-register-round-two.md`
- [[README]] — `docs/results/README.md`
- `authoring/register_analysis.ipynb`
