"""
MedOrbit — Auth Schemas (Pydantic v2)

Request/response models for registration, login, and user retrieval.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


# ── Enums ────────────────────────────────────────────────────

class UserRole(str, Enum):
    """Allowed user roles."""
    DOCTOR = "doctor"
    PATIENT = "patient"


# ── Request Schemas ──────────────────────────────────────────

class RegisterRequest(BaseModel):
    """Registration payload."""
    full_name: str = Field(
        ..., min_length=1, max_length=100, examples=["Dr. Sarah Chen"]
    )
    email: EmailStr = Field(..., examples=["sarah@hospital.com"])
    password: str = Field(
        ..., min_length=8, max_length=128, examples=["SecurePass123!"]
    )
    role: UserRole = Field(..., examples=["doctor"])


class LoginRequest(BaseModel):
    """Login payload."""
    email: EmailStr = Field(..., examples=["sarah@hospital.com"])
    password: str = Field(..., min_length=1, examples=["SecurePass123!"])


# ── Response Schemas ─────────────────────────────────────────

class UserResponse(BaseModel):
    """Public user representation (no password hash)."""
    id: str
    full_name: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """Login success response with JWT and user info."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class MessageResponse(BaseModel):
    """Generic message response for simple confirmations."""
    message: str
