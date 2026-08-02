"""Discourse-layer contracts — rhetorical roles and labelled weak claims.

Added in SCHEMA_VERSION 0.3, mirroring the benchmark corpus definition so ground truth
annexes parse unchanged.

Why this layer matters beyond annotation: a `claim` span and the `justification`
spans it points at are exactly the "is this statement supported by evidence?"
relation the pipeline must reproduce. `cross_step_credit` and `deferral` spans are
where a report hands a claim to a sibling document, which is the natural seed for
cross-document tracking — note, though, that in the corpus today those spans name the
target document only inside their quote text, with no machine-readable target field.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from .base import ExtractionMetadata, SourceReference

#: `commitment` was added at `SCHEMA_VERSION` 1.13 and the other eleven mirror the benchmark
#: corpus's own annotation scheme, so a ground truth annex still parses.
#:
#: A commitment is a promise the document makes: "will be measured", "shall be monitored". It
#: is not a `deferral`, which means "we cannot answer this yet". Measured on the corpus of
#: 2026-08-01: 227 sentences carry commitment language and 224 of them are in plans, so a plan
#: promises and its paired report is where the promise is discharged. Ground truth annotates
#: only two reports and no plan, so the new role collides with nothing that is scored.
RhetoricalRole = Literal[
    "problem_statement",
    "claim",
    "justification",
    "mechanistic_warrant",
    "hedge",
    "bounded_conclusion",
    "cross_step_credit",
    "deviation_disposition",
    "deferral",
    "restatement",
    "weak_claim",
    "commitment",
]

#: Roles that hand a claim to, or borrow a claim from, another document.
CROSS_DOCUMENT_ROLES: frozenset[str] = frozenset({"cross_step_credit", "deferral"})

WeaknessType = Literal[
    "unsupported_prior_knowledge",
    "overstated_outcome",
    "unbounded_generalization",
    "missing_citation",
]


class RhetoricalSpan(BaseModel):
    """A rhetorical-role span over the document text.

    ``supported_by`` links a claim to the spans that justify it, ``restates`` links a
    restatement back to its original, and ``bounds`` links a bounding statement to the
    claim it narrows.

    **A span covers one clause, not one sentence.** A sentence performs several acts at once:
    "HCP and residual DNA will be measured at harvest, but they will not be modelled, because
    both are cleared downstream" promises, declines and explains. Cutting at clause boundaries
    keeps one role per span and keeps spans from overlapping. Measured on the 60 ground truth
    spans of 2026-08-01: splitting them yields 77 clauses, 76 of which locate uniquely in their
    document, and 9 of the 10 spans carrying two roles separate cleanly. Overlap is allowed for
    the residue and is reported for review rather than resolved.
    """
    model_config = ConfigDict(extra="forbid")

    span_id: str
    section: Optional[str] = None
    role: RhetoricalRole
    source_reference: SourceReference
    supported_by: list[str] = Field(default_factory=list)
    restates: Optional[str] = None
    bounds: Optional[str] = None
    #: Documents this span hands something to, as the document writes them: "PCMR-001".
    #: Empty unless the role looks forward, which is `commitment`, `deferral` and
    #: `cross_step_credit`.
    #:
    #: Added at `SCHEMA_VERSION` 1.13 to close a gap this file has recorded since 0.3:
    #: `CROSS_DOCUMENT_ROLES` says those spans "name the target document only inside their
    #: quote text, with no machine-readable target field". Without it a reader can follow the
    #: link and a program cannot.
    #:
    #: **Not a duplicate of `DocumentRelationship`.** That model belongs to the typed
    #: extraction arm, hangs off `pharma_entities.py` and is scored by `benchmark/coverage.py`.
    #: The wiki arm has no equivalent, and this is the wiki's.
    #:
    #: A reference that resolves to no document in the wiki is reported to the Error Book and
    #: the span survives, because a citation that does not resolve is worse than none and a
    #: dropped span would hide it.
    targets: list[str] = Field(default_factory=list)


class WeakClaim(BaseModel):
    """A labelled unsupported or overstated claim — a benchmark negative.

    The quote appears verbatim in the document (so it is span-groundable like any other
    label) but is marked ``support="unsupported"``.

    Note: this layer is empty in every annex of the current corpus. The feature was
    retired because claims injected into a finished document collide with the prose
    around them, turning evidence-grounding into contradiction-detection. Metrics must
    therefore treat an empty ``weak_claims`` block as "no ground truth", not as "found nothing".
    """
    model_config = ConfigDict(extra="forbid")

    claim_id: str
    section: Optional[str] = None
    support: Literal["unsupported"] = "unsupported"
    weakness_type: WeaknessType
    source_reference: SourceReference
    rationale: Optional[str] = None
    correct_version: Optional[str] = None
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


# --------------------------------------------------------------------------- #
# Added in SCHEMA_VERSION 0.4                                                  #
# --------------------------------------------------------------------------- #
#: How one document relates to another. Every one of these appears in the benchmark
#: corpus, and none could be expressed before: "this report rolls up into PCMR-001",
#: "executed under PCP-006", "the scope was set by RA-001".
DocumentRelationKind = Literal[
    "rolls_up_into",
    "executed_under",
    "scoped_by",
    "supersedes",
    "superseded_by",
    "references",
]


class DocumentRelationship(BaseModel):
    """A stated relationship from this document to another one.

    This is the backbone of cross-document grounding and the typed contract could not
    express it at all. `RhetoricalSpan` comes closest, through `cross_step_credit` and
    `deferral`, but those name the target only inside their quote text — so the link
    exists for a human reader and not for a program.

    Recording the target as a field is the whole point. It is what lets a check ask
    "does PCMR-001 actually consolidate what the eight reports claim it does?" without
    someone first reading the prose to work out which documents to compare.
    """
    model_config = ConfigDict(extra="forbid")

    relationship_id: str
    kind: DocumentRelationKind
    #: The document making the statement.
    source_document_id: str
    #: The document referred to, as written — "PCMR-001", "the master report". Resolving
    #: it to a known document is a later step and may fail; the raw form is kept so a
    #: failed resolution is visible rather than silently dropped.
    target_document_ref: str
    statement: Optional[str] = None
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class ExplicitNonClaim(BaseModel):
    """Something the document states it does *not* establish.

    "The step provides no clearance of the non-enveloped model virus MVM (0 log10)."
    "No parameter is a CPP, because the operation forms no product-quality attribute."

    An asserted absence is not the same as silence, and the typed contract collapsed the
    two: both came out as an empty list. That is the single most dangerous equivalence in
    a regulated summary, because a reader takes the more reassuring reading — and here the
    reassuring reading is wrong in one direction and right in the other, with no way to
    tell which.

    Two whole unit operations in the benchmark corpus are justified largely on non-claims:
    harvest and UF/DF form no quality attribute, and say so deliberately.
    """
    model_config = ConfigDict(extra="forbid")

    non_claim_id: str
    #: What is being denied — "MVM clearance", "product-quality CQA", "CPP".
    subject: str
    unit_operation: Optional[str] = None
    statement: str = ""
    #: Why the absence holds, when the document gives a reason. "Because low-pH
    #: inactivation is effective only against enveloped viruses."
    rationale: Optional[str] = None
    #: Where the thing *is* established instead, when the document says so — the
    #: orthogonal step, the other programme. Without this a non-claim reads as a gap
    #: rather than as a deliberate division of responsibility.
    handled_elsewhere: Optional[str] = None
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)
