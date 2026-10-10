# Data state after the owner's decisions of 2026-10-10 (data batch, commits 7768d43 and after)

Read this before you write or revise any document. It supplements `data-state-2026-10-09b.md`, which
still holds. Every value below comes from the data or the config. Pull it through the helpers; never
type it from here. Some assertions in an existing draft will now fail, as they should.

## 1. Owner's decisions (Q1 to Q8)

1. **A held pool is judged against the criteria in force** for the next step's load, as PCR-005 does
   (tightened and widened on verification). Not the a priori values.
2. **The design space is drawn on the single-batch limit.** `D.design_space_grid(key)` now puts a
   grid point inside when, for every quality attribute, both ends of the 95 % prediction interval of
   a single run lie within the criterion (offset applied), and for viral clearance when the mean
   prediction does. `basis="mean"` gives the former convention, for comparison only. Name the
   statistic wherever you state a design space. The region is smaller than before where a quality
   attribute binds (bioreactor and Protein A); compute every fraction.
3. **The HCP ELISA has a coverage figure.** `dev_methods.csv`, AMV-3012: `coverage_pct` (80) and
   `coverage_method` (2D western blot against the platform CHO host cell protein antigen); scalar
   `amv_3012_coverage`. A risk argument about the detection of host cell protein may cite it.
4. **A dose, and DNA in physical units.** `meta.dose`: A-Mab's weekly 10 mg/kg (A-Mab p.26), for a
   70 kg reference adult. The body weight is our assumption: say so wherever the dose matters.
   `_pcpkg.DOSE_MG` (700 mg) and `dna_ng_per_dose(pg_per_mg)`. Residual DNA is carried in pg per mg of
   antibody through the train and judged in ng per dose at the drug substance. The anion exchange DNA
   clearance of the model is 5 logs (was 4), so the drug substance meets A-Mab's < 10^-3 ng/dose
   (`capability.csv`, `monte_carlo.csv`). Every 5-log AEX pool is below the qPCR LOQ (item 9).
5. **The selected model decides among near-equivalent models.** A qualification or conclusion that
   differs among the models within 2 AICc units is reported as a sensitivity, not as the decision.
6. **The out-of-trend rule of DEV-005-02 is in the record.** `deviations.csv` column `oot_rule`;
   scalars `dev_005_02_oot_level` (0.99) and `dev_005_02_first_over_reported`, now **2.5** (was 1.8:
   the first result as recorded lay inside the rule's interval, so the record called a result out of
   trend that was not). `D.oot_check("protein_a", "leached_protein_a_ppm", run, value)` gives the
   interval and the verdict. The first result is now above the range of the other runs of the design.
7. **UF/DF qualification data (S-UFDF-SDM)** are in `sdm_qualification.csv`: 3 scale-down and 5
   manufacturing runs of step yield, aggregate, final concentration and permeate flux (`flux_lmh`).
   Offsets: `D.sdm_offset("ufdf", ...)`, `T.sdm_offsets(["ufdf"])`. The small skid holds more of its
   batch in the recirculation loop, so it gives a little more aggregate and a lower yield. PCMP-001's
   list of compared outputs now includes UF/DF (computed).
8. **Harvest has no scale-down qualification.** There is no laboratory-scale disk-stack centrifuge,
   only pilot scale (owner). PCR-004 records the qualification that PCP-004 planned and that was not
   performed as a deviation; its register entry is added when PCR-004 is prepared.

## 2. Criterion 4 of PCMP-001 §7.2, one definition for everyone

`D.residual_influence(key, resp)` tests the residual and influence criterion as the Version 2.0 plans
state it: the regression of the absolute residuals on the predicted values and of the residuals on the
order of execution (a second block continues the order), each at `THRESHOLDS["residual_alpha"]`, and
Cook's distance against `THRESHOLDS["cook_factor"]`/n. At every DoE step at least one adequate selected
model fails it, so every DoE report carries an influence-analysis discrepancy: PD-003-04, PD-005-02,
PD-006-07, PD-007-02, PD-008-03, PD-009-02 (`discrepancy_register(DOC)`). A plan states the tests with
the two thresholds from `THRESHOLDS`, never as typed numbers.

## 3. Results the Version 1.0 plans required and the record lacked (owner: "Attributes in scope should be measured unless justified")

New columns, each from its own random stream; no earlier result moved.
- **Univariate studies of the designed steps** (`univariate_studies.csv`), as each Version 1.0 plan
  listed its responses. PCP-005 §6.4 required "the same responses measured as in the multivariate
  designs", so S-PA-UNI now has `lmw_sec_pct` and `hmw_sec_pct` (SEC, the method before AMD-001). Its
  samples were not retained beyond 30 days, so the April 2026 retests (S-PA-RET, S-VI-RET) covered only
  the retained response-surface samples, as the promoted documents say: fragments by nrCE-SDS were not
  measured for S-PA-UNI, and its SEC result is biased in this matrix (information only). That is the
  justification PCR-005 states. PCP-006, PCP-007 and PCP-008 Version 1.0 listed no fragment result for
  their univariate studies, so none was added. PCP-007 §6.4 required "the responses of §5.3", which
  include residual DNA and leached Protein A: S-CEX-UNI now has them (load and pool, as below).
- **The spiked anion exchange run** of the flow-rate study at the high end of the range: one row of
  S-AEX-UNI with `spiked` True, `xmulv_lrf` and `mvm_lrf`; its other responses are not reported.
- **Residual DNA and leached Protein A at cation and anion exchange**: every response-surface run
  (`doe_cex_rsm.csv`, `doe_aex_rsm.csv`: `dna_load_pg_mg`, `dna_pool_pg_mg`, `lpa_load_ppm`,
  `lpa_pool_ppm`) and the qualification runs (`sdm_qualification.csv`: pools). A result below the
  method's LOQ carries no value and a `*_lt_loq` flag (AMV-3014 qPCR LOQ 1 pg/mg; AMV-3016 ELISA
  0.25 ppm). Every anion exchange DNA and leached Protein A pool is below the LOQ: a clearance is then
  stated as "more than" load over LOQ. Neither attribute has an intermediate criterion at these steps.
- **Host cell protein and DNA in the bioreactor broth**: `harvest_hcp_ng_mg`, `harvest_dna_pg_mg` on
  every screening, response-surface and univariate run (not the augmentation runs, not the
  qualification). Information on the attributes the register assigns to the bioreactor; no criterion.
- **Harvest S-HAR-UNI2**: fragments by nrCE-SDS (`lmw_cesds_pct`) and residual DNA (`dna_out_pg_mg`) in
  the clarified harvest. **UF/DF S-UFDF-UNI2**: acidic variants by icIEF (`acidic_variants`).
- **Still not measured** (process outputs, recorded as departures in the reports): viable cell
  density, viability and titre in the bioreactor studies; bed pressure (AEX qualification); flux
  decay and integrity test (virus filtration qualification); the set-point runs the Version 1.0
  plans put in the univariate studies of Protein A, cation and anion exchange (the set-point reference
  is the qualification runs).

## 4. Smaller changes
- The harvest step role (`UNIT_OP_ROLE`) now reads "Primary recovery and clarification, where
  fragments form during the harvest hold", as the CQA register and PCMP-001 say.
- New method records in `dev_methods.csv`: AMV-3014 (qPCR) and AMV-3013 (icIEF).
- The revision history of a plan no longer says "re-analysis of the studies" (reports keep it).
