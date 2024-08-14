from typing import List

from sqlalchemy.orm import Session

from backend.exceptions import NoValidPermissionsException
from backend.exceptions import UserNotFoundException
from backend.models.pydantic_models import UserPydantic
from backend.models.sqlalchemy_models import User


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

    if current_user.id != user_id and current_user.role < 5:
        raise NoValidPermissionsException()

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException()

    return UserPydantic.model_validate(
        {"username": user.username, "role": user.role}
    )
