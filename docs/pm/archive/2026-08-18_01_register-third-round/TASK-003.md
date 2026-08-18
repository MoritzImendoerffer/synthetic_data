---
type: pm-task
epic: 2026-08-18_01_register-third-round
sprint: 2026-08-18_01_register-third-round
task: TASK-003
status: done
kind: mechanism
title: "Print the three new measures in brief \u00a75d, and add the write-the-passive rule and the two search strings to the guide"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-18_01_register-third-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-003 — Print the three new measures in brief §5d, and add the write-the-passive rule and the two search strings to the guide

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-003.md. THE HYPOTHESIS UNDER TEST is round two's own: an author executes what is measured and printed back and leaves everything else where it was. So the brief prints all three numbers AND states each rule as a substitution with the strings to search for; check_style prints two of the three back on every render (the passive needs the extra, hence the brief). TWO OF THE THREE RULES ALREADY EXIST IN WORDS: §2d line 161 forbids ', and …' carrying a second claim; §4b line 563 says the sources almost never build 'not X but Y'; §4b line 581 says passive is fine and the sources use it heavily. Round two proved an unmeasured rule is not a rule. Do not restate them at length — cross-reference and add the search strings and the numbers. TRACK B'S RULE goes beside Correction 0 because both are the same failure: the author supplies a subject/agent the fact does not have. Correction 0 covers a runtime NAME as subject; this covers a STUDY as agent. The three 'screening retained' sentences are at PCR-003 lines 494, 915, 1588 (exploration §2) — quote ONE as the ✗, dated. THE ✓ BLOCK SCAN: previous unit's TASK-002 found two ✓ blocks teaching ', so ' that a line grep missed. Run the same block scan for ', and '+opener and ', not ' before finishing; the guide's own commentary is out of scope (owner: Track C later) but its ✓ blocks are not. EXEMPLAR QUOTES must be verbatim in refs/text/, inside one page, and pass check_exemplar_quotes.py; the attribution must name exactly one SRC. Search the extracts for 'were retained', 'was carried forward', 'were identified as', 'were selected' near 'parameters'/'factors'/'design'.

## Acceptance criteria

- [x] `uv run --extra discourse python authoring/build_brief.py PCR-003 PCP-003` emits §5d with three new rows: "mid-sentence `, and ` joining a second clause (%) — regex, a floor" (target ≤ 3.4), "mid-sentence `, not ` (%) " (target ≤ 0.2), and 'sentences with a passive construction (%) — BAND 54–60, never a floor', each with the four source columns and the document's own value; PCR-003 shows 22.6 / 4.3 / 34.4 and PCP-003 18.2 / 0.0 / 54.7; without spaCy the passive row reads 'not measured — uv sync --extra discourse' and the two regex rows still print
- [x] §5d's rules list gains two entries stated as substitutions: (a) a second independent clause after ', and ' becomes its own sentence — search the draft for ', and the', ', and this', ', and both', ', and it', ', and each'; (b) where the sources would write a passive, write the passive: a study, a design, a model or a process is never the AGENT of retain, carry, identify, select or show — search the draft for 'screening retained', 'the design carries', 'the model identifies'
- [x] grep for '> ✓' or '✗' in the emitted §5d returns nothing (no generated example prose)
- [x] WRITING_GUIDE.md §2d, directly under Correction 0's runtime-noun paragraph (line ~190), gains the write-the-passive rule with the owner's example as ✗ ('The 4 factors that screening retained then entered …', dated 2026-08-18) and a ✓ that keeps every fact and uses a passive ('The four factors retained from screening then entered …'); the paragraph names the verbs that manufacture an agent and says the passive is the sources' default for them (§4b line 581 already says so — cross-reference it, do not restate it)
- [x] §2d's substitution paragraph names ', and ' + a second clause and ', not ' as strings to search a draft for, beside ', so ' (line ~164); §4a's table gains three diagnostic rows with the per-source values from TASK-001/002 (', and '+clause 3.4 / 1.1 / 1.3 / 3.1; ', not ' 0.2 / 0.0 / 0.1 / 0.0; passive 54.3 / 59.8 / 59.6 / 58.4) marked not gated, and the note under it says the passive row is a band
- [x] no ✓ block anywhere in the guide contains mid-sentence ', and ' followed by a clause opener or mid-sentence ', not ' — check by the block-level scan TASK-002 of the previous unit used, extended to the two new patterns; report the count (expected 0)
- [x] REGISTER_EXEMPLAR.md gains a sub-heading under 'The step after the full stop' with at least three verbatim source sentences in which the passive carries a study/design/model as patient ('were retained', 'was carried forward', 'were identified'), from at least two sources; `uv run python authoring/check_exemplar_quotes.py` passes with the new count stated
- [x] `make style PY="uv run python"` passes 24 OK / 0 FAIL; `bash authoring/check_blank_repo.sh` PASS

**Depends on:** [[TASK-001]], [[TASK-002]]

## What was built

The three measures reach the author, and the two rules are stated as substitutions.

