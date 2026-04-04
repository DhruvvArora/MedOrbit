import os
from typing import Optional

from agents.shared.llm import execute_structured_prompt
from agents.behavioral.schemas import BehavioralInsightOutput, InsightEvidence
from agents.behavioral.prompts import (
    BEHAVIORAL_AGENT_SYSTEM_PROMPT,
    build_behavioral_user_prompt
)
from agents.psychologist_knowledge.query_index import get_relevant_chunks

class BehavioralInsightAgent:
    """
    Analyzes a consultation transcript to generate behavioral and psychosocial insights.
    """

    def _get_mock_output(self) -> BehavioralInsightOutput:
        """Returns a safe mock payload when no API key is present."""
        return BehavioralInsightOutput(
            summary="Patient expresses moderate distress related to work-life balance and sleep deprivation.",
            emotional_signals=[
                InsightEvidence(
                    observation="High stress and overwhelm.",
                    evidence_snippet="Work is very stressful... I usually get to bed around midnight and wake at 5.",
                    confidence="high"
                )
            ],
            adherence_risk=[
                InsightEvidence(
                    observation="Did not start exercise plan due to pain.",
                    evidence_snippet="I was trying to start jogging but my knee started hurting.",
                    confidence="medium"
                )
            ],
            psychosocial_factors=["Work stress", "Chronic sleep deprivation (5 hours/night)", "Poor diet layout"],
            communication_flags=["Anxious tone", "Overwhelmed"],
            suggested_follow_up_questions=[
                "How are you managing the stress at work?",
                "Are there any specific barriers to getting more sleep?",
                "Would you be open to speaking with a counselor about the anxiety?"
            ],
            cautionary_notes=["AI inference only, verify clinically", "[MOCK MODE ENGAGED]"]
        )

    def analyze(self, transcript_text: str) -> BehavioralInsightOutput:
        """
        Executes the behavioral agent.
        
        Args:
            transcript_text: The formatted plaintext of the transcript.
            
        Returns:
            BehavioralInsightOutput: The structured JSON response.
        """
        if not transcript_text or len(transcript_text.split()) < 20:
            return BehavioralInsightOutput(
                summary="Insufficient data for behavioral analysis.",
                emotional_signals=[],
                adherence_risk=[],
                psychosocial_factors=[],
                communication_flags=[],
                suggested_follow_up_questions=[],
                cautionary_notes=["Transcript too short or empty."]
            )

        # Handle Mock Mode
        if not os.environ.get("OPENAI_API_KEY"):
            return self._get_mock_output()

        # [RAG KNOWLEDGE INJECTION]
        # Dynamically pulls FAISS CPU context.
        relevant_docs = get_relevant_chunks(query=transcript_text, top_k=2)
        
        knowledge_base_str = ""
        if relevant_docs:
            knowledge_base_str = "\n[AUTOMATED CLINICAL KNOWLEDGE BASE RETRIEVAL]:\n"
            for doc in relevant_docs:
                knowledge_base_str += f"- From {doc['source']}: {doc['text']}\n"

        user_prompt = build_behavioral_user_prompt(transcript_text)
        
        injected_system_prompt = BEHAVIORAL_AGENT_SYSTEM_PROMPT + knowledge_base_str

        result = execute_structured_prompt(
            system_prompt=injected_system_prompt,
            user_prompt=user_prompt,
            response_model=BehavioralInsightOutput,
            temperature=0.1
        )
        
        # Ensure mandatory cautionary note
        safe_note = "AI inference only, verify clinically."
        if safe_note not in result.cautionary_notes:
            result.cautionary_notes.append(safe_note)

        return result
