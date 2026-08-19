# Roadmap — what is open, in what order

This file owns the **order**. [`next/`](next/) owns the **argument** for each item, one file each.
Nothing is promoted here without a reason written down, and nothing is worked on that is not here.

**The corpus itself is complete**: 20 documents, all one-pass authored, rendered, annexed and
grounded. Verified on 2026-08-16 from an unmodified checkout — `20/20 annexes valid`,
`2084/2084 quotes grounded` with `GROUNDING_STRICT_ANCHORS=1`, 85 tests passing. So nothing below
is a gap in the deliverable. These are the things a second pass would want.

**The ordering is the project owner's.** The numbers below are a first sequencing, not a decision
that has been taken. Reorder freely; the argument for each item lives in its proposal.

## What to do next, in order

| # | Item | Why it is here | Proposal |
|---|---|---|---|
| — | Make the corpus argue: the register campaign | **Fifth result, 2026-08-19: a whole document under the rebuilt apparatus passed the owner's blind reading** — `PCR-007` re-authored in one pass by one agent under `RUNNER.md` as rebuilt plus one content-review cycle, "B is clearly better to read … reads more like a paper", no sentence quoted from it, promoted and re-grounded (2084/2084). It lands where the probe landed (trailing relatives 6.6 per 100 sentences against 11.9 shipped; the round-one-to-three counters unchanged and the reader did not mind). Found on the way: the first author fetched the reviewer's table itself; `RUNNER.md` now forbids it. The corpus is split across registers: `PCR-007` at the rebuilt apparatus, `PCR-003` round three, `PCP-003` round two, the Track D pilot three, **fourteen at round zero**. Earlier rounds: [one](results/2026-08-17-register-pilot.md), [two](results/2026-08-18-register-round-two.md), [three](results/2026-08-18-register-round-three.md), [Track D stopped](results/2026-08-18-track-d-stopped.md), [the probe](results/2026-08-19-apparatus-probe.md), [the fourth round](results/2026-08-19-fourth-round-PCR-007.md). **What remains is the owner's call: the remaining documents, under the same regime, in the owner's order — and whether a plan behaves the way a report did.** | [next/register-from-four-sources.md](next/register-from-four-sources.md) |
| 1 | Rhetorical layer: eleven missing documents, and an audit of the labels | **Half done 2026-08-18**: one mechanism now, all 263 code-built spans converted to YAML with every annex byte-identical. Eleven documents still carry none. **New, and it outranks the coverage gap**: 6 of the 26 spans labelled `mechanistic_warrant` carry a hollow-warrant frame, so the labelled benchmark teaches that naming a category is giving a cause | [next/rhetorical-layer-coverage.md](next/rhetorical-layer-coverage.md) |
| 2 | The two live seeded-data tensions | An unregistered inconsistency is a bug and a registered one is a benchmark item. These two are currently neither, and one of them moves the headline min Cpk from 1.51 to 1.03 | [next/seeded-data-tensions.md](next/seeded-data-tensions.md) |
| 3 | The weak-claims branch | It drifts further behind `main` with every corpus change, and the cost of carrying it forward is three one-pass re-authorings | [next/weak-claims-branch.md](next/weak-claims-branch.md) |

## Open, no proposal written yet

A row here says the item exists and that nobody has designed it. **Verify it before writing the
proposal** — every claim below is second-hand, and this repository has a record of status lines
outliving the thing they describe.

| Item | What is known | What to check first |
|---|---|---|
| A gate for row-quote reconstruction | `authoring/HANDOFF.md` records "tracked as a gate to add": a row rebuilt by the annex builder must reproduce tabulate's cell wrapping, or a row containing a hyphen-broken cell (`re- assayed`) will not ground | Whether it still bites. The corpus is at 2084/2084 with strict anchors, so if it does bite it does so only for a row that does not exist yet |
| A `docs/` audit against the code | Three claims in `HANDOFF.md` §Next / §3a and `TASKS.md` were checked on 2026-08-16 and all three were false | How many more there are. The three found so far were each found by running one command |

## Recently closed

| Item | What happened |
|---|---|
| The author-facing apparatus, tested on one section first | **Delivered 2026-08-19** (`2026-08-18_03_author-facing-apparatus`). The probe passed blind — "A clearly wins", A the probe, no sentence quoted — and every counter three rounds had targeted was at or beyond round-zero in the preferred text; the gate as it stood failed it. Rebuilt: `check_style.py` gates five tics and prints the rest to a reviewer under `--review`; `section_plan.yaml` is an outline and the obligations are `authoring/REVIEW_CHECKLIST.md` (+ four content questions, calibrated); `WRITING_GUIDE.md` is 122 positive lines; `authoring/mechanism/` supplies each step's physical chemistry as brief §2b, owner-read; the brief carries no counter. Corpus byte-identical: 20/20 valid, 2084/2084 grounded. Not done, and the owner's call: one whole document under the rebuilt apparatus. [Results](results/2026-08-19-apparatus-probe.md) |
| `nlp_reports` does not recognise this corpus's document ids | **Closed by verification, 2026-08-16, no change needed.** `pc_package/TASKS.md` said its `DOCUMENT_ID` pattern recognises `PCR/PVR/PPQ/TT/VAL/AMV/SOP/CS` but not `PTP/PCP/PCMP/PCMR/RA`. It builds the pattern from `settings.document_id_prefixes`, whose default is `PCMP,PCMR,PCP,PCR,PPQ,PTP,PVR,AMV,SOP,VAL,CS,RA,TT` — all five are there, longest first so `PCP` cannot shadow `PCMP`. Nothing to add, and nothing to change in a read-only repository |
| PCR-003's rhetorical layer quotes superseded text | **Closed by verification, 2026-08-16.** `build_rhetorical_annex.py --doc PCR-003` writes 35 spans and drops none. The "34 of 37 dropped" line in `HANDOFF.md` §Next was true before the re-curation and is not now |
| DEV-005-01 contradicts its design matrix | **Closed in the config.** `LOT-BUF-5290` is bound to RSM run 23, with the reason recorded at `config/parameters.yaml:559`. Only `HANDOFF.md` §3a still lists it |
| Row-anchor every annex record | **Delivered 2026-08-03** as `02a170a`. Row anchors 285 → 653, annexes with at most one row anchor 14 → 0, gated spans 1476 → 2084. [results/2026-08-03-annex-anchors.md](results/2026-08-03-annex-anchors.md) |
| Judge each step against an in-process limit | **Delivered** as `083bfb1` and `d7b5ec2`. PARs are judged against per-step in-process limits from `config`'s `ipc_limits`, not against drug-substance specs |

## How an item moves

`docs/ROADMAP.md` → `docs/next/<name>.md` → `/explore` → `/plan` → `/next` → `/ship` → the row here
says what is now true, and the proposal is deleted. The loop is
[`PROJECT_WORKFLOW.md`](PROJECT_WORKFLOW.md).
