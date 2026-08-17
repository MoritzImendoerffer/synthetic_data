# Implementation plan — make the corpus argue, then test it on one document

Work unit `2026-08-16_01_register-from-four-sources`. Ten tasks. Proposal:
[`docs/next/register-from-four-sources.md`](../../../docs/next/register-from-four-sources.md);
evidence in `exploration.md`, `syntax-analysis.md`, `rhetoric-comparison.md`,
`mined-patterns.md` and `register_analysis.ipynb`.

## Picking this up cold

You were not here when this was planned, and you do not need to have been. Read, in order:

1. `docs/next/register-from-four-sources.md` — the requirements. Do not re-derive them.
2. `exploration.md` beside this file — what the repository looks like now, and the two corrections
   exploration made to the proposal.
3. `state.json` — the tasks. Every one carries a `notes` field with file locations, the exact
   strings to add, the expected numbers and the trap that task has.
4. `mined-patterns.md` — TASK-004 is largely a transcription of this file.

Everything runs under `uv`. The scientific stack is not in the system python:

```bash
make test  PY="uv run python"          # expect: 85 passed
make style PY="uv run python"          # selftest, exemplar checker, then every .qmd
uv run python authoring/check_render.py <doc>.qmd --render
cd pc_package && uv run python build_ground_truth.py \
  && uv run python validate_annex.py \
  && GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py
```

**`PY=` is not enough for a full build.** Quarto starts its own Jupyter kernel and resolves
`python3` from `PATH`, so use `PATH="$PWD/.venv/bin:$PATH" make corpus PY="uv run python"`.

Baseline on 2026-08-16, from an unmodified checkout: **20/20 annexes valid, 2084/2084 quotes
grounded** with strict anchors, 85 tests, clean tree. Any task that leaves those worse has not
finished.

## What is being built

Not a gate. The corpus already passes thirteen register thresholds and still does not read like
SME prose, so the work is to **give the author the shapes that carry an argument and remove the
rules that forbid them**, then re-author one document and find out whether it worked.

Four artifacts change: the writing guide, the register exemplar, the source extraction, and the
brief. One document is re-authored. Nothing else in the corpus is touched.

## The order, and why

```
001 extract four sources ──┐
                           ├──> 002 recalibrate the gate ──┐
003 amend §2c/§2d ─────────┼──> 004 moves catalogue ───────┤
                           └──> 005 exemplify given-new ───┼──> 007 re-author PCP-003 (DRAFT)
006 discrepancies in brief ────────────────────────────────┘        │
                                                                    ▼
                                          008 promote + re-anchor ──> 009 measure ──> 010 deliver
```

**001 to 006 are independent of the corpus.** Every one of them leaves the repository green:
they touch `authoring/`, `scripts/` and `refs/`, and no document or annex changes. The gates
(`make test`, `make style`, build/validate/ground) pass at every boundary.

**007 writes a DRAFT.** `pc_package/PCP-003_bioreactor.DRAFT.qmd` has an untracked `.docx`, so
the committed baseline of 21 rendered documents and all 2,084 annex quotes stay intact while the
new text is iterated. This is the only reason the repository can stay green across a re-author.

**008 is the boundary that must close.** It promotes the draft, re-renders, re-anchors the annex
and re-grounds. Until it completes, the corpus is mid-change; after it, everything is green again.

**009 measures, 010 delivers.** Neither may run early: a measurement taken before the annex
re-anchors is a measurement of a half-finished state.

## Decisions taken by the project owner on 2026-08-16

| Question | Answer | What it changed |
|---|---|---|
| May ISPE passages be quoted into the exemplar? | **Yes** — A-Mab, PDA TR 60 and both ISPE guides | TASK-001 extracts all four and commits the text; TASK-004 draws plan-genre examples from ISPE Technology Transfer, which is the only plan-shaped source and the largest single lever, since 10 of 20 documents are plans |
| D-002 would be erased by a re-author | **Port the brief's discrepancy section** | TASK-006 exists, and every document becomes safe to re-author rather than only the pilot |
| How far should the plan reach? | **Through the pilot, then re-decide** | Ten tasks, one re-authored document. The remaining nineteen are not planned |

