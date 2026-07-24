# synthetic_data

Synthetic data around pharmaceutical manufacturing for various NLP tasks.

This repository generates realistic, **fully reproducible** biopharmaceutical
manufacturing documents from a seeded process model — useful both as standalone
CMC deliverables and as synthetic corpora for NLP (document classification, NER on
process parameters/CQAs, table extraction, QA over GMP-style text).

## A-Mab Process Characterization

A **Process Characterization (PC) Report** (Word + PDF) and a **post-PC Process Risk
Assessment / FMEA** (Excel) for the *A-Mab* drug substance — a humanized IgG1
monoclonal antibody. Both documents are generated from a seeded Python model of the
entire drug-substance train, so every figure, table and number can be re-created with
a single command.

Grounded in three source documents (`original_data/`):

- **A-Mab Case Study v2.1** (CMC Biotech Working Group, 2009) — process model, CQAs,
  risk methodology.
- **PDA Technical Report 60** — Process Validation: A Lifecycle Approach — report
  structure and Stage-1 expectations.
- **ISPE Good Practice Guide (2023)** — Practical Implementation of the Lifecycle
  Approach to Process Validation — Stage-1 statistics, design space, control strategy.

### Deliverables

| Deliverable | Path |
|---|---|
| Process Characterization Report (Word) | `report/process_characterization.docx` |
| Process Characterization Report (PDF) | `report/process_characterization.pdf` |
| Post-PC Process Risk Assessment (FMEA, Excel) | `risk_assessment/A-Mab_Post-PC_Process_Risk_Assessment.xlsx` |

### Reproduce everything

```bash
make env      # install Python dependencies (one time)
make all      # data -> figures -> report (Word + PDF) -> FMEA workbook
```

Requires **Quarto** (with a LaTeX engine for PDF) and **Python 3.11+**. Individual
stages: `make data`, `make figures`, `make report`, `make fmea`, `make test`,
`make clean`. Everything derives from the master seed in `config/parameters.yaml`
(`meta.seed`), so re-running reproduces byte-identical datasets.

### How it fits together

```
config/parameters.yaml     <- single numeric source of truth (params, ranges,
                             classifications, CQAs, criticality, risk scales,
                             model coefficients grounded in A-Mab Table 3.16 etc.)
        |
        v
amab_process/              <- the process model (Python package)
  core.py                  <- Stream / StepResult / response-surface helpers
  config.py                <- config loader
  doe.py                   <- DoE designs (factorial, fractional, central-composite)
  unit_ops/                <- one module per unit operation (Steps 3-10)
  process.py               <- chains the train (Process.run_batch)
  studies.py               <- DoE datasets, PPQ, Monte-Carlo capability
  viz.py                   <- validated plotting palette / style
        |
        v
scripts/generate_data.py   <- writes outputs/data/*.csv + outputs/report_values.json
scripts/make_figures.py    <- writes outputs/figures/*.png
        |
        |--> report/process_characterization.qmd  -> Word + PDF (Quarto executes Python)
        \--> risk_assessment/build_fmea.py         -> Excel FMEA workbook
```

### The process model

A **semi-mechanistic hybrid** of the eight A-Mab drug-substance unit operations:

- **Production bioreactor** — logistic growth / integral-productivity kinetics for
  VCD, viability and titer, plus a second-order response-surface model (A-Mab
  Table 3.16 coefficients) mapping pH, temperature, CO₂, osmolality and culture
  duration to the cell-culture CQAs (afucosylation, galactosylation, high mannose,
  aggregate, acidic variants) and the harvest HCP/DNA load.
- **Protein A, low-pH viral inactivation, CEX, AEX, virus filtration, UF/DF** —
  mechanistic mass balances (yields, clearance factors, log-reduction values)
  combined with response surfaces for the parameter→CQA relationships each step
  controls (HCP, aggregate, viral clearance, leached Protein A, DNA).

All randomness is seeded; `make test` checks reproducibility, mass balance,
in-spec CQAs at set-point, viral-clearance margin, capability, and that the DoE
reproduces the documented A-Mab effect directions.

### Risk assessment (FMEA)

A-Mab-aligned post-characterization FMEA: **RPN = Severity × Occurrence × Detection**,
with the CPP rule **Severity ≥ 8 or RPN > 72**. The workbook shows the RPN *before*
and *after* characterization (and the resulting control strategy), making the risk
reduction explicit, and splits critical parameters into CPP vs well-controlled CPP
(WC-CPP) per the case-study designation.

### Source-text extracts

`refs/text/*.txt` and `refs/grounding/*.json` are cached extractions of the source
PDFs used to parameterize the model, re-creatable with
`python scripts/extract_sources.py` (PyMuPDF).
```
