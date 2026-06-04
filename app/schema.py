from typing import Literal

from pydantic import BaseModel, EmailStr
from datetime import datetime

class CreateUser(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class ConfigDict:
        from_attributes = True
   
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserTokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
    
class TokenData(BaseModel):
    id: int | None = None

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class CreatePost(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    
    class Config:
        from_attributes = True       
    
class Vote(BaseModel):
    post_id: int
    dir: Literal[0,1]
    
# 