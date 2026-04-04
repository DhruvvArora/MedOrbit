"""
MedOrbit — Auth Service (Business Logic Layer)

Pure business logic for user registration and authentication.
No HTTP/FastAPI concerns — just takes data in, returns data or raises.
"""

from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User


class AuthServiceError(Exception):
    """Base exception for auth service errors."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class DuplicateEmailError(AuthServiceError):
    """Raised when a registration email already exists."""

    def __init__(self):
        super().__init__("A user with this email already exists", status_code=409)


class InvalidCredentialsError(AuthServiceError):
    """Raised when login credentials are incorrect."""

    def __init__(self):
        super().__init__("Invalid email or password", status_code=401)


class InactiveAccountError(AuthServiceError):
    """Raised when an inactive user attempts to log in."""

    def __init__(self):
        super().__init__("Account is deactivated", status_code=403)


# ── Service Functions ────────────────────────────────────────


def register_user(
    db: Session,
    full_name: str,
    email: str,
    password: str,
    role: str,
) -> User:
    """
    Register a new user.

    Args:
        db: Database session.
        full_name: User's display name.
        email: Unique login email.
        password: Plaintext password (will be hashed).
        role: "doctor" or "patient".

    Returns:
        The newly created User.

    Raises:
        DuplicateEmailError: If email is already registered.
    """
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise DuplicateEmailError()

    user = User(
        full_name=full_name,
        email=email,
        password_hash=hash_password(password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> tuple[User, str]:
    """
    Authenticate a user and return a JWT access token.

    Args:
        db: Database session.
        email: Login email.
        password: Plaintext password.

    Returns:
        Tuple of (User, access_token string).

    Raises:
        InvalidCredentialsError: If email not found or password wrong.
        InactiveAccountError: If user.is_active is False.
    """
    user = db.query(User).filter(User.email == email).first()

    if user is None or not verify_password(password, user.password_hash):
        raise InvalidCredentialsError()

    if not user.is_active:
        raise InactiveAccountError()

    access_token = create_access_token(
        data={"sub": user.id, "role": user.role}
    )

    return user, access_token


def get_user_by_id(db: Session, user_id: str) -> User | None:
    """Retrieve a user by their ID."""
    return db.query(User).filter(User.id == user_id).first()
