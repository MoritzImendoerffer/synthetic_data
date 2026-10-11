# Data state after the owner's decisions of 2026-10-11 (commits 00c0e64 … 51fa592)

Read this before you revise any document. Every value below is computed; pull it through the helpers, never type it.
Some setup assertions of the promoted documents now fail, as they should: they pin the old values.

## 1. The record: no deviations (owner, 2026-10-10)
A process characterization study is not GMP manufacture and raises no deviation. Every departure from a plan,
whether unforeseen work or a requirement not met, is a discrepancy from the plan (`discrepancy_register(DOC)`). The
execution events Version 1.0 numbered DEV-00N-0X keep their numbers as study events (`dev_register`: Event / Summary
/ Detected during / Outcome). The record section is "Study events and discrepancies from the plan" (REPORT-LESSONS
§3 rule 1).

## 2. The criteria are verified at manufacturing scale (owner, 2026-10-11)
- **Offsets in the verification.** The verification of the platform worst cases (`amab_process/iac.py`) now converts
  the scale-down pool prediction with the step's offset at its point estimate before it computes a fold or an
  increase, as PCMP-001 §7.1 rule 2 requires of every judgement. It used to divide a manufacturing-scale feed by a
  scale-down prediction. `iac_verification.csv` carries `offset_scale` and `offset`.
- **UF/DF allowance for aggregate.** PCMP-001 assumed no step after cation exchange changes aggregate. UF/DF raises
  it within its NOR. The one-sided 95 % single-run bound of the rise, from S-UFDF-UNI2 (offset applied), is 0.104
  points. It tightens the cation exchange pool criterion.
- **The criteria that moved** (`iac.csv`), with the rest unchanged:

  | Criterion | Before | Now |
  |---|---|---|
  | Bioreactor aggregate | 6.46 % | 6.30 % |
  | Low-pH (cation exchange load) aggregate | 7.02 % | 6.84 % |
  | Cation exchange pool aggregate | 5.00 % (the drug substance limit) | 4.90 %, tightened on verification |
  | Cation exchange host cell protein | 427 ng/mg | 418 ng/mg |
  | Protein A host cell protein | 17,069 ng/mg | 16,719 ng/mg |

  The verification values also moved:
  - cation exchange host cell protein fold: within the NOR 40.22 (platform 40), bound 32.93;
  - cation exchange aggregate fold bound: 1.398;
  - anion exchange host cell protein fold bound: 4.18, still above the platform 4, so the widening holds;
  - low-pH aggregate increase bound: 0.538;
  - a new row: UF/DF aggregate, increase bound 0.104, "not met", which tightens.
- **Version 1.0 → 2.0 counts.** Any count of tightened or widened criteria, or of criteria that include an A-Mab
  bound, must be recomputed from `iac.csv` and `iac_verification.csv`. The cation exchange aggregate criterion is now
  "tightened on verification".

## 3. NORs come from production (owner, 2026-10-11)
- An offset never narrows a NOR. Offsets compare laboratory results with production scale; they change PARs, not NORs.
  **The Protein A load NOR narrowing (20–40 → 20–39 g/L) is reversed**: the NOR in force is 20–40 again.
- **Flag, don't narrow.** Where a NOR does not fit inside its corrected PAR, the report flags it for discussion with
  manufacturing on whether the NOR can be improved (`D.nor_flags(key)`). On this seed no NOR is flagged.
- **Protein A pool host cell protein.** The scale-down model is not qualified over the NOR in force at the criterion
  (`D.offset_qualification`): the conclusion holds at the offset estimate and fails at the low end of its interval.
  PCR-005 states this, does not narrow the NOR, and flags it for discussion with manufacturing.
- **Bioreactor acidic variants.** They still fail at the least favourable NOR combination. That is a single-run
  judgement, not a PAR flag; the combined alert covers it.

## 4. Other decisions of 2026-10-11
- **Diavolumes are one-sided.** Their NOR is a minimum, at least 7 DV (`nor_one_sided: low`, printed "≥ 7"). The
  buffer-exchange criterion is the minimum diavolumes plus the drug substance buffer within release limits.
- **Bioreactor:**
  - pH is held by base addition, and pCO2 by the CO2 fraction of the sparge gas (PCP-003 change 14);
  - classes: osmolality CPP, dissolved oxygen GPP, basal medium KPP;
  - the combined alert: pH above 6.79, pCO2 above 101 mmHg and temperature below 35.39 °C on this seed, from
    `D.acidic_mitigation()`;
  - the harvest action limit for acidic variants, 18.72 %;
  - acidic variants trended against initial viable cell concentration in production.
- **Classes kept as configured and argued as a judgement:** filtration pressure (WC-CPP, A-Mab's basis), anion
  exchange flow rate (WC-CPP), cation exchange elution flow rate (GPP; the DNA p = 0.044 is a false positive by the
  model's construction, so its practical relevance is argued).
- **Cation exchange stop collect.** The data stand as observed: aggregate rises with the AU setting, against the
  expected mechanism, and no cause is given.
- **Held pools.** PCMP-001 Version 2.0 §5 judges a held pool against the criteria it must meet on entering the next
  step. Only the expected entering level and the reading of the change are the report's approach.
- **A-Mab leaves UF/DF out on p.114** (not p.86).
- **No adequate model, no PAR.** An output with no adequate model has no PAR: `D.par_table` prints "n.a.".
- **The criteria table.** `T.criteria_results` shows the 95 % limits of a single run over the NOR, the statistic that
  decides each verdict, and wraps its header.
- **Practical relevance.** A significant effect is practically relevant only when it has implications for product
  quality or process consistency. Name such judgements as judgements. PCMR-001 will carry the campaign-wide
  demonstration.
