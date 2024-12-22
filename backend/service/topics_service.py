from typing import List

from sqlalchemy.orm import Session

from backend.models.pydantic_models import TopicPydantic
from backend.models.sqlalchemy_models import Topic


def get_all_topics(db: Session) -> List[TopicPydantic]:
    """Get list of all Users"""

    return [TopicPydantic(name=topic.name) for topic in db.query(Topic).all()]
