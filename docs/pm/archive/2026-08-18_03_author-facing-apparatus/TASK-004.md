---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-004
status: done
kind: measurement
title: "The blind reading, recorded verbatim, then the decision rule applied \u2014 HALT for the owner"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-005"]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-004 — The blind reading, recorded verbatim, then the decision rule applied — HALT for the owner

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

This task cannot be finished by the assistant alone; it ends the session's turn with A.pdf and B.pdf ready and D4 open, and resumes when the reading arrives. Same order as all four previous readings: read, record verbatim, then count. The owner has read the shipped text four times today and may recognise it (exploration §4); record that as a limit, do not try to disguise the text. If the owner's answer does not map onto the rule (e.g. 'both are bad'), that is FAIL by the rule's wording, and the outcome says the rule was applied as written.

## Acceptance criteria

- [x] A.pdf and B.pdf are the EXCERPT and PROBE renders copied under the letters blind-key.md assigns, with the source filename not visible in the PDF metadata or title (subtitle line identical in both); the owner is told only: 'two versions of the same two subsections of PCR-005; quote the sentences that read as machine prose, and say which reads as a paper'
- [x] owner-reading-<date>.md holds the owner's answer VERBATIM, dated, with A/B still unresolved in the text, written BEFORE any count is taken and before blind-key.md is opened in the conversation
- [x] below the verbatim reading, the same file resolves the key, lists the quoted sentences per source (shipped vs probe) with counts, and applies decisions.decision_rule mechanically: PASS iff probe judged better AND fewer than three probe sentences quoted
- [x] decisions.probe_outcome in state.json is set to PASS or FAIL with the date; D4-does-the-probe-pass.md is set to `status: settled <date> — PASS|FAIL`; on FAIL, TASK-006..TASK-010 are set to status cancelled with `cancelled_by: D4` and TASK-011/TASK-012 still run
- [x] the outcome states, in one line, what the owner said about the shipped text and about the probe, without paraphrase

**Depends on:** [[TASK-003]]

## What was built

HALTED FOR THE OWNER, 2026-08-18. A.pdf and B.pdf are in the unit, copied under the letters blind-key.md assigns by a shell command that printed neither the key nor the file sizes; PDF metadata (title, author, subject) identical in both. The key has not been opened in the conversation. What is asked of the owner: two versions of the same two subsections of PCR-005 (Response-surface models, Mechanistic interpretation); quote the sentences that read as machine prose, and say which reads as a paper. The answer goes VERBATIM into owner-reading-<date>.md before the key is opened and before any count is taken; then the rule in decisions.decision_rule is applied and D4 settled.

RESUMED AND COMPLETED 2026-08-19. The reading arrived in three messages, each recorded verbatim in owner-reading-2026-08-19.md before the next step: (1) 'yes, the pdfs read fine. Explain step by step what did you change?' — (2) 'I did not know that there is a difference, I read just A.pdf yet. Should I read B too, I guess?' — so (1) was A alone, nothing quoted — (3) after B: 'A clearly wins'. No sentence quoted from either file. Then the key was opened: probe = A, checksum-verified (A.pdf == PROBE.pdf, B.pdf == EXCERPT.pdf). Rule applied mechanically: probe judged the better text, 0 sentences quoted from it -> D4 = PASS. What the owner said about the shipped text: nothing — it was read second and lost. What the owner said about the probe: 'the pdfs read fine' (read alone), 'A clearly wins' (against the shipped text). Limit as recorded in D4: the shipped text had been read four times the day before.

## Documents it is about

- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`

## Files it touched

- `.claude/work/2026-08-18_03_author-facing-apparatus/A.pdf`
- `.claude/work/2026-08-18_03_author-facing-apparatus/B.pdf`
- `.claude/work/2026-08-18_03_author-facing-apparatus/owner-reading-<date>.md`
- [[D4-does-the-probe-pass]] — `docs/pm/decisions/D4-does-the-probe-pass.md`
