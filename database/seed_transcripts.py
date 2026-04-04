"""
MedOrbit — Transcript Seed Script

Injects realistic medical dialogue into existing demo visits.
Requires seed.py (users) and seed_visits.py (visits) to have run first.

Idempotent — safe to run multiple times (skips visits that already have chunks).

Usage:
    cd backend
    python ../database/seed_transcripts.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.core.database import SessionLocal, engine
from app.models import Base, User, Visit, TranscriptChunk

# ── Realistic Medical Dialogues ──────────────────────────────

KNEE_PAIN_DIALOGUE = [
    ("doctor", "Dr. Sarah Chen", "Good afternoon, Alex. How are you doing today?"),
    ("patient", "Alex Johnson", "Hi Doctor. I've been having this pain in my right knee for about two weeks now."),
    ("doctor", "Dr. Sarah Chen", "I see. Can you describe the pain? Is it sharp, dull, or more of an ache?"),
    ("patient", "Alex Johnson", "It's mostly a dull ache, but it gets sharp when I go up or down stairs."),
    ("doctor", "Dr. Sarah Chen", "Has anything changed recently? New exercise routine, any falls or injuries?"),
    ("patient", "Alex Johnson", "I started jogging again about three weeks ago after not exercising for a long time."),
    ("doctor", "Dr. Sarah Chen", "That could be a contributing factor. Any swelling you've noticed?"),
    ("patient", "Alex Johnson", "A little bit, yeah. In the evening it gets slightly puffy."),
    ("doctor", "Dr. Sarah Chen", "On a scale of 1 to 10, how would you rate the pain at its worst?"),
    ("patient", "Alex Johnson", "I'd say about a 6, maybe 7 when climbing stairs."),
    ("doctor", "Dr. Sarah Chen", "Are you taking anything for the pain currently?"),
    ("patient", "Alex Johnson", "Just some ibuprofen. It helps a bit but wears off quickly."),
    ("doctor", "Dr. Sarah Chen", "How often are you taking the ibuprofen?"),
    ("patient", "Alex Johnson", "Twice a day, morning and evening. Sometimes three times."),
    ("doctor", "Dr. Sarah Chen", "Any other medical conditions I should be aware of? Diabetes, heart issues?"),
    ("patient", "Alex Johnson", "No, nothing major. I had my blood pressure checked last month and it was a little high, 140 over 90."),
    ("doctor", "Dr. Sarah Chen", "That's borderline. We should keep an eye on that. Have you been under a lot of stress lately?"),
    ("patient", "Alex Johnson", "Yeah, work has been really stressful. I haven't been sleeping well either. Maybe 4 to 5 hours a night."),
    ("doctor", "Dr. Sarah Chen", "Sleep deprivation can definitely affect your blood pressure and overall recovery. Let me examine your knee now and we'll discuss a plan."),
    ("patient", "Alex Johnson", "Sure, that sounds good. I'm just worried it might be something serious."),
    ("doctor", "Dr. Sarah Chen", "Based on what you've described, it sounds like it may be runner's knee, which is very common when resuming exercise. But let's do a thorough exam to rule out anything else."),
]

HYPERTENSION_DIALOGUE = [
    ("doctor", "Dr. Sarah Chen", "Hello Alex, welcome. This is our initial intake consultation. How can I help you today?"),
    ("patient", "Alex Johnson", "Hi Doctor. My family doctor referred me because my blood pressure has been consistently high over the past few months."),
    ("doctor", "Dr. Sarah Chen", "I see. Do you know what your recent readings have been?"),
    ("patient", "Alex Johnson", "The last three were around 145 over 95, 150 over 92, and 140 over 90."),
    ("doctor", "Dr. Sarah Chen", "Those readings are in the Stage 1 hypertension range. Let's go over your history. Any family history of heart disease or high blood pressure?"),
    ("patient", "Alex Johnson", "My father had a heart attack at 58. My mother takes blood pressure medication."),
    ("doctor", "Dr. Sarah Chen", "That's important to note. What about your diet? Walk me through a typical day of eating."),
    ("patient", "Alex Johnson", "I usually skip breakfast, grab fast food for lunch, and my wife makes dinner. We eat out maybe twice a week."),
    ("doctor", "Dr. Sarah Chen", "How about salt intake? Do you add salt to your food?"),
    ("patient", "Alex Johnson", "I probably add more than I should. I like things well-seasoned."),
    ("doctor", "Dr. Sarah Chen", "Exercise? Physical activity?"),
    ("patient", "Alex Johnson", "Not much recently. I sit at a desk most of the day. I was trying to start jogging but my knee started hurting."),
    ("doctor", "Dr. Sarah Chen", "Do you drink alcohol or smoke?"),
    ("patient", "Alex Johnson", "I have a beer or two most evenings. I quit smoking three years ago."),
    ("doctor", "Dr. Sarah Chen", "Good that you quit smoking, that's a big positive. How about stress and sleep? Tell me about your typical day."),
    ("patient", "Alex Johnson", "Work is very stressful. I manage a team and the deadlines are constant. I usually get to bed around midnight and wake at 5. Maybe 5 hours of sleep on a good night."),
    ("doctor", "Dr. Sarah Chen", "That sleep pattern is concerning. Chronic sleep deprivation is a significant risk factor for hypertension. Do you feel anxious or worried often?"),
    ("patient", "Alex Johnson", "Honestly, yes. I've been feeling pretty overwhelmed lately. Sometimes I get these tension headaches and my chest feels tight."),
    ("doctor", "Dr. Sarah Chen", "Have you spoken to anyone about the anxiety? A counselor or therapist?"),
    ("patient", "Alex Johnson", "No, I've been meaning to but never got around to it. I keep thinking I should handle it on my own."),
    ("doctor", "Dr. Sarah Chen", "There's no shame in getting help. Stress management is a critical part of blood pressure control. I'm going to recommend some lifestyle modifications and we'll discuss whether medication is needed after we review your labs."),
    ("patient", "Alex Johnson", "What kind of lifestyle changes are you thinking?"),
    ("doctor", "Dr. Sarah Chen", "First, reducing sodium intake to under 2300 mg per day. Second, incorporating at least 30 minutes of moderate exercise most days — we'll work around your knee. Third, improving sleep hygiene. And I'd like you to consider speaking with a counselor."),
    ("patient", "Alex Johnson", "That sounds like a lot of changes at once."),
    ("doctor", "Dr. Sarah Chen", "We can take it step by step. Small consistent changes compound over time. I'll create a care plan with specific, actionable steps and we'll follow up in two weeks."),
]

# Short in-person follow-up — for the "scheduled" visit scenario
# (demonstrates what a future visit transcript might look like)
FOLLOWUP_DIALOGUE = [
    ("system", "System", "Virtual consultation session started."),
    ("doctor", "Dr. Sarah Chen", "Good morning, Alex. This is our two-week follow-up. How's the knee doing?"),
    ("patient", "Alex Johnson", "Actually, it's been much better. I've been resting it and doing the stretches you suggested."),
    ("doctor", "Dr. Sarah Chen", "That's great to hear. And how about the blood pressure? Have you been checking it at home?"),
    ("patient", "Alex Johnson", "Yes, the readings have been around 135 over 88. Still a bit high but trending down."),
    ("doctor", "Dr. Sarah Chen", "Good progress. Have you been reducing the salt intake like we discussed?"),
    ("patient", "Alex Johnson", "I have. My wife has been helping with meal prep. Less eating out too."),
    ("doctor", "Dr. Sarah Chen", "Excellent. And sleep? How many hours are you getting now?"),
    ("patient", "Alex Johnson", "I'm up to about 6 hours. Still not great, but better than before."),
    ("doctor", "Dr. Sarah Chen", "That's a meaningful improvement. Let's keep building on it. I'd like to see you again in a month, and we'll decide about medication then based on how the numbers look."),
    ("patient", "Alex Johnson", "Sounds good, Doctor. Thanks for following up."),
    ("system", "System", "Virtual consultation session ended."),
]


def _seed_dialogue(db, visit, dialogue, source_type="simulated"):
    """Seed a single dialogue into a visit, skipping if chunks already exist."""
    existing = (
        db.query(TranscriptChunk)
        .filter(TranscriptChunk.visit_id == visit.id)
        .count()
    )
    if existing > 0:
        print(f"  ⏭  Skipped '{visit.title}' (already has {existing} chunks)")
        return 0

    for i, (role, label, text) in enumerate(dialogue, start=1):
        chunk = TranscriptChunk(
            visit_id=visit.id,
            sequence_number=i,
            speaker_role=role,
            speaker_label=label,
            text=text,
            source_type=source_type,
        )
        db.add(chunk)

    count = len(dialogue)
    print(f"  ✅ Seeded {count} chunks into '{visit.title}'")
    return count


def seed_transcripts():
    """Insert transcript chunks into demo visits."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Find visits by status and title pattern
        active_visit = (
            db.query(Visit)
            .filter(Visit.status == "active", Visit.title.like("%Knee%"))
            .first()
        )
        completed_visit = (
            db.query(Visit)
            .filter(Visit.status == "completed", Visit.title.like("%Initial%"))
            .first()
        )
        scheduled_visit = (
            db.query(Visit)
            .filter(Visit.status == "scheduled", Visit.title.like("%Routine%"))
            .first()
        )

        total_seeded = 0

        # Active visit: Knee pain dialogue (in-progress consultation)
        if active_visit:
            total_seeded += _seed_dialogue(db, active_visit, KNEE_PAIN_DIALOGUE)
        else:
            print("  ⚠️  No active 'Knee Pain' visit found — skipping")

        # Completed visit: Full hypertension intake
        if completed_visit:
            total_seeded += _seed_dialogue(db, completed_visit, HYPERTENSION_DIALOGUE)
        else:
            print("  ⚠️  No completed 'Initial intake' visit found — skipping")

        # Scheduled visit: Left intentionally empty for demo purposes
        # This shows what a visit looks like BEFORE transcript ingestion.
        if scheduled_visit:
            print(f"  📋 Scheduled visit '{scheduled_visit.title}' left with no transcript (demo: empty state)")
        else:
            print("  ⚠️  No scheduled visit found — skipping")

        db.commit()
        print(f"\n🎉 Transcript seed complete: {total_seeded} total chunks created.")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seeding MedOrbit demo transcripts...\n")
    seed_transcripts()
