---
type: pm-task
epic: 2026-08-16_01_register-from-four-sources
sprint: 2026-08-16_01_register-from-four-sources
task: TASK-002
status: done
kind: mechanism
title: "Widen the self-test to four sources and stop capping the only connective in use"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-003", "PCR-005", "PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-16_01_register-from-four-sources/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-002 — Widen the self-test to four sources and stop capping the only connective in use

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

WHERE. authoring/check_style.py:selftest() (about line 306) hard-codes a two-entry list of (name, path, page_lo, page_hi). Add ('ISPE TT (human)', refs/text/ispe_tt.txt, 30, 140) and ('ISPE PV (human)', refs/text/ispe_pv.txt, 30, 190). Page ranges are the running-prose chapters; front matter and appendices are lists, not prose. The function already prints SKIP for a missing file - keep that, and additionally print a one-line summary naming how many sources were measured, so a run that silently halves cannot report OK.

THE THRESHOLDS. LIMITS is the dict at check_style.py:52-69, entries of (lo, hi, description). Measured on 2026-08-16 with the filters of TASK-001, the two ISPE guides FAIL exactly two of the thirteen, both at the top end:
  - mean_len: ISPE PV 28.3 against a ceiling of 28.0 -> raise to about 28.5
  - pct_over_40: ISPE PV 18.5 against a ceiling of 16.0 -> raise to about 19
Re-measure rather than trusting these numbers; your boilerplate filter will move them. The gate's founding rule is in its own docstring: a threshold this file asserts must be one real human regulatory prose passes, so if a source fails, the threshold is wrong.

THE CONNECTIVE CAP. LIMITS has "therefore": (None, 1.2). The corpus uses 'therefore' 10 times in PCR-003, 7 in PCR-008, 5 in PCR-005 - and uses However, For example, By contrast, In addition, Consequently and Note that ZERO times across all four documents, against 46 and 12 for the first two in A-Mab. So the gate caps the only connective in service. Remove the entry, or replace it with a rule over the nine connectives WRITING_GUIDE 4b lists. Do not add a floor for the other eight: a floor would be produced rather than met.

DO NOT add floors for semicolons, colons or pct_over_55. The corpus sits at zero on all three against human 1.1-3.3, and that gap is real, but they are ornament. This was considered and rejected in the proposal; if you disagree, say so rather than adding them.

GUIDE TABLE. WRITING_GUIDE.md 4a holds a table at about lines 158-172 with two source columns. Regenerate it with four, and keep the sentence under it that says to aim for the source numbers rather than the edge of the band.

## Acceptance criteria

- [x] check_style.py --selftest measures four sources and names each in its output, so a skipped source cannot pass silently
- [x] every threshold in LIMITS is one all four human sources pass
- [x] the 'therefore' entry no longer caps the only connective in use
- [x] WRITING_GUIDE 4a's threshold table is regenerated with one column per source
- [x] make style PY="uv run python" passes over all 20 documents, and no corpus document newly fails

**Depends on:** [[TASK-001]]

## What was built

The self-test measures four sources and names each with its page range. A source missing from refs/text/ is now a FAILURE, not a SKIP: the old code printed SKIP and exited 0, so a run that measured nothing reported the same success as a run that measured everything. I hit that hole for real during TASK-001.

PAGE RANGES CORRECTED AGAINST THE PLAN. The plan gave ISPE TT (30, 140) and ISPE PV (30, 190) and described them as the running-prose chapters. They are not. Each guide's own contents page puts Appendix 1 at extract page 97 (TT) and 113 (PV), so the plan's ranges ran 44 and 78 pages into case studies and statistical tables. The roster now reads (30, 96) and (30, 112), and it is a shared HUMAN_SOURCES constant that selftest() and compare() both read instead of each hard-coding its own list.

FIVE CEILINGS RAISED, not the two the plan predicted, and higher than it predicted:
  mean_len     28.0 -> 30.5  (ISPE PV 30.2)
  median_len   25.0 -> 26.5  (ISPE PV 26.0)
  pct_over_40  16.0 -> 21.5  (ISPE PV 20.8)
  pct_over_55   7.5 ->  9.5  (ISPE PV 9.0)
  paren        14.0 -> 14.5  (ISPE TT 14.2)
The plan expected 28.5 and 19 from two failures. The gap is the TASK-001 filter, exactly as the plan warned.

READ THIS BEFORE TRUSTING THE NEW BANDS. I checked whether ISPE PV's length is real prose or an extraction artifact, and it is partly an artifact: its longest 'sentences' are table cells and unmarked list items fused together, because PyMuPDF puts the bullet glyph on its own line and prose_from_extract then joins the item text to the lead-in. I prototyped two fixes -- a list-marker state machine and a short-unterminated-line rule. Both cut the fusion, NEITHER rescued the thresholds: list-aware left ISPE PV at 29.2 mean and pushed ISPE TT's under-15 to 11.7, below the 15.0 floor, and both moved PDA TR 60 and A-Mab, which are the committed calibration baseline. So the ceilings were raised as the plan directed and the extractor was left alone. If a later task wants a tighter envelope, fixing prose_from_extract's list handling is the lever, and it is a task of its own because it re-bases all four sources.

CONNECTIVE CAP REMOVED. 'therefore': (None, 1.2) is gone from LIMITS, which now has 12 entries. It is replaced by a CONNECTIVES diagnostic over the nine WRITING_GUIDE 4b lists: counted, printed on every run and in --compare, gated by nothing. No floor was added for the other eight, per the plan. The measurement it produces is the evidence TASK-009 needs: the 20 corpus documents run a median 1.5 connectives per 1k words using 3 of the 9, against 2.2-2.7 and 6-9 for the four sources, and 'However' occurs twice in the whole corpus against 59 times in the sources.

WRITING_GUIDE 4a regenerated with four source columns plus two diagnostic rows, and the sentence under it now says why the edge of the band is not a target. 4b's connective rule gained the measured gap and a warning against sprinkling.

Gates: make style exit 0 (4 sources + 20 documents OK, 0 FAIL, 88 quotes checked 0 failed); make test 85 passed; 20/20 annexes valid and byte-identical, since no document changed. Verified the missing-source failure by moving ispe_pv.txt aside: exit 1 with 'FAIL 1 source(s) not on disk'.

ALSO CORRECTED, outside the plan's file list, because they stated the gate's calibration and had become false: CLAUDE.md's register rule, pc_package/README.md's Register section, and the Makefile's style comment. STILL STALE, left for TASK-004 which owns those files: authoring/REGISTER_EXEMPLAR.md line 6 and authoring/HANDOFF.md lines 191 and 207 all still say two sources.

## Documents it is about

- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- `authoring/check_style.py`
- [[WRITING_GUIDE]] — `authoring/WRITING_GUIDE.md`
