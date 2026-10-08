# Exploration — rev2-campaign (2026-10-08)

Proposal: `docs/next/rev2-campaign.md`. **It stands.** Every claim in "The problem" was checked
today, as follows.

## Claims checked

| Claim | Check | Result |
|---|---|---|
| Margins are tuned per step | `config/parameters.yaml:200-266` | True. The margins are 6.8, 4.5, 6.0, 5.0, 3.2 and 4.6, and the comment at line 207-210 says each "must also sit above that step's own nominal and design-centre values" |
| Glycan limits are circular | `doe_report.ipc_limit`, `from_capability` | True. The limit is `mean + 2.5·sd` of `capability.csv` |
| Ceilings use nominal clearance from this campaign | `doe_report._ipc_backcalc` | True. It takes the product of `process_summary.csv` downstream fold, which is the seeded nominal batch |
| The arbitrary limit drives a finding | `PCR-007.pdf` §7.1/7.3 | True. The text reads "Dividing by a safety factor of 5 gives the in-process limit of 1 % HMW", and the upper load NOR is "not supported" |
| No merged cells anywhere | `grep -c gridSpan` over the 20 DOCX | Run below: 0 in all 20 |
| One method per attribute | `config deviations.methods`, `_pcpkg` AMV lists | True. There is no fragment attribute and no CE-SDS anywhere |
| The two tensions are live | `studies.UPPER_ONLY` contains `acidic_variants`; `cal_due` < `EFFECTIVE_DATE` | Both still live |

## What the code looks like

- **The noise stream is shared.** `studies._run_design` passes one `rng` through `uo.run` for
  every run and response. Adding a response inside a unit model shifts every later draw, so new
  measurements must be computed after the run, from independent streams
  (`np.random.default_rng([seed, OFFSET, run])`). `monte_carlo` likewise. Record the sampled
  overrides as extra columns; that adds no draw.
- **Drift caution.** `RUNNER.md` warns that regenerating in a different library environment
  drifts deep decimals. Byte-identity tests must compare against a fresh `generate_data.py` run
  made at the tag in the same environment, not against git.
- **Limits.** `doe_report.acceptance_for` (DS criterion), `ipc_limit`, `effective_acceptance`,
  `acceptance_basis` and `meets_acceptance`. They are used by the PAR functions and by
  `build_ground_truth.py:101-120` (basis text, which mentions the "assurance margin").
- **Viral.** `acceptance_for` back-calculates step floors from nominal `viral_clearance.csv`.
  A-Mab gives a-priori platform claims: VI > 6.6 LRF (p.131), AEX XMuLV > 5.5 and MVM > 4.0, and
  VF ≥ 4.62 (p.165). These sum to 16.72 ≥ 16.7 for XMuLV and 8.62 ≥ 8.6 for MVM. Those are the
  IACs.
- **Tables.** `show()` is `df.to_markdown()`. The tested route is: the HTML table in
  `{=html}` gives the DOCX real `gridSpan`/`vMerge`, and `check_grounding.docx_text` reads it
  with " | " per cell (scratchpad test). Pandoc's LaTeX writer collapses spanned tables, so the PDF
  needs a raw-LaTeX twin. The style gate must strip both raw blocks.
- **Annex.** `build_ground_truth.py` is 6,838 lines, with one builder per document. Every
  re-authored document needs its region re-anchored. `row_quotes()` / `_join_cells()` assume
  one rectangular row, so a merged row reads as an empty continuation cell in the DOCX.
- **Registry.** `DOC_REGISTRY` in `_pcpkg.py` has `VERSION = "1.0"` and
  `EFFECTIVE_DATE = "2026-07-24"` globally. The `Makefile` corpus loop globs
  `PTP RA PCMP PCP PCR PCMR` and needs `INV`.
- **Tests.** 95 pass (`uv run python -m pytest -q tests/`).

## Ground rules that bite

- **Numbers change.** The new attributes, IACs, P(OOS) and dates all go into config and then
  into `outputs/`. The platform worst-case clearance values are prior-product inputs and live in
  config with a source comment.
- **Prose changes.** All 21 documents are one-pass authored. Under the owner's decision, the
  report author may read its paired plan and PCMP-001, for content only.
- **Discrepancies.** D-001 and D-002 stay. They are re-planted through the brief, §5c.
- **Weak claims.** Not in scope. Stays empty on `main`.
- **Read-only.** `nlp_reports` and `annex_contract/` are read-only. A new document class (an
  investigation report) and the revision metadata go into `schema_ext.py`.
  `nlp_reports`' default prefixes contain no `INV`. That is a read-only repository, so record it
  as a known gap rather than change it.

## Risks

1. **Rendering.** The LaTeX twin and the Quarto crossref for a raw table. A `{#tbl-}` div around
   raw content must number and caption in both formats. This is tested in TASK-007 before any
   document uses it.
2. **Cost.** 21 one-pass authorings plus annex re-anchoring is larger than the previous campaign
   (20 documents over five days). The pilot halts for the owner.
3. **Rev 1.0 frozen set.** Its DOCX must keep grounding against its frozen annexes, which needs
   `check_grounding` to accept a directory.
