# Shared resolutions for the plan revisions of 2026-10-10 (PCP-007, PCP-008, PCP-009)

The reviews of the three plans found the same corpus-level points. The coordinator resolved them as
follows (some by correcting PCMP-001, which is re-rendered). Write to these resolutions; each plan's own
fix list (`feedback-PCP-00N.run1.md`) adds the step-specific items. Read `data-state-2026-10-10.md` and
`procedures/PLAN-LESSONS.md` (rules 4, 8 and 10 were updated today) first.

1. **The widening rule names its tests.** PCMP-001 §7.5 rule 2 now reads: the bound replaces the platform
   value where it is better and "the response-surface model behind it meets the first three adequacy
   criteria of §7.2 (a significant model, no significant lack of fit and the limit on overfitting) and is
   not an exact fit. The fourth criterion, on the residuals and on influential runs, does not decide the
   change. The report that gives the bound examines it and states whether the bound depends on a single
   run." This is what the engine always did (`amab_process/iac.py`) and what the owner decided on
   2026-10-08 (gap and lack of fit). Restate the rule so; never "passes the tests of Section 7.2", which
   reads as all four.
2. **The frozen Version 1.0 plan carries criteria that no approved plan contained** (PLAN-LESSONS rule
   8). The frozen PDF is the July 2026 compilation: INV-001 root cause 1, criteria set after execution
   "could therefore be added to the plan text when the package was compiled, without a revision of the
   approved plan". The note "No approved Version 1.0 plan contained these criteria" stands. The change on
   the Version 1.0 record names both: the title-block date, and the criteria added to the plan text at
   compilation. Where the plan quotes a Version 1.0 limit, say it was written into the compiled text,
   not approved with the plan.
3. **The residual test regresses the absolute residuals** on the predicted values (and the residuals on
   run order), at `THRESHOLDS["residual_alpha"]` (PLAN-LESSONS rule 10). Cook's distance against
   `THRESHOLDS["cook_factor"]`/n stays as the generic test of every plan; the reports examine a flagged
   run by an influence analysis (their registered discrepancy). Use the two thresholds from `THRESHOLDS`,
   never typed.
4. **Classification.** Keep the Version 1.0 classification sentence word for word, and list the rule of
   PCMP-001 Version 2.0 (§6.2 for "affected", §7.7 for the effect size across the PAR and the margin of
   the PAR to the NOR) as a change, with what it changes (as PCP-010 now does).
5. **The design space is drawn on the single-batch limit.** PCMP-001 Version 2.0 now states it among its
   judgement statistics: a setting lies inside when every quality attribute meets its criterion at both
   ends of the 95 % prediction interval of a single run, and viral clearance on its mean prediction.
   Restate it where the plan defines its operating region or design space, and list it as a change from
   Version 1.0 (which drew the region on the model predictions, that is the mean, or did not say).
6. **The remedy of a failing model is PCMP-001's, word for word**: "either refitted with a justified
   change of terms or transformation, or it is not used to set a range". List it as a change with the
   Version 1.0 consequence it replaces. Judging an output with no adequate model on its measured results
   is INV-002 corrective action CA2, which the reports apply: a plan does not state it as its rule.
7. **The NOR-propagated draw**, as PCMP-001 §6.4 defines it: each other parameter from a normal
   distribution centred on its set-point, standard deviation the NOR width divided by `D.NOR_SD_DIVISOR`,
   clipped to the range studied. Where a set-point is not the midpoint of its NOR, that draw is not
   centred on the NOR and reaches past one NOR edge; do not write that it "treats the NOR as ±3 standard
   deviations" for such a parameter.
8. **Version 1.0 text.** Restore, word for word, every Version 1.0 design, sampling, spiking and decision
   statement that was paraphrased or deleted, including expectations the data did not bear out (the
   report compares them with the data). A descriptive sentence that is scientifically wrong may be
   corrected without changing the design; list such corrections together as one change. Mark Version 1.0
   rules where a reader could take them for new ones.
9. **No execution record in a plan** beyond what PCMP-001 Version 2.0 asks of every plan (the execution
   window of each study and the calibration status of the instrumented systems, INV-001 preventive
   action PA3): state those as recorded facts, in the past tense; leave every other fact of execution to
   the report.
10. **INV-002.** A plan of a step with a design is reissued under INV-001 and INV-002 (its revision
   history). Say once what INV-002 investigated (response-surface models below the model-adequacy
   criteria) and that its corrective actions are applied by the report; list INV-002 in the table of
   related documents only if the table builder does (it does not for plans), and otherwise name it in the
   text where the revision history mentions it.
