# PCR-006 after the content review and the factual check: what to change (one revision, same author)

Inputs, in this folder: `factual-PCR-006.md` (17 errors and minor items, each with its fix) and
`content-review-PCR-006.md` (the fresh judge's flags). Read both, and `procedures/REPORT-LESSONS.md`. Where this
note gives a resolution, write to it; otherwise resolve each flag yourself and say in your report what you did.
Every value stays computed and every deciding word computed or asserted.

## A. What changed under the draft (2026-10-10, afternoon)
1. **DEV-006-04** (deviations.csv): the input pool of the design runs was not tested for aggregate, acidic
   variants and A-Mab concentration, as PCP-006 requires; the increase across the step is taken against the
   nominal load of the step model. Record it in the deviations section and where §3.4, §4.3 and §7.7 rely on
   the load; §4.3 "Every output was measured on every run" goes.
2. **PCP-006 is re-opened** (today) to state the widening rule as PCMP-001 §7.5 rule 2 does (the first three
   adequacy criteria, not an exact fit; the fourth does not decide). Re-read its rendered §7.4 before you write
   about it; if it states the three criteria, the widening is no departure from it.
3. **S-VI-WC** is described as run: pH at the low end of its PAR, hold time and temperature at the upper ends
   of their NORs in force. Not "the harshest combination within the PAR" (the hold-time and temperature PARs
   reach further). The PD-006-03 subject and the builder caption were changed accordingly.
4. **Builders**: true minus signs; `T.criteria_results` note c ("less the offset ... where one is known");
   `T.criteria_change` note e ("a model that meets the first three adequacy criteria"); `D.fig_par` for XMuLV
   ("Others at their NOR combinations", "range of mean predictions over the NOR combinations"). Re-render.
5. **Font floor** (check_render, now that the table-fit false positive is fixed): text below 7.9 pt on pp. 41,
   51, 73 (Tables 7.4, 7.12, D.1). Fix each (shorter headers, fewer columns, or landscape).

## B. The factual check: resolutions
Resolve errors 1 to 17 and the minor items as `factual-PCR-006.md` gives them. In particular:
- **Error 2, the NOR decisions**: describe the three steps as the config holds them (the factual file lists
  them), each with the margin the engine computes at the NOR of that stage.
- **Error 3, the influence analysis**: limit "no conclusion changed" to what holds under every deletion (the
  NOR in force inside every PAR, the claim over it, the decision to move the NOR, the classes) and state the
  run-5 dependence of the XMuLV PARs and of the temperature effect, with the values computed through the
  helpers (REPORT-LESSONS §2 rule 3).
- **Error 4c**: the near-equivalent model comparison is the sensitivity analysis of the model selection
  (REPORT-LESSONS §2 rule 2), recorded within PD-006-04; say so, not "both recorded as discrepancies".
- **Error 4d**: add who bears the risk of the widening (PCMP-001 §7.5 item 1).
- **Error 4e**: report adjusted R²; compare S-VI-UNI acidic variants as the plan says; fix "recorded within
  PD-006-05"; judge the residual trends as PD-006-07 states, or tell me if the register is wrong; report the
  fragment model against criterion 4.
- **Error 11 and Table 7.13**: PCMP-001 §7.5 confirms a platform worst case on the point prediction; say that
  the confirmation for fragments and acidic variants rests on a model that does not meet PCMP-001 §7.2, as a
  limitation, rather than "confirms nothing".

## C. The content review: coordinator's resolutions
- **D-001 stays.** Table 7.4 "PAR (set-point)" and the left panels of Figures 7.1 and 7.2 present the engine's
  values under their own headings (your brief §5c). Add no sentence about where the other factors were held.
- **Q5 science**: correct the first-order kinetics claim (the log reduction is not proportional to time in the
  data, and no pH × time interaction is significant: describe the response surface as the data show it); the
  low-pH acidic variants come from direct amide hydrolysis, not succinimide formation; low pH unfolds the CH2
  domain of the antibody as well as acting on the envelope (§2.1 and §5.4 already say so, so "and not on the
  antibody" goes); the step contributes one of three claims to the cumulative XMuLV requirement, it does not set
  it; pH and hold time have effects of the same size (0.612 and 0.605, SE 0.123): do not call pH "the largest";
  the S-VI-OFAT acidic-variant difference is significant (Holm p = 0.025): report it with its size against the
  criterion, not "beyond the precision of the methods"; "meets its claim of 6.60" (6.77 the predicted minimum);
  the A-Mab concentration class: state what the data can exclude at the least favourable corner, and that the
  class rests on that power; designs at one concentration say nothing about a concentration effect;
  "routine manufacture never holds longer" goes (a hold beyond the NOR is a deviation).
- **Zero scatter of the acidic variants** (33 results, against an icIEF repeatability of 0.41 points in
  S-VI-OFAT): state the fact and its consequence (no adequacy test; the output judged on its measured results)
  without inventing a cause. This is an open owner question.
- **Q3 glosses and self-certification** ("this report says so", "applies it as stated", "reported as what it
  is", "not a more stable product", the stepwise defence, "still right"): cut them.
- **Q1, Q2, Q6, Q7**: fix each flagged sentence (name the physical cause and its direction; "XMuLV clearance"
  for "the attribute the step sets"; criteria named, not numbered; discrepancy codes with their subject).
- **Tables and figures**: fix your own (2.1 "CEX/icIEF", 3.1, 4.3 labels and order, 5.4, 5.9, 7.2, 7.4
  precision, 7.5 header collision, 7.8, 7.9, 13.2 cell length); abbreviations RSM, OFAT, DoE, HPLC, CEX; ICH Q11
  in the references; one spelling of "centre". Leave the shared builders as they are.

## D. Gate and report
Gate with `check_render.py --render` (with `.venv/bin/python`), render the pdf and the docx, read the page image
of every table and figure you changed, refresh `.claude/work/2026-10-08_01_rev2-campaign/PCR-006_viral_inactivation.DRAFT.txt`.
Report each item with where it was resolved, the flags you left and why, the passes, the page count, and any
`<<NEEDS:>>` left (none).
