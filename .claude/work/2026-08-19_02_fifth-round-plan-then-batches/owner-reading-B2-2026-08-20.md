# Project owner's B2 reading — 2026-08-20 (TASK-018)

Recorded VERBATIM before the keys are opened. The three pairs are the files committed in
`fae3ee6`; the keys are `blind-key-B2-PCR-004.md`, `blind-key-B2-PCR-003.md` and
`blind-key-B2-PCR-005.md`, committed sealed in the same commit, each carrying a random nonce so
that neither length nor checksum identifies the letter.

## The reading, verbatim

> for PCR-008 it is clearly the new document (same paragraph), for PCR-004 i like the old one
> better (same paragraph), for PCR-003 I like the new one better. The sentence for PCR-003 which
> tripped me off was "jects 14.3 % of the grid, while the least binding of the
> five is high mannose at 5.3 %. Since no single attribute rejects more than a sixth of
> the characterized region while the five of them together reject over two fifths of it,
> the constraints must act in different directions, which is the interaction argument of
> §5.4 expressed as a volume." in the old report.

## What the reading says, before the keys

- **PCR-008**: the new document, "clearly". (Not one of the three B2 pairs; this restates the
  TASK-047 verdict on the §6 paragraph.)
- **PCR-004**: **the old one**.
- **PCR-003**: **the new one**, with one sentence quoted against the OLD text.
- **PCR-005**: not reported.
- Sentences quoted as machine prose from a NEW document: **none**. The single quoted passage is
  attributed to the old report.
- Section read: §6, the design space paragraph, in each case ("same paragraph").

## The attribution was checked against the files before the keys were opened

The owner reported in *new/old* terms rather than in *A/B* terms, so the attribution was verified
independently. The quoted passage — "the constraints must act in different directions" and
"rejects more than a sixth of the characterized region" — is present in
`B2-old-PCR-003.pdf` and absent from the promoted `pc_package/PCR-003_bioreactor.pdf`. **The
owner's identification of which text is the old one is correct.**

## A limitation of this reading, stated because it is real

**It was not fully blind, and part of that is this session's doing.** Earlier in the same
conversation this session printed the §6 design-space paragraphs of the three *new* documents
(PCR-004, PCR-005 and PCR-008) while analysing the owner's cross-document ranking, and the owner
then read §6 in each blind pair. For `PCR-004` the new text had therefore already been seen, and
the session had warned before the reading that "§6 is spent" for exactly this reason.

`PCR-003` is the exception and the cleaner result: its new §6 was never printed in this
conversation, and the owner identified the old text correctly from the writing itself — the
passage that "tripped me off" is a genuine tell in the old prose ("the least binding of the five",
"no single attribute rejects more than a sixth", "expressed as a volume").

Whether the owner opened any key file before reporting is not known to this session and is not
assumed either way.

The keys are opened below this line.

## The keys, opened after the reading above was committed

| document | key file | verified by first-pages text hash |
|---|---|---|
| `PCR-004` | `new = A` | `B2-PCR-004-A.pdf` = the promoted text, `-B` = the pre-campaign text |
| `PCR-003` | `new = B` | `B2-PCR-003-B.pdf` = the promoted text, `-A` = the pre-campaign text |
| `PCR-005` | `new = A` | not read |

The owner reported in new/old terms, and the keys confirm those terms were used correctly: the
passage quoted for `PCR-003` belongs to `B2-PCR-003-A.pdf`, which the key and the checksum both
identify as the pre-campaign text.

## The rule, applied mechanically

`decisions.pass_rule`: PASS iff the owner judges the NEW document the better text AND quotes fewer
than five sentences from it.

**`PCR-003` — PASS.** The new document was judged better. Sentences quoted from it: 0; the one
quoted passage is from the old text.

**`PCR-004` — FAIL.** The old document was judged better, so the first leg fails. Sentences quoted
from the new text: 0.

**`PCR-005` — not read**, no verdict.

## What this batch says

`B2` splits. The two documents read go opposite ways, and the split falls exactly where the other
evidence in this unit already pointed.

`PCR-004` is the batch's only **non-DoE** report. Its §6 does not describe a design space; it
explains why the step has none. Three independent signals now agree that this is where the
rebuilt apparatus is weakest:

1. this reading, which prefers the pre-campaign text;
2. the owner's cross-document ranking earlier the same day, which placed `PCR-004` last of three
   on the same paragraph and called its sentences "in general weird";
3. the content review, where 16 of `PCR-004`'s 26 run-1 Q1 flags were sentences stating that the
   step governs no critical quality attribute — true, necessary sentences that question 1 has no
   exemption for.

And the counts point the other way, which is the finding worth keeping: `PCR-004` converged
*best* of the whole batch on the four review questions (26/5/7/15 → 4/0/0/8) and is the document
the owner likes least. `PCR-008` attempt 3 converged *worst* (20/8/7/17 → 17/4/7/12) and is the
document the owner likes most. The review counts are not the quality, on the two documents where
a human has now read both versions.

`PCR-003` is the clean PASS: the largest report in the corpus, a full DoE, its new §6 never shown
to the owner in advance, and the owner identified the old text correctly from its prose alone.

**The open question is what a non-DoE report needs**, since `PCR-010` (UF/DF) is the other one and
was promoted in B1 without ever being read.
