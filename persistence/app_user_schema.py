import datetime
from pydantic import BaseModel


class AppUserBase(BaseModel):
    username: str


class AppUserCreate(AppUserBase):
    password: str


class AppUser(AppUserBase):
    id: int
    access_bitmap: int
    created_time: datetime
    last_login_time: datetime

    class Config:
        orm_mode = True
