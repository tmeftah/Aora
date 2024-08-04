from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///users.db")
Base = declarative_base()
Base.metadata.create_all(engine)

session_maker = sessionmaker(bind=engine)
session = session_maker()