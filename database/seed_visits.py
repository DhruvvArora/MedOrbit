"""
MedOrbit — Visit Seed Script

Creates sample visits between the demo doctors and patients.
Useful for testing UI lists and lifecycle buttons.

Usage:
    cd backend
    python -m database.seed_visits
    # — or —
    python ../database/seed_visits.py
"""

import sys
import os

# Ensure the backend package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.core.database import SessionLocal, engine
from app.models.base import Base
from app.models.user import User
from app.models.visit import Visit
from app.schemas.visit import VisitType, VisitStatus

def seed_visits():
    """Create sample visits for demo doctor and patient."""
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Load our known seed users from seed.py
        doctor1 = db.query(User).filter(User.email == "doctor@medorbit.demo").first()
        patient1 = db.query(User).filter(User.email == "patient@medorbit.demo").first()
        
        if not doctor1 or not patient1:
            print("❌ Cannot seed visits: Base demo users not found. Run database/seed.py first.")
            return

        print(f"Creating sample visits for {doctor1.full_name} and {patient1.full_name}...")

        # 1. Scheduled Virtual Checkup
        visit1 = Visit(
            doctor_id=doctor1.id,
            patient_id=patient1.id,
            type=VisitType.VIRTUAL.value,
            status=VisitStatus.SCHEDULED.value,
            title="Routine Virtual Checkup"
        )
        db.add(visit1)

        # 2. Active In-Person Follow Up
        visit2 = Visit(
            doctor_id=doctor1.id,
            patient_id=patient1.id,
            type=VisitType.IN_PERSON.value,
            status=VisitStatus.ACTIVE.value,
            title="In-Person Follow up (Knee Pain)"
        )
        db.add(visit2)

        # 3. Completed Virtual
        visit3 = Visit(
            doctor_id=doctor1.id,
            patient_id=patient1.id,
            type=VisitType.VIRTUAL.value,
            status=VisitStatus.COMPLETED.value,
            title="Past Consultation (Initial intake)"
        )
        db.add(visit3)

        # 4. Cancelled In-Person
        visit4 = Visit(
            doctor_id=doctor1.id,
            patient_id=patient1.id,
            type=VisitType.IN_PERSON.value,
            status=VisitStatus.CANCELLED.value,
            title="Cancelled Lab Results Review"
        )
        db.add(visit4)

        db.commit()
        print("✅ Seeded 4 sample visits (Scheduled, Active, Completed, Cancelled).")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seeding MedOrbit demo visits...\n")
    seed_visits()
