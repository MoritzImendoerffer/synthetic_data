---
type: pm-task
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
task: TASK-002
status: done
kind: mechanism
title: "Rewrite the guide's sentence rule as a substitution, fix the \u2713 text that teaches the fault, and add the referent and Shape 4 examples"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-002 — Rewrite the guide's sentence rule as a substitution, fix the ✓ text that teaches the fault, and add the referent and Shape 4 examples

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-002.md in this work unit — numbered steps, code, commands and the output each must print. Follow it top to bottom.  OWNER DECISION: minimum edits only. Do not re-author the guide's commentary; that is a hypothesis for a later unit (decisions.guide_scope). Change the rule text, the ✓ blocks that teach the fault, and add the examples listed. Nothing else in the guide moves.  WHERE. §2d starts at WRITING_GUIDE.md line 155; the rule sentence is lines 157-159 ('One sentence, one point; if a sentence carries two claims, make it two sentences.'). Correction 2 is lines 197-211; its ✓ at 208-211 is the construction the corpus over-produces. §2d bis starts at 232. Shape 4 is at line 316 with its deletion-only correction at 331-345. §4a's table is under line 404; §4b 'Prefer plain connectives' is lines 490-499.  THE ARGUMENT TO WRITE DOWN in §2d, in one paragraph, with the numbers: the sources put the next reasoning step after a full stop and open it with a connective (3.7–6.1 % of sentences); the corpus puts it after a comma (', so ' in 6–11 % of sentences, 20–30× the source rate) and opens 0–2 % of sentences with a connective. Round one made it worse (PCR-003 6.5→8.0 %, PCP-003 7.9→10.6 %). This is one defect seen from both ends.  THE OWNER'S OWN WORDS on the sentence: 'hard to understand, too many arguments in one sentence including a recommendation in the last part. A classical case for fillers like Therefore, However, As a consequence.'  ON THE EXEMPLAR QUOTES: every quote must be verbatim in refs/text/ and pass check_exemplar_quotes.py, which reads the same extracts; a quote spanning a page break fails (TASK-004 of the previous unit lost 1 of 25 that way). Pick pairs inside one page.  ON RUNTIME NOUNS: add one line under §6 or §2d — an inline expression that yields a response or parameter NAME must not be the grammatical subject of a clause whose verb must agree with it ('acidic variants is the case to watch' came from `{python} lof_p_lo_resp.lower()`); put it in a frame the number cannot break ('the weakest case is …', 'for …').

## Acceptance criteria

- [x] WRITING_GUIDE.md §2d states the rule as a substitution: one argument step per sentence; the next step opens the NEXT sentence with the connective (However / Therefore / As a result / Consequently / For this reason …); the constructions to search a draft for are named verbatim — ', so ', ', and ' joining a second clause, ', which ' carrying a new claim
- [x] §2d carries a worked correction built from the owner's sentence, PCR-003 line 707 as it stood on 2026-08-17 ('The lack-of-fit tests rest on … , so a non-significant result … , and … is the case to watch'), labelled with the date, showing three sentences with the second and third connective-led
- [x] §2d Correction 2's ✓ text no longer contains ', so ' (currently line 208: 'sit far from their limits, so the capability indices show only that'); no ✓ block in §2d, §2d bis or §4c contains mid-sentence ', so ' — check by reading every '> ✓' block
- [x] §2d gains the referent rule: a sentence that counts a set ('the four', 'both', 'the three') names it in the same sentence or the paragraph already has, with PCR-003 line 701 ('a response-surface design that models the four that matter', 2026-08-17) as the ✗ example
- [x] §2d bis names the substitution (the definite article or the noun; never 'it is' / 'it was') and states a BAND for 'its' and 'their' from the pilot's table (sources: its 0.27–0.40, their 0.50–0.96 per 1000 words) instead of a minimum, and says why: PCP-003 round one removed 25 possessives and added 23 copulas
- [x] Shape 4 gains a positive worked correction: a corpus sentence (from PCR-003 or PCP-003 as of 2026-08-17, dated) rewritten to open with a connective or a condition, alongside the existing deletion example
- [x] §4a's target table gains two rows for the TASK-001 measures with the per-source values (', so ' 0.1 / 0.3 / 0.4 / 0.4 %; sentence-initial connective 4.8 / 6.1 / 4.2 / 3.7 %) and the note that neither is gated
- [x] §4b 'Prefer plain connectives' says WHERE the connective goes — at the head of the sentence, after the full stop that ends the previous step — with the corpus figure (0–2 % of sentences against 3.7–6.1 %)
- [x] REGISTER_EXEMPLAR.md gains at least three verbatim two-sentence source quotes in which the second sentence opens with a connective and carries the consequence of the first, from at least two sources; `uv run python authoring/check_exemplar_quotes.py` passes
- [x] `make style PY="uv run python"` passes (it runs the exemplar checker)

