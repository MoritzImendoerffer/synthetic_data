# Factual check, run 2: PCR-005 Version 2.0 draft (Protein A chromatography)

Checked by Claude Opus 5.5 (model ID `claude-opus-5-5`) on 2026-10-09.

- **Document:** `PCR-005_protein_a.DRAFT.txt`, rendered 2026-10-09 09:21.
- **Fact sheet:** `authoring/out/PCR-005.brief.md`.
- **Method:**
  - **Reading:** I read the draft and the brief in full. Each number-bearing sentence, and each sentence whose deciding word depends on data, was checked against the table of the draft that holds its value and against the brief.
  - **Data and config:** I opened CSVs from `outputs/data/` only where the brief and the tables were silent or disagreed: `sdm_qualification`, `univariate_studies`, `hold_harvest`, `hold_protein_a` and the two Protein A designs. In `config/parameters.yaml` I read only the discrepancy register and the LOQ.
  - **Recomputation:** model-derived claims were recomputed with scratch scripts that call the engine read-only:
    - `doe_report`, `tables` and `_pcpkg`;
    - for the deletion analysis, `amab_process.adequacy.select_model`, reached through `D.ad`.
  - **Limits:** I read no other repository file and changed nothing in the repository. Other sessions edited the repository during the check (last note). Every value I recomputed still matched the draft.

## Status of the five errors of the first check

1. **Fixed.** The first check found fragments said to meet their criterion "in every run of the designs".
   - Section 6 now argues from the selected models, the Section 7.3 sentence is gone, and Section 12 item 3 is rewritten.
   - F5 and Section 5.3.3 limit "every run of both designs" to leached Protein A. F6 and Section 5.3.4 limit fragments to the 28 response-surface pools.
   - No sentence now claims a fragment result for the screening runs.
2. **Fixed.** The residual table showed the rejected step-yield model.
   - Table 5.12 now shows the selected models. Its step-yield row (0.758, 0.634, 0.25 at run 16, 2 runs) is the selected model A, C, D, AC, D², refitted.
   - The "smallest p" sentences are gone, and F8 cites Section 5.5.
3. **Fixed.** The reason why fragments carry no offset had ignored S-PA-SDM2. Section 3.1 now adds that the 6 runs of S-PA-SDM2 were made after AMD-001 and were not tested by nrCE-SDS either, and it gives no reason without a source.
4. **Fixed.** One design-space fraction had been computed on a coarser grid. Section 6 now states the grid, 41 points per factor, and every fraction in the section reproduces on it.
5. **Fixed.** Changes in percentage attributes had been given in "%". Section 5.7 and Table 5.16 now give them in percentage points ("points").
6. **Moot.** The probable error was the claim that the PARs are "the same" at the load NOR as characterized and as narrowed. The NOR is no longer narrowed, the config has no Version 2.0 NOR for this step, and the sentence is gone.

## Errors

**1. Section 13.3.2 narrows PD-005-02 to pool host cell protein, but the register entry covers every output with a criterion**
- **Sentences (Section 13.3.2):** "PD-005-02 records it for pool host cell protein, whose upper prediction limit over the NOR lies closest to its criterion. The same deletion was applied to leached Protein A and fragments."
- **What it says:** the discrepancy covers pool host cell protein. The deletion for the other two outputs lies outside it.
- **What the document says:**
  - Table 13.3 is the register: `discrepancy_register("PCR-005")`, config entry PD-005-02.
    - Under Done it records "an influence analysis for every output with a criterion".
    - Its Reason is that "no selected model meets the limit of the plan on influential runs".
  - Sections 3.5 and 5.5 record the whole influence analysis as PD-005-02, and Section 5.5 runs it for all 3 outputs with a criterion.
  - The sentence follows the older wording that the brief still carries (§4c: "Pool host cell protein conclusion resting on an influence analysis").
