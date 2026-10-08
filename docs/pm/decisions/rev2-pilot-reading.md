---
decision: rev2-pilot-reading
work_unit: 2026-10-08_01_rev2-campaign
task: TASK-015
status: waiting on the owner
date: 2026-10-08
---

# The Version 2.0 pilot is ready to read

Four documents are authored, reviewed twice by fresh readers, shipped and annexed:

| Document | What it is | Pages |
|---|---|---|
| `pc_package/INV-001_investigation.pdf` | the QA investigation, new | 30 |
| `pc_package/PCMP-001_master_plan.pdf` | where the a-priori criteria are defined | 35 |
| `pc_package/PCP-005_protein_a.pdf` | the Protein A protocol amendment | 35 |
| `pc_package/PCR-005_protein_a.pdf` | the Protein A report, re-analysed | 55 |

The Version 1.0 originals are in `pc_package/superseded/rev1/` for comparison.

## What to look at

1. **Voice.** Does it read like a process scientist and a QA investigator, not a machine? This
   was your first concern. The rules changed as you agreed. PCR-005 is the strongest test, and
   INV-001 is a new register. **Comment: Sounds good**
2. **The messy tables:**
   - PCMP-001 Table 7.1 (criteria, merged attributes, footnotes);
   - PCR-005's methods table (SEC footnoted, nrCE-SDS from retained samples);
   - the hold table (grid, n.t.);
   - the DoE appendices (method sub-columns, deviation footnotes on runs 11 and 23);
   - INV-001's Version 1.0 / Version 2.0 table (rule codes R1–R4).
3. **The story:**
   - the post-hoc criteria (INV-001);
   - the SEC bias at capture (AMD-001);
   - "wider than Version 1.0 is not a loosening";
   - the qualification that could not pass with three runs (DEV-005-03).

## Decisions that are yours

1. **The review cycle.** The procedure allows one cycle. Each document needed one more factual
   pass, because the second fresh reader still found real contradictions. Several of them were
   in my data, not in the prose. Recommendation: make it two review runs plus one factual pass,
   formally, for the remaining 17 documents. 
2. **Mechanism entries waiting for you.** They are in `authoring/mechanism/`: fragments in
   harvest, protein_a, viral_inactivation and cex, and the leached Protein A entry in protein_a.
   Each is marked `pending_owner_review`. **Comment: Sounds good**
3. **Two calls I made that you may overrule:**
   - Viral clearance is judged on the mean LRF, with the per-batch result reported for
     information. **Comment: Usually a worst case is chosen, not the mean**
   - Data may tighten a criterion and never loosen it. One criterion was tightened: CEX
     aggregate clearance within the NOR is 1.51-fold against the platform's 2.0. **Comment: If the data supports it criterion could be widened but it needs good arguments**
4. **Commit.** Nothing is committed. The work is large, and a checkpoint commit before the other
   17 documents would be prudent.
5. **Pace and cost of the remaining 17.**
   - Each pilot document took one author, two to three judges and one annex pass. Cost was
     about 1–1.5 M subagent tokens per report and less per plan.
   - Up to four documents can run in parallel once their plans exist, in this order:
     1. the plans (PCP-003, 004, 006–010) in parallel;
     2. then their reports;
     3. then PTP-001 and RA-001;
     4. PCMR-001 last.
   - PCR-003 and PCR-006 must address two Version 2.0 findings that INV-001 already states. At a
     NOR corner, acidic variants fall to 17.7 % against the 18 % floor, and XMuLV clearance falls
     to 6.43 against the 6.6 claim.

**General Comments: 

Make a new page after the index so that the document table + approvals are on a separate page,
The Revision History table has an overflow between the texts "Version" and "Effective Date",
Abbreviations should be a table,
For scale down models, it is ok if the models have different means as long as the offset can be determined with sufficient precision. These offset per unit operation should be recorded per unit operation and should be summarized in the PCMR. The PCMR should contain: two matrix table with PPs (columns) vs the unit operations (rows) and affected/studied CQAs in each cell so that it is clear what was studied and what CQAs are affected by which process parameters, an overview of all studies per CQA/PP and unit operation (e.g. univariate, multivariate, number of runs) as table,  an overview for model effects (main, interaction, quadratic) per unit operation. If you find anything else useful, include it. You are free to use merged cells and create complex tables,
For INV-001 Table 4.4. merge the Equipment rows based on their content.
"The safety factor stood in for the worst case of downstream performance without being derived from it." Important: Sentences like this are really hard to read. I have no idea what it means or what the intention is. Try to avoid such dense formulations. Another example: "The viral clearance cri-
teria of R3 have the same weakness" you could say something like recommendation 3 from section 3.3. Do assume that the reader is human and does not have the full context available all the time as you have.
*
---

## Disposition of the owner's comments (2026-10-08)

