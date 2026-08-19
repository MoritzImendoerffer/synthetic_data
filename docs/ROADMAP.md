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
| 0 | The author-facing apparatus, tested on one section first | **D4 = PASS, 2026-08-19.** The two `PCR-005` Results subsections all eight quoted sentences came from were re-authored by the same model under a minimal regime (5,746 words of input, no counters, a role and a reader) and read blind against the shipped text: **"A clearly wins"** — A was the probe, no sentence quoted from it. Trailing relatives 28.8 → 6.7 per 100 sentences, hollow-warrant frames 5 → 0, with no rule about either; and every measure rounds one to three had gated or printed (`, so ` 8.9 %, `, and `+clause 15.6 %, passive 31.8 %) sits at or beyond round-zero in the text the reader preferred. **The current gate FAILS the probe** (`pct_over_40` 1.1 vs floor 3.0, `rather than` 1.6 vs 0.8) and passes the shipped text. Tasks 2–6 of the proposal now run: gate split, obligations to a reviewer checklist, short positive guide, per-step mechanism, content review before promotion. [Results](results/2026-08-19-apparatus-probe.md) | [next/author-facing-apparatus.md](next/author-facing-apparatus.md) |
| — | Make the corpus argue: the register campaign | **Unplaced, and now blocked on a rebuilt gate rather than on more re-authoring.** Four rounds delivered ([one](results/2026-08-17-register-pilot.md), [two](results/2026-08-18-register-round-two.md), [three](results/2026-08-18-register-round-three.md), [Track D stopped](results/2026-08-18-track-d-stopped.md)). Track D re-authored three of nineteen documents as a pilot, **all eight numeric stopping conditions held, and the owner's reading rejected them anyway** — eight sentences quoted from `PCR-005`, every one outside the human band on a measure nobody had gated. Trailing relatives run **11.39 per 100 sentences against sources at 1.20–2.97**, and `acts on / acts through` runs **63 in the corpus against zero in 3,338 sentences of published source**. The fault is in `PCR-003` too, the accepted control, so it predates all four rounds. **The finding that blocks the next round: the eight sentences rewritten as a paper would write them FAIL the register gate**, `mean_len` 13.5 against a gated floor of 20.0 and `pct_under_15` 55.6 % against a gated ceiling of 32.0. The gate built to stop machine register now enforces it. Nothing more should be re-authored until §8 of the results page is done: supply the mechanism, fix the two bands, print the trailing-relative count, audit the 26 `mechanistic_warrant` spans. **Row 0 above argues that §8 treats four symptoms of one cause and puts a one-section probe in front of all of it.** | [next/register-from-four-sources.md](next/register-from-four-sources.md) |
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
| `nlp_reports` does not recognise this corpus's document ids | **Closed by verification, 2026-08-16, no change needed.** `pc_package/TASKS.md` said its `DOCUMENT_ID` pattern recognises `PCR/PVR/PPQ/TT/VAL/AMV/SOP/CS` but not `PTP/PCP/PCMP/PCMR/RA`. It builds the pattern from `settings.document_id_prefixes`, whose default is `PCMP,PCMR,PCP,PCR,PPQ,PTP,PVR,AMV,SOP,VAL,CS,RA,TT` — all five are there, longest first so `PCP` cannot shadow `PCMP`. Nothing to add, and nothing to change in a read-only repository |
| PCR-003's rhetorical layer quotes superseded text | **Closed by verification, 2026-08-16.** `build_rhetorical_annex.py --doc PCR-003` writes 35 spans and drops none. The "34 of 37 dropped" line in `HANDOFF.md` §Next was true before the re-curation and is not now |
| DEV-005-01 contradicts its design matrix | **Closed in the config.** `LOT-BUF-5290` is bound to RSM run 23, with the reason recorded at `config/parameters.yaml:559`. Only `HANDOFF.md` §3a still lists it |
| Row-anchor every annex record | **Delivered 2026-08-03** as `02a170a`. Row anchors 285 → 653, annexes with at most one row anchor 14 → 0, gated spans 1476 → 2084. [results/2026-08-03-annex-anchors.md](results/2026-08-03-annex-anchors.md) |
| Judge each step against an in-process limit | **Delivered** as `083bfb1` and `d7b5ec2`. PARs are judged against per-step in-process limits from `config`'s `ipc_limits`, not against drug-substance specs |

## How an item moves

`docs/ROADMAP.md` → `docs/next/<name>.md` → `/explore` → `/plan` → `/next` → `/ship` → the row here
says what is now true, and the proposal is deleted. The loop is
[`PROJECT_WORKFLOW.md`](PROJECT_WORKFLOW.md).