- **Fix:** write "PD-005-02 records it for every output with a criterion (Section 5.5). Pool host cell protein is the output whose upper prediction limit over the NOR lies closest to its criterion." Delete "The same deletion was applied to leached Protein A and fragments."

**2. Leached Protein A is said to meet criterion 2, a significant model, which a model with no term cannot meet**
- **Sentences:**
  - Section 5.3 first says: "Table 5.7 judges each selected model against criteria 2 to 4 of PCP-005 §7, a significant model, no significant lack of fit and a predicted R² within the limit of R²." It then says: "Each selected model meets the criteria."
  - Table 5.7, leached Protein A row: Model p is "n.a." and Met is "Yes". The footnote defines Met as "criteria 2 to 4 of PCP-005 §7 met".
  - Section 11: "Their selected models meet the adequacy criteria and support PARs over the whole range studied." Here "their" means leached Protein A and fragments.
- **What they say:** every selected model meets criteria 2 to 4, leached Protein A included. The Discussion says, without qualification, that both models meet "the adequacy criteria".
- **What the document says:**
  - Section 3.5 defines criterion 2 as "The model F-test is significant at α = 0.05", and notes that a model with no term has no F-test.
  - Two sentences after "Each selected model meets the criteria", Section 5.3 itself says: "Each is significant except the model of leached Protein A, which has no term and therefore no F-test."
  - No selected model meets criterion 5 (Section 5.5).
  - F2 and Section 12 item 3 already state it correctly: the criteria on lack of fit and predictive power are met, and each model with a term is significant.
- **Fix:**
  - In Table 5.7, mark criterion 2 as not applicable for leached Protein A, for example Met "Yes, 2 n.a.".
  - In Section 5.3, write "Each selected model meets criteria 3 and 4, and each model with a term meets criterion 2."
  - In Section 11, write "meet the adequacy criteria on lack of fit and predictive power".

**3. Section 7.3 says the design space excludes the corner of high load and low pH, but Section 6 includes it when the other two factors are at their set-points**
- **Sentence (Section 7.3):** "Pool host cell protein exceeds its criterion where protein load and elution buffer pH both lie near the edges of their ranges studied, outside both NORs, and the design space of Section 6 excludes that corner."
- **What it says:** the design space leaves out that corner.
- **What the document and the data say:**
  - Section 6 says: "With load flow rate and end of pool collect at their set-points, the whole region of protein load and elution buffer pH studied meets the criterion."
    - The excluded grid points occur "only where load flow rate or end of pool collect is away from its set-point".
    - At 50 g/L resin and pH 3.2, with the other two factors at their set-points, the median is 20,217 ng/mg. That is within the criterion of ≤ 21,662.
  - What exceeds the criterion at that corner is a single batch. With the other two factors at their set-points, the upper prediction limit of a single run there is 25,690 ng/mg at manufacturing scale. That is the `D.prediction_interval` result divided by the ratio 0.973.
- **Fix:** write "...outside both NORs. A single batch there can exceed the criterion even with load flow rate and end of pool collect at their set-points. On mean predictions the design space of Section 6 loses that corner only when one of the two is away from its set-point."

**4. The full quadratic model has "15 terms" and "14 terms" in the same section**
- **Sentences:**
  - Section 3.5: "PCP-005 §5.5 planned to fit the full quadratic model of 15 terms to each output..."
  - Section 3.5: "The full quadratic model keeps all 14 of its terms whatever the data support."
  - Section 5.3: "The selection kept 5 of the 14 terms of the full quadratic model..."
- **What they say:** 15 terms, then 14.
- **What the document says:**
  - Table 5.7 counts "the terms of the selected model besides the intercept", so a term there excludes the intercept.
  - On that count the full quadratic in 4 factors has 14 terms: 4 main effects, 6 interactions and 4 squares. It has 15 coefficients.
  - The 13 residual degrees of freedom in Section 4.3 (28 − 15) are right.
- **Fix:** write "the full quadratic model, an intercept and 14 terms".

