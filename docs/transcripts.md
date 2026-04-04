# MedOrbit — Transcript Ingestion + Storage Pipeline

## Overview

The transcript is the **core data artifact** of every consultation. It feeds the AI agents and ultimately generates the doctor-reviewed clinical report and patient discharge summary.

Transcripts are stored as **ordered chunks** (one row per utterance) tied to a `visit_id`.

---

## Architecture

```
Doctor/Patient ──→ REST API ──→ Transcript Service ──→ Database
                                      ↓
                              Agent Adapter Layer
                                      ↓
                         Behavioral / Clinical Agents
```

The pipeline is **chunk-based**, not blob-based. Each utterance is a separate row, enabling:
- Per-speaker filtering and analysis
- Ordered playback and display
- Metadata per utterance (source, role, timestamp)
- Future integration with real-time STT chunk streams

---

## Data Model

### TranscriptChunk

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | VARCHAR(36) | PK, UUID | Unique chunk identifier |
| `visit_id` | VARCHAR(36) | FK → visits.id, NOT NULL | Owning visit |
| `sequence_number` | INTEGER | NOT NULL, UNIQUE(visit_id, seq) | Ordering guarantee |
| `speaker_role` | VARCHAR(20) | NOT NULL, CHECK | `doctor`, `patient`, or `system` |
| `speaker_label` | VARCHAR(100) | nullable | Human name, e.g. "Dr. Chen" |
| `text` | TEXT | NOT NULL | The actual utterance |
| `source_type` | VARCHAR(20) | NOT NULL, CHECK | `manual`, `transcribed`, or `simulated` |
| `created_at` | TIMESTAMP | NOT NULL | Row creation time |

### Key Constraints
- **UNIQUE(visit_id, sequence_number)**: No two chunks in the same visit can share a sequence number.
- **CHECK(speaker_role)**: Must be one of the allowed values.
- **CHECK(source_type)**: Must be one of the allowed values.
- **ON DELETE CASCADE**: Deleting a visit removes all its transcript chunks.

---

## Ingestion Rules

1. Transcripts can **only be written** to a visit with `status == 'active'`.
2. Only the **assigned doctor** can write transcript chunks.
3. If `sequence_number` is omitted, it is auto-assigned as `max + 1`.
4. Transcripts are **immutable** in the MVP — no edits or deletions.
5. Text is **whitespace-normalized** before storage (leading/trailing stripped).
6. Empty text (after normalization) is **rejected** with 422.
7. Duplicate sequence numbers are **rejected** with 409.
8. Bulk insert is **all-or-nothing** — if any chunk fails, none are saved.

---

## API Endpoints

All endpoints are prefixed with `/api/visits/{visit_id}/transcripts`.

### 1. Add Single Chunk

**`POST /chunks`** — Append one utterance.

```bash
curl -X POST http://localhost:8000/api/visits/<VISIT_ID>/transcripts/chunks \
  -H "Authorization: Bearer <DOCTOR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "speaker_role": "doctor",
    "speaker_label": "Dr. Chen",
    "text": "How are you feeling today?",
    "source_type": "manual"
  }'
```

**Response (201):**
```json
{
  "id": "uuid",
  "visit_id": "visit-uuid",
  "sequence_number": 1,
  "speaker_role": "doctor",
  "speaker_label": "Dr. Chen",
  "text": "How are you feeling today?",
  "source_type": "manual",
  "created_at": "2026-04-04T12:00:00Z"
}
```

**Errors:**
| Code | Reason |
|------|--------|
| 400 | Visit is not in 'active' status |
| 403 | Not the assigned doctor |
| 409 | Sequence number already exists |
| 422 | Empty text or invalid payload |

---

### 2. Bulk Ingest (Hackathon Demo)

**`POST /bulk`** — Ingest multiple chunks at once.

```bash
curl -X POST http://localhost:8000/api/visits/<VISIT_ID>/transcripts/bulk \
  -H "Authorization: Bearer <DOCTOR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "chunks": [
      {
        "speaker_role": "doctor",
        "speaker_label": "Dr. Chen",
        "text": "How are you?"
      },
      {
        "speaker_role": "patient",
        "speaker_label": "Alex Johnson",
        "text": "I have knee pain."
      }
    ]
  }'
```

**Response (201):**
```json
{
  "visit_id": "visit-uuid",
  "chunks_created": 2,
  "chunks": [ ... ]
}
```

---

### 3. Get Chunks (Ordered)

**`GET /chunks`** — Retrieve all chunks, sorted by sequence_number.

```bash
curl http://localhost:8000/api/visits/<VISIT_ID>/transcripts/chunks \
  -H "Authorization: Bearer <TOKEN>"
```

