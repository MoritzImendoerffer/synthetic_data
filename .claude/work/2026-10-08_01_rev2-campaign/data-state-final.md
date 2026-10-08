# The final data state (2026-10-08, evening). Reconcile your document to this.

Every item is in the data and the helpers; compute it, never type it. STORY_BIBLE §9b is updated.

1. **Widening needs an adequate model.** A criterion widens only where the one-sided 95 % confidence
   bound of the downstream step's A-Mab worst case beats the platform value AND the downstream model
   passes the PCMP-001 adequacy tests (R² minus predicted R² within the threshold, no significant
   lack of fit). `iac_verification.csv` gains `model_adequate`, `r2_minus_pred_r2`, `p_lack_of_fit`.
   Tightening needs no adequacy test. Both directions use the one-sided 95 % bound (it had been a
   one-sided 97.5 % bound, mislabelled).
2. **What changed as a result** (`iac.csv`, columns `tightened`, `widened`, `basis`):
   - Protein A pool host cell protein: 16,000 → 16,379 ng/mg, widened on the cation exchange bound
     alone. The anion exchange bound is better than the platform value, but that model fails the
     predicted-R² test, so the platform value stands for anion exchange.
   - Cation exchange pool host cell protein stays at 400 ng/mg. Fragments at Protein A and at the
     low-pH inactivation pool stay at their a priori values (the cation exchange fragment model
     fails the test).
   - Still widened: bioreactor acidic variants (upper limit), bioreactor aggregate (also tightened).
     Still tightened: the two aggregate criteria upstream of cation exchange. Values moved slightly
     with the bound (bioreactor aggregate 6.64 %, low-pH inactivation pool aggregate 7.18 %).
   - `T.worst_case_verification` shows "Confirmed, not widened d)" where the bound was better but
     the model failed an adequacy test.
3. **Two NORs are narrowed at Version 2.0** (config `nor_v2`; `Parameter.nor` is the NOR in force,
   `Parameter.nor_characterized` the NOR the studies used; `D.characterized_nor()` is a context
   manager that makes every helper use the characterized NOR; `T.parameters_by_step` footnotes the
   narrowed rows):
   - Protein A protein load 20–40 → 20–38 g/L resin (PCR-005). At the characterized NOR the
     scale-down model is not qualified for pool host cell protein: the conclusion over the NOR fails
     with the offset at the unfavourable end of its interval. At the narrowed NOR it holds at both
     ends.
   - Low-pH inactivation hold time 60–120 → 90–120 min and temperature 19–23 → 20–23 °C (PCR-006).
     At the worst corner of the characterized NOR the predicted XMuLV clearance is below the 6.6
     claim. At the narrowed NOR it meets it.
   - Monte Carlo and PPQ now sample the NOR in force.
4. **PD-005-01.** On the three planned runs alone the Protein A model would not be qualified for
   pool host cell protein (wider offset interval); on all nine it is. The discrepancy says so openly,
   and that the decision to add runs was taken after the three-run result, with the rule and the
   criterion unchanged. "The conclusion is the same on the planned runs alone" is now false.
5. **Version 1.0 acidic variants criterion** is upper-only (≤ 25.8 %).
6. **Builders:** `T.sdm_offsets` has a two-column Runs header; `T.parameters_by_step` footnotes
   narrowed NORs; `T.frame` handles any index; `D.nor_prediction_limit` gives the single-run
   prediction limit over the NOR at manufacturing scale.

Per document:
- **PCMP-001:** items 1 and 2 (the rule text and every count), item 3 only as far as Table 4.2
  shows it (footnoted narrowed NORs; one sentence that two step reports narrowed a NOR, naming them).
- **INV-001:** items 1, 2 and 5; item 3 as "PCR-005 and PCR-006 narrow the NOR" from the
  investigation's own computed finding at the characterized NOR (the investigation closed before
  either report). Evaluate every NOR-based finding of the investigation inside
  `D.characterized_nor()`, because the investigation judged the NOR as it then stood.
- **PCP-005:** items 1 to 3. A plan states the NOR the studies are planned against (the
  characterized NOR) and may say once that PCR-005 Version 2.0 narrowed the load NOR.
- **PCR-005:** everything. The load NOR narrowing is a result of this report: state the finding at
  the characterized NOR, the narrowed NOR and the result at it, all computed. PD-005-01 per item 4.
