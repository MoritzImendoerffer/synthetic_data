---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-012
status: done
kind: measurement
title: "Sampled blind reading of one document from batch B1 \u2014 HALT for the owner (D8)"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-006", "PCR-007", "PCR-008", "PCR-009", "PCR-010"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-012 — Sampled blind reading of one document from batch B1 — HALT for the owner (D8)

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

HARD STOP. The reading is of the promoted document, so a FAIL means a shipped document the owner rejects is in the corpus: record it, do not revert silently — the owner decides whether to re-author it or to revert to the old text by name.

## Acceptance criteria

- [x] the owner names one document of the batch; its OLD pdf (saved in the annex task) and the promoted pdf copied to A.pdf/B.pdf under a key drawn then (secrets.choice), no key/size/page count printed; READING.md's sampled-reading text delivered
- [x] the answer recorded VERBATIM before the key is opened by checksum; decisions.pass_rule applied mechanically; D8's table gains the batch's row (document, verdict, date)
- [x] PASS releases the next batch; FAIL stops the unit: the next batch's document tasks are set blocked with the reason, and the owner decides in D8

**Depends on:** [[TASK-011]]

## What was built

HALTED FOR THE OWNER, 2026-08-19. Batch B1 is promoted and re-grounded. The owner names ONE of PCR-006 (Low-pH Viral Inactivation, 45 pp), PCR-008 (Anion Exchange, 54 pp), PCR-009 (Small-Virus Retentive Filtration, 34 pp), PCR-010 (UF/DF, non-DoE, 30 pp); its old pdf (B1-old-<DOC>.pdf, saved before promotion) and its promoted pdf are then copied to A.pdf/B.pdf under a key drawn at that moment (no key, size or page count printed), with READING.md's sampled-reading text. Recorded verbatim before the key is opened; the rule applied; D8's B1 row filled. OWNER NAMED PCR-008 (2026-08-20). A.pdf/B.pdf copied under blind-key-B1.md (drawn now, unopened; no size or page count printed — the two versions differ by one page, which the session knows and does not say).

RESUMED AND COMPLETED 2026-08-20 — FAIL. Reading verbatim: 'clearly A wins. I could not find sentences in A which sound machine written'. Key: new = B; A was the OLD PCR-008 (checksums against the promoted pdf and B1-old-PCR-008.pdf). Rule: the new document was not judged better -> FAIL. First blind reading in the campaign where the owner preferred the round-zero text, and the owner found no machine sentence in it (for PCR-007 the same owner quoted three from the old text). B2 is blocked; the promoted PCR-008 stays until the owner decides (D8): re-author under the same regime, revert to the old text by name (restore qmd/docx/pdf, spans yaml and the ax_* builder region from 8327605~1), or accept and continue. Nothing reverted silently. SECOND SAMPLE (Option D), 2026-08-20: the owner named PCR-009; A.pdf/B.pdf replaced under blind-key-B1b.md (drawn now, unopened; no size or page count printed).

SECOND SAMPLE RESULT, 2026-08-20 — PASS. Verbatim: 'I like A better, it has shorter sentences and explains everythinga bit more clearly.' Key: new = A (checksum-verified). Rule: new judged better, 0 quoted -> PASS, with the reason naming exactly the regime's effect. B1 stands at one FAIL (PCR-008) and one PASS (PCR-009); PCR-008's disposition and the release of B2 are the owner's call in D8.

## Documents it is about

- **PCR-006** — `pc_package/PCR-006_viral_inactivation.qmd`
- **PCR-007** — `pc_package/PCR-007_cex.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`
- **PCR-009** — `pc_package/PCR-009_virus_filtration.qmd`
- **PCR-010** — `pc_package/PCR-010_ufdf.qmd`

## Files it touched

- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/owner-reading-B1-<date>.md`
- [[D8-do-the-batches-continue]] — `docs/pm/decisions/D8-do-the-batches-continue.md`
