# Maintaining and extending the A-Mab corpus

**The corpus is complete.** All 20 documents are built, rendered and annexed, and every gate
passes. This file is what you need in order to *change* one, add a step, or re-run the whole
set — not a work list. Read [`../CLAUDE.md`](../CLAUDE.md) first for the conventions, then
this.

> **Never copy an existing document.** Earlier revisions of this file said to copy
> `PCP-003` / `PCR-003` as a reference implementation. That is precisely how the machine
> register spread through the corpus: each document inherited the previous one's voice, and
> the writing guide was then distilled from the result — a loop that had to be broken by
> rebuilding the exemplar from the published human sources and re-authoring all 20 documents.
>
> Authoring is **one pass from the `authoring/` artifacts alone**: `WRITING_GUIDE.md`,
> `REGISTER_EXEMPLAR.md`, `section_plan.yaml`, `STORY_BIBLE.md` and the document's brief. The
> canonical *structure* lives in `section_plan.yaml`; the canonical *voice* lives in
> `REGISTER_EXEMPLAR.md`. Neither lives in a sibling `.qmd`. See
> [`../authoring/RUNNER.md`](../authoring/RUNNER.md) for the loop.

Golden rules, in full in `CLAUDE.md`: every number comes from the seeded model
(`config/parameters.yaml` → `outputs/`) and is never hard-coded; reuse `_pcpkg.py`,
`doe_report.py`, `schema_ext.py` and `build_ground_truth.py`; follow the canonical section
order; every annex quote must appear verbatim in the rendered document.

## What is where

| | |
|---|---|
| The 20 documents and their annexes | this directory; see [`README.md`](README.md) |
| The superseded first-pass documents | `first_pass/` — kept for comparison only, never an input |
| Every perturbation applied during the build | [`../authoring/HANDOFF.md`](../authoring/HANDOFF.md) §3a |
| Deliberate defects, and their exact spans | [`../authoring/DISCREPANCIES.md`](../authoring/DISCREPANCIES.md) |

Read `HANDOFF.md` §3a before changing `config/` or the render pipeline. It records what each
change did to the documents, including a post-mortem on a config edit that never reached the
rendered tables and left a document contradicting itself.

## Changing a document

1. **Change the model, not the prose.** If a number is wrong, it is wrong in
   `config/parameters.yaml`. Edit it there, run `make data figures`, and every document and
   annex follows. A number typed into a `.qmd` is a bug.
2. **If the prose has to change, re-author the whole document in one pass.** Do not patch a
   paragraph: the register gate measures the document as a whole, and a hand-patched
   paragraph is exactly how the corpus drifted the first time.
3. **Rebuild the annex afterwards.** Re-authoring invalidates every quote that touched the
   changed text. `check_grounding.py` will tell you which. Re-anchor the annex to the new
   text — never edit the document to suit a stale quote.
4. **Run the verification checklist** at the bottom.

## Adding a unit operation

1. Add the step to `config/parameters.yaml` and to `amab_process/unit_ops/`, then
   `make data figures`.
2. `python authoring/build_brief.py <DOC>` for the plan and the report.
3. Author each document in one pass from the brief and the `authoring/` artifacts.
4. Add the pair's entities and assertions to `build_ground_truth.py`. Anchor each record on
   its rendered table row with `param_rows()` / `cqa_rows()` / `par_rows()`, not on a caption;
   pass `table_header=rows.header`; and keep the `" | "` cell separator (`_join_cells()`) if
   you build a partial row by hand, with a matching partial header — see
   [`GROUND_TRUTH.md`](GROUND_TRUTH.md) §1.
5. `make corpus` discovers new `PCP-*` / `PCR-*` documents automatically.

## Per-unit-operation facts

Straight from `config/parameters.yaml`. "DoE?" decides whether `doe_report.py` applies at all.

