# A-Mab story bible — world canon for the characterization corpus

The durable, self-contained account of the world these documents live in: the
sponsor, the product, the sites, the process train, the platform history, the
document package, and the campaign storyline. It exists so an author can write any
document in the corpus **consistently** without another report present.

Two kinds of content live here, and the distinction is load-bearing:

- **Grounding map** (§10) — where each *fact that is a number or a controlled value*
  actually lives (a helper, a constant, a CSV). The author **pulls** these through
  inline expressions and **never restates them as prose** (WRITING_GUIDE §6, CLAUDE.md
  golden rule 1). This bible therefore names the *source*, not the value.
- **Narrative canon** (§1–§9) — the qualitative, fictional world: names, roles, the
  platform lineage, the transfer arc, the campaign storyline, register. This is *new
  text*, free to phrase, but fixed in substance: do not contradict it across documents.

Everything here is **synthetic** (see `SYN_BANNER`): Novacyte Biologics, its sites, the
prior products, all SOP/AMV/equipment/lot numbers and signatories are invented for an
NLP corpus built on the public A-Mab case study [@amab2009]. Nothing is a real record.

---

## 1. Sponsor

**Novacyte Biologics** — the fictional sponsor developing and commercializing A-Mab.
Its process-science voice is *Manufacturing Science & Technology (MSAT)* / *Process
Development (PD)*: a PhD-level process scientist writing material to support a Biologics
License Application (BLA). Grounded as `COMPANY` in `_pcpkg.py`; the document owner
string is set by `title_block(...)`.

## 2. Product

**A-Mab** — a humanized IgG1 monoclonal antibody, anti-CD20-like, whose primary
mechanism of action is ADCC (so afucosylation and galactosylation are efficacy-linked
CQAs, and the glycan attributes are formed at the bioreactor). This identity is
narrative canon; it is also carried in `CFG` (`meta.product`, `meta.modality`). The
quantitative product targets (drug-substance concentration, commercial scale, batch
counts) are numbers — pull them, never type them (§10).

A-Mab is purified by a **platform** train:
Protein A → low-pH viral inactivation → cation exchange → anion exchange →
virus filtration → UF/DF. This ordering is canonical and stated the same way in every
document; it originates in the case study [@amab2009] and is realized by
`CFG.train_order` / `process_steps_df()`.

## 3. Sites and the transfer arc (the story spine)

The corpus documents a **technology transfer and Stage-1 process characterization**
campaign that moves the drug-substance process from development to commercial manufacture:

- **Sending site — Novacyte Biologics, Cambridge, MA (Development).** Where the process
  was developed and where the scale-down models and DoE characterization live.
- **Receiving site — Novacyte Biologics, Grafton, WI (Commercial DS).** The commercial
  drug-substance facility the process is being transferred to.

Grounded as `SENDING_SITE` / `RECEIVING_SITE`; `title_block(...)` prints the
"Cambridge → Grafton" transfer relationship. The **Process Transfer Plan (PTP-001)** is
the parent that frames this arc; every per-step report ultimately supports the transfer
and rolls up into the **Master Report (PCMR-001)**. When a document needs to explain
*why* it exists, this is the answer: to characterize the process at commercial-equivalent
scale-down and justify the Stage-2 operating ranges and control strategy for transfer.

## 4. The process train and each step's role

Steps are numbered 3–10 (upstream cell culture through formulation). Titles come from
`UNIT_OP_TITLES`; each step's one-line control-strategy role from `UNIT_OP_ROLE`; the
whole train with roles from `process_steps_df()`. The canonical narrative of each:

- **Step 3 — Production Bioreactor (USP).** The **design-space step**: fed-batch culture
  that *forms* the glycan (afucosylation, galactosylation, high mannose), charge-variant
  and aggregate CQAs. The richest DoE (5 responses). Sets the most CQAs.
- **Step 4 — Harvest & Clarification.** Primary recovery; forms no product-quality CQA.
  **Non-DoE** (univariate/qualitative).
- **Step 5 — Protein A Chromatography.** Capture; sets leached Protein A; principal HCP
  and DNA clearance. DoE.
- **Step 6 — Low-pH Viral Inactivation.** Hold step; sets the cumulative enveloped-virus
  (XMuLV) clearance. DoE (pH is the governing parameter). Q5A framing.
- **Step 7 — Cation Exchange.** Polish; principal aggregate reduction; major HCP/DNA/
  leached-PA clearance. DoE. Sets **no** CQA of its own (clears only).
- **Step 8 — Anion Exchange.** Flow-through final polish; **sets the cumulative MVM
  (parvovirus) clearance** — the tightest capability of the drug substance; clears
  XMuLV/HCP/DNA/leached-PA. DoE. The generalization/register exemplar (PCR-008).
