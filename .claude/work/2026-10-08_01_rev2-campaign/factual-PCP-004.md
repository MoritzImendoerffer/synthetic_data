# Factual check of PCP-004 Version 2.0 (harvest and clarification, Step 4)

Checker: Claude Opus 5.5 (claude-opus-5-5), 2026-10-10. Returned as text (the harness blocks subagent
report files); saved by the coordinator. Sources: the document text, brief, config, CSVs, frozen
Version 1.0 plan, report and master plan, rendered PCMP-001, STORY_BIBLE §9b. Scratch scripts in the
session scratchpad `fact004/`. Every number in the document is correct; the errors are logic,
consistency and §9b.

## Errors, most consequential first

1. **The offsets are said to decide nothing, which misapplies PCMP-001 §7.1.** §5.1: "No output of this
   step has an intermediate acceptance criterion (Section 7). For an output with no criterion at the
   step, PCMP-001 §7.1 requires only that the offset be recorded, and no conclusion depends on it."
   Table 11.1 footnote likewise. "No IAC" is not "no criterion at the step": the plan's own §7 criterion
   1 (impurity release) judges host cell protein and DNA in the clarified harvest, and §5.1 lists both
   among the outputs compared at both scales; PCMP-001 §7.1 items 2-3 then require subtraction and the
   two-ended qualification test; item 4 ("record only") covers outputs with no criterion (step yield).
   §5.1 says the model "is expected to understate lysis", the direction in which a scale-down pass of
   criterion 1 is not conservative. PCMP-001 §5 and §7.1 decide qualification on a response-surface
   model, which this step lacks. Change 2 says the model "is qualified by its offset" while §5.1 and the
   footnote remove every qualification decision; objective 1 dropped "qualify". Fix: step yield, centrate
   turbidity, solids removal and filter pressure have no criterion (offsets recorded only); host cell
   protein and DNA are judged by criterion 1, and since PCMP-001 §7.1 decides on a response-surface model
   the plan sets no rule for them; PCR-004 states its approach as a discrepancy. Amend the footnote.
