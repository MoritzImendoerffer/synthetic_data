# Factual check: PCP-003 (Production Bioreactor, Process Characterization Plan), Version 2.0 draft

- **Checked by:** Claude Opus 5.5 (`claude-opus-5-5`), as a subagent
- **Date:** 2026-10-09
- **Document:** `.claude/work/2026-10-08_01_rev2-campaign/PCP-003_bioreactor.DRAFT.run2.txt`, the text of `pc_package/PCP-003_bioreactor.DRAFT.pdf` as rendered on 2026-10-09
- **References:**
  - fact sheet `authoring/out/PCP-003.brief.md`, regenerated on 2026-10-09;
  - PCMP-001 Version 2.0, rendered `pc_package/PCMP-001_master_plan.pdf`;
  - frozen Version 1.0 plan `pc_package/superseded/rev1/PCP-003_bioreactor.pdf`;
  - context note `data-state-2026-10-09b.md`.
- **Method:**
  1. I read the document and the brief in full.
  2. I checked every sentence that carries a number, and every sentence whose deciding word depends on data, against the document's own tables and the brief.
  3. I opened the data in `outputs/data/` and `config/parameters.yaml` where the brief was silent.
  4. I recomputed the model-derived claims read-only through the engine, using scratch scripts in the session scratchpad (`fc003/s1.py` to `s5.py`). These covered the screening effects, the discrepancy register, the verification of the platform worst cases, the low-pH aggregate model over both NOR grids, the residual tests, the NOR worst corners, the offsets and the PAR table.
  5. I compared the design, sampling, procedures and rules section by section with the frozen Version 1.0 plan and with PCMP-001 Version 1.0 and 2.0.
  6. For context only, I read the rendered INV-001, the INV-002 draft, RA-001 Version 1.0, PCR-003 Version 1.0, the PCP-005 Version 2.0 PDF and the PCP-006 Version 2.0 draft PDF.
  7. I read no `.qmd` file, and nothing under `authoring/rhetorical/` or `authoring/history/`.

Every number in the document checks out (see "Checked and correct"). The errors are all of one kind. The amendment deletes Version 1.0 rules, adds new rules, and rewrites the sampling, the sequence and the prior knowledge to fit what was executed. Most of these changes are missing from "Changes in this revision". In three places the document says that no rule exists where Version 1.0 had one.

---

## Errors

### 1. §6.3 denies the Version 1.0 rule for choosing the response-surface factors, and the screening shows that rule was breached

- **Where:** §6.3 Response-surface design, last paragraph.
  > "The response-surface study starts after Process Development and Statistics have reviewed the results of the screening study. This plan sets no rule by which that review could change the factors of the response-surface design."

  Supporting sentence, same section:
  > "The master plan PCMP-001 plans the response-surface design of this step in 4 of its 5 multivariate parameters (PCMP-001 §6.1)."
- **What it says:** the plan has no rule linking the screening result to the response-surface factors, and the 4-factor design is fixed by PCMP-001.
- **What the sources say instead:**
  - **Version 1.0, §6.3:**
    > "The parameters actually carried into the response surface design will be those the screening analysis identifies as active on the attributes of Table 4.1. If screening identifies a different subset, the design will be amended before execution, the amendment will be approved by the functions listed in Table 1, and it will be reported in PCR-003 with the screening result that prompted it."
  - **PCMP-001 Version 2.0, §6.1:** the response-surface design is "a central composite design over the factors that each step plan carries forward from the screening". PCMP-001 Version 1.0 §6 says the same ("The factors that screening carries forward").
  - **Data:** `effects_bioreactor.csv` shows all 5 screening factors active.
    - Osmolality has significant main effects on galactosylation (−2.45, p = 0.008) and acidic variants (−2.55, p = 0.013).
    - Osmolality also has three significant interactions on galactosylation: temperature × osmolality +3.70 (p = 0.002), pCO2 × osmolality +2.18 (p = 0.011) and osmolality × duration +1.93 (p = 0.016).
    - The frozen PCR-003 Version 1.0 itself says "Osmolality is active on two responses". It dropped osmolality on a summed-effect ranking that the plan does not contain.
  - **Consequence:** under the Version 1.0 rule, the response-surface design should have been amended to include osmolality before execution. The later osmolality study S-BRX-OSM (PD-003-01) answers that gap.
