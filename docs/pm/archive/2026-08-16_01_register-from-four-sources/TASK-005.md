---
type: pm-task
epic: 2026-08-16_01_register-from-four-sources
sprint: 2026-08-16_01_register-from-four-sources
task: TASK-005
status: done
kind: mechanism
title: "Exemplify the given-new rule WRITING_GUIDE 2d already states"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCMR-001", "PCP-003", "PCP-004", "PCR-003", "PCR-004", "PCR-005", "PCR-008", "RA-001"]
---

> [!warning] Generated from `.claude/work/2026-08-16_01_register-from-four-sources/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-005 — Exemplify the given-new rule WRITING_GUIDE 2d already states

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

THE CHEAPEST ITEM IN THE PLAN, because the rule already exists and is simply not met. WRITING_GUIDE 2d says, verbatim: 'Begin with information the reader already has and end with the new information.' Measured with the topic-chaining function in register_analysis.ipynb section 8: a sentence counts as chained when its subject names something the previous sentence mentioned, or is a pronoun. A-Mab 59.0 %, PDA TR 60 59.4 %, PCR-003 35.1 %, PCR-005 34.8 %, PCR-008 32.8 %, PCP-003 31.0 %. So two thirds of corpus sentences start a fresh topic and the reader is re-oriented on nearly every one.

WHERE TO GET THE CORRECTIONS. The corpus's own topic switches are the material: PCR-003's 'For galactosylation', 'For high mannose', 'For aggregate' openings are a parallel block of five, one per response, each starting a new subject. The repair is to carry the previous sentence's subject forward, or to name the referent, rather than opening a fresh topic label.

THE POSSESSIVE RULE, which belongs here because it is the same defect at word level - a referent the reader must bind rather than read. Measured per 1000 words: 'its' 6.67 in PCR-003 against A-Mab's 0.28, which is 24 times the rate; 'their' 4.16 against 0.53; 'it' 10.63 against 1.50. The corpus writes 'its acceptance criterion', 'its characterized range', 'its set-point', 'its limit', 'its expiry', 'its release specification'. A-Mab writes 'the acceptance criterion', or names the thing. Rule to add: prefer the definite article or the noun itself; a possessive is for a genuine relationship the reader would otherwise mistake, not for every attribute of a thing already under discussion. The sentence the owner flagged uses two.

This finding came from the unsupervised divergence ranking in register_analysis.ipynb section 5, not from reading; it is the largest single divergence any method found.

## Acceptance criteria

- [x] 2d's given-new rule carries at least three worked corrections built from real corpus sentences that break it
- [x] each correction shows the repair, which is naming the referent rather than opening on a fresh subject
- [x] the possessive rule is added with its measured contrast
- [x] make style PY="uv run python" still passes

**Depends on:** [[TASK-003]]

## What was built

WRITING_GUIDE 2d's given-new rule now carries three worked corrections, all built from real corpus sentences, and a new 2d bis states the possessive rule.

THE THREE CORRECTIONS, each traced to a document and a verified section name:
  1 PCR-004, Quality attributes in scope. Three consecutive sentences, three brand-new subjects, three copulas. The repair puts 'the three' from sentence one into the subject of sentences two and three, so the ranking is on the page rather than in the reader's head.
  2 PCMR-001, Process capability. A sentence that had a given available and opened somewhere else, stacking three possessives. The repair chains on 'the remaining attributes' and drops two of the three.
  3 PCP-004, Factors, ranges and study type. One sentence with FOUR 'its', the fourth binding to a different parameter than the first three. The repair splits it into three sentences and keeps exactly one possessive, the one marking a real relationship.

MEASURED AGAIN RATHER THAN TRUSTED. The plan quoted chaining from four documents against two sources. I reproduced register_analysis.ipynb section 8's topic_chaining over all four sources and all twenty documents (spaCy is not a project dependency; run it with `uv run --with spacy --with <en_core_web_sm wheel URL>` -- `--with spacy` alone builds a fresh env each time and the downloaded model is not in it).
  sources  PDA 59.4, A-Mab 59.0, ISPE TT 61.9, ISPE PV 57.0  -> 57.0 to 61.9 %
  corpus   median 36.3 %, range 29.2 (PCR-004) to 42.2 (RA-001), 20 documents
The plan's per-document figures were close but not exact (it had PCR-003 35.1, I measure 37.2), so the guide quotes the corpus-wide median against all four sources instead of one document against one source.

POSSESSIVE TABLE, all 13 cells re-measured and matching what is written:
  its    corpus 5.73 | PDA 0.40  A-Mab 0.32  ISPE TT 0.27  ISPE PV 0.36
  their  corpus 2.29 | 0.96  0.50  0.63  0.69
  it     corpus 9.59 | 3.12  1.75  3.33  3.19
'its' runs at 14.2 times the highest source, and PCR-003 reaches 6.66. The plan's A-Mab figures (0.28 / 0.53 / 1.50) came from a different page range; over the self-test range they are 0.32 / 0.50 / 1.75, and those are the numbers in the guide.

REGISTER_EXEMPLAR gained section 23, 'Carrying the topic forward': four verbatim passages showing chained subjects, mined with the same parser and verified. Two A-Mab, one ISPE TT, one ISPE PV. The file is at 124 quotes, 0 failed. The note points out that every chained subject repeats a noun rather than varying it, which ties the chaining rule to the noun-repetition habit the file's opening already asks for.

Gates: make style exit 0 (4 sources + 20 documents OK, 0 FAIL); check_exemplar_quotes.py 124/124; make test 85 passed. No document changed, so no annex was touched.

FOR TASK-007: the three ✗ passages are live text in PCR-004, PCMR-001 and PCP-004. They are quoted in the guide as faults, and they are still in the corpus. Only PCP-003 is being re-authored, so those three stay as they are until somebody decides otherwise; that is a scope question for the pilot's result, not a defect.

## Documents it is about

- **PCMR-001** — `pc_package/PCMR-001_master_report.qmd`
- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCP-004** — `pc_package/PCP-004_harvest.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-004** — `pc_package/PCR-004_harvest.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`
- **RA-001** — `pc_package/RA-001_risk_assessment.qmd`

## Files it touched

- [[WRITING_GUIDE]] — `authoring/WRITING_GUIDE.md`
- [[REGISTER_EXEMPLAR]] — `authoring/REGISTER_EXEMPLAR.md`
