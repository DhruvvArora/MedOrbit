"""
MedOrbit — Shared Transcript Types for AI Agents

This module defines the expected shape of transcript data
that AI agents will consume. It decouples agent logic from
FastAPI/SQLAlchemy internals.

Usage in agent scripts:
    from agents.shared.transcript_types import TranscriptInput, Utterance
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Utterance:
    """A single utterance from a transcript."""
    sequence: int
    speaker_role: str       # "doctor", "patient", "system"
    speaker_label: str      # "Dr. Chen", "Alex Johnson"
    text: str


@dataclass
class TranscriptInput:
    """
    The complete transcript for a visit, ready for agent consumption.

    Agents receive this structured object to avoid coupling
    to database models or HTTP schemas.
    """
    visit_id: str
    utterances: List[Utterance] = field(default_factory=list)

    @property
    def plaintext(self) -> str:
        """Format the transcript as a single readable string."""
        lines = []
        for u in self.utterances:
            label = u.speaker_label or u.speaker_role.capitalize()
            lines.append(f"[{label}]: {u.text}")
        return "\n".join(lines)

    @property
    def chunk_count(self) -> int:
        return len(self.utterances)
