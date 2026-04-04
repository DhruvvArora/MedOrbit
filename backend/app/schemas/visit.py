"""
MedOrbit — Visit Schemas (Pydantic v2)
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.auth import UserResponse

# ── Enums ────────────────────────────────────────────────────


class VisitType(str, Enum):
    VIRTUAL = "virtual"
    IN_PERSON = "in_person"


class VisitStatus(str, Enum):
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# ── Request Schemas ──────────────────────────────────────────


class VisitCreateRequest(BaseModel):
    """Payload to create a new visit."""

    patient_id: str = Field(..., examples=["uuid"])
    type: VisitType = Field(..., examples=["virtual"])
    title: Optional[str] = Field(None, max_length=255, examples=["Routine Checkup"])


# ── Response Schemas ─────────────────────────────────────────


class VisitResponse(BaseModel):
    """Public visit representation."""

    id: str
    doctor_id: str
    patient_id: str
    type: VisitType
    status: VisitStatus
    title: Optional[str]

    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
