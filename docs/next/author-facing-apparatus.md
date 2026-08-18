# The author-facing apparatus is the cause: test it on one section before touching anything else

**Status:** proposed 2026-08-18, from the evaluation of
[`../results/2026-08-18-track-d-stopped.md`](../results/2026-08-18-track-d-stopped.md). Not
started. No work unit. **Task 1 is a probe and decides whether tasks 2–6 run at all.**

## The problem

Track D re-authored three documents with `claude-opus-5`. Every gated and printed measure was
inside its band, and the owner rejected the prose on eight quoted sentences (results page §1–§4).
The results page names five causes (§5). This proposal argues that four of them are one cause,
and that it is upstream of every round the campaign has run.

**The author is given a constraint-satisfaction task, not a writing task.** Measured on the bound
inputs the pilot launch prompt named
(`.claude/work/2026-08-18_02_register-track-d/procedures/AUTHOR-A-DOCUMENT.md` §3), word counts
by `wc -w`:

| bound input | words | what it is about |
|---|---|---|
| `authoring/WRITING_GUIDE.md` | 7,835 | sentence surface: 12 gated + 5 advisory + 5 parser measures, grep lists, 19 ✗ / 18 ✓ worked corrections, dated round history |
| `authoring/REGISTER_EXEMPLAR.md` | 10,389 | verbatim human passages, arranged by reporting move |
| `authoring/section_plan.yaml` | 5,849 | section order, plus per-section `scaffold`, `register` and `rigor` obligations to perform |
| `authoring/STORY_BIBLE.md` | 2,019 | world canon; Step 5 gets two lines of role |
| `authoring/out/PCR-005.brief.md` | 3,362 | data sheet, helper inventory, §5d discourse targets |
| **total** | **29,454** | against a 12,251-word document to write |

Of those 29,454 words, the ones about the physical chemistry of Protein A chromatography are the
A-Mab passages in the exemplar that describe what the step does. None explains why an effect has
the sign it has. The author is asked to write a `Mechanistic interpretation` section
(`section_plan.yaml:280`) and to "state directions + mechanism" (`:273`), and is scored on 22
counters. A capable model given an over-specified spec satisfies the spec. The right-hand column
of results page §4 was written by the same model class, the same day, with no gate and no guide.
The model is not the variable.

### Where the eight sentences come from, one by one

**The rhetorical taxonomy is upstream of authoring.** `authoring/RHETORICAL_ANNEX.md` states that
the span roles "are the concrete text-span realizations of the scaffolds (SCQA/CCC) and rigor
obligations that `section_plan.yaml` assigns each section." The annex layer itself is post hoc and
harmless. The same taxonomy, issued as per-section commands to the author, is not:

| quoted sentence (results §4) | obligation being performed |
|---|---|
| #4 "is put to no other use in this report" | `explicit_non_claim` |
| #5 "follow from the physical chemistry … and confirm the expectations recorded in §2.1" | "Establish the mechanistic expectation now so Results can confirm" (`section_plan.yaml:203`) |
| #2 "do not conflict, because a non-significant screening estimate makes no claim about the sign" | `screening_identifies_rsm_predicts` |
| #8 "behaves as a resin property … none of which is a parameter of a single run" | `null_result_is_informative` + "state mechanism" |
| #1, #3 "which is the curvature a two-level design cannot see" / "which is the interaction … already seen in Table 5.8" | "narrate the diagnostics", "note the significant interactions" |

An author told to perform a move writes a sentence whose function is the move. The owner's reading
names the result without naming the cause: "the sentence explaining itself: the finding is stated
and then … the reader is told how to file it." Filing is what a rigor checklist asks for. The annex
step then chose one of these sentences (`PCR-005-R17`) as the canonical `mechanistic_warrant`,
which is the loop closing.

**The `, which` clause is where the paragraph "Conclusion" went.** The CCC scaffold demands
`Context → Content → Conclusion (what it means)` per paragraph (`section_plan.yaml` meta.scaffolds).
`WRITING_GUIDE.md` §2c forbids the closing significance clause. Rounds one to three then banned
`, so`, `, and`+clause and `, not`. The "what it means" was demanded and had no carrier left, so it
moved into the sentence tail: `, which is the curvature …`. That is why `, which` rose 9.5 → 15.3 %
in the round that drove `, so` to zero. Three rounds document the same migration (`, so` → `, and`
→ `, not` → `, which`). Gating the carriers of a behaviour while keeping the instruction that
produces the behaviour moves the carrier.

