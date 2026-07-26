# Design rationale

Decisions behind `ema_docgen`, including the ones that changed during design.
Recorded so the reasoning survives, and so you can overrule it knowingly.

---

## D1 — The corpus is a versioned release, not a build artifact

**Decision.** Generated prose is committed and frozen. Regeneration is explicit
and produces corpus v2, v3.

**Why.** `build_ground_truth.py` grounds every `SourceReference.quote` as a
verbatim fragment of the rendered document. If prose regenerated on every build,
the annexes would have to regenerate with it — making the *gold standard*
non-deterministic. Benchmark scores would then not be comparable across corpus
builds, by you or anyone else. That is disqualifying.

**Consequence.** Each release needs a manifest: model IDs used, docspec version,
content hash, date. Put it in the tag annotation or a `CORPUS.md`.

---

## D2 — Second pass beats generate-deep-from-the-start

**Decision.** Complete scope in a second pass over existing minimal documents.

**Why (the non-obvious reason).** Strict additive-only means every original
sentence survives untouched, so **the same ground-truth annex validates against
both the minimal and the completed document**. You get a matched pair for free:
identical facts, identical gold answers, materially different length and
distractor density.

That is a controlled ablation isolating the effect of document length on
retrieval and long-document QA while holding ground truth exactly constant. It
turns a corpus into a benchmark contribution. Generating deep documents from
the start throws it away.

**Open option.** Three tiers (`minimal` / `standard` / `full`) rather than two
gives a length-scaling curve, at roughly double the generation and validation
work. Not implemented; the docspec `tier` field would carry it.

---

## D3 — Obligations, not word counts

**Decision.** Sections are specified by required rhetorical moves. Word targets
exist only as a lint tolerance band, never as an instruction to the agent.

**Why.** "Expand to 3,000 words" produces padding — the model inflates clauses
to hit the number. Length in real regulatory documents is emergent from
obligations: defensive anticipation, provenance of every value, documented
negative space, traceability clauses, bounded conclusions, table narration.
Specify those and the words follow. Obligations are also checkable; word counts
tell you nothing about whether a section is doing its job.

---

## D4 — The agent never edits `.qmd`

**Decision.** Agent emits `build/insertions/<DOC>/<SECTION>.yaml`.
`scripts/splice.py` applies it after verifying anchor uniqueness.

**Why.** Claude Code subagents run in acceptEdits mode with auto-approved file
edits. A prompt-level "do not rewrite" will not survive an agent that judges a
sentence improvable. Anchor-verified splicing makes rewriting impossible rather
than detectable-after-the-fact.

**Detail that matters.** The `.qmd` files are hard-wrapped at ~85 characters, so
a verbatim sentence anchor spans multiple lines. `splice.py` matches on
whitespace-normalised text and maps back to original offsets. Anchors inside
fenced code blocks are rejected.

---

## D5 — Fresh context per section, ledger as the bridge

**Decision.** Each section runs in a fresh subagent. A running ledger
(`build/ledger/<DOC>.md`, 2–3 lines per completed section) is the only carried
state.

**Why.** A single agent carrying a whole document's sections in one context
produces the same prose in all of them — the uniformity problem, which is the giveaway of a
synthetic corpus and makes the benchmark systematically unrepresentative. Fresh
context prevents convergence.

**Cost.** Fresh context cannot satisfy the restatement obligation, which needs
to know what the rest of the document says. The ledger bridges it. **Ledger
quality determines whether restatement is real or fabricated** — a vague ledger
produces invented restatements of claims that do not exist, and the grounding
test will not catch that.

---

## D6 — Length variance is spec-assigned, never agent-decided

**Decision.** `target_words` per section spans roughly 150–3,000 and is set by
you. `register` is likewise assigned.

**Why.** Real documents are wildly uneven — some sections are three perfunctory
sentences, others are eight pages of defensive justification because a reviewer
once asked. Uniform section length is unrealistic and reduces benchmark value.
The agent will not produce this variance on its own; it is the one decision it
gets uniformly wrong.

---

## D7 — `forbidden_moves` alongside `required_moves`

**Decision.** The docspec carries both.

**Why.** Without exclusions every section drifts toward the same defensive
register. A results subsection that opens with a transferability denial reads
wrong, and the agent cannot know that unless told.

---

## R1 — REVERSED: A-Mab passages as register exemplars

**Originally proposed.** Point the agent at line ranges in
`refs/text/amab.txt` as style anchors.

**Reversed, for two reasons.**

*IP.* A-Mab is a 2009 CMC Biotech Working Group publication. `synthetic_data` is
public. Passages pasted into prompts get echoed into generated prose, putting
copyrighted text in the repo unnoticed.

