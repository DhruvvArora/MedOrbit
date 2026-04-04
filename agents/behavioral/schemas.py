from typing import List

from pydantic import BaseModel, Field

class InsightEvidence(BaseModel):
    """A specific observation linked to a transcript snippet."""
    observation: str = Field(description="The behavioral or psychosocial observation.")
    evidence_snippet: str = Field(description="A short quote from the transcript supporting this observation.")
    confidence: str = Field(description="'high', 'medium', or 'low'")


class BehavioralInsightOutput(BaseModel):
    """The structured output for the Behavioral Health Insight Agent."""
    summary: str = Field(
        description="A concise 1-2 sentence summary of the behavioral/emotional state."
    )
    emotional_signals: List[InsightEvidence] = Field(
        default_factory=list,
        description="List of emotional tones, stress cues, or anxiety indicators."
    )
    adherence_risk: List[InsightEvidence] = Field(
        default_factory=list,
        description="List of potential risks to medication adherence or care plan follow-through."
    )
    psychosocial_factors: List[str] = Field(
        default_factory=list,
        description="Lifestyle, work stress, or social factors impacting health."
    )
    communication_flags: List[str] = Field(
        default_factory=list,
        description="Flags like 'confusion', 'hesitation', or 'resistance'."
    )
    suggested_follow_up_questions: List[str] = Field(
        default_factory=list,
        description="Supportive questions the doctor could ask to explore these concerns."
    )
    cautionary_notes: List[str] = Field(
        default_factory=list,
        description="Automated disclaimers, such as 'AI inference only, verify clinically'."
    )
