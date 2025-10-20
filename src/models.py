from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    schedule = Column(String(200), nullable=True)
    max_participants = Column(Integer, nullable=True)
    # participants are stored as a comma-separated string for this simple demo
    participants = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def participants_list(self):
        if not self.participants:
            return []
        return [p for p in self.participants.split(",") if p]

    def set_participants(self, lst):
        self.participants = ",".join(lst)
