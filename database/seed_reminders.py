"""
Seed script to artificially invoke the Reminder Generator route logic 
to fill the UI for Patient tests.
"""

from app.core.database import SessionLocal
from app.models.visit import Visit
from app.models.report import VisitReport
from app.models.reminder import Reminder
from datetime import datetime, timedelta

def seed_reminders():
    db = SessionLocal()
    
    # Target Alex Johnson's Hypertension Visit
    visit = db.query(Visit).filter(Visit.title == "Routine Physical (Hypertension)").first()
    if not visit:
        print("Required visit not seeded yet.")
        return
        
    report = db.query(VisitReport).filter(VisitReport.visit_id == visit.id, VisitReport.status == "APPROVED").first()
    if not report:
        print("Required report not seeded or not approved.")
        return

    existing = db.query(Reminder).filter(Reminder.visit_id == visit.id).count()
    if existing > 0:
        print("Reminders already seeded for this visit.")
        return

    now = datetime.utcnow()

    r1 = Reminder(
        visit_id=visit.id,
        patient_id=visit.patient_id,
        source_report_id=report.id,
        title="Schedule 6-month lipid panel",
        status="PENDING",
        due_at=now + timedelta(days=7)
    )
    
    r2 = Reminder(
        visit_id=visit.id,
        patient_id=visit.patient_id,
        source_report_id=report.id,
        title="Log daily blood pressure",
        status="COMPLETED",
        due_at=now - timedelta(days=1),
        completed_at=now
    )

    db.add(r1)
    db.add(r2)
    db.commit()

    print("✅ Dummy Reminders injected securely into DB.")

if __name__ == "__main__":
    seed_reminders()
