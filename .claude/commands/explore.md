---
description: Open a work unit from a docs/next proposal, and read the repository before anything is planned
---

Open a work unit for one item from the backlog. This is the first of four commands:
`/explore` → `/plan` → `/next` → `/ship`. See [`docs/PROJECT_WORKFLOW.md`](../../docs/PROJECT_WORKFLOW.md).

**Input**: `$ARGUMENTS` names a proposal in `docs/next/`, with or without the path and the
`.md` suffix. `rhetorical-layer-coverage`, `docs/next/rhetorical-layer-coverage.md` and
`next/rhetorical-layer-coverage` all mean the same file. When it is empty, list the proposals
in the priority order `docs/ROADMAP.md` gives and stop.

## The rule that shapes this command

**The proposal is the requirements. Do not copy it.** `docs/next/<name>.md` already states what
would be built, what it would cost and how it would be checked. A `requirements.md` beside it
would be a second description of one task, and the two drift. The work unit **references** the
proposal by path and records only what the proposal does not: what the repository actually looks
like today.

If the target is not in `docs/next/`, stop and say so. Offer to write the proposal first —
`docs/next/README.md` gives the shape.

## Steps

1. **Resolve the target.** Find the proposal. If it does not exist, list what does and stop.

2. **Create the work unit** at `.claude/work/YYYY-MM-DD_NN_<slug>/`, and write the unit id into
   `.claude/work/ACTIVE_WORK`. The unit holds:

   | File | Holds |
   |---|---|
   | `metadata.json` | `proposal` (the path), `created_at`, `status`, `roadmap_priority` |
   | `exploration.md` | what the repository looks like now, written by this command |
   | `state.json` | the task list, written by `/plan` |

   `metadata.json` names the proposal instead of copying it. Anything a later session needs
   about *what* to build, it reads from the proposal.

3. **Mark the proposal as being worked on**, in the same sitting the unit opens. Two edits: the
   `**Status:**` line of `docs/next/<name>.md`, and that proposal's row in `docs/next/README.md`.
   Both say the unit id and the date.

   A reader outside this session looks at those two files, not at `.claude/work/`. Leave
   `docs/ROADMAP.md` alone here: it owns the *order*, and opening a unit does not change what
   should come next.

4. **Read the proposal, and check every claim in it against the repository.** A proposal can be
   older than the code, and this repository has form. Three "open" items were checked on
   2026-08-16 and two of them were already closed:

   - `pc_package/TASKS.md` said `nlp_reports`' `DOCUMENT_ID` pattern does not recognise
     `PTP/PCP/PCMP/PCMR/RA`. It builds the pattern from `settings.document_id_prefixes`, whose
     default list already contains all five, so there was nothing to do and nothing to change
     in a read-only repository.
   - `authoring/HANDOFF.md` said the PCR-003 rhetorical layer quotes superseded text and 34 of
     37 spans are dropped. `build_rhetorical_annex.py --doc PCR-003` writes 35 spans and drops
     none.

   Verify every claim of absence — "there is no X", "nothing builds Y" — by running the thing,
   not by reading about it. Record what is now wrong in `exploration.md` and say whether the
   proposal still stands.

5. **Explore what the work would touch.** Name the files, the helpers and the tests that already
   cover them. Prefer `Grep` and `Read` over guessing. Say which of the four layers the work is
   in, because each has a different rebuild cost:

   | Layer | Files | What a change forces |
   |---|---|---|
   | model | `config/parameters.yaml`, `amab_process/`, `scripts/` | `make data figures`, then every document and annex |
   | document | `pc_package/*.qmd` | a one-pass re-author, then re-render and re-anchor |
   | annex | `build_ground_truth.py`, `schema_ext.py` | rebuild, validate, re-ground |
   | machinery | `authoring/`, gates, `Makefile`, `scripts/` | whatever the gate reads |

6. **Check the ground rules that bite here**, and record which apply in `exploration.md`:

   - **Does a number change?** It lives in `config/parameters.yaml` and reaches the document
     through `outputs/`. A number typed into a `.qmd` is a bug. And the documents read the
     **generated CSV**, not `CFG` — commit `641d19a` assumed otherwise, skipped
     `make data figures`, and shipped a PCP-003 whose prose said "univariate" while its own
     Table 6 said `multivariate`.
   - **Does prose change?** The whole document is re-authored in one pass from the `authoring/`
     artifacts. Never patch a paragraph, and never read a sibling `.qmd` for voice: that
     feedback loop is what forced all 20 documents to be re-authored once already.
   - **Is a registered discrepancy in scope?** `authoring/DISCREPANCIES.md` holds D-001 and
     D-002 deliberately. Fixing one without removing its entry silently deletes a benchmark item.
   - **Is `pc_package/annex_contract/` or `nlp_reports` in scope?** Both are read-only. Extend
     `pc_package/schema_ext.py` and record it in `schema_extensions_used`.
   - **Do weak claims come up?** They exist only on `feature/weak-claims-via-brief`, which is
     rebased forward and never merged. On `main` `weak_claims` is empty in all 20 annexes.
   - **Does it change what a document claims?** Nothing is added to a document after authoring.
     The annex is built around the text; when grounding fails, the quote is re-anchored, never
     the document.

7. **Write `exploration.md`.** What exists, what the proposal got wrong, which files change, what
   could go wrong, and any question you could not answer from the repository. Short sentences,
   one idea each, concrete numbers.

8. **Report** the unit path, whether the proposal still stands, and any open question. Then
   recommend `/plan`.

## What this command does not do

It writes no code and renders nothing. The only files it changes outside `.claude/work/` are the
two status markers in step 3.

It does not decide priority. `docs/ROADMAP.md` owns the order, and picking an item out of that
order is the user's call, not this command's.
