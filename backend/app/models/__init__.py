"""
MedOrbit — Models Package

Import all models here to ensure SQLAlchemy's mapper registry
knows about every model class BEFORE any relationship() string
references are resolved.

Any script that uses ANY model should do:
    from app.models import User, Visit, TranscriptChunk
    # or just: import app.models  (to trigger registration)
"""

from app.models.base import Base  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.visit import Visit  # noqa: F401
from app.models.transcript import TranscriptChunk  # noqa: F401
