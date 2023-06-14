from datetime import datetime
from persistence.user_model import AppUser
from sqlalchemy.orm import Session


def create_user(
    username: str,
    password: str,
    created_time: datetime,
    subscription_end_time: datetime,
    db: Session,
) -> AppUser:
    db_user = AppUser(
        username=username,
        password=password,
        created_time=created_time,
        subscription_end_time=subscription_end_time,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(id: int, db: Session) -> AppUser:
    return db.query(AppUser).filter(AppUser.id == id).first()


def get_user_by_username(username: str, db: Session) -> AppUser:
    return db.query(AppUser).filter(AppUser.username == username).first()


def get_user_by_username_and_password(
    username: str, password: str, db: Session
) -> AppUser:
    return (
        db.query(AppUser)
        .filter(AppUser.username == username, AppUser.password == password)
        .first()
    )


def update_user_last_login(id: int, last_login_time: datetime, db: Session) -> AppUser:
    db_user = db.query(AppUser).filter(AppUser.id == id).first()
    db_user.last_login_time = last_login_time
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_subscription_end_time(
    id: int, subscription_end_time: datetime, db: Session
) -> AppUser:
    db_user = db.query(AppUser).filter(AppUser.id == id).first()
    db_user.subscription_end_time = subscription_end_time
    db.commit()
    db.refresh(db_user)
    return db_user
