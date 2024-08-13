from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker

from backend.models.sqlalchemy_models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///aora.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)


# Dependency Injection added


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()
