---
type: pm-decision
sprint: 2026-08-19_01_fourth-round-one-document
status: settled 2026-08-19 — PASS
decided_by: project owner
unblocked: TASK-006, TASK-007
tags: [pm/decision]
---

# D6 — does the whole document written under the rebuilt apparatus read as a paper?

**What is being asked.** Two PDFs, `A.pdf` and `B.pdf`, both the whole `PCR-007` report. One is the
shipped report; the other was written in one pass by one `claude-opus-5` agent under
`authoring/RUNNER.md` as rebuilt on 2026-08-19 — the brief with the step's mechanism, the section
plan as structure, the story bible, the 122-line guide, the exemplar, and no counter, no obligation,
no grep list — then reviewed once on the four content questions and returned to its author once if
any read "no". Which is which is sealed in `blind-key.md`, drawn before the new one was written.

You are asked what every reading in this campaign was asked, on the suggested subset (Executive
summary; Results, all four subsections; Design space; Discussion) or more: **quote the sentences
that read as machine prose, with A or B; and say which reads as a paper.** Your words are recorded
verbatim before the key is opened.

**The rule, fixed before the document was written** (`state.json → decisions.pass_rule`): **PASS**
if you judge the new document the better text *and* quote fewer than five sentences from it across
what you read. Anything else is **FAIL**. Applied mechanically.

**Option A — PASS.** The new `PCR-007` is promoted: rendered, its 33 spans re-cut, its 88 annex
quotes re-anchored, the corpus re-grounded (TASK-006, TASK-007), and the results page says one
document is at the rebuilt-apparatus register. Whether the remaining documents follow is your next
call and a new `/explore`.

**Option B — FAIL.** The draft stays in the unit as evidence, nothing is promoted, and the results
page records what you named — which is then the next thing to change in the RUNNER's inputs before
another document is tried.

**What the plan assumes meanwhile.** Nothing that depends on the answer runs before it. The
difference from the probe: this is a whole document — an executive summary that has to match its
conclusions, cross-references, a SETUP chunk the agent wrote itself — and you have read neither
version before, so no "fourth reading" limit applies.

---

**Settled 2026-08-19 — PASS.** The reading, verbatim
(`.claude/work/2026-08-19_01_fourth-round-one-document/owner-reading-2026-08-19.md`): "B is clearly
bette[r] to read … B reads more like a paper", three sentences quoted from A as machine-generated,
none from B. Key opened afterwards by checksum: **B was the new document.** Rule: new judged
better, 0 < 5 sentences quoted → PASS. TASK-006 (promote, re-anchor, re-ground) and TASK-007 run.
