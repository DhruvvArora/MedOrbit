"""
Script to seed the MedOrbit Database with MVP Reports.
Useful for mocking out the UI without running the AI agents.
"""

from app.core.database import SessionLocal
from app.models.visit import Visit
from app.models.report import VisitReport
from datetime import datetime

def seed_reports():
    db = SessionLocal()
    
    # 1. Retrieve the seeded visits
    visits = db.query(Visit).all()
    if len(visits) < 2:
        print("Not enough visits to seed. Run seed_transcripts.py first.")
        return

    v1 = visits[0]  # Alex Johnson (Hypertension)
    v2 = visits[1]  # Active visit

    # Seed Visit 1 as APPROVED
    r1 = db.query(VisitReport).filter(VisitReport.visit_id == v1.id).first()
    if not r1:
        r1 = VisitReport(
            visit_id=v1.id,
            status="APPROVED",
            doctor_summary="Alex Johnson presented for routine physical. Labs indicated mild hyperlipidemia. Discussed dietary shifts.",
            simplified_explanation="Today you had a routine checkup. Everything looks mostly great, but your cholesterol is slightly high. Try eating more vegetables and less fried food.",
            patient_discharge_draft="Dietary Guidelines updated. Increase fiber intake.",
            reminder_candidates=["Schedule 6-month lipid panel"],
            clinical_review_flags=[],
            approved_by_id=v1.doctor_id,
            approved_at=datetime.utcnow()
        )
        db.add(r1)

    # Seed Visit 2 as DRAFT
    r2 = db.query(VisitReport).filter(VisitReport.visit_id == v2.id).first()
    if not r2:
        r2 = VisitReport(
            visit_id=v2.id,
            status="DRAFT",
            doctor_summary="Patient complains of escalating migraine frequency. DRAFT NOTES ONLY.",
            simplified_explanation="You reported strong headaches. Dr. Smith is reviewing the plan.",
            patient_discharge_draft="Start magnesium supplement protocol.",
            reminder_candidates=["Take magnesium 400mg daily", "Log headaches in app"],
            clinical_review_flags=["Patient reported visual aura pre-migraine."]
        )
        db.add(r2)

    db.commit()
    print("✅ Dummy Reports seeded successfully.")

if __name__ == "__main__":
    seed_reports()
