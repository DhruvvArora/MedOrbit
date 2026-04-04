"""
MedOrbit — Transcript Service

Business logic for transcript chunk ingestion, retrieval, formatting,
and agent-ready transcript export.

This is the SINGLE source of truth for transcript operations.
Routes and agents should call these functions; never query the model directly.
"""

import sys
import os
from collections import Counter
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.transcript import TranscriptChunk
from app.models.visit import Visit

# ── Import shared agent types (safe cross-module import) ─────
# Add the project root so we can import from agents/shared
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from agents.shared.transcript_types import TranscriptInput, Utterance


# ── Error Hierarchy ──────────────────────────────────────────

class TranscriptServiceError(Exception):
    """Base exception for all transcript service errors."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class VisitNotActiveError(TranscriptServiceError):
    """Raised when attempting to write transcript to a non-active visit."""
    def __init__(self):
        super().__init__(
            "Transcripts can only be added to active visits.", status_code=400
        )


class DuplicateSequenceError(TranscriptServiceError):
    """Raised when a sequence_number collision is detected."""
    def __init__(self, seq: int):
        super().__init__(
            f"Sequence number {seq} already exists for this visit.",
            status_code=409,
        )


class EmptyTranscriptError(TranscriptServiceError):
    """Raised when transcript text is empty after normalization."""
    def __init__(self):
        super().__init__(
            "Transcript text cannot be empty.", status_code=422
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


def _normalize_text(text: str) -> str:
    """Strip whitespace and validate non-empty text."""
    normalized = text.strip()
    if not normalized:
        raise EmptyTranscriptError()
    return normalized


def _check_sequence_collision(db: Session, visit_id: str, seq: int) -> None:
    """Raise if sequence_number already exists for this visit."""
    existing = (
        db.query(TranscriptChunk.id)
        .filter(
            TranscriptChunk.visit_id == visit_id,
            TranscriptChunk.sequence_number == seq,
        )
        .first()
    )
    if existing:
        raise DuplicateSequenceError(seq)


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

    Raises:
        VisitNotActiveError: if visit status is not 'active'.
        DuplicateSequenceError: if the provided sequence_number collides.
        EmptyTranscriptError: if text is empty after stripping.
    """
    _assert_visit_active(visit)
    normalized_text = _normalize_text(text)

    if sequence_number is None:
        sequence_number = _next_sequence_number(db, visit.id)
    else:
        _check_sequence_collision(db, visit.id, sequence_number)

    chunk = TranscriptChunk(
        visit_id=visit.id,
        sequence_number=sequence_number,
        speaker_role=speaker_role,
        speaker_label=speaker_label,
        text=normalized_text,
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

    Auto-assigns sequence numbers where missing. Validates all chunks
    before inserting any (all-or-nothing).

    Raises:
        VisitNotActiveError: if visit status is not 'active'.
        DuplicateSequenceError: if any sequence_number collides.
        EmptyTranscriptError: if any text is empty after stripping.
    """
    _assert_visit_active(visit)

    next_seq = _next_sequence_number(db, visit.id)

    # Pre-collect existing sequence numbers for collision detection
    existing_seqs = set(
        row[0]
        for row in db.query(TranscriptChunk.sequence_number)
        .filter(TranscriptChunk.visit_id == visit.id)
        .all()
    )

    # Pre-validate all chunks and assign sequence numbers
    prepared: list[dict] = []
    assigned_seqs: set[int] = set()

    for chunk_data in chunks_data:
        normalized_text = _normalize_text(chunk_data["text"])

        seq = chunk_data.get("sequence_number")
        if seq is None:
            # Find next available seq that doesn't collide
            while next_seq in existing_seqs or next_seq in assigned_seqs:
                next_seq += 1
            seq = next_seq
            next_seq += 1
        else:
            if seq in existing_seqs or seq in assigned_seqs:
                raise DuplicateSequenceError(seq)

        assigned_seqs.add(seq)
        prepared.append({
            "visit_id": visit.id,
            "sequence_number": seq,
            "speaker_role": chunk_data["speaker_role"],
            "speaker_label": chunk_data.get("speaker_label"),
            "text": normalized_text,
            "source_type": chunk_data.get("source_type", "manual"),
        })

    # Insert all chunks in a single transaction
    created_chunks = []
    for data in prepared:
        chunk = TranscriptChunk(**data)
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
        [Dr. Chen]: How are you feeling?
        [Alex Johnson]: I've been having some knee pain.
    """
    chunks = get_chunks(db, visit_id)

    if not chunks:
        return "", 0

    lines = []
    for chunk in chunks:
        label = chunk.speaker_label or chunk.speaker_role.capitalize()
        lines.append(f"[{label}]: {chunk.text}")

    return "\n".join(lines), len(chunks)


def get_stats(db: Session, visit_id: str) -> dict:
    """
    Return transcript statistics for a visit.

    Returns a dict with:
        total_chunks, speaker_breakdown, source_breakdown,
        first_chunk_at, last_chunk_at, total_characters
    """
    chunks = get_chunks(db, visit_id)

    if not chunks:
        return {
            "visit_id": visit_id,
            "total_chunks": 0,
            "speaker_breakdown": {},
            "source_breakdown": {},
            "first_chunk_at": None,
            "last_chunk_at": None,
            "total_characters": 0,
        }

    speaker_counts = Counter(c.speaker_role for c in chunks)
    source_counts = Counter(c.source_type for c in chunks)
    total_chars = sum(len(c.text) for c in chunks)

    return {
        "visit_id": visit_id,
        "total_chunks": len(chunks),
        "speaker_breakdown": dict(speaker_counts),
        "source_breakdown": dict(source_counts),
        "first_chunk_at": chunks[0].created_at.isoformat() if chunks[0].created_at else None,
        "last_chunk_at": chunks[-1].created_at.isoformat() if chunks[-1].created_at else None,
        "total_characters": total_chars,
    }


# ── Agent Integration ────────────────────────────────────────

def get_transcript_for_agent(db: Session, visit_id: str) -> TranscriptInput:
    """
    Build a TranscriptInput dataclass for agent consumption.

    This is the canonical way for AI agents to access transcript data.
    Agents should never query the database directly — they call this function.

    Returns:
        TranscriptInput with ordered Utterance objects.
    """
    chunks = get_chunks(db, visit_id)

    utterances = [
        Utterance(
            sequence=chunk.sequence_number,
            speaker_role=chunk.speaker_role,
            speaker_label=chunk.speaker_label or chunk.speaker_role.capitalize(),
            text=chunk.text,
        )
        for chunk in chunks
    ]

    return TranscriptInput(visit_id=visit_id, utterances=utterances)
