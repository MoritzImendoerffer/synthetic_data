# PTP-001 after review run 2: the final pass (same author)

Input: `content-review-PTP-001.run2.md` (in this folder, the fresh judge's flags on your revised draft). This is
the last pass before promotion. Fix the items below and nothing else. Where an item gives a resolution, write to it.
Keep every value computed and every deciding word computed or asserted. Version 1.0 means the frozen text
(`pdftotext -layout pc_package/superseded/rev1/PTP-001_transfer.pdf -`). The rule is the same as in run 1:
- keep Version 1.0 text unless it is wrong;
- correct what is wrong, and list each correction in §1.1;
- no study result enters as a basis;
- no execution history of the characterization enters the plan.

## A. Amendment scope (R1 to R5)
1. **The fragment method history (R1, R2, R3).**
   - Drop Table 6.4 (`T.methods_by_study`), its footnotes and every sentence that tells which method measured
     fragments in which study, the re-test of retained samples, the re-executed design, or the comparability study
     S-CEX-FRC as the basis of the decision.
   - Drop "Where the characterization reports base a decision on fragments, they use nrCE-SDS results."
   - Point once to PCMP-001 Version 2.0 §7.8 and its Table 7.3 for the method used in each study. RA-001 now does
     the same.
   - Keep the change itself: nrCE-SDS (SOP-3015, AMV-3020) added to the methods to transfer, following AMD-001 as
     PCMP-001 §7.8 sets it, and "This answers INV-001 finding 6, that SEC reads fragments high in samples that
     still carry host cell protein", as the step plans word it. SEC stays the method for aggregate, attributed to
     PCMP-001 §7.8.
2. **R4.** Cut the PD-005-06 sentence and its repeat in §1.1 item 5. Keep the transfer need: SOP-3016 and
   AMV-3021 are added because the titre sets the protein load of a capture run.
3. **R5.** Cut "Those steps were studied in parallel, which their independent scale-down models allowed." The
   dates stay.

## B. Errors (Q5): correct each, listed in §1.1 where it changes Version 1.0 text
1. **The development train (Q5.1, Q2, Q7).**
   - Version 1.0 Table 8.1 names it: "Scale-down models are qualified against the development train only".
     Version 1.0 Table 4.1 row 1 said the models are qualified against the commercial train before any study is
     run, which the order of Table 10.1 rules out.
   - Define the development train once: the manufacturing-scale train at the sending site whose batches are the
     manufacturing-scale reference of each step's qualification (PCMP-001 §7.1). Make Table 4.1 row 1, change 3
     and §5 agree with that definition (correction, listed).
   - If you give the number of manufacturing-scale batches, take it from `sdm_qualification.csv`. Invent no
     equipment and no scale.
2. **Table 8.1, gap 1 action (Q5.2).**
   - No receiving-site batch exists before PCMR-001 (Table 10.1), so the comparison with the receiving-site train
     can use only the engineering batches.
   - It cannot be recorded in a step plan, because each step plan was approved before its studies.
   - Correct the action to what Table 10.1 allows: the comparison is made on the engineering batches and recorded
     in a deliverable of Table 10.1, such as the engineering batch reports (correction, listed).
3. **The schedule (Q5.3, Q7).** "The first two gaps set the schedule" contradicts §10, and both are Version 1.0.
   §10 is right. Replace "set the schedule" with what holds: each needs laboratory work at a site that has not yet
   done it (correction, listed).
4. **The remaining gaps (Q5.4).**
   - Sequencing, training or a bounded qualification study does not close the harvest and UF/DF gap or the viral
     clearance gap. Table 8.1 manages them, by a stated limitation and by retaining the small-scale claims.
   - Say which gaps close and which are managed.
   - Give the Table 8.1 column a header that fits both, for example "Action that closes or manages it"
     (correction, listed).
5. **Comparability (Q5.5).**
   - ICH Q5E judges a manufacturing change, a site change included, by comparing quality attributes before and
     after the change. Conformance to the criteria alone is generally not enough.
   - Correct the paragraph: the drug substance of the engineering batches is compared with that of the
     development-train batches on the attributes of Table 2.2, and each batch must also meet the criteria.
   - Cut "A development mean is a property of the scale-down model and of the few batches behind it" and the
     sentence that follows it. Under §5 the development-train batches are the manufacturing-scale reference.
   - Add ICH Q5E to `references.bib` as an entry in the style of the other ICH entries, and cite it (correction,
     listed).
6. **Viral safety (Q5.6).**
   - Correct "rests on three independent steps": XMuLV clearance rests on three claimed steps and MVM clearance on
     two, because the low-pH step carries no MVM claim. With margins of 0.02 log10, every claimed step is needed.
   - State the premise behind "cannot be made up by the other steps": no step is credited above its claim
     (PCMP-001 §7.4).
   - Keep the margin against the precision of the titre assays (correction, listed).
7. **Judgements at manufacturing scale (Q5.7).** Change 3 says every judgement is stated at manufacturing scale.
   Limit it to the outputs the qualification compared (PCMP-001 §7.1 rule 2).
8. **Methods in scope (Q5.8).**
   - The infectivity titre assays (AMV-3017, AMV-3018) measure viral clearance in the virus spiking studies. Those
     studies stay at small scale (Table 8.1), and no batch test measures viral clearance (§6.3).
   - Take the two assays out of the methods the receiving site transfers, or say that they stay with the spiking
     studies, and make Table 6.3, Table 8.1 row 2 and §6.2 agree.
   - nrCE-SDS is transferred, but the method record holds no performance row for it. Its validation is AMV-3020 in
     Table 6.2. Say so once, and invent no row.
9. **The other elements of Table 4.1 (Q5.9, Q5.10).**
   - Say that they differ between the sites in ways that can affect the process, each managed as Table 4.1 states:
     - the central buffer hold;
     - commercial raw-material lots, a known source of variation in culture performance and glycosylation;
     - the transferred methods.
   - Both buffer preparation and method transfer need laboratory work (correction, listed).
10. **Fragments at harvest (Q5.11).** Attribute the assignment to the CQA register of PCMP-001 Version 2.0, with
    the basis PCMP-001 §3 gives: proteases released from lysed cells clip the antibody, in culture and during the
    harvest hold. Fragments are judged at the downstream steps. Do not claim that a harvest parameter in Table 6.1
    controls them.
11. **Minor items.**
    - Q5.12: AMV-3221 belongs in Table 6.2 if `T.sop_references` takes it, otherwise say where it is listed.
    - Q5.13: Stage 2 of FDA 2011 also covers the qualification of facility, equipment and utilities.
    - Q5.15: post-clarification turbidity is measured, not set. Use the note PCP-004 uses.
    - Q5.16: the qualification protocol sets the PPQ sampling plan, with more sampling than routine manufacture as
      FDA 2011 expects. The sampling plans of the step plans are for small-scale runs.
    - Q5.14: the handovers are the deliverables of Table 10.1.
    - Q5.17 (the empty approvals table) is the corpus convention. Leave it.

## C. Q4
- **Fragments criterion.** PCMP-001 §3 gives its origin and no derivation. Write the origin as PCMP-001 does and
  nothing more. The basis of ≤ 2 % is an owner question.
- **Viral claims.** Give each claimed step's claim, from the config or helpers, beside the sums, so a reader can
  check the sums.
- **Residual DNA.** "Met through clearance ... not tested at release": point to where the clearance is shown (the
  step reports and PCMR-001). No study result enters this plan.
- **Method transfer success.** Table 6.3 gives one accuracy value per method, so "accuracy within the qualified
  range" cannot be checked against it. Say "within the limits the transfer protocol sets", and say that the
  protocol also sets the allowed difference between the sites (minimal edit if this is Version 1.0 text).

## D. Q1, Q2, Q3, Q6, Q7
- Fix the flagged sentences in your own Version 2.0 text:
  - Name the physical cause and its direction: concentration polarization in UF/DF and pore plugging by aggregates
    in the virus filter; the property a buffer can lose in a hold; the lipid envelope for low pH.
  - Use "verification-qualified" nowhere in your prose. The record's title prints as the register gives it.
  - Name the two SEC records, which of them is transferred, and the SOP only if the record names it.
  - Cut the glosses.
  - Give each code its subject at first use: CA3, findings 1 to 3, the step each viral requirement is assigned to.
- Where a flagged sentence is Version 1.0 text and not wrong, keep it. That covers "The division is one of work, not
  of accountability", "The reverse case matters more" and the comparability opening.

## E. Tables
- Table 6.4 goes (A1).
- Table 10.2: rename "Plan approved" so that its first header line does not read as a second "Plan" column, and fix
  the alignment of rows 8 to 10.
- Table 2.2: split "Criticality Tool #1" into a level column and a score column, or name both in the header.
- Table 6.1 is the builder's. Its footnote marks are superscripts in the PDF, so the review's "20–39c1)" is a
  text-extraction artefact. Look at the page image for the stray "a)" line by "Number of diavolumes" and report it
  if the builder causes it.

## F. Gate and report
- Gate with `check_render.py --render` (with `.venv/bin/python`, venv on PATH).
- Render the pdf and the docx.
- Read the page image of every table you changed.
- Refresh `.claude/work/2026-10-08_01_rev2-campaign/PTP-001_transfer.DRAFT.txt`.
- Report each item with where it was resolved, anything left and why, the passes, the page count, and any
  `<<NEEDS:>>` left (none).
