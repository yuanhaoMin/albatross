from fastapi import APIRouter, Depends
from schema import user_schema
from service import user_service
from sqlalchemy.orm import Session
from util.db_util import get_db


router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login", response_model=user_schema.LoginUserResponse)
def login_user(
    request: user_schema.LoginUserRequest, db: Session = Depends(get_db)
) -> user_schema.LoginUserResponse:
    return user_service.login_user(request, db)


@router.post("/register", response_model=user_schema.RegisterUserResponse)
def register_user(
    request: user_schema.RegisterUserRequest, db: Session = Depends(get_db)
) -> user_schema.RegisterUserResponse:
    return user_service.register_user(request, db)
