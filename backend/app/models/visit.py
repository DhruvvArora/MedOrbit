"""
MedOrbit — Visit Model

Represents a consultation session between a Doctor and a Patient.
Anchors all transcripts, agent outputs, and final reports.
"""

import uuid
from datetime import datetime, timezone
from typing import List

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Visit(Base):
    """
    Core consultation record.
    Strictly ties one doctor to one patient for a given encounter.
    """

    __tablename__ = "visits"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    doctor_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False, index=True
    )
    patient_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False, index=True
    )

    type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # 'virtual' or 'in_person'
    status: Mapped[str] = mapped_column(
        String(20), default="scheduled", nullable=False
    )  # 'scheduled', 'active', 'completed', 'cancelled'

    title: Mapped[str | None] = mapped_column(String(255), nullable=True)

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )

    # ── Relationships ─────────────────────────────────────────
    # Uses string reference to avoid circular import.
    # back_populates links to TranscriptChunk.visit (set on that side).
    transcript_chunks: Mapped[List["TranscriptChunk"]] = relationship(
        "TranscriptChunk",
        back_populates="visit",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property
    def transcript_chunk_count(self) -> int:
        """Number of transcript chunks attached to this visit."""
        if self.transcript_chunks is None:
            return 0
        return len(self.transcript_chunks)

    def __repr__(self) -> str:
        return f"<Visit {self.id} status={self.status} type={self.type}>"

