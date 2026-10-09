# INV-002, after review run 2: what to change (the final fix pass)

The draft is `pc_package/INV-002_model_adequacy.DRAFT.qmd`. There are two inputs:
- the data-state note, `data-state-2026-10-09b.md` in this folder. Read it first; the data changed;
- the second content review, `content-review-INV-002.run2.md`, which flags every sentence it quotes.

Where this list gives a resolution, write to it. It was checked against the code and the data. Every
value stays computed, and every deciding word is computed or asserted in the setup chunk.

## A. The data changed: the exact fit (owner, 2026-10-09)

1. Acidic variants in the low-pH design have no scatter. Every result at the same hold time is
   identical, so the full quadratic reproduces them exactly.
   - With no residual there is no pure error for the lack-of-fit test and no residual mean square for
     the model F-test. The model-adequacy criteria therefore cannot be applied.
   - The Box-Cox profile is unbounded, so no interval exists.
   - The engine now returns `adequate = False` and no Box-Cox interval for it (`D.fit(...)["exact"]`).
   - Rewrite the section on an output that fits exactly:
     - the output has no adequate model;
     - it is judged on its measured results;
     - its bound cannot replace a platform value;
     - so the bioreactor acidic-variant upper limit stays at its a priori value.
   - Remove "with replicates that agree exactly at the precision the method reports" and every "fitted
     exactly by more than one candidate" argument. The reason is the absence of scatter, not the
     reporting precision.
2. The counts follow from the data: adequate selected models, criteria widened (now three, not four),
   Table 2.1, Table 9.2 and Table 9.3. Recompute every count, and every sentence that names the widened
   criteria.
3. The sentence that the raw scale is kept where the Box-Cox interval excludes both 0 and 1 is wrong for
   acidic variants, because there is no interval. For afucosylation it holds on all runs only: its
   planned-run model is on the log scale. Make the sentence computed and scoped to the runs it is true
   for.
4. Labels changed: "CO2 partial pressure (pCO2)", mOsm/kg. Never type a parameter name or unit.

## B. The three most consequential problems

1. **Show the adequacy verdicts.**
   - Add a table of every selected model of an output with a criterion. Build it with `T.frame` from
     `D.fit(step, "rsm", resp)`. Columns: the step, the attribute, the scale, the number of terms, the
     runs, the p-value of the model F-test, the p-value of the lack-of-fit test, R², predicted R², R²
     minus predicted R², and the verdict ("adequate", "not adequate", "not testable: exact fit").
   - Show the full quadratic models that pass on the planned runs as well, with
     `T.model_adequacy(failing_only=False)`.
   - Report what the augmentations were sized for: whether the full quadratic with a block term meets
     the model-adequacy criteria on all runs, for each of the three augmented models
     (`D.fit(step, "rsm", resp, form="full")`). Report it as met or not met.
2. **The bioreactor aggregate criterion and the NOR in force.**
   - Replace "The criterion that follows is still right, because routine manufacture never holds longer
     than the NOR" with the computed argument:
     - the low-pH aggregate model has no pH term (`D.fit("viral_inactivation", "rsm", "aggregate_out_pct")["names"]`);
     - the NOR in force ends at the same longest hold and highest temperature as the NOR as
       characterized (`Parameter.nor` against `.nor_characterized`);
     - so the bound over the NOR as characterized also covers the NOR in force.
     Assert both facts.
   - Remove "a normal-tail probability of less than one per million". State instead:
     - the number of simulated batches out of specification, with its one-sided 95 % upper bound on the
       rate, `1 - 0.05**(1/n)`, computed;
     - in one or two sentences, what the integrated process model is: batches simulated through the
       whole train from the step models, with their run-to-run variation, over the NOR in force
       (`D.p_oos()` docstring).
     Never give a normal tail for host cell protein, whose error you show to be multiplicative.
3. **The effectiveness check.**
   - The config now gives a criterion that tests the prediction of new runs
     (`campaign.investigation_2.effectiveness_check`). State it as the config gives it.
   - CA1 and CA3 are open at closure. The Version 2.0 reports carry the re-evaluation on all runs and
     the model selection. Table 10.1 and the closure section follow the config.

## C. Statements that are wrong or contradicted (review Q5, by its numbers)

- **6.** Rewrite the block-term sentence. The block term tests a constant shift between the blocks, and
  its p-values give no evidence of one. That is not evidence that nothing changed between the
  campaigns.
- **7.** The augmentation does repeat planned corner points (runs 29, 33, 35, 41 and 44, and anion
  exchange runs 33 and 36), and a change between blocks would show there. Either compare the planned
  and augmentation results at those repeated corners for the outputs in question (computed), or drop
  the claim.
- **8 and 9.** Define the count of Table 8.3 as every measured result of the screening and
  response-surface designs of the step. Its note must not say "at manufacturing scale" for a log
  reduction: viral clearance has no manufacturing-scale result and no offset.
- **10.** High mannose was selected on the raw scale on the planned runs, and on the log scale on all
  runs. Compute the sentence from the fits.
- **12.** Label the half-split values as the standard deviation of the residuals in each half of the
  predictions, not the residual standard error of the model. Do not compare them with the assay
  precision.
- **13.** Say what the evidence shows: the spread no longer grows with the level on the log scale, and
  the Box-Cox interval supports the log scale. A test can fail to reject an assumption, not prove it,
  and the evidence is for the full quadratic.
