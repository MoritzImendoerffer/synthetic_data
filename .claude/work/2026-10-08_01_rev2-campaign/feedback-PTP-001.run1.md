# PTP-001 after the factual check and the content review: what to change (one revision, same author)

Inputs, in this folder: `factual-PTP-001.md` (11 errors, each with its fix) and the content review summarised in
section C below (judge: Claude Opus 5.5, read only the PDF text; answers 1 No, 2 No, 3 Yes, 4 No, 5 Yes, 6 No,
7 No). Where this note gives a resolution, write to it; otherwise resolve each flag yourself and say in your
report what you did. Every value stays computed and every deciding word computed or asserted. The transfer
elements, gap analysis and PPQ strategy stay those of Version 1.0; no study result enters as a basis.

## A. What changed under the draft (2026-10-10)
1. **Builders**: `T.parameters_by_step` has no "Study" column (univariate parameters carry a note mark) and fits
   its page; its moved-set-point note reads "the set-point in the characterization plan" (factual error 9); the
   virus filter's role in `UNIT_OP_ROLE` names its XMuLV credit (factual error 6, content review on Table 2.1);
   the bioreactor role reads "Forms the glycan, charge-variant and aggregate attributes"; `related_docs_md("PTP-001")`
   gives RA-001, PCMP-001 and PCMR-001 relationships as documents under this plan; true minus signs. Re-render and
   check the table fit (the footer check now catches the overflow you reported).
2. **PCMP-001 §7.8** now says "every study that measures fragments, at every step, measures them by nrCE-SDS"
   (your sentence repeats the old wording: factual error 11). **PCMP-001 §3** now gives the origin of the fragments
   criterion (sponsor-set when fragments joined the register at Version 2.0).

## B. The factual check: resolutions
Resolve errors 1 to 11 as `factual-PTP-001.md` gives them. In particular:
- **Error 1, the 30 studies**: use the 27 studies the Version 1.0 reports reported (exclude S-CEX-FRC, S-PA-RET and
  S-VI-RET, which produced only fragment results that Version 1.0 did not report), computed, or relabel the table
  as the studies executed before the Version 1.0 reports were approved and say that three gave fragment results
  only. Choose one; the caption, §10 and §1.1 item 1 say the same.
- **Error 2**: AMD-001 predates INV-001; write it as PCMP-001 §1.1 item 4 does.
- **Error 3, residual DNA**: the drug substance criterion is A-Mab's claimed acceptable range, met through
  clearance ("None as DNA is consistently cleared from the process", A-Mab p.47). Release testing does not test DNA
  against it; say so where §6.3 and §7 speak of release testing against Table 2.2, and give the dose used to express
  it (`_pcpkg.DOSE`, the 70 kg reference adult being an assumption). The same applies to the cumulative viral
  requirements, which no batch test measures (content review).
- **Error 4**: the Protein A load from the titre is PCR-005's discrepancy PD-005-06: cite it, or cut the paragraph
  to the transfer need (the titre method must be transferred).
- **Error 5**: restore the Version 1.0 sentence on the outputs compared (viable cell concentration, titre, pool
  volume ...); the reports record that the record lacks them.
- **Errors 7, 8, 10, 11**: as the factual file gives them.

## C. The content review: coordinator's resolutions
- **Reissue scope**: the Protein A load sentence (B, error 4); the S-CEX-FRC result as the basis of "the receiving
  site therefore needs nrCE-SDS" (point to PCMP-001 §7.8 and AMD-001 as the basis, not the study result); the
  restated harvest gap basis (declared and a priori: keep, listed); "Its transfer should therefore be completed and
  reviewed before the engineering batches are run" (cut if it is your Version 2.0 sentence).
- **Q5 science and contradictions**: "qPCR is the least precise" (the infectivity titres are less precise: compute
  the ranking across the methods with comparable units, or restrict it to the methods in %RSD); bed height, linear
  velocity and flux are the quantities held constant across scale, not ones that "depend on scale"; the virus filter
  runs at constant pressure and UF/DF at a set TMP (correct "scaled by area at constant flux, which holds the
  transmembrane pressure" if it is wrong for either); "A change in the gas path therefore does not change the two
  transfers equally" (name the cause: CO2 is far more soluble than O2, so its removal is limited by gas flow while
  O2 supply is limited by kLa); "The remaining elements in Table 4.1 carry a difference in documentation, not in the
  process" vs Table 4.1 and §8 (methods and raw-material lots differ: correct); "However, the engineering batches
  confirm that expectation" (they have not run: "will confirm"); the basis of the engineering batches (Table 10.1:
  the master batch record after PCMR-001) vs "the ranges in the current process description" (make them agree, as
  Version 1.0 had it); Table 8.1 row 1 and Table 4.1 row 1 cannot be carried out as written now (the receiving site
  has not run the process): if this is Version 1.0 text, keep it and say once that the comparison is made at the
  sending site's manufacturing scale; Table 6.2 vs Table 6.3 SEC methods (AMV-3011 and AMV-3221: name both and what
  each is); "Each of these steps either binds the impurity ... or elutes the antibody away from it" (Protein A binds
  the antibody while the impurities pass: correct); "SEC remains the method for aggregate, where no such interference
  applies" (PCMP-001's sentence: keep it as PCMP-001's, attributed); "Each Process Characterization Plan ... commits a
  study" (one to five studies per step); "Aggregate forms in the culture" (and at the low-pH steps).
- **Q4**: Table 2.2 criteria have no basis (A-Mab's except fragments, as PCMP-001 §3 now says: add the note); the
  method transfer success criterion has no numbers (Version 1.0 text? If so keep it and say the transfer protocol
  sets the limits); the viral claim sums are stated as met with the margin against the titre-assay precision noted.
- **Q1, Q2, Q3, Q6, Q7**: fix the flagged sentences in your own text (name the interaction and direction for
  afucosylation and galactosylation; "virus spiking study" for "spiking model"; cut the "A reader who wants ..."
  sentences and the other glosses and restatements; name each code's subject at first use).
- **Tables**: Table 6.1 is the builder's (A1); Table 2.2 (the criticality and Tool #1 ranking: say VH for viral
  clearance is by rule, as PCMP-001 §3 does); Table 6.3 (units per row in a column header, or split the column);
  Table 6.4 is the builder's.

## D. Gate and report
Gate with `check_render.py --render` (with `.venv/bin/python`), render the pdf and the docx, read the page image
of every table you changed, refresh `.claude/work/2026-10-08_01_rev2-campaign/PTP-001_transfer.DRAFT.txt`. Report
each item with where it was resolved, the flags you left and why, the passes, the page count, and any `<<NEEDS:>>`
left (none).
