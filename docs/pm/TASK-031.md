---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-031
status: done
kind: measurement
title: "Sampled blind reading of one document from batch B4 \u2014 measurement, not a gate (D8)"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCP-006", "PCP-007"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-031 — Sampled blind reading of one document from batch B4 — measurement, not a gate (D8)

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Not a hard stop. The reading still runs exactly as READING.md specifies — blind, key drawn and sealed before staging, the answer recorded verbatim and committed before the key is opened, the rule applied mechanically — because a reading that cannot fail measures nothing. What changed on 2026-08-21 is only the consequence: the owner is happy with the documents, keeps every promoted one, and released both remaining batches, so the verdict feeds the results page instead of the schedule. The reading is of the promoted document, so a FAIL still means a shipped document the owner reads as the weaker text: record it plainly, never revert silently.

## Acceptance criteria

- [x] the owner names one document of the batch; its OLD pdf (saved in the annex task) and the promoted pdf copied to A.pdf/B.pdf under a key drawn then (secrets.choice), no key/size/page count printed; READING.md's sampled-reading text delivered
- [x] the answer recorded VERBATIM before the key is opened by checksum; decisions.pass_rule applied mechanically; D8's table gains the batch's row (document, verdict, date)
- [x] the verdict is RECORDED and carried to the results page; it releases nothing and blocks nothing. Owner's decision of 2026-08-21: B4 and B5 are both released in advance and every promoted document stays, so a FAIL is a finding about the pipeline and not a disposition of the corpus. If a FAIL names a defect in a specific document, put it to the owner as a question rather than acting on it.

**Depends on:** [[TASK-030]]

## What was built

NOT RUN, by the owner's decision of 2026-08-21: asked whether to read PCP-003 or PCP-007 blind, the owner answered 'just proceed with the rest of the documents'. No blind key was drawn and nothing was staged, so no reading was begun and abandoned. Under D8's amendment of the same day the reading was already a measurement rather than a gate — B4 and B5 were released in advance and every promoted document stays — so declining it costs the results page one data point and blocks nothing. The evidence saved in TASK-030 keeps the reading available later: B4-old-PCP-003.pdf (29 pp) and B4-old-PCP-007.pdf (30 pp) are the pre-campaign texts, committed beside the promoted ones. The campaign's plan-side tally therefore stays at ONE reading, B3's PCP-006, which was its narrowest result. Recorded before the choice was put: this session had spent part of PCP-007's acceptance criteria section in conversation with the owner (the safety-factor sentence and the assurance-factor change), while none of READING.md's five suggested sections had been quoted for PCP-003.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCP-006** — `pc_package/PCP-006_viral_inactivation.qmd`
- **PCP-007** — `pc_package/PCP-007_cex.qmd`

## Files it touched

- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/owner-reading-B4-<date>.md`
- [[D8-do-the-batches-continue]] — `docs/pm/decisions/D8-do-the-batches-continue.md`
