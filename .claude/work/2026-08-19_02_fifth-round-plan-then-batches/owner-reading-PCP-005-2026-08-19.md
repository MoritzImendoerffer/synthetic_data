# Project owner's reading of the plan pilot (PCP-005) — 2026-08-19

Recorded VERBATIM, before the blind key is opened and before any measure is taken of either text.
`A.pdf` and `B.pdf` are the two files committed in `8f44cc2`; the owner was given the pilot text of
`procedures/READING.md`.

## The reading, verbatim (one message)

> A reads better. In B, following sentence clearly revealed it's origin: "Three mechanisms frame what the study expects to find.

## What the reading says, before the key

- Preference: **A** ("A reads better").
- Sentence quoted as machine prose: **one, from B** — "Three mechanisms frame what the study
  expects to find."
- Sentences quoted from A: none.

The reading is complete. The key is opened next, below this line, and the counts come after.

## The key, opened after the reading above was committed

`blind-key-PCP-005.md`: **new = A**. Verified by checksum: `A.pdf` is byte-identical to
`pc_package/PCP-005_protein_a.DRAFT.pdf` (the new plan, after one review cycle) and `B.pdf` to
`pc_package/PCP-005_protein_a.pdf` (the shipped plan). The quoted sentence, "Three mechanisms frame
what the study expects to find", occurs once in the shipped `.qmd` and never in the new one.

So: **A = the new PCP-005**; **B = the shipped PCP-005** (round zero).

## The rule, applied mechanically

`decisions.pass_rule`: PASS iff the owner judges the new document the better text AND quotes fewer
than five sentences from it across whatever was read.

- New document judged better: **yes** — "A reads better".
- Sentences quoted from the new document: **0**.
- Sentences quoted from the shipped document: 1 ("Three mechanisms frame what the study expects to
  find." — a sentence that announces the paragraph's shape, the Q4 frame the content review flags).

**D7 = PASS**, 2026-08-19. The owner had read neither version of `PCP-005` before; the session
printed no page count this time.
