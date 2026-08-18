---
type: pm-decision
sprint: 2026-08-18_02_register-track-d
status: open — numbers and reading are in; the owner settles it
waiting_on: project owner
blocks: TASK-008, TASK-009, TASK-010, TASK-011, TASK-012, TASK-013, TASK-014, TASK-015, TASK-016, TASK-017, TASK-018, TASK-019, TASK-020, TASK-021, TASK-022, TASK-023, TASK-024, TASK-025, TASK-026, TASK-027, TASK-028, TASK-029, TASK-030
tags: [pm/decision]
---

# D3 — after the pilot of three, do the remaining sixteen run?

**What is being asked.** Track D re-authors 19 documents. Three of them run first as a pilot —
`PCP-007` (a plan), `PCR-005` (a DoE report) and `RA-001` (never re-authored, and the largest annex
in the corpus at 317 quotes) — and then the round stops. This note is that stop.

It exists because of one risk that a pilot makes cheap. The proposal's own leading hypothesis is
that `WRITING_GUIDE.md` is written in the register it forbids: measured 2026-08-18, its commentary
carries a mid-sentence `, so ` in **3.77 %** of its sentences and a `, and ` + second clause in
**10.38 %**, against four human sources at 0.1–0.4 % and 1.1–3.4 %. If the guide is the blocker,
every document authored from it needs doing again. Finding that out after three documents costs
three; after nineteen it costs nineteen.

**The numbers that will be in front of you.** The nine-condition stopping rule in
`state.json` → `decisions.pilot_stopping_rule`, applied per document, fixed before the pilot ran and
not moved afterwards. Plus your reading of the three rendered PDFs. Two of the three —
`PCP-007` and `RA-001` — you have never read, which makes this a stronger check than round three's
fourth read of the same document.

**Option A — continue.** The rule holds and the reading is acceptable. The remaining 16 run in
four batches and nothing about the instruction changes. Cost: the bulk of the round, 16 one-pass
re-authors and roughly 250 annex quotes re-anchored.

**Option B — stop at three.** A condition fails, or the reading still names sentences. The round
ends having spent three documents, and Track C — rewriting the commentary of `WRITING_GUIDE.md`,
`REGISTER_EXEMPLAR.md`, `STORY_BIBLE.md` and `CLAUDE.md` into the register they demand — becomes
the candidate instead. The three pilot documents stay: they are re-authored, grounded and shipped
either way.

**What the plan assumes meanwhile.** That the answer is A, because round three is direct evidence
that the current guide plus the printed measures produces a document the owner accepts. That is an
assumption about one document and one genre, which is exactly what the pilot tests.


---

## The pilot ran. Here are the numbers and the reading — 2026-08-18

### The eight numeric conditions all hold

Fixed before TASK-003 ran and not moved since. Produced by
`.claude/work/2026-08-18_02_register-track-d/measure_trackd.py`, saved to `measure_pilot.txt`.
`PCR-003` is the untouched control and reads ±0.0 against its own baseline, which is the check
that the table is measuring what it claims to.

| condition | band | PCP-007 | PCR-005 | RA-001 | holds? |
|---|---|---|---|---|---|
| `, so ` mid-sentence | ≤ 1.0 | 0.0 (0/219) | 0.0 (0/424) | 0.0 (0/190) | yes |
| opens with a connective | ≥ 3.0 | 4.6 (10/219) | 4.5 (19/424) | 4.7 (9/190) | yes |
| `, and ` + clause, regex | ≤ 3.4 | 0.0 (0/219) | 2.1 (9/424) | 0.5 (1/190) | yes |
| `, not ` mid-sentence | ≤ 0.2 | 0.0 | 0.0 | 0.0 | yes |
| passive | 53–68 | 58.0 (127/219) | 54.3 (227/418) | 57.8 (107/185) | yes |
| topic chaining vs own baseline | not below | 59.2 (+19.9) | 39.6 (+4.8) | 44.6 (+5.5) | yes |
| copula vs own baseline | ≤ +2.0 | 13.7 (−3.0) | 18.7 (−8.6) | 17.8 (−6.9) | yes |
| register gate | passing | OK | OK | OK | yes |

