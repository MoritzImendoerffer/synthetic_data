---
type: pm-task
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
task: TASK-005
status: done
kind: document
title: "Re-author PCP-003 in one pass from the amended artifacts, as a DRAFT"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003"]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-005 — Re-author PCP-003 in one pass from the amended artifacts, as a DRAFT

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-005.md in this work unit — numbered steps, code, commands and the output each must print. Follow it top to bottom.  SEPARATE FROM TASK-006 on purpose: two documents in one task is a new instance of the self-reference loop. Two agents, one document each, neither reading the other's draft — the pilot's TASK-007 rule.  THE AUTHOR IS TOLD THE NUMBER THIS TIME. That is the round's hypothesis (decisions.same_method / proposal §'Why two moved and three did not'): round one withheld the measurement and only the substitution rules landed. §5d gives the author its own round-one packing figure and the target, and check_style prints the figure back on every check_render run. The author is NOT told to raise chaining or produce connectives to a count — the guide says a produced connective is a worse tell than a missing one.  NEVER PATCH. If the first draft comes back at 8 % ', so ', that is a result for TASK-008, not a reason to edit sentences. A second one-pass author is allowed; post-editing is not.  THE PLAN GENRE TRAP from round one: PCP-003 removed 25 possessives and added 23 copulas ('it is' 7→21), and went from inside the copula band (18.4 %) to outside all four sources (27.6 %). §2d bis now names the substitution; the author should see 'it is' as the thing not to write.  pct_under_15 has a 32 % ceiling and PCP-003 round one sits at 20.4 %; splitting one sentence in ten adds roughly 5–8 points, so there is room, and the author should know the ceiling exists.  RENDER THE PDF SEPARATELY (cd pc_package && quarto render PCP-003_bioreactor.DRAFT.qmd --to pdf) — check_render glyph-checks whatever pdf is on disk.

## Acceptance criteria

- [x] before authoring, the round-one text is copied: cp pc_package/PCP-003_bioreactor.qmd .claude/work/2026-08-17_01_register-second-round/pre-rewrite/ (it equals `git show f06f1a7:pc_package/PCP-003_bioreactor.qmd`)
- [x] `uv run python authoring/build_brief.py PCP-003` regenerated first, so the brief carries §5c (D-001) and §5d with the round-one numbers (10.6 % ', so ', 1.8 % initial connective)
- [x] ONE agent authors the whole document in one pass from WRITING_GUIDE.md, REGISTER_EXEMPLAR.md, STORY_BIBLE.md, section_plan.yaml and the PCP-003 brief; it reads no sibling .qmd and not the PCR-003 draft
- [x] `uv run python authoring/check_render.py pc_package/PCP-003_bioreactor.DRAFT.qmd --render` passes, including the embedded style gate; the advisory packing line it prints is copied into this task's completion note
- [x] the D-001 at-set-point commitment appears in the draft (brief §5c says which sentence)
- [x] no number is typed: every value is an inline {python} expression; the commercial scale is stated via V["commercial_scale_l"]
- [x] the committed pc_package/PCP-003_bioreactor.qmd and all 20 annexes are untouched at the end of this task; git status shows only the DRAFT, its untracked render, the brief and the pre-rewrite copy

**Depends on:** [[TASK-002]], [[TASK-004]]

## What was built

