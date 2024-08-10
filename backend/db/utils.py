from backend.models.sqlalchemy_models import User
from backend.db.sessions import session
from backend.service.oauth import encrypt_password, get_user


def populate_admin_user():
    admin_user = get_user("admin")
    if not admin_user:
        admin_user = User(
            username="admin", password_hash=encrypt_password("admin"), role=6
        )
        session.add(admin_user)
        session.commit()
