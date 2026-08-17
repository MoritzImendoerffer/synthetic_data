# Seven patterns mined from the human sources, with real examples

Derived on 2026-08-16 by parsing the sources with spaCy and extracting the sentences that
instantiate each construction (`scratchpad/mine.py`). The parse is the **discovery** instrument:
it locates the sentences, and the sentences are the guide. Nothing here is invented, and nothing
here is a threshold.

Pool: A-Mab pages 60–200 and PDA TR 60 pages 18–90, filtered to 8–45 word sentences with no table
debris. The two ISPE guides were parsed for the same patterns and are **not quoted**, because
whether they may be reproduced here is unsettled. Every example below is verbatim.

This file is the source material for two things: the `WRITING_GUIDE.md` §2c/§2d amendment, and a
moves catalogue in `REGISTER_EXEMPLAR.md`.

---

## 1. The frame comes before the subject

**What the parse shows.** Human sentences carry **9.2 (A-Mab) and 9.4 (PDA) tokens before the main
verb**; corpus documents carry 5.8 to 6.9. The human front field holds the case in hand, the
condition, the basis or the contrast. The corpus opens on its subject and appends qualifications
after the verb.

**The openers the sources actually use**, by frequency in the mined pool: `In this case`,
`For example`, `Based on <evidence>`, `In order to <goal>`, `For the purposes of <scope>`,
`However, since <reason>`, `If <condition>`, `While <concession>`, `Although <concession>`,
`Moreover`, `Similarly`, `By contrast`, `Here, we`, `Occasionally`, `Collectively`.

> "**In this case,** changing the medium concentration from 0.8 to 1.6 X only changed the
> aFucosylation levels by 0.3 %." — A-Mab

> "**Based on process understanding,** no further process development studies were deemed
> necessary for A-Mab seed culture expansion up to the N-2 step." — A-Mab

> "**In order to meet anticipated commercial demand,** Process 1 was further optimized to increase
> product titers while ensuring no significant impact on product quality." — A-Mab

> "**For the purposes of this case study,** only a subset of quality attributes was considered in
> the analysis of drug substance and drug product development; these include aggregate,
> galactosylation, a-fucosylation, deamidation, and HCP." — A-Mab

> "**Occasionally,** the science behind a process will be understood well enough to skip screening
> and 2-level factorial experiments and start with response surface experiments." — PDA TR 60

**Rule.** Open a sentence that continues an argument with the frame it belongs to. The subject
follows the frame; the verb follows the subject closely. `WRITING_GUIDE.md` §2c currently forbids
opening a paragraph with a table reference, which is right, and says nothing about this, which is
the gap.

---

## 2. The main verb names the event

**What the parse shows.** `be` is the root verb in 14.7 % of A-Mab sentences and 18.2 % of PDA's,
against **33.3 % in PCR-003**. Light verbs overall: 30 % human, 43 % PCR-003.

> "In this case, changing the medium concentration from 0.8 to 1.6 X only **changed** the
> aFucosylation levels by 0.3 %." — A-Mab

> "Collectively, these steps typically **remove** 4-8 logs of XMuLV, resulting in an overall 12-18
> log safety margin with a minimal risk to patient safety." — A-Mab

> "Protein loads on the AEX Membrane uniformly **exceeded** 10 gram/ml in these studies, providing
> a worst case value for the maximum AEX Membrane load in the manufacturing process." — A-Mab

> "Longer culture times **resulted in** higher titers and lower a-fucosylation levels." — A-Mab

> "Also, prolonged culture durations **resulted in** lower final culture viabilities and thus
> higher HCP and DNA levels." — A-Mab

> "Increasing airflow rate **strips** carbon dioxide and thus **reduces** pH and potentially
> **leads to** an overall reduction of caustic addition." — A-Mab

The last three are the closest human analogue to what a screening-effects section has to say, and
none of them uses a copula.

**Rule.** If the sentence reports something that happened, a lexical verb carries it. `X is a Y of
Z` becomes `X does Z`. The failing corpus sentence — *"These are large and well-resolved effects
of limited practical consequence"* — has `are` as its root and three nominalisations for a
payload.

---

## 3. Concede first, then commit

**What the parse shows.** `However` appears 46 times in A-Mab and 21 in PDA TR 60, and **zero
times** in four corpus documents. `Although`, `While` and `Since` open subordinate concessions
throughout both sources.

> "**Although** key process parameters and key process attributes have been shown not to impact
> product quality, they are included in the control strategy because their monitoring and control
> ensures that the process is operated in a consistent and predictable manner." — A-Mab

> "**However,** sialylation variants are only present at very low levels in A-Mab and thus are not
> considered critical to product quality." — A-Mab

> "**While** these parameters are very valuable to describe bioreactor performance, on their own
> they do not provide sufficient information to predict possible non-homogeneity in the culture
> environment." — A-Mab

> "**While** univariate approaches are appropriate for some variables to establish a proven
> acceptable range (PAR), multivariate studies account for interactions between process
> parameters/material attributes." — PDA TR 60

> "**Since** screening designs do not always clearly identify interactions, the reduced number of
> parameters identified by the screening experiment will be included in further experiments."
> — PDA TR 60

> "**Although** the extent of the effects **may** differ slightly, viral clearance decreases as pH
> decreases and conductivity increases." — A-Mab

That last one carries three of these patterns at once: a concession in the front field, a hedge
(`may`), and two lexical verbs doing the work. It is 20 words long.

