from typing import List

from sqlalchemy.orm import Session

from backend.models.pydantic_models import TopicPydantic
from backend.models.sqlalchemy_models import Topic
from backend.exceptions import DuplicateTopicException
from backend.exceptions import NoTopicFoundException


def get_all_topics(db: Session) -> List[TopicPydantic]:
    """Get list of all Topics"""

    return [TopicPydantic(name=topic.name) for topic in db.query(Topic).all()]


def get_topic_by_name(name: str, db: Session) -> Topic:
    """Get Topic by name"""

    topic = db.query(Topic).filter(Topic.name == name).first()
    return topic if topic else None


def get_topic_by_id(topic_id: str, db: Session) -> Topic:
    """Get topic by id"""

    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    return topic if topic else None


def created_topic(
    db: Session,
    name: str,
) -> TopicPydantic:
    """Create a Topic based on the information passed"""

    topic_exists = get_topic_by_name(name, db)
    if topic_exists:
        raise DuplicateTopicException()

    topic = Topic(name=name)
    db.add(topic)
    db.commit()
    return TopicPydantic.model_validate({"name": topic.name})


def update_topic(
    db: Session,
    old_name: str,
    name: str,
) -> TopicPydantic:
    """Update a topic based on the information passed"""
    topic_exists = get_topic_by_name(old_name, db)
    if not topic_exists:
        raise NoTopicFoundException()

    topic_exists.name = name
    db.commit()
    return TopicPydantic.model_validate({"name": topic_exists.name})


def delete_topic_details(db: Session, topic_name: str) -> dict:
    """Delete Topic based on user id"""

    topic = get_topic_by_name(name=topic_name, db=db)
    if not topic:
        raise NoTopicFoundException()

    db.delete(topic)
    db.commit()
    return {"message": "Topic deleted"}