| Comment | What changes |
|---|---|
| Review cycle (no comment) | Two review runs plus one factual pass become the procedure for the remaining documents. |
| Mechanism entries: sounds good | `pending_owner_review` cleared; `reviewed_by_owner` set to 2026-10-08. |
| Viral clearance: a worst case, not the mean | `decision_statistic` for viral clearance becomes `worst_case`. The other parameters sit at the least favourable combination of their NOR edges, and the claim must hold there. PCMP-001 §6.4 and the plans state it. |
| Criteria may widen with good arguments | The tighten-only rule becomes: verification tightens automatically. A criterion may be widened only where the A-Mab data support it with confidence (the 95 % lower confidence bound of the worst predicted clearance within the NOR beats the platform value), and the report argues it. |
| Scale-down offsets instead of equivalence | Qualification estimates each output's offset (scale-down minus manufacturing) with its 90 % confidence interval. The model is qualified for an output when the offset is known precisely enough that applying either end of its interval changes no conclusion. Offsets are tabulated per unit operation and summarised in PCMR-001. DEV-005-03 becomes "offset not determinable with sufficient precision from three runs". |
| Page break after the contents; revision table overflow; abbreviations as a table | Template and helpers changed; applied to the four pilot documents as a front-matter change. |
| PCMR-001 tables (parameter × unit-operation matrices, studies overview, model-effects overview) | Builders in `tables.py`, named in `section_plan.yaml` for the master report. Built before PCMR-001 is authored. |
| INV-001 Table 4.4: merge equipment rows | Rebuilt as a complex table with merged equipment cells. |
| Dense sentences ("The safety factor stood in for…", "R3 have the same weakness") | A new rule in WRITING_GUIDE (a sentence must be understood by a reader who has not just read the paragraph before it: name the thing, not its code; no abstract stand-ins), and a seventh review question. All four pilot documents get a readability pass. |
| Commit (no comment) | Nothing committed yet. Asked again in the session. |

## Decisions taken in the session of 2026-10-08 (afternoon)

| Question | Owner's answer | What changed |
|---|---|---|
| Commit a checkpoint? | On a branch | Branch `rev2-campaign`, commit `6c51a1a`. `main` stays at tag `corpus-rev1.0` until the campaign ships. |
| Apply widening? | Turn on | `iac.allow_widening: true`. Five criteria widen (Protein A pool HCP 16,000 → 19,241 ng/mg, CEX HCP 400 → 476, Protein A and VI fragments, bioreactor acidic variants upper limit). Two tighten (aggregates upstream of CEX). Widening uses the 95 % confidence bound, never the point prediction. `T.worst_case_verification` shows the bound and the outcome, `T.iac_derivation` marks a widened row. |
| What is "offset known with sufficient precision"? | Decision-based | Qualified for an output when its conclusion over the NOR is the same with the offset at either end of its 90 % CI. Every Version 2.0 judgement subtracts the offset (`D.sdm_offset`, `D.offset_qualification`, `T.sdm_offsets`). Every model qualified on its planned runs at the time. Later superseded: see the adequacy row below. |
| DEV-005-03 and S-PA-SDM2 | "Write as in step 3 but add a discrepancy to the plan in the report. Reports can do stuff which was not planned but a discrepancy has to describe it. Note that the word 'deviation' has a very clear meaning in the GMP world." | DEV-005-03 removed from the deviations. The six runs stay and are recorded as **PD-005-01**, a discrepancy from the plan (`campaign.plan_discrepancies`, `discrepancy_register(DOC)`). The report section becomes "Deviations and discrepancies from the plan", and section_plan tells authors never to call a discrepancy a deviation. |
| Low-pH inactivation fails the 6.6 XMuLV claim at the worst NOR corner (6.43 at pH 3.6, 60 min, 19 °C) | Option C | PCR-006 Version 2.0 narrows the NOR: hold time 90–120 min, temperature 20–23 °C, pH unchanged (worst corner 6.66). Not yet applied: INV-001 must still see the Version 1.0 NOR, so the config needs a Version 2.0 NOR beside the original one. Applying it changes the Monte-Carlo and PPQ outputs (`test_analytics.py` byte-identity list). Done in the PCR-006 batch. |
| Widened criteria rested on inadequate models (PCR-005 author's report) | (my fix) | A widening needs a downstream model that passes the PCMP-001 adequacy tests. Both directions use the one-sided 95 % bound (it had been one-sided 97.5 %). Protein A pool HCP 16,000 → 16,379 ng/mg (cation exchange only), and the other HCP and fragment widenings are dropped. |
| Protein A model not qualified for pool HCP at 16,379 | Narrow load NOR to 20–38 g/L | Config `nor_v2` for Protein A load, and for the low-pH inactivation hold time (90–120 min) and temperature (20–23 °C). `Parameter.nor` is the NOR in force, `nor_characterized` the planned one. Monte Carlo and PPQ follow the NOR in force. On the three planned runs alone the Protein A model would not be qualified for pool HCP; on all nine it is. PD-005-01 says so openly (STORY_BIBLE §9b). |