- **Problem:** by deleting the rule and saying it never existed, the amendment makes the execution look compliant. That is the INV-001 finding 1 pattern, a rule changed after the data were seen. "Changes in this revision" does not mention it.
- **Fix:** restore the Version 1.0 §6.3 rule word for word, and let PCR-003 record the departure (osmolality active in screening, not carried forward, design not amended) as a deviation or discrepancy. If the owner decides to drop the rule, list the deletion as a change and give the reason.

### 2. Change 7 and §7 item 2d add residual tests that PCMP-001 does not set, and every bioreactor model fails them

- **Where:**
  - §1.1 item 7:
    > "A regression of the absolute residuals on the predicted values, and a regression of the residuals on the order in which the runs were started, must each show no slope significant at α = 0.05. No run may have a Cook's distance above 4/n, where n is the number of runs of the design."
  - §7 item 2d repeats the tests, followed by:
    > "A model is used for prediction only if it meets all four criteria (PCMP-001 §6.3)."
- **What it says:** a model that fails either regression test, or has any run with Cook's distance above 4/n, is not adequate and is not used for prediction.
- **Source 1, PCMP-001 Version 2.0 §7.2 item 4:** sets only "The residuals show no pattern against predicted values or run order, and no single run dominates the fit". It names no test and no cut-off.
- **Source 2, the engine:** applies none of these tests. `adequacy.select_model` and `adequacy.adequacy` judge lack of fit, the R² gap and the F-test only. `D.model_status` returns "selected" for all 5 bioreactor outputs, and the PAR table rests on these models.
- **Source 3, the other plans:** the tests are not generic, and the plans define n differently.
  - PCP-005 Version 2.0 states the same cut-off as 0.14 for the 28 planned runs.
  - The PCP-006 Version 2.0 draft defines n as "the number of runs in the fit".
  - PCP-003 defines n as "the number of runs of the design". The bioreactor models are fitted on 44 runs (28 planned plus 16 in S-BRX-AUG).
  - The tests appear only as the Protein A discrepancy PD-005-02 ("no selected model meets criterion 5 of the plan").
- **Source 4, recomputed (`fc003/s2.py`) on the selected models, 44 runs, 4/n = 0.091:**

  | Output | Runs above 4/n | Runs above 4/28 | Slope of absolute residuals on predicted (p) |
  |:--|:--|:--|:--|
  | Afucosylation | 4 | 3 | 0.062 |
  | Galactosylation | 3 | 2 | 0.027 |
  | High mannose | 4 | 3 | 0.16 |
  | Acidic variants | 4 | 3 | 0.0009 |
  | Aggregate | 2 | 0 | 0.29 |

  - Galactosylation and acidic variants therefore also fail the absolute-residual test.
  - The full quadratic models on the 28 planned runs have 2 to 7 runs above 0.143 each.
- **Consequence:** under this plan's own rule, no bioreactor model is adequate. No PAR, no design space and no qualification decision could then be made, because the qualification uses the response-surface model. The computed PCR-003 register (PD-003-01 to PD-003-03) records no departure. This is a step-specific rule written after the data were known.
- **Fix:** state §7.2 criterion 4 as PCMP-001 states it and delete change 7. If the campaign wants these tests, put them into PCMP-001 with one definition of n, and have PCR-003 record the failure as a discrepancy, as PD-005-02 does.

### 3. §7 items 4 and 6 drop the Version 1.0 rule that the NOR must lie inside the acceptable region, and acidic variants fail at the NOR corner

- **Where:**
  - §7 item 4:
    > "Neither PCMP-001 nor this plan sets a rule for a PAR that is narrower than the NOR, and the report states its approach."
  - §7 item 6 (design space) has no requirement on the NOR.
