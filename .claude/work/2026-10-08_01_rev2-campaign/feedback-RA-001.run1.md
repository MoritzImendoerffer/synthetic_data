# RA-001 after the factual check and the content review: what to change (one revision, same author)

Inputs, in this folder: `factual-RA-001.md` (11 errors, each with its fix) and the content review summarised in
section C below (judge: Claude Opus 5.5, read only the PDF text; answers 1 No, 2 No, 3 Yes, 4 No, 5 Yes, 6 No,
7 No). Where this note gives a resolution, write to it; otherwise resolve each flag yourself and say in your
report what you did. Every value stays computed and every deciding word computed or asserted. The method, the
scores, the ranking and the study assignment stay those of Version 1.0; no study result enters.

## A. What changed under the draft (2026-10-10)
1. `ra_content.cqa_table()` prints each criterion as its type reads (a clearance has a floor only) and gives
   fragments no severity (None): the assessment never scored them. Print "—" with a note that fragments were not
   scored, and adapt your asserts (`sev_reg_min`, `sev_reg_max` over the scored attributes only).
2. The failure-mode texts of Tables 4.2–4.9 come from `risk_assessment/build_fmea.py` through
   `build_fmea.fill`: each now carries the parameter's own name and ranges from the config ("Culture temperature
   outside 34–36 °C", "CO2 partial pressure (pCO2) outside 40–160 mmHg"), "titre", and the UF/DF buffer exchange
   no longer "not part of DS characterization". The texts changed from Version 1.0 only in labels and units:
   list that as a correction.
3. `related_docs_md("RA-001")` now gives PCMP-001 the relationship "Applies this assessment at campaign level" and
   PCMR-001 "Master report of the characterization" (factual error 10).
4. The bioreactor role (Table 1.1, `UNIT_OP_ROLE`) now reads "Forms the glycan, charge-variant and aggregate
   attributes" (no "CQAs", no "design-space step").
5. PCMP-001 §3 now says the criteria are A-Mab's except fragments: A-Mab lists fragmentation among the typical
   attributes of an antibody without a limit, and the sponsor set the fragments criterion when fragments joined
   the register at Version 2.0. State the origin the same way (your hand-back item 3).

## B. The factual check: resolutions
Resolve errors 1 to 11 as `factual-RA-001.md` gives them. In particular: drop Table 3.2 (`T.methods_by_study`)
and the S-CEX-FRC reason, and point once to PCMP-001 Version 2.0 §7.8 and Table 7.3 for the method used in each
study (error 1; this also removes the three statements that no study result enters, which the content review
found contradicted); restore the Version 1.0 wording of detection 6 in the prose and in Table 2.1 (error 2);
error 4 wording; the capture-to-hold pH link handled by titration to the hold set-point in the receiving step
(error 5); fragments by nrCE-SDS in the wording of PCMP-001 §7.8 now ("every study that measures fragments, at
every step, measures them by nrCE-SDS"), or delete under error 1 (error 6); the Version 1.0 attribution for the
basal medium ("Platform experience shows") (error 7); "each step output on which a drug substance criterion
depends" (error 8); "assumes, for simplicity, that harvest has no impact on product quality" (error 9); the
minor items, including the continuum citation (restore Version 1.0's ICH Q9(R1) unless PCMP-001 Version 2.0 §2
cites Q8(R2) for it, in which case list the change).

## C. The content review: coordinator's resolutions
- **Q5 science** (correct a Version 1.0 description only where it is wrong, and list each correction): acidic
  variants rise with culture pH (deamidation is base-catalysed; "expected to fall" is wrong; check whether this
  is Version 1.0 text, and correct it either way, listed); "At the load pH, host cell protein, DNA and virus carry
  a net negative charge and bind" (most host cell proteins: basic ones flow through); inactivation "follows first
  order kinetics" (often tails toward the limit of detection: soften); "carries the highest severities of the
  train" (severity 10 is on 8 viral parameters and 1 bioreactor parameter); "Each parameter is assessed against the
  attributes of its own step" (against the attributes it can affect at its own step); the MVM requirement assigned
  to anion exchange beside virus filtration as the principal MVM clearance step (the register assigns the
  cumulative requirement to one step and the claims of several steps add up to it: say so once).
- **Statements that the tables contradict**: "The number separates classes of parameter. It does not separate
  parameters within a class" (Table 4.1: pH 560, temperature 448); "Severity is therefore what separates one
  parameter from another within a unit operation" (detection also differs, for example AEX load pH 10 against
  protein load 8); "A severity in Table 3.1 therefore says what a failure would mean for the patient" (severity
  carries uncertainty too); the UF/DF detection basis (restoring the Version 1.0 detection-6 wording, B above,
  fixes "the next step"; the score stays); turbidity a measured output with a set-point in Table 5.2 (add the note
  PCP-004 uses: measured, not set); Table 1.2 consumers (the step plans are named in the text: leave the builder).
  Where a sentence is Version 1.0 text and not wrong, keep it.
- **Occurrence and severity method** (Q5 items 9, 10, 20): Version 1.0 method; keep it, and do not add claims
  about it. Where the text says the severity is "taken from the attribute assessment", keep Version 1.0's words.
- **Q3 glosses**: cut "The scores in this document are initial scores in the same sense.", the PCMR-001 gloss,
  "It does not divide them into a critical and a non-critical group, and it is not a control strategy.", the
  detectability gloss, and "A low severity lowers the priority ... It does not remove the parameter from study."
  if they are your Version 2.0 text.
- **Q6**: the fragments-not-scored point is said about seven times: say it once in §3 and point there.
- **Q1, Q2, Q7**: fix the flagged sentences in your own text (name the mechanism and its direction; "register"
  for the attribute register only; name the code's subject at first use: the date finding, the interaction, the
  claim, the plan).
- **Tables**: Table 3.1 (a note that the criteria are A-Mab's except fragments; "≤ 2 %" spacing as the helper
  gives it); Table 5.2 (mark the rows superseded at Version 2.0, or point to PCMP-001 Table 4.2 row by row); the
  failure-mode tables are the builder's (A2).

## D. Gate and report
Gate with `check_render.py --render` (with `.venv/bin/python`), render the pdf and the docx, read the page image
of every table you changed, refresh `.claude/work/2026-10-08_01_rev2-campaign/RA-001_risk_assessment.DRAFT.txt`.
Report each item with where it was resolved, the flags you left and why, the passes, the page count, and any
`<<NEEDS:>>` left (none).
