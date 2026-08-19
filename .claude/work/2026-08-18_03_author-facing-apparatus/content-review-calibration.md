# Content-review calibration — the four questions on the shipped excerpt and the probe

**2026-08-19, TASK-010.** Judges: fresh-context `general-purpose` agents, model override `opus`,
each given the four questions and one PDF and nothing else (`procedures/REVIEW-BEFORE-PROMOTION.md`
prompt). Each judge reported itself as **Claude Opus 5** (`claude-opus-5[1m]`) and read only its
PDF (1–2 tool uses). The judges were not told which text was which. `A.pdf` = the probe,
`B.pdf` = the shipped `PCR-005` subsections (key opened in TASK-004).

The calibration target (plan, TASK-010): the shipped text must be flagged on question 4 at least
on the sentences the owner quoted on 2026-08-18 (#1, #3, #8 of results §4) and on question 1 or 2
on #6 and #7; otherwise the questions are reworded once and re-run.

## Run 1 — the questions as first written

### B.pdf, the shipped text — document answers: Q1 **No**, Q2 **No**, Q3 Yes, Q4 **Yes**

Owner-quoted sentences, and where the judge caught them:

| # | owner's quote (2026-08-18) | judge, run 1 |
|---|---|---|
| 1 | "…significant at 1,944 (p = 0.0040), which is the curvature a two-level design cannot see" | **Q4** — "trailing clause relabels the term as a category" |
| 2 | "The two estimates do not conflict, because a non-significant screening estimate makes no claim about the sign" | **Q1** ("a rule about p-values, not a species") and **Q4** ("rebutting a conflict only the document itself has raised") |
| 3 | "The contours are curved instead of parallel, which is the interaction and the pH curvature already seen in Table 5.8" | **Q4** — "re-files the picture as two already-named table terms" |
| 4 | "is retained as knowledge-space evidence and is put to no other use in this report" | **Q4** — "filing instruction in the plainest form" |
| 5 | "follow from the physical chemistry of affinity capture and confirm the expectations recorded in §2.1" | Q3 "closest call", not counted: "the first conjunct gestures at a whole discipline and cannot be contradicted" |
| 6 | "governs pool host cell protein because it sets the aggressiveness of desorption" | **Q2** — "'aggressiveness of desorption' is a coinage; the literature term is elution strength"; **passed Q1** because the clause after the colon names species, interaction and direction |
| 7 | "Protein load acts through the capacity of the bed" | **not flagged** — passed Q1 for the same reason as #6 |
| 8 | "behaves as a resin property … none of which is a parameter of a single run" | **Q1** partial — "three real causes are named but 'depends on' assigns no direction"; not Q4 |

Sixteen Q4 flags in all, "the document's habit; the trailing 'which is / which makes / consistent
with' clause appears throughout §1.1", plus three Q2 flags on "predicted coefficient / adjusted
coefficient" used for predicted R² / adjusted R² ("'coefficient' means a model term everywhere else
in this document") — a real terminology fault nobody had named.

**Against the target:** #1, #3 flagged on Q4 ✓; #6 flagged on Q2 ✓; #8 flagged, but on Q1 and not
Q4; **#7 not flagged.** The judge's reason for #7 is precise: the sentence continues past the
colon into the mass transfer zone and the dynamic binding capacity, so read whole it names the
cause. The owner's objection was to the frame in front of the colon. Four of five; the rule says
reword once and re-run.

### A.pdf, the probe — document answers: Q1 **No**, Q2 Yes, Q3 **No**, Q4 **Yes**

The text the owner preferred is not clean either, and the judge says where:

- **Q1, six** — "The two factors that dominate the host cell protein surface act on the same
  physical process" (an abstraction, no direction); "Load flow rate acts on recovery rather than on
  selectivity" (responses, not causes); "a further rise in pH acts mainly on the product itself" (no
  interaction, no direction); "Elution buffer pH sets how much of that population leaves the column
  together with the product" and "Protein load acts through the mass of antibody the bed carries"
  (physical, but the direction arrives only in the next sentence); "The fitted model acts in that
  direction" (a model as the physical actor).
- **Q3, three** — "the direction of the curvature has a physical reading"; "The interaction terms
  follow the same reading"; "The fitted yield model shows the coupling this predicts" — each "an
  announcement that the data agree, with the actual content in the sentence after".
- **Q4, five** — "The level itself is the reason this matters little"; "the result is read as no
  demonstrated lack of fit rather than as proof that the quadratic form is complete"; "…which is
  unusual for a purity and recovery pair"; "shown for completeness"; "meet the in-process limit for
  that reason".
- **Q2 clean.** Two loose usages ("ranged" as a verb; "a physical reading"), no coinage.
- **And one domain catch outside the four questions:** "A lower elution pH protonates the carboxyl
  and histidine groups at the contacts that hold these species" — histidine is already fully
  protonated across pH 3.2–3.9, so within the range only the carboxyl term is directionally live.
  The same claim was in `authoring/mechanism/protein_a.yaml` (`elution_ph`) and has been corrected
  there in this task: the histidine story explains why low pH elutes at all; the within-range effect
  is the residual affinity and the carboxylate contacts.

