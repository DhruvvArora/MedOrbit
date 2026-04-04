"""
MedOrbit — Behavioral Agent Routes

Provides an internal/testing endpoint to invoke the Behavioral Health Insight Agent.
"""

from fastapi import APIRouter, Depends

from app.core.dependencies import require_assigned_doctor
from app.models.visit import Visit
from app.services.behavioral_service import run_behavioral_agent_for_visit


router = APIRouter(
    prefix="/visits/{visit_id}/agents/behavioral",
    tags=["Agents - Behavioral"],
)

@router.post(
    "/run",
    summary="Run Behavioral Agent manually",
    description="Invokes the Behavioral Insight Agent on the visit's transcript and returns the structured JSON findings."
)
def run_behavioral_agent(
    visit: Visit = Depends(require_assigned_doctor),
):
    """
    Execute the agent on-demand.
    Requires doctor authorization.
    """
    insights_dict = run_behavioral_agent_for_visit(visit)
    return insights_dict
