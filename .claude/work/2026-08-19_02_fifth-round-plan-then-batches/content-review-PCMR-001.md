# Content review of the PCMR-001 draft — before promotion

**2026-08-21, TASK-036 §4.** Batch B5, written last because it rolls up every report. Its brief was
rebuilt after the other three B5 documents were drafted. No §2b, and §5c assigns no registered
discrepancy. Fresh judge (`opus`), one return.

## Counts per question

| run | Q1 | Q2 | Q3 | Q4 | verdicts |
|---|---|---|---|---|---|
| 1 (as authored) | 12 (+3 table cells) | 9 | 7 | 14 (+1 borderline) | No · No · No · Yes |

The heaviest first-run load of the batch, which is what a 38-page roll-up of eight reports should
be expected to produce. The judge called "X is a Y and not a Z" the document's most persistent tic.

## The terminology finding that reached outside the document

The judge called **"assurance factor"** invented and named safety factor as the standard term. That
is the **second independent judge** to make the identical call, after PCP-007's earlier in this
batch — and PCP-007's author had already changed it, and PCP-007 was already promoted. Shipping
PCMR-001 with "assurance factor" would have put two shipped documents in contradiction over the
same quantity, which is a bug rather than a style difference.

So the return stated the corpus fact rather than leaving the author to guess. The author checked
before changing: `safety factor` occurs **8 times** in `refs/text/amab.txt` and `assurance factor`
**zero times anywhere in `refs/`** — both verified independently here. PCMR-001 and PCP-007 now
agree. PCP-008's older two-judge disagreement over the neighbouring "assurance margin" is part of
the same knot and is not resolved by this.

## The author overruled its judge, and was right

The judge called **"quality linked"** a coined umbrella class, saying the literature classifies
CPP, WC-CPP, KPP and GPP with no such term. The author kept it, and its reasoning checks out:
`quality-linked` occurs **15 times** in `refs/text/amab.txt`, including as a section heading, and
**26 times** across the corpus `.qmd` files (both verified here). It is the source's own umbrella
term. What made it read as a coinage was the author's own unhyphenated spelling and the absence of
a gloss, so it fixed the form and glossed it once on first use. Replacing it would have created the
inconsistency rather than fixed one.

That is the **second time in this batch** an author defended a term on corpus-consistency grounds
and was right — RA-001 did the same with "justified univariate", which turned out to be A-Mab's own
Table 5.16 rule.

The rest of question 2 was accepted and fixed: `binding` in the optimization sense became
`limiting` (it collided with the chromatographic sense in a document about chromatography),
`bounded impact argument` became `documented impact assessment`, `charge variant burden` became
`acidic charge variant content`, `control margin` lost its invented noun, and `roll-up` went in all
four places.

## Against the batch's own warning

The return carried the lesson from PTP-001 and RA-001, whose revisions each introduced a confident
wrong claim. This author checked every new direction **before** writing it rather than after:

- It fitted **both** AEX datasets before describing the superseded execution, confirming the
  superseded model predicts 78.8 ng/mg at the high-load, high-conductivity corner against a
  21.7 ng/mg in-process limit while the requalified model predicts 21.1, and that the
  load × wash-conductivity interaction runs p = 0.002 superseded against p = 0.86 requalified.
- It read `harvest.py` and `ufdf.py` before writing their mechanism sentences.
- **It caught one of its own wrong claims**: its residual-DNA sentence had implied no operating
  region could bring the attribute near its limit, where the simulated maximum is 0.00025 ng/dose
  against a 0.001 limit — a factor of 4, not an order of magnitude. It now gives the mean factor
  and the simulated maximum, both pulled.

No third document in this batch shipped an introduced physics error.

## The audit fired, and I judged it a false positive

Seven hits on `prose_from_qmd`, every one printing the document's **own** prose back in slices, and
one `grep -rho "quality[- ]linked" pc_package/*.qmd` whose `-o -h` flags return a bare count of one
term with no filenames and no prose. Neither fetched a measurement nor a sibling's sentences.

The principle applied consistently across this batch: **set aside when sibling prose could
contaminate voice or content** (PCP-007, where four documents' verbatim sentences reached the text);
**record when the extracted information is metadata or a count** (RA-001's subtitle grep, and this).
Recorded as my call, as the PCP-008 `reflow` session recorded its own.

## Findings recorded, not acted on

- `all_sop_table()` was found defective **independently for the third time**. This author needed the
  register's size in prose, so using the helper would have made a false claim; it built the union in
  its own SETUP chunk through the public `sop_table(...)` and left shared machinery alone, noting
  that fixing the helper would silently change PTP-001's and PCMP-001's rendered tables.
- Three Table 2.1 role cells use "sets" with no mechanism. Generated content, left alone.
- The document is 38 pp against the section plan's "~25-30 pp" note. The excess is 16 tables and 5
  figures, not prose: prose is 5,415 words.

## Disposition

One cycle. The revision addressed all four questions, so no second judge was run and the document
proceeded to promotion. Nothing is added to it after this point.
