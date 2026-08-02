"""Phase 2 — inventory and classification contracts."""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

from .base import ExtractionMetadata, SourceReference

DocumentType = Literal[
    "process_characterization_report",
    "process_validation_report",
    "technology_transfer_protocol",
    "technology_transfer_report",
    "control_strategy",
    "analytical_method",
    "analytical_method_validation_report",
    "specification",
    "batch_record",
    "risk_assessment",
    "manufacturing_process_description",
    "unknown",
    # Added in SCHEMA_VERSION 0.3. A characterization campaign is planned and reported at
    # two levels — per unit operation, then rolled up — and none of the values above can
    # express the plan or the roll-up. See docs/BENCHMARK.md.
    "process_transfer_plan",
    "process_characterization_plan",
    "process_characterization_master_plan",
    "process_characterization_master_report",
]

#: Document types whose content is a roll-up of other documents. Cross-document
#: grounding treats these as the *summary* side of a comparison.
ROLLUP_DOCUMENT_TYPES: frozenset[str] = frozenset({
    "process_characterization_master_report",
    "process_characterization_master_plan",
    "technology_transfer_report",
    "control_strategy",
})


class DocumentInventoryItem(BaseModel):
    document_id: str
    file_name: str
    file_hash: Optional[str] = None
    predicted_document_type: DocumentType = "unknown"
    product_name_candidates: list[str] = Field(default_factory=list)
    process_name_candidates: list[str] = Field(default_factory=list)
    site_candidates: list[str] = Field(default_factory=list)
    date_candidates: list[str] = Field(default_factory=list)
    main_topics: list[str] = Field(default_factory=list)
    rationale: Optional[str] = None
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class Inventory(BaseModel):
    run_id: Optional[str] = None
    items: list[DocumentInventoryItem] = Field(default_factory=list)