Corpus state: 2084/2084 quotes grounded across 20 annexes with strict anchors, 0 weak anchors,
20/20 valid, `git diff outputs/` empty. `--check-baseline` over all twenty documents disagrees on
exactly the three that were re-authored and on no other, which is the evidence the pilot changed
what it was supposed to and nothing else.

### The ninth condition — the reading — does not hold

Recorded verbatim and dated in
`.claude/work/2026-08-18_02_register-track-d/owner-reading-2026-08-18.md`, before anything it
names was counted. The owner quoted four sentences, all from `PCR-005`, and asked whether the
formulation can be stopped: three trailing glosses of the shape *finding, which is <abstract
noun>*, and one periphrastic negation.

### What the quotes count out to, measured afterwards

Per 100 sentences. The four human sources are the band the whole campaign is written against.

| | PDA | A-Mab | ISPE TT | ISPE PV | PCP-007 | PCR-005 | RA-001 | PCR-003 control |
|---|---|---|---|---|---|---|---|---|
| `, which` | 1.1 | 1.4 | 0.6 | 2.4 | **17.4** | **16.7** | 7.9 | **15.3** |
| `, which is/was` | 0.1 | 0.6 | 0.1 | 0.9 | 3.7 | **9.9** | 5.3 | 4.8 |
| `, which is the …` | 0.0 | 0.0 | 0.0 | 0.1 | 0.9 | **3.5** | 0.0 | 2.5 |
| `, because` | 0.0 | 0.2 | 0.0 | 0.1 | **8.7** | 1.9 | **8.9** | 3.4 |

`, which is the …` — the exact shape of two of the four quoted sentences — occurs **once in 3,338
sentences** of published human prose. `PCR-005` has 15 in 424.

### The finding that changes the shape of this decision

**`PCR-003` is the control, at `, which` 15.3.** That document was re-authored in round three and
accepted by the owner then. So the fault the reading names is **not caused by the Track D
instruction, and was not introduced by the pilot**. It is corpus-wide, it predates all three
previous rounds, and it survived them for the reason the campaign has now learned twice: nothing
printed it back to the author. Round three did measure `, which` at 15.33 %, recorded it on the
results page as a regression, and shipped anyway — the number lived in a `.txt` file the author
never saw.

That makes Option B's premise wrong as written. Option B blames the guide's own register (Track
C), and the guide is not what produced this: the control has the same fault, and the pilot
instruction never mentioned `, which` at all.

### Option C — add the measure, then re-author

Not in the original note, because the pilot is what revealed it.

Put `, which`, `, which is the …` and `, because` on the printed clause-packing line in
`check_style.py`, the line that already prints `, so ` and `, and `+clause back to the author on
every `check_render.py` run. Give them a **band, not a ban**: `, which` ≤ 2.4, the top of the four
sources. Add a worked correction to `WRITING_GUIDE.md` §2d for the self-explaining sentence, which
is the move the regexes do not reach — one of the four quoted sentences has no regex signature at
all. Then re-author the three pilot documents against the new measure and read again.

Cost: three documents redone plus one mechanism change, against 16 documents that would otherwise
be authored with the fault the reading just named. `PCR-003` would also need redoing to clear the
corpus, which the round currently leaves untouched as the control.

**Recommendation: C.** A ban on `, which is` is the wrong instrument and this repository has the
receipts — `CLAUDE.md` records that a ceiling on `, so ` is met by writing `, and` or `;`, and
round three drove `, and `+clause from 22.6 % to 0.5 % and paid for it with `, which` rising 5.8
points. Zero would also sit below all four human sources, which is the staccato failure round
three already made once. What has moved every measure it was applied to is printing the number to
the author on every run.
