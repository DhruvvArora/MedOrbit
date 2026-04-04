import json
from sqlalchemy.orm import Session
from app.models.visit import Visit
from app.models.report import VisitReport

from agents.shared.transcript_adapter import load_transcript_plaintext
from agents.behavioral.agent import BehavioralInsightAgent
from agents.triage.agent import TriageInsightAgent
from agents.super_agent.agent import SuperInsightAgent


def run_orchestration_for_visit(db: Session, visit: Visit) -> VisitReport:
    """
    Executes the entire multi-agent orchestration for a given visit.
    1. Fetches Transcript.
    2. Runs Triage Agent.
    3. Runs Behavioral Agent.
    4. Combines outputs into Super Agent.
    5. Saves output securely as a DRAFT VisitReport in the DB.
    
    If the report is already APPROVED, an exception should be thrown before reaching here.
    """
    # 1. Fetch transcript string
    transcript_text = load_transcript_plaintext(visit.id) or ""
    
    # 2. Run isolated agents
    behavioral_agent = BehavioralInsightAgent()
    behavioral_output = behavioral_agent.analyze(transcript_text).model_dump()
    
    triage_agent = TriageInsightAgent()
    triage_output = triage_agent.analyze(transcript_text).model_dump()
    
    # 3. Trigger Super Agent Synthesizer
    super_agent = SuperInsightAgent()
    super_output = super_agent.analyze(
        str(visit.id), transcript_text, behavioral_output, triage_output
    )

    # 4. Bind to DB (Component 7 logic)
    # Check if a DRAFT report already exists to overwrite, or create a new one.
    report = db.query(VisitReport).filter(VisitReport.visit_id == visit.id).first()
    
    if not report:
        report = VisitReport(visit_id=visit.id, status="DRAFT")
        db.add(report)
    
    # Overwrite the draft fields 
    report.doctor_summary = super_output.doctor_summary
    report.patient_discharge_draft = super_output.patient_discharge_draft
    report.simplified_explanation = super_output.simplified_explanation
    report.clinical_review_flags = super_output.clinical_review_flags
    report.reminder_candidates = super_output.reminder_candidates
    # Automatically resets to DRAFT if an accidental rerun logic allows it
    report.status = "DRAFT" 

    db.commit()
    db.refresh(report)

    return report
