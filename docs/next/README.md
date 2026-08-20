# docs/next — proposals, one file each

Detailed plans linked from [`../ROADMAP.md`](../ROADMAP.md) live here. The roadmap stays a list of
what is open and why; anything that needs a page of design gets its own file in this folder and is
linked from its roadmap row.

**A file here is not a commitment.** It says what would be built, what it would cost, and how it
would be checked, so the decision can be made on paper instead of in an editor.

**A proposal is the requirements, and there is only one copy.** `/explore` records the *path* to
the file and never copies its content into the work unit. Two descriptions of one task drift, and
the drift is invisible until somebody builds the wrong one.

## What a proposal contains

| Section | Why |
|---|---|
| **The problem** | with the measurement that showed it, not an opinion. In this repository that usually means a count from a gate |
| **What is not the problem** | the claims you checked and found already false. This corpus's status files go stale quietly |
| **The idea** | one paragraph before any detail |
| **What it would take** | files, rough size, and which of the four layers it touches |
| **Verification** | the gate output that would say it worked, with denominators |
| **What it deliberately does not do** | the limits, stated by the author rather than discovered by the reader |
| **Open questions** | what the author could not decide |

**Every claim of absence is checked before it is written.** "Nothing builds X", "no document has
Y" — run the thing. Three such claims in this repository's own documentation were checked on
2026-08-16 and all three were false.

## The proposals

Ordered by the priority [`../ROADMAP.md`](../ROADMAP.md) records. The roadmap holds the ordering
and the argument for it, so the two files cannot drift into disagreeing about what comes next.

| # | Proposal | Status | Blocks |
|---|---|---|---|
| — | [register-from-four-sources.md](register-from-four-sources.md) | **Being worked on since 2026-08-19 in `2026-08-19_02_fifth-round-plan-then-batches`**: the remaining documents under the rebuilt apparatus — `PCP-005` first (a plan, the genre not yet tested; the owner's choice), read blind; then the other eighteen in batches with the content review, a transcript audit for self-measurement, and one owner reading sampled per batch. The fourth round (`PCR-007`) passed on 2026-08-19 ([results](../results/2026-08-19-fourth-round-PCR-007.md)); `PCP-005` and batch B1 are authored, promoted and grounded. **Running again since 2026-08-20.** Five sampled readings passed and two failed, both on `PCR-008` and both to the round-zero text; the second failure followed a full re-author, which ruled out a bad draw and produced the diagnosis. The owner amended the frozen regime once in response: the content review's question 1 moved into the author's guide, so rule 4 now puts the cause in the clause with its causal verb and says what a convention buys where the cause is not a species. B2 is released and authored under that rule, `PCR-008` gets a third attempt alongside it, and the five documents written before the rule stand: see [D8](../pm/decisions/D8-do-the-batches-continue.md). |
| 1 | [comparison-claims-unchecked.md](comparison-claims-unchecked.md) | **proposed 2026-08-20.** Every number in the corpus is pulled from the config and gated; every *comparison between* numbers is authored prose and gated by nothing. Eight defects of this class were found by hand in one day across six documents — four Tool #1 claims, a superlative that was backwards, one that ranked eight methods against a table of two, an "order of magnitude" that was six. Proposes a reviewer's worksheet, never a gate and never author-facing, with the eight as a labelled selftest. | any consumer that trusts a sentence about the numbers as much as the numbers |
| 1 | [rhetorical-layer-coverage.md](rhetorical-layer-coverage.md) | **proposed 2026-08-16, not started.** The discourse layer covers 9 of 20 documents and 315 spans, and is built two ways: PCR-003 from `authoring/rhetorical/PCR-003.spans.yaml`, the other eight from per-step Python builders in `build_ground_truth.py`. Eleven documents carry none — the eight plans, `PTP-001`, `RA-001`, `PCMP-001`. Corrects two claims in `HANDOFF.md` §Next: the PCR-003 layer builds 35 spans and drops none, and PCR-008 has 25. | any consumer that needs to know which sentence is a claim and which justifies it |
| 2 | [seeded-data-tensions.md](seeded-data-tensions.md) | **proposed 2026-08-16. The decision is the owner's.** Two live tensions of the three §3a lists: the acidic-variants range prints `18–40` while capability is assessed against the ceiling alone (making it two-sided moves the headline min Cpk 1.51 → 1.03), and three `cal_due` dates pre-date `EFFECTIVE_DATE` while the equipment table says the equipment was in calibration. The third, DEV-005-01, is already fixed in config and only HANDOFF has not caught up. | nothing; it decides whether two known tensions are benchmark items or bugs |
| 3 | [weak-claims-branch.md](weak-claims-branch.md) | **proposed 2026-08-16, parked by the project owner the same week (`97f94fc`).** `feature/weak-claims-via-brief` is 1 commit ahead of `main` and 4 behind, and both sides re-authored the same documents. A rebase has to pick a text per document and both picks lose something real. Decides nothing: it separates the settled part (never merge; assign claims in the brief; `main` stays fully grounded) from the open one. | any use of this corpus as an unsupported-claim benchmark |

## Where finished work goes

A proposal that gets built moves its findings into `docs/results/` (if it produced a measurement)
and its description into the relevant `docs/`, `authoring/` or `pc_package/` page. The file here is
then deleted rather than left as a stale plan — `git` keeps the history, and a plan that no longer
matches the repository is worse than no plan.
