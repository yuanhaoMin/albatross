from datetime import datetime
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    # Validation will be inherited by subclasses
    username: str = Field(min_length=3, max_length=40)


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
