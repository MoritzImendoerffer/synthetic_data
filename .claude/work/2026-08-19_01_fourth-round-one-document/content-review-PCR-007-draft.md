# Content review of the PCR-007 draft — before the reading

**2026-08-19, TASK-003.** Judge: fresh-context `general-purpose` agent, model override `opus`
(self-reported Claude Opus 5, `claude-opus-5[1m]`), given the four questions of
`REVIEW-BEFORE-PROMOTION.md` and `pc_package/PCR-007_cex.DRAFT.pdf` (run 2, 50 pages) and
nothing else. Told nothing about the guide, the counters, the shipped PCR-007, or the probe.

## Run 1 — on the draft as the author left it (`PCR-007_cex.DRAFT.run2-pre-review.qmd`)

Document answers: **Q1 No · Q2 No · Q3 No · Q4 Yes.**

### Q1 — the causal verb without a physical cause and a direction in its own clause

The judge's scope note: procedural, statistical and regulatory uses ("because all four proved
active on at least one response") were not counted.

- *governs* never names a physical cause and runs four ways: "Aggregate is the attribute that
  governs this step" (§2.2, attribute → step); "the four quality attributes this step governs"
  (Exec. summary and §3.5, §6, §8, §10, §12, step → attribute); "protein load, which is its
  governing parameter" (§7.4, parameter → attribute); "the multivariate region governs" (§7.4,
  analysis over analysis); "a separation whose behaviour is governed by one physical quantity"
  (§11).
- §2.1 "…so protein load was expected to act on aggregate clearance, on host cell protein
  clearance and on yield through one physical quantity." — the quantity is in the sentence before.
- §5.3 "…nearly flat in the vertical direction, because elution pH does not act on host cell
  protein." — circular.
- §5.4 "The three responses of this step move together because one physical quantity drives
  them, the fraction of the ligand that is occupied." — no species, no interaction, no direction.
- §5.4 "Protein load sets that fraction." — back-reference object, no direction.
- §5.4 "Elution buffer pH acts on the resolution of the separation rather than on its extent." —
  mechanism in the next sentence.
- §5.4 "Load and wash conductivity acts on the impurity clearance and not on the size variants,
  which the data confirm twice." — mechanism two sentences later.
- §6 "…the boundary runs diagonally, because the two factors interact." — statistical restatement.
- §11 "Protein load sets the fraction of the ligand in use, and through it the breadth of the
  elution peaks, the resolution between monomer and aggregate, the number of free sites …, and the
  losses at both edges of the pool." — five properties, no direction for any.
- §11 "Only protein load acts on both."

