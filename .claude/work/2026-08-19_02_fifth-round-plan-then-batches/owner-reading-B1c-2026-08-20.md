# Project owner's blind reading of PCR-008, round zero vs attempt 2 — 2026-08-20

Recorded VERBATIM, before the blind key is opened and before any count. `A.pdf` and `B.pdf` are
the two files committed in `6a493b4`; the key is `blind-key-B1c.md`, committed sealed in `edc11aa`.

This is the third reading of `PCR-008`. The first (`B1`, 2026-08-20) put the round-zero report
against the newly promoted attempt 1 and FAILED: the owner preferred the old text. The owner then
chose re-authoring over reverting or accepting (D8). Attempt 2 was authored in a fresh session
under the same frozen regime (TASK-042). Per the plan, the comparison text here is the ROUND-ZERO
report again, not attempt 1. The owner was told before reading that they had seen the round-zero
text before and might recognize it, and was asked to say so if they did.

## The reading, verbatim (one message)

> I like A better. The reasoning is better to understand and follow. E.g. from A: "A laboratory-scale chromatography system was qualified as a model of the commercial
> step under SOP-1001, and it was built on the standard scaling convention for column
> chromatography. Column diameter was reduced, while bed height, linear velocity,
> protein load per litre of resin and load volume expressed in column volumes were
> all held equal to the commercial values. This convention holds residence time and
> mass transport constant across scales, and all buffer volumes are expressed in column
> volumes, so the same proportional quantities are used at both scales." compared with B which is hard to read and has some phrases in it that sound AI generated: "The studies were executed on a scale-down column qualified as a model of the com-
> mercial step under SOP-1001. The model keeps the bed height of the commercial
> column, the linear velocity, the protein load per litre of resin and the resin type, and its
> equilibration, wash, collection and strip volumes are normalized to column volumes.
> Column packing quality was verified before each campaign by plate count and peak
> asymmetry under SOP-2008. Scale-independent settings, which are the four multivari-
> ate parameters and the flow rate, were operated at the values the commercial process
> will use. The model was qualified by comparing its input and output attributes against
> commercial-equivalent operation, and the qualification was accepted under SOP-1001
> before these studies were executed."

## What the reading says, before the key

- Preference: **A** ("I like A better"), on the ground that "the reasoning is better to understand
  and follow".
- Sentences quoted from **A**, as the example of the better reasoning: **3**.
- Sentences quoted from **B**, as "hard to read" and having "some phrases in it that sound AI
  generated": **5**.
- Both quoted passages are the scale-down model qualification paragraph of Materials and methods.
  The owner compared the same passage in the two documents rather than reading each separately.
- The owner did not say whether they recognized the round-zero text from the earlier reading.

The reading is complete. The key is opened next, below this line.

## The key, opened after the reading above was committed (`16b7643`)

`blind-key-B1c.md`: **new = B**. Verified by checksum on the extracted text of the first three
pages, because the embedded dates of `A.pdf` and `B.pdf` were normalized at staging and the file
bytes therefore differ from their sources:

| file | first-pages text hash | source |
|---|---|---|
| `A.pdf` | `6b4f149537c6` | `B1-old-PCR-008.pdf` — the round-zero report |
| `B.pdf` | `4a34d7808bed` | `pc_package/PCR-008_aex.DRAFT.pdf` — attempt 2 |

So: **A = the ROUND-ZERO PCR-008**; **B = attempt 2**, one pass under the rebuilt apparatus with
one content-review cycle.

## The rule, applied mechanically

`decisions.pass_rule`: PASS iff the owner judges the NEW document the better text AND quotes fewer
than five sentences from it.

- New document judged better: **no** — the owner preferred A, the round-zero text.
- Sentences quoted from the new document: **5**, quoted as "hard to read" with "some phrases in it
  that sound AI generated". Not fewer than five.

Both legs fail. **TASK-043 = FAIL**, 2026-08-20. Per TASK-044 the disposition on FAIL is to revert
`PCR-008` to the round-zero text by name, and B2's release is re-put to the owner.

## What this reading adds that the first one did not

The first `PCR-008` reading recorded a preference with no diagnosis: "clearly A wins. I could not
find sentences in A which sound machine written." This one names the passage and the reason, and
the two documents can be compared on it directly. Both quoted passages are the scale-down model
qualification paragraph.

The round-zero paragraph states the convention and then says what the convention buys:

> "This convention holds residence time and mass transport constant across scales, and all buffer
> volumes are expressed in column volumes, so the same proportional quantities are used at both
> scales."

The attempt-2 paragraph enumerates what the model keeps, and never says why keeping those things
makes it a model:

> "The model keeps the bed height of the commercial column, the linear velocity, the protein load
> per litre of resin and the resin type, and its equilibration, wash, collection and strip volumes
> are normalized to column volumes."

The owner's stated ground is "the reasoning is better to understand and follow". The round-zero
text carries one causal sentence about scale invariance; the new text carries a list of held
quantities, a packed appositive ("Scale-independent settings, which are the four multivariate
parameters and the flow rate, were operated at the values the commercial process will use") and a
coinage ("commercial-equivalent operation") that run 2's judge flagged the same class of elsewhere.

This is a finding about the regime, not about this draft alone, and it is the second consecutive
FAIL for `PCR-008` under it. It goes to the batches' results page (TASK-040):

**the content-review questions push the author toward naming a physical cause wherever a causal
verb stands, and toward deleting clauses that file a finding — and in a Materials and methods
paragraph, where the "cause" is a scaling convention rather than a species, that pressure removed
the explanatory sentence and left an inventory.** The owner read the inventory as machine prose.
