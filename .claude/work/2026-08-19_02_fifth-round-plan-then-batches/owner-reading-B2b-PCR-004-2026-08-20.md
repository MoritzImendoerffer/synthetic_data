# Project owner's blind reading of PCR-004, pre-campaign vs attempt 2 — 2026-08-20

Recorded VERBATIM, before the blind key is opened. The pair is `B2b-PCR-004-A.pdf` /
`B2b-PCR-004-B.pdf`, committed in `34321ab`; the key is `blind-key-B2b-PCR-004.md`, drawn with a
random nonce before the authoring agent was launched and committed sealed in `34321ab`. No
checksum of the key was printed at any point.

The owner was told before reading that §6 was spent for this document — this session had printed
that section's paragraph for all three B2 documents earlier the same day — and was asked to read
elsewhere.

## The reading, verbatim

> B is written in a more rigorous way, cites more sources and e.g. table 8.1 seems to be complete
> compared to A. It is hard in both reports to find sentences which are clearly AI gnerated. in A
> I would pick this sentence as AI generated: "The step has no process capability of its own to
> report, because it governs no quality
> attribute and therefore has no acceptance limit to be capable against." in B: "The proven
> acceptable range of each parameter is the range studied, because every
> condition studied produced a clarified harvest that met the requirements of the next
> step and no condition studied changed a quality attribute of the antibody."

## What the reading says, before the key

- Which reads as a paper: **B**, on three named grounds — more rigorous writing, more sources
  cited, and a table 8.1 that "seems to be complete compared to A".
- Sentences quoted as machine prose: **one from A, one from B**.
- The owner states it is hard to find clearly AI-generated sentences in **either** report.

**Both quoted sentences are the same construction**, which is the finding this document has
produced twice already. Each is a `because` clause explaining why the step has no X, resting on the
step governing or changing nothing:

- from A: "…because it governs no quality attribute and therefore has no acceptance limit to be
  capable against."
- from B: "…because every condition studied produced a clarified harvest that met the requirements
  of the next step and no condition studied changed a quality attribute of the antibody."

Neither is a register tic in the sense `check_style` measures. Both are the connective tissue that
run 1's judge named for this document: "The genuinely mechanistic sentences around them are strong
and falsifiable, which makes the empty ones stand out rather than blend in. The failures are the
connective tissue between them." The owner, reading blind and without the questions, picked the
same class of sentence out of both texts independently.

The reading is complete. The key is opened next, below this line.

## The key, opened after the reading above was committed

`blind-key-B2b-PCR-004.md`: **new = B**. Verified by first-pages text hash, because the embedded
dates were normalised at staging:

| file | hash | source |
|---|---|---|
| `B2b-PCR-004-A.pdf` | `459ff3b4c14a` | `B2-old-PCR-004.pdf` — the pre-campaign report |
| `B2b-PCR-004-B.pdf` | `4185f295bbe5` | attempt 2 |

## The rule, applied mechanically

`decisions.pass_rule`: PASS iff the owner judges the NEW document the better text AND quotes fewer
than five sentences from it.

- New document judged better: **yes** — "B is written in a more rigorous way", and B is attempt 2.
- Sentences quoted from the new document: **1**. Fewer than five.

**TASK-050 = PASS**, 2026-08-20. The first PASS for `PCR-004` in three readings.

## One named ground was checkable, and it is correct

The owner gave three grounds and one of them can be verified without judgement: "table 8.1 seems
to be complete compared to A". It is.

| | attributes in Table 8.1 |
|---|---|
| pre-campaign | Host Cell Protein, Residual DNA |
| attempt 2 | Host Cell Protein, Residual DNA, **Aggregates (HMW)** |

Aggregate is the one attribute with a plausible mechanism at this step — shear at the feed zone or
an air-liquid interface in a foaming transfer — and both documents discuss it in the body. Only
attempt 2 carries it into the capability table. The owner found a real content gap blind, from a
table, without the data in front of him.

## The result this reading settles, which is the campaign's sharpest

`PCR-004` has now been authored twice under the same regime and read twice against the same
pre-campaign text. The review counts and the human reading are **inverted**:

| | run-2 review counts (Q1/Q2/Q3/Q4) | owner's blind reading |
|---|---|---|
| attempt 1 | **4 / 0 / 0 / 8** — the best of any document in the campaign | **FAIL** — preferred the pre-campaign text |
| attempt 2 | 5 / 7 / 6 / ~20 — did not converge | **PASS** — preferred attempt 2 |

Same document, same brief, same frozen regime, two authors. The draft the four questions scored
best is the one the owner rejected, and the draft they scored worst is the one he prefers. This is
the third and strongest instance of the pattern first measured on 2026-08-19: a count is not the
quality. It now holds *within* a single document, which removes the confound that different
documents are differently hard.

**And the reading says what the counts could not.** The owner picked one sentence from each text,
and both are the same construction — a `because` clause explaining why the step has no X, resting
on the step governing or changing nothing. He was reading blind, without the four questions, and
selected the exact class of sentence run 1's judge had named as this document's characteristic
failure. What differs between the two attempts is not that class; it is that attempt 2 is, in his
words, more rigorous, better sourced, and more complete in its tables.