- **What it says:** no rule decides what happens when an attribute fails inside the NOR.
- **Version 1.0, §7:**
  > "The normal operating ranges must lie inside the declared region. If they do not, the operating region will be reported as it is found and the normal operating range narrowed until it fits inside."

  and
  > "The plan is met for a parameter when such a range is established and the normal operating range lies inside it for every one of those attributes."

  PCMP-001 Version 1.0 §7 says the same: the design space is the region "and the normal operating range sits inside it".
- **Data:**
  - `D.nor_met("bioreactor","acidic_variants")` is False.
  - At the worst NOR corner (pH 6.95, 34.5 °C, 18 days, 130 mmHg) the single-batch 95 % prediction interval is 16.2 % to 20.8 %, against the criterion of 18.0 % to 39.0 %.
  - PD-003-01 records "narrowing the osmolality NOR was not accepted", and commit 0b452c9 says "no NOR narrowed".
  - So the Version 1.0 rule would have required a narrower NOR, using the single-batch judgement that §7 item 6 now prescribes.
- **Problem:** the claim that this plan sets no rule is false against Version 1.0. "Changes in this revision" does not list the deletion.
- **Fix:** keep the Version 1.0 rule. PCR-003 then records the decision not to narrow as a departure, with the risk argument. Alternatively, list the deletion as a change with its reason.

### 4. §7 item 5 denies the Version 1.0 decision rule for the univariate study

- **Where:** §7 item 5.
  > "Neither PCMP-001 nor this plan sets a decision rule for the univariate study or for the NOR of osmolality, and the bioreactor report PCR-003 states its approach."
- **What it says:** no rule governs the univariate results.
- **Version 1.0, §6.4:**
  > "If a univariate assessment shows an effect on a quality attribute that the mechanism does not account for, the parameter will be carried into a multivariate study and the plan amended."

  Version 1.0 also said that the range "is therefore conditioned on the other parameters sitting at their set-points, and the report will state that condition where it states the range".
- **Data:** in `univariate_studies.csv` (S-BRX-UNI), one effect is significant. Initial viable cell concentration raises acidic variants by 3.4 points: 19.6 % and 20.8 % at the low end against 23.5 % and 23.6 % at the high end (t-test p = 0.03, 2 df). Neither the Version 1.0 nor the Version 2.0 mechanism names this effect. Version 2.0 §4.1 expects initial viable cell concentration to raise aggregate, which did not move.
- **Problem:** the rule is deleted silently, and the "no rule" statement is false against Version 1.0.
- **Fix:** restore the Version 1.0 §6.4 rule and condition. PCR-003 then judges the initial viable cell concentration effect against it.

### 5. HCP, DNA and the wider qualification comparison are dropped from the sampling plan to match what was done

- **Where:**
  - §4.2:
    > "They are not responses of the bioreactor studies, because neither has a criterion at this step."
  - §4.2:
    > "…an effect of culture duration on the load of host cell protein is not assessed in this plan."
  - §5.4:
    > "The sample is tested for the 5 responses by the methods of Table 5.1."
  - §5.1:
    > "The outputs compared are the 5 measured attributes…"
  - Table 3.2 and Table 5.1 no longer list SOP-3012, SOP-3014, AMV-3012 or AMV-3014.
  - §1.1:
    > "The studies, their factors and the ranges studied are unchanged."
- **Version 1.0:**
  - §5.4: "The clarified harvest of each run will be assayed for host cell protein and residual DNA."
  - §6.4: the univariate harvest "will be assayed for the 5 responses and for the two impurity attributes".
  - §5.3 and Table 5.1 list the ELISA and qPCR methods.
  - §5.1: the qualification compares "the viable cell density profile, viability at harvest, titer and the 5 quality responses" against "the at-scale data available from the A-Mab engineering and clinical campaigns".
- **Data:** no bioreactor study file holds HCP, DNA, VCD, viability or titer. This covers the `doe_bioreactor_*` files, the S-BRX-UNI rows and the bioreactor rows of `sdm_qualification.csv`. PCR-003 Version 1.0 nonetheless says that HCP and DNA were measured on the harvested pool.
- **Rules that apply:**
  - The context note §5 says a Version 2.0 plan "keeps the design, sampling and spiking as Version 1.0 planned them, even where a study departed from them".
  - PCMP-001 §7.1 requires each plan to name "the manufacturing-scale data set". Version 2.0 says only "5 batches".
