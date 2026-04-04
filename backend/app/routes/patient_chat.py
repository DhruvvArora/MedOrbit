from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role, get_visit_or_404
from app.models.user import User
from app.models.visit import Visit
from app.models.report import VisitReport
from app.schemas.patient_chat import PatientChatRequest, PatientChatResponse

from agents.patient_simplifier.agent import PatientSimplifierAgent

router = APIRouter(
    prefix="/patient/visits/{visit_id}/explain-chat",
    tags=["Patient Simplifier Chat"],
    dependencies=[Depends(require_role("patient"))]
)

@router.post("", response_model=PatientChatResponse)
def ask_patient_simplifier(
    request: PatientChatRequest,
    visit: Visit = Depends(get_visit_or_404),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submits a conversational query against the APPROVED doctor's report.
    Stateless boundary: Does not retain chat history across subsequent calls.
    """
    # 1. Scope Constraint
    if visit.patient_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to query this visit context.")
        
    # 2. Approved-Only Constraint
    report = db.query(VisitReport).filter(VisitReport.visit_id == visit.id).first()
    if not report or report.status != "APPROVED":
        raise HTTPException(
            status_code=403, 
            detail="There is no approved report available to reference for this visit."
        )

    # 3. Execution
    agent = PatientSimplifierAgent()
    
    agent_response = agent.explain(
        patient_question=request.message,
        simplified_explanation=report.simplified_explanation,
        discharge_draft=report.patient_discharge_draft,
        reminders=report.reminder_candidates
    )
    
    return PatientChatResponse(
        answer=agent_response.answer,
        is_supported=agent_response.is_supported,
        refusal_reason=agent_response.refusal_reason,
        safety_note="AI Explanation. If you are experiencing an emergency, dial 911."
    )