- **Step 9 — Small-Virus Retentive Filtration.** Dedicated size-based small-virus
  removal; principal MVM clearance; orthogonal to steps 6 and 8. DoE.
- **Step 10 — UF/DF (Formulation).** Concentration + buffer exchange to the DS target;
  forms/clears no CQA, so its parameters are KPP, not CPP. **Non-DoE.**

Viral safety is **modular and orthogonal** across steps 6 (low-pH), 8 (AEX) and 9 (VF):
each contributes an independent log-reduction increment, and the cumulative claim is
consolidated in PCMR-001. Any single-step report gives **cross-step credit** and never
implies it delivers the whole viral-safety claim alone (WRITING_GUIDE §3).

## 5. Platform and prior-product history (narrative canon)

A-Mab is developed on Novacyte's humanized-IgG1 platform, whose behaviour is established
from three **prior products — X-Mab, Y-Mab and Z-Mab** (fictional related humanized IgG1
antibodies) plus A-Mab clinical and engineering experience [@amab2009]. This lineage is
the basis for the "prior knowledge" section of every document: platform mechanisms are
*known*, so characterization *confirms and bounds* rather than *discovers*.

X-Mab has partial numeric grounding — several A-Mab acceptance limits are set from X-Mab
clinical experience (recorded in `config/parameters.yaml` CQA comments, surfaced through
the CQA helpers). Y-Mab and Z-Mab are qualitative platform canon only. Use the prior
products to justify factor *ranges* and mechanistic *expectations*; never attach a
fabricated number to them — if a platform value matters, it lives in the config.

## 6. The document package and ID scheme

The corpus is a cross-referenced package (all IDs and titles in `DOC_REGISTRY`; the
cross-reference tables from `related_docs_md(DOC)` and `corpus_docs_md(...)`):

| ID | Document | Role in the package |
|---|---|---|
| `PTP-001` | Process Transfer Plan | Parent — transfer scope (the arc of §3) |
| `RA-001` | Pre-Characterization Process Risk Assessment | Parent — risk basis that *scopes* every study |
| `PCMP-001` | Process Characterization Master Plan | Parent — master plan over the campaign |
| `PCP-00N` | Process Characterization Plan (protocol) | Per step N (3–10); prospective |
| `PCR-00N` | Process Characterization Report | Per step N; the executed study, paired with its PCP |
| `PCMR-001` | Process Characterization Master Report | Every PCR rolls up into it |

`N` = process step (3–10). Filenames: `PCP-00N_<uokey>.qmd`, `PCR-00N_<uokey>.qmd`;
annex `ground_truth/<ID>.json`. Each PCR names its risk basis (RA-001), its paired plan
(PCP-00N) and its roll-up (PCMR-001). **RA-001 scopes; the PCP plans; the PCR executes;
the PCMR consolidates.** That dependency chain is the package's logic.

## 7. SOP / AMV conventions

Controlled-document numbers are **explicit placeholders** (CLAUDE.md): `SOP-####`
(procedures), `AMV-####` (analytical method validations), `PPQ-####`. The shared
registry is `SOP_REFS` / `AMV_REFS`; each step draws a subset via a named list
(`<KEY>_SOP_REFS`, `<KEY>_AMV_REFS`, e.g. `AEX_SOP_REFS`, `AEX_AMV_REFS`) rendered by
`sop_table(...)`. Conventions the author relies on:

- Every DoE step cites `SOP-1001` (SDM qualification), `SOP-1002` (DoE design/analysis),
  its own operation SOP, and `SOP-4001` (parameter classification).
- Each analytical response has one AMV (e.g. HCP → `AMV-3012`, SEC → `AMV-3011`, N-glycan
  → `AMV-3010`, MVM → `AMV-3018`). Pull the step's subset from its `_AMV_REFS` list.
- SOP/AMV numbers are **identifiers, not measurements** — write them plainly; the numeral
  lint exempts them (WRITING_GUIDE §6). Never invent a new number; use the registry.

## 8. Regulatory framing

Cite **only** existing `references.bib` keys. The standard basis, and what each is for:

- `@amab2009` — the A-Mab case study (CMC Biotech Working Group): the source of the
  process model, CQA framework and risk methodology. Cited in every document.
- `@fda2011` — the lifecycle approach to process validation; the report structure maps to
  its Stage-1 (Process Design) study record.
- `@ichq8`, `@ichq9`, `@ichq11` — the enhanced/QbD development approach; criticality as a
  continuum (Q9).
- `@ichq10` — quality system / technology-transfer framing (transfer docs).
- `@ichq5a` — the viral-safety evaluation framework, for the viral steps (6, 8, 9) and
  their modular clearance claims.

## 9. The characterization campaign storyline (the "messy campaign")

