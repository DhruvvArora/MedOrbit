from app.models.visit import Visit
from agents.behavioral.agent import BehavioralInsightAgent
from agents.shared.transcript_adapter import load_transcript_plaintext


def run_behavioral_agent_for_visit(visit: Visit) -> dict:
    """
    Runs the Behavioral Insight Agent on the given visit's transcript.

    Args:
        visit: The active or completed visit to analyze.

    Returns:
        A dict representation of BehavioralInsightOutput.
    """
    transcript_text = load_transcript_plaintext(visit.id)

    # Note: `load_transcript_plaintext` returns None if 0 chunks exist,
    # but our agent handles empty strings gracefully. We normalize it to empty.
    safe_text = transcript_text or ""

    agent = BehavioralInsightAgent()
    output = agent.analyze(safe_text)

    # Return as dict so outer FastApi route can return as JSON natively
    return output.model_dump()
