from datetime import datetime
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    # validation will be inherited by subclasses
    username: str = Field(min_length=3, max_length=20)


class LoginUserRequest(UserBase):
    password: str


class LoginUserResponse(UserBase):
    id: int
    created_time: datetime
    last_login_time: datetime

    class Config:
        orm_mode = True


class RegisterUserRequest(UserBase):
    password: str


class RegisterUserResponse(UserBase):
    id: int
    created_time: datetime

    class Config:
        orm_mode = True
