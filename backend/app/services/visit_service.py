"""
MedOrbit — Visit Service

Business logic for the consultation lifecycle.
Handles validation and state transitions.
"""

from datetime import datetime, timezone
from typing import List

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.visit import Visit
from app.schemas.visit import VisitStatus, VisitType


class VisitServiceError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class VisitNotFoundError(VisitServiceError):
    def __init__(self):
        super().__init__("Visit not found", status_code=404)


class StateTransitionError(VisitServiceError):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


def create_visit(
    db: Session,
    doctor_id: str,
    patient_id: str,
    type: VisitType,
    title: str | None = None,
) -> Visit:
    # Ensure patient exists
    patient = db.query(User).filter(User.id == patient_id).first()
    if not patient or patient.role != "patient":
        raise VisitServiceError("Invalid patient ID", status_code=400)

    visit = Visit(
        doctor_id=doctor_id,
        patient_id=patient_id,
        type=type.value,
        title=title,
        status=VisitStatus.SCHEDULED.value,
    )
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit


def get_visits_for_user(
    db: Session, user: User, status: VisitStatus | None = None
) -> List[Visit]:
    query = db.query(Visit)

    if user.role == "doctor":
        query = query.filter(Visit.doctor_id == user.id)
    else:
        query = query.filter(Visit.patient_id == user.id)

    if status:
        query = query.filter(Visit.status == status.value)

    return query.order_by(Visit.created_at.desc()).all()


def start_visit(db: Session, visit: Visit) -> Visit:
    if visit.status != VisitStatus.SCHEDULED.value:
        raise StateTransitionError(f"Cannot start visit in status: {visit.status}")

    visit.status = VisitStatus.ACTIVE.value
    visit.started_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(visit)
    return visit


def complete_visit(db: Session, visit: Visit) -> Visit:
    if visit.status != VisitStatus.ACTIVE.value:
        raise StateTransitionError(f"Cannot complete visit in status: {visit.status}")

    visit.status = VisitStatus.COMPLETED.value
    visit.ended_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(visit)
    return visit


def cancel_visit(db: Session, visit: Visit) -> Visit:
    if visit.status != VisitStatus.SCHEDULED.value:
        raise StateTransitionError(f"Cannot cancel visit in status: {visit.status}")

    visit.status = VisitStatus.CANCELLED.value
    db.commit()
    db.refresh(visit)
    return visit
