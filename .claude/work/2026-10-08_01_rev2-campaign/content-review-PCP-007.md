# Content review run 1: PCP-007 Version 2.0 (cation exchange plan)

Judge: Claude Opus 5.5 (claude-opus-5-5), fresh context, read only `PCP-007_cex.DRAFT.txt` (plus a
simulation of the §7.2 residual and influence tests). Returned as text; saved by the coordinator
(condensed, quotes shortened). Answers: 1 No, 2 No, 3 about eight mild cases, 4 No, 5 errors (15 major),
6 No, 7 No.

## Q1 Causes (11)
"a property of the chemistry" for leached Protein A clearance (name the charge difference); the
complexed Protein A "released when the antibody binds" (no interaction named; doubtful); "As the load
approaches the dynamic binding capacity ... weakly bound host cell protein finds fewer free sites from
which the wash would displace it" (the cause points the other way: fewer free sites means more HCP in the
flow-through; if the mechanism is HCP bound to product, say so); "Elution flow rate sets the residence
time" (no direction); "Protein load also acts with load/wash conductivity" (no direction of the
interaction); "a later stop ... and an earlier stop the reverse" (direction in time only; a later stop is
a lower AU threshold); "The points at which collection starts and stops change the share of fragments"
(no direction); "Temperature is held constant and is not varied, because the platform runs the step at
controlled room temperature" (procedural reason only); "One buffer therefore sets the ionic strength of
both operations, and the two cannot be varied independently" (the load is the adjusted pool; equal load
and wash conductivity is a design choice); "protein load is expected to interact with each of the other
factors through the peak broadening" (§4.3 places the load x conductivity interaction in the wash); "An
interaction with ... the collection window is therefore not expected" (flow rate changes peak shape, so
flow rate and stop collect should interact by the plan's own mechanism).

## Q2 Terms (9)
"NOR-propagated analysis" / "set-point PAR" (coordinator: PCMP-001 terms, define at first use);
"judgement over the NOR"; "operating region" / "declared region" (ICH Q8 design space; coordinator: keep
Version 1.0 term, define once); "Cation exchange forms no quality attribute" (attributes are not formed;
CEX resin can induce aggregation); "discrepancy from the plan" (corpus term, define once); "execution
window" (study start and end dates; coordinator: PCMP-001 term, define once); "analytical method decision"
(name AMD-001 at first use); "carries" used for "is tested for"; "Most host cell proteins are acidic at the
operating pH" (pI below the load pH, net negative charge); Table 7.1 "Clearance factor" vs text "fold".

## Q3 Glosses (8)
"It is the direct handle on the balance between aggregate and yield."; "The studies are therefore designed
to confirm and bound platform behaviour, not to discover it."; "The table carries no classification,
because classification is an outcome of the study..."; "The rule that PCMP-001 §6.4 sets for viral
clearance ... does not apply here."; "The matrix carries no response columns, and the results are reported
in PCR-007."; "A run at such a pH would confirm the mechanism and would say nothing about the operating
region."; "PCR-007 states it in those terms, not as an absence of effect in general."; "The excess can
never exceed the host cell protein present."

## Q4 Criteria (12)
"comparable in size with the effects estimated in the screening study" (not quantified; coordinator:
Version 1.0 rule, keep and say Version 1.0 set no threshold); "within assay variability of its criterion"
(undefined; conflicts with the §7.4 interval judgement); "an effect smaller than that spread is not
claimed" (a third rule for an effect); "unless the data show one" (no test); the refit "with a justified
change of terms or transformation" (shared item 6); plate count and asymmetry compared with no criterion;
packing limits not stated; mass balance closure criterion not given; "From the cation exchange pool onward
the two methods agreed" (no agreement criterion); the 0.20 limit and α 0.05, 4/n rest only on
"conventional"; one-sided 95 % verification bound vs two-sided 95 % (one-sided 97.5 %) interval elsewhere,
never justified; "out of trend" undefined; decision rules in "should" (binding?).

