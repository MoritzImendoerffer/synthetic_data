# Exploration — why the prose does not read as SME prose

Work unit `2026-08-16_01_register-from-four-sources`. Proposal:
[`docs/next/register-from-four-sources.md`](../../../docs/next/register-from-four-sources.md).

Evidence files beside this one:

| File | What it holds |
|---|---|
| [`rhetoric-comparison.md`](rhetoric-comparison.md) | how the sources argue about DoE results, against how the corpus does |
| [`syntax-analysis.md`](syntax-analysis.md) | the dependency-parse measurements, including the null results |
| [`mined-patterns.md`](mined-patterns.md) | seven patterns with verbatim examples, mined from the sources |

**Verdict: the problem is real and it is not the problem the proposal described.** The proposal
treated the register as a statistics problem to be fixed by recalibrating thresholds. The defect is
in **discourse and information flow**, and the guide's own rules are a substantial part of the
cause. The proposal was rewritten on 2026-08-16 to match. That is a deviation from `/explore`'s
rule that it touches only two status markers outside `.claude/work/`; it was taken because
`/plan` reads the proposal as the requirements, and planning against a spec known to be wrong is
the failure the rule exists to prevent.

---

## 1. What the defect is, measured

Five findings, each against both human sources. Method and full tables in `syntax-analysis.md`.

| Measure | A-Mab | PDA TR 60 | PCR-003 | Gap |
|---|---|---|---|---|
| **% of sentences chained to the previous one** | 57.0 | 59.6 | **35.1** | two thirds of corpus sentences start a fresh topic |
| **`However` / `For example` (counts, whole document)** | 46 / 12 | 21 / 22 | **0 / 0** | zero in ~30,000 words across four documents |
| **% of sentences shaped "X is \<noun phrase\>"** | 14.7 | 18.2 | **33.3** | a third of sentences contain no event |
| **`its` per 1000 words** | 0.28 | — | **6.67** | 24× |
| **% of clauses opening with an adjunct** | 29.5 | 25.4 | **13.6** | and the slot holds enumerators, not connectives |

They are one defect seen five ways. The corpus states a sequence of facts. It does not connect
them, it does not mark which are concessions or instances, and it restates its referents through
possessives instead of naming them. The reader has to rebuild the argument.

The failing sentence the project owner flagged carries four of the five at once:

> "These are large and well-resolved effects of limited practical consequence, because the
> attribute is of very low criticality and its acceptance criterion is applied as an upper limit
> that lies far above the observed range."

Root verb `are`; predicate a noun; three nominalisations on four stacked prepositions; a bare
demonstrative subject whose antecedent is a table; two possessives. A-Mab's version of the same
argument gives the number that settles it in the same sentence that raises the doubt.

## 2. What the defect is NOT, and this bounds the work

Eight hypotheses were tested and returned null. Each would have produced a plausible-sounding rule
that made things worse or changed nothing:

| Hypothesis | Result |
|---|---|
| sentences too long or too complex | corpus is **simpler** on every structural measure: tree depth 6.99 vs 7.75, PP nesting 1.31 vs 1.37, compounds 1.02 vs 1.30 |
| word order is inverted | subject-before-verb **100 %** of clauses in A-Mab, 99.9 % in PDA, 99.7 % in PCR-003; **zero** fronted objects anywhere |
| over-nominalised | corpus does nominalisation+`of` at 4.4/1k against the sources' 8.9 and 9.0 — half as often |
| formulaic and templated | repeated 4-grams 47.6/1k against A-Mab's 66.5; 136 distinct against 405 |
| over-claiming | boosters 7.0/1k against 10.0–10.2. The corpus under-commits **and** under-hedges |
| narrates tables as lists | coordination chains identical, 0.72–0.95 both sides |
| too few numbers in prose | 2.6 per 100 words against A-Mab's 5.3 — but this is not obviously a defect |
| punctuation ornament (semicolons, colons) | real gaps, but ornament: a floor would be gamed, not met |

**So nothing in `check_style.py`'s thirteen thresholds addresses the defect, and adding thresholds
of the same kind will not either.** Every document passes all thirteen today.

## 3. The cause is in the repository, not in the authors

- **`WRITING_GUIDE.md` §2c and §2d forbid the shapes that carry an argument.** "One paragraph, one
  point", "One sentence, one point; if a sentence carries two claims, make it two sentences." A
  concession needs a claim and its counter-consideration together; an instance needs a rule and an
  example. Both are two points. The authors complied.
- **`check_style.py` caps `therefore` at 1.2 per 1000 words** — the only connective the corpus
  still uses — and says nothing about the eight the guide recommends.
- **§2d already states the topic-chaining rule** — "Begin with information the reader already has
  and end with the new information" — and it is met in 35 % of sentences. That makes it a rule to
  **exemplify and check**, not to invent, which is the cheapest fix available here.
- **`REGISTER_EXEMPLAR.md` has no plan-genre passage**, and 10 of the 20 documents are plans. The
  exemplar is built from a technical report and a case study.
- **Neither of the two sources that would supply plan-genre prose is extracted.**
  `scripts/extract_sources.py` has two entries in `SRC`; four documents sit in
  `$SYNTHETIC_DATA_SOURCES`.

## 4. Three corrections to the proposal as first written

