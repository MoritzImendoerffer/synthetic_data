# Spec: graded question–answer set from the corpus (owner, 2026-10-11)

**Purpose.** A test set for the owner's doctool repository (`/home/moritz/github_repos/doctool`, the `dw` tool).
`dw` parses documents into HTML in which every element has a stable id. Every statement it produces cites an element
and a verbatim quote. The set scores two things: a retrieval pipeline (does it find the right passage in the right
document, and is the answer right), and a summarization run such as a PCMR (does it cover the key points, with
correct citations). PCMR-001 is deferred, so the summarization items stand in for it.

**Owner's choices.**
- Mostly generated. A script builds most pairs from the CSVs and annexes, and a small curated set covers the hard
  multi-document and summarization items. The same script checks the curated items.
- Levels L1–L4, plus summarization tasks, plus unanswerable questions.
- No version traps.
- Save tokens.

## Deliverables
- `pc_package/build_qa.py`. Run from `pc_package/`, it writes `pc_package/qa/qa_set.jsonl` and
  `pc_package/qa/qa_set.md`, a readable listing grouped by level.
- `pc_package/qa/curated.yaml`, the hand-written items, checked by the script.
- `pc_package/qa/README.md`. It gives the schema, the levels, how to score, and how to regenerate.
- A `make qa` target, with the same `PY=` convention as the other targets.
- A test in `tests/` that builds the set and asserts:
  - every evidence quote grounds;
  - ids are unique;
  - every level has at least its minimum count.

## Corpus scope
- Only the Version 2.0 documents in `build_ground_truth.REV2_READY`, read from their rendered `.docx`.
- Quotes are checked against the rendered text in the same way `check_grounding.py` does it: the same text
  extraction, whitespace collapse, and table cells joined with `" | "`. Reuse its functions, do not copy them.
- The superseded Version 1.0 files are not evidence.
- PCR-007 and PCR-008 join when they are promoted. The script reads REV2_READY, so it picks them up on rebuild.

## Item schema (one JSON object per line)

| Field | Content |
|---|---|
| `id` | Stable, e.g. `L1-param-nor-PCR-005-load`, from the template and its keys, never a counter |
| `level` | `L1`, `L2`, `L3`, `L4`, `SUM` or `NONE` |
| `template` | The generator or `curated` |
| `question` | Plain English, as a process scientist would ask it. It names the step or document where it must |
| `answer` | Short text answer |
| `answer_value` / `unit` | For numeric answers, from the CSV or annex, never typed |
| `evidence` | List of `{doc_id, quote}`. Every quote is a verbatim substring of the rendered document |
| `docs` | Sorted list of the doc_ids needed |
| `reasoning` | For L2 and above: the steps from evidence to answer, one short line each |
| `key_points` | SUM only: list of `{point, evidence: [{doc_id, quote}]}` |
| `expected` | NONE only: `"not in the documents"` and a `absent_terms` list that the script checks appear in no Version 2.0 document |

## Levels and generators
Target counts are rough; take what the data give, without padding.

- **L1, about 40: one fact, one document, one passage.** Generate from the annexes, whose quotes already ground.
  Cover parameter NOR, PAR and class, attribute criteria, study dates and identifiers, method precision, and
  discrepancy subjects. Spread the items across all documents in scope.
- **L2, about 40: reasoning within one document.** Generate from the CSVs and helpers, with the evidence passages from
  that one document. Examples:
  - is the NOR inside the PAR, and by what margin;
  - which output limits the design space;
  - was a criterion met, and by how much;
  - which factor has the largest effect on an output;
  - how many discrepancies a report records.
- **L3, about 30: the same fact across two documents.** Examples:
  - a parameter's NOR in the plan and in the report;
  - a criterion in PCMP-001 and in the report that applies it;
  - a study planned in the plan and reported in the report;
  - a risk ranking in RA-001 and the class in the report.
- **L4, about 25: reasoning across several documents.** About 15 generated chains, for example:
  - the derivation of a criterion through the downstream steps: the drug substance limit, the UF/DF increase, the
    cation exchange fold and the low-pH increase give the bioreactor aggregate criterion (PCMP-001, PCR-010, PCR-007,
    PCR-006, PCR-003);
  - which verification tightened or widened which criterion;
  - which investigation finding led to which change.
  About 10 curated.
- **SUM, about 8: curated summarization prompts.** Each comes with 5–12 grounded key points. Examples:
  - summarize the control strategy across the steps;
  - summarize what changed from Version 1.0 to 2.0 and why;
  - summarize the open risks flagged for manufacturing;
  - summarize the scale-down model qualification across the steps.
- **NONE, about 15: curated questions the corpus cannot answer.** For example: the bioburden limit of the harvest
  hold, the commercial batch size, a resin's lifetime in cycles. Each lists `absent_terms` that the script verifies are
  in no Version 2.0 document. Avoid anything a document does state.

## Rules
- **Golden rules hold.** No value is typed. Generated answers come from the CSVs, the annexes and the helpers.
  Curated items keep their numbers in the quotes. If a re-seed breaks a curated quote, the build reports the item as
  stale and leaves it out, and the test fails only if a level drops below its minimum.
- **Plain questions.** Use the document's terms of art. Do not leak the answer in the question. Do not ask "according
  to Table 7.3".
- **Prefer evidence that names its subject.** A table row read with its header, or a sentence that names the record.
  Never a caption alone, as in the annex anchor rule.
- **Keep the agent-written part small** (curated: about 35 items in all).
