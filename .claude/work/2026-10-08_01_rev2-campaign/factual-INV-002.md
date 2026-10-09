# Factual check: INV-002 Version 1.0 draft (run 3)

- **Checker:** Claude Opus 5.5 (`claude-opus-5-5`)
- **Date:** 2026-10-09
- **Document:** `.claude/work/2026-10-08_01_rev2-campaign/INV-002_model_adequacy.DRAFT.run3.txt`, the text of
  `pc_package/INV-002_model_adequacy.DRAFT.pdf` (54 pp). Page 47 was rendered as an image to read Table 9.2.
- **Method:**
  - I checked every sentence that carries a number, and every sentence whose deciding word depends on the
    data. Each was checked against the document's own table and the brief (`authoring/out/INV-002.brief.md`).
  - I recomputed the statistics read-only with scratch scripts (`s1.py` to `s11.py` in the session scratchpad).
    They use `doe_report`, `tables`, `_pcpkg` and `amab_process.adequacy` and were run with `uv run python`.
  - Statements about other documents were checked against the rendered PCMP-001 and INV-001
    (`pdftotext -layout`).
  - For two findings I also read the rendered Version 1.0 documents in `pc_package/superseded/rev1/` and the
    rendered `PCR-005_protein_a.DRAFT.pdf`.
  - I read no `.qmd` file and nothing under `authoring/rhetorical/` or `authoring/history/`.

## Errors

1. **The document gives the model-adequacy criteria of PCMP-001 §7.2 as three tests. The master plan has four.**
   - **Where:** Section 3: "The process characterization master plan judges a response-surface model by three
     tests (PCMP-001 §7.2)." The same three-test definition recurs in the Summary, §1, §5, §6.1, §8.1 step 3,
     §8.4, §8.5.1, §9, §11, §12 and in the notes to Tables 2.1, 3.1 and 8.1: "a significant model F-test
     (α = 0.05), no significant lack of fit (α = 0.05) and R² minus predicted R² of at most 0.20".
   - **What it says:** the criteria are these three tests, and a model that passes them is "adequate". The
     verdicts in Tables 3.1, 8.1 and 9.1 are built on that.
   - **What the sources say:**
     - Rendered PCMP-001 §7.2 lists a fourth criterion: "4. The residuals show no pattern against predicted
       values or run order, and no single run dominates the fit."
     - Rendered PCP-005 §7: "Criteria 2 to 5 are the model adequacy criteria of PCMP-001."
     - The PCR-005 draft records that "Criterion 5 of PCP-005 §7, on influential runs and residual trends, is
       not met" (finding F8, §5.5: "criterion 5 is not met for any output"). It handles this through the
       influence analysis of PD-005-02 (`discrepancy_register("PCR-005")`).
     - INV-002 nevertheless calls the three selected Protein A models "adequate": host cell protein, leached
       Protein A and fragments (Table 8.1, Table 9.1, §8.5).
   - **Fix:**
     - State that §7.2 has four criteria, and that the verdicts of this investigation apply the three tests
       (criteria 1 to 3).
     - State that criterion 4, the residual and influence check, is judged in each step report. Name PCR-005,
       where no selected model meets it (PD-005-02).

