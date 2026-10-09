# Status: PCP-003 Version 2.0 fix cycle after content review run 1

Draft: `pc_package/PCP-003_bioreactor.DRAFT.qmd`. Nothing committed. Review:
`content-review-PCP-003.md` (this directory).

## 0000. Pass 4: COMPLETE

`check_render.py --render` passed twice. The second run followed widening Table 5.1, where the AMV identifiers were
breaking across lines. The PDF is 41 pages. I looked at Tables 3.2, 5.1, A.1 and B.1 as images.

The body was rewritten in one pass from the Version 1.0 content:
- §1.1 lists 11 changes, each set by PCMP-001 Version 2.0 or a record correction. Everything else is stated as
  Version 1.0.
- Pass 3 is superseded where it deleted Version 1.0 rules.
- The residual tests use PCP-005's wording. The low-pH aggregate argument and the risk paragraph are removed
  (review run 2 Q4-8 and Q3-1).
- PCR-003 must record these departures:
  - osmolality was active in screening but not carried forward, and the design was not amended;
  - the NOR was not narrowed for the acidic variant worst corner;
  - the univariate effect of initial viable cell concentration on acidic variants;
  - HCP, DNA, VCD, viability and titer were not measured;
  - the univariate study preceded the response surface study;
  - the 16-run augmentation, which the Version 1.0 rule "or the design augmented" foresaw;
  - the replicated univariate runs;
  - the probe drift DEV-003-01 against the calibration verification;
  - how osmolality was set.

## 000. Pass 4 (final; `feedback-PCP-003.final.md`), plan

The coordinator's correction: restore every Version 1.0 rule, design element and procedure that pass 3 deleted,
and list every remaining change from Version 1.0 in §1.1. Version 1.0 content is read from
`pdftotext pc_package/superseded/rev1/PCP-003_bioreactor.pdf` (content only). The PCP-005 residual-test wording
comes from its PDF.

Plan: one rewrite of the body.
- §4.1 from the Version 1.0 expectations (high mannose corrected).
- HCP and DNA sampling restored, with their methods.
- The Version 1.0 qualification comparison scope.
- The Version 1.0 §6.3 and §6.4 rules.
- The Version 1.0 §7 rules: run acceptance, adequacy with normality and augmentation, practical importance,
  operating region with the NOR inside, PAR met, classification, completion.
- §9 calibration verification and second-person review.
- §11 phases.
- §13 amendment.
- Appendices in design order (no start order).
- The §1.1 change list completed.

## 00. Pass 3 (after `data-state-2026-10-09b.md`): COMPLETE, gate passes

The coordinator's message is applied in full. Gate `check_render.py --render` passed twice in this pass (after the
rewrite, and after widening the Unit column of Table 6.2, where "mOsm/kg" ran into the "−1" column). It reports 261
inline expressions, 445 sentences / 8,536 words, "no inline source printed" and 8 complex tables. PDF: 39 pages.
Tables 1.1, 6.1, 6.2 and 7.1 were looked at as images.

**These supersede parts of sections 0–1 below:**
- **Acidic variants (a priori value stands).**
  - The widening is removed from §1.1 and §7: the 39.6 arithmetic, the "adds less over the same 180 min"
    sentence, the risk sentence and `AV_W` / `AV_WIDEN`.
  - Asserted per attribute: not tightened, not widened, upper limit equal to the a priori value; the low-pH model
    is not adequate; `downstream_added` equals the platform value.
  - §7 shows the a priori derivation (40.0 − 1.00 = 39.0).
  - Aggregate is the only changed criterion (`CHANGED == ["aggregates_hmw"]`). "Tightened and then widened" is
    stated in §1.1 and §7.
  - The hold paragraph covers aggregate only. Asserted: more than the platform at the edges; the NOR hold is
    shorter; the bound covers the NORs in force (same hold and temperature highs; the low-pH aggregate model has
    no pH term).
- **Labels.**
  - Every parameter name in the prose comes from the config (`N_*`, `nmc()`); the pCO2 abbreviation is asserted
    against the config label; the units come from the config (`DUR_UNIT`, `HOLD_UNIT`).
  - The abbreviations "e6" and "X" are removed.
  - Tables 6.1 and 6.2 show the new names and units.
