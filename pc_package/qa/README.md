# Graded question–answer set

A test set for the `dw` tool (doctool): it scores a retrieval pipeline (does it find the right
passage in the right document, and is the answer right) and a summarization run (does it cover
the key points, with correct citations). The summarization items stand in for the deferred
master report PCMR-001.

| File | What it is |
|---|---|
| `qa_set.jsonl` | The set, one JSON object per line. Generated; do not edit. |
| `qa_set.md` | The same set as a readable listing, grouped by level. Generated. |
| `curated.yaml` | The hand-written items (L4, SUM, NONE). Edit this. |
| `../build_qa.py` | Builds the set and checks every item. |

## Scope

Only the Version 2.0 documents in `build_ground_truth.REV2_READY`, read from their rendered
`.docx`. A document that joins REV2_READY (PCR-007 and PCR-008 when they are promoted) is picked
up on the next build, with no code change. The superseded Version 1.0 files are never evidence.

## Regenerate

```bash
make qa PY="$PWD/.venv/bin/python"     # or: cd pc_package && python build_qa.py
```

Run it after `make corpus`, because it reads the rendered documents. It prints the count per level
(generated, curated, total, minimum), any stale curated item and any annex value that disagrees
with the data, and exits 1 if a level falls below its minimum. `tests/test_qa_set.py` builds the
set in memory and asserts that every quote grounds, that ids are unique and that every level meets
its minimum.

## Item schema

| Field | Content |
|---|---|
| `id` | Stable, from the template and its keys (`L1-param-nor-pcp-005-load-flow-rate`), never a counter. |
| `level` | `L1`, `L2`, `L3`, `L4`, `SUM` or `NONE`. |
| `template` | The generator, or `curated`. |
| `question` | Plain English. It names the step or document where it must, and does not leak the answer. |
| `answer` | Short text answer. |
| `answer_value`, `unit` | For a numeric answer, from the CSVs or the annexes, never typed. A range is `[low, high]`, with `null` for an open end. |
| `evidence` | List of `{doc_id, quote}`, and `table_header` when the quote is a table row. Each is a verbatim substring of the rendered document. |
| `docs` | Sorted list of the doc_ids the evidence comes from. |
| `reasoning` | L2 and above: the steps from evidence to answer, one short line each. |
| `key_points` | SUM only: list of `{point, evidence: [{doc_id, quote}]}`, 5 to 12 per item. |
| `expected`, `absent_terms` | NONE only: `"not in the documents"`, and the terms the build verifies occur in no Version 2.0 document (whole-word, case-insensitive). |

### How a quote is matched

Exactly as `check_grounding.py` matches an annex quote, using its own functions: the text of
`word/document.xml`, whitespace collapsed, sub- and superscript digits folded to plain digits, and
a table cell boundary read as `" | "`. A table-row quote such as
`Culture pH | pH | 6.85 | 6.75–6.95 | 6.6–7.1 | WC-CPP | multivariate` therefore spans several cells.
A consumer whose elements are cells, not rows, should split such a quote on `" | "` and accept the
citation when the cells are found in order in one row. `table_header` names the columns of the row,
since a row alone does not say which number is the NOR. Rendering artifacts survive the
normalisation: a cross-reference renders as `( Section 3 )` and a subscript as `log 10`, so the
curated quotes stop short of them.

## Levels

| Level | What it tests | Source | Minimum |
|---|---|---|---|
| L1 | One fact, one document, one passage: NOR, class, PAR, criterion, study dates, method, study event, discrepancy subject, Cpk, transfer gap, initial risk priority. | Annexes | 30 |
| L2 | Reasoning within one document: NOR inside the PAR and by how much, a criterion met over the NOR and by what margin, lack of fit and the R² gap, the lowest Cpk, the number of discrepancies, the highest initial RPN of a step, the critical parameters of a step. | Annexes, CSVs, `tables.py` and `doe_report.py` | 25 |
| L3 | The same fact in two documents: a NOR in the plan and the report, a class in the report and in PCMP-001 or PTP-001, a criterion in PCMP-001 and in the report, a study planned and executed, an initial priority in RA-001 and the class in the report. | Annexes | 15 |
| L4 | Reasoning across several documents. Generated: the derivation of a tightened or widened criterion (PCMP-001 Table 9, the verification table of INV-001, the step report), and a parameter traced from RA-001 through plan and report to PTP-001. Curated: investigation findings and their consequences, cross-step chains. | Generators and `curated.yaml` | 15 |
| SUM | Summarization prompts with grounded key points. | `curated.yaml` | 6 |
| NONE | Questions the corpus cannot answer. | `curated.yaml` | 12 |

Generated items are selected stably (by a hash of the item id, round-robin over templates) with a
cap per document (L1, L2) or per unit operation (L3), so the set does not grow with the size of a
table. An item whose quote does not ground is dropped. An annex value that disagrees with the CSV it
should come from (a document rendered before the data changed) is left out and listed by the build.

## How to score

- **Retrieval.** A hit is a retrieved passage in a document of `docs` that contains an evidence
  quote (or, for a row quote, all of its cells). Score recall over the evidence of an item, and
  document recall over `docs`. For L3 and L4 every document in `docs` is needed.
- **Answer.** Compare `answer_value` numerically where it exists (a relative tolerance of 1 % covers
  the rounding of a rendered value), and the `answer` text otherwise (exact identifiers such as
  `AMV-3012`, `WC-CPP` or `PD-005-06`; a judge for free text). `reasoning` lets a judge credit the
  path as well as the result.
- **Citations.** A cited quote is correct when it is verbatim in the cited document; it supports the
  answer when it overlaps an evidence quote of the item.
- **SUM.** Coverage is the share of `key_points` the summary states; a point counts only when the
  statement cites a quote that is verbatim in one of the point's evidence documents. Report
  precision as the share of cited statements whose quote is verbatim.
- **NONE.** The correct response says that the documents do not state it. Any concrete value is
  wrong.

## Curated items

Keep them few (about 35). Write them from the rendered text of the Version 2.0 documents, never
from Version 1.0. Every number goes in a quote; the answer restates it. Prefer a sentence that names
its subject, or a table row with its header, never a caption alone. If a re-seed or a re-authored
document breaks a quote, the build reports the item STALE and leaves it out; re-anchor the quote on
the document, or retire the item. A NONE item lists `absent_terms` that are specific enough to
prove absence (a term that also occurs in another sense, such as "Tween" in "between", is matched
as a whole word).
