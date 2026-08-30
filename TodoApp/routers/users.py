from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

# from database import SessionLocal
from ..database import SessionLocal

# from models import Users
from ..models import Users
from .auth import bcrypt_context, get_current_user

router = APIRouter(prefix="/user", tags=["user"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class UserVerfication(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


class PhoneNumberVerification(BaseModel):
    # phone_number: str = Field(min_length=9, pattern=r"^\d+$")
    phone_number: str = Field(min_length=9, pattern=r"^(\d+|1 \(\d{3}\) \d{3}-\d{4})$")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user["id"]).first()
    # user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found.")

    return user_model

    # return {
    #     "id": user_model.id,
    #     "username": user_model.username,
    #     "email": user_model.email,
    #     "first_name": user_model.first_name,
    #     "last_name": user_model.last_name,
    #     "is_active": user_model.is_active,
    #     "role": user_model.role,
    # }


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    user_verification: UserVerfication,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user["id"]).first()
    # user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found.")

    if not bcrypt_context.verify(
        user_verification.password, user_model.hashed_password
    ):
        # raise HTTPException(status_code=401, detail="Current password is incorrect")
        raise HTTPException(status_code=401, detail="Error on password change")

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put("/phonenumber", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(
    user: user_dependency,
    db: db_dependency,
    user_verification: PhoneNumberVerification,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user["id"]).first()
    # user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found.")

    user_model.phone_number = user_verification.phone_number
    db.add(user_model)
    db.commit()


# @router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
# async def change_phone_number(user: user_dependency,
#                               db: db_dependency,
#                               phone_number: str):

#     if user is None:
#         raise HTTPException(status_code=401, detail="Authentication Failed")
#     user_model = db.query(Users).filter(Users.id == user.get("id")).first()
#     user_model.phone_number = phone_number
#     db.add(user_model)
#     db.commit()


# {
#   "username": "codingwithroby",
#   "email": "codingwithroby@email.com",
#   "first_name": "Eric",
#   "last_name": "Roby",
#   "password": "test1234",
#   "role": "admin"
# }

# {
#   "username": "exampleuser1",
#   "email": "exampleuser1@email.com",
#   "first_name": "Example",
#   "last_name": "User",
#   "password": "test1234",
#   "role": ""
# }
