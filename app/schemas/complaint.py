from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ComplaintCreate(BaseModel):
    text: str


class ComplaintResponse(BaseModel):
    id: int
    status: str
    sentiment: str
    category: str
    ip_location: str
    timestamp: datetime

    class Config:
        from_attributes = True
