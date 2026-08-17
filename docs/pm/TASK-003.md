---
type: pm-task
epic: 2026-08-16_01_register-from-four-sources
sprint: 2026-08-16_01_register-from-four-sources
task: TASK-003
status: done
kind: mechanism
title: "Amend WRITING_GUIDE 2c and 2d to license a claim beside its counter-consideration"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-16_01_register-from-four-sources/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-003 — Amend WRITING_GUIDE 2c and 2d to license a claim beside its counter-consideration

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

THIS IS THE ROOT CAUSE. WRITING_GUIDE.md 2c is at about line 80 and 2d at about line 91. The two sentences that cause the defect are, verbatim:
  2c: 'One paragraph, one point. Open with the point, then give the evidence.'
  2d: 'One sentence, one point; if a sentence carries two claims, make it two sentences.'
Every move that carries an argument needs two ideas held together, so all of them are forbidden: However needs a claim and a counter-consideration, For example needs a rule and an instance, By contrast needs two things compared. The authors complied exactly, which is why there is not one However in roughly 30,000 words.

THE FOUR SHAPES to name, all with verbatim examples in mined-patterns.md:
  1. rule -> instance -> counter-move -> quantified resolution. A-Mab: 'For example, it is seen that medium concentration had a statistically significant effect on aFucosylation (p = 0.001). However, by reviewing Figure 3.4 it is seen that its effect was very shallow. In this case, changing the medium concentration from 0.8 to 1.6 X only changed the aFucosylation levels by 0.3 %.'
  2. concession before commitment. A-Mab: 'Although key process parameters and key process attributes have been shown not to impact product quality, they are included in the control strategy because their monitoring and control ensures that the process is operated in a consistent and predictable manner.'
  3. finding with its limit in the same sentence, the limit in consequence terms not statistical ones. A-Mab: 'Grey arrows indicate the effect was detected statistically but is too small to have an appreciable effect on the quality of the material produced.'
  4. frame before the subject. About one human main clause in four opens with an adjunct (A-Mab 29.5 %, PDA 25.4 %) against 9-14 % of corpus clauses. The human front field carries a connective (Also, Thus, Therefore, However, In addition, For example, In this case); the corpus front field carries an enumerator (First, Second, Third, For galactosylation, For high mannose). Same slot, different job.

THE WORKED CORRECTION to use for shape 1, because it is the sentence the project owner flagged. Before, PCR-003 5.2: 'These are large and well-resolved effects of limited practical consequence, because the attribute is of very low criticality and its acceptance criterion is applied as an upper limit that lies far above the observed range.' Its root verb is 'are', its subject is a bare demonstrative whose antecedent is a table, and its payload is three nominalisations on four stacked prepositions. After: three sentences, three lexical main verbs, one However, and the number that settles the doubt given in place rather than deferred to another section. A full rewrite is in syntax-analysis.md under 'Worked rewrite'.

KEEP THE EXCEPTION NARROW. It licenses a tension pair, NOT long sentences. The failure it must not cause is the first-pass corpus: a 34-word mean sentence, 10-13 em-dashes per 1000 words against A-Mab's zero, and a semicolon splice in every fourth sentence. Say this inside the amendment so the next reader cannot widen it by accident.

## Acceptance criteria

- [x] 2c and 2d keep one-point-per-unit as the default and name the licensed exception explicitly
- [x] four shapes are named with their form and at least one verbatim source example each
- [x] each shape carries a worked correction built from a real corpus sentence, in the style of 4c
- [x] the amendment states the opposite failure it must not cause, citing the 34-word first-pass mean and the 17-word staccato regression
- [x] make style PY="uv run python" still passes

## What was built

WRITING_GUIDE 2c and 2d both keep one point per unit as the default and both name the same single licensed exception: a point may be held together with its counter-consideration. 2c carries the paragraph shape, 2d the three sentence shapes.

FOUR SHAPES, each with verbatim source examples and a worked correction:
  1 rule -> instance -> counter-move -> quantified resolution (2c). 1 A-Mab example.
    Correction from PCR-003 5.2, the sentence the project owner flagged.
  2 concede first, then commit (2d). 2 A-Mab examples.
    Correction from PCP-003 6, the re-issued matrix sentence.
  3 finding and limit in one sentence, limit in consequence terms (2d). 1 A-Mab.
    Correction from PCR-003 5.2, the afucosylation null result.
  4 the frame comes before the subject (2d). 2 A-Mab + 1 PDA TR 60.
    Correction from PCR-003 2.1, the First/Second/Third/Fourth run.
Seven source quotes and five corpus quotes, all 12 verified verbatim against refs/text/ and the .qmd files with the check_exemplar_quotes normalisation.

TWO ERRORS CAUGHT IN MY OWN DRAFT, both worth knowing because they are the failure modes this guide is meant to prevent:
  - The rewrite in syntax-analysis.md uses `acid_max`, which does not exist anywhere in the repository. Left as it stood, the guide would have taught the next author a helper that is not there. The guide now shows the real derivation, `csv(f'doe_{UO}_screening.csv')['acidic_variants'].max()`, and says the number itself may not be typed.
  - My first shape-3 rewrite ended 'both are carried into the response-surface stage'. False: doe_bioreactor_rsm.csv carries pH, temperature, duration and CO2, and drops osmolality. The corrected example says so, and the miss is written up under the example as a warning that a shape is not a licence to write a tidier sentence than the study supports.

Four asserted numbers were also wrong on first draft and were recomputed: the concession example is 18 words not 20 (mined-patterns.md says 20), the PCP-003 sentence is 28 words not 33, the human examples run 14 to 24 words with one at 40 rather than 12 to 30, and shape 4 now quotes the measured 29.5 / 25.4 % against 9.1 to 13.6 % instead of 'one in four'.

The opposite-failure warning is in 2c and cites both regressions: the first-pass 34-word mean against a human 24 to 30, 10 to 13 em-dashes per 1000 words against A-Mab's zero, a semicolon splice in every fourth sentence, and the staccato correction at 17-word averages with 40 % of sentences under 15 words.

Gates: make style exit 0 (4 sources + 20 documents OK, 0 FAIL, 88 quotes checked 0 failed); make test 85 passed. No document changed, so no annex was touched.

FOR TASK-004: the moves catalogue covers seven patterns, and four of them now have a worked treatment here. Do not duplicate the prose. REGISTER_EXEMPLAR.md is the place for the passages; this is the place for the rule and the correction.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- [[WRITING_GUIDE]] — `authoring/WRITING_GUIDE.md`
