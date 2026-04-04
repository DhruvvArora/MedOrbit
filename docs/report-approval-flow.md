# Doctor Approval & Report Persistence Flow

The defining safety mechanism in MedOrbit. No AI hallucination reaches a patient without passing this gate.

## 1. DRAFT State
- Set initially by the `Super Agent`. 
- Allows `PATCH /api/visits/{visit_id}/report` commands by the assigned doctor.
- Denies `GET` requests issued from Patient accounts.
- Mutable.

## 2. APPROVED State
- Triggered exclusively by the Doctor via `POST /api/visits/{visit_id}/report/approve`.
- Casts immutable flags across the Database tuple.
- Prevents subsequent `PATCH` writes.
- Prevents re-running orchestrator AI loops (Returns HTTP 409).
- Opens the API logic for Patient UI retrieval and backend Reminder Cron extraction asynchronously.
