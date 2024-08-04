from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.health import health_router
from backend.api.user import user_router
from backend.api.token import token_router
from backend.api.query import query_router
from backend.utils import populate_admin_user


app = FastAPI()

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
populate_admin_user()
