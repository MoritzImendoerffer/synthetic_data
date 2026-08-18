# One rhetorical layer, two mechanisms, eleven documents without it

**Status:** proposed 2026-08-16. **Half done 2026-08-18** by TASK-001 of work unit
`2026-08-18_02_register-track-d`: the mechanism is now one, and it is YAML. The other half —
eleven documents with no layer at all — is untouched and is what this proposal is still for.

## The problem

The discourse layer is the part of the annex an NLP consumer cannot get anywhere else: which
sentence is a claim, which justifies it, which bounds it, which defers. Measured on `main` on
2026-08-16, it covers **9 of 20 documents and 315 spans**:

| Document | Spans | Built by (as of 2026-08-18) |
|---|---|---|
| PCR-003 | 35 | `authoring/rhetorical/PCR-003.spans.yaml`, read by `build_rhetorical_spans()` |
| PCR-004 | 36 | `authoring/rhetorical/PCR-004.spans.yaml` |
| PCR-005 | 39 | `authoring/rhetorical/PCR-005.spans.yaml` |
| PCR-006 | 31 | `authoring/rhetorical/PCR-006.spans.yaml` |
| PCR-007 | 33 | `authoring/rhetorical/PCR-007.spans.yaml` |
| PCR-008 | 25 | `authoring/rhetorical/PCR-008.spans.yaml` |
| PCR-009 | 37 | `authoring/rhetorical/PCR-009.spans.yaml` |
| PCR-010 | 30 | `authoring/rhetorical/PCR-010.spans.yaml` |
| PCMR-001 | 49 | 32 in `authoring/rhetorical/PCMR-001.spans.yaml`, plus 17 register rows from `pcmr_dev_spans()` |

**Eleven documents carry none**: the eight plans `PCP-003` … `PCP-010`, plus `PTP-001`, `RA-001`
and `PCMP-001`. Every one of them argues — a plan states what it will accept and why, a risk
assessment states a ranking and its warrant — and none of that is annotated.

~~**And one layer is built two ways.**~~ **Closed 2026-08-18.** It was true when this was
written: PCR-003 alone was curated in YAML, and the other eight were Python functions inside
`build_ground_truth.py`, one per unit operation, with the quotes written into the source. A
consumer could not tell the two apart in the output, but a maintainer met a different file, a
different failure mode and a different re-curation cost depending on which document they opened.

The two also failed differently, and that is what decided the direction. The YAML path is a hard
gate: a span whose quote no longer matches the document fails the build for that document with a
message naming the file to re-curate. That is the right behaviour, and it was learned
expensively — a presence check that skipped normalisation once declared the PCR-003 layer dead and
aborted a build partway, leaving later annexes stale on disk while the run looked fine under
`2>/dev/null`. The Python builders had no presence check at all and emitted every span
unconditionally, so a stale one surfaced only later, as an ungrounded quote in `check_grounding`.
Converting the 263 curated Python spans to YAML put all nine documents behind that gate. The
annexes rebuilt byte-identical, which is what proves the conversion changed nothing.

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

1. ~~**Decide the mechanism.**~~ **Done 2026-08-18: YAML.** The measured argument that decided
   it was size — the eight Python builders were 994 lines, the largest single block in a 7,000
   line file — together with the gate, which only the YAML path had.
2. ~~**Migrate the odd one out.**~~ **Done 2026-08-18**, the other way round from the phrasing
   here: it was the eight that moved, not PCR-003. 263 curated spans became eight
   `.spans.yaml` files; the 17 data-derived deviation rows of PCMR-001 stayed in code, because a
   rendered row of `outputs/deviations.csv` is not curated prose and a reseed rewrites it.
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
