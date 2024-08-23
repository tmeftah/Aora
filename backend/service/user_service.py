from typing import List

from sqlalchemy.orm import Session

from backend.exceptions import DuplicateUserException
from backend.exceptions import NoValidPermissionsException
from backend.exceptions import UserNotFoundException
from backend.models.pydantic_models import UserPydantic
from backend.models.sqlalchemy_models import User
from backend.service.oauth import check_current_user_permissions
from backend.service.oauth import encrypt_password


def get_all_user(current_user: User, db: Session) -> List[UserPydantic]:
    """Get list of all Users"""

    if current_user.role < 5:
        raise NoValidPermissionsException()

    return [
        UserPydantic(username=user.username, role=user.role)
        for user in db.query(User).all()
    ]


def fetch_user(current_user: User):
    """Fetch appropriate user"""

    return UserPydantic.model_validate(
        {"username": current_user.username, "role": current_user.role}
    )


def get_user_details(
    current_user: User, db: Session, user_id: int
) -> UserPydantic:
    """Get details of a specific user"""

    user_has_permissions = check_current_user_permissions(
        current_user, user_id
    )

    if not user_has_permissions:
        raise NoValidPermissionsException()

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException()

    return UserPydantic.model_validate(
        {"username": user.username, "role": user.role}
    )


def get_user_by_name(name: str, db: Session) -> User | None:
    """Get user by name"""

    user = db.query(User).filter(User.username == name).first()
    return user if user else None


def get_user_by_id(user_id: str, db: Session) -> User | None:
    """Get user by id"""

    user = db.query(User).filter(User.id == user_id).first()
    return user if user else None


def created_user(
    current_user: User,
    db: Session,
    username: str,
    password: str,
    role: int,
) -> UserPydantic:
    """Create a user based on the information passed"""

    if current_user.role < 5:
        raise NoValidPermissionsException()

    user_exists = get_user_by_name(username, db)
    if user_exists:
        raise DuplicateUserException()

    user = User(
        username=username, password_hash=encrypt_password(password), role=role
    )
    db.add(user)
    db.commit()
    return UserPydantic.model_validate(
        {"username": user.username, "role": user.role}
    )


def update_user_details(
    current_user: User,
    db: Session,
    user_id: int,
    username: str,
    password: str,
    role: int,
):
    """Update user details based on passed user id"""

    user_has_permissions = check_current_user_permissions(
        current_user, user_id
    )

    if not user_has_permissions:
        raise NoValidPermissionsException()

    user = get_user_by_id(user_id, db)
    if not user:
        raise UserNotFoundException()

    user.username = username
    user.password = password
    user.role = role
    db.commit()
    return UserPydantic.model_validate(
        {"username": user.username, "role": user.role}
    )


def delete_user_details(current_user: User, db: Session, user_id: int) -> dict:
    """Delete user based on user id"""

    user_has_permissions = check_current_user_permissions(
        current_user, user_id
    )

    if not user_has_permissions:
        raise NoValidPermissionsException()

    user = get_user_by_id(user_id=user_id, db=db)
    if not user:
        raise UserNotFoundException()

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}