## Q5 Wrong or contradicted (15 major, 19 minor)
Major: the raw-residual test can never fail (shared item 3); 4/n rejects 99 % of adequate models (shared
item 3: keep as generic, reports examine); "The range of elution buffer pH stops short of the pH at which
the antibody would no longer bind reproducibly" (elution pH controls release; failure modes are incomplete
elution and co-elution of aggregate); "Attributes of high (H) and very high criticality are called
critical" vs Table 4.1 "CQA" heading (delete the convention); "The studies are run on a qualified
scale-down model" vs qualification decided at analysis; "Version 1.0 judged the pool against ... 1 % ...
193 ng/mg" vs note a (shared item 2); "An assumption is confirmed when the predicted worst case is no worse
than the platform worst case" (confirmation on the point prediction vs the bound); "A proven acceptable
range is determined for each output ... and for each factor of the response-surface model" (flow rate gets
no PAR, yet classification uses the PAR margin); "Pool aggregate, pool host cell protein and step yield are
measured on each run" (factual error 2; also no fragments for flow rate); the load sampled without
fragments although Table 7.2 checks the fragment fold; "No other study under this plan ran on one of the
instrumented systems..." (implies uncontrolled UV and pH measurement); "The response-surface study follows
the screening analysis" (screening ended Friday 2026-02-27, RSM began Monday 2026-03-02); "Should the
screening analysis identify an active factor that is not carried into the response-surface design, the
design should be augmented..." (cannot arise: both designs carry the same four factors; Version 1.0 rule,
keep); "SEC read fragments high wherever the sample still carried host cell protein" vs "From the cation
exchange pool onward the two methods agreed" (the CEX pool still carries HCP); "The excess can never
exceed the host cell protein present" (UV area vs ELISA mass).
Minor: "Version 1.0 did not assess fragments here" (measured, not judged); the qualification "covers the
attributes that enter and leave the step" lists yield and omits fragments; "The plan covers the 5 process
parameters of the step" (bed height, packing, buffer composition, temperature, start-collect named
elsewhere; start-collect not in Table 6.1); plate count and asymmetry describe a tracer pulse, not the
eluted protein peak; "DNA is repelled by the ligand at every conductivity and pH in Table 6.1" (the only pH
in Table 6.1 is elution pH); both monomer losses at the trailing edge; "The qualification and the centre
point performance test this assumption" (they do not test mechanism); "The declared region lies inside the
ranges studied, and the NORs lie inside the declared region" (assumes the result); "the control strategy
is built on the region" vs §7.5 (the claim rests on the NOR-propagated PAR); the univariate study shares
the feed lot and needs other equipment; "Its samples were not retained and could not be retested by
nrCE-SDS" vs §5.4 retention; S-CEX-FRC missing from Table 11.1; Table 3.1 omits INV-002, PCR-008, AMD-001;
changes 2, 6 and 8 name no Version 1.0 rule replaced; the HCP criterion uses the verified A-Mab bound, not
a platform worst case; "Work that this plan does not foresee is not a deviation" vs §13; "a dimer carries
twice the charged surface" (contact area hides part of each surface); the NOR-propagated PAR narrower
mainly because it uses single-batch percentiles; the capability simulation without a residual per draw
overstates capability.

## Q6 Machine-like (20)
Restatements: finding 1 three times; the AMD-001 sentence word for word; §7.1 repeats §5.1; the
classification sentence repeats change 7; the flow-rate residence-time sentence three times; "They are
controlled inputs to the study, not factors of it."; the ALCOA+ spelling; the roles repeated in Table
10.1; the approval date; the fixed seed; "No result of the studies under this plan enters these criteria."
and "The one A-Mab value in them is the anion exchange bound."; "decided at analysis" four times; "The
centre points are run at the set-point of every factor." five times; "The same level applies to model
terms, to lack of fit and to the regressions of the residuals." Padding: "The level α = 0.05 is the
conventional level for a statistical test."; "The cut-off 4/n is the conventional one, and it falls as
the design grows."; "That limitation is accepted here for a physical reason."; "A PAR that reaches the end
of the range studied is reported as reaching it."; "It shows what one parameter can do while the rest of
the step is at target."; "No viral clearance claim is made for this step." (§7.4, repeats §1).

## Q7 Codes and stand-ins (15)
"the rule of PCMP-001 §7.5" (name it); "The decision compares the conclusion over the NOR..." (name the
conclusion); "Under the offset rule" (name it); "for the reason given in Section 1.1" (name it); "The claims
of this study are bounded by the model." (the scale-down model); "PCR-007 checks the 3 that are responses
of the designs" (name them); "The one A-Mab value in a criterion of this step" (the 4.27-fold AEX bound);
"The report PCR-007 gives its outcome for this step." (name it); "Each output is judged on a single batch."
(against the 95 % prediction interval of a single batch); "Each class is argued from two stated values."
(name them); "The execution record is complete." (name what was added); "RA-001 established this" (the
risk assessment RA-001); "Version 1.0" standing for both plan and reports; "That judgement rests on an
assumption about the mechanism." (fragments judged with no offset); "The decision answers INV-001 finding
6" (name AMD-001).

## Step-specific rules or execution details added after the data
"Fragments are judged as the model predicts them, and no offset is subtracted." with the §5.1 mechanism
paragraph and Assumption 5 (a rule for this step only; no PCMP-001 clause); the S-CEX-UNI retention facts
and the RSM across the decision date (execution facts; belong in PCR-007; the method rule is permitted);
the S-CEX-FRC results in §5.3 (borderline: basis of the permitted fragment method); EQ-CHR-118 calibration
(allowed by PA3 as a recorded fact); the fixed seed 20240724 (require that a seed be fixed and recorded,
unless the value comes from Version 1.0); the PCR-007 reporting duty for the widened HCP criterion (the
risk argument belongs to PCR-008, the report whose check changed the criterion; borderline).

## Tables
Approvals all "—"; the revision-history cell; Table 1.1 "R1" legend with one rule, a cell wrapping three
lines; Table 4.1 "CQA" header and split headers; Table 6.1 unit "pH" and set-points "6" and "1" without
the precision of their ranges; Table 7.1 constant "Increase" column, "Clearance factor 1.00" meaning no
change, caption "output" singular, "factor" vs "fold"; Table 7.2 repeated "Response-surface model";
Table 10.1 near-identical role names; Table 11.1 parenthesis in a cell, S-CEX-FRC missing.
