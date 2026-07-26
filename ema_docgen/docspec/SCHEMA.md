# Docspec schema

One file per document: `ema_docgen/docspec/<DOC_ID>.yaml`.

This is the artifact you curate. The agent decides nothing that lives here.

**All twenty are pre-populated.** Headings are read from the real `.qmd` files;
targets are derived from the corpus, not chosen (see the header comment in each
file). `_TEMPLATE.yaml` is the blank form for a document that does not exist
yet.

---

## Top level

| Field | Required | Meaning |
|---|---|---|
| `doc_id` | yes | e.g. `PCR-007` |
| `source_qmd` | yes | filename under `pc_package/` |
| `version` | yes | integer; bump on any edit, recorded in state |
| `sections` | yes | list, in document order |

---

## Section

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | snake_case, unique, used for all build paths |
| `heading` | yes | the heading text; existing or new |
| `new_section` | no | `true` if the heading does not yet exist. Default `false` |
| `tier` | yes | `1` establishing, `2` analytical, `3` synthesising |
| `register` | yes | one of AUTHORING.md Part 2 |
| `target_words` | yes | lint tolerance band only — never shown to the agent |
| `tolerance` | no | fractional band, default `0.25` |
| `required_moves` | yes | list of move names from AUTHORING.md Part 3 |
| `forbidden_moves` | no | list; prevents register drift |
| `factpack` | no | path override; defaults to `factpack/<DOC_ID>/<id>.yaml` |
| `notes` | no | free text passed to the agent verbatim |

---

## Notes on the fields that matter

**`target_words`** is deliberately withheld from the agent. It exists so
`lint_wordcount.py` can flag sections that came out wildly off, which usually
means the fact pack was thin. Telling the agent a number produces padding.

Spread targets aggressively — 150 to 3,000. Uniform section length is the
clearest signature of a synthetic corpus.

**`tier`** is a hard sequencing constraint, not a preference. Tier 1 sections
create the deviation IDs, lot numbers and equipment references that tiers 2 and
3 cite.

**`forbidden_moves`** matters as much as required. Without it every section
drifts defensive.

**`new_section: true`** changes anchoring: the agent anchors on the last
sentence of the preceding section and emits the heading as the first line of
`insert_after`.

---

## Deliberately absent

There is no `register_anchor` field pointing at passages in `refs/text/`. See
DESIGN.md R1 — exemplars drawn from source literature leak phrasing into the
corpus and contaminate the benchmark. Register comes from AUTHORING.md.
