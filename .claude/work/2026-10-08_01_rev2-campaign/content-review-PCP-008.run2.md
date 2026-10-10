# Content review run 2: PCP-008 Version 2.0 (anion exchange plan)

Judge: Claude Opus 5.5 (claude-opus-5-5), fresh context, read only `PCP-008_aex.DRAFT.run2.txt` (plus one
simulation of the Cook's cut-off). Returned as text; saved by the coordinator (condensed). Answers: 1 No,
2 No, 3 Yes (two minor), 4 No, 5 Yes, 6 No, 7 No. Resolutions: `feedback-PCP-008.final.md`.

Most important (judge's ranking): the coding rule cannot hold for protein load (set-point 200 in 50–300;
Version 1.0 text, D-001); Cook's 4/n fails about 99 % of correct models with 15 terms on 28 runs (6.2
flags on average), and read with "prediction only if it passes the four conditions" almost no model could
be used; §13 keeps Version 1.0 text this revision makes false; contradictions between sections (both worst
cases verified, what a model may be used for, NORs set from an analysis that takes the NORs as input, a
two-sided Cpk wording for one-sided criteria).

Amendment scope: "No two windows overlap."; the spiked-run sentence; "The record names no instrumented
system"; Table 11.1 note a); "no verification at another step has changed them" (borderline).

Q1: yield in flow-through ("because the product is not retained", circular); residence time as a
mechanism; the flow-rate assignment; the highest ranks of RA-001; "attributes are set by the preceding
step"; the spiking model; the "govern"/"acts on" family for statistical effects.
Q2: "governing parameter" (two senses); "single-batch limit"; "frozen Version 1.0 text"; "release profile"
of an intermediate; "limit on overfitting"; "how far mass transfer brings each species"; "small, highly
charged impurities"; minor labels.
Q3: "not by a test of equivalence"; "rather than after".
Q4: "well inside" and "high risk" without thresholds; the univariate PAR statistic for flow rate; leached
Protein A clearance measured on 28 runs but not reported against the 10-fold value; the statistic at each
NOR combination; DNA and leached Protein A have no criterion at this step (only implied).
Q5 (20 contradictions, 7 science points): the coding rule (Table 6.1); §13 vs §1.1 and Table 11.1;
"prediction only if four conditions" vs item 7; "verifies them" vs item 7; NORs set from the second
analysis (circular); two-sided Cpk; "no instrumented system" vs EQ-CHR-118 and §9; "test of equivalence"
vs a test for a difference; "no class for a CPP" vs the WC-CPP class; Table 3.1 omits INV-002; the
fragments objective vs the flow-rate runs; viral clearance in the single-batch objective; "does not vary
the quality of its load"; protein load "well above the set-point"; the conductivity ranges vs buffer
preparation; mass transfer of virus and DNA vs "robust"; the flow-rate reason vs §4.3; load
representativeness vs adjusted pH and conductivity; complexed ligand fragments vs the 10-fold clearance;
clearance vs the modelled pool HCP; Cook's 4/n; the pH × Equil/Wash-1 mechanism; the quadratic-terms
mechanism overstated; pooling reversed; assay precision bound incomplete; DNA ≤ 0.001 ng/dose
(coordinator: A-Mab's claimed acceptable range, met through clearance); virus "large" vs "small".
Q6: thirteen restatements and padding items. Q7: twenty stand-ins and codes.
Tables: 1.1 (R1, R3, no R2; split cell; virus row order), 3.2 (merged Type cells), 4.1 (wrapped headers;
score 20 for viral clearance explained only in a note), 8.1 (header without its formula; the rounding note;
8.60 vs 8.6), 11.1 (S-AEX-SUP description; key fact in a note; spiked runs not shown); minor 6.1, A.1, B.1,
revision history.
