# Factual check: PCP-006 Version 2.0 draft (Low-pH Viral Inactivation, Process Characterization Plan)

- **Checked by:** Claude Opus 5.5 (`claude-opus-5-5`)
- **Date:** 2026-10-09
- **Document:** `.claude/work/2026-10-08_01_rev2-campaign/PCP-006_viral_inactivation.DRAFT.factual.txt`, the text of `pc_package/PCP-006_viral_inactivation.DRAFT.pdf` rendered 2026-10-09 17:26 (39 pp.)
- **Method:** I read the document and `authoring/out/PCP-006.brief.md` (17:25) in full, and the rendered PCMP-001 (`pdftotext -layout`). I checked every number-bearing sentence and every data-dependent deciding word against the table of the same document that holds the value, and against the brief. Where those were silent or disagreed, I used `outputs/data/*.csv` (built 13:32) and `config/parameters.yaml` (17:24). I recomputed the model-derived values with the engine, read-only, from a scratch script. For provenance claims I compared the draft with the frozen Version 1.0 PCP-006 and PCR-006 (`pc_package/superseded/rev1/*.pdf`), and with the rendered INV-001, PCP-005 Version 2.0 and RA-001. I read no `pc_package/*.qmd` and nothing under `authoring/rhetorical/` or `authoring/history/`. The data did not change during the check. The only uncommitted config change is PCP-003's approval date.

## Errors

**1. §7.1, item 3: a refit rule stated as fixed before the data**

- **The text:** "This plan applies that rule to a model that fails any of the four conditions (...). The change is fixed here, before the data are seen, and one refit is allowed." It is followed by two bullets: a log transform when the absolute residuals rise with the predicted value, and otherwise hierarchical backward elimination.
- **What it says:** the plan set the refit rule a priori.
- **What the record shows instead:**
  - The dates rule it out. Version 2.0 is effective 2026-09-30 (title block). Every study of the step had ended by 2026-04-17 (brief, study chronology). The Version 1.0 reports analysed the data in July 2026.
  - INV-002 had already found the full quadratics for XMuLV and fragments below §7.2 (brief, model adequacy: R² − predicted R² of 0.317 and 0.73, remedy "refit"). It refitted them by hierarchical backward elimination (INV-002 CA2, config `investigation_2.capa`; `adequacy.reduce`), then replaced refitting with model selection (CA3, adopted 2026-09-15).
  - The draft's rule is essentially that post-data CA2 refit. It also matches neither Version 1.0, whose §7.2 says "Neither outcome is a reason to refit a different model", nor the analysis in force (selected model, brief §4b).
  - The brief says: "A plan is prospective ... It does not describe INV-002, the augmentation or a refit, which came after the plan." PCP-005 Version 2.0 states the same adequacy criteria with no refit rule.
  - As written, the corrective plan repeats INV-001 finding 1: a rule added to a plan after its data were known, worded as if approved before.
- **Fix:** Delete "The change is fixed here, before the data are seen, and one refit is allowed" and the two refit bullets, and keep PCMP-001 §7.2's own rule (refit with a justified change or not used to set a range, else report descriptively), as PCP-005 does. PCR-006 records the model selection as a discrepancy from the plan.

**2. §7.4, paragraph after Table 7.2: "not a more stable product"**

- **The text:** "Where a bound replaces a platform value, the replacement therefore reflects the shorter hold and not a more stable product."
- **What it says:** any replacement of a platform increase comes from the shorter A-Mab hold and never from the product.
- **What the data show instead:**
  - This is a result that only PCR-006 can establish, and for acidic variants the data contradict it.
  - Every response-surface run at 180 min, the hold of the platform value, adds 0.6 % acidic variants. In `doe_viral_inactivation_rsm.csv` the level is 20.886 % at 180 min, 20.686 % at 120 min and 20.486 % at 60 min, the same at every pH and temperature. The brief's verification gives `observed_edge` 0.6. The platform worst case is 1.00 % over 180 min (Table 7.2).
  - So at the same hold A-Mab adds 40 % less, and the bound of 0.40 % reflects a smaller A-Mab increase as well as the shorter hold.
  - The sentence holds for aggregate: 0.84 % at the edges against 0.70 %.
  - It cannot apply to rule 1 (tightening). There the A-Mab increase within the shorter hold is larger than the platform value. "Therefore" does not follow from the hold length alone.
