"""
MedOrbit — Auth Routes

POST /api/auth/register  — Create a new account
POST /api/auth/login     — Authenticate and receive JWT
GET  /api/auth/me        — Get current user profile
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth_service import (
    AuthServiceError,
    authenticate_user,
    register_user,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ── POST /auth/register ─────────────────────────────────────


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new doctor or patient account.",
)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user with a hashed password.

    - **full_name**: Display name (1–100 chars)
    - **email**: Unique email address
    - **password**: At least 8 characters
    - **role**: "doctor" or "patient"
    """
    try:
        user = register_user(
            db=db,
            full_name=body.full_name,
            email=body.email,
            password=body.password,
            role=body.role.value,
        )
        return user
    except AuthServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


# ── POST /auth/login ────────────────────────────────────────


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login",
    description="Authenticate with email and password. Returns a JWT access token.",
)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT token.

    - **email**: Registered email address
    - **password**: Account password
    """
    try:
        user, access_token = authenticate_user(
            db=db,
            email=body.email,
            password=body.password,
        )
        return TokenResponse(
            access_token=access_token,
            user=UserResponse.model_validate(user),
        )
    except AuthServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


# ── GET /auth/me ─────────────────────────────────────────────


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Returns the profile of the currently authenticated user.",
)
def me(current_user: User = Depends(get_current_user)):
    """
    Retrieve the authenticated user's profile.

    Requires a valid Bearer token in the Authorization header.
    """
    return current_user