- **Fix:** restore the Version 1.0 sampling and the comparison scope, with their methods. PCR-003 then records that HCP, DNA, VCD, viability and titer were not measured. Name the manufacturing-scale data set in §5.1. Change "the studies … are unchanged" so that it does not cover the sampling.

### 6. The Version 1.0 calibration check is replaced by a due-date argument written after a probe-drift deviation

- **Where:** §12 risk 2.
  > "The calibration interval of the probe limits this risk, and every study window closed before the next calibration of the probe was due (Section 11)."

  §9 no longer contains a calibration check.
- **What it says:** keeping each study inside the calibration interval controls drift of the pCO2 probe.
- **Version 1.0, §9:**
  > "Instruments used to set or measure a studied parameter will have their calibration verified before execution and confirmed after it. A calibration failure found after execution will be treated as a deviation, and the impact on the runs performed since the last successful verification will be assessed and reported."
- **Data:** `deviations.csv` records DEV-003-01, "Dissolved-CO2 probe drift during screening run 4". Its root cause is `probe_drift_between_calibrations`, detected by "in-process monitoring vs offline reference", at an offset of 6.5 mmHg. So drift happened inside the calibration interval, and a due date does not limit it. The risk text matches that deviation, and was therefore written with it known.
- **Problem:** the change list does not mention the removal.
- **Fix:** restore the Version 1.0 verification before and after execution. Do not present the due date as the control for drift.

### 7. §11 rewrites the planned study sequence to fit the execution

- **Where:** §11.
  > "The univariate study starts after the screening study ends, and the response-surface study starts after the screening results have been reviewed (Section 6.3). The univariate and response-surface studies then overlap in time."
- **What it says:** the univariate study follows screening and overlaps the response-surface study.
- **Version 1.0, §11 and Table 11.1:** the phases run qualification, then screening, then the response-surface design (phase 3), then the univariate assessments (phase 4), "so the phases run in the order shown".
- **Data:** in `study_chronology.csv`, S-BRX-UNI started on 2025-10-06, before S-BRX-RSM started on 2025-10-20. The execution departed from the Version 1.0 sequence, and the amendment changed the plan to match. The change list does not mention it.
- **Fix:** keep the Version 1.0 sequence and let PCR-003 record the departure, or list the change.

### 8. §4.1 changes the prior expectation for basal medium and feed, against the brief, RA-001 and Version 1.0

- **Where:** §4.1, last paragraph.
  > "The risk assessment RA-001 ranked the 4 remaining parameters lower (Section 4.3), but each has a route to the quality attributes. … The basal medium concentration and the nutrient feed-1 volume set the supply of glucose, amino acids and the precursors of UDP-galactose. A lower supply is expected to deplete the galactose donor earlier and to lower galactosylation."
- **What it says:** less basal medium or feed is expected to lower galactosylation.
- **Brief §2b (mechanism, reviewed by the owner):**
  - Basal medium "has little effect on the glycoforms, because the feed strategy replenishes the same components".
  - For feed, "within the studied range the culture is fed to excess".
- **Version 1.0 §4.1:**
  > "Across the ranges in Table 6.1 the feed replenishes those precursors faster than the cells consume them, so none of the three is expected to move a glycan attribute at a fixed culture age."

  This was the stated reason for studying these parameters one factor at a time (Version 1.0 §4.3 and §6.4).
- **RA-001 Version 1.0 §4:** "none is scored against a quality attribute". It credits basal medium with a "shallow effect on afucosylation", not galactosylation.
- **Data:** the univariate data do not show the expected direction. High basal medium gave 2.7 points lower galactosylation, which is not significant.
- **A related, lower-confidence issue:** §4.1 adds expected directions that Version 1.0 did not state, namely that high osmolality lowers galactosylation and raises high mannose. The screening had already shown the galactosylation direction (−2.45, p = 0.008).
- **Problem:** the change is not listed.
- **Fix:** return to the Version 1.0 and brief statement, that the culture is fed to excess and little glycan effect is expected, and cite the RA-001 platform effects as RA-001 states them. Do not add expected directions that the data were already known to show.