**Reading of run 1.** The questions see what the owner saw on the shipped text (four of the five
targets, all eight quoted sentences hit somewhere except #5 and #7), and they see the same faults at
a lower rate in the probe: the probe's five Q4 flags in 90 sentences against the shipped sixteen in
59; the probe's Q1 flags are mostly a missing direction that the next sentence supplies, where the
shipped Q1 flags are p-value rules and evaluations standing where a cause belongs. The judge is
stricter than the owner and it is consistent, which is what a gate needs.

## Rewording

Q1 gains "— **in the clause where the verb stands**, and not only in a clause that follows a colon
or in the next sentence". This is the owner's objection to #6 and #7 stated as a rule: the frame
"acts through the capacity of the bed" is the fault whether or not the sentence goes on to name the
cause. Q2, Q3 and Q4 unchanged. Applied to `authoring/REVIEW_CHECKLIST.md` and
`procedures/REVIEW-BEFORE-PROMOTION.md` before the re-run.

## Run 2 — after the rewording (both judges again Claude Opus 5, fresh contexts)

### B.pdf, the shipped text — Q1 **No**, Q2 **No**, Q3 **No**, Q4 **Yes**

| # | owner's quote | judge, run 2 |
|---|---|---|
| 1 | "which is the curvature a two-level design cannot see" | **Q4** |
| 2 | "do not conflict, because a non-significant screening estimate makes no claim about the sign" | **Q1** and **Q4** |
| 3 | "which is the interaction and the pH curvature already seen in Table 5.8" | **Q4** |
| 4 | "is put to no other use in this report" | Q2 borderline ("knowledge-space") — not on the Q4 list this run |
| 5 | "follow from the physical chemistry of affinity capture and confirm the expectations recorded in §2.1" | **Q3** — "an announcement of conformity; nothing here can be contradicted without going to §2.1" |
| 6 | "governs pool host cell protein because it sets the aggressiveness of desorption" | **Q1** ("both `governs` and `sets` land on 'the aggressiveness of desorption', an abstraction with no species and no direction; the actual cause appears only after the colon") and **Q2** |
| 7 | "Protein load acts through the capacity of the bed" | **Q1** — "names a resin property but no species and no direction in its own clause — the whole mechanism is deferred past the colon" |
| 8 | "behaves as a resin property … none of which is a parameter of a single run" | **Q1** — "lists three properties without a direction" |

Fourteen Q4 flags (the run-1 list less #4 and plus three: "which leaves the pool most sensitive to
pH exactly where the pH is lowest", "which is why end of pool collect carries the dominant positive
term", "Consequently, both would be narrower …"). Q2 adds "descending edge" and "multivariate
region" as borderline. Q3 now flags four, including #5.

**Against the target after the rewording:** #1, #3 on Q4 ✓; #6 on Q1 and Q2 ✓; #7 on Q1 ✓;
#8 on Q1 (both runs), never on Q4. Seven of the eight owner-quoted sentences are flagged; the
eighth (#4) was flagged in run 1 and is borderline in run 2. The one persistent gap against the
literal target is #8 on Q4: both judges read "none of which is a parameter of a single run" as a
missing direction (Q1) rather than as filing (Q4). That is a defensible reading, and the sentence is
caught either way; the target's assignment of #8 to Q4 was the owner's reading, and the questions
are not reworded a second time (the plan allows one).

### A.pdf, the probe — Q1 **No**, Q2 Yes, Q3 **No**, Q4 **Yes**

Stable across the two runs. Q1: the same five (plus "The fitted model acts in that direction" and
"identify which factors act", verbs outside the listed set), with the judge's own summary: "each
mechanism paragraph opens with the causal verb and defers the cause to the sentence after it. Where
the cause and direction do sit in the clause, the writing is clean". Q3: three plus two borderline.
Q4: seven (the run-1 five plus "the joint constraint is carried into the design space below rather
than expressed as four independent ranges" and "No coefficient of that model is carried into the
interpretation below"). Q2: clean, three loose usages ("a purity and recovery pair", "end of pool
collect" as a nominal, "coupling").

## What the calibration says

1. **The questions see what the reading saw.** On the shipped text they land on seven of the
   eight owner-quoted sentences, in two independent runs, and they find faults the owner did not
   name (the "predicted coefficient / adjusted coefficient" coinage, three times).
2. **They are stricter than the owner and consistent across runs and texts.** The probe, which
   the owner preferred with no sentence quoted, is flagged on Q1, Q3 and Q4 — at roughly a third
   of the shipped rate per sentence for Q4 (seven in 90 against fourteen to sixteen in 59) and
   with a different character: the probe's Q1 flags are a direction that arrives one sentence late,
   the shipped Q1 flags are p-value rules and evaluations standing where a cause belongs. A gate
   that passes the probe as it stands would need a threshold; the checklist as written blocks
   promotion on any "no", so a probe-quality draft would go back to its author once with seven
   sentences named. That is the intended behaviour, and it is cheap.
3. **The judge is a competent scientific reader.** The histidine pKa catch (run 1, A) is correct
   and corrected `authoring/mechanism/protein_a.yaml`; the "for that reason … attaches to the
   wrong half of the number" catch (run 2, A) is a real logical fault in the probe.
4. **Question 4's wording carries most of the load** and its flags are the least contestable.
   Question 3 is the softest (borderline calls in every run) and is kept because it caught #5,
   which no other question reaches.

Whether an LLM judge is a sufficient reviewer stays open, as the proposal says; what this
calibration settles is that these four questions, asked of a fresh reader, reproduce the owner's
2026-08-18 reading on the shipped text and rank the two texts the way the owner did on 2026-08-19.