**4a. The licensing answer was wrong, and the question is now smaller.** `--selftest` reads
`refs/text/`, which is **committed** (`git ls-files refs/`; `.gitignore:222` says so
deliberately). So measuring the ISPE guides is not free of redistribution unless the extract is
read from `$SYNTHETIC_DATA_SOURCES` and skipped when absent, which `selftest()` already does for a
missing file (`check_style.py:315`). Only two acts are blocking: committing an ISPE extract to
`refs/text/`, and quoting ISPE prose into `REGISTER_EXEMPLAR.md`. **Since the mechanism is now
prose rather than thresholds, the ISPE guides are wanted for their plan-genre passages — the
blocked act is exactly the one this unit needs.**

**4b. Re-authoring PCR-003 erases discrepancy D-002, and nothing would notice.** D-001 is safe:
four plans carry it (PCP-003/006/008/009) and `section_plan.yaml:315,535` instructs the author to
write the commitment. D-002 is PCR-003's absolute claim about the bioreactor, and it is carried by
**nothing**: `build_brief.py` emits seven sections and none is discrepancies,
`authoring/discrepancies.yaml` does not exist on `main` (it is on the weak-claims branch), and no
gate reads `DISCREPANCIES.md`. Its annex half lives in `build_ground_truth.py:242` and is
generated, so a re-author erases the prose half only — leaving the annex asserting a claim the
document no longer makes, which is worse than losing it cleanly.

**4c. The pilot choice is safe, by luck.** PCP-003 is a D-001 document, and D-001 survives because
the section plan states it. The plan must check the same for any second document rather than assume
it.

## 5. Layers, and what a change costs

| Layer | Files | Cost |
|---|---|---|
| machinery | `WRITING_GUIDE.md` §2c/§2d/§4, `REGISTER_EXEMPLAR.md`, `section_plan.yaml`, `check_style.py`, `scripts/extract_sources.py` | cheap, and it is where the fix lives |
| document | one `.qmd` per re-author, one pass each | 3,372–10,679 words each; **119,453 words across all 20** |
| annex | `build_ground_truth.py` re-anchor per re-authored document | of 2,084 quotes corpus-wide |
| model | none | no number moves, so no `make data figures` |

Re-authoring twenty documents is a campaign, not a task. The pilot is what keeps that decision
honest.

## 6. Ground rules that bite here

- **Prose changes mean a one-pass re-author of the whole document.** Never a paragraph patch.
- **Never read a sibling `.qmd` for voice.** This unit is about voice, so the rule is
  load-bearing: every instruction must come from the human sources.
- **Registered discrepancies.** §4b. D-001 is carried, D-002 is not.
- **Nothing is added to a document after authoring.** The register fix is authored in.
- **`annex_contract/` and `nlp_reports` are read-only.** Neither is in scope.
- **`weak_claims` stays empty on `main`.** If the brief gains a discrepancy section from the
  feature branch, it must come without the weak-claims half.
- **No number moves**, so `outputs/` must not change.

## 7. Hazards

1. **Every new rule is gameable.** An author told to produce `However` will produce `However`.
   Topic chaining, connective counts and copula rate are diagnoses. They must not reach an author
   as targets, and the acceptance test has to be whether a reader can tell a corpus passage from a
   source passage.
2. **Relaxing §2c invites the sprawl back.** The first-pass corpus ran a 34-word mean with an
   em-dash aside in every third sentence. The exception must be narrow: a claim and its
   counter-consideration, not a licence for long sentences.
3. **spaCy is not a project dependency**, and the analyses were run through
   `uv run --with spacy --with <model wheel>`. If any of this becomes a gate, that is a new
   dependency plus a 12 MB model. It does not have to: the findings can stay diagnostic.
4. **A mined quote can be an extraction artifact.** One of 25 failed a verbatim check because it
   spanned a page break and `prose_from_extract` joins across the running header.
   `check_exemplar_quotes.py` is the gate any exemplar addition must pass.
5. **Re-authoring drifts the committed `.docx`.** Draft under `<DOC>_<uokey>.DRAFT.qmd`.

## 8. Open questions

1. **Blocking.** May the ISPE extracts live outside the repository and be read when present, and
   separately, may ISPE passages be quoted into `REGISTER_EXEMPLAR.md`? The second is what the
   plan-genre exemplar needs. If the answer is no, the fallback is to build the plan-genre exemplar
   from PDA TR 60's protocol sections, which are thinner but unencumbered.
2. **Blocking.** Does D-002 get a carrier in the brief, or does PCR-003 stay out of scope?
3. Which source is the reference for which document type? PDA hedges at 24.5 per 1000 words because
   it is guidance; A-Mab sits at 6.6 and is the closer genre for a report. The plan should say so
   rather than average them.

## 9. What a plan needs to contain

In this order, because each step's result decides whether the next is worth taking:

1. Amend `WRITING_GUIDE.md` §2c/§2d to license the tension pair, with the shapes named.
2. Add the moves catalogue to `REGISTER_EXEMPLAR.md` from `mined-patterns.md`, all quotes passing
   `check_exemplar_quotes.py`.
3. Exemplify §2d's existing given-new rule, which is the cheapest win on the list.
4. Remove the `therefore` ceiling, or pair it with the other eight connectives.
5. Extract the remaining sources, subject to question 1.
6. Pilot: re-author PCP-003, then measure and read it.
7. Decide scope for the remaining nineteen on the pilot's result, not in advance.
