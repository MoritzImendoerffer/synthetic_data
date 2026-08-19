---
type: pm-task
epic: 2026-08-19_01_fourth-round-one-document
sprint: 2026-08-19_01_fourth-round-one-document
task: TASK-008
status: done
kind: documentation
title: "Move the findings into docs, update the roadmap and the proposal, and ship"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
---

> [!warning] Generated from `.claude/work/2026-08-19_01_fourth-round-one-document/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-008 — Move the findings into docs, update the roadmap and the proposal, and ship

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

/ship does this. Whether the campaign continues to the remaining documents is a new decision for the owner and a new /explore, not this unit's.

## Acceptance criteria

- [x] docs/results/README.md gains the page's row; authoring/HANDOFF.md §3a gains one row: 'PCR-007 re-authored in one pass under the rebuilt apparatus, 2026-08-<dd>' with the re-anchoring counts (quotes moved / 88, spans re-cut / 33) on PASS, or 'authored, read, not promoted' on FAIL
- [x] docs/ROADMAP.md: the register-campaign row says what is now true — on PASS, that one document is at the rebuilt-apparatus register and the remaining count (14 at round zero + the earlier-round documents), and that the rest is the owner's call; on FAIL, what the reading named and that the regime needs revising before another document
- [x] docs/next/register-from-four-sources.md: rewritten down to what remains (the other documents, in the owner's order) or deleted if the owner decides the campaign is done — the plan does not decide this; its README.md row matches
- [x] CLAUDE.md depth band and TASKS.md page band re-measured if PCR-007's page count moved them; TASKS.md 'Things that will catch you out' gains an item only if this round found one
- [x] `uv run python scripts/pm_notes.py` regenerated; D5 and D6 settled; metadata.json status = shipped

**Depends on:** [[TASK-005]]

## What was built

Shipped 2026-08-19. Gates at ship: make test 95 passed; make style 24 OK / 0 FAIL; 20/20 annexes valid; 2084/2084 quotes grounded with strict anchors; git diff outputs/ empty; tree clean; the only typed numeral in the promoted document outside inline expressions is a '95 %' interval level. Reproduction check: the annexes-and-gates path plus the explicit re-render of the one changed document (check_render --render, docx and pdf, glyph check) — stated as such; a full make corpus would rewrite nineteen untouched rendered pairs with float noise. Moves: docs/results/README.md row; two HANDOFF §3a rows (the re-author with its re-anchoring counts; the RUNNER sentence from run 1's self-measurement); TASKS.md trap 14 (an autonomous author with the reviewer's tool in reach will use it unasked); ROADMAP register row updated (fifth result, the split of registers, what remains is the owner's call); the proposal rewritten down to what remains and kept (the owner has not decided about the rest); docs/next/README.md row; docs/pm epic, archive row, board; D5 and D6 settled; CLAUDE.md depth band unchanged (50 pp inside 41–56).

## Files it touched

- [[README]] — `docs/results/README.md`
- [[HANDOFF]] — `authoring/HANDOFF.md`
- [[ROADMAP]] — `docs/ROADMAP.md`
- [[register-from-four-sources]] — `docs/next/register-from-four-sources.md`
- [[README]] — `docs/next/README.md`
- `CLAUDE.md`
- [[TASKS]] — `pc_package/TASKS.md`
