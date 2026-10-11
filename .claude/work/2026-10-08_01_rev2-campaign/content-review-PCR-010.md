# Content review of PCR-010 Version 2.0, draft run 1 (2026-10-11)

Judge: Claude Opus 5.5 (af6ee751987ada1f0), read only `PCR-010_ufdf.DRAFT.txt` (47 pp); recomputed slopes, CIs,
p-values, pure errors, offsets, Cpk and tails from Tables A.1 and B.1 (Tables 5.1, 5.2, 3.1, the wash-out slope and
the Cpk values match within rounding, except as listed). Figures judged from captions. Saved by the coordinator.

## Q1. Physical cause with a direction
- "It is limited by the lower end of the criterion, which this step does not drive." (exec. summary)
- "Two of the parameters act through the same layer." (2.3)
- "It therefore sets the flux limit, and with it the TMP at which the polarization layer begins to limit the flux."
  (2.3; the cause is in the previous sentence)
- "The range extends above the NOR because more diavolumes mean more time on the skid and more passes through the
  pump." (4.1; exposure, not mechanism or direction)
- "The level of the acidic charge variants is set upstream." (5.4; a place)
- "The number of diavolumes sets the residual process buffer." (5.7, again in 10 item 3)
- "For operation, the final DS concentration and TMP are the parameters through which the step changes aggregate,
  and their control within the NORs bounds that change by the values above." (5.7, again in 10 item 2)
- "No slope of the acidic charge variants on a UF/DF parameter was significant (Section 5.4), so this step does not
  drive the capability." (8; deamidation can only raise acidic variants, away from the 18 % limit)
- "It sets the completeness of the buffer exchange, and the residual process buffer fell by a factor of 2.70 for each
  diavolume (Section 5.5)." (9)
- "TMP drives the permeate flux and so the duration of the operation (Section 2.1)." (9; only below the limiting flux)
- "It sets the concentration of the drug substance, which followed it with a slope of 0.998 (Section 5.6)." (9)
- "The studies show how the three parameters of UF/DF act on the drug substance within the ranges studied." (11)
- "The number of diavolumes sets the residual process buffer, which falls by the factor that free passage of the
  buffer species predicts." (11; mildest)
- "…the possible interaction of TMP and the final DS concentration through the polarization layer is the one that
  matters for aggregate." (11; no direction)
- "The tightest, for the acidic charge variants, lies between the minimum and the target of PCMP-001 and is set
  upstream of this step (objective v)." (12)
- "At high antibody concentration, Donnan and volume-exclusion effects can leave the pH and the excipient levels of
  the retentate off the values of the buffer." (2.1; no direction)
- "Section 2.1 expected a rise with the number of diavolumes and the final DS concentration and a fall with TMP,
  through the time in solution." (5.4; exposure, not deamidation)

## Q2. Terms of art
- "study event" and "discrepancy from the plan" (judge: coined; terms of art protocol deviation / amendment)
  [coordinator: owner's decision of 2026-10-10; keep, defined once where the record section opens]
- "The record of S-UFDF-UNI2 gives one result of the buffer exchange per run, the residual process buffer as a
  percentage of the process buffer, and no pH reading (Section 3.4)." (no defined measurand, species or method;
  Table 3.2 lists none; 0.0001 % cannot come from the conductivity the plan names)
- "…a plateau of the formulation buffer at or below 7 DV…" (means retentate conductivity and pH at the buffer values)
- "…which below the flux limit drives more permeate…" (limiting flux, pressure-independent regime)
- "2. The NOR-propagated analysis of PCMP-001 §6.4 needs a fitted multivariate model and was not performed."
- "PCMP-001 §7.5 verifies a platform worst case on the response-surface model of the step that performs it, …"
- "PCP-010 §4.3 extends a study to the combination of edges…" (corner point)
- headers "Met over NOR" (Table 3.1), "Performance output it sets" (Table 9.1)

