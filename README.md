# FocusFlow — Student Productivity Dashboard

A modern, full-featured web application for college students to manage assignments, study schedules, deadlines, and productivity — all in one place.

Built as a portfolio project to demonstrate full-stack development skills with Flask, SQLAlchemy, and vanilla JavaScript.

---

## ✨ Features

| Module | What it does |
|---|---|
| **Dashboard** | Personalized greeting, today's tasks, weekly chart, subject chart, upcoming exams, daily quote |
| **Task Manager** | Full CRUD, filter by status/priority/subject, search, sort, overdue highlighting |
| **Subjects** | Color-coded subject cards with study time and task progress |
| **Pomodoro Timer** | 25/5/15 configurable timer, focus mode, session auto-save, audio notification |
| **Calendar** | Monthly grid with tasks and events, add exam/assignment/event |
| **Analytics** | 14-day study chart, subject distribution, task completion doughnut, streak tracker |
| **Weekly Review** | Last-week summary with practical improvement suggestions |
| **Goals & Settings** | Daily/weekly study goals, Pomodoro config, profile, theme |
| **Quick Capture** | Add a task from any page with keyboard shortcut `Q` |
| **Themes** | Light · Dark · Daylight (warm) — toggled per user, persisted to DB |
| **Tests** | 24 pytest tests covering auth, CRUD, isolation, sessions, analytics |

---

## 🗂️ Project Structure

```
focusflow/
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # SQLAlchemy models
│   ├── routes/
│   │   ├── auth.py          # Login, register, logout
│   │   ├── dashboard.py     # Main dashboard stats
│   │   ├── tasks.py         # Task CRUD
│   │   ├── subjects.py      # Subject CRUD
│   │   ├── timer.py         # Pomodoro timer & session saving
│   │   ├── calendar.py      # Calendar planner
│   │   ├── analytics.py     # Charts and analytics
│   │   ├── goals.py         # Goals & settings
│   │   ├── review.py        # Weekly review
│   │   └── api.py           # JSON API (theme, quick capture)
│   ├── templates/           # Jinja2 HTML templates
│   │   ├── base.html        # Sidebar, topbar, flash messages, quick capture modal
│   │   ├── auth/            # Login and register pages
│   │   ├── dashboard/       # Main dashboard
│   │   ├── tasks/           # Task list, form, detail
│   │   ├── subjects/        # Subject list and form
│   │   ├── timer/           # Pomodoro timer page
│   │   ├── calendar/        # Monthly calendar
│   │   ├── analytics/       # Analytics charts
│   │   ├── goals/           # Goals & settings
│   │   ├── review/          # Weekly review
│   │   └── errors/          # 404, 403, 500 pages
│   └── static/
│       ├── css/main.css     # Full CSS (themes, components, responsive)
│       └── js/
│           ├── app.js       # Theme toggle, sidebar, quick capture
│           └── timer.js     # Pomodoro timer logic
├── tests/
│   └── test_app.py          # 24 pytest tests
├── config.py                # Configuration classes
├── run.py                   # Entry point + CLI commands
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🗃️ Database Models

| Model | Key Fields |
|---|---|
| `User` | id, username, email, password_hash, full_name, theme |
| `Subject` | id, user_id, name, color, semester |
| `Task` | id, user_id, subject_id, title, priority, status, due_date, estimated_minutes |
| `StudySession` | id, user_id, subject_id, session_type, duration_minutes, started_at |
| `AcademicEvent` | id, user_id, subject_id, title, event_type, event_date |
| `Goal` | id, user_id, daily_study_goal_minutes, weekly_study_goal_minutes, pomodoro settings |

All user-owned models include `user_id` foreign keys with authorization checks on every server operation.

---

## 🚀 Setup (Windows — VS Code)

### 1. Prerequisites

- Python 3.10+ installed ([python.org](https://python.org))
- Git (optional)

### 2. Clone or download

```powershell
# If using Git:
git clone <your-repo-url>
cd focusflow

# Or just open the focusflow/ folder in VS Code
```

### 3. Create and activate virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> If you get an execution policy error, run:  
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure environment

```powershell
copy .env.example .env
```

Edit `.env` and set a real `SECRET_KEY`:

```
SECRET_KEY=your-long-random-secret-key-here
FLASK_ENV=development
```

Generate a good key:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

### 6. Initialize the database

```powershell
flask init-db
```

### 7. (Optional) Load demo data

```powershell
flask seed-db
```

This creates a demo account: **username=`demo`**, **password=`demo1234`** with sample subjects, tasks, study sessions, and events.

### 8. Run the application

```powershell
flask run
```

Open your browser at **http://127.0.0.1:5000**

---

## 🧪 Running Tests

```powershell
pytest tests/ -v
```

Expected output: **24 passed** in ~8 seconds.

Tests cover:
- User registration and login
- Duplicate username prevention
- Password hashing (never stored in plaintext)
- Protected route redirects
- Task CRUD and ownership isolation
- Study session validation
- Subject creation and deduplication
- Goals update
- Analytics page loading
- User data isolation

---

## 📖 Usage Guide

### Keyboard shortcuts
| Key | Action |
|---|---|
| `Q` | Open Quick Capture (add task from anywhere) |
| `Space` | Start/pause the Pomodoro timer |
| `R` | Reset timer |
| `F` | Enter Focus Mode |
| `Esc` | Exit modal / Focus Mode |

### Themes
Click the ☀️/🌙 icon in the top bar to cycle: **Light → Dark → Daylight**

### Pomodoro Timer
1. Go to **Study Timer**
2. Select a subject (optional)
3. Click **▶ Start** — when the session ends, it's automatically saved
4. Or enter **Focus Mode** for a minimal distraction-free screen

### Quick Capture
Press `Q` on any page to instantly add a task. Fill in title and optional priority/due date.

---

## 🚢 Deployment (basic)

For a simple deployment on a Linux server:

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 "run:app"
```

For production:
- Set `FLASK_ENV=production` in `.env`
- Use a real `SECRET_KEY`
- Set up a reverse proxy (nginx) in front of gunicorn
- Use PostgreSQL instead of SQLite (change `DATABASE_URL`)

---

## 🔒 Security Notes

- Passwords hashed with Werkzeug's PBKDF2-SHA256
- CSRF protection via Flask-WTF on all forms
- Session cookies are `HttpOnly` and `SameSite=Lax`
- Server-side authorization on every user-specific DB operation
- No plaintext secrets in source code — loaded from `.env`
- SQLAlchemy parameterized queries prevent SQL injection

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask 3.0 |
| Database | SQLite + SQLAlchemy 2.0 |
| Auth | Flask-Login + Werkzeug password hashing |
| Forms | Flask-WTF + WTForms (CSRF protection) |
| Templates | Jinja2 |
| Charts | Chart.js 4.4 (CDN) |
| Icons | Inline SVG (Heroicons style) |
| Fonts | Inter (Google Fonts) |
| Tests | pytest + pytest-flask |

---

## 📄 License

MIT — free to use, modify, and distribute.

Built for portfolio purposes. Replace this README with your own project description before publishing.
