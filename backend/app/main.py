"""
MedOrbit — FastAPI Application Entrypoint

Creates the FastAPI app, configures CORS, and mounts all routers.

Run with:
    cd backend
    uvicorn app.main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine
from app.models.base import Base
from app.routes import auth as auth_routes
from app.routes import visits as visits_routes
from app.routes import transcripts as transcripts_routes
from app.routes import behavioral as behavioral_routes
from app.routes import triage as triage_routes
from app.routes import reports as reports_routes
from app.routes import patient as patient_routes
from app.routes import patient_chat as patient_chat_routes
from app.routes import reminders as reminder_doctor_routes
from app.routes import doctor as doctor_routes
from app.models.report import VisitReport
from app.models.reminder import Reminder  # Database auto-discovery hook

# ── Create Tables (dev convenience — use Alembic in production) ──
Base.metadata.create_all(bind=engine)

# ── App ──────────────────────────────────────────────────────

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "AI-assisted doctor–patient care platform. "
        "Transcript-first, doctor-in-the-loop."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ─────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────────

app.include_router(auth_routes.router, prefix="/api")
app.include_router(visits_routes.router, prefix="/api")
app.include_router(transcripts_routes.router, prefix="/api")
app.include_router(behavioral_routes.router, prefix="/api")
app.include_router(triage_routes.router, prefix="/api")
app.include_router(reports_routes.orchestration_router, prefix="/api")
app.include_router(reports_routes.report_router, prefix="/api")
app.include_router(reminder_doctor_routes.router, prefix="/api")
app.include_router(patient_routes.router, prefix="/api")
app.include_router(patient_chat_routes.router, prefix="/api")
app.include_router(doctor_routes.router, prefix="/api")


# ── Health Check ─────────────────────────────────────────────

@app.get("/health", tags=["System"])
def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy", "app": settings.APP_NAME}
