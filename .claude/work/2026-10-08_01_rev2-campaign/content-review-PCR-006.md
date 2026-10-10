# Content review run 1: PCR-006 Version 2.0 (low-pH viral inactivation report)

Judge: Claude Opus 5.5 (claude-opus-5-5), fresh context, read only `PCR-006_viral_inactivation.DRAFT.txt`
(74 pp). Returned as text; saved by the coordinator (condensed). Answers: 1 No, 2 No, 3 Yes, 4 No, 5 Yes,
6 No, 7 No.

## Q5 (coordinator's notes in brackets)
Contradicted by a table or figure: 1 "the pH PAR ends at pH 3.61, which is what moved the NOR" (circular:
3.61 is the edge under the NOR in force; under the old NOR Table 5.7 gives about pH 3.31); 2 "aggregate and
XMuLV clearance have a model that meets the adequacy criteria of PCMP-001 §7.2" (both fail the fourth); 3
Table 7.4 "PAR (set-point)" evaluated at the design centre [registered discrepancy D-001: keep, the report
presents par_table as it comes]; 4 "widened from 9.30 to 6.46 % HMW" (lowering an upper limit tightens it;
the bound moved it from 6.32 to 6.46; 9.30 is the a priori value); 5 S-VI-WC "the harshest combination within
the PAR" (120 min and 23 °C are the NOR ends; the PAR runs to 180 min and 25 °C); 6 "The PAR of a factor is
therefore wider than the slice of the design space at the edge of another factor's NOR" (wrong); 7 "Three of
them carry a squared pH term and a squared hold-time term" (Table 5.9: one lacks hold time²); 8 acidic
variants "20.6 %" vs Table 7.12 (20.3 % at manufacturing scale); 9 "no effect of pH beyond the precision of
the methods" vs Table 7.8 (−0.38, CI −0.65 to −0.11, Holm p = 0.025; a mean difference compared with the SD
of a single result); 10 aggregate results over the hold times "within the NOR in force" cover 0–120 min, not
100–120; 11 "at 90 min the set-point sat on the lower edge of its own NOR" (the old NOR 60–120 had 90 at its
centre); 12 Table 7.13 fragments "Confirmed" vs the text and the bound (0.19) above 0.15; 13 "no statement in
this report puts them at manufacturing scale" vs Table 8.1 and §7.5.3; 14 "no departure from an approved
procedure" vs PD-006-04 and the widening on three criteria where PCP-006 §7.4 requires four; 15 "no conclusion
of this report rests on a rule chosen after the data" (the hold approach, the deletion rule, the risk
acceptance of S-VI-WC); 16 the model comparison within 2 AICc units recorded as a discrepancy but not in Table
13.2; 17 no input pool result (PCP-006 §5.4) and no deviation raised, unlike DEV-006-03; 18 the hold starting
level vs Table 7.3; 19 "none of them was run at settings inside the NOR in force" (true of every run); 20 "three
things that the studies measured" (the claim across the NOR is a model prediction); 21 "63.9 % meets every
criterion" (the two modelled criteria only); 22 Table 5.4 "a block term kept" (one block, no block term); 23 the
NOR-propagated PAR described two ways (§3.5 normal draws, §7.4 NOR combinations).
Science: 24 first-order kinetics vs the log reduction not proportional to time and no pH × time interaction;
25 succinimide formation at low pH (base-catalysed; acidic variants at low pH from direct amide hydrolysis); 26
"the acid acts on the viral envelope and not on the antibody" vs §2.1 and §5.4 (CH2 unfolding); 27 "The step
sets the cumulative requirement for XMuLV" (met by three claims); 28 A-Mab concentration a GPP although the
data cannot exclude a 1.2 log10 loss at 35 g/L (margin 0.17 at the least favourable corner); 29 designs at one
concentration carry no information on a concentration effect; 30 "routine manufacture never holds the pool
longer than the upper end of the NOR"; 31 pH "the largest effect" (−0.612 vs 0.605, SE 0.123); 32 33 results with
zero scatter against a repeatability of 0.41 points, a data-integrity signal [owner question]; 33 aggregate
faster at higher concentration vs Table 7.12 (0.006 points); 34 "inactivates XMuLV by 6.60 log10" (6.60 is the
claim, 6.77 the predicted minimum); 35 the reasoning on claims beyond the ranges runs backwards.

## Q1 (15), Q2 (14), Q3 (16), Q4 (8), Q6 (13), Q7 (18)
Q1: "sets", "acts on", "governs" for statistical effects or with no direction; a short, cool hold said to
raise the lowest log reduction (inverted). Q2: "NOR-propagated PAR", "NOR as characterized" (clashes with
"characterized range"), "characterized region", "Gap", "single-batch limit/bound", "log fold", "producer
risk", "re-centred step", "harshest combination", "discrepancy", "method decision", "spiking model", a function
name, "Met over NOR (low/est./high)". Q3: sixteen filing glosses and self-certifications. Q4: Cpk 1.05 without
a verdict against §7.9; PCP-006 §7.4's own condition unmet and not recorded; S-VI-OFAT difference dismissed
after the fact; classification risk "high/low" without a threshold; S-VI-UNI2 and the hold criterion judged by
approaches set after the results; DEV-006-02 affected runs not named; the missing input pool result. Q6:
textbook glosses, repeats (the Version 1.0 limits, §7.6, the risk acceptance, the Cook's cut-off three times).
Q7: codes as subjects (PD-006-04, PD-006-07, criteria by number, "the criteria behind that prediction").

## Tables and figures
1.2 (rule codes; fused footnote letters); 2.1 (VH score 20 vs H 60; "CEX/icIEF"); 3.1 (three-row header);
4.3 (two "Verification runs", two "A-Mab concentration"; not in date order); 5.4 (full quadratic statistics
beside selected terms); 5.9 (two "Met" columns); 7.2 ("Mean predicted" over measured ranges); 7.4 (12 rows for
3 informative; precision; the D-001 column); 7.5 (colliding header cells); 7.8 (landscape, ten columns, six
notes); 7.9 (unexplained column); 7.13 ("At the edges"; "Confirmed" beside a worse bound); 13.2 (page-long
cells); Figures 5.1/5.2 (no panels named), 7.1 (colour only), 7.2 (axis to 7.02 % with data near 2 %).
Also: RSM, OFAT, DoE, HPLC, CEX missing from the abbreviations; ICH Q11 cited but not in the references;
"centre" vs "center".
