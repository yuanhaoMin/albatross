from datetime import datetime, timedelta
from fastapi import HTTPException
from persistence import user_crud
from persistence.user_model import AppUser
from schema import user_schema
from sqlalchemy.orm import Session
from util.time_util import get_current_utc8_time


def delete_user_by_username(username: str, db: Session) -> AppUser:
    return user_crud.delete_user_by_username(username=username, db=db)


def get_user_by_username(username: str, db: Session) -> AppUser:
    user = user_crud.get_user_by_username(username=username, db=db)
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="User does not exist".format(username),
        )
    return user


def login_user(request: user_schema.LoginRequest, db: Session) -> AppUser:
    user = user_crud.get_user_by_username(
        username=request.username,
        db=db,
    )
    if user is None or user.password != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user_crud.update_user_last_login(user.id, get_current_utc8_time(), db)


def register_user(request: user_schema.RegisterRequest, db: Session) -> AppUser:
    user_with_same_username = user_crud.get_user_by_username(request.username, db)
    if user_with_same_username is not None:
        raise HTTPException(status_code=409, detail="Username already exists")
    created_time = get_current_utc8_time()
    subscription_end_time = created_time + timedelta(days=7)
    return user_crud.create_user(
        username=request.username,
        password=request.password,
        access_bitmap=15,
        created_time=created_time,
        subscription_end_time=subscription_end_time,
        db=db,
    )


def update_user_password(username: str, password: str, db: Session) -> AppUser:
    user = get_user_by_username(username=username, db=db)
    return user_crud.update_user_password(
        id=user.id,
        password=password,
        db=db,
    )