**5. The executive summary calls the scale-down model qualified for each output it compares, including 3 outputs for which qualification does not apply**
- **Sentence (Executive summary, after F11):** "The proven acceptable ranges and the design space rest on the selected models and on a scale-down model qualified for each output that it compares at both scales."
- **What it says:** the model is qualified for every output it compares at both scales.
- **What the document says:**
  - Table 3.1 compares 5 outputs. It marks step yield, column efficiency and peak asymmetry "n.a." under Qualified, because they have no criterion.
  - Section 11 states it correctly: "qualified by its offset for the 2 outputs it compares that have a criterion."
  - A PAR also rests on fragments, which carry no offset. The model is accepted for them on mechanism (Section 3.1).
- **Fix:** write "...on a scale-down model qualified for pool host cell protein and leached Protein A, the 2 outputs with a criterion that it compares at both scales. Fragments carry no offset, and the model is accepted for them on mechanism (Section 3.1)."

## Probable error, not counted: needs one more check

**6. The anion exchange model is described on 28 runs, but INV-002 augmented that design to 40 runs**
- **Sentences (Section 7.1):**
  - "The anion exchange model, from the 28 runs of its design with 4 centre points, predicts a lowest clearance within its NOR of 5.51-fold."
  - "This model passes both tests as well, with a shortfall of predicted R² of 0.02 and a lack of fit test of p = 0.824."
  - "The models of the two steps are reported in PCR-007 and PCR-008."
- **What the data show:**
  - The quoted values match the verification table. `D.iac_verification()` gives a gap of 0.0242, a lack of fit p of 0.8239 and a bound of 5.18.
  - These are the statistics of the selected anion exchange model fitted to the 28 planned runs, `D.fit("aex", "rsm", "hcp_out_ng_mg", runs="planned")`.
  - INV-002 augmented the anion exchange design. `D.has_augmentation("aex")` is True: 40 runs, 12 of them in block 2.
  - The engine's model for that step, `D.fit("aex", "rsm", "hcp_out_ng_mg")`, uses all 40 runs with a block term.
    - Its terms are the same: load pH and wash 1 conductivity, on the log scale.
    - Its gap is 0.021 and its lack of fit p is 0.843.
    - PCR-008 will report this model, so its statistics will differ from those this sentence attributes to it.
  - The cation exchange design was not augmented: 28 runs, 4 centre points. That sentence is right.
- **Check:** confirm that the criteria are meant to rest on the planned runs of a downstream step. The brief says "the augmentation runs moved no criterion", which suggests they are.
  - **If they are:** write "fitted to the 28 runs of its planned design, before the 12 runs that INV-002 added".
  - **If they are not:** recompute the bound of 5.18-fold on all 40 runs. The 217-fold combined clearance and the criterion of ≤ 21,662 ng/mg would change with it.

## Notes (not errors)

- **The brief is stale on three points. Regenerate it.**
  - **PD-005-02 (§4c).** The brief carries the old wording, which is the source of error 1. `discrepancy_register("PCR-005")`, which reads the config, prints Table 13.3 row for row, including the new PD-005-02.
  - **The INV-002 table (§4c, `model_adequacy.csv`).** The two sources give different statistics for the planned full quadratic of pool host cell protein:

    | Source | Run 23 analysed at | R² | Predicted R² | Gap | Lack of fit p |
    |:--|:--|--:|--:|--:|--:|
    | Brief / INV-002 table | design pH 3.55 | 0.989 | 0.932 | 0.057 | 0.058 (adequate) |
    | Table 5.6 and Section 5.3 | recorded pH 3.38 | 0.98 | 0.89 | 0.09 | 0.024 |

    Both are right: refitted both ways, they differ only in the setting used for run 23. Section 5.3 states the run-23 basis only in the sentence after the table. Add it to the Table 5.6 footnote, because INV-002 prints the other numbers for the same planned model and calls it adequate.
  - **The SOP/AMV subset (§6).** It omits SOP-3015, AMV-3019, AMV-3020 and AMV-3013, which the report cites. All four titles are now in the controlled-document register (`all_sop_table()`). That includes AMV-3013 "Charge Variants (icIEF)", which had no source at the first check.
