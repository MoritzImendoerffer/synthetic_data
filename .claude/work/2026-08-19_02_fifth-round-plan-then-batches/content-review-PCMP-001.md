# Content review of the PCMP-001 draft — before promotion

**2026-08-21, TASK-034 §4.** Batch B5, authored under the amended rule 4. PCMP-001 is a
corpus-level document with no single unit operation, so its brief carries no §2b, and §5c assigns no
registered discrepancy. Fresh judges (`opus`), one return between them.

## Counts per question

| run | Q1 | Q2 | Q3 | Q4 | verdicts |
|---|---|---|---|---|---|
| 1 (as authored) | 9 | **0** | **0** | 7 | No · **Yes** · **Yes** · Yes |
| 2 (after one cycle) | 6 (3 marginal, 3 table cells) | 0 (3 close calls) | 1 (1 borderline) | 2 (1 partial) | No · **Yes** · **Yes** · Yes |

**Questions 2 and 3 both passed on the FIRST run**, which no document in this campaign had managed
before. Question 1 fell from 9 to 6 and question 4 from 7 to 2. The verdicts are unchanged across
the cycle because question 1 and question 4 each retained a residue, not because the revision did
nothing.

## What the return fixed, and how the directions were sourced

The author replaced every flagged placeholder with a claim carrying a direction, and took each
direction from `config/parameters.yaml` or the clearance data rather than from memory. Four were
checked independently against the sources:

| claim in the revised text | source | verified |
|---|---|---|
| a longer culture lowers afucosylation | `duration: -1.36` on afucosylation | yes |
| host cell protein rises as load rises and as elution pH falls | `hcp_load_coef: 0.45`, `hcp_ph_coef: -0.55` | yes |
| anion exchange clearance falls as load conductivity rises | `lrv_cond_coef: -0.5` | yes |
| the low pH hold carries no MVM claim | `viral_clearance.csv`, MVM 0.0 at that step | yes |

"Coupled mechanisms" is gone, replaced by the three routes through the culture environment. All four
bare uses of "governs" became "the attributes the step forms or clears", which is the relation the
register actually encodes.

## Run 2 — the judge's report

Model: Claude Opus 5 (`claude-opus-5`). Read: all 23 pages, nothing else.

It stated its own method before answering: "I applied Q1 to every occurrence of the listed verbs,
but judged the administrative ones (a document 'sets' a scope, a plan is 'approved before... because'
of sequencing) as out of scope for 'physical cause' and flagged only where a claim about the process
is carried by one of those verbs." It then ran a census: `governs` and `since` do not occur anywhere
in the document, `acts on` occurs twice, `sets` seven times, `because` eleven times.

### Question 1 — six flags

- "Prior knowledge also sets the ranges to be studied, because the platform campaigns have already found the conditions at which the process fails." — neither "sets" nor the "because" names a species, interaction or direction; the physical content arrives only in the next sentence.
- "The seed expansion steps that precede Step 3 are not characterized here, because platform experience places no drug substance quality attribute under their control (CMC Biotech Working Group 2009)." — the "because" appeals to platform experience and to a citation instead of naming why no attribute is set there.
- "Carbon dioxide accumulation acidifies the medium, the base added to hold pH at set-point raises osmolality, and pH and osmolality act together on the Golgi enzymes that attach galactose and fucose, so a change in gassing arrives at the glycan through three routes at once." — fails in part: "act together on" names the species and the enzyme but no direction.
- "The production bioreactor carries the largest multivariate design because it forms most of the quality attributes in Table 3.1, and because its parameters reach those attributes through one culture environment." — marginal: the three concrete routes only appear in the following sentence.
- "Culture duration acts on the same enzymes for longer, and platform experience is that a longer culture lowers afucosylation (CMC Biotech Working Group 2009)." — marginal: the direction sits in the coordinate clause and is attributed to experience rather than to the mechanism just named.
- Table 1.1 cells "sets leached Protein A", "sets the cumulative XMuLV (enveloped) clearance", "sets the cumulative MVM clearance" — fails as written, though these are table fragments rather than sentences.

Passing instances the judge recorded as the standard the others fall short of: "On the anion exchange resin the counter-ions of the load compete with impurities and virus particles for the quaternary amine ligand, so both host cell protein clearance and virus clearance fall as the load conductivity rises."; "The low pH hold inactivates enveloped virus faster as the hold pH falls and as the hold is extended."; "For the low pH hold, the model must reproduce the mixing and the time taken to reach the hold pH, because inactivation depends on the pH the material sees and on how long it sees it."; "Each of those mechanisms acts on a different property of the particle, its envelope, its charge and its size, so surviving one does not make a particle more likely to survive the next and the log reduction values may be added (International Council for Harmonisation 2023a)."

### Question 2 — no coinages

"No coinages and no invented jargon." Three loose descriptors were named as the closest calls, none presented as a named term: "the property through which scale reaches the product" (a descriptive coinage, with "volumetric mass transfer" being the literature's volumetric mass transfer coefficient with the coefficient dropped); "channel path length" (fuses the two TFF terms of art, channel height and path length); and "counter-ions of the load", where the judge notes they are counter-ions of the ligand and "the physics is right, the possessive is loose".

### Question 3 — one flag

- "Parameters that reach one attribute by several routes cannot be separated one at a time, which is why they are studied together." — the trailing clause cannot be disagreed with on its own; it repeats the study-type rule already stated elsewhere.
- Borderline: "The split is uneven across the train, and it follows what each step does."

### Question 4 — two flags

- "Parameters that reach one attribute by several routes cannot be separated one at a time, which is why they are studied together." — a trailing causal gloss that files the mechanism under the multivariate-design category the reader was already given.
- "Characterization of those attributes is therefore an upstream activity and PCP-003 carries it." — fails in part: "therefore an upstream activity" renames the preceding finding as a category.

Near-misses it did not flag: "It is not a classification of parameters." pre-empts a real regulatory confusion and is followed by the operative rule; the "so…" tails in the viral clearance and impurity paragraphs state consequences rather than categories.

### Answers

1. **No.** 2. **Yes.** 3. **Yes.** 4. **Yes** — one clear instance and one partial.

## Findings recorded, not acted on

- The author's own line-wrapping pass collapsed the YAML front matter mid-revision and broke the
  docx render. It restored the front matter and re-gated. The current file's front matter was
  diffed against the pre-review copy and is **identical**, so the restoration was verbatim rather
  than reconstructed. Recorded because a formatting pass that can break front matter is a hazard
  for any future revision, not because it damaged this document.
- Three table cells in Table 1.1 use "sets" without a mechanism. They are generated table content
  rather than authored prose.
- One sentence is flagged by both question 3 and question 4 and survives, along with the "therefore
  an upstream activity" partial.

## Disposition

One cycle, two fresh judges, no third pass. Two of the four questions pass, and both passed before
any revision. The document proceeds to the batch B5 annex task under `decisions.one_review_cycle`.
Nothing is added to it after this point.
