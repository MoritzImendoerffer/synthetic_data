# Implementation plan — the author-facing apparatus, tested on one section first

**Proposal:** `docs/next/author-facing-apparatus.md` (the requirements; not restated here).
**Exploration:** `exploration.md` in this unit. **Task list:** `state.json`. **Written:** 2026-08-18.

## What is being built

A test, and then — only if it passes — a rebuild. The test is a one-section probe: the two
`PCR-005` Results subsections that all eight owner-quoted sentences come from, re-authored by the
same model class under a minimal regime (facts, canon, a one-page positive guide, the role of the
scientist who ran the study; no counters, no section-plan obligations, no 800-line guide), read
blind by the owner next to the shipped text. The proposal fixed the decision rule in advance:
PASS iff the owner prefers the probe and quotes fewer than three of its sentences.

If PASS, five instruments are rebuilt: the gate (tics gated, length signals for the reviewer only),
the section plan (obligations become a reviewer's checklist), the guide (short, positive, history
moved out), the brief (per-step mechanism prose, owner-read once), and a four-question content
review before promotion. If FAIL, the results page records the test and the proposal retires.

## The order, and why

```
TASK-001  measurement script (frames + span audit)      ─┐ independent; both useful either way
TASK-002  probe scaffold, guide, stripped brief, key     ─┘
TASK-003  author the probe (ONE agent, verbatim prompt)   needs 002
TASK-004  blind reading → D4                              HARD STOP; needs 003
TASK-005  counts + results page                           needs 001, 004
   ── D4 = PASS only ──
TASK-006  gate split                                      needs 004
TASK-007  obligations → reviewer checklist                needs 004
TASK-009  mechanism files (+ owner HALT)                  needs 004
TASK-008  short guide                                     needs 006 (tic list = GATED)
TASK-010  content questions, calibrated on excerpt+probe  needs 007, 005
   ── either way ──
TASK-011  prove the corpus is unchanged                   needs 005 (+ whatever ran)
TASK-012  documentation move, ship                        needs 011
```

**The script before the counts.** Results §9 admits the §3/§5.6 counts were session heredocs.
TASK-001 makes them reproducible *before* the probe is measured, so the probe's numbers and the
corpus baseline come from one committed script. Its acceptance is that it reproduces the results
page cell for cell (`, which` 9.82 (513), trailing relatives 11.39 (595), acts-through 1.21 (63)…).

**The scaffold before the author.** TASK-002 fixes every input the agent will see, and the blind
key, before the agent exists. Then TASK-003 is exactly one thing: launch the agent with
`procedures/TASK-003.md` verbatim. Nothing in that session may improve the prompt.

**The reading before the counts.** Same order as all four previous readings. TASK-003's outcome
records render, glyphs, `<<NEEDS>>`, sentence count and model, and *no* style number. TASK-004
records the owner's words verbatim, then resolves the key, then applies the rule. TASK-005 counts.

**The gate before the guide.** TASK-008's guide lists the gated tics, and the list must equal
`check_style.GATED`, which TASK-006 defines. TASK-006, TASK-007 and TASK-009 are independent of
each other and may run in any order or in parallel.

**Prove-unchanged before ship.** Nothing in this unit is upstream of a rendered document, so the
rebuild-and-reground task the workflow requires is sized to proving *identity*: 20/20 valid,
2084/2084 grounded, `git diff outputs/ ground_truth/ *.qmd` empty, `make test`, `make style`.

## What this plan decided that the proposal left open

All overrulable before the task that depends on them runs; each is in `state.json → decisions`.

- **Arm A only.** No exemplar arm. Two readings cost the owner twice; if A passes, one whole
  document under the rebuilt apparatus is the next check and the exemplar question rides on it.
- **SETUP from the shipped chunk.** `probe-setup.py` is lines 52–260 of the shipped `PCR-005`, code
  only. Holds the numbers constant between shipped and probe, and keeps the agent's effort on
  prose. `RUNNER.md` already allows code files.
- **PDF reading, standalone excerpt.** Both texts rendered under the same scaffold as `A.pdf` /
  `B.pdf`, so layout cannot tell them apart and the inline expressions resolve.
- **Blind key by `secrets.choice`**, written before delivery, opened after the reading.
- **The script is copied**, not imported from the predecessor unit, and must still pass
  `--check-baseline`.
- **`--review` lives in `check_style.py`**, not in `check_render.py`.
- **Guide history goes to `authoring/history/WRITING_GUIDE-2026-08-18.md`**, verbatim, one file.

## What is the owner's

**D4** (`docs/pm/decisions/D4-does-the-probe-pass.md`): the reading. The rule is fixed; the owner
supplies the reading. And inside TASK-009 the owner reads eight mechanism files once each; the
task does not complete until each carries a `reviewed by owner` date.

## What could go wrong

- **The agent writes numbers it has no helper for.** It is told to write `<<NEEDS:>>`. A typed
  number is recorded as a finding and left; prose is not edited (TASK-003 notes).
- **The probe is under 40 sentences.** The gate would not evaluate it (`MIN_SENTENCES`). The
  reading is still valid; the count is recorded and the agent is not re-invoked. The shipped
  excerpt is 59, so a probe of similar depth will clear it.
- **The owner recognises the shipped text.** Recorded as a limit in D4. The question is which
  reads as a paper.
- **A session "helps" the prompt.** `procedures/TASK-003.md` says verbatim, and `read_first`
  says why: the prompt is the variable under test.
- **TASK-006 accidentally goes red on a shipped document.** It cannot if `GATED ⊂ LIMITS` and no
  edge moves; the acceptance says 24 OK / 0 FAIL and the self-test still passes on all four
  sources. `paren`'s floor moves to advisory with the length rows.
- **TASK-007 orphans a name.** The plan greps `SCQA|CCC|rigor_glossary|bounded_conclusion|
  table_narration` across `authoring/ docs/ CLAUDE.md pc_package/TASKS.md pc_package/README.md`
  and lists every survivor; survivors are allowed only in records (results, history, decisions).
- **TASK-009 is prose with no source to ground it.** No numbers, so it cannot go stale on a
  reseed, but it can be wrong. The owner reads every file once; that is the HALT.
- **A hidden `outputs/` drift.** TASK-011's `git diff --stat outputs/` must be empty; nothing here
  runs `make data`.

## What will not be attempted

- No shipped document is re-authored, patched, or spliced. The probe stays untracked.
- No annex, span YAML, `config/`, `outputs/`, `nlp_reports` or `annex_contract` change.
- The 26-span `mechanistic_warrant` audit is counted (TASK-001) but not repaired; that is
  `docs/next/rhetorical-layer-coverage.md`'s.
- No band edge is moved. The length bands stop being gated; they are not widened.
- The fourth register round is not in this unit. On PASS it is the owner's next call, one
  document first.