**The gate is a target, and printing it to the author was the design.** "A measure printed back to
the author moves, and one that is not drifts" is recorded as the campaign's lesson three times. It
is a Goodhart set-up: the number moves and the writing does not. Results §5.1 shows the cost: the
paper-style rewrite fails `mean_len` (13.5 vs floor 20.0) and `pct_under_15` (55.6 vs ceiling
32.0). Those bands were read off whole chapters of guidance documents. A good results paragraph is
shorter and more committed than the average PDA sentence. The asymmetric tics — em-dash,
semicolon, colon, bold, coined compounds, the banned phrases, all at or near zero in the four
sources — catch the 34-word sprawl the gate was built for. The two-sided length bands catch
nothing a reader cares about and punish the sentences the reader asked for.

**The guide primes the fault.** 818 lines, by now largely a changelog: dates, "the project owner
named…", corpus percentages, and 19 machine-register sentences quoted verbatim as ✗. A model is
weak at "do not do X" and strong at continuing the register it was just shown. Results §6 already
concedes the guide's own commentary measures badly.

**Mechanism is demanded, and the published sources will not supply it.** Results §8.1 proposes
"a per-unit-operation mechanism section in the brief, written from the published sources".
Checked: A-Mab's Protein A section (`refs/text/amab.txt` ≈ 10380–10520) is a table of "Expect
higher HCP at low pH … potential interactions with load". It has no mass-transfer explanation
either. The right column of results §4 came from the model's own domain knowledge. The substance
is in the author already; the prompt regime gives it no slot except a checklist item and scores
only surface.

## What is not the problem

- **The model.** All three pilot documents were authored by `claude-opus-5` (`state.json`
  TASK-003/004/005 outcomes). The rewrites the owner accepted came from the same class.
- **The self-reference ban** (`RUNNER.md` preconditions). Correct; keep it. It is half a rule
  only because nothing positive was put in the other half.
- **The annex-as-annotation concept.** `rhetorical_spans` are curated after the text is final and
  change nothing in it. The fault is the taxonomy's second life as authoring instructions.
- **Grounding and inline `{python}` expressions.** They fragment a sentence around a number,
  which is a mild pressure toward templated framing ("is significant at X (p = Y), which is …"),
  not the fault. Golden rule 1 stands.
- **One document, one agent, one pass.** Correct; the probe below respects it by never splicing
  its output into a shipped document.
- **Track C as stated in `register-from-four-sources.md`** — that the guide's own register is
  the cause. Results §6 refuted the narrow form (`PCR-003` was authored from that guide and
  accepted). The wider form survives: the guide's *content* — negative examples, history, and
  counters — is one of the four instruments that together specify machine register.

## The idea

Stop encoding each failure as another rule the author must obey. Give the author facts, canon,
one short positive guide, and the role of the scientist who ran the study. Move every counter and
every completeness obligation to the **reviewer's** side, where a number is a signal and not a
target. Add a content-level judgment (does the `because` clause name a cause? is the term a term
of art? can each sentence be disagreed with on its own?) that no regex will ever make. Then, and
only if a one-section probe confirms it, rebuild the four instruments and run the fourth round.

## What it would take

Six tasks. **Task 1 gates the rest.** Layers touched: authoring machinery (`authoring/*.py`,
`authoring/*.md`, `section_plan.yaml`), the brief builder, `docs/`. No corpus document, no annex,
no `config`, no `outputs/` in tasks 1–5.

### Task 1 — the one-section probe (a day; decides everything)

Re-author the two subsections of `PCR-005` that all eight quoted sentences come from —
`Response-surface models` and `Mechanistic interpretation` under Results — under a minimal regime,
and put the result in front of the owner blind next to the shipped text.

**The regime, fixed before the agent is launched and recorded in the work unit:**

- Author: one agent, `claude-opus-5`, one pass. Same model as the pilot so the model is held
  constant.
- Inputs: `authoring/out/PCR-005.brief.md` **§1–§4b and §7 only** (facts and helpers; §5d
  discourse targets removed from the copy it reads), `authoring/STORY_BIBLE.md`, and a
  **new ten-line positive guide** written for the probe (`$W/probe-guide.md`): who the reader is,
  numbers through inline expressions only, no em-dash / semicolon / bold / coined compounds, the
  four gated tics, and one role sentence — "you are the process scientist who ran this study;
  explain the surfaces as you would in a paper". Nothing else. **No `WRITING_GUIDE.md`, no
  `section_plan.yaml`, no `REGISTER_EXEMPLAR.md`, no counters printed back, no `check_render`
  loop.** The agent writes once and stops.
