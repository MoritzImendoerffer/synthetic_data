# The corpus states facts. It does not argue. — what remains

**Status: partly delivered 2026-08-17; Track 1 being worked on since 2026-08-17 in work unit
`2026-08-17_01_register-second-round`.** Work unit `2026-08-16_01_register-from-four-sources`
shipped nine of its ten tasks, and this proposal is rewritten down to what is still open rather
than deleted, because 18 of 20 documents have not been touched. The second unit opened after the
project owner read the re-authored `PCR-003` and named a defect the pilot did not measure; its
`exploration.md` records the reading and the count that confirms it.

Raised by the project owner: "currently, the prose is written in a way no SME would write", and on
one passage, "hard to read, nearly not understandable, makes vague statements formulated not like a
scientific text is formulated".

**What shipped** — measurements in
[`docs/results/2026-08-17-register-pilot.md`](../results/2026-08-17-register-pilot.md):
all four published sources extracted and the register band recalibrated on them; the `therefore`
ceiling removed and nine connectives counted as a diagnostic that fails nothing;
`WRITING_GUIDE.md` §2c/§2d/§2d bis amended to license a claim beside its counter-consideration
and to state the given-new and possessive rules with worked corrections; a seven-pattern
argument-moves catalogue in `REGISTER_EXEMPLAR.md`, 120 verified quotes from four sources;
`authoring/discrepancies.yaml` plus brief §5c, so a re-authored document keeps its registered
discrepancies; and **`PCP-003` and `PCR-003` re-authored, promoted, re-anchored and measured**.

## What the pilot found

Scored honestly, the amended artifacts produced **one clean win in five**. The connective
repertoire went from 3 of 9 distinct to 6 of 9 in both genres. Possessives moved furthest and
**should not be counted**: fourteen times the source rate is 69 instances in 10,354 words, one
every 6.3 sentences, which no reader experiences as a defect — the project owner read the report
and said so — and removing them cost the plan 23 added copulas. Topic chaining, copula rate and
adjunct front field did not move. Chaining fell in the report and copula rose in the plan.

The explanation is not lexical-versus-discourse. §2d taught the given-new rule with three worked
corrections and §2d bis taught the possessive rule the same way, in adjacent sections of the same
guide, and only one landed. **An author can execute and self-verify a substitution and cannot
self-verify a rate.** The connective repertoire is the confirming case: a discourse property that
moved, because `check_style.py` prints the distinct count back to the author on every run. So the
lever is feedback at write time, not more examples in the guide.

**This does not refute the discourse hypothesis.** The shapes the guide taught as substitutions
moved and the shapes it taught by example did not, which points at how the guide teaches rather
than at what it claims. It does mean the next step is machinery, not prose.

## Track 1 — a second two-document round

**Do this before the eighteen.** Six tasks changed the guide, the exemplar, the gate and the
brief, and nobody knew what any of it did until a document was written and measured. Committing
eighteen documents to two untested amendments repeats exactly that, at nine times the cost.

Same two documents: they are already split from the corpus, both genres stay covered, and a third
measurement is directly comparable to the two on the results page.

1. **`authoring/check_discourse.py`** — chaining, copula and front field with denominators and
   the four source columns, reusing `check_style.prose_from_qmd` / `sentences` / `HUMAN_SOURCES`
   so it measures the same text the gate does. **Advisory, never a gate.** A floor on chaining is
   met by typing a pronoun, which is the failure this proposal already documented once.
2. **A discourse section in the brief.** §5d is free — the brief runs 5, 5c, 6. The targets
   matter less than the worked chains, which `build_brief.py` can generate **from the document's
   own grounded facts** instead of quoting another document. Pre-authoring, so it respects the
   rule that nothing is added to a document afterwards.
3. **§2d bis names the substitution and bounds the target** — the definite article or the noun,
   never `it is`, and a band rather than a minimum, so the licensed exception shows up in the
   numbers instead of being driven out of them. The one fix with direct evidence behind it.
4. **Shape 4 gains a positive front-field example.** The current worked correction only deletes a
   bad one. Cheap, and not expected to carry load alone.

