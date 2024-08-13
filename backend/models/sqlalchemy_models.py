from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    # 1 = user, 4 = manager, 5 = admin, 6 = superadmin
    role = Column(Integer, default=1)


class Documents(Base):
    """ Documents table where all the list of uploaded
    documents are to be found"""

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    content_type = Column(String)
