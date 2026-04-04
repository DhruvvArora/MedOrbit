import logging

logger = logging.getLogger(__name__)

class AbstractNotifierService:
    """
    MVP Interface for Notification delivery.
    In the hackathon, we simply log delivery intents. This hooks directly into 
    SQS or Twilio queues when implemented gracefully.
    """
    @staticmethod
    def notify_patient_reminder_generated(patient_id: int, reminder_counter: int):
        print(f"[🔥 NOTIFIER MOCK] Sent Push Notification to User {patient_id}: 'You have {reminder_counter} new tasks generated from your recent doctor visit!'")

    @staticmethod
    def notify_patient_due_reminder(patient_id: int, title: str):
        print(f"[🔥 NOTIFIER MOCK] Sent SMS to User {patient_id}: 'Friendly reminder: {title}. Log it in MedOrbit today!'")
