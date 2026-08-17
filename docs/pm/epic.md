---
type: pm-epic
sprint: 2026-08-16_01_register-from-four-sources
status: active
started: 2026-08-16
proposal: docs/next/register-from-four-sources.md
tags: [pm/epic]
---

# Epic — make the corpus argue, then test it on one document

Board: [[_Board]] · proposal:
[`docs/next/register-from-four-sources.md`](../next/register-from-four-sources.md) · exploration:
`.claude/work/2026-08-16_01_register-from-four-sources/exploration.md` · plan:
`.claude/work/2026-08-16_01_register-from-four-sources/implementation-plan.md` · method:
`.claude/work/2026-08-16_01_register-from-four-sources/register_analysis.ipynb`

**The finding.** The project owner rejected the corpus prose: no subject matter expert would write
it. Every document passes all thirteen register thresholds, so the gate was measuring the wrong
thing. A dependency-parse comparison against the human sources found the defect and, more usefully,
found what it is not. Across roughly 30,000 words of four documents there is **not one "However"
and not one "For example"**, against 46 and 12 in A-Mab and 21 and 22 in PDA TR 60; the whole
connective repertoire has collapsed onto `therefore`, which the gate happens to cap. Only 31 to
35 % of sentences continue the previous sentence's topic, against 57 to 60 % in the sources. A
third of PCR-003's sentences have `be` for a main verb and carry their meaning in abstract nouns on
stacked prepositions. `its` runs at 24 times the A-Mab rate.

**The cause is in the repository, not in the authors.** `WRITING_GUIDE.md` §2c and §2d say "one
paragraph, one point" and "if a sentence carries two claims, make it two sentences". Every move
that carries an argument needs two ideas held together, so all of them are forbidden. The authors
complied exactly.

**What the epic will not do, and why that matters.** Eight competing hypotheses were tested and
returned null: sentence length, structural complexity, word order, nominalisation, formulaic
repetition, over-claiming, coordination and number density. The corpus is *simpler* than its
sources on every structural measure and inverts word order essentially never. So no threshold of
the kind `check_style.py` already carries can reach this, and six plausible rules were discarded
rather than written into the guide.

**The scope.** Ten tasks. Four artifacts change — the writing guide, the register exemplar, the
source extraction and the brief — and **one document is re-authored**, `PCP-003`, the worst
modality case at `will` 19.7 per 1000 words with `should` and `may` at zero. The remaining
nineteen are deliberately not planned; the corpus is 119,453 words of prose and committing to that
campaign before anything shows the fix works is the expensive mistake.

**Decisions taken by the project owner, 2026-08-16.** ISPE passages may be quoted into the
exemplar, which unblocks the plan-genre material for the ten plan documents and puts the ISPE
extracts into `refs/text/` as committed text. The brief gains a discrepancies section, so a
re-authored document keeps D-001 and D-002 rather than silently dropping one. The plan reaches
through the pilot and no further.

**The gate.** `20/20 annexes valid` and every quote grounded with `GROUNDING_STRICT_ANCHORS=1`,
against a starting 2,084; 85 tests; `make style` over all 20 documents; `git diff outputs/` empty,
because no number moves. **The acceptance test for the pilot is discrimination, not counts**: can a
reader tell a corpus passage from a source passage. Every measurement in this epic is a diagnosis
and none of them is given to an author, because this repository has already watched a metric move
while the prose got worse.
