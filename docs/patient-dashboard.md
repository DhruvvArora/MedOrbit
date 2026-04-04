# Patient Dashboard Read Flow

The critical boundary endpoint guaranteeing that patients never inspect raw AI transcript hallucinations before they are officially vetted by the presiding physician.

## Structure

All endpoints under `/api/patient/` operate as highly restricted DTO filters. They load the `VisitReport`, inspect the `status` flag, and either dynamically scrub or hard-reject non-`APPROVED` responses.

## Key APIs
- **`GET /api/patient/visits`**: Returns all visits attached to `current_user`. The boolean flag `has_approved_report` tells the frontend whether or not the chart notes should unveil. Pydantic `PatientVisitDetailResponse` entirely excludes internal medical tokens.
- **`GET /api/patient/reminders`**: Consolidates `reminder_candidates` across the Approved status filter across all historical charts, surfacing a simple To-Do array for checklist GUIs.

## Frontend Interfacing
The actual UI consumes these cleanly with out-of-the-box React mappings configured under `frontend/src/pages/PatientDashboard/Dashboard.tsx`.
