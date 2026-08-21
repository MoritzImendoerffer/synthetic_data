---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-038
status: done
kind: measurement
title: "Sampled blind reading of one document from batch B5 \u2014 measurement, not a gate (D8)"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCMP-001", "PCMR-001", "PCP-006", "PTP-001", "RA-001"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-038 — Sampled blind reading of one document from batch B5 — measurement, not a gate (D8)

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Not a hard stop. The reading still runs exactly as READING.md specifies — blind, key drawn and sealed before staging, the answer recorded verbatim and committed before the key is opened, the rule applied mechanically — because a reading that cannot fail measures nothing. What changed on 2026-08-21 is only the consequence: the owner is happy with the documents, keeps every promoted one, and released both remaining batches, so the verdict feeds the results page instead of the schedule. The reading is of the promoted document, so a FAIL still means a shipped document the owner reads as the weaker text: record it plainly, never revert silently.

## Acceptance criteria

- [x] the owner names one document of the batch; its OLD pdf (saved in the annex task) and the promoted pdf copied to A.pdf/B.pdf under a key drawn then (secrets.choice), no key/size/page count printed; READING.md's sampled-reading text delivered
- [x] the answer recorded VERBATIM before the key is opened by checksum; decisions.pass_rule applied mechanically; D8's table gains the batch's row (document, verdict, date)
- [x] the verdict is RECORDED and carried to the results page; it releases nothing and blocks nothing. Owner's decision of 2026-08-21: B4 and B5 are both released in advance and every promoted document stays, so a FAIL is a finding about the pipeline and not a disposition of the corpus. If a FAIL names a defect in a specific document, put it to the owner as a question rather than acting on it.

**Depends on:** [[TASK-037]]

## What was built

NOT RUN, by the owner's decision of 2026-08-21: 'skip the reading and finish the batch'. No blind key was drawn and nothing was staged, so no reading was begun and abandoned. This is the second declined sampled reading of the campaign, after B4's, and for the same reason: D8's amendment of the same day had already demoted both to measurements, released both batches in advance and settled that every promoted document stays, so a verdict could change nothing. The evidence is kept and the reading stays available: B5-old-PTP-001.pdf (24 pp), B5-old-PCMP-001.pdf (25 pp), B5-old-RA-001.pdf (30 pp) and B5-old-PCMR-001.pdf (34 pp) are the pre-campaign texts, committed beside the promoted ones. CONSEQUENCE FOR THE RESULTS PAGE, to be stated plainly rather than left to be inferred: the campaign ran NINE readings in total, all of them on documents from B1 to B3, and none on the nine documents of B4 and B5. The plan-side tally rests on a single reading, B3's PCP-006, which was also the narrowest result of the campaign and was reversed by the owner once the key was open. Eleven of the twenty documents were promoted on the content review and the gates alone.

## Documents it is about

- **PCMP-001** — `pc_package/PCMP-001_master_plan.qmd`
- **PCMR-001** — `pc_package/PCMR-001_master_report.qmd`
- **PCP-006** — `pc_package/PCP-006_viral_inactivation.qmd`
- **PTP-001** — `pc_package/PTP-001_transfer.qmd`
- **RA-001** — `pc_package/RA-001_risk_assessment.qmd`

## Files it touched

- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/owner-reading-B5-<date>.md`
- [[D8-do-the-batches-continue]] — `docs/pm/decisions/D8-do-the-batches-continue.md`
