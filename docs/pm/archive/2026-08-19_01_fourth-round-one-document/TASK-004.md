---
type: pm-task
epic: 2026-08-19_01_fourth-round-one-document
sprint: 2026-08-19_01_fourth-round-one-document
task: TASK-004
status: done
kind: measurement
title: "The blind reading of shipped vs new PCR-007, recorded verbatim, then the rule applied \u2014 HALT for the owner"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-007"]
---

> [!warning] Generated from `.claude/work/2026-08-19_01_fourth-round-one-document/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-004 — The blind reading of shipped vs new PCR-007, recorded verbatim, then the rule applied — HALT for the owner

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

HARD STOP: the session ends its turn with A.pdf and B.pdf ready, D6 open, and the READING.md text delivered; it resumes when the reading arrives. Same order as every reading in the campaign: read, record verbatim, then count. If the owner reads only one file first (it happened with the probe), record that message and ask for the other; the rule needs both.

## Acceptance criteria

- [x] A.pdf and B.pdf are the shipped pc_package/PCR-007_cex.pdf and the DRAFT's pdf copied under the letters blind-key.md assigns by a command that prints neither the key nor the file sizes; PDF metadata title/author identical (both are the same template); the owner is given procedures/READING.md's text and nothing about which is which
- [x] owner-reading-<date>.md holds every message of the owner's answer VERBATIM, dated, in order, written before the key is opened and before any count is taken; then the key resolved by checksum (A.pdf/B.pdf against the two source pdfs), the quoted sentences per source counted, and decisions.pass_rule applied mechanically
- [x] decisions.reading_outcome set to PASS or FAIL with the date; D6 set to `status: settled <date> — PASS|FAIL`; on FAIL, TASK-006 and TASK-007 set to cancelled with `cancelled_by: D6`, and TASK-005/TASK-008 still run
- [x] the outcome states in one line what the owner said about each document, without paraphrase, and the limit that applies (none of the previous 'fourth reading' kind — the owner has read neither version of PCR-007 before)

**Depends on:** [[TASK-003]]

## What was built

HALTED FOR THE OWNER, 2026-08-19. A.pdf and B.pdf are in the unit, copied under the letters blind-key.md assigns by a shell command that printed neither the key nor the file sizes; PDF metadata (title, author) identical. LIMIT, recorded: the session then printed the two page counts (51 and 50) and, knowing the shipped PCR-007 is 51 pages, can infer the key; the owner cannot, the key stays closed in the conversation, and the session says nothing about which is which. The owner is given procedures/READING.md's text: two versions of the whole PCR-007 report, the suggested subset (Executive summary; Results, all four subsections; Design space; Discussion), the two questions, and the rule. The reading is recorded verbatim before the key is opened by checksum and before any count.

RESUMED AND COMPLETED 2026-08-19. The reading arrived in one message, recorded verbatim before the key was opened: 'B is clearly bette to read', three distinct sentences quoted from A as machine-generated ('Yield is a process performance response and carries no quality claim, so that limitation does not touch the acceptance argument in Section 6.'; 'The aggregate coefficients in Table 5.6 confirm the screening picture and sharpen it.'; 'The host cell protein coefficients in Table 5.7 reproduce the two dominant main effects and the protein load interaction with conductivity, and they add a second interaction that the screening block did not resolve.'), none from B, 'B reads more like a paper'. Key: new = B, checksum-verified (B.pdf == DRAFT.pdf, A.pdf == shipped PCR-007_cex.pdf); each quoted sentence occurs once in the shipped .qmd and never in the new one. Rule applied mechanically: new judged better, 0 sentences quoted from it -> D6 = PASS. What the owner said about the shipped text: three sentences named as machine-generated; about the new one: 'clearly better to read', 'reads more like a paper'. No prior reading of either version.

## Documents it is about

- **PCR-007** — `pc_package/PCR-007_cex.qmd`

## Files it touched

- `.claude/work/2026-08-19_01_fourth-round-one-document/A.pdf`
- `.claude/work/2026-08-19_01_fourth-round-one-document/B.pdf`
- `.claude/work/2026-08-19_01_fourth-round-one-document/owner-reading-<date>.md`
- [[D6-does-the-whole-document-pass]] — `docs/pm/decisions/D6-does-the-whole-document-pass.md`
