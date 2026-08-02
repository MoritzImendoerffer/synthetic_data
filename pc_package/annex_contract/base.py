"""Base provenance and extraction-metadata contracts.

Every extracted fact in the system carries a SourceReference (where it came
from) and ExtractionMetadata (how it was produced). These two models are the
foundation of the whole audit trail — do not extract anything without them.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

# 0.3 — additive: widened ParameterType (WC-CPP, GPP) and DocumentType (+4 values),
#       structured criticality on QualityAttribute, and the studies/discourse/annex
#       models. Nothing was removed or narrowed, so 0.2 payloads still validate.
# 0.5 — additive: SourceReference.char_frame. Character offsets were already being
#       written in three mutually incompatible coordinate systems with nothing to say
#       which; see CharFrame. Existing payloads validate with char_frame unset.
# 0.6 — additive: ErrorKind gains "over_specific_type". Measured on the wiki of
#       2026-07-28: one model wrote 33 of its 45 entity types with a parenthetical
#       qualifier, so 29 types had exactly one page each and the wiki could not be
#       browsed by kind. Existing error books validate; none carries the new value.
# 0.7 — additive: WikiProvenance.response_sha256, so a wiki records which offline answer
#       it was built from. An answer file on disk can be overwritten by anything, and one
#       was; the artifact had no way to say which build it came from.
# 0.8 — additive: WikiProvenance.seeded_from, so a wiki primed with an earlier wiki's
#       vocabulary says so. A reader comparing two wikis has to know whether the second
#       reached the same names on its own or was handed them.
# 0.9 — additive: WikiPage.page_class. A wiki page can be a kind of thing, one occurrence
#       of one, or a document, and all three were filed together under `concepts/`.
# 1.5 — additive: ReportStatement.rationale, and the whole of nlp_reports/models/trace.py. A report
#       said what it claimed and never why it claimed it, so a reviewer reading a statement
#       beside its citation could not see which fact the sentence was built from. The
#       rationale is authored text about reasoning and is never evidence: it carries no
#       SourceReference, no metric reads it, and the blind judge never receives it. Existing
#       payloads validate with rationale unset.
# 1.6 — additive: WikiFact.fact_id, a content hash over the fact's page, claim and evidence
#       coordinates. Every consumer minted `<entity_id>#<index>` instead, which is
#       positional: a rebuild that reorders facts repoints every stored verdict, and nothing
#       warns. Existing wikis validate with fact_id unset, and WikiPage computes it on load.
# 1.7 — widening, with one changed default: HumanRating.verdict is Optional and defaults to
#       None rather than "cannot_tell". A reviewer can say what is wrong with a claim without
#       choosing one of six words for it, and the first real sitting did: 8 of 56 items came
#       back with a repair_hint and a corrected value and no verdict. ratings_from_export
#       discarded all 8, so six caught planted errors and the two sharpest findings in the
#       batch never reached a metric, and the surviving data read as "all supported" with a
#       kappa of 0. None is not cannot_tell: the old default conflated "did not answer" with
#       "the premise does not settle it", which is the distinction the metric rests on. No
#       stored rating relied on the old default — all 47 in the bundle carry an explicit
#       verdict — so nothing on disk changes meaning.
# 1.8 — additive: RepairTarget gains "link". A wiki fact carries `links_to`, and the viewer
#       renders each target as an edge a reviewer can follow. An edge that points at the wrong
#       page was the one defect a reviewer could see and had no way to report: the three
#       existing targets change a rationale, a statement or a citation, and none of them
#       touches the graph. `repair._apply_link` edits `WikiFact.links_to` on the wiki, so
#       `repair.apply` now takes the wiki it is to change. Existing proposals never carry the
#       new value and are unaffected.
# 1.9 — additive: EvidenceItem.origin and EvidenceItem.fact_id. A brief can now draw evidence
#       from the wiki as well as from the concept store and the value claims, and a reader
#       judging a section has to see which store a fact came from. Two stores disagreeing about
#       one parameter is the case a reviewer is being asked about, so a brief that merged them
#       silently would hide it. `fact_id` is the wiki's content hash and never a positional
#       index: a signed brief outlives the build it was made from. `origin` defaults to
#       "concepts", which is what every stored brief was drawn from, so nothing on disk changes
#       meaning.
# 1.10 — additive: TemplateChange, FitSnapshot and template_content_hash in models/fastlane.py.
#       A template decides what a report contains, and nothing recorded why one changed.
#       `ChangeRecord` answers that question for a repair to a report; this answers it for a
#       change to the template. `FitSnapshot` carries the per-section distribution and not
#       only the unplaced total, because the total is gameable: one section asking for the
#       commonest words in the corpus drives it to zero and helps no reader.
#       `template_content_hash` covers an enumerated field set, so what counts as a new
#       version is defined rather than judged. No existing model changed.
# 1.11 — additive: ReaderFlag in models/trace.py, and SamplingMode gains "reader_flag". The
#       wiki site lets a reader hover a citation and read its whole source document, which is
#       a good way to notice a wrong fact and a bad way to produce a rate: a reader flags what
#       caught their eye, and what catches an eye is not a sample. `ReaderFlag` has no
#       `verdict` field, so `agreement` cannot read one as a rating; the new sampling mode
#       keeps a flagged trace out of `population_rate`, which accepts only "random"; and
#       `scope` is fixed to "document" because a reader who can hover the whole source judges
#       at document scope whatever they think they are doing. Existing selections never carry
#       the new value and are unaffected.
# 1.12 — additive: PageContract and ScopeRule in models/fastlane.py, a `page_contracts` field
#       on OutputTemplate, and the `unscoped_page` ErrorKind in models/wiki.py. A fact is
#       often true only inside a narrower context: a process parameter's operating range
#       holds for one step and not the others. The wiki recorded that context three ways and
#       chose between them by build order. Measured on the wiki of 2026-07-31: the `step`
#       qualifier on 357 of 1,559 facts, a bracket in the page name on 49 of 175 pages, and
#       neither on 15 of the 37 process parameter pages. `prompts.py:494` already told the
#       extractor the context is not part of `entity_type`, and never said which field it
#       belongs in.
#       **Which kinds are scoped is template content, never code.** `PageContract` is keyed
#       by a kind string from `entity_kinds` and `ScopeRule` names a qualifier key and the
#       kind its values come from. Nothing in `nlp_reports/` knows what a step is, so a
#       different document set declares a different pair and changes no Python.
#       `page_contracts` joins `VERSION_BEARING_FIELDS`, because a contract changes what a
#       wiki contains and two templates differing only in it are two templates. A template
#       written before this validates and reports an empty list.
# 1.14 — additive: `PageContract.must_cover`, what a page of one entity kind must carry. The
#       20 source-document pages of the wiki of 2026-07-31 hold 7,309 characters of claim text
#       about 801,781 characters of source document, 109 to 1, and `wiki_default` said nothing
#       about what such a page should contain. The extractor was told a source document
#       deserves a page and nothing about what belongs on one, so the template was behaving
#       exactly as written and the fix belongs in the template.
#       Rendered into the extraction prompt as a floor and not a ceiling, in the way
#       `entity_kinds` is rendered as a menu and not a closed list. Empty asks nothing, which
#       is the right answer for a kind whose pages already carry what they should.
#       `page_contracts` was already version-bearing at 1.12, so nothing changes about how a
#       template's identity is computed.
# 1.13 — additive: `Wiki.discourse` and `Wiki.non_claims`, a twelfth `RhetoricalRole` named
#       `commitment`, and `RhetoricalSpan.targets`. A characterization report does not only
#       measure. It concludes, bounds, declines to claim and promises, and a wiki fact —
#       `(predicate, object)` with a quote — can hold none of those. Measured on the wiki of
#       2026-08-01: 4 of the 8 unit operation pages carried no conclusion-shaped fact at all,
#       and searching the whole wiki for two conclusions stated in PCR-003's executive summary
#       returned 0 facts. 227 sentences in the corpus carry commitment language, 224 of them in
#       plans, and nothing could store one.
#       `RhetoricalSpan` and `ExplicitNonClaim` have been in the contract since 0.3 and nothing
#       has ever produced either, so this gives them somewhere on the wiki to land.
#       `targets` closes a gap this contract has recorded since 0.3: `CROSS_DOCUMENT_ROLES`
#       says `deferral` and `cross_step_credit` "name the target document only inside their
#       quote text, with no machine-readable target field". It is not a duplicate of
#       `DocumentRelationship`, which belongs to the typed arm and is scored by
#       `benchmark/coverage.py`; the wiki arm had no equivalent.
#       Adding a `Literal` member does not change how existing values parse, so a ground truth
#       annex still loads. A test asserts that against a real annex file rather than a fixture.
# 1.15 — additive: `LocalBinding`, `Wiki.bindings`, and two `ErrorKind` members,
#       `unresolved_qualifier` and `missing_binding`. `WikiFact.qualifiers` is a free
#       dictionary: no key is required and no value is checked, so the extractor writing the
#       right context and the extractor writing nothing produce the same well-formed wiki.
#       Measured on the wiki of 2026-07-31 by `run_fastlane qualifier-fit`: of 825 qualifier
#       values, 161 name a page and add a suffix so nothing can join on them, and 38 pack a
#       symbol and its expansion into one string. A reviewer rejected 6 claims of that second
#       shape on 2026-08-01, and 5 of the 6 named the right factor in a field nothing checked.
#       A binding is scoped to one document, which is the field that makes it different from
#       `WikiPage.aliases`. `A` reads four ways across four documents in this corpus and every
#       reading is correct inside its own document, so a corpus-wide vocabulary cannot hold
#       one and a corpus-wide consistency check would report four false contradictions.
#       `binding_kind` is a free string for the reason `entity_type` is: run 3 measured a
#       closed schema discarding 56% to 61% of what documents say.
#       Adding a `Literal` member does not change how existing values parse, so a ground truth
#       annex still loads, and a wiki written before this loads with `bindings` empty. Tests
#       assert both against real files rather than fixtures.
# 1.16 — additive: `OutputTemplate.scoping_qualifiers`, which names the qualifier keys that
#       narrow *what is being claimed* rather than recording where it was written.
#       `detect_contradictions` reads it and nothing else does. That detector grouped facts by
#       `(page, normalized predicate)` and never read `qualifiers`, so two facts about
#       different things were compared as though they were two readings of one quantity.
#       Measured on 2026-08-02 across every stored wiki: 13 contradictions have ever been
#       reported, and reading all 13 by hand, 4 are real and 9 are false. On the wiki of
#       2026-07-31, four of the six compare one factor's screening effect against another's
#       across two different unit operations.
#       The split is not "any qualifier differs". A key such as `stated_in` records where a
#       value was written, and one document stating two capability indices in two of its own
#       sections is exactly the inconsistency worth reporting: two builds of one corpus both
#       found that pair. So the keys are declared rather than inferred, and a key left out
#       keeps its pairs comparable.
#       It joins `VERSION_BEARING_FIELDS`, which widens what that tuple means. The field
#       reaches no prompt, so two templates differing only in it ask for identical wikis. What
#       differs is the Error Book those wikis carry, and a build's own account of what is wrong
#       with it is part of what the build produces.
#       Empty declares nothing and changes no finding, so a template written before this
#       behaves exactly as it did.
# 1.17 — additive: `SourceRecord`, `Wiki.sources`, and the `stale_source` error kind. A wiki
#       recorded which documents it read and nothing about which VERSION. `document_id` is
#       content-addressed — `doc_<stem>_<sha256[:8]>` — so a re-issued report parses to a new
#       id beside the old one, `run_parse` never removes the superseded parse, and
#       `wiki --update` then sends the new document while the wiki keeps the facts it already
#       had from the old. One report becomes two documents that disagree. Demonstrated on
#       2026-08-02, and the median document on the wiki of 2026-07-31 carries 73 facts.
#       Worse, `benchmark.wiki_recall.covers` joins ground truth on the document STEM, so both
#       revisions satisfy the same ground truth document and a wiki holding two scores against
#       ground truth twice. Ground truth value recall is the figure this project treats as
#       stable, so a defect that inflates it is worse than one that inflates a fact count.
#       A superseded document is two `SourceRecord`s sharing a `file_name` with different
#       hashes, which is why the list accumulates rather than being replaced in place: the
#       two revisions have different ids and neither overwrites the other.
#       `Wiki.sources` is NOT version-bearing. `VERSION_BEARING_FIELDS` describes what an
#       `OutputTemplate` asks a build for; a wiki already records `WikiProvenance` per build.
#       Empty means the wiki predates the field, never that it read nothing — `document_ids`
#       still says what it read — so every consumer reports `n/a` for an empty list.
SCHEMA_VERSION = "1.17"

#: Which string `SourceReference.char_start` and `char_end` index into.
#:
#: These offsets were written in three different coordinate systems before this field
#: existed, and a consumer holding a reference could not tell them apart:
#:
#:   element   `DocumentElement.text`            — `DocumentIndex.resolve`, the common path
#:   document  `DocumentIndex.citable_text`      — `DocumentIndex.reference_at`
#:   section   `ParsedDocument.section_text(...)` — the spaCy path, and the review adapter
#:                                                  removed on 2026-08-02
#:
#: The three are not interchangeable and the difference is invisible: two tests pinned
#: opposite behaviours, and that review adapter worked around it by re-finding every
#: offset with `str.find` rather than trusting the one it had been handed. `None` means the
#: producer did not record a frame, which for anything written before 0.5 means "unknown" —
#: read the quote instead.
CharFrame = Literal["element", "section", "document"]

ReviewStatus = Literal["not_reviewed", "accepted", "rejected", "needs_clarification"]
Confidence = Literal["low", "medium", "high"]
Basis = Literal["explicit", "inferred", "unknown", "unsupported"]
ExtractionSource = Literal["spacy_rule", "spacy_model", "llm", "coding_assistant", "human", "hybrid", "table", "rule"]


#: Which corner of the page a bounding box's coordinates are measured from.
#:
#: PDF native is bottom-left and most viewers are top-left, so a rectangle without this is
#: a rectangle in the wrong half of the page. This is the same defect `CharFrame` exists for:
#: offsets were written in three coordinate systems with nothing recording which, and the
#: difference was invisible until something drew in the wrong place.
CoordOrigin = Literal["BOTTOMLEFT", "TOPLEFT"]


class BoundingBox(BaseModel):
    """Where something sits on a page, in the page's own coordinate space.

    `y0` is always the smaller number and `y1` the larger. Which of them is visually the top
    depends on `coord_origin`: with `BOTTOMLEFT`, `y1` is nearer the top of the page.
    """

    page: int
    x0: float
    y0: float
    x1: float
    y1: float
    coord_origin: CoordOrigin = "BOTTOMLEFT"


class SourceReference(BaseModel):
    document_id: str
    document_title: Optional[str] = None
    file_name: Optional[str] = None
    section_id: Optional[str] = None
    section_title: Optional[str] = None
    heading_path: list[str] = Field(default_factory=list)
    element_id: Optional[str] = None
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    table_id: Optional[str] = None
    table_title: Optional[str] = None
    char_start: Optional[int] = None
    char_end: Optional[int] = None
    #: Which string the two offsets above index. Without this they are unusable: see
    #: `CharFrame`. Always set it when you set an offset.
    char_frame: Optional[CharFrame] = None
    bounding_boxes: list[BoundingBox] = Field(default_factory=list)
    quote: Optional[str] = None  # keep short; avoid huge excerpts


class ExtractionMetadata(BaseModel):
    schema_version: str = SCHEMA_VERSION
    extraction_source: ExtractionSource = "hybrid"
    confidence: Optional[Confidence] = None
    basis: Basis = "unknown"
    model: Optional[str] = None
    prompt_id: Optional[str] = None
    run_id: Optional[str] = None
    timestamp_utc: Optional[str] = None
    human_review_status: ReviewStatus = "not_reviewed"
    reviewer: Optional[str] = None
    review_notes: Optional[str] = None
