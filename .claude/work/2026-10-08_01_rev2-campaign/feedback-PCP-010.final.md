# PCP-010: final pass (review run 2)

Fix these and nothing else. The draft is `pc_package/PCP-010_ufdf.DRAFT.qmd`. The review is
`content-review-PCP-010.run2.md` in this folder; `feedback-plans-shared-2026-10-10.md` still applies.
Every value stays computed and every deciding word computed or asserted. Several flagged sentences are
Version 1.0 text (checked against the frozen Version 1.0 PCP-010): "Quality Assurance approves this plan
before any run is executed", "the three parameters reach the product by different routes", the TMP
sentence "without raising throughput", and "One quantity cannot be matched. The ratio of pump
displacement to system hold up volume ...". A Version 1.0 rule stays word for word. A Version 1.0
description that is physically wrong is corrected and listed (B below).

## A. Errors and contradictions

1. **QA approval (§10).** Keep the Version 1.0 sentence. Add once, beside it, that this Version 2.0 is the
   amendment issued after the runs and approved on its effective date (as §1.1 says, name the corrective
   action that amended each step plan rather than "CA2" alone).
2. **Offset timing.** PCMP-001 §7.1 reads: "The scale-down runs at set-point are made, and the offset of
   each output is estimated, before the first characterization run of the step. The decision whether the
   model is qualified for an output needs the response-surface model of the step ... That decision is
   therefore made at analysis." State the requirement once, as PCMP-001's, not as a record. Version 1.0
   did not name the manufacturing-scale batches of the comparison, so say once that PCR-010 names them and
   states when the offsets were estimated. Delete the other two statements of the requirement and make §11
   step 1 the qualification runs, without the estimate.
3. **Classification (§1.1 item 6 vs §7.4).** PCMP-001 §6.2: "An attribute is called affected by a
   parameter when a term that contains the parameter is significant at that level." PCMP-001 §7.7: "A
   significant effect that is too small to move the attribute appreciably within the PAR does not by itself
   make a parameter critical." Item 6 states what §7.7 says, in those terms, and does not say the
   parameter can then be a key process parameter (PCMP-001 does not say that). §7.4 keeps the Version 1.0
   classification sentence and says how PCMP-001's two rules read at a step with no response-surface
   model, or that PCR-010 states it.
4. **Buffer exchange.** Keep the Version 1.0 criterion (conductivity and pH at the plateau of the
   formulation buffer). Say once that the analysis of §5.5 treats conductivity only and that Version 1.0
   set no analysis for the pH, so PCR-010 states its approach. Make §5.4 and §6.2 agree with Tables 5.1 and
   5.2: the buffer-exchange criterion is read on the diafiltration series, not on the final retentate, and
   the diavolume series carries the extra sampling (retitle Table 5.2 or split it so that it does not put
   that sampling in every run; fix its purpose cell).
5. **"a test of equivalence in three parts"** (§1.1): Version 1.0 §7.1 is a test for a difference at
   α = 0.05 on step yield, permeate flux and the change in aggregate, with the final concentration within
   the variability of the A280 method, and a significant difference assessed for size against §7.2 before
   the model is rejected. Describe it so.
6. **"The scale-down model is qualified by its offset from manufacturing scale, as PCMP-001 §7.1
   requires"** contradicts §7.1 of this plan (the decision cannot be made as PCMP-001 states it, since the
   step has no response-surface model). One statement, consistent in both places.
7. **The in-process readings** ("not validated assays ... not to release a run"): they are the basis of
   the buffer-exchange criterion and of the lower diavolume edge. Say what they are and what they decide,
   and cut "not to release a run".
8. **"They arise in the production bioreactor, and aggregate is reduced at the cation exchange step."**:
   acidic variants also form wherever the antibody is in solution, and the low-pH step may change them
   (PCMP-001 §7.2); aggregate also forms at the low-pH elution and hold. Correct.
9. **Objective (iv)** and §8: the PAR basis lists the same criteria in both places.
10. **"with the other parameters at the values the commercial step will hold"**: at their set-points
    (Table A.1).
