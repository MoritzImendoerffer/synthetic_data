# ema_docgen

> **SUPERSEDED. Do not use this to author or change a document.**
>
> This directory describes the two-pass **additive densification** workflow: write a minimal
> document, then have an agent grow it section by section, splicing insertions and tracking
> them in a ledger. It has been replaced by **one-pass authoring** — one document, one agent,
> one context — because the splice-and-ledger design coupled its components by string
> convention rather than by gates, and because per-section fan-out destroys the
> whole-document arc, the cross-references and the coreference that the corpus depends on.
>
> Start at [`../authoring/RUNNER.md`](../authoring/RUNNER.md) instead.
>
> **What is still live here:** `scripts/lint_numerals.py` and `numerals.allow`, which
> `authoring/check_render.py` runs as an advisory bare-numeral lint, and the `docgen-*`
> targets at the bottom of the root `Makefile`, which only that workflow used. Everything
> else is history — kept because the design rationale in `DESIGN.md` explains decisions the
> current system inherited. The text below describes the retired workflow as it was.

---

## 1. Background — what this corpus is

`synthetic_data` generates a **fictional pharmaceutical process-characterization
document package**. Twenty documents describing the manufacture of "A-Mab", a
monoclonal antibody that does not exist, made by "Novacyte Biologics", a company
that does not exist:

| Prefix | Document class | Count |
|---|---|---|
| `PCP-00n` | Process Characterization Plan, one per unit operation | 8 |
| `PCR-00n` | Process Characterization Report, one per unit operation | 8 |
| `PTP-001` | Process Transfer Plan | 1 |
| `RA-001` | Pre-Characterization Risk Assessment | 1 |
| `PCMP-001` / `PCMR-001` | Master Plan / Master Report | 2 |

The technical content follows the **A-Mab case study** (CMC Biotech Working
Group, 2009), published as a public teaching artifact, and the document
structure follows the FDA 2011 guidance, the ICH Q8–Q11, and ICH Q8/Q9/Q11.

Two properties make it more than a pile of plausible text:

**Every number is generated, not written.** A seeded simulation in
`amab_process/` produces the datasets in `outputs/data/`. The documents are
Quarto (`.qmd`) files that pull those values in through inline expressions like
`` `{python} f"{agg_cpk:.2f}"` ``. Re-run the model and every number in every
document updates consistently. Nobody types a measurement by hand.

**Every document has a machine-checked answer key.** `ground_truth/<ID>.json`
holds annotated question-answer pairs, entity annotations and citations. Each
citation carries a `quote` field containing text copied **verbatim** from the
rendered document. `check_grounding.py` verifies that every one of those quotes
still appears in the rendered `.docx`.

That second property is what makes the corpus a benchmark: you can run a
retrieval or QA system against the documents and score it against the annexes.

---

## 2. The problem

The documents are thinner than the real thing. Real process-characterization
reports run 60 to 150 pages of dense, defensive, repetitive prose. These run
4,000 to 7,000 words.

For a benchmark that matters. A short document fits entirely in a model's
context, so retrieval is never really tested — there is no haystack. Difficulty
in long-document QA comes from distractors, restated claims, and answers that
require connecting two distant sections. You need length, and length of a
particular kind.

The goal is to add that length. The obstacle is that the obvious way of doing it
destroys the corpus.

---

## 3. Why "ask an LLM to expand the document" fails

Three ways, each of which the tooling here is built to prevent.

**It breaks the answer key.** The annexes quote the documents verbatim. An agent
that rewrites a sentence — even improving it — silently invalidates every annex
quote drawn from that sentence. Since agents in editing mode routinely rephrase
as they go, this is not a hypothetical.

**It invents numbers.** Asked to write a paragraph about aggregate clearance,
a model will happily write "reduced to 0.8%" because it reads well. Now the
document contradicts the simulation, and nothing catches it.

**It makes everything sound the same.** Generate thirty sections against one
prompt and you get thirty sections with identical paragraph rhythm and identical
length. Real documents are wildly uneven — a three-sentence section next to eight
pages of justification. Uniformity is the tell of a synthetic corpus, and it
makes the benchmark systematically unrepresentative.

---

## 4. How it works

Start with the mental model; the file-by-file detail lands better once it is in
place.

**Input:** a finished, committed document (`PCR-007_cex.qmd`) and its answer key
(`ground_truth/PCR-007.json`), whose citations quote that document verbatim.

