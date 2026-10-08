# A-Mab story bible — world canon for the characterization corpus

The durable, self-contained account of the world these documents live in: the
sponsor, the product, the sites, the process train, the platform history, the
document package, and the campaign storyline. It exists so an author can write any
document in the corpus **consistently** without another report present.

Two kinds of content live here, and the distinction is load-bearing:

- **Grounding map** (§10) — where each *fact that is a number or a controlled value*
  actually lives (a helper, a constant, a CSV). The author **pulls** these through
  inline expressions and **never restates them as prose** (WRITING_GUIDE §3, CLAUDE.md
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
  XMuLV/HCP/DNA/leached-PA. DoE. This is the step with the twice-run DoE (§9).
- **Step 9 — Small-Virus Retentive Filtration.** Dedicated size-based small-virus
  removal; principal MVM clearance; orthogonal to steps 6 and 8. DoE.
- **Step 10 — UF/DF (Formulation).** Concentration + buffer exchange to the DS target;
  forms/clears no CQA, so its parameters are KPP, not CPP. **Non-DoE.**

Viral safety is **modular and orthogonal** across steps 6 (low-pH), 8 (AEX) and 9 (VF):
each contributes an independent log-reduction increment, and the cumulative claim is
consolidated in PCMR-001. Any single-step report gives **cross-step credit** and never
implies it delivers the whole viral-safety claim alone (REVIEW_CHECKLIST.md, cross-step credit).

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
| `INV-001` | Investigation Report (QA) | Why every other document is at Version 2.0 (§9b) |

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
  → `AMV-3010`, MVM → `AMV-3018`, fragments by non-reduced CE-SDS → `AMV-3020` under
  `SOP-3015`). Pull the step's subset from its `_AMV_REFS` list.
- SOP/AMV numbers are **identifiers, not measurements** — write them plainly; the numeral
  lint exempts them (WRITING_GUIDE §3). Never invent a new number; use the registry.

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
adverse-before-mitigation story (WRITING_GUIDE §2, rule 8), grounded entirely in the seeded
scalars and the two datasets — never in invented numbers. Milder deviations (probe drift,
feed under-delivery) are simply **retained** with a bounded-impact argument.

## 9b. Version 2.0: the investigation, the method decision, and the criteria (canon)

Every document except `INV-001` exists at **Version 2.0**. Version 1.0 was approved first and
is kept, frozen, in `pc_package/superseded/rev1/`. The story of the change is fixed canon:

**The trigger.** QA reviewed `PCMR-001` Version 1.0 for BLA readiness and found that the
acceptance criteria used to judge each step in the proven-acceptable-range analysis were not in
any approved protocol. They had been introduced at analysis time, after the `PCR-005` analysis
showed that a Protein A pool cannot meaningfully be judged against a drug-substance limit. QA
opened `INV-001` (classification, dates and title: `INV`, from `config` `campaign:`).

**The findings** (INV-001 numbers them; every other document refers to them by number):
1. The step criteria were defined after the data were seen and outside the approved protocols.
2. Each step's criterion was the drug-substance limit carried back through the NOMINAL downstream
   clearance of this campaign, then divided by a "safety factor" that differed by step. The
   factors were chosen so that every step passed at its own set-point.
3. The glycan and acidic-variant limits at the bioreactor were the mean plus 2.5 standard
   deviations of the capability data they were then used to judge.
4. Acidic variants were printed with a two-sided range and assessed for capability against its
   upper end alone.
5. The records gave no execution dates, so the equipment tables appeared to cite expired
   calibrations.
6. A separate finding from the method side. In the CEX fraction study (`S-CEX-FRC`), SEC and
   non-reduced CE-SDS were run on the same samples. SEC read fragments high wherever the matrix
   still carried host cell protein, part of which elutes in its low molecular weight window (the
   excess is a few tenths of a percent and can never exceed the host cell protein present), and
   agreed with CE-SDS from the CEX pool onward.

**The method decision** `AMD` (id, date and title in `config` `campaign.method_decision`). From
its date, fragments are measured by nrCE-SDS in every study, at every step, so that one method
spans the train. Response-surface samples of Protein A and viral inactivation that had been
retained were re-tested by CE-SDS. Screening samples were not retained, so those SEC results are
kept but marked as not used. The re-executed anion exchange DoE (DEV-008-01) ran after the
decision and measured fragments by CE-SDS. Its invalidated first execution had used SEC.
Fragments were not in scope of the bioreactor DoE. Which method ran in which study is
`method_plan.csv`, and the table is `T.methods_by_study()`.

