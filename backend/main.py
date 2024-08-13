from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from contextlib import asynccontextmanager

from backend.api.health import health_router
from backend.api.user import user_router
from backend.api.token import token_router
from backend.api.query import query_router
from backend.api.document import document_router
from backend.db.utils import populate_admin_user
from backend.db.sessions import create_tables
from backend.db.sessions import get_db
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    db_generator = get_db()
    db: Session = next(db_generator)
    populate_admin_user(db)
    yield

app = FastAPI(
    title="Aora API",
    description="Aora API",
    contact="",
    version="0.0.1",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(token_router)
app.include_router(user_router)
app.include_router(query_router)
app.include_router(document_router)


@app.get(
    "/",
    tags=["Docs"],
    description="Temporary redirect to docs to easy code development",
    include_in_schema=False
)
def redirect_to_docs():
    return RedirectResponse("/docs")
