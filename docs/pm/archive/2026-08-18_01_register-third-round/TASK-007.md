---
type: pm-task
epic: 2026-08-18_01_register-third-round
sprint: 2026-08-18_01_register-third-round
task: TASK-007
status: done
kind: documentation
title: "Move the findings into docs, and rewrite or retire the proposal on the verdict"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-18_01_register-third-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-007 — Move the findings into docs, and rewrite or retire the proposal on the verdict

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-007.md — the previous unit's TASK-009 procedure. THIS IS /ship's WORK. THE VERDICT DECIDES THE SHAPE: if the reading says 'no longer immediately obvious', Track D (the eighteen) opens and the proposal becomes Track C + Track D with the per-document budget from three measured rounds; if the reading names new faults, they become the next target and the proposal is rewritten to them, with Track C still the leading hypothesis (owner: measures first, then C). Prepare both shapes. STATUS LINES: re-check the '41-59 pp' band and any HANDOFF claim about span counts before writing them.

## Acceptance criteria

- [x] HANDOFF.md §3a gains rows for the two new check_style counts (with the regex-is-a-floor note), the passive + parser counts in check_discourse.py, brief §5d's three rows, the guide's write-the-passive rule, and PCR-003's third re-author with its re-anchoring count
- [x] pc_package/TASKS.md 'Things that will catch you out' gains item 10: a study, a design, a model or a process is never the AGENT of retain/carry/identify/select — the author manufactures one when avoiding a passive; verify against the sources' passive rate (54-60 %), a band
- [x] CLAUDE.md's Voice bullet mentions the two new advisory counts in the same sentence as the packing line (one clause), and the page band is re-checked against the new PCR-003 page count
- [x] docs/ROADMAP.md's register row says what is now true, links the round-three page, and names the next target from the owner's reading if there is one; docs/next/register-from-four-sources.md is rewritten to what remains (Track C and D, or the new target) or deleted; docs/next/README.md agrees
- [x] docs/pm/epic.md shipped; docs/pm/_Archive.md gains the row before the notes move; `uv run python scripts/pm_notes.py` shows 7 of 7
- [x] final gates from the checklist: make test, make style 24/0, annexes 20/20, strict grounding N/N with 0 weak anchors, check_blank_repo PASS, `git diff --stat outputs/` empty

**Depends on:** [[TASK-006]]

## What was built

Delivered 2026-08-18 by /ship --commit.

REPRODUCTION, the check that matters: the FULL rebuild was run, not the annex-only path, because the unit re-authored a .qmd -- `make clean && PATH="$PWD/.venv/bin:$PATH" make data figures corpus PY="uv run python"`, exit 0. Results: git diff --stat outputs/ EMPTY (no library drift in doe_*/effects_*); all 20 ground_truth/*.json rebuilt BYTE-IDENTICAL; the rendered TEXT of all 20 documents byte-identical to HEAD, compared through check_grounding.docx_text rather than by file hash. The 40 .docx/.pdf binaries differed only in embedded timestamps and were restored by name, never by directory.

GATES: make test 89 passed; make style 24 OK / 0 FAIL; check_style --selftest 4 of 4 human sources; check_blank_repo PASS; 20/20 annexes valid; GROUNDING_STRICT_ANCHORS=1 -> 2084/2084 quotes grounded across 20 annexes, 0 weak anchors, exit 0; check_render on PCR-003 OK with 0 missing glyphs.

TYPED NUMBERS: three in the re-authored document, all '95 %' -- the prediction/confidence level, which the numeral lint permits as a statistical convention. The annex builder's new strings are grounding quotes, not computed values; check_grounding fails immediately if the document stops saying them.

THREE STATUS CLAIMS WENT FALSE AND WERE CORRECTED, which is exactly what step 4 exists for:
  - CLAUDE.md and TASKS.md item 6 said DoE reports run '41-59 pp'. Re-measured from the fresh PDFs: 56, 51, 50, 44, 43, 41. The band is 41-56 pp. PCR-003 was the only 59 and is now 56.
  - CLAUDE.md's parenthetical said PCR-003 'reached 59 pp ... on the same nine figures'. Now 56 pp on ten figure labels.
  - The ROADMAP row said 'the next target is the three counted faults'. All three are cleared.

AND ONE CLAIM COULD NOT BE REPRODUCED. The proposal quoted the guide's commentary at 1.5 % ', so ' and 0 % initial connectives, 'measured 2026-08-17', by a method never saved to a file. Re-measured today over commentary only (blockquotes, code, tables and headings stripped): WRITING_GUIDE.md 3.77 % / 0.31 % / 10.38 % ', and '+clause; REGISTER_EXEMPLAR.md 6.80 % / 0.00 % / 10.88 %; CLAUDE.md 4.00 % / 1.33 % / 9.33 %; against sources at 0.1-0.4 / 3.7-6.1 / 1.1-3.4. The rewritten proposal carries the new table, says the old figure cannot be reproduced, and makes 'write the measurement as a script first' the first task of any Track C round -- the same repair TASK-001 had to make for the owner-reading counts.

MOVED: HANDOFF.md §3a gained one model row (round three: 22 of 177 quotes re-anchored, all 35 spans re-cut, 59 -> 56 pp, D-002 verbatim so the registries needed no edit) and three tooling rows (the two regex counts with the floor note, the passive/parser pair on one denominator with the band note and the 34.4 -> 35.4 denominator change, brief §5d plus the write-the-passive rule). TASKS.md gained item 10 -- a study, design, model or process is never the AGENT of retain/carry/identify/select -- ending on the round's own lesson, that the four search strings all returned 0 while one instance of the fault stood, because it matched no string anybody had written down. CLAUDE.md's voice bullet now names all five advisory counts and the passive band.

PROPOSAL REWRITTEN, NOT DELETED. Track A and Track B are closed on the reading; Track C and Track D remain, plus the two count-led candidates. The scope question -- Track C next, or the both-genres check this round gave up -- is written up as the owner's to set, with the argument for each side, because it is not the assistant's call.

docs/next/README.md, docs/ROADMAP.md, docs/pm/epic.md (status shipped, with what did NOT ship) and docs/pm/_Archive.md all agree with the above.

## Documents it is about

- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- [[HANDOFF]] — `authoring/HANDOFF.md`
- [[TASKS]] — `pc_package/TASKS.md`
- `CLAUDE.md`
- [[ROADMAP]] — `docs/ROADMAP.md`
- [[register-from-four-sources]] — `docs/next/register-from-four-sources.md`
- [[README]] — `docs/next/README.md`
- [[epic]] — `docs/pm/epic.md`
- [[_Archive]] — `docs/pm/_Archive.md`
- [[README]] — `docs/results/README.md`
