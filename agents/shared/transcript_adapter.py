"""
MedOrbit — Transcript Adapter for AI Agents

Converts database transcript data into the shared TranscriptInput contract.

This is the BRIDGE between the backend service layer and the agent layer.
Agents should call functions here instead of importing backend services directly.

Usage:
    from agents.shared.transcript_adapter import load_transcript_for_visit

    transcript = load_transcript_for_visit("visit-uuid-here")
    print(transcript.plaintext)
    print(transcript.chunk_count)
"""

import sys
import os
from typing import Optional

# Ensure backend is importable
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_backend_root = os.path.join(_project_root, "backend")
if _backend_root not in sys.path:
    sys.path.insert(0, _backend_root)

from agents.shared.transcript_types import TranscriptInput


def load_transcript_for_visit(visit_id: str) -> TranscriptInput:
    """
    Load a full transcript for a given visit_id from the database.

    This function handles its own database session management,
    so agents don't need to know about SQLAlchemy.

    Args:
        visit_id: UUID of the visit to load transcript for.

    Returns:
        TranscriptInput with ordered utterances, ready for agent processing.

    Raises:
        RuntimeError: If the database session cannot be created.
    """
    # Late import to avoid circular dependencies at module load time
    from app.core.database import SessionLocal
    from app.services.transcript_service import get_transcript_for_agent

    db = SessionLocal()
    try:
        return get_transcript_for_agent(db=db, visit_id=visit_id)
    finally:
        db.close()


def load_transcript_plaintext(visit_id: str) -> Optional[str]:
    """
    Convenience function: load transcript and return just the formatted text.

    Returns None if the visit has no transcript chunks.
    """
    transcript = load_transcript_for_visit(visit_id)
    if transcript.chunk_count == 0:
        return None
    return transcript.plaintext
