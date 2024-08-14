from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserPydantic(BaseModel):
    username: str
    role: int


class DocumentPydantic(BaseModel):
    filename: str
    content_type: str
