# Content review of the PCP-009 draft — before promotion

**2026-08-20, TASK-023 §4.** Batch B3, authored under the amended rule 4. §5c assigns **D-001**.
Two fresh judges (`opus`), one return between them.

## Counts per question

| run | Q1 | Q2 | Q3 | Q4 | verdicts |
|---|---|---|---|---|---|
| 1 (as authored) | 6 | 3 | 3 | 7 | No · No · No · Yes |
| 2 (after one cycle) | 0 physical (6 procedural, see below) | 0 | 0 | 4 (+3 mild) | **Yes** · **Yes** · **Yes** · Yes |

**This is the strongest result of the campaign.** Three of the four questions pass. Run 2's Q1
answer is worth quoting in full, because it is a judgement rather than a count:

> "Every causal verb names its cause in the clause where it stands, and none defers to a colon or
> the next sentence. The judgment call: six uses give a procedural or documentary reason rather
> than a physical one … In each the claim being supported is itself procedural, so a physical cause
> would have been wrong there; if the question is read strictly literally, those six make it a no."

That is a fourth judge arriving independently at the scope line the question lacks, and the first
to say plainly that supplying a physical cause in those places **would have been wrong**.

## Run 1, and what the return fixed

Q1: six verbs delegating to a section instead of naming the mechanism. Q2: "governed response"
(coined, four places), "NOR-propagated range", and **"predictive interval"** where the term of art
is *prediction interval*. Q3: three sentences, including one whose "changes the pore structure"
carried no direction. Q4: seven.

The author moved the mechanism into the clause in every case, removed "governed response" in
favour of "the two viral clearance responses", and corrected **predictive interval → prediction
interval**. That correction matters beyond this document: the wrong term appears in eight shipped
documents and is seeded in `doe_report.py`'s own docstring, from which every author read the
helper signature. Recorded for a machinery proposal; not fixed here.

## Run 2 residue

Q4 only: four clear instances plus three mild, all trailing clauses that re-file a finding
("Any manual entry of a value into the analysis is a data integrity finding and will be handled as
one."). D-001 intact and unreconciled.
