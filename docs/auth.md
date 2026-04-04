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
┌──────────┐      POST /api/auth/login       ┌──────────┐
│  Client   │ ─────────────────────────────▶ │  Server   │
│ (browser) │     { email, password }         │ (FastAPI) │
│           │ ◀───────────────────────────── │           │
│           │   { access_token, user }        │           │
└──────────┘                                  └──────────┘
      │
      │  GET /api/auth/me
      │  Authorization: Bearer <token>
      ▼
┌──────────┐
│  Server   │ → decode JWT → load user → return profile
└──────────┘
```

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

## Role-Based Access Control

Routes are protected using FastAPI dependencies:

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

## Environment Variables

| Variable                     | Default                          |
|------------------------------|----------------------------------|
| `DATABASE_URL`               | `sqlite:///./medorbit.db`        |
| `SECRET_KEY`                 | (change in production)           |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| `1440` (24h)                     |
| `CORS_ORIGINS`               | `http://localhost:3000,...`       |