Passing, for contrast (the judge's own): §2.1 "Load and wash conductivity set the ionic strength
that shields the charge on the ligand and on the bound species, so a higher conductivity was
expected to strip weakly bound host cell protein during the wash while the antibody stayed
bound."; §5.4 "Aggregate rises because the two populations are less well resolved when the pool
is cut."; §13.2 "Temperature acts on the strength of the electrostatic interaction between the
antibody and the ligand, and a warmer column would be expected to elute the antibody slightly
earlier and to compress the separation between monomer and aggregate."

### Q2 — terms that are not terms of art

QbD vocabulary clean (knowledge space, design space, proven acceptable range, edge of failure,
Tool #1, pure error, lack of fit, peak cut). Flagged: *handle* ("the direct handle on the trade
between aggregate and yield", §2.1 / §5.4 / §9; "one dominant handle", §5.4, §11); *binding
attribute* ("Pool aggregate is the binding attribute", Exec. summary / §6 / §8 / §12 — collides
with the adsorption sense the report uses three pages earlier); *buys back* (§6); *break-even
point* and *assurance factor* (§7.1; the literature says safety factor / safety margin); *a plane
with twist* (§5.4); *the two mechanisms* used as a named concept never defined (§5.2); *impurity
load* against *protein load* (§5.2); *instrument* for a regression model (§5.3); *the aggregate
front* for the leading edge of an elution peak (§5.4); *governed attribute* throughout.

### Q3 — mechanism sentences that cannot be disagreed with alone

§5.4: "This is why protein load is the largest term in all three models and why it acts to raise
aggregate, to raise host cell protein and to lower yield at the same time."; "The step has one
dominant handle, and moving it trades all three responses at once."; "The interaction with
protein load follows from the same picture."; "This is the largest interaction in the aggregate
model and it has the sign the mechanism predicts." (the predicted sign is never stated); "…both
act in the same direction as the main effect, and both have the same explanation."; "Anything that
moves the aggregate forward into the tail makes the position of the stop point matter more.";
"The interaction with protein load has the sign this predicts."; "Protein load sets that
fraction." §5.2: "…which is what the separation of the two mechanisms predicts." §11: "Every large
term in every model of Section 5 is an expression of that one quantity or of a factor that
modifies it."; "The step therefore has a single dominant handle, which makes it easy to control
…"; "The second finding is that the two governed attributes are separated by mechanism, and this
is what makes the design space tractable."; "Only protein load acts on both."; "A design space in
four parameters is therefore almost two design spaces in three, sharing one axis, which is why its
boundary is simple enough to state in two planes."

### Q4 — sentences that file their own finding

Trailing category: §4.1 "…and it is the reason the characterized region is called the knowledge
space."; §7.4 "…and it is the reason the two proven acceptable range columns of Table 7.1
differ."; §7.4 "A univariate range answers what happens if one parameter moves, which is the
question a deviation raises." / "The multivariate region answers where the process may be
operated, which is the question the control strategy asks."; §8 "Aggregate is therefore the
binding attribute of the design space, and its in-process limit carries the larger of the two
assurance factors."; §11 "…and this is what makes the design space tractable."; §5.3 "The step
yield model is a weaker instrument and is treated as one."; §6 "The knowledge space is what the
study explored, the design space is the part of it that is known to give acceptable material, and
the normal operating range is the smaller region the process is actually held in."

Causal gloss to an unraised objection: §7.1 "The assurance factor is what makes each of these an
in-process control rather than a break-even point, because a limit set at the ceiling itself would
leave the drug substance dependent on every downstream step delivering its nominal clearance
exactly."; §7.3 "The corner is the simultaneous worst case … and is not a condition the process
is run at, which is why the normal operating ranges are treated as a box and the design space as
the operating claim."; §11 "Lack of fit is not significant … which says the quadratic model form
is adequate and not merely convenient."; §11 "The centre-point reproducibility is small beside
every effect the study reports, so the design was able to resolve what it was built to
resolve."; §11 "…which is why its boundary is simple enough to state in two planes."; §11 "…which
makes it easy to control and makes the consequence of moving that handle predictable …"; §5.4
"…which the data confirm twice."; §5.4 "…it has the sign the mechanism predicts." / "…has the sign
this predicts."; §5.2 "…which is what the separation of the two mechanisms predicts."; Exec.
summary "…and they are confirmed at commercial scale during Stage 2 and not before."; §11 "The
term is about a quarter of the size of either main effect and it changes no direction and no
range, so it is reported and carried forward rather than acted on."

A paragraph-level frame, four times: §3.1 "Two bounds apply to the model and they are stated here
because every claim in this report rests on them."; §6 "Three bounds apply to this design space and
each of them limits what may be claimed from it."; §7.3 "Three things bound what that finding
means."; §11 "Four limitations bound what this report claims, and each is managed forward rather
than resolved here."

The one gloss the judge called legitimate: §13.2 "Lack of fit for that model is not significant
(p = 0.158, Table 5.9), which would not be expected if one factorial corner had been displaced by
an uncontrolled variable." — the objection was raised by the deviation itself.

## The return to the author (once)

The lists above, minus the document-level counts and verdicts, sent to the run-2 author in its own
context, as what each sentence lacks; no phrase to insert, no number. The author revises in the
same context, re-runs check_render itself, re-renders the pdf. Then run 2 of the review, below.

## The author's revision (same context, one pass, 3 check_render passes, 50 pages)

Reported by the author: every named sentence changed and nothing else except two referential
fixes the rewrites forced (`It` → `Load and wash conductivity` in §5.4; "any other studied
parameter" → "any other multivariate parameter" in §11, which as written was false about elution
flow rate). §5.4 rewritten end to end; *governs* gone in its four senses; *handle* (5), *binding
attribute*, *buys back*, *assurance factor* → safety factor (6), *a plane with twist*, *the two
mechanisms*, *impurity load*, *instrument*, *aggregate front*, *governed attribute* → *attributes
this step clears* (12, prose and captions) all replaced; every flagged back-reference now asserts a
sign or a direction; the four "n bounds apply" frames deleted; §13.2's legitimate gloss kept.
493 / 10,730 → 482 sentences / 10,702 words. `grep -c 'handle\|binding attribute\|assurance
factor\|buys back'` on the revised draft → 0. Draft preserved as
`PCR-007_cex.DRAFT.run2-post-review.qmd/.pdf`.

## Run 2 — on the revised draft (fresh judge, self-reported Claude Opus 5, quotes machine-verified against the PDF text)

Document answers: **Q1 No · Q2 No · Q3 No (narrowly) · Q4 Yes.**

| question | run 1 | run 2 | what remains |
|---|---|---|---|
| Q1 mechanism-shaped verb without cause/direction in its clause | ~15 (+ *governs* in four senses) | **7** | Exec. summary "acted on host cell protein in opposite directions" / "acted on aggregate" (no channel, no direction); §2.3 "because prior knowledge indicated…"; §4.4 and §2.1 flow-rate sentences (channel named, direction absent); §7.2 "the two answers differ because they answer different questions"; §5.3 "the assay … sets the limit of what can be resolved". Plus **17 documentary / statistical / control-system uses** of the same verbs the judge listed "on the literal test" and called substantively sound ("was classified as a CPP because … held by instrumented control", "the design cannot resolve curvature because it holds only two levels", "It is set by the ultraviolet detector") |
| Q2 not a term of art | 10 coinages incl. *handle*, *binding attribute*, *assurance factor* | **4 + 2 weak** | *identity-controlled and quality-controlled* (§2.3), *verification-qualified* (§13.2, App. D), *quality-linked parameters* (Exec. summary, §9), *instrumented decision* (§9); weaker: *manufacturing family* (§3.1), *the operating claim* (Exec. summary) — none of run 1's remain |
| Q3 not deniable on its own | 14 | **1 clear + 2 borderline** | §5.4 "That result holds only over the characterized ranges."; borderline §2.1 "a property of the chemistry of the step" and §11 "is now characterized as a separation in which one parameter moves every response"; "the rest of §5.4 is strong: all 22 other sentences make directional, species-named claims" |
| Q4 files its own finding | ~24 + 4 frames | **11** | §9 "…which is the criterion that separates a well-controlled critical process parameter from a critical one"; §6 "…which is the knowledge space"; §5.3 "…which is the interaction between the two factors"; Exec. summary "…the multivariate design space rather than the individual ranges is the operating claim"; §6 "…are the practical statement of where the step may be run"; §11 "…are the statement that accounts for this"; §8 "…and is the attribute to watch"; §9 "This is the parameter with the narrowest margin at this step."; §3.3 "…and this is the primary assay of the step" (mild); §5.2 "…and the quantitative model of the step is the response-surface model of Section 5.3"; §7.4 "That widening is the contribution of the other three parameters." (mild). Three glosses judged legitimate because the text raised the objection |

**Disposition: not promotable on content by the checklist's letter** — the four do not all read
yes after one cycle — **and the reading proceeds**, as the plan says: the owner reads whatever
the pipeline produced in one cycle. What one cycle changed is on record above; what it did not
reach is the second-order residue the judge found once the first-order faults were gone
(coinages that were not in run 1's list because bigger ones were; `, which is` in places run 1
did not flag). The plan's rule against a second cycle stands: it would tune the draft to the
judge, and the reading is the test.
