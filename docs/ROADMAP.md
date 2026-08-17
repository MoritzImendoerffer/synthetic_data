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
| — | Make the corpus argue: the register campaign | **Unplaced: the project owner has to set the row.** Raised 2026-08-16 — the prose is not what an SME would write, although every document passes the gate. **Partly delivered 2026-08-17**: four sources extracted, the band recalibrated on all four, the `therefore` cap removed, `WRITING_GUIDE.md` §2c/§2d/§2d bis amended, the moves catalogue added, the discrepancy carrier built, and `PCP-003` + `PCR-003` re-authored and measured. The pilot returned **one clean win in five** ([results](results/2026-08-17-register-pilot.md)) — the connective repertoire — so the remaining 18 are **blocked on a second two-document round** with a stopping rule fixed in advance. The spaCy question is settled (2026-08-17, owner: yes, as an **optional** extra), so Track 1 is unblocked and ready to plan. | [next/register-from-four-sources.md](next/register-from-four-sources.md) |
| 1 | Rhetorical layer: one mechanism, eleven missing documents | It is the part of the annex nothing else supplies, it covers 9 of 20 documents, and it is built two ways for no reason anyone recorded | [next/rhetorical-layer-coverage.md](next/rhetorical-layer-coverage.md) |
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
