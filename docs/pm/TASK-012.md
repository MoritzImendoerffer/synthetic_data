---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-012
status: doing
kind: measurement
title: "Sampled blind reading of one document from batch B1 \u2014 HALT for the owner (D8)"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/doing]
about: ["PCR-006", "PCR-008", "PCR-009", "PCR-010"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-012 — Sampled blind reading of one document from batch B1 — HALT for the owner (D8)

**Epic:** [[epic]] · **Status:** `doing` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

HARD STOP. The reading is of the promoted document, so a FAIL means a shipped document the owner rejects is in the corpus: record it, do not revert silently — the owner decides whether to re-author it or to revert to the old text by name.

## Acceptance criteria

- [ ] the owner names one document of the batch; its OLD pdf (saved in the annex task) and the promoted pdf copied to A.pdf/B.pdf under a key drawn then (secrets.choice), no key/size/page count printed; READING.md's sampled-reading text delivered
- [ ] the answer recorded VERBATIM before the key is opened by checksum; decisions.pass_rule applied mechanically; D8's table gains the batch's row (document, verdict, date)
- [ ] PASS releases the next batch; FAIL stops the unit: the next batch's document tasks are set blocked with the reason, and the owner decides in D8

**Depends on:** [[TASK-011]]

## What was built

HALTED FOR THE OWNER, 2026-08-19. Batch B1 is promoted and re-grounded. The owner names ONE of PCR-006 (Low-pH Viral Inactivation, 45 pp), PCR-008 (Anion Exchange, 54 pp), PCR-009 (Small-Virus Retentive Filtration, 34 pp), PCR-010 (UF/DF, non-DoE, 30 pp); its old pdf (B1-old-<DOC>.pdf, saved before promotion) and its promoted pdf are then copied to A.pdf/B.pdf under a key drawn at that moment (no key, size or page count printed), with READING.md's sampled-reading text. Recorded verbatim before the key is opened; the rule applied; D8's B1 row filled.

## Documents it is about

- **PCR-006** — `pc_package/PCR-006_viral_inactivation.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`
- **PCR-009** — `pc_package/PCR-009_virus_filtration.qmd`
- **PCR-010** — `pc_package/PCR-010_ufdf.qmd`

## Files it touched

- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/owner-reading-B1-<date>.md`
- [[D8-do-the-batches-continue]] — `docs/pm/decisions/D8-do-the-batches-continue.md`
