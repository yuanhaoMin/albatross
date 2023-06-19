from fastapi import APIRouter, Depends
from schema.user_schema import (
    GetUserResponse,
    LoginUserRequest,
    LoginUserResponse,
    RegisterUserRequest,
    RegisterUserResponse,
)
from service import user_service
from sqlalchemy.orm import Session
from util.db_util import get_db


router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.delete("/delete")
def delete_user(username: str, db: Session = Depends(get_db)) -> None:
    return user_service.delete_user_by_username(username, db)


@router.get("/info", response_model=GetUserResponse)
def get_user_info(username: str, db: Session = Depends(get_db)) -> GetUserResponse:
    return user_service.get_user_by_username(username, db)


@router.post("/login", response_model=LoginUserResponse)
def login_user(
    request: LoginUserRequest, db: Session = Depends(get_db)
) -> LoginUserResponse:
    return user_service.login_user(request, db)


@router.post("/register", response_model=RegisterUserResponse)
def register_user(
    request: RegisterUserRequest, db: Session = Depends(get_db)
) -> RegisterUserResponse:
    return user_service.register_user(request, db)
