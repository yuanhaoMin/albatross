from datetime import datetime
from persistence.user_model import AppUser
from sqlalchemy.orm import Session
from typing import Type


def create_user(
    username: str,
    password: str,
    access_bitmap: int,
    created_time: datetime,
    subscription_end_time: datetime,
    db: Session,
) -> AppUser:
    db_user = AppUser(
        username=username,
        password=password,
        access_bitmap=access_bitmap,
        created_time=created_time,
        subscription_end_time=subscription_end_time,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user_by_username(username: str, db: Session) -> None:
    db_user: Type[AppUser] = (
        db.query(AppUser).filter(AppUser.username == username).first()
    )
    if db_user:
        # delete the related completion entry
        if db_user.completion:
            db.delete(db_user.completion)
        # delete the related chat completion entries
        for chat_completion in db_user.chat_completions:
            db.delete(chat_completion)
        # delete the user entry
        db.delete(db_user)
        db.commit()


def get_user_by_id(id: int, db: Session) -> AppUser:
    return db.query(AppUser).filter(AppUser.id == id).first()


def get_user_by_username(username: str, db: Session) -> AppUser:
    return db.query(AppUser).filter(AppUser.username == username).first()


def update_user_last_login(id: int, last_login_time: datetime, db: Session) -> AppUser:
    db_user = db.query(AppUser).filter(AppUser.id == id).first()
    db_user.last_login_time = last_login_time
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_password(id: int, password: str, db: Session) -> AppUser:
    db_user = db.query(AppUser).filter(AppUser.id == id).first()
    db_user.password = password
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_subscription(
    id: int, access_bitmap, subscription_end_time: datetime, db: Session
) -> AppUser:
    db_user = db.query(AppUser).filter(AppUser.id == id).first()
    db_user.access_bitmap = access_bitmap
    db_user.subscription_end_time = subscription_end_time
    db.commit()
    db.refresh(db_user)
    return db_user
