# TASK-007 procedure — the decision point the pilot exists for

**Stop here.** `TASK-008` does not start until the project owner has read the three pilot documents
and D3 is settled. This is the whole reason the round was split.

## 1. Measure, one invocation

```bash
U=.claude/work/2026-08-18_02_register-track-d
uv run python $U/measure_trackd.py \
   pc_package/PCP-007_cex.qmd pc_package/PCR-005_protein_a.qmd pc_package/RA-001_risk_assessment.qmd \
   pc_package/PCR-003_bioreactor.qmd > $U/measure_pilot.txt
```

`PCR-003` is in that list as the **control**: it is already at the target register and this round
does not touch it. A measure that moves in the three and not in `PCR-003` is the instruction. A
measure that moves in all four is something else, and the page has to say so.

Compare each of the three against its own row in `measure_baseline_style.txt` /
`measure_baseline_discourse.txt`, never against another document.

## 2. Apply the pilot stopping rule, per document

From `state.json` → `decisions.pilot_stopping_rule`, and **no edge moves now that the numbers are
visible**:

| # | condition | edge |
|---|---|---|
| 1 | mid-sentence `, so ` | ≤ 1.0 % |
| 2 | opens with a connective | ≥ 3.0 % |
| 3 | `, and ` + second clause | ≤ 3.4 % |
| 4 | mid-sentence `, not ` | ≤ 0.2 % |
| 5 | passive | inside 53–68 % |
| 6 | topic chaining | not below that document's own baseline |
| 7 | copula | not more than 2 pt above its own baseline |
| 8 | register gate | passes |
| 9 | corpus | 2084/2084, 0 weak anchors, 20/20 valid |

`RA-001` starts at 64.2 % passive and `PCP-007` at 63.0 %, both already inside band, so condition 5
is a **ceiling** for them. If either rises above 68 %, that is a failure and not a success.

## 3. The owner's reading

Ask the project owner to read the three rendered PDFs and answer: **is any of them still
immediately recognisable as machine-written, and which sentences give it away?** Record it
verbatim and dated. Whatever it quotes is counted afterwards, in that order — a reader finds it,
the count confirms it. That order is what produced every target this campaign has had, and round
three is the one time it produced nothing.

State the caveat on the page: `RA-001` and `PCP-007` have never been read before, so this is a
first read of two of the three, which makes it a stronger check than round three's fourth read of
the same document.

## 4. Write D3 and stop

`docs/pm/decisions/D3-does-track-d-continue.md`, `status: open`, `waiting_on: project owner`,
`blocks: TASK-008 … TASK-030`. Both branches, with the numbers:

- **Continue** — the rule holds and the reading is acceptable: the remaining 16 run in four
  batches, and nothing about the instruction changes.
- **Stop** — a condition fails, or the reading still names sentences: the round ends at three
  documents instead of nineteen, and Track C (rewriting the guide's own commentary, measured at
  3.77 % `, so ` and 10.38 % `, and `+clause) becomes the candidate. Say what the three documents
  cost, so the trade is visible.
