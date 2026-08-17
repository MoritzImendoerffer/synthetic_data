---
type: pm-task
epic: 2026-08-16_01_register-from-four-sources
sprint: 2026-08-16_01_register-from-four-sources
task: TASK-004
status: done
kind: mechanism
title: "Add the moves catalogue to REGISTER_EXEMPLAR.md"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCMP-001", "PCP-003", "PTP-001"]
---

> [!warning] Generated from `.claude/work/2026-08-16_01_register-from-four-sources/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-004 — Add the moves catalogue to REGISTER_EXEMPLAR.md

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

MOSTLY TRANSCRIPTION. mined-patterns.md in this work unit holds the seven patterns with their examples, and 24 of 25 quotes were already verified verbatim against refs/text/. The seven: (1) the frame comes before the subject; (2) the main verb names the event; (3) concede first, then commit; (4) a finding is reported by a verb with the qualification riding along; (5) modality carries the risk posture; (6) the author manages the reader; (7) state the scope you are not covering.

THE ONE THING TO ADD that mining could not supply: plan-genre passages. Neither previously committed source is a plan, and 10 of the 20 corpus documents are plans (eight PCP-00N, PTP-001, PCMP-001). ISPE Technology Transfer is the only plan-shaped source and the owner has now permitted quoting it. Mine it the same way - scratchpad/mine.py in this unit is the tool, and register_analysis.ipynb section 10 shows the pattern predicates. Prioritise passages that commit, permit and condition, because that is the measured gap: 'should' is 7.3 per 1000 words in ISPE TT and 0.0 in every corpus document, while PCP-003 answers with 'will' at 19.7 against a human 2.0-3.3.

THE TRAP. Run check_exemplar_quotes.py rather than trusting the mining. One of the 25 mined quotes failed the verbatim check because it spans a page break, which prose_from_extract joins across the running header while the raw file does not contain it contiguously. It was swapped rather than kept. A mined sentence can look verbatim and be an artifact of the extractor.

FILE SHAPE. REGISTER_EXEMPLAR.md is 789 lines of verbatim passages arranged by reporting job. The catalogue is an addition in that same style, not a new section type. Never take a quote from a pc_package/*.qmd: that self-reference loop is what forced all 20 documents to be re-authored once already.

## Acceptance criteria

- [x] seven patterns from mined-patterns.md, each with three to five verbatim examples
- [x] examples drawn from at least three of the four sources, with ISPE Technology Transfer supplying the plan-genre passages
- [x] uv run python authoring/check_exemplar_quotes.py passes on every added quote
- [x] the file's arrangement by 'the job each passage does' is preserved
- [x] no corpus document is a source for any quote

**Depends on:** [[TASK-001]], [[TASK-003]]

## What was built

REGISTER_EXEMPLAR.md gained Part 3, 'The argument moves': the seven mined patterns as sections 16 to 22, continuing the file's numbering and its arrangement by the job each passage does. 32 new quotes take the file from 88 to 120. check_exemplar_quotes.py reports 120 quotes checked, 0 failed.

Per pattern: 16 frame before the subject (5), 17 the main verb names the event (5), 18 concede first then commit (5), 19 a finding reported by a verb (4), 20 modality carries the risk posture (5), 21 the author manages the reader (4), 22 state the scope you are not covering (4).

Sources across the 32: A-Mab 16, ISPE Technology Transfer 9, PDA TR 60 4, ISPE Practical Implementation 3. All four are represented, and ISPE TT supplies 3 of the 5 modality passages, which is the plan-genre gap the task was really about.

THE TRAP FIRED TWICE, both on quotes mined-patterns.md presented as verified:
  - The PDA concession quote ends '...material attributes' in mined-patterns. The source ends '...material attributes (1).' with a citation marker. Dropping it made the quote a paraphrase. Restored.
  - The PDA readiness-assessment quote spans the page 39/40 break. Between the halves the extract carries the DRM line, the page marker, a bare page number, the copyright line AND a stray \x08 control character that BOILER does not strip, so it cannot match. Swapped for two clean PDA sentences, per the plan. Worth knowing for later: check_exemplar_quotes.py's norm() strips PDF artifacts but not control characters, so any quote spanning a PDA page break is currently unusable. That is a checker fix, not an exemplar fix, and it was left alone.

FOUR PROSE CLAIMS IN MY OWN NOTES WERE WRONG AND WERE RE-MEASURED. mined-patterns.md's figures came from four documents and two sources, and do not survive the whole corpus or the corrected page ranges:
  - 'should is 0.0 in every corpus document' is false. It is 0.23 per 1000 words, 27 occurrences in 119,000 words, and 12 of 20 documents never use it. Eight do.
  - 'should runs at 7.3 in ISPE TT' is 11.5 over the verified body range pp.30-96.
  - 'we/our, Note that and For example are all zero in the corpus': the first two are zero, but 'For example' occurs once.
  - One note misquoted the A-Mab worst-case sentence by dropping 'bioreactor'.
All 13 numbers now in Part 3 were re-measured and match: should 11.5 / 11.2 / 0.23, may 7.9 / 7.8 / 0.13, PCP-003 will 19.7, For example x1, we/our 0, Note that 0, 119k corpus words, 12 documents.

HEADER REWRITTEN. The file said 'one of the two published human documents'. It now lists four, names ISPE TT as the closer model for a plan and ISPE PV as the longest-sentenced, and gives the printed-to-extract page offsets: A-Mab 0, PDA TR 60 8, both ISPE guides 2, each verified against the guides' own page furniture.

Gates: check_exemplar_quotes.py 120/120; make style exit 0 (4 sources + 20 documents OK, 0 FAIL); make test 85 passed. No document changed, so no annex was touched.

ALSO CORRECTED: authoring/HANDOFF.md lines 191, 197 and 207, which TASK-002 flagged as stale. All 'two sources' claims in shipped documentation are now gone; the remaining ones are in docs/next/register-from-four-sources.md and the work unit's exploration.md, where they correctly describe what was measured at the time.

## Documents it is about

- **PCMP-001** — `pc_package/PCMP-001_master_plan.qmd`
- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PTP-001** — `pc_package/PTP-001_transfer.qmd`

## Files it touched

- [[REGISTER_EXEMPLAR]] — `authoring/REGISTER_EXEMPLAR.md`
