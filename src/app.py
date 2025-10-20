"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Activity, Base


app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Database setup
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./data.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fallback in-memory activities (used only if DB is missing or empty)
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """Return activities from the database if available, otherwise fallback to in-memory dict."""
    # Try to read from DB
    try:
        db = next(get_db())
        db_activities = db.query(Activity).all()
        if db_activities:
            out = {}
            for a in db_activities:
                out[a.name] = {
                    "description": a.description,
                    "schedule": a.schedule,
                    "max_participants": a.max_participants,
                    "participants": a.participants_list()
                }
            return out
    except Exception:
        # If DB isn't set up yet, fall back to in-memory
        pass

    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Try DB-backed signup first
    try:
        db = next(get_db())
        act = db.query(Activity).filter(Activity.name == activity_name).first()
        if not act:
            # fallback to in-memory
            raise Exception("not found in db")

        participants = act.participants_list()
        if email in participants:
            raise HTTPException(status_code=400, detail="Student is already signed up")

        participants.append(email)
        act.set_participants(participants)
        db.add(act)
        db.commit()
        return {"message": f"Signed up {email} for {activity_name}"}
    except HTTPException:
        raise
    except Exception:
        # fallback to in-memory for now
        if activity_name not in activities:
            raise HTTPException(status_code=404, detail="Activity not found")

        activity = activities[activity_name]
        if email in activity["participants"]:
            raise HTTPException(status_code=400, detail="Student is already signed up")

        activity["participants"].append(email)
        return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    try:
        db = next(get_db())
        act = db.query(Activity).filter(Activity.name == activity_name).first()
        if not act:
            raise Exception("not found in db")

        participants = act.participants_list()
        if email not in participants:
            raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

        participants.remove(email)
        act.set_participants(participants)
        db.add(act)
        db.commit()
        return {"message": f"Unregistered {email} from {activity_name}"}
    except HTTPException:
        raise
    except Exception:
        # fallback to in-memory
        if activity_name not in activities:
            raise HTTPException(status_code=404, detail="Activity not found")

        activity = activities[activity_name]
        if email not in activity["participants"]:
            raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

        activity["participants"].remove(email)
        return {"message": f"Unregistered {email} from {activity_name}"}
