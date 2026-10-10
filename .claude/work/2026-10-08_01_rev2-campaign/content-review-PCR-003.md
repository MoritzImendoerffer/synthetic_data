# Content review run 1: PCR-003 Version 2.0 (production bioreactor report)

Judge: Claude Opus 5.5 (claude-opus-5-5), fresh context, read only `PCR-003_bioreactor.DRAFT.txt`.
Returned as text; saved by the coordinator (condensed; quotes kept where a fix depends on them).
Answers: 1 No, 2 No, 3 Yes (glosses present), 4 No (the step's own criteria and verdicts pass), 5 Yes,
6 No, 7 No.

## Q5, strong (coordinator's notes in brackets)
1. "The production bioreactor is the only step of the A-Mab drug substance process at which product quality
   attributes are formed." vs Table 7.1 (low-pH increases) [registered discrepancy D-002: keep].
2. Afucosylation "falls with culture duration ... consistent with ... the donor supply and the Golgi function
   have declined" (backwards: less GDP-fucose and weaker Golgi processing raise afucosylation).
3. "The augmentation repeats no setting" vs Tables B.1 and B.2 (runs 29, 33, 35, 41, 44 repeat runs 2, 5, 7,
   11, 16).
4. Tables B.1 and B.2 factor legend "C, culture duration. D, CO2 partial pressure" vs Table 4.2 (C is pCO2,
   E is duration) and "a factor carries the same letter throughout the report".
5. The augmentation rule "decided on 2026-09-02, before any further run was made" vs Table 4.3 (the
   osmolality study started on 2026-09-01; 16 cultures from 2026-09-03 need a seed train expanded earlier).
6. "The response-surface design ... was made later and is not affected" (DEV-003-01) vs Table 4.3 (the same
   probe EQ-BRX-205, the same next calibration date, no recalibration recorded).
7. DEV-003-02 "The record does not say which of the three screening centre points was affected" vs the mass
   reconciliation that detected it and the re-assay of "the glycan results of the batch" (and AMV-3010 is the
   validation report, not the procedure).
8. "with almost no margin in culture pH and pCO2" vs §7.3 (pH margin 2.25 SD; only pCO2 has almost none).
9. "Every result ... has the offset applied" vs Table 8.1 (drug substance means for afucosylation, high
   mannose and acidic variants 7.98, 5.99, 22.4 % below the manufacturing-scale set-point values of Table
   7.2, 8.67, 6.40, 22.8 %; the integrated model looks unoffset, and the acidic-variant Cpk 1.05 rests on it)
   [check the engine].
10. Dissolved oxygen a KPP on a mechanism that §2.1 says gives no oxygen limitation across the range.
11. "Section 2.1 expects a higher basal medium concentration to raise growth and titre" (it does not).
12. "Without it the criteria ... would differ ... and no conclusion would change" vs Table 5.4 (high mannose
   has no adequate full model, gap 0.25).
13. Table 13.1 lacks the univariate escalation of initial viable cell concentration and the missing equipment
   records [registered since: DEV-003-07, DEV-003-08].
14. The ICH Q8(R2) PAR definition ("keeping other parameters constant") vs the NOR-propagated PAR.
15. "A PAR for each response-surface parameter and each attribute" vs objective 3 (only where the model has a
   significant term).
16. "Its results have no scatter and the model fits them exactly" (measured icIEF results cannot be
   scatter-free; precision 2 %) [the low-pH acidic-variant exact fit: owner question].
17. "No conclusion of this report therefore depends on a single flagged run" (the influence analysis re-judged
   only the conclusion over the NOR, not the PARs, the design space or the capability).
18. Host cell protein and DNA "judged at those steps and at the drug substance" vs §2.2 (DNA judged on the
   drug substance only).
19. PPQ "confirms" the ranges (PPQ runs at target).
20. Wrong cross-reference (§7.4 for §7.3).
Moderate: 21 the purification steps "do not separate charge variants" (CEX separates by charge); 22
osmolality a WC-CPP with no PAR and failing at its NOR high; 23 "They differ in single terms"; 24 the log-scale
factor e^2b ignores interactions; 25 "routine manufacture never holds longer than the NOR"; 26 "The simulation
varies osmolality" (no model has an osmolality term); 27 high-mannose precision; 28 the univariate escalation
timing; 29 duplicates "could not have been tested" otherwise; 30 17 cases on 13 runs; 31 Table 7.3 rounding
(7.02, 131); 32 the DEV-003-04 cell vs the predicted median 18.39 %; 33 afucosylation model 0.68 above the
centre points, not discussed; 34 DNA ≤ 0.001 ng/dose [A-Mab's claimed acceptable range; no change].

## Q1 (15), Q2 (10), Q3 (13), Q4 (6), Q6 (24), Q7 (25)
Q1: "sets", "acts on", "brings" without mechanism or direction (culture and host cell protein; Golgi enzymes;
afucosylation; pH/temperature/pCO2/osmolality; deamidation; "the cells themselves are the same"; pCO2 and
osmolality; probe drift root cause "between calibrations"). Q2: "single-batch limit", "NOR-propagated PAR",
"corner judgement", "age-dependent glycoforms", "Man5" for total high mannose, a function name in Table 13.2,
"producer's risk", "spread trend", "range of experience". Q3: filing glosses (fragments; "a departure from
PCMP-001 §5"; "It is not the model used"; Cook's distance; "reported as observed"; "producer's risk"; patient
and producer; the WC-CPP re-filing; "standard practice"; the duplicates). Q4: alarm limits without values;
acidic variants at harvest without a limit or action; "verified by three determinations"; normality judged by
eye; classification without a threshold (stated); the NOR narrowing set aside "impractical". Q6: garbled
sentence on the Version 1.0 PARs; fragments out of scope four times; restatements; the risk acceptance four
times; "821 per million" three times; tautologies. Q7: codes as actors (INV-002, DEV-003-0x, criterion
letters), "this picture", "The change is argued by its risk".

## Tables and figures
Table 3.1 (counts in one row; differences and ratios in one column); 4.3 (merged probe cells); 5.2 (27 rows;
"PCO2"/"pCO2"); 5.4 (12 columns; scale not stated); 5.8 (log and percentage units mixed); 5.9/5.10 (different
scales side by side); 5.11; 7.3 (18 of 20 rows repeat the range studied; no NOR column); 8.1 (DNA SD
"< 0.0001"); 13.1 (typos "S BRX OSM", "producers risk"); 13.2 (30-line cells; a code identifier); B.1/B.2
(factor letters); 3.3 (carries almost nothing); Figure 6.1 (red/green only); Figure 5.6 (before the offset).