PCP-003 re-authored in one pass into pc_package/PCP-003_bioreactor.DRAFT.qmd by ONE agent in a fresh context (general-purpose subagent, Opus 5 inherited), from WRITING_GUIDE.md, the regenerated brief, section_plan.yaml, REGISTER_EXEMPLAR.md and STORY_BIBLE.md. It was told to open no pc_package/*.qmd and reported opening none; it read _pcpkg.py and doe_report.py for helper signatures, which are code and not documents. 203 sentences, 4783 words, 29 pages.

THE PACKING LINE, verbatim from the final check_render run:

   --    clause packing (diagnostic, never gated)         ', so ' mid-sentence  0.0 % of sentences (0/203), opens with a connective  4.9 % (10/203), 2+ clause coordinators  3.0 %  [sources: 0.1-0.4 / 3.7-6.1 / 1.2-3.1]

Against round one's 10.6 / 1.8 / 9.3, and against the round's targets (<= 1.0 and >= 3.0): ', so ' 10.6 -> 0.0 %, sentence-initial connective 1.8 -> 4.9 %, 2+ coordinators 9.3 -> 3.0 %. All three are inside the source bands. Note 0.0 % is BELOW every source (0.1-0.4); a document that never writes ', so ' has driven out the licensed use as well, which is the possessive lesson repeating and is TASK-008's to score, not this task's to fix.

REGISTER TABLE, all twelve gated rows ok: mean 23.6 (20.0-30.5), median 23.0 (18.0-26.5), over-40 7.4 (3.0-21.5), over-55 0.0 (<=9.5), under-15 23.6 (15.0-32.0) -- the split cost 3.2 points against a 32.0 ceiling, so the room the plan predicted was there -- em-dash 0.0, semicolon 0.0, colon 1.7, paren 5.4 (3.0-14.5), bold 0.0, coined compounds 0.0, 'rather than' 0.0. Connectives 2.9 per 1k words, 7 of 9 distinct (therefore 4, however 3, since 2, once 2, in addition 1, for this reason 1, consequently 1), against 6 of 9 in round one. 'OK    register is within the human-source envelope.'

DISCOURSE, verified by me rather than taken from the agent's report (check_discourse.py --cap, draft vs the pre-rewrite copy): topic chaining 34.4 -> 46.0 % (92/200), copula 27.6 -> 21.9 % (44/201), adjunct front field 10.2 -> 22.4 % (45/201). The round's no-regression conditions are met with room: chaining rose 11.6 points and copula fell 5.7, which takes the plan genre back INSIDE the source band (14.8-26.1) from outside all four. That was round one's worst regression -- 25 possessives traded for 23 expletive subjects -- and the named substitution in 2d bis is the change between the rounds. Front field doubled but is still short of the sources (27.1-36.3).

GATES, all re-run by me. check_render.py --render exits 0: all chunks exec, 51 inline expressions eval, 0 <<NEEDS:>> markers, docx render OK, style gate OK. The PDF was rendered SEPARATELY with the venv on PATH (quarto resolves python3 from PATH, not PY -- the first attempt died on 'Install with conda install jupyter') and glyph-checked fresh: 'no missing glyphs'. The numeral lint reports 20 advisory lines; every one is an identifier (CO2, pCO2, 2-AB, N-glycan, feed-1, ALCOA+, CHO) or a statistical convention (alpha = 0.05, coded -1/+1, 95 % interval), none a typed measurement. The procedure's own typed-measurement grep returns one hit, the 95 % predictive interval, which check_render explicitly permits.

D-001 is carried at lines 599-602 of the draft: 'The first holds the other factors at the set-points in @tbl-params and scans the parameter of interest across the full characterization range'. It says set-points and means it, and a grep for 'design centre', 'midpoint' and 'coded zero' returns nothing, so none of the three framings the assignment forbids leaked in. The commercial scale is stated twice in prose (lines 162 and 348) through scale_l = V["commercial_scale_l"], never typed.

BASELINE UNTOUCHED. git status over pc_package/ shows exactly three entries, all untracked: the DRAFT .qmd, .docx and .pdf. The committed PCP-003_bioreactor.qmd and all 20 annexes are unmodified. The draft is NOT promoted -- that is TASK-007.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`

## Files it touched

- `pc_package/PCP-003_bioreactor.DRAFT.qmd`
- [[PCP-003.brief]] — `authoring/out/PCP-003.brief.md`
- `.claude/work/2026-08-17_01_register-second-round/pre-rewrite/PCP-003_bioreactor.qmd`
