from datetime import datetime
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=20)


class UserRegister(UserBase):
    password: str


class User(UserBase):
    id: int
    access_bitmap: int
    created_time: datetime
    last_login_time: datetime

    class Config:
        orm_mode = True
