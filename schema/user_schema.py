from datetime import datetime
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=20)


class RegisterUserRequest(UserBase):
    password: str


class RegisterUserResponse(UserBase):
    id: int
    created_time: datetime

    class Config:
        orm_mode = True
