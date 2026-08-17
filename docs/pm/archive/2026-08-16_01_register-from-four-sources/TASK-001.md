---
type: pm-task
epic: 2026-08-16_01_register-from-four-sources
sprint: 2026-08-16_01_register-from-four-sources
task: TASK-001
status: done
kind: mechanism
title: "Extract all four sources, each with its own boilerplate filter"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
---

> [!warning] Generated from `.claude/work/2026-08-16_01_register-from-four-sources/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-001 — Extract all four sources, each with its own boilerplate filter

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

WHERE. scripts/extract_sources.py defines SRC as a dict of {key: filename} at about line 30, currently two entries. The PDFs sit in $SYNTHETIC_DATA_SOURCES, default /home/moritz/Nextcloud/Datasets/synthetic_data/source_documents. Add: 'ispe_pv': '2023-ispe-good-practice-guide-practical-implementation-of-the-lifecycle-approach-to-process-validation.pdf' (208 pages) and 'ispe_tt': '2023-ispe-good-practice-guide-technology-transfer-(third-edition).pdf' (152 pages). The script already skips a missing file with a message, so a machine without the sources still runs.

THE FILTER. authoring/check_style.py:prose_from_extract (about line 153) holds a hand-written boilerplate list that is currently PDA-specific and A-Mab-specific: it drops lines containing 'Licensed to', 'Technical Report No', '(c) 20', 'CMC Biotech Working Group', 'Case Study A-Mab'. Extend it, or make it dispatch per source key. The ISPE strings to drop are: 'Downloaded from', 'For personal use only', 'No other uses without permission', 'For individual use only', 'Copyright ISPE', 'guidance-docs.ispe.org'. Two running headers also survive and should go: 'Practical Implementation of the Lifecycle Approach' and 'Technology Transfer'.

WHY IT MATTERS. Unfiltered, the ISPE measurement is not merely noisy, it is wrong: 300 of 470 sentences under 15 words were the same four watermark lines repeated on every page, which pushed 'under 15 words' to 37-41 % against a human band of 15-32 %. Filtered, the same document sits at 19.5 %. Section 1b of register_analysis.ipynb reproduces this and is the fastest way to check your filter.

EXEMPLAR CHECKER. authoring/check_exemplar_quotes.py holds SRC as a dict of {display name: path} near line 22 and a BOILER regex list near line 29. Both need the two new sources, or TASK-004's ISPE quotes cannot be verified and make style will fail.

DO NOT commit the PDFs. .gitignore already guards that; only the .txt extracts are committed.

## Acceptance criteria

- [x] uv run python scripts/extract_sources.py reports four sources, not two
- [x] refs/text/ holds ispe_tt.txt and ispe_pv.txt beside amab.txt and pda60.txt
- [x] prose_from_extract drops the ISPE per-page DRM footer: on ISPE TT pages 30-140, sentences under 15 words fall from 41.2 % to about 19.5 %, with roughly 330 boilerplate lines dropped
- [x] check_exemplar_quotes.py SRC carries all four sources and its BOILER list carries the ISPE footer and running headers
- [x] make style PY="uv run python" still passes (it calls check_exemplar_quotes.py)

## What was built

scripts/extract_sources.py now names four PDFs and reports four extractions; refs/text/ gained ispe_tt.txt (152 pages) and ispe_pv.txt (208 pages) beside the two committed extracts, which re-extracted byte-identically.

check_style.py's boilerplate filter moved out of prose_from_extract into two module-level constants. EXTRACT_BOILER holds substrings that cannot occur inside a sentence, so the six ISPE DRM strings joined the five PDA/A-Mab ones. EXTRACT_HEADERS holds the running headers, matched as a WHOLE LINE, because 'Technology Transfer' occurs 217 times in ISPE TT and only 140 of those are the header; a substring rule would have deleted real prose.

Effect on ISPE TT pp.30-140, reproducing register_analysis.ipynb section 1b: 41.2 % of sentences under 15 words before filtering, 19.5 % after, 330 lines dropped -- the plan's numbers, confirmed exactly. Through prose_from_extract the figures are 15.9 % and 445 lines, because the notebook's list misses 'Copyright (c) 2024 International Society...' while the gate's pre-existing '(c) 20' rule already caught it. The gate is the stricter of the two.

check_exemplar_quotes.py carries all four sources. Its two-way 'PDA else A-Mab' dispatch became a lookup over the SRC names, so an attribution naming none or two is skipped rather than silently charged to A-Mab. Its BOILER gained the ISPE footer and the three running headers, the latter line-anchored for the same reason as above.

Gates: make style exit 0 (2 human sources + 20 documents OK, 88 quotes checked, 0 failed -- the same 88 as before the dispatch change); make test 85 passed. The PDA TR 60 and A-Mab self-test output is byte-identical to the committed version, so the refactor moved no existing measurement.

FOR TASK-002, measured through the new filter at the page ranges the plan names. ISPE TT pp.30-140 passes all thirteen thresholds, but sits at 15.9 % under 15 words against a floor of 15.0 and at 28.0 mean length against a ceiling of 28.0. ISPE PV pp.30-190 fails THREE, not the two the plan predicted: mean_len 29.8 (<=28.0), pct_over_40 20.0 (<=16.0), pct_over_55 8.4 (<=7.5). The third is new because the fuller filter removed short boilerplate that was diluting the long sentences. Also worth knowing: selftest() currently exits 0 while printing SKIP for every missing source, which is the silent-pass hole TASK-002's first acceptance criterion closes.

## Files it touched

- `scripts/extract_sources.py`
- `authoring/check_style.py`
- `authoring/check_exemplar_quotes.py`
- `refs/text/ispe_tt.txt`
- `refs/text/ispe_pv.txt`