### 9. §6.2 and assumption 5 assume pCO2 and osmolality effects add, but the screening estimates their interaction and finds it significant

- **Where:**
  - §6.2:
    > "The effect of a pCO2 excursion at manufacturing scale is then the effect of pCO2 in the models plus the effect of the rise in osmolality that comes with it."
  - §12 assumption 5:
    > "The effects of pCO2 and of osmolality, each estimated at a constant level of the other, add when both change together at manufacturing scale (Section 6.2)."
- **What it says:** the combined effect is a simple sum.
- **Source 1, the plan itself:** §6.2 says the design "estimates all 5 main effects and all 10 two-factor interactions". The pCO2 × osmolality term is therefore measured, not assumed.
- **Source 2, the data:** `effects_bioreactor.csv` gives pCO2 × osmolality on galactosylation as +2.18, p = 0.011. The effects do not add for the attribute where both act.
- **Source 3, §5.5:** the screening model "is not used for prediction". Yet the sentence combines a screening osmolality effect with the response-surface pCO2 effect to predict an excursion.
- **Problem:** this is a new step-specific assumption, in neither Version 1.0 nor PCMP-001.
- **Fix:** delete assumption 5 and the "plus" sentence, or replace them with "the combined effect includes the pCO2 × osmolality interaction that the screening estimates".

### 10. §5.1 cites PCMP-001 §5 for half of its sentence, then contradicts the other half without calling it a departure

- **Where:** §5.1.
  > "Agitation and gas flow depend on scale, and they are set so that oxygen transfer matches that of the commercial vessel (PCMP-001 §5)."

  and, later in the section:
  > "The carbon dioxide stripping of the commercial vessel is therefore not matched."
- **PCMP-001 Version 2.0 §5:**
  > "Agitation and gas flow are set to match the oxygen transfer and carbon dioxide stripping of the commercial vessel."

  PCMP-001 §1 adds: "Where a step plan departs from this plan, it should state the departure and the reason for it."
- **Fix:** state it as a departure from PCMP-001 §5, with the reason already given (pCO2 is a controlled factor). Alternatively, have PCMP-001 §5 corrected so that the citation is true.

### 11. §7 item 2 drops the Version 1.0 remedies "or the design augmented" and the normality check without listing them

- **Where:** §7 item 2.
  > "A model that fails the lack of fit test or the limit on overfitting is either refitted with a justified change of terms or transformation, or it is not used to set a range (PCMP-001 §7.2)."

  Criteria a to d contain no normality check.
- **Version 1.0, §7:** a failing model "will be reduced, or the design augmented, and the revised model reported with the reason for the revision". Adequacy also required "no departure from normality".
- **Consequence:** Version 1.0 foresaw the 16-run augmentation S-BRX-AUG. It now appears as PD-003-02, a discrepancy from "the face-centred central composite design of 28 runs". Change 7 claims to state "the tests by which the residuals … are judged" but does not say that normality was dropped.
- **Fix:** keep "or the design augmented" and the normality criterion, or list both removals as changes.

### 12. Other Version 1.0 rules are dropped without listing

Each item below is a Version 1.0 rule that the amendment removes, and none of them appears in "Changes in this revision".

- **Run acceptance (Version 1.0 §7):**
  > "A run will be accepted into the analysis when it was executed within the tolerances of SOP-2003 for the parameters not being varied and when the harvest samples met the acceptance criteria of the analytical methods … A study whose design is invalidated by a deviation will be re-executed in full …"
  - Version 2.0 §9 keeps only "A run whose recorded setting lies outside the control band … is recorded as a deviation, and its impact is assessed in the report".
  - §12 risk 3 keeps only "the report states whether the design was repaired or re-executed".
  - This bears on DEV-003-02, a feed under-delivery on a centre point, a parameter that was not varied.
- **Practical importance (Version 1.0 §7):**
  > "An effect will be called practically important when the predicted change in the response across the characterization range is large relative to the width of the acceptance criterion …"
  - Version 2.0 §7 item 7 leaves "practically relevant" and "appreciably" undefined, and the classification depends on them.
