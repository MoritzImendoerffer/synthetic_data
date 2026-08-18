---
type: pm-task
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
task: TASK-009
status: done
kind: documentation
title: "Move the findings into docs, settle the decision, and rewrite or retire the proposal on the stopping rule's verdict"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-009 — Move the findings into docs, settle the decision, and rewrite or retire the proposal on the stopping rule's verdict

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-009.md in this work unit — numbered steps, code, commands and the output each must print. Follow it top to bottom.  THIS IS /ship's WORK and the plan leaves room for it; do not do it early.  THE VERDICT DECIDES THE SHAPE OF THE PROPOSAL. Two branches, both prepared here so /ship does not improvise: (a) stopping rule holds → the proposal becomes 'Track 2 — the remaining eighteen', with the budget from the pilot page and the round-two per-document re-anchoring counts, and D1 asks the owner whether Track 2 starts without another decision; (b) it does not → the proposal is rewritten to the target the owner's reading names, and the guide's-own-register hypothesis (decisions.guide_scope) is written up as its first candidate, with the numbers from exploration.md §4 (guide commentary 0 % initial connectives, ', so ' 1.5–11.5 %).  HANDOFF §3a is two tables ('Model / world-canon changes', 'Tooling changes'); everything here is tooling.  TASKS.md's list was six, then seven after round one (the discrepancy trap); these are eight and nine.  pm_notes.py archives the previous epic when ACTIVE_WORK changes; the _Archive.md row is /ship's, written before the notes move.

## Acceptance criteria

- [x] authoring/HANDOFF.md §3a 'Tooling changes' gains rows for: the advisory packing measures in check_style.py, check_discourse.py + the optional extra, brief §5d, and the guide's rule-as-substitution rewrite — each saying what it did
- [x] pc_package/TASKS.md 'Things that will catch you out' gains two: (a) an inline expression that yields a NAME must not be an agreeing subject; (b) the guide's own commentary is written in the register it forbids — verify against the sources, not against the guide's prose
- [x] CLAUDE.md's Voice bullet says the packing measures exist and are advisory, in one sentence, if TASK-003 has not already covered it
- [x] docs/ROADMAP.md's register row says what is now true; if Track 2 opens it names the eighteen and the per-document budget (~40 spans, explicit pdf render); if not, it names the next target from the owner's reading
- [x] docs/next/register-from-four-sources.md is rewritten to Track 2 alone (if the verdict is 'open') or to the new target (if 'stop'), or deleted if nothing remains; docs/next/README.md's row agrees
- [x] docs/pm/decisions/D1-track-two-on-the-verdict.md is settled with the owner's answer and status: settled
- [x] docs/pm/epic.md carries the shipped summary and docs/pm/_Archive.md gains this epic's row before the notes move
- [x] `docs/results/` page is linked from ROADMAP, README and the proposal or its successor

**Depends on:** [[TASK-008]]

## What was built

THE STOP BRANCH, taken because the project owner settled D1 on option B on 2026-08-18. Track D (the remaining eighteen) stays blocked; the three faults the owner's reading named are the next target.

authoring/HANDOFF.md §3a gains five rows: the round-two re-author in the model/world-canon table (44 quote instances re-anchored across the pair from 37 edited strings, against 80 in round one, because every table-row quote survives a re-author untouched; the curated layer needed 33 of its 35 spans re-cut and still carries 35), and four tooling rows -- the advisory packing measures (with the known gap written down: a single ', and ' joining two clauses is caught by neither the ', so ' count nor the 2+ coordinator count), check_discourse.py and its optional extra, brief §5d and the §1 scale line, and the guide's rule-as-substitution rewrite including the two extra ✓ blocks a line-by-line grep could not see.

pc_package/TASKS.md gains traps 8 and 9: a runtime-name expression must never be an agreeing subject, and the guide's own commentary is written in the register it forbids -- verify voice against refs/text/, never against the guide's prose, and in the exemplar only the QUOTES are source register.

CLAUDE.md: the Voice bullet now says the packing line exists and is advisory. Its page band was also corrected, in CLAUDE.md and TASKS.md, from 41-55 pp to 41-59 pp -- PCR-003 renders to 59 pages on flat prose and the same nine figures, so the old line had become false. That is the repository's own rule about status lines applied to itself.

docs/next/register-from-four-sources.md rewritten to four tracks: A, the three measures the reading named, all advisory and two of them regexes; B, the write-the-passive rule, which is the half of the passive finding no counter reaches; C, the guide's own register, held back in round two by owner decision and PROMOTED to first candidate by round two's own result; D, the eighteen, blocked on A-C. The proposal leads with the finding rather than the numbers: an author executes exactly what is measured and printed back, and leaves everything else where it was, including rules it has read. Two new open questions: whether measures come before the guide rewrite, and whether the next round should use a document other than the bioreactor pair, which the owner has now read three times.

docs/ROADMAP.md and docs/next/README.md rows rewritten to agree with it and with each other, both linking the results page. D1 is status: settled, waiting_on: —, with the option and the date. docs/pm/epic.md is status: shipped with the shipped paragraph; docs/pm/_Archive.md has the epic's row, written before the notes move as the file's own rule requires.

FINAL GATES, run after every documentation edit. make test 88 passed. make style 24 OK lines, 0 FAIL. build_ground_truth + validate_annex 20/20 valid. GROUNDING_STRICT_ANCHORS=1 check_grounding 2084/2084 quotes grounded across 20 annexes, 0 weak anchors. check_blank_repo.sh PASS on both halves. git diff outputs/ empty. The annex rebuild produced byte-identical files, so git status lists only documentation: CLAUDE.md, HANDOFF.md, TASKS.md, ROADMAP.md, next/README.md, the proposal, D1, epic.md, _Archive.md, the board and state.json. No rendered document and no annex changed in this task.

## Documents it is about

- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- [[README]] — `docs/results/README.md`
- [[HANDOFF]] — `authoring/HANDOFF.md`
- [[TASKS]] — `pc_package/TASKS.md`
- [[ROADMAP]] — `docs/ROADMAP.md`
- [[register-from-four-sources]] — `docs/next/register-from-four-sources.md`
- [[README]] — `docs/next/README.md`
- [[D1-track-two-on-the-verdict]] — `docs/pm/decisions/D1-track-two-on-the-verdict.md`
- [[epic]] — `docs/pm/epic.md`
- [[_Archive]] — `docs/pm/_Archive.md`
- `CLAUDE.md`