- **Fix:** Replace it with something the plan can state, for example: "A bound smaller than the platform value may reflect the shorter hold rather than the product. PCR-006 states which, from the runs at 180 min." PCMP-001 Version 2.0 §7.3 and §7.5 make the same claim for acidic variants, so its owner should know.

**3. §1.1, change 1: "tighten or widen them"**

- **The text:** "It also sets out the rule by which the verification of the platform worst cases may tighten or widen them (Section 7.4)."
- **What it says:** "Them" is "the intermediate acceptance criteria for the outputs of this step", so this step's own verification may move its own criteria.
- **What the document says instead:**
  - §7.4: "The verification may change the criteria upstream of this step". These are the bioreactor aggregate and acidic variants and the Protein A fragments (Table 7.2).
  - This step's criteria move only through the verification of cation exchange (§7.2, PCR-007).
  - The item as written contradicts the next sentence ("The derivation uses no result of the studies in this plan") and the opening of §7 ("No result of the studies in this plan enters them").
- **Fix:** "... may tighten or widen the criteria upstream of this step (Section 7.4)."

**4. §6.4, the univariate row of Table 5.3, and §12 assumption 4: the univariate study re-described**

- **The text:** "The low-pH hold is run at the low and the high end of the range studied, 5 and 35 g/L, in duplicate." / "The study does not measure XMuLV clearance or fragments, so it supports a range of A-Mab concentration for aggregate and acidic variants only."
- **What it says:** this is the planned design of S-VI-UNI.
- **What the record shows instead:**
  - Version 1.0 §6.4 was the plan under which S-VI-UNI ran (2026-02-02 to 2026-02-06). It planned "settings across the range 5 to 35 g/L", with aggregate, acidic variants "and XMuLV log reduction ... measured on every run".
  - `univariate_studies.csv` holds 5 and 35 g/L in duplicate, with aggregate and acidic variants only.
  - So the draft describes what was done, not what was planned, and §1.1 does not list the change. The XMuLV measurement that was planned and not made reappears as an assumption in §12.
- **Fix:** List the change in §1.1: Version 1.0 planned XMuLV on every univariate run, the study did not measure it, and Version 2.0 states it as an assumption. Otherwise keep the Version 1.0 design and let PCR-006 record the departure.

**5. §5.1, §5.3, Table 5.1 and Table 5.3: the spiking procedure**

- **The text:** "Each run of the designs is spiked with XMuLV before the pH is adjusted. The XMuLV titre is measured in the spiked load and in the neutralized pool at the end of the hold." §5.3 adds: the LRF is "the reduction in log10 infectious virus between the spiked load and the neutralized pool".
- **What it says:** the runs are spiked before acidification, the LRF runs to the neutralized pool, and all outputs come from the spiked runs (Table 5.3).
- **What Version 1.0 said:** Version 1.0 §5.2 and §5.4 governed the executed designs.
  - The spike is "added to the pool after acidification and before the hold begins".
  - The input titre is taken "at the start of the hold" and the output titre "at the end of the hold".
  - Product quality comes from separate unspiked runs: "three samples ... from each spiked run and two from each unspiked run".
  - §1.1 lists no change.
- **The other sources:** the brief and the data are silent. The Version 1.0 report says "spiked into the load" and "held pool", so neither Version 1.0 document supports "neutralized pool".
- **Fix:** Describe the spiking as Version 1.0 planned it, or list the change in §1.1 with its reason. An amendment cannot change how runs that have already been made were spiked.

**6. §1.1: the list of changes is incomplete**

- **The text:** "This version is that amendment for Step 6, and it makes the following changes." Six items follow.
- **What is missing:** besides errors 1, 4 and 5, Version 2.0 makes two more changes.
  - (a) It states new model-adequacy tests (§7.1 item 2): predicted R² within 0.2 of R², regressions of the residuals on the predicted values and on run order, and Cook's distance at most 4/n. Version 1.0 §7.2 had only a significant regression, no significant lack of fit and residuals "with no structure". PCP-005 Version 2.0 lists the same addition as its change 4.
  - (b) It adds the hold study S-VI-HLD and the retention of its day 0, 3 and 7 samples (§6.5, Table 5.3, Table 11.1). No Version 1.0 document (PCP-006, PCR-006, PCMP-001) mentions a hold study, while change 5 lists only the hold criterion.
