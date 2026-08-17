# Implementation plan — the second two-document round: give the author the number

Work unit `2026-08-17_01_register-second-round`. Nine tasks. Proposal:
[`docs/next/register-from-four-sources.md`](../../../docs/next/register-from-four-sources.md),
Track 1. Evidence: `exploration.md` beside this file; round one measured in
[`docs/results/2026-08-17-register-pilot.md`](../../../docs/results/2026-08-17-register-pilot.md).

## Picking this up cold

You were not here. Read, in order:

1. `docs/next/register-from-four-sources.md` — the requirements. Track 1 and its stopping rule.
2. `exploration.md` — the owner read the re-authored `PCR-003` and named a defect the pilot did
   not measure. §3 has the count; §9 has the three decisions the owner took.
3. `state.json` — the tasks. Every one carries `notes` with file locations and line numbers, the
   exact numbers an acceptance run must print, and the trap.
4. `clause_pack.py` in this unit — run it. It prints the table TASK-001 moves into the gate.

Everything runs under `uv`:

```bash
make test  PY="uv run python"          # 85 passed at the start of this unit
make style PY="uv run python"          # selftest 4/4, exemplar checker, then 20 .qmd files
uv run python authoring/check_render.py <doc>.qmd --render      # renders docx ONLY
cd pc_package && quarto render <doc>.qmd --to pdf               # the pdf, explicitly
cd pc_package && uv run python build_ground_truth.py \
  && uv run python validate_annex.py \
  && GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py
```

Baseline, 2026-08-17: **20/20 annexes valid, 2084/2084 quotes grounded** with strict anchors, 85
tests, `make style` 20/20. Any task that leaves those worse has not finished.

## How to execute a task

Every task has a step-by-step file in `procedures/TASK-00N.md` beside this plan: the code to
add (with the line it goes near), the commands to run, the exact output each must print, and the
point at which to stop. **Open it first and follow it top to bottom.** Six rules:

1. Read the whole procedure before touching a file.
2. Do the steps in order. Each names a command and what it must print. If it prints something
   else, stop and fix that step; do not go on to the next.
3. Never change an expected number to make a check pass. Every number in the procedures was
   measured on 2026-08-17; if yours differs, your code differs from `clause_pack.py` or from the
   notebook cell the procedure names.
4. Never edit a sentence in a committed `pc_package/*.qmd`. Documents are re-authored whole
   (TASK-005/006) or left alone.
5. At the end of every task: `make test`, `make style`, build + validate + strict grounding — all
   green (TASK-005/006 write DRAFTs, so the annex line is unchanged there by construction).
6. Write the task's `outcome` in `state.json` with the numbers the procedure asks for, set
   `status: completed`, run `uv run python scripts/pm_notes.py`.

If a procedure and `state.json` disagree, `state.json`'s acceptance list wins and the procedure
is corrected. If a procedure and the repository disagree (a line number moved, a function was
renamed), `grep -n` for the thing and continue; say so in `outcome`.

## What is being built

Round one amended the guide, the exemplar, the gate and the brief, re-authored `PCP-003` and
`PCR-003`, and got one clean win in five. Its diagnosis of why: **an author can execute and
self-verify a substitution and cannot self-verify a rate.** The connective repertoire moved because
`check_style.py` prints it back; topic chaining did not because nothing does.

Then the owner read `PCR-003` and quoted two sentences. The first packs a premise, a consequence
and a recommendation into one sentence with `, so … , and …`. The second counts "the four that
matter" without naming them. Measured over the same prose the gate reads, mid-sentence `, so `
runs at **6–11 % of corpus sentences against 0.1–0.4 % in all four sources**, sentence-initial
connectives at **0–2 % against 3.7–6.1 %**, and round one made both worse. The corpus reasons
inside the sentence; the sources reason across sentences.

So this round builds the feedback loop and tests it on the same two documents:

- **the number** — advisory packing counts in `check_style.py` (regex, printed on every render),
  and `check_discourse.py` for chaining / copula / front field (spaCy, optional extra, advisory);
- **the rule as a substitution** — the guide's "one sentence, one point" restated as *one
  argument step per sentence; the next step opens the next sentence with the connective*, its own
  ✓ example that teaches `, so` fixed, the referent rule, §2d bis's substitution named and banded,
  a positive Shape 4 example;
- **the brief's §5d** — the targets, the four source columns, and *this document's own current
  numbers*, so the author starts knowing where the last revision stood;
- **two one-pass re-authors**, one agent each, then promote, re-anchor, re-ground;
- **one measurement page** on three comparable points, one method, with the stopping rule applied
  and the owner's reading quoted.

## The order, and why

```
001 packing counts in check_style ──┬──> 002 guide: rule as substitution ──┐
                                    │                                       ├──> 005 re-author PCP-003 (DRAFT) ──┐
003 check_discourse + optional extra ┴──> 004 brief §5d (numbers + rules) ──┤                                     ├──> 007 promote, render, re-anchor, re-ground ──> 008 measure + owner reads ──> 009 ship
                                                                            └──> 006 re-author PCR-003 (DRAFT) ──┘
```

**001–004 leave the corpus untouched.** They change `authoring/`, `pyproject.toml`, `uv.lock` and
the Makefile; no document or annex moves, and every gate passes at each boundary. 001 comes
before 002 because the guide's §4a table quotes the measure names and per-source values 001
prints. 003 is independent and can run in parallel with 001/002. 004 needs both because it prints
what they measure.

**005 and 006 are separate tasks and separate agents.** Two documents in one task is a new
instance of the self-reference loop, not an exception to it. Both write DRAFTs, so the committed
baseline and all 2,084 quotes stay intact while the text is iterated.

**007 is the boundary that must close.** Until it completes the corpus is mid-change.