**Output:** the *same* document, longer — new paragraphs interleaved between the
existing ones — with **every original sentence still present, byte for byte**, so
the *same* answer key still validates against it, unchanged.

Two consequences follow, and they are the whole point:

- The added prose is **distractor text**. It introduces no new gold answers; it
  lengthens the haystack the existing answers sit in. That is what turns an easy
  benchmark into a hard one — the questions are identical, the document they must
  be retrieved from is now several times longer.
- Because the answer key is untouched, the short and long versions form a
  **matched pair**: identical ground truth, differing only in length and
  distractor density. Growing the answer key too — promoting a newly seeded
  deviation into its own question — is a **separate, deliberate step**, described
  under "What stays fixed" below.

The mechanism that makes this safe: **the agent never edits a document.** It
proposes additions, and a script applies them after verifying they are safe.

Walk through one section end to end.

**Step 1 — you specify the section.** In `docspec/PCR-007.yaml` you write an
entry saying: this heading, this much longer, in this register, making these
specific rhetorical moves. You decide this, not the agent.

```yaml
  - id: mechanistic_interpretation
    heading: "Mechanistic interpretation"
    tier: 2
    register: analytical
    target_words: 270
    required_moves: [mechanistic_warrant, worst_case_identification]
    forbidden_moves: [table_narration]
```

**Step 2 — you supply the facts.** In `factpack/PCR-007/<section>.yaml` you list
the facts that section may use: deviations, excluded runs, equipment IDs, method
performance. The agent may use nothing else. This is what stops it inventing a
temperature excursion that never happened.

**Step 3 — the agent drafts.** It reads the current document, the docspec entry,
the fact pack, and a running ledger of what other sections already say. It
writes out a file of **anchored insertions**:

```yaml
insertions:
  - anchor: >-
      The step yield declines modestly at high load, where breakthrough costs
      recovery, and is otherwise robust.
    insert_after: |
      New paragraph of prose, which will appear after the paragraph that
      contains the anchor sentence.
```

The `anchor` is an existing sentence copied verbatim. There is no `replace`
operation and no `delete` operation — the schema simply has no slot for them.

**Step 4 — a script applies it.** `splice.py` finds the anchor, checks it occurs
**exactly once**, and inserts the new paragraph after the paragraph containing
it. Existing text is never touched. If the anchor is ambiguous or missing, the
whole section is rejected and nothing is written.

**Step 5 — the gates check it.** Two kinds of check run (§9). The **blocking**
gate (`docgen-verify`) renders the document, rebuilds and validates the annexes,
and runs the grounding check; if any of those fail, the splice is reverted with
`git checkout` and the runner moves on. The **advisory** report
(`docgen-report`) then runs the three lints for information — it never reverts,
because it measures the whole document, not the splice.

### What stays fixed: the answer key

`splice.py` only ever inserts whole paragraphs *between* existing ones, so every
existing byte survives and `check_grounding.py` — which requires every annex
`quote` to appear verbatim in the rendered `.docx` — keeps passing. The invariant
is enforced twice over: structurally (the insertions schema has no `replace` or
`delete` slot) and by the gate (any change that broke a quoted span fails
grounding and is reverted).

One consequence surprises people: **the annexes do not grow with the prose.**
`build_ground_truth.py` builds them from `outputs/data/*.csv` and its own curated
quote set; it knows nothing about the paragraphs the agent added, so that new text
is, by default, pure distractor. When you seed a *new* fact — a deviation, an
excluded run — and want it to become an answerable, multi-hop question, you extend
`build_ground_truth.py` to annotate it, exactly as for any hand-authored annex
entry. This harness grows the **document**; growing the **answer key** is the
step you take next, on purpose.

---

## 5. Vocabulary

Six terms recur throughout the files.

**Docspec** — `docspec/<DOC>.yaml`. The section plan for one document: what to
write, how long, in what register, using which moves. **The artifact you
curate.** Everything the agent does is bounded by it.

**Fact pack** — `factpack/<DOC>/<SECTION>.yaml`. The facts a section is allowed
to use. Also the thing most likely to be your bottleneck (see §9).

**Move** — a named rhetorical pattern that real regulatory documents use, defined
in `AUTHORING.md` with its structure, the obligation it carries, and an example.
For instance `adverse_disclosure`: state a bad result with its magnitude, then
the mitigating evidence, then the residual position — *in that order*. There are
about 25.

