---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-018
status: done
kind: measurement
title: "Sampled blind reading of one document from batch B2 \u2014 HALT for the owner (D8)"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-003", "PCR-004", "PCR-005", "PCR-008"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-018 — Sampled blind reading of one document from batch B2 — HALT for the owner (D8)

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

HARD STOP. The reading is of the promoted document, so a FAIL means a shipped document the owner rejects is in the corpus: record it, do not revert silently — the owner decides whether to re-author it or to revert to the old text by name.

## Acceptance criteria

- [x] the owner names one document of the batch; its OLD pdf (saved in the annex task) and the promoted pdf copied to A.pdf/B.pdf under a key drawn then (secrets.choice), no key/size/page count printed; READING.md's sampled-reading text delivered
- [x] the answer recorded VERBATIM before the key is opened by checksum; decisions.pass_rule applied mechanically; D8's table gains the batch's row (document, verdict, date)
- [x] PASS releases the next batch; FAIL stops the unit: the next batch's document tasks are set blocked with the reason, and the owner decides in D8

**Depends on:** [[TASK-017]]

## What was built

Three pairs staged, one per B2 document, each under its own independently drawn key. FIRST DRAW WAS VOIDED: this session printed each 8-byte key file's MD5, and having already printed the same MD5 for blind-key-B1c.md (later revealed as new = B), the checksums identified all three keys. Re-drawn with a random nonce per key file so neither length nor checksum carries information, no checksum printed, keys committed sealed in fae3ee6. Reading recorded VERBATIM and committed before the keys were opened, then keys opened and verified by first-pages text hash. RESULT: PCR-003 PASS (new preferred, 0 sentences quoted from it, the one quoted passage is from the old text and was verified present in B2-old-PCR-003.pdf and absent from the promoted pdf before the keys were opened). PCR-004 FAIL (old preferred). PCR-005 not read. NOT FULLY BLIND FOR PCR-004, AND THIS SESSION CAUSED IT: it printed the §6 paragraphs of the three NEW documents earlier in the same conversation while analysing the owner's cross-document ranking, and §6 is the paragraph the owner then read in each pair. A warning that '§6 is spent' was given before the reading. PCR-003 is clean: its new §6 was never printed here and the owner identified the old text from the prose alone. The split falls on the DoE/non-DoE line: PCR-004 is the batch's only non-DoE report and its §6 explains the absence of a design space rather than describing one. Its review counts converged BEST of the batch (4/0/0/8) and the owner likes it least; PCR-008 attempt 3 converged WORST (17/4/7/12) and the owner likes it most.

## Documents it is about

- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-004** — `pc_package/PCR-004_harvest.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`

## Files it touched

- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/owner-reading-B2-<date>.md`
- [[D8-do-the-batches-continue]] — `docs/pm/decisions/D8-do-the-batches-continue.md`
