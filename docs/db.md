Database
=======

This project now includes a minimal SQLite + SQLAlchemy setup to persist Activities.

Files added:
- `src/models.py` — SQLAlchemy `Activity` model (simple participants stored as comma-separated string).
- `scripts/init_db.py` — initialization script that creates the SQLite DB and seeds a few activities.

How to initialize locally:

```bash
python3 -m pip install -r requirements.txt
python scripts/init_db.py
# Start the app
uvicorn src.app:app --reload
```

Notes and next steps:
- Participants are stored as a comma-separated string to keep the data model small for the exercise. We'll normalize this to a join table (ActivityParticipants) when we add users.
- After DB is initialized, endpoints at `/activities`, `/activities/{name}/signup`, and `/activities/{name}/unregister` use the DB-backed model automatically.