2. **Table 3.1 and the statement that no model fails the lack-of-fit test use Protein A run 23 at its design pH.
   The rest of the Version 2.0 analysis uses the pH recorded for that run, and on that pH the full quadratic
   model of pool host cell protein fails the lack-of-fit test.**
   - **Where:**
     - Table 3.1, Protein A host cell protein row: "0.99 | 0.93 | 0.06 | 0.058 | <0.001 | adequate".
     - Summary: "No model showed significant lack of fit."
     - §3: "No model fails the lack-of-fit test".
     - §8.2: the residual comparison of "the full quadratic model of pool host cell protein".
   - **What it says:** the full quadratic model of pool host cell protein meets all three tests, with a
     lack-of-fit p-value of 0.058.
   - **What the data say:**
     - The PCR-005 analysis puts run 23 at its recorded elution buffer pH (PD-005-03, DEV-005-01). So does
       `doe_report`, through `rsm_data(corrected=True)`, which is the default.
     - On that pH the same model has R² 0.979, predicted R² 0.894, a difference of 0.085 and a lack-of-fit p of
       **0.024**, which fails.
     - The PCR-005 draft (§5.3) says this explicitly: "with run 23 at its recorded pH, fails the lack of fit
       test (p = 0.024). With run 23 at its design pH, as Version 1.0 and INV-002 fitted it, … p = 0.058".
     - `model_adequacy.csv` and the brief use the design pH.
     - INV-002 mixes the two readings without saying so. Table 3.1 uses the design pH. §8.2 uses the recorded
       pH: the residual SDs of 638 and 947 ng/mg, the Box-Cox λ of 0.06 (−0.32 to 0.42) and the log-scale
       interaction p of 0.156 are all values for the recorded pH. At the design pH they would be 541 and 669
       ng/mg, λ 0.25 (−0.07 to 0.53) and p = 0.069.
     - The selected models in Table 8.1 also use the recorded pH.
   - **Fix:**
     - Say in §3 and in the note to Table 3.1 that the re-analysis fitted run 23 at its design pH.
     - Say that at the recorded pH (DEV-005-01) the full quadratic model of pool host cell protein fails the
       lack-of-fit test (p = 0.024).
     - Qualify "No model showed significant lack of fit" accordingly, and say in §8.2 which reading it uses.
     - Whether the count becomes 15 failing models is for the owner to decide.

3. **The footnote marks in Table 9.2 are swapped.** (§9.1, Table 9.2, checked on the page image)
   - **What it says:**
     - Mark a) is on the selected-model value of acidic variants ("1.00a)"), but footnote a) is about host cell
       protein at anion exchange.
     - Mark b) is on the full-quadratic values of host cell protein at anion exchange ("4.00b)", twice), but
       footnote b) is about acidic variants at low-pH viral inactivation.
   - **What the table needs:** each mark must point to its own explanation. The values themselves are correct
     (brief, `iac_verification_full.csv`).
   - **Fix:** exchange the two footnote texts, or the two marks.

4. **The document says the Version 1.0 reports applied no adequacy test and the Version 1.0 plans set no
   adequacy criterion. Both statements are wrong.**
   - **Where:**
     - §1: "The Version 1.0 reports fitted the full quadratic model to every response-surface design and
       applied no adequacy test."
     - Summary and §12: "The Version 1.0 plans also set no adequacy criterion against which the size of a design
       could have been checked."
   - **What the Version 1.0 documents say** (in `pc_package/superseded/rev1/`):
     - The Version 1.0 PCR-003 "assessed [model adequacy] on four grounds", including the lack-of-fit test. It
       reports "No response shows significant lack of fit" (Table 5.8, acidic variants lack of fit p = 0.147).
     - The Version 1.0 PCMP-001 accepts a model "when its terms are significant at α = 0.05, when the lack of fit
       is not significant against pure error, and when the predicted coefficient of determination is consistent
       with the adjusted coefficient". It leaves only the numeric thresholds to each study.
     - The Version 1.0 PCP-003 sets the lack-of-fit test, predicted R² tracking adjusted R², and residual
       diagnostics, with "No numeric threshold for the coefficient of determination".
     - §4 states this correctly: "left the model-adequacy threshold to the individual study, and the Version 1.0
       plans set none."
   - **Fix:**
     - §1: "…and applied the lack-of-fit test but no numeric limit on R² minus predicted R²".
     - Summary and §12: "set no numeric limit on overfitting against which…".

