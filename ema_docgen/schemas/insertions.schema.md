# Insertions file contract

`build/insertions/<DOC_ID>/<SECTION_ID>.yaml`

The only thing the agent produces that touches the document. Applied by
`scripts/splice.py` after `scripts/validate_insertions.py` passes.

---

## Shape

```yaml
doc_id: PCR-007
section_id: results_rsm_aggregate
insertions:
  - anchor: >-
      The response-surface models reproduce the established behaviour of
      cation-exchange polishing.
    insert_after: |
      First new paragraph.

      Second new paragraph.
```

Keys are exactly `doc_id`, `section_id`, `insertions`. Each insertion has
exactly `anchor` and `insert_after`. Any other key is a validation failure.

**There is no `replace`, `delete`, or `before` operation.** The absence is the
point: additivity is structural, not instructed.

---

## Anchor rules

| Rule | Enforced by |
|---|---|
| Occurs exactly once in the target | `validate_insertions.py` |
| Occurs at least once | `validate_insertions.py` |
| Not inside a fenced code block | `validate_insertions.py` |
| Contains no inline `` `{python} `` expression | `validate_insertions.py` (warning) |
| At least 40 characters | `validate_insertions.py` (warning) |

Matching is **whitespace-normalised**. The `.qmd` files are hard-wrapped at
about 85 characters, so a sentence anchor spans several source lines. Runs of
whitespace including newlines collapse to a single space on both sides before
matching, and offsets map back to the original text. Copy the sentence as it
reads; do not reflow it.

---

## Insertion semantics

`insert_after` is placed as a **new paragraph after the paragraph containing the
anchor** — not mid-paragraph, not immediately after the anchor sentence.

This keeps insertion points predictable and keeps existing paragraphs
byte-identical, which is what the grounding test relies on.

Multiple insertions in one file are applied in a single atomic pass, computed
against original offsets and written in reverse order so earlier offsets stay
valid. If any insertion fails, none are applied.

---

## New sections

Anchor on the last sentence of the preceding section and put the heading first:

```yaml
  - anchor: >-
      ... final sentence of the preceding section ...
    insert_after: |
      # Resin reuse and lifetime study

      Opening paragraph of the new section.
```

Heading level must match the docspec's intent for that section. `splice.py` does
not verify heading levels; `quarto render` and `lint_wordcount.py` will surface
mistakes.