- **Fix:** Add (a) and (b) as numbered changes.

**7. Revision history, Version 2.0 row: "execution dates recorded"**

- **The text:** "... re-analysis of the studies, execution dates recorded; changes listed in the document (see INV-001)".
- **What it says:** this version records the execution dates of its studies.
- **What the document does instead:**
  - It gives no execution window for S-VI-SDM, S-VI-SCR, S-VI-RSM, S-VI-UNI or S-VI-HLD. Table 11.1 gives phases only.
  - The only study dates in the text are the first study start (2026-01-07, §1.1) and the re-test window (Table 5.2, note b).
  - The brief carries every window (study chronology). PCP-005 Version 2.0 records its windows in its Table 11.1 and lists that as its change 5 (INV-001 finding 5, PA3).
  - The same row also names INV-002, which the plan mentions nowhere else. That row text is common to every document (config `campaign.revisions`), so this part is by design.
- **Fix:** Add Start and End columns to Table 11.1 from `study_chronology.csv` for the six studies of this plan, and add the change to §1.1.

**8. §5.5, third paragraph: two of the four single-batch judgements**

- **The text:** "Such judgements are the PAR computed while the other factors vary as in routine operation (Section 8) and the judgement over the NOR in the qualification of the scale-down model (Section 5.1), ..."
- **What it says:** these are the judgements made on a single batch.
- **What the document says instead:** the plan makes two more single-batch judgements. The verification of the platform worst cases uses the one-sided 95 % prediction bound of a single batch (§7.4). The hold criterion uses the 95 % prediction limit of a single run (§7.5). PCMP-001 §6.2 counts the verification among its three.
- **Fix:** Add "the verification of the platform worst cases (Section 7.4) and the expected level of the hold criterion (Section 7.5)".

**9. Table 4.1, acidic charge variants row, "DS criterion" cell**

- **The cell:** "18–40 % (icIEF)".
- **What the source gives instead:** the table says it reproduces the register. The register gives "18–40 % (CEX/icIEF)" (`cqa_register.csv`, unit "% (CEX/icIEF)"; PCMP-001 Table 3.1). The other three rows match the register.
- **Fix:** Print "18–40 % (CEX/icIEF)".

**10. §7.3, first paragraph: "cannot be made up"**

- **The text:** "A shortfall at this step therefore cannot be made up by the claims of the other two steps."
- **What the numbers show instead:** the same paragraph gives the claims a sum of 16.72 against a requirement of 16.7. A shortfall of up to 0.02 log10 still leaves the requirement met, so only a larger shortfall cannot be made up.
- **Fix:** "A shortfall of more than 0.02 log10 at this step cannot be made up by the claims of the other two steps." Alternatively, use PCMP-001 §7.4's wording, "by the surplus of another step".

**11. Notes to Tables A.1 and B.1: "standard order"**

- **The text:** "Runs are listed in standard order."
- **What the tables show instead:** the factorial rows alternate factor C fastest and A slowest (run 1 −1 −1 −1, run 2 −1 −1 +1, run 5 +1 −1 −1). Standard (Yates) order in Montgomery (2017), which §5.5 cites, alternates A fastest. The order shown is that of the design file (`D.planned_matrix_df`).
- **Fix:** "Runs are listed in the order of the design file", or re-sort the factorial runs into Yates order.

## Checked and correct

- **Identity and dates:**
  - The title block, effective date 2026-09-30 and Version 1.0 approval on 2026-01-05, which falls before the first study on 2026-01-07.
  - The dates and classification of INV-001, the date of AMD-001 and the wording of CA2.
  - The Version 1.0 title-block date of 2026-07-24 and the commercial scale of 15,000 L.
