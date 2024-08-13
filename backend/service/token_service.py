from datetime import timedelta

from sqlalchemy.orm import Session

from backend.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.exceptions import InvalidCredentialsException
from backend.models.pydantic_models import Token
from backend.service.oauth import authenticate_user
from backend.service.oauth import create_access_token


def create_token(form_data, db: Session):
    """Create a token based on username and password"""

    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise InvalidCredentialsException()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token.model_validate(
        {"access_token": access_token, "token_type": "bearer"}
    )