BRIEF (build_brief.py). §5d gained four rows, not three: the two regex rows from TASK-001 in the check_style block, and the passive plus the parser and-clause in the check_discourse block. `uv run --extra discourse python authoring/build_brief.py PCR-003 PCP-003` emits, in the document column:

  PCR-003: ', and ' regex 22.6 | ', not ' 4.3 | passive 35.4 (146/413) | ', and ' parser 25.4 (105/413)
  PCP-003: ', and ' regex 18.2 | ', not ' 0.0 | passive 55.2 (111/201) | ', and ' parser 24.9 (50/201)

DEVIATION, from the plan's own decision. The acceptance line asked for 34.4 and 54.7; those are round two's figures over every sentence. The decision `one_denominator` in this state file settles it the other way and /plan measured the consequence itself: on check_discourse's denominator PCR-003 is 35.4 (146/413). PCP-003's analogue is 55.2 (111/201) against round two's 54.7 (111/203) — the same 111 sentences. The §5d caption now says the parser rows divide by the sentences that have a root and a subject, so the passive reads a few tenths above the round-two page for the same text. TASK-006's page has to footnote this once.

The degrade row reads `topic chaining / copula / front field / passive / ', and ' parser | ... | not measured — uv sync --extra discourse`, and both regex rows still print without the extra (verified on a base `uv sync`; the brief built at 29,016 chars against 29,887 with it). No generated example prose: '> ✓' and '✗' both count 0 inside §5d for both documents. `bash authoring/check_blank_repo.sh` -> PASS.

The rules list gained the two substitutions with their search strings: `, and the` / `, and this` / `, and both` / `, and it` / `, and each` / `, and none`, and `screening retained` / `the design carries` / `the study selected` / `the model identifies`.

GUIDE (WRITING_GUIDE.md). §2d's substitution paragraph now names all three strings to search for, and a second paragraph gives the two new rates with the dates and says check_style prints all four. The write-the-passive rule sits after Correction 0's last example pair — the plan said to put it after the runtime-noun paragraph, but a ✗/✓ pair follows that paragraph and the rule would have split Correction 0 in half. It carries the owner's sentence as the ✗, dated 2026-08-18 and quoted from the rendered docx: "The 4 factors that screening retained then entered a face centred response surface design of 28 runs, and the remaining 4 parameters were assessed one at a time." The ✓ keeps the digits, because the counts are `{python}` values the author cannot spell out.

DEVIATION, measured before writing. The plan's verb list was "retain, carry, identify, select or show". Counted in the four sources on 2026-08-18: "Results showed" / "studies showed" / "the data shows" / "The analysis shows" occur about twenty times, and "the assessment identified" / "studies identified" seven times. "retained", "carried" and "selected" with a study, design, model or results as subject occur ZERO times. A rule saying a study is never the agent of "show" would be a rule all four sources break, which is the calibration failure this repository fixes everywhere else. The rule therefore names retain, carry forward and select, and a following paragraph states the exception with those counts: evidence may be the subject of a verb that reports what it shows, a study may not be the subject of a verb that reports what a person decided. All four search strings from the acceptance are kept.

§4a gained three diagnostic rows. The two regex rows carry the acceptance's values (3.4 / 1.1 / 1.3 / 3.1 and 0.2 / 0.0 / 0.1 / 0.0). The passive row carries 56.9 / 64.0 / 62.9 / 60.1, which is what `check_discourse.py` prints uncapped, and the note gives the acceptance's 54.3 / 59.8 / 59.6 / 58.4 as the same sources counted over every sentence and tells the author to compare against the row using the same command. Printing 54-60 above columns the tool reads as 57-64 would have been a number with nothing behind it, which is the defect TASK-001 existed to remove.

THE ✓-BLOCK SCAN found four hits in WRITING_GUIDE.md and none in REGISTER_EXEMPLAR.md; all four were pre-existing ✓ blocks modelling the pattern the guide now forbids, at lines 126, 191, 201 and 395. Two of them sit under commentary that counts their sentences ("Three sentences, three lexical main verbs"; "Three sentences, one step each"), so those two were re-cut to keep the count true: an appositive and a "with" phrase in the first, and "the weakest case to watch at scale is X (p = Y)" merging the third sentence of Correction 0 while keeping the runtime name after "is", which is what its commentary is about. The other two became a compound predicate and a full stop. Final scan: 0 and 0.

EXEMPLAR. New sub-heading "The study is the patient, not the agent" under "The step after the full stop", with five verbatim quotes from three sources: A-Mab p. 122, p. 184 and p. 153; PDA TR 60 printed p. 75 / extract p. 83; ISPE Practical Implementation printed p. 152 / extract p. 154. Each was tested against the checker's normaliser before it was written in. The note says where the study went in each one and gives the active-voice evidence verbs as the contrast. `uv run python authoring/check_exemplar_quotes.py`: 133 quotes checked, 0 failed, up from 128.

Gates. make style: exit 0, 24 OK, 0 FAIL. check_style --selftest: 4 of 4. make test: 89 passed. check_blank_repo.sh: PASS. No .qmd was touched.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `authoring/build_brief.py`
- [[WRITING_GUIDE]] — `authoring/WRITING_GUIDE.md`
- [[REGISTER_EXEMPLAR]] — `authoring/REGISTER_EXEMPLAR.md`
