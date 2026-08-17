---
type: pm-task
epic: 2026-08-16_01_register-from-four-sources
sprint: 2026-08-16_01_register-from-four-sources
task: TASK-007
status: done
kind: document
title: "Re-author PCP-003 and PCR-003, one pass each, from the amended artifacts"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-16_01_register-from-four-sources/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-007 — Re-author PCP-003 and PCR-003, one pass each, from the amended artifacts

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

SCOPE WIDENED to two documents on 2026-08-17; see decisions.pilot_scope. One plan and one report, so both genres and both registered discrepancies are exercised before any decision is taken about the other 18.

WHY THESE TWO. PCP-003 is the worst modality case in the corpus - 'will' at 19.7 per 1000 words against a human 2.0-3.3, with 'should' and 'may' at 0.0 - and it is a plan, the genre that had no exemplar until TASK-004. It carries D-001. It is 4,719 words. PCR-003 is the report the owner quoted when raising this, it carries D-002, and it is the extreme on three of the five shape measures ('its' 6.66 per 1000 words against A-Mab's 0.32, copula-headed sentences 33.3 % against 14.7-18.2, chaining 37.2 % against 57-62). It is 10,354 words, the longest document in the corpus.

TWO AGENTS, NOT ONE. Each document gets its own agent and its own single pass. Do not let one agent write both, and do not let the second read the first. The sibling-copying loop is what forced all 20 documents to be re-authored once already, and running two documents at once is exactly the situation where it would recur without anyone deciding to.

THE LOOP is authoring/RUNNER.md. build_brief.py <DOC> -> instantiate authoring/template.qmd -> one agent writes the body in section_plan.yaml order -> check_render.py --render. Structure from section_plan.yaml, voice from REGISTER_EXEMPLAR.md. Canonical section orders for both genres are in CLAUDE.md.

DRAFT FILENAMES ARE NOT OPTIONAL. Author into pc_package/PCP-003_bioreactor.DRAFT.qmd and pc_package/PCR-003_bioreactor.DRAFT.qmd. Their rendered .docx files are untracked, so the committed baseline of 37 rendered files and all 2084 annex quotes stay green while the text is iterated. TASK-008 promotes both. This is the only reason the repository can stay green across a re-author.

DO NOT GIVE THE AUTHORS THE METRICS. Do not tell an author to raise topic chaining, produce connectives, reduce copulas or cut possessives. The measurement happens in TASK-009, afterwards. This repository has already watched a metric move while the prose got worse: when a one-sided sentence-length cap was added, the next generation came back at a 17-word mean with 41 % of sentences under 15 words. The author gets the guide and the exemplar, which are shapes and examples, never targets.

WATCH THE NEW HEADROOM. TASK-002 raised mean_len to 30.5, pct_over_40 to 21.5 and pct_over_55 to 9.5 because ISPE PV measures there, and partly because that source's extraction fuses list items into pseudo-sentences. An author writing to the edge of the band rather than to the per-source columns is the main risk this pilot exists to detect. Do not tell the author that either; just read the numbers in TASK-009.

## Acceptance criteria

- [x] build_brief.py regenerated for BOTH documents first, so each brief carries its 5c section: PCP-003 with D-001, PCR-003 with D-002
- [x] TWO separate agents, one document each, each authoring its whole document in one pass from WRITING_GUIDE.md, REGISTER_EXEMPLAR.md, STORY_BIBLE.md, section_plan.yaml and its own brief
- [x] NEITHER agent reads the other's draft, and neither reads any sibling .qmd. Two documents in flight is a new instance of the self-reference loop, not an exception to it
- [x] check_render.py --render passes on both DRAFTs, including the PDF glyph check and the embedded style gate
- [x] the D-001 at-set-point commitment appears in the re-authored PCP-003
- [x] the D-002 absolute appears UNQUALIFIED in the re-authored PCR-003, followed by the narrower true elaboration
- [x] no number is typed in either document: every value is an inline {python} expression
- [x] the committed .qmd files and all 20 annexes are untouched at the end of this task

**Depends on:** [[TASK-002]], [[TASK-004]], [[TASK-005]], [[TASK-006]]

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `pc_package/PCP-003_bioreactor.DRAFT.qmd`
- `pc_package/PCR-003_bioreactor.DRAFT.qmd`
- [[PCP-003.brief]] — `authoring/out/PCP-003.brief.md`
- [[PCR-003.brief]] — `authoring/out/PCR-003.brief.md`
