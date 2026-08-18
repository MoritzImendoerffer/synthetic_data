---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-004
status: done
kind: document
title: "Re-author PCR-005 in one pass, as a DRAFT"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-005"]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-004 — Re-author PCR-005 in one pass, as a DRAFT

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/AUTHOR-A-DOCUMENT.md. Outline `report_doe`. Baseline for this document is in measure_baseline_style.txt / measure_baseline_discourse.txt and is printed to the author by brief §5d. Annex exposure at promotion: 123 quotes, 39 rhetorical spans. Currently 43 pp. THE PASSIVE IS A BAND AND NEVER A FLOOR. PILOT, and one of the three the project owner reads. The only pilot document with a rhetorical layer, so it is the one that tests TASK-001's converted YAML end to end.

## Acceptance criteria

- [x] the current text is preserved first: `cp pc_package/PCR-005_protein_a.qmd .claude/work/2026-08-18_02_register-track-d/pre-rewrite/` and it equals `git show HEAD:pc_package/PCR-005_protein_a.qmd`
- [x] `uv run --extra discourse python authoring/build_brief.py PCR-005` regenerated first; §5d carries all twelve rows and §5c is empty for this document
- [x] ONE agent authors the whole document in one pass from WRITING_GUIDE.md, REGISTER_EXEMPLAR.md, STORY_BIBLE.md, section_plan.yaml -> report_doe and the PCR-005 brief; it reads no pc_package/*.qmd and no authoring/rhetorical/*.spans.yaml
- [x] `uv run python authoring/check_render.py pc_package/PCR-005_protein_a.DRAFT.qmd --render` passes including the style gate; the pdf is rendered SEPARATELY with the venv on PATH and glyph-checked fresh; the packing line is copied verbatim into the completion note
- [x] `grep -c '<<NEEDS' <draft>` is 0 and no typed measurement survives the numeral advisory except statistical conventions
- [x] `grep -c 'screening retained\|screening identified\|the design carries\|the model identifies\|the study selected' <draft>` is 0
- [x] the committed pc_package/PCR-005_protein_a.qmd and all 20 annexes are untouched; git status shows only the DRAFT and its untracked renders

**Depends on:** [[TASK-001]], [[TASK-002]]

## What was built

PCR-005 re-authored in one pass by claude-opus-5, as pc_package/PCR-005_protein_a.DRAFT.qmd. Outline `report_doe`. Not promoted -- that is TASK-006.

Final clause packing line, verbatim:

   --    clause packing (diagnostic, never gated)         ', so ' mid-sentence  0.0 % of sentences (0/424), opens with a connective  4.5 % (19/424), 2+ clause coordinators  1.4 %, ', and '+clause  2.1 % (9/424), ', not '  0.0 % (0/424)  [sources: 0.1-0.4 / 3.7-6.1 / 1.2-3.1 / 1.1-3.4 / 0.0-0.2]

Against brief §5d: ', so ' 11.0 -> 0.0 (<=1.0); opens with a connective 0.0 -> 4.5 (>=3.0); 2+ coordinators 6.7 -> 1.4 (source band 1.2-3.1); ', and '+clause regex 16.3 -> 2.1 (<=3.4); ', not ' 0.3 -> 0.0 (<=0.2). The ', and '+clause figure is 2.1 % and not zero ON PURPOSE: the four sources run 1.1-3.4 % and driving it to zero overshoots the band it is meant to land in.

Register table: 424 sentences, 9787 words. All twelve gated rows ok -- mean 23.1, median 21.5, over 40 words 7.5, over 55 words 0.5, under 15 words 18.2, em-dashes 0.0, semicolons 0.5, colons 2.0, parentheses 5.7, bold 0.0, coined compounds 0.6, "rather than" 0.4. Connectives 4.3 per 1k, 9 of 9 distinct -- the full repertoire, which round three reached once and then lost. "OK register is within the human-source envelope."

Parser rows, previous revision -> now: topic chaining 34.8 -> 39.6 % (165/417), did not fall; copula 27.3 -> 18.7 % (78/418), down 8.6 pt from the highest starting copula in the pilot; front field 7.4 -> 16.7 %; passive 51.4 -> 54.3 % (227/418) -- it ROSE, from below the band into it, and was not driven to a floor; ', and '+clause parser 20.2 -> 3.6 %.

PDF: rendered separately, glyph-checked fresh -- 47 pp, no missing glyphs. Previous revision 43 pp; the DoE-report band is 41-56 pp.

Verified by me: <<NEEDS:>> 0; false-agent phrases 0; ', so ' 0, ', and this' 0, ', and both' 0, ', and it' 0, ', and each' 0, ', not ' 0; ', and the' 8 occurrences, which is the 2.1 % above and is inside the source band; no expression-as-subject; one typed-measurement hit, a 95 % predictive interval. git diff over tracked files empty.

The agent's open question is resolved and needs nothing at promotion: it renumbered §n cross-references to the RENDERED numbering, where the executive summary is unnumbered and Introduction is §1. The committed revision uses the same convention -- both files declare `# Executive summary {.unnumbered}` followed by `# Introduction` -- so no mapping has to be reverted.

This is the only pilot document with a rhetorical layer, 39 spans, so TASK-006 tests TASK-001's converted YAML end to end on it. The layer was curated against the OLD text and every span must be re-curated against this one before build_ground_truth runs, or it writes nothing for this document.

## Documents it is about

- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`

## Files it touched

- `pc_package/PCR-005_protein_a.DRAFT.qmd`
- [[PCR-005.brief]] — `authoring/out/PCR-005.brief.md`
- `.claude/work/2026-08-18_02_register-track-d/pre-rewrite/PCR-005_protein_a.qmd`
