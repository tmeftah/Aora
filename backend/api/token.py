from fastapi import APIRouter, Depends, HTTPException
from backend.models.pydantic_models import Token
from backend.service.oauth import authenticate_user, create_access_token
from backend.config import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from backend.db.sessions import get_db
from backend.exceptions import InvalidCredentialsException


token_router = APIRouter(prefix="/token",
                         tags=["Tokens"],
                         responses={
                             200: {"description": "Success"},
                             404: {"description": "Resource Not Found"},
                             500: {"description": "Internal Server Error"},
                         },)


@token_router.post("/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):

    try:
        user = authenticate_user(form_data.username,
                                 form_data.password,
                                 db)

        if not user:
            raise InvalidCredentialsException()

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
