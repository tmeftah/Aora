
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    # 1 = user, 4 = manager, 5 = admin, 6 = superadmin
    role = Column(Integer, default=1)


class Documents(Base):
    """Documents table where all the list of uploaded
    documents are to be found"""

    __tablename__ = "documents"
    # copy doc in /docs folder
    # each doc a hash
    # hash exists in metadata no embeddings

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    filehash = Column(String, unique=True)
    content_type = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)

    topic = relationship("Topic", back_populates="documents")


class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    documents = relationship(
        "Documents", back_populates="topic")
