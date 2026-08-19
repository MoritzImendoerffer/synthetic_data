# Project owner's reading of the fourth round — 2026-08-19

Recorded VERBATIM, before the blind key is opened and before any measure is taken of either text.
`A.pdf` and `B.pdf` are the two files committed in `4531668`; the owner was given the text in
`procedures/READING.md` (suggested subset: Executive summary; Results, all four subsections; Design
space; Discussion).

## The reading, verbatim (one message)

>   B is clearly bette to read. A couple of examples from A which read like machine generated: Yield is a process performance response and carries no quality
> claim, so that limitation does not touch the acceptance argument in Section 6.; The aggregate coefficients in Table 5.6 confirm the screening picture and sharpen it.; The aggregate coefficients in Table 5.6 confirm the screening picture and sharpen it.; The host cell protein coefficients in Table 5.7 reproduce the two dominant main effects
> and the protein load interaction with conductivity, and they add a second interaction
> that the screening block did not resolve.; B reads more like a paper.

## What the reading says, before the key

- Preference: **B**, "clearly bette[r] to read", "B reads more like a paper".
- Sentences quoted as machine-generated, all from **A**: three distinct sentences (one of them
  pasted twice) — "Yield is a process performance response and carries no quality claim, so that
  limitation does not touch the acceptance argument in Section 6."; "The aggregate coefficients in
  Table 5.6 confirm the screening picture and sharpen it."; "The host cell protein coefficients in
  Table 5.7 reproduce the two dominant main effects and the protein load interaction with
  conductivity, and they add a second interaction that the screening block did not resolve."
- Sentences quoted from **B**: none.

The reading is complete. The key is opened next, below this line, and the counts come after.

## The key, opened after the reading above was committed

`blind-key.md`: **new = B**. Verified by checksum: `B.pdf` is byte-identical to
`pc_package/PCR-007_cex.DRAFT.pdf` (the new report, run 2 after one review cycle) and `A.pdf` to
`pc_package/PCR-007_cex.pdf` (the shipped report). The three quoted sentences are each found once in
the shipped `.qmd` and never in the new one.

So: **B = the new PCR-007** (one agent, one pass, RUNNER as rebuilt, one content-review cycle, 50
pages); **A = the shipped PCR-007** (round zero, 51 pages).

## The rule, applied mechanically

`decisions.pass_rule`: PASS iff the owner judges the new document the better text AND quotes fewer
than five sentences from it across whatever was read.

- New document judged better: **yes** — "B is clearly bette[r] to read", "B reads more like a paper".
- Sentences quoted from the new document: **0** (fewer than five).
- Sentences quoted from the shipped document: 3 distinct.

**D6 = PASS**, 2026-08-19.

Limit: the session had inferred the key from the two page counts it printed at TASK-004 (51 vs
50) and said nothing; the owner had read neither version of `PCR-007` before and was given the
letters only.
