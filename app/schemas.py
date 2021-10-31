from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostSchema(BaseModel):
    title: str
    content: str
    published: bool
    created_at: datetime
    owner: UserResponse

    class Config:
        orm_mode = True


class PostResponse(BaseModel):
    Post: PostSchema
    votes: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
