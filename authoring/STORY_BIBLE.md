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
- Statistical methods, for the documents that describe them (INV-002, the statistical methods of
  a DoE report, PCMP-001 only if it already names the method): `@montgomery2017` (response surface
  designs, lack of fit, PRESS and predicted R²), `@boxcox1964` (the Box-Cox transformation),
  `@hurvich1989` (AICc, the small-sample information criterion), `@burnham2002` (model selection by
  information criteria), `@fedorov1972` (D-optimal design and the exchange algorithm).

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
  NOR than the platform worst case, the single-batch bound of the A-Mab prediction replaces the
  platform value and the criteria upstream tighten. Where the A-Mab data show, at the one-sided 95 %
  prediction bound of a single batch, that a step does better than the platform worst case, that
  bound replaces the platform value and the
  criteria upstream widen (owner's decision 2026-10-08: "if the data supports it, a criterion
  could be widened, but it needs good arguments"). A widening also needs a downstream model that
  passes the first three adequacy criteria of PCMP-001 §7.2 (a significant model, no significant lack of fit, R² minus predicted R² within its limit) and is not an exact fit; the fourth, on residuals and influential runs, does not decide a widening and is examined by the report that gives the bound (PCMP-001 §7.5, made precise on 2026-10-10 after the PCP-007 and PCP-008 factual checks): a model that fails
  them is not a good argument. Tightening needs no such test. Both directions use the one-sided
  95 % prediction bound of a single batch, never the point prediction and never a confidence bound
  of the mean (the rule of 2026-10-09 below; `iac_verification.csv`: `model_adequate`).
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
is a computed result, and the report states it openly, whatever it is
(`T.sdm_offsets(["protein_a"], studies=["S-PA-SDM"])` against `T.sdm_offsets(["protein_a"])`,
`D.offset_qualification(..., studies=...)`). Under the final analysis (the log-scale model, a ratio
offset, the single-batch criterion in force, the narrowed load NOR) the model is qualified for pool host
cell protein on all nine runs and would NOT be on the three planned runs alone: the further runs narrowed
the interval of the ratio enough to make the qualification possible. State it plainly and computed; a
re-run that changes it must fail an assertion. The qualification rule and the criterion were not changed
because of the further runs. Only the number of replicates grew, and the report says that the decision to
add runs was taken during the re-analysis, after the three-run result was seen, and that the conclusion
therefore rests on runs added after a result was known (optional stopping): name it as a limitation.

**How every DoE is analysed: model selection (owner, 2026-10-09: "all DoEs should be analyzed
correctly").** INV-002 corrective action CA3 (adopted 2026-09-15, before the criteria were fixed at
INV-001 closure) analyses every response-surface output by model selection:
`adequacy.select_model`, used by the report engine (`D.fit`) and by the verification of platform worst
cases (`iac.py`) alike.
1. The scale from the Box-Cox profile of the full quadratic: the log scale where its 95 % interval
   contains 0 and excludes 1, else the raw scale.
2. The model with the lowest AICc among all hierarchical submodels of the full quadratic, by
   exhaustive search (a block term is kept; stepwise search can stop at a worse model).
3. The selected model judged against PCMP-001 §7.2 (and a significant F-test when it has terms). A
   model with no term says the output does not depend on the parameters within the range studied. An
   output with no adequate model is judged on its measured results and sets no range.
   **An exact fit is never adequate** (owner, 2026-10-09; INV-002 review run 2). Where the results have no
   scatter (acidic variants in the low-pH design, which depend on hold time alone), the full quadratic
   reproduces them exactly: there is no pure error for the lack-of-fit test and no residual mean square
   for the model F-test, the prediction interval has zero width, and the Box-Cox profile is unbounded, so
   no scale is chosen. Such an output has no adequate model, is judged on its measured results, and its
   bound cannot replace a platform value. So the bioreactor acidic-variant upper limit stays at its a
   priori value (`iac.csv`), and the INV-002 count of adequate selected models excludes it.
4. A scale-down offset on the scale of the model: a ratio of geometric means for a log-scale model.
**Explaining the log scale and the search to a reader (owner, 2026-10-09: "Do not expect that a reader
will understand this reasoning").** A document that uses either must give the reader all of this, with
numbers from the data, in plain sentences:
- *The model on each scale.* On the log scale, ln(y) = b0 + b1·x1 + … + e. Transformed back,
  y = e^b0 · e^(b1·x1) · … · e^e: each parameter multiplies the output by a fixed factor e^b per coded
  unit, e^(2b) from the low to the high end of its range, and the run-to-run error multiplies it too,
  so its size in ng/mg grows with the level. Give the fold changes of the main effects.
- *Why an output behaves so* (only what the data and the methods support): a purification step removes
  a share of what is present, so a parameter changes the share, not a fixed amount; the precision of
  the method is a percentage of the level (`deviations.methods` precision_pct; ELISA for host cell
  protein), so the scatter of results grows with the level.
- *The assumption, named.* Least squares, and the t-tests, F-tests and prediction intervals built on it,
  assumes residuals that are independent and normally distributed, with mean zero and the same variance
  over the whole range studied. On the raw scale the residual scatter of such an output grows with the
  predicted value (show it, e.g. the residual SD in the lower and the upper half of the predictions);
  on the log scale it is about constant. The evidence is the Box-Cox profile (λ and its 95 % interval,
  which contains 0 and excludes 1) and the residual plot.
- *The implications, plainly.* The criterion stays in its own unit (ng/mg). Effects are fold changes.
  The scale-down offset is a ratio of geometric means, and a scale-down prediction is divided by it. A
  prediction interval is calculated on the log scale and transformed back. It keeps its 95 % coverage
  (the probability that ln y lies between two values is the probability that y lies between their
  antilogs), so it is suitable, and on the log scale the least-squares assumption holds, which on the
  raw scale it does not. It is asymmetric, further above the predicted value than below it (give one
  example). The predicted value is the median of the output (its geometric mean), not its arithmetic
  mean; the upper prediction limit, which decides against an upper criterion, is not affected by that.
  Near an upper criterion, where the level is high, a raw-scale model understates the scatter, because
  its residual SD is pooled over all levels; the interval from the log scale is correctly wider there.
- *The search, in this order.* The goal: among all hierarchical submodels of the full quadratic, the
  one with the lowest AICc. What AICc is: an estimate of how well a model would predict new runs, which
  penalises every estimated term; its small-sample correction raises the penalty when the runs are few
  for the number of terms, as in these designs, so that the criterion does not favour too many terms.
  The method: every candidate is fitted (1,337 for four factors) and the lowest AICc is taken. Why not
  stepwise: a stepwise search changes one term at a time and stops when no single change lowers AICc,
  so it stops where only a combination of changes would lower it further; on this campaign's data a
  stepwise search by AICc would have stopped at a worse model for many outputs
  (`D.selection_comparison()`, count computed). CA2's backward elimination differed in three ways:
  stepwise, by p-value (a test of each term against zero, not a comparison of models) and on the raw
  scale only.

PCMP-001 is not changed (owner): each DoE report records the model selection as a discrepancy from its
plan (computed, `PLAN_DISCREPANCIES`). Version 1.0 and INV-001's comparison use the full quadratic on
the planned runs (`D.planned_full_models()`, `rev1_criteria_in_force`). Consequence for the criteria:
with the anion exchange host cell protein model adequate once selected, its single-batch bound widens the
Protein A pool and the cation exchange host cell protein criteria; the aggregate criteria upstream of
cation exchange move with the cation exchange bound. What depends on CA3 is computed
(`D.ca3_criteria_sensitivity()`: conclusions, PARs and the scale-down qualifications under the criteria
without CA3). Numbers come from `iac.csv`, never from this file.

**INV-002: response-surface models below the model-adequacy criteria.** The re-analysis applied PCMP-001
§7.2 to the planned full quadratic models (the plan's model) and 14 failed the limit on overfitting.
QA opened INV-002 during INV-001 (config `campaign.investigation_2`). Its record, as decided then:
- **The rule** (config `campaign.model_adequacy`, decided 2026-09-02, before any new run): a failing
  model of an attribute of the drug substance specification with an effect is resolved by further runs;
  every other failing model is refitted; viral clearance is not a drug substance test, so its models are
  refitted and no augmentation spikes virus; no augmentation larger than the planned design.
- **Sample size** (INV-002 carries it in full): the smallest D-optimal augmentation of the face-centred
  design, as a second block, giving an assurance of at least 0.90 that the planned model meets §7.2,
  simulated from the refit of the planned runs. The augmentations were made (S-BRX-AUG, S-AEX-AUG).
- **Root cause and CA3** (2026-09-15): the plans prescribed the full quadratic as the predictive model
  and no model selection. CA3 introduced the analysis above for every output.
- **Honesty about the augmentation** (option a, owner 2026-10-09; INV-002 review run 1): once models are
  selected, the bioreactor and anion exchange models are adequate on the planned runs alone, so the
  augmentation was not needed to pass §7.2. But a model selected on the same runs it is judged on passes an
  optimistic check, and the augmentation runs are the independent one: the planned-run models predict
  them (`D.augmentation_prediction_check()`). Two do it poorly (high mannose, bioreactor aggregates), with no
  block effect, and on all runs high mannose loses the interactions the planned runs suggested while
  aggregates gain a pH curvature. So the augmentation changed what two models say; never write that it
  only "sharpened the estimates". The widening of four criteria under CA3 decides two scale-down
  qualifications (Protein A and cation exchange host cell protein) and no conclusion across the NOR
  (`D.ca3_criteria_sensitivity()`). INV-002 says all of this, and describes every procedure it applied.
- **The reports** carry their additional runs (`T.doe_results(UO, "aug")`), the re-evaluation on all runs
  with a block term (`T.model_reevaluation(UO)`), and the discrepancies from the plan. They cite INV-002
  for the sample size and never recompute it.

**What a Version 2.0 plan may add (coordinator, 2026-10-09, after the PCP-006 factual check).** A
Version 2.0 plan is an amendment issued after its studies ran (CA2). It states the a priori criteria, the
fragment method, the scale-down offset rule, the adequacy tests, the judgement statistics, the
verification rule and the execution windows, as PCMP-001 Version 2.0 sets them, and lists each as a
change. It must not add a step-specific decision rule (a refit procedure, a NOR rule for one parameter, a
test chosen for one study) or an execution detail the record does not hold, because such a rule is
written with the data known: that is INV-001 finding 1 again. It never says a rule was "fixed before
the data". It keeps the design, sampling, spiking and **every decision rule** of Version 1.0 as Version 1.0
stated them, even where a study departed from them or the data broke a rule; the report records the
departure. Deleting a Version 1.0 rule after the data hides the departure and is as wrong as adding
one (PCP-003 factual check, 2026-10-09). Where Version 1.0 had no rule the report needs,
the plan says it has none, and the report states its approach and records it as a discrepancy.

**The hold studies, the concentration study and the labels (owner, 2026-10-09).**
- **Hold studies.** No Version 1.0 document planned or reported a hold study. They were made during the
  Version 2.0 re-analysis, after INV-001 closed and after AMD-001 (S-HAR-HLD, S-PA-HLD, S-VI-HLD in
  `study_chronology.csv`), so fragments are by nrCE-SDS on every sample and SEC gives aggregate only.
  Each report records its hold study as a discrepancy from the plan (PD-004-02, PD-005-05, PD-006-05);
  no plan describes one. The held pool is the nominal set-point material of the step model. The retests
  S-PA-RET and S-VI-RET covered the retained response-surface samples only.
- **The A-Mab concentration study at low pH.** PCP-006 Version 1.0 required XMuLV clearance on every run
  of S-VI-UNI; the study measured aggregate and acidic variants only, and PCR-006 Version 1.0 did not
  notice. Version 2.0: the plan keeps the Version 1.0 design; PCR-006 records the omission as deviation
  DEV-006-03, found in the re-analysis, closed by the confirmation study S-VI-UNI2 (PD-006-06: XMuLV-spiked
  holds at both ends of the concentration range, in duplicate, other parameters at their set-points as
  characterized). Concentration does not enter the inactivation in the step model, so the two levels
  differ by run-to-run variation only; PCR-006 judges that with the run-to-run SD of the design, and a
  single run below the claim is not the claim failing (the claim is judged on the model at the least
  favourable NOR combination).
- **Labels.** pCO2 is "CO2 partial pressure (pCO2)" in mmHg; osmolality in mOsm/kg; dissolved oxygen in %
  air saturation; initial viable cell concentration in 10⁶ cells/mL; basal medium concentration as a
  multiple of standard strength (× standard).

**Version 2.0 NOR and set-point decisions (owner, 2026-10-08 and 2026-10-09).** Config `nor_v2` and
`setpoint_v2`; `Parameter.nor`/`.setpoint` are in force, `nor_characterized`/`setpoint_characterized`
(and `D.characterized_nor()`) give what the studies were planned against and run around.
`T.parameters_by_step` footnotes each change. Monte Carlo and PPQ use the values in force; the recorded
experiments, the nominal batch and the verification of platform worst cases use the characterized ones,
so no NOR or set-point decision moves a criterion or a Version 1.0 number.
- **The rule for changing a criterion (owner, 2026-10-09).** Verification tightens or widens a criterion on
  the one-sided 95 % prediction bound of a SINGLE BATCH at the least favourable NOR combination of the
  downstream step (`iac.verification(..., bound="batch")`, `D.VERIFICATION_BOUND`), never on a confidence
  bound of the mean: every output is judged per batch, and the platform worst case it replaces was a
  single run. A tolerance-interval bound would be statistically purer and is too conservative; the
  single-batch prediction bound is the pragmatic choice (owner). Every change of a criterion is argued by
  its risk (owner: "What is the risk of the change? Producers or patient risk. Detectability and impact on
  downstream unit operations and the drug substance."): who bears the risk, whether and where an excursion
  is detected (an in-process or release test), what the downstream steps must then clear, and the drug
  substance probability out of specification (`p_oos.csv`). Numbers from `iac.csv`, never from this file.
  A replacement is not always "the product did better". The platform worst cases of the low-pH hold are
  increases over a 180-min hold (`iac.platform` sources); the A-Mab value is the increase within the NOR
  as characterized, at most 120 min. So the bioreactor aggregate criterion moves because the A-Mab hold is
  shorter, not because the product is more stable: at the edges of the range studied, which include
  180 min, A-Mab adds more aggregate than the platform value. Say so wherever that replacement is
  described (PCP-006 review run 2). It is not true for acidic variants (PCP-006 factual check,
  2026-10-09): every 180-min run of the low-pH design adds less than the platform value. But their model
  is an exact fit, so no acidic-variant bound replaces the platform value and the bioreactor upper limit
  stays at its a priori value (see "An exact fit is never adequate"). Decide any wording per attribute
  from `iac_verification.csv` (`observed_edge` against `assumed`, `model_adequate`), never in general.
  The aggregate criterion is still right, because routine manufacture never holds longer than the NOR,
  and the aggregate model has no pH term, so the bound over the NOR as characterized also covers the NOR
  in force (same longest hold and highest temperature).
- **PCR-006, low-pH inactivation: a decision revised, and confirmation runs.** On the selected XMuLV model
  (main effects of pH, hold time and temperature) the 6.6 claim fails at the worst corner of the
  characterized NOR. First decision: pH NOR 3.30–3.50 with the set-point re-centred to 3.40 (owner: "0.04 pH
  units is not controllable. 0.1 is already very tight for large scale production"), hold-time set-point
  105 min. Two studies support the re-centring: S-VI-OFAT (pH 3.40 against 3.50 over 0–180 min: aggregate
  and fragments rise with hold time, no pH effect beyond method precision; an apparent acidic-variant
  difference sits at time 0 and does not grow, so it is not a pH effect) and S-CEX-VER (cation exchange on
  worst-case material at pH 3.40; three runs from the simulation; both clearance folds pass). The margin
  analysis (`D.par_margins`) then showed the upper pH NOR edge only 0.04 from the XMuLV PAR edge at the
  least favourable hold time and temperature. The decision was REVISED: hold-time NOR 100–120 min,
  set-point 110 min, which gives that edge a margin of about 0.11 (values from config and `D.par_margins`).
  Because the revision moves routine operation toward longer holds, confirmation runs were made at the
  least favourable combination for the product: pH at the lower end of its range and PAR, hold time
  and temperature at their NOR highs (not "within the PAR": the hold-time and temperature PARs reach further) (S-VI-WC, PD-006-03; three runs, as many as S-CEX-VER;
  `D.vi_worst_case_summary()`). Product quality met every criterion of the step. Cation exchange cleared
  aggregate as required. For fragments every run cleared more than the fold the criteria rely on, but the
  one-sided 95 % lower bound of the three runs fell below it, so the pre-set rule is NOT met. Accepted on its
  risk (owner, decision 5a): even with no fragment clearance by cation exchange the hold output meets the
  drug substance limit, fragments are tested at release by nrCE-SDS, and the patient risk is nil. The
  report states that the rule was not met and why that is acceptable; it never pools the runs with
  S-CEX-VER (an analysis chosen after the result, the pattern INV-001 condemns). D-001 is kept.
- **PCR-005, Protein A.** Under the single-batch rule the pool host cell protein criterion is widened only by
  the anion exchange bound. At that criterion the scale-down model is not qualified for pool host cell
  protein at the characterized load NOR (20–40 g/L resin): with the offset at the unfavourable end of its
  interval the conclusion fails. PCR-005 Version 2.0 therefore narrows the load NOR in force (config
  `nor_v2`), where the model is qualified. On the three planned scale-down runs alone the model would not
  be qualified even there; the six supplementary runs (PD-005-01) made the qualification possible
  (computed: `D.offset_qualification(..., studies=[...])`). Run 23 is analysed at its recorded pH
  (PD-005-03); pool host cell protein is modelled on the log scale with a ratio offset.
- **PCR-003, bioreactor acidic variants (owner: option a, confirmed after the osmolality study).** At the
  worst corner of the NOR (high pH, high pCO2, low temperature, long culture) the single-batch prediction
  interval reaches below the 18 % lower limit while the median at manufacturing scale stays just above it
  (`D.nor_worst_corner`). Osmolality, which the response-surface design held at its set-point, lowers acidic
  variants in the screening; narrowing the osmolality NOR to its set-point was not accepted (owner), so the
  effect was measured (S-BRX-OSM, PD-003-01; osmolality at NOR low, set-point and NOR high at the worst
  corner, osmolality set with sodium chloride independently of pCO2, runs per level from the precision of the
  prediction at the NOR high; `D.osmolality_analysis()`). At the NOR high the worst-corner mean falls below
  18 %. Narrowing the pH or pCO2 NOR would restore it, but a NOR is the range the process is routinely
  controlled in (owner, citing the EMA definition: "Narrowing it would not be easy"), so the risk is accepted
  as the producer's (decision 6a): acidic variants have very low criticality, 18 % is a range-of-experience
  limit, release testing detects a low result, and the probability out of specification is quantified
  (`p_oos.csv`, whose simulation varies osmolality within its NOR). Mitigation: acidic variants monitored at
  harvest, and alarm limits inside the NOR on the side that lowers acidic variants, for pH, pCO2 and now
  osmolality.

**Harvest and UF/DF univariate studies (owner's decision 2026-10-08, option A).** Version 1.0
described a univariate study of each of the two steps without a design (S-HAR-UNI, S-UFDF-UNI) and
narrated its outcome, but gave no result for any parameter effect. Those studies keep their record as
Version 1.0 described it, with no data (Version 1.0's harvest plan and report even describe different
level counts; neither is corrected). Version 2.0 adds a NEW study of each step, made during the
re-analysis after INV-001 closed (owner's option c, 2026-10-09): S-HAR-UNI2 and S-UFDF-UNI2
(`univariate_studies.csv`; config `analytics.univariate_nodoe`), discrepancies from the plan PD-004-01 and
PD-010-01. Each parameter at five levels (low, low-mid, set-point, mid-high, high) in duplicate, the others
at set-point; S-UFDF-UNI2 ran on the second TFF skid EQ-TFF-188, in calibration. They are not designed
experiments, and no document calls them one.
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


**Hold-study fragment results.** The hold studies were made after AMD-001, during the Version 2.0
re-analysis (owner, 2026-10-09), so every sample has an nrCE-SDS fragment result and none has an SEC
fragment result. A hold criterion for fragments is judged on every time point.

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
`T.hold_stability(pool)`), in September 2026, as discrepancies from the plans (see above). The design of the viral-inactivation pool study follows A-Mab
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
