# Factual check of PCR-010 Version 2.0, draft run 1 (2026-10-11)

Checker: Claude Opus 5.5 (a1535bfa8cf3a13a9). Nearly every number reproduces from the CSVs, config and engine. Scratch
script: scratchpad/pcr010chk/check1.py. Saved by the coordinator from the agent's hand-back.

## Errors, most consequential first
- E1 §6: "They support the movement of two parameters away from their set-points at the same time only as far as the
  bound on an interaction in Section 7.3 goes." §7.3 gives no bound (only the size an interaction would need, 4.18 pp,
  about 42 times the two effects; "The study cannot exclude an interaction, and it did not measure one"); PAR
  limitation 1 (§7.3, PCP-010 §8). Fix: the data do not support two parameters moving together; §7.3 gives only the size
  an interaction would need.
- E2 §5.5 (and exec. summary, §1.4, §10.3, §12.3): "This report applies the plateau as PCP-010 §5.5 defines it …
  therefore not met." PCP-010 §5.5 sets two conditions on conductivity ("has reached the plateau set by the formulation
  buffer and no further change is measured over the following diavolume"); the report keeps the second and applies it to
  a different quantity (residual process buffer %, one result per run), which falls 63 % per DV against a constant 5 %
  CV (config analytics.univariate_nodoe.assay.residual_buffer_pct), so the test cannot pass at any DV. §11 says the
  criterion "could not be applied as the plan states it". Fix: quote both conditions; cannot be judged as planned, not
  shown to be met; keep the residual values as the result.
- E3 §10 item 1 vs §5.5: "…delivers the drug substance consistently at its target concentration and in the formulation
  buffer." vs "This report makes no claim that the buffer exchange is complete at 7 DV" and §10 item 3. Fix: drop "and in
  the formulation buffer" or refer to the residual.
- E4 §8: "…with every process parameter drawn within its NOR (PCMP-001 §6.5)." The draw is N(set-point, NOR width/6)
  clipped to the range studied (amab_process/studies.py _sample_overrides; §3.5 is right); 0.27 % of draws per parameter
  outside the NOR, about 18 % of batches with at least one train parameter outside. Fix §8 as §3.5, with the clipping.
- E5 §13.1.2 DEV-010-02: "…it would enter the offset of the final concentration, which has no criterion at this step,
  so no conclusion depends on it." The run's aggregate would also enter the aggregate offset; Version 1.0 records that
  the correction concentrated the retentate further at its highest concentration. Dropping any one scale-down run moves
  the offset 0.020 → 0.010–0.026 pp; highest result then ≤ 0.80 % HMW, margin ≥ 4.20 pp. Add the aggregate path.
- E6 objective (iii): "met only in part" (§5.5) vs "was not established" (§12.3). One verdict: not met.
- E7 §2.1: "…expected to fall exponentially" attributed to PCP-010 §4.1; the plan says "roughly exponentially" (its
  change 7 lists the unqualified wording as a Version 1.0 error).
- E8 §5.5 vs Table 5.1: "At the set-point of 8 DV the mean residual was 0.034 %." (0.0342 is the two 8-DV runs of the
  diavolume series; Table 5.1 0.0333 for six set-point runs; all 22 runs at 8 DV 0.0332). Name the runs.
- E9 "This step does not drive" acidic-variant capability (exec. summary, §8, §12.5): inferred from non-significant
  slopes, while §5.4 says up to 1.4 pp cannot be excluded. Supportable reason: deamidation only raises acidic variants,
  away from the limiting 18 % side, and the integrated model has no UF/DF effect on them (nodoe_extras).
- E10 "Qualified for aggregate" (exec. summary, §12.1) vs Table 3.1 "n.a."; §3.1 and §11 add "under the approach of
  Section 3.1": restore the qualifier.
- E11 A-Mab p.86 citation (§1.3, §2.1, from the brief): p.86 is Table 3.18 (upstream risk assessment); "UF/DF process
  step not included in case study" is on p.114 (refs/text/amab.txt line 9742). The brief, PCP-010 §4.1 and CLAUDE.md say
  p.86, a config comment p.140. Fix at the source.
- E12 A-Mab p.47 in §8: supports "consistently cleared from the process"; "would likely not need testing" is p.57. Cite
  both or drop "and not by a release test".
