# MedOrbit — Transcript Ingestion Reference

## Overview

The transcript is the **core data artifact** of every consultation. It feeds the AI agents and ultimately generates the doctor-reviewed clinical report and patient discharge summary.

Transcripts are stored as **ordered chunks** (one row per utterance) tied to a `visit_id`.

---

## Data Model

Each chunk contains:
- `speaker_role`: `doctor`, `patient`, or `system`
- `speaker_label`: Human-readable name (e.g., "Dr. Chen")
- `text`: The actual utterance
- `sequence_number`: Ordering guarantee
- `source_type`: `manual`, `transcribed`, or `simulated`

---

## Ingestion Rules

1. Transcripts can **only be written** to a visit with `status == 'active'`.
2. Only the **assigned doctor** can write transcript chunks.
3. If `sequence_number` is omitted, it is auto-assigned as `max + 1`.
4. Transcripts are **immutable** in the MVP — no edits or deletions.

---

## API Endpoints

All endpoints are prefixed with `/api/visits/{visit_id}/transcripts`.

### 1. Add Single Chunk

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

### 2. Bulk Ingest (Hackathon Demo)

```bash
curl -X POST http://localhost:8000/api/visits/<VISIT_ID>/transcripts/bulk \
  -H "Authorization: Bearer <DOCTOR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "chunks": [
      { "speaker_role": "doctor", "speaker_label": "Dr. Chen", "text": "How are you?" },
      { "speaker_role": "patient", "speaker_label": "Alex Johnson", "text": "I have knee pain." }
    ]
  }'
```

### 3. Get Chunks (Ordered)

```bash
curl http://localhost:8000/api/visits/<VISIT_ID>/transcripts/chunks \
  -H "Authorization: Bearer <TOKEN>"
```

### 4. Get Plaintext (For AI Agents)

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

## How AI Agents Consume Transcripts

1. Agent receives a `visit_id` after visit completion.
2. Agent calls `GET /plaintext` (or uses the service layer directly).
3. Agent gets a clean `[Speaker]: Text` formatted string.
4. Agent processes the text and produces structured output.

The `agents/shared/transcript_types.py` provides a decoupled `TranscriptInput` dataclass that agents can import without depending on FastAPI internals.

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
