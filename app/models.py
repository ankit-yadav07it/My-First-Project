from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    theme = db.Column(db.String(20), nullable=False, default="light")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    color = db.Column(db.String(50), nullable=True)
    semester = db.Column(db.String(50), nullable=True)


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    subject_id = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(20), nullable=False, default="medium")
    status = db.Column(db.String(30), nullable=False, default="pending")
    due_date = db.Column(db.Date, nullable=True)
    estimated_minutes = db.Column(db.Integer, nullable=True, default=0)


class StudySession(db.Model):
    __tablename__ = "study_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    subject_id = db.Column(db.Integer, nullable=True)
    session_type = db.Column(db.String(30), nullable=False, default="focus")
    duration_minutes = db.Column(db.Integer, nullable=False, default=0)
    started_at = db.Column(db.DateTime, nullable=True)
    ended_at = db.Column(db.DateTime, nullable=True)


class AcademicEvent(db.Model):
    __tablename__ = "academic_events"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    subject_id = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(200), nullable=False)
    event_type = db.Column(db.String(40), nullable=False, default="event")
    event_date = db.Column(db.Date, nullable=True)


class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    daily_study_goal_minutes = db.Column(db.Integer, nullable=False, default=120)
    weekly_study_goal_minutes = db.Column(db.Integer, nullable=False, default=600)
    daily_task_goal = db.Column(db.Integer, nullable=False, default=4)


# Expose the DB instance for run.py and other imports
# This is defined in app/__init__.py but imported into the package namespace.
# The actual `db` object itself is initialized in `create_app`.
