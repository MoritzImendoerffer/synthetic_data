# Content review of the PCR-008 draft — before promotion

**2026-08-19, TASK-008 §4.** Judge: fresh-context agent (`opus`, self-reported Claude Opus 5), the four
questions and `pc_package/PCR-008_aex.DRAFT.pdf` (53 pages), nothing else; quotes re-extracted with
`pdftotext -layout`.

## Run 1 — as authored (`PCR-008.DRAFT.pre-review.qmd`)

**Q1 No · Q2 No · Q3 No · Q4 Yes (pervasive).**

Q1: 25 `govern*`, 9 `sets`, 11 `act(s) on / through` — in none of the 25 `govern` instances does the
clause name species, interaction and direction together; the physics is always in a neighbouring
sentence under another verb ("moves", "shields", "converts", "displaces"). Named: Exec. summary
"Load pH and the equilibration and wash conductivity govern host cell protein clearance, and they
act on it in opposite directions." / "Load pH and load conductivity govern the clearance of both
model viruses."; §5.2 two; §5.3 "…which is the point §5.4 explains." (deferred to a section); §5.4
"Host cell protein clearance is governed by the two parameters that act on the same equilibrium
from opposite sides." / "Virus clearance is governed by load pH in the same direction and by load
conductivity rather than by the equilibration and wash conductivity." / "Each response is governed
by the conductivity of the phase in which its binding is decided."; §2.3/§4.3/§4.4 "act on the same
binding equilibrium", "lay on a mechanistic path", "act on the equilibrium"; §7 "The two analyses
differ because they ask different questions." and the design-space/PAR "statement that governs"
sentence; §9 four (incl. "the direction that matters"); §10 "because their clearance is robust to
the operating parameters"; §11/§12 four bare relations. Passing: §5.4 "Raising the load pH moves
more of the host cell protein population below its isoelectric point, so a larger fraction of the
population is negatively charged and binds, and the pool concentration falls."

Q2: *mechanistic path*, *quality-linked path*, *phase* used for a cycle segment (collides with
stationary/mobile phase), *binds* used for "constrains" (collides with adsorption), *lot family*,
*governed response*, *assurance factor* / *break-even point* (→ safety factor), *buys robustness*,
*separates the two mechanisms in time*, *planar with a twist*.

Q3: §5.4 "The surfaces have the shape the binding equilibrium predicts, and the one result that was
not anticipated is informative rather than anomalous."; "The interaction between them has a direct
physical reading."; "The conductivity result separates the two mechanisms in time."; "Each response
is governed by the conductivity of the phase in which its binding is decided."; §2.1 "The expected
behaviour of each attribute follows from that equilibrium."; §11 "What the study adds to prior
knowledge is the separation between the two conductivities."; "One result of the study is
uncomfortable and is stated here rather than left in the tables."; "Confidence in the scale-down
model rests on three things."

Q4: ~30 — body text carries 30 "rather than", 5 "which is why", 3 "which is what", 5 "the reason";
the signature `<finding>, and it is X rather than Y`; three sentences of commentary on the
document's own conduct ("stated here rather than left in the tables", "named here so that the
boundary of the claim is explicit", "carries it as an action rather than as an observation"). Full
list sent to the author.

**Provenance note for ship:** "assurance factor / margin" reaches authors from `doe_report.py`'s
docstring (line ~418) and a `config/parameters.yaml` comment (line 204); flagged as a coinage in
PCR-007, PCP-005 and PCR-008.

## The return to the author (once) — run 2 below

## The author's revision (same context, 3 check_render passes, 54 pages, 441 → 449 sentences, 9,909 → 9,914 words)

Every named sentence rewritten or de-causalised; *govern* gone from all of them; the coinages
replaced (*phase* now only in its chromatographic sense, *binds the region* → constrains, *assurance
factor* → safety factor ×3 with the parallel edits it forced); the seven Q3 announcements deleted or
replaced; all 17 trailing-category items and all 15 glosses removed; document-wide "rather than"
30 → 11, "which is why" 5 → 0. The PAR section's first-analysis sentences byte-identical; D-001 intact.

## Run 2 — on the revised draft (fresh judge, self-reported Claude Opus 5)

**Q1 No · Q2 Yes · Q3 Yes (one borderline) · Q4 Yes (6–8).**

| question | run 1 | run 2 |
|---|---|---|
| Q1 | 25 *govern* + most *sets/acts* | **0 deferrals** ("the specific failure Q1 names does not occur"); 3 empty/circular connectives (§6 "because both viral criteria are met everywhere in it", §7 "because it differs between the attributes", §3.1 the facility rule), 3–4 *sets/acts on* with no direction (§4.4 "Flow rate sets the residence time in the bed.", §9 ×2, §5.4 marginal), ~10 relational *governs/sets* ("every criterion the step governs", "the attribute this step sets") |
| Q2 | 10 | **0** — "no coined or non-standard term anywhere, in prose or tables" |
| Q3 | 8 | **0** (+1 borderline §11 "tight … wide") — "There is no 'this is consistent with the mechanism' sentence anywhere" |
| Q4 | ~30 | **6** (+2 secondary) — §5.1 "Both bounds are applied where they matter below."; §5.3 "…and is reported as a process performance attribute only."; §6 "That corner is an edge of failure of the step…"; §7 "The criterion column needs its basis stated…"; §8 "…and this is one of them."; §11 "The step holds a tight host cell protein limit and a wide viral margin at the same time." |

**Disposition:** not promotable by the letter (Q1 relational verbs, Q4 six); Q2 and Q3 clean after
one cycle; Q4 ~30 → 6; proceeds to the batch's annex.
