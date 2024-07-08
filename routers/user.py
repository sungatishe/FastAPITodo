from typing import Annotated
from fastapi import Depends, HTTPException, Path, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from models import Users
from db import SessionLocal
from routers.auth import get_current_user, bcrypt_context

router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class PasswordRequest(BaseModel):
    password: str = Field(min_length=3)


@router.get("/user_get", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Auth failed")
    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()
    if user_model is None:
        raise HTTPException(status_code=401, detail="There's no info")
    return user_model


@router.put("/change_pass", status_code=status.HTTP_200_OK)
async def change_password(user: user_dependency,
                          password_request: PasswordRequest,
                          db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Auth failed")

    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if user_model is None:
        raise HTTPException(status_code=401, detail="There's no such user")

    user_model.hashed_password = bcrypt_context.hash(password_request.password)

    db.add(user_model)
    db.commit() 

