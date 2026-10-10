# INV-002, after the factual check of run 3: what to change (the last fix pass before promotion)

The draft is `pc_package/INV-002_model_adequacy.DRAFT.qmd` (54 pp, every gate green). The factual
check is `factual-INV-002.md` in this folder. Read it in full: it gives each error with its source.
Where this list gives a resolution, write to it. It was checked against the code, the config and
the promoted documents. Change what the list requires and leave the rest alone, except where the
readability rule (WRITING_GUIDE rule 11) makes you rewrite a sentence you touch. Every value stays
computed, and every deciding word is computed or asserted in the setup chunk.

## 0. The config changed under the draft (coordinator, 2026-10-10)

The draft substituted three phrases of the config record at display time, with asserts on the old
wording. The record itself is now corrected, so those asserts fail, as they should:
- the CAPA action PA1 now reads "for a probability of success of at least 0.90";
- the effectiveness check now names "the sample-size calculation of preventive action PA1" instead of
  "the design-size check";
- `assurance_basis` now reads "an attribute with a criterion" instead of "a criterion attribute".

Remove the three substitutions and their asserts, and print the record as it stands, so that
Table 10.1 and the effectiveness check quote the record verbatim (this also resolves error 9 of the
factual check). The y-axis of `D.fig_assurance()` now reads "Probability of success", so the figure
and the text use one term. Keep any assert that still guards a fact (for example the split of the
effectiveness check into its three parts).

## 1. The model-adequacy criteria of PCMP-001 §7.2 are four, not three (factual error 1)

- Say once, where the criteria are first given (Section 3), that §7.2 has four criteria: the model
  F-test, the lack-of-fit test, the limit on R² minus predicted R², and the criterion that the
  residuals show no pattern against predicted values or run order and that no single run dominates
  the fit.
- Say that this investigation applies the first three as tests, because they decide whether a model
  of a design of this size can be adequate at all, and that the fourth criterion is judged by each
  step report for its own models. Do not state a result for the fourth criterion unless you compute
  it. If you name an example, the Protein A report records its influence analysis as discrepancy
  PD-005-02 (`discrepancy_register("PCR-005")`); word it so that it does not imply the Version 2.0
  report was issued before this investigation closed.
- Then scope every later use: "adequate" in this document means that a model meets the three tests.
  Define that once, and change each place that presents the three tests as the whole of §7.2 (the
  factual check lists them: the Summary, §1, §5, §6.1, §8.1 step 3, §8.4, §8.5.1, §9, §11, §12 and the
  notes to Tables 2.1, 3.1 and 8.1). A table note may say "the three tests of PCMP-001 §7.2 that this
  investigation applies" or equivalent.

## 2. Protein A response-surface run 23: design pH or recorded pH (factual error 2)

Coordinator's resolution, consistent with the promoted PCR-005 ("With run 23 at its design pH, as
Version 1.0 and INV-002 fitted it, the same model meets both tests"):
- Table 3.1 and Section 3 apply the tests to the full quadratic models as Version 1.0 fitted them,
  with run 23 at its design elution buffer pH. Say so in Section 3 and in the note to Table 3.1. The
  count of failing models stays as Table 3.1 computes it.
- Add, computed: at the pH recorded under deviation DEV-005-01, which the Version 2.0 analysis uses
  (discrepancy PD-005-03), the full quadratic model of pool host cell protein fails the lack-of-fit
  test (p = 0.024 in the factual check; compute it, for example with the private fit on the planned
  runs, full form, corrected settings, or the corrected `rsm_data`). Its selected model on the
  recorded pH is the one Table 8.1 reports. Model selection (corrective action CA3) covers every
  output, so this model needs no separate remedy. State that consequence only if Table 8.1 shows the
  selected model adequate.
- Qualify "No model showed significant lack of fit" in the Summary and "No model fails the
  lack-of-fit test" in Section 3 so that they are true for the reading they describe.
- In §8.2 say which reading the worked example uses (the recorded pH: its values are the
  recorded-pH values, as the factual check confirmed).

## 3. Table 9.2: the footnote marks are swapped (factual error 3)

Mark a) sits on the acidic-variant value and points at the anion exchange note, and mark b) the
reverse. Attach each note to its own cell. If the table is built with `ctable`, use `marker_for(text)`
or the builder's note mechanism so the letters follow the order of use and cannot drift again.
Render and read the page image of Table 9.2.

## 4. What Version 1.0 did about model adequacy (factual error 4)

Version 1.0 did apply adequacy checks, but with no numeric limit on overfitting:
- the Version 1.0 PCMP-001 accepted a model when its terms were significant at α = 0.05, the lack of
  fit was not significant against pure error, and predicted R² was consistent with adjusted R²,
  and left the numeric thresholds to each study;
- the Version 1.0 plans (PCP-003 for example) set the lack-of-fit test, predicted R² tracking
  adjusted R² and residual diagnostics, with no numeric threshold;
- the Version 1.0 reports applied the lack-of-fit test (PCR-003 Version 1.0, Table 5.8).

Change §1 ("applied no adequacy test"), the Summary and §12 ("set no adequacy criterion") to say
what Version 1.0 lacked: a numeric limit on how far predicted R² may fall below R², against which
the size of a design could have been checked. Section 4 already says this correctly; make the other
places agree with it. You may read, for content only, the frozen Version 1.0 PDFs
`pc_package/superseded/rev1/PCMP-001_master_plan.pdf`, `PCP-003_bioreactor.pdf` and
`PCR-003_bioreactor.pdf` (`pdftotext -layout`), to check the wording you write.

## 5. AICc (factual error 5)

`amab_process/adequacy.py` `aicc()` (you may read this function) returns the statsmodels AIC plus
the small-sample correction: n·ln(SSE/n) + n(1 + ln 2π) + 2p + 2k(k + 1)/(n − k − 1), with p the
number of coefficients and k = p + 1. The draft defines the fit term and the penalty differently and
then reports the code's values. Either define AICc as the code computes it, or keep your definition
and say that the values reported include a term that is the same for every candidate of an output,
so that only differences between candidates carry information. The differences the draft gives are
unaffected. Check that every AICc value and every penalty you print follows the definition you give.

## 6. The minor errors

- **INV-001 quotation (error 6):** §9.3 item 1. INV-001 compares the proven acceptable ranges of
  Version 1.0 and Version 2.0 on the models Version 1.0 fitted; the criteria themselves rest on the
  selected models. Write it so.
- **NOR of the worked example (error 7):** §8.2 item 5, "at the least favourable combination of the NOR
  in force".
- **SOP-1002 title (error 8):** §10. Take the title from the SOP register helper rather than typing it,
  and write it as a title ("SOP-1002, Design, Execution and Statistical Analysis of DoE Studies").

## 7. What the factual check could not check (make each one checkable or true)

- The Summary phrase "and one prediction limit that follows from them" does not say which limit.
  Name it.
- §9.1 says the integrated model draws from the NOR in force. Keep it only if the code says so; if
  you cannot establish it from `doe_report`, `tables` or the brief, write what you can establish.
- §9.3 item 3 says what PCMR-001 consolidates. PCMR-001 Version 2.0 is not written. State it as what
  this investigation requires of the master report, not as a description of its content.

## Gate and report

Gate with `check_render.py --render`, render the pdf and the docx, read the page images of the
tables you changed (3.1, 9.2 and any other), and report: which model you are, each item above with
where it was resolved, how many check_render passes you needed, the page count, and any
`<<NEEDS:>>` left (there should be none). Keep `status-INV-002.md` in this folder current as you go
(a short log; a successor must be able to resume from it).
