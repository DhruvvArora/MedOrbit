from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class ReminderResponse(BaseModel):
    id: int
    visit_id: int
    patient_id: int
    title: str
    status: str
    due_at: datetime
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReminderStatusUpdate(BaseModel):
    status: str = Field(..., description="Must be one of: PENDING, COMPLETED, SKIPPED")