- E13 §3.3 "both studies of the step": three studies (S-UFDF-SDM, S-UFDF-UNI, S-UFDF-UNI2); name the two.
- E14 §1.4 misses two reversals of Version 1.0 (buffer exchange complete across 7–10 DV, "far below what the formulation
  tolerates"; "No effect of any parameter on product quality was detected"): say they are reversals.
- Minor: §2.2 cites PCMP-001 §3 for the hold statement (it is §5); §1.4 item 5 points to §4.2 for the windows (S-UFDF-SDM
  is in §3.1); §2.3 drops "agreed with Statistics and QA" from PCP-010 §4.3; §3.5 adds "around the set-point" to the PAR
  definition of PCP-010 §8; §7.3's corner argument uses the mean, every other judgement is per run; §13.1.1 "upper 95 %
  confidence limit" is a one-sided 97.5 % limit; CEX, LMW, HPLC, UV, n.a. undefined; step-yield pure error 2.1 (text) vs
  2.08 (Table 5.1).

## Departures from the plan ("text only" = mentioned, no PLAN_DISCREPANCIES entry)
1. Skid EQ-TFF-188 instead of EQ-TFF-142: confirmed (PCP-010 §5.1, §11). §4.2 says PD-010-01 covers "its levels, its
   replicates and its skid" but the entry names no skid (the register wins); also no offset was ever estimated on
   EQ-TFF-188, the skid behind every result (PCMP-001 §7.1).
2. No pH or conductivity per diavolume: confirmed (no columns). Text only.
3. Buffer-exchange criterion not met: a result, not a departure. Underneath: the analysis is a departure (within-run
   conductivity fit replaced by a fit across runs, pH not judged, no tolerance set), with no register entry; and the
   failure has no owner acceptance while 7 DV stays the NOR edge (owner).
4. No load, pre-diafiltration or permeate results: confirmed. Text only. PCP-010 §4.2 ("what this step adds") cannot be
   met, membrane retention of the antibody unconfirmed; §12 assumption 3 (representative load within the virus
   filtration output criteria) cannot be checked and is not mentioned.
5. Run order not recorded: confirmed (no run_order column, which every DoE CSV has). Text only.
6. Load pools not identified: confirmed (PCP-010 §5.2, §12). Text only.
7. Manufacturing batches unnamed and offset date not stated: confirmed (batches 1–5, no date); the PCMP-001 §7.1
   requirement (offsets before the first characterization run) cannot be shown. Text only.
8. Qualification compared final-retentate aggregate, not the change across the step: confirmed (aggregate_out_pct only).
   Text only.
9. Approaches stated where the plan sets none: confirmed (REPORT-LESSONS §3 rule 2); the plan delegates each (§4.3,
   §5.3, §7.1, §7.2, §7.3, Table 5.1); add applying EQ-TFF-142's offset to EQ-TFF-188 results; §13.2's list leaves out
   §5.5.
10. DEV-010-01/02 name no run: confirmed; weak as a departure (event duties met in form; records not traceable to a run
    under §9, ALCOA+).
Added: A. pure error pooled from the duplicates at all 15 levels (15 df), where PCP-010 §5.5 takes it from the three
set-point replicates (presented as method, not departure); B. method variability not reported (PCP-010 §5.3: Analytical
Development reports it over the sample range; none for SEC or icIEF); C. load assumption (§12 assumption 3) cannot be
checked; D. not in the record and not mentioned: samples assayed within their stability period (§5.4), second-person
review of every calculation (§9); E. S-UFDF-UNI2 changed the design without a plan revision or Statistics review, already
recorded by PD-010-01 as unforeseen work.
For the owner: PCMP-001 Table 7.1 assumes no step after cation exchange changes aggregate; UF/DF raises it by up to
0.06 pp within the NOR, and the 5 % cation exchange criterion makes no allowance for it.

## Checked and correct
Every value in Tables 3.1, 5.1, 5.2, 7.1, 7.2, 8.1, 9.1, A.1, B.1; slopes, CIs, p, df, the four significant slopes of
15; aggregate maxima and margins (0.79/4.21, 0.82, 4.22, 22 results inside the NOR); acidic extremes (19.9, 21.7, 2.2);
corner numbers (0.71, 0.82, 4.18, about 42 times); effects across the NOR (0.07, 0.04, 0.06) and ratios (2.7 %, 1.1 %,
3 %); buffer fit (−0.995, −1.033 to −0.957, R² 0.998, 2.70, 63 %, non-overlap at every step); yield and concentration;
Cpk, means, SDs, 0/1/0 batches outside, 821 ppm, the 0.15 % bound, the DNA conversion (700 mg); DEV-010-01 bound (0.050,
0.017); dates and calibration dues; parameters, levels and classes; criticality and Tool #1, IAC and residual DNA
statements, Cpk thresholds; plan quotations (objectives i–v, decision rules, PAR limitations); Tables 13.1 and 13.2 match
the registers; Version 1.0 facts in §1.4; Figures 5.1 and 5.2 against captions.

## Could not be checked
Offset date, run order, load pool, batch identities (not in the record); whether S-UFDF-UNI2 aggregate was measured under
AMV-3011 (report, plan) or AMV-3221 (config repeatability: if the method of record, an unrecorded method departure); the
runs the two events hit and the concentration after the top-up; the sampling point of the residual process buffer;
other reports' DNA statements; DOCX, style gate and grounding.
