# Factual check of PCR-003 Version 2.0 (draft text of 2026-10-10, rendered 15:44)

Checker: Claude Opus 5.5 (claude-opus-5-5). Returned as text; saved by the coordinator (condensed, every error
kept). Scratch scripts in `scratchpad/chk/`. The register changed after the draft was rendered (DEV-003-07 and
-08 added; DEV-003-01, -03, -05 reworded); the draft was checked against the current register.

1. **"Every NOR-propagated PAR contains the NOR" holds only with the augmentation and the model selection**, and
   the report never says so (§7.2 risk ground 2, §1.4, §13.9 "no conclusion would change", the executive
   summary, Conclusion 3; §5.3.4 and §13.8 list only term changes). Recomputed: selected models on the 28
   planned runs: acidic-variant PARs pH 6.6–6.94, temperature 34.525–36, pCO2 40–116.5 mmHg, none containing the
   NOR; worst-corner lower limit 15.48 % (median 18.01 %); design space 59.6 % (73.7 % on all runs). The plan's
   full quadratic on all 44 runs: pCO2 PAR 40–122.5, design space 63.6 %, high mannose fails the overfitting
   limit (gap 0.247). The full quadratic on the planned runs: pCO2 40–115 mmHg, which INV-001 prints ("no longer
   reaches the upper end of the NOR at 130 mmHg") against PCR-003's 40–131, unexplained. Fix: state these
   results in §5.3.4, §13.8, §13.9; replace "no conclusion would change"; in §7.2 ground 2 and §1.4 say that
   containment rests on runs added after the planned results were known (optional stopping) and on PD-003-03;
   reconcile with INV-001. Hand-back: does ground 2 still support accepting DEV-003-04?
2. **Register entries the draft does not carry**: (a) eight deviations, not six (DEV-003-07, -08 in the
   executive summary, §1.4 item 8, §11, §13; §5.4, §7.4, §9, §11 item 5, §12 item 7 cite DEV-003-07; §4.6 and
   Table 4.3 cite DEV-003-08); (b) DEV-003-01 now gives the direction (the probe read high), so run 4 ran at
   about 153.5 mmHg [the engine now analyses it there: `D.setting_corrections("bioreactor", "screening")`];
   §13.1 "the record gives the size of the drift but not its sign" and §5.2 "either possible setting" change;
   (c) DEV-003-07's disposition is the effect sized against the criterion over the NOR: 0.70 points at
   manufacturing scale; added to the worst corner the median 18.39 % becomes about 17.7 % (below 18.0 even on
   the median) and the lower prediction limit about 15.5 %; the executive summary's "predicted median is
   18.4 %" needs the qualifier; (d) DEV-003-08 needs an impact statement (pCO2 varied in all 16 augmentation
   runs, every selected model fitted to them; pCO2 at 130 mmHg in the osmolality study; both after the
   EQ-BRX-205 calibration due date 2026-06-14).
3. **The classification arguments contradict §2.1**: dissolved oxygen a KPP "on the role of dissolved oxygen in
   the oxidative metabolism (Section 2.1)" while §2.1 expects no oxygen limitation (PCMP-001 §7.7 points to GPP);
   basal medium a GPP because "Section 2.1 expects a higher basal medium concentration to raise growth and titre"
   (it does not; plan §4.1 does, which points to KPP). Correct the reference, state the conflict, hand back.
4. §5.3.5 "They differ in single terms" (one to four terms).
5. Appendix B factor letters (C = duration, D = pCO2) vs Table 4.2 and every other table (C = pCO2, E =
   duration); cause: the builder (`tables.py` around line 524) assigns letters by column position [coordinator:
   builder to fix].
6. Departures in neither register: (a) plan §7 item 4 (each effect against the width of its criterion, with a
   judgement of practical importance; PCMP-001 §7.7) done nowhere; (b) offset timing (offsets in the re-analysis,
   after the characterization) [coordinator: the Version 1.0 test for a difference estimated the difference of
   means before the characterization; the confidence interval and the decision came at analysis, as PCMP-001
   §7.1 allows; say so]; (c) adjusted R² not reported (0.941, 0.951, 0.806, 0.928, 0.949); (d) the ranges carried
   into the control strategy (the intersection of the PARs, plan §7 item 7: pH 6.6–7.02, pCO2 40–131) not
   stated; (e) possibly host cell protein and DNA not measured on the qualification runs (plan §1, §4.2, §5.4
   "every run"); (f) the univariate t-test is the report's own approach, not "the level PCP-003 sets".
7. §13.1 "With run 4 excluded ... fewer effects reach significance" is false for afucosylation (three either way).
8. Next to D-002 (keep the registered sentence): the elaboration "The charge variant distribution is established
   inside the cell and in the culture fluid ..." overstates (Table 7.1 carries an increase at low pH; "no
   downstream step lowers" is an assumption, PCP-003 §12). Fix the elaboration only.
9. Minor: "decided on 2026-09-02, before any further run was made" (S-BRX-OSM started 2026-09-01: "before any
   augmentation run"); "PCO2" in Table 5.2; "p ≥ 0.201" (0.2007); stepwise "backward or forward"; 3.42 and 0.68
   at scale-down scale (3.51 and 0.70 at manufacturing scale); §13.11 overstated; §6 "3.1 %" and "18.8 %" on an
   unstated grid; centre points "spread through the execution order" (screening runs 11, 15, 19 of 19); Table
   7.2 has no prediction limits (builder); register text in Table 13.1 loses hyphens and capitals ("S BRX OSM",
   "producers risk", "nor"); DEV-003-06 cites "Table 11.1".
Outside scope, for the owner: under the Version 1.0 qualification rule aggregate differed between the scales at
p = 0.016 and was not investigated [registered since: DEV-003-09].

Checked and correct: identity and dates; Tables 4.1, 4.2, 2.1, 1.2, 7.1 and the §7.1 derivation; Table 3.1 and its
qualification; Table 5.1; Tables 5.2, 5.3, C.1–C.13; every effect in §5.3.3 and §9; Table 5.5, the 17 flagged
runs and the influence analysis (every PAR survives each deletion); normality; Tables 5.4, 5.8; the 15
near-equivalent models; the judgements over the NOR (9 of 81 combinations, all at pCO2 130); the design space;
Table 7.3, margins and SD ratios; Version 1.0's 13 of 20; Table 8.1; Tables 5.9–5.11; the osmolality run count;
Appendices A, B, D against the CSVs; D-002 present as registered.
