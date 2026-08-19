# Implementation plan — the fourth round: one whole document under the rebuilt apparatus

**Proposal:** `docs/next/register-from-four-sources.md`, its last paragraph. **Exploration:**
`exploration.md`. **Task list:** `state.json`. **Written:** 2026-08-19.

## What is being built

One document — `PCR-007`, the CEX report, unless the owner overrules (D5) — authored in one pass by
one agent under `authoring/RUNNER.md` **as rebuilt on 2026-08-19**: brief with the step's
mechanism, section plan as structure, story bible, the 122-line guide, the exemplar; no counter, no
obligation. The draft goes through the content review once, then the owner reads it blind against
the shipped `PCR-007` under a pass rule fixed now. On PASS it is promoted: rendered, its 33 spans
re-cut, its 88 annex quotes re-anchored, the corpus re-grounded. Then a results page.

The probe answered "was the apparatus the cause?" on two subsections. This answers "does a whole
document under the rebuilt apparatus read as a paper?", which is the question the proposal leaves
open before nineteen more.

## The order, and why

```
TASK-001  prompt, key, brief, scaffold, reading protocol   (fix everything before the agent exists)
TASK-002  author, ONE agent, RUNNER inputs only            (the regime under test)
TASK-003  content review, ONE return cycle                 (the pipeline's own step)
TASK-004  blind reading → D6                               HARD STOP
TASK-005  counts + results page                            (whichever way D6 fell)
   ── D6 = PASS only ──
TASK-006  promote, render, re-cut spans, re-anchor, re-ground
TASK-007  rebuild-and-reground proof
   ── either way ──
TASK-008  ship
```

**Everything the agent sees is fixed before it exists** (TASK-001), including the blind key. The
prompt is the RUNNER's own invocation line — the RUNNER as rebuilt is what is being tested, so a
rule added to the prompt would be a finding disguised as a fix.

**The content review runs before the reading, once.** The proposal's task 6 put a content review
before promotion; the reading judges the pipeline's output, so the pipeline runs. One cycle only:
the calibration showed the judge is stricter than the owner and consistent, and a second cycle
would tune the draft to the judge. The run-1 draft is kept so the page can say what one cycle did.

**The reading before the counts**, as in every round. TASK-002 and TASK-003 record no style number.

**Promotion only on PASS.** A reading with nothing shipped leaves the corpus where it was; the
proposal says "before nineteen", i.e. ship one, then decide.

## What this plan decided (overrulable, each in `state.json → decisions`)

- **`PCR-007`.** Full DoE report, no discrepancy, never read by the owner (so shipped vs new is a
  genuine blind read), mid-sized annex. Owner's decision D5; assumed until overruled.
- **The exemplar is in.** The probe left it out; the guide's §5 sends the author to five of its
  sections. That is one of the two ways this regime differs from the probe's; the other is the
  agent writing its own SETUP chunk. Both are the RUNNER's normal case.
- **What the owner reads.** Two whole PDFs blind; a fixed subset (Executive summary; Results;
  Design space; Discussion) is suggested, the whole available.
- **Pass rule.** New preferred AND fewer than five sentences quoted from it across what was read.
- **One content-review cycle**, before the reading.

## What is the owner's

**D5** — which document (assumed `PCR-007`). **D6** — the reading, under the fixed rule. Whether
the campaign then continues to the remaining documents is a new `/explore`, not this unit.

## What could go wrong

- **The agent needs a helper that does not exist.** It writes `<<NEEDS:>>`; the helper is added
  to `_pcpkg.py`/`doe_report.py`, the brief rebuilt, the SAME agent re-invoked with the name.
  Never a typed number, never a fresh agent mid-document.
- **The whole-document arc fails where two subsections could not** — a summary that does not match
  the conclusions, dangling cross-references. That is exactly what the reading is for; the content
  review's questions do not test arc, and TASK-005's "what was found" section records it.
- **The read is long.** Two 50-page reports. The subset keeps it to roughly what the previous
  readings covered; the whole is there if wanted.
- **Re-anchoring.** 88 quotes and 33 spans; the `R2`/`R²` extractor trap; the report-summary
  statements that have to be read, not grepped. `ANNEX-A-BATCH.md` is the tested loop.
- **`make style` glob.** A DRAFT under `pc_package/` is measured by `make style`; it must read OK
  on the tics (it will, if `check_render` passed) and it is counted as a 25th document until
  promoted or removed.

## What will not be attempted

- No `make data figures`; `outputs/` stays identical.
- No other document is touched, and no rendered pair but `PCR-007`'s is committed.
- No new gate, no new counter, no rule added to the author's inputs.
- No decision about the remaining eighteen; that is the owner's after the page is written.
