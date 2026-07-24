# TASKS — remaining A-Mab corpus documents

Work list for continuing the `pc_package/` document corpus. Written so a fresh Claude
(or engineer) on any machine can pick up. **Read [`../CLAUDE.md`](../CLAUDE.md) first**
(conventions), then this file. The bioreactor pair `PCP-003` / `PCR-003` is the
reference implementation — copy its structure exactly.

Golden rules (full detail in `CLAUDE.md`): every number comes from the seeded model
(`config/parameters.yaml` → `outputs/`), never hard-coded; reuse `_pcpkg.py`,
`doe_report.py`, `schema_ext.py`, `build_ground_truth.py`; follow the canonical section
templates; every ground-truth quote must appear verbatim in the rendered document; run
the verification checklist before marking a document done.

## Status

| Document | Class | Step / key | State |
|---|---|---|---|
| `PCP-003` / `PCR-003` | Plan / Report | 3 · bioreactor | ✅ done (reference pair) |
| `PCP-004` / `PCR-004` | Plan / Report | 4 · harvest | ☐ todo (no DoE) |
| `PCP-005` / `PCR-005` | Plan / Report | 5 · protein_a | ☐ todo (DoE) |
| `PCP-006` / `PCR-006` | Plan / Report | 6 · viral_inactivation | ☐ todo (DoE) |
| `PCP-007` / `PCR-007` | Plan / Report | 7 · cex | ☐ todo (DoE) |
| `PCP-008` / `PCR-008` | Plan / Report | 8 · aex | ☐ todo (DoE) |
| `PCP-009` / `PCR-009` | Plan / Report | 9 · virus_filtration | ☐ todo (DoE) |
| `PCP-010` / `PCR-010` | Plan / Report | 10 · ufdf | ☐ todo (no DoE) |
| `PTP-001` | Process Transfer Plan | — | ☐ todo |
| `RA-001` | Pre-Characterization Risk Assessment | — | ☐ todo |
| `PCMP-001` | PC Master Plan | — | ☐ todo |
| `PCMR-001` | PC Master Report | — | ☐ todo |

## Recommended order

1. **Enabling refactors** (do first — they make every later document faster):
   - ☐ Add a reusable grounding-check script `pc_package/check_grounding.py` (extract the
     inline check currently used ad-hoc: for each `ground_truth/*.json`, every
     `SourceReference.quote` must appear verbatim in the matching rendered document; render
     a `gfm` proxy or read the docx text). Wire it into `make corpus` after `validate_annex.py`.
   - ☐ Refactor `build_ground_truth.py` so `build_plan`/`build_report` take a unit-operation
     config (currently hard-coded to `bioreactor`), so each new pair is a few lines, not a copy.
   - ☐ Extend `doe_report.RESP_LABEL` with the downstream response keys (see gotcha 1).
2. **DoE unit-op pairs** (richest → simplest): `005` protein_a → `006` viral_inactivation
   → `007` cex → `008` aex → `009` virus_filtration.
3. **Non-DoE pairs** (short): `004` harvest, `010` ufdf.
4. **PTP-001**, then **RA-001** (RA derives from PTP).
5. **PCMP-001** (master plan).
6. **PCMR-001** last — it rolls up all the per-unit-operation reports.

Cross-references between documents are by ID (placeholders already resolve), so the order
above is a recommendation, not a hard dependency — except PCMR-001, which should come after
the reports it summarises.

## Building one Plan/Report pair (the loop)

1. Copy `PCP-003_bioreactor.qmd` → `PCP-00N_<key>.qmd` and `PCR-003_bioreactor.qmd` →
   `PCR-00N_<key>.qmd`. Set `DOC`, `UO`, `UO_TITLE` in the setup chunk. Keep the section
   order identical (see `CLAUDE.md`).
2. Rewrite only the unit-specific narrative (the step's role, the CQAs it controls, the
   mechanistic interpretation). Pull all numbers via `report_params(UO)`, `plan_params(UO)`,
   `cap_for([...])`, and `doe_report.*` — never type them.
3. Add the pair's entities/assertions to `build_ground_truth.py` (mirror the bioreactor
   `build_plan`/`build_report`); use quotes that appear in the new document.
4. Verify (see checklist at the bottom).
5. `make corpus` rebuilds and re-validates everything (it auto-discovers new `PCP-*`/`PCR-*`
   qmds).

## Per-unit-operation facts (from `config/parameters.yaml`)

Use these to write grounded content quickly. "DoE?" tells you whether to use `doe_report.py`.