- **Rounding only, not counted:**
  - **The aggregate bound of low-pH viral inactivation.**
    - The criterion uses 0.534997 (`D.iac_table()`). The verification table stores it as 0.5350 and prints 0.54, so Table 7.1 and Sections 4.5 and 7.1 show 0.54 where correct rounding gives 0.53.
    - Section 4.5's own arithmetic, 5 % × 1.52 − 0.54, gives 7.06, not the stated 7.04. The criterion itself is right: 5 × 1.5152 − 0.5350 = 7.041.
    - Either give 1.515 and 0.535 in Section 4.5, or add the "computed from unrounded values" caveat of Table 7.1.
  - **The hold changes.** They are taken from the rounded table values, as the Table 5.16 footnote says.
    - Unrounded, the aggregate rise at 21 °C is 0.457: 0.46, not 0.45.
    - The day-0 aggregate difference is 0.086: 0.09, not 0.08.
    - No conclusion changes. Unrounded, the two fragment rises still differ by less (0.094) than the day-0 aliquots do (0.099).
  - **"The coefficients ... change by at most 3 %".** The largest change is 3.12 %, for protein load with run 6 deleted.
  - **F7's limits of 44 g/L resin and pH 3.27.** These are values of the 41-point grid. On the continuous model the boundary lies at about 43.7 g/L resin and pH 3.28. Section 6 names the grid, but F7 does not.
- **Wording that sits uneasily with the data, not counted:**
  - **Load flow rate in Section 9.** The section says it has "a curvature ... too small to move pool host cell protein appreciably against its criterion".
    - Within the NOR that holds: the curvature changes pool host cell protein by at most 4 %.
    - At either end of the flow range, with end of pool collect at its set-point, the median at 50 g/L resin and pH 3.2 exceeds ≤ 21,662. It is 21,743 ng/mg at 300 cm/hr and 22,957 ng/mg at 100 cm/hr.
    - Section 6 likewise finds excluded points only where flow rate or end of pool collect is away from its set-point.
    - The KPP class still follows criterion 8, because the NOR-propagated PAR spans the range studied.
  - **Section 5.2 on the BD and CD interactions on yield.** It calls them "smaller than the main effects". BD (−0.98) is larger than the main effect of B (−0.24). The sentence means the significant main effects.
  - **The PD-005-01 reason in the register.** "The output that sets the ranges of the step" reads oddly now that every PAR spans the range studied. Section 13.3.1 gives a reason that fits the data better: the output "closest to its criterion".
  - **"Every output" in F8 and Section 12 item 5.** The influence analysis and the criteria apply only to the 3 outputs with a criterion, not to step yield.
  - **The revision history.** `revision_history("PCR-005")` describes Version 2.0 as "Re-analysis under INV-001" and omits the INV-002 CA3 model selection and the run-23 analysis. Section 1.4 lists those as changes 1 and 2. The text comes from the helper or the config.
  - **`D.governing_factor`.** It returns load for fragments and for leached Protein A. The draft is right here, not the helper:
    - In the selected fragment model, elution buffer pH has the larger effect (−0.054 against −0.028, Table 5.11), and that is the parameter Figure 7.2 shows.
    - The leached Protein A model has no term.
