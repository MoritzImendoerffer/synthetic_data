# Content review — PCMP-001 Version 2.0 draft, run 1 (2026-10-08)

Judge: fresh-context agent, Claude Opus 5.5. Its only input was the rendered PDF text and the six
questions in `procedures/AUTHOR-A-DOCUMENT.md` §4.

Verdicts: Q1 No · Q2 No · Q3 Yes (sentences flagged) · Q4 No · Q5 Yes (conflicts found) · Q6 No.

## Findings that were machinery or data, fixed by the orchestrator

- The plan's Version 1.0 date (2026-07-24) came after every study it governs. Fixed with config
  `campaign.plan_approval` and `rev1_date()`. The stamp now becomes part of INV-001 finding 5.
- Table 7.1's tightened rows showed the a-priori fold of 2.00 beside the tightened criterion.
  `iac.final` now carries the replacing fold, 1.51.
- Table 1.1's role strings said "sets the cumulative XMuLV / MVM clearance", which is wrong for a
  single step. Fixed in `_pcpkg.UNIT_OP_ROLE`.
- The CQA table printed viral clearance as "16.7–30". It is now printed by spec type
  (`_pcpkg._acc_text`).
- The units "OD desc." and "% WV", the study kind "fraction", and the "neutralized Protein A
  pool" were all corrected in config and `tables.py`.
- The plan deferred the capability and model-adequacy thresholds because no helper carried
  them. `campaign.thresholds` now does.

## Findings returned to the author (one message, stated as what the text lacks)

- Q1: the agent of fragment clipping; the Protein A binding site.
- Q2: "governed attribute"; defined names for the two PAR analyses.
- Q3 and Q6: eleven filing, defending or signposting sentences.
- Q4: the basis of the CQA criteria and of the viral claims; the thresholds.
- Q5: six overreaching sentences: nrCE-SDS "in every study"; "none chosen with knowledge of an
  A-Mab result"; saturation of the screening fit; the ±3 SD description; "7 can be checked";
  "narrower than".

## Not acted on

- The Q5 note that a VH criticality sits at Tool #1 score 20. This is A-Mab's own scheme: impact
  20 with uncertainty 1 gives 20, and the level follows impact. The note is not an error.

# Run 2 (2026-10-08), fresh judge, Claude Opus 5.5

Verdicts: Q1 Yes · Q2 No · Q3 sentences present · Q4 No · Q5 conflicts found · Q6 No. The judge
confirmed that the arithmetic holds throughout (the parameter counts, the class split, the back
calculation, the viral sums, the degrees of freedom, the calibration dates).

## Orchestrator's disposition

- **Departs from the one-cycle rule, recorded here.** The author got one more pass, limited to
  factual accuracy (twelve Q5 items, the digit-opening sentences, three filing sentences). The
  reason: shipping known factual errors into the plan every other document reads is worse than
  a second pass. No third judge.
- **Fixed at the source:**
  - The virus filtration and anion exchange screening and RSM windows overlapped (config
    chronology).
  - The `decision_statistic` docstring misattributed the mean rule to ICH Q5A. It now cites A-Mab
    p.131.
  - The section plan said "criticality as a continuum (ICH Q9)". It now says ICH Q8(R2).
  - WRITING_GUIDE §3 now says not to open a sentence on an inline number.
- **Not acted on:**
  - Residual DNA ≤ 0.001 ng/dose (taken from A-Mab p.47-48, as the config records).
  - VH criticality at Tool #1 score 20 (A-Mab's scheme).
  - "AMD" as a document class (a sponsor's own record type is legitimate).
  - "Decision statistic" (defined once in the document).