*Contamination — the serious one.* A-Mab is near-certainly in the training data
of every model you will evaluate. If your corpus carries its lexical surface,
retrieval and QA scores are inflated by memorisation. You would be building a
contaminated benchmark, and it would be very hard to detect afterwards.

**Replacement.** `AUTHORING.md` defines moves abstractly, with exemplars written
fresh in the corpus's own voice. `lint_overlap.py` checks n-gram distance from
`amab.txt` as a corpus property. The docspec has no `register_anchor` field.

---

## R2 — CORRECTED: the premise that A-Mab is more verbose

Measured, not assumed:

| | words | words/page |
|---|---|---|
| A-Mab §4.6.1 Protein A (pp. 118–127) | 3,802 incl. tables | 380 |
| PCR-005 Protein A | 4,004 prose only | 208 |
| A-Mab §3.4.3 bioreactor (pp. 68–84) | 7,673 | 451 |
| PCR-003 bioreactor | 4,091 | — |

At the unit-operation level the existing documents are already at or beyond the
source case study. A-Mab's ~99,000 words come from **scope** — 278 pages, twelve
chapters, the whole lifecycle — not from denser treatment of any one topic.

A second point: A-Mab §4.6.1 is a *summary of* process characterization, not a
process characterization report. It compresses what would be a standalone
60-page PCR into ten pages. It is structurally the wrong anchor for report
length and would teach the opposite of the intent.

**Honest gap.** Nothing in `refs/` is an actual PCR. A-Mab is a case study;
PDA TR 60 and the ISPE GPG are guidance. There is no register anchor for the
document class being generated. The move taxonomy is a reconstruction, not a
transcription — treat it as a hypothesis to refine against real documents if you
ever get access to one.

**Consequence.** The task was reframed from *expansion* to **scope completion**.
"Add a Resin Reuse and Lifetime Study section" has a clear success criterion;
"make §Results 3× longer" does not.

---

## R3 — CORRECTED: "data not shown"

A-Mab repeatedly asserts a result and defers with *data not shown*. Correct for
a case study; destructive here, because it removes the retrieval hook. Every
deferral in generated prose must instead name a location — an appendix, a paired
report, an SOP. Encoded in `AUTHORING.md` under the deferral rule.

---

## R4 — UPDATED: scope completion is done; the task is now density

The corpus grew from 10 documents to 20 after this harness was first drafted.
`PTP-001`, `RA-001`, `PCMP-001`, `PCMR-001` and the three remaining unit
operations (AEX, virus filtration, UF/DF) all exist. Corpus prose is now 58,868
words across 20 documents.

**This changes what the second pass is for.** Measured against `PCR-008_aex.qmd`,
the newest and densest report:

- The section taxonomy is **already identical** across reports. There are no
  missing section types to add.
- PCR-008 carries 6,914 prose words; PCR-007 carries 4,453 under the *same*
  headings.
- Of that 2,461 gap, roughly 1,018 is uniform per-section density (+40 to +90
  words per section) and the remainder is two narrated deviation subsections
  (370 and 782 words) that PCR-007 does not have.

So the task is no longer "add sections." It is: **seed deviations per unit
operation, narrate them, and bring the older reports to PCR-008's density.**
`docspec/PCR-007.yaml` is derived from this measured delta rather than
invented.

**PCR-008 also supersedes the invented exemplars.** It is written in the
corpus's own voice, demonstrates the target register precisely, and carries no
contamination risk. AUTHORING.md Part 4 now points at it section by section.

One further consequence: PCR-008 already contains DEV-01 and DEV-02 with a
sample-size justification for verification runs. The fact-pack infrastructure
the design assumed was missing is partly built — what is missing is its
extension to the other five unit operations.

---

## The binding constraint

You cannot write more words about the same facts without padding. The generator
currently simulates a clean campaign: designed runs, clean responses, no
incidents. Real reports are long partly because real campaigns are messy.

Before prose generation is worth scaling, `amab_process/` needs to emit:

- deviations and excursions
- runs excluded from models, with the statistical basis
- assay repeats, OOT results, invalid analyses
- scale-down qualification attributes that *failed* equivalence
- equipment, resin lot, buffer lot, calibration identifiers
- prior-document references with dates and decisions

Each is a seeded fact worth 200–600 words of legitimate prose and — more
valuable — a multi-hop QA item. `<<NEEDS:>>` volume on the pilot will tell you
how far short the fact pack currently falls.

---

## Not designed, deliberately

- Parallel dispatch within a tier (RUNNER.md describes it; no scheduler here)
- The three-tier length ladder (D2)
- Second exemplars per move in `AUTHORING.md`
- Cost instrumentation beyond per-call model logging
