---
type: pm-task
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
task: TASK-006
status: done
kind: document
title: "Re-author PCR-003 in one pass from the amended artifacts, as a DRAFT"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-006 — Re-author PCR-003 in one pass from the amended artifacts, as a DRAFT

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-006.md in this work unit — numbered steps, code, commands and the output each must print. Follow it top to bottom.  SEPARATE FROM TASK-005 on purpose; same rules. PCR-003 is the document the owner read twice and quoted from; it is 9,631 words and carries D-002 and the curated 35-span rhetorical layer (authoring/rhetorical/PCR-003.spans.yaml), which TASK-007 re-curates — the author does not look at the spans file.  THE TWO SENTENCES THE OWNER QUOTED are in the round-one text at lines 701 and 707 (Discussion). They are ✗ examples in the guide now (TASK-002); the author will meet them there and nowhere else.  THE AUTHOR IS TOLD THE NUMBER (see TASK-005 notes) and not told to hit a chaining figure.  NEVER PATCH.  RENDER THE PDF SEPARATELY.

## Acceptance criteria

- [x] before authoring, the round-one text is copied: cp pc_package/PCR-003_bioreactor.qmd .claude/work/2026-08-17_01_register-second-round/pre-rewrite/ (it equals `git show f06f1a7:pc_package/PCR-003_bioreactor.qmd`)
- [x] `uv run python authoring/build_brief.py PCR-003` regenerated first, so the brief carries §5c (D-002) and §5d with the round-one numbers (8.0 % ', so ', 0.9 % initial connective, chaining 30.7 %)
- [x] ONE agent authors the whole document in one pass from WRITING_GUIDE.md, REGISTER_EXEMPLAR.md, STORY_BIBLE.md, section_plan.yaml and the PCR-003 brief; it reads no sibling .qmd and not the PCP-003 draft
- [x] `uv run python authoring/check_render.py pc_package/PCR-003_bioreactor.DRAFT.qmd --render` passes, including the embedded style gate; the advisory packing line it prints is copied into this task's completion note
- [x] the D-002 absolute appears UNQUALIFIED in the draft, followed by the narrower true elaboration (brief §5c)
- [x] the Discussion names the four response-surface factors where it counts them, and the report states the commercial scale via V["commercial_scale_l"]
- [x] no inline expression that yields a response or parameter name is the agreeing subject of a clause (the 'acidic variants is' fault); every value is an inline {python} expression
- [x] the committed pc_package/PCR-003_bioreactor.qmd and all 20 annexes are untouched at the end of this task

**Depends on:** [[TASK-002]], [[TASK-004]]

## What was built

PCR-003 re-authored in one pass into pc_package/PCR-003_bioreactor.DRAFT.qmd by a SECOND agent in its own fresh context (general-purpose subagent, Opus 5 inherited), separate from TASK-005's and barred from the PCP-003 draft, every pc_package/*.qmd and authoring/rhetorical/PCR-003.spans.yaml. 421 sentences, 9822 words, 59 pages, 9 figures, full appendices A-D.

THE PACKING LINE, verbatim:

   --    clause packing (diagnostic, never gated)         ', so ' mid-sentence  0.0 % of sentences (0/421), opens with a connective  4.0 % (17/421), 2+ clause coordinators  1.7 %  [sources: 0.1-0.4 / 3.7-6.1 / 1.2-3.1]

Against round one's 8.0 / 0.9 / 5.4: ', so ' 8.0 -> 0.0 %, initial connective 0.9 -> 4.0 %, coordinators 5.4 -> 1.7 %. Both targets met, and as in the plan the ', so ' rate is BELOW every source (0.1-0.4), the same over-correction TASK-005 recorded. Both genres did it, which makes it a property of the instruction and not of one author -- TASK-008's to score.

REGISTER TABLE, all twelve gated rows ok: mean 23.3, median 22.0, over-40 5.9, over-55 0.2, under-15 19.5 (band 15.0-32.0; round one 22.7, so splitting sentences did NOT push it up here), em-dash 0.0, semicolon 0.1, colon 2.2, paren 7.5, bold 0.0, coined compounds 0.0, 'rather than' 0.5. 'OK    register is within the human-source envelope.' Connectives 3.2 per 1k words and 9 OF 9 DISTINCT (therefore 11, since 6, however 4, for this reason 3, once 2, consequently 2, in addition 1, as a result 1, by contrast 1) -- the full repertoire, against 6 of 9 in round one and 3 of 9 before the campaign. No corpus document has reached 9 of 9 before.

DISCOURSE, measured by me against the preserved round-one text: topic chaining 30.7 -> 46.1 % (190/412), copula 32.5 -> 25.7 % (106/413), adjunct front field 9.2 -> 17.4 % (72/413). Both no-regression conditions met with room, and copula moves from outside all four sources into the band. Chaining lands at 46.1 % in the report and 46.0 % in the plan -- two independent agents, 0.1 points apart, without either being asked to raise chaining. Still well short of the sources (57.0-61.9).

THE OWNER'S TWO SENTENCES ARE BOTH REPAIRED, in the same Discussion. The packed one is now three sentences: '...the test rests on N degrees of freedom of pure error. Therefore a passing test bounds the evidence for the model form without establishing it. For this reason the weakest model of the five is <expr> (p = <expr>), which also carries the lowest predicted R2 at <expr>.' The runtime name sits after 'is' as the guide now prescribes, so the 'acidic variants is' agreement fault cannot recur; the procedure's grep for a name expression as an agreeing subject returns nothing. The uncounted set is named too: 'a response surface design modelled the region defined by the <n_rsm_f> that screening retained: <rsm_list>', with the names pulled through a helper. The one later 'those four parameters' names its set in the same sentence.

D-002 SURVIVES UNQUALIFIED at line 554, in the introduction's account of the step's role, exactly where the assignment places it: 'The production bioreactor is the only step of the drug substance process at which product quality attributes are formed.' The narrower true elaboration follows immediately. Nothing reconciles it anywhere -- 'leached Protein A' does not occur in the document at all -- so the benchmark item is intact.

GATES, all re-run by me. check_render.py --render exits 0: chunks exec, 289 inline expressions eval, 0 <<NEEDS:>>, docx OK, style gate OK. PDF rendered separately with the venv on PATH and glyph-checked fresh: no missing glyphs. Numeral lint flags 14 advisory lines and every one is an identifier or convention (2-AB, pCO2, N-glycan, nutrient feed-1, x 10^6 attached to an inline expression, 95 % confidence level); no typed measurement. Commercial scale stated three times through V['commercial_scale_l'], the first in the Executive summary.

FLAG FOR THE OUTSIDE VIEW (TASK-007/009, not a defect): 59 pages against round one's 51, above the '41-55 pp' as-built band CLAUDE.md records for DoE reports. Prose is flat -- 9822 words against 9614, 421 sentences against 423 -- and the figure count is 9 in both, so the extra pages are table and appendix layout, not filler. If the draft is promoted, that CLAUDE.md line needs re-checking rather than defending.

BASELINE UNTOUCHED: git status over pc_package/ and authoring/ shows only the three untracked DRAFT artifacts. The committed PCR-003_bioreactor.qmd, all 20 annexes and the 35-span rhetorical layer are unmodified. Not promoted -- that is TASK-007.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `pc_package/PCR-003_bioreactor.DRAFT.qmd`
- [[PCR-003.brief]] — `authoring/out/PCR-003.brief.md`
- `.claude/work/2026-08-17_01_register-second-round/pre-rewrite/PCR-003_bioreactor.qmd`
