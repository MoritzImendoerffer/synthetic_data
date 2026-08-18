---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-008
status: todo
kind: mechanism
title: "Replace WRITING_GUIDE.md with a short positive guide and move its history out"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-008 — Replace WRITING_GUIDE.md with a short positive guide and move its history out

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

Runs only on D4 = PASS. Positive means: say the thing to do. Never 'do not write X'; the tics are the one exception and they are listed as a gate, not argued. Take no sentence from the old guide's commentary except §6 (the numbers rule) and the reader paragraph. If a rule cannot be stated without a percentage, it is a reviewer's signal and belongs in REVIEW_CHECKLIST.md, not here.

## Acceptance criteria

- [ ] `wc -l authoring/WRITING_GUIDE.md` ≤ 200; `grep -c '✗' authoring/WRITING_GUIDE.md` → 0; `grep -cE '[0-9]+(\.[0-9]+)? ?%' authoring/WRITING_GUIDE.md` → 0; `grep -c '2026-' authoring/WRITING_GUIDE.md` → 0
- [ ] the new guide contains: the reader; the numbers rule (§6 of the old guide, kept whole); ten rules stated positively, each ≤ 2 sentences; the GATED tic list matching check_style.GATED exactly; the role sentence from probe-guide.md; three to five ✓ passages from REGISTER_EXEMPLAR.md by section reference, not re-quoted; and one line pointing at authoring/history/WRITING_GUIDE-2026-08-18.md
- [ ] authoring/history/WRITING_GUIDE-2026-08-18.md is the previous guide verbatim (`git show HEAD:authoring/WRITING_GUIDE.md | diff - authoring/history/WRITING_GUIDE-2026-08-18.md` empty at the commit that creates it) with a two-line header saying why it was retired and where its measurements live (docs/results/)
- [ ] `uv run python authoring/check_style.py --review authoring/WRITING_GUIDE.md` (prose_from_qmd on a .md is close enough) reports GATED OK
- [ ] CLAUDE.md Voice rule, RUNNER.md step 3, template.qmd's comment block and build_brief.py:423 name the guide's new role in one sentence each; `grep -rn 'WRITING_GUIDE.md §4a\|§4a' authoring/ CLAUDE.md pc_package/` → only hits in authoring/history/ and docs/results/
- [ ] brief §5d: build_brief.py stops emitting the 'rules as substitutions' bullet list (the guide owns the rules) and the numbers table is kept ONLY under a `--review` flag, so the author's brief carries no counters; `grep -c '## 5d' authoring/out/PCR-005.brief.md` → 0 after `build_brief.py PCR-005`, and 1 after `build_brief.py --review PCR-005`

**Depends on:** [[TASK-006]]

## Files it touched

- [[WRITING_GUIDE]] — `authoring/WRITING_GUIDE.md`
- [[WRITING_GUIDE-2026-08-18]] — `authoring/history/WRITING_GUIDE-2026-08-18.md`
- `CLAUDE.md`
- [[RUNNER]] — `authoring/RUNNER.md`
- `authoring/template.qmd`
- `authoring/build_brief.py`
