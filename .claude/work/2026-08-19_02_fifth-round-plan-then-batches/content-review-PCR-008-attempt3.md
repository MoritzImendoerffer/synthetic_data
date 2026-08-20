# Content review of the PCR-008 draft, attempt 3 — before promotion

**2026-08-20, TASK-046 §4.** Third attempt at `PCR-008`, and the **first authored under the amended
rule 4** of `WRITING_GUIDE.md`. Attempt 1 and attempt 2 both lost their blind readings to the
round-zero text. Two fresh judges (`opus`, self-reported Claude Opus 5), the four Content questions
verbatim, the rendered PDF and nothing else, with one return in between.

## Run 1 — as authored (`PCR-008-attempt3.DRAFT.pre-review.qmd`, 56 pp)

**Q1 No · Q2 No · Q3 No · Q4 Yes.** Flags: Q1 20, Q2 8, Q3 7, Q4 17.

Q1 fell in four families: bare "govern / sets / is set by" whose mechanism is in the next sentence
("Load pH and the equilibration and wash-1 conductivity govern pool host cell protein.", exec
summary and §12); "acts on / acts by" pointing at an abstraction ("All four act on the same binding
equilibrium…"); "because" clauses giving a procedural, statistical or regulatory reason; and clauses
where the cause is present but the direction is missing ("Operating flow rate sets the residence
time…").

Q2: "the ionic-strength argument", "binding attribute" and an attribute that "rejects" a region,
"common-mode offset", "assurance margin", "quality-linked", "the cumulative MVM position",
"governed attribute", "dense acidic surface". The judge singled out "binding attribute" as the
damaging one, because it collides with *binding* as adsorption, the document's own core mechanism.

Q3: seven anaphors, framing announcements and statements about the document rather than the step —
"The two impurity mechanisms of the step separate cleanly in the data…", "Prior knowledge also sets
the expectation for each factor…", "The mechanism is consistent with the root cause."

Q4: seventeen, fourteen by trailing category-rename and three by unrequested gloss. The judge noted
the "X rather than Y" formula alone appeared four times.

## Disposition after run 1

Returned to the same authoring agent in one message: the four questions restated and the flagged
sentences with what each lacks, in the judge's words, with the judge's replacement terms stripped.
No count and no verdict was sent.

**The revision found a physics error of its own.** The step-yield paragraph had put the recovery
risk at a load pH "low enough for a fraction of the antibody to acquire a net negative charge",
which is backwards: a lower pH makes the antibody more positive. It now puts the risk edge at a
load pH high enough to approach the isoelectric point and states that the upper edge studied stays
well below it. This is the third document in this batch whose register revision exposed a factual
error, after `PCR-005`'s two.

`govern` went to **zero** in the rendered text, and the "X rather than Y" formula from six to zero.
485 sentences / 11,087 words; 56 pages became 53.

## Run 2 — after the one revision cycle

**Q1 No · Q2 No · Q3 No · Q4 Yes.** Flags: Q1 17 (9 procedural, 3 direction-missing, 5 bare role
verb), Q2 4, Q3 7 (+1 marginal), Q4 12.

The judge's opening: "There is no `since` and no `governs` in the document; no colon-deferred cause,
because the register carries no mid-sentence colons."

### Q1 (a) — "because" introduces a procedural, statistical or documentary reason

Nine, of which **five are the §9 parameter-classification rationales**: "It was classified as a
well-controlled critical process parameter, because it is fixed by buffer preparation and verified
against the buffer release specification before the buffer reaches the column…"; the load
conductivity twin; the flow-rate one resting on the pump. Also the MVM severity score, the
univariate assignment of flow rate, the one-sided Cpk convention, the absence of a flow-rate effect
estimate, the definition of a key process parameter, and "The second analysis is the more demanding
of the two, because it requires the attribute to hold not only on average but across the spread…".

### Q1 (b) — cause named, direction missing

- "The full factorial was run in preference to a fractional design because each of the four factors changes how tightly the same acidic species are held on the same ligand…" — "changes how tightly" gives no direction.
- "Both log reduction factors fall as load pH falls and as load conductivity rises, because virus particles are bound by the acidic groups on their surface while the load passes." — the direction sits only in the main clause.
- "Prior knowledge treated the ionic strength in the bed as acting on everything held on the ligand, and this study confines that expectation to the weakly held fraction."

### Q1 (c) — bare role verb

"…the charge-variant distribution is set in the production bioreactor (PCR-003)." · "Table 8.1 gives
the attributes this step sets or clears." (and its caption and §12 twin) · "The scope of this study
was set by the pre-characterization risk assessment RA-001…" · "Parameters whose ranges are set by
the equipment or by the platform…" · "The load pH fixes the charge each species in the feed carries
relative to its isoelectric point."

The judge's counter-list, where Q1 is met: "At the load pH the antibody carries a net positive
charge, because its isoelectric point lies well above the load pH, and it passes through the bed";
"What reaches the pool with it is the impurity mass it carries, because the ligand holds a finite
mass of bound species and a load heavy enough to approach that mass lets host cell protein break
through"; "Host cell protein removal falls when the conductivity of the equilibration and wash-1
buffer rises, because part of the population is held weakly enough for the wash to displace it."

### Q2 — four

"life-cycled" as a verb · "acidic charge variant burden" (twice; *burden* in this literature means
bioburden) · "late material" (minor). Everything else the judge lists as correct, including the
deamidation chemistry and its pI consequence.

### Q3 — seven

Definitions and tautologies inside mechanism paragraphs: "The load pH fixes the charge each species
in the feed carries relative to its isoelectric point." (true by the definition of isoelectric
point) · "Protein load in flow-through mode is the mass of antibody passed per volume of resin." ·
"The ionic strength during the load is the one the load carries, which is why raising load
conductivity lowers both log reduction factors." (the main clause is a tautology) · "…so the
capacity that can be exhausted is the capacity for the bound species…" · "The response-surface
models of these three attributes are adequate, show no significant lack of fit, and are the
predictive models of this report." (the last clause stipulates about the report) · and two more.

### Q4 — twelve

Including "…and the model records that as a negative interaction.", "…a single protein with one
binding constant would instead give a sharp change at the pH where its charge reverses.", "…so an
interaction found in this design is a property of the data and not of the aliasing structure.",
"Their exclusion is a decision recorded in RA-001 and is not revisited here.", "Nothing at this step
has that character.", "This follows from the size of the margin."

The judge's summary of the pattern: "the filing gloss … clusters exactly where the mechanism is
best — §5.4 states three real mechanisms and then appends a categorization to each. The Q1 failures
are concentrated in §9, where every classification rests on a `because` about a pump, a buffer
release test or an upstream step rather than on the physics the same section has just described."

## Counts per question

| run | Q1 | Q2 | Q3 | Q4 | verdicts |
|---|---|---|---|---|---|
| 1 (as authored) | 20 | 8 | 7 | 17 | No · No · No · Yes |
| 2 (after one cycle) | 17 | 4 | 7 | 12 | No · No · No · Yes |

## Disposition

One cycle only. The draft stands as revised and goes to its blind reading (TASK-047) against the
round-zero pdf, under `blind-key-B1d.md`, sealed before the agent was launched.

## How the four cycles of this campaign compare

| document | regime | run 1 (Q1/Q2/Q3/Q4) | run 2 | direction |
|---|---|---|---|---|
| `PCR-008` attempt 2 | before the amendment | 12 / 8 / 5 / 12 | 16 / 9 / 9 / 14 | **worse on every question** |
| `PCR-004` | after | 26 / 5 / 7 / 15 | 4 / 0 / 0 / 8 | better on every question |
| `PCR-005` | after | 21 / 4 / 7 / 19 | 3 / 3 / 2 / 6 | better on every question |
| `PCR-008` attempt 3 | after | 20 / 8 / 7 / 17 | 17 / 4 / 7 / 12 | better, but far less |

`PCR-008` converges least of the three documents written under the amended rule, and it is the
document the owner has twice preferred the round-zero version of. That is now a property of this
document across four independent authorings, not a property of one draft.

**A large part of its residual Q1 is content the framework requires.** Five of the nine procedural
"because" flags are the §9 classification rationales, and a well-controlled critical process
parameter is *defined* by control capability — a buffer release test, an upstream step, a pump
holding a set-point. A classification section cannot rest those on physics without misstating what
the classification means. Together with `PCR-004` (a step that governs no attribute) and `PCR-003`
(scope limits the writing guide requires), this is the third document in the batch where the
reviewer's questions flag mandated content, and it is recorded in D8 as open.
