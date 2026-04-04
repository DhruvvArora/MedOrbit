"""
MedOrbit — Transcript Service

Business logic for transcript chunk ingestion, retrieval, and formatting.
"""

from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.transcript import TranscriptChunk
from app.models.visit import Visit


class TranscriptServiceError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class VisitNotActiveError(TranscriptServiceError):
    def __init__(self):
        super().__init__(
            "Transcripts can only be added to active visits.", status_code=400
        )


# ── Helpers ──────────────────────────────────────────────────

def _next_sequence_number(db: Session, visit_id: str) -> int:
    """Return the next available sequence number for a visit."""
    max_seq = (
        db.query(func.max(TranscriptChunk.sequence_number))
        .filter(TranscriptChunk.visit_id == visit_id)
        .scalar()
    )
    return (max_seq or 0) + 1


def _assert_visit_active(visit: Visit) -> None:
    """Raise if the visit is not in 'active' status."""
    if visit.status != "active":
        raise VisitNotActiveError()


# ── Service Functions ────────────────────────────────────────

def add_chunk(
    db: Session,
    visit: Visit,
    speaker_role: str,
    text: str,
    speaker_label: str | None = None,
    sequence_number: int | None = None,
    source_type: str = "manual",
) -> TranscriptChunk:
    """
    Add a single transcript chunk to a visit.

    Raises VisitNotActiveError if the visit is not active.
    Auto-assigns sequence_number if not provided.
    """
    _assert_visit_active(visit)

    if sequence_number is None:
        sequence_number = _next_sequence_number(db, visit.id)

    chunk = TranscriptChunk(
        visit_id=visit.id,
        sequence_number=sequence_number,
        speaker_role=speaker_role,
        speaker_label=speaker_label,
        text=text.strip(),
        source_type=source_type,
    )
    db.add(chunk)
    db.commit()
    db.refresh(chunk)
    return chunk


def add_chunks_bulk(
    db: Session,
    visit: Visit,
    chunks_data: list[dict],
) -> List[TranscriptChunk]:
    """
    Add multiple transcript chunks to a visit in a single transaction.

    Each dict in chunks_data should have:
        speaker_role, text, speaker_label (optional),
        sequence_number (optional), source_type (optional).

    Raises VisitNotActiveError if the visit is not active.
    Auto-assigns sequence numbers where missing.
    """
    _assert_visit_active(visit)

    next_seq = _next_sequence_number(db, visit.id)
    created_chunks = []

    for chunk_data in chunks_data:
        seq = chunk_data.get("sequence_number")
        if seq is None:
            seq = next_seq
            next_seq += 1

        chunk = TranscriptChunk(
            visit_id=visit.id,
            sequence_number=seq,
            speaker_role=chunk_data["speaker_role"],
            speaker_label=chunk_data.get("speaker_label"),
            text=chunk_data["text"].strip(),
            source_type=chunk_data.get("source_type", "manual"),
        )
        db.add(chunk)
        created_chunks.append(chunk)

    db.commit()
    for chunk in created_chunks:
        db.refresh(chunk)

    return created_chunks


def get_chunks(db: Session, visit_id: str) -> List[TranscriptChunk]:
    """
    Retrieve all transcript chunks for a visit, ordered by sequence_number.
    """
    return (
        db.query(TranscriptChunk)
        .filter(TranscriptChunk.visit_id == visit_id)
        .order_by(TranscriptChunk.sequence_number.asc())
        .all()
    )


def get_plaintext(db: Session, visit_id: str) -> tuple[str, int]:
    """
    Retrieve the full transcript as formatted plaintext.

    Returns:
        (formatted_text, chunk_count)

    Format:
        [Doctor]: How are you feeling?
        [Patient]: I've been having some knee pain.
    """
    chunks = get_chunks(db, visit_id)

    if not chunks:
        return "", 0

    lines = []
    for chunk in chunks:
        label = chunk.speaker_label or chunk.speaker_role.capitalize()
        lines.append(f"[{label}]: {chunk.text}")

    return "\n".join(lines), len(chunks)
