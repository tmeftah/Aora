from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from backend.sqlalchemy_models import session, User
from backend.oauth import oauth2_scheme, encrypt_password, get_user, authenticate_user
from backend.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.pydantic_models import Token, TokenData
from backend.api.user import user_router

from typing import Optional
from datetime import datetime, timedelta
import jwt

from .rag_llms_langchain import chain, langfuse_handler
from .embeddings.ingest import get_vectorstore
import json
import uuid


origins = [
    "http://localhost",
    "http://127.0.0.1:8000",
]


# FastAPI setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




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
