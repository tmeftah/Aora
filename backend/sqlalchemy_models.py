from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



engine = create_engine("sqlite:///users.db")
Base = declarative_base()
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    # 1 = user, 4 = manager, 5 = admin, 6 = superadmin
    role = Column(Integer, default=1)