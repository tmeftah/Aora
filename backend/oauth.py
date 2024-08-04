import jwt

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

from backend.config import SECRET_KEY, ALGORITHM
from backend.sqlalchemy_models import session, User
from backend.pydantic_models import TokenData

from bcrypt import hashpw, gensalt, checkpw
from datetime import datetime, timedelta
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def encrypt_password(password: str):
    return hashpw(password.encode(), gensalt())


def verify_password(plain_password: str, hashed_password: str):
    return checkpw(plain_password.encode(), hashed_password)

def get_user(username: str):
    return session.query(User).filter(User.username == username).first()


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user.password_hash):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
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