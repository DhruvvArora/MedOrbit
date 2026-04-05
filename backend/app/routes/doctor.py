from collections import Counter
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_assigned_doctor, require_role
from app.models.report import VisitReport
from app.models.transcript import TranscriptChunk
from app.models.user import User
from app.models.visit import Visit
from app.schemas.doctor import (
    ConsultationWorkspaceResponse,
    DoctorDashboardSummaryResponse,
    DoctorVisitListItem,
    ReportStatusSummary,
    TranscriptChunkView,
    TranscriptStatsView,
)

router = APIRouter(prefix="/doctor", tags=["Doctor UI"])


def _to_report_status(report: VisitReport | None) -> str:
    if not report:
        return "none"
    return "approved" if report.status == "APPROVED" else "draft"


def _visit_list_item(db: Session, visit: Visit) -> DoctorVisitListItem:
    patient = db.query(User).filter(User.id == visit.patient_id).first()
    report = db.query(VisitReport).filter(VisitReport.visit_id == visit.id).first()
    last_chunk = (
        db.query(TranscriptChunk)
        .filter(TranscriptChunk.visit_id == visit.id)
        .order_by(TranscriptChunk.sequence_number.desc())
        .first()
    )
    last_activity_at = None
    if last_chunk:
        last_activity_at = last_chunk.created_at
    elif visit.updated_at:
        last_activity_at = visit.updated_at

    return DoctorVisitListItem(
        id=visit.id,
        title=visit.title,
        status=visit.status,
        type=visit.type,
        patient_name=patient.full_name if patient else "Unknown Patient",
        started_at=visit.started_at,
        ended_at=visit.ended_at,
        created_at=visit.created_at,
        transcript_chunk_count=visit.transcript_chunk_count,
        transcript_ready=visit.transcript_chunk_count > 0,
        report_status=_to_report_status(report),
        last_activity_at=last_activity_at,
    )


@router.get("/dashboard-summary", response_model=DoctorDashboardSummaryResponse)
def get_doctor_dashboard_summary(
    current_user: User = Depends(require_role("doctor")),
    db: Session = Depends(get_db),
):
    visits = (
        db.query(Visit)
        .filter(Visit.doctor_id == current_user.id)
        .order_by(Visit.updated_at.desc(), Visit.created_at.desc())
        .all()
    )
    items = [_visit_list_item(db, visit) for visit in visits]

    counts = {
        "total": len(items),
        "scheduled": sum(1 for item in items if item.status == "scheduled"),
        "active": sum(1 for item in items if item.status == "active"),
        "completed": sum(1 for item in items if item.status == "completed"),
        "cancelled": sum(1 for item in items if item.status == "cancelled"),
        "draft_reports": sum(1 for item in items if item.report_status == "draft"),
        "approved_reports": sum(1 for item in items if item.report_status == "approved"),
    }
    return DoctorDashboardSummaryResponse(
        doctor_id=current_user.id,
        doctor_name=current_user.full_name,
        counts=counts,
        visits=items,
    )


@router.get("/visits/{visit_id}/workspace", response_model=ConsultationWorkspaceResponse)
def get_consultation_workspace(
    visit: Visit = Depends(require_assigned_doctor),
    db: Session = Depends(get_db),
):
    visit_item = _visit_list_item(db, visit)
    chunks = (
        db.query(TranscriptChunk)
        .filter(TranscriptChunk.visit_id == visit.id)
        .order_by(TranscriptChunk.sequence_number.asc())
        .all()
    )
    speaker_breakdown = Counter(chunk.speaker_role for chunk in chunks)
    source_breakdown = Counter(chunk.source_type for chunk in chunks)
    report = db.query(VisitReport).filter(VisitReport.visit_id == visit.id).first()

    available_actions = ["refresh_transcript"]
    if visit.status == "scheduled":
        available_actions.append("start_visit")
    if visit.status == "active":
        available_actions.extend(["run_behavioral", "run_triage", "run_orchestration", "complete_visit"])
    if report and report.status == "DRAFT":
        available_actions.extend(["edit_report", "approve_report"])
    if report and report.status == "APPROVED":
        available_actions.append("generate_reminders")

    return ConsultationWorkspaceResponse(
        visit=visit_item,
        transcript_stats=TranscriptStatsView(
            total_chunks=len(chunks),
            speaker_breakdown=dict(speaker_breakdown),
            source_breakdown=dict(source_breakdown),
            first_chunk_at=chunks[0].created_at.isoformat() if chunks else None,
            last_chunk_at=chunks[-1].created_at.isoformat() if chunks else None,
            total_characters=sum(len(chunk.text or "") for chunk in chunks),
        ),
        transcript_chunks=[
    TranscriptChunkView(
        id=chunk.id,
        sequence_number=chunk.sequence_number,
        speaker_role=chunk.speaker_role or "unknown",
        speaker_label=chunk.speaker_label,
        text=chunk.text or "",
        source_type=chunk.source_type or "unknown",
        created_at=chunk.created_at,
    )
    for chunk in chunks
],
        report_status=ReportStatusSummary(
            exists=report is not None,
            status=_to_report_status(report),
            approved_at=report.approved_at if report else None,
            approved_by_id=str(report.approved_by_id) if report and report.approved_by_id is not None else None,
            reminder_candidates_count=len((report.reminder_candidates or [])) if report else 0,
        ),
        report_preview={
            "doctor_summary": report.doctor_summary,
            "patient_discharge_draft": report.patient_discharge_draft,
            "simplified_explanation": report.simplified_explanation,
            "clinical_review_flags": report.clinical_review_flags or [],
            "reminder_candidates": report.reminder_candidates or [],
            "updated_at": report.updated_at.isoformat() if report and report.updated_at else None,
        } if report else None,
        available_actions=available_actions,
    )