## Q3. Filing sentences
- "The A-Mab case study gives nothing for this step, so the effect is a finding of this campaign." (exec. summary)
- "The effect of the final DS concentration and of TMP on aggregate that Section 5.3 reports is a finding of this
  campaign." (2.1)
- "That was a departure of Version 1.0 from its plan." (1.4, change 2)
- "It answers the absence of results in Version 1.0." (4.2)
- "This is an expectation that the study did not test." (5.7)
- "6. The two study events change no conclusion, and the study S-UFDF-UNI2 is the discrepancy PD-010-01 from the
  plan." (12)

## Q4. Criteria and results
Pass: aggregate ≤ 5 % HMW and acidic variants 18–40 % (register basis), met at every level; Cpk minimum 1.00 and target
1.33; α = 0.05 and the pure-error rule; the buffer-exchange criterion reported as not met.
Flagged:
- "This report judges both changes small against the criterion." (5.3) and "...it judges every change small against
  its criterion." (7.2): no threshold; a judgement after the data
- "This report judges that no attribute approached its criterion at an edge." (7.3): the corner trigger has no
  threshold, so skipping the corners was decided after the data
- "This report judges that effect too small to move aggregate appreciably within the PAR, so under PCMP-001 §7.7 it
  does not by itself make TMP critical." (9; same for the final DS concentration)
- "This report therefore takes as the conclusion over the NOR whether every individual aggregate result at a level
  inside the NOR meets the criterion at manufacturing scale." (3.1): a qualification rule written after the data, not
  registered
- "The residual process buffer therefore changed measurably with each further diavolume across the whole range
  studied, and it reached no plateau within it." (5.5): "measurable" defined after the data (non-overlap of
  duplicates), against "sets no tolerance after the results"
- "Objective (iii) is met only in part." (5.5) vs Conclusion 3 "was not established"
- "The lower edge of the diavolume NOR, 7 DV, therefore rests on the measured residual and not on a demonstrated
  plateau." (10): a failed criterion at the NOR edge carried into the control strategy with no disposition

## Q5. Wrong or contradicted
Material:
1. "On that definition the residual process buffer shows no plateau at or below 7 DV. The buffer-exchange criterion
   of PCP-010 §7.2 is therefore not met." (5.5; exec. summary, 1.4, Conclusion 3): constant-volume diafiltration with
   free passage gives an exponential (slope −0.995); an exponential never plateaus on an assay that resolves it, so
   the test fails at any DV; the plan measured conductivity and pH, and at 0.09 % residual (Table A.1, 7 DV) the
   conductivity would not differ from the buffer. Supportable verdict: cannot be judged as planned. Figure 5.2 on a
   log axis can only show a straight line.
2. "The acidic charge variants have a Cpk of 1.05, between the minimum and the target." (8): Table 8.1 uses a simulated
   DS mean of 22.4 %; all 30 measured final-retentate results lie between 19.9 and 21.7 % (Table A.1; set-point mean
   20.6 %, Table 5.1), every one below the simulated mean; at the measured level with the simulated SD, Cpk ≈ 0.62.
3. "A KPP affects process performance, such as yield or concentration, and has no effect on a CQA within its range."
   (9) vs Tables 5.2 and 9.1: TMP (p = 0.015) and final DS concentration (p < 0.001) have significant aggregate effects
   and are KPPs.
4. "Table 13.2 lists the discrepancy from PCP-010 in the register of this report." (13.2): the text names seven
   departures Table 13.2 omits: no load, pre-diafiltration or permeate samples; no conductivity series and no pH; the
   wash-out fit across runs instead of per run; run order not recorded; load pool not identified; manufacturing-scale
   batches not named; qualification on final-retentate aggregate instead of the change across the step.
5. "They support the movement of two parameters away from their set-points at the same time only as far as the bound
   on an interaction in Section 7.3 goes." (6) vs §7.3 ("The study cannot exclude an interaction, and it did not
   measure one") and limitation 1.
