---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-001
status: todo
kind: mechanism
title: "Extend the measurement script with the frame counts, and prove it reproduces the results page"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-001 — Extend the measurement script with the frame counts, and prove it reproduces the results page

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

This is results §9's admission made good: the counts in §3 and §5.6 were session heredocs and are not reproducible until this task lands. Copy, do not import, the predecessor's script (decisions.measure_script_is_copied). Reproducing the results-page numbers exactly is the acceptance, and if a regex cannot reproduce one, say which and why in the outcome rather than moving the number. Sentence splitting and prose extraction come from authoring/check_style.py, never re-implemented. Rate = occurrences / sentences × 100, as the predecessor's SENT_PATTERNS block explains (PCR-003 has 67 `, which` in 66 sentences).

## Acceptance criteria

- [ ] measure_apparatus.py exists as a copy of ../2026-08-18_02_register-track-d/measure_trackd.py plus a new block `frames` (per 100 sentences, on check_style.prose_from_qmd / prose_from_extract, sources first): `, which`; `<quantifier> of which` (none|all|both|each|some|most|one|two|three|several|many|neither|either of which); all trailing relatives (the union); `acts on|through`; `follows? from the`; `governs|sets <noun>`; `aggressive(ness)`; and the hollow-warrant frames `physical chemistry`, `confirms? the expectation`, `by the mechanism`, `consistent with the`
- [ ] `uv run --extra discourse python $U/measure_apparatus.py --blocks frames $(ls pc_package/*.qmd)` reproduces the corpus column of docs/results/2026-08-18-track-d-stopped.md §3 exactly: `, which` 9.82 (513); quantifier-of-which 0.38 (20); all trailing relatives 11.39 (595); acts on/through 1.21 (63); follows from 0.23 (12); governs/sets 2.07 (108); aggressive 2 — and the four source columns 1.10/1.44/0.60/2.35 for `, which` and 0/0/0/0 for acts-through
- [ ] a `--spans` switch counts role: mechanistic_warrant across authoring/rhetorical/*.spans.yaml and reports 26 in total, 6 carrying a flagged frame (behaves as | acts on/through | follows from | aggressiveness), naming the six span ids and their documents (two in PCR-005, the others in PCR-004 and PCR-008)
- [ ] `uv run --extra discourse python $U/measure_apparatus.py --check-baseline $(ls pc_package/*.qmd)` still reproduces both committed baselines cell for cell and disagrees on exactly PCP-007, PCR-005, RA-001 and no other document (the same result the predecessor's script gives today)
- [ ] the script accepts a section-sized file (any .qmd; MIN_SENTENCES is not applied by this script) — verified by running it on the EXCERPT file once TASK-002 creates it, or on a temporary copy of lines 747–876 of PCR-005 before then, and reading `, which` 15/59

## Documents it is about

- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `.claude/work/2026-08-18_03_author-facing-apparatus/measure_apparatus.py`
