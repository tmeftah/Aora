from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserPydantic(BaseModel):
    username: str
    role: int


class DocumentPydantic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    filename: str
    content_type: str
    status: str
    created_at: datetime
    topic_id: int
    vectorized: bool


class TopicPydantic(BaseModel):
    name: str
