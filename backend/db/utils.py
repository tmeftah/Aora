from fastapi import Depends
from sqlalchemy.orm import Session

from backend.db.sessions import get_db
from backend.models.sqlalchemy_models import User, Topic
from backend.service.oauth import encrypt_password
from backend.service.oauth import get_user_by_name
from backend.service.topics_service import get_topic_by_name


def populate_admin_user(db: Session = Depends(get_db)):
    admin_user = get_user_by_name("admin", db)
    if not admin_user:
        admin_user = User(
            username="admin", password_hash=encrypt_password("admin"), role=6
        )
        db.add(admin_user)

    topic = get_topic_by_name("Artifical Intelligence", db)
    if not topic:
        topic = Topic(name="Artifical Intelligence")
        db.add(topic)
    db.commit()
