# Factual check: PCR-005 Version 2.0 draft (Protein A chromatography)

Checked by Claude Opus 5.5 (model ID `claude-opus-5-5`) on 2026-10-08.

- **Document:** `PCR-005_protein_a.DRAFT.txt`
- **Fact sheet:** `authoring/out/PCR-005.brief.md`
- **Method:** I read the draft and the brief in full. Each number-bearing sentence was checked against the table that holds its value and against the brief. I opened `outputs/data/*.csv` and `config/parameters.yaml` only where the brief and the tables were silent or disagreed. Some model-derived claims were refitted from the Appendix data with a scratch script. I read no other repository file and ran no repository code.

## Errors

**1. Fragments are said to have met their criterion "in every run of the designs"** (the same error in three sentences)
- **Sentences:**
  - Section 6: "Leached Protein A and fragments met their criteria in every run of the designs, and step yield has no criterion, so they do not constrain it."
  - Section 7.3: "Every run of the designs met these criteria at every corner of the range studied, so neither output constrains any parameter within it."
  - Section 12, item 3: "Leached Protein A and fragments met their criteria in every run, and no adequate model results for either."
- **What it says:** fragments by nrCE-SDS met ≤ 2.45 % in every run of both designs (47 runs).
- **What the document says:** fragments by nrCE-SDS exist only for the 28 response-surface pools. The 19 screening pools have no nrCE-SDS result. See the Appendix A note ("Not tested in this design: LMW by nrCE-SDS"), Table 3.3, and brief §4c ("Fragment method by study": S-PA-SCR `lmw_cesds` False). F6 and Section 5.3.4 state this correctly ("All 28 response-surface pools").
- **Fix:** "Leached Protein A met its criterion in every run of both designs, and fragments in every one of the 28 response-surface pools."

**2. Table 5.9 reports the rejected step-yield model, so F4 and two Section 5.5 values rest on the wrong row**
- **Sentences:**
  - F4: "Like every model of the study, it does not meet the limit on influential runs (Section 5.3)." Here "it" is the reduced step-yield model.
  - Section 5.5: "No model shows a slope of the absolute residuals on the predicted values (the smallest p is 0.562)."
  - Section 5.5: "...(the smallest p is 0.310)..."
- **What it says:** the reduced model fails criterion 5. Across the models, the smallest trend p is 0.562 against the predicted values and 0.310 against run order.
- **What the table and data say:** Table 5.9's "Step yield" row (0.562, 0.310, max D 0.38 at run 12, 6 runs above 4/n) is the full quadratic model that Section 5.3 and Table 5.6 rejected. No table shows the reduced model (A, C, D, AC). Refitted from the Appendix B data, it has:
  - trend p of 0.519 against the predicted values and 0.743 against run order;
  - a largest Cook's distance of 0.22, at run 15;
  - 2 runs above 4/n (runs 15 and 16).

  F4 is therefore true, but nothing in the document supports it. With the model actually used, the smallest p values become 0.519 and 0.340.
- **Fix:** Show the reduced model in Table 5.9's step-yield row (0.519, 0.743, 0.22, run 15, 2), update the two "smallest p" values to match, and cite Section 5.5 in F4.

**3. The reason why fragments have no offset ignores the supplementary runs**
- **Sentence (Section 3.1):** "Fragments by nrCE-SDS were not part of the qualification, because the method decision AMD-001 was taken after study S-PA-SDM had closed."
- **What it says:** the qualification ran before AMD-001.
- **What the brief says:** AMD-001 is dated 2026-03-20 (§4c). The qualification also includes S-PA-SDM2, run 2026-09-07 to 2026-09-11, which is after AMD-001. The method plan records no nrCE-SDS for S-PA-SDM2 (§4c, "Fragment method by study"). The stated reason therefore covers only 3 of the 9 runs.
- **Fix:** Add that the 6 supplementary runs of S-PA-SDM2, made after AMD-001, did not test fragments by nrCE-SDS either. Give the reason only if a source states it.

**4. One design-space fraction is computed on a coarser grid than the rest of its paragraph**
- **Sentence (Section 6):** "Over the whole range studied of all 4 factors, 93.5 % of the design region meets the criterion."
- **What it says:** 93.5 %.
- **What the data say** (Table 5.7 model refitted from the Appendix B data, offset −251 ng/mg, criterion 16,379 ng/mg):
  - Every other value in this paragraph matches a grid of 41 points per factor exactly. These are 96.3 %, 92.6 to 98.3 %, 94.2 %, 97.9 %, "pH 3.32 and below" and "37 g/L resin".
  - 93.5 % matches only an 11-point grid. On that grid the set-point slice would be 95.0 %, not 96.3 %.
  - On the 41-point grid the four-factor fraction is 95.1 %. In the continuous limit it is about 95.7 %.

  Comparing 96.3 % with 93.5 % overstates how much the full ranges of flow rate and end of pool collect cost.
- **Fix:** Compute every fraction on one grid and state the grid, for example "95.1 %" on 41 points per factor.

**5. Changes in a percentage attribute are given in "%" in Section 5.7 but in percentage points elsewhere**
- **Sentences (Section 5.7):**
  - "Aggregate rose by 0.46 % at 21 °C against 0.07 % at 2-8 °C."
  - "Fragments by nrCE-SDS rose from 0.86 to 1.08 % at 2-8 °C and from 0.76 to 1.08 % at 21 °C, rises of 0.22 and 0.31 %."
  - The same applies to the day-0 differences, to the 0.1 % and 0.4 % acidic-variant figures, and to the "Largest increase" column of Table 5.13.
