# Factual check of PCP-008 Version 2.0 (draft of 2026-10-10)

Checker: Claude Opus 5.5 (claude-opus-5-5). Returned as text; saved by the coordinator (condensed).
Every number checks out against the tables, brief, CSVs and config.

## Errors, most consequential first
1. **Item 7's widening rule is not met by the model the criteria in force rest on** ("Where that bound is
   above the platform value and the model passes the adequacy conditions of Section 5.5, the bound
   replaces the platform value"): the selected AEX HCP model fails condition 4 (run 9 Cook's 0.101 against
   0.100 on 40 runs; runs 2 and 9 on the 28 planned runs). Resolution: shared item 1 (PCMP-001 §7.5 names
   the three tests; condition 4 does not decide a widening; the report examines it; the INV-002 verifier
   found the bound still 4.56 and 4.33 against 4.00 with each flagged run deleted).
2. **"No approved plan contained these criteria"** vs the frozen Version 1.0 PCP-008 §7 (21.7 ng/mg with a
   safety factor of 4.6; XMuLV 3.78 and MVM 3.28). Shared item 2.
3. **"Version 1.0 did not measure fragments at this step" (change 4) is false**: S-AEX-SUP has SEC
   fragment results on all runs; S-AEX-SCR and S-AEX-RSM (still under Version 1.0) have nrCE-SDS on all
   runs. Fix: "Version 1.0 did not list fragments as a response of this step and did not judge them."
   Table 1.1 note b ("The attribute was added at Version 2.0") is builder text: what Version 2.0 added is
   the criterion (coordinator: the builder note will be checked).
4. **Change 9 rewrites a Version 1.0 design statement after the data** ("The centre points of both
   designs therefore run at the centre of the protein load range"; Appendix A "0 is its centre"). Version
   1.0 §5.5 and its appendix said "the set-point is 0"; protein load ran at 175 g/L at every coded-0 level
   and never at the 200 g/L set-point: a departure PCR-008 records. PCMP-001 Version 2.0 sets no coding
   rule. Fix: keep the Version 1.0 statement; PCR-008 records the departure.
5. **The classification rule (item 6) was rewritten and is not listed** (Version 1.0: WC-CPP "acts on a CQA
   and is held well inside its acceptable range", GPP "no demonstrated effect", no CPP class). Shared item 4.
6. Low priority: §5.1 "The other outputs have their offsets recorded" (DNA and leached Protein A are below
   the LOQ at both scales; bed pressure not measured; plate count and asymmetry measured in place of peak
   shape; PCMP-001 §7.1 asks each plan to name the manufacturing-scale data set); EQ-CHR-118 (no equipment
   in the chronology for S-AEX studies; PCMP-001 Table 5.1 lists only S-CEX-RSM); item 5 and objective 2
   name no design-space statistic (shared item 5); "the four conditions of PCMP-001 §7.2, which carry
   numerical limits" (condition 4 has none: "three of which"); "Aggregate is therefore not a response"
   (the same premise holds for fragments, which are measured); §1 output list omits DNA and leached
   Protein A; change 8 omits the move from a step capability estimate to the integrated model.

## For PCR-008 (rules the record breaks)
MVM governing parameter: the plan's rule (largest main effect in the RSM model) gives load conductivity;
`D.governing_factor` reads the screening effects and gives load pH. Condition 4 failures (PD-008-03; the
report also states whether the HCP bound depends on a single run, PCMP-001 §7.5). Univariate: both ends in
duplicate plus one spiked run, no centre run. Bed pressure not measured. D-001 worded as §5c directs.

## Checked and correct
Dates; Table 6.1; design structure and appendices; criteria (Table 1.1, Table 8.1, item 4 values, claim sums
16.72 and 8.62, folds 4 and 10); Table 4.1; statistics (α, 0.20, 4/n = 0.14, 90 % interval, 2,000 batches,
NOR/6, 81 points, seed 20240724, Cpk 1.33 and 1.00); methods; PCMP-001 citations; Version 1.0 described
correctly in changes 1, 2, 3, 5 and 7; Version 1.0 design kept; no later study described.
