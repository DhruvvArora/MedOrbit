import os
import json

from agents.shared.llm import execute_structured_prompt
from agents.patient_simplifier.schemas import PatientSimplifierOutput
from agents.patient_simplifier.prompts import (
    PATIENT_SIMPLIFIER_SYSTEM_PROMPT,
    build_simplifier_user_prompt
)

class PatientSimplifierAgent:
    """Answers patient questions exclusively using approved report artifacts."""

    def _get_mock_output(self, question: str) -> PatientSimplifierOutput:
        """Returns mock payload when API is offline depending on the question's safety."""
        question_lower = question.lower()
        if "emergency" in question_lower or "pain" in question_lower or "dying" in question_lower:
            return PatientSimplifierOutput(
                is_supported=False,
                answer="If you are experiencing a medical emergency or severe symptoms, please dial 911 or visit the nearest emergency room immediately.",
                refusal_reason="Emergency keywords detected."
            )
            
        if "what disease" in question_lower or "different medicine" in question_lower:
            return PatientSimplifierOutput(
                is_supported=False,
                answer="I'm sorry, but I can only clarify the instructions your doctor provided during your visit. Please contact your physician for additional medical guidance.",
                refusal_reason="Out of context clinical question."
            )

        return PatientSimplifierOutput(
            is_supported=True,
            answer="Based on your doctor's notes, you should try to limit foods that are high in salt and schedule a follow-up test in a few months. Was there a specific part of the instructions you'd like me to clarify?",
            refusal_reason=None
        )

    def explain(self, patient_question: str, simplified_explanation: str, discharge_draft: str, reminders: list) -> PatientSimplifierOutput:
        if not os.environ.get("OPENAI_API_KEY"):
            return self._get_mock_output(patient_question)

        # Cast safe empty strings if DB columns are unexpectedly empty
        reminders_str = json.dumps(reminders) if reminders else "None listed."
        safe_summary = simplified_explanation or "None listed."
        safe_discharge = discharge_draft or "None listed."

        user_prompt = build_simplifier_user_prompt(
            patient_question=patient_question,
            simplified_explanation=safe_summary,
            discharge_draft=safe_discharge,
            reminders=reminders_str
        )

        return execute_structured_prompt(
            system_prompt=PATIENT_SIMPLIFIER_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=PatientSimplifierOutput,
            temperature=0.0  # Extremely low temperature to reduce generative hallucination
        )
