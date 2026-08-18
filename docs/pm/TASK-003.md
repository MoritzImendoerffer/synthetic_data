---
type: pm-task
epic: 2026-08-18_01_register-third-round
sprint: 2026-08-18_01_register-third-round
task: TASK-003
status: todo
kind: mechanism
title: "Print the three new measures in brief \u00a75d, and add the write-the-passive rule and the two search strings to the guide"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-18_01_register-third-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-003 — Print the three new measures in brief §5d, and add the write-the-passive rule and the two search strings to the guide

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-003.md. THE HYPOTHESIS UNDER TEST is round two's own: an author executes what is measured and printed back and leaves everything else where it was. So the brief prints all three numbers AND states each rule as a substitution with the strings to search for; check_style prints two of the three back on every render (the passive needs the extra, hence the brief). TWO OF THE THREE RULES ALREADY EXIST IN WORDS: §2d line 161 forbids ', and …' carrying a second claim; §4b line 563 says the sources almost never build 'not X but Y'; §4b line 581 says passive is fine and the sources use it heavily. Round two proved an unmeasured rule is not a rule. Do not restate them at length — cross-reference and add the search strings and the numbers. TRACK B'S RULE goes beside Correction 0 because both are the same failure: the author supplies a subject/agent the fact does not have. Correction 0 covers a runtime NAME as subject; this covers a STUDY as agent. The three 'screening retained' sentences are at PCR-003 lines 494, 915, 1588 (exploration §2) — quote ONE as the ✗, dated. THE ✓ BLOCK SCAN: previous unit's TASK-002 found two ✓ blocks teaching ', so ' that a line grep missed. Run the same block scan for ', and '+opener and ', not ' before finishing; the guide's own commentary is out of scope (owner: Track C later) but its ✓ blocks are not. EXEMPLAR QUOTES must be verbatim in refs/text/, inside one page, and pass check_exemplar_quotes.py; the attribution must name exactly one SRC. Search the extracts for 'were retained', 'was carried forward', 'were identified as', 'were selected' near 'parameters'/'factors'/'design'.

## Acceptance criteria

- [ ] `uv run --extra discourse python authoring/build_brief.py PCR-003 PCP-003` emits §5d with three new rows: "mid-sentence `, and ` joining a second clause (%) — regex, a floor" (target ≤ 3.4), "mid-sentence `, not ` (%) " (target ≤ 0.2), and 'sentences with a passive construction (%) — BAND 54–60, never a floor', each with the four source columns and the document's own value; PCR-003 shows 22.6 / 4.3 / 34.4 and PCP-003 18.2 / 0.0 / 54.7; without spaCy the passive row reads 'not measured — uv sync --extra discourse' and the two regex rows still print
- [ ] §5d's rules list gains two entries stated as substitutions: (a) a second independent clause after ', and ' becomes its own sentence — search the draft for ', and the', ', and this', ', and both', ', and it', ', and each'; (b) where the sources would write a passive, write the passive: a study, a design, a model or a process is never the AGENT of retain, carry, identify, select or show — search the draft for 'screening retained', 'the design carries', 'the model identifies'
- [ ] grep for '> ✓' or '✗' in the emitted §5d returns nothing (no generated example prose)
- [ ] WRITING_GUIDE.md §2d, directly under Correction 0's runtime-noun paragraph (line ~190), gains the write-the-passive rule with the owner's example as ✗ ('The 4 factors that screening retained then entered …', dated 2026-08-18) and a ✓ that keeps every fact and uses a passive ('The four factors retained from screening then entered …'); the paragraph names the verbs that manufacture an agent and says the passive is the sources' default for them (§4b line 581 already says so — cross-reference it, do not restate it)
- [ ] §2d's substitution paragraph names ', and ' + a second clause and ', not ' as strings to search a draft for, beside ', so ' (line ~164); §4a's table gains three diagnostic rows with the per-source values from TASK-001/002 (', and '+clause 3.4 / 1.1 / 1.3 / 3.1; ', not ' 0.2 / 0.0 / 0.1 / 0.0; passive 54.3 / 59.8 / 59.6 / 58.4) marked not gated, and the note under it says the passive row is a band
- [ ] no ✓ block anywhere in the guide contains mid-sentence ', and ' followed by a clause opener or mid-sentence ', not ' — check by the block-level scan TASK-002 of the previous unit used, extended to the two new patterns; report the count (expected 0)
- [ ] REGISTER_EXEMPLAR.md gains a sub-heading under 'The step after the full stop' with at least three verbatim source sentences in which the passive carries a study/design/model as patient ('were retained', 'was carried forward', 'were identified'), from at least two sources; `uv run python authoring/check_exemplar_quotes.py` passes with the new count stated
- [ ] `make style PY="uv run python"` passes 24 OK / 0 FAIL; `bash authoring/check_blank_repo.sh` PASS

**Depends on:** [[TASK-001]], [[TASK-002]]

## Documents it is about

- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `authoring/build_brief.py`
- [[WRITING_GUIDE]] — `authoring/WRITING_GUIDE.md`
- [[REGISTER_EXEMPLAR]] — `authoring/REGISTER_EXEMPLAR.md`
