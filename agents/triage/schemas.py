from typing import List, Optional

from pydantic import BaseModel, Field

class SymptomEvidence(BaseModel):
    """A specific symptom linked to exact transcript observations."""
    symptom: str = Field(description="The primary symptom reported.")
    duration: str = Field(description="How long the symptom has persisted, if mentioned.")
    severity: str = Field(description="Severity cues like 'mild', 'sharp', '7 out of 10'.")
    evidence_snippet: str = Field(description="A short quote from the text as proof.")


class TriageInsightOutput(BaseModel):
    """The structured output for the Clinical Triage Agent."""
    summary: str = Field(
        description="A concise 1-2 sentence clinical summary of the encounter."
    )
    chief_complaint: str = Field(
        description="The primary reason the patient is seeking care."
    )
    symptoms: List[SymptomEvidence] = Field(
        default_factory=list,
        description="List of symptoms reported by the patient."
    )
    medication_mentions: List[str] = Field(
        default_factory=list,
        description="List of medications or supplements discussed."
    )
    history_mentions: List[str] = Field(
        default_factory=list,
        description="List of past medical history conditions mentioned."
    )
    risk_flags: List[str] = Field(
        default_factory=list,
        description="Priority clinical warnings like 'struggling to breathe' or 'sudden severe pain'."
    )
    follow_up_questions: List[str] = Field(
        default_factory=list,
        description="Key clinical questions the doctor should ask to gather missing triage context."
    )
    candidate_discharge_points: List[str] = Field(
        default_factory=list,
        description="Draft points for a care plan based ONLY on what was discussed."
    )
    cautionary_notes: List[str] = Field(
        default_factory=list,
        description="Automated disclaimers, such as 'AI generated summary only, verify clinically'."
    )
