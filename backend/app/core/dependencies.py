"""
MedOrbit — FastAPI Dependencies for Auth & RBAC

This is the module that every protected route imports from.

Usage:
    from app.core.dependencies import get_current_user, require_role

    # Any authenticated user
    @router.get("/profile")
    def profile(user: User = Depends(get_current_user)):
        ...

    # Doctor-only route
    @router.post("/visits")
    def create_visit(user: User = Depends(require_role("doctor"))):
        ...
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.models.visit import Visit

# Allow missing bearer token when SKIP_AUTH is on
security_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> User:
    # Temporary dev bypass
    if settings.SKIP_AUTH:
        demo_user = db.query(User).filter(User.email == "doctor@medorbit.demo").first()
        if demo_user is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="SKIP_AUTH is enabled but demo doctor user was not found.",
            )
        return demo_user

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    return user


def require_role(*allowed_roles: str):
    def role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role: {', '.join(allowed_roles)}",
            )
        return user

    return role_checker


def get_visit_or_404(visit_id: str, db: Session = Depends(get_db)) -> Visit:
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit


def require_visit_participant(
    visit: Visit = Depends(get_visit_or_404),
    current_user: User = Depends(get_current_user),
) -> Visit:
    if current_user.id not in [visit.doctor_id, visit.patient_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a participant in this visit.",
        )
    return visit


def require_assigned_doctor(
    visit: Visit = Depends(get_visit_or_404),
    current_user: User = Depends(require_role("doctor")),
) -> Visit:
    if current_user.id != visit.doctor_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the assigned doctor for this visit.",
        )
    return visit
    