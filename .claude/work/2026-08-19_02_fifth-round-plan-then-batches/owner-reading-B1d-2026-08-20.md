# Project owner's blind reading of PCR-008, round zero vs attempt 3 — 2026-08-20

Recorded VERBATIM, before the blind key is opened and before any count. `A.pdf` and `B.pdf` are the
two files committed in `c75288f`; the key is `blind-key-B1d.md`, committed sealed in `8453525` and
drawn before the authoring agent was launched.

Fourth reading of this document. The first two both went to the round-zero text (`B1`, attempt 1;
`B1c`, attempt 2). Attempt 3 is the first `PCR-008` authored under the amended rule 4 of
`WRITING_GUIDE.md`. Per the plan the comparison text is the round-zero report again, and the owner
was told before reading that they had seen it twice and might recognize it.

## The reading, verbatim (first message)

> from looking at section 2.1, I like the shorter sentences from A better but the logical structure
> of the paragraphs to each other is better in B.

## What this says, before the key

- Scope: **§2.1 only**, by the owner's own statement.
- Sentence level: **A** preferred, on sentence length.
- Paragraph level: **B** preferred, on the logical structure of the paragraphs relative to each
  other.
- Sentences quoted as machine prose: **none**, from either document.
- The owner did not say whether they recognized the round-zero text.

**The reading is split and does not yet answer READING.md's second question.** The pass rule needs
a determinate judgement of which document is the better text, and a preference that runs one way on
sentences and the other way on paragraph structure is not that. Asking the owner to resolve it
AFTER the key was opened would let the session steer the answer, so the key stays closed and the
question is put first.

The reading continues below.

## The deciding question, put before the key was opened

Asked: "Taking §2.1 as a whole — or more of the document if you read further — which of the two
reads as a paper?", with A, B and "no difference" offered, and separately whether the owner wanted
to read further before deciding.

**Answer: A.** And: **§2.1 is enough**, decide on what is there.

## What the reading says, complete, before the key

- Which reads as a paper: **A**.
- Sentence level: A, on sentence length. Paragraph level: B, on the logical structure of the
  paragraphs relative to each other. The owner resolved the split in favour of A.
- Sentences quoted as machine prose: **none**, from either document.
- Scope: §2.1, by the owner's choice, told that it was theirs to widen.

The reading is complete. The key is opened next, below this line.

## The key, opened after the reading above was committed

`blind-key-B1d.md`: **new = A**. Verified by checksum on the extracted text of the first three
pages, because both files' embedded dates were normalized at staging:

| file | first-pages text hash | source |
|---|---|---|
| `A.pdf` | `0257db663624` | `pc_package/PCR-008_aex.DRAFT.pdf` — attempt 3 |
| `B.pdf` | `6b4f149537c6` | `B1-old-PCR-008.pdf` — the round-zero report |

So: **A = attempt 3**, authored under the amended rule 4; **B = the ROUND-ZERO PCR-008**.

## The rule, applied mechanically

`decisions.pass_rule`: PASS iff the owner judges the NEW document the better text AND quotes fewer
than five sentences from it.

- New document judged better: **yes** — asked which of the two reads as a paper, the owner answered
  A, which is attempt 3.
- Sentences quoted from the new document: **0**. Fewer than five.

Both legs hold. **TASK-047 = PASS**, 2026-08-20. TASK-048 promotes attempt 3.

## What this reading says that the three before it did not

`PCR-008` has now been read blind four times. The owner preferred the round-zero text in the first
two and the new text in this one:

| reading | new text | verdict |
|---|---|---|
| B1, 2026-08-20 | attempt 1, pre-amendment | FAIL — round zero preferred, "clearly A wins" |
| B1c, 2026-08-20 | attempt 2, pre-amendment | FAIL — round zero preferred, five sentences quoted from the new text as sounding AI generated |
| B1d, 2026-08-20 | **attempt 3, post-amendment** | **PASS — attempt 3 preferred, nothing quoted against it** |

The variable that changed between attempt 2 and attempt 3 is the amended rule 4, and nothing else:
the same procedure, the same prompt, the same review cycle, the same comparison text, a fresh
author each time.

**And the reading names what the amendment bought and what it did not.** The owner's words are that
the new text has the better sentences and the old text has the better paragraph-to-paragraph logic.
Rule 4 acts on the clause — it says the cause stands where the causal verb stands, and it says what
to do when the cause is a convention. That is a sentence-level instrument, and the sentence level is
exactly where the owner now prefers the new text. Nothing in the apparatus acts on how one paragraph
follows another, and that is exactly where the owner still prefers the old text.

**That is the next rule, if the owner wants one**, and it is a finding for the results page rather
than an edit: the paragraph, not the clause, is the unit the register work has not yet reached.