- **Cannot be checked from the permitted sources:**
  - **PCP-005 and PCMP-001 references.** These are the § numbers and the texts of PCP-005 criteria 1 to 8.
    - "PCP-005 §8.1" in Section 7.1 still looks off. The report cites PCP-005 §7 for every other criterion, and in the canonical plan outline §8 is Data management.
  - **INV-001 findings.** The finding numbers 1, 2, 4, 5 and 6.
  - **S-PA-RET.** The draft says "PCP-005 Version 2.0 includes it".
    - S-PA-RET ran in April 2026, under PCP-005 Version 1.0.
    - By Section 13's own definition of a discrepancy, it is not one only if the reference plan is Version 2.0.
    - Version 2.0 is also the reference under which S-PA-SDM2 counts as PD-005-01.
  - **Statements about the studies themselves:**
    - the screening pools "were not retained";
    - the offset "was measured on the same laboratory columns as the designs";
    - the S-PA-SDM2 runs used "the same procedures as the planned runs".
  - **Attributions to the A-Mab case study:**
    - pool host cell protein rising with load;
    - no parameter with a significant effect on aggregate;
    - a batch at the boundary of a region defined on mean predictions meeting the criterion "about half the time".
  - **PCR-003.** Its acceptance of the acidic-variant corner, with alarm limits.
- **Verified correct, apart from items 1 to 6:**
  - **Tables:**
    - Against the engine or the CSVs: every value of Tables 2.1, 3.1, 5.1 to 5.14, 7.1 (apart from the rounding note), 7.2, 7.3, 8.1, 13.2, 13.4, A.1, B.1 and C.1.
    - Against the register: Table 13.3.
    - Against the brief: Tables 1.2, 3.3, 4.1, 4.3 and 5.15.
  - **Refitted or recomputed: models and statistics.**
    - The selected models and their Box-Cox intervals: −0.32 to 0.42 for pool host cell protein. The intervals of the other 3 outputs contain 1.
    - The raw full quadratic of pool host cell protein fails lack of fit (p = 0.024).
    - The interaction of protein load with elution buffer pH:
      - p = 0.156 on the log scale and p < 0.001 on the raw scale;
      - p < 0.001 in the Version 1.0 model;
      - p = 0.156, 0.069 and 0.081 for the three analyses of run 23;
      - p = 0.064 and 0.071 in the two selected models that keep the term, so "not significant in any of these analyses" holds.
    - The factors 2.43 and 3.30, and the changes of 15 %, 8 %, 14 % and 4 %.
    - 14,081 and 5,804 ng/mg.
    - The medians 7,150, 20,217, 11,522, 10,368 and 7,761 ng/mg, and the range over the NOR of 4,259 to 12,474 ng/mg.
    - The F11 ratio test: a factor of 1.22, p = 0.021.
    - Table 5.12, the drift of 0.84 ppm, the level of 0.0071 and "11 times".
    - The deletion analysis:
      - upper prediction limits of 15,308 to 15,554 ng/mg, and 16,987 ng/mg with the offset at the low end;
      - AB and A² added when run 23 is excluded;
      - the leached Protein A and fragment limits still met after deletion.
  - **Refitted or recomputed: design space and qualification.**
    - The design-space fractions on the 41-point grid:
      - 100 % with the other two factors at set-point;
      - 99.9 to 100.0 % at the corners of their NORs;
      - 98.8 to 100.0 % at the corners of their ranges studied;
      - 99.9 % over all 4 factors.
    - The excluded points at 44 g/L resin and above with pH 3.27 and below, and only where load flow rate or end of pool collect is away from its set-point.
    - The qualification limits of 15,697, 17,143, 14,374 and 19,212 ng/mg, and the half-width 46 % narrower.
    - The leached Protein A limit of 5.52 ppm.
    - The fragment limit of 1.09 %, plus 0.45 points from `hold_harvest.csv`, giving 1.54 %.
    - Each scale-down leached Protein A run below the manufacturing mean of 3.70 ppm (highest 3.66).
  - **Refitted or recomputed: measured results.**
    - The counts against the drug substance criteria: 47 of 47, 4 of 47 and 0 of 28.
    - The 3 results above 21,662 ng/mg, at 21,825 to 25,800 ng/mg.
    - Leached Protein A from 1.70 to 4.61 ppm, the highest result of 5.79 ppm, the mean of 2.94 and 4.12 ppm, the SD of 0.67 ppm and the re-assay of 3.30 ppm.
    - SEC minus nrCE-SDS of 0.12 to 1.37 points, median 0.36.
    - Aggregate from 1.40 to 1.73 % across 47 pools.
    - DNA in the load from 137,045 to 234,778 pg/mg and in the pool from 498 to 1,372 pg/mg, a reduction of 2.2 to 2.5 log10.
    - The Table 5.13 intervals, and the highest univariate results of 10,488 ng/mg and 5.38 ppm.
    - The sums of Table 5.16.
  - **Refitted or recomputed: other steps and capability.**
    - The bioreactor values of 2.35, 30.3 and 16.2 %, the corner (pH 6.95, 34.5 °C, 18 days, 130 mmHg) and its median of 18.4 %.
    - Table 7.1 against `D.iac_verification()`.
    - The criteria 21,662, 158, 2.45, 7.04 and 18–39.6 against `D.iac_table()`, and that no criterion upstream of this step uses a Protein A platform value.
    - The capability values:
      - Cpk 6.14, 10.66 and 10.81;
      - 1.05 is the lowest Cpk in the register;
      - 1 acidic-variant batch in 2,000, 856 per million;
      - none for the other attributes, below 0.15 %.
  - **Config and engine values:**
    - 15,000 L and 2,000 simulated batches;
    - the PAR Monte Carlo: 81 grid points, 2,000 draws, N(set-point, NOR/6), clipped;
    - PCP-005 approved on 2025-11-03;
    - Cpk target 1.33 and minimum 1.00;
    - the LOQ of 0.25 ppm (AMV-3016);
    - AMD-001 on 2026-03-20;
    - the INV-001 dates and classification;
    - the NORs unchanged.
