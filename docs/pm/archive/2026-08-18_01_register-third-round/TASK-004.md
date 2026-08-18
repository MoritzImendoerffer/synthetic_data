---
type: pm-task
epic: 2026-08-18_01_register-third-round
sprint: 2026-08-18_01_register-third-round
task: TASK-004
status: done
kind: document
title: "Re-author PCR-003 in one pass from the amended artifacts, as a DRAFT"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-18_01_register-third-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-004 — Re-author PCR-003 in one pass from the amended artifacts, as a DRAFT

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-004.md — the previous unit's TASK-006 procedure with the round-three brief. ONE GENRE ONLY, by owner decision (proposal, 'shape of the next round'): PCP-003 is NOT re-authored. Its §5d row is generated anyway (it costs nothing) and it is the CONTROL — if a measure moves in PCR-003 the page says 'moved in the report'. THE AUTHOR IS TOLD THE NUMBER for all eight measures now (three new + five from round two) and the two new substitutions. It is NOT told to write more passives to hit a count; the rule is 'where the sources would write a passive, write the passive', and the passive figure is a band the report is under. PREDICTED OVERSHOOT (exploration §3): expect ', and '+clause to go to ~0 %, below the sources' 1.1-3.4, the way ', so ' did. That is a result for TASK-006, not a reason to edit a sentence. NEVER PATCH. Second one-pass author allowed; post-editing is not. pct_under_15 has a 32 % ceiling and round two sits at 19.5 %; splitting the ', and ' clauses adds short sentences — the author should know the ceiling. RENDER THE PDF SEPARATELY with PATH="$PWD/.venv/bin:$PATH"; check_render glyph-checks whatever pdf is on disk.

## Acceptance criteria

