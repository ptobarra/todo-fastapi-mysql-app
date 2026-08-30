# from fastapi import FastAPI
from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

# from database import SessionLocal
from ..database import SessionLocal

# from models import Users
from ..models import Users

# app = FastAPI()
router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "c685e399ae548fe84b16b04744071744a1d11370899d340f22e4344bad6a2af8"
ALGORITHM = "HS256"

# bcrypt is the hashing algortihm
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    """
    FastAPI dependency that provides a SQLAlchemy database session.
    (provide a SQLAlchemy database session for a request.)

    Yields:
        Session: An active DB session for the current request. (An active
        database session to be used by path operations.)

    Notes:
        - A new session is created per request/use. (Creates a new session
        when the dependency is invoked.)
        - The session is always closed in `finally`, even if an error
        occurs. (Always closes the session in the finally block.)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Reusable type alias for injecting a DB session, so route signatures don't
# repeat the full Annotated[...] each time
db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user
    # return True


def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(UTC) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        user_id: int | None = payload.get("id")
        user_role: str | None = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return {"username": username, "id": user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        ) from None


# @app.get("/auth/")
# @router.get("/auth/")
# async def get_user():
#     return {'user': 'authenticated'}


# @router.post("/auth/", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        phone_number=create_user_request.phone_number,
        # hashed_password = create_user_request.password,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
    )
    # return create_user_model

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )
        # return "Failed authentication"
    token = create_access_token(
        user.username, user.id, user.role, timedelta(minutes=20)
    )
    return {"access_token": token, "token_type": "bearer"}

    # return "Sucessful Athentication"
    # return form_data.username
    # return "token"


# (.venv) ptobarra@ptobarra-desktop-W11-20230518:
# ~/projects/udemy-fastapi-books/TodoApp$ sqlite3 todosapp.db
# SQLite version 3.45.1 2024-01-30 16:01:20
# Enter ".help" for usage hints.
# sqlite> SELECT * FROM users;
# 1|codingwithroby@email.com|codingwithroby|Eric|Roby|
# $2b$12$vwetGGfxzbZj1Kh30ogaDObpAZkSFIhrNDD9mMbzLtiml5TW2Olci|1|admin
# sqlite> .quit


# uvicorn auth:app --reload

# pip install passlib
# pip install bcrypt==4.0.1

# $ ruff check .
# $ ruff format .

# (.venv) ptobarra@ptobarra-desktop-W11-20230518:~/projects/udemy-fastapi-books$
# openssl rand -hex 32
# c685e399ae548fe84b16b04744071744a1d11370899d340f22e4344bad6a2af8
