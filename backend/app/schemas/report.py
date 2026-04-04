from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class VisitReportUpdate(BaseModel):
    """Used for PATCHing a report while it is in DRAFT state."""
    doctor_summary: Optional[str] = None
    patient_discharge_draft: Optional[str] = None
    simplified_explanation: Optional[str] = None
    clinical_review_flags: Optional[List[str]] = None
    reminder_candidates: Optional[List[str]] = None


class VisitReportResponse(BaseModel):
    """Returned cleanly to the UI."""
    id: int
    visit_id: int
    status: str
    doctor_summary: Optional[str] = None
    patient_discharge_draft: Optional[str] = None
    simplified_explanation: Optional[str] = None
    clinical_review_flags: Optional[List[str]] = None
    reminder_candidates: Optional[List[str]] = None
    approved_by_id: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
