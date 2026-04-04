from app.models.visit import Visit
from agents.triage.agent import TriageInsightAgent
from agents.shared.transcript_adapter import load_transcript_plaintext


def run_triage_agent_for_visit(visit: Visit) -> dict:
    """
    Runs the Clinical Triage Agent on the given visit's transcript.

    Args:
        visit: The active or completed visit to analyze.

    Returns:
        A dict representation of TriageInsightOutput.
    """
    transcript_text = load_transcript_plaintext(visit.id)

    safe_text = transcript_text or ""

    agent = TriageInsightAgent()
    output = agent.analyze(safe_text)

    # Return as dict so outer FastApi route can return as JSON natively
    return output.model_dump()