- **14.** Change "below the limit on overfitting" to "above".
- **15.** State the remedy of PCMP-001 §7.2 once, in the words of the rendered master plan: "A model
  that fails the lack-of-fit test or the limit on overfitting is either refitted with a justified
  change of terms or transformation, or it is not used to set a range." Make Sections 3 and 5 agree
  with it. Augmentation is this investigation's rule, not a remedy of §7.2.
- **16.** A p-value of a term does compare two nested models. What it does not do is weigh fit against
  the number of terms on one scale, or compare models that are not nested.
- **18.** State both limitations of the simulation as limitations. It re-draws the planned results
  instead of conditioning on them. The refit's kept coefficients are biased away from zero, so the
  probability of success is optimistic.
- **19.** The builder now prints three decimals. Check the text against it.
- **20.** Give the power where it was computed. Elsewhere, drop "at the power the designs give".
- **21–26.**
  - The lack-of-fit test has little power with 3 degrees of freedom for pure error. Say so where you
    lean on a passed test.
  - "Everywhere within the NOR" becomes "at every combination of NOR low, set-point and NOR high".
  - Give the PRESS enlargement at the average leverage as that, or use Σ1/(1−h)/(n−p).
  - Scope the model-of-the-mean sentence to a single block.
  - Least-squares estimates need no normality; the tests and intervals do.
  - Give SDs of percentage results in percentage points.
- **27.** The direction comes from the A-Mab case study's model, Table 3.16: higher culture pH lowers
  acidic variants, and the seeded data follow it. State the sign from the fitted model and cite the
  source. Do not explain it by deamidation.

## D. Terms, glosses, machine-like sentences, references (Q2, Q3, Q6, Q7)

- **Terms.**
  - "Assurance" becomes "probability of success". The builders already say so.
  - Define "conclusion over the NOR", "NOR as characterized", "NOR in force" and "single-batch bound" in
    words at first use, and use the full term once in each section.
  - Replace "statistically purer" and "pragmatic rule" with the reason: a tolerance-interval bound
    covers a stated share of all batches with stated confidence, and is wider.
  - "Design-size check" becomes "the sample-size calculation (PA1)".
  - "Criterion attribute" becomes "attribute with a criterion".
- **Glosses.** Remove the eleven Q3 glosses the review lists, among them "and nothing else",
  "never by a confidence bound of the mean" in the Summary, "A replacement does not always mean …",
  "the record" glosses and "a weaker standard".
- **Machine-like sentences.** Cut or merge the sixteen Q6 sentences. Section 8.5.5 duplicates
  Section 9.1, so keep one.
- **References that name nothing.** Never use "§7.2" alone: write "the model-adequacy criteria of the
  master plan" and name the three tests at first use in each section. Name INV-001 ("the investigation
  into acceptance criteria set after the data were seen") and PCMP-001 ("the process characterization
  master plan") at first use in each section. Name every rule, study and action code (Q7 D and E).
- **Statements the record may not support.** "Detected at release" and "not the patient" are your own
  reading of the specification. Keep a release-test statement only where the brief or the CQA register
  supports it; otherwise drop it.

## E. The owner's request: the log scale and the search (review section, "partly met")

Close the gaps the review lists:
- Explain the Box-Cox step and λ:
  - the output is raised to the power λ; λ = 1 is the raw scale and λ = 0 is read as the natural log;
  - the profile likelihood shows how well each power gives residuals of equal spread;
  - the interval is the set of powers the data do not reject;
  - the scale is chosen on the full quadratic before the search, so that the search compares models on
    one scale.
- Work one coded unit in real units. For protein load, e^(2b) over the range studied gives e^b per coded
  unit, which is half the range in g/L resin; compute both.
- For load flow rate, which has a squared term, give the factor from low to centre and from centre to
  high.
- In the worked interval, say that it is two-sided, computed on the log scale as the prediction ± t·s·√(1
  + h) and transformed back, and whether the scale-down offset is applied. Use "single run" or "single
  batch" consistently with the rest of the document.
- Show the fit term of AICc, n·ln(SSE/n), beside its penalty.

## F. Tables (the review's table observations)

- **Table 1.1:** expand the study codes, or name each study in the row.
- **Table 3.1:** shorter headers, with the step label on the first row of its group.
- **Table 8.1:** drop the constant "Model p" column, and give R² and predicted R² separately.
- **Table 8.2:**
  - put HMW in the Abbreviations;
  - move "Block p" (a different model) into a note, or into a column labelled with its model.
- **Table 8.3:** "Number of results", not "Measured results".
- **Table 9.1:** give a scale for the rows with no adequate model, or a note that none is chosen.
- **Table 9.2:**
  - the unit in each row;
  - a note "calculated before rounding";
  - "Full" and "Selected" used once each, with one meaning.
- **Table 9.3:** drop or merge the constant column.
- **Table 10.1:** take the status from the config.
- **Abbreviations:** add HMW, CV (column volumes), AMV, RSM, and the document-type codes (PCR, PCMP, PCMR,
  INV).

## G. Gate and report

Gate with `PATH="$PWD/.venv/bin:$PATH" uv run python authoring/check_render.py pc_package/INV-002_model_adequacy.DRAFT.qmd --render`.
It now also fails on an inline expression printed as source. Look at the new adequacy table and at
Tables 6.1, 8.1–8.3 and 9.1–9.3 in the PDF. Report what you changed under A to F, what you did not
change and why, the gate result and the page count.
