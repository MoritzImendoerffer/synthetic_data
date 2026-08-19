# authoring/mechanism — the physical chemistry of each step, for the brief's §2b

One YAML file per unit-operation key. Each carries, for every quality attribute the step sets or
clears and every parameter it studies, two to four sentences of physical chemistry in the terms
of art of the field: which species, which interaction, which property of the resin, the buffer or
the culture, and in which direction it acts.

**Why it exists.** Until 2026-08-19 nothing supplied the mechanism the reports were asked to
explain. The section plan demanded a mechanistic interpretation, the exemplar taught how to
report and never how to say why, and the brief carried no domain prose. An author told to explain
a mechanism and given none wrote sentences shaped like explanations ("acts through the capacity
of the bed", "follows from the physical chemistry of affinity capture"). These files are the
supply. `build_brief.py` emits the step's file as brief §2b for every per-unit-operation plan and
report.

**What it must never carry: a number.** No set-point, no range, no effect size, no p-value, no
fold. A file with a number goes stale on the next reseed and breaks golden rule 1. Directions
are stated only where the physical chemistry is unambiguous; where the sign of an effect is
empirical, the file names the pathway and leaves the sign to the data. `tests/test_mechanism.py`
asserts that no prose value contains a digit.

**Where it comes from.** Domain knowledge, not `refs/text/`: the published sources describe what
each step does and expect, and do not explain the mass transfer or the chemistry. This is the one
place in the repository where prose is authored without a source to ground it against, which is
why the project owner reads every file once and the `reviewed_by_owner` field says when.
