from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at : datetime
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password:  str

class User(BaseModel):
    email: EmailStr
    id: int
    created_at : datetime

    class Config:
        from_attributes = True
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    