5. **AICc is defined in one convention in §8.3 and reported in another.**
   - **Where:** §8.3.
     - The definition: "The fit term is n·ln(SSE/n) … The penalty is 2K, where K counts … the coefficients and
       the residual variance … A constant that is the same for every candidate is left out."
     - The values reported: host cell protein at cation exchange "AICc of −31.2 … (−27.4) … (−27.9)". In §8.5.2,
       XMuLV at virus filtration "−7.8 against −6.8".
   - **What the code does:** `adequacy.aicc` uses the statsmodels AIC.
     - That includes the constant n(1 + ln 2π).
     - Its penalty counts the coefficients only, 2(K − 1).
     - The reported values are therefore the document's AICc plus n(1 + ln 2π) − 2.
     - Example: on the document's own fit terms (§8.3), the selected model of Protein A host cell protein has
       AICc −132.8 + 14 + 5.6 = −113.2. The code gives −35.8.
     - Every difference the document gives (46.1, 1.0) is unaffected.
   - **Fix:** say that the AICc values reported include a constant common to all candidates of an output. Or
     report differences only.

6. **INV-001 is quoted as comparing criteria with the Version 1.0 models. It compares ranges.**
   - **Where:** §9.3 item 1: "Its comparison of the Version 1.0 and Version 2.0 criteria uses the models that
     Version 1.0 fitted, so that it shows what the change of criteria moved."
   - **What INV-001 says** (§2, rendered): "Every comparison of ranges in this report uses the models
     Version 1.0 fitted, so that it shows what the change of criteria moved." The criteria themselves rest on
     the selected models (INV-001 §2 and §6.2).
   - **Fix:** "Its comparison of the proven acceptable ranges of Version 1.0 and Version 2.0 uses the models that
     Version 1.0 fitted".

7. **The worked interval in §8.2 does not say which NOR it uses.** (minor)
   - **Where:** §8.2 item 5: "At the least favourable combination of the NOR (protein load 39 g/L resin, …)".
   - **What the data say:**
     - 39 g/L resin is the upper end of the NOR in force (`nor_v2` [20, 39]).
     - The NOR as characterized, which PCMP-001 lists, runs to 40 g/L resin.
     - §2 defines both terms "throughout". The values given (9,698 to 15,349 ng/mg) are correct for the NOR in
       force.
   - **Fix:** "At the least favourable combination of the NOR in force".

8. **The title of SOP-1002 is mangled.** (minor)
   - **Where:** §10: "PA2 revises SOP-1002, the procedure for the design, Execution and Statistical Analysis of
     DoE Studies".
   - **The registered title** (`_pcpkg` SOP list) is "Design, Execution and Statistical Analysis of DoE Studies".
   - **Fix:** "SOP-1002, Design, Execution and Statistical Analysis of DoE Studies, so that…".

9. **Table 10.1 does not reproduce the CAPA record verbatim.** (minor, only if the table is meant to quote the
   record)
   - **Where:** Table 10.1, PA1.
   - **What it says:** "…for a probability of success of at least 0.90…".
   - **The record** (`campaign.investigation_2.capa`, the brief) reads "…for an assurance of at least 0.90…".
     The meaning is the same.
   - **Fix:** quote the record. Alternatively, say once that the document calls "assurance" the probability of
     success.

## Checked and correct

- **Dates and chronology**
  - Opened 2026-08-31 and closed 2026-09-28.
  - INV-001 opened 2026-08-03 and closed 2026-09-18.
  - Rule, sample sizes and designs approved 2026-09-02. Model selection and the root cause dated 2026-09-15.
  - S-BRX-AUG ran 2026-09-03 to 2026-09-24 and S-AEX-AUG 2026-09-10 to 2026-09-24. The last planned
    response-surface study, S-VF-RSM, ended 2026-05-15.
  - "both augmentations were under way on 2026-09-15" is correct.
  - Classification is minor, with its basis as in the config.
- **CAPA** (Table 10.1, §10 and §12): owners, due dates and statuses as in the config (`CAPA2`). Effectiveness
  check due 2027-06-30, with its criterion.
- **Table 2.1:** runs and terms per step (28/15, 18/10, 12/6), the 22 outputs, and the failing set.
- **Table 3.1 and §3**, apart from error 2:
  - Every R², predicted R², difference, lack-of-fit p and F-test p agrees with `model_adequacy.csv`.
  - 14 of 22 fail. Differences run from 0.26 to 2.14. The lowest lack-of-fit p among failing models is 0.096.
  - 5 models fail the F-test, with p from 0.280 to 0.936.
  - The groups split 10 + 4, with R² from 0.60 to 0.95 and from 0.27 to 0.57. The lowest predicted R² is −1.83.
  - Fragments: an effect is kept at Protein A, low-pH viral inactivation and cation exchange, and none at anion
    exchange and virus filtration.
  - The exact fit of low-pH acidic variants is counted among the 8 that passed.
