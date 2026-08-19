# Project owner's reading of the probe — 2026-08-19

Recorded VERBATIM, before the blind key is opened and before any measure is taken of either
text, in the order every previous reading used. A.pdf and B.pdf are the two files committed in
`0cd8d7c`.

## The reading, verbatim (first message)

> yes, the pdfs read fine. Explain step by step what did you change?

## Status at this point

The two questions the decision rule needs are not yet answered in this message: which sentences,
if any, read as machine prose (with A or B), and which of the two reads as a paper. "The pdfs read
fine" is recorded as the first response and the questions are put again below. The key stays
closed until both are answered.

## Second message, verbatim

> I did not know that there is a difference, I read just A.pdf yet. Should I read B too, I guess?

So "the pdfs read fine" applies to A.pdf alone: A was read and nothing in it was quoted. B.pdf is
unread at this point. The key stays closed.

## Third message, verbatim, after reading B.pdf

> A clearly wins

Sentences quoted as machine prose: none from A (first message: "the pdfs read fine", read as A
alone per the second message); none quoted from B. Preference: A, "clearly".

The reading is complete. The key is opened next, below this line, and the counts come after.

## The key, opened after the reading above was committed (78329c4, then this file's third section)

`blind-key.md`: **probe = A**. Verified by checksum: A.pdf is byte-identical to
pc_package/PCR-005_protein_a.PROBE.pdf and B.pdf to PCR-005_protein_a.EXCERPT.pdf.

So: **A = the probe** (Opus 5, minimal regime, 90 sentences); **B = the shipped text** (the
Track D pilot's PCR-005 lines 747–876, the source of all eight sentences quoted on 2026-08-18).

## The rule, applied mechanically

`decisions.decision_rule`: PASS iff the owner judges the probe the better text AND quotes fewer
than three sentences from it.

- Probe judged the better text: **yes** — "A clearly wins".
- Sentences quoted from the probe: **0** (fewer than three).
- Sentences quoted from the shipped text this time: 0 (the same text drew eight yesterday; today
  it was read second and simply lost).

**D4 = PASS**, 2026-08-19.

Limit recorded in advance and unchanged: the owner had read the shipped subsections four times
the day before and may have recognised them. Nothing in the messages above says so, and the
question asked was which reads as a paper, not which is new.
