from persistence import user_crud
from schema import user_schema
from sqlalchemy.orm import Session


def register(request: user_schema.UserRegister, db: Session):
    return user_crud.create_user(
        username=request.username, password=request.password, db=db
    )


def get_by_username(username: str, db: Session):
    return user_crud.get_user_by_username(username=username, db=db)
