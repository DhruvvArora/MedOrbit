from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class PatientVisitDetailResponse(BaseModel):
    """
    Highly scrubbed payload ensuring the patient NEVER sees raw AI drafts, 
    clinical flags, or the doctor's dense summary.
    """
    visit_id: int
    title: str
    status: str
    started_at: Optional[datetime]
    has_approved_report: bool
    simplified_explanation: Optional[str] = None
    patient_discharge_draft: Optional[str] = None

    class Config:
        from_attributes = True

class PatientReminderItem(BaseModel):
    """Flat representation of a reminder bound to its parent visit."""
    visit_id: int
    visit_date: datetime
    task: str
