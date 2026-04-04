"""
MedOrbit — TranscriptChunk Model

Represents a single utterance in a consultation transcript.
Ordered by sequence_number within a visit.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class TranscriptChunk(Base):
    """
    One utterance from a doctor–patient conversation.

    Chunks are ordered by sequence_number within a visit.
    The full transcript is reconstructed by querying all chunks
    for a visit_id, sorted by sequence_number ASC.
    """

    __tablename__ = "transcript_chunks"
    __table_args__ = (
        UniqueConstraint("visit_id", "sequence_number", name="uq_visit_sequence"),
        CheckConstraint(
            "source_type IN ('manual', 'transcribed', 'simulated')",
            name="ck_source_type",
        ),
        CheckConstraint(
            "speaker_role IN ('doctor', 'patient', 'system')",
            name="ck_speaker_role",
        ),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    visit_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("visits.id"), nullable=False, index=True
    )
    sequence_number: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    speaker_role: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # "doctor", "patient", "system"
    speaker_label: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )  # e.g. "Dr. Chen", "Alex Johnson"
    text: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    source_type: Mapped[str] = mapped_column(
        String(20), default="manual", nullable=False
    )  # "manual", "transcribed", "simulated"
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )

    # ── Relationships ─────────────────────────────────────────
    visit = relationship("Visit", back_populates="transcript_chunks")

    def __repr__(self) -> str:
        return f"<TranscriptChunk visit={self.visit_id} seq={self.sequence_number} speaker={self.speaker_role}>"
