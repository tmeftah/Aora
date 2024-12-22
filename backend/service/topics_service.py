from typing import List

from sqlalchemy.orm import Session

from backend.models.pydantic_models import TopicPydantic
from backend.models.sqlalchemy_models import Topic
from backend.exceptions import DuplicateUserException


def get_all_topics(db: Session) -> List[TopicPydantic]:
    """Get list of all Users"""

    return [TopicPydantic(name=topic.name) for topic in db.query(Topic).all()]

def get_topic_by_name(name: str, db: Session) -> User | None:
    """Get user by name"""

    topic = db.query(Topic).filter(Topic.name == name).first()
    return topic if topic else None

def created_topic(
    db: Session,
    name: str,
) -> TopicPydantic:
    """Create a user based on the information passed"""

    topic_exists = get_topic_by_name(name, db)
    if topic_exists:
        raise DuplicateUserException()

    topic = Topic(
        name=name
    )
    db.add(topic)
    db.commit()
    return TopicPydantic.model_validate(
        {"name": topic.name}
    )