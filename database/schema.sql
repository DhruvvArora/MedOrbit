-- MedOrbit — Database Schema Reference
-- =====================================
-- This is a human-readable reference DDL.
-- The actual DB is managed by SQLAlchemy models + Alembic migrations.
-- This file exists for documentation purposes.

-- =============================================
-- Users Table
-- =============================================

CREATE TABLE IF NOT EXISTS users (
    id          VARCHAR(36)   PRIMARY KEY,
    full_name   VARCHAR(100)  NOT NULL,
    email       VARCHAR(255)  NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role        VARCHAR(20)   NOT NULL CHECK (role IN ('doctor', 'patient')),
    is_active   BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role  ON users(role);

-- =============================================
-- Visits Table
-- =============================================

CREATE TABLE IF NOT EXISTS visits (
    id          VARCHAR(36)   PRIMARY KEY,
    doctor_id   VARCHAR(36)   NOT NULL,
    patient_id  VARCHAR(36)   NOT NULL,
    type        VARCHAR(20)   NOT NULL CHECK (type IN ('virtual', 'in_person')),
    status      VARCHAR(20)   NOT NULL DEFAULT 'scheduled'
                              CHECK (status IN ('scheduled', 'active', 'completed', 'cancelled')),
    title       VARCHAR(255),
    started_at  TIMESTAMP,
    ended_at    TIMESTAMP,
    created_at  TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY(doctor_id) REFERENCES users(id),
    FOREIGN KEY(patient_id) REFERENCES users(id)
);

CREATE INDEX idx_visits_doctor_id  ON visits(doctor_id);
CREATE INDEX idx_visits_patient_id ON visits(patient_id);
CREATE INDEX idx_visits_status     ON visits(status);

-- =============================================
-- Transcript Chunks Table
-- =============================================
-- Core data artifact of the platform.
-- Each row = one utterance in a doctor-patient dialogue.
-- Ordered by sequence_number within a visit.
-- The full transcript is reconstructed by querying all chunks
-- for a visit_id, sorted by sequence_number ASC.

CREATE TABLE IF NOT EXISTS transcript_chunks (
    id              VARCHAR(36)   PRIMARY KEY,
    visit_id        VARCHAR(36)   NOT NULL,
    sequence_number INTEGER       NOT NULL,
    speaker_role    VARCHAR(20)   NOT NULL
                    CHECK (speaker_role IN ('doctor', 'patient', 'system')),
    speaker_label   VARCHAR(100),
    text            TEXT          NOT NULL,
    source_type     VARCHAR(20)   NOT NULL DEFAULT 'manual'
                    CHECK (source_type IN ('manual', 'transcribed', 'simulated')),
    created_at      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(visit_id) REFERENCES visits(id) ON DELETE CASCADE,
    UNIQUE(visit_id, sequence_number)
);

-- Primary access pattern: get all chunks for a visit, ordered
CREATE INDEX idx_tc_visit_id  ON transcript_chunks(visit_id);
CREATE INDEX idx_tc_visit_seq ON transcript_chunks(visit_id, sequence_number);

-- =============================================
-- Future tables (will be added in later modules)
-- =============================================
--
-- agent_outputs   — visit_id FK → visits.id
--   Stores structured output from behavioral/clinical agents.
--
-- final_reports   — visit_id FK → visits.id
--   Doctor-reviewed clinical summaries derived from agent outputs.
--
-- reminders       — visit_id FK → visits.id, patient_id FK → users.id
--   Action items and follow-up reminders for patients.