- **Amendment procedure and review:**
  - Version 1.0 §13 says any change to the designs, analyses or criteria "will be documented as an amendment, approved by the same functions". Version 2.0 §9 replaces this with recording "work that this plan does not foresee" as a report discrepancy.
  - Version 1.0 §9 also had a second-person review of data and analyses, which is dropped.
  - The Version 1.0 §7 criteria for completing the study are dropped.
- **Fix:** list each of these in §1.1 with its reason, or restore it.

### 13. Execution and analysis details from the data are added to the plan

These details are in neither Version 1.0 nor PCMP-001 Version 2.0, and none is a generic test.

- **§6.4:**
  > "…in 2 replicate runs at each end … The univariate study has 16 runs."

  Version 1.0 gave no replication. The figure matches `univariate_studies.csv`.
- **§6.4:**
  > "The set-point reference of the univariate study is the 3 set-point runs of the qualification study S-BRX-SDM…"

  §5.5 adds:
  > "The results of the univariate study are reported against the criteria of Table 7.1 and beside the set-point runs of the qualification study. The difference between the two ends of each range is stated together with the replicate variation at each end."

  This is an analysis procedure for one study, chosen with the data known.
- **Appendices A and B:** "with the randomized start order". The start orders match the executed `run_order` in the `doe_bioreactor_*.csv` files exactly. Version 1.0 showed the design order only.
- **§9:** "The data set is locked before the statistical analysis starts". **§6.3:** "after Process Development and Statistics have reviewed the results of the screening study". Both are new.
- **Fix:** keep the Version 1.0 wording. If the details are kept, list them as changes. The univariate reference and reporting procedure belong in PCR-003 as its stated approach.

### 14. §8 changes the set-point PAR grid from 81 to 201 points without listing it

- **Where:** §8.
  > "…evaluating the fitted response-surface model at 201 grid points."
- **Version 1.0 §8:** "…at 81 grid points".
- **Engine:** `par_at_design_centre` has used 201 points since commit ac488b2 (2026-07-26), now `PAR_GRID_SETPOINT`. Version 1.0 therefore misstated the executed grid, and Version 2.0 corrects it silently.
- **Note:** registered discrepancy D-001 (set-points against design centre) is unaffected and correctly carried.
- **Fix:** list the correction in §1.1. Alternatively, keep 81 and let PCR-003 record the departure.

### 15. Record corrections are made without listing them

- **Approval date:**
  - §1.1 and the revision history give Version 1.0 as approved on 2025-08-07. The frozen Version 1.0 title block says "Effective 2026-07-24".
  - INV-001 finding F5 and PCMP-001 Version 2.0 change 7 explain the correction. PCP-003 change 6 cites finding 5 for execution dates only.
- **Labels and units:** these were renamed with no mention.
  - "Dissolved CO2 (pCO2)" became "CO2 partial pressure (pCO2)".
  - "mOsm" became "mOsm/kg".
  - "% sat" became "% air saturation".
  - "e6 cells/mL" became "10⁶ cells/mL".
  - "X" became "× standard".
  - "% WV" became "% of working volume".
- **Fix:** add one sentence to change 6 on the approval date, and one change for the labels and units.

---

## Checked and correct

- **Identity and history:**
  - Version 2.0, effective 2026-09-30, supersedes Version 1.0 of 2025-08-07, before S-BRX-SDM started on 2025-08-11.
  - INV-001 was opened on 2026-08-03 and closed on 2026-09-18, classified major, on review of PCMR-001 Version 1.0 for BLA readiness.
  - CA2 (amend PCP-003 to PCP-010) and PA3 (execution dates and calibration status) match `config` `capa`.
  - AMD-001 is dated 2026-03-20.
  - INV-002 is described correctly, and no hold study appears.
  - No acidic-variant widening remains. Labels and units match the context note §4.