- **What it says:** the increases are given in %, which reads as a relative change. The relative rise in aggregate is in fact about 30 %.
- **What the document says elsewhere:** the same kind of quantity, the largest increase of a size variant, is in "points" in Table 7.1 ("Increase, largest (points)"). In Section 7.1 the fragment increase over low-pH viral inactivation is "0.13 percentage points". Sections 3.1, 3.3, 5.2 and 5.6 also give differences in percentage points.
- **Fix:** Write the changes in Section 5.7, and the increase column of Table 5.13, in percentage points.

## Probable error, not counted: needs one helper run to confirm

**6. The PAR is said to be unchanged by narrowing the load NOR**
- **Sentence (Section 7.3):** "The PARs are the same at the protein load NOR as characterized and as narrowed."
- **What the brief says:** §4b gives the PARs only at the NOR in force, 20–38 g/L resin. Nothing in the document or the brief supports the claim for 20–40.
- **What an approximate re-simulation shows:**
  - The re-simulation varies the other factors uniformly within their NOR, draws coefficients and residuals, takes the 95th percentile, and uses an 81-point pH grid.
  - For elution buffer pH (pool host cell protein) at 20–38 it gives 3.24 to 3.25 across random seeds. The brief has 3.25.
  - At 20–40 it gives 3.26 to 3.27 across the same seeds. The wider NOR raises the upper tail, so the boundary can only move up.
- **Fix:** Run `D.par_table` with the load NOR at [20, 40]. If the pH PAR moves, state both values instead of "the same".

## Notes (not errors)

- **The brief is stale on two points.**
  - Brief §4c lists only PD-005-01. `config` `campaign.plan_discrepancies` also registers PD-005-02, with the subject, planned, done and reason that Section 13 prints, so the report is right. Regenerate the brief.
  - The brief's SOP/AMV subset (§6) omits SOP-3015, AMV-3019, AMV-3020 and AMV-3013, which the report cites. The first three are in the config. AMV-3013 appears in the config only as the icIEF method inside DEV-008-01, so its title "Charge Variants (icIEF)" has no source in the brief or the config.
- **Cannot be checked from the permitted sources:**
  - The bioreactor-model limits used in the hold assessment: 2.20 % aggregate, 29.9 % acidic variants (upper) and 14.7 % (lower). They come from the PCR-003 model.
  - The INV-001 finding numbers 1, 2, 4, 5 and 6. They are numbered in STORY_BIBLE §9b, which I was not to open.
  - All § numbers cited in PCMP-001 and PCP-005, and PCP-005 criteria 1 to 8.
  - One reference looks off. Section 7.1 cites "PCP-005 §8.1" for the application of the intermediate criteria, but the report cites PCP-005 §7 for every other criterion, and in the canonical plan outline §8 is Data management. Check it.
- **Rounding-only differences, not counted:**
  - 33.84 % (Table 5.1) against "34 %" (Section 5.3.3).
  - 40.9, 43.6 and 30.3 (Table 7.1) against 40.95, 43.62 and 30.34 (Section 7.1).
  - "0.10 %" and "0.099 %" for the same day-0 fragment difference (0.0994) in adjacent sentences of Section 5.7. Use one precision there, because the "smaller than" comparison (0.0945 against 0.0994) rests on the third decimal.
- **Verified correct, apart from items 1 to 6:**
  - **Findings and sections:** findings F1 to F11 and every other quoted value in Sections 1.4, 2.2, 2.3, 3.1, 3.5, 4, 5.1 to 5.7, 6, 7, 8, 9, 11, 12 and 13.
  - **Refitted from data:**
    - offsets and confidence intervals (Tables 3.1 and 13.3, including the 678 against 1,249 half-widths, 46 % narrower);
    - prediction limits of 15,384, 16,062, 16,550 and 16,932 ng/mg;
    - influence range 15,023 to 15,417 ng/mg and coefficient changes within 4 %;
    - the 8 runs exceeding the criterion, at 16,820 to 25,366 ng/mg;
    - DEV-005-01 values 12,212, 8,853, 8,418, −434 ng/mg and a Cook's distance of 0.03;
    - the 2,819 ng/mg difference with p = 0.020;
    - the SEC minus nrCE-SDS difference of 0.12 to 1.37 points, median 0.36;
    - aggregate 1.40 to 1.73 % over 47 pools;
    - DNA results for the 7 centre points, with a 2.2 to 2.5 log10 reduction;
    - Table 7.2;
    - Cpk values and no out-of-specification batches among 2,000.
  - **Config values:** 15,000 L, NOR 20–40 to 20–38, PCP-005 approval on 2025-11-03, Cpk target 1.33 and minimum 1.00, LOQ 0.25 ppm, LOT-BUF-5290 on run 23, and the criteria 6.64 % and 18–39.6 %.
- **Dates are in order:**
  - PCP-005 was approved on 2025-11-03, before the first study started on 2025-11-05.
  - The last study ended on 2026-09-11, before the effective date of 2026-09-30.
  - S-PA-SDM2 (2026-09-07) followed Version 1.0 (2026-07-24) and ran while INV-001 was open (2026-08-03 to 2026-09-18).
  - AMD-001 (2026-03-20) preceded S-PA-RET (2026-04-06).

## Tally

- **Sentences checked:** about 570 number-bearing or deciding-word sentences in the prose from the Executive summary to Section 13, of which about 445 carry a number or an identifier. The count comes from an automated sentence split. Every table value that the prose quotes was cross-checked as well.
- **Errors:** 5. Error 1 occurs in three sentences, and error 2 affects F4 and two Section 5.5 values.
- **Probable error, not counted:** 1 (item 6).
