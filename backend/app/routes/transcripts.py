"""
MedOrbit — Transcript Routes

POST /api/visits/{visit_id}/transcripts/chunks     — Add single chunk
POST /api/visits/{visit_id}/transcripts/bulk        — Add multiple chunks
GET  /api/visits/{visit_id}/transcripts/chunks      — Get ordered chunks
GET  /api/visits/{visit_id}/transcripts/plaintext   — Get plaintext for AI
GET  /api/visits/{visit_id}/transcripts/stats        — Get transcript statistics
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_assigned_doctor, require_visit_participant
from app.models.visit import Visit
from app.schemas.transcript import (
    BulkChunkCreateRequest,
    BulkCreateResponse,
    ChunkCreateRequest,
    ChunkResponse,
    TranscriptPlaintextResponse,
    TranscriptStatsResponse,
)
from app.services.transcript_service import (
    TranscriptServiceError,
    add_chunk,
    add_chunks_bulk,
    get_chunks,
    get_plaintext,
    get_stats,
)

router = APIRouter(
    prefix="/visits/{visit_id}/transcripts",
    tags=["Transcripts"],
)


# ── Write Endpoints (Doctor only, active visit) ─────────────


@router.post(
    "/chunks",
    response_model=ChunkResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a single transcript chunk",
    responses={
        400: {"description": "Visit is not active"},
        403: {"description": "Not the assigned doctor"},
        409: {"description": "Sequence number collision"},
        422: {"description": "Empty transcript text"},
    },
)
def add_single_chunk(
    body: ChunkCreateRequest,
    visit: Visit = Depends(require_assigned_doctor),
    db: Session = Depends(get_db),
):
    """
    Append a single utterance to the visit transcript.

    - Only the assigned doctor can write.
    - Visit must be in 'active' status.
    - sequence_number is auto-assigned if omitted.
    - Text is whitespace-normalized before storage.
    """
    try:
        return add_chunk(
            db=db,
            visit=visit,
            speaker_role=body.speaker_role.value,
            text=body.text,
            speaker_label=body.speaker_label,
            sequence_number=body.sequence_number,
            source_type=body.source_type.value,
        )
    except TranscriptServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post(
    "/bulk",
    response_model=BulkCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add multiple transcript chunks at once",
    responses={
        400: {"description": "Visit is not active"},
        403: {"description": "Not the assigned doctor"},
        409: {"description": "Sequence number collision in batch"},
        422: {"description": "Empty transcript text in batch"},
    },
)
def add_bulk_chunks(
    body: BulkChunkCreateRequest,
    visit: Visit = Depends(require_assigned_doctor),
    db: Session = Depends(get_db),
):
    """
    Bulk-ingest transcript chunks for a visit.
    Ideal for hackathon demo simulation or post-call transcript upload.

    - Only the assigned doctor can write.
    - Visit must be in 'active' status.
    - sequence_numbers are auto-assigned for chunks that don't include them.
    - All-or-nothing: if any chunk fails validation, none are saved.
    """
    try:
        chunks_data = [
            {
                "speaker_role": c.speaker_role.value,
                "text": c.text,
                "speaker_label": c.speaker_label,
                "sequence_number": c.sequence_number,
                "source_type": c.source_type.value,
            }
            for c in body.chunks
        ]
        created = add_chunks_bulk(db=db, visit=visit, chunks_data=chunks_data)
        return BulkCreateResponse(
            visit_id=visit.id,
            chunks_created=len(created),
            chunks=[ChunkResponse.model_validate(c) for c in created],
        )
    except TranscriptServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


# ── Read Endpoints (Visit participants) ──────────────────────


@router.get(
    "/chunks",
    response_model=List[ChunkResponse],
    summary="Get transcript chunks",
)
def get_transcript_chunks(
    visit: Visit = Depends(require_visit_participant),
    db: Session = Depends(get_db),
):
    """
    Retrieve all transcript chunks for a visit, ordered by sequence_number.

    - Both the assigned doctor and patient can read.
    """
    return get_chunks(db=db, visit_id=visit.id)


@router.get(
    "/plaintext",
    response_model=TranscriptPlaintextResponse,
    summary="Get transcript as plaintext",
)
def get_transcript_plaintext(
    visit: Visit = Depends(require_visit_participant),
    db: Session = Depends(get_db),
):
    """
    Retrieve the full transcript as a single formatted plaintext string.

    Format:
        [Doctor]: How are you feeling?
        [Patient]: I've been having some knee pain.

    Used by AI agents for context consumption.
    """
    text, count = get_plaintext(db=db, visit_id=visit.id)
    return TranscriptPlaintextResponse(
        visit_id=visit.id,
        text=text,
        chunk_count=count,
    )


@router.get(
    "/stats",
    response_model=TranscriptStatsResponse,
    summary="Get transcript statistics",
)
def get_transcript_stats(
    visit: Visit = Depends(require_visit_participant),
    db: Session = Depends(get_db),
):
    """
    Retrieve transcript metadata and statistics.

    Returns:
    - total chunk count
    - speaker role breakdown (how many chunks per role)
    - source type breakdown
    - timestamp range
    - total character count

    Useful for UI badges and agent pre-processing checks.
    """
    return get_stats(db=db, visit_id=visit.id)
