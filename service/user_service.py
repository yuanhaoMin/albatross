from fastapi import HTTPException
from persistence import user_crud
from persistence.user_model import AppUser
from schema import user_schema
from sqlalchemy.orm import Session
from util.time_util import get_current_berlin_time


def login_user(request: user_schema.LoginUserRequest, db: Session) -> AppUser:
    user = user_crud.get_user_by_username_and_password(
        username=request.username,
        password=request.password,
        db=db,
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user_crud.update_user_last_login(user.id, get_current_berlin_time(), db)


def register_user(request: user_schema.RegisterUserRequest, db: Session) -> AppUser:
    user_with_same_username = get_user_by_username(request.username, db)
    if user_with_same_username:
        raise HTTPException(status_code=409, detail="Username already exists")
    created_time = get_current_berlin_time()
    return user_crud.create_user(
        username=request.username,
        password=request.password,
        created_time=created_time,
        db=db,
    )


def get_user_by_username(username: str, db: Session) -> AppUser:
    user = user_crud.get_user_by_username(username=username, db=db)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User does not exist".format(username),
        )
    return user