**008 measures, 009 delivers.** A measurement before the annexes re-anchor is a measurement of a
half-finished state, and the pilot has already documented one grounding count taken between two
states.

## Decisions taken by the project owner on 2026-08-17

| Question | Answer | What it changed |
|---|---|---|
| Does clause packing displace chaining as the target? | **Yes.** Chaining and copula are no-regression conditions | The stopping rule (below); TASK-008 applies it line by line; the proposal's 45 % chaining bar is not applied |
| Rewrite the guide's own commentary? | **Minimum now, full rewrite as a hypothesis** | TASK-002 changes the rule, the ✓ blocks that teach the fault, and adds examples; nothing else. If TASK-008 shows both documents still packing, the guide's own register is the next unit's first suspect |
| Who is the reader? | **The owner; the discrimination test is dropped** ("it is immediately obvious that the text is AI generated") | TASK-008 records the owner's reading verbatim and says it is not blind. No passage test |
| spaCy? (from the previous unit) | **Optional extra** | TASK-003; nothing in `make test/style/corpus` may need it |

## Decisions the plan had to take, which can be overruled

1. **Stopping-rule edges.** Mid-sentence `, so ` ≤ 1.0 % of sentences *and* sentence-initial
   connectives ≥ 3.0 %, in both documents (source bands 0.1–0.4 % and 3.7–6.1 %); topic chaining
   not more than 2.0 points below round one (30.7 % / 34.4 %) and copula not more than 2.0 points
   above (32.5 % / 27.6 %); the length bands still passing. Two points is the noise the pilot
   found between two runs of the same measure. If all hold, Track 2 opens.
2. **The brief generates no prose.** The proposal said `build_brief.py` "can generate worked
   chains from the document's own grounded facts". A template-generated chain is machine prose
   handed to the author, one level up from the sibling-`.qmd` loop `CLAUDE.md` forbids. §5d
   prints numbers and rules; worked corrections live in the guide.
3. **The measures stay advisory.** Printed like `CONNECTIVES`, in no `LIMITS` entry. A ceiling on
   `, so ` is met by writing `, and` or `;`, so the whole coordinator family and the
   sentence-initial rate are printed together and the semicolon ceiling stays.
4. **One method for all three points.** Rounds zero, one and two are measured by
   `check_style.py --compare` and `check_discourse.py` in one invocation each. The pilot's plan
   quoted "before" values that did not reproduce because two runs measured differently.
5. **The author is told the number this time.** Round one withheld it deliberately and only the
   substitution rules landed. This is the round's hypothesis, stated on the pilot page: *does
   giving the author the measurement change the outcome, when giving them examples did not?*
   The author is still not told to hit a chaining figure or to produce connectives to a count.
6. **The `15,000 L` line goes in the brief.** Round one's `PCR-003` never states the scale it
   characterizes; §1 of the brief now says to, via `V["commercial_scale_l"]`.

## What could go wrong

**The escape routes.** A ceiling on `, so ` is met by `, and`, `; `, `, which`, `so that`. TASK-001
counts the family and prints it; the semicolon ceiling (4.5 per 1k) already catches one route; a
rise in `, which` shows as relative clauses per sentence, which the earlier syntax analysis put at
parity (0.24–0.28) and TASK-008 can re-check.

**Splitting sentences pushes `pct_under_15` up.** Band 15–32 %; `PCR-003` round one at 22.7 %,
`PCP-003` at 20.4 %. One split in ten adds 5–8 points. Room exists; the author has to know the
ceiling. `pct_over_40` is near its floor (4.5 % vs 3.0), so the long tail must not flatten too.

**A floor on initial connectives is met by typing "Therefore,".** That is why nothing is gated
and why the guide keeps saying a produced connective is a worse tell than a missing one. TASK-008
should read the connective-led sentences, not only count them.

**The guide is read by the author that writes.** Its commentary models 0 % initial connectives and
`, so ` at 1.5–5.9 %; the exemplar's commentary 5.4 %; this proposal 11.5 %. TASK-002 fixes the
blocks that *teach* the fault; the rest stays, by owner decision, as the hypothesis for the next
unit if this round fails.

**The possessive rule's cost was measured; the packing rule's has not been.** Round one's
possessive rule bought its result in copulas. TASK-008 must count what the packing rule was paid
in — the most likely currencies are `pct_under_15`, `, and`, and copula.

**The owner is not a blind reader.** Accepted and stated. What the owner quotes is data either way:
if the pair still reads as machine-written, the quoted sentences are the next target.

**The spaCy version pins the parse.** `en_core_web_sm` 3.8.0 on spaCy 3.8; a different minor
changes chaining by a point or two, which is the size of the no-regression margin. TASK-003's
acceptance reproduces the pilot's numbers for exactly this reason.

## What will not be attempted

- **No gate.** Nothing new enters `LIMITS`; `check_discourse.py` is advisory and never on the
  `corpus`, `style` or `test` path.
- **No other document is re-authored.** Eighteen remain; Track 2 is TASK-008's verdict, not this
  plan's.
- **No number moves.** `config/parameters.yaml` and `outputs/` are untouched; TASK-007 asserts
  `git diff outputs/` is empty.
- **No weak claims.** `weak_claims` stays empty in all 20 annexes on `main`; the branch falls two
  re-authorings further behind, which `docs/next/weak-claims-branch.md` already prices.
- **D-001 and D-002 are not fixed.** Brief §5c carries them through the re-author; TASK-007
  re-verifies their sentences.
- **The guide's commentary is not re-authored.** Owner decision; hypothesis for later.
- **No sentence in a committed document is patched.** The two sentences the owner quoted become ✗
  examples in the guide (dated), and the documents are re-authored whole.