- [x] before authoring, the round-two text is copied: `cp pc_package/PCR-003_bioreactor.qmd .claude/work/2026-08-18_01_register-third-round/pre-rewrite/` and it equals `git show e7a4768:pc_package/PCR-003_bioreactor.qmd`
- [x] `uv run --extra discourse python authoring/build_brief.py PCR-003` regenerated first; §5c carries D-002 and §5d carries the round-two numbers (', and '+clause 22.6, ', not ' 4.3, passive 34.4, plus the five round-two measures)
- [x] ONE agent authors the whole document in one pass from WRITING_GUIDE.md, REGISTER_EXEMPLAR.md, STORY_BIBLE.md, section_plan.yaml and the PCR-003 brief; it reads no pc_package/*.qmd and not authoring/rhetorical/PCR-003.spans.yaml
- [x] `uv run python authoring/check_render.py pc_package/PCR-003_bioreactor.DRAFT.qmd --render` passes including the style gate; the pdf is rendered SEPARATELY with the venv on PATH and glyph-checked fresh; the packing line (now five figures) is copied verbatim into the completion note
- [x] the D-002 absolute appears UNQUALIFIED in the introduction with the true elaboration following; the commercial scale is stated via V["commercial_scale_l"]; the Discussion names the four factors it counts
- [x] no inline expression yielding a name is an agreeing subject (grep from the previous unit's TASK-006 §4 returns nothing); `grep -c 'screening retained\|screening identified\|the design carries\|the model identifies' pc_package/PCR-003_bioreactor.DRAFT.qmd` is 0
- [x] the committed pc_package/PCR-003_bioreactor.qmd, pc_package/PCP-003_bioreactor.qmd and all 20 annexes are untouched; git status shows only the DRAFT and its untracked renders

**Depends on:** [[TASK-003]]

## What was built

PCR-003 re-authored in one pass into pc_package/PCR-003_bioreactor.DRAFT.qmd by ONE agent in a fresh context (general-purpose subagent, claude-opus-5 inherited), from WRITING_GUIDE.md, the regenerated brief, section_plan.yaml, REGISTER_EXEMPLAR.md and STORY_BIBLE.md. It was told to open no pc_package/*.qmd and not authoring/rhetorical/PCR-003.spans.yaml, and reported opening neither; it read _pcpkg.py and doe_report.py for helper signatures, which are code and not documents. 437 sentences, 9,639 words, 56 pages, 13 figures, 24 tables, 42 chunks, 275 inline expressions.

THE PACKING LINE, verbatim from the final check_render run (now five figures):

   --    clause packing (diagnostic, never gated)         ', so ' mid-sentence  0.0 % of sentences (0/437), opens with a connective  3.7 % (16/437), 2+ clause coordinators  1.8 %, ', and '+clause  0.5 % (2/437), ', not '  0.0 % (0/437)  [sources: 0.1-0.4 / 3.7-6.1 / 1.2-3.1 / 1.1-3.4 / 0.0-0.2]

Against round two's 0.0 / 4.0 / 1.7 / 22.6 / 4.3: the two measures this round added both collapsed. ', and '+clause 22.6 -> 0.5 % (2/437) and ', not ' 4.3 -> 0.0 % (0/437). The ', and ' regex figure is BELOW the sources' 1.1-3.4 band, which is the overshoot exploration §3 predicted for a rule stated as a substitution -- the third time in three rounds (', so ' to 0.0 %, PCP-003's possessives to zero). The parser half is inside its band at its floor (0.7 %, sources 0.7-3.6), so the two halves disagree about whether the overshoot is real; that is TASK-006's to score, not a sentence to edit. The three measures that were only printed, not newly measured, held: ', so ' stayed 0.0, initial connectives 3.7 (>= 3.0 target, sources 3.7-6.1), coordinators 1.8.

REGISTER TABLE, all twelve gated rows ok: 437 sentences, 9,639 words; mean 22.1 (20.0-30.5), median 21.0 (18.0-26.5), over-40 6.9 (3.0-21.5), over-55 0.0 (<=9.5), under-15 26.1 (15.0-32.0) -- splitting the ', and ' clauses cost 6.6 points against a 32.0 ceiling, from 19.5, so the plan's warning about the ceiling was live and the room held -- em-dash 0.0, semicolon 0.1, colon 1.3, paren 6.6 (3.0-14.5), bold 0.0, coined compounds 0.2, 'rather than' 0.3. 'OK    register is within the human-source envelope.' Connectives 2.4 per 1k words, 8 of 9 distinct (since 7, therefore 5, once 4, however 3, in addition 1, as a result 1, by contrast 1, consequently 1), against 9 of 9 in round two.

DISCOURSE, measured by me rather than taken from the agent (check_discourse.py --cap, draft against the preserved round-two copy, one command, both columns):

  topic chaining     46.1 (190/412) -> 47.6 % (204/429)   sources 57.0-61.9
  copula main verb   25.7 (106/413) -> 16.5 % (71/430)    sources 14.8-26.1
  adjunct front      17.4 (72/413)  -> 30.2 % (130/430)   sources 27.1-36.3
  passive            35.4 (146/413) -> 57.4 % (247/430)   band 57-64 on this n
  ', and ' parser    25.4 (105/413) -> 0.7 % (3/430)      sources 0.7-3.6

THE PASSIVE IS THE RESULT OF THIS ROUND. 35.4 -> 57.4 %, into the band's lower edge, having fallen at every previous revision (44.1 -> 41.6 -> 35.4). It was handed to the author as a band and a rule ('where the sources would write a passive, write the passive'), never as a count to hit, and it moved 22 points. Front field also moved from below all four sources to inside their range, and copula fell 9.2 points without being targeted. No no-regression condition was breached: chaining rose.

GATES, all re-run by me after the fix below. check_render.py --render exit 0: 42 chunks exec, 275 inline expressions eval, 0 <<NEEDS:>>, register OK, quarto docx OK. The pdf was rendered SEPARATELY by me with PATH="$PWD/../.venv/bin:$PATH", fresh after the final edit, then glyph-checked: 'OK    PCR-003_bioreactor.DRAFT.pdf: no missing glyphs', 56 pages. The numeral lint's 38 advisory hits are identifiers and statistical conventions (CO2/pCO2, 2-AB, N-1, feed-1, coded levels, section refs, 95 % CI), no typed measurements.

D-002 IS CARRIED, verbatim as registered and unqualified, at line 536 under '# Introduction' -> '## Product and unit operation' -- the placement the assignment names, not the executive summary: 'The production bioreactor is the only step of the drug substance process at which product quality attributes are formed.' The true elaboration follows in the next two sentences (glycosylation and charge variant distributions established in the cell and the culture fluid, not modified by the platform purification train). 'leached Protein A' does not occur in the document (0).

ONE ACCEPTANCE FAILURE WAS FOUND AND SENT BACK TO THE SAME AGENT, per RUNNER.md §4 (same context, in place, never a fresh agent and never patched by me). The executive summary closed with 'In this report those response surface models carry the predictive claim and the basis of the design space in §6, whereas screening identified only which factors matter' -- two agents in one sentence, models as agent of carry and screening as agent of identify, and grep -c on the five forbidden strings returned 1. Rewritten by the author to 'In this report both the predictive claim for those responses and the basis of the design space in §6 rest on the response surface models, whereas the factors that matter were identified by screening.' The framing rule survives, both agents are gone. Grep now returns 0. Every figure in the packing line is unchanged by the edit; the passive rose 57.2 -> 57.4 %.

ONE INSTANCE OF THE SAME FAULT SURVIVES, DELIBERATELY NOT PATCHED. Line 879, §5.3: 'Within that region, those models carry the predictive claim of this report.' A model is the agent of carry, which WRITING_GUIDE §2d forbids, but it matches none of the five acceptance search strings, so the literal acceptance check passes. Editing it would have widened the task and, worse, would have made round four's page claim the RULE worked when what actually worked was the orchestrator's grep. It is left in as evidence for TASK-006: a search string is not a measure, which is this round's own thesis. Counted crudely (study/design/model/screening within 60 chars of carry/retain/select/identify), the round-two text has 5 such hits and the draft has 1 genuine one; the other draft hit, line 751, is a false positive of that regex ('a screening experiment is run to identify ...' is already passive).

TWO NOTES ON THE ACCEPTANCE LINES THEMSELVES, for the plan rather than the document:

1. `grep -c 'V["commercial_scale_l"]'` returns 0, and the quote-agnostic form returns 4. The document writes `{python} f"{V['commercial_scale_l']:,}"` -- single quotes inside a double-quoted f-string, because double quotes there are a syntax error. The criterion's substance (the scale is stated through the helper, never typed) is met four times, at lines 495, 534, 650 and 659. Only the quote style in the grep differs, and the grep is carried over unchanged from the previous unit.

2. The acceptance grep forbids `screening identified`, but WRITING_GUIDE.md:372 carries a checkmark example that writes 'screening identifies the factors that matter', and §4 line 468 states the framing rule as 'The screening design finds which factors matter'. The guide's own forbidden list is the narrower four (`screening retained`, `the design carries`, `the study selected`, `the model identifies`). The sentence that failed was a genuine fault on the rule's wording either way, so nothing turned on it here, but the guide and the acceptance grep disagree and should be reconciled before round four.

BASELINE UNTOUCHED. git status lists only the three pc_package/PCR-003_bioreactor.DRAFT.* files and the pre-rewrite directory. PCP-003 was not re-authored and is the control column. No tracked .qmd, no rendered corpus file, no ground_truth/*.json and no outputs/ file was modified. authoring/out/ is gitignored, so the regenerated brief does not appear. make style 24 OK / 0 FAIL at the baseline before authoring.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `pc_package/PCR-003_bioreactor.DRAFT.qmd`
- [[PCR-003.brief]] — `authoring/out/PCR-003.brief.md`
- `.claude/work/2026-08-18_01_register-third-round/pre-rewrite/PCR-003_bioreactor.qmd`