| Step | key | Title | DoE? | Parameters (classification) | CQAs it controls / clears | Notes |
|---|---|---|---|---|---|---|
| 4 | `harvest` | Harvest and Clarification | **No** | centrifuge_g (KPP), depth_filter_load (KPP), turbidity (GPP) | none (no product-quality impact) | Shortest pair; parameters are KPP/GPP for process performance & feed consistency. |
| 5 | `protein_a` | Protein A Chromatography | Yes | load (WC-CPP), elution_ph (WC-CPP), flow (KPP), end_collect (KPP), temperature (GPP), bed_height (GPP) | pool HCP, leached Protein A, step yield | HCP rises with high load & low elution pH (A-Mab Fig 4.2); flow/end-collect affect yield not quality. |
| 6 | `viral_inactivation` | Low-pH Viral Inactivation | Yes | **ph (CPP — the only true CPP in the process)**, hold_time (WC-CPP), temperature (WC-CPP), protein_conc (GPP) | XMuLV log-reduction, aggregate | pH is a narrow, high-consequence range (3.2–4.0): >4.0 incomplete inactivation, <3.2 aggregation. |
| 7 | `cex` | Cation Exchange (CEX) | Yes | load, wash_cond, elution_ph, stop_collect (all WC-CPP), flow (GPP) | aggregate (principal polish), HCP, DNA, leached Protein A | Only aggregate-reduction step; test a worst-case aggregate feed. Significant load × conductivity interaction. |
| 8 | `aex` | Anion Exchange (AEX) | Yes | load_ph, wash1_cond, load_cond, load, flow (all WC-CPP) | HCP, DNA, leached Protein A, XMuLV + MVM clearance | Flow-through; quality design space (pH 7.2–7.8, Eq/Wash-1 cond 1.6–3.6 mS/cm) is narrower than the validated viral ranges. |
| 9 | `virus_filtration` | Small-Virus Retentive Filtration | Yes (small design) | filtration_volume (WC-CPP), pressure (WC-CPP) | MVM + XMuLV log-reduction | Load ≤ 105 L/m² preserves LRV ≥ 4.62; modular/orthogonal clearance claim. |
| 10 | `ufdf` | Ultrafiltration / Diafiltration | **No** (`characterized: false`) | diavolumes (KPP), tmp (KPP), final_conc (KPP) | none (mass balance only) | Formulation characterization is reported with the drug product; short pair. |

## Implementation gotchas (learned building the bioreactor pair)

1. **`doe_report.RESP_LABEL` only labels the bioreactor CQAs.** Downstream responses have
   different keys — check `amab_process.studies.DOE_RESPONSES[key]` for the exact set (e.g.
   `pool_hcp_ng_mg`, `aggregate_out_pct`, `xmulv_lrf`, `mvm_lrf`, `step_yield`,
   `leached_protein_a_ppm`). Add readable labels to `RESP_LABEL` or the tables show raw keys.
2. **`doe_report.fig_rsm_contours(key, xf, yf)` defaults to `pH × duration` (bioreactor).**
   Pass the two dominant factors for each step, e.g. `protein_a`: `load` × `elution_ph`;
   `aex`: `load_ph` × `wash1_cond`. Factors come from `studies.RSM_TOP[key]`.
3. **`_pcpkg.cqas_for(key)` filters CQAs by `set_by == key`** and so returns few/none for
   downstream steps (most CQAs are *set* upstream and *cleared* downstream). Downstream
   reports must discuss the CQAs each step **controls/clears** (HCP, aggregate, viral
   clearance), not just those it "sets". Reference them explicitly, or add a small
   step→controlled-CQAs map. The removed consolidated report (git commit `946f7d3`,
   `report/process_characterization.qmd`) has a good control-strategy table for reference.
4. **Non-DoE steps** (`harvest`, `ufdf`): do **not** call `doe_report`. Present
   univariate/qualitative characterization; these pairs are shorter (report ~10–15 pp, plan
   ~10 pp). Do not fabricate a DoE.
5. **`build_ground_truth.py` currently only builds `PCP-003`/`PCR-003`.** Extend it per pair
   (or do the refactor above). `make corpus` runs it, so it must produce every annex.
6. Depth targets (`CLAUDE.md`): DoE reports ~30–35 pp, plans ~20 pp; non-DoE pairs shorter.

## Transfer & master documents

### PTP-001 — Process Transfer Plan
Tech-transfer plan for moving the A-Mab DS process from the sending site (Cambridge, MA
Development) to the receiving site (Grafton, WI Commercial).
- **Grounding:** `refs/text/ispe_tt.txt` (2023 ISPE Tech-Transfer guide), `refs/text/pda_tr60.txt`
  §6.4 (Table 6.4-1, transfer strategy / site-equivalency / gap analysis),
  `refs/grounding/PDA_TR_60.json`, A-Mab cross-scale comparability (`refs/text/amab.txt`).
