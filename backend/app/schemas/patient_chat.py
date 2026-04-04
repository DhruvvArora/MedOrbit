from pydantic import BaseModel, Field
from typing import Optional

class PatientChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="The textual question submitted by the patient.")

class PatientChatResponse(BaseModel):
    answer: str
    is_supported: bool
    refusal_reason: Optional[str] = None
    safety_note: str
