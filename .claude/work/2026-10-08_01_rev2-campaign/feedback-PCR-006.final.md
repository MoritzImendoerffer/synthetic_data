# PCR-006 after review run 2: the final pass (same author)

Inputs: `content-review-PCR-006.run2.md` (the fresh judge's flags on your revised draft) and the owner's decision of
2026-10-10 on the record (section A). This is the last pass before promotion. Fix the items below. Where an item gives
a resolution, write to it. Every value stays computed and every deciding word computed or asserted. Read
`procedures/REPORT-LESSONS.md` §3 rule 1, §6 rule 9 and the new §7 first. Regenerate your brief
(`authoring/build_brief.py PCR-006`), because the register changed.

## A. The record: no deviations (owner, 2026-10-10)
A process characterization study is not GMP manufacture, so it raises no deviation. The config and builders are
changed and committed (00c0e64):
- **DEV-006-03 and DEV-006-04 are now PD-006-07 and PD-006-08:**
  - PD-006-07: XMuLV clearance not measured in the concentration study;
  - PD-006-08: input pool of the design runs not tested.
- **DEV-006-01 and DEV-006-02 stay as study events,** under their Version 1.0 numbers.
- **`dev_register` prints Event / Summary / Detected during / Outcome.**
- **The scalars `dev_006_03_conc_*` are gone.** Take the concentration range from
  `CFG.unit_op("viral_inactivation").param("protein_conc")` or the config `analytics.vi_concentration`.
- **PD-006-03 now records the outcome** in the register: the rule for fragment clearance set before the runs was not
  met. That was accepted on its risk, because the hold output meets the drug substance fragment limit without that
  clearance, and release testing measures fragments by nrCE-SDS.
- **The hold-study entry PD-006-05 now says** that the report states how a held pool is judged, an approach no plan
  set, chosen after the results were known. That answers the review's Q4 on §7.3. Keep §7.3's approach and point to
  the entry.

What to change:
1. **Rename §13 "Study events and discrepancies from the plan".** Open it with one sentence: PCP-006 calls a departure
   from the plan a deviation, and because a process characterization study is not GMP manufacture, this report
   records the events of execution as study events, under the numbers Version 1.0 gave them, and every departure
   from the plan as a discrepancy from the plan. Give the events first, then the discrepancies.
2. **Move the two former deviations into the discrepancy part** as PD-006-07 and PD-006-08, and update every mention.
   - PD-006-07 is not "closed". Say what S-VI-UNI2 showed and what it cannot exclude, which is the loss beyond the
     margin that §7.6 states.
   - The review's F10 sentence "Two were retained with a bounded impact" names the two events and their impacts.
3. **Wording and definitions.** No "deviation" in your own text. "Retained" becomes "retained in the analysis" where
   you use it. The §13.2 definition of a discrepancy follows the record rule: every departure from the plan, so the
   model selection is one too.
4. **Changes in this revision.** One item records the change of term and that the departures found in the
   re-analysis are discrepancies.

## B. Builders changed under you (re-render to pick them up)
- **`T.criteria_results` has a column "95 % limits of a single run over the NOR",** the statistic that decides each
  quality-attribute verdict. Its first column group reads "Mean predicted by the response-surface model, or measured
  results where it has none". That answers the review's Table 7.2 flag. Check the fit.
- **The model-selection discrepancy and the re-evaluation note** now say "a block term kept where the design has a
  second block" and "on one block of runs". That answers the review's §5.3 / Table 5.4 contradiction. Keep your §5.3
  sentence that the design has one block.

## C. Errors (Q5): correct each
- **D-001 stays.** Table 7.4 "PAR (set-point)" and the left panels of Figures 7.1 and 7.2 present the engine's values
  under its headings (brief §5c). Add nothing about where the other factors were held.
1. **§5.4, kinetics.** A first-order description, LRF = k(pH, T)·t, predicts a pH × hold-time interaction. The data
   show none within the range studied. Describe the response surface as the data show it, say the first-order
   description does not explain the absence, and make §2.1 and §2.3 agree (REPORT-LESSONS §7 rule 4).
2. **§9 and §11 limitation 3, "Without that run the attribute has no temperature effect".** Correct it to what
   Tables 5.5 and 5.10 give: the temperature effect on aggregate after each deletion, computed. If temperature stays
   significant in every model, the class does not hang on run 5. Make F3 and §5.3.2 agree.
3. **§5.1, acidic variants.** "One value per hold time" leaves out the concentration study at 90 min (§7.6). Restrict
   the sentence to the designs, or include that value. State the zero scatter as a fact, with no cause; it is an open
   owner question.
4. **§5.3, "small against the scatter of the method".** 0.10 points against a repeatability of 0.06 is not small.
   Correct it and make §11 (4) agree.
5. **§3.3, "The studies of the re-analysis measured fragments by nrCE-SDS on every sample".** S-VI-UNI2 measured no
   fragments. Correct it.
6. **Table 7.4.** Acidic variants and fragments have no adequate model, so no PAR. Show "n.a." or drop their rows if
   your table allows it. If the table is a builder's, report it.
7. **§7.5, "so each decision moved that pH".** Decision 2 left it at 3.54. Correct it.
8. **§5.4, acid hydrolysis.** The increase depends on hold time alone, with no pH or temperature effect. An
   acid-catalysed reaction would show both. Report what the data show, with no mechanism claim (§7 rule 4).
9. **Executive summary.** The cumulative XMuLV requirement is the register's value (Tables 2.1 and 7.1). The 6.60
   log10 is this step's claim, one of three. Correct it (§7 rule 8).
10. **F4, Conclusion 2 and §7.4, "each set by XMuLV clearance".** One edge of each range is set by XMuLV clearance,
    and the other is the end of the range studied (Table 7.6 note). Take the NOR-to-PAR margins from Tables 4.1 and
    7.6, computed: 0.10 pH units at the lower edge and 2.0 °C at the upper temperature edge, as the review found.
11. **§7.7.** At the platform's 180 min, A-Mab added 0.84 points against 0.70 (Table 7.13), so the widening comes
    from the shorter NOR alone. Correct "as well as the behaviour of the product".
12. **Moderate items.**
    - §3.5 and §7.4 must describe the NOR-propagated PAR statistic once and the same way.
    - §3.4: three spiked samples against two.
    - §7.4, "stays near 2.1 %": Table 5.5 gives a 0.47-point rise.
    - §13.2, the 39.6 % sentence: an exact fit is never adequate, and no adequate full model exists.
    - §5.2: say whether the output titres at pH 3.2 were at the assay's limit, from the record. If the record does not
      say, state it, and name DEV-006-02 (cytotoxicity raises the lowest reportable titre) as a possible cause of the
      difference, as a possibility only.
    - The reason the claim is judged on the mean is given once and the same way. It is the worst-case combination
      decided for viral clearance (§1.4, §3.5, §5.1, §11).
    - §9, the GPP class of concentration: state the power limitation.
    - The LRF is the difference of log10 virus loads, not of titres (§3.1, §5.1, Appendix D).
    - §7.3: the held pool reached 23.8 % (Table 7.3), and the day-0 values sit above S-VI-OFAT. Report both as the
      data give them.
    - §10: the hold conclusion is limited to one pool at the old set-points.
13. **Minor items.**
    - §9, the hold-time count against DEV-006-01.
    - §3.2: the concentration was set, not measured (PD-006-08).
    - §3.3: the cross-reference.
    - §1.3: the continuum attribution, as PCMP-001 words it.
    - §8: a longer hold would raise the index.
    - Table 7.2 note a: no offset on the XMuLV row. Report it if it is the builder's.
    - "CQA" headers that include fragments and acidic variants become "Attribute".
    - §5.3: the figure description matches the captions.

## D. Q4: criteria and judgements
- **§9, the CPP and WC-CPP margins.** No plan sets a numerical threshold. Name the judgement as one, with its basis:
  large-scale pH control holds about 0.1 pH units, which is why a 0.04 margin was not accepted and 0.11 was. Do the
  same in §7.5 (REPORT-LESSONS §1 rule 12 and §7 rule 5).
- **§7.5.1, the significant acidic-variant difference** (Holm p = 0.025). Report it as significant, with its size
  against the criterion. The share of the width is a judgement, not a rule (§7 rule 5).
- **§7.5.3, F7 and §12, "accepted on its risk".** Cite PD-006-03, which now carries the grounds, and give them once.
- **§10 item 3.** Include the fragment verification that was not met (Table 7.11).

## E. Q1, Q2, Q3, Q6, Q7
Fix the flagged sentences:
- Name the physical cause and its direction (F5: the acid denatures the viral envelope whatever the antibody
  concentration; F9: the level formed in the bioreactor near 18 %, with its batch spread).
- "Clearance factor" and "log reduction value" for "fold".
- Name S-VI-OFAT by its plan's name, not "stability study" (§7 rule 9).
- "The process model at set-point", with the load value, for "the nominal load of the step model".
- Cut the filing sentences and the tag after every register number (§7 rule 6).
- Say each repeated fact once (the claim judged on the mean, the procedure of the deletions, the nominal load).
- Name what each code and label stands for at first use (the fourth criterion, the two regressions, Table 7.5 for
  "the table of the decisions").

## F. Tables and figures
- Table 1.2: the Version 1.0 rule codes. If the builder prints them, report it.
- Table 5.9: the fourth criterion.
- Table 7.4: the rows that repeat the range studied go to one sentence, and "≥ 6.60" for "≥ 6.6".
- Table 7.8: split it, or cut columns.
- Table 7.9: the nested runs.
- Table 7.13: define the statistic "At the edges" and show the reference load.
- Table 13.2: the register. Leave it.
- The Appendix A table label must be A.1, not 13.3.
- Figure 7.1: the caption describes both panels, and the coding is not colour alone.
- Figure 7.2: the axis.

## G. Gate and report
- Gate with `check_render.py --render` (`.venv/bin/python`, venv on PATH).
- Render the pdf and the docx, and run `check_render` once more.
- Read the page image of every table and figure you changed.
- Refresh `.claude/work/2026-10-08_01_rev2-campaign/PCR-006_viral_inactivation.DRAFT.txt`.
- Report each item with where it was resolved, anything left and why, the passes, the page count, and any
  `<<NEEDS:>>` left (none). Do not commit.