**Register** — the tone class of a section: `boilerplate`, `procedural`,
`analytical`, `argumentative`, `defensive`. Assigned per section; drives density
and hedging.

**Tier** — the write order. Tier 1 sections *create* facts and IDs (deviations,
equipment, method performance); tiers 2 and 3 *cite* them. So tier 1 goes first,
always. Within a tier, sections are independent.

**Ledger** — `build/ledger/<DOC>.md`. Two or three lines per completed section,
recording what it asserts and which IDs it introduced. Each section runs in a
fresh agent context (so they don't all converge on one voice), and the ledger is
the only thing carried between them.

---

## 6. Files

```
ema_docgen/
├── README.md                  you are here
├── DESIGN.md                  why it works this way; decisions and reversals
├── AUTHORING.md               the move taxonomy + rules that always apply
├── AUTHORING_TASK.md          the per-section prompt the agent executes
├── RUNNER.md                  the loop an orchestrating agent follows
├── numerals.allow             lint exemptions for domain nomenclature
├── Makefile.fragment          make targets to append to the repo Makefile
├── docspec/
│   ├── SCHEMA.md              field reference
│   ├── _TEMPLATE.yaml         blank form for a new document
│   └── <DOC_ID>.yaml          pre-populated, one per document (20 files)
├── factpack/
│   ├── SCHEMA.md              field reference
│   ├── _TEMPLATE.yaml         blank form
│   ├── PCR-007/dev_01.yaml    worked examples; all others are stubs
│   └── <DOC_ID>/<SECTION>.yaml  one per docspec section (262 files)
├── schemas/
│   └── insertions.schema.md   the contract for what the agent emits
└── scripts/
    ├── _common.py             shared text handling
    ├── validate_insertions.py schema + anchor checks, run before splicing
    ├── splice.py              the anchor-verified applier
    ├── lint_numerals.py       catches invented numbers
    ├── lint_wordcount.py      section length vs docspec
    ├── lint_overlap.py        catches phrasing copied from source literature
    └── init_factpacks.py      regenerates empty fact-pack stubs
```

Of these, `AUTHORING.md` is the one worth reading in full — it is what the agent
reads on every task, and it defines the moves.

---

## 7. Install

In this repository the wiring is already done: `ema_docgen/` is committed, the
`docgen-*` targets are appended to the root `Makefile`, and `build/` is in
`.gitignore`. A fresh clone needs only the dependency and the working
directories:

```bash
cd /path/to/synthetic_data
pip install pyyaml                                   # only dependency; rest is stdlib
mkdir -p build/insertions build/review build/ledger build/state
```

To wire it into a repo that does *not* yet have it, the one-time step is
`cat ema_docgen/Makefile.fragment >> Makefile` — the targets read `$(PY)` and
`$(PKG_DIR)` from the existing Makefile — plus the two commands above. `build/`
holds insertions, ledgers and state: working files, not corpus artifacts, and
deliberately uncommitted.

Nothing else to configure. Docspecs and fact-pack stubs for all twenty documents
ship pre-populated (see §10). If you add a document later:

```bash
cp ema_docgen/docspec/_TEMPLATE.yaml ema_docgen/docspec/PCR-011.yaml
# edit it, then:
python ema_docgen/scripts/init_factpacks.py ema_docgen/docspec/PCR-011.yaml \
    --root ema_docgen
```

`init_factpacks.py` creates an empty stub for every section in a docspec and
never overwrites an existing one, so it is safe to re-run.

## 8. Running it

### Pilot first — three sections

The docspec is already there. Add real facts to the tier-1 fact packs before
starting — at minimum `factpack/PCR-007/dev_01.yaml`, since an empty fact pack
means the agent has nothing true to say about a deviation and will correctly
refuse to invent one. `factpack/PCR-007/dev_02.yaml` shows the shape.

Then, in Claude Code:

> Execute `ema_docgen/RUNNER.md` for `ema_docgen/docspec/PCR-007.yaml`, tier 1
> only, stop after 3 sections.

Now read `build/review/PCR-007/*.questions.md`. **This is what the pilot is
actually for.** Before drafting, the agent is required to list 6–10 questions a
regulatory assessor would raise about the section, then answer them
pre-emptively in the prose. That step is what produces the defensive, hedged
register that makes real regulatory documents long.

If those questions are generic — "Is the method validated?" — the mechanism is
producing nothing and the move assignments need work before you scale up. If
they are specific and awkward, the kind that would actually come up in a review,
carry on.

### Then a tier at a time

> Execute `ema_docgen/RUNNER.md` for `ema_docgen/docspec/PCR-007.yaml`, tier 2.

```bash
make docgen-check DOC=PCR-007
```

Review at each tier boundary. Per-section review defeats the purpose; reviewing
only at the end finds problems a whole document too late.

### Then freeze

```bash
git add pc_package/PCR-007_cex.qmd
git commit -m "PCR-007: density pass to PCR-008 standard, corpus v2"
git tag corpus-v2
```

Record the model IDs used and the docspec version in the commit message.

> **The corpus is a versioned release, not a build artifact.** Generated prose is
> committed once and frozen. If prose regenerated on every build, the annexes
> would regenerate too — making the answer key non-deterministic and benchmark
> scores incomparable between runs. Regeneration is deliberate and produces
> corpus v2, v3, not a fresh corpus every `make`.

---

## 9. The gates

The checks split into two kinds, and keeping them apart is what lets the runner
make progress (see RUNNER.md). Gating a revert on a whole-document metric would
revert every valid splice, because mid-densification the document is *supposed*
to have short sections and may carry bare numerals that predate the run.

**Blocking — `make docgen-verify DOC=<id>`.** Correctness only. A failure here
means the splice broke something, and the runner reverts it.

| Gate | Catches |
|---|---|
| `validate_insertions.py` (pre-splice) | malformed output, missing or ambiguous anchors, attempted rewrites |
| `quarto render` | broken inline expressions, bad cross-references |
| `build_ground_truth.py` + `validate_annex.py` | annex structure breakage |
| `check_grounding.py` | an annex `quote` that no longer appears verbatim in the render — the additive-only enforcement |

**Advisory — `make docgen-report DOC=<id>`.** Whole-document metrics. Never fails
the build, and never a reason to revert a splice. Read them; act when you choose.

| Report | Surfaces |
|---|---|
| `lint_numerals.py` | bare numerals in prose, i.e. potentially invented numbers |
| `lint_wordcount.py` | sections above/below their docspec target (`LOW`/`HIGH`), or `PEND` for a new section not yet written |
| `lint_overlap.py` | phrasing copied from A-Mab or the guidance documents |

`make docgen-check DOC=<id>` runs the blocking gate then the advisory report, for
a manual look at a tier boundary.

Two of the checks are worth explaining.

**`lint_numerals.py`** flags any digit appearing in prose outside an inline
expression, code block, citation, or identifier. It converts "never invent a
number" from something you hope the prompt achieves into something mechanically
enforced. It needs calibration — domain vocabulary like `wash-1`, `TCID50`,
`ICH Q5A(R2)`, `N-1` looks like numerals but isn't. Add exemptions to
`numerals.allow`; never exempt something that could differ between two runs of
the model.

**`lint_overlap.py`** reports 8-gram overlap between the corpus and the source
literature in `refs/text/`. This protects the benchmark from itself. The A-Mab case study and the cited FDA/ICH guidance are near-certainly in the training data of any model you
evaluate. If the corpus carries their phrasing, retrieval scores measure
memorisation rather than retrieval — a contaminated benchmark, and one that is
very hard to detect afterwards. It also keeps copyrighted text out of a public
repo.

---

## 10. Current state of the corpus

Measured on `main`, July 2026. 20 documents, 58,868 prose words.

### Density

`PCR-008_aex.qmd` is the densest and most complete report and is the standard the
others should reach. Against `PCR-007_cex.qmd`:

- the section taxonomy is **already identical** — there is nothing structural
  left to add
- PCR-008 carries **6,914** prose words to PCR-007's **4,453**, under the same
  headings
- roughly 1,018 words of that gap is uniform per-section density; the remainder
  is two narrated deviation subsections (370 and 782 words) that PCR-007 lacks

So the work is: **seed deviations for the remaining unit operations, narrate
them, and bring the other reports and plans to PCR-008's and PCP-008's
density.**

The shipped docspecs encode exactly that.

**How the targets were derived.** For plans and reports, the target for a section
is the length of that same heading in the reference document of the same class —
`PCR-008_aex` for reports, `PCP-008_aex` for plans. A section is listed only if
it currently sits below 90% of that reference. Everything already at standard is
deliberately absent, which is why the specs are shorter than the documents.
Headings are read from the `.qmd` files and every one is validated against them.

Nothing is invented, and nothing is a round number.

| | docs | sections | current | target | adds |
|---|---|---|---|---|---|
| Plans `PCP-003…010` | 8 | 79 | 7,974 | 12,511 | +4,537 |
| Reports `PCR-003…010` | 8 | 149 | 16,988 | 35,671 | +18,683 |
| Singletons `PTP/RA/PCMP/PCMR-001` | 4 | 34 | 4,087 | 7,100 | +3,013 |
| **total** | **20** | **262** | **29,049** | **55,282** | **+26,233** |

That takes the corpus from 58,868 to roughly 85,000 prose words — about +45%.

`PCP-008` and `PCR-008` ship with `sections: []`. They are the reference
documents; there is no work to plan against them. The files exist so
`make docgen-check DOC=PCR-008` resolves, and so that raising the standard later
means editing them first and regenerating the rest.

**14 of the 262 sections are new** — `dev_01` and `dev_02` on the seven reports
that have no narrated deviations. These are the only entries with
`new_section: true`, and they are the only ones that genuinely need seeded facts
before they can be written. Their fact packs ship as stubs, except `PCR-007`'s,
which are filled in as worked examples.

**The four singleton documents have no peer of the same class.** Their targets
are judgement — roughly 1.4× current, shaped by register — not measurement. Each
file says so at the top. Review those four before running them.

PCR-008 is also the best register exemplar available. It is the corpus's own
prose, so unlike A-Mab it carries no contamination risk. `AUTHORING.md` §4 maps
moves to specific PCR-008 sections.

### Known issues found by the lints

**Bare numerals: 184 flagged lines across the corpus.** Only
`PCR-004_harvest.qmd` is clean. About 70 are recurring constants worth
converting into helpers, because they are study-design decisions that also
appear in the annexes — if text and annex ever drift apart, nothing catches it:

| Constant | Occurrences |
|---|---|
| `α = 0.05` | 13 |
| `p > 0.05` (lack-of-fit) | 12 |
| `R² ≥ 0.90 / 0.80 / 0.75` | 13 |
| `RPN > 72`, `Severity ≥ 8` | 10 |
| `n = 4 replicates` | 6 |
| `effect = 2 × coded coefficient` | 6 |
| `2 L` scale-down volume | 4 |
| `p < 0.001`, `95% CI/PI`, `15/25 °C` | 5 |

Figure and table **captions** are where most hardcoded numbers survive, because
they sit outside the code blocks that generate everything else.

**⚠ Source-text overlap in `PTP-001_transfer.qmd`.** Nineteen of twenty
documents are clean (0–8 overlapping 8-grams against 261,401 reference 8-grams,
all of it abbreviation-list content). PTP-001 carries 11, and five of them chain
into a single **~12-word verbatim run** beginning *"a comparability plan
describes the actions to be taken in the event…"*, carried in from the ICH Q10 — the document PTP-001 is the first to cite. Reword
before tagging a release.

**Missing: `pc_package/HELPER_API.md`.** `AUTHORING_TASK.md` expects a flat list
of the inline expressions and helper functions available to document authors. It
does not exist, so the agent has to infer them from `_pcpkg.py` and
`doe_report.py`. `_pcpkg.py` recently gained `corpus_docs_md`,
`process_steps_df`, `cpp_params` and `class_counts`, which are undiscoverable
except by reading the source. Writing that list is probably the cheapest single
improvement to first-pass output quality.

---

## 11. What tends to go wrong

In rough order of likelihood on a first run:

1. **A flood of `<<NEEDS:>>` markers.** When the agent needs a value that has no
   helper, it is required to emit `<<NEEDS: description>>` rather than invent
   one. Lots of these means the fact pack is thin — the work is in
   `amab_process/`, not in the prompt. Triage with
   `grep -rn "<<NEEDS:" pc_package/`.
2. **Ambiguous anchors.** Sentences like "The results are summarized below."
   occur in several sections; the validator refuses rather than guessing. Fix by
   choosing a longer anchor.
3. **Fabricated restatement.** Sections are asked to restate a claim made
   elsewhere, in different words, because that is what creates coreference
   difficulty for the benchmark. If the ledger entry was vague, the agent will
   restate a claim that does not exist — and no gate catches this. Write ledger
   entries as concrete claims, not topics. This is the failure worth watching.

---

## 12. Further reading

`DESIGN.md` records why the design is shaped this way, including three decisions
that were reversed during development — most importantly why source literature
is *not* used as a style exemplar, and why the measured evidence contradicted the
initial assumption that the documents needed to be four times longer.
