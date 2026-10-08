---
type: pm-epic
sprint: 2026-08-19_02_fifth-round-plan-then-batches
status: delivered 2026-08-21
started: 2026-08-19
proposal: docs/next/register-from-four-sources.md
tags: [pm/epic]
---

> **DELIVERED 2026-08-21.** Every one of the 20 corpus documents is now written under the rebuilt
> apparatus, in one pass by one fresh-context agent, each with one content-review cycle and a
> transcript audit. The register split this epic existed to close is closed. Final state:
> **2089/2089 quotes grounded across 20 annexes**, 20/20 valid, 0 weak anchors, and the corpus
> reproduces from `make clean && make data figures corpus` with `outputs/` byte-identical.
>
> **What did not ship.** The last two sampled blind readings were declined by the owner, so eleven
> of the twenty documents were promoted on the content review and the gates alone. Two machinery
> defects are recorded and deliberately unfixed (the `show()`/tabulate float trap, and the split
> convention for `registered_sentence`), and the round introduced a tic of its own — `rather than`
> rose from 0.0 to 1.8 per 1k words corpus-wide and is not repaired.
>
> Measurements: [`docs/results/2026-08-21-fifth-round-batches.md`](../results/2026-08-21-fifth-round-batches.md).
> What remains is [Track C](../next/register-from-four-sources.md).

# Epic — the fifth round: one plan first, then the batches

Board: [[_Board]] · decisions: [[D7-does-the-plan-pass]], [[D8-do-the-batches-continue]] ·
proposal: [`docs/next/register-from-four-sources.md`](../next/register-from-four-sources.md) ·
exploration: `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/exploration.md` · plan:
`.claude/work/2026-08-19_02_fifth-round-plan-then-batches/implementation-plan.md` · what it follows:
[`docs/results/2026-08-19-fourth-round-PCR-007.md`](../results/2026-08-19-fourth-round-PCR-007.md)

**Why it opened.** `PCR-007` under the rebuilt apparatus was preferred blind by the owner and is in
the corpus; the corpus is split across five registers (one document at the rebuilt one, fourteen at
round zero, five at earlier rounds), which is a confound in every experiment run on it. The owner
decided on 2026-08-19: `PCP-005` first — a plan, the genre not yet tested — then finish the set with
the regime frozen and one sampled reading per batch.

**What it does.** Authors `PCP-005` under exactly the `PCR-007` loop (one agent, the RUNNER's
inputs, no counter, transcript audit, one content-review cycle) and puts it in front of the owner
blind (D7). On PASS: eighteen documents in five batches — reports first, the discrepancy carriers
spread, the earlier-round documents re-done, `PCMR-001` last — each batch promoted, re-anchored and
re-grounded as one serial annex step and one document of it read blind by the owner (D8). Then the
campaign's closing measurement: the whole corpus against the Track D baseline on the same script.

**What it does not do.** Change the apparatus; run `make data figures`; add a gate or a counter;
have the owner read all eighteen.

**The shape.** 41 tasks: the pilot (6) → B1 (7) → B2 (6) → B3 (8) → B4 (5) → B5 (7) → page → ship.
Every reading is a hard stop.