- **Structure:** transfer scope & strategy; product/process description; sending & receiving
  sites; site-equivalency analysis; scale-down-model & comparability strategy; transfer of the
  manufacturing process, analytical methods, and control strategy; PPQ/batch strategy; gap
  analysis (`TransferGap`); responsibilities; schedule.
- **Annex:** `DocumentInventoryItem` type `process_transfer_plan` (already in `schema_ext`);
  entities = sites, process steps, key equipment; `transfer_gaps`; `report_sections`.
- ☐ **First add** an `ispett2023` entry to `pc_package/references.bib` (the ISPE Tech-Transfer
  guide is not yet cited); `ispegpg2023` is the PV-lifecycle guide, a different document.

### RA-001 — Pre-Characterization Process Risk Assessment
Initial risk assessment (A-Mab RA#1–#2 style) **derived from PTP-001**, prioritising which
parameters to characterise and the study type — done **before** the characterization studies.
- **Grounding / reuse:** `refs/grounding/amab_risk.json` (the RRF study-type rule: Severity =
  main-effect × interaction-effect → ≥32 multivariate, 8–16 multivariate/justified univariate,
  4 univariate, ≤2 none; Tables 5.16/5.17); **`risk_assessment/build_fmea.py` `CONTENT` dict**
  (curated per-parameter failure-mode / effect / control text — the richest reusable asset);
  `config` risk scales.
- **Key point:** this is *pre*-characterization — use the **initial** occurrence/detection and
  the study-type decision, **not** the post-characterization residual RPN. The output is the
  characterization scope (which parameter → which study), which feeds each `PCP-00N`.
- **Annex:** type `risk_assessment`; entities = parameters (with pre-hoc risk rationale),
  CQAs; assertions linking parameters → CQAs at risk; `report_sections`.

### PCMP-001 — Process Characterization Master Plan
Umbrella plan over all per-unit-operation plans.
- **Structure:** overall Stage-1 strategy & scope (all unit ops); CQA framework; risk-based
  prioritisation summary (from RA-001); scale-down-model strategy; common statistical approach;
  the list of per-UO plans (`PCP-003…010`); acceptance-criteria framework; schedule.
- Pull the CQA/parameter registers via `_pcpkg` (`cqa_reg`, `param_reg`); reference every
  `PCP-00N` by ID.

### PCMR-001 — Process Characterization Master Report (do last)
Roll-up of all per-unit-operation reports — essentially the content of the removed consolidated
report, but as a summary that cites the `PCR-00N` documents.
- **Reuse:** `outputs/report_values.json` (headline numbers: overall yield, min Cpk, viral
  clearance totals, parameter counts), `capability.csv`, `viral_clearance.csv`,
  `parameter_classification.csv` (all 37 parameters), `fig_process_flow.png`,
  `fig_param_classification.png`, `fig_capability.png`, `fig_viral_clearance.png`,
  `fig_yield_waterfall.png`.
- **Structure:** executive summary; process description & flow; consolidated CQA outcomes;
  full parameter-classification summary; process capability (all CQAs, min Cpk); viral-clearance
  summary; overall control strategy; conclusions & Stage-2 readiness. Cite each `PCR-00N`.

## Cross-cutting TODOs

- ☐ `ispett2023` entry in `pc_package/references.bib` (for PTP-001).
- ☐ Extend `doe_report.RESP_LABEL` for downstream response keys.
- ☐ Refactor `build_ground_truth.py` to be per-unit-operation; add `check_grounding.py` and
  wire both into `make corpus`.
- ☐ (Flag, do not change `nlp_reports`.) Its `regex_matchers.py` DOCUMENT_ID pattern recognises
  `PCR/PVR/PPQ/TT/VAL/AMV/SOP/CS` but not `PTP/PCP/PCMP/PCMR/RA`; note for that repo's owner.

## Verification checklist (run before marking any document done)

- ☐ `make data figures` current for the active seed.
- ☐ `quarto render <doc>.qmd --to docx` and `--to pdf` succeed with no errors.
- ☐ `python build_ground_truth.py && python validate_annex.py` → all annexes valid.
- ☐ Grounding: every annex `SourceReference.quote` appears verbatim in the rendered text.
- ☐ Depth target met; section order matches the canonical template in `CLAUDE.md`.
- ☐ `make corpus` runs clean end-to-end.
