# RA-001 after review run 2: the final pass (same author)

Input: `content-review-RA-001.run2.md` (in this folder, the fresh judge's flags on your revised draft). This is
the last pass before promotion. Fix the items below and nothing else. Where an item gives a resolution, write to it.
Keep every value computed and every deciding word computed or asserted. Version 1.0 means the frozen text
(`pdftotext -layout pc_package/superseded/rev1/RA-001_risk_assessment.pdf -`). Many flagged sentences are Version 1.0
text ("consumer", "Material does carry properties forward", "initial scores", "a separate assessment", the
viral-severity paragraph, the augmentation sentence, the pressure sentence). The rule:
- keep Version 1.0 text unless it is wrong;
- correct what is wrong, and list each correction in Table 1.3;
- no study result enters;
- the method, the scores, the ranking and the study assignment stay those of Version 1.0.

## A. Reissue scope
1. **Table 5.2 marks (reissue item 1, the clear breach).** Drop the per-row marks and footnotes b) and c), which show
   which set-points and NORs the reports changed. Give one note under the table: the values are those the
   assessment was made against, and PCMP-001 Version 2.0 Table 4.2 gives the values in force. Adapt the sentence
   in the text the same way.
2. **Leached Protein A (reissue item 2).** Restore the Version 1.0 sentence: "The capture study measures leached
   Protein A in the pool across the designed experiment, so the ranges this assessment scopes are bounded against it
   even though no parameter is ranked on it." No rule for judging the pool enters.
3. **Fragments (reissue item 3).** Say only that PCMP-001 Version 2.0 §7.8 sets nrCE-SDS as the method for
   fragments, following the decision to change the fragment method (AMD-001). Drop "and Table 7.3 give the method
   used in each study". PTP-001 now says the same.
4. **Reissue items 4, 6 and 8.** Cut three sentences:
   - the spiking-model sentence, which is not in Version 1.0;
   - "No data are planned beyond those ends of the NOR, and a proven acceptable range (PAR) is never claimed beyond
     the range studied (PCMP-001 §7.6)", which is not in Version 1.0;
   - the sentence on the step plans amended under INV-001 corrective action CA2.
5. **Reissue item 5 and Q5.6, the anion exchange augmentation sentence.** This is Version 1.0 text, and it is
   illogical. Flow rate is studied one factor at a time, so no study as assigned can detect an interaction of
   residence time with load pH and conductivity. Correct it (listed): the univariate result bounds the step only if
   that interaction is absent, as prior knowledge expects, and PCP-008 carries that justification.
6. **Reissue item 7.** The Version 1.0 clause "a hold longer than its range raises aggregate at any pH in the range"
   states a result before any study. Make it an expectation from platform experience (listed).

## B. Errors (Q5): correct each, listed in Table 1.3 where it changes Version 1.0 text
1. **Section label.** Table 1.3 says "4.2 to 4.9". Correct it to the sections that hold the relabelled failure modes
   (§4.1 to §4.8, Tables 4.2 to 4.9).
2. **Viral severity (Q5.2).** The paragraph gives undetectability as the reason for severity 10, but detectability
   belongs to the detection score (Table 2.1 and §6). The basis is the very high criticality the register gives
   viral clearance by rule (PCMP-001 §3, your §3). Correct the reason, listed. Keep the rest of the Version 1.0
   paragraph.
3. **Severity and uncertainty (Q5.3).** Cut your Version 2.0 sentence "A severity in Table 3.1 therefore combines the
   impact ... with the uncertainty of that impact". Table 3.1 contradicts it (residual DNA, score 6, severity 2;
   acidic variants, score 4, severity 4). Keep Version 1.0's "Severity is taken from the quality attribute
   assessment and is not re-derived." Keep its clause on capability and detectability, and drop only the words "says
   what a failure would mean for the patient". State no mapping from score to severity.
4. **The lowest ranked parameters (Q5.4, your text).** Make the sentence agree with Tables 4.1 and 5.1. The two
   Protein A parameters of the lowest class, load flow rate and end of pool collect, are carried into the capture
   design so that it bounds step yield. That is the reason §2 already gives.
