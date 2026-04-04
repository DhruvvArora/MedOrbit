# Super Agent / Orchestration

The Orchestration layer consumes both the `BehavioralInsightAgent` output and the `TriageInsightAgent` output alongside the raw transcript to execute the "Super Agent" prompt.

## Flow
1. Fetch Transcript for `visit_id`.
2. Extract purely objective metadata (Triage).
3. Extract purely psychosocial metadata (Behavioral).
4. Run Super Agent System Prompt merging both constraint streams against raw audio.
5. Create structured EMR chart (`SuperAgentDraftOutput`).

## Endpoints
`POST /api/visits/{visit_id}/orchestration/run`
- Returns the complete mapping and actively dumps it straight into the PostgreSQL `visit_reports` chart.
