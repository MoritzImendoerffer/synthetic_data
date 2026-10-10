# Factual check of PCP-007 Version 2.0 (draft rendered 2026-10-10 11:40)

Checker: Claude Opus 5.5 (claude-opus-5-5). Returned as text; saved by the coordinator (condensed).
Every number checks out; the errors are rules and record statements.

## Errors, most consequential first
1. **The plan's own widening rule does not support the 427 ng/mg criterion** (§7.3, §7.6 rule 2, Table
   1.1 note b): the anion exchange model behind the bound fails test 4 (Cook's distance: runs 2 and 9
   above 4/28 on the planned runs). Resolution: shared resolutions item 1 (PCMP-001 §7.5 now names the
   three tests; the fourth does not decide a widening).
2. **§6.4 rewrites a Version 1.0 sampling rule and contradicts the record**: "Pool aggregate, pool host
   cell protein and step yield are measured on each run." Version 1.0 §6.4 required "the responses of
   §5.3" (pool aggregate, pool host cell protein, residual DNA, leached Protein A, step yield);
   S-CEX-UNI now holds DNA and leached Protein A. Write out the Version 1.0 list; do not write "the
   responses of Section 5.3" (Version 2.0 §5.3 now includes fragments, which S-CEX-UNI did not measure).
3. **The residual test as written can never fail** ("The residuals are regressed on the predicted
   values and on the run order"). Shared item 3.
4. **§7.5 states the operating region on mean predictions.** Shared item 5.
5. **§1.1 change 5 misstates what changed** (it implies Version 1.0 did not judge on a single batch;
   PCMP-001 Version 2.0 §1.1 item 6: "Version 1.0 judged every response on a single batch"). Say what is
   new: coefficient uncertainty in each draw, the defined distribution (normal, SD NOR width/6, clipped),
   the 97.5th-percentile rule.
6. **A rule written after the data at the end of §7.2**: "It meets its criterion only if every measured
   result of the designs meets it at manufacturing scale. For fragments the measured results are the
   nrCE-SDS results." That is INV-002 CA2, not PCMP-001. Shared item 6: delete. ("at manufacturing scale"
   also clashes with §5.1: fragments have no known offset.)
7. **§1.1 change 4 misdescribes Version 1.0**: Version 1.0 §5.5 judged adequacy on four things, the fourth
   an examination of the residuals that identified "any run that carries the fit". Say Version 1.0
   examined residuals and influence, with no test and no cut-off.
8. **§1.1 overstates what INV-002 tested** ("which this plan states in Section 7.2"): INV-002 judged lack of
   fit and the overfitting limit (and the F-test); drop the clause or name the tests.
9. **Version 1.0 text rewritten or deleted without being listed** (restore, or list): §5.2 thresholds
   "read as ultraviolet absorbance relative to the peak maximum" became "(OD280)"; §9 deviation sentence
   narrowed and the discrepancy term added; §5.1 deleted "It is the only estimate of experimental error the
   analysis uses"; §8 "Each of the two attributes will be reported with a plot" became "Each output with
   an adequate model".
10. **Corpus-level**: Table 1.1 note a and change 1 vs the frozen Version 1.0 PCP-007 §7 / Table 7.1 (≤ 1 %
   HMW, ≤ 193 ng/mg with factors 5 and 3.2, "before any data exist"; 193 = 100 × 6.19 / 3.2 uses this
   campaign's nominal AEX clearance, so it could not have been set on 2026-02-02). Shared item 2.
11. **§6.2, inherited from Version 1.0**: in a 2^(4−1) fraction the protein-load interactions AB, AC and AD
   are aliased with CD, BD and BC, not "with each other". Fix: "would alias each of them with another
   two-factor interaction" (a descriptive correction).

## Checked and correct
Identity and chronology (approval 2026-02-02; first study 2026-02-04; windows; S-CEX-FRC; AMD-001 inside
the response-surface study; EQ-CHR-118 due 2026-05-30, the only instrumented system); INV-001 facts;
15,000 L; Tables 6.1 and 6.2; designs (19 and 28 runs, 15-term model, 81 combinations) and appendices;
criteria (Table 1.1, Table 7.1, the §7.3 arithmetic 4-fold → 400 → 4.27 → 427, no DNA criterion, leached
Protein A 158 ppm); Table 7.2 worst cases and the criteria relying on each; Table 4.1; qualification (3 + 5
runs; outputs); thresholds and simulation settings; Table 5.1 methods and the S-CEX-FRC statements;
Version 1.0 quotations; no later study described.

## For PCR-007 (not plan errors)
No per-run load aggregate or load host cell protein, and no load DNA or leached Protein A for the
screening runs (§5.4 item 1 and Risk 2 require them); the univariate set-point run is missing; the
fragments verification rests on a model with gap 0.21 (fails §7.2).
