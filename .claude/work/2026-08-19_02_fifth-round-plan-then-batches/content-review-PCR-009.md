# Content review of the PCR-009 draft — before promotion

**2026-08-19, TASK-009 §4.** Judge: fresh-context agent (`opus`, self-reported Claude Opus 5), the four
questions and `pc_package/PCR-009_virus_filtration.DRAFT.pdf` (34 pages), nothing else.

## Run 1 — as authored (`PCR-009.DRAFT.pre-review.qmd`)

**Q1 No · Q2 No (narrowly) · Q3 No · Q4 Yes.**

Q1: the mechanism paragraphs (§2.1, §5.4) pass — species, interaction, property and direction in
clause. Flagged: §4.1 "That range brackets the routine range on both sides, because the mechanism
predicts different failure modes at low and at high pressure." (names "the mechanism", not a
cause); §4.1 "The upper edge sits well above the routine maximum load because the mechanism
predicts that retention falls with load…" (weaker); §9 "It is not classified CPP because it is
directly controlled." (category; physical content in the next sentence); §11 "The study
establishes what governs virus retention at this step and where the claim stops." (cause two
sentences later); administrative *governs/sets* (§1.1 "The two attributes it governs are
cumulative…", §2.2 "The step sets no attribute of its own."); and bare *act* with no target —
§2.1 "Filtration pressure was expected to act in two directions.", §3.5/§5.2 "The screening
design identifies which factors act.", §11 "One parameter acts."

Q2: three house compounds — §9 "quality linkage"; §5.1 "analytical allowance" (used before it is
defined in §7.1); §2.2 "a size based membrane" (the removal is size based, the membrane is not).

Q3: §2.1 "Two features of the mechanism set the expectations the study was designed to test."; "The
first is fouling."; "The second is the size difference between the two model viruses."; §5.4 "Step
yield behaves the same way and for a related reason." (fully anaphoric); weaker: §5.4 "The shape of
the MVM surface follows from the sieving mechanism and from how the membrane fouls."; "XMuLV behaves
as the same mechanism predicts at the other end of the size scale."

Q4 (12): §3.1 "…which is what allows the model to stand for the commercial device."; §3.2 "The
filter is used once and discarded, so there is no life-cycle behaviour to characterize as there is
for a chromatography resin."; §4.1 "…which is what makes it a knowledge space rather than a
confirmation of the routine ranges."; §4.2 "…which is what the response-surface design was executed
to do."; §4.3 "…which is what supports the quadratic terms."; §5.2 "…which is the expected outcome of
a design that spends 3 of its 6 degrees of freedom on terms that carry almost no effect."; §5.3
"…which is a property of a design of 12 runs and a bound on how far the surface should be read.";
§5.3 "…which is the graphical form of a model with one active factor."; §7.2 "…which is the expected
result for a virus retained on any intact pore."; §8 "…which is why the load bound of §7 matters to
an attribute it does not set."; §9 "A parameter whose excursions are detected within the batch and
whose effect within the characterized range is under half a log carries a low risk of taking a
batch outside the design space."; §13.1 "…which is part of the reason the parameter is classified
as well controlled in §9, and the continuous pressure record is named as an in-process control in
§10."; §13.2 "…which is the control that made this a deviation with a bounded consequence rather
than an unmeasured one."

## The return to the author (once) — run 2 below

## The author's revision (same context, 1 check_render pass, 34 pages, 352 → 350 sentences, 7,304 → 7,163 words)

29 replacements covering every named sentence; the PAR section's first-analysis handling untouched.
Causes with direction in the §4.1, §9, §11 clauses; administrative *set/governs* reworded; bare
*act* given its target and direction; the three coinages replaced; §2.1's and §5.4's anaphoric
openers deleted and the paragraphs opened on a deniable physical claim; the twelve Q4 tails removed
or turned into their own claims.

## Run 2 — on the revised draft (fresh judge, self-reported Claude Opus 5, quotes re-extracted)

**Q1 No · Q2 Yes · Q3 Yes · Q4 Yes.**

| question | run 1 | run 2 |
|---|---|---|
| Q1 | ~8 + bare *act* ×3 | **0 in mechanism prose** — every *because/since* complete in-clause; what remains: seven *governs/governed* in the register sense ("each attribute the step governs", "both governed attributes", Table 7.1/8.1 captions) and two "is set at … reported in PCR-0xx" in §10 |
| Q2 | 3 | **0** — "no coinages, no invented compounds" |
| Q3 | 6 | **0** — "Every sentence in every mechanism paragraph makes a claim that can be contradicted on its own" |
| Q4 | 12 | **5** (+2 lesser) — §7.2 "A univariate range tells the reader how far one parameter may move." / "The design space tells them which combinations are acceptable."; §13.1 "The deviation is carried forward as evidence for the control it exercised."; §5.4 "…and the load is the parameter that bounds the clearance claim."; §3.1 "…and they are the direct measure of how reproducible the model is…" |

**Disposition:** not promotable by the checklist's letter (Q1 on register verbs, Q4 five); three of
four questions clean in mechanism prose after one cycle; proceeds to the batch's annex.
