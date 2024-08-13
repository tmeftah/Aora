import jwt

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

from backend.config import SECRET_KEY, ALGORITHM
from backend.models.sqlalchemy_models import User
from backend.db.sessions import get_db
from backend.models.pydantic_models import TokenData

from sqlalchemy.orm import Session
from bcrypt import hashpw, gensalt, checkpw
from datetime import datetime, timedelta
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def encrypt_password(password: str) -> bytes:
    return hashpw(password.encode(), gensalt())


def verify_password(plain_password: str, hashed_password: str) -> bytes:
    return checkpw(plain_password.encode(), hashed_password)


def get_user_by_name(username: str, db: Session):
    """ Get user by name"""
    user = db.query(User).filter(User.username == username).first()
    return user if user else None


def authenticate_user(username: str, password: str, db: Session):
    user = get_user_by_name(username, db)
    if not user or not verify_password(password, user.password_hash):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(username=username)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_name(username=token_data.username)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
