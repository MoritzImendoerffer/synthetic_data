# Content review of PCR-006 Version 2.0, draft run 2 (2026-10-10)

Judge: Claude Opus 5.5 (abcf289d24278f247), read only `PCR-006_viral_inactivation.DRAFT.run2.txt` (3,239 lines);
checked numbers against the tables and Appendix B and refitted the reported models from the appendix data. Saved by
the coordinator from the agent's hand-back. Quotes shortened with "...".

## Q1. Cause words with no physical cause
- F5: "The GPP class rests on the mechanism of the step for XMuLV clearance, because the concentration study cannot
  exclude a loss of clearance larger than the margin of the claim." (a data gap; mechanism never named)
- F9: "The lower end of the criterion limits it, and the low-pH hold only raises acidic variants." (the bioreactor
  level near 18 % with batch spread is the cause)
- §1.4: "...stricter than its own a priori value of 10.0 %, because the verification at cation exchange tightened
  it." (procedural; cation exchange removed less aggregate than the platform assumed)
- §1.4 item 5 and §3.5: "...because viral clearance is validated at worst-case conditions." (justifies the worst-case
  combination, not the mean)
- §2.1: "The same conditions act on the antibody."
- §4.3 "...because each of them was expected to act on XMuLV clearance..."; §5.2 "All three factors acted on the XMuLV
  log reduction." and "...because each of them changes XMuLV clearance." (statistical effects as causes)
- §5.4: "Because the pH range of routine operation is narrow and the pH of a large pool is held by acid addition and
  mixing, that trade is what makes the inactivation pH the parameter the claim is most exposed to..." (no failure
  mode, no direction)
- §7.4: "XMuLV clearance sets every range." (one edge of each range only)
- §8: "...because the drug substance carries both attributes at a small fraction of their limits after cation
  exchange." (circular)
- §9: "...because a WC-CPP is a critical process parameter whose control capability is good, not a parameter without
  an effect." (a definition)
- DEV-006-02: "The root cause is the matrix of the sample." (no cytotoxic component named)
- §7.5 item 3: "Because the narrower NOR moves routine operation toward longer holds, confirmation runs were made..."
  (product consequence missing)

## Q2. Terms that are not terms of art
- "stability study" (§1.4 item 8, §7.5 item 2, §7.5.1 title, §9, §13.2), "OFAT stability study" (Table 13.2) for
  S-VI-OFAT (compares two pH values over hold time; neither a stability study nor one factor at a time; clashes with
  the hold study S-VI-HLD)
- "The fold of a run is the load level divided by the pool level, and the log fold its logarithm." (§7.5.2;
  "clearance folds" §11; terms of art: clearance factor, log reduction value)
- "NOR-propagated PAR" (§3.5)
- "Two were retained with a bounded impact." (F10); "retained" as a disposition (Table 13.1)
- "the nominal batch of the step model" (§3.4, §7.7, §11, §13.1; "step model" never defined)
- "The configuration records three decisions..." (§7.5)
- "Two bounds apply to the region." (§6; "bound" is a statistic elsewhere)
- also: "verification bound" (§5.3.2); "counted beside the intercept" (§3.5); "in percent of the attribute" (Table 5.1
  note); "verdict" (§7.3, §7.5.1); "reads fragments high" (§1.4); "the F limit" (§5.3); "hold output" (§7.5.3)

## Q3. Sentences that file a finding
- §1.4: "...appear in no approved plan, which is finding 1 of INV-001."
- §1.4: "...so the change is discrepancy PD-006-04 from the plan, the model selection (Section 13.2)."; §3.5: "The
  change is discrepancy PD-006-04, the model selection..."
- §3.5: "That comparison is the sensitivity analysis of the model selection and is recorded within discrepancy
  PD-006-04..." (repeated §5.3.1, §13.2)
- §3.4 and §4.3: "...which is deviation DEV-006-04 (Section 13.1)."; §4.4 and §7.6: "...which is deviation
  DEV-006-03..."
- §4.4 and §7.6: "...which is discrepancy PD-006-06 from the plan, the clearance at the two ends of the concentration
  range." (same tag after PD-006-05 §7.3, PD-006-01 §7.5.1, PD-006-02 §7.5.2, PD-006-03 §7.5.3)
- §5.1: "The difference between the two designs is treated as a result in Section 5.2."
- §5.3: "The design has one block, so no selected model carries a block term."
- §5.3: "The conclusions on aggregate rest on that bound, not on the absence of the term." (and not accurate: the
  predictions come from the model without the pH term)
- §5.3.1: "...so a feature that only some of them carry is not a finding."; "...which is a sensitivity and not a
  result."