**Thresholds.** PCMP-001 Version 2.0 states the campaign thresholds (`THRESHOLDS`, `CPK_TARGET`,
`CPK_MIN`): the capability target and minimum, and the model-adequacy limits.

**The criteria (CAPA).** `PCMP-001` Version 2.0 defines intermediate acceptance criteria a
priori:
- **The rule.** Each drug-substance criterion is carried backward through the train, using the
  worst case each downstream step showed on the platform (X-Mab, Y-Mab and Z-Mab). That is the
  lowest clearance fold and the largest increase. No margin is applied.
- **Attributes no step changes.** The glycans keep their drug-substance criterion.
- **Viral clearance.** Each step is held to its platform claim. The claims sum to the
  cumulative requirement.
- **Why applying them retrospectively is acceptable.** The derivation uses no data from the
  studies it judges.
- **Verification.** Each report checks the worst cases that the criteria upstream of its step
  rely on. The rule, stated in PCMP-001 before any study, is: where a step does worse within its
  NOR than the platform worst case, the A-Mab prediction replaces the platform value and the
  criteria upstream tighten. Where the A-Mab data show, at the 95 % confidence bound, that a step
  does better than the platform worst case, that bound replaces the platform value and the
  criteria upstream widen (owner's decision 2026-10-08: "if the data supports it, a criterion
  could be widened, but it needs good arguments"). A widening also needs a downstream model that
  passes the adequacy tests of PCMP-001 (R² minus predicted R², lack of fit): a model that fails
  them is not a good argument. Tightening needs no such test. Both directions use the one-sided
  95 % confidence bound, never the point prediction (`iac_verification.csv`: `model_adequate`).
  Each report that relies on a widened criterion gives the argument: the bound, the runs behind
  it, and why the downstream step's performance at A-Mab is known well enough. Which criteria
  tightened and which widened is a result read from `iac.csv` (`tightened`, `widened`), never
  typed. One assumption was not confirmed: within its NOR, cation exchange cleared aggregate less
  than the platform worst case. That tightened the aggregate criteria upstream of cation
  exchange. Whether any proven acceptable
  range moved because of it is a result. Each affected report states it from its own PAR table,
  and nothing here asserts it.
- **The flow of the derivation.** Rule: `config` `iac:`. Derivation: `amab_process/iac.py`.
  Table: `iac.csv`, with `T.iac_derivation()`. Verification: `iac_verification.csv`, with
  `T.worst_case_verification()`. The Version 1.0 criteria: `criteria_rev1.csv`, with
  `T.criteria_change()`.

**Wider than Version 1.0 is not a loosening (say so where it applies).** Several Version 2.0
criteria are wider than the limits Version 1.0 applied. The Protein A host cell protein criterion
is the clearest case. That is not data loosening an approved criterion outside the rule:
- The Version 1.0 limits were never approved criteria. They were applied at analysis and appear in
  no approved plan (finding 1).
- Version 2.0 replaces them with criteria derived a priori. The tighten-only rule applies to the
  a-priori criteria from here on, together with the widening rule above.

A document that shows a criterion wider than its Version 1.0 value states this once, plainly. It
does not leave the reader to infer it.

**Scale-down models: offsets, not equivalence (owner's decision 2026-10-08).** A scale-down model
may differ in mean from manufacturing scale, provided the difference is known precisely enough.
- The offset of an output is the mean of the scale-down set-point runs minus the mean of the
  manufacturing-scale batches, with its 90 % confidence interval (`D.sdm_offset`).
- Every Version 2.0 judgement against a criterion subtracts the offset from the scale-down
  prediction, so ranges and conclusions are stated at manufacturing scale.
- The model is qualified for an output when its conclusion over the NOR is the same with the offset
  at either end of its interval (`D.offset_qualification`). An output with no criterion at the step
  (step yield, column efficiency) has its offset recorded, and nothing depends on it.
- PCMP-001 states the rule. Each PCP-00N applies it, each PCR-00N reports `T.sdm_offsets([UO])`,
  and PCMR-001 summarises `T.sdm_offsets()` for the whole train.
- Leached Protein A is lower in the scale-down model. The manufacturing load is held longer before
  capture, so host cell proteases in it cleave more ligand (leaching by itself is highest on new
  resin, so cycle history is not the cause). Under the offset rule this is simply the offset of that
  output, and the report gives the cause.

**PD-005-01 (a discrepancy from the plan, not a deviation).** PCP-005 planned three scale-down
set-point runs (S-PA-SDM). During the Version 2.0 re-analysis six further set-point runs were made
(S-PA-SDM2) to narrow the offset interval of pool host cell protein, whose conclusion over the NOR
lies close to its criterion. The plan did not foresee them, so PCR-005 records them as a
discrepancy from the plan (`discrepancy_register(DOC)`, config `campaign.plan_discrepancies`). It
is not a deviation: no procedure or GMP requirement was departed from. What the extra runs changed
is a computed result, and the report states it openly: on the three planned runs alone the
interval is wide enough that the conclusion fails at its unfavourable end, so the model would not
have been qualified for pool host cell protein; on all nine runs it is
(`T.sdm_offsets(["protein_a"], studies=["S-PA-SDM"])` against `T.sdm_offsets(["protein_a"])`). The
qualification rule and the criterion were not changed after the three-run result was seen. Only
the number of replicates grew, and the report says that the decision to add runs was taken after
that result.

**Version 2.0 NOR narrowings (owner's decisions 2026-10-08).** Two reports narrow a NOR, because
the conclusion over the NOR as characterized did not hold. Config `nor_v2`; `Parameter.nor` is the
NOR in force, `Parameter.nor_characterized` and `D.characterized_nor()` give the NOR the studies
were planned against. `T.parameters_by_step` footnotes each narrowed NOR.
- PCR-006: low-pH inactivation. At the worst corner of the characterized NOR the predicted XMuLV
  clearance is below the 6.6 claim. Hold time 60–120 → 90–120 min, temperature 19–23 → 20–23 °C.
- PCR-005: Protein A. At the characterized NOR the scale-down model is not qualified for pool host
  cell protein (the conclusion fails at the unfavourable end of the offset interval). Protein load
  20–40 → 20–38 g/L resin.
Monte Carlo and PPQ sample the NOR in force. INV-001 closed before either report was issued, so it
says only that the reports narrow the NOR, from its own computed finding.

**Harvest and UF/DF univariate studies (owner's decision 2026-10-08, option A).** Version 1.0 had
no parameter data for the two steps without a design. Version 2.0 reports S-HAR-UNI and
S-UFDF-UNI (`univariate_studies.csv`; config `analytics.univariate_nodoe`): each parameter at five
levels (low, low-mid, set-point, mid-high, high) in duplicate, the others at set-point. They are
not designed experiments, and no document calls them one.
- Harvest: centrate turbidity falls with centrifuge rcf and levels off. Clarified turbidity is flat
  across the depth filter load NOR and rises steeply at the top of the characterized range, as the
  filter nears capacity. Host cell protein, aggregate and step yield show no trend beyond assay
  precision. This keeps A-Mab's assumption (p.85) that harvest has no impact on product quality.
  Post-clarification turbidity is the outcome of the other two parameters. It was studied as a
  challenge: clarified filtrate adjusted to each level with centrate, and the attributes measured.
- UF/DF: residual buffer falls as exp(−DV) (0.034 % at 8 DV, the value Version 1.0 printed).
  Aggregate rises a little with final concentration and TMP. The source gives nothing for this
  step (A-Mab p.86), so this effect is the campaign's own finding, and PCR-010 presents it as a
  result, not as prior knowledge. Its size against the criterion is computed, never stated here.
- The process model carries the same effects (`process.harvest.model`, `process.ufdf.model`), so
  Monte Carlo and PPQ include them. They are zero at set-point, so the nominal batch is unchanged.

**Hold-study fragment results.** The hold studies ran before AMD-001. Their first and last time
points were retained and tested by nrCE-SDS together with the retained response-surface samples,
and the intermediate time points have SEC only. A hold criterion for fragments is judged on the
nrCE-SDS time points.

**What moved because of it.**
- Several Version 1.0 findings were artefacts of the tuned limits. The best example is the
  CEX pool aggregate limit of 1 % HMW (5 % ÷ 5), which made the upper load NOR look unsupported.
- The headline minimum Cpk is now acidic variants against its 18 % floor.
- The integrated Monte-Carlo model gives the probability of an out-of-specification drug
  substance per attribute (`p_oos.csv`).

Every report says what moved for its own step, in "Changes in this revision".

**Chronology.** Each plan was approved before its studies began (`PLAN_APPROVAL`,
`rev1_date(DOC)`); the Version 1.0 title blocks carried the package compilation date instead,
which is part of INV-001 finding 5. Every study has an execution window (`study_chronology.csv`). Every window closes
before the calibration due date of the equipment it used, and before Version 1.0 was approved.

**Hold studies.** The clarified harvest, the Protein A eluate (held at elution pH, before the
inactivation step) and the neutralized viral inactivation pool were each held at two temperatures for seven days (`hold_<pool>.csv`,
`T.hold_stability(pool)`). The design of the viral-inactivation pool study follows A-Mab
Table 4.17.

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
| Revision, investigation, method decision, dates | `doc_version(DOC)`, `rev1_date(DOC)`, `revision_history(DOC)`, `REV1`, `REV2`, `INV`, `AMD`, `PLAN_APPROVAL`, `csv("study_chronology.csv")` |
| CAPA, effectiveness check, thresholds | `CAPA` (DataFrame), `EFFECTIVENESS`, `THRESHOLDS`, `CPK_TARGET`, `CPK_MIN` |
| Intermediate acceptance criteria | `D.iac_table(key)`, `D.effective_acceptance(key, resp)`, `D.acceptance_basis(key, resp)`, `T.iac_derivation(...)` |
| Version 1.0 criteria and the change | `D.rev1_criteria(key)`, `T.criteria_change(...)` |
| Worst-case verification | `D.iac_verification(key)`, `T.worst_case_verification(...)` |
| P(OOS) of the drug substance | `D.p_oos()` |
| Fragments, methods, hold, comparability | `csv("method_plan.csv")`, `T.methods_by_study()`, `T.hold_stability(pool)`, `T.method_comparability()`, `V['fragments_nominal']` |
| Complex DoE tables | `T.doe_results(key, kind)`, `T.criteria_results(key)`, `T.parameters_by_step(...)` |
| Univariate studies | `csv("univariate_studies.csv")`: each univariate parameter in duplicate at both ends of its characterized range (S-xx-UNI); set-point reference = the qualification runs |
| Run order, per-pool HMW, residual DNA (Protein A) | `run_order` column in every DoE CSV; `hmw_sec_pct`, `dna_load_pg_mg`, `dna_pool_pg_mg` in the Protein A DoE CSVs (DNA on centre points only) |
| Scale-down model qualification | `csv("sdm_qualification.csv")` (with `plates_per_m`, `asymmetry` for the chromatography steps; PD-005-01's supplementary runs are study S-PA-SDM2): set-point runs, scale-down (n=3) against manufacturing (n=5), per step. Offsets and qualification: `D.sdm_offset`, `D.offset_qualification`, `T.sdm_offsets`. Leached Protein A has a real scale effect, protease cleavage of the ligand during the longer load hold at scale (config `analytics.sdm.scale_offset`) |

## 11. Voice

Third person. Past tense for what was done, present for what holds. Passive where the
object of study outranks the actor.

The register is **plain technical English at about C1 level**, modelled on the two
published human documents in `refs/text/` (PDA Technical Report No. 60 and the A-Mab case
study). Verbatim exemplar passages from both are in `authoring/REGISTER_EXEMPLAR.md`, and
the measurable targets are in `WRITING_GUIDE.md` §4, enforced by `authoring/check_style.py`.
Short sentences, almost no em-dashes or semicolons, no coined compounds, no commentary on
your own rhetoric.

Register still varies by section (`section_plan.yaml`): an administrative sub-section is
three flat sentences, a design-space justification is careful and complete. The narrator is
always Novacyte MSAT/PD, writing to a skeptical BLA assessor.

**Never** take the voice from an existing document in `pc_package/`. The first-pass corpus
was written in a machine register, and copying it reintroduces the problem.