- **Every before/after against `study_chronology.csv`:** qualification before screening, screening before the response-surface design, all three designed studies and the hold study before AMD-001, the re-test after it, and the phase order of Table 11.1.
- **Criteria:**
  - Table 1.1 and Table 7.1, cell by cell, against the brief's IAC and Version 1.0 tables and PCMP-001 Table 7.1.
  - The wider/stricter comparisons after Table 1.1, the derivation sentences of §7.2 and the cation exchange tightening (PCMP-001 §7.3 and §7.5).
  - Table 7.2 (0.70, 0.15, 1.00) and the upstream criteria each value feeds. Note a) agrees with A-Mab Table 4.16 (aggregate 1.8 % to 2.5 % over 180 min).
  - The XMuLV claims of 6.6, 5.5 and 4.62, summing to 16.72.
- **Parameters:**
  - Table 6.1 against `plan_params`.
  - The design centre (3.6, 120 min, 20 °C) and the statements about range versus NOR.
- **Report outcomes (owner's decisions of 2026-10-09):**
  - Notes a) to e) of Table 6.1 and the closing paragraph of §1.1 agree with the config's NOR and set-points in force: pH 3.4 and 3.3–3.5, hold time 110 min and 100–120 min, temperature 20–23 °C. The words "moved" and "narrowed" are right.
  - The draft gives no reason for the changes and says nothing about S-VI-WC, S-VI-OFAT or S-CEX-VER.
  - §12 risk 4 ("Replicate runs at set-point are made only in the qualification study") is true of the studies this plan governs. S-VI-OFAT later ran duplicates at pH 3.5, 90 min and 21 °C, so "under this plan" would make the scope explicit without saying anything only the report knows.
- **Designs and statistics:**
  - Screening: 11 runs with 3 centre points, 7 terms, and 4 residual degrees of freedom (2 pure error, 2 lack of fit).
  - Response surface: 18 runs with 4 centre points, 10 terms, and 8 residual degrees of freedom (3 pure error, 5 lack of fit).
  - The thresholds: Cook's distance 4/18 = 0.22 and the predicted-R² limit of 0.20.
  - The PAR settings: 81 grid points, 2,000 draws and a standard deviation of one sixth of the NOR width.
  - Appendices A and B match `D.planned_matrix_df`, coded and natural.
- **Studies:**
  - Qualification: 3 scale-down runs and 5 manufacturing batches, aggregate and acidic variants only, with a 90 % confidence interval (`sdm_qualification.csv`, `D.sdm_offset`).
  - Univariate study: 5 and 35 g/L in duplicate.
  - Hold study: the temperatures, the sampling days and nrCE-SDS on days 0, 3 and 7 (`hold_viral_inactivation.csv`).
  - The method-by-study statements and Table 5.2 (`method_plan.csv`, PCMP-001 §7.8).
- **Other tables and references:**
  - The CQA entries of Table 4.1 (score, criticality, step), the monotonicity statement and "critical" meaning high or very high (RA-001 §3).
  - The SOP and AMV numbers and titles (PCMP-001 Table 5.2), and the related-documents table.
  - §7.6 quotes PCMP-001 §7.7 verbatim.
- **Registered discrepancy:** D-001 (§8, the first PAR analysis at the set-points) is present as registered and is not counted as an error.

## Could not check

- **How the designed runs were spiked**, before or after acidification, and whether the quality samples came from spiked runs. The brief, the config and the CSVs say nothing on it, and the Version 1.0 plan and report differ (error 5).
- **The platform worst cases themselves.** The X-Mab, Y-Mab and Z-Mab history is recorded only as source strings in the config. The only one I could trace to a source is the aggregate value, to A-Mab Table 4.16.
- **The manufacturing-scale data set**, which PCMP-001 §7.1 asks each plan to name. The config gives only `n_manufacturing: 5` and no lot IDs, and lot IDs must not be invented.
- **RA-001's scores and rationale for the study-type assignments.** They are not in the brief, and I read RA-001 only for its definition of "critical".
- **Not a plan claim, but PCR-006 will need it:** the hold pool starts at 1.68 % and 1.71 % aggregate and 22.8 % and 22.3 % acidic variants on day 0. The set-point runs of S-VI-SDM sit at 1.91–1.96 % and 20.3–20.9 %. The difference is consistent with a different feed lot, but nothing in the brief or the data says which feed the hold study used.
