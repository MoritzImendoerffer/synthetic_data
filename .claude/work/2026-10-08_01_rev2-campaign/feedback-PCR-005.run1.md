# PCR-005, review run 1: what to change (one cycle)

## A. Builder changes since your last render (check your text against them)
- `T.sdm_offsets`: single-step tables drop the Step column; "SD" is now "SDM" (it clashed with
  standard deviation); outputs with no criterion read "n.a. a)" under Qualified; the planned-runs
  table's caption ends "planned runs only".
- `T.worst_case_verification`: a step output that is not a response shows one merged "not a
  response" cell.
- `T.criteria_results`: the viral sentence of note a) appears only where the step has a viral output.
- `dev_register` and `discrepancy_register` have fixed column widths (IDs no longer split).
- Notes are lettered in order of use; cite a note by letter only through `marker_for`.
- The approvals caption is now the plain sentence "Synthetic record. Signatures are not applied."
  (done in your draft).

## B. Science (Q1/Q5)
1. Leached Protein A cause. "Host cell proteases in the held load have more time to cleave Protein A
   ligand from the resin": the held load does not touch the resin. The expected cause is that
   protease activity in the clarified harvest rises during the longer hold, so the load that reaches
   the column carries more protease and cleaves more ligand during loading. It is an expectation that
   this study does not test: say so once in §3.1, and make the executive summary ("for a known
   cause"), §10 ("which sets the offset") and the other mentions say "expected cause" or point to
   §3.1. "Leached Protein A depends on the life of the resin and on the load": name the property
   (protease activity of the load).
2. Pool host cell protein is reported per mg of antibody. Host cell protein associated with the
   antibody scales with the antibody, so it cannot explain a rise in ng/mg with load (§2.1, §5.8).
   State the load effect as the A-Mab observation, and give no mechanism for it, or one that explains
   a per-mg rise. PCP-005 Version 2.0 now says exactly this; follow its content. The pH effect: name
   the interaction that the lower pH disrupts (electrostatic association with the antibody and the
   resin, as histidine and acidic residues are protonated).
3. "It lowers step yield at high load, through its interaction with protein load." Name the physical
   cause (shorter residence time lowers the dynamic binding capacity near saturation).
4. "The mechanism predicted a small rise in pool host cell protein with a faster load at high load":
   give the basis of that prediction, or cut the sentence.
5. Fragments: §4.5 uses the upper prediction limit of a fragment model that §5.3 and Table 5.6
   declare not adequate, and §3.1 says fragments "are judged as the response-surface model predicts
   them" while §7.2–7.3 say the decision rests on the measured results. Make them one rule: the
   fragment decision rests on the measured results (no PAR from an inadequate model), and the hold
   rule's expected level for fragments uses the highest measured result within the NOR, or say why
   the model limit is used despite its adequacy.
6. Executive summary: "The studies were run … between 2025-11-05 and 2026-04-17." S-PA-SDM2 ran in
   September 2026. Say what is true (the characterization studies, then the supplementary runs).
7. §5.7 and Table 5.13: the rises (0.22/0.32 against 0.31; 0.45 against 0.46) and the sums
   (2.20 + 0.07 shown as 2.26): compute the prose from the same unrounded values as the table, and
   give the table a "computed from unrounded values" note.
8. §8 and §9 cite "94.2 % … 97.9 %" and "3.7 % of the plane (Section 6)", which Section 6 does not
   give. Give them in Section 6, or cite what Section 6 does give.
9. §1.4: "The experiments, the data and the fitted models are those of Version 1.0 …" contradicts
   item 5 (reduced step yield model, new nrCE-SDS fragment model) and the supplementary runs. Say
   exactly what is new.
10. §5.5 influence analysis is judged on the mean prediction. Judge it on the decision statistic of
    §7.1 (single-run upper 95 % prediction limit, `D.nor_prediction_limit`), or say why the mean.
11. §13.1: the run with low elution pH reads 8,418 against 12,212 predicted. Present it as what it is
    (a result well below the model's prediction at the recorded pH), and draw only the conclusion the
    data support.
12. Table 5.6 "reduced (5 terms)" against 4 in the text and Figure 5.3: count terms one way.
13. Hold of acidic variants: the expected level (14.7 %) is below the 18 % floor, yet the hold is
    declared met. Say plainly that the hold criterion is met for the increase, and that the floor is
    not met by the expected level before any hold, which is a bioreactor result (PCR-003).

## C. Criteria (Q4)
14. Column efficiency: give the criterion and the result of the plate count and asymmetry check, or
    say it is for information.
15. Executive summary Cpk values: state them against the 1.33 target there too.

## D. Words (Q2/Q3)
16. "decision statistic": say "the value compared with the criterion" (or define it once).
17. "the plane": "the region of protein load and elution buffer pH studied".
18. "the low-pH transition": the term of art (the elution front).
19. Cut the filing glosses: "Under the offset rule the difference is simply the offset of leached
    Protein A."; "This is the bias that INV-001 finding 6 describes …" (name the bias instead);
    "The runs were made after the characterization studies had closed …, so they could not influence
    how those studies were run."; "The qualification for pool host cell protein is reported with this
    order of events."; "Both met their criteria in every run, so the absence of a model limits what
    is known about their shape and not whether the step meets them." Keep the discrepancy-versus-
    deviation classification once, stated as what the work was.

## E. Machine sentences (Q6), cut or merge
"The expectations for each output follow from this mechanism."; "Their history establishes the
mechanism of the step and the direction of its main effects."; "What moved is the following.";
"The ranges are nested. …"; "As the footnotes to Table 7.2 state, …"; "… and the predictions are
shown for completeness."; the third statement of the lack-of-fit point; the fourth statement of the
qualified PARs; "Every output met its criterion across the NOR." in §8; the repeated univariate
limitation (keep it once); "This section keeps two kinds of record apart."; "The widened criterion …
moves part of the weight of the argument to cation exchange." (say the criterion now depends on the
cation exchange bound of 40.95-fold).

## F. Name the thing (Q7)
- "criteria 2 to 4 of PCP-005 §7" (many places): name them (model F-test significant, no lack of
  fit, predicted R² within the limit of R²) at least at first use in each section.
- "Criterion 5 is therefore not met for any response.": name it (Cook's distance below 4/n).
- "criterion 7 of PCP-005": name the hold rule.
- "INV-001 finding 6", "AMD-001", "DEV-005-01", "DEV-005-02", "S-PA-SDM": name what each is.

## G. Tables
- Table 4.1: NOR and Class wrap ("3.4–/3.7", "WC-/CPP"). Narrow the Unit column instead.
- Table 4.2: drop the constant "Studied in" column (say it once).
- Table 4.3: chronological order.
- Tables 5.1–5.3: no scientific notation (use `T.num`), step yield in %, p-values with a fixed
  format.
- Table 5.6: short headers with a note ("R² − pred. R²", "Met (criteria 2–4)").
- Table 5.9: short headers with a note.
- Table 5.10: a two-level header (HCP | Yield | LPA over Δ and 95 % CI).
- Table 5.12: the repeated SEC note goes once on the column header.
- Table 7.3: merge Criterion with Output; use parameter names that fit (or the letters A–D defined in
  the note).
- Table 8.1: Cpk as in the text (two decimals), and "Mean ± SD" on one line or two columns.
- Tables 13.4/13.5: factor codes A–D with units in a second header row; drop the all-"n.t."
  nrCE-SDS column of 13.4 with a note.
- Table 13.10: the qPCR unit.