5. **Interaction judgements (Q5.5).** §4 records no interaction judgement for six parameters:
   - pCO2, osmolality and culture duration;
   - cation exchange elution stop collect;
   - anion exchange wash-1 conductivity and protein load.

   Limit the claim to what §4 records: an interaction judgement is given where it decides the study type. Or name
   the parameters for which the study type follows from the step's design. Add no new judgement. If "The 5
   parameters ... are therefore carried into one designed experiment" is Version 1.0, keep its basis as Version 1.0
   gives it. Otherwise give the basis §4 records.
6. **Virus filtration volume (Q5.7).** Table 4.8 now names the edge of the range studied, 140 L/m2 (the shared
   failure-mode text was corrected for you, see section E).
7. **UF/DF (Q5.8).** The Version 1.0 sentence "It forms and clears no quality attribute." is wrong for a step that
   sets the concentration released against a specification. Correct it to "no attribute in Table 3.1" (listed).
8. **"CQA(s) at risk" (Q5.9).** The header is now "Attribute(s) at risk" in the shared builder (section E), because
   §3 calls only high and very high attributes critical. Use the same words in your text.
9. **Pressure and parvovirus retention (Q5.10).** The Version 1.0 sentence "Prior knowledge places neither the size
   nor the direction of a pressure effect on log reduction" is wrong. Parvovirus filters can retain less virus at low
   pressure or low flux, and after a pressure interruption. Correct it, listed: the direction is known from such
   filters, and the size for this filter is not.
10. **Your own text.** "Dissolved oxygen raises titre through the productivity of each cell" must agree with Table
    4.2 (peak viable cell density, titre and process consistency). "The same glycosyltransferases" must name the
    enzymes the pH mechanism names, which include mannosidases. Change "the study assignment is the output" to "the
    main output", to agree with §7.
11. **Left as Version 1.0, not wrong.**
    - Q5.11 (leached Protein A attributed to the resin): a judgement of Version 1.0.
    - Q5.14 ("The parameter list is assumed complete"). Where §3 says fragments were not scored, add that the
      harvest hold, where they form, is not a parameter of the list.
    - Q5.15: the parenthesis "(viral clearance robust)" is removed from the shared failure-mode text (section E).
      List it.
    - Q5.17: the Version 1.0 method.

## C. Q4
- **Fragments criterion.** PCMP-001 §3 gives its origin and no derivation. Write it as PCMP-001 does, once. The
  basis of ≤ 2 % is an owner question.
- **Residual DNA in Table 3.1.** Add the dose in a note: `_pcpkg.DOSE`, 10 mg/kg for a 70 kg reference adult. The
  body weight is an assumption, and the note says so.
- **Leached Protein A.** The criterion question goes away with A2.

## D. Q1, Q2, Q3, Q6, Q7
- Fix the flagged sentences that are your own Version 2.0 text:
  - Name the physical cause and its direction.
  - "Load pH and conductivity" for "load chemistry", in your own sentences.
  - "Concentration polarization layer".
  - "The decision to change the fragment method (AMD-001)" for "the analytical method decision".
  - "Uses as its risk basis" for "consumes" in your own sentences.
  - "Each step output on which a drug substance criterion depends" is PCMP-001's term. Keep it.
  - Cut your glosses.
  - Name each code's subject at first use.
- Where a flagged sentence is Version 1.0 text and not wrong, keep it.
- The revision history entry is the builder's (`revision_history`). Leave it.

## E. Shared builders, already changed for you (re-render to pick them up)
- `ra_content` failure-mode and ranking tables: the column header is "Attribute(s) at risk".
- `risk_assessment/build_fmea.py`:
  - the virus filtration volume failure mode names the upper end of the range studied;
  - the anion exchange protein load effect reads "Reduced HCP removal capacity", without "(viral clearance robust)".

## F. Gate and report
- Gate with `check_render.py --render` (with `.venv/bin/python`, venv on PATH).
- Render the pdf and the docx.
- Read the page image of every table you changed.
- Refresh `.claude/work/2026-10-08_01_rev2-campaign/RA-001_risk_assessment.DRAFT.txt`.
- Report each item with where it was resolved, anything left and why, the passes, the page count, and any
  `<<NEEDS:>>` left (none).
