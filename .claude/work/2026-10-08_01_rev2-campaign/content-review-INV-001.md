# Content review — INV-001 draft, run 1 (2026-10-08)

Judge: fresh-context agent, Claude Opus 5.5, given the PDF text and the six questions. Questions 1
and 6 were adapted for an investigation: an organisational cause counts, and the reader is "a
quality professional".

Verdicts: Q1 No · Q2 No · Q3 sentences present · Q4 No · Q5 conflicts found · Q6 No. All
arithmetic re-checked and holding (Tables 4.1, 4.2, 4.5, 6.1, 6.3, the viral sums, the Cpk values).

## The finding that was the orchestrator's: the SEC model was physically impossible

The judge computed that the HCP in the Protein A pool (about 0.72 % of the protein) plus the
leached ligand (at most 0.016 %) could not produce a 1.2–1.3 point SEC excess, even if all of it
eluted in the LMW window. Correct. Fixed in `config analytics.sec_bias` and
`analytics.sec_bias()`:
- The excess is now `lmw_fraction` × HCP mass, so it is bounded by the HCP present.
- The ligand term is dropped.
- A test bounds the bias by the HCP mass.

The comparability excess fell from 1.19 / 1.29 to 0.43 / 0.53 points (Protein A pool / VI pool).
It stays at about 0 after CEX. The spurious load and elution-pH effects on SEC "fragments" in
the Protein A screening are still significant (p < 0.001). The mechanism text in PCMP-001,
STORY_BIBLE §9b, `mechanism/protein_a.yaml`, `tables.py` and `analytics.py` was corrected.

## Other source fixes

- CA4 was removed from `campaign.capa`: the retest predates the investigation.
- The Version 1.0 viral rule label "assay allowance" now reads "less 0.35 log10 for assay
  variability".
- PA2 is reworded as a traceability check.
- "Disulfide species" corrected in the comparability footnote and the config comment.

## Returned to the author

Tense and status (the reissue stated as done while open), two wrong causes, the verification
test, the capability basis, eight filing sentences, templated counts, three coined terms.

# Run 2 (2026-10-08), fresh judge, Claude Opus 5.5

Verdicts: Q1 Yes (one borderline) · Q2 Yes · Q3 sentences present · Q4 No · Q5 13 items, five of
them rounding · Q6 No (six sentences). The arithmetic of every table is verified. The judge
called most of the text "plain, concrete quality writing".

## Disposition

- **Source fixes in `tables.py`:**
  - The rule codes R1–R4 now follow the document's rule order. They had been numbered
    independently, which is a real defect.
  - Fragments now read "not assessed c)" instead of the leached-Protein-A footnote a).
  - The comparability note wording is corrected.
- **One factual pass by the author,** with the same recorded departure from the one-cycle rule.
  It covers eight contradictions, the leached Protein A worst cases that could not be verified,
  results against criteria, and six cuts. Then promotion.
- **Not acted on:**
  - Rounding of the printed differences (each is a difference of rounded means).
  - Single-replicate comparability excesses above the HCP mass (CE-SDS noise; the bound holds
    for the systematic excess).
