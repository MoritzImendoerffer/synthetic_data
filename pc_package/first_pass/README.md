# first_pass/ — the superseded first-pass documents

Rendered copies of the **original first-pass** A-Mab documents, kept as history. Every one of
them has been replaced by a document in `pc_package/`, re-authored in one pass during the
2026-07 register correction.

## What is here

- 16 documents as `.docx` and `.pdf`: unit operations 4–7 and 9–10 (harvest, Protein A, viral
  inactivation, CEX, virus filtration, UF/DF) and the corpus-level `PTP-001`, `RA-001`,
  `PCMP-001`, `PCMR-001`.
- Their ground-truth annexes, frozen, under `ground_truth/`.

The `.qmd` sources are not kept here — the current ones live in `pc_package/`, and the git
history has the originals. The bioreactor and anion-exchange pairs have no archived copy
either; they were the first two re-authored, before this directory existed.

## What it is for

Comparison, and nothing else. The pair `first_pass/PCR-005_protein_a.pdf` against
`pc_package/PCR-005_protein_a.pdf` is the clearest before-and-after of the register
correction, and the annexes under `ground_truth/` show how far a span layer drifts when a
document is re-authored.

## Caveats

- **Never take voice from these.** They are written in the superseded machine register:
  roughly 34-word average sentences, about ten em-dashes per 1000 words, and coined compounds
  such as "the quality-attribute-richest characterization in the campaign" — precisely what
  `authoring/check_style.py` now gates against. `make style` deliberately does not glob this
  directory, because these are history, not material to imitate. The voice reference is
  `authoring/REGISTER_EXEMPLAR.md`, built only from published human sources.
- **Not built and not gated.** `build_ground_truth.py`, `validate_annex.py` and
  `check_grounding.py` cover `pc_package/ground_truth/` only. The annexes here are frozen
  snapshots and are neither regenerated nor grounding-checked.
- **The numbers are from an earlier state of the model.** Several config corrections landed
  after these were rendered, so do not read a value here as current. `authoring/HANDOFF.md`
  §3a lists what changed.
