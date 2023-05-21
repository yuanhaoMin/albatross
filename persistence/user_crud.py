from datetime import datetime
from persistence.user_model import AppUser
from sqlalchemy.orm import Session


def create_user(username: str, password: str, created_time: datetime, db: Session):
    db_user = AppUser(username=username, password=password, created_time=created_time)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(username: str, db: Session):
    return db.query(AppUser).filter(AppUser.username == username).first()
