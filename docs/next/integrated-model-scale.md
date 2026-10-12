# The integrated model: what it simulates, and at which scale

**Status:** proposed 2026-10-12, after the owner asked about a sentence in PCR-003. Not started. No
work unit. Part A fixes a defect in the generator. Part B is a gap in the story, and **the decision
on it is the owner's.** Both are cheapest before PCMR-001 is authored for Version 2.0, because
PCMR-001 rolls up every capability number the simulation gives.

## The problem

PCR-003 says twice that the integrated model "simulates manufacturing scale directly": once in the
Executive summary (`pc_package/PCR-003_bioreactor.qmd:1232`) and once in §Process capability
(`:1973`). The second time it adds: "It does not use the response-surface models of this report,
and it applies no scale-down offset". The owner asked what a reviewer would ask. Scale is not a
factor in any design, so how can a model simulate manufacturing scale without the DoEs? There are
two answers. One is a defect in the generator, and the other is a gap in the story.

### A. For three outputs the simulation runs at scale-down (a defect)

The generator has one process model, `amab_process/unit_ops/*`, chained by `Process.run_batch`
(`amab_process/process.py`). Every dataset is drawn from it:

| Dataset | Code | Scale effect applied |
|---|---|---|
| DoE runs (screening, RSM, augmentation) | `studies._run_design` | none (this is scale-down by definition) |
| SDM qualification, scale-down rows | `analytics.sdm_qualification` | none |
| SDM qualification, manufacturing rows | `analytics.sdm_qualification` | `analytics.sdm.scale_offset` |
| Integrated model (`monte_carlo.csv`, `capability.csv`, `p_oos.csv`) | `studies.monte_carlo` | **none** |
| PPQ batches (`ppq_batches.csv`) | `studies.ppq_batches` | **none** |

`scale_offset` (`config/parameters.yaml:1689`) holds the only scale effects the generator has.
Leached Protein A is ×1.15 at manufacturing scale. UF/DF aggregate is ×0.95 and UF/DF step yield
is ×1.01. The code reads these values in exactly one place, `amab_process/analytics.py:334`. The
manufacturing-scale batches of the qualification carry the effects, and the manufacturing-scale
batches of the simulation and of PPQ do not. For these three outputs the "manufacturing-scale"
simulation therefore behaves like the scale-down model:

- **Drug substance aggregate** is simulated too high. UF/DF is the last step, so its aggregate is
  the drug substance value. This error is in the conservative direction.
- **Drug substance leached Protein A** is simulated too low. This error is not conservative. PCR-005
  already calls that Cpk not meaningful, because the simulated values sit below the ELISA's limit of
  quantitation.
- **Overall yield** is simulated slightly low.

The reports apply the offset whenever they convert their own scale-down data. PCR-010 subtracts the
aggregate offset before its verification fit (`PCR-010_ufdf.qmd:924`), and PD-005-08 records that
leached Protein A is judged through its offset. So a report puts its own data on manufacturing
scale, then sets them beside a simulation that never had the effect.

**How much this moves the printed numbers has not been measured.** Measuring it is the first task
(see Verification).

### B. No document says what the integrated model is (a gap)

PCMP-001 §6.5 (`PCMP-001_master_plan.qmd:909–915`) says "Capability at commercial scale is
estimated from an integrated model of the train". It then describes how the model samples the
parameters. It never says what the model is built from, or how anyone showed that it represents
manufacturing scale. The reports only say what it is not. PCR-003 says it "does not use the
response-surface models", and PCR-004 says "no Monte Carlo propagation of a fitted model is made"
(`PCR-004_harvest.qmd:890`).

Within the story, the campaign knows its scale-down DoEs, its qualification runs and its platform
history. A model of manufacturing-scale batches that contains no fitted model has no source that
anyone in the story could have built it from. The ISPE guide on process validation says simulation
"is most useful for studying future events that can be predicted from historical data or knowledge"
(`refs/text/ispe_pv.txt:1212`, p. 25). The documents name neither the data nor the knowledge.

The bioreactor makes the gap sharper. PD-003-13 (`config/parameters.yaml:1030`) records that
aggregate differed between the scales in the bioreactor qualification, and that aggregate is judged
through an offset. The generator has no bioreactor scale effect, so that difference is run-to-run
variation, which is something real data does. But PCR-003 then argues that the integrated model
needs no offset because it simulates manufacturing scale directly. That is set against the
document's own finding that the two scales differ.

## What is not the problem

All checked on 2026-10-12:

- **For the bioreactor's own attributes the sentence is true as the generator stands.**
  `scale_offset` has keys for `protein_a` and `ufdf` only, so the simulated bioreactor and the
  manufacturing-scale bioreactor qualification come from the same model.
- **The parameter sampling matches PCMP-001 §6.5.** Each parameter is drawn from N(set-point,
  NOR width / 6) and clipped (`studies._sample_overrides`).