- **Table 1.1:** all 10 criterion cells, the rules R1 and R2, the 6.8 margin, "every upper limit … higher", the added 18.0 % lower limit and the unchanged glycan lower limits all match `D.rev1_criteria`, `iac.csv` and INV-001 Table 3.1.
- **Tables 4.1, 6.1 and 6.2:** the CQA register (7 rows, criticality and Tool #1 scores) matches. Set-points, ranges, NORs, units, study types and coded levels match. Each range studied exceeds its NOR at both ends, at 1.5 to 2.5 times the NOR width.
- **Design arithmetic:**
  - Screening: 16 terms, 19 runs, 2 df pure error, 1 df lack of fit.
  - Response surface: 15 terms, 28 runs, 3 df pure error, 10 df lack of fit.
  - 3⁴ = 81 combinations, 5 × 4 = 20 PARs, 66 runs, and 16 univariate runs (2 per end, confirmed in the data).
  - Appendix A is a resolution V half fraction (E = ABCD). The coded levels in Appendices A and B match the data.
- **Table 7.1 and its derivations:**
  - 5.00 × 1.40376 − 0.5586 = 6.46, and 5.00 × 2.00 − 0.70 = 9.30.
  - 40.0 − 1.00 = 39.0, and the lower limit stays at 18.0.
  - Cation exchange: platform 2.00-fold, predicted 1.58, bound 1.40.
  - Low-pH aggregate increase: platform 0.70, edge 0.84, predicted 0.53, bound 0.56. The hold lengths are 180 min and 120 min.
  - I recomputed the low-pH aggregate model. It has no pH term (terms are hold time and temperature), and the bound is 0.5586 over both the NOR as characterized and the NOR in force. The claim "the bound therefore also covers the NORs in force" holds.
- **Method constants:**
  - 81 grid points, 2,000 draws, SD = NOR width / 6 clipped to the range studied, 2.5th and 97.5th percentiles, and 2,000 capability batches all match `doe_report` and `report_values.json`.
  - The offset interval (Student's t with pooled SD, 90 %) matches `D.sdm_offset`.
  - The 201-point set-point grid matches the engine.
- **Schedule:**
  - Table 11.1 windows, EQ-BRX-205, and the calibration due date of 2026-06-14 are correct, and every window closed before that date.
  - The univariate study started after screening ended and overlapped the response-surface study. The qualification runs preceded the univariate study.
  - The 3 scale-down runs and 5 manufacturing batches match `sdm_qualification.csv`.
- **Cross-references:**
  - Table 3.1 matches the brief.
  - The Table 3.2 titles match the brief.
  - PD-003-01 is S-BRX-OSM, matching `discrepancy_register("PCR-003")`.
  - PCR-006, PCR-007, PCP-004, AMD-001 and INV-002 are each cited where used.
  - The A-Mab citations hold: the "roughly 50 %" reliability at the edge of a mean-based region (A-Mab text, ch. 3) and ion exchange not separating glycoforms except sialylated ones.
- **Registered discrepancy D-001:** §8 commits the first analysis to the set-points at full strength. It is registered and not flagged. For the bioreactor, the set-points equal the design centre.

## Could not check

- **Screening review:** whether Process Development and Statistics reviewed the screening before S-BRX-RSM started. No such record exists in the data.
- **Per-run records:**
  - The plan says per-run titer, VCD and viability "are recorded with each run". These records are absent from `outputs/data`, so the statement cannot be verified, and no data support the KPP classes in PCMP-001 Table 4.2.
  - Media and feed lots per run and the SOP-2003 control bands are not in the data.
- **RA-001:** RA-001 Version 2.0 is not reissued, so §4.3 was checked against RA-001 Version 1.0.
- **Approved text of Version 1.0:** I could not confirm which parts of the frozen Version 1.0 text were in the plan as approved on 2025-08-07. INV-001 F1 says the criteria were written in at package compilation. I treated the other Version 1.0 rules in errors 1, 3, 4, 6, 7, 11 and 12 as approved.
- **Later studies (a PCR-003 issue, not a plan error):** S-BRX-OSM and S-BRX-AUG have no equipment in `study_chronology.csv`. Both ran in September 2026, after the EQ-BRX-205 calibration fell due on 2026-06-14, and both vary or depend on pCO2.
- **Mechanistic prose in §4.1:** statements on Golgi transit, Man5, GnT-I, the isoelectric point and sialylation were checked only against the brief, Version 1.0 and the A-Mab text, not against the wider literature.
