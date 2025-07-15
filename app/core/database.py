from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLITE_URL = "sqlite:///./complaints.db"

engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
