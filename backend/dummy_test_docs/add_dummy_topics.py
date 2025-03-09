
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from backend.models.sqlalchemy_models import Topic
import os


DATABASE_URL = os.getenv("DATABASE_URL", "aora.db")
engine = create_engine("sqlite:///"+DATABASE_URL)
Base = declarative_base()


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

keywords = [
    "Cybersecurity",
    "Artificial Intelligence",
    "Renewable Energy",
    "Blockchain",
    "Cloud Computing",
    "DevOps",
    "Automation Testing",
    "Big Data",
    "Quantum Computing",
    "Web Development"
]


def add_topics():
    """Add dummy topics."""
    for keyword in keywords:
        try:
            session.add(Topic(name=keyword))
            session.commit()
            print(f"Added: {keyword}")
        except Exception as e:
            print(e)
            session.rollback()  # Rollback transaction to avoid lock
            print(f"Skipped (already exists): {keyword}")


if __name__ == '__main__':
    add_topics()
