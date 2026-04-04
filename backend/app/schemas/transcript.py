"""
MedOrbit — Transcript Schemas (Pydantic v2)

Request/response models for transcript chunk ingestion and retrieval.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


# ── Enums ────────────────────────────────────────────────────

class SpeakerRole(str, Enum):
    DOCTOR = "doctor"
    PATIENT = "patient"
    SYSTEM = "system"


class SourceType(str, Enum):
    MANUAL = "manual"
    TRANSCRIBED = "transcribed"
    SIMULATED = "simulated"


# ── Request Schemas ──────────────────────────────────────────

class ChunkCreateRequest(BaseModel):
    """Single transcript chunk to ingest."""
    speaker_role: SpeakerRole = Field(..., examples=["doctor"])
    speaker_label: Optional[str] = Field(None, max_length=100, examples=["Dr. Chen"])
    text: str = Field(..., min_length=1, max_length=10000, examples=["How are you feeling today?"])
    sequence_number: Optional[int] = Field(
        None,
        ge=1,
        description="Optional. Auto-assigned if omitted.",
        examples=[1],
    )
    source_type: SourceType = Field(default=SourceType.MANUAL, examples=["manual"])


class BulkChunkCreateRequest(BaseModel):
    """Multiple transcript chunks to ingest at once."""
    chunks: List[ChunkCreateRequest] = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Array of chunks. sequence_number will be auto-assigned if omitted.",
    )


# ── Response Schemas ─────────────────────────────────────────

class ChunkResponse(BaseModel):
    """Public representation of a transcript chunk."""
    id: str
    visit_id: str
    sequence_number: int
    speaker_role: SpeakerRole
    speaker_label: Optional[str]
    text: str
    source_type: SourceType
    created_at: datetime

    model_config = {"from_attributes": True}


class TranscriptPlaintextResponse(BaseModel):
    """Full transcript as formatted plaintext."""
    visit_id: str
    text: str
    chunk_count: int


class BulkCreateResponse(BaseModel):
    """Response for bulk ingestion."""
    visit_id: str
    chunks_created: int
    chunks: List[ChunkResponse]
