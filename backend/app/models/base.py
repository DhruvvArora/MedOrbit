"""
MedOrbit — SQLAlchemy Declarative Base

All models inherit from this Base.
Import `Base` when defining new models, and `Base.metadata` for migrations.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models in MedOrbit."""
    pass
