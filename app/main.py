import logging
from fastapi import Request, FastAPI, Depends, HTTPException, status
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.complaint import Complaint
from app.core.database import SessionLocal
from app.schemas.complaint import ComplaintCreate, ComplaintResponse, ComplaintUpdate
from app.services.crud import create_complaint
from app.core.config import NINJAS_API_KEY, API_LAYER_KEY, YANDEX_IAM_TOKEN, YANDEX_FOLDER_ID
from app.services.yandexapi import ApisInterface

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Ошибка работы с БД: {e}", exc_info=True)
        raise
    finally:
        db.close()


@app.post("/complaints/", response_model=ComplaintResponse)
def submit_complaint(
    request: Request,
    complaint_in: ComplaintCreate,
    db: Session = Depends(get_db)
):
    logger.info(f"Получен POST /complaints/ от IP {request.client.host}")
    try:
        apis_request = ApisInterface(
            iam_token=YANDEX_IAM_TOKEN,
            folder_id=YANDEX_FOLDER_ID,
            x_api_key=NINJAS_API_KEY,
            user_text=complaint_in.text,
            api_layer_key=API_LAYER_KEY,
            ip=request.client.host
        )
        analysis = apis_request.run()
        logger.info(f"Анализ жалобы: {analysis}")

        complaint = create_complaint(
            db,
            complaint_in,
            category=analysis.get("yandex"),
            sentiment=analysis.get("ninjas"),
            ip_location=analysis.get("ip_location")
        )
        logger.info(f"Жалоба сохранена с id={complaint.id}")
        return complaint
    except Exception as e:
        logger.error(f"Ошибка при обработке жалобы: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обработке жалобы"
        )


@app.get("/complaints/", response_model=list[ComplaintResponse])
def get_last_hour_complaints(db: Session = Depends(get_db)):
    logger.info("Получен GET /complaints/")
    try:
        one_hour_ago = datetime.now() - timedelta(hours=1)
        complaints = db.query(Complaint).filter(
            Complaint.timestamp >= one_hour_ago
        ).all()
        logger.info(f"Найдено {len(complaints)} жалоб за последний час")
        return complaints
    except Exception as e:
        logger.error(f"Ошибка при получении жалоб: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении жалоб"
        )


@app.patch("/complaints/{complaint_id}")
def update_complaint(complaint_id: int,
                     update_data: ComplaintUpdate, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Жалоба не найдена")

    # Применяем только переданные поля
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(complaint, key, value)

    db.commit()
    db.refresh(complaint)
    return complaint
