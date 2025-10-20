"""Simple script to initialize the SQLite database for the project.

Run this with: python scripts/init_db.py
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base, Activity


def init_db(db_url: str = None):
    if db_url is None:
        db_url = os.environ.get("DATABASE_URL", "sqlite:///./data.db")

    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Seed some activities if none exist
    if session.query(Activity).count() == 0:
        seed = [
            Activity(name="Chess Club", description="Learn strategies and compete in chess tournaments", schedule="Fridays, 3:30 PM - 5:00 PM", max_participants=12, participants=",".join(["michael@mergington.edu","daniel@mergington.edu"])),
            Activity(name="Programming Class", description="Learn programming fundamentals and build software projects", schedule="Tuesdays and Thursdays, 3:30 PM - 4:30 PM", max_participants=20, participants=",".join(["emma@mergington.edu","sophia@mergington.edu"])),
            Activity(name="Gym Class", description="Physical education and sports activities", schedule="Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM", max_participants=30, participants=",".join(["john@mergington.edu","olivia@mergington.edu"]))
        ]
        session.add_all(seed)
        session.commit()
        print("Seeded initial activities")
    else:
        print("Database already initialized with activities")


if __name__ == "__main__":
    init_db()
