# Registered discrepancies — real inconsistencies, deliberately preserved

Documents in this corpus contain a small number of **genuine inconsistencies** that a
competent review should have caught and did not. They are listed here, precisely, so they
can be scored.

This is not the retired weak-claims feature (`WEAK_CLAIMS.md`). Nothing here was *injected*.
Each entry arose naturally while the corpus was built, was found afterwards, and was then
**kept** rather than quietly fixed, because a corpus in which every document agrees with
every other document is a poor test of anything.

## Why keep them

A real Biologics License Application package is written by many people over months. Protocols
are approved, then the executed analysis drifts from the approved method; a table label
outlives the thing it labelled; a value is corrected in one document and not in its sibling.
Reviewers are supposed to catch this. They sometimes do not.

That is the hard version of document-understanding: not "extract the Cpk from this report",
but **"does what this report did match what its protocol said it would do?"** — which needs
two documents read together, a method statement matched against an implementation, and the
knowledge that a plausible-looking label can be wrong.

## Rules for this file

1. **Every entry is real.** If it is not a defect an auditor would raise, it does not belong.
2. **Every entry is precise enough to score**: which documents, which spans, what the correct
   statement would be.
3. **Do not fix a registered discrepancy without removing its entry**, and do not remove an
   entry without agreement — that silently deletes a benchmark item.
4. Conversely, **an unregistered inconsistency is a bug**, not a feature. Fix it.
5. **Every entry here has a machine-readable half in `authoring/discrepancies.yaml`**, which
   `authoring/build_brief.py` emits as §5c of the affected document's authoring brief. That is
   what makes an entry survive a re-authoring: a registered discrepancy lives in prose, so
   before §5c existed, rewriting a document simply deleted the item while this file went on
   calling it open, and no gate noticed. Adding an entry here without one there, or removing
   one there without removing it here, re-creates that drift.

---

## D-001 · The proven-acceptable-range analysis does not follow its own protocol

**Type:** protocol deviation (executed method departs from the approved method)
**Severity:** would be a finding in a real review
**Status:** open, deliberately preserved
**Detected:** after the corpus was generated, by comparing `doe_report.par_at_design_centre`
against the plans' stated method. Not caught during authoring or during the annex pass.

### What the protocols commit to

Each affected plan states that the first PAR analysis holds the **other factors at their
set-points**:

> "The first holds the other parameters at their set-points and scans the parameter of
> interest across its characterization range."
> — PCP-006 (low-pH viral inactivation)

> "The first holds the other parameters at their set-points and evaluates the fitted
> response-surface model across the parameter's characterization range."
> — PCP-008 (anion exchange)

> "The first holds the other parameter at its set-point and scans the parameter of interest
> across its characterization range on a grid of 81 points, using the fitted response-surface
> model."
> — PCP-009 (small-virus retentive filtration)

PCP-003 makes the same commitment ("The first holds the other factors at their set-points…").
The authoring guideline in `section_plan.yaml` says the same thing: *"(1) at set-point (other
factors held at their set-points)"*.

### What the reports actually did

`doe_report.par_at_design_centre` holds the other factors at **coded 0**, which is the
midpoint of each factor's characterization range. The reports then present the result in a
column headed **"PAR (set-point)"**.

The midpoint equals the set-point for most factors, so the error is invisible in most of the
corpus. It bites for six response-surface factors across three steps:

| Step | Factor | Set-point (per protocol) | Design centre (actually used) |
|---|---|---|---|
| viral_inactivation | pH | 3.5 | 3.6 |
| viral_inactivation | hold time | 90 min | 120 min |
| viral_inactivation | temperature | 21 °C | 20 °C |
| aex | protein load | 200 g/L resin | 175 g/L resin |
| virus_filtration | filtration volume | 90 L/m² | 95 L/m² |
| virus_filtration | pressure | 13 psi | 19 psi |

So every "PAR (set-point)" value in **PCR-006, PCR-008 and PCR-009** was computed with the
other factors somewhere the process never runs. The pH case is the sharpest: the protocol for
the only true CPP in the process specifies 3.5, and the analysis used 3.6.

### What makes it a good test

- It is **cross-document**: the plan states the method, the report presents the result. Neither
  document is internally inconsistent, so reading either alone reveals nothing.
- It is **partially masked**: the same helper is used at all six DoE steps, and at three of
  them midpoint and set-point coincide, so a spot check on the wrong step finds nothing wrong.
- The label is **plausible**. "PAR (set-point)" is exactly what a reader expects to see, and
  the number beneath it is a real number from a real model.
