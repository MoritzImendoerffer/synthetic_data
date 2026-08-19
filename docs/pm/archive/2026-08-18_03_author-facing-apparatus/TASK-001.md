---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-001
status: done
kind: mechanism
title: "Extend the measurement script with the frame counts, and prove it reproduces the results page"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-007", "PCR-003", "PCR-004", "PCR-005", "PCR-006", "PCR-008", "RA-001"]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-001 — Extend the measurement script with the frame counts, and prove it reproduces the results page

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

This is results §9's admission made good: the counts in §3 and §5.6 were session heredocs and are not reproducible until this task lands. Copy, do not import, the predecessor's script (decisions.measure_script_is_copied). Reproducing the results-page numbers exactly is the acceptance, and if a regex cannot reproduce one, say which and why in the outcome rather than moving the number. Sentence splitting and prose extraction come from authoring/check_style.py, never re-implemented. Rate = occurrences / sentences × 100, as the predecessor's SENT_PATTERNS block explains (PCR-003 has 67 `, which` in 66 sentences).

## Acceptance criteria

- [x] measure_apparatus.py exists as a copy of ../2026-08-18_02_register-track-d/measure_trackd.py plus a new block `frames` (per 100 sentences, on check_style.prose_from_qmd / prose_from_extract, sources first): `, which`; `<quantifier> of which` (none|all|both|each|some|most|one|two|three|several|many|neither|either of which); all trailing relatives (the union); `acts on|through`; `follows? from the`; `governs|sets <noun>`; `aggressive(ness)`; and the hollow-warrant frames `physical chemistry`, `confirms? the expectation`, `by the mechanism`, `consistent with the`
- [x] `uv run --extra discourse python $U/measure_apparatus.py --blocks frames $(ls pc_package/*.qmd)` reproduces the corpus column of docs/results/2026-08-18-track-d-stopped.md §3 exactly: `, which` 9.82 (513); quantifier-of-which 0.38 (20); all trailing relatives 11.39 (595); acts on/through 1.21 (63); follows from 0.23 (12); governs/sets 2.07 (108); aggressive 2 — and the four source columns 1.10/1.44/0.60/2.35 for `, which` and 0/0/0/0 for acts-through
- [x] a `--spans` switch counts role: mechanistic_warrant across authoring/rhetorical/*.spans.yaml and reports 26 in total, 6 carrying a flagged frame (behaves as | acts on/through | follows from | aggressiveness), naming the six span ids and their documents (two in PCR-005, the others in PCR-004 and PCR-008)
- [x] `uv run --extra discourse python $U/measure_apparatus.py --check-baseline $(ls pc_package/*.qmd)` still reproduces both committed baselines cell for cell and disagrees on exactly PCP-007, PCR-005, RA-001 and no other document (the same result the predecessor's script gives today)
- [x] the script accepts a section-sized file (any .qmd; MIN_SENTENCES is not applied by this script) — verified by running it on the EXCERPT file once TASK-002 creates it, or on a temporary copy of lines 747–876 of PCR-005 before then, and reading `, which` 15/59

## What was built

measure_apparatus.py is the predecessor's measure_trackd.py copied into this unit and extended with block five (`frames`) and `--spans`; it reads the two committed baselines from the predecessor unit rather than copying them.

`uv run --extra discourse python $U/measure_apparatus.py --blocks frames $(ls pc_package/*.qmd)` (saved as measure_frames_corpus.txt), corpus total over 20 documents, 5,226 sentences: `, which` 9.82 (513); <quantifier> of which 0.38 (20); `, where` 0.88 (46); `, whose` 0.31 (16); all trailing relatives 11.39 (595); acts on/through 1.21 (63); aggressive 0.04 (2). Sources: `, which` 1.10 / 1.44 / 0.60 / 2.35; acts-through 0 / 0 / 0 / 0. All of these reproduce results §3 exactly. The quantifier list reproduces 20 ONLY without numerals (one|two|three add 3 -> 23), and the page's own union 595 = 513+20+46+16 is exact only at 20, which is the corroboration.

TWO ROWS DO NOT REPRODUCE and are printed with the disagreement beside them (FRAMES_DISAGREE): `follows from the` reads 14 (0.27) against the page's 12 (0.23) — singular-only reads 10, no pattern reads 12; `governs / sets <noun>` reads 97 (1.86) against the page's 108 (2.07) — `governs` alone 67, `sets <determiner>` 30, no defensible pattern reads 108. The page's two numbers came from unsaved heredocs and are uncheckable; the script's are the ones with code behind them. Not tuned to the number.

`--spans`: 26 spans labelled mechanistic_warrant across authoring/rhetorical/*.spans.yaml; 7 carry a flagged frame — PCR-004-R05/R10/R17 (acts on / act on), PCR-005-R17 (behaves as), PCR-005-R24 (aggressive), PCR-008-R04 (behaves as), and a SEVENTH the results page's hand count of 6 did not list: PCR-006-R14, 'The surfaces behave as acid denaturation kinetics predict' — 'behave as <X> predicts' is a comparison, not the category-label frame, so it is printed and left to the reader. The acceptance said six; the script finds the six named plus this one, and says so.

`--check-baseline` on all 20 (saved as check_baseline_run.txt): style 408 cells compared, 39 disagreements; discourse 120 cells, 15 disagreements; every disagreement is in PCP-007 (15), PCR-005 (20) or RA-001 (19) and in no other document — the three Track D re-authored after the baseline. The RA-001 fixture rows fail for the same reason. ONE BUG FIXED IN THE COPY: the predecessor's TASK-007 commit (5433101) switched the style comparison to lookup-by-name and forgot the ' (human)' suffix the baseline header carries on the four source columns, so its --check-baseline has skipped all four sources as MISS since then (340 cells, 68 MISS lines) where its own TASK-002 outcome records 408. Run today, the predecessor's script prints exactly that. The copy looks the bare name up with the suffix and compares 408 with 0 MISS; the predecessor's file is left as the record it is.

Section-sized input: on a temporary copy of PCR-005 lines 747–876 the frames block reads `, which` 25.42 (15) of 59 sentences, all trailing relatives 28.81 (17). MIN_SENTENCES is not applied by this script.

## Documents it is about

- **PCP-007** — `pc_package/PCP-007_cex.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-004** — `pc_package/PCR-004_harvest.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`
- **PCR-006** — `pc_package/PCR-006_viral_inactivation.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`
- **RA-001** — `pc_package/RA-001_risk_assessment.qmd`

## Files it touched

- `.claude/work/2026-08-18_03_author-facing-apparatus/measure_apparatus.py`