2. **"The step forms no quality attribute" contradicts PCMP-001 Version 2.0 and the register.** §1 and
   §4.3. `cqa_register.csv` has fragments_lmw set_by=harvest ("clipping in culture and during the
   harvest hold"); brief §2 lists fragments under "CQAs this step SETS"; PCMP-001 Table 1.1 "where
   fragments form during the harvest hold", §3 and Table 3.1 "Formed or set at Harvest and
   Clarification". §4.2 wording is accurate ("None of the four is formed by the centrifuge or the
   filters"). The absolute wording comes from `_pcpkg.UNIT_OP_ROLE` (Version 1.0 role text), which
   disagrees with brief §2 and PCMP-001 Version 2.0. Fix the sentence (the centrifuge and filters form
   no attribute; fragments form in culture and while the clarified harvest is held, outside this plan)
   and §4.3; and fix `UNIT_OP_ROLE` (coordinator).
3. **Objective 4 rewritten from Version 1.0, not listed.** Version 1.0: "Establish whether the step
   alters the size-variant profile of the antibody"; Version 2.0: "...changes the high molecular weight
   (HMW) content". Fragments are a size variant, now assigned to harvest, and S-HAR-UNI did not measure
   them (`method_plan.csv`). Narrowing after the data hides the gap. Restore the Version 1.0 wording.
4. **§4.2 says the step does not clear host cell protein or DNA**, against the plan's own text that the
   depth filter media adsorb DNA (§4.1, §5.3, §5.5, risk 5, Table B.1; brief §2b supports partial
   removal). Fix: "The step is not credited with clearing them. The depth filter media adsorb part of
   the DNA (Section 4.1), but no clearance is claimed for it."
5. **PCMP-001 §7.1 asks for outputs, runs per scale and the manufacturing-scale data set; the plan gives
   only the outputs, and the record holds no harvest qualification** (no S-HAR-SDM in the chronology or
   PCMP-001 Table 9.1, no rows in `sdm_qualification.csv`, `D.sdm_offset("harvest", ...)` None, PCMP-001
   §5 lists no harvest output). Fix: state that Version 1.0 set no number of runs and named no data set,
   and that this plan sets none (PCR-004 records it).
6. **Fragments added to the attributes in scope, not listed as a change.** §4.2 "Four quality
   attributes" (Version 1.0: three); AMV-3020 added to Table 3.2. The register entry is new at Version
   2.0 ("sponsor-set (Rev 2.0)"). Say so in change 3.
7. **Smaller Version 1.0 rewrites and additions, not listed.** (a) Criterion 1 "resolution of the
   method" became "precision" (restore); (b) §5.5 dropped the clause that the regressions "will be
   judged on those" (R² and residual standard error) (restore); (c) §7 adds a generic deviation versus
   discrepancy rule (list it or drop it); (d) the verification rule of PCMP-001 §7.5 appears in §7 but
   not in the §1.1 list. Until fixed, §1.1's closing "otherwise kept as Version 1.0 stated them"
   overstates.
8. **Risk 1 lists five compared outputs where §5.1 lists six** (add the removal of solids).
9. **§9 says PCMP-001 §9 "records them for every study of the campaign"**: Table 9.1 holds 31 studies,
   the chronology 43. Fix: "PCMP-001 Table 9.1 records the window of S-HAR-UNI".
10. **§4.2 "attributes of high and very high criticality are called critical"** is not in PCMP-001
    Version 2.0 (criticality "a continuum"; the convention was dropped at Version 2.0). Delete.
11. **§5.1 "The qualification does not compare three outputs"**: the column pressure and cycle yield of
    the turbidity series are also not compared. List them or say they are responses of a fixed test.
12. **Change 3 "fragments are measured by nrCE-SDS ... in every study at every step"**: S-HAR-UNI2 ran
    after AMD-001 and measured no fragments. Use §5.3's wording ("the method for fragments at every step
    is nrCE-SDS").

Notes (not errors): the revision reason "a priori intermediate acceptance criteria" does not apply to
this step (generic `reason_plan`); harmless unlisted edits (two corrected Version 1.0 slips, scope item
5, risk 6); Table 6.1 prints "9,000" beside "6000–12000"; criterion 1 also depends on the qPCR
precision, which the plan does not give.

## Checked and correct

Title block, revision history, dates (approval 2025-10-20 before S-HAR-UNI 2025-11-03 to 2025-11-21;
INV-001; AMD-001 after S-HAR-UNI; S-HAR-HLD and S-HAR-UNI2 after INV-001 closed); every parameter value
(Table 6.1, A.1, objectives, §6.1, criterion 2 10 NTU, the 6,000/12,000 g bracket); derived claims (all
univariate; range beyond NOR at both ends for rcf and depth filter load, only at the top for turbidity;
four distinct turbidity levels; three of five levels are control-strategy values); Tables 4.1, 5.1,
5.2, 3.1, 3.2; criteria (no harvest IAC, no platform worst case, bioreactor criteria carried through,
nothing to verify, no Version 1.0 criterion at this step); fragments facts; every PCMP-001 reference
except error 9; §1.1's description of the replaced Version 1.0 rules; the Version 1.0 design kept (five
levels, random order, replicates across a series, series order, bracket, blending, Protein A test
column, four sample points with SEC at first and last, LOQ handling, culture as a block). Departures in
the Version 1.0 report that PCR-004 must record: three sample points, three levels, turbidity not set
at levels, qualification against engineering-campaign data. No post-Version 1.0 study described; no
"fixed before the data" wording; TOC and cross-references.

## Could not be checked

The A-Mab "called critical" convention; SOP-4001 thresholds (placeholder); "licensed" for X-, Y-, Z-Mab
(STORY_BIBLE says earlier or prior products); the A-Mab p.85, ICH Q8(R2) and ICH Q10 wording; PTP-001's
schedule and RA-001's ranking basis; the mechanism statements.
