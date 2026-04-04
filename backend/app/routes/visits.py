"""
MedOrbit — Visit Routes

POST /api/visits       — Create visit
GET  /api/visits       — List visits for current user
GET  /api/visits/{id}  — Get visit detail

POST /api/visits/{id}/start    — Transition to ACTIVE
POST /api/visits/{id}/complete — Transition to COMPLETED
POST /api/visits/{id}/cancel   — Transition to CANCELLED
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    require_assigned_doctor,
    require_role,
    require_visit_participant,
)
from app.models.user import User
from app.models.visit import Visit
from app.schemas.visit import VisitCreateRequest, VisitResponse, VisitStatus
from app.services.visit_service import (
    VisitServiceError,
    cancel_visit,
    complete_visit,
    create_visit,
    get_visits_for_user,
    start_visit,
)

router = APIRouter(prefix="/visits", tags=["Visits"])


# ── Collection Routes ────────────────────────────────────────

@router.post(
    "",
    response_model=VisitResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a visit",
)
def create_new_visit(
    body: VisitCreateRequest,
    current_user: User = Depends(require_role("doctor")),
    db: Session = Depends(get_db),
):
    """
    Create a new scheduled visit.
    Only doctors can create visits for patients.
    """
    try:
        return create_visit(
            db=db,
            doctor_id=current_user.id,
            patient_id=body.patient_id,
            type=body.type,
            title=body.title,
        )
    except VisitServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get(
    "",
    response_model=List[VisitResponse],
    summary="List visits",
)
def list_visits(
    status: VisitStatus | None = Query(None, description="Filter by status"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    List visits securely scoped to the current user.
    - Doctors see their assigned patients' visits.
    - Patients see their own visits.
    """
    return get_visits_for_user(db=db, user=current_user, status=status)


# ── Detail Routes ────────────────────────────────────────────

@router.get(
    "/{visit_id}",
    response_model=VisitResponse,
    summary="Get visit details",
)
def get_visit(
    visit: Visit = Depends(require_visit_participant),
):
    """
    Retrieve visit details.
    Restricted to the exact doctor or patient assigned to the visit.
    """
    return visit


# ── Lifecycle Action Routes ──────────────────────────────────

@router.post(
    "/{visit_id}/start",
    response_model=VisitResponse,
    summary="Start a visit",
)
def start_visit_handler(
    db: Session = Depends(get_db),
    visit: Visit = Depends(require_assigned_doctor),
):
    """
    Transition a visit from 'scheduled' to 'active'.
    Only the assigned doctor can do this.
    """
    try:
        return start_visit(db=db, visit=visit)
    except VisitServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post(
    "/{visit_id}/complete",
    response_model=VisitResponse,
    summary="Complete a visit",
)
def complete_visit_handler(
    db: Session = Depends(get_db),
    visit: Visit = Depends(require_assigned_doctor),
):
    """
    Transition a visit from 'active' to 'completed'.
    Only the assigned doctor can do this.
    (This will later trigger the AI agent orchestration.)
    """
    try:
        return complete_visit(db=db, visit=visit)
    except VisitServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post(
    "/{visit_id}/cancel",
    response_model=VisitResponse,
    summary="Cancel a visit",
)
def cancel_visit_handler(
    db: Session = Depends(get_db),
    visit: Visit = Depends(require_assigned_doctor),
):
    """
    Transition a visit from 'scheduled' to 'cancelled'.
    Only the assigned doctor can do this.
    """
    try:
        return cancel_visit(db=db, visit=visit)
    except VisitServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
