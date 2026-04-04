from typing import List

from pydantic import BaseModel, Field

class SuperAgentDraftOutput(BaseModel):
    """The structured orchestration output merging prior agent streams."""
    visit_id: str = Field(description="The ID of the visit.")
    doctor_summary: str = Field(description="Dense, highly clinical summary designed for EMR charting and doctor review.")
    patient_discharge_draft: str = Field(description="Gentle, instructional care plan the patient can take home.")
    simplified_explanation: str = Field(description="Accessible explanation at a 5th-grade reading level.")
    clinical_review_flags: List[str] = Field(
        default_factory=list,
        description="Priority clinical/behavioral warnings merged from sub-agents needing doctor attention before discharge."
    )
    reminder_candidates: List[str] = Field(
        default_factory=list,
        description="Action-oriented checklist tasks the patient needs to follow up on."
    )
    cautionary_notes: List[str] = Field(
        default_factory=list,
        description="Automated disclaimers, must include: 'DRAFT ONLY - Requires physician approval'."
    )
