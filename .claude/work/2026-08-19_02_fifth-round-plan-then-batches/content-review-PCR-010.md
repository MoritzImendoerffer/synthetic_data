# Content review of the PCR-010 draft — before promotion

**2026-08-19, TASK-010 §4.** Judge: fresh-context agent (`opus`, self-reported Claude Opus 5), the four
questions and `pc_package/PCR-010_ufdf.DRAFT.pdf` (30 pages), nothing else.

## Run 1 — as authored (`PCR-010.DRAFT.pre-review.qmd`)

**Q1 No · Q2 Yes · Q3 No · Q4 Yes.**

Q1 (≈30 uses of the listed verbs): 16 over an abstraction or a documentary reason (a CQA, a
guideline, a risk score, a specification, an assay limit, the report's own argument — e.g. "The step
sets no critical quality attribute", "because none of them acts on an attribute the step forms or
clears", "This step governs no critical quality attribute … so the region that governs its
operation is a set of univariate ranges"); 7 naming a physical object with no direction, three
deferring it to the next sentence ("The diavolume count acts on the buffer exchange and on nothing
else."; "Transmembrane pressure acts on the permeate flux and, through the polarisation layer, on
the concentration and the shear at the membrane wall."; "The final drug substance concentration
acts on the viscosity of the retentate and on the concentration in the polarisation layer."; "The
final drug substance concentration sets the viscosity of the retentate …"; "Acidic charge variants
are measured because deamidation depends on pH and on time …"; "It governs the permeate flux and
therefore the duration of the step"; the shear-history mismatch). One full pass: "It is the
parameter most likely to drift during a run, because a fouling membrane raises it at constant flux".

Q2: clean — the vocabulary is membrane filtration's (diavolume, transmembrane pressure, permeate
flux, crossflow, polarisation layer, NMWCO, hold-up volume, buffer chase); soft: "pump passage
count", "quality-linked parameters".

Q3 (9): "Prior knowledge also sets what each parameter is expected to do."; "Two bounds apply to
that calculation."; "The relation is used here to show why the step is not sensitive to the
diavolume count within the range studied."; "One bound applies to both attributes."; "What the
comparison supports is the weaker and sufficient statement."; "The measurement was made for that
reason, and …"; "The observations that support the classification of §9 are as follows."; "The
impact on the study rests on two facts."; an elided-predicate sentence in §13.1. The "N bounds
apply" scaffold recurs in §7, §8, §10, §11.

Q4 (19): the dominant form "X rather than Y" in the same sentence as the finding — "Both are
measures of process performance rather than quality attributes."; "…and the loss is a yield outcome
rather than a quality outcome."; "…which is a formulation failure rather than a quality failure.";
"…the measurement is confirmatory rather than limiting."; "…is treated as a bound rather than as a
prediction" — plus "which is expected, because …", "which is the behaviour expected once …", "which
is why it is monitored in process", "which is what the deviation of §13.1 shows", "which is the
mechanism by which this step could raise aggregate (§2.2)", "The consequence is stated plainly in
§4.3.", "Aggregate is therefore the attribute this characterization has to bound, and it is treated
in §2.2 and §5.3.", "What bounds the risk instead is …", "They are also useful evidence in
themselves, because …", "Its wider value is that it shows …".

## The return to the author (once) — run 2 below

## The author's revision (same context, 1 check_render pass, 30 pages, 304 → 289 sentences, 6,116 → 6,005 words)

Every named sentence changed; direction and species moved into the causal clauses (§2.1, §2.2,
§5.3 with two consistency edits in §3.1 and §4.3 it forced, §5.4 ×3, §9); the "N bounds apply"
scaffolds folded into the claims that followed; the filing tails removed or rewritten as claims
with a direction; "pump passage count" → "the number of pump passes", "quality-linked parameters" →
"parameters linked to a quality attribute". The documentary *because/governs* uses left alone.

## Run 2 — on the revised draft (fresh judge, self-reported Claude Opus 5)

**Q1 No · Q2 Yes · Q3 No · Q4 Yes.**

| question | run 1 | run 2 |
|---|---|---|
| Q1 | 16 documentary + 7 physical-no-direction | **5 mechanism-context deferrals** (§2.1 "Because the mechanism is the same for A-Mab…", §3.1 "the quantities that govern the step", §11 the same, §4.3 "act through the same physical route", §2.3 "acts on an attribute the step forms or clears") + 11 registry/documentary uses ("The step sets no critical quality attribute", "For a step that governs a critical quality attribute…", "set by another step"); the four passing *because* clauses name species, property and direction |
| Q2 | clean | **clean** ("no coinages, no pseudo-technical compounds") |
| Q3 | 9 | **7** — two true by definition ("A one factor at a time design cannot determine whether…"), two reporting confidence or an unstated prediction, two unquantified hedges ("applies directly", "does not act strongly"), one trivial restatement |
| Q4 | 19 | **13** — "These are univariate observations."; the "whole-process figures / not a property of this step alone" instruction three times; "and none is claimed here" / "this report makes no claim about it" pre-emptions; "Two things this step does not control should be stated." |

Outside the four questions the judge noted a substantive tension: §1.1 "What the step can do to the
product is mechanical." against §2.2's pH-driven deamidation across the same step. Recorded here
and in the batch page; it is not a Q-fault and the one cycle is spent.

**Disposition:** not promotable on content by the checklist's letter; proceeds to the batch's annex
as the plan says. One cycle removed the first-order faults (the deferred directions, the
coinages, the scaffolds); a second-order residue of registry verbs and disclaimers remains, the
same shape as in `PCR-007`.
