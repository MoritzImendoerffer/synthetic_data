# Section authoring task

> **SUPERSEDED.** Part of the retired two-pass densification workflow — see
> [`README.md`](README.md). Authoring is now one pass, one agent, one context:
> [`../authoring/RUNNER.md`](../authoring/RUNNER.md). Kept as history.

Executed once per section, in a fresh subagent. Placeholders in `<ANGLE
BRACKETS>` are bound by the runner from the docspec.

---

## Read first

```
ema_docgen/AUTHORING.md                        # constraints + move taxonomy, in full
pc_package/<SOURCE_QMD>                        # the current document
pc_package/PCR-008_aex.qmd                     # reference implementation
ema_docgen/docspec/<DOC_ID>.yaml               # section <SECTION_ID> only
ema_docgen/factpack/<DOC_ID>/<SECTION_ID>.yaml # the facts you may use
pc_package/HELPER_API.md                       # available inline expressions
build/ledger/<DOC_ID>.md                       # what earlier sections established
```

If `HELPER_API.md` does not exist, derive the available names from
`pc_package/_pcpkg.py` and `pc_package/doe_report.py` and note that in the
self-check.

PCR-008 is the standard this document is being brought to. Read how it handles
the same heading before writing. Match its density and its register; do not copy
its sentences.

---

## Write

```
build/insertions/<DOC_ID>/<SECTION_ID>.yaml
build/review/<DOC_ID>/<SECTION_ID>.questions.md
build/review/<DOC_ID>/<SECTION_ID>.selfcheck.md
```

Nothing else. **Do not modify any file under `pc_package/`.**

---

## Step 1 — Reviewer anticipation

Before drafting, list 6–10 questions an EMA assessor would raise about this
section. Specific ones — about this parameter, this range, this exclusion — not
generic ones about validation or GMP.

Write them to `<SECTION_ID>.questions.md`. Then answer each pre-emptively in the
prose you draft. Do not put the question list in the insertions.

This step reproduces the mechanism that makes regulatory documents long. If your
questions are generic, the section will be too.

---

## Step 2 — Draft

Section: `<SECTION_ID>` — `<SECTION_HEADING>`
Register: `<REGISTER>` (see AUTHORING.md Part 2)
Required moves: `<REQUIRED_MOVES>`
Forbidden moves: `<FORBIDDEN_MOVES>`

Every required move must appear. Forbidden moves must not. Beyond those, use
whatever the section needs.

Apply all constraints in AUTHORING.md Part 1 — numerals, facts, deferral,
additivity, voice, lexical independence.

**Restatement.** Restate at least one claim the ledger records from another
section, worded differently. Do not contradict it. If the ledger records nothing
suitable, say so in the self-check rather than inventing a claim to restate.

**Length.** Do not count words or aim at a target. Write what the obligations
require and stop.

---

## Step 3 — Emit insertions

```yaml
doc_id: <DOC_ID>
section_id: <SECTION_ID>
insertions:
  - anchor: >-
      the complete existing sentence, copied character for character from the
      document, long enough to be unique
    insert_after: |
      New paragraph. May be several paragraphs separated by blank lines.
```

Rules:

- `anchor` is copied verbatim from existing prose. Line wrapping is normalised
  on matching, so wrapped sentences are fine; do not reflow or edit them.
- `anchor` must occur exactly once. Short generic sentences will collide —
  choose a longer one.
- `anchor` must not sit inside a fenced code block.
- `anchor` should not contain an inline `` `{python} `` expression.
- Insertion places a new paragraph **after the paragraph containing the anchor**.
- No other keys. There is no mechanism to replace or delete text, by design.

For a wholly new section, anchor on the last sentence of the preceding section
and include the heading as the first line of `insert_after`.

---

## Step 4 — Self-check

Write `<SECTION_ID>.selfcheck.md`:

```markdown
## Moves
- <move>: satisfied | NOT SATISFIED — reason

## Constraints
- numerals: all inline expressions / N bare numerals remain — list them
- facts: all from fact pack / used facts not in pack — list them
- deferral: all deferrals name a location / N do not — list them
- restatement: restated "<claim>" from <section> | none available

## NEEDS
- <<NEEDS: ...>> — one line each, with what it is for

## Anchors
- <n> insertions, each anchor verified unique by inspection
```

Report failures plainly. A section with three unmet obligations reported is
useful; one that claims success falsely is not. Unmet obligations usually mean
the fact pack is thin — that is information, not a failure on your part.
