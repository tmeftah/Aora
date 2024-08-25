from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


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
    status:str
    created_at:datetime
    
  


    
   
