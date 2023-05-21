import app_user_model
import app_user_schema
from sqlalchemy.orm import Session


def create_user(db: Session, app_user: app_user_schema.AppUserCreate):
    db_user = app_user_model.AppUser(
        username=app_user.username, password=app_user.password)
    db.add(db_user)
    db.commit()
    print(db_user)
    db.refresh(db_user)
    print(db_user)
    return db_user