**Auth:** Both doctor and patient participants.

---

### 4. Get Plaintext (For AI Agents)

**`GET /plaintext`** — Get the entire transcript as a single formatted string.

```bash
curl http://localhost:8000/api/visits/<VISIT_ID>/transcripts/plaintext \
  -H "Authorization: Bearer <TOKEN>"
```

**Response:**
```json
{
  "visit_id": "...",
  "text": "[Dr. Chen]: How are you?\n[Alex Johnson]: I have knee pain.",
  "chunk_count": 2
}
```

---

### 5. Get Statistics

**`GET /stats`** — Get metadata about the transcript.

```bash
curl http://localhost:8000/api/visits/<VISIT_ID>/transcripts/stats \
  -H "Authorization: Bearer <TOKEN>"
```

**Response:**
```json
{
  "visit_id": "...",
  "total_chunks": 21,
  "speaker_breakdown": { "doctor": 11, "patient": 10 },
  "source_breakdown": { "simulated": 21 },
  "first_chunk_at": "2026-04-04T12:00:00+00:00",
  "last_chunk_at": "2026-04-04T12:10:00+00:00",
  "total_characters": 3842
}
```

---

## RBAC Rules

| Action | Who can do it | Dependency |
|--------|--------------|------------|
| Write transcript (POST) | Assigned doctor only | `require_assigned_doctor` |
| Read transcript (GET) | Doctor OR patient of the visit | `require_visit_participant` |
| Internal agent access | Service layer (no HTTP auth) | `get_transcript_for_agent()` |

---

## How AI Agents Consume Transcripts

### Via HTTP (External Agents)
1. Agent receives a `visit_id` after visit completion.
2. Agent calls `GET /plaintext` (or `/chunks`) with a service account token.
3. Agent gets a clean `[Speaker]: Text` formatted string.
4. Agent processes the text and produces structured output.

### Via Service Layer (Internal Agents)
```python
from agents.shared.transcript_adapter import load_transcript_for_visit

transcript = load_transcript_for_visit("visit-uuid")
print(transcript.plaintext)
print(transcript.chunk_count)

# Filtered access
for u in transcript.doctor_utterances:
    print(f"Doctor said: {u.text}")
```

### Shared Contract
The `agents/shared/transcript_types.py` provides a decoupled `TranscriptInput` dataclass:
- `visit_id`: The visit identifier.
- `utterances`: List of `Utterance` objects.
- `.plaintext`: Formatted string property.
- `.doctor_utterances` / `.patient_utterances`: Filtered views.
- `.to_dict()`: JSON-serializable output.

---

## Integration Contract for Future Modules

| Module | How it uses transcripts |
|--------|----------------------|
| **Behavioral Agent** | Reads ordered chunks, analyzes sentiment, speaker ratios, flags |
| **Clinical Triage Agent** | Consumes plaintext, extracts medical entities and symptoms |
| **Super Agent** | Aggregates transcript + agent outputs for final report |
| **Reports** | References transcript-derived summaries (not raw chunks) |
| **Simplifier Chat** | Uses approved report content only, NOT raw transcript |

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| Chunk added to nonexistent visit | 404 from `get_visit_or_404` |
| Unauthorized user reads transcript | 403 from `require_visit_participant` |
| Unauthorized user writes transcript | 403 from `require_assigned_doctor` |
| Write to completed/cancelled visit | 400 `VisitNotActiveError` |
| Duplicate sequence number | 409 `DuplicateSequenceError` |
| Empty text after stripping | 422 `EmptyTranscriptError` |
| Visit with no transcript | Returns empty array / empty string / zero stats |
| Missing speaker_label | Defaults to capitalized speaker_role ("Doctor") |
| Malformed bulk payload | 422 Pydantic validation error |
| Very large transcript (500+ chunks) | Bulk limit enforced via Pydantic max_length |

---

## Demo Setup

```bash
cd backend

# 1. Seed users (if not done)
python ../database/seed.py

# 2. Seed visits (if not done)
python ../database/seed_visits.py

# 3. Seed transcripts
python ../database/seed_transcripts.py
```

This creates:
- **21 chunks** in the Active visit (knee pain dialogue)
- **25 chunks** in the Completed visit (hypertension intake)
- **0 chunks** in the Scheduled visit (intentionally empty for demo)

---

## Supported Source Types

| Type | When to use |
|------|------------|
| `manual` | Doctor typing transcript directly during or after visit |
| `simulated` | Hackathon demo / seed data / test fixtures |
| `transcribed` | Output from future speech-to-text integration |
