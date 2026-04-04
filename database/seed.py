"""
MedOrbit — Database Seed Script

Creates demo doctor and patient users for hackathon testing.
Idempotent — safe to run multiple times (skips existing emails).

Usage:
    cd backend
    python -m database.seed
    # — or —
    python ../database/seed.py
"""

import sys
import os

# Ensure the backend package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.core.database import SessionLocal, engine
from app.core.security import hash_password
from app.models.base import Base
from app.models.user import User

# ── Demo Users ───────────────────────────────────────────────

SEED_USERS = [
    {
        "full_name": "Dr. Sarah Chen",
        "email": "doctor@medorbit.demo",
        "password": "doctor123",
        "role": "doctor",
    },
    {
        "full_name": "Dr. James Rivera",
        "email": "doctor2@medorbit.demo",
        "password": "doctor123",
        "role": "doctor",
    },
    {
        "full_name": "Alex Johnson",
        "email": "patient@medorbit.demo",
        "password": "patient123",
        "role": "patient",
    },
    {
        "full_name": "Maria Garcia",
        "email": "patient2@medorbit.demo",
        "password": "patient123",
        "role": "patient",
    },
]


def seed():
    """Insert demo users if they don't already exist."""
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    created = 0
    skipped = 0

    try:
        for user_data in SEED_USERS:
            existing = (
                db.query(User).filter(User.email == user_data["email"]).first()
            )
            if existing:
                print(f"  ⏭  Skipped (exists): {user_data['email']}")
                skipped += 1
                continue

            user = User(
                full_name=user_data["full_name"],
                email=user_data["email"],
                password_hash=hash_password(user_data["password"]),
                role=user_data["role"],
            )
            db.add(user)
            created += 1
            print(f"  ✅ Created: {user_data['email']} ({user_data['role']})")

        db.commit()
        print(f"\nSeed complete: {created} created, {skipped} skipped.")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seeding MedOrbit demo users...\n")
    seed()
