# Behavioral Health Insight Agent

## Purpose
The Behavioral Insight Agent analyzes a transcript string from a consultation and identifies psychosocial themes, communication cues, and adherence risks. It strictly does **not** diagnose the patient, but generates drafted intelligence for the doctor's review.

## Inputs
It consumes `transcript.plaintext` which represents the sequence of dialogue correctly labeled with speaker tags `[Dr. Chen]:` and `[Patient]:`.

## Output 
The agent returns structured JSON containing arrays of `InsightEvidence` instances tied directly to quotes in the text.
Fields included:
- `summary`
- `emotional_signals`
- `adherence_risk`
- `psychosocial_factors`
- `communication_flags`
- `suggested_follow_up_questions`
- `cautionary_notes`

## Safety boundaries
The prompt strategy is strictly policed against prescribing treatments or assuming facts. It must include confidence markers on evidence items and always append the cautionary note: "AI inference only, verify clinically".

## Integration / Endpoints
To test during the hackathon:
**`POST /api/visits/{visit_id}/agents/behavioral/run`**
*(Requires 'doctor' role matching the assigned visit).*

## Mock Mode
If `OPENAI_API_KEY` is not loaded in `.env`, the system defaults to "Mock Mode" and will supply a safely filled mock payload matching our demo "Hypertension" scenario. This allows all backend integrations and frontend UI views to be tested totally offline without burning tokens.
