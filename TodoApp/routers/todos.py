from typing import Annotated

# from fastapi import FastAPI
from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

# from database import engine
# from database import SessionLocal
from ..database import SessionLocal

# import models
# from models import Todos
from ..models import Todos
from .auth import get_current_user

# from routers import auth

# app = FastAPI()
router = APIRouter()

# For now, it is easier to delete our `todos.db` and hten recreate it if we
# add anything extra to our todos
# Alembic Section of Course will teach how to enhance DB without deleting
# each time.
# models.Base.metadata.create_all(bind=engine)  # This creates the database
# tables based on the models defined in models.py

# app.include_router(auth.router)


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


class TodoRequest(BaseModel):
    """
    Request body schema for creating or updating a Todo item.

    Attributes:
    title: Short todo title with a minimum length of 3 characters.
    description: Detailed text between 3 and 100 characters.
    priority: Integer priority level from 1 to 5.
    complete: Completion flag indicating whether the todo is done.
    """

    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


# Depends is dependency injection (we've to do something before we execute
# what we're trying to execute)
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    # async def read_all(db: Annotated[Session, Depends(get_db)]):
    """
    Retrieve all Todo items for the authenticated user.

    Args:
        user: Authenticated user payload resolved by get_current_user.
            Expected to contain an "id" key.
        db: SQLAlchemy database session injected by FastAPI dependency.

    Returns:
        list[Todos]: A list of Todo records owned by the authenticated user.

    Raises:
        HTTPException: 401 if authentication fails before the handler runs.
    """
    if user is None:
        raise HTTPException(status_code=401, detail="Authetication Failed")

    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
    # return db.query(Todos).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    """
    Retrieve a single Todo item by ID for the authenticated user.

    Args:
        user: Authenticated user payload resolved by get_current_user.
            Expected to contain an "id" key.
        db: SQLAlchemy database session injected by FastAPI dependency.
        todo_id: Positive integer ID of the Todo to fetch.

    Returns:
        Todos: The matching Todo record owned by the authenticated user.

    Raises:
        HTTPException: 401 if authentication fails or user context is missing.
        HTTPException: 404 if no Todo exists with the given ID for that user.
    """
    if user is None:
        raise HTTPException(status_code=401, detail="Authetication Failed")

    # Uses dependency injection to get a database session (db).
    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found.")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency, db: db_dependency, todo_request: TodoRequest
):
    """
    Create a new Todo item for the authenticated user.

    Args:
    user: Authenticated user payload resolved from get_current_user.
    Must contain the user's id.
    db: SQLAlchemy database session injected by FastAPI dependency.
    todo_request: Validated request body containing the new Todo data.

    Returns:
    None. The Todo is persisted to the database and the endpoint responds
    with HTTP 201 Created.

    Raises:
    HTTPException: 401 if authentication fails or no valid user is available.

    Notes:
    - FastAPI validates todo_request using the TodoRequest model before this
    function runs.
    - The request data is unpacked into a Todos ORM instance.
    - owner_id is set from the authenticated user's id.
    - The new record is added to the session and committed to the database.
    """
    if user is None:
        raise HTTPException(status_code=401, detail="Authetication Failed")
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("id"))

    db.add(todo_model)
    db.commit()

    # @app.post("/todo", status_code=status.HTTP_201_CREATED) registers a
    # POST endpoint at /todo and sets the success status to 201 Created.
    # todo_request: TodoRequest tells FastAPI to read the request body as
    # JSON and validate it against your TodoRequest Pydantic model.
    # Todos(**todo_request.dict()) converts the validated request data into
    # a SQLAlchemy Todos object.
    # db.add(todo_model) stages the new object to be inserted into the
    # database.
    # db.commit() permanently saves that new row to the database.


# in the function parameters TodoRequest objects must come before
# parameters with Path validation
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    """
    Update an existing Todo item by ID for the authenticated user.

    Args:
        user: Authenticated user payload resolved by get_current_user.
            Expected to contain an "id" key.
        db: SQLAlchemy database session injected by FastAPI dependency.
        todo_request: Validated request body containing updated Todo data.
        todo_id: Positive integer ID of the Todo to update.

    Returns:
        None. The Todo is updated in the database and the endpoint responds
        with HTTP 204 No Content.

    Raises:
        HTTPException: 401 if authentication fails or user context is missing.
        HTTPException: 404 if no Todo exists with the given ID for that user.

    Notes:
        - FastAPI validates todo_request before this function runs.
        - The target Todo is filtered by both todo_id and owner_id.
        - Editable fields are updated and the transaction is committed.
    """
    if user is None:
        raise HTTPException(status_code=401, detail="Authetication Failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    # db.add(todo_model) keeps the ORM object in the session, and
    # db.commit() saves the changes.
    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    """
    Delete an existing Todo item by ID for the authenticated user.

    Args:
        user: Authenticated user payload resolved by get_current_user.
            Expected to contain an "id" key.
        db: SQLAlchemy database session injected by FastAPI dependency.
        todo_id: Positive integer ID of the Todo to delete.

    Returns:
        None. The Todo is removed from the database and the endpoint responds
        with HTTP 204 No Content.

    Raises:
        HTTPException: 401 if authentication fails or user context is missing.
        HTTPException: 404 if no Todo exists with the given ID for that user.

    Notes:
        - The target Todo is filtered by both todo_id and owner_id.
        - If found, the matching record is deleted and the transaction is committed.
    """
    if user is None:
        raise HTTPException(status_code=401, detail="Authetication Failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    db.query(Todos).filter(Todos.id == todo_id).filter(
        Todos.owner_id == user.get("id")
    ).delete()

    db.commit()


# .venv/bin/activate
# cd TodoApp/
# uvicorn main:app --reload

# $ sudo apt install sqlite3
# $ which sqlite3
# $ sqlite3 --version
# $ sqlite3 todos.db
# (.venv) ptobarra@ptobarra-desktop-W11-20230518:~/projects/udemy-fastapi-books$ sqlite3
# sqlite> .open ./TodoApp/todos.db

# IN THE COMMAND PROMPT:
# C:\Users\ptoba>sqlite3
# SQLite version 3.53.3 2026-06-26 20:14:12
# Enter ".help" for usage hints.
# Connected to a transient in-memory database.
# Use ".open FILENAME" to reopen on a persistent database.
# sqlite> .quit

# C:\Users\ptoba>
