import os
import sys
from datetime import datetime, UTC

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.core.database import SessionLocal, engine
from app.models import Base
from app.models.visit import Visit
from app.models.report import VisitReport


def seed_reports():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        knee_visit = (
            db.query(Visit)
            .filter(Visit.title == "In-Person Follow up (Knee Pain)")
            .first()
        )

        intake_visit = (
            db.query(Visit)
            .filter(Visit.title == "Past Consultation (Initial intake)")
            .first()
        )

        if not knee_visit:
            print("❌ Knee visit not found. Run seed_visits.py first.")
            return

        if not intake_visit:
            print("❌ Intake visit not found. Run seed_visits.py first.")
            return

        existing_knee = (
            db.query(VisitReport)
            .filter(VisitReport.visit_id == knee_visit.id)
            .first()
        )
        if existing_knee:
            db.delete(existing_knee)
            db.flush()

        existing_intake = (
            db.query(VisitReport)
            .filter(VisitReport.visit_id == intake_visit.id)
            .first()
        )
        if existing_intake:
            db.delete(existing_intake)
            db.flush()

        knee_report = VisitReport(
            visit_id=knee_visit.id,
            status="APPROVED",
            doctor_summary=(
                "Patient reports right knee pain after restarting jogging. "
                "Symptoms are consistent with overuse injury / runner's knee. "
                "Advised rest from high-impact activity, stretching, icing, and follow-up if symptoms worsen."
            ),
            patient_discharge_draft=(
                "Rest the knee, avoid jogging for one week, continue gentle stretching, "
                "use ice after activity, and return if swelling or sharp pain increases."
            ),
            simplified_explanation=(
                "Your knee pain is likely from overuse after restarting exercise. "
                "The plan is to reduce impact, stretch regularly, and monitor recovery."
            ),
            clinical_review_flags=[
                "Pain worsens on stairs",
                "Recent restart of jogging",
                "No major trauma reported",
            ],
            reminder_candidates=[
                "Stretch knee twice daily",
                "Avoid high-impact jogging for 7 days",
                "Ice knee after activity",
                "Track pain level once daily",
            ],
            approved_by_id=knee_visit.doctor_id,
            approved_at=datetime.now(UTC),
        )

        intake_report = VisitReport(
            visit_id=intake_visit.id,
            status="DRAFT",
            doctor_summary=(
                "Initial intake completed for elevated blood pressure, stress, and poor sleep."
            ),
            patient_discharge_draft=(
                "Reduce sodium intake, improve sleep hygiene, and follow up in two weeks."
            ),
            simplified_explanation=(
                "We discussed your blood pressure, stress, sleep habits, and next steps."
            ),
            clinical_review_flags=[
                "Elevated stress may be contributing to symptoms",
                "Sleep quality needs improvement",
            ],
            reminder_candidates=[
                "Check blood pressure daily",
                "Reduce sodium intake",
                "Aim for 7 hours of sleep",
            ],
        )

        db.add(knee_report)
        db.add(intake_report)
        db.commit()
        print("✅ Reports seeded successfully.")

    except Exception as e:
        db.rollback()
        print(f"❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_reports()