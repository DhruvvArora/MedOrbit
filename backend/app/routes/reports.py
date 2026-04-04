from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_assigned_doctor, require_visit_participant, get_current_user
from app.models.visit import Visit
from app.models.report import VisitReport
from app.models.user import User
from app.schemas.report import VisitReportResponse, VisitReportUpdate
from app.services.orchestration_service import run_orchestration_for_visit


orchestration_router = APIRouter(
    prefix="/visits/{visit_id}/orchestration",
    tags=["Agent Orchestration"],
)

report_router = APIRouter(
    prefix="/visits/{visit_id}/report",
    tags=["Visit Reports"],
)

# --- Orchestration Routes ---

@orchestration_router.post(
    "/run",
    response_model=VisitReportResponse,
    summary="Trigger the Super Agent Orchestration"
)
def execute_orchestration(
    visit: Visit = Depends(require_assigned_doctor),
    db: Session = Depends(get_db)
):
    """
    Sequentially triggers the Behavioral Agent and Triage Agent, and feeds them into the Super Agent.
    Saves the output as a DRAFT in the reports table.
    Fails if the report is already APPROVED.
    """
    report = db.query(VisitReport).filter(VisitReport.visit_id == visit.id).first()
    if report and report.status == "APPROVED":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot re-run orchestration on an APPROVED visit."
        )
        
    return run_orchestration_for_visit(db, visit)


# --- Report Routes ---

@report_router.get(
    "",
    response_model=VisitReportResponse,
    summary="Fetch the visit report"
)
def get_report(
    visit: Visit = Depends(require_visit_participant), # Patient or Doctor
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Fetches the Visit Report. 
    IMPORTANT SAFETY RULE: Patients cannot view the report if it is in DRAFT state.
    """
    report = db.query(VisitReport).filter(VisitReport.visit_id == visit.id).first()
    if not report:
        raise HTTPException(status_code=404, detail="No report generated for this visit yet.")

    # Guardrail Check - The Patient shouldn't be reading raw hallucination drafts!
    if report.status == "DRAFT" and current_user.role != "doctor":
        raise HTTPException(
            status_code=403, 
            detail="Report is still in DRAFT mode and requires doctor approval."
        )
        
    return report


@report_router.patch(
    "",
    response_model=VisitReportResponse,
    summary="Update report draft fields"
)
def update_report_draft(
    update_data: VisitReportUpdate,
    visit: Visit = Depends(require_assigned_doctor),
    db: Session = Depends(get_db)
):
    """
    Allows the assigned doctor to edit the DRAFT report fields.
    Fails if the report has already been APPROVED.
    """
    report = db.query(VisitReport).filter(VisitReport.visit_id == visit.id).first()
    if not report:
        raise HTTPException(status_code=404, detail="No report found.")
        
    if report.status == "APPROVED":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot edit an APPROVED report."
        )
        
    # Apply partial updates dynamically
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(report, key, value)
        
    db.commit()
    db.refresh(report)
    return report


@report_router.post(
    "/approve",
    response_model=VisitReportResponse,
    summary="Approve and Finalize the Report"
)
def approve_report(
    visit: Visit = Depends(require_assigned_doctor),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Locks the report data, converting it from DRAFT to APPROVED.
    This creates the source of truth for the patient dashboard and reminder systems.
    """
    report = db.query(VisitReport).filter(VisitReport.visit_id == visit.id).first()
    if not report:
        raise HTTPException(status_code=404, detail="No report found.")
        
    if report.status == "APPROVED":
        # Already approved, idempotent response
        return report
        
    report.status = "APPROVED"
    report.approved_by_id = current_user.id
    report.approved_at = datetime.utcnow()
    
    db.commit()
    db.refresh(report)
    return report

