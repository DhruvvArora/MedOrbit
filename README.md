# MedOrbit

> **AI-Assisted Clinical & Behavioral Intelligence**

MedOrbit is an AI-powered healthcare platform that transforms doctor–patient conversations into structured clinical intelligence. It captures consultation context, analyzes behavioral and clinical signals, and generates draft insights, summaries, and care guidance — all reviewed and approved by the doctor before anything reaches the patient.

---

## Table of Contents

- [Overview](#overview)
- [Problem](#problem)
- [Solution](#solution)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Design Principles](#design-principles)
- [MVP Scope](#mvp-scope)
- [Current Limitations](#current-limitations)
- [Future Improvements](#future-improvements)
- [Contributors](#contributors)
- [License](#license)

---

## Overview

Healthcare conversations often contain valuable clinical and behavioral context that goes unstructured and underused. MedOrbit listens to consultations, extracts meaningful information, and organizes it into doctor-friendly outputs.

The platform is built around a **doctor-in-the-loop** workflow. AI handles analysis and draft generation, but the doctor retains full control over review, approval, and final communication.

---

## Problem

During a consultation, doctors must simultaneously listen, reason, document, and plan next steps. This makes it easy to miss emotional, behavioral, or lifestyle-related cues buried in the conversation.

Patients, meanwhile, often leave visits without a clear understanding of what was discussed or what actions to take next.

---

## Solution

MedOrbit bridges this gap by:

- Capturing consultation conversations
- Generating a live transcript
- Running AI analysis in the background
- Producing draft clinical and behavioral insights
- Letting doctors review and approve outputs before sharing
- Delivering only approved, patient-safe information to patients

---

## Key Features

### 1. AI-Assisted Consultation Capture
- Launch consultations from an interactive landing experience
- Capture conversation data during the doctor–patient interaction
- Build a foundation for real-time structured analysis

### 2. Live Transcript Generation
- Generate a running transcript of the consultation
- Feed transcript chunks into downstream AI analysis
- Keep the MVP focused without requiring full speaker diarization

### 3. Multi-Agent Intelligence

MedOrbit uses a multi-agent setup to analyze consultation content:

| Agent | Role |
|---|---|
| **Behavioral Agent** | Identifies emotional, behavioral, and psychological signals in the conversation |
| **Triage Agent** | Extracts symptoms, concerns, risk indicators, and clinically relevant observations |
| **Super Agent / Orchestrator** | Combines outputs from multiple agents into a structured summary for doctor review |

### 4. Doctor Review Workflow
- AI generates draft reports and insights
- Doctors review, edit, and approve outputs
- Only doctor-approved content is surfaced to patients

### 5. Doctor Dashboard
- Consultation workspace
- Transcript view
- AI-generated analysis panels
- Review and approval actions

### 6. Patient Dashboard
- View approved summaries and care guidance
- Read simplified explanations of the visit
- Access personalized recommendations and reminders

### 7. Smart Care Reminders
- Medication reminders
- Lifestyle and habit suggestions
- Follow-up tracking

---

## How It Works

### Doctor Flow

```
1. Log into the platform
2. Start a consultation
3. Transcript begins generating
4. AI agents analyze the conversation in the background
5. Draft report and care insights are produced
6. Doctor reviews and approves the final output
```

### Patient Flow

```
1. Log into the platform
2. View only doctor-approved outputs
3. Read simplified summary and guidance
4. Follow reminders and recommendations
```

---

## System Architecture

```
Frontend
├── Landing Page
├── Doctor Dashboard
├── Consultation Workspace
└── Patient Dashboard

Backend
├── Authentication
├── Consultation / Visit Management
├── Transcript Processing
├── Agent Orchestration
├── Report Generation
└── Reminder Logic

Agents
├── Behavioral Agent
├── Triage Agent
└── Super Agent

Database
└── Users, visits, reports, reminders, and metadata
```

---

## Project Structure

```
MedOrbit/
├── frontend/      # UI, dashboards, landing page, interaction flows
├── backend/       # APIs, orchestration, business logic
├── agents/        # AI agent implementations
├── database/      # Schema, setup, and persistence logic
├── docs/          # Supporting project documentation
└── README.md
```

---

## Tech Stack

### Frontend
- React
- Vite
- TypeScript
- CSS / component styling

### Backend
- FastAPI
- Python

### Database
- PostgreSQL

### AI / Intelligence Layer
- Multi-agent orchestration
- Behavioral analysis
- Triage reasoning
- Structured report generation

### Authentication / Storage
- Role-based auth for doctor and patient flows
- Cloud/local storage for reports and data

---

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd MedOrbit
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## Environment Variables

Create a `.env` file in the `backend/` directory and populate the following:

```env
DATABASE_URL=
SECRET_KEY=
AUTH_PROVIDER_CONFIG=
STORAGE_CONFIG=
```

Add any additional variables required by your implementation.

---

## Design Principles

| Principle | Description |
|---|---|
| **Doctor-in-the-loop** | AI supports decision-making but does not replace clinical judgment |
| **Safety-first communication** | Patients only see information approved by a doctor |
| **Usable intelligence** | Outputs are structured, actionable, and easy to review |
| **Human-centered design** | Reduces cognitive load rather than adding friction |
| **Hackathon-friendly reliability** | MVP focuses on a stable, impressive end-to-end flow |

---

## MVP Scope

- Consultation transcript capture
- AI-generated behavioral and clinical insight drafts
- Doctor review and approval workflow
- Patient-facing approved report view
- Reminder and guidance delivery

---

## Current Limitations

- Real-time speaker diarization is not fully implemented
- Live video/audio analysis is simplified in the MVP
- Transcript accuracy depends on input quality
- AI outputs are draft-level and require doctor review before use
- Notification/reminder workflows may be basic in the initial version

---

## Future Improvements

- Real-time speech-to-text integration
- Speaker separation for doctor vs. patient
- Live virtual consultation analysis
- Improved behavioral signal modeling
- Multilingual patient summaries
- Reminder notifications via email, SMS, and push
- Doctor analytics and longitudinal patient insights

---

## Why MedOrbit Matters

MedOrbit is not just a transcription tool. It converts raw medical conversations into structured, actionable intelligence while keeping doctors firmly in control. The goal is to improve documentation quality, reduce missed context, and make follow-up guidance clearer and more accessible for patients.

---

## Contributors

- **Dhruv Arora**
- **Pushkraj Kohok**

---

## License

```
MIT License
```

---

*MedOrbit represents a practical step toward more intelligent, human-centered clinical workflows — where AI helps organize and surface what matters, and doctors remain the final decision-makers.*