- **§4 root cause**
  - Average leverage 0.50 to 0.56. Leverage range 0.12 to 0.79. Expected PRESS factor 5.2 to 7.0, so 4.2 to 6.0.
  - Break-even R² 0.95 to 0.97. Every model that passed has R² ≥ 0.96, and every failing model has R² ≤ 0.95.
  - Probabilities of success 0.251, 0.444 and 0.493. The fragment models stay at or below 0.005.
- **§5 and Table 5.1**
  - The refit terms, with non-significant main effects in parentheses, agree with the brief.
  - Runs needed: 16, 12 and 12, and 18, 22 and 8.
  - The 11 refits split 5 viral, 3 with no effect and 3 not reached.
  - The refit differences of low-pH and cation exchange fragments are 0.27 and 0.21, and both fail.
- **§6 and Tables 6.1 and 6.2**
  - Every probability matches `augmentation_sample_size.csv` to three decimals. Some values end in 5 at the
    fourth decimal. The text's 0.921 is the exact value 0.9215, which the brief shows as 0.922.
  - 9 of 10 curves fall at least once; virus filtration MVM is monotone.
  - 0.754 and 0.743 at 18 runs. 0.951 for acidic variants at 16 runs.
  - Lowest power: 0.76, 0.67, 0.55, 0.91, 1.00 and 1.00.
  - All 14 powers in Table 6.2 are correct, and 9 are ≥ 0.90.
  - Refit residual SDs 0.43, 1.50 and 2.37.
  - 4,000 data sets, steps of 2, 81 candidate points.
  - The largest correlation between squared terms falls from 0.69 to 0.54.
  - Planned-run log scale for acidic variants and anion exchange host cell protein, and on all runs also high
    mannose.
- **§7 and Tables 7.1 and 7.2:** every setting matches `doe_*_aug.csv`.
  - Bioreactor: 11 edge midpoints and 5 corners. Anion exchange: 10 and 2.
  - The bioreactor augmentation runs carry all 5 responses. Anion exchange XMuLV, MVM and SEC fragments were
    not measured.
- **§8.1**
  - Afucosylation is the only output whose all-run Box-Cox interval excludes both 0 and 1 (0.11 to 0.79). On its
    planned runs the interval is −0.12 to 0.88, which gives the log scale.
  - The mean-only difference is 0.19 for 12 runs and 0.08 for 28.
  - 4 centre points everywhere, so pure error has 3 degrees of freedom.
- **§8.2 worked example** (on the recorded pH of run 23, see error 2)
  - Coefficient b = 0.443. Fold factors 1.56, 2.43, 0.30, 0.85, 0.88 and 1.08.
  - ELISA precision 9.5 % (AMV-3012). Raw-scale interaction p < 0.001.
  - ln y = 9.382, t = 2.074 on 22 degrees of freedom, s = 0.105, h = 0.107, ±0.230.
  - The interval runs from 9,440 to 14,941 around 11,876 at scale-down, and from 9,698 to 15,349 around 12,201
    at manufacturing scale, 2,503 below and 3,148 above.
  - Offset 0.97 (0.89 to 1.06).
  - 7 outputs are on the log scale, and the list is correct.
- **§8.3**
  - Fit terms −148.6 and −132.8. Penalty 32 + 49.5, and 14 + 5.6. Differences 15.8, 61.9 and 46.1.
  - Candidates: 1,337, 95 and 13.
  - Stepwise comparison over 21 outputs: backward worse for 9, forward for 6, either for 12.
  - Host cell protein at cation exchange: 6, 8 and 3 terms.
- **§8.4**
  - Edge increase 0.84 against 0.70. Bound 0.559.
  - The aggregate model has hold-time and temperature terms only.
  - The NOR in force ends at 120 min and 23 °C, as does the NOR as characterized.
