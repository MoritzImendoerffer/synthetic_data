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
| — | [register-from-four-sources.md](register-from-four-sources.md) | **proposed 2026-08-16, explored the same day, work unit `2026-08-16_01_register-from-four-sources`. Still unplaced — the roadmap row is the owner's to set.** **The proposal was rewritten after exploration**: its first version treated the register as a sentence-statistics problem and that mechanism is wrong. Measured against both human sources: 35 % of corpus sentences continue the previous sentence's topic against 57–60 %; `However` and `For example` appear **zero** times in ~30,000 words against 46/12 in A-Mab and 21/22 in PDA; 33 % of PCR-003 sentences are shaped "X is \<noun phrase\>" against 15–18 %; `its` runs 6.67 per 1k against A-Mab's 0.28. Eight competing hypotheses returned null — sentence length, complexity, word order, nominalisation, formulaicity, over-claiming, coordination, number density — so **no threshold of the kind `check_style.py` already carries will reach it**. The cause was in the repository: `WRITING_GUIDE.md` §2c/§2d forbade a paragraph that holds a claim beside its counter-consideration, the gate capped the one connective still in use, and `REGISTER_EXEMPLAR.md` had no plan-genre passage although 10 of 20 documents are plans. **All three are fixed as of 2026-08-17** (TASK-002, TASK-003, TASK-004): the guide licenses one narrow exception with four shapes, the `therefore` cap is gone and connectives are a diagnostic that fails nothing, and the exemplar carries 120 verified quotes from four sources. The owner permitted ISPE quoting. **A two-document pilot was authored against the amended artifacts on 2026-08-17** (TASK-007): `PCP-003` and `PCR-003`, one agent each, one pass each, neither reading the other. Both pass the render and register gates. They are drafts under a throwaway filename, so **no corpus document has changed yet** — promoting them, re-anchoring their annexes and measuring the result is TASK-008 and TASK-009, and whether the other 18 follow is decided on that measurement. | any claim that this corpus reads like SME prose |
| 1 | [rhetorical-layer-coverage.md](rhetorical-layer-coverage.md) | **proposed 2026-08-16, not started.** The discourse layer covers 9 of 20 documents and 315 spans, and is built two ways: PCR-003 from `authoring/rhetorical/PCR-003.spans.yaml`, the other eight from per-step Python builders in `build_ground_truth.py`. Eleven documents carry none — the eight plans, `PTP-001`, `RA-001`, `PCMP-001`. Corrects two claims in `HANDOFF.md` §Next: the PCR-003 layer builds 35 spans and drops none, and PCR-008 has 25. | any consumer that needs to know which sentence is a claim and which justifies it |
| 2 | [seeded-data-tensions.md](seeded-data-tensions.md) | **proposed 2026-08-16. The decision is the owner's.** Two live tensions of the three §3a lists: the acidic-variants range prints `18–40` while capability is assessed against the ceiling alone (making it two-sided moves the headline min Cpk 1.51 → 1.03), and three `cal_due` dates pre-date `EFFECTIVE_DATE` while the equipment table says the equipment was in calibration. The third, DEV-005-01, is already fixed in config and only HANDOFF has not caught up. | nothing; it decides whether two known tensions are benchmark items or bugs |
| 3 | [weak-claims-branch.md](weak-claims-branch.md) | **proposed 2026-08-16, parked by the project owner the same week (`97f94fc`).** `feature/weak-claims-via-brief` is 1 commit ahead of `main` and 4 behind, and both sides re-authored the same documents. A rebase has to pick a text per document and both picks lose something real. Decides nothing: it separates the settled part (never merge; assign claims in the brief; `main` stays fully grounded) from the open one. | any use of this corpus as an unsupported-claim benchmark |

## Where finished work goes

A proposal that gets built moves its findings into `docs/results/` (if it produced a measurement)
and its description into the relevant `docs/`, `authoring/` or `pc_package/` page. The file here is
then deleted rather than left as a stale plan — `git` keeps the history, and a plan that no longer
matches the repository is worse than no plan.
