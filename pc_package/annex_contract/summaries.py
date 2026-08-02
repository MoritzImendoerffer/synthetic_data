"""Phase 7 — summary/report output contracts (boilerplate).

The generation logic (nlp_reports/pipelines/run_transfer_summary.py) is a TODO stub;
these contracts are final enough for a less capable model to code against.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

from .base import ExtractionMetadata, SourceReference
from .inventory import DocumentInventoryItem
from .pharma_entities import (
    AnalyticalMethod,
    Equipment,
    ManufacturingSite,
    ProcessParameter,
    ProcessStep,
    QualityAttribute,
)


class TransferGap(BaseModel):
    gap_id: str
    gap_area: Literal[
        "process", "equipment", "materials", "analytical_method", "control_strategy",
        "validation", "facility", "quality_system", "documentation", "other",
    ]
    description: str
    impact: Optional[str] = None
    mitigation: Optional[str] = None
    status: Optional[Literal["open", "in_progress", "closed", "unknown"]] = "unknown"
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class ReportStatement(BaseModel):
    """A single sentence/claim in a generated report, with statement-level citations."""
    statement_id: str
    statement_text: str
    #: Why this sentence was written, in the producer's own words. Added at
    #: `SCHEMA_VERSION` 1.5.
    #:
    #: A report said what it claimed and never why. A reviewer reading a statement beside
    #: its citation could see the quote and could not see which fact the sentence was built
    #: from, so a correct fact restated wrongly looked exactly like a correct restatement.
    #: `nlp_reports/summaries/sectionwise.py` asks the model for one. `nlp_reports/fastlane/report.py` writes
    #: no model text at all and states its routing instead, which is what a reviewer needs to
    #: fix a mis-routed fact.
    #:
    #: **A rationale is never evidence.** It carries no `SourceReference` and cannot get one.
    #: No metric reads it. It is shown to the human reviewer and to the repair step, and it
    #: is never sent to the blind judge: it is the builder's own account of its reasoning,
    #: and a judge that sees it is no longer independent of the builder. `JudgeItem` has no
    #: field it could occupy, and a test asserts that field set.
    rationale: str = ""
    supporting_assertion_ids: list[str] = Field(default_factory=list)
    source_references: list[SourceReference] = Field(default_factory=list)
    confidence: Literal["low", "medium", "high"] = "medium"
    review_status: Literal["not_reviewed", "accepted", "rejected", "needs_clarification"] = "not_reviewed"


class ReportSection(BaseModel):
    section_id: str
    title: str
    statements: list[ReportStatement] = Field(default_factory=list)
    #: What a reader must be told about this section itself, printed under the heading.
    #:
    #: A capped section is the case this exists for. The count of what was left out used to
    #: live only in the report's `notes`, which the Markdown renderer had no parameter for
    #: and never printed. A report quietly showing the first twenty facts reads exactly like
    #: a report of twenty facts.
    note: str = ""


class ProcessTransferPackageSummary(BaseModel):
    summary_id: str
    product_name: Optional[str] = None
    process_name: Optional[str] = None
    objective: Optional[str] = None
    sending_sites: list[ManufacturingSite] = Field(default_factory=list)
    receiving_sites: list[ManufacturingSite] = Field(default_factory=list)
    documents_reviewed: list[DocumentInventoryItem] = Field(default_factory=list)
    process_steps: list[ProcessStep] = Field(default_factory=list)
    CPPs: list[ProcessParameter] = Field(default_factory=list)
    CQAs: list[QualityAttribute] = Field(default_factory=list)
    analytical_methods: list[AnalyticalMethod] = Field(default_factory=list)
    key_equipment: list[Equipment] = Field(default_factory=list)
    control_strategy_elements: list[str] = Field(default_factory=list)
    gaps: list[TransferGap] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    narrative_sections: list[ReportSection] = Field(default_factory=list)
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)
