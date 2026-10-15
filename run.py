"""
FocusFlow Entry Point
"""

import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.models import db

app = create_app(os.environ.get("FLASK_ENV", "development"))

# Auto-create tables on startup (works for Render, Railway, etc.)
with app.app_context():
    db.create_all()


@app.cli.command("init-db")
def init_db():
    """Create database tables."""
    with app.app_context():
        db.create_all()
        print("[OK] Database tables created.")


@app.cli.command("seed-db")
def seed_db():
    """Seed the database with sample demo data."""
    from app.models import User, Subject, Task, StudySession, AcademicEvent, Goal
    from datetime import date, datetime, timedelta, timezone
    import random

    with app.app_context():
        db.create_all()

        # Check if demo user already exists
        if User.query.filter_by(username="demo").first():
            print("Demo user already exists. Skipping seed.")
            return

        # Create demo user
        user = User(
            username="demo",
            email="demo@focusflow.app",
            full_name="Alex Johnson",
        )
        user.set_password("demo1234")
        db.session.add(user)
        db.session.flush()

        # Create goal
        goal = Goal(
            user_id=user.id,
            daily_study_goal_minutes=120,
            weekly_study_goal_minutes=600,
            daily_task_goal=4,
        )
        db.session.add(goal)

        # Subjects
        subjects_data = [
            ("Data Structures", "#6366f1", "Fall 2024"),
            ("Algorithms", "#f59e0b", "Fall 2024"),
            ("Web Development", "#10b981", "Fall 2024"),
            ("Database Systems", "#3b82f6", "Fall 2024"),
            ("Operating Systems", "#ec4899", "Fall 2024"),
        ]
        subjects = []
        for name, color, sem in subjects_data:
            s = Subject(user_id=user.id, name=name, color=color, semester=sem)
            db.session.add(s)
            subjects.append(s)
        db.session.flush()

        # Tasks
        today = date.today()
        tasks_data = [
            ("Complete Binary Tree implementation", subjects[0], "high", "in_progress", today + timedelta(days=2), 90),
            ("Solve 5 LeetCode problems", subjects[1], "medium", "pending", today + timedelta(days=3), 120),
            ("Build REST API for login", subjects[2], "high", "pending", today + timedelta(days=1), 180),
            ("ER diagram for library system", subjects[3], "medium", "completed", today - timedelta(days=1), 60),
            ("Read Chapter 4 – Scheduling", subjects[4], "low", "pending", today + timedelta(days=5), 45),
            ("Quiz on Sorting Algorithms", subjects[1], "high", "pending", today, 30),
            ("CSS Flexbox assignment", subjects[2], "low", "completed", today - timedelta(days=2), 60),
            ("Lab report – Page Replacement", subjects[4], "medium", "pending", today + timedelta(days=4), 90),
        ]
        for title, subj, priority, status, due_date, est in tasks_data:
            t = Task(
                user_id=user.id,
                subject_id=subj.id,
                title=title,
                priority=priority,
                status=status,
                due_date=due_date,
                estimated_minutes=est,
                completed_at=datetime.now(timezone.utc) if status == "completed" else None,
            )
            db.session.add(t)

        # Study sessions (last 14 days)
        for day_offset in range(14):
            day = datetime.now(timezone.utc) - timedelta(days=day_offset)
            n_sessions = random.randint(1, 3)
            for _ in range(n_sessions):
                subj = random.choice(subjects)
                dur = random.choice([25, 50, 75, 90])
                db.session.add(StudySession(
                    user_id=user.id,
                    subject_id=subj.id,
                    session_type="focus",
                    duration_minutes=dur,
                    started_at=day,
                    ended_at=day,
                ))

        # Academic events
        events = [
            ("Midterm Exam – Data Structures", subjects[0], "exam", today + timedelta(days=10)),
            ("Final Project Demo", subjects[2], "exam", today + timedelta(days=20)),
            ("Quiz – Algorithms Week 6", subjects[1], "exam", today + timedelta(days=4)),
            ("Assignment 3 Due", subjects[3], "assignment", today + timedelta(days=6)),
        ]
        for title, subj, etype, edate in events:
            db.session.add(AcademicEvent(
                user_id=user.id,
                subject_id=subj.id,
                title=title,
                event_type=etype,
                event_date=edate,
            ))

        db.session.commit()
        print("[OK] Demo data seeded. Login: username=demo  password=demo1234")


if __name__ == "__main__":
    app.run()
