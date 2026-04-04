import os
from typing import Optional

from agents.shared.llm import execute_structured_prompt
from agents.super_agent.schemas import SuperAgentDraftOutput
from agents.super_agent.prompts import (
    SUPER_AGENT_SYSTEM_PROMPT,
    build_super_user_prompt
)

class SuperInsightAgent:
    """
    Orchestrates transcript, behavioral outputs, and triage outputs into final drafted forms.
    """
    
    def _get_mock_output(self, visit_id: str) -> SuperAgentDraftOutput:
        """Returns complex mock payload for orchestration when no API key is present."""
        return SuperAgentDraftOutput(
            visit_id=visit_id,
            doctor_summary="Patient presented for routine intake complaining of intermittent chest tightness associated with stress and tension headaches. Evaluation reveals stage 1 hypertension (145/95). Patient reports chronic sleep deprivation (5 hours/night) and significant work stress. Plan includes lifestyle modifications (sodium under 2300mg, moderate exercise) and 2-week follow up. Differential includes stress-induced tension vs primary hypertension.",
            patient_discharge_draft="Thank you for coming in today. We discussed the tension headaches and chest tightness you've been experiencing. Because your blood pressure was mildly elevated today, I want to start by trying some lifestyle changes. Please try to reduce your sodium intake to under 2300 mg per day, start incorporating 30 minutes of moderate exercise, and focus on getting more sleep. We will re-evaluate in 2 weeks to see if symptoms improve.",
            simplified_explanation="Today you visited the doctor because of headaches, chest tightness, and stress from work. The doctor noticed your blood pressure was a little high. Instead of starting medicine right away, the doctor wants you to eat less salt, exercise a bit, and sleep more to see if it brings your blood pressure down naturally. You'll check back in two weeks.",
            clinical_review_flags=[
                "Patient described chest tightness; though likely tension/anxiety related, verify cardiac risk.",
                "High emotional payload (work stress, sleep deprivation) may hinder adherence to lifestyle plan."
            ],
            reminder_candidates=[
                "Log daily blood pressure readings for next 14 days",
                "Keep daily sodium intake below 2300 mg",
                "Exercise 30 minutes daily",
                "Attend 2-week follow-up appointment"
            ],
            cautionary_notes=["DRAFT ONLY - Requires physician approval.", "[MOCK MODE ENGAGED]"]
        )

    def analyze(self, visit_id: str, transcript_text: str, behavioral_data: dict, triage_data: dict) -> SuperAgentDraftOutput:
        """
        Executes the Super Agent orchestrator.

        Args:
            visit_id: The visit identifier mapping back to the encounter.
            transcript_text: The formatted plaintext of the transcript.
            behavioral_data: The JSON dictionary produced by BehavioralInsightAgent.
            triage_data: The JSON dictionary produced by TriageInsightAgent.
            
        Returns:
            SuperAgentDraftOutput: The completed structured drafting response.
        """
        # Handle Mock Mode
        if not os.environ.get("OPENAI_API_KEY"):
            return self._get_mock_output(visit_id)

        # Execute live mapping
        user_prompt = build_super_user_prompt(visit_id, transcript_text, behavioral_data, triage_data)

        result = execute_structured_prompt(
            system_prompt=SUPER_AGENT_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=SuperAgentDraftOutput,
            temperature=0.0  # Extreme lowest temperature for orchestration deterministic safety
        )
        
        # Ensure mandatory cautionary note
        safe_note = "DRAFT ONLY - Requires physician approval."
        if safe_note not in result.cautionary_notes:
            result.cautionary_notes.append(safe_note)

        return result