- **Dates are in order:**
  - PCP-005 was approved on 2025-11-03, before the first study started on 2025-11-05.
  - AMD-001 (2026-03-20) followed the close of S-PA-SDM, S-PA-SCR, S-PA-UNI, S-PA-RSM and S-PA-HLD, and preceded S-PA-RET (2026-04-06).
  - S-PA-SDM2 (2026-09-07 to 2026-09-11) ran while INV-001 was open (2026-08-03 to 2026-09-18).
  - CA3 was adopted on 2026-09-15, before INV-001 closed.
  - The last study ended before the effective date of 2026-09-30.
- **The repository changed during the check.** Other sessions edited it while I worked:
  - `amab_process/adequacy.py` and `pc_package/doe_report.py` changed at 09:27, after the draft was rendered at 09:21.
  - At 09:32 to 09:33 these changed:
    - `config/parameters.yaml`, `pc_package/tables.py` and `pc_package/_pcpkg.py`;
    - the PCMP-001 files, `authoring/STORY_BIBLE.md` and `authoring/check_render.py`.
  - New PCP-003 and PCP-006 drafts appeared.
  - My scripts ran from 09:30 to 09:41, against that changing state. Every value they recomputed matches the draft, so the draft is current for the engine as of 09:41.
  - I wrote only to the scratchpad. The only trace my imports can leave in the repository is Python's untracked bytecode cache in `pc_package/__pycache__/`.

## Tally

- **Sentences checked:** about 660 sentences carry a number or a deciding word, in the prose from the Executive summary to Section 13.
  - About 375 of them carry a quantity or a date, not just an identifier or a cross-reference.
  - The counts come from an automated split, which also picks up some table fragments.
  - Every table value that the prose quotes was cross-checked as well.
- **Errors:** 5.
  - Errors 1 to 3 change what a reader takes away: the scope of a registered discrepancy, an adequacy criterion said to be met, and the design-space corner.
  - Errors 4 and 5 are a count and a wording fix.
- **Probable error, not counted:** 1 (item 6).
- **Earlier check:** all 5 errors of the first check are fixed, and its probable error is moot.
