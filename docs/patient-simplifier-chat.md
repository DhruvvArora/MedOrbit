# Patient Simplifier API

Safeguarded LLM Chat explicitly wired to `VisitReport` artifacts.

## Usage
`POST /api/patient/visits/{visit_id}/explain-chat`
```json
{
  "message": "When should I take this medication again?"
}
```

## Security
1. Request must match the authorized Patient's JWT Context.
2. The `VisitReport` is loaded, halting securely if `APPROVED` boolean is false.
3. Only the `simplified_explanation`, `patient_discharge_draft`, and `reminder_candidates` strings are passed to the `agents.patient_simplifier.agent`.
4. It ignores conversation history. Multi-turn memory was actively discarded for the MVP to prevent "Context Poisoning" logic loop hallucination architectures.
