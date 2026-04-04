# MedOrbit — Visit Management Reference

## Overview

The `visit` entity represents the core consultation session linking a Doctor and a Patient. It establishes the anchor ID for all future features (transcripts, AI outputs, reports).

## Data Model

- `type`: `virtual` or `in_person`. Dictates frontend UI logic (e.g., showing a video join button vs just an active session panel).
- `status`: `scheduled`, `active`, `completed`, or `cancelled`. The backend enforces valid state transitions.

---

## Visit Lifecycle

```
[ Scheduled ]
      │
      ├──────(Doctor cancels)──────▶ [ Cancelled ]
      │
 (Doctor starts)
      │
      ▼
  [ Active ] ◄── (Ingest Transcripts Allowed Here)
      │
 (Doctor completes)
      │
      ▼
 [ Completed ] ◄── (AI Report Generation Triggered Here)
```

## Access Rules (RBAC)

- **Create**: Only Doctors. Patient ID must be supplied.
- **View Lists**: Doctors only see their patients' visits. Patients only see their own.
- **View Detail**: Both Doctor and Patient can view a visit, but *only* if they are directly assigned to it via `doctor_id` or `patient_id`.
- **Change Status**: Only the assigned Doctor can mutate status (`start`, `complete`, `cancel`).

---

## API Endpoints

Make sure to include `Authorization: Bearer <TOKEN>` on all requests.

### 1. Create a Visit

```bash
curl -X POST http://localhost:8000/api/visits \
  -H "Authorization: Bearer <YOUR_DOCTOR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "<PATIENT_ID>",
    "type": "virtual",
    "title": "Routine Checkup"
  }'
```

### 2. List Visits

```bash
# Get all
curl http://localhost:8000/api/visits \
  -H "Authorization: Bearer <YOUR_TOKEN>"

# Filter by status
curl http://localhost:8000/api/visits?status=scheduled \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

### 3. Get Specific Visit

```bash
curl http://localhost:8000/api/visits/<VISIT_ID> \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

### 4. Lifecycle Actions (Doctor Only)

```bash
# Start Visit
curl -X POST http://localhost:8000/api/visits/<VISIT_ID>/start \
  -H "Authorization: Bearer <YOUR_DOCTOR_TOKEN>"

# Complete Visit
curl -X POST http://localhost:8000/api/visits/<VISIT_ID>/complete \
  -H "Authorization: Bearer <YOUR_DOCTOR_TOKEN>"

# Cancel Visit
curl -X POST http://localhost:8000/api/visits/<VISIT_ID>/cancel \
  -H "Authorization: Bearer <YOUR_DOCTOR_TOKEN>"
```

---

## Demo Instructions

1. Ensure the base users exist: `python database/seed.py`
2. Run the visits seeder: `python database/seed_visits.py`
3. This creates **4 sample visits** between `doctor@medorbit.demo` and `patient@medorbit.demo`:
   - 1 Scheduled (`virtual`)
   - 1 Active (`in_person`)
   - 1 Completed (`virtual`)
   - 1 Cancelled (`in_person`)