6. "TMP drives the permeate flux and so the duration of the operation (Section 2.1)." (9) vs §5.7 ("cannot say on which
   side of the flux limit the set-point lies") and §4.1; flux measured only at 12 psi (Table B.1): the KPP basis for
   TMP is unsupported.
7. "…so this step does not drive the capability." (8) vs §5.4 (cannot tell how much deamidation the step adds).
8. "They are controlled within their NORs so that the step delivers the drug substance consistently at its target
   concentration and in the formulation buffer." (10) vs §5.5 ("no claim that the buffer exchange is complete at
   7 DV") and no pH reading.
9. "All 22 aggregate results inside the NOR met the criterion in all three cases, so the model is qualified for
   aggregate." (3.1; Conclusion 1) vs Table 3.1 "Qualified: n.a."
10. "The intervals of all four offsets include zero, and the model is qualified for aggregate under the approach of
    Section 3.1." (11): zero inside an interval from 3 vs 5 runs is not equivalence (yield −2.4 to 1.6, Table 3.1);
    brings back the significance-test logic change 4 removed.
11. "The run was topped up, as the record states, and retained." (13.1.2; Table 13.1, exec. summary): adding volume to
    a retentate below target lowers its concentration further; as written the action does not fit the event.
Minor: "...with every process parameter drawn within its NOR (PCMP-001 §6.5)" vs §3.5 (untruncated normal, about 0.27 %
outside); "The lowest result was 19.9 %, at the set-point condition of the transmembrane pressure series" (also 19.9 %
at 80 g/L, Tables 7.1, A.1); "The study measured no change across the step at the set-point condition, because the
record holds no load result." (reads as measured zero); residual DNA "0.001 ng per dose" (check unit) [coordinator:
A-Mab's claimed range]; "Fragments form during the harvest hold (PCR-004) and are tested at release." (10; also in
culture and by hinge hydrolysis, §2.2); "The largest of them, −0.5 percentage points ..., is smaller than the margin of
1.9 percentage points ..." (7.2; use the confidence bound −1.4, Table 5.2); "For the buffer exchange it rests on the
passage of the buffer species through the membrane, which depends on the number of diavolumes and on the membrane and
not on scale." (3.1; sieving is a property of membrane and species); "The range extends above the NOR because pressure
above the flux limit compacts the polarization layer without raising throughput." (4.1); Table 7.1 0.72 % at 7 DV vs
Table A.1 0.75 − 0.02 = 0.73 (also 9 DV, 15 psi); "From the mean of the set-point runs at manufacturing scale, 0.71 % HMW,
the two slopes give 0.82 % HMW at the corner ..." (Table 5.1: 0.74 − 0.02 = 0.72; 4.18/(0.82 − 0.71) ≈ 38, not "about
42 times"). Open: after "the cation exchange criterion makes no allowance for that increase", "No criterion was
changed" (a CEX pool at 5 % could give DS above 5 %, no disposition); the executive summary omits that every result came
from a second skid never compared with the first.

## Q6. Machine-written
"The studies show how the three parameters of UF/DF act on the drug substance within the ranges studied."; "The
attributes that other steps control are named by their reports."; "Table 3.3 lists the methods for size variants by
designed study, and this step has no designed study to list."; "Below the target it leaves the drug substance below the
concentration that the drug product program expects."; "Version 1.0 narrated an outcome for the three parameters
without a recorded result. This version reaches its ranges and classes on recorded results."; "It answers the absence of
results in Version 1.0."; "The step met both of its criteria at every level of the range studied of every parameter
(Section 7.2)."; "The study cannot exclude an interaction, and it did not measure one."; "Each PAR is the range studied
and reaches both edges of it, so no claim is made beyond the range studied (PCMP-001 §7.6)." (also 4.1, Table 7.2
caption, limitation 3); "This report sets no threshold after the results." / "This report sets no numerical threshold
after the results." (five times, each before a judgement made after the data); repeated "For operation, the final DS
concentration and TMP are the parameters through which the step changes aggregate ..." and "The number of diavolumes sets
the residual process buffer" (three times); "No conclusion therefore rests on runs added after a result was known."
(13.2); "the record holds / does not give / does not name" 16 times, "therefore" 27, "narrated" 5, "4.21 percentage
points" 4.

