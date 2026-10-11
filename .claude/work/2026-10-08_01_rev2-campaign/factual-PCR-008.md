# Factual check of PCR-008 Version 2.0, draft run 1 (2026-10-11) — summary saved by the coordinator

Checker: Claude Opus 5.5 (ab10d2dd79f6d6afe); scratch scripts scratchpad/chk/c1–c16. D-001 present as registered (note:
§3.5.1 and §4.1 now explain coded 0 = 175 g/L, so the DISCREPANCIES.md seam note goes stale; a register entry for the
coding must not connect it to the "PAR (set-point)" column).

## Errors
1. §2.2 "Attributes of high and very high criticality are critical" (Version 1.0 text) vs PCMP-001 §3 (all 11 are CQAs,
   VL to VH); consequence for the WC-CPP rule of §9 (HCP is M-H). Use PCMP-001's statement.
2. Exec. summary / §5.3.1 "every selected model meets the four adequacy criteria": criterion 1 is n.a. for step yield
   and fragments (no term); §3.5.4 adds a carve-out sentence to the PCMP-001 §7.2 list that PCMP-001 lacks. Say each
   meets every criterion that applies; present the carve-out as the report's reading.
3. "No effect of the parameters on step yield or on fragments was detected" vs §5.2 / Table C.1 (load pH × protein load
   term for fragments, −0.064 points, p = 0.029; screening model F p 0.160; PCP-008 §5.5). Scope to the response-surface
   model and mention the screening term.
4. "…at manufacturing scale" for all outputs (exec. summary, §7.3): fragments and viral clearance have no offset; Table
   7.2 note a) hangs on the column headers (builder). Add "where an offset is known (pool host cell protein)".
5. §11 / §13.1.2 DEV-008-02 "the same in every run": the event covers both executions only; the 12 augmentation runs ran
   under SOP-2011 with the corrected value; limit the claim (block term p = 0.526 absorbs a shift).
6. §3.4 "Samples were taken from the load and the flow-through pool of every run": load results exist only for DNA and
   leached Protein A on the 28 planned response-surface runs.
7. §13.1.1 p 0.361 (all 40 runs, log) and 0.415 (28 planned, raw) from different run sets (like for like: 40 runs raw
   0.402; 28 runs log 0.284).
8. §4.3 the INV-002 success definition: lack of fit and overfitting limit on all runs with a block term (two criteria).
9. §7.5 run 8 "highest pool HCP of the planned runs at an edge … 3.63": only of the 28 planned runs (screening run 5
   35.7 ng/mg → 3.28-fold; augmentation run 33 32.8 → 3.57).
10. §5.3.3 the step-yield model on the planned runs also fails the F-test (p = 0.094).
11. XMuLV load-pH edge 7.22 vs 7.215/7.2525; the 0.13 margin for MVM (printed 7.23 gives 0.12; unrounded 7.2225 → 0.1275).
12. §9 paraphrases PCMP-001 §7.7 without "practically relevant" and the too-small clause.
13. §2.1 / §5.6 "A higher load pH moves more of the host cell protein population below its isoelectric point" is
    backwards (binding needs pH above pI); PCP-008 §4.1 words it correctly; brief §2b carries the faulty wording.
14. §5.6 bound-antibody explanation of DEV-008-01: no yield loss at the high-load, high-conductivity runs (yield terms
    p ≥ 0.19; 96.2 vs 96.4 %, 97.5 vs 97.0 %); report it.
15. Minor: step yield's method in neither Table 3.2 nor D.1; "as INV-001 finding 5 requires" (PA3); §10 item 4 hold limit
    with no value; §5.5 "every response-surface run" → "every planned response-surface run".

## Departures (none registered beyond PD-008-01 to -03; all eleven of the author's confirmed)
1 bed pressure (S-AEX-SDM, §5.1); 2 spiking-model qualification (§5.1); 3 cytotoxicity/interference controls and
detection limits (§5.4, §10); 4 load qualified on icIEF only (§7 item 2, §6.3: also HCP, concentration, pH,
conductivity); 5 DEV-008-03 names no run (§9); 6 augmentation load lot not recorded (LOT-CEX-8851 expired 2026-04-12;
S-AEX-AUG 2026-09-10 to 09-24; no lot comparison, §6.3, §9); 7 no chromatography system named (§5.2 names EQ-CHR-118
with calibration; PA3); 8 flow rate WC-CPP with no effect (§7 item 6 makes it GPP) [owner: keep, argue as judgement];
9 approaches where the plan sets no threshold (PCP-008 §7 delegates them); 10 analyses the plan does not contain;
11 coded 0 = 175 g/L for protein load (§5.5, Appendices A/B). Additional: load lots of S-AEX-UNI and S-AEX-SDM not
recorded (S-AEX-UNI began the day after the lot expired; matched load §5.1); execution records not kept (resin lot, packed
column acceptance, buffer lot and analyst per run, second-person review, retained samples, Statistics' approval of the
designs; §3.2 asserts platform control though DEV-008-03 shows a buffer lot out of range); PAR figures (MVM plotted
against load pH, the governing factor should be load conductivity, |−0.564| vs 0.539 coded; no fragments figure); the
completion rule (§7 item 8) never reported against; DNA and leached Protein A not measured on the augmentation runs;
no ANOVA or diagnostics for yield and fragments; no date for the offset estimates.

## Checked and correct
All model statistics, criterion 4 (F medians 0.855, 0.896, 0.706), Table 5.9 deletions (7.2525 edge, 94.7 %), Table
5.8, stepwise counts, augmentation checks, interaction tests (z = −2.57, p = 0.010), SDM offsets, Table 7.2, design
space 95.0 %, Table 7.3; the bound 4.27 (5.51, 3.63; full quadratic 4.28; all runs 4.27; deletions 4.21–4.58; flagged
runs 2 and 9 → 4.56 and 4.33; offset sensitivity 4.18 and 3.08), criteria 17,069 and 427; flow-rate t-tests; "more
than" clearances; capability; DEV-008-01/02/03 facts; appendices; dates, lots, IDs, Version 1.0 values; registers.
