"""
MedOrbit — Shared Transcript Types for AI Agents

This module defines the expected shape of transcript data
that AI agents will consume. It decouples agent logic from
FastAPI/SQLAlchemy internals.

Usage in agent scripts:
    from agents.shared.transcript_types import TranscriptInput, Utterance

Design principles:
    - Pure Python dataclasses (no FastAPI, no SQLAlchemy, no Pydantic)
    - Immutable-friendly data shapes
    - Agents never import from backend/; they import from here
    - This contract is the "handoff" between the backend pipeline
      and the AI reasoning layers
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Utterance:
    """
    A single utterance from a transcript.

    Attributes:
        sequence: Ordering position within the visit transcript.
        speaker_role: 'doctor', 'patient', or 'system'.
        speaker_label: Human-readable name like 'Dr. Chen'.
        text: The actual spoken content.
        source_type: How this chunk was captured ('manual', 'transcribed', 'simulated').
    """
    sequence: int
    speaker_role: str       # "doctor", "patient", "system"
    speaker_label: str      # "Dr. Chen", "Alex Johnson"
    text: str
    source_type: str = "manual"  # "manual", "transcribed", "simulated"


@dataclass
class TranscriptInput:
    """
    The complete transcript for a visit, ready for agent consumption.

    Agents receive this structured object to avoid coupling
    to database models or HTTP schemas.

    Usage:
        # In an agent module:
        from agents.shared.transcript_types import TranscriptInput

        def analyze(transcript: TranscriptInput):
            for u in transcript.utterances:
                # process each utterance
                ...
            # or use the plaintext property
            full_text = transcript.plaintext
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
        """Total number of utterances."""
        return len(self.utterances)

    @property
    def speaker_roles_present(self) -> set:
        """Set of unique speaker roles in this transcript."""
        return {u.speaker_role for u in self.utterances}

    @property
    def doctor_utterances(self) -> List[Utterance]:
        """Filter to doctor-only utterances."""
        return [u for u in self.utterances if u.speaker_role == "doctor"]

    @property
    def patient_utterances(self) -> List[Utterance]:
        """Filter to patient-only utterances."""
        return [u for u in self.utterances if u.speaker_role == "patient"]

    def to_dict(self) -> Dict:
        """
        Serialize to a plain dict for JSON-based agent APIs.

        Useful for agents that receive input via HTTP or message queues
        rather than direct Python function calls.
        """
        return {
            "visit_id": self.visit_id,
            "chunk_count": self.chunk_count,
            "utterances": [
                {
                    "sequence": u.sequence,
                    "speaker_role": u.speaker_role,
                    "speaker_label": u.speaker_label,
                    "text": u.text,
                    "source_type": u.source_type,
                }
                for u in self.utterances
            ],
            "plaintext": self.plaintext,
        }
