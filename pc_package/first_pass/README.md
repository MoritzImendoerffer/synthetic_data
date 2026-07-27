# first_pass/ — archived first-pass documents

These are the **original first-pass** documents of the A-Mab corpus, moved here to keep
`pc_package/` focused on the current one-pass work. They are **superseded** by the
full-depth, one-pass reports that remain in `pc_package/`:

- `pc_package/PCR-003_bioreactor.qmd` (+ `PCP-003_bioreactor.qmd`) — bioreactor (Step 3)
- `pc_package/PCR-008_aex.qmd` (+ `PCP-008_aex.qmd`) — anion exchange (Step 8)

## What's here

- The other 16 documents' `.qmd` / `.docx` / `.pdf`: unit operations 4–7 and 9–10
  (harvest, Protein A, viral inactivation, CEX, virus filtration, UF/DF), plus the
  corpus-level documents `PTP-001`, `RA-001`, `PCMP-001`, `PCMR-001`.
- Their ground-truth annexes under `first_pass/ground_truth/` (frozen snapshots).

## Status / caveats

- **Written in the superseded register, and not a voice reference.** These documents predate
  the register correction. They average ~34-word sentences, roughly ten em-dashes per 1000
  words and coined compounds such as "the quality-attribute-richest characterization in the
  campaign" — the machine idiom that `authoring/check_style.py` now gates against. `make style`
  deliberately does **not** glob this directory, because these are kept as history, not as
  material to imitate. Never take voice from them; see `authoring/REGISTER_EXEMPLAR.md`.
- **Not built or gated by default.** `pc_package/build_ground_truth.py` now builds only the
  retained bioreactor and anion-exchange pairs; the builder functions for these archived
  documents remain defined but are not invoked, and `check_grounding.py` / `validate_annex.py`
  only cover `pc_package/ground_truth/`. So these annexes are **not** re-generated or
  grounding-checked as part of the active gates.
- **They no longer render in place.** The shared machinery (`_pcpkg.py`, `doe_report.py`,
  `references.bib`, `reference.docx`, `../outputs/`) lives in `pc_package/`; a `.qmd` here
  would need its relative paths adjusted (or to be moved back up) to render.
- **Cross-references still resolve by ID.** The retained documents reference these by
  document ID (`DOC_REGISTRY`, `related_docs_md`), which is path-independent.

## To revive one under the one-pass pipeline

Author it fresh with the `authoring/` pipeline (see `authoring/HANDOFF.md` / `RUNNER.md`)
into `pc_package/`, then rebuild its annex (add its builder back to
`build_ground_truth.py`'s `main()` loop). Do not simply move the old `.qmd` back — it is a
first-pass document, not a one-pass full-depth report.
