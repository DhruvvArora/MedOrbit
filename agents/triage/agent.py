import os
from typing import Optional

from agents.shared.llm import execute_structured_prompt
from agents.triage.schemas import TriageInsightOutput, SymptomEvidence
from agents.triage.prompts import (
    TRIAGE_AGENT_SYSTEM_PROMPT,
    build_triage_user_prompt
)

class TriageInsightAgent:
    """
    Analyzes a consultation transcript to generate a structured clinical triage intake mapping.
    """

    def _get_mock_output(self) -> TriageInsightOutput:
        """Returns a safe mock payload when no API key is present."""
        return TriageInsightOutput(
            summary="Patient presents with elevated blood pressure readings seeking intake consultation.",
            chief_complaint="Consistently high blood pressure over the past few months.",
            symptoms=[
                SymptomEvidence(
                    symptom="Knee pain",
                    duration="Recent",
                    severity="Hurts when jogging",
                    evidence_snippet="I was trying to start jogging but my knee started hurting."
                ),
                SymptomEvidence(
                    symptom="Tension headaches",
                    duration="Lately",
                    severity="Moderate with chest tightness",
                    evidence_snippet="Sometimes I get these tension headaches and my chest feels tight."
                )
            ],
            medication_mentions=["Blood pressure medication (Mother's history)"],
            history_mentions=["Father had heart attack at 58", "Mother has high blood pressure", "Quit smoking 3 years ago"],
            risk_flags=["Reports occasional chest tightness accompanying anxiety/stress", "Stage 1 hypertension range readings (145/95)"],
            follow_up_questions=[
                "Can you describe the chest tightness in more detail?",
                "Have you experienced any shortness of breath?"
            ],
            candidate_discharge_points=[
                "Reduce sodium intake to under 2300 mg per day.",
                "Incorporate at least 30 minutes of moderate exercise.",
                "Improve sleep hygiene.",
                "Follow up in two weeks to review labs and plan."
            ],
            cautionary_notes=["AI generated summary only, verify clinically.", "[MOCK MODE ENGAGED]"]
        )

    def analyze(self, transcript_text: str) -> TriageInsightOutput:
        """
        Executes the clinical triage agent.
        
        Args:
            transcript_text: The formatted plaintext of the transcript.
            
        Returns:
            TriageInsightOutput: The structured JSON response.
        """
        if not transcript_text or len(transcript_text.split()) < 20:
            return TriageInsightOutput(
                summary="Insufficient data for clinical triage analysis.",
                chief_complaint="None recorded",
                symptoms=[],
                medication_mentions=[],
                history_mentions=[],
                risk_flags=[],
                follow_up_questions=[],
                candidate_discharge_points=[],
                cautionary_notes=["Transcript too short or empty."]
            )

        # Handle Mock Mode
        if not os.environ.get("OPENAI_API_KEY"):
            return self._get_mock_output()

        user_prompt = build_triage_user_prompt(transcript_text)

        result = execute_structured_prompt(
            system_prompt=TRIAGE_AGENT_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=TriageInsightOutput,
            temperature=0.1
        )
        
        # Ensure mandatory cautionary note
        safe_note = "AI generated summary only, verify clinically."
        if safe_note not in result.cautionary_notes:
            result.cautionary_notes.append(safe_note)

        return result
