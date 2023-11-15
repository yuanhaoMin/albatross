from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class UserBase(BaseModel):
    # Validation will be inherited by subclasses
    username: str = Field(min_length=3, max_length=40)


class GetInfoResponse(UserBase):
    id: int
    password: str
    access_bitmap: int
    created_time: datetime
    last_login_time: Optional[datetime] = None
    subscription_end_time: Optional[datetime] = None

    class Config:
        orm_mode = True


class LoginRequest(UserBase):
    password: str


class LoginResponse(UserBase):
    id: int
    created_time: datetime
    last_login_time: datetime

    class Config:
        orm_mode = True


class RegisterRequest(UserBase):
    password: str


class RegisterResponse(UserBase):
    id: int
    created_time: datetime
    subscription_end_time: datetime

    class Config:
        orm_mode = True


class ResetPasswordRequest(BaseModel):
    username: str
    password: str


class ResetPasswordResponse(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
