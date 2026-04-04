# Reminder Architecture

This component breaks static JSON arrays parsed by the generative AI into tracked relational elements.

## Lifecycle
1. The **Super Agent** finishes its contextual string inference -> `["Take Pill A", "Rest 20m"]` mapped to `VisitReport.reminder_candidates`.
2. The **Supervising Doctor** reviews this Draft on their EMR terminal and patches any errant logic. They then submit an `APPROVAL` lock.
3. Automatically (or via the `POST /generate` hook), the backend strips those arrays and initiates distinct rows in the `Reminder` PostgreSQL table mapping to the identical `visit_id`.
4. The Patient Dashboard queries those independent rows mapping status UI checkboxes to the `PATCH /status` hooks.

## Notification Scope
MedOrbit delegates the actual Twilio/FCM logic to the `AbstractNotifierService`. This component simply provides the "Target Lists" that standard CRON workers query against.
