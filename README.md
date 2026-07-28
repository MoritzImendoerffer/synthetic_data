# synthetic_data

Synthetic data around pharmaceutical manufacturing for various NLP tasks.

This repository generates realistic, **fully reproducible** biopharmaceutical
manufacturing documents from a seeded process model — useful both as standalone
CMC deliverables and as synthetic corpora for NLP (document classification, NER on
process parameters/CQAs, table extraction, QA over GMP-style text).

## A-Mab Process Characterization

A **document corpus** for the *A-Mab* drug substance — a humanized IgG1 monoclonal
antibody — comprising a set of cross-referenced Quarto documents (a transfer plan, a
pre-characterization risk assessment, a characterization master plan, a plan/report
pair per unit operation, and a master report) each paired with a machine-readable
**ground-truth JSON annex**. Every figure, table and number is generated from a seeded
Python model of the entire drug-substance train, so the whole set can be re-created —
consistently — with a single command. The corpus doubles as standalone CMC
deliverables and as a labelled test corpus for the NLP pipeline in the sibling
`nlp_reports` project. See [`pc_package/README.md`](pc_package/README.md).

Grounded in source documents kept outside the repo (at `$SYNTHETIC_DATA_SOURCES`, default
`/home/moritz/Nextcloud/Datasets/synthetic_data/source_documents/`; page-marked extracts in `refs/text/`):

- **A-Mab Case Study v2.1** (CMC Biotech Working Group, 2009) — process model, CQAs,
  risk methodology.
- **FDA — Process Validation: General Principles and Practices (2011)** — the
  process-validation lifecycle (Stage 1 Process Design), report structure and Stage-1
  expectations.
- **ICH Q8, Q9, Q10, Q11** — pharmaceutical development, quality risk management, quality
  system and drug-substance development — the QbD framework, design space, and control
  strategy.

### Deliverables

| Deliverable | Path |
|---|---|
| 20 documents (Quarto → Word + PDF) + their ground-truth annexes | `pc_package/` (see its README) |
| Reference pair: bioreactor Plan / Report | `pc_package/PCP-003_bioreactor.*`, `pc_package/PCR-003_bioreactor.*` |
| Per-document ground truth (JSON) | `pc_package/ground_truth/*.json` |
| Registered inconsistencies, deliberately kept | [`authoring/DISCREPANCIES.md`](authoring/DISCREPANCIES.md) |

The corpus is complete: a transfer plan, a risk assessment, a master plan, a plan and a
report for each of the eight unit operations, and a master report.

**Two documents contain deliberate defects.** They are real inconsistencies a review should
have caught, kept rather than fixed so that a benchmark has something to find, and listed
precisely in `authoring/DISCREPANCIES.md`. Read that file before treating the corpus as
uniformly correct — and do not "fix" an entry without removing it.

### Reproduce everything

```bash
uv sync       # install Python dependencies (one time; or: make env)
make all      # data -> figures -> corpus (documents + ground-truth annexes)
```

Requires **Quarto** (with a LaTeX engine for PDF) and **Python 3.11+**. Individual
stages: `make data`, `make figures`, `make corpus`, `make style`, `make test`, `make clean`.

The Makefile calls `python3`. If your environment is not on `PATH` — the usual case with
`uv` — pass the interpreter in: `make test PY="uv run python"`.

Everything derives from the master seed in `config/parameters.yaml` (`meta.seed`), so
re-running reproduces byte-identical datasets and a consistent document set.

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
        v
pc_package/                <- document-corpus generator (see pc_package/README.md)
  _pcpkg.py + doe_report.py       <- shared helpers + DoE analysis engine
  PCP-00N_*.qmd / PCR-00N_*.qmd   -> Word + PDF (Quarto executes Python)
  build_ground_truth.py           -> ground_truth/*.json (validated vs nlp_reports models)
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

### Risk-assessment content (`risk_assessment/build_fmea.py`)

`build_fmea.py` builds an A-Mab-aligned post-characterization FMEA
(**RPN = Severity × Occurrence × Detection**; CPP rule **Severity ≥ 8 or RPN > 72**)
and carries a curated per-parameter failure-mode / effect / control map. It is retained
as the **content source** for the corpus's Pre-Characterization Risk Assessment
(`RA-001`); run `make fmea` to build the workbook. It is not a shipped deliverable (the
workbook is gitignored).

### Source-text extracts

`refs/text/*.txt` and `refs/grounding/*.json` are cached extractions of the source
PDFs used to parameterize the model, re-creatable with
`python scripts/extract_sources.py` (PyMuPDF).

### Where to read next

| You want to | Read |
|---|---|
| Run or re-run the whole build | [`docs/WORKFLOW.md`](docs/WORKFLOW.md) |
| Understand the corpus and its documents | [`pc_package/README.md`](pc_package/README.md) |
| Understand how the annexes attach to the text | [`pc_package/GROUND_TRUTH.md`](pc_package/GROUND_TRUTH.md) |
| Understand the DoE statistics | [`pc_package/DOE_ENGINE.md`](pc_package/DOE_ENGINE.md) |
| Write or regenerate a document | [`authoring/RUNNER.md`](authoring/RUNNER.md) and [`authoring/WRITING_GUIDE.md`](authoring/WRITING_GUIDE.md) |
| Work on this repo as a coding agent | [`CLAUDE.md`](CLAUDE.md) |
