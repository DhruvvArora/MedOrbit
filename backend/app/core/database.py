"""
MedOrbit — Database Engine & Session Management

SQLAlchemy engine, session factory, and `get_db` dependency.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# ── Engine ───────────────────────────────────────────────────

# SQLite requires check_same_thread=False for FastAPI's threaded usage.
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ── Dependency ───────────────────────────────────────────────

def get_db() -> Session:
    """
    FastAPI dependency that yields a database session.

    Usage:
        @router.get("/example")
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
