from typing import Annotated

# from fastapi import FastAPI
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

# from database import engine
# from database import SessionLocal
from ..database import SessionLocal

# import models
# from models import Todos
from ..models import Todos
from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


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
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
