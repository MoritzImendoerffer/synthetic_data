# Two seeded-data tensions: register them, or resolve them

**Status:** proposed 2026-08-16. Not started. No work unit. **The decision is the project
owner's**, because both options are defensible and one of them moves a headline number.

## The problem

`authoring/HANDOFF.md` §3a lists three "seeded-data defects found but NOT changed", each a tracked
decision rather than an oversight. Checked against `config/parameters.yaml` and `amab_process/` on
2026-08-16: **one of the three is already resolved, and two are live.**

### 1. The acidic-variants range is printed two-sided and assessed one-sided — live

`config/parameters.yaml:91` gives `acceptance: [18.0, 40.0]` for acidic charge variants, and the
documents print that range. Capability is computed against the ceiling alone:
`amab_process/studies.py` puts `acidic_variants` in `UPPER_ONLY`, so `Cpk = Cpu = (40 − µ) / 3σ`
and the 18% floor is never enforced.

The code says why, and the reasoning is sound: a very-low-criticality attribute whose risk is
elevated levels should not be penalised for sitting far from a range-of-experience floor. The
tension is not the model, it is that a reader sees `18–40` beside a capability index that only
knows about `40`.

**Making it two-sided moves the headline minimum Cpk from 1.51 to 1.03.** That is not a rounding
change; it is the number a reader takes away from the campaign.

### 2. Three calibration due dates pre-date the effective date — live

`config/parameters.yaml:549–551`:

| Equipment | `cal_due` | `calibration_status` |
|---|---|---|
| EQ-CHR-118, chromatography chamber | 2026-05-30 | `in_calibration_at_execution` |
| EQ-BRX-205, bioreactor pCO₂ probe | 2026-06-14 | `in_calibration_at_execution` |
| EQ-TFF-142, UF/DF skid | 2026-04-22 | `in_calibration_at_execution` |

`EFFECTIVE_DATE` is `2026-07-24` (`pc_package/_pcpkg.py:43`). So every document is effective after
all three calibrations expired, while its own equipment table asserts the equipment was in
calibration when the study ran. Both statements can be true — the studies ran before the documents
were issued — but nothing in the corpus states the execution dates that would make it so.

### 3. DEV-005-01 — already resolved, and HANDOFF has not caught up

The listed defect is that DEV-005-01 reports a buffer prepared *below* target at pH 3.38 while
being tied to an RSM run whose design target is 3.20. `LOT-BUF-5290` is now bound to **RSM run
23**, with a comment at `config/parameters.yaml:559` recording exactly why: run 9 sits on the
pH-3.20 face, where 3.38 would be *above* target and the deviation summary would contradict the
design matrix. Nothing to do here except delete the line from HANDOFF §3a.

## The idea

For each of the two live items, choose one of three, and record the choice where it will be found:

| Option | Where it is recorded | What it costs |
|---|---|---|
| **Register it** as a deliberate benchmark item | `authoring/DISCREPANCIES.md`, with its exact span | nothing to rebuild; a reviewer is expected to find it |
| **Resolve it** in the model | `config/parameters.yaml`, then a full rebuild | item 1 moves the headline Cpk; item 2 is cheap |
| **Explain it** in the corpus | the affected documents, re-authored in one pass | a real authoring cost, and only worth it if the explanation is itself interesting |

**An unregistered inconsistency is a bug.** That rule is in `CLAUDE.md`, and it is why leaving
these two in a §3a list titled "found but NOT changed" is the one option that is not available:
that list is a note to the build team, not a benchmark item, and a reviewer scoring the corpus has
no way to reach it.

## Verification

- Whichever option is taken for item 1, the run publishes the min Cpk with its CQA and its
  denominator, before and after. A number that moves 1.51 → 1.03 must never appear without both.
- If either is resolved in the config:
  `make clean && PATH="$PWD/.venv/bin:$PATH" make data figures corpus PY="uv run python"`, then
  `20/20 annexes valid` and the grounded quote count re-reported. A CQA acceptance change reaches
  every capability table, every design space and the master report.
- If either is registered: an entry in `authoring/DISCREPANCIES.md` naming the document, the
  section and the sentence, in the shape D-001 and D-002 already use.

## What this deliberately does not do

It does not pick. Item 1 in particular is a modelling judgement about a very-low-criticality
attribute, and the code comment that made the current choice is a better argument than anything
this file could add.

## Open question

Are these two the whole list? §3a is the record of every perturbation applied during the build, and
one of its three seeded-data entries turned out to be already fixed. The same check run over the
rest of §3a would be worth its hour.