- §7.2: "...which is what qualifies the model for this output (Section 3.1)."
- §7.5: "...so these changes are changes to the control strategy of the step and not analyses."
- §7.5.3: "Pooling them would be an analysis chosen after a result, which is the pattern INV-001 was opened over."
- §7.6: "Of the four, 3 lie below the claim of 6.60 log10, which is not the claim failing."
- §9: the WC-CPP definition sentence (above)
- §13.2: "...which is what separates a discrepancy from a deviation (PCMP-001)."; "The examination of the runs with a
  large Cook's distance is not a discrepancy."
- milder: §7.2 "That is reported for information, because the claim is judged on the mean."; §7.5.3 "...which Section
  11 states as a limitation."; §7.7 "...which is what PCMP-001 §7.5 and PCP-006 §7.4 require of a model behind a
  widening."

## Q4. Criteria without basis; results not judged
- §7.3: "The approach below was set after the hold results were known, and the discrepancy entry records the study
  alone." (criterion set after the data, registered nowhere)
- §7.5.3: "The failure was accepted on its risk." (a pre-set rule failed; acceptance decided afterwards, recorded only
  as a limitation; nothing in Table 13.1)
- §9: "Neither PCMP-001 nor SOP-4001 sets a numerical threshold ... so neither phrase decides a class on its own." (CPP
  and WC-CPP rest on margins judged after the data: 0.11 pH "high risk", 16 min "low risk")
- §7.5: "A margin of 0.04 pH units is the same objection as before, so the hold-time NOR was narrowed again..." (no
  minimum margin stated; 0.04 rejected, 0.11 accepted)
- §7.6 "No effect of the concentration on the inactivation was detected..." and §13.1 "The deviation was closed by the
  confirmation study S-VI-UNI2" (no acceptance criterion; DEV-006-03 closed although the data "cannot exclude a loss of
  clearance ... that would matter")
- §7.5.1: "Whatever its origin, the difference is 1.7 % of the width of the criterion..." (yardstick made up
  afterwards for the significant acidic-variant difference, p = 0.025)
- §10 item 3: "...and Section 7.5.2 verified both on material from the step at its new pH set-point." (omits the
  fragment verification not met, Table 7.11)

## Q5. Wrong or contradicted
Major:
- Table 7.4 "PAR (set-point)" for XMuLV (pH 3.2–3.74, 98.4–180 min, 16.2–25 °C) reproduces at the design centre (pH
  3.6, 120 min, 20 °C), which §4.1 says "is the set-point of none of the three factors". At the set-points in force:
  pH ≤ 3.71, hold ≥ about 62 min, the whole temperature range. The set-point hold-time PAR (98.4–180) narrower than the
  NOR-propagated PAR (84–180) is impossible. [Coordinator: D-001 is registered here; see brief §5c.]
- §5.4: "A first-order description of the inactivation predicts both features..." (no pH × hold-time interaction, no
  curvature). First-order kinetics (LRF = k(pH, T)·t) predicts an interaction; contradicts §2.1 and §2.3.
- §9: "Without that run the attribute has no temperature effect, which would make the parameter a GPP..." (also §11
  limitation 3). Temperature raises aggregate by 0.215 points (p < 0.001, Table 5.5) in every model after any deletion
  (Table 5.10); contradicts F3 and §5.3.2.
- §5.1: "...the attribute took one value per hold time, 20.5 % at 60 min, 20.7 % at 120 min and 20.9 % at 180 min..."
  (the 33 results include the concentration study at 90 min, 20.6 %, §7.6)
- §5.3: "...so the increase is small against the scatter of the method." (0.10 points vs 0.06 repeatability, Table 7.8;
  §11 (4) says "of the same order")
