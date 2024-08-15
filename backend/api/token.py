from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.db.sessions import get_db
from backend.exceptions import InvalidCredentialsException
from backend.models.pydantic_models import Token
from backend.service.token_service import create_token


token_router = APIRouter(
    prefix="/token",
    tags=["Tokens"],
    responses={
        200: {"description": "Success"},
        404: {"description": "Resource Not Found"},
        500: {"description": "Internal Server Error"},
    },
)


@token_router.post("/", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Create a token for a specific user
    If the user does not exists or his credentials are invalid (token will not
    be created) and an appropriate response will be returned
    """

    try:
        return create_token(form_data=form_data, db=db)

    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
