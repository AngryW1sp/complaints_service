from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    status = Column(String, default="open")
    timestamp = Column(DateTime, default=datetime.utcnow)
    sentiment = Column(String, default="unknown")
    category = Column(String, default="другое")
    ip_location = Column(String, default="не указано")
