from fastapi import Depends
from sqlalchemy.orm import Session
from backend.models.sqlalchemy_models import User
from backend.db.sessions import get_db
from backend.service.oauth import encrypt_password, get_user


def populate_admin_user(db: Session = Depends(get_db)):
    admin_user = get_user("admin")
    if not admin_user:
        admin_user = User(
            username="admin",
            password_hash=encrypt_password("admin"),
            role=6
        )
        db.add(admin_user)
        db.commit()
