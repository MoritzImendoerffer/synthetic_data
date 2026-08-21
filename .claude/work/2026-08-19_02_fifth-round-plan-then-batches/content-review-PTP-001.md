# Content review of the PTP-001 draft — before promotion

**2026-08-21, TASK-033 §4.** Batch B5, authored under the amended rule 4. PTP-001 is a corpus-level
document with no single unit operation, so its brief carries no §2b, and §5c assigns no registered
discrepancy. Fresh judges (`opus`), one return between them.

## Counts per question

| run | Q1 | Q2 | Q3 | Q4 | verdicts |
|---|---|---|---|---|---|
| 1 (as authored) | 5 (2 physical, 3 weak) | 0 (3 close calls) | 2 | 6 (4 borderline uncounted) | No · **Yes** · No · Yes |
| 2 (after one cycle) | 4 (3 borderline) | 0 prose (1 table cell) | 0 (2 navigational) | **0** (3 borderline) | No · **Yes** · **Yes** · **Yes** |

**Question 4 passes — the first time in this campaign.** Every document of every batch before this
one answered "yes" to question 4, meaning the defect was present. PTP-001 run 2 answers **no**: the
judge found no sentence that files its own finding, and wrote that the document "contains none of
the usual filing moves — no 'which highlights', no 'this is a classic case of', no 'importantly', no
trailing appositive renaming a result as a category." Three of the four questions now pass.

The carrier fell with it: `rather than` went from 15 occurrences to 4, and the run-1 judge had named
that construction as the vehicle for five of its six question-4 hits.

**Question 2 passed on the FIRST run**, which before this batch only `PCP-010` had managed. The
judge named "verification-qualified", "pressure history" and "control capability" as its closest
calls and let all three stand as descriptive phrasings rather than invented concepts.

## The judge scoped question 1 itself, again

Unprompted, and independently of every earlier judge that has done so: it separated causal claims
from documentary ones, ruled that all seven uses of "govern" take documentary objects and are "the
governance sense, standard in this literature, not a suppressed mechanism claim", and set aside
three table cells as "compressed table labels, not sentences". It then reported five failures of
which it called two "the physical ones and the substantive failures". It also ran its own cue-word
census before answering: `because` ×9, `since` ×0, `govern(s)/governed` ×7, `set(s)` ×8 plus 3
table cells, `acts on` ×2, `acts through` ×0.

That is now the pattern across this campaign rather than an observation about one document: the
question as written over-fires on procedural and documentary uses, and capable judges keep
supplying the scope line it lacks.

## Run 1 — the judge's report, verbatim

Model: Claude Opus 5 (`claude-opus-5`). Read: all 26 pages of
`pc_package/PTP-001_None.DRAFT.pdf` and nothing else.

### Question 1 — causal verb must carry its cause in its own clause

Reading applied: where the verb makes a causal claim, the cause must sit in the clause. Seven of the nine `because` clauses do name their cause in-clause with a direction (e.g. "because central preparation introduces a hold before use that laboratory preparation does not have"). These fail:

- **"Scale acts on mixing, on gas transfer and on the accumulation of dissolved carbon dioxide in cell culture, and it acts on the residence time and the pressure history of the chromatography and filtration steps."** (p. 11) — Fails Q1: names five things acted on but no interaction and no direction in either clause; larger scale does *what* to mixing is never stated.
- **"Because the mechanisms differ, the three claims are independent and are added (International Council for Harmonisation 2023a)."** (p. 17) — Fails Q1: the mechanisms live in the preceding sentence; the because-clause names no species, no interaction, no direction, only the word "mechanisms".
- **"The first two gaps set the schedule."** (p. 20) — Fails Q1: "set" with the cause deferred to the next sentence.
- **"The characterization work sets the duration of the transfer."** (p. 24) — Fails Q1: same shape; the PCMR-001 dependency that actually sets the duration arrives in the following sentence.
- **"Afucosylation, galactosylation, high mannose and the charge variants are set in cell culture."** (p. 8) — Fails Q1 (weakest of the five): names a location, not a property of the culture or a direction.

