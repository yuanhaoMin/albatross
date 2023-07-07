from fastapi import APIRouter, Depends
from schema.user_schema import (
    GetInfoResponse,
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
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
def delete(username: str, db: Session = Depends(get_db)) -> None:
    return user_service.delete_user_by_username(username, db)


@router.get("/info", response_model=GetInfoResponse)
def get_info(username: str, db: Session = Depends(get_db)) -> GetInfoResponse:
    return user_service.get_user_by_username(username, db)


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    return user_service.login_user(request, db)


@router.post("/register", response_model=RegisterResponse)
def register(
    request: RegisterRequest, db: Session = Depends(get_db)
) -> RegisterResponse:
    return user_service.register_user(request, db)


@router.put("/password", response_model=ResetPasswordResponse)
def reset_password(
    request: ResetPasswordRequest, db: Session = Depends(get_db)
) -> ResetPasswordResponse:
    return user_service.update_user_password(request.username, request.password, db)