The corpus is not a clean paper exercise; it documents a **real campaign with recorded
deviations** — this is deliberate, because narrated deviations are what make the corpus
realistic and the benchmark hard. The seeded deviation world (`config/parameters.yaml`
`deviations:` → `deviations.csv`, surfaced by `dev_register`, `dev_facts`, and the
`dev_*` scalars) includes recurring world-level entities the author may reference:

- **Equipment:** `EQ-BRX-205` (bioreactor pCO₂ probe), `EQ-CHR-118` (temperature-controlled
  chromatography chamber), `EQ-TFF-142` (UF/DF TFF skid).
- **Prior campaign documents:** `RA-004` (Alternate Protein A Resin Risk Assessment —
  decided independent characterization is required, no platform bridging) and `SOP-2103`
  (Buffer Preparation / expiry control — authorises retained-sample re-test on expiry
  deviations). These are cited where a deviation's investigation touches them.
- **Lots / methods:** feed and buffer lots (e.g. `LOT-FED-3120`) and verification-qualified
  methods appear per-deviation; the brief surfaces the ones relevant to each document.

**The superseded-study canon (important).** Where a deviation invalidated a study and
forced re-execution, the campaign *actually ran the study twice* and both datasets are
seeded. The paradigm case is **anion exchange (Step 8)**: the first DoE execution used a
**non-representative, deamidated load** (an out-of-trend extended neutralized hold of the
CEX eluate raised the acidic charge-variant burden), which — through an anomalous
protein-load × wash-conductivity interaction — drove the flow-through pool out of its
in-process limit at the high-load/high-conductivity corner. The affected screening and
RSM designs were **invalidated for operating-region definition and re-executed in full on
a requalified, representative load.** The **reported analysis is the requalified
execution; the first execution is retained as a real superseded dataset** and is
*referenced* (to confirm root cause: the anomalous interaction is statistically absent in
the requalified data), **not analysed**. A report of such a step tells this as an
adverse-before-mitigation story (WRITING_GUIDE §3), grounded entirely in the seeded
scalars and the two datasets — never in invented numbers. Milder deviations (probe drift,
feed under-delivery) are simply **retained** with a bounded-impact argument.

## 10. Grounding map — pull, never type

Every value below is a number or a controlled datum. Read it through the named source;
do not restate it as prose. (The per-document brief expands this into the exact inline
expression for the specific step — the "helper inventory".)

| Fact | Source (pull through this) |
|---|---|
| Sponsor / sites / product name | `COMPANY`, `SENDING_SITE`, `RECEIVING_SITE`, `PRODUCT`; `title_block(DOC, UO_TITLE)` |
| Process train order + step roles | `CFG.train_order`, `UNIT_OP_TITLES`, `UNIT_OP_ROLE`, `process_steps_df()` |
| Document IDs / titles / cross-refs | `DOC_REGISTRY`, `related_docs_md(DOC)`, `corpus_docs_md(DOC)` |
| SOP / AMV numbers | `SOP_REFS`, `AMV_REFS`, `<KEY>_SOP_REFS`, `<KEY>_AMV_REFS`, `sop_table(...)` |
| CQAs a step sets / clears (+ acceptance, criticality) | `cqas_for(key)`, `cqas_by_keys([...])` |
| Parameters, set-points, NOR/PAR, class, study | `report_params(key)` (report), `plan_params(key)` (plan) |
| DoE structure (factors, responses, run counts) | `st.DOE_FACTORS`, `st.DOE_RESPONSES`, `st.RSM_TOP`, `doe_runs(key, kind)` |
| Effects / coefficients / ANOVA / model adequacy | `doe_report` (`D.screening_effects_df`, `D.rsm_coeff_df`, `D.anova_lof_df`, `D.fit_summary_df`, `D.fit`) |
| Centre-point reproducibility / pure error | `D.center_cv_df(key, kind)` |
| Figures (surfaces, contours, diagnostics) | `D.fig_rsm_contours(...)`, `D.fig_diagnostics(...)` |
| Commercial-scale capability (Cpk) | `cap_for([keys])`, `cap` |
| Monte-Carlo batch count, product targets, scale | `V['n_monte_carlo']`, `CFG` (`meta.*`) |
| Deviation register + facts + scalars | `dev_register(DOC)`, `dev_facts(DOC)`, `dev_*` module globals |
| Whole-train control-strategy summaries | `cpp_params(...)`, `class_counts()` |

## 11. Voice

Third person; past tense for what was done, present for what holds; passive where the
object of study outranks the actor. Register **varies by section, deliberately**
(WRITING_GUIDE §4 and `section_plan.yaml`) — an administrative sub-section is three flat
sentences, a design-space justification is dense and defensive. The rhetorical moves and
gold excerpts live in `authoring/REGISTER_EXEMPLAR.md`; the full standard in
`authoring/WRITING_GUIDE.md`. The narrator is always Novacyte MSAT/PD, writing to a
skeptical BLA assessor.
