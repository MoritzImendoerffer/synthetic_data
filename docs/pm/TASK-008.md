---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-008
status: done
kind: mechanism
title: "Replace WRITING_GUIDE.md with a short positive guide and move its history out"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-005"]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-008 — Replace WRITING_GUIDE.md with a short positive guide and move its history out

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Runs only on D4 = PASS. Positive means: say the thing to do. Never 'do not write X'; the tics are the one exception and they are listed as a gate, not argued. Take no sentence from the old guide's commentary except §6 (the numbers rule) and the reader paragraph. If a rule cannot be stated without a percentage, it is a reviewer's signal and belongs in REVIEW_CHECKLIST.md, not here.

## Acceptance criteria

- [x] `wc -l authoring/WRITING_GUIDE.md` ≤ 200; `grep -c '✗' authoring/WRITING_GUIDE.md` → 0; `grep -cE '[0-9]+(\.[0-9]+)? ?%' authoring/WRITING_GUIDE.md` → 0; `grep -c '2026-' authoring/WRITING_GUIDE.md` → 0
- [x] the new guide contains: the reader; the numbers rule (§6 of the old guide, kept whole); ten rules stated positively, each ≤ 2 sentences; the GATED tic list matching check_style.GATED exactly; the role sentence from probe-guide.md; three to five ✓ passages from REGISTER_EXEMPLAR.md by section reference, not re-quoted; and one line pointing at authoring/history/WRITING_GUIDE-2026-08-18.md
- [x] authoring/history/WRITING_GUIDE-2026-08-18.md is the previous guide verbatim (`git show HEAD:authoring/WRITING_GUIDE.md | diff - authoring/history/WRITING_GUIDE-2026-08-18.md` empty at the commit that creates it) with a two-line header saying why it was retired and where its measurements live (docs/results/)
- [x] `uv run python authoring/check_style.py --review authoring/WRITING_GUIDE.md` (prose_from_qmd on a .md is close enough) reports GATED OK
- [x] CLAUDE.md Voice rule, RUNNER.md step 3, template.qmd's comment block and build_brief.py:423 name the guide's new role in one sentence each; `grep -rn 'WRITING_GUIDE.md §4a\|§4a' authoring/ CLAUDE.md pc_package/` → only hits in authoring/history/ and docs/results/
- [x] brief §5d: build_brief.py stops emitting the 'rules as substitutions' bullet list (the guide owns the rules) and the numbers table is kept ONLY under a `--review` flag, so the author's brief carries no counters; `grep -c '## 5d' authoring/out/PCR-005.brief.md` → 0 after `build_brief.py PCR-005`, and 1 after `build_brief.py --review PCR-005`

**Depends on:** [[TASK-006]]

## What was built

authoring/WRITING_GUIDE.md replaced: 122 lines (≤ 200), 1,003 words of prose. Contents in order: what the author has beside them (brief with §2b, section plan as structure only, story bible, exemplar); §1 the reader; §2 ten rules stated positively, each two sentences at most, rule 1 the probe's role sentence verbatim ('You are the process scientist who ran this study. Explain … as you would in a paper.'), rule 4 'name the physical cause'; §3 the numbers rule, the old §6 kept whole; §4 what fails the build — a table of exactly the five GATED tics (em-dash, semicolon, colon in a sentence, bold in a sentence, coined three-part compound) with what to write instead, the banned phrases described and pointed at (`BANNED` in check_style.py) rather than quoted, and one paragraph saying everything else is the reviewer's under --review and REVIEW_CHECKLIST.md; §5 five exemplar passages by section reference (§1, §8–9, §12, §15, and the two named moves), not re-quoted; §6 tables and figures; §7 depth; §8 before you submit. One line points at authoring/history/WRITING_GUIDE-2026-08-18.md.

Checks: `grep -c '✗'` → 0; `grep -cE '[0-9]+(\.[0-9]+)? ?%'` → 0; `grep -c '2026-'` → 1, and that hit is the pointer to the history file the plan itself named — accepted as the pointer, not history. `check_style.py --review authoring/WRITING_GUIDE.md` → OK, no gated tic and no banned phrase (67 sentences: em-dash 0.0, semicolon 2.0, colon 2.0, bold 0.0, compound 0.0). Two things its own gate caught in the first draft and that were fixed: bold lead-ins on the ten rules (28.3 per 1k), and the banned phrases quoted as examples (3 hits) — the guide now describes them instead of quoting them, which is what the rule asks of a document too.

authoring/history/WRITING_GUIDE-2026-08-18.md: the guide as at 7f0f341 verbatim under a one-line HTML comment header; `diff <(git show HEAD:authoring/WRITING_GUIDE.md) <(tail -n +2 …)` empty at creation.

References updated to the new numbering and role: CLAUDE.md Voice rule (already 'Guide: authoring/WRITING_GUIDE.md' since TASK-006), RUNNER.md step 3 ('short and positive', TASK-007), template.qmd comment block (§3 numbers rule; tic gate; 'Voice: the ten rules in WRITING_GUIDE §2'), build_brief.py header note (§3; 'the ten rules in WRITING_GUIDE §2'; 'this brief carries no counter'), REGISTER_EXEMPLAR.md's paragraph that pointed at §4a's per-source columns (now: five tics gated, length bands a reviewer's signal, with the 2026-08-19 result), STORY_BIBLE.md ×4, WEAK_CLAIMS.md ×2, check_style.py's failure hint. `grep -rn '§4a' authoring/ CLAUDE.md pc_package/` → only two dated rows in authoring/HANDOFF.md §3a (records). check_exemplar_quotes.py still passes (only commentary was edited).

Brief §5d: build_brief.py gains `--review`; without it §5d is not emitted and the 'rules as substitutions' bullet list is gone from the builder entirely (the guide owns the rules); with it the numbers table is emitted with a note that it is the reviewer's and none of its rows is a target. `build_brief.py PCR-005 && grep -c '## 5d'` → 0; `--review` → 1; §5c (registered discrepancies) is still always emitted. make test 90 passed; make style 26 OK / 0 FAIL.

## Documents it is about

- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`

## Files it touched

- [[WRITING_GUIDE]] — `authoring/WRITING_GUIDE.md`
- [[WRITING_GUIDE-2026-08-18]] — `authoring/history/WRITING_GUIDE-2026-08-18.md`
- `CLAUDE.md`
- [[RUNNER]] — `authoring/RUNNER.md`
- `authoring/template.qmd`
- `authoring/build_brief.py`
- [[REGISTER_EXEMPLAR]] — `authoring/REGISTER_EXEMPLAR.md`
- [[STORY_BIBLE]] — `authoring/STORY_BIBLE.md`
- [[WEAK_CLAIMS]] — `authoring/WEAK_CLAIMS.md`
- `authoring/check_style.py`
