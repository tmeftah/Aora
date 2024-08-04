from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import jwt
from bcrypt import hashpw, gensalt, checkpw
from .rag_llms_langchain import chain, langfuse_handler
from .embeddings.ingest import get_vectorstore
import json
import uuid


origins = [
    "http://localhost",
    "http://127.0.0.1:8000",
]


# SQLAlchemy setup

engine = create_engine("sqlite:///users.db")
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    # 1 = user, 4 = manager, 5 = admin, 6 = superadmin
    role = Column(Integer, default=1)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# FastAPI setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password encryption


def encrypt_password(password: str):
    return hashpw(password.encode(), gensalt())


def verify_password(plain_password: str, hashed_password: str):
    return checkpw(plain_password.encode(), hashed_password)

# User authentication


def get_user(username: str):
    return session.query(User).filter(User.username == username).first()


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user.password_hash):
        return False
    return user


# JWT secret key
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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

# Populate admin user on first start


def populate_admin_user():
    admin_user = get_user("admin")
    if not admin_user:
        admin_user = User(username="admin",
                          password_hash=encrypt_password("admin"), role=6)
        session.add(admin_user)
        session.commit()


populate_admin_user()

# Routes


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "role": current_user.role}


@app.get("/users/")
async def read_users(current_user: User = Depends(get_current_user)):
    if current_user.role < 5:
        raise HTTPException(
            status_code=403, detail="Only admin users can view all users")
    return [{"username": user.username, "role": user.role} for user in session.query(User).all()]


@app.get("/users/{user_id}")
async def read_user(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id and current_user.role < 5:
        raise HTTPException(
            status_code=403, detail="Only admin users can view other users")
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.username, "role": user.role}


@app.post("/users/")
async def create_user(username: str, password: str, role: int, current_user: User = Depends(get_current_user)):
    if current_user.role < 5:
        raise HTTPException(
            status_code=403, detail="Only admin users can create new users")
    user = User(username=username,
                password_hash=encrypt_password(password), role=role)
    session.add(user)
    session.commit()
    return {"username": user.username, "role": user.role}


@app.put("/users/{user_id}")
async def update_user(user_id: int, username: str, password: str, role: int, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id and current_user.role < 5:
        raise HTTPException(
            status_code=403, detail="Only admin users can update other users")
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = username
    user.password = password
    user.role = role
    session.commit()
    return {"username": user.username, "role": user.role}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id and current_user.role < 5:
        raise HTTPException(
            status_code=403, detail="Only admin users can delete other users")
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted"}


# Define a route for the app
@app.get("/query")
async def query(query: str):
    # if current_user.role < 5:
    #     raise HTTPException(status_code=403, detail="Only admin users can delete other users")
    store = get_vectorstore()
    docs = store.invoke(query)

    print(20*"*", "docs", 20*"*", "\n", docs)

    async def stream_generator():
        # Use the LangChain model to generate text
        print(20*'*', "\n", query)
        async for text in chain.astream({"input": query, "context": docs}):
            yield json.dumps({"event_id": str(uuid.uuid4()), "data": text})

        # TODO  here we have to add the metadata/source

    return StreamingResponse(stream_generator(), media_type="application/x-ndjson")
