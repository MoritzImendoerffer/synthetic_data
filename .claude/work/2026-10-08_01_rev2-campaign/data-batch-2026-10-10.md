# Data batch of 2026-10-10 (owner's answers Q1 to Q8; "go ahead with the data batch")

Coordinator's checklist. Rule for every new measurement: a NEW column from a NEW random stream key,
so no existing result moves (byte-identity of the Version 1.0 re-analysis). Existing columns of every
CSV must be identical before and after (checked with a pandas comparison, not only `git diff`).

## Decisions being implemented
- Q1 held pool judged against the criteria in force (no change; PCR-005 already does).
- Q2 design space on the single-batch limit: `D.design_space_grid` judges a quality attribute by both
  ends of the 95 % prediction interval of a single run (offset applied), viral clearance by the mean.
- Q3 HCP ELISA coverage in the method record (AMV-3012): 80 % by 2D western blot (platform value,
  owner's choice of "add coverage").
- Q4 a dose: A-Mab "weekly dose of 10 mg/kg" IV (amab.txt, §2.1.1); 70 kg reference adult
  (assumption, labelled) = 700 mg per dose. DNA carried in pg/mg through the train (harvest 2.0e5
  pg/mg = the Protein A load data), converted to ng/dose at the drug substance. With 8.0 logs of DNA
  clearance the drug substance would sit at 1.4e-3 ng/dose, above A-Mab's < 1e-3 ng/dose; A-Mab's
  harvest DNA is 1.7e3 ppm and its claim implies about 9 logs. AEX DNA clearance set to 5.0 logs
  (typical flow-through value): drug substance about 1.4e-4 ng/dose. Report this calibration choice
  to the owner.
- Q5 measure the attributes in scope that a Version 1.0 plan promised (owner: "Attributes in scope
  should be measured unless justified"); process outputs (bed pressure, flux decay, integrity test,
  VCD, viability, titre) stay recorded departures.
- Q6 selected model decides (no change).
- Q7 out-of-trend rule for DEV-005-02: "outside the two-sided 99 % prediction interval of a single
  result, from the selected model of the design fitted without the result under review, at the run's
  settings". The recorded first result (1.8 x re-assay = 3.82 ppm) is inside it (1.38 to 5.12 ppm),
  so the record was inconsistent; the ratio becomes 2.5 (5.31 ppm). Helper checks it; test asserts.
- Q8 UF/DF qualification data for S-UFDF-SDM (4 outputs; small scale-down offset in aggregate from
  the extra pump passes); UF/DF added to PCMP-001 §5's list of compared outputs (coordinator edit).
  Harvest: no laboratory-scale disk-stack centrifuge exists, only pilot scale (owner); PCR-004
  records the missing qualification as a deviation (config, when PCR-004 is prepared).

## Checklist
- [ ] config: dose; DNA pg/mg at harvest; AEX dna_lrv 5.0; AMV-3012 coverage; AMV-3014 record;
      DEV-005-02 ratio + OOT rule; UF/DF SDM; method plan entries for univariate fragments
- [ ] model: bioreactor DNA keys; ufdf DNA conversion by dose (and a flux metric); protein_a_extras
      reads the harvest DNA from config
- [ ] analytics: UF/DF SDM rows; univariate fragments (S-PA/VI/CEX/AEX-UNI); AEX univariate viral at
      the high setting; CEX/AEX RSM DNA and leached Protein A; CEX/AEX SDM DNA and leached Protein A;
      bioreactor HCP and DNA (designs, univariate, SDM); harvest UNI2 fragments and DNA; UF/DF UNI2
      acidic variants
- [ ] engine: design_space_grid single-batch; residual_influence (criterion 4); oot_check; dose helper
- [ ] _pcpkg: UNIT_OP_ROLE harvest; SOP-3015 in CEX/AEX refs; computed influence-analysis
      discrepancy for every DoE report without a configured one
- [ ] tables: sample_size caption, adequacy_remedy note; methods_by_study note on the retests
- [ ] regenerate; compare existing columns; tests; briefs; data-state note; REPORT-LESSONS update
- [ ] re-render promoted documents and drafts; list broken asserts; re-open PCR-005 (fix pass) and
      PCMP-001 (UF/DF list); INV-001/PCP-005 only if their text describes the retest scope
