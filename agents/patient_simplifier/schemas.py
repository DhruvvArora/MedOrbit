from typing import Optional
from pydantic import BaseModel, Field

class PatientSimplifierOutput(BaseModel):
    """Structured response from the Patient Simplifier LLM ensuring safe outputs."""
    is_supported: bool = Field(description="True if the patient's question can be fully answered using ONLY the provided document context.")
    answer: str = Field(description="The simplified explanation or refusal message directly addressing the patient.")
    refusal_reason: Optional[str] = Field(description="If is_supported is false, explain why internally (e.g. 'Out of scope medical question', 'Symptom triage required').")
