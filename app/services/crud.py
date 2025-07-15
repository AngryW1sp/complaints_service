import logging
from sqlalchemy.orm import Session
from app.models.complaint import Complaint
from app.schemas.complaint import ComplaintCreate
from datetime import datetime

logger = logging.getLogger(__name__)


def create_complaint(db: Session, complaint_in: ComplaintCreate, sentiment: str = "unknown", category: str = "другое", ip_location: str = "не указано") -> Complaint:
    try:
        complaint = Complaint(
            text=complaint_in.text,
            sentiment=sentiment,
            category=category,
            timestamp=datetime.now(),
            ip_location=ip_location
        )
        db.add(complaint)
        db.commit()
        db.refresh(complaint)
        logger.info(
            f"Жалоба создана: id={complaint.id}, категория={category}, настроение={sentiment}")
        return complaint
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при создании жалобы: {e}", exc_info=True)
        raise