- **The cross-references point to the right section.** PCP-003, PCP-008, PCR-004, PCR-007 and
  PCR-009 cite PCMP-001 §6.5, and the rendered PCMP-001 numbers its capability section 6.5.
- **This is not a registered discrepancy.** `authoring/DISCREPANCIES.md` mentions neither the
  simulation nor an offset. Under `CLAUDE.md` it is therefore a bug, or it must be registered.

## The idea

**Part A.** Move the scale effects out of the analytics layer and into the process model, so that
"manufacturing scale" means the same thing in every dataset. `Process.run_batch` takes a scale. At
manufacturing scale it multiplies each step's output by the effect recorded for that step. The
qualification, the simulation and PPQ all call it at manufacturing scale. A multiplication draws no
random number, so every column that does not depend on the three outputs should stay
byte-identical.

**Part B.** There are three options, and the owner chooses:

| Option | What it means | What it costs |
|---|---|---|
| **Name the model** in PCMP-001 §6.5 | state what the integrated model is built from, and which scale effects it carries | one section of PCMP-001 re-authored, and every report sentence on the model re-read. The source has to exist in the config and the story bible first, or the document invents it (golden rule 3) |
| **Build it from what the campaign has** | chain each step's selected model at manufacturing scale (prediction plus offset plus residual variance) | every capability number changes. Harvest and UF/DF have no response-surface model, and no step model carries the link from one step's output to the next step's load |
| **Register it** | an entry in `authoring/DISCREPANCIES.md` for the PCR-003 sentences: a reviewer should ask what the model is | nothing to rebuild. It is only honest once Part A is done, or the registered item is partly a generator bug |

## What it would take

Part A, about 50–80 lines across the config, model and data layers. Documents re-render and
annexes are rebuilt.

- `config/parameters.yaml`: move `analytics.sdm.scale_offset` to a key of the process model, and
  keep its comments.
- `amab_process/process.py` (and possibly `unit_ops/base.py`): apply the effect of a step at
  manufacturing scale.
- `amab_process/analytics.py`: the qualification calls the process at manufacturing scale instead
  of multiplying the value itself.
- `amab_process/studies.py`: `monte_carlo` and `ppq_batches` run at manufacturing scale. No
  document reads the content of `ppq_batches.csv`. PCMP-001, PTP-001, PCR-004 and PCR-009 read
  only the batch count from the config, so the PPQ change moves no rendered number.
- **Version 1.0's simulation keeps its current behaviour.** `scripts/generate_data.py:136–145`
  reruns the same Monte Carlo at the characterized NOR to produce `capability_rev1.csv`, which
  "fixes the Version 1.0 capability-based limits and INV-001's capability findings". Version 1.0 is
  frozen, so the fix must not move that file.
- A test in `tests/` that the effect reaches the simulation, and that the qualification is unchanged.

Every document whose numbers move is re-rendered, and the prose around each moved number is
re-read. Where a claim no longer holds, that document is re-authored in one pass. It is never
patched, because nothing is added to a document after authoring.

Part B depends on the option chosen.

## Verification

- A committed script prints, before and after the fix, the mean, standard deviation, Cpk and count
  outside the criterion for drug substance aggregate and leached Protein A, and the mean overall
  yield, with the denominator (`n_monte_carlo`). The same is printed for the PPQ batches. The
  result goes to `docs/results/`.
- These files are byte-identical before and after: `sdm_qualification.csv`, `capability_rev1.csv`,
  and every column of `monte_carlo.csv` and `ppq_batches.csv` outside the three outputs and what
  they feed.
- `make clean && PATH="$PWD/.venv/bin:$PATH" make data figures corpus PY="uv run python"`. Then
  report the valid annexes as N/N, the grounded quotes with their total, and zero weak anchors under
  `GROUNDING_STRICT_ANCHORS=1`. `make test` passes, including the new test.
- `grep -n "manufacturing scale directly\|no scale-down offset" pc_package/*.qmd`: each hit is
  re-read against the fixed generator.

## What this deliberately does not do

- **It does not make scale a DoE factor.** Characterization runs at one scale, and the
  qualification and its offset bridge the scales. That is how the corpus already argues, and it is
  right.
- **It does not change how the reports estimate or apply an offset** (`doe_report.sdm_offset`,
  `doe_report.to_mfg`). That is the analyst's side, and it is a correct method for an analyst.
- **It does not add a bioreactor scale effect** to make PD-003-13 true. A chance difference
  between the scales is something real data does.
- **It does not choose for Part B.**

## Open questions

1. Which option for Part B?
2. Timing. Should this land before PCMR-001 is authored, so that its roll-up is written once? Or
   after Version 2.0 closes, with the affected documents re-authored? The first is cheaper.
