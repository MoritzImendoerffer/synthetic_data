# The fifth round, batches B1–B5: nineteen documents under the rebuilt apparatus

**2026-08-19 to 2026-08-21**, work unit `2026-08-19_02_fifth-round-plan-then-batches`.
The pilot (`PCP-005`) has its own page: [`2026-08-19-fifth-round-PCP-005.md`](2026-08-19-fifth-round-PCP-005.md).
This page covers the eighteen documents that followed it, plus the three re-authors the campaign
needed, and closes with the corpus-wide before and after.

## What the campaign did

Every one of the 20 documents was re-authored in one pass by a single fresh-context `opus` agent,
from the brief, `WRITING_GUIDE.md`, `REGISTER_EXEMPLAR.md`, `STORY_BIBLE.md` and
`section_plan.yaml`, and from no sibling document. Each got one content-review cycle with two fresh
judges. The corpus now carries one register.

**Final state: 2089/2089 quotes grounded across 20 annexes**, 20/20 valid, 0 weak anchors under
`GROUNDING_STRICT_ANCHORS=1`, `weak_claims` 0 in all 20, `make test` 95 passed, `make style` 24 OK,
`git diff --stat outputs/` empty.

## The corpus-wide before and after

From `aggregate_campaign.py` in this work unit, which shells out to
`measure_apparatus.py --check-baseline` over all 20 shipped `.qmd` and takes the corpus median of
the per-document cells that command prints. The baseline is the pre-campaign corpus recorded in
work unit `2026-08-18_02_register-track-d`.

```
uv run --extra discourse python \
  .claude/work/2026-08-19_02_fifth-round-plan-then-batches/aggregate_campaign.py
```

| block | measure | n | before | after | delta |
|---|---|---:|---:|---:|---:|
| discourse | passive construction % | 20 | 56.0 | 49.8 | **−6.2** |
| discourse | `, and `+clause, parser % | 20 | 26.8 | 20.9 | **−5.9** |
| discourse | copula main verb % | 20 | 25.8 | 21.7 | −4.1 |
| discourse | adjunct front field % | 20 | 8.5 | 9.4 | +0.9 |
| discourse | topic chaining % | 20 | 36.7 | 36.4 | −0.2 |
| style | parenthetical openings per 1k words | 20 | 7.0 | 1.8 | **−5.3** |
| style | % of sentences over 40 words | 19 | 8.1 | 4.0 | −4.1 |
| style | % sentences with `, and ` + a second clause | 19 | 20.5 | 17.2 | −3.3 |
| style | % sentences with 2+ clause coordinators | 20 | 6.3 | 3.3 | −3.0 |
| style | median sentence length (words) | 18 | 23.0 | 21.0 | −2.0 |
| style | mean sentence length (words) | 18 | 23.4 | 22.1 | −1.2 |
| style | % of sentences under 15 words | 20 | 25.6 | 27.6 | +1.9 |
| style | colons per 1k words | 15 | 0.6 | 0.0 | −0.6 |
| style | semicolons per 1k words | 5 | 0.5 | 0.0 | −0.5 |
| style | coined 3+-part compounds per 1k words | 9 | 0.2 | 0.0 | −0.2 |
| style | **`rather than` per 1k words** | 18 | **0.0** | **1.8** | **+1.8** |

The gated tics went to zero and stayed there. The prose got shorter and less passive.