Then re-author both **in one pass each** with the numbers in the brief. Never patch: a second
one-pass author is not post-editing, it is what TASK-007 already did.

**Stopping rule, fixed before the round runs:**

- **Go to Track 2** if chaining clears roughly 45 % in *both* genres and neither copula nor front
  field regresses.
- **Stop and change the target** otherwise. That would mean the discourse hypothesis is not
  reachable by authoring instructions, and the better target is the tell the pilot found by
  reading rather than by measuring: the corpus reads as *edited* and A-Mab reads as *written*.
  Every corpus paragraph is a finished three-sentence argument, while A-Mab drops a bare label
  mid-paragraph, repeats itself and leaves a claim half-supported. No measure here covers that.

## Track 2 — the remaining eighteen

Blocked on Track 1. Budget roughly **40 annex spans re-anchored per document** — the pilot needed
80 across two, of which 34 were `PCR-003`'s curated rhetorical layer — plus a `check_render.py
--render` and a separate PDF render each. `check_render.py` renders only the `.docx` and
glyph-checks whatever `.pdf` is already on disk, so the PDF must be rendered explicitly or the
glyph check reports on a stale file.

The corpus stays split on register until this finishes, which is the argument for not leaving
Track 1 open for long.

## What this deliberately does not do

It does not add a syntactic gate. The measures stay diagnostic unless a later decision says
otherwise, for the reason above: a metric that becomes a target is met by typing the word.

It does not patch paragraphs, and it does not change what any document claims. Both registered
discrepancies survived the pilot and were re-verified against the new text (D-001 in `PCP-003`,
D-002 in `PCR-003`); `authoring/discrepancies.yaml` is what keeps them alive across a re-author.

It does not import the sibling repository's writing standard wholesale. Two of its rules — "if a
sentence needs a semicolon, make it two sentences" and "should read like a checklist, not an
essay" — point at the floor this corpus is already stuck at.

## Open questions

1. ~~**Blocking Track 1. Does spaCy become a dependency?**~~ **Answered by the project owner,
   2026-08-17: yes, as an OPTIONAL dependency.** Not a hard one — the corpus must still build,
   render, annex and ground on a checkout that has never installed a parser. What that commits
   the implementation to:
   - an optional group in `pyproject.toml` (`[project.optional-dependencies]`, e.g. `discourse`),
     installed with `uv sync --extra discourse`, carrying spaCy and the `en_core_web_sm` model.
     The model is a wheel URL, so it needs a direct reference rather than a plain version pin.
   - the same group mirrored in the pip path, since `CLAUDE.md` requires the two declarations to
     agree. A separate `requirements-discourse.txt` keeps `requirements.txt` installable
     unchanged; a marked optional block inside it would also do.
   - **`check_discourse.py` must degrade, not fail.** With spaCy absent it prints one line saying
     how to install the extra and exits 0. It is advisory, so nothing in `make test`, `make style`
     or `make corpus` may start depending on a parser being present.
   - `uv.lock` is regenerated when the group lands. Land it **with** `check_discourse.py`, not
     before: a lock change with no consumer is churn on the tested path.
2. ~~**The discrimination test still has no valid result, so the acceptance test of this proposal
   is unmet.**~~ **Answered by the project owner, 2026-08-17: the discrimination test is dropped
   as the acceptance criterion.** Three rounds scored 64 of 64 and every round was decided by
   something other than register, and the owner's own reading of the re-authored `PCR-003` was
   that "it is immediately obvious that the text is AI generated" — so a blind test would score
   at ceiling and add nothing. The human check for Track 1 is the owner reading the re-authored
   pair and quoting what gives it away, as recorded in work unit
   `2026-08-17_01_register-second-round/exploration.md` §9. Two further decisions taken there:
   clause packing (mid-sentence `, so `, sentence-initial connectives) is the round's primary
   target and topic chaining a no-regression condition; and the guide is amended minimally
   (§2d Correction 2, Shape 4), with a full rewrite of its commentary held as a hypothesis.
3. Which source is the reference for which document type? PDA hedges at 24.5 per 1000 words
   because it is guidance. A-Mab sits at 6.6 and is the closer genre for a report.