**Rule.** A claim that has a real counter-consideration states it in the same paragraph, marked.
This is the shape `WRITING_GUIDE.md` §2c ("one paragraph, one point") currently forbids, and the
reason the corpus reads as a sequence of unrelated assertions.

---

## 4. A finding is reported by a verb, and the qualification rides with it

**What the parse shows.** `show`, `indicate`, `demonstrate` and `confirm` head 143 sentences in the
mined pool. The qualification is attached to the same sentence, not deferred.

> "**Results showed** worst case at the following bioreactor conditions: High pH, high Temp, high
> iVCC, and late harvest." — A-Mab

> "Moreover, **results show that** process performance has been consistent and robust demonstrating
> that all three options may be used to culture cells in the seed expansion stage." — A-Mab

> "This prior information **has demonstrated that** the cell culture expansion steps are robust and
> reproducible in different scale of operations and bioreactor configurations." — A-Mab

> "Grey arrows **indicate** the effect was detected statistically **but is too small to have an
> appreciable effect** on the quality of the material produced." — A-Mab

The last one is the model for the whole problem: the finding and its limit are one sentence, and
the limit is stated in consequence terms rather than statistical ones.

---

## 5. Modality carries the risk posture

**What the parse shows.** `should` runs at 11.2 per 1000 words in PDA TR 60 and 7.3 in ISPE
Technology Transfer. In the corpus it is **0.0 in every document measured**. `may` and `can` run
3.0–11.7 in the sources against 0.4–1.8 in the corpus.

> "Temperature and pH **can affect** glycosylation (afucosylation and galactosylation levels),
> charge heterogeneity, host cell protein levels, and aggregate formation, and hence is considered
> high risk." — A-Mab

> "If pCO2 exceeds acceptable range it **can affect** process performance: peak VCC, integral of
> VCC, final titer, culture duration, growth rate, specific productivity, specific glucose
> consumption and specific lactate production." — A-Mab

> "Due to the dependence of aggregation on pH, the formulation range for pH **should not exceed**
> 5.6." — A-Mab

> "…a readiness assessment **should be conducted** to determine the timing of sufficient
> information and completion of activities to support moving forward with PPQ batch manufacture."
> — PDA TR 60

> "Moreover, results show that process performance has been consistent and robust demonstrating
> that all three options **may be used** to culture cells in the seed expansion stage." — A-Mab

**Rule.** A plan commits, permits and conditions: `will`, `may`, `should`, each doing different
work. A document that uses only `will` — PCP-003 runs `will` at 19.7 per 1000 words against a human
2.0–3.3 — has flattened three distinct stances into one.

---

## 6. The author manages the reader

**What the parse shows.** `we`/`our`, `Note that`/`Notice that` and `For example` are all **zero**
in the corpus. The sources use them to steer attention, to skip, and to say what is out of scope.

> "**Notice that** the limits on acidic variants and soluble aggregates are not exceeded within the
> ranges tested in the DOEs." — A-Mab

> "**If the reader is not interested** in studying the data and rationale that support the above
> statement, the reader can skip this section and go to Step 3 (Production Bioreactor)." — A-Mab

> "**Here, we recognize that** traditional approaches can span the gamut from using
> One-Factor-At-a-Time (OFAT) experiments to full DOEs…" — A-Mab

> "**However for purpose of brevity,** only data for MVM and XMuLV are provided in the case study."
> — A-Mab

**Rule.** Say what the reader should not spend attention on. A document that treats every attribute
identically forces the reader to weigh them all, and produces the uniform sections
`WRITING_GUIDE.md` §7 already calls a signal of machine authorship.

---

## 7. State the scope you are not covering

> "**For the purposes of this case study,** only a subset of quality attributes was considered…"
> — A-Mab

> "**In a real-life case scenario,** the examples and approaches described here would include all
> relevant product quality and material attributes." — A-Mab

> "This type of experimental design **is not able to resolve all the interactions** between
> parameters and it would have to be augmented on the subset of parameters shown to impact CQAs."
> — A-Mab

> "This 'one-factor-at-a-time' type of experimentation **cannot determine** process parameter
> interactions, where the effect of one parameter on a quality attribute differs depending on the
> level of the other parameters." — PDA TR 60

**Rule.** Name the limit of the method in the section that uses it. The corpus does this well once,
in PCR-003's "Three bounds apply to this claim", and almost nowhere else.

---

## How this becomes the guide

1. `WRITING_GUIDE.md` §2c and §2d gain the licensed exception: a paragraph may carry a claim and
   its counter-consideration, and the shapes in §1, §3 and §4 above are the forms it takes.
2. `REGISTER_EXEMPLAR.md` gains a moves catalogue built from these seven, keeping the file's
   existing arrangement by "the job each passage does". Every quote above is already verifiable by
   `check_exemplar_quotes.py`, since all of them come from `refs/text/`.
3. The parse features stay in the work unit as the **diagnosis**, and are re-run after the pilot
   re-author to see whether the shape moved. They are never given to an author as targets.

## Every quote here was checked

All quotes were tested as verbatim substrings of `refs/text/` under whitespace collapse: 24 of 25
passed on the first run. The one that failed — a sentence about sparger design — turned out to
**span a page break**, so `prose_from_extract` reconstructs it across the running header while the
raw file does not contain it contiguously. It was replaced rather than kept, because
`check_exemplar_quotes.py` is the gate that any of these must pass once they reach
`REGISTER_EXEMPLAR.md`, and a quote that needs a tolerance to pass is a quote worth swapping.

That is worth remembering when the exemplar is extended: a mined sentence may look verbatim and be
an artifact of the extractor's page-joining.
