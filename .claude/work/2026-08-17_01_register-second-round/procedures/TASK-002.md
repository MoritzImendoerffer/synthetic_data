# TASK-002 procedure — the guide's rule as a substitution, and the examples

Read `state.json` → `TASK-002` first. **Owner decision: minimum edits.** You change the rule text,
the ✓ blocks that teach the fault, and add the examples listed. You do not re-author the guide's
commentary. Line numbers below are as of 2026-08-17; re-check with `grep -n` before editing.

Draft texts are given so you do not have to invent them. Adapt wording if the file around it has
moved; do not change the numbers.

## 1. §2d — replace the rule (lines 157–159)

Current:

> Begin with information the reader already has and end with the new information. Keep the
> subject next to its verb. One sentence, one point; if a sentence carries two claims, make
> it two sentences.

Replace with:

```markdown
Begin with information the reader already has and end with the new information. Keep the
subject next to its verb. **One argument step per sentence.** When the next step is a
consequence, a contrast or a recommendation, end the sentence and open the next one with the
connective: "Therefore, …", "However, …", "As a result, …", "For this reason, …". Do not join
the steps inside one sentence with ", so …" or with ", and …" carrying a second claim, and do
not carry a new claim in a ", which …" clause.

**This is a substitution, so check it in your draft.** Search for `, so ` and for `, and ` that
introduces a second clause. Each one is a place where the sources would have written a full stop
and a connective. Measured over the pages the self-test reads (2026-08-17): the four sources
carry a mid-sentence ", so " in 0.1 to 0.4 % of their sentences and open 3.7 to 6.1 % of their
sentences with a connective. The corpus carries ", so " in 6 to 11 % of sentences and opens 0 to
2 % with a connective. `check_style.py` prints both figures on every run, and neither is gated.
```

Then add, directly after that paragraph, the worked correction from the owner's sentence:

```markdown
**Correction 0 — three steps in one sentence.** From `PCR-003`, *Discussion*, as it stood on
2026-08-17. The project owner quoted it as "hard to understand, too many arguments in one
sentence, including a recommendation in the last part":

> ✗ The lack-of-fit tests rest on `` `{python} f"{cp_rsm}"` `` centre-point replicates, so a
> non-significant result bounds the evidence for the model form without establishing it, and
> `` `{python} lof_p_lo_resp.lower()` `` is the case to watch (p = `` `{python} f"{lof_p_lo:.2f}"` ``).

A premise, a consequence and a recommendation, joined by ", so … , and …". The reader has to hold
all three to the end.

> ✓ The lack-of-fit tests rest on `` `{python} f"{cp_rsm}"` `` centre-point replicates.
> Therefore, a non-significant result bounds the evidence for the model form without
> establishing it. The weakest case is `` `{python} lof_p_lo_resp.lower()` `` (p = `` `{python} f"{lof_p_lo:.2f}"` ``),
> and it is the one to watch at scale.

Three sentences, one step each. Note the third: the response name is a runtime value, so it is
never the subject of a verb that has to agree with it ("acidic variants is the case to watch"
came from exactly that). Put a runtime name after "is" or after a preposition, never before the
verb.
```

## 2. §2d — the referent rule (add after Correction 3, before §2d bis)

```markdown
**Name the set you count.** "The four that matter", "both", "the three" ask the reader to bind a
number to things named somewhere else. If the paragraph has not named them, the sentence does.
From `PCR-003`, *Discussion*, as it stood on 2026-08-17 (the four factors were last named 270
lines earlier):

> ✗ … a screening design that ranked the factors and a response-surface design that models the
> four that matter.

> ✓ … a screening design that ranked the five factors and a response-surface design in the four
> that screening retained: culture pH, temperature, culture duration and dissolved CO2.
```

## 3. §2d Correction 2 — the ✓ block that teaches the fault (lines 208–211)

Current ✓:

> ✓ The remaining attributes sit far from their limits, so the capability indices show only that
> none of them constrains the process. The furthest is leached Protein A, at …-fold below the
> limit, and @tbl-cap reports its index for completeness.

Replace the first sentence so no ✓ block in the guide models mid-sentence ", so ":

```markdown
> ✓ The remaining attributes sit far from their limits. Their capability indices therefore show
> only that none of them constrains the process. The furthest is leached Protein A, at
> `` `{python} f"{lpa_ratio:,.0f}"` ``-fold below the limit, and @tbl-cap reports its index for
> completeness.
```

Then run this and read every hit; none may be inside a `> ✓` block anywhere in the guide:

```bash
grep -n ", so " authoring/WRITING_GUIDE.md
```

(Hits inside `> ✗` blocks and in source quotes are fine. Hits in the guide's own commentary are
left alone by owner decision — do not rewrite them in this task.)

## 4. §2d bis — name the substitution and bound the target (lines 232–262)

After the **Rule.** paragraph, add:

```markdown
**The substitution is the definite article or the noun, and never "it is".** Round one of the
register pilot applied this rule two ways. `PCR-003` replaced possessives with articles and
nouns and its copula rate barely moved. `PCP-003` replaced 25 possessives with 23 expletive
subjects ("it is", "it was", "it will be" went from 7 to 21) and its copula rate rose from
18.4 % to 27.6 %, outside all four sources. Same rule, opposite cost.

**The target is a band, not a minimum.** The sources sit at 0.27 to 0.40 *its* and 0.50 to 0.96
*their* per 1000 words. Aim inside those bands; a document at 0.02 has driven out the licensed
exception too, and paid for it somewhere else.
```

## 5. Shape 4 — a positive worked correction (after line ~345, the existing ✓ of the deletion example)

Add a second correction that *writes* a front field instead of deleting one. Pick a sentence from
`PCR-003` or `PCP-003` as they stand on 2026-08-17 that states a consequence and could open with
a condition or connective. A ready candidate from `PCR-003` §2.2 (Response-surface design), dated:

```markdown
**Second correction — write the frame instead of deleting one.** From `PCR-003`, *Response-surface
design*, as it stood on 2026-08-17:

> ✗ The response-surface model does not carry osmolality, so the interaction between temperature
> and osmolality that screening resolved on galactosylation (@tbl-eff-gal) is represented in
> this report by the screening estimate alone.

> ✓ Because the response-surface model does not carry osmolality, the interaction between
> temperature and osmolality that screening resolved on galactosylation (@tbl-eff-gal) is
> represented in this report by the screening estimate alone.

The condition moves into the front field and the main clause is the claim. One word changed and
the sentence now has the shape 29.5 % of A-Mab's clauses have.
```

Verify the ✗ text is verbatim in the current file before quoting it:
`grep -n "does not carry osmolality, so" pc_package/PCR-003_bioreactor.qmd`.

## 6. §4a — two diagnostic rows (table under line ~413)

Add after the two existing *diagnostic* rows:

```markdown
| *Sentences with a mid-sentence ", so " — not gated* | *diagnostic* | *0.1 %* | *0.3 %* | *0.4 %* | *0.4 %* |
| *Sentences opening with a connective — not gated* | *diagnostic* | *4.8 %* | *6.1 %* | *4.2 %* | *3.7 %* |
```

and one sentence under the table's existing note: "The two clause-packing rows were added on
2026-08-17; the corpus measured 6–11 % and 0–2 % on them, and round one of the register pilot
made both worse. They fail nothing."

## 7. §4b "Prefer plain connectives" (lines 490–499) — say where it goes

Append to that paragraph:

```markdown
And say where the connective goes: at the head of the sentence, after the full stop that ends
the previous step. The sources open 3.7 to 6.1 % of their sentences that way; the corpus opens
0 to 2 %, and puts the same step after a comma instead (", so …" in 6 to 11 % of sentences).
```

## 8. REGISTER_EXEMPLAR.md — three verbatim two-sentence quotes

Add under `## The connective inventory` (line ~666), a sub-heading **"The step after the full
stop"** with at least three of these (checked verbatim on 2026-08-17 by the same extraction the
checker uses; the checker prints the page):

```markdown
> At an early stage of process development, the information available on product attributes may
> be limited. For this reason, the first set of CQAs may come from prior knowledge obtained
> during early development and/or from similar products rather than from extensive product
> characterization.
> — PDA TR 60

> The specifics of the CPV sampling/testing strategy may not be finalized until completion of
> PPQ. Therefore, the process validation master plan may include general commitments to the
> planned CPV strategy.
> — PDA TR 60

> Results also showed that there are no Critical Process Parameters (CPPs) in Step 3 since all
> parameters are well controlled within their acceptable limits and have demonstrated robust
> process operation. Thus, all quality-linked process parameters for Step 3 were classified as
> WC-CPPs.
> — A-Mab

> In many regulatory regions, a minimum of three successful, consecutive lots are used. However,
> other regulatory bodies may accept more (or less) lots depending on the knowledge available for
> the product.
> — ISPE Technology Transfer
```

All four were re-verified verbatim on 2026-08-17 (whitespace-collapsed substring of the extract).
Extract pages: PDA quote 1 → `PAGE 21` (printed p. 13), PDA quote 2 → `PAGE 52` (printed p. 44),
A-Mab → `PAGE 87` (p. 87), ISPE TT → `PAGE 95` (printed p. 93). Write the attributions the way
the file's other entries do (`— A-Mab, p. 87`; `— PDA TR 60, printed p. 13 / extract p. 21`;
`— ISPE Technology Transfer, printed p. 93 / extract p. 95`). Then:

```bash
uv run python authoring/check_exemplar_quotes.py | tail -5      # every quote verbatim, exit 0
```

If a quote fails, it spans a page break or a hyphenated line; pick another from
`clause_pack.py`'s style of search (see exploration §4) rather than editing the words.

## 9. Gates

```bash
make style PY="uv run python" | tail -3        # exit 0
```

## 10. Done when

Every acceptance line in `state.json` → `TASK-002` is true. Record in `outcome` the line numbers
of each edit and the checker's page numbers for the new quotes.