## Q7. Cannot stand alone
"Objective (iii) is met only in part."; "Every attribute result of every level met its criterion, so every level is
acceptable under the first decision rule of PCP-010 §7.3."; "Cpk is judged against the target and the minimum of
PCMP-001 §7.9."; "2. The NOR-propagated analysis of PCMP-001 §6.4 needs a fitted multivariate model and was not
performed."; "PCMP-001 §7.5 verifies a platform worst case on the response-surface model of the step that performs it";
"Aggregate stays with SEC, where the interference that led to AMD-001 does not apply (PCMP-001 §7.8)."; "Aggregate is
measured by SEC in both studies of the step (PCP-010 §5.3)."; "PCP-010 §4.3 keeps a rule of Version 1.0 for this case.";
study, event and skid codes alone ("S-UFDF-UNI ran from 2026-03-09 to 2026-03-27 on EQ-TFF-142."; "The windows of
S-UFDF-SDM and S-UFDF-UNI closed before the next calibration of EQ-TFF-142, which was due on 2026-04-22."; "DEV-010-01
names the skid EQ-TFF-142, on which S-UFDF-SDM and S-UFDF-UNI ran."; "S-UFDF-UNI2 ran on the second skid EQ-TFF-188 and
not on EQ-TFF-142, where the offsets were estimated."); "6. The two study events change no conclusion, ..."; "The ranges
and classes of this report are the ones against which the PPQ batches of PTP-001 will be run at the receiving site
(PCMP-001 §2)."; "…only as far as the bound on an interaction in Section 7.3 goes."; "Their control within the NORs
bounds that change by the values of Section 7.1." (10) and "…by the values above." (5.7); "Two of the parameters act
through the same layer."; "The A-Mab case study gives nothing for this step, so the effect is a finding of this
campaign."; "For aggregate the two agreed for every parameter (Section 5.3)." Abstract subjects: "The record holds no pH
reading, so the pH part of the criterion cannot be judged." (16 such); "PCP-010 §5.2 loads every run from a single pool
of the virus filtration step, …"; "It answers the absence of results in Version 1.0."; "The study changed the basis of
the report."; "The aggregate effect also bears on the criteria upstream."; "The performance effect on which the class
rests therefore comes from the mechanism of the step and not from this study."

## Tables and figures
Table 3.1 (run counts in merged cells between rows; "no model a)" and "n.a. a)" in every row; footnote defines a "Met
over NOR" test never applied; "n.a." contradicts "qualified"; "models" for one model); Table 3.3 (empty, "no DoE");
Table 5.2 (15 rows; one column mixes %, points and g/L at 0.0001–0.1; aggregate as measured while judgement tables are
at manufacturing scale; "Slope significant" repeats p); Table 7.1 (aggregate offset-corrected next to acidic variants as
measured; highest value vs range; degenerate ranges "20.8–20.8"; "Both criteria met" Yes in all 15 rows); Table 8.1
(DNA in ng/dose with five decimals and SD to one figure, Cpk 7.30 not recheckable (6.9 from displayed); counts out of
2,000 beside per-million tails; verbal categories as values); Table 9.1 (caption gives the class, no class column;
p-values wrapped in attribute cells; TMP performance cell a fragment); Table 13.2 (one row of sentences in two- or
three-word lines; the paragraph below repeats it); Figure 5.1 (aggregate as measured, criterion off the scale);
Figure 5.2 (log axis: an exponential is a straight line by construction); Table 5.1 minor ("Set-point runs," in four
headers; residual buffer to five decimals).

## Answers
1 No; 2 No; 3 Yes; 4 No; 5 Yes; 6 No; 7 No.
