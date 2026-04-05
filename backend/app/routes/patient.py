from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role, get_visit_or_404
from app.models.user import User
from app.models.visit import Visit
from app.models.report import VisitReport
from app.models.reminder import Reminder
from app.schemas.patient import PatientVisitDetailResponse, PatientDashboardSummary
from app.schemas.reminder import ReminderResponse, ReminderStatusUpdate


router = APIRouter(
    prefix="/patient",
    tags=["Patient Flow"],
    dependencies=[Depends(require_role("patient"))]
)


# ── Helper ───────────────────────────────────────────────────

def _build_visit_response(visit: Visit, db: Session) -> PatientVisitDetailResponse:
    """Shared builder used by list, detail, and dashboard endpoints."""
    report = db.query(VisitReport).filter(VisitReport.visit_id == visit.id).first()
    is_approved = report is not None and report.status == "APPROVED"

    return PatientVisitDetailResponse(
        visit_id=visit.id,
        title=visit.title or "Visit",
        status=visit.status,
        started_at=visit.started_at,
        has_approved_report=is_approved,
        simplified_explanation=report.simplified_explanation if is_approved else None,
        patient_discharge_draft=report.patient_discharge_draft if is_approved else None,
    )


# ── Dashboard Summary ────────────────────────────────────────

@router.get("/dashboard-summary", response_model=PatientDashboardSummary)
def get_patient_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Aggregated view-model for the patient dashboard.
    Returns visits, reminder overview, and summary counts in a single call.
    """
    visits = (
        db.query(Visit)
        .filter(Visit.patient_id == current_user.id)
        .order_by(Visit.started_at.desc())
        .all()
    )
    visit_responses = [_build_visit_response(v, db) for v in visits]

    reminders = (
        db.query(Reminder)
        .filter(Reminder.patient_id == current_user.id)
        .order_by(Reminder.due_at.asc())
        .all()
    )

    pending_report_count = sum(1 for v in visit_responses if not v.has_approved_report)
    pending_reminder_count = sum(1 for r in reminders if r.status == "PENDING")

    return PatientDashboardSummary(
        patient_id=current_user.id,
        patient_name=current_user.full_name,
        visit_count=len(visit_responses),
        pending_report_count=pending_report_count,
        pending_reminder_count=pending_reminder_count,
        visits=visit_responses,
        recent_reminders=reminders,
    )


# ── Visit List & Detail ─────────────────────────────────────

@router.get("/visits", response_model=List[PatientVisitDetailResponse])
def list_patient_visits(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lists all visits for the authenticated patient.
    Safely calculates `has_approved_report` dynamically without returning unauthorized draft strings.
    """
    visits = db.query(Visit).filter(Visit.patient_id == current_user.id).order_by(Visit.started_at.desc()).all()
    return [_build_visit_response(v, db) for v in visits]


@router.get("/visits/{visit_id}", response_model=PatientVisitDetailResponse)
def get_patient_visit_detail(
    visit: Visit = Depends(get_visit_or_404),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Gets the specific visit detail.
    Strictly enforces authorization boundaries so patient 1 cannot read patient 2's visit.
    """
    if visit.patient_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to view this visit.")

    return _build_visit_response(visit, db)


# ── Reminders ────────────────────────────────────────────────

@router.get("/reminders", response_model=List[ReminderResponse])
def list_patient_reminders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Fetches real Reminder Database models tracking state safely.
    """
    reminders = db.query(Reminder).filter(Reminder.patient_id == current_user.id).order_by(Reminder.due_at.asc()).all()
    return reminders

@router.patch("/reminders/{reminder_id}/status", response_model=ReminderResponse)
def update_reminder_status(
    reminder_id: int,
    status_update: ReminderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Patient hook to safely check off completed tasks.
    """
    rem = db.query(Reminder).filter(Reminder.id == reminder_id, Reminder.patient_id == current_user.id).first()
    if not rem:
         raise HTTPException(status_code=404, detail="Reminder not found.")

    rem.status = status_update.status
    if rem.status == "COMPLETED":
        rem.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(rem)
    return rem

