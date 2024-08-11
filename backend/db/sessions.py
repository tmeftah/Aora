from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from backend.models.sqlalchemy_models import Base


engine = create_engine("sqlite:///users.db")

Base.metadata.create_all(engine)

session_maker = sessionmaker(bind=engine)
session = session_maker()
