---
type: pm-decision
sprint: 2026-08-19_02_fifth-round-plan-then-batches
status: decided
waiting_on: project owner
blocks: nothing since 2026-08-20 — B2 released by the owner; readings continue one per batch
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
| B1 (PCR-008 attempt 2, re-author) | — | PCR-008 | **FAIL — the owner preferred the ROUND-ZERO text** ("I like A better. The reasoning is better to understand and follow"); five sentences quoted from the new text as sounding AI generated | 2026-08-20 |
| B2 | PCR-004, PCR-003, PCR-005 | PCR-003 | **PASS — the owner preferred the NEW text**, quoting a sentence against the old one | 2026-08-20 |
| B2 (second document read) | — | PCR-004 | **FAIL — the owner preferred the OLD text** ("for PCR-004 i like the old one better"); the batch's only non-DoE report | 2026-08-20 |
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

---

**PCR-008 attempt 2 read on 2026-08-20 — FAIL, on both legs of the rule.** The owner preferred the
round-zero text again and quoted five sentences from the new one, so the re-author did not
reproduce the `PCR-009` result. Two attempts at this document under the same frozen regime have now
lost to the text that preceded the campaign, which answers the question TASK-042 was set to test:
attempt 1 was not simply a bad draw.

This reading, unlike the first, says why. Both quoted passages are the scale-down model
qualification paragraph. The round-zero paragraph explains what the scaling convention buys
("This convention holds residence time and mass transport constant across scales"); the attempt-2
paragraph lists what the model keeps and never says why keeping those things makes it a model. The
owner's ground was "the reasoning is better to understand and follow". Recorded in full in
`owner-reading-B1c-2026-08-20.md` and carried to the results page.

**Disposition, per the plan:** TASK-044 reverts `PCR-008` to the round-zero text by name — the
qmd, docx, pdf and 25-span YAML from the commit before promotion, and only the `ax_*` report
branches of `build_ground_truth.py`, which has moved since. The corpus then carries the old
register for this one document, deliberately and on the record.

**Two questions are open for the project owner.**

1. **Does B2 release?** It has been undecided since the first `PCR-008` FAIL and its tasks
   (TASK-014, TASK-015, TASK-016) are still blocked. The evidence is now three sampled readings
   PASS (the probe, `PCR-007`, `PCP-005`, and `PCR-009` in B1) against two FAILs, both of them on
   `PCR-008`. On that record `PCR-008` looks like the outlier the second B1 sample suggested it was,
   and B2 releasing is the reading of the evidence; the alternative is to treat the paragraph-level
   finding above as a reason to stop and change the regime first.
2. **Does the scale-down qualification finding change the regime?** The regime is frozen for the
   duration of the unit by the owner's own decision, and a change mid-campaign re-splits the
   corpus. The finding is recorded either way.

---

**Resolved by the project owner, 2026-08-20, after the attempt-2 reading.**

The owner's reading of the outcome is that question 1 of the content review is a good rule badly
placed: it was given to the reviewer after the fact and never to the author. The round-zero
paragraph they preferred satisfies it — "This convention holds residence time and mass transport
constant across scales" names what the convention does, in the clause with the verb — while the
attempt-2 inventory names nothing. So the rule moves into the author's guide.

Three decisions, all the owner's:

1. **The frozen regime is amended, once and narrowly.** Rule 4 of `authoring/WRITING_GUIDE.md` now
   says the cause stands in the clause where the causal verb stands, and that where the cause is a
   convention, a procedure or a design choice rather than a species, the sentence says what it
   holds constant or what follows from it. No counter and no threshold reaches the author, and
   `REVIEW_CHECKLIST.md`, `RUNNER.md`, `section_plan.yaml`, `check_style.py` and the launch prompt
   are untouched (TASK-045).
2. **B2 releases and the campaign proceeds** under the amended guide. TASK-014, TASK-015 and
   TASK-016 are unblocked.
3. **`PCR-008` is re-authored a third time under the rule** rather than reverted or promoted as
   attempt 2, running alongside B2 so it costs no campaign time (TASK-046 → TASK-047 → TASK-048).
   The promoted attempt 1 stays in the corpus until that reading disposes of it.

**What this splits, deliberately.** `PCP-005`, `PCR-006`, `PCR-009`, `PCR-010` and `PCR-007` were
authored before the rule and stand as they are; the owner read `PCR-009` blind and preferred it in
that register. The corpus will carry two vintages until someone decides otherwise, and that is
noted at ship rather than repaired now.

**One interaction left open, for the results page.** The reviewer's question 1 still exempts no
procedural or statistical "because", and run 2 of the attempt-2 review flagged eight correct
sentences under it ("because every effect is a contrast over all runs"). The author-facing rule now
covers the convention case, but a review return can still push an author to delete correct prose.
Watched, not changed, because changing the reviewer's questions mid-campaign would re-split the
measurement as well as the corpus.

---

**B3 released and PCR-004 re-authored, both decided by the owner on 2026-08-20.**

B3 (the five plans PCP-004, PCP-006, PCP-008, PCP-009, PCP-010) is released and authoring despite
the B2 split, on the PCR-003 PASS.

`PCR-004` is re-authored as attempt 2 rather than reverted or accepted (TASK-049 → TASK-050 →
TASK-051), running alongside B3 so it costs no campaign time. The promoted attempt 1 stays in the
corpus until that reading disposes of it.

**One thing not to over-read when the result comes.** The `PCR-008` sequence had a variable in it:
attempts 1 and 2 were written before rule 4 was amended and attempt 3 after, so the amendment was
what changed. `PCR-004` attempt 1 was already written under the amended rule, so attempt 2 under an
unchanged regime tests the draw and nothing else. If it passes, that says the first draft was
unlucky; if it fails again, that is the second independent signal that a non-DoE report is where
this apparatus is weakest — and `PCP-004` and `PCP-010`, the plans for the two steps without a DoE,
are in B3 and will say the same thing or not.

**Still open, and nobody has decided it:** whether the non-DoE case needs its own rule, and whether
the reviewer's question 1 should gain a scope line so it stops flagging true statements that a step
governs nothing. Both are recorded findings, neither is acted on.

