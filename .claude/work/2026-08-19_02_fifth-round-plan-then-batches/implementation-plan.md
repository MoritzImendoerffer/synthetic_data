# Implementation plan — the fifth round: `PCP-005` first, then the batches

**Proposal:** `docs/next/register-from-four-sources.md`, its "what remains" pointer.
**Exploration:** `exploration.md`. **Task list:** `state.json` (41 tasks). **Written:** 2026-08-19.
**Owner's decisions at open:** `PCP-005` first; the regime frozen; one sampled reading per batch.

## What is being built

The rest of the corpus at one register. First a plan, `PCP-005`, under exactly the loop that
delivered `PCR-007` — one agent, one pass, the RUNNER's inputs, no counter, one content-review
cycle, a transcript audit — read blind by the owner under the unchanged rule. Then, on a PASS,
eighteen documents in five batches, each batch promoted, re-anchored and re-grounded as one
serial annex step, with the owner reading one document per batch blind against its old version.
A results page for the pilot, one for the batches, and the campaign's closing measurement: the
whole corpus against the Track D baseline on the same script.

## The order, and why

```
pilot    TASK-001 inputs → TASK-002 author+review PCP-005 → TASK-003 reading (HARD STOP, D7)
         → TASK-004 page; on PASS TASK-005 promote → TASK-006 proof
B1       TASK-007..010 PCR-006/008/009/010 (parallel) → TASK-011 annex (serial) → TASK-012 reading (HARD STOP, D8) + TASK-013 proof
B2       TASK-014..016 PCR-004/003/005 → TASK-017 → TASK-018 + TASK-019
B3       TASK-020..024 PCP-004/006/008/009/010 → TASK-025 → TASK-026 + TASK-027
B4       TASK-028..029 PCP-003/007 → TASK-030 → TASK-031 + TASK-032
B5       TASK-033..035 PTP/PCMP/RA → TASK-036 PCMR-001 (last) → TASK-037 → TASK-038 + TASK-039
close    TASK-040 batches' page → TASK-041 ship
```

**The plan genre first**, because half the corpus is plans and nothing has tested the regime on
one; it is also the cheapest document to re-anchor (48 quotes, no spans).

**Reports before plans in the batches**, because the report is the tested genre and carries the
rhetorical layers (282 spans across eight reports) — the expensive, error-prone part is done
while the loop is freshest. **The discrepancy carriers are spread** (B1 three of D-001, B2 D-002,
B3 three of D-001, B4 one) so no batch is all of them. **The earlier-round documents** (`PCR-003`,
`PCR-005`, `PCP-003`, `PCP-007`, `RA-001`) are re-done so the corpus carries one register —
assumed from the owner's "finish the set", overrulable. **`PCMR-001` last**, after every report is
promoted, because it rolls them up.

**Each batch's reading gates the next batch.** A FAIL on a sampled reading means a shipped document
the owner rejects is in the corpus; the unit stops, records it, and the owner decides (D8) — re-author
it, or restore the old text by name.

**Serial annex.** `build_ground_truth.py` is one file; no annex task overlaps another or any
authoring. Document tasks inside a batch may run concurrently.

## What this plan decided (overrulable)

- Pass rule unchanged (new preferred, fewer than five sentences quoted).
- One content-review cycle per document, then on to the annex whatever the second run says.
- Batch composition and order as above.
- The five earlier-round documents are included.
- The old pdf of every document is saved before promotion, so a sampled reading can be blind.

## What is the owner's

D7 (does the plan pass), D8 (per batch: does the sampled document pass, do the batches continue),
and which document of each batch is read.

## What could go wrong

- **A plan is a different genre**: prospective voice, `plan_params`, no findings, already a high
  passive rate (66.7 %). The reading decides; the counters are not a target.
- **Self-measurement again**: the audit runs before any draft is read; a contaminated draft is set
  aside and re-run with the same prompt (it cost 46 minutes once).
- **Discrepancy carriers**: seven documents; brief §5c carries the assignment; ANNEX-A-BATCH §5
  verifies the registered sentence in the new docx and updates both files together if the wording
  moved. TASKS.md item 7 is the failure.
- **`PCMR-001`**'s 49 spans include 17 data-row spans that rebuild themselves; its brief must be
  rebuilt after the reports are promoted, or it rolls up stale text.
- **Rendered pairs**: `check_render --render` rewrites a docx; restore by name; commit only the
  batch's own renders. `make style` counts untracked DRAFTs.
- **Scale**: eighteen authorings at ~30–45 min, five annex steps, five readings. Days, not hours.
  Every boundary green: at the end of every annex task the corpus validates and grounds.

## What will not be attempted

No `make data figures`; no change to the apparatus; no new gate or counter; no document outside
the batch being worked; no reading of all eighteen by the owner.
