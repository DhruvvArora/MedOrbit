from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.schemas.reminder import ReminderResponse


class PatientVisitDetailResponse(BaseModel):
    """
    Highly scrubbed payload ensuring the patient NEVER sees raw AI drafts,
    clinical flags, or the doctor's dense summary.

    NOTE: The field ``patient_discharge_draft`` is named after the DB column.
    Patient-facing UIs MUST relabel it (e.g. "Approved Care Instructions").
    """
    visit_id: int
    title: str
    status: str
    started_at: Optional[datetime] = None
    has_approved_report: bool
    simplified_explanation: Optional[str] = None
    patient_discharge_draft: Optional[str] = None

    class Config:
        from_attributes = True


class PatientDashboardSummary(BaseModel):
    """Aggregated view-model for the patient dashboard."""
    patient_id: str
    patient_name: str
    visit_count: int
    pending_report_count: int
    pending_reminder_count: int
    visits: List[PatientVisitDetailResponse]
    recent_reminders: List[ReminderResponse]


class PatientReminderItem(BaseModel):
    """Flat representation of a reminder bound to its parent visit."""
    visit_id: int
    visit_date: datetime
    task: str
