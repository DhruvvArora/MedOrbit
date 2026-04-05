# MedOrbit — Auth & RBAC Reference

## Overview

The auth system uses **JWT Bearer tokens** with **bcrypt** password hashing.
Every request to a protected endpoint must include:

```
Authorization: Bearer <access_token>
```

Tokens expire after **24 hours** (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`).

---

## Auth Flow

```
                     Home Screen
                         │
                    ┌────┴────┐
                    │  Login  │  ← or "Create Account" → Register
                    └────┬────┘
                         │
              POST /api/auth/login
           { email, password }
                         │
                    ┌────┴────┐
                    │  Server │ → validate → create JWT
                    └────┬────┘
                         │
              { access_token, user }
                         │
              ┌──────────┴──────────┐
              │                     │
         role=doctor          role=patient
              │                     │
    /doctor/dashboard     /patient/dashboard
```

### Frontend Auth Flow

1. User clicks **Login** on the home screen navbar
2. Login page: enter email + password → `POST /api/auth/login`
3. On success: JWT stored in `localStorage`, redirect by role
4. On failure: error message shown inline
5. Token validated on app load via `GET /api/auth/me`
6. If token expired/invalid: auto-logout, redirect to `/login`

### Registration Flow

1. User clicks **Create one** on the login page
2. Register page: enter name, email, password, select role
3. `POST /api/auth/register` → auto-login → redirect by role

---

## Endpoints

### POST `/api/auth/register`

Create a new account.

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Dr. Sarah Chen",
    "email": "sarah@hospital.com",
    "password": "SecurePass123!",
    "role": "doctor"
  }'
```

**Response (201):**
```json
{
  "id": "uuid",
  "full_name": "Dr. Sarah Chen",
  "email": "sarah@hospital.com",
  "role": "doctor",
  "is_active": true,
  "created_at": "2026-04-04T20:00:00Z"
}
```

### POST `/api/auth/login`

Authenticate and receive JWT.

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "doctor@medorbit.demo",
    "password": "doctor123"
  }'
```

**Response (200):**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "full_name": "Dr. Sarah Chen",
    "email": "doctor@medorbit.demo",
    "role": "doctor",
    "is_active": true,
    "created_at": "2026-04-04T20:00:00Z"
  }
}
```

### GET `/api/auth/me`

Get current user profile. Requires Bearer token.

```bash
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer eyJ..."
```

---

## Demo Credentials

| Role    | Email                    | Password     |
|---------|--------------------------|--------------|
| Doctor  | `doctor@medorbit.demo`   | `doctor123`  |
| Doctor  | `doctor2@medorbit.demo`  | `doctor123`  |
| Patient | `patient@medorbit.demo`  | `patient123` |
| Patient | `patient2@medorbit.demo` | `patient123` |

Run the seed script to create these accounts:
```bash
cd backend && python ../database/seed.py
```

---

## Route Protection

### Frontend Routes

| Path | Access | Behavior |
|------|--------|----------|
| `/` | Public | Landing page |
| `/login` | Public | Redirects to dashboard if authenticated |
| `/register` | Public | Redirects to dashboard if authenticated |
| `/doctor/*` | Doctor only | Redirects to `/login` if unauthenticated |
| `/patient/*` | Patient only | Redirects to `/login` if unauthenticated |

### Redirect Rules

| Scenario | Action |
|----------|--------|
| Unauthenticated → protected route | → `/login` |
| Authenticated doctor → `/login` | → `/doctor/dashboard` |
| Authenticated patient → `/login` | → `/patient/dashboard` |
| Doctor → `/patient/*` | → `/doctor/dashboard` |
| Patient → `/doctor/*` | → `/patient/dashboard` |
| Logout | Clear auth → `/` |

### Backend Dependencies

```python
from app.core.dependencies import get_current_user, require_role

# Any authenticated user
@router.get("/profile")
def profile(user = Depends(get_current_user)): ...

# Doctor-only
@router.post("/visits")
def create_visit(user = Depends(require_role("doctor"))): ...

# Patient-only
@router.get("/my-reports")
def my_reports(user = Depends(require_role("patient"))): ...
```

### Error Responses

| Code | Meaning                     |
|------|-----------------------------|
| 401  | Missing / invalid / expired token |
| 403  | Account inactive or wrong role    |
| 409  | Duplicate email on register       |
| 422  | Validation error                  |

---

## Dev/Demo Mode

### `SKIP_AUTH` (Backend Only)

Set `SKIP_AUTH=true` in `backend/.env` to bypass token validation.

**Limitations:**
- Only returns the demo **doctor** user (`doctor@medorbit.demo`)
- Patient routes will return **403** in this mode
- Frontend still shows login UI — bypass is backend-only

**Recommended approach for testing:**
Use seeded demo accounts with real login instead of `SKIP_AUTH`.

### MVP Security Note

JWT is stored in `localStorage` for development speed. In production, this would move to `httpOnly` cookies or a server-side session strategy.

---

## Environment Variables

| Variable                     | Default                          |
|------------------------------|----------------------------------|
| `DATABASE_URL`               | `sqlite:///./medorbit.db`        |
| `SECRET_KEY`                 | (change in production)           |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| `1440` (24h)                     |
| `CORS_ORIGINS`               | `http://localhost:3000,...`       |
| `SKIP_AUTH`                  | `false`                          |