| Step | key | Title | DoE? | Parameters (classification) | CQAs it controls or clears | Notes |
|---|---|---|---|---|---|---|
| 3 | `bioreactor` | Production Bioreactor | Yes | pH, temperature, pCO₂, osmolality, duration (WC-CPP); DO, initial VCD, feed volume (KPP); medium conc. (GPP) | afucosylation, galactosylation, high mannose, aggregate, acidic variants, HCP, DNA | The design-space step. One corner of the characterized region is excluded — a galactosylation edge of failure. |
| 4 | `harvest` | Harvest and Clarification | **No** | centrifuge_g (KPP), depth_filter_load (KPP), turbidity (GPP) | none | Sets no CQA; written around what it carries forward. |
| 5 | `protein_a` | Protein A Chromatography | Yes | load, elution_ph (WC-CPP); flow, end_collect (KPP); temperature, bed_height (GPP) | pool HCP, leached Protein A, step yield | HCP rises with high load and low elution pH (A-Mab Fig 4.2). Leached Protein A is a robustness finding, not a modelled one. |
| 6 | `viral_inactivation` | Low-pH Viral Inactivation | Yes | **ph (CPP — the only true CPP in the process)**, hold_time, temperature (WC-CPP), protein_conc (GPP) | XMuLV log-reduction, aggregate | Narrow, high-consequence range: above pH 4.0 inactivation is incomplete, below 3.2 the product aggregates. |
| 7 | `cex` | Cation Exchange | Yes | load, wash_cond, elution_ph, stop_collect (WC-CPP); flow (GPP) | aggregate (principal polish), HCP, DNA, leached Protein A | The only aggregate-reduction step. Significant load × conductivity interaction. Pool HCP is in-process; the DS limit is met only after AEX. |
| 8 | `aex` | Anion Exchange | Yes | load_ph, wash1_cond, load_cond, load, flow (all WC-CPP) | HCP, DNA, leached Protein A, XMuLV and MVM clearance | Flow-through. The quality design space is narrower than the validated viral ranges. |
| 9 | `virus_filtration` | Small-Virus Retentive Filtration | Yes (2 factors) | filtration_volume, pressure (WC-CPP) | MVM and XMuLV log-reduction | MVM clearance falls with volumetric load; the load limit is the report's principal finding. |
| 10 | `ufdf` | Ultrafiltration / Diafiltration | **No** (`characterized: false`) | diavolumes, tmp, final_conc (KPP) | none | Mass balance only; formulation characterization is reported with the drug product. |

## Things that will catch you out

1. **`cqas_for(key)` filters by `set_by == key`**, so it returns few or no attributes for a
   downstream step — most CQAs are *set* upstream and *cleared* downstream. A downstream
   report must discuss what its step controls or clears, which is not the same list.
2. **A robust, low-R² response is a finding, not a defect.** Protein A's
   `leached_protein_a_ppm` has no significant factor effect (RSM R² ≈ 0.37). Report it as
   robust; do not claim the models are "adequate for all responses".
3. **The config `study` column must match `studies.DOE_FACTORS[key]`.** A parameter labelled
   `multivariate` that is not actually a DoE factor makes the document contradict its own
   table. `tests/test_config.py` now checks this both ways, including CSV against config.
4. **A config edit is not live until `make data figures` runs.** The committed CSVs are stale
   until then, and the documents read the CSVs. This has caused a shipped self-contradiction
   once.
5. **`doe_report.fig_rsm_contours(key, xf, yf)` needs the two dominant factors** for the step;
   the default pair is the bioreactor's. Factors come from `studies.RSM_TOP[key]`.
6. **Depth follows the design, not a target.** Reports with a DoE run 41–55 pages, non-DoE
   reports 26–28, plans 23–31. Achieve depth with grounded analysis and full appendices, never
   with filler, and never invent a DoE for a step that does not have one.

## Open items

They live in [`../docs/ROADMAP.md`](../docs/ROADMAP.md), with one proposal per item in
[`../docs/next/`](../docs/next/). What is being worked on right now is
[`../docs/pm/_Board.md`](../docs/pm/_Board.md).

**Closed by verification, 2026-08-16.** This section used to say that `nlp_reports`'
`regex_matchers.py` recognizes `PCR/PVR/PPQ/TT/VAL/AMV/SOP/CS` but not `PTP/PCP/PCMP/PCMR/RA`. It
builds the pattern from `settings.document_id_prefixes`, whose default is
`PCMP,PCMR,PCP,PCR,PPQ,PTP,PVR,AMV,SOP,VAL,CS,RA,TT` — every one of the five is there, sorted
longest first so `PCP` cannot shadow `PCMP-001`. Nothing to add, and nothing to change in a
read-only repository.

## Verification checklist

Run before treating any document as done:

- ☐ `make data figures` current for the active seed.
- ☐ `quarto render <doc>.qmd --to docx` and `--to pdf` succeed with no errors.
- ☐ `python authoring/check_style.py <doc>.qmd` passes (`check_render.py` runs it as a gate).
- ☐ `python build_ground_truth.py && python validate_annex.py` → all annexes valid.
- ☐ `python check_grounding.py` → every quote verbatim, and no weak anchors
  (`GROUNDING_STRICT_ANCHORS=1` makes that a gate).
- ☐ No missing glyphs in the PDF (`check_render.py` checks this; a missing `≥` once turned a
  clearance floor into a point value).
- ☐ Section order matches the canonical template in `CLAUDE.md`.
- ☐ `make corpus` runs clean end to end.