- Optional arm B, same regime plus `REGISTER_EXEMPLAR.md`, if the owner wants to know whether the
  exemplar helps or hurts. Two arms at most.
- Vehicle: `pc_package/PCR-005_protein_a.PROBE.qmd`, instantiated from `authoring/template.qmd`,
  carrying the SETUP chunk and only the two subsections, rendered to PDF standalone. Untracked; it
  is a probe, not a document. **The output is never spliced into `PCR-005`** (one document, one
  agent), and no annex is touched.
- The reading: the owner receives the shipped subsections and the probe subsections as A and B
  (which is which is decided by the session and recorded before delivery, not told), and is asked
  the questions the four previous readings answered in effect: quote the sentences that read as
  machine prose; say which reads as a paper. **Recorded verbatim, before any count.**
- Then the counts, afterwards and in that order: `measure_trackd.py` on both texts, plus the
  trailing-relative, `acts through`, `follows from`, `governs / sets`, and hollow-warrant frame
  counts, and the current gate's `mean_len` / `pct_under_15` on the probe. Results §9 records that
  those five counts are not yet in `measure_trackd.py`; **putting them there is part of this task**.
  A number in a results page comes from a committed script, never from a session heredoc.

**Decision rule, fixed now.** Arm A is judged the better text by the owner **and** the owner quotes
fewer than three sentences from it (the shipped text drew eight) → the apparatus is the cause and
tasks 2–6 run. Otherwise this proposal is retired, results §8 stands as the plan, and the record
says so. The probe is expected to **fail** the current gate on `mean_len` and `pct_under_15`; that
outcome, together with an accepting reading, is the evidence for task 2 and is not a reason to
revise the probe.

### Task 2 — split the gate into tics and signals (small)

`check_style.py`: `LIMITS` becomes `GATED` (em-dash, semicolon, colon, bold, coined compounds,
`rather than`, the `BANNED` list) and `ADVISORY` (all five length rows, `paren`, and the existing
clause-packing family). `--selftest` must still pass on all four sources for both sets.
`check_render.py` fails only on `GATED` and prints **nothing else to the author**; a new
`check_style.py --review <qmd>` prints the full table, with source columns, for the reviewer.
This retires the "print it back to the author" doctrine deliberately, and the CLAUDE.md Voice
rule is edited to say why: a measure printed to the author moves the number; the reviewer is who
should read it.

### Task 3 — take the obligations off the author and give them to the reviewer (medium)

`section_plan.yaml`: keep section order, headings, `pull:` menus and one plain sentence per section
on what it covers. Remove `scaffold`, `register` and `rigor` from the author-facing plan; remove
the `scaffolds` / `registers` / `rigor_glossary` blocks or move them to a new
`authoring/REVIEW_CHECKLIST.md` **rephrased as questions a reviewer asks of a finished section**
("Does the design-space claim say which ranges it covers and what the model does not cover?"),
never as moves to perform. `RHETORICAL_ANNEX.md`: replace the sentence tying roles to rigor
obligations with the opposite rule — roles are annotated on finished text and are never authoring
instructions — and add a content criterion for `mechanistic_warrant` (must name a physical cause; a
category label is not a warrant). The 26-span audit itself stays in
[`rhetorical-layer-coverage.md`](rhetorical-layer-coverage.md), which already owns it.

### Task 4 — a short positive guide (medium)

Replace `WRITING_GUIDE.md` with a guide of about 150 lines: the reader, the numbers rule, ten
rules stated positively, ✓ passages only, and the four gated tics. **No ✗ examples, no
percentages, no round history, no dates.** The corrections and history move to
`docs/results/` (most are already there) or to `authoring/history/`, and `git` keeps the rest.
`REGISTER_EXEMPLAR.md` is kept; whether it is trimmed depends on arm B of the probe.
`CLAUDE.md` Voice rule and `RUNNER.md` step 3 are updated to the new file list.

### Task 5 — supply the mechanism (medium; the owner reads it once)