Not counted as failures: the seven `govern` instances all take documentary objects (ICH guidelines governing how a design space is defined, SOPs governing qualification and classification). That is the governance sense, standard in this literature, not a suppressed mechanism claim. The three Table 2.1 cells ("sets leached Protein A", "sets the cumulative XMuLV (enveloped) clearance", "sets the cumulative MVM clearance") are compressed table labels, not sentences.

### Question 2 — every technical term a term of art

No failures. Everything load-bearing checks out against the chromatography, cell-culture and virology literature: WC-CPP / KPP / GPP and the criticality continuum are A-Mab case-study terms; modular viral clearance claims, flow-through mode, removal by size and low-pH inactivation are ICH Q5A; intermediate precision, LOQ and TCID50 are analytical terms of art; scale-independent versus scale-dependent variables, linear velocity, bed height, filtration flux, viable cell concentration and titre are all standard.

Closest calls, none of which is an invented concept: "verification-qualified" (Table 6.2, a status label built from method verification), "pressure history" (p. 11, descriptive English where "pressure profile" is the usual phrase), and "control capability" (p. 11, extrapolated from process capability).

### Question 3 — each sentence in a mechanism paragraph disagreeable on its own

The mechanism paragraphs are p. 7 (glycan/ADCC), p. 8 (where attributes are formed and cleared), p. 11 (scale), p. 12 (model qualification) and p. 17 (viral safety). Two sentences fail:

- **"Scale acts on mixing, on gas transfer and on the accumulation of dissolved carbon dioxide in cell culture, and it acts on the residence time and the pressure history of the chromatography and filtration steps."** (p. 11) — Fails Q3: with no direction or magnitude asserted, there is nothing here a reader could hold to be false.
- **"Because the mechanisms differ, the three claims are independent and are added (International Council for Harmonisation 2023a)."** (p. 17) — Fails Q3: its premise is a back-reference, so the sentence cannot be judged without the sentence before it.

The rest hold up. "The low pH hold inactivates enveloped virus, the anion exchange step removes both enveloped and small virus in flow-through mode, and the small virus retentive filter removes small virus by size" is three separately contestable mechanism claims in one sentence, and is the strongest sentence in the document.

### Question 4 — telling the reader how to file the finding

Six sentences do this, five of them through a trailing `rather than` gloss:

- **"Where the receiving site cannot hold a parameter inside the NOR that characterization assumes, either the range must be widened by further study or the equipment must be changed, and the case is recorded as a gap in §8."** (p. 11) — Fails Q4: trailing clause renames the situation "the case" and files it into §8.
- **"For these two steps the ranges will rest on univariate work and on platform experience rather than on a designed experiment, and that limitation is recorded as a gap in §8."** (p. 13) — Fails Q4: renames the fact just stated as "that limitation" and files it.
- **"It is recognized that a campaign of this size cannot capture the full variability of commercial manufacture, which is why continued process verification follows it rather than replacing it."** (p. 18) — Fails Q4: causal gloss answering an objection nobody raised, since nobody proposed that CPV replaces qualification.
- **"PCMP-001 plans the characterization campaign that produces the evidence and PCMR-001 consolidates it, so both documents are prerequisites of the qualification campaign rather than deliverables of it."** (p. 18) — Fails Q4: trailing clause recategorizes the two documents after the substantive point is already made.
- **"The gap on harvest and UF/DF is the one gap that will remain open in substance after the campaign, because it is a property of the characterization design rather than of the transfer."** (p. 20) — Fails Q4: causal gloss that reclassifies the gap instead of explaining it.
- **"Equipment qualification, utility qualification, method transfer and operator training are all in that category, and each of them appears in Table 10.1 with this plan rather than a report as its dependency."** (p. 24) — Fails Q4: literally files four items into "that category", then files them again into a table row.

Borderline, not counted: "The comparison is prospective, so each row states what will be compared and how a difference will be managed rather than a measured outcome" (p. 10), "The order is a dependency order rather than a calendar" (p. 23), "The division is a division of work rather than of accountability" (p. 9), and "The cumulative clearance across the train is stated only in PCMR-001, and no single step report claims it" (p. 8). Each is doing real scoping work for a plan document, but all four share the tic's shape.

The construction is the carrier: `rather than` appears about fifteen times in 26 pages, and every Q4 hit but one rides on it.

### Verdicts

