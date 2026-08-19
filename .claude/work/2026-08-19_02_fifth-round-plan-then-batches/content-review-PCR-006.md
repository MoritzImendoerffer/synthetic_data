# Content review of the PCR-006 draft — before promotion

**2026-08-19, TASK-007 §4.** Judge: fresh-context agent (`opus`, self-reported Claude Opus 5), the four
questions and `pc_package/PCR-006_viral_inactivation.DRAFT.pdf` (46 pages), nothing else.

## Run 1 — as authored (`PCR-006.DRAFT.pre-review.qmd`)

**Q1 No · Q2 No · Q3 No · Q4 Yes.**

Q1: the ownership sense of *sets / governs / acts on* throughout (Exec. summary "The step sets one
critical quality attribute, the cumulative clearance of XMuLV, and it acts on two attributes that
other steps control"; §1.2, §2.2 ×2, §6, §11 ×2, §12; "governed attribute" ×9); two deferrals
(§1.1 "The same conditions act on the antibody."; §2.1 "A-Mab concentration was expected to act on
aggregation and not on inactivation."); §2.3 "Inactivation pH, hold time and temperature all act on
the inactivation kinetics and on the aggregation that proceeds in parallel with it…" (no
direction); §5.4 "The parameter that governs virus inactivation does not govern aggregate…" (inside
mechanism prose, the parameter unnamed); §9 two classification-bookkeeping uses; ten *because /
since* clauses with arithmetic, regulatory or modelling reasons (§5.3 "because the curvature it
describes is expected from the chemistry"; §5.4 "its coefficient is smaller because the range
studied spans only ten degrees"; §2.2 "reported here because the hold moves them"); partial: §2.1
"depends on the stability of its own second constant domain" (no direction). Clean passes: the
§2.1, §4.3, §5.4 and §13.2 mechanism clauses.

Q2: *governed attribute* (9 + verb), *quality-linked* (3), *the assured range* (§9), *reportable
floor* (§11), *the acid chemistry* / *expected from the chemistry* (§9, §5.3); borderline
*characterized region* (defined in §4.1).

Q3 (6, five in §5.4): "The surfaces have the shape the chemistry of the step predicts."; "Two
readings are available for it."; "The clearance is claimed as a minimum in §10 for this reason.";
"The absence of a pH term is consistent with the same picture over this narrow range."; "The step
is therefore not a control point for charge variants, and it is not treated as one in §10."; §1.1
"The same conditions act on the antibody."

Q4 (11+): §2.3 "…which is what makes this a characterization study."; §3.3 "…which is the convention
used throughout this report and the reason the clearance claim is conservative."; §5.3 "…which is
the definition of an adequate fit over the region studied."; §6 "The nesting is the one the enhanced
approach describes."; §10 "…which is correct for the mechanism."; §11 "…which is the position ICH
Q5A(R2) takes for every modular clearance claim"; §2.2 "It is used as the acceptance criterion
throughout §7 and is not a claim that the step must deliver the whole of the drug substance
requirement."; the "not about this step alone" disclaimer three times (Exec. summary, §8, §12); §7
"…the difference is stated here so that no range is read against the wrong yardstick."; §11 "The
second result worth stating is…"; §5.4 "…and it is not treated as one in §10."; borderline §5.4
"…which is exactly the pair of significant coefficients the model returns."

## The return to the author (once) — run 2 below

## The author's revision (same context, 1 check_render pass, 45 pages, 408 → 413 sentences, 8,667 → 8,617 words)

Every named sentence changed: the ownership verbs rewritten as mechanism with direction ("Lowering
the inactivation pH raises the log reduction and leaves the aggregate unchanged"); *governed
attribute* ×9 → "attribute in scope"; *quality-linked* → "affect a critical quality attribute";
*the assured range* → PAR; *reportable floor* → limit of quantitation; *the acid chemistry* → "acid
denaturation of the viral envelope and its glycoproteins"; the six Q3 sentences deleted or replaced
by checkable findings; the Q4 tails and the three "not this step alone" disclaimers removed; the
non-physical *because/governs* uses de-causalised. D-001 ("at fixed settings") untouched.

## Run 2 — on the revised draft (fresh judge, self-reported Claude Opus 5, quotes re-extracted)

**Q1 No (3, mild) · Q2 No (2) · Q3 Yes · Q4 Yes (3–4).**

| question | run 1 | run 2 |
|---|---|---|
| Q1 | ~15 ownership uses + 10 non-physical because | **3** — §5.4 "…against the level the production bioreactor sets", §8 "an attribute another unit operation sets", §1.1 "…the log reduction achieved is set by how acidic the hold is, how long it lasts and how warm it is" (mildest); all nine *because* clauses pass |
| Q2 | 5 | **2** — §3.2 "identity-controlled and quality-controlled inputs" (**from `section_plan.yaml`'s operation note, "identity/quality-controlled"** — a source to fix at ship); §2.2 "assurance margin" (**from `doe_report.py`'s docstring / config comment**) |
| Q3 | 6 | **0** |
| Q4 | 11+ | **3** (+1 weaker) — §3.2 the same identity/quality sentence; §4.1 "That follows from the chemistry and not from the control system."; §5.4 "…which is a bimolecular reaction."; §9 "…so it cannot be a key process parameter." |

Outside the four questions the judge found a **mechanism error in the executive summary**: "The
same acid partially unfolds the antibody, so aggregate and acidic charge variants both rise across
the hold" assigns the charge variants to unfolding, where the document's own §1.1/§5.4 attribute them
to acid-catalysed reactions at labile residues. Recorded for the batch page; the one cycle is spent
and nothing is added to a document after authoring — this is an internal inconsistency of the new
text and the owner decides at the reading / at ship whether it is registered or re-authored.

**Disposition:** three of four clean or near-clean after one cycle; proceeds to the batch's annex.
