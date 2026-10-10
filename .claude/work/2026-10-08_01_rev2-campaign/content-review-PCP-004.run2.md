# Content review run 2: PCP-004 Version 2.0 (harvest plan)

Judge: Claude Opus 5.5 (claude-opus-5-5), fresh context, read only `PCP-004_harvest.DRAFT.run2.txt`
(the run was cut by an API outage and resumed). Returned as text; saved by the coordinator (condensed).
Answers: 1 No, 2 No, 3 Yes (glosses present), 4 No, 5 Yes (errors present), 6 No, 7 No.

## Q1 Causes
"The culture conditions, which set the viability of the culture and with it the host cell protein and
DNA that the culture carries into harvest." (no property, no direction); "The three are in scope because
the operation can add to them." (the cause is in the next sentence); "Samples for size variants will be
drawn at the first and the last point only, since the step is not expected to change the size-variant
profile." (an expectation, no mechanism); "An interaction between centrifugation (rcf) and depth filter
load is expected, because the centrifugal field sets the solids that the centrate carries to the depth
filter." (no direction; the next sentence gives two opposite ones).

## Q2 Terms
"smaller than the resolution of the method" (resolution is not a validation characteristic of an ELISA
or a qPCR; §5.5 calls it precision); "set-point analysis", "NOR-propagated analysis", "scan a factor"
(coined; say what each computes); "is not gated" (write "is not an acceptance criterion"); "the campaign
level of PCMP-001 §6.2" (coined); "discrepancy from the plan" (in GMP usage an unexplained difference to
be investigated); Table 5.1 "Analytical variance (%)".

## Q3 Glosses
"They are not studies of this plan, and the paired report PCR-004 records each of them as a discrepancy
from it."; "Work that this plan does not foresee, done without a departure from this plan or from a
procedure, is not a deviation."; "No parameter is classified in this plan, and no result is stated in it."

## Q4 Criteria
Criterion 1's threshold ("smaller than the resolution of the method") has no value and is not left to the
report in so many words; no criterion fits the post-clarification turbidity series, and the plan does not
say it sets no rule for that PAR; no depth filter load level runs at the 9,000 g set-point and the plan
does not say how a PAR follows from the two bracket series; "will be judged on those" (R² and residual
standard error) right after "No adequacy threshold is set for the regressions"; objectives and §8
presume the result ("confirm that the normal operating range lies inside it", "will be shown nested
inside it", "What Step 4 contributes ... is a proven acceptable range"); "are met by the clearance" (no
result).

## Amendment scope
1. "During the Version 2.0 re-analysis, after INV-001 closed, a hold study of the clarified harvest
   (S-HAR-HLD) and a second univariate study of the parameters of this plan (S-HAR-UNI2) were made at this
   step." (an execution fact known only after the study).
2. "Descriptions that Version 1.0 stated wrongly, of the centrifuge, of the depth filter load, of the
   sampling and of the analysis, are corrected without a change to the design." (not named, not marked).
3. The hold of the clarified harvest out of scope, stated five times (borderline; reads as foreshadowing
   the hold study).
4. "the analysis will fit the culture as a block" (§12 item 3; not in §5.5; new or Version 1.0?).

## Q5 Wrong or contradicted
1. Residual DNA ≤ 0.001 ng/dose against the qPCR LOQ (coordinator: A-Mab's claimed acceptable range,
   "Less than 10-3 ng/dose", A-Mab p.47; met through clearance, not measured in the drug substance; no
   change).
2. "Every parameter not varied in a run will be held at its set-point (Table 6.1), apart from the bracket
   of the depth filter load series" vs Table 6.1 and §6.1 (turbidity is measured in the field and load
   series, not set).
3. The set-point as the holding setting for centrifugation and depth filter load vs Table A.1 (the load
   series runs only on centrate from 6,000 g and 12,000 g); likewise §5.5 and §8.
4. "The bracket bounds the filter response between the centrates of those two fields" (only for a
   monotonic response; the plan's own mechanism allows a worst case between them).
5. "It falls as the centrifugal field rises, because fewer fine particles reach the filters" vs §4.1 and
   §5.5 (a higher field may break more cells into fine debris).
6. Field and Q/Σ: if Q/Σ is held at one value across the field series, the cut size is the same at every
   field; the plan never says whether Q or Q/Σ is held constant (a batch centrifuge matches V/(tΣ)).
7. "A commercial disk-stack centrifuge discharges solids periodically and recirculates part of its
   contents" (a continuous disk stack passes the feed through the feed zone once; the damage comes from
   the feed zone design and the solids discharge).
8. "The mitigation is that the study reports effects and ranges and not absolute impurity levels." (a
   model that under-represents lysis also under-states the effect of the field).
9. The qualification paragraph: three outputs judged and "no qualification rule for these three outputs"
   vs "The comparison does not cover the turbidity of the clarified harvest".
10. SEC on unclarified culture and clarified harvest without Protein A pre-purification.
11. Table 5.1 note "Analytical variance is the share of the total variance of a single result that the
    method contributes" (a property of a data set, not of a method).
12. "Samples will be drawn at four points in every run." vs the turbidity series (blended material loaded
    on Protein A; its responses are not in Table B.1).
13. Which clarified harvest sample (filtrate or sterile filtrate) criteria 1 and 2 judge.
14. "This step has no intermediate acceptance criterion." vs "the criteria of the production bioreactor
    are carried through harvest unchanged".
15. "The decision answers INV-001 finding 6" (AMD-001 of 2026-03-20 predates INV-001, opened
    2026-08-03).
16. The objective on turbidity "on the material presented to capture" (the responses are column pressure
    and cycle yield).
17. "The design, the sampling, the procedures and the decision rules of Version 1.0 are otherwise kept in
    its words." vs §1.1 item 7.
18. Minor: censored results excluded from the regression bias the slope.

## Q6 Machine-like
"no response-surface model" six times (§5.5 twice restates §1.1 item 4); the hold out of scope (fourth and
fifth statements); "This plan keeps the assumption of the A-Mab case study"; the resolution comparison
(§12 and §5.5 repeat §5.3); the AMD-001 sentences of §5.3 (repeat §1.1 item 3); "set-point conditions"
twice; "It shows what the centrifuge passed and therefore what the depth filter was asked to remove,
which the depth filter load series varies through centrate produced at 6,000 g and at 12,000 g."
(garbled); the bracketing arrangement (§8 repeats §5.5); two PAR sentences of §8; the bracket coefficient
sentence; "The centrifuge and the filters can raise a quality attribute in two ways." (third statement);
the host cell protein and DNA method sentences ("the second product of cell breakage"); the SOP sentence
(restates Table 3.2); §12 item 1 repeats §5.1.

## Q7 Codes and stand-ins
The revision history (codes alone); "Section 7 defines the term this campaign uses"; the corrected
descriptions (name each); criterion numbers ("criterion 1 of Section 7", "criterion 2"): name the
impurity release criterion and the 10 NTU clarification limit; "such an output"; "the bracket", "two
centrate qualities"; "No result of this study enters them."; "PCR-004 will give them".

## Tables
Table 3.2 merged "Type" cell, AMV order, hyphenated names; Table 4.1 "Tool #1" header; Table 5.1
"Analytical variance (%)"; Table 6.1 a 5 NTU set-point for a parameter that is not set (needs a
footnote); Table A.1 five level labels repeated in four blocks, replicates not shown; Table B.1 near
constant Methods column, the filtrate's purpose; Table 3.1 nested parentheses; Approvals dashes.
