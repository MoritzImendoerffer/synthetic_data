# Implementation plan — Track D: bring the whole corpus to one register

**30 tasks. 19 documents. One hard stop at task 7.**
Proposal: `docs/next/register-from-four-sources.md`, Track D.
Exploration: `exploration.md` in this unit — read §1 for the measured baseline of all 20 documents
and §2 for the four things the proposal got wrong.

## What is being built

Eighteen of the twenty documents are still at the register the campaign started from: mid-sentence
`, so ` at 6.3–14.6 % of sentences against 0.1–0.4 % in the four human sources, sentences opening
with a connective at 0.0–2.4 % against 3.7–6.1 %, and the balanced `, and ` second clause at
16.3–29.3 % against 1.1–3.4 %. Only `PCP-003` (round two) and `PCR-003` (round three) have been
re-authored.

This round re-authors **19** of them — every document except `PCR-003`, which is already at the
target register and is kept untouched as the control. Each is written by one agent in one pass from
the guide, the exemplar, the story bible and its own brief, and never from a sibling document.

## The order, and why it is that order

**1. Unify the rhetorical layer first (TASK-001).** Nine documents carry 315 rhetorical spans.
`PCR-003`'s 35 live in `authoring/rhetorical/PCR-003.spans.yaml` and are hard-gated. The other 280
are hard-coded in eight Python functions inside a 7600-line `build_ground_truth.py`, and those
functions emit every span unconditionally — a stale one is caught only later, by `check_grounding`,
as an ungrounded quote. Converting them to YAML is a **pure refactor whose proof is that all 20
annexes rebuild byte-identical**, and that proof only exists *before* any document changes. Doing
it after would mean converting and re-cutting at the same time, with nothing to check the
conversion against.

**2. Freeze the measurement as a script (TASK-002).** Twice now a number in a planning document
came from a session heredoc and could not be reproduced: round two's owner-reading counts, and the
proposal's Track C figure, which said 1.5 % and re-measured at 3.77 %. Every number this round
publishes comes from `measure_trackd.py` or from nowhere.

**3. A pilot of three, then a stop (TASK-003…007).** `PCP-007` (a plan), `PCR-005` (a DoE report
with 39 spans, so it exercises the converted YAML end to end) and `RA-001` (never re-authored, no
rhetorical layer, and the largest annex in the corpus at 317 quotes — the worst re-anchoring case,
which is better discovered at task 5 than at task 25). These are the same three the project owner
reads. The stopping rule is fixed in `state.json` before task 3 runs and no edge moves afterwards.

The pilot exists because of one risk. The proposal's own leading hypothesis is that the **guide**
is in the wrong register — `WRITING_GUIDE.md` commentary measures at 3.77 % `, so ` and 10.38 %
`, and ` + clause. If that turns out to be the blocker, every document authored from it needs doing
again. Three documents is a cheap way to find out; nineteen is not.

**4. The remaining 16 in five batches (TASK-008…028).** Batches follow the unit-operation prefixes
in `build_ground_truth.py`, so one annex task touches contiguous regions of that file: harvest +
viral inactivation, aex + virus filtration, UF/DF + the two orphan plans, then CEX/PTP/PCMP, then
`PCMR-001` alone and last, because the master report is the roll-up and carries the second-largest
annex in the corpus.

**5. Measure, then ship (TASK-029, TASK-030).**

## What can be run in parallel, and what cannot

- **Authoring is parallel-safe.** Each document is written into its own `<DOC>.DRAFT.qmd`; nothing
  is shared. The four document tasks inside a batch have identical dependencies and may run at the
  same time. Round two proved two concurrent authoring agents; more is untested, and Quarto keeps
  one `.quarto` cache per project, so raise it carefully.
- **Annex work is strictly serial.** `build_ground_truth.py` is one file. Two agents editing it
  concurrently lose each other's writes.
- **The corpus is green at every task boundary.** Drafts are authored under `.DRAFT.qmd`, so the
  committed corpus keeps grounding at 2084/2084 through every authoring task; only the batch's
  annex task promotes, and it closes before the next batch starts.

## What could go wrong

- **The guide is rewritten later and all 19 need doing again.** Mitigated by the pilot, not
  removed. Track C is still the proposal's leading hypothesis.
- **A registered discrepancy is silently lost.** Seven of the nineteen carry `D-001` — `PCP-003`,
  `PCP-006`, `PCP-008`, `PCP-009`, `PCR-006`, `PCR-008`, `PCR-009`. `TASKS.md` item 7: a
  re-authored document simply does not write it again, `DISCREPANCIES.md` goes on calling the item
  open, and no gate notices, because `check_grounding` inspects quotes and never a description
  field. Brief §5c is the carrier and the annex task re-verifies each one.
- **The passive is restated as a floor.** `PCP-005` (66.7 %), `PCP-008` (67.7 %) and `RA-001`
  (64.2 %) already sit at or above the top of the source range. For them the band is a **ceiling**.
  An instruction copied from round three without its band would push all three the wrong way.
- **A sibling `.qmd` is read for voice.** With 19 documents in flight this is the largest risk in
  the unit, and it is the loop that forced all 20 documents to be re-authored once already.
- **The two-extractor trap.** `check_grounding.docx_text` yields `R2` and
  `build_rhetorical_annex.doc_text` yields `R²` from the same file. Test every span under both
  before any builder runs.
- **Cost.** Round three's author took about 62 minutes and 577k tokens for a 56-page report.
  Nineteen documents is a large multiple of that however it is sequenced.

## What will not be attempted

- **`PCR-003` is not re-authored.** It is the control, and it is already at the newest rules.
- **Track C is not touched.** Rewriting the guide's own commentary is a separate argument and this
  round is the evidence that decides whether it is needed.
- **The rhetorical layer is not extended** to the eleven documents that carry none. TASK-001
  unifies the mechanism for the nine that have one; the extension is
  `docs/next/rhetorical-layer-coverage.md`.
- **No number moves.** Nothing in `config/parameters.yaml` changes and `git diff outputs/` is empty
  at ship.
- **No gate is added for the new measures.** Every one of them is met by typing or avoiding a word,
  and this campaign has watched a rule stated as a substitution overshoot three times out of three.
