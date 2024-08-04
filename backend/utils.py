from backend.sqlalchemy_models import User, session
from backend.oauth import encrypt_password, get_user



def populate_admin_user():
    admin_user = get_user("admin")
    if not admin_user:
        admin_user = User(username="admin",
                          password_hash=encrypt_password("admin"), role=6)
        session.add(admin_user)
        session.commit()