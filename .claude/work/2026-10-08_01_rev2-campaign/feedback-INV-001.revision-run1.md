# INV-001 revision, review run 1: what to change (one cycle)

## A. Data and machinery changed after your revision. Re-render and re-check every computed sentence.
1. Tightening now uses the 95 % confidence bound of the A-Mab prediction, like widening (both
   directions conservative, `amab_process/iac.py: final`). The reviewer flagged the old asymmetry
   (point prediction to tighten, bound to widen) as not conservative, and it was a fault of the
   machinery. The two aggregate criteria upstream of cation exchange are now stricter.
2. The bioreactor aggregate criterion is now marked BOTH tightened (cation exchange model) and
   widened (bound of the low-pH inactivation aggregate increase). `iac.csv` basis "back-calculated,
   tightened and widened on verification". Recount and reword anything that treats tightened and
   widened as disjoint.
3. `T.worst_case_verification()` notes and `T.iac_derivation()` note b) now say the bound replaced
   the platform value. The rule you quote from PCMP-001 must say the same.

## B. Tables (owner's comment, 2026-10-08)
4. Index cells that repeat down the rows are merged; the render gate now fails a table that
   repeats its first cell. Three of yours do: the safety factors of the Version 1.0 step criteria
   (repeats "Cation exchange"), the re-analysed step outputs (Table 6.4, repeats "Production
   bioreactor"), and the viral clearance claims (Table 6.5, repeats "Anion exchange"). Build each
   with `T.frame(df, caption, label, merge=[...])` (tables.py, section 13).
5. Long headers are broken over two lines (`header={"col": "Drug-substance\ncriterion"}`) or
   abbreviated with the abbreviation defined in the table note and in the Abbreviations table.
   Check every table of yours.

## C. Flagged sentences, each with what it lacks
Q1:
- "... for pool host cell protein, which is the output that sets the ranges of the step." Lacks
  why host cell protein limits the step (which parameters move it toward its criterion).
- "Computed against both ends, the index is 1.03, and the lower end governs it." The reason (the
  mean lies close to the lower limit) belongs in this clause.

Q2, terms that are not terms of art:
- "step output(s)": use the field's word (the step pool, or the intermediate).
- "worst-case mean": say the mean predicted log reduction at the least favourable combination of
  the other parameters.
- "method decision AMD-001": name it as the decision to change the fragment method to nrCE-SDS.
- "predictive bound": say the upper 95 % prediction limit.
- the Table 4.1 header "Highest level downstream steps bring to specification": a header that says
  what the number is.
- "specification type": one-sided or two-sided criterion.

Q3, sentences that file their own finding:
- "That is not a loosening of an approved criterion." Keep the fact once with its reason (the
  Version 1.0 limit was never an approved criterion), as information, not as a defence.
- "They are not a corrective action of this investigation."
- "It is a prior action that finding F6 relies on."
- "Host cell protein at cation exchange shows why the edge value is not the test." Give the
  example, then the point.

Q4, criteria without a basis, or results without met / not met:
- the cumulative viral clearance requirements of 16.7 and 8.6 log10 (give their basis);
- "The qualification conclusion is the same on the planned runs alone." State the qualification
  rule this conclusion applies, and the result for each output;
- the SEC bias "matters for a fragment criterion": state against what (the size of the bias
  against the criterion);
- leached Protein A is judged on the mean, against the document's own rule that quality attributes
  are judged per batch. Judge it per batch, or say why not (see Q5 first item);
- "Whether any proven acceptable range moved because of this is stated in the affected reports …"
  and the parallel sentence: an investigation's impact assessment states the impact. Give it from
  the PAR data (`D.par_table`, `D.par_table_rev1`) or name exactly which report states what.

Q5, contradictions and errors:
- Leached Protein A: the text gives a maximum of 4.40 ppm over the NOR and says it is below 5 ppm,
  but Table 6.4 shows 2.17 to 5.87 ppm. Make text and table agree, on the basis your table states,
  and give the result against the criterion on that basis.
- Table 6.5 against Table 6.4: the set-point clearances differ (7.10 against 6.87 for low-pH
  inactivation XMuLV, and the other steps likewise), and Table 6.5 shows a worst case above the
  nominal for XMuLV at virus filtration. The two tables are on different bases (the nominal process
  model against the response-surface model). Use one basis, or name the basis of each column so
  that the reader sees why they differ, and never compare across them.
- The Table 6.3 caption defines "No range" as "the criterion is not met at the set-point", but
  XMuLV at low-pH inactivation meets its claim with every parameter at its set-point. Define "No
  range" as what it is: with the other parameters at their least favourable NOR combination, the
  claim is not met even at the set-point of the scanned parameter.
- "the re-analysis in §6 uses the same characterization data as Version 1.0" is contradicted by the
  nrCE-SDS retests of retained samples and by the supplementary scale-down runs of S-PA-SDM2. Say
  exactly what data are new.
- "Applying these criteria … is acceptable because their derivation uses no data from those
  studies." Contradicted by Tables 6.1 and 6.2, and §3.3 condemns Version 1.0 on that very ground.
  The difference between the two versions is not whether this campaign's data entered. It is
  that Version 1.0 set its criteria after the data were seen, from the nominal performance of the
  downstream steps, with a margin chosen per step. Version 2.0 sets them from the platform worst
  case by a rule written before any report applied it, and admits this campaign's data only through
  the 95 % confidence bound of the downstream step's worst case within its NOR. Make §3.3 and §6
  argue that consistently.
- Dates: the investigation applies rules in its re-analysis twelve days before PCMP-001 Version
  2.0 took effect. Present the rules as defined by the investigation's corrective action (CA1) and
  then issued in PCMP-001 Version 2.0, so the order of events holds.
- "Acidic variants are now judged against both ends of their range (finding F4) …": the Version 1.0
  range criterion (Table 3.1) was already two-sided. Finding F4 concerned the capability index. Fix
  the attribution, and explain the narrowed range at the bioreactor from the data.
- The capability index for MVM clearance quoted from PCMR-001 Version 1.0 (per-batch capability of
  a validated clearance claim has no clear meaning). If you keep the quotation, say so once.
- "SEC read fragments higher … by 0.4 to 0.5 percentage points": Table 4.5 gives 0.53 for the VI
  pool. Compute the range.
- §7 misstates the offset rule: the precision of the offset is the condition for qualification,
  not permission to differ in mean.
- Table 4.6 footnote c equates the cation exchange response-surface study with S-CEX-FRC. If the
  footnote is in a builder (`T.methods_by_study`), report it in your hand-back and do not work
  around it.

Q6, sentences that say nothing a reader would miss (cut, or merge):
- "The table cites each rule by a code (R1 to R4), which is given below with the rule.";
- "What the investigation examined is how the step criteria were then set, and when.";
- "Each system is named once, with its description and its next calibration due date, beside the studies executed on it.";
- "Most of the ranges that changed became wider." (unless it carries the count);
- "The Version 2.0 value follows from rules that PCMP-001 Version 2.0 states before any report uses them." (restates §6.1);
- §7 "PCMP-001 Version 2.0 also states the rules of §6.1 that the re-analysis applies." and the two sentences after it.

Q7, sentences that need the paragraph before them (name the thing):
- "Corrective action CA1 removes the root cause for this campaign, and it also answers the second contributing cause in §5." Name the cause.
- "Preventive action PA1 removes the root cause, and the first contributing cause, for future campaigns." Name the action and the cause.
- "It answers the part of the third contributing cause that concerns dates (finding F5)." Name it.
- "No action creates the procedural step named in the fourth contributing cause either." Name it.
- "The one-sided assessment of acidic variants (finding F4) is therefore corrected by CA3 for this campaign only." Name what CA3 does.
- "Each was checked against the data of the step it describes, by the first rule in §6.1." Name the rule.
- "Table 6.4 gives each re-analysed step output … judged as the third rule in §6.1 states …". Name the two bases.
- "The first, third and fourth rules use the nominal results of this campaign, and the second rule uses its capability data." Name each rule.
- "… where the Version 1.0 criterion (the fourth rule in §3.3) lay above the platform claim …". Name the rule.
- "Several proven acceptable ranges at the bioreactor did not cover the whole NOR for the same reason (§6.3)." Name the reason.
- "The consequence is visible in PCR-003 Version 1.0." Name the consequence and the document.
- "… and the affected reports state the consequence (§6.3)." and "PCR-006 Version 2.0 states the consequence for the operating ranges of the step." Say what happens (for low-pH inactivation: the NOR is narrowed in PCR-006 Version 2.0; the narrowed NOR is not yet in the data, so say only that the report narrows it).
- "The decision and the retests predate Version 1.0." and "Corrective action CA2 brings AMD-001 into the plans …". Name the decision.
- Document identifiers used alone ("INV-001 during the review of PCMR-001 Version 1.0", "PTP-001 and RA-001 are reissued", "corrective actions CA1 to CA3"): give each document's type at first use in a section, and say what the actions are.