11. **Pump passes: "a limited number of times"** vs "many times" (§4.1): one statement.
12. **"The revision history now gives the approval date."**: say the date on which Version 1.0 took
    effect, its approval date, as the revision history's "Effective date" column shows.
13. **The common load pool** does not constrain the run order: say what the single pool does constrain,
    or cut the clause. If the single assay of the load pool for the whole study is Version 1.0 text, keep
    it and add nothing.

## B. Version 1.0 descriptions corrected (one change in §1.1, each correction named)

Replace "Descriptions of the process that Version 1.0 stated wrongly are corrected without a change to the
design (Section 4.1, Section 5.1, Section 5.5)" with a list that names each correction: what Version 1.0
said and what this plan says instead. The corrections:
- **TMP and the wall concentration** (§4.1, twice, and §4.3): below the point where the polarization layer
  limits the flux, a higher TMP drives more permeate and raises the antibody concentration at the wall.
  Beyond it the flux no longer rises, the wall concentration is at its limit, and extra pressure compacts
  the layer at the wall. All three sentences say the same.
- **The quantity that cannot be matched** (§5.1, §12): with crossflow and loading matched per unit area,
  the number of passes through the pump is the same at both scales. What differs is the hold-up: the bench
  system holds a larger share of its batch in its recirculation loop and has a larger surface-to-volume
  ratio, so more antibody is lost to hold-up and more of it meets surfaces and air–liquid interfaces per
  gram (data-state note of 2026-10-10, item 7). Name that quantity in "One quantity cannot be matched."
- **Shear** (Q5 items 21, 22): shear alone causes little antibody aggregation. Interfaces, cavitation in
  the pump and particles shed by it are the usual causes. The pump is not where the antibody is most
  concentrated. How readily an antibody aggregates depends on its colloidal stability and
  self-association, which differ between antibodies.
- **Viscosity at the DS target** (Q5 item 23): do not say it "rises steeply" at the target unless the
  config or a source gives A-Mab's viscosity there. Say only that viscosity rises with concentration.
- **The buffer exchange curve** (Q5 items 24, 25): the residual process buffer components fall roughly
  exponentially with diavolumes, and the conductivity approaches the value of the formulation buffer from
  above or below. Donnan and volume-exclusion effects can leave the retentate pH and excipient levels off
  the buffer values at high concentration.
- **Duration** (Q5 item 26): the final concentration also sets how long the operation lasts.
- **Expectations** that are Version 1.0 text stay ("The effect on aggregate is therefore expected to be
  small.", "expected to be conservative", the §5.5 curvature sentence). If one is not Version 1.0 text,
  delete it: it was written with the results known. Where a correction above removes the premise of a
  Version 1.0 expectation (conservative "by shear", more pump passes), keep the expectation, mark it as
  Version 1.0's, and say that PCR-010 compares it with the data.

## C. The rest of the review
Fix the flagged sentences of Q1, Q3, Q6 and Q7 where the fix is local: name the physical cause and its
direction in the clause (crossflow raises wall shear and lowers the wall concentration; the final
concentration sets the viscosity and, through the bulk concentration, the flux), cut the filing glosses,
say each fact once (the offset timing, no IAC at this step, the non-applying PCMP-001 rules, the aggregate
offset subtraction, the fragments scope, the SEC noise rule, the PA3 sentence), name each document at
first use in a passage ("the report PCR-010", "the master plan PCMP-001"), and give "Three bounds apply"
its word (limitations). Add CE-SDS, HPLC and UV to the abbreviations; fix the fused footnote marker in
Table 5.2 and "Fixes the input" ("Measures the input"). Leave the shared builders as they are.

## D. Gate and report
Gate with `check_render.py --render`, render the pdf and the docx, read the page image of every table you
changed, and refresh `PCP-010_ufdf.DRAFT.txt` with `pdftotext -layout`. Report each item with where it was
resolved, anything you left and why, the check_render passes, the page count, and any `<<NEEDS:>>` left
(none).
