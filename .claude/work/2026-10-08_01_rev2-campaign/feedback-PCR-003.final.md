# PCR-003 after review run 2: the final pass (same author)

Inputs:
- `content-review-PCR-003.run2.md` (the fresh judge's flags on your revised draft);
- the owner's decisions of 2026-10-10 on the record (section A) and of 2026-10-11 on the bioreactor (section B);
- `procedures/REPORT-LESSONS.md` §3 rule 1, §6 rule 9 and the new §7. Read those first.

This is the last pass before promotion. Fix the items below. Where an item gives a resolution, write to it. Every value
stays computed and every deciding word computed or asserted. Regenerate your brief (`authoring/build_brief.py
PCR-003`), because the register and the classes changed. The config and builders are committed (00c0e64, f055c60,
05c068d).

## A. The record: no deviations (owner, 2026-10-10)
A process characterization study is not GMP manufacture, so it raises no deviation.
- **The seven review findings are now discrepancies PD-003-07 to PD-003-13** (formerly DEV-003-03 to DEV-003-09), in
  the same order:
  - PD-003-07: osmolality not carried into the response-surface design;
  - PD-003-08: NOR not narrowed for acidic variants;
  - PD-003-09: viable cell density, viability and titre not in the record;
  - PD-003-10: univariate study before the response-surface study;
  - PD-003-11: initial viable cell concentration not carried into a multivariate study;
  - PD-003-12: equipment and calibration not recorded for the osmolality and augmentation studies;
  - PD-003-13: the aggregate offset accounted for, not investigated, because the Version 1.0 test was stricter than
    the use of the model needs.
- **DEV-003-01 and DEV-003-02 stay as study events,** under their Version 1.0 numbers. `dev_register` prints Event /
  Summary / Detected during / Outcome.

What to change:
1. **Rename §13 "Study events and discrepancies from the plan".** Open it with one sentence: PCP-003 calls a departure
   from the plan a deviation, and because a process characterization study is not GMP manufacture, this report
   records the events of execution as study events, under the numbers Version 1.0 gave them, and every departure from
   the plan as a discrepancy from the plan. Events come first, then discrepancies.
2. **Move the former deviation subsections into the discrepancy part** under their new numbers, and update all
   mentions (about 36). No "deviation" in your own text. The §13 definition of a discrepancy follows the record rule,
   which answers review Q5.3.
3. **PD-003-13.** Give the Version 1.0 test, the difference under it (as computed) and the register's reason. Do not
   call it a failure of Version 1.0.
4. **Changes in this revision.** One item records the change of term and that the departures found in the
   re-analysis are discrepancies.
5. **Asserts.** Adapt the setup asserts to two events and the new entries.

## B. The owner's decisions on the bioreactor (2026-10-11)
1. **Control of pH and pCO2 (review Q5.13).** Describe the control as it must have run with pCO2 as a design factor:
   culture pH held by base addition (the lactate of the culture lowers it), and pCO2 held by the CO2 fraction of the
   sparge gas. This corrects the Version 1.0 description, "controlled by carbon dioxide and base addition". List it as
   a correction, and drop "readily controlled by carbon dioxide and base addition" in §9. The coordinator corrects the
   same sentence in PCP-003.
2. **Classes by the rule of PCMP-001 §7.7.** The config now holds:
   - osmolality CPP: it acts on acidic variants, and its PAR is not wide against its NOR, so the risk of operating
     outside it is not low;
   - dissolved oxygen GPP: no effect on a quality attribute or on process performance is shown;
   - basal medium concentration KPP: an effect on growth and titre is expected, and the record holds no titre.

   Argue each class from the rule and the evidence, and delete the "conflict" sentences (review Q5.5, Q3.10, Q6.8).
   The counts across the campaign change. Read them from the helpers.
3. **Initial viable cell concentration (review Q5.14).** At its NOR low the worst-corner median of acidic variants is
   below the lower limit. The risk acceptance of PD-003-08 is extended to that corner (PD-003-11). State three things:
   - the effect is one significant result among the univariate tests at the per-test level of PCMP-001 §6.2, so
     about one false positive is expected among them. Apply no correction chosen after the result;
   - the acceptance covers the corner on the same producer's-risk grounds;
   - acidic variants at harvest are to be trended against the initial viable cell concentration of each production
     batch (the config `campaign.risk_mitigation...monitoring`). That monitoring is recommended so that a false
     positive is found out.
4. **Alarm and action limits (review Q4.7).** `D.acidic_mitigation()` gives them:
   - an alarm limit inside the NOR on the side that lowers acidic variants, for pH, pCO2 and osmolality, half-way from
     the set-point to that NOR edge;
   - an action limit for acidic variants at harvest, the lower criterion plus two intermediate-precision standard
     deviations of icIEF (AMV-3013).

   Cite the values and the rule in §10 and where §7.2 relies on the mitigation. They are recommendations of this
   report for the control strategy, which PCMR-001 consolidates.

## C. Builders changed under you (re-render to pick them up)
- `T.criteria_results` has a column "95 % limits of a single run over the NOR", the statistic that decides each
  verdict. This answers Table 7.2: the acidic-variant "No" now shows its lower limit. If the table falls below the font
  floor, wrap it as PCR-005 and PCR-006 did, in your own chunk.
- The design tables label high mannose "High mannose", not "Man5". Drop "Man5" from the abbreviations (review Q2.10).
- The Appendix A note now reads "CO2 partial pressure (pCO2) of 153.5 mmHg". Say in the text that the "Run" column
  of the design tables is the standard order, not the run order, and that run 4 shows its design setting while the
  analysis uses the recorded one (review tables A.1/B.1, Q5.7).

## D. Errors (Q5): correct each
- **D-002 stays** (Q5.1). Keep the registered sentence of §1.1 exactly. Correct only the elaboration after it, if it
  claims more.
- **Q5.2.** The low-pH acidic-variant model is an exact fit and cannot be judged, so it gives no 39.6 %. Correct the
  sentence that it would.
- **Q5.4.** No in-process test of aggregate exists at this step, so no batch "fails at this step". Restate the risk:
  a tightening moves the risk to the producer through the release test, which detects an excursion.
- **Q5.6.** Report the residual criterion as it is tested (the slope of the absolute residuals on the predicted values,
  with its p), and describe the two halves consistently with it. Make no claim the numbers do not support.
- **Q5.8.** "Single batch at manufacturing scale" says more than the interval holds. Use the builder's definition: the
  95 % prediction interval of a single run, at manufacturing scale with the offset applied. Say once what it does not
  include: variance between manufacturing batches beyond the run-to-run scatter of the model, and the offset
  uncertainty, which the qualification handles.
- **Q5.10.** Osmolality was a factor of the screening design (360 and 440 mOsm/kg) and was held at its set-point in
  the response-surface design. Correct "held constant while pCO2 varied in these designs".
- **Q5.11.** Check the Version 1.0 acidic-variant criterion in Table 1.2 against finding 4, and make the text agree.
- **Q5.12.** Reconcile "the feed replenishes those components faster than the cells use them" with the late depletion
  of the donor and manganese. Keep the one the data and PCP-003 support, and say the record holds no metabolite data.
- **Q5.15.** The osmolality slope is not significant (p = 0.191, Table 5.12), and the "Mean" values are fitted values.
  Say so. Do not write that osmolality "takes the mean below the lower limit" as a finding.
- **Q5.16.** State the bias of the selected models at the set-point, computed, against the centre-point and
  manufacturing means:
  - acidic variants: 22.23 % predicted against 21.50 % at the centre points, and 22.8 % against 21.85 % at
    manufacturing scale;
  - afucosylation: 8.29 % against 7.61 %.

  Say what the acidic-variant bias means for the 0.39-point margin of the worst-corner median.
- **Q5.17.** The residual of screening run 4 is near zero by leverage. Drop it as evidence, and keep the comparison
  with the run at its design setting and excluded.
- **Q5.18.** Soften "completed in the Golgi before the antibody is secreted". Glycosidases from lysed cells can trim
  glycans in the culture fluid.
- **Q5.19.** For the residual DNA criterion, name its source (A-Mab's claimed range, met through clearance, A-Mab p.47)
  and the dose (`DOSE`, 10 mg/kg for a 70 kg reference adult, an assumption).
- **Q5.20.** State the detectable difference with its power: a difference of 3.1 points is detected about half the
  time, and the difference detectable at 80 % power is computed.

## E. Q4: criteria and judgements
- **Effect-size bands (Q4.1).** PCMP-001 §7.7 asks for the size of an effect beside its significance. Your bands are
  a reading of that size, a judgement and not a rule (REPORT-LESSONS §7 rule 5). The classes are now argued by the rule
  (B2).
- **Normality (Q4.4).** Report the result in the words of the criterion, or state the departure.
- **Prediction of the augmentation runs (Q4.5).** State the consequence: for aggregate only 11 of 16 runs fall inside
  their 95 % interval, so the single-run intervals of aggregate understate the scatter. That is a limitation of the
  aggregate conclusions over the NOR.
- **"Narrowing it was judged impractical" (Q4.6).** Give the basis, which is the risk acceptance of PD-003-08 with its
  reason.
- **"Confirmed by three determinations" (Q4.8).** Say what the record shows, without "confirmed".

## F. Q1, Q2, Q3, Q6, Q7
Fix the flagged sentences in your own text:
- **Causes and directions.** Name the physical cause and its direction, for example the direction of the pH effect on
  each glycan attribute, and the route of culture duration.
- **Terms.** Keep a term PCMP-001 defines, defined once at first use, and replace a coined label with what it means:
  "routine standard deviations", "carried back", "declared operating region", "back toward the patient".
- **Filing sentences (Q3).** Cut them.
- **Restatements (Q6).** Say the containment point once in the body, plus the summary and the conclusions; it now
  appears about eight times.
- **Stand-alone sentences (Q7).**
  - Name the CA3 procedure and the limit on overfitting.
  - Replace "the conclusion over the NOR" with what it means: whether each attribute meets its criterion at every NOR
    combination.
  - Name the augmentation rule where its date is given.
  - Name each code's subject at first use.

## G. Tables and figures
- Table 5.5: rename the "F(p, n − p)" column "F median", because "p" is also a p-value.
- Table 5.12: "Fitted mean".
- Table 7.1: a note that the criterion is computed from unrounded values (6.46 against 6.44). Also show that the
  acidic-variant increase applies to the upper limit only.
- Table 8.1: DNA in ng/dose with sensible digits, and the tail per million stated once.
- Figure 6.1: the caption says the grid covers the NOR of pH and pCO2.
- Leave as the builders give them, and report them if wrong: Table 3.1 (differences and ratios in one column),
  Table 1.2 (rule codes) and Table 3.3.

## H. Gate and report
- Gate with `check_render.py --render` (`.venv/bin/python`, venv on PATH).
- Render the pdf and the docx, and run `check_render` once more.
- Read the page image of every table and figure you changed.
- Refresh `.claude/work/2026-10-08_01_rev2-campaign/PCR-003_bioreactor.DRAFT.txt`.
- Report each item with where it was resolved, anything left and why, the passes, the page count, and any
  `<<NEEDS:>>` left (none). Cut restatements before adding anything (82 pp now). Do not commit.
