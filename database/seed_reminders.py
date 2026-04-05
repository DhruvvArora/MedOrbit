import os
import sys
from datetime import datetime, timedelta, UTC

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.core.database import SessionLocal
from app.models.visit import Visit
from app.models.report import VisitReport
from app.models.reminder import Reminder


def seed_reminders():
    db = SessionLocal()

    try:
        visit = (
            db.query(Visit)
            .filter(Visit.title == "In-Person Follow up (Knee Pain)")
            .first()
        )

        if not visit:
            print("❌ Knee visit not found.")
            return

        report = (
            db.query(VisitReport)
            .filter(VisitReport.visit_id == visit.id)
            .first()
        )

        if not report:
            print("❌ Report not found for knee visit.")
            return

        existing = db.query(Reminder).filter(Reminder.visit_id == visit.id).all()
        for r in existing:
            db.delete(r)
        db.flush()

        now = datetime.now(UTC)

        reminders = [
            Reminder(
                visit_id=visit.id,
                patient_id=visit.patient_id,
                source_report_id=report.id,
                title="Stretch knee twice daily",
                status="pending",
                due_at=now + timedelta(hours=12),
            ),
            Reminder(
                visit_id=visit.id,
                patient_id=visit.patient_id,
                source_report_id=report.id,
                title="Avoid high-impact jogging for 7 days",
                status="pending",
                due_at=now + timedelta(days=1),
            ),
            Reminder(
                visit_id=visit.id,
                patient_id=visit.patient_id,
                source_report_id=report.id,
                title="Ice knee after activity",
                status="pending",
                due_at=now + timedelta(hours=8),
            ),
        ]

        db.add_all(reminders)
        db.commit()
        print("✅ Reminders seeded successfully.")

    except Exception as e:
        db.rollback()
        print(f"❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_reminders()