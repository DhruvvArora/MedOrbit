"""
MedOrbit — Clinical Triage Agent Routes

Provides an internal/testing endpoint to invoke the Clinical Triage Agent.
"""

from fastapi import APIRouter, Depends

from app.core.dependencies import require_assigned_doctor
from app.models.visit import Visit
from app.services.triage_service import run_triage_agent_for_visit


router = APIRouter(
    prefix="/visits/{visit_id}/agents/clinical-triage",
    tags=["Agents - Clinical Triage"],
)

@router.post(
    "/run",
    summary="Run Clinical Triage Agent manually",
    description="Invokes the Clinical Triage Agent on the visit's transcript and returns the structured JSON triage intake."
)
def run_triage_agent(
    visit: Visit = Depends(require_assigned_doctor),
):
    """
    Execute the agent on-demand.
    Requires doctor authorization.
    """
    insights_dict = run_triage_agent_for_visit(visit)
    return insights_dict
