---
type: pm-task
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
task: TASK-002
status: todo
kind: mechanism
title: "Rewrite the guide's sentence rule as a substitution, fix the \u2713 text that teaches the fault, and add the referent and Shape 4 examples"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-002 — Rewrite the guide's sentence rule as a substitution, fix the ✓ text that teaches the fault, and add the referent and Shape 4 examples

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-002.md in this work unit — numbered steps, code, commands and the output each must print. Follow it top to bottom.  OWNER DECISION: minimum edits only. Do not re-author the guide's commentary; that is a hypothesis for a later unit (decisions.guide_scope). Change the rule text, the ✓ blocks that teach the fault, and add the examples listed. Nothing else in the guide moves.  WHERE. §2d starts at WRITING_GUIDE.md line 155; the rule sentence is lines 157-159 ('One sentence, one point; if a sentence carries two claims, make it two sentences.'). Correction 2 is lines 197-211; its ✓ at 208-211 is the construction the corpus over-produces. §2d bis starts at 232. Shape 4 is at line 316 with its deletion-only correction at 331-345. §4a's table is under line 404; §4b 'Prefer plain connectives' is lines 490-499.  THE ARGUMENT TO WRITE DOWN in §2d, in one paragraph, with the numbers: the sources put the next reasoning step after a full stop and open it with a connective (3.7–6.1 % of sentences); the corpus puts it after a comma (', so ' in 6–11 % of sentences, 20–30× the source rate) and opens 0–2 % of sentences with a connective. Round one made it worse (PCR-003 6.5→8.0 %, PCP-003 7.9→10.6 %). This is one defect seen from both ends.  THE OWNER'S OWN WORDS on the sentence: 'hard to understand, too many arguments in one sentence including a recommendation in the last part. A classical case for fillers like Therefore, However, As a consequence.'  ON THE EXEMPLAR QUOTES: every quote must be verbatim in refs/text/ and pass check_exemplar_quotes.py, which reads the same extracts; a quote spanning a page break fails (TASK-004 of the previous unit lost 1 of 25 that way). Pick pairs inside one page.  ON RUNTIME NOUNS: add one line under §6 or §2d — an inline expression that yields a response or parameter NAME must not be the grammatical subject of a clause whose verb must agree with it ('acidic variants is the case to watch' came from `{python} lof_p_lo_resp.lower()`); put it in a frame the number cannot break ('the weakest case is …', 'for …').

## Acceptance criteria

- [ ] WRITING_GUIDE.md §2d states the rule as a substitution: one argument step per sentence; the next step opens the NEXT sentence with the connective (However / Therefore / As a result / Consequently / For this reason …); the constructions to search a draft for are named verbatim — ', so ', ', and ' joining a second clause, ', which ' carrying a new claim
- [ ] §2d carries a worked correction built from the owner's sentence, PCR-003 line 707 as it stood on 2026-08-17 ('The lack-of-fit tests rest on … , so a non-significant result … , and … is the case to watch'), labelled with the date, showing three sentences with the second and third connective-led
- [ ] §2d Correction 2's ✓ text no longer contains ', so ' (currently line 208: 'sit far from their limits, so the capability indices show only that'); no ✓ block in §2d, §2d bis or §4c contains mid-sentence ', so ' — check by reading every '> ✓' block
- [ ] §2d gains the referent rule: a sentence that counts a set ('the four', 'both', 'the three') names it in the same sentence or the paragraph already has, with PCR-003 line 701 ('a response-surface design that models the four that matter', 2026-08-17) as the ✗ example
- [ ] §2d bis names the substitution (the definite article or the noun; never 'it is' / 'it was') and states a BAND for 'its' and 'their' from the pilot's table (sources: its 0.27–0.40, their 0.50–0.96 per 1000 words) instead of a minimum, and says why: PCP-003 round one removed 25 possessives and added 23 copulas
- [ ] Shape 4 gains a positive worked correction: a corpus sentence (from PCR-003 or PCP-003 as of 2026-08-17, dated) rewritten to open with a connective or a condition, alongside the existing deletion example
- [ ] §4a's target table gains two rows for the TASK-001 measures with the per-source values (', so ' 0.1 / 0.3 / 0.4 / 0.4 %; sentence-initial connective 4.8 / 6.1 / 4.2 / 3.7 %) and the note that neither is gated
- [ ] §4b 'Prefer plain connectives' says WHERE the connective goes — at the head of the sentence, after the full stop that ends the previous step — with the corpus figure (0–2 % of sentences against 3.7–6.1 %)
- [ ] REGISTER_EXEMPLAR.md gains at least three verbatim two-sentence source quotes in which the second sentence opens with a connective and carries the consequence of the first, from at least two sources; `uv run python authoring/check_exemplar_quotes.py` passes
- [ ] `make style PY="uv run python"` passes (it runs the exemplar checker)

**Depends on:** [[TASK-001]]

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- [[WRITING_GUIDE]] — `authoring/WRITING_GUIDE.md`
- [[REGISTER_EXEMPLAR]] — `authoring/REGISTER_EXEMPLAR.md`