- **§8.5, Table 8.1 and Table 9.1**
  - 18 of 22 adequate, 11 of the 14 failing, and 4 with none. Every scale, term count, run count, p-value, R²,
    predicted R² and difference matches `D.fit` (all runs). Discrepancy IDs PD-003-02/03, PD-005-04, PD-006-04,
    PD-007-01, PD-008-01/02 and PD-009-01 agree with `discrepancy_register`.
- **§8.5.1, Tables 8.2 and 8.3**
  - Planned and all-run selected models: terms, scales and statistics.
  - Full quadratic plus block on all runs: differences 0.12, 0.11 and 0.25. High mannose lack of fit p = 0.638.
  - Counts inside the interval, error ratios and block p-values. Binomial p = 0.043 and < 0.001. Thresholds 14
    of 16 and 10 of 12.
  - Repeated corners: runs 29, 33, 35, 41 and 44. Heterogeneity F-test against the residual SD of the all-run
    model gives p = 0.565 and 0.054.
  - Term changes for high mannose, acidic variants and aggregates.
- **§8.5.2 to §8.5.4 and Table 8.4**
  - Counts 29, 18, 28 and 19. Most adverse results 20.21 (after the offset of 0.27), 1.13, 0.76 and 5.90.
    Margins 2.21, 1.47, 1.24 and 1.28.
  - Only XMuLV at virus filtration differs between the refit and the selection. Its term is filtration pressure,
    p = 0.053, difference 0.24.
  - Low-pH acidic variants are identical within each hold time, and the hold-time model is exact.
  - 3 models with no term.
- **§9.1, Tables 9.2 and 9.3** (apart from error 3)
  - Every limit and downstream value. Widenings of 4 %, 4 %, 7 % and 7 %. The acidic-variant limit stays at
    39.0 %.
  - No conclusion over the NOR changes. Only the PAR of Protein A host cell protein over elution buffer pH moves,
    from 3.21 to 3.24.
  - The qualification differs only for Protein A and cation exchange host cell protein: 16,763 and 414 ng/mg at
    offset ratios 0.89 and 0.63.
  - Verification on all anion exchange runs gives the same 4.27.
  - p_oos is 0 of 2,000 for host cell protein and aggregates. The 95 % bound is 0.15 %.
- **§9.2**
  - XMuLV at low pH: lowest mean 6.16 at pH 3.6, 60 min and 19 °C on the selected model, and 6.43 on the full
    model, against the 6.6 claim. Claims sum to 16.72 against 16.7.
  - Bioreactor acidic variants: lower limit 16.2 %, median 18.4 %, full-model 14.7 % at pH 6.95, 34.5 °C,
    18 days and 130 mmHg. The pH coefficient is negative, as in A-Mab Table 3.16 (config: pH −2.1).
  - Conclusions are identical between the full and selected models at both NORs.
- **PCMP-001:** the §7.2 remedy quotation is verbatim. §6.1 random run order. §6.2 full quadratic, screening
  identifies effects. §6.4 viral worst case. §6.4/§6.5 SD = NOR width/6. §7.1 offset rule with the 90 %
  interval. Version 2.0 item 8, thresholds formerly left to the study. §7.5 tightening and widening rule, and a
  single run as the platform worst case.
- **INV-001:** opened 2026-08-03 on the PCMR-001 review. Version 1.0 documents on hold. Reissue of the reports at
  Version 2.0. CA3 adopted before closure. Verification on the selected models.

## Could not check

- Figure 6.1, which is an image. Its description is consistent with `augmentation_sample_size.csv`.
- The Summary phrase "and one prediction limit that follows from them". It does not say which limit is meant.
- That the integrated model draws from the NOR **in force** (§9.1). The p_oos result is confirmed, but not which
  NOR the simulation used.
- The citations to ICH Q5A(R2), Montgomery, Box and Cox, Hurvich and Tsai, Burnham and Anderson, and Fedorov, as
  sources for what is attributed to them.
- §9.3 item 3, on what PCMR-001 consolidates. PCMR-001 Version 2.0 was not read.
