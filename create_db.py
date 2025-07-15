from app.core.database import Base, engine
from app.models import complaint

Base.metadata.create_all(bind=engine)
print("✅ База данных и таблицы созданы.")
