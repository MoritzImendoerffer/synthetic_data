---
type: pm-decision
sprint: 2026-08-18_02_register-track-d
status: open
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
