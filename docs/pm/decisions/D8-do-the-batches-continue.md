---
type: pm-decision
sprint: 2026-08-19_02_fifth-round-plan-then-batches
status: open
waiting_on: project owner
blocks: each batch's successor (TASK-014.., TASK-020.., TASK-028.., TASK-033..) until its row reads PASS
tags: [pm/decision]
---

# D8 — after each batch, does the sampled document pass, and do the batches continue?

**What is being asked, once per batch.** After a batch is promoted and the corpus re-grounded, you
name one document of the batch. Its old pdf (saved before promotion) and its promoted pdf are
put in front of you as `A.pdf`/`B.pdf`, key sealed; same two questions, same rule as every reading
(new preferred and fewer than five sentences quoted from it). A PASS releases the next batch. A
FAIL stops the unit: a document you reject is then already in the corpus, and the choice is yours —
re-author it under the same regime, or restore the old text by name.

**Why a sample and not all eighteen.** Your reading has agreed with the pipeline three times since
the rebuild (the probe, `PCR-007`, and — if D7 passes — `PCP-005`). One reading per batch keeps the
human check where it is worth most, at the boundary between batches, at a fifth of the cost.

| batch | documents | document read | verdict | date |
|---|---|---|---|---|
| B1 | PCR-006, PCR-008, PCR-009, PCR-010 | PCR-008 | **FAIL — the owner preferred the OLD text** ("clearly A wins. I could not find sentences in A which sound machine written"; A was the old document) | 2026-08-20 |
| B1 (second sample, option D) | — | PCR-009 | **PASS — the owner preferred the NEW text** ("I like A better, it has shorter sentences and explains everything a bit more clearly") | 2026-08-20 |
| B2 | PCR-004, PCR-003, PCR-005 | — | — | — |
| B3 | PCP-004, PCP-006, PCP-008, PCP-009, PCP-010 | — | — | — |
| B4 | PCP-003, PCP-007 | — | — | — |
| B5 | PTP-001, PCMP-001, RA-001, PCMR-001 | — | — | — |

**What the plan assumes meanwhile.** Each batch's document tasks start only after the previous
batch's row reads PASS.

---

**B1 read on 2026-08-20 — FAIL, and the unit is stopped.** The promoted `PCR-008` stays in the
corpus until you decide. The options:

**Option A — re-author `PCR-008`** under the same regime (a fresh one-pass agent, one review
cycle, another blind reading of old vs new). Costs one authoring day; tests whether this was a
draw of the die or a property of the document.

**Option B — revert `PCR-008` to the old text by name** (restore its qmd/docx/pdf, its 25-span
YAML and the `ax_*` builder region from the commit before promotion, re-ground). The corpus then
carries the old register for this one document, deliberately recorded.

**Option C — accept the new `PCR-008` and continue to B2.** Your reading found no machine sentence
in either text; the preference was for A on overall reading quality. If you can say what A does
better, that becomes a finding for the regime; if not, this may be reading noise, and the next
sample will tell.

Also worth weighing: `PCR-006`, `PCR-009` and `PCR-010` from the same batch were promoted on the
same pipeline and have not been read — a second sample from B1 (Option D) would say whether
`PCR-008` is an outlier before anything is re-done.

---

**With both samples in (2026-08-20):** the regime's effect is what the owner names as the reason
for preferring the new `PCR-009`; `PCR-008` is the outlier, an old text the owner reads as clean.
What remains to decide is `PCR-008` itself — re-author under the same regime and re-read blind
(recommended), revert it by name, or accept the promoted text — and whether B2 releases now on the
`PCR-009` PASS (recommended) or waits for the `PCR-008` disposition.

---

**PCR-008 disposition decided 2026-08-20: re-author (attempt 2), owner's decision, in a fresh
session.** TASK-042 (author + review) → TASK-043 (blind reading, round-zero vs attempt 2) →
TASK-044 (promote or revert by name). **B2's release remains undecided** and its tasks stay
blocked until the owner releases them.