**And the campaign introduced a tic of its own.** `rather than` went from effectively absent to 1.8
per 1k words across eighteen documents. Three separate judges named it independently: PTP-001's
first judge called it "the carrier", finding that every question-4 hit but one rode on it and
counting about fifteen occurrences in twenty-six pages; PCMR-001's judge called `X is a Y and not a
Z` "the document's most persistent tic". PTP-001 cut it from 15 to 4 after its return and PCP-007
from 12 to 1, but corpus-wide the number rose, because the construction is how an author trained to
avoid a filing clause writes a contrast. **This is the round's own artifact and it is not fixed.**

## Per document

Review counts are flagged sentences per question, run 1 then run 2, in the order Q1/Q2/Q3/Q4. A
question passes when its count reaches zero, except question 4, which passes when the answer is
"no" — no sentence files its own finding.

| document | pp | run 1 | run 2 | audit | note |
|---|---:|---|---|---|---|
| `PCR-006` | — | — | — | clean | B1, authored before rule 4 was amended |
| `PCR-008` | — | — | — | clean | B1; **three attempts**, see below |
| `PCR-009` | — | — | — | clean | B1; **PASS** on its blind reading |
| `PCR-010` | — | — | — | clean | B1, before the amendment |
| `PCR-004` | — | — | — | clean | B2; **two attempts**, see below |
| `PCR-003` | — | — | — | clean | B2 |
| `PCR-005` | — | — | — | clean | B2 |
| `PCP-004` | 27 | 7/3/6/10 | 2/1/0/2 | clean | B3 |
| `PCP-006` | 29 | 7/2/3/7 | 4/0/1/2 | clean | B3; its blind reading FAILED, then the owner reversed it |
| `PCP-008` | — | — | — | clean | B3 |
| `PCP-009` | — | — | — | clean | B3; Q1, Q2 and Q3 all pass — the strongest of that batch |
| `PCP-010` | 25 | 10/0/4/12 | 3/0/0/2 | clean | B3; Q2 passed on the **first** run |
| `PCP-003` | 31 | 21/8/9/15 | 1/0/0/3 | clean | B4; Q2 **and** Q3 converged |
| `PCP-007` | 29 | 13/4/4/8 | 12/0/0/3 | **draft 1 set aside** | B4; see the leak below |
| `PTP-001` | 26 | 5/0/2/6 | 4/0/0/**0** | clean | B5; **question 4 passes — the only document in the campaign** |
| `PCMP-001` | 23 | 9/**0**/**0**/7 | 6/0/1/2 | clean | B5; Q2 and Q3 passed on the **first** run |
| `RA-001` | 27 | 19/5/4/7 | 10/0/8/6 | departure recorded | B5; Q2 converged from 5 coinages to 0, Q3 got **worse** |
| `PCMR-001` | 38 | 12/9/7/14 | — | departure recorded | B5; one cycle, revision addressed all four |

## The three things worth keeping

### 1. The transcript audit has three failure modes, and all three fired in one session

The audit exists to catch an author reading a sibling document or measuring its own register. Its
two filters are a keyword list and a check for any `.qmd` that is not the agent's own draft.

- **False negative, and it did real damage.** `PCP-007`'s first author ran
  `cat authoring/DISCREPANCIES.md`. That file is not a `.qmd` and carries no measurement keyword,
  so neither filter saw it — and it quotes **verbatim prose from four sibling documents**. The leak
  reached the text: the draft's §8.2 fused `PCP-008`'s clause with `PCP-009`'s grid clause. The
  draft was set aside and re-authored. **The author was sent there by an allowed input**: the
  brief's own §5c says "The registry is `authoring/DISCREPANCIES.md`". One agent in two followed
  the pointer.
- **False negative, no damage.** `RA-001`'s author grepped two **sibling drafts**. The `other qmd`
  filter drops any path containing "DRAFT" — a rule meant to exclude the agent's *own* draft, which
  therefore hides every sibling draft in an open batch, which is exactly when siblings are most
  contaminating. The read was one YAML `subtitle:` line each, so the draft was not set aside.
- **False positive.** `PCMR-001`'s author tripped `prose_from_qmd` seven times, every one printing
  its own prose back in slices, plus one `grep -o -h` returning a bare count of one term.

The principle applied across the batch, and it should be written into the procedure rather than
re-derived: **set aside when sibling prose could contaminate; record when the extracted information
is metadata or a count.**

### 2. A review cycle can make a document worse, and did so twice

Two B5 documents had their revision introduce a claim that was sharper than the original and wrong.
Neither was in the pre-review draft; both were checked.

- `PTP-001`: *"Oxygen transfer moves with it, since the same interfacial area per unit volume
  carries both gases."* The preceding sentence's own mechanism predicts the opposite sign. And
  *"deamidation … proceeds faster the longer the product sits"* reads an extent as a rate.
- `RA-001`: *"the settling velocity of a particle falls with the centrifugal field applied to it"* —
  the reverse of the truth, read plainly.

The owner authorised a narrow correctness pass, on the `PCP-010` precedent that a correctness
matter is not a style preference. **The valuable part is what the authors then did**: `PTP-001`
*declined to assert a direction it could not establish*, replacing the false co-movement with the
opposite driving-force direction. Warned of the pattern, `PCMR-001`'s author fitted both AEX
datasets before describing them and caught one of its own claims that implied an order of magnitude
where the data gives a factor of 4. **Naming the failure to the next author stopped it recurring.**

### 3. Authors correctly overruled their judges on corpus consistency, twice

- `RA-001`'s judge called "justified univariate" an invented category. It is A-Mab's own Table 5.16
  rule (`refs/grounding/amab_risk.json`). The author kept it and cited the source.
- `PCMR-001`'s judge called "quality linked" a coinage. It occurs 15 times in `refs/text/amab.txt`
  and 26 times across the corpus. The author kept it, fixed the hyphenation and glossed it once.

Both authors also declined to change terms that are **parameter names rendered verbatim in their
own tables** (`Elution stop collect`, `End of pool collect`), because changing only the prose would
have split each document from its own table.

Against that: `assurance factor` was called invented by **two independent judges**, in `PCP-007`
and `PCMR-001`. Both changed it to `safety factor`, and the source text confirms it — 8 occurrences
of "safety factor" in `refs/text/amab.txt`, **zero** of "assurance factor" anywhere in `refs/`. The
corpus vocabulary now diverges from the comment on `ipc_limits.margin` in `config/parameters.yaml`,
which still calls it the assurance factor. **A one-word config comment edit closes it.**

## The readings, and what the campaign does not know

Nine blind readings ran, **5 PASS / 4 FAIL** — plans 1/1, reports 4/3. All nine were on documents
from B1 to B3. **The owner declined the sampled readings for B4 and B5**, after D8's amendment of
2026-08-21 demoted both from gates to measurements and settled that every promoted document stays.

So: **eleven of the twenty documents were promoted on the content review and the gates alone**, and
the plan-side evidence rests on a single reading — B3's `PCP-006`, which was the narrowest result
of the campaign ("a close win for A. But it is close to a tie") and which the owner reversed once
the key was open. The pre-campaign PDFs for all nine unread documents are committed in the work
unit, so the readings remain available.

`PCR-008` needed three attempts and `PCR-004` two. The `PCR-008` sequence is the campaign's one
controlled result on the apparatus itself: attempts 1 and 2 were written before rule 4 was amended
and both lost their blind readings; attempt 3, under the amended rule, passed. `PCR-004`'s
re-author was written under the unchanged rule and also passed, which is why the amendment cannot
be credited on its own.

## Defects found in the machinery, not fixed

| defect | effect | why not fixed here |
|---|---|---|
| `all_sop_table()` unions only globals ending `_SOP_REFS`/`_AMV_REFS`, skipping the base `SOP_REFS`/`AMV_REFS` | its "every controlled document cited anywhere in the corpus" omits 10 SOPs and all 5 AMVs; found independently **three times** | a mechanism change that moves three documents' rendered tables |
| `ANNEX-A-BATCH` §5 tests `registered_sentence` against the `.docx`, but `PCP-003`'s is stored in `.qmd` form | the check can never pass for that carrier, so a session running it mechanically reads a surviving D-001 as reconciled away | the comment now says so and points the check at the `.qmd`; unifying would bake a seeded value in or rewrite three entries |
| the template subtitle doubles for corpus-level documents | all four B5 drafts read "A-Mab Drug Substance — A-Mab Drug Substance — `<DOC>`" | fixed in the four drafts before promotion; the template is a mechanism change |
| `build_brief.py` does not surface `pc_package/ra_content.py` | `section_plan.yaml` names it as `RA-001`'s content source; that author had to find it | one line in the brief builder |
| `show()` re-parses numeric strings via `to_markdown` | a mixed-magnitude set-point column renders `9e+03` unless `floatfmt="g"` is passed | affects any future corpus-wide parameter table |
| `git mv -f` in `ANNEX-A-BATCH` §1 assumes a tracked draft | it refuses an untracked one; plain `mv -f` is the promotion | procedure wording |

Two plan defects were corrected in `state.json` during execution rather than worked around: the
B5 promotion targets (`<DOC>_None.qmd`, which would have shipped four unreferenced documents and
left grounding checking stale text), and the count notes (`PCMR-001` has 32 rhetorical spans, not
the 49 the plan recorded).

## The annex work the batches required

| batch | documents | quotes re-anchored | spans re-cut |
|---|---|---:|---:|
| B4 | `PCP-003`, `PCP-007` | 52 | 0 |
| B5 | `PTP-001`, `PCMP-001`, `RA-001`, `PCMR-001` | 342 | 32 of 32 |

The bulk were table rows, and they failed for a reason worth recording: **`ANNEX-A-BATCH` says table
rows usually need nothing, because the row builders rebuild from the DataFrame the document
renders. That holds only while the document renders the same table.** Every re-authored
corpus-level document built its own derived tables, so `RA-001`'s per-step table gained a
"Potential effect" column (following it cleared 148 quotes in one edit), `PCMP-001` moved "Set by"
to the end as "Formed or set at", and `PCMR-001`'s capability table kept the raw `two_sided`
spelling with one-decimal Cpk and a thousands separator.

**And `report_sections` statements were false, not merely stale, in every B5 document and both B4
documents.** No gate catches this: the quote grounds and the statement lies. `PCMP-001` asserted
three concepts its re-authored text had dropped; `RA-001`'s annex still counted 22 + 14 + 1 where
the document now says 22 + 15; `PTP-001` claimed none of its gaps is closed by the plan, which it
no longer says. One assertion was deleted outright, because `PCMP-001` no longer states the value
it attested. **Reading every statement against the new text should be a numbered step in the
procedure, not a paragraph of prose in it.**