- **Version 2.0 adds no step-specific rule (data note §5).** Removed:
  - the osmolality NOR rule (old §7 item 5);
  - the univariate t-test rule (old item 6);
  - my design-space definition (now PCMP-001's words only, §7 item 6);
  - my KPP and threshold sentences (§7 item 7 is PCMP-001 §7.7 verbatim in substance);
  - the "PAR narrower than NOR" rule, the no-model qualification and judgement rules, and "no decision rests on
    that comparison". The plan now says where PCMP-001 and the plan set no rule, and that PCR-003 states its
    approach.
  - **Also removed, under the same principle:** the response-surface factor ranking rule (§6.3), which I had
    asserted against the screening data. §6.3 now states the Version 1.0 design, says the plan sets no rule for
    what the screening review may change, and says osmolality is screening only and held at its set-point
    (PD-003-01 records S-BRX-OSM).
- **Execution details the record does not hold, removed:**
  - the off-line pCO2 check (risk 2 now says drift is not seen in the recorded setting, and is limited by the
    calibration interval);
  - Protein A capture of samples (§1.1 and §5.3);
  - osmolality set with sodium chloride and pCO2 held "by the sparge" (§5.1, §5.2, §6.3, §6.4);
  - the S-HAR-HLD hold study sentence (§4.2; no plan describes a hold study);
  - Start and End defined as inoculation and harvest (§11 now says only "from the start of its first run to the
    end of its last run").
- **Generic residual and influence tests** are in §7 item 2d and listed as change 7 in §1.1: the absolute residuals
  on the predicted values and the residuals on the start order, no slope significant at α; no Cook's distance
  above 4/n. The start order is defined as the run order of the design in §6.2.
- §5.5 univariate sentence: back to the Version 1.0 wording. §8 points to §7 item 5.

## 0. Where it stands (second author, Claude Opus 5.5, 2026-10-09)

**The fix cycle is complete in the draft.** Every section listed under "Sections and fixes left" by the first
author is rewritten. Gate `check_render.py --render` passed on run 1 and again on run 2, after the table and
readability fixes: all chunks and 218 inline expressions eval, no `<<NEEDS:>>`, tic gate clean (467 sentences, 9,053
words of prose), docx and pdf render, no missing glyph, every cross-reference resolved, 8 complex tables complete, no
repeated index cell, nothing below 7.9 pt. The numeral lint (advisory) flags identifiers only. PDF: 39 pages. Every
complex table was looked at as an image. Table 5.3 was wrong (IDs broken across lines) and is now a `T.frame`.

Coordinator changes applied:
- PCP-003 Version 1.0 approved 2025-08-07, before S-BRX-SDM starts 2025-08-11. The stronger assertion
  `V1_DATE < FIRST_START` is restored, and Section 1.1 says the plan was approved before the first study began.
- Shared table notes now carry the single-batch bound. The prose uses "one-sided 95 % prediction bound of a single
  batch" throughout.
- **Canon correction (low-pH replacements).** Aggregate: A-Mab adds more than the platform at the edges of the range
  studied (0.84 against 0.70), and its replacement reflects the shorter NOR hold (120 min against 180 min). Acidic
  variants: A-Mab adds less than the platform at the same 180-min hold (0.60 against 1.00), and the shorter hold
  lowers it further (0.40). Section 7 says so. All values come from `D.iac_verification()`, and the deciding words
  are asserted.

## 1. What was done, by section

- **Setup chunk.** New asserted deciding words:
  - approval before the first study;
  - the study order;
  - qualification ended before the first characterization run;
  - univariate after screening; univariate and response surface overlap;
  - the set-point reference was not run at the same time as the univariate study;
  - runs of each study overlap in time (culture days exceed the window);
  - the pooled-t offset interval (checked against `D.sdm_offset` for the raw-scale outputs);
  - no NOR or set-point of this step changed;
  - the glycan lower limits are unchanged;
  - the acidic variant lower limit is the drug substance limit;
  - no step after the bioreactor credits acidic variant removal;
  - the criterion arithmetic from unrounded values (aggregate and acidic variants, in force and a priori);
  - the derivation uses downstream data only;
  - the ranking rule for the response-surface factors selects the Appendix B factors and leaves osmolality last;
  - fragments have criteria from the Protein A pool onward;
  - S-HAR-HLD measures fragments;
  - the titer method is in the plan's SOP and AMV lists;
  - the osmolality control text (sodium chloride, sparge);
  - the low-pH hold facts.
- **1 / 1.1.** Documents named at first use. Qualification "planned in 5.1", not "qualified". Approval before the
  first study. "The master plan PCMP-001" as subject. "Safety factor" for the divisor. The changed criteria are
  named from computed text. Thresholds are given (α, LOF α, the gap, Cpk 1.33 and 1). The qualification order is in
  item 4. One INV-002 paragraph says it changes nothing in the plan. The AMD-001 paragraph cites Section 4.2 for the
  scope and the Protein A capture for the samples. "Do not loosen" is dropped. The glycan lower limits are explained.
- **2.** Objectives 1, 3, 4 and 6 are reworded: estimate the offset and decide at analysis; "test" the model;
  "compare it with the NOR"; evidence on product quality. Objective 2 adds judging the osmolality NOR.
- **3.** The Table 3.1 introduction names what the registry table holds and the five other documents cited.
- **4.1.** Mechanisms with direction:
  - the ion exchange steps cannot separate glycoforms, because fucose, galactose and mannose carry no charge;
  - afucosylation falls with GDP-fucose supply and Golgi residence; FcγRIIIa;
  - galactosylation: UDP-galactose and manganese depletion; high osmolality raises specific productivity; a limiting
    donor is the reason interactions are tested;
  - high mannose: Man5 and N-acetylglucosaminyltransferase I;
  - aggregate: the isoelectric point lies above the culture pH; the initial viable cell concentration acts through
    titer;
  - acidic variants: the expected direction through deamidation for temperature, pH and duration; the net direction
    is not predicted for pH, pCO2 and osmolality;
  - the routes of the univariate parameters (the dissolved oxygen sparge strips CO2; medium and feed act through the
    UDP-galactose precursors);
  - "fed to excess", the empty sentence and "known/confirms" are removed.
- **4.2.**
  - Caption "Quality attributes that the drug substance CQA register assigns ...".
  - Critical means H and VH. Host cell protein is M-H.
  - "Tool #1 score".
  - Acidic variants are measured by icIEF only.
  - The host cell protein and DNA scope is argued (no criterion at this step), with the stated limitation on
    classification.
  - The fragments scope is argued (the harvest hold study S-HAR-HLD in PCP-004; criteria from the Protein A pool
    onward).
- **4.3.** Interactions are "may depend", so tested. "Ranked lower" is kept. The wrong sentence about the univariate
  parameters is removed.
- **5.1.**
  - No equivalence overclaim.
  - Runs in parallel.
  - pCO2 tends to rise with scale.
  - The sparge holds pCO2 at the level of each run, so commercial stripping is not matched.
  - An off-line pCO2 check in each run.
  - Student's t with a pooled SD; each end is a one-sided 95 % bound.
  - "The judgement over the NOR" is named and defined before its use.
  - The rule for an output with no adequate model.
  - The offset applies to every study; no range from any study when the model is not qualified.
  - Qualification order: offset before the first characterization run, decision at analysis.
- **5.2.** Osmolality is set with sodium chloride, independently of pCO2 (asserted against the config text). Titer is
  measured by SOP-3016 / AMV-3021. Performance is not a response, so the KPP limitation is stated.
- **5.3.** Protein A capture of every sample. The repeated fragments and AMD-001 sentences are removed. SEC is also
  used in the qualification and univariate studies.
- **5.4.** Table 5.3 is restructured: scale-down runs and manufacturing-scale batches separated, replicate counts, a
  total row, as a `T.frame`. The duplicate set-point-reference sentence is removed.
- **5.5.**
  - "95 % prediction interval of a single future batch".
  - Screening fit statistics: R² describes the fit and overstates prediction.
  - "Integrated process model".
  - Two-sided criteria computed (the glycans and acidic variants).
  - Duplicates removed.
  - Points to the univariate rule.
- **6.2–6.4.**
  - "Start order", runs in progress at the same time.
  - pCO2 and osmolality are estimated at a constant level of the other; at scale they rise together, and the report
    states both.
  - The response-surface factor rule (each main effect over the criterion width, summed over the attributes; the top
    `K_RSM`), with the review-and-amend step, asserted against the data.
  - What the plan does with osmolality.
  - Dissolved oxygen is studied at constant pCO2.
  - The set-point reference was not concurrent (time and media lot), so no decision rests on it.
- **7.** Restructured into 9 items:
  1. qualification, with the judgement over the NOR defined;
  2. adequacy, with any failing criterion meaning no range; criterion d is Statistics' judgement from the plots
     (no numerical threshold exists); an output with no adequate model is judged on its measured results;
  3. single batch; two-sided criteria computed;
  4. PAR, with the consequence when the PAR is narrower than the NOR;
  5. **a new rule for the osmolality NOR**: the screening change over the NOR (main effect and its two-factor
     interactions) against the margin at the least favourable NOR combination;
  6. the univariate rule: every run at both ends meets the criterion; the effect by a two-sided t-test at α;
  7. design space on the predicted mean, with osmolality and the univariate parameters at their set-points; overlay
     contour plots; a single-batch claim rests on the PARs; an attribute with no model;
  8. classification: PCMP-001 sets no numerical threshold, so the report states effect sizes and margins; KPP from
     platform knowledge;
  9. Cpk, including the 1 to 1.33 outcome.

  The IAC paragraph:
  - "platform or verified" worst case;
  - unrounded arithmetic (5.00 × 1.4038 − 0.5586 = 6.46; 9.30 a priori; 40.0 − 0.40 = 39.6);
  - percentage points;
  - the basis of the acidic lower limit.

  The verification wording, the hold-time paragraph (canon correction), the risk of each change and the PCR-003
  sentence are rewritten. "Never the point prediction" is dropped.
- **8.**
  - The set-point PAR and the NOR-propagated PAR are each defined at first use.
  - The draw distributions are stated (99.7 % within the NOR, clipped to the range studied; normal residual; MVN
    coefficients).
  - Two reasons the NOR-propagated PAR is narrower.
  - Two-sided criteria computed.
  - Osmolality and the univariate parameters point to items 5 and 6.
  - D-001 is kept: set-points, at full strength.
- **9.** PA3 is "the preventive action". A deviation is a setting outside the control band of SOP-2003. Discrepancy
  against deviation without "is not".
- **10.** Caption "author, review and approve". Each role is named in the text and the table. Manufacturing Science is
  separated from Process Development / MSAT.
- **11.** Table 11.1 is a `T.frame` with equipment and next calibration due, merged. Start and End are defined. Runs
  are in parallel. The sequence matches PCMP-001. The duplicate approval sentence is removed.
- **12.** The off-line pCO2 check is the control for probe drift. A new assumption 5: the pCO2 and osmolality effects
  add at scale.
- **Appendices.** "Run type", "Start order", the B.1 columns in order A, B, E, C, coded columns right-aligned.
- **Abbreviations.** Added %Gal, CEX, DoE, e6, FcγRIIIa, G1/G2, GDP, GMP, H, M-H, Man5, sd, UDP, VH, VL.

## 2. Left in the draft

Nothing. If the review is run again, re-read Section 7 items 5 to 8, which are new rules (see below).

## 3. Outside the draft (coordinator or owner)

Updated in pass 3:
- The units and the pCO2 label are fixed in the config.
- The new plan rules listed below (osmolality, univariate, design space, KPP, Protein A capture, off-line pCO2,
  Start/End) are REMOVED from the draft, so they no longer bind PCR-003.
- PCR-003 must now state its own approach for:
  - the osmolality NOR;
  - the univariate decision;
  - a PAR narrower than the NOR;
  - an output with no adequate model (qualification);
  - showing a KPP;
  - what the screening review could change.

Each is a discrepancy from the plan where the report needs one.

- **Config (still mislead):**
  - the feed-1 volume definition;
  - the residual DNA unit ≤ 0.001 ng/dose (Table 4.1);
  - the decimals "1–1.4" and set-point "1" in Table 6.1.
- **Helper tables** (still mislead):
  - Table 1.1 (`T.criteria_change`): "R1, margin 6.8" calls the divisor a margin (the prose says safety factor); its
    footnote letters for widened and tightened differ from Table 7.1; the Basis cells wrap; "Drug substance" against
    "DS criterion"; alphabetical row order.
  - Table 7.1 (`T.iac_derivation`): "Clearance factor 1.00" for attributes that are not cleared; two unmarked notes;
    "Drug-substance" hyphenated.
  - Table 3.1 (`related_docs_md`): PCR-003 is "Rolls up into" PCMR-001, not the plan; nested brackets.
  - Table 3.2 (`T.sop_references`): merged type labels sit centred, so some rows have no label; "Titre" against
    "titer"; SOP-3016 paired with AMV-3021.
  - Table 4.1 (`cqas_for`): header "Tool #1" (the prose says score); capitalization; "(CEX/icIEF)"; "(deamidation)".
  - Table 5.2 (`T.methods_by_study`): footnote in the past tense, about "this study".
- **Revision history (config `campaign.revisions`).** "Re-analysis of the studies" describes the reports' work, not a
  plan's.
- **PCMP-001 §6.1 against its own Table 6.1.** The rule says the response-surface design covers "the factors that
  screening showed ... to affect a CQA". Osmolality has significant screening effects on galactosylation and acidic
  variants, yet Table 6.1 plans 4 factors for this step. The plan cites PCMP-001 §6.1 for the four factors and gives
  its own ranking rule. An assessor may read this as a departure from the master plan.
- **New plan rules that PCR-003 must apply or record as discrepancies:**
  - item 5, the osmolality NOR. Computed in the scratchpad, it is supported for afucosylation, galactosylation, high
    mannose and aggregate, and NOT for acidic variants: the worst-corner interval already fails 18 %. This matches
    PD-003-01;
  - item 6, the univariate rule (two-sided t-test of the two ends at α);
  - item 7, design space on the predicted mean;
  - item 8, KPP from platform knowledge (RA-001);
  - 5.3, Protein A capture of every sample;
  - 5.1, the off-line pCO2 check in each run (no off-line pCO2 data exist);
  - 11, Start and End defined as first inoculation and last harvest (`study_chronology.csv` defines neither).
- **No configured scale-down working volume exists.** The review asks for one, and none is stated.
- **Annex builder.** It must call `T.sop_references(sops=PLAN_SOPS, amvs=PLAN_AMVS)` and the new `T.frame` tables
  (tbl-sampling, tbl-schedule, tbl-matrix-*), and anchor on the new Section 7 wording.
- **STORY_BIBLE chronology sentence** is now true for PCP-003 (approved 2025-08-07, first study 2025-08-11).

## 4. First author's record (part 1, condensed)

- **Constants.** `D.PAR_GRID_SETPOINT`, `D.PI_LEVEL` and `D.VERIFICATION_BOUND` replace the inspect-based reads.
- **Studies of this plan.** These are the bioreactor studies closed by `REV1["effective"]`. S-BRX-OSM and S-BRX-AUG
  are excluded; PCR-003 records them as discrepancies.
- **Values tested then and used now:**
  - the osmolality ranking (pH 0.83, pCO2 0.72, duration 0.59, temperature 0.58, osmolality 0.35);
  - the aggregate arithmetic (6.46 and 9.30) and the acidic arithmetic (39.6 and 39.0);
  - the 180-min against 120-min hold;
  - the osmolality control text;
  - the titer SOP and AMV;
  - the fragment criteria and the harvest hold columns;
  - `D.nor_met` for an output with no adequate model.
