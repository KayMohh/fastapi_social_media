from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True

class PostCreate(PostBase):
    pass

class User(BaseModel):
    email: EmailStr
    id: int
    created_at : datetime

    class Config:
        from_attributes = True
class Post(PostBase):
    id: int
    created_at : datetime
    owner_id: int
    # owner: Optional [User]
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password:  str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int

class Vote(BaseModel):
    post_id: int
    dir: conint (le=1, ge = 0) # type: ignore
class PostWithVote(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True