1. **No.** Five causal verbs do not carry a cause in their own clause; two of those ("acts on", "Because the mechanisms differ") are the physical ones and are the substantive failures.
2. **Yes.** Every technical term is a term of art; the three closest calls are descriptive phrasings, not invented concepts.
3. **No.** Two sentences in mechanism paragraphs cannot be contested standing alone.
4. **Yes** — meaning the defect is present. Six sentences tell the reader how to file the finding they just stated.

## Disposition

Returned to the same authoring agent, in its own context, with the flagged sentences as what each
lacks and the questions restated. No counts and no phrase to insert were passed, and question 2 was
passed on with nothing asked of the author, since it read yes.


## Run 2 — the judge's verdicts

Model: Claude Opus 5 (`claude-opus-5`), a second fresh judge, 26 pages, nothing else opened.

1. **No.** Four sentences use "acts through", "set by" or "since" without a directional physical cause in the verb's own clause; two defer the direction to the following sentences, and one gives a reason that does not support the sign it claims.
2. **Yes** for the prose. One non-standard label, "verification-qualified", appears in a Table 6.2 cell.
3. **Yes.** Every sentence in every mechanism paragraph makes an independently contestable claim; only two closing cross-references carry no mechanism.
4. **No.** No sentence files its own finding; the three closest cases are reading instructions or conceded limitations that the surrounding text uses.

The judge also classified about a dozen uses of the trigger words as documentary, scheduling or
logical rather than physical — "This plan governs the transfer…", "ICH Q9 governs the risk
assessment…", "The first two gaps set the schedule, because each requires laboratory work at a site
that has not yet performed it" — and did not flag them, saying each "names a real, checkable reason
in its own clause". That is the same scope line judges have supplied unprompted throughout this
campaign.

## THE REVISION INTRODUCED TWO PHYSICS ERRORS, AND A THIRD PASS FIXED THEM

Both sentences were checked against the pre-review draft and neither is in it. The review cycle
traded vague-but-not-wrong prose for confident-and-wrong prose, which is the same failure mode
`PCP-010` produced when its revision introduced a contradiction with the document's own absolute
claims.

**1. Oxygen transfer.** The revision wrote: *"Oxygen transfer moves with it, since the same
interfacial area per unit volume carries both gases."* The sentence before it establishes the
opposite sign — carbon dioxide stripping falls in a deeper column because a bubble comes closer to
equilibrium — and that same mechanism predicts MORE oxygen delivered per bubble. The stated reason
argues against the claim.

**2. Deamidation.** The revision wrote: *"Acidic charge variants accumulate through deamidation,
which proceeds faster the longer the product sits at culture pH and temperature."* Deamidation
proceeds faster at higher pH and temperature; sitting longer raises the extent, not the rate.

**The owner authorised one more pass for these two sentences only**, overriding
`decisions.one_review_cycle` for this document. The precedent is `PCP-010`, whose physics error was
corrected inside its cycle "because it is a correctness matter rather than a style preference". The
pass was scoped to the two named sentences and nothing else.

What the author did with them is the part worth keeping. On oxygen it **declined to assert a
direction it could not establish**, which is exactly what it should do: the sentence now says oxygen
crosses the same interface in the opposite direction so a change in the gas path does not act on the
two transfers in the same way, and lands the consequence on qualifying the two transfers separately.
On deamidation it split rate from extent and noted that the result stays consistent with the anion
exchange canon, where an extended neutralized hold raised the acidic charge-variant burden as an
extent effect.

After the pass: all hard gates pass, five tics 0.0, 0 `<<NEEDS>>`, 0 typed measurements, fresh pdf
with no missing glyphs, 26 pp, 189 sentences and 3,570 words (was 187 / 3,520; the growth is the two
added sentences). `rather than` still 4.

## Findings recorded, not acted on

- **"verification-qualified"**, the judge's one question-2 flag, is generated table content: it comes
  from `outputs/data/dev_methods.csv`, verified. It is a data-level label rather than authored prose,
  so rewording it in the document would put the table at odds with its source.
- Four question-1 sentences survive, three of which the judge itself called borderline.

## Disposition

Two review runs plus one owner-authorised correctness pass. Three of the four questions pass, and
question 4 passes for the first time in the campaign. The document proceeds to the batch B5 annex
task. Nothing is added to it after this point.