**Depends on:** [[TASK-001]]

## What was built

WRITING_GUIDE.md, seven edits, all inside the sections the owner scoped; no existing commentary outside them was re-authored.

L157-169 §2d: the rule is now a substitution. 'One argument step per sentence', the next step opens the NEXT sentence with the connective, and the three constructions to search a draft for are named verbatim -- ', so ', ', and ' carrying a second claim, ', which ' carrying a new claim -- with the two rates beside them (sources 0.1-0.4 % and 3.7-6.1 %, corpus 6-11 % and 0-2 %) and the note that check_style.py prints both and gates neither.

L171-190 §2d Correction 0: the owner's sentence, PCR-003 Discussion as it stood on 2026-08-17, dated and quoted with the owner's verdict. The corrected version is three sentences with the second and third connective-led ('Therefore, …', 'For this reason …'), and the commentary under it carries the runtime-noun rule: a response name from an inline expression goes after 'is' or after a preposition, never before a verb that must agree with it -- which is where 'acidic variants is the case to watch' came from.

L239 §2d Correction 2: the checkmark text no longer teaches the fault. 'sit far from their limits, so the capability indices show only that' became two sentences with 'therefore' inside the second.

L263-272 §2d: the referent rule, with PCR-003 L701 'the four that matter' as the cross and the four factors named in the corrected version.

L295-303 §2d bis: the substitution is named (the definite article or the noun, never 'it is'), with the pilot's evidence for why -- PCR-003 substituted articles and its copula rate barely moved, PCP-003 replaced 25 possessives with 23 expletive subjects and went 18.4 % to 27.6 %, outside all four sources -- and the target restated as a band (its 0.27-0.40, their 0.50-0.96 per 1000 words) rather than a minimum.

L408-421 Shape 4: a second worked correction that writes a front field instead of deleting one, from PCR-003 Response-surface design, dated. Verified verbatim in the document before quoting.

L496-497 §4a: two diagnostic rows for the TASK-001 measures with the per-source values, and the note at L512 that they were added on 2026-08-17 and fail nothing. L572-574 §4b: where the connective goes -- at the head of the sentence, after the full stop that ends the previous step.

TWO EDITS BEYOND THE PROCEDURE'S DRAFT, both to stop a new line teaching what it forbids. Acceptance line 3 bans mid-sentence ', so ' from every checkmark block, and a line-by-line grep cannot see one broken across a line end. A block-level scan found two more: Shape 3's checkmark at L358 ('…the terms that do, so neither can be called inactive') and Shape 4's first checkmark at L401 ('…the rate of antibody transit, so it was expected to fall'). Both are now two sentences with 'therefore'. The scan reports 0 checkmark blocks with mid-sentence ', so ' in both the guide and the exemplar. The procedure's own draft text for Correction 0 also used the construction twice in its commentary ('This is a substitution, so check it…', 'a runtime value, so it is never…'); both were rewritten as separate sentences. No number was changed.

REGISTER_EXEMPLAR.md L705: new sub-heading 'The step after the full stop' under the connective inventory, with four verbatim pairs from three sources -- PDA TR 60 printed p. 13 / extract p. 21 and printed p. 44 / extract p. 52, A-Mab p. 87, ISPE Technology Transfer printed p. 93 / extract p. 95 -- each a premise finishing as a sentence and a consequence opening the next with For this reason / Therefore / Thus / However. The note points at the A-Mab pair, where the finding and its 'since' clause sit in sentence one and the classification gets its own sentence.

Gates. check_exemplar_quotes.py: 128 quotes checked, 0 failed, up from 124; the four new quotes resolve to extract pages 21, 52, 87 and 95, exactly the pages the procedure named. `make style PY="uv run python"`: exit 0, 24 OK lines, 0 FAIL. `make test PY="uv run python"`: 88 passed, unchanged by this task. No .qmd was touched, so no annex or grounding work was invalidated.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- [[WRITING_GUIDE]] — `authoring/WRITING_GUIDE.md`
- [[REGISTER_EXEMPLAR]] — `authoring/REGISTER_EXEMPLAR.md`