- Several authoring agents noticed the coded-0 convention and wrote a careful sentence about
  it in their own document — but none of them checked it against the *plan*, which is the
  step that would have turned an observation into a finding.

### The correct position

Either the analysis should hold the other factors at their set-points, matching the protocol,
or the protocols and the column heading should say "design centre". A real deviation report
would state which, justify the choice, and assess the impact on the reported ranges.

### The same mistake shows up in three places

| Surface | What it says | What it does |
|---|---|---|
| `par_table`'s column heading | "PAR (set-point)" | other factors at the design centre |
| the plans' method statements | "holds the other parameters at their set-points" | — |
| the response-surface contour figure title | "remaining factors held at set-point" | `_predict_grid` holds them at coded 0 |

All three come from one decision — coded 0 was treated as the set-point — so a reviewer who
finds one has a thread to pull. The figure is the easiest to overlook, because its title is
drawn into the image rather than written in the prose.

### Do not fix silently

`doe_report.par_at_design_centre` is named for what it computes and `_predict_grid` says in
its docstring that it uses the design centre, so the **code** is honest. `par_table`'s column
heading, the contour figure's title and the plans' method statements are all deliberately
left as written, so the **documents** carry the discrepancy. Changing any of them erases part
of D-001. The `ProvenAcceptableRange.par_at_setpoint` annex field keeps its name for the same
reason: it mirrors what the document claims.

---

## D-002 · PCR-003 claims the bioreactor is the only step that forms a quality attribute

**Type:** unsupported absolute claim, contradicted by the corpus's own register
**Severity:** would be a finding in a real review
**Status:** open, deliberately preserved
**Detected:** after the corpus was generated, while re-grounding the PCR-003 annex. Not
caught during authoring, during the annex pass, or by any gate.

### What the report says

PCR-003 §1.1 opens its account of the step's role with an absolute:

> "This is the only step of the drug substance process at which product quality attributes
> are formed."

### What the data says

`outputs/data/cqa_register.csv` carries a `set_by` column, which is the model's own statement
of which step establishes each critical quality attribute:

| `set_by` | attributes |
|---|---|
| `bioreactor` | afucosylation, galactosylation, high mannose, acidic variants, aggregates |
| `protein_a` | **leached Protein A** |
| `viral_inactivation` | viral clearance — XMuLV |
| `aex` | viral clearance — MVM |

Leached Protein A is the sharp counterexample. It is not merely *reduced* downstream, it is
**formed** at the capture step — it leaches off the resin — and PCR-005 characterizes the
parameters that govern how much of it appears. The two viral-clearance attributes are weaker
counterexamples, since clearance is achieved rather than formed.

### The defence, and why it still fails

The register categorises leached Protein A as a *process impurity*, so a reader could argue
"product quality attribute" was meant to exclude it. The sentence does not say that. It says
"product quality attributes" without qualification, in a document whose own §2 lists leached
Protein A among the attributes the process must control, and the register assigns it an
acceptance criterion like any other CQA.

### What makes it a good test

- It is **document ↔ data**, not document ↔ document. Catching it means reading PCR-003
  against the register or against PCR-005 — neither the bioreactor plan nor the bioreactor
  report is internally inconsistent, so reading either alone reveals nothing.
- **The next sentence is true**, and narrower: "The glycosylation and charge variant
  distributions are established inside the cell and in the culture fluid, and neither is
  modified by the platform purification train." A reader who checks only the elaboration finds
  a supported statement and moves on. The overreach is in the sentence above it.
- **The annex repeats the claim.** `ProcessStep.description` for `step:production_bioreactor`
  says the same thing in `PCR-003.json` and `PCP-003.json`. So this is the one item in the
  corpus where the *ground truth itself* asserts something false, which makes it a test of
  whether a system can find an error in its own supervision rather than only in the prose.
- It shows a **real gap in the gates**: `check_grounding` only inspects
  `SourceReference.quote`. A free-prose `description` field is never checked against anything,
  so an annex can state whatever it likes there and every gate stays green.

### The correct position

The claim should be narrowed to what the data supports — the step at which A-Mab acquires its
glycan, charge-variant and aggregate quality attributes — with leached Protein A attributed to
the capture step (PCR-005). A real review would raise the absolute and ask for the
qualification.

### Do not fix silently

Both the PCR-003 prose and the two `ProcessStep.description` fields are deliberately left as
written. Correcting either erases D-002. Note that the branch `feature/weak-claims-via-brief`
carries a narrowed annex description; if that branch is ever rebased onto a `main` that still
registers D-002, keep `main`'s wording.
