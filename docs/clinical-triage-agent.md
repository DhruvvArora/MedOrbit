# Clinical Triage Agent

## Purpose
The Clinical Triage Agent acts as an automated, highly-structured clinical scribe. It analyzes conversation transcripts and parses out fundamental intake components: Chief Complaints, specific Symptom maps, Risk Flags, and Drafted Follow-up suggestions.

It does **not** diagnose illness or define official treatment protocols.

## Integration / Endpoints
To invoke the triage service on demand:
**`POST /api/visits/{visit_id}/agents/clinical-triage/run`**
*(Requires 'doctor' role matching the assigned visit).*

## Output
The agent returns structured JSON containing matching arrays of `SymptomEvidence` linked back strictly to transcript quotas.
Fields included:
- `summary`
- `chief_complaint`
- `symptoms` 
- `medication_mentions`
- `history_mentions`
- `risk_flags`
- `follow_up_questions`
- `candidate_discharge_points`
- `cautionary_notes`

## Safety boundaries
The prompt relies on rigid behavioral controls requesting hedged phrasing (e.g. "Patient reports..."). It mandates tracking back all symptoms into factual text evidence and appending standard disclaimers.

## Pre-Computation & Mock Mode
If an `OPENAI_API_KEY` is not present within `.env`, the system executes completely offline using a robust mock JSON response tuned for "Hypertension" or standard demographic queries. This ensures stable UI testing and eliminates failure scenarios.