**The ISPE decision has a consequence worth stating once.** `refs/text/*.txt` is committed, and
`check_style.py --selftest` reads it. Extracting the ISPE guides therefore puts about 1 MB of text
from two documents watermarked "for personal use only" into the repository. The concern was raised
before the decision; the decision is the owner's and the plan follows it.

## Decisions the plan had to take, which can be overruled

1. **No floors for semicolons, colons or long sentences.** The corpus sits at zero on all three
   against human rates of 1.1 to 3.3, and that is a real gap. It is left alone because those are
   ornament: an author told to produce semicolons produces semicolons, and the metric would improve
   while the prose did not. If you want them, they are a one-line change to `LIMITS`.
2. **The `therefore` cap is removed rather than kept and paired.** Capping the only connective in
   service while eight sit at zero is backwards. The alternative — keep the cap and add the other
   eight to the guide's prose only — is available and does less.
3. **PCP-003 is the pilot, not PCR-003.** It is the worst modality case (`will` at 19.7 per 1000
   words against a human 2.0 to 3.3, `should` and `may` at zero) and it is a plan, which is the
   genre with no exemplar. PCR-003 is the more visible document, but re-authoring it depends on
   TASK-006 landing correctly and it is 10,354 words against PCP-003's 4,719.
4. **The measurement is not given to the author.** TASK-007 does not tell the author to raise topic
   chaining or produce connectives. TASK-009 measures afterwards. This is deliberate and it is the
   single most important line in the plan.

## What could go wrong

**The exception in §2c is read as a licence to sprawl.** The first-pass corpus ran a 34-word mean
with an em-dash aside in every third sentence, and that is what §2c was written to stop. TASK-003's
acceptance requires the amendment to state the opposite failure explicitly. If the pilot comes back
long, the exception is too wide and TASK-003 is wrong, not the author.

**Relaxing two ceilings admits the old prose.** TASK-002 moves `mean_len` to about 28.5 and
`pct_over_40` to about 19 because a published ISPE guide fails today's values. That is closer to
the 34-word first-pass than the current band is. The two-sided bands and the banned-phrase list
still apply, but this is the change most likely to need reverting.

**The mined quotes may not survive the checker.** One of 25 already failed because it spans a page
break that `prose_from_extract` joins across the running header. TASK-004's acceptance runs
`check_exemplar_quotes.py` rather than trusting the mining.

**The ISPE filters are per-source and hand-written.** Get them wrong and the recalibration in
TASK-002 is built on garbage: unfiltered, ISPE TT reads 41.2 % of sentences under 15 words against
a band of 15 to 32, because 300 of 470 short sentences are the same four watermark lines. TASK-001
states the expected post-filter figure so the task can be checked rather than assumed.

**The pilot may show no improvement.** That is a real outcome and TASK-009 must report it. It
would mean the discourse hypothesis is wrong or the guide amendment was too timid, and it stops the
campaign before nineteen more documents are re-authored.

## What will not be attempted

- **No syntactic gate.** spaCy stays out of `pyproject.toml`. The parse findings are diagnostic,
  the notebook runs through `uv run --with spacy`, and nothing in `make corpus` depends on it.
- **No other document is re-authored.** Nineteen remain, and the decision about them is TASK-009's
  output, not this plan's.
- **No number moves.** `config/parameters.yaml` and `outputs/` are untouched; TASK-008 asserts
  `git diff outputs/` is empty.
- **No weak claims.** TASK-006 ports the discrepancy mechanism without the weak-claims half, and
  `weak_claims` stays empty in all 20 annexes on `main`.
- **D-001 and D-002 are not fixed.** They are registered benchmark items. TASK-006 makes them
  survive a re-author, which is the opposite of fixing them.