- §5.3: "The design has one block, so no selected model carries a block term." (Table 5.4 note and Table 13.2 say "a
  block term kept")
- §3.3: "The studies of the re-analysis measured fragments by nrCE-SDS on every sample." (S-VI-UNI2 measured none)
- Table 7.4 lists PARs for acidic variants and fragments (basis "measured results") although §3.5, §5.3, §7.4 and §11
  (4) say an output with no adequate model sets no range.
- §13.2: "Each is work the plan did not foresee, with no departure from an approved procedure..." (PD-006-04 replaces
  the full quadratic PCP-006 §5.5 prescribed)
- §7.5: "...so each decision moved that pH." (decision 2 left it at 3.54)
- §5.4: "Direct acid-catalysed hydrolysis ... is the expected source of that increase at low pH." (the increase depends
  on hold time alone, no pH or temperature effect; 0.2 points per hour implausibly fast)
- Executive summary: "...meet the cumulative requirement for clearance of xenotropic murine leukemia virus (XMuLV), a
  log reduction of 6.60 log10." (Tables 2.1 and 7.1: ≥ 16.7 log10)
- F4: "...each set by XMuLV clearance." (also Conclusion 2 and §7.4; Table 7.6 note: the other edge is the end of the
  range studied); "The edges of the NOR in force lie 0.11 pH units, 16 min and 2.8 °C inside them" (lower pH edge
  0.10, upper temperature edge 2.0 °C, Tables 4.1, 7.6)
- §7.7: "...so the replacement reflects the shorter hold of the A-Mab NOR as well as the behaviour of the product." (at
  180 min A-Mab added 0.84 against 0.70, Table 7.13: the widening comes from the shorter NOR alone)
Moderate:
- §3.5 vs §7.4 on the NOR-propagated PAR statistic ("central 95 % of the simulated batches" vs "the 95 % prediction
  interval of a single batch")
- §3.4: "...three samples from the spiked run..." then "The two spiked samples..."
- §7.4: "...the predicted aggregate stays near 2.1 % across the whole range of hold time..." (Table 5.5: 0.47-point
  rise, about 1.8 to 2.3 %)
- §13.2: "...39.6 % without it, because without the selection the exact fit ... would have replaced the platform
  value." (§3.5: an exact fit is never adequate; Table 5.4: no adequate full model for acidic variants)
- §5.2: "The record names no cause for the difference." (DEV-006-02 cytotoxicity raises the lowest reportable output
  titre where clearance is highest, pH 3.2; were those LRFs "≥" values?)
- §5.1 and §11 (2): "The claim is therefore judged on the mean prediction..." (assay imprecision argues for a lower
  bound; §1.4 and §3.5 give another reason)
- §9: "...and on the absence of a detected effect in four runs." and "...affects no CQA ... on the evidence available,
  so it is a GPP." (§7.6 concedes it cannot exclude a loss beyond the 0.17 log10 margin; CI to −1.20; surplus 0.02)
- §5.1 "the LRF is the difference of two titres" (§3.1, Appendix D note: of log10 virus loads)
- §7.3: "...which gives 22.2 % against the upper limit of 40.0 %" (the held pool reached 23.8 %, Table 7.3; day-0
  22.2–22.8 % vs concurrent S-VI-OFAT 20.81–20.98 %, Table 7.7, unexplained)
- §10: "A hold of the neutralized pool of up to 7 days ... keeps that load inside the criteria" (§7.3 limits it to one
  pool at the old set-points)
Minor: §9 "a hold time is counted by the control system from a defined start" vs DEV-006-01 (4-min clock error);
§3.2 "...held at its set-point of 20 g/L" unmeasured (DEV-006-04); §3.3 cites "(Section 5.2)" for fragment effects
(§5.3); §1.3 "Criticality is treated as a continuum, as ICH Q8(R2) describes" (A-Mab / ICH points to consider); §8
"no action in the control strategy of this step would raise the index" (a longer hold would); Table 7.2 note a) offset
on the XMuLV row (no measured offset); Tables 2.1 and 7.4 headed "CQA" include fragments and acidic variants; §5.3
says Figures 5.1/5.2 plot residuals "against the measured results" (captions: predicted against measured).

## Q6. Machine-written
§2.1 "That history establishes the mechanism of the step ... so this characterization confirms and bounds known
behaviour."; §2.2 "The step contributes one of the three claims that meet the cumulative requirement..." (third time)
and "The low-pH hold can add to each of those three, so each is measured..."; §3.1 "Aggregate is 0.02 percentage points
higher in the scale-down model, with an interval from −0.01 to 0.05 points..." (reads Table 3.1); §3.5 "Every
candidate is fitted, and the one with the lowest AICc is taken."; §5.3 "With no residual there is no pure error for the
lack-of-fit test..." (repeat of §3.5); §5.3 "Those results depend on hold time alone, and the rise ... is 0.4
percentage points." (third time; again Appendix C); §5.3 "Below that limit a Cook's distance above 4/n ... calls for
the examination...", "Each was deleted in turn and the judgement repeated...", §5.3.2 "Each such run was deleted in
turn..." (procedure told three times); §5.4 "At acid pH the second constant domain of the heavy chain is partially
unfolded..." (repeat of §2.1); §5.4 "What the model does show is the trade between the three factors."; §6 "...and the
region studied is the knowledge space the ranges studied bound."; §7.4 "A PAR is therefore wider than the range of that
factor inside the design space at a setting of another factor outside its NOR, and narrower than the range at a
favourable setting."; §7.4 "...which is why the shaded region covers the panel and the predictions sit at the foot of
it."; §7.5 "The upper pH NOR edge sits 0.11 pH units inside the PAR..." and "The set-points sit 0.21 pH units, 26 min
and 3.8 °C inside the same edges." (reads Table 7.6); §7.5 "They were decided on the data of the studies reported
here, which means the ranges in force were chosen after the results were seen."; §7.6 three repeats ("A-Mab
concentration is a property of the Protein A pool rather than a setting of the hold...", "The designs held the
concentration at its set-point...", "No fragment result is claimed from either concentration study."); §7.6 "...because
the acid denatures the envelope of the virus whatever the concentration of antibody around it." (also §2.3, §9); §7.6
"The claim is judged on the mean prediction of the model at the least favourable NOR combination..." (fifth time);
§7.7 "PCR-003 gives the full argument by risk for the bioreactor criterion."; §7.7 "The increase is taken against the
aggregate level of the load in the nominal batch of the step model..." (five times); §9 "...gives a change of 0.63
log10, so the claim is lost at the upper edge of that range."; §11 (4) "...which is a design of 18 runs against an
increase of the same order as the scatter of the method."; §13.2 "The bound this step contributes is nearly the same
under either model, 0.56 ... and 0.56..."; DEV-006-01 "The root cause was an offset between the clocks of the two
records, a clock synchronisation error."; a label tacked on after every register number throughout.

## Q7. Cannot stand alone
F3 "...the decision to move the NOR holds and every class holds." (name each parameter and class; "the judgement
repeated" = refitted and re-judged over the NOR); F7 "This was accepted on its risk", §7.5.3 "The failure was accepted
on its risk.", §12 "...which was accepted on its risk" (who accepted it, on what grounds: load fragments ≤ 1.05 % meet
the 2.00 % limit, producer's risk, release testing detects); F10 "Two were retained with a bounded impact." (name
DEV-006-01/02 and impacts); F10, §3.4, §7.7, §11, §13.1 "...the nominal load of the step model" (name the model and
value); §1.4 "The region of the step that meets every criterion moved with it."; §1.4 "...draws it on the statistics of
PCMP-001 §6.2"; §3.1 "For aggregate the conclusion is the judgement of the selected model over the NOR." (and acidic
variants); §3.3 "...where no such interference applies."; §3.5 "One analysis is not in PCP-006, which sets no rule for
it."; Table 4.1 note "...in the table of the decisions in the section on the ranges in force." (Table 7.5); §5.3 "It
meets the fourth criterion." / "Both selected models meet the fourth criterion of PCMP-001 §7.2." / "The two regressions
pass for both."; §5.3.2 "The verification bound of the aggregate increase, which moved a criterion upstream of this
step..." and "The PARs widen with it."; §6 "...judged on the statistic it is judged on everywhere else in this report."
and "Two bounds apply to the region."; §7.1 "PCR-007 gives that analysis."; §7.3 "The claim stops at that one pool..."
and "Every criterion is met at both ends."; §7.5 "The configuration records three decisions...", "...is the same
objection as before", "The margins of the full analysis are in Table 7.6."; §7.6 "What the class of the parameter rests
on for XMuLV clearance is therefore the mechanism" (and F5); §11 (3) "...the runs the examination of PCP-006 §7.1 covers
changed no conclusion"; §12 (4) "...rest on the arguments of Section 3.1"; DEV-006-01 "The runs were retained and
analysed at their design settings." (which runs); Table 13.2 PD-006-04 "a scale-down offset taken on the scale of the
model"; Appendix D "The table of methods by study in the analytical methods section..." (Table 3.3); §8 "Three results
bound the robustness of the step."

## Tables and figures hard to read
Table 1.2 ("R1, margin 6.0", "R3"); Table 5.9 (stacked header; judgement column mixes % upper limits with log10 means;
fourth criterion left out); Table 7.2 (header "Mean predicted by the response-surface model" over measured ranges for
two rows; offset footnote on XMuLV); Table 7.4 (12 rows, 9 repeat the range studied; "PAR (set-point)" mislabelled;
"≥ 6.6" vs 6.60); Table 7.8 (11 columns, two-level header, six footnotes, mixed adjusted and unadjusted p); Table 7.9
(runs 1–5 nested in each attribute; "Runs needed" floats); Table 7.13 (statistic in "At the edges" undefined; reference
load not shown); Table 13.2 (narrow text-heavy cells over three pages); Appendix A table numbered "Table 13.3"; Figure
7.1 (caption does not describe the panels; green vs grey only); Figure 7.2 (axis scaled to the 7.02 % criterion
flattens the 0.47-point effect). Figures not in the text extract: Figures 5.1–5.4 judged from captions.

## Answers
1 No; 2 No; 3 Yes (failure); 4 No; 5 Yes (failure); 6 No; 7 No.