`authoring/mechanism/<uokey>.yaml`, one file per unit operation: for each governed CQA and each
studied parameter, two to four sentences of physical chemistry with the terms of art, **carrying
no numbers** (so a reseed cannot stale it and golden rule 1 is untouched). Written from domain
knowledge, not from `refs/text/` (checked: the sources do not carry it), and read once by the
owner per step before use. `build_brief.py` emits it as brief §2b. This is the "supply the
mechanism" item of results §8.1, with its source corrected.

### Task 6 — a content review before promotion (small to write, run per document)

`authoring/REVIEW_CHECKLIST.md` (task 3) gains four content questions, and the annex procedure
(`ANNEX-A-BATCH.md` or its successor) runs them **before** a draft is promoted, by an LLM judge
that has read neither the guide nor the counters, or by the owner: (1) does every `because`,
`since` and "governs / sets" name a physical cause? (2) is every technical term a term of art in
chromatography / cell culture literature? (3) can each sentence in a mechanism paragraph be
disagreed with on its own? (4) does any sentence tell the reader how to file the finding it just
stated? The judge's answers are recorded in the work unit; a "no" blocks promotion.

**Then**, out of scope here and the owner's call: the fourth round, one document first, on the
rebuilt apparatus.

## Verification

- **Task 1:** the owner's verbatim reading in `$W/owner-reading-<date>.md`, written before any
  count; then `measure_trackd.py` extended with the five counts, run on shipped and probe text,
  reproducing the results-page corpus baseline cell for cell (`--check-baseline` on all 20 must
  still agree). The decision rule above applied and recorded in `state.json`.
- **Task 2:** `check_style.py --selftest` passes on all four sources for `GATED` and reports the
  `ADVISORY` table; `check_render.py` on the 20 shipped documents fails none of them on `GATED`
  (the corpus is at 24 OK / 0 FAIL today and must stay there); the probe text from task 1 passes
  `GATED` and shows its length rows only under `--review`.
- **Task 3:** `grep -c "rigor:\|scaffold:\|register:" authoring/section_plan.yaml` → 0;
  `build_brief.py` on all 20 documents still runs; `make test` unchanged.
- **Task 4:** `wc -l authoring/WRITING_GUIDE.md` ≤ 200; `grep -c "✗" ` → 0; `check_style.py`
  on the guide's own commentary now passes `GATED`.
- **Task 5:** eight `authoring/mechanism/*.yaml`, `grep -cE "[0-9]"` on their prose → 0 (no
  numbers), the owner's sign-off per file noted in the work unit; `build_brief.py PCR-005` shows
  §2b.
- **Task 6:** the four questions answered and recorded for the probe text and for the shipped
  `PCR-005` Results section; the shipped section is expected to fail (4) on the sentences the owner
  quoted, which is the check that the questions see what the reading saw.
- **At the end:** `20/20 annexes valid`, `2084/2084 quotes grounded`, `git diff outputs/` empty,
  `make test` and `make style` green — nothing in tasks 1–6 touches a shipped document, so nothing
  in the corpus may change.

## What this deliberately does not do

- It does not re-author any of the 19 documents. That is the fourth round, and it waits on task 1.
- It does not promote the probe text into `PCR-005`, in whole or in part.
- It does not touch `pc_package/build_ground_truth.py`, any annex, or the span YAML files. The
  26-span audit stays in `rhetorical-layer-coverage.md`.
- It does not remove the self-reference ban, the grounding rules, or the one-agent invariant.
- It does not decide whether an LLM judge is a sufficient reviewer. Task 6 offers the owner as the
  alternative on every run.
- It does not fix `mean_len` / `pct_under_15` by moving their edges. It stops gating them.

## Open questions

- Should `REGISTER_EXEMPLAR.md` stay in the author's inputs at all? Arm B of the probe answers it
  if the owner wants two readings; otherwise it stays and task 4 leaves it alone.
- Is a section-sized probe enough evidence to rebuild four instruments? It is enough to falsify the
  hypothesis cheaply, which is what it is for. If arm A reads well, one whole document under the
  rebuilt apparatus is the next check before nineteen.
- Where does the mechanism prose live so it stays single-sourced and reviewable —
  `authoring/mechanism/*.yaml` as proposed, or a `mechanism:` block per unit operation in
  `config/parameters.yaml`? The config is numbers and the mechanism must carry none, which is the
  argument for keeping them apart.
- Task 6's judge must not have read the counters or the guide, or it inherits the blind spot
  results §5.6 describes. Whether a fresh-context agent with only the checklist and the two texts
  is "fresh enough" is a question for its first run.
