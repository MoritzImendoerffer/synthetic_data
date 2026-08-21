# Project owner's B3 sampled reading — PCP-006, 2026-08-21

Recorded VERBATIM, before the blind key is opened. The pair is `B3-PCP-006-A.pdf` /
`B3-PCP-006-B.pdf`, committed in `eb32f62`; the key is `blind-key-B3-PCP-006.md`, drawn with a
random nonce and committed sealed in the same commit. No checksum of the key was printed.

The owner named `PCP-006` from the five B3 plans. No section of any B3 document had been quoted in
the session before the reading, so the whole document was clean — unlike the `PCR-004` reading,
where §6 had been spent by this session's own output.

## The reading, verbatim

> In B the mechanistic decriptions are sometimes more accurate. But A is e.g. more rigorous for
> section 7. I like the short sentences in A. In B, I find more sentences which I attribute to AI:
> "The XMuLV criterion is the contribution this step must make for the cumulative claim
> to hold."The ranges studied are wider than the normal operating ranges in every case, and
> each edge is placed where it is for a reason of its own." "The XMuLV criterion is the
> contribution this step must make for the cumulative claim
> to hold." "The aggregate criterion is an in-process limit of 2.17 %, not the drug substance
> specification of 5 %" I would say, it is a close win for A. But it is close to a tie.

## What the reading says, before the key

- Which reads as a paper: **A**, explicitly qualified — "a close win for A. But it is close to a
  tie."
- Where **B** is better: "the mechanistic descriptions are sometimes more accurate".
- Where **A** is better: "more rigorous for section 7", and "I like the short sentences in A".
- Sentences quoted as machine prose, all from **B**: **3 unique**. The owner's message contains
  four quotation blocks, but the XMuLV sentence appears twice, identically.
  1. "The XMuLV criterion is the contribution this step must make for the cumulative claim to
     hold."
  2. "The ranges studied are wider than the normal operating ranges in every case, and each edge
     is placed where it is for a reason of its own."
  3. "The aggregate criterion is an in-process limit of 2.17 %, not the drug substance
     specification of 5 %"

This is the closest reading of the campaign, and the first in which the owner has named a dimension
on which the text he did **not** choose is better.

The reading is complete. The key is opened next, below this line.

## The key, opened after the reading above was committed

`blind-key-B3-PCP-006.md`: **new = B**. Verified by first-pages text hash:

| file | hash | source |
|---|---|---|
| `B3-PCP-006-A.pdf` | `238efa7ac2e0` | `B3-old-PCP-006.pdf` — the pre-campaign plan |
| `B3-PCP-006-B.pdf` | `6504699653ca` | the promoted plan |

So **A = pre-campaign**, **B = the new text**.

## The rule, applied mechanically

`decisions.pass_rule`: PASS iff the owner judges the NEW document the better text AND quotes fewer
than five sentences from it.

- New document judged better: **no** — "a close win for A", and A is the pre-campaign plan.
- Sentences quoted from the new document: **3**, which would have satisfied the second leg.

The first leg fails. **TASK-026 = FAIL**, 2026-08-21.

**It is the narrowest result of the campaign and the owner said so unprompted**: "it is close to a
tie". He also named a dimension on which the new text is better — "in B the mechanistic
descriptions are sometimes more accurate" — which is the first time in eight readings that the
losing text has been credited with anything.

## One of the three flagged sentences was created by the review cycle

Traced through the three versions of this document by substring, before the key was opened:

| sentence | pre-review draft | promoted |
|---|---|---|
| run 1's Q4 flag: "The ranges studied are wider than the normal operating ranges in every case, **which is what allows the study to find the edge of acceptable operation rather than merely to confirm the centre.**" | present | **removed** |
| the owner's flag: "The ranges studied are wider than the normal operating ranges in every case, **and each edge is placed where it is for a reason of its own.**" | **absent** | **present** |

Run 1's judge flagged the trailing gloss. The author removed it and wrote a **different trailing
gloss onto the same sentence**. Run 2, reading the revised draft with no sight of the first, did
not flag it. The owner did, blind, without the questions.

**This is the second confirmed instance of the same failure**, and the first traced through the
files rather than inferred. The first was `PCR-005`, where run 1 flagged "Pool host cell protein is
the binding response, and it rejects 26.6% of the grid on its own", the author removed "binding
response" and kept "rejects" from the same flagged sentence, run 2 flagged a different set of
coinages, and the owner caught "rejects" reading across three documents.

**A one-cycle review is not self-correcting on the construction it flags.** An author can satisfy
the flag by substituting a neighbouring instance of the same fault, and a fresh second judge has no
reason to look at the sentence again because it no longer carries the words the first judge quoted.

The other two sentences the owner flagged — the XMuLV criterion sentence and the aggregate criterion
sentence — were both present in the pre-review draft and survived untouched. Neither was flagged by
either judge. Both are §7, which is the section the owner separately called "more rigorous" in the
pre-campaign text.

## What this batch says

`B3` is the first batch whose sampled document went to the pre-campaign text on a **plan**. The
genre now stands at one PASS (`PCP-005`, the pilot) and one FAIL (`PCP-006`), against reports at
three PASS and three FAIL. Nothing here separates the genres.

What does separate is §7. The owner's stated ground for preferring the old text is that it is "more
rigorous for section 7", and two of his three quoted sentences are from §7 of the new one. The
acceptance-criteria section is where this document lost.
