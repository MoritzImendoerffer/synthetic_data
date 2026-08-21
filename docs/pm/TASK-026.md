---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-026
status: done
kind: measurement
title: "Sampled blind reading of one document from batch B3 \u2014 HALT for the owner (D8)"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-006", "PCR-005"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-026 — Sampled blind reading of one document from batch B3 — HALT for the owner (D8)

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

HARD STOP. The reading is of the promoted document, so a FAIL means a shipped document the owner rejects is in the corpus: record it, do not revert silently — the owner decides whether to re-author it or to revert to the old text by name.

## Acceptance criteria

- [x] the owner names one document of the batch; its OLD pdf (saved in the annex task) and the promoted pdf copied to A.pdf/B.pdf under a key drawn then (secrets.choice), no key/size/page count printed; READING.md's sampled-reading text delivered
- [x] the answer recorded VERBATIM before the key is opened by checksum; decisions.pass_rule applied mechanically; D8's table gains the batch's row (document, verdict, date)
- [x] PASS releases the next batch; FAIL stops the unit: the next batch's document tasks are set blocked with the reason, and the owner decides in D8

**Depends on:** [[TASK-025]]

## What was built

Owner named PCP-006 from the five B3 plans. Pair staged from B3-old-PCP-006.pdf and the promoted pdf under blind-key-B3-PCP-006.md, drawn with a nonce, no checksum printed, dates normalised. No section of any B3 document had been quoted in the session, so the whole document was clean to read. Reading recorded VERBATIM and committed before the key was opened; key opened and verified by first-pages text hash. Key: new = B. RULE: new judged better = NO ('a close win for A', A being the pre-campaign plan); sentences quoted from the new text = 3, which would have satisfied the second leg. FAIL on the first leg. NARROWEST RESULT OF THE CAMPAIGN, and the owner said so unprompted — 'it is close to a tie' — and for the first time in eight readings credited the losing text with something: 'in B the mechanistic descriptions are sometimes more accurate'. ONE OF THE THREE FLAGGED SENTENCES WAS CREATED BY THE REVIEW CYCLE, traced through the files before the key was opened: run 1 flagged the trailing gloss 'which is what allows the study to find the edge of acceptable operation rather than merely to confirm the centre'; the author removed it and wrote a DIFFERENT trailing gloss onto the same sentence, 'and each edge is placed where it is for a reason of its own'; run 2 did not flag the replacement; the owner did. Second confirmed instance of this failure after PCR-005's binding response -> rejects, and the first traced through the files rather than inferred. A one-cycle review is not self-correcting on the construction it flags. The other two flagged sentences were in the pre-review draft, survived untouched and were never flagged by either judge; both are §7, the section the owner separately called more rigorous in the pre-campaign text. Genre score is now plans 1 PASS / 1 FAIL against reports 3 PASS / 3 FAIL — nothing separates them.

## Documents it is about

- **PCP-006** — `pc_package/PCP-006_viral_inactivation.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`

## Files it touched

- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/owner-reading-B3-<date>.md`
- [[D8-do-the-batches-continue]] — `docs/pm/decisions/D8-do-the-batches-continue.md`
