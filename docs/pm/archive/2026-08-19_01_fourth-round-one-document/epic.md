---
type: pm-epic
sprint: 2026-08-19_01_fourth-round-one-document
status: shipped 2026-08-19
started: 2026-08-19
proposal: docs/next/register-from-four-sources.md
tags: [pm/epic]
---

# Epic — the fourth round: one whole document under the rebuilt apparatus

Board: [[_Board]] · decisions: [[D5-which-document]], [[D6-does-the-whole-document-pass]] ·
proposal: [`docs/next/register-from-four-sources.md`](../next/register-from-four-sources.md) (its
2026-08-19 pointer) · exploration:
`.claude/work/2026-08-19_01_fourth-round-one-document/exploration.md` · plan:
`.claude/work/2026-08-19_01_fourth-round-one-document/implementation-plan.md` · what it follows:
[`docs/results/2026-08-19-apparatus-probe.md`](../results/2026-08-19-apparatus-probe.md)

**Shipped 2026-08-19.** `PCR-007` was authored in one pass by one agent under `RUNNER.md` as
rebuilt, went through one content-review cycle, and was preferred blind by the owner over the
shipped report — "B is clearly better to read … B reads more like a paper", no sentence quoted from
it (D6 = PASS). Promoted: 33 spans re-cut, 31 of 110 annex quotes re-anchored, 2084/2084 grounded,
20/20 valid, `outputs/` untouched, 50 pp. Found on the way: the first author fetched the reviewer's
table itself (`check_style.py --review`) and tuned to it; that draft was set aside and `RUNNER.md`
now says the author runs `check_render` and nothing else. Not shipped, the owner's call: the
remaining documents. Results:
[`docs/results/2026-08-19-fourth-round-PCR-007.md`](../results/2026-08-19-fourth-round-PCR-007.md).

**Why it opened.** The probe showed on two subsections that the author-facing apparatus, not the
model, produced the prose the owner rejected, and the apparatus was rebuilt: five tics gate,
obligations to a reviewer's checklist, a short positive guide, each step's mechanism in the brief,
a content review before promotion. No whole document has been written under it. Fifteen documents
sit at round zero; `PCR-007` measured today: `, which` **10.5** per 100 sentences (sources 0.6–2.4),
`, so ` **10.3 %** (0.1–0.4), passive **48.8 %** (57–64), chaining **37.2 %** (56–62).

**What it does.** Authors `PCR-007` in one pass by one agent under `authoring/RUNNER.md` as
rebuilt, runs the content review once, and puts the shipped and the new report in front of the
owner blind under a rule fixed in advance (new preferred and fewer than five sentences quoted).
On PASS it promotes: render, 33 spans re-cut, 88 quotes re-anchored, corpus re-grounded. Then a
results page against the same script as every round.

**What it does not do.** Touch any other document; run `make data figures`; add a rule to the
author's inputs; decide about the remaining eighteen.

**The shape.** TASK-001 (prompt, key, brief, scaffold, reading protocol) → TASK-002 (one agent) →
TASK-003 (content review, one cycle) → TASK-004 (the reading, **hard stop**, D6) → TASK-005
(counts, page) → on PASS TASK-006/007 (promote, prove) → TASK-008 (ship).
