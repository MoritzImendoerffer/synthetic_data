# One rhetorical layer, two mechanisms, eleven documents without it

**Status:** proposed 2026-08-16. Not started. No work unit.

## The problem

The discourse layer is the part of the annex an NLP consumer cannot get anywhere else: which
sentence is a claim, which justifies it, which bounds it, which defers. Measured on `main` on
2026-08-16, it covers **9 of 20 documents and 315 spans**:

| Document | Spans | Built by |
|---|---|---|
| PCR-003 | 35 | `authoring/rhetorical/PCR-003.spans.yaml`, read by `build_rhetorical_spans()` |
| PCR-004 | 36 | `h_rhetorical_spans()` in `build_ground_truth.py` |
| PCR-005 | 39 | `pa_rhetorical_spans()` |
| PCR-006 | 31 | `vi_rhetorical_spans()` |
| PCR-007 | 33 | `cx_rhetorical_spans()` |
| PCR-008 | 25 | `ax_rhetorical_spans()` |
| PCR-009 | 37 | `vf_rhetorical_spans()` |
| PCR-010 | 30 | `uf_rhetorical_spans()` |
| PCMR-001 | 49 | `pcmr_rhetorical_spans()` |

**Eleven documents carry none**: the eight plans `PCP-003` … `PCP-010`, plus `PTP-001`, `RA-001`
and `PCMP-001`. Every one of them argues — a plan states what it will accept and why, a risk
assessment states a ranking and its warrant — and none of that is annotated.

**And one layer is built two ways.** PCR-003 alone is curated in YAML and documented in
`authoring/RHETORICAL_ANNEX.md`. The other eight are Python functions inside
`build_ground_truth.py`, one per unit operation, with the quotes written into the source. A
consumer cannot tell the two apart in the output, but a maintainer meets a different file, a
different failure mode and a different re-curation cost depending on which document they opened.

The two also fail differently. The YAML path is a hard gate: a span whose quote no longer matches
the document fails the build for that document with a message naming the file to re-curate
(`build_ground_truth.py:810`). That is the right behaviour, and it was learned expensively — a
presence check that skipped normalisation once declared the PCR-003 layer dead and aborted a build
partway, leaving later annexes stale on disk while the run looked fine under `2>/dev/null`.

## What is not the problem

**The PCR-003 layer is not stale.** `authoring/HANDOFF.md` §"Next" says its curated spans quote
superseded text and 34 of 37 no longer match. Checked on 2026-08-16:
`uv run python authoring/build_rhetorical_annex.py --doc PCR-003` writes 35 spans and drops none.
The same section lists "PCR-008 rhetorical layer" as outstanding; PCR-008 has 25 spans. Both
sentences were true when written and are false now, which is the reason this proposal exists
rather than a re-curation task.

## The idea

Pick one mechanism, and extend the layer to the documents that have none. In that order: a second
mechanism applied to eleven more documents is twenty-one places to change the day a role is added
to the vocabulary.

## What it would take

1. **Decide the mechanism.** YAML is editable by a person who is not reading Python and keeps
   `build_ground_truth.py` from growing another 300 lines per document. Python keeps the quotes
   beside the entity builders that already ground against the same rendered text. The measured
   argument for YAML is size: the eight Python builders are the largest single block in a 7,000
   line file. The measured argument for Python is that eight of nine layers already use it.
2. **Migrate the odd one out**, whichever way the decision goes, so the corpus has one path.
3. **Author the missing eleven.** A plan's argument is not a report's: it commits rather than
   concludes, so `problem_statement`, `deferral` and `bounded_conclusion` will carry more weight
   than `justification`. Expect the role mix to differ, and do not force a report's shape onto a
   plan.
4. **Extend the gate.** `check_grounding.py` already gates every rhetorical quote as a
   `SourceReference`. Nothing checks *coverage* — that a report with an argument has spans over
   it. A count per document, printed with its denominator, would have made the eleven visible
   without anyone counting by hand.

## Verification

- `cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py` →
  `20/20 annexes valid`.
- `GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py` → every new span verbatim, and the
  total quote count rises from 2084 by the number of spans added.
- A per-document rhetorical span count printed by the build, so the next reader does not have to
  write a script to find out what is covered.

## What this deliberately does not do

It does not add roles to the vocabulary, and it does not touch a document. The rhetorical layer is
annotation *over* finished prose: nothing is added to a document after authoring, and a span that
will not ground is re-anchored or dropped, never fixed by editing the text.

It also does not restore weak claims. `weak_claim` is a role the annex schema knows and `main`
never uses. That is a separate argument, on its own branch.

## Open questions

- Is a **plan** worth annotating at all, or is the argument only interesting where a conclusion is
  drawn? Eleven documents is most of the remaining work, and the answer decides whether this is a
  small job or a large one.
- Does `RA-001` need a role the report vocabulary does not have — a ranking is neither a claim nor
  a justification — and if so, is that a `schema_ext.py` extension?
