from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_assigned_doctor, require_role
from app.models.visit import Visit
from app.models.report import VisitReport
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderResponse, ReminderStatusUpdate
from app.services.notifier_service import AbstractNotifierService

router = APIRouter(
    prefix="/visits/{visit_id}/reminders",
    tags=["Reminder Generation (Doctor Side)"]
)

@router.post("/generate", response_model=List[ReminderResponse])
def generate_reminders_from_report(
    visit: Visit = Depends(require_assigned_doctor),
    db: Session = Depends(get_db)
):
    """
    Doctor-invoked trigger that converts immutable report strings into actionable tracking rows.
    Idempotent layout wipes uncompleted tasks before regenerating.
    """
    report = db.query(VisitReport).filter(VisitReport.visit_id == visit.id).first()
    
    if not report or report.status != "APPROVED":
        raise HTTPException(
            status_code=403, 
            detail="Cannot generate reminders. The VisitReport must be APPROVED first."
        )

    # Idempotent wipe - destroy any pending reminders for this exact visit before regenerating
    db.query(Reminder).filter(Reminder.visit_id == visit.id, Reminder.status == "PENDING").delete()
    db.commit()

    created_reminders = []
    candidates = report.reminder_candidates or []
    
    for task_string in candidates:
        r = Reminder(
            visit_id=visit.id,
            patient_id=visit.patient_id,
            source_report_id=report.id,
            title=str(task_string),
            status="PENDING",
            due_at=datetime.utcnow() + timedelta(days=1)
        )
        db.add(r)
        created_reminders.append(r)
        
    db.commit()
    for rem in created_reminders:
        db.refresh(rem)

    if created_reminders:
        AbstractNotifierService.notify_patient_reminder_generated(visit.patient_id, len(created_reminders))

    return created_reminders


# ----- Patient Endpoints for Reminders mapped in /patient.py safely -----
