from fastapi import APIRouter, Depends, HTTPException
from schema import user_schema
from service import user_service
from sqlalchemy.orm import Session
from util.db_util import get_db


router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", response_model=user_schema.RegisterUserResponse)
def register_user(
    request: user_schema.RegisterUserRequest, db: Session = Depends(get_db)
):
    user_with_same_username = user_service.get_by_username(request.username, db)
    if user_with_same_username:
        raise HTTPException(status_code=409, detail="Username already exists")
    return user_service.register(request, db)
