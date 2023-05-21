from persistence import user_crud
from schema import user_schema
from sqlalchemy.orm import Session
from util.data_util import get_current_berlin_time


def register(request: user_schema.RegisterUserRequest, db: Session):
    created_time = get_current_berlin_time()
    return user_crud.create_user(
        username=request.username,
        password=request.password,
        created_time=created_time,
        db=db,
    )


def get_by_username(username: str, db: Session):
    return user_crud.get_user_by_username(username=username, db=db)
